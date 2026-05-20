param(
    [Parameter(Mandatory=$true)]
    [string]$ZipPath,

    [Parameter(Mandatory=$true)]
    [string]$CommitMessage
)

# UTE GitHub Agency v1 for Windows PowerShell
# Usage:
#   powershell -ExecutionPolicy Bypass -File .\006-tools\github-agency\ute-update.ps1 C:\path\update.zip "Commit message"

$ErrorActionPreference = "Stop"

Write-Host "UTE GitHub Agency v1"
Write-Host "Repository: $(Get-Location)"
Write-Host "Zip: $ZipPath"
Write-Host "Commit: $CommitMessage"
Write-Host ""

if (!(Test-Path $ZipPath)) {
    throw "Update zip not found: $ZipPath"
}

if (!(Test-Path ".git")) {
    throw "This script must be run from the root of the local Git repository."
}

$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "ERROR: Working tree is not clean."
    git status --short
    exit 1
}

$tmp = New-Item -ItemType Directory -Path ([System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), [System.Guid]::NewGuid().ToString()))

try {
    Expand-Archive -Path $ZipPath -DestinationPath $tmp.FullName -Force

    $src = Join-Path $tmp.FullName "upload-these-files"
    if (!(Test-Path $src)) {
        $src = $tmp.FullName
    }

    Write-Host "Running preflight package checks..."

    $packageReadmes = Get-ChildItem -Path $src -Recurse -Filter "PACKAGE-README.md" -ErrorAction SilentlyContinue
    if ($packageReadmes.Count -gt 0) {
        Write-Host "ERROR: Package contains PACKAGE-README.md files. These are deprecated."
        $packageReadmes | ForEach-Object { Write-Host $_.FullName }
        exit 1
    }

    if (Test-Path (Join-Path $src "README.md")) {
        Write-Host "NOTICE: Package includes root README.md."
        if ($CommitMessage -notmatch "README|Readme|readme") {
            throw "Root README.md change blocked because commit message does not mention README."
        }
    }

    Write-Host "Applying files..."
    Copy-Item -Path (Join-Path $src "*") -Destination "." -Recurse -Force

    Write-Host ""
    Write-Host "Changed files:"
    git status --short

    $changes = git status --porcelain
    if (!$changes) {
        Write-Host "No changes detected. Nothing to commit."
        exit 0
    }

    Write-Host ""
    Write-Host "Running assurance checks..."

    $repoPackageReadmes = Get-ChildItem -Path "." -Recurse -Filter "PACKAGE-README.md" -ErrorAction SilentlyContinue
    if ($repoPackageReadmes.Count -gt 0) {
        Write-Host "ERROR: Repository contains PACKAGE-README.md files after update."
        $repoPackageReadmes | ForEach-Object { Write-Host $_.FullName }
        exit 1
    }

    if (Test-Path "docs\graph.js") {
        $node = Get-Command node -ErrorAction SilentlyContinue
        if ($node) {
            node --check docs\graph.js
        } else {
            Write-Host "NOTICE: node not available; skipping JavaScript syntax check."
        }
    }

    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($python) {
        python - <<'PY'
from pathlib import Path
import json, sys

for p in [Path("docs/data/truth-map-v1.json"), Path("docs/data/truth-index-v1.json")]:
    if p.exists():
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"ERROR: Invalid JSON in {p}: {exc}")
            sys.exit(1)

map_path = Path("docs/data/truth-map-v1.json")
index_path = Path("docs/data/truth-index-v1.json")

if map_path.exists() and index_path.exists():
    m = json.loads(map_path.read_text(encoding="utf-8"))
    idx = json.loads(index_path.read_text(encoding="utf-8"))
    map_ids = {n.get("id") for n in m.get("nodes", []) if n.get("id")}
    index_ids = {t.get("id") for t in idx.get("truths", []) if t.get("id")}
    if map_ids != index_ids:
        print("ERROR: Truth index and map node IDs are not aligned.")
        print("Missing from map:", sorted(index_ids - map_ids))
        print("Missing from index:", sorted(map_ids - index_ids))
        sys.exit(1)
    print(f"JSON check passed. Map/index truth count: {len(map_ids)}")

print("Assurance checks passed.")
PY
    } else {
        Write-Host "NOTICE: python not available; skipping JSON/map-index checks."
    }

    Write-Host ""
    Write-Host "Proceeding to commit and push..."
    git add .
    git commit -m "$CommitMessage"
    git push

    Write-Host ""
    Write-Host "Update pushed successfully."
    Write-Host "GitHub Pages may take a short time to redeploy."
}
finally {
    Remove-Item -Path $tmp.FullName -Recurse -Force -ErrorAction SilentlyContinue
}

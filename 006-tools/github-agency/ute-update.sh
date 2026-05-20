#!/usr/bin/env bash
set -euo pipefail

# UTE GitHub Agency v1
# Usage:
#   ./006-tools/github-agency/ute-update.sh /path/to/update.zip "Commit message"
#
# Run from the root of your local universal-truth-engine repository.

ZIP_PATH="${1:-}"
COMMIT_MESSAGE="${2:-}"

if [ -z "$ZIP_PATH" ] || [ -z "$COMMIT_MESSAGE" ]; then
  echo "Usage: ./006-tools/github-agency/ute-update.sh /path/to/update.zip \"Commit message\""
  exit 1
fi

if [ ! -f "$ZIP_PATH" ]; then
  echo "ERROR: Update zip not found: $ZIP_PATH"
  exit 1
fi

if [ ! -d ".git" ]; then
  echo "ERROR: This script must be run from the root of the local Git repository."
  exit 1
fi

if ! command -v git >/dev/null 2>&1; then
  echo "ERROR: git is not installed or not available in PATH."
  exit 1
fi

if ! command -v unzip >/dev/null 2>&1; then
  echo "ERROR: unzip is not installed or not available in PATH."
  exit 1
fi

echo "UTE GitHub Agency v1"
echo "Repository: $(pwd)"
echo "Zip: $ZIP_PATH"
echo "Commit: $COMMIT_MESSAGE"
echo ""

echo "Checking working tree..."
if [ -n "$(git status --porcelain)" ]; then
  echo "ERROR: Working tree is not clean."
  echo "Please commit, stash, or discard current changes before applying a new UTE update."
  git status --short
  exit 1
fi

TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

echo "Extracting update package..."
unzip -q "$ZIP_PATH" -d "$TMP_DIR"

if [ -d "$TMP_DIR/upload-these-files" ]; then
  SRC="$TMP_DIR/upload-these-files"
else
  SRC="$TMP_DIR"
fi

echo "Running preflight package checks..."

if [ -f "$SRC/PACKAGE-README.md" ]; then
  echo "ERROR: Package contains root PACKAGE-README.md. This is deprecated."
  exit 1
fi

if find "$SRC" -name "PACKAGE-README.md" | grep -q .; then
  echo "ERROR: Package contains PACKAGE-README.md files. These are deprecated."
  find "$SRC" -name "PACKAGE-README.md"
  exit 1
fi

if [ -f "$SRC/README.md" ]; then
  echo "NOTICE: Package includes root README.md."
  echo "This is allowed only for intentional repository presentation repairs."
  echo "Commit message must contain: README"
  case "$COMMIT_MESSAGE" in
    *README*|*Readme*|*readme*) ;;
    *)
      echo "ERROR: Root README.md change blocked because commit message does not mention README."
      exit 1
      ;;
  esac
fi

echo "Applying files..."
# rsync preserves folder structure and overwrites intended files.
if command -v rsync >/dev/null 2>&1; then
  rsync -av "$SRC"/ ./ >/dev/null
else
  cp -R "$SRC"/. ./
fi

echo ""
echo "Changed files:"
git status --short

if [ -z "$(git status --porcelain)" ]; then
  echo "No changes detected. Nothing to commit."
  exit 0
fi

echo ""
echo "Running assurance checks..."

if find . -name "PACKAGE-README.md" | grep -q .; then
  echo "ERROR: Repository contains PACKAGE-README.md files after update."
  find . -name "PACKAGE-README.md"
  exit 1
fi

if [ -f "docs/graph.js" ]; then
  if command -v node >/dev/null 2>&1; then
    node --check docs/graph.js
  else
    echo "NOTICE: node not available; skipping JavaScript syntax check."
  fi
fi

if command -v python3 >/dev/null 2>&1; then
  python3 - <<'PY'
from pathlib import Path
import json, sys

checks = [
    Path("docs/data/truth-map-v1.json"),
    Path("docs/data/truth-index-v1.json"),
]

for path in checks:
    if path.exists():
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"ERROR: Invalid JSON in {path}: {exc}")
            sys.exit(1)

map_path = Path("docs/data/truth-map-v1.json")
index_path = Path("docs/data/truth-index-v1.json")

if map_path.exists() and index_path.exists():
    m = json.loads(map_path.read_text(encoding="utf-8"))
    idx = json.loads(index_path.read_text(encoding="utf-8"))
    map_ids = {n.get("id") for n in m.get("nodes", []) if n.get("id")}
    index_ids = {t.get("id") for t in idx.get("truths", []) if t.get("id")}
    missing_from_map = sorted(index_ids - map_ids)
    missing_from_index = sorted(map_ids - index_ids)
    if missing_from_map or missing_from_index:
        print("ERROR: Truth index and map node IDs are not aligned.")
        print("Missing from map:", missing_from_map)
        print("Missing from index:", missing_from_index)
        sys.exit(1)
    print(f"JSON check passed. Map/index truth count: {len(map_ids)}")

print("Assurance checks passed.")
PY
else
  echo "NOTICE: python3 not available; skipping JSON/map-index checks."
fi

echo ""
echo "Review the changed files above."
echo "Proceeding to commit and push..."
git add .
git commit -m "$COMMIT_MESSAGE"
git push

echo ""
echo "Update pushed successfully."
echo "GitHub Pages may take a short time to redeploy."

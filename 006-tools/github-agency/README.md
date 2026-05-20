# GitHub Agency Option B — Local Controlled Update Pipeline

## Purpose

This package implements Option B for UTE updates:

```text
local script → unzip update pack → assurance checks → commit → push
```

It reduces manual GitHub drag-and-drop while keeping John in control of every push.

---

## Requirements

Install:

1. Git
2. GitHub Desktop or Git CLI
3. A local clone of:

```text
https://github.com/UniversalTruthEngine/universal-truth-engine
```

Optional but recommended:

4. Node.js, for JavaScript syntax checks
5. Python 3, for JSON/map-index checks

---

## macOS / Linux Usage

From the root of your local repository:

```bash
chmod +x ./006-tools/github-agency/ute-update.sh
./006-tools/github-agency/ute-update.sh ~/Downloads/update.zip "Commit message"
```

---

## Windows PowerShell Usage

From the root of your local repository:

```powershell
powershell -ExecutionPolicy Bypass -File .\006-tools\github-agency\ute-update.ps1 C:\path\to\update.zip "Commit message"
```

---

## Built-In Guardrails

The script:

- refuses to run if the working tree is not clean,
- blocks deprecated `PACKAGE-README.md`,
- blocks root `README.md` changes unless the commit message mentions README,
- validates `docs/graph.js` if Node.js is installed,
- validates map/index JSON if Python is installed,
- checks `truth-map-v1.json` and `truth-index-v1.json` alignment,
- commits and pushes only after checks pass.

---

## Recommended Workflow

1. Download a UTE update zip from ChatGPT.
2. Run the script locally.
3. Review the changed files shown by Git.
4. Let the script commit and push if checks pass.
5. Wait for GitHub Pages deployment.
6. Perform assurance check if the map or proof system changed.

---

## Important

This is controlled agency, not blind autonomy.

The user still controls:
- the zip used,
- the commit message,
- the local repository,
- and the final push.

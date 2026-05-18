# Manual Cleanup Note

The root of the GitHub repository currently appears to contain an extra nested folder:

```text
universal-truth-engine/
```

This was likely caused by uploading the wrapper folder from an extracted zip.

Recommended action:

1. Open the `universal-truth-engine/` folder in GitHub.
2. Check whether it duplicates files already present at the repository root.
3. If it is only a duplicate wrapper folder, delete it from GitHub.
4. Keep the root-level folders:
   - `000-governance/`
   - `001-fact-vault/`
   - `002-truth-topology/`
   - `003-machine-readable/`

Do not delete any unique truth entries unless they have first been copied to the correct root-level location.

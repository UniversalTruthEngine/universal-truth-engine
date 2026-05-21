# UTE Toolchain Runbook v1

Recommended workflow:

1. Edit or add Core Truths in `001-fact-vault/`.
2. Run browser proof sync.
3. Run topology generator.
4. Run assurance checks.
5. Commit and push.
6. Verify the live map.

Commands:

```bash
python 006-tools/proof-sync/sync-browser-proofs-v1.py
python 006-tools/topology-generator/generate-topology-v1.py
```

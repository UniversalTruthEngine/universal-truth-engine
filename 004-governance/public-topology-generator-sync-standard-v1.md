# Public Topology Generator Sync Standard v1

The topology generator must write both internal and public topology files.

Required outputs:

```text
003-machine-readable/truth-index-v1.json
003-machine-readable/truth-graph.json
docs/data/truth-index-v1.json
docs/data/truth-map-v1.json
```

UTE Assurance checks the public `docs/data` files, so they must be regenerated together with the internal records.

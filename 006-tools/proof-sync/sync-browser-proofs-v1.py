#!/usr/bin/env python3
from pathlib import Path
import json
root=Path.cwd()
vault=root/'001-fact-vault'
out=root/'docs'/'data'/'proofs'
out.mkdir(parents=True, exist_ok=True)
synced=[]
for folder in sorted(vault.glob('UTE-FV-*')):
    proof=folder/'proof.md'
    if proof.exists():
        (out/f'{folder.name}-proof.md').write_text(proof.read_text(encoding='utf-8', errors='replace'), encoding='utf-8')
        synced.append(folder.name)
print(f'Synced {len(synced)} browser proof files.')

# CLI Usage

```bash
traceguard init
traceguard validate --project traceguard.yaml
traceguard atomize --input requirements/system.md --output build/system_atoms.yaml
traceguard check --project traceguard.yaml
traceguard report --project traceguard.yaml --format markdown
traceguard explain --project traceguard.yaml --parent SYS-REQ-001 --atom SYS-REQ-001.A1
```


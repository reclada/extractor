### Reclada dicts extractor

Parser step to extract vocabulary terms from parsed text and tables

Install:

```bash
pip install git+https://github.com/reclada/extractor.git git+https://github.com/reclada/connector.git
```

Set `DB_URI` with connection uri for your postgresql database. E.g.

```bash
export DB_URI='postgres://postgres:password@127.0.0.1'
```

Run:
```bash
reclada-dicts-extractor document_id text.json [tables.json]
```
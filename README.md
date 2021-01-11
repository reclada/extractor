### Reclada dicts extractor

Parser step to extract vocabulary terms from parsed text and tables

Set `DB_URI` with connection uri for your postgresql database. E.g.

```
export DB_URI='postgres://postgres:password@127.0.0.1'
```

Run:
```
reclada-dicts-extractor document_id [text.json [tables.json]]

```
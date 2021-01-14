import json
from dataclasses import dataclass

from reclada.connector import PgConnector


@dataclass(frozen=True)
class TermVariant:
    id: int
    term_id: int
    text: str


class DictTermRepo(PgConnector):
    def add_document_term(self, document_id, term_variant_id, meta):
        res = self.call_func(
            "add_document_term",
            json.dumps({
                "document_id": document_id,
                "term_variant_id": term_variant_id,
                "meta": meta,
            }),
        )
        return res[0][0]["result"]

    def get_term_variants(self, offset, limit=20):
        res = self.call_func(
            "get_term_variants",
            json.dumps({
                "offset": offset,
                "limit": limit,
            }),
        )
        rows = res[0][0]["result"]
        if not rows:
            return []
        return [
            TermVariant(**row)
            for row in rows
        ]

    def add_document_table(self, document_id, table_data, table_structure, meta):
        res = self.call_func(
            "add_document_table",
            json.dumps({
                "document_id": document_id,
                "data": table_data,
                "structure": table_structure,
                "meta": meta,
            }),
        )
        return res[0][0]["result"]

    def add_document_text(self, document_id, text, meta):
        res = self.call_func(
            "add_document_text",
            json.dumps({
                "document_id": document_id,
                "text": text,
                "meta": meta,
            }),
        )
        return res[0][0]["result"]

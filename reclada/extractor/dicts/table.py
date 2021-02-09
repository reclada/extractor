from collections import namedtuple

from .findterms import extract
from .dict_repo import DictTermRepo

FoundTermInfo = namedtuple("FoundTermInfo", ["col", "row", "term_id", "meta"])


def box_key(cell):
    return cell["bbox"]


def process_table(tree, repo: DictTermRepo, document_id, page_num, table):
    if table.get("header"):
        table["header"].sort(key=box_key)
        for col_num, cell in enumerate(table["header"]):
            yield from process_cell(tree, repo, document_id, page_num, cell, None, col_num, True)
    if table.get("rows"):
        for row_num, row in enumerate(table["rows"]):
            row["cells"].sort(key=box_key)
            for col_num, cell in enumerate(row["cells"]):
                yield from process_cell(tree, repo, document_id, page_num, cell, row_num, col_num, False)


def get_entities(tree, cell):
    entities = []
    for term, text in extract(tree, cell.get("text")):
        if term.text not in entities:
            entities.append(term)
    return entities


def process_cell(tree, repo, document_id, page_num, cell, row_num, col_num, store_entities: bool):
    cell["column"] = str(col_num)
    entities = get_entities(tree, cell)
    if store_entities:
        cell["entities"] = [t.text for t in entities]

    repo.add_document_text(document_id, cell.get("text"),
                           meta={"page": page_num, "bbox": cell.get("bbox")})
    for term in entities:
        yield FoundTermInfo(col_num, row_num, term.id, {"page": page_num, "bbox": cell.get("bbox")})

from collections import namedtuple

from .cells import (
    box_key, separate_rows, unmerge_all_cells,
    unheader, merge_rows,
)
from .dict_repo import DictTermRepo
from .findterms import extract

FoundTermInfo = namedtuple("FoundTermInfo", ["col", "row", "term_id", "meta"])


def process_table(tree, repo: DictTermRepo, document_id, page_num, table):
    if table.get("header"):
        if table.get("cells"):
            table["header"], table["cells"] = unheader(table["header"], table["cells"])
        header = unmerge_all_cells(table["header"])
        header = merge_rows(separate_rows(header))
        table["header"] = sorted(header, key=box_key)
        for col_num, cell in enumerate(table["header"]):
            yield from process_cell(tree, repo, document_id, page_num, cell, None, col_num, True)

    if table.get("cells"):
        rows = separate_rows(unmerge_all_cells(table.pop("cells")))
        table["rows"] = rows
        for row_num, row in enumerate(rows):
            row["cells"].sort(key=box_key)
            for col_num, cell in enumerate(row["cells"]):
                yield from process_cell(tree, repo, document_id, page_num, cell,
                                        row_num, col_num, False)


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

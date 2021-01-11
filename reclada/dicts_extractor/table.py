from .findterms import extract
from .dict_repo import DictTermRepo


def box_key(cell):
    return cell["bbox"]


def process_table(tree, repo: DictTermRepo, document_id, page_num, table):
    if table.get("header"):
        table["header"].sort(key=box_key)
        for n, cell in enumerate(table["header"]):
            process_cell(tree, repo, document_id, page_num, cell, n, True)
    if table.get("rows"):
        for row in table["rows"]:
            row["cells"].sort(key=box_key)
            for n, cell in enumerate(row["cells"]):
                process_cell(tree, repo, document_id, page_num, cell, n, False)


def get_entities(tree, cell):
    entities = []
    for term, text in extract(tree, cell.get("text")):
        if term.text not in entities:
            entities.append(term)
    return entities


def process_cell(tree, repo, document_id, page_num, cell, n, store_entities: bool):
    cell["column"] = str(n)
    entities = get_entities(tree, cell)
    if store_entities:
        cell["entities"] = [t.text for t in entities]

    repo.add_document_text(document_id, cell.get("text"),
                           meta={"page": page_num, "bbox": cell.get("bbox")})
    for term in entities:
        repo.add_document_term(document_id, term.id,
                               meta={"page": page_num, "bbox": cell.get("bbox")})

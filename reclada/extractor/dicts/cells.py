from operator import itemgetter


def unmerge_cell(cell, unmerge_rows=True, unmerge_columns=True):
    if unmerge_columns:
        colspan = cell["colspan"]
    else:
        colspan = 1
    if unmerge_rows:
        rowspan = cell["rowspan"]
    else:
        rowspan = 1
    for i in range(colspan):
        for j in range(rowspan):
            yield {
                "row": cell["row"] + j,
                "column": cell["column"] + i,
                "bbox": cell["bbox"],
                "text": cell["text"]
            }


def box_key(cell):
    bbox = cell["bbox"]
    return bbox["left"], bbox["top"]


default_cell = {
    "row": -1,
    "column": -1,
    "rowspan": 0,
    "colspan": 0,
    "bbox": {
        "left": 0,
        "top": 0,
        "height": 0,
        "width": 0,
    },
    "text": ""
}


def separate_rows(all_cells):
    """
    split cell by their rows
    """
    all_cells = tuple(all_cells)
    if not all_cells:
        return []

    min_row = min(map(itemgetter("row"), all_cells))
    max_row = max(map(itemgetter("row"), all_cells)) + 1
    min_column = min(map(itemgetter("column"), all_cells))
    max_column = max(map(itemgetter("column"), all_cells)) + 1
    rows = [{"cells": [default_cell] * (max_column - min_column)} for _ in range(max_row - min_row)]
    for cell in all_cells:
        rows[cell["row"] - min_row]["cells"][cell["column"] - min_column] = cell
    return rows


def unmerge_all_cells(all_cells, unmerge_rows=True, unmerge_columns=True):
    for cell in all_cells:
        yield from unmerge_cell(cell, unmerge_rows, unmerge_columns)


def unheader(header, all_cells):
    """
    remove "left header" cells from header. Keep only top header
    """
    min_row = min(map(itemgetter("row"), all_cells))
    new_cells = []
    new_header = []
    for cell in header:
        if cell["row"] >= min_row:
            new_cells.append(cell)
        else:
            new_header.append(cell)
    return new_header, all_cells + new_cells


def merge_rows(rows):
    print(*rows, sep="\n")
    for col in zip(*(r["cells"] for r in rows)):
        texts = []
        for c in col:
            if c["text"] and c["text"] not in texts:
                texts.append(c["text"])
        yield {
            "row": col[0]["row"],
            "column": col[0]["column"],
            "text": "->".join(texts),
            "bbox": {
                "left": min(c["bbox"]["left"] for c in col),
                "top": min(c["bbox"]["top"] for c in col),
                "height": sum(c["bbox"]["height"] for c in col),
                "width": max(c["bbox"]["width"] for c in col),
            }
        }

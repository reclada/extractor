import json
import os
import sys
from copy import deepcopy
from datetime import datetime

import ahocorasick

from .dict_repo import DictTermRepo
from .findterms import extract
from .table import process_table

DB_URI = os.getenv("DB_URI")


def create_tree(repo):
    tree = ahocorasick.Automaton()
    offset = 0
    limit = 1000
    part = object()
    while part:
        part = repo.get_term_variants(offset, limit)
        offset += limit
        for term in part:
            tree.add_word(term.text, term)

    tree.make_automaton()
    return tree


FIELDS = {"top_left_x", "top_left_y", "bottom_right_x", "bottom_right_y"}


def is_valid_table(block):
    return block.get("header") or block.get("rows")


def process_tables(tree, document_id, repo, filename):
    with open(filename) as f:
        data = json.load(f)

    for page in data["document"]["pages"]:
        page_num = page["page_num"] + 1
        for block in page["blocks"]:
            bbox = block.pop("bbox", None)
            if block["type"] == "table":
                if not is_valid_table(block):
                    continue
                data = deepcopy(block)
                process_table(tree, repo, document_id, page_num, data)
                repo.add_document_table(document_id, data, block,
                                        meta={"page": page_num, "bbox": bbox})
            if block["type"] == "text":
                repo.add_document_text(document_id, block["text"],
                                       meta={"page": page_num, "bbox": bbox})
                for term, text in extract(tree, block["text"]):
                    repo.add_document_term(document_id, term.id,
                                           meta={"page": page_num, "bbox": bbox})


def main():
    print(datetime.now(), "Start")
    repo = DictTermRepo(DB_URI)
    tree = create_tree(repo)
    document_id = int(sys.argv[1])

    # process_text(tree, document_id, repo, sys.argv[2])

    if len(sys.argv) > 3:
        process_tables(tree, document_id, repo, sys.argv[3])

    repo.commit()


if __name__ == '__main__':
    main()

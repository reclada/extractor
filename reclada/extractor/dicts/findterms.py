import json
import logging

logger = logging.getLogger(__name__)


def is_boundary(c: str):
    if not c:
        return True
    return not (c.isalpha() or c.isdigit() or c == '-')


def is_ok(text, match, pos):
    pos2 = pos + len(match)
    if pos > 0 and not is_boundary(text[pos - 1]):
        return False
    if pos2 < len(text) and not is_boundary(text[pos2]):
        return False
    return True


def extract(tree, text):
    if not text:
        return
    text = text.replace("\n\n", "\0")
    text = text.replace("\n", " ")
    text = text.replace("\0", "\n\n")
    text = text.replace("  ", " ")
    for end_index, term in tree.iter(text):
        original_value = term.text
        start_index = end_index - len(original_value) + 1
        if is_ok(text, original_value, start_index):
            if start_index == 0:
                start_index = 1
            # print(start_index, end_index, (insert_order, original_value), text[start_index - 1:end_index + 2], cn)
            yield term, text


def walk(tree, elem):
    if "text" in elem:
        for term, text in extract(tree, elem["text"]):
            yield term, text, elem
    elif "children" in elem:
        for i in elem["children"]:
            yield from walk(tree, i)


def parse_all(tree, name):
    with open(name) as f:
        data = json.load(f)
    for n, page in enumerate(data):
        for elem in page:
            for term, text, elem in walk(tree, elem):
                yield term, n, text, elem

from collections import Counter
from pathlib import Path

from selectolax.parser import HTMLParser

root = Path("~/Coding/Master-Plan/atlas-corpus/postgresql-16.14/doc/src/sgml/html").expanduser()
CANDIDATES = ["div.sect1", "div.refentry", "div.chapter", "body"]
count: Counter[str] = Counter()

for page in sorted(root.glob("*.html")):
    tree = HTMLParser(page.read_text(encoding="utf-8", errors="replace"))
    for curr in CANDIDATES:
        if tree.css_first(curr):
            count[curr] += 1
            break
    # if loop finishes WITHOUT breaking
    else:
        count["NOTHING"] += 1

    # print out the files that fell to body
    if not any(tree.css_first(s) for s in ["div.sect1", "div.refentry", "div.chapter"]):
        print(page.name)

print(count)

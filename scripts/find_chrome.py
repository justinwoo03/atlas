"""
Rank every class in corpus by
1. Page Coverage: % of pages that has this class
2. Text Share: % of that page's text that is in this class
3. Links: How many links are in this class
"""

import statistics as st
from collections import defaultdict
from pathlib import Path

from selectolax.parser import HTMLParser

root = Path("~/Coding/Master-Plan/atlas-corpus/postgresql-16.14/doc/src/sgml/html").expanduser()
files = sorted(root.glob("*.html"))[:200]  # 200 is probably enough

# wrong root probably
if not files:
    raise SystemExit(f"no .html files under {root}")

page_count = defaultdict(int)
text_share = defaultdict(list)
links = defaultdict(int)  # <a> tags inside class (corpus-wide)
words = defaultdict(int)  # how many words inside this class (corpus-wide)
text_sample = {}  # snippet of text from class just so we can see
scanned = 0

# Loop through all html files
for page in files:
    # errors="replace" -> replace invlaid bytes with special replacement char
    # instead of crashing
    tree = HTMLParser(page.read_text(encoding="utf-8", errors="replace"))
    body = tree.css_first("body")

    total = 0
    if body:
        total = len(body.text(separator=" ", strip=True))

    # Skip pages with no text
    if not total:
        continue

    scanned += 1

    # Step 1: Collect info about every class on this current page
    # Structural elements only

    current_page = defaultdict(list)
    for node in tree.css("div, table, ul, ol, nav, header, footer, aside"):
        current_class = node.attributes.get("class")
        if not current_class:
            continue

        # Key using tag and class
        # ex: div.navheader
        _name = f"{node.tag}.{current_class}"
        current_page[_name].append(node)

    # Step 2: Add current_page info to corpus-wide counts
    for name, nodes in current_page.items():
        texts = [n.text(separator=" ", strip=True) for n in nodes]
        page_count[name] += 1
        text_share[name].append(100 * sum(len(t) for t in texts) / total)
        links[name] += sum(len(n.css("a")) for n in nodes)
        words[name] += sum(len(t.split()) for t in texts)
        text_sample.setdefault(name, texts[0][:80])  # probably enough

print(f"{scanned} pages scanned\n")
print(f"{'PAGES%':>7}{'TEXTmed':>9}{'TEXTmax':>9}{'LINK/WD':>9}  CLASS")

for k in sorted(page_count, key=lambda k: -page_count[k])[:20]:
    cov = 100 * page_count[k] / scanned
    ld = links[k] / max(words[k], 1)  # words CAN be 0 for an empty div
    print(f"{cov:6.0f}%{st.median(text_share[k]):8.1f}%{max(text_share[k]):8.1f}%{ld:9.2f}  {k}")
    print(f"{'':33}  e.g. {text_sample[k]!r}")

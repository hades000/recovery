import os, re, zipfile
from html.parser import HTMLParser

ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
V3 = os.path.join(ROOT, r"05 Technical architecture\Recovery Workbench Technical Specifications by Module v3.zip")
V4 = os.path.join(ROOT, r"05 Technical architecture\Recovery Workbench Technical Specifications by Module v4.zip")

z3, z4 = zipfile.ZipFile(V3), zipfile.ZipFile(V4)
n3 = [i.filename for i in z3.infolist()]
n4 = [i.filename for i in z4.infolist()]
print("zip members equal:", n3 == n4, len(n4))
ident = [n for n in n4 if z3.read(n) == z4.read(n)]
print("byte-identical members:", len(ident))
print("changed members:", [n for n in n4 if n not in ident])

changed = [n for n in n4 if n not in ident]
bad_tables = []
for name in changed:
    text = z4.read(name).decode("utf-8")
    block, counts = [], []
    for ln in text.splitlines() + [""]:
        if ln.startswith("|"):
            cells = len(ln.strip().strip("|").split("|"))
            block.append(ln)
            counts.append(cells)
        else:
            if block and len(set(counts)) > 1:
                bad_tables.append((name, block[0][:70], sorted(set(counts))))
            block, counts = [], []
print("table width mismatches:", len(bad_tables))
for b in bad_tables[:10]:
    print("  ", b)

html_path = os.path.join(ROOT, r"06 Data\Recovery Workbench Entity Relationship Diagram v4.html")
s = open(html_path, encoding="utf-8").read()
print("html chars", len(s), "ascii", all(ord(c) < 128 for c in s))
print("cards", s.count('<div class="ent '), "views", s.count('class="ent view'), "ext", s.count('class="ent ext'))
print("literal None", s.count(">None<"), "braces", s.count("%s"), s.count("{}"))
for tok in ("loan_account", "account_payment", "load_run", "tracker_inventory", "dq_exception", "contact_point_id"):
    print("  stale", tok, s.count(tok))

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack = []; self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag not in ("meta", "br", "img", "input", "col", "hr", "link"):
            self.stack.append(tag)
    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.errors.append(("unclosed", self.stack.pop()))
            if self.stack:
                self.stack.pop()
        else:
            self.errors.append(("extra", tag))

p = P(); p.feed(s)
print("html tag errors:", p.errors[:8], "open at end:", p.stack[-5:])
print("sections", s.count('<section class="tab"'), "tables", s.count("<table"), s.count("</table>"))

import pymupdf
pdf = pymupdf.open(os.path.join(ROOT, r"06 Data\Recovery Workbench Entity Relationship Diagram v4.pdf"))
print("pdf pages", pdf.page_count, "metadata title", pdf.metadata.get("title"))

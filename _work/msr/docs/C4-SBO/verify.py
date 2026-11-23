"""Re-extracts the new docx and compares it line for line with the Markdown it was rendered from."""
import subprocess, sys, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
WORK = os.path.join(ROOT, "_work", "msr")
SRC_MD = os.path.join(WORK, "docs", "C4-SBO", "Recovery Workbench Story Build Order v4.md")
DOCX = os.path.join(ROOT, "11 Delivery and operations", "Recovery Workbench Story Build Order v4.docx")
OUT = os.path.join(WORK, "docs", "C4-SBO", "verify")

os.makedirs(OUT, exist_ok=True)
subprocess.run([sys.executable, "-I", os.path.join(ROOT, "22 Microservice Realignment", "compat", "convert_sources.py"),
                DOCX, OUT], check=True)
text = open(os.path.join(OUT, "Recovery Workbench Story Build Order v4.md"), encoding="utf-8").read()

def norm(s):
    s = s.replace("\\|", "|").replace("**", "").replace("\u2013", "-").replace("\u2014", "-")
    s = re.sub(r"^\s*[-*]\s+", "", s)
    return re.sub(r"\s+", " ", s).strip()

def sep(s):
    cells = [c.strip() for c in s.strip().strip("|").split("|")]
    return bool(cells) and all(set(c) <= set("-: ") for c in cells)

got = [norm(l) for l in text.splitlines() if norm(l) and not sep(norm(l))]
want = [norm(l) for l in open(SRC_MD, encoding="utf-8") if norm(l) and not sep(norm(l))]

miss = [w for w in want if w not in got]
extra = [g for g in got if g not in want]
print("md lines:", len(want), "extracted lines:", len(got), "missing:", len(miss), "extra:", len(extra))
for m in miss[:8]:
    print("  MISS", m[:160])
for e in extra[:8]:
    print("  EXTRA", e[:160])

# tables and headings of the new file
import docx
d = docx.Document(DOCX)
print("tables:", len(d.tables), "rows per table:", [len(t.rows) for t in d.tables])
print("headings:", [p.text for p in d.paragraphs if p.style.name.startswith("Heading")])
low = text.lower()
print("jira/atlassian:", bool(re.search(r"jira|atlassian", low)),
      "| emails:", re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text))

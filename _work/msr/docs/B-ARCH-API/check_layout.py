"""Check ref prefixes, line endings and component entry layout (read only)."""
from pathlib import Path
import re, yaml

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "05 Technical architecture" / "Recovery Workbench API Specification v4.yaml"
raw = SRC.read_bytes()
print("CRLF:", raw.count(b"\r\n"), "LF:", raw.count(b"\n"))
text = raw.decode("utf-8")
lines = text.splitlines()
print("lines:", len(lines))
print("first line:", repr(lines[0]))
print("last lines:", repr(lines[-3:]))

refs = re.findall(r"\$ref:\s*'?([^'\n]+)'?", text)
pref = {}
for r in refs:
    pref.setdefault(r.split("/")[1] if r.startswith("#/") else "EXTERNAL:" + r, 0)
    pref[r.split("/")[1] if r.startswith("#/") else "EXTERNAL:" + r] += 1
print("ref prefixes:", pref)

# operation blocks: count x-module lines
print("x-module lines:", len(re.findall(r"(?m)^      x-module:", text)))
print("tags blocks:", len(re.findall(r"(?m)^      tags:$", text)))
print("security blocks:", len(re.findall(r"(?m)^      security:", text)))
# path entry indentation check
bad = [l for l in lines if l.startswith(" ") and not l.startswith("  ") and l.strip()]
print("weird indent 1:", bad[:5])
print("paths section keys:", [l for l in lines[:60] if l and not l.startswith(" ")][:20])

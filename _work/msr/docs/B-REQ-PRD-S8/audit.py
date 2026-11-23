import json, re, io, sys
from pathlib import Path

P = Path("03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md")
t = io.open(P, encoding="utf-8").read()

ids = set()
for f in ["_work/msr/gaps/B-REQ-PRD-S8.jsonl", "_work/msr/assumptions/B-REQ-PRD-S8.jsonl"]:
    for line in io.open(f, encoding="utf-8"):
        if line.strip():
            ids.add(json.loads(line)["id"])

cited = set(re.findall(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b", t))
missing = sorted(c for c in cited if c not in ids)
own = sorted(c for c in cited if "PRD-S8" in c)
print("cited CG/ASM:", len(cited), "own:", len(own), "missing:", missing)

def seq(prefix, w=3):
    return sorted({int(m) for m in re.findall(rf"{prefix}-S8-(\d{{{w}}})", t)})

cap = seq("CAP"); fr = seq("FR"); nfr = seq("NFR"); ac = seq("AC"); jrn = sorted({int(m) for m in re.findall(r"JRN-S8-(\d{2})", t)})
rol = sorted({int(m) for m in re.findall(r"ROL-S8-(\d{2})", t)}); oq = sorted({int(m) for m in re.findall(r"OQ-S8-(\d{2})", t)})
for name, s in [("CAP", cap), ("FR", fr), ("NFR", nfr), ("AC", ac), ("JRN", jrn), ("ROL", rol), ("OQ", oq)]:
    gaps = [n for n in range(1, (max(s) if s else 0) + 1) if n not in s]
    print(name, "count", len(s), "max", max(s) if s else 0, "gaps", gaps)

# every FR referenced anywhere must exist in the FR table
fr_tbl = set(int(m) for m in re.findall(r"^\| FR-S8-(\d{3}) \|", t, re.M))
fr_ref = set(int(m) for m in re.findall(r"FR-S8-(\d{3})", t))
print("FR table rows:", len(fr_tbl), "FR refs not in table:", sorted(fr_ref - fr_tbl))
ac_tbl = set(int(m) for m in re.findall(r"^\| AC-S8-(\d{3}) \|", t, re.M))
print("AC table rows:", len(ac_tbl), "AC refs not in table:", sorted(set(int(m) for m in re.findall(r"AC-S8-(\d{3})", t)) - ac_tbl))
nfr_tbl = set(int(m) for m in re.findall(r"^\| NFR-S8-(\d{3}) \|", t, re.M))
print("NFR table rows:", len(nfr_tbl), "NFR refs not in table:", sorted(set(int(m) for m in re.findall(r"NFR-S8-(\d{3})", t)) - nfr_tbl))
cap_tbl = set(int(m) for m in re.findall(r"^\| CAP-S8-(\d{3}) \|", t, re.M))
print("CAP table rows:", len(cap_tbl), "CAP refs not in table:", sorted(set(int(m) for m in re.findall(r"CAP-S8-(\d{3})", t)) - cap_tbl))

# FR coverage by AC
ac_cov = set()
for row in re.findall(r"^\| AC-S8-\d{3} \|([^|]+)\|", t, re.M):
    ac_cov |= set(int(m) for m in re.findall(r"FR-S8-(\d{3})", row))
print("FRs with no AC:", sorted(fr_tbl - ac_cov))

# header
head = t.splitlines()[:6]
print("HEAD1", head[0])
print("HEAD2", head[1])
print("has D-RCV-60:", "D-RCV-60" in t, "tentative count:", t.count("(tentative)"))
print("jira:", bool(re.search(r"(?i)\bjira\b|atlassian", t)), "email:", bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", t)))
bad = re.findall(r"(?m)^\|\s*(?:Product Owner|FDA)\s*\|[^|]*\|[^|]*\|[^|]*\|\s*$", t)
print("approval rows:", len(bad))
print("lines:", len(t.splitlines()), "chars:", len(t))

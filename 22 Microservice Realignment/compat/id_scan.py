"""Find used D-RCV / ADR / DL numbers across the set (md, extracts, xlsx) and allocate free ones."""
import re, sys
from pathlib import Path
import openpyxl
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WORK, write_json

PAT = {"drcv": re.compile(r"\bD-RCV-(\d{2,3})\b"), "adr": re.compile(r"\bADR-(\d{3})\b"), "dl": re.compile(r"\bDL(\d{2,3})\b")}
WANT = {"drcv": [53], "adr": list(range(13, 24)), "dl": list(range(44, 50))}
SKIP = {"22 Microservice Realignment", "23 Document Gaps", "_work", ".git", "node_modules", "temp", "rwb-wt", ".opencode"}
SKIP_FILES = {"AGENTS.md", "opencode.json", "2026-11-22-recovery-microservice-realignment-implementation-plan.md"}
# Only a register assigns an ID. References elsewhere (for example "ADR-013 onward" in Arch v5)
# are the target of the allocation, not a collision.
REGISTER = {"drcv": None, "adr": ("Architecture Decision Record", "Decision Log"), "dl": ("Decision Log",)}

def scan():
    used = {k: set() for k in PAT}
    for p in ROOT.rglob("*"):
        if any(part in SKIP for part in p.parts) or not p.is_file() or p.name in SKIP_FILES:
            continue
        try:
            if p.suffix.lower() in (".md", ".txt", ".yaml", ".yml", ".sql", ".json"):
                txt = p.read_text(encoding="utf-8", errors="ignore")
            elif p.suffix.lower() == ".xlsx" and "Decision" in p.name:
                wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
                txt = " ".join(str(c) for ws in wb.worksheets for r in ws.iter_rows(values_only=True) for c in r if c)
                wb.close()
            else:
                continue
        except Exception:
            continue
        for k, rx in PAT.items():
            if REGISTER[k] and not any(t in p.name for t in REGISTER[k]):
                continue
            used[k].update(int(x) for x in rx.findall(txt))
    for p in (WORK / "extract").rglob("*.md"):
        txt = p.read_text(encoding="utf-8", errors="ignore")
        used["drcv"].update(int(x) for x in PAT["drcv"].findall(txt))
    return used

def allocate(used, want):
    out, nxt = [], (max(used) + 1 if used else want[0])
    for w in want:
        if w in used or w in out:
            while nxt in used or nxt in out:
                nxt += 1
            out.append(nxt); nxt += 1
        else:
            out.append(w)
    return out

def main():
    used = scan()
    ids = {k: allocate(used[k], WANT[k]) for k in PAT}
    res = {"realignment_decision": f"D-RCV-{ids['drcv'][0]}", "adrs": [f"ADR-{n:03d}" for n in ids["adr"]],
           "dl": [f"DL{n}" for n in ids["dl"]], "max_used": {k: max(v) if v else 0 for k, v in used.items()},
           "collisions": {k: sorted(set(WANT[k]) & used[k]) for k in PAT}}
    write_json(WORK / "plan" / "ids.json", res)
    print("A5 OK", res["realignment_decision"], res["adrs"][0], "..", res["adrs"][-1], res["dl"][0], "..", res["dl"][-1], "collisions", res["collisions"])

if __name__ == "__main__":
    main()

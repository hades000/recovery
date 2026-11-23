"""--seed: known gaps/assumptions (A9). default (D1): merge all candidates, dedupe, number, rewrite citations, write registers."""
import argparse, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, R23, F18, WORK, header, next_version, read_json, read_jsonl, write_json, reset_cands, add_gap, add_asm, decision
from xlsx_write import write_book

DEC = decision()

SEV = {"P1": 1, "P2": 2, "P3": 3}
CITE = re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b|\bASM-seed\b|\bASM-A6-fallback\b")
G_HEAD = ["GAP ID", "Title", "Source", "Section", "Description", "Evidence", "Type", "Area", "Severity", "Needed by wave",
          "Legacy ref", "Owner role", "Assumption", "Proposed resolution", "Raised by", "Status"]
A_HEAD = ["ASM ID", "Assumption", "Why", "What was read", "Gap", "Applied in", "Confidence", "How to confirm", "Impact if wrong", "Raised by", "Status"]

SEED_GAPS = [  # title, description, type, severity, area, owner role, needed by wave
    ("RPO and RTO per service not stated", "The NFR Specification and Availability design give programme targets only; Arch v5 has 19 services.", "Missing", "P1", "NFR", "Solution architect", "1"),
    ("Environment names for per-service deployment", "Environment and Deployment Design names environments for one service only.", "Missing", "P2", "Infrastructure", "SCB IT infrastructure lead", "0"),
    ("'Weeks' versus '28 days' retention wording", "The NFR Specification uses both wordings for the same period.", "Conflict", "P2", "NFR", "Business analyst", "1"),
    ("Kafka cluster ownership and sizing", "Arch v5 names Kafka but not which team provisions and sizes the cluster.", "Missing", "P1", "Infrastructure", "SCB IT infrastructure lead", "0"),
    ("Temporal namespace and codec key ownership", "The Temporal and Drools design does not name who issues the codec key.", "Missing", "P2", "Infrastructure", "SCB IT infrastructure lead", "0"),
    ("Schema registry product", "BACKWARD compatibility is required; the registry product is not named.", "Missing", "P2", "Platform", "Solution architect", "0"),
    ("Non-feature tasks NF-01..NF-08 have no story master", "The NF tasks exist only as titles; content is drafted from Arch v5.", "Missing", "P2", "Stories", "Delivery lead", "0"),
    ("Partner gateway hosting (DMZ)", "Arch v5 places the partner gateway in the DMZ; the hosting team and product are not named.", "Missing", "P2", "Infrastructure", "SCB IT infrastructure lead", "4"),
    ("Issue tracker status of Epic 1 not readable in this run", "Build status is taken from the realignment plan, not from the tracker (U6).", "Missing", "P3", "Delivery", "Delivery lead", "1"),
]
SEED_ASMS = [  # text, why, confidence
    ("Parameters and reference data (E1-042, E1-043) are owned by rwb-case", "R-PREC default ruling", "Medium"),
    ("The case list API is owned by rwb-case", "R-PREC default ruling", "Medium"),
    ("The rule package registry is owned by rwb-decision", "R-PREC default ruling", "Medium"),
    ("The interaction ledger is owned by rwb-source-data", "R-PREC default ruling", "Medium"),
    ("Feature flags are a platform library", "R-PREC default ruling", "Medium"),
    ("Release dates are kept unchanged and are tentative; the programme finishes within 8 months", "user decision U7", "High"),
    ("Ownership is a suggestion only; any team may pick up any story", "user decision U3", "High"),
    ("All AI-drafted documents stay in Draft status until the later verification loop", "user decision U8", "High"),
]

def seed():
    reset_cands("SEED")
    for i, (t, d, ty, sv, ar, ow, wv) in enumerate(SEED_GAPS):
        a = add_asm("SEED", f"Until resolved, the plan default is used for: {t}", "seed gap", read="Arch v5, NFR Specification",
                    confidence="Low", confirm=f"{ow} confirms", impact="Stories and documents citing this item change")
        add_gap("SEED", t, d, gtype=ty, severity=sv, area=ar, owner_role=ow, asm=a, needed_by_wave=wv,
                source="Realignment plan Appendix R", proposed="Confirm in the verification loop")
    for t, why, c in SEED_ASMS:
        add_asm("SEED", t, why, read="Realignment plan Appendix R §R1 and §R3", confidence=c, confirm="Product owner or architect confirms")
    print("A9 SEED OK", len(SEED_GAPS), "gaps", len(SEED_GAPS) + len(SEED_ASMS), "assumptions")

def _norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s or "").lower()).strip()

def _s(v):
    if isinstance(v, (list, tuple, set)):
        return str(next(iter(v), ""))
    return "" if v is None else str(v)

def number(gaps, asms):
    m, out_g, by = {}, [], {}
    gaps = [dict(g) for g in gaps]
    asms = [dict(a) for a in asms]
    for g in gaps:
        if isinstance(g.get("asm"), (list, tuple, set)):
            extra = [str(x) for x in list(g["asm"])[1:]]
            if extra:
                g["description"] = str(g.get("description", "")) + f" (Related assumptions: {', '.join(extra)})"
            g["asm"] = _s(g.get("asm"))
    for a in asms:
        a["gap"] = _s(a.get("gap"))
    for g in gaps:
        key = (_norm(g.get("title")), _norm(g.get("legacy_ref")))
        if key in by:
            t = by[key]
            if SEV.get(g.get("severity"), 3) < SEV.get(t.get("severity"), 3):
                t["severity"] = g["severity"]
            if g.get("wp") and g["wp"] not in t["raised_by"].split("; "):
                t["raised_by"] += "; " + g["wp"]
        else:
            t = dict(g); t["raised_by"] = g.get("wp", ""); t["id"] = f"GAP-{len(out_g) + 1:04d}"; t["status"] = "Open"
            by[key] = t; out_g.append(t)
        m[g["id"]] = t["id"]
    out_a, bya = [], {}
    for a in asms:
        key = _norm(a.get("text"))
        if key in bya:
            t = bya[key]
            if a.get("wp") and a["wp"] not in t["raised_by"].split("; "):
                t["raised_by"] += "; " + a["wp"]
        else:
            t = dict(a); t["raised_by"] = a.get("wp", ""); t["id"] = f"ASM-{len(out_a) + 1:04d}"; t["status"] = "Unconfirmed"
            bya[key] = t; out_a.append(t)
        m[a["id"]] = t["id"]
    for t in out_a:
        t["gap"] = m.get(t.get("gap"), t.get("gap", ""))
    for t in out_g:
        t["asm"] = m.get(t.get("asm"), t.get("asm", ""))
    seed_asm = next((t["id"] for t in out_a if "R-PREC default ruling" in t.get("why", "")), "")
    m.setdefault("ASM-seed", seed_asm)
    fb = next((t["id"] for t in out_a if "most frequent legacy module" in t.get("text", "")), "")
    m.setdefault("ASM-A6-fallback", fb)
    return out_g, out_a, m

def rewrite_text(text, m):
    return CITE.sub(lambda x: m.get(x.group(0)) or x.group(0), text)

def rewrite_file(p, m):
    """Rewrite citations in a file created by this run. Returns 1 if changed."""
    p = Path(p); ext = p.suffix.lower()
    if ext in (".md", ".json", ".yaml", ".yml", ".sql", ".txt", ".excalidraw", ".svg"):
        old = p.read_text(encoding="utf-8", errors="replace"); new = rewrite_text(old, m)
        if new != old:
            p.write_text(new, encoding="utf-8"); return 1
        return 0
    if ext == ".xlsx":
        import openpyxl
        wb = openpyxl.load_workbook(p); ch = 0
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    if isinstance(c.value, str) and CITE.search(c.value):
                        c.value = rewrite_text(c.value, m); ch = 1
        if ch:
            wb.save(p)
        return ch
    if ext == ".docx":
        import docx
        d = docx.Document(p); ch = 0
        paras = list(d.paragraphs) + [pp for t in d.tables for r in t.rows for c in r.cells for pp in c.paragraphs]
        for para in paras:
            if CITE.search(para.text):
                new = rewrite_text(para.text, m)
                for i, r in enumerate(para.runs):
                    r.text = new if i == 0 else ""
                ch = 1
        if ch:
            d.save(p)
        return ch
    return 0

def _run_outputs():
    """Every file this run created: queue expect lists + fragments + the split plan story files. Never a baseline file."""
    base = read_json(WORK / "plan" / "baseline.json", {}) or {}
    out = set()
    for q in (WORK / "wp").glob("queue-*.json"):
        for item in json.loads(q.read_text(encoding="utf-8")):
            out.update(item.get("expect", []))
    out.update(str(p.relative_to(ROOT)).replace("\\", "/") for p in (WORK / "fragments").glob("*.json"))
    plan = read_json(WORK / "plan" / "split_plan.json", {}) or {}
    out.update(x["file"] for x in plan.get("slices", []))
    files = []
    for rel in sorted(out):
        p = ROOT / rel
        if rel in base:
            continue
        files += [f for f in p.rglob("*") if f.is_file()] if p.is_dir() else ([p] if p.exists() else [])
    return files

def _imported():
    p = F18 / "aisdlc" / "DOCUMENT-GAPS.md"
    if not p.exists():
        return ["Source"], []
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in p.read_text(encoding="utf-8").splitlines() if l.startswith("|")]
    rows = [r for r in rows if not all(set(c) <= set("-: ") for c in r)]
    if not rows:
        return ["Source"], []
    w = max(len(r) for r in rows)
    return rows[0] + [""] * (w - len(rows[0])), [r + [""] * (w - len(r)) for r in rows[1:]]

def _md(title, head, rows):
    t = [f"# {title}\n", header(), f"Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision {DEC}.\n",
         "| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    t += ["| " + " | ".join(str(v if v is not None else "").replace("|", "/").replace("\n", " ") for v in r) + " |" for r in rows]
    return "\n".join(t) + "\n"

def d1():
    gaps = [g for p in sorted((WORK / "gaps").glob("*.jsonl")) for g in read_jsonl(p)]
    asms = [a for p in sorted((WORK / "assumptions").glob("*.jsonl")) for a in read_jsonl(p)]
    g, a, m = number(gaps, asms)
    write_json(WORK / "plan" / "register_map.json", m)
    gr = [[x["id"], x.get("title"), x.get("source"), x.get("section"), x.get("description"), x.get("evidence"), x.get("type"), x.get("area"),
           x.get("severity"), x.get("needed_by_wave"), x.get("legacy_ref"), x.get("owner_role"), x.get("asm"), x.get("proposed"), x["raised_by"], x["status"]] for x in g]
    ar = [[x["id"], x.get("text"), x.get("why"), x.get("read"), x.get("gap"), x.get("applied_in"), x.get("confidence"), x.get("confirm"),
           x.get("impact"), x["raised_by"], x["status"]] for x in a]
    ih, irows = _imported()
    ng = next_version(R23, "Recovery Workbench Gap Register"); na = next_version(R23, "Recovery Workbench Assumptions Register")
    gt, at = f"Recovery Workbench Gap Register v{ng}", f"Recovery Workbench Assumptions Register v{na}"
    write_book(R23 / f"{gt}.xlsx", {"Gaps": (G_HEAD, gr), "Imported": (ih, irows)}, read_me=header() + f"\n{gt}. Imported sheet: read-only copy of 18 E2E Recovery Workbench/aisdlc/DOCUMENT-GAPS.md.")
    write_book(R23 / f"{at}.xlsx", {"Assumptions": (A_HEAD, ar)}, read_me=header() + f"\n{at}.")
    (R23 / f"{gt}.md").write_text(_md(gt, G_HEAD, gr), encoding="utf-8")
    (R23 / f"{at}.md").write_text(_md(at, A_HEAD, ar), encoding="utf-8")
    changed = sum(rewrite_file(p, m) for p in _run_outputs())
    left = 0
    for p in _run_outputs():
        if p.suffix.lower() in (".md", ".json"):
            left += len(CITE.findall(p.read_text(encoding="utf-8", errors="replace")))
    print(f"D1 OK gaps={len(g)} (from {len(gaps)}) assumptions={len(a)} (from {len(asms)}) files_rewritten={changed} unmapped_citations={left}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--seed", action="store_true"); a = ap.parse_args()
    seed() if a.seed else d1()

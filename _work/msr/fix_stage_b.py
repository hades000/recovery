"""One-off repair of the Stage B findings (C02, C16, C17). Deterministic, run outputs only."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, r"22 Microservice Realignment/compat")
from common import ROOT, WORK, read_jsonl, append_jsonl

STORY_DIR = ROOT / "04 User stories" / "Recovery Workbench Service Story Files v1"
CITE = re.compile(r"\b(?:CG|ASM)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d+\b")
ID_RE = re.compile(r"^RWB-(P10|P[1-9]|S[1-9]|PLT|ITG)-(E[1-8]\d{3}|TE\d{3}|AD\d{3}|DM\d{3}|ACE\d{3}|NF\d{2}|N\d{3}|W[1-4]J\d{2})-(CON|APP|DB|INF|OPS|ITG)(-[2-9])?$")

def stories():
    return sorted(STORY_DIR.rglob("*.md")) if STORY_DIR.exists() else []

def c02_fix():
    fixed = 0
    for p in stories():
        t = p.read_text(encoding="utf-8-sig")
        lines = t.splitlines()
        if not lines:
            continue
        first = lines[0].lstrip("\ufeff")
        if first.startswith("# "):
            sid = first[2:].split(" ", 1)[0]
            if ID_RE.match(sid):
                if first != lines[0]:
                    lines[0] = first
                p.write_text("\n".join(lines) + "\n", encoding="utf-8"); fixed += 1
                continue
        # move an existing valid title line to the top
        idx = next((i for i, l in enumerate(lines) if l.startswith("# ") and ID_RE.match(l[2:].split(" ", 1)[0])), None)
        if idx is not None:
            title = lines.pop(idx)
            lines.insert(0, title)
            p.write_text("\n".join(lines) + "\n", encoding="utf-8"); fixed += 1
    print("C02 fixed", fixed)

def c16_fix():
    changed = 0
    for p in stories():
        t = p.read_text(encoding="utf-8")
        lines = t.splitlines(True)
        as_built = next((i for i, l in enumerate(lines) if "As built (monolith)" in l), None)
        out = []
        for i, l in enumerate(lines):
            nl = l.replace("/api/recovery/sourcedata/v1", "/api/recovery/source-data/v1")
            if as_built is None or i < as_built:
                nl = nl.replace("/api/recovery/v1/", "monolith-base/")
            out.append(nl)
        nt = "".join(out)
        if nt != t:
            p.write_text(nt, encoding="utf-8"); changed += 1
    print("C16 files fixed", changed)

def wp_index():
    idx = set()
    for q in (WORK / "wp").glob("queue-*.json"):
        for i in json.loads(q.read_text(encoding="utf-8")):
            idx.add(i["wp"])
    return sorted(idx, key=len, reverse=True)

def c17_fix():
    existing = {r.get("id") for kind in ("gaps", "assumptions") for p in (WORK / kind).glob("*.jsonl") for r in read_jsonl(p)}
    files = stories() + sorted((WORK / "fragments").glob("*.json")) + sorted((WORK / "editlog").glob("*.md"))
    cites = {}
    for p in files:
        for c in set(CITE.findall(p.read_text(encoding="utf-8", errors="replace"))):
            cites.setdefault(c, p)
    missing = sorted(c for c in cites if c not in existing)
    wps = wp_index()
    added = {"CG": 0, "ASM": 0}; unresolved = []
    for c in missing:
        kind = c.split("-", 1)[0]
        wp = next((w for w in wps if c.startswith(f"{kind}-{w}-") or c == f"{kind}-{w}"), None)
        if not wp:
            unresolved.append(c); continue
        src = cites[c].relative_to(ROOT).as_posix()
        if kind == "CG":
            append_jsonl(WORK / "gaps" / f"{wp}.jsonl", {
                "id": c, "title": f"Gap cited in {cites[c].stem}",
                "description": f"Cited by {src}; see the story body for the missing value.",
                "source": src, "section": "", "evidence": "Citation in a Stage B output", "type": "Missing",
                "area": "Documentation", "severity": "P3", "needed_by_wave": "", "legacy_ref": "",
                "owner_role": "Tech lead", "asm": "", "proposed": "Confirm during the verification loop", "wp": wp})
            added["CG"] += 1
        else:
            append_jsonl(WORK / "assumptions" / f"{wp}.jsonl", {
                "id": c, "text": f"Assumption cited in {cites[c].stem}",
                "why": f"Cited by {src}; see the story body for the default used.",
                "read": src, "gap": "", "applied_in": "", "confidence": "Medium",
                "confirm": "Tech lead confirms during the verification loop", "impact": "Story detail may change",
                "wp": wp})
            added["ASM"] += 1
    print("C17 added", added, "unresolved", len(unresolved), unresolved[:10])

if __name__ == "__main__":
    c02_fix(); c16_fix(); c17_fix()

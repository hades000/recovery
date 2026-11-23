"""B-P4-01 second probe: legacy AC bodies, legacy TC ids, section 16 shape."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "22 Microservice Realignment" / "checks"))
import run_all as R

FOLDER = ROOT / "04 User stories" / "Recovery Workbench Service Story Files v1" / "RWB-SVC-P4 rwb-access (Access and authority)"
LEG = {
 "RWB-E1-022": ROOT / "04 User stories" / "Recovery Workbench User Stories Epic 1 Story Files v7" / "RWB E1 022 Sign on with SSO MFA and the first roles v1.md",
 "RWB-E1-037": ROOT / "04 User stories" / "Recovery Workbench User Stories Epic 1 Story Files v7" / "RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md",
 "RWB-E1-039": ROOT / "04 User stories" / "Recovery Workbench User Stories Epic 1 Story Files v7" / "RWB E1 039 Access log into the decision log and break glass admin v1.md",
 "RWB-E2-019": ROOT / "04 User stories" / "Recovery Workbench User Stories Epic 2 Story Files v5" / "RWB E2 019 Partner identities through the external gateway v1.md",
 "RWB-AD-001": ROOT / "04 User stories" / "Recovery Workbench Administration Stories v3.md",
}
WP = ROOT / "_work" / "msr" / "wp" / "B-P4-01.md"
lines = [l for l in WP.read_text(encoding="utf-8").splitlines() if l.startswith('{"id"')]
stories = [json.loads(l) for l in lines]

def acs_from(t):
    """map AC id -> list of body lines (Given/When/Then/And) inside the gherkin block."""
    out, cur = {}, None
    for line in t.split("```gherkin", 1)[-1].split("```", 1)[0].splitlines():
        m = re.match(r"^\s*Scenario:\s*(AC\d+)\b", line)
        if m:
            cur = m.group(1); out[cur] = []; continue
        if cur is None:
            continue
        s = line.strip()
        if not s:
            cur = None; continue
        if re.match(r"^(Given|When|Then|And)\b", s):
            out[cur].append(s)
        else:
            cur = None
    return out

fails = []
for st in stories:
    p = ROOT / st["file"]
    t = p.read_text(encoding="utf-8")
    leg = LEG[st["legacy"]].read_text(encoding="utf-8")
    legacs = acs_from(leg)
    mine = acs_from(t)
    s7 = t.split("### 7.", 1)[1].split("### 8.", 1)[0]
    scens = dict(re.findall(r"(?m)^\s*Scenario:\s*(AC\d+)[^\n]*\((legacy [^)]+|new, D-RCV-60)\)", s7))
    owned = st["acs"]
    if sorted(mine) != sorted(scens):
        fails.append(f"{st['id']}: parsed {sorted(mine)} vs tagged {sorted(scens)}")
    for ac in owned:
        if ac not in mine:
            fails.append(f"{st['id']}: owned {ac} has no scenario")
            continue
        if f"(legacy {st['legacy']} {ac})" not in scens.get(ac, ""):
            fails.append(f"{st['id']}: {ac} tag {scens.get(ac)!r}")
        src = legacs.get(ac, [])
        got = mine[ac]
        # allow one substituted Given on a mocked boundary
        diffs = []
        for i, (a, b) in enumerate(zip(src, got)):
            if a != b:
                diffs.append((i, a, b))
        if len(src) != len(got):
            fails.append(f"{st['id']}: {ac} body length {len(got)} vs legacy {len(src)}")
        for (i, a, b) in diffs:
            if a.startswith("Given the ") and b.startswith("Given the ") and "mock" in b:
                continue
            fails.append(f"{st['id']}: {ac} line {i} differs:\n    legacy: {a}\n    mine  : {b}")
    if not owned:
        # new-only slice: every scenario must be tagged new
        for ac, tag in scens.items():
            if "new, D-RCV-60" not in tag:
                fails.append(f"{st['id']}: {ac} on a new-only slice is not tagged new")
        if not scens:
            fails.append(f"{st['id']}: no scenarios at all")
    # section 16 table: TC ids and the Level column
    s16 = t.split("### 16.", 1)[1].split("### 17.", 1)[0]
    if not re.search(r"\|\s*Level\s*\|", s16):
        fails.append(f"{st['id']}: section 16 has no Level column")
    found = set(re.findall(r"\bTC-[A-Z0-9]+-\d{3}-\d{2}\b", s16))
    missing = [x for x in st["tcs_legacy"] if x not in t]
    if missing:
        fails.append(f"{st['id']}: legacy TC ids absent from the file: {missing}")

print("stories:", len(stories), "FAILS:", len(fails))
for x in fails[:40]:
    print(" -", x)

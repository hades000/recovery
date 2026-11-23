"""B-P4-01 probe 2b: legacy AC bodies are preserved in order; extra lines are only mocked Givens."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "22 Microservice Realignment" / "checks"))
import run_all as R

FOLDER = ROOT / "04 User stories" / "Recovery Workbench Service Story Files v1" / "RWB-SVC-P4 rwb-access (Access and authority)"
LEG = {
 "RWB-E1-022": ROOT / "04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 022 Sign on with SSO MFA and the first roles v1.md",
 "RWB-E1-037": ROOT / "04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md",
 "RWB-E1-039": ROOT / "04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 039 Access log into the decision log and break glass admin v1.md",
 "RWB-E2-019": ROOT / "04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5/RWB E2 019 Partner identities through the external gateway v1.md",
 "RWB-AD-001": ROOT / "04 User stories/Recovery Workbench Administration Stories v3.md",
}
WP = ROOT / "_work/msr/wp/B-P4-01.md"
stories = [json.loads(l) for l in WP.read_text(encoding="utf-8").splitlines() if l.startswith('{"id"')]

def acs(t):
    out, cur = {}, None
    for line in t.split("```gherkin", 1)[-1].split("```", 1)[0].splitlines():
        m = re.match(r"^\s*Scenario:\s*(AC\d+)\b", line)
        if m:
            cur = m.group(1); out[cur] = []; continue
        if cur is None: continue
        s = line.strip()
        if not s: cur = None; continue
        if re.match(r"^(Given|When|Then|And)\b", s): out[cur].append(s)
        else: cur = None
    return out

fails, mocked = [], 0
for st in stories:
    t = (ROOT / st["file"]).read_text(encoding="utf-8")
    leg = acs(LEG[st["legacy"]].read_text(encoding="utf-8"))
    mine = acs(t)
    s7 = t.split("### 7.", 1)[1].split("### 8.", 1)[0]
    tags = {m.group(1): m.group(2) for m in re.finditer(r"(?m)^\s*Scenario:\s*(AC\d+)[^(]*\((legacy [^)]+|new, D-RCV-60)\)", s7)}
    if sorted(mine) != sorted(tags):
        fails.append(f"{st['id']}: scenarios {sorted(mine)} vs tags {sorted(tags)}")
    if st["acs"]:
        for ac in st["acs"]:
            if ac not in mine: fails.append(f"{st['id']}: owned {ac} missing"); continue
            if tags.get(ac) != f"legacy {st['legacy']} {ac}":
                fails.append(f"{st['id']}: {ac} tag {tags.get(ac)!r}")
            src, got = leg.get(ac, []), mine[ac]
            i = 0
            for ln in got:
                if i < len(src) and ln == src[i]:
                    i += 1; continue
                if ln.startswith("Given the ") and "mock" in ln:
                    mocked += 1; continue
                fails.append(f"{st['id']}: {ac} line not in legacy and not a mocked Given: {ln[:95]}")
            if i != len(src):
                fails.append(f"{st['id']}: {ac} dropped {len(src)-i} legacy line(s), last kept idx {i}")
    else:
        for ac, tag in tags.items():
            if tag != "new, D-RCV-60":
                fails.append(f"{st['id']}: {ac} is not tagged new on a new-only slice")
        if not tags: fails.append(f"{st['id']}: no scenarios")
    s16 = t.split("### 16.", 1)[1].split("### 17.", 1)[0]
    if not re.search(r"\|\s*Level\s*\|", s16): fails.append(f"{st['id']}: no Level column")
    missing = [x for x in st["tcs_legacy"] if x not in t]
    if missing: fails.append(f"{st['id']}: legacy TCs absent: {missing}")

print("stories:", len(stories), "mocked Givens:", mocked, "FAILS:", len(fails))
for x in fails[:40]: print(" -", x)

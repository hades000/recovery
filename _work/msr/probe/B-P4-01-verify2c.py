"""B-P4-01 probe 2c: legacy AC bodies preserved, mocked Givens only, values kept."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FENCE = "```"
WP = ROOT / "_work/msr/wp/B-P4-01.md"
LEG = {
 "RWB-E1-022": ROOT / "04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 022 Sign on with SSO MFA and the first roles v1.md",
 "RWB-E1-037": ROOT / "04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md",
 "RWB-E1-039": ROOT / "04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 039 Access log into the decision log and break glass admin v1.md",
 "RWB-E2-019": ROOT / "04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5/RWB E2 019 Partner identities through the external gateway v1.md",
 "RWB-AD-001": ROOT / "04 User stories/Recovery Workbench Administration Stories v3.md",
}
stories = [json.loads(l) for l in WP.read_text(encoding="utf-8").splitlines() if l.startswith('{"id"')]


def acs(t):
    out, cur = {}, None
    block = t.split(FENCE + "gherkin", 1)[-1].split(FENCE, 1)[0]
    for line in block.splitlines():
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


def mocked(line):
    return line.startswith("Given the ") and " contract mock returns " in line


def keeps_values(src_line, got_line):
    return all(tok in got_line for tok in re.findall(r'"[^"]+"', src_line))


def match(src, got):
    """True when src is a subsequence of got; a mocked Given may insert or substitute a line."""
    seen = set()
    stack = [(0, 0)]
    while stack:
        i, j = stack.pop()
        if (i, j) in seen:
            continue
        seen.add((i, j))
        if i == len(src) and j == len(got):
            return True
        if j >= len(got):
            continue
        if i < len(src) and src[i] == got[j]:
            stack.append((i + 1, j + 1))
        if mocked(got[j]):
            stack.append((i, j + 1))
            if i < len(src) and keeps_values(src[i], got[j]):
                stack.append((i + 1, j + 1))
    return False


fails, mocked_n = [], 0
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
            if ac not in mine:
                fails.append(f"{st['id']}: owned {ac} missing"); continue
            if tags.get(ac) != f"legacy {st['legacy']} {ac}":
                fails.append(f"{st['id']}: {ac} tag {tags.get(ac)!r}")
            src, got = leg.get(ac, []), mine[ac]
            mocked_n += sum(1 for x in got if mocked(x))
            if not match(src, got):
                fails.append(f"{st['id']}: {ac} body does not preserve the legacy lines")
                for x in got:
                    if x not in src and not mocked(x):
                        fails.append(f"    extra: {x[:90]}")
    else:
        for ac, tag in tags.items():
            if tag != "new, D-RCV-60":
                fails.append(f"{st['id']}: {ac} is not tagged new")
        if not tags:
            fails.append(f"{st['id']}: no scenarios")
    s16 = t.split("### 16.", 1)[1].split("### 17.", 1)[0]
    if not re.search(r"\|\s*Level\s*\|", s16):
        fails.append(f"{st['id']}: no Level column")
    missing = [x for x in st["tcs_legacy"] if x not in t]
    if missing:
        fails.append(f"{st['id']}: legacy TCs absent: {missing}")

print("stories:", len(stories), "mocked Givens:", mocked_n, "FAILS:", len(fails))
for x in fails[:40]:
    print(" -", x)

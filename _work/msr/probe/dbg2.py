import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
FENCE = "```"
leg = (ROOT / "04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 022 Sign on with SSO MFA and the first roles v1.md").read_text(encoding="utf-8")
sto = (ROOT / "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1022 APP Sign-on with SSO, MFA and the first roles v1.md").read_text(encoding="utf-8")


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


a, b = acs(leg)["AC2"], acs(sto)["AC2"]
for x in a:
    print("LEG", [hex(ord(c)) for c in x if ord(c) > 126], repr(x))
for x in b:
    print("STO", [hex(ord(c)) for c in x if ord(c) > 126], repr(x))
print("eq:", a[1] == b[2], len(a[1]), len(b[2]))

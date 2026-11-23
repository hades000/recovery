import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
leg = (ROOT / "04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7/RWB E1 022 Sign on with SSO MFA and the first roles v1.md").read_text(encoding="utf-8")
FENCE = "```"


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


d = acs(leg)
print("scenarios:", len(d), sorted(d))
for l in d["AC2"]:
    print(repr(l))

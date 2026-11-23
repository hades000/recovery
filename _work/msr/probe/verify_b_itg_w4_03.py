import json
from pathlib import Path

root = Path(__file__).resolve().parents[3]
L = (root / "04 User stories/Recovery Workbench Data Migration Stories v3.md").read_text(encoding="utf-8").splitlines()
ranges = {
    "RWB-DM-008": (466, 549),
    "RWB-DM-009": (551, 633),
    "RWB-DM-010": (635, 712),
    "RWB-DM-011": (716, 796),
    "RWB-DM-012": (800, 878),
}
FENCE = "`" * 3


def scen(lines, start, end, label):
    i = start - 1
    while i < end:
        s = lines[i].strip()
        if s == "Scenario: " + label or s.startswith("Scenario: " + label + " "):
            out = [s]
            i += 1
            while i < end and lines[i].strip() and not lines[i].strip().startswith("Scenario:") and lines[i].strip() != FENCE:
                out.append(lines[i].strip())
                i += 1
            return out
        i += 1
    return None


for k, lk, owned in [
    ("DM008", "RWB-DM-008", ["AC1", "AC2"]),
    ("DM009", "RWB-DM-009", ["AC2"]),
    ("DM010", "RWB-DM-010", ["AC2"]),
    ("DM011", "RWB-DM-011", ["AC2"]),
    ("DM012", "RWB-DM-012", ["AC2"]),
]:
    frag = json.load(open(root / f"_work/msr/fragments/RWB-ITG-{k}-ITG.json", encoding="utf-8"))
    S = (root / frag["file"]).read_text(encoding="utf-8").splitlines()
    a0, b0 = ranges[lk]
    for a in owned:
        lb = scen(L, a0, b0, a)
        sb = scen(S, 1, len(S), a)
        body_l = [x for x in lb if not x.startswith("Scenario:")]
        body_s = [x for x in sb if not x.startswith("Scenario:")]
        print(k, a, "verbatim", body_l == body_s)
        if body_l != body_s:
            print("  L", body_l)
            print("  S", body_s)

from pathlib import Path

FENCE = "`" * 3
legacy = Path("04 User stories/Recovery Workbench User Stories Epic 2 Story Files v5/RWB E2 038 Temporal security codec server and admin audit v1.md").read_text(encoding="utf-8")
mine = Path("04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-WF Temporal workflow platform/RWB PLT E2038 APP Temporal security, codec server and admin audit v1.md").read_text(encoding="utf-8")


def block(t):
    seg = t.split(FENCE + "gherkin")[1].split(FENCE)[0]
    return [l for l in seg.splitlines() if l.strip()]


lb, mb = block(legacy), block(mine)
for n in range(1, 8):
    mb = [l.replace(f" (legacy RWB-E2-038 AC{n})", "") for l in mb]
print("identical:", lb == mb, len(lb), len(mb))
for a, b in zip(lb, mb):
    if a != b:
        print("L:", a)
        print("M:", b)

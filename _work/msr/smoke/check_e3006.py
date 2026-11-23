import json, re, pathlib

root = pathlib.Path(".")
files = [
    root / "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3006 APP Calculate the plan installment v1.md",
    root / "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S2 rwb-treatment (Treatment and offer)/RWB S2 E3006 CON Calculate the plan installment - contract v1.md",
]
want = ["Story","Business rationale","Preconditions","Flow","Exception paths","INVEST check","Acceptance criteria","Business rules","State transitions","Authority","Data","Contract","Solution plan","Validation and messages","Screens and states","Test cases","Guardrails","Traceability","Out of scope"]
rows = ["Story key","Work type","Suggested owner","Service","Service epic","Wave","Business epic","Release","Legacy key","Legacy disposition","Build status","Patterns applied","Parallel lane","Ready to start","Depends on (build)","Contract dependencies","Integration dependencies","External dependencies","PRD reference","Status"]
for f in files:
    t = f.read_text(encoding="utf-8")
    print("==", f.name, len(t.encode("utf-8")), "bytes", len(t.splitlines()), "lines")
    heads = re.findall(r"^### (\d+)\. (.+)$", t, re.M)
    print("  sections:", len(heads), [h[1] for h in heads] == want)
    order = [int(h[0]) for h in heads]
    print("  order ok:", order == list(range(1, 20)))
    meta = dict(re.findall(r"^\| ([^|]+?) \| (.+?) \|$", t, re.M))
    missing = [r for r in rows if r not in meta]
    print("  metadata missing:", missing)
    if "meta-order" not in dir():
        pass
    present = [r for r in rows if r in meta]
    print("  metadata order ok:", present == rows)
    print("  subsections 12.x:", re.findall(r"^#### 12\.(\d)", t, re.M))
    print("  ac count:", re.findall(r"^  Scenario: (AC\d)", t, re.M))
    print("  origin tags:", len(re.findall(r"\((legacy RWB-E3-006 AC\d|new, D-RCV-60)\)", t)))
    print("  long sections:", [ (h[0],h[1]) for h in heads ] if False else "")
for frag in ["_work/msr/fragments/RWB-S2-E3006-APP.json","_work/msr/fragments/RWB-S2-E3006-CON.json"]:
    d = json.loads(pathlib.Path(frag).read_text(encoding="utf-8"))
    print("frag ok:", frag, sorted(d.keys()))
for jl in ["_work/msr/gaps/B2-S2-001.jsonl","_work/msr/assumptions/B2-S2-001.jsonl"]:
    lines = pathlib.Path(jl).read_text(encoding="utf-8").strip().splitlines()
    for i, l in enumerate(lines):
        json.loads(l)
    print(jl, len(lines), "rows ok")

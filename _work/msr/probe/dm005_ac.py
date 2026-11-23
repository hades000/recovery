import json, re, pathlib
lg = pathlib.Path("04 User stories/Recovery Workbench Data Migration Stories v3.md").read_text(encoding="utf-8")
m = re.search(r"^## RWB-DM-005 .*?(?=^## RWB-DM-006)", lg, re.M|re.S)
blk = m.group(0)
acc = re.search(r"Scenario: AC3 Cut over\n(.*?)```", blk, re.S).group(1).rstrip("\n")
print(repr(acc))
sp = pathlib.Path("04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P1 rwb-source-data (Source data)/RWB P1 DM005 APP Migrate contact and promises v1.md").read_text(encoding="utf-8")
body = re.search(r"Scenario: AC3 Cut over \(legacy RWB-DM-005 AC3\)\n(.*?)```", sp, re.S).group(1)
body = "\n".join(l for l in body.splitlines() if "contract mock returns" not in l).rstrip("\n")
print(repr(body))
print("VERBATIM MATCH:", body == acc)
# metadata compare
frag = json.loads(pathlib.Path("_work/msr/fragments/RWB-P1-DM005-APP.json").read_text(encoding="utf-8"))
meta = dict(re.findall(r"^\| ([^|]+?) \| ([^|]*?) \|$", sp.split("### 1.",1)[0], re.M))
for k,v in meta.items():
    print(f"  {k!r}: {v!r}")

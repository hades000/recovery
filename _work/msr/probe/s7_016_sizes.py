import io, re, os
APP = "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6028 APP Sell a post charge-off population v1.md"
CON = "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6028 CON Sell a post charge-off population - contract v1.md"
for p in (APP, CON):
    t = io.open(p, encoding="utf-8").read()
    parts = re.split(r"(?m)^### (\d+)\. ", t)
    print("==", os.path.basename(p))
    print("0 kb", round(len(parts[0].encode()) / 1024, 1))
    for i in range(1, len(parts), 2):
        body = parts[i + 1]
        print(" s" + parts[i], round(len(body.encode()) / 1024, 1), "kb", len(body.splitlines()), "lines")

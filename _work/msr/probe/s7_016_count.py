import io, re
for p in ("04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6028 APP Sell a post charge-off population v1.md",
          "04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S7 rwb-writeoff (Write-off)/RWB S7 E6028 CON Sell a post charge-off population - contract v1.md"):
    t = io.open(p, encoding="utf-8").read()
    print(p.split("/")[-1], t.count("Not specified in the source documents"))

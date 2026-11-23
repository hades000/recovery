import re,json,io,os,glob
files = sorted(glob.glob("04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E201[2-6]*.md"))
META = ["Story key","Work type","Suggested owner","Service","Service epic","Wave","Business epic","Release","Legacy key","Legacy disposition","Build status","Patterns applied","Parallel lane","Ready to start","Depends on (build)","Contract dependencies","Integration dependencies","External dependencies","PRD reference","Status"]
for f in files:
    t=io.open(f,encoding="utf-8").read()
    head=t.split("### 1.")[0]
    rows=[r for r in re.findall(r"^\|\s*([^|]+?)\s*\|",head,re.M) if r in META]
    print(os.path.basename(f)[:18], "metaOK", rows==META, "| dpr", len(re.findall(r"^\| DP-\d\d \|",t,re.M)), "| cg", sorted(set(re.findall(r"(?:CG|ASM)-B-ITG-W2-03-E\d{4}-\d+",t))), "| badwords", [w for w in ("Jira","atlassian","/api/recovery/v1/","Claude","Co-Authored-By") if w.lower() in t.lower()], "| emails", len(re.findall(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b",t)))
    print("   title:", t.splitlines()[0])
    for line in head.splitlines():
        if line.startswith("| Patterns") or line.startswith("| Integration dep") or line.startswith("| Release") or line.startswith("| Ready"):
            print("   ",line)

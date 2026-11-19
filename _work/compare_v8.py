import glob, re, os
ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
SRC = os.path.join(ROOT, "04 User stories", "Recovery Workbench User Stories Epic 1 Story Files v6")
MD = os.path.join(ROOT, "04 User stories", "Recovery Workbench User Stories Epic 1 v8.md")
md = open(MD, encoding="ascii").read()
blocks = {re.match(r"## (RWB-\S+)", b).group(1): b for b in re.split(r"(?m)^(?=## RWB-)", md) if b.startswith("## RWB-")}
bad = []
for f in sorted(glob.glob(os.path.join(SRC, "RWB*.md"))):
    raw = open(f, encoding="utf-8-sig").read()
    key = re.match(r"^# (RWB-\S+)", raw).group(1)
    b = blocks[key]
    s_acs = set(re.findall(r"(?m)^  Scenario: (AC\d+)", raw))
    d_acs = set(re.findall(r"(?m)^  Scenario: (AC\d+)", b))
    s_tc = set(re.findall(r"(?m)^\| (TC-\S+) \|", raw))
    d_tc = set(re.findall(r"(?m)^\| (TC-\S+) \|", b))
    if s_acs != d_acs: bad.append((key, "acs", s_acs ^ d_acs))
    if s_tc != d_tc: bad.append((key, "tcs", s_tc ^ d_tc))
    if raw.count("## ") - 1 != b.count("### "): bad.append((key, "sections", raw.count("## ")-1, b.count("### ")))
print("BAD", bad)
print("SECTIONS PER STORY OK", not bad)
# story statement comparison
for f in sorted(glob.glob(os.path.join(SRC, "RWB*.md"))):
    raw = open(f, encoding="utf-8-sig").read()
    key = re.match(r"^# (RWB-\S+)", raw).group(1)
    s = re.search(r"(?ms)^## 1\. Story\n(.*?)\n## 2\.", raw).group(1).strip()
    d = re.search(r"(?ms)^### 1\. Story\n(.*?)\n### 2\.", blocks[key]).group(1).strip()
    if key not in ("RWB-TE-004", "RWB-TE-011") and s != d:
        print("STORY DIFF", key)
print("done")

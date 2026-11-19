import io, re, os

BASE = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
for name in ["Recovery Workbench Administration Stories v3.md", "Recovery Workbench Data Migration Stories v3.md"]:
    p = os.path.join(BASE, "04 User stories", name)
    doc = io.open(p, encoding="ascii").read()
    print("==", name)
    blocks = [b for b in re.split(r"(?m)^(?=## RWB-)", doc) if b.startswith("## RWB-")]
    for b in blocks:
        key = re.match(r"## (RWB-\w+-\d+)", b).group(1)
        labels = re.findall(r"(?m)^\*\*([A-Z][^*]+?)\.?\*\*(.*)$", b)
        order = [l[0].strip() for l in labels]
        if "Removed" in b[:200]:
            print("  %-12s REMOVED, has Story label: %s" % (key, "Story" in order))
            continue
        want = ["Story", "Acceptance criteria", "Data", "Endpoints", "Screen and states",
                "Permission checks", "Validation and messages", "Test cases", "Guardrails"]
        if order != want:
            print("  %-12s ORDER %s" % (key, order))
        if b.count("```gherkin") != 1 or b.count("```") != 2:
            print("  %-12s FENCE %d/%d" % (key, b.count("```gherkin"), b.count("```")))
    # table integrity: every table line count of pipes equal within a table
    bad = 0
    for i, ln in enumerate(doc.split("\n")):
        if ln.startswith("|") and ln.count("|") < 2:
            bad += 1
            print("  odd table row line", i + 1, ln[:60])
    print("  blocks:", len(blocks), "odd rows:", bad)

import re, json, sys, os
base = r"04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P10 rwb-agent (Agent)"
files = [
 ("APP", "RWB P10 E2031 APP Agent monitoring dashboard v2 [E3d] v1.md"),
 ("CON", "RWB P10 E2031 CON Agent monitoring dashboard v2 [E3d] - contract v1.md"),
 ("OPS", "RWB P10 E2031 OPS Agent monitoring dashboard v2 [E3d] - deployment v1.md"),
]
out = {}
for tag, name in files:
    p = os.path.join(base, name)
    t = open(p, encoding="utf-8").read()
    asm = sorted(set(int(x) for x in re.findall(r"ASM-B-P10-02-E2031-(\d+)", t)))
    cg = sorted(set(int(x) for x in re.findall(r"CG-B-P10-02-E2031-(\d+)", t)))
    h3 = re.findall(r"(?m)^### (.+)$", t)
    s12 = re.findall(r"(?m)^#### (12\.\d)", t)
    scen = re.findall(r"(?m)^\s*Scenario: (.+)$", t)
    tags = re.findall(r"(?m)^\s*Scenario: .*\((legacy [^)]+|new, D-RCV-60)\)\s*$", t)
    tcs = re.findall(r"(?m)^\| (TC-[A-Za-z0-9-]+) \|", t)
    out[tag] = dict(asm=asm, cg=cg, h3=len(h3), h3names=h3, s12=s12, scen=scen,
                    tags=tags, tcs=tcs,
                    monolith=t.count("/api/recovery/v1"),
                    tent=t.count("(tentative)"),
                    level=t.count("| Level |") + t.count("| Covers | Level |"))
print(json.dumps(out, indent=1, ensure_ascii=True))

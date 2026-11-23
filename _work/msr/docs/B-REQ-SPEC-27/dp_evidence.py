"""B-REQ-SPEC-27: precise decoupling-pattern evidence per FSD module."""
import glob, json, os, re

ROOT = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14"
SRC = os.path.join(ROOT, r"03 Requirements and specifications\Recovery Workbench Functional Specifications by Module v6")

DP = [
    ("DP-01", r"\brecovery\.(?!v_ace_|v_|recovery_svc)[a-z_]+\b|\brecovery schema\b"),
    ("DP-02", r"\brecovery_svc\b"),
    ("DP-03", r"\bDecisionLogWriter\b|\bdecision record\b|\bdecision log\b"),
    ("DP-04", r"\bRuleEvaluator\b|\bDrools\b|\brule package\b"),
    ("DP-05", r"\bAceSourceQuery\b|\bv_ace_|\baccount_ext\b"),
    ("DP-06", r"\bcasewf\.config\b|\bparameter catalog\b|\bparameters?\b"),
    ("DP-07", r"\bLOV-[A-Z0-9-]+|\breference data\b"),
    ("DP-08", r"\bRecoveryAccessGuard\b|\bcapability area\b"),
    ("DP-09", r"\bEV-\d\d\b|\boutbox\b|\bapplication event\b"),
    ("DP-10", r"\bQuartz\b|\bJOB-\d\d\b"),
    ("DP-11", r"\bpublished interface\b"),
    ("DP-12", r"\bone workflow per case\b|\bCaseWorkflow\b"),
    ("DP-13", r"/api/recovery/v1"),
    ("DP-14", r"rwb\.p\d+\.|rwb\.casewf\."),
    ("DP-15", r"\bV0001\b|\bFlyway\b|\bmigration\b"),
    ("DP-16", r"recovery\.integration\.adapter"),
    ("DP-17", r"\bdata lake\b|\bINT-19\b|\bINT-20\b"),
    ("DP-18", r"\binteraction ledger\b"),
    ("DP-19", r"\bace-web\b|\bgateway-bff\b"),
    ("DP-20", r"\bagent client\b"),
]

rows = []
for p in sorted(glob.glob(os.path.join(SRC, "*.md"))):
    t = open(p, encoding="utf-8").read()
    code = re.search(r"FSD (P\d+|S\d+)", os.path.basename(p)).group(1)
    found = {}
    for d, rx in DP:
        hits = [m for m in re.finditer(rx, t)]
        if hits:
            m = hits[0]
            s = max(0, t.rfind("\n", 0, m.start()) + 1)
            e = t.find("\n", m.end())
            found[d] = (len(hits), t[s:e][:110])
    rows.append((code, found))

out = []
for code, found in rows:
    out.append({"code": code, "dp": {k: list(v) for k, v in found.items()}})
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dp.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
for code, found in rows:
    print("##", code, sorted(found))
    for d in sorted(found):
        n, ex = found[d]
        print("   ", d, n, "|", ex)

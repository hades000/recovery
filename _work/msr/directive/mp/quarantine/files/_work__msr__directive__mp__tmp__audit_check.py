import io
p = r"C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\msr\directive\mp\out\RWB-S5-E3021-CON.md"
t = io.open(p, encoding="utf-8").read()
checks = [
    "| ID | Rule | Source | Covered by |\n|---|---|---|---|",
    "| Depends on (build) | RWB-PLT-TE006-CON (wave 0 outbox and inbox library) |",
    "| TC-S5-E3021-CON-04 | AC4, AC5, AC6, AC7, AC8 | Contract | The four consumed rows and their placeholders; the eight fakes match the document and a drifted fake fails the build; the no-`v_ace_*`, no-`legal_action` and no-`recovery_case` boundary |",
]
for s in checks:
    print(t.count(s), len(s), s[:60])

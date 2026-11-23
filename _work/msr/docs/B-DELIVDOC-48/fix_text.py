import sys

import openpyxl

sys.stdout.reconfigure(encoding="utf-8")
P = r"11 Delivery and operations\Recovery Workbench Risks Assumptions Issues and Dependencies v5.xlsx"
wb = openpyxl.load_workbook(P)

risks = wb["Risks"]
risks["A2"] = (
    "27 risks: 26 open and 1 closed by D-RCV-35, with impact, likelihood, action, owner and review date. "
    "Nine realignment risks R1 to R9 are added by D-RCV-60 as R-19 to R-27 (see the Read me sheet); owners point to "
    "the Ownership Map v1 and the realignment positions to the Assumptions Register v1 (folder 23). v5, 22 November 2026."
)
risks["B23"] = (
    "19 services instead of one deployable: delivery, on-call and release load spread over the services and the shared platform"
)

assum = wb["Assumptions"]
assum["A2"] = (
    "Positions the build uses until the bank decides. The realignment positions are held in the Assumptions Register v1 "
    "(folder 23); row A-11 is the pointer."
)

wb.save(P)
print("OK")

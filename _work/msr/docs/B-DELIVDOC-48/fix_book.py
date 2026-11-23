import sys
from copy import copy

import openpyxl

sys.stdout.reconfigure(encoding="utf-8")

P = r"11 Delivery and operations\Recovery Workbench Risks Assumptions Issues and Dependencies v5.xlsx"
wb = openpyxl.load_workbook(P)

RISK_COVER = (
    "27 risks: 26 open and 1 closed by D-RCV-35, with impact, likelihood, action, owner and review date. "
    "Nine realignment risks R1 to R9 are added by D-RCV-60 as R-19 to R-27 (see the Read me sheet); "
    "owners point to the Ownership Map v1. v5, 22 November 2026."
)
DEP_COVER = (
    "36 dependencies from the dependency map, including DEP-36 for the Temporal and Drools version approval. "
    "Owners point to the Ownership Map v1 (D-RCV-60). v5, 22 November 2026."
)

RISK_OWNERS = {
    "R-01": "Solution architect (P1 rwb-source-data)",
    "R-02": "Data lead (P1 rwb-source-data)",
    "R-03": "Tech leads (PLT)",
    "R-04": "Solution architect (P7 rwb-decision)",
    "R-05": "Data lead (P1 rwb-source-data)",
    "R-06": "Product owner (S9 rwb-partner)",
    "R-07": "IT lead (S2 rwb-treatment)",
    "R-08": "ACE team (PLT)",
    "R-11": "Business lead (P6 rwb-comms)",
    "R-12": "CTO with Enterprise AI (P10 rwb-agent)",
    "R-13": "ACE team lead; program manager (P1 rwb-source-data)",
    "R-14": "SCB IT platform lead (PLT)",
    "R-15": "Program manager (PLT)",
    "R-16": "RW-COE lead (P7 rwb-decision)",
    "R-18": "SCB IT architecture (PLT)",
}

DEP_OWNERS = {
    "DEP-01": "ACE team (PLT)",
    "DEP-02": "ACE team (PLT)",
    "DEP-03": "ACE team (PLT)",
    "DEP-04": "ACE team (PLT)",
    "DEP-10": "Architecture team (S9 rwb-partner)",
    "DEP-11": "CTO with Enterprise AI (P10 rwb-agent)",
    "DEP-12": "Solution architect with Risk (PLT)",
    "DEP-17": "Data lead (P1 rwb-source-data)",
    "DEP-20": "Enterprise AI team (P10 rwb-agent)",
    "DEP-21": "Enterprise AI team with Model Risk (P10 rwb-agent)",
    "DEP-22": "Autonomous Ops team (P5 rwb-document)",
    "DEP-25": "Legal counsel (P6 rwb-comms)",
    "DEP-28": "Partner and agency manager (S9 rwb-partner)",
    "DEP-29": "Partner and agency manager (S9 rwb-partner); Head of Asset Liquidity",
    "DEP-30": "Head of Asset Liquidity (S6 rwb-debtsale)",
    "DEP-31": "Partner and agency manager (S9 rwb-partner)",
    "DEP-32": "Guarantee officer (S3 rwb-guarantee)",
    "DEP-33": "Finance and CFO delegate (S7 rwb-writeoff)",
    "DEP-34": "ACE team lead (P1 rwb-source-data)",
    "DEP-35": "Sponsor with the ACE team lead (P1 rwb-source-data)",
    "DEP-36": "SCB IT architecture (PLT)",
}


def restyle(ws, first_new, last_new, template_row, ncols):
    for r in range(first_new, last_new + 1):
        for c in range(1, ncols + 1):
            src = ws.cell(row=template_row, column=c)
            dst = ws.cell(row=r, column=c)
            dst.font = copy(src.font)
            dst.alignment = copy(src.alignment)
            if src.border.left is not None:
                dst.border = copy(src.border)


risks = wb["Risks"]
risks["A2"] = RISK_COVER
for r in range(5, risks.max_row + 1):
    key = risks.cell(row=r, column=1).value
    if key in RISK_OWNERS:
        risks.cell(row=r, column=6).value = RISK_OWNERS[key]
restyle(risks, 23, 31, 22, 8)
risks.auto_filter.ref = "A4:H31"

assum = wb["Assumptions"]
restyle(assum, 15, 15, 14, 4)
assum.auto_filter.ref = "A4:D15"

deps = wb["Dependencies"]
deps["A2"] = DEP_COVER
for r in range(5, deps.max_row + 1):
    key = deps.cell(row=r, column=1).value
    if key in DEP_OWNERS:
        deps.cell(row=r, column=6).value = DEP_OWNERS[key]

readme = wb["Read me"]
wb.move_sheet("Read me", offset=-(wb.sheetnames.index("Read me")))
readme.column_dimensions["A"].width = 150
for r in range(1, readme.max_row + 1):
    cell = readme.cell(row=r, column=1)
    cell.alignment = openpyxl.styles.Alignment(wrap_text=True, vertical="top")
    cell.font = openpyxl.styles.Font(name="Aptos", size=10, bold=(r == 4 or cell.value in ("Change log", "Realignment notes")))
readme.cell(row=1, column=1).font = openpyxl.styles.Font(name="Aptos", size=16, bold=True)

wb.save(P)
wb2 = openpyxl.load_workbook(P)
print(wb2.sheetnames)
for ws in wb2.worksheets:
    print(ws.title, ws.max_row, ws.max_column, ws.auto_filter.ref)
print("Risks A2:", wb2["Risks"]["A2"].value)
print("R-19:", [wb2["Risks"].cell(row=23, column=c).value for c in (1, 6, 7, 8)])
print("A-11:", [wb2["Assumptions"].cell(row=15, column=c).value for c in (1, 3, 4)])
print("DEP-34 owner:", wb2["Dependencies"].cell(row=38, column=6).value)
print("Read me A8:", wb2["Read me"]["A8"].value)

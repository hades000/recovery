# -*- coding: utf-8 -*-
"""Build Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v3 from v2."""
import copy, shutil, datetime
import openpyxl

SRC = r"04 User stories\Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v2.xlsx"
DST = r"04 User stories\Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v3.xlsx"

shutil.copyfile(SRC, DST)
wb = openpyxl.load_workbook(DST)
ws = wb["Defects"]

# ---- fill the five rows that lost their story key and step
fill = {5: ("RWB-E1-042", "10"), 6: ("RWB-E1-066", "1"), 7: ("RWB-E2-031", "header"),
        8: ("RWB-E2-017", "8, 9"), 9: ("RWB-E1-012", "6, 9")}
for r, (k, s) in fill.items():
    ws.cell(r, 1).value = k
    ws.cell(r, 2).value = s

# ---- close the rows answered by the D-RCV-35 rewrite or removal
CLOSED = {
    9: "Closed 15 Nov 2026. RWB-E1-012 is removed under D-RCV-35 U1; the retirement procedure "
       "now sits in the Cutover and Go Live Plan and no tracker screen or endpoint is built.",
    13: "Closed 15 Nov 2026. RWB-E1-003 is removed under D-RCV-35 U1; the ALS load is ACE "
        "ingestion and the story is not in the set.",
    14: "Closed 15 Nov 2026. RWB-E1-005 is removed under D-RCV-35 U1; the tracker inventory now "
        "sits in the Cutover and Go Live Plan.",
    15: "Closed 15 Nov 2026. The inbound half of RWB-E1-007 is removed under D-RCV-35 U1; the "
        "story now carries four outbound interfaces only (INT-14, INT-19, INT-20 and INT-25).",
    16: "Closed 15 Nov 2026. The inbound half of RWB-E1-007 is removed under D-RCV-35 U1; the "
        "CCMS stale rule leaves with the CCMS load and the story reads dataAsOf from the views.",
    17: "Closed 15 Nov 2026. The inbound half of RWB-E1-007 is removed under D-RCV-35 U1; INT-14 "
        "is now an outbound interface and its retry intervals come from the outbound_item row.",
    18: "Closed 15 Nov 2026. RWB-E1-010 is removed under D-RCV-35 U1; the tracker load and its "
        "container name now sit in the Cutover and Go Live Plan.",
    23: "Closed 15 Nov 2026. RWB-E1-015 is rewritten on the ACE read path; its header lists "
        "RWB-E1-001, RWB-E1-069 and RWB-E1-027, so the dependency the row names is present.",
    103: "Closed 15 Nov 2026. RWB-E1-010 is removed under D-RCV-35 U1; the tracker load and its "
         "AC13 leave with it.",
    106: "Closed 15 Nov 2026. RWB-E1-012 is removed under D-RCV-35 U1; the six-team report and "
         "its filing are in the Cutover and Go Live Plan.",
    110: "Closed 15 Nov 2026. RWB-E1-006 is removed under D-RCV-35 U1; its daily gate moves into "
         "RWB-E1-015, which carries the ACE batch completeness rule.",
    113: "Closed 15 Nov 2026. The inbound half of RWB-E1-007 is removed under D-RCV-35 U1; INT-15 "
         "is an inbound interface and no longer appears in the story.",
    11: "Closed 15 Nov 2026. DL41 is ruled and the counts are superseded by D-RCV-35: 92 tables, "
        "30 views, 122 sys_objects and 1,366 sys_fields, carried by RWB-E1-001 v8 and RWB-E1-064.",
    82: "Closed 15 Nov 2026. DL42 was decided on 5 November as D-RCV-28; every migration is named "
        "V<4-digit seq>__<story>_<name>.sql with ${recoverySchema}, and RWB-E1-001 v8 carries it.",
    83: "Closed 15 Nov 2026. DL42 was decided on 5 November as D-RCV-28; every migration is named "
        "V<4-digit seq>__<story>_<name>.sql with ${recoverySchema}, and RWB-E1-001 v8 carries it.",
}
for r, text in CLOSED.items():
    ws.cell(r, 4).value = text
    ws.cell(r, 7).value = "15 Nov 2026"

# ---- five new rows for the ACE read path
last = ws.max_row
style = {c: copy.copy(ws.cell(last, c)._style) for c in range(1, 8)}
new = [
    ["All retained Workbench tables", "",
     "DEF-05: 42 fields on the retained tables still carry a source system and a source field from "
     "the copy design (hearing, legal_action, notice, write_off, asset_sale, proceeds, dp_treatment, "
     "interaction, decision_log_entry, debt_sale_account, treatment, recovery_case), so each "
     "mirrors an ACE view column that the Workbench must not copy",
     "Open", "Solution architect",
     "Each owning story drops the column and reads the view, or states why the snapshot is kept; a "
     "Tier 3 or Tier 4 judgement is the only ground for keeping one", ""],
    ["RWB-E1-002, RWB-E1-018", "",
     "DEF-06: case_list_row and case_entry_exclusion were UNIQUE (business_date), one row a day in "
     "the whole table, while the case list writes one row per case account and the entry rule one "
     "row per account",
     "Closed 15 Nov 2026. Physical Schema v5 keys are UNIQUE (business_date, case_id, account_no) "
     "and UNIQUE (business_date, account_key); both stories carry the fixed key.",
     "Data architect", "15 Nov 2026"],
    ["RWB-E1-018", "12",
     "the case response and CaseRecordService.findOpenCase publish primaryPersonKey as a plain "
     "String, while section 11 writes DF-CAS-004 recovery_case.primary_person_key and the read path "
     "is v_ace_customer.person_key; the contract does not say the value is the ACE person_key, so a "
     "client can read it as a Workbench id",
     "Open", "Solution architect",
     "State in section 12 that primaryPersonKey carries v_ace_customer.person_key and that no "
     "generated id is published; align the field name in RWB-E1-002, RWB-E2-016 and the API "
     "specification", ""],
    ["RWB-E2-006", "9",
     "step 9 writes the NLEADS reference, result, reason and approval level on the treatment, and "
     "AC2 and AC3 assert the treatment carries them, while DF-TRT-023 to DF-TRT-026 are read from "
     "v_ace_credit_decision under D-RCV-35 and no Workbench table may hold a copy",
     "Open", "Solution architect",
     "Read the result from v_ace_credit_decision and keep only the officer's judgement on the case; "
     "write the reference in the decision log, not on treatment", ""],
    ["RWB-E2-010", "5",
     "dp_treatment is UNIQUE (business_date) in Physical Schema v5, one row a day in the whole "
     "table, while the story writes one row per treatment per business date and asserts 40 rows "
     "for 2026-12-14",
     "Open", "Data architect",
     "Change the key to (treatment_id, business_date) in the RWB-E2-010 migration, as the story "
     "requires", ""],
]
for i, vals in enumerate(new):
    r = last + 1 + i
    for c, v in enumerate(vals, 1):
        cell = ws.cell(r, c, v)
        cell._style = copy.copy(style[c])

ws["A2"] = ("121 contradictions and gaps inside the Epic 1, Epic 2 and technical enabler "
            "stories: 103 open, 16 closed on 15 November 2026 and 2 fixed in October. Rows 121 to "
            "125 carry the ACE read-path defects, including DEF-05 and DEF-06 from the ACE DB "
            "Alignment Change Register.")
ws.auto_filter.ref = "A4:G%d" % (last + len(new))

wb.properties.title = "Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v3"
wb.properties.modified = datetime.datetime(2026, 11, 15, 9, 0, 0)
wb.save(DST)
print("saved", DST, "rows", last + len(new) - 4)


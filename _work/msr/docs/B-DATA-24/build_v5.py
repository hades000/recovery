"""Build Recovery Workbench Data Classification and Personal Data Inventory v5 from the copied v4.

Every v4 cell is kept as it is except the four Handling cells that still describe one
recovery identity and one unnamed PII path. The realignment work is additive: an owner
column from the Ownership Map, a rule column for events and workflow inputs, a rule column
for logs, a new PII controls sheet and the Read me sheet with the header and change-log row.
"""
from copy import copy as _copy

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

V4 = "06 Data/Recovery Workbench Data Classification and Personal Data Inventory v4.xlsx"
V5 = "06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx"
OWN = "22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx"
DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"

TITLE_FONT = Font(bold=True, size=16, color="4E297F")
SUB_FONT = Font(size=10, color="404040")
HDR_FONT = Font(bold=True, size=10, color="4E297F")
HDR_FILL = PatternFill("solid", fgColor="DCD3EB")
BODY_FONT = Font(size=10, color="1F1F1F")
BOLD_FONT = Font(bold=True, size=10, color="1F1F1F")
WRAP = Alignment(wrap_text=True, vertical="top")

# ------------------------------------------------------------------ ownership map
owb = openpyxl.load_workbook(OWN)
service_name, service_schema = {}, {}
for r in owb["Services"].iter_rows(min_row=2, values_only=True):
    if r and r[0]:
        service_name[str(r[0])] = str(r[1])
        service_schema[str(r[0])] = str(r[4])
service_name.setdefault("PLT", "platform library")
service_schema.setdefault("PLT", "platform")
table_owner = {}
for r in owb["Tables"].iter_rows(min_row=2, values_only=True):
    if r and r[0]:
        table_owner[str(r[0])] = (str(r[1]), str(r[2]))
print("ownership map read:", len(service_name), "services,", len(table_owner), "tables")

# ------------------------------------------------------------------ field rules
EVENTS_RULE = {
    "Not personal": "A fact or a code; holds no personal data",
    "Customer data": "A business fact only (a code, an amount or a date), never beside a direct identifier",
    "Indirect identifier": "A reference only (the case id, or the row id of the owning service); the clear key is "
                          "read by REST under the masking policy",
    "Staff identifier": "A user id only; never the person's name",
    "Direct identifier": "Never. Stays in the owning service; a caller reads it by REST, masked by the P4 policy",
    "Sensitive": "Never. Stays in the owning service; masked unless the role handles the deviation",
}
LOG_RULE = {
    "Not personal": "Allowed; holds no personal data",
    "Customer data": "A code or an id only; never the customer value",
    "Indirect identifier": "The id of the read only; never the clear key",
    "Staff identifier": "A user id only; never the person's name",
    "Direct identifier": "Never; the read is audited through the ACE Common PII path",
    "Sensitive": "Never; the read is audited through the ACE Common PII path",
}
# Fields whose content can carry personal data although their category does not say so.
FIELD_OVERRIDE = {
    "DF-OPS-195": ("A reference and a code only, per the event contract; no personal data",
                   "The event id and type only; never the body"),
    "DF-AGT-029": ("Never in an event; a prompt is built from masked fields only",
                   "The prompt version only; never the body"),
    "DF-AGT-049": ("Never in an event; the answer is masked and stays in rwb_agent",
                   "The run id and the guardrail result only; never the answer"),
    "DF-DOC-089": ("Never. OCR text of a customer document (CG-B-DATA-24-4; ASM-B-DATA-24-4)",
                   "Never; the page id only (CG-B-DATA-24-4; ASM-B-DATA-24-4)"),
    "DF-DOC-049": ("Never; a file name can name a customer", "The intake id only"),
    "DF-DOC-052": ("Never; the sender address is masked by role", "The intake id only"),
}
LAKE_EVENTS = "Retired with the data lake (DP-17; ADR-018); nothing is copied and no event carries it"
LAKE_LOG = "Retired with the data lake (DP-17; ADR-018)"
PMR_EVENTS = "Retired as a table (D-RCV-36): a versioned reference row in rwb_case, a code only"
PMR_LOG = "The rule version only"
PMR_STAFF_EVENTS = "Retired as a table (D-RCV-36): a user id only, never the name"
VIEW_OWNER = "P1 rwb-source-data (recovery view)"
RETIRED_ENTITIES = ("lake_copy_watermark", "payment_match_rule")
RETIRED_OWNER = {"lake_copy_watermark": "P1 rwb-source-data (retired table)",
                 "payment_match_rule": "P3 rwb-case (retired table)"}


def owner_cell(entity):
    if entity.startswith("v_ace_"):
        return VIEW_OWNER
    if entity in RETIRED_OWNER:
        return RETIRED_OWNER[entity]
    code, schema = table_owner[entity]
    return f"{code} {service_name[code]} ({schema})"


def rule_for(fid, entity, cat):
    if entity == "lake_copy_watermark":
        return LAKE_EVENTS, LAKE_LOG
    if entity == "payment_match_rule":
        return (PMR_STAFF_EVENTS, PMR_LOG) if fid == "DF-REF-273" else (PMR_EVENTS, PMR_LOG)
    if fid in FIELD_OVERRIDE:
        return FIELD_OVERRIDE[fid]
    return EVENTS_RULE[cat], LOG_RULE[cat]


wb = openpyxl.load_workbook(V5)
fields = wb["Fields"]

# ------------------------------------------------------------------ Fields
assert fields.max_row == 1370 and fields.max_column == 10
hdr, body = fields["A4"], fields["A5"]
FIELD_COLS = [("Owner (D-RCV-60)", 30),
              ("Events and workflow inputs (D-RCV-60)", 60),
              ("Logs (D-RCV-60)", 52)]
for i, (name, width) in enumerate(FIELD_COLS, start=11):
    c = fields.cell(row=4, column=i, value=name)
    c._style = _copy(hdr._style)
    c.alignment = WRAP
    fields.column_dimensions[get_column_letter(i)].width = width

owner_fields, owner_personal, cat_counts, cat_personal = {}, {}, {}, {}
view_fields = view_personal = 0
retired_fields, retired_personal = {}, {}
personal = 0
for r in range(5, 1371):
    fid, entity, field, cat = (fields.cell(row=r, column=c).value for c in (1, 2, 3, 4))
    is_personal = fields.cell(row=r, column=6).value == "Yes"
    own = owner_cell(entity)
    ev, lg = rule_for(fid, entity, cat)
    for i, v in enumerate((own, ev, lg), start=11):
        c = fields.cell(row=r, column=i, value=v)
        c._style = _copy(body._style)
        c.alignment = WRAP
    cat_counts[cat] = cat_counts.get(cat, 0) + 1
    cat_personal[cat] = cat_personal.get(cat, 0) + (1 if is_personal else 0)
    personal += 1 if is_personal else 0
    if entity.startswith("v_ace_"):
        view_fields += 1
        view_personal += 1 if is_personal else 0
    elif entity in RETIRED_ENTITIES:
        retired_fields[entity] = retired_fields.get(entity, 0) + 1
        retired_personal[entity] = retired_personal.get(entity, 0) + (1 if is_personal else 0)
    else:
        code = own.split(" ")[0]
        assert code in service_name, own
        owner_fields[code] = owner_fields.get(code, 0) + 1
        owner_personal[code] = owner_personal.get(code, 0) + (1 if is_personal else 0)
fields.auto_filter.ref = "A4:M1370"
assert sum(owner_fields.values()) + view_fields + sum(retired_fields.values()) == 1366
print("Fields rows", fields.max_row - 4, "owner groups", len(owner_fields), "personal", personal,
      "views", view_fields, "retired", retired_fields)

# ------------------------------------------------------------------ Summary block
ws = wb["Summary"]
assert ws.max_row == 11 and ws.max_column == 3
ws.cell(row=13, column=1, value="Fields by owning service (D-RCV-60)").font = TITLE_FONT
ws.cell(row=14, column=1,
        value="Counted from the Owner column of the Fields tab. Every owner is a row of the Ownership Map v1 sheet "
              "Tables; the 30 recovery.v_ace_* views are P1 under the ACE view contract (CG-B-DATA-24-1; "
              "ASM-B-DATA-24-1) and payment_match_rule is retired (CG-B-DATA-24-2; ASM-B-DATA-24-2).").font = SUB_FONT
for i, h in enumerate(("Owner", "Schema", "Fields", "Personal fields"), start=1):
    c = ws.cell(row=16, column=i, value=h)
    c.font = HDR_FONT
    c.fill = HDR_FILL
    c.alignment = WRAP
ws.column_dimensions["B"].width = 18
ws.column_dimensions["D"].width = 14

row = 17
order = [f"P{i}" for i in range(1, 11)] + [f"S{i}" for i in range(1, 10)] + ["PLT"]
for code in order:
    n = owner_fields.get(code, 0)
    if not n:
        continue
    for i, v in enumerate((f"{code} {service_name[code]}", service_schema[code], n, owner_personal.get(code, 0)),
                          start=1):
        ws.cell(row=row, column=i, value=v).font = BODY_FONT
    row += 1
for i, v in enumerate(("P1 rwb-source-data (views)", "recovery", view_fields, view_personal), start=1):
    ws.cell(row=row, column=i, value=v).font = BODY_FONT
row += 1
for ent in RETIRED_ENTITIES:
    for i, v in enumerate((f"Retired (D-RCV-60): {ent}", "none", retired_fields[ent], retired_personal[ent]),
                          start=1):
        ws.cell(row=row, column=i, value=v).font = BODY_FONT
    row += 1
for i, v in enumerate(("Total", "", 1366, personal), start=1):
    ws.cell(row=row, column=i, value=v).font = BOLD_FONT
summary_rows = row - 16
print("Summary block rows", summary_rows, "last row", row)

# ------------------------------------------------------------------ Identifiers
ws = wb["Identifiers"]
assert ws.max_row == 112 and ws.max_column == 7
hdr, body = ws["A4"], ws["A5"]
for i, (name, width) in enumerate((("Owner (D-RCV-60)", 30),
                                   ("Events, workflow inputs and logs (D-RCV-60)", 62)), start=8):
    c = ws.cell(row=4, column=i, value=name)
    c._style = _copy(hdr._style)
    c.alignment = WRAP
    ws.column_dimensions[get_column_letter(i)].width = width
for r in range(5, 113):
    fid, entity, cat = (ws.cell(row=r, column=c).value for c in (1, 2, 4))
    if entity == "payment_match_rule":
        rule = "Never in an event, a workflow input or a log" if fid == "DF-REF-273" else \
               "Retired as a table (D-RCV-36); a code only"
    elif fid in FIELD_OVERRIDE:
        rule = f"Events and workflow inputs: {FIELD_OVERRIDE[fid][0]}. Logs: {FIELD_OVERRIDE[fid][1]}"
    else:
        rule = f"Events and workflow inputs: {EVENTS_RULE[cat]}. Logs: {LOG_RULE[cat]}"
    for i, v in enumerate((owner_cell(entity), rule), start=8):
        c = ws.cell(row=r, column=i, value=v)
        c._style = _copy(body._style)
        c.alignment = WRAP
ws.auto_filter.ref = "A4:I112"
print("Identifiers rows", ws.max_row - 4)

# ------------------------------------------------------------------ Handling
ws = wb["Handling"]
assert ws.max_row == 22 and ws.max_column == 3
hdr, body = ws["A4"], ws["A5"]
c = ws.cell(row=4, column=4, value="Owner (D-RCV-60)")
c._style = _copy(hdr._style)
c.alignment = WRAP
ws.column_dimensions["D"].width = 34

HANDLING_CHANGED = {
    ("Restricted", "Stored"):
        "ACE source fields stored in ACE only; Workbench Restricted fields encrypted at rest in the owning service's "
        "rwb_* schema. Identification numbers never leave ACE in clear",
    ("Restricted", "In logs"):
        "Never written to application logs. Every read of an ACE personal field is made by rwb-source-data (P1) and "
        "logged through the ACE Common PII logging path to the SOC; the business topics rwb.<service>.events.v1 are "
        "separate and carry no personal data",
    ("Restricted", "Contact values"):
        "phone.phone_number, email.email and address.address are full in v_ace_contact because notices and calls need "
        "them. Display masking is the P4 rwb-access masking policy (E1-037, RWB-P4-E1037) applied by rwb-source-data "
        "at the API, and every read is audited",
    ("Restricted", "Every ACE read"):
        "The rwb_source_data login holds SELECT only on the 30 recovery.v_ace_* views and on nothing else. No other "
        "service login has a grant on a view or on public. A read of a personal field is audited; a direct public "
        "read fails in the catalog",
}
HANDLING_OWNER = {
    ("Restricted", "Stored"): "The owning service (rwb_*)",
    ("Restricted", "On screen"): "P4 rwb-access (policy); the owning service applies it",
    ("Restricted", "In logs"): "P1 rwb-source-data; ACE Common PII logging (INT-34)",
    ("Restricted", "In agent prompts"): "P10 rwb-agent",
    ("Restricted", "In test data"): "PLT masked data set (RWB-PLT-TE004-APP)",
    ("Restricted", "Export"): "The owning service; the export log in P4 rwb-access",
    ("Restricted", "Debt sale tape"): "S6 rwb-debtsale; P2 rwb-integration",
    ("Confidential", "Stored"): "The owning service (rwb_*)",
    ("Confidential", "On screen"): "P4 rwb-access (policy); the owning service applies it",
    ("Confidential", "In agent prompts"): "P10 rwb-agent",
    ("Confidential", "Export"): "The owning service; the export log in P4 rwb-access",
    ("Internal", "Stored"): "The owning service (rwb_*)",
    ("Internal", "On screen"): "The owning service",
    ("All", "Retention"): "P5 rwb-document (retention_rule); Compliance (DL26)",
    ("All", "Data subject request"): "P3 rwb-case (the hold); Compliance (DL26)",
    ("Restricted", "In ACE"): "P1 rwb-source-data (view contract)",
    ("Restricted", "Contact values"): "P1 rwb-source-data; P4 rwb-access (masking policy)",
    ("Restricted", "Every ACE read"): "P1 rwb-source-data (login and grants)",
}
for r in range(5, 23):
    key = (ws.cell(row=r, column=1).value, ws.cell(row=r, column=2).value)
    if key in HANDLING_CHANGED:
        ws.cell(row=r, column=3, value=HANDLING_CHANGED[key])
    c = ws.cell(row=r, column=4, value=HANDLING_OWNER[key])
    c._style = _copy(body._style)
    c.alignment = WRAP

HANDLING_NEW = [
    ["Restricted", "In events and workflow inputs",
     "Never. Events and workflow inputs carry case_id and business facts only; a direct identifier is read back by "
     "REST under the masking policy",
     "Each producing service; the platform workflow kit"],
    ["Confidential", "In events and workflow inputs",
     "Business facts and codes only, never beside a direct identifier; an indirect identifier travels as a reference",
     "Each producing service"],
    ["Internal", "In logs", "User ids and codes only; a staff name is never written", "The owning service"],
    ["All", "In events",
     "The CloudEvents envelope and the payload hold no personal data; the Kafka key is caseId; the JSON Schema "
     "registry rejects a personal field", "Each producing service (DP-09)"],
    ["All", "In workflow history",
     "Search attributes are CaseId, Stage, ProductGroup and QueueCode only; payloads are encrypted by the payload "
     "codec (AES-GCM, Key Vault keys); the history never holds clear personal data",
     "The owning service; PLT workflow kit (RWB-PLT-E1071-CON)"],
    ["All", "PII logging",
     "Audit and personal-data access logs go through the ACE Common PII logging path (INT-34) to the SOC; the "
     "Recovery business topics are separate and carry no personal data",
     "ACE Common (INT-34); each service sends"],
]
for i, row_vals in enumerate(HANDLING_NEW, start=23):
    for j, v in enumerate(row_vals, start=1):
        c = ws.cell(row=i, column=j, value=v)
        c.font = BODY_FONT
        c.alignment = WRAP
ws.auto_filter.ref = "A4:D28"
print("Handling rows", ws.max_row - 4, "changed cells", len(HANDLING_CHANGED), "new rows", len(HANDLING_NEW))

# ------------------------------------------------------------------ Who sees what
ws = wb["Who sees what"]
assert ws.max_row == 18 and ws.max_column == 4
hdr, body = ws["A4"], ws["A5"]
c = ws.cell(row=4, column=5, value="Enforced by (D-RCV-60)")
c._style = _copy(hdr._style)
c.alignment = WRAP
ws.column_dimensions["E"].width = 46
WSW = {
    5: "P4 masking policy; the owning service applies it on every read",
    6: "P4 masking policy; the owning service applies it on every read",
    7: "P4 masking policy; the owning service applies it on every read",
    8: "P4 masking policy; the deviation service and the owning service apply it",
    9: "P4 masking policy; the owning service applies it on every read",
    10: "P4 masking policy; the contact point is masked by rwb-source-data",
    11: "P4 masking policy; the owning service applies it on every read",
    12: "P4 masking policy; the access log in rwb_access records every unmasked read",
    13: "P4 masking policy and the access log; read only and logged",
    14: "P4 masking policy; rwb-reporting reads events and the P1 contract only",
    15: "P4 masking policy; RW-SECADM decode is break-glass and logged",
    16: "P4 masking policy; the S9 rwb-partner contract through the partner gateway",
    17: "P10 rwb-agent masks before the prompt is built",
    18: "Not used under D-RCV-60: only the P1 rwb-source-data login reads the views",
}
for r, v in WSW.items():
    c = ws.cell(row=r, column=5, value=v)
    c._style = _copy(body._style)
    c.alignment = WRAP
ws.auto_filter.ref = "A4:E18"
print("Who sees what rows", ws.max_row - 4)

# ------------------------------------------------------------------ Key
ws = wb["Key"]
assert ws.max_row == 16
KEY_NEW = [
    ["Rule", "Event payload",
     "IDs and business facts only; no personal data. The JSON Schema registry rejects a personal field and the "
     "Kafka key is caseId"],
    ["Rule", "Workflow input and history",
     "IDs and business facts only; the payload codec encrypts (AES-GCM, Key Vault keys); search attributes are "
     "CaseId, Stage, ProductGroup and QueueCode only"],
    ["Rule", "Logs",
     "IDs and codes only. A personal-data access log goes through the ACE Common PII path to the SOC, never a "
     "Recovery business topic"],
    ["Class", "PII logging",
     "The ACE Common audit and personal-data access log path (INT-34) to the SOC, separate from the "
     "rwb.<service>.events.v1 topics"],
    ["Category", "Masking policy",
     "The P4 rwb-access masking_rule rows, enforced in each service and applied by rwb-source-data on every ACE "
     "field it serves"],
]
for i, row_vals in enumerate(KEY_NEW, start=17):
    for j, v in enumerate(row_vals, start=1):
        c = ws.cell(row=i, column=j, value=v)
        c.font = BODY_FONT
        c.alignment = WRAP
ws.auto_filter.ref = "A4:C21"
print("Key rows", ws.max_row - 4, "new", len(KEY_NEW))

# ------------------------------------------------------------------ PII controls
CHANNEL_HEAD = ["Channel", "Carries", "Never", "Owner", "Control"]
CHANNEL_ROWS = [
    ["REST through gateway-bff",
     "The field values the caller's role and scope may see, masked where the policy says so",
     "A clear value the role may not see",
     "P4 rwb-access (masking policy); the owning service applies it",
     "Masking policy as data in rwb_access; the service applies it on every read; one hop, 2 s"],
    ["Kafka rwb.<service>.events.v1",
     "case_id, business facts, codes and amounts",
     "Any personal data; any direct identifier",
     "The producing service",
     "DP-09 outbox and inbox, CloudEvents, JSON Schema registry; key caseId; a personal field is rejected"],
    ["Kafka rwb.decision-record.v1",
     "chain_seq, inputsRef, ruleId, ruleVersion, recommendation, approverUserId, approvalLevel, finalCall, "
     "actions, outcome, decidedAt and the hashes",
     "Personal data; the inputs themselves (inputsRef is a reference)",
     "P7 rwb-decision (central ledger); the owning service (local record)",
     "DP-03; every service keeps its local record and rwb-decision collects it"],
    ["Temporal workflow input, history and activity payload",
     "case_id and business facts; the workflow id is the business key",
     "Personal data; I/O or PII in workflow code",
     "The owning service on queue rwb-<short>",
     "PLT workflow kit (RWB-PLT-E1071-CON); PdpaPayloadCodec AES-GCM with Key Vault keys; search attributes "
     "CaseId, Stage, ProductGroup and QueueCode only"],
    ["Application logs, traces and metrics",
     "Ids, codes, outcome, latency and the trace context",
     "Personal data; any clear value",
     "The owning service",
     "ACE Common PII logging (INT-34) to the SOC; the Recovery business topics are separate from the PII path"],
    ["Agent prompt and answer",
     "The masked fields the step needs, and the answer masked",
     "A clear personal value",
     "P10 rwb-agent",
     "Masked before the prompt is built and before the answer is stored; 60 s then the rules decide"],
    ["Document storage (Blob, WORM)",
     "The document as received, and its OCR text",
     "Document content in an event, a workflow input or a log",
     "P5 rwb-document",
     "WORM; OCR text masked on read; no document content outside rwb_document"],
    ["File to a partner (WIN, debt buyer)",
     "Only the fields the sale or instruction terms allow, as a masked tape",
     "Personal data beyond the terms",
     "P2 rwb-integration and S6 rwb-debtsale",
     "Approved extract, logged with the requester; FAPI 2.0 partner gateway in the DMZ"],
    ["Database (ACE PostgreSQL)",
     "The record in the owning service's own rwb_* schema",
     "A read of another service's schema or of public",
     "The owning service; P1 for the 30 views",
     "One login and one schema per service (ADR-014); encryption at rest; no cross-schema join (DP-01)"],
]
CAT_HEAD = ["Category", "Classification", "Fields", "Events and workflow inputs", "Logs"]
CAT_ROWS = [[c, cl, n, EVENTS_RULE[c], LOG_RULE[c]] for c, cl, n in
            (("Direct identifier", "Restricted", 12), ("Sensitive", "Restricted", 5),
             ("Indirect identifier", "Confidential", 91), ("Customer data", "Confidential", 364),
             ("Staff identifier", "Internal", 51), ("Not personal", "Internal", 843))]
RET_HEAD = ["Item", "v4", "v5", "Basis"]
RET_ROWS = [
    ["Read path to ACE data", "Every service reads recovery.v_ace_*",
     "Only P1 rwb-source-data reads the 30 views; every other service calls its REST contract or an activity",
     "Architecture v5 lines 707, 909, 3016 and 3038; ADR-010; DP-05; CG-B-DATA-24-1"],
    ["Database identity", "recovery_svc, one login and one schema",
     "One login and one rwb_* schema per service; no other login has a grant on a view or on public",
     "Architecture v5 lines 2051, 2126, 2143 and 2147; ADR-014; DP-01, DP-02; CG-B-DATA-24-5"],
    ["PII log path", "\"PII Kafka\", no owner and no separation from the business topics",
     "The ACE Common PII logging path to the SOC (INT-34), separate from rwb.<service>.events.v1",
     "Architecture v5 lines 501, 511, 1503 and 2537; CG-B-DATA-24-6"],
    ["Masking policy", "E1-037 at the API, owner not named",
     "P4 rwb-access masking policy as data, enforced in each service and applied by P1 on ACE fields",
     "Architecture v5 lines 1020, 2562 and 2882; RWB-P4-E1037-CON; CG-B-DATA-24-7"],
    ["Data lake copies", "lake_copy_watermark and the DECISION_LOG copy",
     "Retired; there is no lake to copy to",
     "Architecture v5 line 2988 (JOB-13); ADR-018; DP-17; CG-B-DATA-24-3"],
    ["Payment match rules", "payment_match_rule as a table",
     "Versioned parameter and reference rows in P3 rwb-case, and the PAYMENT_MATCH rule package in P7 rwb-decision",
     "PRD P8 v1 sections 2.3 and 5.1; D-RCV-36; CG-B-DATA-24-2"],
    ["Channel rule in the inventory", "None: the inventory classifies storage, screens, prompts, test data and export",
     "Per-field rules for events, workflow inputs and logs, and this sheet",
     "This version; CG-B-DATA-24-8"],
    ["Interaction ledger owner", "interaction defined by the case module",
     "P1 rwb-source-data owns the ledger; P3 rwb-case owns the timeline API and reads the ledger through P1",
     "Ownership Map sheet Rulings (ASM-A6-tables-1); DP-18; CG-B-DATA-24-9"],
]


def put(ws, r, c, value, font=BODY_FONT, fill=None):
    cell = ws.cell(row=r, column=c, value=value)
    cell.font = font
    if fill is not None:
        cell.fill = fill
    cell.alignment = WRAP
    return cell


def section(ws, r, title, note, head, rows):
    ws.cell(row=r, column=1, value=title).font = TITLE_FONT
    ws.cell(row=r + 1, column=1, value=note).font = SUB_FONT
    hr = r + 3
    for i, h in enumerate(head, start=1):
        put(ws, hr, i, h, font=HDR_FONT, fill=HDR_FILL)
    for j, row_vals in enumerate(rows, start=hr + 1):
        for i, v in enumerate(row_vals, start=1):
            put(ws, j, i, v)
    return hr + len(rows)


ws = wb.create_sheet("PII controls")
ws.sheet_view.showGridLines = False
for i, w in enumerate((34, 46, 34, 38, 58), start=1):
    ws.column_dimensions[get_column_letter(i)].width = w
end = section(ws, 1, "Where personal data may travel (D-RCV-60)",
              "One row per channel of the target architecture. Events and workflow inputs carry case_id and business "
              "facts only; personal data stays in the owning service (Architecture v5 lines 833, 1618, 2533, 2562 "
              "and 3064).",
              CHANNEL_HEAD, CHANNEL_ROWS)
end = section(ws, end + 2, "Field count by category and channel rule (D-RCV-60)",
              "The 1,366 fields of the Fields tab by category, with the rule carried in the two appended columns.",
              CAT_HEAD, CAT_ROWS + [["Total", "", 1366, "", ""]])
section(ws, end + 2, "Changed or retired in v5 (D-RCV-60)",
        "What the realignment changed in this inventory and the source that decides each row.",
        RET_HEAD, RET_ROWS)
print("PII controls rows", len(CHANNEL_ROWS) + len(CAT_ROWS) + 1 + len(RET_ROWS))

# ------------------------------------------------------------------ Read me
README = [
    ("SCB Collections and Recovery. Henka Group, 22 November 2026.", TITLE_FONT),
    ("(C) Siam Commercial Bank and Henka Pte Ltd", BODY_FONT),
    ("", None),
    ("Recovery Workbench Data Classification and Personal Data Inventory v5", TITLE_FONT),
    ("Next version of Recovery Workbench Data Classification and Personal Data Inventory v4.xlsx. "
     f"Decision {DEC} microservice realignment.", SUB_FONT),
    (f"Tool: {TOOL}.", SUB_FONT),
    ("", None),
    ("Change log", HDR_FONT),
    ("v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash", BODY_FONT),
    ("", None),
    ("What changed in v5", HDR_FONT),
    ("1. Fields: three columns are appended at the end. Owner gives the owning service and schema of the entity, "
     "taken row by row from the Ownership Map v1 sheet Tables. Events and workflow inputs gives the rule for a "
     "payload of a Kafka event or a Temporal workflow. Logs gives the rule for an application log, trace or metric. "
     "Columns A to J keep their letters, positions and values; all 1,366 field rows are unchanged.", BODY_FONT),
    ("2. Fields: the rule follows the category of the field. Not personal travels as a fact or a code. Customer data "
     "travels as a business fact only, never beside a direct identifier. An indirect identifier travels as a "
     "reference only and is resolved by REST under the P4 masking policy. A staff identifier travels as a user id "
     "only. A direct identifier and a sensitive field never travel, and their read is audited through the ACE "
     "Common PII path.", BODY_FONT),
    ("3. Fields: six fields carry a rule of their own because their content can hold personal data although their "
     "category does not say so: outbox_event.payload, agent_prompt.body_text, agent_run.output, "
     "document_text.text_content, document_intake.file_name and document_intake.sender_address "
     "(CG-B-DATA-24-4; ASM-B-DATA-24-4).", BODY_FONT),
    ("4. Fields: the 30 recovery.v_ace_* views are P1 rwb-source-data under the ACE view contract, because the "
     "Ownership Map lists tables and not views (CG-B-DATA-24-1; ASM-B-DATA-24-1). lake_copy_watermark is retired "
     "with the data lake (CG-B-DATA-24-3; ASM-B-DATA-24-3) and payment_match_rule is retired as a table "
     "(CG-B-DATA-24-2; ASM-B-DATA-24-2); both keep their rows and their field IDs.", BODY_FONT),
    ("5. Identifiers: two columns are appended, Owner and Events, workflow inputs and logs. The 108 rows keep their "
     "IDs, categories, classes, on-screen rules and meanings.", BODY_FONT),
    ("6. Summary: a block is added below the category counts. It counts the 1,366 fields and the personal fields by "
     "owning service, with the 30 views and the two retired entities on their own rows.", BODY_FONT),
    ("7. Handling: four cells change. Restricted and Stored names the owning service's rwb_* schema. Restricted and "
     "In logs names the ACE Common PII logging path and says the business topics are separate. Restricted and "
     "Contact values names the P4 masking policy. Restricted and Every ACE read gives SELECT on the 30 views to the "
     "rwb-source-data login alone (CG-B-DATA-24-5; ASM-B-DATA-24-5; CG-B-DATA-24-6; ASM-B-DATA-24-6). An Owner "
     "column is appended and six rows are added for events, workflow inputs and logs "
     "(CG-B-DATA-24-8; ASM-B-DATA-24-8).", BODY_FONT),
    ("8. Who sees what: one column is appended, Enforced by, naming the P4 masking policy, the owning service or the "
     "agent runtime (CG-B-DATA-24-7; ASM-B-DATA-24-7). The 14 role rows are unchanged.", BODY_FONT),
    ("9. Key: five rows are appended for the event payload, the workflow input and history, logs, PII logging and the "
     "masking policy. The 11 existing rows are unchanged.", BODY_FONT),
    ("10. PII controls: a new last sheet. It states, one row per channel, what may travel and what never may, with "
     "the owner of each control; the field count by category; and the eight items this version changed or retired.",
     BODY_FONT),
    ("11. Read me: this sheet is new and carries the header of Template and Rules section R8.1 and the change-log "
     "row.", BODY_FONT),
    ("", None),
    ("What did not change", HDR_FONT),
    ("The 122 entities keep their names and their field counts: 88 Workbench tables, 4 extension tables and 30 ACE "
     "source views, 1,366 fields. Every field ID, entity name, field name, personal data category, classification, "
     "personal flag, on-screen rule, lawful basis, retention rule and meaning is copied character for character. The "
     "108 identifier rows, the 22 handling rules, the 14 role rows and the 11 key rows keep their content except the "
     "four handling cells named above.", BODY_FONT),
    ("The source carries no version number in its cells, no release date and no date cell at all, so no release date "
     "is marked (tentative) and no date is changed. No date is raised as a gap.", BODY_FONT),
    ("", None),
    ("Counts", HDR_FONT),
    (f"Fields: 1,366 rows over 122 entities; {personal} personal fields and {cat_counts['Not personal']} not "
     f"personal. Category and class: 12 Direct identifier and 5 Sensitive at Restricted; 91 Indirect identifier and "
     f"364 Customer data at Confidential; 51 Staff identifier and 843 Not personal at Internal. Appended cells: 3 "
     f"headers and 4,098 values.", BODY_FONT),
    (f"Identifiers: 108 rows, 2 headers and 216 values. Summary: 1 block of {summary_rows} rows. Handling: 1 header "
     f"and 24 values, 4 changed cells and 6 new rows. Who sees what: 1 header and 14 values. Key: 5 new rows. PII "
     f"controls: 9 channel rows, 6 category rows and a total, and 8 changed or retired rows.", BODY_FONT),
    ("", None),
    ("Open points", HDR_FONT),
    ("CG-B-DATA-24-1 to CG-B-DATA-24-9 and ASM-B-DATA-24-1 to ASM-B-DATA-24-9 in the Gap and Assumption registers "
     "hold the questions this version leaves open. The build note under _work/msr/docs/B-DATA-24/ cites each one "
     "where it applies.", BODY_FONT),
]
ws = wb.create_sheet("Read me", 0)
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 130
for i, (text, font) in enumerate(README, start=1):
    if text == "":
        continue
    c = ws.cell(row=i, column=1, value=text)
    if font is not None:
        c.font = font
    c.alignment = Alignment(wrap_text=True, vertical="top")
    if font is TITLE_FONT or font is HDR_FONT:
        ws.row_dimensions[i].height = 18

# ------------------------------------------------------------------ properties
p = wb.properties
p.title = "Recovery Workbench Data Classification and Personal Data Inventory v5"
p.creator = "Recovery Workbench programme"
p.lastModifiedBy = TOOL

wb.save(V5)
print("WROTE", V5)
print("sheets", wb.sheetnames)

"""WP C-DEF builder: map every defect of the v4 sheet to the D-RCV-60 story IDs.

Reads the source workbook (read only), the catalog cross reference and the plan.
Writes only scratch files, the rows JSON for office_write.py, defects.jsonl,
gaps/C-DEF.jsonl and assumptions/C-DEF.jsonl.
"""
import json
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[4]
WORK = ROOT / "_work" / "msr"
OUT = Path(__file__).resolve().parent
SRC = ROOT / "04 User stories" / "Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v4.xlsx"
CAT = ROOT / "04 User stories" / "Recovery Workbench Service Story Catalog v1.xlsx"

DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
NONE_CANCELLED = "No new story (legacy key cancelled under D-RCV-35 U1; R6 keeps it cancelled)"
NONE_RETIRED = "No new story (legacy key retired under R6 / D-RCV-60)"
NONE_FIXED = "No new story (fixed in the set; carried by every story file of the set)"

# row in the v4 Defects sheet -> (new story IDs, note)
MAP = {
    5: (["RWB-P3-E1042-CON", "RWB-P3-E1042-APP"],
        "Authority (s10) and the rollback operation (s12) are the rwb-case parameters and reference-data contract (R3 default ruling, DP-06/DP-07); the Reference data right is C at the contract and U only on the rollback route."),
    6: (["RWB-P1-E1066-CON", "RWB-P1-E1066-APP"],
        "InteractionRequest is the rwb-source-data ledger contract (DP-18); promise amount and promise date are added to that schema and to the intake step."),
    7: (["RWB-P10-E2031-CON", "RWB-P10-E2031-APP", "RWB-P4-E2031-APP", "RWB-P10-E2031-OPS", "RWB-ITG-E2031-ITG"],
        "Header defect: the [E3d] tag and the release are metadata of every story of the key; v5 keeps the date unchanged and tentative and carries the business-epic tag EP03."),
    8: (["RWB-P5-E2017-CON", "RWB-P5-E2017-APP"],
        "The send is the rwb-document signature-request contract (Ownership Map, signature_request to P5); only the P5 path is contracted, so the generated-documents path leaves sections 13 and 16."),
    9: ([NONE_CANCELLED],
        "RWB-E1-012 is cancelled under D-RCV-35 U1; no new story, the defect closes with the key and the retirement procedure sits in the Cutover and Go Live Plan."),
    10: (["RWB-P1-E1001-APP", "RWB-PLT-NF06-DB"],
         "The foreign-key count belongs to the schema split (DL47): RWB-P1-E1001-APP carries the P1 tables and RWB-PLT-NF06-DB creates the 19 rwb_* schemas and logins."),
    11: (["RWB-P1-E1001-APP", "RWB-PLT-NF06-DB"],
         "The row counts of sys_objects and sys_fields are read from the physical schema, not restated per story; RWB-PLT-NF06-DB holds the per-schema count check."),
    12: (["RWB-P1-E1002-CON", "RWB-P1-E1002-APP"],
         "The REFUSED load_run row is both the load contract (s12) and the flow (s3), so it changes in the CON and APP stories of RWB-E1-002."),
    13: ([NONE_CANCELLED], "RWB-E1-003 is cancelled under R6; the ALS load is ACE ingestion and no new story carries it."),
    14: ([NONE_CANCELLED], "RWB-E1-005 is cancelled under R6; the tracker inventory sits in the Cutover and Go Live Plan."),
    15: (["RWB-P2-E1007-CON", "RWB-P2-E1007-APP"],
         "Closed row: the inbound half is removed, the outbound half of RWB-E1-007 is the rwb-integration contract (DP-16) and the interface_config rows."),
    16: (["RWB-P2-E1007-CON", "RWB-P2-E1007-APP"],
         "Closed row: the CCMS stale rule leaves with the load; the surviving story reads dataAsOf from the ACE views (DP-05) and states that in the contract."),
    17: (["RWB-P2-E1007-CON", "RWB-P2-E1007-APP"],
         "Closed row: the retry intervals come from the outbound_item row (Ownership Map, outbound_item to P2), so the fixed 5/15/45 minute triple is dropped."),
    18: ([NONE_CANCELLED], "RWB-E1-010 is cancelled under R6; the tracker load and the container name sit in the Cutover and Go Live Plan."),
    19: (["RWB-P1-E1011-APP"],
         "dq_exception check codes REC-01 and REC-02 are written and read by one story, so the flow and the exceptions endpoint agree in RWB-P1-E1011-APP."),
    20: (["RWB-P1-E1013-APP"],
         "The corrected fixture (run 2026-12-01 for business date 2026-11-30) is carried unchanged into RWB-P1-E1013-APP; the date itself is not raised as a gap."),
    21: ([NONE_RETIRED],
         "RWB-E1-014 is retired (the data lake is removed, DP-17 and ADR-018), so the 120 versus 24 month LAKE_COPY rule has no target story."),
    22: ([NONE_RETIRED],
         "RWB-E1-014 is retired (DP-17, ADR-018); the partition fixture has no target story and the row stays as written."),
    23: (["RWB-P1-E1015-CON", "RWB-P1-E1015-APP"],
         "Closed row: the rewritten header lists RWB-E1-001, RWB-E1-069 and RWB-E1-027; the new story keeps those H and C dependencies (DP-05)."),
    24: (["RWB-P1-E1015-APP", "RWB-P1-E1015-OPS"],
         "JOB-01 and JOB-09 are retired (Ownership Map, ACE ingestion read through the rwb-source-data views); the freshness step becomes one event-started workflow, so the APP and OPS stories name one place."),
    25: (["RWB-P1-E1016-APP"],
         "role, permission and masking move to rwb-access (Ownership Map, role and permission to P4); the P1 story reads role codes from the session only, which is the section 13 position."),
    26: (["RWB-P1-E1017-APP"],
         "The test-case list and the traceability list are generated from section 16 in v5 story files, so the counts agree by construction."),
    27: (["RWB-P3-E1018-APP"],
         "The decision-record write is one local library call before commit (DP-03); the order is stated once, in the section 13 component list."),
    28: (["RWB-P3-E1019-CON", "RWB-P3-E1019-APP"],
         "Reference data rights are held by rwb-case (R3 default ruling, DP-07); the contract grants C to the loader and U to the rollback route only."),
    29: ([NONE_RETIRED],
         "Closed by D-RCV-36: the story is retired and the work moved to RWB-E1-073; R6 keeps no new story for RWB-E1-029."),
    30: (["RWB-P3-E1030-APP"],
         "The decision-record write is one call (DP-03) and its position is stated once; the flow and the section 13 build steps agree in RWB-P3-E1030-APP."),
    31: (["RWB-P5-E1032-CON", "RWB-P5-E1032-APP"],
         "The intake operations are the rwb-document contract (document_intake to P5); one naming set is used in the contract and the components."),
    32: (["RWB-P5-E1033-APP"],
         "document and document_text are P5 tables (Ownership Map), so the search route and the feature flag name are fixed in RWB-P5-E1033-APP."),
    33: (["RWB-P6-E1034-APP"],
         "The template version is the row in force on the business date; the set-current action is dropped and the derivation is stated in section 13."),
    34: (["RWB-P3-E1035-CON", "RWB-P3-E1035-APP"],
         "Event order and page order are fixed by the paging contract and the topic order (DP-09); the tie-break is stated in section 12 and reflected in the criteria."),
    35: (["RWB-P3-E1035-CON", "RWB-P3-E1035-APP"],
         "Queue fields are recorded with the allocation slice (queue and queue_member to P3), so one story owns the from and to queue fields."),
    36: (["RWB-P4-E1039-APP"],
         "Access event codes are held by rwb-access (access_log is P4's); the six codes including AC-VERS are one list in section 3 and in the publisher comment."),
    37: (["RWB-P4-E1039-CON", "RWB-P4-E1039-APP"],
         "One break-glass path in the rwb-access contract: POST /api/recovery/access/v1/admin/break-glass-grants, used by the flow and the criteria."),
    38: (["RWB-P5-E1041-APP"],
         "Retention is rwb-document's (retention_rule and retention_action to P5, ASM-A6-tables-10), so one entity name is used in sections 11 and 13."),
    39: (["RWB-P3-E1042-APP"],
         "Exception order X9 and X10 is restored and the twelfth test case is named in section 18; both are mechanical fixes in the APP story."),
    40: (["RWB-PLT-E1044-APP-2"],
         "The schema is rwb_case (DP-01, DP-02, ADR-014); the delta story sets RWB_SCHEMA per service and the preserved as-built section keeps the monolith value."),
    41: (["RWB-PLT-E1047-CON", "RWB-PLT-E1047-APP"],
         "The duplicate-key message is the feature-flag defect message, not MSG-GEN-004; the message map in section 12 and the text in section 14 are aligned."),
    42: (["RWB-P3-E2041-APP"],
         "RWB-E1-048 is cancelled under R6 and has no plan row; the work it names sits in RWB-E2-041, whose APP story is RWB-P3-E2041-APP."),
    43: (["RWB-P5-E1054-CON", "RWB-P5-E1054-APP"],
         "The review and intake operations are the rwb-document contract (document_intake to P5); one operation set is named in sections 12, 13 and 16."),
    44: (["RWB-P5-E1054-APP"],
         "The dependency on RWB-E1-024 is an H dependency on the same service's document store story (RWB-P5-E1024-APP), so it appears in the header."),
    45: (["RWB-PLT-E1056-OPS"],
         "JOB-12 is an event-started DocumentIntakeWorkflow in rwb-document (Ownership Map, Jobs), not a new Quartz job; TE-007 is retired and the OPS story records the Schedule and its run book."),
    46: (["RWB-PLT-E1056-OPS"],
         "MSG-P2-004 text is corrected to the threshold case in the OPS run book; no business value is invented, the message stays as the source writes it."),
    47: (["RWB-PLT-E1056-OPS"],
         "JOB-07 and JOB-08 are event-started workflows in rwb-payment (Ownership Map, Jobs), so the restart order names those workflows and the OPS story owns the run book."),
    48: (["RWB-P5-E1057-APP", "RWB-P5-E1057-OPS"],
         "The window is 08:00 to 18:00 inclusive, so the last run is 18:00; the cron is corrected in the APP story and the run book."),
    49: (["RWB-P10-E1058-CON", "RWB-P10-E1058-APP"],
         "The endpoint count in section 6 and the contract list in section 12 are read from one table in the rwb-agent contract."),
    50: (["RWB-P10-E1060-APP"],
         "The precondition and the criterion use the same sample size; the fixture is corrected in the APP story without changing the business value."),
    51: (["RWB-P10-E1061-CON", "RWB-P10-E1061-APP"],
         "The path parameter and the request line are aligned in the rwb-agent contract (evaluationId in the path, runId in the body)."),
    52: (["RWB-P10-E1061-APP"],
         "The proposal and the evaluation run are consistent: the gap type NO_CONTACT_POINT is a separate evaluation line, not a contradiction of the threshold."),
    53: (["RWB-P1-E1064-APP"],
         "Six load attributes are named once in section 3, BR1, AC1 and section 13; the build step is corrected in the APP story."),
    54: (["RWB-P1-E1065-APP", "RWB-P1-E1065-DB"],
         "The sandbox build fills rwb_sandbox and never renames the live schema (DP-15, ADR-021); the APP and DB stories state one procedure."),
    55: (["RWB-P1-E1065-APP", "RWB-P1-E1065-DB"],
         "decision_log_entry is P7's table (Ownership Map) and is not generated by the sandbox build, so the entity count and the verifier exclude it."),
    56: (["RWB-P1-E1068-APP"],
         "The P3 case scope and RWB-E1-037 join the header as C dependencies (RWB-PLT-E1037-CON and RWB-PLT-E1027-CON), so the story can build without them."),
    57: (["RWB-P2-E2001-CON", "RWB-P2-E2001-APP"],
         "X2 is the late load and X3 the missing party; one exception numbering is used in sections 3 and 5."),
    58: (["RWB-P2-E2003-APP"],
         "party_product is loaded by the P1 data-product job and read through the P1 contract (DP-05), so the story no longer creates it in a P1 migration."),
    59: (["RWB-P3-E2004-CON", "RWB-P3-E2004-APP"],
         "TimerDue carries the timer ID only (DP-10, DP-12); the treatment ID is read from the case, so the payload and the criteria agree."),
    60: (["RWB-P7-E2005-APP"],
         "The dependency on RWB-E1-048 moves to RWB-P3-E2041-APP (the story that carries the work); no H dependency crosses a service, so it is a C dependency on the rwb-decision side."),
    61: (["RWB-P2-E2007-APP", "RWB-P7-E2007-APP"],
         "BOOKING_CONFIRMED to NLEADS APPROVED is a decision result (rwb-decision) that the integration story consumes; the state is named in both stories."),
    62: (["RWB-P8-E2008-CON", "RWB-P8-E2008-APP"],
         "The missed-event rule is stated once: due date plus grace days strictly before the business date; the criterion uses a later due date."),
    63: (["RWB-P1-E2010-APP"],
         "The DP04 row and the sys_fields entries are P1's (Ownership Map, dp_treatment to P1), so RWB-P1-E2010-APP depends on RWB-P1-E1064-APP."),
    64: (["RWB-P3-E2011-APP"],
         "The 40 cases of U-CO-01 are split once, without adding the paused cases to the same 40; AC9 is corrected."),
    65: (["RWB-P3-E2012-APP"],
         "RWB-E1-020 and RWB-E1-027 join the header as C and H dependencies; the deviation story builds against the published contracts."),
    66: (["RWB-P3-E2015-APP"],
         "NFR-009 and NFR-008 are read together; the 2 second target and the 2 second timeout are stated as one budget in section 13."),
    67: (["RWB-P3-E2015-CON", "RWB-P3-E2015-APP"],
         "Three consumed interfaces are contracted (DeviationQuery, DecisionLogQuery, ProductParameterService); section 6 is corrected to three."),
    68: (["RWB-P3-E2016-APP"],
         "The move list is newest first and the oldest move is named last; the criterion is corrected in one direction."),
    69: (["RWB-P5-E2017-CON", "RWB-P5-E2017-APP"],
         "MSG-P5-009 is added to the section 14 message list, since section 12 already returns it after an override."),
    70: (["RWB-P5-E2018-APP"],
         "signature_request.signed_at is written once, through the P5 contract (signature_request to P5); the direct write is dropped."),
    71: (["RWB-P5-E2018-APP", "RWB-P6-E2018-APP"],
         "One event name is used: CUSTOMER_ACCEPTED, published by rwb-document and consumed by rwb-comms (DP-09); the local event name is dropped."),
    72: (["RWB-P6-E2021-APP"],
         "The conduct check and the proof window sit in one sequence; JOB-10 is a Temporal Schedule in rwb-comms (Ownership Map, Jobs) and is named once in section 12."),
    73: (["RWB-P5-E2024-APP"],
         "The dependency on RWB-E1-049 is an H dependency on the same service's document intake story (RWB-P5-E1049-APP)."),
    74: (["RWB-P5-E2025-APP"],
         "The pass mark is applied per field, so the criterion tests each field on its own against 0.90."),
    75: (["RWB-P5-E2026-APP"],
         "The unique key on template_code becomes (template_code, template_version) in the P6 template story; the note in section 13 is corrected."),
    76: (["RWB-P5-E2026-CON", "RWB-P5-E2026-APP"],
         "D6.4 and D6.5 are both named in the header, the flow step and the contract."),
    77: (["RWB-P5-E2026-APP"],
         "document carries template_code and template_version (DF-DOC-032 is replaced), so sections 11 and 13 agree."),
    78: (["RWB-P10-E2029-CON", "RWB-P10-E2029-APP", "RWB-S8-E2029-APP", "RWB-P7-E2029-APP", "RWB-ITG-E2029-ITG"],
         "Header defect: the key stays RWB-E2-029 and the business epic is EP03 with the release unchanged and tentative; the tag [E3d] is the only E3 marker."),
    79: (["RWB-P10-E2030-CON", "RWB-P10-E2030-APP", "RWB-P5-E2030-APP", "RWB-ITG-E2030-ITG"],
         "Header defect: the key stays RWB-E2-030 and the business epic is EP03 with the release unchanged and tentative."),
    80: (["RWB-P2-E2034-CON", "RWB-S9-E2034-APP"],
         "The ordered read is the ledger entry sequence; the occurred-time order is the page order on the S9 fact view and the P2 contract, stated once."),
    81: (["RWB-P3-E2035-APP"],
         "One service-level seed per route-set state in force; AC6 uses the DEV_WITH_OWNER state without a row because the state is seeded elsewhere."),
    82: (["RWB-P1-E1001-APP", "RWB-PLT-NF06-DB"],
         "Closed row: the migration name follows the per-service Flyway sequence (DP-15, ADR-021); the baseline is created by RWB-PLT-NF06-DB."),
    83: (["RWB-PLT-E1044-CON", "RWB-PLT-E1044-APP"],
         "Closed row: the 68 migration names follow the per-service Flyway sequence in the platform library story (DL47, ADR-021)."),
    84: ([NONE_FIXED],
         "Fixed row: every story of the set names Recovery Workbench Physical Schema and the file in the hub; the new story files carry the same name."),
    85: (["RWB-PLT-TE001-APP-2"],
         "The boundary rule codes are BND-1 to BND-5; the delta story states the codes once in section 8."),
    86: (["RWB-PLT-TE002-APP"],
         "The code owners file has one approving team (ACE) and one owner of record; the OPS story is not an approver."),
    87: (["RWB-PLT-TE003-APP-2"],
         "The lint set includes x-module and x-first-release (ADR-020); BR2 and the step name the same checks."),
    88: (["RWB-PLT-TE003-APP-2"],
         "The build fails an operation of the current release with no implementation and allows a named later-release story, so the Done rule and AC5 agree."),
    89: (["RWB-PLT-TE004-APP"],
         "The CTL-02 checks run during the load into the service schema (DP-15); the flow is corrected to the build step."),
    90: (["RWB-PLT-TE004-APP"],
         "MaskingVerifier runs after the load (P4 masking_rule, DP-08); the flow is corrected to the build step."),
    91: ([NONE_RETIRED],
         "TE-005 is cancelled under R6 and has no plan row; rule_row sits with rwb-decision (Ownership Map, ASM-A6-tables-3)."),
    92: (["RWB-PLT-TE006-CON", "RWB-PLT-TE006-APP"],
         "MSG-P4-003 is the out-of-scope text; the delivery-not-found case gets its own message in the outbox library contract (DP-09)."),
    93: ([NONE_RETIRED],
         "TE-007 is retired (Quartz replaced by Temporal Schedules, R6 and ADR-016); JOB-02 becomes the DailyCaseRun workflow in rwb-case and the timing is stated there, with RWB-PLT-E1071-CON for the workflow kit."),
    94: (["RWB-PLT-TE008-APP"],
         "The check field list has nine fields including rerun and copyJobEndedAt in the step and in section 12."),
    95: (["RWB-ITG-TE009-ITG"],
         "The harness owns the masked-copy reload trigger through the P4 contract (DP-08), so the platform administrator is not a second owner."),
    96: (["RWB-ITG-TE010-ITG"],
         "The retry rule is stated once: a failed test that passes on its one retry passes the stage; the criteria are aligned."),
    97: (["RWB-PLT-TE011-APP"],
         "The generated name variants are the three the RuleGenerator emits; entity class names are removed from the step."),
    98: (["RWB-PLT-TE011-APP"],
         "The literal scan covers generated fixtures at run time, so AC3 uses a run-time generated identifier and the step matches it."),
    99: (["RWB-PLT-TE012-APP"],
         "The hash is compared before the write in ContentHashGuard, and storage refusal is the fallback; X9 and AC12 state one order."),
    100: (["RWB-P10-TE013-CON", "RWB-P10-TE013-APP"],
          "The autonomy mode is read from agent_policy as one value; the precondition and the criterion use the same value."),
    101: (["RWB-P10-TE013-APP"],
          "A failed decision-record write is X4: the case stays in its state and the task is raised; section 9 is corrected."),
    102: (["RWB-P1-E1001-APP"],
          "loan_account keeps DF-ACC-001 to DF-ACC-021 and account_payment keeps DF-ACC-022 to DF-ACC-028; AC1 is corrected to section 11."),
    103: ([NONE_CANCELLED],
          "RWB-E1-010 is cancelled under R6; the tracker refusal fixture has no target story."),
    104: (["RWB-P3-E1030-APP"],
          "The 5 cases in TDR-BKK-CO are an overflow placement, so MSG-P3-011 and AC4 say the same thing."),
    105: (["RWB-PLT-E1044-APP-2"],
          "RWB_SCHEMA is rwb_case in DEV and SIT and per service in production (DP-01, ADR-014); the delta story replaces the monolith assumption."),
    106: ([NONE_CANCELLED],
          "RWB-E1-012 is cancelled under R6; the report-filing criterion has no target story."),
    107: (["RWB-P4-E1022-APP"],
          "The menu is the gateway-bff composite route (DP-19) and not an Epic 1 business screen; section 15 states the route set."),
    108: (["RWB-PLT-E1056-OPS"],
          "One message per threshold case; MSG-P2-004 keeps its text and the criterion uses the failed-run case only."),
    109: (["RWB-P1-E1015-APP"],
          "The DP06 stamp carries the business date of the run and the Monday commit; one date is used in the Background, AC3 and AC8."),
    110: ([NONE_CANCELLED],
          "RWB-E1-006 is cancelled under R6; the DQ07 validity criterion has no target story."),
    111: (["RWB-P1-E1016-APP"],
          "The access load reads no role table (Ownership Map, role to P4); AC4 is corrected to the session role codes."),
    112: (["RWB-PLT-TE006-APP"],
          "An event with no case raises the MSG-P2-001 exception-queue task; AC10 is aligned with X8."),
    113: (["RWB-P2-E1007-APP"],
          "Closed row: the inbound half is removed and INT-15 is not loaded, so AC1 no longer adds it."),
    114: (["RWB-P3-E1018-APP"],
          "The case-number sequence is stated once; AC4 and AC8 use consecutive numbers."),
    115: (["RWB-P4-E1039-CON", "RWB-P4-E1039-APP"],
          "One path: POST /api/recovery/access/v1/admin/break-glass-grants, in the contract and in sections 3, 7 and 16."),
    116: (["RWB-P7-E1008-OPS", "RWB-P7-E1008-APP"],
          "The nightly chain check is JOB-14, a Temporal Schedule in rwb-decision (Ownership Map, Jobs), so it leaves section 19 of the APP story and lands in the OPS story."),
    117: (["RWB-P3-E1028-APP"],
          "The SERVICE_LEVEL row for HIRE_PURCHASE and ASSIGNED is 5 working days, in the Background and in AC4."),
    118: (["RWB-P3-E1042-CON", "RWB-P3-E1042-APP"],
          "The parameter default 300 is the UAT value; AC4 and the catalog seed agree (DP-06)."),
    119: (["RWB-PLT-TE008-APP"],
          "The failed run covers business date 2 December 2026 and the last complete check is the earlier date; the message text and the criterion agree."),
    120: (["RWB-PLT-TE008-APP"],
          "MSG-P7-008 takes a list of entry IDs, so one report names both entries; the message template is widened."),
    121: (["RWB-PLT-NF06-DB"],
          "No copy of an ACE view column (ADR-014, DP-01, DP-05). Owner per Ownership Map: hearing and legal_action S4 rwb-litigation, notice P6 rwb-comms, write_off S7 rwb-writeoff, asset_sale S5 rwb-asset, proceeds P8 rwb-payment, dp_treatment and interaction P1 rwb-source-data, decision_log_entry P7 rwb-decision, debt_sale_account S6 rwb-debtsale, treatment S2 rwb-treatment, recovery_case P3 rwb-case; the column drop lands in each owner's story (CG-C-DEF-1)."),
    122: (["RWB-P1-E1002-APP", "RWB-P3-E1018-APP"],
          "Closed row: case_list_row is P1's daily projection (ASM-A6-tables-2) and case_entry_exclusion is P3's; both keys are built in those stories."),
    123: (["RWB-P3-E1018-CON", "RWB-P3-E1018-APP"],
          "Section 12 states that primaryPersonKey carries v_ace_customer.person_key (DP-05) and that no generated id is published; the field name is aligned with RWB-E1-002 and RWB-E2-016."),
    124: (["RWB-S2-E2006-APP", "RWB-P7-E2006-APP"],
          "The NLEADS reference, result, reason and approval level are read from v_ace_credit_decision (DP-05); the officer's judgement and the reference go to the decision log (DP-03)."),
    125: (["RWB-P1-E2010-APP"],
          "dp_treatment is keyed (treatment_id, business_date) (Ownership Map, dp_treatment to P1); the migration in RWB-P1-E2010-APP is changed and AC2 reads 40 rows."),
}


def load_catalog():
    wb = openpyxl.load_workbook(CAT, data_only=True)
    ws = wb["Stories"]
    hdr = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
    out = {}
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[0]:
            out[r[0]] = dict(zip(hdr, r))
    return out


def load_source():
    wb = openpyxl.load_workbook(SRC, data_only=True)
    ws = wb["Defects"]
    rows = []
    for i in range(5, ws.max_row + 1):
        v = [ws.cell(row=i, column=c).value for c in range(1, 8)]
        rows.append({"row": i, "story": v[0] or "", "step": v[1] or "", "what": v[2] or "",
                     "status": v[3] or "", "ruled": v[4] or "", "decision": v[5] or "", "decided": v[6] or ""})
    return rows


def main():
    cat = load_catalog()
    src = load_source()
    assert len(src) == len(MAP) == 121, (len(src), len(MAP))

    sheet_rows = [
        ["SCB Collections and Recovery. Henka Group, 22 November 2026."],
        ["(C) Siam Commercial Bank and Henka Pte Ltd"],
        [],
        ["Change log"],
        ["Version", "Date", "Change", "Decision", "Tool"],
        ["v5", "22 November 2026", "D-RCV-60 microservice realignment: every defect of v4 kept unchanged on the Defects sheet and mapped to the new story IDs", DEC, TOOL],
        [],
        ["How to read this sheet"],
        ["The Defects sheet of this workbook is v4 unchanged: one row per defect, the same story keys, steps, text, status, rulings and dates."],
        ["This sheet adds one row per defect with the story or stories of the D-RCV-60 realignment that will carry the fix."],
        ["Owner and service come from the Ownership Map v1; work type, suggested owner and release come from the Service Story Catalog v1."],
        ["Release dates are copied unchanged and marked (tentative). No date is raised as a gap."],
        ["A defect of a legacy key that R6 cancels or retires has no new story; the row says so in place of a story ID."],
        ["Defect IDs DEF-001 to DEF-121 are the register numbers of this run; two v4 rows already carry the narrative labels DEF-05 and DEF-06 in their text and those labels are kept word for word."],
        [],
        ["Defect", "Story in v4", "Step", "Status in v4", "Realigned story (D-RCV-60)", "Work type(s)",
         "Owner (Ownership Map)", "Suggested owner (R5.3)", "Release", "Mapping note"],
    ]

    defects = []
    for n, r in enumerate(src, start=1):
        did = f"DEF-{n:03d}"
        stories, note = MAP[r["row"]]
        is_none = stories[0].startswith("No new story")
        if is_none:
            wts, owners, phrases, rels = "n/a", "n/a", "n/a", "n/a"
            story_cell = stories[0]
        else:
            wts, owners, phrases, rels = [], [], [], []
            for s in stories:
                c = cat.get(s)
                if not c:
                    raise SystemExit(f"story not in catalog: {s}")
                wt = {"Contract": "CON", "App development": "APP", "ACE DB": "DB", "Infrastructure": "INF",
                      "DevOps": "OPS", "Integration": "ITG"}.get(c["Work type"], c["Work type"])
                if wt not in wts:
                    wts.append(wt)
                svc = c["Service"]
                if svc == "platform":
                    svc = "platform (PLT)"
                elif svc == "integration":
                    svc = "integration (ITG)"
                if svc not in owners:
                    owners.append(svc)
                if c["Suggested owner"] not in phrases:
                    phrases.append(c["Suggested owner"])
                rel = c["Release"] or "Not specified in the source documents (ASM-C-DEF-11)"
                if rel not in rels:
                    rels.append(rel)
            story_cell = "; ".join(stories)
            wts, owners, phrases, rels = " + ".join(wts), "; ".join(owners), "; ".join(phrases), "; ".join(rels)
        sheet_rows.append([did, r["story"], r["step"], r["status"], story_cell, wts, owners, phrases, rels, note])
        defects.append({"id": did, "legacy": r["story"], "story": story_cell, "note": note})

    (OUT / "rows.json").write_text(json.dumps([r or [""] for r in sheet_rows], ensure_ascii=False, indent=0), encoding="utf-8")

    with (WORK / "plan" / "defects.jsonl").open("w", encoding="utf-8") as f:
        for d in defects:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")

    gaps = [
        {"id": "CG-C-DEF-1", "title": "The 42-column drop of DEF-05 has no named story for seven services",
         "source": "Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v4.xlsx row 121 (DEF-05); Recovery Workbench Microservice Ownership Map v1 Tables and Services sheets; Service Story Catalog v1 Stories sheet",
         "section": "Defects, row 121 (all retained Workbench tables)",
         "description": "DEF-05 rules that each owning story drops the source-system and source-field columns of the retained tables. The Ownership Map names twelve owning services (S4, P6, S7, S5, P8, P1, P7, S6, S2, P3 and P1 again for the interaction ledger), but the catalog has an ACE DB story for only P1, P3, P4, P7 and the platform. No story ID exists for the column drop in S2 rwb-treatment, S4 rwb-litigation, S5 rwb-asset, S6 rwb-debtsale, S7 rwb-writeoff, P6 rwb-comms and P8 rwb-payment.",
         "evidence": "Ownership Map v1 Tables sheet (hearing and legal_action S4, notice P6, write_off S7, asset_sale S5, proceeds P8, dp_treatment and interaction P1, decision_log_entry P7, debt_sale_account S6, treatment S2, recovery_case P3); Service Story Catalog v1 Stories sheet filtered on work type ACE DB gives RWB-PLT-NF06-DB, RWB-PLT-N011-DB, RWB-P4-AD006-DB, RWB-P4-E1022-DB, RWB-P4-E1039-DB, RWB-P3-E1019-DB, RWB-P7-E1008-DB, RWB-P1-ACE001-DB, RWB-P1-E1016-DB, RWB-P1-E1065-DB and RWB-P1-E1069-DB only",
         "type": "Missing", "area": "Data", "severity": "P2", "needed_by_wave": "2", "legacy_ref": "RWB-E2-010; RWB-E2-024; RWB-E2-025",
         "owner_role": "Data architect", "asm": "ASM-C-DEF-6",
         "proposed": "Raise one ACE DB story per service without one (S2, S4, S5, S6, S7, P6, P8) for the column drop, or attach the drop to the APP story that creates the table, and cite the chosen story on row 121 before wave 2 starts",
         "wp": "C-DEF"},
        {"id": "CG-C-DEF-2", "title": "Open defects of retired and cancelled keys have no target story",
         "source": "Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v4.xlsx rows 9, 13, 14, 18, 21, 22, 29, 42, 91, 93, 103, 106, 110; Template and Rules v1 R6",
         "section": "Defects, rows with a cancelled or retired legacy key",
         "description": "Twelve open or regated defects belong to legacy keys that R6 cancels or retires (RWB-E1-003, E1-005, E1-006, E1-010, E1-012, E1-014, E1-029, E1-048, TE-005, TE-007). They have no new story, so the defect cannot be closed by a story; the source keeps them with their v4 status and this sheet maps them to 'No new story'.",
         "evidence": "Split plan legacy rows for those keys with retired or empty slices; Template and Rules v1 R6 table (Already cancelled and Retired rows); source rows 9, 13, 14, 18, 21, 22, 29, 42, 91, 93, 103, 106, 110",
         "type": "Outdated", "area": "Delivery", "severity": "P3", "needed_by_wave": "1", "legacy_ref": "RWB-E1-014; RWB-TE-007",
         "owner_role": "Delivery lead", "asm": "ASM-C-DEF-4",
         "proposed": "Close those rows as 'closed with the key' in the verification loop, or move the behaviour to the story that now owns it (JOB-02 to the DailyCaseRun workflow, the retention class to rwb-document)",
         "wp": "C-DEF"},
        {"id": "CG-C-DEF-3", "title": "Two v4 rows carry narrative defect labels that do not match a register number",
         "source": "Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v4.xlsx rows 121 and 122",
         "section": "Defects, rows 121 and 122",
         "description": "Rows 121 and 122 open their text with DEF-05 and DEF-06 while the other 119 rows carry no defect label at all. The v4 sheet has no ID column, so the labels cannot be reconciled with a sequence; this run numbers every row DEF-001 to DEF-121 in sheet order and keeps the two narrative labels word for word.",
         "evidence": "Source rows 121 and 122 text; the remaining rows begin with the story key or with 'the'",
         "type": "ID collision", "area": "Documentation", "severity": "P3", "needed_by_wave": "1", "legacy_ref": "",
         "owner_role": "Delivery lead", "asm": "ASM-C-DEF-1",
         "proposed": "Adopt DEF-001 to DEF-121 as the register numbering and keep DEF-05 and DEF-06 as historical labels only",
         "wp": "C-DEF"},
        {"id": "CG-C-DEF-4", "title": "No source states the replacement timing rule for the retired Quartz job behind row 93",
         "source": "Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v4.xlsx row 93; Recovery Workbench Batch and Scheduling Design v4; Ownership Map v1 Jobs sheet",
         "section": "Defects, row 93 (RWB-TE-007)",
         "description": "Row 93 reconciles two Quartz instances being down from 04:30 to 09:40 against JOB-02 succeeding at 05:50. R6 retires the Quartz scheduler and the Ownership Map replaces JOB-02 with an event-started DailyCaseRun workflow in rwb-case, but no source states whether the workflow keeps the 04:30 start window or when the first case run must finish.",
         "evidence": "Ownership Map v1 Jobs sheet (JOB-02 event-started workflow, DailyCaseRun in rwb-case); Template and Rules v1 R6 Retired row for RWB-TE-007; Architecture v5 Text Extract v1 slide 44",
         "type": "Missing", "area": "Workflow", "severity": "P2", "needed_by_wave": "1", "legacy_ref": "RWB-TE-007",
         "owner_role": "Recovery tech lead", "asm": "ASM-C-DEF-9",
         "proposed": "State the start window of the DailyCaseRun workflow and its expected finish in RWB-P3-E2002-CON, then close row 93 against that contract",
         "wp": "C-DEF"},
    ]
    with (WORK / "gaps" / "C-DEF.jsonl").open("w", encoding="utf-8") as f:
        for g in gaps:
            f.write(json.dumps(g, ensure_ascii=False) + "\n")

    asm = [
        {"id": "ASM-C-DEF-1", "text": "Every defect row gets the register number DEF-001 to DEF-121 in v4 sheet order",
         "why": "the v4 sheet has no ID column, and two rows carry the narrative labels DEF-05 and DEF-06", "read": "source rows 5 to 125", "gap": "CG-C-DEF-3", "applied_in": "Realignment v5 sheet, column Defect", "confidence": "High", "confirm": "Delivery lead", "impact": "the register numbering is stable for the verification loop", "wp": "C-DEF"},
        {"id": "ASM-C-DEF-2", "text": "A defect that names a contract section, an operation or a message map is mapped to the CON story, and a defect that names a flow step, a criterion or a test case is mapped to the APP story",
         "why": "the split rule puts the contract in the CON story and the behaviour in the APP story", "read": "Template and Rules v1 R5.3, R5.7 and R7.2; split plan slices", "gap": "", "applied_in": "Realignment v5 sheet, column Realigned story", "confidence": "High", "confirm": "", "impact": "one fix owner per side of the contract", "wp": "C-DEF"},
        {"id": "ASM-C-DEF-3", "text": "A header defect is mapped to every story of its legacy key, because the tag, the epic and the release are metadata of all of them",
         "why": "no single story owns a header, and v5 writes the header on each file", "read": "Template and Rules v1 R7.1 and R8.7", "gap": "", "applied_in": "rows 7, 78 and 79", "confidence": "High", "confirm": "", "impact": "three rows list four or five stories", "wp": "C-DEF"},
        {"id": "ASM-C-DEF-4", "text": "A defect of a legacy key that R6 cancels or retires is recorded as 'No new story' and keeps its v4 status",
         "why": "R6 forbids a new story for those keys and the source status is not the realignment's to change", "read": "Template and Rules v1 R6; split plan legacy rows with no slice", "gap": "CG-C-DEF-2", "applied_in": "rows 9, 13, 14, 18, 21, 22, 29, 42, 91, 93, 103, 106, 110", "confidence": "High", "confirm": "", "impact": "thirteen rows carry no story ID", "wp": "C-DEF"},
        {"id": "ASM-C-DEF-5", "text": "Owner, service, work type, suggested-owner phrase and release are taken from the Ownership Map v1 and the Service Story Catalog v1, and the release keeps its (tentative) marker",
         "why": "the Work Package fixes the Ownership Map as the owner source and R1 U7 keeps dates unchanged and tentative", "read": "Ownership Map v1 Services and Tables sheets; Service Story Catalog v1 Stories sheet", "gap": "", "applied_in": "Realignment v5 sheet, columns Work type, Owner, Suggested owner and Release", "confidence": "High", "confirm": "", "impact": "no person name appears in the document", "wp": "C-DEF"},
        {"id": "ASM-C-DEF-6", "text": "Row 121 (DEF-05) cites RWB-PLT-NF06-DB for the schema work and lists the twelve owning services in the note, because no per-service column-drop story exists",
         "why": "the catalog has ACE DB stories for P1, P3, P4, P7 and the platform only", "read": "Service Story Catalog v1 Stories sheet; Ownership Map v1 Tables sheet", "gap": "CG-C-DEF-1", "applied_in": "row 121", "confidence": "Medium", "confirm": "Data architect", "impact": "the column drop has a platform anchor and seven services without a story", "wp": "C-DEF"},
        {"id": "ASM-C-DEF-7", "text": "The Status, Ruled by, Decision and Decided on columns of v4 are copied word for word, including two cells that hold a date where a decision was expected",
         "why": "R1 keeps every number and date of the source and the realignment changes only the mapping", "read": "source rows 9, 11, 122", "gap": "", "applied_in": "Defects sheet left unchanged; Status repeated on the Realignment v5 sheet", "confidence": "High", "confirm": "", "impact": "the v4 rulings survive the version bump", "wp": "C-DEF"},
        {"id": "ASM-C-DEF-8", "text": "The Realignment v5 sheet is placed first so the workbook opens on the two R8.1 header lines and the change-log row",
         "why": "R8.1 puts the header on every new document and the source Defects sheet keeps its own title rows", "read": "Template and Rules v1 R8.1 and R8.2", "gap": "", "applied_in": "workbook sheet order", "confidence": "High", "confirm": "", "impact": "the Defects sheet stays byte for byte as v4", "wp": "C-DEF"},
        {"id": "ASM-C-DEF-9", "text": "Row 93 is mapped to 'No new story' with the replacement named in the note, and the missing timing rule is raised as a gap rather than a story",
         "why": "R6 retires RWB-TE-007 and no source gives the DailyCaseRun window", "read": "Ownership Map v1 Jobs sheet; Template and Rules v1 R6", "gap": "CG-C-DEF-4", "applied_in": "row 93", "confidence": "Medium", "confirm": "Recovery tech lead", "impact": "the row closes against the rwb-case contract once the window is stated", "wp": "C-DEF"},
        {"id": "ASM-C-DEF-10", "text": "Rows whose v4 status is Closed, Fixed or Regated keep that status and still name where the fix lives",
         "why": "a closed defect is still traceable to the story that carries the built behaviour", "read": "source rows 10, 11, 15, 16, 17, 23, 82, 83, 84, 103, 106, 110, 113, 122", "gap": "", "applied_in": "Status in v4 column and the mapping note", "confidence": "High", "confirm": "", "impact": "no built behaviour is re-opened by the realignment", "wp": "C-DEF"},
        {"id": "ASM-C-DEF-11", "text": "A platform story with no release date in any source shows the R9 placeholder and its wave instead, and no date is raised as a gap",
         "why": "R1 U7 and rule 10 forbid raising a date as a gap, while R9 wants a placeholder and an assumption row", "read": "Service Story Catalog v1 Stories sheet (empty Release for RWB-PLT-N001 to N012 and the W<n>J01 harness stories); Template and Rules v1 R9", "gap": "", "applied_in": "Release column for RWB-PLT-NF06-DB", "confidence": "High", "confirm": "", "impact": "the workbook carries no invented release date", "wp": "C-DEF"},
    ]
    with (WORK / "assumptions" / "C-DEF.jsonl").open("w", encoding="utf-8") as f:
        for a in asm:
            f.write(json.dumps(a, ensure_ascii=False) + "\n")

    print(f"rows={len(sheet_rows)} defects={len(defects)} gaps={len(gaps)} asm={len(asm)}")


if __name__ == "__main__":
    main()

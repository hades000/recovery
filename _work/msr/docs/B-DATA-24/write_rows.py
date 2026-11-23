"""Write the candidate gap and assumption rows for B-DATA-24 (one assumption per gap)."""
import json
from pathlib import Path

WP = "B-DATA-24"
SRC = "06 Data/Recovery Workbench Data Classification and Personal Data Inventory v4.xlsx"
DOC = "06 Data/Recovery Workbench Data Classification and Personal Data Inventory v5.xlsx"

GAPS = [
    dict(
        n=1,
        title="The 30 ACE source views have no owner in the Ownership Map",
        section="Fields (the 30 recovery.v_ace_* entities and their 304 fields)",
        description="The Fields tab classifies 304 fields of the 30 recovery.v_ace_* views. The Ownership Map v1 "
                    "sheet Tables lists 93 Workbench tables and no view, so the Owner column appended in v5 has no "
                    "map row for those 304 fields and the ownership of the view contract has to be read from the "
                    "architecture instead.",
        evidence="Architecture v5 Text Extract v1 line 707 (only rwb-source-data reads the 30 recovery.v_ace_* "
                 "views), line 850 (SQL view: only rwb-source-data, read-only login, 30 views), lines 2147 and "
                 "2884 (schema recovery holds the 30 views; P1 owns the ACE view contract and the extension "
                 "tables); Ownership Map v1 sheet Tables, 93 rows, none of them a v_ace_* view; DP-05; ADR-010.",
        type="Missing", area="Ownership", severity="P2", wave="1", legacy="RWB-E1-069",
        owner_role="Data architecture team", asm=1,
        proposed="P1 rwb-source-data owns the 30 views under the ACE view contract. The Owner column reads "
                 "P1 rwb-source-data (recovery view) on all 304 view fields, and no other service login holds a "
                 "grant on a view.",
    ),
    dict(
        n=2,
        title="payment_match_rule is in the inventory but not in the Ownership Map, and D-RCV-36 retires it as a table",
        section="Fields (payment_match_rule, DF-REF-261 to DF-REF-273)",
        description="The Fields tab classifies the 13 fields of payment_match_rule. The Ownership Map has no row "
                    "for the table, and PRD P8 records it retired by D-RCV-36: the values become versioned "
                    "parameter and reference rows and the logic becomes the PAYMENT_MATCH rule package, so the "
                    "entity has an owner and a disposition that the inventory does not state.",
        evidence="PRD P8 rwb-payment v1 lines 123, 169 and 250 (payment_match_rule retired by D-RCV-36; versioned "
                 "parameter and reference rows in rwb-case and the PAYMENT_MATCH rule package in rwb-decision); "
                 "Recovery Workbench Temporal and Drools Design Text Extract v1 line 1084 (PAYMENT_MATCH replaces "
                 "payment_match_rule, T10); Physical Schema v6.sql rows DF-REF-261 to DF-REF-273; Ownership Map v1 "
                 "sheet Tables, no row payment_match_rule.",
        type="Outdated", area="Ownership", severity="P2", wave="2", legacy="RWB-E2-027",
        owner_role="Business analysis team", asm=2,
        proposed="The 13 rows are kept with their field IDs and marked retired as a table. The Owner column reads "
                 "P3 rwb-case (retired table) because the values live as versioned reference rows there, and the "
                 "PAYMENT_MATCH rule package is P7 rwb-decision.",
    ),
    dict(
        n=3,
        title="lake_copy_watermark is still an entity of the inventory although the data lake is removed",
        section="Fields (lake_copy_watermark, DF-OPS-130 to DF-OPS-135)",
        description="Six fields of lake_copy_watermark are classified as Workbench data. The target architecture "
                    "has no data lake and no Power BI connection, so the table has nothing to watermark and the "
                    "inventory still presents it as live data with an on-screen rule and a retention rule.",
        evidence="Architecture v5 Text Extract v1 line 67 and line 707 (Recovery has no connection to the data "
                 "lake; INT-19 and INT-20 removed), line 2988 (JOB-13: the decision log copy is replaced by "
                 "continuous Kafka ingest); ADR-018; DP-17; Template and Rules R6 (RWB-E1-014 retired).",
        type="Outdated", area="Ownership", severity="P3", wave="1", legacy="RWB-E1-014",
        owner_role="Data architecture team", asm=3,
        proposed="The six rows are kept with their field IDs and marked retired with the data lake; the Owner "
                 "column reads P1 rwb-source-data (retired table) and no copy is built.",
    ),
    dict(
        n=4,
        title="OCR text is classified Not personal while the same content at field level is Restricted",
        section="Fields (document_text.text_content, DF-DOC-089; document_field.field_value, DF-DOC-015)",
        description="document_text.text_content, the OCR text of a page of a customer document, is classified Not "
                    "personal and Internal with the note masked by role on read, while document_field.field_value, "
                    "the same content read as a field, is a Direct identifier at Restricted. One of the two rows "
                    "must be wrong, and the field-level rule for events, workflow inputs and logs cannot be read "
                    "from the category alone.",
        evidence="v4 Fields DF-DOC-089 (Not personal; Internal; No; Shown by permission; Meaning: OCR text of the "
                 "page; masked by role on read) against DF-DOC-015 (Direct identifier; Restricted; Yes; Masked "
                 "unless the role may see it); v4 Handling row 5 (Restricted fields encrypted at rest) and row 21 "
                 "(contact values masked for display); Key row 5 (Direct identifier identifies a person on its "
                 "own, free text about them).",
        type="Conflict", area="Personal data", severity="P2", wave="1", legacy="RWB-E1-037",
        owner_role="Data steward", asm=4,
        proposed="The classification is left for the data steward. In this version the row carries the rule "
                 "never in an event, a workflow input or a log, and the page id only in a log, which is what a "
                 "Restricted field gets.",
    ),
    dict(
        n=5,
        title="One recovery identity reads the ACE views; the target has one login and one schema per service",
        section="Handling (Restricted, Every ACE read; Restricted, In logs)",
        description="The Handling tab gives the recovery identity SELECT on recovery.v_ace_* and assumes that any "
                    "service may read a view. Under D-RCV-60 there are 19 schemas and 19 logins, only "
                    "rwb-source-data reads the 30 views, and no other login has a grant on them or on public, so "
                    "the rule and the read-audit path change.",
        evidence="v4 Handling rows 7 and 22 (the recovery identity holds SELECT only on recovery.v_ace_*; every "
                 "read of a v_ace_* personal field is logged through PII Kafka); Architecture v5 Text Extract v1 "
                 "lines 509, 707, 909, 2051, 2126, 2143, 2147, 2533, 3016, 3038 (one login and one schema per "
                 "service; only rwb-source-data reads the views); ADR-010; ADR-014; DP-01; DP-02; DP-05.",
        type="Outdated", area="Access", severity="P2", wave="1", legacy="RWB-E1-069",
        owner_role="Solution architecture team", asm=5,
        proposed="Only the rwb_source_data login holds SELECT on the 30 views; every other service reads the same "
                 "data through the P1 REST contract or a Temporal activity, and the read audit is written through "
                 "the ACE Common PII logging path.",
    ),
    dict(
        n=6,
        title="The PII log path is named PII Kafka with no owner and no separation from the business topics",
        section="Handling (Restricted, In logs); Key (Read audit)",
        description="The inventory sends every read of a personal field to PII Kafka and records the read audit in "
                    "the access log, without saying that this is the ACE Common path to the SOC or that the "
                    "Recovery business topics are a different set of topics. A reader can conclude that a personal "
                    "field may travel on rwb.<service>.events.v1.",
        evidence="v4 Handling row 7 (logged through PII Kafka) and row 22 (a read is audited); v4 Key row 16 "
                 "(written to the access log through PII Kafka); Architecture v5 Text Extract v1 line 511 (ACE "
                 "Common gives audit and PII logging, PII Kafka to SOC), line 1503 (Recovery business-event topics "
                 "separate from ACE's PII logging topics), lines 2179 to 2183 (Kafka PII path to SOC) and line "
                 "2537 (ACE PII logging to SOC).",
        type="Ambiguous", area="Logging", severity="P3", wave="1", legacy="RWB-E1-037",
        owner_role="Security team", asm=6,
        proposed="The rule names the ACE Common PII logging path to the SOC (INT-34) and states that the business "
                 "topics are separate and carry no personal data.",
    ),
    dict(
        n=7,
        title="The masking rule has no owner on the page that lists who sees what",
        section="Who sees what (note row 2 and the 14 role rows)",
        description="The sheet is proposed until Compliance issues the masking rules under DL26 and names no owner "
                    "for the rule. Under D-RCV-60 the masking policy is P4 rwb-access data, enforced in each "
                    "service, so the page needs the owner and where the rule is applied.",
        evidence="v4 Who sees what A2 (proposed until Compliance issues the masking rules, DL26); Architecture v5 "
                 "Text Extract v1 line 1020 (P4 writes the masking policy in rwb_access), line 2882 (P4 owns "
                 "masking policy), line 2562 (masking rules (P4) enforced in each service), line 776 (ACE data "
                 "masked by policy at the gateway); RWB-P4-E1037-CON.",
        type="Missing", area="Access", severity="P3", wave="1", legacy="RWB-AD-004",
        owner_role="Compliance team", asm=7,
        proposed="An Enforced by column names P4 rwb-access for the policy, the owning service that applies it, "
                 "P10 rwb-agent for a prompt and the P1 login for an ACE value; DL26 still owns the rule content.",
    ),
    dict(
        n=8,
        title="The inventory has no rule for events, workflow inputs or logs",
        section="Handling; Key; Who sees what",
        description="The inventory classifies storage, screens, prompts, test data, export and the debt sale tape, "
                    "but it has no rule for a Kafka event, a Temporal workflow input or history, or an application "
                    "log. Those are the three channels the realignment must close, so every field carries no "
                    "statement about what may leave the service.",
        evidence="v4 Handling B5 to B22 (Where values: Stored, On screen, In logs, In agent prompts, In test data, "
                 "Export, Debt sale tape, Retention, Data subject request, In ACE, Contact values, Every ACE read) "
                 "has no row for an event or a workflow; Architecture v5 Text Extract v1 line 833 (Never: personal "
                 "data in events, I/O or PII in workflow code or payloads), line 1618 (Payload: IDs and business "
                 "facts, no PII), line 3064 and Temporal and Drools Design Text Extract v1 line 1885 (payload codec, "
                 "search attributes); Template and Rules R7.2 s17.",
        type="Missing", area="Personal data", severity="P2", wave="1", legacy="None (new, D-RCV-60)",
        owner_role="Solution architecture team", asm=8,
        proposed="Three appended columns on Fields and Identifiers, six new Handling rows and a new PII controls "
                 "sheet give the rule per field and per channel, with the owner of each control.",
    ),
    dict(
        n=9,
        title="The interaction ledger is defined by the case module but the Ownership Map gives it to P1",
        section="Fields (interaction, 29 fields); Identifiers",
        description="The interaction entity carries 29 classified fields and the case timeline reads it. The "
                    "Ownership Map gives the ledger to P1 rwb-source-data under the R-PREC default ruling and keeps "
                    "the timeline API with P3 rwb-case, so the Owner column shows P1 on 29 fields that a reader of "
                    "this inventory would expect on the case service.",
        evidence="Ownership Map v1 sheet Rulings row interaction (ledger and intake rule stay with P1; the case "
                 "timeline and interaction API stay with P3, ASM-A6-tables-1); Ownership Map sheet Tables row "
                 "interaction (P1); Architecture v5 Text Extract v1 line 2884 (P1 owns the ACE view contract and "
                 "the extension tables) and Template and Rules R3 default ruling list (interaction ledger, P1); "
                 "DP-18.",
        type="Conflict", area="Ownership", severity="P3", wave="1", legacy="RWB-E1-066; RWB-E1-068",
        owner_role="Solution architecture team", asm=9,
        proposed="The Owner column follows the map: P1 rwb-source-data on the 29 interaction fields, and P3 "
                 "rwb-case reads the ledger through the P1 contract for the case timeline.",
    ),
]

ASSUMPTIONS = [
    dict(
        n=1,
        text="P1 rwb-source-data owns the 30 recovery.v_ace_* views under the ACE view contract, so all 304 view "
             "fields carry P1 rwb-source-data (recovery view) in the Owner column and no other service reads a view.",
        why="The Ownership Map lists tables and not views, and the architecture gives the views, their grants and "
            "the boundary rule to rwb-source-data; leaving 304 fields without an owner would break the WP rule that "
            "every owner comes from the map.",
        read="Architecture v5 Text Extract v1 lines 707, 850, 909, 2147, 2884, 3016 and 3038; Ownership Map v1 "
             "sheet Tables (93 rows) and sheet Services row P1; DP-05; ADR-010.",
        confidence="High",
        confirm="Data architecture team confirms that the view contract and the grants sit with rwb-source-data "
                "and adds the 30 views to the next Ownership Map version.",
        impact="One owner for the views; every other service reads ACE data through the P1 REST contract or an "
               "activity, and no second grant on a view is issued.",
        applied="Fields column K on the 304 view fields; Summary block; PII controls",
    ),
    dict(
        n=2,
        text="payment_match_rule stays in the inventory with its 13 field IDs, marked retired as a table: the "
             "values live as versioned parameter and reference rows in P3 rwb-case and the logic as the "
             "PAYMENT_MATCH rule package in P7 rwb-decision.",
        why="PRD P8 records the retirement by D-RCV-36 and the Ownership Map has no row for the table, so the "
            "owner and the disposition have to be stated here or the 13 fields stay unowned.",
        read="PRD P8 rwb-payment v1 lines 123, 169 and 250; Recovery Workbench Temporal and Drools Design Text "
             "Extract v1 line 1084; Physical Schema v6.sql DF-REF-261 to DF-REF-273; Ownership Map v1 sheet "
             "Tables.",
        confidence="High",
        confirm="Business analysis team confirms the reference rows are P3 and the rule package is P7 in the next "
                "data model version.",
        impact="No payment_match_rule table is built; the matching values are versioned rows and the matching "
               "logic is a rule package.",
        applied="Fields columns K to M on DF-REF-261 to DF-REF-273; Summary block; PII controls",
    ),
    dict(
        n=3,
        text="lake_copy_watermark is retired with the data lake and keeps its six rows and field IDs, with P1 "
             "rwb-source-data as the owner and no copy built.",
        why="Arch v5 removes the data lake and INT-19 and INT-20, and ADR-018 and DP-17 replace the copies with "
            "the event-fed read model, so the entity cannot stay live in the inventory.",
        read="Architecture v5 Text Extract v1 lines 67, 707 and 2988; ADR-018; DP-17; Template and Rules R6 "
             "(RWB-E1-014 retired).",
        confidence="Medium",
        confirm="Data architecture team confirms the table is dropped from the next physical schema version.",
        impact="No watermark table and no lake copy; the read model in rwb-reporting is rebuilt from the topics.",
        applied="Fields columns L and M on DF-OPS-130 to DF-OPS-135; Summary block; PII controls",
    ),
    dict(
        n=4,
        text="document_text.text_content keeps its source classification and carries the rule of a Restricted "
             "field: never in an event, a workflow input or a log, and the page id only in a log.",
        why="The same content is a Direct identifier at Restricted on document_field.field_value, so a Not "
            "personal row cannot be read as permission to carry OCR text out of the service; the classification "
            "itself belongs to the data steward.",
        read="v4 Fields DF-DOC-089 and DF-DOC-015; v4 Handling row 5 and row 21; v4 Key row 5; Architecture v5 "
             "Text Extract v1 line 833.",
        confidence="Medium",
        confirm="Data steward decides whether document_text.text_content is reclassified as Restricted or Direct "
                "identifier in the next version.",
        impact="OCR text never leaves rwb-document through an event, a workflow or a log; a reader of a field "
               "takes the page through the document contract.",
        applied="Fields columns L and M on DF-DOC-089; Identifiers column I; Read me item 3",
    ),
    dict(
        n=5,
        text="Only the rwb_source_data login holds SELECT on the 30 recovery.v_ace_* views and on nothing else; "
             "every other service reads ACE data through the P1 contract or an activity, and no other login has a "
             "grant on a view or on public.",
        why="The target has one login and one schema per service and gives the view contract to rwb-source-data, so "
            "the single recovery identity of the source cannot be kept and the audit path follows the P1 login.",
        read="Architecture v5 Text Extract v1 lines 509, 707, 850, 2051, 2126, 2143, 2147, 2533, 3016 and "
             "3038; ADR-010; ADR-014; DP-01; DP-02; DP-05.",
        confidence="High",
        confirm="Solution architecture team confirms the grants in the physical schema and the boundary test.",
        impact="One read path to ACE data and one audit point; a direct public read fails in the catalog.",
        applied="Handling C7 and C22; Handling column D; PII controls",
    ),
    dict(
        n=6,
        text="Every read of a personal field is logged through the ACE Common PII logging path to the SOC (INT-34), "
             "and the Recovery business topics rwb.<service>.events.v1 are separate and carry no personal data.",
        why="The source names PII Kafka without an owner and without separating it from the business topics, and "
            "the architecture puts audit and PII logging in ACE Common with its own topics and ACLs.",
        read="Architecture v5 Text Extract v1 lines 501, 511, 1503, 2179 to 2183 and 2537; v4 Handling row 7 and "
             "row 22; v4 Key row 16.",
        confidence="Medium",
        confirm="Security team confirms the PII logging topics and the retention of the access log with the SOC.",
        impact="The audit is one path to the SOC; no personal data appears on a business topic.",
        applied="Handling C7; Handling rows 23 to 28; Key rows 17 to 21; PII controls",
    ),
    dict(
        n=7,
        text="The masking policy is P4 rwb-access data (masking_rule), enforced in each service and applied by "
             "rwb-source-data on every ACE field it serves; the content of the rule stays with Compliance under "
             "DL26.",
        why="The page says the unmasked rules are proposed until DL26 and names no owner, while the architecture "
            "gives the masking policy to rwb-access as data and requires each service to enforce it.",
        read="Architecture v5 Text Extract v1 lines 776, 1020, 2562 and 2882; RWB-P4-E1037-CON; v4 Who sees what "
             "A2.",
        confidence="Medium",
        confirm="Compliance team issues the rule content and P4 confirms the masking_rule rows in the next "
                "release.",
        impact="A masking change is a data change, not a release; every service applies the same policy.",
        applied="Who sees what column E; Handling column D; PII controls",
    ),
    dict(
        n=8,
        text="Three channels are added to the inventory: the Kafka event, the Temporal workflow input and history, "
             "and the application log. Each field carries its rule, and each channel has one owner and one control.",
        why="The realignment requires that no personal data travels in an event, a workflow input or a log, and "
            "the source has no rule for any of the three, so the requirement cannot be checked field by field "
            "without them.",
        read="Architecture v5 Text Extract v1 lines 833, 1618, 2533, 2562, 2936 and 3064; Recovery Workbench "
             "Temporal and Drools Design Text Extract v1 lines 522, 888 and 1885; Template and Rules R7.2 s17.",
        confidence="High",
        confirm="Solution architecture team confirms the per-field rule at the contract review of each service.",
        impact="Every field states what may travel; a schema that carries a personal field fails the registry "
               "check.",
        applied="Fields columns L and M; Identifiers column I; Handling rows 23 to 28; PII controls",
    ),
    dict(
        n=9,
        text="The interaction ledger stays with P1 rwb-source-data and P3 rwb-case reads it through the P1 "
             "contract for the case timeline, so the 29 interaction fields carry P1 in the Owner column.",
        why="The Ownership Map rules the ledger to P1 under the R-PREC default ruling, and this inventory must not "
            "contradict the map it is taking every other owner from.",
        read="Ownership Map v1 sheet Rulings row interaction and sheet Tables row interaction; Architecture v5 Text "
             "Extract v1 line 2884; Template and Rules R3 default ruling list; DP-18.",
        confidence="Medium",
        confirm="Solution architecture team confirms the ledger and the timeline split at the P1 and P3 contract "
                "review.",
        impact="One writer for the ledger; the case timeline is a P3 read of the P1 contract.",
        applied="Fields column K on the 29 interaction fields; PII controls",
    ),
]

gaps_path = Path("_work/msr/gaps") / f"{WP}.jsonl"
asm_path = Path("_work/msr/assumptions") / f"{WP}.jsonl"

with gaps_path.open("w", encoding="utf-8", newline="\n") as f:
    for g in GAPS:
        row = {
            "id": f"CG-{WP}-{g['n']}",
            "title": g["title"],
            "source": SRC,
            "section": g["section"],
            "description": " ".join(g["description"].split()),
            "evidence": " ".join(g["evidence"].split()),
            "type": g["type"],
            "area": g["area"],
            "severity": g["severity"],
            "needed_by_wave": g["wave"],
            "legacy_ref": g["legacy"],
            "owner_role": g["owner_role"],
            "asm": f"ASM-{WP}-{g['asm']}",
            "proposed": " ".join(g["proposed"].split()),
            "wp": WP,
        }
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

with asm_path.open("w", encoding="utf-8", newline="\n") as f:
    for a in ASSUMPTIONS:
        row = {
            "id": f"ASM-{WP}-{a['n']}",
            "text": " ".join(a["text"].split()),
            "why": " ".join(a["why"].split()),
            "read": " ".join(a["read"].split()),
            "gap": f"CG-{WP}-{a['n']}",
            "applied_in": f"{DOC} {a['applied']}",
            "confidence": a["confidence"],
            "confirm": " ".join(a["confirm"].split()),
            "impact": " ".join(a["impact"].split()),
            "wp": WP,
        }
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print("wrote", gaps_path, len(GAPS))
print("wrote", asm_path, len(ASSUMPTIONS))

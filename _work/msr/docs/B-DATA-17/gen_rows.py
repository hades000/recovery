"""Write the candidate gap and assumption rows for B-DATA-17 (one JSON object per line)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
WP = "B-DATA-17"
SRC = "06 Data/Recovery Workbench Conceptual Data Model v6.xlsx"
ARCH = "Architecture v5 Text Extract v1"
DL = "Decision Log v10"
OM = "Ownership Map v1"

gaps = [
    dict(
        title="The 30 recovery.v_ace_* views have no row in the Ownership Map, so the model gives them no owner",
        section="Entities (the 30 v_ace_* rows)",
        description=("v6 holds 122 entities: 88 Workbench tables, the 4 extension tables and the 30 ACE source views, and it has no "
                     "owner column at all. The Ownership Map sheet Tables has 93 rows and every one is a Workbench table, so the 30 "
                     "views have no owner row to take a value from, although they are 30 of the 122 entities and the only read path "
                     "the realignment keeps into ACE."),
        evidence=(f"{ARCH} slide 41 line 1074 (SQL: ACE DB views, SELECT recovery.v_ace_* (30 views)), line 700 (only rwb-source-data "
                  "reads the 30 recovery.v_ace_* views) and line 843 (SQL view: only rwb-source-data, read-only login, 30 views, "
                  f"statement timeout); {OM} sheet Tables, 93 rows, first column holds table names only (account_ext to write_off) and "
                  "no v_ace_* name; v6 Entities row 2 (122 entities: 88 Workbench tables, then the 4 extension tables, then the 30 ACE "
                  "source views)."),
        type="Missing", area="Data / ownership of the ACE source views", severity="P3", needed_by_wave=1,
        legacy_ref="RWB-E1-001", owner_role="Data architecture team", asm="ASM-B-DATA-17-1",
        proposed=("Give all 30 views owning service P1 and target schema 'recovery (ACE, read-only view)', taken from Architecture v5 "
                  "rather than the map, and add a Views sheet to the Ownership Map so the map stays the single source of owners."),
    ),
    dict(
        title="The entity Payment match rule has no row in the Ownership Map and no target table",
        section="Entities (row Payment match rule) and the Reference and access subject area",
        description=("v6 holds Payment match rule with 13 fields in DP14. The table is dropped by D-RCV-36 T10, so the Ownership Map, "
                     "which lists target tables, has no row for it, and the realignment has to name an owner for a row that has no "
                     "target table. The LDM already marks every one of its fields 'Retired by D-RCV-36'."),
        evidence=(f"{DL} D-RCV-36 T10 (payment_match_rule is dropped and payment matching becomes the PAYMENT_MATCH package); the LDM v8 "
                  f"field descriptions of payment_match_rule carry 'Retired by D-RCV-36'; {OM} sheet Tables has no payment_match_rule "
                  "row, while rule_package and rule_package_version are there with owner P7; v6 Entities row Payment match rule."),
        type="Outdated", area="Data / reference data and the rule registry", severity="P3", needed_by_wave=1,
        legacy_ref="RWB-E2-041", owner_role="Solution architect", asm="ASM-B-DATA-17-2",
        proposed=("Keep the entity and all 13 fields, set owning service P7 and target schema rwb_decision, and record in the ownership "
                  "basis that the table is retired and the rule lives in the PAYMENT_MATCH rule package."),
    ),
    dict(
        title="No entity is owned by S1 rwb-valuation, although Architecture v5 gives S1 the valuations and the route decision",
        section="Service ownership (S1 row) and the Collateral and asset subject area",
        description=("The Ownership Map assigns 93 tables to 18 services and the platform library. rwb-valuation owns none of them: the "
                     "appraisal data is the read-only v_ace_valuation view and valuation_ext, both P1 under the map's own ruling, and the "
                     "assets are S5. S1 therefore has no table, no schema content and no DB story of its own in this model, although Arch "
                     "v5 gives it 'valuations, D6 route decision, route agent output'."),
        evidence=(f"{OM} sheet Tables: no row with owner S1; rows valuation_ext (owner P1) and listing and asset_sale (owner S5); {OM} "
                  f"sheet Rulings row valuation_ext (ruling ASM-A6-tables-15 keeps valuation_ext with P1); {ARCH} slide 41 (S1 rwb-valuation "
                  "owning valuations, D6 route decision, route agent output); v6 Entities rows Valuation extension and v_ace_valuation."),
        type="Ambiguous", area="Data / ownership of valuations", severity="P2", needed_by_wave=3,
        legacy_ref="None", owner_role="Solution architect", asm="ASM-B-DATA-17-3",
        proposed=("Record S1 as owning no entity in this version and let its DB story create the rwb_valuation schema with its Flyway "
                  "baseline only; refer the definition of a rwb_valuation table, if one is wanted, to the S1 design review."),
    ),
    dict(
        title="The entity called Rule is rule_row, and the model holds neither rule_package nor rule_package_version",
        section="Entities (row Rule) and the Reference and access subject area",
        description=("v6 names the entity 'Rule', which is not a table name, and holds 18 fields. The LDM maps that name to rule_row. The "
                     "two registry rows that the realignment makes central, rule_package and rule_package_version, are in the Ownership "
                     "Map but not in the model, so one entity name needed resolving and two entities are absent."),
        evidence=("LDM v8 dictionary row rule_row (entity 'Rule', 18 fields, 'One versioned routing rule or sentry') and rows rule_package "
                  f"(5 fields) and rule_package_version; {OM} sheet Tables rows rule_package, rule_package_version, rule_row and rule_test_case, "
                  f"all owner P7, schema rwb_decision; {DL} D-RCV-36 T4 (rule_package_version with rollback) and T6 (rule_row stays the "
                  "rule catalog); v6 Entities row Rule."),
        type="Missing", area="Data / rule registry", severity="P3", needed_by_wave=1,
        legacy_ref="RWB-E1-073", owner_role="Solution architect", asm="ASM-B-DATA-17-4",
        proposed=("Resolve 'Rule' to rule_row in the ownership basis (done, owner P7) and add rule_package and rule_package_version as "
                  "entities of P7 in the next version; no row of v6 is renamed."),
    ),
    dict(
        title="The 104 relationships are single-schema references and the Ownership Map's FK cut sheet is empty",
        section="Relationships (all 104 rows)",
        description=("v6 draws 104 references as if one schema held every table. With one schema and one login per service, 59 of them now "
                     "cross a service boundary: 11 already point at a read-only ACE view as a business key, and 48 are a Workbench table in "
                     "one service pointing at a Workbench table in another, which cannot stay a foreign key. The Ownership Map has a sheet "
                     "for that cut, and it holds no data row."),
        evidence=(f"{OM} sheet FK cuts: header row only (From table, From owner, To table, To owner, Becomes) and no data row; v6 "
                  "Relationships row 2 (104 relationships, a reference to a v_ace_* view is a business key with no foreign key); Template "
                  "and Rules R4 (schema and login per service) and DP-01 (never read another service's tables); Ownership Map sheet "
                  "Services (19 schemas)."),
        type="Missing", area="Data / cross-service references", severity="P2", needed_by_wave=1,
        legacy_ref="RWB-E1-001", owner_role="Data architecture team", asm="ASM-B-DATA-17-5",
        proposed=("Cut the 48 table-to-table foreign keys to business-key columns, keep the 11 ACE view references as they are, and show all "
                  "three cases per row in the Relationships sheet; each service's DB story creates no foreign key to another schema."),
    ),
    dict(
        title="The four platform library tables have schema 'platform' in the map but are created in every service schema",
        section="Entities (Outbox event, Outbox delivery, Processed event, Idempotency key)",
        description=("The map gives outbox_event, outbox_delivery, processed_event and idempotency_key owner PLT and schema 'platform', while "
                     "the ruling on the same rows says they are library objects created in every service schema. A single target schema per "
                     "entity cannot say both, so the column needed a wording of its own."),
        evidence=(f"{OM} sheet Tables rows outbox_event, outbox_delivery, processed_event and idempotency_key (owner PLT, schema platform) with "
                  "the ruling 'library objects created in every service schema ... ASM-A6-tables-8'; Architecture v5 Text Extract v1 slide 20 "
                  "(every service: own schema with outbox and inbox) and slide 11 (transactional outbox); Template and Rules DP-09."),
        type="Ambiguous", area="Data / platform library objects", severity="P3", needed_by_wave=1,
        legacy_ref="None", owner_role="Data architecture team", asm="ASM-B-DATA-17-6",
        proposed=("Write target schema 'every service schema (platform library object)' for the four rows, keep owner PLT, and record that "
                  "each service's DB story creates its own copy."),
    ),
    dict(
        title="Feature flags are 'Workbench' as system of record in the model but owned by the platform library",
        section="Entities (Feature flag, Feature flag change) in the Loads and operations subject area",
        description=("v6 states 'Workbench' as the system of record of both feature-flag tables. The map moves them to the platform library "
                     "under the default ruling, and P2 only serves the admin API. The preserved column and the new owner now disagree, which "
                     "is left visible rather than edited."),
        evidence=(f"{OM} sheet Tables rows feature_flag and feature_flag_change (owner PLT, schema platform) and sheet Rulings row feature_flag "
                  f"(R-PREC default ruling, ASM-A6-tables-7, P2 serves the admin API); {ARCH} slide 20 (every service from the service template "
                  "and shared libraries); v6 Entities rows Feature flag and Feature flag change, System of record 'Workbench'."),
        type="Conflict", area="Data / feature flags", severity="P3", needed_by_wave=1,
        legacy_ref="None", owner_role="Solution architect", asm="ASM-B-DATA-17-7",
        proposed=("Keep column E word for word, add owner PLT and target schema 'platform library', and note in the next version that P2 "
                  "serves the admin API against the library."),
    ),
    dict(
        title="The Key sheet has no term for the five realignment concepts the new columns use",
        section="Key (rows 5 to 21)",
        description=("The Key defines 16 terms and values of v6: subject area, data product, entity, system of record, the four system-of-record "
                     "values, the two cardinalities, the two standards and the ACE source view, extension table and business key. It has no "
                     "term for an owning service, a target schema, the platform library, a cross-service reference or a service contract, which "
                     "are the words of every new column."),
        evidence=(f"v6 Key sheet rows 5 to 21 (16 rows) and row 2 (What each term and value means); v6 has no owning-service column anywhere; "
                  f"Template and Rules R4 and R5.5 (schema, login, topic and package per service) and {OM} sheet Services (19 services, 19 "
                  "schemas)."),
        type="Missing", area="Data / documentation of terms", severity="P3", needed_by_wave=0,
        legacy_ref="None", owner_role="Data architecture team", asm="ASM-B-DATA-17-8",
        proposed="Append five Term rows at rows 22 to 26 and leave the 16 v6 rows unchanged.",
    ),
]

asms = [
    dict(
        text=("All 30 recovery.v_ace_* views are owned by P1 rwb-source-data and keep the read-only recovery schema as their target schema; "
              "no domain service owns a view."),
        why="Only rwb-source-data reads the views and it owns the ACE view contract, so the reader is the owner until the map adds a Views sheet.",
        read=f"{ARCH} slides 15, 41 and the SQL view standard lines 700 and 843; ADR-010; Template and Rules DP-05; {OM} sheet Tables.",
        gap="CG-B-DATA-17-1",
        applied_in="06 Data/Recovery Workbench Conceptual Data Model v7.xlsx (Entities column H and I for the 30 views; Service ownership P1 row)",
        confidence="High",
        confirm="Data architecture team adds a Views sheet to the Ownership Map v2.",
        impact="48 of the 122 entities are P1's; the 30 views are not copied into any rwb_* schema.",
    ),
    dict(
        text=("Payment match rule stays as an entity of the model, owned by P7 rwb-decision, and its ownership basis records that the table is "
              "retired and the rule moved into the PAYMENT_MATCH package."),
        why="D-RCV-36 T10 drops the table and the map therefore has no row for it, but the WP keeps every entity and ID of the source.",
        read=f"{DL} D-RCV-36 T4 and T10; LDM v8 payment_match_rule field descriptions; {OM} sheet Tables.",
        gap="CG-B-DATA-17-2",
        applied_in="06 Data/Recovery Workbench Conceptual Data Model v7.xlsx (Entities row Payment match rule, columns H to J)",
        confidence="Medium",
        confirm="Solution architect confirms the P7 owner at the rule registry design review.",
        impact="One entity has an owner but no target table; P8 matches payments through the P7 package.",
    ),
    dict(
        text="S1 rwb-valuation owns no entity in this version, and its DB story creates the rwb_valuation schema and Flyway baseline only.",
        why="The map gives S1 no table, and the appraisal data is a P1 view and a P1 extension table under the map's own ruling.",
        read=f"{OM} sheet Tables and sheet Rulings (valuation_ext, ASM-A6-tables-15); {ARCH} slide 41.",
        gap="CG-B-DATA-17-3",
        applied_in="06 Data/Recovery Workbench Conceptual Data Model v7.xlsx (Service ownership S1 row and its note)",
        confidence="Medium",
        confirm="S1 design review decides whether rwb_valuation gets a table of its own.",
        impact="One of the 19 services has no entity; the 122 entity count and the 14 data products are unchanged.",
    ),
    dict(
        text="The entity 'Rule' is rule_row, owned by P7; rule_package and rule_package_version are not in this version of the model and are added in the next one.",
        why="The LDM maps 'Rule' to rule_row and its 18 fields match; the model has no row for the two registry tables.",
        read=f"LDM v8 dictionary rows rule_row, rule_package, rule_package_version; {OM} sheet Tables; {DL} D-RCV-36 T4 and T6.",
        gap="CG-B-DATA-17-4",
        applied_in="06 Data/Recovery Workbench Conceptual Data Model v7.xlsx (Entities row Rule, column J; Service ownership P7 note)",
        confidence="High",
        confirm="Solution architect accepts the three additions at the next LDM review.",
        impact="The five P7 entities stay five; the model is silent on the two registry tables until the next version.",
    ),
    dict(
        text=("A cross-service reference keeps the business key and carries no foreign key; the 48 table-to-table cuts and the 11 ACE view "
              "references are marked per row in the Relationships sheet."),
        why="Every service has its own schema and login and never reads another service's schema, so a foreign key across two schemas cannot survive.",
        read=f"{OM} sheet Services and sheet FK cuts (header only); Template and Rules R4 and DP-01; {ARCH} slides 20 and 41.",
        gap="CG-B-DATA-17-5",
        applied_in="06 Data/Recovery Workbench Conceptual Data Model v7.xlsx (Relationships columns F to H)",
        confidence="High",
        confirm="Data architecture team fills the FK cuts sheet of the Ownership Map v2 with the 48 rows.",
        impact="59 of the 104 references cross a service boundary and none of them is enforced by the database.",
    ),
    dict(
        text=("For outbox_event, outbox_delivery, processed_event and idempotency_key the target schema reads 'every service schema (platform "
              "library object)', with owner PLT."),
        why="The map gives schema 'platform' and the same rows say the object is created in every service schema.",
        read=f"{OM} sheet Tables rows outbox_event, outbox_delivery, processed_event, idempotency_key and their ruling (ASM-A6-tables-8); {ARCH} slides 11 and 20; Template and Rules DP-09.",
        gap="CG-B-DATA-17-6",
        applied_in="06 Data/Recovery Workbench Conceptual Data Model v7.xlsx (Entities column I for the four rows)",
        confidence="High",
        confirm="Data architecture team confirms the wording in the Ownership Map v2.",
        impact="Each of the 19 schemas holds its own copy; the model keeps one entity per object.",
    ),
    dict(
        text="Feature flag and Feature flag change keep 'Workbench' in the preserved system-of-record column, take owner PLT and target schema 'platform library', and the platform serves them.",
        why="The map's default ruling moves feature flags to the platform library while the model's column is copied from v6 unchanged.",
        read=f"{OM} sheet Tables and sheet Rulings row feature_flag (ASM-A6-tables-7); {ARCH} slide 20.",
        gap="CG-B-DATA-17-7",
        applied_in="06 Data/Recovery Workbench Conceptual Data Model v7.xlsx (Entities rows Feature flag and Feature flag change, columns H to J)",
        confidence="Medium",
        confirm="Solution architect confirms at the platform library review.",
        impact="Two entities show a system of record that differs from their owner; the preserved text is not edited.",
    ),
    dict(
        text="Five Term rows are appended to the Key sheet for owning service, target schema, PLT, cross-service reference and service contract; the 16 v6 rows are untouched.",
        why="The new columns need defined words, and the Key is where the workbook defines every other word it uses.",
        read="v6 Key sheet rows 2 and 5 to 21; Template and Rules R4 and R5.5; Ownership Map v1 sheet Services.",
        gap="CG-B-DATA-17-8",
        applied_in="06 Data/Recovery Workbench Conceptual Data Model v7.xlsx (Key rows 22 to 26)",
        confidence="High",
        confirm="Data architecture team accepts the five definitions at the next document review.",
        impact="The Key holds 21 rows; no v6 term, row or order changes.",
    ),
]

for i, g in enumerate(gaps, 1):
    g["id"] = f"CG-{WP}-{i}"
    g["source"] = SRC
    g["wp"] = WP
out = [{k: g[k] for k in ["id", "title", "source", "section", "description", "evidence", "type", "area", "severity",
                          "needed_by_wave", "legacy_ref", "owner_role", "asm", "proposed", "wp"]} for g in gaps]
(ROOT / "_work" / "msr" / "gaps" / f"{WP}.jsonl").write_text(
    "\n".join(json.dumps(r, ensure_ascii=False) for r in out) + "\n", encoding="utf-8")

for i, a in enumerate(asms, 1):
    a["id"] = f"ASM-{WP}-{i}"
    a["wp"] = WP
aout = [{k: a[k] for k in ["id", "text", "why", "read", "gap", "applied_in", "confidence", "confirm", "impact", "wp"]} for a in asms]
(ROOT / "_work" / "msr" / "assumptions" / f"{WP}.jsonl").write_text(
    "\n".join(json.dumps(r, ensure_ascii=False) for r in aout) + "\n", encoding="utf-8")
print("wrote", len(out), "gap rows and", len(aout), "assumption rows")

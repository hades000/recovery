"""Write README.md for the v7 schema folder."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "06 Data" / "Recovery Workbench Physical Schema v7"
REP = json.load(open(Path(__file__).resolve().parent / "schema_report.json", encoding="utf-8"))
OM = json.load(open(ROOT / "_work" / "msr" / "plan" / "ownership.json", encoding="utf-8"))
SRC = ROOT / "06 Data" / "Recovery Workbench Physical Schema v6.sql"

SERVICES = [
    ("P1", "rwb-source-data", "Source data", 1, "rwb_source_data"),
    ("P2", "rwb-integration", "Integration", 1, "rwb_integration"),
    ("P3", "rwb-case", "Case and workflow", 1, "rwb_case"),
    ("P4", "rwb-access", "Access and authority", 1, "rwb_access"),
    ("P5", "rwb-document", "Document", 1, "rwb_document"),
    ("P6", "rwb-comms", "Communications", 1, "rwb_comms"),
    ("P7", "rwb-decision", "Decision and rules", 1, "rwb_decision"),
    ("P8", "rwb-payment", "Payment", 2, "rwb_payment"),
    ("P9", "rwb-reporting", "Reporting", 1, "rwb_reporting"),
    ("P10", "rwb-agent", "Agent", 1, "rwb_agent"),
    ("S1", "rwb-valuation", "Valuation and route", 3, "rwb_valuation"),
    ("S2", "rwb-treatment", "Treatment and offer", 2, "rwb_treatment"),
    ("S3", "rwb-guarantee", "Guarantee", 3, "rwb_guarantee"),
    ("S4", "rwb-litigation", "Litigation", 3, "rwb_litigation"),
    ("S5", "rwb-asset", "Asset", 2, "rwb_asset"),
    ("S6", "rwb-debtsale", "Debt sale", 3, "rwb_debtsale"),
    ("S7", "rwb-writeoff", "Write-off", 4, "rwb_writeoff"),
    ("S8", "rwb-deviation", "Deviation", 2, "rwb_deviation"),
    ("S9", "rwb-partner", "Partner", 4, "rwb_partner"),
]
CODE = {c: (svc, name, wave, schema) for c, svc, name, wave, schema in SERVICES}
SCHEMA = {c: s for c, _, _, _, s in SERVICES}
DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"


def main():
    src = SRC.read_text(encoding="utf-8")
    counts = {
        "tables": len(re.findall(r"CREATE TABLE (\w+)", src)),
        "views": len(re.findall(r"CREATE (?:OR REPLACE )?VIEW ", src)),
        "ace": len(re.findall(r"CREATE (?:OR REPLACE )?VIEW recovery\.v_ace_", src)),
        "indexes": len(re.findall(r"CREATE (?:UNIQUE )?INDEX ", src)),
        "ctable": len(re.findall(r"COMMENT ON TABLE ", src)),
        "ccolumn": len(re.findall(r"COMMENT ON COLUMN ", src)),
        "insert": len(re.findall(r"INSERT INTO ", src)),
        "fk": len(re.findall(r"ADD CONSTRAINT \w+ FOREIGN KEY", src)),
    }
    per = {}
    for c, svc, name, wave, schema in SERVICES:
        t = (OUT / f"{schema}.sql").read_text(encoding="utf-8")
        m = re.search(r"Tables in this file: (\d+)\. Owned by this service in the Ownership Map v1: (\d+)", t)
        per[c] = {
            "tables": len(re.findall(r"CREATE TABLE ", t)),
            "owned": int(m.group(2)),
            "in_file": int(m.group(1)),
            "fk": len(re.findall(r"ADD CONSTRAINT \w+ FOREIGN KEY", t)),
            "index": len(re.findall(r"CREATE (?:UNIQUE )?INDEX ", t)),
            "lines": len(t.splitlines()),
        }
    cuts = REP["cuts"]
    total_owned = sum(v["owned"] for v in per.values())

    L = []
    L.append("SCB Collections and Recovery. Henka Group, 22 November 2026.")
    L.append("(C) Siam Commercial Bank and Henka Pte Ltd")
    L.append("")
    L.append("# Recovery Workbench Physical Schema v7")
    L.append("")
    L.append("| Item | Value |")
    L.append("|---|---|")
    L.append("| Version | 7 |")
    L.append("| Date | 22 November 2026 |")
    L.append(f"| Change log | 7, 22 November 2026, {DEC} microservice realignment, {TOOL} |")
    L.append("| Source | `06 Data/Recovery Workbench Physical Schema v6.sql` (read only, 16 November 2026, version 6) |")
    L.append("| Decision | D-RCV-60: adopt Architecture v5 and realign the documents (Physical Schema, LDM and ERD) |")
    L.append("| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |")
    L.append(f"| Tables | {counts['tables']} distinct tables; {sum(v['tables'] for v in per.values())} CREATE TABLE statements across the 19 files (the four library objects repeat in every schema) |")
    L.append(f"| Views | {counts['views']} views: {counts['ace']} read-only ACE views plus the data dictionary view |")
    L.append(f"| Foreign keys | {counts['fk']} in the source; 44 kept inside one owner, 48 cut at an owner boundary (80 statements across the 19 files because the two library keys repeat) |")
    L.append(f"| Indexes | {counts['indexes']} |")
    L.append(f"| Dictionary comments | {counts['ctable']} table comments and {counts['ccolumn']} column comments |")
    L.append(f"| Seed rows | {counts['insert']} INSERT statements |")
    L.append("")
    L.append("## 1. What this folder is")
    L.append("")
    L.append("The Physical Schema v6 was one file in one `recovery` schema. Architecture v5 slides 12, 20, 29 and 41 put one schema and one login per service inside the single ACE database, so this version splits the same DDL into 19 `rwb_<name>.sql` files, one per service in the Ownership Map. Every table, column, constraint, index, comment, seed row and view of v6 is carried over unchanged; the only changes are the schema name, the foreign keys that cross an owner boundary, and the placement of the four platform library objects.")
    L.append("")
    L.append("The source text is never edited. Each file states the source it came from and the change log row.")
    L.append("")
    L.append("## 2. Files")
    L.append("")
    L.append("| File | Code | Service | Wave | Schema | Tables owned | Hosted PLT tables | Library objects | FK kept | Indexes |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for c, svc, name, wave, schema in SERVICES:
        v = per[c]
        hosted = 2 if c == "P2" else 0
        lib = 4
        L.append(f"| `{schema}.sql` | {c} | {svc} | {wave} | `{schema}` | {v['owned']} | {hosted} | {lib} | {v['fk']} | {v['index']} |")
    L.append(f"| `recovery_views.sql` | P1 | rwb-source-data | 1 | `rwb_source_data` and `recovery` | 0 | 0 | 0 | 0 | 0 |")
    L.append("")
    L.append("`recovery_views.sql` holds the data dictionary view in `rwb_source_data` and the 30 ACE views in `recovery`. No table is created there.")
    L.append("")
    L.append("## 3. Source coverage")
    L.append("")
    L.append("| Source object | Count | Where it goes |")
    L.append("|---|---|---|")
    L.append(f"| Tables | {counts['tables']} | the file of the owner in the Ownership Map |")
    L.append(f"| Views | {counts['views']} | `recovery_views.sql` |")
    L.append(f"| Foreign keys | {counts['fk']} | kept when both tables share an owner, otherwise cut to a plain uuid column |")
    L.append(f"| Indexes | {counts['indexes']} | the file of the table owner |")
    L.append(f"| Table and column comments | {counts['ctable']} and {counts['ccolumn']} | the file of the table owner |")
    L.append(f"| Seed INSERT statements | {counts['insert']} | the file of the table owner |")
    L.append("| Schema, search path, pgcrypto | 1 | every file creates its own schema and sets its own search path |")
    L.append("")
    L.append("The four extension tables (`party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext`) have column comments in v6 but no `COMMENT ON TABLE`; that is kept as found (CG-B-ARCH-DB-7).")
    L.append("")
    L.append("## 4. Ownership")
    L.append("")
    L.append("Ownership is taken from `22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx`, sheet Tables, for all 93 tables. The 19 service rows and the wave order are from sheet Services.")
    L.append("")
    L.append("| Code | Service | Wave | Schema | Login | REST base | Topic | Queue |")
    L.append("|---|---|---|---|---|---|---|---|")
    for c, svc, name, wave, schema in SERVICES:
        short = svc[4:]
        L.append(f"| {c} | {svc} | {wave} | `{schema}` | `{schema}` | `/api/recovery/{short}/v1` | `rwb.{short}.events.v1` | `{svc}` |")
    L.append("")
    L.append("Twelve Owning-Map rulings move a table away from the module that declared it in a TSD (ASM-A6-tables-1 to ASM-A6-tables-15). This folder applies the ruling, not the TSD: `interaction` and `efs_ledger_outcome` to P1, `delegation_limit` to P4, `lov_value` to P3, `partner_user` to S9, `retention_rule` and `signature_request` to P5, `rule_package*` and `rule_test_case` to P7, `job_catalog` to P2, `timer` to P3, `valuation_ext` to P1, and the feature flags to the platform library.")
    L.append("")
    L.append("## 5. Cross-service references (FK cuts)")
    L.append("")
    L.append("A foreign key is kept only when both tables have the same owner in the Ownership Map. The 48 keys below cross an owner boundary, so the column stays a plain uuid and integrity is through the owner's API contract (or the shared event). The Ownership Map sheet `FK cuts` was generated empty in v1 (it has the header row only), so the list is derived from sheet Tables (CG-B-ARCH-DB-1; ASM-B-ARCH-DB-1).")
    L.append("")
    L.append("| # | From table | From service | Column | To table | To service | Becomes |")
    L.append("|---|---|---|---|---|---|---|")
    for i, c in enumerate(cuts, 1):
        fs = CODE.get(c["from_owner"], ("platform library",))[0]
        ts = CODE.get(c["to_owner"], ("platform library",))[0]
        L.append(f"| {i} | `{c['from']}` | {fs} ({c['from_owner']}) | `{c['column']}` | `{c['to']}` | {ts} ({c['to_owner']}) | plain uuid; integrity through the {ts or 'platform-library'} contract |")
    L.append("")
    L.append("The cut is written twice in each affected file: a trailing comment on the column and a note block at the end of the file. The constraint name from v6 is recorded there so the original key can be traced.")
    L.append("")
    L.append("Three of the 48 cuts have both tables in the same output file (`outbox_event.case_id` and `outbox_delivery.task_id` in `rwb_case.sql`, `case_document_check.last_event_id` in `rwb_document.sql`). They are still cut, because the library object is identical in all 19 schemas and must not carry conditional foreign keys (ASM-B-ARCH-DB-3).")
    L.append("")
    L.append("## 6. Platform library objects")
    L.append("")
    L.append("The Ownership Map gives six tables to PLT, the platform library. Architecture v5 slide 20 and DP-09 make the outbox, inbox and idempotency objects part of every service schema, and the library is not one of the 19 services.")
    L.append("")
    L.append("| Object | Owner | Emitted in | Reason |")
    L.append("|---|---|---|---|")
    L.append("| `outbox_event` | PLT | all 19 files | RWB-PLT-TE006-CON; DP-09; Ownership Map ruling ASM-A6-tables-8 |")
    L.append("| `outbox_delivery` | PLT | all 19 files | same |")
    L.append("| `processed_event` | PLT | all 19 files | same |")
    L.append("| `idempotency_key` | PLT | all 19 files | same |")
    L.append("| `feature_flag` | PLT | `rwb_integration.sql` only | platform library; rwb-integration serves the admin API (ruling ASM-A6-api-2) |")
    L.append("| `feature_flag_change` | PLT | `rwb_integration.sql` only | same |")
    L.append("")
    L.append("The four per-schema objects carry no foreign key to a business table. Their one shared key, `processed_event.event_id` to `outbox_event.id`, is kept inside each schema. The placement is a realignment decision, not a source value (CG-B-ARCH-DB-3; ASM-B-ARCH-DB-3).")
    L.append("")
    L.append("## 7. Views")
    L.append("")
    L.append("- `rwb_source_data.v_data_dictionary` is the v6 `v_data_dictionary` view, re-qualified to the three P1 tables it reads (`sys_fields`, `sys_objects`, `data_product`).")
    L.append("- The 30 `recovery.v_ace_*` views stay in schema `recovery` and are read only. This follows Architecture v5 slide 29, which keeps `recovery.v_ace_*` SELECT-only for `rwb_source_data`, and DP-05, which allows a service to read ACE only through the rwb-source-data contract or its own ACE views (CG-B-ARCH-DB-4; ASM-B-ARCH-DB-4).")
    L.append("- The three helper functions (`ace_to_date`, `ace_to_boolean`, `ace_mask_value`) stay in schema `recovery` because the views call them.")
    L.append("- The grants block is carried over as a comment for the reason in CG-B-ARCH-DB-5: the source uses `:recovery_role` and `:ace_view_owner` placeholders, and the 19 logins are created by RWB-PLT-NF06, not by this file.")
    L.append("")
    L.append("## 8. Objects with a note")
    L.append("")
    L.append("| Object | Note |")
    L.append("|---|---|")
    L.append("| `lake_copy_watermark` | No target: the data lake is removed (Architecture v5 slide 37; DP-17) and JOB-13 is continuous Kafka ingest (slide 44), so the P1 DB story drops it (ruling ASM-A6-tables-13). The DDL is kept so no source object is lost (CG-B-ARCH-DB-8). |")
    L.append("| `rwb_valuation.sql` | rwb-valuation owns no table. `valuation_ext` stays in rwb_source_data (ruling ASM-A6-tables-15) and route economics come from ACE through the rwb-source-data contract. The file holds the schema, the library objects and a note (CG-B-ARCH-DB-2; ASM-B-ARCH-DB-2). |")
    L.append("| `decision_log_entry`, `interaction` | The append-only trigger `refuse_change()` and its two triggers are kept with the owning service (`rwb_decision.sql`, `rwb_source_data.sql`). |")
    L.append("")
    L.append("## 9. Run order and Flyway")
    L.append("")
    L.append("1. `rwb_<name>.sql` for each service, in wave order: P1 to P10 and S1 to S9 by table above. Each file is self-contained in its own schema.")
    L.append("2. `recovery_views.sql` after `rwb_source_data.sql`, because the dictionary view reads three P1 tables. The ACE views read only `public` tables.")
    L.append("")
    L.append("Per-service Flyway (DP-15, ADR-021): one `V0001` baseline per schema. The source split V0001 tables and dictionary, V0002 Tier 1 views and V0003 Tier 2 views; the per-service sequence is not fixed in the source documents (CG-B-ARCH-DB-6; ASM-B-ARCH-DB-6).")
    L.append("")
    L.append("## 10. Gaps and assumptions")
    L.append("")
    L.append("| ID | Gap | Assumption |")
    L.append("|---|---|---|")
    L.append("| CG-B-ARCH-DB-1 / ASM-B-ARCH-DB-1 | The Ownership Map sheet `FK cuts` has only a header, while 48 cross-owner foreign keys exist in v6. | The cuts are derived from sheet Tables: a difference in owner means a cut. |")
    L.append("| CG-B-ARCH-DB-2 / ASM-B-ARCH-DB-2 | rwb-valuation owns no table in the map. | The service reads ACE through the rwb-source-data contract and keeps no local table until a TSD adds one. |")
    L.append("| CG-B-ARCH-DB-3 / ASM-B-ARCH-DB-3 | The map does not say where the six PLT tables live after the split. | The four outbox, inbox and idempotency objects go in every service schema; the two feature-flag tables go in rwb_integration. |")
    L.append("| CG-B-ARCH-DB-4 / ASM-B-ARCH-DB-4 | The map does not say which schema holds the 30 ACE views. | They stay in schema `recovery`, read only, as Architecture v5 slide 29 describes. |")
    L.append("| CG-B-ARCH-DB-5 / ASM-B-ARCH-DB-5 | The source grants use `:recovery_role` and `:ace_view_owner` placeholders; the 19 logins are not in the SQL. | The grants block stays a commented template; RWB-PLT-NF06 and RWB-PLT-N011 create the 19 logins and privileges. |")
    L.append("| CG-B-ARCH-DB-6 / ASM-B-ARCH-DB-6 | The per-service Flyway sequence is not specified. | One V0001 per schema (DP-15); the view file follows the source V0002 and V0003 sections. |")
    L.append("| CG-B-ARCH-DB-7 / ASM-B-ARCH-DB-7 | The four extension tables have no `COMMENT ON TABLE` in v6. | Kept as found; the column comments still feed the data dictionary. |")
    L.append("| CG-B-ARCH-DB-8 / ASM-B-ARCH-DB-8 | `lake_copy_watermark` has an owner but no target. | The DDL is kept and marked for retirement, so no source object is lost. |")
    L.append("")
    L.append("## 11. Checks")
    L.append("")
    L.append("- Every one of the 93 source tables appears in exactly one service file, except the four library objects, which appear in all 19.")
    L.append("- Every one of the 31 source views appears once in `recovery_views.sql`.")
    L.append("- Every foreign key kept inside a file points to a table created in that file; no file references another service's schema.")
    L.append("- Every index, comment and seed row points to a table created in the same file.")
    L.append("- The two header lines and the D-RCV-60 change-log row are at the top of every file.")
    L.append("")
    path = OUT / "README.md"
    path.write_text("\n".join(L).rstrip() + "\n", encoding="utf-8")
    print("WROTE", path.name, len(L), "lines")


if __name__ == "__main__":
    main()

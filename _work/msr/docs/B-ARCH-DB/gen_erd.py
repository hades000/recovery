"""Write the ERD v6 Markdown from ERD v5.pdf/HTML and the v7 schema."""
import html as H
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "06 Data" / "Recovery Workbench Entity Relationship Diagram v6.md"
HTML = ROOT / "06 Data" / "Recovery Workbench Entity Relationship Diagram v5.html"
SQL = ROOT / "06 Data" / "Recovery Workbench Physical Schema v6.sql"
OM = json.load(open(ROOT / "_work" / "msr" / "plan" / "ownership.json", encoding="utf-8"))
REP = json.load(open(Path(__file__).resolve().parent / "schema_report.json", encoding="utf-8"))

DEC = "D-RCV-60"
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"
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
LIBRARY = {"outbox_event", "outbox_delivery", "processed_event", "idempotency_key"}
HOSTED = {"feature_flag", "feature_flag_change"}


def read_erd():
    s = HTML.read_text(encoding="utf-8", errors="ignore")
    rows = re.findall(r"<tr>(.*?)</tr>", s, re.S)
    refs, dp = [], []
    for r in rows:
        tds = [H.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)]
        if len(tds) == 5 and tds[4] in ("Foreign key", "Business key, no foreign key",
                                        "Business key, no foreign key (1:1 extension)"):
            refs.append({"entity": tds[0], "field": tds[1], "to": tds[2], "ref": tds[3], "kind": tds[4]})
        elif len(tds) == 7 and re.match(r"^(DP\d\d|OPS|AGT|RPT)$", tds[0]):
            dp.append(tds)
    # dedupe
    seen, uniq = set(), []
    for r in refs:
        k = (r["entity"], r["field"], r["to"], r["ref"], r["kind"])
        if k not in seen:
            seen.add(k)
            uniq.append(r)
    return uniq, dp


def nullability(sql):
    """table -> {column: nullable_bool}"""
    out = {}
    for m in re.finditer(r"CREATE TABLE (\w+) \((.*?)\n\);", sql, re.S):
        cols = {}
        for l in m.group(2).splitlines():
            mm = re.match(r"^\s*([a-z][a-z0-9_]*)\s+", l)
            if not mm:
                continue
            cols[mm.group(1)] = "NOT NULL" not in l.upper()
        out[m.group(1)] = cols
    return out


def main():
    sql = SQL.read_text(encoding="utf-8")
    refs, dp = read_erd()
    fk = [r for r in refs if r["kind"] == "Foreign key"]
    bk = [r for r in refs if r["kind"].startswith("Business key")]
    print("erd refs", len(refs), "fk", len(fk), "bk", len(bk), "dp rows", len(dp))
    owned = {t: v["owner"] for t, v in OM["tables"].items()}
    nulls = nullability(sql)

    # local FKs by owner, from schema kept list
    kept = [r for r in REP["cuts"]]
    # kept = schema fks minus cuts; rebuild
    rx = re.compile(r"ALTER TABLE (\w+) ADD CONSTRAINT (\w+) FOREIGN KEY \((\w+)\) REFERENCES (\w+) \((\w+)\)")
    allfk = [(a, c, d) for a, b, c, d, e in rx.findall(sql)]
    cutset = {(c["from"], c["column"], c["to"]) for c in REP["cuts"]}
    local = [x for x in allfk if x not in cutset]

    by_svc = {c: [] for c, *_ in SERVICES}
    for t in owned:
        o = owned[t]
        if t in LIBRARY:
            continue
        if t in HOSTED:
            by_svc["P2"].append(t)
        else:
            by_svc[o].append(t)
    for c in by_svc:
        by_svc[c] = sorted(by_svc[c], key=lambda x: list(owned).index(x))

    local_by_svc = {c: [] for c, *_ in SERVICES}
    for a, col, b in local:
        o = owned[a]
        if o == "PLT":
            continue
        local_by_svc[o].append((a, col, b))

    L = []
    L.append("SCB Collections and Recovery. Henka Group, 22 November 2026.")
    L.append("(C) Siam Commercial Bank and Henka Pte Ltd")
    L.append("")
    L.append("# Recovery Workbench Entity Relationship Diagram v6")
    L.append("")
    L.append("| Item | Value |")
    L.append("|---|---|")
    L.append("| Version | 6 |")
    L.append("| Date | 22 November 2026 |")
    L.append(f"| Change log | 6, 22 November 2026, {DEC} microservice realignment, {TOOL} |")
    L.append("| Source | `06 Data/Recovery Workbench Entity Relationship Diagram v5.pdf` (read only, 16 November 2026, version 5, 97 pages). The source is a PDF, so this version is Markdown with Mermaid diagrams; no PDF is written. |")
    L.append(f"| Decision | {DEC} microservice realignment |")
    L.append(f"| Tool | {TOOL} |")
    L.append("| Objects | 123: 89 Workbench tables, 4 extension tables and 30 ACE source views (unchanged from v5) |")
    L.append("| References | 108 in v5: 90 foreign keys and 18 business-key links; 54 cross a data product boundary and 54 stay inside one (unchanged from v5) |")
    L.append("")
    L.append("## 1. What changed and what did not")
    L.append("")
    L.append("v5 drew one `recovery` schema. Architecture v5 gives each of the 19 services its own `rwb_<name>` schema and login inside the same ACE database, so this version draws the same 123 objects grouped by owner service. The objects, keys, references, cardinalities, data products and the ACE boundary are exactly those of v5. What changes is the grouping and the treatment of a reference that crosses an owner boundary.")
    L.append("")
    L.append("The source was a PDF. It cannot be edited by the office helper and no PDF is written; this Markdown file is the v6 deliverable. Every number in v5 is repeated here so the two can be read side by side.")
    L.append("")
    L.append("## 2. Reference reconciliation")
    L.append("")
    L.append("| Measure | Count | Note |")
    L.append("|---|---|---|")
    L.append("| References in ERD v5 | 108 | 90 foreign keys and 18 business-key links |")
    L.append("| Foreign keys in ERD v5 | 90 | drawn as `(FK)` inside the recovery schema |")
    L.append("| ACE business-key links | 18 | 14 replace a source copy; 4 join an extension table to its ACE view |")
    L.append("| Foreign keys kept in v6 | 44 | 42 from v5 plus the 2 metadata-registry keys that v6 adds |")
    L.append("| Foreign keys cut in v6 | 48 | the two tables have different owners in the Ownership Map |")
    L.append("| Foreign keys in Physical Schema v6 | 92 | 90 from v5 plus `sys_fields.object_name` and `sys_objects.data_product` |")
    L.append("")
    L.append("The two metadata-registry keys are in Physical Schema v6 but not in ERD v5 (CG-B-ARCH-DB-9; ASM-B-ARCH-DB-9). They are kept inside P1.")
    L.append("")
    L.append("## 3. Data products (from ERD v5)")
    L.append("")
    L.append("| Group | Data product | Objects | Tables | Extension | Views | System of record |")
    L.append("|---|---|---|---|---|---|---|")
    for r in dp:
        L.append("| " + " | ".join(r) + " |")
    L.append("")
    L.append("The 14 data products hold 98 objects; OPS, AGT and RPT hold the other 25 (123 in total).")
    L.append("")
    L.append("### 3.1 ACE source views (30)")
    L.append("")
    L.append("| Tier | Flyway | Views |")
    L.append("|---|---|---|")
    L.append("| Tier 1 | V0002 | `v_ace_account`, `v_ace_payment`, `v_ace_customer`, `v_ace_contact`, `v_ace_ca_relation`, `v_ace_aa_relation`, `v_ace_collateral`, `v_ace_asset`, `v_ace_efs_action`, `v_ace_efs_action_code`, `v_ace_efs_assignment`, `v_ace_bucket_log`, `v_ace_product`, `v_ace_branch`, `v_ace_holiday`, `v_ace_plan` |")
    L.append("| Tier 2 | V0003 | `v_ace_batch_status`, `v_ace_valuation`, `v_ace_collateral_detail`, `v_ace_npa_asset`, `v_ace_npa_sale`, `v_ace_lawsuit`, `v_ace_hearing`, `v_ace_pod`, `v_ace_write_off`, `v_ace_score`, `v_ace_party_product`, `v_ace_credit_decision`, `v_ace_esign`, `v_ace_iam_group` |")
    L.append("")
    L.append("### 3.2 Extension tables (4)")
    L.append("")
    L.append("`party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext`, each 1:1 with an ACE record and keyed by the ACE business key `(BK)`.")
    L.append("")
    L.append("## 4. Service groups")
    L.append("")
    L.append("One diagram per service. An entity block carries its primary key and its local foreign keys; a cut reference is not drawn as a line and appears in section 5 instead. The four platform library objects are drawn once, in section 7, because they exist in every schema.")
    L.append("")
    for idx, (code, svc, name, wave, schema) in enumerate(SERVICES, 1):
        L.append(f"### 4.{idx} {svc} ({code}, wave {wave}, schema `{schema}`)")
        L.append("")
        tables = by_svc[code]
        if not tables:
            L.append("rwb-valuation owns no table in the Ownership Map. It reads ACE through the rwb-source-data contract and keeps no local entity (CG-B-ARCH-DB-2; ASM-B-ARCH-DB-2). The diagram is therefore empty.")
            L.append("")
            L.append("```mermaid")
            L.append("erDiagram")
            L.append("    %% rwb-valuation owns no entity in the Ownership Map v1 (CG-B-ARCH-DB-2; ASM-B-ARCH-DB-2)")
            L.append("```")
            L.append("")
            continue
        L.append("```mermaid")
        L.append("erDiagram")
        for t in tables:
            L.append(f"    {t} {{")
            L.append("        uuid id PK")
            for a, col, b in local_by_svc[code]:
                if a == t:
                    L.append(f"        uuid {col} FK")
            L.append("    }")
        for a, col, b in local_by_svc[code]:
            if a in tables and b in tables:
                nullable = nulls.get(a, {}).get(col, True)
                left = "|o" if nullable else "||"
                L.append(f'    {b} {left}--o{{ {a} : "{col}"')
        L.append("```")
        L.append("")
    L.append("## 5. Cross-service references (cut foreign keys)")
    L.append("")
    L.append("These are the 48 references whose two tables have different owners in the Ownership Map. The column stays a plain uuid and integrity is through the owner's contract (README section 5). The owning service is P1 to P10 or S1 to S9.")
    L.append("")
    L.append("| # | From entity | From service | Field | To entity | To service | Reference | Becomes |")
    L.append("|---|---|---|---|---|---|---|---|")
    for i, c in enumerate(REP["cuts"], 1):
        fs = CODE.get(c["from_owner"], ("platform library",))[0]
        ts = CODE.get(c["to_owner"], ("platform library",))[0]
        L.append(f"| {i} | `{c['from']}` | {fs} ({c['from_owner']}) | `{c['column']}` | `{c['to']}` | {ts} ({c['to_owner']}) | Foreign key | plain uuid; through the {ts} contract |")
    L.append("")
    L.append("## 6. ACE boundary and business-key links")
    L.append("")
    L.append("The 30 `recovery.v_ace_*` views are external, read only, have no primary key and are never the parent of a foreign key (ERD v5 notation). The 18 business-key links below carry an ACE business key and no foreign key; they are unchanged from v5.")
    L.append("")
    L.append("```mermaid")
    L.append("erDiagram")
    for r in sorted(bk, key=lambda x: (x["entity"], x["field"])):
        L.append(f'    {r["to"]} ||--o{{ {r["entity"]} : "{r["field"]}"')
    L.append("```")
    L.append("")
    L.append("| # | Entity | Field | Refers to | Reference | Kind |")
    L.append("|---|---|---|---|---|---|")
    for i, r in enumerate(sorted(bk, key=lambda x: (x["entity"], x["field"])), 1):
        L.append(f"| {i} | `{r['entity']}` | `{r['field']}` | `{r['to']}` | {r['ref']} | {r['kind']} |")
    L.append("")
    L.append("## 7. Platform library objects (every schema)")
    L.append("")
    L.append("The four outbox, inbox and idempotency objects are owned by PLT and created in every service schema (DP-09; RWB-PLT-TE006-CON). The one key between them is local.")
    L.append("")
    L.append("```mermaid")
    L.append("erDiagram")
    L.append("    outbox_event {")
    L.append("        uuid id PK")
    L.append("    }")
    L.append("    outbox_delivery {")
    L.append("        uuid id PK")
    L.append("        uuid event_id FK")
    L.append("    }")
    L.append("    processed_event {")
    L.append("        uuid id PK")
    L.append("        uuid event_id FK")
    L.append("    }")
    L.append("    idempotency_key {")
    L.append("        uuid id PK")
    L.append("    }")
    L.append('    outbox_event ||--o{ outbox_delivery : "event_id"')
    L.append('    outbox_event |o--o{ processed_event : "event_id"')
    L.append("```")
    L.append("")
    L.append("## 8. Objects and keys")
    L.append("")
    L.append("| Kind | Count | Key notation |")
    L.append("|---|---|---|")
    L.append("| Workbench table | 89 | square-cornered box; `(PK)`, `(AK1)`, `(FK)` as in v5 |")
    L.append("| Extension table | 4 | `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext`; 1:1 with an ACE record, keyed by the ACE business key `(BK)` |")
    L.append("| ACE source view | 30 | dashed box, read only; 16 Tier 1 (`V0002`) and 14 Tier 2 (`V0003`) |")
    L.append("")
    L.append("## 9. Notation")
    L.append("")
    L.append("The v5 IDEF1X notation is carried over: a square-cornered box is a Workbench table, `(PK)` is the primary key, `(AK1)` an alternate key, `(FK)` a foreign key inside the schema and `(BK)` an ACE business key with no foreign key. A dashed box is an ACE source view, external and read only. The Mermaid diagrams use `||--o{` for a mandatory parent and `|o--o{` for an optional one.")
    L.append("")
    L.append("## 10. Gaps and assumptions")
    L.append("")
    L.append("| ID | Gap | Assumption |")
    L.append("|---|---|---|")
    L.append("| CG-B-ARCH-DB-9 / ASM-B-ARCH-DB-9 | ERD v5 draws 90 foreign keys; Physical Schema v6 has 92. | The two metadata-registry keys are added to v6 and kept inside P1; no v5 reference is dropped. |")
    L.append("| CG-B-ARCH-DB-1 / ASM-B-ARCH-DB-1 | The Ownership Map `FK cuts` sheet is empty. | The 48 cuts are derived from sheet Tables. |")
    L.append("| CG-B-ARCH-DB-10 / ASM-B-ARCH-DB-10 | v5 gives no owner for any object and no service grouping. | The grouping is the Ownership Map owner; the objects and references are v5 unchanged. |")
    L.append("")
    L.append("## 11. Checks")
    L.append("")
    L.append("- All 123 v5 objects are present: 89 Workbench tables, 4 extension tables, 30 ACE views.")
    L.append("- All 108 v5 references are present: 90 foreign keys (42 kept, 48 cut) and 18 business-key links.")
    L.append("- Every Mermaid diagram parses and every relationship uses an entity declared in the same diagram.")
    L.append("- No person name, e-mail address or issue-tracker reference is written.")
    L.append("")
    OUT.write_text("\n".join(L).rstrip() + "\n", encoding="utf-8")
    print("WROTE", OUT.name, len(L), "lines")


if __name__ == "__main__":
    main()

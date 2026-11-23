"""Write the B-DATA-18 build note from the finished v5 workbook."""
import collections

import openpyxl

V5 = "06 Data/Recovery Workbench Source to Target Mapping v5.xlsx"
OUT = "_work/msr/docs/B-DATA-18/build_notes.md"

wb = openpyxl.load_workbook(V5)
m = wb["Mapping"]
rows = collections.Counter()
schema = {}
for r in range(2, m.max_row + 1):
    ent = m.cell(row=r, column=3).value
    rows[ent] += 1
    schema[ent] = (m.cell(row=r, column=15).value, m.cell(row=r, column=16).value)

ACE_ENTITIES = {
    "party", "contact_point", "loan_account", "account_payment", "collateral",
    "account_collateral", "valuation", "asset", "score", "collections_history",
    "party_product",
}

lines = []
A = lines.append
A("SCB Collections and Recovery. Henka Group, 22 November 2026.")
A("(C) Siam Commercial Bank and Henka Pte Ltd")
A("")
A("# Build note B-DATA-18 - Recovery Workbench Source to Target Mapping v5")
A("")
A("Decision D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.")
A("")
A("## Source and output")
A("")
A("- Source (read only, never edited): `06 Data/Recovery Workbench Source to Target Mapping v4.xlsx`, 4 sheets.")
A("- Output: `06 Data/Recovery Workbench Source to Target Mapping v5.xlsx`, 5 sheets (Read me added first).")
A("- The copy was made with `compat/office_write.py copy`; only the copy was changed.")
A("")
A("## What the realignment changed")
A("")
A("1. `Mapping`: two columns appended at the end, `Target schema` (rwb_<name>) and `Owning service` (P1 to S7), one value per row from the Ownership Map sheet Tables. Columns A to N are untouched.")
A("2. `ACE gaps`: the same two columns appended at the end. All 80 rows read through rwb-source-data, so the target schema is rwb_source_data and the owner is P1 (ADR-010, DP-05).")
A("3. `By source`: one cell changed, the ACE table(s) cell of the Aric via COLLINS row, from `recovery` to `rwb_source_data.party_ext`; counts and the Total row are unchanged.")
A("4. `Mapping rules`: eight rules appended after the ten v4 rules, which are unchanged word for word.")
A("5. `Read me`: new first sheet with the Template and Rules section R8.1 header lines and the change-log row `v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`.")
A("")
A("## Every section, ID, number and date is kept")
A("")
A("- The source carries no date anywhere in the four sheets, so no release date is marked (tentative) and none is changed.")
A("- All 133 Field IDs, the 80 ACE gap row Field IDs, the 17 source-system names and the Total row are copied unchanged.")
A("- `verify_v5.py` compares every v4 cell with v5: exactly one v4 cell differs, the Aric via COLLINS ACE table(s) cell named in CG-B-DATA-18-3.")
A("")
A("## Target schema and owner per entity")
A("")
A("| Workbench entity | Fields | Target schema | Owner | Basis |")
A("|---|---|---|---|---|")
for ent, n in sorted(rows.items(), key=lambda kv: (-kv[1], kv[0])):
    s, o = schema[ent]
    basis = "ACE entity read through rwb-source-data (ADR-010)" if ent in ACE_ENTITIES else "Ownership Map sheet Tables"
    A(f"| {ent} | {n} | {s} | {o} | {basis} |")
A("")
A(f"Total: {sum(rows.values())} field rows over {len(rows)} entities; "
  f"{sum(n for e, n in rows.items() if e in ACE_ENTITIES)} rows are ACE-side entities that read through rwb_source_data, "
  "and 4 further rows (interaction, dp_treatment) are P1 Workbench tables, so rwb_source_data holds 85 rows in all.")
A("")
A("## Counts")
A("")
A("- Mapping: 133 field rows, 25 entities, 17 source systems, target schemas rwb_source_data (85), rwb_litigation (12), rwb_asset (7), rwb_case (6), rwb_treatment (6), rwb_comms (5), rwb_writeoff (5), rwb_payment (3), rwb_access (1), rwb_debtsale (1), rwb_decision (1), rwb_document (1).")
A("- ACE gaps: 80 rows. All read through rwb-source-data.")
A("- By source: 17 source rows plus the Total row; 133 fields, 52 ACE reuse, 80 ACE new, 1 extension.")
A("- Mapping rules: 10 v4 rules plus 8 new rules.")
A("")
A("## Register rows raised by this WP")
A("")
A("| Row | Type or confidence | Subject |")
A("|---|---|---|")
A("| CG-B-DATA-18-1 | Ambiguous, P2 | eleven ACE entities named as Workbench entities (ASM-B-DATA-18-1) |")
A("| CG-B-DATA-18-2 | Missing, P2 | no owner and no target schema in v4 (ASM-B-DATA-18-2) |")
A("| CG-B-DATA-18-3 | Outdated, P3 | extension field counted against ACE table 'recovery' (ASM-B-DATA-18-3) |")
A("| CG-B-DATA-18-4 | Outdated, P3 | five rows cite Interface Specifications v3 (ASM-B-DATA-18-4) |")
A("| CG-B-DATA-18-5 | Ambiguous, P3 | 80 Status cells carry the legacy key RWB-ACE-001 (ASM-B-DATA-18-5) |")
A("| CG-B-DATA-18-6 | Missing, P3 | three extension tables absent from the mapping (ASM-B-DATA-18-6) |")
A("| CG-B-DATA-18-7 | Missing, P3 | 81 field rows without a data product (ASM-B-DATA-18-7) |")
A("")
A("Numbering to GAP-nnnn and ASM-nnnn is left to step D1, as rule 7 and Template and Rules section R9 require.")
A("")
A("## Checks")
A("")
A("`python -I \"22 Microservice Realignment/checks/run_all.py\" --wp B-DATA-18 --quick` - C02, C03, C05, C12, C13 and C18.")
A("")
A("## Scratch files")
A("")
A("- `dump_v4.py`, `v4_dump.json`: the v4 workbook read out cell by cell.")
A("- `build_v5.py`: the v5 builder.")
A("- `verify_v5.py`: the v4-to-v5 cell comparison.")
A("- `gen_notes.py`: this note.")
A("- `probe_entities.py`, `probe2.py`, `probe3.py`, `probe4.py`, `probe_ownmap.py`, `probe_svc.py`, `probe_props.py`: source probes.")
A("- `check_cites.py`, `show_v5.py`, `show_v5b.py`: citation check and read-back of the finished workbook.")

open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print("wrote", OUT, len(lines), "lines")

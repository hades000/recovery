# Edit log - WP B-DELIVDOC-49 (Recovery Workbench Resource Plan and Team Structure next version)

Work package: WP B-DELIVDOC-49. Decision: D-RCV-60 microservice realignment. Agent: aisdlc-msr-worker. Fanout: 0, so no subagent was started.
Tool line: T3 Code / OpenCode / DeepSeek v4.1 Flash. Date: 22 November 2026.

## Files written

- `11 Delivery and operations/Recovery Workbench Resource Plan and Team Structure v3.xlsx` - the next version of the workbook, 8 sheets
- `_work/msr/gaps/B-DELIVDOC-49.jsonl` - 11 gap rows, `GAP-0319` to `GAP-0329`
- `_work/msr/assumptions/B-DELIVDOC-49.jsonl` - 11 assumption rows, `ASM-0411` to `ASM-0421`
- `_work/msr/editlog/B-DELIVDOC-49.md` - this file

Scratch only, under `_work/msr/docs/B-DELIVDOC-49/`:

- `rows_readme.py`, `rows_sheets.py` - build the row JSON of the four new sheets
- `rows_readme.json`, `rows_ownership.json`, `rows_services.json`, `rows_teams.json` - the row JSON passed to `compat/office_write.py xlsx-append`
- `finalize.py` - sheet order, column widths, core properties and the verification scan
- `write_jsonl.py` - writes the two registers
- `v3_dump.txt`, `v3_text.txt` - the new workbook read back, cell by cell, for review

The converted source text sits in the extract folder the WP names, `_work/msr/extract/B-DELIVDOC-49/`, and was written by `compat/convert_sources.py` for both the version 2 workbook and the Ownership Map v1.

No file that already existed was edited. The version 2 workbook and the Ownership Map v1 are unchanged.

## What was done

1. **Copy, then append.** `compat/office_write.py copy` made the version 3 file from `Recovery Workbench Resource Plan and Team Structure v2.xlsx`; `xlsx-append` then added the four new sheets from the row JSON. The four source sheets were never touched: a cell-by-cell comparison of `Team`, `People by month`, `Structure` and `Accountability` between v2 and v3 reports 0 differences, so the 24 team rows, the 20 people-by-month rows with the `=SUM(D5:D24)` to `=SUM(K5:K24)` Total row, the 6 structure rows, the 11 accountability rows, every From and To date (Sep 2026, Nov 2026, Feb 2027, Mar 2027, Jun 2027) and every ID (DL02, DL09, DL30, DL36) are kept as they stand.

2. **Header and change log.** The new `Read me` sheet is first and its cells A1 and A2 are the two header lines of Template and Rules §R8.1. Below them: the title, the tool line, the status (Version 3, 22 November 2026, Draft with its CG and ASM pair), the change log with the version 2 source row and the version 3 row, and the literal change-log line `v3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`. Then what version 3 changes and a sheet index.

3. **Suggested ownership by team type** (new sheet `Ownership by team type`). The six work types CON, APP, DB, INF, OPS and ITG with their fixed owner phrases copied character for character from Template and Rules §R5.3, including the ITG phrase's QA sentence. Each row adds what the owner holds in the 19-service shape and its Day-1 position under §R5.7 rules 1, 2, 6 and 7. A second block gives artefact ownership from the Ownership Map v1: parameters and reference data E1-042 and E1-043 to P3 rwb-case, the case list API to P3, the rule package registry and rule rows to P7 rwb-decision, rule evaluation in the owning service (DP-04), the interaction ledger to P1 rwb-source-data, feature flags to the platform library, outbox, inbox and idempotency to the PLT library, DoA limits to P4 rwb-access, ACE data and the 30 `recovery.v_ace_*` views to P1 only, the Temporal cluster, namespace and workflow kit to the platform team (Temporal and Drools Design slide 23), and one schema and login per service to the ACE team.

4. **Services and squads** (new sheet). The 19 services with the wave and the service name from the Ownership Map v1 Services sheet, the source module and the squad from the version 2 Structure sheet, the owner by work type, and the volume from the plan: 1,034 story slices for 358 legacy stories, 939 Day 1. The fourteen module names of the source are read as thirteen services (rwb-decision takes two of them), and the six services with no module (P2, P8, P9, P10, S3, S9) carry the §R9 placeholder. The sheet states the reading: the decision center and log is squad 2, the rules component is the embedded Drools kit that squad 1 builds. The Total row reproduces the plan totals.

5. **Team types and resources** (new sheet). The five team types of §R5.3 against the full-time equivalents the plan records: TechX 12 (two squads of 6), ACE team 1, QA 2 inside the 12 TechX and not counted twice, SCB IT infrastructure at the placeholder, DevOps team at 0, the 9.5 program roles and the 7 data, business and reference-data roles that belong to no team type of §R5.3, and the 29.5 of the Total row. A second block lists what the plan does not staff: wave 0, the six unmapped services, the squad split, the shared Epic 2 items of DL30, the QA capacity, the DL36 squad-shape basis and the missing approval.

6. **No names, no invented values.** The core properties of version 2 held a person name in `creator` and `lastModifiedBy`; the version 3 file sets both to the organisation and the tool line, and title, subject, description, category and revision 3. A scan of every cell finds no person name and no e-mail address. Every missing value is the §R9 placeholder with its CG and ASM pair; the workbook cites 22 ids, all 22 rows exist, and every row is cited at least once. No release date is invented, changed or raised as a gap; the only dates are the source From and To dates and 22 November 2026 of this run.

7. **Sheet order** of version 3: `Read me`, `Team`, `People by month`, `Structure`, `Accountability`, `Ownership by team type`, `Services and squads`, `Team types and resources`.

## Counts

- Gap rows: 11 (`GAP-0319` to `GAP-0329`). Severity: P1 1, P2 4, P3 6. Type: Missing 8, Ambiguous 2, Outdated 1. Area: delivery 7, documentation 3, governance 1.
- Assumption rows: 11 (`ASM-0411` to `ASM-0421`). Confidence: High 6, Medium 5, Low 0.
- Each gap is paired with one assumption and the pairing is one to one in both directions.
- New decision IDs: none beyond D-RCV-60; the workbook cites the existing DL02, DL09, DL30, DL36, DL46 and DL48, ADR-010 and ADR-013, and no new ADR or DL id.
- Rows numbered GAP-nnnn and ASM-nnnn: none; step D1 numbers them.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-DELIVDOC-49 --quick` at the end of the work package: C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS, no findings. The report is under `22 Microservice Realignment/checks/reports/`.

Checked by hand as well, because the quick checks read `.md`, `.json`, `.yaml` and `.sql` and not the workbook:

- the four source sheets compare equal cell by cell (0 differences), including the Total row formulas;
- the first two cells of the workbook are the §R8.1 header lines and the change-log row is present word for word;
- 22 citations, 22 register rows, no citation without a row and no row without a citation;
- no person name, no e-mail address and no issue-tracker reference anywhere in the workbook or in the scratch files;
- the core properties name the organisation and the tool, not a person.

## Failures

None. Nothing was retried three times.

## Not done, by rule

- No approval was sought and none is recorded; the plan is issued as Draft.
- No master file or register was written, no gap or assumption was numbered, no other document was edited.
- No issue tracker, wiki, repository or web call was made, and no commit was created.

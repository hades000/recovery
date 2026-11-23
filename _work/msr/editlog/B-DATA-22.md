# Edit log B-DATA-22 — Party and Customer Master Data Design next version

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Agent aisdlc-msr-worker, fanout 0.

## What was done

- The source `06 Data/Recovery Workbench Party and Customer Master Data Design v3.xlsx` was read once, cell by cell, and never edited. It was copied to v4 with `compat/office_write.py copy`, and only the copy was changed: `06 Data/Recovery Workbench Party and Customer Master Data Design v4.xlsx`.
- `Read me` is a new first sheet. Rows 1 and 2 are the two header lines of Template and Rules §R8.1. Row 9 is the change-log row `v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`. Rows 12 to 16 say what changed, rows 18 to 20 what did not, rows 22 to 25 the counts, rows 27 to 29 the ownership basis and row 32 the open register rows.
- `Party fields`: three columns were appended at the end, `Owning service` (`P1`, `P3` or `S9`), `Target schema` (`rwb_source_data`, `rwb_case`, `rwb_partner`, or `recovery (read-only)` for a view) and `Access rule` (who may read the table and which contract serves it). Columns A to G keep their letters, positions, values and styles; all 52 field rows are unchanged.
- The owner of every entity comes from the Ownership Map v1 sheet `Tables`, row by row, per the WP instruction "Use the Ownership Map for every owner": `case_party` P3, `party_ext` P1, `contact_point_ext` P1, `partner` S9. The three `recovery.v_ace_*` views are not table rows in the map; they are P1 because only rwb-source-data holds SELECT on the 30 views and owns the view contract (Architecture v5 slides 35, 37, 41 and 45; DP-05).
- `Match rules`: two columns were appended, `Target component` and `Owning service`. M1 to M4 resolve to ACE ingestion and the rwb-source-data view contract (P1); M5 resolves to the rwb-partner partner master (S9). Rules M1 to M5 and both narrative rows are unchanged, word for word.
- `Service ownership`: a new sheet, one row per owning service (P1 39 fields, P3 6, S9 7) plus a Total row of 52, with schema, epic, wave, contract entry point and a note.
- `Read paths`: a new sheet, 10 rows. It states the realignment rule in one place: ACE party data is read only through rwb-source-data, `case_party` only through rwb-case, and the partner panel entry only through rwb-partner. No other service reads these tables or the 30 views (DP-01, DP-05).
- Nothing else moved. `verify_v4.py` compares both v3 sheets with v4 cell by cell, value and style: 0 differences outside the appended cells and no row, column or sheet lost. The sheet order is `Read me`, `Party fields`, `Match rules`, `Service ownership`, `Read paths`.
- The workbook carries no release date at all (0 date cells, 0 date-like strings), so no date is changed and no date needs "(tentative)". No date is raised as a gap.
- The document properties of the copy carry a person's name in `creator` from the source file. It is replaced with `Recovery Workbench programme` and `lastModifiedBy` with the tool line, so no person name survives in the workbook (root rule 4). No content cell was touched for this.
- No person name, no e-mail address and no issue-tracker reference was written. No repository, wiki or web call was made; no commit was created.

## Files written

- `06 Data/Recovery Workbench Party and Customer Master Data Design v4.xlsx`
- `_work/msr/gaps/B-DATA-22.jsonl`
- `_work/msr/assumptions/B-DATA-22.jsonl`
- `_work/msr/editlog/B-DATA-22.md`
- `_work/msr/docs/B-DATA-22/read_me_rows.json`
- `_work/msr/docs/B-DATA-22/service_owner_rows.json`
- `_work/msr/docs/B-DATA-22/read_paths_rows.json`
- `_work/msr/docs/B-DATA-22/build_v4.py`
- `_work/msr/docs/B-DATA-22/verify_v4.py`
- `_work/msr/docs/B-DATA-22/gen_rows.py`

The converted source text is `_work/msr/extract/B-DATA-22/Recovery Workbench Party and Customer Master Data Design v3.md`.

## Rows

- Candidate gap rows: 7, `GAP-0244` to `GAP-0250`, in the gaps file, with every key of Template and Rules §R9. Severity: 2 at P2 (GAP-0244 and GAP-0245) and 5 at P3. Types: 3 Missing (GAP-0244 to GAP-0246), 3 Ambiguous (GAP-0248 to GAP-0250) and 1 Outdated (GAP-0247).
- Candidate assumption rows: 7, `ASM-0334` to `ASM-0340`, in the assumptions file, one per gap, each with `gap` pointing at its CG row. Confidence High on 4 and Medium on 3.
- Numbering to `GAP-nnnn` and `ASM-nnnn` is left to step D1, as root rule 7 and Template and Rules §R9 require.

## Counts

- Party fields: 52 rows over 7 entities: case_party 6, v_ace_customer 13, party_ext 5, v_ace_contact 9, v_ace_ca_relation 5, contact_point_ext 7, partner 7.
- Owned per service: P1 39, P3 6, S9 7; total 52. No row is left without an owner, a schema and an access rule.
- Match rules: 5 rules; M1 to M4 P1, M5 S9. Service ownership: 3 service rows and 1 Total row. Read paths: 10 rows over 9 consumer roles.
- Gaps: 7 rows; assumptions: 7 rows.

## Checks run

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-DATA-22 --quick`: C02, C03, C05, C12, C13 and C18 PASS, 0 findings.
- `verify_v4.py`: 0 problems. Both header lines and the change-log row are present; all 52 rows carry owner, schema and access rule; the entity counts and the 52-field total match; the creator name is scrubbed.
- C17 by hand over the same write set: every candidate gap and assumption row cited in this log, in the Read me sheet and in the two new sheets has a row in its register file, and no other candidate id is cited.

## Failures

None.

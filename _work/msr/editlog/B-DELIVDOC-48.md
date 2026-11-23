# Edit log B-DELIVDOC-48 - Recovery Workbench Risks Assumptions Issues and Dependencies v5

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 (microservice realignment)
Agent: aisdlc-msr-worker. Fanout: 0 (no subagents).

## Files written

- `11 Delivery and operations/Recovery Workbench Risks Assumptions Issues and Dependencies v5.xlsx`
- `_work/msr/gaps/B-DELIVDOC-48.jsonl`
- `_work/msr/assumptions/B-DELIVDOC-48.jsonl`
- `_work/msr/docs/B-DELIVDOC-48/rows_readme.json`
- `_work/msr/docs/B-DELIVDOC-48/rows_risks.json`
- `_work/msr/docs/B-DELIVDOC-48/rows_assumptions.json`
- `_work/msr/docs/B-DELIVDOC-48/fix_book.py`
- `_work/msr/docs/B-DELIVDOC-48/fix_text.py`
- `_work/msr/docs/B-DELIVDOC-48/peek.py`
- `_work/msr/docs/B-DELIVDOC-48/check/Recovery Workbench Risks Assumptions Issues and Dependencies v5.md`
- `_work/msr/editlog/B-DELIVDOC-48.md`

Scratch only: the extract at `_work/msr/extract/B-DELIVDOC-48/` (source workbook and Ownership Map converted with compat/convert_sources.py) and the read-back conversion used to verify the output. The source v4 workbook was copied, never edited.

## What the new version does

| Item | Change |
|---|---|
| Read me sheet | New first sheet: the two header lines of Template and Rules R8.1, the title, the change-log row, five realignment notes, the tool line |
| Change-log row | `v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash` |
| Risks sheet | All 18 source risks kept with ID, text, impact, likelihood, action and review date unchanged; cover row restated for 27 risks at v5; nine realignment risks R1-R9 added as R-19 to R-27 |
| Risk owners | Source role kept; Ownership Map v1 service code and name added in brackets where the map assigns the item (14 of 18 rows; R-09, R-10, R-17 have no service owner) |
| Assumptions sheet | A-01 to A-10 kept unchanged; pointer row A-11 to the Assumptions Register v1 (folder 23); cover row restated |
| Issues sheet | I-01 to I-03 copied unchanged (the realignment adds no issue) |
| Dependencies sheet | DEP-01 to DEP-36 kept with needed-by dates unchanged; cover row restated for v5; owner cells realigned to the map where a service owns the item (21 of 36 rows) |

The nine realignment risks: R-19 service and on-call load of 19 deployables; R-20 Kafka not ready (outbox holds events); R-21 19 schemas and logins in the ACE database; R-22 shared Temporal layer and the 1.30+ upgrade; R-23 XLS to DMN 1.6 rule conversion and package governance; R-24 contract-first calls, one hop and 2 s timeout; R-25 ledger model not yet accepted by Audit; R-26 the 8-month programme with nine services in Wave 1; R-27 no data lake, reporting from events.

No release date appears in the source or the output; the review-by and needed-by dates are copied character for character. No person name, no issue-tracker reference, no external call.

## Gap and assumption rows

| Register | Rows | IDs |
|---|---|---|
| Gaps (CG) | 3 | GAP-0316 (review date of the nine new risks, Missing, P3), GAP-0317 (R1-R9 numbering against R-01 to R-18, ID collision, P3), GAP-0318 (owner vocabulary, Ambiguous, P3) |
| Assumptions (ASM) | 3 | ASM-0408, ASM-0409, ASM-0410 |

Counts: 3 CG rows, 3 ASM rows. The placeholder `Not specified in the source documents (GAP-0316; ASM-0408)` appears in the Review by cell of R-19 to R-27.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-DELIVDOC-48 --quick` - C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS. No failure, no retry needed.

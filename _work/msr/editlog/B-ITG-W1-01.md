# Edit log — WP B-ITG-W1-01 (RWB-ITG-W1, wave 1 integration stories)

Tools and model: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60. Date: 22 November 2026.

Execution mode: fanout 5. One `aisdlc-msr-worker` task subagent per legacy key (RWB-E1-001, RWB-E1-002, RWB-E1-007, RWB-E1-008, RWB-E1-011), all five dispatched in one message; each wrote only its own story file, its own fragment and its own candidate rows in the two shared registers.

## Files written

- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1001 ITG Recovery tables for the 14 data products - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1002 ITG Case list v1 with case ID, owner and queue - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1007 ITG Integration adapters for outbound files - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1008 ITG Decision log store v1, append only and hash chained - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1011 ITG Reconciliation and data quality report - integration v1.md
- _work/msr/fragments/RWB-ITG-E1001-ITG.json
- _work/msr/fragments/RWB-ITG-E1002-ITG.json
- _work/msr/fragments/RWB-ITG-E1007-ITG.json
- _work/msr/fragments/RWB-ITG-E1008-ITG.json
- _work/msr/fragments/RWB-ITG-E1011-ITG.json
- _work/msr/gaps/B-ITG-W1-01.jsonl
- _work/msr/assumptions/B-ITG-W1-01.jsonl
- _work/msr/editlog/B-ITG-W1-01.md

## Counts

| Item | Count | Detail |
|---|---|---|
| Stories | 5 | one per legacy key, 19 sections and 20 metadata rows each |
| Fragments | 5 | the WP step-8 key set, `prd_ref` Pending (C1) |
| Acceptance criteria | 35 | 14 legacy ACs copied verbatim with the origin tag; 21 new integration ACs tagged (new, D-RCV-60) |
| Test cases | 73 | 52 legacy TC copies with the -ITG suffix and the Level column; 21 new TCs for the new ACs |
| Candidate gap rows (CG) | 7 | one combined row per story for the mandatory missing value, plus two sourced conflict rows (E1007, E1011) |
| Candidate assumption rows (ASM) | 7 | one per gap, every one linked to its CG id |

E1008 owns no legacy AC (`acs` empty in the WP), so its five ACs are all new integration criteria and its ten legacy TCs are carried as -ITG copies against them.

## Verification

- WP quick check `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W1-01 --quick`: C02, C03, C05, C12, C13 and C18 all PASS.
- Additional local verification (read-only scripts in `_work/msr/logs/`): every owned legacy AC body is byte-identical to the legacy story; all 20 metadata rows and their values match the WP JSON; the 19 headings are complete and in order; 12.1 to 12.9 exist in every story; every fragment has the full key set and the WP values; every cited CG/ASM id resolves to a row; no U+FFFD, no BOM, UTF-8 throughout.

## Notes

- Two extra candidate gap rows were kept beyond the mandatory one per story: `GAP-0338` and `GAP-0337` record Conflict findings between the Architecture v5 slide 13 connection matrix and the REST call types of the file and reconciliation paths; both carry their own assumption row.
- E1011 section 12.2 marks the rwb-case exclusion read as the operation the P3 contract must publish, with the placeholder and both ids, because no source names its path; the notice read uses the documented `GET /cases/{caseId}/notices` of rwb-comms.
- No legacy file was edited; no master file, tracker, register or architecture document was touched.

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Edit log — WP B-REQ-PRD-S3

| Item | Value |
|---|---|
| Work package | B-REQ-PRD-S3 — PRD S3 rwb-guarantee v1 (PRD Builder) |
| Agent | aisdlc-prd-builder |
| Tool line | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Decision | D-RCV-60 (microservice realignment) |
| Date | 22 November 2026 |
| Fanout | 0; no subagent was used |
| Status | Complete. No step was blocked and nothing failed |

## 1. Files written

- `03 Requirements and specifications/PRD/Recovery Workbench PRD S3 rwb-guarantee v1.md`
- `_work/msr/docs/B-REQ-PRD-S3/sources-read.md`
- `_work/msr/gaps/B-REQ-PRD-S3.jsonl`
- `_work/msr/assumptions/B-REQ-PRD-S3.jsonl`
- `_work/msr/editlog/B-REQ-PRD-S3.md`

No existing file was edited. PRD S3 v1 is the first version of this family and sits next to the sibling PRDs in the same folder; the folder held no PRD for S3 before this run.

## 2. What the deliverable contains

| Section | Content | Count |
|---|---|---|
| 1 | Document control, change log, inherited history, documents read against | 1 change-log row, 4 history rows |
| 2 | Product overview, what is new, what is reused or leaves the service, 10 confirmed v5 constraints | 7 new, 17 reuse rows |
| 3 | Personas and roles | ROL-S3-01 to ROL-S3-12 (12) |
| 4 | Current state and target journeys | JRN-S3-01 to JRN-S3-05 (5) |
| 5 | Capabilities and features with BR, MoSCoW, wave and FSD feature | CAP-S3-001 to CAP-S3-013 (13) |
| 6 | Functional requirements with CAP, BR, FSD REQ, priority and wave | FR-S3-001 to FR-S3-032 (32) |
| 7 | Non-functional requirements with target, BR, priority and test | NFR-S3-001 to NFR-S3-030 (30) |
| 8 | Data requirements: owned entities, data read but not owned, field-level rules, data rules | 4 owned entity groups, 12 read rows |
| 9 | Integration points and integration questions | 16 rows, 4 questions |
| 10 | Release slicing: wave 0, before wave 3, wave 3 in 10 slices, later increments | 10 wave-3 slices |
| 11 | Acceptance criteria, requirement trace summary, validation evidence | AC-S3-001 to AC-S3-022 (22); 9 trace rows; 13 evidence rows |
| 12 | Open questions with owner role, needed-by, what is blocked and source | OQ-S3-01 to OQ-S3-16 (16) |
| 13 | Approval table, left empty | 2 rows |
| Appendix A | Sources and the sections used | 12 sources |

Every functional requirement names a BR and an FSD REQ, every non-functional requirement names a BR, and every capability, requirement and criterion appears in the trace summary of section 11.2. The BR and REQ coverage statement is in section 11.2: 7 of 7 program requirements and 4 of 4 E4 BRD requirements naming this service are covered.

## 3. Registers

| File | Rows | Range |
|---|---|---|
| `_work/msr/gaps/B-REQ-PRD-S3.jsonl` | 19 gap rows | GAP-1717 to GAP-1735 |
| `_work/msr/assumptions/B-REQ-PRD-S3.jsonl` | 23 assumption rows | ASM-2875 to ASM-2897 |

Rows 1 to 19 of the two registers pair one to one: each gap carries the assumption it was read under. Rows 20 to 23 are the four run-level assumptions (approval treated as given, the service wave against the business epic wave, the dates tentative, the requirement set of record). The numbering is the WP-local placeholder numbering; step D1 renumbers to GAP-nnnn and ASM-nnnn and rewrites every citation.

## 4. Source conflicts recorded rather than resolved silently

| Conflict | Gap |
|---|---|
| FSD reads the ACE views directly; Arch v5 makes rwb-source-data the only reader and gives the S3 row no P1 cell | GAP-1717 |
| FSD A2.2 has the system file the claim; INT-29 is not available today and the S3 row has no P2 or Outside cell | GAP-1718 |
| R-GUA-04 and Temporal slide 19 use an agent; the connection matrix gives the S3 row no P10 cell | GAP-1719 |
| LOV-CLAIM-STATUS has 5 values and the claim workflow has 17 states over 32 rules, with no mapping | GAP-1720, GAP-1723 |
| Arch v5 gives the schema three subject areas; the Ownership Map and the TSD name one table | GAP-1721 |
| TSD S3 publishes no event; Arch v5 names two claim events and the catalogue numbers neither | GAP-1727 |
| Arch v5 gives the service a GET; the API specification and the TSD publish POST and PATCH only | GAP-1726 |
| The guarantee claim route is R4 in R-LIT-01 and R4 is the guarantee claim in the case journeys | GAP-1732 |

No conflict was resolved by changing a source value: each one is a gap row with its assumption, and the PRD states the assumption where it is applied.

## 5. Places where the WP's base instruction was overridden by this run's rules

| Instruction in the base playbook | What was done here, and why |
|---|---|
| Take the BRD as Approved before starting | The BRD status was not treated as a stop: root rule 9 and the realignment overlay make a missing approval an assumption and the document continues in Draft (ASM-2894) |
| Append rows to `requirement/Traceability_Matrix.md` | Not written: root rule 7 gives master files to the assembler, and that path is not in this WP's "Write only". The BR to CAP to FR/NFR to AC trace is in section 11.2, ready for the assembler |
| Write in the AI-SDLC workspace `22 Microservice Realignment/aisdlc/` | Not written: the WP fixes the output paths at the workspace root, and the workspace copy holds no requirement folder for this service |
| Ask the user when a product question is open | No question was put to a person: all 16 questions are OQ rows with an owner role and a needed-by point (root rule 9) |

## 6. Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-PRD-S3 --quick` was run after the last write: C02, C03, C05, C12, C13 and C18 all PASS with zero findings for this WP.

The checks outside the quick set that read the same files were also run by hand on this WP's outputs: C14 (header lines) PASS, C17 (every CG- and ASM- citation resolves to a jsonl row) PASS, C20 (tool line, no wrong attribution) PASS. C19 was run and reports 200 findings, all of them planned outputs of other work packages whose queues have not been assembled yet; no finding names B-REQ-PRD-S3. The report file is written under `22 Microservice Realignment/checks/reports/`.

No check fails on a file this WP wrote, and nothing was left open as FAILED under root rule 13.

# Edit log B-REQ-PRD-P5 — PRD P5 rwb-document v1

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision: D-RCV-60. Date: 22 November 2026.

Agent: aisdlc-prd-builder. fanout: 0 (no subagent used).

## Files written

- `03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md`
- `_work/msr/gaps/B-REQ-PRD-P5.jsonl`
- `_work/msr/assumptions/B-REQ-PRD-P5.jsonl`
- `_work/msr/editlog/B-REQ-PRD-P5.md`
- `_work/msr/docs/B-REQ-PRD-P5/gen.py`

No source document was edited or moved. No output outside the WP "Write only" list was written.

## What was produced

| Item | Value |
|---|---|
| Output document | Recovery Workbench PRD P5 rwb-document v1 (first PRD of the family; status Draft) |
| Header | Template and Rules §R8.1 two-line header on lines 1 and 2 |
| Change log row | `1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash` |
| Sections | 13 sections plus Appendix A, in the PRD Builder order |
| Capabilities | CAP-P5-001 to CAP-P5-019 (19) |
| Functional requirements | FR-P5-001 to FR-P5-032 (32) |
| Non-functional requirements | NFR-P5-001 to NFR-P5-033 (33) |
| Acceptance criteria | AC-P5-001 to AC-P5-025 (25) |
| Journeys | JRN-P5-01 to JRN-P5-06 (6) |
| Roles | ROL-P5-01 to ROL-P5-14 (14) |
| Open questions | OQ-P5-01 to OQ-P5-14 (14) |
| Approval table | Empty, by design |

## Registers

| Register | File | Rows |
|---|---|---|
| Gaps | `_work/msr/gaps/B-REQ-PRD-P5.jsonl` | 15 (GAP-1580 to -15) |
| Assumptions | `_work/msr/assumptions/B-REQ-PRD-P5.jsonl` | 16 (ASM-2711 to -16) |

Every gap and every assumption row is cited at least once in the PRD; every CG and ASM citation in the PRD resolves to a row in these two files.

## Sources read

- `03 Requirements and specifications` BRDs at their latest versions, through `_work/msr/extract/`: Business Requirements Program v4, Epic 1 v4, Epic 2 v2.
- `_work/msr/extract/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD P5 Document hub v3.md` (22 features, 20 requirements, 218 acceptance criteria).
- `_work/msr/extract/Recovery Workbench Technical Specifications by Module v5/Recovery Workbench TSD P5 Document hub v2.md` (T3 data model, T-A operations API-P5-001 to API-P5-017).
- `22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md` (slides 8, 9, 16, 21, 41, 42, 44, 45).
- `22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md`.
- `22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md` (§R1, §R3, §R5, §R8, §R9).
- `_work/msr/plan/ownership.json` and `22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx`: 12 tables, 17 operations, EV-16, EV-17, JOB-12, JOB-17 and DocumentIntakeWorkflow owned by P5.
- `_work/msr/plan/split_plan.json` (`stats` and `legacy` only) and `_work/msr/plan/ids.json`.
- `_work/msr/extract/Recovery Workbench Non Functional Specification v3.md` for the numeric targets.

No conversion was needed: the FSD P5, the TSD P5 and the BRDs were already converted under `_work/msr/extract/`.

## Rulings applied

1. Precedence R-PREC rule 1: Architecture v5 wins on the store, the intake path, the job mechanism and the signature ownership. Each loser is a gap row plus an assumption row (GAP-1587, -9, -11; ASM-2720, -11, -13).
2. Requirements of the BRD with no FSD feature (REQ-DCM-012, -014, -015, -016, -017, -018, -019, -020) are carried from the BRD, the TSD operation list, the Ownership Map and the confirmed v5 constraint, and each is a gap row (GAP-1580, -2, -3, -4).
3. A missing approval or status is an assumption, not a stop (GAP-1592; ASM-2711). PRD status Draft, approval table empty.
4. Release dates are copied unchanged and marked "(tentative)": wave 1 30 November 2026, wave 2 31 December 2026, wave 4 30 June 2027. No date was raised as a gap.
5. No person is named; roles only. No issue-tracker, Confluence, GitLab, Figma or web access; no git command run.
6. No value was invented: where a source is silent the text carries `Not specified in the source documents (CG-…; ASM-…)` and the row exists in the register.

## BR coverage

All 20 program requirements REQ-DCM-001 to REQ-DCM-020 are covered by at least one functional requirement, and REQ-ACA-006, REQ-DRI-004 and REQ-ILG-005 are covered too. No BR is without an FR. The coverage gaps are in the source, not in the trace: 8 of the 20 requirements have no FSD feature section, and each one is recorded as a gap row and traced to the BRD, the TSD operation list or the confirmed v5 constraint.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-PRD-P5 --quick`:

| Check | Result | Findings |
|---|---|---|
| C02 metadata rows | PASS | 0 (story files only; this WP writes no story) |
| C03 19 sections | PASS | 0 (story files only) |
| C05 AC origin tags | PASS | 0 (story files only) |
| C12 no person names or emails | PASS | 0 |
| C13 no issue-tracker reference | PASS | 0 |
| C18 write scope and untouched legacy files | PASS | 0 |

Extended run of the remaining checks against the files of this WP: C01, C12, C13, C14 (header lines 1 and 2), C16 (service, topic and API names), C17 (every CG and ASM citation resolves to a jsonl row), C18 and C20 all PASS. C19 reports missing planned outputs for B-P1-04, B-P1-08 and B-P10-02 only; those are other work packages and outside this WP's write scope. Both expected outputs of this WP (`03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md` and this edit log) exist and carry the D-RCV-60 change-log row.

## Notes for the next step

The PRD is Draft and waits on the Product Owner and FDA approval gate. Open questions OQ-P5-01, OQ-P5-02, OQ-P5-05, OQ-P5-06, OQ-P5-07 and OQ-P5-08 block wave 1 acceptance; OQ-P5-03, OQ-P5-04, OQ-P5-09 and OQ-P5-13 block wave 2. The most material source conflict is legal hold: the BRD makes it an Epic 1 Must and the only delivery story (RWB-AD-021) is an Epic 8 story at 30 June 2027.

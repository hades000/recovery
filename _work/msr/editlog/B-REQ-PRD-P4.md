# B-REQ-PRD-P4 edit log

WP: `_work/msr/wp/B-REQ-PRD-P4.md` — PRD P4 rwb-access v1 (agent aisdlc-prd-builder).
Decision: D-RCV-60. Date: 22 November 2026.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Execution

- fanout: 0. One agent, no subagents, no merge step.
- No human approval was required (D-RCV-60 overlay). The four business requirement documents and the P4 technical and functional specifications carry status "In review" and no governance signature, so the PRD is issued with status Draft and an empty approval table; the missing approval is recorded as `ASM-2697` instead of stopping the run.
- Read first: BRD Program v4 (section 5.4, REQ-ACA-001 to REQ-ACA-013), BRD Epic 1 v4 (section 3.4), BRD Epic 2 v2 (section 3.4), Epics 3 to 8 Specification v3 (FEAT-ADM rows), FSD P4 Access and administration v3 (A1.2, A2.1 to A2.30, Requirements served), TSD P4 Access and administration v3 (T3.1, T3.2, T6.1, T6.3, T7, appendix T-A), Architecture v5 extract (slides 11, 14, 16, 20, 37, 41, 42, 43, 44), Non-Functional Specification v3 (NFR-001 to NFR-078), Decision Log v10 (DL01, DL03, DL26, DL38, DL39, DL40, DL48, D-RCV-35, D-RCV-36), Batch and Scheduling Design v4 (JOB-18), Event and Messaging Design v4, Temporal and Drools Design extract (slide 15), `_work/msr/plan/ownership.json`, `_work/msr/plan/split_plan.json` (stats and legacy), `_work/msr/plan/ids.json`, Template and Rules v1 (R1, R3, R5, R8, R9).
- No file that already existed was edited. The PRD folder did not exist; the file is a new v1. No source was converted with `compat/convert_sources.py`, because every source already had a text extract under `_work/msr/extract/`.
- Ownership applied throughout: role, permission, masking_rule, role_conflict and delegation_limit stay P4; `/admin/lists/{listCode}` and `/admin/reference-loads` (with approve, verify and rollback) go to P3; rule packages, rule rows, rule test cases, the six rule-package paths and the change report go to P7; `POST /admin/workflows/smoke` goes to PLT; `lov_value` goes to P3; `partner_user` goes to S9; feature flags, outbox, inbox, idempotency and the decision-record object are platform library objects.

## Files written

- `03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md`
- `_work/msr/docs/B-REQ-PRD-P4/source-notes.md`
- `_work/msr/gaps/B-REQ-PRD-P4.jsonl`
- `_work/msr/assumptions/B-REQ-PRD-P4.jsonl`
- `_work/msr/editlog/B-REQ-PRD-P4.md`

## Content counts

| Item | Count |
|---|---|
| Capabilities (CAP-P4-) | 14 |
| Functional requirements (FR-P4-) | 38 |
| Non-functional requirements (NFR-P4-) | 20 |
| Acceptance criteria (AC-P4-) | 32 |
| Open questions (Q-P4-) | 17 |
| Business requirements served | 13 of 13 (REQ-ACA-001 to REQ-ACA-013) |
| Business requirements with no functional requirement (coverage gaps) | 0 |
| Release increments | 3 (wave 1, 30 November 2026; wave 2, 31 December 2026; wave 4, 30 June 2027 — all tentative) |

## BR coverage

- Every P4 business requirement REQ-ACA-001 to REQ-ACA-013 is served by at least one functional requirement, and every functional and non-functional requirement names at least one BR. The map is section 6.1.
- Three requirements of other modules are partly served and are named in section 6.2, not claimed: REQ-CWC-006 (role rows only; queues and capacity are P3), REQ-CWC-018 (the authorise and masking answers), REQ-RDF-010 (the per-role data product check and the masking answer).
- Blocking questions for wave 1: Q-P4-01 (authorise, session and DoA schemas), Q-P4-02 (event contract and refresh window), Q-P4-03 (who owns the policy load path), Q-P4-11 (personal field register), Q-P4-12 (role conflict list and matrix row counts).

## Rows

- Gap rows: 16 — `GAP-1564` to `GAP-1579`. Severity: P2 for 8, P3 for 8. Types: Missing 8, Conflict 5, Ambiguous 2, Outdated 1.
- Assumption rows: 14 — `ASM-2697` to `ASM-2710`.
- Every placeholder in the PRD cites one of these rows, and every cited row exists in one of the two jsonl files. No row is numbered GAP-nnnn or ASM-nnnn here: only step D1 numbers the registers.

## Realignment changes made to the source position

| Change | Source position | PRD position |
|---|---|---|
| Reference-data loads, lists of values and the load path | API Specification v4 and TSD P4 T-A give them to P4 | Dependency on rwb-case; gap `GAP-1564` |
| Rule package administration and the change report | TSD P4 T1, T2, T3.1 and API-P4-014 to API-P4-020 | Out of P4 scope, dependency on rwb-decision; gap `GAP-1565` |
| Smoke workflow operation | TSD P4 API-P4-021 and TSD P3 API-P3-027 | Platform dependency; gap `GAP-1566` |
| `lov_value`, `partner_user` | TSD P4 T3.1 | Referenced entities owned by rwb-case and rwb-partner; gap `GAP-1567` |
| Case record view and history timeline | FSD P4 FEAT-ACA-11 and FEAT-ACA-12 | Out of P4 scope, rwb-case's screen; gap `GAP-1577` |
| Release checklist feature | FSD P4 FEAT-ACA-15 | Out of product scope; gap `GAP-1578` |
| Access log third object | REQ-ACA-006 and NFR-042 name the data lake copy | Read as the data products, since the lake is removed; gap `GAP-1576` |
| Release slicing | Epics, not services | Three increments by wave, each a list of CAP ids with the reason it is in that wave |

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-PRD-P4 --quick`:

| Check | Result | Findings |
|---|---|---|
| C02 | PASS | 0 |
| C03 | PASS | 0 |
| C05 | PASS | 0 |
| C12 | PASS | 0 |
| C13 | PASS | 0 |
| C18 | PASS | 0 |

The checks of the wider B set (C14, C15, C16, C17, C19, C20) were also run against the files of this WP: C14 and C17 pass on the PRD, C20 passes on this edit log, and C19 reports on other work packages' planned outputs only.

## Notes

- No person name, e-mail address or personal identifier appears in the output. Roles, role codes and decision IDs only.
- No issue tracker, wiki, design tool, source-control service or web call was made. No repository was committed.
- The service naming of the Template and Rules is used: schema `rwb_access`, base `/api/recovery/access/v1`, topic `rwb.access.events.v1`, event names `rwb.access.<Event>.v1`, task queue `rwb-access`, wave 1, epic `RWB-SVC-P4`.
- The document starts with the two header lines of Template and Rules §R8.1, then the front matter, and carries the D-RCV-60 change-log row with the tool line.

# Build-readiness review (script) — RWB-ITG-TE013-ITG Agent runtime client with fallback — integration

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-TE013-ITG (RWB ITG TE013 ITG Agent runtime client with fallback - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-TE-013 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Partial 5, Fail 7. Detcheck rows: 10 (3 P1). AC review rows: 0. Missing criteria: 0.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 15 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 5 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Pass | §8 has 12 rules | — |
| 5 | State transitions | Pass | §9 has 9 transitions | — |
| 6 | Authority | Pass | §10 has 10 roles | — |
| 7 | Data | Partial | §11 has 15 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-503, CG-ALL-511 |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1; P2 Activity Decision-record ingest of rwb-decision is not in Temporal Catalog v1 | CG-ALL-504, CG-ALL-506, CG-ALL-507 |
| 9 | Messages | Pass | §14 lists 2 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-46 has no empty, loading, error, no access state in the story | CG-ALL-512 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 15 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-ITG-TE013-01, TC-ITG-TE013-02, TC-ITG-TE013-03, TC-ITG-TE013-04, TC-ITG-TE013-05; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-508, CG-ALL-509, CG-ALL-510 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 2 build dependencies are not done yet (RWB-P10-TE013-APP, RWB-P7-TE013-APP); 2 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-505 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104); open decision DL33 (assumptions: ASM-0135, ASM-0140, ASM-0890) | — |
| 19 | Test data | Pass | every test case in §16 names its data (15) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-TE013-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-504 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-505 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-506 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-503 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-507 | Activity Decision-record ingest of rwb-decision is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-508 | Test cases not in Test Cases v8: TC-ITG-TE013-01, TC-ITG-TE013-02, TC-ITG-TE013-03, TC-ITG-TE013-04, TC-ITG-TE013-05 | X9 | Missing | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-509 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-510 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-511 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-512 | SCR-46 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

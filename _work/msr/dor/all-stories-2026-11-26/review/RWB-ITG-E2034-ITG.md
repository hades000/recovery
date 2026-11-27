# Build-readiness review (script) — RWB-ITG-E2034-ITG Interaction ledger on the case and from every channel

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E2034-ITG (RWB ITG E2034 ITG Interaction ledger on the case and from every channel - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E2-034 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 8 (1 P1). AC review rows: 0. Missing criteria: 0.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'member of the integration and QA team' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 9 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 10 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Pass | §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 9 transitions | — |
| 6 | Authority | Pass | §10 has 11 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-INT-036; §11 has 35 data rows; detcheck: P2 Field IDs DF-INT-036 are not all fields of v_ace_efs_action in LDM v9 | CG-ALL-759 |
| 8 | Contract | Fail | detcheck: P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-760 |
| 9 | Messages | Partial | §14 lists 3 messages; detcheck: P2 MSG-P3-024 text differs from the Error and Message Standard v4 | CG-ALL-761 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-04 has no empty, loading, error, no access state in the story | CG-ALL-764, CG-ALL-765 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 12 test cases; detcheck: P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-762, CG-ALL-763 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 9 build dependencies are not done yet (RWB-P1-E1066-APP, RWB-P1-E1067-APP, RWB-P1-E1069-APP, RWB-P1-E2034-APP, RWB-P2-E2034-APP, RWB-P3-E2016-APP); 9 dependencies named | — |
| 18 | Open decisions | Partial | open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355); open decision DL29 (assumptions: none); detcheck: P2 Open decision DL29 has no assumption | CG-ALL-766 |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E2034-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-760 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-759 | Field IDs DF-INT-036 are not all fields of v_ace_efs_action in LDM v9 | X3 | Conflict | Data |
| CG-ALL-761 | MSG-P3-024 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-766 | Open decision DL29 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-762 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-763 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-764 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-765 | SCR-04 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

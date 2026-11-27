# Build-readiness review (script) — RWB-PLT-E1071-APP Temporal worker and SDK in the recovery module

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-PLT-E1071-APP (RWB PLT E1071 APP Temporal worker and SDK in the recovery module v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | platform |
| Legacy key | RWB-E1-071 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 8, Fail 7. Detcheck rows: 28 (2 P1). AC review rows: 0. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'platform administrator' is in the roles table | — |
| 2 | Links | Partial | §18 has 17 traceability rows; detcheck: P2 FR-PLT-001 has 2 meanings in the PRD; P2 FR-PLT-009 has 2 meanings in the PRD; P2 FR-PLT-010 has 2 meanings in the PRD; P2 FR-PLT-011 has 2 meanings in the PRD (+15 more) | CG-ALL-1674, CG-ALL-1675, CG-ALL-1676, CG-ALL-1677, CG-ALL-1678, CG-ALL-1679, CG-ALL-1680, CG-ALL-1681, CG-ALL-1682, CG-ALL-1683, CG-ALL-1684, CG-ALL-1685 (+7) |
| 3 | Acceptance criteria | Partial | exception X6 is covered by 'TC-E1-071-08', not by a criterion; §7 holds 7 owned criteria in Gherkin; §5 has 6 exception paths | — |
| 4 | Business rules | Partial | 4 of 11 rules are covered by no criterion and no test case: BR2, BR4, BR6, BR10; §8 has 11 rules | — |
| 5 | State transitions | Pass | §9 has 4 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 5 data rows; detcheck: P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-1673 |
| 8 | Contract | Fail | detcheck: P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1; P2 Activity PlatformSmokeActivity is not in Temporal Catalog v1 | CG-ALL-1668, CG-ALL-1669 |
| 9 | Messages | Partial | §14 lists 5 messages; detcheck: P2 MSG-P4-001 is used with another meaning than the standard's; P2 MSG-GEN-004 is used with another meaning than the standard's | CG-ALL-1670, CG-ALL-1671 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-1693 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; §16 has 8 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-1672 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 build dependencies are not done yet (RWB-PLT-TE001-APP); 12 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-1667 |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (8) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-PLT-E1071-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1667 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-1668 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 22 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1669 | Activity PlatformSmokeActivity is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-1670 | MSG-P4-001 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-1671 | MSG-GEN-004 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-1674 | FR-PLT-001 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1675 | FR-PLT-009 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1676 | FR-PLT-010 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1677 | FR-PLT-011 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1678 | FR-PLT-012 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1679 | FR-PLT-013 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1680 | FR-PLT-014 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1681 | FR-PLT-015 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1682 | FR-PLT-016 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1683 | FR-PLT-017 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1684 | FR-PLT-018 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1685 | FR-PLT-021 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1686 | FR-PLT-022 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1687 | FR-PLT-023 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1688 | FR-PLT-024 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1689 | FR-PLT-025 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1690 | FR-PLT-026 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1691 | FR-PLT-028 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1692 | FR-PLT-029 has 2 meanings in the PRD | X16 | ID collision | Business analyst |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1672 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-1673 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-1693 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-1694 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | §5 X6: A role without Platform administration U calls `POST /admin/workflows/smoke` (covered by 'TC-E1-071-08' only) | Not specified in the source documents | |
| AC9 | §8 BR2, BR4, BR6, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC10 | error answers 401, 403 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC11 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC12 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC13 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

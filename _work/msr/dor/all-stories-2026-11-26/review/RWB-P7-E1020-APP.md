# Build-readiness review (script) — RWB-P7-E1020-APP Allocation and assignment engine v1

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P7-E1020-APP (RWB P7 E1020 APP Allocation and assignment engine v1 v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-decision |
| Legacy key | RWB-E1-020 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 7, Fail 9. Detcheck rows: 14 (3 P1). AC review rows: 1. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 3 Acceptance criteria; 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'team manager (RW-TEAMMGR), an internal auditor (RW-AUDIT) and the owning service itself' is in the roles table | — |
| 2 | Links | Pass | §18 has 15 traceability rows | — |
| 3 | Acceptance criteria | Fail | exception X4 is covered by 'TC-E1-020-15', not by a criterion; exception X8 has no criterion ('None'); §7 holds 6 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 3 of 10 rules are covered by no criterion and no test case: BR4, BR8, BR9; §8 has 10 rules; detcheck: P2 Rule ID ALLOC-014 used in the criteria exists in no current source | CG-ALL-6896 |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Pass | §11 has 12 data rows | — |
| 8 | Contract | Fail | detcheck: P1 GET /rule-models/{packageCode}/{version} is not in rwb-decision.yaml; P2 Payload of rwb.decision.RulePackageInForce.v1 differs from Kafka Catalog v1; P1 rwb.decision.DecisionRecorded.v1 is on topic rwb.decision-record.v1 in the catalog, not rwb.decision-record.v1` (shared) | CG-ALL-6892, CG-ALL-6894, CG-ALL-6895 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P2 MSG-P7-009 is used with another meaning than the standard's; P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-6897, CG-ALL-6898 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-38 has no empty, loading, error, no access state in the story | CG-ALL-6904 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-6902 |
| 12 | Test cases | Fail | AC6 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 15 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC6; P3 §18 test lists differ from RTM v7 | CG-ALL-6899, CG-ALL-6900, CG-ALL-6901 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-6893 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL22 (assumptions: ASM-1162, ASM-1304, ASM-2217, ASM-2569); open decision DL23 (assumptions: ASM-1232, ASM-1237, ASM-1259, ASM-1560) | — |
| 19 | Test data | Pass | every test case in §16 names its data (15) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P7-E1020-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.4 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6892 | GET /rule-models/{packageCode}/{version} is not in rwb-decision.yaml | X5 | Missing | Solution architect |
| CG-ALL-6893 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-6895 | rwb.decision.DecisionRecorded.v1 is on topic rwb.decision-record.v1 in the catalog, not rwb.decision-record.v1` (shared) | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6894 | Payload of rwb.decision.RulePackageInForce.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-6896 | Rule ID ALLOC-014 used in the criteria exists in no current source | X7 | Missing | Business analyst |
| CG-ALL-6897 | MSG-P7-009 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-6898 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-6900 | Criteria with no test case: AC6 | X9 | Missing | QA |
| CG-ALL-6902 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6899 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-6901 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-6903 | Flyway file V1020_1__allocation_record.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-6904 | SCR-38 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6905 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC6 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC14. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC14 | §5 X4: The ledger store is unavailable (covered by 'TC-E1-020-15' only) | Not specified in the source documents | |
| AC15 | §5 X8: A record carries a decision code of another point in a case's life, for example CASE_CREATED (the exception path has no criterion) | Not specified in the source documents | |
| AC16 | §8 BR4, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC17 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC18 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC19 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

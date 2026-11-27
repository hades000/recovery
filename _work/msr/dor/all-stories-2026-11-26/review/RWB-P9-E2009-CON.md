# Build-readiness review (script) — RWB-P9-E2009-CON Steering dashboard v1 data set — contract

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P9-E2009-CON (RWB P9 E2009 CON Steering dashboard v1 data set - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-reporting |
| Legacy key | RWB-E2-009 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Pass (not applicable) 2, Partial 9, Fail 4. Detcheck rows: 18 (2 P1). AC review rows: 0. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'contract owner of the reporting service (TechX)' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 2 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 7 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 11 of 11 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11; §8 has 11 rules | — |
| 5 | State transitions | Pass | §9 has 4 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 10 data rows; detcheck: P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-7844 |
| 8 | Contract | Fail | detcheck: P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1; P2 rwb-reporting is not a consumer of rwb.treatment.TreatmentApproved.v1 in Kafka Catalog v1; P2 rwb-reporting is not a consumer of rwb.comms.NoticeDelivered.v1 in Kafka Catalog v1; P2 rwb-reporting is not a consumer of rwb.agent.AgentRunCompleted.v1 in Kafka Catalog v1 (+1 more) | CG-ALL-7845, CG-ALL-7846, CG-ALL-7847, CG-ALL-7848, CG-ALL-7849 |
| 9 | Messages | Partial | MSG-P9-002 has no English text in §14; MSG-P1-001 has no English text in §14; MSG-GEN-003 has no English text in §14; MSG-P4-002 has no English text in §14; MSG-GEN-006 has no English text in §14; MSG-P7-003 has no English text in §14; §14 lists 6 messages; detcheck: P2 MSG-P9-002 is used with another meaning than the standard's; P2 MSG-P1-001 is used with another meaning than the standard's; P2 MSG-GEN-003 is used with another meaning than the standard's; P2 MSG-P4-002 is used with another meaning than the standard's (+2 more) | CG-ALL-7850, CG-ALL-7851, CG-ALL-7852, CG-ALL-7853, CG-ALL-7854, CG-ALL-7855 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-37 has no empty, loading, error, no access state in the story; P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-7859, CG-ALL-7860 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 8 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-P9-E2009-CON-01, TC-P9-E2009-CON-02, TC-P9-E2009-CON-03, TC-P9-E2009-CON-04, TC-P9-E2009-CON-05, TC-P9-E2009-CON-06, TC-P9-E2009-CON-07, TC-P9-E2009-CON-08; P3 §18 test lists differ from RTM v7 | CG-ALL-7856, CG-ALL-7857 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602) | — |
| 19 | Test data | Pass | every test case in §16 names its data (8) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.4 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7845 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-7849 | Workflow reportingMeasuresDaily` (JOB-15; name Not specified in the source documents (GAP-2577; ASM-4248)) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 10 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7844 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7846 | rwb-reporting is not a consumer of rwb.treatment.TreatmentApproved.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-7847 | rwb-reporting is not a consumer of rwb.comms.NoticeDelivered.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-7848 | rwb-reporting is not a consumer of rwb.agent.AgentRunCompleted.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-7850 | MSG-P9-002 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7851 | MSG-P1-001 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7852 | MSG-GEN-003 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7853 | MSG-P4-002 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7854 | MSG-GEN-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7855 | MSG-P7-003 is used with another meaning than the standard's | X8 | ID collision | Business analyst |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7856 | Test cases not in Test Cases v8: TC-P9-E2009-CON-01, TC-P9-E2009-CON-02, TC-P9-E2009-CON-03, TC-P9-E2009-CON-04, TC-P9-E2009-CON-05, TC-P9-E2009-CON-06, TC-P9-E2009-CON-07, TC-P9-E2009-CON-08 | X9 | Missing | QA |
| CG-ALL-7857 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-7858 | Flyway file V2_009__measure_publish.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-7859 | SCR-37 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7860 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7861 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC9 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC10 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC11 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

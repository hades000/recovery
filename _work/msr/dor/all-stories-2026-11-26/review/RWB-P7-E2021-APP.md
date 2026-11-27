# Build-readiness review (script) — RWB-P7-E2021-APP Letter dispatch loop with proof of delivery from WIN

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P7-E2021-APP (RWB P7 E2021 APP Letter dispatch loop with proof of delivery from WIN v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-decision |
| Legacy key | RWB-E2-021 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 7, Fail 7. Detcheck rows: 14 (4 P1). AC review rows: 0. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 7 Data; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'conduct and QA officer (RW-CONDUCT), a litigation officer (RW-LITOFF) and an internal auditor (RW-AUDIT)' is in the roles table | — |
| 2 | Links | Pass | §18 has 24 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 9 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 2 of 14 rules are covered by no criterion and no test case: BR13, BR14; §8 has 14 rules | — |
| 5 | State transitions | Pass | §9 has 9 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Fail | §11 has 21 data rows; detcheck: P1 Index column decision_log_entry.decided_at DESC is not a field of decision_log_entry in LDM v9; P2 Name `tr_declog_append_only` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-7244, CG-ALL-7245 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/decision/v1/decision-log is not in rwb-decision.yaml; P1 GET /api/recovery/decision/v1/decision-log/{entryId} is not in rwb-decision.yaml; P2 HTTP errors with no message ID: 401 no session; 422 a query value is outside its list; 503 the ledger is unavailable. Every error is an RFC 9457 problem response with `messageId` set. `GET /api/recovery/decision/v1/cases/{caseId}/recommendation` (API-P7-001) and the approval operations (API-P7-002 to API-P7-005) are the decision center's and belong to the approval and recommendation stories of this service; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-7246, CG-ALL-7247, CG-ALL-7248, CG-ALL-7249 |
| 9 | Messages | Partial | §14 lists 8 messages; detcheck: P2 MSG-P7-009 is used with another meaning than the standard's | CG-ALL-7250 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-04 has no empty, loading, error, no access state in the story; P3 SCR-18 has no empty, loading, error, no access state in the story; P3 SCR-38 has no empty, loading, error, no access state in the story | CG-ALL-7254, CG-ALL-7255, CG-ALL-7256 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-7252 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 14 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-7251 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (14) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P7-E2021-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.2 has no owner or service column; §13 names other schemas: rwb_case, rwb_comms, rwb_integration, rwb_source_data | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7244 | Index column decision_log_entry.decided_at DESC is not a field of decision_log_entry in LDM v9 | X3 | Conflict | Data |
| CG-ALL-7246 | GET /api/recovery/decision/v1/decision-log is not in rwb-decision.yaml | X5 | Missing | Solution architect |
| CG-ALL-7247 | GET /api/recovery/decision/v1/decision-log/{entryId} is not in rwb-decision.yaml | X5 | Missing | Solution architect |
| CG-ALL-7249 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7245 | Name `tr_declog_append_only` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7248 | HTTP errors with no message ID: 401 no session; 422 a query value is outside its list; 503 the ledger is unavailable. Every error is an RFC 9457 problem response with `messageId` set. `GET /api/recovery/decision/v1/cases/{caseId}/recommendation` (API-P7-001) and the approval operations (API-P7-002 to API-P7-005) are the decision center's and belong to the approval and recommendation stories of this service | X5 | Missing | Business analyst |
| CG-ALL-7250 | MSG-P7-009 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7252 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7251 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-7253 | Flyway file V2021_1__decision_log_dispatch_index.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-7254 | SCR-04 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7255 | SCR-18 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7256 | SCR-38 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7257 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC13. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC13 | §8 BR13, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC14 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC15 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

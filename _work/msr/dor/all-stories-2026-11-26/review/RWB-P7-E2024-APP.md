# Build-readiness review (script) — RWB-P7-E2024-APP Field app photos and bills into the document hub

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P7-E2024-APP (RWB P7 E2024 APP Field app photos and bills into the document hub v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-decision |
| Legacy key | RWB-E2-024 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 7, Fail 8. Detcheck rows: 20 (3 P1). AC review rows: 3. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 7 Data; 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner (RW-CASEOWN) and the internal auditor (RW-AUDIT) who has to show what happened to an inspection' is in the roles table | — |
| 2 | Links | Pass | §18 has 14 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X10 is covered by 'TC-E2-024-16', not by a criterion; exception X11 is covered by 'TC-E2-024-12, TC-E2-024-14, TC-E2-024-15', not by a criterion; §7 holds 7 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | 8 of 15 rules are covered by no criterion and no test case: BR1, BR2, BR5, BR8, BR10, BR12, BR13, BR14; §8 has 15 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 13 roles | — |
| 7 | Data | Fail | §11 has 30 data rows; detcheck: P1 Index column decision_log_entry.object_ref is not a field of decision_log_entry in LDM v9; P2 Name `bill_amount` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `due_date` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `account_ref` is not a field or entity in LDM v9 or Data Classification v5 (+1 more) | CG-ALL-7270, CG-ALL-7271, CG-ALL-7272, CG-ALL-7273, CG-ALL-7274 |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P2 HTTP errors with no message ID: 401 no session; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-7275, CG-ALL-7276, CG-ALL-7277 |
| 9 | Messages | Partial | §14 lists 13 messages; detcheck: P2 MSG-P7-009 is used with another meaning than the standard's; P2 MSG-GEN-006 is used with another meaning than the standard's | CG-ALL-7278, CG-ALL-7279 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-11 has no empty, loading, error, no access state in the story; P3 SCR-30 has no empty, loading, error, no access state in the story; P3 SCR-31 has no empty, loading, error, no access state in the story | CG-ALL-7286, CG-ALL-7287, CG-ALL-7288 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-7283 |
| 12 | Test cases | Fail | AC4 has no test case in §16; AC5 has no test case in §16; AC6 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 17 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC4, AC5, AC6; P3 §18 test lists differ from RTM v7 | CG-ALL-7280, CG-ALL-7281, CG-ALL-7282 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL03 (assumptions: ASM-0189, ASM-0193, ASM-0578, ASM-2567); open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
| 19 | Test data | Pass | every test case in §16 names its data (17) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P7-E2024-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_access, rwb_case, rwb_document | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7270 | Index column decision_log_entry.object_ref is not a field of decision_log_entry in LDM v9 | X3 | Conflict | Data |
| CG-ALL-7275 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-7277 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 9 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7271 | Name `bill_amount` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7272 | Name `due_date` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7273 | Name `account_ref` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7274 | Name `tr_declog_append_only` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7276 | HTTP errors with no message ID: 401 no session | X5 | Missing | Business analyst |
| CG-ALL-7278 | MSG-P7-009 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7279 | MSG-GEN-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7281 | Criteria with no test case: AC4, AC5, AC6 | X9 | Missing | QA |
| CG-ALL-7283 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7280 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-7282 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-7284 | Flyway file V2_5_024__field_capture.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-7285 | Flyway file V2024_1__decision_field_capture_entry.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-7286 | SCR-11 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7287 | SCR-30 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7288 | SCR-31 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7289 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC4 | no test case in §16 |  |
| AC5 | no test case in §16 |  |
| AC6 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | §5 X10: The caller holds no right in the `DECISION_LOG` area, or asks for a case out of scope (covered by 'TC-E2-024-16' only) | Not specified in the source documents | |
| AC9 | §5 X11: A request never reached the store: a manifest and file mismatch, too many files, or a case outside the collector's scope (covered by 'TC-E2-024-12, TC-E2-024-14, TC-E2-024-15' only) | Not specified in the source documents | |
| AC10 | §8 BR1, BR2, BR5, BR8, BR10, BR12, BR13, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

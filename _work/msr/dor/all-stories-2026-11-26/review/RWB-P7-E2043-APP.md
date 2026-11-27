# Build-readiness review (script) — RWB-P7-E2043-APP Temporal and Drools integration pattern and reference case workflow

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P7-E2043-APP (RWB P7 E2043 APP Temporal and Drools integration pattern and reference case workflow v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-decision |
| Legacy key | RWB-E2-043 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 7, Fail 8. Detcheck rows: 18 (4 P1). AC review rows: 1. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 7 Data; 8 Contract; 14 Epic design; 16 Size; 17 Dependencies; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'developer of `rwb-decision` and the internal auditor (RW-AUDIT) who has to prove the order of a reference-case step' is in the roles table | — |
| 2 | Links | Pass | §18 has 4 traceability rows | — |
| 3 | Acceptance criteria | Partial | AC5 has no When; exception X7 is covered by 'TC-E2-043-04', not by a criterion; exception X8 is covered by 'TC-E2-043-01', not by a criterion; exception X9 is covered by 'TC-E2-043-01', not by a criterion; exception X10 is covered by 'TC-E2-043-01', not by a criterion; §7 holds 8 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Pass | §8 has 15 rules | — |
| 5 | State transitions | Pass | §9 has 8 transitions | — |
| 6 | Authority | Pass | §10 has 11 roles | — |
| 7 | Data | Fail | 3 row(s) of §11 have no BR Field ID; §11 has 28 data rows; detcheck: P1 Index column decision_log_entry.source_service is not a field of decision_log_entry in LDM v9; P1 Index column decision_log_entry.source_entry_ref is not a field of decision_log_entry in LDM v9; P2 Name `tr_declog_append_only` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `ingest_at` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-7435, CG-ALL-7436, CG-ALL-7437, CG-ALL-7438 |
| 8 | Contract | Fail | detcheck: P2 HTTP errors with no message ID: 401 no session; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1; P2 Activity ChainCheckActivity is not in Temporal Catalog v1 | CG-ALL-7439, CG-ALL-7441, CG-ALL-7442 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P2 MSG-P7-009 is used with another meaning than the standard's; P2 MSG-GEN-002 is used with another meaning than the standard's; P2 MSG-GEN-006 is used with another meaning than the standard's | CG-ALL-7443, CG-ALL-7444, CG-ALL-7445 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-38 has no empty, loading, error, no access state in the story; P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-7450, CG-ALL-7451 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-7448 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 7 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P3 §18 test lists differ from RTM v7 | CG-ALL-7446, CG-ALL-7447 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 1 dependencies named; detcheck: P1 Story RWB-P7-E1073-CON named as a dependency does not exist | CG-ALL-7440 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (7) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P7-E2043-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_access, rwb_case, rwb_document | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7435 | Index column decision_log_entry.source_service is not a field of decision_log_entry in LDM v9 | X3 | Conflict | Data |
| CG-ALL-7436 | Index column decision_log_entry.source_entry_ref is not a field of decision_log_entry in LDM v9 | X3 | Conflict | Data |
| CG-ALL-7440 | Story RWB-P7-E1073-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-7441 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7437 | Name `tr_declog_append_only` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7438 | Name `ingest_at` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7439 | HTTP errors with no message ID: 401 no session | X5 | Missing | Business analyst |
| CG-ALL-7442 | Activity ChainCheckActivity is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-7443 | MSG-P7-009 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7444 | MSG-GEN-002 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7445 | MSG-GEN-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7448 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7446 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-7447 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-7449 | Flyway file V2043_1__decision_central_ledger.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-7450 | SCR-38 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7451 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7452 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC5 | no When: the trigger is not stated |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §5 X7: A fact carries a personal-data field outside the schema — a name, an account number, a contact point (covered by 'TC-E2-043-04' only) | Not specified in the source documents | |
| AC10 | §5 X8: A correction arrives for an entry that exists (covered by 'TC-E2-043-01' only) | Not specified in the source documents | |
| AC11 | §5 X9: Two consumers of the same partition attempt the chain head at once (covered by 'TC-E2-043-01' only) | Not specified in the source documents | |
| AC12 | §5 X10: An entry is amended or deleted through the service login or through the schema owner role (covered by 'TC-E2-043-01' only) | Not specified in the source documents | |
| AC13 | error answers 401 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC14 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

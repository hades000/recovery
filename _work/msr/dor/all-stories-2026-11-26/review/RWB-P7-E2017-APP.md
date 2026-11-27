# Build-readiness review (script) — RWB-P7-E2017-APP Contract, CA and mortgage document generation screens

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P7-E2017-APP (RWB P7 E2017 APP Contract, CA and mortgage document generation screens v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-decision |
| Legacy key | RWB-E2-017 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 16 (5 P1). AC review rows: 0. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 7 Data; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'restructuring officer (FCR), a case owner and an internal audit reader' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 13 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 11 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 2 of 13 rules are covered by no criterion and no test case: BR9, BR13; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 12 roles | — |
| 7 | Data | Fail | §11 has 26 data rows; detcheck: P1 Index column decision_log_entry.decided_at DESC is not a field of decision_log_entry in LDM v9; P2 Name `tr_declog_append_only` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `transfer_price` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-7215, CG-ALL-7216, CG-ALL-7217 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/decision/v1/decision-log is not in rwb-decision.yaml; P1 GET /api/recovery/decision/v1/decision-log/{entryId} is not in rwb-decision.yaml; P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P2 HTTP errors with no message ID: 401 no session; 422 a query value is outside its list; 503 the ledger is unavailable. Every error is an RFC 9457 problem response with `messageId` set. `GET /api/recovery/decision/v1/cases/{caseId}/recommendation` (API-P7-001), the approval operations (API-P7-002 to API-P7-005 and API-P7-008) and the rule-registry paths belong to the other P7 stories of this service (+1 more) | CG-ALL-7218, CG-ALL-7219, CG-ALL-7220, CG-ALL-7221, CG-ALL-7222 |
| 9 | Messages | Partial | §14 lists 10 messages; detcheck: P2 MSG-P4-003 is used with another meaning than the standard's | CG-ALL-7223 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-14 has no empty, loading, error, no access state in the story; P3 SCR-30 has no empty, loading, error, no access state in the story; P3 SCR-38 has no empty, loading, error, no access state in the story | CG-ALL-7227, CG-ALL-7228, CG-ALL-7229 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-7225 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 15 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-7224 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'estimable' has no result in §6; INVEST 'small' has no result in §6 | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
| 19 | Test data | Pass | every test case in §16 names its data (15) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P7-E2017-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-case; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Pass | — | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case, rwb_comms, rwb_document, rwb_treatment | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7215 | Index column decision_log_entry.decided_at DESC is not a field of decision_log_entry in LDM v9 | X3 | Conflict | Data |
| CG-ALL-7218 | GET /api/recovery/decision/v1/decision-log is not in rwb-decision.yaml | X5 | Missing | Solution architect |
| CG-ALL-7219 | GET /api/recovery/decision/v1/decision-log/{entryId} is not in rwb-decision.yaml | X5 | Missing | Solution architect |
| CG-ALL-7220 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-7222 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7216 | Name `tr_declog_append_only` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7217 | Name `transfer_price` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-7221 | HTTP errors with no message ID: 401 no session; 422 a query value is outside its list; 503 the ledger is unavailable. Every error is an RFC 9457 problem response with `messageId` set. `GET /api/recovery/decision/v1/cases/{caseId}/recommendation` (API-P7-001), the approval operations (API-P7-002 to API-P7-005 and API-P7-008) and the rule-registry paths belong to the other P7 stories of this service | X5 | Missing | Business analyst |
| CG-ALL-7223 | MSG-P4-003 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-7225 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-7224 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-7226 | Flyway file V2026_2__decision_log_documentscreens_index.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-7227 | SCR-14 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7228 | SCR-30 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7229 | SCR-38 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-7230 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC14. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC14 | §8 BR9, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

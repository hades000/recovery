# Build-readiness review (script) — RWB-P5-AD021-CON Retention classes and legal hold

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P5-AD021-CON (RWB P5 AD021 CON Retention classes and legal hold - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-document |
| Legacy key | RWB-AD-021 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Pass (not applicable) 2, Partial 9, Fail 6. Detcheck rows: 22 (12 P1). AC review rows: 2. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 7 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 8 of 13 rules are covered by no criterion and no test case: BR1, BR4, BR8, BR9, BR10, BR11, BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Fail | §9 has 5 transitions; detcheck: P1 The story adds LEGAL10Y to the closed list LOV-RETENTION-ACTION; P1 The story adds GENERAL05Y to the closed list LOV-RETENTION-ACTION; P1 The story adds LEGAL10Y to the closed list LOV-RETENTION-END; P1 The story adds GENERAL05Y to the closed list LOV-RETENTION-END | CG-ALL-5715, CG-ALL-5716, CG-ALL-5717, CG-ALL-5718 |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 8 roles | — |
| 7 | Data | Partial | 11 row(s) of §11 have no BR Field ID; §11 has 11 data rows; detcheck: P2 Name `recorded_at` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-5719 |
| 8 | Contract | Fail | POST `/api/recovery/document/v1/admin/retention-loads` has no idempotency key; POST `/api/recovery/document/v1/admin/retention-loads/{loadId}/approve` has no idempotency key; POST `/api/recovery/document/v1/admin/retention-runs/{runId}/rerun` has no idempotency key; detcheck: P1 GET /api/recovery/document/v1/retention-classes is not in rwb-document.yaml; P1 GET /api/recovery/document/v1/retention-classes/{classCode} is not in rwb-document.yaml; P1 GET /api/recovery/document/v1/documents/{documentId}/retention is not in rwb-document.yaml; P1 GET /api/recovery/document/v1/documents/{documentId}/retention-actions is not in rwb-document.yaml (+4 more) | CG-ALL-5720, CG-ALL-5721, CG-ALL-5722, CG-ALL-5723, CG-ALL-5724, CG-ALL-5725, CG-ALL-5726, CG-ALL-5727 |
| 9 | Messages | Partial | §14 lists 12 messages; detcheck: P2 MSG-GEN-002 is used with another meaning than the standard's; P2 MSG-P1-020 is used with another meaning than the standard's; P2 MSG-P2-006 is used with another meaning than the standard's | CG-ALL-5728, CG-ALL-5729, CG-ALL-5730 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-31 has no empty, loading, error, no access state in the story; P3 SCR-32 has no empty, loading, error, no access state in the story | CG-ALL-5734, CG-ALL-5735 |
| 11 | Guardrails | Partial | §17 does not state the personal data rule | — |
| 12 | Test cases | Fail | AC6 has no test case in §16; AC7 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 3 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC6, AC7; P3 §18 test lists differ from RTM v7 | CG-ALL-5731, CG-ALL-5732, CG-ALL-5733 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'independent' has no result in §6; INVEST 'negotiable' has no result in §6; INVEST 'valuable' has no result in §6; INVEST 'estimable' has no result in §6; INVEST 'small' has no result in §6; INVEST 'testable' has no result in §6 | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
| 19 | Test data | Pass | every test case in §16 names its data (3) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 12 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5715 | The story adds LEGAL10Y to the closed list LOV-RETENTION-ACTION | X1 | Conflict | Product owner |
| CG-ALL-5716 | The story adds GENERAL05Y to the closed list LOV-RETENTION-ACTION | X1 | Conflict | Product owner |
| CG-ALL-5717 | The story adds LEGAL10Y to the closed list LOV-RETENTION-END | X1 | Conflict | Product owner |
| CG-ALL-5718 | The story adds GENERAL05Y to the closed list LOV-RETENTION-END | X1 | Conflict | Product owner |
| CG-ALL-5720 | GET /api/recovery/document/v1/retention-classes is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5721 | GET /api/recovery/document/v1/retention-classes/{classCode} is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5722 | GET /api/recovery/document/v1/documents/{documentId}/retention is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5723 | GET /api/recovery/document/v1/documents/{documentId}/retention-actions is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5724 | POST /api/recovery/document/v1/admin/retention-loads is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5725 | POST /api/recovery/document/v1/admin/retention-loads/{loadId}/approve is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5726 | GET /api/recovery/document/v1/admin/retention-runs is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5727 | POST /api/recovery/document/v1/admin/retention-runs/{runId}/rerun is not in rwb-document.yaml | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5719 | Name `recorded_at` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-5728 | MSG-GEN-002 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-5729 | MSG-P1-020 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-5730 | MSG-P2-006 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-5732 | Criteria with no test case: AC6, AC7 | X9 | Missing | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5731 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-5733 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5734 | SCR-31 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5735 | SCR-32 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5736 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC6 | no test case in §16 |  |
| AC7 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | §8 BR1, BR4, BR8, BR9, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

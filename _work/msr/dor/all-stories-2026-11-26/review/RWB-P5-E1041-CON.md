# Build-readiness review (script) — RWB-P5-E1041-CON Retention classes and virus scan on intake

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P5-E1041-CON (RWB P5 E1041 CON Retention classes and virus scan on intake - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-document |
| Legacy key | RWB-E1-041 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Pass (not applicable) 2, Partial 9, Fail 6. Detcheck rows: 18 (10 P1). AC review rows: 2. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 17 Dependencies; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 15 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 7 of 12 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR8, BR9, BR11, BR12; §8 has 12 rules | — |
| 5 | State transitions | Pass | §9 has 9 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 8 roles | — |
| 7 | Data | Partial | 11 row(s) of §11 have no BR Field ID; §11 has 11 data rows | — |
| 8 | Contract | Fail | detcheck: P1 GET /retention-rules is not in rwb-document.yaml; P1 GET /retention-rules/{classCode} is not in rwb-document.yaml; P1 POST /admin/retention-loads is not in rwb-document.yaml; P1 POST /admin/retention-loads/{loadId}/approve is not in rwb-document.yaml (+5 more) | CG-ALL-5886, CG-ALL-5887, CG-ALL-5888, CG-ALL-5889, CG-ALL-5890, CG-ALL-5891, CG-ALL-5892, CG-ALL-5893, CG-ALL-5895 |
| 9 | Messages | Partial | §14 lists 8 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-5896 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-44 has no empty, loading, error, no access state in the story; P3 SCR-47 has no empty, loading, error, no access state in the story | CG-ALL-5901, CG-ALL-5902 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-5900 |
| 12 | Test cases | Fail | AC8 has no test case in §16; no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC8; P3 §18 test lists differ from RTM v7 | CG-ALL-5897, CG-ALL-5898, CG-ALL-5899 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'independent' has no result in §6; INVEST 'negotiable' has no result in §6; INVEST 'valuable' has no result in §6; INVEST 'estimable' has no result in §6; INVEST 'small' has no result in §6; INVEST 'testable' has no result in §6 | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Fail | 0 dependencies named; detcheck: P1 Story RWB-P5-E1026-CON named as a dependency does not exist | CG-ALL-5894 |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 10 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5886 | GET /retention-rules is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5887 | GET /retention-rules/{classCode} is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5888 | POST /admin/retention-loads is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5889 | POST /admin/retention-loads/{loadId}/approve is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5890 | GET /admin/retention-loads/{loadId} is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5891 | POST /scans is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5892 | GET /documents/{documentId}/scan-status is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5893 | GET /intake-items/{intakeItemId}/scan-status is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5894 | Story RWB-P5-E1026-CON named as a dependency does not exist | X5 | Missing | Solution architect |
| CG-ALL-5895 | Event type rwb.document.RetentionApplied.v1 is not in Kafka Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5896 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-5898 | Criteria with no test case: AC8 | X9 | Missing | QA |
| CG-ALL-5900 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5897 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-5899 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5901 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5902 | SCR-47 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5903 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC8 | no test case in §16 |  |
| AC4 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC11. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC11 | §8 BR1, BR2, BR3, BR8, BR9, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

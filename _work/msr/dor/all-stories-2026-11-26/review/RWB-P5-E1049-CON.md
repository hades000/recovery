# Build-readiness review (script) — RWB-P5-E1049-CON OCR pipeline on the Workbench document hub

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P5-E1049-CON (RWB P5 E1049 CON OCR pipeline on the Workbench document hub - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-document |
| Legacy key | RWB-E1-049 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Pass (not applicable) 2, Partial 9, Fail 5. Detcheck rows: 12 (5 P1). AC review rows: 1. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 15 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 12 of 13 rules are covered by no criterion and no test case: BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 10 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 5 roles | — |
| 7 | Data | Partial | 8 row(s) of §11 have no BR Field ID; §11 has 8 data rows | — |
| 8 | Contract | Fail | detcheck: P1 POST /intake-items is not in rwb-document.yaml; P1 GET /intake-items/{intakeItemId}/text is not in rwb-document.yaml; P1 GET /intake-items/{intakeItemId}/ocr-status is not in rwb-document.yaml; P1 GET /api/recovery/case/v1/admin/parameters/{paramCode} is not published by rwb-case (+2 more) | CG-ALL-5919, CG-ALL-5920, CG-ALL-5921, CG-ALL-5922, CG-ALL-5923, CG-ALL-5924 |
| 9 | Messages | Pass | §14 lists 5 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-31 has no empty, loading, error, no access state in the story | CG-ALL-5929 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-5928 |
| 12 | Test cases | Fail | AC8 has no test case in §16; no boundary test for the tables of §12.7 (ASM-3438); §16 has 10 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P2 Criteria with no test case: AC8; P3 §18 test lists differ from RTM v7 | CG-ALL-5925, CG-ALL-5926, CG-ALL-5927 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'independent' has no result in §6; INVEST 'negotiable' has no result in §6; INVEST 'valuable' has no result in §6; INVEST 'estimable' has no result in §6; INVEST 'small' has no result in §6; INVEST 'testable' has no result in §6 | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (10) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.4 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5919 | POST /intake-items is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5920 | GET /intake-items/{intakeItemId}/text is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5921 | GET /intake-items/{intakeItemId}/ocr-status is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-5922 | GET /api/recovery/case/v1/admin/parameters/{paramCode} is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-5923 | Event type rwb.document.OcrCompleted.v1 is not in Kafka Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5924 | rwb-document is not a consumer of rwb.document.DocumentStored.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-5926 | Criteria with no test case: AC8 | X9 | Missing | QA |
| CG-ALL-5928 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5925 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-5927 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5929 | SCR-31 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5930 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC8 | no test case in §16 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §8 BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

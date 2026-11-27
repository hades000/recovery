# Build-readiness review (script) — RWB-P3-AD019-APP Data quality and reconciliation console

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-AD019-APP (RWB P3 AD019 APP Data quality and reconciliation console v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-AD-019 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 17 (7 P1). AC review rows: 2. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'data steward (RW-DATASTEW)' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 13 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X6 is covered by 'Access test TC-AD-019-04', not by a criterion; exception X9 is covered by 'Validation', not by a criterion; §7 holds 3 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 6 of 13 rules are covered by no criterion and no test case: BR1, BR9, BR10, BR11, BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has no transition (no status change in this story) | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 9 data rows; detcheck: P2 Criteria and test data read ACE views directly; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-3355, CG-ALL-3356 |
| 8 | Contract | Fail | detcheck: P1 GET /data-quality/reconciliation-breaks is not in rwb-case.yaml; P1 GET /data-quality/referential-completeness is not in rwb-case.yaml; P1 GET /data-quality/stale-products is not in rwb-case.yaml; P1 GET /api/recovery/source-data/v1/freshness is not published by rwb-source-data (+3 more) | CG-ALL-3343, CG-ALL-3344, CG-ALL-3345, CG-ALL-3346, CG-ALL-3347, CG-ALL-3348, CG-ALL-3349 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P3 MSG-P1-012 text differs from the Error and Message Standard v4; P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-3350, CG-ALL-3351 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story; P3 SCR-45 has no empty, loading, error, no access state in the story | CG-ALL-3357, CG-ALL-3358 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-3352 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; §16 has 4 test cases | — |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 2 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story of this legacy key; the CON stories it depends on are not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3343 | GET /data-quality/reconciliation-breaks is not in rwb-case.yaml | X5 | Missing | Solution architect |
| CG-ALL-3344 | GET /data-quality/referential-completeness is not in rwb-case.yaml | X5 | Missing | Solution architect |
| CG-ALL-3345 | GET /data-quality/stale-products is not in rwb-case.yaml | X5 | Missing | Solution architect |
| CG-ALL-3346 | GET /api/recovery/source-data/v1/freshness is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-3348 | Workflow DataQualityFreshnessCheck is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3353 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |
| CG-ALL-3354 | Java package th.co.scb.ace.workbench.recovery.case.dataquality uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3347 | HTTP errors with no message ID: 401 no session; 503 rwb-source-data down. The response schema, the error envelope and the status codes are fixed by the rwb-case service contract (GAP-0728 | X5 | Missing | Business analyst |
| CG-ALL-3349 | Activity refreshStaleSet is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3352 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-3355 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3350 | MSG-P1-012 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3351 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3356 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-3357 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3358 | SCR-45 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3359 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC1 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC2 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC4. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC4 | §5 X6: A role without Platform administration R opens SCR-45 (covered by 'Access test TC-AD-019-04' only) | Not specified in the source documents | |
| AC5 | §5 X9: The business date parameter is missing or malformed (covered by 'Validation' only) | Not specified in the source documents | |
| AC6 | §8 BR1, BR9, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC7 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC8 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC9 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

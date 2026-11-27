# Build-readiness review (script) — RWB-PLT-E1056-OPS Run books and monitoring for every Epic 1 Workbench job

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-PLT-E1056-OPS (RWB PLT E1056 OPS Run books and monitoring for every Epic 1 Workbench job - deployment v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | platform |
| Legacy key | RWB-E1-056 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 10, Fail 5. Detcheck rows: 24 (0 P1). AC review rows: 3. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'platform administrator (RW-PLATADM)' is in the roles table | — |
| 2 | Links | Partial | §18 has 4 traceability rows; detcheck: P2 FR-PLT-001 has 2 meanings in the PRD; P2 FR-PLT-009 has 2 meanings in the PRD; P2 FR-PLT-010 has 2 meanings in the PRD; P2 FR-PLT-011 has 2 meanings in the PRD (+10 more) | CG-ALL-1469, CG-ALL-1470, CG-ALL-1471, CG-ALL-1472, CG-ALL-1473, CG-ALL-1474, CG-ALL-1475, CG-ALL-1476, CG-ALL-1477, CG-ALL-1478, CG-ALL-1479, CG-ALL-1480 (+2) |
| 3 | Acceptance criteria | Pass | §7 holds 9 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 1 of 8 rules are covered by no criterion and no test case: BR8; §8 has 8 rules | — |
| 5 | State transitions | Pass | §9 has no transition (no status change in this story) | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | §11 has 21 data rows; detcheck: P2 Criteria and test data read ACE views directly | CG-ALL-1468 |
| 8 | Contract | Partial | detcheck: P2 platform is not a consumer of rwb.source-data.AceDataReady.v1 in Kafka Catalog v1; P2 platform is not a consumer of rwb.source-data.AceDataLate.v1 in Kafka Catalog v1 | CG-ALL-1461, CG-ALL-1462 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P3 MSG-P2-005 text differs from the Error and Message Standard v4; P3 MSG-P2-006 text differs from the Error and Message Standard v4; P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-1463, CG-ALL-1464, CG-ALL-1465 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-1483 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 10 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-E1-056-09, TC-E1-056-10; P3 §18 test lists differ from RTM v7 | CG-ALL-1466, CG-ALL-1467 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104) | — |
| 19 | Test data | Pass | every test case in §16 names its data (10) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-PLT-E1056-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.4 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 17 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1461 | platform is not a consumer of rwb.source-data.AceDataReady.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-1462 | platform is not a consumer of rwb.source-data.AceDataLate.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-1468 | Criteria and test data read ACE views directly | X12 | Outdated | QA |
| CG-ALL-1469 | FR-PLT-001 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1470 | FR-PLT-009 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1471 | FR-PLT-010 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1472 | FR-PLT-011 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1473 | FR-PLT-012 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1474 | FR-PLT-013 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1475 | FR-PLT-021 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1476 | FR-PLT-022 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1477 | FR-PLT-023 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1478 | FR-PLT-024 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1479 | FR-PLT-025 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1480 | FR-PLT-026 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1481 | FR-PLT-028 has 2 meanings in the PRD | X16 | ID collision | Business analyst |
| CG-ALL-1482 | FR-PLT-029 has 2 meanings in the PRD | X16 | ID collision | Business analyst |

### R3.3 Minor (P3) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1463 | MSG-P2-005 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-1464 | MSG-P2-006 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-1465 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-1466 | Test cases not in Test Cases v8: TC-E1-056-09, TC-E1-056-10 | X9 | Missing | QA |
| CG-ALL-1467 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-1483 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-1484 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC6 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC8 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |
| AC9 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §8 BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

# Build-readiness review (script) — RWB-P1-E1015-CON Freshness stamp per data product

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P1-E1015-CON (RWB P1 E1015 CON Freshness stamp per data product - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-source-data |
| Legacy key | RWB-E1-015 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Pass (not applicable) 2, Partial 7, Fail 4. Detcheck rows: 12 (4 P1). AC review rows: 0. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 5 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 6 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 8 of 8 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8; §8 has 8 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Pass | §10 has 5 roles | — |
| 7 | Data | Partial | 5 row(s) of §11 have no BR Field ID; §11 has 5 data rows | — |
| 8 | Contract | Fail | POST `/business-days/{date}/ready` has no idempotency key; detcheck: P1 GET /freshness is not in rwb-source-data.yaml; P1 POST /business-days/{date}/ready is not in rwb-source-data.yaml; P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P1 Workflow AceIngestCheckWorkflow is not in Temporal Catalog v1 (+1 more) | CG-ALL-2122, CG-ALL-2123, CG-ALL-2124, CG-ALL-2125, CG-ALL-2126 |
| 9 | Messages | Partial | §14 lists 5 messages; detcheck: P2 MSG-P4-001 is used with another meaning than the standard's; P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-2127, CG-ALL-2128 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story | CG-ALL-2132 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-E1-015-10, TC-E1-015-11, TC-E1-015-12; P3 Test cases cover other criteria in Test Cases v8; P3 §18 test lists differ from RTM v7 | CG-ALL-2129, CG-ALL-2130, CG-ALL-2131 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2122 | GET /freshness is not in rwb-source-data.yaml | X5 | Missing | Solution architect |
| CG-ALL-2123 | POST /business-days/{date}/ready is not in rwb-source-data.yaml | X5 | Missing | Solution architect |
| CG-ALL-2124 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-2125 | Workflow AceIngestCheckWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2126 | Activity checkDailyCompleteness is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2127 | MSG-P4-001 is used with another meaning than the standard's | X8 | ID collision | Business analyst |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2128 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2129 | Test cases not in Test Cases v8: TC-E1-015-10, TC-E1-015-11, TC-E1-015-12 | X9 | Missing | QA |
| CG-ALL-2130 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-2131 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2132 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2133 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC10 | error answers 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC11 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

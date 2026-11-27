# Build-readiness review (script) — RWB-ITG-E1011-ITG Reconciliation and data quality report — integration

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E1011-ITG (RWB ITG E1011 ITG Reconciliation and data quality report - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E1-011 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 14 (5 P1). AC review rows: 4. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'test engineer in the release squad (RW-TRIBE), with the data steward (RW-DATASTEW) as the reader of the result' is in the roles table | — |
| 2 | Links | Pass | §18 has 3 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X7 is covered by 'TC-E1-011-09-ITG', not by a criterion; exception X8 is covered by 'TC-E1-011-07-ITG', not by a criterion; §7 holds 9 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | 2 of 15 rules are covered by no criterion and no test case: BR3, BR4; §8 has 15 rules | — |
| 5 | State transitions | Pass | §9 has no transition (no status change in this story) | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | §11 has 23 data rows; detcheck: P2 Criteria and test data read ACE views directly; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-190, CG-ALL-191 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/source-data/v1/freshness is not published by rwb-source-data; P1 GET /api/recovery/case/v1/exclusions?businessDate={businessDate} is not published by rwb-case; P1 GET /api/recovery/comms/v1/cases/{caseId}/notices is not published by rwb-comms; P1 GET /api/recovery/reporting/v1/reports/{reportId} is not published by rwb-reporting (+2 more) | CG-ALL-179, CG-ALL-180, CG-ALL-181, CG-ALL-182, CG-ALL-183, CG-ALL-184 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P3 MSG-P1-012 text differs from the Error and Message Standard v4; P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-185, CG-ALL-186 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-45 has no empty, loading, error, no access state in the story | CG-ALL-192 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; §16 has 13 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E1-011-08-ITG, TC-E1-011-09-ITG, TC-ITG-E1011-01, TC-ITG-E1011-02, TC-ITG-E1011-03, TC-ITG-E1011-04; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-187, CG-ALL-188, CG-ALL-189 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 4 build dependencies are not done yet (RWB-P1-E1011-APP, RWB-P3-E1011-APP, RWB-P6-E1011-APP, RWB-S5-E1011-APP); 4 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602) | — |
| 19 | Test data | Pass | every test case in §16 names its data (13) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E1011-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-asset, rwb-case, rwb-comms, rwb-integration, rwb-reporting, rwb-source-data; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-179 | GET /api/recovery/source-data/v1/freshness is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-180 | GET /api/recovery/case/v1/exclusions?businessDate={businessDate} is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-181 | GET /api/recovery/comms/v1/cases/{caseId}/notices is not published by rwb-comms | X5 | Missing | Solution architect |
| CG-ALL-182 | GET /api/recovery/reporting/v1/reports/{reportId} is not published by rwb-reporting | X5 | Missing | Solution architect |
| CG-ALL-183 | Workflow Reconciliation workflow (JOB-04) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-184 | Activity Publish status step is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-187 | Test cases not in Test Cases v8: TC-E1-011-08-ITG, TC-E1-011-09-ITG, TC-ITG-E1011-01, TC-ITG-E1011-02, TC-ITG-E1011-03, TC-ITG-E1011-04 | X9 | Missing | QA |
| CG-ALL-190 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-185 | MSG-P1-012 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-186 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-188 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-189 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-191 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-192 | SCR-45 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC1 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC2 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC4 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC7 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC16. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC16 | §5 X7: A view or a store returns an error during the run (covered by 'TC-E1-011-09-ITG' only) | Not specified in the source documents | |
| AC17 | §5 X8: A role without Platform administration R lists the break rows (covered by 'TC-E1-011-07-ITG' only) | Not specified in the source documents | |
| AC18 | §8 BR3, BR4 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

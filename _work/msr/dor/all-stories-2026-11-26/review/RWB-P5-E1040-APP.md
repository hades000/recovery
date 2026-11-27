# Build-readiness review (script) — RWB-P5-E1040-APP Document checklist per case type as reference data

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P5-E1040-APP (RWB P5 E1040 APP Document checklist per case type as reference data v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-document |
| Legacy key | RWB-E1-040 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 10, Fail 5. Detcheck rows: 9 (0 P1). AC review rows: 0. Missing criteria: 7.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **READY WITH GAPS**.

Failed items: 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'litigation officer (RW-LITOFF)' is in the roles table | — |
| 2 | Links | Pass | §18 has 8 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X5 is covered by 'TC-E1-040-10 (Access)', not by a criterion; exception X6 is covered by 'Section 13, build step 4', not by a criterion; exception X7 is covered by 'TC-E1-040-10 (Access)', not by a criterion; §7 holds 9 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 1 of 7 rules are covered by no criterion and no test case: BR7; §8 has 7 rules | — |
| 5 | State transitions | Pass | §9 has no transition (no status change in this story) | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 5 roles | — |
| 7 | Data | Pass | §11 has 11 data rows | — |
| 8 | Contract | Partial | detcheck: P2 rwb-document is not a consumer of rwb.document.DocumentStored.v1 in Kafka Catalog v1; P2 rwb-document is not a consumer of rwb.case.CaseStateChanged.v1 in Kafka Catalog v1 | CG-ALL-5865, CG-ALL-5866 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P2 MSG-P3-027 text differs from the Error and Message Standard v4 | CG-ALL-5867 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-02 has no empty, loading, error, no access state in the story; P3 SCR-30 has no empty, loading, error, no access state in the story | CG-ALL-5871, CG-ALL-5872 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 14 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E1-040-01-ITG, TC-E1-040-02-ITG, TC-E1-040-05-ITG, TC-E1-040-08-ITG; P3 §18 test lists differ from RTM v7 | CG-ALL-5868, CG-ALL-5869 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 3 build dependencies are not done yet (RWB-P5-E1024-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP); 9 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL01 (assumptions: ASM-0189, ASM-1230, ASM-1770, ASM-1988); open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL19 (assumptions: ASM-1051, ASM-1164, ASM-1809, ASM-1810) | — |
| 19 | Test data | Pass | every test case in §16 names its data (14) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story of this legacy key; the CON stories it depends on are not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P5-E1024-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5865 | rwb-document is not a consumer of rwb.document.DocumentStored.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-5866 | rwb-document is not a consumer of rwb.case.CaseStateChanged.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-5867 | MSG-P3-027 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-5868 | Test cases not in Test Cases v8: TC-E1-040-01-ITG, TC-E1-040-02-ITG, TC-E1-040-05-ITG, TC-E1-040-08-ITG | X9 | Missing | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5869 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5870 | Flyway file V1_5_040__document_checklist.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-5871 | SCR-02 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5872 | SCR-30 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5873 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC10. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC10 | §5 X5: A role without Documents R opens the checklist (covered by 'TC-E1-040-10 (Access)' only) | Not specified in the source documents | |
| AC11 | §5 X6: The rwb-case contract does not answer inside the 2 s budget, or answers with an error (covered by 'Section 13, build step 4' only) | Not specified in the source documents | |
| AC12 | §5 X7: The case is outside the user's scope (covered by 'TC-E1-040-10 (Access)' only) | Not specified in the source documents | |
| AC13 | §8 BR7 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC14 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC15 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC16 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

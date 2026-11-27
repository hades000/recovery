# Build-readiness review (script) — RWB-P6-E1011-APP Reconciliation and data quality report

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P6-E1011-APP (RWB P6 E1011 APP Reconciliation and data quality report v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-comms |
| Legacy key | RWB-E1-011 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 21 (6 P1). AC review rows: 0. Missing criteria: 9.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'data steward and data product owner (RW-DATASTEW)' is in the roles table | — |
| 2 | Links | Pass | §18 has 27 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X7 is covered by 'TC-E1-011-09', not by a criterion; exception X8 is covered by 'TC-E1-011-07', not by a criterion; exception X9 is covered by 'BR10', not by a criterion; exception X10 is covered by 'TC-E1-011-07', not by a criterion; §7 holds 8 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 2 of 14 rules are covered by no criterion and no test case: BR13, BR14; §8 has 14 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Partial | §11 has 14 data rows; detcheck: P2 Name `comms_quality_run` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `comms_quality_result` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `comms_quality_break` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-6317, CG-ALL-6318, CG-ALL-6319 |
| 8 | Contract | Fail | detcheck: P1 GET /quality-runs/{businessDate} is not in rwb-comms.yaml; P1 GET /quality-results is not in rwb-comms.yaml; P1 GET /cases/{caseId}/notices is not in rwb-comms.yaml; P1 GET /api/recovery/source-data/v1/data-products/DP07/records is not published by rwb-source-data (+6 more) | CG-ALL-6320, CG-ALL-6321, CG-ALL-6322, CG-ALL-6323, CG-ALL-6324, CG-ALL-6325, CG-ALL-6326, CG-ALL-6327, CG-ALL-6328, CG-ALL-6329 |
| 9 | Messages | Partial | §14 lists 5 messages; detcheck: P3 MSG-P1-012 text differs from the Error and Message Standard v4; P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-6330, CG-ALL-6331 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-44 has no empty, loading, error, no access state in the story; P3 SCR-45 has no empty, loading, error, no access state in the story | CG-ALL-6335, CG-ALL-6336 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 9 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E1-011-08, TC-E1-011-09; P3 §18 test lists differ from RTM v7 | CG-ALL-6332, CG-ALL-6333 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602) | — |
| 19 | Test data | Pass | every test case in §16 names its data (9) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-P6-E1011-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6320 | GET /quality-runs/{businessDate} is not in rwb-comms.yaml | X5 | Missing | Solution architect |
| CG-ALL-6321 | GET /quality-results is not in rwb-comms.yaml | X5 | Missing | Solution architect |
| CG-ALL-6322 | GET /cases/{caseId}/notices is not in rwb-comms.yaml | X5 | Missing | Solution architect |
| CG-ALL-6323 | GET /api/recovery/source-data/v1/data-products/DP07/records is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-6324 | rwb-comms.yaml holds deliveryStatus as a closed enum while the story reads LOV-DELIVERY as data | X5 | Conflict | Solution architect |
| CG-ALL-6325 | Workflow NoticeQualityWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6317 | Name `comms_quality_run` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6318 | Name `comms_quality_result` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6319 | Name `comms_quality_break` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6326 | Activity loadTolerance is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-6327 | Activity readDeliveryFacts is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-6328 | Activity reconcileNotices is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-6329 | Activity writeQualityFacts is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-6332 | Test cases not in Test Cases v8: TC-E1-011-08, TC-E1-011-09 | X9 | Missing | QA |

### R3.3 Minor (P3) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6330 | MSG-P1-012 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-6331 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-6333 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-6334 | Flyway file V1011_1__comms_quality.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-6335 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6336 | SCR-45 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6337 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §5 X7: The parameters contract or the rwb-source-data contract returns an error mid-run (covered by 'TC-E1-011-09' only) | Not specified in the source documents | |
| AC10 | §5 X8: A role without Platform administration R reads the run record or the break rows (covered by 'TC-E1-011-07' only) | Not specified in the source documents | |
| AC11 | §5 X9: A caller reads a path outside `/api/recovery/comms/v1`, a cross-schema read appears, or an extract file or lake path is  (covered by 'BR10' only) | Not specified in the source documents | |
| AC12 | §5 X10: The token carries no Workbench role (covered by 'TC-E1-011-07' only) | Not specified in the source documents | |
| AC13 | §8 BR13, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC14 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC15 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC16 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC17 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

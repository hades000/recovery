# Build-readiness review (script) — RWB-P1-AD019-APP Data quality and reconciliation console

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P1-AD019-APP (RWB P1 AD019 APP Data quality and reconciliation console v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-source-data |
| Legacy key | RWB-AD-019 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 10, Fail 6. Detcheck rows: 12 (2 P1). AC review rows: 0. Missing criteria: 12.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'data steward (RW-DATASTEW) and a data product owner of the reconciliation' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 19 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X2 is covered by 'Component test', not by a criterion; exception X3 is covered by 'BR4; component test', not by a criterion; exception X6 is covered by 'Business rule BR6; component test', not by a criterion; exception X7 is covered by 'TC-AD-019-04', not by a criterion; exception X8 is covered by 'Component test', not by a criterion; exception X10 is covered by 'Business rule BR8', not by a criterion; §7 holds 1 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 10 of 14 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR8, BR9, BR10, BR14; §8 has 14 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Pass | §11 has 11 data rows | — |
| 8 | Contract | Fail | detcheck: P1 GET /admin/reconciliation/results is not in rwb-source-data.yaml; P2 rwb-source-data is not a consumer of rwb.source-data.AceDataReady.v1 in Kafka Catalog v1; P1 Workflow ReconciliationWorkflow is not in Temporal Catalog v1; P2 Activity runRec01 is not in Temporal Catalog v1 (+3 more) | CG-ALL-1864, CG-ALL-1865, CG-ALL-1866, CG-ALL-1867, CG-ALL-1868, CG-ALL-1869, CG-ALL-1870 |
| 9 | Messages | Partial | §14 lists 5 messages; detcheck: P3 MSG-P1-012 text differs from the Error and Message Standard v4; P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-1871, CG-ALL-1872 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-45 has no empty, loading, error, no access state in the story | CG-ALL-1874 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-1873 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 2 test cases | — |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 3 build dependencies are not done yet (RWB-P1-AD019-OPS, RWB-P1-E1015-APP, RWB-P1-E1069-APP); 6 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL25 (assumptions: ASM-0728, ASM-0735, ASM-0743, ASM-2602) | — |
| 19 | Test data | Pass | every test case in §16 names its data (2) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | no contract story of this legacy key; the CON stories it depends on are not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P1-E1015-APP, RWB-P1-E1069-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1864 | GET /admin/reconciliation/results is not in rwb-source-data.yaml | X5 | Missing | Solution architect |
| CG-ALL-1866 | Workflow ReconciliationWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1865 | rwb-source-data is not a consumer of rwb.source-data.AceDataReady.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-1867 | Activity runRec01 is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-1868 | Activity runRec02 is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-1869 | Activity resolveRec05 is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-1870 | Activity writeReconciliationResult is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-1873 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-1871 | MSG-P1-012 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-1872 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-1874 | SCR-45 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-1875 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC4. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC4 | §5 X2: No `case_list_row` exists for the business date (covered by 'Component test' only) | Not specified in the source documents | |
| AC5 | §5 X3: `AceDataReady` arrives twice with the same event id (covered by 'BR4; component test' only) | Not specified in the source documents | |
| AC6 | §5 X6: A result is BREAK over the tolerance (covered by 'Business rule BR6; component test' only) | Not specified in the source documents | |
| AC7 | §5 X7: The caller's Platform administration R is absent (covered by 'TC-AD-019-04' only) | Not specified in the source documents | |
| AC8 | §5 X8: The query carries a malformed `from` or `to` date (covered by 'Component test' only) | Not specified in the source documents | |
| AC9 | §5 X10: The parameter read of the baseline does not answer (covered by 'Business rule BR8' only) | Not specified in the source documents | |
| AC10 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR8, BR9, BR10, BR14 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC12 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC13 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC14 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC15 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

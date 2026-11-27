# Build-readiness review (script) — RWB-S5-E4030-APP Apply proceeds and raise the shortfall

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S5-E4030-APP (RWB S5 E4030 APP Apply proceeds and raise the shortfall v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-asset |
| Legacy key | RWB-E4-030 |

## R1. Verdict

**NOT READY.** Checklist: Pass 7, Partial 11, Fail 7. Detcheck rows: 16 (4 P1). AC review rows: 0. Missing criteria: 8.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'sale officer' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 13 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X9 is covered by '§17', not by a criterion; exception X10 is covered by 'GAP-2950', not by a criterion; §7 holds 4 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | rule row 'R-DIS-54' has no BR ID; rule row 'R-DIS-55' has no BR ID; 10 of 12 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 12 rules | — |
| 5 | State transitions | Fail | §9 has 9 transitions; detcheck: P1 The story adds PROCEEDS_APPLIED to the closed list LOV-HOLDING; P1 The story adds SHORTFALL_RAISED to the closed list LOV-HOLDING | CG-ALL-10176, CG-ALL-10177 |
| 6 | Authority | Partial | role SY-DATALOAD in §10 is not in Users Roles and Permissions v5; the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 6 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-COL-028, DF-COL-042; §11 has 11 data rows; detcheck: P2 Name `shortfall_amount` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `residual_route` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-10178, CG-ALL-10179, CG-ALL-10180, CG-ALL-10188 |
| 8 | Contract | Fail | detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/case/v1; P2 HTTP errors with no message ID: 400; 401; 404; 503 when a library or a contract does not answer; P1 Workflow AssetDisposalWorkflow task queue rwb-asset` in `rwb-recovery differs from the catalog; P2 Workflow ID form and start rule of AssetDisposalWorkflow are not stated (+1 more) | CG-ALL-10181, CG-ALL-10182, CG-ALL-10183, CG-ALL-10184, CG-ALL-10185 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P1-001; §14 lists 5 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-21 has no empty, error, no access state in the story; P3 SCR-22 has no empty, loading, error, no access state in the story | CG-ALL-10189, CG-ALL-10190 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-10187 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E4-030-01, TC-E4-030-02, TC-E4-030-03, TC-E4-030-04, TC-E4-030-05, TC-E4-030-06 | CG-ALL-10186 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 3 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Fail | the contract story RWB-S5-E4030-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.4 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10176 | The story adds PROCEEDS_APPLIED to the closed list LOV-HOLDING | X1 | Conflict | Product owner |
| CG-ALL-10177 | The story adds SHORTFALL_RAISED to the closed list LOV-HOLDING | X1 | Conflict | Product owner |
| CG-ALL-10181 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-10183 | Workflow AssetDisposalWorkflow task queue rwb-asset` in `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10178 | Name `shortfall_amount` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-10179 | Name `residual_route` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-10180 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-10182 | HTTP errors with no message ID: 400; 401; 404; 503 when a library or a contract does not answer | X5 | Missing | Business analyst |
| CG-ALL-10184 | Workflow ID form and start rule of AssetDisposalWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-10185 | Activity applyProceeds is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-10186 | Test cases not in Test Cases v8: TC-E4-030-01, TC-E4-030-02, TC-E4-030-03, TC-E4-030-04, TC-E4-030-05, TC-E4-030-06 | X9 | Missing | QA |
| CG-ALL-10187 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10188 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-10189 | SCR-21 has no empty, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-10190 | SCR-22 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-10191 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC5. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC5 | §5 X9: A statement reaches a `v_ace_*` view, `recovery_case` or a foreign schema (covered by '§17' only) | Not specified in the source documents | |
| AC6 | §5 X10: The residual routes nowhere because `residual_route` is unset (covered by 'GAP-2950' only) | Not specified in the source documents | |
| AC7 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC8 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC9 | duplicate delivery of a consumed event (no criterion covers a redelivered event) | Not specified in the source documents | |
| AC10 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC11 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC12 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

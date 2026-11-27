# Build-readiness review (script) — RWB-S5-E3027-CON Recommend the disposal route - contract

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S5-E3027-CON (RWB S5 E3027 CON Recommend the disposal route - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-asset |
| Legacy key | RWB-E3-027 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Pass (not applicable) 2, Partial 8, Fail 5. Detcheck rows: 13 (3 P1). AC review rows: 0. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 13 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 6 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 8 of 8 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8; §8 has 8 rules | — |
| 5 | State transitions | Fail | §9 has 6 transitions; detcheck: P1 The story adds ROUTE_APPROVED_BUYBACK to the closed list LOV-SALE-CHANNEL; P1 The story adds RENTAL_ACTIVE to the closed list LOV-SALE-CHANNEL | CG-ALL-9864, CG-ALL-9865 |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 7 roles | — |
| 7 | Data | Partial | 14 row(s) of §11 have no BR Field ID; §11 has 14 data rows; detcheck: P2 Name `route_recommendation` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `recommended_route` is not a field or entity in LDM v9 or Data Classification v5; P2 Criteria and test data read ACE views directly; P3 Criteria and tests keep legacy job and decision-log wording | CG-ALL-9866, CG-ALL-9867, CG-ALL-9872, CG-ALL-9873 |
| 8 | Contract | Fail | detcheck: P1 Workflow AssetDisposalWorkflow task queue rwb-asset` in namespace `rwb-recovery differs from the catalog; P2 Workflow ID form and start rule of AssetDisposalWorkflow are not stated | CG-ALL-9868, CG-ALL-9869 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-9870 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-21 has no empty, loading, error, no access state in the story; P3 SCR-22 has no empty, loading, error, no access state in the story | CG-ALL-9874, CG-ALL-9875 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 11 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-E3-027-01, TC-E3-027-02, TC-E3-027-03, TC-E3-027-04, TC-E3-027-05, TC-E3-027-06, TC-S5-E3027-CON-01, TC-S5-E3027-CON-02, TC-S5-E3027-CON-03, TC-S5-E3027-CON-04, TC-S5-E3027-CON-05 | CG-ALL-9871 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (11) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9864 | The story adds ROUTE_APPROVED_BUYBACK to the closed list LOV-SALE-CHANNEL | X1 | Conflict | Product owner |
| CG-ALL-9865 | The story adds RENTAL_ACTIVE to the closed list LOV-SALE-CHANNEL | X1 | Conflict | Product owner |
| CG-ALL-9868 | Workflow AssetDisposalWorkflow task queue rwb-asset` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9866 | Name `route_recommendation` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9867 | Name `recommended_route` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-9869 | Workflow ID form and start rule of AssetDisposalWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-9872 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9870 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-9871 | Test cases not in Test Cases v8: TC-E3-027-01, TC-E3-027-02, TC-E3-027-03, TC-E3-027-04, TC-E3-027-05, TC-E3-027-06, TC-S5-E3027-CON-01, TC-S5-E3027-CON-02, TC-S5-E3027-CON-03, TC-S5-E3027-CON-04, TC-S5-E3027-CON-05 | X9 | Missing | QA |
| CG-ALL-9873 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-9874 | SCR-21 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9875 | SCR-22 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9876 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC7. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC7 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC8 | error answers 401, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC9 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC10 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

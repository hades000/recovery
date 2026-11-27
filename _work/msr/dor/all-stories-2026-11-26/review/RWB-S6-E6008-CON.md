# Build-readiness review (script) — RWB-S6-E6008-CON Derecognize and post to the general ledger - contract

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S6-E6008-CON (RWB S6 E6008 CON Derecognize and post to the general ledger - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-debtsale |
| Legacy key | RWB-E6-008 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Pass (not applicable) 2, Partial 7, Fail 5. Detcheck rows: 42 (32 P1). AC review rows: 0. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 7 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 13 of 13 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Fail | §9 has 6 transitions; detcheck: P1 The story adds DATA_TRANSFERRED to the closed list LOV-BUYER-CLASS; P1 The story adds DERECOGNISED to the closed list LOV-BUYER-CLASS; P1 The story adds GL_POSTED to the closed list LOV-BUYER-CLASS; P1 The story adds POSTING_REJECTED_DS to the closed list LOV-BUYER-CLASS (+24 more) | CG-ALL-10669, CG-ALL-10670, CG-ALL-10671, CG-ALL-10672, CG-ALL-10673, CG-ALL-10674, CG-ALL-10675, CG-ALL-10676, CG-ALL-10677, CG-ALL-10678, CG-ALL-10679, CG-ALL-10680 (+16) |
| 6 | Authority | Pass | §10 has 6 roles | — |
| 7 | Data | Partial | 9 row(s) of §11 have no BR Field ID; §11 has 9 data rows | — |
| 8 | Contract | Fail | detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/source-data/v1; P1 No API Specification v5 yaml has the base of /api/recovery/case/v1; P1 No API Specification v5 yaml has the base of /api/recovery/decision/v1; P1 Workflow DebtSaleWorkflow task queue rwb-debtsale` in namespace `rwb-recovery differs from the catalog (+4 more) | CG-ALL-10697, CG-ALL-10698, CG-ALL-10699, CG-ALL-10700, CG-ALL-10701, CG-ALL-10702, CG-ALL-10703, CG-ALL-10704 |
| 9 | Messages | Partial | §14 lists 6 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4; P2 MSG-P2-001 is used with another meaning than the standard's | CG-ALL-10705, CG-ALL-10706 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-25 has no empty, loading, error, no access state in the story; P3 SCR-26 has no empty, loading, error, no access state in the story | CG-ALL-10708, CG-ALL-10709 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 10 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-E6-008-01, TC-E6-008-02, TC-E6-008-03, TC-E6-008-04, TC-E6-008-05, TC-E6-008-06, TC-S6-E6008-CON-01, TC-S6-E6008-CON-02, TC-S6-E6008-CON-03, TC-S6-E6008-CON-04 | CG-ALL-10707 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (10) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 32 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10669 | The story adds DATA_TRANSFERRED to the closed list LOV-BUYER-CLASS | X1 | Conflict | Product owner |
| CG-ALL-10670 | The story adds DERECOGNISED to the closed list LOV-BUYER-CLASS | X1 | Conflict | Product owner |
| CG-ALL-10671 | The story adds GL_POSTED to the closed list LOV-BUYER-CLASS | X1 | Conflict | Product owner |
| CG-ALL-10672 | The story adds POSTING_REJECTED_DS to the closed list LOV-BUYER-CLASS | X1 | Conflict | Product owner |
| CG-ALL-10673 | The story adds ALS_BALANCE_REMOVAL to the closed list LOV-BUYER-CLASS | X1 | Conflict | Product owner |
| CG-ALL-10674 | The story adds GL_ENTRY to the closed list LOV-BUYER-CLASS | X1 | Conflict | Product owner |
| CG-ALL-10675 | The story adds PROVISION_INPUT to the closed list LOV-BUYER-CLASS | X1 | Conflict | Product owner |
| CG-ALL-10676 | The story adds DATA_TRANSFERRED to the closed list LOV-LOT-STATUS | X1 | Conflict | Product owner |
| CG-ALL-10677 | The story adds DERECOGNISED to the closed list LOV-LOT-STATUS | X1 | Conflict | Product owner |
| CG-ALL-10678 | The story adds GL_POSTED to the closed list LOV-LOT-STATUS | X1 | Conflict | Product owner |
| CG-ALL-10679 | The story adds POSTING_REJECTED_DS to the closed list LOV-LOT-STATUS | X1 | Conflict | Product owner |
| CG-ALL-10680 | The story adds ALS_BALANCE_REMOVAL to the closed list LOV-LOT-STATUS | X1 | Conflict | Product owner |
| CG-ALL-10681 | The story adds GL_ENTRY to the closed list LOV-LOT-STATUS | X1 | Conflict | Product owner |
| CG-ALL-10682 | The story adds PROVISION_INPUT to the closed list LOV-LOT-STATUS | X1 | Conflict | Product owner |
| CG-ALL-10683 | The story adds DATA_TRANSFERRED to the closed list LOV-PUTBACK | X1 | Conflict | Product owner |
| CG-ALL-10684 | The story adds DERECOGNISED to the closed list LOV-PUTBACK | X1 | Conflict | Product owner |
| CG-ALL-10685 | The story adds GL_POSTED to the closed list LOV-PUTBACK | X1 | Conflict | Product owner |
| CG-ALL-10686 | The story adds POSTING_REJECTED_DS to the closed list LOV-PUTBACK | X1 | Conflict | Product owner |
| CG-ALL-10687 | The story adds ALS_BALANCE_REMOVAL to the closed list LOV-PUTBACK | X1 | Conflict | Product owner |
| CG-ALL-10688 | The story adds GL_ENTRY to the closed list LOV-PUTBACK | X1 | Conflict | Product owner |
| CG-ALL-10689 | The story adds PROVISION_INPUT to the closed list LOV-PUTBACK | X1 | Conflict | Product owner |
| CG-ALL-10690 | The story adds DATA_TRANSFERRED to the closed list LOV-SEGMENT | X1 | Conflict | Product owner |
| CG-ALL-10691 | The story adds DERECOGNISED to the closed list LOV-SEGMENT | X1 | Conflict | Product owner |
| CG-ALL-10692 | The story adds GL_POSTED to the closed list LOV-SEGMENT | X1 | Conflict | Product owner |
| CG-ALL-10693 | The story adds POSTING_REJECTED_DS to the closed list LOV-SEGMENT | X1 | Conflict | Product owner |
| CG-ALL-10694 | The story adds ALS_BALANCE_REMOVAL to the closed list LOV-SEGMENT | X1 | Conflict | Product owner |
| CG-ALL-10695 | The story adds GL_ENTRY to the closed list LOV-SEGMENT | X1 | Conflict | Product owner |
| CG-ALL-10696 | The story adds PROVISION_INPUT to the closed list LOV-SEGMENT | X1 | Conflict | Product owner |
| CG-ALL-10697 | No API Specification v5 yaml has the base of /api/recovery/source-data/v1 | X5 | Missing | Solution architect |
| CG-ALL-10698 | No API Specification v5 yaml has the base of /api/recovery/case/v1 | X5 | Missing | Solution architect |
| CG-ALL-10699 | No API Specification v5 yaml has the base of /api/recovery/decision/v1 | X5 | Missing | Solution architect |
| CG-ALL-10700 | Workflow DebtSaleWorkflow task queue rwb-debtsale` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10701 | Workflow ID form and start rule of DebtSaleWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-10702 | Activity derecogniseAccounts is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-10703 | Activity postToLedger is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-10704 | Activity The outbound item call is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-10706 | MSG-P2-001 is used with another meaning than the standard's | X8 | ID collision | Business analyst |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-10705 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-10707 | Test cases not in Test Cases v8: TC-E6-008-01, TC-E6-008-02, TC-E6-008-03, TC-E6-008-04, TC-E6-008-05, TC-E6-008-06, TC-S6-E6008-CON-01, TC-S6-E6008-CON-02, TC-S6-E6008-CON-03, TC-S6-E6008-CON-04 | X9 | Missing | QA |
| CG-ALL-10708 | SCR-25 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-10709 | SCR-26 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-10710 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

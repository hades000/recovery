# Build-readiness review (script) — RWB-P3-E1023-APP Case record view v1, read only

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P3-E1023-APP (RWB P3 E1023 APP Case record view v1, read only v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-case |
| Legacy key | RWB-E1-023 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 10 (2 P1). AC review rows: 2. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner (RW-CASEOWN)' is in the roles table | — |
| 2 | Links | Pass | §18 has 12 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X1 is covered by AC4, which this story neither owns nor names as owned by another story; exception X8 is covered by 'Access test TC-E1-023-11', not by a criterion; exception X9 is covered by AC12, which this story neither owns nor names as owned by another story; §7 holds 9 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | 5 of 13 rules are covered by no criterion and no test case: BR6, BR10, BR11, BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has no transition (no status change in this story) | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | §11 has 52 data rows; detcheck: P2 Criteria and test data read ACE views directly | CG-ALL-3591 |
| 8 | Contract | Fail | detcheck: P1 rwb-case.yaml holds partyRole as a closed enum while the story reads LOV-PARTY-ROLE as data | CG-ALL-3585 |
| 9 | Messages | Partial | §14 lists 7 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-3586 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-03 has no empty, loading, error, no access state in the story | CG-ALL-3592 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 13 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E1-023-12, TC-E1-023-13; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-3587, CG-ALL-3588, CG-ALL-3589 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 1 build dependencies are not done yet (RWB-P3-E1018-APP); 13 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355); open decision DL43 (assumptions: ASM-0193, ASM-0737, ASM-0748, ASM-0816) | — |
| 19 | Test data | Pass | every test case in §16 names its data (13) | — |
| 20 | Reference data | Partial | detcheck: P2 List LOV-CONTACT-TYPE is not in Reference Data v5 | CG-ALL-3584 |
| 21 | Contract published | Fail | the contract story RWB-P3-E1023-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P3-E1018-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3585 | rwb-case.yaml holds partyRole as a closed enum while the story reads LOV-PARTY-ROLE as data | X5 | Conflict | Solution architect |
| CG-ALL-3590 | Java package th.co.scb.ace.workbench.recovery.case uses the reserved word 'case' | X11 | Conflict | Solution architect |

### R3.2 Major (P2) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3584 | List LOV-CONTACT-TYPE is not in Reference Data v5 | X4 | Missing | Business analyst |
| CG-ALL-3587 | Test cases not in Test Cases v8: TC-E1-023-12, TC-E1-023-13 | X9 | Missing | QA |
| CG-ALL-3591 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3586 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-3588 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-3589 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3592 | SCR-03 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3593 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC2 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC3 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC13. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC13 | §5 X1: The ACE batch behind a section is not COMPLETE for the latest business date (covered by AC4, which exist nowhere in this story) | Not specified in the source documents | |
| AC14 | §5 X8: A role without Case record R opens the view (covered by 'Access test TC-E1-023-11' only) | Not specified in the source documents | |
| AC15 | §5 X9: A case link holds an `account_key` that the account contract does not return (covered by AC12, which exist nowhere in this story) | Not specified in the source documents | |
| AC16 | §8 BR6, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC17 | error answers 401, 403 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

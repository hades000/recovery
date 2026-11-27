# Build-readiness review (script) — RWB-S4-E5001-CON Issue demand and recall notices - contract

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S4-E5001-CON (RWB S4 E5001 CON Issue demand and recall notices - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-litigation |
| Legacy key | RWB-E5-001 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Pass (not applicable) 2, Partial 8, Fail 4. Detcheck rows: 8 (2 P1). AC review rows: 0. Missing criteria: 1.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 9 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 8 exception paths | — |
| 4 | Business rules | Partial | 12 of 12 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12; §8 has 12 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 5 roles | — |
| 7 | Data | Partial | 7 row(s) of §11 have no BR Field ID; §11 has 7 data rows | — |
| 8 | Contract | Fail | detcheck: P1 No API Specification v5 yaml has the base of /api/recovery/comms/v1; P1 Workflow LitigationWorkflow task queue rwb-litigation` in namespace `rwb-recovery differs from the catalog; P2 Workflow ID form and start rule of LitigationWorkflow are not stated; P2 Activity issueDemandAndRecallNotices is not in Temporal Catalog v1 | CG-ALL-9005, CG-ALL-9006, CG-ALL-9007, CG-ALL-9008 |
| 9 | Messages | Partial | §14 lists 7 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4 | CG-ALL-9009 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-18 has no empty, loading, error, no access state in the story | CG-ALL-9011 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 8 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-E5-001-01, TC-E5-001-02, TC-E5-001-03, TC-E5-001-04, TC-E5-001-05, TC-S4-E5001-CON-01, TC-S4-E5001-CON-02, TC-S4-E5001-CON-03 | CG-ALL-9010 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (8) | — |
| 20 | Reference data | Partial | reads lists or parameters and names neither the parameters nor the reference-data contract (DP-06, DP-07) | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9005 | No API Specification v5 yaml has the base of /api/recovery/comms/v1 | X5 | Missing | Solution architect |
| CG-ALL-9006 | Workflow LitigationWorkflow task queue rwb-litigation` in namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9007 | Workflow ID form and start rule of LitigationWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-9008 | Activity issueDemandAndRecallNotices is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-9009 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-9010 | Test cases not in Test Cases v8: TC-E5-001-01, TC-E5-001-02, TC-E5-001-03, TC-E5-001-04, TC-E5-001-05, TC-S4-E5001-CON-01, TC-S4-E5001-CON-02, TC-S4-E5001-CON-03 | X9 | Missing | QA |
| CG-ALL-9011 | SCR-18 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-9012 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

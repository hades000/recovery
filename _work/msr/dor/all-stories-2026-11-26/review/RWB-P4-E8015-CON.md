# Build-readiness review (script) — RWB-P4-E8015-CON Detect a broken hash chain in the decision log

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-E8015-CON (RWB P4 E8015 CON Detect a broken hash chain in the decision log - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-E8-015 |

## R1. Verdict

**NOT READY.** Checklist: Pass 13, Pass (not applicable) 2, Partial 6, Fail 4. Detcheck rows: 10 (4 P1). AC review rows: 3. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'tech lead' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 4 traceability rows | — |
| 3 | Acceptance criteria | Partial | AC2 has no When; AC3 has no When; AC5 has no When; §7 holds 6 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 9 of 9 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9; §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 7 roles | — |
| 7 | Data | Partial | 4 row(s) of §11 have no BR Field ID; §11 has 4 data rows | — |
| 8 | Contract | Fail | POST `/admin/chain-checks` has no idempotency key; detcheck: P1 POST /admin/chain-checks is not in rwb-access.yaml; P1 GET /admin/chain-checks is not in rwb-access.yaml; P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-5612, CG-ALL-5613, CG-ALL-5614, CG-ALL-5615 |
| 9 | Messages | Pass | §14 lists 5 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-39 has no empty, loading, error, no access state in the story; P3 SCR-41 has no empty, loading, error, no access state in the story; P3 SCR-43 has no empty, loading, error, no access state in the story | CG-ALL-5618, CG-ALL-5619, CG-ALL-5620 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-E8-015-CON-01, TC-E8-015-CON-02, TC-E8-015-CON-03, TC-E8-015-CON-04, TC-E8-015-CON-05, TC-E8-015-CON-06; P3 §18 test lists differ from RTM v7 | CG-ALL-5616, CG-ALL-5617 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Pass | — | — |
| 19 | Test data | Pass | every test case in §16 names its data (6) | — |
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
| CG-ALL-5612 | POST /admin/chain-checks is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-5613 | GET /admin/chain-checks is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-5614 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-5615 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 0 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5616 | Test cases not in Test Cases v8: TC-E8-015-CON-01, TC-E8-015-CON-02, TC-E8-015-CON-03, TC-E8-015-CON-04, TC-E8-015-CON-05, TC-E8-015-CON-06 | X9 | Missing | QA |
| CG-ALL-5617 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5618 | SCR-39 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5619 | SCR-41 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5620 | SCR-43 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5621 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC2 | no When: the trigger is not stated |  |
| AC3 | no When: the trigger is not stated |  |
| AC5 | no When: the trigger is not stated |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC7. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC7 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC8 | error answers 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC9 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC10 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC11 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

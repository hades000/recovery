# Build-readiness review (script) — RWB-P4-AD004-CON Masking profiles per role - contract

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-AD004-CON (RWB P4 AD004 CON Masking profiles per role - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-AD-004 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Pass (not applicable) 2, Partial 9, Fail 4. Detcheck rows: 10 (4 P1). AC review rows: 0. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'consumer of the access service** — the enforcement point, the two administration screens and any service that shows a personal field —' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 7 traceability rows | — |
| 3 | Acceptance criteria | Partial | §5 has no 'Covered by' column, so no exception path is tied to a criterion; §7 holds 6 owned criteria in Gherkin | — |
| 4 | Business rules | Partial | 7 of 7 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7; §8 has 7 rules | — |
| 5 | State transitions | Pass | §9 has 6 transitions | — |
| 6 | Authority | Pass | §10 has 4 roles | — |
| 7 | Data | Partial | §11 has 5 data rows; detcheck: P2 Criteria and test data read ACE views directly | CG-ALL-4590 |
| 8 | Contract | Fail | POST `/admin/masking-profile-versions` has no idempotency key; POST `/admin/masking-profiles/{roleCode}/unmask` has no idempotency key; detcheck: P1 GET /admin/masking-profiles is not in rwb-access.yaml; P1 POST /admin/masking-profile-versions is not in rwb-access.yaml; P1 POST /admin/masking-profiles/{roleCode}/unmask is not in rwb-access.yaml; P2 HTTP errors with no message ID: 409 a version label already in force or a stale `If-Match` (+1 more) | CG-ALL-4584, CG-ALL-4585, CG-ALL-4586, CG-ALL-4587, CG-ALL-4588 |
| 9 | Messages | Pass | §14 lists 5 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-43 has no empty, loading, error, no access state in the story; P3 SCR-47 has no empty, loading, error, no access state in the story | CG-ALL-4591, CG-ALL-4592 |
| 11 | Guardrails | Partial | §17 does not state the personal data rule | — |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 6 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-AD-004-CON-01, TC-AD-004-CON-02, TC-AD-004-CON-03, TC-AD-004-CON-04, TC-AD-004-CON-05, TC-AD-004-CON-06 | CG-ALL-4589 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'independent' has no result in §6; INVEST 'negotiable' has no result in §6; INVEST 'valuable' has no result in §6; INVEST 'estimable' has no result in §6; INVEST 'small' has no result in §6; INVEST 'testable' has no result in §6 | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
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
| CG-ALL-4584 | GET /admin/masking-profiles is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4585 | POST /admin/masking-profile-versions is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4586 | POST /admin/masking-profiles/{roleCode}/unmask is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4588 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4587 | HTTP errors with no message ID: 409 a version label already in force or a stale `If-Match` | X5 | Missing | Business analyst |
| CG-ALL-4590 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4589 | Test cases not in Test Cases v8: TC-AD-004-CON-01, TC-AD-004-CON-02, TC-AD-004-CON-03, TC-AD-004-CON-04, TC-AD-004-CON-05, TC-AD-004-CON-06 | X9 | Missing | QA |
| CG-ALL-4591 | SCR-43 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4592 | SCR-47 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4593 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC7. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC7 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC8 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC9 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

# Build-readiness review (script) — RWB-P4-AD014-APP Configure queues

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-AD014-APP (RWB P4 AD014 APP Configure queues v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-AD-014 |

## R1. Verdict

**NOT READY.** Checklist: Pass 8, Partial 10, Fail 7. Detcheck rows: 7 (3 P1). AC review rows: 0. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 5 State transitions; 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'reference data administrator (RW-REFADM)' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 6 traceability rows | — |
| 3 | Acceptance criteria | Partial | §5 has no 'Covered by' column, so no exception path is tied to a criterion; §7 holds 2 owned criteria in Gherkin | — |
| 4 | Business rules | Partial | rule row 'Every `overflow_queue_code` is either a ' has no BR ID; rule row 'Every `role_code` exists in `rwb_access.' has no BR ID; rule row 'Every `team_code` is a value of LOV-TEAM' has no BR ID; rule row 'Every `assignment_method` is a value of ' has no BR ID; rule row '`capacity_cap`, where the file carries i' has no BR ID; rule row '`queue_code` is unique in the file, `val' has no BR ID; rule row 'The acceptance entry is written before t' has no BR ID; §8 has 7 rules | — |
| 5 | State transitions | Fail | §9 has 4 transitions; detcheck: P1 The story adds ASSIGNMENT_METHOD_UNKNOWN to the closed list LOV-ASSIGN | CG-ALL-4782 |
| 6 | Authority | Pass | §10 has 4 roles | — |
| 7 | Data | Partial | §11 has 8 data rows; detcheck: P2 Name `overflow_queue_code` is not a field or entity in LDM v9 or Data Classification v5; P2 Criteria and test data read ACE views directly | CG-ALL-4783, CG-ALL-4786 |
| 8 | Contract | Fail | POST /api/recovery/access/v1/admin/queue-file-checks has no idempotency key; detcheck: P1 POST /api/recovery/access/v1/admin/queue-file-checks is not in rwb-access.yaml; P1 GET /api/recovery/access/v1/admin/queue-file-checks/{checkId} is not in rwb-access.yaml | CG-ALL-4784, CG-ALL-4785 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P1-002, MSG-P4-002, MSG-P7-003; §14 lists 0 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-42 has no empty, loading, error, no access state in the story; P3 SCR-43 has no empty, loading, error, no access state in the story | CG-ALL-4787, CG-ALL-4788 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 4 test cases | — |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'independent' has no result in §6; INVEST 'negotiable' has no result in §6; INVEST 'valuable' has no result in §6; INVEST 'estimable' has no result in §6; INVEST 'small' has no result in §6; INVEST 'testable' has no result in §6 | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 8 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL23 (assumptions: ASM-1232, ASM-1237, ASM-1259, ASM-1560) | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P4-AD014-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.7 has no owner or service column; §12.2 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4782 | The story adds ASSIGNMENT_METHOD_UNKNOWN to the closed list LOV-ASSIGN | X1 | Conflict | Product owner |
| CG-ALL-4784 | POST /api/recovery/access/v1/admin/queue-file-checks is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4785 | GET /api/recovery/access/v1/admin/queue-file-checks/{checkId} is not in rwb-access.yaml | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4783 | Name `overflow_queue_code` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-4786 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4787 | SCR-42 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4788 | SCR-43 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC3. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC3 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC4 | replay of a write with the same idempotency key (no criterion covers a replay) | Not specified in the source documents | |
| AC5 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC6 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

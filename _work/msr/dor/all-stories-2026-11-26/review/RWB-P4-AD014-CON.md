# Build-readiness review (script) — RWB-P4-AD014-CON Configure queues - contract

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-AD014-CON (RWB P4 AD014 CON Configure queues - contract v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-AD-014 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Pass (not applicable) 2, Partial 8, Fail 6. Detcheck rows: 5 (2 P1). AC review rows: 6. Missing criteria: 0.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 1 Story; 8 Contract; 12 Test cases; 14 Epic design; 16 Size; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Fail | §1 is not in the form 'As a <role>, I want ..., so that ...' | — |
| 2 | Links | Pass | §18 has 5 traceability rows | — |
| 3 | Acceptance criteria | Partial | §5 has no 'Covered by' column, so no exception path is tied to a criterion; §7 holds 8 owned criteria in Gherkin | — |
| 4 | Business rules | Partial | rule row 'One check, one answer' has no BR ID; rule row 'No partial acceptance' has no BR ID; rule row 'Row numbering is the file's' has no BR ID; rule row 'Field names are the owner's' has no BR ID; rule row 'No value in the document' has no BR ID; rule row 'Author and approver are two people' has no BR ID; rule row 'Additive within v1' has no BR ID; §8 has 7 rules | — |
| 5 | State transitions | Pass | §9 has 3 transitions | — |
| 6 | Authority | Pass | §10 has 3 roles | — |
| 7 | Data | Partial | 10 row(s) of §11 have no BR Field ID; §11 has 10 data rows | — |
| 8 | Contract | Fail | POST /api/recovery/access/v1/admin/queue-file-checks has no idempotency key; detcheck: P1 POST /api/recovery/access/v1/admin/queue-file-checks is not in rwb-access.yaml; P1 GET /api/recovery/access/v1/admin/queue-file-checks/{checkId} is not in rwb-access.yaml | CG-ALL-4789, CG-ALL-4790 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-GEN-001, MSG-P1-002, MSG-P4-002, MSG-P7-002, MSG-P7-003; §14 lists 0 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-42 has no empty, loading, error, no access state in the story; P3 SCR-43 has no empty, loading, error, no access state in the story | CG-ALL-4792, CG-ALL-4793 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Fail | AC3 has no test case in §16; AC4 has no test case in §16; AC5 has no test case in §16; AC8 has no test case in §16; §16 has 4 test cases; detcheck: P2 Criteria with no test case: AC3, AC4, AC5, AC8 | CG-ALL-4791 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'independent' has no result in §6; INVEST 'negotiable' has no result in §6; INVEST 'valuable' has no result in §6; INVEST 'estimable' has no result in §6; INVEST 'small' has no result in §6; INVEST 'testable' has no result in §6 | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL23 (assumptions: ASM-1232, ASM-1237, ASM-1259, ASM-1560) | — |
| 19 | Test data | Pass | every test case in §16 names its data (4) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Pass (not applicable) | this is the contract story | — |
| 22 | Fake published | Pass (not applicable) | this is the contract story; it publishes the fakes | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.2 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4789 | POST /api/recovery/access/v1/admin/queue-file-checks is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4790 | GET /api/recovery/access/v1/admin/queue-file-checks/{checkId} is not in rwb-access.yaml | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4791 | Criteria with no test case: AC3, AC4, AC5, AC8 | X9 | Missing | QA |

### R3.3 Minor (P3) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4792 | SCR-42 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-4793 | SCR-43 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC3 | no test case in §16 |  |
| AC4 | no test case in §16 |  |
| AC5 | no test case in §16 |  |
| AC8 | no test case in §16 |  |
| AC6 | message MSG-P4-002 is not in §14 |  |
| AC7 | message MSG-P7-003 is not in §14 |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

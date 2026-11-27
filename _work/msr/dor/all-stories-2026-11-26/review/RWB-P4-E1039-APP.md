# Build-readiness review (script) — RWB-P4-E1039-APP Access log into the decision log and break-glass admin

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-E1039-APP (RWB P4 E1039 APP Access log into the decision log and break-glass admin v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-E1-039 |

## R1. Verdict

**NOT READY.** Checklist: Pass 12, Partial 7, Fail 6. Detcheck rows: 12 (6 P1). AC review rows: 0. Missing criteria: 2.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'security administrator (RW-SECADM)' is in the roles table | — |
| 2 | Links | Pass | §18 has 10 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 10 owned criteria in Gherkin; §5 has 10 exception paths | — |
| 4 | Business rules | Partial | 4 of 11 rules are covered by no criterion and no test case: BR7, BR9, BR10, BR11; §8 has 11 rules | — |
| 5 | State transitions | Pass | §9 has 8 transitions | — |
| 6 | Authority | Pass | §10 has 9 roles | — |
| 7 | Data | Partial | §11 has 8 data rows; detcheck: P2 Name `break_glass_grant` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-5023 |
| 8 | Contract | Fail | POST `/api/recovery/access/v1/admin/break-glass-grants` has no idempotency key; POST `/api/recovery/access/v1/admin/break-glass-grants/{grantId}/end` has no idempotency key; detcheck: P1 GET /api/recovery/access/v1/admin/access-log is not in rwb-access.yaml; P1 POST /api/recovery/access/v1/admin/break-glass-grants is not in rwb-access.yaml; P1 POST /api/recovery/access/v1/admin/break-glass-grants/{grantId}/end is not in rwb-access.yaml; P1 GET /api/recovery/access/v1/admin/break-glass-grants/{grantId} is not in rwb-access.yaml (+2 more) | CG-ALL-5024, CG-ALL-5025, CG-ALL-5026, CG-ALL-5027, CG-ALL-5028, CG-ALL-5029 |
| 9 | Messages | Pass | §14 lists 8 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-38 has no empty, loading, error, no access state in the story; P3 SCR-43 has no empty, loading, error, no access state in the story | CG-ALL-5032, CG-ALL-5033 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-5031 |
| 12 | Test cases | Partial | no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-5030 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 3 build dependencies are not done yet (RWB-P4-E1022-APP, RWB-P4-E1039-DB, RWB-P4-E1039-OPS); 12 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL38 (assumptions: ASM-0245, ASM-1413, ASM-1424, ASM-1508); open decision DL40 (assumptions: ASM-0422, ASM-2705) | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P4-E1039-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-case; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P4-E1022-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5024 | GET /api/recovery/access/v1/admin/access-log is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-5025 | POST /api/recovery/access/v1/admin/break-glass-grants is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-5026 | POST /api/recovery/access/v1/admin/break-glass-grants/{grantId}/end is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-5027 | GET /api/recovery/access/v1/admin/break-glass-grants/{grantId} is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-5028 | rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | X5 | Conflict | Solution architect |
| CG-ALL-5029 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5023 | Name `break_glass_grant` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-5031 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-5030 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-5032 | SCR-38 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5033 | SCR-43 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5034 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC11. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC11 | §8 BR7, BR9, BR10, BR11 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC12 | error answers 401, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

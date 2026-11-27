# Build-readiness review (script) — RWB-P5-E1057-APP Intake from branches, mailroom, partner SFTP and email

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P5-E1057-APP (RWB P5 E1057 APP Intake from branches, mailroom, partner SFTP and email v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-document |
| Legacy key | RWB-E1-057 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 11 (3 P1). AC review rows: 0. Missing criteria: 8.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner' is in the roles table | — |
| 2 | Links | Pass | §18 has 10 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X3 is covered by AC7, which this story neither owns nor names as owned by another story; exception X5 is covered by AC9, which this story neither owns nor names as owned by another story; exception X9 is covered by AC13, which this story neither owns nor names as owned by another story; exception X12 is covered by 'Access test TC-E1-057-17', not by a criterion; §7 holds 11 owned criteria in Gherkin; §5 has 12 exception paths | — |
| 4 | Business rules | Partial | 1 of 9 rules are covered by no criterion and no test case: BR8; §8 has 9 rules | — |
| 5 | State transitions | Pass | §9 has 4 transitions | — |
| 6 | Authority | Partial | the story provides REST operations and names no rwb-access authorise check (DP-08); §10 has 4 roles | — |
| 7 | Data | Partial | §11 has 21 data rows; detcheck: P2 Name `uk_intake_channel_ref` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-6061 |
| 8 | Contract | Fail | POST `/api/recovery/document/v1/admin/jobs/{jobId}/rerun` has no idempotency key; detcheck: P1 GET /api/recovery/document/v1/admin/jobs is not in rwb-document.yaml; P1 GET /api/recovery/document/v1/admin/jobs/{jobId} is not in rwb-document.yaml; P1 POST /api/recovery/document/v1/admin/jobs/{jobId}/rerun is not in rwb-document.yaml | CG-ALL-6062, CG-ALL-6063, CG-ALL-6064 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-GEN-004; §14 lists 6 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-30 has no empty, loading, error, no access state in the story; P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-6069, CG-ALL-6070 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 17 test cases; detcheck: P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-6065, CG-ALL-6066 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 4 build dependencies are not done yet (RWB-P5-E1049-APP, RWB-P5-E1057-INF, RWB-P5-E1057-OPS, RWB-PLT-TE012-APP); 14 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL03 (assumptions: ASM-0189, ASM-0193, ASM-0578, ASM-2567); open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL11 (assumptions: ASM-0553, ASM-0703, ASM-1051, ASM-1104); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
| 19 | Test data | Pass | every test case in §16 names its data (17) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P5-E1057-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P5-E1049-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6062 | GET /api/recovery/document/v1/admin/jobs is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-6063 | GET /api/recovery/document/v1/admin/jobs/{jobId} is not in rwb-document.yaml | X5 | Missing | Solution architect |
| CG-ALL-6064 | POST /api/recovery/document/v1/admin/jobs/{jobId}/rerun is not in rwb-document.yaml | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6061 | Name `uk_intake_channel_ref` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |

### R3.3 Minor (P3) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6065 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-6066 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-6067 | Flyway file V1057_1__intake_channels.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-6068 | Flyway file V1_5_057__intake_channels.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-6069 | SCR-30 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6070 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-6071 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC17. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC17 | §5 X3: Partner subfolder code unknown or partner not ACTIVE (covered by AC7, which exist nowhere in this story) | Not specified in the source documents | |
| AC18 | §5 X5: No new file on any channel (covered by AC9, which exist nowhere in this story) | Not specified in the source documents | |
| AC19 | §5 X9: Email with no attachment, or only images under 10 KB (covered by AC13, which exist nowhere in this story) | Not specified in the source documents | |
| AC20 | §5 X12: A user without Platform administration U reruns the job (covered by 'Access test TC-E1-057-17' only) | Not specified in the source documents | |
| AC21 | §8 BR8 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC22 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC23 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |
| AC24 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

# Build-readiness review (script) — RWB-P4-E1037-APP Role to permission matrix as data and PDPA field masking by role

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P4-E1037-APP (RWB P4 E1037 APP Role to permission matrix as data and PDPA field masking by role v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-access |
| Legacy key | RWB-E1-037 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 16 (6 P1). AC review rows: 3. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'product owner' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 23 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X10 is covered by 'TC-E1-037-13', not by a criterion; exception X11 is covered by 'TC-E1-037-13', not by a criterion; §7 holds 13 owned criteria in Gherkin; §5 has 12 exception paths | — |
| 4 | Business rules | Partial | 3 of 15 rules are covered by no criterion and no test case: BR13, BR14, BR15; §8 has 15 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Pass | §10 has 13 roles | — |
| 7 | Data | Partial | §11 has 21 data rows; detcheck: P2 Name `uk_permission_version` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `uk_masking_rule` is not a field or entity in LDM v9 or Data Classification v5; P2 Criteria and test data read ACE views directly | CG-ALL-4987, CG-ALL-4988, CG-ALL-4999 |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/access/v1/admin/reference-loads is not in rwb-access.yaml; P1 POST /api/recovery/access/v1/admin/reference-loads/{loadId}/approve is not in rwb-access.yaml; P1 GET /api/recovery/access/v1/admin/roles is not in rwb-access.yaml; P1 GET /api/recovery/access/v1/masking-policies is not in rwb-access.yaml (+3 more) | CG-ALL-4989, CG-ALL-4990, CG-ALL-4991, CG-ALL-4992, CG-ALL-4993, CG-ALL-4994, CG-ALL-4995 |
| 9 | Messages | Pass | §14 lists 8 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-43 has no empty, loading, error, no access state in the story; P3 SCR-47 has no empty, loading, error, no access state in the story | CG-ALL-5000, CG-ALL-5001 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 15 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-E1-037-13, TC-E1-037-14, TC-E1-037-15; P3 §18 test lists differ from RTM v7 | CG-ALL-4996, CG-ALL-4997 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 1 build dependencies are not done yet (RWB-P4-E1022-APP); 12 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL02 (assumptions: ASM-0189, ASM-0324, ASM-5687); open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355); open decision DL38 (assumptions: ASM-0245, ASM-1413, ASM-1424, ASM-1508) | — |
| 19 | Test data | Pass | every test case in §16 names its data (15) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P4-E1037-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §13 names other schemas: rwb_case | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P4-E1022-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4989 | POST /api/recovery/access/v1/admin/reference-loads is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4990 | POST /api/recovery/access/v1/admin/reference-loads/{loadId}/approve is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4991 | GET /api/recovery/access/v1/admin/roles is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4992 | GET /api/recovery/access/v1/masking-policies is not in rwb-access.yaml | X5 | Missing | Solution architect |
| CG-ALL-4993 | rwb-access.yaml holds roleClass as a closed enum while the story reads LOV-ROLE-CLASS as data | X5 | Conflict | Solution architect |
| CG-ALL-4994 | rwb-access.yaml holds defaultScope as a closed enum while the story reads LOV-SCOPE as data | X5 | Conflict | Solution architect |

### R3.2 Major (P2) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4987 | Name `uk_permission_version` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-4988 | Name `uk_masking_rule` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-4995 | Payload of rwb.access.AccessPolicyChanged.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-4996 | Test cases not in Test Cases v8: TC-E1-037-13, TC-E1-037-14, TC-E1-037-15 | X9 | Missing | QA |
| CG-ALL-4999 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 5 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-4997 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-4998 | Flyway file V1037_1__permission_version_index.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-5000 | SCR-43 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5001 | SCR-47 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-5002 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC9 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC11 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |
| AC12 | vague wording in the steps (should, may, correctly, as expected); the Then must name a value |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC14. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC14 | §5 X10: A rule asks for the clear identity number (covered by 'TC-E1-037-13' only) | Not specified in the source documents | |
| AC15 | §5 X11: A masking file names a role code the `role` table does not hold, or a field id that is not `is_personal` (covered by 'TC-E1-037-13' only) | Not specified in the source documents | |
| AC16 | §8 BR13, BR14, BR15 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

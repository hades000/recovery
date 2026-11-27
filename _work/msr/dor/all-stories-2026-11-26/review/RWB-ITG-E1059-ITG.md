# Build-readiness review (script) — RWB-ITG-E1059-ITG Case intake agent in shadow [E1b]

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-ITG-E1059-ITG (RWB ITG E1059 ITG Case intake agent in shadow [E1b] - integration v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | integration |
| Legacy key | RWB-E1-059 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 10 (1 P1). AC review rows: 1. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'QA integration engineer** proving the case intake agent end to end on the real SIT services of rwb-agent (P10) and rwb-case (P3), with the published contracts of rwb-source-data (P1), rwb-document (P5) and rwb-access (P4) as wave-1 preconditions' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 21 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X3 is covered by 'Section 4 step 12', not by a criterion; exception X4 is covered by 'Section 4 step 12', not by a criterion; exception X8 is covered by 'Section 13', not by a criterion; exception X11 is covered by 'Section 12.8', not by a criterion; exception X15 is covered by 'Section 17', not by a criterion; §7 holds 14 owned criteria in Gherkin; §5 has 16 exception paths | — |
| 4 | Business rules | Partial | 16 of 16 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13, BR14, BR15, BR16; §8 has 16 rules | — |
| 5 | State transitions | Pass | §9 has 15 transitions | — |
| 6 | Authority | Pass | §10 has 14 roles | — |
| 7 | Data | Partial | §11 has 9 data rows; detcheck: P2 Name `read_case` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `read_accounts` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `read_contact_points` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `read_documents` is not a field or entity in LDM v9 or Data Classification v5 (+2 more) | CG-ALL-370, CG-ALL-371, CG-ALL-372, CG-ALL-373, CG-ALL-374, CG-ALL-378 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/source-data/v1/collateral/{id} is not published by rwb-source-data | CG-ALL-375 |
| 9 | Messages | Pass | §14 lists 3 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-46 has no empty, loading, error, no access state in the story | CG-ALL-379 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | §16 has 14 test cases; detcheck: P2 Test cases not in Test Cases v8: TC-ITG-E1059-ITG-10, TC-ITG-E1059-ITG-11, TC-ITG-E1059-ITG-12, TC-ITG-E1059-ITG-13, TC-ITG-E1059-ITG-14; P3 §18 test lists differ from RTM v7 | CG-ALL-376, CG-ALL-377 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P10-E1059-APP, RWB-P3-E1030-APP); 2 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (14) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-ITG-E1059-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-375 | GET /api/recovery/source-data/v1/collateral/{id} is not published by rwb-source-data | X5 | Missing | Solution architect |

### R3.2 Major (P2) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-370 | Name `read_case` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-371 | Name `read_accounts` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-372 | Name `read_contact_points` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-373 | Name `read_documents` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-374 | Name `read_valuations` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-376 | Test cases not in Test Cases v8: TC-ITG-E1059-ITG-10, TC-ITG-E1059-ITG-11, TC-ITG-E1059-ITG-12, TC-ITG-E1059-ITG-13, TC-ITG-E1059-ITG-14 | X9 | Missing | QA |
| CG-ALL-378 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-377 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-379 | SCR-46 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|
| AC5 | the Given reads an ACE view; this service reads source data through the rwb-source-data contract (DP-01, DP-05) |  |

## R5. Missing acceptance criteria

Proposed AC IDs start at AC15. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC15 | §5 X3: The answer confidence is below the policy floor of 0.80 (covered by 'Section 4 step 12' only) | Not specified in the source documents | |
| AC16 | §5 X4: The agent asks for a tool that is not on its allowed list (covered by 'Section 4 step 12' only) | Not specified in the source documents | |
| AC17 | §5 X8: An evaluation is started while one for the same agent and sample version is running (covered by 'Section 13' only) | Not specified in the source documents | |
| AC18 | §5 X11: A fake is configured for P1, P3, P4, P5 or P10 (covered by 'Section 12.8' only) | Not specified in the source documents | |
| AC19 | §5 X15: A suite step tries to read a service schema directly (covered by 'Section 17' only) | Not specified in the source documents | |
| AC20 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13, BR14, BR15, BR16 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

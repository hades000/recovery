# Build-readiness review (script) — RWB-P2-E1007-APP Integration adapters for outbound files

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P2-E1007-APP (RWB P2 E1007 APP Integration adapters for outbound files v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-integration |
| Legacy key | RWB-E1-007 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 10, Fail 6. Detcheck rows: 29 (7 P1). AC review rows: 0. Missing criteria: 6.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'platform administrator (RW-PLATADM)' is in the roles table | — |
| 2 | Links | Pass | §18 has 4 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X7 is covered by 'TC-E1-007-10', not by a criterion; exception X11 is covered by 'TC-E1-007-09', not by a criterion; §7 holds 6 owned criteria in Gherkin; §5 has 12 exception paths | — |
| 4 | Business rules | Partial | 3 of 13 rules are covered by no criterion and no test case: BR11, BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 10 transitions | — |
| 6 | Authority | Pass | §10 has 10 roles | — |
| 7 | Data | Partial | §11 has 26 data rows; detcheck: P2 Name `recovery_svc` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `interface_run` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `interface_signoff` is not a field or entity in LDM v9 or Data Classification v5; P2 Criteria and test data read ACE views directly (+1 more) | CG-ALL-2937, CG-ALL-2938, CG-ALL-2939, CG-ALL-2962, CG-ALL-2963 |
| 8 | Contract | Fail | detcheck: P1 GET /api/recovery/source-data/v1/freshness is not published by rwb-source-data; P1 GET /api/recovery/source-data/v1/customers/{id} is not published by rwb-source-data; P1 GET /api/recovery/source-data/v1/accounts/{id} is not published by rwb-source-data; P1 POST /api/recovery/document/v1/documents is not published by rwb-document (+11 more) | CG-ALL-2940, CG-ALL-2941, CG-ALL-2942, CG-ALL-2943, CG-ALL-2944, CG-ALL-2945, CG-ALL-2946, CG-ALL-2947, CG-ALL-2948, CG-ALL-2949, CG-ALL-2950, CG-ALL-2951 (+3) |
| 9 | Messages | Partial | §14 lists 8 messages; detcheck: P3 MSG-P1-001 text differs from the Error and Message Standard v4; P2 MSG-P2-001 text differs from the Error and Message Standard v4; P3 MSG-P4-003 text differs from the Error and Message Standard v4 | CG-ALL-2955, CG-ALL-2956, CG-ALL-2957 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-09 has no empty, loading, error, no access state in the story | CG-ALL-2964 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-2961 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 10 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-2958, CG-ALL-2959, CG-ALL-2960 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P2-E1007-INF, RWB-P2-E1007-OPS); 10 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL06 (assumptions: ASM-0189, ASM-2559, ASM-2608, ASM-2776) | — |
| 19 | Test data | Pass | every test case in §16 names its data (10) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P2-E1007-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2940 | GET /api/recovery/source-data/v1/freshness is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-2941 | GET /api/recovery/source-data/v1/customers/{id} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-2942 | GET /api/recovery/source-data/v1/accounts/{id} is not published by rwb-source-data | X5 | Missing | Solution architect |
| CG-ALL-2943 | POST /api/recovery/document/v1/documents is not published by rwb-document | X5 | Missing | Solution architect |
| CG-ALL-2944 | POST /api/recovery/case/v1/cases/{caseId}/actions is not published by rwb-case | X5 | Missing | Solution architect |
| CG-ALL-2945 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-2950 | Workflow OutboundFileWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 14 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2937 | Name `recovery_svc` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2938 | Name `interface_run` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2939 | Name `interface_signoff` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-2946 | Payload of rwb.integration.FileDelivered.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-2947 | Payload of rwb.integration.FileFailed.v1 differs from Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-2948 | rwb-integration is not a consumer of rwb.source-data.AceDataReady.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |
| CG-ALL-2949 | Activity deliverFile(manifest) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2951 | Activity buildOutboundFile is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2952 | Activity storeOutboundFile is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2953 | Activity sendFileOverMft is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2954 | Activity parkItemInException is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-2956 | MSG-P2-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2961 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-2962 | Criteria and test data read ACE views directly | X12 | Outdated | QA |

### R3.3 Minor (P3) — 8 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-2955 | MSG-P1-001 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2957 | MSG-P4-003 text differs from the Error and Message Standard v4 | X8 | Conflict | Business analyst |
| CG-ALL-2958 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-2959 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-2960 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-2963 | Criteria and tests keep legacy job and decision-log wording | X12 | Outdated | QA |
| CG-ALL-2964 | SCR-09 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-2965 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | §5 X7: A role without the Platform administration right lists or resends exception items (covered by 'TC-E1-007-10' only) | Not specified in the source documents | |
| AC9 | §5 X11: A resend names an item that is not in EXCEPTION, or the item version changed (covered by 'TC-E1-007-09' only) | Not specified in the source documents | |
| AC10 | §8 BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC12 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC13 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

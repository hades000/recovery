# Build-readiness review (script) — RWB-P2-E2034-APP Interaction ledger on the case and from every channel

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P2-E2034-APP (RWB P2 E2034 APP Interaction ledger on the case and from every channel v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-integration |
| Legacy key | RWB-E2-034 |

## R1. Verdict

**NOT READY.** Checklist: Pass 9, Partial 10, Fail 6. Detcheck rows: 22 (3 P1). AC review rows: 0. Missing criteria: 8.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'platform operator of the channel intake (RW-PLATADM on call)' is in the roles table | — |
| 2 | Links | Pass | §18 has 9 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X6 is covered by 'BR4', not by a criterion; exception X8 is covered by 'BR2', not by a criterion; exception X9 is covered by 'Carried by the CON story as a contract case', not by a criterion; exception X10 is covered by 'BR6', not by a criterion; §7 holds 1 owned criteria in Gherkin; §5 has 11 exception paths | — |
| 4 | Business rules | Partial | 1 of 10 rules are covered by no criterion and no test case: BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 7 transitions | — |
| 6 | Authority | Partial | role SY-INTGR in §10 is not in Users Roles and Permissions v5; §10 has 7 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-INT-036; §11 has 13 data rows; detcheck: P2 Name `tr_interaction_append_only` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-3205, CG-ALL-3206 |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P1 Workflow LedgerChannelIntakeWorkflow is not in Temporal Catalog v1; P2 Activity mapChannelEvent is not in Temporal Catalog v1; P2 Activity resolveChannelFacts is not in Temporal Catalog v1 (+6 more) | CG-ALL-3207, CG-ALL-3208, CG-ALL-3209, CG-ALL-3210, CG-ALL-3211, CG-ALL-3212, CG-ALL-3213, CG-ALL-3214, CG-ALL-3215, CG-ALL-3216 |
| 9 | Messages | Partial | §14 lists 4 messages; detcheck: P2 MSG-P2-001 is used with another meaning than the standard's; P2 MSG-GEN-005 is used with another meaning than the standard's | CG-ALL-3217, CG-ALL-3218 |
| 10 | Screens and states | Partial | detcheck: P3 SCR-04 has no empty, loading, error, no access state in the story; P3 SCR-09 has no empty, loading, error, no access state in the story | CG-ALL-3223, CG-ALL-3224 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-3221 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P3 Test cases listed for criteria this story does not own; P3 §18 test lists differ from RTM v7 | CG-ALL-3219, CG-ALL-3220 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P2-E1007-APP, RWB-P2-E2034-OPS); 18 dependencies named | — |
| 18 | Open decisions | Partial | open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355); open decision DL29 (assumptions: none); detcheck: P2 Open decision DL29 has no assumption | CG-ALL-3226 |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P2-E2034-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P2-E1007-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3207 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-3208 | Workflow LedgerChannelIntakeWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3213 | Workflow EfsLedgerReadWorkflow is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.2 Major (P2) — 13 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3205 | Name `tr_interaction_append_only` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3206 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-3209 | Activity mapChannelEvent is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3210 | Activity resolveChannelFacts is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3211 | Activity appendLedgerEntry is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3212 | Activity parkDeliveryInException is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3214 | Activity readEfsOutcomes is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3215 | Activity appendEfsEntries is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3216 | Activity writeEfsReadSummary is not in Temporal Catalog v1 | X6 | Missing | Solution architect |
| CG-ALL-3217 | MSG-P2-001 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-3218 | MSG-GEN-005 is used with another meaning than the standard's | X8 | ID collision | Business analyst |
| CG-ALL-3221 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |
| CG-ALL-3226 | Open decision DL29 has no assumption | X2 | Ambiguous | Product owner |

### R3.3 Minor (P3) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-3219 | Test cases listed for criteria this story does not own | X9 | Missing | QA |
| CG-ALL-3220 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-3222 | Flyway file V2034_1__ledger_intake.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-3223 | SCR-04 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3224 | SCR-09 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-3225 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §5 X6: A fact read answers 404 (covered by 'BR4' only) | Not specified in the source documents | |
| AC13 | §5 X8: A message fails envelope validation, or carries a type this consumer does not declare (covered by 'BR2' only) | Not specified in the source documents | |
| AC14 | §5 X9: A role without Platform administration opens the exception queue or resends (covered by 'Carried by the CON story as a contract case' only) | Not specified in the source documents | |
| AC15 | §5 X10: The delivery is resent while the workflow for the same event is running (covered by 'BR6' only) | Not specified in the source documents | |
| AC16 | §8 BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC17 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC18 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC19 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

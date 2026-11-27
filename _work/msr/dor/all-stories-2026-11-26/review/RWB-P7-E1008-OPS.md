# Build-readiness review (script) — RWB-P7-E1008-OPS Decision log store v1, append only and hash chained - deployment

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P7-E1008-OPS (RWB P7 E1008 OPS Decision log store v1, append only and hash chained - deployment v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-decision |
| Legacy key | RWB-E1-008 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 10 (1 P1). AC review rows: 0. Missing criteria: 3.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'DevOps engineer of the platform' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 13 traceability rows | — |
| 3 | Acceptance criteria | Pass | §7 holds 8 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 10 of 10 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 10 transitions | — |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Partial | §11 has no data table; detcheck: P2 Name `flyway_schema_history` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `ce_id` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `ce_type` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `tr_declog_append_only` is not a field or entity in LDM v9 or Data Classification v5 (+1 more) | CG-ALL-6859, CG-ALL-6860, CG-ALL-6861, CG-ALL-6862, CG-ALL-6863 |
| 8 | Contract | Fail | detcheck: P1 rwb.decision.DecisionRecorded.v1 is on topic rwb.decision-record.v1 in the catalog, not rwb.decision-record.v1 (shared topic) | CG-ALL-6864 |
| 9 | Messages | Partial | messages used but not listed in §14: MSG-P7-009; §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-44 has no empty, loading, error, no access state in the story | CG-ALL-6868 |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-6867 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; §16 has 8 test cases; detcheck: P3 Test cases not in Test Cases v8: TC-P7-E1008-OPS-01, TC-P7-E1008-OPS-02, TC-P7-E1008-OPS-03, TC-P7-E1008-OPS-04, TC-P7-E1008-OPS-05, TC-P7-E1008-OPS-06, TC-P7-E1008-OPS-07, TC-P7-E1008-OPS-08; P3 §18 test lists differ from RTM v7 | CG-ALL-6865, CG-ALL-6866 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 0 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863); open decision DL26 (assumptions: ASM-0247, ASM-0264, ASM-0275, ASM-0355) | — |
| 19 | Test data | Pass | every test case in §16 names its data (8) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P7-E1008-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake named in §12.8 for rwb-source-data; no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Partial | §12.4 has no owner or service column | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 1 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6864 | rwb.decision.DecisionRecorded.v1 is on topic rwb.decision-record.v1 in the catalog, not rwb.decision-record.v1 (shared topic) | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6859 | Name `flyway_schema_history` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6860 | Name `ce_id` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6861 | Name `ce_type` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6862 | Name `tr_declog_append_only` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6863 | Name `refuse_change` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6867 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6865 | Test cases not in Test Cases v8: TC-P7-E1008-OPS-01, TC-P7-E1008-OPS-02, TC-P7-E1008-OPS-03, TC-P7-E1008-OPS-04, TC-P7-E1008-OPS-05, TC-P7-E1008-OPS-06, TC-P7-E1008-OPS-07, TC-P7-E1008-OPS-08 | X9 | Missing | QA |
| CG-ALL-6866 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-6868 | SCR-44 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC9. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC9 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC10 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |
| AC11 | a status change the model does not allow is refused (no criterion covers a disallowed transition) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

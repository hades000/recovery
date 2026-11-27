# Build-readiness review (script) — RWB-P7-E1027-APP Decision log writer v1

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-P7-E1027-APP (RWB P7 E1027 APP Decision log writer v1 v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-decision |
| Legacy key | RWB-E1-027 |

## R1. Verdict

**NOT READY.** Checklist: Pass 10, Partial 9, Fail 6. Detcheck rows: 7 (2 P1). AC review rows: 0. Missing criteria: 5.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Partial | §1 role 'caller that takes a decision — rwb-case for case created, owner assigned and case transferred, rwb-document for document attached, and rwb-decision itself for the decisions it takes — and as the owner of the writer that is the reference implementation of the shared library' is not a role code or role name in Users Roles and Permissions v5 | — |
| 2 | Links | Pass | §18 has 22 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X8 is covered by 'BR4, section 16 TC-E1-027-02', not by a criterion; exception X9 is covered by 'TC-E1-027-08', not by a criterion; §7 holds 7 owned criteria in Gherkin; §5 has 9 exception paths | — |
| 4 | Business rules | Partial | 7 of 13 rules are covered by no criterion and no test case: BR4, BR8, BR9, BR10, BR11, BR12, BR13; §8 has 13 rules | — |
| 5 | State transitions | Pass | §9 has 9 transitions | — |
| 6 | Authority | Pass | §10 has 8 roles | — |
| 7 | Data | Partial | §11 has 9 data rows; detcheck: P2 Name `uk_declog_idempotency` is not a field or entity in LDM v9 or Data Classification v5 | CG-ALL-6917 |
| 8 | Contract | Fail | detcheck: P1 rwb-decision.yaml holds approvalLevel as a closed enum while the story reads LOV-APPROVAL-LEVEL as data; P1 Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | CG-ALL-6918, CG-ALL-6919 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Pass | — | — |
| 11 | Guardrails | Partial | detcheck: P2 Fields classed as personal data where the story says none is carried | CG-ALL-6921 |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 9 test cases; detcheck: P3 §18 test lists differ from RTM v7 | CG-ALL-6920 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Partial | INVEST 'Small' does not say it fits two weeks | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Partial | 2 build dependencies are not done yet (RWB-P7-E1008-APP, RWB-PLT-E1056-OPS); 12 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (9) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | the contract story RWB-P7-E1027-CON exists; its build status is 'Not started', not Done | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: After RWB-P7-E1008-APP | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6918 | rwb-decision.yaml holds approvalLevel as a closed enum while the story reads LOV-APPROVAL-LEVEL as data | X5 | Conflict | Solution architect |
| CG-ALL-6919 | Event type rwb.decision-record.DecisionRecorded.v1 is rwb.decision.DecisionRecorded.v1 in Kafka Catalog v1 | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 2 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6917 | Name `uk_declog_idempotency` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-6921 | Fields classed as personal data where the story says none is carried | X10 | Conflict | Compliance |

### R3.3 Minor (P3) — 3 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-6920 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-6922 | Flyway file V_E1027__declog_idempotency.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-6923 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC8. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC8 | §5 X8: A record carries an approver without an approval level (covered by 'BR4, section 16 TC-E1-027-02' only) | Not specified in the source documents | |
| AC9 | §5 X9: A caller outside the right of the capability area calls the writer through an operation (covered by 'TC-E1-027-08' only) | Not specified in the source documents | |
| AC10 | §8 BR4, BR8, BR9, BR10, BR11, BR12, BR13 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC11 | error answers 401, 403, 404 of the provided operations (no criterion names these status codes) | Not specified in the source documents | |
| AC12 | activity retry and timeout (no criterion covers a retried or timed-out activity) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

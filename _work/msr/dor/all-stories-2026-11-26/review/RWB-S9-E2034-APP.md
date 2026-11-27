# Build-readiness review (script) — RWB-S9-E2034-APP Interaction ledger on the case and from every channel

SCB Collections and Recovery. Henka Group.

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

| Item | Value |
|---|---|
| Story reviewed | RWB-S9-E2034-APP (RWB S9 E2034 APP Interaction ledger on the case and from every channel v1.md) |
| Review kind | Script checks only: Recovery Workbench Definition of Ready and Done v4 section 2, AC structure, missing-criterion types, detcheck X1-X20 |
| Service | rwb-partner |
| Legacy key | RWB-E2-034 |

## R1. Verdict

**NOT READY.** Checklist: Pass 11, Partial 8, Fail 6. Detcheck rows: 17 (4 P1). AC review rows: 0. Missing criteria: 4.

On the story text alone (items 14, 16, 21, 22, 23 left out, they need records the story files do not hold): **NOT READY**.

Failed items: 8 Contract; 14 Epic design; 16 Size; 21 Contract published; 22 Fake published; 23 Contract version fixed.

## R2. Definition of ready — every item of Recovery Workbench Definition of Ready and Done v4 section 2

| # | Item | Result | Evidence (story section + document checked) | Gap |
|---|---|---|---|---|
| 1 | Story | Pass | §1 role 'case owner (RW-CASEOWN)' is in the roles table | — |
| 2 | Links | Partial | §18 has no feature column; §18 has no L3 process column; §18 has 18 traceability rows | — |
| 3 | Acceptance criteria | Partial | exception X4 is covered by 'Section 14', not by a criterion; exception X7 is covered by 'Section 17', not by a criterion; §7 holds 6 owned criteria in Gherkin; §5 has 7 exception paths | — |
| 4 | Business rules | Partial | 10 of 10 rules are covered by no criterion and no test case: BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10; §8 has 10 rules | — |
| 5 | State transitions | Pass | §9 has 5 transitions | — |
| 6 | Authority | Partial | role SY-PARTNER in §10 is not in Users Roles and Permissions v5; §10 has 9 roles | — |
| 7 | Data | Partial | BR Field IDs not in LDM v9: DF-INT-036; §11 has 12 data rows; detcheck: P2 Name `v_partner_ledger_fact` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5; P2 Name `recovery_svc` is not a field or entity in LDM v9 or Data Classification v5; P2 Field IDs DF-INT-001 to DF-INT-036 are not all fields of interaction in LDM v9 | CG-ALL-11763, CG-ALL-11764, CG-ALL-11765, CG-ALL-11766 |
| 8 | Contract | Fail | detcheck: P1 POST /api/recovery/access/v1/authorise is not published by rwb-access; P1 rwb.partner.InstructionIssued.v1 is on topic rwb.partner.events.v1 in the catalog, not rwb.partner.events.v1`, with its retry and `.dlt` topics; P1 rwb.partner.PartnerResultSubmitted.v1 is on topic rwb.partner.events.v1 in the catalog, not rwb.partner.events.v1`, with its retry and `.dlt` topics; P1 Workflow InstructionWorkflow task queue rwb-partner`, namespace `rwb-recovery differs from the catalog (+2 more) | CG-ALL-11767, CG-ALL-11768, CG-ALL-11769, CG-ALL-11770, CG-ALL-11771, CG-ALL-11772 |
| 9 | Messages | Pass | §14 lists 4 messages | — |
| 10 | Screens and states | Partial | detcheck: P3 SCR-04 has no empty, loading, error, no access state in the story; P3 SCR-34 has no empty, loading, error, no access state in the story; P3 SCR-35 has no empty, loading, error, no access state in the story | CG-ALL-11776, CG-ALL-11777, CG-ALL-11778 |
| 11 | Guardrails | Pass | — | — |
| 12 | Test cases | Partial | no contract test for the operations, events and activities of §12; no boundary test for the tables of §12.7 (ASM-3438); §16 has 12 test cases; detcheck: P3 Test cases cover other criteria in Test Cases v8; P3 §18 test lists differ from RTM v7 | CG-ALL-11773, CG-ALL-11774 |
| 13 | Out of scope | Pass | — | — |
| 14 | Epic design | Fail | no signed epic design is recorded in the story or the source documents; confirm the sign-off with the epic design record | — |
| 15 | INVEST | Pass | — | — |
| 16 | Size | Fail | the story carries no size; the squad sizes it at refinement | — |
| 17 | Dependencies | Pass | 1 dependencies named | — |
| 18 | Open decisions | Partial | open decisions apply; each has an assumption, the decision is still open; open decision DL10 (assumptions: ASM-2250, ASM-2357, ASM-2377, ASM-2863) | — |
| 19 | Test data | Pass | every test case in §16 names its data (12) | — |
| 20 | Reference data | Pass | — | — |
| 21 | Contract published | Fail | no contract story RWB-S9-E2034-CON and no CON dependency | — |
| 22 | Fake published | Fail | no contract fake library version is recorded as published | — |
| 23 | Contract version fixed | Fail | the story states no contract version it builds against (only the /v1 path) | — |
| 24 | Ownership stated | Pass | — | — |
| 25 | Ready to start | Pass | Ready to start: Day 1 | — |

## R3. Gap list (detcheck rows of this story)

### R3.1 Blockers (P1) — 4 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11767 | POST /api/recovery/access/v1/authorise is not published by rwb-access | X5 | Missing | Solution architect |
| CG-ALL-11768 | rwb.partner.InstructionIssued.v1 is on topic rwb.partner.events.v1 in the catalog, not rwb.partner.events.v1`, with its retry and `.dlt` topics | X6 | Conflict | Solution architect |
| CG-ALL-11769 | rwb.partner.PartnerResultSubmitted.v1 is on topic rwb.partner.events.v1 in the catalog, not rwb.partner.events.v1`, with its retry and `.dlt` topics | X6 | Conflict | Solution architect |
| CG-ALL-11770 | Workflow InstructionWorkflow task queue rwb-partner`, namespace `rwb-recovery differs from the catalog | X6 | Conflict | Solution architect |

### R3.2 Major (P2) — 6 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11763 | Name `v_partner_ledger_fact` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11764 | Name `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11765 | Name `recovery_svc` is not a field or entity in LDM v9 or Data Classification v5 | X3 | Missing | Data |
| CG-ALL-11766 | Field IDs DF-INT-001 to DF-INT-036 are not all fields of interaction in LDM v9 | X3 | Conflict | Data |
| CG-ALL-11771 | Workflow ID form and start rule of InstructionWorkflow are not stated | X6 | Missing | Solution architect |
| CG-ALL-11772 | Activity writeLedgerFact` (name is this story's design choice) is not in Temporal Catalog v1 | X6 | Missing | Solution architect |

### R3.3 Minor (P3) — 7 rows

| CG id | Title | Check | Gap type | Owner role |
|---|---|---|---|---|
| CG-ALL-11773 | Test cases cover other criteria in Test Cases v8 | X9 | Conflict | QA |
| CG-ALL-11774 | §18 test lists differ from RTM v7 | X9 | Conflict | QA |
| CG-ALL-11775 | Flyway file V2034_1__partner_ledger_fact.sql is not in the V0001..Vnnnn form | X11 | Conflict | Solution architect |
| CG-ALL-11776 | SCR-04 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11777 | SCR-34 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11778 | SCR-35 has no empty, loading, error, no access state in the story | X17 | Missing | Business analyst |
| CG-ALL-11779 | Story cites document versions that are not the highest | X20 | Outdated | Business analyst |

## R4. AC review — structural problems of the owned criteria

| AC | Problem | Improved Given / When / Then (model pass) |
|---|---|---|

## R5. Missing acceptance criteria

Proposed AC IDs start at AC12. The Gherkin is written in the model pass from the sources; the script names only what has no criterion.

| Proposed AC | Covers | Proposed TC (proposed) | Gherkin |
|---|---|---|---|
| AC12 | §5 X4: The list or the parameter read misses the 2 s budget, or its breaker is open (covered by 'Section 14' only) | Not specified in the source documents | |
| AC13 | §5 X7: A component or a test reaches `interaction`, `recovery_case`, the ACE views or another `rwb_*` schema (covered by 'Section 17' only) | Not specified in the source documents | |
| AC14 | §8 BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10 (these rules have no criterion and no test; a rule that is an architecture constraint may belong in a guardrail or boundary test instead) | Not specified in the source documents | |
| AC15 | a consumed call fails or does not answer (no criterion covers a failed call) | Not specified in the source documents | |

## R7. Assumptions and limits

- Script review only. Not judged here: whether a criterion is correct or testable as written, the meaning of a rule, conflicts of meaning across documents, NFR behaviour (scale, retries, caching), open questions, and the wording of improved or missing criteria. Run the model review for those.
- Items 14, 16, 21, 22 and 23 read records the story files do not hold (epic design sign-off, size, build status, fake library, contract version); a Fail there is a missing record, not a defect in the text.
- Missing-criterion types are found by keywords in §7; a criterion worded differently can be missed or reported falsely. Confirm each R5 row.

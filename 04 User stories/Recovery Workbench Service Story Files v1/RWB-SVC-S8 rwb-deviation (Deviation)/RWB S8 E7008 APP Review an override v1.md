# RWB-S8-E7008-APP Review an override

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E7008-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 4 |
| Business epic | EP07 |
| Release | 31 May 2027 (tentative) |
| Legacy key | RWB-E7-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-S8-S |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S8-E7008-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the override-review slice of RWB-E7-008 in rwb-deviation. The two legacy criteria are kept word for word with their origin tag; the step reads the open deviations of a case at `DEV_WITH_OWNER`, records the forum's outcome and its reason on `deviation` (DF-CAS-045), moves the deviation on R-DEV-09, R-DEV-10 and R-DEV-22, writes the local decision record with the rule ID and the package version in force before any change (DP-03), and serves the review branch of the published `PATCH /deviations/{deviationId}` (API-S8-002) on base `/api/recovery/deviation/v1` (DP-13), reached from SCR-08 Deviation queue through the gateway-bff composite route (DP-19). No source defines the override as a record of S8 or gives the reason a field, no rule row names the review forum, no requirement row traces to FEAT-DVF-08, the plan's C row is empty while the package read is consumed, the S8 row of the connection matrix carries no P7 edge, and the primary role holds R on the case record while the review needs U (GAP-3066; ASM-5202, ASM-5203, ASM-5204, ASM-5205, ASM-5207, ASM-5210). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **risk and model risk officer**, I want **to put overrides in front of the review forum, with the reason and the outcome of each**, so that **every deviation has a handler and a clock**.

This is the override-review slice of legacy RWB-E7-008. It owns:

- the two legacy criteria this story owns (AC1, AC2), copied verbatim with their origin tag, and the operation, the messages and the screen they depend on;
- one step of `DeviationWorkflow` on task queue `rwb-deviation` in namespace `rwb-recovery`, the deviation stage that can start at any time on a case and pauses the stage clock (context pack, Temporal and Drools slide 13);
- the review of the open deviations of a case: each one is presented with its code, its raise facts, its paused state and its named handler, and the forum records its outcome and its reason on the deviation row (FSD S8 A2.17.2; TSD S8 T3.1);
- the evaluation of the DEVIATION rows that fire on the recorded outcome — R-DEV-09, R-DEV-10 and R-DEV-22 — over the package version in force (TSD S8 T4; Business Rules and Routing Logic v4);
- the local decision record of the review, written through RWB-PLT-E1027-CON with the rule ID, the package version, the reason and the outcome, **before any change** (DP-03);
- the review branch of the published `PATCH /deviations/{deviationId}` (API-S8-002) on base `/api/recovery/deviation/v1`, case-record right U, scope applied (DP-13);
- the review panel of SCR-08 Deviation queue behind the gateway-bff composite route (DP-19).

It does not own: the published shapes of the two operations, the `Deviation` and `DeviationOutcome` elements, the review properties, the consumed row, the error set, the rights of the document and the fakes, which are RWB-S8-E7008-CON; raising a deviation (API-S8-001, RWB-E1-062, FEAT-DVH-01); pausing the stage clock and keeping the prescription clock running (FEAT-DVH-02, FEAT-DVH-03, R-DEV-01); routing a deviation to its named owner (FEAT-DVH-04, R-DEV-02 to R-DEV-06, R-DEV-21); clearing a deviation, lifting the contact stop, writing `cleared_at` and resuming the timers (FEAT-DVH-06, R-DEV-18); reopening the route decision (R-DEV-19); the X1 to X7 journeys and the breach path (RWB-S8-E7001-APP to RWB-S8-E7007-APP, RWB-S8-E7010-APP); the case of record, its states and the parent workflow, which are rwb-case (P3); the DEVIATION package and its 22 rules, which are rwb-decision (P7); and the deployment of this build, which is the operations story of this legacy key.

### 2. Business rationale

The feature objective, the problem and the metric are unchanged from the legacy story and the module FSD: overrides go in front of the review forum with the reason and the outcome of each, because complaints, hardship, death, fraud, bankruptcy, lost contact and collateral events are handled case by case with no clock (FSD S8 A1.3, A2.17.1), and the deviations closed within the service level are measured on the decision log and the Workbench records against a target set with DL22, reviewed monthly (FSD S8 A2.17.1). What D-RCV-60 changes is who owns the record, the rule, the decision and the screen.

- **The reviewed record is this service's.** `deviation` is S8's only table in `rwb_deviation` (context pack ownership rows; TSD S8 T3.1), and the DEVIATION route set of 22 rules over 9 states is the deviation stage's (TSD S8 T4). No source defines a separate override entity, and the FSD field catalog of A2.17.3.2 lists the deviation fields only, so the override the forum reviews is the open deviation of the case (GAP-3066; ASM-5202).
- **The outcome is a published list.** LOV-DEV-OUTCOME holds `RETURNED`, `RE_ROUTED` and `CASE_ENDED` (TSD S8 T3.2) and the request element carries it (API Specification v4 `DeviationOutcome`); the legacy "outcome of each" is recorded on DF-CAS-045 and never invented (ASM-5203).
- **The reason has no field of its own.** `DeviationOutcome` carries `outcome` and `note`, the FSD names no reason field, and no column of `deviation` carries one, so the forum's reason rides `note` and the local decision record (GAP-3066; ASM-5203).
- **Three rows fire, not four.** On `DEVIATION_RESOLVED` the set gives R-DEV-09 (`X1`, `X7`), R-DEV-10 (`X2`) and R-DEV-22 (an outcome that names no next step); R-DEV-11 reaches `CASE_ENDED` on `INSURANCE_SETTLED` and belongs to the X3 path (ASM-5205).
- **The review records an outcome, it does not clear.** `cleared_at`, the contact stop and the resumption of the stage clock are FEAT-DVH-06, whose outcome recording is the clearance step of the stage; this story ends at the recorded outcome and the rule-driven state move (GAP-3066; ASM-5205).
- **The package is read, not embedded.** The DEVIATION set is governed in rwb-decision, DP-04 is not in this key's pattern set, and the S8 row of the connection matrix carries no P7 edge, so the version in force arrives on a read with a fake and the kit rows are recorded as absent (GAP-3066; ASM-5204).
- **The case stays with rwb-case.** The deviation row holds `case_id` and the paused state; the stage outcome returns to the parent `CaseWorkflow`, which owns the case, the clock and the route (ASM-5205, ASM-5206).
- **The forum's right is short.** FSD S8 A2.17.3.3 names the Risk and model risk officer as primary and TSD S8 T6.1 gives RW-RISK R on the case record, while both operations declare right U; the right is taken over the operation matrix and the conflict is recorded rather than resolved by a new grant (GAP-3066; ASM-5207).
- **No requirement row names the feature.** TSD S8 T8 maps every REQ-DVH and REQ-S8 row to FEAT-DVH-01, FEAT-DVF-01 or a placeholder, and none names FEAT-DVF-08, so the story cites no requirement ID until the E7 BRD and the PRD publish one (GAP-3066; ASM-5210).

No business value moves: the outcome values, the deviation states, the rule IDs, the package version and the right are values of reference data and of the rule package, read with their version and never written in code.

### 3. Preconditions

- RWB-S8-E7008-CON is published: the review branch of `PATCH /deviations/{deviationId}` with the `DeviationOutcome` request and the `Deviation` answer, the review properties, the consumed row, the rights, the error set and the fakes are baselined and handed to this story.
- The rwb-decision rule-package read is published with its fake and answers the DEVIATION package at its version in force, with R-DEV-01 to R-DEV-22 over its 9 states. The operation name is Not specified in the source documents (GAP-3066; ASM-5204).
- RWB-PLT-E1027-CON is published with its writer fake: the local decision-record library writes in the caller's transaction, and a failed write stops the action with MSG-P7-003, so nothing changes (DP-03).
- RWB-PLT-N001-CON is published: SCR-08 Deviation queue reaches this service through the gateway-bff composite route, one hop, and no screen calls a service directly (DP-19).
- `deviation` exists in schema `rwb_deviation` from the DB story of this service, with the columns of DF-CAS-036 to DF-CAS-045 and the standard record columns of TSD S8 T3.0; this story adds no table, no column and no migration, and writes `outcome`, `state` and the standard columns only.
- The case is in place: at least one deviation of the case is open at `DEV_WITH_OWNER` with its handler set by the routing step (FEAT-DVH-04, R-DEV-02 to R-DEV-06), and the stage clock is paused (R-DEV-01). This story reads that state and moves it no further than the outcome rows allow.
- The DEVIATION package is in force at its version; the rule rows, the outcome list and the states are governed in rwb-decision and are not a build item of this story.
- The service runs as its own login on schema `rwb_deviation`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `rwb_case` or on an ACE view is refused by the database and fails the boundary test.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S8-E7008-CON when its tests pass.

### 4. Flow

1. A deviation of the case is open at `DEV_WITH_OWNER` with the handler the routing step named (FEAT-DVH-04); the deviation stage runs as the child of `CaseWorkflow` on `rwb-deviation` and can start at any time on a case (context pack, Temporal and Drools slide 13).
2. The risk and model risk officer opens SCR-08 Deviation queue through the gateway-bff composite route, one hop, and reads the open deviations of the case with their codes, their raise facts, their handlers and their ages (DP-19).
3. The officer selects one deviation, records the forum's outcome and its reason, and confirms. The screen sends the deviation reference, the outcome, the reason and the member's identity (FSD S8 A2.17.2); the operation declares no `Idempotency-Key` header (TSD S8 T-A.2).
4. `DeviationReviewController` serves the review branch of `PATCH /deviations/{deviationId}` (API-S8-002) on base `/api/recovery/deviation/v1`, declares case-record right U with the scope applied and validates the request (DP-13).
5. The service reads the deviation row in `rwb_deviation`: its reference, its case, its code, its from state, its paused state, its handler and its current outcome. A deviation that is not open at `DEV_WITH_OWNER` is refused with 409 and nothing is written.
6. The service reads the DEVIATION package in force on the rwb-decision contract and holds its version for the record; the package read is one hop with a 2 s budget and a breaker (ASM-5204).
7. `DeviationOutcomeEvaluator` evaluates the `DEVIATION_RESOLVED` rows of the package over the deviation: `X1` and `X7` fire R-DEV-09 and give `DEV_RESOLVED`; `X2` fires R-DEV-10 and gives `DEV_REROUTE`; any outcome that names no next step fires R-DEV-22 and gives `DEV_REROUTE`. The condition is a rule of the package in force and never a branch of the code (ASM-5205).
8. `DeviationDecisionRecordWriter` writes one decision record through the local decision-record library, **before any change**: the case reference, the deviation reference and code, the rule ID that fired, the package version in force, the reason, the outcome, the from state, the to state and the decided-at time. A failed write stops the step with nothing changed (DP-03; AC1, AC2).
9. `RecordAndApply` writes in one transaction: `outcome` (DF-CAS-045), the deviation `state` the rule gives and the standard columns `updated_at` and `updated_by`. `cleared_at`, `contact_stop` and the timers are not touched (ASM-5205).
10. The answer returns the deviation element with its outcome, its state and the decision-record reference; the officer sees the recorded outcome on SCR-08, read back from this service (DP-19).
11. The stage outcome returns to the parent `CaseWorkflow`: the deviation state and the outcome. The parent owns the clock and the route, so the resume of R-DEV-18 and the reopen of R-DEV-19 are its steps and the clearance stories', not this one (ASM-5205, ASM-5206).
12. A repeat of the same review answers the record that exists and writes no second one, matched on the deviation reference and the outcome. No phone number, address, identity number or other personal value is copied into the record, the answer or a log.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written | Nothing changes: no outcome is recorded and the deviation stays where it was, with no record | MSG-P7-003 | AC2, TC-E7-008-02, TC-E7-008-04 |
| X2 | The role does not hold the case record right U | 403 before any read or write; nothing changes and no record is written | MSG-P4-002 | TC-E7-008-03 |
| X3 | The deviation is not open at `DEV_WITH_OWNER`, is not on that case, or the outcome is absent | 409 or 422 with nothing written; an outcome is never recorded on a deviation the forum cannot see | MSG-GEN-001 | AC1, X7 |
| X4 | The outcome is not one of LOV-DEV-OUTCOME | 422 with nothing written; the value stays the list's and never the code's | MSG-GEN-001 | AC1 |
| X5 | The rwb-decision package read does not answer inside 2 s, or its breaker is open | The step retries on the workflow's own schedule; nothing is written; the caller sees 503 with the platform error envelope | None | AC1, X2 |
| X6 | The outcome is `CASE_ENDED` | Recorded on the deviation, and no case is closed here: R-DEV-11 closes on `INSURANCE_SETTLED` and belongs to the X3 path | None | AC1, X8 |
| X7 | A repeated request for the same deviation and outcome | One record and one answer; the repeat answers the record that exists and is counted | None | AC1 |
| X8 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR5, BR8 |

X1 and X2 are the legacy exception paths carried onto the slice (the legacy set also carries MSG-GEN-001 and MSG-S8-001, kept in section 14), X3 to X7 are the paths the target call types and the interactive trigger add, and X8 is the ACE and schema boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against RWB-S8-E7008-CON, the rwb-decision package fake and the decision-record stub, on its own schema, and needs no live P3 or P7 |
| Negotiable | The activity name, the record's internal shape and the front-end component are this story's and the baseline's choice; the operation, the right, the outcome list, the messages, the screen and the two criteria are fixed |
| Valuable | Every reviewed override carries the forum's outcome and its reason with the rule ID and the package version that were in force, instead of an outcome known only to the forum |
| Estimable | One workflow step, one evaluator, one record write, one operation branch, one client and one read-only screen state |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on a synthetic open deviation through the contract fakes, plus the access, not-open, bad-outcome and failed-record cases |

### 7. Acceptance criteria

```gherkin
Feature: Review an override

  Background:
    Given case "RW-2026-000502" has the deviation "X3" open at state "DEV_WITH_OWNER" with the specialist as its handler and paused state "WITH_FCR_OFFICER"
    Given the DEVIATION rule package is in force at its version and carries R-DEV-01 to R-DEV-22
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 Review an override (legacy RWB-E7-008 AC1)
    Given the rwb-decision contract mock returns the rule version in force
    Given the data and the rule version this feature needs are in place
    When the user acts on the screen
    Then puts overrides in front of the review forum, with the reason and the outcome of each
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E7-008 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

The two criteria are the legacy criteria of RWB-E7-008 word for word, with their origin tag added and nothing else changed: the repeated `Then`, the wording of `the user acts on the screen`, `the action is taken` and `the decision log cannot be written` all stand. The cross-service part of AC1 is the rule version, so AC1 carries one `Given the rwb-decision contract mock returns the rule version in force` line and that is the only addition. AC2 has no cross-service part and is copied with nothing added. The same outcome is the one FSD S8 AC-S8-017-01 records as written one epic ahead — "The data and rules it needs are in place / The user acts / The result is recorded with its rule version" — so the legacy line and the module line agree. The `decision log` of the legacy text is the local decision record of DP-03 in `rwb_deviation`, with the central `decision_log_entry` ledger of rwb-decision behind it.

### 8. Business rules

The review is the step that emits `DEVIATION_RESOLVED`; the rows below are the three of the 22-row DEVIATION set that fire on it, copied character for character, plus the row that reaches `CASE_ENDED` and is **not** fired here (Business Rules and Routing Logic v4, Rules sheet; TSD S8 T4).

| Rule | Route set | Decision | From state | Event | Condition | Action | To state | Owner | Systems | Timer |
|---|---|---|---|---|---|---|---|---|---|---|
| R-DEV-09 | Deviations | X1 to X7 | DEV_WITH_OWNER | DEVIATION_RESOLVED | deviation_code in (X1,X7) | Record the outcome; the same decision resumes | DEV_RESOLVED | Case owner | Workbench | None |
| R-DEV-10 | Deviations | X1 to X7 | DEV_WITH_OWNER | DEVIATION_RESOLVED | deviation_code = X2 | Route to the restructure assessment | DEV_REROUTE | Restructuring officer | Workbench | None |
| R-DEV-22 | Deviations | X1 to X7 | DEV_WITH_OWNER | DEVIATION_RESOLVED | otherwise, the outcome does not name a next step | Return the case to the route decision and record that the outcome was not mapped | DEV_REROUTE | Case owner | Workbench | 2 working days |
| R-DEV-11 | Deviations | X1 to X7 | DEV_WITH_OWNER | INSURANCE_SETTLED | deviation_code = X3 and insurance clears the balance | Close the case | CASE_ENDED | Workbench | ALS, Workbench | None |

Their owner and systems columns name a business role and systems, not services: "Workbench" is the case of rwb-case and this service's own record read through the composite route, "ALS" is reached through rwb-integration, and "Case owner", "Restructuring officer" and "Specialist" are read as the roles the permission table gives right U on the case record (GAP-3066; ASM-5207, ASM-5208). No rule row of the set names the review forum, so the forum's act is the outcome the officer records and the row that fires on it (ASM-5202).

| ID | Rule | Source |
|---|---|---|
| BR1 | The review is a step of the deviation stage: it runs in `DeviationWorkflow` on `rwb-deviation`, writes `outcome`, `state` and the standard columns of `deviation` and nothing else | TSD S8 T3.0, T3.1, T4; context pack ownership rows (table and workflow); FSD S8 A2.17.2 |
| BR2 | The result is recorded before the change, with the rule ID, the package version in force, the reason and the outcome; a failed write changes nothing and the caller sees MSG-P7-003 | DP-03; TSD S8 T2 ("writes the decision log entry before any change"); legacy AC1 and AC2 |
| BR3 | Only a deviation open at `DEV_WITH_OWNER` of that case is reviewed, and only one of LOV-DEV-OUTCOME is recorded; any other state, case or value is refused | TSD S8 T4; TSD S8 T3.2; Business Rules and Routing Logic v4 rows R-DEV-09, R-DEV-10 and R-DEV-22 |
| BR4 | The state move is the rule's: `X1` and `X7` to `DEV_RESOLVED`, `X2` and an unmapped outcome to `DEV_REROUTE`; `CASE_ENDED` on the row is not a close of the case | Business Rules and Routing Logic v4; ASM-5205 |
| BR5 | No cross-schema join and no foreign key leaves `rwb_deviation`; `case_id` is an identifier of another service's fact | DP-01; TSD S8 T3.3 |
| BR6 | The package version in force is read from rwb-decision and recorded with the review; a row that fires is recorded by its ID and no rule ID is invented for the forum | ASM-5204, ASM-5205; TSD S8 T4 |
| BR7 | Every value a business person may change is a rule row or reference data read with its version: the deviation codes, the outcome list, the states, the right and the package version | FSD S8 BR-S8-017; legacy Guardrails |
| BR8 | No personal data in `rwb_deviation`, the decision record, a log or a workflow input; the member's identity is a key and not a name | Template and Rules §R7.2 (s17); TSD S8 T6.2 |
| BR9 | The clearance stays outside: `cleared_at`, `contact_stop`, the timers and the clock resume of R-DEV-18 are FEAT-DVH-06's and no column of them is written here | FSD S8 A2.6; ASM-5205 |
| BR10 | The same review twice writes one record and sends one answer; the operation declares no `Idempotency-Key`, so the repeat is matched on the deviation reference and the outcome | TSD S8 T-A.2; ASM-5203 |

### 9. State transitions

| From (deviation state, rwb-deviation) | Event | Condition | To | Written by |
|---|---|---|---|---|
| `DEV_WITH_OWNER` | `DEVIATION_RESOLVED` with the outcome recorded | `deviation_code in (X1,X7)` | `DEV_RESOLVED` | rwb-deviation, on R-DEV-09, by this story |
| `DEV_WITH_OWNER` | `DEVIATION_RESOLVED` with the outcome recorded | `deviation_code = X2` | `DEV_REROUTE` | rwb-deviation, on R-DEV-10, by this story |
| `DEV_WITH_OWNER` | `DEVIATION_RESOLVED` with an outcome that names no next step | `deviation_code` is none of the rows above | `DEV_REROUTE` | rwb-deviation, on R-DEV-22, by this story |
| `DEV_WITH_OWNER` | `DEV_RESOLVED` (the answer of the review) | Any | `DEV_RESOLVED`, unchanged by R-DEV-18 | rwb-deviation, on the clearance step (FEAT-DVH-06, R-DEV-18) |
| `DEV_REROUTE` | `ROUTE_REOPENED` | Any | `ROUTE_D6` | rwb-deviation, on R-DEV-19, by the route stories |
| `DEV_WITH_OWNER` | `INSURANCE_SETTLED` | `deviation_code = X3` and insurance clears the balance | `CASE_ENDED` | rwb-deviation, on R-DEV-11, by the X3 path |
| Any state but `DEV_WITH_OWNER` | A review request | The deviation is not open at `DEV_WITH_OWNER` | Unchanged | none; 409 (X3) |

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | A review request for an open deviation | The package in force is read | Evaluating |
| Evaluating | A row of the package fires | The code and the outcome are the row's | Recording |
| Evaluating | No row fires with a mapped outcome | The outcome names no next step | Recording, on R-DEV-22 |
| Recording | The record and the row commit | The transaction commits | Waiting for the next request |
| Recording | Either write fails | X1 | Waiting, nothing changed |

The states `DEV_WITH_OWNER`, `DEV_RESOLVED`, `DEV_REROUTE`, `CASE_ENDED` and `RESUMED` are those of the DEV machine of TSD S8 T4 and the States sheet of the Business Rules and Routing Logic v4 (9 states over 22 rules). This story writes the three states the `DEVIATION_RESOLVED` rows give and none of the others.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RISK, risk and model risk officer | Case record R in TSD S8 T6.1: the primary role of FSD S8 A2.17.3.3, reviewing an override through the operation's right U (ASM-5207) |
| RW-CONDUCT, conduct and QA officer | Case record R: an also-uses role of FSD S8 A2.17.3.3, reading the review and needing the operation's U to record one |
| RW-COE, center of excellence analyst | Case record R: the second also-uses role of FSD S8 A2.17.3.3 |
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-ENFORCE, RW-SALEOFF | Case record U: the roles the legacy permission table names with right U |
| RW-DEBTSALE, RW-GUARANT, SY-CASEWF, SY-DATALOAD | Case record U: the four further identities TSD S8 T6.1 gives U, which are the legacy table's "and 4 more" (ASM-5208) |
| RW-TEAMMGR, RW-LEGAL, RW-NPAMGR, RW-WRITEOFF, RW-CREDITAD, RW-AGENCYMG, RW-AUDIT, RW-COMPLY, RW-BIANAL, RW-TRIBE and the other PT-* and SY-* identities | Case record R: read only, in scope, and refused the review |
| rwb-deviation service identity | Reads the package, evaluates the rows, writes the record and the row and serves the operation; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD S8 T6.1 and nothing wider. The right this story needs is U: the legacy permission table gives right U on the case record to the eight roles it names plus four more, and TSD S8 T-A.2 declares right U on API-S8-002. The primary role holds R only, and the matrix row is not widened here. DP-08 is not in this story's pattern set: the capability area and the right are declared per operation and the access guard is a service-template capability, so the check is stated and not built.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-CAS-036 | deviation (S8, `rwb_deviation`) | id | Read, the deviation reference the operation takes as `deviationId` and the record cites |
| DF-CAS-037 | deviation (S8, `rwb_deviation`) | case_id | Read, the case of the review; recorded in the decision record |
| DF-CAS-038 | deviation (S8, `rwb_deviation`) | deviation_code | Read, the code the fired row tests |
| DF-CAS-039 | deviation (S8, `rwb_deviation`) | raised_at | Read, presented to the forum as the age of the override |
| DF-CAS-040 | deviation (S8, `rwb_deviation`) | raised_by | Read, the source of the flag |
| DF-CAS-041 | deviation (S8, `rwb_deviation`) | paused_state | Read, the state the case paused in; not changed here |
| DF-CAS-042 | deviation (S8, `rwb_deviation`) | handler_user_id | Read, the handler the review does not reassign |
| DF-CAS-043 | deviation (S8, `rwb_deviation`) | contact_stop | Read, the stop this story does not lift |
| DF-CAS-044 | deviation (S8, `rwb_deviation`) | cleared_at | Not written: the clearance step writes it (FEAT-DVH-06) |
| DF-CAS-045 | deviation (S8, `rwb_deviation`) | outcome | Write, the forum's outcome from LOV-DEV-OUTCOME |
| Standard columns | deviation (S8, `rwb_deviation`) | `state`, `version`, `updated_at`, `updated_by` | Write `state` (the rule's to-state) and the audit columns; `version` guards the update |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_deviation`) | rule id, rule version, decision code, inputs reference, reason, from and to state, decided at | Write through the local library, before anything else: the rule ID that fired, the package version, the reason, the outcome and the states |
| DF-WRK-027 to DF-WRK-036 | timer (P3) | id, case_id, task_id, timer_type, started_at, expires_at and 4 more | Not read as a table and not written: the stage clock is paused by the raise step and resumed by R-DEV-18 |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Not read as a table: the package version arrives on the package read |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | id, case_no, product_group, primary_person_key, status, stage_code and 17 more | Not read as a table and not written: the case reference arrives on the deviation row and the case stays with P3 |
| the reason of the forum | the review request | Read as `note` of the request and recorded in the decision record; it has no column in `deviation` (TSD S8 T3.1), no field ID and no value format in any source: Not specified in the source documents (GAP-3066; ASM-5203) |

Field IDs are those of TSD S8 T3.1 and the Logical Data Model and Data Dictionary, and the timer, rule and case rows are the rows the legacy Data table lists, with their owners changed to P3 and P7 by the target. **No new table, no new column and no migration**: the table arrives with the DB story of this service, and `decision_record` and `idempotency_key` are library objects created in `rwb_deviation` by the library's own migration (DP-03). `outbox_event` also sits in the schema as a library object, and this step writes no row to it because it publishes no event (§12.3).

**No personal data.** The rows carry identifiers, codes, dates, list values, a rule ID, a package version and a reason text. The member's identity is a key: no name, e-mail, phone number, address or identity number is read into the record, the answer, a log or a workflow input, and the fixtures are synthetic. `primary_person_key` is P3's and is never copied here.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13). This story supplies the review branch of the deviation-outcome operation, whose shape RWB-S8-E7008-CON declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| PATCH | `/deviations/{deviationId}` (API-S8-002) | `DeviationOutcome` in with the outcome and the note that carries the reason, `Deviation` out with the recorded outcome, the state and the decision-record reference | Case record, right U, scope applied | Not applicable |
| POST | `/cases/{caseId}/deviations` (API-S8-001) | `DeviationRequest` in, `Deviation` out; declared by the same baseline and built by the raise stories of the module, not here | Case record, right U, scope applied | `Idempotency-Key` header |

The errors are 400, 401, 403 with MSG-P4-002, 404 for a deviation that is not on the case, 409 for a deviation that is not open at `DEV_WITH_OWNER`, 422 with MSG-GEN-001 for a missing or unlisted outcome, and 503 when the library or the package read does not answer. TSD S8 T-A.1 publishes both operations with their requests, answers and the error set 401, 403, 404, 409, 422 and 503, so the mutation is published and needs no placeholder. The ownership rows of the context pack give this service two operations and no read of the deviation list, and the legacy SCR-08 "Loading; list" state needs one; the list read is therefore Not specified in the source documents (GAP-3066; ASM-5206) and is reached, until it is published, through the composite route of SCR-08 (§15).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The rule-package read in force (operation name Not specified in the source documents (GAP-3066; ASM-5204)) | `/api/recovery/decision/v1` | P7 rwb-decision | The DEVIATION package at its version, with R-DEV-01 to R-DEV-22 over its 9 states, read once per review; faked |

The row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). It is a contract dependency of class C that the plan does not carry, because this story's C row is None, and the S8 row of the connection matrix carries no P7 edge although the default ruling gives the rule package registry to rwb-decision; the absence is recorded (GAP-3066; ASM-5204).

#### 12.3 Events published

None. The service publishes on `rwb.deviation.events.v1` and its event set carries EV-06 `DeviationRaised` (`caseId`, `deviationCode`, `raisedBy`, consumed by Timers and Communications for the contact stop) and EV-07 `DeviationCleared` (`caseId`, `deviationCode`, `outcome`, consumed by Timers and Communications), and both belong to the raise and clearance steps of the stage (Event and Messaging Design v4; TSD S8 T5.3). A review sets the outcome and the state the rule gives and lifts no stop, so this story declares no event, no producer group and no outbox row, and a build that publishes EV-07 here fails the absence test. The topic carries the retry and `.dlt` topics of the platform (DP-14), and the outbox and inbox library that relays it is the DP-09 dependency the plan does not carry (GAP-3066; ASM-5206).

#### 12.4 Events consumed

None. The service listens to rwb-case events on the connection matrix's column P3 and to P1 and P10 events (context pack connection matrix, row S8: events from P3, REST and events to P1, Temporal and events to P10), and none of them belongs to the review, whose trigger is the officer's confirmation on SCR-08. This story therefore holds no consumer group, no subscription of its own and no inbox row, and a build that adds one fails the absence test. The FSD declares no background event for the feature (FSD S8 A2.17.4.4).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DeviationWorkflow` | Workflow, one execution per deviation, can start at any time on a case, continues-as-new with the case stage | `rwb-deviation` in namespace `rwb-recovery` | Input: the case reference, the deviation reference and the package in force; signals: the review request, the clearance and the routing; outcome for the parent: the deviation state and the outcome |
| `recordDeviationReview` | Activity, the one review step of the stage | `rwb-deviation` | The deviation reference, the outcome, the reason and the package version in; the record reference and the state out, with the record written before the row |

The parent is `CaseWorkflow` on task queue `rwb-case`, which starts this stage as a child and applies the clock and the route; the stage outcome travels on the parent-child edge and never on a REST call (context pack, Temporal and Drools slide 13; ASM-5206). No child workflow for the case and none for the money exists in this service. The activity name is a target design choice fixed by no source document.

#### 12.6 Schedules

None. The review is an officer-driven step and owns no Temporal Schedule, no Quartz row and no shared job table. The service owns no job in the context pack's ownership rows (Jobs: None), and nothing of the pause, the escalation timer of R-DEV-20 or the screening run is built or declared here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| deviation | S8 (`rwb_deviation`) | The deviation X1 to X7 of a case; this story writes its `outcome`, its `state` and the audit columns |
| decision_record | PLT library, created in `rwb_deviation` | The local hash-linked decision record of the review (DP-03) |
| idempotency_key | PLT library, created in `rwb_deviation` | The key of the raise operation, provided by the same baseline; the review declares none (§12.1) |
| outbox_event | PLT library, created in `rwb_deviation` | Present as a library object; this step writes no row to it (§12.3) |

Not owned and never read as a table: `recovery_case` and `timer` (P3), every `v_ace_*` view (P1), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `payment` (P8). No foreign key leaves the schema and `case_id` is an identifier, not a foreign key across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision rule-package fake | The DEVIATION package at its version in force, with R-DEV-01 to R-DEV-22 over 9 states | AC1 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC2, X1 |
| gateway-bff composite route fake | The merged SCR-08 answer for the open deviations of `RW-2026-000502`, before and after the review | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation name of the package read carries the placeholder until its owner confirms it (GAP-3066; ASM-5204).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 consumed | The review branch of `/api/recovery/deviation/v1/deviations/{deviationId}` and the raise operation of the same base; the package read of rwb-decision; one hop, 2 s. The SCR-08 list read is not published (§12.1) |
| Kafka | 0 published, 0 consumed | EV-06 and EV-07 belong to the raise and clearance steps; no event of this step (§12.3, §12.4) |
| Temporal | 1 workflow and 1 activity | `DeviationWorkflow` and `recordDeviationReview` on `rwb-deviation`; the stage outcome returns to `CaseWorkflow` on `rwb-case`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.deviation`, module `review`; front end `src/modules/recovery/deviation/DeviationQueue.tsx`, the fragment SCR-08 embeds.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the step: the record and the row commit together or not at all. DP-13 moves the base of the legacy `/api/recovery/v1` paths and gives the deviation-outcome operation its home. DP-19 is how SCR-08 reaches this service, one hop through the gateway. These three are the whole pattern set of the key and the story adds no fourth: DP-04 (the embedded Drools kit), DP-07 (the reference-data contract of rwb-case, which holds the lists this step reads as published values), DP-08 (the access guard of the template) and DP-09 (the outbox and inbox library) are real dependencies of the step that the plan does not hold, and they are recorded in the registers instead of the metadata table (GAP-3066; ASM-5204, ASM-5206).

**Dependencies the tables add and the plan does not hold.** The package row is a class C dependency in fact and the plan's C row is None, so the story builds against its document and fake on Day 1. The Drools kit of DP-04 would add `RWB-PLT-E1072-CON` and `RWB-P7-E1073-CON`; the package is read as data and evaluated by this service's own evaluator, so no kit is declared. The outbox library of DP-09 would add `RWB-PLT-TE006-CON` and is needed only by the stories that publish. The plan's H row stands unchanged.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DeviationWorkflow` review branch | Workflow | Receives the review request as a signal on the deviation stage, reads the package in force and reports the state and the outcome to the parent |
| `recordDeviationReview` | Activity | Reads the deviation and the package, evaluates the rows, writes the record and the row and answers |
| `DeviationOutcomeEvaluator` | Service | Fires R-DEV-09, R-DEV-10 and R-DEV-22 over the package in force: the from-state test, the code test and the unmapped-outcome test |
| `DeviationDecisionRecordWriter` | Library adapter | Writes the record with the rule ID and the package version before anything else, hash-linked; refuses the step when the write fails |
| `DeviationReviewController` | Controller | The review branch of the deviation-outcome operation, the capability area and right U, the scope and the problem mapping |
| `RulePackageClient` | Client | The DEVIATION package read of rwb-decision at its version in force, one hop, 2 s, breaker |
| `DeviationQueue` | React component | Shows the open deviations of the case and the recorded outcome on SCR-08 |

**Database and migrations.** No Flyway file. The `deviation` table arrives with the DB story of this service, and the record is a library object created in `rwb_deviation` by the library's migration (DP-03). No column is added for the reason or the review: neither has a source (ASM-5202, ASM-5203).

**Configuration and reference data.**

- The review conditions, the deviation codes, the outcome list, the from and to states and the package version: rule rows and reference data with their version, never written in code (ASM-5203, ASM-5205).
- The capability area "Case record" and its rights: access rows of rwb-access, read through the guard.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020; the review has no timer of its own.

**Build steps**

1. The review branch of `DeviationWorkflow` and its input record, registered on `rwb-deviation` as the deviation stage, with the officer's confirmation as its signal.
2. `RulePackageClient` against its fake, with the 2 s budget, the breaker and the no-answer path (AC1, X5).
3. `DeviationOutcomeEvaluator` over the package, with the three firing rows, the unmapped-outcome path and the not-open path (AC1, X3, X4).
4. `DeviationDecisionRecordWriter` against the stub, with the failed-write path (AC1, AC2, X1).
5. `DeviationReviewController` with the review branch, right U, the scope and the problem mapping of the declared errors, and `DeviationQueue` on SCR-08 through the composite route fake (AC1, X2, X6, X7).
6. The transaction step: the record, `outcome`, `state` and the audit columns in one commit, with the optimistic-lock version (AC1, X1).
7. The boundary test: no statement outside `rwb_deviation`, no `v_ace_*` read, no write to `rwb_case`, `rwb_decision` or any other schema, and no write to `cleared_at`, `contact_stop` or a timer (X8, BR5, BR9).

**Feature flag.** `rwb.deviation.override-review-v1`, a flag of the platform library; off means the operation answers 503 with no write and SCR-08 hides the review action, and the raise, routing and clearance stories are unaffected.

**Done when.** The tests of section 16 pass, the step runs from a synthetic open deviation in SIT, the outcome and the reason are recorded with the rule ID and the package version in force, a deviation that is not open and an outcome outside the list are refused, a repeated request writes once, a forced record failure changes nothing, no `recovery_case` row, no `cleared_at` write and no `v_ace_*` read exists in the build, and SCR-08 answers through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S8-001 | Carried from the legacy message set of RWB-E7-008: the deviation was raised and the case is with its handler. Raised by the raise story of the module, not by this step | {deviation} was raised. The case is with {handler}. |
| MSG-GEN-001 | A required element is absent or invalid: the outcome, the reason, or a deviation that is not on the case (X3, X4) | Enter {field}. |
| MSG-P4-002 | A role without the case record right U calls the review (X2) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the review is answered (X1) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The four IDs are those of the legacy message set; the text is the legacy and FSD wording, copied unchanged, and no message is reworded and no new one is added. MSG-S8-001 is kept because the legacy table of RWB-E7-008 lists it: it is the message the officer sees on the deviations this step reviews, and it is not raised here.

### 15. Screens and states

SCR-08 Deviation queue is served through the gateway-bff composite route (DP-19). The route calls rwb-deviation for the deviations, their handlers and the recorded outcome, and rwb-case for the case and its route state; this story fixes the rwb-deviation answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The legacy screen table gives SCR-08 "Loading; list" and SCR-06 Raise deviation "Form; saved". This story produces the review from the list state of SCR-08: the forum sees each open deviation with its code, its raise facts, its handler and its paused state, and records the outcome and the reason. SCR-06 is the raise form and belongs to the raise stories (RWB-S8-E7001-APP to RWB-S8-E7007-APP). Neither screen is described as a review screen, so the place of the review action on SCR-08 is Not specified in the source documents (GAP-3066; ASM-5202), and no published operation reads the deviation list (GAP-3066; ASM-5206). The refusal, not-open, bad-outcome and not-recorded states read the messages of section 14.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E7-008-01 | AC1 | Component | The open deviation `X3` of `RW-2026-000502` on the fakes; the outcome, the reason, the record, the state and the package version asserted |
| TC-E7-008-02 | AC2 | Component | The decision-record stub stopped; nothing written and MSG-P7-003 shown |
| TC-E7-008-03 | Access | Component | A role without the case record right U; 403 with MSG-P4-002 and no read |
| TC-E7-008-04 | Principle 5 | Component | A forced decision log write failure inside the transaction; the deviation is unchanged and no record exists |

The four legacy cases are those of RWB-E7-008 in their legacy order, with the Level column added: every case is tested on the fakes, so every case is `Component`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written by this story, and the cross-service journey belongs to the wave 4 harness.

### 17. Guardrails

- No business value in code: the review conditions, the deviation codes, the outcome list, the states, the right and the package version stay rule rows and reference data, never a constant, a default or a branch.
- No personal data in `rwb_deviation`, in a workflow input or in a log: identifiers, codes, dates, a list value, a rule ID, a package version and a reason text only, and every fixture is synthetic. The member's identity is a key and never a name.
- ACE data only through the owner's contract: this service holds no `v_ace_*` grant and reads no ACE table.
- The case stays with rwb-case: no `recovery_case` row, no case state column and no case write here; the stage outcome returns to the parent workflow.
- The clearance stays outside: `cleared_at`, `contact_stop`, the timers and the clock resume are not written by this step (BR9).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no shared job table, no Quartz row, no monolith base, no event published by this step and no `recovery_log` write.
- The record is written before the row; a build that answers outside the record's transaction fails the review (DP-03).
- The package is read and never embedded: a build that adds a Drools kit or a rule row of its own fails the review (ASM-5204).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| No requirement row traces to FEAT-DVF-08 | The requirement this feature serves is Not specified in the source documents (GAP-3066; ASM-5210): TSD S8 T8 maps every REQ-DVH and REQ-S8 row to FEAT-DVH-01, FEAT-DVF-01 or a placeholder | The trace rests on the legacy key, the feature row and AC1 | TC-E7-008-01 |
| ADR-013 | 19 services inside ACE | rwb-deviation as the owner of the deviation stage | TC-E7-008-01 |
| ADR-014 | Schema and login per service | `rwb_deviation` and its own login | TC-E7-008-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The package read with its budget and breaker | TC-E7-008-01 |
| ADR-022 | Local decision record plus central ledger | The record written before the review is answered | TC-E7-008-02, TC-E7-008-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E7-008, disposition Split (rework); feature FEAT-DVF-08 |
| Legacy criteria | AC1 and AC2, owned word for word by this story |
| Wave and release | Wave 4 and release 31 May 2027 (tentative), copied unchanged from the plan; EP07 is wave 4 and the service's Arch v5 wave is 2, so the W-MAP wave is not earlier and no conflict is raised (ASM-5209) |
| Source text | Legacy RWB-E7-008; FSD S8 Deviation handling v4 A1.2, A1.3, A2.17, A2.17.2, A2.17.3.1, A2.17.3.2, A2.17.3.3 and A2.17.4; TSD S8 Deviation handling v3 T0.2, T2, T3.0, T3.1, T3.2, T4, T5.3, T6.1, T6.2, T8 and T-A; Business Rules and Routing Logic v4 rows R-DEV-09, R-DEV-10, R-DEV-11 and R-DEV-22; Event and Messaging Design v4 events EV-06 and EV-07; API Specification v4 element `DeviationOutcome` |
| Test cases | TC-E7-008-01 to TC-E7-008-04 |
| Feature and screens | FEAT-DVF-08, SCR-08 Deviation queue (SCR-06 belongs to the raise stories) |
| Rules | R-DEV-09, R-DEV-10 and R-DEV-22 fired; R-DEV-11 named as the X3 path's |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The published shapes of the operations, the `Deviation` and `DeviationOutcome` elements, the review properties, the consumed row, the rights of the document and the fakes: RWB-S8-E7008-CON.
- The screening that proposes a deviation and the L1 agent: RWB-S8-E1062-APP and the other E1 and E2 stories of the module.
- Raising a deviation, pausing the stage clock, the prescription clock, the routing to the named owner and the contact stop: RWB-S8-E7001-APP to RWB-S8-E7007-APP.
- The clearance of the deviation, `cleared_at`, the lift of the contact stop and the resume of R-DEV-18: FEAT-DVH-06 and the clearance stories of the module.
- The route reopen of R-DEV-19, the case closed on `INSURANCE_SETTLED` of R-DEV-11 and the escalation timer of R-DEV-20: the route and X3 stories.
- The breach path of a contact sent while a block is on: RWB-S8-E7010-APP.
- The case of record, its states, the parent `CaseWorkflow` and the clock: rwb-case (P3). The DEVIATION package and its rule rows: rwb-decision (P7).
- The gateway-bff composite route and the screen field list of SCR-08: RWB-PLT-N001-CON and the edge stories.
- An event that carries the review to rwb-reporting: none is published by the service, so the measure rests on the decision-record ledger (ASM-5206).
- The requirement row of FEAT-DVF-08: no source publishes one, and the trace waits for the E7 BRD and the PRD (GAP-3066; ASM-5210).
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

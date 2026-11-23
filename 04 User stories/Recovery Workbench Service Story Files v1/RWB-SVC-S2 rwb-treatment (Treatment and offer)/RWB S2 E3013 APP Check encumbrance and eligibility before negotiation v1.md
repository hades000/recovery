# RWB-S2-E3013-APP Check encumbrance and eligibility before negotiation

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: application slice split from RWB-E3-013 for rwb-treatment. The four legacy acceptance criteria are kept word for word with their origin tag and now run on the deed-in-lieu readiness step of `TreatmentWorkflow` on task queue `rwb-treatment`, reached through the gateway-bff composite route (DP-19) and served on the base `/api/recovery/treatment/v1` (DP-13); the one `recovery` schema becomes `rwb_treatment` and no other service's table is read (DP-01); the collateral and registration facts are read from the service's own read-only `v_ace_collateral`, `v_ace_collateral_detail` and `v_ace_npa_asset` views (DP-05); the legacy `DecisionLogWriter` write to the shared `decision_log_entry` becomes the local decision record of RWB-PLT-E1027-CON written in the same transaction as the change (DP-03); the check answer, the block message and the title-set task request have no source shape and are declared as the working read (GAP-2674; ASM-4394, ASM-4395, ASM-4396). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S2-X |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S2-E3013-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **restructuring officer (FCR)**, I want **the Workbench to run the encumbrance and title checks on a deed-in-lieu candidate as soon as the route is approved, to block the route and raise the title-set task where the asset cannot transfer, and to record every check with the rule version that decided it**, so that **a deed in lieu is not negotiated on an asset that cannot transfer and the deed-in-lieu path reaches its 12-day target instead of the 26 days it takes today**.

This is the application slice of legacy RWB-E3-013. It owns:

- all four legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages, screens and data rows they depend on;
- the deed-in-lieu readiness step of `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case, with the activities `readEncumbrance`, `evaluateReadiness` and `recordAndApply`;
- the read of the ACE collateral, collateral-detail and NPA-asset views under DP-05, and the encumbrance, registration and title-set facts they carry;
- the rules R-DIL-01 to R-DIL-06 of the DEEDINLIEU package and R-SET-22 of the SETTLEMENT package, with the 2, 10 and 5 working-day clocks read from the rule set in force;
- the local decision record of each check, written through RWB-PLT-E1027-CON in the same transaction as the `treatment` row (DP-03);
- the readiness outcome of the `treatment` row in schema `rwb_treatment`, and the stage outcome the parent `CaseWorkflow` uses to move the case status and raise the title-set task.

It does not own: the published shape of the readiness section, of the title-set task request and of the error set, which are RWB-S2-E3013-CON; the deed-in-lieu offer, price, floor and second signature, which are RWB-S2-E3012-APP and its siblings; the treatment record and the treatment read, which are RWB-S2-E3001-APP and RWB-S2-E3001-CON; the case, its status, its tasks and its timers, which are rwb-case's; the valuation order that follows a clear asset, which is S1 rwb-valuation and S5 rwb-asset; the asset unlock that follows the inspection, which is RWB-S2-E3014-APP; and the deployment of this build, which is the wave 2 integration harness and the platform DevOps stories.

### 2. Business rationale

Legacy RWB-E3-013 existed because a deed in lieu negotiated on an asset that cannot transfer loses the negotiation, the appraisal fee and weeks of the case clock. The functional specification keeps the objective unchanged — the encumbrance and title checks run early, so a deed in lieu is not negotiated on an asset that cannot transfer — and the program keeps the requirement: REQ-S2-005 states that deed-in-lieu readiness, including the encumbrance check and an early valuation, is established before negotiation starts, and the program metric for the deed-in-lieu path is 12 days against 26 today.

What D-RCV-60 changes is where the check runs, what it reads and what it writes. In the monolith the check was a method in the same process as the case row, the collateral rows and the decision log. In the target:

- the readiness step runs inside `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow`, so the check happens where the DEEDINLIEU and SETTLEMENT rules live and the case keeps one parent workflow from entry to closure (DP-12; Architecture v5 slides 5 and 11);
- the collateral, registration and NPA facts are read from the ACE views this service is granted, read only, and never from another service's table (DP-05; DP-01);
- the check answer and the outcome are written to `treatment` in `rwb_treatment`, and the decision goes to the local decision record in the same transaction (DP-03);
- the case status, the tasks and the clocks they run on stay rwb-case's: the stage reports an outcome and the parent moves the status and raises the title-set task (ASM-4394);
- the officer reads the answer through the gateway-bff composite route, one hop, on SCR-16 (DP-19; DP-13).

No business value moves. The 2 working days of R-DIL-01, the 10 working days of R-DIL-04 and the 5 working days of R-SET-22 are values in force in the rule set, read with the rule version and never written in code (BR-S2-013).

### 3. Preconditions

- RWB-S2-E3013-CON is published: the `readiness` section of the treatment answer, its properties, the title-set task request element, the error set, the compatibility rule and the fakes are baselined and handed to this story. The section and the task request have no source shape and are published as the working read (GAP-2674; ASM-4396).
- RWB-PLT-E1027-CON is published with its writer fake: `DecisionRecordWriter.record(DecisionRecord)` runs with `@Transactional(propagation = MANDATORY)`, refuses with MSG-P7-009 and fails with MSG-P7-003, so the check and its record commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-16 and SCR-14 reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- The three ACE views are readable by the login of rwb-treatment with SELECT only, and they carry the encumbrance, registration and title-set facts under DP-05. The named fields are DF-ACE-091 to DF-ACE-098, DF-ACE-196 to DF-ACE-207 and DF-ACE-208 to DF-ACE-219; the column that carries `encumbrance_status` of R-DIL-02 and R-DIL-04 is not among the names in the source and is the working read of ASM-4395 (GAP-2674).
- The route decision signal is available: the parent `CaseWorkflow` forwards the case status change to the running stage, and the signal that starts the deed-in-lieu stage carries the route R3, the product group and the collateral business keys. Where the rwb-case contract fixes field names, they are copied from it; no source fixes them here (GAP-2674; ASM-4394).
- The embedded Drools runtime and the DEEDINLIEU and SETTLEMENT packages are the service template's wave-0 capability, and the package version in force arrives on `rwb.decision.RulePackageInForce.v1`; this story names the packages and their versions and adds no build dependency of its own (ASM-4397).
- The access guard, the outbox and inbox library and the workflow kit are service-template capabilities; this story declares the capability area "Treatment and offer", the right R and the call types and adds no build dependency of its own (ASM-4398).
- The per-service Flyway sequence of rwb-treatment carries `treatment` with DF-TRT-001 to DF-TRT-033 and the library object `decision_record`; this story adds no table, no column and never edits an applied migration.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S2-E3013-CON when its tests pass.

### 4. Flow

1. rwb-case's `CaseWorkflow` receives the case status change and forwards it to the running `TreatmentWorkflow` child on queue `rwb-treatment` as a signal; the stage never calls rwb-case (ASM-4394).
2. R-DIL-01 starts the readiness step: the lead is prioritised and the early readiness checks begin, on the 2 working-day clock of the rule set. The route is R3, the route state ROUTE_APPROVED_DIL, the target state EARLY_READINESS_CHECK.
3. `readEncumbrance` reads `v_ace_collateral`, `v_ace_collateral_detail` and `v_ace_npa_asset` for the collateral of the case by `collateral_no` and `asset_key`, read only and with no write to any ACE object (DP-05).
4. The read returns the encumbrance fact for a mortgage (`encumbrance_status` clear or unresolved), the registration fact for hire purchase (registration clear in SCIS) and the title-set fact (the title document numbers of the collateral detail are present or missing).
5. `evaluateReadiness` evaluates the DEEDINLIEU package in the version in force: R-DIL-02 or R-DIL-03 sends a clear asset to VALUATION_ORDERED, R-DIL-04 blocks an unresolved mortgage in ENCUMBRANCE_BLOCKED with the 10 working-day hold, R-DIL-05 resumes on a cleared status and R-DIL-06 returns the case to the route decision when the hold expires.
6. The same activity evaluates R-SET-22 of the SETTLEMENT package for the settlement-side title set: a case at COLLATERAL_RELEASE_REQUESTED with title documents missing raises the title-set request and stays at COLLATERAL_RELEASE_REQUESTED, on the 5 working-day clock.
7. `recordAndApply` assembles the `DecisionRecord` — the decision code of the readiness event, the case, the rule ID with the package version, the recommendation, the final call and the actor — and writes it through `DecisionRecordWriter.record` in the caller's transaction, then writes the readiness outcome and the decision reference to the `treatment` row in the same transaction (DP-03).
8. The stage publishes nothing: it reports the outcome to the parent `CaseWorkflow`, which moves the case status and, on the title-set outcome, raises the task to re-create the title set with its 5 working-day clock (ASM-4394).
9. The officer reads the answer on SCR-16 Deed in lieu through the treatment read, one hop through the gateway-bff composite route (DP-19): the encumbrance status, the title-set status, the hold date, the rule ID and version, and the check time.
10. While the route is blocked nothing is negotiated: the case owner sees the hold and its review date, and the resume or the return is decided by R-DIL-05 and R-DIL-06 on the fact that arrives.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The role does not hold right R on "Treatment and offer" | 403 before any read; the refusal is the guard library's and is logged by it | MSG-P4-002 | AC1, TC-E3-013-05 |
| X2 | The decision record cannot be written | `recordAndApply` throws before the `treatment` row is written and the transaction rolls back; nothing changes | MSG-P7-003 | AC4, TC-E3-013-06 |
| X3 | The decision record is refused for a missing or invalid field | Nothing is written and the field is named in the service log and the incident | MSG-P7-009 | AC4 |
| X4 | The mortgage encumbrance is unresolved | The route is blocked and held for the 10 working-day limit; the stage reports ENCUMBRANCE_BLOCKED to the parent | Not specified in the source documents (GAP-2674; ASM-4394) | AC1, AC3 |
| X5 | The title documents are missing on a collateral-release case | The title-set request is reported to the parent, which raises the task on the 5 working-day clock, and the case stays where it is | None in the source | AC2 |
| X6 | No collateral row is found for the case's `asset_key` | The check cannot decide: the stage reports an unmatched readiness outcome and raises a task for the case owner; nothing is blocked or cleared | MSG-GEN-001 | AC1 |
| X7 | The hold expires with the encumbrance still unresolved | R-DIL-06 reports the return to the route decision with reason `encumbrance_unresolved`; the parent moves the case | None in the source | AC3 |
| X8 | The rule package in force is not the one the step started on | The step re-evaluates against the package named on `rwb.decision.RulePackageInForce.v1` and records the version it used | None | AC1 |

X1, X2 and X3 are the exception paths of RWB-E3-013 carried onto the split, X4 to X7 are the readiness paths the rule set adds, and X8 belongs to the parent-and-child workflow model of the target. The 10-day hold and the 5-day clock are values in force, so neither is a constant of this story.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published readiness contract, the decision-record library and the gateway route with their fakes, on its own schema and its own ACE views, and needs no live rwb-case, no live rwb-valuation and no live rwb-decision to start |
| Negotiable | The activity names, the decision code per readiness event and the shape of the stage outcome are this story's choice; the rules, the messages, the screens and the seven view tables are fixed |
| Valuable | A deed-in-lieu candidate is blocked or cleared in days instead of after negotiation, and every check carries the rule version that decided it |
| Estimable | One workflow branch, three activities, one view read set, one repository and one record write |
| Small | Finished inside two weeks with its tests on the fakes and the view fixture |
| Testable | Each criterion runs on synthetic treatments and collateral facts through the fake and the view fixture, plus the two component cases of the access answer and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Check encumbrance and eligibility before negotiation

  Scenario: AC1 Check encumbrance and eligibility before negotiation (legacy RWB-E3-013 AC1)
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then runs the encumbrance and title checks early, so a deed in lieu is not negotiated on an asset that cannot transfer
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-SET-22 (legacy RWB-E3-013 AC2)
    Given the rwb-case contract mock returns case status COLLATERAL_RELEASE_REQUESTED
    Given a case in state COLLATERAL_RELEASE_REQUESTED
    When title documents missing
    Then raise a task to re-create the title set before release
    Then the case moves to COLLATERAL_RELEASE_REQUESTED

  Scenario: AC3 Rule R-DIL-01 (legacy RWB-E3-013 AC3)
    Given the rwb-case contract mock returns case status ROUTE_APPROVED_DIL
    Given a case in state ROUTE_APPROVED_DIL
    When route approved
    Then prioritize the lead and start the early readiness checks
    Then the case moves to EARLY_READINESS_CHECK

  Scenario: AC4 Not recorded (legacy RWB-E3-013 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Target reading.** Every line and every value above is the legacy line and the legacy value, unchanged, including the repetition of `Then` and the legacy wording `the action is taken` and `the decision log cannot be written`; what changes is where it runs, what produces the fact and how it is reached. The one added line is the mock Given of AC2 and AC3, which stands in for the case status that rwb-case owns, so the stage can be tested before the live case workflow exists (ASM-4394). The check runs on the deed-in-lieu readiness step of `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery`, with the activities `readEncumbrance`, `evaluateReadiness` and `recordAndApply` (Architecture v5 slides 5 and 11; DP-12). The facts of AC1 are read from `v_ace_collateral`, `v_ace_collateral_detail` and `v_ace_npa_asset` under DP-05, read only, and the encumbrance and title statuses are values of that read and never derived in code (GAP-2674; ASM-4395). "The decision log" of AC1 and AC4 is the local decision record of `decision_record` in `rwb_treatment`, written through RWB-PLT-E1027-CON with `@Transactional(propagation = MANDATORY)` in the same transaction as the `treatment` row; `decision_log_entry` is P7's ledger and is neither written nor read here (DP-03). The states of AC2 and AC3 — COLLATERAL_RELEASE_REQUESTED, ROUTE_APPROVED_DIL and EARLY_READINESS_CHECK — are case statuses of rwb-case: the stage reports the outcome and the parent moves the status, so the transition is proved against the mock and not by a write of this service (ASM-4394). R-SET-22 is carried by this story because the title set is the same readiness fact on the settlement side; its self-loop keeps the case where it is and the task is the only move. The answer the officer reads, its property names and the title-set request are published by RWB-S2-E3013-CON as the working read (ASM-4396).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | An approved deed-in-lieu route starts the early readiness checks at once: the lead is prioritised and the encumbrance and title facts are read before any negotiation | R-DIL-01; REQ-S2-005 |
| BR2 | A mortgage whose encumbrance is clear, and a hire-purchase asset whose registration is clear in SCIS, order the valuation and leave the readiness state | R-DIL-02, R-DIL-03 |
| BR3 | An unresolved mortgage encumbrance blocks the route and holds the case for the hold limit, resumes on a cleared status and returns to the route decision when the hold expires | R-DIL-04, R-DIL-05, R-DIL-06 |
| BR4 | Title documents that cannot be found raise a task to re-create the title set before release, and the case stays where it is until the set exists | R-SET-22 |
| BR5 | The decision is recorded with the rule version before or with the change; if it cannot be recorded, nothing changes | REQ-DRI-005; DP-03; MSG-P7-003 |
| BR6 | No value a business person may change is written in code: the encumbrance and title statuses, the hold limit and the three clocks are values in force, read with their version | BR-S2-013 |
| BR7 | The case status, the task and its clock are not this service's: the stage reports and the parent moves and raises | DP-01; ASM-4394 |
| BR8 | ACE data is read only, through this service's own views, and never written and never copied into another service's table | DP-05; DP-01; ASM-4395 |

**Where each rule lives in the target.** BR1 is the start signal and the first step of the branch. BR2, BR3 and BR4 are `evaluateReadiness` against the DEEDINLIEU and SETTLEMENT packages, with the statuses taken from the view read and no threshold in code. BR5 is the `MANDATORY` transaction of the library, so the `treatment` row and the `decision_record` row commit together or not at all. BR6 is the reason the hold limit and the three clocks are read from the rule set with the package version and not configured here. BR7 is the reason the stage outcome carries the request and the parent raises the task. BR8 is the reason the read is a SELECT against the views and no ACE object is written.

### 9. State transitions

The case status is rwb-case's and is not changed by this story: the readiness step reports an outcome and the parent `CaseWorkflow` moves the case (ASM-4394). The transitions below are the rule set's, and each row is one outcome this story reports.

| From | Event | Condition | To (rule) |
|---|---|---|---|
| ROUTE_APPROVED_DIL | ROUTE_APPROVED | decision.approved and route = R3 | EARLY_READINESS_CHECK (R-DIL-01) |
| EARLY_READINESS_CHECK | ENCUMBRANCE_CLEAR | product = MTG and encumbrance_status = clear | VALUATION_ORDERED (R-DIL-02) |
| EARLY_READINESS_CHECK | REGISTRATION_CHECK_PASSED | product = HP and registration clear in SCIS | VALUATION_ORDERED (R-DIL-03) |
| EARLY_READINESS_CHECK | ENCUMBRANCE_UNRESOLVED | product = MTG and encumbrance_status = unresolved | ENCUMBRANCE_BLOCKED (R-DIL-04) |
| ENCUMBRANCE_BLOCKED | ENCUMBRANCE_CLEARED | encumbrance_status = clear | VALUATION_ORDERED (R-DIL-05) |
| ENCUMBRANCE_BLOCKED | HOLD_EXPIRED | still unresolved at the hold limit | RETURNED_TO_ROUTE_DIL (R-DIL-06) |
| COLLATERAL_RELEASE_REQUESTED | TITLE_DOCUMENTS_MISSING | title documents not found | COLLATERAL_RELEASE_REQUESTED (R-SET-22) |

| `treatment.state` | Event | Condition | To |
|---|---|---|---|
| Draft | readiness outcome reported | `treatment_type` is DEED_IN_LIEU or SETTLEMENT | Draft, with `outcome` and `outcome_at` written |
| Draft | decision record refused or failed | X2, X3 | Draft, unchanged |

The readiness step moves from running to waiting on each signal and ends when the parent closes the stage. No readiness state is stored as a lifecycle of its own: the answer is the outcome columns, the hold date and the decision record, and the case states above stay the parent's.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery squad (RW-TRIBE) | Writes the readiness branch, the three activities, the view read and the repository |
| RW-CASEOWN, case owner | Reads the answer, holds the case while the route is blocked and receives the title-set task; holds CRU |
| RW-RESTRUCT, restructuring officer (FCR) | Reads the answer and acts on the resumed route; holds CRUA |
| RW-SPECIAL, RW-GUARANT | Read the answer; hold CRU |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL | Read the answer; right R only |
| RW-PRODHEAD, RW-CREDCOMM | Read the answer; right RA, and no approval is made in this story |
| SY-CASEWF, SY-RULES, SY-AGENT | Read as service identities, subject to the same checks |
| The case status, the task and its clock | Not this story: rwb-case owns them and the parent moves and raises (ASM-4394) |
| The valuation order, the price, the floor and the second signature | Not this story: S1 rwb-valuation and the deed-in-lieu offer stories hold them |

The rights above are those of TSD S2 T6.1 for the capability area "Treatment and offer", and the check itself is the platform guard library's: this story declares the area and the right R and calls the guard, and it owns no check of its own. No delegation of authority level applies, because a readiness check is not a credit decision. No credential and no personal name appears in the request, the payloads or the logs, which carry case and treatment identifiers, collateral and asset keys, statuses, dates and rule versions only.

### 11. Data

| BR Field ID | Entity or view | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-003 | treatment | decision_log_id | Write: the entry id returned by `DecisionRecordWriter.record` |
| DF-TRT-004 | treatment | treatment_type | Read: DEED_IN_LIEU or SETTLEMENT |
| DF-TRT-013 | treatment | outcome | Write: the readiness outcome |
| DF-TRT-014 | treatment | outcome_at | Write |
| T3.0 `state`, `version`, `updated_at`, `updated_by` | treatment | standard record columns | Write |
| DF-DEC-001 to DF-DEC-018 | decision_record | the record fields of the library | Write through RWB-PLT-E1027-CON |
| DF-ACE-091 to DF-ACE-098 | v_ace_collateral | collateral_no, asset_key, account_key, collateral_value, collateral_type, register_date and 2 more | Read only |
| DF-ACE-196 to DF-ACE-207 | v_ace_collateral_detail | asset_key, title_doc_no, plot_no, area_text, province, lien_rank and 6 more | Read only |
| DF-ACE-208 to DF-ACE-219 | v_ace_npa_asset | asset_ref, asset_key, asset_code, transfer_in_type, from_segment, book_value and 6 more | Read only |
| DF-CAS-001 to DF-CAS-023, DF-WRK-009 to DF-WRK-036 | rwb-case | case, assignment, task and timer rows | Not read and not written: the parent owns them (ASM-4394) |

`treatment` is the only business table this story writes, in schema `rwb_treatment` and through this service's own login (DP-01). The three views are read with SELECT only under DP-05 and no ACE object is written; the `decision_record` row is a library object of RWB-PLT-E1027-CON written in the caller's transaction, and `decision_log_entry` in `rwb_decision` is P7's and is named here only. The encumbrance status, the title-set status and the hold date are not columns of `rwb_treatment`: no source gives them one, and TSD S2 T3.1 carries no such field, so they travel in the answer and in the decision record (GAP-2674; ASM-4396).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). None of its own. The readiness answer is served as the optional `readiness` section of the treatment read `GET /treatments/{treatmentId}`, whose operation entry belongs to RWB-S2-E3001-CON and whose section is declared by RWB-S2-E3013-CON as a compatible addition at major version 1. This story fills that section and publishes no operation entry of its own: the check is started by R-DIL-01 on the case signal and the officer takes no action in it, so there is no write operation to publish, and the legacy endpoint table of RWB-E3-013 names only the treatment read that already exists (GAP-2674; ASM-4396).

The section carries the check type, the encumbrance status, the title-set status, the checked time, the rule ID and version, the hold date and the references by business key — the property names are the working read of the contract story and are not restated here.

#### 12.2 REST operations consumed

None. The route, the product group and the collateral keys arrive on the signal the parent forwards, the collateral facts are read from this service's own views, and the decision record is called in process inside the caller's transaction (DP-03; DP-05; ASM-4394). This is why the Work Package records no C dependency for this story.

#### 12.3 Events published

None. The topic of the service is `rwb.treatment.events.v1` with event names `rwb.treatment.<Event>.v1` (DP-14), and its events `TreatmentApproved` and `TreatmentClosed` belong to the approval and closure stories. This story writes no outbox row of its own and reports its outcome to the parent as a stage outcome.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 rwb-decision | The DEEDINLIEU and SETTLEMENT package versions in force, so each check is evaluated and recorded with the version it used |
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | S8 rwb-deviation | A deviation raised on the case, so the stage holds while the case clock is paused |

Both events arrive through the inbox of the outbox library, deduplicated by cloud event id, so a redelivery changes nothing. The case status change is not an event of this table: it arrives as the signal the parent forwards (ASM-4394).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` (deed-in-lieu readiness branch) | Workflow, one execution per case per stage, the child of `CaseWorkflow` | `rwb-treatment` in namespace `rwb-recovery` | Input: the case, the route R3, the product group and the collateral keys; signals: the case status forwarded by the parent, the rule package in force and the deviation |
| `readEncumbrance` | Activity | `rwb-treatment` | The collateral and asset keys in; the encumbrance, registration and title-set facts of the three views out, read only |
| `evaluateReadiness` | Activity | `rwb-treatment` | The facts in; the outcome of R-DIL-01 to R-DIL-06 and R-SET-22 with the hold date and the rule version out |
| `recordAndApply` | Activity | `rwb-treatment` | The `DecisionRecord` and the `treatment` row written in one transaction through RWB-PLT-E1027-CON, and the stage outcome for the parent |

The stage is the deed-in-lieu branch of the one `TreatmentWorkflow` the service owns, and the parent-and-child model with the steps of receive, ask, record and apply, wait is the one of the target design (DP-12; Architecture v5 slides 5 and 11). The activity names are a design choice of this story and are fixed by no source document. A workflow class never calls the decision-record library directly: the call is made inside `recordAndApply`, so a replay reuses the recorded decision.

#### 12.6 Schedules

None. The step runs from the signal the parent forwards, and the 2 working-day lead clock, the 10 working-day hold and the 5 working-day title-set clock are durable timers inside the workflow, not Temporal Schedules. The service has no legacy Quartz job in this legacy key.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 rwb-treatment | Written for `decision_log_id`, `outcome`, `outcome_at` and the standard record columns; created by the per-service Flyway sequence and never re-created here |
| `decision_record` | `rwb_treatment` | PLT, library object | Not written directly: the row is written by RWB-PLT-E1027-CON in the caller's transaction (DP-03) |
| `v_ace_collateral`, `v_ace_collateral_detail`, `v_ace_npa_asset` | `recovery` (read-only views) | ACE, read through DP-05 | Read only; never written and never owned |

No table of another service is read and no foreign key crosses a schema (DP-01). The case, the task and the timer are rwb-case's and are not read here (ASM-4394). No encumbrance, title-set or hold column is added to `treatment`, because no source gives one (GAP-2674; ASM-4396).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S2-E3013-CON readiness fake | The `readiness` section, the title-set task request and the error set | A clear mortgage; an unresolved mortgage with a hold date; an HP asset with clearance in SCIS; a collateral-release case with title documents missing; a case with no collateral row |
| RWB-PLT-E1027-CON writer fake | The decision record | An accepted record with chain sequence and entry hash; a refusal with MSG-P7-009 and the field; a failed write raising MSG-P7-003 |
| RWB-PLT-N001-CON route fake | The gateway-bff composite route | A composite answer for SCR-16 that joins the treatment read and its readiness section; a refused route for a role without right R |
| rwb-case case-status mock | The signal the parent forwards, used by AC2 and AC3 | A case at COLLATERAL_RELEASE_REQUESTED and a case at ROUTE_APPROVED_DIL; a case status the readiness step does not accept. Test-only, adds no contract dependency (ASM-4394) |
| ACE view fixture | The read of the three views | A mortgage collateral with a clear registration and present title documents; one with an unresolved encumbrance; one with the title document numbers absent; one HP asset with a clear SCIS registration |

The readiness fake is the published contract of RWB-S2-E3013-CON; the case-status mock and the view fixture stand in for the signal of the parent and for the ACE read, which have no published shape of their own here (GAP-2674; ASM-4394, ASM-4395).

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 operations of its own | 0 | The readiness section is served inside the treatment read of RWB-S2-E3001-CON |
| Kafka | 0 | 2 events (`rwb.decision.RulePackageInForce.v1`, `rwb.deviation.DeviationRaised.v1`) | Own topic unused by this story; inbox dedupe by cloud event id |
| Temporal | 0 | `TreatmentWorkflow` readiness branch and 3 activities on `rwb-treatment` | Namespace `rwb-recovery`; stage child of `CaseWorkflow`; no Schedule |
| SQL view | 0 | 3 read-only ACE views | SELECT only under DP-05; no write to any ACE object |
| File, Nexus | 0 | 0 | No file and no Nexus operation is used by the readiness check |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, modules `readiness` and `web`, with the published types in `...treatment.api`. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the check: the record and the `treatment` row commit together, and a failed record leaves nothing behind. DP-05 is the read of the three views, taken as this service's own read-only views, which is the form that adds no dependency; the alternative, the contract read of rwb-source-data, would be a C dependency and is not taken here (ASM-4395). DP-13 moves the base of the operations the screens use and nothing else. DP-19 is how SCR-16 and SCR-14 reach this service, one hop through the gateway, so no screen reads a view or a table.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentWorkflow` readiness branch | Workflow | One execution per case per stage; the route facts, the collateral keys, the package in force and the stage outcome |
| `readEncumbrance` | Activity | The read of the three views and the encumbrance, registration and title-set facts |
| `evaluateReadiness` | Activity | The DEEDINLIEU and SETTLEMENT evaluation, the outcome, the hold date and the rule version |
| `recordAndApply` | Activity | The `DecisionRecord` and the `treatment` row in one transaction through RWB-PLT-E1027-CON |
| `ReadinessRepository` | Repository | The readiness columns of `treatment` in `rwb_treatment`, with the optimistic lock of `version` |
| `AceViewReader` | Repository, read only | The SELECT against the three views by `collateral_no` and `asset_key` |
| `StageOutcomeReporter` | Signal reporter | The outcome the parent `CaseWorkflow` uses to move the case and raise the title-set task; it reports, it never changes a case row |

**Database.** `treatment` holds the readiness columns of DF-TRT-003, DF-TRT-013 and DF-TRT-014 and the standard record columns of T3.0, with the optimistic lock on `version`. No new table and no new column: the encumbrance status, the title-set status and the hold date have no field in the source and stay in the answer and the decision record (GAP-2674; ASM-4396). `decision_record` is the library object applied by the per-service Flyway sequence, written only through the library.

**Configuration and reference data.** The capability area "Treatment and offer" and right R are access rows of rwb-access, read through its guard. The three clocks and the hold limit are values in force in the rule set, read with the package version and never written in code (BR-S2-013). The grant on the three views is a DB story's, not this one's: this story reads them under the login it is given (DP-05; ASM-4395).

**Build steps**

1. The readiness branch of `TreatmentWorkflow` and its input record, registered on `rwb-treatment` as the stage child of `CaseWorkflow`, with the case signal and the route facts (AC3).
2. `AceViewReader` and `readEncumbrance` against the view fixture, read only (AC1).
3. `evaluateReadiness` against the DEEDINLIEU and SETTLEMENT packages, with the clear, blocked, resumed and returned outcomes and the title-set request (AC1, AC2, AC3).
4. `recordAndApply` with the `DecisionRecord`, the `MANDATORY` transaction and the `treatment` row, plus the failed-write path (AC4).
5. The readiness section of the answer with the guard check on right R and the error mapping of section 12.1 (AC1).
6. `StageOutcomeReporter` and the parent signal, with the two rule outcomes of AC2 and AC3 and the title-set request.
7. Tests for AC1 to AC4 against the fakes and the view fixture, plus the two component cases of section 16.

**Feature flag.** `rwb.treatment.readiness-check`.

**Done when.** The tests in section 16 pass, the step runs from a synthetic case signal in SIT, a clear mortgage orders the valuation, an unresolved mortgage blocks with its hold date, a missing title set reports the request the parent turns into a task, a repeated `asset_key` read returns the same answer, the decision record and the `treatment` row commit or roll back together, and SCR-16 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field is absent or invalid, or no collateral row is found for the case | Enter {field}. |
| MSG-P4-002 | The role does not hold right R on the capability area | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | The decision record is refused for a field | The decision record was refused: {field} is missing or not valid. |

MSG-S2-001, MSG-S2-002 and MSG-S2-003 are the offer messages of the same module and belong to RWB-S2-E3002-APP and RWB-S2-E3003-APP; the readiness check raises none of them. The message shown when the route is blocked and held has no text in any source and is Not specified in the source documents (GAP-2674; ASM-4394). The four texts above are carried unchanged from the legacy story, and no message identifier is added or renamed. MSG-P4-002 is the access answer of the guard library, and MSG-P7-003 and MSG-P7-009 are raised by RWB-PLT-E1027-CON and shown here. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-16 Deed in lieu (Checks; appraisal; approved; transferred) and SCR-14 Treatment record (Draft; submitted; approved; booked; broken) are the two legacy screens of this story and keep their state lists unchanged. The "Checks" state of SCR-16 is where the officer reads the encumbrance status, the title-set status, the hold date, the rule ID and version and the check time; the blocked state shows the hold and its review date and nothing is negotiated while it lasts. Both screens reach the service through the gateway-bff composite route, one hop each (DP-19); the screen field list and the composite route specification belong to the platform edge story and the screen owners, and this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-013-01 | AC1 | End to end | Check encumbrance and eligibility before negotiation |
| TC-E3-013-02 | AC2 | End to end | Rule R-SET-22 |
| TC-E3-013-03 | AC3 | End to end | Rule R-DIL-01 |
| TC-E3-013-04 | AC4 | End to end | Not recorded |
| TC-E3-013-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E3-013-06 | Principle 5 | Component | A forced decision log write failure stops the action with MSG-P7-003 |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character; the legacy level "System" maps to "End to end" and "Access" and "Principle 5" map to "Component", as in the other stories of this run. The readiness fake, the decision-record writer fake, the route fake and the ACE view fixture of section 12.8 stand behind every case, and the case-status mock supplies the two statuses of AC2 and AC3. The full test, with its Given, When and Then, is in the legacy test document under the same test case ID. The `-ITG` copies of these cases belong to the wave 2 integration harness and are not listed here.

### 17. Guardrails

- No value that a business person may change is written in code: the encumbrance and title statuses, the hold limit and the three clocks are values in force in the rule set, read with the package version (BR-S2-013).
- No personal data in logs, events, workflow inputs, prompts or the fixture: the rows carry case and treatment identifiers, collateral and asset keys, statuses, dates and rule versions only, and the test data is synthetic.
- No read of another service's table and no write to an ACE object: the collateral facts come from the three read-only views and the case rows are never touched (DP-01; DP-05).
- ACE data only through the owner's contract or the `v_ace_*` views, and here only through the views, with SELECT granted to this service's login and no derivation of a status in code (ASM-4395).
- No encumbrance, title-set or hold column in `rwb_treatment`; a schema change that adds one fails the guardrail test (GAP-2674; ASM-4396).
- No event of this story and no outbox row: the outcome is reported to the parent, so a replay of the stage produces no second message.
- The decision record and the `treatment` row commit in one transaction through the `MANDATORY` rule of the library; an action that commits without its record is a build failure, not a defect (DP-03).
- An applied migration is never edited: any correction to the `treatment` table is a new version on the service sequence.
- No screen calls a service directly and no screen reads a view: SCR-14 and SCR-16 go through the gateway-bff composite route (DP-19).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-005 | Deed in lieu readiness, including the encumbrance check and an early valuation, is established before negotiation starts | Program 5.9 | FEAT-TRT-13 | 07 Route, settle and claim | R-DIL-01, R-DIL-02, R-DIL-03, R-DIL-04, R-DIL-05, R-DIL-06 | TC-E3-013-01, TC-E3-013-03 |
| REQ-S2-005 | The same readiness fact on the settlement side: a title set that cannot be re-created blocks the release | Program 5.9 | FEAT-TRT-13 | 07 Route, settle and claim | R-SET-22 | TC-E3-013-02 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3013-CON | Contract | H: declares the readiness section, the title-set task request, the error set and the fakes |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record writer called in the caller's transaction with the `MANDATORY` rule |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route that SCR-14 and SCR-16 use |
| RWB-S2-E3012-APP, RWB-S2-E3012-CON | App development, Contract | Sibling: the deed-in-lieu offer that this readiness step precedes; no build dependency is recorded |
| RWB-S2-E3014-APP | App development | Sibling: the asset unlock that follows the inspection, after this check has cleared the asset |
| RWB-S2-E3001-APP, RWB-S2-E3001-CON | App development, Contract | Sibling: the treatment record and the treatment read whose answer carries the readiness section |
| S1 rwb-valuation | Service, wave 3 | Receives the valuation order that R-DIL-02 and R-DIL-03 lead to; owns FEAT-VAL-01 and FEAT-VAL-06 |
| S5 rwb-asset | Service, wave 2 | Takes the asset onto the books after the transfer; owns FEAT-AST-02 |
| P1 rwb-source-data | Service, wave 1 | Owns the ACE read; the alternative to the direct view read is its contract (ASM-4395) |
| rwb-case (P3) | Service, wave 1 | Owns the case, its status, its tasks and its timers; the stage reports and never moves or raises |
| rwb-deviation (S8) | Service, wave 2 | Owns `rwb.deviation.DeviationRaised.v1`, consumed here so the stage holds while the case clock is paused |
| Wave 2 integration harness | Integration | I: the cross-service proof of the same legacy key against the live owners, with the `-ITG` copies of the six test cases |

### 19. Out of scope

- The published shape of the readiness section, the title-set task request, the error set and the fakes: RWB-S2-E3013-CON.
- The deed-in-lieu offer, the transfer price, the floor, the second signature and the document set: RWB-S2-E3012-APP, RWB-S2-E3016-APP and RWB-S2-E3018-APP.
- The asset unlock and the field inspection: RWB-S2-E3014-APP and RWB-S2-E3015-APP.
- The treatment record, the treatment read and the treatment resource body: RWB-S2-E3001-APP and RWB-S2-E3001-CON.
- The case, its CMMN status, the parent `CaseWorkflow`, the case signal, the task and its clock: rwb-case (P3), so no case table is read or written here (ASM-4394).
- The ACE views themselves, their grant, their ingestion from CCMS and the Land Office request: P1 rwb-source-data, P2 rwb-integration and the ACE DB stories; this story reads what the views carry (ASM-4395).
- The valuation order, the appraisal and the value: S1 rwb-valuation (FEAT-VAL-01, FEAT-VAL-06) and S5 rwb-asset.
- The decision-record library, its chain, its envelope and the central ledger of P7: RWB-PLT-E1027-CON, RWB-PLT-E1027-APP and RWB-P7-E1027-APP.
- The DEEDINLIEU and SETTLEMENT rule packages, their authoring, their approval and their promotion: P7 rwb-decision, with the embedded runtime as a service-template capability (ASM-4397).
- The gateway-bff composite route and the screen field list of SCR-14 and SCR-16: RWB-PLT-N001-CON and the screen owners (DP-19).
- The deployment, the flag switch and the runbook: the platform DevOps stories of wave 2; the real cross-service proof: the wave 2 integration harness.

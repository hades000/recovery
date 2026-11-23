# RWB-S2-E3017-APP Release the collateral after settlement

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: application slice split from RWB-E3-017 for rwb-treatment. The three legacy acceptance criteria this story owns are kept word for word with their origin tag and now run on the collateral-release branch of `TreatmentWorkflow` on task queue `rwb-treatment`, reached through the gateway-bff composite route (DP-19) and served on the base `/api/recovery/treatment/v1` (DP-13); the one `recovery` schema becomes `rwb_treatment` and no other service's table is read (DP-01); the cleared balance and the securities are read from the service's own read-only `v_ace_account`, `v_ace_payment`, `v_ace_collateral` and `v_ace_collateral_detail` views (DP-05); the legacy `DecisionLogWriter` write to the shared `decision_log_entry` becomes the local decision record of RWB-PLT-E1027-CON written in the same transaction as the `treatment` row (DP-03); the shape of the release instruction, of the confirmation read and of the release message has no source and is declared as the working read (GAP-2682; ASM-4420 to ASM-4424). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3017-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S2-AB |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S2-E3017-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **case owner**, I want **the Workbench to tell CCMS to release the security once the settlement has cleared, and record the release against the case**, so that **restructures and settlements reach booking in days**.

This is the application slice of legacy RWB-E3-017. It owns:

- the three legacy acceptance criteria it carries — AC1, AC2 (R-RES-33) and AC4 — copied verbatim with their origin tag, and the rules, messages, screens and data rows they depend on;
- the collateral-release branch of `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow` owned by rwb-case, with the activities `readClearance`, `requestRelease`, `confirmRelease` and `recordAndApply`;
- the read of the four ACE views under DP-05: the zero balance of `v_ace_account`, the final installment in `v_ace_payment`, the securities in `v_ace_collateral` and the title detail in `v_ace_collateral_detail`;
- the rules R-RES-33 of the RESTRUCTURE package, R-SET-20 and R-SET-21 of the SETTLEMENT package and the release call of R-DIL-27 of the DEEDINLIEU package;
- the release request and the release confirmation as the two events of the service topic, and the stage outcome the parent uses to close the case;
- the local decision record of the request and of the confirmation, written through RWB-PLT-E1027-CON in the same transaction as the change (DP-03);
- the outcome and outcome date of the `treatment` row in schema `rwb_treatment`.

It does not own: the published shape of the release section, of the two events and of the error set, which are RWB-S2-E3017-CON; AC3 of the legacy story, which is the settlement clearance transition of R-SET-20 and is owned by RWB-ITG-E3017-ITG, so this story implements the rule and that story carries the criterion; the treatment record, the treatment read and the treatment resource body, which are RWB-S2-E3001-APP and RWB-S2-E3001-CON; the settlement offer, the floor and the approval, which are RWB-S2-E3002-APP and RWB-S2-E3003-APP; the deed-in-lieu transfer and its asset record, which are RWB-S2-E3012-APP and S5 rwb-asset; the case, its status, its tasks and its timers, which are rwb-case's; the outbound adapter that delivers a message to CCMS and the ACE ingestion that brings the CCMS fact back, which are platform and rwb-integration work; and the deployment of this build, which is the wave 2 integration harness and the platform DevOps stories.

### 2. Business rationale

Legacy RWB-E3-017 existed because a settlement that clears but leaves the security registered holds the case open and delays booking by weeks. The functional specification keeps the objective unchanged — tell CCMS to release the security once the settlement has cleared, and record the release — and the program keeps the requirement: REQ-S2-008 states that booked terms, settled accounts and released collateral are posted to their systems of record without re-keying.

What D-RCV-60 changes is where the release runs, what it reads and how the request leaves:

- the release branch runs inside `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery`, as the stage child of `CaseWorkflow`, so the release happens where the RESTRUCTURE, SETTLEMENT and DEEDINLIEU rules live and the case keeps one parent workflow from entry to closure (DP-12; Architecture v5 slides 5 and 11);
- the balance and the securities are read from the ACE views this service is granted, read only, and never from another service's table (DP-05; DP-01);
- the instruction to CCMS leaves as an event of this service on `rwb.treatment.events.v1`, carried by the outbound adapter of the platform, and never as a direct call from this service into a source system;
- the confirmation is not a message from CCMS into this service: it is the same ACE read showing the security inactive, which is exactly what the legacy story did;
- the request, the confirmation and their rule version are written to `treatment` in `rwb_treatment` with the local decision record in one transaction (DP-03);
- the case status and the clocks stay rwb-case's: the stage reports an outcome and the parent moves the case (ASM-4420);
- the officer reads the release on SCR-14 through the gateway-bff composite route, one hop (DP-19; DP-13).

No business value moves. The three criteria that rule the release — R-RES-33, R-SET-20 and R-SET-21 — keep their conditions and their events, and the release call of R-DIL-27 keeps its condition on the Land Office transfer. None of them becomes a constant of this story (BR-S2-017).

### 3. Preconditions

- RWB-S2-E3017-CON is published: the `collateralRelease` section of the treatment answer, its properties, the schemas of `rwb.treatment.CollateralReleaseRequested.v1` and `rwb.treatment.CollateralReleased.v1`, the error set, the compatibility rule and the fakes are baselined. The section and the two events have no source shape and are published as the working read (GAP-2682; ASM-4422).
- RWB-PLT-E1027-CON is published with its writer fake: `DecisionRecordWriter.record(DecisionRecord)` runs with `@Transactional(propagation = MANDATORY)`, refuses with MSG-P7-009 and fails with MSG-P7-003, so the release record and the `treatment` row commit together or not at all (DP-03).
- RWB-PLT-N001-CON is published: SCR-14 and SCR-15 reach this service through the gateway-bff composite route, one hop each, and no screen calls a service directly (DP-19).
- The four ACE views are readable by the login of rwb-treatment with SELECT only: DF-ACE-001 to DF-ACE-042 of `v_ace_account`, DF-ACE-043 to DF-ACE-054 of `v_ace_payment`, DF-ACE-091 to DF-ACE-098 of `v_ace_collateral` and DF-ACE-196 to DF-ACE-207 of `v_ace_collateral_detail`. The column that carries the legacy `in_active` fact is not among the names the source gives and is the working read of ASM-4421 (GAP-2682).
- The settlement clearance fact reaches the stage as the P8 rwb-payment event the case router forwards; where rwb-payment fixes a field name it is copied from that contract, and the name used here is the working read of ASM-4422 (GAP-2682).
- The release instruction leaves as a CloudEvent on the service topic through the outbox, and the outbound adapter that delivers it to CCMS (INT-10) is platform and rwb-integration work wired at deployment; this story names the instruction and adds no build dependency for the adapter (ASM-4424).
- The embedded Drools runtime and the RESTRUCTURE, SETTLEMENT and DEEDINLIEU packages are the service template's wave-0 capability, and the package version in force arrives on `rwb.decision.RulePackageInForce.v1`; this story names the packages and their versions and adds no build dependency of its own (ASM-4423).
- The access guard, the outbox and inbox library and the workflow kit are service-template capabilities; this story declares the capability area "Treatment and offer", the right R and the call types and adds no build dependency of its own (ASM-4398).
- The per-service Flyway sequence of rwb-treatment carries `treatment` with DF-TRT-001 to DF-TRT-033 and the library object `decision_record`; this story adds no table, no column and never edits an applied migration.
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-S2-E3017-CON when its tests pass.

### 4. Flow

1. The parent `CaseWorkflow` forwards the case signal to the running `TreatmentWorkflow` child on queue `rwb-treatment`; the stage never calls rwb-case (ASM-4420).
2. On a restructure, R-RES-33 starts the branch: the plan is PLAN_RUNNING, the plan's last installment is paid, and installments_paid equals the due count the rule set holds. The target state is PLAN_COMPLETED.
3. On a settlement, R-SET-20 starts the same branch from PAYMENT_CLEARED once the funds have cleared: the account is closed in ALS and the release of the securities read from `v_ace_collateral` is requested. The target state is COLLATERAL_RELEASE_REQUESTED.
4. On a deed in lieu, the release call of R-DIL-27 runs after the Land Office transfer: the NPA is recorded in AMIS, the debt is settled and the collateral is released in CCMS, towards ASSET_ON_BOOKS.
5. `readClearance` reads `v_ace_account` for the zero balance of the account (AC1), `v_ace_payment` for the clearing installment and `v_ace_collateral` with `v_ace_collateral_detail` for the securities and their title detail, read only and with no write to any ACE object (DP-05).
6. `requestRelease` assembles the release instruction for every active security of the account — by `collateral_no` and `asset_key`, with no personal data — and writes it to the outbox in the same transaction as the `treatment` row and the decision record; the relay publishes `rwb.treatment.CollateralReleaseRequested.v1` on `rwb.treatment.events.v1`, and the platform adapter delivers it to CCMS (AC1; ASM-4424).
7. `confirmRelease` re-reads `v_ace_collateral` and `v_ace_collateral_detail` on each ACE data-ready signal and on a durable timer, and reports the security inactive when the read shows the legacy `in_active` fact false for every security of the account (AC1; ASM-4421).
8. `recordAndApply` assembles the `DecisionRecord` — the decision code of the release event, the case and treatment, the rule ID with the package version, the recommendation, the final call and the actor — and writes it through `DecisionRecordWriter.record` in the caller's transaction, then writes `outcome` COMPLETED and `outcome_at` on the `treatment` row in the same transaction, and publishes `rwb.treatment.CollateralReleased.v1` from the outbox (DP-03; AC1, AC4).
9. The stage reports the outcome to the parent `CaseWorkflow`, which moves the case to PLAN_COMPLETED, to COLLATERAL_RELEASE_REQUESTED or to CASE_CLOSED_SETTLED per the rule, and closes the treatment; the stage writes no case row (ASM-4420; AC2).
10. The case owner reads the release on SCR-14 Treatment record through the treatment read, one hop through the gateway-bff composite route (DP-19): the release status, the securities released, the request date, the released date, the rule ID and version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The role does not hold right R on "Treatment and offer" | 403 before any read; the refusal is the guard library's and is logged by it | MSG-P4-002 | TC-E3-017-05 |
| X2 | The decision record cannot be written | `recordAndApply` throws before the `treatment` row is written and the transaction rolls back; nothing changes | MSG-P7-003 | AC4, TC-E3-017-04, TC-E3-017-06 |
| X3 | The decision record is refused for a missing or invalid field | Nothing is written and the field is named in the service log and the incident | MSG-P7-009 | AC4 |
| X4 | The account is not at a zero balance, or the final installment is absent from `v_ace_payment` | The release is not requested; the stage reports an unmatched outcome and raises a task for the case owner | MSG-GEN-001 | AC1 |
| X5 | No active security is found on `v_ace_collateral` for the account | The release is recorded as not applicable with the read time, and the parent moves the case; nothing is requested from CCMS | None in the source | AC1 |
| X6 | The re-read still shows the security active at the confirmation limit | The request stays open, the stage reports the waiting outcome and the case owner sees the request date and the rule version | Not specified in the source documents (GAP-2682; ASM-4420) | AC1 |
| X7 | The outbox row is written but the relay has not published the instruction | The transaction has committed; the relay retries and the instruction keeps its dedupe key, so CCMS receives it once | None | AC1 |
| X8 | The rule package in force is not the one the branch started on | The branch re-evaluates against the package named on `rwb.decision.RulePackageInForce.v1` and records the version it used | None | AC1 |

X1, X2 and X3 are the exception paths of RWB-E3-017 carried onto the split, X4 to X6 are the release paths the rule set and the read add, and X7 and X8 belong to the outbox and to the rule governance of the target. No limit, interval or count above is written in code: each is read from the rule set with its version (BR-S2-017).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published release contract, the decision-record library and the gateway route with their fakes, on its own schema and its own ACE views, and needs no live rwb-case, no live rwb-payment and no live CCMS to start |
| Negotiable | The activity names, the decision code per release event and the shape of the stage outcome are this story's choice; the rules, the messages, the screens and the four view tables are fixed |
| Valuable | A cleared settlement releases its security on the rule's own evidence instead of on a person's reminder, and the case closes in days |
| Estimable | One workflow branch, four activities, one view read set, one repository and one record write |
| Small | Finished inside two weeks with its tests on the fakes and the view fixture |
| Testable | Each criterion runs on synthetic treatments, balances and securities through the fake and the view fixture, plus the two component cases of the refused role and the failed record write |

### 7. Acceptance criteria

```gherkin
Feature: Release the collateral after settlement

  Scenario: AC1 Release the collateral after settlement (legacy RWB-E3-017 AC1)
    Given v_ace_account holds a zero balance for account "A-0001" and v_ace_collateral holds two active securities for it
    When the settlement has cleared
    Then the Workbench sends the release instruction to CCMS through the outbound interface
    Then it reads v_ace_collateral and v_ace_collateral_detail again and records the release against the treatment when in_active is false
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-RES-33 (legacy RWB-E3-017 AC2)
    Given the rwb-case contract mock returns case status PLAN_RUNNING
    Given a case in state PLAN_RUNNING
    When final installment paid
    Then close the treatment, release the collateral and close the case
    Then the case moves to PLAN_COMPLETED

  Scenario: AC4 Not recorded (legacy RWB-E3-017 AC4)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Target reading.** Every line and every value above is the legacy line and the legacy value, unchanged, including the repetition of `Then` and the legacy wording `the action is taken` and `the decision log cannot be written`; what changes is where it runs, what produces the fact and how the instruction leaves. The one added line is the mock Given of AC2, which stands in for the case status that rwb-case owns, so the branch can be tested before the live case workflow exists (ASM-4420). AC1 needs no such line: its cross-service part is the CCMS instruction, which is an outbound port stubbed by the adapter fake and not a service contract of the 19, so the WP records no C dependency for it (ASM-4424).

The release runs on the release branch of `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery`, with the activities `readClearance`, `requestRelease`, `confirmRelease` and `recordAndApply` (Architecture v5 slides 5 and 11; DP-12). The balance and the securities of AC1 are read from `v_ace_account`, `v_ace_payment`, `v_ace_collateral` and `v_ace_collateral_detail` under DP-05, read only; the legacy `in_active` fact is a column of that read and never derived in code, and the column name is the working read (GAP-2682; ASM-4421). "The outbound interface" of AC1 is the release event `rwb.treatment.CollateralReleaseRequested.v1` on `rwb.treatment.events.v1`, published from the outbox and carried to CCMS by the platform adapter, so the test asserts the event on the topic and its delivery by the fake (ASM-4424). "The decision log" of AC1 and AC4 is the local decision record of `decision_record` in `rwb_treatment`, written through RWB-PLT-E1027-CON with `@Transactional(propagation = MANDATORY)` in the same transaction as the `treatment` row; `decision_log_entry` is P7's central ledger and is neither written nor read here (DP-03). The states of AC2 — PLAN_RUNNING and PLAN_COMPLETED — are case statuses of rwb-case: the stage reports the outcome and the parent moves the status, so the transition is proved against the mock and not by a write of this service (ASM-4420). R-SET-20's AC3 is carried by RWB-ITG-E3017-ITG and its test TC-E3-017-03 is listed in section 16 as the settlement-side trace of the same branch.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A running plan whose last installment is paid closes the treatment, releases the collateral and closes the case, and the case moves to PLAN_COMPLETED | R-RES-33; REQ-S2-008 |
| BR2 | Cleared settlement funds close the account in ALS and request the release of the securities read from `v_ace_collateral`, and the case moves to COLLATERAL_RELEASE_REQUESTED | R-SET-20 |
| BR3 | A release confirmed by CCMS returns the title, closes the treatment and closes the case, and the case moves to CASE_CLOSED_SETTLED | R-SET-21 |
| BR4 | A deed in lieu whose ownership has transferred at the Land Office records the NPA in AMIS, settles the debt and releases the collateral in CCMS, and the case moves to ASSET_ON_BOOKS | R-DIL-27 |
| BR5 | The release is recorded against the treatment only when the re-read of the two collateral views shows the security inactive; the request and the confirmation are both recorded | Legacy AC1; ASM-4421 |
| BR6 | The decision is recorded with the rule version in the same transaction as the change; if it cannot be recorded, nothing changes | BR-S2-017; DP-03; MSG-P7-003 |
| BR7 | No value a business person may change is written in code: the conditions, the clocks and the limits are read from the rule set in force with its version | BR-S2-017 |
| BR8 | The case status, the task and the clock are not this service's: the stage reports an outcome and the parent moves the case and raises the task | DP-01; ASM-4420 |

**Where each rule lives in the target.** BR1, BR2 and BR4 are the rule evaluation of `requestRelease` and BR3 is the one of `confirmRelease`, against the RESTRUCTURE, SETTLEMENT and DEEDINLIEU packages, with every condition taken from the view read and no threshold in code. BR5 is the two-step shape of the branch: the request event after `requestRelease`, the `treatment` outcome after `confirmRelease`. BR6 is the `MANDATORY` transaction of the library, so the `treatment` row, the outbox row and the `decision_record` row commit together or not at all. BR7 is the reason the due count, the confirmation limit and the confirmation interval are read with the package version and are never configured here. BR8 is the reason the stage outcome carries the request and the parent moves the case and raises the task.

### 9. State transitions

The case status is rwb-case's and is not changed by this story: the branch reports an outcome and the parent `CaseWorkflow` moves the case (ASM-4420). The transitions below are the rule set's, and each row is one outcome this story reports.

| From | Event | Condition | To (rule) |
|---|---|---|---|
| PLAN_RUNNING | FINAL_INSTALLMENT_PAID | installments_paid = installments_due | PLAN_COMPLETED (R-RES-33) |
| PAYMENT_CLEARED | CLEARANCE_CONFIRMED | funds cleared | COLLATERAL_RELEASE_REQUESTED (R-SET-20) |
| COLLATERAL_RELEASE_REQUESTED | COLLATERAL_RELEASED | CCMS confirms the release | CASE_CLOSED_SETTLED (R-SET-21) |
| AWAITING_TRANSFER | TRANSFER_COMPLETED | product = MTG and ownership transferred at the Land Office | ASSET_ON_BOOKS (R-DIL-27) |

| `treatment.state` | Event | Condition | To |
|---|---|---|---|
| Draft, submitted or booked | release requested | R-RES-33, R-SET-20 or R-DIL-27 fires | unchanged, with the request reference and its date written |
| Booked or approved | release confirmed | the re-read shows the security inactive | unchanged, with `outcome` COMPLETED and `outcome_at` written |
| Booked or approved | decision record refused or failed | X2, X3 | unchanged |

The release branch moves from running to waiting on the request and ends when the parent closes the stage. No release state of its own is stored: the answer is the outcome columns, the request reference and the decision record, and the case states above stay the parent's. R-SET-23, the reversal after a release, is the settlement reversal path of another story and is not part of this branch.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery squad (RW-TRIBE) | Writes the release branch, the four activities, the view read and the repository |
| RW-CASEOWN, case owner | Reads the release, holds the case where the release is not confirmed and receives the unmatched task; holds CRU |
| RW-RESTRUCT, restructuring officer (FCR) | Reads the release and acts on a returned case; holds CRUA |
| RW-SPECIAL, RW-GUARANT | Read the release; hold CRU |
| RW-CREDCOMM, RW-PRODHEAD | Hold RA on the capability area; no approval is made in this story |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL | Read the release; right R only |
| SY-CASEWF, SY-RULES, SY-AGENT | Read as service identities, subject to the same checks |
| The release branch itself | Runs unattended: the trigger is the rule's event and no person acts |
| The case status, the task and its clock | Not this story: rwb-case owns them and the parent moves and raises (ASM-4420) |
| The CCMS instruction and the ACE ingestion | Not this story: the outbound adapter and ACE ingestion are platform and P1 work (ASM-4424) |

The rights above are those of TSD S2 T6.1 for the capability area "Treatment and offer", and the check itself is the platform guard library's: this story declares the area and the right R and calls the guard, and it owns no check of its own. No delegation of authority level applies, because a release after a cleared settlement is not a credit decision. No credential and no personal name appears in the request, the payloads or the logs, which carry case, treatment, account, collateral and asset identifiers, amounts, statuses, dates and rule versions only.

### 11. Data

| BR Field ID | Entity or view | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-003 | treatment | decision_log_id | Write: the entry id returned by `DecisionRecordWriter.record` |
| DF-TRT-004 | treatment | treatment_type | Read: RESTRUCTURE, SETTLEMENT or DEED_IN_LIEU |
| DF-TRT-009 | treatment | installments | Read: the due count R-RES-33 compares |
| DF-TRT-013 | treatment | outcome | Write: COMPLETED |
| DF-TRT-014 | treatment | outcome_at | Write |
| DF-TRT-032 | treatment | installments_paid | Read |
| T3.0 `state`, `version`, `updated_at`, `updated_by` | treatment | standard record columns | Write |
| DF-DEC-001 to DF-DEC-018 | decision_record | the record fields of the library | Write through RWB-PLT-E1027-CON |
| DF-ACE-001 to DF-ACE-042 | v_ace_account | account_key, account_code, account_status, contract_no, product_category_efs, total_balance and 36 more | Read only |
| DF-ACE-043 to DF-ACE-054 | v_ace_payment | payment_code, account_key, payment_date, payment_amount, payment_channel, capital_amount and 6 more | Read only |
| DF-ACE-091 to DF-ACE-098 | v_ace_collateral | collateral_no, asset_key, account_key, collateral_value, collateral_type, register_date and 2 more | Read only |
| DF-ACE-196 to DF-ACE-207 | v_ace_collateral_detail | asset_key, title_doc_no, plot_no, area_text, province, lien_rank and 6 more | Read only |
| DF-CAS-001 to DF-CAS-023 | rwb-case | case, status and stage rows | Not read and not written: the parent owns them (ASM-4420) |

`treatment` is the only business table this story writes, in schema `rwb_treatment` and through this service's own login (DP-01). The four views are read with SELECT only under DP-05 and no ACE object is written; the `decision_record` row is a library object of RWB-PLT-E1027-CON written in the caller's transaction, and `decision_log_entry` in `rwb_decision` is P7's and is named here only. The release status, the request reference, the released date and the confirmed date are not columns of `rwb_treatment`: no source gives them one and TSD S2 T3.1 carries no such field, so they travel in the answer, in the two events and in the decision record (GAP-2682; ASM-4422). The legacy condition of R-RES-33 names `installments_due` and TSD S2 T3.1 carries `installments` and `installments_paid` only, so the comparison is made on those two fields and the naming is the working read (GAP-2682; ASM-4422).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). None of its own. The release answer is served as the optional `collateralRelease` section of the treatment read `GET /treatments/{treatmentId}`, whose operation entry belongs to RWB-S2-E3001-CON and whose section is declared by RWB-S2-E3017-CON as a compatible addition at major version 1. This story fills that section and publishes no operation entry: the release is started by the rule on the case signal and the officer takes no action in it, so there is no write operation to publish, and the legacy endpoint table of RWB-E3-017 names the treatment create and the treatment read only, both of which are RWB-S2-E3001-CON's (GAP-2682; ASM-4422).

The section carries the release status, the securities released by `collateral_no` and `asset_key`, the request reference and date, the released date, the read time and the rule ID and version — the property names are the working read of the contract story and are not restated here.

#### 12.2 REST operations consumed

None. The case signal arrives on the parent's signal, the clearance arrives on the rwb-payment event, the balance and the securities are read from this service's own views, and the decision record is called in process inside the caller's transaction (DP-03; DP-05; ASM-4420). This is why the Work Package records no C dependency for this story.

#### 12.3 Events published

| Event | Topic | Trigger | Payload (no personal data) |
|---|---|---|---|
| `rwb.treatment.CollateralReleaseRequested.v1` | `rwb.treatment.events.v1` | R-RES-33, R-SET-20 or R-DIL-27 requests the release | Case, treatment, account key, the `collateral_no` and `asset_key` list, the request reference, the request date, the rule ID and version |
| `rwb.treatment.CollateralReleased.v1` | `rwb.treatment.events.v1` | The re-read shows every security of the account inactive | Case, treatment, account key, the released securities, the released date, the read time, the rule ID and version |

Both events are written to the outbox in the same transaction as the `treatment` row (DP-09 semantics through the service template), carry a CloudEvents envelope with a stable dedupe key derived from the release request reference, and are published in order by the relay; a redelivery is deduplicated by the consumer. Their names and their payloads are published by RWB-S2-E3017-CON as the working read (ASM-4422). `TreatmentApproved` (EV-10) and `TreatmentBooked` (EV-11) belong to the approval and booking stories of this module.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.payment.PaymentCleared.v1` | `rwb.payment.events.v1` | P8 rwb-payment | The settlement clearance that starts R-SET-20; the name is the working read of ASM-4422 (GAP-2682) |
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 rwb-decision | The RESTRUCTURE, SETTLEMENT and DEEDINLIEU package versions in force, so each release is evaluated and recorded with the version it used |
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | S8 rwb-deviation | A deviation raised on the case, so the branch holds while the case clock is paused |

All three arrive through the inbox of the outbox library, deduplicated by cloud event id, so a redelivery changes nothing. The case status change is not an event of this table: it arrives as the signal the parent forwards (ASM-4420). The confirmation of a release is not an event either: it is the re-read of the two collateral views (AC1).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` (collateral-release branch) | Workflow, one execution per case per stage, the child of `CaseWorkflow` | `rwb-treatment` in namespace `rwb-recovery` | Input: the case, treatment, account key and rule route; signals: the case status forwarded by the parent, the payment clearance, the rule package in force, the deviation and the ACE data-ready tick |
| `readClearance` | Activity | `rwb-treatment` | The account, payment and collateral keys in; the zero balance, the clearing installment, the securities and the title detail out, read only |
| `requestRelease` | Activity | `rwb-treatment` | The instruction out: the securities, the request reference, the rule ID and version, and the outbox row in the caller's transaction |
| `confirmRelease` | Activity | `rwb-treatment` | The re-read in; the per-security active fact, the released date and the read time out |
| `recordAndApply` | Activity | `rwb-treatment` | The `DecisionRecord`, the `treatment` row and the second outbox row written in one transaction through RWB-PLT-E1027-CON, and the stage outcome for the parent |

The branch is one branch of the single `TreatmentWorkflow` the service owns, and the parent-and-child model with the steps of receive, ask, record and apply, wait is the one of the target design (DP-12; Architecture v5 slides 5 and 11). The activity names are a design choice of this story and are fixed by no source document. A workflow class never calls the decision-record library directly: the call is made inside `recordAndApply`, so a replay reuses the recorded decision.

#### 12.6 Schedules

None. The branch runs from the rule's event and waits on a durable workflow timer for the confirmation read; the interval and the limit of that wait are values in force in the rule set and are Not specified in the source documents (GAP-2682; ASM-4422). The service has no legacy Quartz job in this legacy key, so nothing becomes a Temporal Schedule.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 rwb-treatment | Written for `decision_log_id`, `outcome`, `outcome_at` and the standard record columns; created by the per-service Flyway sequence and never re-created here |
| `decision_record` | `rwb_treatment` | PLT, library object | Not written directly: the row is written by RWB-PLT-E1027-CON in the caller's transaction (DP-03) |
| `v_ace_account`, `v_ace_payment`, `v_ace_collateral`, `v_ace_collateral_detail` | `recovery` (read-only views) | ACE, read through DP-05 | Read only; never written and never owned |

No table of another service is read and no foreign key crosses a schema (DP-01). The case, its status, its tasks and its timers are rwb-case's and are not read here (ASM-4420). No release, request-reference or released-date column is added to `treatment`, because no source gives one (GAP-2682; ASM-4422).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S2-E3017-CON release fake | The `collateralRelease` section, the two event schemas and the error set | Two active securities released; a security still active at the read time; an account with no active security; a treatment with no release record |
| RWB-PLT-E1027-CON writer fake | The decision record | An accepted record with chain sequence and entry hash; a refusal with MSG-P7-009 and the field; a failed write raising MSG-P7-003 |
| RWB-PLT-N001-CON route fake | The gateway-bff composite route | A composite answer for SCR-14 that joins the treatment read and its release section; a refused route for a role without right R |
| rwb-case case-status mock | The signal the parent forwards, used by AC2 | A case at PLAN_RUNNING; a case status the branch does not accept. Test-only, adds no contract dependency (ASM-4420) |
| CCMS outbound adapter fake | The delivery of `CollateralReleaseRequested` | Accepted with a request reference; a transport failure that leaves the outbox row unpublished for the relay to retry (ASM-4424) |
| ACE view fixture | The read of the four views | A zero-balance account with two active securities and one clearing installment; a security whose `in_active` fact turns false on the second read; a balance that is not zero; an account with no security |

The release fake is the published contract of RWB-S2-E3017-CON; the case-status mock, the adapter fake and the view fixture stand in for the signal of the parent, the outbound delivery and the ACE read, which have no published shape of their own here (GAP-2682; ASM-4420, ASM-4421, ASM-4424).

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 operations of its own | 0 | The release section is served inside the treatment read of RWB-S2-E3001-CON |
| Kafka | 2 events (`rwb.treatment.CollateralReleaseRequested.v1`, `rwb.treatment.CollateralReleased.v1`) | 3 events (`rwb.payment.PaymentCleared.v1`, `rwb.decision.RulePackageInForce.v1`, `rwb.deviation.DeviationRaised.v1`) | Outbox and inbox, dedupe by cloud event id, retry and `.dlt` topics per service |
| Temporal | 0 | `TreatmentWorkflow` release branch and 4 activities on `rwb-treatment` | Namespace `rwb-recovery`; stage child of `CaseWorkflow`; no Schedule |
| SQL view | 0 | 4 read-only ACE views | SELECT only under DP-05; no write to any ACE object |
| File, Nexus | 0 | 0 | The CCMS instruction is a Kafka message carried by the platform adapter, not a file and not a Nexus operation |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, modules `release` and `web`, with the published types in `...treatment.api`. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule of the release: the record, the outbox row and the `treatment` row commit together, and a failed record leaves nothing behind. DP-05 is the read of the four views, taken as this service's own read-only views, which is the form that adds no dependency; the alternative, the contract read of rwb-source-data, would be a C dependency and is not taken here (ASM-4421). DP-13 moves the base of the operations the screens use and nothing else. DP-19 is how SCR-14 and SCR-15 reach this service, one hop through the gateway, so no screen reads a view or a table.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentWorkflow` release branch | Workflow | One execution per case per stage; the route facts, the account key, the package in force and the stage outcome |
| `readClearance` | Activity | The read of the four views and the balance, installment, security and title facts |
| `requestRelease` | Activity | The release instruction, the request reference and the outbox row of the request event |
| `confirmRelease` | Activity | The re-read of the two collateral views and the per-security inactive fact |
| `recordAndApply` | Activity | The `DecisionRecord`, the `treatment` row and the second outbox row in one transaction |
| `TreatmentReleaseRepository` | Repository | The release columns of `treatment` in `rwb_treatment`, with the optimistic lock of `version` |
| `AceViewReader` | Repository, read only | The SELECT against the four views by `account_key`, `collateral_no` and `asset_key` |
| `ReleasePublisher` | Outbox publisher | The two events of section 12.3 written in the caller's transaction and relayed with their dedupe key |

**Database.** `treatment` holds DF-TRT-003, DF-TRT-013 and DF-TRT-014 and the standard record columns of T3.0, with the optimistic lock on `version`. No new table and no new column: the release status, the request reference and the released date have no field in the source and stay in the answer, the two events and the decision record (GAP-2682; ASM-4422). `decision_record` is the library object applied by the per-service Flyway sequence, written only through the library.

**Configuration and reference data.** The capability area "Treatment and offer" and right R are access rows of rwb-access, read through its guard. The due count comparison, the confirmation limit and the confirmation interval are values in force in the rule set, read with the package version and never written in code (BR-S2-017). The grant on the four views is a DB story's, not this one's: this story reads them under the login it is given (DP-05; ASM-4421).

**Build steps**

1. The release branch of `TreatmentWorkflow` and its input record, registered on `rwb-treatment` as the stage child of `CaseWorkflow`, with the case signal and the rule route (AC2).
2. `AceViewReader` and `readClearance` against the view fixture, read only (AC1).
3. `requestRelease` with the instruction, the request reference and the outbox row, plus the adapter fake (AC1).
4. `confirmRelease` with the re-read, the per-security inactive fact and the waiting path of X6 (AC1).
5. `recordAndApply` with the `DecisionRecord`, the `MANDATORY` transaction, the `treatment` row and the second outbox row, plus the failed-write path (AC4).
6. The release section of the answer with the guard check on right R and the error mapping of section 12.1 (AC1).
7. The stage outcome with the four rule outcomes of section 9 and the parent signal (AC1, AC2).
8. Tests for AC1, AC2 and AC4 against the fakes and the view fixture, plus the two component cases of section 16.

**Feature flag.** `rwb.treatment.collateral-release`.

**Done when.** The tests in section 16 pass, the branch runs from a synthetic case signal in SIT, a zero-balance account with two active securities publishes one request event, the re-read of an inactive security writes the outcome and publishes one confirmation event, a balance that is not zero publishes nothing, a repeated read returns the same answer, the decision record, the outbox rows and the `treatment` row commit or roll back together, and SCR-14 answers through the gateway-bff composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field is absent or invalid, the balance is not zero, or no security is found for the account | Enter {field}. |
| MSG-P4-002 | The role does not hold right R on the capability area | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | The decision record is refused for a field | The decision record was refused: {field} is missing or not valid. |

MSG-S2-001, MSG-S2-002 and MSG-S2-003 are the offer messages of the same module and belong to RWB-S2-E3002-APP and RWB-S2-E3003-APP; the release raises none of them. The message shown while a release is requested and not yet confirmed has no text in any source and is Not specified in the source documents (GAP-2682; ASM-4420). The four texts above are carried unchanged from the legacy story, and no message identifier is added or renamed. MSG-P4-002 is the access answer of the guard library, and MSG-P7-003 and MSG-P7-009 are raised by RWB-PLT-E1027-CON and shown here. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-14 Treatment record (Draft; submitted; approved; booked; broken) and SCR-15 Settlement offer (Draft; below floor; approved; sent; accepted) are the two legacy screens of this story and keep their state lists unchanged. The release facts the officer reads on SCR-14 are the release status, the securities released with their `collateral_no` and `asset_key`, the request date, the released date, the read time and the rule ID and version; while the request is open the case owner sees the request date and the rule version, and nothing else is decided on the screen. Both screens reach the service through the gateway-bff composite route, one hop each (DP-19); the screen field list and the composite route specification belong to the platform edge story and the screen owners, and this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-017-01 | AC1 | End to end | Release the collateral after settlement |
| TC-E3-017-02 | AC2 | End to end | Rule R-RES-33 |
| TC-E3-017-03 | AC3 | End to end | Rule R-SET-20 |
| TC-E3-017-04 | AC4 | End to end | Not recorded |
| TC-E3-017-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E3-017-06 | Principle 5 | Component | A forced decision log write failure stops the action with MSG-P7-003 |

The six legacy test case IDs, their Covers and their Data are kept in order and character for character; the legacy level "System" maps to "End to end" and "Access" and "Principle 5" map to "Component", as in the other stories of this run. TC-E3-017-03 covers AC3, whose criterion is owned by RWB-ITG-E3017-ITG; it is kept here because it runs on the same release branch and the Work Package lists the whole legacy set for this story, and its cross-service proof is the harness's. The release fake, the decision-record writer fake, the route fake, the adapter fake and the ACE view fixture of section 12.8 stand behind every case, and the case-status mock supplies the status of AC2. The full test, with its Given, When and Then, is in the legacy test document under the same test case ID. The `-ITG` copies of these cases belong to the wave 2 integration harness and are not listed here.

### 17. Guardrails

- No value that a business person may change is written in code: the conditions, the due count, the confirmation limit and the confirmation interval are values in force in the rule set, read with the package version (BR-S2-017).
- No personal data in logs, events, workflow inputs, prompts or the fixture: the rows carry case, treatment, account, collateral and asset identifiers, amounts, statuses, dates and rule versions only, and the test data is synthetic.
- No read of another service's table and no write to an ACE object: the balance and the securities come from the four read-only views and the case rows are never touched (DP-01; DP-05).
- ACE data only through the owner's contract or the `v_ace_*` views, and here only through the views, with SELECT granted to this service's login and no derivation of the `in_active` fact in code (ASM-4421).
- No release, request-reference or released-date column in `rwb_treatment`; a schema change that adds one fails the guardrail test (GAP-2682; ASM-4422).
- The two events carry a business key, a status, a date and a rule version and no name, national identifier or account number; the outbox row is written in the same transaction as the change, so a rollback publishes nothing.
- The decision record, the outbox rows and the `treatment` row commit in one transaction through the `MANDATORY` rule of the library; an action that commits without its record is a build failure, not a defect (DP-03).
- An applied migration is never edited: any correction to the `treatment` table is a new version on the service sequence.
- No screen calls a service directly and no screen reads a view: SCR-14 and SCR-15 go through the gateway-bff composite route (DP-19).
- No direct call from this service to CCMS or to any source system: the instruction is an event of this service, carried by the platform adapter (ASM-4424).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-008 | Booked terms, settled accounts and released collateral are posted to their systems of record without re-keying | Program 5.9 | FEAT-TRT-17 | 07 Route, settle and claim | R-RES-33, R-SET-20, R-SET-21, R-DIL-27 | TC-E3-017-01, TC-E3-017-02, TC-E3-017-04 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3017-CON | Contract | H: declares the `collateralRelease` section, the two event schemas, the error set and the fakes |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record writer called in the caller's transaction with the `MANDATORY` rule |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route that SCR-14 and SCR-15 use |
| RWB-S2-E3001-APP, RWB-S2-E3001-CON | App development, Contract | Sibling: the treatment record and the treatment read whose answer carries the release section |
| RWB-S2-E3002-APP, RWB-S2-E3003-APP | App development | Sibling: the settlement offer and the approval below the floor that precede the clearance |
| RWB-S2-E3012-APP | App development | Sibling: the deed-in-lieu transfer whose completion leads to the release call of R-DIL-27 |
| RWB-ITG-E3017-ITG | Integration | Owner of legacy AC3 and of the cross-service proof of this legacy key, with the `-ITG` copies of the six test cases |
| P8 rwb-payment | Service, wave 2 | Publishes the clearance that starts R-SET-20 and the payment facts of `v_ace_payment` |
| P7 rwb-decision | Service, wave 1 | Owns the rule packages in force and the central ledger the local record is sealed into |
| S8 rwb-deviation | Service, wave 2 | Owns `rwb.deviation.DeviationRaised.v1`, consumed here so the branch holds while the case clock is paused |
| S5 rwb-asset | Service, wave 2 | Takes the asset onto the books after a deed-in-lieu transfer |
| P1 rwb-source-data | Service, wave 1 | Owns the ACE read; the alternative to the direct view read is its contract (ASM-4421) |
| rwb-case (P3) | Service, wave 1 | Owns the case, its status, its tasks and its timers; the stage reports and never moves or raises |
| Wave 2 integration harness | Integration | I: the cross-service proof of the release path against the live owners, with the `-ITG` copies of the six test cases |

### 19. Out of scope

- The published shape of the release section, of the two events, of the error set and of the fakes: RWB-S2-E3017-CON.
- Legacy AC3 and the settlement clearance transition of R-SET-20 as a criterion: RWB-ITG-E3017-ITG, which proves it across services; the rule itself is implemented here.
- The treatment record, the treatment read and the treatment resource body: RWB-S2-E3001-APP and RWB-S2-E3001-CON.
- The settlement offer, the floor, the approval below the floor and the payoff freshness: RWB-S2-E3002-APP, RWB-S2-E3003-APP and RWB-S2-E3006-APP.
- The deed-in-lieu transfer, its inspection and its asset record: RWB-S2-E3012-APP, RWB-S2-E3014-APP and S5 rwb-asset.
- The settlement reversal after a release (R-SET-23): the reversal path of RWB-S2-E3015-APP.
- The case, its CMMN status, the parent `CaseWorkflow`, the case signal, the task and its clock: rwb-case (P3), so no case table is read or written here (ASM-4420).
- The release instruction adapter to CCMS and its file or message format (INT-10), and the ACE ingestion of the CCMS result: P2 rwb-integration, the platform integration stories and the ACE DB stories (ASM-4424).
- The ACE views themselves and their grant: P1 rwb-source-data and the ACE DB stories; this story reads what the views carry (ASM-4421).
- The decision-record library, its chain, its envelope and the central ledger of P7: RWB-PLT-E1027-CON, RWB-PLT-E1027-APP and RWB-P7-E1027-APP.
- The RESTRUCTURE, SETTLEMENT and DEEDINLIEU rule packages, their authoring, their approval and their promotion: P7 rwb-decision, with the embedded runtime as a service-template capability (ASM-4423).
- The gateway-bff composite route and the screen field list of SCR-14 and SCR-15: RWB-PLT-N001-CON and the screen owners (DP-19).
- The deployment, the flag switch and the runbook: the platform DevOps stories of wave 2; the real cross-service proof: the wave 2 integration harness.

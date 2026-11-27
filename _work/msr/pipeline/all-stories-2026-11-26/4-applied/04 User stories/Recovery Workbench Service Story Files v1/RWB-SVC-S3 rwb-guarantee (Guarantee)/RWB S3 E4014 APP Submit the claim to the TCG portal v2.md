# RWB-S3-E4014-APP Submit the claim to the TCG portal

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E4-014 split out for rwb-guarantee. The filing leaves the monolith's method of `GuaranteesAndGuarantorsService` and becomes the submit branch of `GuaranteeClaimWorkflow` on this service's own task queue; the filing is written on `guarantee_claim` in `rwb_guarantee` with its local decision record in the same transaction (DP-03); the account facts are read at the ACE batch date from this service's own SELECT-only `recovery.v_ace_*` views and are never copied (DP-05); the case moves on the stage report to the parent `CaseWorkflow` and never by a case write; the officer's two operations sit on base `/api/recovery/guarantee/v1` (DP-13) and are reached through the gateway-bff composite route (DP-19); the four legacy criteria this story owns are copied word for word with their origin tag. No source gives the submission reference a field (GAP-2711; ASM-4503), publishes an interface to the TCG claim channel (GAP-2711; ASM-4504) or maps the seventeen rule states to the claim status list (GAP-2711; ASM-4505). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S3-E4014-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S3-E4014-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-guarantee |
| Service epic | RWB-SVC-S3 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-014 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-S3-C |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S3-E4014-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S3 rwb-guarantee v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **guarantee officer (RW-GUARANT)**, I want **a verified guarantee claim to be filed through the TCG claim channel by the submit branch of `GuaranteeClaimWorkflow`, with the filing written on the claim row, the submission reference recorded and the case moved to `CLAIM_SUBMITTED` on the stage report** — so that **no guarantee claim misses its deadline, which is the failure the module exists to prevent**.

This is the application slice of legacy RWB-E4-014. It owns:

- the four legacy acceptance criteria this story is given (AC1 to AC4), copied verbatim with their origin tag, and the rules, rows, states and messages they carry;
- the submit branch of `GuaranteeClaimWorkflow` on task queue `rwb-guarantee` in namespace `rwb-recovery`: the step that evaluates the `GUA` rule set (32 rules over 17 states) at the approval of the case and records the filing (Temporal and Drools Design slides 5 and 13; TSD S3 T4);
- the two answers of the rule set that this story files: R-GUA-12 (the guarantee officer verifies the claim at D6.5, submit through the TCG claim channel, to `CLAIM_SUBMITTED`, timer 2 working days) and R-GUA-21 (the unpaid share is still claimable inside the deadline, submit the balance claim, to `CLAIM_SUBMITTED`, timer 5 working days), with their condition terms, owners and timers carried unchanged (Business Rules and Routing Logic v4);
- the filing write on `guarantee_claim` in `rwb_guarantee`: `status` takes `FILED` of LOV-CLAIM-STATUS and `filed_at` the business date, with the local decision record of the step written through `DecisionRecordWriter.record(DecisionRecord)` in the caller's transaction (DP-03; RWB-PLT-E1027-CON);
- the account facts of the claim at the ACE batch date: the guaranteed contract, its status and its outstanding balance read only from this service's own SELECT-only views, kept as no column of this service (DP-05; D-RCV-35);
- the freshness guard VR-S3-002-1 on `recovery.v_ace_batch_status`, so a stale data product blocks the filing instead of filing on yesterday's facts;
- the stage report to the parent `CaseWorkflow` carrying `CLAIM_SUBMITTED` and the rule version, because the case status, the case task and the case timer are rwb-case's (DP-12);
- the officer's two operations of RWB-S3-E4014-CON — `POST /api/recovery/guarantee/v1/cases/{caseId}/guarantee-claims` and `PATCH /api/recovery/guarantee/v1/guarantee-claims/{claimId}` — implemented behind the published shape, and the `submitted` state of SCR-17 reached through the gateway-bff composite route (DP-13; DP-19);
- the refusal and failure paths: no record, nothing changes and MSG-P7-003; a role without the right is refused with MSG-P4-002; a missing value is named with MSG-GEN-001; a stale product blocks with MSG-P1-001.

It does not own: the published resource shape, the DDL template, the error set, the versioning rule and the fakes, which are RWB-S3-E4014-CON; the preparation of the claim and its checklist, which are RWB-S3-E4013-APP; the tracking of the claim to payment, the service level breach and the lost claim, which are RWB-S3-E4015-APP; the subrogation position, which is RWB-S3-E4016-APP; the case, its status, its tasks and its timers, which are rwb-case's; the rule package, its approval and the central ledger, which are P7 rwb-decision's; the TCG portal itself, which is INT-29 and outside the cluster.

### 2. Business rationale

In the monolith the filing was a method of `GuaranteesAndGuarantorsService` behind `GuaranteesAndGuarantorsController`: it read the case and the account from the one `recovery` schema, wrote the claim into `recovery.guarantee_claim`, wrote `decision_log_entry` beside it and moved the case status in the same transaction, all in one process and one schema (TSD S3 T2). The consequence was the one the module was built to avoid — the claim deadline and the filing lived in the same code as the case, so the step could not be released, scaled or proved on its own, and a guarantee claim that stopped because the process stopped left no trace of why.

D-RCV-60 changes the source of each input and the owner of each fact, and nothing about the officer's work. The claim becomes a row of `rwb_guarantee` with its own login and no cross-schema key (DP-01, DP-02). The account and its balance stay in ACE and are read at the ACE batch date through this service's own SELECT-only views, with the product's date on the answer, and are never copied (DP-05; D-RCV-35, ADR-010). The decision is recorded locally in the same transaction as the filing, so a filing that cannot be recorded does not happen (DP-03; ADR-022). The case moves because the stage reports and the parent applies the rule, never because this service writes a case row (DP-01, DP-12).

The filing is a branch of the stage workflow the service already owns: one child per case on the owner's queue `rwb-guarantee`, event in, rule decides, person signs, timer waits (Temporal and Drools Design slides 5 and 13; Architecture v5 slides 3 and 13). The rules that name the behaviour are the GUA rows R-GUA-12 and R-GUA-21, whose from states, events, conditions, actions, timers and systems are carried into the split character for character.

Two facts of the target are recorded rather than designed away. The first is that INT-29 — the TCG claim channel — is "not available today; entered and filed by the guarantee officer", so the submission is an officer action the service records, and no outbound call, file or queue is invented for it (GAP-2711; ASM-4504). The second is that the legacy story says the submission reference is recorded "on the case" while TSD S3 T3.1 gives `guarantee_claim` eight fields and none of them holds a reference, so v1 records the filing by status and date and the reference waits for a field identifier (GAP-2711; ASM-4503).

Delivery is EP04 in wave 3 on release 28 February 2027 (tentative). REQ-S3-001 of FSD S3 — "a guarantee claim is prepared from case data and submitted inside the guarantor's deadline" — is the requirement this story traces to, and REQ-S3-002 carries the status write (Section 18).

### 3. Preconditions

- RWB-S3-E4014-CON is published: `GuaranteeClaimRequest`, `GuaranteeClaimUpdate` and `GuaranteeClaim` over the eight DF-TRT fields, the `guarantee_claim` DDL template, the error set, the `Idempotency-Key` rule and the fakes. The build starts against the Draft baseline, because every CON story of this run publishes on Day 1 at status Draft (realignment v1).
- RWB-PLT-E1027-CON is published: `DecisionRecordWriter`, `DecisionRecord`, the `MANDATORY` propagation, the refusal with MSG-P7-009 and the failure with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-17 from the case read and this service's claim read (DP-19).
- The `rwb_guarantee` schema and its login exist from the platform database story, and `guarantee_claim` is on the per-service Flyway sequence with DF-TRT-015 to DF-TRT-022 of TSD S3 T3.1 and the seven standard columns of T3.0; `decision_record` is created as the platform library object in the same schema (DP-01; DP-15).
- SELECT on `recovery.v_ace_account` and `recovery.v_ace_batch_status` is granted to this service's login and on no other ACE object. Architecture v5 slide 8 says the 30 `recovery.v_ace_*` views are read only by rwb-source-data while DP-05 allows a service's own SELECT-only views; the grant is the working read of ASM-4506, which this story carries rather than re-raises, and the Work Package records no contract dependency on P1.
- The case is in `CLAIM_APPROVAL` on the case signal the parent `CaseWorkflow` forwards, the claim row is in state `PREPARING` with `claim_type`, `claim_deadline` and `claimed_amount`, and for R-GUA-21 the case is in `CLAIM_PART_PAID` with `paid_amount` below `claimed_amount` (DF-TRT-016 to DF-TRT-021).
- The `GUA` package and route set are in this service's rule cache at the version the answer names; the rule identifiers, the condition texts and the two timers of 2 and 5 working days are rule rows, not code (EV-30; BR-S3-002).
- No approval stop: FSD S3 v3 and TSD S3 v2 carry status "In review", and nothing in this story needs a human sign-off to start on Day 1 (ASM-4510).

### 4. Flow

1. rwb-case: the parent `CaseWorkflow` forwards the case signal to the `GuaranteeClaimWorkflow` child of the case when R-GUA-07 has presented the claim for approval at D6.5 and the officer verifies it, or when R-GUA-21's balance event arrives on a part-paid claim, carrying the case ID, the case status and the claim reference (TSD S3 T4; R-GUA-07; R-GUA-12; R-GUA-21).
2. `GuaranteeClaimWorkflow`: the submit branch opens the step, calls `EvaluateRules` and the `GUA` set in force answers R-GUA-12 or R-GUA-21 with the rule ID and the package version (R-GUA-12; R-GUA-21).
3. `readAccountFacts` activity, step one: reads `recovery.v_ace_batch_status` and compares each product date with today's business date; a product older than today's ACE batch stops the step with MSG-P1-001 naming the product and its date (VR-S3-002-1).
4. Step two: reads the guaranteed contract of the case from `recovery.v_ace_account` at the batch date — `account_key`, `account_code`, `account_status`, `contract_no`, `product_category_efs` and `total_balance` among DF-ACE-001 to DF-ACE-042 — read only, one hop, inside the 2 s budget, with no copy kept (DP-05).
5. Step three: assembles the submission pack from the claim row and the account facts: `claim_type`, `claim_deadline`, `claimed_amount` for R-GUA-12, and `claimed_amount` less `paid_amount` as the balance claim for R-GUA-21 (DF-TRT-017 to DF-TRT-021; R-GUA-21 condition).
6. Step four: files the claim. INT-29 states that the TCG claim channel is not available today and is entered and filed by the guarantee officer, so the officer files on the channel and the step records the filing; no outbound call, file or queue is made (GAP-2711; ASM-4504).
7. `RecordAndApply` activity, one transaction: `guarantee_claim.status` takes `FILED`, `filed_at` takes the business date of the filing, the decision record is written through `DecisionRecordWriter.record(DecisionRecord)` with the rule ID, the rule version and the pack reference, and the stage report is emitted (DP-03).
8. The stage reports `CLAIM_APPROVED` or `BALANCE_CLAIMED` with the rule version and the 2 or 5 working day timer; the parent applies `CLAIM_SUBMITTED` and raises the case task and its timer, and the claim row carries the filing from that moment (R-GUA-12; R-GUA-21).
9. The officer sees the `submitted` state, the filing date and the claim result on SCR-17 through the gateway-bff composite route, which composes the case read and the claim read in one hop each (DP-19).
10. rwb-case holds the case in `CLAIM_SUBMITTED` until the TCG answer arrives; the query, the rejection and the payment are the tracking story's, not this step's.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A data product the step reads is older than today's ACE batch | The step blocks, names the product and its date, and files nothing | MSG-P1-001 | AC1; VR-S3-002-1 |
| X2 | The decision record cannot be written | The transaction rolls back: no status, no filing date, no stage report; the officer sees MSG-P7-003 and an incident is raised | MSG-P7-003 | AC4 |
| X3 | A required claim value is missing, or the balance claim has no unpaid share | The step names the field, writes nothing and raises a guarantee officer task | MSG-GEN-001 | AC3; Section 12.8 |
| X4 | A role without the right in the capability area tries the action | 403 from the access guard on the operation, and nothing changes | MSG-P4-002 | Section 10 |
| X5 | The TCG claim channel holds no interface in any source | The officer files on the channel and the step records the filing; no call is made and the gap stays open | None | GAP-2711; ASM-4504 |
| X6 | A second case signal arrives while the branch is running | The inbox dedupes by the cloud event id and the branch is idempotent on the claim, the rule version and the status, so no second filing is written | None | Section 12.5 |
| X7 | The claim is already in `FILED` and a second submission is asked for | The update answers 409 of the contract; the stage reports nothing new and the case does not move twice | None | ASM-4509 |
| X8 | The account view does not answer | The activity is retried by the workflow's retry policy; when the attempts are exhausted the step stays where it was and the officer sees MSG-GEN-006 naming the product | MSG-GEN-006 | AC1 |

X1, X2, X3 and X4 are the legacy paths of RWB-E4-014 carried onto the split; X5 is the boundary the missing channel interface forces; X6 and X7 are the platform idempotency rules; X8 is the availability path of the ACE read.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-S3-E4014-CON, its fakes and the gateway route; the account view is replaced by a fixture and the rule package by a fake, so no deployment of P1, P7, ACE, the TCG channel or rwb-case is needed |
| Negotiable | The activity names, the shape of the stage report and the retry numbers are this story's choice; the elements, the rules, the condition terms and the messages are fixed |
| Valuable | A verified claim is filed with its date, its rule version and its record in one action, and the case moves without a hand-written status |
| Estimable | One workflow branch, one read activity, one pack assembly, one filing write, one decision-record call and tests |
| Small | Finished inside two weeks with its tests against the fakes |
| Testable | Each criterion runs on a synthetic case, an account fixture and a rule-package fake, plus component tests of the stale-input, the missing-value and the refusal paths |

### 7. Acceptance criteria

```gherkin
Feature: Submit the claim to the TCG portal

  Background:
    Given claim "GCL-SYN-0414" of case "RW-2026-000914" is in state PREPARING
    Given the rule package in force is version "GUA-2026.11"

  Scenario: AC1 Submit the claim to the TCG portal (legacy RWB-E4-014 AC1)
    Given the rwb-case contract mock returns the case in state CLAIM_APPROVAL
    Given the decision-record library mock returns an accepted record
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then files the prepared claim and records the submission reference on the case
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-GUA-12 (legacy RWB-E4-014 AC2)
    Given the rwb-case contract mock returns the case in state CLAIM_APPROVAL
    Given a case in state CLAIM_APPROVAL
    When claim approved
    Then submit the claim through the TCG claim channel
    Then the case moves to CLAIM_SUBMITTED

  Scenario: AC3 Rule R-GUA-21 (legacy RWB-E4-014 AC3)
    Given the rwb-case contract mock returns the case in state CLAIM_PART_PAID
    Given a case in state CLAIM_PART_PAID
    When balance claimed
    Then submit the balance claim
    Then the case moves to CLAIM_SUBMITTED

  Scenario: AC4 Not recorded (legacy RWB-E4-014 AC4)
    Given the decision-record library mock returns the failure MSG-P7-003
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Target reading.** Every legacy line above keeps its wording; what changes is where it runs, which service holds each fact and how it is reached. "Files the prepared claim and records the submission reference on the case" is no longer a method of `GuaranteesAndGuarantorsService` writing `recovery.guarantee_claim`: the filing is the submit branch of `GuaranteeClaimWorkflow` on queue `rwb-guarantee`, the claim row is `rwb_guarantee.guarantee_claim`, and the filing shows as `status = FILED` with `filed_at` — while the reference itself has no field in TSD S3 T3.1 and is not published (GAP-2711; ASM-4503). "Records the submission reference on the case" is carried by the claim row update and by the `CLAIM_SUBMITTED` status the parent applies from the stage report; no case column is written here (DP-01).

"Writes the result to the decision log with the rule version" is the local `DecisionRecordWriter.record(DecisionRecord)` call in the same transaction as the filing, with MSG-P7-003 on failure (DP-03; RWB-PLT-E1027-CON); `decision_log_entry` stays P7's and is never written here. "Submit the claim through the TCG claim channel" is the officer's filing on INT-29 recorded by the service, because the channel has no interface in any source (GAP-2711; ASM-4504). "The case moves to CLAIM_SUBMITTED" is the stage report to the parent and the rule the parent applies; the case status is rwb-case's (ASM-4505). "Balance claimed" is R-GUA-21's event on a claim whose `paid_amount` is below `claimed_amount`, and the balance submitted is `claimed_amount` less `paid_amount`. "Its trigger arrives" is the case signal the parent forwards at the verification of D6.5, because the FSD names "a completed ACE batch, an event or a timer" and no source names which one.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No value a business person may change is written in code: the rule IDs, the conditions, the two timers, the list members and the message texts are rule rows or governed rows with a version | BR-S3-002 of FSD S3 A2.2.3.1 |
| BR2 | The verified claim is filed by R-GUA-12 from `CLAIM_APPROVAL` on `CLAIM_APPROVED`, and the balance claim by R-GUA-21 from `CLAIM_PART_PAID` on `BALANCE_CLAIMED`; both move to `CLAIM_SUBMITTED` | R-GUA-12; R-GUA-21 |
| BR3 | The balance submitted is the `claimed_amount` less the `paid_amount` of the claim, and only while the unpaid share is still claimable inside `claim_deadline` | R-GUA-21 condition; DF-TRT-018 to DF-TRT-021 |
| BR4 | The filing is one write on `guarantee_claim`: `status` takes `FILED` of LOV-CLAIM-STATUS and `filed_at` the business date; the claim row has no other field for a channel reference | TSD S3 T3.1, T3.2; GAP-2711; ASM-4503 |
| BR5 | The filing and its decision record are written in one transaction; if the record cannot be written nothing changes and MSG-P7-003 is shown | DP-03; ADR-022; RWB-PLT-E1027-CON |
| BR6 | The case status, the case task and the case timer are never this service's: the stage reports the outcome, the rule version and the timer, and the parent applies the rule | DP-01; DP-12; ASM-4505 |
| BR7 | Account facts are read only, at the ACE batch date, from this service's own SELECT-only view, one hop inside the 2 s budget, and no account value is copied into `rwb_guarantee` | DP-05; VR-S3-002-1; D-RCV-35 |
| BR8 | A data product older than today's ACE batch blocks the filing and is named with its date; nothing is filed on a stale input | VR-S3-002-1; MSG-P1-001 |
| BR9 | The TCG claim channel is INT-29 and has no published interface; the submission is the officer's filing recorded by the service, with no outbound call, file or queue | TSD S3 T5.1; ASM-4504 |
| BR10 | The capability area is "Treatment and offer" with right C on the create and right U on the update; the right is declared per operation and checked by the platform guard | TSD S3 T6.1 |

**Where each rule lives in the target.** BR1 is why the rules and the timers are inputs of the step; BR2 is the two answered rows and their from states; BR3 is the pack assembly; BR4 is the single write and the reason no reference element exists; BR5 is the `MANDATORY` propagation of the library write; BR6 is the boundary to rwb-case; BR7 and BR8 are the read activity and its guard; BR9 is the recorded filing; BR10 is the `security` section of the two operations the contract publishes.

### 9. State transitions

None of the case statuses below is this service's; the table shows what the stage reports and does not write, so a reader can see the boundary of this story.

| Rule | From (rwb-case) | Event | Condition | What this stage does | To (rwb-case) |
|---|---|---|---|---|---|
| R-GUA-12 | `CLAIM_APPROVAL` | `CLAIM_APPROVED` | the guarantee officer verifies the claim at D6.5 | Builds the pack, records the filing, records the decision, reports `CLAIM_SUBMITTED` with the 2 working day timer | `CLAIM_SUBMITTED` |
| R-GUA-21 | `CLAIM_PART_PAID` | `BALANCE_CLAIMED` | the unpaid share is still claimable inside the deadline | Builds the balance claim, records the filing, records the decision, reports `CLAIM_SUBMITTED` with the 5 working day timer | `CLAIM_SUBMITTED` |
| R-GUA-13 (read only) | `CLAIM_APPROVAL` | `CLAIM_SENT_BACK` | the officer rejects the assembled claim | Answers "sent back" and files nothing; the rework is RWB-S3-E4013-APP's | `CLAIM_PREPARATION` |

The states of this story's own row are the claim's, from LOV-CLAIM-STATUS: `PREPARING` before the filing and `FILED` after it. `DEFECT`, `PAID` and `REJECTED` belong to the tracking and subrogation stories. The seventeen rule states of TSD S3 T4 and this five-member list are two vocabularies and no source maps them, so only the one pair this story needs is fixed — `PREPARING` to `FILED` on submission — and the rest stays open (GAP-2711; ASM-4505). The `GuaranteeClaimWorkflow` execution has the platform states RUNNING, COMPLETED and FAILED, and a FAILED execution restarts from the last recorded step, which is why the read and the write are activities and not workflow-local computation.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery squad (RW-TRIBE) | Writes the workflow branch, the read activity, the pack assembly, the filing write and the tests |
| RW-GUARANT, guarantee officer | Verifies the claim at D6.5, files on the TCG claim channel and records the filing; holds rights C, R and U on Treatment and offer |
| RW-CASEOWN, case owner | Owns the case the claim is filed on; holds rights C, R and U |
| RW-RESTRUCT, restructuring officer (FCR) | Holds rights C, R, U and A; sees the filing and the result |
| RW-SPECIAL, hardship and vulnerability specialist | Holds rights C, R and U |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and the read-only roles of TSD S3 T6.1 | Right R only: they read the claim and its filing and cannot file |
| SY-CASEWF, the case workflow module | Runs the step unattended under the service identity and reports to the parent |
| rwb-case (P3) | Owns the case, its status, its tasks, its timers and the parent `CaseWorkflow` |
| P7 rwb-decision | Owns the `GUA` package, the 32 rows, their approval, their effective date and the central ledger |
| The TCG (INT-29) | Owns the claim channel and receives the officer's filing; it holds no right in the Workbench |
| ACE and its DBA | Own the `recovery.v_ace_*` views, their grants and the batch that dates them |
| The platform workflow and data owners | Own the task queue, the namespace, the ACE PostgreSQL grants and the decision-record library |

The check is the platform guard library's: this story declares the capability area "Treatment and offer" and the right C or U on each entry point, and no check is written in code. No credential and no personal name appears in the workflow input, the activity request or the logs, which carry the case ID, the claim ID, account keys, dates, amounts and versions only.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-015 | guarantee_claim | id | Read (the row the filing is written on) |
| DF-TRT-016 | guarantee_claim | case_id | Read |
| DF-TRT-017 | guarantee_claim | claim_type | Read (the pack and the list LOV-CLAIM-TYPE) |
| DF-TRT-018 | guarantee_claim | claim_deadline | Read (the R-GUA-21 condition) |
| DF-TRT-019 | guarantee_claim | claimed_amount | Read |
| DF-TRT-020 | guarantee_claim | filed_at | Write (the business date of the filing) |
| DF-TRT-021 | guarantee_claim | paid_amount | Read (the balance claim) |
| DF-TRT-022 | guarantee_claim | status | Write (`FILED`) |
| TSD S3 T3.0, no field identifier | guarantee_claim | the seven standard columns is_active, state, version, created_at, created_by, updated_at, updated_by | Write (`version`, `updated_at` and `updated_by` change with the filing) |
| DF-ACE-001 to DF-ACE-042 | v_ace_account | account_key, account_code, account_status, contract_no, product_category_efs, total_balance and 36 more | Read only, at the batch date |
| DF-ACE-001 to DF-ACE-042 | v_ace_batch_status | the product date of the ACE batch | Read only, the freshness guard |
| DF-CAS-001 to DF-CAS-023 | recovery_case | case_no, product_group, status, stage_code and the rest | Read on the case signal only |
| DF-DEC-001 to DF-DEC-018 | decision_record | the field groups of the record | Write |
| DF-REF-001 to DF-REF-015 | rule_row | the `GUA` rows in force, their conditions and the two timers | Read |
| DF-WRK-027 to DF-WRK-036 | timer | the case timer of the 2 and 5 working day rules | Not this service's; rwb-case writes it (ASM-4507) |

`guarantee_claim` and `decision_record` are this service's own objects in `rwb_guarantee`, written through its own repository and login (DP-01). The account columns are read through the read-only view at the ACE batch date and are not copied: there is no account, balance or contract column in `rwb_guarantee`. The case fields arrive on the case signal and are never read from a table; the rule rows are read through the rule loader and are never joined to this service's tables. The document set the claim needs is assembled by the preparation story and lives with rwb-document, so no document row or blob reference is owned here. The submission reference has no field identifier in the Logical Data Model (GAP-2711; ASM-4503).

### 12. Contract

#### 12.1 REST operations provided

None new. This story implements the two operations that RWB-S3-E4014-CON publishes on base `/api/recovery/guarantee/v1` (DP-13), and adds no path of its own.

| Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|
| POST | `/cases/{caseId}/guarantee-claims` | `GuaranteeClaimRequest`; `caseId` from the path | 201 with `GuaranteeClaim` | Treatment and offer C, scope applied | `Idempotency-Key` header required | 401, 403, 404, 409, 422, 503 |
| PATCH | `/guarantee-claims/{claimId}` | `GuaranteeClaimUpdate` | 200 with `GuaranteeClaim` | Treatment and offer U, scope applied | Not applicable | 401, 403, 404, 409, 422, 503 |

The two operations, their entities, their rights, their idempotency and their error statuses are TSD S3 T-A.1 and T-A.2 for API-S3-001 and API-S3-002 with the base renamed by DP-13; the shape, the DDL template, the message identifiers and the fakes are RWB-S3-E4014-CON's and are not restated here. There is no third operation: the TCG claim channel is INT-29 with no interface, so no submit path and no channel callback path exists (GAP-2711; ASM-4504).

#### 12.2 REST operations consumed

None. The case status and the claim reference arrive on the case signal the parent `CaseWorkflow` forwards, and Architecture v5 slide 13 shows the S3 to P3 edge as a Temporal call and not a REST one. The account facts are a SQL read of the view in 12.7, the rule rows arrive on the package event of 12.4 and the screen is composed by the gateway route of 12.8 (DP-19). No source publishes an operation for this step and none is invented.

#### 12.3 Events published

None. The service's topic is `rwb.guarantee.events.v1` with names `rwb.guarantee.<Event>.v1` (DP-14), and the ownership rows give S3 no event type; the connection matrix has rwb-reporting listening to S3, which no catalogued event satisfies, so the submission raises no Kafka event and its signal is the stage report to the parent `CaseWorkflow` (GAP-2711; ASM-4508). The `DecisionRecorded` event of the library is written in the caller's transaction under RWB-PLT-E1027-CON and is not a type of this service (DP-03).

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | Loads the `GUA` package and route set in force, verifies the checksum, swaps them atomically and keeps the last good set on failure; EV-30 |

The service also listens to P8 payment events on the connection matrix, and the event that opens R-GUA-20 sits with the tracking story RWB-S3-E4015-APP; no event name is published for it in the sources read here, so none is named. Both subscriptions are the service template's inbox and rule loader; this story adds no subscription of its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `GuaranteeClaimWorkflow` (the submit branch) | Child workflow of `CaseWorkflow`, one per case, on this service's own queue | `rwb-guarantee` in namespace `rwb-recovery` | Input: the case ID, the claim ID, the case status on the signal, the rule version and the claim facts. Output: the stage report with the filing date, the pack reference, the rule version and the timer |
| `EvaluateRules` | Activity of the template | `rwb-guarantee` | The package and route set in force and the case facts in; the rule ID, the action and the next event out; `NoPackageInForce` is not retried |
| `readAccountFacts` | Activity | `rwb-guarantee` | The two view reads at the batch date and the stale guard in; the account facts and the product dates out; the stale answer is non-retryable |
| `recordSubmission` | Activity | `rwb-guarantee` | The pack and the claim row in; the `GuaranteeClaimUpdate` of RWB-S3-E4014-CON out, with `status = FILED` and `filed_at` |
| `RecordAndApply` | Activity of the template | `rwb-guarantee` | The update and the decision record in one transaction, then the stage report |

The workflow name is fixed by Temporal and Drools Design slide 13; the three activity names are this story's choice. The retry policy is the workflow kit's (1 s initial interval, back-off 2, 10 attempts; a stale product and `NoPackageInForce` non-retryable). A replay never re-reads a view: the answer is recorded by the activity and read from history, and the branch is idempotent on the claim, the rule version and the status, so a repeated signal writes no second filing.

#### 12.6 Schedules

None. The step is signal-driven from the case and owns no Temporal Schedule and no legacy Quartz job; the ownership rows give S3 no job. The 2 working day timer of R-GUA-12, the 5 working day timer of R-GUA-21 and the claim deadline of R-GUA-01 are workflow and case timers driven by the platform and written by rwb-case, not a schedule of this service (ASM-4507).

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `guarantee_claim` | `rwb_guarantee` | S3 rwb-guarantee | Created by the per-service Flyway sequence and written here for `status`, `filed_at` and the standard columns; DF-TRT-015 to DF-TRT-022 of TSD S3 T3.1 |
| `decision_record` | `rwb_guarantee` | PLT library object | Written only through `DecisionRecordWriter` in the caller's transaction (DP-03) |

No table of another service is read and no foreign key crosses a schema (DP-01). Two `recovery.v_ace_*` views of the ACE database are read, `v_ace_account` and `v_ace_batch_status`, read only at the ACE batch date and with no copy kept; the case table, the timer table and the task rows of rwb-case, the rule tables of rwb-decision and the ledger of P7 are never named in SQL.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-S3-E4014-CON claim fake | The two operations of 12.1 | A 201 create and a 200 update with a `GuaranteeClaim`; a 409 for a claim already in `FILED`; a 422 and a 403 refusal; a 404 and a 503 |
| ACE view fixture | `v_ace_account` and `v_ace_batch_status` | A guaranteed contract with its balance; a product dated yesterday; a claim with no unpaid share; an unreachable view |
| Case-signal fake | The signal the parent forwards | `CLAIM_APPROVAL`; `CLAIM_PART_PAID` with `paid_amount` below `claimed_amount`; `CLAIM_PREPARATION` for the send-back |
| Decision-record writer fake (RWB-PLT-E1027-CON) | `DecisionRecordWriter` | An accepted record with its chain sequence; a refusal with MSG-P7-009 and the field; a failure with MSG-P7-003 |
| Rule-package fake | The `GUA` package and rows in force | Version `GUA-2026.11` with R-GUA-12 and R-GUA-21; a set with no matching row; a checksum mismatch |
| Gateway route fake (RWB-PLT-N001-CON) | The SCR-17 composite route | The case read and the claim read composed in one answer |

The view fixture and the case-signal fake are the Day-1 unblockers: the build and every test run against them, and no test reads a production view, needs a live case or reaches the TCG channel.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations implemented on `/api/recovery/guarantee/v1` | 0 | OpenAPI 3.1, RFC 9457 problem bodies; the browser reaches them through gateway-bff (DP-19) |
| Kafka | 0 | 1 event (`rwb.decision.RulePackageInForce.v1`) | Own topic named, no event type declared; inbox dedupe by cloud event id |
| Temporal | `GuaranteeClaimWorkflow` and 4 activities on `rwb-guarantee` | The case signal forwarded by the parent `CaseWorkflow` | Namespace `rwb-recovery`; no Schedule |
| SQL view | 0 | 2 (`recovery.v_ace_account`, `recovery.v_ace_batch_status`) | Read only, at the batch date, no copy |
| File | 0 | 0 | No file is read or written; the TCG channel takes none |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.guarantee`, modules `claimsubmit` and `workflow`, with the published types in `...guarantee.api`. Service base `/api/recovery/guarantee/v1`, schema `rwb_guarantee`, topic `rwb.guarantee.events.v1`, task queue `rwb-guarantee` in namespace `rwb-recovery` (DP-13; §R4).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is taken as the service's own SELECT-only view, because the Work Package records no contract dependency on P1; the reading and the conflict with Architecture v5 slide 8 are in ASM-4506. DP-03 is the record of the filing, DP-13 the base the two operations sit on, and DP-19 the path SCR-17 is read on. The outbox and inbox library, the workflow kit, the access guard and the embedded Drools runtime are the service template's wave-0 capabilities and add no build dependency of their own.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `ClaimSubmitBranch` | Workflow | The branch of `GuaranteeClaimWorkflow` that opens the step, reports the outcome and waits |
| `EvaluateRules` | Activity | Runs the `GUA` package and route set in force and returns the rule ID, the action and the next event |
| `readAccountFacts` | Activity | The two read-only view queries, the stale guard and the account facts |
| `ClaimPackAssembler` | Service | Builds the pack and the balance claim from the claim row and the account facts |
| `ClaimSubmitRepository` | Repository | Writes `status`, `filed_at` and the standard columns on `guarantee_claim` |
| `DecisionRecorder` | Service | Assembles `DecisionRecord` and calls `DecisionRecordWriter.record` in the caller's transaction |
| `StageReporter` | Service | Builds the stage report with the filing date, the rule version, the timer and the officer messages |

**Database.** No new table and no new column: this story writes `guarantee_claim.status` (DF-TRT-022), `guarantee_claim.filed_at` (DF-TRT-020) and the standard columns in `rwb_guarantee`, and `decision_record` is the library object of DP-03. A channel-reference column is deliberately not added; if the reference must be persisted it becomes a field of the Logical Data Model first (GAP-2711; ASM-4503).

**Configuration and reference data.** The rule IDs, the conditions, the two timers and the list members are data of rwb-decision and the reference lists, read with their version and never configured here. The retry numbers, the activity names and the 2 s budget are configuration of the activity. The capability area "Treatment and offer" and the rights are access data of P4 read through the guard library.

**Build steps**

1. The submit branch of `GuaranteeClaimWorkflow` on `rwb-guarantee`, its input record and the stage report.
2. `EvaluateRules` against the package fake, with R-GUA-12 and R-GUA-21 as rule rows and the `NoPackageInForce` answer (AC2, AC3).
3. `readAccountFacts` against the view fixture, with the batch-date test and MSG-P1-001 (AC1, X1).
4. `ClaimPackAssembler` with the claim amount, the balance claim and the missing-value path (AC1, AC3, X3).
5. The filing write and the `GuaranteeClaimUpdate` against the claim fake, with the 409 of a filed claim (AC1, X7).
6. `RecordAndApply` with the record in the same transaction and the rollback path of MSG-P7-003 (AC4).
7. The recorded officer filing of INT-29, with no outbound call (AC2, X5).
8. Tests for AC1 to AC4 against the fakes, the component tests of X1, X3, X5 and X8, and the replay test of X6.

**Feature flag.** `rwb.guarantee.claim-submission`.

**Done when.** The tests in section 16 pass, the branch runs from a synthetic case signal in SIT with the views, the package and the channel faked, the claim shows `status = FILED` with its date, the record is written in the same transaction and rolls back with the filing, the stale product path blocks with MSG-P1-001, and the case reaches `CLAIM_SUBMITTED` on the report with its 2 or 5 working day timer.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A data product the step reads is older than today's ACE batch | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-001 | A required claim value is missing and the step cannot build the pack | Enter {field}. |
| MSG-GEN-006 | An ACE view does not answer after the retries | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | A role without the right in the capability area tries the action | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written and the filing is not made | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | The record is refused for a missing or invalid field | The decision record was refused: {field} is missing or not valid. |

The texts are copied unchanged from the legacy story, FSD S3 A2.2.3.1 and the platform message set, and this story adds no message ID. The 403 of a right the role does not hold and the 409 of an already filed claim carry the platform problem body; the 409 has no business text in any source read for this key (GAP-2712; ASM-4509). Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-17 Guarantee claim shows the guarantee, the claim deadline, the checklist and the claim result, in the states `Not due`, `due`, `submitted`, `paid` and `refused`. This story makes `submitted` real: the filing date, the claim type, the claimed amount and the rule version are read on the same screen through the gateway-bff composite route, which calls rwb-case and this service's claim read in one hop each (DP-19; Architecture v5 slide 41). The screen field list and the route specification belong to the platform edge story and the screen owner; this story fixes what the service writes and what the sibling contract's read returns. A blocked step is shown as its message with the product and its date, never as a filed claim.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-014-01 | AC1 | End to end | Submit the claim to the TCG portal |
| TC-E4-014-02 | AC2 | End to end | Rule R-GUA-12 |
| TC-E4-014-03 | AC3 | End to end | Rule R-GUA-21 |
| TC-E4-014-04 | AC4 | End to end | Not recorded |
| TC-E4-014-05 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E4-014-06 | Principle 5 | Component | A forced decision log write failure stops the action with MSG-P7-003 |

The legacy test case IDs, their Covers and their Data are kept in order and character for character; the story level "System" of the legacy suite is carried as "End to end" and the two exception cases as "Component", as in the other stories of this run. TC-E4-014-05 and TC-E4-014-06 restate the same guard as the legacy suite, so they run once each. The claim, view, case-signal, decision-record, rule-package and gateway fakes of section 12.8 stand behind every case, and the full Given, When and Then of each is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID. The `-ITG` copies (TC-E4-014-01-ITG to TC-E4-014-06-ITG) belong to the wave 3 integration harness (RWB-ITG-W3) and are not written by this story. The contract's own tests are TC-S3-E4014-CON-01 to -05 and are owned by RWB-S3-E4014-CON.

### 17. Guardrails

- No value a business person may change is written in code: the rule IDs, the conditions, the two timers, the list members and the six messages are rule rows or governed rows with a version (BR-S3-002; BR1).
- No personal data in logs, workflow inputs, activity requests, events or tests: the step carries the case ID, the claim ID, account keys, dates, amounts and versions only, and the fixture is synthetic.
- No read of another service's tables: the case arrives on the signal, the rule rows on the package event, and nothing joins across a schema (DP-01).
- No copy of ACE data: the account and its balance are read at the batch date and no account, balance or contract column exists in `rwb_guarantee` (BR7; DP-05).
- ACE data only through the owner's contract or the `v_ace_*` views, and here only two views with SELECT granted to this service's login (ASM-4506).
- No outbound call, file or queue to the TCG: the channel has no interface and the filing is the officer's, recorded by the service (BR9).
- No business value in the record: the `DecisionRecord` carries the rule ID, the rule version, the claim amount and the result code, never a free-text reason or a customer field (DP-03).
- No status change from this service: the stage reports and the parent applies the rule (BR6).
- No live view, live channel and no live rule package in any test: the fixture and the fake are the only endpoints.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S3-001 | A guarantee claim is prepared from case data and submitted inside the guarantor's deadline | Business Requirements Program v5, section 5.10 | FEAT-GUA-02 | 07 Route, settle and claim | R-GUA-12; R-GUA-21; BR1 to BR10 | TC-E4-014-01, TC-E4-014-02, TC-E4-014-03, TC-E4-014-04, TC-E4-014-05, TC-E4-014-06 |
| REQ-S3-002 | Claim status, payment and any shortfall are recorded on the case | Business Requirements Program v5, section 5.10 | FEAT-GUA-02 | 07 Route, settle and claim | BR4; BR5; BR6 | TC-E4-014-01, TC-E4-014-04 |

REQ-S3-001 and REQ-S3-002 are the two requirements whose text names this behaviour, so the trace runs on them; TSD S3 T8 maps the module's requirements to FEAT-GUA-01 as the "written one epic ahead" placeholder, and the feature code FEAT-GUA-02 of FSD S3 A2.2 is carried alongside until the C1 PRD settles the mapping (Section 19). The legacy key also names FEAT-GUA-01 as its prerequisite; no requirement of this module references that prerequisite, so it is not carried as a row.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S3-E4014-CON | Contract | H: declares the resource, the DDL template, the error set, the versioning rule and the fakes this story builds against |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library, with MSG-P7-009 and MSG-P7-003 |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route through which SCR-17 shows the `submitted` state |
| RWB-S3-E4013-APP | App development | Sibling: prepares the claim, runs the scheme checklist and presents it at D6.5; this branch starts where that one leaves the claim |
| RWB-S3-E4015-APP | App development | Sibling: tracks the claim to payment, records the query, the rejection and the service level breach |
| RWB-S3-E4016-APP | App development | Sibling: records the subrogation position after payment |
| P3 rwb-case | Service | The case, its status, its tasks, its timers and the parent `CaseWorkflow` |
| P7 rwb-decision | Service | The `GUA` package and the 32 rows; EV-30 is consumed here |
| ACE and its DBA | Data | The two `recovery.v_ace_*` views, their grants and the batch that dates them |
| The TCG (INT-29) | External | The claim channel the officer files on; no interface today |
| RWB-ITG-W3 | Integration | I: the cross-service proof of the filing against the live owners, and the owner of the `-ITG` copies |

### 19. Out of scope

- The published resource, the DDL template, the error set, the versioning rule and the fakes: RWB-S3-E4014-CON.
- The preparation of the claim, its scheme checklist and its document set: RWB-S3-E4013-APP, with rwb-document for the documents.
- The tracking of the claim to payment, the query and rejection answers, the lost claim and the service level breach: RWB-S3-E4015-APP.
- The subrogation position and the closing of a guarantee that clears the balance: RWB-S3-E4016-APP.
- The case, its status, its tasks, its timers and the parent `CaseWorkflow`: rwb-case (P3), reached only through the forwarded case signal and the stage report.
- The rule authoring, the four-eyes approval, the effective date, the rollback of the `GUA` rows and the central ledger: rwb-decision (P7).
- The `recovery.v_ace_*` views, their columns, their grants and the ACE batch that dates them: ACE and its DBA.
- Any interface to the TCG claim channel, its operation, its file or its schema: not published by any source; raised as GAP-2711 and ASM-4504.
- The submission reference as a published field, until the Logical Data Model names a field identifier: GAP-2711 and ASM-4503.
- SCR-17, its field list and the gateway-bff composite route: the platform edge story and the screen owner (DP-19).
- The deployment of this build: the chart values, the schema and login, the topic and the flag.
- The real cross-service proof against the live owners and the `-ITG` copies of the legacy cases: RWB-ITG-W3.

# RWB-S2-E3006-APP Calculate the plan installment

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the application slice of RWB-E3-006 split out for rwb-treatment. The plan-installment step leaves the monolith's `TdrSettlementAndDeedInLieuService` and becomes the plan-installment branch of `TreatmentWorkflow` on this service's own task queue; the ALS balance is read at the ACE batch date from this service's own SELECT-only `recovery.v_ace_*` views and is never copied (DP-05); the band, the floor and the freshness limit are read from the reference-data contract of rwb-case with the version in force (DP-07); the result is written on the treatment row with its local decision record in the same transaction (DP-03); the two legacy criteria this story owns are copied word for word with their origin tag; the two screens are reached through the gateway-bff composite route (DP-19); this story declares no REST path of its own, so the legacy base `/api/recovery/v1` is not carried (DP-13). No source fixes the element fields, the reference-data operation or the freshness limit (GAP-2651, GAP-2652; ASM-4359, ASM-4360), allocates a requirement to FEAT-TRT-06 (GAP-2653; ASM-4361), settles whether S2 may read the ACE views (GAP-2654; ASM-4362), gives the feature a field catalog (GAP-2655; ASM-4363) or names the trigger of the step (GAP-2656; ASM-4364). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S2-E3006-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3006-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP07, DP13, DP19 |
| Parallel lane | L-S2-Q |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S2-E3006-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the plan-installment step of a treatment to run as the plan-installment branch of `TreatmentWorkflow` — the model installment and the range I may move within computed from the ALS balance at the ACE batch date, the affordability answer already recorded against the treatment and the band in force in reference data, with the rule version that decided written with the result** — so that **restructures and settlements reach booking in days instead of being tracked by hand for 23 to 26 days**.

This is the application slice of legacy RWB-E3-006. It owns:

- the two legacy acceptance criteria this story is given (AC1 and AC3), copied verbatim with their origin tag, and the rules, data rows and messages they carry;
- the plan-installment branch of `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery`: the step that evaluates the rule set in force, computes the model installment and the band, records the answer and reports the stage outcome to the parent `CaseWorkflow` (Temporal and Drools Design slides 13 and 18);
- the calculation activity: the ALS balance of each account of the case read at the ACE batch date from this service's own SELECT-only views `recovery.v_ace_account` and `recovery.v_ace_batch_status`, the plan terms already on the treatment, and the band with its floor from reference data (DP-05; DP-07);
- the band read: the reference set of rwb-case through the client library of RWB-PLT-E1043-CON on contract RWB-P3-E1043-CON, one hop inside the 2 s budget, with the set version recorded next to the result (DP-07);
- the stale-input guard of FSD A2.6.3.1 VR-S2-006-1: a data product older than today's ACE batch blocks the step with MSG-P1-001 naming the product and its date;
- the `PlanInstallment` element of RWB-S2-E3006-CON written against the treatment row in `rwb_treatment` (`installment_amount` and `installments` among TSD S2 T3.1 fields) and the local decision record of the step written through `DecisionRecordWriter.record(DecisionRecord)` in the caller's transaction (DP-03; RWB-PLT-E1027-CON);
- the refusal and failure paths: no record, nothing changes and MSG-P7-003; no band, the step blocks with MSG-GEN-006; a missing value is named with MSG-GEN-001.

It does not own: the published element, the reference-data consumption rule, the ACE read rule, the versioning rule and the fakes, which are RWB-S2-E3006-CON; the affordability branch and its Nexus call, which are RWB-S2-E3005-APP; AC2 of the legacy key, the R-SET-01 state step, which the Work Package does not assign to this story and whose state movement stays with the case and the settlement stories of this service (GAP-2657; ASM-4365); the treatment record, its create and read operations, which are RWB-S2-E3001-APP; the settlement offer inside the range and the below-floor approval, which are RWB-S2-E3002-APP and RWB-S2-E3003-APP; the offer build and its validity timer, which are RWB-S2-E3004-APP and the offer stories; the payoff and settlement range of the route decision, which are FEAT-VAL-06 and RWB-S1-E4006-APP; the case record and every case status, which are rwb-case's and arrive on the case signal the parent forwards; the reference data and its governance, which are rwb-case's (P3); the ACE views and their content, which are ACE's; the rule package, its approval and the central ledger, which are P7 rwb-decision's; the screens and their composite route, which are the platform edge story's and the screen owners' under DP-19.

### 2. Business rationale

In the monolith this feature was a method of `TdrSettlementAndDeedInLieuService` that read the account from the `recovery` schema, read the thresholds from `rule_row` and wrote the answer into `treatment` and `decision_log_entry`, all inside one process and one schema (TSD S2 T2 and T3.1). Three things followed from that shape. The numbers could not be recomputed without the whole monolith, so a change of a threshold was a code release. The account balance was copied into the Workbench's own tables, so a balance could be read at a date nobody could reconstruct. And a reader of the answer had to read the module's tables, because the answer had no shape of its own.

D-RCV-60 changes the source of each input and nothing else. The balance stays where ACE holds it and is read at the ACE batch date through this service's own SELECT-only views, with the data product's date on the answer (DP-05; D-RCV-35, ADR-010). The band, the floor and the freshness limit become governed rows of rwb-case read through its contract with the version that was in force, so a change of policy is a data release and not a build (DP-07; the default ruling on parameters and reference data). The decision is recorded locally in the same transaction as the result, so a calculation that cannot be recorded does not proceed (DP-03; ADR-022).

The step is a branch of the stage workflow the service already owns: one child workflow per case on the owner's queue, `rwb-treatment`, with the rules evaluated from the package and the route set in force (Temporal and Drools Design slide 13; Architecture v5 slide 18). The two rules that name the numbers are R-SET-01's "calculate the payoff from ALS and set the range from reference data" and the settlement range test of R-SET-04 and R-SET-05, whose field names — `settlement_range_low`, `settlement_range_high`, `floor_price`, `payoff_as_at` — are carried into the element unchanged (Business Rules and Routing Logic v4).

What it does not change is the officer's work. The range is still the range the officer may move within, an offer inside it is still an offer, and an offer below the floor still goes to the approver of R-SET-05, which is RWB-S2-E3003-APP. The plan is still booked by operations. No business value moves: the rule IDs, the state names and the six messages are the legacy values, held as data and as rule rows, never as code constants (BR-S2-006 of FSD A2.6.3.1).

Delivery is EP03 in wave 2 on release 31 January 2027 (tentative). No requirement ID is allocated to FEAT-TRT-06 in the source documents — TSD S2 T8 maps REQ-S2-001 to REQ-S2-010 to FEAT-TRT-01 only — so the trace runs on the feature code until the C1 PRD allocates one (GAP-2653; ASM-4361).

### 3. Preconditions

- RWB-S2-E3006-CON is published: the `PlanInstallment` element, its required and optional fields, the reference-data elements it consumes, the ACE read rule, the messages and the fakes. The build starts against the Draft baseline, as every CON story of this run publishes on Day 1 at status Draft (realignment v1).
- RWB-PLT-E1043-CON is published: the reference-data client library, its cache keyed by set and version, its 2 s budget and its refusal when the set is not in force (DP-07).
- RWB-P3-E1043-CON is in place as a contract dependency: the reference sets this story reads — the band bounds, the floor and the freshness limit — with their identifiers and their version (DP-07; default ruling: reference data owned by P3 rwb-case). Contract dependencies never block the build (§R5.4).
- RWB-PLT-E1027-CON is published: `DecisionRecordWriter`, `DecisionRecord`, the `MANDATORY` propagation, the refusal with MSG-P7-009 and the failure with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-14 and SCR-15 from the case read and this service's read (DP-19).
- The `rwb_treatment` schema and its login exist from the platform database story, the `treatment` table is on the per-service Flyway sequence with DF-TRT-001 to DF-TRT-033 of TSD S2 T3.1, and `decision_record` is created as the platform library object in the same schema (DP-01; DP-15).
- SELECT on `recovery.v_ace_account` and `recovery.v_ace_batch_status` is granted to this service's login and on no other ACE object. Architecture v5 slide 8 says the 30 `recovery.v_ace_*` views are read only by rwb-source-data while DP-05 allows the service's own SELECT-only views; the grant is the working read of ASM-4362 and the Work Package records no contract dependency on P1 (GAP-2654).
- The treatment carries an accepted affordability answer with its rule version from RWB-S2-E3005-APP, and `treatment.installments` and `treatment.installment_amount` are the two fields the answer left behind (DF-TRT-009, DF-TRT-031).
- The rule package and route set in force are in this service's rule cache at the version the answer names; their identifiers and conditions are rule rows, not code (EV-30; BR-S2-006).
- No approval stop: the FSD S2 and TSD S2 documents carry status "In review" and nothing in this story needs a human sign-off to start on Day 1.

### 4. Flow

1. rwb-case: the parent `CaseWorkflow` forwards the case signal to the `TreatmentWorkflow` child of the case when the treatment reaches the plan-installment step (Temporal and Drools Design slide 13; EV-29).
2. `TreatmentWorkflow`: the plan-installment branch opens the step, calls `EvaluateRules` and the rule set in force returns the row that nominates the calculation, with the rule ID and the package version (R-SET-01 and the range rows of R-SET-04 and R-SET-05 where the treatment is a settlement; the RESTRUCTURE package where it is a plan).
3. `calculatePlanInstallment` activity, step one: reads `recovery.v_ace_batch_status` and compares the data product date with today's business date; a product older than today's ACE batch stops the step with MSG-P1-001 naming the product and its date (VR-S2-006-1).
4. Step two: reads `total_balance`, `contract_no`, `product_category_efs` and the account identifiers of each account of the case from `recovery.v_ace_account` at the batch date, read only, one hop, inside the 2 s budget, and keeps no copy (DP-05).
5. Step three: reads the band bounds, the floor and the freshness limit from the reference sets of rwb-case through the client library, with the set version, and refuses the step when no set is in force with MSG-GEN-006 (DP-07).
6. Step four: computes the model installment and the range from the accepted plan terms on the treatment (`installment_amount`, `installments`, `interest_rate`), the ALS balance at the batch date and the band, and names the rule ID, the rule version and the reference-set version on the answer (BR-S2-006; GAP-2651; ASM-4359).
7. `RecordAndApply` activity, one transaction: the `PlanInstallment` element is written against the treatment row, `installment_amount` and `installments` take the accepted values, the decision record is written through `DecisionRecordWriter.record(DecisionRecord)` with the rule ID, the rule version and the reference-set version, and the stage report goes to the parent.
8. The stage reports the outcome to the parent, which applies the rule for the status; this service writes no case row and publishes no case event for it (DP-01; ASM-4362).
9. The officer reads the model installment and the range on SCR-14 and SCR-15 through the gateway-bff composite route and through the treatment read of RWB-S2-E3001-APP, and builds the offer inside the range.
10. The payoff on the case is older than the freshness limit: the step warns with MSG-S2-002, requests a fresh figure and does not compute on the stale one (R-SET-03).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A data product the step reads is older than today's ACE batch | The step blocks, names the product and its date, and computes nothing | MSG-P1-001 | AC1; VR-S2-006-1 |
| X2 | No reference set is in force, or the set version cannot be resolved | The client library refuses, the step blocks and nothing is written; the stage stays where it was | MSG-GEN-006 | AC1; Section 12.2 |
| X3 | The decision record cannot be written | The transaction rolls back: no element, no plan terms, no stage report; the caller sees MSG-P7-003 and an incident is raised | MSG-P7-003 | AC3 |
| X4 | The record is refused for a missing or invalid field | Nothing is written, the field is named, the stage stays where it was | MSG-P7-009 | Section 12.8 |
| X5 | A required value is missing on the treatment, for example the installment count | The step holds, names the field and raises a task for the owner; no element is written | MSG-GEN-001 | Section 14 |
| X6 | A role without the right tries to re-run the step or read its result | 403 from the access guard and nothing changes; the step itself runs unattended under the service identity | MSG-P4-002 | Section 10 |
| X7 | The payoff on the case is older than the freshness limit | The step warns, requests a fresh figure and does not compute on the stale one | MSG-S2-002 | Section 4 |
| X8 | A second case signal arrives while the branch is running | The inbox dedupes by the cloud event id of the case signal and the activity is idempotent on the treatment and the rule version, so no second element is written | None | Section 12.5 |
| X9 | The ACE views are not reachable | The activity is retried by the workflow's retry policy; when the attempts are exhausted the stage stays where it was and the caller sees MSG-GEN-006 naming the product | MSG-GEN-006 | AC1 |

X1, X3, X5, X6 and X7 are the legacy paths of RWB-E3-006 carried onto the split. X2 is the reference-data library's answer, X4 the platform library's refusal, X8 the inbox dedupe and X9 the availability path of the ACE read.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-S2-E3006-CON and its fakes, the reference-data library, the decision-record library and the gateway route; the ACE views are replaced by a fixture and the reference data by a fake, so no deployment of P1, P3 or ACE is needed |
| Negotiable | The activity name, the shape of the stage report and the retry numbers are this story's choice; the element, the rules, the field names of the range and the messages are fixed |
| Valuable | The officer receives the model installment and the range in one place, with the version of the policy that produced them, and books in days |
| Estimable | One workflow branch, one calculation activity, two reads, one result repository, one decision-record call and tests |
| Small | Finished inside two weeks with its tests against the fakes |
| Testable | Each criterion runs on a synthetic case, an ACE view fixture and a reference-data fake, plus one component test of the stale-input and refusal paths |

### 7. Acceptance criteria

```gherkin
Feature: Calculate the plan installment

  Background:
    Given treatment "TRT-SYN-0601" of case "RW-2026-000613" is a RESTRUCTURE plan with an accepted affordability answer
    Given the rule package in force is version "RESTRUCTURE-2026.11"

  Scenario: AC1 Calculate the plan installment (legacy RWB-E3-006 AC1)
    Given the rwb-case contract mock returns the band, the floor and the freshness limit in force at version "REF-2026.11"
    Given the ACE account view returns the ALS balance of the case at today's batch date
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then produces the model installment and the range the officer may move within
    Then the system writes the result to the decision log with the rule version

  Scenario: AC3 Not recorded (legacy RWB-E3-006 AC3)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

**Target reading.** Every legacy line above keeps its wording; what changes is where it runs, who produces each number and how it is reached. "Produces the model installment and the range the officer may move within" is no longer a method of `TdrSettlementAndDeedInLieuService` reading the `recovery` schema and `rule_row`: the model installment and the band are computed by the `calculatePlanInstallment` activity of `TreatmentWorkflow` on queue `rwb-treatment`, from the plan terms already recorded against the treatment by the affordability answer (DF-TRT-031, DF-TRT-009), the ALS balance read read-only at the ACE batch date through `recovery.v_ace_account` (DP-05, `total_balance` and the account identifiers of DF-ACE-001 to DF-ACE-042) and the band, the floor and the freshness limit read from the reference sets of rwb-case through RWB-P3-E1043-CON with the set version (DP-07). "The range the officer may move within" is the amount band bounded by `settlement_range_low` and `settlement_range_high` with `floor_price` applied, the three names the routing logic already uses in R-SET-04 and R-SET-05; the element that carries them, its field names and the set that holds them are not specified in any source and are the working read of ASM-4359 and ASM-4360 (GAP-2651, GAP-2652). "Writes the result to the decision log with the rule version" is the local `DecisionRecordWriter.record(DecisionRecord)` call in the same transaction as the element and the plan terms, with MSG-P7-003 on failure (DP-03; RWB-PLT-E1027-CON); `decision_log_entry` stays P7's and is never written here, and the version written is the rule version in force together with the reference-set version. "Its trigger arrives" is the case signal the parent `CaseWorkflow` forwards to the stage (EV-29), because the FSD names "a completed ACE batch, an event or a timer" and no source names which one (GAP-2656; ASM-4364). The stale-data rule of the FSD is the guard before the calculation: VR-S2-006-1 with MSG-P1-001, so an input older than today's ACE batch produces no number at all. No state is named in the two criteria this story owns; the case statuses of the legacy key stay with rwb-case and are applied by the parent, and AC2, the R-SET-01 state step, is not assigned to this story (GAP-2657; ASM-4365).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The model installment and the range are produced per calculation from the accepted plan terms, the ALS balance at the ACE batch date and the band in force; no amount, count, rate or bound is a constant | BR-S2-006 of FSD A2.6.3.1; DF-TRT-009; DF-TRT-031; R-SET-01 |
| BR2 | The band, the floor and the freshness limit are reference rows of rwb-case read through its contract with the version in force, and the version is recorded with the result | DP-07; R-SET-04; R-SET-05; default ruling on reference data |
| BR3 | ACE balances are read only, at the ACE batch date, from this service's own SELECT-only views, one hop inside the 2 s budget, and no balance is copied into `rwb_treatment` | DP-05; VR-S2-006-1; D-RCV-35; ADR-010 |
| BR4 | A data product older than today's ACE batch blocks the step and is named with its date; nothing is computed on a stale input | VR-S2-006-1; MSG-P1-001 |
| BR5 | A payoff older than the freshness limit is not used: the step warns, requests a fresh figure and waits | R-SET-03; MSG-S2-002 |
| BR6 | The element, the plan terms and the decision record are written in one transaction; if the record cannot be written nothing changes and MSG-P7-003 is shown | DP-03; RWB-PLT-E1027-CON; ADR-022 |
| BR7 | The rule version and the reference-set version that decided are written on the record and on the element; no rule ID, state name, threshold or message text is written in code | BR-S2-006; EV-30 |
| BR8 | The case status is never this service's: the stage reports and the parent applies the rule, so a replay can never move a case twice | DP-01; ASM-4362 |

**Where each rule lives in the target.** BR1 is the calculation activity and the reason the treatment's own terms are an input rather than a second definition. BR2 is the client library call and the version column on the element. BR3 is the SELECT-only grant and the reason no balance column exists in `rwb_treatment`. BR4 and BR5 are the two guards before the calculation, one on the data product date and one on the payoff date, and they produce different messages because one is a system fact and the other a case fact. BR6 is the `MANDATORY` propagation of the library write. BR7 is why the package version and the set version are inputs of the activity and fields of the element. BR8 is the boundary to rwb-case.

### 9. State transitions

None of the case statuses below is this service's; the table shows what the stage reports and what it never writes, so a reader can see the boundary of this story.

| Rule | From (rwb-case) | Event | Condition | What this stage does | To (rwb-case) |
|---|---|---|---|---|---|
| R-SET-01 | `ROUTE_APPROVED_SETTLEMENT` | `ROUTE_APPROVED` | `decision.approved` and route = R2 | Evaluates the row, reads the payoff and the band, computes the installment and the range, records the element with its record, reports `PAYOFF_AND_RANGE_SET` | `PAYOFF_AND_RANGE_SET` |
| R-RES-07 (plan branch) | `AFFORDABILITY_IN_ACE` | `AFFORDABILITY_PASSED` | `affordability_result = pass` | Takes the accepted plan terms, computes the model installment and the band, records both, reports the answer to the parent | `WITH_FCR_OFFICER` |
| R-SET-04, R-SET-05 (read only) | `WITH_FCR_OFFICER_SET` | `OFFER_PREPARED` | `offer_amount` inside or below the band and the floor | Supplies the numbers the offer stories test against; this story moves nothing | `OFFER_WITH_CUSTOMER_SET` / `AWAITING_APPROVAL_SET` |

The states of this story's own object are the treatment's: `Draft`, `submitted`, `approved`, `booked` and `broken` as SCR-14 shows them, and they belong to the sibling stories of this service. The `PlanInstallment` element has no state machine: it is written once per calculation and replaced only by a later calculation on the same treatment, each with its own decision record. The `TreatmentWorkflow` execution has the platform states RUNNING, COMPLETED and FAILED, and a FAILED execution restarts from the last recorded step, which is why the reads and the write are activities and not workflow-local computation.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The recovery squad (RW-TRIBE) | Writes the workflow branch, the calculation activity, the two reads, the record and the tests |
| RW-RESTRUCT, restructuring officer (FCR) | Triggers the step through the case, reads the model installment and the range, and builds the offer; holds rights C, R and U on the capability area |
| RW-CASEOWN, RW-SPECIAL, RW-GUARANT | Hold rights C, R and U on the capability area and see the element on the treatment |
| RW-TEAMMGR, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and the read-only roles of TSD S2 T6.1 | Right R only: they read the element and cannot trigger a recalculation |
| RW-PRODHEAD, RW-CREDCOMM | Rights R and A: they approve an offer below the floor and read the range it was tested against |
| SY-CASEWF, the case workflow module | Runs the step unattended under the service identity and reports to the parent |
| rwb-case (P3) | Owns the case, its status, the parent `CaseWorkflow` and the reference data this step reads |
| P7 rwb-decision | Owns the rule package and the route set, their approval, their effective date and the central ledger |
| ACE and its DBA | Own the `recovery.v_ace_*` views, their grants and the batch that dates them |
| The platform workflow and data owners | Own the task queue, the namespace, the ACE PostgreSQL grants and the reference-data client library |

The check is the platform guard library's: this story declares the capability area "Treatment and offer" and the right C, R or U on each entry point. No credential and no personal name appears in the workflow input, the activity request or the logs, which carry the case ID, the treatment ID, account keys, amounts and versions only.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Write (the row the element is recorded against) |
| DF-TRT-002 | treatment | case_id | Read |
| DF-TRT-003 | treatment | decision_log_id | Write |
| DF-TRT-004 | treatment | treatment_type | Read |
| DF-TRT-005 | treatment | proposed_by | Read |
| DF-TRT-006 | treatment | proposed_at | Read |
| DF-TRT-007 | treatment | offer_amount | Read |
| DF-TRT-008 | treatment | haircut_amount | Read |
| DF-TRT-009 | treatment | installments | Read and write |
| DF-TRT-027 | treatment | interest_rate | Read |
| DF-TRT-031 | treatment | installment_amount | Read and write |
| DF-TRT-032 | treatment | installments_paid | Read |
| DF-TRT-033 | treatment | installment_shortfall | Read |
| DF-ACE-001 to DF-ACE-042 | v_ace_account | account_key, account_code, account_status, contract_no, product_category_efs, total_balance and 36 more | Read only |
| DF-REF-001 to DF-REF-015 | reference set | the band bounds, the floor and the freshness limit with their version | Read |
| DF-DEC-002 to DF-DEC-016 | decision_record | the seven field groups | Write |

`treatment` and `decision_record` are this service's own objects in `rwb_treatment`, written through its own repository and login (DP-01). The ACE columns are read through the read-only views at the batch date and are not copied into any column of this service: there is no balance field, no band field and no floor field in `rwb_treatment`, and the element of RWB-S2-E3006-CON is the only shape the numbers take. The reference rows are read through RWB-P3-E1043-CON and are never joined to this service's tables. The case, its status and the case facts are not read from a table: they arrive on the case signal the parent forwards. The field names of the element itself are Not specified in the source documents (GAP-2651; ASM-4359).

### 12. Contract

#### 12.1 REST operations provided

None. This story adds no path to base `/api/recovery/treatment/v1` (DP-13): the element is read through the treatment read of RWB-S2-E3001-APP, `GET /api/recovery/treatment/v1/treatments/{treatmentId}` (API-S2-002 of TSD S2 T-A.1), and the shape, the required fields, the versioning and the fakes of that element are declared by RWB-S2-E3006-CON and are not restated here.

#### 12.2 REST operations consumed

| Operation | Contract | Element | Owner | Use |
|---|---|---|---|---|
| Reference-data read on base `/api/recovery/case/v1` | RWB-P3-E1043-CON | The reference sets holding `settlement_range_low`, `settlement_range_high`, `floor_price` and the freshness limit, with the set version | P3 rwb-case | The band, the floor and the freshness limit of the calculation |

The operation and its path inside the rwb-case contract are not specified in the sources read here, so the row names the contract and the elements rather than an invented path (GAP-2652; ASM-4360). The read goes through the client library of RWB-PLT-E1043-CON, one hop, inside the 2 s budget, and caches only by set and version. The case status is not consumed as a REST read: it arrives on the case signal the parent forwards. The ACE balance is not a REST read either; it is a SQL read of the views in 12.7.

#### 12.3 Events published

None. The service's topic is `rwb.treatment.events.v1` with names `rwb.treatment.<Event>.v1` (DP-14), and its one catalogued event EV-10 `rwb.treatment.TreatmentApproved.v1` belongs to the offer story of this service (TSD S2 T5.3). This story publishes no event and writes no outbox row of its own: the stage report to the parent is a Temporal signal inside the case, not a Kafka event.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | Loads the package and the route set in force, verifies the checksum, swaps them atomically and keeps the last good set on failure; EV-30 |

The event is consumed by the service template's rule loader and this story reads the version it put in force. `rwb.payment.PaymentMissed.v1` (EV-12) and `rwb.deviation.DeviationRaised.v1` (EV-06) are the other events the service has available; they drive the cure-period and deviation branches of `TreatmentWorkflow`, which belong to the later stories of this epic and not to this one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` (the plan-installment branch) | Child workflow of `CaseWorkflow`, one per case, on this service's own queue | `rwb-treatment` in namespace `rwb-recovery` | Input: the case ID, the treatment ID, the case status on the signal, the event. Output: the stage report with the model installment, the range, the rule version and the set version |
| `EvaluateRules` | Activity of the template | `rwb-treatment` | The package and route set in force and the case facts in; the rule ID, the action and the next event out; `NoPackageInForce` is not retried |
| `calculatePlanInstallment` | Activity | `rwb-treatment` | The ACE view read at the batch date, the plan terms on the treatment and the reference-data read in; the `PlanInstallment` of RWB-S2-E3006-CON out; retried by the workflow, with the stale guards non-retryable |
| `RecordAndApply` | Activity of the template | `rwb-treatment` | The element, the plan terms, the decision record and the stage report in one transaction |

The workflow name is fixed by Temporal and Drools Design slides 13 and 18; the three activity names are this story's choice. The retry policy is the workflow kit's (1 s initial interval, back-off 2, 10 attempts; `NoPackageInForce` and a stale product non-retryable). A replay never re-reads the views: the answer is recorded by the activity and read from history.

#### 12.6 Schedules

None. The step is signal-driven from the case and owns no Temporal Schedule and no legacy Quartz job. The freshness test is a comparison at the moment of the calculation, not a scheduled scan.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 rwb-treatment | Created by the per-service Flyway sequence and written here for the element and the plan terms; DF-TRT-001 to DF-TRT-033 of TSD S2 T3.1, with no balance, band or floor column |
| `decision_record` | `rwb_treatment` | PLT library object | Written only through `DecisionRecordWriter` in the caller's transaction (DP-03) |

No table of another service is read and no foreign key crosses a schema (DP-01). Two `recovery.v_ace_*` views of the ACE database are read, `v_ace_account` and `v_ace_batch_status`, read only at the ACE batch date and with no copy kept; the case table of rwb-case, the reference sets of rwb-case and the rule tables of rwb-decision are never named in SQL.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case reference-data fake (RWB-P3-E1043-CON) | The band, the floor and the freshness limit | A set in force at version `REF-2026.11`; a set with the floor above the band; no set in force; a set whose version cannot be resolved |
| ACE view fixture | `v_ace_account` and `v_ace_batch_status` | A balance at today's batch date; a product dated yesterday; a case with two accounts; an unreachable view |
| RWB-S2-E3006-CON element fake | The `PlanInstallment` shape | A complete element; one per missing required field; an element with and without the reference-set version |
| Decision-record writer fake (RWB-PLT-E1027-CON) | `DecisionRecordWriter` | An accepted record with its chain sequence; a refusal with MSG-P7-009 and the field; a failure with MSG-P7-003 |
| Rule-package fake | The package and route set in force | Version `RESTRUCTURE-2026.11` with the range rows; a set with no matching row; a checksum mismatch |

The reference-data and ACE fakes are the Day-1 unblockers: the build and every test run against them, and no test calls the live reference data or reads the production views.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 1 (`rwb-case` reference data) | One hop, 2 s budget, through the client library of RWB-PLT-E1043-CON |
| Kafka | 0 | 1 event (`rwb.decision.RulePackageInForce.v1`) | Own topic, no row written by this story; inbox dedupe by cloud event id |
| Temporal | `TreatmentWorkflow` and 3 activities on `rwb-treatment` | The case signal forwarded by the parent `CaseWorkflow` | Namespace `rwb-recovery`; no Schedule |
| SQL view | 0 | 2 (`recovery.v_ace_account`, `recovery.v_ace_batch_status`) | Read only, at the batch date, no copy |
| File | 0 | 0 | No file is read or written |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, modules `planinstallment` and `workflow`, with the published types in `...treatment.api`. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery` (DP-13; §R4).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is taken as the service's own SELECT-only views, because the Work Package records no contract dependency on P1; the reading and the conflict with Architecture v5 slide 8 are in GAP-2654 and ASM-4362. DP-07 is the governed-data path of the band and the floor. DP-03 and DP-19 are the record and the screen path.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `PlanInstallmentBranch` | Workflow | The branch of `TreatmentWorkflow` that opens the step, reports the outcome and waits |
| `EvaluateRules` | Activity | Runs the package and route set in force and returns the rule ID and the action |
| `calculatePlanInstallment` | Activity | Reads the views and the reference set, applies the guards, computes the element |
| `AceAccountReader` | Repository | The two read-only view queries; no entity, no cache beyond the request |
| `ReferenceDataClient` | Client | The rwb-case reference read through `rwb.treatment.referencedata` of RWB-PLT-E1043-CON, cached by set and version |
| `PlanInstallmentRepository` | Repository | Writes the element against the treatment row and the two plan fields |
| `DecisionRecorder` | Service | Assembles `DecisionRecord` and calls `DecisionRecordWriter.record` in the caller's transaction |
| `StageReporter` | Service | Builds the stage report and the officer messages of the guard paths |

**Database.** No new table and no new column: the element is written against `treatment` in `rwb_treatment` using DF-TRT-009, DF-TRT-031 and DF-TRT-027, and `decision_record` is the library object of DP-03. The element's own field identifiers are not allocated in the Logical Data Model (GAP-2651; ASM-4359), and nothing is added to the schema until RWB-S2-E3006-CON freezes the shape.

**Configuration and reference data.** The reference-set identifiers, the band, the floor and the freshness limit are data of rwb-case with a version and are read, never configured here. The retry numbers, the activity name and the 2 s budget are configuration of the activity and the client. The capability area "Treatment and offer" and the rights are access data of P4 read through the guard library.

**Build steps**

1. The branch of `TreatmentWorkflow` on `rwb-treatment`, its input record and the stage report.
2. `EvaluateRules` against the package fake, with the range rows as rule rows and the `NoPackageInForce` answer.
3. `AceAccountReader` against the view fixture, with the batch-date test and MSG-P1-001 (AC1, X1).
4. `ReferenceDataClient` on RWB-PLT-E1043-CON against the reference fake, with the version on the answer and the refusal path (AC1, X2).
5. `calculatePlanInstallment` with the element of RWB-S2-E3006-CON and the stale-payoff guard (AC1, X7).
6. `RecordAndApply` with the record in the same transaction and the rollback path of MSG-P7-003 (AC3).
7. The missing-value path with MSG-GEN-001 and the task for the owner (X5).
8. Tests for AC1 and AC3 against the fakes, the component tests of X1, X2 and X9, and the replay test of X8.

**Feature flag.** `rwb.treatment.plan-installment`.

**Done when.** The tests in section 16 pass, the branch runs from a synthetic case signal in SIT with the views and the reference data faked, the element and the plan terms appear on the treatment, the record is written in the same transaction and rolls back with the action, the stale product path blocks with MSG-P1-001 and the officer sees the model installment and the range on SCR-14 and SCR-15.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A data product the step reads is older than today's ACE batch | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-S2-002 | The payoff figure on the case is older than the freshness limit | The payoff is from {date}. A new figure has been requested. |
| MSG-GEN-001 | A required value is missing and the step cannot compute | Enter {field}. |
| MSG-GEN-006 | The reference set is not in force, or a read does not answer | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | A role without the right in the capability area tries the action | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | A record is refused for a missing or invalid field | The decision record was refused: {field} is missing or not valid. |

The texts are copied unchanged from the legacy story, FSD A2.6.3.1, RWB-PLT-E1027-CON and the platform message set, and this story adds no message ID. MSG-S2-001 and MSG-S2-003 of the legacy validation table belong to the offer and its expiry and are raised by the offer stories of this service, not here. Thai text for each message follows decision DL10.

### 15. Screens and states

SCR-15 Settlement offer shows the model installment, the range, the floor and the payoff with its as-at date, in the states Draft, below floor, approved, sent and accepted. SCR-14 Treatment record shows the same element against the treatment, in the states Draft, submitted, approved, booked and broken. Both are reached through the gateway-bff composite route, which calls rwb-case and rwb-treatment and composes the answer (DP-19; Architecture v5 slide 41). The screen field list and the route specification belong to the platform edge story and the screen owners; this story fixes what the service records and what the sibling story's read returns. A blocked step is shown as its message on the treatment screen with the product and its date, never as an empty range.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-006-01 | AC1 | End to end | Calculate the plan installment |
| TC-E3-006-03 | AC3 | End to end | Not recorded |
| TC-E3-006-04 | Access | Component | A role without the right is refused with MSG-P4-002 |
| TC-E3-006-05 | Principle 5 | Component | A forced decision log write failure stops the action with MSG-P7-003 |

The legacy test case IDs, their Covers and their Data are kept in order and character for character; the legacy level "System" maps to "End to end" and "Access" to "Component", as in the other stories of this run. TC-E3-006-02, which covers AC2 and the R-SET-01 state step, is not carried here because AC2 is not one of the criteria this story is given; the state movement is proved with the settlement stories of this service (GAP-2657; ASM-4365). The reference-data, view, element, decision-record and rule-package fakes of section 12.8 stand behind every case, and the full Given, When and Then of each is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID. The `-ITG` copies belong to the wave 2 integration harness (RWB-ITG-W2). The contract's own tests are TC-S2-E3006-CON-01 to -05 and are owned by RWB-S2-E3006-CON.

### 17. Guardrails

- No value a business person may change is written in code: the band, the floor, the freshness limit, the rule IDs, the condition texts and the six messages are reference rows, rule rows or package content, never constants (BR-S2-006; BR1, BR2).
- No personal data in logs, workflow inputs, activity requests, events or tests: the step carries the case ID, the treatment ID, account keys, amounts and versions only, and the fixture is synthetic.
- No read of another service's tables: the case arrives on the signal, the reference rows come through the contract, and nothing joins across a schema (DP-01; DP-07).
- No copy of ACE data: the views are read at the batch date and no balance, band or floor column exists in `rwb_treatment` (BR3; DP-05).
- ACE data only through the owner's contract or the `v_ace_*` views, and here only two views with SELECT granted to this service's login (ASM-4362).
- No live view and no live reference data in any test: the fixtures and the fake are the only endpoints, so a red test never depends on the ACE batch or on P3's estate.
- No business value in the record: the `DecisionRecord` carries the rule ID, the rule version, the set version, the final call and the result code, never a free-text reason or a customer field (DP-03).
- No status change from this service: the stage reports and the parent applies the rule (BR8).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| None (GAP-2653; ASM-4361) | The model installment and the range the officer may move within, produced with the version of the policy that produced them | Business Requirements Program, section 5.9 | FEAT-TRT-06 | 05 Restructure; 07 Route, settle and claim | R-SET-01; R-SET-04; R-SET-05 | TC-E3-006-01, TC-E3-006-03, TC-E3-006-04, TC-E3-006-05 |

REQ-S2-001 and REQ-S2-004 of section 5.9 describe the surrounding outcomes — a restructure reaching the officer with the case, and terms negotiated inside a rule-set range — but neither names FEAT-TRT-06, and TSD S2 T8 maps its ten requirement IDs to FEAT-TRT-01 only. The trace therefore runs on the feature code until the C1 PRD allocates a requirement (GAP-2653; ASM-4361).

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3006-CON | Contract | H: declares the `PlanInstallment` element, the reference-data consumption rule, the ACE read rule, the versioning rule and the fakes this story builds against |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library, with MSG-P7-009 and MSG-P7-003 |
| RWB-PLT-E1043-CON | Contract | H: the reference-data client library, its cache keyed by set and version and its refusal |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route through which SCR-14 and SCR-15 show the element |
| RWB-P3-E1043-CON | Contract | C: the reference-data contract of rwb-case that holds the band, the floor and the freshness limit; never blocks the build |
| RWB-S2-E3005-APP | App development | Sibling: the affordability answer whose accepted terms are this step's input |
| RWB-S2-E3001-APP | App development | Sibling: the treatment record and the read that returns the element |
| RWB-S2-E3002-APP, RWB-S2-E3003-APP | App development | Siblings: the offer inside the range and the below-floor approval, which are tested against this range |
| RWB-S1-E4006-APP | App development | Sibling service: the payoff and settlement range of the route decision, FEAT-VAL-06, which reads the same ACE balance for a different purpose and owns its own element |
| P3 rwb-case | Service | The case, its status, the parent `CaseWorkflow` and the reference data |
| P7 rwb-decision | Service | The rule package and route set, their version and the central ledger; EV-30 is consumed here |
| RWB-ITG-W2 | Integration | I: the cross-service proof of the reads and the record against the live owners, and the owner of the `-ITG` copies |

### 19. Out of scope

- The published element, the reference-data consumption rule, the ACE read rule, the versioning and the fakes: RWB-S2-E3006-CON.
- AC2 of the legacy key and the R-SET-01 state step: not assigned to this story; the state movement is proved with the settlement stories of this service (GAP-2657; ASM-4365).
- The affordability branch, the Nexus call to the ACE Common restructure calculator and its result: RWB-S2-E3005-APP.
- The treatment record, its create and read operations, its states and its read representation: RWB-S2-E3001-APP.
- The settlement offer inside the range and the below-floor approval: RWB-S2-E3002-APP and RWB-S2-E3003-APP; the offer build and the validity timer: the offer stories of this service.
- The payoff and settlement range of the route decision: FEAT-VAL-06 and RWB-S1-E4006-APP, a different feature and a different service.
- The case, its status, the parent `CaseWorkflow` and the case facts: rwb-case (P3), reached only on the forwarded case signal.
- The reference data, its sets, its values, its version and its governance: rwb-case (P3) and its contract; this story reads and never writes them.
- The `recovery.v_ace_*` views, their columns, their grants and the ACE batch that dates them: ACE and its DBA (GAP-2654).
- The rule authoring, the four-eyes approval, the effective date, the rollback and the central ledger: rwb-decision (P7).
- The screens SCR-14 and SCR-15, their field lists and the gateway-bff composite route: the platform edge story and the screen owners (DP-19).
- The real cross-service proof against the live owners and the `-ITG` copies of the legacy cases: RWB-ITG-W2.

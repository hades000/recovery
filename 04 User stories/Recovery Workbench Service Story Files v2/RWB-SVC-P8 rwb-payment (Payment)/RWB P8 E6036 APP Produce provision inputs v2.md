# RWB-P8-E6036-APP Produce provision inputs

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P8-E6036-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-payment |
| Service epic | RWB-SVC-P8 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-036 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement |
| Patterns applied | DP03, DP05, DP19 |
| Parallel lane | L-P8-N |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract version | Not specified in the source documents (DOR-RWB-P8-E6036-APP-23); the build uses the /v1 path only |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md (FEAT-PAY-08 has no FR or REQ ID in the PRD yet; Not specified in the source documents (GAP-2562)) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 12 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **finance and CFO delegate**, I want **the Workbench to build the provision inputs Finance needs from the case and asset positions**, so that **every payment and booking is matched to its case**.

This is the application slice of legacy RWB-E6-036 (FEAT-PAY-08 Produce provision inputs, module P8 Payments and posting, priority Must, depends on FEAT-PAY-07, epic E6, release 30 April 2027). It owns:

- the two legacy acceptance criteria of the story, copied verbatim with their origin tag, and the rules, messages, screen, rights and test cases they depend on;
- the provision-input build step of this service: one input row per case in scope, built from the case position, the held-asset position, the receipts of the business date and the rule version in force, and answered as the step's result;
- the case position read on the rwb-case contract, because `recovery_case` is P3's table and this service holds no grant on `rwb_case` (DP-01);
- the asset position read on the rwb-asset contract, because the held-asset position and its provision step are S5's (context pack, the S5 service row of Architecture v5 slide 4);
- the receipts and the ACE batch status on the rwb-source-data contract, because this service holds no `v_ace_*` grant (DP-05);
- the local decision record of every build, written through RWB-PLT-E1027-CON before the input set is answered, and MSG-P7-003 when it cannot be written (DP-03; legacy AC1 and AC2);
- the build-once key per case and business date, so a repeated business date answers once;
- the states of SCR-28 Proceeds matching, which reaches this service through the gateway-bff composite route and one hop only (DP-19).

It does not own the positions (P3 and S5), the ACE facts (P1), the rule rows (P7), the route states and the release of the provision that precede the feed (S7, S5, S6), the accounting entries and posting file (FEAT-PAY-07), the finance-feed delivery (published nowhere) or the deployment (the operations story of this key and the wave 4 harness); section 19 lists each one.

### 2. Business rationale

Legacy RWB-E6-036 gives Finance one step after the money is posted: the Workbench builds the provision inputs it needs from the case and asset positions, and the outcome is written to the decision log with the rule version. The FSD keeps the feature as FEAT-PAY-08 with the same objective, a step that runs unattended with no primary role, the Finance and CFO delegate as the secondary use, and the metric "receipts matched the same day, rising each month" (FSD P8 A2.8.1 and A2.8.3.3). In the Epic 3 to 8 specification the feature sits in E6, module P8, runs unattended, touches ALS and GL and depends on FEAT-PAY-07 (Epics 3 to 8 Specification v3, E6 row FEAT-PAY-08). The Epic 6 BRD carries the same obligation in its business rule row BR-054, which names FEAT-PAY-08 and RWB-E6-036 beside the write-off postings and their release of the provision (Business Requirements Epics 3 to 8 v1, BR-054).

What D-RCV-60 changes is who owns each part of the step.

- **both positions are answers, not reads.** The case position is rwb-case's, the held-asset position is rwb-asset's and the ACE facts belong to rwb-source-data, so the step asks two owners and one data owner on their contracts and reads no foreign table (DP-01, DP-05; GAP-2564; ASM-4230).
- **the build is this service's.** rwb-payment holds the matched receipts in `proceeds` and the posting references of the FEAT-PAY-07 stories, so the assembly of the input from the posted positions belongs here (context pack ownership row `proceeds`; TSD P8 T3.1).
- **the decision is recorded first.** One record per build, through the local library and the shared topic `rwb.decision-record.v1`, before the input set is answered; a failed write changes nothing and shows MSG-P7-003, which is what AC1 and AC2 ask and DP-03 with R-UNI-39 behind it.
- **the content is policy.** The provision step, its thresholds, its re-appraisal interval and the period the input covers are policy parameters and rule rows with a version (Business Requirements Epics 3 to 8 v1, ASM-012 and Q-005), so the build carries the rule ID and the version in force and invents no threshold or period (GAP-2563; ASM-4229).
- **the feed is a separate, unpublished deliverable.** R-WO-26 sends the provision inputs to Finance on the finance provision feed inside the month-end close window, and no interface number, file layout, transport or acknowledgement is published, and no P8 table holds a provision input (GAP-2565; ASM-4231). The build is the story's deliverable; the delivery stays out of scope.

The legacy criteria are kept exactly and they are thin: AC1 says "the data and the rule version this feature needs are in place / its trigger arrives" and the legacy test cases name no case, amount, product group or date (GAP-2562; ASM-4228). Everything the legacy omits is filled from FSD P8 A2.8 and BR-054, or held as a placeholder.

### 3. Preconditions

- RWB-PLT-E1027-CON is published with its writer fake: the library writes in the caller's transaction and a failed write stops the action with MSG-P7-003 (DP-03).
- RWB-PLT-N001-CON is published: SCR-28 Proceeds matching reaches this service through the gateway-bff composite route, one hop, and no screen calls the service directly (DP-19).
- The case position of a case is answered on the rwb-case contract: the case reference, its product group, its status and stage, its balance components and its open treatments. No `recovery_case`, `case_account`, `task` or `timer` row is read as a table (DP-01).
- The held-asset position of a case is answered on the rwb-asset contract: the asset reference, its book value, the date taken in, the holding age and the provision step in force. The operation name is Not specified in the source documents (GAP-2564; ASM-4230).
- The receipts of the business date and the ACE batch status of the source `ALS` are answered on the rwb-source-data contract with the freshness stamp of the data product, because this service holds no `v_ace_*` grant (DP-05; GAP-2564; ASM-4230).
- The rule rows of the provision-input family are in force at their version in rwb-decision, and the version is read with them; the package code, the rule IDs of the build, the provision step thresholds and the period of the input are Not specified in the source documents (GAP-2563; ASM-4229).
- The ACE batch for source `ALS` is complete for the business date: FSD P8 A2.8.4.4 names the completed ACE batch of source `ALS` as the trigger of the family, and VR-P8-008-1 holds the run when the batch is late or failed (FSD P8 A2.8.3.1).
- No CON story of this legacy key is in the plan's build list: the H rows are the two platform CON stories above, so the field list, the row layout and the answer shape of the provision input are taken from the legacy Data table, `proceeds` and the business rule BR-054, and every value no source publishes is held as a placeholder (GAP-2563; ASM-4229).
- The build owns no table: `proceeds` and the platform library objects are the only tables of `rwb_payment` this step touches, and no provision-input row is persisted because no source publishes one (GAP-2565; ASM-4231).
- The capability area "Write-off and posting" and its rights R, A and U exist as access rows of rwb-access, and the service runs as its own login on schema `rwb_payment` with no grant on another `rwb_*` schema (TSD P8 T6.1; Architecture v5 slide 29).
- No approval is needed to build against a Draft delivery scope, and no human verification stop is part of this run.

### 4. Flow

1. The completed ACE batch of source `ALS` for business date D is announced by `AceDataReady` (EV-26); the inbox writes its processed-event row and a redelivery is a no-op (DP-09).
2. The provision-input build step runs for D on task queue `rwb-payment` in namespace `rwb-recovery`, inside the service's ACE-batch-started run family; the run and step names are Not specified in the source documents (GAP-2563; ASM-4229).
3. The step reads the receipts of D and the batch status of `ALS` on the rwb-source-data contract, one hop with a 2 s budget and a breaker, and holds when the data product is stale (VR-P8-008-1, MSG-P1-001).
4. It reads the rule rows of the provision-input family at the version in force from rwb-decision, with the provision step, its thresholds and the period of the input; no threshold and no period is a constant of the build (BR-P8-008; GAP-2563).
5. For each case in scope it reads the case position on the rwb-case contract: the case reference, the product group, the status and stage, the balance components and the open treatments. No case row is read as a table.
6. It reads the held-asset position of the case on the rwb-asset contract: the asset reference, the book value, the date taken in, the holding age and the provision step in force; a case with no held asset answers an empty position and is not held for it.
7. It assembles one input row per case and business date: the case and product group, the position amounts of the case, the asset position and the provision step, the receipts matched in `proceeds` and the posting reference the FEAT-PAY-07 stories wrote, and the rule ID with the version in force (BR-054; GAP-2563).
8. The decision is written before the answer: one record through the local decision-record library, with the case reference, the business date, the rule IDs and versions, the inputs reference and the built amounts (DP-03).
9. A failed record write stops the build: no input row is answered, MSG-P7-003 is raised and an incident is opened under R-UNI-39 (legacy AC2; FSD P8 A2.8.4.3).
10. The input set of D is answered as the step's result, and the same case and business date answered again returns the stored result and counts the repeat (R-UNI-40; GAP-2565; ASM-4231).
11. Finance and the CFO delegate read the position the input set is built from on SCR-28 through the composite route, one hop, and the delivery of the set to Finance is the unpublished finance-feed path (GAP-2565; ASM-4231).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The local decision record cannot be written (library failure, stopped hash chain, outbox failure) | Nothing is built and nothing is answered; an incident is opened | MSG-P7-003 | AC2, TC-E6-036-02, TC-E6-036-04 |
| X2 | The role does not hold the Write-off and posting right R for the screen position the input set is built from | 403 before any read; nothing is built and no record is written | MSG-P4-002 | AC4, TC-E6-036-03 |
| X3 | The ACE data product of source `ALS` is stale after a late or failed batch | The build holds, answers nothing and resumes on the next fresh answer | MSG-P1-001 | AC1 |
| X4 | The rwb-case, rwb-asset, rwb-source-data or rwb-decision contract does not answer inside 2 s, or its breaker is open | The step retries on the run's own policy; nothing is built and nothing is answered | None | AC1 |
| X5 | No provision-input rule row is in force, or the period of the input cannot be derived | The build holds and answers nothing; the package gap is reported to rwb-decision | None | AC1 |
| X6 | The same case and business date are built twice, or the same event is redelivered | The stored answer is returned, no second record and no second input row, and the repeat is counted | None | AC1 |
| X7 | A component, a statement or a test reaches a `v_ace_*` view, a `recovery_case` row, an asset row or another `rwb_*` schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC3, TC-E6-036-05 |

X1 and X2 are the exception paths of the legacy key and of FSD P8 A2.8.4.3 carried onto the split; X3 and X5 are the stale-data and no-rule paths the family already declares; X4 is the 2 s contract budget; X6 is the build-once rule; X7 is the DP-01 and DP-05 boundary. No threshold, period or percentage appears in this table, because none is published.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against the rwb-case, rwb-asset, rwb-source-data and rwb-decision fakes and the decision-record stub, on its own schema, and needs no live neighbour |
| Negotiable | The run and step names, the answer shape and the consumer group are this story's choice; the legacy criteria, the messages, the lists and the rights are fixed |
| Valuable | Finance holds a provision input per case, built from the posted positions, on the morning after the ACE load, with the rule version on every record |
| Estimable | One step, four contract reads, one record write, one input row per case, one read-only screen state and no new table |
| Small | Finished inside two weeks with its tests on the fakes |
| Testable | Each criterion runs on synthetic cases, assets and receipts through the contract fakes, plus the access case and the forced record failure |

### 7. Acceptance criteria

```gherkin
Feature: Produce provision inputs

  Background:
    Given case "RC-2026-000555" of product group MORTGAGE is open on business date 2026-12-31
    Given the case has held asset "AST-2026-000555" with book value 3,200,000.00 THB and the provision step of its holding age is in force
    Given the receipts of the business date are posted and the provision-input rule rows are in force at their version

  Scenario: AC1 Produce provision inputs (legacy RWB-E6-036 AC1)
    Given the rwb-case contract mock returns the case positions of the open cases and the rwb-asset contract mock returns the asset positions of the held assets
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then builds the provision inputs Finance needs from the case and asset positions
    Then the system writes the result to the decision record with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E6-036 AC2)
    Given the rwb-decision contract mock returns a failed decision-record write
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 A statement outside rwb_payment is refused (new, D-RCV-60)
    Given a component, a statement or a test of this build reaches a `v_ace_*` view, a `recovery_case` row, an asset row or another `rwb_*` schema
    When the statement runs
    Then the grant refuses the statement and the boundary test fails the build; nothing is released

  Scenario: AC4 A role without the Write-off and posting right is refused (new, D-RCV-60)
    Given the role does not hold the Write-off and posting right R for the screen position the input set is built from
    When the role reads the position on SCR-28
    Then the request is refused with 403 before any read; nothing is built and no record is written; the user sees MSG-P4-002

  Scenario: AC5 The input set is recorded before it is answered and repeats answer once (new, D-RCV-60)
    Given the input set of business date 2026-12-31 is built for case RC-2026-000555
    When the same case and business date are built again
    Then the decision is recorded before the input set is answered; the repeat returns the stored set, writes no second record and no second input row, and is counted; no person data enters the record

  Scenario: AC6 A redelivered AceDataReady event is a no-op (new, D-RCV-60)
    Given the completed ACE batch of source `ALS` for business date 2026-12-31 has been announced by AceDataReady
    When the same event is delivered a second time
    Then the inbox writes no second processed-event row, no second record and no second input row, and the stored answer is returned

  Scenario: AC7 A retried or timed-out activity writes no second record (new, D-RCV-60)
    Given an activity of the build is retried or runs past its timeout
    When the activity is run again for the same case and business date
    Then no second decision record and no second input row are written and the stored answer is returned

  Scenario: AC8 A consumed call that fails or does not answer changes nothing (new, D-RCV-60)
    Given a consumed call of the build fails or does not answer
    When the build reaches that call
    Then nothing is built, nothing is written and nothing is answered

  Scenario: AC9 A status change the model does not allow is refused (new, D-RCV-60)
    Given a status change that the model does not allow is requested
    When the change is submitted
    Then the change is refused and nothing changes
```

The two criteria are the legacy criteria of RWB-E6-036 word for word, with their origin tag added and the decision log renamed to decision record, and nothing else changed: the legacy wording of `its trigger arrives`, `the provision inputs Finance needs` and `the decision record cannot be written` all stand, with decision record replacing the legacy decision log. One leading `Given` is added to each, and those two lines are the only additions: AC1 needs the two positions, which are rwb-case's and rwb-asset's facts, and AC2 needs the failed write of the decision record, which is the platform and rwb-decision boundary. What the legacy lines describe happens in four places in the target: rwb-case answers the case position, rwb-asset answers the asset position and its provision step, this story builds the input set, writes the record and answers it, and the finance feed carries it to Finance. The field list, the period, the provision step thresholds and the answer shape of the input set appear in no source and are held as GAP-2563 with ASM-4229, and the missing test data as GAP-2562 with ASM-4228.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| VR-P8-008-1 | Data product stale after a late or failed ACE batch for its source (batch status on the rwb-source-data contract) raises MSG-P1-001 `{product} is from {date}. Today's ACE batch has not arrived.` | FSD P8 A2.8.3.1, with the batch-status read moved to the rwb-source-data contract (GAP-2564) |
| BR-P8-008 | No value a business person may change is written in code; it is read from reference data with its version | FSD P8 A2.8.3.1, copied character for character |
| BR1 | The provision input of a case is built from its case position, its held-asset position, the receipts matched to it and the posting reference of the posted population; the build is this service's alone | Business Requirements Epics 3 to 8 v1 BR-054; FSD P8 A2.8.1; context pack ownership row `proceeds` |
| BR2 | The case position is rwb-case's; the asset position, its holding age and its provision step are rwb-asset's; both are read on the owners' contracts and neither as a table | DP-01; context pack P8 ownership rows; Architecture v5 slide 4 (S5 rwb-asset) |
| BR3 | The receipts of the business date and the ACE batch status arrive on the rwb-source-data contract; this service reads no `v_ace_*` view and no ACE table | DP-05; Architecture v5 slide 29; GAP-2564; ASM-4230 |
| BR4 | The provision step, its thresholds, its re-appraisal interval and the period of the input are rule rows and policy parameters read at their version, never constants, defaults or branches of the build | BR-P8-008; Business Requirements Epics 3 to 8 v1 ASM-012 and Q-005; GAP-2563; ASM-4229 |
| BR5 | The decision is recorded before the input set is answered, one record per build, with the rule IDs, the version in force and the built amounts; a failed write changes nothing and shows MSG-P7-003 | DP-03; legacy RWB-E6-036 AC2; FSD P8 A2.8.4.3; R-UNI-39 |
| BR6 | The build runs only on a complete ACE batch of source `ALS`; no input is built from a stale data product | FSD P8 A2.8.4.4; VR-P8-008-1 |
| BR7 | One input row per case and business date: a repeated business date, a redelivered event or a repeated request answers once, records once and counts the repeat | R-UNI-40; GAP-2565; ASM-4231 |
| BR8 | No provision-input row is persisted in `rwb_payment`: the input set is the step's answer, and its delivery to Finance is the unpublished finance-feed path | GAP-2565; ASM-4231 |
| BR9 | The release of the provision and the write-off, asset and debt-sale route states that precede the feed are the route services' and are not moved here | R-WO-25, R-WO-26, R-DIS-09, R-DS-31 of the Business Rules and Routing Logic v4 |
| BR10 | The accounting entries, the posting references and the posting file are not this step's: the posting reference is read from `proceeds` once FEAT-PAY-07 writes it | FSD P8 A2.8.2 (ALS and GL); TSD P8 T3.1 (DF-FIN-009) |
| BR11 | No person name, address, contact value or identity number enters a record, the input set, a log or a workflow input | Template and Rules v1 s17; Architecture v5 slide 42 notes |
| BR12 | A build that cannot record, cannot read a position or cannot find a rule row answers nothing and holds; the cause is corrected in rwb-decision or at the contract owner, never in this build | FSD P8 A2.8.4.3; R-UNI-39 and R-UNI-41 |

The row BR-P8-008 is the row of FSD P8 A2.8.3.1, copied character for character; VR-P8-008-1 keeps that rule and its message, with its read moved to rwb-source-data (GAP-2564); the rest are the rules the target split fixes. R-UNI-39 and R-UNI-41 are copies of the Business Rules and Routing Logic v4: a decision log that cannot be written blocks the action and raises an incident, and a person who decides names the missing data.

### 9. State transitions

None of the case. The case states are rwb-case's, and the write-off, asset and debt-sale route states that precede the feed — `POSTED` to `PROVISION_RELEASED` to `FINANCE_FEED_SENT` under R-WO-25 and R-WO-26 — are S7's and are named here only as the context the input set serves. What this story owns is the execution state of the step and the status of the input set it answers.

| Step execution | Event | Condition | To |
|---|---|---|---|
| Waiting | `AceDataReady` for business date D | The inbox row is written | Reading |
| Reading | The batch status and the receipts answer fresh | The rule rows in force answer | Building |
| Building | The case position and the asset position answer | Every case in scope carries a position | Recording |
| Recording | The decision record is written | The library commits | Answered |
| Answered | The input set of D is returned | The build-once key is written | Waiting for the next business date |
| Reading | The data product is stale (X3) | VR-P8-008-1 | Held, until a fresh answer |
| Any | The record cannot be written (X1) | The library refuses | Unchanged, nothing answered, MSG-P7-003 and an incident |
| Any | No rule row is in force (X5) | The period cannot be derived | Held, nothing answered, reported to rwb-decision |

| Input set status | Event | Condition | To |
|---|---|---|---|
| Not existing | The build of D commits | The record is written | Built, with its rule IDs and version; the status values are Not specified in the source documents (GAP-2563; ASM-4229) |
| Built | The same case and business date again (X6) | The stored answer is returned | Built, no second record, the repeat counted |
| Built | A position contract fails after the build | The set is superseded by the next business date | Built, unchanged, no partial set answered |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-FINANCE, Finance and CFO delegate | Write-off and posting RA: reads the position the input set is built from and accepts the provision input of a case (TSD P8 T6.1; FSD P8 A2.8.3.3, "also uses") |
| RW-CREDITAD, Credit Administration officer | Write-off and posting CRUA: reads the same position and may approve and update where the family allows it |
| RW-WRITEOFF, write-off team member | Write-off and posting CRU: reads the same position for the posted population |
| RW-PRODHEAD, RW-WOCOMM | Write-off and posting RA: read and approve within the matrix |
| RW-FRAUD, RW-DEBTSALE, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE and the 34 roles of the legacy permission table | Write-off and posting R and the case-record right R the legacy table names: read only, in scope, through SCR-28 |
| SY-CASEWF, SY-RULES, SY-AGENT | Write-off and posting R: the service identities run inside the same checks as a person |
| rwb-payment service identity | Runs the build step under "None; runs unattended", reads the four contracts, writes the decision record and answers the input set; it holds no grant on another schema and no `v_ace_*` grant |

The rights are the rows of TSD P8 T6.1 and of the legacy permission table of this key, and nothing wider. DP-08 is not in this story's pattern set: the right is declared by the contract and checked by the guard of the service template, so it is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3) | `id`, `case_no`, `product_group`, `primary_person_key`, `status`, `stage_code` and 17 more | Read on the rwb-case contract only, never as a table |
| DF-ACE-043 to DF-ACE-054 | `v_ace_payment` (P1) | `payment_code`, `account_key`, `payment_date`, `payment_amount`, `payment_channel`, `capital_amount` and 6 more | Not read: this service holds no `v_ace_*` grant; the receipts arrive on the rwb-source-data contract (BR3) |
| DF-ACE-208 to DF-ACE-219 | `v_ace_npa_asset` (P1) / held-asset position (S5) | `asset_ref`, `asset_key`, `asset_code`, `transfer_in_type`, `from_segment`, `book_value` and 6 more | Not read as a table: the asset position arrives on the rwb-asset contract (BR2) |
| DF-FIN-001 to DF-FIN-009 | proceeds (P8, `rwb_payment`) | `id`, `case_id`, `treatment_id`, `account_payment_id`, `source`, `amount`, `received_date`, `matched_to`, `posting_ref` | Read: the matched receipts of the case and the posting reference the FEAT-PAY-07 stories wrote; no row is written here |
| DF-DEC-001 to DF-DEC-018 | decision record (PLT library, created in `rwb_payment`) | `case_id`, `decision_code`, `rule_id`, `rule_version`, `model_version` and the inputs reference and answer | Write through the local library, one per build, before the input set is answered |
| DF-REF-001 to DF-REF-015 | rule_row (P7) | `id`, `rule_id`, `rule_version`, `route_set`, `from_state`, `event_code` and 9 more | Not read as a table: the rule rows arrive with the package read of rwb-decision, at their version (BR4) |
| Not specified in the source documents (DOR-RWB-P8-E6036-APP-7) | provision input (no owner published) | The input row of a case: its case and product group, its position amounts, its asset position and provision step, its receipts and posting reference, its rule ID and version | Built as the step's answer, not persisted (GAP-2565; ASM-4231) |

Field IDs are those of TSD P8 T3.1 and of the legacy data table of RWB-E6-036, with their owners changed by the target. **No new table, no new column and no migration**: `proceeds` arrives with the DB story of this service, and `decision_record`, `outbox_event`, `processed_event` and `idempotency_key` are platform library objects created in `rwb_payment` by the library's own migration (DP-03, DP-09). The field list of the provision input, its period and the provision step values are Not specified in the source documents (GAP-2563; ASM-4229) and stay rule rows, policy parameters or the answer shape of this step, never columns invented here.

**No personal data.** The rows this story reads and the answer it builds carry identifiers, codes, amounts, dates and a rule version. No name, address, contact value or identity number enters `rwb_payment`, the decision record, the input set, a log or a workflow input, and the fixture data of the tests is synthetic.

### 12. Contract

#### 12.1 REST operations provided

None. The legacy feature declares no endpoint ("Endpoints: None. The work runs as a service or a scheduled job inside the recovery module"), and the two operations of this service, `GET /proceeds` (API-P8-001) and `POST /proceeds/{proceedsId}/match` (API-P8-002) on base `/api/recovery/payment/v1`, are declared by the contract baseline of RWB-P8-E4049-CON and built by the Epic 4 stories. This story adds no operation, no path and no resource, and the provision input is the answer of the build step, not a REST resource.

#### 12.2 REST operations consumed

| Operation | Base / contract | Owner | Use |
|---|---|---|---|
| The case position of a case (operation name Not specified in the source documents (GAP-2563; ASM-4229)) | `/api/recovery/case/v1` | P3 rwb-case | the case reference, product group, status and stage, the balance components and the open treatments; faked |
| The held-asset position of a case (operation name Not specified in the source documents (GAP-2564; ASM-4230)) | `/api/recovery/asset/v1` | S5 rwb-asset | the asset reference, book value, date taken in, holding age and provision step in force; faked |
| The receipts of the business date and the batch status of source `ALS` (operation names Not specified in the source documents (GAP-2564; ASM-4230)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | payment_code, account_key, payment_date, payment_amount and the freshness stamp; source_system, business_date and status of the batch; faked |
| The provision-input rule rows and the version in force (operation name Not specified in the source documents (GAP-2563; ASM-4229)) | `/api/recovery/decision/v1` | P7 rwb-decision | the rule IDs of the family, the provision step, its thresholds, the re-appraisal interval and the period of the input, at the version in force; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C that the plan does not carry, because the C row of this slice is None, so this story builds against their published documents and fakes on Day 1 (GAP-2563, GAP-2564; ASM-4229, ASM-4230).

#### 12.3 Events published

None. This service owns three events, `TreatmentBooked` (EV-11), `PaymentMissed` (EV-12) and `ProceedsMatched` (EV-25), and the provision input is not one of them; no event carries it and none is declared by this story. `DecisionRecorded` (EV-08) is written by the local library of DP-03 to this service's outbox and relayed on the shared topic `rwb.decision-record.v1`, whose owner is rwb-decision; it is a platform row and not an event of this service.

#### 12.4 Events consumed

| Event | Topic | Consumer group | Payload used | When |
|---|---|---|---|---|
| `AceDataReady` (EV-26) | `rwb.source-data.events.v1`, with its `.retry` and `.dlt` topics | `rwb-payment.provision-inputs.v1` | the source `ALS`, the business date and the batch status; CloudEvents envelope; deduped in the inbox on the event id | On the outbox relay of rwb-source-data; starts the build for the business date |
| `RulePackageInForce` (EV-30) | `rwb.decision.events.v1` | `rwb-payment.provision-inputs.v1` | the package code and the version in force, so the build reads its rule rows at the released version; deduped in the inbox | On the outbox relay of rwb-decision, and at every step start from the package read |

Owner of each event: `AceDataReady` is published by rwb-source-data and `RulePackageInForce` by rwb-decision; the consumer is rwb-payment.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| The ACE-batch-started run of the service (name Not specified in the source documents (GAP-2563; ASM-4229)) | Workflow, one execution per business date and source, started by `AceDataReady` | `rwb-payment` in namespace `rwb-recovery` | input: the business date, the source and the package in force; signals: `AceDataReady`, `RulePackageInForce`; the build is one stage of it |
| The provision-input build step (activity name Not specified in the source documents (GAP-2563; ASM-4229)) | Activity | `rwb-payment` | the four contract answers in; the rule IDs with their version, the record and the input set of the business date out, in one transaction |

`matchPayments` (JOB-07) and `confirmBookings` (JOB-08) are the two jobs the context pack assigns to this service and belong to the matching and booking stories; this story neither renames them nor claims them. No source names the run or the step of FEAT-PAY-08, and the placeholder is carried as GAP-2563 with ASM-4229 rather than invented.

#### 12.6 Schedules

None. The trigger is the completed ACE batch of source `ALS` and not a Temporal Schedule, a Quartz row or a shared job table (FSD P8 A2.8.4.4; Architecture v5 slide 44). The month-end close window of the finance feed is a policy timer of the write-off route (R-WO-26) and not a Schedule of this story, and the outbox relay runs as a library component in every service.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| proceeds | P8 (`rwb_payment`) | Read only here: the matched receipts of the case and the posting reference of DF-FIN-009 written by the FEAT-PAY-07 stories |
| decision_record | PLT library, created in `rwb_payment` | The local hash-linked decision record, one per build (DP-03) |
| outbox_event | PLT library, created in `rwb_payment` | The `DecisionRecorded` row of the same transaction (DP-03) |
| processed_event | PLT library, created in `rwb_payment` | The inbox row of each consumed event and its dedupe key (DP-09) |
| idempotency_key | PLT library, created in `rwb_payment` | The build-once key of the case and business date and the answer it holds |
| provision input | Not created | No source publishes a table for it in `rwb_payment` or any other schema; the input set is the step's answer (GAP-2565; ASM-4231) |

Not owned and never read as a table: `recovery_case`, `case_account`, `assignment`, `task`, `timer` and the case balance (P3), the held-asset position, `asset` and the provision step (S5), `decision_log_entry`, `rule_row` and `payment_match_rule` (P7), the `v_ace_*` views (P1), the write-off, sale and placement rows (S6, S7) and the fee and booking tables of this service. No foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case position fake | Case `RC-2026-000555` of product group MORTGAGE with its balance components and open treatments, a case with no open treatment, and an unknown case reference | AC1, X4 |
| rwb-asset position fake | Held asset `AST-2026-000555` with book value 3,200,000.00 THB, its date taken in, its holding age and the provision step in force; a case with no held asset; a position that does not answer in 2 s | AC1, X4 |
| rwb-source-data receipt and batch fake | The receipts of business date 2026-12-31 for source `ALS` with the freshness stamp, a stale product with its date, and an empty batch | AC1, X3 |
| rwb-decision package fake | The provision-input rule rows at the version in force with the provision step, its thresholds and the period; a package without the rows | AC1, X5 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and outbox, and a stopped chain | AC2, X1 |
| `AceDataReady` event fake | The `ALS` business date 2026-12-31, the same event twice, and an event for a failed batch | AC1, X6 |
| gateway-bff composite route fake | The merged SCR-28 answer for the case, with the position of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-case, rwb-asset, rwb-source-data and rwb-decision reads are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2563, GAP-2564; ASM-4229, ASM-4230).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 4 consumed | the rwb-case position read, the rwb-asset position read, the rwb-source-data receipt and batch read and the rwb-decision rule read; one hop, 2 s |
| Kafka | 0 published, 2 consumed | `AceDataReady` and `RulePackageInForce` in consumer group `rwb-payment.provision-inputs.v1`; the decision record is relayed by the library on `rwb.decision-record.v1` |
| Temporal | 1 run and 1 step | the ACE-batch-started run of the service and its provision-input build step on `rwb-payment`; no Schedule, no Quartz row |
| File | None | no file is laid out, built or delivered here; the finance feed and its transport are published nowhere (GAP-2565; ASM-4231) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.payment`, module `provision`, Java package `th.co.scb.ace.workbench.recovery.payment.provision`; front end `src/modules/recovery/payment/ProceedsMatching.tsx`, the fragment SCR-28 embeds, read only.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies only as a prohibition: rwb-payment holds no `v_ace_*` grant, because only rwb-source-data has SELECT on the views (Architecture v5 slide 29), so the receipts and the batch status arrive on the owner's contract and the legacy reads of `v_ace_payment` and `v_ace_npa_asset` are retired (GAP-2564; ASM-4230). DP-03 is the transaction rule of the step: the record, the answer and the build-once key commit together or not at all. DP-19 is how SCR-28 reaches this service, one hop through the gateway; this story adds no screen field and no route.

**Dependencies the tables add and the plan does not hold.** The pattern table adds the two H rows the plan already carries, and the plan carries no other H row. The four consumed rows of 12.2 are contract dependencies of class C that the plan's C row does not list, because that row is None, so they are built against their documents and fakes on Day 1 (GAP-2563, GAP-2564; ASM-4229, ASM-4230). This story applies no DP-04, DP-06, DP-07, DP-10 or DP-15: it evaluates no Drools of its own, reads no parameter and no list, registers no Schedule and opens no migration.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| The provision-input stage of the run (name placeholder) | Workflow stage | Waits for the business date and reports the input set to its caller |
| `ProvisionInputStep` (name placeholder) | Activity | the one step: read the four answers, assemble the input rows, write the record and answer the set |
| `ProvisionEventConsumer` | Inbox adapter | Consumes `AceDataReady` and `RulePackageInForce` in group `rwb-payment.provision-inputs.v1`, writes the `processed_event` row and dedupes |
| `ProvisionInputAssembler` | Service | Builds one input row per case and business date from the positions, the receipts and the rule rows, and invents no field and no threshold |
| `PaymentDecisionRecordWriter` | Library adapter | Writes one decision record per build before the answer, hash-linked, and refuses the step when the write fails (DP-03) |
| `CasePositionClient`, `AssetPositionClient`, `PaymentFactClient`, `RulePackageClient` | Clients | The four consumed reads of 12.2, one hop each, 2 s, breaker, and the freshness stamp of the receipt read |
| `ProvisionInputStore` | Library adapter | The build-once key of the case and business date and the stored answer (DP-09) |

**Database and migrations.** No Flyway file of this story. `proceeds` arrives with the DB story of this service, and the decision record, the outbox, the inbox and the idempotency key are library objects created in `rwb_payment` by the library's migration (DP-03, DP-09). No table and no column is added for the provision input, its period or its status (GAP-2565; ASM-4231). The schemas `rwb_case`, `rwb_asset`, `rwb_source_data` and `rwb_decision` are owned by their services; they are named here only as the boundary this build does not write.

**Configuration and reference data.**

- The provision-input rule rows and their version, authored, tested and approved in rwb-decision (P7) and loaded on `RulePackageInForce`; the provision step, its thresholds, the re-appraisal interval and the period of the input are values of those rows and not of this build (BR4).
- Reference data read: the rule rows of the package in force, read through `RulePackageClient` on the rwb-decision contract at their version; the parameters are Not specified in the source documents (DOR-RWB-P8-E6036-APP-20; GAP-2563; ASM-4229). The reference-data contract is named in the source documents and is not applied by this build.
- The capability area "Write-off and posting" and its rights R, A and U are access rows of rwb-access, read through the guard.
- The consumer group `rwb-payment.provision-inputs.v1` and its two subscriptions are configuration of the inbox library.
- The 2 s budget and the single hop are the platform rule of ADR-020; no other parameter is named in the sources for this step (GAP-2563; ASM-4229).

**Build steps**

1. The provision-input stage and its input record, registered on `rwb-payment`, with `AceDataReady` as its trigger (AC1).
2. `ProvisionEventConsumer` and the inbox row, with the duplicate and redelivery paths (AC1, X6).
3. `PaymentFactClient`, `CasePositionClient`, `AssetPositionClient` and `RulePackageClient` against their fakes, with the 2 s budget, the breaker, the stale-data path and the no-answer path (AC1, X3, X4).
4. `ProvisionInputAssembler` over the positions, the receipts and the rule rows, with the no-row path and the empty-asset path (AC1, X5).
5. `PaymentDecisionRecordWriter` against the library stub, with the failed-write path (AC2, X1).
6. `ProvisionInputStore` with the build-once key and the stored answer (AC1, X6).
7. The answer of the input set with its rule IDs and version, and its repeat (AC1).
8. The boundary test: no statement outside `rwb_payment`, no `v_ace_*` read, no write to `rwb_case`, `rwb_asset`, `rwb_source_data` or `rwb_decision`, and no Schedule (X7, BR2, BR3).

**Feature flag.** `rwb.payment.provision-inputs-v1`, read as a flag of the platform library; off means the consumer writes the inbox row and holds the business date, builds no input set and writes no record, and the sibling stories are unaffected.

**Screen states of SCR-28 for this step.** The no-access state is MSG-P4-002 of section 14, and the position is not read. The empty and error states are Not specified in the source documents (DOR-RWB-P8-E6036-APP-10); the loading state stays that of the receipts list.

**Done when.** The tests of section 16 pass, the step runs from a synthetic `AceDataReady` in SIT, one input row per case and business date is answered with the rule IDs and the version in force, a case with no rule row stays held, a repeated business date answers once, a forced record failure changes nothing, and no `v_ace_*` read and no foreign row write exists in the build.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required field of the build is absent or invalid, or a position answer breaks its invariant | Enter {field}. |
| MSG-P4-002 | A role without the Write-off and posting right reads the position on SCR-28 | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the input set is answered | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product of source `ALS` is stale after a late or failed batch (VR-P8-008-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The four message IDs are those of the legacy message set of this key and of FSD P8 A2.8.3.1, and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-P7-003 is the message of legacy AC2 and of FSD AC-EXC-P8-008-02, and MSG-P4-002 is the message of TC-E6-036-03 and of FSD AC-EXC-P8-008-01.

### 15. Screens and states

SCR-28 Proceeds matching is served through the gateway-bff composite route (DP-19). The legacy story names that screen with its three states, loading, matched and unmatched; the FSD keeps the same screen for the family and the feature itself names no screen of its own. This story therefore fixes no screen field and adds no state: the finance delegate reads the case and asset position the input set is built from on SCR-28, and the loading, matched and unmatched states stay those of the receipts list. The empty and error states of SCR-28 are Not specified in the source documents (CG-ALL-7797) and are not added; the no-access state is MSG-P4-002.

The states this step produces are the step states of section 9 and the status of the input set; where a build holds, the screen shows the same refused state with MSG-P4-002, not-recorded state with MSG-P7-003 and stale-data state with MSG-P1-001 as the family. The composite route specification and the screen field list belong to RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-036-01 | AC1, BR1, BR4, BR6, BR7, BR8, BR11 | Component | Case `RC-2026-000555` of product group MORTGAGE, held asset `AST-2026-000555` of book value 3,200,000.00 THB, the receipts of business date 2026-12-31 and the provision-input rule rows at their version; the input row, the rule IDs and version, the decision record and the build-once key asserted on the fakes |
| TC-E6-036-02 | AC2, BR5, BR12 | NFR | The decision-record stub stopped; nothing built, nothing answered, MSG-P7-003 shown and an incident opened |
| TC-E6-036-03 | Access, AC4 | Contract | A role without the Write-off and posting right R; 403 with MSG-P4-002 and no read of a position |
| TC-E6-036-04 | Principle 5, BR5, BR7 | NFR | A forced decision-record write failure at the moment of the build; no input row, no answer, and the repeat answers once when the library recovers |
| TC-E6-036-05 | AC3, X7, BR2, BR3, BR9, BR10 | Component | Statements of the build against the tables of section 12.7 and the schemas of section 13; a statement outside `rwb_payment`, a `v_ace_*` read or a write to `rwb_case`, `rwb_asset`, `rwb_source_data` or `rwb_decision` fails the build |
| TC-E6-036-06 | AC5, BR5, BR7, BR11 | Component | Case `RC-2026-000555` of product group MORTGAGE built twice for business date 2026-12-31; the decision record written before the answer, the stored input set returned, and no person data in the record asserted on the fakes |
| TC-E6-036-07 | AC6, X6, BR7 | Component | AceDataReady of source `ALS` for business date 2026-12-31 delivered twice; one processed-event row, one record and one input row asserted on the fakes |
| TC-E6-036-08 | AC7 | Component | Not specified in the source documents (NEWAC-RWB-P8-E6036-APP-AC7) |
| TC-E6-036-09 | AC8 | Component | Not specified in the source documents (NEWAC-RWB-P8-E6036-APP-AC8) |
| TC-E6-036-10 | AC9 | Component | Not specified in the source documents (NEWAC-RWB-P8-E6036-APP-AC9) |

The first four test cases are the legacy cases of RWB-E6-036 in their legacy order, with the Level column added (TC-E6-036-05 to TC-E6-036-10 are added for AC3 and AC5 to AC9, new, D-RCV-60): TC-E6-036-01 is the component proof of the step on its fakes, the two forced-failure cases map to NFR because they prove the no-side-effect property of the transaction, and the access case maps to Contract because the artefact under test is the declared right. The legacy rows name no case, amount, product group or date, which is recorded as GAP-2562 with ASM-4228; the full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID, and the `-ITG` copies belong to the wave 4 harness.

### 17. Guardrails

- No business value in code: the provision step, its thresholds, its re-appraisal interval, the period of the input and the rule IDs stay rule rows of rwb-decision at their version, never a constant, a default or a branch of the build.
- No personal data in `rwb_payment`, in the input set, in a workflow input or in a log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract or a `v_ace_*` view this service holds: it holds none, because only rwb-source-data has SELECT on the views, so the receipts and the batch status arrive on P1's contract and a build that adds a view or an ACE table read fails the boundary test (DP-05; Architecture v5 slide 29).
- The case position is rwb-case's and the asset position is rwb-asset's: no `recovery_case`, `case_account`, `asset`, holding-age or provision-step row is written here, and neither owner's state is moved here (BR2).
- One base, one topic, one queue and one login per service: `/api/recovery/payment/v1`, `rwb.payment.events.v1`, `rwb-payment` and the `rwb_payment` login, and no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- The decision is recorded before the answer and every consumed event is deduped in the inbox; a build that answers a set before its record, or that answers twice for one business date, fails the review (DP-03, DP-09, R-UNI-40).
- No new table and no new event: the provision input is an answer and this service publishes none of its three events from this step.
- No retired element is reintroduced: no shared Quartz table, no Quartz job, no monolith API base, no `recovery` schema read, and no data-lake copy of the input set.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| No requirement id for this slice | The split plan carries no requirement id for this slice; the requirement is FEAT-PAY-08 of FSD P8 A2.8 and its main success criterion AC-P8-008-01, that the provision inputs Finance needs are built from the case and asset positions and the result is recorded with its rule version (GAP-2562; ASM-4228) | The build step, the input row, the decision record and the rule version | TC-E6-036-01, TC-E6-036-02 |
| BR-054 (Business Requirements Epics 3 to 8 v1) | An approved write-off posts, the provision is released, completeness is published, and the provision inputs reach Finance from the posted population; the row names REQ-S7-005, FEAT-WOF-09, FEAT-WOF-10, FEAT-PAY-08 and RWB-E6-036 | The build from the posted population and the rule version on every record | TC-E6-036-01 |
| BR-P8-008 | No value a business person may change is written in code; it is read from reference data with its version (FSD P8 A2.8.3.1) | The rule rows, the provision step and the period read at their version | TC-E6-036-01 |
| VR-P8-008-1 | Data product stale after a late or failed ACE batch raises MSG-P1-001 (FSD P8 A2.8.3.1) | The freshness check of the receipt and batch read | TC-E6-036-01 |
| ADR-013 | 19 services inside ACE | rwb-payment as the owner of the build and rwb-asset and rwb-case as the owners of the positions | TC-E6-036-01 |
| ADR-014 | Schema and login per service | `rwb_payment` and its own login, no cross-schema read or write | TC-E6-036-04 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The inbox of the two consumed events and the library's outbox row | TC-E6-036-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-E6-036-01 |
| ADR-022 | Local decision record plus central ledger | The record written before the input set is answered | TC-E6-036-02, TC-E6-036-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-036, disposition Split (rework) |
| Legacy criteria | AC1 and AC2, owned word for word by this story |
| Test cases | TC-E6-036-01 to TC-E6-036-04 |
| Feature and screens | FEAT-PAY-08 Produce provision inputs; SCR-28 Proceeds matching |
| Rules | VR-P8-008-1 and BR-P8-008 (FSD P8 A2.8.3.1), the provision-input rule rows governed in rwb-decision, and R-UNI-39 and R-UNI-41 of the Business Rules and Routing Logic v4; the provision step thresholds, the re-appraisal interval and the period are not published (GAP-2563; ASM-4229) |
| Decoupling patterns | DP03, DP05, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022 |
| L3 process | Not specified in the source documents (DOR-RWB-P8-E6036-APP-2) |

### 19. Out of scope

- The published shapes, the field list and the fakes of the provision input, if a CON story of this legacy key is added: no such story is in the plan, and the field list is held as GAP-2563 with ASM-4229.
- The delivery of the input set to Finance, the finance provision feed, its file layout, its interface number, its transport and its acknowledgement: no source publishes them (GAP-2565; ASM-4231).
- The case of record, its states, its balances, `assignment`, `task`, `timer` and the parent `CaseWorkflow`: rwb-case (P3).
- The held-asset position, its holding age, the provision step application, the re-appraisal order, the sale and the floor price: rwb-asset (S5) under R-DIS-06 and R-DIS-09.
- The write-off release of the provision, the tax file, the write-off scan and the committee pack (S7 under BR-054, R-WO-25 to R-WO-27) and the debt-sale posting with its provision input (S6 under R-DS-31).
- The accounting entries, the posting references, the posting file and the deed in lieu rental: the FEAT-PAY-07 and FEAT-PAY-09 stories of this service.
- The ACE receipt, asset and batch-status facts and the freshness of the data product: rwb-source-data (P1).
- The provision-input rule rows, their thresholds, their period and their release: rwb-decision (P7).
- The roles, scopes and masking behind the Write-off and posting right (rwb-access and the guard of the service template) and the gateway-bff composite route with the screen field list of SCR-28 (RWB-PLT-N001-CON and the edge stories).
- The cross-service journey of the legacy key and its evidence: the wave 4 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.

Change log: D-RCV-60 (realignment v1), 22 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Change log: D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P8-E6036-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

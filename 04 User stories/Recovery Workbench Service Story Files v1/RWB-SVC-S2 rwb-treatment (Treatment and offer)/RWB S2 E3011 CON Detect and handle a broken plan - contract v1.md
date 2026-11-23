# RWB-S2-E3011-CON Detect and handle a broken plan - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E3-011 split out for rwb-treatment. The document publishes the `PlanBreak` element recorded against the treatment, the read rule of the payment view and the batch date it is read at, the break-count and break-limit rule, the stage report that returns the case to the route decision, the decision-record group, the versioning rule and the fakes. It declares no REST operation of its own on base `/api/recovery/treatment/v1`, because the element is a component of the treatment representation published by RWB-S2-E3001-CON (DP-13); the payment evidence is read through the service's own SELECT-only views under DP-05; the screen path is the gateway-bff composite route (DP-19). It is published on Day 1 at status Draft (realignment v1). No source gives the break count a field or the break limit a governed row (GAP-2668; ASM-4383), publishes the event a broken plan is said to raise (GAP-2669; ASM-4384), says where the plan status is held after the split (GAP-2670; ASM-4385) or names the payment window and the cure-period set (GAP-2671; ASM-4386). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3011-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **contract owner of rwb-treatment**, I want **the published contract of the break step — the `PlanBreak` element recorded against the treatment, the read rule of the payment view with the batch date and the no-copy rule, the break-count and break-limit rule, the stage report that returns the case to the route decision with its reason and its owner task, the decision-record group, the versioning rule and the fakes — instead of the monolith's method reading `rule_row` and the `recovery` schema in one process**, so that **the application story of this feature, the sibling plan stories of this service and the wave 2 integration harness build and test on Day 1 without a P1, P7 or rwb-case deployment and without a production ACE view, and no reader of a broken plan depends on a count that was never defined**.

This is the contract slice of legacy RWB-E3-011. It owns:

- the `PlanBreak` element: the break count, the break limit, the payment evidence and its as-at date, the reason code `broken_plan`, the break date, the rule ID and the rule version, with the rule that it is recorded against the treatment and against nothing else;
- the read rule of the payment evidence: the view `recovery.v_ace_payment` and the batch status view, the columns consumed, the batch date, the cure window the evidence is tested over, and the rule that nothing is copied (DP-05);
- the break-count and break-limit rule: how the count is composed from the case's own treatment rows, that `max_breaks` is the value of the rule row in force, and the four answers R-RES-29, R-RES-30, R-RES-31 and R-RES-36 (GAP-2668; ASM-4383);
- the stage report: the outcome and the reason `broken_plan` reported to the parent `CaseWorkflow`, the case statuses the parent applies, and the 5 working day owner task of R-RES-30 that this document orders but does not create (GAP-2670; ASM-4385);
- the decision-record group of the same transaction, named as the local record of RWB-PLT-E1027-CON, with its refusal and failure messages;
- the guard answers — MSG-P1-001 for a stale data product, MSG-GEN-001 for a missing count and MSG-GEN-006 for a view that does not answer — the compatibility and pinning rule, the fakes and the drift test that hold the document and the code together.

It does not own: the break branch of `TreatmentWorkflow`, the detection activity, the two reads, the mark, the record call and the tests against them, which are RWB-S2-E3011-APP; the treatment representation and its read operation, which are RWB-S2-E3001-CON and RWB-S2-E3001-APP; the cure period and the plan timers, which are RWB-S2-E3010-CON and RWB-S2-E3010-APP; the four legacy acceptance criteria of RWB-E3-011, which are carried verbatim by RWB-S2-E3011-APP; the case status, the case task and the case timer, which are rwb-case's; the ACE view and its grants, which are ACE's; the RESTRUCTURE rule rows, their approval and the central ledger, which are P7 rwb-decision's; the payment matching that finds a missed installment, which is P8 rwb-payment's; and SCR-14 and its composite route, which are the platform edge story's under DP-19.

### 2. Business rationale

In the monolith the break step had no contract at all. `TdrSettlementAndDeedInLieuService` read the payments from the `recovery` schema, read the threshold row from `rule_row`, decided in code and wrote the outcome into `treatment` and `decision_log_entry` (TSD S2 T2 and T3.1). Nothing about that arrangement could be reused or tested alone: the threshold was a row any module could read, the payment evidence was a copy or a live join, and a broken plan had no shape — a reader of it had one option, which was to read the module's tables.

D-RCV-60 replaces three inputs and one output, and the contract is where each of them is written down. The payment stays in ACE and is read at the batch date from the service's own SELECT-only view (DP-05; D-RCV-35, ADR-010). The break limit becomes a value of the rule row in force, read with the version that decided (R-RES-30, R-RES-31). The decision becomes a local record in the same transaction (DP-03; ADR-022). And the output becomes an element with a field list, a required flag on each field, a version label and a set of fakes, recorded against the treatment the officer already sees.

Two of the four things this contract must fix are absences rather than decisions. The break count has no column in the Logical Data Model and no row in TSD S2 T3.1, so the contract states how it is composed — from the case's own treatment rows whose outcome is `BROKEN`, and from the count the case signal carries — and refuses to invent a column (GAP-2668; ASM-4383). And REQ-S2-009 says a broken plan "raises an event" while the ownership rows give this service one event, EV-10, and the plan gives the story no event-platform dependency; the contract therefore fixes the stage report to the parent as the event of the step and leaves a Kafka event to the gap (GAP-2669; ASM-4384).

The legacy key divides cleanly and the division is fixed. This WP delivers the **contract**. The **application** — the branch, the activity, the reads, the mark and the guard paths — is **RWB-S2-E3011-APP**, and the **four legacy acceptance criteria stay with it**: AC1 to AC4 are listed in its section 7 with their origin tag and are not repeated here. The **cross-service proof** is **RWB-ITG-W2**. Every criterion in section 7 of this document is new and tests only the contract deliverable in this title.

### 3. Preconditions

- The rules whose states, events and condition terms the element carries are fixed by the Routing Logic v4: R-RES-29 (`PLAN_CURE_PERIOD`, `CURE_PERIOD_EXPIRED`, "no payment and cure_period passed", to `PLAN_BROKEN`), R-RES-30 (`PLAN_BROKEN`, `BREAK_RECORDED`, `break_count < max_breaks`, reason `broken_plan`, 5 working days), R-RES-31 (`break_count >= max_breaks`, to `RESTRUCTURE_BARRED`) and R-RES-36 (`break_count` missing or not a number, to `UNMATCHED_EXCEPTION`). The names are copied into the element and the report, character for character.
- The fields the mark lands on exist in TSD S2 T3.1: `outcome` (DF-TRT-013, varchar(12), LOV-TRT-OUTCOME, value `BROKEN`) and `outcome_at` (DF-TRT-014, timestamptz).
- The payment evidence is fixed in kind: FSD A2.11.3.1 VR-S2-011-1 reads `v_ace_batch_status` for the data-product date, and the legacy data table names `v_ace_payment` with DF-ACE-043 to DF-ACE-054; the columns consumed and the grant path are the working read of ASM-4362 (GAP-2654).
- The decision record is the platform library's: `DecisionRecordWriter.record(DecisionRecord)` with `@Transactional(propagation = MANDATORY)`, refusing with MSG-P7-009 and failing with MSG-P7-003 (DP-03; RWB-PLT-E1027-CON).
- The element is served to SCR-14 through the gateway-bff composite route (DP-19; RWB-PLT-N001-CON), so the contract fixes the element, not a route.
- No source publishes the element's own field list, the break-limit row, the payment window or a broken-plan event (GAP-2668 to GAP-2671; ASM-4383 to ASM-4386). The document is published as that working read, at major version 1 and status Draft (realignment v1).
- No build dependency and no approval stop: a CON story is Day 1 by rule (§R5.7) and nothing in this story needs a human sign-off to start (ASM-4387).

### 4. Flow

1. The contract author fixes the `PlanBreak` element: its eight fields, which are required, and the rule that it is recorded against the treatment.
2. The author fixes the read rule of the payment evidence: the two views, the columns consumed, the batch date, the cure window and the ban on copying.
3. The author fixes the break-count and break-limit rule: the composition of the count, `max_breaks` as a value of the rule row, and the four answers with their to states.
4. The author fixes the stage report: the outcome and reason reported to the parent, the case statuses the parent applies and the 5 working day owner task, with the boundary stated — no case row, no case task, no case timer is written here.
5. The author writes the guard answers — MSG-P1-001, MSG-GEN-001 and MSG-GEN-006 — and the decision-record group with the two library messages.
6. The author writes the versioning and pinning rule: what may change inside major version 1 and what raises version 2.
7. The fake set and the drift fixture are generated from the document, and the contract test runs them against it on every change.
8. The document and the fakes are published at v1; RWB-S2-E3011-APP and RWB-ITG-W2 pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A published element drops a required field, or adds an optional one a consumer depends on | The schema check fails the build; required and optional fields are as published | None | AC1 |
| X2 | The read rule is published without the batch date, the column list or the cure window, or allows a copy | The read lint and the no-copy check fail the build | None | AC2 |
| X3 | The break-count rule is published with a fixed limit, or without the composition of the count | The rule lint fails the build; the limit is named, never fixed | None | AC3 |
| X4 | The stage report is published as a case write, or without the reason or the owner task | The boundary check fails the build; the report carries the reason and the task and writes no case row | None | AC4 |
| X5 | The failure answers are published as exceptions or as a silent no-op | The lint fails the build; a stale product is MSG-P1-001, a missing count is MSG-GEN-001 and a view that does not answer is MSG-GEN-006 | MSG-P1-001; MSG-GEN-001; MSG-GEN-006 | AC3 |
| X6 | A breaking change is made to the element, the read rule or a guard answer | The change raises major version 2; v1 is never edited in place and stays readable | None | AC5 |
| X7 | A consuming story ships without the drift test, or a fake stops answering the document | The drift test fails the build of the consuming story | None | AC6 |
| X8 | A value a consumer needs is named by no source — the break-count field, the limit row, the payment window or the event | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-2668; ASM-4383) | Section 3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document and fakes; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | Field order, record widths and the fixture set are open until v1 is frozen; the element, the two views, the count rule, the report and the guards are fixed |
| Valuable | Unblocks the application story and the wave 2 harness on Day 1, and gives the sibling plan stories one definition of a broken plan |
| Estimable | One element, one read rule, one count rule, one report, one versioning rule and five fakes |
| Small | One sprint for the document, the fakes and the drift test |
| Testable | Each criterion below is one schema, rule-lint or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: broken-plan contract of rwb-treatment

  Background:
    Given the contract document is published with major version 1 on the base of rwb-treatment
    Given the element is a component of the treatment representation and the contract declares no REST path of its own
    Given the break limit is the max_breaks value of the rule row in force and the payment evidence is read from recovery.v_ace_payment

  Scenario: AC1 The PlanBreak element and its required fields are published (new, D-RCV-60)
    Given the element section of the contract document
    When it is validated and linted
    Then it publishes PlanBreak with breakCount, breakLimit, paymentsFound, paymentsAsAt, reasonCode, brokenAt, ruleId and ruleVersion
    Then breakCount, breakLimit, paymentsFound, paymentsAsAt, reasonCode and brokenAt are required and ruleId and ruleVersion are optional
    Then reasonCode carries the value broken_plan of R-RES-30 and the element maps brokenAt to DF-TRT-014 and the mark to DF-TRT-013
    Then the element is recorded against the treatment and against no other record, and it has no collection, no free-text field and no payment detail
    Then a document that drops a required field fails the schema check

  Scenario: AC2 The payment read rule, the batch date and the cure window are fixed (new, D-RCV-60)
    Given the read rule section of the contract document
    When it is linted against the views and the platform rules
    Then it names recovery.v_ace_payment and recovery.v_ace_batch_status as the only ACE objects read, with the columns consumed and the SELECT-only grant
    Then the payments are read at the ACE batch date and paymentsAsAt carries that date, while the cure window of the plan decides which payments count
    Then a data product older than today's ACE batch is answered with MSG-P1-001 naming the product and its date
    Then a read that does not answer is answered with MSG-GEN-006 and never with a guessed evidence
    Then a rule that reads a third ACE object, keeps a copy or names a payment table of rwb-payment fails the lint

  Scenario: AC3 The break-count rule, the limit and the guard answers are fixed (new, D-RCV-60)
    Given the count and guard sections of the contract document
    When they are linted against the routing logic and the library contract
    Then the count is composed from the case's own treatment rows whose outcome is BROKEN and from the count the case signal carries, and no break-count column is declared for rwb_treatment
    Then breakLimit is the max_breaks value of the rule row in force, read with its version, and no limit is fixed as a number in the document or the code
    Then break_count < max_breaks answers R-RES-30, break_count >= max_breaks answers R-RES-31 and a count that is missing or not a number answers R-RES-36 with MSG-GEN-001
    Then the mark and the record are written in one transaction; a refused record names its field with MSG-P7-009 and a failed one stops the action with MSG-P7-003

  Scenario: AC4 The stage report and the case boundary are fixed (new, D-RCV-60)
    Given the report section of the contract document
    When it is linted against the case boundary and the routing logic
    Then the report carries the outcome, the reason broken_plan, the break count and the break limit to the parent CaseWorkflow and orders the 5 working day owner task of R-RES-30
    Then the document states that PLAN_BROKEN, BACK_TO_ROUTE_DECISION, RESTRUCTURE_BARRED and UNMATCHED_EXCEPTION are case statuses applied by rwb-case and never written by this service
    Then the document states that no case row, case task and case timer is created by the consumer and that plan_status and plan_status_as_of are read on the case signal only
    Then the document publishes no Kafka event, records the reason the event of REQ-S2-009 is a stage report, and names the event gap and its assumption

  Scenario: AC5 Versioning separates a compatible change from a new major version (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published field or rule
    Then a backward-compatible change keeps major version 1
    Then a breaking change to the element, the count rule, the report or a guard answer raises major version 2, and v1 is never edited in place
    Then RWB-S2-E3011-APP and RWB-ITG-W2 pin a published version and raise a change request rather than a private variant

  Scenario: AC6 The fakes answer the document and the drift test holds (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the element fake, the view fixture, the case-signal fake, the record fake and the drift fixture
    Then the view fixture answers no payment in the cure window, a payment inside it and an unreachable view
    Then the element fake answers the element of AC1 and one variant per missing required field
    Then the case-signal fake answers a count below, at and above the limit and a count that is missing
    Then the drift test fails the build of a consuming story on any difference from sections 12 and 13
```

These criteria are new and test only the contract deliverable. No legacy acceptance criterion is repeated here: **AC1 to AC4 of RWB-E3-011 are carried by RWB-S2-E3011-APP**. Every identifier used above comes from the legacy story, the Routing Logic v4, TSD S2 or the FSD, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The element recorded against the treatment carries the break count, the break limit, the payment evidence with its as-at date, the reason code `broken_plan`, the break date and the rule versions, and nothing else | RWB-E3-011 AC1 to AC3; DF-TRT-013; DF-TRT-014; ASM-4383 |
| BR2 | The reason code is `broken_plan` of R-RES-30 and the states are `PLAN_CURE_PERIOD`, `PLAN_BROKEN`, `BACK_TO_ROUTE_DECISION`, `RESTRUCTURE_BARRED` and `UNMATCHED_EXCEPTION` of the routing logic; no name is renamed by the element | R-RES-29; R-RES-30; R-RES-31; R-RES-36 |
| BR3 | The count is composed from the case's own treatment rows whose outcome is `BROKEN` and from the count the case signal carries; no break-count column is declared | GAP-2668; ASM-4383; LOV-TRT-OUTCOME |
| BR4 | The limit is the `max_breaks` value of the rule row in force, read with its version, and is never fixed as a number in the document or in code | R-RES-30; R-RES-31; BR-S2-011 |
| BR5 | The payments are read at the ACE batch date from `recovery.v_ace_payment` and `recovery.v_ace_batch_status` only, read only, and are never copied into `rwb_treatment` | DP-05; VR-S2-011-1; D-RCV-35; ADR-010 |
| BR6 | A data product older than today's ACE batch is answered with MSG-P1-001, a missing count with MSG-GEN-001 and a view that does not answer with MSG-GEN-006; none of them is an exception a consumer has to guess | VR-S2-011-1; R-RES-36; FSD A2.11.3.1 |
| BR7 | The mark and the element are written with the local decision record in one transaction, through `DecisionRecordWriter` with `MANDATORY` propagation | DP-03; ADR-022; RWB-PLT-E1027-CON |
| BR8 | The case status, the case task and the case timer stay rwb-case's: the report carries the outcome, the reason and the task due date, and the parent applies the rule | DP-01; R-RES-30; ASM-4385 |
| BR9 | A published version is never edited: a compatible change stays in major version 1 and a breaking change raises major version 2 | Template and Rules §R7.2; §R5.4 class C |

### 9. State transitions

None of the case statuses are this contract's, and a document has no runtime state of its own. The table fixes the outcomes the contract names so that a consumer cannot invent a fifth.

| Object | State | Meaning in the contract |
|---|---|---|
| Break step | Answered | The views answered inside their budgets and the element was written with its record |
| Break step | No break | A payment inside the cure window was found; the clear is R-RES-28's and nothing is written here |
| Break step | Blocked, stale product | A data product is older than today's ACE batch; MSG-P1-001, nothing written |
| Break step | Blocked, missing count | The count is missing or not a number; MSG-GEN-001, nothing written, a case owner task |
| Break step | Blocked, no answer | A view did not answer; MSG-GEN-006, nothing written |
| Break step | Rolled back | The record could not be written; no mark, no element, MSG-P7-003 |
| Element | Recorded / Absent | Written against the treatment in the same transaction, or not written at all; there is no partial element |
| Contract version | v1 / v2 | v1 is the published version every consumer pins; v2 is raised by a breaking change and v1 stays readable |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document and the fakes |
| The service owner of rwb-treatment | Approves a breaking change and freezes a version |
| The owner of P7 rwb-decision | Confirms the RESTRUCTURE rows that carry `max_breaks` and the condition terms the element names, at the wave 2 contract freeze (ASM-4383) |
| The owner of P3 rwb-case | Confirms the case statuses the report triggers, the 5 working day owner task of R-RES-30 and the case plan fields DF-CAS-046 to DF-CAS-048 (ASM-4385) |
| ACE and its DBA | Confirm the two views, the columns consumed and the SELECT-only grant to this service's login (ASM-4362) |
| The platform data and workflow owners | Confirm the decision-record library, the task queue and the retry policy |
| RW-CASEOWN, case owner | Works the returned case and its task; holds rights C, R and U on the capability area; the step itself runs unattended under the service identity |
| RW-RESTRUCT, restructuring officer (FCR) | Consumes the element through SCR-14 and holds rights C, R and U |
| The consumer stories of this service | Consume the element, pin the version and raise a change request rather than a private variant |
| RW-AUDIT, RW-COE | Read the recorded element and the decision records; they do not consume this document directly |
| No delegation of authority level applies | A contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in the document, an example or a fake; where an actor must be named, a role code or a service identity is used.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The document publishes field names, the condition terms `cure_period`, `break_count` and `max_breaks`, the reason code and the messages; no customer, account or case value appears |
| Element published | The eight fields of section 12.1, with the required and optional flags and the two treatment columns they map to |
| Personal data | None. The element carries a count, a limit, a date, a count of payments, a reason code and versions; no name, national identifier, account number, payment amount or document content |
| Tables published | None. The consumer writes the element and the mark against `treatment` in `rwb_treatment`; `decision_record` is the platform library object |
| Field identifiers | DF-TRT-013 and DF-TRT-014 for the mark; the element's own identifiers are Not specified in the source documents (GAP-2668; ASM-4383) |
| Retention | The element is kept with the treatment row for the life of the case record; the retention period of the element is Not specified in the source documents (GAP-2668; ASM-4383) |

### 12. Contract

#### 12.1 REST operations provided

None of its own. The element and the mark are components of the treatment representation that RWB-S2-E3001-CON publishes on `GET /api/recovery/treatment/v1/treatments/{treatmentId}` (API-S2-002 of TSD S2 T-A.1), and this contract fixes the component, not the path (DP-13). SCR-14 reaches it through the gateway-bff composite route (DP-19).

**Element: `PlanBreak`**

| Field | Type | Required | Maps to | Note |
|---|---|---|---|---|
| `breakCount` | integer | Yes | No treatment column | The count of breaks the case has carried, composed from its treatment rows and the case signal |
| `breakLimit` | integer | Yes | No treatment column | The `max_breaks` value of the rule row in force; never fixed |
| `paymentsFound` | integer | Yes | No treatment column | The payments of the plan found inside the cure window at the batch date; zero for R-RES-29 |
| `paymentsAsAt` | date | Yes | No treatment column | The ACE batch date the payments were read at |
| `reasonCode` | string | Yes | No treatment column | `broken_plan` for R-RES-30; the code of the answered row otherwise |
| `brokenAt` | timestamptz | Yes | DF-TRT-014 `outcome_at` | The business time the plan was marked broken |
| `ruleId` | string | No | No treatment column | The RESTRUCTURE row that answered, R-RES-29 to R-RES-31 or R-RES-36 |
| `ruleVersion` | string | No | The version group of the decision record | The version of the package or route set in force |

The element is recorded against the `treatment` row and against no other record; it has no collection, no free-text field and no payment detail, because the evidence is a count and a date, not the payments themselves. The mark itself is `treatment.outcome = BROKEN` (DF-TRT-013, LOV-TRT-OUTCOME) with `outcome_at` (DF-TRT-014). The element's own BR Field IDs have no row in the Logical Data Model, so the field names are the working read of ASM-4383 (GAP-2668); the reason code, the state names and the limit keep the names the routing logic already uses.

#### 12.2 REST operations consumed

None. The contract declares no REST read: the case status, the break count and the plan reference arrive on the signal the parent `CaseWorkflow` forwards, the rule rows arrive on the package event of 12.4, and the payment evidence is the SQL read of 12.5. The plan rows that would have been read from a P1 contract are read as views under DP-05. No source publishes an operation for this step, and the contract names the elements rather than an invented path (GAP-2668; ASM-4383).

#### 12.3 Events published

None. This contract owns no topic and publishes no event; the service's topic `rwb.treatment.events.v1` and its event EV-10 `rwb.treatment.TreatmentApproved.v1` belong to the offer story of this service (DP-14; TSD S2 T5.3). REQ-S2-009 says a broken plan "raises an event": the contract fixes that event as the `BREAK_RECORDED` stage report to the parent `CaseWorkflow`, a Temporal signal inside the case, and states that a Kafka event would need the event platform of DP-09, which the plan does not give this legacy key; the name, the schema and the consumers of such an event are the open gap (GAP-2669; ASM-4384).

#### 12.4 Events consumed

None by this contract. The consumer's package and route set arrive on `rwb.decision.RulePackageInForce.v1` from P7 (EV-30), which is the application story's subscription and the service template's rule loader; the contract only requires that the element and the record name the version that was in force. `rwb.payment.PaymentMissed.v1` (EV-12) is the service's other input and opens the cure period at R-RES-27; it belongs to the payment-missed branch of RWB-S2-E3010-APP and this contract only fixes the field it carries, `treatmentId`.

#### 12.5 Workflows and activities

None of its own: the contract defines no workflow, no activity and no task queue. What it fixes is the two reads the consumer's activity makes, the count it composes and the report it sends, so that both sides of each read are written down in one place.

| Read element | Value |
|---|---|
| ACE read | SQL, SELECT-only, on `recovery.v_ace_payment` and `recovery.v_ace_batch_status`, in the ACE database, at the ACE batch date |
| ACE columns | `payment_code`, `account_key`, `payment_date`, `payment_amount`, `payment_channel`, `capital_amount` and the rest of DF-ACE-043 to DF-ACE-054, and the product date of the batch status |
| ACE rule | No copy is kept; no third ACE object is read; no write of any kind; no payment table of rwb-payment is named |
| Count rule | Composed from the case's own treatment rows whose outcome is `BROKEN` and from the count the case signal carries |
| Limit rule | `max_breaks` of the rule row in force, with its version; never a constant |
| Report | The outcome, the reason `broken_plan`, the count, the limit and the 5 working day owner task, to the parent `CaseWorkflow` |
| On a stale product | MSG-P1-001 naming the product and its date; nothing decided |
| On a missing count | MSG-GEN-001 with the field; nothing decided, a case owner task |
| On no answer | MSG-GEN-006; nothing decided |

The column list, the grant path, the composition of the count and the payment window are the working read of ASM-4383 and ASM-4386, because no source document states them: the FSD names `v_ace_batch_status` in a validation rule, the legacy data table names `v_ace_payment` with a field range, the routing logic states the condition in words, and the Work Package records no contract dependency on P1 (GAP-2668, GAP-2671). The owners confirm all of them at the wave 2 contract freeze.

#### 12.6 Schedules

None. The contract declares no Schedule: the step is entered on the cure-period expiry of the plan and reports the 5 working day task of R-RES-30, and neither is a scheduled scan of this service. The ownership rows give S2 no job, and the legacy Quartz scheduler is retired.

#### 12.7 Tables owned

None. The element and the mark are written by the consumer against `treatment` in `rwb_treatment`, a table of this service created on its own Flyway sequence, and `decision_record` is the platform library object of DP-03 applied in the same schema. The contract creates no table, declares no column and adds no foreign key: there is deliberately no break-count column, and `decision_log_entry` is P7's ledger in `rwb_decision`, named only and never written or read here.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Element fake | The `PlanBreak` shape | A complete element; one element per missing required field; an element with and without `ruleId` and `ruleVersion` |
| ACE view fixture | The two views | No payment in the cure window; a payment inside it; a partial payment; a product dated yesterday; an unreachable view |
| Case-signal fake | The forwarded case signal | `PLAN_CURE_PERIOD` with a count; a count that is missing; `PLAN_BROKEN` with a count below, at and above the limit |
| Output fake | The guard answers | MSG-P1-001 with the product and its date, MSG-GEN-001 with the field, MSG-GEN-006 for no answer |
| Decision-record fake | The record group of AC3 | An accepted record with the rule and set versions; a refusal with MSG-P7-009 and the field; a failure with MSG-P7-003 |
| Drift fixture | The contract test | One accepted and one refused body per section of the document |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consuming story rather than as a surprise at run time. The view fixture and the case-signal fake are what make Day 1 possible for RWB-S2-E3011-APP and RWB-ITG-W2.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 0 | The element rides the treatment representation; no operation is declared |
| Kafka | 0 | 0 | The consumer's package subscription is the application story's; no topic is declared here |
| Temporal | 0 | 0 | The contract fixes no workflow; it fixes the reads, the count and the report of the consumer's activity |
| SQL view | 0 | 2 (`recovery.v_ace_payment`, `recovery.v_ace_batch_status`) | SELECT only, at the batch date, no copy |
| File | 0 | 0 | No file crosses the contract |

### 13. Solution plan

**Package.** Contract artefact of rwb-treatment: the element and the report types in `th.co.scb.ace.workbench.recovery.treatment.api`, the fakes as a test resource, and the versioning rule in the contract document. The implementation that performs the reads, composes the count and writes the mark is RWB-S2-E3011-APP. The artefact coordinates and the publication channel are Not specified in the source documents (GAP-2668; ASM-4383).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is taken as the service's own SELECT-only views, as the Work Package records no contract dependency on P1 and the conflict with Architecture v5 slide 8 is recorded in GAP-2654. DP-13 fixes the base this contract declares nothing on; DP-03 is the record of the mark and DP-19 the path the mark is read on.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `PlanBreak` | Published type | The eight fields, the required and optional flags and the recording rule (BR1, BR2) |
| `PaymentReadRule` | Document | The two views, the columns, the batch date, the cure window and the no-copy ban (BR5, AC2) |
| `BreakCountRule` | Document | The composition of the count, `max_breaks` as a rule value and the four answers (BR3, BR4, AC3) |
| `BreakReport` | Published type | The outcome, the reason, the count, the limit and the owner task, and the case boundary (BR8, AC4) |
| `GuardAnswers` | Document | MSG-P1-001, MSG-GEN-001, MSG-GEN-006 and the record messages (BR6) |
| `VersioningSpecification` | Document | Major version 1, the compatible versus breaking rule and the pinning rule (AC5) |
| Fake set and drift fixture | Test asset | The element, view, case-signal, output and record fakes and the drift test (AC6) |

**Database.** No table and no column in this contract. The mark lands in `treatment.outcome` (DF-TRT-013) and `treatment.outcome_at` (DF-TRT-014), both TSD S2 T3.1 fields; the break count, the limit and the payment count have no column and no field ID, which is why they exist only in the element (GAP-2668; ASM-4383).

**Configuration and reference data.** The limit, the cure window and the four rule rows are data of rwb-decision with a version and are named here, never fixed. The 2 s budget and the retry policy are the activity's and the workflow kit's. The capability area and the rights are access data of P4 and are not declared by this document.

**Build steps**

1. Write the element with its eight fields and the required and optional flags; validate it against the schema check (AC1).
2. Write the payment read rule with the two views, the columns, the batch date, the cure window and the no-copy ban (AC2).
3. Write the break-count rule, the limit rule and the four answers with their to states and their messages (AC3).
4. Write the stage report and the case boundary, and lint them against rwb-case's statuses and the routing logic (AC4).
5. Write the guard answers and the record group, and lint them against the library contract (AC3).
6. Write the versioning and pinning section with the compatible and breaking examples (AC5).
7. Generate the fake set and the drift fixture, and wire the drift test into the build of RWB-S2-E3011-APP (AC6).
8. Publish v1 and record the pinned versions of RWB-S2-E3011-APP and RWB-ITG-W2.

**Feature flag.** `rwb.treatment.plan-break-contract`.

**Done when.** The document and the schema validate, the read and count lints, the no-copy check and the case-boundary check are green, the fakes answer every criterion including the stale product, the missing count and the unreachable view, the drift test fails on an edited field and passes on the published version, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P1-001 | A data product is older than today's ACE batch | {product} is from {date}. Today's ACE batch has not arrived. | The stale-product answer of the read rule; the product named is the one the step read |
| MSG-GEN-001 | The break count is missing or not a number | Enter {field}. | The missing-count answer of R-RES-36 |
| MSG-GEN-006 | A view does not answer | {system} is not available. Your request is queued and will be retried. | The no-answer answer of the read rule |
| MSG-P7-009 | A record is refused for a missing or invalid field | The decision record was refused: {field} is missing or not valid. | The library's refusal, named by the record group |
| MSG-P7-003 | The record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The library's failure, named by the record group |

The five texts are copied unchanged from the legacy story, FSD S2 A2.11.3.1 and RWB-PLT-E1027-CON, and this contract adds no message ID. MSG-P4-002 is the access guard's message and is named in the report boundary rather than published here. MSG-S2-001, MSG-S2-002 and MSG-S2-003 belong to the offer, the stale payoff and the offer expiry and are not published here. Thai text follows decision DL10.

### 15. Screens and states

No screen in this story, and the contract declares none. The element and the mark are shown on SCR-14 Treatment record, which is reached through the gateway-bff composite route (DP-19) and whose field list belongs to the platform edge story and the screen owner. The contract fixes what that screen may show of the break step: the outcome, its date, the break count against the limit, the reason `broken_plan` and the rule version, and no payment detail beyond the count and its as-at date. The screen's `broken` state is the one this element makes visible.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S2-E3011-CON-01 | AC1 | Contract | The element schema: the eight fields, the required and optional flags, the mapping to DF-TRT-013 and DF-TRT-014, the `broken_plan` code; one element per missing required field refused |
| TC-S2-E3011-CON-02 | AC2 | Contract | The read rule linted: the two views, the columns, the batch date, the cure window and the no-copy rule; a rule with a third ACE object, a copy or a rwb-payment table refused |
| TC-S2-E3011-CON-03 | AC3 | Contract | The count rule linted: the composition, `max_breaks` as a rule value, the four answers and their messages; a fixed limit refused |
| TC-S2-E3011-CON-04 | AC4 | Component | The report and the boundary: the reason, the count, the limit, the 5 working day task; a case write, a case task or a case timer refused |
| TC-S2-E3011-CON-05 | AC5, AC6 | Component | A compatible and a breaking change on the element and the rules; the fake set and the drift fixture on a consuming story, green on the published version and red on an edited field |

The legacy test set of RWB-E3-011 — TC-E3-011-01 to TC-E3-011-06 — is carried by RWB-S2-E3011-APP and by the wave 2 integration harness, and no legacy id is renumbered here. These five are the contract's own tests.

### 17. Guardrails

- No business value in the contract: the limit and the cure window are named, never fixed as numbers, and the mark lands on TSD S2 T3.1 fields (BR4).
- No personal data in the element, a read, an answer, a fake or a log: the element carries a count, a limit, a date, a payment count, a reason code and versions only, never a payment amount or an account number.
- No copy of ACE data: no payment or balance column is declared, and the consumer keeps no copy (BR5).
- No REST surface, no topic and no table of the contract's own: the base is fixed by DP-13 and the element rides the treatment representation.
- No second source for the limit and no third ACE object: one rule row and two views.
- The outcome of a stale input, a missing count or a dead view is a written answer, never an exception a consumer has to guess.
- A published version is never edited in place: a breaking change raises major version 2 and a consumer pins rather than forks.
- The case status is never the contract's: the mark is recorded, the report is sent and rwb-case moves the status (BR8).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-009 | A broken plan raises an event and returns the case to a decision rather than leaving it in a plan state | Business Requirements Program, section 5.9; FSD S2 requirements | FEAT-TRT-11 | 05 Restructure; 07 Route, settle and claim | R-RES-29; R-RES-30; R-RES-31; R-RES-36 | TC-S2-E3011-CON-01 to TC-S2-E3011-CON-05 |
| Legacy test set RWB-E3-011 | TC-E3-011-01 to TC-E3-011-06 | Business Requirements Program, section 5.9 | FEAT-TRT-11 | 05 Restructure; 07 Route, settle and claim | R-RES-29; R-RES-30 | Executed by RWB-S2-E3011-APP and the wave 2 integration harness; not owned here |

REQ-S2-009 is the one requirement whose text names this behaviour, so the trace runs on it; TSD S2 T8 maps the same ID to FEAT-TRT-01, which is the module's "written one epic ahead" placeholder, and the feature code is carried alongside until the C1 PRD settles the mapping.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3011-APP | App development | H consumer: implements the branch, the activity, the two reads, the mark and the report against this contract and its fakes; owner of the four legacy acceptance criteria |
| RWB-PLT-E1027-CON | Contract | Referred to: the local decision-record library and its two messages. This contract adds no build dependency of its own |
| RWB-PLT-N001-CON | Contract | Referred to: the gateway-bff composite route that shows the element on SCR-14 |
| RWB-S2-E3001-CON | Contract | Sibling: the treatment representation that carries this element on its read |
| RWB-S2-E3010-CON | Contract | Sibling: the booking contract whose schedule the cure period runs on |
| P3 rwb-case | Service | The case statuses, the case tasks, the case timers and the case plan fields |
| P7 rwb-decision | Service | The RESTRUCTURE rows, their `max_breaks` value, their version and the central ledger |
| P8 rwb-payment | Service | The payment matching and EV-12, whose `treatmentId` this contract names |
| ACE and its DBA | External capability, existing | The two views, their columns and the SELECT grant (ASM-4362) |
| RWB-ITG-W2 | Integration | I: the cross-service proof of the read and the report against the live owners, and the owner of the legacy `-ITG` copies |

### 19. Out of scope

- The break branch of `TreatmentWorkflow`, the detection activity, the two reads, the count, the mark, the report and the tests against this contract: RWB-S2-E3011-APP.
- The four legacy acceptance criteria of RWB-E3-011, AC1 to AC4: carried verbatim by RWB-S2-E3011-APP; none is repeated or renumbered here.
- The treatment representation, its create and read operations and the treatment states: RWB-S2-E3001-CON and RWB-S2-E3001-APP.
- The plan booking, the schedule, the plan timers and the cure period: RWB-S2-E3010-CON and RWB-S2-E3010-APP.
- The case, its status, its tasks, its timers and the parent `CaseWorkflow`: rwb-case (P3); the contract declares no case read and no status write.
- The payment matching, the payment posting and `rwb.payment.PaymentMissed.v1`: P8 rwb-payment.
- The `recovery.v_ace_*` views, their columns, their grants and the ACE batch that dates them: ACE and its DBA (GAP-2654).
- The RESTRUCTURE rows, their authoring, approval, effective date, rollback and the central ledger: P7 rwb-decision; this contract names the version and the limit only.
- A Kafka event for a broken plan, its name, its schema and its consumers: not published by this contract; raised as GAP-2669 and ASM-4384.
- SCR-14, its field list and the gateway-bff composite route: the platform edge story and the screen owner (DP-19).
- The real cross-service proof of the read, the report and the screen against the live owners: RWB-ITG-W2, which also owns the `-ITG` copies of the legacy cases.

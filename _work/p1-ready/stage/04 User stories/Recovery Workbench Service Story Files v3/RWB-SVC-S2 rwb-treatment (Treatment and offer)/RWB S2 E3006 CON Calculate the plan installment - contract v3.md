# RWB-S2-E3006-CON Calculate the plan installment - contract

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E3-006 split out for rwb-treatment. The document publishes the `PlanInstallment` element recorded against the treatment, the reference-data consumption rule of the band, the floor and the freshness limit through the contract of rwb-case, the read rule of the two ACE views, the decision-record group, the versioning rule and the fakes. It declares no REST operation of its own on base `/api/recovery/treatment/v1`, because the element is a component of the treatment representation published by RWB-S2-E3001-CON (DP-13); it names the reference-data elements of DP-07, whose dependencies are H RWB-PLT-E1043-CON and C RWB-P3-E1043-CON and are carried by the consuming application story; it reads the ACE balance through the service's own views under DP-05; the screen path is the gateway-bff composite route (DP-19). It is published on Day 1 at status Draft (realignment v1). No source fixes the element's field list or the reference set that holds the band (GAP-2651, GAP-2652; ASM-4359, ASM-4360), settles the ACE view grant (GAP-2654; ASM-4362) or names the trigger (GAP-2656; ASM-4364). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 11 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3006-CON |
| Readiness decisions | RD-P1-004 |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-S2-E3006-CON-14) |
| Size | Not specified in the source documents (DOR-RWB-S2-E3006-CON-16) |
| Contract version | Not specified in the source documents (DOR-RWB-S2-E3006-CON-23) |
| Patterns applied | DP03, DP05, DP07, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs; trace runs on feature code FEAT-TRT-06 until a requirement ID is allocated, GAP-2653) |
| Status | Draft (directive resolutions) |

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register). Aligned the quoted English to Error and Message Standard v6.


### 1. Story

As a **contract owner of rwb-treatment**, I want **the published contract of the plan-installment calculation — the `PlanInstallment` element that is recorded against the treatment, the reference-data elements it consumes from rwb-case with their version, the two ACE views it reads and at which date, the rule that nothing is copied, the decision-record group, the versioning rule and the fakes — instead of the monolith's method reading `rule_row` and the `recovery` schema in one process**, so that **the application story of this feature, the offer stories of this service and the wave 2 integration harness build and test on Day 1 without a P3 deployment and without a production ACE view, and no reader of the range depends on a shape that was never written down**.

This is the contract slice of legacy RWB-E3-006. It owns:

- the `PlanInstallment` element: the model installment, the installment count, the band bounds, the floor, the payoff with its as-at date, the reference-set version, the rule ID and the rule version, with the rule that it is recorded against the treatment and against nothing else;
- the reference-data consumption rule: which sets are read, what `settlement_range_low`, `settlement_range_high`, `floor_price` and the freshness limit mean, and that the set version is carried on the element (DP-07);
- the ACE read rule: the two views `recovery.v_ace_account` and `recovery.v_ace_batch_status`, the columns consumed, the batch date the balance is read at, and the rule that no balance is copied (DP-05);
- the two guards, on the data-product date with MSG-P1-001 and on the payoff date with MSG-S2-002, and the answer when a read does not reply, MSG-GEN-006;
- the decision-record group of the same transaction, named as the local record of RWB-PLT-E1027-CON, with its refusal and failure messages;
- the compatibility and pinning rule, the fakes and the drift test that hold the document and the code together.

It does not own: the branch of `TreatmentWorkflow`, the calculation activity, the two reads, the result repository and the tests against them, which are RWB-S2-E3006-APP; the affordability element and its Nexus binding, which are RWB-S2-E3005-CON; the treatment representation and its read operation, which are RWB-S2-E3001-CON and RWB-S2-E3001-APP; the offer inside the range and the below-floor approval, which are RWB-S2-E3002-APP, RWB-S2-E3003-APP and their contracts; AC2 of the legacy key and the R-SET-01 state step, which the Work Package does not assign to this legacy key's stories here; the case status, which is rwb-case's; the reference sets themselves and their values, which are rwb-case's (P3); the ACE views, their columns and their grants, which are ACE's; the rule package, which is P7 rwb-decision's; and the two screens and their composite route, which are the platform edge story's under DP-19.

### 2. Business rationale

In the monolith the calculation had no contract at all. `TdrSettlementAndDeedInLieuService` read the account from the `recovery` schema, read the threshold rows from `rule_row`, computed the numbers and wrote them into `treatment` and `decision_log_entry` (TSD S2 T2 and T3.1). Nothing about that arrangement could be reused or tested alone: the thresholds were rows of a table any module could read, the balance was a copy, and the answer had no shape — a reader of the range had one option, which was to read the module's tables.

D-RCV-60 replaces three inputs and one output, and the contract is where each of them is written down. The band, the floor and the freshness limit become reference rows of rwb-case behind a contract with a version (DP-07; the run's default ruling puts parameters and reference data in P3 rwb-case). The balance stays in ACE and is read at the batch date from the service's own SELECT-only views (DP-05; D-RCV-35, ADR-010). The decision becomes a local record in the same transaction (DP-03; ADR-022). And the output becomes an element with a field list, a required flag on each field, a version label and a set of fakes.

The legacy key divides cleanly and the division is fixed. This WP delivers the **contract**. The **application** — the workflow branch, the activity, the reads, the record and the guard paths — is **RWB-S2-E3006-APP**, and the **two legacy acceptance criteria stay with it**: AC1 and AC3 are listed in its section 7 with their origin tag and are not repeated here. AC2, the R-SET-01 state step, is not assigned to this legacy key's stories here. The **cross-service proof** is **RWB-ITG-W2**. Every criterion in section 7 of this document is new and tests only the contract deliverable in this title.

The contract has to unblock three things on Day 1. The element gives the offer stories, the treatment read and the integration harness one shape for the range, so the officer's band is defined once. The reference-data rule gives the consumer a fake instead of a P3 deployment. And the two guard answers — a stale data product and a stale payoff — are written outcomes rather than exceptions, which is the part of a calculation over governed data that is most often left unstated.

What the contract deliberately does not do: it copies no balance, declares no REST path of its own, owns no topic and no task queue, writes no table, and does not decide the case status. All four refusals are in section 12 and in section 19.

### 3. Preconditions

- The two rules whose field names the element carries are fixed by the Routing Logic v4: R-SET-01 (payoff from ALS and the range from reference data), R-SET-02 and R-SET-03 (`payoff_as_at` against the freshness limit) and R-SET-04 and R-SET-05 (`settlement_range_low`, `settlement_range_high`, `floor_price`). The names are copied into the element, character for character.
- The field names of the two plan numbers exist in TSD S2 T3.1: `installment_amount` (DF-TRT-031, numeric(18,2)), `installments` (DF-TRT-009, integer) and `interest_rate` (DF-TRT-027, numeric(7,4)).
- The ACE read is fixed in kind: FSD A2.6.3.1 VR-S2-006-1 reads `v_ace_batch_status` for the data-product date and the legacy data table names `v_ace_account` with DF-ACE-001 to DF-ACE-042; the columns consumed and the grant path are the working read of ASM-4362 (GAP-2654).
- Reference data is owned by P3 rwb-case by the run's default ruling; the contract names the reference-data elements of RWB-P3-E1043-CON and the client library of RWB-PLT-E1043-CON (DP-07). The Work Package records no contract dependency for this story, so the dependency sits on RWB-S2-E3006-APP, which performs the read.
- The decision record is the platform library's: `DecisionRecordWriter.record(DecisionRecord)` with `@Transactional(propagation = MANDATORY)`, refusing with MSG-P7-009 and failing with MSG-P7-003 (DP-03; RWB-PLT-E1027-CON).
- The element is served to the screens through the gateway-bff composite route (DP-19; RWB-PLT-N001-CON), so the contract fixes the element, not a route.
- No source publishes the element's own field list, the reference set that holds the band or the reference-data operation (GAP-2651, GAP-2652; ASM-4359, ASM-4360). The document is published as that working read, at major version 1 and status Draft (realignment v1).
- No build dependency and no approval stop: a CON story is Day 1 by rule (§R5.7) and nothing in this story needs a human sign-off to start.

### 4. Flow

The trigger of the plan-installment step is the case signal that the parent CaseWorkflow forwards to the stage; this contract publishes no Kafka subscription for it (GAP-2656; ASM-4364).

1. The contract author fixes the `PlanInstallment` element: its eleven fields, which are required, and the rule that it is recorded against the treatment. The field list is confirmed by the S2 rwb-treatment service owner at the wave 2 contract freeze (GAP-2651).
2. The author fixes the reference-data consumption rule: the four governed values, their meaning, the set version and the refusal when no set is in force. The reference set is read from rwb-case through RWB-P3-E1043-CON; its set identifiers and freshness limit are named when published (GAP-2652).
3. The author fixes the ACE read rule: the two views, the columns consumed, the batch date and the ban on copying. The two views are recovery.v_ace_account and recovery.v_ace_batch_status; SELECT on both for the rwb-treatment login is a condition of the wave 2 tag (GAP-2654).
4. The author writes the two guards: the data-product date with MSG-P1-001 and the payoff date with MSG-S2-002, plus the no-answer path with MSG-GEN-006.
5. The author writes the decision-record group and names the two library messages.
6. The author writes the versioning and pinning rule: what may change inside major version 1 and what raises version 2.
7. The fake set and the drift fixture are generated from the document, and the contract test runs them against it on every change.
8. The document and the fakes are published at v1; RWB-S2-E3006-APP and RWB-ITG-W2 pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A published element drops a required field, or adds an optional one a consumer depends on | The schema check fails the build; required and optional fields are as published | None | AC1 |
| X2 | The reference-data rule is published without the set identifiers, the version or the refusal | The rule lint fails the build; all four are required | None | AC2 |
| X3 | The ACE read rule is published without the batch date or the column list, or allows a copy | The read lint and the no-copy check fail the build | None | AC3, AC4 |
| X4 | The failure answer is published as an exception or as an empty range | The lint fails the build; a stale product is an answer with MSG-P1-001 and a no-answer is MSG-GEN-006 | MSG-P1-001; MSG-GEN-006 | AC3 |
| X5 | A breaking change is made to the element, the reference-data rule or a guard answer | The change raises major version 2; v1 is never edited in place and stays readable | None | AC5 |
| X6 | A consuming story ships without the drift test, or a fake stops answering the document | The drift test fails the build of the consuming story | None | AC6 |
| X7 | A value a consumer needs is named by no source — the set that holds the band, the reference operation or the payoff composition | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-2652; ASM-4360) | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document and fakes; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | Field order, record widths and the fixture set are open until v1 is frozen; the element, the four governed values, the two views, the guards and the no-copy rule are fixed |
| Valuable | Unblocks the application story and the wave 2 harness on Day 1, and gives the offer stories one definition of the range |
| Estimable | One element, one consumption rule, one read rule, two guards, one versioning rule and four fakes |
| Small | One sprint for the document, the fakes and the drift test |
| Testable | Each criterion below is one schema, rule-lint or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: plan-installment contract of rwb-treatment

  Background:
    Given the contract document is published with major version 1 on the base of rwb-treatment
    Given the element is a component of the treatment representation and the contract declares no REST path of its own
    Given the band, the floor and the freshness limit are reference rows of rwb-case read through RWB-P3-E1043-CON
    Given the element is written only by a step started by rwb-case or by an event of the service that owns the fact, and no schedule or batch trigger starts it

  Scenario: AC1 The PlanInstallment element and its required fields are published (new, D-RCV-60)
    Given the element section of the contract document
    When it is validated and linted
    Then it publishes PlanInstallment with installmentAmount, installmentCount, settlementRangeLow, settlementRangeHigh, floorPrice, payoffAmount, payoffAsAt, referenceSetVersion, ruleId and ruleVersion
    Then installmentAmount, installmentCount, settlementRangeLow, settlementRangeHigh, floorPrice, payoffAmount, payoffAsAt and referenceSetVersion are required and ruleId and ruleVersion are optional
    Then installmentAmount maps to DF-TRT-031 and installmentCount to DF-TRT-009, and the band and the floor keep the names settlement_range_low, settlement_range_high and floor_price of R-SET-04 and R-SET-05
    Then the element is recorded against the treatment and against no other record, and it has no collection and no free-text field
    Then a document that drops a required field fails the schema check

  Scenario: AC2 The reference-data consumption rule and its version are fixed (new, D-RCV-60)
    Given the reference-data section of the contract document
    When it is linted against the rwb-case contract and the client library
    Then it names the four governed values it reads, the set identifiers that hold them and the version carried on the element
    Then the read is one operation on base /api/recovery/case/v1, one hop, inside the 2 s budget of the client library, cached by set and version and never by time
    Then it declares no table read of rwb-case and no second source for the band or the floor
    Then when no set is in force the documented answer is MSG-GEN-006 and the step blocks
    Then a rule published without the set identifiers or the version fails the lint

  Scenario: AC3 The ACE read rule, the batch date and the two guards are fixed (new, D-RCV-60)
    Given the ACE read section of the contract document
    When it is linted against the views and the platform rules
    Then it names recovery.v_ace_account and recovery.v_ace_batch_status as the only ACE objects read, with the columns consumed and the SELECT-only grant
    Then the balance is read at the ACE batch date, payoffAsAt carries that date, and the figure is used only while its age is within the freshness limit of R-SET-03, which is Not specified in the source documents (ACR-RWB-S2-E3006-CON-AC3)
    Then a data product older than today's ACE batch is answered with MSG-P1-001 naming the product and its date, and a payoff older than the freshness limit with MSG-S2-002
    Then a read that does not answer is answered with MSG-GEN-006 and never with a guessed number
    Then a rule that reads a third ACE object or names a copy fails the lint

  Scenario: AC4 The no-copy rule and the decision-record group are fixed (new, D-RCV-60)
    Given the data rule and the record group of the contract document
    When the element and the schema are checked together
    Then no balance, band, floor or range column is declared for rwb_treatment, and rwb_treatment holds only the fields TSD S2 T3.1 already gives
    Then the element, the plan terms and the record are written in one transaction
    Then the record is the local record of RWB-PLT-E1027-CON, written with ruleId, ruleVersion and referenceSetVersion; a refused record names its field with MSG-P7-009 and a failed one stops the action with MSG-P7-003
    Then decision_log_entry is named only as P7's ledger and is never written or read by the consumer

  Scenario: AC5 Versioning separates a compatible change from a new major version (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published field or rule
    Then a backward-compatible change keeps major version 1
    Then a breaking change to the element, a governed value or a guard answer raises major version 2, and v1 is never edited in place
    Then RWB-S2-E3006-APP and RWB-ITG-W2 pin a published version and raise a change request rather than a private variant

  Scenario: AC6 The fakes answer the document and the drift test holds (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the reference-data fake, the view fixture, the element fake and the drift fixture
    Then the reference-data fake answers a set in force at a version, a set whose floor is above the band, and no set in force
    Then the view fixture answers a balance at today's batch date, a product dated yesterday and an unreachable view
    Then the element fake answers the element of AC1 and one variant per missing required field
    Then the drift test fails the build of a consuming story on any difference from sections 12 and 13

  Scenario: AC7 A value named by no source is published as the working read and the gap stays open (new, D-RCV-60)
    Given a value a consumer needs is named by no source
    When the contract document is validated and linted
    Then the value is published as the working read of the assumption and the gap stays open
    Then the value is written with its GAP and ASM identifiers and carries no fixed number

  Scenario: AC8 The contract fixes no business number and leaves the case status to rwb-case (new, D-RCV-60)
    Given the band, the floor, the freshness limit and the case status of the treatment
    When the contract document and the element are checked
    Then no business number is written as a fixed value for the band, the floor or the freshness limit
    Then the contract writes no case status, and the stage reports to the parent CaseWorkflow without writing a case row

  Scenario: AC9 The contract declares no REST operation and so answers no 401, 403 or 404 of its own (new, D-RCV-60)
    Given the contract declares no REST path of its own
    When the contract document is checked for provided operations
    Then it publishes no status code 401, 403 or 404 of its own
    Then the answers of the treatment operations are owned by RWB-S2-E3001-CON, which publishes the element as a component of the representation (DP-13)

  Scenario: AC10 A retried or timed-out activity is answered without a guessed value (new, D-RCV-60)
    Given a read of rwb-case is retried or runs past the 2 s budget of the client library, or an ACE view read is retried
    When the retry or the timeout ends without an answer
    Then the answer is MSG-GEN-006 and no value is written to the element
    Then the retry count and the ACE view timeout are Not specified in the source documents (NEWAC-RWB-S2-E3006-CON-AC10)
```

These criteria are new and test only the contract deliverable. No legacy acceptance criterion is repeated here: **AC1 and AC3 of RWB-E3-006 are carried by RWB-S2-E3006-APP**, and AC2 is not assigned to this legacy key's stories here (GAP-2657; ASM-4365). Every identifier used above comes from the legacy story, the Routing Logic v4, TSD S2 or the FSD, character for character.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The element recorded against the treatment carries the model installment, the count, the band, the floor, the payoff with its as-at date, the reference-set version, the rule ID and the rule version, and nothing else | RWB-E3-006 AC1; DF-TRT-009; DF-TRT-031; ASM-4359 | AC1; TC-S2-E3006-CON-01 |
| BR2 | The band and the floor are the values R-SET-04 and R-SET-05 name, `settlement_range_low`, `settlement_range_high` and `floor_price`, and their names are not renamed by the element | R-SET-04; R-SET-05; ASM-4360 | AC1; TC-S2-E3006-CON-01 |
| BR3 | The band, the floor and the freshness limit are governed rows of rwb-case read through RWB-P3-E1043-CON with the version in force, one hop inside the 2 s budget | DP-07; default ruling on parameters and reference data | AC2; TC-S2-E3006-CON-02 |
| BR4 | The balance is read at the ACE batch date from `recovery.v_ace_account` and `recovery.v_ace_batch_status` only, read only, and is never copied into `rwb_treatment` | DP-05; VR-S2-006-1; D-RCV-35; ADR-010 | AC3, AC4; TC-S2-E3006-CON-03, TC-S2-E3006-CON-04 |
| BR5 | A data product older than today's ACE batch is answered with MSG-P1-001; a payoff older than the freshness limit with MSG-S2-002; a read that does not answer with MSG-GEN-006 | VR-S2-006-1; R-SET-03; FSD A2.6.3.1 | AC3; TC-S2-E3006-CON-03 |
| BR6 | The element and the plan terms are written with the local decision record in one transaction, through `DecisionRecordWriter` with `MANDATORY` propagation | DP-03; ADR-022; RWB-PLT-E1027-CON | AC4; TC-S2-E3006-CON-04 |
| BR7 | A published version is never edited: a compatible change stays in major version 1 and a breaking change raises major version 2 | Template and Rules §R7.2; §R5.4 class C | AC5; TC-S2-E3006-CON-05 |
| BR8 | The case status stays rwb-case's: the contract fixes the element and the reads, and the stage reports to the parent `CaseWorkflow` without writing a case row | DP-01; ASM-4362 | AC8; TC-S2-E3006-CON-07 |
| BR9 | No value a business person may change is written into the contract as a number: the band, the floor and the freshness limit are named, never fixed | BR-S2-006 of FSD A2.6.3.1 | AC8; TC-S2-E3006-CON-07 |

### 9. State transitions

None of the case statuses are this contract's, and a document has no runtime state of its own. The table fixes the outcomes the contract names so that a consumer cannot invent a fifth.

| Object | State | Meaning in the contract |
|---|---|---|
| Calculation | Answered | The two reads answered inside their budgets and the element was written with its record |
| Calculation | Blocked, stale product | A data product is older than today's ACE batch; MSG-P1-001, nothing written |
| Calculation | Blocked, stale payoff | The payoff is older than the freshness limit; MSG-S2-002, nothing written |
| Calculation | Blocked, no set | No reference set is in force, or a read did not answer; MSG-GEN-006, nothing written |
| Calculation | Rolled back | The record could not be written; no element, no plan terms, MSG-P7-003 |
| Element | Recorded / Absent | Written against the treatment in the same transaction, or not written at all; there is no partial element |
| Contract version | v1 / v2 | v1 is the published version every consumer pins; v2 is raised by a breaking change and v1 stays readable |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document and the fakes |
| The service owner of rwb-treatment | Approves a breaking change and freezes a version |
| The owner of P3 rwb-case | Confirms the reference sets that hold the band, the floor and the freshness limit, and the operation that reads them at the wave 2 contract freeze (ASM-4360) |
| ACE and its DBA | Confirm the two views, the columns consumed and the SELECT-only grant to this service's login (ASM-4362) |
| The platform data and workflow owners | Confirm the client library, its cache rule and the 2 s budget |
| RW-RESTRUCT, restructuring officer (FCR) | Consumes the element through the screens and holds rights C, R and U on the capability area; the calculation itself runs unattended under the service identity |
| The consumer stories of this service | Consume the element, pin the version and raise a change request rather than a private variant |
| P7 rwb-decision | Owns the rule package and its version, which the element and the record name; the package codes are Not specified in the source documents (GAP-1707) and are named before wave 3 release |
| RW-AUDIT, RW-COE | Read the recorded element and the decision records; they do not consume this document directly |
| The rwb-access authorisation check of the screen path | Not specified in the source documents (DP-08); the contract declares no REST operation of its own |
| No delegation of authority level applies | A contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in the document, an example or a fake; where an actor must be named, a role code or a service identity is used.

### 11. Data

| Item | Value | BR Field ID |
|---|---|---|
| Business data published | None. The document publishes field names, the four governed values and the messages; no customer, account or case value appears | None |
| Element published | The ten fields of section 12.1, with the required and optional flags and the two treatment columns they map to | BR1; BR2 |
| Personal data | None. The element carries account keys, amounts, dates and versions; no name, national identifier, account number or document content | None |
| Tables published | None. The consumer writes the element against `treatment` in `rwb_treatment`; `decision_record` is the platform library object | BR6 |
| Field identifiers | DF-TRT-009 and DF-TRT-031 for the two plan numbers; the element's own identifiers are Not specified in the source documents (GAP-2651; ASM-4359) | BR2 |
| Retention | The element is kept with the treatment row for the life of the case record; the retention period of the element is Not specified in the source documents (GAP-2651; ASM-4359) | Not specified in the source documents (DOR-RWB-S2-E3006-CON-7) |

### 12. Contract

#### 12.1 REST operations provided

None of its own. The element is a component of the treatment representation that RWB-S2-E3001-CON publishes on `GET /api/recovery/treatment/v1/treatments/{treatmentId}` (API-S2-002 of TSD S2 T-A.1), and this contract fixes the component, not the path (DP-13). The two screens reach it through the gateway-bff composite route (DP-19).

**Element: `PlanInstallment`**

| Field | Type | Required | Maps to | Note |
|---|---|---|---|---|
| `installmentAmount` | numeric(18,2) | Yes | DF-TRT-031 `installment_amount` | The model installment of the plan |
| `installmentCount` | integer | Yes | DF-TRT-009 `installments` | The number of installments of the plan |
| `settlementRangeLow` | numeric(18,2) | Yes | No treatment column | The lower bound of the band; the name of R-SET-04 |
| `settlementRangeHigh` | numeric(18,2) | Yes | No treatment column | The upper bound of the band; the name of R-SET-04 |
| `floorPrice` | numeric(18,2) | Yes | No treatment column | The floor the offer is tested against below the band; the name of R-SET-05 |
| `payoffAmount` | numeric(18,2) | Yes | No treatment column | The ALS balance at the batch date; copied nowhere |
| `payoffAsAt` | date | Yes | No treatment column | The ACE batch date the balance was read at; the date R-SET-03 tests |
| `referenceSetVersion` | string | Yes | The version group of the decision record | The version of the reference sets in force when the calculation ran |
| `ruleId` | string | No | No treatment column | Present when the calculation reports a rule of its own |
| `ruleVersion` | string | No | The version group of the decision record | The version of the package or route set in force |

The element is recorded against the `treatment` row and against no other record; it has no collection and no free-text field. Its own BR Field IDs have no row in the Logical Data Model, so the field names are the working read of ASM-4359 (GAP-2651); the band, the floor and the payoff date keep the names the routing logic already uses.

#### 12.2 REST operations consumed

| Operation | Contract | Element | Owner | Budget |
|---|---|---|---|---|
| Reference-data read on base `/api/recovery/case/v1` | RWB-P3-E1043-CON | The reference sets holding `settlement_range_low`, `settlement_range_high`, `floor_price` and the freshness limit, each with its version | P3 rwb-case | One hop, 2 s, cached by set and version |

The operation and its path inside the rwb-case contract are not specified in the sources read here, so the contract names the contract and the elements rather than an invented path (GAP-2652; ASM-4360). The read goes through the client library of RWB-PLT-E1043-CON. The case status and the case facts are not consumed as REST reads by this contract at all, and the balance is not a REST read either: it is the SQL read of 12.5.

#### 12.3 Events published

None. This contract owns no topic and publishes no event; the service's topic `rwb.treatment.events.v1` and its event EV-10 `rwb.treatment.TreatmentApproved.v1` belong to the offer story of this service (DP-14; TSD S2 T5.3). The element is not announced on Kafka: it is recorded and read.

#### 12.4 Events consumed

None by this contract. The consumer's package and route set arrive on `rwb.decision.RulePackageInForce.v1` from P7 (EV-30), which is the application story's subscription and the service template's rule loader; the contract only requires that the record name the version that was in force.

#### 12.5 Workflows and activities

None of its own: the contract defines no workflow, no activity and no task queue. What it fixes is the two reads the consumer's activity makes and the guards around them, so that both sides of each read are written down in one place.

| Read element | Value |
|---|---|
| ACE read | SQL, SELECT-only, on `recovery.v_ace_account` and `recovery.v_ace_batch_status`, in the ACE database, at the ACE batch date |
| ACE columns | The account identifiers, `contract_no`, `product_category_efs` and `total_balance` of DF-ACE-001 to DF-ACE-042, and the product date of the batch status |
| ACE rule | No copy is kept; no third ACE object is read; no write of any kind |
| Reference read | REST, one operation on RWB-P3-E1043-CON through the client library of RWB-PLT-E1043-CON |
| Reference values | `settlement_range_low`, `settlement_range_high`, `floor_price` and the freshness limit, with the set version |
| Reference rule | One hop, 2 s, cached by set and version only, with MSG-GEN-006 when no set is in force |
| On a stale product | MSG-P1-001 naming the product and its date; nothing computed |
| On a stale payoff | MSG-S2-002; nothing computed |
| On no answer | MSG-GEN-006; nothing computed |

The ACE column list, the grant path and the reference operation are the working read of ASM-4360 and ASM-4362, because no source document states them: the FSD names `v_ace_batch_status` in a validation rule, the legacy data table names `v_ace_account` with a field range, and the Work Package records no contract dependency on P1 (GAP-2652, GAP-2654). The owners confirm both at the wave 2 contract freeze.

#### 12.6 Schedules

None. The contract declares no Schedule: the freshness test is a comparison at the moment of the calculation, not a scheduled scan, and the legacy key owns no job in the context pack's ownership rows.

#### 12.7 Tables owned

None. The element is written by the consumer against `treatment` in `rwb_treatment`, a table of this service created on its own Flyway sequence, and `decision_record` is the platform library object of DP-03 applied in the same schema. The contract creates no table, declares no column and adds no foreign key; `decision_log_entry` is P7's ledger in `rwb_decision` and is named only, never written or read here.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Reference-data fake (RWB-P3-E1043-CON) | The four governed values | A set in force at a version; a set whose floor is above the band; no set in force; a set whose version cannot be resolved |
| rwb-source-data contract fake | The two ACE reads, served through rwb-source-data | A balance at today's batch date; a product dated yesterday; a case with two accounts; an unreachable view |
| Element fake | The `PlanInstallment` shape | A complete element; one element per missing required field; an element with and without `ruleId` and `ruleVersion` |
| Output fake | The guard answers | MSG-P1-001 with the product and its date, MSG-S2-002 with the payoff date, MSG-GEN-006 for no answer |
| Decision-record fake | The record group of AC4 | An accepted record with the rule and set versions; a refusal with MSG-P7-009 and the field; a failure with MSG-P7-003 |
| Drift fixture | The contract test | One accepted and one refused body per section of the document |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consuming story rather than as a surprise at run time. The reference-data fake and the view fixture are what make Day 1 possible for RWB-S2-E3006-APP and RWB-ITG-W2.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 1 operation on RWB-P3-E1043-CON | Reference data only; one hop, 2 s, cached by set and version |
| Kafka | 0 | 0 | The consumer's package subscription is the application story's; no topic is declared here |
| Temporal | 0 | 0 | The contract fixes no workflow and no activity; it fixes the two reads the consumer's activity makes |
| SQL view | 0 | 2 (`recovery.v_ace_account`, `recovery.v_ace_batch_status`) | SELECT only, at the batch date, no copy |
| File | 0 | 0 | No file crosses the contract |

### 13. Solution plan

**Package.** Contract artefact of rwb-treatment: the element and the read types in `th.co.scb.ace.workbench.recovery.treatment.api`, the fakes as a test resource, and the versioning rule in the contract document. The implementation that performs the reads and writes the element is RWB-S2-E3006-APP. The artefact coordinates and the publication channel are Not specified in the source documents (GAP-2651; ASM-4359).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is taken as the service's own SELECT-only views, as the Work Package records no contract dependency on P1 and the conflict with Architecture v5 slide 8 is recorded in GAP-2654. DP-13 fixes the base this contract declares nothing on; DP-07 names the reference elements and their dependencies, with the C carried by the consuming story; DP-03 and DP-19 are the record and the screen paths.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `PlanInstallment` | Published type | The ten fields, the required and optional flags and the recording rule (BR1, BR2) |
| `ReferenceDataConsumptionRule` | Document | The four governed values, the set identifiers, the version and the refusal (BR3, AC2) |
| `AceReadRule` | Document | The two views, the columns, the batch date and the no-copy ban (BR4, AC3) |
| `GuardAnswers` | Document | MSG-P1-001, MSG-S2-002, MSG-GEN-006 and the record messages (BR5) |
| `VersioningSpecification` | Document | Major version 1, the compatible versus breaking rule and the pinning rule (AC5) |
| Fake set and drift fixture | Test asset | The reference-data, view, element, output and record fakes and the drift test (AC6) |

**Database.** No table and no column in this contract. The two plan numbers land in `treatment.installments` (DF-TRT-009) and `treatment.installment_amount` (DF-TRT-031), both TSD S2 T3.1 fields; the band, the floor and the payoff have no column and no field ID, which is why they exist only in the element (GAP-2651; ASM-4359).

**Configuration and reference data.** The set identifiers, the band, the floor and the freshness limit are data of rwb-case with a version and are named here, never fixed. The 2 s budget and the cache rule are the client library's. The capability area and the rights are access data of P4 and are not declared by this document.

**Build steps**

1. Write the element with its ten fields and the required and optional flags; validate it against the schema check (AC1).
2. Write the reference-data consumption rule with the four values, the set identifiers, the version and the refusal (AC2).
3. Write the ACE read rule with the two views, the columns and the batch date, and the no-copy ban (AC3, AC4).
4. Write the guard answers and the record group, and lint them against the library contract (AC3, AC4).
5. Write the versioning and pinning section with the compatible and breaking examples (AC5).
6. Generate the fake set and the drift fixture, and wire the drift test into the build of RWB-S2-E3006-APP (AC6).
7. Publish v1 and record the pinned versions of RWB-S2-E3006-APP and RWB-ITG-W2.

**Feature flag.** `rwb.treatment.plan-installment-contract`.

**Done when.** The document and the schema validate, the reference-data and read lints and the no-copy check are green, the fakes answer every criterion including the stale product, the stale payoff and the missing set, the drift test fails on an edited field and passes on the published version, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P1-001 | Data product stale after a late or failed load | {product} is from {date}. Today's load has not arrived. | The stale-product answer of the read rule; the product named is the one the step read |
| MSG-S2-002 | The payoff is older than the freshness limit | The payoff is from {date}. A new figure has been requested. | The stale-payoff answer of the read rule |
| MSG-GEN-006 | No reference set is in force, or a read does not answer | {system} is not available. Try again in a few minutes. | The no-answer answer of the reference rule |
| MSG-P7-009 | A record is refused for a missing or invalid field | The decision record was refused: {field} is missing or not valid. | The library's refusal, named by the record group |
| MSG-P7-003 | The record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The library's failure, named by the record group |

The five texts are copied unchanged from the legacy story, FSD A2.6.3.1 and RWB-PLT-E1027-CON, except MSG-P1-001, which is copied from the Error and Message Standard v4; this contract adds no message ID. MSG-S2-001 and MSG-S2-003 belong to the offer and its expiry and are not published here. Thai text follows decision DL10, which stays open with assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 named here; their confirmation is Not specified in the source documents (DL10).

### 15. Screens and states

No screen in this story, and the contract declares none. The element is shown on SCR-15 Settlement offer and SCR-14 Treatment record, which are reached through the gateway-bff composite route (DP-19) and whose field lists belong to the platform edge story and the screen owners. The contract fixes what those screens may show of the calculation: the model installment, the count, the band, the floor, the payoff with its as-at date and the versions, and no other number the step read. The states of SCR-14 Treatment record are empty, loading, error and no access: Not specified in the source documents (CG-ALL-8566). The states of SCR-15 Settlement offer are empty, loading, error and no access: Not specified in the source documents (CG-ALL-8567).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S2-E3006-CON-01 | AC1 | Contract | The element schema: the ten fields, the required and optional flags, the mapping to DF-TRT-009 and DF-TRT-031, the band and floor names; one element per missing required field refused |
| TC-S2-E3006-CON-02 | AC2 | Contract | The reference-data rule linted: the four values, the set identifiers, the version, the one-hop budget and the cache key; a rule without the set identifiers refused |
| TC-S2-E3006-CON-03 | AC3 | Component | The view fixture at today's batch date, dated yesterday and unreachable; MSG-P1-001, MSG-S2-002 and MSG-GEN-006 asserted; a read of a third ACE object refused |
| TC-S2-E3006-CON-04 | AC4 | Contract | The no-copy check on the schema: no balance, band, floor or range column; the record group in one transaction with MSG-P7-009 and MSG-P7-003 |
| TC-S2-E3006-CON-05 | AC5, AC6 | Component | A compatible and a breaking change on the element and the rules; the fake set and the drift fixture on a consuming story, green on the published version and red on an edited field |
| TC-S2-E3006-CON-06 | AC7 | Contract | A value named by no source in the reference fixture published as the working read, with its GAP and ASM identifiers and no fixed number |
| TC-S2-E3006-CON-07 | AC8 | Contract | The contract and the element checked for any fixed band, floor or freshness value and any written case status; each refused |
| TC-S2-E3006-CON-08 | AC9 | Contract | The contract checked for any REST path and any 401, 403 or 404 answer; each refused as owned by RWB-S2-E3001-CON |
| TC-S2-E3006-CON-09 | AC10 | Component | A read of rwb-case retried and run past the 2 s budget, and an ACE view read retried; MSG-GEN-006 asserted and no element written |

The legacy test set of RWB-E3-006 — TC-E3-006-01, TC-E3-006-03, TC-E3-006-04 and TC-E3-006-05 — is carried by RWB-S2-E3006-APP and by the wave 2 integration harness, and no legacy id is renumbered here. TC-E3-006-02 covers AC2, which is not assigned to this legacy key's stories here (GAP-2657; ASM-4365). These five are the contract's own tests.

### 17. Guardrails

- No business value in the contract: the band, the floor and the freshness limit are named, never fixed as numbers, and the two treatment fields are TSD S2 T3.1 fields (BR9).
- No personal data in the element, a read, an answer, a fake or a log: the element carries account keys, amounts, dates and versions only.
- No copy of ACE data: no balance, band or floor column is declared, and the consumer keeps no copy (BR4).
- No REST surface, no topic and no table of the contract's own: the base is fixed by DP-13 and the element rides the treatment representation.
- No second source for the band or the floor, and no second ACE object: one reference contract and two views.
- The outcome of a stale input or a missing answer is a written answer, never an exception a consumer has to guess.
- A published version is never edited in place: a breaking change raises major version 2 and a consumer pins rather than forks.
- The case status is never the contract's: the element is recorded, the stage reports and rwb-case moves the status (BR8).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| None (GAP-2653; ASM-4361) | The model installment and the range recorded with the version of the policy that produced them | Business Requirements Program, section 5.9 | FEAT-TRT-06 | 05 Restructure; 07 Route, settle and claim | R-SET-01; R-SET-03; R-SET-04; R-SET-05 | TC-S2-E3006-CON-01 to TC-S2-E3006-CON-05 |
| Legacy test set RWB-E3-006 | TC-E3-006-01, TC-E3-006-03, TC-E3-006-04, TC-E3-006-05 | Business Requirements Program, section 5.9 | FEAT-TRT-06 | 05 Restructure; 07 Route, settle and claim | R-SET-01; R-SET-04; R-SET-05 | Executed by RWB-S2-E3006-APP and the wave 2 integration harness; not owned here |

No requirement ID is allocated to FEAT-TRT-06: TSD S2 T8 maps REQ-S2-001 to REQ-S2-010 to FEAT-TRT-01 only, and the two section 5.9 requirements that describe the surrounding outcome, REQ-S2-001 and REQ-S2-004, name no feature. The trace runs on the feature code until the C1 PRD allocates one (GAP-2653; ASM-4361).

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3006-APP | App development | H consumer: implements the branch, the activity, the two reads, the element and the guard paths against this contract and its fakes; owner of the two legacy acceptance criteria |
| RWB-PLT-E1043-CON | Contract | Referred to: the reference-data client library, its cache rule and its refusal. This contract adds no build dependency of its own |
| RWB-P3-E1043-CON | Contract | Referred to: the reference-data contract that holds the band, the floor and the freshness limit |
| RWB-PLT-E1027-CON | Contract | Referred to: the local decision-record library and its two messages |
| RWB-PLT-N001-CON | Contract | Referred to: the gateway-bff composite route that shows the element on SCR-14 and SCR-15 |
| RWB-S2-E3005-CON | Contract | Sibling: the affordability element whose accepted terms are this element's input |
| RWB-S2-E3001-CON | Contract | Sibling: the treatment representation that carries this element on its read |
| P3 rwb-case | Service | The reference sets, their values and their version |
| ACE and its DBA | External capability, existing | The two views, their columns and the SELECT grant (ASM-4362) |
| RWB-ITG-W2 | Integration | I: the cross-service proof of the reads and the record against the live owners, and the owner of the legacy `-ITG` copies |

### 19. Out of scope

- The branch of `TreatmentWorkflow`, the calculation activity, the two reads, the result repository, the guard paths and the tests against this contract: RWB-S2-E3006-APP.
- The two legacy acceptance criteria of RWB-E3-006, AC1 and AC3: carried verbatim by RWB-S2-E3006-APP; none is repeated or renumbered here. AC2 is not assigned to this legacy key's stories here (GAP-2657; ASM-4365).
- The affordability element, its Nexus binding and its guards: RWB-S2-E3005-CON and RWB-S2-E3005-APP.
- The treatment representation, its create and read operations and the treatment states: RWB-S2-E3001-CON and RWB-S2-E3001-APP.
- The offer inside the range, the below-floor approval and the offer build: RWB-S2-E3002-APP, RWB-S2-E3003-APP and RWB-S2-E3004-APP.
- The case, its status and the parent `CaseWorkflow`: rwb-case (P3); the contract declares no case read and no status write.
- The reference sets, their values, their version and their governance: rwb-case (P3) and its contract; this document names them only.
- The `recovery.v_ace_*` views, their columns, their grants and the ACE batch that dates them: ACE and its DBA (GAP-2654).
- The rule package and the route set, their authoring, approval, effective date, rollback and the central ledger: P7 rwb-decision; this contract names the version only.
- SCR-14 and SCR-15, their field lists and the gateway-bff composite route: the platform edge story and the screen owners (DP-19).
- The real cross-service proof of the reads, the element and the screens against the live owners: RWB-ITG-W2, which also owns the `-ITG` copies of the legacy cases.

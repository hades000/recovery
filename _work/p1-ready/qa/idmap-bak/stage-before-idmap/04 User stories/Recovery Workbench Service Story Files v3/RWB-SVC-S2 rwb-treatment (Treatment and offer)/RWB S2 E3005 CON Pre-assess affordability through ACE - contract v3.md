# RWB-S2-E3005-CON Pre-assess affordability through ACE - contract

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E3-005 for rwb-treatment. The contract declares the affordability element recorded against the treatment and the one Nexus binding to the ACE Common restructure calculator in the `ace-collection` namespace, and it declares no REST operation of its own on base `/api/recovery/treatment/v1` (DP-13); the record group it names is the local decision record of RWB-PLT-E1027-CON (DP-03) and the element is reached by the screens through the gateway-bff composite route (DP-19). It is published on Day 1 at status Draft (realignment v1). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (11 resolved, 8 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3005-CON |
| Readiness decisions | RD-P1-004 |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Contract version | Major version 1 on base /api/recovery/treatment/v1 |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Size | Set by the squad at refinement (no size in the source documents) |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-005 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register). Aligned the quoted English to Error and Message Standard v6.


### 1. Story

As a **contract owner of rwb-treatment**, I want **the published contract of the affordability step — the `AffordabilityResult` element that is recorded against the treatment, the one Nexus binding to the ACE Common restructure calculator with its request, its answer, its 2 s budget, its retry and the answer it gives when the calculator does not reply, the rule that nothing is copied out of ACE, the versioning rule and the fakes — instead of the monolith's in-process call into the ACE common module under INT-34**, so that **the application story, the offer stories of this service and the wave 2 integration harness build and test on Day 1 without an ACE Common deployment, and no reader of the result depends on a shape that was never written down**.

This is the contract slice of legacy RWB-E3-005. It owns:

- the `AffordabilityResult` element, its required and optional fields and the rule that it is recorded against the treatment and against nothing else;
- the Nexus binding: the operation name `calculateRestructurePlan`, the namespace `ace-collection`, the request, the answer, the 2 s synchronous budget, the retry and the failure answer with MSG-GEN-006;
- the no-copy rule: no affordability band, score, threshold or result column is copied out of ACE into `rwb_treatment`, and the element carries the result, the plan reference, the two plan numbers and the two times only;
- the decision-record group of the same transaction, named as the local record of RWB-PLT-E1027-CON, with its refusal and failure messages;
- the compatibility rule and the pinning rule for the consuming stories;
- the fakes and the drift test that keep the document and the code together.

It does not own: the branch of `TreatmentWorkflow` that calls the calculator, the activity, the result repository and the tests against it, which are RWB-S2-E3005-APP; the treatment read that shows the result, which is RWB-S2-E3001-APP; the offer build and the plan installment range, which are RWB-S2-E3004-APP; the settlement range and its floor, which are RWB-S2-E3002-APP and RWB-S2-E3003-APP; the case status the step reacts to, which is rwb-case's; the rule package and its version, which are P7 rwb-decision's; the calculator itself, which is an existing ACE capability with its own owner; and the two screens and their composite route, which are the platform edge story's under DP-19.

### 2. Business rationale

In the monolith the affordability step called the ACE common module through a published Java interface in the same process (TSD S2 T2 "Published interface: Java interface other modules call"; T5.1 row INT-34 "ACE common module — Both — Published module interface — Per request"), and the result lived in the offer row and in `decision_log_entry`. Nothing in that arrangement could be built on its own. The application could not be tested without the other side of the interface, the result had no agreed field list, and a downstream reader had only one option if it wanted the affordability answer: read the module's table.

Architecture v5 changes the call type and with it the whole contract. Slide 18 gives rwb-treatment one OUT line, "NEXUS ACE Common: restructure calculator (Nexus)", and the slide's legend fixes what that means: "NEXUS = Temporal Nexus operation into another namespace". Slide 39 lists the restructure calculator (Nexus) among the ACE Common contracts the ACE team owns, and the Temporal and Drools Design states that `ace-collection` is ACE's namespace, "reached through Nexus (for example the restructure calculator)", on Temporal 1.30+ (slide 11 notes). The calculator is therefore not a REST operation of the 19 services, not a table and not one of the 19 services. It is an external capability with a namespace and an operation, and the only thing the Workbench can publish about it is the binding.

**The division of the legacy key is fixed.** This WP delivers the contract. The **application** — the affordability branch of `TreatmentWorkflow`, the `calculateAffordability` activity, the result record, the refusal and stale-input paths and the tests — is **RWB-S2-E3005-APP**, and the **four legacy acceptance criteria stay with it** and are not repeated here (they are listed in its section 7 with their origin tag). The **cross-service proof** is **RWB-ITG-W2**. Every criterion in section 7 of this document is new and tests only the contract deliverable in this title.

The contract exists to unblock three things on Day 1. The element gives the offer stories and the treatment read one shape, so the plan reference and the two plan numbers can be shown and reused without a second definition. The binding gives the application one fake to build against, so no test waits for the ACE Common estate and no build depends on a namespace that is not in the plan. And the failure answer gives the timeout a written outcome, so the stage can be told to stay in `AFFORDABILITY_IN_ACE` rather than leaving a case half-moved — the failure path is the part of a synchronous check that is most often left unstated and most often discovered in production.

What the contract deliberately does not do: it copies no band out of ACE, declares no REST path, owns no topic and no task queue, writes no table, and does not decide the case status. All four refusals are in section 12 and in section 19.

### 3. Preconditions

- The call type is fixed: Architecture v5 slide 18 (OUT, "NEXUS ACE Common: restructure calculator (Nexus)") and its legend ("NEXUS = Temporal Nexus operation into another namespace"), slide 39 (the restructure calculator among the ACE Common contracts), and the Temporal and Drools Design slide 11 notes on `ace-collection` and Nexus.
- The operation name, the request and answer fields, the 2 s budget, the retry and the failure answer have no published source. Architecture v5 names the calculator by call type only, TSD S2 T5.1 gives INT-34 as a "published module interface" with no operation, and TSD S2 T3.1 has no affordability field and no `plan_ref` column; the contract is therefore published as the working read of ASM-3071 (GAP-1875).
- The two rules that drive the step are fixed by the Routing Logic v4: R-RES-06 from `WITH_FCR_OFFICER` on `AFFORDABILITY_REQUIRED` when `treatment_type = TDR` to `AFFORDABILITY_IN_ACE`, and R-RES-07 from `AFFORDABILITY_IN_ACE` on `AFFORDABILITY_PASSED` when `affordability_result = pass` to `WITH_FCR_OFFICER`. The `pass` value of the condition is the vocabulary the element's `affordabilityResult` uses.
- The decision record is the platform library's: `DecisionRecordWriter.record(DecisionRecord)` with `@Transactional(propagation = MANDATORY)`, refusing with MSG-P7-009 and failing with MSG-P7-003, and `decision_record` is the library object created in `rwb_treatment` (DP-03; RWB-PLT-E1027-CON).
- The treatment columns that take the two plan numbers exist in TSD S2 T3.1: `installments` (DF-TRT-009, integer) and `installment_amount` (DF-TRT-031, numeric(18,2)).
- The documents are served to the screens through the gateway-bff composite route (DP-19; RWB-PLT-N001-CON), so the contract fixes the element, not a route.
- No build dependency and no approval stop: a CON story is Day 1 by rule (Template and Rules §R5.7) and is published at status Draft (realignment v1).

### 4. Flow

1. The contract author fixes the `AffordabilityResult` element: its seven fields, which of them are required, and the rule that it is recorded against the treatment.
2. The author fixes the Nexus binding: the operation name, the namespace, the request and the answer, and the mapping of the answer fields to the element.
3. The author fixes the call rules: the 2 s synchronous budget of the one-hop rule, the retry the workflow applies, the answer when the calculator does not reply, and the warning the stale payoff raises.
4. The author writes the no-copy rule and the decision-record group, and names the two library messages.
5. The author writes the compatibility and pinning rule: what may change inside major version 1 and what raises version 2.
6. The fake set is generated from the document: the calculator fake, the element fake, the failure and timeout answers and the drift fixture.
7. The contract test runs the fakes against the document on every change and fails the build on any drift.
8. The document and the fakes are published at v1 and RWB-S2-E3005-APP and RWB-ITG-W2 pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A published element drops a required field, or adds an optional one that a consumer depends on | The schema check fails the build; required and optional fields are as published | None | AC1 |
| X2 | The binding is published without the namespace, the operation name or the 2 s budget | The binding lint fails the build; all three are required | None | AC2, AC3 |
| X3 | The failure answer is published as an exception or as an empty answer | The binding lint fails the build; the failure is a documented answer with MSG-GEN-006 | MSG-GEN-006 | AC3 |
| X4 | A consumer copies a band, a score or a result column out of ACE, or reads the calculator's store | The boundary and drift checks fail the build; the element carries the result and the plan terms only | None | AC4 |
| X5 | A breaking change is made to the element, the binding or the failure answer | The change raises major version 2; v1 is never edited in place and stays readable | None | AC5 |
| X6 | A consuming story ships without the drift test, or a fake stops answering the document | The drift test fails the build of the consuming story | None | AC6 |
| X7 | A value a consumer needs is named by no source — the full field list, the plan inputs or the exact answer envelope | The value is published as the working read of the assumption, and the gap stays open | Not specified in the source documents (GAP-1875; ASM-3071) | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document and fakes; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | The field order, the record widths and the fixture set are open until v1 is frozen; the element, the required fields, the operation, the budget, the failure answer and the no-copy rule are fixed |
| Valuable | Unblocks the application story and the wave 2 harness on Day 1, and gives the offer stories one shape for the plan reference and the plan numbers |
| Estimable | One element, one binding, three call rules, one compatibility rule and four fakes |
| Small | One sprint for the document, the fakes and the drift test |
| Testable | Each criterion below is one schema, binding or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: affordability contract of rwb-treatment

  Background:
    Given the contract document is published with major version 1 on the base of rwb-treatment
    Given the calculator is one Nexus operation into namespace ace-collection
    Given the contract declares no REST operation, no topic and no table of its own

  Scenario: AC1 The AffordabilityResult element and its required fields are published (new, D-RCV-60)
    Given the element section of the contract document
    When it is validated and linted
    Then it publishes AffordabilityResult with affordabilityResult, planRef, installmentAmount, installmentCount, calculatedAt, ruleId and ruleVersion
    Then affordabilityResult, planRef, installmentAmount, installmentCount, calculatedAt and ruleVersion are required and ruleId is optional
    Then affordabilityResult carries the pass and fail vocabulary of R-RES-07 and R-RES-08, and installmentAmount and installmentCount map to DF-TRT-031 and DF-TRT-009
    Then the element is recorded against the treatment and against no other record, and it has no collection and no free-text field
    Then a document that drops a required field fails the schema check

  Scenario: AC2 The Nexus binding and its request and response are fixed (new, D-RCV-60)
    Given the binding section of the contract document
    When it is validated against the platform Nexus conventions
    Then it names one operation calculateRestructurePlan in namespace ace-collection, called synchronously by an activity on queue rwb-treatment
    Then the request carries caseId, the plan inputs of the case and ruleVersion, and nothing else
    Then the response maps to affordabilityResult, planRef, installmentAmount, installmentCount, calculatedAt, ruleId and ruleVersion
    Then the binding declares no REST path, no topic and no second operation
    Then a binding published without the namespace, the operation name or the request fields fails the lint

  Scenario: AC3 The budget, the retry and the failure answer are fixed (new, D-RCV-60)
    Given the call rules of the binding section
    When a call is made and the calculator does not answer
    Then the call is bounded by the 2 s synchronous budget of the one-hop rule
    Then the activity answers a timeout to the workflow, which retries to the document's limit
    Then when the attempts are exhausted the documented answer is "stage stays in AFFORDABILITY_IN_ACE, nothing written" with MSG-GEN-006
    Then the failure is an answer and never an unhandled exception, and a stale payoff is answered with MSG-S2-002 before the call
    Then a binding that publishes no failure answer fails the lint

  Scenario: AC4 The no-copy rule and the decision-record group are fixed (new, D-RCV-60)
    Given the data rule and the record group of the contract document
    When the element and the schema are checked together
    Then no affordability band, score, threshold or result column is declared for rwb_treatment, and no calculator field is copied
    Then the result, the two plan numbers and the record are written in one transaction
    Then the record is the local record of RWB-PLT-E1027-CON, written with ruleId and ruleVersion, and a refused record names its field with MSG-P7-009 and a failed one stops the action with MSG-P7-003
    Then decision_log_entry is named only as P7's ledger and is never written or read by the consumer

  Scenario: AC5 Versioning separates a compatible change from a new major version (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published element
    Then a backward-compatible change keeps major version 1
    Then a breaking change to the element, the binding or the failure answer raises major version 2 and v1 is never edited in place
    Then RWB-S2-E3005-APP and RWB-ITG-W2 pin a published version and raise a change request rather than a private variant

  Scenario: AC6 The fakes answer the document and the drift test holds (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the calculator fake, the element fake, the output fake and the drift fixture
    Then the calculator fake answers a passed result and the calculated plan, a failed result, a timeout inside the budget and a timeout beyond it
    Then the output fake answers the element of AC1 with the plan reference, the installment amount and the count
    Then the drift test fails the build of a consuming story on any difference from sections 12 and 13

  Scenario: AC7 A value that no source names is published as the working read and the gap stays open (new, D-RCV-60)
    Given a consumer needs a value that no source names
    When the element and its answer envelope are published with that value
    Then the value is published as the working read of the assumption
    Then the gap stays open with the message Not specified in the source documents (GAP-1875; ASM-3071)

  Scenario: AC8 The business rules BR1 to BR9 of section 8 are each checked (new, D-RCV-60)
    Given the business rules BR1 to BR9 of section 8 apply to the element, the binding, the write and the step
    When each rule is checked against the contract
    Then each of BR1 to BR9 is verified
    Then the test values are Not specified in the source documents (DOR-RWB-S2-E3005-CON-4)

  Scenario: AC9 The error answers 401, 403 and 404 of the provided operations are fixed (new, D-RCV-60)
    Given the failure answers of the provided operations in the contract document
    When the error answers are validated against the platform conventions
    Then the answers 401, 403 and 404 are each declared for the provided operations with the status they return
    Then an error answer that the contract does not declare is refused
```

These criteria are new and test only the contract deliverable. No legacy acceptance criterion is repeated here: **AC1 to AC4 of RWB-E3-005 are carried by RWB-S2-E3005-APP**, and every identifier used above comes from the legacy story, the Routing Logic v4, TSD S2 or Architecture v5, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The element recorded against the treatment carries the result, the plan reference, the installment amount, the installment count, the calculated-at time, the rule ID and the rule version, and nothing else | RWB-E3-005 AC1; DF-TRT-009; DF-TRT-031; ASM-3071 |
| BR2 | `affordabilityResult` uses the `pass` and `fail` vocabulary of R-RES-07 and R-RES-08, so the rule condition and the recorded value agree | R-RES-07; R-RES-08 |
| BR3 | The calculator is one Nexus operation in `ace-collection`, called synchronously inside the 2 s budget of the one-hop rule, and it is never a REST contract, a table or a shared schema | INT-34; Architecture v5 slides 18 and 39; Temporal and Drools Design slide 11 |
| BR4 | When the calculator does not answer, the stage stays in `AFFORDABILITY_IN_ACE` and the caller sees MSG-GEN-006; no partial result and no guessed plan is recorded | ASM-3071; R-RES-06 |
| BR5 | No affordability band, score, threshold or result column is copied out of ACE, and the consumer reads no store of the calculator | DP-01; ASM-3071 |
| BR6 | The result and the plan terms are written with the local decision record in one transaction, through `DecisionRecordWriter` with `MANDATORY` propagation | DP-03; ADR-022; RWB-PLT-E1027-CON |
| BR7 | A published version is never edited: a compatible change stays in major version 1 and a breaking change raises major version 2 | Template and Rules §R7.2; §R5.4 class C |
| BR8 | The case status stays rwb-case's: the contract fixes the element and the binding, and the stage reports to the parent `CaseWorkflow` without writing a case row | DP-01; ASM-3062 |
| BR9 | The step is nominated by the RESTRUCTURE rules evaluated locally, and the rule version that decided is the version recorded with the result | R-RES-06; R-RES-07; EV-30; ASM-3063 |

### 9. State transitions

None of the case statuses are this contract's, and a document has no runtime state of its own. The table fixes the four outcomes the contract names so that a consumer cannot invent a fifth.

| Object | State | Meaning in the contract |
|---|---|---|
| Call | Answered, pass | The calculator answered inside the budget with `affordabilityResult` pass; the result is recorded and the stage reports `AFFORDABILITY_PASSED` |
| Call | Answered, fail | The calculator answered with `affordabilityResult` fail; the result is recorded and the stage reports `AFFORDABILITY_FAILED` |
| Call | Not answered | No answer inside the budget after the retries; nothing is written, the stage stays in `AFFORDABILITY_IN_ACE`, MSG-GEN-006 |
| Call | Refused before the call | The payoff on the case is stale; MSG-S2-002 and no call |
| Element | Recorded | Written against the treatment in the same transaction as the record and the stage report |
| Element | Absent | The transaction rolled back, or the calculator did not answer; there is no partial element |
| Contract version | v1 | The published version every consuming story pins |
| Contract version | v2 | Raised by a breaking change; v1 stays readable and is never edited |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document and the fakes |
| The service owner of rwb-treatment | Approves a breaking change and freezes a version |
| The ACE Common owner | Confirms the operation name, the namespace and the answer fields at the wave 2 contract freeze (ASM-3071) |
| The platform workflow owner | Confirms the Nexus binding, the 2 s budget and the retry of the workflow kit |
| RW-RESTRUCT, restructuring officer (FCR) | Consumes the result through the screens and holds rights C, R and U on the capability area; the step itself runs unattended under the service identity |
| The service teams of the offer stories | Consume the element, pin the version and raise a change request rather than a private variant |
| P7 rwb-decision | Owns the rule package and its version, which the request names |
| RW-AUDIT, RW-COE | Read the recorded result and the decision records; they do not consume this document directly |
| No delegation of authority level applies | A contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in the document, an example or a fake; where an actor must be named, a role code or a service identity is used. The rwb-access authorise check of DP-08 for the operations is Not specified in the source documents (DOR-RWB-S2-E3005-CON-6); the document declares no REST operation of its own.

### 11. Data

| Item | Value |
|---|---|
| Business data published (BR Field ID: Not specified in the source documents (DOR-RWB-S2-E3005-CON-7)) | None. The document publishes field names, the two vocabularies, the budget and the messages; no customer, account or case value appears |
| Element published (BR Field ID: Not specified in the source documents (DOR-RWB-S2-E3005-CON-7)) | The seven fields of section 12.1, with the required and optional flags and the two treatment columns they map to |
| Personal data (BR Field ID: Not specified in the source documents (DOR-RWB-S2-E3005-CON-7)) | None. The request carries the case ID and the plan inputs; no name, national identifier, account number or document content |
| Tables published (BR Field ID: Not specified in the source documents (DOR-RWB-S2-E3005-CON-7)) | None. The consumer writes the element against `treatment` in `rwb_treatment`; `decision_record` is the platform library object |
| Field identifiers (BR Field ID: Not specified in the source documents (DOR-RWB-S2-E3005-CON-7)) | DF-TRT-009 and DF-TRT-031 for the two plan numbers; the element's own identifiers are Not specified in the source documents (GAP-1875; ASM-3071) |
| Retention (BR Field ID: Not specified in the source documents (DOR-RWB-S2-E3005-CON-7)) | The element is kept with the treatment row for the life of the case record; the retention period of the result is Not specified in the source documents (GAP-1875; ASM-3071) |

The element is the one place where a calculator value could leak into the service's schema, so the document fixes that it carries the answer and the plan reference only: no band, no score, no threshold, no rate table and no free-text reason from the calculator.

### 12. Contract

#### 12.1 REST operations provided

None. This contract declares no REST operation, adds no path to base `/api/recovery/treatment/v1` and publishes no OpenAPI document (DP-13). The two screens that show the recorded result reach it through the gateway-bff composite route and the sibling treatment read, and neither is declared here (DP-19).

**Element: `AffordabilityResult`**

| Field | Type | Required | Maps to | Note |
|---|---|---|---|---|
| `affordabilityResult` | enum `pass`, `fail` | Yes | The condition of R-RES-07 and R-RES-08 | The vocabulary is the rule's own, so the recorded value and the rule condition agree |
| `planRef` | string | Yes | No treatment column | The reference of the calculated plan; the field name in the calculator's own store is not published |
| `installmentAmount` | numeric(18,2) | Yes | DF-TRT-031 `installment_amount` | The model installment the calculator returns |
| `installmentCount` | integer | Yes | DF-TRT-009 `installments` | The number of installments of the calculated plan |
| `calculatedAt` | timestamptz | Yes | No treatment column | When the calculator answered; not the time the Workbench recorded it |
| `ruleId` | string | No | No treatment column | Present when the calculator reports a rule of its own, which is not the RESTRUCTURE rule that called it |
| `ruleVersion` | string | Yes | The version group of the decision record | The version of the RESTRUCTURE package in force when the call was made |

The element is recorded against the `treatment` row and against no other record; it has no collection and no free-text field. Its own BR Field IDs have no row in the Logical Data Model, so the field names are the working read of ASM-3071 (GAP-1875).

#### 12.2 REST operations consumed

None. The contract consumes no REST operation: the calculator is reached by Nexus (section 12.5), the rule package arrives on an event (section 12.4), and the case status is not read by this contract at all. The case ID that the request carries arrives on the case signal the parent `CaseWorkflow` forwards, so no case read is declared either (ASM-3062).

#### 12.3 Events published

None. This contract owns no topic and publishes no event; the service's topic `rwb.treatment.events.v1` and its events `TreatmentApproved` and `TreatmentClosed` belong to the offer and closure stories of this service (DP-14). The result is not announced on Kafka: it is recorded and read.

#### 12.4 Events consumed

None by this contract. The consumer's rule package arrives on `rwb.decision.RulePackageInForce.v1` from P7 (EV-30), which is the application story's subscription and the service template's rule loader; the contract only requires that the request name the version that was in force.

#### 12.5 Workflows and activities

None of its own: the contract defines no workflow, no activity and no task queue. What it does fix is the one binding the consumer's activity calls, so that the call type, the namespace and both sides of the wire are written down in one place.

| Binding element | Value |
|---|---|
| Call type | Temporal Nexus operation, synchronous, from an activity on task queue `rwb-treatment` in namespace `rwb-recovery` |
| Namespace | `ace-collection`, ACE's namespace, reached through Nexus on Temporal 1.30+ |
| Operation | `calculateRestructurePlan` |
| Request | `caseId`, the plan inputs of the case, `ruleVersion`; no personal data, no document and no free text |
| Response | `affordabilityResult`, `planRef`, `installmentAmount`, `installmentCount`, `calculatedAt`, `ruleId`, `ruleVersion` |
| Budget | 2 s synchronous, the one-hop rule of the platform |
| On timeout | The activity answers a timeout; the workflow retries per the kit (1 s initial interval, back-off 2, 10 attempts) |
| On exhausted retries | The documented answer is the stage stays in `AFFORDABILITY_IN_ACE`, nothing is written, the caller sees MSG-GEN-006 |
| On a stale payoff | MSG-S2-002 and no call |
| Second operation | None |

The operation name, the request and answer field list, the budget, the retry and the failure answer are the working read of ASM-3071, because no source document states them: Architecture v5 slide 18 names the calculator by call type only and TSD S2 T5.1 gives INT-34 as a "published module interface" (GAP-1875). The ACE Common owner and the platform workflow owner confirm both at the wave 2 contract freeze.

#### 12.6 Schedules

None. The contract declares no Schedule; the two-working-day timer of R-RES-06 is the consumer's durable timer and is not part of this document.

#### 12.7 Tables owned

None. The element is written by the consumer against `treatment` in `rwb_treatment`, a table of this service created on its own Flyway sequence, and `decision_record` is the platform library object of DP-03 applied in the same schema. The contract creates no table, declares no column and adds no foreign key; `decision_log_entry` is P7's ledger in `rwb_decision` and is named only, never written or read here.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Calculator fake | The Nexus operation `calculateRestructurePlan` | A passed answer with `planRef`, `installmentAmount`, `installmentCount` and `calculatedAt`; a failed answer; an answer with no `planRef`; a timeout inside the 2 s budget and one beyond it |
| Element fake | The `AffordabilityResult` shape | A complete element; one element per missing required field; an element with and without `ruleId` |
| Output fake | The failure answer | The documented timeout answer with MSG-GEN-006, and the stale-payoff answer with MSG-S2-002 before any call |
| Decision-record fake | The record group of AC4 | An accepted record with the rule version; a refusal with MSG-P7-009 and the field; a failure with MSG-P7-003 |
| Drift fixture | The contract test | One accepted and one refused body per section of the document |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consuming story rather than as a surprise at run time. The calculator fake is what makes Day 1 possible for RWB-S2-E3005-APP and RWB-ITG-W2.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 0 | The contract declares no path and no OpenAPI document |
| Kafka | 0 | 0 | The consumer's package subscription is the application story's; no topic is declared here |
| Temporal | 0 | 1 Nexus operation declared | `calculateRestructurePlan` in `ace-collection`, synchronous, 2 s budget, bound from the consumer's activity |
| File | 0 | 0 | No file crosses the contract |

### 13. Solution plan

**Package.** Contract artefact of rwb-treatment: the element and the binding types in `th.co.scb.ace.workbench.recovery.treatment.api`, the operation and request and answer records with them, the fakes as a test resource, and the versioning rule in the contract document. The implementation that calls the binding is RWB-S2-E3005-APP. The artefact coordinates and the publication channel are Not specified in the source documents (GAP-1875; ASM-3071).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the record group the element is written with; DP-13 fixes the base this contract declares nothing on; DP-19 is how the recorded element reaches SCR-14 and SCR-15.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `AffordabilityResult` | Published type | The seven fields, the required and optional flags and the recording rule (BR1, BR2) |
| `CalculateRestructurePlanRequest`, `CalculateRestructurePlanResponse` | Published types | Both sides of the Nexus operation, with the plan inputs and the answer fields (BR3) |
| `AffordabilityBindingSpecification` | Document | The operation, the namespace, the budget, the retry, the failure answer and the stale-payoff rule (AC2, AC3) |
| `AffordabilityNoCopyRule` | Document | The ban on copying a band, a score, a threshold or a result column, and the record group of the same transaction (BR5, BR6) |
| `VersioningSpecification` | Document | Major version 1, the compatible versus breaking rule and the pinning rule (AC5) |
| Fake set and drift fixture | Test asset | The calculator, element, output and decision-record fakes and the drift test every consuming story runs (AC6) |

**Database.** No table and no column in this contract. The two plan numbers land in `treatment.installments` (DF-TRT-009) and `treatment.installment_amount` (DF-TRT-031), both of which TSD S2 T3.1 already defines; the result and the times have no column and no field ID yet, which is the reason the element is published as a working read (GAP-1875; ASM-3071).

**Configuration and reference data.** The namespace, the operation and the budget are configuration of the binding and are confirmed at the wave 2 contract freeze. The `pass` and `fail` values are the rule vocabulary of R-RES-07 and R-RES-08 and are not a list this contract invents. The rule package and its version are P7's data.

**Build steps**

1. Write the element with its seven fields and the required and optional flags; validate it against the schema check (AC1).
2. Write the binding with the namespace, the operation, the request and the answer; lint it against the platform Nexus conventions (AC2).
3. Write the call rules: the 2 s budget, the retry, the failure answer with MSG-GEN-006 and the stale-payoff answer with MSG-S2-002 (AC3).
4. Write the no-copy rule and the record group; lint the decision record against the library contract (AC4).
5. Write the versioning and pinning section with the compatible and breaking examples (AC5).
6. Generate the fake set and the drift fixture, and wire the drift test into the build of RWB-S2-E3005-APP (AC6).
7. Publish v1 and record the pinned version of RWB-S2-E3005-APP and RWB-ITG-W2.

**Feature flag.** `rwb.treatment.affordability-contract`.

**Done when.** The document and the schema validate, the binding lint and the no-copy check are green, the four fakes answer every criterion including the timeout and the missing `planRef`, the drift test fails on an edited field and passes on the published version, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-GEN-006 | The calculator does not answer inside the budget, after the retries | {system} is not available. Try again in a few minutes. | The documented failure answer of the binding; the system named is the ACE Common calculator |
| MSG-S2-002 | A stale payoff is on the case before the call | The payoff is from {date}. A new figure has been requested. | The pre-call warning of the binding |
| MSG-P7-009 | A record is refused for a missing or invalid field | The decision record was refused: {field} is missing or not valid. | The library's refusal, named by the record group |
| MSG-P7-003 | The record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The library's failure, named by the record group |

The four texts are copied unchanged from RWB-E3-005 and RWB-PLT-E1027-CON, and this contract adds no message ID. The element declares no message of its own: a refused element is a library refusal with its field name, and a missing answer is the binding's failure answer. Thai text follows decision DL10.

### 15. Screens and states

No screen in this story, and the contract declares none. The element is shown on SCR-14 Treatment record and SCR-15 Settlement offer, which are reached through the gateway-bff composite route (DP-19) and whose field lists belong to the platform edge story and the screen owners. The contract fixes what those screens may show of the result: the plan reference, the installment amount, the installment count, the calculated-at time and the result, and no band or score from the calculator. SCR-14 states (empty, loading, error, no access): Not specified in the source documents (CG-ALL-8545). SCR-15 states (empty, loading, error, no access): Not specified in the source documents (CG-ALL-8546).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S2-E3005-CON-01 | AC1 | Contract | The element schema: the seven fields, the required and optional flags, the `pass` and `fail` values, the mapping to DF-TRT-009 and DF-TRT-031; one element per missing required field refused |
| TC-S2-E3005-CON-02 | AC2 | Contract | The binding linted: the namespace `ace-collection`, the operation `calculateRestructurePlan`, the request and answer fields; a binding without the namespace, the operation or a request field refused |
| TC-S2-E3005-CON-03 | AC3 | Component | The calculator fake answering inside and beyond the 2 s budget; the retry to the kit limit; the failure answer with MSG-GEN-006; the stale-payoff answer with MSG-S2-002 |
| TC-S2-E3005-CON-04 | AC4 | Contract | The no-copy check on the schema: no band, score, threshold or result column; the record group in one transaction with MSG-P7-009 and MSG-P7-003 |
| TC-S2-E3005-CON-05 | AC5, AC6 | Component | A compatible change and a breaking change on the element and the binding; the four fakes and the drift fixture on a consuming story, green on the published version and red on an edited field |
| TC-S2-E3005-CON-06 | AC7 | Contract | A value named by no source: the working read published as the element value and the gap kept open with the message Not specified in the source documents (GAP-1875; ASM-3071) |
| TC-S2-E3005-CON-07 | AC8 (BR1 to BR9) | Contract | The nine rules of section 8 checked on the element, the binding, the write and the step; test values Not specified in the source documents (DOR-RWB-S2-E3005-CON-4) |
| TC-S2-E3005-CON-08 | AC9 | Contract | Not specified in the source documents (NEWAC-RWB-S2-E3005-CON-AC9) |

The legacy test set of RWB-E3-005 — TC-E3-005-01 to TC-E3-005-06 — is carried by RWB-S2-E3005-APP and by the wave 2 integration harness, and no legacy id is renumbered here. These five are the contract's own tests.

### 17. Guardrails

- No business value in the contract: the `pass` and `fail` values are the rule vocabulary of R-RES-07 and R-RES-08, the two treatment columns are TSD S2 T3.1 fields, and no threshold, band or rate is fixed here.
- No personal data in the element, a request, an answer, a fake or a log: the request carries the case ID and the plan inputs, and the answer carries numbers, a reference, a result and a version.
- No copy of ACE data: no band, score, threshold or result column is declared, and the consumer reads no store of the calculator (BR5).
- No REST surface, no topic and no table of the contract's own: the base is fixed by DP-13 and the contract declares nothing on it.
- No second operation and no second namespace: one binding, one operation, one budget.
- The outcome of a missing answer is a written answer, never an exception a consumer has to guess: MSG-GEN-006 and the stage stays where it is.
- A published version is never edited in place: a breaking change raises major version 2 with a new version label and a migration note, and a consumer pins rather than forks.
- The case status is never the contract's: the element is recorded, the stage reports and rwb-case moves the status (BR8).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-001 | A restructure proposed in the collections system reaches the restructuring officer with the case, and the case does not leave the Workbench | Business Requirements Program, section 5.9 | FEAT-TRT-05 | 07 Route, settle and claim | R-RES-06; R-RES-07 | TC-S2-E3005-CON-01, TC-S2-E3005-CON-02, TC-S2-E3005-CON-04 |
| Legacy test set RWB-E3-005 | TC-E3-005-01, TC-E3-005-02, TC-E3-005-03, TC-E3-005-04, TC-E3-005-05, TC-E3-005-06 | Business Requirements Program, section 5.9 | FEAT-TRT-05 | 07 Route, settle and claim | R-RES-06; R-RES-07 | Executed by RWB-S2-E3005-APP and the wave 2 integration harness; not owned here |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3005-APP | App development | H consumer: implements the branch, the activity, the binding call, the result record and the refusal path against this contract and its fakes; owner of the four legacy acceptance criteria |
| RWB-PLT-E1027-CON | Contract | Referred to: the local decision-record library and its two messages that the record group names. This contract adds no build dependency of its own |
| RWB-PLT-N001-CON | Contract | Referred to: the gateway-bff composite route that shows the element on SCR-14 and SCR-15 |
| RWB-S2-E3001-APP | App development | Sibling: the treatment read that returns the recorded element |
| RWB-S2-E3004-APP | App development | Sibling: the offer build and the plan installment range, which consume the plan reference and the two plan numbers |
| ACE Common restructure calculator | External capability, existing | The namespace `ace-collection` and the operation this contract binds; owned by the ACE Common owner, not a story of this plan |
| P7 rwb-decision | Service | Referred to: the RESTRUCTURE package and its version, which the request and the record name |
| RWB-ITG-W2 | Integration | I: the cross-service proof of the binding and the record against the live owners, and the owner of the legacy `-ITG` copies |

### 19. Out of scope

- The branch of `TreatmentWorkflow`, the `calculateAffordability` activity, the result repository, the refusal and stale-input paths and the tests against this contract: RWB-S2-E3005-APP.
- The four legacy acceptance criteria of RWB-E3-005: carried verbatim by RWB-S2-E3005-APP; none is repeated or renumbered here.
- The treatment element, the treatment create and read operations and the treatment states: RWB-S2-E3001-APP and the contract of that legacy key.
- The settlement range, the below-floor approval, the offer build and the plan installment range: RWB-S2-E3002-APP, RWB-S2-E3003-APP and RWB-S2-E3004-APP.
- The case, its status and the parent `CaseWorkflow`: rwb-case (P3); the contract declares no case read and no status write.
- The rule package, its authoring, its approval, its effective date and the central ledger: P7 rwb-decision; this contract names the version only.
- The ACE Common restructure calculator — its implementation, its calculations, its availability, its namespace and its deployments: the ACE Common owner and the platform workflow owner (ASM-3071; GAP-1875).
- SCR-14 and SCR-15, their field lists and the gateway-bff composite route: the platform edge story and the screen owners (DP-19).
- The access rule, the roles and the masking: P4 rwb-access and the guard library; the contract declares no right of its own.
- The real cross-service proof of the binding, the record and the screens against the live owners: RWB-ITG-W2, which also owns the `-ITG` copies of the legacy cases.

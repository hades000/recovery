# RWB-S2-E3009-CON Return the case to its prior status on no signature - contract

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E3-009 for rwb-treatment. The contract declares the `PriorStatusRestore` element recorded against the treatment and the two rows the no-signature branch consumes — the case answer of rwb-case carrying the prior status, and the restore operation rwb-integration publishes for the COLLINS and EFS write — and it declares no REST operation of its own on base `/api/recovery/treatment/v1` (DP-13); the record group it names is the local decision record of RWB-PLT-E1027-CON (DP-03); it reads no ACE view (DP-05) and the element is reached by the screens through the gateway-bff composite route (DP-19). It is published on Day 1 at status Draft (realignment v1). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 6 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3009-CON |
| Readiness decisions | RD-P1-004 |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| Contract version | Major version 1 on base /api/recovery/treatment/v1 |
| Open decisions | DL10 stays open; assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 are confirmed by the programme directive |
| Reference data | DP-06 and DP-07; the return-reason vocabulary and the rule version are read under these contracts; parameter names: Not specified in the source documents (DOR-RWB-S2-E3009-CON-20) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register). Aligned the quoted English to Error and Message Standard v6.


### 1. Story

As a **contract owner of rwb-treatment**, I want **the published contract of the no-signature step — the `PriorStatusRestore` element that is recorded against the treatment, the two consumed rows with their request and answer, the return-reason and rule vocabulary of R-RES-17, R-RES-18 and R-RES-20, the rule that no COLLINS status is copied and no case status is owned here, the versioning rule and the fakes — instead of the monolith's in-process method that wrote back to COLLINS from inside the module**, so that **the application story and the wave 2 harness build and test on Day 1 without a COLLINS or EFS connection, and the owner of the two external rows publishes one shape that both sides can test against**.

This is the contract slice of legacy RWB-E3-009. It owns:

- the `PriorStatusRestore` element, its required and optional fields and the rule that it is recorded against the treatment and against nothing else;
- the two consumed rows: the case answer of rwb-case, which carries the case status and the prior status the case held before the restructure, and the restore operation of rwb-integration, with the case ID, the prior status, the return reason and the rule version in the request and the restore reference in the answer;
- the call rules of both rows: one hop each, a 2 s synchronous budget, the retry the workflow applies, and the answer when a row does not reply;
- the rule vocabulary: the return reasons `CUSTOMER_DECLINED` and `OFFER_EXPIRED` of R-RES-17 and R-RES-18, their conditions, and the restart rule R-RES-20 with its event `PRIOR_STATUS_RESTORED`;
- the no-copy rule and the no-status rule: no COLLINS status table and no ACE view is read, and no case status is written by a consumer of this contract;
- the decision-record group of the same transaction, named as the local record of RWB-PLT-E1027-CON, with its refusal and failure messages;
- the compatibility and pinning rule, the fakes and the drift test.

It does not own: the branch of `TreatmentWorkflow`, the activity, the outcome write, the guard paths and the tests against this contract, which are RWB-S2-E3009-APP; the offer and its validity timer, which are RWB-S2-E3007-APP; the signed-offer route, which is RWB-S2-E3008-APP; the treatment read that shows the outcome, which is RWB-S2-E3001-APP; the case, its status and the parent `CaseWorkflow`, which are rwb-case's; the restore operation and the COLLINS and EFS adapters themselves, which are rwb-integration's; the rule package and its version, which are P7 rwb-decision's; and the two screens and their composite route, which are the platform edge story's under DP-19.

### 2. Business rationale

In the monolith the no-signature step wrote back to COLLINS from inside `TdrSettlementAndDeedInLieuService`, through the module's own outbound path, and the FSD records the outcome in a single sentence: "Sends the case back to the status it held in COLLINS when the customer declines or the offer expires" (A2.9.1). The routing logic adds the two rules with their conditions, their reason for leaving the state, and `COLLINS, EFS, Workbench` as the systems column (rows R-RES-17 and R-RES-18). Nothing in that arrangement could be built on its own: the outward write sat inside the same process as the case, the reader of the outcome had only the module's table, and neither side had a written field list.

Two facts of the target force a contract rather than a method. The case status is rwb-case's — a stage reports and the parent applies the rule (Temporal and Drools Design slide 13) — so the outcome of this step has to travel as an element with an agreed shape and not as a status the module sets. And the external estate is reached only through rwb-integration's contract (DP-16), so the COLLINS and EFS write is a consumed row with a request, an answer, a budget and a failure answer, not a method call. The prior status itself is a value the case supplies, which is why the element records it rather than deriving it: a reader must be able to see which status was restored and on which rule version.

**The division of the legacy key is fixed.** This WP delivers the contract. The **application** — the branch, the `restorePriorStatus` activity, the outcome write, the guard paths and the tests — is **RWB-S2-E3009-APP**, and the **four legacy acceptance criteria stay with it** and are not repeated here. The **cross-service proof** is **RWB-ITG-W2**. Every criterion in section 7 of this document is new and tests only the contract deliverable in this title.

What the contract deliberately does not do: it declares no REST path, owns no topic, no task queue and no table, copies no COLLINS status and decides no case status. All four refusals are in section 12 and in section 19.

### 3. Preconditions

- The call type of the outward write is fixed by DP-16: the module boundary of the monolith becomes rwb-integration's contract, one hop, and the external adapter is not one of the 19 services' own surfaces. The FSD names the integration points of the feature as "COLLINS, Workbench" and the routing logic names the systems as "COLLINS, EFS, Workbench".
- The two rules and the restart rule are fixed by the Business Rules and Routing Logic v4, Rules sheet: R-RES-17 from `OFFER_WITH_CUSTOMER` on `CUSTOMER_DECLINED` when `declined = Y`, R-RES-18 from `OFFER_WITH_CUSTOMER` on `OFFER_EXPIRED` when `signed = N and offer_validity passed`, both to `RETURNED_TO_COLLINS`, and R-RES-20 from `RETURNED_TO_COLLINS` on `PRIOR_STATUS_RESTORED` on any condition to `BACK_TO_ROUTE_DECISION`.
- The restore operation name of rwb-integration, its request and answer fields and its error set have no published source: the FSD gives the integration points without an operation, the ownership rows of S2 carry no integration row, and TSD S2 T5.1 lists ALS and NLEADS only. The contract is therefore published as the working read of ASM-4375 (GAP-2663).
- The decision record is the platform library's: `DecisionRecordWriter.record(DecisionRecord)` with `@Transactional(propagation = MANDATORY)`, refusing with MSG-P7-009 and failing with MSG-P7-003 (DP-03; RWB-PLT-E1027-CON).
- The treatment columns that take the outcome exist in TSD S2 T3.1: `outcome` (DF-TRT-013, LOV-TRT-OUTCOME) and `outcome_at` (DF-TRT-014), with `valid_until` (DF-TRT-010) holding the offer end and `signature_status` (DF-TRT-030, LOV-TRT-SIGNATURE) holding the signature state.
- The element is served to the screens through the gateway-bff composite route (DP-19; RWB-PLT-N001-CON), so the contract fixes the element, not a route.
- No build dependency and no approval stop: a CON story is Day 1 by rule (Template and Rules §R5.7) and is published at status Draft (realignment v1; ASM-4378).

### 4. Flow

1. The contract author fixes the `PriorStatusRestore` element: its seven fields, which of them are required, and the rule that it is recorded against the treatment.
2. The author fixes the case row: the case answer carries the case status and the prior status the case held before the restructure, and no consumer reads the case table for them.
3. The author fixes the restore row with rwb-integration: the request, the answer, the 2 s budget, the retry, the failure answer with MSG-GEN-006 and the idempotency key.
4. The author fixes the return-reason vocabulary and the three rule rows, so the recorded reason, the rule condition and the stage report agree.
5. The author writes the no-copy and no-status rules and the decision-record group, and names the two library messages.
6. The author writes the compatibility and pinning rule: what may change inside major version 1 and what raises version 2.
7. The fake set is generated from the document: the case-answer fake, the restore fake, the element fake, the failure answers and the drift fixture.
8. The contract test runs the fakes against the document on every change, and the document and the fakes are published at v1 with RWB-S2-E3009-APP and RWB-ITG-W2 pinning the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A published element drops a required field, or adds an optional one a consumer depends on | The schema check fails the build; required and optional fields are as published | None | AC1 |
| X2 | A row is published without its budget, its retry or its failure answer | The binding lint fails the build; all three are required on both rows | None | AC2 |
| X3 | A document publishes the restore as an exception or as an empty answer | The binding lint fails the build; the failure is a documented answer with MSG-GEN-006 | MSG-GEN-006 | AC2 |
| X4 | A document lets a consumer read a COLLINS status table, an ACE view or the case table | The boundary and drift checks fail the build; the prior status is a field of the case answer only | None | AC4 |
| X5 | A breaking change is made to the element, a row or the failure answer | The change raises major version 2; v1 is never edited in place and stays readable | None | AC5 |
| X6 | A consuming story ships without the drift test, or a fake stops answering the document | The drift test fails the build of the consuming story | None | AC6 |
| X7 | A value a consumer needs is named by no source — the operation name, the exact answer envelope or the prior status field name | The value is published as the working read of the assumption, and the gap stays open | Not specified in the source documents (GAP-2663; ASM-4375) | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document and fakes; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | The field order, the record widths and the fixture set are open until v1 is frozen; the element, the required fields, the two rows, the budget, the failure answer and the three rules are fixed |
| Valuable | Unblocks the application story and the wave 2 harness on Day 1 and gives rwb-integration and rwb-case one shape each to publish against |
| Estimable | One element, two rows, three call rules, one compatibility rule and five fakes |
| Small | One sprint for the document, the fakes and the drift test |
| Testable | Each criterion below is one schema, binding or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: no-signature contract of rwb-treatment

  Background:
    Given the contract document is published with major version 1 on the base of rwb-treatment
    Given the contract declares no REST operation, no topic and no table of its own
    Given the restore row is consumed from rwb-integration and the case row from rwb-case

  Scenario: AC1 The PriorStatusRestore element and its required fields are published (new, D-RCV-60)
    Given the element section of the contract document
    When it is validated and linted
    Then it publishes PriorStatusRestore with priorStatus, returnReason, returnedAt, ruleVersion, offerValidUntil, restoreReference and ruleId
    Then priorStatus, returnReason, returnedAt and ruleVersion are required and offerValidUntil, restoreReference and ruleId are optional
    Then returnReason carries the two rule events CUSTOMER_DECLINED and OFFER_EXPIRED and no other value
    Then offerValidUntil maps to DF-TRT-010 valid_until and the outcome fields of the consumer map to DF-TRT-013 and DF-TRT-014
    Then the element is recorded against the treatment and against no other record, and it has no collection and no free-text field
    Then a document that drops a required field fails the schema check

  Scenario: AC2 The two consumed rows and their call rules are fixed (new, D-RCV-60)
    Given the consumed-rows section of the contract document
    When each row is validated against the platform one-hop conventions
    Then the case row is the case answer of rwb-case carrying the case status and the prior status, with no operation name claimed and no case read of its own
    Then the restore row is one operation of rwb-integration on the COLLINS and EFS write, its name published as the placeholder
    Then each row is one hop with a 2 s synchronous budget and no chain, and the retry is the workflow kit's
    Then when the restore row does not answer, the documented answer is "stage stays in OFFER_WITH_CUSTOMER, nothing written" with MSG-GEN-006
    Then a row published without its budget, its retry or its failure answer fails the lint

  Scenario: AC3 The return reasons and the three rule rows are named without inventing a value (new, D-RCV-60)
    Given the rule section of the contract document
    When it is checked against the routing logic
    Then it names R-RES-17 from OFFER_WITH_CUSTOMER on CUSTOMER_DECLINED when declined = Y to RETURNED_TO_COLLINS
    Then it names R-RES-18 from OFFER_WITH_CUSTOMER on OFFER_EXPIRED when signed = N and offer_validity passed to RETURNED_TO_COLLINS
    Then it names R-RES-20 from RETURNED_TO_COLLINS on PRIOR_STATUS_RESTORED on any condition to BACK_TO_ROUTE_DECISION
    Then it declares no fourth return reason, no threshold and no validity period of its own
    Then a documented reason that is not one of the two rule events fails the lint

  Scenario: AC4 The no-copy rule, the no-status rule and the record group are fixed (new, D-RCV-60)
    Given the data rule and the record group of the contract document
    When the element and the schema are checked together
    Then no COLLINS status table, no ACE view and no case table is declared readable, and the prior status and the restore reference are the only new values recorded
    Then no case status and no stage state is declared writable by a consumer, because both belong to rwb-case
    Then the element and the record are written in one transaction, with ruleId and ruleVersion on the record
    Then a refused record names its field with MSG-P7-009 and a failed one stops the action with MSG-P7-003
    Then decision_log_entry is named only as P7's ledger and is never written or read by the consumer

  Scenario: AC5 Versioning separates a compatible change from a new major version (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published element or row
    Then a backward-compatible change keeps major version 1
    Then a breaking change to the element, a row or the failure answer raises major version 2 and v1 is never edited in place
    Then RWB-S2-E3009-APP and RWB-ITG-W2 pin a published version and raise a change request rather than a private variant

  Scenario: AC6 The fakes answer the document and the drift test holds (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the case-answer fake, the restore fake, the element fake and the drift fixture
    Then the case-answer fake answers OFFER_WITH_CUSTOMER with a prior status, a counter-offer at the same moment and a case answer with no prior status
    Then the restore fake answers a restored status with a reference, a refusal and a timeout inside and beyond the budget
    Then the element fake answers the element of AC1 for each return reason
    Then the drift test fails the build of a consuming story on any difference from sections 12 and 13

  Scenario: AC7 A value no source names is published as the working read with the gap open (new, D-RCV-60)
    Given a consumer needs the operation name, the exact answer envelope or the prior status field name
    When the contract document is checked against the sources
    Then the value is published as the working read of the assumption
    Then GAP-2663 and ASM-4375 stay open and the message reads Not specified in the source documents (GAP-2663; ASM-4375)

  Scenario: AC8 Each business rule BR1 to BR9 in section 8 is checked by a test, or by a guardrail or boundary test where the rule is an architecture constraint (new, D-RCV-60)
    Given the rules BR1 to BR9 in section 8
    When the element, the rows and the record are checked against the rules
    Then each rule is checked by a test, or by a guardrail or boundary test where the rule is an architecture constraint

  Scenario: AC9 The error answers 401, 403 and 404 of the provided operations are published (new, D-RCV-60)
    Given the operations the contract provides
    When the error answers are validated against the contract document
    Then the 401, 403 and 404 answers of each provided operation are published as documented error answers
```

These criteria are new and test only the contract deliverable. No legacy acceptance criterion is repeated here: **AC1 to AC4 of RWB-E3-009 are carried by RWB-S2-E3009-APP**, and every identifier used above comes from the legacy story, the Routing Logic v4 or TSD S2, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The element recorded against the treatment carries the prior status, the return reason, the return time, the rule version, the offer end, the restore reference and the rule ID, and nothing else | RWB-E3-009 AC1; DF-TRT-010; ASM-4375 |
| BR2 | `returnReason` uses the two rule events `CUSTOMER_DECLINED` and `OFFER_EXPIRED`, so the recorded reason and the rule that fired agree | R-RES-17; R-RES-18 |
| BR3 | The prior status is a field of the case answer of rwb-case and is never read from a COLLINS table, an ACE view or the case table | DP-01; DP-05; ASM-4376 |
| BR4 | The outward restore is one hop on rwb-integration's operation inside the 2 s budget; this service owns no external connection and no adapter; the write-back of the prior status to COLLINS is raised through the rwb-integration contract, and P2 owns the interface, its retries and its exception queue | DP-16; ASM-4375; Architecture v5 |
| BR5 | When the restore row does not answer, the stage stays in `OFFER_WITH_CUSTOMER` and the caller sees MSG-GEN-006; no partial restore and no guessed status is recorded | R-RES-17; R-RES-18; ASM-4375 |
| BR6 | No consumer of this contract writes a case status: the stage reports and rwb-case applies R-RES-17, R-RES-18 and R-RES-20 | ASM-4376; Temporal and Drools Design slide 13 |
| BR7 | The element and the record are written in one transaction, through `DecisionRecordWriter` with `MANDATORY` propagation | DP-03; ADR-022; RWB-PLT-E1027-CON |
| BR8 | A published version is never edited: a compatible change stays in major version 1 and a breaking change raises major version 2 | Template and Rules §R7.2; §R5.4 class C |
| BR9 | The rule version that decided is the version recorded on the element and on the record; no rule ID, state name, reason code, validity period or timer value is a document constant | EV-30; BR-S2-009 of FSD A2.9.3.1 |

### 9. State transitions

None of the case statuses are this contract's, and a document has no runtime state of its own. The table fixes the outcomes the contract names so that a consumer cannot invent a fourth.

| Object | State | Meaning in the contract |
|---|---|---|
| Restore row | Restored | The adapter answered inside the budget with the prior status and a restore reference; the element is recorded and the stage reports `RETURNED_TO_COLLINS` |
| Restore row | Refused | The adapter answered a refusal with its reason; nothing is recorded and the stage stays where it was |
| Restore row | Not answered | No answer inside the budget after the retries; nothing is written, the stage stays in `OFFER_WITH_CUSTOMER`, MSG-GEN-006 |
| Case row | Prior status present | The stage proceeds and records the prior status |
| Case row | Prior status absent | The stage does not invent one; it reports the gap and keeps the case where it is |
| Element | Recorded | Written against the treatment in the same transaction as the record and the stage report |
| Element | Absent | The transaction rolled back, or a row did not answer; there is no partial element |
| Contract version | v1 | The published version every consuming story pins |
| Contract version | v2 | Raised by a breaking change; v1 stays readable and is never edited |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document and the fakes |
| The service owner of rwb-treatment | Approves a breaking change and freezes a version |
| The rwb-integration owner | Publishes the restore operation, its answer and its error set; confirms them at the wave 2 contract freeze (ASM-4375) |
| The rwb-case owner | Confirms the case answer that carries the prior status and the status column of the three rules (ASM-4376) |
| RW-RESTRUCT, restructuring officer (FCR) | Consumes the outcome through the screens and holds right R on the capability area; the step itself runs unattended under the service identity |
| P7 rwb-decision | Owns the RESTRUCTURE package and its version, which the element and the record name |
| RW-AUDIT, RW-COE | Read the recorded outcome and the decision records; they do not consume this document directly |
| No delegation of authority level applies | A contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in the document, an example or a fake; where an actor must be named, a role code or a service identity is used.

The authorise check on the consumed operations is the rwb-access check of DP-08; this contract declares no authorise check of its own.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The document publishes field names, one vocabulary, the budget and the messages; no customer, account, case or status value appears |
| Element published | The seven fields of section 12.1, with the required and optional flags and the two treatment columns they map to |
| Personal data | None. The requests carry the case ID, the prior status, a reason code and the rule version; no name, national identifier, account number or document content |
| Tables published | None. The consumer writes the element against `treatment` in `rwb_treatment`; `decision_record` is the platform library object of DP-03, named in neither LDM v9 nor Data Classification v5 as a field or entity |
| Field identifiers | DF-TRT-010 for the offer end and DF-TRT-013 and DF-TRT-014 for the outcome; the element's own identifiers are Not specified in the source documents (GAP-2663; GAP-2664; ASM-4377) |
| Retention | The element is kept with the treatment row for the life of the case record; the retention period of the outcome is Not specified in the source documents (GAP-2663; ASM-4375) |
| BR Field ID | Not specified in the source documents (DOR-RWB-S2-E3009-CON-7) for the six rows above; the Data owner allocates the element's BR Field IDs at the wave 2 contract freeze, the service owner names the publication channel, and the rwb-integration and rwb-case owners publish the operation names and error sets (GAP-2664) |

The element is the one place where a COLLINS status could leak into the service's schema, so the document fixes that it carries the restored status as a value with its reason and its rule version only: no copy of a COLLINS status table, no account state and no free-text reason.

### 12. Contract

#### 12.1 REST operations provided

None. This contract declares no REST operation, adds no path to base `/api/recovery/treatment/v1` and publishes no OpenAPI document (DP-13). The two screens that show the recorded outcome reach it through the gateway-bff composite route and the sibling treatment read, and neither is declared here (DP-19).

**Element: `PriorStatusRestore`**

| Field | Type | Required | Maps to | Note |
|---|---|---|---|---|
| `priorStatus` | string | Yes | No treatment column | The status the case held before the restructure, as the case answer supplies it |
| `returnReason` | enum `CUSTOMER_DECLINED`, `OFFER_EXPIRED` | Yes | The event of R-RES-17 and R-RES-18 | The vocabulary is the rule's own, so the recorded reason and the rule that fired agree |
| `returnedAt` | timestamptz | Yes | DF-TRT-014 `outcome_at` | When the branch recorded the return |
| `ruleVersion` | string | Yes | The version group of the decision record | The version of the RESTRUCTURE package in force when the rule fired |
| `offerValidUntil` | date | No | DF-TRT-010 `valid_until` | The date the offer ended; present on the expiry branch where the validity date was set |
| `restoreReference` | string | No | No treatment column | The adapter's reference for the restore; absent when the adapter answered without one |
| `ruleId` | string | No | No treatment column | Present when the branch reports a rule of its own, which is R-RES-17 or R-RES-18 where the answer names it |

The element is recorded against the `treatment` row and against no other record; it has no collection and no free-text field. Its own BR Field IDs have no row in the Logical Data Model, so the field names are the working read of ASM-4377 and their identifiers are the placeholder of GAP-2663 and GAP-2664.

#### 12.2 REST operations consumed

| Row | Owner | Request | Answer | Budget and failure |
|---|---|---|---|---|
| Case answer carrying the prior status | rwb-case (P3) | The case ID | The case status, the prior status the case held before the restructure and the event on the signal | One hop, 2 s; a case answer with no prior status stops the branch (MSG-GEN-006) |
| Restore operation on the COLLINS and EFS write | rwb-integration (P2) | The case ID, the prior status, the return reason and the rule version; an idempotency key | The restored status and the restore reference | One hop, 2 s; on exhausted retries the stage stays in `OFFER_WITH_CUSTOMER` with MSG-GEN-006 |

Neither operation name is published in a source: the FSD gives the integration points as "COLLINS, Workbench" with no operation, the ownership rows of S2 name no consumed operation, and TSD S2 T5.1 lists ALS and NLEADS only. The names are therefore published as the placeholder of ASM-4375 (GAP-2663), and both rows are faked in every test. Because this legacy key's plan row carries no class C dependency, the rows are built against the documented use of this section and their fakes, and the two owners confirm them at the wave 2 contract freeze.

#### 12.3 Events published

None. This contract owns no topic and publishes no event; the service's topic `rwb.treatment.events.v1` and its event EV-10 `TreatmentApproved` belong to the offer story of this service (DP-14). The outcome is not announced on Kafka: it is recorded and read.

#### 12.4 Events consumed

None by this contract. The consumer's rule package arrives on `rwb.decision.RulePackageInForce.v1` from P7 (EV-30), which is the application story's subscription and the service template's rule loader; the contract only requires that the element and the record name the version that was in force.

#### 12.5 Workflows and activities

None of its own: the contract defines no workflow, no activity and no task queue. What it does fix is the two rows the consumer's activity and workflow read, so that both sides of each wire are written down in one place.

| Row element | Value |
|---|---|
| Case row type | The case answer the parent `CaseWorkflow` forwards to the child on the case signal, not a REST read and not a table read |
| Case row content | Case ID, case status, the prior status held before the restructure, the event |
| Restore row call type | One hop from an activity on task queue `rwb-treatment` in namespace `rwb-recovery` |
| Restore row request | `caseId`, `priorStatus`, `returnReason`, `ruleVersion`; no personal data, no document and no free text |
| Restore row answer | The restored status and the restore reference |
| Budget | 2 s synchronous on each row |
| On timeout | The activity answers a timeout; the workflow retries per the kit (1 s initial interval, back-off 2, 10 attempts) |
| On exhausted retries | The documented answer is the stage stays in `OFFER_WITH_CUSTOMER`, nothing is written, the caller sees MSG-GEN-006 |
| Idempotency | The restore request carries an idempotency key of the case ID and the rule version, so a replay never restores twice |
| Second operation | None |

#### 12.6 Schedules

None. The contract declares no Schedule; the offer validity clock is the consumer's durable timer, started by RWB-S2-E3007-APP, and is not part of this document.

#### 12.7 Tables owned

None. The element is written by the consumer against `treatment` in `rwb_treatment`, a table of this service created on its own Flyway sequence, and `decision_record` is the platform library object of DP-03 applied in the same schema. The contract creates no table, declares no column and adds no foreign key; the case table of rwb-case and any store of the adapter are never named, and `decision_log_entry` is P7's ledger in `rwb_decision`, named only.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Case-answer fake | The case row of AC2 | `OFFER_WITH_CUSTOMER` with a prior status; a case that counters at the same moment; a case answer with no prior status |
| Restore fake | The restore row of AC2 | A restored status with a reference; a refusal with its reason; an answer with no reference; a timeout inside the 2 s budget and one beyond it |
| Element fake | The `PriorStatusRestore` shape | A complete element for each return reason; one element per missing required field; an element with and without `ruleId` |
| Output fake | The failure answer | The documented timeout answer with MSG-GEN-006 and the missing-prior-status answer |
| Drift fixture | The contract test | One accepted and one refused body per section of the document |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consuming story rather than as a surprise at run time. The restore fake is what makes Day 1 possible for RWB-S2-E3009-APP and RWB-ITG-W2.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 2 rows declared: the rwb-case case answer and rwb-integration's restore operation | Neither name is published; one hop and 2 s each; faked in every test |
| Kafka | 0 | 0 | The consumer's package subscription is the application story's; no topic is declared here |
| Temporal | 0 | 0 | The contract declares no workflow and no activity; the consumer's child workflow runs on `rwb-treatment` |
| Nexus | 0 | 0 | No namespace is entered from this key |
| File | 0 | 0 | No file crosses the contract |

### 13. Solution plan

**Package.** Contract artefact of rwb-treatment: the element and the two row records in `th.co.scb.ace.workbench.recovery.treatment.api`, the fakes as a test resource, and the versioning rule in the contract document. The implementation that reads the rows is RWB-S2-E3009-APP. The artefact coordinates and the publication channel are Not specified in the source documents (GAP-2664; ASM-4377).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is the rule this contract writes down as a prohibition: no ACE view and no COLLINS table is declared readable, and the prior status is a field of the case answer. DP-03 is the record group the element is written with; DP-13 fixes the base this contract declares nothing on; DP-19 is how the recorded outcome reaches SCR-14 and SCR-15.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `PriorStatusRestore` | Published type | The seven fields, the required and optional flags and the recording rule (BR1, BR2) |
| `CaseAnswer`, `RestorePriorStatusRequest`, `RestorePriorStatusResponse` | Published types | Both sides of each row, with the prior status and the reason (BR3, BR4) |
| `ReturnReasonVocabulary` | Published type | The two rule events and their conditions, with no fourth value (BR2, AC3) |
| `NoCopyAndNoStatusRule` | Document | The ban on reading a COLLINS status, an ACE view or the case table and on writing a case status, with the record group (BR5, BR6, BR7) |
| `VersioningSpecification` | Document | Major version 1, the compatible versus breaking rule and the pinning rule (AC5) |
| Fake set and drift fixture | Test asset | The case-answer, restore, element and output fakes and the drift test every consuming story runs (AC6) |

**Database.** No table and no column in this contract. The outcome lands in `treatment.outcome` (DF-TRT-013) and `treatment.outcome_at` (DF-TRT-014), the offer end is `treatment.valid_until` (DF-TRT-010), all defined by TSD S2 T3.1; the prior status and the restore reference have no column and no field ID yet, which is why they are published as an element (GAP-2663).

**Configuration and reference data.** The restore operation name, its shape and the 2 s budget are configuration of the row and are confirmed at the wave 2 contract freeze. The return reasons are the rule events of R-RES-17 and R-RES-18 and are not a list this contract invents. The rule package and its version are P7's data.

**Build steps**

1. Write the element with its seven fields and the required and optional flags; validate it against the schema check (AC1).
2. Write the two rows with their request, answer, budget, retry and failure answer; lint them against the platform one-hop conventions (AC2).
3. Write the return-reason and rule section against the routing logic rows, with no fourth value (AC3).
4. Write the no-copy, no-status and record-group rules; lint the record against the library contract (AC4).
5. Write the versioning and pinning section with the compatible and breaking examples (AC5).
6. Generate the fake set and the drift fixture, and wire the drift test into the build of RWB-S2-E3009-APP (AC6).
7. Publish v1 and record the pinned version of RWB-S2-E3009-APP and RWB-ITG-W2.

**Feature flag.** `rwb.treatment.return-to-collins-contract`.

**Done when.** The document and its schema validate, the row lint and the no-copy and no-status checks are green, the four fakes answer every criterion including the timeout and the missing prior status, the drift test fails on an edited field and passes on the published version, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-GEN-006 | A row does not answer inside the budget after the retries, or the case carries no prior status | {system} is not available. Try again in a few minutes. | The documented failure answer of the row group |
| MSG-S2-003 | The offer is with the customer and its validity date is set | The offer to the customer ends on {date}. | The information the element's `offerValidUntil` supports |
| MSG-P7-009 | A record is refused for a missing or invalid field | The decision record was refused: {field} is missing or not valid. | The library's refusal, named by the record group |
| MSG-P7-003 | The record cannot be written and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The library's failure, named by the record group |

The four texts are copied unchanged from RWB-E3-009 and RWB-PLT-E1027-CON, and this contract adds no message ID and no text. The element declares no message of its own: a refused element is a library refusal with its field name, and a missing answer is the row's failure answer. Thai text follows decision DL10.

### 15. Screens and states

No screen in this story, and the contract declares none. The element is shown on SCR-14 Treatment record and SCR-15 Settlement offer, which are reached through the gateway-bff composite route (DP-19) and whose field lists belong to the platform edge story and the screen owners. The contract fixes what those screens may show of the outcome: the prior status, the return reason, the return time, the offer end and the restore reference, and no COLLINS status table and no account state.

SCR-14 states (empty, loading, error, no access): Not specified in the source documents (CG-ALL-8612). SCR-15 states (empty, loading, error, no access): Not specified in the source documents (CG-ALL-8613).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S2-E3009-CON-01 | AC1 | Contract | The element schema: the seven fields, the required and optional flags, the mapping to DF-TRT-010, DF-TRT-013 and DF-TRT-014; one element per missing required field refused |
| TC-S2-E3009-CON-02 | AC2 | Contract | The two rows linted: the case answer with the prior status and the restore request and answer; a row without its budget, its retry or its failure answer refused |
| TC-S2-E3009-CON-03 | AC3 | Contract | The three rule rows and the two return reasons checked against the routing logic; a documented fourth reason refused |
| TC-S2-E3009-CON-04 | AC4 | Component | The no-copy and no-status checks on the schema; the record group in one transaction with MSG-P7-009 and MSG-P7-003 |
| TC-S2-E3009-CON-05 | AC5, AC6 | Component | A compatible and a breaking change on the element and the rows; the four fakes and the drift fixture, green on the published version and red on an edited field |
| TC-S2-E3009-CON-06 | AC7 | Contract | A value named by no source published as the working read; GAP-2663 and ASM-4375 stay open and the message is shown |
| TC-S2-E3009-CON-07 | AC8 | Contract | The nine rules BR1 to BR9 checked against the element, the rows and the record; a rule that is an architecture constraint checked by the boundary test |
| TC-S2-E3009-CON-08 | AC9 | Contract | Not specified in the source documents (NEWAC-RWB-S2-E3009-CON-AC9) |

The legacy test set of RWB-E3-009 — TC-E3-009-01 to TC-E3-009-06 — is carried by RWB-S2-E3009-APP and by the wave 2 integration harness, and no legacy id is renumbered here. These five are the contract's own tests.

### 17. Guardrails

- No business value in the contract: the return reasons are the rule events of R-RES-17 and R-RES-18, the dates and outcome columns are TSD S2 T3.1 fields, and no threshold, validity period or reason beyond the two is fixed here.
- No personal data in the element, a request, an answer, a fake or a log: the requests carry the case ID, the prior status, a reason code and the rule version only.
- No copy of COLLINS data and no ACE read: no COLLINS status table and no `v_ace_*` view is declared readable (DP-05; BR3).
- No case status written by a consumer: the stage reports and rwb-case applies the rule (BR6).
- No REST surface, no topic and no table of the contract's own: the base is fixed by DP-13 and the contract declares nothing on it.
- No second operation and no second external connection: one restore row on rwb-integration's contract.
- The outcome of a missing answer is a written answer, never an exception a consumer has to guess: MSG-GEN-006 and the stage stays where it is.
- A published version is never edited in place: a breaking change raises major version 2 with a new version label and a migration note, and a consumer pins rather than forks.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| Not specified in the source documents (GAP-2663; ASM-4375) | A declined or lapsed offer returns the case to the status it held in COLLINS, and the return is recorded with its rule version | Pending (C1) | FEAT-TRT-09 | 07 Route, settle and claim | R-RES-17; R-RES-18; R-RES-20 | TC-S2-E3009-CON-01, TC-S2-E3009-CON-02, TC-S2-E3009-CON-04 |
| Legacy test set RWB-E3-009 | TC-E3-009-01, TC-E3-009-02, TC-E3-009-03, TC-E3-009-04, TC-E3-009-05, TC-E3-009-06 | Pending (C1) | FEAT-TRT-09 | 07 Route, settle and claim | R-RES-17; R-RES-18 | Executed by RWB-S2-E3009-APP and the wave 2 integration harness; not owned here |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3009-APP | App development | H consumer: implements the branch, the activity, the outcome write and the guard paths against this contract and its fakes; owner of the four legacy acceptance criteria |
| RWB-PLT-E1027-CON | Contract | Referred to: the local decision-record library and its two messages that the record group names. This contract adds no build dependency of its own |
| RWB-PLT-N001-CON | Contract | Referred to: the gateway-bff composite route that shows the element on SCR-14 and SCR-15 |
| RWB-S2-E3001-APP | App development | Sibling: the treatment read that returns the recorded outcome |
| RWB-S2-E3007-APP, RWB-S2-E3008-APP | App development | Siblings: the offer and its validity timer, and the signed-offer route, which are the two other outcomes of the same state |
| P3 rwb-case | Service | The case answer that carries the prior status and the status column of R-RES-17, R-RES-18 and R-RES-20 (ASM-4376) |
| P2 rwb-integration | Service | The restore operation and the COLLINS and EFS adapters this contract binds (DP-16) |
| RWB-ITG-W2 | Integration | I: the cross-service proof of the two rows and the record against the live owners, and the owner of the legacy `-ITG` copies |

### 19. Out of scope

- The branch of `TreatmentWorkflow`, the `restorePriorStatus` activity, the outcome write, the guard paths and the tests against this contract: RWB-S2-E3009-APP.
- The four legacy acceptance criteria of RWB-E3-009: carried verbatim by RWB-S2-E3009-APP; none is repeated or renumbered here.
- The offer, its validity timer and the signed-offer route: RWB-S2-E3007-APP and RWB-S2-E3008-APP.
- The treatment element, the treatment create and read operations and the treatment states: RWB-S2-E3001-APP and the contract of that legacy key.
- The case, its status, the prior status value and the parent `CaseWorkflow`: rwb-case (P3); the contract declares no case read of its own and no status write.
- The rule package, its authoring, its approval, its effective date and the central ledger: P7 rwb-decision; this contract names the version only.
- The restore operation, the COLLINS and EFS adapters, their availability and their retry: rwb-integration (P2) and its own contract (GAP-2663).
- SCR-14 and SCR-15, their field lists and the gateway-bff composite route: the platform edge story and the screen owners (DP-19).
- The access rule, the roles and the masking: P4 rwb-access and the guard library; the contract declares no right of its own.
- The real cross-service proof of the two rows and the record against the live owners: RWB-ITG-W2, which also owns the `-ITG` copies of the legacy cases.

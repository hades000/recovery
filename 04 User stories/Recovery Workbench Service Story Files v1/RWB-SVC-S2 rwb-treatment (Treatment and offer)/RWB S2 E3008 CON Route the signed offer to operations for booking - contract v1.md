# RWB-S2-E3008-CON Route the signed offer to operations for booking - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E3-008 for rwb-treatment (S2, Treatment and offer). This document publishes the `SignedOfferHandover` element — the result of the signed branch of `TreatmentWorkflow` that carries a signed offer to operations — with its eleven properties, its mapping to the `treatment` field set of TSD S2 T3.1, the rule that the five facts without a column are recorded on the decision record, the two `toState` values taken from the rules R-RES-16 and R-SET-10, the validation, the versioning rule and the fakes; it publishes no REST path of its own, names the two legacy operations as RWB-S2-E3001-CON's, writes through the library of RWB-PLT-E1027-CON (DP-03), reads ACE facts only through their owner where a step needs them (DP-05) and serves the screen through the gateway-bff composite route (DP-19). The legacy acceptance criteria stay with RWB-S2-E3008-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3008-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-008 |
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

As a **contract owner of rwb-treatment**, I want **the published hand-over of a signed offer to operations — the `SignedOfferHandover` element, its properties mapped to the `treatment` field set, the rule for the facts that have no column, the two target states of R-RES-16 and R-SET-10, the validation, the versioning rule and the fakes — instead of the monolith's single write to the case status**, so that **the signed path, the operations step, the settlement instruction and the wave 2 integration harness build against one frozen element from Day 1, and no service invents a second shape for the same hand-over**.

The contract covers exactly five things:

- the `SignedOfferHandover` element and its eleven properties, published as the result of the signed branch of `TreatmentWorkflow`, the stage child of `CaseWorkflow` that rwb-treatment runs on task queue `rwb-treatment` (TSD S2 T0.1 and T5.2.1; ASM-4371);
- the mapping of those properties to the `treatment` field set of TSD S2 T3.1, and the rule that the five facts without a column — `signedAt`, `toState`, `paymentInstructionRequired`, `ruleId` and `ruleVersion` — are carried on the element and recorded on the decision record, never stored (GAP-2662; ASM-4371);
- the two `toState` values, WITH_OPS_BOOKING and WITH_OPS_SETTLEMENT, taken character for character from the rules R-RES-16 and R-SET-10 and read at run time from the package in force, never written as constants (Rules v4 rows R-RES-16, R-SET-10; TSD S2 T4);
- the validation and the refusal set: a signature status other than SIGNED, a treatment type outside LOV-TREATMENT, a property outside its domain, a `toState` the contract does not publish, and an instruction flag that contradicts the route (ASM-4371);
- the versioning rule and the fakes, so that the signed path, the parent stage contract, the settlement instruction and the integration harness pin v1 and raise a change request rather than a private variant.

It does not own: the signed branch of the workflow, the signature write, the rule evaluation and the record write, which are RWB-S2-E3008-APP; the treatment entity and the two operations the legacy story lists, which are RWB-S2-E3001-CON; the offer and its clock, which are RWB-S2-E3002-APP, RWB-S2-E3004-APP and RWB-S2-E3007-APP; the case status and the operations queue, which are rwb-case's (ASM-4373); the settlement instruction record, which is rwb-payment's (ASM-4374); the decision-record library, which is RWB-PLT-E1027-CON; and the screens, which are the platform edge story's and the screen owners' (DP-19).

### 2. Business rationale

The signed offer is where a restructure or a settlement stops waiting on the customer and starts moving to booking, and the feature that owns the moment is measured by restructure turnaround of 5 days against today's 23 to 26 days tracked by hand, with the rule giving the step one working day (FSD S2 v4, section A2.8.1; Rules v4 rows R-RES-16 and R-SET-10). REQ-S2-003 makes that moment a requirement: a signed offer routes to operations for booking, and an unsigned or declined offer returns the case to its prior status. The step runs unattended, so there is no screen and no person to absorb an ambiguity: the hand-over has to be one shape, or three consumers drift.

In the monolith the hand-over was one field on one row: `recovery_case.status` moved to WITH_OPS_BOOKING or WITH_OPS_SETTLEMENT, and the settlement instruction was raised in the same process. The target splits it four ways. The case state is rwb-case's (DP-01; ASM-4373); the treatment and its `signature_status` are rwb-treatment's (TSD S2 T3.1); the rule that chooses the route is data of the package in force (BR-S2-008); and the settlement instruction is rwb-payment's, with no published operation naming it (ASM-4374). What is missing in every source is the shape of the thing that travels between them — and that is the one artefact that all four consumers need before any of them can build.

Two facts make the contract urgent rather than tidy. The first is that TSD S2 T3.1 has `signature_status` and no signed-at column, no route column and no instruction column, while the routing rules need a signature time, a target state, an instruction flag and the rule version that produced them: if that is left to implementers, one team stores them, one team hard-codes them and the rule version becomes unprovable, which contradicts BR-S2-008 and AC1. The contract therefore fixes them as request-context facts recorded on the decision record (GAP-2662; ASM-4371). The second is the missing path: the legacy endpoint table publishes only the treatment create and read, and no source publishes a signature path or a hand-over path, so the contract binds the element to the workflow result that the TSD already names and invents no operation (GAP-2662; TSD S2 T5.2.1).

The fake is the Day-1 unblocker: the signed path, the parent stage contract, the settlement instruction and the integration harness can build and test the two routes, the four signature states and the refusals before rwb-document, rwb-payment or rwb-case exist in an environment (Template and Rules §R5.4 class C, §R5.7).

### 3. Preconditions

- The mapped fields are fixed by TSD S2 T3.1: `id` (DF-TRT-001, uuid), `case_id` (DF-TRT-002, uuid), `treatment_type` (DF-TRT-004, varchar(20), LOV-TREATMENT), `signature_status` (DF-TRT-030, varchar(12), LOV-TRT-SIGNATURE), `valid_until` (DF-TRT-010, date) and `offer_amount` (DF-TRT-007, numeric(18,2)), on `treatment` in schema `rwb_treatment`, owned by S2 (DP-01).
- The two routing rules and their target states are fixed by the rules in force: R-RES-16 on `OFFER_WITH_CUSTOMER` with `CUSTOMER_SIGNED` and condition `signed = Y and signature verified`, action "Route the case to operations to complete the booking", target `WITH_OPS_BOOKING`, timer 1 working day; R-SET-10 on `OFFER_WITH_CUSTOMER_SET` with `CUSTOMER_SIGNED` and condition `signed = Y`, action "Route the case to operations and raise the payment instruction", target `WITH_OPS_SETTLEMENT`, timer 1 working day (Rules v4; TSD S2 T4).
- The workflow that returns the element exists and is the stage child of the case: `TreatmentWorkflow`, on task queue `rwb-treatment` in namespace `rwb-recovery`, called by P3 rwb-case (TSD S2 T0.1 and T5.2.1).
- The two legacy operations are another contract's: `POST /cases/{caseId}/treatments` and `GET /treatments/{treatmentId}` on base `/api/recovery/treatment/v1`, declared by RWB-S2-E3001-CON (DP-13; TSD S2 T-A.1).
- No source defines the hand-over element, defines a signature path, or names a settlement instruction operation; the element and its rules are this contract's working read, published with the gap and the assumption (GAP-2662; ASM-4371, ASM-4374).
- The decision record is written through RWB-PLT-E1027-CON with `@Transactional(propagation = MANDATORY)`, refusing with MSG-P7-009 and failing with MSG-P7-003; `decision_record` is a library object in `rwb_treatment` and `decision_log_entry` is P7's (DP-03, DP-01).
- The gateway-bff composite route of RWB-PLT-N001-CON exists, so the screens' binding to the element is named and not declared here (DP-19).
- The access rule is the platform guard library's: capability area "Treatment and offer", right R for the read of the signed treatment, with RW-RESTRUCT holding CRUA and RW-CASEOWN CRU (TSD S2 T6.1).
- The two legacy message texts this element raises are kept unchanged: MSG-GEN-001 and MSG-P4-002, with MSG-P7-003 and MSG-P7-009 for the record path.
- No build dependency and no approval stop: a CON story is Day 1 by rule (Template and Rules §R5.7) and is published at status Draft (realignment v1).

### 4. Flow

1. The contract author fixes the element: `SignedOfferHandover` with its eleven properties, their types taken from TSD S2 T3.1 where a column exists, and nothing else.
2. The author fixes the mapping: six properties map to a `treatment` field and five are request-context facts, and the row for each names its field identifier or states that it has none.
3. The author writes the record-home rule: the five facts without a column are recorded on the decision record with the rule ID and version, and `treatment` gains no column for any of them.
4. The author writes the two `toState` values and the instruction rule: `WITH_OPS_BOOKING` with `paymentInstructionRequired = false` on R-RES-16, `WITH_OPS_SETTLEMENT` with `paymentInstructionRequired = true` on R-SET-10, both read from the package in force.
5. The author writes the validation and the refusal set with the field names and the message identifiers, and states that the element adds no REST path and no error code of its own.
6. The author writes the versioning and pinning section: major version 1, the compatible-versus-breaking rule and the pinning obligation of the four consumers.
7. The schema and lint steps run: the element validated against the type set, the example scanned for personal data, a `toState` outside the two values refused, and a migration set that carries no column for the five facts.
8. The fake set is generated from the same example set: the hand-over fake, the decision-record fake, the case-status mock, the route fake and the signature fixture.
9. The drift test runs the fakes against the document on every change and fails the build on any difference.
10. The document and the fakes are published at v1, and RWB-S2-E3008-APP, the parent stage contract, the settlement instruction and the wave 2 integration harness pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The element is published without one of its required properties, or with a property that is not in the set | The schema validation fails the build; the element holds exactly eleven properties and the required set is fixed | None | AC1, AC2 |
| X2 | A migration adds a column for `signedAt`, `toState`, `paymentInstructionRequired`, `ruleId` or `ruleVersion` | The schema lint and the drift test fail the build; the five facts live on the decision record | None | AC3 |
| X3 | `toState` carries a value other than the two the rules state, or the instruction flag contradicts the route | The element is refused with the field named and nothing is handed over | MSG-GEN-001 | AC4, AC5 |
| X4 | `signatureStatus` is other than SIGNED, or `treatmentType` is outside LOV-TREATMENT | The element is refused with the field named; the signed path hands over nothing | MSG-GEN-001 | AC5 |
| X5 | The element is published on a REST path of its own, or a second hand-over shape appears | The lint fails the build; the element is the workflow result and the two operations stay RWB-S2-E3001-CON's | None | AC1, AC6 |
| X6 | A breaking change is made to a property, a required rule, the column rule, a `toState` value or the instruction rule | The change raises major version 2; v1 is never edited in place and stays readable | None | AC6 |
| X7 | A consuming story ships without the drift test, or a schema change breaks a consumer | The drift test fails the build of that consumer and the registry refuses the change | None | AC7 |
| X8 | A value the consumers need is named by no source — the element shape, the five facts, or the settlement instruction | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-2662; ASM-4371) | Section 3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document and a fake set; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | The example values, the property order and the description texts are open until v1 is frozen; the eleven properties, the required set, the no-column rule, the two `toState` values and the instruction rule are fixed |
| Valuable | Unblocks the signed path, the parent stage contract, the settlement instruction and the integration harness with one hand-over element on Day 1 |
| Estimable | One element, one mapping section, one record-home rule, one validation section, one versioning rule and five fakes |
| Small | One sprint for the document, the schema, the fakes and the drift test |
| Testable | Each criterion below is one schema, lint or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Signed offer hand-over contract

  Background:
    Given the rwb-treatment contract document is published at major version 1
    Given the treatment table carries the 33 fields of TSD S2 T3.1 in schema rwb_treatment
    Given the hand-over is the result of the signed branch of TreatmentWorkflow and declares no path of its own

  Scenario: AC1 The SignedOfferHandover element is published as the stage result (new, D-RCV-60)
    Given the element section of the contract document
    When it is validated and linted
    Then it publishes SignedOfferHandover with exactly eleven properties: treatmentId, caseId, treatmentType, signatureStatus, signedAt, validUntil, offerAmount, toState, paymentInstructionRequired, ruleId and ruleVersion
    Then the element is the result of TreatmentWorkflow on task queue rwb-treatment in namespace rwb-recovery, the stage child that CaseWorkflow of rwb-case starts, and this contract publishes no REST path and no operation
    Then the two operations of the legacy endpoint table, POST /cases/{caseId}/treatments and GET /treatments/{treatmentId} on base /api/recovery/treatment/v1, are named as RWB-S2-E3001-CON's and are not redeclared
    Then the document records that no source publishes a signature path or a hand-over path, and that none is invented
    Then the access of the read is capability area Treatment and offer with right R, checked by the platform guard library and declared here as the right only

  Scenario: AC2 Every property maps to the treatment field set or to the decision record (new, D-RCV-60)
    Given the element section and the treatment field set of TSD S2 T3.1
    When every property is compared to its column and to its type
    Then treatmentId is required and maps to DF-TRT-001 id, uuid
    Then caseId is required and maps to DF-TRT-002 case_id, uuid
    Then treatmentType is required and maps to DF-TRT-004 treatment_type, varchar(20), LOV-TREATMENT
    Then signatureStatus is required and maps to DF-TRT-030 signature_status, varchar(12), LOV-TRT-SIGNATURE
    Then validUntil is optional and maps to DF-TRT-010 valid_until, date, and offerAmount is optional and maps to DF-TRT-007 offer_amount, numeric(18,2)
    Then signedAt, toState, paymentInstructionRequired, ruleId and ruleVersion are required and map to no column
    Then no property without a mapping beyond the five request-context facts is published, and the required set is named as the working read of GAP-2662 and ASM-4371

  Scenario: AC3 The five request-context facts are recorded and gain no column (new, D-RCV-60)
    Given the record-home section of the document and the DDL of treatment
    When the element, the decision record and the migration set are compared
    Then signedAt, toState, paymentInstructionRequired, ruleId and ruleVersion are recorded on the decision record of the apply transaction with the rule version
    Then treatment has no column for any of the five and no migration in rwb_treatment adds one
    Then no value of the five is published as a constant, a default or a reference-data row of this contract
    Then an element or a migration that stores one of the five fails the schema lint and the drift test

  Scenario: AC4 The two target states are the rules' own and the instruction flag follows the route (new, D-RCV-60)
    Given the route section of the document and the rules R-RES-16 and R-SET-10
    When the two routes are compared to the rules in force
    Then toState carries WITH_OPS_BOOKING with paymentInstructionRequired false on R-RES-16, the restructure route
    Then toState carries WITH_OPS_SETTLEMENT with paymentInstructionRequired true on R-SET-10, the settlement route
    Then both values are read at run time from the package in force announced by rwb.decision.RulePackageInForce.v1 and are written as no constant
    Then ruleId and ruleVersion carry the rule that fired and the version in force, so that the hand-over proves which version produced the route
    Then the settlement instruction itself is not published here: the element flags it and rwb-payment raises it

  Scenario: AC5 The validation and the refusal set are published (new, D-RCV-60)
    Given the validation section of the document
    When an element is validated against it
    Then a missing required property is refused with MSG-GEN-001 and the field name, before any hand-over
    Then a signatureStatus other than SIGNED is refused with MSG-GEN-001 and the field name
    Then a treatmentType outside LOV-TREATMENT is refused with MSG-GEN-001 and the field name
    Then a toState other than the two published values, and an instruction flag that contradicts the route, are refused with MSG-GEN-001 and the field name
    Then a signedAt after validUntil is refused with MSG-GEN-001 and the field name
    Then the element adds no HTTP status code and no error envelope of its own, and the record path fails with MSG-P7-003 and refuses with MSG-P7-009

  Scenario: AC6 Versioning separates a compatible change from a new major version (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published property or rule
    Then an added optional property keeps major version 1 and is accepted by the registry in BACKWARD mode
    Then a change to a property name, a type, a required rule, the no-column rule, a toState value or the instruction rule raises major version 2, and v1 is never edited in place
    Then RWB-S2-E3008-APP, the parent stage contract, the settlement instruction and the wave 2 integration harness pin a published version and raise a change request rather than a private variant

  Scenario: AC7 The fakes answer the document and the drift test fails on any difference (new, D-RCV-60)
    Given the fake set generated from the same example set as the document
    When the contract test runs the hand-over fake, the decision-record fake, the case-status mock, the route fake and the signature fixture
    Then the hand-over fake answers a complete booking hand-over, a complete settlement hand-over, an element missing a required property and an element with an unpublished toState
    Then the decision-record fake answers an accepted record, a refusal with MSG-P7-009 and a failure with MSG-P7-003, and the case-status mock answers OFFER_WITH_CUSTOMER and OFFER_WITH_CUSTOMER_SET
    Then the route fake answers the two screen reads one hop each, and the signature fixture answers signed and verified, signed and not verified, not signed, and a signature after the validity date
    Then the drift test of every consuming story fails the build on any difference from section 12 and section 13
```

These criteria are new: no legacy acceptance criterion is repeated here — **AC1 to AC4 of RWB-E3-008 stay with RWB-S2-E3008-APP** — and every identifier comes from the legacy story, the TSD, the FSD or the Business Rules and Routing Logic v4, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The hand-over is one element of eleven properties, published as the result of the signed branch of the stage workflow, and this contract declares no path, no operation and no error code of its own | TSD S2 T5.2.1; RWB-S2-E3001-CON; DP-13 |
| BR2 | Six properties map to a `treatment` field; the five facts without a column — `signedAt`, `toState`, `paymentInstructionRequired`, `ruleId` and `ruleVersion` — are recorded on the decision record | TSD S2 T3.1; GAP-2662; ASM-4371 |
| BR3 | The only signature status this element may carry is SIGNED; PENDING and NOT_SIGNED belong to the offer and to the no-signature path | TSD S2 T3.2 LOV-TRT-SIGNATURE; Rules v4 rows R-RES-17, R-RES-18 |
| BR4 | The two target states are WITH_OPS_BOOKING of R-RES-16 and WITH_OPS_SETTLEMENT of R-SET-10, read from the package in force and never written as constants | Rules v4; TSD S2 T4; FSD S2 A2.8.3.1 BR-S2-008 |
| BR5 | The instruction flag follows the route: false on the restructure route, true on the settlement route; the instruction record itself is rwb-payment's and is not published here | Rules v4 row R-SET-10; ASM-4374 |
| BR6 | The element carries facts and identifiers only: no customer, account, collateral or document value, and no personal data | DP-09; Template and Rules §R7.2 s17 |
| BR7 | A refused element names its field with MSG-GEN-001 before any hand-over, and the record path fails with MSG-P7-003 or refuses with MSG-P7-009 | RWB-E3-008 validation table; DP-03; RWB-PLT-E1027-CON |
| BR8 | The case status, the operations queue and the task timer are not part of the command this element carries: the parent applies the state and rwb-case owns the queue and the timer | ASM-4373; DP-01 |
| BR9 | The access of the read is capability area Treatment and offer, right R, checked by the platform guard library | TSD S2 T6.1; ASM-4371 |
| BR10 | A published version is never edited: a backward-compatible change stays in major version 1 and a breaking change raises major version 2 | Template and Rules §R5.4 class C; §R7.2 |

### 9. State transitions

None of its own: a contract document has no runtime state. Two vocabularies are fixed here and the runtime behind them is specified in RWB-S2-E3008-APP section 9.

| Object | State | Meaning in the contract |
|---|---|---|
| Hand-over element | Built | The signed branch assembled the eleven properties and no rule has been checked |
| Hand-over element | Validated | Every property passed its type, domain and cross-property rule |
| Hand-over element | Refused | A property failed or an unpublished `toState` was named; the field is named and nothing is handed over |
| Hand-over element | Returned | The element left the stage as the workflow result and the record was committed with it |
| Hand-over element | Applied or rejected by the parent | The parent moved the case or refused the state; both are outside this contract |
| Contract version | v1 | The published version every consumer pins |
| Contract version | v2 | Raised by a breaking change; v1 stays readable and is never edited |

The case states of the two routes — `OFFER_WITH_CUSTOMER`, `OFFER_WITH_CUSTOMER_SET`, `WITH_OPS_BOOKING` and `WITH_OPS_SETTLEMENT` — are rwb-case's vocabulary and are named here only as the context the element is returned in (DP-01; ASM-4373).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the element, the mapping section, the route section and the fakes |
| The rwb-treatment tech lead | Approves a breaking change and freezes a version of the hand-over |
| The solution architect | Confirms the element as the workflow result against the missing-path gap (GAP-2662; ASM-4371) |
| The P3 owner of the case workflow | Confirms the parent applies the state and owns the operations queue and the task timer (ASM-4373) |
| The rwb-payment owner (P8) and the rwb-partner owner (S9) | Confirm the instruction flag and the instruction record they raise from it (ASM-4374) |
| The service team of rwb-treatment (RW-TRIBE) | Consumes the contract in RWB-S2-E3008-APP, pins the version and raises a change request rather than a private variant |
| RW-RESTRUCT and RW-CASEOWN | Read the signed treatment through the gateway-bff composite route; RW-RESTRUCT holds CRUA and RW-CASEOWN CRU in capability area Treatment and offer |
| RW-PLATADM | Receives the incident that a refused or failed record raises |
| No delegation of authority level applies | A hand-over element is a technical artefact; the route itself is the rule's |

No personal name and no credential appears in the document, an example or a fake. Where an actor must be named, the example uses a role code or a service identity only.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The document publishes an element, its property types, the field identifiers of the six `treatment` fields it maps to and the message identifiers it raises; no customer, account or case value appears |
| Element published | The eleven properties of section 12.5, with the field identifiers DF-TRT-001, DF-TRT-002, DF-TRT-004, DF-TRT-030, DF-TRT-010 and DF-TRT-007 for the six that map to a column |
| Request-context facts published | Five properties with no field identifier and no column: `signedAt`, `toState`, `paymentInstructionRequired`, `ruleId` and `ruleVersion`; their home is the decision record (GAP-2662; ASM-4371) |
| Personal data | None. The element carries identifiers, a type, a status, a date, an amount, a state code and a version; the case subject never appears |
| Tables published | `treatment` only, as the field set the element maps to; this contract creates no table and adds no column, and `decision_record` is RWB-PLT-E1027-CON's |
| Retention | Not applicable: the contract stores nothing. The retention of `signature_status` and of the decision record belongs to the table owners |

### 12. Contract

#### 12.1 REST operations provided

None. Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). This contract provides no REST operation and no body of one: the two rows of the legacy endpoint table, `POST /cases/{caseId}/treatments` and `GET /treatments/{treatmentId}`, are RWB-S2-E3001-CON's and are named here, not redeclared. The element it publishes is the result of a Temporal workflow, and no source publishes a signature path or a hand-over path (GAP-2662; ASM-4371; TSD S2 T-A.1).

#### 12.2 REST operations consumed

None. The contract calls no service. The signature fact reaches the stage on the case event, the package version on `rwb.decision.RulePackageInForce.v1`, the record is written in process through RWB-PLT-E1027-CON, and the settlement instruction is rwb-payment's (DP-03, DP-05; ASM-4372, ASM-4374).

#### 12.3 Events published

None. The service topic is `rwb.treatment.events.v1` with event names `rwb.treatment.<Event>.v1` (DP-14), and its events TreatmentApproved (EV-10) and TreatmentClosed belong to the approval and closure stories (TSD S2 T5.3). The signed path publishes nothing of its own: the `DecisionRecorded` event of the record is the library's, written to this service's outbox in the apply transaction on the shared topic `rwb.decision-record.v1` (DP-03, DP-09).

#### 12.4 Events consumed

None. The package version is consumed by RWB-S2-E3008-APP's workflow on `rwb.decision.RulePackageInForce.v1` and is not a subscription of this contract; the contract only requires that the version in force is carried on the element and recorded with it (BR4).

#### 12.5 Workflows and activities

None. The contract defines no workflow and no activity; it defines the result element of one branch of an existing workflow.

| Item | Value |
|---|---|
| Element | `SignedOfferHandover` |
| Type | The result element of the signed branch of `TreatmentWorkflow`, published in the Temporal interface of the service |
| Produced by | `TreatmentWorkflow` on task queue `rwb-treatment` in namespace `rwb-recovery`, through `buildSignedHandover` and `recordSignedOutcome` of RWB-S2-E3008-APP |
| Consumed by | The parent `CaseWorkflow` of P3 rwb-case, as the child result, and the settlement instruction path of P8 through the flag it carries |

| Property | Type | Required | Maps to | Note |
|---|---|---|---|---|
| `treatmentId` | uuid | Yes | DF-TRT-001 `id` | The treatment the signed offer belongs to |
| `caseId` | uuid | Yes | DF-TRT-002 `case_id` | The case that moves to operations |
| `treatmentType` | varchar(20), LOV-TREATMENT | Yes | DF-TRT-004 `treatment_type` | RESTRUCTURE or SETTLEMENT on this path |
| `signatureStatus` | varchar(12), LOV-TRT-SIGNATURE | Yes | DF-TRT-030 `signature_status` | SIGNED only; PENDING and NOT_SIGNED are refused |
| `signedAt` | timestamptz | Yes | none | A request-context fact recorded on the decision record; no column is created |
| `validUntil` | date | No | DF-TRT-010 `valid_until` | The validity date the signature was inside |
| `offerAmount` | numeric(18,2) | No | DF-TRT-007 `offer_amount` | The amount the signed offer carries; the settlement instruction amount |
| `toState` | varchar(40) | Yes | none | The rule's target state, read from the package: WITH_OPS_BOOKING or WITH_OPS_SETTLEMENT |
| `paymentInstructionRequired` | boolean | Yes | none | false on R-RES-16, true on R-SET-10 |
| `ruleId` | varchar(20) | Yes | none | The rule that fired: R-RES-16 or R-SET-10 |
| `ruleVersion` | varchar(20) | Yes | none | The version of the rule in force that produced the route |

The required set is this contract's working read. TSD S2 T3.1 marks every mapped column as not required at column level and no source document fixes a hand-over body, so the properties without which no hand-over can be applied are made required here, and the reason is published with the gap and the assumption (GAP-2662; ASM-4371). The two `toState` values and the instruction flag are taken character for character from the rules in force and are read at run time, never written as constants (BR4, BR5; Rules v4 rows R-RES-16, R-SET-10).

#### 12.6 Schedules

None. The stage is started by the parent `CaseWorkflow` and advanced by the case signal; this contract declares no Schedule and no job, and the one-working-day follow-up of the rule is a task timer of rwb-case (ASM-4373; DP-10).

#### 12.7 Tables owned

| Table | Schema | Owner | This contract |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | The field set the element maps to: six fields of TSD S2 T3.1; no column is created or changed here, and no column exists for the five request-context facts |
| `decision_record` | `rwb_treatment` | PLT, a library object | The home of the five request-context facts; its shape and DDL template are RWB-PLT-E1027-CON's (DP-03) |
| `decision_log_entry` | `rwb_decision` | P7 | Named only: the central ledger is never read and never written by a consumer of this contract (DP-01) |
| `recovery_case`, `assignment`, `timer` | `rwb_case` | P3 | Named only: the case status, the queue and the timer are rwb-case's and are applied by the parent (ASM-4373) |

The contract declares no foreign key and no reference across a service boundary, and it creates nothing in another service's schema (DP-01). None of the five request-context facts has a row in any table of this service except the decision record (BR2).

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Hand-over fake | The `SignedOfferHandover` element | A complete booking hand-over; a complete settlement hand-over with the instruction flag; an element missing a required property with MSG-GEN-001 and the field; an unpublished `toState` with the same refusal; a `signedAt` after `validUntil` with the same refusal |
| Decision-record fake | RWB-PLT-E1027-CON | An accepted record with chain sequence and entry hash, a refusal with MSG-P7-009 and the field, and a failure with MSG-P7-003 |
| Case-status mock | The case status on the forwarded case signal | `OFFER_WITH_CUSTOMER` and `OFFER_WITH_CUSTOMER_SET`, the two statuses the criteria of RWB-S2-E3008-APP name |
| Route fake | The gateway-bff composite route of RWB-PLT-N001-CON | The SCR-14 signed treatment read and the SCR-15 settlement read, one hop each, from the same example set |
| Signature fixture | The signature fact on the case event | `signed = Y` and verified; `signed = Y` and not verified; `signed = N`; a signature that arrives after the validity date |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consuming story rather than as a surprise at run time. The case-status mock and the signature fixture are test-only and stand for the signal answer recorded with ASM-4373 and ASM-4372; no case table, no case REST call and no e-signature call exists behind them.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 of its own; 2 operations named as RWB-S2-E3001-CON's | 0 | No OpenAPI fragment is added; no path is published |
| Kafka | 0 | 0 | The service topic and its two events belong to other stories; the record event is the library's |
| Temporal | 1 element on the result of `TreatmentWorkflow` | 0 | The workflow and its activities are RWB-S2-E3008-APP's; this contract fixes the result shape only |
| File | 0 | 0 | No file crosses the contract |

### 13. Solution plan

**Package.** Contract artefact of rwb-treatment: the `SignedOfferHandover` type in `th.co.scb.ace.workbench.recovery.treatment.api`, registered in the service's Temporal interface, and the mapping, route and versioning sections in the contract document. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery` (DP-13, DP-14). The implementation is RWB-S2-E3008-APP.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The four rows are referred to here, not carried: this contract builds against nothing, and the two H dependencies are the consuming story's, which is why its own build list is empty by rule (Template and Rules §R5.7). DP-03 fixes the transaction the recorded facts must satisfy, DP-05 states that no ACE fact is copied onto the element, DP-13 fixes the base the named operations sit under, and DP-19 is the route through which the screens bind the element.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `SignedOfferHandover` | Published type | The eleven properties, their types and their mapped field identifiers (BR1, BR2) |
| `HandoverSpecification` | Document | The mapping, the required and optional rule and the record home of the five facts (BR2) |
| `RouteSpecification` | Document | The two `toState` values, the instruction rule and the read-from-the-package rule (BR4, BR5) |
| `ValidationSpecification` | Document | The type, domain and cross-property rules and the refusal set (BR7) |
| `VersioningSpecification` | Document | Major version 1, the compatible versus breaking rule and the pinning rule (BR10) |
| Fake set and fixtures | Test asset | The hand-over fake, the decision-record fake, the case-status mock, the route fake and the signature fixture (AC7) |

**Database.** No change. The six mapped fields already exist on `treatment` in `rwb_treatment` (DF-TRT-001, DF-TRT-002, DF-TRT-004, DF-TRT-030, DF-TRT-010, DF-TRT-007), and the contract requires that no migration adds a column for `signedAt`, `toState`, `paymentInstructionRequired`, `ruleId` or `ruleVersion` and that no column is renamed to carry one (BR2; GAP-2662; ASM-4371). `decision_record` is the library's object; this contract neither creates nor alters it.

**Configuration and reference data.** None of its own. The two target states, the two rule IDs and the rule versions are values in force of the package, not of this contract (BR4). The treatment type and signature lists are reference data read through the owner's contract (DP-07 is a service-template capability, ASM-4371), and the capability area and right of the read are the platform guard library's rows (BR9).

**Build steps**

1. Write the `SignedOfferHandover` type with the eleven properties and their types from TSD S2 T3.1 (AC1, AC2).
2. Register the element in the service's Temporal interface as the result of the signed branch, and assert that no REST fragment and no path is added (AC1).
3. Write the mapping section and the record home of the five request-context facts, and assert the absence of a column in the migration set (AC3).
4. Write the route section with the two `toState` values, the instruction rule and the read-from-the-package rule (AC4).
5. Write the validation and the refusal set, with the field naming and the record failure rule (AC5).
6. Write the versioning and pinning section with the compatible and breaking examples (AC6).
7. Generate the five fakes from the example set and write the drift test into the build of every consuming story (AC7).
8. Publish v1 and record the pinned version of RWB-S2-E3008-APP, the parent stage contract, the settlement instruction and the wave 2 integration harness (AC6).

**Feature flag.** `rwb.treatment.signed-handover-contract`.

**Done when.** The element validates against the service interface, a booking hand-over and a settlement hand-over are accepted, each of the five refusals answers with MSG-GEN-001 and its field, the migration set proves no column for the five facts, the five fakes answer every example, the drift test is green on RWB-S2-E3008-APP's build, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-GEN-001 | A required property is missing or a value is outside its type or domain | Enter {field}. | The element's validation answer with the field name, before any hand-over |
| MSG-P4-002 | The caller's role does not hold right R in Treatment and offer | You cannot {action} here. Your role does not include it. | 403 of the read, the guard library's answer |
| MSG-P7-009 | A record field is refused (log and incident, not the screen) | The decision record was refused: {field} is missing or not valid. | The library's `DecisionLogRecordInvalidException`, RWB-PLT-E1027-CON |
| MSG-P7-003 | The record cannot be written and nothing is handed over | The action was not taken because the decision could not be recorded. Try again in a few minutes. | 503 of the read path that shows the result, the library's `DecisionLogUnavailableException` |
| MSG-S2-003 | The offer reaches its validity date before a signature arrives (named here for the element's neighbour path) | The offer to the customer ends on {date}. | Information, RWB-S2-E3008-APP and the no-signature story |

The five texts are the legacy texts carried unchanged and this contract adds no message identifier of its own; MSG-GEN-001 and MSG-P4-002 are the legacy body's, MSG-P7-003 and MSG-P7-009 are the record library's, and MSG-S2-003 belongs to the offer clock. Thai text for each message follows decision DL10. Where the verification line of R-RES-16 fails, no message is published by any source (GAP-2662; ASM-4372).

### 15. Screens and states

No screen in this story and none declared. SCR-14 Treatment record (Draft, submitted, approved, booked, broken) shows the signed treatment with `signatureStatus` SIGNED, the validity date and the case after the hand-over, and SCR-15 Settlement offer (Draft, below floor, approved, sent, accepted) shows the settlement side of the same element; both bind the properties through the gateway-bff composite route and neither is built here (DP-19; RWB-PLT-N001-CON). The screen state lists name no operations state, so the operations step appears through the case status the parent holds and not through a new screen state (ASM-4373). The screen field list and the composite route specification belong to the platform edge story and the screen owners.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S2-E3008-CON-01 | AC1, AC2 | Contract | The element validated against the service interface: eleven properties, their types, the six field identifiers, the required set and the five request-context facts; no path and no REST fragment added |
| TC-S2-E3008-CON-02 | AC3 | Component | The record-home section compared to the migration set: no column for the five facts in `rwb_treatment`, no constant and no reference row; a migration that adds one is refused |
| TC-S2-E3008-CON-03 | AC4 | Contract | The two routes compared to R-RES-16 and R-SET-10: WITH_OPS_BOOKING with the flag false, WITH_OPS_SETTLEMENT with the flag true, both read from the package and neither written as a constant |
| TC-S2-E3008-CON-04 | AC5 | Contract | An accepted element; a missing required property, a signature status other than SIGNED, a treatment type outside the list, an unpublished `toState`, a contradictory instruction flag and a `signedAt` after `validUntil` each refused with MSG-GEN-001 and the field |
| TC-S2-E3008-CON-05 | AC6, AC7 | Component | A compatible change accepted in BACKWARD mode; a renamed property or a changed `toState` value raising major version 2; the five fakes answering every example; the drift test failing on a one-property difference |

The legacy test set of RWB-E3-008 is carried by RWB-S2-E3008-APP and by the wave 2 integration harness; these five are the contract's own tests and no legacy id is renumbered.

### 17. Guardrails

- No business value in the element: the two target states, the rule IDs and the rule versions are values in force of the package, and the contract fixes only types, rules and the read-from-the-package obligation (BR4).
- No column for the five request-context facts, no constant and no reference row: they are recorded on the decision record (BR2).
- No personal data in the schema, an example, a fake or a log: the element carries identifiers, a type, a status, a date, an amount, a state code and a version, and the scan fails the build otherwise (BR6).
- No path, no operation and no error code of this contract's own: the two legacy rows are RWB-S2-E3001-CON's and are named only (BR1).
- No cross-schema reference and no foreign key across services; the boundary test fails the build (DP-01).
- No case table read and no case state written: the parent applies the state, and the case-status mock is test-only (BR8; ASM-4373).
- No record written outside the library's `MANDATORY` transaction, and no ledger row: `decision_log_entry` is P7's and is named here only (DP-03; DP-01).
- No ACE fact copied onto the element: customer and payment facts stay with their owner and arrive through its contract only if a step needs them (DP-05).
- A published version is never edited in place: a breaking change raises major version 2 with a migration note (BR10).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-003 | A signed offer routes to operations for booking, and an unsigned or declined offer returns the case to its prior status | Program, 5.9 | FEAT-TRT-08 | 07 Route, settle and claim | R-RES-16; R-SET-10 | TC-S2-E3008-CON-01, TC-S2-E3008-CON-03, TC-S2-E3008-CON-04 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3008-APP | App development | H consumer: builds the signed branch, the signature write, the rule evaluation and the record write against this contract and its fakes |
| RWB-S2-E3001-CON, RWB-S2-E3001-APP | Contract, App development | Referred to: the treatment entity and the two operations the legacy endpoint table lists. This contract adds no build dependency of its own |
| RWB-S2-E3009-APP | App development | Referred to: the no-signature path, which owns the other two signature list values |
| The booking stories of S2 (FEAT-TRT-10) | App development | Referred to: booking to ALS and NLEADS and the settlement booking, which act after this hand-over |
| RWB-PLT-E1027-CON | Contract | DP-03: the local decision-record library that holds the five request-context facts |
| RWB-PLT-N001-CON | Contract | DP-19: the gateway-bff composite route through which SCR-14 and SCR-15 bind the element |
| rwb-case (P3) | App development | The parent `CaseWorkflow` that consumes the element and owns the case state and the operations queue |
| rwb-payment (P8), rwb-partner (S9) | App development | The settlement instruction the element flags |
| rwb-document (P5) | App development | The e-signature execution behind the signature fact |
| RWB-PLT-DB, the per-service DB stories | Database | X: the schema, login and grants of `rwb_treatment` in which `treatment` sits |
| The wave 2 integration harness | Integration | I: the cross-service proof of the same legacy key against the live owners |

### 19. Out of scope

- The signed branch of the workflow, the signature write, the rule evaluation, the record write and the read: RWB-S2-E3008-APP.
- The treatment entity, its other fields, its states and the two operations of the legacy endpoint table: RWB-S2-E3001-APP and RWB-S2-E3001-CON.
- The offer, its validity clock, the counter-offer path and the below-floor approval: RWB-S2-E3002-APP, RWB-S2-E3003-APP, RWB-S2-E3004-APP and RWB-S2-E3007-APP.
- The return on no signature, on decline and on expiry: RWB-S2-E3009-APP.
- The case status, the operations queue, the assignment and the task timer: rwb-case (P3), RWB-P3-E2004-APP and its contract.
- The settlement instruction record, the payment posting and the settlement due date: rwb-payment (P8) and rwb-partner (S9).
- The e-signature execution, the offer documents and the signature verification itself: rwb-document (P5).
- The decision-record library, its DDL template, its envelope and its exceptions: RWB-PLT-E1027-CON and RWB-PLT-E1027-APP; the central ledger: the P7 ledger story.
- The rule package registry, the rule versions and their announcement: P7 rwb-decision, RWB-P7-E1073-CON.
- SCR-14 and SCR-15, their field list and the gateway-bff composite route: the platform edge story and the screen owners (DP-19).
- The real cross-service proof of the signed route, the record and the instruction: the wave 2 integration harness.

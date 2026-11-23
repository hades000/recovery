# RWB-S2-E3004-CON Offer a TDR plan - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E3-004 for rwb-treatment (S2, Treatment and offer). This document publishes the `PlanOffer` element of the TDR plan offer — its properties, its required and optional rules, its validation against the `treatment` field set of TSD S2 T3.1, the rule that the band is a request-context fact and not a stored column, its place on the offer operation that RWB-S2-E3002-CON declares, the versioning rule and the fakes — on base `/api/recovery/treatment/v1` (DP-13), with the screens reached through the gateway-bff composite route (DP-19) and the decision record written through the library of RWB-PLT-E1027-CON (DP-03). The legacy acceptance criteria stay with RWB-S2-E3004-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3004-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-004 |
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
| Status | Draft (realignment v1) |

### 1. Story

As a **contract owner of rwb-treatment**, I want **the published plan body of the TDR offer — the `PlanOffer` element, its required and optional properties, its validation against the `treatment` field set, the rule that the band is request-context and never a column, its place on the offer operation that the offer contract declares, the versioning rule and the fakes — instead of the monolith's in-process offer assembled from the affordability calculation**, so that **the plan story, the screens, the affordability story and the wave 2 integration harness can build against one frozen plan body from Day 1, and no band is ever stored or hard-coded**.

The contract covers exactly five things:

- the `PlanOffer` element and its seven properties, and the operation it belongs to — `POST /treatments/{treatmentId}/offer`, declared by RWB-S2-E3002-CON and named, not redeclared, here (DP-13; Architecture v5 slide 18);
- the required and optional rules of those properties within the `treatment` field set of TSD S2 T3.1, so that the body cannot carry a property the table has no column for and cannot omit a term an offer cannot be without;
- the band rule: `bandLow` and `bandHigh` are request-context facts of the ACE affordability result of RWB-S2-E3005 and are recorded with the offer on the decision record, and no `treatment` column and no constant exists for either (GAP-1873; ASM-3069);
- the versioning rule and the pinning rule that let the plan story, the screens, the affordability story and the integration harness pin v1 and raise a change request rather than a private variant;
- the fakes: a plan-offer fake, a route fake, a decision-record fake and a case-status mock, all answering from one example set, with the drift test that fails a build on any difference from this document.

It does not own: the offer operation, its envelope, its `Treatment` response and its error set, which are RWB-S2-E3002-CON; the plan steps, the plan columns write, the offer timer and the record write, which are RWB-S2-E3004-APP; the affordability calculation and its band, which are RWB-S2-E3005-APP; the treatment entity and its other fields, which are RWB-S2-E3001-APP and its contract; the decision-record library and its DDL template, which are RWB-PLT-E1027-CON; the case status, which is rwb-case's (DP-01; ASM-3062); and the screens, which are the platform edge story's and the screen owners' (DP-19).

### 2. Business rationale

The plan offer is the step of S2 where a restructure either reaches booking or deviates. The FSD measures the feature by restructure turnaround of 5 days against today's 23 to 26 days (FSD S2 v3, section A2.4.1), and the two requirements behind it are REQ-S2-001, that a restructure reaches the restructuring officer with the case and the case does not leave the Workbench, and REQ-S2-002, that an offer carries a validity period and that expiry returns the case to the status it came from. Both requirements are unbuildable without one agreed plan body: two teams that each invent a plan payload produce two offers that cannot be compared, and an offer whose validity date is optional is no offer at all.

In the monolith the plan was assembled inside the process from the affordability calculation, so no shape was ever written down. Architecture v5 changes that: rwb-treatment accepts `POST /treatments/{id}/offer` (Architecture v5 slide 18) and owns the treatments, contracts, settlement and deed-in-lieu agreements and plan timers in `rwb_treatment` (Architecture v5 slide 41), while the affordability result comes from the ACE restructure calculator through a Nexus operation (Architecture v5 slide 18, "NEXUS ACE Common: restructure calculator (Nexus)"). A published body is therefore the only place where the ACE result, the officer's screen and the stored plan meet.

Two facts make the contract urgent rather than tidy. The first is the band. The FSD says the band and the rule version are applied to the offer and that the affordability calculation produces the plan, without naming a shape, and TSD S2 T3.1 has no band column: if the band is left to the implementers, one team stores it, one team hard-codes it and the rule version becomes unprovable, which contradicts BR-S2-004 (no value a business person may change is written in code) and the acceptance criteria AC1 and AC3. The contract therefore fixes the band as a request-context fact of the offer body and of the decision record, and forbids a column (GAP-1873; ASM-3069). The second is the write path. Architecture v5 slide 18 names `POST /treatments/{id}/offer`; API Specification v4 and TSD S2 T-A.1 API-S2-004 name `POST /treatments/{treatmentId}/submit`; the legacy story's own endpoint table lists neither, only the GET. The contract records the conflict, publishes `/offer` and records the TSD form as superseded (GAP-1874; ASM-3070).

The fake is the Day-1 unblocker. RWB-S2-E3004-APP, the two screen stories and the wave 2 integration harness can build and test the plan form, the band path and the refusal paths before the affordability story or the live route exists, and the plan story can prove its own contract conformance before a single environment is booked (Template and Rules §R5.4 class C, §R5.7).

### 3. Preconditions

- The plan columns are fixed by TSD S2 T3.1: `installments` (DF-TRT-009, integer), `installment_amount` (DF-TRT-031, numeric(18,2)), `interest_rate` (DF-TRT-027, numeric(7,4)), `first_due_date` (DF-TRT-029, date) and `valid_until` (DF-TRT-010, date), on `treatment` in schema `rwb_treatment`, owned by S2 (DP-01; Architecture v5 slide 41).
- The offer operation exists and is another contract's: `POST /treatments/{treatmentId}/offer` on base `/api/recovery/treatment/v1`, declared by RWB-S2-E3002-CON with its envelope and its error set (DP-13; Architecture v5 slide 18).
- The two sources disagree on the write path and the disagreement is recorded: Architecture v5 slide 18 names `/offer`, API Specification v4 and TSD S2 T-A.1 API-S2-004 name `/submit`, and the legacy endpoint table names neither (GAP-1874; ASM-3070).
- No source defines the plan body, the band's shape or the offer clock's mechanism; the plan properties, the required set and the band's home are this contract's working read, published with the gap and the assumption (GAP-1873; ASM-3069).
- The band arrives with the ACE affordability result of RWB-S2-E3005-APP, which is the sibling story of this service; until it is built the fixture of section 12.8 stands in for it.
- The decision record is written through RWB-PLT-E1027-CON with `@Transactional(propagation = MANDATORY)`, refusing with MSG-P7-009 and failing with MSG-P7-003; `decision_record` is a library object in `rwb_treatment` and `decision_log_entry` is P7's (DP-03, DP-01).
- The gateway-bff composite route of RWB-PLT-N001-CON exists, so the screens' binding to the plan body is named and not declared here (DP-19).
- The access rule is the platform guard library's: capability area "Treatment and offer", right U for the offer and right R for the read, with RW-RESTRUCT holding CRUA and RW-CASEOWN CRU (TSD S2 T6.1; ASM-3064).
- The two legacy message texts this body raises are kept unchanged: MSG-GEN-001 and MSG-P4-002, with MSG-P7-003 for the record path.
- No build dependency and no approval stop: a CON story is Day 1 by rule (Template and Rules §R5.7) and is published at status Draft (realignment v1).

### 4. Flow

1. The contract author fixes the element: `PlanOffer` with its seven properties, their types taken from TSD S2 T3.1 and their field identifiers, and nothing else.
2. The author fixes the required and optional rule: the four terms an offer cannot be without are required, the interest rate and the two band values are optional, and the reasoning and its gap reference are written into the document.
3. The author writes the validation section: the property domains, the cross-property rules, the refusal of an unknown property including any band column, and the error set with the message identifiers.
4. The author writes the band section: the band is a request-context fact of the affordability result, carried on the body and recorded with the offer on the decision record, and `treatment` gains no column for it.
5. The author writes the operation section: the path, the method, the right, the idempotency header and the response, all named as RWB-S2-E3002-CON's, with this contract's body attached to it and the `/submit` conflict recorded as superseded.
6. The author writes the versioning and pinning section: major version 1, the compatible-versus-breaking rule and the pinning obligation of the four consumers.
7. The schema and lint steps run: the body validated against the element and against the `treatment` field set, the example scanned for personal data, and a body naming a band column refused.
8. The fake set is generated from the same example set: the plan-offer fake, the route fake, the decision-record fake and the case-status mock.
9. The drift test runs the fakes against the document on every change and fails the build on any difference.
10. The document and the fakes are published at v1, and RWB-S2-E3004-APP, the screen stories, RWB-S2-E3005-APP and the wave 2 integration harness pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The body is published without one of the four required terms, or with a property that is not in the element | The schema validation fails the build; the element holds exactly seven properties and the required set is fixed | None | AC1, AC2 |
| X2 | A body names a band column, or a plan property with no `treatment` field | The request is refused as a contract violation; the band is context only and the table gains no column | MSG-GEN-001 | AC3, AC4 |
| X3 | A property carries a value outside its type or domain, or the band is inverted | The request is refused with the field named; nothing is written | MSG-GEN-001 | AC4 |
| X4 | The body is published on a path other than the offer operation, or on `/treatments/{treatmentId}/submit` | The drift test and the lint fail the build; the plan is submitted through `/offer` and the TSD form is recorded as superseded | None | AC1, AC5 |
| X5 | A breaking change is made to a property, a required rule, the band rule or the path | The change raises major version 2; v1 is never edited in place and stays readable | None | AC5 |
| X6 | A consuming story ships without the drift test, or a schema change breaks a consumer | The drift test fails the build of that consumer and the registry refuses the change | None | AC6 |
| X7 | A value the consumers need is named by no source — the plan body, the required set, the band's home or the offer clock's mechanism | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-1873; ASM-3069) | Section 3 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document and a fake set; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | The example values, the property order and the description texts are open until v1 is frozen; the seven properties, the required set, the no-column rule and the path are fixed |
| Valuable | Unblocks the plan story, the two screen stories, the affordability story and the integration harness with one plan body on Day 1 |
| Estimable | One element, one validation section, one band section, one versioning rule and four fakes |
| Small | One sprint for the document, the schema, the fakes and the drift test |
| Testable | Each criterion below is one schema, lint or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: TDR plan offer contract

  Background:
    Given the rwb-treatment contract document is published at major version 1
    Given the treatment table carries the 33 fields of TSD S2 T3.1 in schema rwb_treatment
    Given the plan body is published on the offer operation of the same service and declares no path of its own

  Scenario: AC1 The PlanOffer element is published on the offer operation (new, D-RCV-60)
    Given the element section of the contract document
    When it is validated and linted
    Then it publishes PlanOffer with exactly seven properties: installmentCount, installmentAmount, interestRate, firstDueDate, validUntil, bandLow and bandHigh
    Then the body is the request of POST /treatments/{treatmentId}/offer on base /api/recovery/treatment/v1, the operation declared by RWB-S2-E3002-CON and named here, not redeclared
    Then the response of the operation is the Treatment of RWB-S2-E3002-CON and this contract adds no second path and no second operation
    Then the document records that API Specification v4 and TSD S2 T-A.1 API-S2-004 name /treatments/{treatmentId}/submit and that the form is superseded by /offer
    Then the access is capability area Treatment and offer with right U for the offer and right R for the read, checked by the platform guard library and declared here as the right only

  Scenario: AC2 The required set and the optional set are fixed against the treatment field set (new, D-RCV-60)
    Given the element section and the treatment field set of TSD S2 T3.1
    When every property is compared to its column and to its type
    Then installmentCount is required and maps to DF-TRT-009 installments, integer
    Then installmentAmount is required and maps to DF-TRT-031 installment_amount, numeric(18,2)
    Then firstDueDate is required and maps to DF-TRT-029 first_due_date, date
    Then validUntil is required and maps to DF-TRT-010 valid_until, date
    Then interestRate is optional and maps to DF-TRT-027 interest_rate, numeric(7,4)
    Then bandLow and bandHigh are optional and map to no column
    Then no property without a mapping beyond the band pair is published, and the required set is named as the working read of GAP-1873 and ASM-3069 because TSD S2 T3.1 marks all five plan columns as not required

  Scenario: AC3 The band is a request-context fact and gains no column (new, D-RCV-60)
    Given the band section of the document and the DDL of treatment
    When the body, the decision record and the table are compared
    Then bandLow and bandHigh are carried on the body from the ACE affordability result of RWB-S2-E3005 and are recorded with the offer on the decision record
    Then treatment has no column for either band and no migration in rwb_treatment adds one
    Then no band value is published as a constant, a default or a reference-data row of this contract
    Then a body or a migration that stores a band fails the schema lint and the drift test

  Scenario: AC4 The validation and the error set are published (new, D-RCV-60)
    Given the validation section of the document
    When a body is validated against it
    Then a missing required property is refused with MSG-GEN-001 and the field name, before any write
    Then a property outside its type or domain is refused with MSG-GEN-001 and the field name
    Then a body that names a band column or an unknown property is refused with MSG-GEN-001 and the field name
    Then a band present as a pair with bandLow greater than bandHigh is refused with MSG-GEN-001 and the field name
    Then the error set of the operation is the one RWB-S2-E3002-CON publishes, with 401, 403 with MSG-P4-002, 404, 409, 422 and 503, and MSG-P7-003 when the record cannot be written, and this contract adds no status code

  Scenario: AC5 Versioning separates a compatible change from a new major version (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published property or rule
    Then an added optional property keeps major version 1 and is accepted by the registry in BACKWARD mode
    Then a change to a property name, a type, a required rule, the band rule or the path raises major version 2, and v1 is never edited in place
    Then RWB-S2-E3004-APP, the screen stories, RWB-S2-E3005-APP and the wave 2 integration harness pin a published version and raise a change request rather than a private variant

  Scenario: AC6 The fakes answer the document and the drift test fails on any difference (new, D-RCV-60)
    Given the fake set generated from the same example set as the document
    When the contract test runs the plan-offer fake, the route fake, the decision-record fake and the case-status mock
    Then the plan-offer fake answers a complete plan body, a refused body with MSG-GEN-001 and its field, and a body naming a band column with the same refusal
    Then the route fake answers the two screen reads one hop each, and the decision-record fake answers an accepted record, a refusal with MSG-P7-009 and a failure with MSG-P7-003
    Then the case-status mock answers IN_FCR_QUEUE and AFFORDABILITY_IN_ACE for the two criteria of RWB-S2-E3004-APP
    Then the drift test of every consuming story fails the build on any difference from section 12 and section 13
```

These criteria are new: no legacy acceptance criterion is repeated here — **AC1 to AC4 of RWB-E3-004 stay with RWB-S2-E3004-APP** — and every identifier comes from the legacy story, Architecture v5, the TSD or the Temporal and Drools Design, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The plan body is one element of seven properties, published on the offer operation of the same service, and this contract declares no path, no response and no error code of its own | Architecture v5 slide 18; RWB-S2-E3002-CON; DP-13 |
| BR2 | The four terms an offer cannot be without are required; the interest rate and the band pair are optional; every property beyond the band pair maps to a `treatment` column | TSD S2 T3.1; GAP-1873; ASM-3069 |
| BR3 | The band is a request-context fact of the ACE affordability result, recorded with the offer on the decision record; `treatment` has no band column and this contract publishes no band constant | GAP-1873; ASM-3069; FSD A2.4.3.1 BR-S2-004 |
| BR4 | No value a business person may change is written in code: the validity period and the plan terms are values in force, and the band and the rule version come from the affordability result with their version | FSD A2.4.3.1 BR-S2-004; TSD S2 T6.1 |
| BR5 | The plan is submitted through `POST /treatments/{treatmentId}/offer`; `/treatments/{treatmentId}/submit` is not published | GAP-1874; ASM-3070 |
| BR6 | A refused body names its field with MSG-GEN-001 before any write; the record path fails with MSG-P7-003 and the apply step rolls back | RWB-E3-004 validation table; DP-03; RWB-PLT-E1027-CON |
| BR7 | The access of the operation is capability area Treatment and offer, right U for the offer and right R for the read, checked by the platform guard library | TSD S2 T6.1; ASM-3064 |
| BR8 | A published version is never edited: a backward-compatible change stays in major version 1 and a breaking change raises major version 2 | Template and Rules §R5.4 class C; §R7.2 |
| BR9 | The case status is not part of this body and is not read here: the case status stays rwb-case's and reaches the stage on the case signal | ASM-3062; DP-01 |
| BR10 | The `PlanOffer` body carries facts and identifiers only: no customer, account, collateral or document value, and no personal data | DP-09; Template and Rules §R7.2 s17 |

### 9. State transitions

None of its own: a contract document has no runtime state. Two vocabularies are fixed here and the runtime behind them is specified in RWB-S2-E3004-APP section 9.

| Object | State | Meaning in the contract |
|---|---|---|
| Plan offer body | Received | The body arrived on the offer operation and no rule has run |
| Plan offer body | Validated | The seven properties passed their type, domain and cross-property rules |
| Plan offer body | Refused | A property failed or an unknown property was named; the field is named and nothing is written |
| Plan offer body | Accepted | The plan columns, the decision record and the outbox row were committed together |
| Plan offer body | Expired | The validity date was reached and the offer ended; the case move is rwb-case's |
| Contract version | v1 | The published version every consumer pins |
| Contract version | v2 | Raised by a breaking change; v1 stays readable and is never edited |

The case statuses of the plan — `IN_FCR_QUEUE`, `WITH_FCR_OFFICER`, `AFFORDABILITY_IN_ACE`, `OFFER_WITH_CUSTOMER` — are rwb-case's vocabulary and are named here only as the context the body is offered in (DP-01; ASM-3062).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the element, the validation section and the fakes |
| The rwb-treatment tech lead | Approves a breaking change and freezes a version of the plan body |
| The solution architect | Confirms the write path decision against the Arch v5 and TSD conflict (GAP-1874; ASM-3070) |
| The rwb-valuation and ACE affordability owner (S1) | Confirms the band that the affordability result carries |
| The service team of rwb-treatment (RW-TRIBE) | Consumes the contract in RWB-S2-E3004-APP, pins the version and raises a change request rather than a private variant |
| The screen owners, RW-RESTRUCT and RW-CASEOWN | Bind the plan form and the plan view through the gateway-bff composite route; RW-RESTRUCT holds CRUA and RW-CASEOWN CRU in capability area Treatment and offer |
| RW-PLATADM | Receives the incident that a refused or failed record raises |
| No delegation of authority level applies | A plan body is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in the document, an example or a fake. Where an actor must be named, the example uses a role code or a user identifier only.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The document publishes a body, its property types, the field identifiers of the `treatment` columns it maps to and the message identifiers it raises; no customer, account or case value appears |
| Plan body published | The seven properties of section 12.1, with the field identifiers DF-TRT-009, DF-TRT-031, DF-TRT-027, DF-TRT-029 and DF-TRT-010 for the five that map to a column |
| Band published | Two optional properties, `bandLow` and `bandHigh`, with no field identifier and no column: their shape and their home are Not specified in the source documents (GAP-1873; ASM-3069) |
| Personal data | None. The body carries amounts, counts, rates and dates; the case is identified by its ID outside the body |
| Tables published | `treatment` only, as the field set the body validates against; this contract creates no table and adds no column, and `decision_record` is RWB-PLT-E1027-CON's |
| Retention | Not applicable: the contract stores nothing. The retention of the plan columns and of the decision record belongs to the table owners |

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). This contract provides the plan body of one operation whose path, envelope, response and error set are declared by RWB-S2-E3002-CON; it declares no operation of its own and no second path.

| Item | Value |
|---|---|
| Operation | `POST /treatments/{treatmentId}/offer`, declared by RWB-S2-E3002-CON and named here |
| Body | `PlanOffer` |
| Response | `Treatment` of RWB-S2-E3002-CON, with the plan terms of the five mapped columns |
| Access | Capability area Treatment and offer, right U, scope applied, checked by the platform guard library |
| Idempotency | `Idempotency-Key` header of the operation |
| Errors | The error set of RWB-S2-E3002-CON: 400 or 422 with MSG-GEN-001 and the field, 401, 403 with MSG-P4-002, 404, 409, 503, and MSG-P7-003 on the record path |

| Property | Type | Required | Maps to | Note |
|---|---|---|---|---|
| `installmentCount` | integer | Yes | DF-TRT-009 `installments` | The number of installments in the plan |
| `installmentAmount` | numeric(18,2) | Yes | DF-TRT-031 `installment_amount` | The amount of one installment |
| `firstDueDate` | date | Yes | DF-TRT-029 `first_due_date` | The first due date of the plan |
| `validUntil` | date | Yes | DF-TRT-010 `valid_until` | The validity date of the offer; the offer clock runs to this date |
| `interestRate` | numeric(7,4) | No | DF-TRT-027 `interest_rate` | Optional: a plan may carry no rate |
| `bandLow` | numeric(18,2) | No | none | A request-context fact of the ACE affordability result |
| `bandHigh` | numeric(18,2) | No | none | A request-context fact of the ACE affordability result |

The required set is this contract's working read. TSD S2 T3.1 marks all five plan columns as not required at column level and no source document fixes a request body, so the four terms without which an offer cannot be sent are made required here, and the reason is published with the gap and the assumption (GAP-1873; ASM-3069). The path is the one Architecture v5 slide 18 names, `POST /treatments/{id}/offer`; API Specification v4 and TSD S2 T-A.1 API-S2-004 name `POST /treatments/{treatmentId}/submit` and that form is recorded as superseded by this contract, because the legacy story's own endpoint table names neither and publishes only the GET (GAP-1874; ASM-3070).

#### 12.2 REST operations consumed

None. The contract calls no service. The band arrives on the body from the ACE affordability result of RWB-S2-E3005 as a value the plan story passes in, the case status stays rwb-case's and reaches the stage on the case signal, and the decision record is written in process through RWB-PLT-E1027-CON (DP-03; ASM-3062; ASM-3069).

#### 12.3 Events published

None. The service topic is `rwb.treatment.events.v1` with event names `rwb.treatment.<Event>.v1` (DP-14), and its events `TreatmentApproved` and `TreatmentClosed` belong to the approval and closure stories. The plan offer publishes nothing of its own: the `DecisionRecorded` event of the record is the library's, written to this service's outbox in the offer's transaction on the shared topic `rwb.decision-record.v1` (DP-03, DP-09).

#### 12.4 Events consumed

None. The rule package version is consumed by RWB-S2-E3004-APP's workflow on `rwb.decision.RulePackageInForce.v1` (EV-30) and is not a subscription of this contract; the contract only requires that the version in force is recorded with the offer (BR4).

#### 12.5 Workflows and activities

None. The contract defines no workflow and no activity. The plan steps live in `TreatmentWorkflow` of RWB-S2-E3004-APP on task queue `rwb-treatment` in namespace `rwb-recovery`, which calls `buildPlanOffer`, `applyBand` and `recordAndApply`; the contract fixes the body those steps validate and writes (ASM-3069).

#### 12.6 Schedules

None. The offer clock is a durable Temporal timer inside `TreatmentWorkflow` and belongs to RWB-S2-E3004-APP; this contract declares no Schedule and no job, and the legacy five-minute timer check is retired (ASM-3069; DP-10).

#### 12.7 Tables owned

| Table | Schema | Owner | This contract |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | The field set the body validates against: the five plan columns of TSD S2 T3.1; no column is created or changed here, and no band column exists |
| `decision_record` | `rwb_treatment` | PLT, a library object | Named only: the shape and the DDL template are RWB-PLT-E1027-CON's (DP-03) |
| `decision_log_entry` | `rwb_decision` | P7 | Named only: the central ledger is never read and never written by a consumer of this contract (DP-01) |

The contract declares no foreign key and no reference across a service boundary, and it creates nothing in another service's schema (DP-01). The band pair has no row in any table: it is a request-context fact recorded with the offer on the decision record (BR3).

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Plan-offer fake | The `PlanOffer` element and the offer operation of RWB-S2-E3002-CON | A complete plan body; a body missing one of the four required terms with MSG-GEN-001 and the field; a body with a property outside its domain with the same refusal; a body naming a band column with the same refusal; a band pair inverted with the same refusal |
| Route fake | The gateway-bff composite route of RWB-PLT-N001-CON | The SCR-14 plan form answer and the SCR-15 plan view answer, one hop each, both built from the same example body |
| Decision-record fake | RWB-PLT-E1027-CON | An accepted record with chain sequence and entry hash, a refusal with MSG-P7-009 and the field, and a failure with MSG-P7-003 |
| Case-status mock | The case status on the forwarded case signal | `IN_FCR_QUEUE` and `AFFORDABILITY_IN_ACE`, the two statuses the criteria of RWB-S2-E3004-APP name |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consuming story rather than as a surprise at run time. The case-status mock is test-only and stands for the signal answer recorded with ASM-3062; no case table and no case REST call exists behind it.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 1 body on 1 operation declared by another contract | 0 | OpenAPI 3.1 fragment of the offer operation, merged into the service document of RWB-S2-E3002-CON |
| Kafka | 0 | 0 | The service topic and its two events belong to other stories; the record event is the library's |
| Temporal | 0 | 0 | No workflow and no activity; the plan steps are RWB-S2-E3004-APP's |
| File | 0 | 0 | No file crosses the contract |

### 13. Solution plan

**Package.** Contract artefact of rwb-treatment: the `PlanOffer` type in `th.co.scb.ace.workbench.recovery.treatment.api`, the OpenAPI fragment of the plan form merged into the service document of RWB-S2-E3002-CON, and the validation, band and versioning sections in the contract document. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery` (DP-13, DP-14). The implementation is RWB-S2-E3004-APP.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The three rows are referred to here, not carried: this contract builds against nothing, and the two H dependencies are the consuming story's, which is why its own build list is empty by rule (Template and Rules §R5.7). DP-03 fixes the transaction rule the record path must satisfy, DP-13 fixes the base the plan body is published under, and DP-19 is the route through which SCR-14 and SCR-15 bind the body.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `PlanOffer` | Published type | The seven properties, their types and their mapped field identifiers (BR1, BR2) |
| PlanOfferSchema | Resource | The OpenAPI fragment of the plan form, merged into the service document of RWB-S2-E3002-CON (BR1, BR5) |
| ValidationSpecification | Document | The type, domain and cross-property rules and the refusal set (BR6) |
| BandSpecification | Document | The band as a request-context fact, the no-column rule and the record home (BR3) |
| VersioningSpecification | Document | Major version 1, the compatible versus breaking rule and the pinning rule (BR8) |
| Fake set and fixtures | Test asset | The plan-offer fake, the route fake, the decision-record fake and the case-status mock (AC6) |

**Database.** No change. The five plan columns already exist on `treatment` in `rwb_treatment` (DF-TRT-009, DF-TRT-031, DF-TRT-027, DF-TRT-029, DF-TRT-010), and the contract requires that no migration adds a band column and no column is renamed to carry one (BR3; GAP-1873; ASM-3069). `decision_record` is the library's object; this contract neither creates nor alters it.

**Configuration and reference data.** None of its own. The validity period of the offer and the length of the offer clock are values in force of the parameters and the rule package, not of this contract (BR4; Temporal and Drools Design slide 18, "Offer 14 days"). The status and treatment-type lists are reference data read through the owner's contract, and the capability area and rights of the operation are the platform guard library's rows (BR7; ASM-3064).

**Build steps**

1. Write the `PlanOffer` type with the seven properties and their types from TSD S2 T3.1 (AC1, AC2).
2. Write the OpenAPI fragment of the plan form and merge it into the service document of RWB-S2-E3002-CON; assert one path and no `/submit` (AC1).
3. Write the required and optional rule with the field mapping and the gap reference (AC2).
4. Write the band section and the no-column rule, and assert the absence of a band column in the migration set (AC3).
5. Write the validation and the error set, with the field naming and the rollback rule (AC4).
6. Write the versioning and pinning section with the compatible and breaking examples (AC5).
7. Generate the four fakes from the example set and write the drift test into the build of every consuming story (AC6).
8. Publish v1 and record the pinned version of RWB-S2-E3004-APP, the two screen stories, RWB-S2-E3005-APP and the wave 2 integration harness (AC5).

**Feature flag.** `rwb.treatment.plan-offer-contract`.

**Done when.** The element and the fragment validate against the service document, a complete body is accepted and each of the five refusals answers with MSG-GEN-001 and its field, the migration set proves no band column, the four fakes answer every example, the drift test is green on RWB-S2-E3004-APP's build, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-GEN-001 | A required property is missing or a value is outside its type or domain | Enter {field}. | 422 with the field name, before any write |
| MSG-P4-002 | The caller's role does not hold right U in Treatment and offer | You cannot {action} here. Your role does not include it. | 403 of the operation, the guard library's answer |
| MSG-P7-009 | A record field is refused (log and incident, not the screen) | The decision record was refused: {field} is missing or not valid. | The library's `DecisionLogRecordInvalidException`, RWB-PLT-E1027-CON |
| MSG-P7-003 | The record cannot be written and the offer is not sent | The action was not taken because the decision could not be recorded. Try again in a few minutes. | 503 of the operation, the library's `DecisionLogUnavailableException` |
| MSG-S2-003 | The offer reaches its validity date (raised by the plan story, named here for the body) | The offer to the customer ends on {date}. | Information, RWB-S2-E3004-APP |

The five texts are the legacy texts carried unchanged and this contract adds no message identifier of its own; MSG-GEN-001 and MSG-P4-002 are the legacy body's, MSG-P7-003 and MSG-P7-009 are the record library's, and MSG-S2-003 belongs to the plan steps run by RWB-S2-E3004-APP. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story and none declared. SCR-14 Treatment record (Draft, submitted, approved, booked, broken) shows the plan form and the plan terms of a submitted body, and SCR-15 Settlement offer (Draft, below floor, approved, sent, accepted) shows the plan view; both bind the `PlanOffer` properties through the gateway-bff composite route and neither is built here (DP-19; RWB-PLT-N001-CON). The band appears on the ride-along view of the affordability result as a read-only fact and never as an editable field, because it is a request-context fact of the offer (BR3). The screen field list and the composite route specification belong to the platform edge story and the screen owners.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S2-E3004-CON-01 | AC1, AC2 | Contract | The element validated against the service document: seven properties, their types, the five field identifiers, the required set and the two optional band properties; one path on the offer operation and no `/submit` |
| TC-S2-E3004-CON-02 | AC3 | Component | The band section compared to the migration set: no band column in `rwb_treatment`, no band constant and no reference row; a migration that adds one is refused |
| TC-S2-E3004-CON-03 | AC4 | Contract | A complete body accepted; a missing required property, an out-of-domain value, an unknown property, a named band column and an inverted band pair each refused with MSG-GEN-001 and the field; the operation's error set unchanged |
| TC-S2-E3004-CON-04 | AC5 | Contract | A compatible change accepted in BACKWARD mode; a renamed property, a changed type and a changed path each raising major version 2; v1 readable and unedited |
| TC-S2-E3004-CON-05 | AC6 | Component | The four fakes answering every example, including the three refusals, the accepted record, the record failure and the two case statuses; the drift test failing on a one-property difference |

The legacy test set of RWB-E3-004 is carried by RWB-S2-E3004-APP and by the wave 2 integration harness; these five are the contract's own tests and no legacy id is renumbered.

### 17. Guardrails

- No business value in the body: the plan terms, the validity period and the band are values in force of the parameters, the rule package and the affordability result, and the contract fixes only types and rules (BR4).
- No band column, no band constant and no band reference row: the band is request-context and is recorded with the offer on the decision record (BR3).
- No personal data in the schema, an example, a fake or a log: the body carries amounts, counts, rates and dates, the case is identified by its ID outside the body, and the scan fails the build otherwise (BR10).
- No path, no response and no error code of this contract's own: the operation, its envelope and its statuses belong to RWB-S2-E3002-CON, and `/treatments/{treatmentId}/submit` is not published (BR1, BR5).
- No cross-schema reference and no foreign key across services; the boundary test fails the build (DP-01).
- No case table read: the case status stays rwb-case's and reaches the stage on the case signal, and the case-status mock is test-only (BR9; ASM-3062).
- No record written outside the library's `MANDATORY` transaction, and no ledger row: `decision_log_entry` is P7's and is named here only (DP-03; DP-01).
- A published version is never edited in place: a breaking change raises major version 2 with a migration note (BR8).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-001 | A restructure proposed in the collections system reaches the restructuring officer with the case, and the case does not leave the Workbench | Program, 5.9 | FEAT-TRT-04 | 07 Route, settle and claim | R-RES-04; R-RES-07 | TC-S2-E3004-CON-01, TC-S2-E3004-CON-05 |
| REQ-S2-002 | An offer to a customer carries a validity period, and expiry returns the case to the status it came from | Program, 5.9 | FEAT-TRT-04 | 07 Route, settle and claim | R-RES-15; BR3; BR4 | TC-S2-E3004-CON-01, TC-S2-E3004-CON-04 |
| Legacy test set RWB-E3-004 | TC-E3-004-01, TC-E3-004-02, TC-E3-004-03, TC-E3-004-04, TC-E3-004-05, TC-E3-004-06 | Program, 5.9 | FEAT-TRT-04 Offer a TDR plan | 07 Route, settle and claim | R-RES-04, R-RES-07, R-RES-15 | Executed by RWB-S2-E3004-APP; not owned here |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3004-APP | App development | H consumer: builds the plan branch, the plan columns, the offer timer and the record write against this contract and its fakes |
| RWB-S2-E3002-CON | Contract | Referred to: the offer operation, its envelope, its `Treatment` response and its error set that this body is published on. This contract adds no build dependency of its own |
| RWB-S2-E3001-CON, RWB-S2-E3001-APP | Contract, App development | Referred to: the treatment entity and its fields, which this body validates against |
| RWB-S2-E3005-APP | App development | The ACE affordability result that carries the band and the rule version onto the body |
| RWB-PLT-E1027-CON | Contract | DP-03: the local decision-record library that records the band with the offer |
| RWB-PLT-N001-CON | Contract | DP-19: the gateway-bff composite route through which SCR-14 and SCR-15 bind the body |
| RWB-PLT-DB, the per-service DB stories | Database | X: the schema, login and grants of `rwb_treatment` in which `treatment` sits |
| The wave 2 integration harness | Integration | I: the cross-service proof of the same legacy key against the live owners |

### 19. Out of scope

- The offer operation, the `Treatment` response, the envelope and the error set: RWB-S2-E3002-CON.
- The plan branch of the workflow, the plan columns write, the offer timer, the band application and the record write: RWB-S2-E3004-APP.
- The ACE affordability calculation, its outcome and the band it returns: RWB-S2-E3005-APP and RWB-S2-E3005-CON.
- The treatment entity, its other fields and its states: RWB-S2-E3001-APP and RWB-S2-E3001-CON.
- The decision-record library, its DDL template, its envelope and its exceptions: RWB-PLT-E1027-CON and RWB-PLT-E1027-APP; the central ledger: RWB-P7-E1027-APP.
- The rule package registry and the rule version labels: P7 rwb-decision, RWB-P7-E1073-CON.
- The case status, the assignment and the `timer` table: rwb-case (P3), RWB-P3-E2004-APP and its contract.
- SCR-14 and SCR-15, their field list and the gateway-bff composite route: the platform edge story and the screen owners (DP-19).
- The settlement range check and the below-floor approval: RWB-S2-E3002-APP and RWB-S2-E3003-APP.
- The real cross-service proof of the plan body, the band and the record: the wave 2 integration harness.

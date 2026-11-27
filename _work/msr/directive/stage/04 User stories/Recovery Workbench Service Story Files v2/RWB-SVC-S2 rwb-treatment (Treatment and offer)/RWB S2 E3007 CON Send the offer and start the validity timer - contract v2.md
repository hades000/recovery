# RWB-S2-E3007-CON Send the offer and start the validity timer - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E3-007 for rwb-treatment (S2, Treatment and offer). This document publishes the release element of the offer — the `OfferRelease` body, its properties and their mapping to the `treatment` field set of TSD S2 T3.1, the validity rule that turns a release instant and a period in force into `valid_until`, the body and the key of the service event that dispatches the offer to rwb-comms, the input of the validity timer, the versioning rule and the fakes — on base `/api/recovery/treatment/v1` (DP-13), with the decision record written through the library of RWB-PLT-E1027-CON (DP-03), the event on `rwb.treatment.events.v1` (DP-14) and the screens reached through the gateway-bff composite route (DP-19). The legacy acceptance criteria stay with RWB-S2-E3007-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-S2-E3007-CON-L252). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (13 resolved, 10 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3007-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-007 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S2-E3007-CON-16) |
| Contract version | 1 (major version 1, base /api/recovery/treatment/v1) |
| Open decisions | DL10 closed on its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863, confirmed by the programme directive |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **contract owner of rwb-treatment**, I want **the published release body of the offer — the `OfferRelease` element, the validity rule, the dispatch event and its body, the timer input, the versioning rule and the fakes — instead of the monolith's in-process send with an unstated validity date**, so that **the release story, the screens, the letter's owner, the payment owner and the wave 2 integration harness can build against one frozen release body and one stated validity rule from Day 1, and no validity period is ever hard-coded**.

The contract covers exactly five things:

- the `OfferRelease` element and its six properties, and the operation it belongs to — the release form of `POST /treatments/{treatmentId}/offer`, declared by RWB-S2-E3002-CON and named, not redeclared, here (DP-13; Architecture v5 slide 18);
- the validity rule: the validity date is the release date plus the validity period in force, the period is read and never a constant, and the answer is written to `valid_until` (DF-TRT-010) or the release is refused (BR-S2-007; FSD A2.7.3.1);
- the dispatch: the service event `rwb.treatment.TreatmentApproved.v1` (EV-10) on `rwb.treatment.events.v1`, its key and its body, consumed by rwb-comms to issue the offer letter and by rwb-payment to expect the money, with no customer value in it (DP-09, DP-14; Architecture v5 slide 42 row 10);
- the timer input: the three facts the durable validity timer may hold, and the expiry announcement MSG-S2-003, so that the wait is a timer and not a routed state;
- the versioning rule and the fakes: major version 1, the pinning rule and the drift test, and the five fakes every consumer builds against.

It does not own: the offer operation, its envelope, its `Treatment` response and its error set, which are RWB-S2-E3002-CON; the release branch of the workflow, the `valid_until` write, the record write and the timer itself, which are RWB-S2-E3007-APP; the treatment entity and its states, which are RWB-S2-E3001-APP and RWB-S2-E3001-CON; the plan terms and the band, which are RWB-S2-E3004-APP and RWB-S2-E3005-APP; the letter template and the channel, which are rwb-comms' (P6); the decision-record library, which is RWB-PLT-E1027-CON; the case status, which is rwb-case's (DP-01; ASM-4367); and the screens, which are the platform edge story's and the screen owners' (DP-19).

### 2. Business rationale

An offer that reaches the customer without a validity date is not an offer the bank can enforce or plan against, and the requirement says so plainly: an offer to a customer carries a validity period, and expiry returns the case to the status it came from (REQ-S2-002; FSD S2 v3, "Requirements served"). The feature's own description adds the second fact: the Workbench sends the offer and starts the validity clock, and the wait is a timer, not a routed state (FSD S2 v3, section A2.7.2). Neither fact has a shape today. No source document fixes a release body, a validity period key or an expiry announcement, and the legacy story carries only the sentence and the two rule rows (GAP-2659).

In the monolith the send was an in-process call in one deployable, so no payload was ever written down and the validity date was whatever the caller computed. Architecture v5 changes all three: rwb-treatment accepts the offer operation on `/treatments` (Architecture v5 slide 18), the business event topics carry the service's events and rwb-comms subscribes to S2's (Architecture v5 slides 13 and 42), and the clock becomes a durable timer inside the stage workflow because the catalogue retires `TimerDue` for that reason (Architecture v5 slide 42, event 18; Temporal and Drools Design slide 18). A published body is therefore the only place where the officer's release, the letter and the payment expectation meet.

Two facts make the contract urgent rather than tidy. The first is the period. The routing workbook states an offer validity of fourteen days on R-RES-09, R-RES-11 and R-SET-06 and a two-working-day clock on R-RES-04, but no parameter key exists for either and TSD S2 T3.1 has no validity-period column: left to the implementers, one team stores the period, one team hard-codes fourteen and the rule version becomes unprovable, which contradicts BR-S2-007 (no value a business person may change is written in code) and AC1 and AC3 of the legacy story. The contract therefore fixes the period as a value in force read at the release, and fixes `valid_until` as the only column the answer is written to (GAP-2659; ASM-4368). The second is the send. The legacy data table lists `v_ace_customer` because the monolith filled the letter from it; in the target the views are read only by rwb-source-data and no service puts personal data in an event (Architecture v5 slide 8; Template and Rules §R7.2 s17). The body therefore carries facts and identifiers only, and the addressee is resolved where the letter is built (GAP-2659; ASM-4366).

The fake is the Day-1 unblocker. RWB-S2-E3007-APP, the two screen stories, rwb-comms' letter work, rwb-payment's expectation and the wave 2 integration harness can build and test the release, the validity date and the refusal paths before any live route exists, and the release story can prove its own contract conformance before an environment is booked (Template and Rules §R5.4 class C, §R5.7).

### 3. Preconditions

- The validity date has a column and only one: `valid_until` (DF-TRT-010, date) on `treatment` in schema `rwb_treatment`, owned by S2 (DP-01; TSD S2 T3.1).
- The offer operation exists and is another contract's: `POST /treatments/{treatmentId}/offer` on base `/api/recovery/treatment/v1`, declared by RWB-S2-E3002-CON with its envelope and its error set (DP-13; Architecture v5 slide 18).
- The service event exists and is this service's only one: `rwb.treatment.TreatmentApproved.v1` (EV-10) on `rwb.treatment.events.v1`, which rwb-comms and rwb-payment consume (DP-14; Architecture v5 slides 13 and 42; Ownership Map).
- The period and the clock lengths are named by no model: the routing workbook carries them in its service-level column only, so the keys are this contract's working read (GAP-2658, GAP-2659; ASM-4368).
- The release instant has no column: no source gives `treatment` a send-date, a channel or a letter reference, so the instant is a request-context fact recorded with the release (GAP-2659; ASM-4369).
- The decision record is written through RWB-PLT-E1027-CON with `@Transactional(propagation = MANDATORY)`, refusing with MSG-P7-009 and failing with MSG-P7-003; `decision_record` is a library object in `rwb_treatment` and `decision_log_entry` is P7's (DP-03, DP-01).
- The gateway-bff composite route of RWB-PLT-N001-CON exists, so the screens' binding to the release is named and not declared here (DP-19).
- The access rule is the platform guard library's: capability area "Treatment and offer", right U for the release and right R for the read, with RW-RESTRUCT holding CRUA and RW-CASEOWN CRU (TSD S2 T6.1; ASM-4367).
- The legacy message texts this body raises are kept unchanged: MSG-GEN-001, MSG-P4-002, MSG-P7-003, MSG-P7-009 and MSG-S2-003.
- No build dependency and no approval stop: a CON story is Day 1 by rule (Template and Rules §R5.7) and is published at status Draft (realignment v1).

### 4. Flow

1. The contract author fixes the element: `OfferRelease` with six properties, their types taken from TSD S2 T3.1 where a column exists and from the offer facts where it does not, and nothing else.
2. The author fixes the validity rule: the date is the release date plus the period in force, the arithmetic is stated, a date before the release instant is refused, and the answer lands in `valid_until` and nowhere else.
3. The author writes the dispatch section: the event name, the topic, the key `caseId`, the body property by property, the consumer set and the no-customer-value rule.
4. The author writes the timer section: the three facts the durable timer may hold, the expiry announcement, and the statement that no `timer` row and no Schedule exists.
5. The author writes the operation section: the path, the method, the right and the idempotency header, all named as RWB-S2-E3002-CON's, with this contract's body attached to it.
6. The author writes the versioning and pinning section: major version 1, the compatible-versus-breaking rule and the pinning obligation of the five consumers.
7. The schema and lint steps run: the body validated against the element and the `treatment` field set, the event body scanned for personal data, and a body carrying a customer field refused.
8. The fakes are generated from the same example set: the release fake, the decision-record fake, the case-status mock, the rwb-comms consumer stub and the route fake.
9. The drift test runs the fakes against the document on every change and fails the build on any difference.
10. The document and the fakes are published at v1, and RWB-S2-E3007-APP, the screen stories, the letter and payment consumers and the wave 2 integration harness pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The body is published without `treatmentId`, `releasedAt` or `validityDate`, or with a property that is not in the element | The schema validation fails the build; the element holds exactly six properties and the required set is fixed | None | AC1, AC2 |
| X2 | A body carries a customer field, an address, an account or a document reference | The request is refused as a contract violation and the lint fails the build; the addressee belongs to the letter | MSG-GEN-001 | AC1, AC3 |
| X3 | The validity date is before the release instant, or the period in force is absent | The release is refused with the field named; nothing is written and no event leaves | MSG-GEN-001 | AC2 |
| X4 | A property carries a value outside its type or domain | The release is refused with the field named; nothing is written | MSG-GEN-001 | AC2, AC4 |
| X5 | The body is published on a path of its own, or on the treatment submit path instead of the offer operation | The drift test and the lint fail the build; the release runs on the operation RWB-S2-E3002-CON publishes | None | AC1, AC5 |
| X6 | A breaking change is made to a property, the validity rule, the event body or the key | The change raises major version 2; v1 is never edited in place and stays readable | None | AC5 |
| X7 | A value the consumers need is named by no source — the period key, the release instant's home or the event body | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-2659; ASM-4369) | AC2, AC3, AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document and a fake set; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | The example values, the property order and the description texts are open until v1 is frozen; the six properties, the required set, the validity rule, the event body and the no-personal-data rule are fixed |
| Valuable | Unblocks the release story, the two screen stories, the letter consumer, the payment consumer and the integration harness with one release body and one validity rule on Day 1 |
| Estimable | One element, one validity rule, one event body, one timer input, one versioning rule and five fakes |
| Small | One sprint for the document, the schema, the fakes and the drift test |
| Testable | Each criterion below is one schema, lint or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Offer release and validity contract

  Background:
    Given the rwb-treatment contract document is published at major version 1
    Given the treatment table carries the 33 fields of TSD S2 T3.1 in schema rwb_treatment
    Given the release body is published on the offer operation of the same service and declares no path of its own

  Scenario: AC1 The OfferRelease element is published on the offer operation (new, D-RCV-60)
    Given the element section of the contract document
    When it is validated and linted
    Then it publishes OfferRelease with exactly six properties: treatmentId, treatmentType, offerAmount, releasedAt, validityDate and approvalLevel
    Then the body is the request of the release form of POST /treatments/{treatmentId}/offer on base /api/recovery/treatment/v1, the operation declared by RWB-S2-E3002-CON and named here, not redeclared
    Then the response of the operation is the Treatment of RWB-S2-E3002-CON and this contract adds no second path and no second operation
    Then the access is capability area Treatment and offer with right U for the release and right R for the read, checked by the platform guard library and declared here as the right only
    Then no property names a customer, an address, an account or a document, and a body that carries one is refused

  Scenario: AC2 The validity rule turns a release and a period in force into one date (new, D-RCV-60)
    Given the validity section of the document, the treatment field set of TSD S2 T3.1 and the parameters in force
    When a release is computed
    Then validityDate is the release date plus the validity period in force and is written to DF-TRT-010 valid_until, date, the only column the answer lands in
    Then the validity period is read as a value in force and is exported as a parameter key, and no period, no date and no fourteen-day literal appears in the code
    Then releasedAt is required, maps to no column and is recorded with the release on the decision record, because TSD S2 T3.1 gives the send instant no column
    Then a validityDate before releasedAt, or an absent period in force, is refused with MSG-GEN-001 and the field name before any write
    Then the offer-preparation clock of R-RES-04 is a separate value in force and this contract fixes no number for either value

  Scenario: AC3 The dispatch event and its body are published (new, D-RCV-60)
    Given the dispatch section of the document and the service topic
    When the event body is validated and scanned
    Then the event is rwb.treatment.TreatmentApproved.v1 on rwb.treatment.events.v1 with key caseId, in the CloudEvents envelope of the platform
    Then its body is exactly treatmentId, caseId, treatmentType, offerAmount, validityDate, approvalLevel, approverRole, finalCall, decidedAt, ruleId and ruleVersion
    Then the consumers are rwb-comms, which issues the letter on the consented channel, and rwb-payment, which expects the money
    Then no name, address, account, document or other personal value appears in the body, the example or a fake, and the scan fails the build otherwise
    Then the event leaves only through this service's outbox in the release transaction, and a refused, declined or expired offer publishes nothing

  Scenario: AC4 The validity timer input and the expiry announcement are fixed (new, D-RCV-60)
    Given the timer section of the document
    When the timer input is compared to the durable timer of the workflow
    Then the timer holds caseId, treatmentId and validityDate only, and no customer value and no document reference
    Then the wait is a durable timer inside TreatmentWorkflow on task queue rwb-treatment, with no timer row, no polling job and no Schedule
    Then the expiry is announced with MSG-S2-003 and the date, and the case move on expiry (R-RES-18) is not part of this contract

  Scenario: AC5 Versioning separates a compatible change from a new major version (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published property, rule, event or key
    Then an added optional property keeps major version 1 and is accepted by the registry in BACKWARD mode
    Then a change to a property name, a type, the required set, the validity rule, the event body or the key raises major version 2, and v1 is never edited in place
    Then RWB-S2-E3007-APP, the screen stories, the letter consumer, the payment consumer and the wave 2 integration harness pin a published version and raise a change request rather than a private variant

  Scenario: AC6 The fakes answer the document and the drift test fails on any difference (new, D-RCV-60)
    Given the fake set generated from the same example set as the document
    When the contract test runs the release fake, the decision-record fake, the case-status mock, the consumer stub and the route fake
    Then the release fake answers a complete body, a refused body with MSG-GEN-001 and its field, a body carrying a customer field with the same refusal, and a validity date before the release instant with the same refusal
    Then the decision-record fake answers an accepted record, a refusal with MSG-P7-009 and a failure with MSG-P7-003, and the consumer stub records the envelope, asserts the absent customer field and answers a redelivery
    Then the case-status mock answers IN_FCR_QUEUE and AWAITING_CREDIT_APPROVAL for the two criteria of RWB-S2-E3007-APP, and the route fake answers the two screen reads one hop each
    Then the drift test of every consuming story fails the build on any difference from section 12 and section 13

  Scenario: AC7 The tables of section 12.7 are named here and never created, read or written by this contract (new, D-RCV-60)
    Given the table set of section 12.7 and the schema of each table
    When the contract and its migrations are linted for table references
    Then treatment is written only in valid_until and no column is created or changed
    Then decision_record, decision_log_entry and timer are named here and never created, read or written by this contract
    Then no foreign key and no reference across a service boundary appears, and the boundary test fails the build otherwise

  Scenario: AC8 A value the consumers need that no source names is published as the working read and the gap stays open (new, D-RCV-60)
    Given the period key, the release instant's home and the event body are named by no source
    When the contract publishes one of these values
    Then the value is published as the working read of the assumption with GAP-2659 and ASM-4369
    Then the gap stays open and no value is presented as settled

  Scenario: AC9 Every business rule of section 8 is covered by a criterion or a test row (new, D-RCV-60)
    Given the business rules BR1 to BR11 of section 8
    When the document is linted for coverage against sections 7 and 16
    Then each rule BR1 to BR11 is named in a Covers cell of section 16
    Then a rule named by no test row fails the build, and an architecture constraint may be proven by the boundary test of AC7 instead

  Scenario: AC10 The release and the read answer 401, 403 and 404 on their refusals and no answer carries a customer value (new, D-RCV-60)
    Given the release operation and the read of the offer on base /api/recovery/treatment/v1
    When a call carries no credential, lacks the right of BR9, or names a treatment that does not exist
    Then the call is answered 401, 403 or 404 respectively
    Then no answer body carries a customer, address, account or document value
```

These criteria are new: no legacy acceptance criterion is repeated here — **AC1 to AC4 of RWB-E3-007 stay with RWB-S2-E3007-APP** — and every identifier comes from the legacy story, Architecture v5, the TSD, the routing workbook or the Temporal and Drools Design, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The release body is one element of six properties, three of them required, published on the offer operation of the same service as `POST /treatments/{treatmentId}/submit` (read as `POST /treatments/{id}/offer` on Architecture v5 slide 18), and this contract declares no path, no response, no error code and no `GET /treatments` list of its own | Architecture v5 slide 18; RWB-S2-E3002-CON; DP-13; GAP-1699; GAP-2659 |
| BR2 | The validity date is the release date plus the validity period in force, and the only column it lands in is `valid_until` | REQ-S2-002; TSD S2 T3.1 DF-TRT-010; ASM-4368 |
| BR3 | No value a business person may change is written in code: the validity period and the offer-preparation clock are values in force, exported as parameter keys by this contract | FSD A2.7.3.1 BR-S2-007; ASM-4368 |
| BR4 | The release instant has no column, so it is a request-context fact recorded with the release on the decision record | GAP-2659; ASM-4369 |
| BR5 | The dispatch is one event, `rwb.treatment.TreatmentApproved.v1` on `rwb.treatment.events.v1` with key `caseId`; its consumers are rwb-comms and rwb-payment | EV-10; DP-09, DP-14; Architecture v5 slide 42 row 10; GAP-2658; GAP-2659 |
| BR6 | Neither the event body, the timer input nor an example carries a customer value; the letter resolves its own addressee | DP-09; Template and Rules §R7.2 s17; ASM-4366 |
| BR7 | The wait is a timer, not a routed state: the validity clock is a durable timer inside `TreatmentWorkflow` through the workflow kit; no Quartz table, job or connection is used, and this contract declares no Schedule and no job | FSD A2.7.2; Architecture v5 slide 42 event 18; ASM-4368 |
| BR8 | A refused body names its field with MSG-GEN-001 before any write; the record path fails with MSG-P7-003 and refuses with MSG-P7-009, and the apply step rolls back | RWB-E3-007 validation table; DP-03; RWB-PLT-E1027-CON |
| BR9 | The access of the operation is capability area Treatment and offer, right U for the release and right R for the read, checked by the rwb-access authorise check (DP-08) | TSD S2 T6.1; ASM-4367; DP-08 |
| BR10 | A published version is never edited: a compatible change stays in major version 1 and a breaking change raises major version 2 | Template and Rules §R5.4 class C; §R7.2 |
| BR11 | The case status is not part of this body and is not read here: the status stays rwb-case's and reaches the stage on the case signal | ASM-4367; DP-01 |

### 9. State transitions

None of its own: a contract document has no runtime state. Three vocabularies are fixed here and the runtime behind them is specified in RWB-S2-E3007-APP section 9.

| Object | State | Meaning in the contract |
|---|---|---|
| Release body | Received | The body arrived on the offer operation and no rule has run |
| Release body | Validated | The six properties passed their type, domain and cross-property rules and the period in force was present |
| Release body | Refused | A property failed, a customer field was named or the date preceded the release; the field is named and nothing is written |
| Release body | Released | `valid_until`, the decision record and the EV-10 outbox row were committed together |
| Validity timer | Armed | The durable timer runs to `valid_until` inside the stage workflow |
| Validity timer | Fired | The validity date was reached, MSG-S2-003 names it, and the case move is rwb-case's |
| Validity timer | Cancelled | A signature, a decline or a new offer ended the wait before the date |
| Contract version | v1 | The published version every consumer pins |
| Contract version | v2 | Raised by a breaking change; v1 stays readable and is never edited |

The case statuses of the release — `IN_FCR_QUEUE`, `WITH_FCR_OFFICER`, `AWAITING_CREDIT_APPROVAL`, `OFFER_WITH_CUSTOMER` — are rwb-case's vocabulary and are named here only as the context the body is released in (DP-01; ASM-4367).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the element, the validity rule, the dispatch section and the fakes |
| The rwb-treatment tech lead | Approves a breaking change and freezes a version of the release body |
| The solution architect | Confirms that the release rides the offer operation and that no path of its own is published (GAP-2659; ASM-4369) |
| The rwb-comms owner (P6) | Confirms the event body and the key as the letter's input, and that the addressee is resolved on its own path |
| The rwb-payment owner (P8) | Confirms the offer facts the payment expectation needs |
| The S1 owner of the payoff and range calculation | Confirms the offer facts the body names and their freshness rule |
| The service team of rwb-treatment (RW-TRIBE) | Consumes the contract in RWB-S2-E3007-APP, pins the version and raises a change request rather than a private variant |
| The screen owners, RW-RESTRUCT and RW-CASEOWN | Bind the validity date and the release state through the gateway-bff composite route; RW-RESTRUCT holds CRUA and RW-CASEOWN CRU in capability area Treatment and offer |
| RW-PLATADM | Receives the incident that a refused or failed record raises |
| No delegation of authority level applies | A release body is a technical artefact, not a credit decision |
| The rwb-access authorise check (DP-08) | Grants or refuses the release (right U) and the read (right R) in capability area Treatment and offer before the operation runs |

No personal name, no email address and no credential appears in the document, an example or a fake. Where an actor must be named, the example uses a role code or a user identifier only.

### 11. Data

| Item | Value | BR Field ID |
|---|---|---|
| Business data published | None. The document publishes a body, its property types, the field identifiers of the `treatment` columns it maps to, the event body and the message identifiers it raises; no customer, account or case value appears | None |
| Release body published | The six properties of section 12.1, with the field identifiers DF-TRT-001, DF-TRT-004, DF-TRT-007, DF-TRT-010 and DF-TRT-011 for the five that map to a column | DF-TRT-001, DF-TRT-004, DF-TRT-007, DF-TRT-010, DF-TRT-011 |
| Release instant published | `releasedAt` has no field identifier and no column: its home is Not specified in the source documents (GAP-2659; ASM-4369) | Not specified in the source documents (DOR-RWB-S2-E3007-CON-7) |
| Personal data | None. The body, the event and the examples carry case IDs, treatment IDs, codes, amounts and dates; the addressee is the letter owner's | None |
| Tables published | `treatment` only, as the field set the body validates against; this contract creates no table and adds no column, and `decision_record` is RWB-PLT-E1027-CON's | DF-TRT-001, DF-TRT-004, DF-TRT-007, DF-TRT-010, DF-TRT-011 for `treatment`; `decision_record`: Not specified in the source documents (DOR-RWB-S2-E3007-CON-7) |
| Retention | Not applicable: the contract stores nothing. The retention of `valid_until` and of the decision record belongs to the table owners | Not applicable |

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). This contract provides the release body of one operation whose path, envelope, response and error set are declared by RWB-S2-E3002-CON; it declares no operation of its own and no second path.

| Item | Value |
|---|---|
| Operation | The release form of `POST /treatments/{treatmentId}/offer`, declared by RWB-S2-E3002-CON and named here |
| Body | `OfferRelease` |
| Response | `Treatment` of RWB-S2-E3002-CON, with `valid_until` set from the validity rule |
| Access | Capability area Treatment and offer, right U, scope applied, checked by the platform guard library |
| Idempotency | `Idempotency-Key` header of the operation |
| Errors | The error set of RWB-S2-E3002-CON: 400 or 422 with MSG-GEN-001 and the field, 401, 403 with MSG-P4-002, 404, 409, 503, and MSG-P7-003 and MSG-P7-009 on the record path |

| Property | Type | Required | Maps to | Note |
|---|---|---|---|---|
| `treatmentId` | uuid | Yes | DF-TRT-001 `id` | The treatment being released |
| `treatmentType` | varchar(20) LOV-TREATMENT | No | DF-TRT-004 `treatment_type` | Restructure, settlement or deed in lieu; read from the record when absent |
| `offerAmount` | numeric(18,2) | No | DF-TRT-007 `offer_amount` | The amount the customer is offered; read from the record when absent |
| `approvalLevel` | varchar(4) LOV-APPROVAL-LEVEL | No | DF-TRT-011 `approval_level` | The level that approved the offer; read from the record when absent |
| `releasedAt` | timestamptz | Yes | none | The release instant; a request-context fact recorded on the decision record, because the table has no column |
| `validityDate` | date | Yes | DF-TRT-010 `valid_until` | The answer of the validity rule; the only column the release writes |

The element is this contract's working read. No source document fixes a release body: TSD S2 T3.1 gives `valid_until` and the offer terms but no release element, no release instant and no period, FSD A2.7 names the send without a shape, and the legacy story names only the sentence and the rules. The six properties are therefore published with the gap and the assumption, and every one of them either maps to a column or is stated as request-context (GAP-2659; ASM-4369). The path is the one RWB-S2-E3002-CON publishes; the submit form named by API Specification v5 and TSD S2 T-A.1 API-S2-004 is carried by that operation and is not republished here.

#### 12.2 REST operations consumed

None. The contract calls no service. The case status stays rwb-case's and reaches the stage on the case signal, the rule package version arrives on its event, the decision record is written in process through RWB-PLT-E1027-CON, and the period in force arrives from the parameters contract as a value the release story passes in (DP-03; ASM-4367, ASM-4368).

#### 12.3 Events published

| Event | Topic | Key | Body | Use |
|---|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | `caseId` | treatmentId, caseId, treatmentType, offerAmount, validityDate, approvalLevel, approverRole, finalCall, decidedAt, ruleId, ruleVersion | EV-10: the dispatch of a released offer to rwb-comms for the letter and to rwb-payment for the expectation of the money (Architecture v5 slide 42 row 10; DP-14) |

| Envelope element | Value |
|---|---|
| `id` | One UUID per release |
| `source` | `rwb-treatment` |
| `type` | `rwb.treatment.TreatmentApproved.v1` |
| `subject` | The treatment ID |
| `time` | The release instant |
| `datacontenttype` | `application/json` |
| Extension | `caseId`, used as the partition key |

The body is this contract's working read: Architecture v5 slide 42 names the event and the consumers, TSD S2 T5.3 names `TreatmentApproved` as published, and no source lists its fields, so the eleven properties are published here with the gap and the assumption (GAP-2659; ASM-4366). The event is written to this service's outbox in the release transaction and leaves after the commit; a refused, declined or expired offer publishes nothing. No customer value crosses it, because the letter resolves its own addressee.

#### 12.4 Events consumed

None. The rule package version is consumed by RWB-S2-E3007-APP's workflow on `rwb.decision.RulePackageInForce.v1` (EV-30) and is not a subscription of this contract; the contract only requires that the version in force is stamped on the record of the release (BR3).

#### 12.5 Workflows and activities

None. The contract defines no workflow and no activity. The release lives in `TreatmentWorkflow` of RWB-S2-E3007-APP on task queue `rwb-treatment` in namespace `rwb-recovery`, which calls `releaseOffer`, `recordAndApply`, `publishRelease` and the validity timer; the contract fixes the body and the rule those steps apply (ASM-4368).

#### 12.6 Schedules

None. The validity clock is a durable Temporal timer inside `TreatmentWorkflow` and belongs to RWB-S2-E3007-APP; this contract declares no Schedule and no job, and the legacy timer check is retired (ASM-4368; DP-10).

#### 12.7 Tables owned

| Table | Schema | Owner | This contract |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | The field set the body validates against: `id`, `treatment_type`, `offer_amount`, `valid_until` and `approval_level` of TSD S2 T3.1; no column is created or changed here, and no send-date column exists |
| `decision_record` | `rwb_treatment` | PLT, a library object | Named only: the shape, the DDL template and the home of `releasedAt` are RWB-PLT-E1027-CON's (DP-03) |
| `decision_log_entry` | `rwb_decision` | P7 | Named only: the central ledger is never read and never written by a consumer of this contract (DP-01) |
| `timer` | `rwb_case` | P3 | Named only: the validity clock is a durable timer, so no row is read or written here (ASM-4368) |

The contract declares no foreign key and no reference across a service boundary, and it creates nothing in another service's schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Release fake | The `OfferRelease` element and the release form of the offer operation | A complete body; a body missing one of the three required properties with MSG-GEN-001 and the field; a body carrying a customer field with the same refusal; a validity date before the release instant with the same refusal; an absent period in force with the same refusal |
| Decision-record fake | RWB-PLT-E1027-CON | An accepted record with chain sequence and entry hash, a refusal with MSG-P7-009 and the field, and a failure with MSG-P7-003 |
| Case-status mock | The case status on the forwarded case signal | `IN_FCR_QUEUE` and `AWAITING_CREDIT_APPROVAL`, the two statuses the criteria of RWB-S2-E3007-APP name |
| Consumer stub | The EV-10 publication | A subscriber that records the envelope, asserts the absent customer field, asserts the key `caseId`, and answers a redelivery of the same cloud event id |
| Route fake | The gateway-bff composite route of RWB-PLT-N001-CON | The SCR-14 release answer and the SCR-15 validity view, one hop each, both built from the same example body |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consuming story rather than as a surprise at run time. The case-status mock is test-only and stands for the signal answer recorded with ASM-4367; the consumer stub is test-only and is replaced by the wave 2 integration harness (GAP-2659; ASM-4366).

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 1 body on 1 operation declared by another contract | 0 | OpenAPI 3.1 fragment of the release form, merged into the service document of RWB-S2-E3002-CON |
| Kafka | 1 event body and its key (`rwb.treatment.TreatmentApproved.v1`) | 0 | Own topic `rwb.treatment.events.v1` with retry and `.dlt`; CloudEvents envelope; outbox |
| Temporal | 1 timer input | 0 | The timer itself belongs to RWB-S2-E3007-APP on `rwb-treatment` |
| File | 0 | 0 | No file crosses the contract; the letter is rwb-comms' |

### 13. Solution plan

**Package.** Contract artefact of rwb-treatment: the `OfferRelease` type in `th.co.scb.ace.workbench.recovery.treatment.api`, the OpenAPI fragment of the release form merged into the service document of RWB-S2-E3002-CON, the event schema of EV-10, and the validity, dispatch, timer, versioning and fake sections in the contract document. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery` (DP-13, DP-14). The implementation is RWB-S2-E3007-APP.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views; this body carries no ACE fact, because the addressee belongs to the letter | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The four rows are referred to here, not carried: this contract builds against nothing, and the two H dependencies are the consuming story's, which is why its own build list is empty by rule (Template and Rules §R5.7). DP-03 fixes the transaction rule the release and the record must satisfy, DP-05 is applied by removal because no `v_ace_*` fact appears in the body or the event, DP-13 fixes the base the body is published under, and DP-19 is the route through which SCR-14 and SCR-15 bind the validity date.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `OfferRelease` | Published type | The six properties, their types and their mapped field identifiers (BR1, BR2, BR4) |
| ReleaseSchema | Resource | The OpenAPI fragment of the release form, merged into the service document of RWB-S2-E3002-CON (BR1) |
| `TreatmentApproved` event schema | Resource | The eleven body properties, the envelope and the key of EV-10 (BR5, BR6) |
| ValiditySpecification | Document | The validity rule, the period as a value in force and the single landing column (BR2, BR3) |
| DispatchSpecification | Document | The event, its topic, its key, its consumers and the no-customer-value rule (BR5, BR6) |
| TimerSpecification | Document | The three timer facts, the expiry announcement and the no-row rule (BR7) |
| VersioningSpecification | Document | Major version 1, the compatible versus breaking rule and the pinning rule (BR10) |
| Fake set and fixtures | Test asset | The release fake, the decision-record fake, the case-status mock, the consumer stub and the route fake (AC6) |

**Database.** No change. `valid_until` already exists on `treatment` in `rwb_treatment` (DF-TRT-010) and is the only column the release writes; `releasedAt` has no column and is recorded on the decision record (BR4; GAP-2659; ASM-4369). The contract requires that no migration adds a send-date, channel or period column, and that `decision_record` stays the library's object.

**Configuration and reference data.** None of its own. The validity period and the offer-preparation clock are values in force of the parameters and the rule package, and this contract exports their keys rather than their values (BR3; ASM-4368). The treatment-type and approval-level lists are reference data read through the owner's contract, and the capability area and rights of the operation are the platform guard library's rows (BR9).

**Build steps**

1. Write the `OfferRelease` type with the six properties and their types from TSD S2 T3.1 (AC1, AC2).
2. Write the OpenAPI fragment of the release form and merge it into the service document of RWB-S2-E3002-CON; assert one path and no second path (AC1, AC5).
3. Write the validity rule with the period key, the single landing column and the refusal set (AC2).
4. Write the dispatch section and the event schema with the envelope and the key, and assert the absent customer field (AC3).
5. Write the timer section and the expiry announcement (AC4).
6. Write the versioning and pinning section with the compatible and breaking examples (AC5).
7. Generate the five fakes from the example set and write the drift test into the build of every consuming story (AC6).
8. Publish v1 and record the pinned version of RWB-S2-E3007-APP, the screen stories, the two consumers and the wave 2 integration harness (AC5).

**Feature flag.** `rwb.treatment.offer-release-contract`.

**Done when.** The element and the fragment validate against the service document, a complete body is accepted and each of the five refusals answers with MSG-GEN-001 and its field, the event schema proves the absent customer field, the five fakes answer every example, the drift test is green on RWB-S2-E3007-APP's build, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-GEN-001 | A required property is missing or a value is outside its type or domain | Enter {field}. | 422 with the field name, before any write |
| MSG-P4-002 | The caller's role does not hold right U in Treatment and offer | You cannot {action} here. Your role does not include it. | 403 of the operation, the guard library's answer |
| MSG-P7-009 | A record field is refused (log and incident, not the screen) | The decision record was refused: {field} is missing or not valid. | The library's `DecisionLogRecordInvalidException`, RWB-PLT-E1027-CON |
| MSG-P7-003 | The record cannot be written and the offer is not released | The action was not taken because the decision could not be recorded. Try again in a few minutes. | 503 of the operation, the library's `DecisionLogUnavailableException` |
| MSG-S2-003 | The offer reaches its validity date (raised by the release story, named here for the timer) | The offer to the customer ends on {date}. | Information, RWB-S2-E3007-APP |

The five texts are the legacy texts carried unchanged and this contract adds no message identifier of its own; MSG-GEN-001 and MSG-P4-002 are the legacy body's, MSG-P7-003 and MSG-P7-009 are the record library's, and MSG-S2-003 belongs to the release steps run by RWB-S2-E3007-APP. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story and none declared. SCR-14 Treatment record (Draft, submitted, approved, booked, broken; empty, loading, error and no access: Not specified in the source documents (CG-ALL-8586)) shows the validity date, the days left and the release state of the treatment; SCR-15 Settlement offer (Draft, below floor, approved, sent, accepted; empty, loading, error and no access: Not specified in the source documents (CG-ALL-8587)) shows the same facts for a settlement offer; both bind the `OfferRelease` properties and the response of the operation through the gateway-bff composite route and neither is built here (DP-19; RWB-PLT-N001-CON). The screens show the validity date as a read-only fact of the release and never invite an officer to type it, because the date is the answer of a rule and a period in force (BR2, BR3). The screen field list and the composite route specification belong to the platform edge story and the screen owners.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S2-E3007-CON-01 | AC1, BR1 | Contract | The element validated against the service document: six properties, their types, the five field identifiers, the required set, one path on the offer operation and no second path; a body carrying a customer field refused |
| TC-S2-E3007-CON-02 | AC2, BR2, BR3, BR4 | Contract | The validity rule: the date from the release instant and the period in force, the single landing column, the exported key, no literal in the code, and the two refusals |
| TC-S2-E3007-CON-03 | AC3, BR5, BR6 | Contract | The event schema: eleven body properties, the envelope, the key `caseId`, the two consumers and the scan for a customer field; a body with one refused |
| TC-S2-E3007-CON-04 | AC4, BR7 | Component | The timer input compared to the workflow's durable timer: three facts, no customer value, no `timer` row, no Schedule, and MSG-S2-003 at expiry |
| TC-S2-E3007-CON-05 | AC5, AC6, BR8, BR10, BR11 | Component | A compatible change accepted in BACKWARD mode and a breaking change raising major version 2; the five fakes answering every example, including the four refusals, the record failure, the redelivery and the two case statuses; the drift test failing on a one-property difference |
| TC-S2-E3007-CON-06 | AC7 | Contract | The table boundary of section 12.7: treatment written only in valid_until, the three named tables never created, read or written, no foreign key and no cross-service reference; a migration adding a table fails the build (ASM-3438) |
| TC-S2-E3007-CON-07 | BR9 | Component | The access of the operation: right U for the release and right R for the read in capability area Treatment and offer, checked by the rwb-access authorise check (DP-08); a call without the right is refused, and the refusal code is Not specified in the source documents (DOR-RWB-S2-E3007-CON-6) |
| TC-S2-E3007-CON-08 | AC8, BR4 | Contract | The working read of the period key, the release instant's home and the event body, each marked with GAP-2659 and ASM-4369, with the gap left open; a value presented as settled fails the build |
| TC-S2-E3007-CON-09 | AC9, BR1, BR2, BR3, BR4, BR5, BR6, BR7, BR8, BR9, BR10, BR11 | Contract | The coverage lint of section 8: each of BR1 to BR11 named in a Covers cell of section 16; a rule named by no test row fails the build |
| TC-S2-E3007-CON-10 | AC10, BR9 | Component | The release and the read: no credential answers 401, a refused right answers 403 and an unknown treatmentId answers 404; no answer carries a customer, address, account or document value |

The legacy test set of RWB-E3-007 is carried by RWB-S2-E3007-APP and by the wave 2 integration harness; these ten are the contract's own tests and no legacy id is renumbered.

### 17. Guardrails

- No business value in the body: the period, the dates and the clock are values in force, and the contract fixes only types, keys and rules (BR3).
- No customer value in the body, the event, an example, a fake or a log: the addressee belongs to the letter and the scan fails the build otherwise (BR6).
- No send-date, channel or period column: the release instant is request-context and the period is a parameter (BR2, BR4).
- No path, no response and no error code of this contract's own: the operation, its envelope and its statuses belong to RWB-S2-E3002-CON (BR1).
- No cross-schema reference and no foreign key across services; the boundary test fails the build (DP-01).
- No case table read and no case status in the body: the status stays rwb-case's and reaches the stage on the case signal (BR11; ASM-4367).
- No record written outside the library's `MANDATORY` transaction, and no ledger row: `decision_log_entry` is P7's and is named here only (DP-03; DP-01).
- A published version is never edited in place: a breaking change raises major version 2 with a migration note (BR10).
- Personal data: no name, address, account, document or other personal value appears in any body, event, example, fake or log of this contract, and the scan fails the build otherwise (BR6; DP-09).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-002 | An offer to a customer carries a validity period, and expiry returns the case to the status it came from | Program, 5.9 | FEAT-TRT-07 | 07 Route, settle and claim | R-RES-11; R-RES-18; BR2 | TC-S2-E3007-CON-01, TC-S2-E3007-CON-02, TC-S2-E3007-CON-04 |
| REQ-S2-001 | A restructure proposed in the collections system reaches the restructuring officer with the case, and the case does not leave the Workbench | Program, 5.9 | FEAT-TRT-07 | 07 Route, settle and claim | R-RES-04 | TC-S2-E3007-CON-02, TC-S2-E3007-CON-05 |
| Legacy test set RWB-E3-007 | TC-E3-007-01, TC-E3-007-02, TC-E3-007-03, TC-E3-007-04, TC-E3-007-05, TC-E3-007-06 | Program, 5.9 | FEAT-TRT-07 Send the offer and start the validity timer | 07 Route, settle and claim | R-RES-04, R-RES-11, R-RES-15 | Executed by RWB-S2-E3007-APP; not owned here |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3007-APP | App development | H consumer: builds the release branch, the `valid_until` write, the event publication, the validity timer and the record write against this contract and its fakes |
| RWB-S2-E3002-CON | Contract | Referred to: the offer operation, its envelope, its `Treatment` response and its error set that this body is published on. This contract adds no build dependency of its own |
| RWB-S2-E3001-CON, RWB-S2-E3001-APP | Contract, App development | Referred to: the treatment entity and the fields this body validates against |
| RWB-S2-E3002-APP, RWB-S2-E3003-APP, RWB-S2-E3004-APP, RWB-S2-E3005-APP | App development | The offer facts this body names: the settlement terms, the approval, the plan terms and the band |
| RWB-PLT-E1027-CON | Contract | DP-03: the local decision-record library that records the release instant with the release |
| RWB-PLT-N001-CON | Contract | DP-19: the gateway-bff composite route through which SCR-14 and SCR-15 bind the validity date |
| rwb-comms (P6) | App development | The letter the event dispatches, and the addressee it resolves on its own path |
| rwb-payment (P8) | App development | The expectation of the money a released offer sets up |
| RWB-PLT-DB, the per-service DB stories | Database | X: the schema, login and grants of `rwb_treatment` in which `treatment` sits |
| The wave 2 integration harness | Integration | I: the cross-service proof of the same legacy key against the live owners, including the letter and the payment expectation |

### 19. Out of scope

- The release branch of the workflow, the `valid_until` write, the record write, the event publication and the timer: RWB-S2-E3007-APP.
- The offer operation, the `Treatment` response, the envelope and the error set: RWB-S2-E3002-CON.
- The treatment entity, its other fields and its states: RWB-S2-E3001-APP and RWB-S2-E3001-CON.
- The plan offer, the affordability calculation and the band: RWB-S2-E3004-APP and RWB-S2-E3005-APP.
- The settlement range, the floor, the below-floor approval and the payoff freshness: RWB-S2-E3002-APP and RWB-S2-E3003-APP.
- The letter template, the consented channel, the addressee and the delivery evidence: rwb-comms (P6).
- The decision-record library, its DDL template and the central ledger: RWB-PLT-E1027-CON, RWB-PLT-E1027-APP and RWB-P7-E1027-APP.
- The rule package registry and the rule version labels: P7 rwb-decision, RWB-P7-E1073-CON.
- The case status, the assignment, the expiry and decline moves and the `timer` table: rwb-case (P3) and its stories, including R-RES-17 and R-RES-18.
- SCR-14 and SCR-15, their field list and the gateway-bff composite route: the platform edge story and the screen owners (DP-19).
- The real cross-service proof of the release, the event and the letter: the wave 2 integration harness.

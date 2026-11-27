# RWB-S2-E3016-CON Set up a deed in lieu buy-back rental - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E3-016 for rwb-treatment. The contract is published on Day 1 and fixes the rental elements the treatment carries (`rentAmount` in `offer_amount`, `firstRentDue` in `first_due_date`, `installmentsPaid` in `installments_paid`, and `rentalRef`, `autoDebitRef`, `autoDebitStatus`), the rule that the rental is a `treatment` row of type RENTAL and that no rental table is created, the event position, the compatibility rule and the fakes; the implementation is RWB-S2-E3016-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-S2-E3016-CON-L217). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 7 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3016-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Contract version | v1 (/v1 path) |
| Size | Squad sizes at refinement (DOR-RWB-S2-E3016-CON-16) |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **contract owner of rwb-treatment**, I want **the published contract of the buy-back rental — the elements the treatment carries for a rental (the rent, the first rental due date, the instalments paid and the rental, mandate and mandate-status references), the rule that a rental is a `treatment` row of type RENTAL and that no rental table is created, the event position of the rental on the service's own topic, the compatibility rule and the fakes — instead of the monolith's rental row in the shared `recovery` schema beside its `decision_log_entry` row and its in-process ATS and AMIS calls**, so that **RWB-S2-E3016-APP can build and test the rental stage on Day 1, rwb-payment and rwb-asset can pin the elements they read, and no team adds a rental table to hold what the treatment already holds**.

### 2. Business rationale

The monolith kept the whole rental in one place: the S2 service inserted the rental into the shared `recovery` schema, set the ATS debit in the same transaction boundary, wrote `decision_log_entry` with the rule version, read `v_ace_customer` and `v_ace_npa_asset` directly, and matched the proceeds in the same code. Three consequences followed that the target cannot keep. The rental had no shape of its own, so the rent, the due date and the mandate were distinguished by free text and screens. The facts had no owner outside the monolith, so the payment service could not match a rent instalment without re-reading a table it does not own. And a team adding an arrears follow-up would have added a table, and a team adding the mandate would have added another, so the same tenancy would be recorded three times.

In the 19-service target the case status is rwb-case's (ASM-4388), the record is the platform library's and local to the service (DP-03), the customer and NPA-asset facts are rwb-source-data's and arrive as facts (DP-05; ASM-4415), the AMIS rental record and the ATS mandate are rwb-asset's and rwb-integration's (ASM-4416), the receipts and the proceeds are rwb-payment's (ASM-4417). What is left for this contract is the part the other services and the screens depend on: what a rental treatment carries, that it is a treatment and not a table, and where the rental stands in the event landscape of the service. The TSD lists DF-TRT-001 to DF-TRT-033 with no rental reference, no mandate reference and no mandate status (TSD S2 T3.1), so the element names and their domains are Not specified in the source documents (GAP-2681; ASM-4419).

**The division of the legacy key is fixed.** This WP delivers the **contract**. The **implementation** — the rental stage of `TreatmentWorkflow`, its six activities and its calls to the owners — is **RWB-S2-E3016-APP**, and the **cross-service proof** is the wave 2 integration harness. The three legacy acceptance criteria **stay with RWB-S2-E3016-APP** and are not copied here: every criterion in section 7 is new (D-RCV-60) and tests only the contract deliverable in this title.

The contract has to exist before the code for three reasons. rwb-payment and rwb-asset build in the same wave and need the element names on Day 1. The element set is what stops the second table: a team that finds no field for the tenancy adds `rental` and the same rent is then recorded twice, once as a row and once as a record. And the compatibility rule lets the screens and the consumers pin a version while the stage is still being built. The fake is the Day-1 unblocker: the stage is built and tested before rwb-asset, rwb-integration or rwb-payment exists.

### 3. Preconditions

- The treatment of the case is rwb-treatment's own object in schema `rwb_treatment` (Ownership Map row `treatment`, owner S2), with DF-TRT-001 to DF-TRT-033 and `treatment_type` taking the value RENTAL of LOV-TREATMENT (TSD S2 T3.1 and T3.2).
- The published elements the rental reuses keep their names and types: `offer_amount` (DF-TRT-007) for the agreed rent, `first_due_date` (DF-TRT-029) for the first rental due date and `installments_paid` (DF-TRT-032) for the instalments paid. `rentalRef`, `autoDebitRef` and `autoDebitStatus` have no published element on the treatment, which is the gap this contract closes for the wave (GAP-2681; ASM-4419).
- The service owns one event in the catalogue, `TreatmentApproved` (EV-10), producer rwb-treatment, topic `rwb.treatment.events.v1`, consumers rwb-comms and rwb-payment; its envelope is fixed by RWB-S2-E3003-CON and this contract refers to it and never redefines it.
- No source names an event for the rental: the stage reports the outcome to the parent `CaseWorkflow`, and that absence is the gap recorded here (GAP-2680).
- The rules that give each step its answer are in force as data: R-DIL-32, R-DIL-33 and R-DIL-34, with the state names ASSET_ON_BOOKS, RENTAL_RUNNING and HANDED_TO_DISPOSAL (Business Rules and Routing Logic v4). The names and the arrears limit are reference values, never a list held by this contract (BR-S2-016).
- The asset record, the AMIS and ATS interfaces, the receipts and the proceeds are not this contract's: `asset` is S5's, the interfaces are P2's and S5's, and the payment facts are P8's (DP-01; ASM-4416; ASM-4417).
- The case statuses of the route are rwb-case's and never values of this contract (ASM-4388).
- The decision record is written through RWB-PLT-E1027-CON, whose write refuses with MSG-P7-009 and fails with MSG-P7-003; this contract declares the record's use and not its shape (DP-03).
- The schema registry is in BACKWARD mode and the AsyncAPI document per service is the contract, so the one event is registered against it.
- No build dependency and no approval stop: a CON story is Day 1 by rule and is published at status Draft (realignment v1).

### 4. Flow

1. The contract author fixes the element set of a rental treatment: the three elements that already exist (`offer_amount`, `first_due_date`, `installments_paid`) and the three named here, with their value domains and their absent-until rule.
2. The author fixes the no-new-table rule and states where each fact already lives: the `treatment` row, the library's `decision_record`, S5's `asset`, P8's `proceeds` and the ACE views of rwb-source-data.
3. The author writes the event section: this contract publishes no event type of its own, refers to the envelope of RWB-S2-E3003-CON, and states that the rental path publishes nothing and that the outcome reaches the case on the case signal.
4. The author writes the compatibility rule: which change keeps major version 1, which raises major version 2 with a new `ce_type`, and how a consumer pins a version.
5. The author writes the refusal and hold rules: a refused mandate, a stale data product and a disposal hand-off carry their reason code or their status on the treatment and publish nothing, and the two decision-record exceptions keep a step from taking effect.
6. The author writes the fake set: an element fake for the states of the rental, a consumer fake for rwb-payment and rwb-asset, and the decision-record fake reference.
7. The lint step runs: the element names compared with the API Specification and the TSD list, the treatment representation compared with the service's document, and the examples scanned for personal data.
8. The contract test runs the fakes against the document on every change and fails the build on any drift in this story and in RWB-S2-E3016-APP.
9. The document and the fakes are published at v1; RWB-S2-E3016-APP, rwb-payment and rwb-asset pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A team adds a `rental` or a `tenancy` table, or a second write path for the rent | The boundary and drift checks fail the build; the `treatment` row plus the decision record are the only places a rental fact lives | None | AC1 |
| X2 | A team adds an element for the rent, the mandate or the reference that duplicates a published one | The drift test against the treatment representation fails the build; `offer_amount`, `first_due_date` and `installments_paid` are used as they are | None | AC1 |
| X3 | A team publishes a rental event, or reuses the `TreatmentApproved` envelope for the rental | The contract test fails: no event type is added and EV-10 stays with the offer release of the deed in lieu | None | AC2 |
| X4 | A payload or an example carries a personal field, a tenancy document or free text | The personal-data scan fails the build; the elements carry references, figures and timestamps only | None | AC3 |
| X5 | A refusal or a disposal hand-off publishes an event, or a step updates the treatment while the record cannot be written | The contract test fails; the `MANDATORY` rule and the drift test keep a step without its record from taking effect | MSG-P7-003 | AC4 |
| X6 | An element is renamed, removed or retyped | The change raises major version 2 and a new `ce_type`; v1 is never edited in place and stays readable | None | AC5 |
| X7 | A value the consumers need is named by no source — the three element names, their domains, or the rental event | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-2681; ASM-4419) | AC1, AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document and fakes; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | The value domains, the example values and the fixture set are open until v1 is frozen; the six element names, the no-new-table rule and the event position are fixed |
| Valuable | Unblocks RWB-S2-E3016-APP, rwb-payment and rwb-asset on Day 1 and keeps one table out of the service plan |
| Estimable | One element set, one event position, one rule set, one fake set and one document |
| Small | One sprint for the document, the fakes and the lint rules |
| Testable | Each criterion below is one document, schema or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: the buy-back rental contract of rwb-treatment

  Background:
    Given the rwb-treatment contract document is published with major version 1
    Given the rental of a case is carried by a treatment of rwb-treatment in schema rwb_treatment
    Given the case status stays rwb-case's and reaches the stage on the case signal

  Scenario: AC1 A rental is a treatment row of type RENTAL and creates no new table (new, D-RCV-60)
    Given the element section of the contract document
    When it is validated against the treatment representation and the TSD
    Then a rental carries rentAmount, firstRentDue and installmentsPaid in offer_amount (DF-TRT-007), first_due_date (DF-TRT-029) and installments_paid (DF-TRT-032)
    Then it carries rentalRef, autoDebitRef and autoDebitStatus with no published field, each absent until its step has answered
    Then treatment_type is RENTAL of LOV-TREATMENT and one rental exists per case at a time
    Then the document declares that no rental table and no tenancy table is created, and names decision_record as the library object of DP-03, asset as S5's and proceeds as P8's
    Then a proposed rental table fails the boundary test

  Scenario: AC2 The rental adds no event and uses the one service envelope not at all (new, D-RCV-60)
    Given the event section of the document
    When the rental path is validated against the event catalogue of the service
    Then the service keeps one event type, rwb.treatment.TreatmentApproved.v1 on rwb.treatment.events.v1, published at the offer release of the deed in lieu and not on the rental path
    Then the rental start reaches rwb-payment through the case events of rwb-case and the case signal, and no event type is added
    Then a proposed rental event, or a rental body on the TreatmentApproved envelope, fails the contract test

  Scenario: AC3 The rental facts are carried once and re-keyed by no one (new, D-RCV-60)
    Given the data section of the document
    When a rental at RENTAL_RUNNING is validated against it
    Then rentalRef carries the reference its owner returns for the rental record and autoDebitRef the ATS mandate reference
    Then autoDebitStatus carries the mandate state its owner reports, and no state of the mandate is held by this contract
    Then the treatment carries no tenancy document, no customer name, no address and no measurement, and the document states that rwb-payment and rwb-asset hold them
    Then the personal-data scan fails the build on any of them

  Scenario: AC4 A refusal or a disposal hand-off is carried on the treatment and publishes nothing, and a failure to record stops the step (new, D-RCV-60)
    Given the refusal and hold section of the document
    When a refused mandate, a stale data product and an arrears hand-off are put through it
    Then the treatment carries the mandate state, the stale-product message identifier and the disposal hand-off, with the reason code in force
    Then no event is published and no outbox row is written on any of the three
    Then the decision record is written through DecisionRecordWriter with propagation MANDATORY, and a failed write answers MSG-P7-003 and rolls the rental back
    Then a refused field answers MSG-P7-009 with the field name and no event

  Scenario: AC5 A compatible change keeps major version 1 and a breaking change raises version 2 (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published element
    Then an added optional element keeps major version 1 and is accepted by the registry in BACKWARD mode
    Then a renamed, removed or retyped element raises major version 2 and a new ce_type, and v1 is never edited in place
    Then RWB-S2-E3016-APP, rwb-payment and rwb-asset each pin a published version and raise a change request rather than a private variant

  Scenario: AC6 The fakes answer the document and the drift test runs on both sides (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the element fake and the two consumer fakes
    Then the element fake answers a rental at each state, one with no mandate answer, one with a refused mandate and one with no rental reference
    Then the consumer fake of rwb-payment accepts the rent and the due date and refuses a rental with no instalment count
    Then the consumer fake of rwb-asset accepts the rental reference and refuses a rental with no asset fact
    Then the drift test fails on any difference from sections 12 and 13 in this story and in RWB-S2-E3016-APP

  Scenario: AC7 Every business rule of section 8 has a criterion, a test or a named guardrail (new, D-RCV-60)
    Given the business rules table of section 8
    When each rule from BR1 to BR9 is matched to the criteria of section 7 and the test cases of section 16
    Then each rule is covered by a criterion or a test case, or by a guardrail or boundary test named for it
    Then a rule with neither a criterion nor a test fails the contract test

  Scenario: AC8 A provided operation answers 401, 403 or 404 when the call is not allowed or the treatment is not found (new, D-RCV-60)
    Given the provided operations of the rwb-treatment contract document
    When a call without credentials, a call without the right and a call for a treatment that does not exist are sent
    Then the operation answers 401, 403 and 404 respectively
```

These criteria are new and test only the contract deliverable: no legacy acceptance criterion is repeated here — **AC1 to AC3 of RWB-E3-016 stay with RWB-S2-E3016-APP** — and every identifier comes from the legacy story, the TSD, Architecture v5, the BRD or the Business Rules and Routing Logic, character for character. The three element names, their domains and the absence of a rental event are Not specified in the source documents (GAP-2681; ASM-4419).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A rental is a `treatment` row of type RENTAL of LOV-TREATMENT, with `rentAmount` in `offer_amount`, `firstRentDue` in `first_due_date`, `installmentsPaid` in `installments_paid`, and `rentalRef`, `autoDebitRef` and `autoDebitStatus`; no rental table is created | GAP-2681; ASM-4414; TSD S2 T3.1 |
| BR2 | The rent, the first due date and the instalment count are figures and dates in force, never constants; the element carries a figure, a reference or a timestamp and never a limit, a threshold or a clock | BR-S2-016; FSD S2 A2.16.3.1 |
| BR3 | The service publishes one event type, `TreatmentApproved` (EV-10), on its own topic, in CloudEvents 1.0 binary mode with key `caseId`; the rental path publishes none and adds no field to it | Architecture v5 slide 42 row 10; RWB-S2-E3003-CON; GAP-2680 |
| BR4 | The rental facts carry references, figures and versions only: no name, no national identifier, no account number, no address and no tenancy document | NFR-054; NFR-053 |
| BR5 | A refused mandate, a stale data product and a disposal hand-off publish nothing and are carried on the treatment with the state or the reason code in force | R-DIL-32; R-DIL-33; R-DIL-34; BR-S2-016 |
| BR6 | Every step is recorded through DecisionRecordWriter with propagation MANDATORY, refusing with MSG-P7-009 and failing with MSG-P7-003, so a step that cannot be recorded does not take effect | DP-03; R-UNI-39; RWB-PLT-E1027-CON |
| BR7 | The asset record is S5's, the AMIS and ATS interfaces are theirs and P2's, and the receipts and the proceeds are P8's: this contract names them and declares no field, no read and no write of any; the AMIS rental record, the ATS mandate and the disposal hand-off are requested through rwb-asset and rwb-integration | DP-01; ASM-4416; ASM-4417 |
| BR8 | The case statuses ASSET_ON_BOOKS, RENTAL_RUNNING and HANDED_TO_DISPOSAL are rwb-case's: this contract declares no status value and no case event; the case status and the case task are moved by the parent CaseWorkflow | ASM-4388; GAP-2680 |
| BR9 | A published version is never edited: a backward-compatible change keeps major version 1, a breaking change raises major version 2 with a new `ce_type` (not a field or entity in LDM v9 or Data Classification v5; Not specified in the source documents (CG-ALL-8767)), and every consumer pins a version | Template and Rules §R7.2; Architecture v5 slides 42 and 43 notes |

### 9. State transitions

None in this story: a contract document has no runtime state. Two vocabularies are fixed here and the runtime behind them is specified in RWB-S2-E3016-APP section 9.

| Object | State | Meaning in the contract |
|---|---|---|
| Rental element set | Opened | `rentAmount` and `firstRentDue` are present and no mandate has answered |
| Rental element set | Mandated | `rentalRef` and `autoDebitRef` are present and `autoDebitStatus` carries its owner's answer |
| Rental element set | Receipting | `installmentsPaid` grows with each matched receipt and the due date moves by the rule in force |
| Rental element set | Handed off | The arrears passed the limit in force and the asset went to the disposal route |
| Rental element set | Closed | The treatment's `outcome` carries a LOV-TRT-OUTCOME value and `outcome_at` the time |
| Rental element set | Refused | The mandate was refused or the data product is stale; the rental is held with the owner's state |
| Contract version | v1 | The published version RWB-S2-E3016-APP, rwb-payment and rwb-asset pin |
| Contract version | v2 | Raised by a breaking change, with a new `ce_type`; v1 stays readable and is never edited |

The case statuses of the route — ASSET_ON_BOOKS, RENTAL_RUNNING, HANDED_TO_DISPOSAL — are rwb-case's. This contract refers to the point at which each element is written and holds no status list of its own.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the element section, the event position and the fakes |
| The owner of rwb-treatment | Approves a breaking change to the element set and freezes a version |
| The rwb-payment owner (P8) | Confirms the rent and the due date it matches against, and that the receipts and the proceeds are its own; this contract declares none of their fields |
| The rwb-asset owner (S5) | Confirms the rental reference it returns and the fields it keeps; this contract declares none of them |
| The rwb-integration owner (P2) | Confirms the AMIS rental record and the ATS mandate interfaces are its own |
| The rwb-case owner (P3) | Confirms that no case status and no case event is declared here, and that no rental event exists |
| The rwb-source-data owner (P1) | Confirms that the customer and NPA-asset facts reach the stage as facts and that no view is read here |
| RW-AUDIT, RW-COE | Audit the decisions through the P7 ledger and the local record, not through this contract |
| No delegation of authority level applies | A service contract is a technical artefact, not a credit decision |
| The rwb-access authorise check (DP-08) | Guards the REST operations of this contract; the check itself is DP-08's and is not restated here |

No personal name, no email address and no credential appears in the document, an example or a fake. Where a caller or an officer must be named, the example uses a role code or a user identifier only.

### 11. Data

| Item | Value | BR Field ID |
|---|---|---|
| Business data published | None. The document publishes element names, domains, codes and message identifiers; no customer, account or case value appears outside a synthetic example | BR4 |
| Element set published | `rentAmount` (`offer_amount`), `firstRentDue` (`first_due_date`), `installmentsPaid` (`installments_paid`), `rentalRef`, `autoDebitRef` and `autoDebitStatus`, with the absent-until rule of section 12.1: each of the three new names is absent until its step has answered, and the mandate state is as its owner reports it; the three new names are a working read (ASM-B2-S2-011-2, ASM-B2-S2-011-7) to be confirmed with the P8, S5 and P3 owners at the wave 2 contract stage | BR1, BR2 |
| Personal data | None. The rental and mandate references are system references, never a name, an address or a document; no account number and no national identifier appears. Each element of the set is classed as not personal data under Data Classification v5 | BR4 |
| Tables published | None created: the `treatment` row of S2, the library object `decision_record` of DP-03, S5's `asset`, P8's `proceeds` and P1's read of `v_ace_npa_asset` are named, and the document declares that no rental table is added. The `decision_record` is not a field or entity in LDM v9 or Data Classification v5 | BR1, BR7 |
| Field identifiers | `offer_amount` carries DF-TRT-007, `first_due_date` DF-TRT-029 and `installments_paid` DF-TRT-032; the three new elements carry no field ID in the TSD, which stops at DF-TRT-033 (GAP-2681; ASM-4419; working read ASM-B2-S2-011-2 and ASM-B2-S2-011-7) | BR1 |
| Retention | The treatment row and the local record follow their owners' retention; the decision record reaches the shared topic under the platform policy | BR1, BR6 |
| Reference data | LOV-TREATMENT (type RENTAL) is read; the reference-data contract is DP-06 and the parameters it reads are DP-07 | BR1 |

The element set is the one place where a business value could leak into the contract, so the document fixes that an element carries a code, a figure, a reference or a timestamp and never a floor, a limit, a threshold or a clock.

### 12. Contract

#### 12.1 REST operations provided

None. This contract declares no REST operation, no path, no method and no media type. The treatment resource and its read are RWB-S2-E3001-CON's (`POST /cases/{caseId}/treatments`, `GET /treatments/{treatmentId}`), and the draft-terms change `PATCH /treatments/{treatmentId}` is RWB-S2-E3002-CON's, which supersedes the `/submit` form of API Specification v5 and TSD S2 T-A.1 API-S2-004 under the source precedence of Template and Rules §R3. The officer's action on SCR-14 that records the buy-back agreement is an update of the treatment through that surface, and this contract fixes only what the rental treatment then carries.

| Element | Domain | Absence rule |
|---|---|---|
| `rentAmount` | numeric(18,2), baht; carried as `offer_amount` (DF-TRT-007) in the representation | Absent until R-DIL-32 sets the rent |
| `firstRentDue` | date; carried as `first_due_date` (DF-TRT-029) | Absent until R-DIL-32 sets the first due date |
| `installmentsPaid` | integer; carried as `installments_paid` (DF-TRT-032) | Present from the insert at zero and grown by each matched receipt |
| `rentalRef` | The reference its owner returns for the rental record | Absent until the rental record has been accepted |
| `autoDebitRef` | The ATS mandate reference | Absent until the mandate has been accepted |
| `autoDebitStatus` | The mandate state as its owner reports it | Absent until the mandate has answered |

#### 12.2 REST operations consumed

None. The contract consumes no operation: the case status, the customer and asset facts and the matched receipt arrive on the case signal, the AMIS rental record, the ATS mandate and the disposal hand-off are reached through Temporal on their owners' queues, and the rule version arrives as an event. RWB-S2-E3016-APP consumes no service by REST either.

#### 12.3 Events published

None of its own. The service publishes one event type and this contract refers to it rather than restating it.

| Event | Topic | Position on this path | Purpose |
|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | Not published: the rental path announces nothing, and EV-10 stays with the offer release of the deed in lieu on RWB-S2-E3012-APP | EV-10 tells rwb-comms to issue the offer documents and rwb-payment to expect the settlement of the debt |

The event name follows Template and Rules §R4 and the topic is the service's own; the envelope is the one RWB-S2-E3003-CON fixes and this contract adds no field to it. No source names an event for the rental: the outcome reaches the case on the case signal, rwb-case's own case events carry the rental start to rwb-payment, and the absence is Not specified in the source documents (GAP-2680; ASM-4417). A refusal, a stale product or a disposal hand-off publishes nothing: the state or the reason code is carried on the treatment and in the decision record.

#### 12.4 Events consumed

None. The contract consumes no event; `rwb.decision.RulePackageInForce.v1` (EV-30) and `rwb.payment.PaymentMissed.v1` (EV-12) are consumed by RWB-S2-E3016-APP, and this document refers to the rule version of an answer only.

#### 12.5 Workflows and activities

None. The contract defines no workflow and no activity. The stage that writes the rental row and the record is RWB-S2-E3016-APP's, the AMIS, ATS and disposal requests run on their owners' queues, and the receipts arrive as facts and events; a workflow class never writes the element set or an event.

#### 12.6 Schedules

None. The stage is signal-started and owns no Temporal Schedule and no legacy Quartz job; the rental due clock and the arrears window are workflow timers of the stage, and this contract declares none.

#### 12.7 Tables owned

| Table | Schema | Owner | Note |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Carries the rental row of type RENTAL with `offer_amount` (DF-TRT-007), `first_due_date` (DF-TRT-029), `installments_paid` (DF-TRT-032) and the three rental elements; no column of a limit, a threshold or a clock is added |
| `decision_record` | `rwb_treatment` | PLT (library object, DP-03) | The record of each step, written through RWB-PLT-E1027-CON in the same transaction; its shape is that contract's and is not restated here |
| `outbox` | `rwb_treatment` | S2, from the service template | The decision-record row of each step, written in the same transaction; no business event row on this path |
| (none) | — | — | No rental table and no tenancy table is created, and no foreign key crosses a schema |
| `asset` | `rwb_asset` | S5 | Named only: the AMIS rental record is requested and its reference returns as a fact |
| `proceeds` | `rwb_payment` | P8 | Named only: the matched receipt and the posting are the payment service's |
| `v_ace_npa_asset`, `v_ace_customer` | ACE views, `rwb_source_data`'s read | P1 | Named only: the facts reach the stage on the case signal and are never read here |

The no-new-table rule is the contract's, not a coding preference: a second table would let the same tenancy be recorded twice, once as a row and once as a record, which DP-01, DP-03 and Principle 5 forbid. The three published fields already carry the figure, the date and the count; the three new columns are added on the service's own migration sequence by RWB-S2-E3016-APP, and this contract fixes their names and domains only (GAP-2681; ASM-4419).

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Element fake | The six rental elements | A rental at each state of section 9; one with no mandate answer; one with a refused mandate; one with no rental reference; a disposal hand-off |
| Consumer fake of rwb-payment | The rent and the due date it matches against | A rental body with the rent, the first due date and the instalment count; a body with no instalment count, refused |
| Consumer fake of rwb-asset | The rental reference and the asset | A rental body with a reference and an asset fact; a body with no asset fact, refused |
| Decision-record fake | The record write of DP-03 | An accepted record with chain sequence and entry hash; a refusal with MSG-P7-009 and the field; an unavailable writer with MSG-P7-003 |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consuming service rather than as a surprise at run time.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0: the contract declares no operation | 0 | The treatment resource is RWB-S2-E3001-CON's and the update surface RWB-S2-E3002-CON's |
| Kafka | 0 new: no event type on this path | 0 | The one event type of the service stays with the offer release of the deed in lieu |
| Temporal | 0 | 0 | No workflow and no activity; the stage and the requests are the APP story's |
| File | 0 | 0 | No file crosses the contract |

### 13. Solution plan

**Package.** Contract artefact of rwb-treatment: the rental element set and the event position in the service's contract document, with the published types in `th.co.scb.ace.workbench.recovery.treatment.api` for the rental element. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`. The implementation is RWB-S2-E3016-APP.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; this contract declares the record's use and not its shape | referred to; the consuming story carries the dependency |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE data read through rwb-source-data's contract; on this path the facts arrive on the case signal and no view is named | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the contract adds no path | referred to; the consuming story carries the dependency |
| DP-19 | Screen, ace-web | gateway-bff composite route; SCR-14 and SCR-16 read the element set through the route | referred to; the consuming story carries the dependency |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `RentalElement` | Document section | The six element names, their domains and their absent-until rule (BR1, BR2) |
| `NoNewTableRule` | Document section | The rental is a treatment row; `decision_record`, `asset`, `proceeds` and the ACE views are named and not created (BR1, BR7) |
| `EventPosition` | Document section | No event type on the rental path, the one envelope referred to and not reused, and the case-signal route to rwb-payment (BR3, BR8) |
| `RefusalAndHoldRule` | Document section | No event on a refusal, a stale product or a disposal hand-off, and the two decision-record exceptions (BR5, BR6) |
| `VersioningSpecification` | Document section | Major version 1, the compatible versus breaking rule and the pinning rule (BR9) |
| Fake set and fixtures | Test asset | The element and two consumer fakes used by this story and the APP story (AC6) |

**Build steps**

1. Write the element section against the treatment representation and the TSD list, and lint the names and domains (AC1).
2. Write the no-new-table rule and name `decision_record`, `asset`, `proceeds` and the ACE views with their owners (AC1).
3. Write the event position and assert that no event type, no payload field and no reuse of EV-10 is added on the rental path (AC2).
4. Write the refusal and hold rules with the mandate state, the stale-product message and the disposal hand-off (AC4).
5. Write the versioning section with the compatible and the breaking example (AC5).
6. Generate the fake set and the drift test for this story and RWB-S2-E3016-APP (AC6).
7. Scan every example for personal data and publish v1 with the pinned versions of the two consumers recorded (AC3, AC5).

**Feature flag.** `rwb.treatment.buyback-rental`.

**Done when.** The document validates, the element fake answers every state and the three absences, the consumer fakes of rwb-payment and rwb-asset accept their bodies and refuse a body with no key value, a proposed rental table and a proposed rental event both fail the build, the drift test is green on this story and on the build of RWB-S2-E3016-APP, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P7-003 | The decision record cannot be written and the step is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. | `DecisionLogUnavailableException` of RWB-PLT-E1027-CON |
| MSG-P7-009 | The record is refused for a missing or invalid field (service log and incident, not shown to customers) | The decision record was refused: {field} is missing or not valid. | `DecisionLogRecordInvalidException` with `field` |
| MSG-S2-003 | The rental arrangement to the customer carries its end date | The offer to the customer ends on {date}. | The caller's screen |
| MSG-S2-001 | A figure on the rental is below the floor and has been routed for approval | The offer is below the floor of {floor}. It has been sent for approval. | The caller's screen; the contract fixes the element, not the display |
| MSG-S2-002 | The figure behind the rental is stale when the row is opened | The payoff is from {date}. A new figure has been requested. | The caller's screen |
| MSG-P1-001 | The data product behind the rental is from an earlier date | {product} is from {date}. Today's load has not arrived. | The caller's screen; VR-S2-016-1 |
| MSG-GEN-001 | A required field of the rental is missing | Enter {field}. | The caller's screen |
| MSG-P4-002 | A role without the right acts on the rental | You cannot {action} here. Your role does not include it. | The guard's answer, unchanged |

The texts are copied unchanged from RWB-E3-016, the FSD validation rule of FEAT-TRT-16 and the decision-record contract; this story adds no message ID. MSG-P7-003 and MSG-P7-009 are the two exceptions that keep a step from taking effect without its record. Thai text follows decision DL10, which is still open; its assumptions are ASM-2250, ASM-2357, ASM-2377 and ASM-2863.

### 15. Screens and states

No screen is declared by this contract, and it fixes no field of one. SCR-14 Treatment record (states Draft; submitted; approved; booked; broken; empty, loading, error and no access: Not specified in the source documents (CG-ALL-8773)) shows the rental treatment with its rent, its first due date, its mandate status and its instalment count, and SCR-16 Deed in lieu (states Checks; appraisal; approved; transferred; empty, loading, error and no access: Not specified in the source documents (CG-ALL-8774)) shows the deed-in-lieu facts that led to it; both read the element set through the gateway-bff composite route (DP-19). The screen field list and the composite route specification belong to the platform edge story and the screen owners. The contract fixes only the names, domains and absent-until rule of the six elements, so a screen can show "mandated, awaiting the first receipt" or "rental handed to disposal" without inventing a field.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S2-E3016-CON-01 | AC1; BR1, BR2, BR7 | Contract | The element section linted against the treatment representation and the TSD list; the six elements with their domains and their absent-until rule; the no-new-table statement; a proposed rental table refused |
| TC-S2-E3016-CON-02 | AC2; BR3, BR8 | Contract | The event position asserted against the catalogue: one event type, no rental event, no reuse of the EV-10 envelope; a proposed rental event refused |
| TC-S2-E3016-CON-03 | AC3; BR4 | Contract | The rental and mandate references carried once; the mandate state as its owner reports it; the personal-data scan refusing a name, an account number and a tenancy document |
| TC-S2-E3016-CON-04 | AC4; BR5, BR6 | Contract | A refused mandate, a stale data product and an arrears hand-off; no event and no outbox row; a forced record failure with MSG-P7-003 and a refused field with MSG-P7-009 |
| TC-S2-E3016-CON-05 | AC5, AC6; BR9 | Component | A compatible change and a breaking change against the registry; the element and two consumer fakes; the drift test on this story and on RWB-S2-E3016-APP |
| TC-S2-E3016-CON-06 | AC1; BR1, BR7 | Contract | Each table of section 12.7 checked against the schema: `treatment` as the only carrier of the rental, `decision_record`, `outbox`, and no rental or tenancy table; the three published fields carry the figure, date and count; a limit, threshold or clock column refused |
| TC-S2-E3016-CON-07 | AC7; BR1 to BR9 | Contract | Not specified in the source documents (NEWAC-RWB-S2-E3016-CON-AC7) |
| TC-S2-E3016-CON-08 | AC8 | Contract | Not specified in the source documents (NEWAC-RWB-S2-E3016-CON-AC8) |

The legacy test set of RWB-E3-016, TC-E3-016-01 to TC-E3-016-05, is carried by RWB-S2-E3016-APP and by the wave 2 integration harness; these five are the contract's own tests and no legacy id is renumbered.

### 17. Guardrails

- No business value in the contract: the rent, the arrears limit, the clocks and the state names are values in force of their owners; the only values this document fixes are the element names, their domains and the synthetic examples.
- No personal data in a schema, an example, a fake or a log: the rental and mandate references are system references, the subject is a case identifier, and the scan fails the build otherwise.
- No rental table and no second write path for the rent: the treatment row and the decision record are the only places it lives, and the boundary test fails the build on a third (BR1).
- No cross-schema reference and no foreign key across services: `asset`, `proceeds` and the ACE views are named, never joined and never read (BR7).
- No REST surface of this contract's own and no new event: the treatment resource and the update surface belong to sibling CON stories, and the one event type is RWB-S2-E3003-CON's (BR3).
- No event on a refusal, a stale product or a disposal hand-off, and no field added to the payload (BR5).
- A published version is never edited in place: a breaking change raises major version 2 with a new `ce_type` and a migration note (BR9).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-010 | Buyback rental, auto-debit, receipts and arrears follow-up run without a person for a standard arrangement | Business Requirements Program, section 5.9 | FEAT-TRT-16 | 07 Route, settle and claim | R-DIL-32; R-DIL-34 | TC-S2-E3016-CON-01, TC-S2-E3016-CON-04 |
| REQ-S2-008 | Booked terms, settled accounts and released collateral are posted to their systems of record without re-keying | Business Requirements Program, section 5.9 | FEAT-TRT-16 | 07 Route, settle and claim | R-DIL-32 | TC-S2-E3016-CON-03 |
| Legacy test set RWB-E3-016 | TC-E3-016-01, TC-E3-016-02, TC-E3-016-03, TC-E3-016-04, TC-E3-016-05 | Program, section 5.9 | The legacy story's own feature | 07 Route, settle and claim | R-DIL-32 | Executed by RWB-S2-E3016-APP and the wave 2 integration harness; not owned here |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3016-APP | App development | H consumer: implements the rental stage, the element set and the record against this contract and its fakes |
| RWB-S2-E3001-CON | Contract | Referred to: the treatment contract baseline that carries the treatment representation |
| RWB-S2-E3002-CON | Contract | Referred to: the update surface, which is not declared here |
| RWB-S2-E3003-CON | Contract | Referred to: the `TreatmentApproved` envelope this contract names and does not reuse on this path |
| RWB-PLT-E1027-CON | Contract | Referred to: the local decision-record library whose shape and exceptions are named and not restated |
| RWB-PLT-N001-CON | Contract | Referred to: the gateway-bff composite route by which the screens read the element set |
| P8 rwb-payment, S5 rwb-asset | Consumer and owner | Read the rent, the due date, the instalment count and the rental reference; pin the version |
| P1 rwb-source-data, P2 rwb-integration | Owner | The ACE facts and the AMIS and ATS interfaces, named and not read here |
| The wave 2 integration harness | Integration | The cross-service proof of the rental against the live owners |

### 19. Out of scope

- The implementation — the rental stage of `TreatmentWorkflow`, its six activities, the rental row, the three columns and the requests to the owners: RWB-S2-E3016-APP.
- The treatment resource, its creation and its field list DF-TRT-001 to DF-TRT-033: RWB-S2-E3001-CON and RWB-S2-E3001-APP.
- The update surface `PATCH /treatments/{treatmentId}` and the settlement offer: RWB-S2-E3002-CON and RWB-S2-E3002-APP.
- The deed in lieu from the offer to the asset on books and the field inspection: RWB-S2-E3012-CON and RWB-S2-E3012-APP.
- The `TreatmentApproved` payload shape, its registry entry and its two consumers: RWB-S2-E3003-CON, RWB-PLT-EVT and the event platform.
- The asset record, the asset list, the AMIS interface, the ATS mandate interface and the disposal route: rwb-asset and rwb-integration and their own stories.
- The payment matching, the posting, the receipt, the proceeds and the arrears event: rwb-payment and its own contract.
- The case status, the case table, the case task and the case signal: rwb-case.
- The rule packages, the version promotion and the approval record: rwb-decision.
- The topic, its ACLs, the retry topics and the dead-letter topic: the event platform and the platform infrastructure stories.
- The deployment, the flag and the dashboards of this build: this legacy key's DevOps story.
- The real cross-service proof of the rental against the live rwb-case, rwb-asset, rwb-integration and rwb-payment: the wave 2 integration harness.

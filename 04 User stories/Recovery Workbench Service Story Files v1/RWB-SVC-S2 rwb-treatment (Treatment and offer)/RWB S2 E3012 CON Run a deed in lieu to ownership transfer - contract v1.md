# RWB-S2-E3012-CON Run a deed in lieu to ownership transfer - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E3-012 for rwb-treatment. The contract is published on Day 1 and fixes the elements the treatment carries for a deed in lieu (`transferPrice`, `inspectionOutcome`, `unlockDecision`, `assetRef`, `transferredAt`), the reuse of the `rwb.treatment.TreatmentApproved.v1` envelope on `rwb.treatment.events.v1`, the rule that no table is created for the inspection or the transfer, the compatibility rule and the fakes; the implementation is RWB-S2-E3012-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3012-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-012 |
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

As a **contract owner of rwb-treatment**, I want **the published contract of the deed-in-lieu treatment — the elements the treatment carries from the offer to the transferred asset (`transferPrice`, `inspectionOutcome`, `unlockDecision`, `assetRef`, `transferredAt`), the reuse of the `rwb.treatment.TreatmentApproved.v1` envelope on `rwb.treatment.events.v1` with key `caseId`, the rule that no table is created for the inspection or the transfer, the compatibility rule and the fakes — instead of the monolith's `recovery_case` status column, its `decision_log_entry` row and its `document` row in the shared `recovery` schema**, so that **RWB-S2-E3012-APP can build and test the deed-in-lieu stage on Day 1, rwb-asset and rwb-case can pin the elements they read, and no team adds an inspection table or a transfer table to hold what the treatment already holds**.

### 2. Business rationale

The monolith kept the whole deed in lieu in one place: the S2 service set `recovery_case.status` itself, wrote `decision_log_entry` with the rule version, wrote the `document` rows, read `v_ace_customer` and `v_ace_npa_asset` directly, and asked AMIS, ALS and the registration system in the same process. Three consequences followed that the target cannot keep. The status moved in the case table, so no stage could announce an outcome. The facts had no shape of their own, so the offer, the inspection and the transfer were distinguished by free text and screens. And a team adding the field inspection would have added a table, and a team adding the transfer would have added another, so the same asset would be recorded three times.

In the 19-service target the case status is rwb-case's (ASM-4388), the record is the platform library's and local to the service (DP-03), the customer and NPA-asset facts are rwb-source-data's and arrive as facts (DP-05), the asset record is rwb-asset's, the documents are rwb-document's, and the AMIS and core-bank work is rwb-integration's (ASM-4390; ASM-4391). What is left for this contract is the part two other services and the screens depend on: what a deed-in-lieu treatment carries, and how the one event of the service is used on this path. The TSD lists DF-TRT-001 to DF-TRT-033 with no transfer price, no inspection outcome, no asset reference and no unlock answer (TSD S2 T3.1), so the element names and their domains are Not specified in the source documents (GAP-2673; ASM-4393).

**The division of the legacy key is fixed.** This WP delivers the **contract**. The **implementation** — the deed-in-lieu stage of `TreatmentWorkflow`, its seven activities and its calls to the owners — is **RWB-S2-E3012-APP**, and the **cross-service proof** is the wave 2 integration harness. The four legacy acceptance criteria **stay with RWB-S2-E3012-APP** and are not copied here: every criterion in section 7 is new (D-RCV-60) and tests only the contract deliverable in this title.

The contract has to exist before the code for three reasons. rwb-asset and rwb-case build in the same wave and need the element names on Day 1. The element set is what stops a second and a third table: a team that finds no field for the inspection adds `inspection` and the same asset is then recorded twice, once as a row and once as a record. And the compatibility rule lets the screens and the consumers pin a version while the stage is still being built. The fake is the Day-1 unblocker: the stage is built and tested before rwb-asset, rwb-document or rwb-integration exists.

### 3. Preconditions

- The treatment of the case is rwb-treatment's own object in schema `rwb_treatment` (Ownership Map row `treatment`, owner S2), with DF-TRT-001 to DF-TRT-033 and `treatment_type` taking the value DEED_IN_LIEU of LOV-TREATMENT (TSD S2 T3.1 and T3.2).
- The approved-offer elements reuse the published names where they exist: `offerAmount` (DF-TRT-007) carries the transfer price the rules call `transfer_price`, and `validUntil` is the `valid_until` of DF-TRT-010; `inspectionOutcome`, `unlockDecision`, `assetRef` and `transferredAt` have no published element on the treatment, which is the gap this contract closes for the wave (GAP-2673; ASM-4393).
- The service owns one event in the catalogue, `TreatmentApproved` (EV-10), producer rwb-treatment, topic `rwb.treatment.events.v1`, consumers rwb-comms and rwb-payment; its envelope is fixed by RWB-S2-E3003-CON and this contract refers to it and never redefines it.
- No source names an event for the transfer completion: the stage reports the outcome to the parent `CaseWorkflow`, and that absence is the gap recorded here (GAP-2673).
- The rules that give each step its answer are in force as data: R-DIL-16, R-DIL-18, R-DIL-22, R-DIL-23 to R-DIL-26, R-DIL-28 and R-DIL-29, with the reason codes `offer_expired`, `unlock_refused` and `title_not_clean` (Business Rules and Routing Logic v4). The codes are reference values, never a list held by this contract (BR-S2-012).
- The asset record, the documents and the ACE facts are not this contract's: `asset` is S5's, `document` is P5's, and the customer and NPA-asset views are rwb-source-data's read (DP-01; DP-05; ASM-4389; ASM-4390).
- The decision record is written through RWB-PLT-E1027-CON, whose write refuses with MSG-P7-009 and fails with MSG-P7-003; this contract declares the record's use and not its shape (DP-03).
- The schema registry is in BACKWARD mode and the AsyncAPI document per service is the contract, so the event is registered against it.
- No build dependency and no approval stop: a CON story is Day 1 by rule and is published at status Draft (realignment v1).

### 4. Flow

1. The contract author fixes the element set of a deed-in-lieu treatment: the two elements that already exist (`offerAmount` carrying the transfer price, `validUntil`) and the five named here, with their value domains and their absent-until rule.
2. The author fixes the no-new-table rule and states where each fact already lives: the treatment row, the library's `decision_record`, S5's `asset`, P5's `document` and the ACE views of rwb-source-data.
3. The author writes the event section: this contract publishes no event type of its own, refers to the envelope of RWB-S2-E3003-CON, and states at which step the service publishes it on this path (R-DIL-16) and that the transfer completion of R-DIL-28 publishes nothing.
4. The author writes the compatibility rule: which change keeps major version 1, which raises major version 2 with a new `ce_type`, and how a consumer pins a version.
5. The author writes the refusal and hold rules: a refusal or a title hold carries its reason code on the treatment and publishes nothing, and the two decision-record exceptions keep a step from taking effect.
6. The author writes the fake set: an element fake for the five states of the deed in lieu, an envelope-reuse fake, a consumer fake for rwb-asset and rwb-case, and the decision-record fake reference.
7. The lint step runs: the element names compared with the API Specification and the TSD list, the payload compared with the AsyncAPI document of the service, and the examples scanned for personal data.
8. The contract test runs the fakes against the document on every change and fails the build on any drift in this story and in RWB-S2-E3012-APP.
9. The document and the fakes are published at v1; RWB-S2-E3012-APP, rwb-asset and rwb-case pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A team adds an `inspection` or a `transfer` table, or a second write path for the asset reference | The boundary and drift checks fail the build; the treatment row plus the decision record are the only places a deed-in-lieu fact lives | None | AC1 |
| X2 | A team redefines the `TreatmentApproved` payload or adds a field for the deed in lieu | The drift test against RWB-S2-E3003-CON fails the build; this contract refers to the envelope and adds no field | None | AC2 |
| X3 | A payload or an example carries a personal field, document content or free text | The personal-data scan fails the build; the event carries identifiers, figures and versions only | None | AC3 |
| X4 | A refusal or a title hold publishes an event, or the transfer completion is announced on an event the catalogue does not name | The contract test fails: a refusal publishes nothing and the transfer reaches the case on the case signal | None | AC4 |
| X5 | A step updates the treatment while the record cannot be written | The `MANDATORY` rule and the drift test fail the build; the caller's transaction rolls back | MSG-P7-003 | AC4 |
| X6 | An element is renamed, removed or retyped | The change raises major version 2 and a new `ce_type`; v1 is never edited in place and stays readable | None | AC5 |
| X7 | A value the consumers need is named by no source — the element names, their domains, or the transfer event | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-2673; ASM-4393) | AC1, AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document and fakes; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | The value domains, the example values and the fixture set are open until v1 is frozen; the five element names, the event reference and the no-new-table rule are fixed |
| Valuable | Unblocks RWB-S2-E3012-APP, rwb-asset and rwb-case on Day 1 and keeps two tables out of the service plan |
| Estimable | One element set, one event reference, one rule set, one fake set and one document |
| Small | One sprint for the document, the fakes and the lint rules |
| Testable | Each criterion below is one document, schema or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: the deed-in-lieu contract of rwb-treatment

  Background:
    Given the rwb-treatment contract document is published with major version 1
    Given the treatment of a case is owned by rwb-treatment in schema rwb_treatment
    Given the case status stays rwb-case's and reaches the stage on the case signal

  Scenario: AC1 The deed-in-lieu treatment carries five elements and creates no new table (new, D-RCV-60)
    Given the element section of the contract document
    When it is validated against the treatment representation and the TSD
    Then a deed-in-lieu treatment carries transferPrice, inspectionOutcome, unlockDecision, assetRef and transferredAt on the treatment row
    Then transferPrice is numeric(18,2) in baht and is absent until R-DIL-13 sets it, and it is carried as offerAmount (DF-TRT-007) in the treatment representation
    Then each of the five elements is absent until its step has answered, and present with the rule's answer after it
    Then the document declares that no table is created for the inspection and none for the transfer, and names decision_record as the library object of DP-03, asset as S5's, document as P5's and v_ace_npa_asset as P1's read
    Then a proposed inspection table or transfer table fails the boundary test

  Scenario: AC2 The offer release uses the one service event and adds no field (new, D-RCV-60)
    Given the event section of the document
    When a deed-in-lieu offer release is validated against the envelope of RWB-S2-E3003-CON
    Then the event is rwb.treatment.TreatmentApproved.v1 on rwb.treatment.events.v1 in CloudEvents 1.0 binary mode with ce_type, ce_source rwb-treatment and ce_subject the case ID
    Then the record key is caseId and treatmentType carries DEED_IN_LIEU
    Then offerAmount carries the transfer price and approvalLevel and approverRole are absent when the price was inside the floor
    Then this contract adds no event type and no payload field, and declares that the transfer completion of R-DIL-28 publishes nothing

  Scenario: AC3 The transfer facts are carried once and re-keyed by no one (new, D-RCV-60)
    Given the transfer section of the document
    When a completed transfer is validated against it
    Then assetRef carries the reference of the asset recorded by rwb-asset and transferredAt the time of the transfer
    Then the treatment carries no asset description, no registration document and no measurement, and the document states that rwb-asset and rwb-document hold them
    Then the payload carries no name, no national identifier, no account number, no address, no document content and no free text
    Then the personal-data scan fails the build on any of them

  Scenario: AC4 A refusal or a hold is carried on the treatment and publishes nothing, and a failure to record stops the step (new, D-RCV-60)
    Given the refusal and hold section of the document
    When a refused unlock, an expired offer and a title hold are put through it
    Then the treatment carries the final call and the reason code in force, unlock_refused, offer_expired and title_not_clean of their owners
    Then no TreatmentApproved event is published and no outbox row is written on any of the three
    Then the decision record is written through DecisionRecordWriter with propagation MANDATORY, and a failed write answers MSG-P7-003 and rolls the treatment back
    Then a refused field answers MSG-P7-009 with the field name and no event

  Scenario: AC5 A compatible change keeps major version 1 and a breaking change raises version 2 (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published element
    Then an added optional element keeps major version 1 and the ce_type version, and is accepted by the registry in BACKWARD mode
    Then a renamed, removed or retyped element raises major version 2 and a new ce_type, and v1 is never edited in place
    Then RWB-S2-E3012-APP, rwb-asset and rwb-case each pin a published version and raise a change request rather than a private variant

  Scenario: AC6 The fakes answer the document and the drift test runs on both sides (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the element fake, the envelope-reuse fake and the two consumer fakes
    Then the element fake answers a treatment at each deed-in-lieu state, one with no inspection, one with no unlock answer and one with no asset reference
    Then the envelope fake answers the deed-in-lieu body against the envelope of RWB-S2-E3003-CON and refuses a body with a field outside it
    Then the consumer fakes of rwb-asset and rwb-case accept the transferred body and refuse a body with no key
    Then the drift test fails on any difference from sections 12 and 13 in this story and in RWB-S2-E3012-APP
```

These criteria are new and test only the contract deliverable: no legacy acceptance criterion is repeated here — **AC1 to AC4 of RWB-E3-012 stay with RWB-S2-E3012-APP** — and every identifier comes from the legacy story, the TSD, Architecture v5, the BRD or the Business Rules and Routing Logic, character for character. The element names, their domains and the absence of a transfer event are Not specified in the source documents (GAP-2673; ASM-4393).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A deed-in-lieu treatment carries `transferPrice`, `inspectionOutcome`, `unlockDecision`, `assetRef` and `transferredAt`, and no table is created for the inspection or the transfer | GAP-2673; ASM-4393 |
| BR2 | The transfer price is carried as `offerAmount` (DF-TRT-007) in the treatment representation and is a figure in force, never a constant; the offer end is `valid_until` (DF-TRT-010) | TSD S2 T3.1; BR-S2-012 |
| BR3 | The service publishes one event type, `TreatmentApproved` (EV-10), on its own topic, in CloudEvents 1.0 binary mode with key `caseId`, and this path publishes it once, at R-DIL-16 | Architecture v5 slide 42 row 10; RWB-S2-E3003-CON; Template and Rules §R4 |
| BR4 | The payload carries identifiers, figures and versions only, and this contract adds no field to it | NFR-054; RWB-S2-E3003-CON |
| BR5 | A refusal, an expiry or a title hold publishes nothing and is carried on the treatment with the reason code in force: `unlock_refused`, `offer_expired`, `title_not_clean` | R-DIL-21; R-DIL-26; R-DIL-29; BR-S2-012 |
| BR6 | Every step is recorded through DecisionRecordWriter with propagation MANDATORY, refusing with MSG-P7-009 and failing with MSG-P7-003, so a step that cannot be recorded does not take effect | DP-03; R-UNI-39; RWB-PLT-E1027-CON |
| BR7 | The asset record is S5's, the documents are P5's and the ACE facts are P1's: this contract names them and declares no field, no read and no write of any | DP-01; DP-05; Ownership Map rows `asset`, `document`, `v_ace_npa_asset` |
| BR8 | The case status is rwb-case's: this contract declares no status value and no case event, and no event announces the transfer completion | ASM-4388; GAP-2673 |
| BR9 | A published version is never edited: a backward-compatible change keeps major version 1, a breaking change raises major version 2 with a new `ce_type`, and every consumer pins a version | Template and Rules §R7.2; Architecture v5 slides 42 and 43 notes |

### 9. State transitions

None in this story: a contract document has no runtime state. Two vocabularies are fixed here and the runtime behind them is specified in RWB-S2-E3012-APP section 9.

| Object | State | Meaning in the contract |
|---|---|---|
| Deed-in-lieu element set | Price set | `transferPrice` is present and no inspection has been recorded |
| Deed-in-lieu element set | Offered | `validUntil` is present, the offer has gone to the customer and the offer timer runs |
| Deed-in-lieu element set | Inspected | `inspectionOutcome` carries the checklist result; the unlock has not answered |
| Deed-in-lieu element set | Unlocked | `unlockDecision` carries the rule's answer or the approver's release |
| Deed-in-lieu element set | Transferred | `assetRef` and `transferredAt` are present and the asset is on books |
| TreatmentApproved | Published | The caller's outbox relay published the event after the transaction of R-DIL-16 committed |
| TreatmentApproved | Absent | A refusal, an expiry, a hold or a rolled-back transaction; no event exists |
| Contract version | v1 | The published version RWB-S2-E3012-APP, rwb-asset and rwb-case pin |
| Contract version | v2 | Raised by a breaking change, with a new `ce_type`; v1 stays readable and is never edited |

The case statuses of the route — TRANSFER_PRICE_SET, OFFER_WITH_CUSTOMER_DIL, WITH_FIELD_INSPECTION, ASSET_UNLOCK_DECISION, AWAITING_TRANSFER, ASSET_ON_BOOKS — are rwb-case's. This contract refers to the point at which each element is written and holds no status list of its own.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the element section, the event reference and the fakes |
| The owner of rwb-treatment | Approves a breaking change to the element set and freezes a version |
| The rwb-asset owner (S5) | Confirms the asset reference it returns and the fields it keeps; this contract declares none of them |
| The rwb-case owner (P3) | Confirms that no case status and no case event is declared here, and that no transfer event exists |
| The rwb-document owner (P5) | Confirms that the inspection captures and the document set are its own |
| The rwb-source-data owner (P1) | Confirms that the customer and NPA-asset facts reach the stage as facts and that no view is read here |
| The rwb-decision owner (P7) | Confirms the rule packages and their versions, and the approval side of the unlock exception |
| RW-AUDIT, RW-COE | Audit the decisions through the P7 ledger and the local record, not through this contract |
| No delegation of authority level applies | A service contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in the document, an example or a fake. Where a caller or an approver must be named, the example uses a role code or a user identifier only.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The document publishes element names, domains, codes and message identifiers; no customer, account or case value appears outside a synthetic example |
| Element set published | `transferPrice` (numeric(18,2)), `inspectionOutcome`, `unlockDecision`, `assetRef`, `transferredAt`, with the absent-until rule of section 12.1, beside `offerAmount` and `validUntil` of the treatment |
| Personal data | None. The asset reference is a system reference, never a name, an address or a document; no account number and no national identifier appears |
| Tables published | None created: the treatment row of S2, the library object `decision_record` of DP-03, S5's `asset`, P5's `document` and P1's read of `v_ace_npa_asset` are named, and the document declares that no table is added for the inspection or the transfer |
| Field identifiers | `offerAmount` carries DF-TRT-007 and `validUntil` DF-TRT-010; the five new elements carry no field ID in the TSD, which stops at DF-TRT-033 (GAP-2673; ASM-4393) |
| Retention | The treatment row and the local record follow their owners' retention; the event is retained on the topic under the platform policy |

The element set is the one place where a business value could leak into the contract, so the document fixes that an element carries a code, a figure, a reference or a timestamp and never a floor, a limit, a threshold or a clock.

### 12. Contract

#### 12.1 REST operations provided

None. This contract declares no REST operation, no path, no method and no media type. The treatment resource and its read are RWB-S2-E3001-CON's, and the draft-terms change `PATCH /treatments/{treatmentId}` and the offer `POST /treatments/{treatmentId}/offer` are RWB-S2-E3002-CON's, the offer superseding the `/submit` form of API Specification v4 and TSD S2 T-A.1 API-S2-004 under the source precedence of Template and Rules §R3. The officer's action on SCR-16 that records an inspection outcome or asks for the transfer is an update of the treatment through that surface, and this contract fixes only what the treatment then carries.

| Element | Domain | Absence rule |
|---|---|---|
| `transferPrice` | numeric(18,2), baht; carried as `offerAmount` (DF-TRT-007) in the representation | Absent until R-DIL-13 sets the price |
| `inspectionOutcome` | The checklist result of R-DIL-22, complete or incomplete with the missing item named | Absent until the inspection has been recorded |
| `unlockDecision` | The rule's answer of R-DIL-23 or the approver's answer of R-DIL-25 or R-DIL-26 | Absent until the unlock has answered |
| `assetRef` | The reference rwb-asset returns for the asset recorded at the transfer | Absent until the transfer has completed |
| `transferredAt` | timestamptz of the completed transfer | Absent until the transfer has completed |

#### 12.2 REST operations consumed

None. The contract consumes no operation: the case status and the customer and NPA-asset facts arrive on the case signal, the document set, the asset record, the AMIS record and the debt settlement are reached through Temporal on their owners' queues, and the rule version arrives as an event. RWB-S2-E3012-APP consumes no service by REST either.

#### 12.3 Events published

None of its own. The service publishes one event type and this contract refers to it rather than restating it.

| Event | Topic | Key | This contract | Purpose |
|---|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | `caseId` | Refers to the envelope and the ten payload fields fixed by RWB-S2-E3003-CON; on this path `treatmentType` is DEED_IN_LIEU, `offerAmount` carries the transfer price, and `approvalLevel` and `approverRole` are present only where the price went below the floor | EV-10: tells rwb-comms to issue the offer documents and rwb-payment to expect the settlement of the debt (Architecture v5 slide 42 row 10) |

| Envelope element | Value |
|---|---|
| Mode | CloudEvents 1.0, binary mode |
| ce_specversion | 1.0 |
| ce_type | rwb.treatment.TreatmentApproved.v1 |
| ce_source | rwb-treatment |
| ce_subject | The case ID of the approved treatment |
| ce_id and traceparent | The event identifier and the W3C trace context of the transaction that wrote it |
| Payload | Identifiers, figures and versions only; no personal data and no free text |

The event name follows Template and Rules §R4 and the topic is the service's own. The transfer completion of R-DIL-28 publishes nothing: no source names an event for it, the outcome reaches the case on the case signal, and the absence is Not specified in the source documents (GAP-2673; ASM-4393). A refusal, an expiry or a title hold publishes nothing: the reason code is carried on the treatment row and in the decision record.

#### 12.4 Events consumed

None. The contract consumes no event; `rwb.decision.RulePackageInForce.v1` (EV-30) is consumed by RWB-S2-E3012-APP and names a version this document refers to only as the rule version of an answer.

#### 12.5 Workflows and activities

None. The contract defines no workflow and no activity. The stage that writes the treatment and the outbox row is RWB-S2-E3012-APP's, the approval child is the workflow kit's on rwb-decision's queue, and the document, asset and integration requests run on their owners' queues; a workflow class never writes the element set or the event.

#### 12.6 Schedules

None. The stage is signal-started and owns no Temporal Schedule and no legacy Quartz job; the offer validity and the title hold are workflow timers of the stage, and this contract declares none.

#### 12.7 Tables owned

| Table | Schema | Owner | Note |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Carries the five deed-in-lieu columns beside `offerAmount` (DF-TRT-007) and `valid_until` (DF-TRT-010); no column of a floor, a threshold or a clock is added |
| `decision_record` | `rwb_treatment` | PLT (library object, DP-03) | The record of each step, written through RWB-PLT-E1027-CON in the same transaction; its shape is that contract's and is not restated here |
| `outbox` | `rwb_treatment` | S2, from the service template | The `TreatmentApproved` row of R-DIL-16, written in the same transaction |
| (none) | — | — | No table is created for the inspection and none for the transfer, and no foreign key crosses a schema |
| `asset` | `rwb_asset` | S5 | Named only: the asset record is requested and its reference returns as a fact |
| `document` | `rwb_document` | P5 | Named only: the document set and the field captures are its own |
| `v_ace_npa_asset`, `v_ace_customer` | ACE views, `rwb_source_data`'s read | P1 | Named only: the facts reach the stage on the case signal and are never read here |

The no-new-table rule is the contract's, not a coding preference: a second table would let the same asset be recorded twice, once as a row and once as a record, which DP-03, DP-05 and Principle 5 forbid. The two-column pair that already exists carries the figure and the date; the five new columns are added on the service's own migration sequence by RWB-S2-E3012-APP, and this contract fixes their names and domains only (GAP-2673; ASM-4393).

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Element fake | The five deed-in-lieu elements | A treatment at each state of section 9; a treatment with no inspection; one with no unlock answer; one with no asset reference; a title hold with `title_not_clean` |
| Envelope-reuse fake | The `TreatmentApproved` body on this path | A deed-in-lieu body with `treatmentType` DEED_IN_LIEU and the transfer price; a below-floor body with a level and an approver role; a body with a field outside the envelope, refused |
| Consumer fake of rwb-asset | The asset record | A transferred body with an asset reference and the fields S5 keeps; a refused body with no key |
| Consumer fake of rwb-case | The case and its task | A transferred body and the status it moves; a refused body with no key |
| Decision-record fake | The record write of DP-03 | An accepted record with chain sequence and entry hash; a refusal with MSG-P7-009 and the field; an unavailable writer with MSG-P7-003 |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consuming service rather than as a surprise at run time.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0: the contract declares no operation | 0 | The treatment resource is RWB-S2-E3001-CON's and the draft-terms change and the offer RWB-S2-E3002-CON's |
| Kafka | 0 new: one existing event type referred to | 0 | CloudEvents 1.0 binary mode, key `caseId` on `rwb.treatment.events.v1` |
| Temporal | 0 | 0 | No workflow and no activity; the stage and the requests are the APP story's |
| File | 0 | 0 | No file crosses the contract |

### 13. Solution plan

**Package.** Contract artefact of rwb-treatment: the element set and the event reference in the service's contract document, with the published types in `th.co.scb.ace.workbench.recovery.treatment.api` for the deed-in-lieu element. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`. The implementation is RWB-S2-E3012-APP.

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
| `DeedInLieuElement` | Document section | The five element names, their domains and their absent-until rule (BR1, BR2) |
| `EventReference` | Document section | The one event type, the key, the fields this path fills and the absence of a transfer event (BR3, BR4, BR8) |
| `RefusalAndHoldRule` | Document section | No event on a refusal, an expiry or a hold, the reason codes, and the two decision-record exceptions (BR5, BR6) |
| `VersioningSpecification` | Document section | Major version 1, the compatible versus breaking rule and the pinning rule (BR9) |
| Fake set and fixtures | Test asset | The element, envelope-reuse, consumer and decision-record fakes used by this story and the APP story (AC6) |

**Build steps**

1. Write the element section against the treatment representation and the TSD list, and lint the names and domains (AC1).
2. Write the no-new-table rule and name `decision_record`, `asset`, `document` and the ACE views with their owners (AC1).
3. Write the event reference and validate a deed-in-lieu body against the envelope of RWB-S2-E3003-CON; assert that no field and no event type is added (AC2, AC3).
4. Write the refusal and hold rules with the three reason codes and the two decision-record exceptions (AC4).
5. Write the versioning section with the compatible and the breaking example (AC5).
6. Generate the fake set and the drift test for this story and RWB-S2-E3012-APP (AC6).
7. Scan every example for personal data and publish v1 with the pinned versions of the three consumers recorded (AC3, AC5).

**Feature flag.** `rwb.treatment.deed-in-lieu`.

**Done when.** The document validates, a deed-in-lieu body passes the envelope fake of the service and a body with an extra field is refused, the element fake answers all five states and the three absences, the consumer fakes of rwb-asset and rwb-case accept the transferred body and refuse a body with no key, the drift test is green on this story and on the build of RWB-S2-E3012-APP, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P7-003 | The decision record cannot be written and the step is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. | `DecisionLogUnavailableException` of RWB-PLT-E1027-CON |
| MSG-P7-009 | The record is refused for a missing or invalid field (service log and incident, not shown to customers) | The decision record was refused: {field} is missing or not valid. | `DecisionLogRecordInvalidException` with `field` |
| MSG-S2-001 | The transfer price is below the floor and has been routed for approval | The offer is below the floor of {floor}. It has been sent for approval. | The caller's screen; the contract fixes the element, not the display |
| MSG-S2-002 | The figure behind the offer is stale when the documents are requested | The payoff is from {date}. A new figure has been requested. | The caller's screen |
| MSG-S2-003 | The offer to the customer carries its end date | The offer to the customer ends on {date}. | The `validUntil` element of the treatment |
| MSG-GEN-001 | A required field of the inspection or the transfer is missing | Enter {field}. | The caller's screen |
| MSG-P4-002 | A role without the right acts on the stage | You cannot {action} here. Your role does not include it. | The guard's answer, unchanged |

The texts are copied unchanged from RWB-E3-012 and from the decision-record contract; this story adds no message ID. MSG-P7-003 and MSG-P7-009 are the two exceptions that keep a step from taking effect without its record. Thai text follows decision DL10.

### 15. Screens and states

No screen is declared by this contract, and it fixes no field of one. SCR-16 Deed in lieu (states Checks, appraisal, approved, transferred) and SCR-14 Treatment record (states Draft, submitted, approved, booked, broken) read the element set through the gateway-bff composite route (DP-19), and the screen field list and the composite route specification belong to the platform edge story and the screen owners. The contract fixes only the names, domains and absent-until rule of the five elements, so a screen can show "inspected, awaiting unlock" or "transferred, asset {ref}" without inventing a field.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S2-E3012-CON-01 | AC1 | Contract | The element section linted against the treatment representation and the TSD list; the five elements with their domains and their absent-until rule; the no-new-table statement; a proposed inspection table and a proposed transfer table refused |
| TC-S2-E3012-CON-02 | AC2 | Contract | A deed-in-lieu body validated against the envelope of RWB-S2-E3003-CON; `treatmentType` DEED_IN_LIEU; the transfer price in `offerAmount`; a below-floor body with a level; a body with an extra field refused |
| TC-S2-E3012-CON-03 | AC3 | Contract | The key `caseId` with `ce_subject`; the asset reference and the transfer time carried once; the personal-data scan refusing a name, an account number and a free-text field |
| TC-S2-E3012-CON-04 | AC4 | Contract | A refused unlock with `unlock_refused`, an expired offer with `offer_expired` and a title hold with `title_not_clean`; no event and no outbox row; a forced record failure with MSG-P7-003 and a refused field with MSG-P7-009 |
| TC-S2-E3012-CON-05 | AC5, AC6 | Component | A compatible change and a breaking change against the registry; the element, envelope-reuse and two consumer fakes; the drift test on this story and on RWB-S2-E3012-APP |

The legacy test set of RWB-E3-012, TC-E3-012-01 to TC-E3-012-06, is carried by RWB-S2-E3012-APP and by the wave 2 integration harness; these five are the contract's own tests and no legacy id is renumbered.

### 17. Guardrails

- No business value in the contract: the product conditions, the unlock thresholds, the clocks and the reason-code list are values in force of their owners; the only values this document fixes are the element names, their domains and the synthetic examples.
- No personal data in a schema, an example, a fake or a log: the asset reference is a system reference, the subject is a case identifier, and the scan fails the build otherwise.
- No new table and no second write path for a deed-in-lieu fact: the treatment row and the decision record are the only places it lives, and the boundary test fails the build on a third.
- No cross-schema reference and no foreign key across services: `asset`, `document` and the ACE views are named, never joined and never read.
- No REST surface of this contract's own and no new event: the treatment resource and the offer belong to sibling CON stories, and the one event type is RWB-S2-E3003-CON's.
- No event on a refusal, an expiry or a hold, and no field added to the payload: rwb-comms and rwb-payment hear only of an approved treatment.
- A published version is never edited in place: a breaking change raises major version 2 with a new `ce_type` and a migration note.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-006 | The credit application, contract and mortgage documents for a deed in lieu are generated from templates | Business Requirements Program, section 5.9 | FEAT-TRT-12 | 07 Route, settle and claim | R-DIL-16 | TC-S2-E3012-CON-02 |
| REQ-S2-007 | An asset accepted under a deed in lieu is unlocked as a non performing asset by rule, with exceptions summarized for the approver | Business Requirements Program, section 5.9 | FEAT-TRT-12 | 07 Route, settle and claim | R-DIL-23; R-DIL-24; R-DIL-25 | TC-S2-E3012-CON-01 |
| REQ-S2-008 | Booked terms, settled accounts and released collateral are posted to their systems of record without re-keying | Business Requirements Program, section 5.9 | FEAT-TRT-12 | 07 Route, settle and claim | R-DIL-27; R-DIL-28 | TC-S2-E3012-CON-03 |
| Legacy test set RWB-E3-012 | TC-E3-012-01, TC-E3-012-02, TC-E3-012-03, TC-E3-012-04, TC-E3-012-05, TC-E3-012-06 | Program, section 5.9 | The legacy story's own feature | 07 Route, settle and claim | R-DIL-16; R-DIL-28 | Executed by RWB-S2-E3012-APP and the wave 2 integration harness; not owned here |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3012-APP | App development | H consumer: implements the deed-in-lieu stage, the element set and the publisher against this contract and its fakes |
| RWB-S2-E3001-CON | Contract | Referred to: the treatment contract baseline that carries the treatment representation |
| RWB-S2-E3002-CON | Contract | Referred to: the offer operation and the draft-terms change, which are not declared here |
| RWB-S2-E3003-CON | Contract | Referred to: the `TreatmentApproved` envelope this contract uses and never restates |
| RWB-PLT-E1027-CON | Contract | Referred to: the local decision-record library whose shape and exceptions are named and not restated |
| RWB-PLT-N001-CON | Contract | Referred to: the gateway-bff composite route by which the screens read the element set |
| S5 rwb-asset, P3 rwb-case | Consumer and owner | Read the transferred facts and the asset reference; pin the version |
| P1 rwb-source-data, P5 rwb-document | Owner | The ACE facts and the documents, named and not read here |
| The wave 2 integration harness | Integration | The cross-service proof of the deed-in-lieu journey against the live owners |

### 19. Out of scope

- The implementation — the deed-in-lieu stage of `TreatmentWorkflow`, its seven activities, the treatment columns, the requests to the owners and the publish: RWB-S2-E3012-APP.
- The treatment resource, its creation and its field list DF-TRT-001 to DF-TRT-033: RWB-S2-E3001-CON and RWB-S2-E3001-APP.
- The offer operation `POST /treatments/{treatmentId}/offer`, the draft-terms change and the settlement range: RWB-S2-E3002-CON and RWB-S2-E3002-APP.
- The below-floor second signature and the transfer price comparison against the floor: RWB-S2-E3003-CON and RWB-S2-E3003-APP.
- The `TreatmentApproved` payload shape, its registry entry and its two consumers: RWB-S2-E3003-CON, RWB-PLT-EVT and the event platform.
- The asset record, the asset list, the AMIS interface, the core-bank settlement and the registration release: rwb-asset, rwb-integration and their own stories.
- The document templates, the document hub and the field captures of the inspection: rwb-document and FEAT-TRT-18.
- The encumbrance and eligibility check and the early valuation: FEAT-TRT-13 and the sibling stories of this service.
- The case status, the case table, the case task and the case signal: rwb-case.
- The `approval` record, the `ApprovalWorkflow`, the rule package registry and the version promotion: rwb-decision.
- The topic, its ACLs, the retry topics and the dead-letter topic: the event platform and the platform infrastructure stories.
- The deployment, the flag and the dashboards of this build: this legacy key's DevOps story.
- The real cross-service proof of the journey against the live rwb-case, rwb-asset, rwb-document and rwb-integration: the wave 2 integration harness.

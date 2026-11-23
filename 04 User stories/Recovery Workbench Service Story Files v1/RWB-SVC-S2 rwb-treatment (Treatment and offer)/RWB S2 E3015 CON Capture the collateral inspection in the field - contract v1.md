# RWB-S2-E3015-CON Capture the collateral inspection in the field - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E3-015 for rwb-treatment. The contract is published on Day 1 and fixes the elements the treatment carries for a field inspection (`inspectionOutcome`, `inspectionChecklistRef`, `inspectionPhotoRefs`, `inspectionBillRefs`, `inspectedAt`, `fieldOfficerRef`), their domains and their absent-until rule, the rule that the capture rides on the treatment surface with no new operation, the rule that no table is created for the inspection, the checklist, the photographs or the bills, the reference to rwb-document for the content, the validation and refusal rules, the compatibility rule and the fakes; the implementation is RWB-S2-E3015-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3015-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-015 |
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

As a **contract owner of rwb-treatment**, I want **the published contract of the field-inspection capture — the six elements the treatment carries from the visit to the asset-unlock decision with their domains and their absent-until rule, the rule that the capture rides on the treatment surface its siblings publish and declares no operation of its own, the rule that no table is created for the inspection, the checklist, the photographs or the bills, the reference to rwb-document for the content, the validation and refusal rules, the compatibility rule and the fakes — instead of the monolith's free-text inspection note, its `document` rows in the shared `recovery` schema and its `v_ace_collateral` read**, so that **RWB-S2-E3015-APP can build and test the capture on Day 1, the field app and the three screens can pin the elements they show, and no team adds an inspection table or a checklist table to hold what the treatment already holds**.

### 2. Business rationale

The monolith kept the whole visit in one place: the S2 service set `recovery_case.status` itself, wrote `decision_log_entry` with the rule version, wrote `document` rows for the photographs and the bills, and read `v_ace_collateral` and `v_ace_collateral_detail` in process for the title document number, the plot number and the lien rank. Three consequences followed that the target cannot keep. The case status moved in the case table, so no step could announce an outcome. The inspection had no shape of its own, so the checklist, the photographs and the bills were distinguished by screens, free text and file names. And a team adding a checklist would have added a table, and a team adding the bills would have added another, so the same visit would be recorded three times against one case.

In the 19-service target the case status is rwb-case's (ASM-4409), the record is the platform library's and local to the service (DP-03), the collateral facts are rwb-source-data's and arrive as facts (DP-05), the documents are rwb-document's (ASM-4410), and the field app reaches the service through the gateway-bff composite route (DP-19). What is left for this contract is the part two other teams and the screens depend on: what a field inspection carries on the treatment, and how it is written without a second table and without a new operation.

The TSD lists DF-TRT-001 to DF-TRT-033 and has no inspection, no checklist and no bill, and the FSD's field catalog for A2.15 repeats the generic treatment fields only, so the element names and their domains are Not specified in the source documents (GAP-2679; ASM-4410). The contract fixes them for the wave rather than leaving each squad to invent its own.

**The division of the legacy key is fixed.** This WP delivers the **contract**. The **implementation** — the field-inspection step of `TreatmentWorkflow`, its four activities, the treatment columns and the report to the parent — is **RWB-S2-E3015-APP**, and the **cross-service proof** is the wave 2 integration harness. The four legacy acceptance criteria **stay with RWB-S2-E3015-APP** and are not copied here: every criterion in section 7 is new (D-RCV-60) and tests only the contract deliverable in this title.

The contract has to exist before the code for three reasons. The field app and the screens show the elements and need their names on Day 1. The element set is what stops a second and a third table: a squad that finds no element for the checklist adds a table, and the visit is then recorded twice. And the compatibility rule lets consumers pin a version while the step is still being built, with the fake as the Day-1 unblocker before rwb-document exists.

### 3. Preconditions

- The treatment of the case is rwb-treatment's own object in schema `rwb_treatment` (Ownership Map row `treatment`, owner S2), with DF-TRT-001 to DF-TRT-033 and `treatment_type` taking the value DEED_IN_LIEU of LOV-TREATMENT (TSD S2 T3.1 and T3.2).
- The published names are reused where they exist: the treatment resource and its read are RWB-S2-E3001-CON's, and the terms change by which the capture is written is RWB-S2-E3002-CON's `PATCH /treatments/{treatmentId}`; this contract adds no operation and no path.
- No element of an inspection exists on the treatment, which is the gap this contract closes for the wave: the six names, their domains and their absent-until rule are the working read of it (GAP-2679; ASM-4410).
- The service owns one event in the catalogue, `TreatmentApproved` (EV-10), topic `rwb.treatment.events.v1`; the inspection publishes nothing, and no source names an event for it (GAP-2679).
- The rules that answer the step are in force as data: R-DIL-18 schedules the visit and R-DIL-22 answers on the checklist, the photographs and the bills (Business Rules and Routing Logic v4). The checklist items and the required set are reference values of their owner, never a list held by this contract.
- The checklist, the photographs and the bills are rwb-document's artefacts, reached through Temporal on its queue; this contract declares their references only (ASM-4410).
- The collateral facts are rwb-source-data's read and reach the step as facts; no ACE view is named by this contract (DP-05; ASM-4409).
- The decision record is written through RWB-PLT-E1027-CON, whose write refuses with MSG-P7-009 and fails with MSG-P7-003; this contract declares the record's use and not its shape (DP-03).
- The access surface is the platform guard's: capability area "Treatment and offer", right U, with the roles TSD S2 T6.1 lists (ASM-4412).
- No build dependency and no approval stop: a CON story is Day 1 by rule and is published at status Draft (realignment v1) (ASM-4413).

### 4. Flow

1. The contract author fixes the element set of a field inspection: the six named elements with their domains, their nullability and their absent-until rule.
2. The author fixes the no-new-table rule and states where each fact already lives: the treatment row for the outcome and the references, rwb-document for the content, rwb-case for the status and the task, rwb-source-data for the collateral facts.
3. The author fixes the surface rule: the capture is written through the treatment change of RWB-S2-E3002-CON, this contract declares no operation, no path, no media type and no event of its own.
4. The author writes the validation and refusal rules: a required element empty refuses with MSG-GEN-001, an unrecordable decision stops the step with MSG-P7-003, a refused record answers MSG-P7-009, and a role without right U is refused with MSG-P4-002.
5. The author writes the compatibility rule: which change keeps major version 1, which raises major version 2 with a new revision of the document, and how a consumer pins a version.
6. The author writes the fake set: an element fake covering each inspection state and each absence, a capture fake for the surface, a consumer fake for the field app and the three screens, and the decision-record fake reference.
7. The lint step runs: the element names compared with the treatment representation and the TSD list, the examples scanned for personal data and free text, and the schema compared with the published treatment document.
8. The contract test runs the fakes against the document on every change and fails the build on any drift in this story and in RWB-S2-E3015-APP.
9. The document and the fakes are published at v1; RWB-S2-E3015-APP, the field app and the three screens pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A team adds an inspection, checklist, photograph or bill table, or a second write path for a capture | The boundary and drift checks fail the build; the treatment row plus the decision record are the only places an inspection fact lives | None | AC1 |
| X2 | A team adds a `/inspections` operation, a second media type or an event for the capture | The drift test fails the build; the capture rides on the treatment change and publishes nothing | None | AC2 |
| X3 | An example carries a photograph, a bill image, a document body, a name or an address | The personal-data and content scan fails the build; the elements carry references, codes and timestamps only | None | AC3 |
| X4 | A capture is written with a missing required element, or a step takes effect with no record | The contract test fails: MSG-GEN-001 names the field and MSG-P7-003 stops the step | MSG-GEN-001; MSG-P7-003 | AC4 |
| X5 | An element is renamed, removed or retyped | The change raises major version 2 and a new document revision; v1 is never edited in place and stays readable | None | AC5 |
| X6 | A value a consumer needs is named by no source — an element name, a domain or a reference shape | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-2679; ASM-4410) | AC1, AC6 |
| X7 | A consumer pins v1 and then requires a field the document does not carry | The consumer raises a change request against the published document; no private variant is built | None | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document and fakes; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | The domains, the example values and the fixture set are open until v1 is frozen; the six element names, the surface rule, the no-new-table rule and the absence of an event are fixed |
| Valuable | Unblocks RWB-S2-E3015-APP, the field app and the three screens on Day 1 and keeps three tables out of the service plan |
| Estimable | One element set, one surface rule, one rule set, one fake set and one document |
| Small | One sprint for the document, the fakes and the lint rules |
| Testable | Each criterion below is one document, schema or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: the field-inspection contract of rwb-treatment

  Background:
    Given the rwb-treatment contract document is published with major version 1
    Given the treatment of a case is owned by rwb-treatment in schema rwb_treatment
    Given the case status stays rwb-case's and reaches the step on the case signal

  Scenario: AC1 The inspection capture carries six elements and creates no new table (new, D-RCV-60)
    Given the element section of the contract document
    When it is validated against the treatment representation and the TSD
    Then a field inspection carries inspectionOutcome, inspectionChecklistRef, inspectionPhotoRefs, inspectionBillRefs, inspectedAt and fieldOfficerRef on the treatment row
    Then each element is absent until its step has answered and present with the rule's answer after it
    Then the document declares that no table is created for the inspection, the checklist, the photographs or the bills, and names decision_record as the library object of DP-03 and document as P5's
    Then a proposed inspection table, checklist table or bill table fails the boundary test

  Scenario: AC2 The capture rides on the treatment surface and declares no operation and no event (new, D-RCV-60)
    Given the surface section of the document
    When the capture is validated against the operations the service publishes
    Then the capture is written through PATCH /treatments/{treatmentId}, which RWB-S2-E3002-CON declares, and this contract declares no operation, no path, no method and no media type
    Then the document declares that the inspection completion publishes nothing and that the service's one event type remains EV-10 with its publication at the offer release
    Then the service base is /api/recovery/treatment/v1 and the schema is rwb_treatment, and this contract adds no topic and no queue

  Scenario: AC3 The captures are referenced, never carried (new, D-RCV-60)
    Given the document section of the contract
    When a completed capture is validated against it
    Then inspectionChecklistRef, inspectionPhotoRefs and inspectionBillRefs carry the references rwb-document returns, and inspectedAt and fieldOfficerRef the time and the user identifier of the actor
    Then no element carries a photograph, a bill image, a document body, a name, a national identifier, an account number, an address or free text, and the document states that rwb-document holds the content
    Then the personal-data and content scan fails the build on any of them

  Scenario: AC4 A missing required element and an unrecordable decision stop the step (new, D-RCV-60)
    Given the validation and refusal section of the document
    When a capture with a missing required element and a capture whose record cannot be written are put through it
    Then a required element empty refuses with MSG-GEN-001 and the field name, and nothing is written
    Then the decision record is written through DecisionRecordWriter with propagation MANDATORY, and an unavailable writer answers MSG-P7-003 and rolls the treatment back
    Then a refused record answers MSG-P7-009 with the field, and a role without right U is refused with MSG-P4-002

  Scenario: AC5 A compatible change keeps major version 1 and a breaking change raises version 2 (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published element
    Then an added optional element keeps major version 1 and is accepted in BACKWARD mode
    Then a renamed, removed or retyped element raises major version 2, and v1 is never edited in place
    Then RWB-S2-E3015-APP, the field app and the three screens each pin a published version and raise a change request rather than a private variant

  Scenario: AC6 The fakes answer the document and the drift test runs on both sides (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the element fake, the capture fake, the consumer fakes and the decision-record fake
    Then the element fake answers a treatment at each inspection state, one with no checklist, one with no photographs and one with no bills
    Then the capture fake accepts a body with the six elements and refuses one with a field outside the document
    Then the consumer fakes of the field app and the three screens accept the capture and refuse one with no key
    Then the drift test fails on any difference from sections 12 and 13 in this story and in RWB-S2-E3015-APP
```

These criteria are new and test only the contract deliverable: no legacy acceptance criterion is repeated here — **AC1 to AC4 of RWB-E3-015 stay with RWB-S2-E3015-APP** — and every identifier comes from the legacy story, the TSD, Architecture v5, the BRD or the Business Rules and Routing Logic, character for character. The element names, their domains and the absence of an inspection event are Not specified in the source documents (GAP-2679; ASM-4410).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A field inspection carries `inspectionOutcome`, `inspectionChecklistRef`, `inspectionPhotoRefs`, `inspectionBillRefs`, `inspectedAt` and `fieldOfficerRef` on the treatment, and no table is created for any of them | GAP-2679; ASM-4410 |
| BR2 | The capture is written through the treatment change `PATCH /treatments/{treatmentId}` and this contract declares no operation, no path and no media type | RWB-S2-E3002-CON; Template and Rules §R7.2 |
| BR3 | The service publishes one event type, `TreatmentApproved` (EV-10), and this path publishes it at no point; the inspection completion is announced by no event | Architecture v5 slide 42 row 10; GAP-2679 |
| BR4 | The elements carry references, codes and timestamps only: no photograph, bill image, document body, name, national identifier, account number, address or free text | NFR-054; ASM-4410 |
| BR5 | A required element empty refuses with MSG-GEN-001 and the field name, and nothing is written | VR-S2-015-1; FSD S2 A2.15.3.1 |
| BR6 | Every capture is recorded through DecisionRecordWriter with propagation MANDATORY, refusing with MSG-P7-009 and failing with MSG-P7-003 | DP-03; R-UNI-39; RWB-PLT-E1027-CON |
| BR7 | The checklist items, the required set, the state names and the reason codes are values in force of their owners; this contract fixes no business value | BR-S2-015; FSD S2 A2.15.3.1 |
| BR8 | The case status, the case task and the collateral facts stay with their owners: this contract declares no status and no read | DP-01; DP-05; ASM-4409 |
| BR9 | A published version is never edited: a backward-compatible change keeps major version 1, a breaking change raises major version 2, and every consumer pins a version | Template and Rules §R7.2 |

### 9. State transitions

None in this story: a contract document has no runtime state. Two vocabularies are fixed here and the runtime behind them is specified in RWB-S2-E3015-APP section 9.

| Object | State | Meaning in the contract |
|---|---|---|
| Inspection element set | Absent | No element is present and the case has not been captured |
| Inspection element set | Checklist captured | `inspectionChecklistRef` is present and the photographs or the bills may still be missing |
| Inspection element set | Complete | All six elements are present and `inspectionOutcome` carries the value in force |
| Inspection element set | Incomplete | `inspectionOutcome` names the missing item and the step holds |
| Contract version | v1 | The published version RWB-S2-E3015-APP, the field app and the screens pin |
| Contract version | v2 | Raised by a breaking change; v1 stays readable and is never edited |

The case statuses of the route — OFFER_WITH_CUSTOMER_DIL, WITH_FIELD_INSPECTION, ASSET_UNLOCK_DECISION — are rwb-case's. This contract refers to the point at which each element is written and holds no status list of its own.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the element section, the surface rule and the fakes |
| The owner of rwb-treatment | Approves a breaking change to the element set and freezes a version |
| The rwb-document owner (P5) | Confirms the document references it returns and that the content stays with it; this contract declares none of the content |
| The rwb-case owner (P3) | Confirms that no case status, no case task and no case event is declared here |
| The rwb-source-data owner (P1) | Confirms that the collateral facts reach the step as facts and that no view is read here |
| The rwb-decision owner (P7) | Confirms the rule packages and their versions |
| The field app and screen owners | Confirm the elements they show and pin the version |
| RW-AUDIT, RW-COE | Audit the decisions through the P7 ledger and the local record, not through this contract |
| No delegation of authority level applies | A service contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in the document, an example or a fake. Where an actor must be named, the example uses a role code or a user identifier only.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The document publishes element names, domains, codes and message identifiers; no customer, account or case value appears outside a synthetic example |
| Element set published | `inspectionOutcome`, `inspectionChecklistRef`, `inspectionPhotoRefs`, `inspectionBillRefs`, `inspectedAt`, `fieldOfficerRef`, with the domains and the absent-until rule of section 12.1 |
| Personal data | None. `fieldOfficerRef` is a user identifier and the references are system references; no name, address, national identifier or document content appears |
| Tables published | None created: the treatment row of S2, the library object `decision_record` of DP-03, P5's `document` and P3's `recovery_case` are named, and the document declares that no table is added for the inspection, the checklist, the photographs or the bills |
| Field identifiers | None of the six elements carries a field ID in the TSD, which stops at DF-TRT-033 (GAP-2679; ASM-4410) |
| Retention | The treatment row and the local record follow their owners' retention; the documents follow rwb-document's retention class |

The element set is the one place where a business value could leak into the contract, so the document fixes that an element carries a code, a reference or a timestamp and never a checklist item, a threshold or a clock.

### 12. Contract

#### 12.1 REST operations provided

None. This contract declares no REST operation, no path, no method and no media type. The treatment resource and its read are RWB-S2-E3001-CON's, and the terms change `PATCH /treatments/{treatmentId}` is RWB-S2-E3002-CON's; the capture is an update of the treatment through that surface. The service base is `/api/recovery/treatment/v1` (DP-13).

| Element | Domain | Absence rule |
|---|---|---|
| `inspectionOutcome` | The checklist result of R-DIL-22: complete, or incomplete with the missing item named | Absent until R-DIL-22 has answered |
| `inspectionChecklistRef` | A document identifier returned by rwb-document for the completed checklist | Absent until the checklist is stored |
| `inspectionPhotoRefs` | A set of document identifiers returned by rwb-document for the photograph set | Absent until the photographs are stored |
| `inspectionBillRefs` | A set of document identifiers returned by rwb-document for the bills of the visit | Absent until the bills are stored |
| `inspectedAt` | timestamptz of the completed capture | Absent until the capture is recorded |
| `fieldOfficerRef` | The user identifier of the officer who captured | Absent until the capture is recorded |

#### 12.2 REST operations consumed

None. The contract consumes no operation: the case status and the collateral facts arrive on the case signal, the documents are requested on rwb-document's queue through Temporal, and the rule version arrives as an event. RWB-S2-E3015-APP consumes no service by REST either.

#### 12.3 Events published

None of its own. The service publishes one event type and this contract refers to it rather than restating it.

| Event | Topic | Key | This contract | Purpose |
|---|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | `caseId` | Refers to the envelope fixed by RWB-S2-E3003-CON, published at the offer release by RWB-S2-E3012-APP; the inspection completion publishes nothing | EV-10: tells rwb-comms to issue the offer documents and rwb-payment to expect the settlement of the debt |

No source names an event for the inspection completion: the outcome reaches rwb-case on the case signal, inventing a second event would break the one-event rule of the catalogue, and the absence is Not specified in the source documents (GAP-2679).

#### 12.4 Events consumed

None. The contract consumes no event; `rwb.decision.RulePackageInForce.v1` (EV-30) is consumed by RWB-S2-E3015-APP and names a version this document refers to only as the rule version of an answer.

#### 12.5 Workflows and activities

None. The contract defines no workflow and no activity. The step that writes the treatment and the record is RWB-S2-E3015-APP's, and the document requests run on rwb-document's queue; a workflow class never writes the element set.

#### 12.6 Schedules

None. The inspection has no clock in any source and owns no Temporal Schedule and no legacy Quartz job; the locks of the route are workflow timers of their own steps, and this contract declares none.

#### 12.7 Tables owned

| Table | Schema | Owner | Note |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Carries the six inspection columns; no column of a checklist item, a threshold or a clock is added |
| `decision_record` | `rwb_treatment` | PLT (library object, DP-03) | The record of each capture, written through RWB-PLT-E1027-CON in the same transaction; its shape is that contract's and is not restated here |
| `outbox` | `rwb_treatment` | S2, from the service template | Not written on this path: the inspection publishes nothing |
| (none) | — | — | No table is created for the inspection, the checklist, the photographs or the bills, and no foreign key crosses a schema |
| `document` | `rwb_document` | P5 | Named only: the content, the templates and the retention are its own |
| `recovery_case`, `assignment` | `rwb_case` | P3 | Named only: the status and the task are its own |
| `v_ace_collateral`, `v_ace_collateral_detail` | ACE views, `rwb_source_data`'s read | P1 | Named only: the facts reach the step on the case signal and are never read here |

The no-new-table rule is the contract's, not a coding preference: a second table would let one visit be recorded twice, once as a row and once as a reference, which DP-01, DP-03 and Principle 5 forbid. The six columns are added on the service's own migration sequence by RWB-S2-E3015-APP, and this contract fixes their names and domains only (GAP-2679; ASM-4410).

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Element fake | The six elements | A treatment at each state of section 9; one with no checklist, one with no photographs and one with no bills; an incomplete capture naming its missing item |
| Capture fake | The body written through the treatment change | A body with the six elements accepted; a body with a field outside the document refused; a body with no key refused |
| Consumer fake of the field app | The capture screen | A complete capture rendered from the six elements; an incomplete capture with its missing item |
| Consumer fake of the three screens | SCR-14, SCR-15 and SCR-16 | A treatment at each inspection state; a refusal when the element is absent |
| Decision-record fake | The record write of DP-03 | An accepted record with chain sequence and entry hash; a refusal with MSG-P7-009 and the field; an unavailable writer with MSG-P7-003 |

The fakes answer from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consuming story rather than as a surprise at run time.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0: the contract declares no operation | 0 | The treatment resource is RWB-S2-E3001-CON's and the terms change RWB-S2-E3002-CON's |
| Kafka | 0 new: one existing event type referred to | 0 | CloudEvents 1.0 envelope, key `caseId` on `rwb.treatment.events.v1` |
| Temporal | 0 | 0 | No workflow and no activity; the step and the document requests are the APP story's |
| File | 0 | 0 | The photographs and the bills are documents of rwb-document and cross no boundary here |

### 13. Solution plan

**Package.** Contract artefact of rwb-treatment: the element set and the surface rule in the service's contract document, with the published types in `th.co.scb.ace.workbench.recovery.treatment.api` for the inspection elements. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`. The implementation is RWB-S2-E3015-APP.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; this contract declares the record's use and not its shape | referred to; the consuming story carries the dependency |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | ACE data read through rwb-source-data's contract; on this path the collateral facts arrive on the case signal and no view is named | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the contract adds no path | referred to; the consuming story carries the dependency |
| DP-19 | Screen, ace-web | gateway-bff composite route; the field app and the three screens read the element set through the route | referred to; the consuming story carries the dependency |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `InspectionElement` | Document section | The six names, their domains and their absent-until rule (BR1) |
| `SurfaceRule` | Document section | The capture rides on the treatment change, no operation, no path, no media type and no event (BR2, BR3) |
| `ValidationAndRefusalRule` | Document section | MSG-GEN-001, MSG-P4-002, MSG-P7-003 and MSG-P7-009, and the transaction rule (BR5, BR6) |
| `VersioningSpecification` | Document section | Major version 1, the compatible versus breaking rule and the pinning rule (BR9) |
| Fake set and fixtures | Test asset | The element, capture, consumer and decision-record fakes (AC6) |

**Build steps**

1. Write the element section against the treatment representation and the TSD list, and lint the names and domains (AC1).
2. Write the no-new-table rule and name `decision_record`, `document`, `recovery_case` and the ACE views with their owners (AC1, AC3).
3. Write the surface rule and validate a capture body against the treatment change of RWB-S2-E3002-CON; assert that no operation and no event is added (AC2).
4. Write the validation and refusal rules with the four messages and the transaction rule (AC4).
5. Write the versioning section with the compatible and the breaking example (AC5).
6. Generate the fake set and the drift test for this story and RWB-S2-E3015-APP (AC6).
7. Scan every example for personal data and content and publish v1 with the pinned versions recorded (AC3, AC5).

**Feature flag.** `rwb.treatment.field-inspection`.

**Done when.** The document validates, a capture body with the six elements passes the fake and a body with an extra field is refused, the element fake answers every state and every absence, the consumer fakes accept the capture and refuse one with no key, the drift test is green on this story and on the build of RWB-S2-E3015-APP, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-GEN-001 | A required element of the capture is missing | Enter {field}. | The caller's screen; the contract fixes the element, not the display |
| MSG-P4-002 | A role without right U acts on the capture | You cannot {action} here. Your role does not include it. | The guard's answer, unchanged |
| MSG-P7-003 | The decision record cannot be written and the step is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. | `DecisionLogUnavailableException` of RWB-PLT-E1027-CON |
| MSG-P7-009 | The record is refused for a missing or invalid field (service log and incident, not shown to customers) | The decision record was refused: {field} is missing or not valid. | `DecisionLogRecordInvalidException` with `field` |
| MSG-S2-001 | A settlement figure of the case is below the floor and has been routed for approval (sibling slices) | The offer is below the floor of {floor}. It has been sent for approval. | The caller's screen |
| MSG-S2-002 | The figure behind the offer is stale when the screen is read | The payoff is from {date}. A new figure has been requested. | The caller's screen |
| MSG-S2-003 | The offer to the customer carries its end date | The offer to the customer ends on {date}. | The offer slice's element |

The texts are copied unchanged from RWB-E3-015 and from the decision-record contract; this story adds no message ID. MSG-P7-003 and MSG-P7-009 are the two exceptions that keep a step from taking effect without its record. Thai text follows decision DL10.

### 15. Screens and states

No screen is declared by this contract, and it fixes no field of one. SCR-14 Treatment record (Draft; submitted; approved; booked; broken) and SCR-15 Settlement offer (Draft; below floor; approved; sent; accepted) are the two screens the legacy story names, SCR-16 Deed in lieu (Checks; appraisal; approved; transferred) is the screen of the route, and the capture itself is opened on the field app, which is the integration point the FSD names for FEAT-TRT-15. None of the four is specified with a field list, so the contract fixes only the element names, the domains and the absent-until rule, and a screen can show "captured, awaiting unlock" without inventing a field (GAP-2679; ASM-4412). All of them reach this service through the gateway-bff composite route (DP-19).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S2-E3015-CON-01 | AC1 | Contract | The element section linted against the treatment representation and the TSD list; the six elements with their domains and absent-until rule; the no-new-table statement; a proposed inspection, checklist and bill table refused |
| TC-S2-E3015-CON-02 | AC2 | Contract | A capture body validated against the treatment change of RWB-S2-E3002-CON; no operation, no path and no event added; the service base and the schema asserted |
| TC-S2-E3015-CON-03 | AC3 | Contract | The three reference elements and the two stamping elements; the content scan refusing a photograph, a bill image, a name and a free-text field |
| TC-S2-E3015-CON-04 | AC4 | Contract | A missing required element with MSG-GEN-001, a forced record failure with MSG-P7-003, a refused field with MSG-P7-009 and a role without right U with MSG-P4-002 |
| TC-S2-E3015-CON-05 | AC5, AC6 | Component | A compatible change and a breaking change against the registry; the element, capture and consumer fakes; the drift test on this story and on RWB-S2-E3015-APP |

The legacy test set of RWB-E3-015, TC-E3-015-01 to TC-E3-015-06, is carried by RWB-S2-E3015-APP and by the wave 2 integration harness; these five are the contract's own tests and no legacy id is renumbered.

### 17. Guardrails

- No business value in the contract: the checklist items, the required set, the state names and the reason codes are values in force of their owners; the only values this document fixes are the element names, their domains and the synthetic examples.
- No personal data and no document content in a schema, an example, a fake or a log: the references are system references and `fieldOfficerRef` is a user identifier.
- No new table for the inspection, the checklist, the photographs or the bills, and no second write path for a capture fact.
- No cross-schema reference and no foreign key across services: `document`, `recovery_case` and the ACE views are named, never joined and never read.
- No REST surface of this contract's own and no new event: the treatment resource and the terms change belong to sibling CON stories, and the one event type is published by the offer slice.
- A published version is never edited in place: a breaking change raises major version 2 with a migration note and every consumer pins a version.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| Not specified in the source documents (GAP-2679; ASM-4410) | No requirement of the FSD S2 maps to FEAT-TRT-15; REQ-S2-001 to REQ-S2-010 are traced to FEAT-TRT-01 (TSD S2 T8) | Business Requirements Program, section 5.9 | FEAT-TRT-15 | 07 Route, settle and claim | R-DIL-22 | TC-S2-E3015-CON-02 |
| (no requirement ID) | The inspection answer feeds the deed-in-lieu readiness of the route | Business Requirements Program, section 5.9 | FEAT-TRT-15 | 07 Route, settle and claim | R-DIL-18; R-DIL-22 | TC-S2-E3015-CON-01 |
| Legacy test set RWB-E3-015 | TC-E3-015-01, TC-E3-015-02, TC-E3-015-03, TC-E3-015-04, TC-E3-015-05, TC-E3-015-06 | Program, section 5.9 | The legacy story's own feature | 07 Route, settle and claim | R-RES-12; R-SET-09; R-DIL-22 | Executed by RWB-S2-E3015-APP and the wave 2 integration harness; not owned here |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3015-APP | App development | H consumer: implements the capture, the six columns and the report against this contract and its fakes |
| RWB-S2-E3001-CON | Contract | Referred to: the treatment contract baseline that carries the treatment representation |
| RWB-S2-E3002-CON | Contract | Referred to: the terms change `PATCH /treatments/{treatmentId}` through which the capture is written |
| RWB-S2-E3012-CON | Contract | Referred to: the deed-in-lieu element set of the same stage, of which the inspection is a step |
| RWB-S2-E3003-CON | Contract | Referred to: the `TreatmentApproved` envelope this contract refers to and never restates |
| RWB-PLT-E1027-CON | Contract | Referred to: the local decision-record library whose shape and exceptions are named and not restated |
| RWB-PLT-N001-CON | Contract | Referred to: the gateway-bff composite route by which the field app and the screens read the element set |
| P3 rwb-case, P5 rwb-document | Owner | The case status and task, and the content of the checklist, the photographs and the bills |
| P1 rwb-source-data | Owner | The collateral facts, named and not read here |
| The wave 2 integration harness | Integration | The cross-service proof of the capture against the live owners |

### 19. Out of scope

- The implementation — the field-inspection step of `TreatmentWorkflow`, its four activities, the six treatment columns and the report to the parent: RWB-S2-E3015-APP.
- The treatment resource, its creation and its field list DF-TRT-001 to DF-TRT-033: RWB-S2-E3001-CON and RWB-S2-E3001-APP.
- The terms change, the offer operation and the settlement range: RWB-S2-E3002-CON and RWB-S2-E3002-APP.
- The below-floor second signature and the floor comparison: RWB-S2-E3003-CON and RWB-S2-E3003-APP.
- The deed-in-lieu element set, the scheduling of the visit (R-DIL-18) and the transfer (R-DIL-28): RWB-S2-E3012-CON and RWB-S2-E3012-APP.
- The asset-unlock rule that follows the capture (R-DIL-23 to R-DIL-26): the slice of RWB-E3-014.
- The checklist items, the required set and their versions: the reference data of their owner and the rule package registry.
- The checklist, the photographs, the bills, their templates, their custody and their retention: rwb-document and FEAT-TRT-18.
- The field app, its offline behaviour and its device capture: the platform edge and the field app's own stories.
- The case status, the case table and the inspector's task: rwb-case and RWB-P3-E1018.
- The rule packages, their versions and the ledger: rwb-decision.
- The topic, its ACLs, the retry topics and the dead-letter topic: the event platform and the platform infrastructure stories.
- The deployment, the flag, the dashboards and the alerts of this build: this legacy key's DevOps story.
- The real cross-service proof against the live rwb-case and rwb-document: the wave 2 integration harness.

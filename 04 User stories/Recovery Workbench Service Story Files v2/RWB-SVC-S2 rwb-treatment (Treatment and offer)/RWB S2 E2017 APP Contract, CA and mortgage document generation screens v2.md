# RWB-S2-E2017-APP Contract, CA and mortgage document generation screens

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: secondary slice of legacy RWB-E2-017 for rwb-treatment (S2). The screens, the overrides, the review action, the regenerate operation and the send stay with RWB-P5-E2017-APP in rwb-document and keep the thirteen legacy criteria; this story delivers the treatment leg of SCR-14 only — the optional `documentPanel` section of the treatment read on the base `/api/recovery/treatment/v1` (DP-13), which carries the treatment-side gate (approved and open, from this service's own `treatment` row in `rwb_treatment`, DP-01), the set the treatment type requires read as reference data at its version (DP-07), and the set summary read in one hop from the set operation of RWB-P5-E2017-CON with a 2 s timeout and a fake (DP-11), so the screen knows whether to offer Generate and Send and why not; the section is reached on SCR-14 through the gateway-bff composite route (DP-19) and the approval fact is the reference to the local decision record the approval story wrote through the DP-03 library, which this story reads and never writes. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S2-E2017-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 23 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E2017-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP11, DP13, DP19 |
| Parallel lane | L-S2-F |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S2-E2017-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E2017-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to REQ-DCM-012, REQ-OCC-002, REQ-OCC-009) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **restructuring officer (FCR)**, I want **SCR-14 to tell me, on the treatment itself, which document set this treatment must carry, whether I may generate it, and whether the set in front of me is ready to send for signature**, so that **I do not ask for a set on a treatment that is not approved, do not send an incomplete set, and never have to read the document hub's tables to know where the set stands**.

This is the treatment-side slice of legacy RWB-E2-017, whose capability is the generation, review and send screens of the deed in lieu and restructure document set. It owns:

- the optional `documentPanel` section of the treatment read `GET /treatments/{treatmentId}` on `/api/recovery/treatment/v1` (API-S2-002, DP-13), served from `rwb_treatment` and from the one-hop set read of 12.2;
- the treatment gate: approved means `decision_log_id` set, open means no outcome and a state that is not closed, both read from this service's own `treatment` row (DP-01);
- the expected set of the treatment type — the document types and template codes a DEED_IN_LIEU or a RESTRUCTURE treatment must carry — read as reference data at its version through the client library of rwb-case (DP-07);
- the set summary, read in one hop from the set operation of `RWB-P5-E2017-CON` with a 2 s timeout, a breaker and a fake, filtered by `treatmentId` (DP-11);
- the action availability the screen binds to: `canGenerate` with the blocker MSG-P5-011, and `canSend` with the blocker MSG-P5-013 naming the document or the template version that stops the send, with the legacy values of AC4, AC7 and AC13 kept;
- the merged read through the gateway-bff composite route that serves SCR-14 (DP-19).

It does not own: the screens themselves, the overrides form, the regenerate operation, the review action and the send, which are RWB-P5-E2017-APP's; the published shape of those operations, which is `RWB-P5-E2017-CON`'s; the generation engine, the template catalogue, the merge fields, the Legal approval of a version, the rendered body, the write-once copy and the e-signature, which are RWB-P5-E2026-APP, P6 rwb-comms and P5 rwb-document's; the treatment terms, the offer and the plan, which are RWB-S2-E3002-APP to RWB-S2-E3005-APP; the case, its status and its tasks, which are rwb-case's (P3); the central ledger, which is P7 rwb-decision's; and the rights and the scope data, which are rwb-access's (P4).

**Panel states on SCR-14.** Empty and Loading: Not specified in the source documents (CG-ALL-8356). Error: the set summary is marked unavailable with MSG-GEN-006 and the gate still shows (X5). No access: the refusal of X7 with MSG-P4-002 or MSG-P4-003, and the section is not built.

### 2. Business rationale

The officer today copies case facts into three Word files, prints them and walks them to signature, and a late change is made by hand on the printed copy with no record. The screens of this key produce the set from the approved treatment, let the officer correct an allowed value with a recorded reason, and send the reviewed set as write-once documents. That objective does not change.

What D-RCV-60 changes on the treatment side is what the screen is allowed to say. In the monolith SCR-14 read the treatment module and the document module in one process and one `recovery` schema, so the panel could compose the set and the gate from two tables in one transaction. In the target the treatment row is `rwb_treatment`'s and the documents are `rwb_document`'s, in another service, with no grant either way (DP-01). Three things follow.

1. The gate is the treatment's and stays here: only an approved, open treatment can have its set generated, and that fact is two columns of this service's own row. It is served by the treatment read, not recomputed by the document service from a copy.
2. The set is the document service's and is read, not owned: this story asks the set operation of `RWB-P5-E2017-CON` once, on one hop with a 2 s budget and a fake, and answers with what the owner said (DP-11). A document that is refused or missing is shown as the owner reports it and never as this service's opinion.
3. The set the treatment must carry is data: which document types and template codes a DEED_IN_LIEU or a RESTRUCTURE treatment requires is a reference row read at its version (DP-07), so Legal and the product owner change the set without a release, and no template code is a constant of this service.

The approval fact the panel shows is the reference to the local decision record the approval story wrote through the DP-03 library; this story reads the reference and writes no record, because every record of the actions this key performs — the correction, the send — is the document service's and is written there (DP-03; ASM-4464). The panel reaches the officer through the gateway-bff composite route, so the browser calls no owner directly (DP-19).

Serves REQ-DCM-012, REQ-OCC-002 and REQ-OCC-009. No business value is invented: the treatment types, the document types, the template codes, the states DRAFT, REVIEWED and SENT, decision code D6.4, the message IDs and the screen IDs are the values the legacy story already carries.

### 3. Preconditions

- `RWB-P5-E2017-CON` is published: the set operation `GET /api/recovery/document/v1/cases/{caseId}/generated-documents` with the query `treatmentId` and `state` and the answer `GeneratedDocumentSetPage`, whose documents carry `documentId`, `treatmentId`, `documentType`, `templateCode`, `templateVersion`, `state`, `writeOnce`, `docVersion` and `reviewStatus`; its error set, its `Idempotency-Key` rule for the writes and its fakes (ASM-4463).
- `RWB-S2-E3001-CON` serves `GET /treatments/{treatmentId}` (API-S2-002) with `Treatment and offer R` and the scope filter; this story adds one optional property to that answer at major version 1 and changes no declared field (ASM-4463).
- `treatment` exists in `rwb_treatment` from RWB-S2-E3001-APP with DF-TRT-001 to DF-TRT-033, and the row holds treatment "TRT-0501" of type DEED_IN_LIEU with `decision_log_id` set, no outcome and an open state (ASM-4462).
- The approval reference in DF-TRT-003 resolves to the local `decision_record` the approval story wrote through the DP-03 library with decision code D6.4; a reference that does not resolve, or that resolves to another decision code, is not an approval (DP-03; ASM-4464).
- The reference-data contract and client library of rwb-case are reachable (DP-07): LOV-DOC-TYPE holds CONTRACT, CREDIT_APPROVAL and MORTGAGE_DOCUMENT at its version, and the treatment-type set row names the template codes DIL-CONTRACT, DIL-CA and DIL-MORTGAGE for DEED_IN_LIEU and RES-AGREEMENT for RESTRUCTURE, with the mapping to the three legal types (ASM-4465).
- The templates themselves, their Legal approval and their merge fields are P6 rwb-comms' and P5 rwb-document's; this story reads no template row and copies no template code into `rwb_treatment` (ASM-4465).
- `RWB-PLT-N001-CON` is published: the gateway-bff composite route that serves SCR-14 Treatment record from the case read, the treatment read and the document reads, one hop each, read only (DP-19; ASM-4466).
- The access guard is the platform library's and the capability area "Treatment and offer" with its rights is rwb-access data; this story declares the area and the right and owns no check of its own (ASM-4468).
- The parameter and reference-data client libraries and the workflow kit are service-template capabilities of wave 0; this story adds no build row for them, which is why Depends on (build) is None (ASM-4468).
- No approval is needed to build against a Draft contract baseline: a CON story is Day 1 by rule and this story starts on Day 1 with CON dependencies only (§R5.7).

### 4. Flow

1. The officer opens SCR-14 Treatment record for treatment "TRT-0501" through the gateway-bff composite route; the route calls this service once for the treatment and once for the case record of rwb-case (DP-19).
2. `TreatmentPanelService` reads the `treatment` row: the type (DF-TRT-004), the approval reference (DF-TRT-003), the outcome (DF-TRT-013) and the standard state column, and decides the gate: approved when the reference resolves to a D6.4 record, open when no outcome is set and the state is not closed (DP-03; BR1, BR2).
3. `ExpectedSetReader` reads the reference-data row of the treatment type and LOV-DOC-TYPE at their version through the client library of rwb-case, and holds the three document types and the template codes the set must carry; an unknown type answers an empty expected set and the panel names it (DP-07; BR3).
4. `DocumentSetClient` calls the set operation of `RWB-P5-E2017-CON` once, with `treatmentId` and no state filter, one hop with a 2 s timeout and a breaker, and receives `GeneratedDocumentSetPage` or a problem body (DP-11; BR4).
5. `DocumentPanelAssembler` joins the expected set, the set answer and the gate: every expected document type present once, the version of each document against the template version in force as the owner reported it, and the states DRAFT, REVIEWED and SENT as the owner reported them (BR4, BR5).
6. The assembler sets `canGenerate` from the gate and `canSend` from the set: all of the set REVIEWED and on the current template version and none SENT; the blocker carries MSG-P5-011 on the gate and MSG-P5-013 naming the document or the version on the set (BR6, BR7).
7. The section answers inside the treatment read with 200; the route merges it with the case read and the screen shows the terms, the set, the two buttons and the reason a button is disabled.
8. The officer chooses Generate documents or Send for signature; the browser calls the operations of `RWB-P5-E2017-CON` through the route, and this service is not called and writes nothing. After the action the screen re-reads the panel and shows the new state the document service reports (BR8).
9. A refused or unavailable set read never fails the treatment read: the panel still answers the gate and marks the set summary unavailable with MSG-GEN-006 naming "Document service" (BR9; X5).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The treatment is not approved: no `decision_log_id`, or a reference that does not resolve to D6.4 | The panel answers 200 with `canGenerate` false and the blocker; the screen disables Generate and shows the message | MSG-P5-011 | AC2 |
| X2 | The treatment is closed or carries an outcome | The same as X1, with the gate closed on the outcome | MSG-P5-011 | AC2 |
| X3 | The treatment type is unknown to the reference row | The expected set is empty, `setComplete` false and the panel names the type; nothing else is guessed and no default set is used | MSG-P5-013 | AC6 |
| X4 | A document of the set is still DRAFT | `canSend` false; the panel names the document as the owner reported it, and the send operation itself answers 422 in P5 | MSG-P5-013 | AC4 |
| X5 | The document service answers 503, or does not answer inside 2 s | The treatment read still answers 200 with the gate and marks the set summary unavailable; nothing is written and no retry chain runs from the read | MSG-GEN-006 | AC5 |
| X6 | A document was made from a template version that is no longer current | `canSend` false and the panel names the document and the version in force; the officer regenerates through P5 | MSG-P5-013 | AC4 |
| X7 | The caller holds no Treatment and offer R, or the case lies outside the scope | 403 with MSG-P4-002, or 404 with MSG-P4-003, from the guard and the scope filter of the declared read; the section is not built | MSG-P4-002, MSG-P4-003 | AC7 |
| X8 | A component, a statement or a test reads `rwb_document`, `rwb_comms`, `rwb_case`, `rwb_decision` or a `v_ace_*` view | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC9, AC10, BR10 |

X1 to X4 and X6 are the legacy gates of AC4, AC7 and AC13 carried onto the panel and reported with the legacy messages; X5 is the unavailability the one-hop read adds; X7 is the guard's answer; X8 is the boundary of the target. The panel writes nothing on any path, so no exception path leaves a partial state behind.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against the `RWB-P5-E2017-CON` set fake, the reference-data fake and the route fake; needs no live rwb-document, rwb-case or rwb-comms |
| Negotiable | The section and property names, the client budget and the reading of an unknown type are this story's design; the treatment types, the document types, the template codes, the states, the messages and the screens are values in force |
| Valuable | The officer sees on the treatment whether the set may be generated, what it must contain and what stops the send, without reading another service's tables |
| Estimable | One read section, one client, one gate, one expected-set reader and one assembler |
| Small | Fits within two weeks: one week inside the two-week lane, because the screens, the actions and their records are P5's |
| Testable | Each of the twelve criteria of section 7 is one automated test, and every cross-service answer is stubbed in a contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Contract, CA and mortgage document generation screens — the rwb-treatment panel

  Background:
    Given case "RW-2026-000501" with product group "MORTGAGE" in team "FCR-BKK"
    Given treatment "TRT-0501" of type "DEED_IN_LIEU" approved at D6.4 with decision_log_id set and no outcome
    Given a restructuring officer with role RW-RESTRUCT and scope team "FCR-BKK"

  Scenario: AC1 The treatment panel answers the generation gate (new, D-RCV-60)
    Given treatment "TRT-0501" is open and its decision_log_id resolves to a local decision record with decision code "D6.4"
    When the officer reads "TRT-0501" on /api/recovery/treatment/v1/treatments/TRT-0501
    Then the answer carries the optional documentPanel section with treatmentApproved true, treatmentOpen true, treatmentType "DEED_IN_LIEU", productGroup "MORTGAGE" and canGenerate true
    Then the gate is built from the treatment row and its local decision record only
    Then no document, template, case or decision_log_entry table of another service is read

  Scenario: AC2 A treatment that is not approved, or is closed, cannot generate (new, D-RCV-60)
    Given treatment "TRT-0502" of type "DEED_IN_LIEU" has no decision_log_id
    When the officer reads the panel for "TRT-0502"
    Then treatmentApproved is false, canGenerate is false and blockerMessageId is "MSG-P5-011"
    Given treatment "TRT-0503" of type "DEED_IN_LIEU" is approved and carries outcome "CANCELED"
    When the officer reads the panel for "TRT-0503"
    Then treatmentOpen is false, canGenerate is false and blockerMessageId is "MSG-P5-011"
    Then both reads answer 200 with the treatment shown, and the refusal of the generate operation itself is the document service's 409 with MSG-P5-011 and is not restated here

  Scenario: AC3 The set summary is read from the document service in one hop (new, D-RCV-60)
    Given the rwb-document contract mock returns for treatment "TRT-0501" one document of type "CONTRACT" with templateCode "DIL-CONTRACT" and templateVersion 2, one of type "CREDIT_APPROVAL" with templateCode "DIL-CA" and templateVersion 1, and one of type "MORTGAGE_DOCUMENT" with templateCode "DIL-MORTGAGE" and templateVersion 1, all in state "REVIEWED"
    When the officer reads the panel for "TRT-0501"
    Then the section lists the three documents with the type, the template code, the template version, the state, the docVersion and the writeOnce flag of each
    Then the call is one hop with a 2 s timeout and a breaker, and no document row is read from rwb_document
    Then the panel writes nothing and holds no copy of the set

  Scenario: AC4 Send availability follows the set the owner reports (new, D-RCV-60)
    Given the set answer returns the three documents in state "REVIEWED" at template versions 2, 1 and 1, and version 2 is the version in force for "DIL-CONTRACT"
    When the officer reads the panel for "TRT-0501"
    Then canSend is true and blockerMessageId is empty
    Given the set answer returns "DIL-MORTGAGE" in state "DRAFT"
    Then canSend is false and blockerMessageId is "MSG-P5-013" naming the mortgage document
    Given the set answer returns "DIL-CONTRACT" at template version 2 while version 3 is in force
    Then canSend is false and blockerMessageId is "MSG-P5-013" naming the contract and "template version 3"

  Scenario: AC5 The document service being unavailable does not break the treatment read (new, D-RCV-60)
    Given the rwb-document contract mock answers 503 with MSG-GEN-006 naming "Document service", or does not answer inside 2 s
    When the officer reads the panel for "TRT-0501"
    Then the response is 200 with treatmentApproved, treatmentOpen and canGenerate exactly as the treatment row gives them
    Then the set summary is marked unavailable with messageId "MSG-GEN-006" and the document count is reported as unknown
    Then nothing is written, no retry chain runs from the read, and a later read when the service answers fills the summary

  Scenario: AC6 The set must be the set the treatment type requires (new, D-RCV-60)
    Given the reference-data mock returns LOV-DOC-TYPE with "CONTRACT", "CREDIT_APPROVAL" and "MORTGAGE_DOCUMENT" at its version
    Given the treatment-type set row of "DEED_IN_LIEU" names the template codes "DIL-CONTRACT", "DIL-CA" and "DIL-MORTGAGE" at its version
    Given the set answer returns only the documents of "DIL-CONTRACT" and "DIL-CA"
    When the officer reads the panel for "TRT-0501"
    Then setComplete is false, blockerMessageId is "MSG-P5-013" naming the mortgage document, and canSend is false
    Then canGenerate stays true, because the set can still be generated
    Then no document type and no template code is written in code: both are read at their version

  Scenario: AC7 The panel reaches SCR-14 through the composite route (new, D-RCV-60)
    Given the gateway-bff composite route serves SCR-14 Treatment record for case "RW-2026-000501"
    When the officer opens SCR-14
    Then the screen shows the treatment terms with the panel's generate and send availability and the set summary, merged from the treatment read of this service and the case read of rwb-case
    Then the browser calls no owner service directly, and this service serves no screen field list and no layout
    Then a caller without Treatment and offer R is refused with MSG-P4-002, and a case outside the caller's scope with MSG-P4-003

  Scenario: AC8 The panel carries no personal value and publishes no event (new, D-RCV-60)
    Given treatment "TRT-0501" is linked to case "RW-2026-000501" and to party identifiers, never to names
    When the panel is read and the log lines are written
    Then the section carries caseId, treatmentId, documentType and templateCode codes, template versions, states, counts and dates only
    Then it carries no merge value, no party name, no national ID number, no address and no file byte
    Then this story publishes no event, writes no outbox row and puts no message on rwb.treatment.events.v1
    Then no log line and no span attribute carries a personal value, and the profile codec is on every payload

  Scenario: AC9 A statement on a table outside the grant is refused (new, D-RCV-60)
    Given the rwb_treatment login and the panel component are built
    When a statement reads a table of section 12.7 other than treatment or decision_record, or a v_ace_* view
    Then the grant refuses the statement and the boundary test fails the build
    Then nothing is released

  Scenario: AC10 A component, a statement or a test that reads a restricted table or view fails the build (new, D-RCV-60)
    Given the rwb_treatment login, the panel component and the boundary test are built
    When a component, a statement or a test reads rwb_document, rwb_comms, rwb_case, rwb_decision or a v_ace_* view
    Then the grant refuses the statement, the build fails and nothing is released

  Scenario: AC11 An unavailable document service leaves the gate answer intact (new, D-RCV-60)
    Given the rwb-document contract mock answers 503
    When the officer reads the panel for "TRT-0501"
    Then treatmentApproved, treatmentOpen and canGenerate are answered exactly as the treatment row gives them
    Then only the set summary is marked unavailable

  Scenario: AC12 The treatment read answers 401, 403 and 404 as the declared error set (new, D-RCV-60)
    Given the caller presents no valid session
    When the officer reads "TRT-0501" on /api/recovery/treatment/v1/treatments/TRT-0501
    Then the answer is 401 with Not specified in the source documents (NEWAC-RWB-S2-E2017-APP-AC16)
    Given a caller without Treatment and offer R reads the same treatment
    Then the answer is 403 with MSG-P4-002
    Given a case outside the caller's scope is read
    Then the answer is 404 with MSG-P4-003
```

The twelve criteria are new under D-RCV-60 and test only the S2 deliverable of this key: the gate on the treatment row, the refusal of an unapproved or closed treatment, the one-hop set summary, the send availability with the legacy messages, the unavailable document service, the expected set read as data, the composite route, the personal-data and event boundary (ASM-4462) and the table boundary of section 12.7 (AC9 and AC10), the unavailable service read (AC11) and the error statuses of the provided operations (AC12). The thirteen legacy criteria AC1 to AC13 of RWB-E2-017 — Generate, Review, Send, Generate for a treatment that is not approved, A correction without a reason, A locked value cannot be corrected, Send with a draft not reviewed, A sent document cannot be changed, The decision record write fails on a correction, Send chosen twice, Two officers correct the same draft, The signature service refuses the request and The template changed after the drafts were made — belong to `RWB-P5-E2017-APP`, are written there word for word with their origin tags, and are not restated here. The paths, the request and answer shapes, the error set and the fakes of the actions this panel enables are `RWB-P5-E2017-CON`'s, and the cross-service journey of the same set across rwb-treatment, rwb-document, rwb-comms and rwb-case is the wave 2 integration harness's.

Two readings are stated here rather than left in the code. The section, its properties and the action vocabulary are Not specified in the source documents (GAP-2697), so they are taken as this story's design on the declared treatment read, kept provisional (GAP-2697; ASM-4463). The legacy files the whole capability in the document module and gives the treatment module no read of its own, while the target gives SCR-14's treatment leg to this service and the set to rwb-document, so the two services answer one screen through the route and neither duplicates the other's fact; this slice writes no decision record of this key (GAP-2698; ASM-4466).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only an approved, open treatment has its set generated: approved is a `decision_log_id` that resolves to a D6.4 local decision record, open is no outcome on a state that is not closed | Legacy RWB-E2-017 BR2; DF-TRT-003, DF-TRT-013; R-DIL-14, R-DIL-16 |
| BR2 | The panel reports the gate and never moves it: the treatment state, the outcome and the approval are changed by the approval and closing stories, and this story writes none of them | Legacy RWB-E2-017 section 9; DP-01 |
| BR3 | The set a treatment type requires is reference data read at its version, and an unknown type answers an empty expected set and never a default one | Legacy RWB-E2-017 BR1; DF-REF-046 to DF-REF-051; DL28; DP-07 |
| BR4 | The set summary is what the document service reports, read in one hop with a 2 s timeout and a breaker; this service holds no document, no template and no file | Legacy RWB-E2-017 section 12; DP-01, DP-11 |
| BR5 | A document is current when its template version is the version the owner reports in force; the panel compares and never recomputes a version | Legacy RWB-E2-017 BR6; CTL-14; R-UNI-38 |
| BR6 | Send is offered only when every document of the set is REVIEWED, every document is on the current template version and none is SENT; otherwise the panel names the document or the version | Legacy RWB-E2-017 BR6, BR7; AC7, AC13 |
| BR7 | The messages are the legacy ones: MSG-P5-011 on the gate, MSG-P5-013 on the set, MSG-GEN-006 on an unavailable owner, MSG-P4-002 and MSG-P4-003 on the guard; no message is re-worded here | Legacy RWB-E2-017 section 14 |
| BR8 | The screen actions are the document service's: this story answers a read, and the generate, regenerate, review and send operations of `RWB-P5-E2017-CON` are called by the browser through the route and write nothing here | GAP-2698; ASM-4466 |
| BR9 | An unavailable document service never fails the treatment read: the gate is still answered and only the set summary is marked unavailable | AC5; ASM-4463 |
| BR10 | This service reads no `document`, `document_type`, `signature_request`, `template`, `merge_field`, `recovery_case` or `decision_log_entry` row and no `v_ace_*` view; the `rwb_treatment` login holds no grant that would allow otherwise | DP-01; Architecture v5 slides 8 and 13; Ownership Map |
| BR11 | A new rule or template version applies from its effective date; a record keeps the version it was made under, so the panel compares a document with the version in force and never rewrites it | Business Rules and Routing Logic v4 (R-UNI-38) |
| BR12 | A repeated request with the same key returns the first result; the actions behind the panel keep this rule in P5 and this story holds no key of its own | Business Rules and Routing Logic v4 (R-UNI-40) |

The rules hold in the section as follows. BR1 is the gate builder: two columns and one reference resolution. BR2 is the reason the read issues no statement that changes a row. BR3 is `ExpectedSetReader` and the reason a type with no row is named rather than defaulted. BR4 is `DocumentSetClient` with its budget and breaker. BR5 and BR6 are the assembler's comparisons over the answer. BR7 is the message mapping. BR8 is the boundary with the five write operations of P5. BR9 is the partial answer of X5. BR10 is the schema grant and the boundary test.

### 9. State transitions

The case status is rwb-case's and the treatment state is the approval, plan and closing stories' (BR2): this story moves nothing. The two tables below are the states the panel reads and reports.

| Document state, as reported by rwb-document | What the panel answers | Condition |
|---|---|---|
| DRAFT | `canSend` false, MSG-P5-013 naming the document | At least one document of the set is not reviewed |
| REVIEWED | `canSend` true when every other document is REVIEWED and current | Every document REVIEWED and on the current template version |
| SENT | `canSend` false; the set is shown as sent and read only | At least one document SENT |
| Any state at an old template version | `canSend` false, MSG-P5-013 naming the document and the version in force | `templateVersion` is not the version in force |

| Treatment gate | What the panel answers | Condition |
|---|---|---|
| Approved and open | `canGenerate` true, `canSend` from the set | `decision_log_id` resolves to D6.4 and no outcome |
| Not approved | `canGenerate` false, MSG-P5-011 | No `decision_log_id`, or a reference that does not resolve to D6.4 |
| Closed | `canGenerate` false, MSG-P5-011 | An outcome is set, or the state is closed |

The document lifecycle itself belongs to `RWB-P5-E2017-APP` and the store of RWB-P5-E1024-APP: the panel reports DRAFT, REVIEWED and SENT and never sets one.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer (FCR) | Treatment and offer CRUA and Documents CRU in the TSD S2 T6.1 matrix: opens SCR-14, reads the gate and the set summary and starts the actions the panel enables |
| RW-CASEOWN, case owner | Treatment and offer CRU: the same in scope |
| RW-LEGAL, legal counsel | Reads the set and owns which fields are overridable and which templates are approved; this story serves the read only |
| RW-TEAMMGR, team manager | Reads the panel (Documents R) and edits nothing |
| RW-SPECIAL, RW-GUARANT, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-CREDCOMM, RW-PRODHEAD | Read the panel on cases in scope |
| The rwb-treatment service identity (login `rwb_treatment`, DP-02) | Serves the treatment read and its section, calls the set operation once and holds no grant on `rwb_document`, `rwb_comms`, `rwb_case`, `rwb_decision` or a `v_ace_*` view |
| rwb-document (P5) service identity | Owns the documents, the templates of record, the review and the send; answers the set read and is never written by this story |
| The gateway-bff (platform) | Merges the treatment read, the case read and the document reads for SCR-14; this story fixes the service side of the answer only |

No delegation of authority level applies: the treatment was approved at D6.4 before generation and this story requests no approval. No credential and no personal name appears in the section, the log lines or the tests; where a person must be identified the section carries a user identifier, never a name.

**Guard.** Every REST operation of this story is checked by the rwb-access authorise check (DP-08) before the section is built; the check's call name is Not specified in the source documents (DOR-RWB-S2-E2017-APP-6), and the treatment and scope rules of this section are its input.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment (S2, `rwb_treatment`) | id | Read: the treatment of the panel |
| DF-TRT-002 | treatment (S2, `rwb_treatment`) | case_id | Read: the case key of the set read |
| DF-TRT-003 | treatment (S2, `rwb_treatment`) | decision_log_id | Read: the approval reference the gate resolves against the local record |
| DF-TRT-004 | treatment (S2, `rwb_treatment`) | treatment_type | Read: selects the expected set and the reference row |
| DF-TRT-013 | treatment (S2, `rwb_treatment`) | outcome | Read: empty is open |
| Standard column | treatment (S2, `rwb_treatment`) | state, version, updated_at | Read: the state is the other half of the gate; none is written |
| DF-DEC-001 to DF-DEC-018 | decision_record (local, in `rwb_treatment`) | decision code, final call, subject reference | Read through the DP-03 library: the record of the D6.4 approval that DF-TRT-003 points at; nothing is written |
| No field ID | reference row (P3, `rwb_case`) | LOV-DOC-TYPE and the treatment-type set row | Read through the reference-data contract of DP-07 at its version: the document types and the template codes the set must carry; the field IDs are that contract's and are not restated here |
| DF-DOC-001 to DF-DOC-011 | document (P5, `rwb_document`) | id, document_type, state, doc_version, review_status, write_once | Not read as a table: the identifier, the type, the state, the version and the flags arrive in the set answer (BR4, BR10) |
| DF-REF-045 to DF-REF-051 | template (P6, `rwb_comms`) | all fields | Not read at all: the version in force is reported by the document service on its answer |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3, `rwb_case`) | the case and its product group | Not read: the case and the product group are merged by the composite route from the case read, and the product group reaches the panel as a route value |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (P7, `rwb_decision`) | the central ledger entry | Not written and not read: P7 seals it from the shared topic |

Field IDs are those of TSD S2 T3.1 and the Logical Data Model and Data Dictionary. **No table, no column and no index is added by this story:** it writes nothing, and the panel is an answer over this service's own row, the local record and the reference data. The document, template, case and ledger rows are named here to show what this story does **not** touch. No foreign key leaves `rwb_treatment` and no cross-schema join exists (DP-01).

**No personal data.** The set answer carries identifiers, codes, versions, states and dates; the merge values and the rendered bodies are the document service's and never pass through this service, so the section, the log lines and the tests carry none (AC8; ASM-4467).

**Open decisions.** DL10 and DL28 remain open. Each carries its assumptions (DL10: ASM-2250, ASM-2357, ASM-2377, ASM-2863; DL28: ASM-1861, ASM-1925, ASM-2093, ASM-2727). The directive of 26 November 2026 confirms every assumption, and this story builds on them as stated.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). This story provides no operation of its own: it adds one optional property to the answer of the declared read, and the addition is compatible inside major version 1.

| ID | Method | Path | This story | Access | Idempotency |
|---|---|---|---|---|---|
| API-S2-002 | GET | `/treatments/{treatmentId}` | Adds the optional `documentPanel` property to the `Treatment` answer: `treatmentApproved`, `treatmentOpen`, `treatmentType`, `productGroup`, `canGenerate`, `canSend`, `blockerMessageId`, `blockerDetail`, `expectedSet[]` (documentType, templateCode) and `documents[]` (documentId, documentType, templateCode, templateVersion, state, docVersion, writeOnce), with `setComplete` and `setAvailable`; the declared operation, its error set and its fakes are `RWB-S2-E3001-CON`'s | Treatment and offer R, scope applied, through the guard library | Not applicable |

The errors remain the declared ones: 401, 403 with MSG-P4-002, 404 with MSG-P4-003 and 503. The property is optional and its inner members are nullable, so a consumer that ignores it keeps working and a treatment with no set answers an empty document list with `setAvailable` true and `setComplete` false. The name and the members are Not specified in the source documents (GAP-2697; ASM-4463).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/document/v1/cases/{caseId}/generated-documents?treatmentId={treatmentId}` | P5 rwb-document (`RWB-P5-E2017-CON`); no API ID exists for it in TSD P5 T-A.1 | The set of the treatment: 200 `GeneratedDocumentSetPage` with the documents of the case filtered by `treatmentId`, each carrying `documentId`, `treatmentId`, `documentType`, `templateCode`, `templateVersion`, `state`, `writeOnce`, `docVersion` and `reviewStatus`; one hop, 2 s, a breaker, built against the contract and its fake (DP-11, ADR-020) |
| GET | the reference-data read of LOV-DOC-TYPE and the treatment-type set row, operation Not specified in the source documents (GAP-2697; ASM-4463) | P3 rwb-case (`RWB-P3-E1043-CON`) | The document types and the template codes a treatment type requires, at their version, cached; an unknown type answers an empty set and no default is applied (DP-07) |

One operation is consumed at run time and one as a list and a set row; both are one hop with a 2 s timeout and a breaker, and neither calls another service. A failed set read never fails the treatment read (BR9); a failed list read answers the panel with an empty expected set and the type named, and writes nothing.

#### 12.3 Events published

None. This story is a read: it writes no outbox row, holds no idempotency key and creates no message. The service's topic `rwb.treatment.events.v1` and its event names `rwb.treatment.<Event>.v1` are unchanged and carry nothing from this key; DP-09 is not in the pattern set of this story (ASM-4467).

#### 12.4 Events consumed

None. The panel is read on request, in the request of the officer: no case signal, no rule package and no deviation event changes it, and the service holds no consumer group for this capability. The inbox table of the platform library exists in `rwb_treatment` for the consumers the sibling stories add.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` | Workflow, the stage child of `CaseWorkflow`, one execution per case and stage | `rwb-treatment` | Named here only and not changed: the panel is not a step of the stage and starts no workflow. Workflow ID form: Not specified in the source documents (CG-ALL-8350). Start rule and duplicate-start policy: Not specified in the source documents (CG-ALL-8350) |

No activity, no child workflow and no timer of this story is registered; the set read is a synchronous read inside the API request with a 2 s budget, and it is not an activity because it changes nothing and needs no retry of its own (ASM-4463).

#### 12.6 Schedules

None. No job map row belongs to this capability, no cron entry, no Temporal Schedule and no event-started workflow is created or moved, and DP-10 is not in this story's pattern set.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Read only: the six fields of section 11 and the standard state column; no column is added and no row is written |
| `decision_record` | `rwb_treatment` | PLT library object applied in this schema | Read through the library by the reference DF-TRT-003; nothing is written |
| `v_ace_*` views | `recovery` | P1, read-only views | Not used by this story: no ACE value is needed by the panel |

Not owned and never read as a table: `document`, `document_type`, `signature_request`, `document_hub_parameter`, `document_field` and `retention_rule` (P5, `rwb_document`), `template`, `merge_field` and `notice` (P6, `rwb_comms`), `recovery_case`, `parameter_catalog`, `reference_row` and `lov_value` (P3, `rwb_case`), `decision_log_entry` (P7, `rwb_decision`). No foreign key leaves the schema and no cross-schema join exists (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-document set fake (`RWB-P5-E2017-CON`) | For treatment "TRT-0501": one document each of type CONTRACT at "DIL-CONTRACT" version 2, CREDIT_APPROVAL at "DIL-CA" version 1 and MORTGAGE_DOCUMENT at "DIL-MORTGAGE" version 1; the same set with "DIL-MORTGAGE" in DRAFT; the same set with "DIL-CONTRACT" at version 2 while version 3 is in force; a set missing a type; a 503 with MSG-GEN-006 naming "Document service"; no answer beyond 2 s | AC3, AC4, AC5, AC6, AC8 |
| rwb-case reference-data fake (`RWB-P3-E1043-CON`) | LOV-DOC-TYPE with CONTRACT, CREDIT_APPROVAL and MORTGAGE_DOCUMENT at its version; the DEED_IN_LIEU set row with "DIL-CONTRACT", "DIL-CA" and "DIL-MORTGAGE"; the RESTRUCTURE row with "RES-AGREEMENT"; an unknown type with no row; a delayed answer beyond 2 s | AC1, AC6 |
| treatment fixture of this service | Approved and open "TRT-0501"; "TRT-0502" with no decision_log_id; "TRT-0503" with outcome CANCELED; a treatment whose reference resolves to a record that is not D6.4 | AC1, AC2 |
| gateway-bff composite route fake (`RWB-PLT-N001-CON`) | The merged SCR-14 answer for case "RW-2026-000501" with the treatment read, the case read and the document read once; a route answer for a caller without the right | AC7 |
| guard and scope doubles | A 403 with MSG-P4-002 and a 404 with MSG-P4-003 | AC7 |

The fakes are test-only and are replaced by the real services in SIT; a drift between a fake and the published contract is a build failure of the contract story that owns the fake.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided (additive), 2 consumed | `GET /treatments/{treatmentId}` on `/api/recovery/treatment/v1` with the added property; the set operation of `RWB-P5-E2017-CON` on `/api/recovery/document/v1` and the reference-data read of rwb-case; one hop and 2 s on each consumed call |
| Kafka | 0 published, 0 consumed | The topic `rwb.treatment.events.v1` carries nothing from this key and no consumer group is registered |
| Temporal | 0 | No workflow, activity, timer or Schedule is started, registered or moved |
| File | None | No file is read, built or delivered: the document body and the write-once copy are rwb-document's and rwb-comms' |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, module `panel`, Java package `th.co.scb.ace.workbench.recovery.treatment.panel`. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-11 is the change of this slice: the monolith read the document and treatment rows in one schema, and here the set arrives on one hop with a published shape, a fake and a 2 s timeout, so the panel builds on Day 1 without a document table. DP-01 keeps the gate inside `rwb_treatment` and makes the document, template, case and ledger rows unreachable. DP-03 is applied as a read: the approval fact is the reference to the local record the approval story wrote, through the same library; this story writes no record of its own, because every record of the actions it enables belongs to P5 (ASM-4464). DP-07 is the set row and the type list, so no type and no template code is a constant. DP-13 moves the base of the read the screen uses. DP-19 is how SCR-14 reaches the section.

**Dependencies the table adds and the plan does not hold.** The table adds four H rows — `RWB-PLT-E1027-CON` for DP-03, `RWB-PLT-E1043-CON` for DP-07, `RWB-PLT-N001-CON` for DP-19 — and one C row, `RWB-P3-E1043-CON`, while the plan's lists for this story hold Depends on (build) `None` and Contract dependencies `RWB-P5-E2017-CON` only. The metadata keeps the plan's lists, and the story builds against the platform fakes and the reference-data fake until those contracts publish (ASM-4465, ASM-4468).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `TreatmentPanelService` | Service | Reads the treatment row, resolves the approval reference against the local record and answers the gate (BR1, BR2) |
| `ExpectedSetReader` | Service | Reads LOV-DOC-TYPE and the treatment-type set row at their version and holds the expected document types and template codes (BR3, DP-07) |
| `DocumentSetClient` | Client | The set read on `RWB-P5-E2017-CON`, one hop, 2 s, a breaker, no retry chain, with the problem body carried back unchanged (DP-11) |
| `SetCompleteness` | Service | Compares the expected set with the answer: every type once, the template version against the version in force (BR4 to BR6) |
| `DocumentPanelAssembler` | Service | Builds the section, `canGenerate`, `canSend` and the blocker with its message ID and detail (BR6, BR7, BR9) |
| `TreatmentPanelResource` | Read resource | Serves the optional property on the declared treatment read, additive and nullable (12.1) |
| `BoundaryGuard` | Build check | Fails the build on a statement outside `rwb_treatment`, a read of a foreign schema, a `v_ace_*` view or an event publisher in the module (BR10) |

**Database.** No table, no column and no index: the panel is an answer over the six `treatment` fields of section 11, the local `decision_record` and the reference-data answer. No migration is added, no existing migration is edited, and DP-15 is not in this story's patterns (ASM-4463).

**Configuration and reference data.**

- LOV-DOC-TYPE and the treatment-type set row are read through the reference-data contract and client library of rwb-case at their version (DP-07); no document type and no template code is written in code (BR3).
- The capability area "Treatment and offer", the right R and the scope filter are rwb-access rows read through the guard (ASM-4468).
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020 and not a value of this story.
- The feature switch `rwb.treatment.document-panel`, read as a flag of the platform library: off means the read answers without the property, the screen shows no panel and no set read is made.

**Build steps**

1. `TreatmentPanelService` with the gate over the row and the local record, and the two refusal cases of AC2.
2. `ExpectedSetReader` over the reference-data fake, with the unknown type and the delayed answer (AC6).
3. `DocumentSetClient` against the set fake, with the 2 s budget, the breaker, the 503 with MSG-GEN-006 and the no-answer path (AC3, AC5).
4. `SetCompleteness` and `DocumentPanelAssembler`, with the send availability of AC4 and the blockers of X3, X4 and X6.
5. `TreatmentPanelResource` on the declared read, additive and nullable, with a treatment that has no set (AC1).
6. The route fake and the SCR-14 answer, with the guard and scope cases of AC7.
7. The boundary test and the property test of AC8: no foreign table, no `v_ace_*` view, no event publisher, no personal value in the section or the logs.

**Feature flag.** `rwb.treatment.document-panel`.

**Done when.** The tests of section 16 pass, a SIT week shows the panel answering the gate from the treatment row, the set from the document service in one hop, the two buttons disabled with the legacy messages where a document is DRAFT or on an old version, an unavailable document service leaving the treatment read intact, SCR-14 showing the panel through the composite route, and no personal value and no event appearing anywhere in the module.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-011 | The treatment is not approved or not open (X1, X2; AC2) | Documents can be generated only for an approved {treatment} that is still open. |
| MSG-P5-013 | A document of the set is not reviewed, or is on an old template version (X3, X4, X6; AC4, AC6) | {document} cannot be sent yet: {reason}. |
| MSG-GEN-006 | The document service did not answer, or the reference-data read failed (X5; AC5) | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | The caller holds no Treatment and offer R (X7; AC7) | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case or the treatment lies outside the caller's scope (X7; AC7) | This case is not in your scope. |

The five identifiers and the wording are copied unchanged from legacy RWB-E2-017 section 14 and this story re-words none of them; the messages of the actions it enables — MSG-P5-012, MSG-P5-014, MSG-P5-002, MSG-GEN-001, MSG-GEN-004 and MSG-P7-003 — stay with `RWB-P5-E2017-APP` and are raised there. Thai text for each message follows decision DL10. Delivery shape: the two guards answer an RFC 9457 problem response, and the two panel messages are answered inside the 200 as `blockerMessageId` with `blockerDetail` carrying the text with its placeholders filled; for MSG-GEN-006 the {system} value is "Document service" on the set read and "Reference data" on the list read, and for MSG-P4-002 the {action} value names what the caller tried and never a case fact or a document identifier.

### 15. Screens and states

No screen is built in this story. SCR-14 Treatment record is the treatment screen and its treatment leg is this service's; SCR-30 Case documents, the review view and the correction form are `RWB-P5-E2017-APP`'s and P5's.

| Screen | State | What the user sees |
|---|---|---|
| SCR-14 Treatment record | Approved | The terms, the expected set with the template codes, the three documents with their type, template version and state, Generate documents and Send for signature both enabled |
| SCR-14 Treatment record | Approved, one document DRAFT | Send disabled with MSG-P5-013 naming the document; Generate enabled |
| SCR-14 Treatment record | Approved, one document on an old version | Send disabled with MSG-P5-013 naming the document and the version in force |
| SCR-14 Treatment record | Draft, submitted, closed | Generate disabled with MSG-P5-011 and Send disabled |
| SCR-14 Treatment record | Document service unavailable | The treatment and the gate as this service reports them, and the set summary marked unavailable with MSG-GEN-006 |
| SCR-14 Treatment record | Set sent | The documents shown as SENT and read only, with no edit control |
| SCR-14 Treatment record | Caller without the right or out of scope | MSG-P4-002 or MSG-P4-003 from the declared read |
| SCR-14 Treatment record | Empty | Not specified in the source documents (CG-ALL-8356) |
| SCR-14 Treatment record | Loading | Not specified in the source documents (CG-ALL-8356) |
| SCR-14 Treatment record | Error | MSG-GEN-006 with the gate still shown (X5) |
| SCR-14 Treatment record | No access | The refusal of X7 (the row above) |

The route path, the screen field list, the merge order and the layout belong to `RWB-PLT-N001-CON` and the edge stories (ASM-4466); this story fixes the service side of the answer only.

SCR-30 Case documents is RWB-P5-E2017-APP's: its Loading state is the one Screen Specifications v1 gives; its Empty, Error and No access states are Not specified in the source documents (CG-ALL-8357).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-017-14 | Access (legacy RWB-E2-017 Access) | Component | RW-TEAMMGR user (Documents R) calls POST generated-documents/send; refused with MSG-P4-002 |
| TC-E2-017-01 | AC1, BR1, BR2 (legacy AC1) | End to end | Synthetic mortgage DIL treatment, three approved templates |
| TC-E2-017-02 | AC2, BR3, BR4, BR5 (legacy AC2) | End to end | Contract date moved by two days |
| TC-E2-017-03 | AC3, BR6, BR7, BR8 (legacy AC3) | End to end | Three reviewed drafts; P6 stub returns ACCEPTED |
| TC-E2-017-04 | AC4, BR2 (legacy AC4) | End to end | Treatment with no decision_log_id |
| TC-E2-017-05 | AC5, BR3 (legacy AC5) | End to end | Empty reason |
| TC-E2-017-06 | AC6, BR3 (legacy AC6) | End to end | Locked transfer price |
| TC-E2-017-07 | AC7, BR6 (legacy AC7) | End to end | One draft not reviewed |
| TC-E2-017-08 | AC8, BR7 (legacy AC8) | End to end | Document in state SENT |
| TC-E2-017-09 | AC9, BR4 (legacy AC9); run by RWB-P5-E2017-APP | End to end | Decision record stub refusing writes on a correction |
| TC-E2-017-10 | AC10, BR10 (legacy AC10); run by RWB-P5-E2017-APP | End to end | Same send key twice |
| TC-E2-017-11 | AC11 (legacy AC11); run by RWB-P5-E2017-APP | End to end | Two sessions on one draft |
| TC-E2-017-12 | AC12 (legacy AC12); run by RWB-P5-E2017-APP | End to end | P6 stub returns UNAVAILABLE, then ACCEPTED |
| TC-E2-017-13 | AC13, BR6 (legacy AC13); run by RWB-P5-E2017-APP | End to end | Template version 3 made current after the drafts |
| TC-E2-017-15 | Principle 5 (legacy RWB-E2-017 TC-E2-017-15) | NFR | Decision record write forced to fail on send; nothing sent, documents stay REVIEWED, MSG-P7-003, incident raised |
| TC-S2-E2017-APP-01 | AC1, AC2 | Component | Approved open "TRT-0501"; "TRT-0502" with no decision_log_id; "TRT-0503" with outcome CANCELED; gate and blocker ids |
| TC-S2-E2017-APP-02 | AC3, AC4, AC6 | Contract | Set fake with three documents at versions 2, 1 and 1; one DRAFT; version 3 in force; a set missing the mortgage document |
| TC-S2-E2017-APP-03 | AC5, BR9 | Component | Set fake answering 503 with MSG-GEN-006 and no answer inside 2 s; the gate still answered |
| TC-S2-E2017-APP-04 | AC7, AC8 | Component | SCR-14 through the route fake; the section, the log lines and the topic carry no personal value and no event |
| TC-S2-E2017-APP-05 | AC9, BR10 | Component | Boundary test: the rwb_treatment login and the panel issue no statement on a table of section 12.7 other than treatment and decision_record, and no v_ace_* view; any other statement fails the build |
| TC-S2-E2017-APP-06 | AC10, BR10 (X8) | Component | Not specified in the source documents (NEWAC-RWB-S2-E2017-APP-AC14) |
| TC-S2-E2017-APP-07 | AC11, BR9 | Component | Not specified in the source documents (NEWAC-RWB-S2-E2017-APP-AC15) |
| TC-S2-E2017-APP-08 | AC12 | Component | Not specified in the source documents (NEWAC-RWB-S2-E2017-APP-AC16) |

The fifteen legacy test case IDs are kept in the order the work package lists, with their legacy Covers and Data character for character, except the decision-log wording replaced by decision record (CG-ALL-8355); the legacy level "System" maps to End to end, "Access" to Component and "Resilience" to NFR, and each Covers cell keeps the legacy AC number that owns it in brackets because that behaviour is proved in `RWB-P5-E2017-APP`. The legacy rows are references only: RWB-P5-E2017-APP owns and runs them, and this story runs none of them. The eight added cases are this story's and test only the S2 deliverable; the fakes of section 12.8 stand behind every case. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 2 integration harness and are not listed here.

### 17. Guardrails

- No value that a business person may change is written in code: the document types, the template codes, the treatment types and the messages are values in force read at their version (BR3, BR7; DP-07).
- No personal data in the section, the log lines, the tests, the workflow inputs or a prompt: the section carries case and treatment identifiers, document identifiers, type codes, template codes, versions, states, counts and dates only (AC8; ASM-4467).
- No read of another module's tables: the set and the templates arrive on the published operations, and `rwb_treatment` holds no foreign key into another schema (DP-01, BR10).
- ACE data only through the owner's contract or the `v_ace_*` views: this story needs no ACE value and reads neither form.
- No document body, file byte, merge value or signature is touched here: this story carries identifiers, codes, versions, states and counts and no byte (BR4).
- This story writes nothing: no `treatment` column, no decision record, no outbox row and no idempotency row is inserted, updated or deleted by it, and a write in the module fails the review (BR2, BR8).
- No event is published and no consumer group is registered: the topic carries nothing from this key (ASM-4467).
- The section is additive and optional at major version 1 and every inner member is nullable, so no consumer of the treatment read is broken by it (12.1).
- An unavailable document service never fails the treatment read and never shows an empty set as a complete one (BR9, AC5).
- No right is re-implemented: the capability area and the right are declared and the guard library answers, and no screen calls a service directly (DP-19).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-012 | Contracts, credit applications and mortgage documents generated from approved templates with no re-keying | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence | R-DIL-14, R-DIL-16, R-UNI-38, R-UNI-40 | TC-E2-017-01 to TC-E2-017-15, TC-S2-E2017-APP-01 to TC-S2-E2017-APP-08 |
| REQ-OCC-002 | Templates versioned with the Legal approval recorded against the version | Business Requirements Program, section 5.6; Epic 2, section 3.5 | FEAT-OCC-07 | 13 Manage documents and correspondence | R-UNI-38 | TC-E2-017-01, TC-E2-017-13, TC-S2-E2017-APP-02 |
| REQ-OCC-009 | The signature path is chosen by product and Legal rule | Business Requirements Program, section 5.6; Epic 2, section 3.5 | FEAT-OCC-07 | 13 Manage documents and correspondence | R-DIL-18, R-RES-16 | TC-E2-017-03, TC-E2-017-12, TC-S2-E2017-APP-02 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P5-E2017-CON | Contract | C: declares the set read, the regenerate and send operations, the shapes, the error set, the `Idempotency-Key` rule and the fakes this story builds against |
| RWB-P5-E2017-APP | App development | The primary slice of the legacy key: the screens, the overrides, the review, the send and the thirteen legacy criteria |
| RWB-S2-E3001-APP, RWB-S2-E3001-CON | App development, Contract | Sibling: the treatment row and the treatment read whose answer carries the added property |
| RWB-S2-E3002-APP to RWB-S2-E3005-APP | App development | Siblings: the offer, the approval below the floor, the plan and the affordability pre-assessment the treatment carries |
| RWB-S2-E2026-APP | App development | Sibling: the generation activity of the same key that produces the documents this panel reports |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library whose record of the approval the gate resolves (DP-03) |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | Contract | H and C: the reference-data client library and the list and set rows (DP-07) |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route that serves SCR-14 (DP-19) |
| P5 rwb-document, P6 rwb-comms | Service, wave 1 | Own the documents, the templates, the merge fields and the Legal approval of a version |
| rwb-case (P3), rwb-decision (P7), rwb-access (P4) | Service, wave 1 | Own the case and its status, the rule packages and the central ledger, and the rights and scope data |
| Wave 2 integration harness | Integration | The cross-service proof of the same set across the four owners, with the `-ITG` copies of the legacy cases |

### 19. Out of scope

- The screens, the generation panel, the review view, the correction form, the regenerate operation and the send: `RWB-P5-E2017-APP` and `RWB-P5-E2017-CON`.
- The generation engine, the template selection, the merge-field resolution, the rendering, the PDF/A-2b body and the draft files: `RWB-P5-E2026-APP`, `RWB-P5-E2026-CON` and `RWB-S2-E2026-APP`.
- The templates, the merge-field definitions, the template versions and the Legal approval of a version: P6 rwb-comms and P5 rwb-document.
- The write-once copy, the file custody, the retention and the e-signature: `RWB-P5-E2018-APP`, `RWB-PLT-TE012-APP` and P5.
- The treatment record, the treatment terms, the offer, the plan and the approval below the floor: `RWB-S2-E3001-APP` to `RWB-S2-E3005-APP`.
- The approval decision itself, the state it moves and the closing of the treatment: the approval and closing stories of this epic and P7 rwb-decision.
- The case, its status, its tasks and the parent `CaseWorkflow`: rwb-case (P3); this story reads no case table.
- The rule packages and the central decision ledger: P7 rwb-decision.
- The rights, the roles and the scope data, and the guard library that answers them: rwb-access (P4) and the platform library stories.
- The gateway-bff composite route, the screen field list and the layout of SCR-14: `RWB-PLT-N001-CON` and the screen owners.
- The real cross-service proof of the same set against the live owners: the wave 2 integration harness.
- The deployment of this build: chart values, the topic and route provisioning, the flag, dashboards and the runbook.

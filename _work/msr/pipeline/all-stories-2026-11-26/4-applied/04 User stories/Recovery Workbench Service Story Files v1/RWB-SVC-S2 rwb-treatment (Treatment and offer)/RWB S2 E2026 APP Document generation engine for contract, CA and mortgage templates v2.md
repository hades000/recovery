# RWB-S2-E2026-APP Document generation engine for contract, CA and mortgage templates

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: secondary slice of legacy RWB-E2-026 for rwb-treatment (S2). The generation engine itself moves to rwb-document (P5) and keeps the legacy acceptance criteria; this story delivers only the treatment side — the `generateContractDocument` activity of `TreatmentWorkflow` asks the generation operation of RWB-P5-E2026-CON for the three template codes, pins the template version in force, stores the returned document reference and the pinned version on its own `treatment` row in the same `rwb_treatment` transaction as its local decision record through the RWB-PLT-E1027-CON library (DP-03), and writes the outbox row in that transaction (DP-09); the base becomes `/api/recovery/treatment/v1` (DP-13) and SCR-14 and SCR-15 are reached through the gateway-bff composite route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S2-E2026-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E2026-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-026 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP15, DP19 |
| Parallel lane | L-S2-I |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E2026-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to REQ-DCM-012, REQ-OCC-002) |
| Status | Draft (realignment v1) |

### 1. Story

As a **restructuring officer (FCR)**, I want **the treatment stage of the case to ask the generation engine of the document service for the contract, credit approval and mortgage documents of the treatment it is working, to pin the template version that was in force on the request date, and to keep the returned document reference and that version on the treatment row in the same transaction as the decision record that says which template and which version produced it**, so that **the documents the screens show are the ones produced from the Legal-approved version, and the treatment itself carries the proof of which version it was given**.

This is the treatment-side slice of legacy RWB-E2-026. The generation engine of the legacy — the template selector, the merge-field resolver, the value formatter, the renderer, the file and the store — is RWB-P5-E2026-APP's and P5 rwb-document's, or P6 rwb-comms' for the catalogue. This story owns:

- the request and the use of the generated document: `generateContractDocument`, the activity of `TreatmentWorkflow` on queue `rwb-treatment` in namespace `rwb-recovery`, the stage child of `CaseWorkflow` of rwb-case (DP-12; Architecture v5 slide 18; Temporal and Drools Design slides 13 and 18);
- the one-hop REST call to the generation operation that RWB-P5-E2026-CON publishes, with a 2 s timeout, a breaker and a mock, built on Day 1 against the contract and never against rwb-document (DP-11, ADR-020);
- the two `treatment` columns it writes — the reference of the contract document the engine returned and the template version it pinned — added by this story's own Flyway version on the per-service sequence, with their index (DP-15);
- the local decision record of the generation, written through the RWB-PLT-E1027-CON library inside the caller's transaction with decision code D6.4, the template code and the template version (DP-03), and the outbox row of the same transaction (DP-09);
- the parameters read and the reference-data read the request is checked against, at their version (DP-06, DP-07);
- the treatment side of the base `/api/recovery/treatment/v1` (DP-13) and the read that surfaces the reference on SCR-14 and SCR-15 through the gateway-bff composite route (DP-19);
- the event the generation writes, which carries identifiers, codes and versions and no personal value (DP-09).

It does not own: the templates, the merge-field definitions, the template versions and the Legal approval of a version, which are P6 rwb-comms' (`template`, `merge_field`); the generation engine, the rendering, the PDF/A-2b body, the file custody, the e-signature and the retention, which are P5 rwb-document's and P6 rwb-comms' (`document`, `document_type`, `document_hub_parameter`, `signature_request`, `retention_rule`) and the stories RWB-P5-E2026-APP and RWB-P5-E2026-CON; the offer, the settlement terms and the approval below the floor, which are RWB-S2-E3001-APP to RWB-S2-E3005-APP; the case status and the `CaseWorkflow`, which are rwb-case's (P3); the central decision ledger, which is P7 rwb-decision's; the rights, the roles and the scope data, which are rwb-access's (P4); the gateway-bff composite route and the screen field list, which are the platform edge story's and the screen owners'.

### 2. Business rationale

Deed in lieu and restructure document sets are typed today from the case file into Word templates, and a wrong amount or an old template wording reaches the customer. The legacy engine fills each Legal-approved template version from the case facts held in the Workbench, refuses to produce a document with a missing value or an unapproved template, and records which template version and which inputs produced each document. That business objective is unchanged and is now split across two services: the engine and the files live in rwb-document (P5), the template catalogue in rwb-comms (P6), and the treatment that the documents belong to stays here.

What D-RCV-60 changes on this side is small in code and large in guarantees. In the monolith the generation was an in-process call from the treatment module into the document module: `DocumentGenerator.generate(...)` ran inside one JVM, wrote `document` rows and a `decision_log_entry` in the one `recovery` schema, and returned. In the target the call is one hop over the published contract of the document service (DP-11), the documents are rows of `rwb_document` that this service never reads, and the only durable trace on the treatment is the reference the engine returned plus the version it pinned. That trace has to be written with the decision record of the same action, in one transaction, because a treatment that carries a document reference no record explains is exactly what REQ-DCM-012 and the no-record rule forbid (DP-03; Temporal and Drools Design slide 14; R-UNI-39).

The second change is where the version rule bites. The legacy read the current version by language, product group and request date inside the engine. Here the version is read by the owner of the catalogue and reported on the answer, and this service pins the reported version on its own row: a new template version applies from its valid-from date and earlier documents keep their version (R-UNI-38). Pinning it here is what lets SCR-14 show, months later, which wording the customer was given, without this service reading a template row.

The third change is the boundary. The legacy story read `template`, `document`, `case` and the ACE views within one module. In the target this service writes two columns of its own `treatment` row and calls one operation; it holds no grant on `rwb_document`, `rwb_comms`, `rwb_case` or a `v_ace_*` view (DP-01, DP-05). The merge values it supplies are the ones its own row holds; the customer name and the title-doc number never pass through it (DP-05, CTL-11).

Serves REQ-DCM-012 and REQ-OCC-002. No business value is invented or moved: the template codes, the document types, the type mapping, the decision code D6.4, the amounts, the dates and the message IDs are the values the legacy story, the FSD S2 A2.18 and the TSD S2 already carry, read in force.

### 3. Preconditions

- RWB-P5-E2026-CON is published: the generate operation on `/api/recovery/document/v1`, `POST /cases/{caseId}/generated-documents` (API-P5-016) with `GenerateRequest` (treatmentId, templateCodes, language, overrides), the 201 `GenerationResult` (`decisionLogEntryId`, `documents`), the `Document` shape with `documentId`, `documentType`, `source`, `docVersion`, `templateCode`, `templateVersion` and `treatmentId`, the error set with the RFC 9457 problem body and its message IDs, the `Idempotency-Key` rule and the fakes. The operation identifier the contract does not state is Not specified in the source documents (GAP-1878; ASM-3080).
- RWB-PLT-E1027-CON is published: `DecisionRecordWriter.record(DecisionRecord)` with `@Transactional(propagation = MANDATORY)`, refusing with MSG-P7-009 and failing with MSG-P7-003, and the `decision_record` DDL template applied in this service's own schema (DP-03).
- `treatment` exists in `rwb_treatment` from RWB-S2-E3001-APP with the fields DF-TRT-001 to DF-TRT-033 of TSD S2 T3.1, holding treatment "TRT-0301" of type DEED_IN_LIEU or RESTRUCTURE with `decision_log_id` set and no outcome.
- Templates "DIL-CONTRACT", "DIL-CA" and "DIL-MORTGAGE" for a restructure and "RES-AGREEMENT" are loaded in Thai with the Legal approval recorded against the version, and the type mapping is DIL-CONTRACT to CONTRACT, DIL-CA to CREDIT_APPROVAL, DIL-MORTGAGE to MORTGAGE_DOCUMENT and RES-AGREEMENT to CONTRACT. The codes, the mapping and the approval are values in force read at their version; the catalogue and the mapping are P6 rwb-comms' and P5 rwb-document's and this story reads neither table (GAP-1879; ASM-3082).
- Package DEEDINLIEU or RESTRUCTURE is in force for the business date with the row R-DIL-16 (generate the credit approval, the contract and the mortgage documents, when `final_call = approved`), arriving from rwb-decision on `RulePackageInForce` and evaluated by the embedded Drools runtime of the service template, which adds no build dependency of its own (ASM-3082; Temporal and Drools Design slides 13 and 15; FSD S2 A2.18).
- The two columns and the index of section 13 are applied on this service's Flyway sequence by this story, after the version that carries the library tables, and no applied migration is edited (DP-15).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-14 Treatment record and SCR-15 Settlement offer from the case read, the treatment read and the document read, one hop each, read only (DP-19).
- The parameters contract and the reference-data contract of rwb-case are reachable as client libraries (DP-06, DP-07), and the capability area "Treatment and offer" with its rights is rwb-access data.
- No approval is needed to build against a Draft contract baseline, and a CON story is Day 1 by rule: this story starts on Day 1 with only CON build dependencies (§R5.7).

### 4. Flow

1. The case reaches D6.4 with an approved route, or the deed in lieu route reaches TRANSFER_PRICE_SET; `TreatmentWorkflow` on queue `rwb-treatment`, the child of `CaseWorkflow` of rwb-case, is running for the case (Architecture v5 slide 18; Temporal and Drools Design slides 13 and 18).
2. The stage asks the embedded Drools runtime for the package version in force and evaluates it with the treatment facts it holds: the treatment type, the approval, `final_call` and the transfer price against the floor.
3. R-DIL-16 fires with `final_call = approved`: its action is to generate the credit approval, the contract and the mortgage documents and to put the offer to the customer; its target state is OFFER_WITH_CUSTOMER_DIL, reported to the parent and moved there, not here (FSD S2 A2.18; ASM-3082).
4. `generateContractDocument` activity: reads the `treatment` row it owns and builds the `GenerateRequest` of the contract — `treatmentId`, the template codes of the set, `language` TH — and the S2 value set the contract's treatment provider answers for that treatment.
5. The S2 value set is exactly what the row holds: the contract amount from `offer_amount` (DF-TRT-007), the installments (DF-TRT-009), the interest rate (DF-TRT-027), the first due date (DF-TRT-029), and the case and decision-record identifiers (DF-TRT-002, DF-TRT-003). Names, the national ID number and the title-doc number are never supplied by this service; they belong to rwb-source-data and rwb-case and are masked by policy (DP-05, CTL-11).
6. The request is checked against the template-count bound read through the parameters contract at its version, and the template codes against LOV-DOC-TYPE read through the reference-data contract at its version; a code outside the list or a count above the bound is refused before the call (DP-06, DP-07).
7. The activity calls the generate operation of RWB-P5-E2026-CON once, on one hop, with a 2 s timeout and a breaker. The engine reads the template version in force by language, product group and request date, checks that every required merge field has a value, renders and stores the drafts, and answers 201 with the `documentId`, the `templateCode` and the `templateVersion` of each document (DP-11; FSD S2 A2.18; R-UNI-38).
8. The activity takes the document of type CONTRACT from the answer — the document of record of the treatment — and its `templateVersion`, and writes, in one `rwb_treatment` transaction: the two columns of the treatment row, the local `decision_record` through `DecisionRecordWriter.record` with decision code D6.4, the template code and the template version, the outbox row of the generation event, and the idempotency row of the request (DP-03, DP-09).
9. The write key is the treatment ID, the template code and the template version, so a replay of the same activity, a redelivery of the same request and a repeated `Idempotency-Key` all answer the first reference and write once (R-UNI-40; legacy AC8).
10. The stage reports the outcome to the parent `CaseWorkflow`: the document reference, the template version, the decision record and the target state the rule names. The parent moves the case; this service writes no case table.
11. A refused or failed generation writes nothing: the treatment keeps every column it had, no decision record and no outbox row is written, and the activity retries on the platform policy or fails non-retryably as the contract's status says.
12. SCR-14 shows the treatment with its document reference and template version, read from this service and merged with the document read of rwb-document by the gateway-bff composite route; SCR-15 shows the treatment the offer is built on (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A required merge field has no value on the case | The engine refuses before storing anything and names the template and the field; the activity carries the problem body back unchanged; no reference, no version and no record is written | MSG-P5-009 | AC2 |
| X2 | The version in force is not approved by Legal, or no template exists for the product group or language | The engine refuses and names the template; the treatment row is unchanged; the stage reports the refusal to the parent | MSG-P5-010 | AC2, AC6 |
| X3 | The template is withdrawn and no later version is approved | The engine refuses and names the template; the task to the officer who requested it is raised by the screens story, not here | MSG-P6-003 | AC6 |
| X4 | The treatment is not approved, is closed, or is of another type | 409 with the problem body; nothing is stored | MSG-P5-011 | AC6 |
| X5 | The local decision record cannot be written | The whole transaction rolls back: no reference, no template version, no outbox row; the user sees MSG-P7-003 and the activity retries | MSG-P7-003 | AC5 |
| X6 | The same request is repeated with the same key, or the activity is replayed | The first answer is returned; nothing new is written | None | AC4 |
| X7 | The same treatment and template are requested twice at once | One transaction commits; the other is refused by the engine with 409 and this service writes nothing | MSG-GEN-004 | AC4 |
| X8 | A template body cannot be rendered, or the document service does not answer inside 2 s | 503 with the problem body naming the system; nothing is stored here and the activity retries on the platform policy | MSG-GEN-006 | AC6 |
| X9 | The caller holds no Documents C, or the case lies outside the caller's scope | 403 or 404 with the problem body; nothing is read further and nothing is written | MSG-P4-002, MSG-P4-003 | AC6, AC8 |
| X10 | A component, a statement or a test reaches a `rwb_document`, `rwb_comms` or `rwb_case` table, a template row or a `v_ace_*` view | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 8, BR1 |

X1 to X6 are the legacy paths of the generation carried onto the split; X7 and X8 add the concurrent and the unavailable cases of the one-hop call; X9 is the guard's answer; X10 is the boundary rule of the target. Nothing is written on any of X1 to X4 or X8 to X10, because the engine's refusal arrives before this service's transaction opens, and X5 rolls back the transaction that already holds the reference and the record.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against the RWB-P5-E2026-CON fake, the decision-record writer fake, the parameters and reference-data fakes and the composite-route fake; needs no live rwb-document, rwb-comms, rwb-decision or rwb-case |
| Negotiable | The activity name, the column names, the write key and the value-set shape are this story's design; the template codes, the document types, the decision code, the message IDs and the version rule are values in force |
| Valuable | The officer stops re-keying the contract set and the treatment carries the version it was given, so the wording behind a signed document can be shown months later |
| Estimable | One activity, one client, one value builder, one writer, two columns and one index, one event and one read model |
| Small | Fits two weeks with its tests, as a secondary slice of the legacy key |
| Testable | Each of the eight criteria of section 7 is one automated test; every cross-service answer is stubbed in a contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Document generation engine for contract, CA and mortgage templates — the rwb-treatment request and use

  Background:
    Given case "RW-2026-000301" with product group "MORTGAGE"
    Given treatment "TRT-0301" of type "DEED_IN_LIEU" on that case with decision_log_id set and no outcome
    Given template "DIL-CONTRACT" version 2 in Thai for "MORTGAGE" with approved_by_legal true
    Given the merge fields of "DIL-CONTRACT" version 2 are case_no, borrower_name, title_doc_no, transfer_price and contract_date
    Given the template-to-document-type mapping is DIL-CONTRACT to CONTRACT, DIL-CA to CREDIT_APPROVAL and DIL-MORTGAGE to MORTGAGE_DOCUMENT
    Given a restructuring officer with role RW-RESTRUCT in scope of the case

  Scenario: AC1 The request carries the treatment values and the pinned template version (new, D-RCV-60)
    Given the rwb-document contract mock returns document "DOC-0311" of type "CONTRACT" with templateCode "DIL-CONTRACT", templateVersion 2 and source "GENERATED", and one document each of type "CREDIT_APPROVAL" and "MORTGAGE_DOCUMENT"
    Given the treatment row "TRT-0301" holds offer_amount 1250000.00 and its own installments, interest rate and first due date
    When generateContractDocument runs for treatment "TRT-0301" with template codes "DIL-CONTRACT", "DIL-CA" and "DIL-MORTGAGE"
    Then the request carries treatmentId "TRT-0301", the three template codes and language TH
    Then the values this service supplies are exactly the ones its own row holds: transfer_price 1250000.00 from offer_amount, the installments, the interest rate, the first due date, and the case and decision-record identifiers
    Then case_no, borrower_name and title_doc_no are not supplied by this service, and no name and no national ID number is put on the request
    Then the template version recorded is the one the contract reports in force, version 2 on 2026-12-10 and version 3 from its valid-from date 2026-12-15

  Scenario: AC2 A missing merge value is refused and nothing is generated (new, D-RCV-60)
    Given the case has no title_doc_no
    Given the rwb-document contract mock returns status 422 with the problem body messageId "MSG-P5-009" naming "DIL-CONTRACT" and "title_doc_no"
    When generateContractDocument runs for treatment "TRT-0301" and template "DIL-CONTRACT"
    Then the answer is 422 with MSG-P5-009 naming "DIL-CONTRACT" and "title_doc_no", carried back unchanged
    Then no document reference and no template version is written on the treatment row, and no decision record and no outbox row is written
    Then the treatment keeps the state and the columns it had, and the stage reports the refusal to the parent CaseWorkflow without a case move

  Scenario: AC3 The reference is stored with the decision record in one transaction (new, D-RCV-60)
    Given the rwb-document contract mock returns document "DOC-0311" of type "CONTRACT" with templateCode "DIL-CONTRACT", templateVersion 2 and a decisionLogEntryId
    When generateContractDocument runs for treatment "TRT-0301" and template "DIL-CONTRACT"
    Then the treatment row "TRT-0301" holds document reference "DOC-0311" and template version 2
    Then the same transaction writes the local decision record with decision code "D6.4", template code "DIL-CONTRACT", template version 2 and document "DOC-0311"
    Then the outbox row of rwb.treatment.ContractDocumentGenerated.v1 is written in the same transaction
    Then a forced failure of the reference write, of the record or of the outbox row leaves none of the three in rwb_treatment

  Scenario: AC4 A repeated request with the same key returns the first reference and writes once (new, D-RCV-60)
    Given a request with Idempotency-Key "K-0301" generated document "DOC-0311" and wrote one decision record
    When the same request with Idempotency-Key "K-0301" arrives again, or the activity is replayed after a worker restart
    Then the answer is the first answer with document "DOC-0311" and the first decisionLogEntryId
    Then no second document reference, no second template version and no second decision record is written, and the treatment row is unchanged
    Then the write key is the treatment ID, the template code and the template version, so a version 3 in force from 2026-12-15 is one new request and not a repeat

  Scenario: AC5 The record names the template code and version, and a record failure stops the call (new, D-RCV-60)
    Given the rwb-document contract mock returns document "DOC-0311" with templateCode "DIL-CONTRACT" and templateVersion 2
    Given the decision-record library answers MSG-P7-003 and accepts no write
    When generateContractDocument runs for treatment "TRT-0301" and template "DIL-CONTRACT"
    Then the record this story attempts carries decision code "D6.4", template code "DIL-CONTRACT" and template version 2
    Then the whole call fails with MSG-P7-003 and nothing in rwb_treatment changes: no reference, no version, no outbox row
    Then the document "DOC-0311" the engine produced is referenced by no treatment, and the activity retries on the platform policy

  Scenario: AC6 A refusal or a 503 leaves the treatment unchanged (new, D-RCV-60)
    Given the rwb-document contract mock refuses generation for treatment "TRT-0302" with status 409 and MSG-P5-011
    When generateContractDocument runs for treatment "TRT-0302"
    Then the answer is 409 with MSG-P5-011 and treatment "TRT-0302" keeps every column it had
    Given the rwb-document contract mock answers status 503 with MSG-GEN-006 naming "Document service"
    When generateContractDocument runs for treatment "TRT-0301" and template "DIL-CONTRACT"
    Then nothing is stored before the call succeeds, and the activity retries on the platform policy with a 1 s initial interval, back-off 2 and 10 attempts
    Then no partial document set is referenced and no decision record is written on any failed attempt

  Scenario: AC7 The generated document shows on SCR-14 through the composite route (new, D-RCV-60)
    Given the gateway-bff composite route serves SCR-14 Treatment record for case "RW-2026-000301"
    Given treatment "TRT-0301" holds document reference "DOC-0311" and template version 2
    When the officer opens SCR-14
    Then SCR-14 shows document "DOC-0311" of type "CONTRACT" with template code "DIL-CONTRACT" and template version 2, read from this service and merged with the document read of rwb-document
    Then the browser calls no owner service directly and this service serves no screen field list
    Then the reference shows with the decision record it was written with, and this service serves no merge value and no file byte

  Scenario: AC8 No personal data reaches the event, the merge payload or the logs (new, D-RCV-60)
    Given treatment "TRT-0301" is linked to case "RW-2026-000301" and to party identifiers, never to names
    When generateContractDocument runs and the event and the log lines are written
    Then the event rwb.treatment.ContractDocumentGenerated.v1 carries caseId, treatmentId, documentId "DOC-0311", templateCode "DIL-CONTRACT" and templateVersion 2 and no name, no national ID number and no title-doc number
    Then the values this service supplies carry identifiers, codes, amounts and dates only, never a name
    Then no log line, no workflow input and no history field carries a personal value, and the profile codec is on every payload
```

The eight criteria are new under D-RCV-60 and test only the S2 deliverable of this story: the request and its values, the pinned version, the reference in one transaction with the record, the repeat, the record failure, the refusal and the unavailable service, the screen and the personal-data boundary (ASM-3079). The fourteen legacy criteria AC1 to AC14 of RWB-E2-026 — Generate, Missing field, Version, A version not approved by Legal, A withdrawn template, A treatment that is not approved, The decision log write fails, A repeated request, Two requests at the same time, A template body that cannot be rendered, No template for the product group, A case outside the caller's scope, A set of three documents in one request and A set stored whole or not at all — belong to `RWB-P5-E2026-APP`, are written there word for word with their origin tags, and are not restated here. The paths, the request and answer shapes, the error set and the fakes this story consumes are `RWB-P5-E2026-CON`'s. The cross-service journey of the same values across rwb-treatment, rwb-document, rwb-comms and rwb-case is `RWB-ITG-E2026-ITG`'s and no criterion of this story claims it.

Three readings of the sources are stated here rather than hidden in the code. The operation identifier of the generation call and the shape of the S2 value set on the wire are Not specified in the source documents, so they come from `RWB-P5-E2026-CON` and from this story's own design over the row's fields (GAP-1878; ASM-3080). The `treatment` table of TSD S2 T3.1 has no column that holds a document reference and no column that holds a template version, so this story adds two nullable columns and records the difference (GAP-1878; ASM-3085). The template catalogue and the merge-field definitions sit with P6 rwb-comms in the target while the legacy files them under the document module's feature, and the loser is the legacy placement, which changes nothing here because this story reads neither table (GAP-1879; ASM-3082).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | This service supplies only the merge values its own `treatment` row holds; a name, a national ID number and a title-doc number are never supplied by it and reach it from no table and no view | DP-05, CTL-11, DL26; legacy RWB-E2-026 BR11; TSD S2 T3.1 |
| BR2 | The template version is the one in force on the request date — approved by Legal, active and valid on that date, the most specific product group match winning over a template for all products — read by the catalogue owner and pinned on the treatment row as reported | Legacy RWB-E2-026 BR1; DF-REF-047, DF-REF-049, DF-REF-051; CTL-14; R-UNI-38 |
| BR3 | A new template version applies to documents generated from its valid-from date; earlier documents keep the version they were generated under, and that version stays readable on the treatment row | Legacy RWB-E2-026 BR10; R-UNI-38 |
| BR4 | An approval below the floor, a withdrawn template and a treatment that is not open are refusals that arrive on the contract's problem body; this service re-words no message and stores nothing on a refusal | Legacy RWB-E2-026 BR2, BR5, BR7; MSG-P5-010, MSG-P6-003, MSG-P5-011 |
| BR5 | A document reference is written only with the decision record of the same generation, in one transaction, with the template code and the template version; a failed record write rolls the reference back too | Legacy RWB-E2-026 BR7; Principle 5; R-UNI-39; DP-03 |
| BR6 | A repeat with the same key writes once: one reference, one pin and one record; the key is the treatment ID, the template code and the template version | Legacy RWB-E2-026 BR9; R-UNI-40; AC4 |
| BR7 | A generation that the treatment records is announced once, on this service's topic, with identifiers, the document type, the template code, the template version and the decision record; no personal value and no file byte is on it | DP-09; Architecture v5 slides 18 and 42 notes; AC8 |
| BR8 | No value a business person may change is written in code: the template codes, the type mapping, the languages, the formats, the generation window and the template bound are data rows or parameters read at their version | Legacy RWB-E2-026 BR4, section 17; BR-S2-001; DP-06, DP-07 |
| BR9 | This service reads no `document`, `document_type`, `document_hub_parameter`, `template` or `merge_field` row and no `v_ace_*` view; the documents and the catalogue arrive only on the published contract, and the `rwb_treatment` login holds no grant that would allow otherwise | DP-01; Architecture v5 slides 29 and 41; Ownership Map |
| BR10 | The case status stays rwb-case's: the stage reports the generation and the target state R-DIL-16 names to the parent `CaseWorkflow`, which moves the status, and this service writes no case table | DP-01; Architecture v5 slide 18; FSD S2 A2.18 |
| BR11 | The two columns this story adds are nullable and additive: a treatment without a generated document keeps them empty, and no sibling story's write is narrowed by them | DP-15; TSD S2 T3.1; section 13 |
| BR12 | A refusal of the engine, a 503 or a record failure leaves the treatment exactly as it was; nothing is stored before the engine's 201 answer names the document and its version | AC2, AC5, AC6; R-UNI-39 |
| R-UNI-38 | A new rule version applies to decisions taken from its effective date, and an open case keeps the version it was decided under. Here it is the template version, pinned on the treatment row | Business Rules and Routing Logic v4 (R-UNI-38) |
| R-UNI-39 | The decision record, the change and the outbox rows are one transaction; a failed write moves nothing | Business Rules and Routing Logic v4 (R-UNI-39); Temporal and Drools Design slide 14 |
| R-UNI-40 | A repeated request with the same key returns the first result and writes nothing new | Business Rules and Routing Logic v4 (R-UNI-40) |
| R-DIL-16 | The credit approval, the contract and the mortgage documents are generated when `final_call = approved`, and the offer goes to the customer; the target state is OFFER_WITH_CUSTOMER_DIL | Business Rules and Routing Logic v4 (R-DIL-16); FSD S2 A2.18.3.1 |
| CTL-11 | Personal data is masked for a role that may not see it and is not copied outside the system that owns it; no name, national ID number or title-doc number is written to `rwb_treatment` | Legacy RWB-E2-026 BR11; CTL-11; DL26 |
| CTL-14 | A document is produced only from an approved template version, and the approval is recorded against the version | Legacy RWB-E2-026 BR1; CTL-14 |

The rules hold in `rwb_treatment` as follows. BR1 is the value builder: it holds the four column names of the row and the two identifiers, and a property test places a synthetic name in the contract's answer and proves it appears in no column, no log line, no event and no span attribute. BR2 and BR3 are the pin: the version is taken from the answer and never computed here, and the build check fails on a version literal. BR4 and BR12 are the ordering of the checks: nothing opens a transaction until the engine has answered 201. BR5 and BR6 are the writer's one transaction and the write key. BR7 is the outbox row and the AsyncAPI fragment. BR8 is the parameters and reference-data reads. BR9 is the schema grant and the boundary test. BR10 is the child-workflow return. BR11 is the migration review: two nullable columns, no backfill and no change to an existing column.

### 9. State transitions

None of the rows below is a case status owned here: each is a change of this service's own record, and the case status R-DIL-16 implies is reported to the parent `CaseWorkflow` (BR10; DP-01).

| From | Event | Condition | To |
|---|---|---|---|
| A `treatment` row with no contract document | `generateContractDocument` and a 201 answer from the engine | R-DIL-16 with `final_call = approved`, the treatment approved and open, the engine's version approved by Legal | The same row with the document reference and the template version written, in state DRAFT of the document |
| A `treatment` row with a document reference | A repeat of the same request key | Same treatment, same template code, same template version | Unchanged; the first reference is answered |
| A `treatment` row with no contract document | A refusal of the engine | MSG-P5-009, MSG-P5-010, MSG-P6-003, MSG-P5-011 or MSG-GEN-004 | Unchanged, and the stage reports the refusal |
| A `treatment` row with no contract document | A record failure or a 503 | MSG-P7-003 or MSG-GEN-006 | Unchanged; the transaction rolls back and the activity retries |
| A `treatment` row with a document reference | A new template version in force | A new request with the new version on or after its valid-from date | The reference and the version of the new request; the earlier document keeps its own version on the document side |

The document's own lifecycle is not this story's: `source` GENERATED, state DRAFT and `write_once` false are the values of the generated draft, and the review out of DRAFT and the write-once switch on send belong to the screens story of this key (RWB-P5-E2017-APP). The treatment's `state` column is not moved here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer (FCR) | Treatment and offer CRUA in the TSD S2 T6.1 matrix: runs the generation from the treatment screen and reads the reference and the version it produced |
| RW-CASEOWN, case owner | Treatment and offer CRU: the same in scope |
| RW-SPECIAL, hardship and vulnerability specialist (CRU); RW-GUARANT, guarantee officer (CRU) | Read the treatment and its document reference on cases in scope; the request is the officer's |
| RW-TEAMMGR, team manager (R); RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE (R) | Read the reference and the version on cases in scope; generate nothing |
| RW-CREDCOMM, credit approval committee member (RA); RW-PRODHEAD, product head (RA) | Read the reference; the approval itself is RWB-S2-E3003-APP's |
| SY-CASEWF, the case workflow module (R) | Calls the generation for rule-driven generation through the stage, with the service identity of `rwb_treatment`, as R-DIL-16 names |
| The rwb-treatment service identity (login `rwb_treatment`, DP-02) | Builds the request, calls the contract once, writes the two columns, the record and the outbox row in one transaction, and holds no grant on `rwb_document`, `rwb_comms`, `rwb_case` or a `v_ace_*` view |
| rwb-document (P5) service identity | Owns the engine, the documents, the types and the files; answers the generate operation and is never written by this story |
| rwb-comms (P6) service identity | Owns `template` and `merge_field` and the Legal approval of a version; this story reads neither table and calls no P6 operation |
| No delegation of authority level applies | The treatment was approved at D6.4 before generation; this story requests documents and records their reference |

No credential and no personal name appears in the request, the row, the record, the event or the logs. Where a person must be named the row carries a user identifier, never a name.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment (S2, `rwb_treatment`) | id | Read: the treatment of the request and the first element of the write key |
| DF-TRT-002 | treatment (S2, `rwb_treatment`) | case_id | Read: the case identifier the request carries instead of any party name |
| DF-TRT-003 | treatment (S2, `rwb_treatment`) | decision_log_id | Read: the approval reference the stage already holds; the record of this generation is a new row and this column is not overwritten here |
| DF-TRT-004 | treatment (S2, `rwb_treatment`) | treatment_type | Read: only DEED_IN_LIEU and RESTRUCTURE are in the legacy precondition, and the engine decides the rest |
| DF-TRT-007 | treatment (S2, `rwb_treatment`) | offer_amount | Read: the contract amount (`transfer_price`), 1250000.00 in the legacy example |
| DF-TRT-009 | treatment (S2, `rwb_treatment`) | installments | Read: the installments of the plan |
| DF-TRT-010 | treatment (S2, `rwb_treatment`) | valid_until | Read: the offer end date, where the row holds one; it is not the `contract_date` code of the legacy example (GAP-1878; ASM-3080) |
| DF-TRT-012 | treatment (S2, `rwb_treatment`) | booked_at | Read, nullable: empty at generation, because generation precedes booking |
| DF-TRT-013 | treatment (S2, `rwb_treatment`) | outcome | Read: empty is the legacy precondition "no outcome" |
| DF-TRT-027 | treatment (S2, `rwb_treatment`) | interest_rate | Read: the interest rate of the plan |
| DF-TRT-029 | treatment (S2, `rwb_treatment`) | first_due_date | Read: the first due date of the plan |
| No field ID | treatment (S2, `rwb_treatment`) | the contract-document reference this story adds | Write: the `documentId` of the CONTRACT document the engine returned; no field of TSD S2 T3.1 carries it (GAP-1878; ASM-3085) |
| No field ID | treatment (S2, `rwb_treatment`) | the pinned template version this story adds | Write: the `templateVersion` the engine reported for that document (GAP-1878; ASM-3085) |
| DF-DEC-001 to DF-DEC-018 | decision_record (local, in `rwb_treatment`) | all fields through `DecisionRecordWriter.record` | Write, in the same transaction: decision code D6.4, the template code, the template version and the document reference (DP-03) |
| DF-DOC-001, DF-DOC-032, DF-DOC-033 | document (P5, `rwb_document`) | id, template_id, treatment_id | Not read directly: the identifier, the template and the treatment of the document arrive in the answer of the contract and are never read from the table (BR9) |
| DF-DOC-002, DF-DOC-004, DF-DOC-010 | document (P5, `rwb_document`) | case_id, document_type, source | Not read directly: carried on the answer as `caseId`, `documentType` and `source` |
| DF-REF-045 to DF-REF-051 | template (P6, `rwb_comms`) | all fields | Not read directly: the version in force, its Legal approval and its merge fields arrive on the contract's template answer |
| DF-REF-0xx | merge_field (P6, `rwb_comms`) | code, required flag, format | Not read directly: the required set and the format arrive on the template answer; a missing required value is the engine's refusal |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (P7, `rwb_decision`) | the central ledger entry | Not written and not read here: P7 seals it from the shared topic (DP-03) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (`rwb_case`, owner P3) | the case and its status | Not read and not written; the case identifier is carried as a value and the status is the parent's |
| Standard column | treatment (S2, `rwb_treatment`) | state, version, created_at, created_by, updated_at, updated_by | Write: `version`, `updated_at` and `updated_by` move with the two columns; `state` is not moved |
| idempotency_key | PLT library, created in `rwb_treatment` | the write key of the request | Write, once per request |

Field IDs are those of TSD S2 T3.1 and the Logical Data Model and Data Dictionary. **Two columns and one index are added to `treatment`, and no table.** The document-side identifiers, the template fields, the merge-field definitions, the case fields and the central ledger are named here to show what this story does **not** touch: they arrive through the contract or the event, or they never arrive at all. No foreign key leaves `rwb_treatment`: the document reference is an identifier and not a foreign key into `rwb_document`, and `case_id` and `decision_log_id` are cross references (DP-01).

**No personal data.** The only personal values in the pipeline are the customer name and the title-doc number that the generation engine reads from their owners to fill a template. They never pass through this service: it supplies identifiers, codes, amounts and dates only, it stores none of them, it logs none of them and it puts none of them on an event (CTL-11; DP-05; ASM-3081).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). This slice provides no operation of its own: the reference it writes surfaces on the read RWB-S2-E3001-CON already declares, as two additive optional properties, and the additive change is inside major version 1.

| ID | Method | Path | This story | Access | Idempotency |
|---|---|---|---|---|---|
| API-S2-002 | GET | `/treatments/{treatmentId}` | Adds two optional properties to the `Treatment` answer — the contract-document reference and the pinned template version — and serves them from `rwb_treatment`; the declared operation, its error set and its fakes are RWB-S2-E3001-CON's | Treatment and offer R, scope applied, through the guard library | Not applicable |

The errors remain the ones of RWB-S2-E3001-CON: 401, 403 with MSG-P4-002, 404 with MSG-P4-003, 409, 422 and 503. The two added properties are nullable, so a consumer that ignores them keeps working and a treatment without a generated document answers empty values.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| POST | `/api/recovery/document/v1/cases/{caseId}/generated-documents` (API-P5-016), operation identifier Not specified in the source documents (GAP-1878; ASM-3080) | P5 rwb-document (`RWB-P5-E2026-CON`) | The generate operation: `GenerateRequest` with `treatmentId`, `templateCodes` and `language` in, 201 `GenerationResult` with `decisionLogEntryId` and the `Document` set out — each document with `documentId`, `documentType`, `source`, `docVersion`, `templateCode`, `templateVersion` and `treatmentId`; the `Idempotency-Key` header; one hop, 2 s, a breaker, no call chain (DP-11, ADR-020); built against the contract and its fake |
| GET | the parameters read of the generation bound, operation Not specified in the source documents (GAP-1878; ASM-3086) | P3 rwb-case (`RWB-P3-E1042-CON`) | `GEN_MAX_TEMPLATES`, whose value is 10, at its version, cached; the request is refused before the call when its template codes exceed it (DP-06) |
| GET | the reference-data read of the document type list, operation Not specified in the source documents (GAP-1878; ASM-3086) | P3 rwb-case (`RWB-P3-E1043-CON`) | LOV-DOC-TYPE with the types CONTRACT, CREDIT_APPROVAL and MORTGAGE_DOCUMENT at their version; the codes this service may ask for are the list values and no code is a constant (DP-07) |

One operation is consumed at run time and two are consumed as a parameter and a list; all three are one hop with a 2 s timeout and a breaker, and none calls another service. A failed generation answers 503 with MSG-GEN-006 naming "Document service"; a failed parameter or list read answers 503 with MSG-GEN-006 naming "Reference data"; and no refusal returns a partial document set.

#### 12.3 Events published

| Event | Topic | Shape | Written by |
|---|---|---|---|
| `rwb.treatment.ContractDocumentGenerated.v1` | `rwb.treatment.events.v1` (DP-14) | CloudEvents 1.0, keyed by caseId; payload treatmentId, caseId, documentId, documentType, templateCode, templateVersion, decisionLogEntryId; no personal value, no merge value, no file byte | The outbox row of the same `rwb_treatment` transaction as the reference and the record (DP-09) |
| decision record | `rwb.decision-record.v1` | Hash-chained record with decision code D6.4, the template code and the template version and `inputsRef` naming the merge snapshot, never the snapshot | The RWB-PLT-E1027-CON library, inside the caller's transaction (DP-03) |

The event name, its payload and the decision code of the generation are this story's design: the service's catalogue events are TreatmentApproved and TreatmentClosed, which belong to RWB-S2-E3003-APP and to the closing story, and no source names a third event or a code for this one (GAP-1878; ASM-3086). The event carries identifiers, a type code, a template code, a version and a record reference, which is the shape the no-personal-data rule requires (ASM-3081).

#### 12.4 Events consumed

None. The generation is triggered inside the stage by the evaluated package, not by a Kafka subscription: the case signal is a Temporal signal the parent `CaseWorkflow` forwards, the rule package arrives on `rwb.decision.RulePackageInForce.v1` for the stage that RWB-S2-E3001-APP builds, and the documents are asked for synchronously. This story holds no consumer group and writes no inbox row of its own; the inbox table of the platform library exists in `rwb_treatment` for the consumers the sibling stories add.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` | Workflow, the stage child of `CaseWorkflow`, one execution per case and stage | `rwb-treatment` in namespace `rwb-recovery` | Named here as the stage the generation runs in; built by RWB-S2-E3001-APP and unchanged by this slice |
| `generateContractDocument` | Activity | `rwb-treatment` | `treatmentId` and the template codes in; the document reference, the template version, the decision record and the engine's answer out; one call, one transaction, idempotent by the write key |
| `recordAndApply` | Activity | `rwb-treatment` | The row change, the local decision record, the outbox row and the idempotency row in one transaction (the `RecordAndApply` contract of the design); shared with the sibling stories and used here for the reference |

The activity name `generateContractDocument` is this story's design and is fixed by no source document (GAP-1878; ASM-3080); the design's `TreatmentWorkflow` and `RecordAndApply` are its own.

#### 12.6 Schedules

None. The generation is a step of the stage, not a job: no row of the job map belongs to this capability, no cron entry, no Temporal Schedule and no event-started workflow is created or moved, and DP-10 is not in this story's pattern set.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Two nullable columns and one index added by this story's Flyway version; the columns are written by the generation transaction and read by the treatment read |
| `decision_record` | `rwb_treatment` | PLT library object applied in this schema | Written through `DecisionRecordWriter.record` in the caller's transaction; the central `decision_log_entry` is P7's and is never touched |
| `idempotency_key` | `rwb_treatment` | PLT library object | The write key of the generation and the result it answers on a repeat |
| `outbox_event` | `rwb_treatment` | PLT library object | The `ContractDocumentGenerated` row of the same transaction, relayed by the outbox sender |

Not owned and never read as a table: `document`, `document_type`, `document_hub_parameter`, `document_field`, `signature_request` and `retention_rule` (P5, `rwb_document`), `template`, `merge_field` and `notice` (P6, `rwb_comms`), `recovery_case`, `parameter_catalog`, `reference_row` and `lov_value` (P3, `rwb_case`), `decision_log_entry` (P7, `rwb_decision`) and every `v_ace_*` view (P1). No foreign key leaves the schema and no cross-schema join exists (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-document generate fake (`RWB-P5-E2026-CON`) | For treatment "TRT-0301" and the three codes: 201 with "DOC-0311" of type CONTRACT, `templateCode` "DIL-CONTRACT", `templateVersion` 2 and one document each of type CREDIT_APPROVAL and MORTGAGE_DOCUMENT; a 422 with MSG-P5-009 naming "DIL-CONTRACT" and "title_doc_no"; a 422 with MSG-P5-010 for an unapproved version; a 422 with MSG-P6-003 for a withdrawn template; a 409 with MSG-P5-011 for treatment "TRT-0302"; a 409 with MSG-GEN-004 for a concurrent request; a 503 with MSG-GEN-006; no answer beyond 2 s | AC1, AC2, AC3, AC4, AC6 |
| decision-record writer fake (`RWB-PLT-E1027-CON`) | An accepted record with its chain sequence and entry hash; a refusal with MSG-P7-009 and the field; an unavailable store answering MSG-P7-003 | AC3, AC5 |
| rwb-case parameters fake (`RWB-P3-E1042-CON`) | `GEN_MAX_TEMPLATES` 10 at its version, and a delayed answer beyond 2 s | AC1, AC6 |
| rwb-case reference-data fake (`RWB-P3-E1043-CON`) | LOV-DOC-TYPE with the types of the mapping at its version | AC1, AC2 |
| gateway-bff composite route fake (`RWB-PLT-N001-CON`) | The merged SCR-14 answer for case "RW-2026-000301" with the treatment read of this service and the document read of rwb-document once | AC7 |
| outbox and idempotency doubles | One row per committed transaction; a repeat of the same key answered from the first row | AC3, AC4, AC8 |

The fakes are test-only and are replaced by the real services in SIT; a drift between a fake and the published contract is a build failure of `RWB-P5-E2026-CON` or of the platform story that owns the fake.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided (additive), 3 consumed | `GET /treatments/{treatmentId}` on `/api/recovery/treatment/v1` with the two added properties; the generate operation of `RWB-P5-E2026-CON` on `/api/recovery/document/v1`, and the parameters and reference-data reads of rwb-case; one hop and 2 s on each consumed call |
| Kafka | 1 published, 0 consumed | `rwb.treatment.ContractDocumentGenerated.v1` on `rwb.treatment.events.v1`, written in the outbox of the generation transaction (DP-09); the record on `rwb.decision-record.v1` written by the library |
| Temporal | The stage and 1 activity of this slice | `TreatmentWorkflow` on queue `rwb-treatment` in namespace `rwb-recovery`, with `generateContractDocument` and the shared `recordAndApply`; no Schedule and no timer of its own |
| File | None | No file is read, built or delivered: the document body and the blob are rwb-document's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, module `generation`, Java package `th.co.scb.ace.workbench.recovery.treatment.generation`. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-11 is the whole point of the slice: the legacy in-process `DocumentGenerator` becomes one hop with a published shape, a fake and a 2 s timeout, so S2 builds on Day 1 without a document table. DP-05 is a boundary rather than a call: this module reads no ACE view and calls no ACE interface, because the values it supplies are its own row's. DP-01 keeps the write inside `rwb_treatment` — the two columns, the record and the outbox row — and makes the document, the template and the case unreachable as tables. DP-03 is the record of the generation and DP-09 the announcement of it, both in the caller's transaction. DP-06 and DP-07 are the two reads of 12.2, so no list value and no bound is a constant. DP-15 is this story's migration. DP-19 is the route SCR-14 and SCR-15 use.

**Dependencies the table adds and the plan does not hold.** The pattern table adds five H rows — `RWB-PLT-E1027-CON` for DP-03, `RWB-PLT-E1042-CON` and `RWB-PLT-E1043-CON` for DP-06 and DP-07, `RWB-PLT-TE006-CON` for DP-09 and `RWB-PLT-E1044-CON` for DP-15 — plus `RWB-PLT-N001-CON` for DP-19, and two C rows, `RWB-P3-E1042-CON` and `RWB-P3-E1043-CON`, while the plan's lists for this story hold Depends on (build) `None` and Contract dependencies `RWB-P5-E2026-CON` only. The metadata table keeps the plan's lists as they are, the story builds against the fakes until those platform stories publish, and the DP-03 dependency is the one the platform contract supplies on Day 1 (ASM-3084).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `generateContractDocument` | Activity | Builds the request, calls the contract once, takes the contract document of the answer and hands the reference and the version to the writer; idempotent by the write key |
| `GenerationClient` | Client | The generate call on `RWB-P5-E2026-CON`, one hop, 2 s, a breaker, no retry chain, with the problem body carried back unchanged (DP-11) |
| `TreatmentMergeValueBuilder` | Service | Builds the S2 value set from the row's four columns and the two identifiers, and holds no name, no national ID number and no title-doc number (BR1) |
| `GenerationRequestGuard` | Service | Checks the template codes against LOV-DOC-TYPE and the count against `GEN_MAX_TEMPLATES` at their version, before any call (DP-06, DP-07) |
| `DocumentReferenceWriter` | Repository | Writes the two columns of `treatment` in one `rwb_treatment` transaction, with the record, the outbox row and the idempotency row |
| `DecisionRecordAdapter` | Library adapter | Calls `DecisionRecordWriter.record` with decision code D6.4, the template code and the template version (DP-03) |
| `GenerationEventPublisher` | Library adapter | Writes the `ContractDocumentGenerated` outbox row of the same transaction (DP-09) |
| `GenerationIdempotency` | Service | The write key of treatment ID, template code and template version; recognises a repeat and re-runs nothing that completed |
| `TreatmentReferenceView` | Service | Serves the two added properties on the treatment read, and nothing else |

**Database.** `treatment` gains two nullable columns: the contract-document reference, of the key type TSD P5 T3.1 gives the document identifier (DF-DOC-001, uuid), and the pinned template version, an integer. Their names, and the fact that the treatment rather than the document holds them, are this story's design and are Not specified in the source documents (GAP-1878; ASM-3085). The index is `ix_treatment_contract_document ON treatment (contract_document_id)` so a document reference resolves to the treatment it belongs to; no uniqueness rule is implied, because the write key of the record is the triple of treatment, template code and version. No existing column changes, no backfill runs, and no row of another service's table is copied (DP-01, DP-15).

**Configuration and reference data.**

- `GEN_MAX_TEMPLATES`, whose value is 10, is read through the parameters contract and client library of rwb-case (DP-06); the operation this story calls is Not specified in the source documents (GAP-1878; ASM-3086).
- LOV-DOC-TYPE with the types CONTRACT, CREDIT_APPROVAL and MORTGAGE_DOCUMENT is read through the reference-data client library (DP-07); no type code is copied into `rwb_treatment`.
- The template codes, the type mapping, the languages and the formats stay data of P6 and P5 and reach this service only on the answer of the contract (GAP-1879; ASM-3082).
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020 and not a value of this story.
- The feature switch `rwb.treatment.contract-document`, read as a flag of the platform library: off means the stage requests no document, the two columns stay empty, no record and no event is written, and the treatment read answers empty values.

**Build steps**

1. The Flyway version with the two nullable columns and the index, and its migration test against the sibling's `treatment` template (AC3, BR11).
2. `GenerationClient` against the contract fake, with the 2 s budget, the breaker, the no-answer path and the problem bodies of MSG-P5-009, MSG-P5-010, MSG-P6-003, MSG-P5-011, MSG-GEN-004 and MSG-GEN-006 (AC2, AC6).
3. `TreatmentMergeValueBuilder` with the row's four columns and the two identifiers, and the property test that a synthetic name reaches no column, no log line and no event (AC1, AC8).
4. `GenerationRequestGuard` over the parameters and reference-data fakes, with an unknown type code and a count above the bound (AC1).
5. `DocumentReferenceWriter`, `DecisionRecordAdapter` and `GenerationEventPublisher` in one transaction, with the rollback path of the record failure (AC3, AC5).
6. `GenerationIdempotency` with the repeat, the replay and the new version in force (AC4, AC7 of the legacy on the engine side).
7. `TreatmentReferenceView` on the declared read, additive, with a treatment that has no document (AC7).
8. The boundary test: no statement outside `rwb_treatment`, no read of `rwb_document`, `rwb_comms`, `rwb_case` or a `v_ace_*` view, one event only, and no Schedule in the module (BR9, section 12.9).

**Feature flag.** `rwb.treatment.contract-document`.

**Done when.** The tests of section 16 pass, the contract tests of `RWB-P5-E2026-CON` stay green, a SIT week shows one reference and one pinned version per treatment, one record and one event per generation, a repeated request writes once, a forced record failure leaves no column and no outbox row, SCR-14 shows the reference and the version through the composite route, and no read of a document, template or case table appears in the logs.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-009 | The engine refuses because a required merge field has no value (X1, AC2) | {template} cannot be generated. {field} has no value on the case. |
| MSG-P5-010 | No current template version approved by Legal, or no template for the product group or language (X2, AC6) | {template} has no version approved by Legal for {product} in {language}. |
| MSG-P6-003 | The template is withdrawn (X3, AC6) | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P5-011 | The treatment is not approved or not open (X4, AC6) | Documents can be generated only for an approved {treatment} that is still open. |
| MSG-P7-003 | The local decision record cannot be written (X5, AC5) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-009 | The record is refused for a missing or invalid field (X5) | The decision record was refused: {field} is missing or not valid. |
| MSG-GEN-004 | A concurrent request for the same treatment and template (X7) | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | The document service did not answer, or the parameter or list read failed (X8) | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | The caller holds no Documents C on the request, or no Treatment and offer right on the read (X9, AC8) | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case or the treatment lies outside the caller's scope (X9, AC6) | This case is not in your scope. |

The message IDs and the wording are copied unchanged from legacy RWB-E2-026 section 14; the generation texts are the document service's and this story re-words none of them. Thai text for each message follows decision DL10. Delivery shape: each error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. MSG-P7-003 and MSG-P7-009 are the library's and are declared by RWB-PLT-E1027-CON; for MSG-GEN-006 the {system} value is "Document service" on the generation call and "Reference data" on the parameter and list reads; for MSG-P4-002 the {action} value names what the caller tried and never a case fact or a document identifier.

### 15. Screens and states

No screen is built in this story. Two surfaces show what it writes, both read through the gateway-bff composite route (DP-19), and only the first is this service's own read model.

| Screen | State | What the user sees |
|---|---|---|
| SCR-14 Treatment record | Loading | The placeholder while the composite route answers |
| SCR-14 Treatment record | Draft, with a generated document | The treatment's terms, its state and its document reference of type CONTRACT with the template code and the pinned template version, read from this service, with the document itself as rwb-document serves it |
| SCR-14 Treatment record | Draft, no document yet | The treatment without a reference, and the generation action the screens story offers |
| SCR-14 Treatment record | Refused | MSG-P5-009, MSG-P5-010, MSG-P6-003, MSG-P5-011, MSG-P4-002 or MSG-P4-003 as the engine or the guard answered, with the treatment unchanged |
| SCR-14 Treatment record | Document service unavailable | MSG-GEN-006, and the treatment keeps the columns it already holds |
| SCR-15 Settlement offer | Draft; below floor; approved; sent; accepted | The treatment the offer is built on and its document reference, read only here; the offer itself is RWB-S2-E3002-APP's |

The route merges the answer of this service with the document read of rwb-document; the route path, the screen-model field list and the merge order belong to `RWB-PLT-N001-CON` and the edge stories, not here (ASM-3083). The screen field list and the layout of SCR-14 and SCR-15 belong to the screen owners, and this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-026-15 | AC8 (legacy Access) | Component | RW-TEAMMGR user (Documents R) calls the generate operation; refused with MSG-P4-002 and the treatment unchanged |
| TC-E2-026-01 | AC1, AC3 (legacy AC1) | End to end | Synthetic mortgage case "RW-2026-000301" and DIL treatment "TRT-0301", template DIL-CONTRACT v2, transfer_price 1250000.00, document "DOC-0311" |
| TC-E2-026-02 | AC2 (legacy AC2) | End to end | Case with no title deed number |
| TC-E2-026-03 | AC1, AC4 (legacy AC3) | End to end | Template v3 valid from 2026-12-15 |
| TC-E2-026-04 | AC6 (legacy AC4) | End to end | DIL-CA v1 not approved |
| TC-E2-026-05 | AC6 (legacy AC5) | End to end | DIL-MORTGAGE withdrawn |
| TC-E2-026-06 | AC6 (legacy AC6) | End to end | Treatment "TRT-0302" with no decision_log_id |
| TC-E2-026-07 | AC5 (legacy AC7) | End to end | Decision log stub refusing writes |
| TC-E2-026-08 | AC4 (legacy AC8) | End to end | Same Idempotency-Key "K-0301" twice |
| TC-E2-026-09 | AC4, AC6 (legacy AC9) | End to end | Two parallel requests |
| TC-E2-026-10 | AC6 (legacy AC10) | End to end | Damaged template body |
| TC-E2-026-11 | AC2, AC6 (legacy AC11) | End to end | Hire purchase case, mortgage-only template |
| TC-E2-026-12 | AC6 (legacy AC12) | End to end | Case of team HP-NE, officer of team FCR-BKK |
| TC-E2-026-13 | AC1, AC3 (legacy AC13) | End to end | Three current templates |
| TC-E2-026-14 | AC2, AC6 (legacy AC14) | End to end | Three templates, DIL-CA not approved |
| TC-E2-026-16 | AC5 (legacy Principle 5) | Component | Decision log write forced to fail during a three-document set; no document, no file, MSG-P7-003, incident raised |
| TC-S2-E2026-APP-01 | AC1 | Component | The request for treatment "TRT-0301": the S2 value set equals the row, the three codes, language TH, template version 2 pinned, and no name on the payload |
| TC-S2-E2026-APP-02 | AC2, AC3, AC5 | Integration | Engine 201 with "DOC-0311" stored with its record and outbox row in one transaction; a forced record refusal rolls all three back |
| TC-S2-E2026-APP-03 | AC4, AC6 | Component | A repeat of key "K-0301" and a replay answer the first reference; a 409 and a 503 write nothing and retry on the platform policy |
| TC-S2-E2026-APP-04 | AC7, AC8 | Component | SCR-14 through the composite route shows "DOC-0311" with template version 2; the event and the logs carry no personal value |

The sixteen legacy test case IDs, their Covers and their Data are kept in the order of the work package, and the values of the legacy story are kept character for character; the legacy level "System" maps to "End to end", and the Access, Resilience and Principle 5 cases map to "Component". The four added cases are this story's and test only the S2 deliverable; the business outcome of the engine is proved by the sixteen legacy cases as they are written in `RWB-P5-E2026-APP`. The fakes of section 12.8 stand behind every case. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The `-ITG` copies of these cases belong to the wave 2 integration harness and are not listed here.

### 17. Guardrails

- No value that a business person may change is written in code: the template codes, the type mapping, the languages, the formats, the template bound and the decision code are values in force read with their version (BR8; the lists and the bound are template data and parameters, read through DP-06 and DP-07).
- No personal data in logs, tests, workflow inputs or prompts: the request, the row, the record, the event and the logs carry case IDs, treatment IDs, document IDs, codes, dates, amounts and versions only, and the profile codec is on every payload (CTL-11; ASM-3081; AC8).
- No read of another module's tables: the documents come through the contract, the templates through the catalogue owner's answer, and `rwb_treatment` holds no foreign key into another schema (DP-01, BR9).
- ACE data only through the owner's contract or the `v_ace_*` views: this story reads no ACE view and calls no ACE interface, and the values it supplies are its own row's (DP-05).
- The document body, the file, the e-signature and the retention are never touched here: this story carries a reference and a version and no byte (BR9).
- The decision record is written in the same transaction as the reference, the version and the outbox row, and a failed write rolls the whole call back with MSG-P7-003 (DP-03, BR5).
- The central ledger is never written or read here: `decision_log_entry` belongs to P7 and is reached only through the shared topic.
- An applied migration is never edited: a correction to the two columns is a new version on the service sequence (DP-15).
- No right is re-implemented: the capability area and the right are declared and the guard library answers; the Documents C check on the generation is the document service's.
- One event only: this module declares `rwb.treatment.ContractDocumentGenerated.v1` and no second event, and a build that adds another on this topic fails the review.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-012 | Contracts, credit applications and mortgage documents generated from approved templates with no re-keying | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence | R-DIL-14, R-DIL-16, R-UNI-39, R-UNI-40 | TC-E2-026-01, TC-E2-026-02, TC-E2-026-06 to TC-E2-026-16, TC-S2-E2026-APP-01 to TC-S2-E2026-APP-04 |
| REQ-OCC-002 | Letter templates versioned, with the Legal approval recorded against the version | Business Requirements Program, section 5.6; Epic 2, section 3.5 | FEAT-OCC-07 | 13 Manage documents and correspondence | R-LIT-03, R-LIT-04, R-LIT-06, R-UNI-38 | TC-E2-026-03 to TC-E2-026-05, TC-E2-026-11, TC-S2-E2026-APP-01, TC-S2-E2026-APP-02 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P5-E2026-CON | Contract | C: declares the generate operation, `GenerateRequest`, `GenerationResult`, the `Document` shape, the error set, the `Idempotency-Key` rule and the fakes this story builds against |
| RWB-P5-E2026-APP | App development | The primary slice of the legacy key: the generation engine, the renderer, the resolver, the store call and the fourteen legacy criteria |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library the reference is written through in the same transaction (DP-03) |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON | Contract | H: the parameters and reference-data client libraries (DP-06, DP-07) |
| RWB-PLT-TE006-CON | Contract | H: the outbox and inbox library and the CloudEvents envelope (DP-09) |
| RWB-PLT-E1044-CON | Contract | H: the per-service Flyway sequence the two columns ride on (DP-15) |
| RWB-PLT-N001-CON | Contract | H: the gateway-bff composite route that serves SCR-14 and SCR-15 (DP-19) |
| RWB-S2-E3001-APP to RWB-S2-E3005-APP | App development | Siblings: the treatment row, the offer, the approval below the floor, the plan and the affordability pre-assessment |
| RWB-P6-E2026-APP, RWB-P6-E1046-APP | App development | P6 rwb-comms: the template catalogue, the merge fields and the Legal approval of a version |
| P3 rwb-case | App development | The parent `CaseWorkflow`, the case status and the parameters and lists this story reads through their contracts |
| P7 rwb-decision | App development | The DEEDINLIEU and RESTRUCTURE packages and the central ledger |
| RWB-ITG-E2026-ITG | Integration | The cross-service proof of the same values across rwb-treatment and rwb-document, held by the wave 2 harness |

### 19. Out of scope

- The generation engine, the template selection, the merge-field resolution, the value formatting, the renderer, the PDF/A-2b body, the draft files and the store call: RWB-P5-E2026-APP and RWB-P5-E2026-CON.
- The published shape of the generate operation, its resources, its error set, its `Idempotency-Key` rule and its fakes: RWB-P5-E2026-CON.
- The templates, the merge-field definitions, the template versions and the Legal approval of a version: P6 rwb-comms and RWB-P6-E1046-APP.
- The generation, review and send screens, the overrides form and the regenerate operation: RWB-P5-E2017-APP and RWB-P5-E2017-CON.
- The e-signature flow: RWB-P5-E2018-APP. The file custody and the retention run: P5 rwb-document.
- The offer, the settlement terms, the deed in lieu readiness and the approval below the floor: RWB-S2-E3002-APP, RWB-S2-E3003-APP and RWB-S2-E3005-APP.
- The TDR plan, its installments and its plan timers, which supply the installments, the interest rate and the first due date this story reads: RWB-S2-E3004-APP.
- The case status, the `CaseWorkflow`, the case table and the case signal: rwb-case (P3).
- The DEEDINLIEU and RESTRUCTURE packages, their rows and their versions, and the central decision ledger: rwb-decision (P7).
- The rights, the roles and the scope data, and the guard library that answers them: rwb-access (P4) and the platform library stories.
- The gateway-bff composite route, the screen field list and the layout: the platform edge story and the screen owners (DP-19).
- The real cross-service proof of the same values across rwb-treatment and rwb-document, and the live catalogue: the wave 2 integration harness.
- The deployment of this build: chart values, the queue and topic provisioning, the flag, dashboards and the runbook.

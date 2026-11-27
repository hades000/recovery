# RWB-S2-E2025-APP Extraction for the stage 2 and 3 document types

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the S2 treatment slice of legacy RWB-E2-025 is split out of the document hub key. The stage becomes `TreatmentWorkflow`, the child of `CaseWorkflow` on task queue `rwb-treatment`, and gains the `applyDocumentFacts` activity; the confirmed checked fields of the `CONTRACT`, `CREDIT_APPROVAL` and `MORTGAGE_DOCUMENT` types are consumed from the published contract RWB-P5-E2025-CON on one hop with a 2 s timeout, kept only in state `OK`, `CONFIRMED` or `CORRECTED`, and written on this service's own row in `rwb_treatment` in one transaction, idempotent on the document ID, the `doc_version` and the type-table version; the read is masked for a role without the right and the type-table version is stamped on the row; the base becomes `/api/recovery/treatment/v1` (DP-13) and SCR-14 and SCR-15 are reached through the gateway-bff composite route (DP-19). The eleven legacy acceptance criteria stay with RWB-P5-E2025-APP; this slice writes eight criteria of its own. The open points are the two gaps GAP-2702 and GAP-2703 and the seven assumptions ASM-4478 to ASM-4483. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S2-E2025-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (31 resolved, 33 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E2025-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-025 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Approval status | Draft (realignment v1); no sign-off of this story, the FSD or the TSD is recorded, treated as an assumption (GAP-1905) |
| Size | Set by the squad at refinement |
| Patterns applied | DP01, DP06, DP07, DP11, DP13, DP19 |
| Pattern boundary | No outbox producer, no inbox consumer, no event and no Schedule in this slice; a build that adds one fails the boundary test (DP-09, DP-10; GAP-1899) |
| Parallel lane | L-S2-H |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E2025-CON |
| Contract version | v1 (the /v1 paths of RWB-P5-E2025-CON in section 12.2) |
| Integration dependencies | None |
| Pattern dependencies (DP-added) | H RWB-PLT-E1027-CON; H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON; H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON; H RWB-PLT-TE006-CON; H RWB-PLT-E1071-CON; H RWB-PLT-N001-CON |
| Checked-field transport | One REST hop to RWB-P5-E2025-CON on the /v1 path with a 2 s timeout, a breaker and no retry chain; the Temporal cell of architecture v5 slide 13 is an open amendment to the architecture review |
| Treatment fact columns | contract_amount, contract_date, mortgage_amount, registration_date, land_office and title_doc_no added to rwb_treatment on the service's own Flyway sequence (types Not specified in the source documents (GAP-2702; ASM-4478)); source_document_id, source_doc_version and table_version beside them; the table version of the reader's answer is stamped in the same transaction; party_names stays masked and is stored nowhere |
| Field-code mapping | A code maps onto a column only when the names match; filing_date maps to filed_date as one recorded name difference; contract, credit-approval and mortgage codes, party_names, notice_date, hearing_type and lawsuit_no stay unmapped and are recorded as the difference |
| Apply write key and calls | Write key derived from the treatment, the document type, the document versions and the values; route field list and merge order left to RWB-PLT-N001-CON; parameter and list calls from RWB-P3-E1042-CON and RWB-P3-E1043-CON |
| Build-time fakes | Fakes of RWB-PLT-E1042-CON, RWB-PLT-E1043-CON and RWB-PLT-N001-CON, and of RWB-P3-E1042-CON and RWB-P3-E1043-CON, replaced when published in the same iteration; RWB-PLT-TE006-CON and RWB-PLT-E1071-CON are not used by this slice |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to REQ-DCM-006, REQ-DCM-005, REQ-DCM-017, REQ-DCM-018) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the confirmed fields that rwb-document extracted from the stage 2 and 3 document types — the contract, the credit approval and the mortgage document — applied by `TreatmentWorkflow` to the treatment record of the case in rwb-treatment, through the published checked-field contract RWB-P5-E2025-CON and without opening a document, a field row, a type row or a parameter table myself**, so that **the treatment record carries the contract amount, the contract date and the mortgage registration facts from the paper the officer already holds, so that the value a case is worked on is not retyped and never one that no person has checked and no rule has passed**.

This document is the S2 treatment slice of legacy RWB-E2-025. It owns no legacy criterion: the eleven criteria AC1 to AC11 of the story master are the document hub's and are owned by `RWB-P5-E2025-APP`, which keeps the classification, the extraction, the evaluation runner, the review queue and the write-once rule word for word, and the shapes, the path, the state filter, the masking rule and the fakes of the reader are owned by the contract `RWB-P5-E2025-CON`. The cross-service journey of the same values across rwb-document, rwb-treatment and rwb-case is the integration harness's. What this story owns is the S2 deliverable of the title: the application of the checked fields to its own row, the withholding of a field in review, the type and parameter reads at their version, the idempotent write, the refusal it passes through, the masking it never breaks and the read model of the two treatment screens. Its criteria are therefore new under D-RCV-60 and test only that deliverable.

The legacy story says what this slice is in its flow step 9: "S4 and S2 modules: read confirmed field values through DocumentFieldReader to fill the pack and the treatment record (from Epic 3 and Epic 5)". Its out-of-scope list says the complementary half just as plainly: "Writing extracted values into legal_action, hearing or treatment (S4 in Epic 5, S2 in Epic 3)". That write is this story, and it is the only business write it makes.

Four facts shape the slice.

1. **The reader is a contract, not a table.** Legacy `DocumentFieldReader.checkedFields(UUID caseId, String documentType)` returned `List<CheckedField>` in process, inside one module. In the target, rwb-document publishes that read on its own service base and this service consumes it, one hop, with a 2 s timeout and a breaker (DP-11; ADR-020). The `CheckedField` shape is `documentId, docVersion, fieldName, value, state (OK, CONFIRMED, CORRECTED), confidence`, and the read returns only fields in those three states. The operation, its path under `/api/recovery/document/v1` and its field-level element names are the baseline's and are recorded as named by no source (GAP-2702; ASM-4478).
2. **S2 holds no document.** rwb-treatment reads no `document`, `document_field`, `document_type` or `document_hub_parameter` row and no `v_ace_*` view: those tables are rwb-document's in `rwb_document` and the thirty `recovery.v_ace_*` views are read by rwb-source-data alone (DP-01, DP-05; Architecture v5 slide 8). The `rwb_treatment` login holds no grant on `rwb_document` and no `v_ace_*` grant (Architecture v5 slide 8), so the boundary is enforced by the database and not only by review.
3. **Only checked values move.** A field in state `REVIEW`, a field of a type that is not in the version in force and a value whose extraction confidence is below the pass mark are never promoted here. The treatment row keeps the value it already holds, the fact set it needs stays reported open with its review reason, and the officer is sent to the review queue of the hub.
4. **The values are data with a version.** The type and field codes, the field threshold and the accuracy pass mark are rows read at their version: the type version arrives as `tableVersion` on the reader's answer, the threshold and the pass mark come from the parameters contract of rwb-case, and the type list from its reference-data contract (DP-06, DP-07). Nothing of them is a constant of this module.

Two patterns in the metadata list apply here as prohibitions and are stated as such in section 13. DP-09 is the outbox and inbox library, and this story publishes and consumes no event: the extraction event of the hub is rwb-document's and this story carries no integration dependency on it, while the one event of this service, `TreatmentApproved`, belongs to the approval story (TSD S2 T5.3; EV-10 in the context pack). DP-10 is a Temporal Schedule or an event-started workflow, and this story registers no Schedule: the document intake job JOB-12 (legacy RWB-E2-025 section 4) and the monthly retention run JOB-17 are rwb-document's. Both rows are in the pattern list and neither has an application in this slice; no event and no Schedule is invented to fill them.

It does not own: the classification, the extraction, the review queue, the document type table and its version, the extractor versions and every `rwb_document` row, which are `RWB-P5-E2025-APP`'s and `RWB-P5-E2025-CON`'s; the treatment create, offer, approval, plan and affordability stories, which are `RWB-S2-E3001-APP` to `RWB-S2-E3005-APP`; the case status and the `CaseWorkflow` parent, which are rwb-case's (P3); the RESTRUCTURE, SETTLEMENT and DEEDINLIEU packages and their rows, which are rwb-decision's (P7); the roles, rights and scope data, which are rwb-access's (P4); the gateway-bff composite route and the screen field list, which are the platform edge story's and the screen owners'.

### 2. Business rationale

A treatment record is the row the whole restructure, settlement and deed-in-lieu stage is worked on: the offer is built against it, the approval level is looked up from it and the plan is booked from it. Today the officer types its baseline facts from paper — the contract amount and the day it was signed, and the mortgage document that secures it — and two people reading the same contract produce two different amounts. The legacy story measured the gap on the document side and on the treatment side at once: the litigation pack and the treatment record need the contract amount and the mortgage registration, and officers read them from paper and type them in (legacy RWB-E2-025 section 2).

The document hub now extracts those values. Legacy RWB-E2-025 extended classification and extraction to five new types — `CONTRACT`, `CREDIT_APPROVAL`, `MORTGAGE_DOCUMENT`, `COURT_FILING` and `JUDGMENT` — with `contract_no`, `party_names`, `contract_amount`, `contract_date`, `approval_no`, `approved_amount`, `approval_date`, `approval_level`, `title_doc_no`, `mortgage_amount`, `registration_date` and `land_office` among the fields of the three types this slice consumes, in the type table version `DOCTYPE-2026.12` valid from `2026-12-31`, with a field threshold of `0.80` and an accuracy pass mark of `0.90`. That half is `RWB-P5-E2025-APP`, and this story does not repeat it, restate it or test it.

What the hub cannot do is write the treatment. The treatment, its contract amounts and its mortgage facts are rwb-treatment's: the service owns treatments, contracts, settlement and deed-in-lieu agreements and plan timers, in schema `rwb_treatment` (Architecture v5 slide 4 places TDR, settlement and DIL with S2; `treatment` is the one table of the service in the context pack and the Ownership Map). So the value leaves the hub once, on a published read, and lands on the row of the service that owns the fact. That is the whole of this slice, and it is why the story is a consumer and never a reader: the moment rwb-treatment reads `document_field` for itself, two services own one extraction and the state filter of the reader can be bypassed by a query.

Three consequences follow, and each is designed rather than left to discipline.

- **The stage, not the screen, applies the facts.** The legacy reader was called by the module that needed the values. In the target the caller is `applyDocumentFacts`, an activity of `TreatmentWorkflow` on task queue `rwb-treatment`, started by the case signal the parent `CaseWorkflow` forwards (Architecture v5 slide 13, row P3 Case with T and E into S2 Treatment; Temporal and Drools Design slides 9 and 11). The activity runs inside the stage, so a replay reuses the recorded result and a retry repeats nothing that completed.
- **A withheld value keeps the row as it is.** The reader returns no `REVIEW` field, and this service additionally drops any entry the reader returns in another state and any value below the pass mark. The treatment row therefore keeps the amount it already holds, the fact set is reported open with the review reason the hub gives — `LOW_CONFIDENCE` for a field below the threshold and `UNKNOWN_TYPE` for a document that arrived before the type version took effect — and the officer is sent to the review queue of the hub, which is where a person may accept or correct the value. This service has no review screen and no override of its own, and it never clears a column because one read came back short.
- **The write is a write of facts, not a case move.** Applying a contract amount does not move the case to `PROPOSED_IN_COLLINS` and does not open, send or approve an offer: R-RES-01, R-RES-10 and the offer and approval rows are the stage stories' of this epic, and the case status is moved by the parent `CaseWorkflow` alone (FSD S2 A2.1.3.1; TSD S2 T4). This story supplies the facts those rows read.

It serves REQ-DCM-006 ("fields are extracted into the index for the agreed document types, in Thai and in English") on the treatment side and REQ-DCM-005 ("classified with a confidence; below the threshold to the review queue") as the consumer of its outcome: the record that receives the value is the treatment, and the review path is the hub's. It puts control CTL-08 in place on the reading side — a proposal below the pass mark takes effect only when it is loaded, so no value is promoted here from a package that is not in force — and CTL-11 and CTL-12 by construction: a personal value is never stored and a write-once document is never touched, because no document is written at all. It carries R-UNI-38: a value is applied under the version in force on the date it is read.

### 3. Preconditions

- RWB-P5-E2025-CON is published: the checked-fields read on base `/api/recovery/document/v1`, the `CheckedField` and `CheckedFieldSet` shapes, the state filter (OK, CONFIRMED and CORRECTED only), the masking rule, the error envelope with its message IDs and statuses, and the contract fake. The operation, its path and its field-level names are the baseline's own and are Not specified in the source documents (GAP-2702; ASM-4478); this story builds against the contract and its fake on Day 1 and never against a document table.
- `treatment` exists in `rwb_treatment` from `RWB-S2-E3001-APP`, with the columns of TSD S2 T3.1 — DF-TRT-001 to DF-TRT-033 — the standard record columns of T3.0 and the lists of T3.2 (LOV-TREATMENT, LOV-PROPOSER, LOV-TRT-OUTCOME, LOV-APPROVAL-LEVEL, LOV-CREDIT-RESULT, LOV-TRT-SIGNATURE). This story adds the fact columns of section 11 to that table on the service's own Flyway sequence and creates no other table.
- A treatment row of the case exists, or the stage has just opened it through `RWB-S2-E3001-APP`; the apply writes the row of the case and never opens a second treatment for the same case and stage.
- The field threshold and the accuracy pass mark are read at their version through the parameters contract of rwb-case (DP-06, C `RWB-P3-E1042-CON`); the parameter codes are the hub's own (`EXTRACT_ACCURACY_PASS` and the field threshold of the extraction contract) and the operation names this story reads are Not specified in the source documents (GAP-2702; ASM-4478).
- The type list LOV-DOC-TYPE with the eleven types is read at its version through the reference-data contract of rwb-case (DP-07, C `RWB-P3-E1043-CON`); the type codes themselves arrive on the reader's answer and the list is used only to name the three types this slice consumes.
- The platform parameter and reference-data libraries (H `RWB-PLT-E1042-CON`, H `RWB-PLT-E1043-CON`), the outbox and inbox library (H `RWB-PLT-TE006-CON`), the workflow kit (H `RWB-PLT-E1071-CON`) and the gateway-bff composite route (H `RWB-PLT-N001-CON`) are named by the pattern table and stand in no build row of this story's plan; the service template carries them and the story builds against their fakes until they publish (ASM-4481). The outbox producer and the workflow kit's Schedule are not used at all by this slice (ASM-4482).
- The service runs as login `rwb_treatment` on schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.treatment`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant (Architecture v5 slide 8, one login and connection pool per service; DP-02).
- The caller holds a Workbench role with the Treatment and offer right of TSD S2 T6.1 — RW-RESTRUCT holds CRUA and RW-CASEOWN, RW-SPECIAL and RW-GUARANT hold CRU — and the reader is called with a role that carries Documents R on the document side; the refusal and the masking of the read are the P5 contract's and this story adds no right of its own (AC6, AC7).
- The gateway-bff composite route serves SCR-14 Treatment record and SCR-15 Settlement offer, both listed with the treatment stage of this epic; the read model is built and proved against the route fake until the route publishes (ASM-3076).
- The release date 31 December 2026 is the legacy one and is tentative, and the story stands Draft (realignment v1) until the realignment is approved; no approval is a precondition of the build.

### 4. Flow

1. The case reaches the treatment stage: the route decision of rwb-valuation ends with the case in `ROUTE_APPROVED_RESTRUCTURE`, `ROUTE_APPROVED_SETTLEMENT` or `ROUTE_APPROVED_DIL`, the case router of rwb-case signals `CaseWorkflow`, and the parent starts `TreatmentWorkflow` as a child on task queue `rwb-treatment` (Architecture v5 slides 3 and 13; Temporal and Drools Design slide 9).
2. The stage opens or reads the treatment row of the case through `RWB-S2-E3001-APP`'s `openTreatment` activity, and the case signal it holds names the case and the business date.
3. `TreatmentWorkflow` calls `applyDocumentFacts` for the types of this slice — `CONTRACT`, `CREDIT_APPROVAL` and `MORTGAGE_DOCUMENT` — with the case ID, the treatment ID and the identity of the caller the stage is working for.
4. `CheckedFieldClient` calls the checked-fields read of `RWB-P5-E2025-CON` once per type, one hop, with a 2 s timeout and a breaker, with no retry chain and no second downstream call; the operation name and path are the contract's (GAP-2702; ASM-4478).
5. `CheckedFieldFilter` keeps only the entries in state `OK`, `CONFIRMED` or `CORRECTED` and drops every other entry and every value below the accuracy pass mark, so a value in `REVIEW` cannot be applied even if a future contract version returned it.
6. `Stage23TreatmentMapper` maps each kept field code onto the treatment column of the same name in this service's own set: `contract_amount`, `contract_date`, `mortgage_amount`, `registration_date`, `land_office` and `title_doc_no`. A code with no column of the same name is not mapped and the difference is recorded (GAP-2702; ASM-4478).
7. `Stage23VersionGuard` checks the `tableVersion` the reader reports against the version the reference-data contract reports in force, and checks that the threshold and the pass mark it applies are the ones the parameters contract answers at their version (DP-06, DP-07).
8. `TreatmentFactWriter` writes, in one `rwb_treatment` transaction, the mapped columns of the `treatment` row, the source identifier of each contributing entry — `documentId`, `docVersion` and the type-table version — and the idempotency row of the request. The outbox row set is empty and no other service's row is touched (DP-01, DP-09).
9. `Stage23Idempotency` builds the write key from the document ID, the `doc_version` and the type-table version of each contributing entry, recognises a repeat of the same key and answers from the first result; a repeated read writes nothing at all (AC5).
10. The activity returns to the workflow the facts it applied, the version they were applied under, the entries it withheld with their review reasons and the outcome of each read; the workflow records the result in its history and waits on the next signal.
11. The officer reads the treatment through `GET /api/recovery/treatment/v1/treatments/{treatmentId}` (API-S2-002): the fact columns, the document version each fact came from and the open items are answered from `rwb_treatment`, and the checked fields themselves are shown on the hub's own surfaces, read only.
12. SCR-14 Treatment record and SCR-15 Settlement offer read the treatment through the gateway-bff composite route, which composes the case read of rwb-case with the treatment read of this service, one hop each, read only (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A field of the requested type is in state `REVIEW` in the hub | The field is not applied and the column keeps the value it holds; the fact set is reported open with its review reason and the officer is sent to the review queue of the hub | MSG-P5-003 | AC2 |
| X2 | A value arrives with an extraction confidence below the pass mark | The value is not promoted by this service, whatever state the entry carries, and the fact set is reported open | MSG-P5-003 | AC2 |
| X3 | The document arrived before the type version took effect, or the classifier could not place it, so the item carries `UNKNOWN_TYPE` | No field is applied, the treatment row is unchanged, and the item stays in review with its reason | MSG-P5-003 | AC3 |
| X4 | The checked-fields read does not answer inside 2 s, or its breaker is open | Nothing is written; the activity fails with 503 and the platform envelope, and it is retried on the platform policy of 1 s initial interval, back-off 2 and 10 attempts | MSG-GEN-006 | AC6 |
| X5 | The caller's role carries no Documents R on the document read | The reader refuses before returning a value; this service writes nothing and adds no right of its own | MSG-P4-002 | AC6, AC7 |
| X6 | The document or the case lies outside the caller's scope | The reader answers 404 and this service writes nothing; the caller cannot tell an out-of-scope document from a missing one | MSG-P4-003 | AC6 |
| X7 | The same read is repeated for the same document ID, `doc_version` and type-table version | No column changes; the repeat is answered from the first result and counted | None | AC5 |
| X8 | A field code has no treatment column of the same name — `contract_no`, `party_names`, `approval_no`, `approved_amount`, `approval_date`, `approval_level` | Nothing is written for that code; the value stays in the hub and the difference is recorded with its assumption (GAP-2702; ASM-4478) | None | AC1 |
| X9 | The treatment named by the stage does not exist, does not belong to the case, or is not in a state that accepts facts | The activity fails with 404 or 409 and nothing is read further; no partial fact set is written | None | AC5 |
| X10 | A component, a statement or a test reaches a `rwb_document` table, a `document_type` row, a `document_hub_parameter` row or a `v_ace_*` view | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC9, AC12; Section 8, BR9 |

X1 to X3 are the withholding paths the reader's state filter implies; X4 to X6 are the three refusals of the published read; X7 is the idempotency of the apply; X8 is the mapping difference between the extracted codes and the treatment columns; X9 is the row the stage names; X10 is the schema boundary. A refusal under X4, X5 or X6 writes nothing at all, because the filter, the guard and the mapping run before the transaction opens, and the activity is retried only under the platform policy of ADR-020 and not with a retry chain of its own.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 against `RWB-P5-E2025-CON` and its fake; the parameter, reference-data, outbox and composite-route contracts are fakes until their stories publish (ASM-4481) |
| Negotiable | The type and field codes, the threshold, the pass mark and the table version are rows read at their version; the story fixes the behaviour, not the values, and the mapping is limited to names the sources share |
| Valuable | The officer stops retyping the contract amount, the contract date and the mortgage registration from paper, and a value no person checked never reaches the treatment |
| Estimable | One activity, one client, one filter, one mapper, one version guard, one writer, one idempotency guard and one read model |
| Small | Fits two weeks with its tests, as a secondary slice of the legacy key |
| Testable | Each of the eight criteria of section 7 is one automated test; every cross-service answer is stubbed in the contract fakes |

### 7. Acceptance criteria

```gherkin
Feature: Extraction for the stage 2 and 3 document types — the rwb-treatment fill

  Background:
    Given the document type table version "DOCTYPE-2026.12" is in force from 2026-12-31
    Given the field threshold is 0.80 and the accuracy pass mark is 0.90
    Given the rwb-document contract mock returns the checked fields of the case and the type it is asked for
    Given the rwb-case parameters mock returns the field threshold and the accuracy pass mark at their version in force

  Scenario: AC1 The confirmed contract and mortgage facts reach the treatment row (new, D-RCV-60)
    Given the rwb-document contract mock returns for case "RW-2026-000601" and type "CONTRACT" the checked fields contract_amount "2400000.00" and contract_date "2026-11-01" in state "CONFIRMED"
    And it returns for the same case and type "MORTGAGE_DOCUMENT" the checked fields mortgage_amount "2400000.00" and registration_date "2026-11-01" in state "OK"
    When "TREAT-01" applies the checked fields of types "CONTRACT", "CREDIT_APPROVAL" and "MORTGAGE_DOCUMENT" to the treatment row of case "RW-2026-000601"
    Then the treatment row holds contract_amount 2400000.00, contract_date 2026-11-01, mortgage_amount 2400000.00 and registration_date 2026-11-01
    Then the fact columns, the source identifiers of each contributing entry and the idempotency row are written in one transaction, and no other column of the row changes
    Then every value written is the one the reader returned with its state, and this service promotes no value the reader did not return

  Scenario: AC2 A field in review is withheld and the previous value is kept (new, D-RCV-60)
    Given the rwb-document contract mock returns for case "RW-2026-000601" and type "CONTRACT" the checked field contract_amount of contract "DOC-0601" in state "REVIEW" with confidence 0.7100, below the field threshold 0.80
    And the treatment row of case "RW-2026-000601" already holds contract_amount 2400000.00 from the confirmed read of the same field
    When "TREAT-01" applies the checked fields of type "CONTRACT" to the treatment row
    Then contract_amount is not written, the row keeps 2400000.00, and no other column of the row changes
    Then the contract fact set is reported open with its review reason and contract "DOC-0601" shows MSG-P5-003
    Then this service promotes no value in a state other than OK, CONFIRMED or CORRECTED and no value below the accuracy pass mark 0.90

  Scenario: AC3 An unknown type or a document before the version in force applies nothing (new, D-RCV-60)
    Given credit approval "DOC-0602" of case "RW-2026-000601" was received on 2026-12-26, before the valid-from date of "DOCTYPE-2026.12"
    Given the rwb-document contract mock returns no checked field for case "RW-2026-000601" and type "CREDIT_APPROVAL" and reports the item in review with reason "UNKNOWN_TYPE"
    When "TREAT-01" applies the checked fields of type "CREDIT_APPROVAL" to the treatment row
    Then no column of the treatment row changes and no credit-approval fact is written
    Then the item stays in the review queue with reason "UNKNOWN_TYPE" and the treatment read reports it open
    Then this service reads no type table, classifies nothing and re-types no document

  Scenario: AC4 The type and field set, the threshold and the pass mark are read at their version (new, D-RCV-60)
    Given the rwb-case parameters contract mock returns the field threshold 0.80 and the accuracy pass mark 0.90 at the version in force
    And the rwb-case reference-data contract mock returns LOV-DOC-TYPE with the eleven types, including CONTRACT, CREDIT_APPROVAL and MORTGAGE_DOCUMENT
    When the rwb-document contract mock answers with a checked-field set carrying tableVersion "DOCTYPE-2026.12" and the fields of type "MORTGAGE_DOCUMENT"
    Then the type code, the field codes and the table version are taken from the reader's answer and the threshold and the pass mark from the parameters answer
    Then the treatment row carries "DOCTYPE-2026.12", the table version of the answer it was written from
    Then no type code, field code, threshold, pass mark, table version or valid-from date appears in the Java source or the module configuration
    Then this service writes no document, document_field, document_type or document_hub_parameter row and reads no v_ace_* view

  Scenario: AC5 A repeated read applies once (new, D-RCV-60)
    Given the treatment row of case "RW-2026-000601" holds contract_amount 2400000.00 and contract_date 2026-11-01 from contract "DOC-0601" at doc_version 1 and table version "DOCTYPE-2026.12"
    When the same read of the same types is applied a second time for the same document ID, the same doc_version and the same table version
    Then no column of the treatment row changes and the applied set of the row still names one document version and one table version
    Then the second answer is the first result and the repeat is counted
    Then a read that returns the same values with a new doc_version writes the row once more and records the new version

  Scenario: AC6 A refusal of the reader changes nothing here and the activity retries (new, D-RCV-60)
    Given the rwb-document contract mock refuses the read for case "RW-2026-000605" of team "LIT-NE" with status 404 and MSG-P4-003
    When "TREAT-01", an officer of team "LIT-BKK", applies the checked fields to the treatment row of case "RW-2026-000605"
    Then the answer is status 404 with MSG-P4-003, no column of the treatment row changes, and no partial field set is written
    Given the rwb-document contract mock refuses the read for a role that carries no Documents R with status 403 and MSG-P4-002
    When the same apply is requested
    Then the answer is status 403 with MSG-P4-002 and nothing changes
    Given the rwb-document contract mock does not answer inside 2 s
    When the activity runs
    Then the answer is status 503 with MSG-GEN-006 and nothing is written
    Then the activity is retried on the platform policy of 1 s initial interval, back-off 2 and 10 attempts, and the repeat never writes twice

  Scenario: AC7 The party names of a contract are masked for a role without the right (new, D-RCV-60)
    Given the rwb-document contract mock returns for case "RW-2026-000601" and type "CONTRACT" the field party_names masked for a role that carries no Documents R
    When "TREAT-02", a role of team "LIT-BKK" without that right, reads the treatment through GET /api/recovery/treatment/v1/treatments/{treatmentId}
    Then the party names show masked as rwb-document returned them and the treatment row holds no party name
    Then the masked value appears in no log line, no event payload and no workflow input
    Then the contract amount and the contract date are shown, because neither carries a personal value

  Scenario: AC8 The applied facts show on SCR-14 and SCR-15 through the composite route (new, D-RCV-60)
    Given the gateway-bff composite route serves SCR-14 Treatment record and SCR-15 Settlement offer for case "RW-2026-000601"
    And the treatment row of case "RW-2026-000601" holds contract_amount 2400000.00, contract_date 2026-11-01 and the mortgage registration facts
    When "TREAT-01" opens SCR-14 and SCR-15
    Then SCR-14 shows contract_amount, contract_date and registration_date read from this service, with the document ID and doc_version of each fact; the values are Not specified in the source documents (ACR-RWB-S2-E2025-APP-AC8)
    Then SCR-15 shows contract_amount as the baseline of the offer it builds on, read only; the value is Not specified in the source documents (ACR-RWB-S2-E2025-APP-AC8)
    Then SCR-14 and SCR-15 show empty, loading, error and no-access states Not specified in the source documents (CG-ALL-8402; CG-ALL-8403)
    Then the party names show masked and no screen calls an owner service directly

  Scenario: AC9 A statement that reaches a document table is refused and fails the build (new, D-RCV-60)
    Given a component, a statement or a test of this module names a table of rwb_document, a document_type row, a document_hub_parameter row or a v_ace_* view
    When the boundary test runs in the build
    Then the grant refuses the statement and the boundary test fails the build
    Then nothing is released

  Scenario: AC12 A statement from the rwb_treatment login that reaches a document table is refused by the grant (new, D-RCV-60)
    Given the rwb_treatment login names a rwb_document table, a document_type row, a document_hub_parameter row or a v_ace_* view in a statement
    When the statement runs against the database
    Then the grant refuses the statement and the boundary test fails the build
    Then no row is returned, no column is read and nothing is released

  Scenario: AC13 The section 8 rules hold in the module build (new, D-RCV-60)
    Given the source and configuration of the rwb-treatment module are built
    When the build check and the boundary test run
    Then BR1, BR4, BR6, BR8 and BR12 hold: no type code, field code, pattern, threshold, pass mark, file or era conversion is written in the module, and every value is read at its version
    Then BR9 and BR10 hold: the login holds no grant on a document table and no case-state, offer or approval call exists in the module
    Then BR11 holds: a repeated read writes once and never clears a column

  Scenario: AC14 A request without a valid identity is answered 401 (new, D-RCV-60)
    Given a request to GET /api/recovery/treatment/v1/treatments/{treatmentId} carries no valid identity
    When the request is sent
    Then the answer is status 401 and no treatment field is read or returned

  Scenario: AC15 A treatment not in a state that accepts facts refuses the apply (new, D-RCV-60)
    Given the treatment named by the stage of the case is not in a state that accepts facts
    When "TREAT-01" applies the checked fields to that treatment row
    Then the activity fails with status 409, no partial fact set is written and no column changes
```

The thirteen criteria are new under D-RCV-60 and test only the S2 deliverable of this story: the application of confirmed checked fields to the treatment row, the withholding of a field in review and the value the row keeps, the version and parameter reads, the idempotent write, the refusal it passes through with the retry the platform policy gives, the masking it never breaks and the read model of the two treatment screens. The eleven legacy criteria AC1 to AC11 of RWB-E2-025 — the court notice, the contract, the low confidence, the pass-mark proposal, the classification, the document before the version, the Buddhist Era date, the pattern mismatch, the reader filter, the write-once file and the scope refusal — belong to `RWB-P5-E2025-APP`, are written there word for word with their origin tags, and are not restated here. The shapes, the path, the state filter and the fakes this story consumes are `RWB-P5-E2025-CON`'s. The cross-service journey of the same values across rwb-document, rwb-treatment and rwb-case is the wave 2 integration harness's, and no criterion of this story claims it.

Three readings of the sources are stated here rather than hidden in the code. The reader's transport, operation name and field-level names are Not specified in the source documents and come from `RWB-P5-E2025-CON`; the column of `treatment` that carries a fact and the column that carries the type-table version are this story's design and are named by no source (GAP-2702; ASM-4478). The masking rule the treatment read applies is the hub's for the value it returns, and which role may see an unmasked party name on the treatment side is named by no source for this service (GAP-2702; ASM-4478). The `registration_date "2026-11-01"` of AC1 is the contract date of the same fixture used as synthetic test data, and it is not a business value of any source. The one-hop REST read of the legacy in-process interface is the pattern table's (DP-11) and the architecture's REST rule, while the connection matrix of Architecture v5 slide 13 puts the S2 call to P5 in the Temporal column; the story follows the pattern table and the work package, and the disagreement is carried as GAP-2703 with ASM-4483.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The stage 2 and 3 types and their fields are those of the document type table version in force on the extraction date; the version is the one the reader reports and this service reads no type table of its own | Legacy RWB-E2-025 BR1; R-UNI-38; TSD S2 T3.1 (GAP-2702; ASM-4478) |
| BR2 | A field below the threshold, failing its pattern or marked review-only has state REVIEW in the hub and is never applied here; the fact set that needs it stays reported open with its review reason | Legacy RWB-E2-025 BR2; RWB-P5-E2025-CON state filter; MSG-P5-003 |
| BR3 | A value whose extraction confidence is below the accuracy pass mark is never promoted by this service, whatever state an upstream answer carries; the proposal of a review-only field takes effect only when its version is loaded | Legacy RWB-E2-025 BR3 and AC4; CTL-08; DL11 |
| BR4 | Each field may carry a pattern in the hub's field definitions; the pattern is data, and this service repeats none of it and validates no extracted value against a pattern of its own | Legacy RWB-E2-025 BR4; RWB-P5-E2025-CON |
| BR5 | Only fields in state OK, CONFIRMED or CORRECTED are used; a field in any other state is withheld and never written on `treatment` | Legacy RWB-E2-025 BR5; RWB-P5-E2025-CON |
| BR6 | Extraction never changes the stored file of a write-once document. This is the hub's rule; here it is a boundary, because this story writes no document and no file at all | Legacy RWB-E2-025 BR6; CTL-12; DP-01 |
| BR7 | Party names and other personal field values are masked unless the role may see them; a personal value is never stored on `treatment`, never logged and never put on an event | Legacy RWB-E2-025 BR7; DF-DOC-015; CTL-11; DL26 (GAP-2702; ASM-4480) |
| BR8 | Dates read in Buddhist Era are stored as ISO dates; the value applied to a date column is the ISO value the reader returns, and no era conversion is repeated here | Legacy RWB-E2-025 BR8; TSD S2 T3.1 |
| BR9 | This service reads no `document`, `document_field`, `document_type` or `document_hub_parameter` row and no `v_ace_*` view; the checked values arrive only on the published read of RWB-P5-E2025-CON, and the `rwb_treatment` login holds no grant that would allow otherwise | DP-01; Architecture v5 slide 8; the ownership rows of the S2 context pack and the Ownership Map (the four tables are P5's) |
| BR10 | The write is a write of facts: it moves no case status, opens no offer, approves nothing and writes no decision record, because no rule is evaluated by this slice | FSD S2 A2.1.3.1; TSD S2 T4; legacy RWB-E2-025 section 9 |
| BR11 | A repeated read of the same document ID, `doc_version` and type-table version writes once, and a repeated read never clears a column the row already holds | R-UNI-40; legacy RWB-E2-025 section 12 (idempotency); AC5 |
| BR12 | No value a business person may change is written in code: the types, the fields, the patterns, the threshold, the pass mark and the lists are rows read at their version | BR-S2-001; FSD S2 A2.1.3.1; legacy RWB-E2-025 BR4 |
| R-UNI-38 | A new rule version applies to decisions taken from its effective date, and an open case keeps the version it was decided under. Here the version in force is the table version the reader reports and the parameter values the contracts answer | Business Rules and Routing Logic v4 (R-UNI-38) |
| CTL-08 | A proposed change takes effect only when it is loaded. This story therefore promotes no threshold, no pass mark and no review-only proposal that is not in force at its version | Legacy RWB-E2-025 BR3; CTL-08; DL11 |
| CTL-11 | Personal data is masked for a role that may not see it and is not copied outside the system that owns it; a party name is never written to `rwb_treatment` | Legacy RWB-E2-025 BR7; CTL-11; DL26 |
| CTL-12 | A write-once document is never altered. It holds here by construction: this story touches no document and no file | Legacy RWB-E2-025 BR6; CTL-12 |

The open decisions DL10 (assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863), DL11 (assumptions ASM-0553, ASM-0703, ASM-1051, ASM-1104), DL19 (assumptions ASM-1051, ASM-1164, ASM-1809, ASM-1810) and DL26 (assumptions ASM-0247, ASM-0264, ASM-0275, ASM-0355) apply to the rules above. Each has its assumptions named here, and each decision is still open.

The rules hold in `rwb_treatment` as follows. BR1, BR3 and BR5 are executed by `CheckedFieldFilter` and `Stage23VersionGuard` before anything is written: the filter drops every entry that is not OK, CONFIRMED or CORRECTED and every value below the pass mark, and the guard compares the reported table version with the version the reference-data contract reports in force. BR2 and BR3 are visible to the officer as an open fact set with its review reason and as MSG-P5-003 on the document, not as a value on the treatment. BR4, BR6 and BR8 are prohibitions over this module: no pattern, no file and no era conversion exists in it, and a build check fails on a date literal, an amount literal, a threshold or a pass mark in the source. BR7 is asserted by a property test that places a synthetic party name in the reader's answer and proves it appears in no row, no log line and no span attribute. BR9 is the schema grant and the boundary test. BR10 is a build check on the module: no call to a case-state operation, no offer operation and no approval envelope. BR11 is the write key of `Stage23Idempotency` and the rule that a withholding read never nulls a column. BR12 is the reference-data and parameter reads.

### 9. State transitions

None. This story does not change a case status and does not move the lifecycle state of the treatment, which belongs to the stage stories.

Two things are written, and both are records rather than state machines:

| From | Event | Condition | To |
|---|---|---|---|
| A `treatment` row with no fact column set | The `applyDocumentFacts` activity | The case, the types and the caller are valid and the reader answers with kept entries | The same row with the fact columns, the source identifiers and the stamped type-table version |
| A `treatment` row with fact columns set | The `applyDocumentFacts` activity | A kept entry of a later `doc_version` arrives | The same row with the new value and the new source identifiers |
| A `treatment` row with fact columns set | The `applyDocumentFacts` activity | Every entry of the type is in `REVIEW`, below the pass mark, or the read reports `UNKNOWN_TYPE` | Unchanged, and every fact set is reported open with its reason |
| A `treatment` row and a document set already applied | The `applyDocumentFacts` activity | The same document ID, `doc_version` and type-table version | Unchanged; the first result is answered and the repeat is counted |

The field-state values are the hub's and not this story's: `OK`, `CONFIRMED` and `CORRECTED` are applied, `REVIEW` is withheld, and the move out of `REVIEW` happens in the review queue of the hub's own story. The case states of the stage — `PROPOSED_IN_COLLINS`, `IN_FCR_QUEUE`, `WITH_FCR_OFFICER`, `OFFER_WITH_CUSTOMER`, `AWAITING_CREDIT_APPROVAL`, `WITH_OPS_BOOKING`, `BOOKED_IN_ALS_NLEADS`, `PLAN_RUNNING` and their settlement and deed-in-lieu siblings (TSD S2 T4) — are moved by the parent `CaseWorkflow` and by the stage stories of this epic, and no state of them is written here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer (FCR) | Treatment and offer CRUA in the TSD S2 T6.1 matrix: works the stage, applies the checked fields of the three types on the case in scope, reads the facts and the open items |
| RW-CASEOWN, case owner | Treatment and offer CRU: applies and reads the same facts on the cases in scope |
| RW-SPECIAL, hardship and vulnerability specialist; RW-GUARANT, guarantee officer | Treatment and offer CRU: applies and reads the same facts in scope |
| RW-TEAMMGR, team manager | R: reads the facts and the open items of the team's cases |
| RW-CREDCOMM, credit approval committee member; RW-PRODHEAD, product head | RA: reads the credit-approval facts the stage compares its offer against; no approval is taken here |
| RW-LITOFF, litigation officer; RW-LEGAL, legal counsel | R: reads the contract and mortgage facts of a case they are working; the litigation fill is the S4 slice's |
| The other reading roles of TSD S2 T6.1 — RW-COMPLAIN, RW-FRAUD, RW-CONDUCT, RW-RISK, RW-COE, RW-AUDIT, RW-BIANAL, RW-TRIBE (R) | Read the applied facts of a case and the version they were applied under |
| SY-CASEWF, SY-RULES, SY-AGENT (R) | Read as service identities through the same checks; a service identity carries no Documents R unless the hub's contract grants it |
| rwb-treatment service identity (login `rwb_treatment`, DP-02) | Calls the checked-fields read with the caller's own identity, filters, maps, guards the version, writes `treatment` in `rwb_treatment`, and holds no grant on `rwb_document` or on a `v_ace_*` view |
| rwb-document (P5) service identity | Owns the documents, the fields, the type table and the review queue; serves the checked fields and the masking decision and is never written by this story |
| rwb-case (P3) service identity | Owns the parameters and the reference rows this story reads at their version; called as a contract and never read as a table |

The rights above are the rows of TSD S2 T6.1 and nothing wider. Every REST operation of this service calls the rwb-access authorise check (DP-08) with the caller's own identity before it reads or writes; a refused call is answered 403 and writes nothing. Four roles named by the legacy authority table are not exercised here because their rights are on the document side and not on the treatment record: SY-OCR, the extraction pipeline, holds Documents CRU and writes the fields the hub serves; RW-REFADM, the reference data administrator, loads the type table version and the parameter values; the business lead with Legal approves the type and field list under DL19; and RW-RESTRUCT's Documents CRU is exercised in the hub's screens, not on this row. This slice passes the reader the caller's own identity, so the hub's refusal and masking apply unchanged, and no credential and no personal name appears in the request, the row, the workflow input or the logs. Where a person must be named the row carries the user identifier, never a name.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment (S2, `rwb_treatment`) | id | Read as the row the facts are written on; written only when the stage opens the row |
| DF-TRT-002 | treatment (S2, `rwb_treatment`) | case_id | Read as the key of the read and of the write |
| DF-TRT-004 | treatment (S2, `rwb_treatment`) | treatment_type | Read to place the stage; never written by this slice |
| DF-TRT-013, DF-TRT-014 | treatment (S2, `rwb_treatment`) | outcome, outcome_at | Not written: the outcome of the treatment is the stage's and the plan stories' |
| DF-TRT-003, DF-TRT-005 to DF-TRT-012, DF-TRT-023 to DF-TRT-033 | treatment (S2, `rwb_treatment`) | the proposer, the terms, the approval, the booking, the credit result, the plan and the signature fields | Not written: they belong to `RWB-S2-E3001-APP` to `RWB-S2-E3005-APP` and are left exactly as those stories set them |
| No BR Field ID | treatment (S2, `rwb_treatment`) | `contract_amount`, `contract_date`, `mortgage_amount`, `registration_date`, `land_office`, `title_doc_no` | Write, from the field code of the same name of `CONTRACT` or `MORTGAGE_DOCUMENT`; the column names and their field IDs are this story's design and are Not specified in the source documents (GAP-2702; ASM-4478) |
| No BR Field ID | treatment (S2, `rwb_treatment`) | `source_document_id`, `source_doc_version`, `table_version` | Write, the identifiers and the type-table version of the entry each fact came from; the column names are Not specified in the source documents (GAP-2702; ASM-4478) |
| DF-DOC-001, DF-DOC-002, DF-DOC-004 | document (P5, `rwb_document`) | id, case_id, document_type | Read through the contract only, as the identifier and the type of each checked field; never from the table |
| DF-DOC-012 to DF-DOC-017 | document_field (P5, `rwb_document`) | id, document_id, field_name, field_value, confidence, confirmed_by | Read through the contract only, as `documentId`, `fieldName`, `value` and `confidence`; never from the table |
| DF-DOC-034, DF-DOC-035 | document_field (P5, `rwb_document`) | extracted_value, extractor_version | Read through the contract only, as the extracted value and the version of the extractor; never from the table |
| DF-DOC-015 | document_field (P5, `rwb_document`) | the personal field the party names ride on | Read through the contract only and never stored: a party name is masked or withheld and reaches no row, no log and no event |
| DF-REF-224, DF-REF-229 to DF-REF-231, DF-REF-233 | document_type (P5, `rwb_document`) | field_definitions, table_version, valid_from, valid_to, classify_threshold | Read through the contract only, as `tableVersion` on the answer; never from the table |
| DF-REF-246 and the parameter catalog | document_hub_parameter (P5) and parameter_catalog (P3) | param_value and the parameter row | Read through the parameters contract of rwb-case only, never from the table |
| Standard column | treatment (S2, `rwb_treatment`) | state, version, created_at, created_by, updated_at, updated_by | Write `updated_at`, `updated_by` and the optimistic `version` of the row; the other standard columns are the stage's |
| idempotency_key | PLT library, created in `rwb_treatment` | the write key of the apply | Write, once per applied document set |

Field IDs are those of TSD S2 T3.1 and the Logical Data Model and Data Dictionary. The fact columns are the one addition this story makes: TSD S2 T3.1 gives the treatment no contract and no mortgage column, so the columns are named for the extracted codes, the amounts follow the numeric(18,2) convention TSD S2 T3.1 already uses for DF-TRT-007 and DF-TRT-008, the dates follow its date convention, and `title_doc_no` and `land_office` carry no type in any source — the whole set is recorded as GAP-2702 with ASM-4478. `document`, `document_field`, `document_type` and `document_hub_parameter` (P5), `recovery_case`, `parameter_catalog` and `reference_row` (P3) and `decision_log_entry` (P7) are not created, not written and not read as tables: no foreign key leaves `rwb_treatment`, `treatment.case_id` is an identifier and not a foreign key across schemas, and no `v_ace_*` view is reachable from the login (DP-01, BR9).

**No personal data.** The only personal value in the pipeline is `party_names`, which the hub extracts from a contract and masks for a role that may not see it. It is never mapped onto a column, never stored, never logged and never put on an event: the officer sees it on the hub's own document surfaces through the composite route, masked, and this service holds no copy of it. Amounts, dates, a title document number and a land office are business facts of the treatment and not personal data, and the fixture values of section 7 are synthetic examples only.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). The two operations are the rows API-S2-001 and API-S2-002 of TSD S2 T-A.1, re-based on the service path; this story adds no operation of its own and changes no element of their published shape.

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| API-S2-001 | POST | `/cases/{caseId}/treatments` | Open a treatment; when the request names a document type, apply the confirmed checked fields of that type in the same transaction | Treatment and offer C, scope applied | `Idempotency-Key` header required; a repeated key answers the first result |
| API-S2-002 | GET | `/treatments/{treatmentId}` | Read the treatment with its terms, its state, the fact columns, the document version each fact came from and the fact sets it reports open | Treatment and offer R, scope applied | Not applicable |

The errors are 401, 403, 404, 409, 422 and 503 with the RFC 9457 problem body; 403 carries MSG-P4-002, 404 carries MSG-P4-003, 422 carries the platform field error and 503 carries MSG-GEN-006. The answer of API-S2-001 and API-S2-002 carries the applied facts with their `documentId`, `docVersion` and type-table version, and the withheld fact sets with their review reasons; those element names of the checked-field fill are this story's design and are Not specified in the source documents (GAP-2702; ASM-4478). The treatment resource declares no offer operation, no approval envelope and no plan body: those belong to `RWB-S2-E3002-CON`, `RWB-S2-E3003-CON` and `RWB-S2-E3004-CON`.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| The checked-fields read, whose path and operation name are fixed by RWB-P5-E2025-CON and are Not specified in the source documents (GAP-2702; ASM-4478) | `/api/recovery/document/v1` | P5 rwb-document (`RWB-P5-E2025-CON`) | The target shape of the legacy `DocumentFieldReader.checkedFields(UUID caseId, String documentType)`: the checked fields of a case and a type, each `documentId, docVersion, fieldName, value, state (OK, CONFIRMED, CORRECTED), confidence`, filtered by state and masked by role; one hop, 2 s, a breaker, no call chain (DP-11; ADR-020); built against the contract and its fake |
| The parameters read of the field threshold and the accuracy pass mark, operation name Not specified in the source documents (GAP-2702; ASM-4478) | `/api/recovery/case/v1` | P3 rwb-case (`RWB-P3-E1042-CON`) | The field threshold and `EXTRACT_ACCURACY_PASS` at their version, cached; no threshold and no pass mark in code (DP-06) |
| The reference-data read of LOV-DOC-TYPE, operation name Not specified in the source documents (GAP-2702; ASM-4478) | `/api/recovery/case/v1` | P3 rwb-case (`RWB-P3-E1043-CON`) | The eleven type codes the stage may ask for and the version in force they are read at; the extracted codes themselves come on the reader's answer (DP-07) |

One operation is consumed at run time and two are consumed as parameters and lists; all three are one hop with a 2 s timeout and a breaker, and none calls another service. The two H rows of DP-06 and DP-07 and the two C rows they add stand in no build row of this story's plan (ASM-4481). A failed document read answers 503 with MSG-GEN-006 naming "Document service", and a failed parameter or list read answers 503 with MSG-GEN-006 naming "Reference data"; no refusal returns a partial fact set.

#### 12.3 Events published

None. The topic of the service is `rwb.treatment.events.v1` with event names `rwb.treatment.<Event>.v1` (Architecture v5 slide 8; context pack), and the one event it carries, `TreatmentApproved`, belongs to the approval story of this epic (TSD S2 T5.3; EV-10 in the context pack). This slice announces no second event: applying an extracted amount is a fact about a row and not a decision or a stage move, and DP-09 is stated as a prohibition in section 13. No outbox row is written by this story.

#### 12.4 Events consumed

None. The extraction event of the hub is rwb-document's own and this story carries no integration dependency on it (I is None in the work package), so this service subscribes to no topic for it, holds no consumer group for it and registers no listener. The stage receives its trigger as the case signal the parent `CaseWorkflow` forwards, and a replayed workflow reuses the recorded signal (Architecture v5 slide 13; Temporal and Drools Design slide 9). The inbox table of the platform event library exists in `rwb_treatment` for the events other S2 stories consume — `PaymentMissed` (EV-12) among them, which the design shows reaching the stage through the case router (Temporal and Drools Design slide 9) — and this story writes none of its rows.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `TreatmentWorkflow` | Workflow, the stage child of `CaseWorkflow`, one execution per case and stage; not changed in shape by this story | `rwb-treatment` | Input: case ID, treatment ID, business date, caller identity; output: the applied and withheld fact sets of section 7 |
| `applyDocumentFacts` | Activity, new in this story | `rwb-treatment` | Input: case ID, treatment ID, the three document types, caller identity; output: the applied facts with their source identifiers and table version, the withheld fact sets with their reasons, and the outcome of each read |

The activity is called by `TreatmentWorkflow` in the stage it already runs; it opens no child workflow, starts no timer and calls no third service. The name `applyDocumentFacts` and the shape of its input and output records are this story's design and are fixed by no source (GAP-2702; ASM-4478).

Workflow ID form and start rule of `TreatmentWorkflow`: Not specified in the source documents (DOR-RWB-S2-E2025-APP-8; CG-ALL-8397).

#### 12.6 Schedules

None. No row of the job map belongs to this capability: the document intake job JOB-12 (legacy RWB-E2-025 section 4) and the monthly retention run JOB-17 are rwb-document's, and the classifier and the extraction run inside the intake workflow. DP-10 is in the pattern list and registers nothing here: no cron entry, no Temporal Schedule and no event-started workflow is created or moved by this story, and the only clock it touches is the 2 s budget of a single REST hop.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | Adds the fact and source columns of section 11 on the service's Flyway sequence and writes them through `TreatmentFactWriter`; the fields DF-TRT-003 to DF-TRT-033 stay the stage stories' |
| `idempotency_key` | `rwb_treatment` | PLT library object created in this schema | Written once per applied document set, in the same transaction as the row |
| `processed_event` | `rwb_treatment` | PLT library object created in this schema | Created by the library for the consumers other S2 stories add; this story writes none of its rows |

Not owned and never read as a table: `document`, `document_field`, `document_type` and `document_hub_parameter` (P5, `rwb_document`), `recovery_case`, `parameter_catalog`, `reference_row` and `lov_value` (P3, `rwb_case`), `decision_log_entry` and `rule_row` (P7, `rwb_decision`), and every `v_ace_*` view (P1). No foreign key leaves the schema and no cross-schema join exists (DP-01, BR9). The outbox, inbox and idempotency tables are the service template's and are described here only for the row this story writes (ASM-4481).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-document checked-fields fake (`RWB-P5-E2025-CON`) | The checked fields of case "RW-2026-000601" for CONTRACT, CREDIT_APPROVAL and MORTGAGE_DOCUMENT with the values of section 7; a REVIEW entry at confidence 0.7100 for "DOC-0601"; an empty answer with reason UNKNOWN_TYPE for "DOC-0602"; a 404 for the document of team "LIT-NE"; a 403 for a role without Documents R; a masked party_names entry; no answer beyond 2 s | AC1, AC2, AC3, AC6, AC7, AC8 |
| rwb-case parameters fake (`RWB-P3-E1042-CON`) | The field threshold 0.80 and the accuracy pass mark 0.90 at their version, and a delayed answer beyond 2 s | AC4, AC6 |
| rwb-case reference-data fake (`RWB-P3-E1043-CON`) | LOV-DOC-TYPE with the eleven types at their version | AC3, AC4 |
| gateway-bff composite route fake (`RWB-PLT-N001-CON`) | The merged SCR-14 and SCR-15 answer for case "RW-2026-000601" with the treatment facts of this service and the checked fields of rwb-document read once | AC8 |
| idempotency double over the write key | One applied set per document ID, `doc_version` and type-table version; a second apply of the same key is answered by the first | AC5 |

The fakes are test-only and are replaced by the real services in SIT; a drift between a fake and the published contract is a build failure of `RWB-P5-E2025-CON` or of the platform story that owns the fake.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | API-S2-001 and API-S2-002 on `/api/recovery/treatment/v1`; the checked-fields read of `RWB-P5-E2025-CON`, the parameters read and the reference-data read of rwb-case; one hop and 2 s on each consumed call |
| Kafka | None | No event published and none consumed by this story; the topic `rwb.treatment.events.v1` carries the events of the sibling stories |
| Temporal | 1 workflow, 1 activity | `TreatmentWorkflow` on queue `rwb-treatment` and the new `applyDocumentFacts` activity; no child workflow, no timer and no Schedule |
| File | None | No file is read, built or delivered: no document content is touched |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.treatment`, module `stage23facts`, Java package `th.co.scb.ace.workbench.recovery.treatment.stage23facts`; front end `src/modules/recovery/treatment/Stage23Facts.tsx`, the read-only fragment SCR-14 and SCR-15 embed. Service base `/api/recovery/treatment/v1`, schema `rwb_treatment`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 keeps the write inside `rwb_treatment`: `treatment`, the fact columns and the idempotency row are this schema's, and the case, the type version, the threshold and the pass mark are answers of contracts, never rows of another schema. DP-06 and DP-07 are the two parameter and list reads of 12.2, cached, so no threshold, pass mark, type code or version is a constant of the module. DP-11 is the whole point of the slice: the legacy in-process `DocumentFieldReader` becomes one hop with a published shape, a fake and a 2 s timeout, and S2 builds on Day 1 without a document table. DP-13 puts the two operations on the service base and removes the monolith base from the paths this story serves. DP-19 records that the facts reach SCR-14 and SCR-15 through the gateway-bff composite route; the route specification and the screen field list are the edge contract's.

Two patterns are prohibitions in this slice and are stated so that no build adds what the list implies:

- **DP-09 writes no event.** The library is the service template's and this story uses it for the idempotency and inbox tables of `rwb_treatment` and for the one write key of the apply. `DocumentFieldsExtracted` is produced by rwb-document and this story registers no listener for it (I is None), and the one event of rwb-treatment belongs to the approval story, so this module declares no producer, writes no outbox row and adds no event to the topic.
- **DP-10 registers no Schedule.** No job of this capability exists to schedule: the intake Schedule and the retention Schedule are rwb-document's (JOB-12, JOB-17; the job map). This module declares no cron entry, no Temporal Schedule and no event-started workflow, and the stage clock it runs under is the parent workflow's.

**Dependencies the table adds and the plan does not hold.** The pattern table adds five H rows — `RWB-PLT-E1042-CON` and `RWB-PLT-E1043-CON` for DP-06 and DP-07, `RWB-PLT-TE006-CON` for DP-09, `RWB-PLT-E1071-CON` for DP-10 and `RWB-PLT-N001-CON` for DP-19 — and two C rows, `RWB-P3-E1042-CON` and `RWB-P3-E1043-CON`, while the plan's lists for this story hold Depends on (build) `None` and Contract dependencies `RWB-P5-E2025-CON` only. The metadata table keeps the plan's lists as they are, the service template carries every one of the five, and the story builds against their fakes until those stories publish (ASM-4481).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `ApplyDocumentFactsActivity` | Activity | The `applyDocumentFacts` entry point: resolves the types, calls the client per type, filters, maps, guards the version, writes, and returns the applied and withheld sets |
| `CheckedFieldClient` | Client | The checked-fields call on `RWB-P5-E2025-CON`, one hop, 2 s, a breaker and no retry chain (GAP-2702; ASM-4478) |
| `CheckedFieldFilter` | Service | Keeps only OK, CONFIRMED and CORRECTED entries and drops every entry below the pass mark, so a withheld value cannot be promoted by a future contract version |
| `Stage23TreatmentMapper` | Mapper | Maps a field code onto the treatment column of the same name only; holds the field code names of the contract and the column names of section 11, and no amount, no date and no list value (GAP-2702; ASM-4478) |
| `Stage23VersionGuard` | Service | Compares the reported `tableVersion` with the version the reference-data contract reports in force and the parameter values with the parameters contract; refuses the apply when they disagree |
| `TreatmentFactWriter` | Repository | Writes the fact columns, the source identifiers, the stamped type-table version and the idempotency row in one `rwb_treatment` transaction; writes no other table |
| `Stage23Idempotency` | Service | Builds the write key from the document ID, the `doc_version` and the type-table version, recognises a repeat and re-runs nothing that completed |
| `TreatmentFactReader` | Service | Serves API-S2-002 with the facts, the source identifiers and the fact sets reported open |
| `Stage23FactsPanel` | React component | Shows the applied facts, the version each came from and the open fact sets on SCR-14 and SCR-15, read only, with the refusal and unavailable states |

**Database and migrations.** One Flyway version on the service's own sequence adds the fact and source columns of section 11 to `treatment`, with no cross-schema key and no index of another schema. `idempotency_key` and `processed_event` are platform library objects created in `rwb_treatment` by the library's own migration. No other table, column or index is added, and an applied migration is never edited. The column set is Not specified in the source documents and is recorded as GAP-2702 with ASM-4478.

**Configuration and reference data.**

- The field threshold and the accuracy pass mark are parameter values resolved through the parameters contract and client library of rwb-case (DP-06); the operation this story calls is Not specified in the source documents (GAP-2702; ASM-4478).
- LOV-DOC-TYPE with the eleven types is read through the reference-data client library (DP-07); no list value is copied into `rwb_treatment`.
- The type and field codes and the table version are taken from the reader's answer at run time; a build check pairs the field code names held by `Stage23TreatmentMapper` with the fixture of `RWB-P5-E2025-CON`, so a code that leaves the fixture fails the build (AC4).
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020 and not a value of this story.
- The feature switch `rwb.treatment.stage23-facts`, read as a flag of the platform library: off means the stage applies no checked field and API-S2-002 answers the treatment with no applied set, while the two operations themselves are unchanged.

**Build steps**

1. `CheckedFieldClient` against the contract fake, with the 2 s budget, the breaker, the no-answer path and the two refusals; test X4, X5, X6 and AC6.
2. `CheckedFieldFilter` and `Stage23VersionGuard` over the fake's answers, with the REVIEW entry, the below-pass-mark value, the empty answer and the version disagreement; test AC2, AC3, AC4.
3. `Stage23TreatmentMapper` with the name-identical mapping and the unmapped codes; test AC1, X8 and the build check of AC4.
4. `TreatmentFactWriter` in one transaction with the idempotency row and the uniqueness of the write key; test AC1 and AC5.
5. `Stage23Idempotency` with the repeated apply, the repeated read and the new `doc_version`; test AC5.
6. `ApplyDocumentFactsActivity` registered on `rwb-treatment` and called from `TreatmentWorkflow`, with the retry policy of the platform and the no-partial-write path; test AC6.
7. `TreatmentFactReader` and `Stage23FactsPanel` through the composite route fake, with the applied set, the open fact sets and the masked party names; test AC7 and AC8.
8. The boundary test: no statement outside `rwb_treatment`, no `v_ace_*` read, no read of any table section 12.7 does not own, no event producer, no consumer and no Schedule in the module; test BR9, BR10, BR11 and the two prohibitions.

**Done when.** The tests of section 16 pass, the contract tests of `RWB-P5-E2025-CON` stay green, a SIT week shows the contract and mortgage facts applied once per document version and type-table version, no value in REVIEW promoted and no column cleared by a withholding read, no read of a document table or an ACE view in the logs, no event and no Schedule registered by this module, and SCR-14 shows the facts through the composite route.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | A document has a field in review, so the fact this story needs is withheld and its set is reported open (X1, X2, X3) | Some fields need checking. The document is in the review queue. |
| MSG-P4-002 | The caller's role lacks Documents R on the read, or the Treatment and offer right on the operation (X5, AC6, AC7) | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The document or the case lies outside the caller's scope (X6, AC6) | This case is not in your scope. |
| MSG-GEN-006 | The checked-fields read, the parameters read or the reference-data read did not answer inside the budget (X4) | {system} is not available. Your request is queued and will be retried. |

The four texts are copied unchanged from legacy RWB-E2-025 section 14 and are the wording of the hub and the access module; no message is reworded and no new message is added. For MSG-P4-002 the {action} value names what the caller tried — for example "apply the checked fields of this treatment" — and never a case fact, a document ID or a role name. For MSG-GEN-006 the {system} value is "Document service" on the checked-fields read and "Reference data" on the parameters and list reads. Each error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled and `instance` naming the request; the status mapping is 403 for MSG-P4-002, 404 for MSG-P4-003 and 503 for MSG-GEN-006, and MSG-P5-003 is a label of the document and of the open fact set and not an error of this service. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen is built in this story. Three surfaces show what it writes, all read through the gateway-bff composite route (DP-19), and only the first two are this service's own read model.

| Screen | State | What the user sees or does |
|---|---|---|
| SCR-14 Treatment record | Loading | The placeholder while the composite route answers |
| SCR-14 Treatment record | Draft or submitted | The contract amount, the contract date and the mortgage registration facts, with the document ID and the document version each fact came from, and the type-table version they were applied under |
| SCR-14 Treatment record | Fact set open | The contract, credit-approval or mortgage fact set that needs a withheld field, with its review reason and the review queue of the hub as the place to fix it, and MSG-P5-003 on the document |
| SCR-14 Treatment record | Refused | A role without the Treatment and offer right reads MSG-P4-002 and nothing changes |
| SCR-14 Treatment record | Out of scope | A case outside the scope reads MSG-P4-003 |
| SCR-14 Treatment record | Document service unavailable | Not specified in the source documents (CG-ALL-8402); the treatment keeps the facts it already holds |
| SCR-14 Treatment record | Empty | Not specified in the source documents (CG-ALL-8402) |
| SCR-14 Treatment record | Loading | Not specified in the source documents (CG-ALL-8402) |
| SCR-14 Treatment record | Error | Not specified in the source documents (CG-ALL-8402) |
| SCR-14 Treatment record | No access | Not specified in the source documents (CG-ALL-8402) |
| SCR-15 Settlement offer | Draft or below floor | The contract amount as the baseline of the offer the settlement story builds, read only |
| SCR-15 Settlement offer | Approval sought, sent, accepted | The same baseline, unchanged by this story |
| SCR-15 Settlement offer | Empty | Not specified in the source documents (CG-ALL-8403) |
| SCR-15 Settlement offer | Loading | Not specified in the source documents (CG-ALL-8403) |
| SCR-15 Settlement offer | Error | Not specified in the source documents (CG-ALL-8403) |
| SCR-15 Settlement offer | No access | Not specified in the source documents (CG-ALL-8403) |
| SCR-30 Case documents | List, as rwb-document serves it | The stage 2 and 3 types with their checked fields and their review state, read only through the same route |
| SCR-30 Case documents | Empty | Not specified in the source documents (CG-ALL-8404) |
| SCR-30 Case documents | Loading | Not specified in the source documents (CG-ALL-8404) |
| SCR-30 Case documents | Error | Not specified in the source documents (CG-ALL-8404) |
| SCR-30 Case documents | No access | Not specified in the source documents (CG-ALL-8404) |
| SCR-31 Document review queue | List and reviewed, as rwb-document serves it | The marked fields of the new types, read only here; the correction is the hub's |
| SCR-31 Document review queue | Empty | Not specified in the source documents (CG-ALL-8405) |
| SCR-31 Document review queue | Loading | Not specified in the source documents (CG-ALL-8405) |
| SCR-31 Document review queue | Error | Not specified in the source documents (CG-ALL-8405) |
| SCR-31 Document review queue | No access | Not specified in the source documents (CG-ALL-8405) |

The route merges the answer of this service with rwb-document's; the route path, the screen-model field list and the merge order belong to `RWB-PLT-N001-CON` and the edge stories, not here (ASM-3076). SCR-14 and SCR-15 are the treatment screens of the epic, so the panel is built against the route fake and switched on with them.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-025-12 | AC6 (legacy Access) | Component | RW-REFADM holds no Documents R; the checked-fields read is refused with 403 and MSG-P4-002 and the apply writes nothing |
| TC-E2-025-01 | AC3 (legacy AC1) | End to end | 10 masked court notices of the sample; COURT_NOTICE is no treatment type, so the row takes no fact from it and no column changes |
| TC-E2-025-02 | AC1, AC7 (legacy AC2) | End to end | Contract "DOC-0601" on case "RW-2026-000601": contract_amount 2400000.00 and contract_date 2026-11-01 on the row, party_names masked and stored nowhere |
| TC-E2-025-03 | AC2 (legacy AC3) | End to end | contract_amount at confidence 0.7100 in REVIEW; withheld, the previous 2400000.00 kept, and the set open with MSG-P5-003 |
| TC-E2-025-04 | AC2, AC4 (legacy AC4) | End to end | 10 sample contracts with 8 amounts correct, the pass mark 0.90 in force; the proposal changes nothing until it is loaded |
| TC-E2-025-05 | AC3 (legacy AC5) | End to end | 50 documents of the five new types; a type the treatment does not consume and an item the classifier could not place write no fact |
| TC-E2-025-06 | AC3 (legacy AC6) | End to end | "DOC-0602" received 2026-12-26, before the valid-from date; no column changes, reason UNKNOWN_TYPE |
| TC-E2-025-07 | AC1 (legacy AC7) | End to end | A contract date read as "1 December 2569 BE"; contract_date 2026-11-01 on the row |
| TC-E2-025-08 | AC2 (legacy AC8) | End to end | A value failing its pattern arrives in REVIEW with confidence 0.9200; nothing is applied and the set is reported open |
| TC-E2-025-09 | AC1, AC2 (legacy AC9) | Contract | A contract with one field in OK and contract_amount in REVIEW: the mapped field is applied, the amount is never promoted |
| TC-E2-025-10 | AC5 (legacy AC10) | End to end | Write-once contract "DOC-0604": the facts are applied and no document row, hash or storage reference is written by this service |
| TC-E2-025-11 | AC6 (legacy AC11) | Contract | Document "DOC-0605" of team "LIT-NE" read by an officer of team "LIT-BKK": 404 with MSG-P4-003 and no fact written |
| TC-S2-E2025-APP-01 | AC1, AC5 | Integration | The contract and mortgage facts applied once per document ID, doc_version and type-table version; a repeat writes nothing and a new doc_version applies once more |
| TC-S2-E2025-APP-02 | AC4 | Contract | The parameter and reference-data answers at their version, and a build check that fails on a type code, a field code, a threshold, a pass mark or a valid-from date in the source |
| TC-S2-E2025-APP-03 | AC6 | Component | 503 with MSG-GEN-006, nothing written, and the retry policy of 1 s initial interval, back-off 2 and 10 attempts |
| TC-S2-E2025-APP-04 | AC7, AC8 | Component | The composite route fake merging SCR-14 and SCR-15 with the masked party names and the facts of this service |
| TC-S2-E2025-APP-05 | AC9, BR9 | Integration | No statement outside `rwb_treatment` names or reads a table of section 12.7 that this story does not own; the grant refuses it and the build fails |
| TC-S2-E2025-APP-06 | AC12 | Integration | Not specified in the source documents (NEWAC-RWB-S2-E2025-APP-AC12) |
| TC-S2-E2025-APP-07 | AC13 | Component | Not specified in the source documents (NEWAC-RWB-S2-E2025-APP-AC13) |
| TC-S2-E2025-APP-08 | AC14 | Component | Not specified in the source documents (NEWAC-RWB-S2-E2025-APP-AC14) |
| TC-S2-E2025-APP-09 | AC15 | Component | Not specified in the source documents (NEWAC-RWB-S2-E2025-APP-AC15) |

The twelve identifiers TC-E2-025-12 and TC-E2-025-01 to TC-E2-025-11 are legacy-carried: this slice answers the S2 half of each, at Contract where the row proves the reader contract and at End to end where the row proves the extraction-to-treatment path, and the nine cases TC-S2-E2025-APP-01 to TC-S2-E2025-APP-09 are new for the criteria of this story that no legacy row exercises. The legacy level "System" maps to "End to end" and "Access" to "Component". The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID, and the `-ITG` copies of these rows belong to the wave 2 integration harness.

### 17. Guardrails

- No business value in code: the type codes, the field codes, the table version, the field threshold, the accuracy pass mark and the lists are rows read at their version; a build check fails on a type code, a field code, an amount, a date, a threshold, a pass mark or a valid-from date in the Java source or the module configuration.
- No personal data in logs, tests, workflow inputs, events or `rwb_treatment`: `party_names` is never mapped, stored, logged or put on a message, and a property test places a synthetic party name in the reader's answer and asserts that it appears in no row, no log line and no span attribute.
- ACE data only through the owner's contract: no component of this story reads an ACE view or an ACE table, and the `rwb_treatment` login holds no `v_ace_*` grant (DP-01; Architecture v5 slide 8).
- No read of another service's tables and no cross-schema join: `document`, `document_field`, `document_type` and `document_hub_parameter` (P5), `recovery_case`, `parameter_catalog` and `reference_row` (P3) and `decision_log_entry` (P7) are reached only through their owners' contracts, and the boundary test fails the build on any statement outside `rwb_treatment`.
- Only checked values move: a field in REVIEW, a value below the pass mark, a type not in force and an item with reason UNKNOWN_TYPE are withheld, and no code path promotes them; the withheld fact set is shown open with its reason.
- One hop and a 2 s budget on the single consumed read, with a breaker and no call chain; a repeat is the same write key and never a silent second write.
- No event, no topic producer, no outbox row and no Schedule: this story publishes nothing, consumes nothing and schedules nothing (DP-09 and DP-10 as prohibitions), and the facts reach the other services on the owners' own reads.
- The write is a write of facts: no case state, no treatment lifecycle state, no offer and no approval is written here, and no decision record is written because no rule is evaluated.
- The screens are read only: SCR-14 and SCR-15 show what this service wrote and what the hub serves, and no screen writes a checked field.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-006 | Fields are extracted into the index for the agreed document types, in Thai and in English, which this story consumes on the treatment side by filling the treatment record from the checked fields | Business Requirements Program v5, section 5.5; Epic 2 v2, section 3.5 | FEAT-DCM-22 | 13 Manage documents and correspondence | R-UNI-38, CTL-08, CTL-11, CTL-12 | TC-E2-025-02, TC-E2-025-07, TC-E2-025-09, TC-E2-025-10, TC-S2-E2025-APP-01 |
| REQ-DCM-005 | Inbound documents are classified into one of the agreed types with a confidence score, and anything below the threshold goes to a review queue; this story withholds what the queue still holds | Business Requirements Program v5, section 5.5; Epic 2 v2, section 3.5 | FEAT-DCM-22 | 13 Manage documents and correspondence | R-UNI-38, CTL-08 | TC-E2-025-01, TC-E2-025-03, TC-E2-025-04, TC-E2-025-05, TC-E2-025-06, TC-E2-025-08 |
| REQ-DCM-017 | The hub answers an electronic discovery request for a named population with its metadata and version history; carried by the plan's requirement list and not by the legacy traceability table, and out of scope of the legacy key | Business Requirements Program v5, section 5.5; Epic 2 v2, section 3.5 | FEAT-DCM-22 | 13 Manage documents and correspondence | None | None here: the discovery answer is the document hub's (ASM-4479) |
| REQ-DCM-018 | A document produced from the hub carries what a court needs to accept it; carried by the plan's requirement list and not by the legacy traceability table, and out of scope of the legacy key | Business Requirements Program v5, section 5.5; Epic 2 v2, section 3.5 | FEAT-DCM-22 | 13 Manage documents and correspondence | None | None here: the court-evidence attributes are the document hub's (ASM-4479) |

The four requirements are the plan's list for this story. The legacy traceability table of RWB-E2-025 carries REQ-DCM-006 and REQ-DCM-005 only, and its out-of-scope list puts REQ-DCM-017 and REQ-DCM-018 outside the key, so the two are carried with the plan's list and answered by the hub. Feature FEAT-DCM-22 ("Extend extraction to the stage 2 and 3 document types") and L3 process 13 ("Manage documents and correspondence") are the legacy key's and are kept unchanged; this story answers them on the S2 side of the same key.

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E2-025 | The S2 deliverable of the key: the confirmed checked fields applied to `treatment`, the withheld field and the value the row keeps, the version and parameter reads, the idempotent write, the refusal passed through with the platform retry, the masking and the read model |
| RWB-P5-E2025-APP (P5) | The classification, the extraction, the evaluation runner, the review queue, the write-once rule and the eleven legacy criteria AC1 to AC11 word for word |
| RWB-P5-E2025-CON | The checked-fields read, the `CheckedField` and `CheckedFieldSet` shapes, the state filter, the masking rule, the error envelope and the fake this story builds against (GAP-2702; ASM-4478) |
| The wave 2 integration harness | The end-to-end proof of the same values across rwb-document, rwb-treatment and rwb-case, which no criterion of this story claims |
| RWB-S2-E3001-APP to RWB-S2-E3005-APP | The treatment row this story writes on, the offer, the approval, the plan and the affordability pre-assessment, and the events and timers of the stage |
| DP-01, DP-13 | The owner's schema and the service base `/api/recovery/treatment/v1` |
| DP-06, DP-07 | The parameters and the reference-data reads of rwb-case at their version (ASM-4481) |
| DP-09, DP-10 | The two prohibitions: no event producer or consumer, and no Schedule in this slice (ASM-4482) |
| DP-11, DP-19 | One hop with a 2 s timeout on the reader, and the two screens behind the gateway-bff composite route (GAP-2703; ASM-4483) |
| ADR-013, ADR-014, ADR-015, ADR-020 | 19 services inside ACE, a schema and a login per service, the Kafka platform this story adds no producer to, and contract-first REST with one hop |
| Document generation, review and signature | Not in this slice: generation, review and signature are requested through the P5 and P6 contracts, not the document hub; this story holds only the document reference and version and keeps no document content in rwb_treatment (GAP-1704) |

### 19. Out of scope

- The classification, the extraction, the evaluation runner, the pass-mark proposal, the review queue and the write-once rule, and the eleven legacy criteria AC1 to AC11: `RWB-P5-E2025-APP` and the extraction, review and type-load stories of rwb-document.
- The checked-fields read, its path, its shapes, its state filter, its masking rule, its error envelope and its fakes: `RWB-P5-E2025-CON`.
- The type table, the `DOCTYPE-2026.12` load, its Legal and NPA sign-off and the parameter values: the document hub's type-load story and the reference data administrator of rwb-case.
- The opening of the treatment row, the offer and its range, the approval below the floor, the TDR plan and its timers, the ACE affordability pre-assessment and the one event of the service, `TreatmentApproved`: `RWB-S2-E3001-APP` to `RWB-S2-E3005-APP`.
- The case status, the `CaseWorkflow`, the case router, the case table and the case signal: rwb-case (P3).
- The RESTRUCTURE, SETTLEMENT and DEEDINLIEU packages, their rows and their versions: rwb-decision (P7); this slice evaluates no rule and writes no decision record.
- The rights, the roles, the scope data and the masking policy, and the guard library that answers them: rwb-access (P4) and the platform library stories.
- The litigation fill of the same legacy key, the pack of the litigation route and the judgment and enforcement decisions: the S4 slice of RWB-E2-025 and the pack, judgment and enforcement stories of rwb-litigation.
- The gateway-bff composite route, the screen field list, the layout of SCR-14 and SCR-15, and SCR-30 and SCR-31 themselves: `RWB-PLT-N001-CON`, the edge story and the screen owners.
- The end-to-end proof of these values across the three services: the wave 2 integration harness.
- The deployment of this build: chart values, the queue and topic provisioning, the flag, dashboards, alerts and the runbook.

# RWB-S4-E2025-APP Extraction for the stage 2 and 3 document types

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the S4 litigation slice of legacy RWB-E2-025 is split out of the document hub key. The confirmed checked fields of the `COURT_FILING`, `JUDGMENT`, `COURT_NOTICE`, `CONTRACT`, `CREDIT_APPROVAL` and `MORTGAGE_DOCUMENT` types are consumed from the published contract RWB-P5-E2025-CON on one hop with a 2 s timeout, kept only in state `OK`, `CONFIRMED` or `CORRECTED`, mapped only onto a column of the same name on `legal_action` and `hearing` in `rwb_litigation` in one transaction, idempotent on the document ID, the `doc_version` and the type-table version, and with no read of a document, a field row, a type row or a parameter table; the type-table version is stamped on the row, the base is `/api/recovery/litigation/v1` (DP-13) and SCR-19 is reached through the gateway-bff composite route (DP-19). The eleven legacy acceptance criteria stay with RWB-P5-E2025-APP; this slice writes eight criteria of its own. The two open points are GAP-2835 and GAP-2836 and the eight assumptions ASM-4689 to ASM-4696. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S4-E2025-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-litigation |
| Service epic | RWB-SVC-S4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-025 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Parallel lane | L-S4-A |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E2025-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md (no FR mapped to REQ-DCM-006, REQ-DCM-005, REQ-DCM-017, REQ-DCM-018) |
| Status | Draft (realignment v1) |

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the confirmed fields that rwb-document extracted from the stage 2 and 3 document types — contracts, credit approvals, mortgage documents, court filings, hearing notices and judgments — applied to the legal action and to its hearing in rwb-litigation, through the published checked-field contract RWB-P5-E2025-CON and without opening a document, a field row, a type row or a parameter table myself**, so that **the legal action carries the court name, the black and red case numbers, the claim and the judgment amounts and the filing, judgment and hearing dates from the paper the officer already holds, and a value that no person has checked and no rule has passed never reaches the case**.

This document is the S4 litigation slice of legacy RWB-E2-025. It owns no legacy criterion: the eleven criteria AC1 to AC11 of the story master are the document hub's and are owned by `RWB-P5-E2025-APP`, which keeps the classification, the extraction, the evaluation runner, the review queue and the write-once rule word for word; the shapes, the path, the state filter, the masking rule and the fakes of the reader are owned by the contract `RWB-P5-E2025-CON`. What this story owns is the S4 deliverable of the title: the application of the checked fields to its own rows, the withholding of a field in review, the version and parameter reads, the idempotent write, the refusals it passes through and the read model of the litigation screen. Its criteria are therefore new under D-RCV-60 and test only that deliverable.

The legacy story says what this slice is in its flow step 9: "S4 and S2 modules: read confirmed field values through DocumentFieldReader to fill the pack and the treatment record (from Epic 3 and Epic 5)". Its out-of-scope list says the complementary half just as plainly: "Writing extracted values into legal_action, hearing or treatment (S4 in Epic 5, S2 in Epic 3)". That write into `legal_action` and `hearing` is this story, and it is the only business write it makes.

Four facts shape the slice.

1. **The reader is a contract, not a table.** Legacy `DocumentFieldReader.checkedFields(UUID caseId, String documentType)` returned `List<CheckedField>` in process. In the target, rwb-document publishes that read as `GET /api/recovery/document/v1/cases/{caseId}/checked-fields` with `CheckedFieldSet` and `CheckedField` (`documentId, docVersion, fieldName, value, state (OK, CONFIRMED, CORRECTED), confidence`), and this service consumes it one hop, with a 2 s timeout, a breaker and a GET retry once with jitter (DP-11; RWB-P5-E2025-CON).
2. **S4 holds no document.** rwb-litigation reads no `document`, `document_field`, `document_type` or `document_hub_parameter` row and no `v_ace_*` view: those tables are rwb-document's in `rwb_document` and the thirty `recovery.v_ace_*` views are read by rwb-source-data alone (DP-01, DP-05). The `rwb_litigation` login holds no grant on `rwb_document` and no `v_ace_*` grant, so the boundary is enforced by the database and not only by review.
3. **Only checked values move.** A field in state `REVIEW`, a field of a type that is not in the version in force and a value whose extraction confidence is below the pass mark are never promoted here. The column keeps the value it already holds, the fact set that needs the withheld field stays reported open with its review reason, and the officer is sent to the review queue of the hub.
4. **The values are data with a version.** The type codes, the field codes, the field threshold and the accuracy pass mark are read at their version: the type-table version arrives as `tableVersion` on the reader's answer, the threshold and the pass mark come from the parameters contract of rwb-case, and the type list from its reference-data contract (DP-06, DP-07). Nothing of them is a constant of this module.

### 2. Business rationale

A judgment is a date and an amount, and a court filing is a court, a black case number, a filing date and a claim. Today the litigation officer reads them from paper and types them onto the legal action, and the litigation pack of `R-LIT-16` is assembled from the same paper by hand. The legacy key measured the cost: litigation takes 21 days to file, packs are incomplete and law firm progress is not tracked (FSD S4 A1.3, A2.4 and A2.16).

The document hub now extracts those values. Legacy RWB-E2-025 extended classification and extraction to five new types — `CONTRACT`, `CREDIT_APPROVAL`, `MORTGAGE_DOCUMENT`, `COURT_FILING`, `JUDGMENT` — and kept hearing notices under the Epic 1 type `COURT_NOTICE`, in the type table version `DOCTYPE-2026.12` valid from `2026-12-31`, with a field threshold of `0.80` and an accuracy pass mark of `0.90`. That half is `RWB-P5-E2025-APP` and is not restated here.

What the hub cannot do is write the litigation record. The legal action, its hearing, its court numbers and its judgment are rwb-litigation's: the service owns legal actions, hearings, judgments, enforcement and the LED auction ladder in schema `rwb_litigation`, on tables `legal_action` and `hearing` (TSD S4 T3.1; context pack S4). So a value leaves the hub once, on a published read, and lands on the row of the service that owns the fact. The moment rwb-litigation reads `document_field` for itself, two services own one extraction and the state filter of the reader can be bypassed by a query.

Three consequences follow, and each is designed rather than left to discipline.

- **The litigation rows fill themselves where the names meet.** Of the six types, three carry codes whose names are the names of S4 columns: `COURT_FILING` gives `court_name`, `black_case_no`, `filing_date` and `claim_amount`; `JUDGMENT` gives `court_name`, `red_case_no`, `judgment_date` and `judgment_amount`; `COURT_NOTICE` gives `court_name`, `black_case_no` and `hearing_date`. They fill `legal_action` DF-LEG-006 to DF-LEG-012 and `hearing` DF-LEG-026. Three types do not: `contract_no`, `party_names`, `contract_amount`, `contract_date`, `approval_no`, `approved_amount`, `approval_date`, `approval_level`, `title_doc_no`, `mortgage_amount`, `registration_date` and `land_office` name no litigation column, and `filing_date` meets `filed_date` only by word. Where the names do not meet, nothing is mapped, and the difference is counted and recorded (GAP-2835; ASM-4689).
- **A withheld value keeps its item open.** The reader returns no `REVIEW` field, so the legal action keeps its empty or previous column and the pack item that needs the value stays open with the review reason the hub reports — `LOW_CONFIDENCE` for a field below the threshold and `UNKNOWN_TYPE` for a document that arrived before the type version took effect. The officer is sent to the review queue of the hub, which is where a person may accept or correct the value; this service has no review screen and no override.
- **The write is a write of facts, not a case move.** Applying a judgment amount does not set a LOV-LEGAL-STATUS value and does not move the case: `R-LIT-44` records the judgment, `R-LIT-16` verifies the pack, and the litigation states of `R-LIT-01` to `R-LIT-79` are the stage stories' (FSD S4 A2.4, A2.16; TSD S4 T4). This story supplies the facts those rules read.

It serves REQ-DCM-006 on the litigation side and REQ-DCM-005 as the consumer of its outcome: the record that receives the value is the legal action, and the review path is the hub's. It puts CTL-08 in place on the reading side — a proposal below the pass mark takes effect only when it is loaded, so no value is promoted from a package that is not in force — and CTL-11 and CTL-12 by construction: a personal value is never stored and a write-once document is never touched, because no document is written at all. It carries R-UNI-38: a value is applied under the version in force on the date it is read. Wave 2 is the W-MAP wave of EP02, earlier than the service's Architecture v5 wave 3, and R5.6 keeps it.

### 3. Preconditions

- RWB-P5-E2025-CON is published: the checked-fields read on base `/api/recovery/document/v1` as `GET /cases/{caseId}/checked-fields` with the `documentType` query, the `CheckedFieldSet` and `CheckedField` shapes, the state filter (OK, CONFIRMED and CORRECTED only), the masking rule, the error envelope with its message IDs and statuses, and the contract fake. This story builds against the contract and its fake on Day 1 and never against a document table.
- `legal_action` and `hearing` exist in `rwb_litigation` from the S4 baseline stories, with the columns of TSD S4 T3.1 — `legal_action` DF-LEG-001 to DF-LEG-014 and `hearing` DF-LEG-024 to DF-LEG-029 — the standard record columns of T3.0 and the lists of T3.2: LOV-LEGAL-TYPE (`NOTICE`, `CIVIL_CASE`, `APPEAL`, `ENFORCEMENT`, `BANKRUPTCY_PETITION`, `LED_AUCTION`), LOV-LEGAL-STATUS (`OPEN`, `FILED`, `JUDGMENT`, `ENFORCING`, `CLOSED`, `WITHDRAWN`), LOV-HEARING (`FIRST_HEARING`, `WITNESS`, `JUDGMENT_READING`, `MEDIATION`) and LOV-HEARING-OUTCOME (`HELD`, `ADJOURNED`, `SETTLED`, `JUDGMENT`). This story creates no table of its own and adds only the source-stamp columns of section 11.
- A legal action of the case exists, or the caller creates it in the same request (API-S4-002). A hearing is created or updated only from a `hearing_date` the reader returns, and the `hearing_type` of such a row is Not specified in the source documents (GAP-2836; ASM-4695).
- The field threshold and the accuracy pass mark are read at their version through the parameters contract of rwb-case (DP-06, C `RWB-P3-E1042-CON`), and the type list LOV-DOC-TYPE with the eleven types through its reference-data contract (DP-07, C `RWB-P3-E1043-CON`).
- The platform outbox and inbox library (H `RWB-PLT-TE006-CON`), the workflow kit (H `RWB-PLT-E1071-CON`), the parameter and reference-data client libraries (H `RWB-PLT-E1042-CON`, H `RWB-PLT-E1043-CON`) and the gateway-bff composite route (H `RWB-PLT-N001-CON`) are named by the pattern table and stand in no build row of this story's plan; the story builds against their fakes until they publish (ASM-4692). The outbox library and the workflow kit are not used by this slice at all (ASM-4694).
- The service runs as login `rwb_litigation` on schema `rwb_litigation`, topic `rwb.litigation.events.v1`, task queue `rwb-litigation` and Java package `th.co.scb.ace.workbench.recovery.litigation`; it holds no grant on another `rwb_*` schema and no `v_ace_*` grant (DP-02, DP-01).
- The caller holds a Workbench role with the Litigation right of TSD S4 T6.1 — RW-LITOFF holds CRUA, RW-ENFORCE CRU, RW-LEGAL RA, RW-HEADLIT and RW-PRODHEAD RA — and the read is refused on the document side for a role without Documents R; this story adds no right of its own.
- The gateway-bff composite route serves SCR-19 Litigation workspace, which the FSD lists first in E5, later than this story's wave 2, so the read model is built and proved against the route fake (ASM-4693).
- The release date 31 December 2026 is the legacy one and is tentative, and the status is Draft (realignment v1) because no approval of the realigned story is recorded (ASM-4696).

### 4. Flow

1. The litigation officer opens SCR-19 Litigation workspace for a case through the gateway-bff composite route (DP-19) and selects a legal action and the document type whose extracted facts the action needs — `COURT_FILING`, `JUDGMENT` or `COURT_NOTICE` for the mappings of this story.
2. `LitigationAndEnforcementController` accepts `POST /api/recovery/litigation/v1/cases/{caseId}/legal-actions` (API-S4-002) with an `Idempotency-Key`, or `PATCH /api/recovery/litigation/v1/legal-actions/{legalActionId}` (API-S4-004) when the action exists, and validates the case, the action type, the scope and the declared right before anything is read.
3. `CheckedFieldsClient` calls `GET /api/recovery/document/v1/cases/{caseId}/checked-fields?documentType={type}`, one hop, 2 s timeout, breaker, GET retry once with jitter (DP-11).
4. `LegalActionFieldMapper` maps only a field code that names a column of `legal_action` or `hearing`, and counts every code that does not (section 11). It ignores `state` other than OK, CONFIRMED and CORRECTED — which the contract already filters — and rejects a field whose confidence is below the pass mark.
5. `LegalActionRepository` and `HearingRepository` write the mapped values, the source `document_id`, `doc_version` and `table_version` and the idempotency row in one transaction with the local decision record the service writes before any change; no column outside the mapped set changes.
6. `HearingRepository` creates one hearing row for a `hearing_date` of the action that has none for that date, or updates the `next_date` of the open hearing of the action to it; the `hearing_type` policy is the one of ASM-4695.
7. The officer sees the values on SCR-19 with the document and version each came from; the hub's SCR-30 and SCR-31 remain the only place a `REVIEW` field is checked or corrected, and the withheld fact set is shown open with its review reason.
8. The pack of `R-LIT-16` and the treatment record of `RWB-S2-E2025-APP` read the same facts from their owners — the pack from this service, the treatment row from rwb-treatment — and no caller is offered a second copy of the reader.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A field is in state REVIEW or below the pass mark | Not mapped; the column keeps its value; the fact set is reported open | MSG-P5-003 on the document in the hub | AC3 |
| X2 | The type is not in the version in force, or the item is in review with any reason | No checked field returned, so nothing is mapped and the item stays open | None | AC3 |
| X3 | A field code names no litigation column | Counted as unmapped, never stored, never logged with its value | None | AC7 |
| X4 | The reader refreshes inside the 2 s window and then refuses | 503 with MSG-GEN-006, nothing written, one GET retry with jitter | MSG-GEN-006 | AC6 |
| X5 | The caller lacks Documents R on the document side | 403 from the reader, passed through unchanged, nothing written | MSG-P4-002 | AC6 |
| X6 | The document is outside the caller's scope | 404 from the reader, passed through unchanged, nothing written | MSG-P4-003 | AC6 |
| X7 | The same document version and type-table version is applied twice | The second apply is the first result and no column changes | None | AC5 |
| X8 | A role without Litigation right calls the action endpoint | 403 from this service before any read | MSG-P4-002 | Access test |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Consumes one published contract and its fake; adds no table, no event, no Schedule and no workflow of its own |
| Negotiable | Type codes, field codes, threshold, pass mark and the mapping table are data and contract, not code |
| Valuable | The court numbers, amounts and dates reach the legal action without retyping, and only after a person or a rule has passed them |
| Estimable | One client, one mapper, two repositories, one idempotency key and eight criteria |
| Small | Fits in two weeks with its contract, component and end-to-end tests |
| Testable | Every criterion runs against the P5 contract fake and the two rwb-case fakes with the legacy fixture values |

### 7. Acceptance criteria

```gherkin
Feature: Extraction for the stage 2 and 3 document types — the rwb-litigation fill

  Background:
    Given the document type table version "DOCTYPE-2026.12" is in force from 2026-12-31
    Given the field threshold is 0.80 and the accuracy pass mark is 0.90
    Given the rwb-document contract mock returns the checked fields of the case and the type it is asked for
    Given the rwb-case parameters mock returns the field threshold and the accuracy pass mark at their version in force

  Scenario: AC1 The confirmed court-filing facts reach the legal action (new, D-RCV-60)
    Given the rwb-document contract mock returns for case "RW-2026-000601" and type "COURT_FILING" the checked fields court_name in state "OK", black_case_no in state "OK", filing_date "2026-11-01" in state "CONFIRMED" and claim_amount "2400000.00" in state "OK"
    When "LIT-01" applies the checked fields of type "COURT_FILING" to legal action "LA-0601" of case "RW-2026-000601"
    Then legal_action.court_name, black_case_no, filed_date 2026-11-01 and claim_amount 2400000.00 hold the values the reader returned
    Then the source document ID, its doc_version and the tableVersion "DOCTYPE-2026.12" are written beside them in the same transaction as the row
    Then no other column of the row changes and no document, document_field, document_type or document_hub_parameter row is read or written

  Scenario: AC2 The judgment facts reach the legal action and the hearing date its hearing (new, D-RCV-60)
    Given the rwb-document contract mock returns for case "RW-2026-000601" and type "JUDGMENT" the checked fields red_case_no in state "OK", judgment_date "2027-03-05" in state "CONFIRMED" and judgment_amount "2400000.00" in state "CONFIRMED"
    And it returns for the same case and type "COURT_NOTICE" the checked field hearing_date "2026-11-01" in state "OK"
    When "LIT-01" applies both types to legal action "LA-0601"
    Then the legal action holds red_case_no, judgment_date 2027-03-05 and judgment_amount 2400000.00
    Then a hearing row of the legal action holds hearing_date 2026-11-01 and is_active true, and the hearing_type of that row is Not specified in the source documents (GAP-2836; ASM-4695)
    Then this apply sets no LOV-LEGAL-STATUS value and the case status does not change

  Scenario: AC3 A field in review is withheld and the previous value is kept (new, D-RCV-60)
    Given the rwb-document contract mock returns for case "RW-2026-000601" and type "JUDGMENT" the checked field judgment_amount of judgment "DOC-0602" in state "REVIEW" with confidence 0.7100, below the field threshold 0.80
    And legal action "LA-0601" already holds judgment_amount 2400000.00 from a confirmed read of the same field
    When "LIT-01" applies the checked fields of type "JUDGMENT" to legal action "LA-0601"
    Then judgment_amount is not written, the row keeps 2400000.00 and no other column of the row changes
    Then the judgment fact set is reported open with its review reason and judgment "DOC-0602" shows MSG-P5-003
    Then this service promotes no value in a state other than OK, CONFIRMED or CORRECTED and no value below the accuracy pass mark 0.90

  Scenario: AC4 The type and field set, the threshold and the pass mark are read at their version (new, D-RCV-60)
    Given the rwb-case parameters contract mock returns the field threshold 0.80 and the accuracy pass mark 0.90 at the version in force
    And the rwb-case reference-data contract mock returns LOV-DOC-TYPE with the eleven types, including COURT_FILING, JUDGMENT and COURT_NOTICE
    When the rwb-document contract mock answers with a checked-field set carrying tableVersion "DOCTYPE-2026.12" and the fields of type "COURT_FILING"
    Then the type code, the field codes and the table version are taken from the reader's answer and the threshold and the pass mark from the parameters answer
    Then the legal action carries "DOCTYPE-2026.12", the table version of the answer it was written from
    Then no type code, field code, threshold, pass mark, table version or valid-from date appears in the Java source or the module configuration
    Then this service writes no document, document_field, document_type or document_hub_parameter row and reads no v_ace_* view

  Scenario: AC5 A repeated apply applies once (new, D-RCV-60)
    Given legal action "LA-0601" holds the COURT_FILING facts of "DOC-0603" at doc_version 1 and table version "DOCTYPE-2026.12"
    When the same read of the same type is applied a second time for the same document ID, the same doc_version and the same table version
    Then no column of the legal action changes and the applied set still names one document version and one table version
    Then the second answer is the first result and the repeat is counted
    Then a read of "DOC-0603" at doc_version 2 writes the row once more and records the new version

  Scenario: AC6 A refusal of the reader changes nothing here (new, D-RCV-60)
    Given the rwb-document contract mock refuses the read for case "RW-2026-000605" of team "LIT-NE" with status 404 and MSG-P4-003
    When "LIT-01", an officer of team "LIT-BKK", applies the checked fields to legal action "LA-0605"
    Then the answer is status 404 with MSG-P4-003, no column of the legal action changes and no partial field set is written
    Given the rwb-document contract mock refuses the read for a role that carries no Documents R with status 403 and MSG-P4-002
    When the same apply is requested
    Then the answer is status 403 with MSG-P4-002 and nothing changes
    Given the rwb-document contract mock does not answer inside 2 s
    When the apply runs
    Then the answer is status 503 with MSG-GEN-006, nothing is written, and the GET is retried once with jitter and never twice on a write

  Scenario: AC7 A code that names no litigation column is not mapped and no party name is stored (new, D-RCV-60)
    Given the rwb-document contract mock returns for case "RW-2026-000601" and type "CONTRACT" the checked fields contract_no, party_names marked personal, contract_amount "2400000.00" and contract_date "2026-11-01"
    And it returns for the same case and type "MORTGAGE_DOCUMENT" the checked fields title_doc_no, mortgage_amount, registration_date and land_office
    When "LIT-01" applies the checked fields of both types to legal action "LA-0601"
    Then no column of legal_action, of hearing or of any other table of rwb_litigation holds a contract, credit-approval or mortgage field and none holds a party name
    Then the twelve unmapped field codes are counted in the apply result and their values appear in no log line, no event payload and no span attribute
    Then the party names appear in no row, no log line and no span attribute

  Scenario: AC8 The applied facts show on SCR-19 through the composite route (new, D-RCV-60)
    Given the gateway-bff composite route serves SCR-19 Litigation workspace for case "RW-2026-000601"
    And legal action "LA-0601" holds the court-filing and judgment facts of AC1 and AC2
    When "LIT-OFF" opens SCR-19
    Then SCR-19 shows court_name, black_case_no, red_case_no, claim_amount 2400000.00, filed_date, judgment_date and judgment_amount with the document ID and the doc_version each fact came from
    Then SCR-30 and SCR-31 open the hub's own surfaces read only and no screen calls an owner service directly
    Then no party name is shown and the withheld judgment_amount is shown open with its review reason
```

The eight criteria are new under D-RCV-60 and test only the S4 deliverable of this story. The eleven legacy criteria AC1 to AC11 of RWB-E2-025 — the court notice, the contract, the low confidence, the pass-mark proposal, the classification, the document before the version, the Buddhist Era date, the pattern mismatch, the reader filter, the write-once file and the scope refusal — belong to `RWB-P5-E2025-APP`, are written there word for word with their origin tags, and are not restated here. The shapes, the path, the state filter and the fakes this story consumes are `RWB-P5-E2025-CON`'s. The cross-service journey of the same values across rwb-document, rwb-litigation and rwb-case is the wave 2 integration harness's, and no criterion of this story claims it.

Two readings of the sources are stated here rather than hidden in the code. The columns that carry a fact, the source-stamp columns and the mapping rule are this story's design and are named by no source (GAP-2835; ASM-4689). The creation of a `hearing` row from an extracted `hearing_date` and the `hearing_type` it carries are named by no source either (GAP-2836; ASM-4695). The values of the examples are the legacy ones — case "RW-2026-000601", documents "DOC-0602", "DOC-0603" and "DOC-0605", the confidence 0.7100, the threshold 0.80, the pass mark 0.90, the amounts 2400000.00 — and the dates 2026-11-01 and 2027-03-05 are synthetic test data of the same fixture, not business values of any source.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The stage 2 and 3 types and their fields are those of the document type table version in force on the read date; the version is the one the reader reports and this service reads no type table of its own | Legacy RWB-E2-025 BR1; R-UNI-38; TSD S4 T3.1 (ASM-4689) |
| BR2 | A field in state REVIEW in the hub is never applied here; the column keeps its value and the fact set that needs it stays reported open with its review reason | Legacy BR2; RWB-P5-E2025-CON state filter; MSG-P5-003 |
| BR3 | A value below the accuracy pass mark is never promoted whatever state an upstream answer carries, and a review-only proposal takes effect only when its version is loaded | Legacy BR3 and AC4; CTL-08; DL11 |
| BR4 | Only a field code that names a column of `legal_action` or `hearing` is mapped; a code that names none is counted and recorded, and no amount or date is translated from one name into another | Legacy BR4; modified for the service boundary (GAP-2835; ASM-4689) |
| BR5 | The write is a write of facts: it sets no LOV-LEGAL-STATUS value, moves no case status and satisfies no litigation rule by itself | FSD S4 A2.4, A2.16; TSD S4 T4 (`R-LIT-16`, `R-LIT-44`) |
| BR6 | The apply is idempotent on the legal action, the document ID, the doc_version and the type-table version, in one transaction with the source stamps | Legacy section 12 idempotency; TSD S4 T3.0 |
| BR7 | No personal value is written, logged or put on a payload: `party_names` is never mapped, and masking is the hub's rule applied on its own answer | Legacy BR7; DF-DOC-015; CTL-11; DL26 (ASM-4691) |
| BR8 | No table of another service and no ACE table or view is read: the case, the parameters, the lists, the document fields and the decision log are reached only through their owners' contracts | DP-01, DP-05, DP-06, DP-07 |

### 9. State transitions

None. This story changes no case status and sets no LOV-LEGAL-STATUS value: `legal_action.status` stays where the legal-action stories put it, and the litigation transitions `R-LIT-01` to `R-LIT-79` remain the stage stories'. What this story writes is the fact columns of `legal_action` and, for a `hearing_date`, a `hearing` row that is active; `hearing.outcome` and `legal_action.lit_status` are untouched.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Reads and applies the checked fields of a legal action in scope (Litigation CRUA) |
| RW-ENFORCE, enforcement owner | Reads the applied facts of an action after judgment (Litigation CRU) |
| RW-LEGAL, legal counsel and RW-HEADLIT, head of litigation | Read and approve on the action (Litigation RA) |
| RW-NPAMGR, NPA and asset manager | Reads the applied facts (Litigation R) |
| RW-CONDUCT, conduct and QA officer | Reads the applied facts and the unmapped count (Litigation R) |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-LEG-001, DF-LEG-002 | legal_action | id, case_id | Read (scope and key) |
| DF-LEG-004 | legal_action | action_type | Read |
| DF-LEG-006 | legal_action | black_case_no | Write (from `black_case_no`) |
| DF-LEG-007 | legal_action | red_case_no | Write (from `red_case_no`) |
| DF-LEG-008 | legal_action | court_name | Write (from `court_name`) |
| DF-LEG-009 | legal_action | claim_amount | Write (from `claim_amount`) |
| DF-LEG-010 | legal_action | filed_date | Write (from `filing_date`) |
| DF-LEG-011 | legal_action | judgment_date | Write (from `judgment_date`) |
| DF-LEG-012 | legal_action | judgment_amount | Write (from `judgment_amount`) |
| DF-LEG-025, DF-LEG-026 | hearing | legal_action_id, hearing_date | Write (from `hearing_date`) |
| DF-LEG-027 to DF-LEG-029 | hearing | hearing_type, outcome, next_date | Read; `next_date` written only when an open hearing exists |
| Standard column | legal_action, hearing | is_active, state, version, created_at, created_by, updated_at, updated_by | Read and write (T3.0) |
| Source stamp (design, no BR ID) | legal_action | source_document_id, source_doc_version, source_table_version | Write (GAP-2835; ASM-4689) |
| Idempotency row (design, no BR ID) | rwb_litigation | apply key = legalActionId, documentId, docVersion, tableVersion | Write (BR6) |

**Mapping and non-mapping.** `COURT_FILING` → `court_name`, `black_case_no`, `filed_date`, `claim_amount`; `JUDGMENT` → `court_name`, `red_case_no`, `judgment_date`, `judgment_amount`; `COURT_NOTICE` → `court_name`, `black_case_no`, `hearing.hearing_date`. Not mapped, counted as the difference: `contract_no`, `party_names`, `contract_amount`, `contract_date`, `approval_no`, `approved_amount`, `approval_date`, `approval_level`, `title_doc_no`, `mortgage_amount`, `registration_date`, `land_office`. No parameter table, no type row and no field row is read: the type list and the two parameter values arrive through the rwb-case contracts (DP-06, DP-07), and `legal_action` and `hearing` are the only tables of `rwb_litigation` this story writes beyond the idempotency row.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-litigation (S4); base `/api/recovery/litigation/v1`.

| Method | Path | API ID | Documented shape | Access | Idempotency |
|---|---|---|---|---|---|
| POST | `/cases/{caseId}/legal-actions` | API-S4-002 | `LegalActionRequest` in, `LegalAction` out, applying the checked fields of a named type in the same transaction | Litigation C, scope applied | `Idempotency-Key` |
| PATCH | `/legal-actions/{legalActionId}` | API-S4-004 | `LegalActionUpdate` in, `LegalAction` out, applying the checked fields of a named type in the same transaction | Litigation U, scope applied | Apply key of section 11 (BR6) |
| GET | `/legal-actions/{legalActionId}` | API-S4-003 | `LegalAction` with pack, instruction, hearings and judgment, and the applied facts with their source document and version | Litigation R, scope applied | Not applicable |
| POST | `/legal-actions/{legalActionId}/hearings` | API-S4-005 | `HearingRequest` in, `Hearing` out; used when a `hearing_date` is applied to an action without an open hearing | Litigation U, scope applied | `Idempotency-Key` |

`POST /notices/{noticeId}/approve` (API-S4-001) is declared by `RWB-S4-E5001-CON` and is not re-declared here. The statuses of each row are the ones TSD S4 T-A.2 gives that operation — 401, 403, 404 and 503 everywhere, and 409 and 422 on the create and update operations — with the message IDs of section 14.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/document/v1/cases/{caseId}/checked-fields` | P5 rwb-document (RWB-P5-E2025-CON) | The checked fields of one type for the case; `documentType` required; one hop, 2 s, breaker, GET retry once with jitter |
| GET | `/api/recovery/case/v1/admin/parameters/{paramCode}` | P3 rwb-case (C `RWB-P3-E1042-CON`) | `EXTRACT_FIELD_THRESHOLD` and `EXTRACT_ACCURACY_PASS` at their version |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case (C `RWB-P3-E1043-CON`) | LOV-DOC-TYPE with the eleven types, and LOV-HEARING for the hearing type of a created row |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case, its team and its queue behind the scope filter; faked, and in no C row of the plan (ASM-4692) |

A failed read maps to 503 with MSG-GEN-006 naming the unavailable owner, and a refusal never returns a partial field set (section 5).

#### 12.3 Events published

| Event | Topic | Owner | Declared schema |
|---|---|---|---|
| None | `rwb.litigation.events.v1` (the service's own topic) | P7 rwb-decision for the shared `rwb.decision-record.v1`; this service for its own topics | The service has no event in the ownership map, and this slice declares none: the facts reach their readers on the owners' own reads, and no `DocumentFieldsApplied` event is invented (ASM-4694) |

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| None | `rwb.document.events.v1` carries `rwb.document.DocumentFieldsExtracted.v1` | P5 rwb-document | Not consumed here: the apply is triggered by the officer's request, and the extraction event is rwb-case's to consume. A change of the type-table version reaches this service on its next read (ASM-4694) |

#### 12.5 Workflows and activities

| Name | Kind | Queue | Contracted use |
|---|---|---|---|
| `LitigationWorkflow` | Workflow | `rwb-litigation` | The service's one workflow, named by the ownership map and built by the litigation stage stories; this slice registers nothing on it |
| None in this story | — | — | The apply is one synchronous request with one consumed read; DP-10 is carried as a prohibition and no activity, timer or Schedule is declared (ASM-4694) |

#### 12.6 Schedules

| Schedule | Workflow | Queue | Interval | Note |
|---|---|---|---|---|
| None | `LitigationWorkflow` | `rwb-litigation` | — | This slice registers no Temporal Schedule and no cron entry; the litigation timers the service runs are the stage stories' and the intake Schedule JOB-12 is rwb-document's |

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| `legal_action` | S4 (`rwb_litigation`) | DF-LEG-001 to DF-LEG-014; this story writes the fact columns of section 11 and the source stamps |
| `hearing` | S4 (`rwb_litigation`) | DF-LEG-024 to DF-LEG-029; this story writes `hearing_date`, `next_date`, `legal_action_id` and the standard columns of a created row |
| idempotency and inbox library tables | PLT library, created in `rwb_litigation` | The apply key of BR6, in `rwb_litigation` only |

`document`, `document_field`, `document_type` and `document_hub_parameter` are P5's in `rwb_document`; `recovery_case`, `parameter_catalog`, `reference_row` and `lov_value` are P3's; `decision_log_entry` is P7's; the `recovery.v_ace_*` views are read by rwb-source-data alone. None of them is declared as this story's table (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| checked-fields fake | The read for case "RW-2026-000601" and types "COURT_FILING", "JUDGMENT" and "COURT_NOTICE" with `red_case_no` in OK, `judgment_amount` absent because it is in REVIEW, `hearing_date` in OK, and a document of team "LIT-NE" for the 404 case | This story's contract and end-to-end tests; the S2 slice's |
| parameters and reference-data WireMock | `EXTRACT_FIELD_THRESHOLD` 0.80, `EXTRACT_ACCURACY_PASS` 0.90, LOV-DOC-TYPE with the eleven types, LOV-HEARING, a delayed answer beyond 2 s and a 503 | Contract and component tests |
| rwb-case case WireMock | The case, its team and its queue for "RW-2026-000601" and for the case of team "LIT-NE", and a delayed answer | Contract tests |
| composite route fake | SCR-19 merged from the case read and this service's legal-action read, with the fact source of each value | AC8 and the screen test |
| drift and absence tests | Compare every fake and the mapping table with the contract and fail on a path, a status, a field name, a state or a code count mismatch | Build pipeline |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 4 consumed | The legal-action operations of 12.1; the checked-fields read, the two rwb-case admin reads and the case read of 12.2; one hop and 2 s on every cross-service call |
| Kafka | 0 published, 0 consumed | The service's own topic `rwb.litigation.events.v1` carries no event of this slice |
| Temporal | 0 declared, 1 named | `LitigationWorkflow` on queue `rwb-litigation`, named and not changed |
| File | None | No byte and no document body is touched; only field values cross the boundary |

### 13. Solution plan

**Package.** folder `recovery/litigation/extract`, Java package `th.co.scb.ace.workbench.recovery.litigation.extract`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `LitigationAndEnforcementController` | Controller | The operations of 12.1; validation, scope, rights and error mapping |
| `CheckedFieldsClient` | Client | The one-hop read of 12.2 with a 2 s timeout, a breaker and a GET retry once with jitter |
| `LegalActionFieldMapper` | Service | The mapping table of section 11, the state and pass-mark filter, and the unmapped count |
| `LegalActionRepository`, `HearingRepository` | Repository | The read and write of `legal_action` and `hearing` in `rwb_litigation` only, with the source stamps |
| `ApplyKeyRepository` | Repository | The idempotency row of BR6 and the repeat count |

**Pattern application** (§R5.5)

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_litigation`; never read another service's tables; no document row, no `v_ace_*` view | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON (prohibition: no event of this slice) |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON (prohibition: no Schedule, no activity) |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C RWB-P5-E2025-CON from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-09 and DP-10 are carried as prohibitions: the slice publishes no event and registers no Schedule, and the library and kit stand in no build row (ASM-4692, ASM-4694). DP-11 is the whole point of the story: the legacy in-process `DocumentFieldReader` becomes one hop with a published shape, a fake and a 2 s timeout, so this slice builds on Day 1 against RWB-P5-E2025-CON.

**Build steps**

1. Build `CheckedFieldsClient` against the P5 fake and the drift test of 12.8; no statement may name `rwb_document`.
2. Build `LegalActionFieldMapper` with the mapping table as one data row set and a unit test per mapped code and per unmapped code.
3. Add the source-stamp and idempotency columns on the service's own Flyway sequence, owned by the S4 baseline stories, with the apply key of BR6.
4. Write the apply in one transaction with the local decision record and the repeat count; prove AC3 and AC5.
5. Prove AC4 with the parameters and reference-data fakes and a build check that fails on a code, a threshold, a pass mark or a version in the source.
6. Prove AC6 with the 404, 403 and timeout fakes, and AC8 with the composite route fake.

**Feature flag.** `rwb.litigation.extract-stage23`. Off: the apply offers no type, nothing is read from rwb-document and no column is written.

**Done when** the tests in section 16 pass and the applied-fact report of the 60-document sample runs against the P5 fake with the unmapped count attached.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | A document of the type has a field in REVIEW | Some fields need checking. The document is in the review queue. |
| MSG-P4-002 | The caller lacks the right on the action or on the document | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case or the document is outside the caller's scope | This case is not in your scope. |
| MSG-GEN-006 | The document hub or rwb-case does not answer inside 2 s | {system} is not available. Your request is queued and will be retried. |

Thai text for each message follows decision DL10. This story adds no message ID of its own; the four are the legacy ones and the platforms'.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-19 Litigation workspace | Read and edit; applied | Sees the court numbers, amounts and dates of the action with the document and version each came from; applies a type; sees a withheld fact set open with its review reason |
| SCR-30 Case documents (hub) | List | Read only here: shows the new types with their fields and confidence and MSG-P5-003 on documents with fields in review |
| SCR-31 Document review queue (hub) | List; reviewed | Not built here: the officer checks and corrects marked fields on the hub's screen, which is the only place a REVIEW field is cleared |

SCR-19 is listed first in E5 and the two hub screens are P5's; all three are reached through the gateway-bff composite route (DP-19) and this story serves the read model only (ASM-4693).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-025-12 | AC6 (legacy Access) | Component | RW-REFADM holds no Documents R; the checked-fields read is refused with 403 and MSG-P4-002 and the apply writes nothing |
| TC-E2-025-01 | AC2, AC3 (legacy AC1) | End to end | 10 masked court notices of the sample; `hearing_date` reaches the hearing row and `court_name` and `black_case_no` the action |
| TC-E2-025-02 | AC7 (legacy AC2) | Contract | Contract "DOC-0601" on case "RW-2026-000601": `contract_amount` and `party_names` map to no litigation column, are counted, and no party name is stored |
| TC-E2-025-03 | AC3 (legacy AC3) | End to end | `judgment_amount` at confidence 0.7100 in REVIEW; withheld, the previous 2400000.00 kept, the set open with MSG-P5-003 |
| TC-E2-025-04 | AC3, AC4 (legacy AC4) | End to end | 10 sample judgments with 8 amounts correct and the pass mark 0.90; the proposal changes nothing until it is loaded |
| TC-E2-025-05 | AC3, AC7 (legacy AC5) | End to end | 50 documents of the five new types; a type that maps nothing and an item the classifier could not place write no column |
| TC-E2-025-06 | AC3 (legacy AC6) | End to end | "DOC-0603" received 2026-12-26, before the valid-from date; no column changes, reason UNKNOWN_TYPE |
| TC-E2-025-07 | AC2 (legacy AC7) | End to end | A judgment date read as "5 March 2570 BE"; `judgment_date` 2027-03-05 on the row |
| TC-E2-025-08 | AC3 (legacy AC8) | Contract | A value failing its pattern arrives in REVIEW with confidence 0.9200; nothing is applied and the set is reported open |
| TC-E2-025-09 | AC2, AC3 (legacy AC9) | Contract | A judgment with `red_case_no` in OK and `judgment_amount` in REVIEW: the mapped field is applied, the amount is never promoted |
| TC-E2-025-10 | AC5 (legacy AC10) | End to end | Write-once judgment "DOC-0604": the facts are applied and this service writes no document row, hash or storage reference |
| TC-E2-025-11 | AC6 (legacy AC11) | Contract | Document "DOC-0605" of team "LIT-NE" read by an officer of team "LIT-BKK": 404 with MSG-P4-003 and no column written |
| TC-S4-E2025-APP-01 | AC1, AC5 | Integration | The court-filing facts applied once per document ID, doc_version and type-table version; a repeat writes nothing and a new doc_version applies once more |
| TC-S4-E2025-APP-02 | AC4 | Contract | The parameter and reference-data answers at their version, and a build check that fails on a type code, a field code, a threshold, a pass mark or a valid-from date in the source |
| TC-S4-E2025-APP-03 | AC6 | Component | 503 with MSG-GEN-006, nothing written, and one GET retry with jitter and no retry on the write |
| TC-S4-E2025-APP-04 | AC7, AC8 | Component | The composite route fake merging SCR-19 with the seven facts and their document versions, the unmapped count and the open fact set |

The twelve identifiers TC-E2-025-12 and TC-E2-025-01 to TC-E2-025-11 are legacy-carried: this slice answers the S4 half of each, at Contract where the row proves the reader contract and at End to end where the row proves the extraction-to-legal-action path. The legacy level "System" maps to "End to end" and "Access" to "Component". The four cases TC-S4-E2025-APP-01 to TC-S4-E2025-APP-04 are new for the criteria that no legacy row exercises. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID, and the `-ITG` copies of these rows belong to the wave 2 integration harness.

### 17. Guardrails

- No business value in code: type codes, field codes, the table version, the threshold, the pass mark and the two lists are rows read at their version; a build check fails on a type code, a field code, an amount, a date, a threshold, a pass mark or a valid-from date in the Java source or the module configuration.
- No personal data in logs, tests, workflow inputs, events or `rwb_litigation`: `party_names` is never mapped, stored, logged or put on a message, and a property test places a synthetic party name in the reader's answer and asserts that it appears in no row, no log line and no span attribute (ASM-4691).
- ACE data only through the owner's contract: no component reads an ACE table or a `recovery.v_ace_*` view, and the `rwb_litigation` login holds no `v_ace_*` grant (DP-01, DP-05).
- No read of another service's tables and no cross-schema join: `document`, `document_field`, `document_type` and `document_hub_parameter` (P5), `recovery_case`, `parameter_catalog`, `reference_row` and `lov_value` (P3) and `decision_log_entry` (P7) are reached only through their owners' contracts, and the boundary test fails the build on any statement outside `rwb_litigation`.
- Only checked values move: a `REVIEW` field, a value below the pass mark, a type not in force and an item with reason `UNKNOWN_TYPE` are withheld, and no code path promotes them.
- One hop and a 2 s budget on every consumed read, with a breaker and no call chain; a repeat is the same apply key and never a silent second write.
- No event, no topic producer, no outbox row and no Schedule in this slice (DP-09 and DP-10 as prohibitions), and no case status and no LOV-LEGAL-STATUS value is written.
- The screens are read only for the hub's fields: SCR-19 shows what this service wrote, and no screen writes a checked field.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-006 | Fields are extracted into the index for the agreed types, in Thai and in English; this story consumes them on the litigation side by filling the legal action | Business Requirements Program v4, section 5.5; Epic 2 v2, section 3.5 | FEAT-DCM-22 | 13 Manage documents and correspondence | R-UNI-38, CTL-08, CTL-11, CTL-12 | TC-E2-025-01, TC-E2-025-07, TC-E2-025-09, TC-E2-025-10, TC-S4-E2025-APP-01 |
| REQ-DCM-005 | Documents are classified with a confidence and anything below the threshold goes to a review queue; this story withholds what the queue still holds | Business Requirements Program v4, section 5.5; Epic 2 v2, section 3.5 | FEAT-DCM-22 | 13 Manage documents and correspondence | R-UNI-38, CTL-08 | TC-E2-025-02, TC-E2-025-03, TC-E2-025-04, TC-E2-025-05, TC-E2-025-06, TC-E2-025-08, TC-E2-025-11 |
| REQ-DCM-017 | The hub answers an electronic discovery request for a named population; carried by the plan's requirement list and not by the legacy traceability table, and out of scope of the legacy key | Business Requirements Program v4, section 5.5; Epic 2 v2, section 3.5 | FEAT-DCM-22 | 13 Manage documents and correspondence | None | None here: the discovery answer is the document hub's (ASM-4690) |
| REQ-DCM-018 | A document produced from the hub carries what a court needs to accept it; carried by the plan's requirement list and not by the legacy traceability table, and out of scope of the legacy key | Business Requirements Program v4, section 5.5; Epic 2 v2, section 3.5 | FEAT-DCM-22 | 13 Manage documents and correspondence | None | None here: the court-evidence attributes are the document hub's (ASM-4690) |

The four requirements are the plan's list for this story. The legacy traceability table of RWB-E2-025 carries REQ-DCM-006 and REQ-DCM-005 only and its out-of-scope list puts REQ-DCM-017 and REQ-DCM-018 outside the key, so the two are carried with the plan's list and answered by the hub. Feature FEAT-DCM-22 and L3 process 13 are the legacy key's and are kept unchanged; this story answers them on the S4 side of the same key.

| Item | What it covers in this story |
|---|---|
| Legacy key RWB-E2-025 | The S4 deliverable: the checked fields applied to `legal_action` and `hearing`, the withheld field and the value the row keeps, the version and parameter reads, the idempotent write, the refusals, the unmapping and the read model |
| RWB-P5-E2025-APP (P5) | The classification, the extraction, the evaluation runner, the review queue, the write-once rule and the eleven legacy criteria AC1 to AC11 word for word |
| RWB-P5-E2025-CON | The checked-fields read, the `CheckedFieldSet` and `CheckedField` shapes, the state filter, the masking rule, the error envelope and the fake this story builds against |
| The wave 2 integration harness | The end-to-end proof of the same values across rwb-document, rwb-litigation and rwb-case, which no criterion of this story claims |
| RWB-S2-E2025-APP | The sibling slice of the same key: the same reader applied to the treatment row |
| RWB-S4-E5001 to RWB-S4-E5022 | The legal action, notice, pack, filing, hearing, judgment, enforcement and auction stories this story supplies facts to |
| DP-01, DP-13 | The owner's schema `rwb_litigation` and the base `/api/recovery/litigation/v1` |
| DP-06, DP-07 | The parameters and reference-data reads of rwb-case at their version (ASM-4692) |
| DP-09, DP-10 | The two prohibitions: no event and no Schedule in this slice (ASM-4694) |
| DP-11, DP-19 | One hop with a 2 s timeout on the reader, and SCR-19 behind the gateway-bff composite route (ASM-4693) |
| ADR-013, ADR-014, ADR-015, ADR-020 | 19 services inside ACE, a schema and a login per service, the Kafka platform this story adds no producer to, and contract-first REST with one hop |

### 19. Out of scope

- Classification, extraction, the extractors, the normalizer, the evaluation runner, the review queue, the write-once rule, the document type table and the parameters: the document hub's, in `RWB-P5-E2025-APP` and `RWB-P5-E2025-CON`.
- Writing the same values into the treatment record: the S2 slice, `RWB-S2-E2025-APP`.
- Litigation pack assembly and the defect list check (`R-LIT-16`, `R-LIT-17`, FEAT-LIT-04 and FEAT-LIT-05) and the legal-action, notice, filing, hearing, judgment and enforcement stories that read these facts.
- Generating contract, credit approval and mortgage documents (legacy RWB-E2-026).
- Electronic discovery and the court evidence attributes of REQ-DCM-017 and REQ-DCM-018, which the plan carries here and the hub answers.
- Any event, topic, Schedule, workflow or case status of this slice; any read of an ACE table or view; any change to `lit_status`, `outcome` or the hearing list of obligations.

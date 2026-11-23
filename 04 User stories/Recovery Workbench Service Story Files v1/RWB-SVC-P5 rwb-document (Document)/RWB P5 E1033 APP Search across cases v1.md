# RWB-P5-E1033-APP Search across cases

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1033-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-033 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP11, DP15, DP19 |
| Parallel lane | L-P5-G |
| Ready to start | After RWB-P5-E1024-APP, RWB-P5-E1049-APP |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P5-E1024-APP, RWB-P5-E1049-APP, RWB-P5-E1053-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-001, FR-P5-002, FR-P5-009, FR-P5-010, FR-P5-013, FR-P5-014, FR-P5-028, FR-P5-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: search across cases moved into `rwb-document` with the schema `rwb_document`, the REST base `/api/recovery/document/v1`, the topic `rwb.document.events.v1` and the gateway-bff composite route; the case scope, the masking decision, the parameters, the reference lists, the access record and the migration are rebased on the target contracts and libraries. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **a search across all cases in my scope by document type, date range, extracted field and free text, with every search written to the access log**, so that **I find a document in seconds without opening cases one by one, and every look at personal data can be audited**.

Inside `rwb-document` this is the cross-case search capability of the document service:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`. No Kafka event and no workflow is used by a search.
- One operation is provided, `GET /documents`, the cross-case search of TSD P5 API-P5-009 (12.1). It reads `document`, `document_field`, `document_text` and `document_type` in `rwb_document` and nothing outside it (DP01). `document_text` rows carry `document_id` once the intake item that produced them is attached, which RWB-P5-E1032-APP and RWB-P5-E1049-APP make true; a page of text that is still held in intake is not searchable across cases.
- The case scope (legacy `CaseDirectory.caseIdsInScope`) is one REST hop to `rwb-case`, and the masking decision (legacy `mayReadUnmasked`) is one REST hop to `rwb-access`; both are called with a fake and a 2 s timeout (DP11) and no case, account or role table of another service is read. Neither contract is in the Work Package contract rows, which are copied as they stand (GAP-2335; ASM-3884, ASM-3885).
- The four search parameters `SEARCH_MAX_RESULTS`, `SEARCH_PAGE_SIZE`, `FREE_TEXT_MIN_CHARS` and `FREE_TEXT_MAX_CHARS` arrive through the parameters contract and client library of `rwb-case` (DP06, H RWB-PLT-E1042-CON, C RWB-P3-E1042-CON); the rows they resolve to are in `document_hub_parameter` in `rwb_document`, which the Ownership Map gives to P5. The document-type list and the other LOV lists arrive through the reference-data contract (DP07, H RWB-PLT-E1043-CON, C RWB-P3-E1043-CON); the type table `document_type` itself is P5's own table and is read locally in the version in force (RWB-P5-E1025-APP).
- Each search is one append to the service's local decision-record chain through the DP03 library and one record on `rwb.decision-record.v1`, which `rwb-decision` collects into the central ledger; the free text term is carried as its SHA-256 hash. The record code of a search access event and the acknowledgement the request waits for are Not specified in the source documents (GAP-2334; ASM-3882).
- The page is published by gateway-bff through the composite route of DP19 (H RWB-PLT-N001-CON), which asks this service one hop for what is on screen; the search indexes are one step in the per-service Flyway sequence (DP15, H RWB-PLT-E1044-CON).
- The database login is one per service (DP02) and its name is Not specified in the source documents (GAP-2334; ASM-3882); this story uses the phrase "the rwb-document login" and never a shared login.

The legacy behaviour is carried unchanged: the same user story, rationale, preconditions, flow, exception paths, business rules, authority, data fields, ten acceptance criteria with their values, six messages and eleven test cases, rebased on the target service's schema, parameters, reference data and two contract hops.

### 2. Business rationale

Legal, audit and recovery questions span many cases: every appraisal above a value, every notice from one court, every document naming a guarantor. Today each case folder is opened by hand (FSD P5 A2.6). This story searches the document index, the extracted fields and the OCR text across the cases the user may see, masks personal data the role may not see, and records each search. It meets REQ-DCM-001 (documents found by their type, date and extracted fields) and REQ-ACA-006 (every read of the document store written to the access log), under control CTL-09 and CTL-11, and it is the read that makes an audit population answerable at all (REQ-DCM-017, whose export is Epic 2).

The realignment changes the mechanics, not the business rule:

1. One schema, one base: the query runs in `rwb_document` over the four P5 tables and never over a `recovery.*` table or another service's schema (DP01). The legacy join to `recovery_case` for the scope and the case number becomes an answer on the `rwb-case` contract (DP11).
2. The in-process scope call `CaseDirectory.caseIdsInScope` becomes the case-list read of `rwb-case`, one hop with a 2 s timeout and a breaker, and the in-process masking call `mayReadUnmasked` becomes the authorise decision of `rwb-access` (DP11). Both are faked from Day 1, so the search builds before either service is ready.
3. The PII access log write becomes the local decision-record append of DP03 with the record published on `rwb.decision-record.v1`; the access log is held in the append-only decision log in the target (FEAT-ACA-08), the record is written in the request, and a search whose record is not acknowledged returns no row (AC9).
4. The parameters leave the code path and arrive through the parameters contract and client library of `rwb-case` (DP06). The rows stay in `document_hub_parameter` in this schema; the values are unchanged from the legacy story.
5. The LOV lists arrive through the reference-data contract (DP07); the type table and its field definitions are read locally in the version in force, so a field condition is always checked against the fields of the type table in force.
6. The legacy `V1_5_033__document_search_indexes.sql` becomes one step in the per-service Flyway sequence of `rwb_document` (DP15), with no baseline and no shared migration file.
7. The page is published to the browser by the gateway-bff composite route (DP19), which calls this service one hop; no screen chains calls to the case service or the access service, and the row opens the DocumentDetailPanel of RWB-P5-E1024-APP.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-PLT-E1027-CON | The decision-record library and the `rwb.decision-record.v1` topic: one append per search, acknowledged before any row is returned (DP03) |
| RWB-PLT-E1042-CON | The parameters client library, so the four `SEARCH_*` values are read and never typed in code (DP06) |
| RWB-PLT-E1043-CON | The reference-data client library for LOV-DOC-TYPE and the other lists the criteria use (DP07) |
| RWB-PLT-E1044-CON | The per-service Flyway sequence that carries the search indexes as one step in `rwb_document` (DP15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that publishes the Document search page and asks this service one hop (DP19) |
| RWB-P5-E1024-APP | The store and index: `document` and `document_field` populated, active and versioned, with the case number on the row |
| RWB-P5-E1049-APP | The OCR pipeline: `document_text` populated for every read page and linked to the document once the intake item is attached |
| RWB-P5-E1053-CON | The extraction contract: the field names and values in `document_field` are the agreed ones, with their confidence |
| RWB-P3-E1042-CON | The parameters contract of `rwb-case`, read through the client library of DP06 |
| RWB-P3-E1043-CON | The reference-data contract of `rwb-case`, read through the client library of DP07 |

Business preconditions carried from RWB-E1-033, unchanged in value:

- Documents and extracted fields are in the index (RWB-P5-E1024-APP), OCR text is in `document_text` (RWB-P5-E1049-APP), and extracted fields carry names from the type table and a confidence (RWB-P5-E1053-CON).
- Masking rules loaded (DL26). Assumed until Compliance provides them: RW-LITOFF, RW-LEGAL and RW-AUDIT see party names in document text unmasked; every other role sees them masked.
- Parameters loaded in `document_hub_parameter`: SEARCH_MAX_RESULTS = 1000, SEARCH_PAGE_SIZE = 50, FREE_TEXT_MIN_CHARS = 3, FREE_TEXT_MAX_CHARS = 100 (assumed; DL11), read through the parameters contract of DP06.
- Every search is recorded in the append-only decision log and the append is acknowledged before a row is returned (FEAT-ACA-08; ASM-3882).
- The user holds Documents R and the case IDs of the search are in their scope. Feature flag `rwb.document.search` is on; the legacy flag `rwb.dochub.search` is retired with the monolith.

### 4. Flow

1. Litigation officer: opens Document search from the Documents menu and enters a type, a stored date range, a field condition (field, operator, value) and or a free text term. The page is published by gateway-bff through the composite route of DP19; the browser calls `/api/recovery/document/v1/documents` once.
2. `DocumentSearchController`: accepts the criteria, applies the guard the service template holds, and passes the caller, the role codes and the criteria to the service.
3. `DocumentSearchService`: validates the criteria: at least one criterion, date order, free text length, field in the type's field list, operator in the allowed set (BR4, BR5).
4. `DocumentSearchService`: asks `rwb-access` through the authorise contract whether the role may search a personal field or free text (legacy `mayReadUnmasked`, field classes PARTY_NAME, ACCOUNT_NO, ID_NO); a refusal ends the request with 422 and MSG-P5-020, and no query runs. One hop, 2 s timeout, breaker (DP11).
5. `DocumentSearchService`: gets the case IDs in the caller's scope from the case-list read of `rwb-case` (legacy `caseIdsInScope`; the filter is empty for scope ALL), one hop, 2 s timeout, breaker (DP11). An empty answer returns the empty state and still records the search.
6. `DocumentSearchRepository`: one query over active `document` rows joined to `document_field` for the field condition and to `document_text` for the free text, newest stored date first, capped at SEARCH_MAX_RESULTS; the page is served at SEARCH_PAGE_SIZE. The case number is taken from the case answer of step 5, not from a case table.
7. `DocumentSearchService`: builds each row: case number, document type, stored date, source, the matched field or a text snippet of 60 characters with the term highlighted and other personal identifiers masked (BR2).
8. `DocumentSearchService`: appends the access record for the search through the decision-record library of DP03 (user, role, criteria with the free text term as a SHA-256 hash, result count, case IDs returned), waits for the acknowledgement, and only then returns the page; the record is published on `rwb.decision-record.v1` for the central ledger in `rwb-decision`.
9. Front end: shows the first page of 50 rows; the user opens a row in DocumentDetailPanel (RWB-P5-E1024-APP). A row is a metadata read of that document, recorded by the same rule.

The record is written before the rows are released, so no search is answered without its record (REQ-ACA-006; FEAT-ACA-08).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The role's masking rule hides party names and the user searches free text or a personal field | Refused with 422; nothing searched | MSG-P5-020 | AC4 |
| X2 | No criterion entered | Refused with 422 | MSG-GEN-001 | AC5 |
| X3 | Date from after date to | Refused with 422 | MSG-GEN-003 | AC6 |
| X4 | Free text shorter than 3 or longer than 100 characters | Refused with 422 | MSG-GEN-002 | AC7 |
| X5 | More than SEARCH_MAX_RESULTS documents match | The first 1000 by date are returned with a capped flag | MSG-P5-021 | AC8 |
| X6 | The access record is not confirmed | Results are not returned; 503 | MSG-P5-019 | AC9 |
| X7 | Nothing matches | Empty state | None | AC10 |
| X8 | A role without Documents R searches | Refused with 403 | MSG-P4-002 | TC-E1-033-11 (Access) |
| X9 | The `rwb-case` case-list read does not answer within 2 s or its breaker is open | Refused with 503; nothing searched and no record; the breaker shields the case service | MSG-GEN-006 (system "Case service") | TC-E1-033-02 (target path) |
| X10 | The `rwb-access` authorise read does not answer within 2 s or its breaker is open | Refused with 503; nothing searched; the masking decision is never assumed | MSG-GEN-006 (system "Access service") | TC-E1-033-04 (target path) |

Three target-service notes:

- A 503 on X9 or X10 is a refusal, not a partial answer: no criterion is evaluated in part, no row is returned and no access record is written, because nothing was read.
- A search refused at X1, X2, X3, X4 or X8 writes no access record: the append of step 8 happens only for a search that runs. The refusal itself stays in the request log of the shared edge, which is not this service's control.
- The access record of step 8 replaces the legacy PII access log call: the ACE common module still logs the request at the edge, but the search record is the append of DP03, which is what AC9 waits for (ASM-3882).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the index (RWB-P5-E1024-APP), the OCR text (RWB-P5-E1049-APP), the extraction contract (RWB-P5-E1053-CON) and the two faked contract reads, all earlier or contract work |
| Negotiable | Limits, page size, text length and the masking rules are data; the criteria set can grow |
| Valuable | A cross-case question takes one search instead of opening each case |
| Estimable | One operation, one service, one query with three indexes, one page |
| Small | Fits within two weeks with its tests |
| Testable | Each criterion below is one test case in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Search across cases

  Background:
    Given 500 synthetic documents indexed across 120 cases
    Given 60 of them are "APPRAISAL_REPORT", 14 with appraised_value above 5,000,000, 9 of those stored in October 2026
    Given user "TEST-LIT-01" holds RW-LITOFF with scope ALL
    Given the rwb-case contract mock returns the 120 case IDs in the scope of "TEST-LIT-01" for scope ALL, with their case numbers
    Given the rwb-access contract mock returns that "RW-LITOFF" may read "PARTY_NAME" unmasked

  Scenario: AC1 Search by field (legacy RWB-E1-033 AC1)
    Given "TEST-LIT-01" is on the Document search page
    When "TEST-LIT-01" searches type "APPRAISAL_REPORT", field appraised_value greater than 5,000,000, stored from 1 October 2026 to 31 October 2026
    Then exactly the 9 matching documents list with case number, type, stored date and the field value
    Then the response arrives within 2 seconds

  Scenario: AC2 Role limit (legacy RWB-E1-033 AC2)
    Given user "TEST-LIT-02" holds RW-LITOFF with scope TEAM on team "MTG-BKK-LIT", whose cases are all product group "MORTGAGE"
    Given 40 of the 500 documents are on "HIRE_PURCHASE" cases
    Given the rwb-case contract mock returns the case IDs in the scope of "TEST-LIT-02" for team "MTG-BKK-LIT" with product group "MORTGAGE"
    When "TEST-LIT-02" searches type "COURT_NOTICE" with no date
    Then no document on a "HIRE_PURCHASE" case appears
    Then the system writes one access event "DOCUMENT_SEARCH" with the user, the criteria, the result count and the case IDs returned

  Scenario: AC3 Free text (legacy RWB-E1-033 AC3)
    Given the OCR text of 3 documents holds the synthetic guarantor name "SYN GUARANTOR ONE"
    When "TEST-LIT-01" searches the free text "SYN GUARANTOR ONE"
    Then the 3 documents list with a snippet in which the name is highlighted
    Then the access event holds the SHA-256 hash of the term and not the term

  Scenario: AC4 Free text refused for a masked role (legacy RWB-E1-033 AC4)
    Given user "TEST-CO-01" holds RW-CASEOWN, whose masking rule hides party names
    Given the rwb-access contract mock returns that "RW-CASEOWN" may not read "PARTY_NAME" unmasked
    When "TEST-CO-01" searches the free text "SYN GUARANTOR"
    Then the system refuses the request with 422 and MSG-P5-020 naming "document text"
    Then no query runs

  Scenario: AC5 No criterion (legacy RWB-E1-033 AC5)
    Given "TEST-LIT-01" is on the Document search page
    When "TEST-LIT-01" searches with every criterion empty
    Then the system refuses the request with 422 and MSG-GEN-001 naming "a search criterion"

  Scenario: AC6 Date range in the wrong order (legacy RWB-E1-033 AC6)
    Given "TEST-LIT-01" is on the Document search page
    When "TEST-LIT-01" searches stored from 31 October 2026 to 1 October 2026
    Then the system refuses the request with 422 and MSG-GEN-003

  Scenario: AC7 Free text length boundary (legacy RWB-E1-033 AC7)
    Given "TEST-LIT-01" is on the Document search page
    When "TEST-LIT-01" searches the free text "ab" and then the free text "abc"
    Then the system refuses "ab" with 422 and MSG-GEN-002 showing 3 and 100
    Then "abc" runs

  Scenario: AC8 More results than the limit (legacy RWB-E1-033 AC8)
    Given 1,250 documents of type "DEMAND_LETTER" in the user's scope
    When "TEST-LIT-01" searches type "DEMAND_LETTER"
    Then the first page of 50 rows returns with total 1000 and capped true
    Then MSG-P5-021 shows with the count 1000

  Scenario: AC9 Access log not confirmed (legacy RWB-E1-033 AC9)
    Given the PII access log does not confirm writes
    When "TEST-LIT-01" searches type "COURT_NOTICE"
    Then the request returns 503 with MSG-P5-019
    Then the system returns no result row

  Scenario: AC10 Nothing matches (legacy RWB-E1-033 AC10)
    Given no document holds the free text "NO SUCH TEXT"
    When "TEST-LIT-01" searches it
    Then the page shows the empty state "No documents match this search." and the action "Clear the search"
    Then the access event records a result count of 0
```

Every Given, When and Then line above is the legacy line unchanged. The cross-service parts are mocked by the two added Background Givens on the `rwb-case` and `rwb-access` contracts and by the per-scenario Givens in AC2 and AC4. In AC9 the "PII access log" is the append of DP03 into the local decision-record chain: the request waits for the library's acknowledgement, and an unacknowledged append is the 503 the criterion fixes (ASM-3882).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Results hold only active documents on cases in the user's scope | CTL-09; FEAT-DCM-20 |
| BR2 | Personal fields and free text are searchable only by roles that see them unmasked; snippets mask other personal identifiers | CTL-11; DL26; masking rules reference table |
| BR3 | Every search is written to the access log before results are returned; a free text term is logged as a hash | REQ-ACA-006; CTL-11 |
| BR4 | Field conditions use the field names and data types of the type table in force | RWB-P5-E1025-APP; DL19 |
| BR5 | Result limit, page size and free text length are parameters | Document hub parameter table (New); DL11 |
| BR6 | The date criterion is the stored date of the document | FSD P5 A2.6 |

Target-service statements that make the rules hold in `rwb-document`:

- BR1 is executed in `rwb_document` by the `is_active` predicate on `document` and by the case-ID set of the case-list read; no case row is copied and no `rwb_case` table is read (DP01, DP11). A case that leaves the caller's scope stops matching on the next search, because the set is fetched per request and never cached across requests.
- BR2 is executed by the authorise decision of `rwb-access` before the query (DP11) and by `SnippetBuilder`, which masks every other identifier in the 60-character snippet; the masking rule set is versioned data, not code.
- BR3 is executed by the decision-record append of DP03 in the request path: the record is acknowledged before the page is released, the free text term is stored as its SHA-256 hash, and the record is published on `rwb.decision-record.v1` for the central ledger.
- BR4 is executed by reading `document_type` in the version in force (`valid_from`, `valid_to`) and by comparing the field condition with `field_definitions` (DF-REF-224) before any SQL is built; an unknown field is refused as a criterion error, not ignored.
- BR5 is executed by the parameters contract of DP06: the four `SEARCH_*` rows resolve in `document_hub_parameter`, and no limit, page size or length is a constant in the code.
- BR6 is executed on `document.created_at`, the stored date, with the range predicate on the `(case_id, document_type, created_at)` index that RWB-P5-E1024-APP created.
- DP07 keeps the type and other lists in reference data; DP15 puts the three search indexes in one step of the service's sequence; DP19 puts the page behind the composite route, so the screen never calls `rwb-case` or `rwb-access` itself.

### 9. State transitions

None. This story does not change a case status and writes no document record. In the target it performs one append to the local decision-record chain:

| From | Event | To |
|---|---|---|
| (no entry) | a search runs and the append is acknowledged | one access record on the chain, replicated to `rwb.decision-record.v1` |
| (no entry) | the append is not acknowledged | no record; 503 with MSG-P5-019 and no row |
| (no entry) | the search is refused before the query (X1 to X4, X8) | no record; the refusal is a validation answer |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Searches by type, date, field and free text in their scope |
| RW-LEGAL, legal counsel; RW-AUDIT, internal audit | Search across all cases (scope ALL); free text allowed under the assumed masking rule |
| RW-COMPLY, compliance and PDPA officer | Searches by type, date and non-personal fields; reads the access log |
| Other roles with Documents R | Search by type, date and non-personal fields in their scope |
| RW-CAPACITY and other roles without Documents R | No search |
| SY-DOCUMENT, the service identity | Runs the query and appends the access record; it searches no case outside the set the case-list read returns |

The authorisation decision is taken by `rwb-access` (roles, scope, masking and DoA as data) and consumed as the authorise answer of DP11; the command-level guard of the service template checks the Documents right R before the criteria are read, and a scope answer that omits a case is the only thing that keeps the case out of the result. The recovery access guard is not built here: the story inherits the guard library the service template carries. The database login is one per service (DP02) and its name is Not specified in the source documents (GAP-2334; ASM-3882).

### 11. Data

| BR Field ID | Table in `rwb_document` | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | `rwb-case` case-list read, through the contract | id | Read |
| DF-CAS-002 | `rwb-case` case-list read, through the contract | case_no | Read |
| DF-DOC-001 | `document` | id | Read |
| DF-DOC-002 | `document` | case_id | Read |
| DF-DOC-004 | `document` | document_type | Read |
| DF-DOC-005 | `document` | source | Read |
| Standard column | `document` | created_at, as the stored date | Read |
| Standard column | `document` | is_active | Read |
| DF-DOC-013 | `document_field` | document_id | Read |
| DF-DOC-014 | `document_field` | field_name | Read |
| DF-DOC-015 | `document_field` | field_value | Read, masked by role |
| DF-DOC-016 | `document_field` | confidence | Read |
| DF-DOC-087 | `document_text` | document_id | Read |
| DF-DOC-089 | `document_text` | text_content | Read |
| DF-REF-224 | `document_type` | field_definitions | Read |
| DF-REF-229 | `document_type` | table_version | Read |
| DF-REF-245 | `document_hub_parameter` | param_code | Read |
| DF-REF-246 | `document_hub_parameter` | param_value | Read |
| (decision record) | decision-record library table in `rwb_document` | record code, inputsRef, finalCall, decidedAt, prev_hash, entry_hash | Write |

Field IDs are those in the Logical Data Model and Data Dictionary and the TSD P5 T3.1 table. No `rwb_case` row is copied, no ACE view is read and no foreign schema is queried (DP01): DF-CAS-001 and DF-CAS-002 arrive inside the case-list answer. Personal data never enters the record payload, the log or the event; the free text term is a SHA-256 hash and a snippet in a response is masked for every identifier but the matched term.

### 12. Contract

#### 12.1 REST operations provided

| Operation | Path | Owner | Notes |
|---|---|---|---|
| GET | `/api/recovery/document/v1/documents` | P5 | The cross-case search of TSD P5 API-P5-009. Query: `type` (doc type code), `dateFrom`, `dateTo` (date), `field`, `op` (eq, gt, lt, between), `value`, `value2`, `q` (free text, 3 to 100 characters), `page`, `size` (default 50, maximum 50). Response 200 DocumentSearchPage: items [documentId, caseId, caseNo, documentType, storedAt, source, matchedField, matchedValue, snippet], page, size, total, capped. Errors 401; 403 no Documents R (MSG-P4-002); 422 no criterion (MSG-GEN-001), date order (MSG-GEN-003), text length (MSG-GEN-002), personal field or free text not allowed (MSG-P5-020); 503 record not acknowledged (MSG-P5-019) or a contract downstream unavailable (MSG-GEN-006). Authorisation: Documents, right R, scope applied. No `Idempotency-Key`: each call writes its own access record |

The parameter names above are the legacy Request row of RWB-E1-033 section 12; the page bounds beyond `size` maximum 50 and the behaviour of `page` beyond the cap are Not specified in the source documents (GAP-2334; ASM-3882). The operation is carried into the service's contract document; this story builds it.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Story | Note |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | RWB-P3-E1018-CON | The case IDs in the caller's scope with their case numbers (legacy `caseIdsInScope` and `caseNumbers`); one hop, 2 s timeout, breaker per downstream (DP11). Consumed and faked although it is in no C row of this Work Package (GAP-2335; ASM-3884) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | RWB-P4-E1037-CON | The masking decision for a role and a field class (legacy `mayReadUnmasked`); one hop, 2 s timeout, breaker (DP11). Consumed and faked although it is in no C row of this Work Package (GAP-2335; ASM-3885) |

The scope filter parameter names of the case-list read are Not specified in the source documents (GAP-2334; ASM-3884). The four parameters and the LOV lists are not REST operations of this story: they are read through the parameters and reference-data client libraries of DP06 and DP07, which wrap RWB-P3-E1042-CON and RWB-P3-E1043-CON. The document type table is a P5 table read locally.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| access record of a search | `rwb.decision-record.v1` | PLT library, consumed by P7 | the caller reference (a search spans cases) | record code, role codes, criteria with the free text term as its SHA-256 hash, result count, case IDs returned, decidedAt |

CloudEvents 1.0 envelope, binary mode; no personal data in the payload. The record is appended in the request path and published by the DP03 library, so it exists exactly when a search is answered; a failed append answers 503 and releases no row.

#### 12.4 Events consumed

None. This story consumes no Kafka event. `DocumentStored` (EV-16) and the intake events (EV-17) are consumed by other paths of this service and by `rwb-case`; the search reads committed rows only, in its own schema.

#### 12.5 Workflows and activities

None. A search is a synchronous read and starts no workflow and no activity. `DocumentIntakeWorkflow` on queue `rwb-document` is RWB-P5-E1049-APP's and is untouched here; `document_text` reaches the search through that workflow's output, which is why this story depends on it.

#### 12.6 Schedules

None. No Schedule is owned or started by this story; the indexes are created by a migration, not by a job.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document` | P5 | Read only: active rows with type, source, stored date and case |
| `document_field` | P5 | Read only: the field condition and the matched value |
| `document_text` | P5 | Read only: the free text and the snippet |
| `document_type` | P5 | Read only: the field definitions and the version in force |
| `document_hub_parameter` | P5 | Read only: the four `SEARCH_*` rows behind the parameters contract |
| decision-record library table | PLT library, created in `rwb_document` | The access record appended per search |

No table of another service is read (DP01) and no ACE view is read by this service. No table is created by this story, only indexes (section 13).

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| rwb-case case-list fake | RWB-P3-E1018-CON | The scope set for AC1, AC2, AC7, AC8 and AC10, the empty set, the 2 s timeout and the open breaker (X9) |
| rwb-access authorise fake | RWB-P4-E1037-CON | The masking answer of AC3 and AC4, the refusal, the timeout and the open breaker (X10) |
| reference-data fake | RWB-P3-E1043-CON (through RWB-PLT-E1043-CON) | LOV-DOC-TYPE and the lists the criteria use |
| parameters fake | RWB-P3-E1042-CON (through RWB-PLT-E1042-CON) | SEARCH_MAX_RESULTS, SEARCH_PAGE_SIZE, FREE_TEXT_MIN_CHARS, FREE_TEXT_MAX_CHARS |
| decision-record fake | RWB-PLT-E1027-CON | The acknowledged and the unacknowledged append (AC9) and the record content of AC2 and AC3 |
| gateway-bff composite route fake | RWB-PLT-N001-CON | The page states of section 15 and the one-hop call |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 1, consumed 2 | The search; the `rwb-case` case-list read and the `rwb-access` authorise decision |
| Kafka | Published 1 decision record; consumed 0 | `rwb.decision-record.v1`; no business topic of this service is published or consumed |
| Temporal | 0 | No workflow, no Schedule, no activity |
| File | 0 | A snippet and metadata travel in the response body; no file is opened by a search |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `document/search`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DocumentSearchController | Controller | The one operation of 12.1; criteria binding, the Documents right R, RFC 9457 problems with the message ID |
| DocumentSearchService | Service | Validation, masking check, scope, query orchestration, row building, access record and its acknowledgement |
| DocumentSearchRepository | Repository | One query over `document`, `document_field` and `document_text` in `rwb_document`, with paging and the cap |
| SnippetBuilder | Service | 60-character snippet, term highlight and the masking of every other identifier through the authorise answer |
| CaseScopeClient | Client | The case-list read of `rwb-case`: the case IDs in scope and their numbers, on the request, 2 s timeout, breaker |
| AccessDecisionClient | Client | The authorise read of `rwb-access` for a role and a field class, cached per request, 2 s timeout, breaker |
| SearchParameters | Library client | Reads the four `SEARCH_*` values through the parameters contract of `rwb-case`, cached 5 minutes |
| DocumentSearchPage | React component | Criteria form, result table with paging, the capped banner, the empty and error states |

**Database.** One step in the per-service Flyway sequence (DP15), `V1033_1__document_search_indexes.sql`:

- `CREATE EXTENSION IF NOT EXISTS pg_trgm;` and `ix_document_text_trgm` on `document_text` using gin (`text_content` `gin_trgm_ops`).
- `dochub_to_numeric(text)` returning numeric or null, and `ix_document_field_name_num` on `document_field` (`field_name`, `dochub_to_numeric(field_value))`.
- `ix_document_field_name_value` on `document_field` (`field_name`, `field_value`).
- No table and no column is added; the case/type/date index `ix_document_case_type_created` comes from RWB-P5-E1024-APP and is reused. No extension or index is created in another schema.

**Configuration and reference data.**

- SEARCH_MAX_RESULTS = 1000, SEARCH_PAGE_SIZE = 50, FREE_TEXT_MIN_CHARS = 3, FREE_TEXT_MAX_CHARS = 100 in `document_hub_parameter`, assumed (DL11), read through the parameters contract of DP06.
- Masking rules (DL26), assumed as the legacy story states them, held as versioned data of the access service; this service holds no masking rule.
- Document type table version in force with the field definitions of the six types (RWB-P5-E1025-APP); LOV-DOC-TYPE through the reference-data contract of DP07.
- Feature flag `rwb.document.search`. Off: the operation returns 404 with a feature-off problem and the menu item is hidden.

**Build steps**

1. Write the migration and test that Thai free text is found through the trigram index on the legacy 500-document set.
2. Build criteria validation: at least one criterion, date order, text length, field in the type's field list, operator set; unit test AC5, AC6, AC7.
3. Build `AccessDecisionClient` against its fake and the masking check; test AC4 and the timeout path X10.
4. Build `CaseScopeClient` against its fake, the scope ALL path and the empty set; test X9 and the empty-scope state.
5. Build the query with scope, paging, cap and newest-first order; integration test AC1, AC2 and AC8 on the 500-document set with the two fakes.
6. Build `SnippetBuilder`; test AC3 with the synthetic Thai and Latin names.
7. Add the access record with the SHA-256 hash and the acknowledgement wait; test AC9 and the record content of AC2 and AC3.
8. Build DocumentSearchPage on the composite route with the states of section 15; component tests, AC10, and the SIT performance run of AC1.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 moves the four tables the legacy query joined into `rwb_document` and removes the `recovery_case` join: the scope and the case number now arrive on the case-list read, which is DP-11's REST-with-mock shape. DP-03 replaces the write to the ACE common PII access log with the local append and the shared decision-record topic, so the record, the query answer and the 503 of AC9 have one source. DP-06 and DP-07 keep four parameters and the lists out of the code, while `document_hub_parameter` and `document_type` stay P5's own tables. DP-11 covers both legacy in-process calls, each with a fake and a 2 s timeout, and adds the two C rows the Work Package does not list. DP-15 puts the three indexes in one step of the service's own sequence. DP-19 puts the page behind the composite route, so the browser makes one call and the screen chains nothing.

**Done when.** The tests in section 16 pass, AC1 answers within 2 seconds at the 95th percentile over 50 runs in SIT, a Thai free text term is found through the trigram index, and every answered search has exactly one access record on `rwb.decision-record.v1` with no term and no personal data in it.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | No criterion | Enter {field}. |
| MSG-GEN-002 | Free text length outside 3 to 100 | {field} must be between {min} and {max}. |
| MSG-GEN-003 | Date from after date to | {field} cannot be before {other}. |
| MSG-GEN-006 | A contract downstream does not answer or its breaker is open | {system} is not available. Your request is queued and will be retried. |
| MSG-P5-019 | Access record not acknowledged | The search was not run because it could not be recorded. Try again in a few minutes. |
| MSG-P5-020 | Role may not search personal data | Your role cannot search on {field} because it holds personal data. |
| MSG-P5-021 | Results above the limit | More than {count} documents match. Narrow the search to see them all. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

HTTP mapping unchanged from the legacy contract: 422 for MSG-GEN-001, MSG-GEN-002, MSG-GEN-003 and MSG-P5-020; 403 for MSG-P4-002; 503 for MSG-P5-019 and MSG-GEN-006. For MSG-GEN-006 the {system} value is "Case service" for X9 and "Access service" for X10. Every error is an RFC 9457 problem response with `messageId`, `detail` with the placeholders filled and `instance`; MSG-P5-021 is a banner on a 200 answer, not an error. Thai text for each message follows decision DL10.

### 15. Screens and states

The screen ID of "search across cases" is Not specified in the source documents (GAP-2334; ASM-3882); `screens.txt` holds none and the legacy story records the same absence. The page Document search under the Documents menu is published through the gateway-bff composite route of DP19 (RWB-PLT-N001-CON), which asks `rwb-document` one hop for what is on screen.

| State | What the user sees |
|---|---|
| Loading | Skeleton rows while the search runs; the criteria stay enabled |
| Result list | Case number, document type, stored date, source and the matched field or the 60-character snippet with the term highlighted |
| Capped | The first SEARCH_MAX_RESULTS rows with the MSG-P5-021 banner and the count 1000, plus the paging control |
| Empty | "No documents match this search." with the action "Clear the search" (labels.txt) |
| Error | The section 14 message at the top of the form, with the criterion preserved so it can be corrected |
| Refused | 403 with MSG-P4-002 when Documents R is missing; 422 on the criteria when the role may not search a personal field |

A row opens DocumentDetailPanel (RWB-P5-E1024-APP), which is a second one-hop call from the same composite route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-033-11 | Access | Component | Capacity and workforce planner (RW-CAPACITY, no Documents right) searches; refused with MSG-P4-002 |
| TC-E1-033-01 | AC1, BR4 | End to end | 500 synthetic documents, 9 matching appraisal reports |
| TC-E1-033-02 | AC2, BR1, BR3 | End to end | Litigation officer with scope TEAM on a mortgage team; 40 hire purchase documents; the case-list fake scoped to "MTG-BKK-LIT" |
| TC-E1-033-03 | AC3, BR2, BR3 | End to end | 3 documents holding a synthetic Thai guarantor name |
| TC-E1-033-04 | AC4, BR2 | End to end | Case owner with masked party names; the authorise fake refusing PARTY_NAME |
| TC-E1-033-05 | AC5 | End to end | Empty criteria |
| TC-E1-033-06 | AC6 | End to end | Dates in the wrong order |
| TC-E1-033-07 | AC7, BR5 | End to end | Free text of 2 and 3 characters |
| TC-E1-033-08 | AC8, BR5 | End to end | 1,250 synthetic demand letters |
| TC-E1-033-09 | AC9, BR3 | Component | Decision-record stub without acknowledgement; 503 and no row |
| TC-E1-033-10 | AC10 | End to end | Free text with no match |

The legacy level System maps to End to end and Access to Component. The integration list `I` of this slice is empty, so no test case is copied with the `-ITG` suffix here; the wave-1 harness runs the real `rwb-case` and `rwb-access` against TC-E1-033-02 and TC-E1-033-04 when those services are up. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: result limit, page size, free text length, the masking rule set, the LOV lists and the type fields are data rows or parameters.
- No personal data in logs, events, records or tests: the free text term is stored as a SHA-256 hash, snippets mask every identifier but the match, and every test name is synthetic.
- No read of another service's tables (DP01). The scope and case numbers come from the `rwb-case` case-list read and the masking decision from `rwb-access`, each one hop with a 2 s timeout and a breaker; this service reads no ACE view.
- A result is never returned before its access record is acknowledged, and an unacknowledged record answers 503 with no row (REQ-ACA-006).
- The query is built from the type table in force and from bound parameters only; no criterion string is concatenated into SQL, and the field name is checked against `field_definitions` first.
- Scope is fetched per request and never cached across callers; a page is capped at SEARCH_MAX_RESULTS so a wide search cannot drain the service.
- The feature flag `rwb.document.search` removes the capability without a schema rollback; the three indexes stay valid and harmless when it is off.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-001 | Documents found by type, date and extracted fields | Epic 1, 3.5; Program, 5.5 | FEAT-DCM-06 | 13 Manage documents and correspondence | None | TC-E1-033-01, TC-E1-033-03, TC-E1-033-05 to TC-E1-033-08, TC-E1-033-10 |
| REQ-ACA-006 | Every read of the document store written to the access log | Epic 1, 3.4; Program, 5.4 | FEAT-DCM-06 | 13 Manage documents and correspondence | CTL-11 | TC-E1-033-02, TC-E1-033-04, TC-E1-033-09, TC-E1-033-11 |
| REQ-DCM-017 | The hub answers an electronic discovery request with every document for a named population and its version history | Epic 1, 3.5; Program, 5.5 | FEAT-DCM-06 | 13 Manage documents and correspondence | None | None in this slice: the export is Epic 2 and sits in section 19 (ASM-3888) |

| Legacy reference | Where it is kept |
|---|---|
| User story, rationale, authority and the six business rules | Sections 1, 2, 8, 10 |
| Preconditions: type table in force, SEARCH_MAX_RESULTS 1000, SEARCH_PAGE_SIZE 50, FREE_TEXT_MIN_CHARS 3, FREE_TEXT_MAX_CHARS 100, DL26 masking, `rwb.dochub.search` | Sections 3, 8, 13 |
| Legacy flow steps 1 to 9, with `CaseDirectory` and `mayReadUnmasked` | Sections 2, 4, 12.2 |
| Exception paths X1 to X8 and messages MSG-GEN-001, MSG-GEN-002, MSG-GEN-003, MSG-P5-019, MSG-P5-020, MSG-P5-021, MSG-P4-002 | Sections 5, 14 |
| Legacy contract `GET /documents` with its request, response and errors | Section 12.1 |
| Legacy components DocumentHubController, DocumentSearchService, DocumentSearchRepository, SnippetBuilder, DocumentSearchPage | Section 13 |
| Legacy migration `V1_5_033__document_search_indexes.sql` with pg_trgm, `dochub_to_numeric` and the two field indexes | Section 13 |
| Screens: no screen ID in `screens.txt`, states Loading, list, Empty, Error | Section 15 |
| Test cases TC-E1-033-01 to TC-E1-033-11 | Section 16 |

### 19. Out of scope

- Answering a legal or audit document request with an export (FEAT-COM-07, Epic 4) and electronic discovery (Epic 2, REQ-DCM-017).
- Search within one case and the case documents tab (RWB-P5-E1026-APP).
- The store, the index, the versions and the detail panel (RWB-P5-E1024-APP); the type table and its fields (RWB-P5-E1025-APP).
- The OCR pipeline and the intake workflow (RWB-P5-E1049-APP); field extraction and the review queue (RWB-P5-E1053-CON, RWB-P5-E1054-APP).
- The access log query screen and its copy to the decision log (the access service's own read).
- Search on dates read from the document content, beyond field conditions (Epic 2).
- The published contract document of `GET /documents`, its versioning and its fake; the permissions, masking rows and scope data of `rwb-access`; the case-list contract of `rwb-case`.
- The Helm chart, the feature-flag rollout plan, the topic and DLT provisioning, the metrics, the alerts and the runbook of this service.

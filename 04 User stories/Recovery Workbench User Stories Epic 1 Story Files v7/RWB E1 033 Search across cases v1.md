# RWB-E1-033 Search across cases

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-033 |
| Epic | E1, release 30 November 2026 |
| Module | P5 Document hub |
| Feature | FEAT-DCM-06 Search documents across cases |
| Requirement IDs | REQ-DCM-001, REQ-ACA-006 |
| BRD section | Business Requirements Epic 1, sections 3.5 and 3.4; Business Requirements Program, sections 5.5 and 5.4 |
| L3 process | 13 Manage documents and correspondence |
| Decision | None |
| Priority | Should |
| Depends on | RWB-E1-024, RWB-E1-053, RWB-E1-049 |
| Status | Ready for build |

## 1. Story

As a **litigation officer (RW-LITOFF)**, I want **a search across all cases in my scope by document type, date range, extracted field and free text, with every search written to the access log**, so that **I find a document in seconds without opening cases one by one, and every look at personal data can be audited**.

## 2. Business rationale

Legal, audit and recovery questions span many cases: every appraisal above a value, every notice from one court, every document naming a guarantor. Today each case folder is opened by hand (FSD P5 A2.6). This story searches the document index, the extracted fields and the OCR text across the cases the user may see, masks personal data the role may not see, and logs each search. It meets REQ-DCM-001 (documents found by their type, date and extracted fields) and REQ-ACA-006 (every read of the document store written to the access log), under control CTL-09 and CTL-11.

## 3. Preconditions

- RWB-E1-024 is done: documents and extracted fields are in the index.
- RWB-E1-049 is done: OCR text is in document_text.
- RWB-E1-053 is done: extracted fields carry names from the type table and a confidence.
- Masking rules loaded (DL26). Assumed until Compliance provides them: RW-LITOFF, RW-LEGAL and RW-AUDIT see party names in document text unmasked; every other role sees them masked.
- Parameters loaded in document_hub_parameter: SEARCH_MAX_RESULTS = 1000, SEARCH_PAGE_SIZE = 50, FREE_TEXT_MIN_CHARS = 3, FREE_TEXT_MAX_CHARS = 100 (assumed; DL11).
- The ACE common module writes access events to the PII access log and confirms each write.
- The user holds Documents R. Feature flag rwb.dochub.search is on.

## 4. Flow

1. Litigation officer: opens Document search from the Documents menu and enters a type, a stored date range, a field condition (field, operator, value) and or a free text term.
2. Front end: calls GET /documents with the criteria.
3. DocumentSearchService: validates the criteria: at least one criterion, date order, free text length, field in the type's field list.
4. DocumentSearchService: checks with the masking policy that the role may search a personal field or free text; refuses otherwise.
5. DocumentSearchService: gets the case IDs in the user's scope through CaseDirectory.caseIdsInScope (all cases for scope ALL).
6. DocumentSearchRepository: queries active documents in those cases by type and stored date, joined to document_field for the field condition and to document_text for the free text, newest first, up to SEARCH_MAX_RESULTS.
7. DocumentSearchService: builds each row: case number, document type, stored date, source, the matched field or a text snippet of 60 characters with the term highlighted and other personal identifiers masked.
8. DocumentSearchService: writes the access event DOCUMENT_SEARCH (user, role, criteria with the free text term as a SHA-256 hash, result count, case IDs returned) through the PII access log and waits for the confirmation.
9. Front end: shows the first page of 50 rows; the user opens a row in DocumentDetailPanel (RWB-E1-024).

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The role's masking rule hides party names and the user searches free text or a personal field | Refused with 422; nothing searched | MSG-P5-020 | AC4 |
| X2 | No criterion entered | Refused with 422 | MSG-GEN-001 | AC5 |
| X3 | Date from after date to | Refused with 422 | MSG-GEN-003 | AC6 |
| X4 | Free text shorter than 3 or longer than 100 characters | Refused with 422 | MSG-GEN-002 | AC7 |
| X5 | More than SEARCH_MAX_RESULTS documents match | The first 1000 by date are returned with a capped flag | MSG-P5-021 | AC8 |
| X6 | The access log write is not confirmed | Results are not returned; 503 | MSG-P5-019 | AC9 |
| X7 | Nothing matches | Empty state | None | AC10 |
| X8 | A role without Documents R searches | Refused with 403 | MSG-P4-002 | TC-E1-033-11 (Access) |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the index (RWB-E1-024), OCR text (RWB-E1-049) and extracted fields (RWB-E1-053), all earlier in Epic 1 |
| Negotiable | Limits, page size and the masking rules are data; the criteria set can grow |
| Valuable | A cross-case question takes one search instead of opening each case |
| Estimable | One endpoint, one service, one query with two indexes, one page |
| Small | Fits within two weeks with its tests |
| Testable | Each criterion below is one test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Search across cases

  Background:
    Given 500 synthetic documents indexed across 120 cases
    Given 60 of them are "APPRAISAL_REPORT", 14 with appraised_value above 5,000,000, 9 of those stored in October 2026
    Given user "TEST-LIT-01" holds RW-LITOFF with scope ALL

  Scenario: AC1 Search by field
    Given "TEST-LIT-01" is on the Document search page
    When "TEST-LIT-01" searches type "APPRAISAL_REPORT", field appraised_value greater than 5,000,000, stored from 1 October 2026 to 31 October 2026
    Then exactly the 9 matching documents list with case number, type, stored date and the field value
    Then the response arrives within 2 seconds

  Scenario: AC2 Role limit
    Given user "TEST-LIT-02" holds RW-LITOFF with scope TEAM on team "MTG-BKK-LIT", whose cases are all product group "MORTGAGE"
    Given 40 of the 500 documents are on "HIRE_PURCHASE" cases
    When "TEST-LIT-02" searches type "COURT_NOTICE" with no date
    Then no document on a "HIRE_PURCHASE" case appears
    Then the system writes one access event "DOCUMENT_SEARCH" with the user, the criteria, the result count and the case IDs returned

  Scenario: AC3 Free text
    Given the OCR text of 3 documents holds the synthetic guarantor name "SYN GUARANTOR ONE"
    When "TEST-LIT-01" searches the free text "SYN GUARANTOR ONE"
    Then the 3 documents list with a snippet in which the name is highlighted
    Then the access event holds the SHA-256 hash of the term and not the term

  Scenario: AC4 Free text refused for a masked role
    Given user "TEST-CO-01" holds RW-CASEOWN, whose masking rule hides party names
    When "TEST-CO-01" searches the free text "SYN GUARANTOR"
    Then the system refuses the request with 422 and MSG-P5-020 naming "document text"
    Then no query runs

  Scenario: AC5 No criterion
    Given "TEST-LIT-01" is on the Document search page
    When "TEST-LIT-01" searches with every criterion empty
    Then the system refuses the request with 422 and MSG-GEN-001 naming "a search criterion"

  Scenario: AC6 Date range in the wrong order
    Given "TEST-LIT-01" is on the Document search page
    When "TEST-LIT-01" searches stored from 31 October 2026 to 1 October 2026
    Then the system refuses the request with 422 and MSG-GEN-003

  Scenario: AC7 Free text length boundary
    Given "TEST-LIT-01" is on the Document search page
    When "TEST-LIT-01" searches the free text "ab" and then the free text "abc"
    Then the system refuses "ab" with 422 and MSG-GEN-002 showing 3 and 100
    Then "abc" runs

  Scenario: AC8 More results than the limit
    Given 1,250 documents of type "DEMAND_LETTER" in the user's scope
    When "TEST-LIT-01" searches type "DEMAND_LETTER"
    Then the first page of 50 rows returns with total 1000 and capped true
    Then MSG-P5-021 shows with the count 1000

  Scenario: AC9 Access log not confirmed
    Given the PII access log does not confirm writes
    When "TEST-LIT-01" searches type "COURT_NOTICE"
    Then the request returns 503 with MSG-P5-019
    Then the system returns no result row

  Scenario: AC10 Nothing matches
    Given no document holds the free text "NO SUCH TEXT"
    When "TEST-LIT-01" searches it
    Then the page shows the empty state "No documents match this search." and the action "Clear the search"
    Then the access event records a result count of 0
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Results hold only active documents on cases in the user's scope | CTL-09; FEAT-DCM-20 |
| BR2 | Personal fields and free text are searchable only by roles that see them unmasked; snippets mask other personal identifiers | CTL-11; DL26; masking rules reference table |
| BR3 | Every search is written to the access log before results are returned; a free text term is logged as a hash | REQ-ACA-006; CTL-11 |
| BR4 | Field conditions use the field names and data types of the type table in force | RWB-E1-025; DL19 |
| BR5 | Result limit, page size and free text length are parameters | Document hub parameter table (New); DL11 |
| BR6 | The date criterion is the stored date of the document in Epic 1 | FSD P5 A2.6 |

## 9. State transitions

None. This story does not change a case status. It writes no record of its own; the access event goes to the PII access log of the ACE common module.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Searches by type, date, field and free text in their scope |
| RW-LEGAL, legal counsel; RW-AUDIT, internal audit | Search across all cases (scope ALL); free text allowed under the assumed masking rule |
| RW-COMPLY, compliance and PDPA officer | Searches by type, date and non-personal fields; reads the access log |
| Other roles with Documents R | Search by type, date and non-personal fields in their scope |
| RW-CAPACITY and other roles without Documents R | No search |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read, through CaseDirectory |
| DF-CAS-002 | recovery_case | case_no | Read, through CaseDirectory |
| DF-DOC-001 | document | id | Read |
| DF-DOC-002 | document | case_id | Read |
| DF-DOC-004 | document | document_type | Read |
| DF-DOC-005 | document | source | Read |
| Standard column | document | created_at | Read, as the stored date |
| DF-DOC-013 | document_field | document_id | Read |
| DF-DOC-014 | document_field | field_name | Read |
| DF-DOC-015 | document_field | field_value | Read, masked by role |
| DF-DOC-016 | document_field | confidence | Read |
| DF-DOC-089 | document_text | text_content | Read |
| DF-REF-224 | document_type | field_definitions | Read |
| DF-REF-246 | document_hub_parameter | param_value | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /documents** (new, see additions)

| Item | Value |
|---|---|
| Request | Query: type (doc_type_code), dateFrom, dateTo (date), field (field name), op (eq, gt, lt, between), value, value2, q (free text, 3 to 100 characters), page, size (default 50, maximum 50) |
| Response | 200 DocumentSearchPage: items [documentId, caseId, caseNo, documentType, storedAt, source, matchedField, matchedValue, snippet], page, size, total, capped |
| Errors | 401; 403 no Documents R (MSG-P4-002); 422 no criterion (MSG-GEN-001), date order (MSG-GEN-003), text length (MSG-GEN-002), personal field or free text not allowed (MSG-P5-020); 503 access log not confirmed (MSG-P5-019) or store unavailable (MSG-GEN-006) |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable; each call writes its own access event |

**Published interfaces called**

```java
// P3
Set<UUID> caseIdsInScope(ScopeFilter scope);        // empty filter for scope ALL
Map<UUID, String> caseNumbers(Collection<UUID> caseIds);
// P4
boolean mayReadUnmasked(String roleCode, String fieldClass);   // fieldClass PARTY_NAME, ACCOUNT_NO, ID_NO
```

## 13. Solution plan

**Package.** Folder `recovery/dochub/search`, Java package `recovery.dochub.search`; front end folder `recovery/documents`.

**Components.**

| Component | Type | Responsibility |
|---|---|---|
| DocumentHubController | Controller | Adds GET /documents/search |
| DocumentSearchService | Service | Validation, masking check, scope, query, row building, access event |
| DocumentSearchRepository | Repository | One SQL query over document, document_field and document_text, with paging and the cap |
| SnippetBuilder | Service | 60-character snippet, highlight, masking of other identifiers through the ACE PII service |
| DocumentSearchPage | React component | Criteria form, result table with paging, empty and error states |

**Database.**
- Reads document, document_field and document_text. No new table.
- Flyway migration `V1_5_033__document_search_indexes.sql`: CREATE EXTENSION IF NOT EXISTS pg_trgm; GIN index ix_document_text_trgm on document_text using gin (text_content gin_trgm_ops); function dochub_to_numeric(text) returning numeric or null; index ix_document_field_name_num on document_field (field_name, dochub_to_numeric(field_value)); index ix_document_field_name_value on document_field (field_name, field_value).

**Configuration and reference data.**
- SEARCH_MAX_RESULTS, SEARCH_PAGE_SIZE, FREE_TEXT_MIN_CHARS, FREE_TEXT_MAX_CHARS in document_hub_parameter, loaded by the reference data administrator.
- Masking rules (DL26), loaded by the reference data administrator for Compliance.

**Build steps.**
1. Write the migration; test that Thai free text is found with ILIKE through the trigram index.
2. Build criteria validation; unit test AC5, AC6 and AC7.
3. Build the masking check; test AC4.
4. Build the query with scope, paging and the cap; integration test AC1, AC2 and AC8 on the 500-document set.
5. Build SnippetBuilder; test AC3.
6. Add the access event with the hash and the confirmation wait; test AC9 and the event content in AC2.
7. Build DocumentSearchPage with the states; component tests and AC10; performance test of AC1 in SIT.

**Feature flag.** `rwb.dochub.search`. Off: GET /documents/search returns 404 and the menu item is hidden.

**Done when.** The tests in section 16 pass and AC1 answers within 2 seconds at the 95th percentile over 50 runs in SIT.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | No criterion | Enter {field}. |
| MSG-GEN-002 | Free text length outside 3 to 100 | {field} must be between {min} and {max}. |
| MSG-GEN-003 | Date from after date to | {field} cannot be before {other}. |
| MSG-P5-019 | Access log write not confirmed | The search was not run because it could not be recorded. Try again in a few minutes. |
| MSG-P5-020 | Role may not search personal data | Your role cannot search on {field} because it holds personal data. |
| MSG-P5-021 | Results above the limit | More than {count} documents match. Narrow the search to see them all. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

## 15. Screens and states

screens.txt holds no screen ID for search across cases. This story builds the page Document search under the Documents menu, with the common states: Loading (skeleton rows), the result list, Empty ("No documents match this search." with "Clear the search") and Error (message from section 14 at the top). A row opens DocumentDetailPanel (RWB-E1-024). The missing screen ID is recorded in the additions file.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-033-01 | AC1, BR4 | System | 500 synthetic documents, 9 matching appraisal reports |
| TC-E1-033-02 | AC2, BR1, BR3 | System | Litigation officer with scope TEAM on a mortgage team; 40 hire purchase documents |
| TC-E1-033-03 | AC3, BR2, BR3 | System | 3 documents holding a synthetic Thai guarantor name |
| TC-E1-033-04 | AC4, BR2 | System | Case owner with masked party names |
| TC-E1-033-05 | AC5 | System | Empty criteria |
| TC-E1-033-06 | AC6 | System | Dates in the wrong order |
| TC-E1-033-07 | AC7, BR5 | System | Free text of 2 and 3 characters |
| TC-E1-033-08 | AC8, BR5 | System | 1,250 synthetic demand letters |
| TC-E1-033-09 | AC9, BR3 | System | PII access log stub without confirmation |
| TC-E1-033-10 | AC10 | System | Free text with no match |
| TC-E1-033-11 | Access | Access | Capacity and workforce planner (RW-CAPACITY, no Documents right) searches; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: limits, page size, text length and masking are data.
- No personal data in logs, tests or prompts: the free text term is logged as a hash; names in tests are synthetic.
- No read of another module's tables: scope and case numbers come through CaseDirectory, masking through the P4 interface.
- A result is never returned before its access event is confirmed.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-001 | Documents found by type, date and extracted fields | Business Requirements Epic 1, section 3.5 | FEAT-DCM-06 | 13 Manage documents and correspondence | None | TC-E1-033-01, TC-E1-033-03, TC-E1-033-05 to TC-E1-033-08, TC-E1-033-10 |
| REQ-ACA-006 | Every read of the document store written to the access log | Business Requirements Epic 1, section 3.4 | FEAT-DCM-06 | 13 Manage documents and correspondence | None | TC-E1-033-02, TC-E1-033-04, TC-E1-033-09, TC-E1-033-11 |

## 19. Out of scope

- Answering a legal or audit document request with an export (FEAT-COM-07, Epic 4) and electronic discovery (Epic 2, REQ-DCM-017).
- Search within one case (RWB-E1-026).
- The access log query screen and its copy to the decision log (RWB-E1-039).
- Search on dates read from the document content, beyond field conditions (Epic 2).

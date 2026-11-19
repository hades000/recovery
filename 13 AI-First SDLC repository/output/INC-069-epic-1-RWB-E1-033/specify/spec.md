# Technical Specification — RWB-E1-033 Search across cases

| Field | Value |
|---|---|
| Story | RWB-E1-033 — Search across cases |
| Epic / module | E1 / P5 Document hub |
| RUN_ID | `INC-069-epic-1-RWB-E1-033` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-DCM-001, REQ-ACA-006); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 033 Search across cases v1.md`; FSD P5 A2.6; TSD P5 T3.1 |
| Upstream IDs | REQ-DCM-001, REQ-ACA-006; FEAT-DCM-06; US-RWB-E1-033; DL11, DL26; CTL-09, CTL-11 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `YES` — new Document search page under the Documents menu: criteria form, result table, paging, empty and error states. No SCR ID exists in the inventory; see CLAR-008. |
| Logic In Scope | `YES` — criteria validation, masking check, scope, query, result building, snippet and access event. |
| API In Scope | `YES` — new `GET /api/recovery/v1/documents` search endpoint. |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | `DocumentHubController` (new search action); `DocumentSearchRepository`; SCR-30 DocumentDetailPanel (row opens it). |
| New Nodes Required | `YES` — `DocumentSearchService`, `DocumentSearchRepository`, `SnippetBuilder`, `DocumentSearchPage`, `DocumentSearchHit`. |
| Inherited Existing Behavior | Document index and fields (RWB-E1-024); OCR text (RWB-E1-049); extracted fields (RWB-E1-053); case scope and case numbers through `CaseDirectory` (P3); masking through the P4 interface; PII access log (ACE common). |
| Frontend Changes Required | `YES` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Results hold only active documents on cases in the user's scope. | SPEC-RWB-E1-033-003 | DIRECT | `CaseDirectory.caseIdsInScope`; `document.is_active`; no cross-scope row. | COVERED |
| BR2 | Personal fields and free text are searchable only by roles that see them unmasked; snippets mask other personal identifiers. | SPEC-RWB-E1-033-002, SPEC-RWB-E1-033-005 | DIRECT | `mayReadUnmasked`; snippet masking through the ACE PII service. | COVERED |
| BR3 | Every search is written to the access log before results are returned; a free text term is logged as a hash. | SPEC-RWB-E1-033-006 | DIRECT | `DOCUMENT_SEARCH` event; wait for confirmation; SHA-256 of the term. | COVERED |
| BR4 | Field conditions use the field names and data types of the type table in force. | SPEC-RWB-E1-033-001, SPEC-RWB-E1-033-013 | DIRECT | Field must be in `field_definitions`; operators respect the data type. | COVERED |
| BR5 | Result limit, page size and free text length are parameters. | SPEC-RWB-E1-033-001, SPEC-RWB-E1-033-004, SPEC-RWB-E1-033-008 | DIRECT | `SEARCH_MAX_RESULTS`, `SEARCH_PAGE_SIZE`, `FREE_TEXT_MIN_CHARS`, `FREE_TEXT_MAX_CHARS`. | COVERED |
| BR6 | The date criterion is the stored date of the document in Epic 1. | SPEC-RWB-E1-033-012 | DIRECT | `document.created_at`. | COVERED |
| AC1 | A type, field and date search returns exactly the 9 matching appraisal reports within 2 seconds. | SPEC-RWB-E1-033-004, SPEC-RWB-E1-033-005, SPEC-RWB-E1-033-013 | DIRECT | One query over document and document_field; 95th percentile target. | COVERED |
| AC2 | A team-scoped litigation officer sees no hire-purchase document; one access event records user, criteria, count and case IDs. | SPEC-RWB-E1-033-003, SPEC-RWB-E1-033-006 | DIRECT | Scope filter; event before results. | COVERED |
| AC3 | Three documents with a synthetic guarantor name are found; the snippet highlights the name; the event holds the SHA-256 hash. | SPEC-RWB-E1-033-005, SPEC-RWB-E1-033-006, SPEC-RWB-E1-033-009 | DIRECT | Trigram search; snippet builder. | COVERED |
| AC4 | A case owner whose masking rule hides party names is refused free text with 422 MSG-P5-020; no query runs. | SPEC-RWB-E1-033-002 | DIRECT | Masking check before scope and query. | COVERED |
| AC5 | A search with every criterion empty is refused with 422 MSG-GEN-001. | SPEC-RWB-E1-033-001 | DIRECT | At least one criterion. | COVERED |
| AC6 | A date range in the wrong order is refused with 422 MSG-GEN-003. | SPEC-RWB-E1-033-001 | DIRECT | `dateFrom <= dateTo`. | COVERED |
| AC7 | Free text of 2 characters is refused with 422 MSG-GEN-002 showing 3 and 100; 3 characters runs. | SPEC-RWB-E1-033-001 | DIRECT | Length boundary. | COVERED |
| AC8 | 1,250 demand letters return the first page of 50 with total 1000 and capped true, and MSG-P5-021 shows 1000. | SPEC-RWB-E1-033-004, SPEC-RWB-E1-033-008 | DIRECT | Cap and page size; capped flag. | COVERED |
| AC9 | An unconfirmed access log returns 503 MSG-P5-019 and no result row. | SPEC-RWB-E1-033-006 | DIRECT | No results before confirmation. | COVERED |
| AC10 | No match shows the empty state and records a result count of 0. | SPEC-RWB-E1-033-005, SPEC-RWB-E1-033-006, SPEC-RWB-E1-033-007 | DIRECT | Empty state; event with 0. | COVERED |
| X1 | A masked role searches free text or a personal field. | SPEC-RWB-E1-033-002 | DIRECT | 422 MSG-P5-020; no query. | COVERED |
| X2, X3, X4 | No criterion, dates in the wrong order, or free text outside 3 to 100 characters. | SPEC-RWB-E1-033-001 | DIRECT | 422 with MSG-GEN-001/003/002. | COVERED |
| X5 | More than `SEARCH_MAX_RESULTS` documents match. | SPEC-RWB-E1-033-004, SPEC-RWB-E1-033-008 | DIRECT | First 1000 by date; capped true; MSG-P5-021. | COVERED |
| X6 | The access log write is not confirmed. | SPEC-RWB-E1-033-006 | DIRECT | 503 MSG-P5-019; no rows. | COVERED |
| X7 | Nothing matches. | SPEC-RWB-E1-033-007 | DIRECT | Empty state. | COVERED |
| X8 | A role without Documents R searches. | SPEC-RWB-E1-033-011 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **litigation officer**, I want **a search across all cases in my scope by document type, date range, extracted field and free text, with every search written to the access log**, so that **I find a document in seconds without opening cases one by one, and every look at personal data can be audited**. The story adds a new Document search page and one read endpoint. It is read-only: no case, document or intake status changes.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | The user opens Document search from the Documents menu and submits the criteria form. |
| Preconditions | RWB-E1-024, RWB-E1-049 and RWB-E1-053 done; masking rules loaded (DL26); `SEARCH_MAX_RESULTS`, `SEARCH_PAGE_SIZE`, `FREE_TEXT_MIN_CHARS` and `FREE_TEXT_MAX_CHARS` loaded; the ACE common module confirms PII access log writes; the user holds Documents R; flag `rwb.dochub.search` on. |
| Input | `type`, `dateFrom`, `dateTo`, `field`, `op`, `value`, `value2`, `q`, `page`, `size`. |
| Output | `DocumentSearchPage` with rows, page, size, total and capped; one `DOCUMENT_SEARCH` access event. |
| Feature flag | `rwb.dochub.search`. Off: `GET /documents` returns 404 and the menu item is hidden. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| Request | `type` | Type list in force | User selects | Optional; must be a `doc_type_code` in force. |
| Request | `dateFrom`, `dateTo` | Date pickers | User selects | Optional; `dateFrom <= dateTo`; stored date. |
| Request | `field`, `op`, `value`, `value2` | Field list of the type | User selects and enters | `op` is eq, gt, lt or between; field must be in `field_definitions`. |
| Request | `q` | Free text box | User enters | 3 to 100 characters; refused for a masked role. |
| Request | `page`, `size` | First page, 50 | User pages | Size default and maximum 50. |
| Response | `documentId`, `caseId`, `caseNo` | Document and case | Read-only | Case number from `CaseDirectory`. |
| Response | `documentType`, `storedAt`, `source` | Document | Read-only | Stored date is `created_at`. |
| Response | `matchedField`, `matchedValue` | Field condition | Read-only | Value masked by role. |
| Response | `snippet` | OCR text | Read-only | 60 characters; term highlighted; other identifiers masked. |
| Response | `total`, `capped` | Query result | Read-only | `total` stops at `SEARCH_MAX_RESULTS`; `capped` true when more match. |
| Access event | `DOCUMENT_SEARCH` | Search | System writes | User, role, criteria, result count and case IDs; free text as SHA-256. |

## Status-transition matrix

No domain status changes. The search is read-only and writes only the access event.

| Request state | Event | Condition | Result state | Side effects |
|---|---|---|---|---|
| New | Submit | Criteria valid and masking allowed | Results or empty | One access event before the rows return. |
| New | Submit | More than `SEARCH_MAX_RESULTS` match | Capped results | `capped true`; MSG-P5-021. |
| New | Submit | Invalid criteria or masked role | Refused | 422; no query; no event. |
| New | Submit | Access log not confirmed | Refused | 503 MSG-P5-019; no rows. |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Masked role searches free text or a personal field | 422; nothing searched | MSG-P5-020 |
| X2 | No criterion entered | 422 | MSG-GEN-001 |
| X3 | `dateFrom` after `dateTo` | 422 | MSG-GEN-003 |
| X4 | Free text shorter than 3 or longer than 100 | 422 | MSG-GEN-002 |
| X5 | More than `SEARCH_MAX_RESULTS` match | First 1000 by date; capped flag | MSG-P5-021 |
| X6 | Access log write not confirmed | No results; 503 | MSG-P5-019 |
| X7 | Nothing matches | Empty state; result count 0 | None |
| X8 | Role without Documents R | 403; nothing searched | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| New endpoint | `GET /api/recovery/v1/documents` (API-P5-009), query `type`, `dateFrom`, `dateTo`, `field`, `op`, `value`, `value2`, `q`, `page`, `size`. |
| Contract delta | `DocumentSearchPage` with `items`, `page`, `size`, `total`, `capped`; each hit has `documentId`, `caseId`, `caseNo`, `documentType`, `storedAt`, `source`, `matchedField`, `matchedValue`, `snippet`. |
| Backward compatibility | New endpoint; no existing contract changes. |
| Authorization | Documents R with scope; 403 MSG-P4-002. |
| Error behaviour | 401; 403 MSG-P4-002; 422 MSG-GEN-001/002/003 or MSG-P5-020; 503 MSG-P5-019 or MSG-GEN-006. |
| Versioning | First release; no version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DCM-001, REQ-ACA-006; SPEC-RWB-E1-033-001, -005, -007, -008 | New Document search page with criteria form, result table, paging, empty and error states. | Component tests for each state, paging, cap message and row open. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DCM-001, REQ-ACA-006; SPEC-RWB-E1-033-001..013 | New service, repository, snippet builder and access event. | Unit tests for validation, masking, scope, each operator, free text, cap, empty, access log failure and Thai text. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `DocumentHubController` | Controller | Adds `GET /documents`. |
| `DocumentSearchService` | Service | Validation, masking check, scope, query, row building and access event. |
| `DocumentSearchRepository` | Repository | One query over `document`, `document_field` and `document_text`, with paging and the cap. |
| `SnippetBuilder` | Service | 60-character snippet, highlight and masking of other identifiers. |
| `DocumentSearchPage` | React component | Criteria form, result table, paging, empty and error states. |

### Package and boundaries

`recovery/dochub/search`, Java package `recovery.dochub.search`; front end `recovery/documents`. Scope and case numbers come through `CaseDirectory`; masking through the P4 interface; the access event through the ACE common PII access log. No module reads another module's tables.

### Data and migration

- Reads: `document` (`id`, `case_id`, `document_type`, `source`, `created_at`, `is_active`), `document_field` (`document_id`, `field_name`, `field_value`, `confidence`), `document_text` (`text_content`), `document_type` (`field_definitions`), `document_hub_parameter`.
- No new table. Migration `V1_5_033__document_search_indexes.sql` creates `pg_trgm`, the GIN index `ix_document_text_trgm` on `document_text.text_content`, the function `dochub_to_numeric(text)`, and indexes `ix_document_field_name_num` and `ix_document_field_name_value`.
- No business value is hard-coded: limits, page size, free text length and masking are data.

### Search rules

1. Require at least one criterion; check the date order; check the free text length; check the field is in the type's field list.
2. Check with the masking policy that the role may search a personal field or free text; refuse otherwise before any query.
3. Get the case IDs in the user's scope through `CaseDirectory.caseIdsInScope`; scope ALL uses an empty filter.
4. Query active documents in those cases by type and stored date, joined to `document_field` for the field condition and `document_text` for free text, newest first, up to `SEARCH_MAX_RESULTS`.
5. Build each row with case number, type, stored date, source, the matched field value or a 60-character snippet with the term highlighted and other identifiers masked.
6. Write `DOCUMENT_SEARCH` with the user, role, criteria, free text hash, result count and case IDs; wait for confirmation before returning rows.

### Transaction, events and access log

- The search is read-only; no transaction spans the result build and the access log.
- The access event is written before the response; an unconfirmed write returns 503 and no rows.
- The free text term is never stored in clear in the access event; only its SHA-256 hash.
- No outbox event and no decision log entry: the search does not change a case or a document.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-LITOFF | Documents R | Team or all |
| RW-LEGAL, RW-AUDIT | Documents R | All |
| RW-COMPLY | Documents R | All; non-personal fields |
| Other roles with Documents R | Documents R | Own or team |
| Roles without Documents R | None | No search |

The assumed masking rule under DL26: RW-LITOFF, RW-LEGAL and RW-AUDIT see party names in document text unmasked; every other role sees them masked. The rule is data, not code.

### Observability, performance and operations

- Metrics: searches per role, result count, capped rate, refusal rate, p95 duration, access log failures.
- Alerts: access log failure rate; p95 above 2 seconds.
- Performance: AC1 within 2 seconds at the 95th percentile over 50 runs in SIT; trigram index for Thai and English free text; field indexes for numeric and text conditions.
- Run book: not a job; the operational note is the access log dependency.

### Feature flag and rollback

`rwb.dochub.search`. Off: `GET /documents` returns 404 and the menu item is hidden. Rollback: turn the flag off; the migration adds indexes only and is forward-only.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-033-01 | AC1, BR4 | System | 500 synthetic documents; 9 matching appraisal reports | 9 rows with case number, type, date and value; p95 within 2 seconds. |
| TC-E1-033-02 | AC2, BR1, BR3 | System | Litigation officer, mortgage team; 40 hire-purchase documents | No hire-purchase row; one DOCUMENT_SEARCH event with criteria, count and case IDs. |
| TC-E1-033-03 | AC3, BR2, BR3 | System | 3 documents with a synthetic Thai guarantor name | 3 rows; snippet highlights the name; event holds the SHA-256 hash. |
| TC-E1-033-04 | AC4, BR2 | System | Case owner with masked party names | 422 MSG-P5-020; no query. |
| TC-E1-033-05 | AC5 | System | Empty criteria | 422 MSG-GEN-001. |
| TC-E1-033-06 | AC6 | System | Dates in the wrong order | 422 MSG-GEN-003. |
| TC-E1-033-07 | AC7, BR5 | System | Free text of 2 and 3 characters | 2 refused with MSG-GEN-002; 3 runs. |
| TC-E1-033-08 | AC8, BR5 | System | 1,250 synthetic demand letters | Page of 50; total 1000; capped true; MSG-P5-021. |
| TC-E1-033-09 | AC9, BR3 | System | PII access log stub without confirmation | 503 MSG-P5-019; no rows. |
| TC-E1-033-10 | AC10 | System | Free text with no match | Empty state; event count 0. |
| TC-E1-033-11 | X8 | Security | RW-CAPACITY without Documents R | 403 MSG-P4-002. |

## Guardrails

- No business value in code: limits, page size, text length and masking are data.
- No personal data in logs, tests or prompts: the free text term is logged as a hash; names in tests are synthetic.
- No read of another module's tables: scope and case numbers come through `CaseDirectory`; masking through the P4 interface.
- A result is never returned before its access event is confirmed.

## Out of scope

- Answering a legal or audit document request with an export (FEAT-COM-07, Epic 4) and electronic discovery (Epic 2, REQ-DCM-017).
- Search within one case (RWB-E1-026).
- The access log query screen and its copy to the decision log (RWB-E1-039).
- Search on dates read from document content, beyond field conditions (Epic 2).

## Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-DCM-001 | Documents found by type, date and extracted fields | FEAT-DCM-06 | 13 Manage documents and correspondence | None | TC-E1-033-01, 03, 05..08, 10 |
| REQ-ACA-006 | Every read of the document store written to the access log | FEAT-DCM-06 | 13 Manage documents and correspondence | None | TC-E1-033-02, 04, 09, 11 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | Flow; §12; SPEC-004 | Flow and section 12 name `GET /documents`; section 13 and the feature flag name `GET /documents/search`. | Determines the endpoint the page calls. | Use API-P5-009 `GET /api/recovery/v1/documents`; the `/documents/search` wording is a known defect. | RESOLVED | SPEC-RWB-E1-033-004 |
| CLAR-002 | BR2; SPEC-002 | The masking rules are assumed under DL26: RW-LITOFF, RW-LEGAL and RW-AUDIT see party names; others do not. | Determines who may use free text and personal fields. | Treat as the assumed rule until Compliance provides the table; load it as data. | RESOLVED | SPEC-RWB-E1-033-002 |
| CLAR-003 | AC1; SPEC-004 | Is the 2-second target an approved NFR? | Determines the SIT performance gate. | It is the story's AC1 target; section 13 sets 95th percentile over 50 runs. Confirm with the NFR owner. | RESOLVED | SPEC-RWB-E1-033-004 |
| CLAR-004 | BR6; SPEC-012 | Which date is the "stored date"? | Determines the date filter column. | `document.created_at`, as the story's data table states. | RESOLVED | SPEC-RWB-E1-033-012 |
| CLAR-005 | AC3; SPEC-006 | How is the free text term recorded in the access log? | Determines the audit payload. | SHA-256 of the term; the clear term is never stored. | RESOLVED | SPEC-RWB-E1-033-006 |
| CLAR-006 | AC8; SPEC-004, SPEC-008 | What do `total` and `capped` mean above the limit? | Determines the response and the message. | `total` stops at `SEARCH_MAX_RESULTS` (1000); `capped` is true; MSG-P5-021 shows 1000. | RESOLVED | SPEC-RWB-E1-033-004, SPEC-RWB-E1-033-008 |
| CLAR-007 | Contract; SPEC-001 | Which operators does `op` accept? | Determines the field condition. | `eq`, `gt`, `lt` and `between`, as section 12 states. | RESOLVED | SPEC-RWB-E1-033-001 |
| CLAR-008 | §15; SPEC-010 | `screens.txt` holds no screen ID for search across cases. | The page has no inventory ID or screen specification. | Build the page as Document search under the Documents menu from the story's states and the design system; allocate an SCR ID before build. No behaviour changes. | RESOLVED | SPEC-RWB-E1-033-010 |

`CLARIFICATION_STATUS: RESOLVED` — all 8 items are answered from the story, the FSD/TSD, the API specification or the decision log. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source; the page has no SCR ID and is specified from the story and the design system.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New read-only cross-case search endpoint and a new Document search page; access event before results.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: YES] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new search capability with a new endpoint and page]
REQUIREMENT_COVERAGE_SUMMARY: All 6 business rules, 10 acceptance criteria and 8 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 6] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] [UNBLOCK_ACTION: n/a; SCR ID allocation is a Low finding]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

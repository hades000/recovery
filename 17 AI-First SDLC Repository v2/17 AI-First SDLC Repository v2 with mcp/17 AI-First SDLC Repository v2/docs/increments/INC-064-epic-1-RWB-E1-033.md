# Increment Card — INC-064-epic-1-RWB-E1-033

**RWB-E1-033 — Search across cases**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-064` |
| Title | Search across cases |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-033` |
| RUN_ID | `INC-064-epic-1-RWB-E1-033` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P5 Document hub |
| Story type | User story |
| Priority | Should |
| Build order | 64 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-024, RWB-E1-053, RWB-E1-049 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P5 Document hub.

## Scope

**Story:** As a **litigation officer (RW-LITOFF)**, I want **a search across all cases in my scope by document type, date range, extracted field and free text, with every search written to the access log**, so that **I find a document in seconds without opening cases one by one, and every look at personal data can be audited**.

**Business outcome:** Legal, audit and recovery questions span many cases: every appraisal above a value, every notice from one court, every document naming a guarantor. Today each case folder is opened by hand (FSD P5 A2.6). This story searches the document index, the extracted fields and the OCR text across the cases the user may see, masks personal data the role may not see, and logs each search. It meets REQ-DCM-001 (documents found by their type, date and extracted fields) and REQ-ACA-006 (every read of the document store written to the access log), under control CTL-09 and CTL-11.

**Main flow:**
1. Litigation officer: opens Document search from the Documents menu and enters a type, a stored date range, a field condition (field, operator, value) and or a free text term.
2. Front end: calls GET /documents with the criteria.
3. DocumentSearchService: validates the criteria: at least one criterion, date order, free text length, field in the type's field list.
4. DocumentSearchService: checks with the masking policy that the role may search a personal field or free text; refuses otherwise.
5. DocumentSearchService: gets the case IDs in the user's scope through CaseDirectory.caseIdsInScope (all cases for scope ALL).
6. DocumentSearchRepository: queries active documents in those cases by type and stored date, joined to document_field for the field condition and to document_text for the free text, newest first, up to SEARCH_MAX_RESULTS.

**Acceptance criteria:**
- AC1: Search by field
- AC2: Role limit
- AC3: Free text
- AC4: Free text refused for a masked role
- AC5: No criterion
- AC6: Date range in the wrong order
- AC7: Free text length boundary
- AC8: More results than the limit
- AC9: Access log not confirmed
- AC10: Nothing matches

**Out of scope:**
- Answering a legal or audit document request with an export (FEAT-COM-07, Epic 4) and electronic discovery (Epic 2, REQ-DCM-017).
- Search within one case (RWB-E1-026).
- The access log query screen and its copy to the decision log (RWB-E1-039).
- Search on dates read from the document content, beyond field conditions (Epic 2).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-033-search-across-cases-v1.md` |
| Requirement IDs | REQ-DCM-001, REQ-ACA-006 |
| BRD section | Business Requirements Epic 1, sections 3.5 and 3.4; Business Requirements Program, sections 5.5 and 5.4 |
| Decision | None |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| Physical schema | `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Searches by type, date, field and free text in their scope |
| RW-LEGAL, legal counsel; RW-AUDIT, internal audit | Search across all cases (scope ALL); free text allowed under the assumed masking rule |
| RW-COMPLY, compliance and PDPA officer | Searches by type, date and non-personal fields; reads the access log |
| Other roles with Documents R | Search by type, date and non-personal fields in their scope |
| RW-CAPACITY and other roles without Documents R | No search |

## Contract extract

**GET /documents** (new, see additions) | Item | Value | |---|---| | Request | Query: type (doc_type_code), dateFrom, dateTo (date), field (field name), op (eq, gt, lt, between), value, value2, q (free text, 3 to 100 characters), page, size (default 50, maximum 50) | | Response | 200 DocumentSearchPage: items [documentId, caseId, caseNo, documentType, storedAt, source, matchedField, matchedValue, snippet], page, size, total, capped | | Errors | 401; 403 no Documents R (MSG-P4-002); 422 no criterion (MSG-GEN-001), date order (MSG-GEN-003), text length (MSG-GEN-002), personal field or free text not allowed (MSG-P5-020); 503 access log not confirmed (MSG-P5-019) or store unavailable (MSG-GEN-006) | | Authorization | Documents, right R, scope applied | | Idempotency | Not applicable; each call writes its own access event | **Published interfaces called** ```java // P3 Set<UUID> caseIdsInSco…

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Requirements approval | Product Owner | Chitchaya Muanchonchana | Source story set v7/v6, 16 Nov 2026 |
| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | CONTEXT-20261116 |
| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per-story plan gate |
| Pull request approval | Forward Deployed Engineer | Recovery tech lead | Per MR |

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder / Updater | Applicable | Context package CONTEXT-20261116. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in ACE. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Per API scope | Driven by the spec. |
| Quality and release | Functional Automation Test | Per UI scope | Driven by the spec. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Stop signals:** any guardrail in story §17; a migration that is not `V<seq>__<story>_<name>.sql`; a direct read of an ACE table outside `recovery.v_ace_*`.

**Guardrails:**

- No business value in code: limits, page size, text length and masking are data. - No personal data in logs, tests or prompts: the free text term is logged as a hash; names in tests are synthetic. - No read of another module's tables: scope and case numbers come through CaseDirectory, masking through the P4 interface. - A result is never returned before its access event is confirmed.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-033-search-across-cases-v1.md` |
| Specification | `output/INC-064-epic-1-RWB-E1-033/specify/spec.md` |
| Compliance validation | `output/INC-064-epic-1-RWB-E1-033/specify/compliance-validation.md` |
| Agent run log | `output/INC-064-epic-1-RWB-E1-033/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-064-epic-1-RWB-E1-033/plan/` |
| Implementation evidence | `output/INC-064-epic-1-RWB-E1-033/implement/` |
| API / functional test reports | `output/INC-064-epic-1-RWB-E1-033/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-064-epic-1-RWB-E1-033/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 10 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-033-search-across-cases-v1.md` |
| Output run | `output/INC-064-epic-1-RWB-E1-033/` |


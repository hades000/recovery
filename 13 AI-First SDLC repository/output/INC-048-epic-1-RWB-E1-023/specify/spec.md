# Technical Specification — RWB-E1-023 Case record view v1, read only

| Field | Value |
|---|---|
| Story | RWB-E1-023 — Case record view v1, read only |
| Epic / module | E1 / P3 Case and workflow |
| RUN_ID | `INC-048-epic-1-RWB-E1-023` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-010); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 023 Case record view v1 read only v1.md` |
| Upstream IDs | BRD-RWB-003; FR-RWB-010; REQ-OCC-007, REQ-RDF-009, REQ-ACA-005, REQ-ACA-006; US-RWB-E1-023; CTX-FEATURE-003, CTX-FEATURE-004, CTX-FEATURE-005; NFR-009 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `YES` — SCR-03 Case record gains the Epic 1 read-only layout: header plus Accounts, Parties, Contact history and Documents sections, with Loading, read only, on hold, stale and section-error states. |
| Logic In Scope | `YES` — scoped read, per-section business date, masking, access logging, partial-failure behaviour and the prescription/hold banner. |
| API In Scope | `YES` — five existing read endpoints are reused; `CaseAccount` and `CaseParty` gain additive response fields for the screen. |
| API Impact Type | `EXISTING_API_CHANGE` |
| Impacted Existing Nodes | `CaseAndWorkflowController`; `CaseAndWorkflowRepository`; API-P3-002, API-P3-004, API-P3-005, API-P3-014; P5 `GET /cases/{caseId}/documents`; `FieldMasker` (P4); `AccessEventPublisher` (P4); `RecoveryDataQuery` (P1); SCR-03. |
| New Nodes Required | `YES` — `CaseRecordQueryService`, `MaskingApplier`, `CaseRecordPage`, `CaseHeader`, `AccountsPanel`, `PartiesPanel`, `ContactHistoryPanel`, `DocumentsPanel`, `StaleBanner`, `OnHoldBanner`, `SectionMessage`. |
| Inherited Existing Behavior | Case and account/party links (RWB-E1-018); document hub (RWB-E1-024); masking rules (RWB-E1-037); access log (RWB-E1-039); data-product freshness stamps (RWB-E1-015); case list (RWB-E1-002, RWB-E1-031); roles and scope (RWB-E1-022, RWB-E1-037). |
| Frontend Changes Required | `YES` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every section shows the business date of the data product it reads. | SPEC-RWB-E1-023-003, -004, -005, -006, -007 | DIRECT | `dataAsOf` is carried on each section DTO from P1 or P5; the UI renders a `DataDateBadge`. | COVERED |
| BR2 | A section older than the latest business date shows the stale banner. | SPEC-RWB-E1-023-007 | DIRECT | Compare section `dataAsOf` with the current business date from the freshness stamp; MSG-P1-001 above the section. | COVERED |
| BR3 | Personal fields show masked unless the role may see them. | SPEC-RWB-E1-023-008 | DIRECT | `FieldMasker.mask` on the party and interaction DTOs; no rule means masked. | COVERED |
| BR4 | Every read of personal data is written to the access log. | SPEC-RWB-E1-023-009 | DIRECT | One AC-READ event per page open with field IDs and masked flags. | COVERED |
| BR5 | Only cases in the caller's scope open; others return 404. | SPEC-RWB-E1-023-010 | DIRECT | Scope check before any read; 404 MSG-P4-003, not 403. | COVERED |
| BR6 | The view has no edit control in Epic 1. | SPEC-RWB-E1-023-014 | DIRECT | Read-only React components; no PATCH or POST call. | COVERED |
| BR7 | The view loads in under 2 seconds with 50 documents. | SPEC-RWB-E1-023-015 | DIRECT | Parallel calls; paged documents; index `ix_interaction_case_time`; NFR-009. | COVERED |
| BR8 | Customer facts come from the profile ACE receives through COLLINS. | SPEC-RWB-E1-023-004 | DIRECT | Party facts through `RecoveryDataQuery.partiesFor`; no direct core-bank call. | COVERED |
| AC1 | The header, accounts, parties, contact history and first document page show in under 2 seconds at p95 over 50 openings. | SPEC-RWB-E1-023-015 | DIRECT | Performance test with 50 documents and 120 interactions. | COVERED |
| AC2 | Accounts show 97 days past due and THB 206,175.00 for A-7001, the section business date, and the header queue/owner/status/entry date. | SPEC-RWB-E1-023-002, -003, -007 | DIRECT | Header from `recovery_case`; account figures from P1; badge from `dataAsOf`. | COVERED |
| AC3 | Parties show the borrower, role BORROWER, segment RETAIL and the business date; contact history shows EFS entries with channel, direction, result and time. | SPEC-RWB-E1-023-004, -005 | DIRECT | Party profile through P1; interactions through P3 with source EFS. | COVERED |
| AC4 | A stale account product shows its date and MSG-P1-001 for the account product. | SPEC-RWB-E1-023-007 | DIRECT | Per-section staleness; the rest of the page still renders. | COVERED |
| AC5 | A case outside scope returns 404 with MSG-P4-003 and no case data. | SPEC-RWB-E1-023-010 | DIRECT | Scope predicate applied before composition. | COVERED |
| AC6 | If the document hub does not answer, Documents shows MSG-P3-023 and the other sections show. | SPEC-RWB-E1-023-013 | DIRECT | Per-section timeout; partial result. | COVERED |
| AC7 | If the personal-data access log cannot be written, personal fields stay masked and Parties shows MSG-P3-023. | SPEC-RWB-E1-023-009 | DIRECT | Masked fallback; no unmasked response on log failure. | COVERED |
| AC8 | A phone collector sees the customer number masked as `xxxxxx4821`; the access log records the masked read. | SPEC-RWB-E1-023-008, -009 | DIRECT | Masking pattern from the masking rule; field-level flags in the log. | COVERED |
| AC9 | An on-hold case shows MSG-P3-004 with the deviation and the prescription date. | SPEC-RWB-E1-023-011 | DIRECT | Banner when `status = ON_HOLD` or `legal_hold = true`. | COVERED |
| AC10 | A case with no documents and no contact history shows MSG-P3-024 in each section. | SPEC-RWB-E1-023-012 | DIRECT | Empty state per section. | COVERED |
| X1 | A data product is from an earlier date. | SPEC-RWB-E1-023-007 | DIRECT | Stale banner. | COVERED |
| X2 | The case is outside the user's scope. | SPEC-RWB-E1-023-010 | DIRECT | 404. | COVERED |
| X3 | The document hub does not answer. | SPEC-RWB-E1-023-013 | DIRECT | Section message. | COVERED |
| X4 | The access log cannot be written. | SPEC-RWB-E1-023-009 | DIRECT | Masked fallback. | COVERED |
| X5 | The role may not see a field unmasked. | SPEC-RWB-E1-023-008 | DIRECT | Masked. | COVERED |
| X6 | The case is on hold. | SPEC-RWB-E1-023-011 | DIRECT | On-hold banner. | COVERED |
| X7 | No documents and no contact history. | SPEC-RWB-E1-023-012 | DIRECT | Empty sentences. | COVERED |
| X8 | A role without Case record R opens the view. | SPEC-RWB-E1-023-017 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **case owner (RW-CASEOWN)**, I want **one read-only screen per case with the case ID, accounts, arrears,
owner, queue, stage, status, contact history and documents, read from the data products with the business
date of each**, so that **I stop searching files and systems to understand a case**.

The story delivers the Epic 1 read-only half of SCR-03. It does not add the timeline (RWB-E1-035), the
editable view (RWB-E2-016), document upload (RWB-E1-026) or collateral (Epic 2). The case owner is the
primary user; team managers and control roles read the same screen within their scope.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | The user opens a case from SCR-02 Case list, My work or search; the route carries `caseId`. |
| Preconditions | RWB-E1-018 done (case, account and party links); RWB-E1-024 done (documents by case); RWB-E1-037 done (masking rules in force, DL26); RWB-E1-039 done (access events published); data products carry `data_as_of` (DL20); the user holds Case record R and the case is in scope. |
| Input | `caseId`; caller session (user, roles, scope); current business date. |
| Output | One `Case` header; `CaseAccount[]`; `CaseParty[]`; `InteractionPage`; `DocumentPage`; AC-READ access event. |
| Feature flag | `rwb.p3.caserecordview`. Off: SCR-03 shows the case header only. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `recovery_case` | `case_no`, `product_group`, `status`, `stage_code`, `route_code` | P3 case row | Read only | Header shows the stored value; no edit control |
| `recovery_case` | `owner_user_id`, `queue_id`, `team_code` | P3 case row and `queue` | Read only | Owner name resolved from the ACE user directory; blank when unassigned |
| `recovery_case` | `entry_date`, `prescription_date`, `deviation_open`, `legal_hold` | P3 case row | Read only | Prescription date shown in the header and the on-hold banner |
| `case_account` | `is_primary` | P3 link row | Read only | Primary account marked |
| `loan_account` | `account_no`, `principal_outstanding`, `total_balance`, `days_past_due`, `bucket`, `data_as_of` | P1 interface | Read only | Figures and date from the same product snapshot |
| `party` | `cif_no`, `first_name`, `last_name`, `segment` | P1 interface | Read only, masked by role | Masked values never leave the server unmasked |
| `interaction` | `occurred_at`, `channel`, `direction`, `contact_result`, `source_system`, `summary` | P3 interaction table | Read only, summary masked | EFS history is read-only |
| `document` | `document_type`, `source`, `doc_version`, `stored_at` | P5 endpoint | Read only | First page only; link opens the document view |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| Any displayed status | View opened | Case in scope | Unchanged | Read only; AC-READ access event |
| `ON_HOLD` | View opened | `status = ON_HOLD` or `legal_hold = true` | Unchanged | MSG-P3-004 banner with the deviation and prescription date |

This story writes no case status. It displays the status and the hold flag written by other stories.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | A section's product is older than the business date | Section renders with its date and the stale banner; other sections unaffected | MSG-P1-001 |
| X2 | Case outside scope | 404; no data returned | MSG-P4-003 |
| X3 | P5 document call exceeds 3 seconds or fails | Documents section shows the section message; header, accounts, parties and contact history render | MSG-P3-023 |
| X4 | AC-READ access event cannot be written | Personal fields remain masked; Parties shows the section message; no unmasked value is returned | MSG-P3-023 |
| X5 | Role may not unmask a field | Field renders masked; the access log records `masked = true` | None |
| X6 | Case on hold | On-hold banner with deviation/legal hold and prescription date | MSG-P3-004 |
| X7 | Section has no rows | Empty sentence per section | MSG-P3-024 |
| X8 | Caller lacks Case record R | 403 before any read | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `EXISTING_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/cases/{caseId}` (API-P3-002); `GET /cases/{caseId}/accounts` (API-P3-004); `GET /cases/{caseId}/parties` (API-P3-005); `GET /cases/{caseId}/interactions` (API-P3-014); `GET /cases/{caseId}/documents` (P5). |
| Contract delta | Additive only: `CaseAccount` adds `accountNo`, `daysPastDue`, `principalOutstanding`, `totalBalance`, `bucket`, `dataAsOf`; `CaseParty` adds `displayName`, `customerNo`, `segment`, `dataAsOf`. No field is removed or renamed. |
| Backward compatibility | Compatible. Existing consumers ignore the new fields. |
| Authorization | Case record R with scope for the four P3 endpoints; Documents R with scope for the P5 endpoint. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 503 store unavailable; section-level MSG-P3-023 on a partial failure. |
| Versioning | No version bump; additive fields are backward compatible. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-OCC-007; SPEC-RWB-E1-023-002..015 | New `CaseRecordPage` and five section components with Loading, read only, on hold, stale and error states. | Each state renders; parallel calls issued once; badge shows the section date; stale and on-hold banners; empty and error messages; masked value rendered as received; no personal data in fixtures. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-RDF-009, REQ-ACA-005, REQ-ACA-006; SPEC-RWB-E1-023-001..017 | New query service, masking applier, controller changes, scope check and P1/P5 composition. | Header and section composition; each `dataAsOf`; stale detection; masking by role; AC-READ event on success; masked fallback on log failure; scope 404; P5 timeout partial result; empty sections. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `CaseAndWorkflowController` | Controller | The four P3 read endpoints; access check; scope; problem responses. |
| `CaseRecordQueryService` | Service | Composes the case header, accounts, parties and interactions; attaches `dataAsOf` per section. |
| `MaskingApplier` | Service | Calls `FieldMasker` (RWB-E1-037), publishes AC-READ through `AccessEventPublisher` (RWB-E1-039), and masks every personal field when the publish fails. |
| `CaseAndWorkflowRepository` | Repository | Reads `recovery_case`, `case_account`, `case_party`, `interaction`, `queue`. |
| `CaseRecordPage` | React component | SCR-03 read-only layout; parallel calls; per-section timeout. |
| `CaseHeader`, `AccountsPanel`, `PartiesPanel`, `ContactHistoryPanel`, `DocumentsPanel` | React components | One section each, each with a `DataDateBadge`. |
| `StaleBanner`, `OnHoldBanner`, `SectionMessage` | React components | MSG-P1-001, MSG-P3-004, MSG-P3-023 and MSG-P3-024. |

### Read algorithm

1. Check Case record R and resolve the caller's scope.
2. Load the case; if absent or outside scope, return 404 MSG-P4-003.
3. Issue the five reads in parallel: case (already loaded), accounts, parties, interactions, documents.
4. For accounts and parties, call `RecoveryDataQuery` with the linked account and party IDs; the P1 response carries `dataAsOf`.
5. Apply `FieldMasker` to party and interaction DTOs; build the AC-READ event with field IDs and masked flags.
6. Publish AC-READ; on failure, force all personal fields to masked and mark the Parties section unavailable.
7. Compare each section `dataAsOf` with the business date; mark stale sections.
8. Return the composed response; the UI renders each section independently.

### Data and migration

- Reads `recovery_case`, `case_account`, `case_party`, `interaction`, `queue` only.
- Uses `ix_interaction_case_time` for the contact-history page.
- No migration. No write to a P3 table.
- No personal data in application logs: the log carries `caseNo`, section names and field IDs, never values.

### Events and access log

| Event | Payload | When |
|---|---|---|
| AC-READ (access log) | `actorUserRef`, `caseId`, `area = Case record`, `right = R`, field IDs, masked flags, `dataAsOf` per section | On every successful page composition |

No domain event is published. The access log write is synchronous; a failed write downgrades the response to
fully masked rather than returning unmasked personal data.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-CASEOWN | Case record R | Own |
| RW-TEAMMGR | Case record R | Team |
| RW-PHONECOL | Case record R, masked | Own |
| RW-CONDUCT, RW-AUDIT | Case record R | All |
| RW-REFADM, RW-SECADM | No Case record right; refused | — |
| SY-CASEWF | Case record R through the published interface | All |

Every endpoint uses Spring Security method security with the capability area and right. Scope filters every
query; an out-of-scope case returns 404, not 403, so the caller cannot infer that the case exists.

### Observability and operations

- Metrics: page opens; per-section latency; stale sections; masked fields; AC-READ failures; P5 timeouts.
- Alerts: p95 page latency above 2 seconds; AC-READ failure rate; P5 error rate.
- Audit: AC-READ entries in the access log; PII access record through the ACE common module.
- Run book entry under RWB-E1-056.

### Performance

- Target: under 2 seconds at p95 for a case with 50 documents and 120 interactions (NFR-009).
- Parallel section reads; documents and interactions paged; no N+1 party or account lookup.
- Test with 50 openings in SIT; record the p95 in the test evidence.

### Feature flag and rollback

- `rwb.p3.caserecordview`. Off: SCR-03 shows the case header only; the section endpoints remain available.
- Rollback: turn the flag off; no migration to reverse; the additive DTO fields remain harmless.

## Screens and design evidence

SCR-03 Case record, states Loading, read only and on hold. The layout is specified in
`requirement/legacy/07-screens-and-experience/recovery-workbench-screen-specifications-v1.md` (SCR-03) and
the local prototype `recovery-workbench-screen-prototype-v1-html.md`; there is no Figma source. The header
carries case number, product, status, stage, route, owner, queue, entry date, prescription date, deviation
and hold flags. The five sections follow in that order.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-023-01 | AC1, BR7 | Performance | Case with 50 documents and 120 interactions, 50 openings | p95 under 2 seconds; all sections render |
| TC-E1-023-02 | AC2, BR1 | System | Account A-7001 at 97 DPD, balance THB 206,175.00 | Figures and 2026-12-02 badge; header queue/owner/status/entry date |
| TC-E1-023-03 | AC3, BR8 | System | Party profile from the 2026-12-02 COLLINS load | BORROWER, RETAIL, badge 2026-12-02; EFS contact rows |
| TC-E1-023-04 | AC4, BR2 | System | Account product from 2026-12-02, business date 2026-12-03 | MSG-P1-001 with 2026-12-02; other sections unaffected |
| TC-E1-023-05 | AC5, BR5 | System | Case of team LIT-BKK; user scope Own | 404 MSG-P4-003; no data |
| TC-E1-023-06 | AC6, X3 | System | P5 does not answer within 3 seconds | Documents MSG-P3-023; other sections render |
| TC-E1-023-07 | AC7, X4 | System | Access log store unavailable | Personal fields masked; Parties MSG-P3-023 |
| TC-E1-023-08 | AC8, BR3, BR4 | System | Phone collector without unmask right | Customer number `xxxxxx4821`; AC-READ with masked flag |
| TC-E1-023-09 | AC9, X6 | System | Case ON_HOLD for X1, prescription 2028-03-15 | MSG-P3-004 with X1 and 2028-03-15 |
| TC-E1-023-10 | AC10, X7 | System | Case with no documents and no interactions | MSG-P3-024 in both sections |
| TC-E1-023-11 | X8 | Security | RW-REFADM opens the case | 403 MSG-P4-002 |
| TC-E1-023-12 | UI states | Unit | Loading, read only, stale, on hold, empty, error | Correct state and message; no edit control |

## Guardrails

- No business value in code: masking rules, labels, the section timeout and the type lists are data.
- No personal data in logs, tests or prompts; synthetic parties only; the application log holds case numbers and field IDs.
- No read of another module's tables: accounts and parties through `RecoveryDataQuery` (P1), documents through the P5 endpoint.
- Personal fields are never shown unmasked when the access log write fails.
- The view is read only in Epic 1; no edit, upload or delete affordance.

## Out of scope

- The history timeline panel (RWB-E1-035).
- The full editable case view with collateral, decisions and timers (RWB-E2-016).
- Document upload and search (RWB-E1-026).
- Collateral and valuation sections (Epic 2, after the CCMS and SVAF loads).

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | Contract; SPEC-006 | The story's documents row says Case record R, while API-P5 requires Documents R. Which applies? | Determines whether a case reader without Documents R sees the page or a section message. | The P5 endpoint keeps Documents R; a caller without it sees the Documents section message MSG-P3-023 and the rest of the page. The page itself needs Case record R only. | RESOLVED | SPEC-006, SPEC-013 |
| CLAR-002 | BR2; SPEC-007 | What is "the latest business date" for staleness? | Determines when the banner appears. | The business date of the current daily load, from the freshness stamp (RWB-E1-015); a section older than it is stale. | RESOLVED | SPEC-007 |
| CLAR-003 | X3; SPEC-013 | Is the 3-second section timeout fixed? | Determines configurability. | Parameter `caserecord.section.timeout.ms` = 3000 (assumed; DL11) from RWB-E1-042. | RESOLVED | SPEC-013 |
| CLAR-004 | AC7; SPEC-009 | May the view return unmasked data if the access log fails? | Determines the PDPA fallback. | No. Personal fields stay masked and the section shows MSG-P3-023; the story X4 and guardrails. | RESOLVED | SPEC-009 |
| CLAR-005 | AC1; SPEC-006 | How many documents are on the first page? | Determines the read size. | First page, default 50, maximum 200, per API-P5 and the story AC1. | RESOLVED | SPEC-006 |
| CLAR-006 | API; SPEC-016 | Does the view need a new endpoint? | Determines API impact. | No. Five existing read endpoints; only additive `CaseAccount` and `CaseParty` fields. | RESOLVED | SPEC-016 |

`CLARIFICATION_STATUS: RESOLVED` — all 6 items are answered from the story, the API specification, the
screen specification or the decision log. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] — SCR-03 Case record is specified in the screen inventory and the local screen specification/prototype; no Figma source is claimed.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New read-only SCR-03 case record view; five existing read endpoints reused with additive account and party response fields.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: YES] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: EXISTING_API_CHANGE] [REASON: new SCR-03 read-only screen plus additive CaseAccount and CaseParty fields]
REQUIREMENT_COVERAGE_SUMMARY: All 8 business rules, 10 acceptance criteria and 8 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 8] [COVERED_RULES: 8] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

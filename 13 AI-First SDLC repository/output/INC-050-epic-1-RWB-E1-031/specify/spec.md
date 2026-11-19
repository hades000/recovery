# Technical Specification — RWB-E1-031 Queue and owner on the case list with filters

| Field | Value |
|---|---|
| Story | RWB-E1-031 — Queue and owner on the case list with filters |
| Epic / module | E1 / P3 Case and workflow |
| RUN_ID | `INC-050-epic-1-RWB-E1-031` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-009, FR-RWB-005); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 031 Queue and owner on the case list with filters v1.md` |
| Upstream IDs | BRD-RWB-003, BRD-RWB-009; FR-RWB-009, FR-RWB-005; REQ-CWC-007, REQ-ACA-009; US-RWB-E1-031; CTX-FEATURE-003, CTX-FEATURE-004; NFR-008 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `YES` — SCR-02 Case list gains queue and owner columns, queue/team/status filters, an Export action and the Loading, empty, list and filtered states. |
| Logic In Scope | `YES` — scoped query, AND filters, export row limit, masking, access log before the file, file naming. |
| API In Scope | `YES` — `GET /api/recovery/v1/cases` gains the `team` query parameter; `GET /api/recovery/v1/cases/export` is delivered. |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | `CaseAndWorkflowController`; `CaseQueryService`; `CaseAndWorkflowRepository`; API-P3-001 `GET /cases`; `FieldMasker` (P4); `AccessEventPublisher` (P4); ACE user directory; SCR-02. |
| New Nodes Required | `YES` — `CaseExportService`, `CaseListPage`, `CaseListFilters`, `ExportButton`, index `ix_case_team_status`. |
| Inherited Existing Behavior | Allocation result on the case (RWB-E1-020); access log (RWB-E1-039); masking rules (RWB-E1-037); queues (RWB-E1-019); lists through P4; labels (DL10); case list base (RWB-E1-002). |
| Frontend Changes Required | `YES` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | The list holds only cases inside the caller's scope (Own, Team, Region, All). | SPEC-RWB-E1-031-001 | DIRECT | Scope predicate from the P4 scope service; an out-of-scope queue returns an empty page, not 403. | COVERED |
| BR2 | Filters combine with AND. | SPEC-RWB-E1-031-001 | DIRECT | One query with all predicates; no filter is ignored. | COVERED |
| BR3 | Every export is written to the access log before the file is made. | SPEC-RWB-E1-031-006 | DIRECT | AC-EXPT write is the first step; failure returns 503 and no file. | COVERED |
| BR4 | Export columns follow the masking rules for the caller's role. | SPEC-RWB-E1-031-007 | DIRECT | `FieldMasker` on each row; no customer name or ID number in the file. | COVERED |
| BR5 | An export holds at most the configured number of rows. | SPEC-RWB-E1-031-005 | DIRECT | `caselist.export.maxrows` = 10,000 (assumed; DL11); 10,000 allowed, 10,001 refused. | COVERED |
| BR6 | A screen responds in under 2 seconds. | SPEC-RWB-E1-031-012 | DIRECT | NFR-008; indexed query; paged reads; export separate. | COVERED |
| AC1 | Filtering by queue DIL-BKK-CO shows 64 cases, each with owner and status; no other queue shows. | SPEC-RWB-E1-031-001, -002 | DIRECT | Queue filter plus scope; owner and status columns. | COVERED |
| AC2 | Export of 51 filtered cases downloads an Excel file with 51 rows; the access log holds user, time, filters and row count. | SPEC-RWB-E1-031-006, -007, -008 | DIRECT | AC-EXPT before build; xlsx with header row. | COVERED |
| AC3 | No case meets the filters: empty state with MSG-P3-020. | SPEC-RWB-E1-031-004 | DIRECT | Empty page; the UI shows the message. | COVERED |
| AC4 | Export above the limit: no file, MSG-P3-021 with maximum 10000. | SPEC-RWB-E1-031-005 | DIRECT | 422 before the access log; no file. | COVERED |
| AC5 | Access log unavailable: no file, MSG-P7-003. | SPEC-RWB-E1-031-006 | DIRECT | 503; nothing written. | COVERED |
| AC6 | Queue outside the scope: no case, empty state with MSG-P3-020. | SPEC-RWB-E1-031-001, -011 | DIRECT | Scope wins over the filter; no existence leak. | COVERED |
| AC7 | A case with no owner shows with a blank owner cell. | SPEC-RWB-E1-031-010 | DIRECT | Null owner renders blank; the row stays. | COVERED |
| AC8 | Exactly 10,000 rows: the export downloads with 10,000 rows. | SPEC-RWB-E1-031-009 | DIRECT | Boundary inclusive. | COVERED |
| X1 | No case meets the filters. | SPEC-RWB-E1-031-004 | DIRECT | MSG-P3-020. | COVERED |
| X2 | Filtered list above the export limit. | SPEC-RWB-E1-031-005 | DIRECT | MSG-P3-021. | COVERED |
| X3 | Access log cannot be written. | SPEC-RWB-E1-031-006 | DIRECT | MSG-P7-003. | COVERED |
| X4 | Filter names an out-of-scope queue. | SPEC-RWB-E1-031-011 | DIRECT | Empty page. | COVERED |
| X5 | A case has no owner. | SPEC-RWB-E1-031-010 | DIRECT | Blank cell. | COVERED |
| X6 | Exactly 10,000 rows. | SPEC-RWB-E1-031-009 | DIRECT | Allowed. | COVERED |
| X7 | A role without Case record R opens the list. | SPEC-RWB-E1-031-014 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **team manager (RW-TEAMMGR)**, I want **the queue and owner columns on the case list, with filters by
queue, team and status and an export to Excel**, so that **I see my queues and who owns each case without a
new screen**.

The story completes the case list that RWB-E1-002 established. It does not add the My queue or Team queues
screens (RWB-E2-011, SCR-07), the base filters by product, stage, age and deviation (RWB-E1-002), or the
masking rules themselves (RWB-E1-037). The export is the first PDPA-relevant export on the list and must be
logged before the file exists.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | The user opens SCR-02 Case list; changes a filter; chooses Export. |
| Preconditions | RWB-E1-020 done (queue, team and owner on the case); RWB-E1-039 done (access log); user holds Case record R with a scope; `caselist.export.maxrows` = 10,000 (assumed; DL11) from RWB-E1-042; owner display names from the ACE user directory. |
| Input | Query: queue, team, status, owner, product, stage, page, size, sort. |
| Output | `CasePage`; an `.xlsx` export; one AC-EXPT access event per export. |
| Feature flag | `rwb.p3.caselistqueue`. Off: the list hides the queue/owner columns and the export. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `recovery_case` | `case_no`, `product_group`, `status`, `stage_code`, `entry_date` | P3 case row | Read only | Columns as in SCR-02 |
| `recovery_case` | `queue_id` | P3 case row; joined to `queue` | Read only | Shows the queue code; blank only when unassigned |
| `recovery_case` | `owner_user_id` | P3 case row; display name from ACE | Read only | Blank cell when null; no placeholder text |
| `recovery_case` | `team_code` | P3 case row | Read only | Filterable; used by scope |
| `queue` | `queue_code`, `queue_name` | P3 queue row | Read only | Filter picker shows in-scope queues |
| Filter | `queue` | User choice | Editable | UUID; must resolve to a queue; out-of-scope returns empty |
| Filter | `team` | User choice | Editable | LOV-TEAM; new query parameter |
| Filter | `status` | User choice | Editable | LOV-CASE-STATUS |
| Export | File name | System | System | `Case list YYYYMMDD 1.xlsx`; no personal data in the name |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| Any case status | List opened or filtered | Case in scope | Unchanged | Read only; no status write |
| Any case status | Export chosen | Within the row limit and the access log written | Unchanged | AC-EXPT event; file built |

This story does not change a case status. It reads queue, owner and status only.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | No case meets the filters | Empty page; the UI shows the empty state | MSG-P3-020 |
| X2 | Filtered list above the export limit | 422; no file | MSG-P3-021 with `{max}` = 10000 |
| X3 | Access log store unavailable | 503; no file; nothing written | MSG-P7-003 |
| X4 | Filter names an out-of-scope queue | Empty page; no existence leak | MSG-P3-020 |
| X5 | Case has no owner | Row renders with a blank owner cell | None |
| X6 | Exactly 10,000 rows | Export allowed | None |
| X7 | Role without Case record R | 403 before the query | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| Existing endpoint changed | `GET /api/recovery/v1/cases` (API-P3-001) gains `team` (LOV-TEAM); the response already carries `queueId`, `ownerUserId`, `teamCode`. Additive, backward compatible. |
| New endpoint | `GET /api/recovery/v1/cases/export` (API-P3-017): same filters without `page`/`size`; returns `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`; 422 above the limit; 503 when the access log fails. |
| Backward compatibility | The `team` parameter is optional; existing callers are unaffected. The export is new. |
| Authorization | Case record R with scope for both; export additionally writes AC-EXPT through P4. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 422 MSG-P3-021; 503 MSG-P7-003. |
| Versioning | No version bump; additive parameter and a new endpoint under the same major version. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-CWC-007, REQ-ACA-009; SPEC-RWB-E1-031-002..012 | New columns, filter bar, Export button and four list states on SCR-02. | Columns render; filters issue the right query; empty and filtered states; export success, limit and log-failure messages; blank owner; no personal data in fixtures. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-CWC-007, REQ-ACA-009; SPEC-RWB-E1-031-001..014 | Scoped query, team filter, export service, row limit, access log and masking. | Scope per role; each filter and AND combination; 10,000/10,001 boundary; access log before file; log failure; masked columns; 2-second query on 26,500 cases. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `CaseAndWorkflowController` | Controller | `GET /cases` with the team filter; `GET /cases/export`; problem responses. |
| `CaseQueryService` | Service | Builds the scoped query with all filters; joins `queue` for code and name. |
| `CaseExportService` | Service | Row-limit check, AC-EXPT access event, xlsx build with masked columns. |
| `CaseAndWorkflowRepository` | Repository | Paged query on `recovery_case` and `queue`. |
| `CaseListPage` | React component | SCR-02 with queue and owner columns and Loading, empty, list and filtered states. |
| `CaseListFilters` | React component | Queue, team and status pickers from the queues and lists in force. |
| `ExportButton` | React component | Calls the export; shows MSG-P3-021 or MSG-P7-003. |

### Query and export algorithm

1. Check Case record R; resolve the caller's scope.
2. Validate `status` against LOV-CASE-STATUS and `team` against LOV-TEAM; an unknown value returns 422 MSG-GEN-007.
3. Build one predicate: scope AND queue AND team AND status AND the other supplied filters.
4. Read the page ordered by the requested `sort`; the story does not fix a default, so the implementation plan records the chosen default.
5. For export: count the filtered rows; if greater than `caselist.export.maxrows`, return 422 MSG-P3-021.
6. Publish AC-EXPT with user, time, filters and row count; on failure return 503 MSG-P7-003.
7. Build the xlsx with a header row and one row per case; apply `FieldMasker` per row.
8. Return the file named `Case list YYYYMMDD 1.xlsx`.

### Data and migration

- Reads `recovery_case` and `queue` only.
- Uses `ix_case_status_queue (status, queue_id)` and `ix_case_owner_status`.
- Migration `V031_1__case_team_index.sql` adds `ix_case_team_status ON recovery_case (team_code, status)`.
- No personal data in the export beyond the masked columns; the file holds no customer name or ID number.

### Events

| Event | Payload | When |
|---|---|---|
| AC-EXPT (access log) | `actorUserRef`, `area = Case record`, `right = R`, filters, `rowCount`, time | Before the export file is built |

No domain event is published. A failed AC-EXPT write blocks the export.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-TEAMMGR | Case record R | Team |
| RW-CASEOWN | Case record R | Own |
| Every role with Case record R | Case record R | Its scope |
| RW-REFADM, RW-SECADM | No Case record right; refused | — |
| RW-COMPLY | Reads AC-EXPT entries in the access log | All |

Every request uses Spring Security method security with the capability area and right. Scope filters the
query; an out-of-scope queue returns an empty page rather than 403 so the caller cannot infer queue
existence.

### Observability and operations

- Metrics: list reads; filter use; export count; export rows; export refusals; AC-EXPT failures; p95 latency.
- Alerts: p95 above 2 seconds; AC-EXPT failure rate; export refusal spike.
- Audit: AC-EXPT entries for every export.
- Run book entry under RWB-E1-056.

### Performance

- Target: list under 2 seconds on 26,500 cases (NFR-008).
- Indexed scope and filter predicates; paged reads; export streams rows and is not loaded into memory twice.
- Test the filtered list and the 10,000-row export in SIT.

### Feature flag and rollback

- `rwb.p3.caselistqueue`. Off: the list hides the queue and owner columns and the export; the base list remains.
- Rollback: turn the flag off; the index remains and is harmless.

## Screens and design evidence

SCR-02 Case list, states Loading, empty, list and filtered. The layout is specified in
`requirement/legacy/07-screens-and-experience/recovery-workbench-screen-specifications-v1.md` (SCR-02) and
the local prototype `recovery-workbench-screen-prototype-v1-html.md`; there is no Figma source. Columns:
case number, product, status, stage, queue, owner, entry date. Filters: queue, team, status. Export uses the
filters shown.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-031-01 | AC1, BR1, BR2 | System | 64 cases in DIL-BKK-CO, 20 in DIL-BKK-OVF | 64 rows; each with owner and status; no other queue |
| TC-E1-031-02 | AC2, BR3, BR4 | System | 51 cases filtered by queue and status | 51-row xlsx; AC-EXPT with user, time, filters and 51 |
| TC-E1-031-03 | AC3, X1 | System | Filter with no match | Empty state; MSG-P3-020 |
| TC-E1-031-04 | AC4, BR5 | System | 10,001 cases, scope All | 422 MSG-P3-021 with 10000; no file |
| TC-E1-031-05 | AC5, BR3 | System | Access log store down | 503 MSG-P7-003; no file |
| TC-E1-031-06 | AC6, BR1 | System | Queue of another team | Empty page; MSG-P3-020 |
| TC-E1-031-07 | AC7, X5 | System | Case in DIL-BKK-OVF with no owner | Row shows; owner cell blank |
| TC-E1-031-08 | AC8, BR5 | System | Exactly 10,000 cases | File with 10,000 rows |
| TC-E1-031-09 | X7 | Security | RW-REFADM calls GET /cases | 403 MSG-P4-002 |
| TC-E1-031-10 | BR6 | Performance | 26,500 cases, filtered list | Under 2 seconds |
| TC-E1-031-11 | UI states | Unit | Loading, empty, list, filtered, export error | Correct state and message; no personal data in fixtures |

## Guardrails

- No business value in code: the export limit, filters, labels and lists come from data.
- No personal data in logs, tests or prompts; the export applies masking by role and holds no customer name or ID number.
- No read of another module's tables: the access log through `AccessEventPublisher` (P4); owner names through the ACE user directory; lists through P4.
- The export is never made when its access log entry cannot be written.

## Out of scope

- My queue and team queue screens (RWB-E2-011, SCR-07 in Epic 2).
- The base case list filters by product, stage, age and deviation (RWB-E1-002).
- The masking rules themselves (RWB-E1-037, DL26).
- The Power BI case list (RWB-E1-002 reporting path).

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR5; SPEC-005 | Is the export limit fixed at 10,000? | Determines the boundary and the message. | `caselist.export.maxrows` = 10,000 (assumed; DL11); data, not code. | RESOLVED | SPEC-005 |
| CLAR-002 | AC2; SPEC-008 | What columns does the export carry? | Determines the file contract. | The SCR-02 list columns in story §15: case number, product, status, stage, queue, owner, entry date. The API description's extra age/service-level/prescription/next-action columns belong to the stories that add them. | RESOLVED | SPEC-008 |
| CLAR-003 | BR3; SPEC-006 | Is the access log written before the file is built? | Determines the failure path. | Yes; the story flow step 7 and BR3. A failed write returns 503 and no file. | RESOLVED | SPEC-006 |
| CLAR-004 | BR4; SPEC-007 | Does the export contain personal data? | Determines masking and PDPA treatment. | It carries the masked list columns only; no customer name or ID number (story §17). | RESOLVED | SPEC-007 |
| CLAR-005 | API; SPEC-013 | Is the team filter a contract change? | Determines API impact. | Yes; `team` is a new optional query parameter on API-P3-001, and API-P3-017 is delivered. | RESOLVED | SPEC-013 |
| CLAR-006 | AC6; SPEC-011 | Should an out-of-scope queue return 403 or an empty page? | Determines the existence-leak behaviour. | Empty page with MSG-P3-020; the story AC6 and BR1. | RESOLVED | SPEC-011 |

`CLARIFICATION_STATUS: RESOLVED` — all 6 items are answered from the story, the API specification or the
decision log. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] — SCR-02 Case list is specified in the screen inventory and the local screen specification/prototype; no Figma source is claimed.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: SCR-02 gains queue/owner columns, queue/team/status filters and an Excel export; new export endpoint and an additive team parameter.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: YES] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new API-P3-017 export endpoint plus an additive team filter on API-P3-001]
REQUIREMENT_COVERAGE_SUMMARY: All 6 business rules, 8 acceptance criteria and 7 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 6] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 1] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

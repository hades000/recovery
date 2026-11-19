# Technical Specification — RWB-E1-005 Excel and SharePoint inventory

| Field | Value |
|---|---|
| Story | RWB-E1-005 — Excel and SharePoint inventory |
| Epic / module | E1 / P1 Recovery data engine |
| RUN_ID | `INC-012-epic-1-RWB-E1-005` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-RDF-005); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 005 Excel and SharePoint inventory v1.md` |
| Upstream IDs | REQ-RDF-005; FEAT-RDF-07; US-RWB-E1-005; CTL-08; CTL-11; Principle 1; LOV-TEAM; LOV-TRACKER-LOCATION, LOV-UPDATE-CYCLE, LOV-TRACKER-DECISION, LOV-TRACKER-STATUS |
| Status | `SUCCESS` |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. The inventory is loaded by file and read through the endpoint; story §15. |
| Logic In Scope | `YES` — versioned inventory load, row checks, team coverage, status carry-over, filtered read. |
| API In Scope | `YES` — new `GET /api/recovery/v1/admin/trackers` (API-P1-004). |
| API Impact Type | `NEW_API_REQUIRED` — the endpoint is new; the contract is already listed in API Specification v2. |
| Impacted Existing Nodes | `tracker_inventory` (new); reference data service (RWB-E1-043); `data_product` (RWB-E1-001); `lov_value` (P4). |
| New Nodes Required | `YES` — `TrackerInventory`, `TrackerInventoryRepository`, `TrackerInventoryHandler`, `TrackerService`, `RecoveryDataEngineController` method. |
| Inherited Existing Behavior | `ReferenceTableHandler` load/approve flow (RWB-E1-043); data product catalog (RWB-E1-001); team list parameter (RWB-E1-042). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every team's Excel, SharePoint and local files are listed with owner, fields and update cycle. | SPEC-RWB-E1-005-001, 002, 009 | DIRECT | `tracker_inventory` columns; `field_list` jsonb; `GET /admin/trackers`. | COVERED |
| BR2 | Each tracker has a decision LOAD, RETIRE or KEEP with a reason; LOAD names a target data product. | SPEC-RWB-E1-005-003, 006, 007 | DIRECT | List checks; `target_product` required only for LOAD. | COVERED |
| BR3 | The inventory covers the six teams in the parameter. | SPEC-RWB-E1-005-005 | DIRECT | `tracker.inventory.teams`; one row per team minimum. | COVERED |
| BR4 | The inventory is a versioned load; a file with an exception is refused whole. | SPEC-RWB-E1-005-008, 010 | DIRECT | `validate` writes nothing; `apply` one transaction. | COVERED |
| BR5 | A tracker already in the previous version keeps its status. | SPEC-RWB-E1-005-007 | DIRECT | Lookup by `tracker_code`; carry `status`. | COVERED |
| BR6 | Field names carry a personal data tag; personal fields are not loaded later. | SPEC-RWB-E1-005-012 | DIRECT | `field_list[].personal`; RWB-E1-010 drops personal fields. | COVERED |
| AC1 | A 23-row file loads for TRK-2026.11; LIT returns 6 trackers including LIT-07 with 18 fields. | SPEC-RWB-E1-005-001, 002, 008, 009, 013 | DIRECT | 5 TDR, 3 DIL, 6 LIT, 4 NPA, 2 DEBT_SALE, 3 WRITE_OFF. | COVERED |
| AC2 | Every tracker has a decision and reason; 14 LOAD name a product; 14 LOAD + 6 RETIRE are LISTED; 3 KEEP are KEPT. | SPEC-RWB-E1-005-003, 006, 007 | DIRECT | First status by decision. | COVERED |
| AC3 | A file with no DEBT_SALE row is refused whole. | SPEC-RWB-E1-005-005, 008 | DIRECT | MSG-P1-016. | COVERED |
| AC4 | A row without a decision is refused whole. | SPEC-RWB-E1-005-002, 008 | DIRECT | MSG-GEN-001. | COVERED |
| AC5 | A value outside its list is refused whole. | SPEC-RWB-E1-005-003, 008 | DIRECT | MSG-P1-007. | COVERED |
| AC6 | A LOAD row without a target product is refused whole. | SPEC-RWB-E1-005-006, 008 | DIRECT | MSG-GEN-001. | COVERED |
| AC7 | A duplicate tracker code is refused whole. | SPEC-RWB-E1-005-004, 008 | DIRECT | MSG-P1-017. | COVERED |
| AC8 | The same file loaded again writes nothing. | SPEC-RWB-E1-005-010 | DIRECT | Content hash; MSG-P1-011. | COVERED |
| X1 | A team has no row. | SPEC-RWB-E1-005-005 | DIRECT | MSG-P1-016. | COVERED |
| X2 | A row has no decision or reason. | SPEC-RWB-E1-005-002 | DIRECT | MSG-GEN-001. | COVERED |
| X3 | A value is outside its list. | SPEC-RWB-E1-005-003 | DIRECT | MSG-P1-007. | COVERED |
| X4 | A LOAD row has no target product. | SPEC-RWB-E1-005-006 | DIRECT | MSG-GEN-001. | COVERED |
| X5 | A tracker code appears twice. | SPEC-RWB-E1-005-004 | DIRECT | MSG-P1-017. | COVERED |
| X6 | The same file is loaded again. | SPEC-RWB-E1-005-010 | DIRECT | MSG-P1-011. | COVERED |
| X7 | A role without Reference data R lists the trackers. | SPEC-RWB-E1-005-011 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **data steward and data product owner (RW-DATASTEW)**, I want **every recovery team's Excel files, SharePoint lists and local files listed with owner, fields, update cycle and a load, retire or keep decision**, so that **each file can be loaded into its data product and then retired**.

The story creates the inventory as versioned reference data. It does not open, copy or change any tracker; it records what exists and what will replace it. The load and retirement stories move the status forward.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | RW-REFADM loads an inventory file through `POST /admin/reference-loads` with `table = tracker_inventory`; RW-DATASTEW confirms the version. |
| Preconditions | RWB-E1-001 done (DP01–DP14); RWB-E1-043 done (reference load handler); `tracker.inventory.teams` holds the six team codes; the inventory template is complete; RW-REFADM holds Reference data C. |
| Input | Inventory file (one row per tracker) with tracker code, team, name, location type, location, owner, field list, update cycle, target product, decision and reason. |
| Output | `tracker_inventory` rows for the version; `GET /admin/trackers` response. |
| Feature flag | `rwb.p1.tracker-inventory`. Off: the handler and endpoint are unavailable. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `tracker_inventory` | `tracker_code` | File | Load only | Unique per version; pattern from the team prefix. |
| `tracker_inventory` | `inventory_version` | File name stem (e.g. `TRK-2026.11`) | Load only | Required; same on every row; see CLAR-001. |
| `tracker_inventory` | `team_code` | File | Load only | Must be in LOV-TEAM; one of the six parameter teams. |
| `tracker_inventory` | `tracker_name` | File | Load only | Required. |
| `tracker_inventory` | `location_type` | File | Load only | EXCEL, SHAREPOINT, LOCAL_FILE, NONE. |
| `tracker_inventory` | `location_ref` | File | Load only | Optional; required unless `location_type = NONE`. |
| `tracker_inventory` | `owner_user_id` | File | Load only | Optional; synthetic test user in DEV/SIT. |
| `tracker_inventory` | `field_list` | File | Load only | JSON array of `{name, personal, mappedTo?}`; no values. |
| `tracker_inventory` | `update_cycle` | File | Load only | DAILY, WEEKLY, MONTHLY, AD_HOC. |
| `tracker_inventory` | `target_product` | File | Load only | Required for LOAD; must be DP01–DP14; null for RETIRE/KEEP. |
| `tracker_inventory` | `decision` | File | Load only | LOAD, RETIRE, KEEP; reason required. |
| `tracker_inventory` | `status` | System | System | First status LISTED for LOAD/RETIRE, KEPT for KEEP; carried over on a new version. |
| `tracker_inventory` | `valid_from` | Load parameter | Load only | Required. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | New tracker, decision LOAD or RETIRE | File valid | LISTED | Row written. |
| None | New tracker, decision KEEP | File valid | KEPT | Row written. |
| Previous status | New inventory version | Tracker code present | Unchanged | Status carried over. |
| LISTED | Load (RWB-E1-010) | File loaded | LOADED | Outside this story. |
| LISTED | Retirement (RWB-E1-012) | Decision RETIRE | RETIRED | Outside this story. |
| LOADED | Sign-off (RWB-E1-010) | Counts match | SIGNED_OFF | Outside this story. |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | A team has no row | Refuse whole; no row written. | MSG-P1-016 |
| X2 | A row has no decision or reason | Refuse whole; row and field named. | MSG-GEN-001 |
| X3 | A value is outside its list | Refuse whole; row and allowed values. | MSG-P1-007 |
| X4 | A LOAD row has no target product | Refuse whole; row named. | MSG-GEN-001 |
| X5 | A tracker code appears twice | Refuse whole; row and code. | MSG-P1-017 |
| X6 | Same file again | No write; reported as already done. | MSG-P1-011 |
| X7 | Caller without Reference data R | 403; nothing returned. | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| New endpoint | `GET /api/recovery/v1/admin/trackers` (API-P1-004), query `team`, `decision`, `status`; response `Tracker[]`. |
| Contract delta | The API schema types `Tracker.inventoryVersion` as `integer`; the story and table require a version string such as `TRK-2026.11`. The contract must change to `string` (max 20). No other delta. |
| Backward compatibility | New endpoint; no existing consumer. |
| Authorization | Reference data R, scope applied. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 503 MSG-GEN-006. |
| Versioning | Additive endpoint; update API Specification v2 before implementation (RWB-TE-003). |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | Story §15 states no screen; the inventory is read through the endpoint. | Existing frontend tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-RDF-005; SPEC-RWB-E1-005-001..014 | New entity, repository, handler, service and controller method. | Positive, negative, boundary and error-path tests: each required field; each list; duplicate code; missing team; LOAD without product; status carry-over; repeat file; filters; 403. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `TrackerInventory` | Entity | Maps `tracker_inventory`. |
| `TrackerInventoryRepository` | Repository | Reads by team, decision and status; writes a version with carried-over status. |
| `TrackerInventoryHandler` | Published interface implementation | `ReferenceTableHandler` for `tracker_inventory`: row checks, team coverage, apply. |
| `TrackerService` | Service | Lists trackers with filters. |
| `RecoveryDataEngineController` | Controller | `GET /admin/trackers`. |

### Data and migration

- Migration `V1_005__tracker_inventory.sql` creates `tracker_inventory` with `tracker_code varchar(20)`, `inventory_version varchar(20)`, `team_code varchar(20)`, `tracker_name varchar(120)`, `location_type varchar(12)` check, `location_ref varchar(400)`, `owner_user_id uuid`, `field_list jsonb`, `update_cycle varchar(10)` check, `target_product varchar(25)` references `data_product`, `decision varchar(8)` check, `decision_reason varchar(400)`, `status varchar(12)` check, `valid_from date`, standard columns; unique `(tracker_code, inventory_version)`; index `(team_code, status)`.
- `target_product` uses the `data_product.product_code` width (`varchar(25)`).
- No delete: the handler writes the rows of the file and leaves earlier versions readable. A tracker absent from a new version is not changed by this story (CLAR-004).

### Rules

1. Required fields: tracker code, team, name, location type, field list, update cycle, decision and reason.
2. List values: `location_type`, `update_cycle`, `decision`; `team_code` must be in LOV-TEAM and in `tracker.inventory.teams`.
3. Tracker code unique within the file.
4. LOAD requires a target data product; RETIRE and KEEP must not carry one.
5. Team coverage: at least one row for each of the six parameter teams; a team with no tracker uses one row with `location_type = NONE`.
6. Status: new LOAD/RETIRE → LISTED; new KEEP → KEPT; existing tracker → previous status.
7. The whole file is refused on any row error; no partial version.

### Transaction and events

- `validate` writes nothing; `apply` writes all rows in one transaction.
- The reference load version is the record; no event is published.
- The file content hash is the idempotency key.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-REFADM | Reference data C — load | All |
| RW-DATASTEW | Reference data R/U — prepare, confirm, list | All |
| RW-COE | Reference data R — list | All |
| RW-TEAMMGR | Reference data R — supply rows, list | Team |
| Partner users | None | 403 MSG-P4-002 |

Separation of duty: the RW-REFADM who loads cannot confirm as owner.

### Observability and operations

- `ReferenceLoad` response: id, table, valid-from, status, rows.
- `GET /admin/trackers` returns the inventory with status and version.
- No job, metric or alert; the load is a reference-data change.

### Performance

- The file is small (23 rows in the AC); validation is in memory; the apply is a single batch.
- The read endpoint filters by indexed `(team_code, status)`; no unbounded scan.

### Feature flag and rollback

- `rwb.p1.tracker-inventory`. Off: handler and endpoint unavailable.
- Rollback: revert to the previous approved inventory version through the reference-data rollback path; no schema change.

### No UI change

No screen. SCR-40 Reference data arrives in E8; the data steward and team managers read the endpoint.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-005-01 | AC1, BR1, BR3 | System | 23 rows across six teams | 23 rows for TRK-2026.11; LIT returns 6, including LIT-07 with 18 fields |
| TC-E1-005-02 | AC2, BR2, BR5 | System | Loaded version | Every tracker has a decision and reason; 14 LOAD name a product; 14+6 LISTED; 3 KEPT |
| TC-E1-005-03 | AC3, BR3, BR4 | System | No DEBT_SALE row | Refused whole; MSG-P1-016 |
| TC-E1-005-04 | AC4, BR2 | System | Row 7 no decision | Refused whole; MSG-GEN-001 |
| TC-E1-005-05 | AC5, BR4 | System | Row 9 decision MAYBE | Refused whole; MSG-P1-007 |
| TC-E1-005-06 | AC6, BR2 | System | Row 12 LOAD without product | Refused whole; MSG-GEN-001 |
| TC-E1-005-07 | AC7, BR4 | System | NPA-02 on rows 15 and 16 | Refused whole; MSG-P1-017 |
| TC-E1-005-08 | AC8, BR4 | System | Same file twice | No write; MSG-P1-011 |
| TC-E1-005-09 | X7 | Security | PT-AGENCY calls the endpoint | 403 MSG-P4-002 |
| TC-E1-005-10 | BR6 | Unit | Field list with personal tags | Tags stored; no values |

## Guardrails

- Team list is a parameter; decisions and owners are data.
- No personal data in logs, tests or prompts; the inventory lists field names, never values.
- No read of another module's tables; team codes come through P4.
- The Workbench does not open, copy or change any tracker in this story.

## Out of scope

- Loading trackers (RWB-E1-010), retiring copies (RWB-E1-012), the inventory screen (SCR-40, Epic 8).
- Mapping tracker fields into `legal_action` or other module tables (Epic 5).

## Traceability

| Requirement ID | Requirement (short) | Feature | Rules | Test cases |
|---|---|---|---|---|
| REQ-RDF-005 | Every team file listed with owner, fields, update cycle and a decision | FEAT-RDF-07 | CTL-08; CTL-11; Principle 1 | TC-E1-005-01..10 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | AC1; SPEC-001, 013 | Where does `inventory_version` come from? The flow names TRK-2026.11 but the request has no version field and the template omits the column. | The value stored on every row and the API response. | **ASSUMED**: the file name stem is the version (`TRK-2026.11.xlsx` → `TRK-2026.11`), matching FSD AC-P1-007-01. Confirm with the data steward before the first SIT load. | `RESOLVED` | SPEC-001, 013 |
| CLAR-002 | AC1; SPEC-009 | API schema types `inventoryVersion` as integer, but the story uses `TRK-2026.11`. | The response contract. | The story and table require a string; change the API schema to `string` (max 20). | `RESOLVED` | SPEC-009 |
| CLAR-003 | BR5; SPEC-007 | What happens to a tracker absent from a new version? | Whether rows are deleted or left. | No rule in the story; the handler writes the file rows and leaves earlier versions readable. No delete. | `RESOLVED` | SPEC-007 |
| CLAR-004 | AC1; SPEC-001 | Story §13 says `target_product varchar(4)`; `data_product.product_code` is `varchar(25)`. | Column width and FK compatibility. | Use `varchar(25)` to match the parent key. | `RESOLVED` | SPEC-001 |
| CLAR-005 | AC2; SPEC-007 | Are the 14 LOAD and 6 RETIRE trackers all LISTED, and the 3 KEEP all KEPT? | First status. | AC2 states exactly this; the counts follow the 23-row file. | `RESOLVED` | SPEC-007 |

`CLARIFICATION_STATUS: RESOLVED` — all 5 items are answered from the story, FSD or API contract.
CLAR-001 is an explicit assumption to confirm before SIT; it does not change the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New versioned tracker inventory and one read endpoint; no UI; contract delta is the inventoryVersion type.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new inventory table, handler and GET /admin/trackers]
REQUIREMENT_COVERAGE_SUMMARY: All 6 business rules, 8 acceptance criteria and 7 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 6] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

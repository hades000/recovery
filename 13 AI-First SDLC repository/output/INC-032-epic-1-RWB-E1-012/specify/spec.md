# Technical Specification — RWB-E1-012 Retire local copies

| Field | Value |
|---|---|
| Story | RWB-E1-012 — Retire local copies |
| Epic / module | E1 / P1 Recovery data engine |
| RUN_ID | `INC-032-epic-1-RWB-E1-012` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-RDF-006); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 012 Retire local copies v1.md` |
| Upstream IDs | REQ-RDF-006; FEAT-RDF-09; US-RWB-E1-012; R-UNI-40; CTL-09; ADR-007 |
| Status | `SUCCESS` |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. The team manager retires through the endpoint; the Tribe lead reads the report; story §15. |
| Logic In Scope | `YES` — team scope, retirable check, parallel period, unfed fields, status change, repeat, report. |
| API In Scope | `YES` — new `POST /admin/trackers/{trackerId}/retire` (API-P1-007) and `GET /admin/trackers/retirement-report` (API-P1-008); `GET /admin/trackers` response is extended. |
| API Impact Type | `NEW_API_REQUIRED` — new endpoints; the Tracker response extension is additive and already in the schema. |
| Impacted Existing Nodes | `tracker_inventory` (RWB-E1-005, RWB-E1-010); `tracker_row` (read); tracker file store (RWB-E1-010); working-day calendar (RWB-E1-043). |
| New Nodes Required | `YES` — `TrackerRetirementService`, `TrackerRetirementReportService`, `TrackerLoadController` methods, `WorkingDayCalendar` consumer. |
| Inherited Existing Behavior | Inventory and field list (RWB-E1-005); load/sign-off and stored file (RWB-E1-010); team scope and Entra sign-in (RWB-E1-022); working-day calendar (RWB-E1-043). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | A tracker is retired only with its team manager's confirmation and a read-only archive location. | SPEC-RWB-E1-012-001, 002, 010 | DIRECT | Queue and allocation A, team scope; `archiveRef` required. | COVERED |
| BR2 | A LOAD tracker is retired only after sign-off and the parallel period. | SPEC-RWB-E1-012-003, 004 | DIRECT | `tracker.retire.parallel.days`; working-day calendar. | COVERED |
| BR3 | A RETIRE tracker retires from LISTED; a KEEP tracker is never retired. | SPEC-RWB-E1-012-003, 016 | DIRECT | Decision/status matrix. | COVERED |
| BR4 | The retirement logs every non-personal field with no data product mapping. | SPEC-RWB-E1-012-005 | DIRECT | `field_list[].mappedTo`; `unfed_fields`. | COVERED |
| BR5 | The stored tracker file is kept unchanged as the archive copy. | SPEC-RWB-E1-012-011 | DIRECT | No update or delete of the write-once file. | COVERED |
| BR6 | A repeated retirement has no further effect. | SPEC-RWB-E1-012-007 | DIRECT | Return the existing retirement; no field change. | COVERED |
| BR7 | Only the team manager of the tracker's team may confirm. | SPEC-RWB-E1-012-002 | DIRECT | Team scope; 403 MSG-P4-002. | COVERED |
| AC1 | LIT-07 signed off 2026-11-20 is retired 2026-11-25 with the archive location; stored file unchanged. | SPEC-RWB-E1-012-001, 004, 006, 011 | DIRECT | Two working days: Mon 23, Tue 24. | COVERED |
| AC2 | A retired LIT-07 shows archive location, date, confirming user, stored file reference and 3 unfed fields. | SPEC-RWB-E1-012-005, 008 | DIRECT | `GET /admin/trackers?status=RETIRED`. | COVERED |
| AC3 | Six teams retired all LOAD/RETIRE trackers; the report shows 6 rows, outstanding 0. | SPEC-RWB-E1-012-008, 009, 014 | DIRECT | Tribe lead files the report with the release checklist. | COVERED |
| AC4 | NPA-02 LOAD/LOADED cannot be retired. | SPEC-RWB-E1-012-003 | DIRECT | MSG-P1-013. | COVERED |
| AC5 | Retirement on 2026-11-23 is refused; first allowed 2026-11-25. | SPEC-RWB-E1-012-004 | DIRECT | MSG-P1-014; stays SIGNED_OFF. | COVERED |
| AC6 | No archive location returns 400. | SPEC-RWB-E1-012-010 | DIRECT | MSG-GEN-001. | COVERED |
| AC7 | An NPA manager retiring LIT-07 gets 403. | SPEC-RWB-E1-012-002 | DIRECT | MSG-P4-002; stays SIGNED_OFF. | COVERED |
| AC8 | A repeated retirement returns 200 with the existing date; no change. | SPEC-RWB-E1-012-007 | DIRECT | Idempotent. | COVERED |
| AC9 | Two retirements from version 4: one succeeds, one 409. | SPEC-RWB-E1-012-006 | DIRECT | Optimistic lock; MSG-GEN-004. | COVERED |
| AC10 | NPA has 3 of 4 retired; the report shows outstanding 1 with NPA-02/LOADED. | SPEC-RWB-E1-012-009 | DIRECT | Outstanding list. | COVERED |
| X1 | Tracker LOADED/not signed off or KEEP. | SPEC-RWB-E1-012-003 | DIRECT | MSG-P1-013. | COVERED |
| X2 | Fewer than two working days. | SPEC-RWB-E1-012-004 | DIRECT | MSG-P1-014. | COVERED |
| X3 | No archive location. | SPEC-RWB-E1-012-010 | DIRECT | 400 MSG-GEN-001. | COVERED |
| X4 | Caller from another team. | SPEC-RWB-E1-012-002 | DIRECT | 403 MSG-P4-002. | COVERED |
| X5 | Already retired. | SPEC-RWB-E1-012-007 | DIRECT | 200 existing; no change. | COVERED |
| X6 | Two retire calls at once. | SPEC-RWB-E1-012-006 | DIRECT | 409 MSG-GEN-004. | COVERED |
| X7 | A team still has an unretired tracker. | SPEC-RWB-E1-012-009 | DIRECT | Outstanding list. | COVERED |
| X8 | Role without Queue and allocation A. | SPEC-RWB-E1-012-012 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **team manager (RW-TEAMMGR)**, I want **to confirm in the Workbench that my team's Excel or SharePoint tracker is replaced by the case list, with the location of the read-only archive recorded**, so that **there is one list and no shadow copy**.

The Workbench does not change or move the team's tracker. The team makes it read-only; the Workbench records the archive location, the confirming user and the fields no data product carries. The Tribe lead uses the report for the release checklist.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | RW-TEAMMGR calls `POST /admin/trackers/{trackerId}/retire`; RW-TRIBE/RW-DATASTEW calls `GET /admin/trackers/retirement-report`. |
| Preconditions | RWB-E1-010 done (loaded and signed-off trackers; stored file); RWB-E1-005 done (`tracker.inventory.teams`, `field_list.mappedTo`); RWB-E1-022 done (team manager sign-in); `tracker.retire.parallel.days = 2`; working-day calendar. |
| Input | Tracker ID, archive location, version read. |
| Output | Tracker status RETIRED with archive reference, date, confirming user and unfed fields; per-team retirement report. |
| Feature flag | `rwb.p1.tracker-retire`. Off: retire and report unavailable. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `tracker_inventory` | `decision` | RWB-E1-005 | Read | LOAD or RETIRE; KEEP never retires. |
| `tracker_inventory` | `status` | RWB-E1-010 | Read | LOAD: SIGNED_OFF; RETIRE: LISTED. |
| `tracker_inventory` | `signed_off_at` | RWB-E1-010 | Read | Parallel period start for LOAD. |
| `tracker_inventory` | `archive_ref` | Retirement request | Team manager | Required; up to 400 characters; read-only location. |
| `tracker_inventory` | `retired_at` | System | System | Set once; repeat keeps the first value. |
| `tracker_inventory` | `retire_confirmed_by` | Session | System | Team manager of the tracker's team. |
| `tracker_inventory` | `unfed_fields` | Field list | System | Non-personal fields with no `mappedTo`. |
| `tracker_inventory` | `version` | Row | System | Optimistic lock; 409 on mismatch. |
| `tracker_inventory` | `source_file_ref` | RWB-E1-010 | Read | Stored file reference; never changed. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| SIGNED_OFF | Retirement confirmed | LOAD; parallel period passed; archive location; caller in team | RETIRED | `retired_at`, `retire_confirmed_by`, `archive_ref`, `unfed_fields`. |
| LISTED | Retirement confirmed | RETIRE; archive location; caller in team | RETIRED | Same fields; no load required. |
| LOADED | Retirement attempt | Not signed off | LOADED | MSG-P1-013. |
| KEPT | Retirement attempt | KEEP | KEPT | MSG-P1-013. |
| RETIRED | Retirement repeated | Same tracker | RETIRED | 200 existing; no field change. |
| SIGNED_OFF | Retirement before the period | Fewer than 2 working days | SIGNED_OFF | MSG-P1-014 with first allowed date. |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Tracker LOADED/not signed off, or KEEP | Refuse retirement. | MSG-P1-013 |
| X2 | Fewer than two working days | Refuse with the first allowed date. | MSG-P1-014 |
| X3 | No archive location | 400. | MSG-GEN-001 |
| X4 | Caller from another team | 403. | MSG-P4-002 |
| X5 | Already retired | 200 with the existing retirement; no change. | None |
| X6 | Two retire calls at once | Second refused. | MSG-GEN-004 |
| X7 | A team still has an unretired tracker | Report lists it as outstanding. | None |
| X8 | Role without Queue and allocation A | 403. | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| New endpoints | `POST /admin/trackers/{trackerId}/retire` (API-P1-007); `GET /admin/trackers/retirement-report` (API-P1-008). |
| Contract delta | `GET /admin/trackers` adds `archiveRef`, `retiredAt`, `retireConfirmedBy`, `sourceFileRef`, `unfedFields`; these are already in the `Tracker` schema. The retire request is `TrackerRetirement` (`archiveRef`, `version`); the report is `TrackerRetirementReport[]`. No breaking change. |
| Backward compatibility | Additive; existing `GET /admin/trackers` consumers see new fields. |
| Authorization | Queue and allocation A, scope Team for retire; Reference data R for the report. |
| Error behaviour | 400 MSG-GEN-001; 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-P1-013/014/GEN-004; 503 MSG-GEN-006. |
| Versioning | Additive; update API Specification v2 before implementation (RWB-TE-003). |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | Story §15 states no screen; the endpoints are used directly. | Existing frontend tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-RDF-006; SPEC-RWB-E1-012-001..016 | New retirement service, report service and controller methods. | Positive, negative, boundary and error-path tests: LOAD/RETIRE/KEEP; signed-off/loaded; parallel boundary across a weekend; archive required; team scope; repeat; optimistic lock; outstanding list; 403. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `TrackerRetirementService` | Service | Team scope, retirable check, parallel period, unfed fields, status change with optimistic lock. |
| `TrackerRetirementReportService` | Service | Builds the per-team report from `tracker_inventory` and the team list. |
| `TrackerLoadController` | Controller (from RWB-E1-010) | Adds the retire and report endpoints. |
| `TrackerInventoryRepository` | Repository (from RWB-E1-005) | Reads and updates `tracker_inventory`. |
| `WorkingDayCalendar` | Service (reference data) | Adds working days to the sign-off date. |

### Data and migration

- Migration `V1_012__tracker_retirement.sql` adds `archive_ref varchar(400)`, `retired_at timestamptz`, `retire_confirmed_by uuid` and `unfed_fields jsonb` to `tracker_inventory`.
- `field_list` entries gain an optional `mappedTo` (entity.field) used for the unfed list. RWB-E1-005 supplies the field list; this story reads it.
- No new table; the stored file in the write-once container is not changed.

### Rules

1. Retire requires Queue and allocation A with team scope; the caller must be in the tracker's team.
2. LOAD tracker: status SIGNED_OFF and at least `tracker.retire.parallel.days` working days since `signed_off_at`.
3. RETIRE tracker: status LISTED; no load required.
4. KEEP tracker: never retirable.
5. Archive location required; 400 MSG-GEN-001 if missing.
6. Unfed fields = non-personal fields in `field_list` with no `mappedTo`.
7. Set status RETIRED, `retired_at`, `retire_confirmed_by`, `archive_ref`, `unfed_fields` with the optimistic lock.
8. A repeat retirement returns 200 with the existing values; no field change.
9. The report includes LOAD and RETIRE trackers per team, the retired count, the outstanding list and the confirmations.

### Transaction and events

- The retirement update is one transaction with the optimistic lock.
- No event is published; the tracker row is the record.
- The report is read-only; filing with the release checklist is a manual Tribe lead action.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-TEAMMGR | Queue and allocation A — confirm retirement | Team |
| RW-DATASTEW | Reference data R — read trackers and report | All |
| RW-COE, RW-TEAMMGR, RW-AUDIT | Reference data R — read | All/Team |
| RW-TRIBE | Reference data R — read the report | All |
| Any other role | None | 403 MSG-P4-002 |

No personal data in the report; archive locations in tests use the example domain.

### Observability and operations

- Tracker row: status, archive reference, retired date, confirming user, unfed fields.
- Report: per team, trackers, retired, outstanding, confirmations.
- No job or alert; the report is the release-checklist evidence.

### Performance

- Single-row update by tracker ID; the report groups `tracker_inventory` by team.
- The working-day calculation uses the reference-data calendar; no per-row service call.

### Feature flag and rollback

- `rwb.p1.tracker-retire`. Off: retire and report unavailable.
- Rollback: turn the flag off; a RETIRED row stays readable; no schema rollback.

### No UI change

No screen. The team manager uses the endpoint; the Tribe lead reads the report for the 26 November 2026 business sign-off. A Power BI page is optional and not in this story.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-012-01 | AC1, BR1, BR2, BR5 | System | LIT-07 signed off 2026-11-20; retire 2026-11-25 | RETIRED with date, user, archive; stored file unchanged |
| TC-E1-012-02 | AC2, BR4 | System | Retired LIT-07 with 3 unmapped fields | Archive, date, user, file ref and 3 unfed fields |
| TC-E1-012-03 | AC3 | System | Six teams fully retired | 6 rows; outstanding 0 |
| TC-E1-012-04 | AC4, BR3 | System | NPA-02 LOAD/LOADED | Refused; MSG-P1-013 |
| TC-E1-012-05 | AC5, BR2 | System | Retire 2026-11-23 | Refused; MSG-P1-014; first allowed 2026-11-25 |
| TC-E1-012-06 | AC6 | System | No archive location | 400 MSG-GEN-001 |
| TC-E1-012-07 | AC7, BR7 | System | NPA manager on LIT-07 | 403 MSG-P4-002; stays SIGNED_OFF |
| TC-E1-012-08 | AC8, BR6 | System | Second retirement | 200; retired_at unchanged |
| TC-E1-012-09 | AC9 | System | Two sessions at version 4 | One succeeds; one 409 MSG-GEN-004 |
| TC-E1-012-10 | AC10 | System | NPA 3 of 4 retired | Outstanding 1 with NPA-02/LOADED |
| TC-E1-012-11 | X8 | Security | RW-DATASTEW retires | 403 MSG-P4-002 |
| TC-E1-012-12 | BR2 | Unit | Parallel boundary across a weekend | Correct first allowed date |

## Guardrails

- The parallel period and the team list are parameters.
- No personal data in logs, tests or prompts; archive locations use the example domain.
- No read of another module's tables; team names come through P4.
- The Workbench does not change, move or delete the team's tracker; the team makes it read-only and the Workbench records the location.

## Out of scope

- Setting the tracker read-only in SharePoint (the team does it).
- Loading the tracker content (RWB-E1-010); feeding unfed fields into a data product (owning module).
- A screen for the inventory and retirement (SCR-40, Epic 8).

## Traceability

| Requirement ID | Requirement (short) | Feature | Rules | Test cases |
|---|---|---|---|---|
| REQ-RDF-006 | Local copy retired with the owner's confirmation and a read-only archive kept | FEAT-RDF-09 | R-UNI-40; CTL-09 | TC-E1-012-01..12 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | Header; SPEC-001, 005 | The header Depends on omits RWB-E1-005, but the story needs `tracker.inventory.teams` and `field_list.mappedTo`. | Dependency order and field list shape. | Add RWB-E1-005 as a dependency; the field list carries `mappedTo`. | `RESOLVED` | SPEC-001, 005 |
| CLAR-002 | AC3; SPEC-014 | AC3 says the system files the report with the release checklist; step 9 gives that to the Tribe lead and the endpoint is read-only. | Whether the code writes to the release checklist. | The system produces the report; the Tribe lead files it manually. No code writes the checklist. | `RESOLVED` | SPEC-014 |
| CLAR-003 | BR2, AC1, AC5; SPEC-004 | How are two working days counted? | The first allowed retirement date. | Sign-off Friday 2026-11-20; Mon 23 and Tue 24 are the two working days; retirement allowed from Wed 25. | `RESOLVED` | SPEC-004 |
| CLAR-004 | AC1; SPEC-006 | AC1 says "retires the tracker status"; is the target RETIRED? | Status value. | Yes; `status = RETIRED` with `retired_at`. | `RESOLVED` | SPEC-006 |
| CLAR-005 | BR4; SPEC-005 | Which fields are "unfed"? | The `unfed_fields` list. | Non-personal fields in `field_list` with no `mappedTo`. | `RESOLVED` | SPEC-005 |

`CLARIFICATION_STATUS: RESOLVED` — all 5 items are answered from the story or its ACs. No open item
changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New tracker retirement and per-team report; two new endpoints; no UI.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new retire and report endpoints with a tracker status change]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 10 acceptance criteria and 8 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

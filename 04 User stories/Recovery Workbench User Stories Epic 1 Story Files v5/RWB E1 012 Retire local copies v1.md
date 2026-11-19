# RWB-E1-012 Retire local copies

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-012 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-RDF-09 Retire a local tracker copy |
| Requirement IDs | REQ-RDF-006 |
| BRD section | Business Requirements Epic 1, section 3.1; Business Requirements Program, section 5.1 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-022, RWB-E1-010 |
| Status | Ready for build |

## 1. Story

As a **team manager (RW-TEAMMGR)**, I want **to confirm in the Workbench that my team's Excel or SharePoint tracker is replaced by the case list, with the location of the read-only archive recorded**, so that **there is one list and no shadow copy**.

## 2. Business rationale

A tracker that stays in use after its data is loaded becomes a second version of the truth, and the two drift apart within days. This story lets the team manager retire each tracker after its load is signed off and the team has worked from the case list for two working days, records where the read-only archive is, logs the tracker fields that no data product carries, and gives the Tribe lead one report of the six teams for the business sign-off before the release. It completes REQ-RDF-006 (local copy retired with the owner's confirmation and a read-only archive kept).

## 3. Preconditions

- RWB-E1-010 is done: trackers with a LOAD decision are loaded and signed off, and the stored file is in the write-once tracker file store.
- RWB-E1-022 is done: team managers sign in with Entra ID and hold RW-TEAMMGR with their team scope.
- The team has made the tracker read-only in its current location, or moved it to a read-only archive location, before it confirms the retirement.
- Parameters are loaded: `tracker.retire.parallel.days` 2 working days, `tracker.inventory.teams` (from RWB-E1-005).
- The working day calendar is loaded in the reference data service.

## 4. Flow

1. Team manager: works from the case list for at least two working days after the tracker's load is signed off.
2. Team manager: sets the tracker read-only in SharePoint or moves it to the archive location.
3. Team manager: calls `POST /admin/trackers/{trackerId}/retire` with the archive location.
4. System: checks the caller belongs to the tracker's team and holds Queue and allocation A.
5. System: checks the tracker can be retired: decision LOAD with status SIGNED_OFF and at least two working days since sign-off, or decision RETIRE with status LISTED.
6. System: lists the fields of the tracker's field list that are not personal and have no data product field mapped to them.
7. System: sets status RETIRED with the archive location, the time, the confirming user and the list of fields no feed carries, using the optimistic lock version.
8. Data steward or team manager: calls `GET /admin/trackers?status=RETIRED` and reads the archive location, the date and the stored file reference.
9. Tribe lead (RW-TRIBE): on 26 November 2026, calls `GET /admin/trackers/retirement-report` and files the report with the release checklist.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The tracker is LOADED and not signed off, or its decision is KEEP | Retirement refused | MSG-P1-013 | AC4 |
| X2 | Fewer than two working days since sign-off | Retirement refused with the first allowed date | MSG-P1-014 | AC5 |
| X3 | No archive location in the request | 400 | MSG-GEN-001 | AC6 |
| X4 | The caller is a team manager of another team | 403 | MSG-P4-002 | AC7 |
| X5 | The tracker is already RETIRED | 200 with the existing retirement; nothing changes | None | AC8 |
| X6 | Two retire calls on one tracker at the same time | The second is refused | MSG-GEN-004 | AC9 |
| X7 | A team still has a tracker that is not retired on the report date | The report lists the team as outstanding with the tracker codes | None | AC10 |
| X8 | A role without Queue and allocation A calls the retirement | 403 | MSG-P4-002 | TC-E1-012-11 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the signed-off loads of RWB-E1-010 and the team manager sign-in of RWB-E1-022 |
| Negotiable | The parallel period is a parameter; the archive location is the team's choice |
| Valuable | Ends the shadow copies and gives the release one report for the business sign-off |
| Estimable | One action endpoint, one report endpoint, two status checks |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion below is one automated test on synthetic trackers |

## 7. Acceptance criteria

```gherkin
Feature: Retire local copies

  Background:
    Given the parameter tracker.retire.parallel.days = 2
    Given tracker "LIT-07 Litigation case tracker" of team LIT has decision LOAD, status SIGNED_OFF and signed off on Friday 2026-11-20

  Scenario: AC1 Team confirmation
    Given the LIT team has worked from the case list on Monday 2026-11-23 and Tuesday 2026-11-24
    When the LIT team manager calls POST /admin/trackers/{trackerId}/retire on 2026-11-25 with archive location "https://sharepoint.example/sites/lit/archive/LIT-07"
    Then the system retires the tracker status with retired_at 2026-11-25, the team manager's user ID and the archive location
    Then the system keeps the stored tracker file in the write-once store unchanged

  Scenario: AC2 Archive location
    Given LIT-07 was retired on 2026-11-25
    When the data steward calls GET /admin/trackers with status RETIRED
    Then the row for LIT-07 shows archive location "https://sharepoint.example/sites/lit/archive/LIT-07", retired on 2026-11-25, the confirming user and the stored file reference
    Then it lists the 3 fields "Hearing note", "Firm contact" and "Court room" as fields no feed carries

  Scenario: AC3 Business sign-off
    Given the six teams TDR, DIL, LIT, NPA, DEBT_SALE and WRITE_OFF have retired all their LOAD and RETIRE trackers by 2026-11-26
    When the Tribe lead calls GET /admin/trackers/retirement-report on 2026-11-26
    Then the report holds six team rows, each with the number of trackers, the number retired, the team manager who confirmed each retirement and the date
    Then every team row shows outstanding 0
    Then the system files the report with the release checklist of 30 November 2026

  Scenario: AC4 Tracker not signed off
    Given tracker "NPA-02 Asset holding list" has decision LOAD and status LOADED
    When the NPA team manager calls the retirement for NPA-02
    Then the system refuses the retirement with MSG-P1-013 "NPA-02 cannot be retired: its decision is LOAD and its status is LOADED."

  Scenario: AC5 Parallel period not yet complete
    Given LIT-07 was signed off on 2026-11-20
    When the LIT team manager calls the retirement on Monday 2026-11-23
    Then the system refuses the retirement with MSG-P1-014 "LIT-07 can be retired from 2026-11-25, after 2 working days of use of the case list."
    Then the status stays SIGNED_OFF

  Scenario: AC6 No archive location
    Given LIT-07 can be retired
    When the LIT team manager calls the retirement with no archive location
    Then the response is 400 with MSG-GEN-001 "Enter archive location."

  Scenario: AC7 Team manager of another team
    Given LIT-07 can be retired
    When the NPA team manager calls the retirement for LIT-07
    Then the response is 403 with MSG-P4-002
    Then the status stays SIGNED_OFF

  Scenario: AC8 Retirement repeated
    Given LIT-07 was retired on 2026-11-25
    When the LIT team manager calls the retirement again on 2026-11-26
    Then the response is 200 with retired_at 2026-11-25 and no field changes

  Scenario: AC9 Two retirements at the same time
    Given two sessions of the LIT team manager read LIT-07 at version 4
    When both call the retirement
    Then one succeeds and the other is refused with 409 and MSG-GEN-004

  Scenario: AC10 A team with an outstanding tracker
    Given team NPA has retired 3 of its 4 LOAD and RETIRE trackers and NPA-02 is still LOADED on 2026-11-26
    When the Tribe lead calls GET /admin/trackers/retirement-report on 2026-11-26
    Then the NPA row shows outstanding 1 with tracker code "NPA-02" and status LOADED
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A tracker is retired only with its team manager's confirmation and a read-only archive location | REQ-RDF-006 |
| BR2 | A LOAD tracker is retired only after its load is signed off and the team has used the case list for the parallel period | Parameter tracker.retire.parallel.days, 2 working days |
| BR3 | A RETIRE tracker is retired from LISTED with no load; a KEEP tracker is never retired | RWB-E1-005 BR2 |
| BR4 | The retirement logs every non-personal field of the tracker that no data product field carries | FEAT-RDF-09 |
| BR5 | The stored tracker file is kept unchanged as the Workbench archive copy | ADR-007 storage pattern; RWB-E1-010 BR7 |
| BR6 | A repeated retirement has no further effect | R-UNI-40 |
| BR7 | Only the team manager of the tracker's team may confirm | Scope Team (roles key); CTL-09 |

## 9. State transitions

None. This story does not change a case status. It changes the tracker status.

| From | Event | Condition | To |
|---|---|---|---|
| SIGNED_OFF | Retirement confirmed | Decision LOAD; parallel period passed; archive location given; caller in the team | RETIRED |
| LISTED | Retirement confirmed | Decision RETIRE; archive location given; caller in the team | RETIRED |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TEAMMGR, team manager of the tracker's team | Confirms the retirement (Queue and allocation A, scope Team) |
| RW-DATASTEW, data steward and data product owner | Reads the trackers and the retirement report (Reference data R) |
| RW-COE, RW-TEAMMGR, RW-AUDIT | Read the trackers and the report (Reference data R) |
| RW-TRIBE, Tribe lead and squad members | Read the report for the release checklist (Reference data R) |

The confirmation is not an approval within the delegation of authority; no approval level applies.

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-086 | tracker_inventory | team_code | Read |
| DF-OPS-094 | tracker_inventory | decision | Read |
| DF-OPS-096 | tracker_inventory | status | Read |
| DF-OPS-103 | tracker_inventory | signed_off_at | Read |
| DF-OPS-091 | tracker_inventory | field_list | Read |
| DF-OPS-104 | tracker_inventory | source_file_ref | Read |
| DF-OPS-096 | tracker_inventory | status | Write |
| DF-OPS-105 | tracker_inventory | archive_ref | Write |
| DF-OPS-106 | tracker_inventory | retired_at | Write |
| DF-OPS-107 | tracker_inventory | retire_confirmed_by | Write |
| DF-OPS-108 | tracker_inventory | unfed_fields | Write |
| DF-REF-028 | lov_value | lov_code | Read through the P4 published interface (team names on the report) |
| DF-REF-030 | lov_value | label_en | Read through the P4 published interface (team names on the report) |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /admin/trackers/{trackerId}/retire** (new endpoint, recorded in the additions file)

| Item | Value |
|---|---|
| Request | `TrackerRetirement`: archiveRef (string, up to 400 characters, required), version (integer, the version read) |
| Response 200 | `Tracker` with status RETIRED, archiveRef, retiredAt, retireConfirmedBy, unfedFields |
| 400 | archiveRef missing (MSG-GEN-001) |
| 403 | Role lacks Queue and allocation A, or the caller is not in the tracker's team (MSG-P4-002) |
| 404 | No tracker with that id (MSG-P4-003) |
| 409 | Not retirable (MSG-P1-013); parallel period not passed (MSG-P1-014); version changed (MSG-GEN-004) |
| 401, 503 | MSG-P4-001; database unavailable |
| Authorization | Queue and allocation A, scope Team |
| Idempotency | A call on a RETIRED tracker returns 200 with the existing retirement |

**GET /admin/trackers/retirement-report** (new endpoint, recorded in the additions file)

| Item | Value |
|---|---|
| Request | Query `asOf` (date, default today) |
| Response 200 | `TrackerRetirementReport[]`: team, trackers (LOAD and RETIRE), retired, outstanding (count and list of tracker code and status), confirmations (tracker code, user ID, date) |
| 401, 403, 503 | MSG-P4-001; MSG-P4-002; database unavailable |
| Authorization | Reference data R |
| Idempotency | Read only |

**GET /admin/trackers** (from RWB-E1-005) adds archiveRef, retiredAt, retireConfirmedBy, sourceFileRef and unfedFields to `Tracker`.

## 13. Solution plan

**Package.** Folder `recovery/dataengine/tracker`, Java package `recovery.dataengine.tracker`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TrackerRetirementService | Service | Team scope, retirable check, parallel period by working days, unfed field list, status change with optimistic lock |
| TrackerRetirementReportService | Service | Builds the per-team report from tracker_inventory and the team list parameter |
| TrackerLoadController | Controller (from RWB-E1-010) | Adds the retire and report endpoints |
| TrackerInventoryRepository | Repository (from RWB-E1-005) | Reads and updates tracker_inventory |
| WorkingDayCalendar | Service (reference data service) | Adds working days to the sign-off date |

**Database.** Migration `V1_012__tracker_retirement.sql` adds archive_ref varchar(400), retired_at timestamptz, retire_confirmed_by uuid and unfed_fields jsonb to tracker_inventory. The field_list entries of RWB-E1-005 gain an optional `mappedTo` (entity.field) used for the unfed field list.

**Configuration and reference data.** Parameter `tracker.retire.parallel.days` from the parameter catalog, loaded by the center of excellence analyst. The working day calendar from the reference data service. The team list from `tracker.inventory.teams`.

**Build steps**

1. Write migration V1_012.
2. Write TrackerRetirementService with the retirable check for LOAD and RETIRE trackers; unit test each status and decision.
3. Add the parallel period check with the working day calendar; test the boundary on the second working day and across a weekend.
4. Add the unfed field list from the field list entries that are not personal and have no mappedTo.
5. Add the team scope check, the optimistic lock and the repeat handling.
6. Write TrackerRetirementReportService with the outstanding list.
7. Add both endpoints to TrackerLoadController with their capability checks and Problem mapping.

**Feature flag.** `rwb.p1.tracker-retire`.

**Done when.** The tests in section 16 pass, and the SIT retirement report shows the six teams.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-013 | Tracker not retirable | {tracker} cannot be retired: its decision is {decision} and its status is {status}. |
| MSG-P1-014 | Parallel period not passed | {tracker} can be retired from {date}, after {days} working days of use of the case list. |
| MSG-GEN-001 | Archive location missing | Enter {field}. |
| MSG-GEN-004 | Tracker changed by someone else | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | Role or team without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No screen in this story. The team manager confirms the retirement through the endpoint, and the Tribe lead reads the retirement report through the endpoint for the business sign-off on 26 November 2026. A screen for trackers is not planned; the report becomes a Power BI page if the Tribe asks for it.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-012-01 | AC1, BR1, BR2, BR5 | System | LIT-07 signed off on 2026-11-20; retirement on 2026-11-25 |
| TC-E1-012-02 | AC2, BR4 | System | Retired LIT-07 with 3 unmapped fields |
| TC-E1-012-03 | AC3 | System | Six teams with every LOAD and RETIRE tracker retired |
| TC-E1-012-04 | AC4, BR3 | System | NPA-02 in status LOADED |
| TC-E1-012-05 | AC5, BR2 | System | Retirement on 2026-11-23 |
| TC-E1-012-06 | AC6 | System | Request without archive location |
| TC-E1-012-07 | AC7, BR7 | System | NPA team manager on LIT-07 |
| TC-E1-012-08 | AC8, BR6 | System | Second retirement of LIT-07 |
| TC-E1-012-09 | AC9 | System | Two sessions at version 4 |
| TC-E1-012-10 | AC10 | System | NPA with NPA-02 still LOADED on 2026-11-26 |
| TC-E1-012-11 | Access | Access | RW-DATASTEW calls the retirement; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the parallel period and the team list are parameters.
- No personal data in logs, tests or prompts. Archive locations in tests use the example domain.
- No read of another module's tables. Team names come through the P4 published interface.
- The Workbench does not change, move or delete the team's tracker; the team makes it read-only, and the Workbench records the location.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-006 | Local copy retired with the owner's confirmation and a read-only archive kept | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-09 | All recovery processes | R-UNI-40; CTL-09 | TC-E1-012-01 to TC-E1-012-11 |

## 19. Out of scope

- Setting the tracker read-only in SharePoint, which the team does in SharePoint.
- Loading the tracker content (RWB-E1-010).
- Feeding the fields no feed carries into a data product (the owning module, in the epic that needs the field).
- A screen for the inventory and retirement (SCR-40 Reference data, Epic 8).


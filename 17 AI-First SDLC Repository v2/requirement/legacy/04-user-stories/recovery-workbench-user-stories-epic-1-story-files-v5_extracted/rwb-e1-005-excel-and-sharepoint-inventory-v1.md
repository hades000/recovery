<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 005 Excel and SharePoint inventory v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 005 Excel and SharePoint inventory v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-005 Excel and SharePoint inventory

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-005 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-RDF-07 Inventory the Excel and SharePoint trackers |
| Requirement IDs | REQ-RDF-005 |
| BRD section | Business Requirements Epic 1, section 3.1; Business Requirements Program, section 5.1 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-001, RWB-E1-043 |
| Status | Ready for build |

## 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **every recovery team's Excel files, SharePoint lists and local files listed with owner, fields, update cycle and a load, retire or keep decision**, so that **each file can be loaded into its data product and then retired**.

## 2. Business rationale

The TDR, deed in lieu, litigation, NPA, debt sale and write-off teams each keep their own trackers, and no list says which trackers exist, who owns them or what replaces them. This story holds the tracker inventory as a versioned table in the Workbench, refuses an inventory that leaves out a team or a decision, and gives every tracker the status that the load (RWB-E1-010) and the retirement (RWB-E1-012) move forward. It meets REQ-RDF-005 and is the first step of REQ-RDF-006.

## 3. Preconditions

- RWB-E1-001 is done: the data product catalog holds DP01 to DP14.
- RWB-E1-043 is done: the reference data service loads a table through the handler the owning module provides.
- Parameter `tracker.inventory.teams` holds the six team codes TDR, DIL, LIT, NPA, DEBT_SALE and WRITE_OFF (assumed codes; the values come from LOV-TEAM, loaded from the organization structure).
- The data steward has collected the inventory from the six team managers in the inventory template (one row per tracker).
- The reference data administrator (RW-REFADM) holds Reference data C; the data steward holds Reference data R and U.

## 4. Flow

1. Data steward: fills the inventory template, one row per tracker, with the decision and reason for each.
2. Reference data administrator: loads the file through `POST /admin/reference-loads` with table code `tracker_inventory`, version "TRK-2026.11" and valid from 2026-11-16.
3. System: `TrackerInventoryHandler.validate` checks every row: required fields, list values, a unique tracker code, a target data product for each LOAD decision, and at least one row for each of the six teams.
4. System: refuses the whole file and returns the row errors if any check fails.
5. Data steward: confirms the version as its owner through the reference data change process.
6. System: `TrackerInventoryHandler.apply` writes the rows in one transaction; a tracker already in the previous version keeps its status; a new tracker gets status LISTED, or KEPT for a KEEP decision.
7. Data steward or team manager: calls `GET /admin/trackers?team=LIT` and reads the trackers of the team with owner, fields, update cycle, decision and status.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The file has no row for one of the six teams | Load refused in full | MSG-P1-016 | AC3 |
| X2 | A row has no decision or no decision reason | Load refused in full; the row and field are named | MSG-GEN-001 | AC4 |
| X3 | A row has a value outside its list (for example decision "MAYBE") | Load refused in full | MSG-P1-007 | AC5 |
| X4 | A LOAD row has no target data product | Load refused in full | MSG-GEN-001 | AC6 |
| X5 | A tracker code appears twice in the file | Load refused in full | MSG-P1-017 | AC7 |
| X6 | The same file is loaded again | Nothing is written; the load is reported as already done | MSG-P1-011 | AC8 |
| X7 | A role without Reference data R lists the trackers | 403 | MSG-P4-002 | TC-E1-005-09 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the catalog of RWB-E1-001 and the reference load service; the load and retire stories build on it |
| Negotiable | The team list is a parameter and the decisions are data; the story fixes the checks |
| Valuable | One list of every tracker with a decision, owned by one person |
| Estimable | One table, one handler, one read endpoint |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion below is one automated test on synthetic inventory files |

## 7. Acceptance criteria

```gherkin
Feature: Excel and SharePoint inventory

  Background:
    Given the parameter tracker.inventory.teams holds TDR, DIL, LIT, NPA, DEBT_SALE and WRITE_OFF

  Scenario: AC1 Inventory covers six teams
    Given an inventory file "TRK-2026.11" with 23 rows: 5 for TDR, 3 for DIL, 6 for LIT, 4 for NPA, 2 for DEBT_SALE and 3 for WRITE_OFF
    Given each row has tracker code, tracker name, location type, location, owner user ID, field list, update cycle, decision and reason
    When the reference data administrator loads it and the data steward confirms it
    Then tracker_inventory holds 23 rows for version "TRK-2026.11"
    Then GET /admin/trackers with team "LIT" returns 6 trackers, among them "LIT-07 Litigation case tracker" on SharePoint, update cycle WEEKLY, with its owner and 18 fields

  Scenario: AC2 Decision per file
    Given the loaded version "TRK-2026.11"
    When the data steward calls GET /admin/trackers
    Then every one of the 23 trackers has a decision LOAD, RETIRE or KEEP and a reason
    Then the 14 LOAD trackers each name a target data product, for example "LIT-07" names DP07
    Then the 14 LOAD and 6 RETIRE trackers have status LISTED and the 3 KEEP trackers have status KEPT

  Scenario: AC3 A team is missing
    Given an inventory file with no row for team DEBT_SALE
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P1-016 "The inventory has no row for team DEBT_SALE. List its trackers, or add one row with location type NONE."
    Then the system writes no tracker_inventory row

  Scenario: AC4 A row without a decision
    Given an inventory file whose row 7 has no decision
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-GEN-001 "Enter decision." for row 7

  Scenario: AC5 A value outside its list
    Given an inventory file whose row 9 has decision "MAYBE"
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P1-007 "Row 9: decision must be one of LOAD, RETIRE, KEEP."

  Scenario: AC6 A load decision without a target data product
    Given an inventory file whose row 12 has decision LOAD and no target data product
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-GEN-001 "Enter target data product." for row 12

  Scenario: AC7 A tracker code twice
    Given an inventory file in which tracker code "NPA-02" is on rows 15 and 16
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P1-017 "Row 16: tracker code NPA-02 appears more than once."

  Scenario: AC8 The same file loaded again
    Given version "TRK-2026.11" is in force
    When the reference data administrator loads the same file again
    Then the system writes nothing
    Then the response carries MSG-P1-011 "The tracker inventory load for 2026-11-16 is already complete or running. It was not run again."
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every recovery team's Excel files, SharePoint lists and local files are listed with owner, fields and update cycle | REQ-RDF-005 |
| BR2 | Each tracker has a decision: LOAD into a named data product, RETIRE without a load, or KEEP as out of scope, with a reason | REQ-RDF-005 |
| BR3 | The inventory covers the six teams named in the parameter | Parameter tracker.inventory.teams (assumed codes, LOV-TEAM) |
| BR4 | The inventory is a versioned load; a file with an exception is refused in full | Principle 1; reference data change process, step 3; CTL-08 |
| BR5 | A tracker already in the previous version keeps its status in the new version | Reference data change process, step 6 |
| BR6 | Field names in the field list carry a personal data tag; personal fields are not loaded later | CTL-11; PDPA minimization (FEAT-RDF-15) |

## 9. State transitions

None. This story does not change a case status. It sets the first status of each tracker: LISTED for a LOAD or RETIRE decision and KEPT for a KEEP decision. RWB-E1-010 and RWB-E1-012 move LISTED to LOADED, SIGNED_OFF and RETIRED.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-REFADM, reference data administrator | Loads the inventory file (Reference data C) |
| RW-DATASTEW, data steward and data product owner | Prepares the file; confirms the version as owner; lists trackers (Reference data R) |
| RW-COE, center of excellence analyst | Lists trackers (Reference data R) |
| RW-TEAMMGR, team manager | Supplies the team's rows; lists trackers (Reference data R) |
| Partner users | Refused with MSG-P4-002 |

Separation of duty: the reference data administrator who loads the version cannot confirm it.

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-083 | tracker_inventory | id | Write (through the handler); read |
| DF-OPS-084 | tracker_inventory | tracker_code | Write (through the handler); read |
| DF-OPS-085 | tracker_inventory | inventory_version | Write (through the handler); read |
| DF-OPS-086 | tracker_inventory | team_code | Write (through the handler); read |
| DF-OPS-087 | tracker_inventory | tracker_name | Write (through the handler); read |
| DF-OPS-088 | tracker_inventory | location_type | Write (through the handler); read |
| DF-OPS-089 | tracker_inventory | location_ref | Write (through the handler); read |
| DF-OPS-090 | tracker_inventory | owner_user_id | Write (through the handler); read |
| DF-OPS-091 | tracker_inventory | field_list | Write (through the handler); read |
| DF-OPS-092 | tracker_inventory | update_cycle | Write (through the handler); read |
| DF-OPS-093 | tracker_inventory | target_product | Write (through the handler); read |
| DF-OPS-094 | tracker_inventory | decision | Write (through the handler); read |
| DF-OPS-095 | tracker_inventory | decision_reason | Write (through the handler); read |
| DF-OPS-096 | tracker_inventory | status | Write (through the handler); read |
| DF-OPS-097 | tracker_inventory | valid_from | Write (through the handler); read |
| DF-REF-071 | data_product | product_code | Read (target data product check) |
| DF-REF-028 | lov_value | lov_code | Read through the P4 published interface (LOV-TEAM check) |
| DF-REF-029 | lov_value | value_code | Read through the P4 published interface (LOV-TEAM check) |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Inventory load.** `POST /admin/reference-loads` (P4, Reference data C) with `file`, `table = tracker_inventory`, `validFrom`; response `ReferenceLoad` (id, table, validFrom, status, rows). P1 implements `ReferenceTableHandler` (signature in RWB-E1-001) as `TrackerInventoryHandler`. Errors: 422 with MSG-GEN-001, MSG-P1-007, MSG-P1-016 or MSG-P1-017 and the row number in `detail`; 409 when the file hash equals the version in force (MSG-P1-011). Idempotency: the file hash.

**GET /admin/trackers** (new endpoint, recorded in the additions file)

| Item | Value |
|---|---|
| Request | Query `team`, `decision`, `status` (all optional) |
| Response 200 | `Tracker[]`: id, trackerCode, team, name, locationType, locationRef, ownerUserId, fields (name and personal tag), updateCycle, targetProduct, decision, decisionReason, status, inventoryVersion |
| 401, 403, 503 | MSG-P4-001; MSG-P4-002; database unavailable |
| Authorization | Reference data R |
| Idempotency | Read only |

## 13. Solution plan

**Package.** Folder `recovery/dataengine/tracker`, Java package `recovery.dataengine.tracker`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TrackerInventory | Entity | Maps tracker_inventory |
| TrackerInventoryRepository | Repository | Reads by team, decision and status; writes a version with carried-over status |
| TrackerInventoryHandler | Published interface implementation | ReferenceTableHandler for `tracker_inventory`: row checks, team coverage, apply |
| TrackerService | Service | Lists trackers with filters |
| RecoveryDataEngineController | Controller | GET /admin/trackers |

**Database.** Migration `V1_005__tracker_inventory.sql` creates tracker_inventory: tracker_code varchar(20), inventory_version varchar(20), team_code varchar(20), tracker_name varchar(120), location_type varchar(12) check in ('EXCEL','SHAREPOINT','LOCAL_FILE','NONE'), location_ref varchar(400), owner_user_id uuid, field_list jsonb, update_cycle varchar(10) check in ('DAILY','WEEKLY','MONTHLY','AD_HOC'), target_product varchar(4) references data_product, decision varchar(8) check in ('LOAD','RETIRE','KEEP'), decision_reason varchar(400), status varchar(12) check in ('LISTED','LOADED','SIGNED_OFF','RETIRED','KEPT'), valid_from date, standard columns; unique (tracker_code, inventory_version); index on (team_code, status).

**Configuration and reference data.** Parameter `tracker.inventory.teams` from the parameter catalog, loaded by the center of excellence analyst. Inventory template columns: tracker_code, team_code, tracker_name, location_type, location_ref, owner_user_id, field_list, update_cycle, target_product, decision, decision_reason. The list values for location_type, update_cycle, decision and status are proposed as new lists LOV-TRACKER-LOCATION, LOV-UPDATE-CYCLE, LOV-TRACKER-DECISION and LOV-TRACKER-STATUS (recorded in the additions file).

**Build steps**

1. Write migration V1_005, TrackerInventory and its repository.
2. Write the row checks of TrackerInventoryHandler.validate: required fields, list values, unique code, target product for LOAD, LOV-TEAM membership; unit test each with a failing row.
3. Write the team coverage check against the parameter.
4. Write TrackerInventoryHandler.apply with the status carry-over from the previous version and the first status for new trackers.
5. Connect the handler to the reference data service and test a full load, a refused load and a repeated file.
6. Write TrackerService and the GET /admin/trackers method with the capability check.

**Feature flag.** `rwb.p1.tracker-inventory`.

**Done when.** The tests in section 16 pass, and the SIT inventory version holds at least one row for each of the six teams.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | Required field empty | Enter {field}. |
| MSG-P1-007 | Value outside its list | Row {row}: {field} must be one of {values}. |
| MSG-P1-016 | A team has no row | The inventory has no row for team {team}. List its trackers, or add one row with location type NONE. |
| MSG-P1-017 | A tracker code twice in the file | Row {row}: tracker code {value} appears more than once. |
| MSG-P1-011 | The same file loaded again | The {source} load for {date} is already complete or running. It was not run again. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No screen in this story. The inventory is loaded as a file through the reference data service, as other reference tables are before SCR-40 Reference data arrives in E8. The data steward and team managers read it through GET /admin/trackers.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-005-01 | AC1, BR1, BR3 | System | Inventory file of 23 synthetic rows across the six teams |
| TC-E1-005-02 | AC2, BR2, BR5 | System | Loaded version TRK-2026.11 |
| TC-E1-005-03 | AC3, BR3, BR4 | System | File with no DEBT_SALE row |
| TC-E1-005-04 | AC4, BR2 | System | Row 7 without a decision |
| TC-E1-005-05 | AC5, BR4 | System | Row 9 with decision MAYBE |
| TC-E1-005-06 | AC6, BR2 | System | Row 12 LOAD without a target product |
| TC-E1-005-07 | AC7, BR4 | System | NPA-02 on rows 15 and 16 |
| TC-E1-005-08 | AC8, BR4 | System | Same file loaded twice |
| TC-E1-005-09 | Access | Access | PT-AGENCY user calls GET /admin/trackers; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: the team list is a parameter; decisions and owners are data.
- No personal data in logs, tests or prompts. The inventory lists field names, never field values.
- No read of another module's tables. Team codes are checked through the P4 published interface.
- The Workbench does not open, copy or change any tracker in this story.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-005 | Every team file listed with owner, fields, update cycle and a decision | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-07 | All recovery processes | CTL-08; CTL-11; Principle 1 | TC-E1-005-01 to TC-E1-005-09 |

## 19. Out of scope

- Loading the trackers with a LOAD decision (RWB-E1-010).
- Retiring the local copies (RWB-E1-012).
- A screen for the inventory (SCR-40 Reference data, Epic 8).
- Mapping tracker fields into the proper data product tables, such as legal_action (S4, Epic 5).

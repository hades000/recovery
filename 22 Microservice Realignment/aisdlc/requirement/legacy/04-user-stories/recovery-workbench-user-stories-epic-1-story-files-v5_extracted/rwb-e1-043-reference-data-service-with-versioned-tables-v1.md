<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 043 Reference data service with versioned tables v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 043 Reference data service with versioned tables v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-043 Reference data service with versioned tables

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-043 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-23 Run the reference data service with versioned tables |
| Requirement IDs | REQ-DRI-011, REQ-CWC-006 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, sections 5.3 and 5.7 |
| L3 process | 14 Set strategy, policy and decision rules |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-042, RWB-E1-044 |
| Status | Ready for build |

## 1. Story

As a **reference data administrator (RW-REFADM)**, I want **products, regions, exposure bands, roles, teams, queues, service levels, document types, templates, delegation of authority, legal periods and holidays held as versioned reference data with valid from, valid to, author and approver**, so that **business values change by a data release and not by code, and every engine can say which version it used**.

## 2. Business rationale

Today the values that drive allocation, timers and approval limits live in team spreadsheets and in procedure documents, so nobody can say which value applied to a case on a given day. This story gives every reference table a version with a valid from date, an author and a different approver, and serves the version in force to the engines. It meets REQ-DRI-011 and REQ-CWC-006 and supports control CTL-08 (a rule, limit or list changes only through a validated load approved by its owner). The measure is that every value an engine reads carries a table code and a version number in its log line.

## 3. Preconditions

- RWB-E1-044 is done: Flyway migrations run with the schema name taken from a parameter.
- RWB-E1-042 is done: the configuration service serves `refdata.cache.ttl-seconds` (assumed 300; DL11) and the list of reference table codes.
- The list LOV-REF-TABLE (new, see Additions) is loaded with the 13 table codes in section 8, BR1.
- The reference load endpoint `POST /api/recovery/v1/admin/reference-loads` (P4) is deployed and calls this story's published interface.
- The loader holds RW-REFADM (Reference data C). The approver holds the approve right in Reference data (assumed RW-RISK; see section 10).
- The business date of the ACE service is set (the COLLINS business date from JOB-01).

## 4. Flow

1. Reference data administrator: uploads a load file for one table code with a valid from date through `POST /admin/reference-loads`.
2. P4 load handler: passes the file rows, the table code, the valid from date and the caller's user ID to `ReferenceVersionRegistry.recordVersion(...)`.
3. Reference data service: checks the table code, the row schema for that table, the row keys, the valid from date and the author; computes the content hash and the next version number.
4. Reference data service: writes one `reference_version` row with status VALIDATED and one `reference_row` row per file row, in one transaction.
5. Approver: approves the load through `POST /admin/reference-loads/{loadId}/approve`.
6. Reference data service: checks that the approver is present, is not the author and holds the approve right; sets status APPROVED, `approver_user_id` and `approved_at`.
7. Reference data service: sets `valid_to` of the version it replaces to the day before the new valid from date.
8. Case service, allocation engine and timer engine: on start and on each cache expiry, call `ReferenceDataService.rows(tableCode, businessDate)` and receive the approved version whose valid from is the latest on or before the business date.
9. Each engine: writes one log line per table read, with the table code, the version number and the business date.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Approval attempted with no approver, or by the author | The version stays VALIDATED and is never served | MSG-P7-002 | AC2, AC5 |
| X2 | A row fails the schema or key check for its table | The load is refused in full; no version is written | MSG-P3-027 | AC4 |
| X3 | The valid from date is before the business date | The load is refused in full | MSG-P3-027 | AC6 |
| X4 | The same file is loaded twice for the same table and valid from date | No second version; the first load is returned | None | AC7 |
| X5 | Two approvals of the same load arrive at the same time | One succeeds; the other is refused | MSG-GEN-004 | AC8 |
| X6 | No approved version is in force for a table on the business date | The engine does not start its run and raises an alert to the platform administrator | MSG-P3-027 | AC9 |
| X7 | The load file is empty | The load is refused in full | MSG-GEN-001 | AC10 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the migration tool (RWB-E1-044) and the configuration service (RWB-E1-042). The P4 load endpoint calls this story's interface |
| Negotiable | The list of table codes is data (LOV-REF-TABLE). The story fixes the versioning behavior, not the tables |
| Valuable | Every later rule, timer and approval reads a dated, approved value instead of a spreadsheet |
| Estimable | Two tables, one registry service, one read service, one cache |
| Small | Fits in two weeks with its tests; no screen |
| Testable | Every criterion below is one automated test against a PostgreSQL test container |

## 7. Acceptance criteria

```gherkin
Feature: Reference data service with versioned tables

  Background:
    Given the business date is 2026-11-25
    Given the table "EXPOSURE_BAND" has version 3 approved with valid from 2026-11-30 and bands "E1" to "E4"
    Given user "U-REF-01" holds RW-REFADM and user "U-RSK-01" holds the approve right in Reference data

  Scenario: AC1 Versioned row
    Given "U-REF-01" loads table "EXPOSURE_BAND" with bands "E1" to "E5" and valid from 2026-12-01
    Given "U-RSK-01" approves the load
    When the allocation engine reads "EXPOSURE_BAND" for business date 2026-11-30
    Then version 4 exists with status "APPROVED" and 5 rows
    Then version 3 stays readable with its 4 rows and has valid to 2026-11-30
    Then the service returns version 3 for business date 2026-11-30
    Then the service returns version 4 for business date 2026-12-01

  Scenario: AC2 Approver recorded
    Given "U-REF-01" loads table "DELEGATION_LIMIT" with 24 rows and valid from 2026-12-01
    When "U-REF-01" tries to approve the same load
    Then the system refuses the approval with MSG-P7-002
    Then the version stays "VALIDATED" with no approver
    Then the service still returns the previous "DELEGATION_LIMIT" version for business date 2026-12-01

  Scenario: AC3 Read by services
    Given approved versions are in force for "QUEUE" version 7, "SERVICE_LEVEL" version 2 and "HOLIDAY" version 1
    When the case service and the allocation engine start for business date 2026-11-30
    Then each reads every table it uses from the reference data service
    Then each writes one log line per table with the table code, the version number and the business date
    Then no log line contains a party identifier

  Scenario: AC4 Row fails the schema check
    Given a "SERVICE_LEVEL" load file whose row 12 has the text "five" in the column "limit_days"
    When "U-REF-01" loads it
    Then the system refuses the load with MSG-P3-027 naming row 12 and column "limit_days"
    Then no version and no rows are written

  Scenario: AC5 Approval with no approver
    Given a "HOLIDAY" version 2 with status "VALIDATED" and valid from 2026-12-01
    When the business date reaches 2026-12-01 with no approval recorded
    Then the service returns "HOLIDAY" version 1
    Then version 2 stays "VALIDATED"

  Scenario: AC6 Valid from in the past
    Given the business date is 2026-11-25
    When "U-REF-01" loads table "LEGAL_PERIOD" with valid from 2026-11-24
    Then the system refuses the load with MSG-P3-027 naming the valid from date
    Then the system writes no version

  Scenario: AC7 Same file loaded twice
    Given "U-REF-01" has loaded a "REGION" file with content hash "a1b2" and valid from 2026-12-01 as version 5
    When "U-REF-01" loads the same file with the same valid from date again
    Then the response returns the version 5 load
    Then there is still exactly one version 5 and no version 6

  Scenario: AC8 Two approvals at once
    Given a "QUEUE" version 8 with status "VALIDATED"
    When "U-RSK-01" and "U-RSK-02" approve it at the same moment
    Then the system records exactly one approval
    Then the system refuses the other with MSG-GEN-004

  Scenario: AC9 No version in force
    Given the table "TEAM" has no approved version with valid from on or before 2026-11-30
    When the allocation engine starts for business date 2026-11-30
    Then the engine does not start its run
    Then an alert names table "TEAM" and business date 2026-11-30 with MSG-P3-027

  Scenario: AC10 Empty load file
    Given a "DOCUMENT_TYPE" load file with a header row and no data rows
    When "U-REF-01" loads it
    Then the system refuses the load with MSG-GEN-001 naming "rows"
    Then the system writes no version
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The reference tables served are PRODUCT, REGION, EXPOSURE_BAND, ROLE, TEAM, QUEUE, SERVICE_LEVEL, DOCUMENT_TYPE, TEMPLATE, DELEGATION_LIMIT, LEGAL_PERIOD, HOLIDAY and PRODUCT_PARAMETER. The list is data and changes by a load of LOV-REF-TABLE | Principle 1; DT02; refdata.txt Reference tables |
| BR2 | Each load creates one version, numbered one above the highest version of that table. A version is never changed after it is written | ADR-004; refdata.txt Change process step 5 |
| BR3 | The version in force on a business date is the approved version with the latest valid from on or before that date | R-UNI-38 |
| BR4 | A version takes effect only after an approver who is not the author approves it | CTL-08; roles.txt Separation of duty (Reference data administrator and Risk and model risk officer) |
| BR5 | A load with any failed check is refused in full | refdata.txt Change process step 3; CTL-02 |
| BR6 | A valid from date before the current business date is refused. Open cases keep the version they were decided under | R-UNI-38 |
| BR7 | Every engine logs the table code and version of every table it reads | REQ-CWC-016; ADR-004 |
| BR8 | Approving a new version sets the valid to of the version it replaces to the day before the new valid from | refdata.txt Key (Valid from) |
| BR9 | An engine that finds no version in force for a table it needs does not run on stale or missing values | Principle 5; NFR-033 |

## 9. State transitions

None. This story does not change a case status. It moves a reference version through these statuses (field `reference_version.status`, new):

| From | Event | Condition | To |
|---|---|---|---|
| None | Load received | Every check passes | VALIDATED |
| None | Load received | Any check fails | Not written; load refused |
| VALIDATED | Approval | Approver present, not the author, holds the approve right | APPROVED |
| APPROVED | Rollback (RWB-E1-029 for rule tables; same call for reference tables) | A later version is rolled back | ROLLED_BACK |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-REFADM, reference data administrator | Loads a version (Reference data C). Reads versions (R) |
| RW-COE, center of excellence analyst | Loads a version of the tables it owns (Reference data C) |
| RW-RISK, risk and model risk officer | Approves a version. Assumed: RW-RISK holds the approve right in Reference data, because no role holds it in the permission matrix today. The permission matrix change is loaded through RWB-E1-037; holders by name follow DL18 |
| SY-CASEWF, case workflow module | Reads the version in force (Reference data R) |
| SY-RULES, rules component | Reads the version in force (Reference data R) |
| RW-AUDIT, internal audit | Reads versions and their author and approver (Reference data R) |

The same person may not hold RW-REFADM and RW-RISK (separation of duty table). Approval of DELEGATION_LIMIT follows doa.txt How it applies, rule 11: a change is a data load approved by Risk.

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-159 | reference_version | id | Write |
| DF-REF-160 | reference_version | table_code | Write |
| DF-REF-161 | reference_version | version_no | Write |
| DF-REF-163 | reference_version | valid_from | Write |
| DF-REF-164 | reference_version | valid_to | Write |
| DF-REF-165 | reference_version | status | Write |
| DF-REF-166 | reference_version | author_user_id | Write |
| DF-REF-167 | reference_version | approver_user_id | Write |
| DF-REF-168 | reference_version | approved_at | Write |
| DF-REF-169 | reference_version | row_count | Write |
| DF-REF-170 | reference_version | content_hash | Write |
| DF-REF-171 | reference_version | load_id | Write |
| DF-REF-181 | reference_row | id | Write |
| DF-REF-182 | reference_row | version_id | Write |
| DF-REF-183 | reference_row | row_key | Write |
| DF-REF-184 | reference_row | row_data | Write |
| DF-REF-028 | lov_value | lov_code | Read, through the P4 published interface, for LOV-REF-TABLE |
| DF-REF-029 | lov_value | value_code | Read, through the P4 published interface, for LOV-REF-TABLE |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /api/recovery/v1/admin/reference-loads** (P4 endpoint; calls this story's interface)

| Item | Value |
|---|---|
| Request | multipart/form-data: `file` (CSV or XLSX, one sheet), `table` (a LOV-REF-TABLE code), `validFrom` (date) |
| Response | 201 `ReferenceLoad`: `id`, `table`, `validFrom`, `status` (VALIDATED), `rows` |
| Errors | 401 no session (MSG-P4-001); 403 no Reference data C (MSG-P4-002); 409 an approved version of the table already has this valid from (MSG-P3-027); 422 a check failed (MSG-P3-027) or the file has no rows (MSG-GEN-001); 503 the store is unavailable |
| Authorization | Reference data, right C |
| Idempotency | Table code, valid from and content hash. A repeat returns the existing load and writes nothing |

**POST /api/recovery/v1/admin/reference-loads/{loadId}/approve** (P4 endpoint)

| Item | Value |
|---|---|
| Request | Path `loadId` (uuid). No body |
| Response | 200 `ReferenceLoad` with `status` APPROVED |
| Errors | 401; 403 no Reference data A (MSG-P4-002); 404 unknown load (MSG-P4-003); 409 the approver is the author (MSG-P7-002) or the version changed since it was read (MSG-GEN-004); 503 |
| Authorization | Reference data, right A |
| Idempotency | A second approval of an APPROVED version returns 200 with the same body and changes nothing |

**GET /api/recovery/v1/admin/lists/{listCode}** (P4 endpoint) reads a list with its versions (`ListOfValues`). Reference data R. Used by AC1 to read version 3.

**Published interfaces** (package `recovery.casewf.refdata.api`):

```java
public interface ReferenceVersionRegistry {
    ReferenceVersion recordVersion(String tableCode, LocalDate validFrom, UUID authorUserId,
                              UUID loadId, List<Map<String, Object>> rows);
    ReferenceVersion approve(UUID loadId, UUID approverUserId);
}

public interface ReferenceDataService {
    VersionedRows rows(String tableCode, LocalDate businessDate);
    ReferenceVersion versionInForce(String tableCode, LocalDate businessDate);
    List<ReferenceVersion> versions(String tableCode);
}

public record ReferenceVersion(UUID id, String tableCode, int versionNo, LocalDate validFrom,
                               LocalDate validTo, String status, UUID authorUserId,
                               UUID approverUserId, Instant approvedAt, int rowCount, String contentHash) {}

public record VersionedRows(String tableCode, int versionNo, LocalDate validFrom,
                            List<Map<String, Object>> rows) {}
```

`rows(...)` throws `NoVersionInForceException(tableCode, businessDate)` when no approved version applies. No events are published; the outbox carries none for this story.

## 13. Solution plan

**Package.** `recovery.casewf.refdata` in the recovery module; folder `recovery/casewf/refdata`. Published types in `recovery.casewf.refdata.api`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ReferenceVersionRegistryImpl | Service | Runs the load checks, numbers the version, writes the version and its rows, approves |
| ReferenceDataServiceImpl | Service | Resolves the version in force for a date; serves rows from the cache |
| ReferenceRowCache | Service | In-memory cache keyed by table code and business date; entry time to live from `refdata.cache.ttl-seconds` |
| ReferenceTableSchemas | Rule table | Column names, types and key columns per table code, read from the parameter catalog (RWB-E1-042) |
| ReferenceVersionRepository | Repository | Reads and writes `reference_version` |
| ReferenceRowRepository | Repository | Reads and writes `reference_row` |
| ReferenceVersionEntity, ReferenceRowEntity | Entity | JPA mappings of the two tables, with the standard columns |
| ReferenceVersionRegistry, ReferenceDataService | Published interface | The Java interfaces in section 12 |
| ReferenceVersionLogger | Service | Writes the one log line per table read (table code, version, business date) |

**Database.** Flyway migration `V<next>__rwb_e1_043_reference_versions.sql` (this story creates both tables; schema from the `${schema}` placeholder):

- `reference_version`: `id uuid PK`, `table_code varchar(30) NOT NULL`, `version_no integer NOT NULL`, `valid_from date NOT NULL`, `valid_to date`, `status varchar(15) NOT NULL`, `author_user_id uuid NOT NULL`, `approver_user_id uuid`, `approved_at timestamptz`, `row_count integer NOT NULL`, `content_hash char(64) NOT NULL`, `load_id uuid NOT NULL`, plus the seven standard columns. Constraints: `UNIQUE (table_code, version_no)`; `UNIQUE (table_code, valid_from, content_hash)`; `CHECK (approver_user_id IS NULL OR approver_user_id <> author_user_id)`; partial unique index on `(table_code, valid_from) WHERE status = 'APPROVED'`.
- `reference_row`: `id uuid PK`, `version_id uuid NOT NULL REFERENCES reference_version (id)`, `row_key varchar(200) NOT NULL`, `row_data jsonb NOT NULL`, plus the standard columns. `UNIQUE (version_id, row_key)`; index on `version_id`.
- Both tables append only: an update trigger refuses changes to `reference_row`, and to `reference_version` except `status`, `approver_user_id`, `approved_at`, `valid_to` and the standard columns.

**Configuration and reference data.** `refdata.cache.ttl-seconds` = 300 (assumed; DL11), loaded by the platform administrator in the configuration service. LOV-REF-TABLE values and the column definitions per table code, loaded by the reference data administrator. The first version of each of the 13 tables is loaded by the reference data administrator before SIT and approved by Risk.

**Build steps**

1. Write the migration and the two entities and repositories; test the constraints in a PostgreSQL test container.
2. Build `ReferenceTableSchemas` from the parameter catalog and the row check (type, required, key uniqueness) with a check result per row and column.
3. Build `recordVersion(...)`: table code check, empty file check, valid from check against the business date, content hash (SHA-256 over the rows sorted by key), idempotent return on the same hash, version numbering, one transaction.
4. Build `approve(...)`: approver present and different from the author, approve right checked through the ACE access check, optimistic lock on `version`, set `valid_to` of the replaced version.
5. Build `versionInForce` and `rows` with `NoVersionInForceException`, and the cache.
6. Build `ReferenceVersionLogger` and call it from the case service, the allocation engine and the timer engine start-up hooks (one line per table; no row content).
7. Wire the P4 load and approve handlers to the published interface; map exceptions to the problem responses in section 12.
8. Write the tests in section 16.

**Feature flag.** `rwb.p3.refdata-versions`. Off: the engines read the reference values loaded before this story.

**Done when.** The tests in section 16 pass, the 13 tables each have version 1 approved in SIT, and the boundary test (RWB-TE-001) shows no read of `reference_version` or `reference_row` from outside `recovery.casewf.refdata`.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | A load check fails, the valid from is in the past, or no version is in force for a table an engine needs | The {table} load was refused: {check}. Version {version} stays in force. |
| MSG-P7-002 | The author approves their own load | You prepared this decision, so you cannot approve it. |
| MSG-GEN-001 | The load file has no data rows | Enter {field}. |
| MSG-GEN-004 | Two approvals of one version at once | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | A role without the right loads or approves | You cannot {action} here. Your role does not include it. |

MSG-P3-027 is new (see Additions). Thai text follows DL10.

## 15. Screens and states

No screen in this story. The reference data screen SCR-40 comes in Epic 8; until then the reference data administrator loads files through the endpoint, and the load result (status, row count, refused checks) is returned in the response and listed in the daily data quality report (RWB-E1-011).

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-043-01 | AC1, BR2, BR3, BR8 | System | EXPOSURE_BAND versions 3 and 4, business dates 2026-11-30 and 2026-12-01 |
| TC-E1-043-02 | AC2, BR4 | System | DELEGATION_LIMIT load of 24 rows, author approves own load |
| TC-E1-043-03 | AC3, BR7 | System | QUEUE v7, SERVICE_LEVEL v2, HOLIDAY v1; captured log lines |
| TC-E1-043-04 | AC4, BR5 | System | SERVICE_LEVEL file with a text value in row 12 |
| TC-E1-043-05 | AC5, BR3, BR4 | System | HOLIDAY v2 never approved |
| TC-E1-043-06 | AC6, BR6 | System | LEGAL_PERIOD with valid from 2026-11-24 |
| TC-E1-043-07 | AC7, BR2 | System | REGION file loaded twice with the same hash |
| TC-E1-043-08 | AC8 | System | Two parallel approvals of QUEUE v8 |
| TC-E1-043-09 | AC9, BR9 | System | TEAM with no approved version |
| TC-E1-043-10 | AC10, BR5 | System | DOCUMENT_TYPE file with a header only |
| TC-E1-043-11 | Access | Access | RW-CASEOWN (Reference data R only) calls the load endpoint; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code. Table codes, columns, bands, periods and limits are rows; the code holds only the versioning behavior.
- No personal data in logs, tests or prompts. Log lines carry table codes and version numbers only. Test files use synthetic codes.
- No read of another module's tables. `lov_value` is read through the P4 published interface; P4 reaches the registry only through `ReferenceVersionRegistry`.
- A version row is never updated in place except for its status, approver and valid to; a correction is a new version.
- The cache never serves a version that is not APPROVED.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-011 | Reference data service with versioned tables, valid from and to, author and approver | Business Requirements Epic 1, section 4; Program, section 5.7 | FEAT-CWC-23 | 14 Set strategy, policy and decision rules | R-UNI-38; CTL-08 | TC-E1-043-01 to TC-E1-043-11 |
| REQ-CWC-006 | Roles, teams, queues and capacity as versioned reference data | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-23 | 14 Set strategy, policy and decision rules | R-UNI-38 | TC-E1-043-01, TC-E1-043-03, TC-E1-043-09 |

## 19. Out of scope

- The rule table load, validation and rollback for the five rule tables (RWB-E1-029).
- The permission matrix and masking tables (RWB-E1-037) and the delegation of authority content (RWB-E1-038).
- The checklist fields and the rule change audit report (RWB-E1-048).
- Product parameter completeness checks (RWB-E1-045).
- Reference data screens SCR-39, SCR-40 and SCR-42 (Epic 8).

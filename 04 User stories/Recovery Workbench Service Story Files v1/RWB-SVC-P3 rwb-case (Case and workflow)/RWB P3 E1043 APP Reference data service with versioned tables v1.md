# RWB-P3-E1043-APP Reference data service with versioned tables

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1043-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-043 |
| Legacy disposition | Preserved + delta |
| Build status | In build |
| Patterns applied | DP01, DP04, DP05, DP06, DP07, DP08, DP09, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-O |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P3-E1043-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-P3-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-TE006-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P4-E1037-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-008, FR-P3-012, FR-P3-026, FR-P3-030) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: preserved from RWB-E1-043 word for word, with sections 1 to 11, 14 to 16, 18 and 19 verbatim (only the heading level and the test-case level vocabulary of section 16 in the target form) and the as-built contract and solution plan unchanged under "As built (monolith)", the target reading of sections 3, 8 and 11 and the target traceability additions for REQ-CWC-016 and ADR-012 carried in section 13, sections 12, 13 and 17 written for the target, and the microservice delta in RWB-P3-E1043-CON. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **reference data administrator (RW-REFADM)**, I want **products, regions, exposure bands, roles, teams, queues, service levels, document types, templates, delegation of authority and legal periods held as versioned reference data with valid from, valid to, author and approver**, so that **business values change by a data release and not by code, and every engine can say which version it used**.

### 2. Business rationale

Today the values that drive allocation, timers and approval limits live in team spreadsheets and in procedure documents, so nobody can say which value applied to a case on a given day. This story gives every reference table a version with a valid from date, an author and a different approver, and serves the version in force to the engines. The holiday calendar is not one of them: ACE holds the Bank of Thailand calendar in `bot_holiday`, and the timer engine reads it through `v_ace_holiday`, so no Workbench list holds holidays and no holiday load is needed. It meets REQ-DRI-011 and REQ-CWC-006 and supports control CTL-08 (a rule, limit or list changes only through a validated load approved by its owner). The measure is that every value an engine reads carries a table code and a version number in its log line.

Rule tables are not reference tables any more. The reference data service holds reference tables only, and the rule packages are Drools packages that RWB-E1-072 evaluates and RWB-E1-073 loads, approves and rolls back (D-RCV-36 T3, T4, T8; ADR-012).

### 3. Preconditions

- RWB-E1-044 is done: Flyway migrations run with the schema name taken from a parameter.
- RWB-E1-042 is done: the configuration service serves `refdata.cache.ttl-seconds` (assumed 300; DL11) and the list of reference table codes.
- The list LOV-REF-TABLE (new, see Additions) is loaded with the 12 reference table codes in section 8, BR1. No rule table has a code in it.
- The reference load endpoint `POST /api/recovery/v1/admin/reference-loads` (P4) is deployed and calls this story's published interface.
- The loader holds RW-REFADM (Reference data C). The approver holds the approve right in Reference data (assumed RW-RISK; see section 10).
- The business date of the ACE service is set from the ACE batch record for the day (v_ace_batch_status).

### 4. Flow

1. Reference data administrator: uploads a load file for one table code with a valid from date through `POST /admin/reference-loads`.
2. P4 load handler: passes the file rows, the table code, the valid from date and the caller's user ID to `ReferenceVersionRegistry.recordVersion(...)`.
3. Reference data service: checks the table code, the row schema for that table, the row keys, the valid from date and the author; computes the content hash and the next version number.
4. Reference data service: writes one `reference_version` row with status VALIDATED and one `reference_row` row per file row, in one transaction.
5. Approver: approves the load through `POST /admin/reference-loads/{loadId}/approve`.
6. Reference data service: checks that the approver is present, is not the author and holds the approve right; sets status APPROVED, `approver_user_id` and `approved_at`.
7. Reference data service: sets `valid_to` of the version it replaces to the day before the new valid from date.
8. Case service, allocation engine and timer engine: on start and on each cache expiry, call `ReferenceDataService.rows(tableCode, businessDate)` and receive the approved version whose valid from is the latest on or before the business date.
9. Each engine: writes one log line per table read, with the table code, the version number and the business date.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Approval attempted with no approver, or by the author | The version stays VALIDATED and is never served | MSG-P7-002 | AC2, AC5 |
| X2 | A row fails the schema or key check for its table | The load is refused in full; no version is written | MSG-P3-027 | AC4 |
| X3 | The valid from date is before the business date | The load is refused in full | MSG-P3-027 | AC6 |
| X4 | The same file is loaded twice for the same table and valid from date | No second version; the first load is returned | None | AC7 |
| X5 | Two approvals of the same load arrive at the same time | One succeeds; the other is refused | MSG-GEN-004 | AC8 |
| X6 | No approved version is in force for a table on the business date | The engine does not start its run and raises an alert to the platform administrator | MSG-P3-027 | AC9 |
| X7 | The load file is empty | The load is refused in full | MSG-GEN-001 | AC10 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the migration tool (RWB-E1-044) and the configuration service (RWB-E1-042). The P4 load endpoint calls this story's interface |
| Negotiable | The list of table codes is data (LOV-REF-TABLE). The story fixes the versioning behavior, not the tables |
| Valuable | Every later timer and approval reads a dated, approved value instead of a spreadsheet |
| Estimable | Two tables, one registry service, one read service, one cache |
| Small | Fits in two weeks with its tests; no screen |
| Testable | Every criterion below is one automated test against a PostgreSQL test container |

### 7. Acceptance criteria

```gherkin
Feature: Reference data service with versioned tables

  Background:
    Given the business date is 2026-11-25
    Given the table "EXPOSURE_BAND" has version 3 approved with valid from 2026-11-30 and bands "E1" to "E4"
    Given user "U-REF-01" holds RW-REFADM and user "U-RSK-01" holds the approve right in Reference data

  Scenario: AC1 Versioned row (legacy RWB-E1-043 AC1)
    Given the rwb-access contract mock returns the approve right in Reference data for "U-RSK-01"
    Given "U-REF-01" loads table "EXPOSURE_BAND" with bands "E1" to "E5" and valid from 2026-12-01
    Given "U-RSK-01" approves the load
    When the allocation engine reads "EXPOSURE_BAND" for business date 2026-11-30
    Then version 4 exists with status "APPROVED" and 5 rows
    Then version 3 stays readable with its 4 rows and has valid to 2026-11-30
    Then the service returns version 3 for business date 2026-11-30
    Then the service returns version 4 for business date 2026-12-01

  Scenario: AC2 Approver recorded (legacy RWB-E1-043 AC2)
    Given the rwb-access contract mock returns the approve right in Reference data for "U-RSK-01" and no approve right for "U-REF-01"
    Given "U-REF-01" loads table "DELEGATION_LIMIT" with 24 rows and valid from 2026-12-01
    When "U-REF-01" tries to approve the same load
    Then the system refuses the approval with MSG-P7-002
    Then the version stays "VALIDATED" with no approver
    Then the service still returns the previous "DELEGATION_LIMIT" version for business date 2026-12-01

  Scenario: AC3 Read by services (legacy RWB-E1-043 AC3)
    Given the rwb-source-data contract mock returns the Bank of Thailand calendar from v_ace_holiday for business date 2026-11-30
    Given approved versions are in force for "QUEUE" version 7 and "SERVICE_LEVEL" version 2, and v_ace_holiday holds the Bank of Thailand calendar
    When the case service and the allocation engine start for business date 2026-11-30
    Then each reads every reference table it uses from the reference data service and the holiday calendar from v_ace_holiday
    Then each writes one log line per table with the table code, the version number and the business date
    Then no log line contains a customer identifier

  Scenario: AC4 Row fails the schema check (legacy RWB-E1-043 AC4)
    Given a "SERVICE_LEVEL" load file whose row 12 has the text "five" in the column "limit_days"
    When "U-REF-01" loads it
    Then the system refuses the load with MSG-P3-027 naming row 12 and column "limit_days"
    Then no version and no rows are written

  Scenario: AC5 Approval with no approver (legacy RWB-E1-043 AC5)
    Given a "LEGAL_PERIOD" version 2 with status "VALIDATED" and valid from 2026-12-01
    When the business date reaches 2026-12-01 with no approval recorded
    Then the service returns "LEGAL_PERIOD" version 1
    Then version 2 stays "VALIDATED"

  Scenario: AC6 Valid from in the past (legacy RWB-E1-043 AC6)
    Given the business date is 2026-11-25
    When "U-REF-01" loads table "LEGAL_PERIOD" with valid from 2026-11-24
    Then the system refuses the load with MSG-P3-027 naming the valid from date
    Then the system writes no version

  Scenario: AC7 Same file loaded twice (legacy RWB-E1-043 AC7)
    Given "U-REF-01" has loaded a "REGION" file with content hash "a1b2" and valid from 2026-12-01 as version 5
    When "U-REF-01" loads the same file with the same valid from date again
    Then the response returns the version 5 load
    Then there is still exactly one version 5 and no version 6

  Scenario: AC8 Two approvals at once (legacy RWB-E1-043 AC8)
    Given the rwb-access contract mock returns the approve right in Reference data for "U-RSK-01" and "U-RSK-02"
    Given a "QUEUE" version 8 with status "VALIDATED"
    When "U-RSK-01" and "U-RSK-02" approve it at the same moment
    Then the system records exactly one approval
    Then the system refuses the other with MSG-GEN-004

  Scenario: AC9 No version in force (legacy RWB-E1-043 AC9)
    Given the table "TEAM" has no approved version with valid from on or before 2026-11-30
    When the allocation engine starts for business date 2026-11-30
    Then the engine does not start its run
    Then an alert names table "TEAM" and business date 2026-11-30 with MSG-P3-027

  Scenario: AC10 Empty load file (legacy RWB-E1-043 AC10)
    Given a "DOCUMENT_TYPE" load file with a header row and no data rows
    When "U-REF-01" loads it
    Then the system refuses the load with MSG-GEN-001 naming "rows"
    Then the system writes no version
```

The ten criteria are the legacy ones, copied with their values unchanged. Four of them name a cross-service answer that the story cannot obtain on its own; those criteria carry one added `Given` line for the rwb-access contract mock (the approve right) or the rwb-source-data contract mock (the holiday calendar of `v_ace_holiday`), and no value already in the criterion is changed (DP-05, DP-08, DP-11).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The reference tables served are PRODUCT, REGION, EXPOSURE_BAND, ROLE, TEAM, QUEUE, SERVICE_LEVEL, DOCUMENT_TYPE, TEMPLATE, DELEGATION_LIMIT, LEGAL_PERIOD and PRODUCT_PARAMETER. The list is data and changes by a load of LOV-REF-TABLE. Rule tables are not reference tables and have no code in LOV-REF-TABLE. The holiday calendar is not among them; it is read from v_ace_holiday | Principle 1; REQ-DRI-011; refdata.txt Reference tables; RWB-E1-069 |
| BR2 | Each load creates one version, numbered one above the highest version of that table. A version is never changed after it is written | ADR-012; refdata.txt Change process step 5 |
| BR3 | The version in force on a business date is the approved version with the latest valid from on or before that date | R-UNI-38 |
| BR4 | A version takes effect only after an approver who is not the author approves it | CTL-08; roles.txt Separation of duty (Reference data administrator and Risk and model risk officer) |
| BR5 | A load with any failed check is refused in full | refdata.txt Change process step 3; CTL-02 |
| BR6 | A valid from date before the current business date is refused. Open cases keep the version they were decided under | R-UNI-38 |
| BR7 | Every engine logs the table code and version of every table it reads | REQ-CWC-016; ADR-012 |
| BR8 | Approving a new version sets the valid to of the version it replaces to the day before the new valid from | refdata.txt Key (Valid from) |
| BR9 | An engine that finds no version in force for a table it needs does not run on stale or missing values | Principle 5; NFR-033 |

### 9. State transitions

None. This story does not change a case status. It moves a reference version through these statuses (field `reference_version.status`, new):

| From | Event | Condition | To |
|---|---|---|---|
| None | Load received | Every check passes | VALIDATED |
| None | Load received | Any check fails | Not written; load refused |
| VALIDATED | Approval | Approver present, not the author, holds the approve right | APPROVED |
| APPROVED | Rollback of a reference table by the same call; rule packages roll back through RWB-E1-073 | A later version is rolled back | ROLLED_BACK |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-REFADM, reference data administrator | Loads a version (Reference data C). Reads versions (R) |
| RW-COE, center of excellence analyst | Loads a version of the tables it owns (Reference data C) |
| RW-RISK, risk and model risk officer | Approves a version. Assumed: RW-RISK holds the approve right in Reference data, because no role holds it in the permission matrix today. The permission matrix change is loaded through RWB-E1-037; holders by name follow DL18 |
| SY-CASEWF, case workflow module | Reads the version in force (Reference data R) |
| SY-RULES, Drools evaluator | Reads reference values as Drools facts during an evaluation (Reference data R) |
| RW-AUDIT, internal audit | Reads versions and their author and approver (Reference data R) |

The same person may not hold RW-REFADM and RW-RISK (separation of duty table). Approval of DELEGATION_LIMIT follows doa.txt How it applies, rule 11: a change is a data load approved by Risk.

### 11. Data

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

This story reads and writes no rule table and no rule field: rule_package, rule_package_version and rule_row belong to RWB-E1-072 and RWB-E1-073.

### 12. Contract

The shapes below are the contract of record of RWB-P3-E1043-CON. This story implements them under the rwb-case base `/api/recovery/case/v1` with the schema `rwb_case` (DP-13, DP-15), and the as-built form of the three endpoints is kept under "As built (monolith)" section 12.

#### 12.1 REST operations provided

| Operation | Request | Answer | Owner |
|---|---|---|---|
| `GET /api/recovery/case/v1/admin/lists/{listCode}?asOf=YYYY-MM-DD` | Path list code, for example LOV-REF-TABLE; optional `asOf` business date | The list with its versions; for a reference table code the approved version in force on the date with its rows | P3 |
| `POST /api/recovery/case/v1/admin/reference-loads` | `multipart/form-data`: `file`, `table`, `validFrom`; `Idempotency-Key` | 201 with the load id, table, valid from, status VALIDATED and row count | P3 |
| `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/verify` | Path load id; verifier and note | The check result per row and column of the validated load | P3 |
| `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve` | Path load id | 200 with the approved load and its approver and approval time | P3 |
| `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/rollback` | Path load id; reason | The version returned to ROLLED_BACK and the version in force for the business date | P3 |

A read with no approved version in force for the requested date is refused rather than answered from the latest version: the refusal names the table code and the business date and carries MSG-P3-027 (GAP-0698; ASM-1245).

#### 12.2 REST operations consumed

| Operation | Provider | Use in this story | Pattern |
|---|---|---|---|
| `POST /api/recovery/access/v1/authorise` | P4 rwb-access | The Reference data C, U and A right of a load, a verify, an approval and a rollback | DP-08, DP-11 |
| `GET /api/recovery/access/v1/doa-limits` | P4 rwb-access | The delegation limit a caller needs; this service holds no DoA table | DP-08, DP-11 |
| `GET /api/recovery/case/v1/admin/parameters` | P3 rwb-case (RWB-P3-E1042-CON) | `refdata.cache.ttl-seconds` and the list of reference table codes | DP-06, DP-11 |

Every call is one hop with a 2 s timeout and a breaker per provider (DP-11, ADR-020).

#### 12.3 Events published

None. The Arch v5 catalogue gives rwb-case the topic `rwb.case.events.v1` with CaseCreated, CaseAllocated, CaseAllocationFailed, CaseTransferred, CaseStateChanged and TimerBreached, and a reference version carries no event of its own (Architecture v5 slide 14); a consumer sees a new version at its next cache expiry.

#### 12.4 Events consumed

None. No source declares an event for a version change, and the cache refresh is the expiry of `refdata.cache.ttl-seconds`. An owner event, were one added later, would arrive through the inbox library of RWB-PLT-TE006-CON (DP-09) and would raise a new contract version.

#### 12.5 Workflows and activities

None. A load, a verify, an approval and a rollback are one synchronous transaction each, and a read is a cached read; neither runs in a Temporal workflow or activity on the `rwb-case` queue, and no engine start-up hook is a workflow.

#### 12.6 Schedules

None. There is no Schedule and no job: the refresh is the cache expiry and the loads are operator actions. The 00:01 rule promotion and the six-monthly access review belong to other owners.

#### 12.7 Tables owned

| Table | Schema | Key and indexes | Owner | Rows exposed |
|---|---|---|---|---|
| reference_version | rwb_case | PK id; unique on table_code and version_no; unique on table_code, valid_from and content_hash; partial unique index on table_code, valid_from where status is APPROVED | P3 | The load, verify, approve and rollback answers; the version list of the list read |
| reference_row | rwb_case | PK id; version_id to reference_version; unique on version_id and row_key | P3 | The rows of the version in force in the list read |
| lov_value | rwb_case | PK id; unique on lov_code and value_code | P3 | The list read of a LOV code |

`delegation_limit` is not in this list and not in this schema: it is the P4 rwb-access DoA table (ASM-0070). No rule table is held here (DP-01, DP-04).

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| rwb-access contract fake | `POST /authorise` granting Reference data C, U and A to RW-REFADM and RW-RISK and refusing RW-CASEOWN with MSG-P4-002; `GET /doa-limits` with the DoA rows | This story's right checks and the approval refusal of AC2 and AC8 |
| rwb-case parameters fake (RWB-P3-E1042-CON) | `GET /admin/parameters` with `refdata.cache.ttl-seconds` at 300 and the twelve table codes | The cache and the code check |
| rwb-source-data contract fake | The `v_ace_holiday` answer for a business date | AC3 |

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 5 operations under `/api/recovery/case/v1` | 3 operations over 2 providers | OpenAPI 3.1, one hop, 2 s timeout, `Idempotency-Key` on every POST |
| Kafka | 0 | 0 | No event exists for a version change; the topic of the service is the case life cycle |
| Temporal | 0 | 0 | The load and the read are synchronous; no activity is registered |
| File | 0 | 1 | The load file (CSV or XLSX, one sheet) arrives on the load operation; no runtime file exchange |

### 13. Solution plan

**As-built component set unchanged.** The eight components of the as-built plan stay as built: `ReferenceVersionRegistryImpl`, `ReferenceDataServiceImpl`, `ReferenceRowCache`, `ReferenceVersionRepository`, `ReferenceRowRepository`, `ReferenceVersionEntity`, `ReferenceRowEntity` and `ReferenceVersionLogger`, with the published interfaces `ReferenceVersionRegistry` and `ReferenceDataService`. This story changes none of them, and the as-built contract and solution plan are kept word for word under "As built (monolith)".

**Target reading of the preserved sections 3, 8 and 11.**

**Section 3.** In the target the two tables `reference_version` and `reference_row` and the list `lov_value` are tables of `rwb_case` owned by P3 rwb-case, and the load, verify, approve and rollback operations are operations of this service (Ownership Map ruling ASM-0041, which moves the reference-load paths from rwb-access to rwb-case); their base path is the rwb-case base of the paragraph above and their shapes are the contract of RWB-P3-E1043-CON. One table of the legacy list, `DELEGATION_LIMIT`, is not held here: the Ownership Map keeps `delegation_limit` with P4 rwb-access (ASM-0070), so the DoA table is read from the rwb-access DoA operation and the legacy wording of section 8 BR1 stays as written (GAP-0696; ASM-1243).

**Section 8.** BR1 is the legacy list and stays as written. In the target the twelve codes remain the codes of LOV-REF-TABLE, and eleven of them are served from `rwb_case`; `DELEGATION_LIMIT` is not, because the Ownership Map keeps `delegation_limit` with P4 rwb-access as the DoA table (ASM-0070), so a caller that needs a delegation limit reads it through the rwb-access DoA operation and not through this service (GAP-0696; ASM-1243). The approve right of BR4 is checked on the rwb-access authorise contract (DP-08), and the author check stays local.

**Section 11.** The three tables are created and read in the schema `rwb_case`: `reference_version` and `reference_row` as the rows above carry them, and `lov_value` as a P3 table of the same schema, read through the reference-data contract of this service and not through a P4 interface (Ownership Map ruling ASM-0071; DP-01; DP-07). The `delegation_limit` table is not in this schema and this story reads no column of it (ASM-0070; GAP-0696; ASM-1243). The eleven remaining table codes are rows in `reference_row` and carry no column of their own in this schema. The column definitions of each reference table code — the required columns, their types and their key columns — are Not specified in the source documents (GAP-0697; ASM-1244); they are held as data beside LOV-REF-TABLE and are read by the row check of section 13.

**Target traceability additions.**

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-016 | Every engine logs the table code and version of every table it reads | Business Requirements Epic 1, section 4; Program, section 5.7 | FEAT-CWC-23 | 14 Set strategy, policy and decision rules | R-UNI-38 | TC-E1-043-03 |
| ADR-012 | Versioned reference data with valid from, author and approver; rule packages separate from reference tables | Business Requirements Epic 1, section 4 | FEAT-CWC-23 | 14 Set strategy, policy and decision rules | CTL-08 | TC-E1-043-01, TC-E1-043-07 |

The two legacy rows of section 18 stay unchanged; these two rows are added for the target because section 8 BR7 and section 2 cite REQ-CWC-016 and ADR-012 and the legacy section 18 table named neither.

**Target form of the plan.** The package moves to `th.co.scb.ace.workbench.recovery.case.refdata` inside the rwb-case repository, with the published part of the reference-data contract in `...case.refdata.api` (DP-13, DP-02). The five operations of section 12 are served under the rwb-case base `/api/recovery/case/v1` and not under the monolith base `/api/recovery/v1` on which the as-built endpoints sat, and their shapes are the contract of RWB-P3-E1043-CON (DP-13). The migration is a step of the rwb-case Flyway sequence in the schema `rwb_case` and takes the schema name from the parameter of RWB-PLT-E1044-CON (DP-15; RWB-E1-044). The approve right and the load right are checked on the rwb-access authorise contract and the guard library (DP-08), the cache time to live is read through the parameters contract of this service (DP-06), and the topic and event naming of the service follow RWB-PLT-E1047-CON (DP-14). The read side that the other 18 services and the Drools evaluator compile against is the client contract of RWB-PLT-E1043-CON. The holiday calendar stays ACE data read through `v_ace_holiday` and is served by no part of this story (DP-05).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The three tables are created and read in `rwb_case` only | none |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision. The evaluator reads reference values as facts and this service holds no rule table | H RWB-PLT-E1072-CON; no rule-package contract is consumed by this key |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views. The holiday calendar is read through the P1 contract of `v_ace_holiday` and is served by no list here | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library. `refdata.cache.ttl-seconds` and the table-code list are catalog entries | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case. This legacy key is the owner of that contract, and every other service reads the version in force through it | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library. The load, verify, approve and rollback rights are checked there | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents. No event is published or consumed for a version change, and the library is present for the case side of the service | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. The legacy in-process `ReferenceDataService` becomes the published REST read and the client library, with a fake | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`. The five operations sit under `/api/recovery/case/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library. The reference surface publishes no event, and the service topic stays `rwb.case.events.v1` with `rwb.case.<Event>.v1` names | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema. The two reference tables and `lov_value` arrive on the rwb-case sequence in `rwb_case` | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route. The reference data screens of Epic 8 read the tables through gateway-bff; this story serves no screen | H RWB-PLT-N001-CON |

**Build steps for the target**

1. Move the eight components and the two published interfaces into the rwb-case package and keep the behaviour of sections 4 and 5 unchanged.
2. Add the reference-data migration to the rwb-case Flyway sequence in `rwb_case`, with the three tables and the constraints of the as-built plan, and no `delegation_limit` table (DP-15; ASM-0070).
3. Wire the five operations of section 12.1 to the registry and the read service, with the `asOf` effective-dated read and the refusal of section 12.1.
4. Replace the in-process approve-right check with the rwb-access authorise check and the guard library (DP-08), and read the cache time to live through the parameters contract (DP-06).
5. Build the column definitions per reference table code beside LOV-REF-TABLE and run the row check of section 4 step 3 from them (GAP-0697; ASM-1244).
6. Write the tests of section 16 against the contract baseline of RWB-P3-E1043-CON and its fakes.

**Feature flag.** `rwb.p3.refdata-versions`. Off: the engines read the reference values loaded before this story.

**Done when.** The eleven test cases of section 16 pass, the eleven table codes served here each have version 1 approved in SIT, the holiday calendar is read from `v_ace_holiday` in SIT, the delegation limit is read from the rwb-access DoA operation and not from this service, and the boundary test (RWB-TE-001) shows no read of `reference_version` or `reference_row` from outside the reference-data package.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | A load check fails, the valid from is in the past, or no version is in force for a table an engine needs | The {table} load was refused: {check}. Version {version} stays in force. |
| MSG-P7-002 | The author approves their own load | You prepared this decision, so you cannot approve it. |
| MSG-GEN-001 | The load file has no data rows | Enter {field}. |
| MSG-GEN-004 | Two approvals of one version at once | Someone else changed this record. Reload it to see their change. |
| MSG-P4-002 | A role without the right loads or approves | You cannot {action} here. Your role does not include it. |

MSG-P3-027 is new (see Additions). Thai text follows DL10.

### 15. Screens and states

No screen in this story. The reference data screen SCR-40 comes in Epic 8; until then the reference data administrator loads files through the endpoint, and the load result (status, row count, refused checks) is returned in the response and listed in the daily data quality report (RWB-E1-011).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-043-01 | AC1, BR2, BR3, BR8 | Component | EXPOSURE_BAND versions 3 and 4, business dates 2026-11-30 and 2026-12-01 |
| TC-E1-043-02 | AC2, BR4 | Component | DELEGATION_LIMIT load of 24 rows, author approves own load |
| TC-E1-043-03 | AC3, BR7 | Component | QUEUE v7, SERVICE_LEVEL v2 and v_ace_holiday; captured log lines |
| TC-E1-043-04 | AC4, BR5 | Component | SERVICE_LEVEL file with a text value in row 12 |
| TC-E1-043-05 | AC5, BR3, BR4 | Component | LEGAL_PERIOD v2 never approved |
| TC-E1-043-06 | AC6, BR6 | Component | LEGAL_PERIOD with valid from 2026-11-24 |
| TC-E1-043-07 | AC7, BR2 | Component | REGION file loaded twice with the same hash |
| TC-E1-043-08 | AC8 | Component | Two parallel approvals of QUEUE v8 |
| TC-E1-043-09 | AC9, BR9 | Component | TEAM with no approved version |
| TC-E1-043-10 | AC10, BR5 | Component | DOCUMENT_TYPE file with a header only |
| TC-E1-043-11 | Access | End to end | RW-CASEOWN (Reference data R only) calls the load endpoint; refused with MSG-P4-002 |

The legacy level `System` maps to Component in the target and the legacy level `Access` maps to End to end; nothing else in a row changes, and the full test, with its Given, When and Then, stays in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: table codes, columns, bands, periods and limits are rows; the code holds only the versioning behaviour.
- No personal data in logs, events, workflow inputs, tests or prompts: log lines carry table codes and version numbers only, and test files use synthetic codes and user identifiers.
- ACE data only through the owner's contract or the `v_ace_*` views: the holiday calendar is read through the P1 contract of `v_ace_holiday`, and no reference class opens a connection to an ACE table.
- One schema and one login per service: the three tables are read and written in `rwb_case` and no class reads a table of another schema, `delegation_limit` included (DP-01).
- A version row is never updated in place except for its status, approver and valid to; a correction is a new version.
- The cache never serves a version that is not APPROVED, and a missing version is a refusal with MSG-P3-027, never a default value.
- No rule table is held, loaded or versioned here: rule packages are Drools packages of RWB-E1-072 and RWB-E1-073, and LOV-REF-TABLE carries no rule table code.
- The load, verify, approve and rollback rights come from the rwb-access authorise contract and never from a local role list; the separation of duty of section 10 is enforced on every approval.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-011 | Reference data service with versioned tables, valid from and to, author and approver | Business Requirements Epic 1, section 4; Program, section 5.7 | FEAT-CWC-23 | 14 Set strategy, policy and decision rules | R-UNI-38; CTL-08 | TC-E1-043-01 to TC-E1-043-11 |
| REQ-CWC-006 | Roles, teams, queues and capacity as versioned reference data | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-23 | 14 Set strategy, policy and decision rules | R-UNI-38 | TC-E1-043-01, TC-E1-043-03, TC-E1-043-09 |

### 19. Out of scope

- Rule packages and their load, validation, approval and rollback (RWB-E1-072, RWB-E1-073). Rule tables are not reference tables.
- The permission matrix and masking tables (RWB-E1-037) and the delegation of authority content (RWB-E1-038).
- The checklist fields and the rule change audit report (RWB-E2-041).
- Product parameter completeness checks (RWB-E1-045).
- Reference data screens SCR-39, SCR-40 and SCR-42 (Epic 8).

## As built (monolith)

#### 12. Contract

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

`rows(...)` throws `NoVersionInForceException(tableCode, businessDate)` when no approved version applies. The holiday calendar is not served by this interface: the working-day calculator reads `v_ace_holiday` through the P1 query of RWB-E1-028, because ACE owns the Bank of Thailand calendar. No events are published; the outbox carries none for this story.

Rule packages are out of scope for these endpoints. A rule package is not a reference table: it is loaded, approved and rolled back through the endpoints of RWB-E1-073 and evaluated through RuleEvaluator (RWB-E1-072), so no reference load accepts a rule package code.

#### 13. Solution plan

**Package.** `recovery.casewf.refdata` in the recovery module; folder `recovery/casewf/refdata`. Published types in `recovery.casewf.refdata.api`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ReferenceVersionRegistryImpl | Service | Runs the load checks, numbers the version, writes the version and its rows, approves |
| ReferenceDataServiceImpl | Service | Resolves the version in force for a date; serves rows from the cache |
| ReferenceRowCache | Service | In-memory cache keyed by table code and business date; entry time to live from `refdata.cache.ttl-seconds` |
| ReferenceVersionRepository | Repository | Reads and writes `reference_version` |
| ReferenceRowRepository | Repository | Reads and writes `reference_row` |
| ReferenceVersionEntity, ReferenceRowEntity | Entity | JPA mappings of the two tables, with the standard columns |
| ReferenceVersionRegistry, ReferenceDataService | Published interface | The Java interfaces in section 12 |
| ReferenceVersionLogger | Service | Writes the one log line per table read (table code, version, business date) |

**Database.** Flyway migration `V<next>__rwb_e1_043_reference_versions.sql` (this story creates both tables; schema from the `${schema}` placeholder):

- `reference_version`: `id uuid PK`, `table_code varchar(30) NOT NULL`, `version_no integer NOT NULL`, `valid_from date NOT NULL`, `valid_to date`, `status varchar(15) NOT NULL`, `author_user_id uuid NOT NULL`, `approver_user_id uuid`, `approved_at timestamptz`, `row_count integer NOT NULL`, `content_hash char(64) NOT NULL`, `load_id uuid NOT NULL`, plus the seven standard columns. Constraints: `UNIQUE (table_code, version_no)`; `UNIQUE (table_code, valid_from, content_hash)`; `CHECK (approver_user_id IS NULL OR approver_user_id <> author_user_id)`; partial unique index on `(table_code, valid_from) WHERE status = 'APPROVED'`.
- `reference_row`: `id uuid PK`, `version_id uuid NOT NULL REFERENCES reference_version (id)`, `row_key varchar(200) NOT NULL`, `row_data jsonb NOT NULL`, plus the standard columns. `UNIQUE (version_id, row_key)`; index on `version_id`.
- Both tables append only: an update trigger refuses changes to `reference_row`, and to `reference_version` except `status`, `approver_user_id`, `approved_at`, `valid_to` and the standard columns.
- No rule table exists in this schema, and this story creates none.

**Configuration and reference data.** `refdata.cache.ttl-seconds` = 300 (assumed; DL11), loaded by the platform administrator in the configuration service. LOV-REF-TABLE values and the column definitions per reference table code, loaded by the reference data administrator. The first version of each of the 12 reference tables is loaded by the reference data administrator before SIT and approved by Risk. The holiday calendar is ACE data read through `v_ace_holiday` and has no version row of its own.

**Build steps**

1. Write the migration and the two entities and repositories; test the constraints in a PostgreSQL test container.
2. Build the column definitions per reference table code and the row check (type, required, key uniqueness) from the parameter catalog of RWB-E1-042, with a check result per row and column. The definitions cover the reference table codes only.
3. Build `recordVersion(...)`: table code check, empty file check, valid from check against the business date, content hash (SHA-256 over the rows sorted by key), idempotent return on the same hash, version numbering, one transaction.
4. Build `approve(...)`: approver present and different from the author, approve right checked through the ACE access check, optimistic lock on `version`, set `valid_to` of the replaced version.
5. Build `versionInForce` and `rows` with `NoVersionInForceException`, and the cache.
6. Build `ReferenceVersionLogger` and call it from the case service, the allocation engine and the timer engine start-up hooks (one line per table; no row content).
7. Wire the P4 load and approve handlers to the published interface; map exceptions to the problem responses in section 12.
8. Write the tests in section 16.

**Feature flag.** `rwb.p3.refdata-versions`. Off: the engines read the reference values loaded before this story.

**Done when.** The tests in section 16 pass, the 12 reference tables each have version 1 approved in SIT, the holiday calendar is read from `v_ace_holiday` in SIT, and the boundary test (RWB-TE-001) shows no read of `reference_version` or `reference_row` from outside `recovery.casewf.refdata`.

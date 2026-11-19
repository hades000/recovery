<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-045 Multi-product parameters for Mortgage, HP and SSME

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-045 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-25 Set product parameters without a code change |
| Requirement IDs | REQ-DRI-010, REQ-CWC-011 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, sections 5.3 and 5.7 |
| L3 process | 14 Set strategy, policy and decision rules |
| Decision | D6 entry |
| Priority | Must |
| Depends on | RWB-E1-042, RWB-E1-043, RWB-E1-012 |
| Status | Ready for build |

## 1. Story

As a **center of excellence analyst (RW-COE)**, I want **every product-specific value (entry rule, exclusion list, service levels, notice and cure periods, exposure bands) keyed by product in the reference data**, so that **a new product or a product change needs no code change**.

## 2. Business rationale

Mortgage, hire purchase and SSME follow different notice periods, service levels and bands, and today each difference is held in a team procedure. If the engines carry these values as constants, every product change waits for a release. This story keys each value by product group in the versioned reference tables of RWB-E1-043 and refuses a load that leaves a product without a required value. It meets REQ-DRI-010 and REQ-CWC-011. The measure is that a product is added or changed by a reference load with no deployment.

## 3. Preconditions

- RWB-E1-043 is done: versioned reference tables, the registry and the read service.
- RWB-E1-042 is done: the parameter catalog marks each parameter with scope PRODUCT or GLOBAL, required yes or no, type, unit and allowed range (new catalog fields, see Additions).
- RWB-E1-012 is done: the local copies that held product values are retired.
- Tables PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL have an approved version in force.
- The timer engine (RWB-E1-028), case creation (RWB-E1-018) and the allocation engine (RWB-E1-020) read product values only through `ProductParameterService`.
- The loader holds RW-COE or RW-REFADM (Reference data C); the approver holds the approve right in Reference data.

## 4. Flow

1. Center of excellence analyst: prepares a PRODUCT_PARAMETER load with one row per product group and parameter code, and a SERVICE_LEVEL load with one row per product group and case status.
2. Reference data administrator: loads each file through `POST /admin/reference-loads`.
3. Reference data service: runs the RWB-E1-043 checks, then the product completeness check: every product in the PRODUCT version in force on the valid from date has a row for every catalog parameter with scope PRODUCT and required yes, and a SERVICE_LEVEL row for every status in the parameter `servicelevel.required-statuses`.
4. Reference data service: checks each value against the catalog type and range.
5. Approver: approves the version; it takes effect on its valid from date.
6. Timer engine: when it starts a notice timer for a case, calls `ProductParameterService.get(productGroup, "NOTICE_PERIOD_DAYS", businessDate)` and sets `expires_at` from the value and its unit.
7. Case creation and allocation: read the entry threshold, the exclusion list and the exposure bands for the case's product group the same way.
8. Each engine: records the PRODUCT_PARAMETER version used in its decision log entry inputs (written by the owning story).

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A product has no SERVICE_LEVEL row for a required status | The load is refused in full and the missing product and status are named | MSG-P3-034 | AC3 |
| X2 | A parameter value is outside the catalog range or of the wrong type | The load is refused in full | MSG-GEN-002 | AC4 |
| X3 | Two rows for the same product and parameter | The load is refused in full | MSG-P3-027 | AC5 |
| X4 | A PRODUCT version removes a product that still has open cases | The load is refused in full | MSG-P3-027 | AC6 |
| X5 | At run time a case's product has no parameter row in force | No timer is set; the case goes to the exception queue; the gap is named | MSG-P3-034 | AC7 |
| X6 | A parameter changes while a timer is running | The running timer keeps its expiry; new timers use the new value from its valid from date | None | AC8 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the reference data service of RWB-E1-043 and the catalog of RWB-E1-042 only |
| Negotiable | The parameter list and every value are data; the story fixes the lookup and the completeness check |
| Valuable | A product change becomes a reference load approved by its owner |
| Estimable | One read service, one completeness check, three call sites changed |
| Small | Fits in one week with its tests |
| Testable | Each criterion runs against a PostgreSQL test container with synthetic cases |

## 7. Acceptance criteria

```gherkin
Feature: Multi-product parameters for Mortgage, HP and SSME

  Background:
    Given the business date is 2026-12-01
    Given PRODUCT_PARAMETER version 2 is in force with NOTICE_PERIOD_DAYS 30 calendar days for "MORTGAGE" and 60 calendar days for "HIRE_PURCHASE"
    Given PRODUCT version 1 is in force with "MORTGAGE", "HIRE_PURCHASE", "SSME" and "UNSECURED"

  Scenario: AC1 Product value differs
    Given case "RW-2026-000101" with product group "MORTGAGE" and case "RW-2026-000102" with product group "HIRE_PURCHASE"
    When the timer engine sets the notice timer on both cases on 2026-12-01
    Then the notice timer of "RW-2026-000101" expires on 2026-12-31
    Then the notice timer of "RW-2026-000102" expires on 2027-01-30
    Then each timer start records PRODUCT_PARAMETER version 2

  Scenario: AC2 New product added
    Given PRODUCT version 2 adds product group "AUTO_LEASE" with valid from 2026-12-05
    Given PRODUCT_PARAMETER version 3 and SERVICE_LEVEL version 3 add every required row for "AUTO_LEASE" with valid from 2026-12-05
    Given all three versions are approved
    When the COLLINS load of 2026-12-05 carries an "AUTO_LEASE" account at 90 days past due
    Then the system creates a case with product group "AUTO_LEASE"
    Then the system sets its timers from the "AUTO_LEASE" rows
    Then no deployment took place between 2026-12-01 and 2026-12-05

  Scenario: AC3 Missing parameter blocked
    Given a SERVICE_LEVEL load with valid from 2026-12-10 that has no row for "SSME" and status "WAITING_PARTNER"
    When the load validates
    Then the system refuses the load with MSG-P3-034 naming "SSME" and "WAITING_PARTNER"
    Then SERVICE_LEVEL version 3 stays in force

  Scenario: AC4 Value outside its range
    Given the catalog range for NOTICE_PERIOD_DAYS is 1 to 365
    When a PRODUCT_PARAMETER load sets NOTICE_PERIOD_DAYS to 0 for "SSME"
    Then the system refuses the load with MSG-GEN-002 naming "NOTICE_PERIOD_DAYS", 1 and 365

  Scenario: AC5 Duplicate product row
    Given a PRODUCT_PARAMETER load with two NOTICE_PERIOD_DAYS rows for "MORTGAGE", 30 and 45
    When the load validates
    Then the system refuses the load with MSG-P3-027 naming "MORTGAGE" and "NOTICE_PERIOD_DAYS"

  Scenario: AC6 Product removed while cases are open
    Given 3 open cases with product group "UNSECURED"
    When a PRODUCT load with valid from 2026-12-15 leaves out "UNSECURED"
    Then the system refuses the load with MSG-P3-027 naming "UNSECURED" and 3 open cases

  Scenario: AC7 No parameter in force at run time
    Given case "RW-2026-000140" with product group "SSME" and no NOTICE_PERIOD_DAYS row for "SSME" in force
    When the timer engine sets the notice timer on 2026-12-01
    Then the system writes no notice timer
    Then the system places the case in the exception queue with MSG-P3-034 naming "SSME" and "NOTICE_PERIOD_DAYS"

  Scenario: AC8 Value changes while a timer runs
    Given the notice timer of "RW-2026-000101" started on 2026-12-01 and expires on 2026-12-31
    Given PRODUCT_PARAMETER version 4 with NOTICE_PERIOD_DAYS 45 for "MORTGAGE" takes effect on 2026-12-03
    When the timer engine sets a notice timer on Mortgage case "RW-2026-000150" on 2026-12-03
    Then the timer of "RW-2026-000101" still expires on 2026-12-31
    Then the timer of "RW-2026-000150" expires on 2027-01-17
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every product-specific value is a PRODUCT_PARAMETER or SERVICE_LEVEL row keyed by product group; no engine holds a product value or a product name in code | Principle 1; DT02 |
| BR2 | The parameters required per product are those the catalog marks with scope PRODUCT and required yes: ENTRY_DPD, EXCLUSION_LIST, NOTICE_PERIOD_DAYS, CURE_PERIOD_DAYS and EXPOSURE_BAND_SET. Values per product are the business's (entry 90 days, DL16; service levels DL22; caps DL23) | RWB-E1-042 catalog; DL16; DL22 |
| BR3 | Every product in force has one SERVICE_LEVEL row per status in `servicelevel.required-statuses` (assumed NEW, ASSIGNED, IN_PROGRESS, WAITING_CUSTOMER, WAITING_PARTNER, WAITING_APPROVAL; DL22) | REQ-CWC-011; casemodel.txt Case status |
| BR4 | A load that leaves a required row missing, a value out of range or a duplicate key is refused in full | CTL-08; refdata.txt Change process step 3 |
| BR5 | A product with open cases cannot be removed from PRODUCT | R-UNI-38 |
| BR6 | A timer takes the value in force on the date it starts and keeps it; new values apply from their valid from date | R-UNI-38 |
| BR7 | A value in unit WORKING_DAYS skips the dates in the HOLIDAY table in force; a value in CALENDAR_DAYS does not | refdata.txt Reference tables |
| BR8 | A case whose product has no required value in force is not timed and goes to the exception queue | Principle 5; R-UNI-41 handles the case once a person decides |

## 9. State transitions

None. This story does not change a case status. It changes how the timer engine sets `timer.expires_at` and adds the completeness check to reference version validation (status VALIDATED or refused, RWB-E1-043). A case sent to the exception queue under X5 keeps status New or its current status.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Prepares and loads PRODUCT_PARAMETER and SERVICE_LEVEL versions (Reference data C) |
| RW-REFADM, reference data administrator | Loads PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL versions (Reference data C) |
| RW-PRODHEAD, product head | Owns the values for the product (LOV-PRODUCT owner in refdata.txt); reads versions (Reference data R) |
| RW-RISK, risk and model risk officer | Approves a version where a limit or threshold moves (refdata.txt Change process step 4; assumed approve right as in RWB-E1-043) |
| SY-CASEWF, case workflow module | Reads product values and writes timers |
| SY-RULES, rules component | Reads product values for allocation |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-003 | recovery_case | product_group | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-010 | recovery_case | queue_id | Write (exception queue under X5) |
| DF-WRK-028 | timer | case_id | Write |
| DF-WRK-030 | timer | timer_type | Write |
| DF-WRK-031 | timer | started_at | Write |
| DF-WRK-032 | timer | expires_at | Write |
| DF-WRK-033 | timer | warn_at | Write |
| DF-REF-160 | reference_version | table_code | Read |
| DF-REF-161 | reference_version | version_no | Read |
| DF-REF-183 | reference_row | row_key | Read |
| DF-REF-184 | reference_row | row_data | Read |
| DF-REF-140 | parameter_catalog | scope | Read |
| DF-REF-141 | parameter_catalog | required | Read |

The timer rows are written through the timer engine of RWB-E1-028, which also writes the decision log entry for each timer start. Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**POST /api/recovery/v1/admin/reference-loads** (P4 endpoint; the completeness check runs inside the RWB-E1-043 registry)

| Item | Value |
|---|---|
| Request | multipart/form-data: `file`, `table` (PRODUCT, PRODUCT_PARAMETER or SERVICE_LEVEL), `validFrom` |
| Response | 201 `ReferenceLoad` (`id`, `table`, `validFrom`, `status`, `rows`) |
| Errors | 401 (MSG-P4-001); 403 (MSG-P4-002); 409 open cases on a removed product (MSG-P3-027); 422 missing required row (MSG-P3-034), value out of range (MSG-GEN-002), duplicate key (MSG-P3-027); 503 |
| Authorization | Reference data, right C |
| Idempotency | As RWB-E1-043: table code, valid from and content hash |

**GET /api/recovery/v1/cases/{caseId}/timers** (P3) returns `Timer[]` (`timerType`, `startedAt`, `expiresAt`, `warnAt`, `status`). Case record R. Errors 401, 403, 404 (MSG-P4-003), 503. Used to check AC1, AC2 and AC8.

**Published interface** (package `recovery.casewf.refdata.api`):

```java
public interface ProductParameterService {
    ProductParameter get(String productGroup, String parameterCode, LocalDate businessDate);
    ServiceLevel serviceLevel(String productGroup, String caseStatus, LocalDate businessDate);
}

public record ProductParameter(String productGroup, String parameterCode, String value,
                               String unit, String tableCode, int versionNo) {}

public record ServiceLevel(String productGroup, String caseStatus, int limit, String unit,
                           int warnPercent, String escalateToRole, int versionNo) {}
```

Both methods throw `MissingProductParameterException(productGroup, parameterCode, businessDate)` when no row is in force. No events are published by this story.

## 13. Solution plan

**Package.** `recovery.casewf.refdata.product` in the recovery module; published types in `recovery.casewf.refdata.api`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ProductParameterServiceImpl | Service | Reads PRODUCT_PARAMETER and SERVICE_LEVEL rows in force through `ReferenceDataService`; converts value and unit |
| ProductCompletenessCheck | Service | Load check for PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL: required rows, range, duplicates, products with open cases |
| OpenCaseCounter | Repository | Counts open cases by product group in `recovery_case` (status not CLOSED) |
| DueDateCalculator | Service | Adds calendar or working days, reading HOLIDAY rows in force |
| TimerEngine (RWB-E1-028) | Service | Changed: takes the period from `ProductParameterService` instead of its own table |
| CaseEntryService (RWB-E1-018), AllocationService (RWB-E1-020) | Service | Changed: take ENTRY_DPD, EXCLUSION_LIST and EXPOSURE_BAND_SET from `ProductParameterService` |
| ProductParameterService | Published interface | The interface in section 12 |

**Database.** No new table. Reads `reference_version` and `reference_row` (RWB-E1-043) through the published service, and `recovery_case` (status, product group). Writes `timer` through the timer engine. Index `ix_case_status_queue` on `recovery_case (status, queue_id)` serves the open case count.

**Configuration and reference data.** PRODUCT, PRODUCT_PARAMETER, SERVICE_LEVEL and HOLIDAY versions, loaded by the reference data administrator and owned by the product heads (values per DL16, DL22, DL23). Catalog entries for the five parameters in BR2 with scope, required, type, unit and range, loaded by the center of excellence analyst through RWB-E1-042. Parameter `servicelevel.required-statuses` (assumed list in BR3; DL22).

**Build steps**

1. Build `DueDateCalculator` with the calendar and working day rules; unit test across the 2026-12-31 year end and a holiday row.
2. Build `ProductParameterServiceImpl` over `ReferenceDataService` with `MissingProductParameterException`.
3. Build `ProductCompletenessCheck` and add it as a table check for PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL in the RWB-E1-043 registry.
4. Change the timer engine to take the notice and cure periods from the service and keep the started value on running timers.
5. Change case creation and allocation to take ENTRY_DPD, EXCLUSION_LIST and EXPOSURE_BAND_SET from the service; remove any product name or number from their code.
6. Add the X5 path: on `MissingProductParameterException`, place the case in the exception queue and name the gap.
7. Write the tests in section 16 with synthetic products and cases.

**Feature flag.** `rwb.p3.product-parameters`. Off: the engines use the values they read before this story.

**Done when.** The tests in section 16 pass, and a search of the recovery module code finds no product group code literal outside test fixtures and the generated API types.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-034 | A product has no required parameter or service level row, at load or at run time | {product} has no {parameter} row. Add it before the load. |
| MSG-P3-027 | Duplicate row, or a product with open cases removed | The {table} load was refused: {check}. Version {version} stays in force. |
| MSG-GEN-002 | A value is outside its catalog range | {field} must be between {min} and {max}. |
| MSG-P4-002 | A role without Reference data C loads a file | You cannot {action} here. Your role does not include it. |

MSG-P3-027 and MSG-P3-034 are new (see Additions). Thai text follows DL10.

## 15. Screens and states

No screen in this story. A person sees the result on SCR-03 Case record (read only in Epic 1): the notice timer and its due date for each case. A case sent to the exception queue under X5 shows on SCR-09 Exception queue (Loading; list) with MSG-P3-034.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-045-01 | AC1, BR1, BR6 | System | One Mortgage and one HP case; NOTICE_PERIOD_DAYS 30 and 60 |
| TC-E1-045-02 | AC2, BR1, BR2 | System | New product group AUTO_LEASE with all required rows; one synthetic account |
| TC-E1-045-03 | AC3, BR3, BR4 | System | SERVICE_LEVEL load missing SSME and WAITING_PARTNER |
| TC-E1-045-04 | AC4, BR4 | System | NOTICE_PERIOD_DAYS 0 against range 1 to 365 |
| TC-E1-045-05 | AC5, BR4 | System | Two MORTGAGE rows for one parameter |
| TC-E1-045-06 | AC6, BR5 | System | Three open UNSECURED cases; PRODUCT load without UNSECURED |
| TC-E1-045-07 | AC7, BR8 | System | SSME case with no NOTICE_PERIOD_DAYS in force |
| TC-E1-045-08 | AC8, BR6, BR7 | System | Value changes from 30 to 45 on 2026-12-03 |
| TC-E1-045-09 | Access | Access | RW-PHONECOL (Reference data R only) loads PRODUCT_PARAMETER; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code. No product group code, period, threshold or band is written in Java or TypeScript; the generated API types treat product group as a string checked against LOV-PRODUCT, not as a closed enum.
- No personal data in logs, tests or prompts. Test cases use synthetic case numbers and no customer data.
- No read of another module's tables. Reference rows are read through `ReferenceDataService`; LOV-PRODUCT through the P4 published interface.
- A running timer is never recalculated when a parameter changes.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-010 | Parameter catalog and configuration service hold every threshold, limit and name, versioned | Business Requirements Epic 1, section 4; Program, section 5.7 | FEAT-CWC-25 | 14 Set strategy, policy and decision rules | R-UNI-38; CTL-08 | TC-E1-045-01 to TC-E1-045-09 |
| REQ-CWC-011 | Service levels per queue and status held as data | Business Requirements Epic 1, section 3.3; Program, section 5.3 | FEAT-CWC-25 | 14 Set strategy, policy and decision rules | R-UNI-30; R-UNI-38 | TC-E1-045-01, TC-E1-045-03, TC-E1-045-08 |

## 19. Out of scope

- Letter and notice templates per product (P6, DL28).
- Treatment bands, floors and ranges per product (FEAT-ADM-04, Epic 8).
- Delegation limits per product (RWB-E1-038).
- The timer engine, warnings and escalations themselves (RWB-E1-028).
- Product parameter screens (SCR-39 and SCR-42, Epic 8).

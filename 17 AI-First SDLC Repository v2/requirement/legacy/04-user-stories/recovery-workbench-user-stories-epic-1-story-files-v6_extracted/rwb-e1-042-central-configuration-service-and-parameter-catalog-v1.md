<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 042 Central configuration service and parameter catalog v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB E1 042 Central configuration service and parameter catalog v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-E1-042 Central configuration service and parameter catalog

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-042 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-22 Hold the parameter catalog and configuration service |
| Requirement IDs | REQ-DRI-010 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, sections 5.3 and 5.7 |
| L3 process | 14 Set strategy, policy and decision rules |
| Decision | D6 entry |
| Priority | Must |
| Depends on | RWB-E1-044 |
| Status | Ready for build |

## 1. Story

As a **squad member (RW-TRIBE)**, I want **every environment setting and business parameter read from one configuration service and listed in a parameter catalog with name, type, default, owner, environment and where it is used**, so that **no value is hard-coded and every parameter has an owner**.

## 2. Business rationale

Thresholds such as the 90-day entry point are written into code and spreadsheets today, so a change needs a release and nobody can say who owns a value. This story holds every parameter definition in a catalog with an owner and a default, holds business values as approved, dated versions per environment, serves them to every engine at run time, and fails the build when code carries a literal business value or reads a parameter the catalog does not list. It meets REQ-DRI-010 and puts Principle 1 (DT02) into the build pipeline.

## 3. Preconditions

- RWB-E1-044 is done: the recovery schema exists in each environment.
- The catalog seed file `config/parameter-catalog.csv` is in the repository, owned by RW-COE, with the Epic 1 entries, including `case.entry.dpd` (default 90; DL16), `refdata.cache.ttl-seconds` (default 300; DL11) and `caselist.export.maxrows` (default 10000; DL11).
- The ACE secret store holds secrets per environment; the catalog lists them and never holds their values.
- Loaders hold Reference data C (RW-COE, RW-REFADM). Approvers hold Reference data A: the parameter owner, and RW-RISK where a threshold or a limit moves (assumed grant; DL01).
- The build pipeline runs the checks of this story on every pull request (DL37 code owners).

## 4. Flow

1. Squad member: adds a parameter to `config/parameter-catalog.csv` with key, kind, type, unit, range, default, scope, required, owner role, environments and used by; the pull request is reviewed by the owner.
2. Build: generates the `ParameterKeys` class from the catalog file; code reads a value only through ParameterService with a generated key.
3. Build: runs the magic number check over the recovery packages and the catalog completeness check.
4. Flyway: loads the catalog rows and the default values into parameter_catalog and parameter_value at deployment.
5. RW-COE: loads a new value version through POST /admin/reference-loads with table "PARAMETER", for example `case.entry.dpd` = 91 in PROD valid from 2026-12-10.
6. ParameterLoadChecks: checks key in catalog, type, range, environment and required values; refuses the load whole on any failure.
7. Owner: approves through POST /admin/reference-loads/{loadId}/approve; refused if the approver is the author.
8. ParameterService: from the valid from date returns the new value; every instance refreshes its cache on ParameterVersionApproved and at the latest after the cache time to live.
9. Engines: read values at run time with the version number, and record the version in their decision log inputs.
10. Any role with Rules and parameters R: reads the catalog and the values in force through GET /admin/parameters.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Code holds a literal business value | Build fails naming the file, the line and the parameter with that default | None (build output) | AC2 |
| X2 | Code reads a key that the catalog does not list | Build fails naming the key | None (build output) | AC3 |
| X3 | A required parameter has no value for the environment at start-up | The service does not start; the health check names the key | MSG-P3-032 | AC4 |
| X4 | A loaded value is outside its range | Load refused in full | MSG-GEN-002 | AC5 |
| X5 | A loaded value has the wrong type | Load refused in full | MSG-P1-002 | AC6 |
| X6 | The approver is the author | Approval refused | MSG-P7-002 | AC7 |
| X7 | A secret is asked for through the catalog read | The value is not returned | None | AC9 |
| X8 | Rollback of a value version | The previous version is in force | MSG-P3-015 when none exists | AC10 |
| X10 | A new version is approved before its valid from date | The current value stays until that date; no restart is needed | None | AC11 |
| X9 | A role without Rules and parameters R reads the catalog | Refused with 403 | MSG-P4-002 | Access test TC-E1-042-12 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the schema and migrations (RWB-E1-044); every later engine reads through it |
| Negotiable | The catalog columns and the build check rules can be tuned; the values are data |
| Valuable | No business value in code, and every parameter has an owner |
| Estimable | Two tables, one service, one load check, two build checks, one read endpoint |
| Small | Fits two weeks with its tests |
| Testable | Every criterion has a test case in section 16 |

## 7. Acceptance criteria

```gherkin
Feature: Central configuration service and parameter catalog

  Background:
    Given the catalog lists "case.entry.dpd" as INTEGER, range 1 to 365, default 90, scope GLOBAL, required, owner RW-COE, used by "recovery.casewf.casecreation"

  Scenario: AC1 Parameter read at run time
    Given the parameter "case.entry.dpd" set to 90 in PROD, version 1
    When the case service evaluates entry on 2026-12-01
    Then it uses 90 from the service, not a constant in code
    Then the entry decision records parameter version 1

  Scenario: AC2 Hard-coded value caught
    Given code in package "recovery.casewf.casecreation" with a literal 90 in the entry rule
    When the lint rule for magic numbers runs in the build
    Then the build fails
    Then the output names the file, the line and the parameter "case.entry.dpd"

  Scenario: AC3 Catalog complete
    Given the parameter catalog
    Given code that reads the key "allocation.retry.limit" which the catalog does not list
    When the pipeline compares the catalog with the parameters read by the services
    Then the build fails naming "allocation.retry.limit"
    Then every other parameter in use is in the catalog with an owner and a default

  Scenario: AC4 Required value missing at start-up
    Given "refdata.cache.ttl-seconds" is required and has no value and no default for UAT
    When the service starts in UAT
    Then the health check fails with MSG-P3-032 for "refdata.cache.ttl-seconds" and "UAT"
    Then the service takes no traffic

  Scenario: AC5 Value outside its range
    When RW-COE loads "case.entry.dpd" = 400 for PROD
    Then the system refuses the load with MSG-GEN-002 with minimum 1 and maximum 365

  Scenario: AC6 Wrong type
    When RW-COE loads "case.entry.dpd" = "ninety" for PROD
    Then the system refuses the load with MSG-P1-002 and check "value is not INTEGER"

  Scenario: AC7 Author cannot approve
    Given RW-COE user U-41 loaded value version 3
    When U-41 approves version 3
    Then the system refuses the approval with MSG-P7-002

  Scenario: AC8 Values per environment
    Given "refdata.cache.ttl-seconds" is 30 in SIT and 300 in PROD
    When the reference data service reads it in SIT and in PROD
    Then SIT uses 30 and PROD uses 300

  Scenario: AC9 Secrets are listed, never served
    Given the catalog lists "ace.db.password" as kind ENVIRONMENT with secret = true
    When GET /admin/parameters is called by RW-COE
    Then the entry shows owner, environments and used by
    Then the system returns no value for "ace.db.password"

  Scenario: AC10 Rollback of a value version
    Given value version 2 of "case.entry.dpd" is in force and version 1 was in force before it
    When RW-COE calls rollback for version 2
    Then version 1 is in force and the service returns 90

  Scenario: AC11 A new value takes effect on its valid from date
    Given version 2 sets "case.entry.dpd" to 91 for PROD with valid from 2026-12-10 and is approved on 2026-12-05
    When the case service evaluates entry on 2026-12-09 and on 2026-12-10
    Then it uses 90 on 2026-12-09 and 91 on 2026-12-10
    Then the system restarts no instance
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every value a business person may change is a parameter row with a version, never a constant in code | Principle 1; DT02; BR-P3-022 |
| BR2 | Every parameter in use has a catalog entry with owner, type, default, environments and used by | REQ-DRI-010 |
| BR3 | A business value changes only through a checked, approved, dated load | CTL-08; reference data change process |
| BR4 | The author of a load cannot approve it; Risk approves where a threshold or a limit moves | Separation of duty table; reference data change process, step 4 |
| BR5 | Open decisions keep the version they were taken under; new decisions use the version in force | R-UNI-38 |
| BR6 | Secrets are listed in the catalog and held only in the secret store | DL26; REQ-ACA-005 |
| BR7 | A service does not start without every required parameter for its environment | Principle 1 |

## 9. State transitions

None. This story does not change a case status. It changes the status of a parameter value version: VALIDATED, APPROVED, ROLLED_BACK.

| From | Event | Condition | To |
|---|---|---|---|
| None | Load | Every check passes | VALIDATED |
| VALIDATED | Approve | Approver is not the author | APPROVED; in force from valid from |
| APPROVED | Rollback | An earlier approved version exists | ROLLED_BACK |

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE | Owns the catalog; loads value versions (Reference data C; Rules and parameters CRUD) |
| RW-RISK | Approves a value version where a threshold or a limit moves (Reference data A, assumed grant; DL01) |
| RW-PLATADM | Owns environment settings; reads the catalog (Rules and parameters R) |
| RW-TRIBE | Adds catalog entries through reviewed pull requests |
| Every role with Rules and parameters R | Reads the catalog |
| RW-PHONECOL | No Rules and parameters right; refused |
| No delegation of authority level applies | A parameter is not a credit decision |

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-132 to DF-REF-146 | parameter_catalog | all fields | Write |
| DF-REF-147 to DF-REF-158 | parameter_value | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**GET /admin/parameters** (new endpoint, see additions)

| Item | Value |
|---|---|
| Request | Query key (prefix), kind, owner, environment |
| Response | 200 array of { key, kind, type, unit, min, max, default, scope, required, owner, environments, usedBy, secret, valueInForce (absent when secret), versionNo, validFrom } |
| Errors | 401 (MSG-P4-001); 403 no Rules and parameters R (MSG-P4-002); 503 |
| Authorization | Rules and parameters, right R |
| Idempotency | Not applicable |

**POST /api/recovery/v1/admin/reference-loads** with table "PARAMETER" (P4 endpoint; this story builds the PARAMETER handler)

| Item | Value |
|---|---|
| Request | multipart/form-data: file (rows of key, environment, value), table = "PARAMETER", validFrom |
| Response | 201 ReferenceLoad: id, table, validFrom, status, rows |
| Errors | 401; 403 no Reference data C (MSG-P4-002); 422 range (MSG-GEN-002), type or unknown key (MSG-P1-002), empty file (MSG-GEN-001); 503 |
| Authorization | Reference data, right C |
| Idempotency | Table, valid from and content hash; a repeat returns the existing load |

**POST /api/recovery/v1/admin/reference-loads/{loadId}/approve**: Reference data A; 409 when the approver is the author (MSG-P7-002). **POST /api/recovery/v1/admin/reference-loads/{loadId}/rollback** (new endpoint, recorded with RWB-E1-019): Reference data U; 409 when no earlier version exists (MSG-P3-015).

**Event.** Publishes ParameterVersionApproved (new internal event, see additions: paramKeys, versionNo, validFrom) to the outbox; every instance refreshes its cache.

**Published interface**

```java
// P3, package recovery.casewf.config.api (published)
public interface ParameterService {
    <T> ParameterValue<T> get(ParameterKey<T> key, LocalDate businessDate);
    <T> ParameterValue<T> get(ParameterKey<T> key, String productGroup, LocalDate businessDate);
    CatalogEntry entry(String key);
}
public record ParameterValue<T>(String key, T value, int versionNo, LocalDate validFrom, String environment) {}
// ParameterKeys is generated from config/parameter-catalog.csv, for example
// ParameterKeys.CASE_ENTRY_DPD : ParameterKey<Integer>
```

## 13. Solution plan

**Package.** `recovery/casewf/config` (Java package `recovery.casewf.config`); published types in `recovery.casewf.config.api`; build checks in `build-tools/rwb-checks`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ParameterService | Published interface | Typed read by key, environment and date, with version; cache with refresh on ParameterVersionApproved |
| ParameterCatalogRepository | Repository | parameter_catalog |
| ParameterValueRepository | Repository | parameter_value versions |
| ParameterLoadChecks | Service | Key, type, range, environment and required checks for table PARAMETER |
| ParameterLoadHandler | Service | Handler behind POST /admin/reference-loads for table PARAMETER; approve and rollback |
| ParameterCatalogController | Controller | GET /admin/parameters with secrets left out |
| ParameterStartupCheck | Service | Health indicator that fails when a required value is missing for the environment |
| ParameterKeysGenerator | Build tool | Generates ParameterKeys from the catalog file |
| RwbMagicNumberCheck | Build tool | Fails on numeric and string business literals in recovery packages; allowed: 0, 1, -1, test code; names catalog keys whose default equals the literal |
| CatalogCompletenessCheck | Build tool | Compares keys read through ParameterService with the catalog file; fails on a missing key, owner or default |

**Database**

- Migration in this story: `V042_1__parameter_catalog.sql` creates parameter_catalog (param_key varchar(100) primary key, kind, value_type, unit, min_value, max_value, default_value, scope, required, owner_role, environments, used_by, secret, description, standard columns) and parameter_value (id, param_key references parameter_catalog, environment, param_value, product_group, version_no, valid_from, valid_to, status, author_user_id, approver_user_id, approved_at, standard columns; unique (param_key, environment, product_group, version_no); index (param_key, environment, valid_from) where status = 'APPROVED').
- `V042_2__parameter_seed.sql` is generated from the catalog file and loads the defaults; the schema name comes from the Flyway placeholder.

**Configuration and reference data**

- The catalog file, owned by RW-COE; the Epic 1 entries named in section 3.
- Cache time to live `config.cache.ttl-seconds` = 60 (assumed; DL11), itself a catalog entry.
- Environment settings come from the environment and the secret store; only their catalog entries are in the tables.

**Build steps**

1. Migration, entities and repositories; constraint tests on PostgreSQL.
2. ParameterKeysGenerator and the generated keys from the catalog file.
3. ParameterService with date and environment resolution, version in the result and the cache; tests AC1, AC8, AC10, AC11.
4. ParameterLoadChecks and ParameterLoadHandler with approve and rollback; tests AC5, AC6, AC7, AC10.
5. ParameterStartupCheck; test AC4.
6. ParameterCatalogController with secrets left out; tests AC9 and access.
7. RwbMagicNumberCheck and CatalogCompletenessCheck in the build; tests AC2, AC3 on fixture modules.

**Feature flag.** `rwb.p3.configservice`. Off: services read the defaults from the generated keys only, and value loads are refused.

**Done when.** The tests in section 16 pass and the build on main runs both checks with zero findings.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-032 | A required parameter has no value at start-up | Parameter {name} has no value for {environment}. The service did not start. |
| MSG-GEN-002 | Value outside its range | {field} must be between {min} and {max}. |
| MSG-P1-002 | Wrong type or unknown key in a load | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | Empty load file | Enter {field}. |
| MSG-P7-002 | Approver is the author | You prepared this decision, so you cannot approve it. |
| MSG-P3-015 | Rollback with no earlier version | There is no earlier version of {table} to return to. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No screen in this story. Parameters are read through GET /admin/parameters and changed by file load; SCR-39 Rules and parameters comes in Epic 8 ("by file load before"). Squad members see build check findings in the pipeline output.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-042-01 | AC1, BR1 | System | case.entry.dpd version 1 (90) |
| TC-E1-042-02 | AC2, BR1 | System | Fixture module with a literal 90 |
| TC-E1-042-03 | AC3, BR2 | System | Fixture reading allocation.retry.limit |
| TC-E1-042-04 | AC4, BR7 | System | UAT with no refdata.cache.ttl-seconds |
| TC-E1-042-05 | AC5, BR3 | System | Value 400 |
| TC-E1-042-06 | AC6, BR3 | System | Value "ninety" |
| TC-E1-042-07 | AC7, BR4 | System | Load and approval by U-41 |
| TC-E1-042-08 | AC8 | System | 30 in SIT, 300 in PROD |
| TC-E1-042-09 | AC9, BR6 | System | Secret ace.db.password |
| TC-E1-042-10 | AC10, BR3 | System | Versions 1 and 2 |
| TC-E1-042-11 | AC11, BR5 | System | case.entry.dpd version 2 (91) from 2026-12-10 |
| TC-E1-042-12 | Access | Access | RW-PHONECOL calls GET /admin/parameters and is refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: every limit, threshold, name and timer is a catalog entry with a value row; the build check enforces it.
- No personal data in parameters, logs, tests or prompts; no secret value in the tables, the logs or any response.
- No read of another module's tables: other modules read values only through ParameterService.
- A value change never needs a deployment; a new parameter needs a reviewed catalog entry.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-010 | Parameter catalog and configuration service, versioned, changed without a release | Epic 1, 3.3; Program, 5.7 | FEAT-CWC-22 | 14 Set strategy, policy and decision rules | R-UNI-38 | TC-E1-042-01 to TC-E1-042-11 |

## 19. Out of scope

- The reference data service for the other tables (RWB-E1-043).
- Product-specific parameters and service levels (RWB-E1-045).
- Dated feature flags (FEAT-CWC-26).
- The administration screen for parameters (Epic 8, FEAT-ADM-01).
- The change checklist and audit report (RWB-E1-048).

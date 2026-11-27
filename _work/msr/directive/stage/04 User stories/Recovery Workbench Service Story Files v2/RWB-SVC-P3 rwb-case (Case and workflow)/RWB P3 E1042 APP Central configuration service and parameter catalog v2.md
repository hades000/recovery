# RWB-P3-E1042-APP Central configuration service and parameter catalog

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1042-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-042 |
| Legacy disposition | Preserved + delta |
| Build status | In build |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P3-N |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P3-E1042-APP-16) |
| Depends on (build) | RWB-P3-E1042-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (FR-P3-025) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: preserved from RWB-E1-042 word for word (sections 1 to 11, 14 to 16, 18 and 19), with the as-built contract and solution plan kept unchanged under "As built (monolith)" and sections 12, 13 and 17 written for rwb-case; the delta of this legacy key is the contract slice RWB-P3-E1042-CON. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P3-E1042-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (11 resolved, 20 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **squad member (RW-TRIBE)**, I want **every environment setting and business parameter read from one configuration service and listed in a parameter catalog with name, type, default, owner, environment and where it is used**, so that **no value is hard-coded and every parameter has an owner**.

### 2. Business rationale

Thresholds such as the 90-day entry point are written into code and spreadsheets today, so a change needs a release and nobody can say who owns a value. This story holds every parameter definition in a catalog with an owner and a default, holds business values as approved, dated versions per environment, serves them to every engine at run time, and fails the build when code carries a literal business value or reads a parameter the catalog does not list. It meets REQ-DRI-010 and puts Principle 1 (DT02) into the build pipeline.

### 3. Preconditions

- RWB-E1-044 is done: the recovery schema exists in each environment.
- The catalog seed file `config/parameter-catalog.csv` is in the repository, owned by RW-COE, with the Epic 1 entries, including `case.entry.dpd` (default 90; DL16), `refdata.cache.ttl-seconds` (default 300; DL11) and `caselist.export.maxrows` (default 10000; DL11).
- The ACE secret store holds secrets per environment; the catalog lists them and never holds their values.
- Loaders hold Reference data C (RW-COE, RW-REFADM). Approvers hold Reference data A: the parameter owner, and RW-RISK where a threshold or a limit moves (assumed grant; DL01).
- The build pipeline runs the checks of this story on every pull request (DL37 code owners).

### 4. Flow

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

### 5. Exception paths

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
| X9 | A role without Rules and parameters R reads the catalog | Refused with 403 | MSG-P4-002 | AC12; access test TC-E1-042-12 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the schema and migrations (RWB-E1-044); every later engine reads through it |
| Negotiable | The catalog columns and the build check rules can be tuned; the values are data |
| Valuable | No business value in code, and every parameter has an owner |
| Estimable | Two tables, one service, one load check, two build checks, one read endpoint |
| Small | Fits two weeks with its tests |
| Testable | Every criterion has a test case in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Central configuration service and parameter catalog

  Background:
    Given the catalog lists "case.entry.dpd" as INTEGER, range 1 to 365, default 90, scope GLOBAL, required, owner RW-COE, used by "recovery.casewf.casecreation"

  Scenario: AC1 Parameter read at run time (legacy RWB-E1-042 AC1)
    Given the parameter "case.entry.dpd" set to 90 in PROD, version 1
    When the case service evaluates entry on 2026-12-01
    Then it uses 90 from the service, not a constant in code
    Then the entry decision records parameter version 1

  Scenario: AC2 Hard-coded value caught (legacy RWB-E1-042 AC2)
    Given code in package "recovery.casewf.casecreation" with a literal 90 in the entry rule
    When the lint rule for magic numbers runs in the build
    Then the build fails
    Then the output names the file, the line and the parameter "case.entry.dpd"

  Scenario: AC3 Catalog complete (legacy RWB-E1-042 AC3)
    Given the parameter catalog
    Given code that reads the key "allocation.retry.limit" which the catalog does not list
    When the pipeline compares the catalog with the parameters read by the services
    Then the build fails naming "allocation.retry.limit"
    Then every other parameter in use is in the catalog with an owner and a default

  Scenario: AC4 Required value missing at start-up (legacy RWB-E1-042 AC4)
    Given "refdata.cache.ttl-seconds" is required and has no value and no default for UAT
    When the service starts in UAT
    Then the health check fails with MSG-P3-032 for "refdata.cache.ttl-seconds" and "UAT"
    Then the service takes no traffic

  Scenario: AC5 Value outside its range (legacy RWB-E1-042 AC5)
    When RW-COE loads "case.entry.dpd" = 400 for PROD
    Then the system refuses the load with MSG-GEN-002 with minimum 1 and maximum 365

  Scenario: AC6 Wrong type (legacy RWB-E1-042 AC6)
    When RW-COE loads "case.entry.dpd" = "ninety" for PROD
    Then the system refuses the load with MSG-P1-002 and check "value is not INTEGER"

  Scenario: AC7 Author cannot approve (legacy RWB-E1-042 AC7)
    Given RW-COE user U-41 loaded value version 3
    When U-41 approves version 3
    Then the system refuses the approval with MSG-P7-002

  Scenario: AC8 Values per environment (legacy RWB-E1-042 AC8)
    Given "refdata.cache.ttl-seconds" is 30 in SIT and 300 in PROD
    When the reference data service reads it in SIT and in PROD
    Then SIT uses 30 and PROD uses 300

  Scenario: AC9 Secrets are listed, never served (legacy RWB-E1-042 AC9)
    Given the catalog lists "ace.db.password" as kind ENVIRONMENT with secret = true
    When GET /admin/parameters is called by RW-COE
    Then the entry shows owner, environments and used by
    Then the system returns no value for "ace.db.password"

  Scenario: AC10 Rollback of a value version (legacy RWB-E1-042 AC10)
    Given value version 2 of "case.entry.dpd" is in force and version 1 was in force before it
    When RW-COE calls rollback for version 2
    Then version 1 is in force and the service returns 90

  Scenario: AC11 A new value takes effect on its valid from date (legacy RWB-E1-042 AC11)
    Given version 2 sets "case.entry.dpd" to 91 for PROD with valid from 2026-12-10 and is approved on 2026-12-05
    When the case service evaluates entry on 2026-12-09 and on 2026-12-10
    Then it uses 90 on 2026-12-09 and 91 on 2026-12-10
    Then the system restarts no instance

  Scenario: AC12 A role without Rules and parameters R is refused the catalog (new, D-RCV-60)
    Given a user whose role does not include Rules and parameters R
    When that user calls GET /admin/parameters
    Then the system refuses the read with 403 and MSG-P4-002

  Scenario: AC13 An error answer of a provided operation carries its status code (new, D-RCV-60)
    Given a request to GET /admin/parameters without a valid identity
    When the request is sent
    Then the system answers 401
    And the same operation answers 403 to a role without Rules and parameters R
    And the same operation answers 404 for a parameter the catalog does not list

  Scenario: AC14 A status change the model does not allow is refused (new, D-RCV-60)
    Given a value version whose current status does not allow the requested change
    When RW-COE requests that status change
    Then the system refuses the change with a message code Not specified in the source documents (NEWAC-RWB-P3-E1042-APP-AC14)
    Then the version keeps its current status
```

These eleven criteria stay as written and every value in them is kept, and AC12 to AC14 (new, D-RCV-60) cover exception X9, the error answers and the refused status change: no criterion carries a cross-service leg, because in the target the catalog, the value versions, the case engine and the reference-data reader all live in rwb-case, so no scenario needs a contract mock; where the legacy text says "the service" or "the reference data service" it is rwb-case itself. The two build checks of AC2 and AC3 run against the target packages of section 13, and the `used by` value "recovery.casewf.casecreation" is the legacy package name (GAP-2214; ASM-3641).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every value a business person may change is a parameter row with a version, never a constant in code | Principle 1; DT02; BR-P3-022 |
| BR2 | Every parameter in use has a catalog entry with owner, type, default, environments and used by | REQ-DRI-010 |
| BR3 | A business value changes only through a checked, approved, dated load | CTL-08; reference data change process |
| BR4 | The author of a load cannot approve it; Risk approves where a threshold or a limit moves | Separation of duty table; reference data change process, step 4 |
| BR5 | Open decisions keep the version they were taken under; new decisions use the version in force | R-UNI-38 |
| BR6 | Secrets are listed in the catalog and held only in the secret store | DL26; REQ-ACA-005 |
| BR7 | A service does not start without every required parameter for its environment | Principle 1 |

### 9. State transitions

None. This story does not change a case status. It changes the status of a parameter value version: VALIDATED, APPROVED, ROLLED_BACK.

| From | Event | Condition | To |
|---|---|---|---|
| None | Load | Every check passes | VALIDATED |
| VALIDATED | Approve | Approver is not the author | APPROVED; in force from valid from |
| APPROVED | Rollback | An earlier approved version exists | ROLLED_BACK |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE | Owns the catalog; loads value versions (Reference data C; Rules and parameters CRUD) |
| RW-RISK | Approves a value version where a threshold or a limit moves (Reference data A, assumed grant; DL01) |
| RW-PLATADM | Owns environment settings; reads the catalog (Rules and parameters R) |
| RW-TRIBE | Adds catalog entries through reviewed pull requests |
| Every role with Rules and parameters R | Reads the catalog |
| RW-PHONECOL | No Rules and parameters right; refused |
| No delegation of authority level applies | A parameter is not a credit decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-132 to DF-REF-146 | parameter_catalog | all fields | Write |
| DF-REF-147 to DF-REF-158 | parameter_value | all fields | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

The shapes below are the contract of record of RWB-P3-E1042-CON. This story implements them under the rwb-case base `/api/recovery/case/v1` in the schema `rwb_case` (DP-13, DP-15) against Version 1 (major) of the published client contract, the version the contract artefact of the as-built section 12 records; the monolith endpoints and the published Java interface are kept unchanged under "As built (monolith)" section 12.

#### 12.1 REST operations provided

| Operation | Request | Answer | Owner |
|---|---|---|---|
| `GET /api/recovery/case/v1/admin/parameters` | Query: key (prefix), kind, owner, environment | 200 with the catalog entries and the value in force per environment as { key, kind, type, unit, min, max, default, scope, required, owner, environments, usedBy, secret, valueInForce, versionNo, validFrom }; `valueInForce` absent when secret; 401 MSG-P4-001; 403 MSG-P4-002; 503 | P3 |
| `POST /api/recovery/case/v1/admin/reference-loads` with `table` = PARAMETER | `multipart/form-data`: file (rows of key, environment, value), table, validFrom; `Idempotency-Key` | 201 with the load id, table, valid from, status VALIDATED and row count; 401; 403 MSG-P4-002; 422 MSG-GEN-002, MSG-P1-002 or MSG-GEN-001; 503 | P3 |
| `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/approve` | Path load id | 200 with the approved load, its approver and the approval time; 401; 403 MSG-P4-002; 404; 409 MSG-P7-002 when the approver is the author; 503 | P3 |
| `POST /api/recovery/case/v1/admin/reference-loads/{loadId}/rollback` | Path load id; reason | 200 with the version returned to ROLLED_BACK and the version in force for the business date; 401; 403 MSG-P4-002; 404; 409 MSG-P3-015 when no earlier version exists; 503 | P3 |

A load of table PARAMETER is refused in full on any failed check and a repeat load of the same table, valid from and content hash returns the first load and writes nothing. The rights are the legacy ones — Reference data C for a load, Reference data A for an approval, Reference data U for a rollback and Rules and parameters R for the read — and are resolved by the authorise model of rwb-access through the guard the service template wires, so no role list is stored here (GAP-2215; ASM-3642).

#### 12.2 REST operations consumed

None. The PARAMETER handler plugs into the reference-load operation of this same service (RWB-P3-E1043-CON, an H dependency and a same-service component, not a cross-service call), and every key the handler checks is a row of `parameter_catalog` in `rwb_case`. The read that the other services make is described in section 12.8 and its path and right for a service identity are Not specified in the source documents (GAP-2213; ASM-3640).

#### 12.3 Events published

| Event | Topic | Payload | Owner |
|---|---|---|---|
| `rwb.case.ParameterVersionApproved.v1` | `rwb.case.events.v1` | paramKeys, versionNo, validFrom, environment; CloudEvents envelope; written to the outbox in the same transaction as the approval; no personal data | P3 |

Every instance refreshes its cache on this event and at the latest at the cache time to live. The place of the event in the rwb-case event catalogue, its key and any payload field beyond the three the legacy story names are Not specified in the source documents (GAP-2212; ASM-3639).

#### 12.4 Events consumed

None from another service. Every instance of rwb-case refreshes on the event of section 12.3 through the inbox library of RWB-PLT-TE006-CON (DP-09) and, at the latest, at the cache time to live, so a missed event delays a refresh and never a correctness of a value.

#### 12.5 Workflows and activities

None. A load, a check, an approval, a rollback and a read are one synchronous transaction each on the api deployment; nothing runs in a Temporal workflow or activity on the `rwb-case` queue.

#### 12.6 Schedules

None. No Temporal Schedule and no job is declared: the value takes effect on its valid from date, the refresh is the event of section 12.3 or the cache expiry, and a load is an operator action.

#### 12.7 Tables owned

| Table | Schema | Key and indexes | Owner | Rows exposed |
|---|---|---|---|---|
| parameter_catalog | rwb_case | PK param_key (varchar(100)); the id column of DF-REF-132 also present; one row per parameter, never per environment | P3 | Every row of the catalog read |
| parameter_value | rwb_case | PK id; param_key references parameter_catalog; unique on param_key, environment, product_group and version_no; index on param_key, environment and valid_from where status is APPROVED | P3 | valueInForce, versionNo and validFrom per environment; the load, approve and rollback answers |

No table of another service is read and no engine reads these two tables: another service reads values through the operation of 12.1 and the client library (DP-01, DP-06, DP-11).

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| rwb-case parameters fake (this story) | The four operations of 12.1 with the seeded entries — `case.entry.dpd` at version 1 (90), `refdata.cache.ttl-seconds` at 30 in SIT and 300 in PROD, `caselist.export.maxrows` at 10000, `ace.db.password` listed with secret = true and no value — plus the load, approve and rollback answers and the refusal messages | RWB-P3-E1042-CON, RWB-PLT-E1042-CON, the case, allocation and timer engines |
| rwb-case reference-data fake (RWB-P3-E1043-CON) | The reference-load operation for the other table codes and the shared four-eyes refusal | The PARAMETER handler's shared checks and AC7 |
| Build-check fixtures (this story) | A fixture module with a literal 90 in the entry rule (AC2) and a fixture that reads `allocation.retry.limit` (AC3) | The two build checks and the pipeline |

The fake answers from fixtures and carries role codes and user identifiers only; it never carries a secret value and never a customer identifier.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 4 operations under `/api/recovery/case/v1` | 0 | OpenAPI 3.1, one hop, 2 s timeout and a breaker, `Idempotency-Key` on every POST |
| Kafka | 1 event on `rwb.case.events.v1` | 0 | Outbox and inbox, CloudEvents, no personal data, cache refresh only |
| Temporal | 0 | 0 | Everything is synchronous; no activity is registered |
| File | 0 | 1 | The load file of table PARAMETER (CSV or XLSX) arrives on the load operation; no runtime file exchange |

### 13. Solution plan

**As-built component set unchanged.** The ten components of the as-built plan stay as built: `ParameterService`, `ParameterCatalogRepository`, `ParameterValueRepository`, `ParameterLoadChecks`, `ParameterLoadHandler`, `ParameterCatalogController`, `ParameterStartupCheck`, `ParameterKeysGenerator`, `RwbMagicNumberCheck` and `CatalogCompletenessCheck`. This story changes none of their behaviour, and the as-built contract and solution plan are kept word for word under "As built (monolith)".

**Target reading of the preserved sections 3, 8 and 11.**

**Section 3.** The schema is `rwb_case` and the two tables are created by the rwb-case Flyway sequence in it, not by the single recovery schema of RWB-E1-044 (DP-01, DP-15). The catalog file stays the single source of the keys and lives in the rwb-case repository, owned by RW-COE; its path is as built and the path the service template expects is Not specified in the source documents (GAP-2214; ASM-3641). A secret is still only listed: its value is read from the ACE secret store and never stored (BR6).

**Section 8.** BR1 to BR7 stand as written. BR2 reads in the target as the entry of `parameter_catalog` plus the value versions of `parameter_value` in `rwb_case`, and the `used by` column names the target service and component instead of the monolith package (GAP-2214; ASM-3641). BR5 holds because a decision record carries the key and the version number it used, written through the local decision-record library (DP-03). BR7 holds for every service, not only for rwb-case: a service's start-up check reads its keys through the client library and fails its health check with MSG-P3-032 (GAP-2213; ASM-3640).

**Section 11.** Both tables are written in `rwb_case` only, with the field identifiers DF-REF-132 to DF-REF-158 unchanged (DP-01). No other service reads them; the read is the operation of 12.1 through the client library, so a value reaches another service as a dated read with its version, never as a table read (DP-06, DP-11).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. Both tables are created and read in `rwb_case` only | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`. A decision that used a parameter records the key and the version number | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library. This key owns that contract and the platform client is what the other 18 services compile | H RWB-PLT-E1042-CON; the same-service contract RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case. Table PARAMETER is loaded through the reference-load operation of this service and the other table codes stay with RWB-P3-E1043 | H RWB-PLT-E1043-CON; the same-service contract RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents. ParameterVersionApproved is written to the outbox with the approval | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout. The in-process `ParameterService` stays inside rwb-case, and the other services read the published operation with a fake | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`. The four operations sit under `/api/recovery/case/v1`; the monolith base survives only inside the as-built section | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library. The event is `rwb.case.ParameterVersionApproved.v1` on `rwb.case.events.v1` | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema. The two tables arrive on the rwb-case sequence in `rwb_case` with the schema name from the placeholder | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route. SCR-39 reads the catalog through gateway-bff in Epic 8; this story serves no screen and declares no route | H RWB-PLT-N001-CON |

**Target traceability additions.**

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-005 | A secret is held in the secret store and never in a table, a log or an answer | Business Requirements Program, section 5.7 | FEAT-CWC-22 | 14 Set strategy, policy and decision rules | None | TC-E1-042-09 |

The legacy row of section 18 stays unchanged; this row is added for the target because section 8 BR6 cites REQ-ACA-005 and the legacy section 18 table named only REQ-DRI-010.

**Build steps for the target**

1. Move the ten components into the target service package ruled by the Solution architect under the Service Template Specification v1 naming rule, with the published part in its `.api` subpackage, and keep the behaviour of sections 4 and 5 unchanged (DP-02, DP-13). The ruled segment replaces the segment `case` of `th.co.scb.ace.workbench.recovery.case.config`, which is a Java reserved word; the segment is Not specified in the source documents (CG-ALL-3731).
2. Put the two tables and their constraints on the rwb-case Flyway sequence in `rwb_case`, with the seed generated from the catalog file, and record the target file numbers of the two migrations (DP-15; GAP-2214; ASM-3641).
3. Wire the four operations of 12.1 to `ParameterCatalogController` and `ParameterLoadHandler`, with `Idempotency-Key` on every POST and the `valueInForce` left out when `secret` is true (AC9).
4. Publish `rwb.case.ParameterVersionApproved.v1` to the outbox with the approval, and refresh the cache on receipt through the inbox library and at the latest at the cache time to live (DP-09, DP-14).
5. Keep `ParameterStartupCheck` for rwb-case and hand the same check to every other service through the client library, so a missing required value stops the service with MSG-P3-032 (AC4; GAP-2213; ASM-3640).
6. Re-point `RwbMagicNumberCheck` and `CatalogCompletenessCheck` at the target packages and run them in the rwb-case pipeline and in each consuming service's pipeline (AC2, AC3).
7. Record the key and the version number of every parameter a decision used in the decision record (AC1, BR5).

**Feature flag.** `rwb.p3.configservice`, read through the platform feature-flag library per the default ruling. Off: services read the defaults from the generated keys only and a value load is refused. The flag keeps the as-built name and the name the flag library expects is Not specified in the source documents (GAP-2214; ASM-3641).

**Done when.** The twelve test cases of section 16 pass, the catalog and its Epic 1 defaults are loaded in SIT and UAT, both build checks run with zero findings on the main build, one value version has been loaded, approved and rolled back in SIT, and one service has started, refused to start and started again with MSG-P3-032 proved against a missing required value.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-032 | A required parameter has no value at start-up | Parameter {name} has no value for {environment}. The service did not start. |
| MSG-GEN-002 | Value outside its range | {field} must be between {min} and {max}. |
| MSG-P1-002 | Wrong type or unknown key in a load | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-001 | Empty load file | Enter {field}. |
| MSG-P7-002 | Approver is the author | You prepared this decision, so you cannot approve it. |
| MSG-P3-015 | Rollback with no earlier version | There is no earlier version of {table} to return to. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-001 | Request without a valid sign-in (401) | Not specified in the source documents (DOR-RWB-P3-E1042-APP-9) |

### 15. Screens and states

No screen in this story. Parameters are read through GET /admin/parameters and changed by file load; SCR-39 Rules and parameters comes in Epic 8 ("by file load before"). SCR-39 states: empty, loading, error and no access are Not specified in the source documents (CG-ALL-3734). Squad members see build check findings in the pipeline output.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-042-01 | AC1, BR1 | Component | case.entry.dpd version 1 (90) |
| TC-E1-042-02 | AC2, BR1 | Component | Fixture module with a literal 90 |
| TC-E1-042-03 | AC3, BR2 | Component | Fixture reading allocation.retry.limit |
| TC-E1-042-04 | AC4, BR7 | Component | UAT with no refdata.cache.ttl-seconds |
| TC-E1-042-05 | AC5, BR3 | Component | Value 400 |
| TC-E1-042-06 | AC6, BR3 | Component | Value "ninety" |
| TC-E1-042-07 | AC7, BR4 | Component | Load and approval by U-41 |
| TC-E1-042-08 | AC8 | Component | 30 in SIT, 300 in PROD |
| TC-E1-042-09 | AC9, BR6 | Component | Secret ace.db.password |
| TC-E1-042-10 | AC10, BR3 | Component | Versions 1 and 2 |
| TC-E1-042-11 | AC11, BR5 | Component | case.entry.dpd version 2 (91) from 2026-12-10 |
| TC-E1-042-12 | AC12, Access | End to end | RW-PHONECOL calls GET /admin/parameters and is refused with MSG-P4-002 |
| TC-E1-042-13 | Section 12 operations and events (contract) | Component | GET /admin/parameters, reference-loads, approve, rollback and the ParameterVersionApproved payload |
| TC-E1-042-14 | Section 12.7 tables (boundary, ASM-3438) | Component | param_key at varchar(100); one row per parameter and per environment |
| TC-E1-042-15 | AC13, Section 12 operations (contract) | Component | Request without identity, request by a role without R, unknown parameter |
| TC-E1-042-16 | AC14 | Component | Value version whose status does not allow the requested change |

The legacy level `System` maps to Component in the target and the legacy level `Access` maps to End to end; nothing else in a row changes, and the full test, with its Given, When and Then, stays in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: every limit, threshold, name, timer and default is a catalog row and a value row, and both build checks enforce it; the only constants in code are the ones the catalog generates.
- No personal data in parameters, logs, tests or prompts, and no secret value in a table, a log, an example or an answer: a secret entry carries `secret = true` and no `valueInForce` (AC9, BR6).
- One schema and one login per service: both tables live in `rwb_case`, no other service reads them, and no class of this service opens another service's schema (DP-01).
- ACE data only through the owner's contract or the `v_ace_*` views; this story reads no ACE table.
- A value change never needs a deployment; a new parameter needs a reviewed catalog entry and a regenerated key class.
- A breaking change to the four operations or to the event raises a new contract version and deprecates the old one; the event name stays inside the `rwb.case.<Event>.v1` form (DP-14).
- The rights of the four operations are resolved by the guard the service template wires and are never re-implemented here as a role list.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-010 | Parameter catalog and configuration service, versioned, changed without a release | Epic 1, 3.3; Program, 5.7 | FEAT-CWC-22 | 14 Set strategy, policy and decision rules | R-UNI-38 | TC-E1-042-01 to TC-E1-042-11, TC-E1-042-13, TC-E1-042-14 |

Open decisions for this story (DOR-RWB-P3-E1042-APP-18): DL01 (ASM-0189, ASM-1230, ASM-1770, ASM-1988); DL11 (ASM-0553, ASM-0703, ASM-1051, ASM-1104); DL16 (ASM-1094, ASM-5264); DL26 (ASM-0247, ASM-0264, ASM-0275, ASM-0355); DL37 (ASM-0189, ASM-0425, ASM-2516, ASM-3199). Each decision is still open and its assumptions apply until it is closed.

### 19. Out of scope

- The reference data service for the other tables (RWB-E1-043).
- Product-specific parameters and service levels (RWB-E1-045).
- Dated feature flags (FEAT-CWC-26).
- The administration screen for parameters (Epic 8, FEAT-ADM-01).
- The change checklist and audit report (RWB-E2-041).

## As built (monolith)

#### 12. Contract

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

**Event.** Publishes rwb.case.ParameterVersionApproved.v1 (topic Not specified in the source documents (GAP-2212)) with paramKeys, versionNo and validFrom to the outbox; every instance refreshes its cache, and the cache time to live is the fallback. The owner of the cache time to live is Not specified in the source documents (GAP-1406).

The client artefact coordinates (group, artefact name, version scheme and publication channel) are taken from the platform library baseline at version freeze and pinned in the service template.

**Contract artefact.** Version 1 (major) of the published client contract; its members, the catalog and value data contract, the operation status codes and the freeze rule are Not specified in the source documents (GAP-1407).

**Build-check contract.** The two build-check rule sets are the contract of RWB-PLT-E1042-CON; the rule set itself is Not specified in the source documents (GAP-1406).

**Chart values and probe.** The chart values, the seed ordering, the probe and the alert thresholds are Not specified in the source documents (GAP-1408).

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

#### 13. Solution plan

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

- Migration in this story: `V<next free number of the rwb-case sequence>__parameter_catalog.sql` creates parameter_catalog (param_key varchar(100) primary key, kind, value_type, unit, min_value, max_value, default_value, scope, required, owner_role, environments, used_by, secret, description, standard columns) and parameter_value (id, param_key references parameter_catalog, environment, param_value, product_group, version_no, valid_from, valid_to, status, author_user_id, approver_user_id, approved_at, standard columns; unique (param_key, environment, product_group, version_no); index (param_key, environment, valid_from) where status = 'APPROVED').
- `V<next free number of the rwb-case sequence, plus one>__parameter_seed.sql` is generated from the catalog file and loads the defaults; the schema name comes from the Flyway placeholder.

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

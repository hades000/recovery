# Technical Specification — RWB-E1-045 Multi-product parameters for Mortgage, HP and SSME

| Field | Value |
|---|---|
| Story | RWB-E1-045 — Multi-product parameters for Mortgage, HP and SSME |
| Epic / module | E1 / P3 Case and workflow |
| RUN_ID | `INC-037-epic-1-RWB-E1-045` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-007, FR-RWB-020); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md` |
| Upstream IDs | BRD-RWB-003, BRD-RWB-020; FR-RWB-007, FR-RWB-020; REQ-DRI-010, REQ-CWC-011; US-RWB-E1-045; CTX-FEATURE-003; DL16, DL22, DL23; R-UNI-30, R-UNI-38 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. SCR-03 Case record and SCR-09 Exception queue already exist and display the timer and the exception; no component, route, label or state is added. |
| Logic In Scope | `YES` — product-parameter lookup, completeness checks, due-date calculation and the missing-parameter path. |
| API In Scope | `NO` — no new or changed contract. The story reuses `POST /admin/reference-loads` (P4) and `GET /api/recovery/v1/cases/{caseId}/timers` (P3). |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `PRODUCT_PARAMETER`, `SERVICE_LEVEL`, `PRODUCT`, `HOLIDAY` reference tables; timer engine (RWB-E1-028); case creation (RWB-E1-018); allocation (RWB-E1-020); SCR-03 and SCR-09. |
| New Nodes Required | `YES` — `ProductParameterServiceImpl`, `ProductCompletenessCheck`, `OpenCaseCounter`, `DueDateCalculator`, `MissingProductParameterException`. |
| Inherited Existing Behavior | RWB-E1-043 reference versions and registry; RWB-E1-042 catalog and parameters; RWB-E1-028 timer engine; RWB-E1-018 case creation; RWB-E1-020 allocation. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every product-specific value is a PRODUCT_PARAMETER or SERVICE_LEVEL row keyed by product group; no engine holds a product value or name in code. | SPEC-RWB-E1-045-001, SPEC-RWB-E1-011 | DIRECT | `ProductParameterService` is the only read path; product group is a string checked against the list. | COVERED |
| BR2 | Required parameters per product are those the catalog marks scope PRODUCT and required yes: ENTRY_DPD, EXCLUSION_LIST, NOTICE_PERIOD_DAYS, CURE_PERIOD_DAYS and EXPOSURE_BAND_SET. | SPEC-RWB-E1-045-002, SPEC-RWB-E1-045-003 | DIRECT | Catalog drives the list; values per product are the business's (DL16, DL22). | COVERED |
| BR3 | Every product in force has one SERVICE_LEVEL row per status in `servicelevel.required-statuses`. | SPEC-RWB-E1-045-004 | DIRECT | Assumed list: NEW, ASSIGNED, IN_PROGRESS, WAITING_CUSTOMER, WAITING_PARTNER, WAITING_APPROVAL (DL22). | COVERED |
| BR4 | A load that leaves a required row missing, a value out of range or a duplicate key is refused in full. | SPEC-RWB-E1-045-005, SPEC-RWB-E1-045-006 | DIRECT | `ProductCompletenessCheck` refuses whole; previous version stays. | COVERED |
| BR5 | A product with open cases cannot be removed from PRODUCT. | SPEC-RWB-E1-045-007 | DIRECT | `OpenCaseCounter` counts cases with status other than CLOSED. | COVERED |
| BR6 | A timer takes the value in force on the date it starts and keeps it; new values apply from their valid from date. | SPEC-RWB-E1-045-008 | DIRECT | Running timers are not recalculated. | COVERED |
| BR7 | A value in WORKING_DAYS skips the dates in the HOLIDAY table in force; CALENDAR_DAYS does not. | SPEC-RWB-E1-045-009 | DIRECT | `DueDateCalculator` reads HOLIDAY through `ReferenceDataService`. | COVERED |
| BR8 | A case whose product has no required value in force is not timed and goes to the exception queue. | SPEC-RWB-E1-045-010 | DIRECT | `MissingProductParameterException`; MSG-P3-034; R-UNI-41 handles it. | COVERED |
| AC1 | Mortgage notice timer expires 2026-12-31 and HP 2027-01-30 from 2026-12-01; each records PRODUCT_PARAMETER version 2. | SPEC-RWB-E1-045-001, SPEC-RWB-E1-045-008, SPEC-RWB-E1-045-009 | DIRECT | 30 and 60 calendar days. | COVERED |
| AC2 | A new AUTO_LEASE product with all required rows creates a case and timers with no deployment. | SPEC-RWB-E1-045-002, SPEC-RWB-E1-045-003, SPEC-RWB-E1-045-011 | DIRECT | PRODUCT v2, PRODUCT_PARAMETER v3, SERVICE_LEVEL v3 from 2026-12-05. | COVERED |
| AC3 | A SERVICE_LEVEL load missing SSME / WAITING_PARTNER is refused naming both; version 3 stays. | SPEC-RWB-E1-045-004 | DIRECT | MSG-P3-034. | COVERED |
| AC4 | NOTICE_PERIOD_DAYS 0 against 1..365 is refused naming the parameter and bounds. | SPEC-RWB-E1-045-005 | DIRECT | MSG-GEN-002. | COVERED |
| AC5 | Two NOTICE_PERIOD_DAYS rows for MORTGAGE are refused naming product and parameter. | SPEC-RWB-E1-045-006 | DIRECT | MSG-P3-027. | COVERED |
| AC6 | A PRODUCT load that removes UNSECURED with 3 open cases is refused naming the product and count. | SPEC-RWB-E1-045-007 | DIRECT | MSG-P3-027. | COVERED |
| AC7 | An SSME case with no NOTICE_PERIOD_DAYS writes no timer and goes to the exception queue. | SPEC-RWB-E1-045-010 | DIRECT | MSG-P3-034. | COVERED |
| AC8 | A running timer keeps its expiry; a new timer uses the new value. | SPEC-RWB-E1-045-008, SPEC-RWB-E1-045-009 | DIRECT | 30 -> 45 days on 2026-12-03; new expiry 2027-01-17. | COVERED |
| X1..X6 | Exceptional paths in the table below map to SPEC-004..010. | SPEC-RWB-E1-045-004..010 | DIRECT | Missing service level, range/type, duplicate, product removal, missing at run time, value change. | COVERED |

## User story intent interpretation

As a **center of excellence analyst (RW-COE)**, I want **every product-specific value (entry rule, exclusion list, service levels, notice and cure periods, exposure bands) keyed by product in the reference data**, so that **a new product or a product change needs no code change**.

The story makes product differences data. It adds the completeness check that refuses a load leaving a product without a required row, a read service that the timer, case-creation and allocation engines use, and the run-time path that sends a case with no value to the exception queue instead of guessing. Mortgage, HP and SSME are the Epic 1 products; the same mechanism accepts a new product.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Reference-data load of PRODUCT, PRODUCT_PARAMETER or SERVICE_LEVEL; timer start; case creation; allocation. |
| Preconditions | RWB-E1-043 done; RWB-E1-042 catalog marks scope PRODUCT and required; RWB-E1-012 done (local copies retired); PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL have an approved version in force; the timer, case-creation and allocation engines read only through `ProductParameterService`; loader holds Reference data C. |
| Input | Product group, parameter code or case status, business date, reference load file. |
| Output | `ProductParameter` and `ServiceLevel` values with version; timer expiry; exception-queue placement; load result. |
| Feature flag | `rwb.p3.product-parameters`. Off: the engines use the values they read before this story. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `reference_row` (PRODUCT) | product group | PRODUCT load | New version only | Must be in LOV-PRODUCT; a removed product with open cases is refused. |
| `reference_row` (PRODUCT_PARAMETER) | product group, parameter code, value, unit | PRODUCT_PARAMETER load | New version only | One row per product and parameter; value type and range from the catalog. |
| `reference_row` (SERVICE_LEVEL) | product group, case status, limit, unit, warn percent, escalate-to role | SERVICE_LEVEL load | New version only | One row per product and status in `servicelevel.required-statuses`. |
| `parameter_catalog` | `scope`, `required`, `value_type`, `min_value`, `max_value` | RWB-E1-042 | Reviewed change only | Drives the completeness and range checks. |
| `timer` | `timer_type`, `started_at`, `expires_at`, `warn_at` | Timer engine | System-written | Running timer keeps its expiry; new timer uses the value in force. |
| `recovery_case` | `product_group`, `status`, `queue_id` | Existing case | Read; queue written on X5 | Product group is a string, not a closed enum. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | PRODUCT_PARAMETER / SERVICE_LEVEL load | Every required row, range and duplicate check passes | VALIDATED | Version stored; no engine change yet. |
| None | Load | Any check fails | Not written | Load refused in full; previous version stays. |
| VALIDATED | Approve | Approver not author | APPROVED | In force from `valid_from`. |
| Timer RUNNING | Parameter change | New version takes effect | RUNNING (unchanged) | Expiry stays; only new timers use the new value. |
| Timer none | Timer start | No value in force for the product | No timer | Case to exception queue; MSG-P3-034. |

This story changes no case status; a case sent to the exception queue keeps its current status.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Product has no SERVICE_LEVEL row for a required status | Load refused in full; product and status named | MSG-P3-034 |
| X2 | Value outside range or wrong type | Load refused in full | MSG-GEN-002 |
| X3 | Two rows for the same product and parameter | Load refused in full | MSG-P3-027 |
| X4 | PRODUCT version removes a product with open cases | Load refused in full | MSG-P3-027 |
| X5 | At run time the product has no parameter row in force | No timer; case to exception queue; gap named | MSG-P3-034 |
| X6 | Parameter changes while a timer runs | Running timer keeps expiry; new timers use the new value | None |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | `POST /api/recovery/v1/admin/reference-loads` (table PRODUCT, PRODUCT_PARAMETER or SERVICE_LEVEL); `GET /api/recovery/v1/cases/{caseId}/timers`. |
| Contract delta | None. The load endpoint already accepts a table code and valid from; the timer response already carries timerType, startedAt, expiresAt, warnAt and status. |
| Backward compatibility | Unchanged. |
| Authorization | Reference data C to load; Case record R to read timers. 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-P3-027; 422 MSG-P3-034/MSG-GEN-002/MSG-P3-027; 503. |
| Versioning | No version change. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | SCR-03 and SCR-09 are existing screens; no component, route, state or label changes. | Existing frontend tests remain green. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-007, FR-RWB-020; SPEC-RWB-E1-045-001..013 | New read service, completeness check, due-date calculator and three engine call-site changes. | Positive, negative, boundary and error-path tests: product difference, new product, missing row, range, duplicate, product removal, missing at run time, value change, working-day holiday. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `ProductParameterServiceImpl` | Service | Reads PRODUCT_PARAMETER and SERVICE_LEVEL rows in force through `ReferenceDataService`; converts value and unit. |
| `ProductCompletenessCheck` | Service | Load check for PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL: required rows, range, duplicates, products with open cases. |
| `OpenCaseCounter` | Repository | Counts open cases by product group in `recovery_case` (status not CLOSED). |
| `DueDateCalculator` | Service | Adds calendar or working days, reading HOLIDAY rows in force. |
| `TimerEngine` | Service | Changed: takes the period from `ProductParameterService` instead of its own table. |
| `CaseEntryService` / `AllocationService` | Service | Changed: take ENTRY_DPD, EXCLUSION_LIST and EXPOSURE_BAND_SET from the service. |
| `ProductParameterService` | Published interface | `get(productGroup, parameterCode, businessDate)` and `serviceLevel(productGroup, caseStatus, businessDate)`. |

### Package and boundaries

`recovery.casewf.refdata.product`, published types in `recovery.casewf.refdata.api`. Reference rows
are read through `ReferenceDataService`; LOV-PRODUCT through the P4 interface; `recovery_case` is read
only for open-case counts. No engine reads `reference_row` directly.

### Data and migration

No new table. Reads `reference_version` and `reference_row` (RWB-E1-043) and `recovery_case`
(status, product group). Writes `timer` through the timer engine (RWB-E1-028). Index
`ix_case_status_queue` on `recovery_case (status, queue_id)` serves the open-case count.

### Product lookup

- `get(productGroup, parameterCode, businessDate)` resolves the PRODUCT_PARAMETER version in force and
  returns the row for the product and parameter with value, unit, table code and version.
- `serviceLevel(productGroup, caseStatus, businessDate)` resolves the SERVICE_LEVEL version in force
  and returns limit, unit, warn percent, escalate-to role and version.
- A missing row throws `MissingProductParameterException(productGroup, parameterCode, businessDate)`.
- Product group is a string checked against LOV-PRODUCT, not a Java enum.

### Completeness and range checks

1. Every product in the PRODUCT version in force on the valid from date has a row for every catalog
   parameter with scope PRODUCT and required yes: ENTRY_DPD, EXCLUSION_LIST, NOTICE_PERIOD_DAYS,
   CURE_PERIOD_DAYS and EXPOSURE_BAND_SET.
2. Every product has a SERVICE_LEVEL row for every status in `servicelevel.required-statuses`.
3. Every value matches its catalog type and range.
4. No duplicate (product group, parameter code) or (product group, case status) row.
5. A PRODUCT load cannot remove a product that has open cases.
Any failure refuses the load whole and names the product, parameter or status.

### Due dates and running timers

- `DueDateCalculator` adds the value in its unit: CALENDAR_DAYS adds calendar days; WORKING_DAYS adds
  working days and skips HOLIDAY rows in force.
- `expires_at` is the start date plus the period; `warn_at` is set by the timer engine from the
  service-level warning percent, not by this story.
- A running timer keeps its `expires_at` when a parameter changes. A new timer uses the value in force
  on its start date and records the PRODUCT_PARAMETER version in the decision log inputs.

### Run-time gap

On `MissingProductParameterException`, the timer engine writes no timer and places the case in the
exception queue with MSG-P3-034 naming the product and parameter. The case keeps its current status;
R-UNI-41 handles it once a person decides.

### Transaction and events

The load writes the version and rows in one transaction. The timer write and the exception-queue
placement are in the timer engine's transaction. No event is published by this story.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-COE | Reference data C; prepares and loads PRODUCT_PARAMETER and SERVICE_LEVEL | All |
| RW-REFADM | Reference data C; loads PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL | All |
| RW-PRODHEAD | Owns the product values; Reference data R | All |
| RW-RISK | Approves where a limit or threshold moves (assumed; DL01) | All |
| SY-CASEWF | Reads product values and writes timers | All |
| SY-RULES | Reads product values for allocation | All |

### Observability and operations

- Load response: status, row count, each missing product/parameter/status and each out-of-range value.
- Timer start log: case number, product group, parameter code, version and expiry; no personal data.
- Metrics: loads, refusals by check, missing-parameter exceptions, timers started by product.
- Alert: a run-time missing parameter; a product in force with no SERVICE_LEVEL rows.

### Performance

- Reads are cached by `ReferenceDataService`; the product lookup is one indexed row.
- The completeness check runs at load, not at run time.
- `ix_case_status_queue` supports the open-case count.

### Feature flag and rollback

- `rwb.p3.product-parameters`: off means the engines use the values they read before this story.
- Rollback: turn the flag off; redeploy the previous tag. A parameter rollback is a data action through
  the reference rollback endpoint.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-045-01 | AC1, BR1, BR6 | System | Mortgage and HP cases, 30/60 days | Expiry 2026-12-31 and 2027-01-30; version 2 |
| TC-E1-045-02 | AC2, BR1, BR2 | System | AUTO_LEASE with all rows | Case and timers created; no deployment |
| TC-E1-045-03 | AC3, BR3, BR4 | System | SERVICE_LEVEL missing SSME/WAITING_PARTNER | Refused; both named; v3 stays |
| TC-E1-045-04 | AC4, BR4 | System | NOTICE_PERIOD_DAYS 0 | Refused; 1 and 365 named |
| TC-E1-045-05 | AC5, BR4 | System | Two MORTGAGE rows | Refused; product and parameter named |
| TC-E1-045-06 | AC6, BR5 | System | Three open UNSECURED cases | Refused; product and count named |
| TC-E1-045-07 | AC7, BR8 | System | SSME with no NOTICE_PERIOD_DAYS | No timer; exception queue; MSG-P3-034 |
| TC-E1-045-08 | AC8, BR6, BR7 | System | 30 -> 45 on 2026-12-03 | Old timer 2026-12-31; new 2027-01-17 |
| TC-E1-045-09 | X5 | Security | RW-PHONECOL loads PRODUCT_PARAMETER | 403; MSG-P4-002 |

## Guardrails and out of scope

- No business value in code. No product group code, period, threshold or band in Java or TypeScript;
  product group is a string checked against LOV-PRODUCT.
- No personal data in logs, tests or prompts. Test cases use synthetic case numbers.
- Reference rows are read through `ReferenceDataService`; LOV-PRODUCT through the P4 interface.
- A running timer is never recalculated when a parameter changes.
- Out of scope: letter and notice templates per product (P6, DL28); treatment bands, floors and ranges
  (FEAT-ADM-04, Epic 8); delegation limits per product (RWB-E1-038); the timer engine, warnings and
  escalations (RWB-E1-028); product parameter screens (SCR-39, SCR-42, Epic 8).

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR3; SPEC-004 | Is the required-status list fixed? | Determines completeness. | `servicelevel.required-statuses` = NEW, ASSIGNED, IN_PROGRESS, WAITING_CUSTOMER, WAITING_PARTNER, WAITING_APPROVAL (assumed; DL22); the list is data. | RESOLVED | SPEC-004 |
| CLAR-002 | BR7; SPEC-009 | Which unit applies to notice and cure periods? | Changes expiry dates. | The row's unit decides: CALENDAR_DAYS or WORKING_DAYS; the AC uses calendar days. | RESOLVED | SPEC-009 |
| CLAR-003 | Title; SPEC-001 | Is "HP" a product code? | Lookup value. | No; HIRE_PURCHASE is the code. HP is the business shorthand. | RESOLVED | SPEC-001 |
| CLAR-004 | BR5; SPEC-007 | What counts as an open case for product removal? | Boundary. | A case with status other than CLOSED. | RESOLVED | SPEC-007 |
| CLAR-005 | AC2; SPEC-002 | Does adding AUTO_LEASE need a separate LOV-PRODUCT load? | The AC names only PRODUCT v2. | The PRODUCT reference version is the source of product groups; LOV-PRODUCT is served from it. Recorded as ASSUMED for the data steward. | RESOLVED | SPEC-002 |
| CLAR-006 | AC1, AC8; SPEC-009 | Is the expiry the start date plus the period? | Date arithmetic. | Yes: 2026-12-01 + 30 days = 2026-12-31; + 60 = 2027-01-30; + 45 from 2026-12-03 = 2027-01-17. | RESOLVED | SPEC-009 |
| CLAR-007 | §11; SPEC-008 | Does this story set `warn_at`? | Warning behaviour. | No; the timer engine sets it from the service-level warning percent (RWB-E1-028). | RESOLVED | SPEC-008 |
| CLAR-008 | BR6; SPEC-008 | Does a value change recalculate running timers? | Would move agreed dates. | No; running timers keep their expiry. | RESOLVED | SPEC-008 |

`CLARIFICATION_STATUS: RESOLVED` — all 8 items are answered from the story, DL22 or the data model.
The LOV-PRODUCT source is an accepted assumption with a named owner.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend product-parameter story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New multi-product parameter lookup and completeness checks; no screen and no contract change; reference-load and timer endpoints reused.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: product value lookup and validation with no screen or contract delta]
REQUIREMENT_COVERAGE_SUMMARY: All 8 business rules, 8 acceptance criteria, 6 exception paths and 3 timer states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 8] [COVERED_RULES: 8] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

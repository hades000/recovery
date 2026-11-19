# Technical Specification — RWB-E1-042 Central configuration service and parameter catalog

| Field | Value |
|---|---|
| Story | RWB-E1-042 — Central configuration service and parameter catalog |
| Epic / module | E1 / P3 Case and workflow |
| RUN_ID | `INC-003-epic-1-RWB-E1-042` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-020); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 042 Central configuration service and parameter catalog v1.md` |
| Upstream IDs | BRD-RWB-020; FR-RWB-020; REQ-DRI-010; US-RWB-E1-042; CTX-FEATURE-020; DT02; DL11, DL16, DL26; API-P3-018 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. Parameters are read through the API and changed by file load; SCR-39 is Epic 8. |
| Logic In Scope | `YES` — catalog, typed read, load checks, approval, effective dating, rollback, cache and startup check. |
| API In Scope | `YES` — this story first delivers `GET /admin/parameters` (API-P3-018) and the `PARAMETER` handler of the reference-load endpoints. The contract is already in API Specification v2; no OpenAPI delta. |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | P4 reference-load handler; P1 job monitor (no change); configuration/secret store; SCR-39 (Epic 8, not built here). |
| New Nodes Required | `YES` — `ParameterService`, `ParameterCatalogRepository`, `ParameterValueRepository`, `ParameterLoadChecks`, `ParameterLoadHandler`, `ParameterCatalogController`, `ParameterStartupCheck`, `ParameterKeysGenerator`, `RwbMagicNumberCheck`, `CatalogCompletenessCheck`. |
| Inherited Existing Behavior | RWB-E1-044 migrations and `RWB_SCHEMA`; ACE secret store; P4 reference-load and approval pattern (RWB-E1-043); ACE access check. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every value a business person may change is a parameter row with a version, never a constant in code. | SPEC-RWB-E1-042-001, SPEC-RWB-E1-042-002, SPEC-RWB-E1-042-004 | DIRECT | `parameter_catalog` + `parameter_value`; generated `ParameterKeys`; magic-number build check. | COVERED |
| BR2 | Every parameter in use has a catalog entry with owner, type, default, environments and used by. | SPEC-RWB-E1-042-003 | DIRECT | `CatalogCompletenessCheck` compares keys read through `ParameterService` with the catalog file. | COVERED |
| BR3 | A business value changes only through a checked, approved, dated load. | SPEC-RWB-E1-042-005, SPEC-RWB-E1-042-011 | DIRECT | `ParameterLoadChecks` refuses the load whole; effective from `valid_from`. | COVERED |
| BR4 | The author of a load cannot approve it; Risk approves where a threshold or limit moves. | SPEC-RWB-E1-042-006 | DIRECT | Approver must differ from author; threshold parameters require RW-RISK. | COVERED |
| BR5 | Open decisions keep the version they were taken under; new decisions use the version in force. | SPEC-RWB-E1-042-011 | DIRECT | Version returned with each read and recorded in decision-log inputs by the calling engine. | COVERED |
| BR6 | Secrets are listed in the catalog and held only in the secret store. | SPEC-RWB-E1-042-009 | DIRECT | `secret=true`; read response omits `valueInForce`. | COVERED |
| BR7 | A service does not start without every required parameter for its environment. | SPEC-RWB-E1-042-007 | DIRECT | `ParameterStartupCheck` fails readiness; no traffic. | COVERED |
| AC1 | `case.entry.dpd` is read at run time and the entry decision records parameter version 1. | SPEC-RWB-E1-042-002, SPEC-RWB-E1-042-011 | DIRECT | Typed read returns value, version and valid from. | COVERED |
| AC4 | A required parameter with no value or default for UAT fails the health check. | SPEC-RWB-E1-042-007 | DIRECT | MSG-P3-032 names key and environment; service takes no traffic. | COVERED |
| AC5 | A value outside its range is refused with the minimum and maximum. | SPEC-RWB-E1-042-005 | DIRECT | 400 against 1..365; MSG-GEN-002. | COVERED |
| AC6 | A value of the wrong type is refused with the failed check. | SPEC-RWB-E1-042-005 | DIRECT | "ninety" against INTEGER; MSG-P1-002. | COVERED |
| AC7 | The author cannot approve their own value version. | SPEC-RWB-E1-042-006 | DIRECT | U-41 loads and approves version 3; MSG-P7-002. | COVERED |
| AC8 | SIT and PROD read their own values for the same key. | SPEC-RWB-E1-042-008 | DIRECT | Environment is part of the lookup key. | COVERED |
| AC9 | A secret is listed with owner, environments and used by, but no value. | SPEC-RWB-E1-042-009, SPEC-RWB-E1-042-012 | DIRECT | `ace.db.password`; `valueInForce` absent. | COVERED |
| AC10 | Rolling back version 2 returns version 1 and its value. | SPEC-RWB-E1-042-010 | DIRECT | Previous approved version becomes current. | COVERED |
| AC11 | A new value takes effect on its valid from date without a restart. | SPEC-RWB-E1-042-011 | DIRECT | Date-based resolution; cache refresh on `ParameterVersionApproved`. | COVERED |
| X1..X10 | Exceptional paths in the table below map to SPEC-003..011 and the access rule. | SPEC-RWB-E1-042-003..011 | DIRECT | Build failures, startup failure, range/type, author approval, secret, rollback, future version, access. | COVERED |

> **AC cleanup (4 November 2026):** the development-process criteria removed from story §7 are not mapped here. The remaining acceptance criteria are those in the current story.

## User story intent interpretation

As a **squad member (RW-TRIBE)**, I want **every environment setting and business parameter read from one configuration service and listed in a parameter catalog with name, type, default, owner, environment and where it is used**, so that **no value is hard-coded and every parameter has an owner**.

The story is a platform capability. It replaces constants and spreadsheet values with dated, approved rows, makes a value change a data load rather than a release, and puts two build checks in place so a hard-coded value or an uncatalogued key cannot merge. No business user sees a new screen in Epic 1.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Service start (catalog load and startup check); a reviewed catalog change on merge; a value load through `POST /admin/reference-loads` with `table=PARAMETER`. |
| Preconditions | RWB-E1-044 done; `config/parameter-catalog.csv` exists and is owned by RW-COE; the ACE secret store holds secrets per environment; loaders hold Reference data C; approvers hold Reference data A; the pipeline runs both build checks on every pull request. |
| Input | Catalog file, parameter value file (key, environment, value), `validFrom`, environment, caller identity. |
| Output | `parameter_catalog` and `parameter_value` rows; typed values with version; build findings; a `ParameterVersionApproved` outbox event. |
| Feature flag | `rwb.p3.configservice`. Off: services read defaults from generated keys only and value loads are refused. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `parameter_catalog` | `param_key` | Catalog CSV | Reviewed change only | Primary key; lower-case dotted key. |
| `parameter_catalog` | `kind`, `value_type`, `unit`, `min_value`, `max_value` | Catalog CSV | Reviewed change only | `value_type` drives the load check; range is inclusive. |
| `parameter_catalog` | `default_value` | Catalog CSV | Reviewed change only | Used only when no approved value exists and the parameter is not required. |
| `parameter_catalog` | `scope` | Catalog CSV | Reviewed change only | `PRODUCT` or `GLOBAL` (LOV-PARAM-SCOPE). |
| `parameter_catalog` | `required`, `owner_role`, `environments`, `used_by`, `secret` | Catalog CSV | Reviewed change only | Owner role is mandatory; a secret never carries a value. |
| `parameter_value` | `param_value` | Load file | New version only | Type and range checked; never updated in place. |
| `parameter_value` | `environment`, `product_group` | Load file | New version only | Environment in LOV-ENVIRONMENT; product group in LOV-PRODUCT when present. |
| `parameter_value` | `version_no`, `valid_from`, `valid_to`, `status` | Service | System-managed | Version rises by one per key/environment/product; status VALIDATED, APPROVED, ROLLED_BACK. |
| `parameter_value` | `author_user_id`, `approver_user_id`, `approved_at` | Session | System-managed | Approver must differ from author. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | Load | Every check passes | VALIDATED | Version row written; no value served yet. |
| None | Load | Any check fails | Not written | Load refused in full; previous value stays. |
| VALIDATED | Approve | Approver present, not author, holds the right | APPROVED | In force from `valid_from`; `ParameterVersionApproved` published. |
| APPROVED | Valid from reached | Date reached | In force (derived) | Reads for that date return the new value and version; no restart. |
| APPROVED | Rollback | An earlier approved version exists | ROLLED_BACK | Earlier version served again. |

This story changes no case status.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Code holds a literal business value | Build fails naming file, line and parameter | Build output |
| X2 | Code reads an uncatalogued key | Build fails naming the key | Build output |
| X3 | Required parameter missing at start-up | Health check fails; no traffic | MSG-P3-032 |
| X4 | Value outside range | Load refused in full | MSG-GEN-002 |
| X5 | Wrong type | Load refused in full | MSG-P1-002 |
| X6 | Approver is the author | Approval refused | MSG-P7-002 |
| X7 | Secret requested through the read | No value returned | None |
| X8 | Rollback with no earlier version | Refused; current value stays | MSG-P3-015 |
| X9 | Role without Rules and parameters R reads the catalog | 403; nothing returned | MSG-P4-002 |
| X10 | New version approved before its valid from | Current value stays until that date | None |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| Endpoints delivered | `GET /api/recovery/v1/admin/parameters` (API-P3-018); `POST /api/recovery/v1/admin/reference-loads` with `table=PARAMETER`; `POST /api/recovery/v1/admin/reference-loads/{loadId}/approve`; `POST /api/recovery/v1/admin/reference-loads/{loadId}/rollback`. |
| Contract delta | None against API Specification v2. `Parameter` already carries key, kind, type, unit, min, max, default, scope, required, owner, environments, usedBy, secret, valueInForce, versionNo and validFrom. `valueInForce` is absent for a secret. |
| Backward compatibility | Additive; existing endpoints unchanged. |
| Authorization | Rules and parameters R for the read; Reference data C for load; Reference data A for approve; Reference data U for rollback. 401 MSG-P4-001; 403 MSG-P4-002; 409 MSG-P7-002/MSG-P3-015; 422 MSG-GEN-001/MSG-GEN-002/MSG-P1-002; 503. |
| Versioning | No API version change; the OpenAPI file is unchanged. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change; SCR-39 is Epic 8. | Existing frontend tests remain green. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-020; SPEC-RWB-E1-042-001..014 | New service, repositories, load checks, startup indicator, controller and two build tools. | Positive, negative, boundary and error-path tests: typed read, environment/date resolution, range/type, author approval, secret, rollback, future version, missing required, both build checks. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `ParameterService` | Published interface | Typed read by key, environment, product group and business date; returns value, version and valid from; cache refresh on `ParameterVersionApproved`. |
| `ParameterCatalogRepository` / `ParameterValueRepository` | Repository | Read and write `parameter_catalog` and `parameter_value`. |
| `ParameterLoadChecks` | Service | Key in catalog, type, range, environment and required checks for table `PARAMETER`; refuses the load whole. |
| `ParameterLoadHandler` | Service | Handler behind the reference-load endpoint; approve and rollback. |
| `ParameterCatalogController` | Controller | `GET /admin/parameters`, secrets omitted. |
| `ParameterStartupCheck` | Service | Health indicator that fails when a required value is missing for the environment. |
| `ParameterKeysGenerator` | Build tool | Generates `ParameterKeys` from the catalog file. |
| `RwbMagicNumberCheck` | Build tool | Fails on numeric and string business literals in recovery packages; allows 0, 1, -1 and test code; names the catalog key whose default equals the literal. |
| `CatalogCompletenessCheck` | Build tool | Compares keys read through `ParameterService` with the catalog; fails on a missing key, owner or default. |

### Package and boundaries

`recovery.casewf.config` holds the implementation; published types in `recovery.casewf.config.api`;
build checks in `build-tools/rwb-checks`. Other modules read values only through `ParameterService`.
No module reads `parameter_catalog` or `parameter_value` directly.

### Data and migration

- `V042_1__parameter_catalog.sql` creates `parameter_catalog` (`param_key` primary key, kind,
  value_type, unit, min_value, max_value, default_value, scope, required, owner_role, environments,
  used_by, secret, description, standard columns) and `parameter_value` (id, param_key FK, environment,
  param_value, product_group, version_no, valid_from, valid_to, status, author_user_id,
  approver_user_id, approved_at, standard columns; unique (param_key, environment, product_group,
  version_no); index (param_key, environment, valid_from) where status = 'APPROVED').
- `V042_2__parameter_seed.sql` is generated from the catalog file and loads the defaults. Schema names
  come from the Flyway `${schema}` placeholder (RWB-E1-044).
- `case.entry.dpd` default 90 (DL16), `refdata.cache.ttl-seconds` default 300 (DL11) and
  `caselist.export.maxrows` default 10000 (DL11) are Epic 1 entries.
- `config.cache.ttl-seconds` = 60 (assumed; DL11) is the configuration service's own cache TTL and is a
  separate catalog entry from the reference data cache TTL.

### Resolution and cache

- Lookup key: `param_key`, `environment`, `product_group` (null for GLOBAL) and business date.
- The value is the approved version with the latest `valid_from` on or before the business date.
- The product-group overload performs an exact product row match; the source defines no implicit
  fallback to a GLOBAL row, so a missing product row is an error.
- The cache is keyed by parameter, environment and product group; it refreshes on
  `ParameterVersionApproved` and at the latest after `config.cache.ttl-seconds`.
- The five product business parameters of RWB-E1-045 are defined in the catalog with scope PRODUCT but
  their values are `PRODUCT_PARAMETER` rows read through `ProductParameterService`; E1-045 is
  authoritative for those values.

### Transaction and events

A load writes the version and its values in one transaction. Approval writes status, approver and
`approved_at`, and sets the replaced version's `valid_to` to the day before the new `valid_from`.
`ParameterVersionApproved` (paramKeys, versionNo, validFrom) is written to the outbox in the same
transaction; the publisher delivers it with retry and idempotency.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-COE | Reference data CRUD; Rules and parameters CRUD | All |
| RW-RISK | Reference data A where a threshold or limit moves (assumed; DL01) | All |
| RW-PLATADM | Rules and parameters R; owns environment settings | All |
| RW-TRIBE | Adds catalog entries through reviewed pull requests | All |
| Every role with Rules and parameters R | Read the catalog | Per scope |
| RW-PHONECOL | No Rules and parameters right | Refused |

### Observability and operations

- Build output names file, line and key for both checks.
- Load response returns status, row count and each failed check.
- Startup log names the missing key and environment; readiness stays false.
- Metrics: loads, refusals by check, approvals, rollbacks, cache refreshes, missing-required alarms.
- Audit: author, approver, load and approval times in `parameter_value`; the approval also writes a
  decision log entry through the P4 pattern (RWB-E1-043).

### Performance

- Reads are cached; a cache hit is in-memory. A miss is one indexed query.
- The catalog is small (Epic 1 tens of rows); no pagination is needed for the read.
- Build checks run once per pull request, not at run time.

### Feature flag and rollback

- `rwb.p3.configservice`: off means defaults from generated keys only and value loads refused.
- Rollback: turn the flag off and redeploy the previous tag; the tables remain and are harmless. A
  value rollback is a data action, not a deployment.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-042-01 | AC1, BR1 | System | `case.entry.dpd` version 1 = 90 | Entry uses 90; decision records version 1 |
| TC-E1-042-02 | BR1 | Unit | Fixture with literal 90 | Build fails naming file, line and key |
| TC-E1-042-03 | BR2 | Unit | Fixture reading `allocation.retry.limit` | Build fails naming the key |
| TC-E1-042-04 | AC4, BR7 | System | UAT without `refdata.cache.ttl-seconds` | Readiness false; MSG-P3-032 |
| TC-E1-042-05 | AC5, BR3 | System | 400 against 1..365 | Refused; MSG-GEN-002 |
| TC-E1-042-06 | AC6, BR3 | System | "ninety" | Refused; MSG-P1-002 |
| TC-E1-042-07 | AC7, BR4 | System | U-41 loads and approves | Refused; MSG-P7-002 |
| TC-E1-042-08 | AC8 | System | 30 in SIT, 300 in PROD | Each environment returns its own value |
| TC-E1-042-09 | AC9, BR6 | System | `ace.db.password` | Listed; no value returned |
| TC-E1-042-10 | AC10, BR3 | System | Versions 1 and 2 | Version 1 served; 90 |
| TC-E1-042-11 | AC11, BR5 | System | Version 2 = 91 from 2026-12-10 | 90 on 09th, 91 on 10th; no restart |
| TC-E1-042-12 | X9 | Security | RW-PHONECOL calls the read | 403; MSG-P4-002 |
| TC-E1-042-13 | BR1, BR2 | Unit | Key read outside the catalog | Completeness check fails |

## Guardrails and out of scope

- No business value in code; the build check enforces it. No personal data or secret value in
  parameters, logs, tests or responses.
- Other modules read values only through `ParameterService`.
- Out of scope: the reference data service for other tables (RWB-E1-043), product parameters and
  service levels (RWB-E1-045), dated feature flags (FEAT-CWC-26), the administration screen (Epic 8)
  and the change checklist/audit report (RWB-E1-048).

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | §3, §13; SPEC-011 | Are `refdata.cache.ttl-seconds` (300) and `config.cache.ttl-seconds` (60) the same setting? | Two caches or one; affects refresh behaviour. | Two settings: one for reference data reads, one for the configuration service's own cache. Both are catalog entries. | RESOLVED | SPEC-011 |
| CLAR-002 | BR4; SPEC-006 | Who approves a parameter that is not a threshold? | Determines the approver role. | The parameter owner approves; RW-RISK approves where a threshold or limit moves (assumed grant; DL01). | RESOLVED | SPEC-006 |
| CLAR-003 | Contract; SPEC-012 | Is `GET /admin/parameters` new? | A contract delta would need an OpenAPI change. | It is new to the delivered surface but already defined as API-P3-018 in API Specification v2. No OpenAPI delta, no version bump. | RESOLVED | SPEC-012 |
| CLAR-004 | Contract; SPEC-002 | Does the product-group overload replace RWB-E1-045's `ProductParameterService`? | Two services could read different stores. | No. E1-045 is authoritative for the five product business parameters; the overload is for product-scoped configuration rows and has no Epic 1 caller. | RESOLVED | SPEC-002 |
| CLAR-005 | BR6, AC9; SPEC-009 | Where is a secret value held? | Determines whether the table can be read safely. | Only in the ACE secret store; the catalog lists the key, owner and environments. | RESOLVED | SPEC-009 |
| CLAR-006 | §13; SPEC-001 | Is the CSV or the database the source of truth for catalog definitions? | Affects review and deployment. | The CSV is reviewed in the repository; the generated migration loads it. A change needs a reviewed pull request. | RESOLVED | SPEC-001 |
| CLAR-007 | AC4; SPEC-007 | What does "takes no traffic" mean? | Startup behaviour. | The readiness probe fails and the load balancer sends no traffic; the process may stay up for diagnosis. | RESOLVED | SPEC-007 |
| CLAR-008 | SPEC-004 | Which literals are allowed? | The check would fail legitimate code. | 0, 1, -1 and test code; everything else must be a catalog key. | RESOLVED | SPEC-004 |

`CLARIFICATION_STATUS: RESOLVED` — all 8 items are answered from the story, the architecture or the
decision log. The two assumed grants are recorded as Low findings, not as open behaviour.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend configuration story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New configuration service and parameter catalog; four administration endpoints delivered from the existing v2 contract; no screen.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: first delivery of API-P3-018 and the PARAMETER load handler with no OpenAPI delta]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 9 acceptance criteria, 10 exception paths and 5 value states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

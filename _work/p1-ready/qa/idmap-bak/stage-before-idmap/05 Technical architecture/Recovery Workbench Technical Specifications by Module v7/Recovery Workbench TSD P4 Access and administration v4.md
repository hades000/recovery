SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench P4 Access and administration

Technical specification. SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD P4 Access and administration |
| Document ID | P4-RWB-TSD-v4 |
| Version | 4 |
| Status | Draft |
| Date | 22 November 2026 |
| Supersedes | Version 3, 16 November 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads (GAP-1999; ASM-3225: no squad is named per service) |
| Decision | D-RCV-60 microservice realignment |
| Status note | Draft: no approval of version 4 is recorded (GAP-1998; ASM-3217) |
| Change | 4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD P4 Access and administration | FSD | Pair |
| Recovery Workbench Target Architecture | Architecture | Parent |
| Recovery Workbench Logical Data Model and Data Dictionary | Data | Source of T3 |
| Recovery Workbench API Specification | API | Source of appendix T-A |
| Recovery Workbench Architecture Decision Records | ADR | ADR-011 Temporal; ADR-012 Drools |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every table, endpoint, event, workflow and job in T0 and T5.2 |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit, PII and SOC logging | REUSE | ACE common module | Called through the published interface |
| Scheduler and batch | REUSE | ACE pattern: Quartz and Spring Batch | Jobs in the Batch and Scheduling Design |
| Outbox and retry | REUSE | Error Handling and Resilience Standard | Through P2 |
| Rules evaluation | NEW | Rules Engine Design | Embedded Drools from versioned rule packages (ADR-012) |
| Workflow engine | NEW | Workflow Engine Design | Temporal, self-hosted; case workflows from Epic 3 (ADR-011) |

Under D-RCV-60 the scheduler and batch row is delivered by the Temporal layer (ADR-016): Temporal Schedules and event-started workflows in the owning service replace the Quartz and Spring Batch jobs (DP-10). The outbox and retry row is delivered by the Kafka outbox, inbox and retry topics (ADR-015; DP-09).

## T0. Service

P4 Access and administration is one of the 19 services of Architecture v5: `rwb-access` (service name Access and authority, module P4, wave 1, service epic `RWB-SVC-P4`). Version 4 adds this section so that the specification is read as the specification of one service: its identity, what it owns, and the decoupling patterns that replace the monolith's in-process calls. Every owner is taken from Microservice Ownership Map v1 and every identifier from Template and Rules R4 (ADR-013, ADR-014).

P4 is the authorisation provider for all 19 services: the authorise contract and the guard library replace the monolith's in-process access check (DP-08).

### T0.1 Service identity

| Item | Value |
|---|---|
| Module | P4 Access and administration |
| Service | `rwb-access` (Access and authority) |
| Service epic | `RWB-SVC-P4` |
| Wave | 1 |
| Schema | `rwb_access` |
| Database login | `rwb_access`: one login per service, with its own connection pool cap |
| REST base | `/api/recovery/access/v1` |
| Kafka topic | `rwb.access.events.v1`, with `.retry` and `.dlt` topics |
| Event names | `rwb.access.<Event>.v1`, CloudEvents 1.0 in binary mode, key `caseId` |
| Temporal | namespace `rwb-recovery`; task queue `rwb-access` |
| Java package | `th.co.scb.ace.workbench.recovery.access` |
| Edge | gateway-bff for the staff screens of this service |
| Contract artefacts | `05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml`; `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-access.asyncapi.yaml` |
| Suggested owner, app development | TechX (suggested; any team may pick up this story) |
| Suggested owner, ACE DB | ACE team (suggested; any team may pick up this story) |

### T0.2 What this service owns

Architecture v5 slide 41 gives this service: Recovery roles as data, scope, masking policy, DoA table, access log. Table T0.2 states the same ownership in the form the Ownership Map uses, with the counts this specification carries. A table that the map assigns to another service is not built here, whatever T3 says (see the note under T3).

| Area | Owner and artefact | Count |
|---|---|---|
| Business tables in `rwb_access` | `delegation_limit`, `masking_rule`, `permission`, `role`, `role_conflict` | 5 |
| REST operations | appendix T-A and `rwb-access.yaml` | 4 |
| Events published | AccessPolicyChanged, DoaLimitChanged | 2 |
| Workflows and schedules | none in the Ownership Map sheet; T5.2.1 names Access review list (six-monthly) | 1 |
| Jobs | JOB-18 | 1 |

### T0.3 Decoupling patterns applied

The left column is the pattern of Template and Rules R5.5; the middle column quotes the line of this specification that carries the legacy marker, where one is present; the right column is what replaces it in this service.

| DP | Legacy marker in this specification | How the service lands it |
|---|---|---|
| DP-01 | — | Owns its tables in `rwb_access`; no other service reads them (ADR-014). |
| DP-02 | — | One login, `rwb_access`, with its own connection pool cap. |
| DP-03 | `…on events from P3 and writes through the decision log.` | Local decision record plus DecisionRecorded (EV-08) on `rwb.decision-record.v1`. |
| DP-04 | `…delegation of authority table, access log, the rule package store and the workflow administration surface.…` | Embedded Drools kit; rule packages from `rwb-decision` (C RWB-P7-E1073-CON; ADR-017). |
| DP-06 | `Role / Rules and parameters / Reference data / Platform administration` | Parameters from the `rwb-case` contract and the client library (H RWB-PLT-E1042-CON). |
| DP-07 | `DF-REF-037 / role_class / LOV / varchar(15) / Yes / LOV-ROLE-CLASS / Workbench` | Reference data and lists of values from the `rwb-case` contract (H RWB-PLT-E1043-CON). |
| DP-08 | `…Temporal Web UI uses the same Entra roles: RW-PLATADM operates, RW-AUDIT reads and RW-SECADM decodes…` | Authorisation through the `rwb-access` authorise contract and the guard library (H RWB-PLT-E1037-CON). |
| DP-09 | `…state machine of its own; the module acts on events from P3 and writes through the decision…` | Outbox and inbox library; CloudEvents on `rwb.access.events.v1` with retry topics and `.dlt`. |
| DP-10 | `Scheduler and batch / REUSE / ACE pattern: Quartz and Spring Batch / Jobs in the Batch and…` | Temporal Schedules and event-started workflows through the workflow kit (ADR-016). |
| DP-11 | `…reaches other modules only through their published interfaces and other systems only through COLLINS,…` | One REST hop, 2 s timeout, breaker; the consumer builds against the provider's fake (ADR-020). |
| DP-12 | `…Workflow Engine Design / Temporal, self-hosted; case workflows from Epic 3 (ADR-011)` | CaseWorkflow parent with a child workflow per stage. |
| DP-13 | `API-P4-004 / GET / /api/recovery/v1/admin/lists/{listCode} / Reference data…` | REST base `/api/recovery/access/v1`. |
| DP-14 | `…through WorkflowGateway; returns 404 when rwb.p3.temporal is off` | Topic `rwb.access.events.v1`, retry topics and `.dlt`; naming library (H RWB-PLT-E1047-CON). |
| DP-15 | — | Per-service Flyway sequence in `rwb_access`. |
| DP-17 | `…the case store, the document store and the data lake copy is logged. / Every read / Proposed` | No data lake: reporting reads events; the lake copy is removed (ADR-018). |
| DP-19 | `…at rest in the case store, and on every screen and every agent call, by role. / Masked…` | Screens composed by gateway-bff; one composite route per screen (H RWB-PLT-N001-CON). |

### T0.4 What this service is not

- It holds no other service's table and no ACE table beyond the read-only `recovery.v_ace_*` views (DP-01, DP-05).
- It runs no shared Quartz job and touches no ACE batch table (DP-10; ADR-016).
- It holds no partner user and no reference data: partner users are S9's and reference data is P3's (DP-07).
- It is not a monolith module: the published Java interface of T2 is replaced by the contract set of T5.2 (DP-11; ADR-020).

## T1. Architecture overview

P4 Access and administration is delivered as the service `rwb-access` (module P4, wave 1, service epic `RWB-SVC-P4`): one repository, one pipeline, one schema `rwb_access` with one login, behind gateway-bff (ADR-013, ADR-014). It covers: roles, permissions, scope, masking, delegation of authority table, access log, the rule package store and the workflow administration surface. The rule package store is the four tables rule_package, rule_package_version, rule_row and rule_test_case, which the Ownership Map places in `rwb-decision` (ADR-012; GAP-1993); the workflow administration surface runs the platform smoke workflow and decodes payloads under break-glass (ADR-011). It reaches other modules only through the contracts of T5.2 and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| AccessAndAdministrationController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| AccessAndAdministrationService | Business logic; calls RuleEvaluator where a rule decides an administrative change; writes the decision log entry before any change |
| AccessAndAdministrationRepository | Reads and writes the module's tables only |
| RulePackageStore | Reads rule_package, rule_package_version, rule_row and rule_test_case from P7's contract; the four tables are the P7 registry (Ownership Map; Architecture v5 slide 41; GAP-1993) |
| RulePackageAuditService | Builds the change report and links each package version to the decisions it made |
| WorkflowAdminService | Runs PlatformSmokeWorkflow through WorkflowGateway; returns 404 when rwb.p3.temporal is off |
| Jobs | Temporal Schedules and event-started workflows this service owns (T0.2, T5.2.1; DP-10) |
| Published interface | The contracts of T5.2: REST operations, events and workflows other services call; no table is read across modules (DP-11) |

The published interface of this table is the contract set of T5.2: the REST operations, the events and the workflows, not a Java interface in a shared classpath (DP-11; ADR-020). Components that the Ownership Map places in another service are stated in T0.2 and T5.2 and are built by that service. T2 of version 3 describes the rule package store; the registry tables are P7's and P4 reads them through the contract of T5.2.2 (GAP-1993).

## T3. Data model

Every object of T3 that Microservice Ownership Map v1 assigns to `rwb-access` lives in schema `rwb_access` with the standard columns of T3.0 (DP-01, DP-15; ADR-014). T3.1 names three objects that the Ownership Map v1 places elsewhere: `lov_value` is P3's reference data (DP-07), `partner_user` is S9's (Ownership Map ruling `partner_user`, ASM-0072), and `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7's registry (GAP-1993). `delegation_limit` stays here (Ownership Map ruling `delegation_limit`, ASM-0070).

### T3.0 Standard record columns

| Column | Type | Meaning |
|---|---|---|
| is_active | boolean | The active or inactive status of the record |
| state | varchar(40) | Record lifecycle state |
| version | integer | Optimistic lock version |
| created_at | timestamptz | When the record was created |
| created_by | uuid | Who or which service identity created it |
| updated_at | timestamptz | When the record last changed |
| updated_by | uuid | Who or which service identity last changed it |

### T3.1 Object and field definitions

**role** (EXTEND ACE RBAC). A Workbench role, held as data.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-034 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-035 | role_code | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-036 | role_name | TEXT | varchar(80) | Yes | None | Workbench |
| DF-REF-037 | role_class | LOV | varchar(15) | Yes | LOV-ROLE-CLASS | Workbench |
| DF-REF-038 | default_scope | LOV | varchar(8) | Yes | LOV-SCOPE | Workbench |
| DF-REF-039 | entra_group | TEXT | varchar(120) | No | None | Entra ID |

**permission** (EXTEND ACE RBAC). What a role may do in one capability area.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-040 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-041 | role_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-REF-042 | capability_area | LOV | varchar(30) | Yes | LOV-CAPABILITY | Workbench |
| DF-REF-043 | letters | TEXT | varchar(5) | Yes | None | Workbench |
| DF-REF-044 | matrix_version | TEXT | varchar(20) | Yes | None | Workbench |

**delegation_limit** (NEW). An approval limit by decision, level, product and amount.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-016 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-017 | decision_code | LOV | varchar(8) | Yes | LOV-DECISION | Workbench |
| DF-REF-018 | approval_level | LOV | varchar(4) | Yes | LOV-APPROVAL-LEVEL | Workbench |
| DF-REF-019 | product_group | LOV | varchar(15) | Yes | LOV-PRODUCT | Workbench |
| DF-REF-020 | principal_limit | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-REF-021 | loss_pct_limit | NUMBER | numeric(5,2) | No | None | Workbench |
| DF-REF-022 | min_price_pct_fmv | NUMBER | numeric(5,2) | No | None | Workbench |
| DF-REF-023 | holder_user_id | USER_REF | uuid | No | None | Workbench |
| DF-REF-024 | substitute_user_id | USER_REF | uuid | No | None | Workbench |
| DF-REF-025 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-026 | valid_to | DATE | date | No | None | Workbench |
| DF-REF-055 | limit_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-056 | regulation_item | TEXT | varchar(10) | Yes | None | Workbench |
| DF-REF-057 | applies_when | TEXT | varchar(40) | No | None | Workbench |
| DF-REF-058 | max_loss_amount | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-REF-059 | max_delay_count | NUMBER | integer | No | None | Workbench |
| DF-REF-060 | min_price_pct_principal | NUMBER | numeric(5,2) | No | None | Workbench |
| DF-REF-061 | min_received_pct | NUMBER | numeric(5,2) | No | None | Workbench |
| DF-REF-062 | max_term_years | NUMBER | numeric(4,1) | No | None | Workbench |

**lov_value** (NEW; P3's table, field rows kept for the T3 trace). A value in a list of values.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-027 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-028 | lov_code | TEXT | varchar(30) | Yes | None | Workbench |
| DF-REF-029 | value_code | TEXT | varchar(30) | Yes | None | Workbench |
| DF-REF-030 | label_en | TEXT | varchar(120) | Yes | None | Workbench |
| DF-REF-031 | label_th | TEXT | varchar(120) | No | None | Workbench |
| DF-REF-032 | sort_order | NUMBER | integer | Yes | None | Workbench |
| DF-REF-033 | valid_from | DATE | date | Yes | None | Workbench |

Version 3 gives P4 the four rule tables rule_package, rule_package_version, rule_row and rule_test_case; the Ownership Map places them in `rwb-decision` and Architecture v5 slide 41 gives P7 the DMN model registry, so they are built there (GAP-1993). The field rows stay here for the trace of T3. They replace the single rule_row and rule_version pair of the earlier design: a rule now belongs to a package version, and a package version is approved as a whole.

**rule_package** (NEW). One rule package: a named decision table with an owner role and a hit policy.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-274 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-275 | package_code | TEXT | varchar(30) | Yes | None | Workbench |
| DF-REF-276 | title | TEXT | varchar(120) | Yes | None | Workbench |
| DF-REF-277 | owner_role | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-REF-278 | hit_policy | TEXT | varchar(20) | Yes | None | Workbench |

**rule_package_version** (NEW). One version of a rule package: the uploaded workbook, the generated DRL, the checksum, the approval and the change checklist.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-279 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-280 | package_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-REF-281 | version_label | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-282 | status | LOV | varchar(15) | Yes | LOV-VERSION-STATUS | Workbench |
| DF-REF-283 | source_blob_ref | TEXT | varchar(200) | Yes | None | Workbench |
| DF-REF-284 | drl_source | TEXT | text | Yes | None | Workbench |
| DF-REF-285 | checksum | TEXT | char(64) | Yes | None | Workbench |
| DF-REF-286 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-287 | valid_to | DATE | date | No | None | Workbench |
| DF-REF-288 | author | USER_REF | uuid | Yes | None | Workbench |
| DF-REF-289 | approver | USER_REF | uuid | No | None | Workbench |
| DF-REF-290 | loaded_at | DATE | timestamptz | Yes | None | Workbench |
| DF-REF-291 | approved_at | DATE | timestamptz | No | None | Workbench |
| DF-REF-292 | test_result | LOV | varchar(10) | No | LOV-TEST-RESULT | Workbench |
| DF-REF-293 | dry_run_counts | TEXT | jsonb | No | None | Workbench |
| DF-REF-294 | rollback_of | CROSS_REF | uuid | No | None | Workbench |
| DF-REF-295 | change_checklist | TEXT | jsonb | No | None | Workbench |

**rule_row** (NEW). One rule of a package version: the parsed, queryable copy of a decision-table row. Stories read action_text, owner_role, timer_spec and target_queue_code from the catalog by rule ID and package version; they do not read the package source.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-002 | rule_id | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-003 | rule_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-004 | route_set | LOV | varchar(15) | Yes | LOV-ROUTE-SET | Workbench |
| DF-REF-005 | from_state | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-006 | event_code | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-007 | condition_expr | TEXT | varchar(1000) | No | None | Workbench |
| DF-REF-008 | action_text | TEXT | varchar(1000) | Yes | None | Workbench |
| DF-REF-009 | to_state | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-010 | owner_role | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-REF-011 | timer_spec | TEXT | varchar(60) | No | None | Workbench |
| DF-REF-012 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-013 | valid_to | DATE | date | No | None | Workbench |
| DF-REF-014 | approved_by | USER_REF | uuid | Yes | None | Workbench |
| DF-REF-015 | test_case_id | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-052 | rule_table | LOV | varchar(15) | No | LOV-RULE-TABLE | Workbench |
| DF-REF-053 | row_order | NUMBER | integer | No | None | Workbench |
| DF-REF-054 | target_queue_code | TEXT | varchar(30) | No | None | Workbench |
| DF-REF-296 | package_version_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-REF-297 | drools_rule_name | TEXT | varchar(40) | Yes | None | Workbench |
| DF-REF-298 | outputs | TEXT | jsonb | No | None | Workbench |

**rule_test_case** (NEW; P7's table, field row kept for the T3 trace). One scenario of a rule package version, with its expected and actual result. The field table is in TSD P3 T3.1; this release adds one field:

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-299 | package_version_id | CROSS_REF | uuid | No | None | Workbench |

**masking_rule** (NEW). Which role sees which personal data field unmasked, by version.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-198 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-199 | role_code | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-REF-200 | field_id | TEXT | varchar(16) | Yes | None | Workbench |
| DF-REF-201 | unmasked | BOOLEAN | boolean | Yes | None | Workbench |
| DF-REF-202 | masking_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-203 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-204 | valid_to | DATE | date | No | None | Workbench |

**role_conflict** (NEW). A pair of roles one person may not hold together, by version.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-205 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-206 | role_code | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-REF-207 | conflicts_with | TEXT | varchar(30) | Yes | None | Workbench |
| DF-REF-208 | reason | TEXT | varchar(200) | Yes | None | Workbench |
| DF-REF-209 | conflict_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-210 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-211 | valid_to | DATE | date | No | None | Workbench |

**partner_user** (NEW; S9's table, field rows kept for the T3 trace). A partner user's identity bound to one partner firm and one partner role.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-212 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-213 | identity_ref | TEXT | varchar(64) | Yes | None | Workbench |
| DF-REF-214 | partner_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-REF-215 | role_code | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-REF-216 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-217 | valid_to | DATE | date | No | None | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-APPROVAL-LEVEL | L1, L2, L3, L4, L5, L6 |
| LOV-CAPABILITY | CASE_RECORD, QUEUE_AND_ALLOCATION, TREATMENT_AND_OFFER, LITIGATION, ASSET_AND_DISPOSAL, DEBT_SALE, WRITE_OFF_AND_POSTING, DOCUMENTS, RULES_AND_PARAMETERS, REFERENCE_DATA, DECISION_LOG, PARTNER_PORTAL, REPORTING, PLATFORM_ADMINISTRATION |
| LOV-PRODUCT | MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED |
| LOV-ROLE-CLASS | BANK_USER, PARTNER_USER, NON_HUMAN_ACTOR |
| LOV-ROUTE-SET | RESTRUCTURE, SETTLEMENT, DEED_IN_LIEU, GUARANTEE_CLAIM, LITIGATION, ASSET_DISPOSAL, DEBT_SALE, WRITE_OFF, DEVIATIONS, UNIVERSAL_RULES |
| LOV-RULE-TABLE | ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER |
| LOV-SCOPE | OWN, TEAM, REGION, ALL |
| LOV-VERSION-STATUS | LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| permission | role_id | role | Many to 1 |
| rule_package_version | package_id | rule_package | Many to 1 |
| rule_row | package_version_id | rule_package_version | Many to 1 |
| rule_test_case | package_version_id | rule_package_version | Many to 0 or 1 |
| partner_user | partner_id | partner | Many to 1 |

## T4. State machines and workflow

No case state machine of its own; the module acts on events from P3 and writes through the decision log.

A rule package version has its own lifecycle: LOADED on a passed load, APPROVED by a second person, IN_FORCE from its valid-from date, then SUPERSEDED by the next version or ROLLED_BACK by one call. A load that fails any check is REFUSED and is never in force.

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-21 | Entra ID and the bank IAM | In | ACE sign-in | At each sign-in |
| INT-22 | PII Kafka, audit and SOC logs | Out | ACE logging | As they happen |

### T5.2 Contracts

Version 4 states every cross-module dependency of this module as a contract, so that the service is built against a published artefact and its fake (ADR-020; DP-11). The artefact per call type is: OpenAPI 3.1 for REST, AsyncAPI 3.0 for Kafka, the Temporal interface named here for a workflow or activity, the Interface Specifications manifest for a file, the Nexus operation for the ACE restructure calculator, and a grant on the view for SQL. No row of this section reads another service's table (DP-01). Every consumed contract is class C (Template and Rules R5.4): it never blocks the build, because the consumer builds against the fake, and the real cross-service behaviour is class I work on an integration story. Architecture v5 slides 13 to 20 name a few operations differently from the published files of 22 November 2026; the published file is the artefact the fake is generated from and is the one cited here (GAP-1997; ASM-3224).

#### T5.2.1 Contracts provided

The REST operations of this service are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml` (5.0.0, 22 November 2026) under the base `/api/recovery/access/v1`. Appendix T-A holds the endpoint IDs, the access right and the first release of each one.

| # | Method | Path | operationId |
|---|---|---|---|
| 1 | GET | `/admin/roles` | `getAdminRoles` |
| 2 | GET | `/admin/access-log` | `getAdminAccessLog` |
| 3 | GET | `/me/session` | `getMeSession` |
| 4 | POST | `/admin/break-glass-grants` | `postAdminBreakGlassGrants` |

Workflows, schedules, files and views this service provides:

| Contract | Type | Called by or target | Note |
|---|---|---|---|
| Access review list (six-monthly) | Temporal Schedule | P4 rwb-access | JOB-18 (DP-10) |

Events this service publishes (AsyncAPI 3.0, CloudEvents 1.0):

| Event | EV | Topic | Consumers |
|---|---|---|---|
| AccessPolicyChanged | — | `rwb.access.events.v1` | all (cache refresh) |
| DoaLimitChanged | — | `rwb.access.events.v1` | all (cache refresh) |

#### T5.2.2 Contracts consumed

| Contract | Type | Provider | Class | Failure path |
|---|---|---|---|---|
| Sign-in and group-to-role mapping (Entra ID) | REST | ACE Common | X | Tracked only; outside the Workbench; class X |

Events this service consumes:

None.

#### T5.2.3 Call-type summary

| Call type | Provided | Consumed | Artefact |
|---|---|---|---|
| REST | 4 | 1 | OpenAPI 3.1, one file per service |
| Kafka (events) | 2 | 0 | AsyncAPI 3.0, one file per service |
| Temporal | 1 | 0 | Workflow and activity interfaces, queue `rwb-access` |
| File | 0 | 0 | Interface Specifications manifest and the SAS link |
| Nexus | 0 | 0 | Nexus operation into ACE |
| SQL | 0 | 0 | Read-only grant on the view |

A contract change is a new version of the artefact, never a code change in the consumer (ADR-020). The provider named in T5.2.2 is the owner in Microservice Ownership Map v1, and the consumer list of each event is the Arch v5 event catalogue on slides 42 and 43.

### T5.3 Events

The event contract of this service is `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-access.asyncapi.yaml`; the shared decision-record contract is `asyncapi/rwb.decision-record.v1.asyncapi.yaml`. Every service publishes DecisionRecorded (EV-08) to `rwb.decision-record.v1` from its outbox in the same transaction as its state change (DP-03, DP-09; ADR-015, ADR-022); consuming services dedupe through their inbox table. Events carry identifiers and facts, never personal data (Event and Messaging Design v4, sheet Rules).

| Event | EV | Direction | Topic |
|---|---|---|---|
| AccessPolicyChanged | — | Published | `rwb.access.events.v1` |
| DoaLimitChanged | — | Published | `rwb.access.events.v1` |

An event shown with `—` has no number in the numbered catalogue: the Arch v5 catalogue calls these rows `+`, so the number is not specified in the source documents (GAP-1996; ASM-3223).

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Rules and parameters | Reference data | Platform administration |
|---|---|---|---|
| RW-CASEOWN Case owner | R | R | - |
| RW-TEAMMGR Team manager | R | R | - |
| RW-PHONECOL Phone collector | - | R | - |
| RW-FIELDCOL Field collector | - | R | - |
| RW-RESTRUCT Restructuring officer (FCR) | R | R | - |
| RW-SPECIAL Hardship and vulnerability specialist | R | R | - |
| RW-COMPLAIN Complaint officer | R | R | - |
| RW-FRAUD Fraud investigator | R | R | - |
| RW-LITOFF Litigation officer | R | R | - |
| RW-ENFORCE Enforcement owner | R | R | - |
| RW-LEGAL Legal counsel | R | RU | - |
| RW-SALEOFF Sale officer | R | R | - |
| RW-NPAMGR NPA and asset manager | R | R | - |
| RW-DEBTSALE Debt sale officer | R | R | - |
| RW-WRITEOFF Write-off team member | R | R | - |
| RW-CREDITAD Credit Administration officer | R | R | - |
| RW-GUARANT Guarantee officer | R | R | - |
| RW-AGENCYMG Partner and agency manager | R | RU | - |
| RW-CONDUCT Conduct and QA officer | R | R | - |
| RW-CAPACITY Capacity and workforce planner | R | R | - |
| RW-PRODHEAD Product head (Mortgage, HP, SSME) | R | R | - |
| RW-HEADLIT Head of Litigation | R | R | - |
| RW-HEADNPA Head of NPA | R | R | - |
| RW-HEADASL Head of Asset Liquidity | R | R | - |
| RW-CREDCOMM Credit approval committee member | R | R | - |
| RW-WOCOMM Write-off committee member | R | R | - |
| RW-RISK Risk and model risk officer | RA | R | - |
| RW-COE Center of excellence analyst | CRUD | CRUD | R |
| RW-DATASTEW Data steward and data product owner | R | RU | R |
| RW-FINANCE Finance and CFO delegate | R | R | - |
| RW-AUDIT Internal audit | R | R | R |
| RW-COMPLY Compliance and PDPA officer | R | RU | R |
| RW-PLATADM Platform administrator | R | R | CRUD |
| RW-REFADM Reference data administrator | R | CRUD | - |
| RW-SECADM Security administrator | R | R | CRUDA |
| RW-BIANAL Reporting and BI analyst | R | R | - |
| RW-TRIBE Tribe lead and squad members | R | R | - |
| SY-CASEWF Case workflow module | R | R | - |
| SY-RULES Drools evaluator | R | R | - |
| SY-DATALOAD Data load from COLLINS | - | R | - |
| SY-OCR OCR and extraction pipeline | - | R | - |
| SY-AGENT Agent platform | R | R | - |

Rule package and workflow administration rights refine the three columns above:

| Role | Rule packages | Temporal workflows |
|---|---|---|
| RW-COE Center of excellence analyst | C, U: upload a version, list it, dry-run it and roll back | - |
| RW-RISK Risk and model risk officer | A: approve a version; the author cannot approve | - |
| RW-AUDIT Internal audit | R: package list, versions, dry run counts and change report | R: Web UI read-only |
| RW-REFADM Reference data administrator | Prepares the change checklist and the load file; no upload, no approval and no rollback | - |
| RW-PLATADM Platform administrator | R | Runs the smoke workflow; operates the Web UI |
| RW-SECADM Security administrator | R | Decodes payloads through the codec server under break-glass |
| SY-RULES Drools evaluator | R: reads the package version in force | - |
| SY-CASEWF Case workflow module | R | Starts and signals a workflow through WorkflowGateway |

### T6.2 Authentication and authorization

Entra ID single sign-on through the ACE front end; each endpoint declares its capability area and right; scope filters every query; masking applies to personal fields; service identities for jobs and agents. The Temporal Web UI uses the same Entra roles: RW-PLATADM operates, RW-AUDIT reads and RW-SECADM decodes through the codec server under break-glass (RWB-E2-038). mTLS protects the worker, the frontend and the internal services.

### T6.3 Audit of a rule package change

| Requirement | What is recorded | Where |
|---|---|---|
| change_checklist | The seven items: request, impact, test result, approver, load, verify and rollback plan. The version cannot be approved while an item is missing | rule_package_version.change_checklist (DF-REF-295); MSG-P3-022 |
| checksum | SHA-256 of the uploaded workbook and of the generated DRL; recorded at load, checked when the KieBase is built, and shown on the change report | rule_package_version.checksum (DF-REF-285) |
| author and approver | The author who loaded the version and the approver who approved it, with both times; the author cannot approve | rule_package_version.author (DF-REF-288), approver (DF-REF-289), loaded_at (DF-REF-290) and approved_at (DF-REF-291); MSG-P7-002 |
| decision log linkage | Every decision of the package writes the rule ID and the package version label; the change report counts the decisions per package version | decision_log_entry.rule_id and rule_version; the change report of API-P4-021 |

A load, an approval and a rollback each write a change log entry with the version label, the status change, the author or approver and the time. The entry is append only. The change report reads the versions and the decision log and is the report RW-AUDIT reads for a rule change.

This service is the authorisation provider of DP-08: it publishes the authorise, permission, delegation-limit and masking operations that the other 18 services call, and it applies the same check to its own administration operations (H RWB-PLT-E1037-CON).

## T7. Non-functional requirements

| ID | Requirement | Target | Status |
|---|---|---|---|
| NFR-039 | Party identifiers are masked at rest in the case store, and on every screen and every agent call, by role. | Masked at rest and in use | Proposed |
| NFR-040 | Each screen and each agent receives only the personal data it needs. | Data minimization per screen and per agent | Proposed |
| NFR-041 | The debt sale data tape is masked before it reaches the data room. | Masked tape | Proposed |
| NFR-042 | Every read of the case store, the document store and the data lake copy is logged. | Every read | Proposed |
| NFR-043 | A data subject access, correction or erasure request is answered inside the statutory period. | Statutory period, Not set as a working service level | Open, DL26 |
| NFR-044 | Consent state per channel is held and applied, and statutory notices continue when consent is withdrawn. | Applied on every send | Proposed |
| NFR-045 | No production data is used in the development environment, and the user acceptance environment uses masked copies. | Synthetic in development, masked in user acceptance | Proposed |
| NFR-049 | Staff authenticate with single sign-on and multi-factor authentication. | Entra ID single sign-on with multi-factor | Proposed |
| NFR-050 | Partner accounts authenticate with multi-factor and are scoped to their own cases. | Multi-factor, scoped | Proposed |
| NFR-051 | Agents run under service identities and are subject to the same role checks as people. | Service identities | Proposed |
| NFR-052 | Secrets are held in the key store and never in code, configuration files or prompts. | No secrets in code or prompts | Proposed |
| NFR-053 | Data is encrypted at rest and in transit. | Encrypted | Proposed |
| NFR-054 | The build pipeline blocks a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency. | Pipeline checks pass | Proposed |
| NFR-055 | Agent outputs are schema checked against an allowed-action list with a confidence threshold, and fall back to rules when the check fails. | Schema check on every output | Proposed |
| NFR-056 | Penetration testing and a security review are completed before the first production release. | Before the first production release and before the partner portal opens to users outside the bank | Proposed, DL11 |

## T8. Requirement traceability

| Requirement | Feature | Story | Test |
|---|---|---|---|
| REQ-ACA-001 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
| REQ-ACA-002 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
| REQ-ACA-003 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
| REQ-ACA-004 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
| REQ-ACA-005 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
| REQ-ACA-006 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
| REQ-ACA-007 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
| REQ-ACA-008 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
| REQ-ACA-009 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
| REQ-ACA-010 | FEAT-ACA-01 | RWB-E1-022 | TC-E1-022-01 |
| REQ-ACA-011 | None | Written one epic ahead | With the story |
| REQ-ACA-012 | None | Written one epic ahead | With the story |
| REQ-ACA-013 | FEAT-ADM-01 | Written one epic ahead | With the story |
| REQ-CWC-013 | FEAT-CWC-16 | RWB-E2-041 | TC-E2-041-01 |
| REQ-CWC-014 | FEAT-CWC-14 | RWB-E1-073 | TC-E1-073-02 |
| REQ-DRI-011 | FEAT-CWC-16 | RWB-E2-041 | TC-E2-041-10 |
| REQ-DRI-001 | None | RWB-E2-038 | TC-E2-038-01 |
| REQ-DRI-005 | None | RWB-E2-038 | TC-E2-038-02 |
| REQ-DRI-007 | None | RWB-E1-070 | TC-E1-070-02 |
| REQ-DRI-010 | None | RWB-E1-071 | TC-E1-071-06 |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-P4-004 | GET | /api/recovery/access/v1/admin/lists/{listCode} | Reference data R | E1 |
| API-P4-005 | POST | /api/recovery/access/v1/admin/reference-loads | Reference data C | E1 |
| API-P4-006 | POST | /api/recovery/access/v1/admin/reference-loads/{loadId}/approve | Reference data A | E1 |
| API-P4-007 | GET | /api/recovery/access/v1/admin/roles | Platform administration R | E1 |
| API-P4-008 | GET | /api/recovery/access/v1/admin/access-log | Platform administration R | E1 |
| API-P4-009 | POST | /api/recovery/access/v1/admin/reference-loads/{loadId}/verify | Reference data U | E1 |
| API-P4-010 | POST | /api/recovery/access/v1/admin/reference-loads/{loadId}/rollback | Reference data U | E1 |
| API-P4-012 | GET | /api/recovery/access/v1/me/session | None R | E1 |
| API-P4-013 | POST | /api/recovery/access/v1/admin/break-glass-grants | Platform administration C | E1 |
| API-P4-014 | GET | /api/recovery/access/v1/admin/rule-packages | Rules and parameters R | E1 |
| API-P4-015 | POST | /api/recovery/access/v1/admin/rule-packages/{packageCode}/versions | Rules and parameters C | E1 |
| API-P4-016 | GET | /api/recovery/access/v1/admin/rule-packages/{packageCode}/versions | Rules and parameters R | E1 |
| API-P4-017 | POST | /api/recovery/access/v1/admin/rule-package-versions/{versionId}/approve | Rules and parameters A | E1 |
| API-P4-018 | POST | /api/recovery/access/v1/admin/rule-package-versions/{versionId}/rollback | Rules and parameters U | E1 |
| API-P4-019 | GET | /api/recovery/access/v1/admin/rule-package-versions/{versionId}/dry-run | Rules and parameters R | E1 |
| API-P4-020 | GET | /api/recovery/access/v1/admin/rule-packages/change-report | Rules and parameters R | E2 |
| API-P4-021 | POST | /api/recovery/access/v1/admin/workflows/smoke | Platform administration C | E1 |

The operation IDs, paths and operationIds of these endpoints are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-access.yaml`; where an appendix row and the published operation differ, the published operation is the contract of T5.2.1 and the row keeps its ID for traceability (GAP-1997; ASM-3224).

### T-A.2 Endpoint detail

#### API-P4-004 GET /admin/lists/{listCode}

| Item | Value |
|---|---|
| Purpose | Read a list of values with its versions |
| Request | None |
| Response | ListOfValues |
| Errors | 401, 403, 404, 503 |
| Authorization | Reference data, right R, scope applied |
| Idempotency | Not applicable |

#### API-P4-005 POST /admin/reference-loads

| Item | Value |
|---|---|
| Purpose | Load reference data: lists, queues, timers, templates, delegation limits |
| Request | Multipart: file, table, validFrom |
| Response | ReferenceLoad |
| Errors | 401, 403, 409, 422, 503 |
| Authorization | Reference data, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P4-006 POST /admin/reference-loads/{loadId}/approve

| Item | Value |
|---|---|
| Purpose | Approve a reference data load |
| Request | None |
| Response | ReferenceLoad |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Reference data, right A, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P4-007 GET /admin/roles

| Item | Value |
|---|---|
| Purpose | List roles with permissions and scope |
| Request | None |
| Response | Role[] |
| Errors | 401, 403, 503 |
| Authorization | Platform administration, right R, scope applied |
| Idempotency | Not applicable |

#### API-P4-008 GET /admin/access-log

| Item | Value |
|---|---|
| Purpose | Search the access log |
| Request | Query: user, from, to, event, page, size |
| Response | AccessLogPage |
| Errors | 401, 403, 503 |
| Authorization | Platform administration, right R, scope applied |
| Idempotency | Not applicable |

#### API-P4-009 POST /admin/reference-loads/{loadId}/verify

| Item | Value |
|---|---|
| Purpose | Record the verification of a reference data version after its valid from date |
| Request | VerifyRequest |
| Response | ReferenceLoad |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Reference data, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P4-010 POST /admin/reference-loads/{loadId}/rollback

| Item | Value |
|---|---|
| Purpose | Roll back an approved reference data version to the version before it |
| Request | RollbackRequest |
| Response | ReferenceLoad |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Reference data, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P4-012 GET /me/session

| Item | Value |
|---|---|
| Purpose | Read the caller's resolved session: roles, scope, matrix and conflict versions, partner and break-glass state |
| Request | None |
| Response | Session |
| Errors | 401, 503 |
| Authorization | None, right R, scope applied |
| Idempotency | Not applicable |

#### API-P4-013 POST /admin/break-glass-grants

| Item | Value |
|---|---|
| Purpose | Activate a break-glass grant approved in the bank IAM for an open incident, area, right, scope and reason |
| Request | BreakGlassActivation |
| Response | BreakGlassGrant |
| Errors | 401, 403, 409, 422, 503 |
| Authorization | Platform administration, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P4-014 GET /admin/rule-packages

| Item | Value |
|---|---|
| Purpose | List rule packages with the version in force and its status |
| Request | Query: status, page, size |
| Response | RulePackage[] |
| Errors | 401, 403, 503 |
| Authorization | Rules and parameters, right R, scope applied |
| Idempotency | Not applicable |

#### API-P4-015 POST /admin/rule-packages/{packageCode}/versions

| Item | Value |
|---|---|
| Purpose | Upload an Excel workbook in Drools decision-table format, compile it, run the checks and the scenarios and store the version LOADED |
| Request | Multipart: file (xlsx), validFrom |
| Response | RulePackageVersion |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Rules and parameters, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P4-016 GET /admin/rule-packages/{packageCode}/versions

| Item | Value |
|---|---|
| Purpose | List the versions of one package with status, checksum, author, approver, test result and dry run counts |
| Request | Query: status |
| Response | RulePackageVersion[] |
| Errors | 401, 403, 404, 503 |
| Authorization | Rules and parameters, right R, scope applied |
| Idempotency | Not applicable |

#### API-P4-017 POST /admin/rule-package-versions/{versionId}/approve

| Item | Value |
|---|---|
| Purpose | Approve a loaded package version after the change checklist is complete; the author cannot approve |
| Request | None |
| Response | RulePackageVersion |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Rules and parameters, right A, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P4-018 POST /admin/rule-package-versions/{versionId}/rollback

| Item | Value |
|---|---|
| Purpose | Roll back a package version in force to the version before it, with a reason |
| Request | RollbackRequest |
| Response | RulePackageVersion |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Rules and parameters, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P4-019 GET /admin/rule-package-versions/{versionId}/dry-run

| Item | Value |
|---|---|
| Purpose | Read the dry run result of a loaded version against the open cases it would decide |
| Request | None |
| Response | DryRunResult |
| Errors | 401, 403, 404, 503 |
| Authorization | Rules and parameters, right R, scope applied |
| Idempotency | Not applicable |

#### API-P4-020 GET /admin/rule-packages/change-report

| Item | Value |
|---|---|
| Purpose | Report every package version change for audit, with its checklist, checksum, author, approver and the decisions it made (RWB-E2-041) |
| Request | Query: from, to, packageCode, format, page, size |
| Response | RuleChangeReportPage, JSON or CSV |
| Errors | 401, 403, 422, 503 |
| Authorization | Rules and parameters, right R, scope applied |
| Idempotency | Not applicable |

#### API-P4-021 POST /admin/workflows/smoke

| Item | Value |
|---|---|
| Purpose | Run PlatformSmokeWorkflow on demand in the caller's environment; 404 when rwb.p3.temporal is off |
| Request | SmokeRequest |
| Response | SmokeResult |
| Errors | 401, 403, 404, 503 |
| Authorization | Platform administration, right C, scope applied |
| Idempotency | Idempotency-Key header |

## Appendix T-B. Open technical decisions

| Decision | What is needed |
|---|---|
| DL06 | Which interfaces need same-day data |
| DL11 | Non-functional target values |
| DL26 | Retention periods, including the 30-day Temporal history retention |
| DL35 | Deployment slots |

## Document sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| Solution architect | | | |
| Tech lead | | | |
| ACE team | | | |
| QA lead | | | |

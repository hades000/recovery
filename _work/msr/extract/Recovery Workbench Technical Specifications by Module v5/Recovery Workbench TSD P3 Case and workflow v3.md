# Recovery Workbench P3 Case and workflow

Technical specification. SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD P3 Case and workflow |
| Document ID | P3-RWB-TSD-v3 |
| Version | 3 |
| Status | In review |
| Date | 16 November 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD P3 Case and workflow | FSD | Pair |
| Recovery Workbench Target Architecture | Architecture | Parent |
| Recovery Workbench Logical Data Model and Data Dictionary | Data | Source of T3 |
| Recovery Workbench API Specification | API | Source of appendix T-A |
| Recovery Workbench Architecture Decision Records | ADR | ADR-011 Temporal; ADR-012 Drools |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit, PII and SOC logging | REUSE | ACE common module | Called through the published interface |
| Scheduler and batch | REUSE | ACE pattern: Quartz and Spring Batch | Jobs in the Batch and Scheduling Design |
| Outbox and retry | REUSE | Error Handling and Resilience Standard | Through P2 |
| Rules evaluation | NEW | Rules Engine Design | Embedded Drools from versioned rule packages (ADR-012) |
| Workflow engine | NEW | Workflow Engine Design | Temporal, self-hosted; case workflows from Epic 3 (ADR-011) |

## T1. Architecture overview

P3 Case and workflow is part of the recovery module in the ACE service: one service, one repository, one front end. It covers: case record, CMMN state, queues, allocation, timers, the Drools evaluator, the timer port and the Temporal worker. Case data stays the system of record in the recovery schema; Temporal runs the case lifecycle from Epic 3 (ADR-011), and rules are evaluated by embedded Drools from versioned rule packages (ADR-012). It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

### T2.1 Component table

| Component | Responsibility |
|---|---|
| CaseAndWorkflowController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| CaseAndWorkflowService | Business logic; calls RuleEvaluator for every decision; writes the decision log entry before any change |
| CaseAndWorkflowRepository | Reads and writes the module's tables only |
| RulePackageRepository | Reads rule_package, rule_package_version and rule_row; holds the workbook, the DRL and the checksum of each version |
| KieBaseRegistry | Builds one KieBase per package version from drl_source on first use and caches up to drools.kiebase.cache.max; refuses a checksum mismatch |
| RuleEvaluator | Published interface; picks the version in force on the date, inserts the facts, fires and returns one RuleResult |
| RuleCatalog | Published interface; reads action text, owner role, timer spec and outputs from rule_row by rule ID and package version |
| DecisionLogAgendaListener | Captures the name of the fired Drools rule for the decision log entry |
| TimerScheduler | Published port; schedule, cancel, pause and resume a timer; every caller uses it |
| TimerCheckJob | JOB-05 on Quartz; the implementation of TimerScheduler in Epics 1 and 2 |
| WorkflowGateway | Published interface; starts a workflow and sends a signal; the only path from module code to Temporal |
| TemporalConfig | Spring Boot starter configuration; target, namespace, task queue, retention, mTLS and the feature flag |
| PdpaPayloadCodec | Encrypts and decrypts every workflow payload; AES-GCM with the key in Key Vault |
| PlatformSmokeWorkflow | Daily smoke workflow on rwb-platform; one activity writes a PLATFORM_SMOKE decision log entry |
| WorkerBuildIdProvider | Supplies the build ID of the running worker to the replay gate |
| Jobs | Quartz and Spring Batch jobs the module owns |
| Published interface | Java interface other modules call; no table is read across modules |

### T2.2 Rules package

A rule package is a Drools XLS decision table held as data. rule_package names the package and its owner role; rule_package_version holds one uploaded version with its workbook, the generated DRL, the checksum and its approval. The package code is the RuleSet of the workbook. Phase 1 uses five package codes:

| Package code | Phase | Rules in the table | Used by |
|---|---|---|---|
| ENTRY | 1 | entry rows (DL24) | RWB-E1-018 |
| EXCLUSION | 1 | exclusion rows (DL24) | RWB-E1-018 |
| ALLOCATION | 1 | allocation rows (DL24) | RWB-E1-020, RWB-E1-030 |
| ASSIGNMENT | 1 | assignment rows (DL24) | RWB-E1-020, RWB-E1-030 |
| TRANSFER | 1 | transfer rows (DL24) | RWB-E1-021, RWB-E2-012 |

RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH follow in Epic 2 (RWB-E2-042). The R-UNI-xx rules that Epic 1 cites stay as coded behaviour and are cited by ID; they move into a UNIVERSAL package in Epic 3.

Drools is embedded in the recovery module. The build uses the KIE runtime libraries only: drools-engine, drools-mvel, drools-decisiontables and drools-xml-support. There is no KIE Server, no Business Central and no KJAR in Maven.

The published interfaces are:

```java
public interface RuleEvaluator {
    RuleResult evaluate(String packageCode, Object facts, LocalDate onDate); // throws NoPackageInForce
}
public record RuleResult(String packageCode, String packageVersion, String ruleId, Map<String,Object> outputs) {}
public interface RuleCatalog { RuleRow row(String ruleId, String packageVersion); }
```

RuleEvaluator.evaluate picks the version IN_FORCE on the date, inserts the facts, fires the rules and returns one RuleResult. It throws NoPackageInForce when no version is in force, and the caller reports MSG-P3-027. A version is never edited in place; a change is a new version.

First match is kept. Each decision table has RuleSet = the package code. Each row is one rule whose NAME is the rule ID, for example ALLOC-031. All rows share one activation-group and salience is derived from row order, so exactly one row decides; the default row is last. The decision log records rule ID = the Drools rule name and rule version = the package version label, in the existing decision_log_entry.rule_id and rule_version columns, with no schema change.

The package version is chosen at evaluation time, returned in RuleResult and written to the decision log. A case keeps the version it was decided under (R-UNI-38). Workflow code calls Drools only inside an activity (T2.4 and T2.5).

A rule change is made through RWB-E1-073: RW-COE uploads the workbook, the checks and the scenarios run, RW-RISK approves, and the version is in force from its valid-from date. The author cannot approve, and rollback is one call.

### T2.3 Timers port

A timer stays a row in the timer table with its type, started_at, expires_at, warn_at, paused flag and status. Every caller schedules, cancels, pauses and resumes a timer through the published port:

```java
public interface TimerScheduler {
    void schedule(TimerSpec t);
    void cancel(UUID timerId);
    void pause(UUID timerId);
    void resume(UUID timerId);
}
```

TimerCheckJob (JOB-05, Quartz) is the implementation. It runs every 5 minutes as SY-CASEWF, finds RUNNING timers whose warn_at or expires_at has passed, writes the decision log entry and raises the warning or the breach. It is the only component that reads due timers from the table.

No caller holds a Quartz trigger, a job class or a scheduler factory. A caller names a TimerSpec, and the port owns the Quartz job data and the misfire policy. The port is the swap point: Epic 3 replaces the TimerCheckJob implementation with Temporal durable timers behind the same interface, and no caller changes (ADR-011). Temporal Schedules are not used in Epics 1 and 2.

### T2.4 Workflow package

The workflow code is one package, recovery.casewf.workflow, with the published gateway:

```java
public interface WorkflowGateway {
    String start(String workflowType, String workflowId, Object input);
    void signal(String workflowId, String signal, Object payload);
}
```

| Class | Responsibility |
|---|---|
| WorkflowGateway | Published interface; start and signal; turns a Temporal failure into MSG-P3-036 |
| TemporalConfig | Spring Boot starter beans; target, namespace, task queue, retention, mTLS, build ID and the feature flag |
| PdpaPayloadCodec | Payload codec on every payload; encrypts before the history write and decrypts after the read |
| PlatformSmokeWorkflow | Smoke workflow on rwb-platform; one activity writes a PLATFORM_SMOKE decision log entry |
| PlatformSmokeActivity | The only activity of the smoke workflow; writes the decision log entry and returns its ID |

Workflow code is deterministic: no clock read, no random, no I/O and no Drools call in workflow code. All I/O, including every rule evaluation, is in an activity.

Workflow IDs are fixed by convention, so a retry is safe:

| Workflow | Workflow ID | Task queue |
|---|---|---|
| Case workflow (Epic 3) | case-{caseId}, for example case-RW-2026-000123 | rwb-case |
| Platform smoke (Epic 1) | platform-smoke-{yyyymmdd} | rwb-platform |

A duplicate start with an existing running workflow returns the running execution and starts nothing. Each worker carries the build ID of its build, so a new build takes new workflows while the old build drains (RWB-E2-040). A boundary test fails a workflow class placed outside recovery.casewf.workflow.

### T2.5 Temporal worker and configuration

The recovery module runs a Temporal worker through the Temporal Spring Boot starter. The worker connects to the namespace, polls the platform task queue and registers the workflows and activities of recovery.casewf.workflow. The feature flag rwb.p3.temporal turns it on; with the flag off the worker does not start and the workflow admin endpoint returns 404.

| Parameter | Value | Note |
|---|---|---|
| temporal.target | Frontend gRPC address per environment | Internal only; port 7233 |
| temporal.namespace | rwb-recovery | One namespace per cluster; ace-collection is reserved for the ACE team |
| temporal.taskqueue.platform | rwb-platform | Smoke and health workflows; rwb-case and rwb-integration follow in Epic 3 |
| temporal.retention.days | 30 | Closed workflow history; assumed, confirmed with DL26 |
| rwb.p3.temporal | On or off per environment | Off: no worker, and the admin smoke endpoint returns 404 |

All values come from parameters through RWB-E1-042, never from code.

The worker and the frontend use mTLS with certificates from the ACE internal CA, bound from Key Vault. The worker identity is SY-CASEWF; the Drools evaluator identity is SY-RULES. Payloads are encrypted by PdpaPayloadCodec (AES-GCM, key in Azure Key Vault) before the history write, so the history holds no clear personal data; the search attributes carry CaseId, Stage, ProductGroup and QueueCode only. The Web UI is behind Entra ID OIDC: RW-PLATADM operates, RW-AUDIT reads and RW-SECADM decodes through the codec server under break-glass (RWB-E2-038).

## T3. Data model

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

**recovery_case** (EXTEND ACE Case). One recovery case per customer per product, from 90 days past due to close.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-CAS-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-CAS-002 | case_no | TEXT | varchar(18) | Yes | None | Workbench |
| DF-CAS-003 | product_group | LOV | varchar(15) | Yes | LOV-PRODUCT | Core bank (ALS) via COLLINS |
| DF-CAS-004 | primary_customer_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-CAS-005 | status | LOV | varchar(20) | Yes | LOV-CASE-STATUS | Workbench |
| DF-CAS-006 | stage_code | LOV | varchar(20) | No | LOV-STAGE | Workbench |
| DF-CAS-007 | route_state | TEXT | varchar(60) | No | None | Workbench |
| DF-CAS-008 | route_code | LOV | varchar(4) | No | LOV-ROUTE | Workbench |
| DF-CAS-009 | owner_user_id | USER_REF | uuid | No | None | Workbench |
| DF-CAS-010 | queue_id | CROSS_REF | uuid | No | None | Workbench |
| DF-CAS-011 | team_code | LOV | varchar(20) | No | LOV-TEAM | Workbench |
| DF-CAS-012 | region_code | LOV | varchar(10) | No | LOV-REGION | Workbench |
| DF-CAS-013 | entry_date | DATE | date | Yes | None | Workbench |
| DF-CAS-014 | dpd_at_entry | NUMBER | integer | Yes | None | Core bank (ALS) via COLLINS |
| DF-CAS-015 | exposure_band | LOV | varchar(10) | No | LOV-EXPOSURE | Workbench |
| DF-CAS-016 | total_outstanding_at_entry | NUMBER | numeric(18,2) | Yes | None | Core bank (ALS) via COLLINS |
| DF-CAS-017 | prescription_date | DATE | date | No | None | Workbench |
| DF-CAS-018 | stage_clock_start | DATE | timestamptz | No | None | Workbench |
| DF-CAS-019 | deviation_open | BOOLEAN | boolean | Yes | None | Workbench |
| DF-CAS-020 | legal_hold | BOOLEAN | boolean | Yes | None | Workbench |
| DF-CAS-021 | rule_version | TEXT | varchar(20) | No | None | Workbench |
| DF-CAS-022 | closed_date | DATE | date | No | None | Workbench |
| DF-CAS-023 | closure_reason | LOV | varchar(20) | No | LOV-CLOSURE | Workbench |
| DF-CAS-046 | plan_ref | TEXT | varchar(30) | No | None | ACE |
| DF-CAS-047 | plan_status | LOV | varchar(10) | No | LOV-PLAN-STATUS | ACE |
| DF-CAS-048 | plan_status_as_of | DATE | date | No | None | ACE |
| DF-CAS-049 | next_action_text | TEXT | varchar(1000) | No | None | Workbench |
| DF-CAS-050 | next_action_owner_role | LOV | varchar(20) | No | LOV-ROLE | Workbench |
| DF-CAS-051 | next_action_due_date | DATE | date | No | None | Workbench |
| DF-CAS-052 | next_action_rule_id | TEXT | varchar(20) | No | None | Workbench |
| DF-CAS-053 | next_action_waiting | BOOLEAN | boolean | Yes | None | Workbench |
| DF-CAS-054 | last_allocation_date | DATE | date | No | None | Workbench |
| DF-CAS-055 | status_before_hold | LOV | varchar(20) | No | LOV-CASE-STATUS | Workbench |

**case_account** (NEW). Links each loan account to the case it is recovered under.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-CAS-024 | id | TEXT | uuid | Yes | None | Workbench |
| DF-CAS-025 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-CAS-026 | account_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-CAS-027 | is_primary | BOOLEAN | boolean | Yes | None | Workbench |
| DF-CAS-028 | linked_from | DATE | date | Yes | None | Workbench |
| DF-CAS-029 | linked_to | DATE | date | No | None | Workbench |

**case_party** (NEW). The role each party plays on a case.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-CAS-030 | id | TEXT | uuid | Yes | None | Workbench |
| DF-CAS-031 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-CAS-032 | party_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-CAS-033 | party_role | LOV | varchar(20) | Yes | LOV-PARTY-ROLE | Workbench |
| DF-CAS-034 | role_from | DATE | date | Yes | None | Workbench |
| DF-CAS-035 | role_to | DATE | date | No | None | Workbench |

**queue** (EXTEND ACE work queue). A queue of work belonging to one team and one role.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-WRK-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-WRK-002 | queue_code | TEXT | varchar(30) | Yes | None | Workbench |
| DF-WRK-003 | queue_name | TEXT | varchar(100) | Yes | None | Workbench |
| DF-WRK-004 | team_code | LOV | varchar(20) | Yes | LOV-TEAM | Workbench |
| DF-WRK-005 | role_code | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-WRK-006 | assignment_method | LOV | varchar(20) | Yes | LOV-ASSIGN | Workbench |
| DF-WRK-007 | capacity_cap | NUMBER | integer | No | None | Workbench |
| DF-WRK-008 | overflow_queue_id | CROSS_REF | uuid | No | None | Workbench |
| DF-WRK-037 | rr_cursor_user_id | USER_REF | uuid | No | None | Workbench |
| DF-WRK-038 | table_version | NUMBER | integer | No | None | Workbench |

**assignment** (REUSE ACE Assignee). Who holds a case or a task and from when.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-WRK-009 | id | TEXT | uuid | Yes | None | Workbench |
| DF-WRK-010 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-WRK-011 | task_id | CROSS_REF | uuid | No | None | Workbench |
| DF-WRK-012 | assignee_user_id | USER_REF | uuid | Yes | None | Workbench |
| DF-WRK-013 | assigned_at | DATE | timestamptz | Yes | None | Workbench |
| DF-WRK-014 | ended_at | DATE | timestamptz | No | None | Workbench |
| DF-WRK-015 | reason | LOV | varchar(20) | Yes | LOV-ASSIGN-REASON | Workbench |
| DF-WRK-016 | rule_id | TEXT | varchar(20) | No | None | Workbench |
| DF-WRK-039 | queue_id | CROSS_REF | uuid | No | None | Workbench |
| DF-WRK-040 | transfer_reason_code | LOV | varchar(20) | No | LOV-TRANSFER-REASON | Workbench |

**task** (NEW). A unit of work on a case: a CMMN human, customer, partner or decision task.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-WRK-017 | id | TEXT | uuid | Yes | None | Workbench |
| DF-WRK-018 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-WRK-019 | task_code | TEXT | varchar(60) | Yes | None | Workbench |
| DF-WRK-020 | element_type | LOV | varchar(20) | Yes | LOV-ELEMENT | Workbench |
| DF-WRK-021 | discretion | LOV | varchar(15) | Yes | LOV-DISCRETION | Workbench |
| DF-WRK-022 | status | LOV | varchar(15) | Yes | LOV-TASK-STATUS | Workbench |
| DF-WRK-023 | owner_role | LOV | varchar(20) | No | LOV-ROLE | Workbench |
| DF-WRK-024 | due_at | DATE | timestamptz | No | None | Workbench |
| DF-WRK-025 | completed_at | DATE | timestamptz | No | None | Workbench |
| DF-WRK-026 | outcome_code | TEXT | varchar(40) | No | None | Workbench |

**timer** (NEW). A running clock on a case: a service level, a legal period or an offer validity.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-WRK-027 | id | TEXT | uuid | Yes | None | Workbench |
| DF-WRK-028 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-WRK-029 | task_id | CROSS_REF | uuid | No | None | Workbench |
| DF-WRK-030 | timer_type | LOV | varchar(20) | Yes | LOV-TIMER | Workbench |
| DF-WRK-031 | started_at | DATE | timestamptz | Yes | None | Workbench |
| DF-WRK-032 | expires_at | DATE | timestamptz | Yes | None | Workbench |
| DF-WRK-033 | warn_at | DATE | timestamptz | No | None | Workbench |
| DF-WRK-034 | paused | BOOLEAN | boolean | Yes | None | Workbench |
| DF-WRK-035 | status | LOV | varchar(15) | Yes | LOV-TIMER-STATUS | Workbench |
| DF-WRK-036 | escalation_level | NUMBER | integer | Yes | None | Workbench |
| DF-WRK-041 | warned_at | DATE | timestamptz | No | None | Workbench |
| DF-WRK-042 | treatment_id | CROSS_REF | uuid | No | None | Workbench |
| DF-WRK-043 | escalated_to_role | LOV | varchar(20) | No | LOV-ROLE | Workbench |
| DF-WRK-044 | escalated_at | DATE | timestamptz | No | None | Workbench |

**interaction** (EXTEND ACE activity log). One entry in the interaction ledger: a contact, letter, promise, payment or hand-over.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-INT-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-INT-002 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-INT-003 | party_id | CROSS_REF | uuid | No | None | Workbench |
| DF-INT-004 | occurred_at | DATE | timestamptz | Yes | None | Workbench |
| DF-INT-005 | channel | LOV | varchar(15) | No | LOV-CHANNEL | Workbench |
| DF-INT-006 | direction | LOV | varchar(8) | No | LOV-DIRECTION | Workbench |
| DF-INT-007 | action_code | LOV | varchar(10) | No | LOV-ACTION-CODE | EFS via COLLINS |
| DF-INT-008 | contact_result | LOV | varchar(20) | No | LOV-CONTACT-RESULT | EFS via COLLINS |
| DF-INT-009 | promise_amount | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-INT-010 | promise_date | DATE | date | No | None | Workbench |
| DF-INT-011 | summary | TEXT | varchar(2000) | No | None | Workbench |
| DF-INT-012 | conduct_check | LOV | varchar(15) | No | LOV-CONDUCT | Workbench |
| DF-INT-013 | source_system | LOV | varchar(10) | Yes | LOV-SOURCE | Workbench |
| DF-INT-014 | event_code | LOV | varchar(40) | No | LOV-LEDGER-EVENT | Workbench |
| DF-INT-015 | actor_type | LOV | varchar(10) | No | LOV-ACTOR-TYPE | Workbench |
| DF-INT-016 | actor_ref | TEXT | varchar(64) | No | None | Workbench |
| DF-INT-017 | source_ref | TEXT | varchar(60) | No | None | Workbench |
| DF-INT-018 | idempotency_key | TEXT | varchar(120) | No | None | Workbench |
| DF-INT-019 | case_seq | NUMBER | bigint | No | None | Workbench |
| DF-INT-020 | decision_log_id | CROSS_REF | uuid | No | None | Workbench |
| DF-INT-021 | corrects_entry_id | CROSS_REF | uuid | No | None | Workbench |
| DF-INT-022 | contact_point_id | CROSS_REF | uuid | No | None | Workbench |
| DF-INT-023 | from_holder_ref | TEXT | varchar(60) | No | None | Workbench |
| DF-INT-024 | to_holder_ref | TEXT | varchar(60) | No | None | Workbench |
| DF-INT-025 | treatment_id | CROSS_REF | uuid | No | None | Workbench |
| DF-INT-026 | proceeds_id | CROSS_REF | uuid | No | None | Workbench |
| DF-INT-027 | retention_class | LOV | varchar(10) | No | LOV-RETENTION | Workbench |
| DF-INT-028 | delivery_status | LOV | varchar(15) | No | LOV-SEND-STATUS | Workbench |
| DF-INT-029 | external_ref | TEXT | varchar(60) | No | None | Workbench |

**case_entry_exclusion** (NEW). An account at 90 days past due that an exclusion rule kept out of recovery on a business date.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-CAS-056 | id | TEXT | uuid | Yes | None | Workbench |
| DF-CAS-057 | account_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-CAS-058 | business_date | DATE | date | Yes | None | Workbench |
| DF-CAS-059 | reason_code | LOV | varchar(20) | Yes | LOV-EXCLUSION-REASON | Workbench |
| DF-CAS-060 | rule_id | TEXT | varchar(20) | Yes | None | Workbench |
| DF-CAS-061 | rule_version | TEXT | varchar(20) | Yes | None | Workbench |

**queue_member** (NEW). A person who works a queue, with personal capacity and skills, by version.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-WRK-045 | id | TEXT | uuid | Yes | None | Workbench |
| DF-WRK-046 | queue_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-WRK-047 | user_id | USER_REF | uuid | Yes | None | Workbench |
| DF-WRK-048 | capacity | NUMBER | integer | No | None | Workbench |
| DF-WRK-049 | skill_codes | TEXT | varchar(200) | No | None | Workbench |
| DF-WRK-050 | table_version | NUMBER | integer | Yes | None | Workbench |
| DF-WRK-051 | valid_from | DATE | date | Yes | None | Workbench |
| DF-WRK-052 | valid_to | DATE | date | No | None | Workbench |

**queue_measure** (NEW). One snapshot of a queue's counts, ageing and breaches, published when it reconciles to the case list.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-RPT-020 | id | TEXT | uuid | Yes | None | Workbench |
| DF-RPT-021 | queue_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-RPT-022 | as_of | DATE | timestamptz | Yes | None | Workbench |
| DF-RPT-023 | depth | NUMBER | integer | Yes | None | Workbench |
| DF-RPT-024 | unassigned | NUMBER | integer | Yes | None | Workbench |
| DF-RPT-025 | avg_age_days | NUMBER | numeric(7,2) | No | None | Workbench |
| DF-RPT-026 | max_age_days | NUMBER | integer | No | None | Workbench |
| DF-RPT-027 | owner_min | NUMBER | integer | No | None | Workbench |
| DF-RPT-028 | owner_max | NUMBER | integer | No | None | Workbench |
| DF-RPT-029 | breached | NUMBER | integer | Yes | None | Workbench |
| DF-RPT-030 | status | LOV | varchar(15) | Yes | LOV-SNAPSHOT-STATUS | Workbench |

**parameter_catalog** (NEW). The definition of every parameter and environment setting, with its owner and default.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-132 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-133 | param_key | TEXT | varchar(100) | Yes | None | Workbench |
| DF-REF-134 | kind | TEXT | varchar(15) | Yes | None | Workbench |
| DF-REF-135 | value_type | TEXT | varchar(15) | Yes | None | Workbench |
| DF-REF-136 | unit | TEXT | varchar(20) | No | None | Workbench |
| DF-REF-137 | min_value | TEXT | varchar(40) | No | None | Workbench |
| DF-REF-138 | max_value | TEXT | varchar(40) | No | None | Workbench |
| DF-REF-139 | default_value | TEXT | varchar(400) | No | None | Workbench |
| DF-REF-140 | scope | LOV | varchar(10) | Yes | LOV-PARAM-SCOPE | Workbench |
| DF-REF-141 | required | BOOLEAN | boolean | Yes | None | Workbench |
| DF-REF-142 | owner_role | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-REF-143 | environments | TEXT | varchar(40) | No | None | Workbench |
| DF-REF-144 | used_by | TEXT | varchar(400) | No | None | Workbench |
| DF-REF-145 | secret | BOOLEAN | boolean | Yes | None | Workbench |
| DF-REF-146 | description | TEXT | varchar(400) | Yes | None | Workbench |

**parameter_value** (NEW). An approved, dated value version of a parameter per environment and product group.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-147 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-148 | param_key | TEXT | varchar(100) | Yes | None | Workbench |
| DF-REF-149 | environment | LOV | varchar(4) | Yes | LOV-ENVIRONMENT | Workbench |
| DF-REF-150 | param_value | TEXT | varchar(400) | Yes | None | Workbench |
| DF-REF-151 | product_group | LOV | varchar(15) | No | LOV-PRODUCT | Workbench |
| DF-REF-152 | version_no | NUMBER | integer | Yes | None | Workbench |
| DF-REF-153 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-154 | valid_to | DATE | date | No | None | Workbench |
| DF-REF-155 | status | LOV | varchar(15) | Yes | LOV-VERSION-STATUS | Workbench |
| DF-REF-156 | author_user_id | USER_REF | uuid | Yes | None | Workbench |
| DF-REF-157 | approver_user_id | USER_REF | uuid | No | None | Workbench |
| DF-REF-158 | approved_at | DATE | timestamptz | No | None | Workbench |

**reference_version** (NEW). One version of a reference or rule table, with its author, approver, checks and change checklist.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-159 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-160 | table_code | LOV | varchar(30) | Yes | LOV-REF-TABLE | Workbench |
| DF-REF-161 | version_no | NUMBER | integer | Yes | None | Workbench |
| DF-REF-162 | version_label | TEXT | varchar(20) | No | None | Workbench |
| DF-REF-163 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-164 | valid_to | DATE | date | No | None | Workbench |
| DF-REF-165 | status | LOV | varchar(15) | Yes | LOV-VERSION-STATUS | Workbench |
| DF-REF-166 | author_user_id | USER_REF | uuid | Yes | None | Workbench |
| DF-REF-167 | approver_user_id | USER_REF | uuid | No | None | Workbench |
| DF-REF-168 | approved_at | DATE | timestamptz | No | None | Workbench |
| DF-REF-169 | row_count | NUMBER | integer | Yes | None | Workbench |
| DF-REF-170 | content_hash | TEXT | char(64) | Yes | None | Workbench |
| DF-REF-171 | load_id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-172 | dry_run_counts | TEXT | jsonb | No | None | Workbench |
| DF-REF-173 | rollback_reason | TEXT | varchar(400) | No | None | Workbench |
| DF-REF-174 | change_request_ref | TEXT | varchar(30) | No | None | Workbench |
| DF-REF-175 | impact_summary | TEXT | varchar(1000) | No | None | Workbench |
| DF-REF-176 | test_result | LOV | varchar(10) | No | LOV-TEST-RESULT | Workbench |
| DF-REF-177 | rollback_plan | TEXT | varchar(1000) | No | None | Workbench |
| DF-REF-178 | verified_by | USER_REF | uuid | No | None | Workbench |
| DF-REF-179 | verified_at | DATE | timestamptz | No | None | Workbench |
| DF-REF-180 | verify_note | TEXT | varchar(1000) | No | None | Workbench |

**reference_row** (NEW). One row of a reference table version held as data.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-181 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-182 | version_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-REF-183 | row_key | TEXT | varchar(200) | Yes | None | Workbench |
| DF-REF-184 | row_data | TEXT | jsonb | Yes | None | Workbench |

**rule_test_case** (NEW, owned by P4). A test case of the rule package scenario harness, with its expected and actual result.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-185 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-186 | test_case_id | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-187 | route_set | LOV | varchar(15) | Yes | LOV-ROUTE-SET | Workbench |
| DF-REF-188 | rule_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-189 | rule_id | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-190 | from_state | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-191 | event_code | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-192 | facts | TEXT | jsonb | Yes | None | Workbench |
| DF-REF-193 | expected_to_state | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-194 | expected_owner_role | LOV | varchar(20) | No | LOV-ROLE | Workbench |
| DF-REF-195 | expected_timer_spec | TEXT | varchar(60) | No | None | Workbench |
| DF-REF-196 | result | LOV | varchar(10) | No | LOV-TEST-RESULT | Workbench |
| DF-REF-197 | result_detail | TEXT | varchar(1000) | No | None | Workbench |
| DF-REF-299 | package_version_id | CROSS_REF | uuid | No | None | Workbench |

**rule_package** (NEW, owned by P4). One rule package: a named decision table with an owner role and a hit policy.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-274 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-275 | package_code | TEXT | varchar(30) | Yes | None | Workbench |
| DF-REF-276 | title | TEXT | varchar(120) | Yes | None | Workbench |
| DF-REF-277 | owner_role | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-REF-278 | hit_policy | TEXT | varchar(20) | Yes | None | Workbench |

**rule_package_version** (NEW, owned by P4). One version of a rule package: the uploaded workbook, the generated DRL, the checksum and its approval.

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

**rule_row** additions (table owned by P4). The three fields this release adds to the rule catalog; the rest of the table is in TSD P4 T3.1.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-296 | package_version_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-REF-297 | drools_rule_name | TEXT | varchar(40) | Yes | None | Workbench |
| DF-REF-298 | outputs | TEXT | jsonb | No | None | Workbench |

payment_match_rule is retired (D-RCV-36 T10). Payment matching is package PAYMENT_MATCH, whose rows carry match type, tolerance, window, grace and partial floor as decision-table columns.

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-ACTOR-TYPE | USER, SERVICE, PARTNER |
| LOV-ASSIGN | ROUND_ROBIN, LOWEST_LOAD, NAMED_OWNER, SKILL |
| LOV-ASSIGN-REASON | ALLOCATION, TRANSFER, REBALANCE, MANUAL, ESCALATION |
| LOV-CASE-STATUS | NEW, ASSIGNED, IN_PROGRESS, WAITING_CUSTOMER, WAITING_PARTNER, WAITING_APPROVAL, ON_HOLD, CLOSED |
| LOV-CHANNEL | MOBILE, HOME_PHONE, WORK_PHONE, LINE, EMAIL, POSTAL_ADDRESS, CALL, VISIT, SMS, LETTER, PORTAL, BRANCH |
| LOV-CLOSURE | CURED, SETTLED, REALIZED, SOLD, WRITTEN_OFF, INSURANCE_SETTLED, MERGED, CANCELED |
| LOV-CONDUCT | PASSED, BLOCKED, NOT_APPLICABLE |
| LOV-CONTACT-RESULT | RIGHT_PARTY, THIRD_PARTY, NO_ANSWER, WRONG_NUMBER, REFUSED |
| LOV-DIRECTION | INBOUND, OUTBOUND |
| LOV-DISCRETION | AUTOMATIC, DISCRETIONARY, REQUIRED |
| LOV-ELEMENT | HUMAN_TASK, CUSTOMER_TASK, PARTNER_TASK, DECISION_TASK, STAGE_ENTRY, MILESTONE, EVENT_LISTENER |
| LOV-ENVIRONMENT | DEV, SIT, UAT, PROD |
| LOV-EXCLUSION-REASON | DECEASED, FRAUD, BANKRUPTCY, ACTIVE_PLAN, OPEN_DISPUTE |
| LOV-LEDGER-EVENT | CONTACT, LETTER, PROMISE, PAYMENT, HANDOVER, CASE_CREATED, CASE_ALLOCATED, CASE_TRANSFERRED, CASE_ESCALATED, DOCUMENT_ATTACHED, DECISION_TAKEN, CORRECTION, PARTNER_RESULT, OFFER |
| LOV-PARAM-SCOPE | PRODUCT, GLOBAL |
| LOV-PARTY-ROLE | BORROWER, CO_BORROWER, GUARANTOR, AUTHORIZED_SIGNATORY, HEIR |
| LOV-PLAN-STATUS | CREATED, APPROVED, BOOKED, BROKEN |
| LOV-PRODUCT | MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED |
| LOV-REF-TABLE | PRODUCT, REGION, EXPOSURE_BAND, ROLE, TEAM, QUEUE, QUEUE_MEMBER, SERVICE_LEVEL, DOCUMENT_TYPE, DOCUMENT_CHECKLIST, RETENTION_CLASS, TEMPLATE, DELEGATION_LIMIT, PERMISSION, MASKING_RULE, PARTNER_USER, LEGAL_PERIOD, HOLIDAY, PRODUCT_PARAMETER, PARAMETER, ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT, TRANSFER |
| LOV-ROUTE | R1, R2, R3, R4, R5, R6, R7, R8 |
| LOV-ROUTE-SET | RESTRUCTURE, SETTLEMENT, DEED_IN_LIEU, GUARANTEE_CLAIM, LITIGATION, ASSET_DISPOSAL, DEBT_SALE, WRITE_OFF, DEVIATIONS, UNIVERSAL_RULES |
| LOV-SEND-STATUS | SENT, DELIVERED, READ, FAILED |
| LOV-SNAPSHOT-STATUS | TAKEN, PUBLISHED, HELD |
| LOV-SOURCE | EFS, WORKBENCH |
| LOV-STAGE | RESTRUCTURE, SETTLEMENT, DEED_IN_LIEU, GUARANTEE_CLAIM, LITIGATION, ASSET_DISPOSAL, DEBT_SALE, WRITE_OFF, DEVIATIONS |
| LOV-TASK-STATUS | OPEN, IN_PROGRESS, DONE, CANCELED |
| LOV-TEST-RESULT | PASSED, FAILED |
| LOV-TIMER | SERVICE_LEVEL, NOTICE_PERIOD, CURE_PERIOD, PRESCRIPTION, HEARING_DEADLINE, OFFER_VALIDITY, HOLDING_AGE, CLAIM_DEADLINE, INSTALLMENT_DUE |
| LOV-TIMER-STATUS | RUNNING, PAUSED, EXPIRED, STOPPED |
| LOV-TRANSFER-REASON | R01, R02, R03, R04, R05, R06 |
| LOV-VERSION-STATUS | LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| recovery_case | primary_customer_id | party | Many to 1 |
| recovery_case | queue_id | queue | Many to 0 or 1 |
| case_account | case_id | recovery_case | Many to 1 |
| case_account | account_id | loan_account | Many to 1 |
| case_party | case_id | recovery_case | Many to 1 |
| case_party | party_id | party | Many to 1 |
| queue | overflow_queue_id | queue | Many to 0 or 1 |
| assignment | case_id | recovery_case | Many to 1 |
| assignment | task_id | task | Many to 0 or 1 |
| assignment | queue_id | queue | Many to 0 or 1 |
| task | case_id | recovery_case | Many to 1 |
| timer | case_id | recovery_case | Many to 1 |
| timer | task_id | task | Many to 0 or 1 |
| timer | treatment_id | treatment | Many to 0 or 1 |
| interaction | case_id | recovery_case | Many to 1 |
| interaction | party_id | party | Many to 0 or 1 |
| interaction | decision_log_id | decision_log_entry | Many to 0 or 1 |
| interaction | corrects_entry_id | interaction | Many to 0 or 1 |
| interaction | contact_point_id | contact_point | Many to 0 or 1 |
| interaction | treatment_id | treatment | Many to 0 or 1 |
| interaction | proceeds_id | proceeds | Many to 0 or 1 |
| case_entry_exclusion | account_id | loan_account | Many to 1 |
| queue_member | queue_id | queue | Many to 1 |
| queue_measure | queue_id | queue | Many to 1 |
| reference_row | version_id | reference_version | Many to 1 |
| rule_package_version | package_id | rule_package | Many to 1 |
| rule_row | package_version_id | rule_package_version | Many to 1 |
| rule_test_case | package_version_id | rule_package_version | Many to 0 or 1 |

## T4. State machines and workflow

**UNIVERSAL.** 50 rules over 15 states. The full table is in the Business Rules and Routing Logic workbook.

| Rule | From | Event | To |
|---|---|---|---|
| R-UNI-01 | ANY_ACTIVE | PAYMENT_RECEIVED | CASE_CURED_CLOSED |
| R-UNI-02 | ANY_ACTIVE | PAYMENT_RECEIVED | ROUTE_D6_REOPEN |
| R-UNI-03 | ANY_ACTIVE | PAYMENT_RECEIVED | EXCEPTION_QUEUE |
| R-UNI-04 | ANY_ACTIVE | COMPLAINT_RAISED | HELD_DEVIATION |
| R-UNI-05 | ANY_ACTIVE | CUSTOMER_DECEASED | HELD_DEVIATION |
| R-UNI-06 | ANY_ACTIVE | VULNERABILITY_IDENTIFIED | HELD_DEVIATION |
| R-UNI-07 | ANY_ACTIVE | BANKRUPTCY_NOTIFIED | HELD_DEVIATION |
| R-UNI-08 | ANY_ACTIVE | FRAUD_FLAGGED | HELD_DEVIATION |
| R-UNI-09 | ANY_ACTIVE | DEBT_DISPUTED | HELD_DEVIATION |
| R-UNI-10 | ANY_ACTIVE | CONSENT_WITHDRAWN | HELD_CONDUCT |
| R-UNI-11 | ANY_ACTIVE | DATA_SUBJECT_REQUEST | HELD_LEGAL |
| R-UNI-12 | ANY_ACTIVE | CONTACT_DETAIL_CHANGED | RESUME_STATE |
| R-UNI-13 | ANY_ACTIVE | RELIEF_SCHEME_APPLIED | HELD_LEGAL |
| R-UNI-14 | ANY_ACTIVE | ROUTE_OVERRIDDEN | ROUTE_D6_REOPEN |
| R-UNI-15 | ANY_ACTIVE | OVERRIDE_REFUSED | ESCALATED |
| R-UNI-16 | ANY_ACTIVE | CASE_CREATED_IN_ERROR | CANCELED_IN_ERROR |
| R-UNI-17 | ANY_ACTIVE | DUPLICATE_CASE_FOUND | MERGED |
| R-UNI-18 | ANY_ACTIVE | OWNER_UNAVAILABLE | REALLOCATED |
| R-UNI-19 | ANY_ACTIVE | CASELOAD_CAP_BREACHED | REALLOCATED |
| R-UNI-20 | ANY_ACTIVE | LEGAL_HOLD_PLACED | HELD_LEGAL |
| R-UNI-21 | HELD_LEGAL | LEGAL_HOLD_LIFTED | RESUME_STATE |
| R-UNI-22 | ANY_ACTIVE | CLASSIFICATION_CHANGED | ROUTE_D6_REOPEN |
| R-UNI-23 | ANY_ACTIVE | PRODUCT_MIGRATED | RESUME_STATE |
| R-UNI-24 | ANY_ACTIVE | CORRECTION_RECORDED | RESUME_STATE |
| R-UNI-25 | ANY_ACTIVE | PARTNER_NO_RESPONSE | PARTNER_RECALLED |
| and 25 more | | | |

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| None | | | | |

### T5.2 Cross-module interfaces

Calls go through the published Java interfaces: RuleEvaluator and RuleCatalog for rules, TimerScheduler for timers and WorkflowGateway for workflows; P3 for the case, P7 for the decision log, P4 for access and the rule package tables, P5 for documents, P6 for notices, P1 for ACE case data. Case data stays in the recovery schema; Temporal holds the execution of a case workflow from Epic 3 (ADR-011).

### T5.3 Events

| Event | Direction |
|---|---|
| CaseCreated | Published |
| CaseAllocated | Published |
| CaseAllocationFailed | Published |
| CaseTransferred | Published |
| CaseStateChanged | Published |
| TimerDue | Published |
| TimerBreached | Published |

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Case record | Queue and allocation |
|---|---|---|
| RW-CASEOWN Case owner | CRU | R |
| RW-TEAMMGR Team manager | R | CRUA |
| RW-PHONECOL Phone collector | R | R |
| RW-FIELDCOL Field collector | R | R |
| RW-RESTRUCT Restructuring officer (FCR) | RU | R |
| RW-SPECIAL Hardship and vulnerability specialist | RU | R |
| RW-COMPLAIN Complaint officer | RU | R |
| RW-FRAUD Fraud investigator | RU | R |
| RW-LITOFF Litigation officer | RU | R |
| RW-ENFORCE Enforcement owner | RU | R |
| RW-LEGAL Legal counsel | R | - |
| RW-SALEOFF Sale officer | RU | R |
| RW-NPAMGR NPA and asset manager | R | - |
| RW-DEBTSALE Debt sale officer | RU | R |
| RW-WRITEOFF Write-off team member | R | - |
| RW-CREDITAD Credit Administration officer | R | - |
| RW-GUARANT Guarantee officer | RU | R |
| RW-AGENCYMG Partner and agency manager | R | R |
| RW-CONDUCT Conduct and QA officer | R | R |
| RW-CAPACITY Capacity and workforce planner | R | RU |
| RW-PRODHEAD Product head (Mortgage, HP, SSME) | R | R |
| RW-HEADLIT Head of Litigation | R | R |
| RW-HEADNPA Head of NPA | R | - |
| RW-HEADASL Head of Asset Liquidity | R | - |
| RW-CREDCOMM Credit approval committee member | R | - |
| RW-WOCOMM Write-off committee member | R | - |
| RW-RISK Risk and model risk officer | R | R |
| RW-COE Center of excellence analyst | R | R |
| RW-DATASTEW Data steward and data product owner | R | - |
| RW-FINANCE Finance and CFO delegate | R | - |
| RW-AUDIT Internal audit | R | R |
| RW-COMPLY Compliance and PDPA officer | R | - |
| RW-PLATADM Platform administrator | R | R |
| RW-BIANAL Reporting and BI analyst | R | R |
| RW-TRIBE Tribe lead and squad members | R | R |
| PT-AGENCY Collection agency (OA) user | R | - |
| PT-LAWFIRM Law firm user | R | - |
| SY-CASEWF Case workflow module | CRU | CRU |
| SY-RULES Drools evaluator | R | R |
| SY-DATALOAD Data load from COLLINS | CU | - |
| SY-OCR OCR and extraction pipeline | R | - |
| SY-AGENT Agent platform | R | R |

### T6.2 Authentication and authorization

Entra ID single sign-on through the ACE front end; each endpoint declares its capability area and right; scope filters every query; masking applies to personal fields; service identities for jobs and agents.

## T7. Non-functional requirements

| ID | Requirement | Target | Status |
|---|---|---|---|
| NFR-001 | The case store holds one case per customer and product for every account at 90 or more days past due across Mortgage, Hire Purchase and SSME. | About 23,600 open cases at go-live and 26,500 at the end of 2027, from 3,110 new accounts at 90 days past due a month. Confirmed under DL15 | Proposed from the volume forecast |
| NFR-002 | The system supports the peak number of staff users signed on at once. | About 370 staff online in the busiest hour, of 914 named users | Proposed from the volume forecast |
| NFR-003 | The system supports the peak number of partner users signed on at once across 73 agencies, 11 to 12 law firms, 4 auction vendors and 35 buyers. | About 50 partner users online in the busiest hour, of about 320 named users | Proposed from the volume forecast |
| NFR-004 | The document store holds the annual inbound document volume with its growth rate. | About 860,000 documents in 2027, rising with 15 percent inflow growth a year | Proposed from the volume forecast |
| NFR-005 | The restructure path carries the monthly case volume reaching the Workbench. | About 3,000 restructure accounts a month reach the bank's restructure process today | Proposed |
| NFR-006 | The deed in lieu path carries its target monthly volume. | 1,000 cases a month in 2027, from 685 today | Proposed |
| NFR-007 | The decision log holds one record for every decision on every case for the full retention period without degrading query time. | About 36 GB for the decision log and the interaction ledger by the end of 2031; a single case history query under 2 seconds at that size | Proposed, DL11 |
| NFR-069 | The document hub holds the full recovery document estate as a system of record, including every version and every held document, with storage sized for growth. | About 5.8 million documents and 2.8 TB by the end of 2031, with every version and held document | Proposed, DL11 |
| NFR-070 | The interaction ledger holds every interaction on every open and closed case within its retention period, and reads a single case history inside the user wait. | One case history reads in under 2 seconds with the ledger at its 2031 size | Proposed, DL11 |
| NFR-008 | A screen responds within its target under normal load. | Under 2 seconds | Proposed |
| NFR-009 | The case record view loads for a case with 50 documents. | Under 2 seconds | Proposed |
| NFR-010 | An agent returns an answer within its target, after which the rule result is used and the case still routes. | Under 60 seconds | Proposed |
| NFR-011 | A rule evaluation at a routing decision completes inside the user's wait. | Under 300 milliseconds per rule evaluation at the 95th percentile | Proposed, DL11 |
| NFR-012 | A search across cases and documents returns within its target. | Under 3 seconds for a search across cases; under 5 seconds across documents | Proposed, DL11 |

## T8. Requirement traceability

| Requirement | Feature | Story | Test |
|---|---|---|---|
| REQ-CWC-001 | FEAT-CWC-01 | RWB-E1-018 | TC-E1-018-01 |
| REQ-CWC-002 | FEAT-CWC-01 | RWB-E1-018 | TC-E1-018-01 |
| REQ-CWC-003 | FEAT-CWC-01 | RWB-E1-018 | TC-E1-018-01 |
| REQ-CWC-004 | FEAT-CWC-01 | RWB-E1-018 | TC-E1-018-01 |
| REQ-CWC-005 | FEAT-CWC-01 | RWB-E1-018 | TC-E1-018-01 |
| REQ-CWC-006 | FEAT-CWC-01 | RWB-E1-018 | TC-E1-018-01 |
| REQ-CWC-007 | FEAT-CWC-01 | RWB-E1-018 | TC-E1-018-01 |
| REQ-CWC-008 | FEAT-CWC-01 | RWB-E1-018 | TC-E1-018-01 |
| REQ-CWC-009 | FEAT-CWC-01 | RWB-E1-018 | TC-E1-018-01 |
| REQ-CWC-010 | FEAT-CWC-01 | RWB-E1-018 | TC-E1-018-01 |
| REQ-CWC-011 | FEAT-CWC-01 | RWB-E1-018 | TC-E1-018-01 |
| REQ-CWC-012 | FEAT-CWC-01 | RWB-E1-018 | TC-E1-018-01 |
| REQ-CWC-013 | FEAT-CWC-01 | RWB-E1-018 | TC-E1-018-01 |
| REQ-CWC-014 | FEAT-CWC-01 | RWB-E1-018 | TC-E1-018-01 |
| REQ-CWC-015 | FEAT-CWC-01 | RWB-E1-018 | TC-E1-018-01 |
| REQ-CWC-016 | FEAT-CWC-01 | RWB-E1-018 | TC-E1-018-01 |
| REQ-CWC-017 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-CWC-018 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-CWC-019 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-CWC-020 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-CHO-001 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-CHO-002 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-CHO-003 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-CHO-004 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-CHO-005 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-CHO-006 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-CHO-007 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-CHO-008 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-CHO-009 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-CHO-010 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-WKM-001 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-WKM-002 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-WKM-003 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-WKM-004 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-WKM-005 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-WKM-006 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-WKM-007 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-WKM-008 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-WKM-009 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-WKM-010 | None | Written one epic ahead | With the story |
| REQ-WKM-011 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-WKM-012 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-WKM-013 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-WKM-014 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-WKM-015 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-WKM-016 | FEAT-CHO-01 | RWB-E2-001 | TC-E2-001-01 |
| REQ-DRI-007 | None | RWB-E1-070 | TC-E1-070-01 |
| REQ-DRI-010 | None | RWB-E1-070 | TC-E1-070-05 |
| REQ-DRI-005 | None | RWB-E1-071 | TC-E1-071-01 |
| REQ-DRI-007 | None | RWB-E1-071 | TC-E1-071-03 |
| REQ-DRI-010 | None | RWB-E1-071 | TC-E1-071-06 |
| REQ-CWC-016 | FEAT-CWC-21 | RWB-E1-072 | TC-E1-072-01 |
| REQ-DRI-001 | FEAT-DRI-07 | RWB-E1-072 | TC-E1-072-01 |
| REQ-DRI-004 | FEAT-DRI-07 | RWB-E1-072 | TC-E1-072-02 |
| REQ-DRI-011 | FEAT-DRI-01 | RWB-E1-072 | TC-E1-072-06 |
| REQ-CWC-013 | FEAT-CWC-14 | RWB-E1-073 | TC-E1-073-01 |
| REQ-CWC-014 | FEAT-CWC-14 | RWB-E1-073 | TC-E1-073-02 |
| REQ-DRI-004 | FEAT-DRI-07 | RWB-E1-073 | TC-E1-073-15 |
| REQ-CWC-008 | FEAT-CWC-07 | RWB-E1-073 | TC-E1-073-07 |
| REQ-DRI-007 | None | RWB-E2-037 | TC-E2-037-01 |
| REQ-DRI-001 | FEAT-DRI-01 | RWB-E2-038 | TC-E2-038-01 |
| REQ-DRI-005 | FEAT-DRI-05 | RWB-E2-038 | TC-E2-038-02 |
| REQ-DRI-007 | None | RWB-E2-039 | TC-E2-039-01 |
| REQ-DRI-005 | FEAT-DRI-05 | RWB-E2-040 | TC-E2-040-01 |
| REQ-CWC-013 | FEAT-CWC-16 | RWB-E2-041 | TC-E2-041-01 |
| REQ-DRI-011 | FEAT-CWC-16 | RWB-E2-041 | TC-E2-041-10 |
| REQ-CWC-013 | FEAT-CWC-14 | RWB-E2-042 | TC-E2-042-01 |
| REQ-CWC-014 | FEAT-CWC-14 | RWB-E2-042 | TC-E2-042-01 |
| REQ-DRI-001 | FEAT-DRI-07 | RWB-E2-043 | TC-E2-043-01 |
| REQ-DRI-005 | FEAT-DRI-07 | RWB-E2-043 | TC-E2-043-02 |
| REQ-CWC-016 | FEAT-DRI-07 | RWB-E2-043 | TC-E2-043-01 |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-P3-001 | GET | /api/recovery/v1/cases | Case record R | E1 |
| API-P3-002 | GET | /api/recovery/v1/cases/{caseId} | Case record R | E1 |
| API-P3-003 | GET | /api/recovery/v1/cases/{caseId}/timeline | Case record R | E2 |
| API-P3-004 | GET | /api/recovery/v1/cases/{caseId}/accounts | Case record R | E1 |
| API-P3-005 | GET | /api/recovery/v1/cases/{caseId}/parties | Case record R | E1 |
| API-P3-006 | POST | /api/recovery/v1/cases/{caseId}/transfer | Queue and allocation U | E2 |
| API-P3-007 | POST | /api/recovery/v1/cases/{caseId}/legal-hold | Case record U | E2 |
| API-P3-008 | GET | /api/recovery/v1/me/tasks | Case record R | E2 |
| API-P3-009 | PATCH | /api/recovery/v1/tasks/{taskId} | Case record U | E2 |
| API-P3-010 | GET | /api/recovery/v1/queues | Queue and allocation R | E2 |
| API-P3-011 | GET | /api/recovery/v1/queues/{queueId}/cases | Queue and allocation R | E2 |
| API-P3-012 | POST | /api/recovery/v1/queues/{queueId}/placements | Queue and allocation C | E2 |
| API-P3-013 | GET | /api/recovery/v1/cases/{caseId}/timers | Case record R | E1 |
| API-P3-014 | GET | /api/recovery/v1/cases/{caseId}/interactions | Case record R | E1 |
| API-P3-015 | POST | /api/recovery/v1/cases/{caseId}/interactions | Case record C | E1 |
| API-P3-016 | GET | /api/recovery/v1/cases/{caseId}/next-action | Case record R | E2 |
| API-P3-017 | GET | /api/recovery/v1/cases/export | Case record R | E1 |
| API-P3-018 | GET | /api/recovery/v1/admin/parameters | Rules and parameters R | E1 |
| API-P3-019 | GET | /api/recovery/v1/admin/change-log | Rules and parameters R | E1 |
| API-P3-020 | GET | /api/recovery/v1/admin/rule-packages | Rules and parameters R | E1 |
| API-P3-021 | POST | /api/recovery/v1/admin/rule-packages/{packageCode}/versions | Rules and parameters C | E1 |
| API-P3-022 | GET | /api/recovery/v1/admin/rule-packages/{packageCode}/versions | Rules and parameters R | E1 |
| API-P3-023 | POST | /api/recovery/v1/admin/rule-package-versions/{versionId}/approve | Rules and parameters A | E1 |
| API-P3-024 | POST | /api/recovery/v1/admin/rule-package-versions/{versionId}/rollback | Rules and parameters U | E1 |
| API-P3-025 | GET | /api/recovery/v1/admin/rule-package-versions/{versionId}/dry-run | Rules and parameters R | E1 |
| API-P3-026 | GET | /api/recovery/v1/admin/rule-packages/change-report | Rules and parameters R | E2 |
| API-P3-027 | POST | /api/recovery/v1/admin/workflows/smoke | Platform administration C | E1 |

### T-A.2 Endpoint detail

#### API-P3-001 GET /cases

| Item | Value |
|---|---|
| Purpose | List cases in the caller's scope with filters and paging |
| Request | Query: product, stage, status, owner, queue, deviation, ageFrom, ageTo, page, size, sort |
| Response | CasePage |
| Errors | 401, 403, 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

#### API-P3-002 GET /cases/{caseId}

| Item | Value |
|---|---|
| Purpose | Read one case with accounts, parties, stage, owner, clocks and deviations |
| Request | None |
| Response | Case |
| Errors | 401, 403, 404, 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

#### API-P3-003 GET /cases/{caseId}/timeline

| Item | Value |
|---|---|
| Purpose | Read the case history as one timeline |
| Request | Query: type, from, to |
| Response | TimelinePage |
| Errors | 401, 403, 404, 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

#### API-P3-004 GET /cases/{caseId}/accounts

| Item | Value |
|---|---|
| Purpose | Read the accounts on the case with balances and arrears |
| Request | None |
| Response | CaseAccount[] |
| Errors | 401, 403, 404, 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

#### API-P3-005 GET /cases/{caseId}/parties

| Item | Value |
|---|---|
| Purpose | Read the parties on the case, masked by role |
| Request | None |
| Response | CaseParty[] |
| Errors | 401, 403, 404, 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

#### API-P3-006 POST /cases/{caseId}/transfer

| Item | Value |
|---|---|
| Purpose | Transfer the case to another owner or queue with a reason |
| Request | TransferRequest |
| Response | Assignment |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Queue and allocation, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P3-007 POST /cases/{caseId}/legal-hold

| Item | Value |
|---|---|
| Purpose | Place or lift a legal hold on the case |
| Request | LegalHoldRequest |
| Response | Case |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Case record, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P3-008 GET /me/tasks

| Item | Value |
|---|---|
| Purpose | List the caller's open tasks |
| Request | Query: due, type, page, size |
| Response | TaskPage |
| Errors | 401, 403, 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

#### API-P3-009 PATCH /tasks/{taskId}

| Item | Value |
|---|---|
| Purpose | Complete or reassign a task |
| Request | TaskUpdate |
| Response | Task |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Case record, right U, scope applied |
| Idempotency | Not applicable |

#### API-P3-010 GET /queues

| Item | Value |
|---|---|
| Purpose | List queues with counts, age and cap use |
| Request | None |
| Response | Queue[] |
| Errors | 401, 403, 503 |
| Authorization | Queue and allocation, right R, scope applied |
| Idempotency | Not applicable |

#### API-P3-011 GET /queues/{queueId}/cases

| Item | Value |
|---|---|
| Purpose | List the cases in a queue |
| Request | Query: page, size, sort |
| Response | CasePage |
| Errors | 401, 403, 404, 503 |
| Authorization | Queue and allocation, right R, scope applied |
| Idempotency | Not applicable |

#### API-P3-012 POST /queues/{queueId}/placements

| Item | Value |
|---|---|
| Purpose | Place a case on a queue from a model or an agent |
| Request | PlacementRequest |
| Response | Assignment |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Queue and allocation, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P3-013 GET /cases/{caseId}/timers

| Item | Value |
|---|---|
| Purpose | Read the clocks on a case: stage, service level, prescription, notice |
| Request | None |
| Response | Timer[] |
| Errors | 401, 403, 404, 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

#### API-P3-014 GET /cases/{caseId}/interactions

| Item | Value |
|---|---|
| Purpose | Read the interaction ledger for a case |
| Request | Query: channel, from, to, page, size |
| Response | InteractionPage |
| Errors | 401, 403, 404, 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

#### API-P3-015 POST /cases/{caseId}/interactions

| Item | Value |
|---|---|
| Purpose | Record a contact, promise or hand-over |
| Request | InteractionRequest |
| Response | Interaction |
| Errors | 401, 403, 404, 422, 503 |
| Authorization | Case record, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P3-016 GET /cases/{caseId}/next-action

| Item | Value |
|---|---|
| Purpose | Read the next action of a case with its owner, due date, wait and overdue state |
| Request | None |
| Response | NextAction |
| Errors | 401, 403, 404, 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

#### API-P3-017 GET /cases/export

| Item | Value |
|---|---|
| Purpose | Export the filtered case list to Excel, masked by role, with access event AC-EXPT |
| Request | Query: product, stage, status, owner, queue, team, deviation, ageFrom, ageTo, sort |
| Response | Binary |
| Errors | 401, 403, 422, 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

#### API-P3-018 GET /admin/parameters

| Item | Value |
|---|---|
| Purpose | Read the parameter catalog with the value in force per environment; secrets listed without values |
| Request | Query: key, kind, owner, environment |
| Response | Parameter[] |
| Errors | 401, 403, 503 |
| Authorization | Rules and parameters, right R, scope applied |
| Idempotency | Not applicable |

#### API-P3-019 GET /admin/change-log

| Item | Value |
|---|---|
| Purpose | Report every reference and rule package version change for audit, with its checklist and effect, as JSON or CSV |
| Request | Query: from, to, table, format, page, size |
| Response | ChangeLogPage |
| Errors | 401, 403, 422, 503 |
| Authorization | Rules and parameters, right R, scope applied |
| Idempotency | Not applicable |

#### API-P3-020 GET /admin/rule-packages

| Item | Value |
|---|---|
| Purpose | List rule packages with the version in force and its status |
| Request | Query: status, page, size |
| Response | RulePackage[] |
| Errors | 401, 403, 503 |
| Authorization | Rules and parameters, right R, scope applied |
| Idempotency | Not applicable |

#### API-P3-021 POST /admin/rule-packages/{packageCode}/versions

| Item | Value |
|---|---|
| Purpose | Upload an Excel workbook in Drools decision-table format, compile it, run the checks and the scenarios and store the version LOADED |
| Request | Multipart: file (xlsx), validFrom |
| Response | RulePackageVersion |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Rules and parameters, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P3-022 GET /admin/rule-packages/{packageCode}/versions

| Item | Value |
|---|---|
| Purpose | List the versions of one package with status, checksum, test result and dry run counts |
| Request | Query: status |
| Response | RulePackageVersion[] |
| Errors | 401, 403, 404, 503 |
| Authorization | Rules and parameters, right R, scope applied |
| Idempotency | Not applicable |

#### API-P3-023 POST /admin/rule-package-versions/{versionId}/approve

| Item | Value |
|---|---|
| Purpose | Approve a loaded package version; the author cannot approve |
| Request | None |
| Response | RulePackageVersion |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Rules and parameters, right A, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P3-024 POST /admin/rule-package-versions/{versionId}/rollback

| Item | Value |
|---|---|
| Purpose | Roll back a package version in force to the version before it, with a reason |
| Request | RollbackRequest |
| Response | RulePackageVersion |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Rules and parameters, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P3-025 GET /admin/rule-package-versions/{versionId}/dry-run

| Item | Value |
|---|---|
| Purpose | Read the dry run result of a loaded version against the open cases it would decide |
| Request | None |
| Response | DryRunResult |
| Errors | 401, 403, 404, 503 |
| Authorization | Rules and parameters, right R, scope applied |
| Idempotency | Not applicable |

#### API-P3-026 GET /admin/rule-packages/change-report

| Item | Value |
|---|---|
| Purpose | Report every package version change for audit, with its checklist, checksum, author, approver and the decisions it made (RWB-E2-041) |
| Request | Query: from, to, packageCode, format, page, size |
| Response | RuleChangeReportPage, JSON or CSV |
| Errors | 401, 403, 422, 503 |
| Authorization | Rules and parameters, right R, scope applied |
| Idempotency | Not applicable |

#### API-P3-027 POST /admin/workflows/smoke

| Item | Value |
|---|---|
| Purpose | Run PlatformSmokeWorkflow on demand in the caller's environment |
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

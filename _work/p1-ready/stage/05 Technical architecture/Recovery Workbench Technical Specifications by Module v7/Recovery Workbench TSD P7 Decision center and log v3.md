SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench P7 Decision center and log

Technical specification. SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD P7 Decision center and log |
| Document ID | P7-RWB-TSD-v3 |
| Version | 3 |
| Status | Draft |
| Date | 22 November 2026 |
| Supersedes | Version 2, 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads (GAP-1999; ASM-3225: no squad is named per service) |
| Decision | D-RCV-60 microservice realignment |
| Status note | Draft: no approval of version 3 is recorded (GAP-1998; ASM-3217) |
| Change | 3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD P7 Decision center and log | FSD | Pair |
| Recovery Workbench Target Architecture | Architecture | Parent |
| Recovery Workbench Logical Data Model and Data Dictionary | Data | Source of T3 |
| Recovery Workbench API Specification | API | Source of appendix T-A |
| Recovery Workbench Microservice Ownership Map v1 | Ownership | Owner of every table, endpoint, event, workflow and job in T0 and T5.2 |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit, PII and SOC logging | REUSE | ACE common module | Called through the published interface |
| Scheduler and batch | REUSE | ACE pattern: Quartz and Spring Batch | Jobs in the Batch and Scheduling Design |
| Outbox and retry | REUSE | Error Handling and Resilience Standard | Through P2 |
| Rules evaluation | REUSE | Rules Engine Design | Through the rules component |

Under D-RCV-60 the scheduler and batch row is delivered by the Temporal layer (ADR-016): Temporal Schedules and event-started workflows in the owning service replace the Quartz and Spring Batch jobs (DP-10). The outbox and retry row is delivered by the Kafka outbox, inbox and retry topics (ADR-015; DP-09).

## T0. Service

P7 Decision center and log is one of the 19 services of Architecture v5: `rwb-decision` (service name Decision and rules, module P7, wave 1, service epic `RWB-SVC-P7`). Version 3 adds this section so that the specification is read as the specification of one service: its identity, what it owns, and the decoupling patterns that replace the monolith's in-process calls. Every owner is taken from Microservice Ownership Map v1 and every identifier from Template and Rules R4 (ADR-013, ADR-014).

P7 owns the central decision ledger and the rule package registry; every service publishes DecisionRecorded to `rwb.decision-record.v1` and evaluates rules locally (DP-03, DP-04).

### T0.1 Service identity

| Item | Value |
|---|---|
| Module | P7 Decision center and log |
| Service | `rwb-decision` (Decision and rules) |
| Service epic | `RWB-SVC-P7` |
| Wave | 1 |
| Schema | `rwb_decision` |
| Database login | `rwb_decision`: one login per service, with its own connection pool cap |
| REST base | `/api/recovery/decision/v1` |
| Kafka topic | `rwb.decision.events.v1`, with `.retry` and `.dlt` topics |
| Event names | `rwb.decision.<Event>.v1`, CloudEvents 1.0 in binary mode, key `caseId` |
| Temporal | namespace `rwb-recovery`; task queue `rwb-decision` |
| Java package | `th.co.scb.ace.workbench.recovery.decision` |
| Edge | gateway-bff for the staff screens of this service |
| Contract artefacts | `05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml`; `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-decision.asyncapi.yaml` |
| Suggested owner, app development | TechX (suggested; any team may pick up this story) |
| Suggested owner, ACE DB | ACE team (suggested; any team may pick up this story) |

### T0.2 What this service owns

Architecture v5 slide 41 gives this service: approvals, central decision ledger, DMN model registry. Table T0.2 states the same ownership in the form the Ownership Map uses, with the counts this specification carries. A table that the map assigns to another service is not built here, whatever T3 says (see the note under T3).

| Area | Owner and artefact | Count |
|---|---|---|
| Business tables in `rwb_decision` | `approval`, `decision_log_entry`, `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` | 6 |
| REST operations | appendix T-A and `rwb-decision.yaml` | 15 |
| Events published | EV-08 DecisionRecorded, EV-09 ApprovalRequested, EV-30 RulePackageInForce | 3 |
| Workflows and schedules | ApprovalWorkflow | 1 |
| Jobs | JOB-13, JOB-14, JOB-20 | 3 |

### T0.3 Decoupling patterns applied

The left column is the pattern of Template and Rules R5.5; the middle column quotes the line of this specification that carries the legacy marker, where one is present; the right column is what replaces it in this service.

| DP | Legacy marker in this specification | How the service lands it |
|---|---|---|
| DP-01 | — | Owns its tables in `rwb_decision`; no other service reads them (ADR-014). |
| DP-02 | — | One login, `rwb_decision`, with its own connection pool cap. |
| DP-03 | `…with reasons, approval within delegation, decision log store and writer. It reaches other modules…` | Local decision record plus DecisionRecorded (EV-08) on `rwb.decision-record.v1`. |
| DP-07 | `DF-DEC-003 / decision_code / LOV / varchar(8) / Yes / LOV-DECISION / Workbench` | Reference data and lists of values from the `rwb-case` contract (H RWB-PLT-E1043-CON). |
| DP-08 | `RW-CASEOWN Case owner / R` | Authorisation through the `rwb-access` authorise contract and the guard library (H RWB-PLT-E1037-CON). |
| DP-09 | `…state machine of its own; the module acts on events from P3 and writes through the decision…` | Outbox and inbox library; CloudEvents on `rwb.decision.events.v1` with retry topics and `.dlt`. |
| DP-10 | `Scheduler and batch / REUSE / ACE pattern: Quartz and Spring Batch / Jobs in the Batch and…` | Temporal Schedules and event-started workflows through the workflow kit (ADR-016). |
| DP-11 | `…reaches other modules only through their published interfaces and other systems only through COLLINS,…` | One REST hop, 2 s timeout, breaker; the consumer builds against the provider's fake (ADR-020). |
| DP-13 | `API-P7-001 / GET / /api/recovery/v1/cases/{caseId}/recommendation / Decision…` | REST base `/api/recovery/decision/v1`. |
| DP-14 | — | Topic `rwb.decision.events.v1`, retry topics and `.dlt`; naming library (H RWB-PLT-E1047-CON). |
| DP-15 | — | Per-service Flyway sequence in `rwb_decision`. |
| DP-17 | `INT-19 / Data lake and Power BI / Out / Daily batch…` | No data lake: reporting reads events; the lake copy is removed (ADR-018). |
| DP-18 | `NFR-077 / A failed write to the interaction ledger raises an incident, and no entry is discarded.…` | Interaction ledger owned by `rwb-source-data` (default ruling; DP-18). |
| DP-19 | `…with its routing details for the decision screen` | Screens composed by gateway-bff; one composite route per screen (H RWB-PLT-N001-CON). |

### T0.4 What this service is not

- It holds no other service's table and no ACE table beyond the read-only `recovery.v_ace_*` views (DP-01, DP-05).
- It runs no shared Quartz job and touches no ACE batch table (DP-10; ADR-016).
- It holds no business table of another service: every decision arrives as an event or a contract call (EV-08).
- It is not a monolith module: the published Java interface of T2 is replaced by the contract set of T5.2 (DP-11; ADR-020).

## T1. Architecture overview

P7 Decision center and log is delivered as the service `rwb-decision` (module P7, wave 1, service epic `RWB-SVC-P7`): one repository, one pipeline, one schema `rwb_decision` with one login, behind gateway-bff (ADR-013, ADR-014). It covers: recommendation with reasons, approval within delegation, decision log store and writer. It reaches other modules only through the contracts of T5.2 and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| DecisionCenterAndLogController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| DecisionCenterAndLogService | Business logic; calls the rules component; writes the decision log entry before any change |
| DecisionCenterAndLogRepository | Reads and writes the module's tables only |
| Jobs | Temporal Schedules and event-started workflows this service owns (T0.2, T5.2.1; DP-10) |
| Published interface | The contracts of T5.2: REST operations, events and workflows other services call; no table is read across modules (DP-11) |

The published interface of this table is the contract set of T5.2: the REST operations, the events and the workflows, not a Java interface in a shared classpath (DP-11; ADR-020). Components that the Ownership Map places in another service are stated in T0.2 and T5.2 and are built by that service.

## T3. Data model

Every object of T3 that Microservice Ownership Map v1 assigns to `rwb-decision` lives in schema `rwb_decision` with the standard columns of T3.0 (DP-01, DP-15; ADR-014). `approval`, `decision_log_entry` and the four rule package tables are P7's under the Ownership Map; T3.1 of TSD P3 v3 and TSD P4 v3 place the rule package tables with P4, which Architecture v5 does not support (GAP-1993; ASM-3220).

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

**decision_log_entry** (NEW). One record per decision. Append only and hash chained.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-DEC-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-DEC-002 | case_id | CROSS_REF | uuid | No | None | Workbench |
| DF-DEC-003 | decision_code | LOV | varchar(8) | Yes | LOV-DECISION | Workbench |
| DF-DEC-004 | rule_id | TEXT | varchar(20) | No | None | Workbench |
| DF-DEC-005 | rule_version | TEXT | varchar(20) | No | None | Workbench |
| DF-DEC-006 | model_version | TEXT | varchar(40) | No | None | COLLINS |
| DF-DEC-007 | agent_version | TEXT | varchar(40) | No | None | Workbench |
| DF-DEC-008 | inputs_ref | TEXT | varchar(400) | Yes | None | Workbench |
| DF-DEC-009 | recommendation | TEXT | jsonb | No | None | Workbench |
| DF-DEC-010 | approver_user_id | USER_REF | uuid | No | None | Workbench |
| DF-DEC-011 | approval_level | LOV | varchar(4) | No | LOV-APPROVAL-LEVEL | Workbench |
| DF-DEC-012 | final_call | TEXT | varchar(40) | Yes | None | Workbench |
| DF-DEC-013 | override_reason | TEXT | varchar(1000) | No | None | Workbench |
| DF-DEC-014 | actions | TEXT | jsonb | No | None | Workbench |
| DF-DEC-015 | outcome | TEXT | jsonb | No | None | Workbench |
| DF-DEC-016 | decided_at | DATE | timestamptz | Yes | None | Workbench |
| DF-DEC-017 | prev_hash | TEXT | char(64) | Yes | None | Workbench |
| DF-DEC-018 | entry_hash | TEXT | char(64) | Yes | None | Workbench |
| DF-DEC-028 | chain_seq | NUMBER | bigint | Yes | None | Workbench |
| DF-DEC-029 | corrects_entry_id | CROSS_REF | uuid | No | None | Workbench |
| DF-DEC-030 | actor_user_id | USER_REF | uuid | No | None | Workbench |
| DF-DEC-031 | idempotency_key | TEXT | varchar(80) | No | None | Workbench |

**approval** (NEW). An item waiting for approval, routed to the level the delegation of authority requires.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-DEC-032 | id | TEXT | uuid | Yes | None | Workbench |
| DF-DEC-033 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-DEC-034 | decision_code | LOV | varchar(8) | Yes | LOV-DECISION | Workbench |
| DF-DEC-035 | regulation_item | TEXT | varchar(10) | No | None | Workbench |
| DF-DEC-036 | capability_area | LOV | varchar(30) | Yes | LOV-CAPABILITY | Workbench |
| DF-DEC-037 | route_role_code | LOV | varchar(20) | No | LOV-ROLE | Workbench |
| DF-DEC-038 | approval_level | LOV | varchar(4) | No | LOV-APPROVAL-LEVEL | Workbench |
| DF-DEC-039 | delegation_limit_id | CROSS_REF | uuid | No | None | Workbench |
| DF-DEC-040 | limit_version | TEXT | varchar(20) | No | None | Workbench |
| DF-DEC-041 | product_group | LOV | varchar(15) | Yes | LOV-PRODUCT | Workbench |
| DF-DEC-042 | amount | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-DEC-043 | terms | TEXT | jsonb | No | None | Workbench |
| DF-DEC-044 | prepared_by | USER_REF | uuid | Yes | None | Workbench |
| DF-DEC-045 | assigned_user_id | USER_REF | uuid | No | None | Workbench |
| DF-DEC-046 | status | LOV | varchar(20) | Yes | LOV-APPROVAL-STATUS | Workbench |
| DF-DEC-047 | due_at | DATE | timestamptz | No | None | Workbench |
| DF-DEC-048 | escalation_level | NUMBER | integer | Yes | None | Workbench |
| DF-DEC-049 | source_type | TEXT | varchar(20) | Yes | None | Workbench |
| DF-DEC-050 | source_ref | TEXT | varchar(60) | Yes | None | Workbench |
| DF-DEC-051 | rule_id | TEXT | varchar(20) | No | None | Workbench |
| DF-DEC-052 | rule_version | TEXT | varchar(20) | No | None | Workbench |
| DF-DEC-053 | decision_log_id | CROSS_REF | uuid | No | None | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-APPROVAL-LEVEL | L1, L2, L3, L4, L5, L6 |
| LOV-APPROVAL-STATUS | WAITING, HELD_NO_LIMIT, APPROVED, REFUSED, RETURNED |
| LOV-CAPABILITY | CASE_RECORD, QUEUE_AND_ALLOCATION, TREATMENT_AND_OFFER, LITIGATION, ASSET_AND_DISPOSAL, DEBT_SALE, WRITE_OFF_AND_POSTING, DOCUMENTS, RULES_AND_PARAMETERS, REFERENCE_DATA, DECISION_LOG, PARTNER_PORTAL, REPORTING, PLATFORM_ADMINISTRATION |
| LOV-PRODUCT | MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| decision_log_entry | case_id | recovery_case | Many to 0 or 1 |
| decision_log_entry | corrects_entry_id | decision_log_entry | Many to 0 or 1 |
| approval | case_id | recovery_case | Many to 1 |
| approval | delegation_limit_id | delegation_limit | Many to 0 or 1 |
| approval | decision_log_id | decision_log_entry | Many to 0 or 1 |

## T4. State machines and workflow

No case state machine of its own; the module acts on events from P3 and writes through the decision log.

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-19 | Data lake and Power BI | Out | Daily batch | Daily |
| INT-20 | COLLINS | Out | Daily batch to the data lake | Daily |

### T5.2 Contracts

Version 3 states every cross-module dependency of this module as a contract, so that the service is built against a published artefact and its fake (ADR-020; DP-11). The artefact per call type is: OpenAPI 3.1 for REST, AsyncAPI 3.0 for Kafka, the Temporal interface named here for a workflow or activity, the Interface Specifications manifest for a file, the Nexus operation for the ACE restructure calculator, and a grant on the view for SQL. No row of this section reads another service's table (DP-01). Every consumed contract is class C (Template and Rules R5.4): it never blocks the build, because the consumer builds against the fake, and the real cross-service behaviour is class I work on an integration story. Architecture v5 slides 13 to 20 name a few operations differently from the published files of 22 November 2026; the published file is the artefact the fake is generated from and is the one cited here (GAP-1997; ASM-3224).

#### T5.2.1 Contracts provided

The REST operations of this service are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml` (5.0.0, 22 November 2026) under the base `/api/recovery/decision/v1`. Appendix T-A holds the endpoint IDs, the access right and the first release of each one.

| # | Method | Path | operationId |
|---|---|---|---|
| 1 | GET | `/cases/{caseId}/recommendation` | `getCasesCaseidRecommendation` |
| 2 | GET | `/approvals` | `getApprovals` |
| 3 | POST | `/approvals/{approvalId}/approve` | `postApprovalsApprovalidApprove` |
| 4 | POST | `/approvals/{approvalId}/return` | `postApprovalsApprovalidReturn` |
| 5 | POST | `/approvals/{approvalId}/refuse` | `postApprovalsApprovalidRefuse` |
| 6 | GET | `/decision-log` | `getDecisionLog` |
| 7 | GET | `/decision-log/{entryId}` | `getDecisionLogEntryid` |
| 8 | GET | `/admin/rule-packages` | `getAdminRulePackages` |
| 9 | GET | `/admin/rule-packages/{packageCode}/versions` | `getAdminRulePackagesPackagecodeVersions` |
| 10 | POST | `/admin/rule-packages/{packageCode}/versions` | `postAdminRulePackagesPackagecodeVersions` |
| 11 | POST | `/admin/rule-package-versions/{versionId}/approve` | `postAdminRulePackageVersionsVersionidApprove` |
| 12 | POST | `/admin/rule-package-versions/{versionId}/rollback` | `postAdminRulePackageVersionsVersionidRollback` |
| 13 | GET | `/admin/rule-package-versions/{versionId}/dry-run` | `getAdminRulePackageVersionsVersionidDryRun` |
| 14 | GET | `/admin/rule-packages/change-report` | `getAdminRulePackagesChangeReport` |
| 15 | GET | `/approvals/{approvalId}` | `getApprovalsApprovalid` |

Workflows, schedules, files and views this service provides:

| Contract | Type | Called by or target | Note |
|---|---|---|---|
| ApprovalWorkflow | Temporal workflow | P3 rwb-case and the stage services | Kit template; runs on rwb-decision |
| Rule promote, 00:01 | Temporal Schedule | P7 rwb-decision | JOB-20; publishes RulePackageInForce (EV-30) |
| Chain check, 02:00 | Temporal Schedule | P7 rwb-decision | JOB-14 hash-chain check |
| Daily ledger seal in immutable storage (WORM) | Claim-check file | P7 rwb-decision | One seal per business date (Architecture v5 slide 14) |

Events this service publishes (AsyncAPI 3.0, CloudEvents 1.0):

| Event | EV | Topic | Consumers |
|---|---|---|---|
| DecisionRecorded | EV-08 | `rwb.decision.events.v1` | rwb-decision, rwb-reporting |
| ApprovalRequested | EV-09 | `rwb.decision.events.v1` | gateway-bff (inbox) |
| RulePackageInForce | EV-30 | `rwb.decision.events.v1` | rwb-case, rwb-valuation, rwb-treatment, rwb-payment |

#### T5.2.2 Contracts consumed

| Contract | Type | Provider | Class | Failure path |
|---|---|---|---|---|
| GET /doa-limits (delegation of authority) | REST | P4 rwb-access | C | 2 s timeout, breaker; built against the fake (ADR-020) |

Events this service consumes:

| Event | EV | Provider topic | Provider | Class | Failure path |
|---|---|---|---|---|---|
| DecisionRecorded (from all 19) | EV-08 | `all 19 service topics` | all | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| NoticeGenerated | EV-13 | `rwb.comms.events.v1` | P6 rwb-comms | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| AgentRunCompleted | EV-28 | `rwb.agent.events.v1` | P10 rwb-agent | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |

#### T5.2.3 Call-type summary

| Call type | Provided | Consumed | Artefact |
|---|---|---|---|
| REST | 15 | 1 | OpenAPI 3.1, one file per service |
| Kafka (events) | 3 | 3 | AsyncAPI 3.0, one file per service |
| Temporal | 3 | 0 | Workflow and activity interfaces, queue `rwb-decision` |
| File | 1 | 0 | Interface Specifications manifest and the SAS link |
| Nexus | 0 | 0 | Nexus operation into ACE |
| SQL | 0 | 0 | Read-only grant on the view |

A contract change is a new version of the artefact, never a code change in the consumer (ADR-020). The provider named in T5.2.2 is the owner in Microservice Ownership Map v1, and the consumer list of each event is the Arch v5 event catalogue on slides 42 and 43.

### T5.3 Events

The event contract of this service is `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-decision.asyncapi.yaml`; the shared decision-record contract is `asyncapi/rwb.decision-record.v1.asyncapi.yaml`. Every service publishes DecisionRecorded (EV-08) to `rwb.decision-record.v1` from its outbox in the same transaction as its state change (DP-03, DP-09; ADR-015, ADR-022); consuming services dedupe through their inbox table. Events carry identifiers and facts, never personal data (Event and Messaging Design v4, sheet Rules).

| Event | EV | Direction | Topic |
|---|---|---|---|
| DecisionRecorded | EV-08 | Published | `rwb.decision.events.v1` |
| ApprovalRequested | EV-09 | Published | `rwb.decision.events.v1` |
| RulePackageInForce | EV-30 | Published | `rwb.decision.events.v1` |
| DecisionRecorded (from all 19) | EV-08 | Consumed | `all 19 service topics` |
| NoticeGenerated | EV-13 | Consumed | `rwb.comms.events.v1` |
| AgentRunCompleted | EV-28 | Consumed | `rwb.agent.events.v1` |

An event shown with `—` has no number in the numbered catalogue: the Arch v5 catalogue calls these rows `+`, so the number is not specified in the source documents (GAP-1996; ASM-3223). Architecture v5 slide 14 also names ApprovalDecided on `rwb.decision.events.v1`; the AsyncAPI document of 22 November 2026 does not carry it (GAP-1996; ASM-3223).

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Decision log |
|---|---|
| RW-CASEOWN Case owner | R |
| RW-TEAMMGR Team manager | R |
| RW-RESTRUCT Restructuring officer (FCR) | R |
| RW-SPECIAL Hardship and vulnerability specialist | R |
| RW-COMPLAIN Complaint officer | R |
| RW-FRAUD Fraud investigator | R |
| RW-LITOFF Litigation officer | R |
| RW-ENFORCE Enforcement owner | R |
| RW-LEGAL Legal counsel | R |
| RW-SALEOFF Sale officer | R |
| RW-NPAMGR NPA and asset manager | R |
| RW-DEBTSALE Debt sale officer | R |
| RW-WRITEOFF Write-off team member | R |
| RW-CREDITAD Credit Administration officer | R |
| RW-GUARANT Guarantee officer | R |
| RW-AGENCYMG Partner and agency manager | R |
| RW-CONDUCT Conduct and QA officer | R |
| RW-PRODHEAD Product head (Mortgage, HP, SSME) | R |
| RW-HEADLIT Head of Litigation | R |
| RW-HEADNPA Head of NPA | R |
| RW-HEADASL Head of Asset Liquidity | R |
| RW-CREDCOMM Credit approval committee member | R |
| RW-WOCOMM Write-off committee member | R |
| RW-RISK Risk and model risk officer | R |
| RW-COE Center of excellence analyst | R |
| RW-DATASTEW Data steward and data product owner | R |
| RW-FINANCE Finance and CFO delegate | R |
| RW-AUDIT Internal audit | R |
| RW-COMPLY Compliance and PDPA officer | R |
| RW-PLATADM Platform administrator | R |
| RW-REFADM Reference data administrator | R |
| RW-SECADM Security administrator | R |
| RW-BIANAL Reporting and BI analyst | R |
| RW-TRIBE Tribe lead and squad members | R |
| SY-CASEWF Case workflow module | C |
| SY-RULES Rules component | C |
| SY-DATALOAD Data load from COLLINS | C |
| SY-OCR OCR and extraction pipeline | C |
| SY-DECLOG Decision log writer | C |
| SY-AGENT Agent platform | C |

### T6.2 Authentication and authorization

Entra ID single sign-on through the ACE front end; each endpoint declares its capability area and right; scope filters every query; masking applies to personal fields; service identities for jobs and agents.

Every operation of T5.2.1 is authorised through the `rwb-access` authorise contract with the role, the scope and the delegation limit of T6.1 (DP-08; C RWB-P4-E1037-CON); the caller caches the answer and refreshes it on AccessPolicyChanged and DoaLimitChanged.

## T7. Non-functional requirements

| ID | Requirement | Target | Status |
|---|---|---|---|
| NFR-033 | Every decision is reproducible from the log, including the rule, model, agent and prompt versions and the inputs used. | Every decision reproducible | Proposed |
| NFR-034 | Every action carries the rule version applied and the approver who allowed it. | Every action | Proposed |
| NFR-035 | The decision log hash chain is checked daily, and a break is reported to Compliance the same day. | Daily check, same-day report | Proposed |
| NFR-036 | An audit or regulatory request is answered inside its deadline with the decision history and the supporting documents. | Inside the deadline set by the requester | Proposed |
| NFR-037 | Quality assurance reaches first-time-right on case packs and write-off returns. | 90 percent | Proposed |
| NFR-038 | Every outbound contact carries a conduct check result, and a contact without one is held. | Every contact | Proposed |
| NFR-076 | A document produced from the hub carries its origin, the date it entered the hub, whether it has been altered since, and who has read it, to the standard a court applies. | Every document produced | Proposed |
| NFR-077 | A failed write to the interaction ledger raises an incident, and no entry is discarded. | No silent gaps | Proposed |
| NFR-078 | A model or agent write to a queue is logged with the model or agent version, on the same terms as a decision taken by a person. | Every write | Proposed |

## T8. Requirement traceability

| Requirement | Feature | Story | Test |
|---|---|---|---|
| REQ-DRI-001 | FEAT-DRI-01 | RWB-E1-008 | TC-E1-008-01 |
| REQ-DRI-002 | FEAT-DRI-01 | RWB-E1-008 | TC-E1-008-01 |
| REQ-DRI-003 | FEAT-DRI-01 | RWB-E1-008 | TC-E1-008-01 |
| REQ-DRI-004 | FEAT-DRI-01 | RWB-E1-008 | TC-E1-008-01 |
| REQ-DRI-005 | FEAT-DRI-01 | RWB-E1-008 | TC-E1-008-01 |
| REQ-DRI-009 | FEAT-DRI-01 | RWB-E1-008 | TC-E1-008-01 |
| REQ-DRI-010 | FEAT-DRI-01 | RWB-E1-008 | TC-E1-008-01 |
| REQ-DRI-011 | FEAT-DRI-01 | RWB-E1-008 | TC-E1-008-01 |
| REQ-DRI-012 | FEAT-APD-01 | RWB-E2-013 | TC-E2-013-01 |
| REQ-APD-001 | FEAT-APD-01 | RWB-E2-013 | TC-E2-013-01 |
| REQ-APD-002 | FEAT-APD-01 | RWB-E2-013 | TC-E2-013-01 |
| REQ-APD-003 | FEAT-APD-01 | RWB-E2-013 | TC-E2-013-01 |
| REQ-APD-004 | FEAT-APD-01 | RWB-E2-013 | TC-E2-013-01 |
| REQ-APD-005 | FEAT-APD-01 | RWB-E2-013 | TC-E2-013-01 |
| REQ-APD-006 | FEAT-APD-01 | RWB-E2-013 | TC-E2-013-01 |
| REQ-APD-007 | FEAT-APD-01 | RWB-E2-013 | TC-E2-013-01 |
| REQ-APD-008 | FEAT-APD-01 | RWB-E2-013 | TC-E2-013-01 |
| REQ-APD-009 | FEAT-APD-01 | RWB-E2-013 | TC-E2-013-01 |
| REQ-APD-010 | FEAT-APD-01 | RWB-E2-013 | TC-E2-013-01 |
| REQ-APD-011 | FEAT-APD-01 | RWB-E2-013 | TC-E2-013-01 |
| REQ-ILG-001 | FEAT-DRI-01 | RWB-E1-008 | TC-E1-008-01 |
| REQ-ILG-002 | FEAT-DRI-01 | RWB-E1-008 | TC-E1-008-01 |
| REQ-ILG-003 | FEAT-DRI-01 | RWB-E1-008 | TC-E1-008-01 |
| REQ-ILG-004 | FEAT-DRI-01 | RWB-E1-008 | TC-E1-008-01 |
| REQ-ILG-005 | FEAT-DRI-01 | RWB-E1-008 | TC-E1-008-01 |
| REQ-ILG-006 | FEAT-DRI-01 | RWB-E1-008 | TC-E1-008-01 |
| REQ-ILG-007 | FEAT-DRI-01 | RWB-E1-008 | TC-E1-008-01 |
| REQ-ILG-008 | FEAT-DRI-01 | RWB-E1-008 | TC-E1-008-01 |
| REQ-ILG-009 | FEAT-APD-01 | RWB-E2-013 | TC-E2-013-01 |
| REQ-ILG-010 | FEAT-APD-01 | RWB-E2-013 | TC-E2-013-01 |
| REQ-ILG-011 | FEAT-APD-01 | RWB-E2-013 | TC-E2-013-01 |
| REQ-ILG-012 | FEAT-APD-01 | RWB-E2-013 | TC-E2-013-01 |
| REQ-ILG-013 | FEAT-APD-01 | RWB-E2-013 | TC-E2-013-01 |
| REQ-ILG-014 | FEAT-DRI-01 | RWB-E1-008 | TC-E1-008-01 |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-P7-001 | GET | /api/recovery/decision/v1/cases/{caseId}/recommendation | Decision log R | E4 |
| API-P7-002 | GET | /api/recovery/decision/v1/approvals | Decision log A | E2 |
| API-P7-003 | POST | /api/recovery/decision/v1/approvals/{approvalId}/approve | Decision log A | E2 |
| API-P7-004 | POST | /api/recovery/decision/v1/approvals/{approvalId}/return | Decision log A | E2 |
| API-P7-005 | POST | /api/recovery/decision/v1/approvals/{approvalId}/refuse | Decision log A | E2 |
| API-P7-006 | GET | /api/recovery/decision/v1/decision-log | Decision log R | E1 |
| API-P7-007 | GET | /api/recovery/decision/v1/decision-log/{entryId} | Decision log R | E1 |
| API-P7-008 | GET | /api/recovery/decision/v1/approvals/{approvalId} | Decision log A | E2 |

The operation IDs, paths and operationIds of these endpoints are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-decision.yaml`; where an appendix row and the published operation differ, the published operation is the contract of T5.2.1 and the row keeps its ID for traceability (GAP-1997; ASM-3224).

### T-A.2 Endpoint detail

#### API-P7-001 GET /cases/{caseId}/recommendation

| Item | Value |
|---|---|
| Purpose | Read the current recommendation with reasons and the expected return by route |
| Request | Query: decision |
| Response | Recommendation |
| Errors | 401, 403, 404, 503 |
| Authorization | Decision log, right R, scope applied |
| Idempotency | Not applicable |

#### API-P7-002 GET /approvals

| Item | Value |
|---|---|
| Purpose | List decisions waiting for the caller's approval level |
| Request | Query: decision, product, page, size |
| Response | ApprovalPage |
| Errors | 401, 403, 503 |
| Authorization | Decision log, right A, scope applied |
| Idempotency | Not applicable |

#### API-P7-003 POST /approvals/{approvalId}/approve

| Item | Value |
|---|---|
| Purpose | Approve a decision within the caller's limit |
| Request | ApprovalAction |
| Response | DecisionLogEntry |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Decision log, right A, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P7-004 POST /approvals/{approvalId}/return

| Item | Value |
|---|---|
| Purpose | Return a decision to the preparer with a reason |
| Request | ApprovalAction |
| Response | Approval |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Decision log, right A, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P7-005 POST /approvals/{approvalId}/refuse

| Item | Value |
|---|---|
| Purpose | Refuse a decision with a reason |
| Request | ApprovalAction |
| Response | DecisionLogEntry |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Decision log, right A, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P7-006 GET /decision-log

| Item | Value |
|---|---|
| Purpose | Search the decision log by case, rule, approver and date |
| Request | Query: caseId, decision, ruleId, approver, from, to, page, size |
| Response | DecisionLogPage |
| Errors | 401, 403, 503 |
| Authorization | Decision log, right R, scope applied |
| Idempotency | Not applicable |

#### API-P7-007 GET /decision-log/{entryId}

| Item | Value |
|---|---|
| Purpose | Read one decision log entry with its inputs and versions |
| Request | None |
| Response | DecisionLogEntry |
| Errors | 401, 403, 404, 503 |
| Authorization | Decision log, right R, scope applied |
| Idempotency | Not applicable |

#### API-P7-008 GET /approvals/{approvalId}

| Item | Value |
|---|---|
| Purpose | Read one approval with its routing details for the decision screen |
| Request | None |
| Response | ApprovalDetail |
| Errors | 401, 403, 404, 503 |
| Authorization | Decision log, right A, scope applied |
| Idempotency | Not applicable |

## Appendix T-B. Open technical decisions

| Decision | What is needed |
|---|---|
| DL06 | Which interfaces need same-day data |
| DL11 | Non-functional target values |
| DL35 | Deployment slots |

## Document sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| Solution architect | | | |
| Tech lead | | | |
| ACE team | | | |
| QA lead | | | |

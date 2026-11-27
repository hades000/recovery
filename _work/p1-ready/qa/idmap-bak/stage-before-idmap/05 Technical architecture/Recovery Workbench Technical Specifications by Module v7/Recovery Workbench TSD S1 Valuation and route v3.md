SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench S1 Valuation and route

Technical specification. SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD S1 Valuation and route |
| Document ID | S1-RWB-TSD-v3 |
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
| Recovery Workbench FSD S1 Valuation and route | FSD | Pair |
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

S1 Valuation and route is one of the 19 services of Architecture v5: `rwb-valuation` (service name Valuation and route, module S1, wave 3, service epic `RWB-SVC-S1`). Version 3 adds this section so that the specification is read as the specification of one service: its identity, what it owns, and the decoupling patterns that replace the monolith's in-process calls. Every owner is taken from Microservice Ownership Map v1 and every identifier from Template and Rules R4 (ADR-013, ADR-014).

S1 owns the D6 route decision and the route agent output; it reaches the case only through the RouteDecisionWorkflow child of P3 (DP-12).

### T0.1 Service identity

| Item | Value |
|---|---|
| Module | S1 Valuation and route |
| Service | `rwb-valuation` (Valuation and route) |
| Service epic | `RWB-SVC-S1` |
| Wave | 3 |
| Schema | `rwb_valuation` |
| Database login | `rwb_valuation`: one login per service, with its own connection pool cap |
| REST base | `/api/recovery/valuation/v1` |
| Kafka topic | `rwb.valuation.events.v1`, with `.retry` and `.dlt` topics |
| Event names | `rwb.valuation.<Event>.v1`, CloudEvents 1.0 in binary mode, key `caseId` |
| Temporal | namespace `rwb-recovery`; task queue `rwb-valuation` |
| Java package | `th.co.scb.ace.workbench.recovery.valuation` |
| Edge | gateway-bff for the staff screens of this service |
| Contract artefacts | `05 Technical architecture/Recovery Workbench API Specification v5/rwb-valuation.yaml`; `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-valuation.asyncapi.yaml` |
| Suggested owner, app development | TechX (suggested; any team may pick up this story) |
| Suggested owner, ACE DB | ACE team (suggested; any team may pick up this story) |

### T0.2 What this service owns

Architecture v5 slide 41 gives this service: valuations, D6 route decision, route agent output. Table T0.2 states the same ownership in the form the Ownership Map uses, with the counts this specification carries. A table that the map assigns to another service is not built here, whatever T3 says (see the note under T3).

| Area | Owner and artefact | Count |
|---|---|---|
| Business tables in `rwb_valuation` | none recorded for this service in the Ownership Map Tables sheet | 0 |
| REST operations | appendix T-A and `rwb-valuation.yaml` | 2 |
| Events published | RouteDecided | 1 |
| Workflows and schedules | RouteDecisionWorkflow | 1 |
| Jobs | none | 0 |

### T0.3 Decoupling patterns applied

The left column is the pattern of Template and Rules R5.5; the middle column quotes the line of this specification that carries the legacy marker, where one is present; the right column is what replaces it in this service.

| DP | Legacy marker in this specification | How the service lands it |
|---|---|---|
| DP-01 | — | Owns its tables in `rwb_valuation`; no other service reads them (ADR-014). |
| DP-02 | — | One login, `rwb_valuation`, with its own connection pool cap. |
| DP-03 | `…on events from P3 and writes through the decision log.` | Local decision record plus DecisionRecorded (EV-08) on `rwb.decision-record.v1`. |
| DP-07 | `DF-COL-022 / appraisal_type / LOV / varchar(15) / Yes / LOV-APPRAISAL / SVAF` | Reference data and lists of values from the `rwb-case` contract (H RWB-PLT-E1043-CON). |
| DP-08 | `RW-CASEOWN Case owner / CRU` | Authorisation through the `rwb-access` authorise contract and the guard library (H RWB-PLT-E1037-CON). |
| DP-09 | `…state machine of its own; the module acts on events from P3 and writes through the decision…` | Outbox and inbox library; CloudEvents on `rwb.valuation.events.v1` with retry topics and `.dlt`. |
| DP-10 | `Scheduler and batch / REUSE / ACE pattern: Quartz and Spring Batch / Jobs in the Batch and…` | Temporal Schedules and event-started workflows through the workflow kit (ADR-016). |
| DP-11 | `…reaches other modules only through their published interfaces and other systems only through COLLINS,…` | One REST hop, 2 s timeout, breaker; the consumer builds against the provider's fake (ADR-020). |
| DP-13 | `API-S1-001 / POST / /api/recovery/v1/cases/{caseId}/route / Treatment and offer…` | REST base `/api/recovery/valuation/v1`. |
| DP-14 | — | Topic `rwb.valuation.events.v1`, retry topics and `.dlt`; naming library (H RWB-PLT-E1047-CON). |
| DP-15 | — | Per-service Flyway sequence in `rwb_valuation`. |
| DP-20 | `…decision with COLLINS return by route and the route agent. It reaches other modules only through their…` | Agent work through the `rwb-agent` contract (C RWB-P10-TE013-CON). |

### T0.4 What this service is not

- It holds no other service's table and no ACE table beyond the read-only `recovery.v_ace_*` views (DP-01, DP-05).
- It runs no shared Quartz job and touches no ACE batch table (DP-10; ADR-016).
- It writes no case row: the route decision is returned to P3 through the child workflow (DP-12).
- It is not a monolith module: the published Java interface of T2 is replaced by the contract set of T5.2 (DP-11; ADR-020).

## T1. Architecture overview

S1 Valuation and route is delivered as the service `rwb-valuation` (module S1, wave 3, service epic `RWB-SVC-S1`): one repository, one pipeline, one schema `rwb_valuation` with one login, behind gateway-bff (ADR-013, ADR-014). It covers: d6 route decision with COLLINS return by route and the route agent. It reaches other modules only through the contracts of T5.2 and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| ValuationAndRouteController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| ValuationAndRouteService | Business logic; calls the rules component; writes the decision log entry before any change |
| ValuationAndRouteRepository | Reads and writes the module's tables only |
| Jobs | Temporal Schedules and event-started workflows this service owns (T0.2, T5.2.1; DP-10) |
| Published interface | The contracts of T5.2: REST operations, events and workflows other services call; no table is read across modules (DP-11) |

The published interface of this table is the contract set of T5.2: the REST operations, the events and the workflows, not a Java interface in a shared classpath (DP-11; ADR-020). Components that the Ownership Map places in another service are stated in T0.2 and T5.2 and are built by that service.

## T3. Data model

Every object of T3 that Microservice Ownership Map v1 assigns to `rwb-valuation` lives in schema `rwb_valuation` with the standard columns of T3.0 (DP-01, DP-15; ADR-014). T3.1 defines `valuation` as a NEW table of this service and `score` as a REUSE ACE object. The Ownership Map Tables sheet lists no table owned by S1: `valuation_ext` is P1's, and the `rwb_valuation` schema of Architecture v5 slide 41 holds the route decision. The map's Endpoints ruling puts the valuation paths with S1, so T5.2.1 lists them here and the table question is recorded (GAP-1995; ASM-3222).

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

**valuation** (NEW). An appraisal of collateral or an asset.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-COL-018 | id | TEXT | uuid | Yes | None | Workbench |
| DF-COL-019 | collateral_id | CROSS_REF | uuid | No | None | Workbench |
| DF-COL-020 | asset_id | CROSS_REF | uuid | No | None | Workbench |
| DF-COL-021 | appraisal_no | TEXT | varchar(20) | Yes | None | SVAF |
| DF-COL-022 | appraisal_type | LOV | varchar(15) | Yes | LOV-APPRAISAL | SVAF |
| DF-COL-023 | appraised_value | NUMBER | numeric(18,2) | Yes | None | SVAF |
| DF-COL-024 | forced_sale_value | NUMBER | numeric(18,2) | No | None | SVAF |
| DF-COL-025 | appraisal_date | DATE | date | Yes | None | SVAF |
| DF-COL-026 | valuer_partner_id | CROSS_REF | uuid | No | None | Workbench |
| DF-COL-027 | accepted | BOOLEAN | boolean | Yes | None | Workbench |
| DF-COL-043 | stale_flag | BOOLEAN | boolean | Yes | None | Workbench |
| DF-COL-044 | age_days | FORMULA | integer | No | None | Workbench |

**score** (REUSE ACE). A score or estimate COLLINS returns for an account or case.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-DEC-019 | id | TEXT | uuid | Yes | None | Workbench |
| DF-DEC-020 | account_id | CROSS_REF | uuid | No | None | Workbench |
| DF-DEC-021 | case_id | CROSS_REF | uuid | No | None | Workbench |
| DF-DEC-022 | model_code | TEXT | varchar(30) | Yes | None | COLLINS |
| DF-DEC-023 | model_version | TEXT | varchar(20) | Yes | None | COLLINS |
| DF-DEC-024 | score_value | NUMBER | numeric(12,4) | No | None | COLLINS |
| DF-DEC-025 | estimate_value | NUMBER | numeric(18,2) | No | None | COLLINS |
| DF-DEC-026 | route_code | LOV | varchar(4) | No | LOV-ROUTE | COLLINS |
| DF-DEC-027 | scored_at | DATE | date | Yes | None | COLLINS |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-APPRAISAL | MARKET, OFFICIAL, FORCED_SALE, DESKTOP, AGENT_ESTIMATE |
| LOV-ROUTE | R1, R2, R3, R4, R5, R6, R7, R8 |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| valuation | collateral_id | collateral | Many to 0 or 1 |
| valuation | asset_id | asset | Many to 0 or 1 |
| valuation | valuer_partner_id | partner | Many to 0 or 1 |
| score | account_id | loan_account | Many to 0 or 1 |
| score | case_id | recovery_case | Many to 0 or 1 |

## T4. State machines and workflow

No case state machine of its own; the module acts on events from P3 and writes through the decision log.

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| None | | | | |

### T5.2 Contracts

Version 3 states every cross-module dependency of this module as a contract, so that the service is built against a published artefact and its fake (ADR-020; DP-11). The artefact per call type is: OpenAPI 3.1 for REST, AsyncAPI 3.0 for Kafka, the Temporal interface named here for a workflow or activity, the Interface Specifications manifest for a file, the Nexus operation for the ACE restructure calculator, and a grant on the view for SQL. No row of this section reads another service's table (DP-01). Every consumed contract is class C (Template and Rules R5.4): it never blocks the build, because the consumer builds against the fake, and the real cross-service behaviour is class I work on an integration story. Architecture v5 slides 13 to 20 name a few operations differently from the published files of 22 November 2026; the published file is the artefact the fake is generated from and is the one cited here (GAP-1997; ASM-3224).

#### T5.2.1 Contracts provided

The REST operations of this service are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-valuation.yaml` (5.0.0, 22 November 2026) under the base `/api/recovery/valuation/v1`. Appendix T-A holds the endpoint IDs, the access right and the first release of each one.

| # | Method | Path | operationId |
|---|---|---|---|
| 1 | POST | `/cases/{caseId}/route` | `postCasesCaseidRoute` |
| 2 | POST | `/assets/{assetKey}/valuations` | `postAssetsAssetkeyValuations` |
The valuation path was moved here from S5 in the API split (Ownership Map ruling `POST /assets/{assetKey}/valuations`, ASM-0043).

Workflows, schedules, files and views this service provides:

| Contract | Type | Called by or target | Note |
|---|---|---|---|
| RouteDecisionWorkflow (child of the case) | Temporal workflow | P3 rwb-case | Child of CaseWorkflow; runs on rwb-valuation |

Events this service publishes (AsyncAPI 3.0, CloudEvents 1.0):

| Event | EV | Topic | Consumers |
|---|---|---|---|
| RouteDecided | — | `rwb.valuation.events.v1` | rwb-case |

#### T5.2.2 Contracts consumed

| Contract | Type | Provider | Class | Failure path |
|---|---|---|---|---|
| Collateral and appraisals (read-only) | REST | P1 rwb-source-data | C | 2 s timeout, breaker; built against the fake (ADR-020) |
| Agent run: route agent | Temporal child workflow | P10 rwb-agent | C | Workflow retry policy; the caller keeps its state (DP-12) |
| Approval | Temporal child workflow | P7 rwb-decision | C | Workflow retry policy; the caller keeps its state (DP-12) |

Events this service consumes:

| Event | EV | Provider topic | Provider | Class | Failure path |
|---|---|---|---|---|---|
| RulePackageInForce | EV-30 | `rwb.decision.events.v1` | P7 rwb-decision | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |

#### T5.2.3 Call-type summary

| Call type | Provided | Consumed | Artefact |
|---|---|---|---|
| REST | 2 | 1 | OpenAPI 3.1, one file per service |
| Kafka (events) | 1 | 1 | AsyncAPI 3.0, one file per service |
| Temporal | 1 | 2 | Workflow and activity interfaces, queue `rwb-valuation` |
| File | 0 | 0 | Interface Specifications manifest and the SAS link |
| Nexus | 0 | 0 | Nexus operation into ACE |
| SQL | 0 | 0 | Read-only grant on the view |

A contract change is a new version of the artefact, never a code change in the consumer (ADR-020). The provider named in T5.2.2 is the owner in Microservice Ownership Map v1, and the consumer list of each event is the Arch v5 event catalogue on slides 42 and 43.

### T5.3 Events

The event contract of this service is `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-valuation.asyncapi.yaml`; the shared decision-record contract is `asyncapi/rwb.decision-record.v1.asyncapi.yaml`. Every service publishes DecisionRecorded (EV-08) to `rwb.decision-record.v1` from its outbox in the same transaction as its state change (DP-03, DP-09; ADR-015, ADR-022); consuming services dedupe through their inbox table. Events carry identifiers and facts, never personal data (Event and Messaging Design v4, sheet Rules).

| Event | EV | Direction | Topic |
|---|---|---|---|
| RouteDecided | — | Published | `rwb.valuation.events.v1` |
| RulePackageInForce | EV-30 | Consumed | `rwb.decision.events.v1` |

An event shown with `—` has no number in the numbered catalogue: the Arch v5 catalogue calls these rows `+`, so the number is not specified in the source documents (GAP-1996; ASM-3223).

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Treatment and offer |
|---|---|
| RW-CASEOWN Case owner | CRU |
| RW-TEAMMGR Team manager | R |
| RW-RESTRUCT Restructuring officer (FCR) | CRUA |
| RW-SPECIAL Hardship and vulnerability specialist | CRU |
| RW-COMPLAIN Complaint officer | R |
| RW-FRAUD Fraud investigator | R |
| RW-LITOFF Litigation officer | R |
| RW-LEGAL Legal counsel | R |
| RW-GUARANT Guarantee officer | CRU |
| RW-CONDUCT Conduct and QA officer | R |
| RW-PRODHEAD Product head (Mortgage, HP, SSME) | RA |
| RW-CREDCOMM Credit approval committee member | RA |
| RW-RISK Risk and model risk officer | R |
| RW-COE Center of excellence analyst | R |
| RW-AUDIT Internal audit | R |
| RW-BIANAL Reporting and BI analyst | R |
| RW-TRIBE Tribe lead and squad members | R |
| SY-CASEWF Case workflow module | R |
| SY-RULES Rules component | R |
| SY-AGENT Agent platform | R |

### T6.2 Authentication and authorization

Entra ID single sign-on through the ACE front end; each endpoint declares its capability area and right; scope filters every query; masking applies to personal fields; service identities for jobs and agents.

Every operation of T5.2.1 is authorised through the `rwb-access` authorise contract with the role, the scope and the delegation limit of T6.1 (DP-08; C RWB-P4-E1037-CON); the caller caches the answer and refreshes it on AccessPolicyChanged and DoaLimitChanged.

## T7. Non-functional requirements

| ID | Requirement | Target | Status |
|---|---|---|---|
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
| REQ-S1-001 | FEAT-VAL-01 | Written one epic ahead | With the story |
| REQ-S1-002 | FEAT-VAL-01 | Written one epic ahead | With the story |
| REQ-S1-003 | FEAT-VAL-01 | Written one epic ahead | With the story |
| REQ-S1-004 | FEAT-VAL-01 | Written one epic ahead | With the story |
| REQ-S1-005 | FEAT-VAL-01 | Written one epic ahead | With the story |
| REQ-S1-006 | FEAT-VAL-01 | Written one epic ahead | With the story |
| REQ-S1-007 | FEAT-VAL-01 | Written one epic ahead | With the story |
| REQ-S1-008 | FEAT-VAL-01 | Written one epic ahead | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-S1-001 | POST | /api/recovery/valuation/v1/cases/{caseId}/route | Treatment and offer U | E4 |

The operation IDs, paths and operationIds of these endpoints are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-valuation.yaml`; where an appendix row and the published operation differ, the published operation is the contract of T5.2.1 and the row keeps its ID for traceability (GAP-1997; ASM-3224).

### T-A.2 Endpoint detail

#### API-S1-001 POST /cases/{caseId}/route

| Item | Value |
|---|---|
| Purpose | Submit the route decision for approval, with an override reason where it departs from the recommendation |
| Request | RouteRequest |
| Response | Approval |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Treatment and offer, right U, scope applied |
| Idempotency | Idempotency-Key header |

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

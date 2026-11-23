SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench S3 Guarantees and guarantors

Technical specification. SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD S3 Guarantees and guarantors |
| Document ID | S3-RWB-TSD-v3 |
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
| Recovery Workbench FSD S3 Guarantees and guarantors | FSD | Pair |
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

S3 Guarantees and guarantors is one of the 19 services of Architecture v5: `rwb-guarantee` (service name Guarantee, module S3, wave 3, service epic `RWB-SVC-S3`). Version 3 adds this section so that the specification is read as the specification of one service: its identity, what it owns, and the decoupling patterns that replace the monolith's in-process calls. Every owner is taken from Microservice Ownership Map v1 and every identifier from Template and Rules R4 (ADR-013, ADR-014).

S3 pursues the guarantor through P6 notices and P7 approvals; it holds the claim, not the notice (DP-01, DP-11).

### T0.1 Service identity

| Item | Value |
|---|---|
| Module | S3 Guarantees and guarantors |
| Service | `rwb-guarantee` (Guarantee) |
| Service epic | `RWB-SVC-S3` |
| Wave | 3 |
| Schema | `rwb_guarantee` |
| Database login | `rwb_guarantee`: one login per service, with its own connection pool cap |
| REST base | `/api/recovery/guarantee/v1` |
| Kafka topic | `rwb.guarantee.events.v1`, with `.retry` and `.dlt` topics |
| Event names | `rwb.guarantee.<Event>.v1`, CloudEvents 1.0 in binary mode, key `caseId` |
| Temporal | namespace `rwb-recovery`; task queue `rwb-guarantee` |
| Java package | `th.co.scb.ace.workbench.recovery.guarantee` |
| Edge | gateway-bff for the staff screens of this service |
| Contract artefacts | `05 Technical architecture/Recovery Workbench API Specification v5/rwb-guarantee.yaml`; `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-guarantee.asyncapi.yaml` |
| Suggested owner, app development | TechX (suggested; any team may pick up this story) |
| Suggested owner, ACE DB | ACE team (suggested; any team may pick up this story) |

### T0.2 What this service owns

Architecture v5 slide 41 gives this service: TCG and insurance claims, guarantor notices and pursuit. Table T0.2 states the same ownership in the form the Ownership Map uses, with the counts this specification carries. A table that the map assigns to another service is not built here, whatever T3 says (see the note under T3).

| Area | Owner and artefact | Count |
|---|---|---|
| Business tables in `rwb_guarantee` | `guarantee_claim` | 1 |
| REST operations | appendix T-A and `rwb-guarantee.yaml` | 2 |
| Events published | GuaranteeClaim | 1 |
| Workflows and schedules | GuaranteeClaimWorkflow | 1 |
| Jobs | none | 0 |

### T0.3 Decoupling patterns applied

The left column is the pattern of Template and Rules R5.5; the middle column quotes the line of this specification that carries the legacy marker, where one is present; the right column is what replaces it in this service.

| DP | Legacy marker in this specification | How the service lands it |
|---|---|---|
| DP-01 | — | Owns its tables in `rwb_guarantee`; no other service reads them (ADR-014). |
| DP-02 | — | One login, `rwb_guarantee`, with its own connection pool cap. |
| DP-03 | `…logic; calls the rules component; writes the decision log entry before any change` | Local decision record plus DecisionRecorded (EV-08) on `rwb.decision-record.v1`. |
| DP-07 | `DF-TRT-017 / claim_type / LOV / varchar(25) / Yes / LOV-CLAIM-TYPE / Workbench` | Reference data and lists of values from the `rwb-case` contract (H RWB-PLT-E1043-CON). |
| DP-08 | `RW-CASEOWN Case owner / CRU` | Authorisation through the `rwb-access` authorise contract and the guard library (H RWB-PLT-E1037-CON). |
| DP-09 | — | Outbox and inbox library; CloudEvents on `rwb.guarantee.events.v1` with retry topics and `.dlt`. |
| DP-10 | `Scheduler and batch / REUSE / ACE pattern: Quartz and Spring Batch / Jobs in the Batch and…` | Temporal Schedules and event-started workflows through the workflow kit (ADR-016). |
| DP-11 | `…reaches other modules only through their published interfaces and other systems only through COLLINS,…` | One REST hop, 2 s timeout, breaker; the consumer builds against the provider's fake (ADR-020). |
| DP-13 | `API-S3-001 / POST / /api/recovery/v1/cases/{caseId}/guarantee-claims / Treatment…` | REST base `/api/recovery/guarantee/v1`. |
| DP-14 | — | Topic `rwb.guarantee.events.v1`, retry topics and `.dlt`; naming library (H RWB-PLT-E1047-CON). |
| DP-15 | — | Per-service Flyway sequence in `rwb_guarantee`. |

### T0.4 What this service is not

- It holds no other service's table and no ACE table beyond the read-only `recovery.v_ace_*` views (DP-01, DP-05).
- It runs no shared Quartz job and touches no ACE batch table (DP-10; ADR-016).
- It sends no notice itself: the guarantor notice is a P6 child workflow (DP-11).
- It is not a monolith module: the published Java interface of T2 is replaced by the contract set of T5.2 (DP-11; ADR-020).

## T1. Architecture overview

S3 Guarantees and guarantors is delivered as the service `rwb-guarantee` (module S3, wave 3, service epic `RWB-SVC-S3`): one repository, one pipeline, one schema `rwb_guarantee` with one login, behind gateway-bff (ADR-013, ADR-014). It covers: tCG and insurance claims, guarantor notices and pursuit. It reaches other modules only through the contracts of T5.2 and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| GuaranteesAndGuarantorsController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| GuaranteesAndGuarantorsService | Business logic; calls the rules component; writes the decision log entry before any change |
| GuaranteesAndGuarantorsRepository | Reads and writes the module's tables only |
| Jobs | Temporal Schedules and event-started workflows this service owns (T0.2, T5.2.1; DP-10) |
| Published interface | The contracts of T5.2: REST operations, events and workflows other services call; no table is read across modules (DP-11) |

The published interface of this table is the contract set of T5.2: the REST operations, the events and the workflows, not a Java interface in a shared classpath (DP-11; ADR-020). Components that the Ownership Map places in another service are stated in T0.2 and T5.2 and are built by that service.

## T3. Data model

Every object of T3 that Microservice Ownership Map v1 assigns to `rwb-guarantee` lives in schema `rwb_guarantee` with the standard columns of T3.0 (DP-01, DP-15; ADR-014). `guarantee_claim` is this service's table; the dated DP04 copies of the claim stay with P1 and are read-only here (Ownership Map ruling `dp_guarantee_claim`, ASM-0080).

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

**guarantee_claim** (NEW). A claim against a Thai Credit Guarantee Corporation guarantee or an insurer.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-TRT-015 | id | TEXT | uuid | Yes | None | Workbench |
| DF-TRT-016 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-TRT-017 | claim_type | LOV | varchar(25) | Yes | LOV-CLAIM-TYPE | Workbench |
| DF-TRT-018 | claim_deadline | DATE | date | Yes | None | Workbench |
| DF-TRT-019 | claimed_amount | NUMBER | numeric(18,2) | Yes | None | Workbench |
| DF-TRT-020 | filed_at | DATE | date | No | None | Workbench |
| DF-TRT-021 | paid_amount | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-TRT-022 | status | LOV | varchar(12) | Yes | LOV-CLAIM-STATUS | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-CLAIM-STATUS | PREPARING, FILED, DEFECT, PAID, REJECTED |
| LOV-CLAIM-TYPE | TCG, CREDIT_LIFE_INSURANCE, MORTGAGE_INSURANCE, COLLATERAL_INSURANCE |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| guarantee_claim | case_id | recovery_case | Many to 1 |

## T4. State machines and workflow

**GUARANTEE.** 32 rules over 17 states. The full table is in the Business Rules and Routing Logic workbook.

| Rule | From | Event | To |
|---|---|---|---|
| R-GUA-01 | GUARANTEE_DETECTED | GUARANTEE_FOUND | DEADLINE_TIMER_RUNNING |
| R-GUA-02 | GUARANTEE_DETECTED | CONDITIONS_NOT_MET | NOT_ELIGIBLE |
| R-GUA-03 | NOT_ELIGIBLE | CONDITIONS_LATER_MET | DEADLINE_TIMER_RUNNING |
| R-GUA-04 | DEADLINE_TIMER_RUNNING | PREPARATION_DUE | CLAIM_PREPARATION |
| R-GUA-05 | DEADLINE_TIMER_RUNNING | CLAIM_DEADLINE_MISSED | DEADLINE_MISSED |
| R-GUA-06 | DEADLINE_TIMER_RUNNING | GUARANTOR_NOTICE_DUE | GUARANTOR_NOTICE |
| R-GUA-07 | CLAIM_PREPARATION | CHECKLIST_COMPLETE | CLAIM_APPROVAL |
| R-GUA-08 | CLAIM_PREPARATION | CHECKLIST_INCOMPLETE | CLAIM_DEFECT_HOLD |
| R-GUA-09 | CLAIM_PREPARATION | CLAIM_DEADLINE_MISSED | DEADLINE_MISSED |
| R-GUA-10 | CLAIM_DEFECT_HOLD | DOCUMENT_SUPPLIED | CLAIM_PREPARATION |
| R-GUA-11 | CLAIM_DEFECT_HOLD | DEADLINE_WARNING | CLAIM_APPROVAL |
| R-GUA-12 | CLAIM_APPROVAL | CLAIM_APPROVED | CLAIM_SUBMITTED |
| R-GUA-13 | CLAIM_APPROVAL | CLAIM_SENT_BACK | CLAIM_PREPARATION |
| R-GUA-14 | CLAIM_SUBMITTED | TCG_QUERY_RAISED | TCG_QUERY |
| R-GUA-15 | TCG_QUERY | QUERY_ANSWERED | CLAIM_SUBMITTED |
| R-GUA-16 | TCG_QUERY | QUERY_UNANSWERED | CLAIM_REJECTED |
| R-GUA-17 | CLAIM_SUBMITTED | CLAIM_REJECTED_BY_TCG | CLAIM_REJECTED |
| R-GUA-18 | CLAIM_REJECTED | RESUBMISSION_POSSIBLE | CLAIM_PREPARATION |
| R-GUA-19 | CLAIM_REJECTED | RESUBMISSION_NOT_POSSIBLE | RESIDUAL_TO_ROUTE |
| R-GUA-20 | CLAIM_SUBMITTED | PART_PAYMENT_RECEIVED | CLAIM_PART_PAID |
| R-GUA-21 | CLAIM_PART_PAID | BALANCE_CLAIMED | CLAIM_SUBMITTED |
| R-GUA-22 | CLAIM_SUBMITTED | FULL_PAYMENT_RECEIVED | CLAIM_PAID |
| R-GUA-23 | CLAIM_PAID | SUBROGATION_DUE | SUBROGATION_POSITION |
| R-GUA-24 | CLAIM_PART_PAID | SUBROGATION_DUE | SUBROGATION_POSITION |
| R-GUA-25 | SUBROGATION_POSITION | RESIDUAL_REMAINS | RESIDUAL_TO_ROUTE |
| and 7 more | | | |

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-29 | Thai Credit Guarantee Corporation | Both | Not available today; entered and filed by the guarantee officer | As needed |

### T5.2 Contracts

Version 3 states every cross-module dependency of this module as a contract, so that the service is built against a published artefact and its fake (ADR-020; DP-11). The artefact per call type is: OpenAPI 3.1 for REST, AsyncAPI 3.0 for Kafka, the Temporal interface named here for a workflow or activity, the Interface Specifications manifest for a file, the Nexus operation for the ACE restructure calculator, and a grant on the view for SQL. No row of this section reads another service's table (DP-01). Every consumed contract is class C (Template and Rules R5.4): it never blocks the build, because the consumer builds against the fake, and the real cross-service behaviour is class I work on an integration story. Architecture v5 slides 13 to 20 name a few operations differently from the published files of 22 November 2026; the published file is the artefact the fake is generated from and is the one cited here (GAP-1997; ASM-3224).

#### T5.2.1 Contracts provided

The REST operations of this service are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-guarantee.yaml` (5.0.0, 22 November 2026) under the base `/api/recovery/guarantee/v1`. Appendix T-A holds the endpoint IDs, the access right and the first release of each one.

| # | Method | Path | operationId |
|---|---|---|---|
| 1 | POST | `/cases/{caseId}/guarantee-claims` | `postCasesCaseidGuaranteeClaims` |
| 2 | PATCH | `/guarantee-claims/{claimId}` | `patchGuaranteeClaimsClaimid` |

Workflows, schedules, files and views this service provides:

| Contract | Type | Called by or target | Note |
|---|---|---|---|
| GuaranteeClaimWorkflow | Temporal workflow | P3 rwb-case | Stage workflow of the case; runs on rwb-guarantee |

Events this service publishes (AsyncAPI 3.0, CloudEvents 1.0):

| Event | EV | Topic | Consumers |
|---|---|---|---|
| GuaranteeClaim | — | `rwb.guarantee.events.v1` | rwb-case, rwb-reporting |

#### T5.2.2 Contracts consumed

| Contract | Type | Provider | Class | Failure path |
|---|---|---|---|---|
| Guarantor notice | Temporal child workflow | P6 rwb-comms | C | Workflow retry policy; the caller keeps its state (DP-12) |
| Approval | Temporal child workflow | P7 rwb-decision | C | Workflow retry policy; the caller keeps its state (DP-12) |

Events this service consumes:

| Event | EV | Provider topic | Provider | Class | Failure path |
|---|---|---|---|---|---|
| NoticeDelivered | EV-15 | `rwb.comms.events.v1` | P6 rwb-comms | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| ProceedsMatched | EV-25 | `rwb.payment.events.v1` | P8 rwb-payment | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |

#### T5.2.3 Call-type summary

| Call type | Provided | Consumed | Artefact |
|---|---|---|---|
| REST | 2 | 0 | OpenAPI 3.1, one file per service |
| Kafka (events) | 1 | 2 | AsyncAPI 3.0, one file per service |
| Temporal | 1 | 2 | Workflow and activity interfaces, queue `rwb-guarantee` |
| File | 0 | 0 | Interface Specifications manifest and the SAS link |
| Nexus | 0 | 0 | Nexus operation into ACE |
| SQL | 0 | 0 | Read-only grant on the view |

A contract change is a new version of the artefact, never a code change in the consumer (ADR-020). The provider named in T5.2.2 is the owner in Microservice Ownership Map v1, and the consumer list of each event is the Arch v5 event catalogue on slides 42 and 43.

### T5.3 Events

The event contract of this service is `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-guarantee.asyncapi.yaml`; the shared decision-record contract is `asyncapi/rwb.decision-record.v1.asyncapi.yaml`. Every service publishes DecisionRecorded (EV-08) to `rwb.decision-record.v1` from its outbox in the same transaction as its state change (DP-03, DP-09; ADR-015, ADR-022); consuming services dedupe through their inbox table. Events carry identifiers and facts, never personal data (Event and Messaging Design v4, sheet Rules).

| Event | EV | Direction | Topic |
|---|---|---|---|
| GuaranteeClaim | — | Published | `rwb.guarantee.events.v1` |
| NoticeDelivered | EV-15 | Consumed | `rwb.comms.events.v1` |
| ProceedsMatched | EV-25 | Consumed | `rwb.payment.events.v1` |

An event shown with `—` has no number in the numbered catalogue: the Arch v5 catalogue calls these rows `+`, so the number is not specified in the source documents (GAP-1996; ASM-3223). Architecture v5 slide 18 names GuaranteeClaimFiled and GuaranteeClaimSettled; the AsyncAPI document carries the single message GuaranteeClaim (GAP-1996; ASM-3223).

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
| REQ-S3-001 | FEAT-GUA-01 | Written one epic ahead | With the story |
| REQ-S3-002 | FEAT-GUA-01 | Written one epic ahead | With the story |
| REQ-S3-003 | FEAT-GUA-01 | Written one epic ahead | With the story |
| REQ-S3-004 | FEAT-GUA-01 | Written one epic ahead | With the story |
| REQ-S3-005 | FEAT-GUA-01 | Written one epic ahead | With the story |
| REQ-S3-006 | FEAT-GUA-01 | Written one epic ahead | With the story |
| REQ-S3-007 | FEAT-GUA-01 | Written one epic ahead | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-S3-001 | POST | /api/recovery/guarantee/v1/cases/{caseId}/guarantee-claims | Treatment and offer C | E4 |
| API-S3-002 | PATCH | /api/recovery/guarantee/v1/guarantee-claims/{claimId} | Treatment and offer U | E4 |

The operation IDs, paths and operationIds of these endpoints are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-guarantee.yaml`; where an appendix row and the published operation differ, the published operation is the contract of T5.2.1 and the row keeps its ID for traceability (GAP-1997; ASM-3224).

### T-A.2 Endpoint detail

#### API-S3-001 POST /cases/{caseId}/guarantee-claims

| Item | Value |
|---|---|
| Purpose | Open a guarantee or TCG claim |
| Request | GuaranteeClaimRequest |
| Response | GuaranteeClaim |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Treatment and offer, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S3-002 PATCH /guarantee-claims/{claimId}

| Item | Value |
|---|---|
| Purpose | Record the claim result |
| Request | GuaranteeClaimUpdate |
| Response | GuaranteeClaim |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Treatment and offer, right U, scope applied |
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

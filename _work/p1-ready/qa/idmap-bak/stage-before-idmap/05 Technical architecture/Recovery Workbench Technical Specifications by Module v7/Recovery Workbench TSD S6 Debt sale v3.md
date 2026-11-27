SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench S6 Debt sale

Technical specification. SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD S6 Debt sale |
| Document ID | S6-RWB-TSD-v3 |
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
| Recovery Workbench FSD S6 Debt sale | FSD | Pair |
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

S6 Debt sale is one of the 19 services of Architecture v5: `rwb-debtsale` (service name Debt sale, module S6, wave 3, service epic `RWB-SVC-S6`). Version 3 adds this section so that the specification is read as the specification of one service: its identity, what it owns, and the decoupling patterns that replace the monolith's in-process calls. Every owner is taken from Microservice Ownership Map v1 and every identifier from Template and Rules R4 (ADR-013, ADR-014).

S6 is a saga with the transfer as its pivot; the data room is published through the partner gateway and the buyer file leaves through P2 (Architecture v5 slides 13 and 19).

### T0.1 Service identity

| Item | Value |
|---|---|
| Module | S6 Debt sale |
| Service | `rwb-debtsale` (Debt sale) |
| Service epic | `RWB-SVC-S6` |
| Wave | 3 |
| Schema | `rwb_debtsale` |
| Database login | `rwb_debtsale`: one login per service, with its own connection pool cap |
| REST base | `/api/recovery/debtsale/v1` |
| Kafka topic | `rwb.debtsale.events.v1`, with `.retry` and `.dlt` topics |
| Event names | `rwb.debtsale.<Event>.v1`, CloudEvents 1.0 in binary mode, key `caseId` |
| Temporal | namespace `rwb-recovery`; task queue `rwb-debtsale` |
| Java package | `th.co.scb.ace.workbench.recovery.debtsale` |
| Edge | gateway-bff for the staff screens of this service |
| Contract artefacts | `05 Technical architecture/Recovery Workbench API Specification v5/rwb-debtsale.yaml`; `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-debtsale.asyncapi.yaml` |
| Suggested owner, app development | TechX (suggested; any team may pick up this story) |
| Suggested owner, ACE DB | ACE team (suggested; any team may pick up this story) |

### T0.2 What this service owns

Architecture v5 slide 41 gives this service: lots, data room, buyer terms, bids, award, transfer. Table T0.2 states the same ownership in the form the Ownership Map uses, with the counts this specification carries. A table that the map assigns to another service is not built here, whatever T3 says (see the note under T3).

| Area | Owner and artefact | Count |
|---|---|---|
| Business tables in `rwb_debtsale` | `debt_sale_account`, `debt_sale_lot` | 2 |
| REST operations | appendix T-A and `rwb-debtsale.yaml` | 5 |
| Events published | EV-23 LotAwarded, AccountsTransferred | 2 |
| Workflows and schedules | DebtSaleWorkflow | 1 |
| Jobs | none | 0 |

### T0.3 Decoupling patterns applied

The left column is the pattern of Template and Rules R5.5; the middle column quotes the line of this specification that carries the legacy marker, where one is present; the right column is what replaces it in this service.

| DP | Legacy marker in this specification | How the service lands it |
|---|---|---|
| DP-01 | — | Owns its tables in `rwb_debtsale`; no other service reads them (ADR-014). |
| DP-02 | — | One login, `rwb_debtsale`, with its own connection pool cap. |
| DP-03 | `…logic; calls the rules component; writes the decision log entry before any change` | Local decision record plus DecisionRecorded (EV-08) on `rwb.decision-record.v1`. |
| DP-07 | `DF-SAL-023 / segment / LOV / varchar(20) / Yes / LOV-SEGMENT / Workbench` | Reference data and lists of values from the `rwb-case` contract (H RWB-PLT-E1043-CON). |
| DP-08 | `RW-SALEOFF Sale officer / R` | Authorisation through the `rwb-access` authorise contract and the guard library (H RWB-PLT-E1037-CON). |
| DP-09 | — | Outbox and inbox library; CloudEvents on `rwb.debtsale.events.v1` with retry topics and `.dlt`. |
| DP-10 | `Scheduler and batch / REUSE / ACE pattern: Quartz and Spring Batch / Jobs in the Batch and…` | Temporal Schedules and event-started workflows through the workflow kit (ADR-016). |
| DP-11 | `…reaches other modules only through their published interfaces and other systems only through COLLINS,…` | One REST hop, 2 s timeout, breaker; the consumer builds against the provider's fake (ADR-020). |
| DP-13 | `API-S6-001 / POST / /api/recovery/v1/debt-sale-lots / Debt sale C / E5` | REST base `/api/recovery/debtsale/v1`. |
| DP-14 | — | Topic `rwb.debtsale.events.v1`, retry topics and `.dlt`; naming library (H RWB-PLT-E1047-CON). |
| DP-15 | — | Per-service Flyway sequence in `rwb_debtsale`. |

### T0.4 What this service is not

- It holds no other service's table and no ACE table beyond the read-only `recovery.v_ace_*` views (DP-01, DP-05).
- It runs no shared Quartz job and touches no ACE batch table (DP-10; ADR-016).
- It publishes no data room: the pack is a P5 document set (DP-11).
- It is not a monolith module: the published Java interface of T2 is replaced by the contract set of T5.2 (DP-11; ADR-020).

## T1. Architecture overview

S6 Debt sale is delivered as the service `rwb-debtsale` (module S6, wave 3, service epic `RWB-SVC-S6`): one repository, one pipeline, one schema `rwb_debtsale` with one login, behind gateway-bff (ADR-013, ADR-014). It covers: lot building, data room, buyer terms, award, transfer. It reaches other modules only through the contracts of T5.2 and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| DebtSaleController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| DebtSaleService | Business logic; calls the rules component; writes the decision log entry before any change |
| DebtSaleRepository | Reads and writes the module's tables only |
| Jobs | Temporal Schedules and event-started workflows this service owns (T0.2, T5.2.1; DP-10) |
| Published interface | The contracts of T5.2: REST operations, events and workflows other services call; no table is read across modules (DP-11) |

The published interface of this table is the contract set of T5.2: the REST operations, the events and the workflows, not a Java interface in a shared classpath (DP-11; ADR-020). Components that the Ownership Map places in another service are stated in T0.2 and T5.2 and are built by that service.

## T3. Data model

Every object of T3 that Microservice Ownership Map v1 assigns to `rwb-debtsale` lives in schema `rwb_debtsale` with the standard columns of T3.0 (DP-01, DP-15; ADR-014). `debt_sale_lot` and `debt_sale_account` are this service's tables; the data room is a P5 document set and the buyer tape is a P2 file (DP-11, DP-16).

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

**debt_sale_lot** (NEW). A lot of accounts offered to debt buyers.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-SAL-020 | id | TEXT | uuid | Yes | None | Workbench |
| DF-SAL-021 | lot_no | TEXT | varchar(15) | Yes | None | Workbench |
| DF-SAL-022 | cut_off_date | DATE | date | Yes | None | Workbench |
| DF-SAL-023 | segment | LOV | varchar(20) | Yes | LOV-SEGMENT | Workbench |
| DF-SAL-024 | reserve_price | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-SAL-025 | buyer_partner_id | CROSS_REF | uuid | No | None | Workbench |
| DF-SAL-026 | buyer_class | LOV | varchar(10) | No | LOV-BUYER-CLASS | Workbench |
| DF-SAL-027 | signing_date | DATE | date | No | None | Workbench |
| DF-SAL-028 | approval_authority | TEXT | varchar(60) | No | None | Workbench |
| DF-SAL-029 | payment_terms | TEXT | varchar(400) | No | None | Workbench |
| DF-SAL-030 | status | LOV | varchar(12) | Yes | LOV-LOT-STATUS | Workbench |

**debt_sale_account** (NEW). An account in a debt sale lot.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-SAL-031 | id | TEXT | uuid | Yes | None | Workbench |
| DF-SAL-032 | lot_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-SAL-033 | account_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-SAL-034 | borrower_code | TEXT | varchar(20) | No | None | Workbench |
| DF-SAL-035 | outstanding | NUMBER | numeric(18,2) | Yes | None | Core bank (ALS) via COLLINS |
| DF-SAL-036 | selling_price | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-SAL-037 | put_back_status | LOV | varchar(12) | No | LOV-PUTBACK | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-BUYER-CLASS | AMC, NON_AMC |
| LOV-LOT-STATUS | BUILDING, OFFERED, AWARDED, TRANSFERRED, CLOSED |
| LOV-PUTBACK | NONE, CLAIMED, ACCEPTED, REJECTED |
| LOV-SEGMENT | RETAIL, SSME, CORPORATE |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| debt_sale_lot | buyer_partner_id | partner | Many to 0 or 1 |
| debt_sale_account | lot_id | debt_sale_lot | Many to 1 |
| debt_sale_account | account_id | loan_account | Many to 1 |

## T4. State machines and workflow

**DEBTSALE.** 41 rules over 29 states. The full table is in the Business Rules and Routing Logic workbook.

| Rule | From | Event | To |
|---|---|---|---|
| R-DS-01 | LOT_CANDIDATE_SELECTED | DEBT_SALE_CYCLE_OPENED | LOT_BUILT |
| R-DS-02 | LOT_CANDIDATE_SELECTED | ACCOUNT_EXCLUDED | CASE_EXCLUDED |
| R-DS-03 | CASE_EXCLUDED | EXCLUSION_CLEARED | BACK_TO_CASE_LIST |
| R-DS-04 | LOT_BUILT | LOT_PRICED | LOT_WITH_COMMITTEE |
| R-DS-05 | LOT_BUILT | LOT_TOO_THIN | LOT_BUILT |
| R-DS-06 | LOT_WITH_COMMITTEE | LOT_APPROVED_BY_COMMITTEE | LOT_APPROVED |
| R-DS-07 | LOT_WITH_COMMITTEE | RESERVE_RAISED | LOT_WITH_COMMITTEE |
| R-DS-08 | LOT_WITH_COMMITTEE | LOT_REFUSED | LOT_WITHDRAWN |
| R-DS-09 | LOT_WITHDRAWN | ACCOUNTS_RETURNED | BACK_TO_CASE_LIST |
| R-DS-10 | LOT_APPROVED | TAPE_BUILD_RUN | TAPE_PREPARED |
| R-DS-11 | TAPE_PREPARED | MASKING_CHECK_FAILED | TAPE_REJECTED |
| R-DS-12 | TAPE_REJECTED | TAPE_REBUILT | TAPE_PREPARED |
| R-DS-13 | TAPE_PREPARED | MASKING_CHECK_PASSED | DATA_ROOM_OPEN |
| R-DS-14 | DATA_ROOM_OPEN | BUYER_REQUESTED_ACCESS | BUYER_PENDING_KYC |
| R-DS-15 | BUYER_PENDING_KYC | KYC_PASSED | BUYER_CLEARED |
| R-DS-16 | BUYER_PENDING_KYC | KYC_FAILED | BUYER_REJECTED |
| R-DS-17 | BUYER_CLEARED | BIDDING_WINDOW_OPENED | BIDDING_OPEN |
| R-DS-18 | BIDDING_OPEN | BID_SUBMITTED | BIDS_RECEIVED |
| R-DS-19 | BIDS_RECEIVED | BIDDING_WINDOW_CLOSED | AWARD_PENDING |
| R-DS-20 | BIDS_RECEIVED | BEST_BID_BELOW_RESERVE | BID_BELOW_RESERVE |
| R-DS-21 | BID_BELOW_RESERVE | LOT_REOFFERED | BIDDING_OPEN |
| R-DS-22 | BID_BELOW_RESERVE | LOT_NOT_CLEARED | LOT_WITHDRAWN |
| R-DS-23 | AWARD_PENDING | AWARD_CONFIRMED | LOT_AWARDED |
| R-DS-24 | LOT_AWARDED | SETTLEMENT_TERM_STARTED | SETTLEMENT_PENDING |
| R-DS-25 | SETTLEMENT_PENDING | BUYER_SETTLED | SETTLED |
| and 16 more | | | |

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-25 | Debt buyers | Out | File through the data room | Per lot |

### T5.2 Contracts

Version 3 states every cross-module dependency of this module as a contract, so that the service is built against a published artefact and its fake (ADR-020; DP-11). The artefact per call type is: OpenAPI 3.1 for REST, AsyncAPI 3.0 for Kafka, the Temporal interface named here for a workflow or activity, the Interface Specifications manifest for a file, the Nexus operation for the ACE restructure calculator, and a grant on the view for SQL. No row of this section reads another service's table (DP-01). Every consumed contract is class C (Template and Rules R5.4): it never blocks the build, because the consumer builds against the fake, and the real cross-service behaviour is class I work on an integration story. Architecture v5 slides 13 to 20 name a few operations differently from the published files of 22 November 2026; the published file is the artefact the fake is generated from and is the one cited here (GAP-1997; ASM-3224).

#### T5.2.1 Contracts provided

The REST operations of this service are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-debtsale.yaml` (5.0.0, 22 November 2026) under the base `/api/recovery/debtsale/v1`. Appendix T-A holds the endpoint IDs, the access right and the first release of each one.

| # | Method | Path | operationId |
|---|---|---|---|
| 1 | POST | `/debt-sale-lots` | `postDebtSaleLots` |
| 2 | GET | `/debt-sale-lots/{lotId}` | `getDebtSaleLotsLotid` |
| 3 | POST | `/debt-sale-lots/{lotId}/award` | `postDebtSaleLotsLotidAward` |
| 4 | GET | `/partner/data-room/{lotId}` | `getPartnerDataRoomLotid` |
| 5 | POST | `/partner/data-room/{lotId}/bids` | `postPartnerDataRoomLotidBids` |

Workflows, schedules, files and views this service provides:

| Contract | Type | Called by or target | Note |
|---|---|---|---|
| DebtSaleWorkflow (saga, pivot at transfer) | Temporal workflow | P3 rwb-case | Stage workflow of the case; runs on rwb-debtsale |

Events this service publishes (AsyncAPI 3.0, CloudEvents 1.0):

| Event | EV | Topic | Consumers |
|---|---|---|---|
| LotAwarded | EV-23 | `rwb.debtsale.events.v1` | rwb-case, rwb-payment |
| AccountsTransferred | — | `rwb.debtsale.events.v1` | rwb-case, rwb-reporting |

#### T5.2.2 Contracts consumed

| Contract | Type | Provider | Class | Failure path |
|---|---|---|---|---|
| Data room pack | Temporal activity | P5 rwb-document | C | Workflow retry policy; the caller keeps its state (DP-12) |
| Approval | Temporal child workflow | P7 rwb-decision | C | Workflow retry policy; the caller keeps its state (DP-12) |
| deliverFile(manifest) for the buyer file | Temporal activity | P2 rwb-integration | C | Workflow retry policy; the caller keeps its state (DP-12) |
| postProceeds | Temporal activity | P8 rwb-payment | C | Workflow retry policy; the caller keeps its state (DP-12) |

Events this service consumes:

| Event | EV | Provider topic | Provider | Class | Failure path |
|---|---|---|---|---|---|
| ProceedsMatched | EV-25 | `rwb.payment.events.v1` | P8 rwb-payment | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |

#### T5.2.3 Call-type summary

| Call type | Provided | Consumed | Artefact |
|---|---|---|---|
| REST | 5 | 0 | OpenAPI 3.1, one file per service |
| Kafka (events) | 2 | 1 | AsyncAPI 3.0, one file per service |
| Temporal | 1 | 4 | Workflow and activity interfaces, queue `rwb-debtsale` |
| File | 0 | 0 | Interface Specifications manifest and the SAS link |
| Nexus | 0 | 0 | Nexus operation into ACE |
| SQL | 0 | 0 | Read-only grant on the view |

A contract change is a new version of the artefact, never a code change in the consumer (ADR-020). The provider named in T5.2.2 is the owner in Microservice Ownership Map v1, and the consumer list of each event is the Arch v5 event catalogue on slides 42 and 43.

### T5.3 Events

The event contract of this service is `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-debtsale.asyncapi.yaml`; the shared decision-record contract is `asyncapi/rwb.decision-record.v1.asyncapi.yaml`. Every service publishes DecisionRecorded (EV-08) to `rwb.decision-record.v1` from its outbox in the same transaction as its state change (DP-03, DP-09; ADR-015, ADR-022); consuming services dedupe through their inbox table. Events carry identifiers and facts, never personal data (Event and Messaging Design v4, sheet Rules).

| Event | EV | Direction | Topic |
|---|---|---|---|
| LotAwarded | EV-23 | Published | `rwb.debtsale.events.v1` |
| AccountsTransferred | — | Published | `rwb.debtsale.events.v1` |
| ProceedsMatched | EV-25 | Consumed | `rwb.payment.events.v1` |

An event shown with `—` has no number in the numbered catalogue: the Arch v5 catalogue calls these rows `+`, so the number is not specified in the source documents (GAP-1996; ASM-3223).

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Debt sale |
|---|---|
| RW-SALEOFF Sale officer | R |
| RW-NPAMGR NPA and asset manager | R |
| RW-DEBTSALE Debt sale officer | CRUA |
| RW-WRITEOFF Write-off team member | R |
| RW-CREDITAD Credit Administration officer | R |
| RW-AGENCYMG Partner and agency manager | R |
| RW-CONDUCT Conduct and QA officer | R |
| RW-PRODHEAD Product head (Mortgage, HP, SSME) | RA |
| RW-HEADNPA Head of NPA | R |
| RW-HEADASL Head of Asset Liquidity | RA |
| RW-RISK Risk and model risk officer | R |
| RW-COE Center of excellence analyst | R |
| RW-FINANCE Finance and CFO delegate | R |
| RW-AUDIT Internal audit | R |
| RW-BIANAL Reporting and BI analyst | R |
| RW-TRIBE Tribe lead and squad members | R |
| PT-BUYER Debt buyer and AMC | RU |
| PT-RAMC RAMC user | R |
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
| REQ-S6-001 | FEAT-DBS-01 | Written one epic ahead | With the story |
| REQ-S6-002 | FEAT-DBS-01 | Written one epic ahead | With the story |
| REQ-S6-003 | FEAT-DBS-01 | Written one epic ahead | With the story |
| REQ-S6-004 | FEAT-DBS-05 | Written one epic ahead | With the story |
| REQ-S6-005 | FEAT-DBS-05 | Written one epic ahead | With the story |
| REQ-S6-006 | FEAT-DBS-05 | Written one epic ahead | With the story |
| REQ-S6-007 | FEAT-DBS-05 | Written one epic ahead | With the story |
| REQ-S6-008 | FEAT-DBS-05 | Written one epic ahead | With the story |
| REQ-S6-009 | FEAT-DBS-05 | Written one epic ahead | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-S6-001 | POST | /api/recovery/debtsale/v1/debt-sale-lots | Debt sale C | E5 |
| API-S6-002 | GET | /api/recovery/debtsale/v1/debt-sale-lots/{lotId} | Debt sale R | E5 |
| API-S6-003 | POST | /api/recovery/debtsale/v1/debt-sale-lots/{lotId}/award | Debt sale A | E6 |
| API-S6-004 | GET | /api/recovery/debtsale/v1/partner/data-room/{lotId} | Partner portal R | E5 |
| API-S6-005 | POST | /api/recovery/debtsale/v1/partner/data-room/{lotId}/bids | Partner portal C | E5 |

The operation IDs, paths and operationIds of these endpoints are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-debtsale.yaml`; where an appendix row and the published operation differ, the published operation is the contract of T5.2.1 and the row keeps its ID for traceability (GAP-1997; ASM-3224).

### T-A.2 Endpoint detail

#### API-S6-001 POST /debt-sale-lots

| Item | Value |
|---|---|
| Purpose | Create a lot from eligible accounts |
| Request | LotRequest |
| Response | DebtSaleLot |
| Errors | 401, 403, 409, 422, 503 |
| Authorization | Debt sale, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S6-002 GET /debt-sale-lots/{lotId}

| Item | Value |
|---|---|
| Purpose | Read a lot with its accounts, reserve and bids |
| Request | None |
| Response | DebtSaleLot |
| Errors | 401, 403, 404, 503 |
| Authorization | Debt sale, right R, scope applied |
| Idempotency | Not applicable |

#### API-S6-003 POST /debt-sale-lots/{lotId}/award

| Item | Value |
|---|---|
| Purpose | Award a lot to a buyer after the bids close |
| Request | AwardRequest |
| Response | DecisionLogEntry |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Debt sale, right A, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S6-004 GET /partner/data-room/{lotId}

| Item | Value |
|---|---|
| Purpose | Read the lot tape and documents for an admitted buyer |
| Request | None |
| Response | DataRoom |
| Errors | 401, 403, 404, 503 |
| Authorization | Partner portal, right R, scope applied |
| Idempotency | Not applicable |

#### API-S6-005 POST /partner/data-room/{lotId}/bids

| Item | Value |
|---|---|
| Purpose | Submit a bid on a lot |
| Request | BidRequest |
| Response | Bid |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Partner portal, right C, scope applied |
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

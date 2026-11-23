SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench S5 Assets and auction

Technical specification. SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD S5 Assets and auction |
| Document ID | S5-RWB-TSD-v3 |
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
| Recovery Workbench FSD S5 Assets and auction | FSD | Pair |
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

S5 Assets and auction is one of the 19 services of Architecture v5: `rwb-asset` (service name Asset, module S5, wave 2, service epic `RWB-SVC-S5`). Version 3 adds this section so that the specification is read as the specification of one service: its identity, what it owns, and the decoupling patterns that replace the monolith's in-process calls. Every owner is taken from Microservice Ownership Map v1 and every identifier from Template and Rules R4 (ADR-013, ADR-014).

S5 owns the disposal path from the judgment to the proceeds, with the auction vendor instructed through S9 and the money posted through P8 (Architecture v5 slide 19).

### T0.1 Service identity

| Item | Value |
|---|---|
| Module | S5 Assets and auction |
| Service | `rwb-asset` (Asset) |
| Service epic | `RWB-SVC-S5` |
| Wave | 2 |
| Schema | `rwb_asset` |
| Database login | `rwb_asset`: one login per service, with its own connection pool cap |
| REST base | `/api/recovery/asset/v1` |
| Kafka topic | `rwb.asset.events.v1`, with `.retry` and `.dlt` topics |
| Event names | `rwb.asset.<Event>.v1`, CloudEvents 1.0 in binary mode, key `caseId` |
| Temporal | namespace `rwb-recovery`; task queue `rwb-asset` |
| Java package | `th.co.scb.ace.workbench.recovery.asset` |
| Edge | gateway-bff for the staff screens of this service |
| Contract artefacts | `05 Technical architecture/Recovery Workbench API Specification v5/rwb-asset.yaml`; `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-asset.asyncapi.yaml` |
| Suggested owner, app development | TechX (suggested; any team may pick up this story) |
| Suggested owner, ACE DB | ACE team (suggested; any team may pick up this story) |

### T0.2 What this service owns

Architecture v5 slide 41 gives this service: assets taken on, holding, floor price, listings, auction rounds. Table T0.2 states the same ownership in the form the Ownership Map uses, with the counts this specification carries. A table that the map assigns to another service is not built here, whatever T3 says (see the note under T3).

| Area | Owner and artefact | Count |
|---|---|---|
| Business tables in `rwb_asset` | `asset_sale`, `listing` | 2 |
| REST operations | appendix T-A and `rwb-asset.yaml` | 4 |
| Events published | EV-22 AssetTakenOn, AssetSold | 2 |
| Workflows and schedules | AssetDisposalWorkflow | 1 |
| Jobs | JOB-19 | 1 |

### T0.3 Decoupling patterns applied

The left column is the pattern of Template and Rules R5.5; the middle column quotes the line of this specification that carries the legacy marker, where one is present; the right column is what replaces it in this service.

| DP | Legacy marker in this specification | How the service lands it |
|---|---|---|
| DP-01 | — | Owns its tables in `rwb_asset`; no other service reads them (ADR-014). |
| DP-02 | — | One login, `rwb_asset`, with its own connection pool cap. |
| DP-03 | `…logic; calls the rules component; writes the decision log entry before any change` | Local decision record plus DecisionRecorded (EV-08) on `rwb.decision-record.v1`. |
| DP-07 | `DF-COL-033 / asset_type / LOV / varchar(20) / Yes / LOV-ASSET-TYPE / AMIS` | Reference data and lists of values from the `rwb-case` contract (H RWB-PLT-E1043-CON). |
| DP-08 | `RW-CASEOWN Case owner / R` | Authorisation through the `rwb-access` authorise contract and the guard library (H RWB-PLT-E1037-CON). |
| DP-09 | — | Outbox and inbox library; CloudEvents on `rwb.asset.events.v1` with retry topics and `.dlt`. |
| DP-10 | `Scheduler and batch / REUSE / ACE pattern: Quartz and Spring Batch / Jobs in the Batch and…` | Temporal Schedules and event-started workflows through the workflow kit (ADR-016). |
| DP-11 | `…reaches other modules only through their published interfaces and other systems only through COLLINS,…` | One REST hop, 2 s timeout, breaker; the consumer builds against the provider's fake (ADR-020). |
| DP-13 | `API-S5-001 / GET / /api/recovery/v1/assets / Asset and disposal R / E3` | REST base `/api/recovery/asset/v1`. |
| DP-14 | — | Topic `rwb.asset.events.v1`, retry topics and `.dlt`; naming library (H RWB-PLT-E1047-CON). |
| DP-15 | — | Per-service Flyway sequence in `rwb_asset`. |

### T0.4 What this service is not

- It holds no other service's table and no ACE table beyond the read-only `recovery.v_ace_*` views (DP-01, DP-05).
- It runs no shared Quartz job and touches no ACE batch table (DP-10; ADR-016).
- It holds no asset record: the asset is an ACE record read through the read path (DP-05).
- It is not a monolith module: the published Java interface of T2 is replaced by the contract set of T5.2 (DP-11; ADR-020).

## T1. Architecture overview

S5 Assets and auction is delivered as the service `rwb-asset` (module S5, wave 2, service epic `RWB-SVC-S5`): one repository, one pipeline, one schema `rwb_asset` with one login, behind gateway-bff (ADR-013, ADR-014). It covers: asset record, holding, floor price, listing, auction rounds, RAMC. It reaches other modules only through the contracts of T5.2 and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| AssetsAndAuctionController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| AssetsAndAuctionService | Business logic; calls the rules component; writes the decision log entry before any change |
| AssetsAndAuctionRepository | Reads and writes the module's tables only |
| Jobs | Temporal Schedules and event-started workflows this service owns (T0.2, T5.2.1; DP-10) |
| Published interface | The contracts of T5.2: REST operations, events and workflows other services call; no table is read across modules (DP-11) |

The published interface of this table is the contract set of T5.2: the REST operations, the events and the workflows, not a Java interface in a shared classpath (DP-11; ADR-020). Components that the Ownership Map places in another service are stated in T0.2 and T5.2 and are built by that service.

## T3. Data model

Every object of T3 that Microservice Ownership Map v1 assigns to `rwb-asset` lives in schema `rwb_asset` with the standard columns of T3.0 (DP-01, DP-15; ADR-014). `listing` and `asset_sale` are this service's tables. `asset` is an ACE record read through the read path and is not a table of this service; the Ownership Map gives S5 no `asset` row.

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

**asset** (EXTEND ACE Asset). An asset the bank holds after repossession, deed in lieu or auction purchase.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-COL-028 | id | TEXT | uuid | Yes | None | Workbench |
| DF-COL-029 | case_id | CROSS_REF | uuid | No | None | Workbench |
| DF-COL-030 | collateral_id | CROSS_REF | uuid | No | None | Workbench |
| DF-COL-031 | asset_ref | TEXT | varchar(20) | Yes | None | AMIS |
| DF-COL-032 | asset_code | TEXT | varchar(20) | No | None | AMIS |
| DF-COL-033 | asset_type | LOV | varchar(20) | Yes | LOV-ASSET-TYPE | AMIS |
| DF-COL-034 | transfer_in_type | LOV | varchar(20) | Yes | LOV-TRANSFER-IN | AMIS |
| DF-COL-035 | from_segment | LOV | varchar(20) | No | LOV-SEGMENT | AMIS |
| DF-COL-036 | transfer_in_date | DATE | date | Yes | None | AMIS |
| DF-COL-037 | book_value | NUMBER | numeric(18,2) | Yes | None | AMIS |
| DF-COL-038 | auction_purchase_price | NUMBER | numeric(18,2) | No | None | AMIS |
| DF-COL-039 | repossessed_date | DATE | date | No | None | RPS |
| DF-COL-040 | stock_date | DATE | date | No | None | RPS |
| DF-COL-041 | holding_status | LOV | varchar(15) | Yes | LOV-HOLDING | Workbench |
| DF-COL-042 | holding_cost_to_date | NUMBER | numeric(18,2) | No | None | Workbench |

**listing** (NEW). An asset offered for sale, with its prices and rounds.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-SAL-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-SAL-002 | asset_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-SAL-003 | sale_channel | LOV | varchar(15) | Yes | LOV-SALE-CHANNEL | Workbench |
| DF-SAL-004 | start_price | NUMBER | numeric(18,2) | Yes | None | Workbench |
| DF-SAL-005 | floor_price | NUMBER | numeric(18,2) | Yes | None | Workbench |
| DF-SAL-006 | round_no | NUMBER | integer | Yes | None | Workbench |
| DF-SAL-007 | listed_at | DATE | timestamptz | No | None | Workbench |
| DF-SAL-008 | status | LOV | varchar(12) | Yes | LOV-LISTING | Workbench |

**asset_sale** (NEW). The sale of an asset.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-SAL-009 | id | TEXT | uuid | Yes | None | Workbench |
| DF-SAL-010 | asset_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-SAL-011 | listing_id | CROSS_REF | uuid | No | None | Workbench |
| DF-SAL-012 | contract_date | DATE | date | Yes | None | AMIS |
| DF-SAL-013 | sale_date | DATE | date | Yes | None | AMIS |
| DF-SAL-014 | sale_price | NUMBER | numeric(18,2) | Yes | None | AMIS |
| DF-SAL-015 | transfer_fee | NUMBER | numeric(18,2) | No | None | AMIS |
| DF-SAL-016 | specific_business_tax | NUMBER | numeric(18,2) | No | None | AMIS |
| DF-SAL-017 | corporate_income_tax | NUMBER | numeric(18,2) | No | None | AMIS |
| DF-SAL-018 | gain_loss | FORMULA | numeric(18,2) | No | None | Workbench |
| DF-SAL-019 | incentive_amount | NUMBER | numeric(18,2) | No | None | AMIS |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-ASSET-TYPE | DETACHED_HOUSE, TOWNHOUSE, CONDOMINIUM, LAND, COMMERCIAL_BUILDING, VEHICLE |
| LOV-HOLDING | HELD, LISTED, UNDER_OFFER, SOLD, TRANSFERRED, RENTED |
| LOV-LISTING | DRAFT, LIVE, UNDER_OFFER, SOLD, WITHDRAWN |
| LOV-SALE-CHANNEL | DUTCH_AUCTION, BROKER, DIRECT, LED_AUCTION, RAMC |
| LOV-SEGMENT | RETAIL, SSME, CORPORATE |
| LOV-TRANSFER-IN | AUCTION_PURCHASE, DEED_IN_LIEU, REPOSSESSION |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| asset | case_id | recovery_case | Many to 0 or 1 |
| asset | collateral_id | collateral | Many to 0 or 1 |
| listing | asset_id | asset | Many to 1 |
| asset_sale | asset_id | asset | Many to 1 |
| asset_sale | listing_id | listing | Many to 0 or 1 |

## T4. State machines and workflow

**DISPOSAL.** 72 rules over 40 states. The full table is in the Business Rules and Routing Logic workbook.

| Rule | From | Event | To |
|---|---|---|---|
| R-DIS-01 | ASSET_PENDING_TAKE_ON | REPOSSESSION_COMPLETED | ASSET_ON_BOOKS |
| R-DIS-02 | ASSET_PENDING_TAKE_ON | DIL_TRANSFER_REGISTERED | ASSET_ON_BOOKS |
| R-DIS-03 | ASSET_PENDING_TAKE_ON | LED_HANDOVER_RECEIVED | ASSET_ON_BOOKS |
| R-DIS-04 | ASSET_PENDING_TAKE_ON | STATUTORY_NOTICE_FAILED | FAILED_NOTICE_QUEUE |
| R-DIS-05 | FAILED_NOTICE_QUEUE | NOTICE_REISSUED | ASSET_PENDING_TAKE_ON |
| R-DIS-06 | ASSET_ON_BOOKS | ASSET_RECORD_CONFIRMED | ASSET_HELD |
| R-DIS-07 | ASSET_ON_BOOKS | TITLE_UNRESOLVED | TITLE_BLOCKED |
| R-DIS-08 | TITLE_BLOCKED | TITLE_CLEARED | ASSET_HELD |
| R-DIS-09 | ASSET_HELD | PROVISION_STEP_DUE | ASSET_HELD |
| R-DIS-10 | ASSET_HELD | WORK_ORDER_RAISED | WORK_ORDER_OPEN |
| R-DIS-11 | WORK_ORDER_OPEN | WORK_ACCEPTED | ASSET_HELD |
| R-DIS-12 | WORK_ORDER_OPEN | WORK_REFUSED | WORK_ORDER_OPEN |
| R-DIS-13 | ASSET_HELD | OCCUPANTS_REFUSE_POSSESSION | EVICTION_REQUIRED |
| R-DIS-14 | EVICTION_REQUIRED | POSSESSION_TAKEN | ASSET_HELD |
| R-DIS-15 | ASSET_HELD | REAPPRAISAL_CYCLE_DUE | REAPPRAISAL_ORDERED |
| R-DIS-16 | REAPPRAISAL_ORDERED | VALUER_REPORTED | REAPPRAISAL_RECEIVED |
| R-DIS-17 | REAPPRAISAL_RECEIVED | VALUE_ACCEPTED | ASSET_HELD |
| R-DIS-18 | REAPPRAISAL_RECEIVED | VALUE_REJECTED | REAPPRAISAL_ORDERED |
| R-DIS-19 | ASSET_HELD | READY_TO_SELL | ROUTE_RECOMMENDED |
| R-DIS-20 | ROUTE_RECOMMENDED | ROUTE_SUBMITTED | ROUTE_WITH_APPROVER |
| R-DIS-21 | ROUTE_WITH_APPROVER | ROUTE_APPROVED | ROUTE_APPROVED_AUCTION |
| R-DIS-22 | ROUTE_WITH_APPROVER | ROUTE_APPROVED | ROUTE_APPROVED_AUCTION |
| R-DIS-23 | ROUTE_WITH_APPROVER | ROUTE_APPROVED | ROUTE_APPROVED_RAMC |
| R-DIS-24 | ROUTE_WITH_APPROVER | ROUTE_APPROVED | ROUTE_APPROVED_BUYBACK |
| R-DIS-25 | ROUTE_WITH_APPROVER | ROUTE_APPROVED | RENTAL_ACTIVE |
| and 47 more | | | |

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-11 | SVAF | In | File load | Weekly |
| INT-12 | AMIS | In | File load | Monthly |
| INT-13 | RPS | In | File load | Weekly |
| INT-27 | HOME.SCB | Out | Not available today; published by the sale officer | As listed |

### T5.2 Contracts

Version 3 states every cross-module dependency of this module as a contract, so that the service is built against a published artefact and its fake (ADR-020; DP-11). The artefact per call type is: OpenAPI 3.1 for REST, AsyncAPI 3.0 for Kafka, the Temporal interface named here for a workflow or activity, the Interface Specifications manifest for a file, the Nexus operation for the ACE restructure calculator, and a grant on the view for SQL. No row of this section reads another service's table (DP-01). Every consumed contract is class C (Template and Rules R5.4): it never blocks the build, because the consumer builds against the fake, and the real cross-service behaviour is class I work on an integration story. Architecture v5 slides 13 to 20 name a few operations differently from the published files of 22 November 2026; the published file is the artefact the fake is generated from and is the one cited here (GAP-1997; ASM-3224).

#### T5.2.1 Contracts provided

The REST operations of this service are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-asset.yaml` (5.0.0, 22 November 2026) under the base `/api/recovery/asset/v1`. Appendix T-A holds the endpoint IDs, the access right and the first release of each one.

| # | Method | Path | operationId |
|---|---|---|---|
| 1 | GET | `/assets` | `getAssets` |
| 2 | GET | `/assets/{assetKey}` | `getAssetsAssetkey` |
| 3 | POST | `/assets/{assetKey}/listings` | `postAssetsAssetkeyListings` |
| 4 | POST | `/listings/{listingId}/rounds` | `postListingsListingidRounds` |

Workflows, schedules, files and views this service provides:

| Contract | Type | Called by or target | Note |
|---|---|---|---|
| AssetDisposalWorkflow | Temporal workflow | P3 rwb-case | Stage workflow of the case; runs on rwb-asset |
| Re-appraisal, monthly | Temporal Schedule | S5 rwb-asset | JOB-19 (DP-10) |

Events this service publishes (AsyncAPI 3.0, CloudEvents 1.0):

| Event | EV | Topic | Consumers |
|---|---|---|---|
| AssetTakenOn | EV-22 | `rwb.asset.events.v1` | rwb-case, rwb-payment |
| AssetSold | — | `rwb.asset.events.v1` | rwb-payment, rwb-case |

#### T5.2.2 Contracts consumed

| Contract | Type | Provider | Class | Failure path |
|---|---|---|---|---|
| issueInstruction (auction vendor) | Temporal activity | S9 rwb-partner | C | Workflow retry policy; the caller keeps its state (DP-12) |
| Approval | Temporal child workflow | P7 rwb-decision | C | Workflow retry policy; the caller keeps its state (DP-12) |
| postProceeds | Temporal activity | P8 rwb-payment | C | Workflow retry policy; the caller keeps its state (DP-12) |

Events this service consumes:

| Event | EV | Provider topic | Provider | Class | Failure path |
|---|---|---|---|---|---|
| JudgmentRecorded | — | `rwb.litigation.events.v1` | S4 rwb-litigation | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| AuctionResult | — | `rwb.litigation.events.v1` | S4 rwb-litigation | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |
| ProceedsMatched | EV-25 | `rwb.payment.events.v1` | P8 rwb-payment | C | Retry 1 min, 10 min, 1 h, then `.dlt`; inbox dedupe |

#### T5.2.3 Call-type summary

| Call type | Provided | Consumed | Artefact |
|---|---|---|---|
| REST | 4 | 0 | OpenAPI 3.1, one file per service |
| Kafka (events) | 2 | 3 | AsyncAPI 3.0, one file per service |
| Temporal | 2 | 3 | Workflow and activity interfaces, queue `rwb-asset` |
| File | 0 | 0 | Interface Specifications manifest and the SAS link |
| Nexus | 0 | 0 | Nexus operation into ACE |
| SQL | 0 | 0 | Read-only grant on the view |

A contract change is a new version of the artefact, never a code change in the consumer (ADR-020). The provider named in T5.2.2 is the owner in Microservice Ownership Map v1, and the consumer list of each event is the Arch v5 event catalogue on slides 42 and 43.

### T5.3 Events

The event contract of this service is `05 Technical architecture/Recovery Workbench API Specification v5/asyncapi/rwb-asset.asyncapi.yaml`; the shared decision-record contract is `asyncapi/rwb.decision-record.v1.asyncapi.yaml`. Every service publishes DecisionRecorded (EV-08) to `rwb.decision-record.v1` from its outbox in the same transaction as its state change (DP-03, DP-09; ADR-015, ADR-022); consuming services dedupe through their inbox table. Events carry identifiers and facts, never personal data (Event and Messaging Design v4, sheet Rules).

| Event | EV | Direction | Topic |
|---|---|---|---|
| AssetTakenOn | EV-22 | Published | `rwb.asset.events.v1` |
| AssetSold | — | Published | `rwb.asset.events.v1` |
| JudgmentRecorded | — | Consumed | `rwb.litigation.events.v1` |
| AuctionResult | — | Consumed | `rwb.litigation.events.v1` |
| ProceedsMatched | EV-25 | Consumed | `rwb.payment.events.v1` |

An event shown with `—` has no number in the numbered catalogue: the Arch v5 catalogue calls these rows `+`, so the number is not specified in the source documents (GAP-1996; ASM-3223).

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Asset and disposal |
|---|---|
| RW-CASEOWN Case owner | R |
| RW-TEAMMGR Team manager | R |
| RW-FIELDCOL Field collector | R |
| RW-COMPLAIN Complaint officer | R |
| RW-LITOFF Litigation officer | R |
| RW-ENFORCE Enforcement owner | CRU |
| RW-LEGAL Legal counsel | R |
| RW-SALEOFF Sale officer | CRUA |
| RW-NPAMGR NPA and asset manager | CRU |
| RW-DEBTSALE Debt sale officer | R |
| RW-WRITEOFF Write-off team member | R |
| RW-CREDITAD Credit Administration officer | R |
| RW-AGENCYMG Partner and agency manager | R |
| RW-CONDUCT Conduct and QA officer | R |
| RW-PRODHEAD Product head (Mortgage, HP, SSME) | RA |
| RW-HEADLIT Head of Litigation | R |
| RW-HEADNPA Head of NPA | RA |
| RW-HEADASL Head of Asset Liquidity | RA |
| RW-RISK Risk and model risk officer | R |
| RW-COE Center of excellence analyst | R |
| RW-FINANCE Finance and CFO delegate | R |
| RW-AUDIT Internal audit | R |
| RW-BIANAL Reporting and BI analyst | R |
| RW-TRIBE Tribe lead and squad members | R |
| PT-VALUER Valuer | R |
| PT-AUCTION Auction vendor | RU |
| PT-RAMC RAMC user | RU |
| SY-CASEWF Case workflow module | R |
| SY-RULES Rules component | R |
| SY-DATALOAD Data load from COLLINS | CU |
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
| REQ-S5-001 | FEAT-AST-01 | Written one epic ahead | With the story |
| REQ-S5-002 | FEAT-AST-01 | Written one epic ahead | With the story |
| REQ-S5-003 | FEAT-AST-01 | Written one epic ahead | With the story |
| REQ-S5-004 | FEAT-AST-01 | Written one epic ahead | With the story |
| REQ-S5-005 | FEAT-AST-01 | Written one epic ahead | With the story |
| REQ-S5-006 | FEAT-AST-08 | Written one epic ahead | With the story |
| REQ-S5-007 | FEAT-AST-08 | Written one epic ahead | With the story |
| REQ-S5-008 | FEAT-AST-08 | Written one epic ahead | With the story |
| REQ-S5-009 | FEAT-AST-08 | Written one epic ahead | With the story |
| REQ-S5-010 | FEAT-AST-08 | Written one epic ahead | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-S5-001 | GET | /api/recovery/asset/v1/assets | Asset and disposal R | E3 |
| API-S5-002 | GET | /api/recovery/asset/v1/assets/{assetId} | Asset and disposal R | E3 |
| API-S5-003 | POST | /api/recovery/asset/v1/assets/{assetId}/valuations | Asset and disposal C | E3 |
| API-S5-004 | POST | /api/recovery/asset/v1/assets/{assetId}/listings | Asset and disposal C | E3 |
| API-S5-005 | POST | /api/recovery/asset/v1/listings/{listingId}/rounds | Asset and disposal U | E4 |

The operation IDs, paths and operationIds of these endpoints are published in `05 Technical architecture/Recovery Workbench API Specification v5/rwb-asset.yaml`; where an appendix row and the published operation differ, the published operation is the contract of T5.2.1 and the row keeps its ID for traceability (GAP-1997; ASM-3224).

### T-A.2 Endpoint detail

#### API-S5-001 GET /assets

| Item | Value |
|---|---|
| Purpose | List assets held with age, holding cost and sale status |
| Request | Query: type, status, region, page, size |
| Response | AssetPage |
| Errors | 401, 403, 503 |
| Authorization | Asset and disposal, right R, scope applied |
| Idempotency | Not applicable |

#### API-S5-002 GET /assets/{assetId}

| Item | Value |
|---|---|
| Purpose | Read one asset with title, condition, valuations, costs and listing |
| Request | None |
| Response | Asset |
| Errors | 401, 403, 404, 503 |
| Authorization | Asset and disposal, right R, scope applied |
| Idempotency | Not applicable |

#### API-S5-003 POST /assets/{assetId}/valuations

| Item | Value |
|---|---|
| Purpose | Order or record a valuation |
| Request | ValuationRequest |
| Response | Valuation |
| Errors | 401, 403, 404, 422, 503 |
| Authorization | Asset and disposal, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S5-004 POST /assets/{assetId}/listings

| Item | Value |
|---|---|
| Purpose | Set the list price and floor and send for approval |
| Request | ListingRequest |
| Response | Approval |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Asset and disposal, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S5-005 POST /listings/{listingId}/rounds

| Item | Value |
|---|---|
| Purpose | Record an auction round and its result |
| Request | AuctionRoundRequest |
| Response | AssetSale |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Asset and disposal, right U, scope applied |
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

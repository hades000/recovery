# Recovery Workbench S5 Assets and auction

Technical specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD S5 Assets and auction |
| Document ID | S5-RWB-TSD-v2 |
| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD S5 Assets and auction | FSD | Pair |
| Recovery Workbench Target Architecture | Architecture | Parent |
| Recovery Workbench Logical Data Model and Data Dictionary | Data | Source of T3 |
| Recovery Workbench API Specification | API | Source of appendix T-A |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit, PII and SOC logging | REUSE | ACE common module | Called through the published interface |
| Scheduler and batch | REUSE | ACE pattern: Quartz and Spring Batch | Jobs in the Batch and Scheduling Design |
| Outbox and retry | REUSE | Error Handling and Resilience Standard | Through P2 |
| Rules evaluation | REUSE | Rules Engine Design | Through the rules component |

## T1. Architecture overview

S5 Assets and auction is part of the recovery module in the ACE service: one service, one repository, one front end. It covers: asset record, holding, floor price, listing, auction rounds, RAMC. It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| AssetsAndAuctionController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| AssetsAndAuctionService | Business logic; calls the rules component; writes the decision log entry before any change |
| AssetsAndAuctionRepository | Reads and writes the module's tables only |
| Jobs | Quartz and Spring Batch jobs the module owns |
| Published interface | Java interface other modules call; no table is read across modules |

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

### T5.2 Cross-module interfaces

Calls go through the published Java interfaces: P3 for the case, P7 for the decision log, P4 for access and reference data, P5 for documents, P6 for notices.

### T5.3 Events

| Event | Direction |
|---|---|
| AssetTakenOn | Published |

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
| API-S5-001 | GET | /api/recovery/v1/assets | Asset and disposal R | E3 |
| API-S5-002 | GET | /api/recovery/v1/assets/{assetId} | Asset and disposal R | E3 |
| API-S5-003 | POST | /api/recovery/v1/assets/{assetId}/valuations | Asset and disposal C | E3 |
| API-S5-004 | POST | /api/recovery/v1/assets/{assetId}/listings | Asset and disposal C | E3 |
| API-S5-005 | POST | /api/recovery/v1/listings/{listingId}/rounds | Asset and disposal U | E4 |

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

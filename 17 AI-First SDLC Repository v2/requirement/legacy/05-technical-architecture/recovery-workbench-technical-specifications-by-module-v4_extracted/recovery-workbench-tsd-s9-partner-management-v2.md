<!-- source: 05 Technical architecture/Recovery Workbench Technical Specifications by Module v4.zip!Recovery Workbench TSD S9 Partner management v2.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `05 Technical architecture/Recovery Workbench Technical Specifications by Module v4.zip!Recovery Workbench TSD S9 Partner management v2.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench S9 Partner management

Technical specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD S9 Partner management |
| Document ID | S9-RWB-TSD-v2 |
| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD S9 Partner management | FSD | Pair |
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

S9 Partner management is part of the recovery module in the ACE service: one service, one repository, one front end. It covers: panel, allocation, fees, scorecards, conduct. It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| PartnerManagementController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| PartnerManagementService | Business logic; calls the rules component; writes the decision log entry before any change |
| PartnerManagementRepository | Reads and writes the module's tables only |
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

**partner** (NEW). An outside firm the bank places work with.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-PRT-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-PRT-002 | partner_code | TEXT | varchar(20) | Yes | None | Workbench |
| DF-PRT-003 | partner_name | TEXT | varchar(160) | Yes | None | Workbench |
| DF-PRT-004 | partner_type | LOV | varchar(15) | Yes | LOV-PARTNER-TYPE | Workbench |
| DF-PRT-005 | panel_status | LOV | varchar(12) | Yes | LOV-PANEL | Workbench |
| DF-PRT-006 | contract_end | DATE | date | No | None | Workbench |
| DF-PRT-007 | score | NUMBER | numeric(5,2) | No | None | Workbench |

**partner_instruction** (NEW). Work placed with a partner on a case.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-PRT-008 | id | TEXT | uuid | Yes | None | Workbench |
| DF-PRT-009 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-PRT-010 | partner_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-PRT-011 | instruction_type | LOV | varchar(20) | Yes | LOV-INSTRUCTION | Workbench |
| DF-PRT-012 | instructed_at | DATE | timestamptz | Yes | None | Workbench |
| DF-PRT-013 | due_at | DATE | timestamptz | No | None | Workbench |
| DF-PRT-014 | status | LOV | varchar(12) | Yes | LOV-INSTR-STATUS | Workbench |
| DF-PRT-015 | result_code | TEXT | varchar(40) | No | None | Workbench |
| DF-PRT-016 | fee_amount | NUMBER | numeric(18,2) | No | None | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-INSTR-STATUS | SENT, ACCEPTED, DECLINED, IN_PROGRESS, DONE, RECALLED |
| LOV-INSTRUCTION | COLLECT, FILE_SUIT, ENFORCE, APPRAISE, REPOSSESS, LIST, SELL |
| LOV-PANEL | ACTIVE, ON_NOTICE, SUSPENDED, EXITED |
| LOV-PARTNER-TYPE | AGENCY, LAW_FIRM, VALUER, AUCTION_VENDOR, BROKER, DEBT_BUYER, AMC, RAMC |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| partner_instruction | case_id | recovery_case | Many to 1 |
| partner_instruction | partner_id | partner | Many to 1 |

## T4. State machines and workflow

No case state machine of its own; the module acts on events from P3 and writes through the decision log.

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-24 | Partner portal | Both | Workbench screens through the external gateway | As entered |

### T5.2 Cross-module interfaces

Calls go through the published Java interfaces: P3 for the case, P7 for the decision log, P4 for access and reference data, P5 for documents, P6 for notices.

### T5.3 Events

| Event | Direction |
|---|---|
| InstructionIssued | Published |
| PartnerResultSubmitted | Published |

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Partner portal |
|---|---|
| RW-CASEOWN Case owner | R |
| RW-TEAMMGR Team manager | R |
| RW-LITOFF Litigation officer | CRU |
| RW-ENFORCE Enforcement owner | CRU |
| RW-LEGAL Legal counsel | R |
| RW-SALEOFF Sale officer | CRU |
| RW-NPAMGR NPA and asset manager | CRU |
| RW-DEBTSALE Debt sale officer | CRU |
| RW-GUARANT Guarantee officer | CRU |
| RW-AGENCYMG Partner and agency manager | CRUDA |
| RW-CONDUCT Conduct and QA officer | R |
| RW-CAPACITY Capacity and workforce planner | R |
| RW-PRODHEAD Product head (Mortgage, HP, SSME) | R |
| RW-HEADLIT Head of Litigation | RA |
| RW-HEADNPA Head of NPA | RA |
| RW-HEADASL Head of Asset Liquidity | RA |
| RW-RISK Risk and model risk officer | R |
| RW-COE Center of excellence analyst | R |
| RW-AUDIT Internal audit | R |
| RW-COMPLY Compliance and PDPA officer | R |
| RW-PLATADM Platform administrator | R |
| RW-BIANAL Reporting and BI analyst | R |
| RW-TRIBE Tribe lead and squad members | R |
| PT-AGENCY Collection agency (OA) user | RU |
| PT-LAWFIRM Law firm user | RU |
| PT-VALUER Valuer | RU |
| PT-AUCTION Auction vendor | RU |
| PT-BUYER Debt buyer and AMC | RU |
| PT-RAMC RAMC user | RU |

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
| REQ-S9-001 | FEAT-PRM-01 | Written one epic ahead | With the story |
| REQ-S9-002 | FEAT-PRM-01 | Written one epic ahead | With the story |
| REQ-S9-003 | FEAT-PRM-01 | Written one epic ahead | With the story |
| REQ-S9-004 | FEAT-PRM-01 | Written one epic ahead | With the story |
| REQ-S9-005 | FEAT-PRM-08 | Written one epic ahead | With the story |
| REQ-S9-006 | FEAT-PRM-08 | Written one epic ahead | With the story |
| REQ-S9-007 | FEAT-PRM-08 | Written one epic ahead | With the story |
| REQ-S9-008 | FEAT-PRM-01 | Written one epic ahead | With the story |
| REQ-S9-009 | FEAT-PRM-08 | Written one epic ahead | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-S9-001 | GET | /api/recovery/v1/partners | Partner portal R | E2 |
| API-S9-002 | POST | /api/recovery/v1/cases/{caseId}/instructions | Partner portal C | E4 |
| API-S9-003 | GET | /api/recovery/v1/partner/instructions | Partner portal R | E4 |
| API-S9-004 | POST | /api/recovery/v1/partner/instructions/{instructionId}/accept | Partner portal U | E4 |
| API-S9-005 | POST | /api/recovery/v1/partner/instructions/{instructionId}/results | Partner portal U | E4 |
| API-S9-006 | POST | /api/recovery/v1/partner/instructions/{instructionId}/invoices | Partner portal C | E6 |

### T-A.2 Endpoint detail

#### API-S9-001 GET /partners

| Item | Value |
|---|---|
| Purpose | List partners with panel status and score |
| Request | Query: type, status |
| Response | Partner[] |
| Errors | 401, 403, 503 |
| Authorization | Partner portal, right R, scope applied |
| Idempotency | Not applicable |

#### API-S9-002 POST /cases/{caseId}/instructions

| Item | Value |
|---|---|
| Purpose | Issue an instruction to a partner by rule |
| Request | InstructionRequest |
| Response | PartnerInstruction |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Partner portal, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S9-003 GET /partner/instructions

| Item | Value |
|---|---|
| Purpose | List the instructions placed with the caller's firm |
| Request | Query: status, page, size |
| Response | InstructionPage |
| Errors | 401, 403, 503 |
| Authorization | Partner portal, right R, scope applied |
| Idempotency | Not applicable |

#### API-S9-004 POST /partner/instructions/{instructionId}/accept

| Item | Value |
|---|---|
| Purpose | Accept or decline an instruction |
| Request | InstructionAcceptance |
| Response | PartnerInstruction |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Partner portal, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S9-005 POST /partner/instructions/{instructionId}/results

| Item | Value |
|---|---|
| Purpose | Record a result with its documents |
| Request | Multipart: result, files |
| Response | PartnerInstruction |
| Errors | 401, 403, 404, 409, 415, 422, 503 |
| Authorization | Partner portal, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-S9-006 POST /partner/instructions/{instructionId}/invoices

| Item | Value |
|---|---|
| Purpose | Submit a fee invoice |
| Request | InvoiceRequest |
| Response | Invoice |
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

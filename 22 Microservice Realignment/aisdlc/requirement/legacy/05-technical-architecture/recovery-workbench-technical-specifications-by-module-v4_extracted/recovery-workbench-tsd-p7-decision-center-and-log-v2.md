<!-- source: 05 Technical architecture/Recovery Workbench Technical Specifications by Module v4.zip!Recovery Workbench TSD P7 Decision center and log v2.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `05 Technical architecture/Recovery Workbench Technical Specifications by Module v4.zip!Recovery Workbench TSD P7 Decision center and log v2.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench P7 Decision center and log

Technical specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD P7 Decision center and log |
| Document ID | P7-RWB-TSD-v2 |
| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD P7 Decision center and log | FSD | Pair |
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

P7 Decision center and log is part of the recovery module in the ACE service: one service, one repository, one front end. It covers: recommendation with reasons, approval within delegation, decision log store and writer. It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| DecisionCenterAndLogController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| DecisionCenterAndLogService | Business logic; calls the rules component; writes the decision log entry before any change |
| DecisionCenterAndLogRepository | Reads and writes the module's tables only |
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

### T5.2 Cross-module interfaces

Calls go through the published Java interfaces: P3 for the case, P7 for the decision log, P4 for access and reference data, P5 for documents, P6 for notices.

### T5.3 Events

| Event | Direction |
|---|---|
| DecisionRecorded | Published |
| ApprovalRequested | Published |

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
| API-P7-001 | GET | /api/recovery/v1/cases/{caseId}/recommendation | Decision log R | E4 |
| API-P7-002 | GET | /api/recovery/v1/approvals | Decision log A | E2 |
| API-P7-003 | POST | /api/recovery/v1/approvals/{approvalId}/approve | Decision log A | E2 |
| API-P7-004 | POST | /api/recovery/v1/approvals/{approvalId}/return | Decision log A | E2 |
| API-P7-005 | POST | /api/recovery/v1/approvals/{approvalId}/refuse | Decision log A | E2 |
| API-P7-006 | GET | /api/recovery/v1/decision-log | Decision log R | E1 |
| API-P7-007 | GET | /api/recovery/v1/decision-log/{entryId} | Decision log R | E1 |
| API-P7-008 | GET | /api/recovery/v1/approvals/{approvalId} | Decision log A | E2 |

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

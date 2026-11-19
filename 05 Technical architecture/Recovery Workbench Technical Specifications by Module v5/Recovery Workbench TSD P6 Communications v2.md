# Recovery Workbench P6 Communications

Technical specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD P6 Communications |
| Document ID | P6-RWB-TSD-v2 |
| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD P6 Communications | FSD | Pair |
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

P6 Communications is part of the recovery module in the ACE service: one service, one repository, one front end. It covers: letters, notices, SMS, LINE, proof of delivery. It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| CommunicationsController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| CommunicationsService | Business logic; calls the rules component; writes the decision log entry before any change |
| CommunicationsRepository | Reads and writes the module's tables only |
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

**notice** (NEW). A demand, recall or statutory notice and its proof of delivery.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-LEG-015 | id | TEXT | uuid | Yes | None | Workbench |
| DF-LEG-016 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-LEG-017 | document_id | CROSS_REF | uuid | No | None | Workbench |
| DF-LEG-018 | notice_type | LOV | varchar(25) | Yes | LOV-NOTICE | Workbench |
| DF-LEG-019 | sent_date | DATE | date | No | None | WIN |
| DF-LEG-020 | barcode | TEXT | varchar(40) | No | None | WIN |
| DF-LEG-021 | callback_date | DATE | date | No | None | WIN |
| DF-LEG-022 | delivery_status | LOV | varchar(15) | No | LOV-DELIVERY | WIN |
| DF-LEG-023 | sent_type | LOV | varchar(10) | No | LOV-SENT-TYPE | WIN |
| DF-LEG-030 | party_id | CROSS_REF | uuid | No | None | Workbench |
| DF-LEG-031 | template_id | CROSS_REF | uuid | No | None | Workbench |
| DF-LEG-032 | hold_reason | TEXT | varchar(30) | No | None | Workbench |
| DF-LEG-033 | dispatch_file_id | CROSS_REF | uuid | No | None | Workbench |
| DF-LEG-034 | dispatch_attempts | NUMBER | integer | Yes | None | Workbench |

**template** (NEW). A letter or notice template.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-045 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-046 | template_code | TEXT | varchar(30) | Yes | None | Workbench |
| DF-REF-047 | template_version | NUMBER | integer | Yes | None | Workbench |
| DF-REF-048 | language | LOV | varchar(2) | Yes | LOV-LANG | Workbench |
| DF-REF-049 | product_group | LOV | varchar(15) | No | LOV-PRODUCT | Workbench |
| DF-REF-050 | body_ref | ATTACHMENT | varchar(400) | Yes | None | Workbench |
| DF-REF-051 | approved_by_legal | BOOLEAN | boolean | Yes | None | Workbench |
| DF-REF-063 | approved_by | USER_REF | uuid | No | None | Workbench |
| DF-REF-064 | approved_at | DATE | timestamptz | No | None | Workbench |
| DF-REF-065 | valid_from | DATE | date | No | None | Workbench |
| DF-REF-066 | channel | LOV | varchar(15) | No | LOV-CHANNEL | Workbench |
| DF-REF-067 | notice_type | LOV | varchar(25) | No | LOV-NOTICE | Workbench |
| DF-REF-068 | signature_basis | LOV | varchar(20) | No | LOV-SIGNATURE-BASIS | Workbench |
| DF-REF-069 | merge_codes | TEXT | jsonb | No | None | Workbench |

**merge_field** (NEW). A merge code a template may use and the field that supplies its value, by catalog version.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-252 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-253 | merge_code | TEXT | varchar(40) | Yes | None | Workbench |
| DF-REF-254 | source_entity | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-255 | source_field | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-256 | field_id | TEXT | varchar(16) | Yes | None | Workbench |
| DF-REF-257 | is_required | BOOLEAN | boolean | Yes | None | Workbench |
| DF-REF-258 | personal_data | BOOLEAN | boolean | Yes | None | Workbench |
| DF-REF-259 | catalog_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-260 | valid_from | DATE | date | Yes | None | Workbench |

**signature_request** (NEW). A request for a party to sign a generated document, and its result.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-DOC-096 | id | TEXT | uuid | Yes | None | Workbench |
| DF-DOC-097 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-DOC-098 | treatment_id | CROSS_REF | uuid | No | None | Workbench |
| DF-DOC-099 | document_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-DOC-100 | party_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-DOC-101 | method | LOV | varchar(15) | Yes | LOV-SIGN-METHOD | Workbench |
| DF-DOC-102 | status | LOV | varchar(15) | Yes | LOV-SIGN-STATUS | Workbench |
| DF-DOC-103 | external_ref | TEXT | varchar(60) | No | None | EasyApp |
| DF-DOC-104 | sent_at | DATE | timestamptz | No | None | Workbench |
| DF-DOC-105 | signed_at | DATE | timestamptz | No | None | Workbench |
| DF-DOC-106 | signed_document_id | CROSS_REF | uuid | No | None | Workbench |
| DF-DOC-107 | expires_at | DATE | timestamptz | No | None | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-CHANNEL | MOBILE, HOME_PHONE, WORK_PHONE, LINE, EMAIL, POSTAL_ADDRESS, CALL, VISIT, SMS, LETTER, PORTAL, BRANCH |
| LOV-DELIVERY | DELIVERED, REFUSED, UNDELIVERABLE, PENDING |
| LOV-LANG | TH, EN |
| LOV-NOTICE | DEMAND, RECALL, STATUTORY_SALE_NOTICE, GUARANTOR_NOTICE |
| LOV-PRODUCT | MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED |
| LOV-SENT-TYPE | BEFORE_NPL, NPL |
| LOV-SIGN-METHOD | E_SIGNATURE, BRANCH, PAPER |
| LOV-SIGN-STATUS | QUEUED, SENT, SIGNED, DECLINED, EXPIRED |
| LOV-SIGNATURE-BASIS | E_SIGNATURE_ALLOWED, WET_INK_REQUIRED |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| notice | case_id | recovery_case | Many to 1 |
| notice | document_id | document | Many to 0 or 1 |
| notice | party_id | party | Many to 0 or 1 |
| notice | template_id | template | Many to 0 or 1 |
| notice | dispatch_file_id | outbound_item | Many to 0 or 1 |
| signature_request | case_id | recovery_case | Many to 1 |
| signature_request | treatment_id | treatment | Many to 0 or 1 |
| signature_request | document_id | document | Many to 1 |
| signature_request | party_id | party | Many to 1 |
| signature_request | signed_document_id | document | Many to 0 or 1 |

## T4. State machines and workflow

No case state machine of its own; the module acts on events from P3 and writes through the decision log.

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-14 | WIN | Out | File | Daily |
| INT-17 | NSS | Out | ACE notification path | As sent |
| INT-18 | LINE OA | Out | ACE notification path | As sent |

### T5.2 Cross-module interfaces

Calls go through the published Java interfaces: P3 for the case, P7 for the decision log, P4 for access and reference data, P5 for documents, P6 for notices.

### T5.3 Events

| Event | Direction |
|---|---|
| NoticeGenerated | Published |
| NoticeDispatched | Published |
| NoticeDelivered | Published |

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Documents | Litigation |
|---|---|---|
| RW-CASEOWN Case owner | CRU | R |
| RW-TEAMMGR Team manager | R | R |
| RW-PHONECOL Phone collector | R | - |
| RW-FIELDCOL Field collector | CR | - |
| RW-RESTRUCT Restructuring officer (FCR) | CRU | - |
| RW-SPECIAL Hardship and vulnerability specialist | CRU | - |
| RW-COMPLAIN Complaint officer | CRU | R |
| RW-FRAUD Fraud investigator | CRU | R |
| RW-LITOFF Litigation officer | CRU | CRUA |
| RW-ENFORCE Enforcement owner | CRU | CRU |
| RW-LEGAL Legal counsel | CRUA | RA |
| RW-SALEOFF Sale officer | CRU | R |
| RW-NPAMGR NPA and asset manager | CRU | R |
| RW-DEBTSALE Debt sale officer | CRU | R |
| RW-WRITEOFF Write-off team member | CRU | R |
| RW-CREDITAD Credit Administration officer | CRU | R |
| RW-GUARANT Guarantee officer | CRU | R |
| RW-AGENCYMG Partner and agency manager | R | R |
| RW-CONDUCT Conduct and QA officer | R | R |
| RW-PRODHEAD Product head (Mortgage, HP, SSME) | R | RA |
| RW-HEADLIT Head of Litigation | R | RA |
| RW-HEADNPA Head of NPA | R | R |
| RW-HEADASL Head of Asset Liquidity | R | R |
| RW-CREDCOMM Credit approval committee member | R | - |
| RW-WOCOMM Write-off committee member | R | - |
| RW-RISK Risk and model risk officer | R | R |
| RW-COE Center of excellence analyst | R | R |
| RW-DATASTEW Data steward and data product owner | R | - |
| RW-AUDIT Internal audit | R | R |
| RW-COMPLY Compliance and PDPA officer | RU | R |
| RW-PLATADM Platform administrator | R | - |
| RW-BIANAL Reporting and BI analyst | - | R |
| RW-TRIBE Tribe lead and squad members | R | R |
| PT-AGENCY Collection agency (OA) user | CR | - |
| PT-LAWFIRM Law firm user | CRU | RU |
| PT-VALUER Valuer | CR | - |
| PT-AUCTION Auction vendor | CR | - |
| PT-BUYER Debt buyer and AMC | R | - |
| PT-RAMC RAMC user | R | - |
| SY-CASEWF Case workflow module | R | R |
| SY-RULES Rules component | R | R |
| SY-DATALOAD Data load from COLLINS | - | U |
| SY-OCR OCR and extraction pipeline | CRU | - |
| SY-AGENT Agent platform | R | R |

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
| REQ-OCC-001 | None | Written one epic ahead | With the story |
| REQ-OCC-002 | None | Written one epic ahead | With the story |
| REQ-OCC-003 | FEAT-OCC-01 | RWB-E2-021 | TC-E2-021-01 |
| REQ-OCC-004 | FEAT-OCC-01 | RWB-E2-021 | TC-E2-021-01 |
| REQ-OCC-005 | FEAT-OCC-01 | RWB-E2-021 | TC-E2-021-01 |
| REQ-OCC-006 | FEAT-OCC-01 | RWB-E2-021 | TC-E2-021-01 |
| REQ-OCC-007 | None | Written one epic ahead | With the story |
| REQ-OCC-008 | FEAT-OCC-01 | RWB-E2-021 | TC-E2-021-01 |
| REQ-OCC-009 | FEAT-OCC-01 | RWB-E2-021 | TC-E2-021-01 |
| REQ-OCC-010 | FEAT-OCC-01 | RWB-E2-021 | TC-E2-021-01 |
| REQ-OCC-011 | FEAT-COM-01 | Written one epic ahead | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-P6-001 | POST | /api/recovery/v1/cases/{caseId}/notices | Litigation C | E2 |
| API-P6-002 | GET | /api/recovery/v1/notices/{noticeId} | Litigation R | E2 |
| API-P6-003 | GET | /api/recovery/v1/admin/templates | Documents R | E1 |
| API-P6-004 | POST | /api/recovery/v1/admin/templates | Documents C | E1 |
| API-P6-005 | GET | /api/recovery/v1/admin/templates/{templateId}/content | Documents R | E1 |
| API-P6-006 | POST | /api/recovery/v1/admin/templates/{templateId}/approve | Documents A | E1 |
| API-P6-007 | POST | /api/recovery/v1/admin/templates/{templateId}/withdraw | Documents A | E1 |
| API-P6-008 | POST | /api/recovery/v1/cases/{caseId}/messages | Case record C | E2 |
| API-P6-009 | POST | /api/recovery/v1/treatments/{treatmentId}/signature-requests | Treatment and offer C | E2 |
| API-P6-010 | GET | /api/recovery/v1/treatments/{treatmentId}/signature-requests | Treatment and offer R | E2 |
| API-P6-011 | POST | /api/recovery/v1/signature-requests/{requestId}/result | Treatment and offer U | E2 |

### T-A.2 Endpoint detail

#### API-P6-001 POST /cases/{caseId}/notices

| Item | Value |
|---|---|
| Purpose | Generate a notice from the approved template |
| Request | NoticeRequest |
| Response | Notice |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Litigation, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P6-002 GET /notices/{noticeId}

| Item | Value |
|---|---|
| Purpose | Read a notice with its dispatch and proof of delivery |
| Request | None |
| Response | Notice |
| Errors | 401, 403, 404, 503 |
| Authorization | Litigation, right R, scope applied |
| Idempotency | Not applicable |

#### API-P6-003 GET /admin/templates

| Item | Value |
|---|---|
| Purpose | List template versions by code, language and state |
| Request | Query: code, language, state, page, size |
| Response | TemplatePage |
| Errors | 401, 403, 503 |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |

#### API-P6-004 POST /admin/templates

| Item | Value |
|---|---|
| Purpose | Upload a new template version in state DRAFT |
| Request | Multipart: file, templateCode, language, productGroup, channel, noticeType, signatureBasis, mergeCodes |
| Response | Template |
| Errors | 401, 403, 413, 415, 422, 503 |
| Authorization | Documents, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P6-005 GET /admin/templates/{templateId}/content

| Item | Value |
|---|---|
| Purpose | Download a template body |
| Request | None |
| Response | Binary |
| Errors | 401, 403, 404, 503 |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |

#### API-P6-006 POST /admin/templates/{templateId}/approve

| Item | Value |
|---|---|
| Purpose | Record the Legal approval of a draft template version with its valid from date |
| Request | TemplateApproval |
| Response | Template |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Documents, right A, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P6-007 POST /admin/templates/{templateId}/withdraw

| Item | Value |
|---|---|
| Purpose | Withdraw an approved template version with a reason |
| Request | TemplateWithdrawal |
| Response | Template |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Documents, right A, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P6-008 POST /cases/{caseId}/messages

| Item | Value |
|---|---|
| Purpose | Send an SMS or LINE message from an approved template after the conduct check |
| Request | MessageRequest |
| Response | Interaction |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Case record, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P6-009 POST /treatments/{treatmentId}/signature-requests

| Item | Value |
|---|---|
| Purpose | Send reviewed generated documents for signature by e-signature, branch or paper; copies them to the write-once store and writes the decision log entry |
| Request | SignatureRequestCreate |
| Response | SignatureRequest[] |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Treatment and offer, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P6-010 GET /treatments/{treatmentId}/signature-requests

| Item | Value |
|---|---|
| Purpose | List the signature requests of a treatment |
| Request | None |
| Response | SignatureRequest[] |
| Errors | 401, 403, 404, 503 |
| Authorization | Treatment and offer, right R, scope applied |
| Idempotency | Not applicable |

#### API-P6-011 POST /signature-requests/{requestId}/result

| Item | Value |
|---|---|
| Purpose | Record a branch or paper signature result with the scanned document |
| Request | SignatureResultRequest |
| Response | SignatureRequest |
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

<!-- source: 05 Technical architecture/Recovery Workbench Technical Specifications by Module v3.zip!Recovery Workbench TSD P5 Document hub v2.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `05 Technical architecture/Recovery Workbench Technical Specifications by Module v3.zip!Recovery Workbench TSD P5 Document hub v2.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench P5 Document hub

Technical specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD P5 Document hub |
| Document ID | P5-RWB-TSD-v2 |
| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD P5 Document hub | FSD | Pair |
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

P5 Document hub is part of the recovery module in the ACE service: one service, one repository, one front end. It covers: store, index, OCR, classification, extraction, review queue, retention, custody. It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| DocumentHubController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| DocumentHubService | Business logic; calls the rules component; writes the decision log entry before any change |
| DocumentHubRepository | Reads and writes the module's tables only |
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

**document** (EXTEND ACE Attachment). A document held against a case.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-DOC-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-DOC-002 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-DOC-003 | party_id | CROSS_REF | uuid | No | None | Workbench |
| DF-DOC-004 | document_type | LOV | varchar(30) | Yes | LOV-DOC-TYPE | Workbench |
| DF-DOC-005 | source | LOV | varchar(12) | Yes | LOV-DOC-SOURCE | Workbench |
| DF-DOC-006 | storage_ref | ATTACHMENT | varchar(400) | Yes | None | Workbench |
| DF-DOC-007 | classification_confidence | NUMBER | numeric(5,4) | No | None | Workbench |
| DF-DOC-008 | review_status | LOV | varchar(12) | Yes | LOV-REVIEW | Workbench |
| DF-DOC-009 | retention_class | LOV | varchar(10) | Yes | LOV-RETENTION | Workbench |
| DF-DOC-010 | write_once | BOOLEAN | boolean | Yes | None | Workbench |
| DF-DOC-011 | doc_version | NUMBER | integer | Yes | None | Workbench |
| DF-DOC-025 | previous_version_id | CROSS_REF | uuid | No | None | Workbench |
| DF-DOC-026 | content_sha256 | TEXT | char(64) | Yes | None | Workbench |
| DF-DOC-027 | captured_at | DATE | timestamptz | No | None | Workbench |
| DF-DOC-028 | capture_latitude | NUMBER | numeric(9,6) | No | None | Workbench |
| DF-DOC-029 | capture_longitude | NUMBER | numeric(9,6) | No | None | Workbench |
| DF-DOC-030 | client_file_id | TEXT | varchar(64) | No | None | Workbench |
| DF-DOC-031 | capture_kind | LOV | varchar(12) | No | LOV-CAPTURE-KIND | Workbench |
| DF-DOC-032 | template_id | CROSS_REF | uuid | No | None | Workbench |
| DF-DOC-033 | treatment_id | CROSS_REF | uuid | No | None | Workbench |

**document_field** (NEW). A field read from a document.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-DOC-012 | id | TEXT | uuid | Yes | None | Workbench |
| DF-DOC-013 | document_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-DOC-014 | field_name | TEXT | varchar(60) | Yes | None | Workbench |
| DF-DOC-015 | field_value | TEXT | varchar(1000) | No | None | Workbench |
| DF-DOC-016 | confidence | NUMBER | numeric(5,4) | No | None | Workbench |
| DF-DOC-017 | confirmed_by | USER_REF | uuid | No | None | Workbench |
| DF-DOC-034 | extracted_value | TEXT | varchar(1000) | No | None | Workbench |
| DF-DOC-035 | extractor_version | TEXT | varchar(40) | No | None | Workbench |

**document_custody** (NEW). Each movement of an original document.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-DOC-018 | id | TEXT | uuid | Yes | None | Workbench |
| DF-DOC-019 | document_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-DOC-020 | moved_at | DATE | timestamptz | Yes | None | Workbench |
| DF-DOC-021 | from_location | LOV | varchar(20) | Yes | LOV-CUSTODY | Workbench |
| DF-DOC-022 | to_location | LOV | varchar(20) | Yes | LOV-CUSTODY | Workbench |
| DF-DOC-023 | held_by | TEXT | varchar(120) | Yes | None | Workbench |
| DF-DOC-024 | due_back | DATE | date | No | None | Workbench |

**document_type** (NEW). A document type, the fields extracted from it and its Legal and NPA sign-off, by version.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-218 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-219 | doc_type_code | TEXT | varchar(30) | Yes | None | Workbench |
| DF-REF-220 | label_en | TEXT | varchar(120) | Yes | None | Workbench |
| DF-REF-221 | label_th | TEXT | varchar(120) | No | None | Workbench |
| DF-REF-222 | write_once | BOOLEAN | boolean | Yes | None | Workbench |
| DF-REF-223 | retention_class | LOV | varchar(10) | Yes | LOV-RETENTION | Workbench |
| DF-REF-224 | field_definitions | TEXT | jsonb | Yes | None | Workbench |
| DF-REF-225 | legal_signoff_by | USER_REF | uuid | No | None | Workbench |
| DF-REF-226 | legal_signoff_date | DATE | date | No | None | Workbench |
| DF-REF-227 | npa_signoff_by | USER_REF | uuid | No | None | Workbench |
| DF-REF-228 | npa_signoff_date | DATE | date | No | None | Workbench |
| DF-REF-229 | table_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-230 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-231 | valid_to | DATE | date | No | None | Workbench |
| DF-REF-232 | reference_version_id | CROSS_REF | uuid | No | None | Workbench |
| DF-REF-233 | classify_threshold | NUMBER | numeric(4,3) | No | None | Workbench |

**document_checklist_item** (NEW). A document type required or expected for a case stage and route, by checklist version.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-234 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-235 | stage_code | LOV | varchar(20) | Yes | LOV-STAGE | Workbench |
| DF-REF-236 | route_code | LOV | varchar(4) | No | LOV-ROUTE | Workbench |
| DF-REF-237 | document_type | LOV | varchar(30) | Yes | LOV-DOC-TYPE | Workbench |
| DF-REF-238 | required | BOOLEAN | boolean | Yes | None | Workbench |
| DF-REF-239 | sort_order | NUMBER | integer | Yes | None | Workbench |
| DF-REF-240 | table_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-241 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-242 | valid_to | DATE | date | No | None | Workbench |
| DF-REF-243 | reference_version_id | CROSS_REF | uuid | No | None | Workbench |

**case_document_check** (NEW). The latest document completeness check of a case against its checklist.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-DOC-036 | id | TEXT | uuid | Yes | None | Workbench |
| DF-DOC-037 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-DOC-038 | checklist_version | TEXT | varchar(20) | No | None | Workbench |
| DF-DOC-039 | required_count | NUMBER | integer | Yes | None | Workbench |
| DF-DOC-040 | present_count | NUMBER | integer | Yes | None | Workbench |
| DF-DOC-041 | missing_types | TEXT | jsonb | No | None | Workbench |
| DF-DOC-042 | complete | BOOLEAN | boolean | No | None | Workbench |
| DF-DOC-043 | checked_at | DATE | timestamptz | Yes | None | Workbench |
| DF-DOC-044 | last_event_id | CROSS_REF | uuid | No | None | Workbench |

**document_hub_parameter** (NEW). A document hub parameter value, by version.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-244 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-245 | param_code | TEXT | varchar(40) | Yes | None | Workbench |
| DF-REF-246 | param_value | TEXT | varchar(200) | Yes | None | Workbench |
| DF-REF-247 | unit | TEXT | varchar(20) | No | None | Workbench |
| DF-REF-248 | table_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-249 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-250 | valid_to | DATE | date | No | None | Workbench |
| DF-REF-251 | reference_version_id | CROSS_REF | uuid | No | None | Workbench |

**document_intake** (NEW). A file received by the document hub, from scan to OCR, classification, extraction, matching and review.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-DOC-045 | id | TEXT | uuid | Yes | None | Workbench |
| DF-DOC-046 | source | LOV | varchar(12) | Yes | LOV-DOC-SOURCE | Workbench |
| DF-DOC-047 | source_ref | TEXT | varchar(400) | Yes | None | Workbench |
| DF-DOC-048 | channel_code | TEXT | varchar(40) | No | None | Workbench |
| DF-DOC-049 | file_name | TEXT | varchar(255) | No | None | Workbench |
| DF-DOC-050 | file_size | NUMBER | bigint | No | None | Workbench |
| DF-DOC-051 | captured_at | DATE | timestamptz | No | None | Workbench |
| DF-DOC-052 | sender_address | TEXT | varchar(320) | No | None | Workbench |
| DF-DOC-053 | partner_id | CROSS_REF | uuid | No | None | Workbench |
| DF-DOC-054 | run_id | CROSS_REF | uuid | No | None | Workbench |
| DF-DOC-055 | received_at | DATE | timestamptz | Yes | None | Workbench |
| DF-DOC-056 | file_sha256 | TEXT | char(64) | Yes | None | Workbench |
| DF-DOC-057 | intake_ref | ATTACHMENT | varchar(400) | Yes | None | Workbench |
| DF-DOC-058 | scan_result | LOV | varchar(10) | No | LOV-SCAN-RESULT | Workbench |
| DF-DOC-059 | scanned_at | DATE | timestamptz | No | None | Workbench |
| DF-DOC-060 | case_id | CROSS_REF | uuid | No | None | Workbench |
| DF-DOC-061 | document_id | CROSS_REF | uuid | No | None | Workbench |
| DF-DOC-062 | ocr_ref | ATTACHMENT | varchar(400) | No | None | Workbench |
| DF-DOC-063 | ocr_status | LOV | varchar(12) | Yes | LOV-OCR-STATUS | Workbench |
| DF-DOC-064 | ocr_attempts | NUMBER | integer | Yes | None | Workbench |
| DF-DOC-065 | page_count | NUMBER | integer | No | None | Workbench |
| DF-DOC-066 | rescan_pages | TEXT | varchar(200) | No | None | Workbench |
| DF-DOC-067 | ocr_quality | NUMBER | numeric(5,4) | No | None | Workbench |
| DF-DOC-068 | languages | TEXT | varchar(20) | No | None | Workbench |
| DF-DOC-069 | ocr_engine_version | TEXT | varchar(40) | No | None | Workbench |
| DF-DOC-070 | predicted_type | LOV | varchar(30) | No | LOV-DOC-TYPE | Workbench |
| DF-DOC-071 | classification_confidence | NUMBER | numeric(5,4) | No | None | Workbench |
| DF-DOC-072 | type_candidates | TEXT | jsonb | No | None | Workbench |
| DF-DOC-073 | classifier_version | TEXT | varchar(40) | No | None | Workbench |
| DF-DOC-074 | classify_fallback | BOOLEAN | boolean | Yes | None | Workbench |
| DF-DOC-075 | match_status | LOV | varchar(12) | Yes | LOV-INTAKE-MATCH | Workbench |
| DF-DOC-076 | candidate_case_ids | TEXT | jsonb | No | None | Workbench |
| DF-DOC-077 | extracted_fields | TEXT | jsonb | No | None | Workbench |
| DF-DOC-078 | extract_status | LOV | varchar(12) | No | LOV-EXTRACT-STATUS | Workbench |
| DF-DOC-079 | extract_attempts | NUMBER | integer | Yes | None | Workbench |
| DF-DOC-080 | review_reason | LOV | varchar(20) | No | LOV-INTAKE-REVIEW | Workbench |
| DF-DOC-081 | review_outcome | LOV | varchar(12) | No | LOV-INTAKE-OUTCOME | Workbench |
| DF-DOC-082 | resolved_by | USER_REF | uuid | No | None | Workbench |
| DF-DOC-083 | resolved_at | DATE | timestamptz | No | None | Workbench |
| DF-DOC-084 | discard_reason | TEXT | varchar(400) | No | None | Workbench |

**document_text** (NEW). The OCR text of one page of an intake item.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-DOC-085 | id | TEXT | uuid | Yes | None | Workbench |
| DF-DOC-086 | intake_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-DOC-087 | document_id | CROSS_REF | uuid | No | None | Workbench |
| DF-DOC-088 | page_no | NUMBER | integer | Yes | None | Workbench |
| DF-DOC-089 | text_content | TEXT | text | Yes | None | Workbench |
| DF-DOC-090 | quality | NUMBER | numeric(5,4) | No | None | Workbench |

**retention_action** (NEW). What the monthly retention job did with one document.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-DOC-091 | id | TEXT | uuid | Yes | None | Workbench |
| DF-DOC-092 | document_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-DOC-093 | run_month | TEXT | char(7) | Yes | None | Workbench |
| DF-DOC-094 | action | LOV | varchar(12) | Yes | LOV-RETENTION-ACTION | Workbench |
| DF-DOC-095 | decision_log_id | CROSS_REF | uuid | No | None | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-CAPTURE-KIND | PHOTO, BILL, CHECKLIST |
| LOV-CUSTODY | VAULT, BRANCH, POST, LAWYER, COURT, LAND_OFFICE |
| LOV-DOC-SOURCE | SCAN, UPLOAD, GENERATED, PARTNER, EMAIL |
| LOV-EXTRACT-STATUS | PENDING, DONE, FAILED |
| LOV-INTAKE-MATCH | PENDING, MATCHED, NO_MATCH, MULTIPLE, CONFLICT, CASE_CLOSED, NO_TYPE |
| LOV-INTAKE-OUTCOME | ATTACHED, DISCARDED |
| LOV-INTAKE-REVIEW | RESCAN, UNREADABLE_FILE, LOW_CONFIDENCE, MODEL_UNAVAILABLE, UNKNOWN_TYPE |
| LOV-OCR-STATUS | PENDING, DONE, RESCAN, FAILED |
| LOV-RETENTION-ACTION | ARCHIVED, LISTED, HELD, EXCEPTION |
| LOV-REVIEW | NOT_NEEDED, PENDING, CONFIRMED, CORRECTED |
| LOV-ROUTE | R1, R2, R3, R4, R5, R6, R7, R8 |
| LOV-SCAN-RESULT | CLEAN, INFECTED |
| LOV-STAGE | RESTRUCTURE, SETTLEMENT, DEED_IN_LIEU, GUARANTEE_CLAIM, LITIGATION, ASSET_DISPOSAL, DEBT_SALE, WRITE_OFF, DEVIATIONS |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| document | case_id | recovery_case | Many to 1 |
| document | party_id | party | Many to 0 or 1 |
| document | previous_version_id | document | Many to 0 or 1 |
| document | template_id | template | Many to 0 or 1 |
| document | treatment_id | treatment | Many to 0 or 1 |
| document_field | document_id | document | Many to 1 |
| document_custody | document_id | document | Many to 1 |
| document_type | reference_version_id | reference_version | Many to 0 or 1 |
| document_checklist_item | reference_version_id | reference_version | Many to 0 or 1 |
| case_document_check | case_id | recovery_case | Many to 1 |
| case_document_check | last_event_id | outbox_event | Many to 0 or 1 |
| document_hub_parameter | reference_version_id | reference_version | Many to 0 or 1 |
| document_intake | partner_id | partner | Many to 0 or 1 |
| document_intake | run_id | load_run | Many to 0 or 1 |
| document_intake | case_id | recovery_case | Many to 0 or 1 |
| document_intake | document_id | document | Many to 0 or 1 |
| document_text | intake_id | document_intake | Many to 1 |
| document_text | document_id | document | Many to 0 or 1 |
| retention_action | document_id | document | Many to 1 |
| retention_action | decision_log_id | decision_log_entry | Many to 0 or 1 |

## T4. State machines and workflow

No case state machine of its own; the module acts on events from P3 and writes through the decision log.

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| None | | | | |

### T5.2 Cross-module interfaces

Calls go through the published Java interfaces: P3 for the case, P7 for the decision log, P4 for access and reference data, P5 for documents, P6 for notices.

### T5.3 Events

| Event | Direction |
|---|---|
| DocumentStored | Published |
| DocumentFieldsExtracted | Published |

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Documents |
|---|---|
| RW-CASEOWN Case owner | CRU |
| RW-TEAMMGR Team manager | R |
| RW-PHONECOL Phone collector | R |
| RW-FIELDCOL Field collector | CR |
| RW-RESTRUCT Restructuring officer (FCR) | CRU |
| RW-SPECIAL Hardship and vulnerability specialist | CRU |
| RW-COMPLAIN Complaint officer | CRU |
| RW-FRAUD Fraud investigator | CRU |
| RW-LITOFF Litigation officer | CRU |
| RW-ENFORCE Enforcement owner | CRU |
| RW-LEGAL Legal counsel | CRUA |
| RW-SALEOFF Sale officer | CRU |
| RW-NPAMGR NPA and asset manager | CRU |
| RW-DEBTSALE Debt sale officer | CRU |
| RW-WRITEOFF Write-off team member | CRU |
| RW-CREDITAD Credit Administration officer | CRU |
| RW-GUARANT Guarantee officer | CRU |
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
| RW-AUDIT Internal audit | R |
| RW-COMPLY Compliance and PDPA officer | RU |
| RW-PLATADM Platform administrator | R |
| RW-TRIBE Tribe lead and squad members | R |
| PT-AGENCY Collection agency (OA) user | CR |
| PT-LAWFIRM Law firm user | CRU |
| PT-VALUER Valuer | CR |
| PT-AUCTION Auction vendor | CR |
| PT-BUYER Debt buyer and AMC | R |
| PT-RAMC RAMC user | R |
| SY-CASEWF Case workflow module | R |
| SY-RULES Rules component | R |
| SY-OCR OCR and extraction pipeline | CRU |
| SY-AGENT Agent platform | R |

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
| NFR-028 | Every document type carries a retention class, and the class sets how long the document is kept. | Retention classes defined per type; periods not set | Open, DL26 |
| NFR-029 | Legal documents are held in a write-once container and cannot be altered or deleted inside their retention period. | Write-once for legal types | Proposed |
| NFR-030 | The decision log is retained for the period the regulator and internal audit require. | Log retention is set by Compliance | Open, DL26 |
| NFR-031 | Case records carry a retention and archive rule by record class, and a case closes after its retention period. | Not set | Open, DL26 |
| NFR-032 | A retired local file is kept as a read-only archive at a recorded location. | Archive location recorded per file | Proposed |
| NFR-072 | A legal hold stops deletion and expiry for the case or document it covers, for as long as it is in place, overriding the retention class. | Hold overrides retention | Proposed |
| NFR-073 | An electronic discovery request is answered with every document for a named population, its metadata, its version history and the date each version was created. | Not set as a response time | Open, DL26 |
| NFR-074 | A document reaching the end of its retention period is disposed of or extended by a recorded decision, and is never removed silently. | Recorded decision on every disposal | Proposed |
| NFR-075 | Interaction ledger entries carry their own retention period, set independently of the decision log. | Not set | Open, DL26 |

## T8. Requirement traceability

| Requirement | Feature | Story | Test |
|---|---|---|---|
| REQ-DCM-001 | FEAT-DCM-01 | RWB-E1-024 | TC-E1-024-01 |
| REQ-DCM-002 | FEAT-DCM-01 | RWB-E1-024 | TC-E1-024-01 |
| REQ-DCM-003 | FEAT-DCM-01 | RWB-E1-024 | TC-E1-024-01 |
| REQ-DCM-004 | FEAT-DCM-01 | RWB-E1-024 | TC-E1-024-01 |
| REQ-DCM-005 | FEAT-DCM-01 | RWB-E1-024 | TC-E1-024-01 |
| REQ-DCM-006 | FEAT-DCM-01 | RWB-E1-024 | TC-E1-024-01 |
| REQ-DCM-007 | FEAT-DCM-01 | RWB-E1-024 | TC-E1-024-01 |
| REQ-DCM-008 | FEAT-DCM-01 | RWB-E1-024 | TC-E1-024-01 |
| REQ-DCM-009 | FEAT-DCM-01 | RWB-E1-024 | TC-E1-024-01 |
| REQ-DCM-010 | FEAT-DCM-01 | RWB-E1-024 | TC-E1-024-01 |
| REQ-DCM-011 | FEAT-DCM-01 | RWB-E1-024 | TC-E1-024-01 |
| REQ-DCM-012 | FEAT-DCM-21 | RWB-E2-024 | TC-E2-024-01 |
| REQ-DCM-013 | FEAT-DCM-21 | RWB-E2-024 | TC-E2-024-01 |
| REQ-DCM-014 | FEAT-DCM-01 | RWB-E1-024 | TC-E1-024-01 |
| REQ-DCM-015 | FEAT-DCM-01 | RWB-E1-024 | TC-E1-024-01 |
| REQ-DCM-016 | FEAT-DCM-01 | RWB-E1-024 | TC-E1-024-01 |
| REQ-DCM-017 | FEAT-DCM-21 | RWB-E2-024 | TC-E2-024-01 |
| REQ-DCM-018 | FEAT-DCM-21 | RWB-E2-024 | TC-E2-024-01 |
| REQ-DCM-019 | FEAT-DCM-21 | RWB-E2-024 | TC-E2-024-01 |
| REQ-DCM-020 | FEAT-DCM-01 | RWB-E1-024 | TC-E1-024-01 |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-P5-001 | POST | /api/recovery/v1/cases/{caseId}/documents | Documents C | E1 |
| API-P5-002 | GET | /api/recovery/v1/cases/{caseId}/documents | Documents R | E1 |
| API-P5-003 | GET | /api/recovery/v1/documents/{documentId} | Documents R | E1 |
| API-P5-004 | GET | /api/recovery/v1/documents/{documentId}/content | Documents R | E1 |
| API-P5-005 | POST | /api/recovery/v1/documents/{documentId}/versions | Documents U | E1 |
| API-P5-006 | PATCH | /api/recovery/v1/documents/{documentId}/fields/{fieldId} | Documents U | E1 |
| API-P5-007 | POST | /api/recovery/v1/documents/{documentId}/custody | Documents U | E2 |
| API-P5-008 | GET | /api/recovery/v1/cases/{caseId}/document-checklist | Documents R | E1 |
| API-P5-009 | GET | /api/recovery/v1/documents | Documents R | E1 |
| API-P5-010 | GET | /api/recovery/v1/review-items | Documents R | E1 |
| API-P5-011 | GET | /api/recovery/v1/intake-items/{intakeItemId} | Documents R | E1 |
| API-P5-012 | GET | /api/recovery/v1/intake-items/{intakeItemId}/content | Documents R | E1 |
| API-P5-013 | POST | /api/recovery/v1/intake-items/{intakeItemId}/resolve | Documents U | E1 |
| API-P5-014 | POST | /api/recovery/v1/documents/{documentId}/review | Documents U | E1 |
| API-P5-015 | POST | /api/recovery/v1/cases/{caseId}/field-captures | Documents C | E2 |
| API-P5-016 | POST | /api/recovery/v1/cases/{caseId}/generated-documents | Documents C | E2 |
| API-P5-017 | POST | /api/recovery/v1/documents/{documentId}/regenerate | Documents U | E2 |

### T-A.2 Endpoint detail

#### API-P5-001 POST /cases/{caseId}/documents

| Item | Value |
|---|---|
| Purpose | Upload a document to the case |
| Request | Multipart: file, type, source |
| Response | Document |
| Errors | 401, 403, 404, 413, 415, 422, 503 |
| Authorization | Documents, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P5-002 GET /cases/{caseId}/documents

| Item | Value |
|---|---|
| Purpose | List the documents on a case |
| Request | Query: type, page, size |
| Response | DocumentPage |
| Errors | 401, 403, 404, 503 |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |

#### API-P5-003 GET /documents/{documentId}

| Item | Value |
|---|---|
| Purpose | Read a document's metadata, versions and extracted fields |
| Request | None |
| Response | Document |
| Errors | 401, 403, 404, 503 |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |

#### API-P5-004 GET /documents/{documentId}/content

| Item | Value |
|---|---|
| Purpose | Download the document content |
| Request | None |
| Response | Binary |
| Errors | 401, 403, 404, 503 |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |

#### API-P5-005 POST /documents/{documentId}/versions

| Item | Value |
|---|---|
| Purpose | Add a new version of a document |
| Request | Multipart: file, reason |
| Response | Document |
| Errors | 401, 403, 404, 409, 415, 503 |
| Authorization | Documents, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P5-006 PATCH /documents/{documentId}/fields/{fieldId}

| Item | Value |
|---|---|
| Purpose | Confirm or correct an extracted field |
| Request | FieldReview |
| Response | DocumentField |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Documents, right U, scope applied |
| Idempotency | Not applicable |

#### API-P5-007 POST /documents/{documentId}/custody

| Item | Value |
|---|---|
| Purpose | Record an original document going out or coming back |
| Request | CustodyRequest |
| Response | DocumentCustody |
| Errors | 401, 403, 404, 422, 503 |
| Authorization | Documents, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P5-008 GET /cases/{caseId}/document-checklist

| Item | Value |
|---|---|
| Purpose | Read the required document types for the case with present counts |
| Request | None |
| Response | DocumentChecklist |
| Errors | 401, 403, 404, 503 |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |

#### API-P5-009 GET /documents

| Item | Value |
|---|---|
| Purpose | Search active documents across the cases in the caller's scope by type, stored date, extracted field and free text; each search written to the access log |
| Request | Query: type, dateFrom, dateTo, field, op, value, value2, q, page, size |
| Response | DocumentSearchPage |
| Errors | 401, 403, 422, 503 |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |

#### API-P5-010 GET /review-items

| Item | Value |
|---|---|
| Purpose | List the document review queue: held intake items and documents with fields in review, in the caller's scope, oldest first |
| Request | Query: kind, reason, page, size |
| Response | ReviewItemPage |
| Errors | 401, 403, 422, 503 |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |

#### API-P5-011 GET /intake-items/{intakeItemId}

| Item | Value |
|---|---|
| Purpose | Read one held intake item with its OCR text, candidates and extracted fields, masked by role; each read written to the access log |
| Request | None |
| Response | IntakeItem |
| Errors | 401, 403, 404, 503 |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |

#### API-P5-012 GET /intake-items/{intakeItemId}/content

| Item | Value |
|---|---|
| Purpose | Download the file of a held intake item for the reviewer |
| Request | None |
| Response | Binary |
| Errors | 401, 403, 404, 503 |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |

#### API-P5-013 POST /intake-items/{intakeItemId}/resolve

| Item | Value |
|---|---|
| Purpose | Resolve a held intake item: set its type, attach it to a case in scope with confirmed fields, or discard it with a reason |
| Request | IntakeResolveRequest |
| Response | IntakeResolution |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Documents, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P5-014 POST /documents/{documentId}/review

| Item | Value |
|---|---|
| Purpose | Complete the review of a stored document or a generated draft whose fields were in review |
| Request | DocumentReviewRequest |
| Response | Document |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Documents, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P5-015 POST /cases/{caseId}/field-captures

| Item | Value |
|---|---|
| Purpose | Sync field app photos, bills and checklists for a case with capture time and position |
| Request | Multipart: manifest, files |
| Response | FieldCaptureResult |
| Errors | 401, 403, 404, 413, 415, 422, 503 |
| Authorization | Documents, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P5-016 POST /cases/{caseId}/generated-documents

| Item | Value |
|---|---|
| Purpose | Generate documents for an approved treatment from the current Legal-approved template versions |
| Request | GenerateRequest |
| Response | DocumentPage |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Documents, right C, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P5-017 POST /documents/{documentId}/regenerate

| Item | Value |
|---|---|
| Purpose | Correct overridable merge values of a generated draft with a reason and generate the next version |
| Request | RegenerateRequest |
| Response | Document |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Documents, right U, scope applied |
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

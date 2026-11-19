<!-- source: 05 Technical architecture/Recovery Workbench Technical Specifications by Module v3.zip!Recovery Workbench TSD P1 Recovery data engine v2.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `05 Technical architecture/Recovery Workbench Technical Specifications by Module v3.zip!Recovery Workbench TSD P1 Recovery data engine v2.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench P1 Recovery data engine

Technical specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | TSD P1 Recovery data engine |
| Document ID | P1-RWB-TSD-v2 |
| Version | 2 |
| Status | In review |
| Date | 28 October 2026 |
| TSD owner | Solution architect |
| Build squad | TechX recovery squads |

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench FSD P1 Recovery data engine | FSD | Pair |
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

P1 Recovery data engine is part of the recovery module in the ACE service: one service, one repository, one front end. It covers: cOLLINS and file loads, load checks, reconciliation, freshness. It reaches other modules only through their published interfaces and other systems only through COLLINS, file loads and the ACE paths.

## T2. Component design

| Component | Responsibility |
|---|---|
| RecoveryDataEngineController | REST endpoints in appendix T-A; validation; maps errors to problem responses |
| RecoveryDataEngineService | Business logic; calls the rules component; writes the decision log entry before any change |
| RecoveryDataEngineRepository | Reads and writes the module's tables only |
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

**loan_account** (REUSE ACE Account). A loan account in the core bank.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-ACC-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-ACC-002 | account_no | TEXT | varchar(20) | Yes | None | Core bank (ALS) via COLLINS |
| DF-ACC-003 | contract_no | TEXT | varchar(20) | No | None | Core bank (ALS) via COLLINS |
| DF-ACC-004 | product_code | LOV | varchar(10) | Yes | LOV-PRODUCT-CODE | Core bank (ALS) via COLLINS |
| DF-ACC-005 | product_category_efs | TEXT | varchar(60) | No | None | EFS via COLLINS |
| DF-ACC-006 | business_unit | LOV | varchar(10) | No | LOV-BU | Core bank (ALS) via COLLINS |
| DF-ACC-007 | contract_date | DATE | date | No | None | Core bank (ALS) via COLLINS |
| DF-ACC-008 | interest_rate | NUMBER | numeric(7,4) | No | None | Core bank (ALS) via COLLINS |
| DF-ACC-009 | principal_outstanding | NUMBER | numeric(18,2) | Yes | None | Core bank (ALS) via COLLINS |
| DF-ACC-010 | interest_outstanding | NUMBER | numeric(18,2) | Yes | None | Core bank (ALS) via COLLINS |
| DF-ACC-011 | fees_outstanding | NUMBER | numeric(18,2) | Yes | None | Core bank (ALS) via COLLINS |
| DF-ACC-012 | total_balance | NUMBER | numeric(18,2) | Yes | None | Core bank (ALS) via COLLINS |
| DF-ACC-013 | accounting_balance | NUMBER | numeric(18,2) | No | None | Core bank (ALS) via COLLINS |
| DF-ACC-014 | days_past_due | NUMBER | integer | Yes | None | Core bank (ALS) via COLLINS |
| DF-ACC-015 | bucket | LOV | varchar(10) | No | LOV-BUCKET | Core bank (ALS) via COLLINS |
| DF-ACC-016 | classification | LOV | varchar(10) | No | LOV-CLASS | Core bank (ALS) via COLLINS |
| DF-ACC-017 | last_payment_date | DATE | date | No | None | Core bank (ALS) via COLLINS |
| DF-ACC-018 | next_installment_date | DATE | date | No | None | Core bank (ALS) via COLLINS |
| DF-ACC-019 | tdr_flag | BOOLEAN | boolean | Yes | None | Core bank (ALS) via COLLINS |
| DF-ACC-020 | last_tdr_date | DATE | date | No | None | Core bank (ALS) via COLLINS |
| DF-ACC-021 | data_as_of | DATE | date | Yes | None | Core bank (ALS) via COLLINS |
| DF-ACC-029 | dispute_open | BOOLEAN | boolean | Yes | None | Workbench |
| DF-ACC-030 | settlement_booked_date | DATE | date | No | None | Core bank (ALS) via COLLINS |
| DF-ACC-031 | settlement_booked_amount | NUMBER | numeric(18,2) | No | None | Core bank (ALS) via COLLINS |

**account_payment** (REUSE ACE Payment). A payment posted to a loan account.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-ACC-022 | id | TEXT | uuid | Yes | None | Workbench |
| DF-ACC-023 | account_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-ACC-024 | payment_code | TEXT | varchar(20) | Yes | None | Core bank (ALS) via COLLINS |
| DF-ACC-025 | payment_date | DATE | date | Yes | None | Core bank (ALS) via COLLINS |
| DF-ACC-026 | payment_amount | NUMBER | numeric(18,2) | Yes | None | Core bank (ALS) via COLLINS |
| DF-ACC-027 | payment_channel | LOV | varchar(15) | No | LOV-PAY-CHANNEL | Core bank (ALS) via COLLINS |
| DF-ACC-028 | data_as_of | DATE | date | Yes | None | Core bank (ALS) via COLLINS |

**party** (EXTEND ACE Customer). A person or company with a role on one or more cases.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-PTY-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-PTY-002 | cif_no | TEXT | varchar(20) | Yes | None | SCBPDM via COLLINS |
| DF-PTY-003 | party_type | LOV | varchar(15) | Yes | LOV-PARTY-TYPE | SCBPDM via COLLINS |
| DF-PTY-004 | first_name | TEXT | varchar(100) | Yes | None | SCBPDM via COLLINS |
| DF-PTY-005 | last_name | TEXT | varchar(100) | No | None | SCBPDM via COLLINS |
| DF-PTY-006 | id_type | LOV | varchar(20) | Yes | LOV-ID-TYPE | SCBPDM via COLLINS |
| DF-PTY-007 | id_no_token | TEXT | varchar(64) | Yes | None | SCBPDM via COLLINS |
| DF-PTY-008 | date_of_birth | DATE | date | No | None | SCBPDM via COLLINS |
| DF-PTY-009 | segment | LOV | varchar(20) | No | LOV-SEGMENT | SCBPDM via COLLINS |
| DF-PTY-010 | vulnerable_flag | BOOLEAN | boolean | Yes | None | Workbench |
| DF-PTY-011 | deceased_flag | BOOLEAN | boolean | Yes | None | Workbench |
| DF-PTY-012 | bankruptcy_flag | BOOLEAN | boolean | Yes | None | Workbench |
| DF-PTY-021 | fraud_flag | BOOLEAN | boolean | Yes | None | Aric via COLLINS |

**contact_point** (NEW). A way to reach a party, with its consent and whether it works.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-PTY-013 | id | TEXT | uuid | Yes | None | Workbench |
| DF-PTY-014 | party_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-PTY-015 | channel | LOV | varchar(15) | Yes | LOV-CHANNEL | Workbench |
| DF-PTY-016 | value_token | TEXT | varchar(256) | Yes | None | SCBPDM via COLLINS |
| DF-PTY-017 | source | LOV | varchar(15) | Yes | LOV-CONTACT-SRC | Workbench |
| DF-PTY-018 | consent_status | LOV | varchar(12) | Yes | LOV-CONSENT | Workbench |
| DF-PTY-019 | verified_at | DATE | timestamptz | No | None | Workbench |
| DF-PTY-020 | failed_count | NUMBER | integer | Yes | None | Workbench |

**collateral** (EXTEND ACE Collateral). Property or vehicle securing one or more accounts.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-COL-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-COL-002 | collateral_no | TEXT | varchar(20) | Yes | None | CCMS |
| DF-COL-003 | collateral_type | LOV | varchar(15) | Yes | LOV-COLL-TYPE | CCMS |
| DF-COL-004 | title_doc_no | TEXT | varchar(40) | No | None | CCMS |
| DF-COL-005 | plot_no | TEXT | varchar(20) | No | None | CCMS |
| DF-COL-006 | area_text | TEXT | varchar(20) | No | None | CCMS |
| DF-COL-007 | province | LOV | varchar(40) | No | LOV-PROVINCE | CCMS |
| DF-COL-008 | district | TEXT | varchar(60) | No | None | CCMS |
| DF-COL-009 | subdistrict | TEXT | varchar(60) | No | None | CCMS |
| DF-COL-010 | occupancy | LOV | varchar(15) | No | LOV-OCCUPANCY | Workbench |
| DF-COL-011 | encumbrance_status | LOV | varchar(15) | No | LOV-ENCUMBRANCE | Workbench |
| DF-COL-012 | insured_value | NUMBER | numeric(18,2) | No | None | CCMS |
| DF-COL-013 | insurance_expiry | DATE | date | No | None | CCMS |

**account_collateral** (NEW). Which collateral secures which account.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-COL-014 | id | TEXT | uuid | Yes | None | Workbench |
| DF-COL-015 | account_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-COL-016 | collateral_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-COL-017 | lien_rank | NUMBER | integer | No | None | CCMS |

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

**data_product** (NEW). One of the 14 data products, with its single system of record, owner and refresh cycle.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-070 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-071 | product_code | LOV | varchar(25) | Yes | LOV-DATA-PRODUCT | Workbench |
| DF-REF-072 | product_name | TEXT | varchar(80) | Yes | None | Workbench |
| DF-REF-073 | definition | TEXT | varchar(400) | Yes | None | Workbench |
| DF-REF-074 | system_of_record | TEXT | varchar(120) | Yes | None | Workbench |
| DF-REF-075 | owner_role | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-REF-076 | owner_user_id | USER_REF | uuid | No | None | Workbench |
| DF-REF-077 | refresh_cycle | LOV | varchar(10) | Yes | LOV-REFRESH | Workbench |
| DF-REF-078 | expected_by | TEXT | varchar(20) | No | None | Workbench |
| DF-REF-079 | valid_from | DATE | date | Yes | None | Workbench |

**data_product_access** (NEW). Which role may read which data product, by version.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-080 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-081 | product_code | LOV | varchar(25) | Yes | LOV-DATA-PRODUCT | Workbench |
| DF-REF-082 | role_code | LOV | varchar(20) | Yes | LOV-ROLE | Workbench |
| DF-REF-083 | can_read | BOOLEAN | boolean | Yes | None | Workbench |
| DF-REF-084 | access_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-085 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-086 | valid_to | DATE | date | No | None | Workbench |

**data_product_load** (NEW). The freshness stamp of a data product for one business date.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-002 | product_code | LOV | varchar(25) | Yes | LOV-DATA-PRODUCT | Workbench |
| DF-OPS-003 | source_system | TEXT | varchar(40) | Yes | None | Workbench |
| DF-OPS-004 | business_date | DATE | date | Yes | None | Workbench |
| DF-OPS-005 | source_extracted_at | DATE | timestamptz | Yes | None | Workbench |
| DF-OPS-006 | loaded_at | DATE | timestamptz | Yes | None | Workbench |
| DF-OPS-007 | status | LOV | varchar(10) | Yes | LOV-FRESHNESS | Workbench |
| DF-OPS-008 | stale_flagged_at | DATE | timestamptz | No | None | Workbench |
| DF-OPS-009 | duplicate_count | NUMBER | integer | Yes | None | Workbench |

**data_contract** (NEW). A versioned data contract with one source system, confirmed by its system owner.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-010 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-011 | contract_code | TEXT | varchar(20) | Yes | None | Workbench |
| DF-OPS-012 | source_system | TEXT | varchar(80) | Yes | None | Workbench |
| DF-OPS-013 | interface_id | TEXT | varchar(40) | Yes | None | Workbench |
| DF-OPS-014 | contract_version | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-015 | status | LOV | varchar(10) | Yes | LOV-CONTRACT-STATUS | Workbench |
| DF-OPS-016 | confirmed_by_role | TEXT | varchar(80) | No | None | Workbench |
| DF-OPS-017 | confirmed_on | DATE | date | No | None | Workbench |
| DF-OPS-018 | confirmation_document_ref | ATTACHMENT | varchar(400) | No | None | Workbench |
| DF-OPS-019 | published_at | DATE | timestamptz | No | None | Workbench |
| DF-OPS-020 | published_by | USER_REF | uuid | No | None | Workbench |

**sys_objects** (NEW). The metadata registry of entities: one row per object in the data dictionary.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-087 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-088 | object_name | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-089 | business_name | TEXT | varchar(120) | Yes | None | Workbench |
| DF-REF-090 | subject_area | TEXT | varchar(10) | Yes | None | Workbench |
| DF-REF-091 | data_product | TEXT | varchar(10) | Yes | None | Workbench |
| DF-REF-092 | system_of_record | TEXT | varchar(120) | Yes | None | Workbench |
| DF-REF-093 | description | TEXT | varchar(400) | Yes | None | Workbench |

**sys_fields** (NEW). The metadata registry of fields: the data dictionary held as data.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-094 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-095 | field_id | TEXT | varchar(16) | Yes | None | Workbench |
| DF-REF-096 | object_name | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-097 | field_name | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-098 | data_type | TEXT | varchar(12) | Yes | None | Workbench |
| DF-REF-099 | physical_type | TEXT | varchar(30) | Yes | None | Workbench |
| DF-REF-100 | is_mandatory | BOOLEAN | boolean | Yes | None | Workbench |
| DF-REF-101 | lov_code | TEXT | varchar(30) | No | None | Workbench |
| DF-REF-102 | references_object | TEXT | varchar(60) | No | None | Workbench |
| DF-REF-103 | source_system | TEXT | varchar(80) | Yes | None | Workbench |
| DF-REF-104 | source_field | TEXT | varchar(80) | No | None | Workbench |
| DF-REF-105 | is_personal | BOOLEAN | boolean | Yes | None | Workbench |
| DF-REF-106 | description | TEXT | varchar(400) | Yes | None | Workbench |
| DF-REF-107 | owner_role | LOV | varchar(20) | No | LOV-ROLE | Workbench |
| DF-REF-108 | refresh_cycle | TEXT | varchar(30) | No | None | Workbench |
| DF-REF-109 | late_behavior | TEXT | varchar(200) | No | None | Workbench |
| DF-REF-110 | interface_id | TEXT | varchar(10) | No | None | Workbench |

**sys_field_version** (NEW). Each version of a field definition, kept when the definition changes.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-111 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-112 | field_id | TEXT | varchar(16) | Yes | None | Workbench |
| DF-REF-113 | field_version | NUMBER | integer | Yes | None | Workbench |
| DF-REF-114 | definition | TEXT | jsonb | Yes | None | Workbench |
| DF-REF-115 | change_reason | TEXT | varchar(400) | Yes | None | Workbench |

**load_run** (NEW). One run of a data load or job step, with its checks and row counts.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-021 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-022 | interface_id | TEXT | varchar(10) | No | None | Workbench |
| DF-OPS-023 | job_code | TEXT | varchar(6) | No | None | Workbench |
| DF-OPS-024 | product_code | LOV | varchar(25) | No | LOV-DATA-PRODUCT | Workbench |
| DF-OPS-025 | business_date | DATE | date | Yes | None | Workbench |
| DF-OPS-026 | status | LOV | varchar(12) | Yes | LOV-LOAD-STATUS | Workbench |
| DF-OPS-027 | started_at | DATE | timestamptz | Yes | None | Workbench |
| DF-OPS-028 | ended_at | DATE | timestamptz | No | None | Workbench |
| DF-OPS-029 | rows_read | NUMBER | integer | No | None | Workbench |
| DF-OPS-030 | rows_loaded | NUMBER | integer | No | None | Workbench |
| DF-OPS-031 | rows_held | NUMBER | integer | No | None | Workbench |
| DF-OPS-032 | rows_rejected | NUMBER | integer | No | None | Workbench |
| DF-OPS-033 | failed_check | TEXT | varchar(8) | No | None | Workbench |
| DF-OPS-034 | check_results | TEXT | jsonb | No | None | Workbench |
| DF-OPS-035 | mapping_version | TEXT | varchar(20) | No | None | Workbench |
| DF-OPS-036 | interface_run_id | CROSS_REF | uuid | No | None | Workbench |
| DF-OPS-037 | tracker_id | CROSS_REF | uuid | No | None | Workbench |
| DF-OPS-038 | loaded_by | USER_REF | uuid | No | None | Workbench |
| DF-OPS-039 | source_file_name | TEXT | varchar(200) | No | None | Workbench |
| DF-OPS-040 | source_file_hash | TEXT | char(64) | No | None | Workbench |

**dq_exception** (NEW). A record a load check or data quality rule held, until it passes again.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-041 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-042 | load_run_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-OPS-043 | product_code | LOV | varchar(25) | Yes | LOV-DATA-PRODUCT | Workbench |
| DF-OPS-044 | check_code | TEXT | varchar(8) | Yes | None | Workbench |
| DF-OPS-045 | record_key | TEXT | varchar(60) | Yes | None | Workbench |
| DF-OPS-046 | reason_code | TEXT | varchar(8) | Yes | None | Workbench |
| DF-OPS-047 | detail | TEXT | varchar(400) | No | None | Workbench |
| DF-OPS-048 | raised_on | DATE | date | Yes | None | Workbench |
| DF-OPS-049 | status | LOV | varchar(10) | Yes | LOV-DQ-STATUS | Workbench |
| DF-OPS-050 | rule_version | TEXT | varchar(20) | No | None | Workbench |
| DF-OPS-051 | cleared_on | DATE | date | No | None | Workbench |

**dq_rule** (NEW). A versioned data quality row rule run on a P1 table.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-052 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-053 | rule_code | TEXT | varchar(8) | Yes | None | Workbench |
| DF-OPS-054 | rule_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-OPS-055 | rule_name | TEXT | varchar(120) | Yes | None | Workbench |
| DF-OPS-056 | product_code | LOV | varchar(25) | Yes | LOV-DATA-PRODUCT | Workbench |
| DF-OPS-057 | target_entity | TEXT | varchar(60) | Yes | None | Workbench |
| DF-OPS-058 | rule_type | LOV | varchar(15) | Yes | LOV-DQ-RULE-TYPE | Workbench |
| DF-OPS-059 | rule_params | TEXT | jsonb | Yes | None | Workbench |
| DF-OPS-060 | valid_from | DATE | date | Yes | None | Workbench |
| DF-OPS-061 | valid_to | DATE | date | No | None | Workbench |
| DF-OPS-062 | approved_by | USER_REF | uuid | Yes | None | Workbench |
| DF-OPS-063 | test_case_id | TEXT | varchar(20) | Yes | None | Workbench |

**source_field_map** (NEW). How a source field maps to a Workbench field, by interface and mapping version.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-064 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-065 | interface_id | TEXT | varchar(10) | Yes | None | Workbench |
| DF-OPS-066 | mapping_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-OPS-067 | source_field | TEXT | varchar(80) | Yes | None | Workbench |
| DF-OPS-068 | target_entity | TEXT | varchar(60) | Yes | None | Workbench |
| DF-OPS-069 | target_field | TEXT | varchar(60) | Yes | None | Workbench |
| DF-OPS-070 | transformation | TEXT | varchar(200) | Yes | None | Workbench |
| DF-OPS-071 | approved_by | USER_REF | uuid | No | None | Workbench |
| DF-OPS-072 | approved_on | DATE | date | No | None | Workbench |
| DF-OPS-073 | approval_ref | TEXT | varchar(200) | No | None | Workbench |
| DF-OPS-074 | valid_from | DATE | date | Yes | None | Workbench |

**source_code_map** (NEW). How a source code maps to a Workbench list value, by interface and map version.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-075 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-076 | interface_id | TEXT | varchar(10) | Yes | None | Workbench |
| DF-OPS-077 | lov_code | TEXT | varchar(30) | Yes | None | Workbench |
| DF-OPS-078 | source_code | TEXT | varchar(30) | Yes | None | Workbench |
| DF-OPS-079 | value_code | TEXT | varchar(30) | Yes | None | Workbench |
| DF-OPS-080 | map_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-OPS-081 | valid_from | DATE | date | Yes | None | Workbench |
| DF-OPS-082 | valid_to | DATE | date | No | None | Workbench |

**tracker_inventory** (NEW). A team's Excel or SharePoint tracker, its decision and its load, sign-off and retirement.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-083 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-084 | tracker_code | TEXT | varchar(20) | Yes | None | Workbench |
| DF-OPS-085 | inventory_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-OPS-086 | team_code | LOV | varchar(20) | Yes | LOV-TEAM | Workbench |
| DF-OPS-087 | tracker_name | TEXT | varchar(120) | Yes | None | Workbench |
| DF-OPS-088 | location_type | LOV | varchar(12) | Yes | LOV-TRACKER-LOCATION | Workbench |
| DF-OPS-089 | location_ref | TEXT | varchar(400) | No | None | Workbench |
| DF-OPS-090 | owner_user_id | USER_REF | uuid | No | None | Workbench |
| DF-OPS-091 | field_list | TEXT | jsonb | Yes | None | Workbench |
| DF-OPS-092 | update_cycle | LOV | varchar(10) | No | LOV-UPDATE-CYCLE | Workbench |
| DF-OPS-093 | target_product | LOV | varchar(25) | No | LOV-DATA-PRODUCT | Workbench |
| DF-OPS-094 | decision | LOV | varchar(8) | No | LOV-TRACKER-DECISION | Workbench |
| DF-OPS-095 | decision_reason | TEXT | varchar(400) | No | None | Workbench |
| DF-OPS-096 | status | LOV | varchar(12) | Yes | LOV-TRACKER-STATUS | Workbench |
| DF-OPS-097 | valid_from | DATE | date | Yes | None | Workbench |
| DF-OPS-098 | file_rows | NUMBER | integer | No | None | Workbench |
| DF-OPS-099 | loaded_rows | NUMBER | integer | No | None | Workbench |
| DF-OPS-100 | rejected_rows | NUMBER | integer | No | None | Workbench |
| DF-OPS-101 | last_load_run_id | CROSS_REF | uuid | No | None | Workbench |
| DF-OPS-102 | signed_off_by | USER_REF | uuid | No | None | Workbench |
| DF-OPS-103 | signed_off_at | DATE | timestamptz | No | None | Workbench |
| DF-OPS-104 | source_file_ref | ATTACHMENT | varchar(400) | No | None | Workbench |
| DF-OPS-105 | archive_ref | TEXT | varchar(400) | No | None | Workbench |
| DF-OPS-106 | retired_at | DATE | timestamptz | No | None | Workbench |
| DF-OPS-107 | retire_confirmed_by | USER_REF | uuid | No | None | Workbench |
| DF-OPS-108 | unfed_fields | TEXT | jsonb | No | None | Workbench |

**tracker_row** (NEW). One row loaded from a tracker file, with its non-personal fields.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-109 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-110 | tracker_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-OPS-111 | load_run_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-OPS-112 | row_no | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-113 | account_no | TEXT | varchar(20) | No | None | Workbench |
| DF-OPS-114 | target_product | LOV | varchar(25) | Yes | LOV-DATA-PRODUCT | Workbench |
| DF-OPS-115 | source_file_name | TEXT | varchar(200) | Yes | None | Workbench |
| DF-OPS-116 | field_values | TEXT | jsonb | No | None | Workbench |
| DF-OPS-117 | loaded_on | DATE | date | Yes | None | Workbench |

**case_list_row** (NEW). One row of the daily case list per case account and business date, published to Power BI.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-RPT-001 | id | TEXT | uuid | Yes | None | Workbench |
| DF-RPT-002 | business_date | DATE | date | Yes | None | Workbench |
| DF-RPT-003 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-RPT-004 | case_no | TEXT | varchar(18) | Yes | None | Workbench |
| DF-RPT-005 | account_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-RPT-006 | account_no | TEXT | varchar(20) | Yes | None | Workbench |
| DF-RPT-007 | product_group | LOV | varchar(15) | Yes | LOV-PRODUCT | Workbench |
| DF-RPT-008 | stage_code | LOV | varchar(20) | No | LOV-STAGE | Workbench |
| DF-RPT-009 | status | LOV | varchar(20) | Yes | LOV-CASE-STATUS | Workbench |
| DF-RPT-010 | owner_user_id | USER_REF | uuid | No | None | Workbench |
| DF-RPT-011 | queue_code | TEXT | varchar(30) | No | None | Workbench |
| DF-RPT-012 | team_code | LOV | varchar(20) | No | LOV-TEAM | Workbench |
| DF-RPT-013 | route_code | LOV | varchar(4) | No | LOV-ROUTE | Workbench |
| DF-RPT-014 | total_balance | NUMBER | numeric(18,2) | Yes | None | Workbench |
| DF-RPT-015 | days_past_due | NUMBER | integer | Yes | None | Workbench |
| DF-RPT-016 | refreshed_at | DATE | timestamptz | Yes | None | Workbench |
| DF-RPT-017 | last_contact_at | DATE | timestamptz | No | None | Workbench |
| DF-RPT-018 | last_action_code | LOV | varchar(10) | No | LOV-ACTION-CODE | Workbench |
| DF-RPT-019 | publish_status | LOV | varchar(10) | Yes | LOV-PUBLISH-STATUS | Workbench |

**collections_history** (NEW). An EFS contact or promise on an account, loaded from the COLLINS daily batch.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-INT-030 | id | TEXT | uuid | Yes | None | Workbench |
| DF-INT-031 | account_no | TEXT | varchar(20) | Yes | None | EFS via COLLINS |
| DF-INT-032 | efs_record_key | TEXT | varchar(40) | Yes | None | EFS via COLLINS |
| DF-INT-033 | contact_at | DATE | timestamptz | Yes | None | EFS via COLLINS |
| DF-INT-034 | action_code | LOV | varchar(10) | Yes | LOV-ACTION-CODE | EFS via COLLINS |
| DF-INT-035 | action_contact_status | TEXT | varchar(20) | No | None | EFS via COLLINS |
| DF-INT-036 | contact_result | LOV | varchar(20) | No | LOV-CONTACT-RESULT | EFS via COLLINS |
| DF-INT-037 | promise_amount | NUMBER | numeric(18,2) | No | None | EFS via COLLINS |
| DF-INT-038 | promise_date | DATE | date | No | None | EFS via COLLINS |
| DF-INT-039 | business_date | DATE | date | Yes | None | Workbench |

**reconciliation_result** (NEW). The daily reconciliation of the case list to ALS by product group.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-118 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-119 | rec_code | TEXT | varchar(6) | Yes | None | Workbench |
| DF-OPS-120 | business_date | DATE | date | Yes | None | Workbench |
| DF-OPS-121 | product_group | LOV | varchar(15) | Yes | LOV-PRODUCT | Workbench |
| DF-OPS-122 | source_count | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-123 | workbench_count | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-124 | source_amount | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-OPS-125 | workbench_amount | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-OPS-126 | variance_count | NUMBER | integer | Yes | None | Workbench |
| DF-OPS-127 | variance_pct | NUMBER | numeric(9,4) | Yes | None | Workbench |
| DF-OPS-128 | tolerance_pct | NUMBER | numeric(9,4) | Yes | None | Workbench |
| DF-OPS-129 | result | LOV | varchar(8) | Yes | LOV-REC-RESULT | Workbench |

**lake_copy_watermark** (NEW). How far a copy to the data lake has reached, for example the decision log copy.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-OPS-130 | id | TEXT | uuid | Yes | None | Workbench |
| DF-OPS-131 | copy_name | TEXT | varchar(40) | Yes | None | Workbench |
| DF-OPS-132 | last_entry_hash | TEXT | char(64) | No | None | Workbench |
| DF-OPS-133 | last_decided_at | DATE | timestamptz | No | None | Workbench |
| DF-OPS-134 | rows_copied_total | NUMBER | bigint | Yes | None | Workbench |
| DF-OPS-135 | business_date | DATE | date | No | None | Workbench |

**retention_rule** (NEW). How long rows of a table or a retention class are kept and what happens at the end, by version.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-REF-116 | id | TEXT | uuid | Yes | None | Workbench |
| DF-REF-117 | product_code | LOV | varchar(25) | Yes | LOV-DATA-PRODUCT | Workbench |
| DF-REF-118 | table_name | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-119 | record_class | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-120 | retention_months | NUMBER | integer | Yes | None | Workbench |
| DF-REF-121 | age_basis_field | TEXT | varchar(60) | Yes | None | Workbench |
| DF-REF-122 | end_action | LOV | varchar(12) | Yes | LOV-RETENTION-END | Workbench |
| DF-REF-123 | rule_version | TEXT | varchar(20) | Yes | None | Workbench |
| DF-REF-124 | valid_from | DATE | date | Yes | None | Workbench |
| DF-REF-125 | valid_to | DATE | date | No | None | Workbench |
| DF-REF-126 | approved_by | USER_REF | uuid | No | None | Workbench |
| DF-REF-127 | reference_version_id | CROSS_REF | uuid | No | None | Workbench |

**dp_treatment** (NEW). The copy of each treatment for a business date in the DP04 data product.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-TRT-034 | id | TEXT | uuid | Yes | None | Workbench |
| DF-TRT-035 | treatment_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-TRT-036 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-TRT-037 | decision_log_id | CROSS_REF | uuid | No | None | Workbench |
| DF-TRT-038 | treatment_type | LOV | varchar(20) | Yes | LOV-TREATMENT | Workbench |
| DF-TRT-039 | proposed_by | LOV | varchar(10) | Yes | LOV-PROPOSER | Workbench |
| DF-TRT-040 | proposed_at | DATE | timestamptz | Yes | None | Workbench |
| DF-TRT-041 | offer_amount | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-TRT-042 | haircut_amount | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-TRT-043 | installments | NUMBER | integer | No | None | Workbench |
| DF-TRT-044 | valid_until | DATE | date | No | None | Workbench |
| DF-TRT-045 | approval_level | LOV | varchar(4) | No | LOV-APPROVAL-LEVEL | Workbench |
| DF-TRT-046 | booked_at | DATE | timestamptz | No | None | Workbench |
| DF-TRT-047 | outcome | LOV | varchar(12) | No | LOV-TRT-OUTCOME | Workbench |
| DF-TRT-048 | outcome_at | DATE | timestamptz | No | None | Workbench |
| DF-TRT-049 | business_date | DATE | date | Yes | None | Workbench |
| DF-TRT-050 | contract_no | TEXT | varchar(20) | No | None | Core bank (ALS) via COLLINS |
| DF-TRT-051 | contract_date | DATE | date | No | None | Core bank (ALS) via COLLINS |

**dp_guarantee_claim** (NEW). The copy of each guarantee claim for a business date in the DP04 data product.

| BR Field ID | Field | Data type | Physical type | Required | List | Source |
|---|---|---|---|---|---|---|
| DF-TRT-052 | id | TEXT | uuid | Yes | None | Workbench |
| DF-TRT-053 | guarantee_claim_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-TRT-054 | case_id | CROSS_REF | uuid | Yes | None | Workbench |
| DF-TRT-055 | claim_type | LOV | varchar(25) | Yes | LOV-CLAIM-TYPE | Workbench |
| DF-TRT-056 | claim_deadline | DATE | date | Yes | None | Workbench |
| DF-TRT-057 | claimed_amount | NUMBER | numeric(18,2) | Yes | None | Workbench |
| DF-TRT-058 | filed_at | DATE | date | No | None | Workbench |
| DF-TRT-059 | paid_amount | NUMBER | numeric(18,2) | No | None | Workbench |
| DF-TRT-060 | status | LOV | varchar(12) | Yes | LOV-CLAIM-STATUS | Workbench |
| DF-TRT-061 | business_date | DATE | date | Yes | None | Workbench |

### T3.2 Lists of values

| List | Values |
|---|---|
| LOV-APPROVAL-LEVEL | L1, L2, L3, L4, L5, L6 |
| LOV-CASE-STATUS | NEW, ASSIGNED, IN_PROGRESS, WAITING_CUSTOMER, WAITING_PARTNER, WAITING_APPROVAL, ON_HOLD, CLOSED |
| LOV-CHANNEL | MOBILE, HOME_PHONE, WORK_PHONE, LINE, EMAIL, POSTAL_ADDRESS, CALL, VISIT, SMS, LETTER, PORTAL, BRANCH |
| LOV-CLAIM-STATUS | PREPARING, FILED, DEFECT, PAID, REJECTED |
| LOV-CLAIM-TYPE | TCG, CREDIT_LIFE_INSURANCE, MORTGAGE_INSURANCE, COLLATERAL_INSURANCE |
| LOV-COLL-TYPE | LAND, HOUSE, CONDOMINIUM, VEHICLE, DEPOSIT, OTHER |
| LOV-CONSENT | GIVEN, WITHDRAWN, UNKNOWN |
| LOV-CONTACT-RESULT | RIGHT_PARTY, THIRD_PARTY, NO_ANSWER, WRONG_NUMBER, REFUSED |
| LOV-CONTACT-SRC | BANK_RECORD, FIELD_VISIT, AGENCY, BUREAU_TRACE, CUSTOMER |
| LOV-CONTRACT-STATUS | DRAFT, PUBLISHED, SUPERSEDED |
| LOV-DATA-PRODUCT | DP01, DP02, DP03, DP04, DP05, DP06, DP07, DP08, DP09, DP10, DP11, DP12, DP13, DP14 |
| LOV-DQ-RULE-TYPE | NOT_NULL, UNIQUE_ACROSS, RANGE, SUM_EQUALS, EXISTS_LINK, MAX_AGE_DAYS, FIELD_BEFORE |
| LOV-DQ-STATUS | OPEN, CLEARED |
| LOV-ENCUMBRANCE | CLEAR, OTHER_CREDITOR, SEIZED, UNDER_DISPUTE |
| LOV-FRESHNESS | LOADED, STALE |
| LOV-ID-TYPE | THAI_NATIONAL_ID, PASSPORT, COMPANY_REGISTRATION |
| LOV-LOAD-STATUS | RUNNING, COMPLETED, REFUSED, LATE, FAILED, SUPERSEDED |
| LOV-OCCUPANCY | OWNER, TENANT, VACANT, UNKNOWN |
| LOV-PARTY-TYPE | INDIVIDUAL, JURISTIC_PERSON |
| LOV-PRODUCT | MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED |
| LOV-PROPOSER | AGENT, RULE, PERSON |
| LOV-PUBLISH-STATUS | PENDING, HELD, RELEASED |
| LOV-REC-RESULT | PASS, BREAK |
| LOV-REFRESH | DAILY, WEEKLY, MONTHLY, ON_CHANGE |
| LOV-RETENTION-END | ARCHIVE, REVIEW |
| LOV-ROUTE | R1, R2, R3, R4, R5, R6, R7, R8 |
| LOV-SEGMENT | RETAIL, SSME, CORPORATE |
| LOV-STAGE | RESTRUCTURE, SETTLEMENT, DEED_IN_LIEU, GUARANTEE_CLAIM, LITIGATION, ASSET_DISPOSAL, DEBT_SALE, WRITE_OFF, DEVIATIONS |
| LOV-TRACKER-DECISION | LOAD, RETIRE, KEEP |
| LOV-TRACKER-LOCATION | EXCEL, SHAREPOINT, LOCAL_FILE, NONE |
| LOV-TRACKER-STATUS | LISTED, LOADED, SIGNED_OFF, RETIRED, KEPT |
| LOV-TREATMENT | RESTRUCTURE, SETTLEMENT, DEED_IN_LIEU, BUY_BACK, GUARANTEE_CLAIM, REPOSSESSION, AUCTION, DEBT_SALE, WRITE_OFF, RAMC_TRANSFER, RENTAL |
| LOV-TRT-OUTCOME | KEPT, BROKEN, COMPLETED, CANCELED, DECLINED |
| LOV-UPDATE-CYCLE | DAILY, WEEKLY, MONTHLY, AD_HOC |

### T3.3 Relationships

| From | To | Field | Cardinality |
|---|---|---|---|
| contact_point | party_id | party | Many to 1 |
| account_payment | account_id | loan_account | Many to 1 |
| account_collateral | account_id | loan_account | Many to 1 |
| account_collateral | collateral_id | collateral | Many to 1 |
| score | account_id | loan_account | Many to 0 or 1 |
| score | case_id | recovery_case | Many to 0 or 1 |
| load_run | interface_run_id | interface_run | Many to 0 or 1 |
| load_run | tracker_id | tracker_inventory | Many to 0 or 1 |
| dq_exception | load_run_id | load_run | Many to 1 |
| tracker_inventory | last_load_run_id | load_run | Many to 0 or 1 |
| tracker_row | tracker_id | tracker_inventory | Many to 1 |
| tracker_row | load_run_id | load_run | Many to 1 |
| case_list_row | case_id | recovery_case | Many to 1 |
| case_list_row | account_id | loan_account | Many to 1 |
| retention_rule | reference_version_id | reference_version | Many to 0 or 1 |
| dp_treatment | treatment_id | treatment | Many to 1 |
| dp_treatment | case_id | recovery_case | Many to 1 |
| dp_treatment | decision_log_id | decision_log_entry | Many to 0 or 1 |
| dp_guarantee_claim | guarantee_claim_id | guarantee_claim | Many to 1 |
| dp_guarantee_claim | case_id | recovery_case | Many to 1 |

## T4. State machines and workflow

No case state machine of its own; the module acts on events from P3 and writes through the decision log.

## T5. Integration and interfaces

### T5.1 External system interfaces

| ID | System | Direction | Approach | Frequency |
|---|---|---|---|---|
| INT-01 | Core bank (ALS) | In | COLLINS batch | Daily, end of day |
| INT-02 | Core bank (ALS) | In | COLLINS batch | Daily, end of day |
| INT-04 | SCBPDM | In | COLLINS batch | Daily, end of day |
| INT-05 | UDP | In | COLLINS batch | Daily, end of day |
| INT-07 | EFS | In | COLLINS batch | Daily, end of day |
| INT-08 | COLLINS models | In | COLLINS batch | Daily; monthly for some models |
| INT-09 | LIT | In | COLLINS batch | Daily, end of day |
| INT-10 | CCMS | In | File load | Weekly |
| INT-11 | SVAF | In | File load | Weekly |
| INT-12 | AMIS | In | File load | Monthly |
| INT-13 | RPS | In | File load | Weekly |
| INT-15 | WIN | In | File load | Weekly |
| INT-16 | GL | In | File load | Monthly |

### T5.2 Cross-module interfaces

Calls go through the published Java interfaces: P3 for the case, P7 for the decision log, P4 for access and reference data, P5 for documents, P6 for notices.

### T5.3 Events

| Event | Direction |
|---|---|
| LoadCompleted | Published |
| LoadRefused | Published |

## T6. Security and access control

### T6.1 RBAC matrix

| Role | Platform administration |
|---|---|
| RW-COE Center of excellence analyst | R |
| RW-DATASTEW Data steward and data product owner | R |
| RW-AUDIT Internal audit | R |
| RW-COMPLY Compliance and PDPA officer | R |
| RW-PLATADM Platform administrator | CRUD |
| RW-SECADM Security administrator | CRUDA |

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
| NFR-013 | The daily core system load completes before the working day starts, and a failure raises an alert. | Job runs by 07:00 | Proposed |
| NFR-014 | Collections data is ingested at start of day. | Start of day | Proposed |
| NFR-015 | The recovery data store is no more than the agreed lag behind its sources, and a decision that must be made the same day uses an event instead. | End of day; in the Workbench the next morning. Same-day needs are named under DL06 | Proposed |
| NFR-016 | The document intake pipeline processes its throughput in the test environment. | 500 pages per hour | Proposed |
| NFR-017 | Document classification is correct on the labeled sample, and anything below the confidence threshold goes to a review queue. | 90 percent correct | Proposed |
| NFR-018 | The case list reconciles to the core system count daily. | No unexplained variance; tolerance per data product under DL25 | Proposed, DL25 |
| NFR-019 | The daily rebalancing job completes before the working day starts. | Complete by 07:00 | Proposed, DL11 |

## T8. Requirement traceability

| Requirement | Feature | Story | Test |
|---|---|---|---|
| REQ-RDF-001 | FEAT-RDF-01 | RWB-E1-001 | TC-E1-001-01 |
| REQ-RDF-002 | FEAT-RDF-01 | RWB-E1-001 | TC-E1-001-01 |
| REQ-RDF-003 | FEAT-RDF-01 | RWB-E1-001 | TC-E1-001-01 |
| REQ-RDF-004 | FEAT-RDF-01 | RWB-E1-001 | TC-E1-001-01 |
| REQ-RDF-005 | FEAT-RDF-01 | RWB-E1-001 | TC-E1-001-01 |
| REQ-RDF-006 | FEAT-RDF-01 | RWB-E1-001 | TC-E1-001-01 |
| REQ-RDF-007 | FEAT-RDF-01 | RWB-E1-001 | TC-E1-001-01 |
| REQ-RDF-008 | FEAT-RDF-01 | RWB-E1-001 | TC-E1-001-01 |
| REQ-RDF-009 | FEAT-RDF-01 | RWB-E1-001 | TC-E1-001-01 |
| REQ-RDF-010 | FEAT-RDF-01 | RWB-E1-001 | TC-E1-001-01 |
| REQ-RDF-011 | FEAT-RDF-01 | RWB-E1-001 | TC-E1-001-01 |
| REQ-RDF-012 | FEAT-RDF-01 | RWB-E1-001 | TC-E1-001-01 |
| REQ-RDF-013 | FEAT-RDF-01 | RWB-E1-001 | TC-E1-001-01 |
| REQ-RDF-014 | None | Written one epic ahead | With the story |

## Appendix T-A. API specification

### T-A.1 Endpoint inventory

| ID | Method | Path | Access | First in |
|---|---|---|---|---|
| API-P1-001 | GET | /api/recovery/v1/admin/jobs | Platform administration R | E1 |
| API-P1-002 | POST | /api/recovery/v1/admin/jobs/{jobId}/rerun | Platform administration U | E1 |
| API-P1-003 | GET | /api/recovery/v1/admin/data-quality/exceptions | Platform administration R | E1 |
| API-P1-004 | GET | /api/recovery/v1/admin/trackers | Reference data R | E1 |
| API-P1-005 | POST | /api/recovery/v1/admin/trackers/{trackerId}/loads | Reference data U | E1 |
| API-P1-006 | POST | /api/recovery/v1/admin/trackers/{trackerId}/sign-off | Queue and allocation A | E1 |
| API-P1-007 | POST | /api/recovery/v1/admin/trackers/{trackerId}/retire | Queue and allocation A | E1 |
| API-P1-008 | GET | /api/recovery/v1/admin/trackers/retirement-report | Reference data R | E1 |
| API-P1-009 | GET | /api/recovery/v1/data-products/freshness | Case record R | E1 |
| API-P1-010 | GET | /api/recovery/v1/data-products/{productCode}/records | Case record R | E1 |
| API-P1-011 | GET | /api/recovery/v1/admin/data-products | Platform administration R | E1 |
| API-P1-012 | GET | /api/recovery/v1/admin/data-dictionary/fields | Reference data R | E1 |
| API-P1-013 | PATCH | /api/recovery/v1/admin/data-dictionary/fields/{fieldCode} | Reference data U | E1 |
| API-P1-014 | GET | /api/recovery/v1/admin/data-contracts | Reference data R | E1 |
| API-P1-015 | PATCH | /api/recovery/v1/admin/data-contracts/{contractId} | Reference data U | E1 |
| API-P1-016 | POST | /api/recovery/v1/admin/data-contracts/{contractId}/publish | Reference data U | E1 |

### T-A.2 Endpoint detail

#### API-P1-001 GET /admin/jobs

| Item | Value |
|---|---|
| Purpose | List loads, files and jobs with status |
| Request | Query: type, status, from, to |
| Response | Job[] |
| Errors | 401, 403, 503 |
| Authorization | Platform administration, right R, scope applied |
| Idempotency | Not applicable |

#### API-P1-002 POST /admin/jobs/{jobId}/rerun

| Item | Value |
|---|---|
| Purpose | Rerun a failed load or job |
| Request | None |
| Response | Job |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Platform administration, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P1-003 GET /admin/data-quality/exceptions

| Item | Value |
|---|---|
| Purpose | List load check exceptions and reconciliation breaks |
| Request | Query: product, from, to |
| Response | DataQualityException[] |
| Errors | 401, 403, 503 |
| Authorization | Platform administration, right R, scope applied |
| Idempotency | Not applicable |

#### API-P1-004 GET /admin/trackers

| Item | Value |
|---|---|
| Purpose | List the tracker inventory with decision and status |
| Request | Query: team, decision, status |
| Response | Tracker[] |
| Errors | 401, 403, 503 |
| Authorization | Reference data, right R, scope applied |
| Idempotency | Not applicable |

#### API-P1-005 POST /admin/trackers/{trackerId}/loads

| Item | Value |
|---|---|
| Purpose | Upload and load a tracker file with a LOAD decision |
| Request | Multipart: file |
| Response | Job |
| Errors | 401, 403, 404, 409, 413, 415, 503 |
| Authorization | Reference data, right U, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P1-006 POST /admin/trackers/{trackerId}/sign-off

| Item | Value |
|---|---|
| Purpose | Confirm the tracker file row count against the load |
| Request | TrackerSignOff |
| Response | Tracker |
| Errors | 400, 401, 403, 404, 409, 503 |
| Authorization | Queue and allocation, right A, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P1-007 POST /admin/trackers/{trackerId}/retire

| Item | Value |
|---|---|
| Purpose | Confirm a tracker is replaced by the case list and record its archive location |
| Request | TrackerRetirement |
| Response | Tracker |
| Errors | 400, 401, 403, 404, 409, 503 |
| Authorization | Queue and allocation, right A, scope applied |
| Idempotency | Idempotency-Key header |

#### API-P1-008 GET /admin/trackers/retirement-report

| Item | Value |
|---|---|
| Purpose | Report tracker retirement per team for the business sign-off |
| Request | Query: asOf |
| Response | TrackerRetirementReport[] |
| Errors | 401, 403, 503 |
| Authorization | Reference data, right R, scope applied |
| Idempotency | Not applicable |

#### API-P1-009 GET /data-products/freshness

| Item | Value |
|---|---|
| Purpose | Read the freshness stamp of each data product |
| Request | Query: product, asOf |
| Response | DataProductFreshness[] |
| Errors | 400, 401, 403, 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

#### API-P1-010 GET /data-products/{productCode}/records

| Item | Value |
|---|---|
| Purpose | Read the rows of one data product for a case, masked by role, with its freshness stamp |
| Request | Query: caseId, page, size |
| Response | DataProductRecordPage |
| Errors | 400, 401, 403, 404, 503 |
| Authorization | Case record, right R, scope applied |
| Idempotency | Not applicable |

#### API-P1-011 GET /admin/data-products

| Item | Value |
|---|---|
| Purpose | List the data catalog entries |
| Request | Query: product |
| Response | DataProductCatalogEntry[] |
| Errors | 401, 403, 503 |
| Authorization | Platform administration, right R, scope applied |
| Idempotency | Not applicable |

#### API-P1-012 GET /admin/data-dictionary/fields

| Item | Value |
|---|---|
| Purpose | Search the data dictionary |
| Request | Query: product, entity, field, sourceSystem, page, size |
| Response | DataDictionaryFieldPage |
| Errors | 401, 403, 503 |
| Authorization | Reference data, right R, scope applied |
| Idempotency | Not applicable |

#### API-P1-013 PATCH /admin/data-dictionary/fields/{fieldCode}

| Item | Value |
|---|---|
| Purpose | Change a field definition with a reason, creating a new version |
| Request | DataDictionaryFieldChange |
| Response | DataDictionaryField |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Reference data, right U, scope applied |
| Idempotency | Not applicable |

#### API-P1-014 GET /admin/data-contracts

| Item | Value |
|---|---|
| Purpose | List data contracts per source system |
| Request | Query: sourceSystem, status |
| Response | DataContract[] |
| Errors | 401, 403, 503 |
| Authorization | Reference data, right R, scope applied |
| Idempotency | Not applicable |

#### API-P1-015 PATCH /admin/data-contracts/{contractId}

| Item | Value |
|---|---|
| Purpose | Record the system owner's confirmation of a data contract |
| Request | DataContractConfirmation |
| Response | DataContract |
| Errors | 401, 403, 404, 409, 422, 503 |
| Authorization | Reference data, right U, scope applied |
| Idempotency | Not applicable |

#### API-P1-016 POST /admin/data-contracts/{contractId}/publish

| Item | Value |
|---|---|
| Purpose | Publish a confirmed data contract |
| Request | None |
| Response | DataContract |
| Errors | 401, 403, 404, 409, 503 |
| Authorization | Reference data, right U, scope applied |
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

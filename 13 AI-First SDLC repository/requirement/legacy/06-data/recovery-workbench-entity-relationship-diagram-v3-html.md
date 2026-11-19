<!-- source: 06 Data/Recovery Workbench Entity Relationship Diagram v3.html -->
<!-- converted: 2026-11-04 from HTML -->

> **Source:** `06 Data/Recovery Workbench Entity Relationship Diagram v3.html`  
> **Converted from:** HTML

Recovery Workbench Entity Relationship Diagram

## Data products and the references between them

108 entities in 14 data products, with 119 relationships. Each line joins two data products, with the number of references between them; the dot is at the referring end. Case and ownership is shaded. Each data product has its own tab with every attribute.

**Entities**108**Relationships**119**Mandatory references**56**Optional references**63

## DP01 Account and arrears

Loan accounts with balances, interest, fees, days past due, bucket, classification, restructure flag and payments

**System of record**Core bank (ALS)**How it reaches the Workbench**COLLINS daily batch into the ACE database**Freshness**End of day; in the Workbench the next morning

References from other data products to these entities are on the tabs of those products and on the overview.

### Relationships

| Entity | Foreign key | Refers to | Reference |
|---|---|---|---|
| account_payment | account_id | loan_account | Mandatory |

## DP02 Customer and party

Customers, guarantors, co-borrowers and heirs, tokenized identifiers, contact points, consent and flags for vulnerability, death and bankruptcy

**System of record**SCBPDM and core bank**How it reaches the Workbench**COLLINS daily batch into the ACE database**Freshness**End of day; in the Workbench the next morning

References from other data products to these entities are on the tabs of those products and on the overview.

### Relationships

| Entity | Foreign key | Refers to | Reference |
|---|---|---|---|
| contact_point | party_id | party | Mandatory |
| party_product | party_id | party | Mandatory |

## DP03 Case and ownership

The case, its accounts and parties, status, stage, route, owner, queue, tasks, timers and deviations

**System of record**Recovery Workbench**How it reaches the Workbench**Held in the Workbench**Freshness**As it changes

References from other data products to these entities are on the tabs of those products and on the overview.

### Relationships

| Entity | Foreign key | Refers to | Reference |
|---|---|---|---|
| recovery_case | primary_customer_id | party | Mandatory |
| recovery_case | queue_id | queue | Optional |
| case_account | case_id | recovery_case | Mandatory |
| case_account | account_id | loan_account | Mandatory |
| case_party | case_id | recovery_case | Mandatory |
| case_party | party_id | party | Mandatory |
| deviation | case_id | recovery_case | Mandatory |
| queue | overflow_queue_id | queue | Optional |
| assignment | case_id | recovery_case | Mandatory |
| assignment | task_id | task | Optional |
| assignment | queue_id | queue | Optional |
| task | case_id | recovery_case | Mandatory |
| timer | case_id | recovery_case | Mandatory |
| timer | task_id | task | Optional |
| timer | treatment_id | treatment | Optional |
| case_list_row | case_id | recovery_case | Mandatory |
| case_list_row | account_id | loan_account | Mandatory |
| case_entry_exclusion | account_id | loan_account | Mandatory |
| queue_member | queue_id | queue | Mandatory |
| queue_measure | queue_id | queue | Mandatory |

## DP04 Treatment and offers

Restructures, settlements, deeds in lieu, buy-backs and guarantee claims, with terms, approval level and outcome

**System of record**Recovery Workbench; restructure plans in ACE**How it reaches the Workbench**Held in the Workbench**Freshness**As it changes

References from other data products to these entities are on the tabs of those products and on the overview.

### Relationships

| Entity | Foreign key | Refers to | Reference |
|---|---|---|---|
| treatment | case_id | recovery_case | Mandatory |
| treatment | decision_log_id | decision_log_entry | Optional |
| guarantee_claim | case_id | recovery_case | Mandatory |
| dp_treatment | treatment_id | treatment | Mandatory |
| dp_treatment | case_id | recovery_case | Mandatory |
| dp_treatment | decision_log_id | decision_log_entry | Optional |
| dp_guarantee_claim | guarantee_claim_id | guarantee_claim | Mandatory |
| dp_guarantee_claim | case_id | recovery_case | Mandatory |

## DP05 Contact and promises

Every contact, letter, promise and hand-over on the case, in order, including the collections history from EFS

**System of record**EFS before day 90; the Workbench after**How it reaches the Workbench**COLLINS daily batch from EFS; held in the Workbench**Freshness**End of day for EFS history; as it changes after

References from other data products to these entities are on the tabs of those products and on the overview.

### Relationships

| Entity | Foreign key | Refers to | Reference |
|---|---|---|---|
| interaction | case_id | recovery_case | Mandatory |
| interaction | party_id | party | Optional |
| interaction | decision_log_id | decision_log_entry | Optional |
| interaction | corrects_entry_id | interaction | Optional |
| interaction | contact_point_id | contact_point | Optional |
| interaction | treatment_id | treatment | Optional |
| interaction | proceeds_id | proceeds | Optional |

## DP06 Collateral and assets

Collateral, appraisals, assets held after repossession or transfer, listings and sale results

**System of record**CCMS, SVAF, AMIS, RPS**How it reaches the Workbench**File load until a batch feed exists**Freshness**Weekly or monthly today

References from other data products to these entities are on the tabs of those products and on the overview.

### Relationships

| Entity | Foreign key | Refers to | Reference |
|---|---|---|---|
| account_collateral | account_id | loan_account | Mandatory |
| account_collateral | collateral_id | collateral | Mandatory |
| valuation | collateral_id | collateral | Optional |
| valuation | asset_id | asset | Optional |
| valuation | valuer_partner_id | partner | Optional |
| asset | case_id | recovery_case | Optional |
| asset | collateral_id | collateral | Optional |
| listing | asset_id | asset | Mandatory |
| asset_sale | asset_id | asset | Mandatory |
| asset_sale | listing_id | listing | Optional |

## DP07 Legal events and cases

Notices and proof of delivery, lawsuits, court case numbers, hearings, judgments and enforcement

**System of record**LIT for court records; the Workbench for instructions**How it reaches the Workbench**COLLINS daily batch for litigation status; held in the Workbench**Freshness**End of day for LIT status

References from other data products to these entities are on the tabs of those products and on the overview.

### Relationships

| Entity | Foreign key | Refers to | Reference |
|---|---|---|---|
| legal_action | case_id | recovery_case | Mandatory |
| legal_action | law_firm_id | partner | Optional |
| notice | case_id | recovery_case | Mandatory |
| notice | document_id | document | Optional |
| notice | party_id | party | Optional |
| notice | template_id | template | Optional |
| notice | dispatch_file_id | outbound_item | Optional |
| hearing | legal_action_id | legal_action | Mandatory |

## DP08 Partner performance

Partners on the panel, work placed with each, results, fees and scorecards

**System of record**Recovery Workbench**How it reaches the Workbench**Held in the Workbench; partner results through the partner portal**Freshness**As it changes

References from other data products to these entities are on the tabs of those products and on the overview.

### Relationships

| Entity | Foreign key | Refers to | Reference |
|---|---|---|---|
| partner_instruction | case_id | recovery_case | Mandatory |
| partner_instruction | partner_id | partner | Mandatory |

## DP09 Debt sale

Debt sale lots, the accounts in each lot, buyers, prices, approval and put-backs

**System of record**Recovery Workbench**How it reaches the Workbench**Held in the Workbench**Freshness**As it changes

References from other data products to these entities are on the tabs of those products and on the overview.

### Relationships

| Entity | Foreign key | Refers to | Reference |
|---|---|---|---|
| debt_sale_lot | buyer_partner_id | partner | Optional |
| debt_sale_account | lot_id | debt_sale_lot | Mandatory |
| debt_sale_account | account_id | loan_account | Mandatory |

## DP10 Documents and extracted fields

Documents against the case, the fields read from them, retention class and custody of originals

**System of record**Recovery Workbench document hub**How it reaches the Workbench**Held in the Workbench**Freshness**As it changes

References from other data products to these entities are on the tabs of those products and on the overview.

### Relationships

| Entity | Foreign key | Refers to | Reference |
|---|---|---|---|
| document | case_id | recovery_case | Mandatory |
| document | party_id | party | Optional |
| document | previous_version_id | document | Optional |
| document | template_id | template | Optional |
| document | treatment_id | treatment | Optional |
| document_field | document_id | document | Mandatory |
| document_custody | document_id | document | Mandatory |
| case_document_check | case_id | recovery_case | Mandatory |
| case_document_check | last_event_id | outbox_event | Optional |
| document_intake | partner_id | partner | Optional |
| document_intake | run_id | load_run | Optional |
| document_intake | case_id | recovery_case | Optional |
| document_intake | document_id | document | Optional |
| document_text | intake_id | document_intake | Mandatory |
| document_text | document_id | document | Optional |
| retention_action | document_id | document | Mandatory |
| retention_action | decision_log_id | decision_log_entry | Optional |
| signature_request | case_id | recovery_case | Mandatory |
| signature_request | treatment_id | treatment | Optional |
| signature_request | document_id | document | Mandatory |
| signature_request | party_id | party | Mandatory |
| signature_request | signed_document_id | document | Optional |

## DP11 Scores and route economics

Risk scores, expected return by route, estimated sale price and sale success rate, restructure scheme suggestions

**System of record**COLLINS**How it reaches the Workbench**COLLINS daily batch into the ACE database**Freshness**End of day; monthly for some models

References from other data products to these entities are on the tabs of those products and on the overview.

### Relationships

| Entity | Foreign key | Refers to | Reference |
|---|---|---|---|
| score | account_id | loan_account | Optional |
| score | case_id | recovery_case | Optional |

## DP12 Decision log

One entry per decision with the rule, model and agent versions, inputs, recommendation, approval, actions and outcome

**System of record**Recovery Workbench**How it reaches the Workbench**Held in the Workbench**Freshness**As it changes

References from other data products to these entities are on the tabs of those products and on the overview.

### Relationships

| Entity | Foreign key | Refers to | Reference |
|---|---|---|---|
| decision_log_entry | case_id | recovery_case | Optional |
| decision_log_entry | corrects_entry_id | decision_log_entry | Optional |
| approval | case_id | recovery_case | Mandatory |
| approval | delegation_limit_id | delegation_limit | Optional |
| approval | decision_log_id | decision_log_entry | Optional |

## DP13 Money and closure

Payments and proceeds matched to the case, write-off postings and recovery after charge-off

**System of record**Core bank (ALS) and GL**How it reaches the Workbench**COLLINS daily batch for payments; file load for GL**Freshness**End of day for payments; monthly for GL

References from other data products to these entities are on the tabs of those products and on the overview.

### Relationships

| Entity | Foreign key | Refers to | Reference |
|---|---|---|---|
| proceeds | case_id | recovery_case | Mandatory |
| proceeds | treatment_id | treatment | Optional |
| proceeds | account_payment_id | account_payment | Optional |
| write_off | case_id | recovery_case | Mandatory |
| write_off | decision_log_id | decision_log_entry | Optional |

## DP14 Reference data

Rules, approval limits, lists of values, roles, permissions and letter templates, each versioned

**System of record**Recovery Workbench**How it reaches the Workbench**Held in the Workbench**Freshness**By versioned load

References from other data products to these entities are on the tabs of those products and on the overview.

### Relationships

| Entity | Foreign key | Refers to | Reference |
|---|---|---|---|
| permission | role_id | role | Mandatory |
| retention_rule | reference_version_id | reference_version | Optional |
| reference_row | version_id | reference_version | Mandatory |
| partner_user | partner_id | partner | Mandatory |
| document_type | reference_version_id | reference_version | Optional |
| document_checklist_item | reference_version_id | reference_version | Optional |
| document_hub_parameter | reference_version_id | reference_version | Optional |

## OPS Loads and operations

Loads, interfaces, data quality, jobs, feature flags, the outbox and idempotency records that run the Workbench

**System of record**Recovery Workbench**How it reaches the Workbench**Held in the Workbench**Freshness**As it changes

References from other data products to these entities are on the tabs of those products and on the overview.

### Relationships

| Entity | Foreign key | Refers to | Reference |
|---|---|---|---|
| load_run | interface_run_id | interface_run | Optional |
| load_run | tracker_id | tracker_inventory | Optional |
| dq_exception | load_run_id | load_run | Mandatory |
| tracker_inventory | last_load_run_id | load_run | Optional |
| tracker_row | tracker_id | tracker_inventory | Mandatory |
| tracker_row | load_run_id | load_run | Mandatory |
| processed_event | event_id | outbox_event | Optional |
| outbox_event | case_id | recovery_case | Optional |
| outbox_delivery | event_id | outbox_event | Mandatory |
| outbox_delivery | task_id | task | Optional |

## AGT Agent runtime

Agent policies, prompts, runs, labeled samples, evaluations, feedback and alerts

**System of record**Recovery Workbench**How it reaches the Workbench**Held in the Workbench**Freshness**As it changes

References from other data products to these entities are on the tabs of those products and on the overview.

### Relationships

| Entity | Foreign key | Refers to | Reference |
|---|---|---|---|
| agent_policy | evaluation_run_id | agent_evaluation_run | Optional |
| agent_run | case_id | recovery_case | Optional |
| agent_run | evaluation_run_id | agent_evaluation_run | Optional |
| agent_run | decision_log_id | decision_log_entry | Optional |
| agent_evaluation | evaluation_run_id | agent_evaluation_run | Mandatory |
| agent_feedback | agent_run_id | agent_run | Mandatory |
| agent_feedback | decision_log_id | decision_log_entry | Optional |

## RPT Reporting

Measure definitions and the snapshots published to Power BI

**System of record**Recovery Workbench**How it reaches the Workbench**Held in the Workbench**Freshness**Daily

References from other data products to these entities are on the tabs of those products and on the overview.

### Relationships

| Entity | Foreign key | Refers to | Reference |
|---|---|---|---|

## All 119 relationships

| Entity | Foreign key | Refers to | Cardinality | Reference | Data product of the entity |
|---|---|---|---|---|---|
| recovery_case | primary_customer_id | party | Zero, one or more to one | Mandatory | DP03 |
| recovery_case | queue_id | queue | Zero, one or more to zero or one | Optional | DP03 |
| case_account | case_id | recovery_case | Zero, one or more to one | Mandatory | DP03 |
| case_account | account_id | loan_account | Zero, one or more to one | Mandatory | DP03 |
| case_party | case_id | recovery_case | Zero, one or more to one | Mandatory | DP03 |
| case_party | party_id | party | Zero, one or more to one | Mandatory | DP03 |
| deviation | case_id | recovery_case | Zero, one or more to one | Mandatory | DP03 |
| queue | overflow_queue_id | queue | Zero, one or more to zero or one | Optional | DP03 |
| assignment | case_id | recovery_case | Zero, one or more to one | Mandatory | DP03 |
| assignment | task_id | task | Zero, one or more to zero or one | Optional | DP03 |
| assignment | queue_id | queue | Zero, one or more to zero or one | Optional | DP03 |
| task | case_id | recovery_case | Zero, one or more to one | Mandatory | DP03 |
| timer | case_id | recovery_case | Zero, one or more to one | Mandatory | DP03 |
| timer | task_id | task | Zero, one or more to zero or one | Optional | DP03 |
| timer | treatment_id | treatment | Zero, one or more to zero or one | Optional | DP03 |
| contact_point | party_id | party | Zero, one or more to one | Mandatory | DP02 |
| account_payment | account_id | loan_account | Zero, one or more to one | Mandatory | DP01 |
| account_collateral | account_id | loan_account | Zero, one or more to one | Mandatory | DP06 |
| account_collateral | collateral_id | collateral | Zero, one or more to one | Mandatory | DP06 |
| valuation | collateral_id | collateral | Zero, one or more to zero or one | Optional | DP06 |
| valuation | asset_id | asset | Zero, one or more to zero or one | Optional | DP06 |
| valuation | valuer_partner_id | partner | Zero, one or more to zero or one | Optional | DP06 |
| asset | case_id | recovery_case | Zero, one or more to zero or one | Optional | DP06 |
| asset | collateral_id | collateral | Zero, one or more to zero or one | Optional | DP06 |
| treatment | case_id | recovery_case | Zero, one or more to one | Mandatory | DP04 |
| treatment | decision_log_id | decision_log_entry | Zero, one or more to zero or one | Optional | DP04 |
| guarantee_claim | case_id | recovery_case | Zero, one or more to one | Mandatory | DP04 |
| legal_action | case_id | recovery_case | Zero, one or more to one | Mandatory | DP07 |
| legal_action | law_firm_id | partner | Zero, one or more to zero or one | Optional | DP07 |
| notice | case_id | recovery_case | Zero, one or more to one | Mandatory | DP07 |
| notice | document_id | document | Zero, one or more to zero or one | Optional | DP07 |
| notice | party_id | party | Zero, one or more to zero or one | Optional | DP07 |
| notice | template_id | template | Zero, one or more to zero or one | Optional | DP07 |
| notice | dispatch_file_id | outbound_item | Zero, one or more to zero or one | Optional | DP07 |
| hearing | legal_action_id | legal_action | Zero, one or more to one | Mandatory | DP07 |
| partner_instruction | case_id | recovery_case | Zero, one or more to one | Mandatory | DP08 |
| partner_instruction | partner_id | partner | Zero, one or more to one | Mandatory | DP08 |
| listing | asset_id | asset | Zero, one or more to one | Mandatory | DP06 |
| asset_sale | asset_id | asset | Zero, one or more to one | Mandatory | DP06 |
| asset_sale | listing_id | listing | Zero, one or more to zero or one | Optional | DP06 |
| debt_sale_lot | buyer_partner_id | partner | Zero, one or more to zero or one | Optional | DP09 |
| debt_sale_account | lot_id | debt_sale_lot | Zero, one or more to one | Mandatory | DP09 |
| debt_sale_account | account_id | loan_account | Zero, one or more to one | Mandatory | DP09 |
| interaction | case_id | recovery_case | Zero, one or more to one | Mandatory | DP05 |
| interaction | party_id | party | Zero, one or more to zero or one | Optional | DP05 |
| interaction | decision_log_id | decision_log_entry | Zero, one or more to zero or one | Optional | DP05 |
| interaction | corrects_entry_id | interaction | Zero, one or more to zero or one | Optional | DP05 |
| interaction | contact_point_id | contact_point | Zero, one or more to zero or one | Optional | DP05 |
| interaction | treatment_id | treatment | Zero, one or more to zero or one | Optional | DP05 |
| interaction | proceeds_id | proceeds | Zero, one or more to zero or one | Optional | DP05 |
| document | case_id | recovery_case | Zero, one or more to one | Mandatory | DP10 |
| document | party_id | party | Zero, one or more to zero or one | Optional | DP10 |
| document | previous_version_id | document | Zero, one or more to zero or one | Optional | DP10 |
| document | template_id | template | Zero, one or more to zero or one | Optional | DP10 |
| document | treatment_id | treatment | Zero, one or more to zero or one | Optional | DP10 |
| document_field | document_id | document | Zero, one or more to one | Mandatory | DP10 |
| document_custody | document_id | document | Zero, one or more to one | Mandatory | DP10 |
| decision_log_entry | case_id | recovery_case | Zero, one or more to zero or one | Optional | DP12 |
| decision_log_entry | corrects_entry_id | decision_log_entry | Zero, one or more to zero or one | Optional | DP12 |
| score | account_id | loan_account | Zero, one or more to zero or one | Optional | DP11 |
| score | case_id | recovery_case | Zero, one or more to zero or one | Optional | DP11 |
| proceeds | case_id | recovery_case | Zero, one or more to one | Mandatory | DP13 |
| proceeds | treatment_id | treatment | Zero, one or more to zero or one | Optional | DP13 |
| proceeds | account_payment_id | account_payment | Zero, one or more to zero or one | Optional | DP13 |
| write_off | case_id | recovery_case | Zero, one or more to one | Mandatory | DP13 |
| write_off | decision_log_id | decision_log_entry | Zero, one or more to zero or one | Optional | DP13 |
| permission | role_id | role | Zero, one or more to one | Mandatory | DP14 |
| load_run | interface_run_id | interface_run | Zero, one or more to zero or one | Optional | OPS |
| load_run | tracker_id | tracker_inventory | Zero, one or more to zero or one | Optional | OPS |
| dq_exception | load_run_id | load_run | Zero, one or more to one | Mandatory | OPS |
| tracker_inventory | last_load_run_id | load_run | Zero, one or more to zero or one | Optional | OPS |
| tracker_row | tracker_id | tracker_inventory | Zero, one or more to one | Mandatory | OPS |
| tracker_row | load_run_id | load_run | Zero, one or more to one | Mandatory | OPS |
| case_list_row | case_id | recovery_case | Zero, one or more to one | Mandatory | DP03 |
| case_list_row | account_id | loan_account | Zero, one or more to one | Mandatory | DP03 |
| retention_rule | reference_version_id | reference_version | Zero, one or more to zero or one | Optional | DP14 |
| dp_treatment | treatment_id | treatment | Zero, one or more to one | Mandatory | DP04 |
| dp_treatment | case_id | recovery_case | Zero, one or more to one | Mandatory | DP04 |
| dp_treatment | decision_log_id | decision_log_entry | Zero, one or more to zero or one | Optional | DP04 |
| dp_guarantee_claim | guarantee_claim_id | guarantee_claim | Zero, one or more to one | Mandatory | DP04 |
| dp_guarantee_claim | case_id | recovery_case | Zero, one or more to one | Mandatory | DP04 |
| processed_event | event_id | outbox_event | Zero, one or more to zero or one | Optional | OPS |
| outbox_event | case_id | recovery_case | Zero, one or more to zero or one | Optional | OPS |
| outbox_delivery | event_id | outbox_event | Zero, one or more to one | Mandatory | OPS |
| outbox_delivery | task_id | task | Zero, one or more to zero or one | Optional | OPS |
| party_product | party_id | party | Zero, one or more to one | Mandatory | DP02 |
| case_entry_exclusion | account_id | loan_account | Zero, one or more to one | Mandatory | DP03 |
| queue_member | queue_id | queue | Zero, one or more to one | Mandatory | DP03 |
| queue_measure | queue_id | queue | Zero, one or more to one | Mandatory | DP03 |
| reference_row | version_id | reference_version | Zero, one or more to one | Mandatory | DP14 |
| partner_user | partner_id | partner | Zero, one or more to one | Mandatory | DP14 |
| document_type | reference_version_id | reference_version | Zero, one or more to zero or one | Optional | DP14 |
| document_checklist_item | reference_version_id | reference_version | Zero, one or more to zero or one | Optional | DP14 |
| case_document_check | case_id | recovery_case | Zero, one or more to one | Mandatory | DP10 |
| case_document_check | last_event_id | outbox_event | Zero, one or more to zero or one | Optional | DP10 |
| document_hub_parameter | reference_version_id | reference_version | Zero, one or more to zero or one | Optional | DP14 |
| document_intake | partner_id | partner | Zero, one or more to zero or one | Optional | DP10 |
| document_intake | run_id | load_run | Zero, one or more to zero or one | Optional | DP10 |
| document_intake | case_id | recovery_case | Zero, one or more to zero or one | Optional | DP10 |
| document_intake | document_id | document | Zero, one or more to zero or one | Optional | DP10 |
| document_text | intake_id | document_intake | Zero, one or more to one | Mandatory | DP10 |
| document_text | document_id | document | Zero, one or more to zero or one | Optional | DP10 |
| retention_action | document_id | document | Zero, one or more to one | Mandatory | DP10 |
| retention_action | decision_log_id | decision_log_entry | Zero, one or more to zero or one | Optional | DP10 |
| signature_request | case_id | recovery_case | Zero, one or more to one | Mandatory | DP10 |
| signature_request | treatment_id | treatment | Zero, one or more to zero or one | Optional | DP10 |
| signature_request | document_id | document | Zero, one or more to one | Mandatory | DP10 |
| signature_request | party_id | party | Zero, one or more to one | Mandatory | DP10 |
| signature_request | signed_document_id | document | Zero, one or more to zero or one | Optional | DP10 |
| approval | case_id | recovery_case | Zero, one or more to one | Mandatory | DP12 |
| approval | delegation_limit_id | delegation_limit | Zero, one or more to zero or one | Optional | DP12 |
| approval | decision_log_id | decision_log_entry | Zero, one or more to zero or one | Optional | DP12 |
| agent_policy | evaluation_run_id | agent_evaluation_run | Zero, one or more to zero or one | Optional | AGT |
| agent_run | case_id | recovery_case | Zero, one or more to zero or one | Optional | AGT |
| agent_run | evaluation_run_id | agent_evaluation_run | Zero, one or more to zero or one | Optional | AGT |
| agent_run | decision_log_id | decision_log_entry | Zero, one or more to zero or one | Optional | AGT |
| agent_evaluation | evaluation_run_id | agent_evaluation_run | Zero, one or more to one | Mandatory | AGT |
| agent_feedback | agent_run_id | agent_run | Zero, one or more to one | Mandatory | AGT |
| agent_feedback | decision_log_id | decision_log_entry | Zero, one or more to zero or one | Optional | AGT |

## IDEF1X notation

The diagrams use the IDEF1X notation for entities, keys and relationships.

| Symbol | Meaning |
|---|---|
| Square-cornered box | An independent entity. Its key does not depend on any other entity. Every entity in this model is independent |
| Name above the box | The entity name as it is held in the ACE database |
| Line inside the box | Above the line is the primary key. Below it are the other attributes |
| (FK) | A foreign key: a reference to another entity |
| (AK1) | An alternate key: unique on its own or together with the other AK1 attributes of the entity |
| Dashed line | A non-identifying relationship. The child refers to the parent, and the child's key does not include it |
| Filled dot | The child end of the relationship: zero, one or more child records |
| Open diamond | At the parent end: the reference is optional, so a child may have no parent |
| No diamond | At the parent end: the reference is mandatory, so every child has exactly one parent |
| Label on the line | The foreign key attribute that carries the relationship |
| Dashed grey box | An entity from another data product, shown with its key only |

<!-- source: 06 Data/Recovery Workbench Entity Relationship Diagram v5.html -->
<!-- converted: 2026-11-16 from HTML -->

> **Source:** `06 Data/Recovery Workbench Entity Relationship Diagram v5.html`  
> **Converted from:** HTML

Recovery Workbench Entity Relationship Diagram

## The ACE boundary and the references between data products

123 objects: 89 Workbench tables, 4 extension tables and 30 ACE source views, with 108 references. The 14 data products hold 98 of them; OPS, AGT and RPT hold the other 25. The views are external and read only, and their boxes are dashed. The 18 business-key links carry no foreign key into ACE; the other 90 references are ordinary foreign keys inside the recovery schema.

**Objects**123**Workbench tables**89**Extension tables**4**ACE views, read only**30**References**108**Business-key links**18

### Data products

| ID | Data product | Objects | Tables | Extension | Views | System of record |
|---|---|---|---|---|---|---|
| DP01 | Account and arrears | 5 | 0 | 1 | 4 | ACE (ingested from ALS) |
| DP02 | Customer and party | 6 | 0 | 2 | 4 | ACE (ingested from SCBPDM and the core bank) |
| DP03 | Case and ownership | 12 | 12 | 0 | 0 | Recovery Workbench |
| DP04 | Treatment and offers | 6 | 4 | 0 | 2 | Recovery Workbench for the treatment; ACE (ingested from the core bank) for the restructure plan |
| DP05 | Contact and promises | 3 | 1 | 0 | 2 | ACE (ingested from EFS) |
| DP06 | Collateral and assets | 9 | 2 | 1 | 6 | ACE (ingested from CCMS, SVAF, AMIS and RPS) |
| DP07 | Legal events and cases | 6 | 3 | 0 | 3 | ACE (ingested from LIT and WIN) for the court record and the proof of delivery; Workbench for notices and enforcement |
| DP08 | Partner performance | 2 | 2 | 0 | 0 | Recovery Workbench |
| DP09 | Debt sale | 2 | 2 | 0 | 0 | Recovery Workbench |
| DP10 | Documents and extracted fields | 9 | 8 | 0 | 1 | Recovery Workbench document hub |
| DP11 | Scores and route economics | 1 | 0 | 0 | 1 | ACE (ingested from COLLINS) |
| DP12 | Decision log | 2 | 2 | 0 | 0 | Recovery Workbench |
| DP13 | Money and closure | 3 | 2 | 0 | 1 | ACE (ingested from ALS and GL) |
| DP14 | Reference data | 32 | 27 | 0 | 5 | Recovery Workbench |
| OPS | Loads and operations | 14 | 13 | 0 | 1 | Recovery Workbench; ACE for the batch record |
| AGT | Agent runtime | 8 | 8 | 0 | 0 | Recovery Workbench |
| RPT | Reporting | 3 | 3 | 0 | 0 | Recovery Workbench |

### References between data products

54 references cross a data product boundary and 54 stay inside one. Each row reads from the first data product to the second, and is ordered by count.

| Data product | Refers to | References | Mandatory | Business key |
|---|---|---|---|---|
| DP03 | DP04 | 5 | 4 | 0 |
| DP03 | DP10 | 4 | 3 | 0 |
| DP01 | DP03 | 3 | 3 | 3 |
| AGT | DP12 | 2 | 0 | 0 |
| DP02 | DP03 | 2 | 2 | 2 |
| DP02 | DP05 | 2 | 0 | 2 |
| DP02 | DP10 | 2 | 1 | 2 |
| DP03 | DP07 | 2 | 2 | 0 |
| DP03 | DP12 | 2 | 1 | 0 |
| DP03 | DP13 | 2 | 2 | 0 |
| DP03 | OPS | 2 | 0 | 0 |
| DP04 | DP10 | 2 | 0 | 0 |
| DP04 | DP12 | 2 | 0 | 0 |
| AGT | DP03 | 1 | 0 | 0 |
| DP01 | DP09 | 1 | 1 | 1 |
| DP01 | DP13 | 1 | 0 | 1 |
| DP02 | DP07 | 1 | 0 | 1 |
| DP03 | DP05 | 1 | 1 | 0 |
| DP03 | DP08 | 1 | 1 | 0 |
| DP04 | DP05 | 1 | 0 | 0 |
| DP04 | DP13 | 1 | 0 | 0 |
| DP05 | DP12 | 1 | 0 | 0 |
| DP05 | DP13 | 1 | 0 | 0 |
| DP07 | DP08 | 1 | 0 | 0 |
| DP07 | DP10 | 1 | 0 | 0 |
| DP07 | DP14 | 1 | 0 | 0 |
| DP07 | OPS | 1 | 0 | 0 |
| DP08 | DP09 | 1 | 0 | 0 |
| DP08 | DP10 | 1 | 0 | 0 |
| DP08 | DP14 | 1 | 1 | 0 |
| DP10 | DP12 | 1 | 0 | 0 |
| DP10 | DP14 | 1 | 0 | 0 |
| DP10 | OPS | 1 | 0 | 0 |
| DP12 | DP13 | 1 | 0 | 0 |
| DP12 | DP14 | 1 | 0 | 0 |

## DP01 Account and arrears

Loan accounts with balances, interest, fees, days past due, bucket, classification, restructure flag and payments

**System of record**ACE (ingested from ALS)**How it reaches the Workbench**Read through recovery.v_ace_account, v_ace_payment, v_ace_aa_relation and v_ace_bucket_log. ACE ingests ALS daily; the Workbench loads nothing.**Freshness**ACE end of day; the views carry the ACE business date**Objects**5

### Objects

| account_key | PK, BK |
|---|---|
| dispute_open |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| account_key | BK |
|---|---|
| account_code |  |
| account_name |  |
| account_status |  |
| account_status_date |  |
| contract_no |  |
| contract_date |  |
| product_key |  |
| product_type |  |
| product_category |  |
| product_category_efs |  |
| branch_code |  |
| branch_name |  |
| oc_code |  |
| company_code |  |
| collection_officer |  |
| collection_phase |  |
| days_past_due |  |
| classification |  |
| total_balance |  |
| accounting_balance |  |
| past_due_amount |  |
| total_interest_fin_charge |  |
| collections_fee |  |
| interest_rate |  |
| last_payment_date |  |
| last_payment_amount |  |
| next_installment_date |  |
| next_installment_amount |  |
| last_tdr_date |  |
| tdr_flag |  |
| rescheduled_flag |  |
| number_reschedules |  |
| tdr_aging |  |
| principle_not_reduce |  |
| data_as_of |  |
| days_since_last_contact |  |
| days_since_last_collection_activity |  |
| relationship_manager |  |
| relationship_manager_phone |  |
| special_memo |  |
| expiry_date |  |
| business_unit | B |
| principal_outstanding | B |
| interest_outstanding | B |
| fees_outstanding | B |
| daily_bucket | B |
| settlement_booked_date | B |
| settlement_booked_amount | B |

| payment_code | BK |
|---|---|
| account_key | BK |
| payment_date |  |
| payment_amount |  |
| capital_amount |  |
| interest_amount |  |
| expense_amount |  |
| commission_amount |  |
| payment_channel |  |
| description |  |
| comments |  |
| data_as_of |  |

| parent_account_key |  |
|---|---|
| child_account_key |  |

| account_key | BK |
|---|---|
| snapshot_year |  |
| snapshot_month |  |
| bucket |  |
| past_due_amount |  |
| snapshot_month_start |  |

### References

| Entity | Field | Refers to | Reference | Kind |
|---|---|---|---|---|
| case_account | account_key | v_ace_account | Mandatory | Business key, no foreign key |
| debt_sale_account | account_key | v_ace_account | Mandatory | Business key, no foreign key |
| proceeds | payment_code | v_ace_payment | Optional | Business key, no foreign key |
| case_list_row | account_key | v_ace_account | Mandatory | Business key, no foreign key |
| case_entry_exclusion | account_key | v_ace_account | Mandatory | Business key, no foreign key |
| account_ext | account_key | v_ace_account | Mandatory | Business key, no foreign key (1:1 extension) |

## DP02 Customer and party

Customers, guarantors, co-borrowers and heirs, identity masked to the last four, contact points, consent and flags for vulnerability, death and bankruptcy

**System of record**ACE (ingested from SCBPDM and the core bank)**How it reaches the Workbench**Read through recovery.v_ace_customer, v_ace_contact, v_ace_ca_relation and v_ace_party_product. The Workbench holds only its own flags and consent in party_ext and contact_point_ext.**Freshness**ACE end of day; consent and flags as they change in the Workbench**Objects**6

### Objects

| person_key | PK, BK |
|---|---|
| vulnerable |  |
| deceased_override |  |
| bankruptcy |  |
| fraud_flag |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| contact_key | PK, BK |
|---|---|
| contact_type |  |
| consent_given |  |
| consent_at |  |
| verified_at |  |
| failed_count |  |
| source |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| cif_no |  |
|---|---|
| person_key | BK |
| first_name |  |
| last_name |  |
| date_of_birth |  |
| deceased_date |  |
| deceased_flag |  |
| gender |  |
| nationality |  |
| marital_status |  |
| occupation |  |
| spouse_name |  |
| customer_status |  |
| category |  |
| country_of_residence |  |
| is_staff |  |
| branch_code |  |
| vat_number |  |
| id_no_masked |  |
| id_no_last4 |  |
| party_type | B |
| id_type | B |
| segment | B |

| contact_type |  |
|---|---|
| contact_key | BK |
| person_key | BK |
| contact_value |  |
| contact_value_masked |  |
| usage_code |  |
| city |  |
| post_code |  |
| country |  |

| person_key | BK |
|---|---|
| account_key | BK |
| relation_type |  |
| amount_of_guarantee |  |
| date_of_guarantee |  |

| person_key | BK |
|---|---|
| account_no |  |
| account_key | BK |
| product_type |  |
| product_status |  |
| data_as_of |  |

### References

| Entity | Field | Refers to | Reference | Kind |
|---|---|---|---|---|
| recovery_case | primary_person_key | v_ace_customer | Mandatory | Business key, no foreign key |
| case_party | person_key | v_ace_customer | Mandatory | Business key, no foreign key |
| notice | person_key | v_ace_customer | Optional | Business key, no foreign key |
| interaction | person_key | v_ace_customer | Optional | Business key, no foreign key |
| interaction | contact_key | v_ace_contact | Optional | Business key, no foreign key |
| document | person_key | v_ace_customer | Optional | Business key, no foreign key |
| signature_request | person_key | v_ace_customer | Mandatory | Business key, no foreign key |
| party_ext | person_key | v_ace_customer | Mandatory | Business key, no foreign key (1:1 extension) |
| contact_point_ext | contact_key | v_ace_contact | Mandatory | Business key, no foreign key (1:1 extension) |

## DP03 Case and ownership

The case, its accounts and parties, status, stage, route, owner, queue, tasks, timers and deviations

**System of record**Recovery Workbench**How it reaches the Workbench**Held in the Workbench. Accounts and parties are linked by ACE business key to v_ace_account and v_ace_customer; no foreign key.**Freshness**As it changes**Objects**12

### Objects

| id | PK |
|---|---|
| case_no | AK1 |
| product_group |  |
| primary_person_key | BK |
| status |  |
| stage_code |  |
| route_state |  |
| route_code |  |
| owner_user_id |  |
| queue_id | FK |
| team_code |  |
| region_code |  |
| entry_date |  |
| dpd_at_entry |  |
| exposure_band |  |
| total_outstanding_at_entry |  |
| prescription_date |  |
| stage_clock_start |  |
| deviation_open |  |
| legal_hold |  |
| rule_version |  |
| closed_date |  |
| closure_reason |  |
| plan_ref |  |
| plan_status |  |
| plan_status_as_of |  |
| next_action_text |  |
| next_action_owner_role |  |
| next_action_due_date |  |
| next_action_rule_id |  |
| next_action_waiting |  |
| last_allocation_date |  |
| status_before_hold |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| case_id | FK |
| account_key | BK |
| is_primary |  |
| linked_from |  |
| linked_to |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| case_id | FK |
| person_key | BK |
| party_role |  |
| role_from |  |
| role_to |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| case_id | FK |
| deviation_code |  |
| raised_at |  |
| raised_by |  |
| paused_state |  |
| handler_user_id |  |
| contact_stop |  |
| cleared_at |  |
| outcome |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| queue_code | AK1 |
| queue_name |  |
| team_code |  |
| role_code |  |
| assignment_method |  |
| capacity_cap |  |
| overflow_queue_id | FK |
| rr_cursor_user_id |  |
| table_version |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| case_id | FK |
| task_id | FK |
| assignee_user_id |  |
| assigned_at |  |
| ended_at |  |
| reason |  |
| rule_id |  |
| queue_id | FK |
| transfer_reason_code |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| case_id | FK |
| task_code |  |
| element_type |  |
| discretion |  |
| status |  |
| owner_role |  |
| due_at |  |
| completed_at |  |
| outcome_code |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| case_id | FK |
| task_id | FK |
| timer_type |  |
| started_at |  |
| expires_at |  |
| warn_at |  |
| paused |  |
| status |  |
| escalation_level |  |
| warned_at |  |
| treatment_id | FK |
| escalated_to_role |  |
| escalated_at |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| business_date | AK1 |
| case_id | AK1, FK |
| case_no |  |
| account_key | BK |
| account_no | AK1 |
| product_group |  |
| stage_code |  |
| status |  |
| owner_user_id |  |
| queue_code |  |
| team_code |  |
| route_code |  |
| total_balance |  |
| days_past_due |  |
| refreshed_at |  |
| last_contact_at |  |
| last_action_code |  |
| publish_status |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| account_key | AK1, BK |
| business_date | AK1 |
| reason_code |  |
| rule_id |  |
| rule_version |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| queue_id | FK |
| user_id |  |
| capacity |  |
| skill_codes |  |
| table_version |  |
| valid_from |  |
| valid_to |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| queue_id | FK |
| as_of | AK1 |
| depth |  |
| unassigned |  |
| avg_age_days |  |
| max_age_days |  |
| owner_min |  |
| owner_max |  |
| breached |  |
| status |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

### References

| Entity | Field | Refers to | Reference | Kind |
|---|---|---|---|---|
| recovery_case | primary_person_key | v_ace_customer | Mandatory | Business key, no foreign key |
| recovery_case | queue_id | queue | Optional | Foreign key |
| case_account | case_id | recovery_case | Mandatory | Foreign key |
| case_account | account_key | v_ace_account | Mandatory | Business key, no foreign key |
| case_party | case_id | recovery_case | Mandatory | Foreign key |
| case_party | person_key | v_ace_customer | Mandatory | Business key, no foreign key |
| deviation | case_id | recovery_case | Mandatory | Foreign key |
| queue | overflow_queue_id | queue | Optional | Foreign key |
| assignment | case_id | recovery_case | Mandatory | Foreign key |
| assignment | task_id | task | Optional | Foreign key |
| assignment | queue_id | queue | Optional | Foreign key |
| task | case_id | recovery_case | Mandatory | Foreign key |
| timer | case_id | recovery_case | Mandatory | Foreign key |
| timer | task_id | task | Optional | Foreign key |
| timer | treatment_id | treatment | Optional | Foreign key |
| treatment | case_id | recovery_case | Mandatory | Foreign key |
| guarantee_claim | case_id | recovery_case | Mandatory | Foreign key |
| legal_action | case_id | recovery_case | Mandatory | Foreign key |
| notice | case_id | recovery_case | Mandatory | Foreign key |
| partner_instruction | case_id | recovery_case | Mandatory | Foreign key |
| interaction | case_id | recovery_case | Mandatory | Foreign key |
| document | case_id | recovery_case | Mandatory | Foreign key |
| decision_log_entry | case_id | recovery_case | Optional | Foreign key |
| proceeds | case_id | recovery_case | Mandatory | Foreign key |
| write_off | case_id | recovery_case | Mandatory | Foreign key |
| case_list_row | case_id | recovery_case | Mandatory | Foreign key |
| case_list_row | account_key | v_ace_account | Mandatory | Business key, no foreign key |
| dp_treatment | case_id | recovery_case | Mandatory | Foreign key |
| dp_guarantee_claim | case_id | recovery_case | Mandatory | Foreign key |
| outbox_event | case_id | recovery_case | Optional | Foreign key |
| outbox_delivery | task_id | task | Optional | Foreign key |
| case_entry_exclusion | account_key | v_ace_account | Mandatory | Business key, no foreign key |
| queue_member | queue_id | queue | Mandatory | Foreign key |
| queue_measure | queue_id | queue | Mandatory | Foreign key |
| case_document_check | case_id | recovery_case | Mandatory | Foreign key |
| document_intake | case_id | recovery_case | Optional | Foreign key |
| signature_request | case_id | recovery_case | Mandatory | Foreign key |
| approval | case_id | recovery_case | Mandatory | Foreign key |
| agent_run | case_id | recovery_case | Optional | Foreign key |

## DP04 Treatment and offers

Restructures, settlements, deeds in lieu, buy-backs and guarantee claims, with terms, approval level and outcome

**System of record**Recovery Workbench for the treatment; ACE (ingested from the core bank) for the restructure plan**How it reaches the Workbench**Held in the Workbench; the plan reference, status and published calculation are read through recovery.v_ace_plan, and the credit result through v_ace_credit_decision.**Freshness**As it changes in the Workbench; plan status from the ACE batch**Objects**6

### Objects

| id | PK |
|---|---|
| case_id | FK |
| decision_log_id | FK |
| treatment_type |  |
| proposed_by |  |
| proposed_at |  |
| offer_amount |  |
| haircut_amount |  |
| installments |  |
| valid_until |  |
| approval_level |  |
| booked_at |  |
| outcome |  |
| outcome_at |  |
| interest_rate |  |
| booking_difference |  |
| first_due_date |  |
| signature_status |  |
| installment_amount |  |
| installments_paid |  |
| installment_shortfall |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| case_id | FK |
| claim_type |  |
| claim_deadline |  |
| claimed_amount |  |
| filed_at |  |
| paid_amount |  |
| status |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| treatment_id | AK1, FK |
| case_id | FK |
| decision_log_id | FK |
| treatment_type |  |
| proposed_by |  |
| proposed_at |  |
| offer_amount |  |
| haircut_amount |  |
| installments |  |
| valid_until |  |
| approval_level |  |
| booked_at |  |
| outcome |  |
| outcome_at |  |
| business_date | AK1 |
| contract_no |  |
| contract_date |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| guarantee_claim_id | AK1, FK |
| case_id | FK |
| claim_type |  |
| claim_deadline |  |
| claimed_amount |  |
| filed_at |  |
| paid_amount |  |
| status |  |
| business_date | AK1 |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| plan_ref |  |
|---|---|
| ace_case_id |  |
| plan_status |  |
| plan_created_at |  |
| tdr_calculation_id |  |
| plan_published_at |  |
| associated_account_id |  |
| account_key | BK |
| booked_at |  |
| approved_at |  |
| submitted_at |  |
| closed_at |  |
| closed_reason |  |
| ca_approved_at |  |
| installments |  |
| recommended_installment |  |
| recommended_package |  |
| plan_status_as_of |  |

| credit_decision_key |  |
|---|---|
| account_key | BK |
| nleads_ref |  |
| credit_result |  |
| credit_result_reason |  |
| decided_at |  |
| source_system |  |
| data_as_of |  |

### References

| Entity | Field | Refers to | Reference | Kind |
|---|---|---|---|---|
| timer | treatment_id | treatment | Optional | Foreign key |
| treatment | case_id | recovery_case | Mandatory | Foreign key |
| treatment | decision_log_id | decision_log_entry | Optional | Foreign key |
| guarantee_claim | case_id | recovery_case | Mandatory | Foreign key |
| interaction | treatment_id | treatment | Optional | Foreign key |
| document | treatment_id | treatment | Optional | Foreign key |
| proceeds | treatment_id | treatment | Optional | Foreign key |
| dp_treatment | treatment_id | treatment | Mandatory | Foreign key |
| dp_treatment | case_id | recovery_case | Mandatory | Foreign key |
| dp_treatment | decision_log_id | decision_log_entry | Optional | Foreign key |
| dp_guarantee_claim | guarantee_claim_id | guarantee_claim | Mandatory | Foreign key |
| dp_guarantee_claim | case_id | recovery_case | Mandatory | Foreign key |
| signature_request | treatment_id | treatment | Optional | Foreign key |

## DP05 Contact and promises

Every contact, letter, promise and hand-over on the case, in order, including the collections history from EFS

**System of record**ACE (ingested from EFS)**How it reaches the Workbench**Read through recovery.v_ace_efs_action and v_ace_efs_assignment. The Workbench writes its own contact, letter and promise entries to interaction.**Freshness**ACE end of day; Workbench entries as they change**Objects**3

### Objects

| id | PK |
|---|---|
| case_id | FK |
| person_key | BK |
| occurred_at |  |
| channel |  |
| direction |  |
| action_code |  |
| contact_result |  |
| promise_amount |  |
| promise_date |  |
| summary |  |
| conduct_check |  |
| source_system |  |
| event_code |  |
| actor_type |  |
| actor_ref |  |
| source_ref |  |
| idempotency_key | AK1 |
| case_seq |  |
| decision_log_id | FK |
| corrects_entry_id | FK |
| contact_key | BK |
| from_holder_ref |  |
| to_holder_ref |  |
| treatment_id | FK |
| proceeds_id | FK |
| retention_class |  |
| delivery_status |  |
| external_ref |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| efs_record_key |  |
|---|---|
| account_key | BK |
| person_key | BK |
| action_code |  |
| action_code_name |  |
| action_date |  |
| contact_at |  |
| user_code |  |
| comments |  |
| is_call |  |
| is_rpc |  |
| is_ptp |  |
| promise_status |  |
| promise_eval_status |  |
| promise_date |  |
| promise_amount |  |
| collection_phase |  |
| act_date_bucket |  |
| act_date_past_due_days |  |
| last_tdr_date |  |
| contact_result | B |
| action_contact_status | B |

| account_key | BK |
|---|---|
| assignment_scheme |  |
| assignee_code |  |
| assignee_name |  |
| assignment_start_date |  |
| assignment_end_date |  |
| assignment_start_total_balance |  |
| assignment_end_total_balance |  |
| distribution_area |  |

### References

| Entity | Field | Refers to | Reference | Kind |
|---|---|---|---|---|
| interaction | case_id | recovery_case | Mandatory | Foreign key |
| interaction | person_key | v_ace_customer | Optional | Business key, no foreign key |
| interaction | decision_log_id | decision_log_entry | Optional | Foreign key |
| interaction | corrects_entry_id | interaction | Optional | Foreign key |
| interaction | contact_key | v_ace_contact | Optional | Business key, no foreign key |
| interaction | treatment_id | treatment | Optional | Foreign key |
| interaction | proceeds_id | proceeds | Optional | Foreign key |

## DP06 Collateral and assets

Collateral, appraisals, assets held after repossession or transfer, listings and sale results

**System of record**ACE (ingested from CCMS, SVAF, AMIS and RPS)**How it reaches the Workbench**Read through recovery.v_ace_collateral, v_ace_collateral_detail, v_ace_asset, v_ace_npa_asset, v_ace_npa_sale and v_ace_valuation. Listings and sale results stay in the Workbench.**Freshness**ACE weekly or monthly per source; listings as they change**Objects**9

### Objects

| id | PK |
|---|---|
| asset_key | BK |
| sale_channel |  |
| start_price |  |
| floor_price |  |
| round_no |  |
| listed_at |  |
| status |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| asset_key | BK |
| listing_id | FK |
| contract_date |  |
| sale_date |  |
| sale_price |  |
| transfer_fee |  |
| specific_business_tax |  |
| corporate_income_tax |  |
| gain_loss |  |
| incentive_amount |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| valuation_key | PK, BK |
|---|---|
| accepted |  |
| accepted_at |  |
| accepted_by |  |
| valuer_partner_id |  |
| stale_flag |  |
| age_days |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| collateral_no |  |
|---|---|
| asset_key | BK |
| account_key | BK |
| collateral_value |  |
| register_date |  |
| in_active |  |
| collateral_type |  |
| description |  |

| asset_ref |  |
|---|---|
| asset_key | BK |
| asset_type |  |
| description |  |
| address |  |
| town |  |
| post_code |  |
| county |  |
| country |  |

| valuation_key | BK |
|---|---|
| asset_key | BK |
| appraisal_no |  |
| appraisal_type |  |
| appraised_value |  |
| forced_sale_value |  |
| appraisal_date |  |
| source_system |  |
| data_as_of |  |

| asset_key | BK |
|---|---|
| title_doc_no |  |
| plot_no |  |
| area_text |  |
| province |  |
| district |  |
| subdistrict |  |
| insured_value |  |
| insurance_expiry |  |
| lien_rank |  |
| source_system |  |
| data_as_of |  |

| asset_ref |  |
|---|---|
| asset_key | BK |
| asset_code |  |
| transfer_in_type |  |
| from_segment |  |
| transfer_in_date |  |
| book_value |  |
| auction_purchase_price |  |
| repossessed_date |  |
| stock_date |  |
| source_system |  |
| data_as_of |  |

| npa_sale_key |  |
|---|---|
| npa_asset_key |  |
| contract_date |  |
| sale_date |  |
| sale_price |  |
| transfer_fee |  |
| specific_business_tax |  |
| corporate_income_tax |  |
| incentive_amount |  |
| source_system |  |
| data_as_of |  |

### References

| Entity | Field | Refers to | Reference | Kind |
|---|---|---|---|---|
| listing | asset_key | v_ace_asset | Mandatory | Business key, no foreign key |
| asset_sale | asset_key | v_ace_asset | Mandatory | Business key, no foreign key |
| asset_sale | listing_id | listing | Optional | Foreign key |
| valuation_ext | valuation_key | v_ace_valuation | Mandatory | Business key, no foreign key (1:1 extension) |

## DP07 Legal events and cases

Notices and proof of delivery, lawsuits, court case numbers, hearings, judgments and enforcement

**System of record**ACE (ingested from LIT and WIN) for the court record and the proof of delivery; Workbench for notices and enforcement**How it reaches the Workbench**Read through recovery.v_ace_lawsuit, v_ace_hearing and v_ace_pod. Notices and enforcement actions are written to the Workbench and dispatched through WIN.**Freshness**ACE end of day; Workbench entries as they change**Objects**6

### Objects

| id | PK |
|---|---|
| case_id | FK |
| law_firm_id | FK |
| action_type |  |
| lawsuit_no |  |
| black_case_no |  |
| red_case_no |  |
| court_name |  |
| claim_amount |  |
| filed_date |  |
| judgment_date |  |
| judgment_amount |  |
| lit_status |  |
| status |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| case_id | FK |
| document_id | FK |
| notice_type |  |
| sent_date |  |
| barcode |  |
| callback_date |  |
| delivery_status |  |
| sent_type |  |
| person_key | BK |
| template_id | FK |
| hold_reason |  |
| dispatch_file_id | FK |
| dispatch_attempts |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| legal_action_id | FK |
| hearing_date |  |
| hearing_type |  |
| outcome |  |
| next_date |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| lawsuit_key |  |
|---|---|
| account_key | BK |
| lawsuit_no |  |
| black_case_no |  |
| red_case_no |  |
| court_name |  |
| claim_amount |  |
| filed_date |  |
| judgment_date |  |
| judgment_amount |  |
| lit_status |  |
| source_system |  |
| data_as_of |  |

| hearing_key |  |
|---|---|
| lawsuit_key |  |
| hearing_date |  |
| hearing_type |  |
| next_date |  |
| source_system |  |
| data_as_of |  |

| pod_key |  |
|---|---|
| account_key | BK |
| notice_ref |  |
| sent_date |  |
| barcode |  |
| callback_date |  |
| delivery_status |  |
| sent_type |  |
| source_system |  |
| data_as_of |  |

### References

| Entity | Field | Refers to | Reference | Kind |
|---|---|---|---|---|
| legal_action | case_id | recovery_case | Mandatory | Foreign key |
| legal_action | law_firm_id | partner | Optional | Foreign key |
| notice | case_id | recovery_case | Mandatory | Foreign key |
| notice | document_id | document | Optional | Foreign key |
| notice | person_key | v_ace_customer | Optional | Business key, no foreign key |
| notice | template_id | template | Optional | Foreign key |
| notice | dispatch_file_id | outbound_item | Optional | Foreign key |
| hearing | legal_action_id | legal_action | Mandatory | Foreign key |

## DP08 Partner performance

Partners on the panel, work placed with each, results, fees and scorecards

**System of record**Recovery Workbench**How it reaches the Workbench**Held in the Workbench; partner results arrive through the partner portal.**Freshness**As it changes**Objects**2

### Objects

| id | PK |
|---|---|
| partner_code | AK1 |
| partner_name |  |
| partner_type |  |
| panel_status |  |
| contract_end |  |
| score |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| case_id | FK |
| partner_id | FK |
| instruction_type |  |
| instructed_at |  |
| due_at |  |
| status |  |
| result_code |  |
| fee_amount |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

### References

| Entity | Field | Refers to | Reference | Kind |
|---|---|---|---|---|
| legal_action | law_firm_id | partner | Optional | Foreign key |
| partner_instruction | case_id | recovery_case | Mandatory | Foreign key |
| partner_instruction | partner_id | partner | Mandatory | Foreign key |
| debt_sale_lot | buyer_partner_id | partner | Optional | Foreign key |
| partner_user | partner_id | partner | Mandatory | Foreign key |
| document_intake | partner_id | partner | Optional | Foreign key |

## DP09 Debt sale

Debt sale lots, the accounts in each lot, buyers, prices, approval and put-backs

**System of record**Recovery Workbench**How it reaches the Workbench**Held in the Workbench. Past lots are migrated once from the bank's debt sale files; nothing is loaded at run time.**Freshness**As it changes**Objects**2

### Objects

| id | PK |
|---|---|
| lot_no | AK1 |
| cut_off_date |  |
| segment |  |
| reserve_price |  |
| buyer_partner_id | FK |
| buyer_class |  |
| signing_date |  |
| approval_authority |  |
| payment_terms |  |
| status |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| lot_id | FK |
| account_key | BK |
| borrower_code |  |
| outstanding |  |
| selling_price |  |
| put_back_status |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

### References

| Entity | Field | Refers to | Reference | Kind |
|---|---|---|---|---|
| debt_sale_lot | buyer_partner_id | partner | Optional | Foreign key |
| debt_sale_account | lot_id | debt_sale_lot | Mandatory | Foreign key |
| debt_sale_account | account_key | v_ace_account | Mandatory | Business key, no foreign key |

## DP10 Documents and extracted fields

Documents against the case, the fields read from them, retention class and custody of originals

**System of record**Recovery Workbench document hub**How it reaches the Workbench**Held in the Workbench. The signature request and its status are read through recovery.v_ace_esign.**Freshness**As it changes**Objects**9

### Objects

| id | PK |
|---|---|
| case_id | FK |
| person_key | BK |
| document_type |  |
| source |  |
| storage_ref |  |
| classification_confidence |  |
| review_status |  |
| retention_class |  |
| write_once |  |
| doc_version |  |
| previous_version_id | FK |
| content_sha256 |  |
| captured_at |  |
| capture_latitude |  |
| capture_longitude |  |
| client_file_id |  |
| capture_kind |  |
| template_id | FK |
| treatment_id | FK |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| document_id | FK |
| field_name |  |
| field_value |  |
| confidence |  |
| confirmed_by |  |
| extracted_value |  |
| extractor_version |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| document_id | FK |
| moved_at |  |
| from_location |  |
| to_location |  |
| held_by |  |
| due_back |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| case_id | FK |
| checklist_version |  |
| required_count |  |
| present_count |  |
| missing_types |  |
| complete |  |
| checked_at |  |
| last_event_id | FK |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| source |  |
| source_ref |  |
| channel_code |  |
| file_name |  |
| file_size |  |
| captured_at |  |
| sender_address |  |
| partner_id | FK |
| run_id |  |
| received_at |  |
| file_sha256 |  |
| intake_ref |  |
| scan_result |  |
| scanned_at |  |
| case_id | FK |
| document_id | FK |
| ocr_ref |  |
| ocr_status |  |
| ocr_attempts |  |
| page_count |  |
| rescan_pages |  |
| ocr_quality |  |
| languages |  |
| ocr_engine_version |  |
| predicted_type |  |
| classification_confidence |  |
| type_candidates |  |
| classifier_version |  |
| classify_fallback |  |
| match_status |  |
| candidate_case_ids |  |
| extracted_fields |  |
| extract_status |  |
| extract_attempts |  |
| review_reason |  |
| review_outcome |  |
| resolved_by |  |
| resolved_at |  |
| discard_reason |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| intake_id | FK |
| document_id | FK |
| page_no | AK1 |
| text_content |  |
| quality |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| document_id | FK |
| run_month | AK1 |
| action |  |
| decision_log_id | FK |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| case_id | FK |
| treatment_id | FK |
| document_id | FK |
| person_key | BK |
| method |  |
| status |  |
| sent_at |  |
| signed_at |  |
| signed_document_id | FK |
| expires_at |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| esign_key |  |
|---|---|
| account_key | BK |
| external_ref |  |
| requested_at |  |
| status |  |
| source_system |  |
| data_as_of |  |

### References

| Entity | Field | Refers to | Reference | Kind |
|---|---|---|---|---|
| notice | document_id | document | Optional | Foreign key |
| document | case_id | recovery_case | Mandatory | Foreign key |
| document | person_key | v_ace_customer | Optional | Business key, no foreign key |
| document | previous_version_id | document | Optional | Foreign key |
| document | template_id | template | Optional | Foreign key |
| document | treatment_id | treatment | Optional | Foreign key |
| document_field | document_id | document | Mandatory | Foreign key |
| document_custody | document_id | document | Mandatory | Foreign key |
| case_document_check | case_id | recovery_case | Mandatory | Foreign key |
| case_document_check | last_event_id | outbox_event | Optional | Foreign key |
| document_intake | partner_id | partner | Optional | Foreign key |
| document_intake | case_id | recovery_case | Optional | Foreign key |
| document_intake | document_id | document | Optional | Foreign key |
| document_text | intake_id | document_intake | Mandatory | Foreign key |
| document_text | document_id | document | Optional | Foreign key |
| retention_action | document_id | document | Mandatory | Foreign key |
| retention_action | decision_log_id | decision_log_entry | Optional | Foreign key |
| signature_request | case_id | recovery_case | Mandatory | Foreign key |
| signature_request | treatment_id | treatment | Optional | Foreign key |
| signature_request | document_id | document | Mandatory | Foreign key |
| signature_request | person_key | v_ace_customer | Mandatory | Business key, no foreign key |
| signature_request | signed_document_id | document | Optional | Foreign key |

## DP11 Scores and route economics

Risk scores, expected return by route, estimated sale price and sale success rate, restructure scheme suggestions

**System of record**ACE (ingested from COLLINS)**How it reaches the Workbench**Read through recovery.v_ace_score. The Workbench loads nothing.**Freshness**ACE end of day; monthly for some models**Objects**1

### Objects

| score_key |  |
|---|---|
| account_key | BK |
| model_code |  |
| model_version |  |
| score_value |  |
| estimate_value |  |
| route_code |  |
| scored_at |  |
| source_system |  |
| data_as_of |  |

### References

No references.

## DP12 Decision log

One entry per decision with the rule, model and agent versions, inputs, recommendation, approval, actions and outcome

**System of record**Recovery Workbench**How it reaches the Workbench**Held in the Workbench.**Freshness**As it changes**Objects**2

### Objects

| id | PK |
|---|---|
| case_id | FK |
| decision_code |  |
| rule_id |  |
| rule_version |  |
| model_version |  |
| agent_version |  |
| inputs_ref |  |
| recommendation |  |
| approver_user_id |  |
| approval_level |  |
| final_call |  |
| override_reason |  |
| actions |  |
| outcome |  |
| decided_at |  |
| prev_hash |  |
| entry_hash | AK1 |
| chain_seq | AK1 |
| corrects_entry_id | FK |
| actor_user_id |  |
| idempotency_key | AK1 |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| case_id | FK |
| decision_code |  |
| regulation_item |  |
| capability_area |  |
| route_role_code |  |
| approval_level |  |
| delegation_limit_id | FK |
| limit_version |  |
| product_group |  |
| amount |  |
| terms |  |
| prepared_by |  |
| assigned_user_id |  |
| status |  |
| due_at |  |
| escalation_level |  |
| source_type |  |
| source_ref |  |
| rule_id |  |
| rule_version |  |
| decision_log_id | FK |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

### References

| Entity | Field | Refers to | Reference | Kind |
|---|---|---|---|---|
| treatment | decision_log_id | decision_log_entry | Optional | Foreign key |
| interaction | decision_log_id | decision_log_entry | Optional | Foreign key |
| decision_log_entry | case_id | recovery_case | Optional | Foreign key |
| decision_log_entry | corrects_entry_id | decision_log_entry | Optional | Foreign key |
| write_off | decision_log_id | decision_log_entry | Optional | Foreign key |
| dp_treatment | decision_log_id | decision_log_entry | Optional | Foreign key |
| retention_action | decision_log_id | decision_log_entry | Optional | Foreign key |
| approval | case_id | recovery_case | Mandatory | Foreign key |
| approval | delegation_limit_id | delegation_limit | Optional | Foreign key |
| approval | decision_log_id | decision_log_entry | Optional | Foreign key |
| agent_run | decision_log_id | decision_log_entry | Optional | Foreign key |
| agent_feedback | decision_log_id | decision_log_entry | Optional | Foreign key |

## DP13 Money and closure

Payments and proceeds matched to the case, write-off postings and recovery after charge-off

**System of record**ACE (ingested from ALS and GL)**How it reaches the Workbench**Read through recovery.v_ace_payment and v_ace_write_off; proceeds matching and the write-off decision stay in the Workbench.**Freshness**ACE end of day for payments; monthly for GL**Objects**3

### Objects

| id | PK |
|---|---|
| case_id | FK |
| treatment_id | FK |
| payment_code | BK |
| source |  |
| amount |  |
| received_date |  |
| matched_to |  |
| posting_ref |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| case_id | FK |
| decision_log_id | FK |
| amount |  |
| tax_criteria_met |  |
| committee_date |  |
| posted_date |  |
| responsibility_center |  |
| cost_center |  |
| gl_product |  |
| recovered_after |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| write_off_key |  |
|---|---|
| account_key | BK |
| amount |  |
| posted_date |  |
| responsibility_center |  |
| cost_center |  |
| gl_product |  |
| source_system |  |
| data_as_of |  |

### References

| Entity | Field | Refers to | Reference | Kind |
|---|---|---|---|---|
| interaction | proceeds_id | proceeds | Optional | Foreign key |
| proceeds | case_id | recovery_case | Mandatory | Foreign key |
| proceeds | treatment_id | treatment | Optional | Foreign key |
| proceeds | payment_code | v_ace_payment | Optional | Business key, no foreign key |
| write_off | case_id | recovery_case | Mandatory | Foreign key |
| write_off | decision_log_id | decision_log_entry | Optional | Foreign key |

## DP14 Reference data

Rules, approval limits, lists of values, roles, permissions and letter templates, each versioned

**System of record**Recovery Workbench**How it reaches the Workbench**Held in the Workbench and versioned. Source codes and descriptions are read through v_ace_product, v_ace_branch, v_ace_efs_action_code, v_ace_holiday and v_ace_iam_group rather than loaded.**Freshness**By versioned load**Objects**32

### Objects

| id | PK |
|---|---|
| package_code | AK1 |
| title |  |
| owner_role |  |
| hit_policy |  |

| id | PK |
|---|---|
| package_id | AK1, FK |
| version_label | AK1 |
| status |  |
| source_blob_ref |  |
| drl_source |  |
| checksum |  |
| valid_from |  |
| valid_to |  |
| author |  |
| approver |  |
| loaded_at |  |
| approved_at |  |
| test_result |  |
| dry_run_counts |  |
| rollback_of | FK |
| change_checklist |  |

| id | PK |
|---|---|
| rule_id | AK1 |
| rule_version | AK1 |
| route_set |  |
| from_state |  |
| event_code |  |
| condition_expr |  |
| action_text |  |
| to_state |  |
| owner_role |  |
| timer_spec |  |
| valid_from |  |
| valid_to |  |
| approved_by |  |
| test_case_id |  |
| rule_table |  |
| row_order |  |
| target_queue_code |  |
| package_version_id | FK |
| drools_rule_name |  |
| outputs |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| decision_code |  |
| approval_level |  |
| product_group |  |
| principal_limit |  |
| loss_pct_limit |  |
| min_price_pct_fmv |  |
| holder_user_id |  |
| substitute_user_id |  |
| valid_from |  |
| valid_to |  |
| limit_version |  |
| regulation_item |  |
| applies_when |  |
| max_loss_amount |  |
| max_delay_count |  |
| min_price_pct_principal |  |
| min_received_pct |  |
| max_term_years |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| lov_code | AK1 |
| value_code | AK1 |
| label_en |  |
| label_th |  |
| sort_order |  |
| valid_from |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| role_code | AK1 |
| role_name |  |
| role_class |  |
| default_scope |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| role_id | FK |
| capability_area |  |
| letters |  |
| matrix_version |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| template_code | AK1 |
| template_version | AK1 |
| language |  |
| product_group |  |
| body_ref |  |
| approved_by_legal |  |
| approved_by |  |
| approved_at |  |
| valid_from |  |
| channel |  |
| notice_type |  |
| signature_basis |  |
| merge_codes |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| product_code | AK1 |
| product_name |  |
| definition |  |
| system_of_record |  |
| owner_role |  |
| owner_user_id |  |
| refresh_cycle |  |
| expected_by |  |
| valid_from |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| product_code | AK1 |
| role_code | AK1 |
| can_read |  |
| access_version | AK1 |
| valid_from |  |
| valid_to |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| object_name | AK1 |
| business_name |  |
| subject_area |  |
| data_product |  |
| system_of_record |  |
| description |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| field_id | AK1 |
| object_name |  |
| field_name |  |
| data_type |  |
| physical_type |  |
| is_mandatory |  |
| lov_code |  |
| references_object |  |
| source_system |  |
| source_field |  |
| is_personal |  |
| description |  |
| owner_role |  |
| refresh_cycle |  |
| late_behavior |  |
| interface_id |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| field_id | AK1 |
| field_version | AK1 |
| definition |  |
| change_reason |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| product_code |  |
| table_name | AK1 |
| record_class | AK1 |
| retention_months |  |
| age_basis_field |  |
| end_action |  |
| rule_version | AK1 |
| valid_from |  |
| valid_to |  |
| approved_by |  |
| reference_version_id | FK |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| action_code | AK1 |
| channel |  |
| in_ledger |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| param_key | AK1 |
| kind |  |
| value_type |  |
| unit |  |
| min_value |  |
| max_value |  |
| default_value |  |
| scope |  |
| required |  |
| owner_role |  |
| environments |  |
| used_by |  |
| secret |  |
| description |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| param_key | AK1 |
| environment | AK1 |
| param_value |  |
| product_group | AK1 |
| version_no | AK1 |
| valid_from |  |
| valid_to |  |
| status |  |
| author_user_id |  |
| approver_user_id |  |
| approved_at |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| table_code | AK1 |
| version_no | AK1 |
| version_label |  |
| valid_from |  |
| valid_to |  |
| status |  |
| author_user_id |  |
| approver_user_id |  |
| approved_at |  |
| row_count |  |
| content_hash |  |
| load_id |  |
| dry_run_counts |  |
| rollback_reason |  |
| change_request_ref |  |
| impact_summary |  |
| test_result |  |
| rollback_plan |  |
| verified_by |  |
| verified_at |  |
| verify_note |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| version_id | FK |
| row_key | AK1 |
| row_data |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| test_case_id | AK1 |
| route_set |  |
| rule_version | AK1 |
| rule_id |  |
| package_version_id | FK |
| from_state |  |
| event_code |  |
| facts |  |
| expected_to_state |  |
| expected_owner_role |  |
| expected_timer_spec |  |
| result |  |
| result_detail |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| role_code | AK1 |
| field_id | AK1 |
| unmasked |  |
| masking_version | AK1 |
| valid_from |  |
| valid_to |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| role_code | AK1 |
| conflicts_with | AK1 |
| reason |  |
| conflict_version | AK1 |
| valid_from |  |
| valid_to |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| identity_ref | AK1 |
| partner_id | FK |
| role_code |  |
| valid_from |  |
| valid_to |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| doc_type_code | AK1 |
| label_en |  |
| label_th |  |
| write_once |  |
| retention_class |  |
| field_definitions |  |
| legal_signoff_by |  |
| legal_signoff_date |  |
| npa_signoff_by |  |
| npa_signoff_date |  |
| table_version | AK1 |
| valid_from |  |
| valid_to |  |
| reference_version_id | FK |
| classify_threshold |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| stage_code | AK1 |
| route_code | AK1 |
| document_type | AK1 |
| required |  |
| sort_order |  |
| table_version | AK1 |
| valid_from |  |
| valid_to |  |
| reference_version_id | FK |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| param_code | AK1 |
| param_value |  |
| unit |  |
| table_version | AK1 |
| valid_from |  |
| valid_to |  |
| reference_version_id | FK |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| merge_code | AK1 |
| source_entity |  |
| source_field |  |
| field_id |  |
| is_required |  |
| personal_data |  |
| catalog_version | AK1 |
| valid_from |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| action_code |  |
|---|---|
| action_name |  |
| category |  |

| product_code |  |
|---|---|
| product_name |  |
| product_type |  |
| product_category |  |
| product_category_efs |  |

| branch_code |  |
|---|---|
| branch_name |  |
| address |  |
| phone |  |

| holiday_date |  |
|---|---|
| holiday_year |  |
| holiday_name |  |
| holiday_name_thai |  |
| holiday_weekday |  |

| entra_group |  |
|---|---|
| role_code |  |
| source_system |  |
| data_as_of |  |

### References

| Entity | Field | Refers to | Reference | Kind |
|---|---|---|---|---|
| notice | template_id | template | Optional | Foreign key |
| document | template_id | template | Optional | Foreign key |
| permission | role_id | role | Mandatory | Foreign key |
| retention_rule | reference_version_id | reference_version | Optional | Foreign key |
| reference_row | version_id | reference_version | Mandatory | Foreign key |
| partner_user | partner_id | partner | Mandatory | Foreign key |
| document_type | reference_version_id | reference_version | Optional | Foreign key |
| document_checklist_item | reference_version_id | reference_version | Optional | Foreign key |
| document_hub_parameter | reference_version_id | reference_version | Optional | Foreign key |
| approval | delegation_limit_id | delegation_limit | Optional | Foreign key |
| rule_package_version | package_id | rule_package | Mandatory | Foreign key |
| rule_package_version | rollback_of | rule_package_version | Optional | Foreign key |
| rule_row | package_version_id | rule_package_version | Optional | Foreign key |
| rule_test_case | package_version_id | rule_package_version | Optional | Foreign key |

## OPS Loads and operations

The freshness stamp, reconciliation, outbound interfaces, jobs, feature flags, the outbox and idempotency records that run the Workbench. No inbound load: the ACE batch record is read through v_ace_batch_status

**System of record**Recovery Workbench; ACE for the batch record**How it reaches the Workbench**Held in the Workbench; the ACE batch business date is read through recovery.v_ace_batch_status**Freshness**As it changes; batch status at each ACE batch**Objects**14

### Objects

| id | PK |
|---|---|
| product_code | AK1 |
| source_system |  |
| business_date | AK1 |
| source_extracted_at |  |
| loaded_at |  |
| status |  |
| stale_flagged_at |  |
| duplicate_count |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| contract_code | AK1 |
| source_system |  |
| interface_id |  |
| contract_version | AK1 |
| status |  |
| confirmed_by_role |  |
| confirmed_on |  |
| confirmation_document_ref |  |
| published_at |  |
| published_by |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| rec_code | AK1 |
| business_date | AK1 |
| product_group | AK1 |
| source_count |  |
| workbench_count |  |
| source_amount |  |
| workbench_amount |  |
| variance_count |  |
| variance_pct |  |
| tolerance_pct |  |
| result |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| copy_name | AK1 |
| last_entry_hash |  |
| last_decided_at |  |
| rows_copied_total |  |
| business_date |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| interface_id | AK1 |
| direction |  |
| transport |  |
| inbound_path |  |
| file_pattern |  |
| data_product |  |
| max_attempts |  |
| retry_intervals_min |  |
| owner_role |  |
| alert_role |  |
| valid_from | AK1 |
| valid_to |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| interface_id |  |
| idempotency_key | AK1 |
| payload_ref |  |
| case_ids |  |
| attempt_count |  |
| next_attempt_at |  |
| status |  |
| last_error |  |
| owner_role |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| consumer | AK1 |
| idempotency_key | AK1 |
| event_id | FK |
| hit_count |  |
| last_seen_at |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| idempotency_key | AK1 |
| endpoint |  |
| request_hash |  |
| response |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| event_type |  |
| schema_version |  |
| case_id | FK |
| case_seq | AK1 |
| idempotency_key | AK1 |
| payload |  |
| actor_ref |  |
| occurred_at |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| event_id | AK1, FK |
| consumer | AK1 |
| status |  |
| attempt_count |  |
| next_attempt_at |  |
| last_error_code |  |
| delivered_at |  |
| task_id | FK |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| flag_key | AK1 |
| description |  |
| owner_user_id |  |
| owner_team |  |
| default_on |  |
| dev_on |  |
| sit_on |  |
| uat_on |  |
| prod_on |  |
| removal_date |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| flag_key |  |
| environment |  |
| old_value |  |
| new_value |  |
| reason |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| job_id | AK1 |
| job_name |  |
| owner_role |  |
| schedule_text |  |
| runbook_path |  |
| expected_minutes |  |
| alert_after_minutes |  |
| first_release |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| source_system |  |
|---|---|
| business_date |  |
| started_at |  |
| completed_at |  |
| status |  |
| record_count |  |
| checksum |  |
| feed_version |  |
| is_complete |  |

### References

| Entity | Field | Refers to | Reference | Kind |
|---|---|---|---|---|
| notice | dispatch_file_id | outbound_item | Optional | Foreign key |
| processed_event | event_id | outbox_event | Optional | Foreign key |
| outbox_event | case_id | recovery_case | Optional | Foreign key |
| outbox_delivery | event_id | outbox_event | Mandatory | Foreign key |
| outbox_delivery | task_id | task | Optional | Foreign key |
| case_document_check | last_event_id | outbox_event | Optional | Foreign key |

## AGT Agent runtime

Agent policies, prompts, runs, labeled samples, evaluations, feedback and alerts

**System of record**Recovery Workbench**How it reaches the Workbench**Held in the Workbench**Freshness**As it changes**Objects**8

### Objects

| id | PK |
|---|---|
| agent_code | AK1 |
| policy_version | AK1 |
| model_code |  |
| model_version |  |
| output_schema_ref |  |
| allowed_tools |  |
| autonomy_mode |  |
| segment_product_group |  |
| segment_region_code |  |
| confidence_floor |  |
| timeout_seconds |  |
| daily_cost_cap_thb |  |
| price_per_1k_tokens_thb |  |
| alert_role |  |
| review_date |  |
| evaluation_run_id | FK |
| promotion_conditions |  |
| watch_measures |  |
| fallback_rule |  |
| status |  |
| valid_from |  |
| valid_to |  |
| loaded_by |  |
| approved_by |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| agent_code | AK1 |
| prompt_version | AK1 |
| body_text |  |
| body_hash |  |
| status |  |
| valid_from |  |
| valid_to |  |
| loaded_by |  |
| approved_by |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| agent_code |  |
| agent_version |  |
| prompt_version |  |
| model_version |  |
| case_id | FK |
| subject_id |  |
| autonomy_mode |  |
| trigger_event |  |
| idempotency_key | AK1 |
| status |  |
| fallback |  |
| guardrail_result |  |
| output |  |
| confidence |  |
| latency_ms |  |
| tokens_in |  |
| tokens_out |  |
| cost_thb |  |
| data_as_of |  |
| run_at |  |
| evaluation_run_id | FK |
| decision_log_id | FK |
| segment_product_group |  |
| segment_region_code |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| agent_code |  |
| sample_code | AK1 |
| sample_version | AK1 |
| subject_type |  |
| subject_id |  |
| label_key | AK1 |
| expected_value |  |
| labeled_by |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| agent_code |  |
| sample_code |  |
| sample_version |  |
| policy_version |  |
| prompt_version |  |
| model_version |  |
| status |  |
| started_at |  |
| finished_at |  |
| requested_by |  |
| total_cost_thb |  |
| p95_latency_ms |  |
| failure_counts |  |
| proposal |  |
| review_count |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| evaluation_run_id | FK |
| approach |  |
| label_key |  |
| sample_size |  |
| true_positive |  |
| false_positive |  |
| false_negative |  |
| agreement_rate |  |
| precision_value |  |
| recall_value |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| agent_run_id | FK |
| item_key |  |
| verdict |  |
| reason |  |
| decision_log_id | FK |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| agent_code |  |
| alert_type |  |
| segment |  |
| business_date |  |
| measured_value |  |
| threshold_value |  |
| sent_to_role |  |
| sent_at |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

### References

| Entity | Field | Refers to | Reference | Kind |
|---|---|---|---|---|
| agent_policy | evaluation_run_id | agent_evaluation_run | Optional | Foreign key |
| agent_run | case_id | recovery_case | Optional | Foreign key |
| agent_run | evaluation_run_id | agent_evaluation_run | Optional | Foreign key |
| agent_run | decision_log_id | decision_log_entry | Optional | Foreign key |
| agent_evaluation | evaluation_run_id | agent_evaluation_run | Mandatory | Foreign key |
| agent_feedback | agent_run_id | agent_run | Mandatory | Foreign key |
| agent_feedback | decision_log_id | decision_log_entry | Optional | Foreign key |

## RPT Reporting

Measure definitions and the snapshots published to Power BI

**System of record**Recovery Workbench**How it reaches the Workbench**Held in the Workbench**Freshness**Daily**Objects**3

### Objects

| id | PK |
|---|---|
| measure_code | AK1 |
| name |  |
| formula |  |
| data_product |  |
| unit |  |
| definition_version | AK1 |
| approved_by |  |
| approved_at |  |
| valid_from |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| measure_code |  |
| definition_version |  |
| business_date |  |
| product_group |  |
| dimension_code |  |
| dimension_value |  |
| value |  |
| case_count |  |
| is_baseline |  |
| frozen |  |
| published_at |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

| id | PK |
|---|---|
| business_date | AK1 |
| status |  |
| case_list_count |  |
| dashboard_count |  |
| held_reason |  |
| is_active |  |
| state |  |
| version |  |
| created_at |  |
| created_by |  |
| updated_at |  |
| updated_by |  |

### References

No references.

## The 30 ACE source views

These are the only way the recovery module reads ACE. Each is a SELECT-only view over one ACE object family, owned by ace_view_owner; the recovery service identity holds SELECT on the views and on nothing else in public. They have no primary key and no foreign key, and the Workbench links to them by business key. Section A ships with RWB-E1-069; Section B ships the week RWB-ACE-001 lands.

| View | Tier | ACE objects read | Data product | What it gives the Workbench |
|---|---|---|---|---|
| v_ace_account | 1 | public.account, public.product, public.branch | DP01 | Read-only view over the ACE account: balances, arrears, days past due, classification, restructure flag and the ACE business date. Replaces the former loan account copy. |
| v_ace_payment | 1 | public.payment, public.account | DP01 | Read-only view over the ACE payment: amount, capital, interest and expense split, channel and payment date. Replaces the former account payment copy. |
| v_ace_customer | 1 | public.customer | DP02 | Read-only view over the ACE customer: name, identity masked to the last four, date of birth, status and profile. Replaces the former customer copy. |
| v_ace_contact | 1 | public.phone, public.email, public.address | DP02 | Read-only view over ACE phone, email and address, unioned behind a contact_type discriminator. Replaces the former contact point copy; values in full because notices need them. |
| v_ace_ca_relation | 1 | public.ca_relation | DP02 | Read-only view over the ACE borrower, guarantor and co-borrower relation, with the guarantee amount. |
| v_ace_aa_relation | 1 | public.aa_relation | DP01 | Read-only view over the ACE parent and child account link. |
| v_ace_collateral | 1 | public.collateral, public.asset | DP06 | Read-only view over the ACE collateral link: collateral number, asset, account, value and type. Replaces the former collateral copy. |
| v_ace_asset | 1 | public.asset | DP06 | Read-only view over the ACE asset: the collateral asset, its type and its address. Replaces the former asset copy. |
| v_ace_efs_action | 1 | public.efs_action | DP05 | Read-only view over the ACE collections action: action code, contact result, promise and outcome. Replaces the former collections history copy. |
| v_ace_efs_action_code | 1 | public.efs_action_code | DP14 | Read-only view over the ACE action code list: 1,106 values, with the English name and category. |
| v_ace_efs_assignment | 1 | public.efs_assignment | DP05 | Read-only view over the ACE assignment and hand-over history, with the balance at each hand-over. |
| v_ace_bucket_log | 1 | public.bucket_log_snapshot, public.account | DP01 | Read-only view over the ACE monthly bucket snapshot: bucket, past due amount and month start. |
| v_ace_product | 1 | public.product | DP14 | Read-only view over the ACE product list: code, name, type and category. Source of the product and product code lists. |
| v_ace_branch | 1 | public.branch | DP14 | Read-only view over the ACE branch list: code, name, address and phone. Source of the branch, business unit and region values. |
| v_ace_holiday | 1 | public.bot_holiday | DP14 | Read-only view over the ACE holiday calendar, used for service levels and legal days. |
| v_ace_plan | 1 | public.ace_case, public.cfsc_mg_ssme_tdr_case, public.account, public.tdr_calculation, public.ai_recommended_plan | DP04 | Read-only view over the ACE restructure plan: reference, status, booking, approval and the published calculation. |
| v_ace_batch_status | 2 | public.ace_batch_run | OPS | Read-only view over the ACE batch record: source, business date, completion, row count and checksum. Drives the Workbench freshness stamp. |
| v_ace_valuation | 2 | public.valuation | DP06 | Read-only view over the ACE appraisal: number, type, appraised and forced sale value, date. Replaces the former valuation copy. |
| v_ace_collateral_detail | 2 | public.collateral_detail | DP06 | Read-only view over the ACE collateral detail: title deed, plot, area, province, district, insurance and lien rank. Replaces the former collateral link copy. |
| v_ace_npa_asset | 2 | public.npa_asset | DP06 | Read-only view over the ACE NPA asset: transfer in, book value, auction price and repossession dates. |
| v_ace_npa_sale | 2 | public.npa_sale | DP06 | Read-only view over the ACE NPA sale: contract, sale price, taxes, fees and incentive. |
| v_ace_lawsuit | 2 | public.lawsuit | DP07 | Read-only view over the ACE lawsuit: court case numbers, claim, filing, judgment and status. |
| v_ace_hearing | 2 | public.hearing | DP07 | Read-only view over the ACE hearing: date, type and next date. |
| v_ace_pod | 2 | public.pod_receipt | DP07 | Read-only view over the ACE proof of delivery: notice reference, barcode, sent date and delivery status. |
| v_ace_write_off | 2 | public.gl_write_off | DP13 | Read-only view over the ACE write-off posting: amount, posted date, responsibility and cost centre. |
| v_ace_score | 2 | public.collins_score | DP11 | Read-only view over the ACE score: model, version, score, estimate and route. Replaces the former score copy. |
| v_ace_party_product | 2 | public.party_product | DP02 | Read-only view over the ACE customer product holding: product type and status. Replaces the former product holding copy. |
| v_ace_credit_decision | 2 | public.credit_decision | DP04 | Read-only view over the ACE credit decision: NLEADS reference, result, reason and decision date. |
| v_ace_esign | 2 | public.esign_request | DP10 | Read-only view over the ACE e-signature request: external reference, requested date and status. The signed file stays in the Workbench document hub. |
| v_ace_iam_group | 2 | public.iam_group | DP14 | Read-only view over the ACE group-to-role mapping, used at sign-in by the ACE common module. |

### View boxes

Every view box is dashed: it is external to the recovery schema and read only. The fields are the view columns named for the Workbench, not the ACE column names. A field marked B is one of the 12 Tier 2 columns that V0003 adds to an existing view through CREATE OR REPLACE VIEW: seven on v_ace_account, three on v_ace_customer and two on v_ace_efs_action.

| account_key | BK |
|---|---|
| account_code |  |
| account_name |  |
| account_status |  |
| account_status_date |  |
| contract_no |  |
| contract_date |  |
| product_key |  |
| product_type |  |
| product_category |  |
| product_category_efs |  |
| branch_code |  |
| branch_name |  |
| oc_code |  |
| company_code |  |
| collection_officer |  |
| collection_phase |  |
| days_past_due |  |
| classification |  |
| total_balance |  |
| accounting_balance |  |
| past_due_amount |  |
| total_interest_fin_charge |  |
| collections_fee |  |
| interest_rate |  |
| last_payment_date |  |
| last_payment_amount |  |
| next_installment_date |  |
| next_installment_amount |  |
| last_tdr_date |  |
| tdr_flag |  |
| rescheduled_flag |  |
| number_reschedules |  |
| tdr_aging |  |
| principle_not_reduce |  |
| data_as_of |  |
| days_since_last_contact |  |
| days_since_last_collection_activity |  |
| relationship_manager |  |
| relationship_manager_phone |  |
| special_memo |  |
| expiry_date |  |
| business_unit | B |
| principal_outstanding | B |
| interest_outstanding | B |
| fees_outstanding | B |
| daily_bucket | B |
| settlement_booked_date | B |
| settlement_booked_amount | B |

| payment_code | BK |
|---|---|
| account_key | BK |
| payment_date |  |
| payment_amount |  |
| capital_amount |  |
| interest_amount |  |
| expense_amount |  |
| commission_amount |  |
| payment_channel |  |
| description |  |
| comments |  |
| data_as_of |  |

| cif_no |  |
|---|---|
| person_key | BK |
| first_name |  |
| last_name |  |
| date_of_birth |  |
| deceased_date |  |
| deceased_flag |  |
| gender |  |
| nationality |  |
| marital_status |  |
| occupation |  |
| spouse_name |  |
| customer_status |  |
| category |  |
| country_of_residence |  |
| is_staff |  |
| branch_code |  |
| vat_number |  |
| id_no_masked |  |
| id_no_last4 |  |
| party_type | B |
| id_type | B |
| segment | B |

| contact_type |  |
|---|---|
| contact_key | BK |
| person_key | BK |
| contact_value |  |
| contact_value_masked |  |
| usage_code |  |
| city |  |
| post_code |  |
| country |  |

| person_key | BK |
|---|---|
| account_key | BK |
| relation_type |  |
| amount_of_guarantee |  |
| date_of_guarantee |  |

| parent_account_key |  |
|---|---|
| child_account_key |  |

| collateral_no |  |
|---|---|
| asset_key | BK |
| account_key | BK |
| collateral_value |  |
| register_date |  |
| in_active |  |
| collateral_type |  |
| description |  |

| asset_ref |  |
|---|---|
| asset_key | BK |
| asset_type |  |
| description |  |
| address |  |
| town |  |
| post_code |  |
| county |  |
| country |  |

| efs_record_key |  |
|---|---|
| account_key | BK |
| person_key | BK |
| action_code |  |
| action_code_name |  |
| action_date |  |
| contact_at |  |
| user_code |  |
| comments |  |
| is_call |  |
| is_rpc |  |
| is_ptp |  |
| promise_status |  |
| promise_eval_status |  |
| promise_date |  |
| promise_amount |  |
| collection_phase |  |
| act_date_bucket |  |
| act_date_past_due_days |  |
| last_tdr_date |  |
| contact_result | B |
| action_contact_status | B |

| action_code |  |
|---|---|
| action_name |  |
| category |  |

| account_key | BK |
|---|---|
| assignment_scheme |  |
| assignee_code |  |
| assignee_name |  |
| assignment_start_date |  |
| assignment_end_date |  |
| assignment_start_total_balance |  |
| assignment_end_total_balance |  |
| distribution_area |  |

| account_key | BK |
|---|---|
| snapshot_year |  |
| snapshot_month |  |
| bucket |  |
| past_due_amount |  |
| snapshot_month_start |  |

| product_code |  |
|---|---|
| product_name |  |
| product_type |  |
| product_category |  |
| product_category_efs |  |

| branch_code |  |
|---|---|
| branch_name |  |
| address |  |
| phone |  |

| holiday_date |  |
|---|---|
| holiday_year |  |
| holiday_name |  |
| holiday_name_thai |  |
| holiday_weekday |  |

| plan_ref |  |
|---|---|
| ace_case_id |  |
| plan_status |  |
| plan_created_at |  |
| tdr_calculation_id |  |
| plan_published_at |  |
| associated_account_id |  |
| account_key | BK |
| booked_at |  |
| approved_at |  |
| submitted_at |  |
| closed_at |  |
| closed_reason |  |
| ca_approved_at |  |
| installments |  |
| recommended_installment |  |
| recommended_package |  |
| plan_status_as_of |  |

| source_system |  |
|---|---|
| business_date |  |
| started_at |  |
| completed_at |  |
| status |  |
| record_count |  |
| checksum |  |
| feed_version |  |
| is_complete |  |

| valuation_key | BK |
|---|---|
| asset_key | BK |
| appraisal_no |  |
| appraisal_type |  |
| appraised_value |  |
| forced_sale_value |  |
| appraisal_date |  |
| source_system |  |
| data_as_of |  |

| asset_key | BK |
|---|---|
| title_doc_no |  |
| plot_no |  |
| area_text |  |
| province |  |
| district |  |
| subdistrict |  |
| insured_value |  |
| insurance_expiry |  |
| lien_rank |  |
| source_system |  |
| data_as_of |  |

| asset_ref |  |
|---|---|
| asset_key | BK |
| asset_code |  |
| transfer_in_type |  |
| from_segment |  |
| transfer_in_date |  |
| book_value |  |
| auction_purchase_price |  |
| repossessed_date |  |
| stock_date |  |
| source_system |  |
| data_as_of |  |

| npa_sale_key |  |
|---|---|
| npa_asset_key |  |
| contract_date |  |
| sale_date |  |
| sale_price |  |
| transfer_fee |  |
| specific_business_tax |  |
| corporate_income_tax |  |
| incentive_amount |  |
| source_system |  |
| data_as_of |  |

| lawsuit_key |  |
|---|---|
| account_key | BK |
| lawsuit_no |  |
| black_case_no |  |
| red_case_no |  |
| court_name |  |
| claim_amount |  |
| filed_date |  |
| judgment_date |  |
| judgment_amount |  |
| lit_status |  |
| source_system |  |
| data_as_of |  |

| hearing_key |  |
|---|---|
| lawsuit_key |  |
| hearing_date |  |
| hearing_type |  |
| next_date |  |
| source_system |  |
| data_as_of |  |

| pod_key |  |
|---|---|
| account_key | BK |
| notice_ref |  |
| sent_date |  |
| barcode |  |
| callback_date |  |
| delivery_status |  |
| sent_type |  |
| source_system |  |
| data_as_of |  |

| write_off_key |  |
|---|---|
| account_key | BK |
| amount |  |
| posted_date |  |
| responsibility_center |  |
| cost_center |  |
| gl_product |  |
| source_system |  |
| data_as_of |  |

| score_key |  |
|---|---|
| account_key | BK |
| model_code |  |
| model_version |  |
| score_value |  |
| estimate_value |  |
| route_code |  |
| scored_at |  |
| source_system |  |
| data_as_of |  |

| person_key | BK |
|---|---|
| account_no |  |
| account_key | BK |
| product_type |  |
| product_status |  |
| data_as_of |  |

| credit_decision_key |  |
|---|---|
| account_key | BK |
| nleads_ref |  |
| credit_result |  |
| credit_result_reason |  |
| decided_at |  |
| source_system |  |
| data_as_of |  |

| esign_key |  |
|---|---|
| account_key | BK |
| external_ref |  |
| requested_at |  |
| status |  |
| source_system |  |
| data_as_of |  |

| entra_group |  |
|---|---|
| role_code |  |
| source_system |  |
| data_as_of |  |

## All 108 references

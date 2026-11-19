<!-- source: 06 Data/Recovery Workbench Entity Relationship Diagram v4.html -->
<!-- converted: 2026-11-16 from HTML -->

> **Source:** `06 Data/Recovery Workbench Entity Relationship Diagram v4.html`  
> **Converted from:** HTML

Recovery Workbench Entity Relationship Diagram

## The ACE boundary and the references between data products

122 objects: 88 Workbench tables, 4 extension tables and 30 ACE source views, with 104 references. The 14 data products hold 97 of them; OPS, AGT and RPT hold the other 25. The views are external and read only, and their boxes are dashed. The 18 business-key links carry no foreign key into ACE; the other 86 references are ordinary foreign keys inside the recovery schema.

**Objects**122**Workbench tables**88**Extension tables**4**ACE views, read only**30**References**104**Business-key links**18

### Data products, their ACE views and the references between them

Each purple box is a data product with its Workbench and extension tables; DP03 Case and ownership is shaded. Each amber box holds the ACE views of that data product, marked T1 or T2. A line joins two boxes with the number of references between them; the dot is at the referring end. Purple dashed lines are foreign keys inside the recovery schema (42 across products). Amber long-dashed lines are logical links by ACE business key with no foreign key (18 across products, 18 in all).

**Workbench table**Extension table, 1:1 by ACE business key**ACE view, Tier 1 (ACE table today)**ACE view, Tier 2 (RWB-ACE-001)**Entity of another data product**Foreign key**Logical link: business key, no foreign key

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
| DP14 | Reference data | 31 | 26 | 0 | 5 | Recovery Workbench |
| OPS | Loads and operations | 14 | 13 | 0 | 1 | Recovery Workbench; ACE for the batch record |
| AGT | Agent runtime | 8 | 8 | 0 | 0 | Recovery Workbench |
| RPT | Reporting | 3 | 3 | 0 | 0 | Recovery Workbench |

### References between data products

54 references cross a data product boundary and 50 stay inside one. Each row reads from the first data product to the second, and is ordered by count.

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

**Workbench table**Extension table, 1:1 by ACE business key**ACE view, Tier 1 (ACE table today)**ACE view, Tier 2 (RWB-ACE-001)**Entity of another data product**Foreign key**Logical link: business key, no foreign key

References from other data products to these entities are on the tabs of those products, on the overview and on the ACE views tab.

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

**Workbench table**Extension table, 1:1 by ACE business key**ACE view, Tier 1 (ACE table today)**ACE view, Tier 2 (RWB-ACE-001)**Entity of another data product**Foreign key**Logical link: business key, no foreign key

References from other data products to these entities are on the tabs of those products, on the overview and on the ACE views tab.

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

**Workbench table**Extension table, 1:1 by ACE business key**ACE view, Tier 1 (ACE table today)**ACE view, Tier 2 (RWB-ACE-001)**Entity of another data product**Foreign key**Logical link: business key, no foreign key

References from other data products to these entities are on the tabs of those products, on the overview and on the ACE views tab.

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

**Workbench table**Extension table, 1:1 by ACE business key**ACE view, Tier 1 (ACE table today)**ACE view, Tier 2 (RWB-ACE-001)**Entity of another data product**Foreign key**Logical link: business key, no foreign key

References from other data products to these entities are on the tabs of those products, on the overview and on the ACE views tab.

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

**Workbench table**Extension table, 1:1 by ACE business key**ACE view, Tier 1 (ACE table today)**ACE view, Tier 2 (RWB-ACE-001)**Entity of another data product**Foreign key**Logical link: business key, no foreign key

References from other data products to these entities are on the tabs of those products, on the overview and on the ACE views tab.

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

**Workbench table**Extension table, 1:1 by ACE business key**ACE view, Tier 1 (ACE table today)**ACE view, Tier 2 (RWB-ACE-001)**Entity of another data product**Foreign key**Logical link: business key, no foreign key

References from other data products to these entities are on the tabs of those products, on the overview and on the ACE views tab.

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

**Workbench table**Extension table, 1:1 by ACE business key**ACE view, Tier 1 (ACE table today)**ACE view, Tier 2 (RWB-ACE-001)**Entity of another data product**Foreign key**Logical link: business key, no foreign key

References from other data products to these entities are on the tabs of those products, on the overview and on the ACE views tab.

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

**Workbench table**Extension table, 1:1 by ACE business key**ACE view, Tier 1 (ACE table today)**ACE view, Tier 2 (RWB-ACE-001)**Entity of another data product**Foreign key**Logical link: business key, no foreign key

References from other data products to these entities are on the tabs of those products, on the overview and on the ACE views tab.

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

**Workbench table**Extension table, 1:1 by ACE business key**ACE view, Tier 1 (ACE table today)**ACE view, Tier 2 (RWB-ACE-001)**Entity of another data product**Foreign key**Logical link: business key, no foreign key

References from other data products to these entities are on the tabs of those products, on the overview and on the ACE views tab.

### References

| Entity | Field | Refers to | Reference | Kind |
|---|---|---|---|---|
| debt_sale_lot | buyer_partner_id | partner | Optional | Foreign key |
| debt_sale_account | lot_id | debt_sale_lot | Mandatory | Foreign key |
| debt_sale_account | account_key | v_ace_account | Mandatory | Business key, no foreign key |

## DP10 Documents and extracted fields

Documents against the case, the fields read from them, retention class and custody of originals

**System of record**Recovery Workbench document hub**How it reaches the Workbench**Held in the Workbench. The signature request and its status are read through recovery.v_ace_esign.**Freshness**As it changes**Objects**9

**Workbench table**Extension table, 1:1 by ACE business key**ACE view, Tier 1 (ACE table today)**ACE view, Tier 2 (RWB-ACE-001)**Entity of another data product**Foreign key**Logical link: business key, no foreign key

References from other data products to these entities are on the tabs of those products, on the overview and on the ACE views tab.

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

**Workbench table**Extension table, 1:1 by ACE business key**ACE view, Tier 1 (ACE table today)**ACE view, Tier 2 (RWB-ACE-001)**Entity of another data product**Foreign key**Logical link: business key, no foreign key

References from other data products to these entities are on the tabs of those products, on the overview and on the ACE views tab.

### References

No references.

## DP12 Decision log

One entry per decision with the rule, model and agent versions, inputs, recommendation, approval, actions and outcome

**System of record**Recovery Workbench**How it reaches the Workbench**Held in the Workbench.**Freshness**As it changes**Objects**2

**Workbench table**Extension table, 1:1 by ACE business key**ACE view, Tier 1 (ACE table today)**ACE view, Tier 2 (RWB-ACE-001)**Entity of another data product**Foreign key**Logical link: business key, no foreign key

References from other data products to these entities are on the tabs of those products, on the overview and on the ACE views tab.

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

**Workbench table**Extension table, 1:1 by ACE business key**ACE view, Tier 1 (ACE table today)**ACE view, Tier 2 (RWB-ACE-001)**Entity of another data product**Foreign key**Logical link: business key, no foreign key

References from other data products to these entities are on the tabs of those products, on the overview and on the ACE views tab.

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

**System of record**Recovery Workbench**How it reaches the Workbench**Held in the Workbench and versioned. Source codes and descriptions are read through v_ace_product, v_ace_branch, v_ace_efs_action_code, v_ace_holiday and v_ace_iam_group rather than loaded.**Freshness**By versioned load**Objects**31

**Workbench table**Extension table, 1:1 by ACE business key**ACE view, Tier 1 (ACE table today)**ACE view, Tier 2 (RWB-ACE-001)**Entity of another data product**Foreign key**Logical link: business key, no foreign key

References from other data products to these entities are on the tabs of those products, on the overview and on the ACE views tab.

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

## OPS Loads and operations

The freshness stamp, reconciliation, outbound interfaces, jobs, feature flags, the outbox and idempotency records that run the Workbench. No inbound load: the ACE batch record is read through v_ace_batch_status

**System of record**Recovery Workbench; ACE for the batch record**How it reaches the Workbench**Held in the Workbench; the ACE batch business date is read through recovery.v_ace_batch_status**Freshness**As it changes; batch status at each ACE batch**Objects**14

**Workbench table**Extension table, 1:1 by ACE business key**ACE view, Tier 1 (ACE table today)**ACE view, Tier 2 (RWB-ACE-001)**Entity of another data product**Foreign key**Logical link: business key, no foreign key

References from other data products to these entities are on the tabs of those products, on the overview and on the ACE views tab.

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

**Workbench table**Extension table, 1:1 by ACE business key**ACE view, Tier 1 (ACE table today)**ACE view, Tier 2 (RWB-ACE-001)**Entity of another data product**Foreign key**Logical link: business key, no foreign key

References from other data products to these entities are on the tabs of those products, on the overview and on the ACE views tab.

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

**Workbench table**Extension table, 1:1 by ACE business key**ACE view, Tier 1 (ACE table today)**ACE view, Tier 2 (RWB-ACE-001)**Entity of another data product**Foreign key**Logical link: business key, no foreign key

References from other data products to these entities are on the tabs of those products, on the overview and on the ACE views tab.

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

### Diagram

The 30 views in two tiers, the ACE tables each reads, and the 18 logical links from the recovery schema. No line carries a foreign key: ACE cascades deletes on account, so integrity is checked by the read model and reconciliation rule REC-05. The fields of each view are on its data product tab.

**Workbench table**Extension table, 1:1 by ACE business key**ACE view, Tier 1 (ACE table today)**ACE view, Tier 2 (RWB-ACE-001)**Entity of another data product**Foreign key**Logical link: business key, no foreign key

## All 104 references

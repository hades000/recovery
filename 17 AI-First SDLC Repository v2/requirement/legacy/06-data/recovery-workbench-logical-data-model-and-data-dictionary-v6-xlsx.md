<!-- source: 06 Data/Recovery Workbench Logical Data Model and Data Dictionary v6.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `06 Data/Recovery Workbench Logical Data Model and Data Dictionary v6.xlsx`  
> **Converted from:** XLSX

## Entities

| Entities |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|
| 108 entities. Field counts are calculated from the Fields tab. Every entity also carries the standard columns. |  |  |  |  |  |  |  |  |
| Entity | Business name | Subject area | Data product | What it is | System of record | ACE | Fields | Personal data fields |
| recovery_case | Recovery case | Case | DP03 | One recovery case per customer per product, from 90 days past due to close. | Workbench | Extend ACE Case |  |  |
| case_account | Case account | Case | DP03 | Links each loan account to the case it is recovered under. | Workbench | New |  |  |
| case_party | Case party | Case | DP03 | The role each party plays on a case. | Workbench | New |  |  |
| deviation | Deviation | Case | DP03 | A deviation X1 to X7 raised on a case. | Workbench | New |  |  |
| queue | Queue | Work management | DP03 | A queue of work belonging to one team and one role. | Workbench | Extend ACE work queue |  |  |
| assignment | Assignment | Work management | DP03 | Who holds a case or a task and from when. | Workbench | Reuse ACE Assignee |  |  |
| task | Task | Work management | DP03 | A unit of work on a case: a CMMN human, customer, partner or decision task. | Workbench | New |  |  |
| timer | Timer | Work management | DP03 | A running clock on a case: a service level, a legal period or an offer validity. | Workbench | New |  |  |
| party | Party | Party | DP02 | A person or company with a role on one or more cases. | SCBPDM via COLLINS | Extend ACE Customer |  |  |
| contact_point | Contact point | Party | DP02 | A way to reach a party, with its consent and whether it works. | Workbench | New |  |  |
| loan_account | Loan account | Account and arrears | DP01 | A loan account in the core bank. | Core bank (ALS) via COLLINS | Reuse ACE Account |  |  |
| account_payment | Account payment | Account and arrears | DP01 | A payment posted to a loan account. | Core bank (ALS) via COLLINS | Reuse ACE Payment |  |  |
| collateral | Collateral | Collateral and asset | DP06 | Property or vehicle securing one or more accounts. | CCMS | Extend ACE Collateral |  |  |
| account_collateral | Account collateral | Collateral and asset | DP06 | Which collateral secures which account. | Workbench | New |  |  |
| valuation | Valuation | Collateral and asset | DP06 | An appraisal of collateral or an asset. | SVAF | New |  |  |
| asset | Asset | Collateral and asset | DP06 | An asset the bank holds after repossession, deed in lieu or auction purchase. | AMIS for property; RPS for vehicles | Extend ACE Asset |  |  |
| treatment | Treatment | Treatment | DP04 | A resolution put to the customer or carried out on the case, with its terms and outcome. | Workbench | New; restructure plans reuse ACE TDRCalculation |  |  |
| guarantee_claim | Guarantee claim | Treatment | DP04 | A claim against a Thai Credit Guarantee Corporation guarantee or an insurer. | Workbench | New |  |  |
| legal_action | Legal action | Legal | DP07 | A notice, lawsuit, appeal, enforcement or bankruptcy action on a case. | LIT for court records; Workbench for instructions | New |  |  |
| notice | Notice | Legal | DP07 | A demand, recall or statutory notice and its proof of delivery. | Workbench; WIN for dispatch | New |  |  |
| hearing | Hearing | Legal | DP07 | A court hearing on a legal action. | LIT | New |  |  |
| partner | Partner | Partner | DP08 | An outside firm the bank places work with. | Workbench | New |  |  |
| partner_instruction | Partner instruction | Partner | DP08 | Work placed with a partner on a case. | Workbench | New |  |  |
| listing | Listing | Disposal and debt sale | DP06 | An asset offered for sale, with its prices and rounds. | Workbench | New |  |  |
| asset_sale | Asset sale | Disposal and debt sale | DP06 | The sale of an asset. | AMIS | New |  |  |
| debt_sale_lot | Debt sale lot | Disposal and debt sale | DP09 | A lot of accounts offered to debt buyers. | Workbench | New |  |  |
| debt_sale_account | Debt sale account | Disposal and debt sale | DP09 | An account in a debt sale lot. | Workbench | New |  |  |
| interaction | Interaction | Interaction | DP05 | One entry in the interaction ledger: a contact, letter, promise, payment or hand-over. | Workbench | Extend ACE activity log |  |  |
| document | Document | Document | DP10 | A document held against a case. | Workbench document hub | Extend ACE Attachment |  |  |
| document_field | Document field | Document | DP10 | A field read from a document. | Workbench document hub | New |  |  |
| document_custody | Document custody | Document | DP10 | Each movement of an original document. | Workbench | New |  |  |
| decision_log_entry | Decision log entry | Decision and control | DP12 | One record per decision. Append only and hash chained. | Workbench | New |  |  |
| score | Score | Decision and control | DP11 | A score or estimate COLLINS returns for an account or case. | COLLINS | Reuse ACE |  |  |
| proceeds | Proceeds | Money and closure | DP13 | Money received on a case and what it was matched to. | Workbench | New |  |  |
| write_off | Write-off | Money and closure | DP13 | A write-off of the balance on a case. | GL for posting; Workbench for the decision | New |  |  |
| rule_row | Rule | Reference and access | DP14 | One versioned routing rule or sentry. | Workbench | New |  |  |
| delegation_limit | Delegation limit | Reference and access | DP14 | An approval limit by decision, level, product and amount. | Workbench | New |  |  |
| lov_value | List value | Reference and access | DP14 | A value in a list of values. | Workbench | New |  |  |
| role | Role | Reference and access | DP14 | A Workbench role, held as data. | Workbench | Extend ACE RBAC |  |  |
| permission | Permission | Reference and access | DP14 | What a role may do in one capability area. | Workbench | Extend ACE RBAC |  |  |
| template | Template | Reference and access | DP14 | A letter or notice template. | Workbench | New |  |  |
| data_product | Data product | Reference and access | DP14 | One of the 14 data products, with its single system of record, owner and refresh cycle. | Workbench | New |  |  |
| data_product_access | Data product access | Reference and access | DP14 | Which role may read which data product, by version. | Workbench | New |  |  |
| data_product_load | Data product load | Loads and operations | OPS | The freshness stamp of a data product for one business date. | Workbench | New |  |  |
| data_contract | Data contract | Loads and operations | OPS | A versioned data contract with one source system, confirmed by its system owner. | Workbench | New |  |  |
| sys_objects | Sys objects | Reference and access | DP14 | The metadata registry of entities: one row per object in the data dictionary. | Workbench | New |  |  |
| sys_fields | Sys fields | Reference and access | DP14 | The metadata registry of fields: the data dictionary held as data. | Workbench | New |  |  |
| sys_field_version | Sys field version | Reference and access | DP14 | Each version of a field definition, kept when the definition changes. | Workbench | New |  |  |
| load_run | Load run | Loads and operations | OPS | One run of a data load or job step, with its checks and row counts. | Workbench | New |  |  |
| dq_exception | Dq exception | Loads and operations | OPS | A record a load check or data quality rule held, until it passes again. | Workbench | New |  |  |
| dq_rule | Dq rule | Loads and operations | OPS | A versioned data quality row rule run on a P1 table. | Workbench | New |  |  |
| source_field_map | Source field map | Loads and operations | OPS | How a source field maps to a Workbench field, by interface and mapping version. | Workbench | New |  |  |
| source_code_map | Source code map | Loads and operations | OPS | How a source code maps to a Workbench list value, by interface and map version. | Workbench | New |  |  |
| tracker_inventory | Tracker inventory | Loads and operations | OPS | A team's Excel or SharePoint tracker, its decision and its load, sign-off and retirement. | Workbench | New |  |  |
| tracker_row | Tracker row | Loads and operations | OPS | One row loaded from a tracker file, with its non-personal fields. | Workbench | New |  |  |
| case_list_row | Case list row | Reporting | DP03 | One row of the daily case list per case account and business date, published to Power BI. | Workbench | New |  |  |
| collections_history | Collections history | Interaction | DP05 | An EFS contact or promise on an account, loaded from the COLLINS daily batch. | Workbench | New |  |  |
| reconciliation_result | Reconciliation result | Loads and operations | OPS | The daily reconciliation of the case list to ALS by product group. | Workbench | New |  |  |
| lake_copy_watermark | Lake copy watermark | Loads and operations | OPS | How far a copy to the data lake has reached, for example the decision log copy. | Workbench | New |  |  |
| retention_rule | Retention rule | Reference and access | DP14 | How long rows of a table or a retention class are kept and what happens at the end, by version. | Workbench | New |  |  |
| dp_treatment | Dp treatment | Treatment | DP04 | The copy of each treatment for a business date in the DP04 data product. | Workbench | New |  |  |
| dp_guarantee_claim | Dp guarantee claim | Treatment | DP04 | The copy of each guarantee claim for a business date in the DP04 data product. | Workbench | New |  |  |
| interface_config | Interface config | Loads and operations | OPS | The settings of one file interface, by version. | Workbench | New |  |  |
| interface_run | Interface run | Loads and operations | OPS | One inbound file received by the adapter and the result of its file checks. | Workbench | New |  |  |
| interface_signoff | Interface signoff | Loads and operations | OPS | The data steward's sign-off that an interface no longer needs manual handling. | Workbench | New |  |  |
| outbound_item | Outbound item | Loads and operations | OPS | One outbound file waiting to be sent, sent or in the exception queue. | Workbench | New |  |  |
| processed_event | Processed event | Loads and operations | OPS | An event or work key a consumer has already processed, so a repeat is ignored and counted. | Workbench | New |  |  |
| idempotency_key | Idempotency key | Loads and operations | OPS | The stored response of an API request sent with an Idempotency-Key header, kept 24 hours. | Workbench | New |  |  |
| outbox_event | Outbox event | Loads and operations | OPS | An application event or outbound work request written in the same transaction as the change. | Workbench | New |  |  |
| outbox_delivery | Outbox delivery | Loads and operations | OPS | The delivery of one outbox event to one consumer, with its retries. | Workbench | New |  |  |
| feature_flag | Feature flag | Loads and operations | OPS | A feature flag with its value per environment, owner and removal date. | Workbench | New |  |  |
| feature_flag_change | Feature flag change | Loads and operations | OPS | One change of a feature flag value in one environment. | Workbench | New |  |  |
| job_catalog | Job catalog | Loads and operations | OPS | A scheduled job with its owner, run book and expected duration. | Workbench | New |  |  |
| party_product | Party product | Party | DP02 | Another product the party holds at the bank, from the customer profile. | Workbench | New |  |  |
| efs_ledger_outcome | Efs ledger outcome | Reference and access | DP14 | Which EFS action codes enter the interaction ledger and on which channel. | Workbench | New |  |  |
| case_entry_exclusion | Case entry exclusion | Case | DP03 | An account at 90 days past due that an exclusion rule kept out of recovery on a business date. | Workbench | New |  |  |
| queue_member | Queue member | Work management | DP03 | A person who works a queue, with personal capacity and skills, by version. | Workbench | New |  |  |
| queue_measure | Queue measure | Reporting | DP03 | One snapshot of a queue's counts, ageing and breaches, published when it reconciles to the case list. | Workbench | New |  |  |
| parameter_catalog | Parameter catalog | Reference and access | DP14 | The definition of every parameter and environment setting, with its owner and default. | Workbench | New |  |  |
| parameter_value | Parameter value | Reference and access | DP14 | An approved, dated value version of a parameter per environment and product group. | Workbench | New |  |  |
| reference_version | Reference version | Reference and access | DP14 | One version of a reference or rule table, with its author, approver, checks and change checklist. | Workbench | New |  |  |
| reference_row | Reference row | Reference and access | DP14 | One row of a reference table version held as data. | Workbench | New |  |  |
| rule_test_case | Rule test case | Reference and access | DP14 | A test case of the rule table test harness, with its expected and actual result. | Workbench | New |  |  |
| masking_rule | Masking rule | Reference and access | DP14 | Which role sees which personal data field unmasked, by version. | Workbench | New |  |  |
| role_conflict | Role conflict | Reference and access | DP14 | A pair of roles one person may not hold together, by version. | Workbench | New |  |  |
| partner_user | Partner user | Reference and access | DP14 | A partner user's identity bound to one partner firm and one partner role. | Workbench | New |  |  |
| document_type | Document type | Reference and access | DP14 | A document type, the fields extracted from it and its Legal and NPA sign-off, by version. | Workbench | New |  |  |
| document_checklist_item | Document checklist item | Reference and access | DP14 | A document type required or expected for a case stage and route, by checklist version. | Workbench | New |  |  |
| case_document_check | Case document check | Document | DP10 | The latest document completeness check of a case against its checklist. | Workbench | New |  |  |
| document_hub_parameter | Document hub parameter | Reference and access | DP14 | A document hub parameter value, by version. | Workbench | New |  |  |
| document_intake | Document intake | Document | DP10 | A file received by the document hub, from scan to OCR, classification, extraction, matching and review. | Workbench | New |  |  |
| document_text | Document text | Document | DP10 | The OCR text of one page of an intake item. | Workbench | New |  |  |
| retention_action | Retention action | Document | DP10 | What the monthly retention job did with one document. | Workbench | New |  |  |
| merge_field | Merge field | Reference and access | DP14 | A merge code a template may use and the field that supplies its value, by catalog version. | Workbench | New |  |  |
| signature_request | Signature request | Document | DP10 | A request for a party to sign a generated document, and its result. | Workbench | New |  |  |
| approval | Approval | Decision and control | DP12 | An item waiting for approval, routed to the level the delegation of authority requires. | Workbench | New |  |  |
| payment_match_rule | Payment match rule | Reference and access | DP14 | A rule for matching a payment to a plan installment, by version. | Workbench | New |  |  |
| measure_definition | Measure definition | Reporting | RPT | The agreed definition of a reported measure, by version. | Workbench | New |  |  |
| measure_snapshot | Measure snapshot | Reporting | RPT | The value of one measure for a business date, product and dimension value. | Workbench | New |  |  |
| measure_publish | Measure publish | Reporting | RPT | Whether the day's dashboard data set was published or held after reconciling to the case list. | Workbench | New |  |  |
| agent_policy | Agent policy | Agent runtime | AGT | A version of an agent's policy: model, tools, autonomy, limits and fallback. | Workbench | New |  |  |
| agent_prompt | Agent prompt | Agent runtime | AGT | A version of an agent's prompt text. | Workbench | New |  |  |
| agent_run | Agent run | Agent runtime | AGT | One call of an agent or model, with its versions, checks, answer, cost and fallback. | Workbench | New |  |  |
| agent_sample | Agent sample | Agent runtime | AGT | One labeled subject in a versioned evaluation sample. | Workbench | New |  |  |
| agent_evaluation_run | Agent evaluation run | Agent runtime | AGT | One evaluation of an agent version against a sample. | Workbench | New |  |  |
| agent_evaluation | Agent evaluation | Agent runtime | AGT | The score of one approach on one label key in an evaluation run. | Workbench | New |  |  |
| agent_feedback | Agent feedback | Agent runtime | AGT | A person's verdict on an agent answer. | Workbench | New |  |  |
| agent_alert | Agent alert | Agent runtime | AGT | A cost cap or drift alert raised for an agent. | Workbench | New |  |  |
| Total |  |  |  |  |  |  |  |  |

## Fields

| Data dictionary |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1256 fields in 108 entities, in the bank TSD section T3 form. Filter by entity, subject area, source system or personal data. |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| BR Field ID | Entity | Field | Data type | Physical type | Length | Mandatory | Default | List of values | Key | Refers to | Source system | Source field | Personal data | Meaning |
| DF-CAS-001 | recovery_case | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the case |
| DF-CAS-002 | recovery_case | case_no | TEXT | varchar(18) | 18 | Yes | None | None | UK | None | Workbench | None | No | Case number RW-YYYY-NNNNNN, issued at creation and never reused |
| DF-CAS-003 | recovery_case | product_group | LOV | varchar(15) | 15 | Yes | None | LOV-PRODUCT | None | None | Core bank (ALS) via COLLINS | Product_Category_Host | No | Mortgage, hire purchase, SSME or unsecured |
| DF-CAS-004 | recovery_case | primary_customer_id | CROSS_REF | uuid |  | Yes | None | None | FK | party | Workbench | None | No | The borrower the case is opened for |
| DF-CAS-005 | recovery_case | status | LOV | varchar(20) | 20 | Yes | NEW | LOV-CASE-STATUS | None | None | Workbench | None | No | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed |
| DF-CAS-006 | recovery_case | stage_code | LOV | varchar(20) | 20 | No | None | LOV-STAGE | None | None | Workbench | None | No | The stage the case is on |
| DF-CAS-007 | recovery_case | route_state | TEXT | varchar(60) | 60 | No | None | None | None | None | Workbench | None | No | The routing state from the rule set, for example FIRM_INSTRUCTED |
| DF-CAS-008 | recovery_case | route_code | LOV | varchar(4) | 4 | No | None | LOV-ROUTE | None | None | Workbench | None | No | The approved route R1 to R8 |
| DF-CAS-009 | recovery_case | owner_user_id | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | The case owner |
| DF-CAS-010 | recovery_case | queue_id | CROSS_REF | uuid |  | No | None | None | FK | queue | Workbench | None | No | The queue the case is in |
| DF-CAS-011 | recovery_case | team_code | LOV | varchar(20) | 20 | No | None | LOV-TEAM | None | None | Workbench | None | No | The owning team, used by scope rules |
| DF-CAS-012 | recovery_case | region_code | LOV | varchar(10) | 10 | No | None | LOV-REGION | None | None | Workbench | None | No | The owning region, used by scope rules |
| DF-CAS-013 | recovery_case | entry_date | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | The date the case entered recovery |
| DF-CAS-014 | recovery_case | dpd_at_entry | NUMBER | integer |  | Yes | None | None | None | None | Core bank (ALS) via COLLINS | DELAY_DAYS | No | Days past due on the entry date |
| DF-CAS-015 | recovery_case | exposure_band | LOV | varchar(10) | 10 | No | None | LOV-EXPOSURE | None | None | Workbench | None | No | Exposure band set from the outstanding balance at entry |
| DF-CAS-016 | recovery_case | total_outstanding_at_entry | NUMBER | numeric(18,2) | 18,2 | Yes | None | None | None | None | Core bank (ALS) via COLLINS | TOTAL_BALANCE | No | Total outstanding across linked accounts at entry, in baht |
| DF-CAS-017 | recovery_case | prescription_date | DATE | date |  | No | None | None | None | None | Workbench | None | No | The earliest date a legal claim on the case expires |
| DF-CAS-018 | recovery_case | stage_clock_start | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the current state started, for the service level |
| DF-CAS-019 | recovery_case | deviation_open | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True while any deviation X1 to X7 is open |
| DF-CAS-020 | recovery_case | legal_hold | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True while a legal hold stops normal routing |
| DF-CAS-021 | recovery_case | rule_version | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | The rule version the current state was entered under |
| DF-CAS-022 | recovery_case | closed_date | DATE | date |  | No | None | None | None | None | Workbench | None | No | The date the case closed |
| DF-CAS-023 | recovery_case | closure_reason | LOV | varchar(20) | 20 | No | None | LOV-CLOSURE | None | None | Workbench | None | No | Cured, settled, realized, sold, written off, insurance settled, merged, canceled |
| DF-CAS-046 | recovery_case | plan_ref | TEXT | varchar(30) | 30 | No | None | None | None | None | ACE | None | No | Reference of the ACE restructure plan on the case |
| DF-CAS-047 | recovery_case | plan_status | LOV | varchar(10) | 10 | No | None | LOV-PLAN-STATUS | None | None | ACE | None | No | ACE plan status: created, approved, booked or broken |
| DF-CAS-048 | recovery_case | plan_status_as_of | DATE | date |  | No | None | None | None | None | ACE | None | No | Date of the plan status in ACE |
| DF-CAS-049 | recovery_case | next_action_text | TEXT | varchar(1000) | 1000 | No | None | None | None | None | Workbench | None | No | The next action, copied from action_text of the rule that moved the case |
| DF-CAS-050 | recovery_case | next_action_owner_role | LOV | varchar(20) | 20 | No | None | LOV-ROLE | None | None | Workbench | None | No | Owner role of the next action, from owner_role of the rule |
| DF-CAS-051 | recovery_case | next_action_due_date | DATE | date |  | No | None | None | None | None | Workbench | None | No | Due date from the rule's timer_spec or the service levels and timers table |
| DF-CAS-052 | recovery_case | next_action_rule_id | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | Rule ID that set the next action |
| DF-CAS-053 | recovery_case | next_action_waiting | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True when the next action waits on a customer, party or partner |
| DF-CAS-054 | recovery_case | last_allocation_date | DATE | date |  | No | None | None | None | None | Workbench | None | No | Business date of the last allocation run that decided the case |
| DF-CAS-055 | recovery_case | status_before_hold | LOV | varchar(20) | 20 | No | None | LOV-CASE-STATUS | None | None | Workbench | None | No | The case status when a legal hold was placed, restored when it is lifted |
| DF-CAS-024 | case_account | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the case account link |
| DF-CAS-025 | case_account | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | None | No | The recovery_case this record belongs to |
| DF-CAS-026 | case_account | account_id | CROSS_REF | uuid |  | Yes | None | None | FK | loan_account | Workbench | None | No | The loan_account this record belongs to |
| DF-CAS-027 | case_account | is_primary | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True for the account the case was opened on |
| DF-CAS-028 | case_account | linked_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the account joined the case |
| DF-CAS-029 | case_account | linked_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Date the account left the case |
| DF-CAS-030 | case_party | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the case party link |
| DF-CAS-031 | case_party | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | None | No | The recovery_case this record belongs to |
| DF-CAS-032 | case_party | party_id | CROSS_REF | uuid |  | Yes | None | None | FK | party | Workbench | None | No | The party this record belongs to |
| DF-CAS-033 | case_party | party_role | LOV | varchar(20) | 20 | Yes | None | LOV-PARTY-ROLE | None | None | Workbench | None | No | Borrower, co-borrower, guarantor, authorized signatory, heir |
| DF-CAS-034 | case_party | role_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the role starts |
| DF-CAS-035 | case_party | role_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Date the role ends |
| DF-CAS-036 | deviation | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the deviation |
| DF-CAS-037 | deviation | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | None | No | The recovery_case this record belongs to |
| DF-CAS-038 | deviation | deviation_code | LOV | varchar(3) | 3 | Yes | None | LOV-DEVIATION | None | None | Workbench | None | No | X1 to X7 |
| DF-CAS-039 | deviation | raised_at | DATE | timestamptz |  | Yes | None | None | None | None | Workbench | None | No | When it was raised |
| DF-CAS-040 | deviation | raised_by | LOV | varchar(20) | 20 | Yes | None | LOV-RAISED-BY | None | None | Workbench | None | No | Screening agent, rule, officer, customer contact |
| DF-CAS-041 | deviation | paused_state | TEXT | varchar(60) | 60 | Yes | None | None | None | None | Workbench | None | No | The routing state the case was in when paused |
| DF-CAS-042 | deviation | handler_user_id | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | The named handler |
| DF-CAS-043 | deviation | contact_stop | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True when customer contact is stopped |
| DF-CAS-044 | deviation | cleared_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When it cleared |
| DF-CAS-045 | deviation | outcome | LOV | varchar(20) | 20 | No | None | LOV-DEV-OUTCOME | None | None | Workbench | None | No | Returned, re-routed, case ended |
| DF-WRK-001 | queue | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the queue |
| DF-WRK-002 | queue | queue_code | TEXT | varchar(30) | 30 | Yes | None | None | UK | None | Workbench | None | No | Queue code |
| DF-WRK-003 | queue | queue_name | TEXT | varchar(100) | 100 | Yes | None | None | None | None | Workbench | None | No | Queue name |
| DF-WRK-004 | queue | team_code | LOV | varchar(20) | 20 | Yes | None | LOV-TEAM | None | None | Workbench | None | No | Team the queue belongs to |
| DF-WRK-005 | queue | role_code | LOV | varchar(20) | 20 | Yes | None | LOV-ROLE | None | None | Workbench | None | No | Role that works the queue |
| DF-WRK-006 | queue | assignment_method | LOV | varchar(20) | 20 | Yes | ROUND_ROBIN | LOV-ASSIGN | None | None | Workbench | None | No | Round robin, lowest load, named owner, skill |
| DF-WRK-007 | queue | capacity_cap | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Most open cases one person may hold in the queue |
| DF-WRK-008 | queue | overflow_queue_id | CROSS_REF | uuid |  | No | None | None | FK | queue | Workbench | None | No | Queue that receives overflow |
| DF-WRK-037 | queue | rr_cursor_user_id | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | The member last given a case by round robin in the queue |
| DF-WRK-038 | queue | table_version | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | The QUEUE reference version applied to the row |
| DF-WRK-009 | assignment | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the assignment |
| DF-WRK-010 | assignment | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | None | No | The recovery_case this record belongs to |
| DF-WRK-011 | assignment | task_id | CROSS_REF | uuid |  | No | None | None | FK | task | Workbench | None | No | The task this record belongs to |
| DF-WRK-012 | assignment | assignee_user_id | USER_REF | uuid |  | Yes | None | None | None | None | Workbench | None | No | The person or service identity assigned |
| DF-WRK-013 | assignment | assigned_at | DATE | timestamptz |  | Yes | now() | None | None | None | Workbench | None | No | When assigned |
| DF-WRK-014 | assignment | ended_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the assignment ended |
| DF-WRK-015 | assignment | reason | LOV | varchar(20) | 20 | Yes | None | LOV-ASSIGN-REASON | None | None | Workbench | None | No | Allocation, transfer, rebalance, manual, escalation |
| DF-WRK-016 | assignment | rule_id | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | The rule that made the assignment |
| DF-WRK-039 | assignment | queue_id | CROSS_REF | uuid |  | No | None | None | FK | queue | Workbench | None | No | The queue the assignment placed the case in |
| DF-WRK-040 | assignment | transfer_reason_code | LOV | varchar(20) | 20 | No | None | LOV-TRANSFER-REASON | None | None | Workbench | None | No | Coded reason for a manual transfer or move |
| DF-WRK-017 | task | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the task |
| DF-WRK-018 | task | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | None | No | The recovery_case this record belongs to |
| DF-WRK-019 | task | task_code | TEXT | varchar(60) | 60 | Yes | None | None | None | None | Workbench | None | No | The task in the case model, for example VERIFY_PACK |
| DF-WRK-020 | task | element_type | LOV | varchar(20) | 20 | Yes | None | LOV-ELEMENT | None | None | Workbench | None | No | Human, customer, partner or decision task, milestone, event listener |
| DF-WRK-021 | task | discretion | LOV | varchar(15) | 15 | Yes | None | LOV-DISCRETION | None | None | Workbench | None | No | Automatic, discretionary, required |
| DF-WRK-022 | task | status | LOV | varchar(15) | 15 | Yes | OPEN | LOV-TASK-STATUS | None | None | Workbench | None | No | Open, in progress, done, canceled |
| DF-WRK-023 | task | owner_role | LOV | varchar(20) | 20 | No | None | LOV-ROLE | None | None | Workbench | None | No | Role that owns the task |
| DF-WRK-024 | task | due_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the task is due |
| DF-WRK-025 | task | completed_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When it completed |
| DF-WRK-026 | task | outcome_code | TEXT | varchar(40) | 40 | No | None | None | None | None | Workbench | None | No | The event the task produced |
| DF-WRK-027 | timer | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the timer |
| DF-WRK-028 | timer | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | None | No | The recovery_case this record belongs to |
| DF-WRK-029 | timer | task_id | CROSS_REF | uuid |  | No | None | None | FK | task | Workbench | None | No | The task this record belongs to |
| DF-WRK-030 | timer | timer_type | LOV | varchar(20) | 20 | Yes | None | LOV-TIMER | None | None | Workbench | None | No | Service level, notice period, cure period, prescription, hearing deadline, offer validity, holding age, claim deadline |
| DF-WRK-031 | timer | started_at | DATE | timestamptz |  | Yes | None | None | None | None | Workbench | None | No | When it started |
| DF-WRK-032 | timer | expires_at | DATE | timestamptz |  | Yes | None | None | None | None | Workbench | None | No | When it expires |
| DF-WRK-033 | timer | warn_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the warning is raised |
| DF-WRK-034 | timer | paused | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True while paused by a deviation. A prescription timer never pauses |
| DF-WRK-035 | timer | status | LOV | varchar(15) | 15 | Yes | RUNNING | LOV-TIMER-STATUS | None | None | Workbench | None | No | Running, paused, expired, stopped |
| DF-WRK-036 | timer | escalation_level | NUMBER | integer |  | Yes | 0 | None | None | None | Workbench | None | No | How many times it has escalated |
| DF-WRK-041 | timer | warned_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the warning was sent, so it is sent once |
| DF-WRK-042 | timer | treatment_id | CROSS_REF | uuid |  | No | None | None | FK | treatment | Workbench | None | No | The treatment a plan timer belongs to |
| DF-WRK-043 | timer | escalated_to_role | LOV | varchar(20) | 20 | No | None | LOV-ROLE | None | None | Workbench | None | No | Role the breach was last escalated to |
| DF-WRK-044 | timer | escalated_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the timer last escalated |
| DF-PTY-001 | party | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the party |
| DF-PTY-002 | party | cif_no | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | SCBPDM via COLLINS | CIF | Yes | Customer number in the bank |
| DF-PTY-003 | party | party_type | LOV | varchar(15) | 15 | Yes | None | LOV-PARTY-TYPE | None | None | SCBPDM via COLLINS | None | No | Individual or juristic person |
| DF-PTY-004 | party | first_name | TEXT | varchar(100) | 100 | Yes | None | None | None | None | SCBPDM via COLLINS | None | Yes | First name or company name |
| DF-PTY-005 | party | last_name | TEXT | varchar(100) | 100 | No | None | None | None | None | SCBPDM via COLLINS | None | Yes | Last name |
| DF-PTY-006 | party | id_type | LOV | varchar(20) | 20 | Yes | None | LOV-ID-TYPE | None | None | SCBPDM via COLLINS | None | No | Thai national ID, passport, company registration |
| DF-PTY-007 | party | id_no_token | TEXT | varchar(64) | 64 | Yes | None | None | None | None | SCBPDM via COLLINS | None | Yes | Tokenized identity number. The clear value is never stored in the Workbench |
| DF-PTY-008 | party | date_of_birth | DATE | date |  | No | None | None | None | None | SCBPDM via COLLINS | None | Yes | Date of birth |
| DF-PTY-009 | party | segment | LOV | varchar(20) | 20 | No | None | LOV-SEGMENT | None | None | SCBPDM via COLLINS | Segment | No | Retail, SSME, corporate |
| DF-PTY-010 | party | vulnerable_flag | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | Yes | Vulnerable customer or hardship confirmed |
| DF-PTY-011 | party | deceased_flag | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | Yes | Death confirmed |
| DF-PTY-012 | party | bankruptcy_flag | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | Yes | Bankruptcy or receivership confirmed |
| DF-PTY-021 | party | fraud_flag | BOOLEAN | boolean |  | Yes | false | None | None | None | Aric via COLLINS | None | Yes | True while fraud is confirmed or under investigation for the party |
| DF-PTY-013 | contact_point | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the contact point |
| DF-PTY-014 | contact_point | party_id | CROSS_REF | uuid |  | Yes | None | None | FK | party | Workbench | None | No | The party this record belongs to |
| DF-PTY-015 | contact_point | channel | LOV | varchar(15) | 15 | Yes | None | LOV-CHANNEL | None | None | Workbench | None | No | Mobile, home phone, work phone, LINE, email, postal address |
| DF-PTY-016 | contact_point | value_token | TEXT | varchar(256) | 256 | Yes | None | None | None | None | SCBPDM via COLLINS | None | Yes | The number, handle or address, stored masked |
| DF-PTY-017 | contact_point | source | LOV | varchar(15) | 15 | Yes | None | LOV-CONTACT-SRC | None | None | Workbench | None | No | Bank record, field visit, agency, bureau trace, customer |
| DF-PTY-018 | contact_point | consent_status | LOV | varchar(12) | 12 | Yes | UNKNOWN | LOV-CONSENT | None | None | Workbench | None | No | Given, withdrawn, unknown |
| DF-PTY-019 | contact_point | verified_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When it last reached the right party |
| DF-PTY-020 | contact_point | failed_count | NUMBER | integer |  | Yes | 0 | None | None | None | Workbench | None | No | Failed attempts since last success |
| DF-ACC-001 | loan_account | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the account |
| DF-ACC-002 | loan_account | account_no | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Core bank (ALS) via COLLINS | ACCOUNT_KEY / iacct / AccNo | No | Account number |
| DF-ACC-003 | loan_account | contract_no | TEXT | varchar(20) | 20 | No | None | None | None | None | Core bank (ALS) via COLLINS | ContractNo | No | Contract number |
| DF-ACC-004 | loan_account | product_code | LOV | varchar(10) | 10 | Yes | None | LOV-PRODUCT-CODE | None | None | Core bank (ALS) via COLLINS | acct_prd_cd | No | Core bank product code |
| DF-ACC-005 | loan_account | product_category_efs | TEXT | varchar(60) | 60 | No | None | None | None | None | EFS via COLLINS | Product_Category_EFS | No | Product category in EFS |
| DF-ACC-006 | loan_account | business_unit | LOV | varchar(10) | 10 | No | None | LOV-BU | None | None | Core bank (ALS) via COLLINS | BU | No | Owning business unit |
| DF-ACC-007 | loan_account | contract_date | DATE | date |  | No | None | None | None | None | Core bank (ALS) via COLLINS | CONTRACT_DATE | No | Contract date |
| DF-ACC-008 | loan_account | interest_rate | NUMBER | numeric(7,4) | 7,4 | No | None | None | None | None | Core bank (ALS) via COLLINS | INTEREST_RATE | No | Contract interest rate, percent |
| DF-ACC-009 | loan_account | principal_outstanding | NUMBER | numeric(18,2) | 18,2 | Yes | 0 | None | None | None | Core bank (ALS) via COLLINS | Principal | No | Principal outstanding, baht |
| DF-ACC-010 | loan_account | interest_outstanding | NUMBER | numeric(18,2) | 18,2 | Yes | 0 | None | None | None | Core bank (ALS) via COLLINS | AINT1 + AINT2 | No | Accrued interest outstanding, baht |
| DF-ACC-011 | loan_account | fees_outstanding | NUMBER | numeric(18,2) | 18,2 | Yes | 0 | None | None | None | Core bank (ALS) via COLLINS | AFEE | No | Fees outstanding, baht |
| DF-ACC-012 | loan_account | total_balance | NUMBER | numeric(18,2) | 18,2 | Yes | 0 | None | None | None | Core bank (ALS) via COLLINS | TOTAL_BALANCE | No | Total balance, baht |
| DF-ACC-013 | loan_account | accounting_balance | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Core bank (ALS) via COLLINS | ACCOUNTING_BALANCE | No | Accounting balance, baht |
| DF-ACC-014 | loan_account | days_past_due | NUMBER | integer |  | Yes | 0 | None | None | None | Core bank (ALS) via COLLINS | DELAY_DAYS | No | Days past due |
| DF-ACC-015 | loan_account | bucket | LOV | varchar(10) | 10 | No | None | LOV-BUCKET | None | None | Core bank (ALS) via COLLINS | Bucket | No | Arrears bucket, for example 91-120, 180+ |
| DF-ACC-016 | loan_account | classification | LOV | varchar(10) | 10 | No | None | LOV-CLASS | None | None | Core bank (ALS) via COLLINS | None | No | Loan classification and stage |
| DF-ACC-017 | loan_account | last_payment_date | DATE | date |  | No | None | None | None | None | Core bank (ALS) via COLLINS | LAST_PAYMENT_DATE | No | Date of the last payment |
| DF-ACC-018 | loan_account | next_installment_date | DATE | date |  | No | None | None | None | None | Core bank (ALS) via COLLINS | NEXT_INSTALLMENT_DATE | No | Next installment date |
| DF-ACC-019 | loan_account | tdr_flag | BOOLEAN | boolean |  | Yes | false | None | None | None | Core bank (ALS) via COLLINS | TDR list | No | True when the account is under a restructure |
| DF-ACC-020 | loan_account | last_tdr_date | DATE | date |  | No | None | None | None | None | Core bank (ALS) via COLLINS | Last_TDR_Date | No | Date of the last restructure |
| DF-ACC-021 | loan_account | data_as_of | DATE | date |  | Yes | None | None | None | None | Core bank (ALS) via COLLINS | ms_data_dt | No | The business date of the load |
| DF-ACC-029 | loan_account | dispute_open | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True while the customer disputes the balance or the security on the account |
| DF-ACC-030 | loan_account | settlement_booked_date | DATE | date |  | No | None | None | None | None | Core bank (ALS) via COLLINS | None | No | Date a settlement was booked in ALS; source field to confirm with the system owner |
| DF-ACC-031 | loan_account | settlement_booked_amount | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Core bank (ALS) via COLLINS | None | No | Settlement amount booked in ALS, baht; source field to confirm with the system owner |
| DF-ACC-022 | account_payment | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the account payment |
| DF-ACC-023 | account_payment | account_id | CROSS_REF | uuid |  | Yes | None | None | FK | loan_account | Workbench | None | No | The loan_account this record belongs to |
| DF-ACC-024 | account_payment | payment_code | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Core bank (ALS) via COLLINS | Payment_Code | No | Payment reference |
| DF-ACC-025 | account_payment | payment_date | DATE | date |  | Yes | None | None | None | None | Core bank (ALS) via COLLINS | Payment_Date | No | Value date |
| DF-ACC-026 | account_payment | payment_amount | NUMBER | numeric(18,2) | 18,2 | Yes | None | None | None | None | Core bank (ALS) via COLLINS | Payment_Amount | No | Amount, baht |
| DF-ACC-027 | account_payment | payment_channel | LOV | varchar(15) | 15 | No | None | LOV-PAY-CHANNEL | None | None | Core bank (ALS) via COLLINS | None | No | Channel the payment came through |
| DF-ACC-028 | account_payment | data_as_of | DATE | date |  | Yes | None | None | None | None | Core bank (ALS) via COLLINS | ms_data_dt | No | The business date of the load |
| DF-COL-001 | collateral | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the collateral |
| DF-COL-002 | collateral | collateral_no | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | CCMS | None | No | Collateral number |
| DF-COL-003 | collateral | collateral_type | LOV | varchar(15) | 15 | Yes | None | LOV-COLL-TYPE | None | None | CCMS | None | No | Land, house, condominium, vehicle, deposit, other |
| DF-COL-004 | collateral | title_doc_no | TEXT | varchar(40) | 40 | No | None | None | None | None | CCMS | Title Deed / Ownership Doc | No | Title deed or registration number |
| DF-COL-005 | collateral | plot_no | TEXT | varchar(20) | 20 | No | None | None | None | None | CCMS | Plot No. | No | Plot number |
| DF-COL-006 | collateral | area_text | TEXT | varchar(20) | 20 | No | None | None | None | None | CCMS | Area | No | Land area in rai-ngan-wa |
| DF-COL-007 | collateral | province | LOV | varchar(40) | 40 | No | None | LOV-PROVINCE | None | None | CCMS | Province | No | Province |
| DF-COL-008 | collateral | district | TEXT | varchar(60) | 60 | No | None | None | None | None | CCMS | District | No | District |
| DF-COL-009 | collateral | subdistrict | TEXT | varchar(60) | 60 | No | None | None | None | None | CCMS | Subdistrict | No | Subdistrict |
| DF-COL-010 | collateral | occupancy | LOV | varchar(15) | 15 | No | None | LOV-OCCUPANCY | None | None | Workbench | None | No | Occupied by owner, tenant, vacant, unknown |
| DF-COL-011 | collateral | encumbrance_status | LOV | varchar(15) | 15 | No | None | LOV-ENCUMBRANCE | None | None | Workbench | None | No | Clear, other creditor, seized, under dispute |
| DF-COL-012 | collateral | insured_value | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | CCMS | Insvalue | No | Insured value, baht |
| DF-COL-013 | collateral | insurance_expiry | DATE | date |  | No | None | None | None | None | CCMS | None | No | Insurance expiry date |
| DF-COL-014 | account_collateral | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the account collateral link |
| DF-COL-015 | account_collateral | account_id | CROSS_REF | uuid |  | Yes | None | None | FK | loan_account | Workbench | None | No | The loan_account this record belongs to |
| DF-COL-016 | account_collateral | collateral_id | CROSS_REF | uuid |  | Yes | None | None | FK | collateral | Workbench | None | No | The collateral this record belongs to |
| DF-COL-017 | account_collateral | lien_rank | NUMBER | integer |  | No | None | None | None | None | CCMS | None | No | Rank of the bank's lien |
| DF-COL-018 | valuation | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the valuation |
| DF-COL-019 | valuation | collateral_id | CROSS_REF | uuid |  | No | None | None | FK | collateral | Workbench | None | No | The collateral this record belongs to |
| DF-COL-020 | valuation | asset_id | CROSS_REF | uuid |  | No | None | None | FK | asset | Workbench | None | No | The asset this record belongs to |
| DF-COL-021 | valuation | appraisal_no | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | SVAF | Appraisal No. | No | Appraisal number |
| DF-COL-022 | valuation | appraisal_type | LOV | varchar(15) | 15 | Yes | None | LOV-APPRAISAL | None | None | SVAF | None | No | Market, official, forced sale, desktop, agent estimate |
| DF-COL-023 | valuation | appraised_value | NUMBER | numeric(18,2) | 18,2 | Yes | None | None | None | None | SVAF | Appraised Value | No | Appraised value, baht |
| DF-COL-024 | valuation | forced_sale_value | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | SVAF | Forced Sale Value | No | Forced sale value, baht |
| DF-COL-025 | valuation | appraisal_date | DATE | date |  | Yes | None | None | None | None | SVAF | Appraisal Date | No | Appraisal date |
| DF-COL-026 | valuation | valuer_partner_id | CROSS_REF | uuid |  | No | None | None | FK | partner | Workbench | None | No | The valuer |
| DF-COL-027 | valuation | accepted | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True once accepted for the route decision |
| DF-COL-043 | valuation | stale_flag | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True when the appraisal is older than appraisal.max.age at the load business date |
| DF-COL-044 | valuation | age_days | FORMULA | integer |  | No | None | None | None | None | Workbench | None | No | Age of the appraisal in days at the load business date |
| DF-COL-028 | asset | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the asset |
| DF-COL-029 | asset | case_id | CROSS_REF | uuid |  | No | None | None | FK | recovery_case | Workbench | None | No | The recovery_case this record belongs to |
| DF-COL-030 | asset | collateral_id | CROSS_REF | uuid |  | No | None | None | FK | collateral | Workbench | None | No | The collateral this record belongs to |
| DF-COL-031 | asset | asset_ref | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | AMIS | Asset ID | No | Asset reference |
| DF-COL-032 | asset | asset_code | TEXT | varchar(20) | 20 | No | None | None | None | None | AMIS | Asset Code | No | Asset code |
| DF-COL-033 | asset | asset_type | LOV | varchar(20) | 20 | Yes | None | LOV-ASSET-TYPE | None | None | AMIS | Asset Type | No | Detached house, townhouse, condominium, land, vehicle |
| DF-COL-034 | asset | transfer_in_type | LOV | varchar(20) | 20 | Yes | None | LOV-TRANSFER-IN | None | None | AMIS | Transfer-in Type | No | Auction purchase, deed in lieu, repossession |
| DF-COL-035 | asset | from_segment | LOV | varchar(20) | 20 | No | None | LOV-SEGMENT | None | None | AMIS | From Segment | No | Segment the asset came from |
| DF-COL-036 | asset | transfer_in_date | DATE | date |  | Yes | None | None | None | None | AMIS | Ownership Transfer in Date | No | Date ownership passed to the bank |
| DF-COL-037 | asset | book_value | NUMBER | numeric(18,2) | 18,2 | Yes | None | None | None | None | AMIS | Book  Value | No | Book value, baht |
| DF-COL-038 | asset | auction_purchase_price | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | AMIS | Auction Purchase Price | No | Price paid at auction, baht |
| DF-COL-039 | asset | repossessed_date | DATE | date |  | No | None | None | None | None | RPS | ReposessedCarDate | No | Date the vehicle was repossessed |
| DF-COL-040 | asset | stock_date | DATE | date |  | No | None | None | None | None | RPS | STOCK_DATE | No | Date the vehicle entered stock |
| DF-COL-041 | asset | holding_status | LOV | varchar(15) | 15 | Yes | HELD | LOV-HOLDING | None | None | Workbench | None | No | Held, listed, under offer, sold, transferred, rented |
| DF-COL-042 | asset | holding_cost_to_date | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Workbench | None | No | Holding cost to date, baht |
| DF-TRT-001 | treatment | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the treatment |
| DF-TRT-002 | treatment | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | None | No | The recovery_case this record belongs to |
| DF-TRT-003 | treatment | decision_log_id | CROSS_REF | uuid |  | No | None | None | FK | decision_log_entry | Workbench | None | No | The decision that approved it |
| DF-TRT-004 | treatment | treatment_type | LOV | varchar(20) | 20 | Yes | None | LOV-TREATMENT | None | None | Workbench | None | No | Restructure, settlement, deed in lieu, buy-back, guarantee claim, repossession, auction, debt sale, write-off, RAMC transfer, rental |
| DF-TRT-005 | treatment | proposed_by | LOV | varchar(10) | 10 | Yes | None | LOV-PROPOSER | None | None | Workbench | None | No | Agent, rule, person |
| DF-TRT-006 | treatment | proposed_at | DATE | timestamptz |  | Yes | None | None | None | None | Workbench | None | No | When proposed |
| DF-TRT-007 | treatment | offer_amount | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Workbench | None | No | Amount offered or agreed, baht |
| DF-TRT-008 | treatment | haircut_amount | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Workbench | None | No | Amount forgiven, baht |
| DF-TRT-009 | treatment | installments | NUMBER | integer |  | No | None | None | None | None | ACE | None | No | Number of installments in a plan |
| DF-TRT-010 | treatment | valid_until | DATE | date |  | No | None | None | None | None | Workbench | None | No | Offer validity |
| DF-TRT-011 | treatment | approval_level | LOV | varchar(4) | 4 | No | None | LOV-APPROVAL-LEVEL | None | None | Workbench | None | No | Approval level that approved it |
| DF-TRT-012 | treatment | booked_at | DATE | timestamptz |  | No | None | None | None | None | Core bank (ALS) via COLLINS | None | No | When booked in the core |
| DF-TRT-013 | treatment | outcome | LOV | varchar(12) | 12 | No | None | LOV-TRT-OUTCOME | None | None | Workbench | None | No | Kept, broken, completed, canceled, declined |
| DF-TRT-014 | treatment | outcome_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the outcome was recorded |
| DF-TRT-023 | treatment | nleads_ref | TEXT | varchar(30) | 30 | No | None | None | None | None | NLEADS | None | No | NLEADS reference of the credit approval |
| DF-TRT-024 | treatment | credit_result | LOV | varchar(10) | 10 | No | None | LOV-CREDIT-RESULT | None | None | NLEADS | None | No | Approved or refused, from NLEADS |
| DF-TRT-025 | treatment | credit_result_reason | TEXT | varchar(1000) | 1000 | No | None | None | None | None | NLEADS | None | No | Reason given by NLEADS; required when refused |
| DF-TRT-026 | treatment | credit_result_at | DATE | timestamptz |  | No | None | None | None | None | NLEADS | None | No | When the result was given in NLEADS |
| DF-TRT-027 | treatment | interest_rate | NUMBER | numeric(7,4) | 7,4 | No | None | None | None | None | Workbench | None | No | Approved interest rate of the plan, percent |
| DF-TRT-028 | treatment | booking_difference | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Each term that differs between approval and booking: term, approved, booked, business date |
| DF-TRT-029 | treatment | first_due_date | DATE | date |  | No | None | None | None | None | Workbench | None | No | Date the first installment is due |
| DF-TRT-030 | treatment | signature_status | LOV | varchar(12) | 12 | No | None | LOV-TRT-SIGNATURE | None | None | Workbench | None | No | Pending, signed or not signed, read by the routing rules |
| DF-TRT-031 | treatment | installment_amount | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Workbench | None | No | Amount due per plan installment, baht |
| DF-TRT-032 | treatment | installments_paid | NUMBER | integer |  | Yes | 0 | None | None | None | Workbench | None | No | Installments matched so far |
| DF-TRT-033 | treatment | installment_shortfall | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Workbench | None | No | Shortfall left on the plan by a partial payment, baht |
| DF-TRT-015 | guarantee_claim | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the guarantee claim |
| DF-TRT-016 | guarantee_claim | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | None | No | The recovery_case this record belongs to |
| DF-TRT-017 | guarantee_claim | claim_type | LOV | varchar(25) | 25 | Yes | None | LOV-CLAIM-TYPE | None | None | Workbench | None | No | TCG, credit life insurance, mortgage insurance, collateral insurance |
| DF-TRT-018 | guarantee_claim | claim_deadline | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Last date the claim can be filed |
| DF-TRT-019 | guarantee_claim | claimed_amount | NUMBER | numeric(18,2) | 18,2 | Yes | None | None | None | None | Workbench | None | No | Amount claimed, baht |
| DF-TRT-020 | guarantee_claim | filed_at | DATE | date |  | No | None | None | None | None | Workbench | None | No | Date filed |
| DF-TRT-021 | guarantee_claim | paid_amount | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Workbench | None | No | Amount paid, baht |
| DF-TRT-022 | guarantee_claim | status | LOV | varchar(12) | 12 | Yes | PREPARING | LOV-CLAIM-STATUS | None | None | Workbench | None | No | Preparing, filed, defect, paid, rejected |
| DF-LEG-001 | legal_action | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the legal action |
| DF-LEG-002 | legal_action | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | None | No | The recovery_case this record belongs to |
| DF-LEG-003 | legal_action | law_firm_id | CROSS_REF | uuid |  | No | None | None | FK | partner | Workbench | None | No | The law firm instructed |
| DF-LEG-004 | legal_action | action_type | LOV | varchar(20) | 20 | Yes | None | LOV-LEGAL-TYPE | None | None | Workbench | None | No | Notice, civil case, appeal, enforcement, bankruptcy petition, LED auction |
| DF-LEG-005 | legal_action | lawsuit_no | TEXT | varchar(30) | 30 | No | None | None | None | None | LIT | LAWSUIT_NO / LAWSUIT_RUN | No | Lawsuit reference in LIT |
| DF-LEG-006 | legal_action | black_case_no | TEXT | varchar(30) | 30 | No | None | None | None | None | LIT | เลขที่คดีดำ | No | Court black case number |
| DF-LEG-007 | legal_action | red_case_no | TEXT | varchar(30) | 30 | No | None | None | None | None | LIT | None | No | Court red case number after judgment |
| DF-LEG-008 | legal_action | court_name | TEXT | varchar(120) | 120 | No | None | None | None | None | LIT | NCOURT | No | Court |
| DF-LEG-009 | legal_action | claim_amount | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | LIT | AAMT_SUIT | No | Amount sued for, baht |
| DF-LEG-010 | legal_action | filed_date | DATE | date |  | No | None | None | None | None | LIT | None | No | Date filed |
| DF-LEG-011 | legal_action | judgment_date | DATE | date |  | No | None | None | None | None | LIT | Judgment date | No | Date of judgment |
| DF-LEG-012 | legal_action | judgment_amount | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | LIT | None | No | Amount awarded, baht |
| DF-LEG-013 | legal_action | lit_status | TEXT | varchar(200) | 200 | No | None | None | None | None | LIT via COLLINS | STATE_RES_NAME | No | Latest status text in LIT |
| DF-LEG-014 | legal_action | status | LOV | varchar(15) | 15 | Yes | OPEN | LOV-LEGAL-STATUS | None | None | Workbench | None | No | Open, filed, judgment, enforcing, closed, withdrawn |
| DF-LEG-015 | notice | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the notice |
| DF-LEG-016 | notice | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | None | No | The recovery_case this record belongs to |
| DF-LEG-017 | notice | document_id | CROSS_REF | uuid |  | No | None | None | FK | document | Workbench | None | No | The generated notice |
| DF-LEG-018 | notice | notice_type | LOV | varchar(25) | 25 | Yes | None | LOV-NOTICE | None | None | Workbench | None | No | Demand, recall, statutory sale notice, guarantor notice |
| DF-LEG-019 | notice | sent_date | DATE | date |  | No | None | None | None | None | WIN | DDMMYYYY | No | Date sent |
| DF-LEG-020 | notice | barcode | TEXT | varchar(40) | 40 | No | None | None | None | None | WIN | Barcode | No | Registered mail barcode |
| DF-LEG-021 | notice | callback_date | DATE | date |  | No | None | None | None | None | WIN | DDMMYYYY_callBack | No | Date the proof of delivery came back |
| DF-LEG-022 | notice | delivery_status | LOV | varchar(15) | 15 | No | None | LOV-DELIVERY | None | None | WIN | None | No | Delivered, refused, undeliverable, pending |
| DF-LEG-023 | notice | sent_type | LOV | varchar(10) | 10 | No | None | LOV-SENT-TYPE | None | None | WIN | Sent Type | No | Before NPL or NPL |
| DF-LEG-030 | notice | party_id | CROSS_REF | uuid |  | No | None | None | FK | party | Workbench | None | No | Party the notice is addressed to |
| DF-LEG-031 | notice | template_id | CROSS_REF | uuid |  | No | None | None | FK | template | Workbench | None | No | Template version the notice was generated from |
| DF-LEG-032 | notice | hold_reason | TEXT | varchar(30) | 30 | No | None | None | None | None | Workbench | None | No | Why the notice is held: missing merge field, TEMPLATE_WITHDRAWN, CONTACT_STOP_Xn, LEGAL_HOLD |
| DF-LEG-033 | notice | dispatch_file_id | CROSS_REF | uuid |  | No | None | None | FK | outbound_item | Workbench | None | No | WIN file the notice was last written to |
| DF-LEG-034 | notice | dispatch_attempts | NUMBER | integer |  | Yes | 0 | None | None | None | Workbench | None | No | Number of WIN files the notice has been sent in without acknowledgment |
| DF-LEG-024 | hearing | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the hearing |
| DF-LEG-025 | hearing | legal_action_id | CROSS_REF | uuid |  | Yes | None | None | FK | legal_action | Workbench | None | No | The legal_action this record belongs to |
| DF-LEG-026 | hearing | hearing_date | DATE | timestamptz |  | Yes | None | None | None | None | LIT | None | No | Hearing date |
| DF-LEG-027 | hearing | hearing_type | LOV | varchar(20) | 20 | No | None | LOV-HEARING | None | None | LIT | None | No | First hearing, witness, judgment reading, mediation |
| DF-LEG-028 | hearing | outcome | LOV | varchar(20) | 20 | No | None | LOV-HEARING-OUTCOME | None | None | Workbench | None | No | Held, adjourned, settled, judgment |
| DF-LEG-029 | hearing | next_date | DATE | timestamptz |  | No | None | None | None | None | LIT | None | No | Next date set |
| DF-PRT-001 | partner | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the partner |
| DF-PRT-002 | partner | partner_code | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | OACode | No | Partner code |
| DF-PRT-003 | partner | partner_name | TEXT | varchar(160) | 160 | Yes | None | None | None | None | Workbench | REPOSS_NAME / Investor | No | Registered name |
| DF-PRT-004 | partner | partner_type | LOV | varchar(15) | 15 | Yes | None | LOV-PARTNER-TYPE | None | None | Workbench | None | No | Agency, law firm, valuer, auction vendor, broker, debt buyer, AMC, RAMC |
| DF-PRT-005 | partner | panel_status | LOV | varchar(12) | 12 | Yes | ACTIVE | LOV-PANEL | None | None | Workbench | None | No | Active, on notice, suspended, exited |
| DF-PRT-006 | partner | contract_end | DATE | date |  | No | None | None | None | None | Workbench | None | No | Contract end date |
| DF-PRT-007 | partner | score | NUMBER | numeric(5,2) | 5,2 | No | None | None | None | None | Workbench | None | No | Latest scorecard result |
| DF-PRT-008 | partner_instruction | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the partner instruction |
| DF-PRT-009 | partner_instruction | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | None | No | The recovery_case this record belongs to |
| DF-PRT-010 | partner_instruction | partner_id | CROSS_REF | uuid |  | Yes | None | None | FK | partner | Workbench | None | No | The partner this record belongs to |
| DF-PRT-011 | partner_instruction | instruction_type | LOV | varchar(20) | 20 | Yes | None | LOV-INSTRUCTION | None | None | Workbench | None | No | Collect, file suit, enforce, appraise, repossess, list, sell |
| DF-PRT-012 | partner_instruction | instructed_at | DATE | timestamptz |  | Yes | None | None | None | None | Workbench | None | No | When instructed |
| DF-PRT-013 | partner_instruction | due_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the result is due |
| DF-PRT-014 | partner_instruction | status | LOV | varchar(12) | 12 | Yes | SENT | LOV-INSTR-STATUS | None | None | Workbench | None | No | Sent, accepted, declined, in progress, done, recalled |
| DF-PRT-015 | partner_instruction | result_code | TEXT | varchar(40) | 40 | No | None | None | None | None | Workbench | None | No | Result reported by the partner |
| DF-PRT-016 | partner_instruction | fee_amount | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Workbench | None | No | Fee payable, baht |
| DF-SAL-001 | listing | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the listing |
| DF-SAL-002 | listing | asset_id | CROSS_REF | uuid |  | Yes | None | None | FK | asset | Workbench | None | No | The asset this record belongs to |
| DF-SAL-003 | listing | sale_channel | LOV | varchar(15) | 15 | Yes | None | LOV-SALE-CHANNEL | None | None | Workbench | Sale By | No | Dutch auction, broker, direct, LED auction, RAMC |
| DF-SAL-004 | listing | start_price | NUMBER | numeric(18,2) | 18,2 | Yes | None | None | None | None | Workbench | None | No | Start price, baht |
| DF-SAL-005 | listing | floor_price | NUMBER | numeric(18,2) | 18,2 | Yes | None | None | None | None | Workbench | None | No | Floor price approved, baht |
| DF-SAL-006 | listing | round_no | NUMBER | integer |  | Yes | 1 | None | None | None | Workbench | None | No | Current price round |
| DF-SAL-007 | listing | listed_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When listed |
| DF-SAL-008 | listing | status | LOV | varchar(12) | 12 | Yes | DRAFT | LOV-LISTING | None | None | Workbench | None | No | Draft, live, under offer, sold, withdrawn |
| DF-SAL-009 | asset_sale | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the asset sale |
| DF-SAL-010 | asset_sale | asset_id | CROSS_REF | uuid |  | Yes | None | None | FK | asset | Workbench | None | No | The asset this record belongs to |
| DF-SAL-011 | asset_sale | listing_id | CROSS_REF | uuid |  | No | None | None | FK | listing | Workbench | None | No | The listing this record belongs to |
| DF-SAL-012 | asset_sale | contract_date | DATE | date |  | Yes | None | None | None | None | AMIS | Contract Date | No | Sale contract date |
| DF-SAL-013 | asset_sale | sale_date | DATE | date |  | Yes | None | None | None | None | AMIS | Sale Date | No | Sale date |
| DF-SAL-014 | asset_sale | sale_price | NUMBER | numeric(18,2) | 18,2 | Yes | None | None | None | None | AMIS | Sale Price | No | Sale price, baht |
| DF-SAL-015 | asset_sale | transfer_fee | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | AMIS | Sale Transfer Fee | No | Transfer fee, baht |
| DF-SAL-016 | asset_sale | specific_business_tax | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | AMIS | Specific Business Tax | No | Specific business tax, baht |
| DF-SAL-017 | asset_sale | corporate_income_tax | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | AMIS | Corporate Income Tax | No | Corporate income tax, baht |
| DF-SAL-018 | asset_sale | gain_loss | FORMULA | numeric(18,2) | 18,2 | No | None | None | None | None | Workbench | None | No | Sale price less book value and costs |
| DF-SAL-019 | asset_sale | incentive_amount | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | AMIS | Incentive Amount | No | Incentive paid on the sale, baht |
| DF-SAL-020 | debt_sale_lot | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the debt sale lot |
| DF-SAL-021 | debt_sale_lot | lot_no | TEXT | varchar(15) | 15 | Yes | None | None | UK | None | Workbench | Lot | No | Lot number, for example 1/2024 |
| DF-SAL-022 | debt_sale_lot | cut_off_date | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Balance cut-off date |
| DF-SAL-023 | debt_sale_lot | segment | LOV | varchar(20) | 20 | Yes | None | LOV-SEGMENT | None | None | Workbench | Segment | No | Segment of the lot |
| DF-SAL-024 | debt_sale_lot | reserve_price | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Workbench | None | No | Reserve price, baht |
| DF-SAL-025 | debt_sale_lot | buyer_partner_id | CROSS_REF | uuid |  | No | None | None | FK | partner | Workbench | Investor | No | Winning buyer |
| DF-SAL-026 | debt_sale_lot | buyer_class | LOV | varchar(10) | 10 | No | None | LOV-BUYER-CLASS | None | None | Workbench | AMC/NON AMC | No | AMC or non-AMC |
| DF-SAL-027 | debt_sale_lot | signing_date | DATE | date |  | No | None | None | None | None | Workbench | SigningYear | No | Date the sale was signed |
| DF-SAL-028 | debt_sale_lot | approval_authority | TEXT | varchar(60) | 60 | No | None | None | None | None | Workbench | Debt Sale Approval Authority | No | Authority that approved the sale |
| DF-SAL-029 | debt_sale_lot | payment_terms | TEXT | varchar(400) | 400 | No | None | None | None | None | Workbench | Payment Terms and Conditions | No | Deposit and payment terms |
| DF-SAL-030 | debt_sale_lot | status | LOV | varchar(12) | 12 | Yes | BUILDING | LOV-LOT-STATUS | None | None | Workbench | None | No | Building, offered, awarded, transferred, closed |
| DF-SAL-031 | debt_sale_account | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the debt sale account |
| DF-SAL-032 | debt_sale_account | lot_id | CROSS_REF | uuid |  | Yes | None | None | FK | debt_sale_lot | Workbench | None | No | The debt_sale_lot this record belongs to |
| DF-SAL-033 | debt_sale_account | account_id | CROSS_REF | uuid |  | Yes | None | None | FK | loan_account | Workbench | None | No | The loan_account this record belongs to |
| DF-SAL-034 | debt_sale_account | borrower_code | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | BorrCode | No | Borrower code |
| DF-SAL-035 | debt_sale_account | outstanding | NUMBER | numeric(18,2) | 18,2 | Yes | None | None | None | None | Core bank (ALS) via COLLINS | OS By Acct | No | Outstanding at cut-off, baht |
| DF-SAL-036 | debt_sale_account | selling_price | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Workbench | SellingPriceByAcct | No | Price allocated to the account, baht |
| DF-SAL-037 | debt_sale_account | put_back_status | LOV | varchar(12) | 12 | No | None | LOV-PUTBACK | None | None | Workbench | None | No | None, claimed, accepted, rejected |
| DF-INT-001 | interaction | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the interaction |
| DF-INT-002 | interaction | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | None | No | The recovery_case this record belongs to |
| DF-INT-003 | interaction | party_id | CROSS_REF | uuid |  | No | None | None | FK | party | Workbench | None | No | The party this record belongs to |
| DF-INT-004 | interaction | occurred_at | DATE | timestamptz |  | Yes | None | None | None | None | Workbench | None | No | When it happened |
| DF-INT-005 | interaction | channel | LOV | varchar(15) | 15 | No | None | LOV-CHANNEL | None | None | Workbench | None | No | Call, visit, SMS, LINE, email, letter, portal, branch; empty for Workbench events such as CASE_CREATED |
| DF-INT-006 | interaction | direction | LOV | varchar(8) | 8 | No | None | LOV-DIRECTION | None | None | Workbench | None | No | Inbound or outbound; empty for Workbench events such as CASE_CREATED |
| DF-INT-007 | interaction | action_code | LOV | varchar(10) | 10 | No | None | LOV-ACTION-CODE | None | None | EFS via COLLINS | Actioncode ID | No | Action code |
| DF-INT-008 | interaction | contact_result | LOV | varchar(20) | 20 | No | None | LOV-CONTACT-RESULT | None | None | EFS via COLLINS | Call Result | No | Right party, third party, no answer, wrong number |
| DF-INT-009 | interaction | promise_amount | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Workbench | None | No | Amount promised, baht |
| DF-INT-010 | interaction | promise_date | DATE | date |  | No | None | None | None | None | Workbench | None | No | Date promised |
| DF-INT-011 | interaction | summary | TEXT | varchar(2000) | 2000 | No | None | None | None | None | Workbench | None | Yes | Summary of what was said |
| DF-INT-012 | interaction | conduct_check | LOV | varchar(15) | 15 | No | None | LOV-CONDUCT | None | None | Workbench | None | No | Passed, blocked, not applicable |
| DF-INT-013 | interaction | source_system | LOV | varchar(10) | 10 | Yes | WORKBENCH | LOV-SOURCE | None | None | Workbench | None | No | EFS for collections history, or the Workbench |
| DF-INT-014 | interaction | event_code | LOV | varchar(40) | 40 | No | None | LOV-LEDGER-EVENT | None | None | Workbench | None | No | Ledger event |
| DF-INT-015 | interaction | actor_type | LOV | varchar(10) | 10 | No | None | LOV-ACTOR-TYPE | None | None | Workbench | None | No | User, service or partner |
| DF-INT-016 | interaction | actor_ref | TEXT | varchar(64) | 64 | No | None | None | None | None | Workbench | None | No | User ID or service identity code that acted |
| DF-INT-017 | interaction | source_ref | TEXT | varchar(60) | 60 | No | None | None | None | None | Workbench | None | No | Producing module and event, or the interface, for example EV-02 CaseAllocated or INT-07 |
| DF-INT-018 | interaction | idempotency_key | TEXT | varchar(120) | 120 | No | None | None | UK | None | Workbench | None | No | Unique key of the event or request; repeats are rejected; unique on its own |
| DF-INT-019 | interaction | case_seq | NUMBER | bigint |  | No | None | None | None | None | Workbench | None | No | Gap-free sequence of the entry within its case; unique with case_id |
| DF-INT-020 | interaction | decision_log_id | CROSS_REF | uuid |  | No | None | None | FK | decision_log_entry | Workbench | None | No | Decision log entry the entry records, for DECISION_TAKEN |
| DF-INT-021 | interaction | corrects_entry_id | CROSS_REF | uuid |  | No | None | None | FK | interaction | Workbench | None | No | Entry this entry corrects |
| DF-INT-022 | interaction | contact_point_id | CROSS_REF | uuid |  | No | None | None | FK | contact_point | Workbench | None | No | The contact point reached; the number or address stays masked in contact_point |
| DF-INT-023 | interaction | from_holder_ref | TEXT | varchar(60) | 60 | No | None | None | None | None | Workbench | None | No | Who held the case before a hand-over: USER:<user id> or PARTNER:<partner code> |
| DF-INT-024 | interaction | to_holder_ref | TEXT | varchar(60) | 60 | No | None | None | None | None | Workbench | None | No | Who holds the case after a hand-over: USER:<user id> or PARTNER:<partner code> |
| DF-INT-025 | interaction | treatment_id | CROSS_REF | uuid |  | No | None | None | FK | treatment | Workbench | None | No | The treatment offered, for an OFFER entry |
| DF-INT-026 | interaction | proceeds_id | CROSS_REF | uuid |  | No | None | None | FK | proceeds | Workbench | None | No | The proceeds matched, for a PAYMENT entry |
| DF-INT-027 | interaction | retention_class | LOV | varchar(10) | 10 | No | None | LOV-RETENTION | None | None | Workbench | None | No | Retention class of the entry, set by entry type |
| DF-INT-028 | interaction | delivery_status | LOV | varchar(15) | 15 | No | None | LOV-SEND-STATUS | None | None | Workbench | None | No | Delivery state of an outbound SMS, LINE message or letter |
| DF-INT-029 | interaction | external_ref | TEXT | varchar(60) | 60 | No | None | None | None | None | Workbench | None | No | Reference returned by NSS, LINE OA or WIN |
| DF-DOC-001 | document | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the document |
| DF-DOC-002 | document | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | None | No | The recovery_case this record belongs to |
| DF-DOC-003 | document | party_id | CROSS_REF | uuid |  | No | None | None | FK | party | Workbench | None | No | The party this record belongs to |
| DF-DOC-004 | document | document_type | LOV | varchar(30) | 30 | Yes | None | LOV-DOC-TYPE | None | None | Workbench | None | No | Type from the document checklist |
| DF-DOC-005 | document | source | LOV | varchar(12) | 12 | Yes | None | LOV-DOC-SOURCE | None | None | Workbench | None | No | Scan, upload, generated, partner, email |
| DF-DOC-006 | document | storage_ref | ATTACHMENT | varchar(400) | 400 | Yes | None | None | None | None | Workbench | None | No | Reference to the stored file |
| DF-DOC-007 | document | classification_confidence | NUMBER | numeric(5,4) | 5,4 | No | None | None | None | None | Workbench | None | No | OCR classification confidence |
| DF-DOC-008 | document | review_status | LOV | varchar(12) | 12 | Yes | NOT_NEEDED | LOV-REVIEW | None | None | Workbench | None | No | Not needed, pending, confirmed, corrected |
| DF-DOC-009 | document | retention_class | LOV | varchar(10) | 10 | Yes | None | LOV-RETENTION | None | None | Workbench | None | No | Retention class |
| DF-DOC-010 | document | write_once | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True for legal documents held write-once |
| DF-DOC-011 | document | doc_version | NUMBER | integer |  | Yes | 1 | None | None | None | Workbench | None | No | Document version |
| DF-DOC-025 | document | previous_version_id | CROSS_REF | uuid |  | No | None | None | FK | document | Workbench | None | No | The document row this version supersedes; empty for version 1 |
| DF-DOC-026 | document | content_sha256 | TEXT | char(64) | 64 | Yes | None | None | None | None | Workbench | None | No | SHA-256 of the stored file, for the duplicate check and the integrity check |
| DF-DOC-027 | document | captured_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | Device time when the field app captured the file |
| DF-DOC-028 | document | capture_latitude | NUMBER | numeric(9,6) | 9,6 | No | None | None | None | None | Workbench | None | Yes | GPS latitude at capture |
| DF-DOC-029 | document | capture_longitude | NUMBER | numeric(9,6) | 9,6 | No | None | None | None | None | Workbench | None | Yes | GPS longitude at capture |
| DF-DOC-030 | document | client_file_id | TEXT | varchar(64) | 64 | No | None | None | None | None | Workbench | None | No | Field app file ID, unique per case, for repeat syncs |
| DF-DOC-031 | document | capture_kind | LOV | varchar(12) | 12 | No | None | LOV-CAPTURE-KIND | None | None | Workbench | None | No | Photo, bill or checklist |
| DF-DOC-032 | document | template_id | CROSS_REF | uuid |  | No | None | None | FK | template | Workbench | None | No | Template version a generated document was made from |
| DF-DOC-033 | document | treatment_id | CROSS_REF | uuid |  | No | None | None | FK | treatment | Workbench | None | No | Treatment a generated document belongs to |
| DF-DOC-012 | document_field | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the document field |
| DF-DOC-013 | document_field | document_id | CROSS_REF | uuid |  | Yes | None | None | FK | document | Workbench | None | No | The document this record belongs to |
| DF-DOC-014 | document_field | field_name | TEXT | varchar(60) | 60 | Yes | None | None | None | None | Workbench | None | No | Field name from the document type |
| DF-DOC-015 | document_field | field_value | TEXT | varchar(1000) | 1000 | No | None | None | None | None | Workbench | None | Yes | Value read, masked where personal |
| DF-DOC-016 | document_field | confidence | NUMBER | numeric(5,4) | 5,4 | No | None | None | None | None | Workbench | None | No | Extraction confidence |
| DF-DOC-017 | document_field | confirmed_by | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Who confirmed a low confidence value |
| DF-DOC-034 | document_field | extracted_value | TEXT | varchar(1000) | 1000 | No | None | None | None | None | Workbench | None | Yes | The value as first read by the extractor, kept when a person corrects field_value; masked by role |
| DF-DOC-035 | document_field | extractor_version | TEXT | varchar(40) | 40 | No | None | None | None | None | Workbench | None | No | Extraction approach and model version that produced the value |
| DF-DOC-018 | document_custody | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the custody movement |
| DF-DOC-019 | document_custody | document_id | CROSS_REF | uuid |  | Yes | None | None | FK | document | Workbench | None | No | The document this record belongs to |
| DF-DOC-020 | document_custody | moved_at | DATE | timestamptz |  | Yes | None | None | None | None | Workbench | None | No | When it moved |
| DF-DOC-021 | document_custody | from_location | LOV | varchar(20) | 20 | Yes | None | LOV-CUSTODY | None | None | Workbench | None | No | Vault, branch, post, lawyer, court, land office |
| DF-DOC-022 | document_custody | to_location | LOV | varchar(20) | 20 | Yes | None | LOV-CUSTODY | None | None | Workbench | None | No | Where it went |
| DF-DOC-023 | document_custody | held_by | TEXT | varchar(120) | 120 | Yes | None | None | None | None | Workbench | None | No | Person or firm holding it |
| DF-DOC-024 | document_custody | due_back | DATE | date |  | No | None | None | None | None | Workbench | None | No | When it is due back |
| DF-DEC-001 | decision_log_entry | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the decision log entry |
| DF-DEC-002 | decision_log_entry | case_id | CROSS_REF | uuid |  | No | None | None | FK | recovery_case | Workbench | None | No | The recovery_case this record belongs to; empty only for access events (decision code AC-...) with no case |
| DF-DEC-003 | decision_log_entry | decision_code | LOV | varchar(8) | 8 | Yes | None | LOV-DECISION | None | None | Workbench | None | No | D5.1 to D9.3, X1 to X7, or an access event |
| DF-DEC-004 | decision_log_entry | rule_id | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | Rule that fired |
| DF-DEC-005 | decision_log_entry | rule_version | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | Rule version |
| DF-DEC-006 | decision_log_entry | model_version | TEXT | varchar(40) | 40 | No | None | None | None | None | COLLINS | None | No | Model version used |
| DF-DEC-007 | decision_log_entry | agent_version | TEXT | varchar(40) | 40 | No | None | None | None | None | Workbench | None | No | Agent and prompt version used |
| DF-DEC-008 | decision_log_entry | inputs_ref | TEXT | varchar(400) | 400 | Yes | None | None | None | None | Workbench | None | No | Reference to the inputs snapshot, with the freshness of each input |
| DF-DEC-009 | decision_log_entry | recommendation | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Option, reasons, confidence and alternatives |
| DF-DEC-010 | decision_log_entry | approver_user_id | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Who approved |
| DF-DEC-011 | decision_log_entry | approval_level | LOV | varchar(4) | 4 | No | None | LOV-APPROVAL-LEVEL | None | None | Workbench | None | No | Approval level applied |
| DF-DEC-012 | decision_log_entry | final_call | TEXT | varchar(40) | 40 | Yes | None | None | None | None | Workbench | None | No | The option decided |
| DF-DEC-013 | decision_log_entry | override_reason | TEXT | varchar(1000) | 1000 | No | None | None | None | None | Workbench | None | No | Reason when the person did not follow the recommendation |
| DF-DEC-014 | decision_log_entry | actions | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Target system, result and timestamps of each action |
| DF-DEC-015 | decision_log_entry | outcome | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Cash, cure, loss and time, written when known |
| DF-DEC-016 | decision_log_entry | decided_at | DATE | timestamptz |  | Yes | now() | None | None | None | Workbench | None | No | When decided |
| DF-DEC-017 | decision_log_entry | prev_hash | TEXT | char(64) | 64 | Yes | None | None | None | None | Workbench | None | No | Hash of the previous entry |
| DF-DEC-018 | decision_log_entry | entry_hash | TEXT | char(64) | 64 | Yes | None | None | UK | None | Workbench | None | No | Hash of this entry |
| DF-DEC-028 | decision_log_entry | chain_seq | NUMBER | bigint |  | Yes | None | None | UK | None | Workbench | None | No | Position of the entry in the hash chain; prev_hash is the entry_hash of chain_seq minus 1; unique on its own |
| DF-DEC-029 | decision_log_entry | corrects_entry_id | CROSS_REF | uuid |  | No | None | None | FK | decision_log_entry | Workbench | None | No | The entry this entry corrects |
| DF-DEC-030 | decision_log_entry | actor_user_id | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | The person or service identity whose action, preparation or access the entry records |
| DF-DEC-031 | decision_log_entry | idempotency_key | TEXT | varchar(80) | 80 | No | None | None | UK | None | Workbench | None | No | Event ID of the calling module; a repeat returns the first entry; unique on its own |
| DF-DEC-019 | score | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the score |
| DF-DEC-020 | score | account_id | CROSS_REF | uuid |  | No | None | None | FK | loan_account | Workbench | None | No | The loan_account this record belongs to |
| DF-DEC-021 | score | case_id | CROSS_REF | uuid |  | No | None | None | FK | recovery_case | Workbench | None | No | The recovery_case this record belongs to |
| DF-DEC-022 | score | model_code | TEXT | varchar(30) | 30 | Yes | None | None | None | None | COLLINS | None | No | Model, for example CRR_RET_380 asset pricing |
| DF-DEC-023 | score | model_version | TEXT | varchar(20) | 20 | Yes | None | None | None | None | COLLINS | None | No | Model version |
| DF-DEC-024 | score | score_value | NUMBER | numeric(12,4) | 12,4 | No | None | None | None | None | COLLINS | None | No | Score |
| DF-DEC-025 | score | estimate_value | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | COLLINS | None | No | Estimated amount, baht, for example return by route or sale price |
| DF-DEC-026 | score | route_code | LOV | varchar(4) | 4 | No | None | LOV-ROUTE | None | None | COLLINS | None | No | Route the estimate is for |
| DF-DEC-027 | score | scored_at | DATE | date |  | Yes | None | None | None | None | COLLINS | None | No | Score date |
| DF-FIN-001 | proceeds | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the proceeds |
| DF-FIN-002 | proceeds | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | None | No | The recovery_case this record belongs to |
| DF-FIN-003 | proceeds | treatment_id | CROSS_REF | uuid |  | No | None | None | FK | treatment | Workbench | None | No | The treatment this record belongs to |
| DF-FIN-004 | proceeds | account_payment_id | CROSS_REF | uuid |  | No | None | None | FK | account_payment | Workbench | None | No | The account_payment this record belongs to |
| DF-FIN-005 | proceeds | source | LOV | varchar(12) | 12 | Yes | None | LOV-PROCEEDS-SRC | None | None | Workbench | None | No | Customer, LED, auction, buyer, agency, insurer, guarantor |
| DF-FIN-006 | proceeds | amount | NUMBER | numeric(18,2) | 18,2 | Yes | None | None | None | None | Core bank (ALS) via COLLINS | Payment_Amount | No | Amount, baht |
| DF-FIN-007 | proceeds | received_date | DATE | date |  | Yes | None | None | None | None | Core bank (ALS) via COLLINS | Payment_Date | No | Date received |
| DF-FIN-008 | proceeds | matched_to | LOV | varchar(15) | 15 | Yes | UNMATCHED | LOV-MATCH | None | None | Workbench | None | No | Installment, settlement, fee, sale proceeds, unmatched |
| DF-FIN-009 | proceeds | posting_ref | TEXT | varchar(40) | 40 | No | None | None | None | None | Core bank (ALS) via COLLINS | None | No | Posting reference in the core or GL |
| DF-FIN-010 | write_off | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the write-off |
| DF-FIN-011 | write_off | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | None | No | The recovery_case this record belongs to |
| DF-FIN-012 | write_off | decision_log_id | CROSS_REF | uuid |  | No | None | None | FK | decision_log_entry | Workbench | None | No | The decision_log_entry this record belongs to |
| DF-FIN-013 | write_off | amount | NUMBER | numeric(18,2) | 18,2 | Yes | None | None | None | None | GL | AMT | No | Amount written off, baht |
| DF-FIN-014 | write_off | tax_criteria_met | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True when the tax criteria are met |
| DF-FIN-015 | write_off | committee_date | DATE | date |  | No | None | None | None | None | Workbench | None | No | Committee approval date |
| DF-FIN-016 | write_off | posted_date | DATE | date |  | No | None | None | None | None | GL | DATE | No | Posting date |
| DF-FIN-017 | write_off | responsibility_center | TEXT | varchar(10) | 10 | No | None | None | None | None | GL | RC | No | Responsibility center |
| DF-FIN-018 | write_off | cost_center | TEXT | varchar(10) | 10 | No | None | None | None | None | GL | OC | No | Operating cost center |
| DF-FIN-019 | write_off | gl_product | TEXT | varchar(10) | 10 | No | None | None | None | None | GL | PRODUCT | No | GL product code |
| DF-FIN-020 | write_off | recovered_after | NUMBER | numeric(18,2) | 18,2 | Yes | 0 | None | None | None | Workbench | None | No | Recovered after charge-off to date, baht |
| DF-REF-001 | rule_row | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the rule row |
| DF-REF-002 | rule_row | rule_id | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Rule ID, for example R-LIT-12 |
| DF-REF-003 | rule_row | rule_version | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Version |
| DF-REF-004 | rule_row | route_set | LOV | varchar(15) | 15 | Yes | None | LOV-ROUTE-SET | None | None | Workbench | None | No | Route set |
| DF-REF-005 | rule_row | from_state | TEXT | varchar(60) | 60 | Yes | None | None | None | None | Workbench | None | No | From state |
| DF-REF-006 | rule_row | event_code | TEXT | varchar(60) | 60 | Yes | None | None | None | None | Workbench | None | No | Event |
| DF-REF-007 | rule_row | condition_expr | TEXT | varchar(1000) | 1000 | No | None | None | None | None | Workbench | None | No | Condition |
| DF-REF-008 | rule_row | action_text | TEXT | varchar(1000) | 1000 | Yes | None | None | None | None | Workbench | None | No | Action |
| DF-REF-009 | rule_row | to_state | TEXT | varchar(60) | 60 | Yes | None | None | None | None | Workbench | None | No | To state |
| DF-REF-010 | rule_row | owner_role | LOV | varchar(20) | 20 | Yes | None | LOV-ROLE | None | None | Workbench | None | No | Owner of the next state |
| DF-REF-011 | rule_row | timer_spec | TEXT | varchar(60) | 60 | No | None | None | None | None | Workbench | None | No | Timer |
| DF-REF-012 | rule_row | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Valid from |
| DF-REF-013 | rule_row | valid_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Valid to |
| DF-REF-014 | rule_row | approved_by | USER_REF | uuid |  | Yes | None | None | None | None | Workbench | None | No | Who approved the version |
| DF-REF-015 | rule_row | test_case_id | TEXT | varchar(20) | 20 | Yes | None | None | None | None | Workbench | None | No | Test case that proves the rule |
| DF-REF-052 | rule_row | rule_table | LOV | varchar(15) | 15 | No | None | LOV-RULE-TABLE | None | None | Workbench | None | No | The Epic 1 rule table a row belongs to |
| DF-REF-053 | rule_row | row_order | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Order in which rows of one rule table are evaluated; first match wins |
| DF-REF-054 | rule_row | target_queue_code | TEXT | varchar(30) | 30 | No | None | None | None | None | Workbench | None | No | The queue an allocation or transfer row places the case in |
| DF-REF-016 | delegation_limit | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the delegation limit |
| DF-REF-017 | delegation_limit | decision_code | LOV | varchar(8) | 8 | Yes | None | LOV-DECISION | None | None | Workbench | None | No | Decision the limit applies to |
| DF-REF-018 | delegation_limit | approval_level | LOV | varchar(4) | 4 | Yes | None | LOV-APPROVAL-LEVEL | None | None | Workbench | None | No | Level 1 to 6 under Regulation กกค.540031 |
| DF-REF-019 | delegation_limit | product_group | LOV | varchar(15) | 15 | Yes | None | LOV-PRODUCT | None | None | Workbench | None | No | Product group |
| DF-REF-020 | delegation_limit | principal_limit | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Workbench | None | No | Principal limit, baht; empty means no limit |
| DF-REF-021 | delegation_limit | loss_pct_limit | NUMBER | numeric(5,2) | 5,2 | No | None | None | None | None | Workbench | None | No | Loss limit as a percentage |
| DF-REF-022 | delegation_limit | min_price_pct_fmv | NUMBER | numeric(5,2) | 5,2 | No | None | None | None | None | Workbench | None | No | Lowest sale price as a percentage of fair market value |
| DF-REF-023 | delegation_limit | holder_user_id | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Person holding the level |
| DF-REF-024 | delegation_limit | substitute_user_id | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Substitute when the holder is absent |
| DF-REF-025 | delegation_limit | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Valid from |
| DF-REF-026 | delegation_limit | valid_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Valid to |
| DF-REF-055 | delegation_limit | limit_version | TEXT | varchar(20) | 20 | Yes | None | None | None | None | Workbench | None | No | Delegation version the row belongs to, for example DOA-2026.11 |
| DF-REF-056 | delegation_limit | regulation_item | TEXT | varchar(10) | 10 | Yes | None | None | None | None | Workbench | None | No | Item of Regulation กกค.540031, for example 2.1.1; one decision code covers several items |
| DF-REF-057 | delegation_limit | applies_when | TEXT | varchar(40) | 40 | No | None | None | None | None | Workbench | None | No | Case condition that selects the row, WO_CRITERIA_MET or WO_CRITERIA_NOT_MET for item 2.1.10 |
| DF-REF-058 | delegation_limit | max_loss_amount | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Workbench | None | No | Maximum loss the level may approve, baht |
| DF-REF-059 | delegation_limit | max_delay_count | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Most delays of legal action, seizure or auction the level may approve on a case |
| DF-REF-060 | delegation_limit | min_price_pct_principal | NUMBER | numeric(5,2) | 5,2 | No | None | None | None | None | Workbench | None | No | Lowest sale price as a percentage of principal outstanding |
| DF-REF-061 | delegation_limit | min_received_pct | NUMBER | numeric(5,2) | 5,2 | No | None | None | None | None | Workbench | None | No | Lowest amount received against the total debt, percent |
| DF-REF-062 | delegation_limit | max_term_years | NUMBER | numeric(4,1) | 4,1 | No | None | None | None | None | Workbench | None | No | Longest lease term the level may approve, years |
| DF-REF-027 | lov_value | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the list value |
| DF-REF-028 | lov_value | lov_code | TEXT | varchar(30) | 30 | Yes | None | None | UK | None | Workbench | None | No | List code, for example LOV-ROUTE |
| DF-REF-029 | lov_value | value_code | TEXT | varchar(30) | 30 | Yes | None | None | UK | None | Workbench | None | No | Value code |
| DF-REF-030 | lov_value | label_en | TEXT | varchar(120) | 120 | Yes | None | None | None | None | Workbench | None | No | English label |
| DF-REF-031 | lov_value | label_th | TEXT | varchar(120) | 120 | No | None | None | None | None | Workbench | None | No | Thai label |
| DF-REF-032 | lov_value | sort_order | NUMBER | integer |  | Yes | 0 | None | None | None | Workbench | None | No | Display order |
| DF-REF-033 | lov_value | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Valid from |
| DF-REF-034 | role | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the role |
| DF-REF-035 | role | role_code | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Role code, for example RW-CASEOWN |
| DF-REF-036 | role | role_name | TEXT | varchar(80) | 80 | Yes | None | None | None | None | Workbench | None | No | Role name |
| DF-REF-037 | role | role_class | LOV | varchar(15) | 15 | Yes | None | LOV-ROLE-CLASS | None | None | Workbench | None | No | Bank user, partner user, non-human actor |
| DF-REF-038 | role | default_scope | LOV | varchar(8) | 8 | Yes | None | LOV-SCOPE | None | None | Workbench | None | No | Own, team, region, all |
| DF-REF-039 | role | entra_group | TEXT | varchar(120) | 120 | No | None | None | None | None | Entra ID | None | No | Entra ID group mapped to the role |
| DF-REF-040 | permission | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the permission |
| DF-REF-041 | permission | role_id | CROSS_REF | uuid |  | Yes | None | None | FK | role | Workbench | None | No | The role this record belongs to |
| DF-REF-042 | permission | capability_area | LOV | varchar(30) | 30 | Yes | None | LOV-CAPABILITY | None | None | Workbench | None | No | One of the 14 capability areas |
| DF-REF-043 | permission | letters | TEXT | varchar(5) | 5 | Yes | - | None | None | None | Workbench | None | No | C, R, U, D and A, or a dash for none |
| DF-REF-044 | permission | matrix_version | TEXT | varchar(20) | 20 | Yes | None | None | None | None | Workbench | None | No | Permission matrix version |
| DF-REF-045 | template | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the template |
| DF-REF-046 | template | template_code | TEXT | varchar(30) | 30 | Yes | None | None | UK | None | Workbench | None | No | Template code |
| DF-REF-047 | template | template_version | NUMBER | integer |  | Yes | 1 | None | UK | None | Workbench | None | No | Version; unique with template_code, since a template holds several versions |
| DF-REF-048 | template | language | LOV | varchar(2) | 2 | Yes | TH | LOV-LANG | None | None | Workbench | None | No | Thai or English |
| DF-REF-049 | template | product_group | LOV | varchar(15) | 15 | No | None | LOV-PRODUCT | None | None | Workbench | None | No | Product group it applies to |
| DF-REF-050 | template | body_ref | ATTACHMENT | varchar(400) | 400 | Yes | None | None | None | None | Workbench | None | No | Stored template body |
| DF-REF-051 | template | approved_by_legal | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True once Legal approves the wording |
| DF-REF-063 | template | approved_by | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Legal counsel who approved the version |
| DF-REF-064 | template | approved_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the version was approved |
| DF-REF-065 | template | valid_from | DATE | date |  | No | None | None | None | None | Workbench | None | No | Date from which the approved version is current |
| DF-REF-066 | template | channel | LOV | varchar(15) | 15 | No | None | LOV-CHANNEL | None | None | Workbench | None | No | Channel the template is for: letter, SMS or LINE |
| DF-REF-067 | template | notice_type | LOV | varchar(25) | 25 | No | None | LOV-NOTICE | None | None | Workbench | None | No | Notice type for a notice template; empty for other documents |
| DF-REF-068 | template | signature_basis | LOV | varchar(20) | 20 | No | None | LOV-SIGNATURE-BASIS | None | None | Workbench | None | No | How Legal allows the document to be signed |
| DF-REF-069 | template | merge_codes | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | The merge codes the template body uses |
| DF-REF-070 | data_product | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the data product |
| DF-REF-071 | data_product | product_code | LOV | varchar(25) | 25 | Yes | None | LOV-DATA-PRODUCT | UK | None | Workbench | None | No | Data product code DP01 to DP14 |
| DF-REF-072 | data_product | product_name | TEXT | varchar(80) | 80 | Yes | None | None | None | None | Workbench | None | No | Data product name, for example Account and arrears |
| DF-REF-073 | data_product | definition | TEXT | varchar(400) | 400 | Yes | None | None | None | None | Workbench | None | No | Definition of the product |
| DF-REF-074 | data_product | system_of_record | TEXT | varchar(120) | 120 | Yes | None | None | None | None | Workbench | None | No | The one system of record for the product |
| DF-REF-075 | data_product | owner_role | LOV | varchar(20) | 20 | Yes | None | LOV-ROLE | None | None | Workbench | None | No | Role of the owner, normally RW-DATASTEW |
| DF-REF-076 | data_product | owner_user_id | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | The named owner of the product; required by the catalog load, empty in the seed |
| DF-REF-077 | data_product | refresh_cycle | LOV | varchar(10) | 10 | Yes | None | LOV-REFRESH | None | None | Workbench | None | No | Daily, weekly, monthly or on change |
| DF-REF-078 | data_product | expected_by | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | Time the load is expected by, for example 08:00 or MON 08:00 |
| DF-REF-079 | data_product | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the catalog version comes into force |
| DF-REF-080 | data_product_access | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the data product access row |
| DF-REF-081 | data_product_access | product_code | LOV | varchar(25) | 25 | Yes | None | LOV-DATA-PRODUCT | UK | None | Workbench | None | No | Data product the row grants |
| DF-REF-082 | data_product_access | role_code | LOV | varchar(20) | 20 | Yes | None | LOV-ROLE | UK | None | Workbench | None | No | Role the row applies to |
| DF-REF-083 | data_product_access | can_read | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True when the role may read the product |
| DF-REF-084 | data_product_access | access_version | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Version of the access table, for example DPA-2026.11 |
| DF-REF-085 | data_product_access | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the row comes into force |
| DF-REF-086 | data_product_access | valid_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Date the row ends |
| DF-OPS-001 | data_product_load | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the freshness stamp |
| DF-OPS-002 | data_product_load | product_code | LOV | varchar(25) | 25 | Yes | None | LOV-DATA-PRODUCT | UK | None | Workbench | None | No | Data product loaded |
| DF-OPS-003 | data_product_load | source_system | TEXT | varchar(40) | 40 | Yes | None | None | None | None | Workbench | None | No | Source system of the load |
| DF-OPS-004 | data_product_load | business_date | DATE | date |  | Yes | None | None | UK | None | Workbench | None | No | Business date of the load |
| DF-OPS-005 | data_product_load | source_extracted_at | DATE | timestamptz |  | Yes | None | None | None | None | Workbench | None | No | When the source extract was taken, from the COLLINS control record or the file |
| DF-OPS-006 | data_product_load | loaded_at | DATE | timestamptz |  | Yes | None | None | None | None | Workbench | None | No | When the load committed in the Workbench |
| DF-OPS-007 | data_product_load | status | LOV | varchar(10) | 10 | Yes | LOADED | LOV-FRESHNESS | None | None | Workbench | None | No | Loaded or stale |
| DF-OPS-008 | data_product_load | stale_flagged_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the product was flagged stale |
| DF-OPS-009 | data_product_load | duplicate_count | NUMBER | integer |  | Yes | 0 | None | None | None | Workbench | None | No | Repeat stamps ignored for the same product and business date |
| DF-OPS-010 | data_contract | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the data contract |
| DF-OPS-011 | data_contract | contract_code | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Contract code per source system, for example DC-ALS |
| DF-OPS-012 | data_contract | source_system | TEXT | varchar(80) | 80 | Yes | None | None | None | None | Workbench | None | No | Source system |
| DF-OPS-013 | data_contract | interface_id | TEXT | varchar(40) | 40 | Yes | None | None | None | None | Workbench | None | No | Interfaces covered, for example INT-01, INT-02 |
| DF-OPS-014 | data_contract | contract_version | NUMBER | integer |  | Yes | None | None | UK | None | Workbench | None | No | Contract version |
| DF-OPS-015 | data_contract | status | LOV | varchar(10) | 10 | Yes | DRAFT | LOV-CONTRACT-STATUS | None | None | Workbench | None | No | Draft, published or superseded |
| DF-OPS-016 | data_contract | confirmed_by_role | TEXT | varchar(80) | 80 | No | None | None | None | None | Workbench | None | No | Role of the system owner who confirmed, for example ALS system owner |
| DF-OPS-017 | data_contract | confirmed_on | DATE | date |  | No | None | None | None | None | Workbench | None | No | Date of the confirmation |
| DF-OPS-018 | data_contract | confirmation_document_ref | ATTACHMENT | varchar(400) | 400 | No | None | None | None | None | Workbench | None | No | Stored confirmation from the system owner |
| DF-OPS-019 | data_contract | published_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the contract was published |
| DF-OPS-020 | data_contract | published_by | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Who published the contract |
| DF-REF-087 | sys_objects | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the registered object |
| DF-REF-088 | sys_objects | object_name | TEXT | varchar(60) | 60 | Yes | None | None | UK | None | Workbench | None | No | Table name |
| DF-REF-089 | sys_objects | business_name | TEXT | varchar(120) | 120 | Yes | None | None | None | None | Workbench | None | No | Business name of the object |
| DF-REF-090 | sys_objects | subject_area | TEXT | varchar(10) | 10 | Yes | None | None | None | None | Workbench | None | No | Subject area code |
| DF-REF-091 | sys_objects | data_product | TEXT | varchar(10) | 10 | Yes | None | None | None | None | Workbench | None | No | Data product the object belongs to, DP01 to DP14 or None |
| DF-REF-092 | sys_objects | system_of_record | TEXT | varchar(120) | 120 | Yes | None | None | None | None | Workbench | None | No | System of record of the object |
| DF-REF-093 | sys_objects | description | TEXT | varchar(400) | 400 | Yes | None | None | None | None | Workbench | None | No | What the object holds |
| DF-REF-094 | sys_fields | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the registered field |
| DF-REF-095 | sys_fields | field_id | TEXT | varchar(16) | 16 | Yes | None | None | UK | None | Workbench | None | No | BR Field ID, for example DF-CAS-001 |
| DF-REF-096 | sys_fields | object_name | TEXT | varchar(60) | 60 | Yes | None | None | None | None | Workbench | None | No | Table the field belongs to, from sys_objects |
| DF-REF-097 | sys_fields | field_name | TEXT | varchar(60) | 60 | Yes | None | None | None | None | Workbench | None | No | Column name; unique with object_name |
| DF-REF-098 | sys_fields | data_type | TEXT | varchar(12) | 12 | Yes | None | None | None | None | Workbench | None | No | TSD data type: TEXT, NUMBER, DATE, BOOLEAN, LOV, USER_REF, CROSS_REF, FORMULA or ATTACHMENT |
| DF-REF-099 | sys_fields | physical_type | TEXT | varchar(30) | 30 | Yes | None | None | None | None | Workbench | None | No | PostgreSQL type |
| DF-REF-100 | sys_fields | is_mandatory | BOOLEAN | boolean |  | Yes | None | None | None | None | Workbench | None | No | True when the field is required |
| DF-REF-101 | sys_fields | lov_code | TEXT | varchar(30) | 30 | No | None | None | None | None | Workbench | None | No | List of values the field takes its values from |
| DF-REF-102 | sys_fields | references_object | TEXT | varchar(60) | 60 | No | None | None | None | None | Workbench | None | No | Table a cross-reference field points to |
| DF-REF-103 | sys_fields | source_system | TEXT | varchar(80) | 80 | Yes | None | None | None | None | Workbench | None | No | Source system of the value |
| DF-REF-104 | sys_fields | source_field | TEXT | varchar(80) | 80 | No | None | None | None | None | Workbench | None | No | Field name in the source system |
| DF-REF-105 | sys_fields | is_personal | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True for personal data under PDPA |
| DF-REF-106 | sys_fields | description | TEXT | varchar(400) | 400 | Yes | None | None | None | None | Workbench | None | No | Meaning of the field |
| DF-REF-107 | sys_fields | owner_role | LOV | varchar(20) | 20 | No | None | LOV-ROLE | None | None | Workbench | None | No | Owner of the field definition |
| DF-REF-108 | sys_fields | refresh_cycle | TEXT | varchar(30) | 30 | No | None | None | None | None | Workbench | None | No | Refresh frequency, for example Daily, end of day |
| DF-REF-109 | sys_fields | late_behavior | TEXT | varchar(200) | 200 | No | None | None | None | None | Workbench | None | No | What the Workbench does when the value is missing or late |
| DF-REF-110 | sys_fields | interface_id | TEXT | varchar(10) | 10 | No | None | None | None | None | Workbench | None | No | Interface that carries the field, INT-01 to INT-34; empty for Workbench fields |
| DF-REF-111 | sys_field_version | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the field version |
| DF-REF-112 | sys_field_version | field_id | TEXT | varchar(16) | 16 | Yes | None | None | UK | None | Workbench | None | No | Field the version belongs to, from sys_fields |
| DF-REF-113 | sys_field_version | field_version | NUMBER | integer |  | Yes | None | None | UK | None | Workbench | None | No | Version number |
| DF-REF-114 | sys_field_version | definition | TEXT | jsonb |  | Yes | None | None | None | None | Workbench | None | No | The full field definition at this version |
| DF-REF-115 | sys_field_version | change_reason | TEXT | varchar(400) | 400 | Yes | None | None | None | None | Workbench | None | No | Reason for the change |
| DF-OPS-021 | load_run | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the load or job run |
| DF-OPS-022 | load_run | interface_id | TEXT | varchar(10) | 10 | No | None | None | None | None | Workbench | None | No | Interface loaded, for example INT-01; TRACKER for tracker loads; empty for job steps |
| DF-OPS-023 | load_run | job_code | TEXT | varchar(6) | 6 | No | None | None | None | None | Workbench | None | No | Job the run belongs to, for example JOB-01 |
| DF-OPS-024 | load_run | product_code | LOV | varchar(25) | 25 | No | None | LOV-DATA-PRODUCT | None | None | Workbench | None | No | Data product loaded or built |
| DF-OPS-025 | load_run | business_date | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Business date of the load |
| DF-OPS-026 | load_run | status | LOV | varchar(12) | 12 | Yes | RUNNING | LOV-LOAD-STATUS | None | None | Workbench | None | No | Running, completed, refused, late, failed or superseded |
| DF-OPS-027 | load_run | started_at | DATE | timestamptz |  | Yes | None | None | None | None | Workbench | None | No | When the run started |
| DF-OPS-028 | load_run | ended_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the run ended |
| DF-OPS-029 | load_run | rows_read | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Records read from the source |
| DF-OPS-030 | load_run | rows_loaded | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Records written |
| DF-OPS-031 | load_run | rows_held | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Records held in the exception list |
| DF-OPS-032 | load_run | rows_rejected | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Rows rejected |
| DF-OPS-033 | load_run | failed_check | TEXT | varchar(8) | 8 | No | None | None | None | None | Workbench | None | No | Check that refused the load, for example DQ-003 |
| DF-OPS-034 | load_run | check_results | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Result per check code, plus the sample and other counts |
| DF-OPS-035 | load_run | mapping_version | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | Source field mapping version used |
| DF-OPS-036 | load_run | interface_run_id | CROSS_REF | uuid |  | No | None | None | FK | interface_run | Workbench | None | No | The P2 interface run the file load belongs to |
| DF-OPS-037 | load_run | tracker_id | CROSS_REF | uuid |  | No | None | None | FK | tracker_inventory | Workbench | None | No | Tracker of a tracker load |
| DF-OPS-038 | load_run | loaded_by | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | User who uploaded the file |
| DF-OPS-039 | load_run | source_file_name | TEXT | varchar(200) | 200 | No | None | None | None | None | Workbench | None | No | Name of the loaded file |
| DF-OPS-040 | load_run | source_file_hash | TEXT | char(64) | 64 | No | None | None | None | None | Workbench | None | No | SHA-256 of the loaded file |
| DF-OPS-041 | dq_exception | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the data quality exception |
| DF-OPS-042 | dq_exception | load_run_id | CROSS_REF | uuid |  | Yes | None | None | FK | load_run | Workbench | None | No | The load run that raised it |
| DF-OPS-043 | dq_exception | product_code | LOV | varchar(25) | 25 | Yes | None | LOV-DATA-PRODUCT | None | None | Workbench | None | No | Data product of the record |
| DF-OPS-044 | dq_exception | check_code | TEXT | varchar(8) | 8 | Yes | None | None | None | None | Workbench | None | No | Load check (DQ-nnn), row rule (DQnn), reconciliation (REC-nn) or tracker check (TRK-nn) |
| DF-OPS-045 | dq_exception | record_key | TEXT | varchar(60) | 60 | Yes | None | None | None | None | Workbench | None | No | Business key of the failing record, for example the account number; never personal data |
| DF-OPS-046 | dq_exception | reason_code | TEXT | varchar(8) | 8 | Yes | None | None | None | None | Workbench | None | No | Reason code shown to the data product owner |
| DF-OPS-047 | dq_exception | detail | TEXT | varchar(400) | 400 | No | None | None | None | None | Workbench | None | No | Short reason without personal data |
| DF-OPS-048 | dq_exception | raised_on | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Business date raised |
| DF-OPS-049 | dq_exception | status | LOV | varchar(10) | 10 | Yes | OPEN | LOV-DQ-STATUS | None | None | Workbench | None | No | Open or cleared |
| DF-OPS-050 | dq_exception | rule_version | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | Rule version that raised the exception |
| DF-OPS-051 | dq_exception | cleared_on | DATE | date |  | No | None | None | None | None | Workbench | None | No | Date the record passed again |
| DF-OPS-052 | dq_rule | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the data quality rule |
| DF-OPS-053 | dq_rule | rule_code | TEXT | varchar(8) | 8 | Yes | None | None | UK | None | Workbench | None | No | Rule code, for example DQ02 |
| DF-OPS-054 | dq_rule | rule_version | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Rule version |
| DF-OPS-055 | dq_rule | rule_name | TEXT | varchar(120) | 120 | Yes | None | None | None | None | Workbench | None | No | Rule name |
| DF-OPS-056 | dq_rule | product_code | LOV | varchar(25) | 25 | Yes | None | LOV-DATA-PRODUCT | None | None | Workbench | None | No | Data product the rule runs for |
| DF-OPS-057 | dq_rule | target_entity | TEXT | varchar(60) | 60 | Yes | None | None | None | None | Workbench | None | No | P1 table the rule checks |
| DF-OPS-058 | dq_rule | rule_type | LOV | varchar(15) | 15 | Yes | None | LOV-DQ-RULE-TYPE | None | None | Workbench | None | No | Not null, unique across, range, sum equals, exists link, maximum age in days, field before |
| DF-OPS-059 | dq_rule | rule_params | TEXT | jsonb |  | Yes | None | None | None | None | Workbench | None | No | Fields and values for the rule type |
| DF-OPS-060 | dq_rule | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the version comes into force |
| DF-OPS-061 | dq_rule | valid_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Last date the version is in force |
| DF-OPS-062 | dq_rule | approved_by | USER_REF | uuid |  | Yes | None | None | None | None | Workbench | None | No | Who approved the version |
| DF-OPS-063 | dq_rule | test_case_id | TEXT | varchar(20) | 20 | Yes | None | None | None | None | Workbench | None | No | Test case that proves the rule |
| DF-OPS-064 | source_field_map | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the source field mapping |
| DF-OPS-065 | source_field_map | interface_id | TEXT | varchar(10) | 10 | Yes | None | None | UK | None | Workbench | None | No | Interface the mapping is for |
| DF-OPS-066 | source_field_map | mapping_version | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Mapping version |
| DF-OPS-067 | source_field_map | source_field | TEXT | varchar(80) | 80 | Yes | None | None | UK | None | Workbench | None | No | Field name in the source |
| DF-OPS-068 | source_field_map | target_entity | TEXT | varchar(60) | 60 | Yes | None | None | None | None | Workbench | None | No | Workbench entity |
| DF-OPS-069 | source_field_map | target_field | TEXT | varchar(60) | 60 | Yes | None | None | None | None | Workbench | None | No | Workbench field |
| DF-OPS-070 | source_field_map | transformation | TEXT | varchar(200) | 200 | Yes | None | None | None | None | Workbench | None | No | Transformation type and parameters: COPY_TRIM, SUM, TO_DATE_BE, TO_NUMERIC_2, BOOLEAN_YN, CODE_MAP, BUSINESS_DATE |
| DF-OPS-071 | source_field_map | approved_by | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Who approved the mapping version |
| DF-OPS-072 | source_field_map | approved_on | DATE | date |  | No | None | None | None | None | Workbench | None | No | Approval date |
| DF-OPS-073 | source_field_map | approval_ref | TEXT | varchar(200) | 200 | No | None | None | None | None | Workbench | None | No | Reference of the system owner's sign-off on the mapping version |
| DF-OPS-074 | source_field_map | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the version comes into force |
| DF-OPS-075 | source_code_map | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the source code mapping |
| DF-OPS-076 | source_code_map | interface_id | TEXT | varchar(10) | 10 | Yes | None | None | UK | None | Workbench | None | No | Interface the code map is for |
| DF-OPS-077 | source_code_map | lov_code | TEXT | varchar(30) | 30 | Yes | None | None | UK | None | Workbench | None | No | Target list of values |
| DF-OPS-078 | source_code_map | source_code | TEXT | varchar(30) | 30 | Yes | None | None | UK | None | Workbench | None | No | Code in the source |
| DF-OPS-079 | source_code_map | value_code | TEXT | varchar(30) | 30 | Yes | None | None | None | None | Workbench | None | No | Workbench list value |
| DF-OPS-080 | source_code_map | map_version | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Code map version |
| DF-OPS-081 | source_code_map | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the version comes into force |
| DF-OPS-082 | source_code_map | valid_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Last date the version is in force |
| DF-OPS-083 | tracker_inventory | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the tracker |
| DF-OPS-084 | tracker_inventory | tracker_code | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Tracker code |
| DF-OPS-085 | tracker_inventory | inventory_version | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Inventory version |
| DF-OPS-086 | tracker_inventory | team_code | LOV | varchar(20) | 20 | Yes | None | LOV-TEAM | None | None | Workbench | None | No | Owning team |
| DF-OPS-087 | tracker_inventory | tracker_name | TEXT | varchar(120) | 120 | Yes | None | None | None | None | Workbench | None | No | Tracker name |
| DF-OPS-088 | tracker_inventory | location_type | LOV | varchar(12) | 12 | Yes | None | LOV-TRACKER-LOCATION | None | None | Workbench | None | No | Excel, SharePoint, local file or none |
| DF-OPS-089 | tracker_inventory | location_ref | TEXT | varchar(400) | 400 | No | None | None | None | None | Workbench | None | No | Where the tracker is kept |
| DF-OPS-090 | tracker_inventory | owner_user_id | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Tracker owner |
| DF-OPS-091 | tracker_inventory | field_list | TEXT | jsonb |  | Yes | None | None | None | None | Workbench | None | No | Field names with the personal data tag and the optional mapped-to field |
| DF-OPS-092 | tracker_inventory | update_cycle | LOV | varchar(10) | 10 | No | None | LOV-UPDATE-CYCLE | None | None | Workbench | None | No | Daily, weekly, monthly or ad hoc |
| DF-OPS-093 | tracker_inventory | target_product | LOV | varchar(25) | 25 | No | None | LOV-DATA-PRODUCT | None | None | Workbench | None | No | Target data product for a LOAD decision |
| DF-OPS-094 | tracker_inventory | decision | LOV | varchar(8) | 8 | No | None | LOV-TRACKER-DECISION | None | None | Workbench | None | No | Load, retire or keep |
| DF-OPS-095 | tracker_inventory | decision_reason | TEXT | varchar(400) | 400 | No | None | None | None | None | Workbench | None | No | Reason for the decision |
| DF-OPS-096 | tracker_inventory | status | LOV | varchar(12) | 12 | Yes | LISTED | LOV-TRACKER-STATUS | None | None | Workbench | None | No | Listed, loaded, signed off, retired or kept |
| DF-OPS-097 | tracker_inventory | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the inventory version comes into force |
| DF-OPS-098 | tracker_inventory | file_rows | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Rows in the loaded file |
| DF-OPS-099 | tracker_inventory | loaded_rows | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Rows loaded |
| DF-OPS-100 | tracker_inventory | rejected_rows | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Rows rejected |
| DF-OPS-101 | tracker_inventory | last_load_run_id | CROSS_REF | uuid |  | No | None | None | FK | load_run | Workbench | None | No | Latest load run of the tracker |
| DF-OPS-102 | tracker_inventory | signed_off_by | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Team manager who signed off the load |
| DF-OPS-103 | tracker_inventory | signed_off_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | Sign-off time |
| DF-OPS-104 | tracker_inventory | source_file_ref | ATTACHMENT | varchar(400) | 400 | No | None | None | None | None | Workbench | None | No | Stored tracker file in the write-once store |
| DF-OPS-105 | tracker_inventory | archive_ref | TEXT | varchar(400) | 400 | No | None | None | None | None | Workbench | None | No | Read-only archive location of the retired tracker |
| DF-OPS-106 | tracker_inventory | retired_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | Retirement time |
| DF-OPS-107 | tracker_inventory | retire_confirmed_by | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Team manager who confirmed the retirement |
| DF-OPS-108 | tracker_inventory | unfed_fields | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Non-personal tracker fields no data product field carries |
| DF-OPS-109 | tracker_row | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the tracker row |
| DF-OPS-110 | tracker_row | tracker_id | CROSS_REF | uuid |  | Yes | None | None | FK | tracker_inventory | Workbench | None | No | Tracker the row came from |
| DF-OPS-111 | tracker_row | load_run_id | CROSS_REF | uuid |  | Yes | None | None | FK | load_run | Workbench | None | No | Load run that loaded the row |
| DF-OPS-112 | tracker_row | row_no | NUMBER | integer |  | Yes | None | None | None | None | Workbench | None | No | Row number in the file |
| DF-OPS-113 | tracker_row | account_no | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | Account number |
| DF-OPS-114 | tracker_row | target_product | LOV | varchar(25) | 25 | Yes | None | LOV-DATA-PRODUCT | None | None | Workbench | None | No | Target data product |
| DF-OPS-115 | tracker_row | source_file_name | TEXT | varchar(200) | 200 | Yes | None | None | None | None | Workbench | None | No | Source file name |
| DF-OPS-116 | tracker_row | field_values | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Non-personal tracker fields of the row |
| DF-OPS-117 | tracker_row | loaded_on | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Load date |
| DF-RPT-001 | case_list_row | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the case list row |
| DF-RPT-002 | case_list_row | business_date | DATE | date |  | Yes | None | None | UK | None | Workbench | None | No | Business date of the list |
| DF-RPT-003 | case_list_row | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | None | No | Case |
| DF-RPT-004 | case_list_row | case_no | TEXT | varchar(18) | 18 | Yes | None | None | None | None | Workbench | None | No | Case number |
| DF-RPT-005 | case_list_row | account_id | CROSS_REF | uuid |  | Yes | None | None | FK | loan_account | Workbench | None | No | Loan account; unique with business_date |
| DF-RPT-006 | case_list_row | account_no | TEXT | varchar(20) | 20 | Yes | None | None | None | None | Workbench | None | No | Account number |
| DF-RPT-007 | case_list_row | product_group | LOV | varchar(15) | 15 | Yes | None | LOV-PRODUCT | None | None | Workbench | None | No | Product group |
| DF-RPT-008 | case_list_row | stage_code | LOV | varchar(20) | 20 | No | None | LOV-STAGE | None | None | Workbench | None | No | Stage |
| DF-RPT-009 | case_list_row | status | LOV | varchar(20) | 20 | Yes | None | LOV-CASE-STATUS | None | None | Workbench | None | No | Case status |
| DF-RPT-010 | case_list_row | owner_user_id | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Case owner |
| DF-RPT-011 | case_list_row | queue_code | TEXT | varchar(30) | 30 | No | None | None | None | None | Workbench | None | No | Queue code |
| DF-RPT-012 | case_list_row | team_code | LOV | varchar(20) | 20 | No | None | LOV-TEAM | None | None | Workbench | None | No | Team |
| DF-RPT-013 | case_list_row | route_code | LOV | varchar(4) | 4 | No | None | LOV-ROUTE | None | None | Workbench | None | No | Route |
| DF-RPT-014 | case_list_row | total_balance | NUMBER | numeric(18,2) | 18,2 | Yes | 0 | None | None | None | Workbench | None | No | Total balance, baht |
| DF-RPT-015 | case_list_row | days_past_due | NUMBER | integer |  | Yes | 0 | None | None | None | Workbench | None | No | Days past due |
| DF-RPT-016 | case_list_row | refreshed_at | DATE | timestamptz |  | Yes | None | None | None | None | Workbench | None | No | When the row was built |
| DF-RPT-017 | case_list_row | last_contact_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | Latest EFS contact across the case's accounts |
| DF-RPT-018 | case_list_row | last_action_code | LOV | varchar(10) | 10 | No | None | LOV-ACTION-CODE | None | None | Workbench | None | No | Action code of the latest contact |
| DF-RPT-019 | case_list_row | publish_status | LOV | varchar(10) | 10 | Yes | PENDING | LOV-PUBLISH-STATUS | None | None | Workbench | None | No | Pending, held or released for the date's extract |
| DF-INT-030 | collections_history | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the collections history record |
| DF-INT-031 | collections_history | account_no | TEXT | varchar(20) | 20 | Yes | None | None | None | None | EFS via COLLINS | None | No | Account number |
| DF-INT-032 | collections_history | efs_record_key | TEXT | varchar(40) | 40 | Yes | None | None | UK | None | EFS via COLLINS | None | No | EFS record key |
| DF-INT-033 | collections_history | contact_at | DATE | timestamptz |  | Yes | None | None | None | None | EFS via COLLINS | None | No | Contact date and time |
| DF-INT-034 | collections_history | action_code | LOV | varchar(10) | 10 | Yes | None | LOV-ACTION-CODE | None | None | EFS via COLLINS | Actioncode ID | No | EFS action code |
| DF-INT-035 | collections_history | action_contact_status | TEXT | varchar(20) | 20 | No | None | None | None | None | EFS via COLLINS | None | No | EFS action contact status |
| DF-INT-036 | collections_history | contact_result | LOV | varchar(20) | 20 | No | None | LOV-CONTACT-RESULT | None | None | EFS via COLLINS | Call Result | No | Call result |
| DF-INT-037 | collections_history | promise_amount | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | EFS via COLLINS | None | No | Amount promised, baht |
| DF-INT-038 | collections_history | promise_date | DATE | date |  | No | None | None | None | None | EFS via COLLINS | None | No | Date promised |
| DF-INT-039 | collections_history | business_date | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Business date of the load |
| DF-OPS-118 | reconciliation_result | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the reconciliation result |
| DF-OPS-119 | reconciliation_result | rec_code | TEXT | varchar(6) | 6 | Yes | None | None | UK | None | Workbench | None | No | Reconciliation, REC-01 or REC-02 |
| DF-OPS-120 | reconciliation_result | business_date | DATE | date |  | Yes | None | None | UK | None | Workbench | None | No | Business date |
| DF-OPS-121 | reconciliation_result | product_group | LOV | varchar(15) | 15 | Yes | None | LOV-PRODUCT | UK | None | Workbench | None | No | Product group |
| DF-OPS-122 | reconciliation_result | source_count | NUMBER | integer |  | Yes | None | None | None | None | Workbench | None | No | ALS count |
| DF-OPS-123 | reconciliation_result | workbench_count | NUMBER | integer |  | Yes | None | None | None | None | Workbench | None | No | Case list count |
| DF-OPS-124 | reconciliation_result | source_amount | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Workbench | None | No | ALS balance sum, baht |
| DF-OPS-125 | reconciliation_result | workbench_amount | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Workbench | None | No | Case list balance sum, baht |
| DF-OPS-126 | reconciliation_result | variance_count | NUMBER | integer |  | Yes | None | None | None | None | Workbench | None | No | Count difference |
| DF-OPS-127 | reconciliation_result | variance_pct | NUMBER | numeric(9,4) | 9,4 | Yes | None | None | None | None | Workbench | None | No | Variance, percent |
| DF-OPS-128 | reconciliation_result | tolerance_pct | NUMBER | numeric(9,4) | 9,4 | Yes | None | None | None | None | Workbench | None | No | Tolerance used, percent |
| DF-OPS-129 | reconciliation_result | result | LOV | varchar(8) | 8 | Yes | None | LOV-REC-RESULT | None | None | Workbench | None | No | Pass or break |
| DF-OPS-130 | lake_copy_watermark | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the lake copy watermark |
| DF-OPS-131 | lake_copy_watermark | copy_name | TEXT | varchar(40) | 40 | Yes | None | None | UK | None | Workbench | None | No | Name of the copy; DECISION_LOG for the decision log lake copy |
| DF-OPS-132 | lake_copy_watermark | last_entry_hash | TEXT | char(64) | 64 | No | None | None | None | None | Workbench | None | No | Entry hash of the last decision log entry copied and matched |
| DF-OPS-133 | lake_copy_watermark | last_decided_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | decided_at of the last entry copied |
| DF-OPS-134 | lake_copy_watermark | rows_copied_total | NUMBER | bigint |  | Yes | 0 | None | None | None | Workbench | None | No | Cumulative count of entries in the lake copy |
| DF-OPS-135 | lake_copy_watermark | business_date | DATE | date |  | No | None | None | None | None | Workbench | None | No | Business date of the last complete partition |
| DF-REF-116 | retention_rule | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the retention rule |
| DF-REF-117 | retention_rule | product_code | LOV | varchar(25) | 25 | Yes | None | LOV-DATA-PRODUCT | None | None | Workbench | None | No | Data product the rule applies to |
| DF-REF-118 | retention_rule | table_name | TEXT | varchar(60) | 60 | Yes | None | None | UK | None | Workbench | None | No | Table the rule applies to, from sys_objects; never decision_log_entry |
| DF-REF-119 | retention_rule | record_class | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Retention class from LOV-RETENTION, or LAKE_COPY for the decision log lake copy |
| DF-REF-120 | retention_rule | retention_months | NUMBER | integer |  | Yes | None | None | None | None | Workbench | None | No | Retention period in months, 1 to 600 |
| DF-REF-121 | retention_rule | age_basis_field | TEXT | varchar(60) | 60 | Yes | None | None | None | None | Workbench | None | No | Field the age is measured from, for example interaction.occurred_at |
| DF-REF-122 | retention_rule | end_action | LOV | varchar(12) | 12 | Yes | ARCHIVE | LOV-RETENTION-END | None | None | Workbench | None | No | Archive or review at the end of the period |
| DF-REF-123 | retention_rule | rule_version | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Version, for example RET-2026.11 |
| DF-REF-124 | retention_rule | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the version comes into force |
| DF-REF-125 | retention_rule | valid_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Last date the version is in force |
| DF-REF-126 | retention_rule | approved_by | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Who approved the version |
| DF-REF-127 | retention_rule | reference_version_id | CROSS_REF | uuid |  | No | None | None | FK | reference_version | Workbench | None | No | Reference version that brought the row |
| DF-TRT-034 | dp_treatment | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the treatment copy |
| DF-TRT-035 | dp_treatment | treatment_id | CROSS_REF | uuid |  | Yes | None | None | FK | treatment | Workbench | treatment.id | No | The treatment copied; unique with business_date |
| DF-TRT-036 | dp_treatment | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | treatment.case_id | No | The case of the treatment |
| DF-TRT-037 | dp_treatment | decision_log_id | CROSS_REF | uuid |  | No | None | None | FK | decision_log_entry | Workbench | treatment.decision_log_id | No | The decision that approved the treatment |
| DF-TRT-038 | dp_treatment | treatment_type | LOV | varchar(20) | 20 | Yes | None | LOV-TREATMENT | None | None | Workbench | treatment.treatment_type | No | Treatment type |
| DF-TRT-039 | dp_treatment | proposed_by | LOV | varchar(10) | 10 | Yes | None | LOV-PROPOSER | None | None | Workbench | treatment.proposed_by | No | Agent, rule or person |
| DF-TRT-040 | dp_treatment | proposed_at | DATE | timestamptz |  | Yes | None | None | None | None | Workbench | treatment.proposed_at | No | When proposed |
| DF-TRT-041 | dp_treatment | offer_amount | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Workbench | treatment.offer_amount | No | Amount offered or agreed, baht |
| DF-TRT-042 | dp_treatment | haircut_amount | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Workbench | treatment.haircut_amount | No | Amount forgiven, baht |
| DF-TRT-043 | dp_treatment | installments | NUMBER | integer |  | No | None | None | None | None | Workbench | treatment.installments | No | Number of installments in a plan |
| DF-TRT-044 | dp_treatment | valid_until | DATE | date |  | No | None | None | None | None | Workbench | treatment.valid_until | No | Offer validity |
| DF-TRT-045 | dp_treatment | approval_level | LOV | varchar(4) | 4 | No | None | LOV-APPROVAL-LEVEL | None | None | Workbench | treatment.approval_level | No | Approval level that approved it |
| DF-TRT-046 | dp_treatment | booked_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | treatment.booked_at | No | When booked in the core |
| DF-TRT-047 | dp_treatment | outcome | LOV | varchar(12) | 12 | No | None | LOV-TRT-OUTCOME | None | None | Workbench | treatment.outcome | No | Kept, broken, completed, canceled or declined |
| DF-TRT-048 | dp_treatment | outcome_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | treatment.outcome_at | No | When the outcome was recorded |
| DF-TRT-049 | dp_treatment | business_date | DATE | date |  | Yes | None | None | UK | None | Workbench | None | No | Business date of the build |
| DF-TRT-050 | dp_treatment | contract_no | TEXT | varchar(20) | 20 | No | None | None | None | None | Core bank (ALS) via COLLINS | ContractNo | No | Contract number of the case's primary account |
| DF-TRT-051 | dp_treatment | contract_date | DATE | date |  | No | None | None | None | None | Core bank (ALS) via COLLINS | CONTRACT_DATE | No | Contract date of the case's primary account |
| DF-TRT-052 | dp_guarantee_claim | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the guarantee claim copy |
| DF-TRT-053 | dp_guarantee_claim | guarantee_claim_id | CROSS_REF | uuid |  | Yes | None | None | FK | guarantee_claim | Workbench | guarantee_claim.id | No | The guarantee claim copied; unique with business_date |
| DF-TRT-054 | dp_guarantee_claim | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | guarantee_claim.case_id | No | The case of the claim |
| DF-TRT-055 | dp_guarantee_claim | claim_type | LOV | varchar(25) | 25 | Yes | None | LOV-CLAIM-TYPE | None | None | Workbench | guarantee_claim.claim_type | No | TCG, credit life insurance, mortgage insurance or collateral insurance |
| DF-TRT-056 | dp_guarantee_claim | claim_deadline | DATE | date |  | Yes | None | None | None | None | Workbench | guarantee_claim.claim_deadline | No | Last date the claim can be filed |
| DF-TRT-057 | dp_guarantee_claim | claimed_amount | NUMBER | numeric(18,2) | 18,2 | Yes | None | None | None | None | Workbench | guarantee_claim.claimed_amount | No | Amount claimed, baht |
| DF-TRT-058 | dp_guarantee_claim | filed_at | DATE | date |  | No | None | None | None | None | Workbench | guarantee_claim.filed_at | No | Date filed |
| DF-TRT-059 | dp_guarantee_claim | paid_amount | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Workbench | guarantee_claim.paid_amount | No | Amount paid, baht |
| DF-TRT-060 | dp_guarantee_claim | status | LOV | varchar(12) | 12 | Yes | None | LOV-CLAIM-STATUS | None | None | Workbench | guarantee_claim.status | No | Preparing, filed, defect, paid or rejected |
| DF-TRT-061 | dp_guarantee_claim | business_date | DATE | date |  | Yes | None | None | UK | None | Workbench | None | No | Business date of the build |
| DF-OPS-136 | interface_config | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the interface setting |
| DF-OPS-137 | interface_config | interface_id | TEXT | varchar(10) | 10 | Yes | None | None | UK | None | Workbench | None | No | Interface ID, for example INT-10 |
| DF-OPS-138 | interface_config | direction | LOV | varchar(8) | 8 | Yes | None | LOV-DIRECTION | None | None | Workbench | None | No | Inbound or outbound |
| DF-OPS-139 | interface_config | transport | LOV | varchar(10) | 10 | Yes | None | LOV-TRANSPORT | None | None | Workbench | None | No | SFTP or COLLINS |
| DF-OPS-140 | interface_config | inbound_path | TEXT | varchar(200) | 200 | No | None | None | None | None | Workbench | None | No | Inbound or outbound folder |
| DF-OPS-141 | interface_config | file_pattern | TEXT | varchar(120) | 120 | No | None | None | None | None | Workbench | None | No | File name pattern with the business date |
| DF-OPS-142 | interface_config | data_product | LOV | varchar(25) | 25 | No | None | LOV-DATA-PRODUCT | None | None | Workbench | None | No | Data product the file feeds, for example DP06 |
| DF-OPS-143 | interface_config | max_attempts | NUMBER | integer |  | Yes | None | None | None | None | Workbench | None | No | Most send attempts before the exception queue |
| DF-OPS-144 | interface_config | retry_intervals_min | TEXT | varchar(60) | 60 | No | None | None | None | None | Workbench | None | No | Minutes between attempts, comma separated, for example 5,15,45 |
| DF-OPS-145 | interface_config | owner_role | LOV | varchar(20) | 20 | Yes | None | LOV-ROLE | None | None | Workbench | None | No | Role that receives the exception task |
| DF-OPS-146 | interface_config | alert_role | LOV | varchar(20) | 20 | No | None | LOV-ROLE | None | None | Workbench | None | No | Role alerted on a refused or missing file |
| DF-OPS-147 | interface_config | valid_from | DATE | date |  | Yes | None | None | UK | None | Workbench | None | No | Date the version comes into force |
| DF-OPS-148 | interface_config | valid_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Last date the version is in force |
| DF-OPS-149 | interface_run | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the interface run |
| DF-OPS-150 | interface_run | interface_id | TEXT | varchar(10) | 10 | Yes | None | None | UK | None | Workbench | None | No | Interface ID |
| DF-OPS-151 | interface_run | file_name | TEXT | varchar(200) | 200 | Yes | None | None | None | None | Workbench | None | No | File name |
| DF-OPS-152 | interface_run | file_hash | TEXT | char(64) | 64 | Yes | None | None | UK | None | Workbench | None | No | SHA-256 of the file |
| DF-OPS-153 | interface_run | business_date | DATE | date |  | Yes | None | None | UK | None | Workbench | None | No | Business date of the file |
| DF-OPS-154 | interface_run | record_count | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Records read |
| DF-OPS-155 | interface_run | control_total | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Workbench | None | No | Control total from the trailer |
| DF-OPS-156 | interface_run | status | LOV | varchar(12) | 12 | Yes | RECEIVED | LOV-INTERFACE-RUN | None | None | Workbench | None | No | Received, loaded, refused, missing, duplicate or failed |
| DF-OPS-157 | interface_run | failed_check | TEXT | varchar(40) | 40 | No | None | None | None | None | Workbench | None | No | Load check ID and name that refused the file |
| DF-OPS-158 | interface_run | checks | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Result of each check and the run summary counts |
| DF-OPS-159 | interface_run | started_at | DATE | timestamptz |  | Yes | None | None | None | None | Workbench | None | No | Run start |
| DF-OPS-160 | interface_run | ended_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | Run end |
| DF-OPS-161 | interface_signoff | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the interface sign-off |
| DF-OPS-162 | interface_signoff | interface_id | TEXT | varchar(10) | 10 | Yes | None | None | UK | None | Workbench | None | No | Interface whose manual handling is retired |
| DF-OPS-163 | interface_signoff | from_date | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | First clean day counted |
| DF-OPS-164 | interface_signoff | to_date | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Last clean day counted |
| DF-OPS-165 | interface_signoff | clean_days | NUMBER | integer |  | Yes | None | None | None | None | Workbench | None | No | Clean days in a row at sign-off |
| DF-OPS-166 | interface_signoff | signed_by | USER_REF | uuid |  | Yes | None | None | None | None | Workbench | None | No | Data steward who signed off |
| DF-OPS-167 | interface_signoff | signed_at | DATE | timestamptz |  | Yes | None | None | None | None | Workbench | None | No | When signed off |
| DF-OPS-168 | outbound_item | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the outbound item |
| DF-OPS-169 | outbound_item | interface_id | TEXT | varchar(10) | 10 | Yes | None | None | None | None | Workbench | None | No | Interface ID |
| DF-OPS-170 | outbound_item | idempotency_key | TEXT | varchar(120) | 120 | Yes | None | None | UK | None | Workbench | None | No | Unique key of the outbound work |
| DF-OPS-171 | outbound_item | payload_ref | ATTACHMENT | varchar(400) | 400 | Yes | None | None | None | None | Workbench | None | No | Stored file to send |
| DF-OPS-172 | outbound_item | case_ids | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Cases whose step waits on the file |
| DF-OPS-173 | outbound_item | attempt_count | NUMBER | integer |  | Yes | 0 | None | None | None | Workbench | None | No | Attempts made |
| DF-OPS-174 | outbound_item | next_attempt_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the next attempt is due |
| DF-OPS-175 | outbound_item | status | LOV | varchar(12) | 12 | Yes | PENDING | LOV-OUTBOUND-STATUS | None | None | Workbench | None | No | Pending, sent, retry, exception or acknowledged |
| DF-OPS-176 | outbound_item | last_error | TEXT | varchar(400) | 400 | No | None | None | None | None | Workbench | None | No | Last transfer error, no personal data |
| DF-OPS-177 | outbound_item | owner_role | LOV | varchar(20) | 20 | Yes | None | LOV-ROLE | None | None | Workbench | None | No | Role that owns the exception task |
| DF-OPS-178 | processed_event | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the processed event |
| DF-OPS-179 | processed_event | consumer | TEXT | varchar(60) | 60 | Yes | None | None | UK | None | Workbench | None | No | Consumer name |
| DF-OPS-180 | processed_event | idempotency_key | TEXT | varchar(120) | 120 | Yes | None | None | UK | None | Workbench | None | No | Event or work key |
| DF-OPS-181 | processed_event | event_id | CROSS_REF | uuid |  | No | None | None | FK | outbox_event | Workbench | None | No | Outbox event of the first delivery, where the key came from an event |
| DF-OPS-182 | processed_event | hit_count | NUMBER | integer |  | Yes | 1 | None | None | None | Workbench | None | No | Deliveries seen, 1 on first |
| DF-OPS-183 | processed_event | last_seen_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the last repeat arrived |
| DF-OPS-184 | idempotency_key | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the idempotent request |
| DF-OPS-185 | idempotency_key | idempotency_key | TEXT | uuid |  | Yes | None | None | UK | None | Workbench | None | No | Idempotency-Key header value |
| DF-OPS-186 | idempotency_key | endpoint | TEXT | varchar(100) | 100 | Yes | None | None | None | None | Workbench | None | No | Method and path of the request |
| DF-OPS-187 | idempotency_key | request_hash | TEXT | char(64) | 64 | Yes | None | None | None | None | Workbench | None | No | SHA-256 of the request body |
| DF-OPS-188 | idempotency_key | response | TEXT | jsonb |  | Yes | None | None | None | None | Workbench | None | No | Stored response returned to a repeat |
| DF-OPS-189 | outbox_event | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the outbox event |
| DF-OPS-190 | outbox_event | event_type | TEXT | varchar(40) | 40 | Yes | None | None | None | None | Workbench | None | No | Event name from EV-01 to EV-28, or an outbound work request type such as WIN_DISPATCH |
| DF-OPS-191 | outbox_event | schema_version | NUMBER | integer |  | Yes | None | None | None | None | Workbench | None | No | Schema version of the payload; consumers accept the current and previous version |
| DF-OPS-192 | outbox_event | case_id | CROSS_REF | uuid |  | No | None | None | FK | recovery_case | Workbench | None | No | The case the event belongs to; empty for events with no case; unique with case_seq |
| DF-OPS-193 | outbox_event | case_seq | NUMBER | bigint |  | No | None | None | UK | None | Workbench | None | No | Order of the event among the events of its case |
| DF-OPS-194 | outbox_event | idempotency_key | TEXT | varchar(120) | 120 | Yes | None | None | UK | None | Workbench | None | No | Key passed to every consumer so a repeat is dropped; unique on its own |
| DF-OPS-195 | outbox_event | payload | TEXT | jsonb |  | Yes | None | None | None | None | Workbench | None | No | References and codes only; no personal data |
| DF-OPS-196 | outbox_event | actor_ref | TEXT | varchar(64) | 64 | No | None | None | None | None | Workbench | None | No | User ID or service identity that caused the event |
| DF-OPS-197 | outbox_event | occurred_at | DATE | timestamptz |  | Yes | None | None | None | None | Workbench | None | No | When the change happened |
| DF-OPS-198 | outbox_delivery | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the outbox delivery |
| DF-OPS-199 | outbox_delivery | event_id | CROSS_REF | uuid |  | Yes | None | None | FK | outbox_event | Workbench | None | No | The outbox event delivered |
| DF-OPS-200 | outbox_delivery | consumer | TEXT | varchar(60) | 60 | Yes | None | None | UK | None | Workbench | None | No | Consumer name from the consumer list; unique with event_id |
| DF-OPS-201 | outbox_delivery | status | LOV | varchar(12) | 12 | Yes | PENDING | LOV-OUTBOX-DELIVERY | None | None | Workbench | None | No | Pending, retrying, delivered or exception |
| DF-OPS-202 | outbox_delivery | attempt_count | NUMBER | integer |  | Yes | 0 | None | None | None | Workbench | None | No | Delivery attempts made |
| DF-OPS-203 | outbox_delivery | next_attempt_at | DATE | timestamptz |  | Yes | None | None | None | None | Workbench | None | No | When the next attempt is due |
| DF-OPS-204 | outbox_delivery | last_error_code | TEXT | varchar(40) | 40 | No | None | None | None | None | Workbench | None | No | Code of the last failure returned by the consumer |
| DF-OPS-205 | outbox_delivery | delivered_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the consumer succeeded |
| DF-OPS-206 | outbox_delivery | task_id | CROSS_REF | uuid |  | No | None | None | FK | task | Workbench | None | No | The RESOLVE_OUTBOX_DELIVERY task raised when the delivery entered the exception queue |
| DF-OPS-207 | feature_flag | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the feature flag |
| DF-OPS-208 | feature_flag | flag_key | TEXT | varchar(80) | 80 | Yes | None | None | UK | None | Workbench | None | No | Flag key rwb.<module>.<short-name> |
| DF-OPS-209 | feature_flag | description | TEXT | varchar(400) | 400 | Yes | None | None | None | None | Workbench | None | No | What the flag switches |
| DF-OPS-210 | feature_flag | owner_user_id | USER_REF | uuid |  | Yes | None | None | None | None | Workbench | None | No | Owner of the flag |
| DF-OPS-211 | feature_flag | owner_team | TEXT | varchar(60) | 60 | No | None | None | None | None | Workbench | None | No | Owning squad |
| DF-OPS-212 | feature_flag | default_on | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | Default value |
| DF-OPS-213 | feature_flag | dev_on | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | Value in DEV |
| DF-OPS-214 | feature_flag | sit_on | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | Value in SIT |
| DF-OPS-215 | feature_flag | uat_on | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | Value in UAT |
| DF-OPS-216 | feature_flag | prod_on | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | Value in PROD |
| DF-OPS-217 | feature_flag | removal_date | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date by which the flag and its old path are removed |
| DF-OPS-218 | feature_flag_change | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the feature flag change |
| DF-OPS-219 | feature_flag_change | flag_key | TEXT | varchar(80) | 80 | Yes | None | None | None | None | Workbench | None | No | Flag changed |
| DF-OPS-220 | feature_flag_change | environment | LOV | varchar(4) | 4 | Yes | None | LOV-ENVIRONMENT | None | None | Workbench | None | No | DEV, SIT, UAT or PROD |
| DF-OPS-221 | feature_flag_change | old_value | BOOLEAN | boolean |  | Yes | None | None | None | None | Workbench | None | No | Value before |
| DF-OPS-222 | feature_flag_change | new_value | BOOLEAN | boolean |  | Yes | None | None | None | None | Workbench | None | No | Value after |
| DF-OPS-223 | feature_flag_change | reason | TEXT | varchar(400) | 400 | Yes | None | None | None | None | Workbench | None | No | Reason for the change |
| DF-OPS-224 | job_catalog | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the job |
| DF-OPS-225 | job_catalog | job_id | TEXT | varchar(6) | 6 | Yes | None | None | UK | None | Workbench | None | No | Job ID JOB-nn |
| DF-OPS-226 | job_catalog | job_name | TEXT | varchar(80) | 80 | Yes | None | None | None | None | Workbench | None | No | Job name from the batch schedule |
| DF-OPS-227 | job_catalog | owner_role | LOV | varchar(20) | 20 | Yes | None | LOV-ROLE | None | None | Workbench | None | No | Role that owns failures |
| DF-OPS-228 | job_catalog | schedule_text | TEXT | varchar(120) | 120 | Yes | None | None | None | None | Workbench | None | No | Schedule as in the batch schedule |
| DF-OPS-229 | job_catalog | runbook_path | TEXT | varchar(200) | 200 | No | None | None | None | None | Workbench | None | No | Path of the run book in the repository |
| DF-OPS-230 | job_catalog | expected_minutes | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Expected duration in minutes |
| DF-OPS-231 | job_catalog | alert_after_minutes | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Duration after which the owner is alerted |
| DF-OPS-232 | job_catalog | first_release | TEXT | varchar(3) | 3 | No | None | None | None | None | Workbench | None | No | Epic of first release, for example E1 |
| DF-PTY-022 | party_product | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the party product |
| DF-PTY-023 | party_product | party_id | CROSS_REF | uuid |  | Yes | None | None | FK | party | Workbench | None | No | The party that holds the product |
| DF-PTY-024 | party_product | product_type | TEXT | varchar(20) | 20 | Yes | None | None | None | None | SCBPDM via COLLINS | None | No | Product type from the customer profile |
| DF-PTY-025 | party_product | account_no | TEXT | varchar(20) | 20 | Yes | None | None | None | None | SCBPDM via COLLINS | None | No | Account number of the product, masked by role |
| DF-PTY-026 | party_product | product_status | LOV | varchar(15) | 15 | Yes | None | LOV-PRODUCT-STATUS | None | None | SCBPDM via COLLINS | None | No | Active, delinquent, closed or written off |
| DF-PTY-027 | party_product | data_as_of | DATE | date |  | Yes | None | None | None | None | SCBPDM via COLLINS | None | No | Business date of the customer profile load |
| DF-REF-128 | efs_ledger_outcome | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the EFS ledger outcome row |
| DF-REF-129 | efs_ledger_outcome | action_code | LOV | varchar(10) | 10 | Yes | None | LOV-ACTION-CODE | UK | None | Workbench | None | No | EFS action code named for the ledger |
| DF-REF-130 | efs_ledger_outcome | channel | LOV | varchar(15) | 15 | Yes | CALL | LOV-CHANNEL | None | None | Workbench | None | No | Ledger channel for the action code |
| DF-REF-131 | efs_ledger_outcome | in_ledger | BOOLEAN | boolean |  | Yes | true | None | None | None | Workbench | None | No | True when rows with this action code enter the ledger |
| DF-CAS-056 | case_entry_exclusion | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the case entry exclusion |
| DF-CAS-057 | case_entry_exclusion | account_id | CROSS_REF | uuid |  | Yes | None | None | FK | loan_account | Workbench | None | No | The account excluded; unique with business_date |
| DF-CAS-058 | case_entry_exclusion | business_date | DATE | date |  | Yes | None | None | UK | None | Workbench | None | No | Business date of the exclusion |
| DF-CAS-059 | case_entry_exclusion | reason_code | LOV | varchar(20) | 20 | Yes | None | LOV-EXCLUSION-REASON | None | None | Workbench | None | No | Deceased, fraud, bankruptcy, active plan or open dispute |
| DF-CAS-060 | case_entry_exclusion | rule_id | TEXT | varchar(20) | 20 | Yes | None | None | None | None | Workbench | None | No | Exclusion rule that blocked the entry |
| DF-CAS-061 | case_entry_exclusion | rule_version | TEXT | varchar(20) | 20 | Yes | None | None | None | None | Workbench | None | No | Version of that rule |
| DF-WRK-045 | queue_member | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the queue member |
| DF-WRK-046 | queue_member | queue_id | CROSS_REF | uuid |  | Yes | None | None | FK | queue | Workbench | None | No | The queue |
| DF-WRK-047 | queue_member | user_id | USER_REF | uuid |  | Yes | None | None | None | None | Workbench | None | No | The person |
| DF-WRK-048 | queue_member | capacity | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Most open cases the person may hold in the queue |
| DF-WRK-049 | queue_member | skill_codes | TEXT | varchar(200) | 200 | No | None | None | None | None | Workbench | None | No | Skills of the person, comma separated |
| DF-WRK-050 | queue_member | table_version | NUMBER | integer |  | Yes | None | None | None | None | Workbench | None | No | QUEUE_MEMBER reference version the row belongs to |
| DF-WRK-051 | queue_member | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the row comes into force |
| DF-WRK-052 | queue_member | valid_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Last date the row is in force |
| DF-RPT-020 | queue_measure | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the queue measure |
| DF-RPT-021 | queue_measure | queue_id | CROSS_REF | uuid |  | Yes | None | None | FK | queue | Workbench | None | No | The queue measured; unique with as_of |
| DF-RPT-022 | queue_measure | as_of | DATE | timestamptz |  | Yes | None | None | UK | None | Workbench | None | No | When the snapshot was taken |
| DF-RPT-023 | queue_measure | depth | NUMBER | integer |  | Yes | None | None | None | None | Workbench | None | No | Open cases in the queue |
| DF-RPT-024 | queue_measure | unassigned | NUMBER | integer |  | Yes | None | None | None | None | Workbench | None | No | Open cases with no owner |
| DF-RPT-025 | queue_measure | avg_age_days | NUMBER | numeric(7,2) | 7,2 | No | None | None | None | None | Workbench | None | No | Average age of the open cases, days |
| DF-RPT-026 | queue_measure | max_age_days | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Age of the oldest open case, days |
| DF-RPT-027 | queue_measure | owner_min | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Fewest open cases held by one owner |
| DF-RPT-028 | queue_measure | owner_max | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Most open cases held by one owner |
| DF-RPT-029 | queue_measure | breached | NUMBER | integer |  | Yes | None | None | None | None | Workbench | None | No | Open cases past their service level |
| DF-RPT-030 | queue_measure | status | LOV | varchar(15) | 15 | Yes | TAKEN | LOV-SNAPSHOT-STATUS | None | None | Workbench | None | No | Taken, published or held |
| DF-REF-132 | parameter_catalog | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the parameter definition |
| DF-REF-133 | parameter_catalog | param_key | TEXT | varchar(100) | 100 | Yes | None | None | UK | None | Workbench | None | No | Parameter key, for example case.entry.dpd |
| DF-REF-134 | parameter_catalog | kind | TEXT | varchar(15) | 15 | Yes | None | None | None | None | Workbench | None | No | Kind of parameter, for example ENVIRONMENT for an environment setting |
| DF-REF-135 | parameter_catalog | value_type | TEXT | varchar(15) | 15 | Yes | None | None | None | None | Workbench | None | No | Type of the value |
| DF-REF-136 | parameter_catalog | unit | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | Unit, for example CALENDAR_DAYS, WORKING_DAYS, BAHT, PERCENT, COUNT, CODE_LIST |
| DF-REF-137 | parameter_catalog | min_value | TEXT | varchar(40) | 40 | No | None | None | None | None | Workbench | None | No | Lowest allowed value |
| DF-REF-138 | parameter_catalog | max_value | TEXT | varchar(40) | 40 | No | None | None | None | None | Workbench | None | No | Highest allowed value |
| DF-REF-139 | parameter_catalog | default_value | TEXT | varchar(400) | 400 | No | None | None | None | None | Workbench | None | No | Default value |
| DF-REF-140 | parameter_catalog | scope | LOV | varchar(10) | 10 | Yes | GLOBAL | LOV-PARAM-SCOPE | None | None | Workbench | None | No | Product, when the parameter is keyed by product group, or global |
| DF-REF-141 | parameter_catalog | required | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True when every product in force must have a row |
| DF-REF-142 | parameter_catalog | owner_role | LOV | varchar(20) | 20 | Yes | None | LOV-ROLE | None | None | Workbench | None | No | Role that owns the parameter |
| DF-REF-143 | parameter_catalog | environments | TEXT | varchar(40) | 40 | No | None | None | None | None | Workbench | None | No | Environments the parameter is set in |
| DF-REF-144 | parameter_catalog | used_by | TEXT | varchar(400) | 400 | No | None | None | None | None | Workbench | None | No | Modules and stories that read the parameter |
| DF-REF-145 | parameter_catalog | secret | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True for a secret; its value is never returned |
| DF-REF-146 | parameter_catalog | description | TEXT | varchar(400) | 400 | Yes | None | None | None | None | Workbench | None | No | What the parameter controls |
| DF-REF-147 | parameter_value | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the parameter value |
| DF-REF-148 | parameter_value | param_key | TEXT | varchar(100) | 100 | Yes | None | None | UK | None | Workbench | None | No | Parameter, from parameter_catalog |
| DF-REF-149 | parameter_value | environment | LOV | varchar(4) | 4 | Yes | None | LOV-ENVIRONMENT | UK | None | Workbench | None | No | DEV, SIT, UAT or PROD |
| DF-REF-150 | parameter_value | param_value | TEXT | varchar(400) | 400 | Yes | None | None | None | None | Workbench | None | No | Value as text |
| DF-REF-151 | parameter_value | product_group | LOV | varchar(15) | 15 | No | None | LOV-PRODUCT | UK | None | Workbench | None | No | Product group for a product-scoped parameter |
| DF-REF-152 | parameter_value | version_no | NUMBER | integer |  | Yes | None | None | UK | None | Workbench | None | No | Version number |
| DF-REF-153 | parameter_value | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the value comes into force |
| DF-REF-154 | parameter_value | valid_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Last date the value is in force |
| DF-REF-155 | parameter_value | status | LOV | varchar(15) | 15 | Yes | VALIDATED | LOV-VERSION-STATUS | None | None | Workbench | None | No | Validated, approved, in force, superseded, rolled back or refused |
| DF-REF-156 | parameter_value | author_user_id | USER_REF | uuid |  | Yes | None | None | None | None | Workbench | None | No | Who loaded the value |
| DF-REF-157 | parameter_value | approver_user_id | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Who approved the value; never the author |
| DF-REF-158 | parameter_value | approved_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the value was approved |
| DF-REF-159 | reference_version | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the reference version |
| DF-REF-160 | reference_version | table_code | LOV | varchar(30) | 30 | Yes | None | LOV-REF-TABLE | UK | None | Workbench | None | No | The reference or rule table the version belongs to, for example EXPOSURE_BAND or ALLOCATION |
| DF-REF-161 | reference_version | version_no | NUMBER | integer |  | Yes | None | None | UK | None | Workbench | None | No | Version number, one above the previous version of the table |
| DF-REF-162 | reference_version | version_label | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | Version label the rows carry, for example DOCTYPE-2026.11 |
| DF-REF-163 | reference_version | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the version comes into force |
| DF-REF-164 | reference_version | valid_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Last date the version is in force; set when the next version is approved |
| DF-REF-165 | reference_version | status | LOV | varchar(15) | 15 | Yes | VALIDATED | LOV-VERSION-STATUS | None | None | Workbench | None | No | Validated, approved, in force, superseded, rolled back or refused |
| DF-REF-166 | reference_version | author_user_id | USER_REF | uuid |  | Yes | None | None | None | None | Workbench | None | No | Who loaded the version |
| DF-REF-167 | reference_version | approver_user_id | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Who approved the version; never the author |
| DF-REF-168 | reference_version | approved_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the version was approved |
| DF-REF-169 | reference_version | row_count | NUMBER | integer |  | Yes | None | None | None | None | Workbench | None | No | Rows in the version |
| DF-REF-170 | reference_version | content_hash | TEXT | char(64) | 64 | Yes | None | None | None | None | Workbench | None | No | SHA-256 of the rows sorted by key; used for idempotency |
| DF-REF-171 | reference_version | load_id | TEXT | uuid |  | Yes | None | None | None | None | Workbench | None | No | Identifier of the reference load request that created the version |
| DF-REF-172 | reference_version | dry_run_counts | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Counts of live cases each changed rule row would move, from the dry run |
| DF-REF-173 | reference_version | rollback_reason | TEXT | varchar(400) | 400 | No | None | None | None | None | Workbench | None | No | Reason given for a rollback |
| DF-REF-174 | reference_version | change_request_ref | TEXT | varchar(30) | 30 | No | None | None | None | None | Workbench | None | No | Reference of the change request in the bank's request tool |
| DF-REF-175 | reference_version | impact_summary | TEXT | varchar(1000) | 1000 | No | None | None | None | None | Workbench | None | No | What the change affects, for example the open cases it touches |
| DF-REF-176 | reference_version | test_result | LOV | varchar(10) | 10 | No | None | LOV-TEST-RESULT | None | None | Workbench | None | No | Passed or failed, from the load checks or the rule table test harness |
| DF-REF-177 | reference_version | rollback_plan | TEXT | varchar(1000) | 1000 | No | None | None | None | None | Workbench | None | No | How to return to the previous version |
| DF-REF-178 | reference_version | verified_by | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Who verified the change after it took effect |
| DF-REF-179 | reference_version | verified_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the change was verified |
| DF-REF-180 | reference_version | verify_note | TEXT | varchar(1000) | 1000 | No | None | None | None | None | Workbench | None | No | What was checked |
| DF-REF-181 | reference_row | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the reference row |
| DF-REF-182 | reference_row | version_id | CROSS_REF | uuid |  | Yes | None | None | FK | reference_version | Workbench | None | No | The reference version the row belongs to; unique with row_key |
| DF-REF-183 | reference_row | row_key | TEXT | varchar(200) | 200 | Yes | None | None | UK | None | Workbench | None | No | Key of the row inside its table |
| DF-REF-184 | reference_row | row_data | TEXT | jsonb |  | Yes | None | None | None | None | Workbench | None | No | Column values of the row |
| DF-REF-185 | rule_test_case | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the rule test case |
| DF-REF-186 | rule_test_case | test_case_id | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | The test case named by rule_row.test_case_id |
| DF-REF-187 | rule_test_case | route_set | LOV | varchar(15) | 15 | Yes | None | LOV-ROUTE-SET | None | None | Workbench | None | No | Route set |
| DF-REF-188 | rule_test_case | rule_version | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Rule version tested |
| DF-REF-189 | rule_test_case | rule_id | TEXT | varchar(20) | 20 | Yes | None | None | None | None | Workbench | None | No | Rule the test expects to hit |
| DF-REF-190 | rule_test_case | from_state | TEXT | varchar(60) | 60 | Yes | None | None | None | None | Workbench | None | No | Input state |
| DF-REF-191 | rule_test_case | event_code | TEXT | varchar(60) | 60 | Yes | None | None | None | None | Workbench | None | No | Input event |
| DF-REF-192 | rule_test_case | facts | TEXT | jsonb |  | Yes | None | None | None | None | Workbench | None | No | Synthetic case file facts the condition reads |
| DF-REF-193 | rule_test_case | expected_to_state | TEXT | varchar(60) | 60 | Yes | None | None | None | None | Workbench | None | No | Expected to state |
| DF-REF-194 | rule_test_case | expected_owner_role | LOV | varchar(20) | 20 | No | None | LOV-ROLE | None | None | Workbench | None | No | Expected owner role |
| DF-REF-195 | rule_test_case | expected_timer_spec | TEXT | varchar(60) | 60 | No | None | None | None | None | Workbench | None | No | Expected timer |
| DF-REF-196 | rule_test_case | result | LOV | varchar(10) | 10 | No | None | LOV-TEST-RESULT | None | None | Workbench | None | No | Passed or failed |
| DF-REF-197 | rule_test_case | result_detail | TEXT | varchar(1000) | 1000 | No | None | None | None | None | Workbench | None | No | Expected against actual, and the rows that hit |
| DF-REF-198 | masking_rule | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the masking rule |
| DF-REF-199 | masking_rule | role_code | LOV | varchar(20) | 20 | Yes | None | LOV-ROLE | UK | None | Workbench | None | No | Role the rule applies to |
| DF-REF-200 | masking_rule | field_id | TEXT | varchar(16) | 16 | Yes | None | None | UK | None | Workbench | None | No | BR Field ID of a personal data field (sys_fields.is_personal true) |
| DF-REF-201 | masking_rule | unmasked | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True when the role sees the field unmasked; no row means masked |
| DF-REF-202 | masking_rule | masking_version | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Version of the masking rules, for example MASK-2026.11 |
| DF-REF-203 | masking_rule | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the version comes into force |
| DF-REF-204 | masking_rule | valid_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Last date the version is in force |
| DF-REF-205 | role_conflict | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the role conflict |
| DF-REF-206 | role_conflict | role_code | LOV | varchar(20) | 20 | Yes | None | LOV-ROLE | UK | None | Workbench | None | No | Role that may not be held with the other |
| DF-REF-207 | role_conflict | conflicts_with | TEXT | varchar(30) | 30 | Yes | None | None | UK | None | Workbench | None | No | Role code, or ANY_BUSINESS_ROLE or ANY_OTHER_ROLE, per the Separation of duty sheet |
| DF-REF-208 | role_conflict | reason | TEXT | varchar(200) | 200 | Yes | None | None | None | None | Workbench | None | No | Why the pair is not allowed |
| DF-REF-209 | role_conflict | conflict_version | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Version of the conflict table, for example SOD-2026.11 |
| DF-REF-210 | role_conflict | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the version comes into force |
| DF-REF-211 | role_conflict | valid_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Last date the version is in force |
| DF-REF-212 | partner_user | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the partner user |
| DF-REF-213 | partner_user | identity_ref | TEXT | varchar(64) | 64 | Yes | None | None | UK | None | Workbench | None | No | Partner identity directory ID |
| DF-REF-214 | partner_user | partner_id | CROSS_REF | uuid |  | Yes | None | None | FK | partner | Workbench | None | No | The firm the partner user works for |
| DF-REF-215 | partner_user | role_code | LOV | varchar(20) | 20 | Yes | None | LOV-ROLE | None | None | Workbench | None | No | The one partner role held, for example PT-LAWFIRM |
| DF-REF-216 | partner_user | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the binding starts |
| DF-REF-217 | partner_user | valid_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Date the binding ends; no later than the firm's contract end |
| DF-REF-218 | document_type | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the document type |
| DF-REF-219 | document_type | doc_type_code | TEXT | varchar(30) | 30 | Yes | None | None | UK | None | Workbench | None | No | Document type code, the value set of LOV-DOC-TYPE |
| DF-REF-220 | document_type | label_en | TEXT | varchar(120) | 120 | Yes | None | None | None | None | Workbench | None | No | English label |
| DF-REF-221 | document_type | label_th | TEXT | varchar(120) | 120 | No | None | None | None | None | Workbench | None | No | Thai label |
| DF-REF-222 | document_type | write_once | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True for a legal type held in the write-once container |
| DF-REF-223 | document_type | retention_class | LOV | varchar(10) | 10 | Yes | None | LOV-RETENTION | None | None | Workbench | None | No | Retention class of the type |
| DF-REF-224 | document_type | field_definitions | TEXT | jsonb |  | Yes | None | None | None | None | Workbench | None | No | Fields extracted from the type: name, label, data type, personal flag, required flag, extraction method (TEMPLATE or MODEL), review only flag and optional pattern |
| DF-REF-225 | document_type | legal_signoff_by | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Legal counsel user who signed the type and its fields |
| DF-REF-226 | document_type | legal_signoff_date | DATE | date |  | No | None | None | None | None | Workbench | None | No | Date of the Legal sign-off |
| DF-REF-227 | document_type | npa_signoff_by | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Head of NPA user who signed the type and its fields |
| DF-REF-228 | document_type | npa_signoff_date | DATE | date |  | No | None | None | None | None | Workbench | None | No | Date of the NPA sign-off |
| DF-REF-229 | document_type | table_version | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Version of the type table, for example DOCTYPE-2026.11 |
| DF-REF-230 | document_type | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the version comes into force |
| DF-REF-231 | document_type | valid_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Last date the version is in force |
| DF-REF-232 | document_type | reference_version_id | CROSS_REF | uuid |  | No | None | None | FK | reference_version | Workbench | None | No | Reference version that brought the row |
| DF-REF-233 | document_type | classify_threshold | NUMBER | numeric(4,3) | 4,3 | No | None | None | None | None | Workbench | None | No | Confidence below which a document of this type goes to the review queue |
| DF-REF-234 | document_checklist_item | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the checklist item |
| DF-REF-235 | document_checklist_item | stage_code | LOV | varchar(20) | 20 | Yes | None | LOV-STAGE | UK | None | Workbench | None | No | Case stage the row applies to |
| DF-REF-236 | document_checklist_item | route_code | LOV | varchar(4) | 4 | No | None | LOV-ROUTE | UK | None | Workbench | None | No | Route the row applies to; empty for every route |
| DF-REF-237 | document_checklist_item | document_type | LOV | varchar(30) | 30 | Yes | None | LOV-DOC-TYPE | UK | None | Workbench | None | No | Document type |
| DF-REF-238 | document_checklist_item | required | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True when the type is required for the stage and route |
| DF-REF-239 | document_checklist_item | sort_order | NUMBER | integer |  | Yes | 0 | None | None | None | Workbench | None | No | Order of the item on the checklist |
| DF-REF-240 | document_checklist_item | table_version | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Version of the checklist, for example CHK-2026.11 |
| DF-REF-241 | document_checklist_item | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the version comes into force |
| DF-REF-242 | document_checklist_item | valid_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Last date the version is in force |
| DF-REF-243 | document_checklist_item | reference_version_id | CROSS_REF | uuid |  | No | None | None | FK | reference_version | Workbench | None | No | Reference version that brought the row |
| DF-DOC-036 | case_document_check | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the completeness check |
| DF-DOC-037 | case_document_check | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | None | No | Case checked; one row per case; unique |
| DF-DOC-038 | case_document_check | checklist_version | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | Checklist version used |
| DF-DOC-039 | case_document_check | required_count | NUMBER | integer |  | Yes | 0 | None | None | None | Workbench | None | No | Number of required types |
| DF-DOC-040 | case_document_check | present_count | NUMBER | integer |  | Yes | 0 | None | None | None | Workbench | None | No | Number of required types present |
| DF-DOC-041 | case_document_check | missing_types | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Required types not present |
| DF-DOC-042 | case_document_check | complete | BOOLEAN | boolean |  | No | None | None | None | None | Workbench | None | No | True when every required type is present; empty when the stage has no checklist |
| DF-DOC-043 | case_document_check | checked_at | DATE | timestamptz |  | Yes | None | None | None | None | Workbench | None | No | When the check last ran |
| DF-DOC-044 | case_document_check | last_event_id | CROSS_REF | uuid |  | No | None | None | FK | outbox_event | Workbench | None | No | Event that triggered the last check, for repeat detection |
| DF-REF-244 | document_hub_parameter | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the document hub parameter |
| DF-REF-245 | document_hub_parameter | param_code | TEXT | varchar(40) | 40 | Yes | None | None | UK | None | Workbench | None | No | Parameter code, for example INTAKE_MAX_FILE_MB, OCR_MIN_QUALITY, CLASSIFY_THRESHOLD, CASE_NO_PATTERN, SEARCH_MAX_RESULTS |
| DF-REF-246 | document_hub_parameter | param_value | TEXT | varchar(200) | 200 | Yes | None | None | None | None | Workbench | None | No | Parameter value as text, typed by the reader |
| DF-REF-247 | document_hub_parameter | unit | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | Unit of the value, for example MB, seconds, ratio |
| DF-REF-248 | document_hub_parameter | table_version | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Version of the parameter load |
| DF-REF-249 | document_hub_parameter | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the value comes into force |
| DF-REF-250 | document_hub_parameter | valid_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Last date the value is in force |
| DF-REF-251 | document_hub_parameter | reference_version_id | CROSS_REF | uuid |  | No | None | None | FK | reference_version | Workbench | None | No | Reference version that brought the row |
| DF-DOC-045 | document_intake | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the intake item |
| DF-DOC-046 | document_intake | source | LOV | varchar(12) | 12 | Yes | None | LOV-DOC-SOURCE | None | None | Workbench | None | No | Source of the file |
| DF-DOC-047 | document_intake | source_ref | TEXT | varchar(400) | 400 | Yes | None | None | None | None | Workbench | None | No | Path, partner reference or email message ID at the channel |
| DF-DOC-048 | document_intake | channel_code | TEXT | varchar(40) | 40 | No | None | None | None | None | Workbench | None | No | Branch code, MAILROOM, partner code or mailbox code |
| DF-DOC-049 | document_intake | file_name | TEXT | varchar(255) | 255 | No | None | None | None | None | Workbench | None | Yes | File name as received; personal where it names a customer |
| DF-DOC-050 | document_intake | file_size | NUMBER | bigint |  | No | None | None | None | None | Workbench | None | No | File size in bytes |
| DF-DOC-051 | document_intake | captured_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | Scan time recorded by the scanner, for scanner files |
| DF-DOC-052 | document_intake | sender_address | TEXT | varchar(320) | 320 | No | None | None | None | None | Workbench | None | Yes | Sender email address for mailbox items; masked by role |
| DF-DOC-053 | document_intake | partner_id | CROSS_REF | uuid |  | No | None | None | FK | partner | Workbench | None | No | Partner that sent the file by SFTP |
| DF-DOC-054 | document_intake | run_id | CROSS_REF | uuid |  | No | None | None | FK | load_run | Workbench | None | No | JOB-12 run that took the item in |
| DF-DOC-055 | document_intake | received_at | DATE | timestamptz |  | Yes | None | None | None | None | Workbench | None | No | When the Workbench received the file |
| DF-DOC-056 | document_intake | file_sha256 | TEXT | char(64) | 64 | Yes | None | None | None | None | Workbench | None | No | SHA-256 of the file |
| DF-DOC-057 | document_intake | intake_ref | ATTACHMENT | varchar(400) | 400 | Yes | None | None | None | None | Workbench | None | No | Received file in the intake container |
| DF-DOC-058 | document_intake | scan_result | LOV | varchar(10) | 10 | No | None | LOV-SCAN-RESULT | None | None | Workbench | None | No | Malware scan result: clean or infected; empty until scanned |
| DF-DOC-059 | document_intake | scanned_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the malware scan ran |
| DF-DOC-060 | document_intake | case_id | CROSS_REF | uuid |  | No | None | None | FK | recovery_case | Workbench | None | No | Case the item belongs to once known |
| DF-DOC-061 | document_intake | document_id | CROSS_REF | uuid |  | No | None | None | FK | document | Workbench | None | No | Document created from the item, or the uploaded document |
| DF-DOC-062 | document_intake | ocr_ref | ATTACHMENT | varchar(400) | 400 | No | None | None | None | None | Workbench | None | No | OCR JSON output (text and layout) in the standard container |
| DF-DOC-063 | document_intake | ocr_status | LOV | varchar(12) | 12 | Yes | PENDING | LOV-OCR-STATUS | None | None | Workbench | None | No | Pending, done, rescan or failed |
| DF-DOC-064 | document_intake | ocr_attempts | NUMBER | integer |  | Yes | 0 | None | None | None | Workbench | None | No | Number of OCR calls made for the item |
| DF-DOC-065 | document_intake | page_count | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Number of pages read |
| DF-DOC-066 | document_intake | rescan_pages | TEXT | varchar(200) | 200 | No | None | None | None | None | Workbench | None | No | Page numbers below the OCR quality threshold |
| DF-DOC-067 | document_intake | ocr_quality | NUMBER | numeric(5,4) | 5,4 | No | None | None | None | None | Workbench | None | No | Lowest page quality of the item |
| DF-DOC-068 | document_intake | languages | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | Languages found, for example th,en |
| DF-DOC-069 | document_intake | ocr_engine_version | TEXT | varchar(40) | 40 | No | None | None | None | None | Workbench | None | No | Version of the OCR service that read the item |
| DF-DOC-070 | document_intake | predicted_type | LOV | varchar(30) | 30 | No | None | LOV-DOC-TYPE | None | None | Workbench | None | No | Type with the highest classification score |
| DF-DOC-071 | document_intake | classification_confidence | NUMBER | numeric(5,4) | 5,4 | No | None | None | None | None | Workbench | None | No | Score of the predicted type |
| DF-DOC-072 | document_intake | type_candidates | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Top two types with their scores |
| DF-DOC-073 | document_intake | classifier_version | TEXT | varchar(40) | 40 | No | None | None | None | None | Workbench | None | No | Model version that classified the item |
| DF-DOC-074 | document_intake | classify_fallback | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True when the classifier did not answer and the item went to a person |
| DF-DOC-075 | document_intake | match_status | LOV | varchar(12) | 12 | Yes | PENDING | LOV-INTAKE-MATCH | None | None | Workbench | None | No | Pending, matched, no match, multiple, conflict, case closed or no type |
| DF-DOC-076 | document_intake | candidate_case_ids | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Cases found for the item when more than one or none can be chosen by rule |
| DF-DOC-077 | document_intake | extracted_fields | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | Yes | Fields read before the item is attached: field name, value, extracted value, confidence, state, extractor version, personal flag |
| DF-DOC-078 | document_intake | extract_status | LOV | varchar(12) | 12 | No | None | LOV-EXTRACT-STATUS | None | None | Workbench | None | No | Pending, done or failed |
| DF-DOC-079 | document_intake | extract_attempts | NUMBER | integer |  | Yes | 0 | None | None | None | Workbench | None | No | Number of extraction attempts |
| DF-DOC-080 | document_intake | review_reason | LOV | varchar(20) | 20 | No | None | LOV-INTAKE-REVIEW | None | None | Workbench | None | No | Why the item needs a person: rescan, unreadable file, low confidence, model unavailable, unknown type |
| DF-DOC-081 | document_intake | review_outcome | LOV | varchar(12) | 12 | No | None | LOV-INTAKE-OUTCOME | None | None | Workbench | None | No | Attached or discarded once a person resolves the review item |
| DF-DOC-082 | document_intake | resolved_by | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Who resolved the review item |
| DF-DOC-083 | document_intake | resolved_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the review item was resolved |
| DF-DOC-084 | document_intake | discard_reason | TEXT | varchar(400) | 400 | No | None | None | None | None | Workbench | None | No | Reason given when a review item is discarded |
| DF-DOC-085 | document_text | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the page text |
| DF-DOC-086 | document_text | intake_id | CROSS_REF | uuid |  | Yes | None | None | FK | document_intake | Workbench | None | No | Intake item the page belongs to; unique with page_no |
| DF-DOC-087 | document_text | document_id | CROSS_REF | uuid |  | No | None | None | FK | document | Workbench | None | No | Document the page belongs to once attached |
| DF-DOC-088 | document_text | page_no | NUMBER | integer |  | Yes | None | None | UK | None | Workbench | None | No | Page number |
| DF-DOC-089 | document_text | text_content | TEXT | text |  | Yes | None | None | None | None | Workbench | None | Yes | OCR text of the page; masked by role on read |
| DF-DOC-090 | document_text | quality | NUMBER | numeric(5,4) | 5,4 | No | None | None | None | None | Workbench | None | No | Mean word confidence of the page |
| DF-DOC-091 | retention_action | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the retention action |
| DF-DOC-092 | retention_action | document_id | CROSS_REF | uuid |  | Yes | None | None | FK | document | Workbench | None | No | Document acted on; unique with run_month |
| DF-DOC-093 | retention_action | run_month | TEXT | char(7) | 7 | Yes | None | None | UK | None | Workbench | None | No | Month of the JOB-17 run, YYYY-MM |
| DF-DOC-094 | retention_action | action | LOV | varchar(12) | 12 | Yes | None | LOV-RETENTION-ACTION | None | None | Workbench | None | No | Archived, listed, held or exception |
| DF-DOC-095 | retention_action | decision_log_id | CROSS_REF | uuid |  | No | None | None | FK | decision_log_entry | Workbench | None | No | DOCRET decision log entry for an archive |
| DF-REF-252 | merge_field | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the merge field |
| DF-REF-253 | merge_field | merge_code | TEXT | varchar(40) | 40 | Yes | None | None | UK | None | Workbench | None | No | Code written in the template body, for example CASE_NO |
| DF-REF-254 | merge_field | source_entity | TEXT | varchar(60) | 60 | Yes | None | None | None | None | Workbench | None | No | Entity that holds the value |
| DF-REF-255 | merge_field | source_field | TEXT | varchar(60) | 60 | Yes | None | None | None | None | Workbench | None | No | Field that holds the value |
| DF-REF-256 | merge_field | field_id | TEXT | varchar(16) | 16 | Yes | None | None | None | None | Workbench | None | No | BR Field ID of the source field in the data dictionary |
| DF-REF-257 | merge_field | is_required | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True when generation holds on an empty value |
| DF-REF-258 | merge_field | personal_data | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True when the value is personal data, detokenized only at generation |
| DF-REF-259 | merge_field | catalog_version | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Version of the catalog load |
| DF-REF-260 | merge_field | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the catalog version comes into force |
| DF-DOC-096 | signature_request | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the signature request |
| DF-DOC-097 | signature_request | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | None | No | Case |
| DF-DOC-098 | signature_request | treatment_id | CROSS_REF | uuid |  | No | None | None | FK | treatment | Workbench | None | No | Treatment the agreement belongs to |
| DF-DOC-099 | signature_request | document_id | CROSS_REF | uuid |  | Yes | None | None | FK | document | Workbench | None | No | Generated document sent for signature |
| DF-DOC-100 | signature_request | party_id | CROSS_REF | uuid |  | Yes | None | None | FK | party | Workbench | None | No | Signing party |
| DF-DOC-101 | signature_request | method | LOV | varchar(15) | 15 | Yes | None | LOV-SIGN-METHOD | None | None | Workbench | None | No | E-signature, branch or paper |
| DF-DOC-102 | signature_request | status | LOV | varchar(15) | 15 | Yes | QUEUED | LOV-SIGN-STATUS | None | None | Workbench | None | No | Queued, sent, signed, declined or expired |
| DF-DOC-103 | signature_request | external_ref | TEXT | varchar(60) | 60 | No | None | None | None | None | EasyApp | None | No | EasyApp reference |
| DF-DOC-104 | signature_request | sent_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the request was sent |
| DF-DOC-105 | signature_request | signed_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the party signed |
| DF-DOC-106 | signature_request | signed_document_id | CROSS_REF | uuid |  | No | None | None | FK | document | Workbench | None | No | Signed copy or branch scan |
| DF-DOC-107 | signature_request | expires_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | End of the offer validity |
| DF-DEC-032 | approval | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the approval |
| DF-DEC-033 | approval | case_id | CROSS_REF | uuid |  | Yes | None | None | FK | recovery_case | Workbench | None | No | The case |
| DF-DEC-034 | approval | decision_code | LOV | varchar(8) | 8 | Yes | None | LOV-DECISION | None | None | Workbench | None | No | Decision to approve |
| DF-DEC-035 | approval | regulation_item | TEXT | varchar(10) | 10 | No | None | None | None | None | Workbench | None | No | Delegation item, for example 2.1.1 |
| DF-DEC-036 | approval | capability_area | LOV | varchar(30) | 30 | Yes | None | LOV-CAPABILITY | None | None | Workbench | None | No | Area whose A letter the approver needs |
| DF-DEC-037 | approval | route_role_code | LOV | varchar(20) | 20 | No | None | LOV-ROLE | None | None | Workbench | None | No | Role for a decision with no amount limit, for example RW-LITOFF |
| DF-DEC-038 | approval | approval_level | LOV | varchar(4) | 4 | No | None | LOV-APPROVAL-LEVEL | None | None | Workbench | None | No | Required level L1 to L6 |
| DF-DEC-039 | approval | delegation_limit_id | CROSS_REF | uuid |  | No | None | None | FK | delegation_limit | Workbench | None | No | Delegation row that covers the item |
| DF-DEC-040 | approval | limit_version | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | Delegation version the item routed under |
| DF-DEC-041 | approval | product_group | LOV | varchar(15) | 15 | Yes | None | LOV-PRODUCT | None | None | Workbench | None | No | Product group |
| DF-DEC-042 | approval | amount | NUMBER | numeric(18,2) | 18,2 | No | None | None | None | None | Workbench | None | No | Principal used for the limit, baht |
| DF-DEC-043 | approval | terms | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Proposed and changed terms |
| DF-DEC-044 | approval | prepared_by | USER_REF | uuid |  | Yes | None | None | None | None | Workbench | None | No | Person or service identity that prepared the item |
| DF-DEC-045 | approval | assigned_user_id | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Holder the item is assigned to; empty for a role route |
| DF-DEC-046 | approval | status | LOV | varchar(20) | 20 | Yes | WAITING | LOV-APPROVAL-STATUS | None | None | Workbench | None | No | Waiting, held with no limit, approved, refused or returned |
| DF-DEC-047 | approval | due_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the service level ends |
| DF-DEC-048 | approval | escalation_level | NUMBER | integer |  | Yes | 0 | None | None | None | Workbench | None | No | Times escalated |
| DF-DEC-049 | approval | source_type | TEXT | varchar(20) | 20 | Yes | None | None | None | None | Workbench | None | No | What asked for approval, for example NOTICE or TREATMENT |
| DF-DEC-050 | approval | source_ref | TEXT | varchar(60) | 60 | Yes | None | None | None | None | Workbench | None | No | ID of the source record, for example the notice ID |
| DF-DEC-051 | approval | rule_id | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | Rule that asked for approval |
| DF-DEC-052 | approval | rule_version | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | Version of that rule |
| DF-DEC-053 | approval | decision_log_id | CROSS_REF | uuid |  | No | None | None | FK | decision_log_entry | Workbench | None | No | Decision log entry of the outcome |
| DF-REF-261 | payment_match_rule | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the payment match rule |
| DF-REF-262 | payment_match_rule | rule_code | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Row code, for example EXACT |
| DF-REF-263 | payment_match_rule | rule_version | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Parameter version, for example PM-2026.12 |
| DF-REF-264 | payment_match_rule | match_type | LOV | varchar(15) | 15 | Yes | None | LOV-MATCH-TYPE | None | None | Workbench | None | No | Exact, window or partial |
| DF-REF-265 | payment_match_rule | amount_tolerance_pct | NUMBER | numeric(5,2) | 5,2 | Yes | 0 | None | None | None | Workbench | None | No | Allowed difference from the installment, 0 to 100 percent |
| DF-REF-266 | payment_match_rule | window_days_before | NUMBER | integer |  | Yes | 0 | None | None | None | Workbench | None | No | Days before the due date a payment may arrive |
| DF-REF-267 | payment_match_rule | window_days_after | NUMBER | integer |  | Yes | 0 | None | None | None | Workbench | None | No | Days after the due date a payment may arrive |
| DF-REF-268 | payment_match_rule | grace_days | NUMBER | integer |  | Yes | 0 | None | None | None | Workbench | None | No | Days after the due date before PaymentMissed is raised |
| DF-REF-269 | payment_match_rule | partial_floor_pct | NUMBER | numeric(5,2) | 5,2 | No | None | None | None | None | Workbench | None | No | Lowest share of the installment matched as partial, percent |
| DF-REF-270 | payment_match_rule | priority | NUMBER | integer |  | Yes | None | None | None | None | Workbench | None | No | Order in which rows are tried |
| DF-REF-271 | payment_match_rule | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the version comes into force |
| DF-REF-272 | payment_match_rule | valid_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Last date the version is in force |
| DF-REF-273 | payment_match_rule | approved_by | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Credit Administration approver |
| DF-RPT-031 | measure_definition | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the measure definition |
| DF-RPT-032 | measure_definition | measure_code | TEXT | varchar(40) | 40 | Yes | None | None | UK | None | Workbench | None | No | Measure code |
| DF-RPT-033 | measure_definition | name | TEXT | varchar(120) | 120 | Yes | None | None | None | None | Workbench | None | No | Measure name |
| DF-RPT-034 | measure_definition | formula | TEXT | varchar(1000) | 1000 | Yes | None | None | None | None | Workbench | None | No | Formula in plain terms |
| DF-RPT-035 | measure_definition | data_product | LOV | varchar(25) | 25 | Yes | None | LOV-DATA-PRODUCT | None | None | Workbench | None | No | Data product the measure reads |
| DF-RPT-036 | measure_definition | unit | LOV | varchar(10) | 10 | Yes | None | LOV-MEASURE-UNIT | None | None | Workbench | None | No | Count, baht, days or percent |
| DF-RPT-037 | measure_definition | definition_version | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Definition version, for example MD-2026.11 |
| DF-RPT-038 | measure_definition | approved_by | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Tribe lead who approved |
| DF-RPT-039 | measure_definition | approved_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | Approval time |
| DF-RPT-040 | measure_definition | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the definition comes into force |
| DF-RPT-041 | measure_snapshot | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the measure snapshot |
| DF-RPT-042 | measure_snapshot | measure_code | TEXT | varchar(40) | 40 | Yes | None | None | None | None | Workbench | None | No | Measure, from measure_definition |
| DF-RPT-043 | measure_snapshot | definition_version | TEXT | varchar(20) | 20 | Yes | None | None | None | None | Workbench | None | No | Definition version used |
| DF-RPT-044 | measure_snapshot | business_date | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Business date measured |
| DF-RPT-045 | measure_snapshot | product_group | LOV | varchar(15) | 15 | No | None | LOV-PRODUCT | None | None | Workbench | None | No | Product group |
| DF-RPT-046 | measure_snapshot | dimension_code | LOV | varchar(20) | 20 | No | None | LOV-MEASURE-DIM | None | None | Workbench | None | No | Dimension: route, age band, queue, stage or agent |
| DF-RPT-047 | measure_snapshot | dimension_value | TEXT | varchar(60) | 60 | No | None | None | None | None | Workbench | None | No | Value of the dimension |
| DF-RPT-048 | measure_snapshot | value | NUMBER | numeric(18,4) | 18,4 | Yes | None | None | None | None | Workbench | None | No | Measure value |
| DF-RPT-049 | measure_snapshot | case_count | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Cases behind the value |
| DF-RPT-050 | measure_snapshot | is_baseline | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True for a row of the baseline date |
| DF-RPT-051 | measure_snapshot | frozen | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True when the row may not change |
| DF-RPT-052 | measure_snapshot | published_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When published |
| DF-RPT-053 | measure_publish | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the measure publish |
| DF-RPT-054 | measure_publish | business_date | DATE | date |  | Yes | None | None | UK | None | Workbench | None | No | Business date |
| DF-RPT-055 | measure_publish | status | LOV | varchar(10) | 10 | Yes | None | LOV-MEASURE-PUBLISH | None | None | Workbench | None | No | Published or held |
| DF-RPT-056 | measure_publish | case_list_count | NUMBER | integer |  | Yes | None | None | None | None | Workbench | None | No | Open cases on the case list at the cut-off |
| DF-RPT-057 | measure_publish | dashboard_count | NUMBER | integer |  | Yes | None | None | None | None | Workbench | None | No | Open cases in the dashboard facts |
| DF-RPT-058 | measure_publish | held_reason | TEXT | varchar(200) | 200 | No | None | None | None | None | Workbench | None | No | Why the publish is held |
| DF-AGT-001 | agent_policy | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the agent policy version |
| DF-AGT-002 | agent_policy | agent_code | LOV | varchar(30) | 30 | Yes | None | LOV-AGENT | UK | None | Workbench | None | No | Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER |
| DF-AGT-003 | agent_policy | policy_version | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Policy version, for example P1 |
| DF-AGT-004 | agent_policy | model_code | TEXT | varchar(40) | 40 | Yes | None | None | None | None | Workbench | None | No | Model deployment the agent calls through the gateway |
| DF-AGT-005 | agent_policy | model_version | TEXT | varchar(40) | 40 | Yes | None | None | None | None | Workbench | None | No | Model version the policy uses |
| DF-AGT-006 | agent_policy | output_schema_ref | TEXT | varchar(400) | 400 | Yes | None | None | None | None | Workbench | None | No | Reference to the JSON Schema the answer must meet |
| DF-AGT-007 | agent_policy | allowed_tools | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Tools the agent may call through the tool gateway |
| DF-AGT-008 | agent_policy | autonomy_mode | LOV | varchar(10) | 10 | Yes | OFF | LOV-AUTONOMY | None | None | Workbench | None | No | Off, shadow or L1 |
| DF-AGT-009 | agent_policy | segment_product_group | LOV | varchar(15) | 15 | No | None | LOV-PRODUCT | None | None | Workbench | None | No | Product group the mode applies to; empty for all |
| DF-AGT-010 | agent_policy | segment_region_code | LOV | varchar(10) | 10 | No | None | LOV-REGION | None | None | Workbench | None | No | Region the mode applies to; empty for all |
| DF-AGT-011 | agent_policy | confidence_floor | NUMBER | numeric(5,4) | 5,4 | Yes | None | None | None | None | Workbench | None | No | Answers below this confidence fall back or are marked for review |
| DF-AGT-012 | agent_policy | timeout_seconds | NUMBER | integer |  | Yes | None | None | None | None | Workbench | None | No | Seconds the gateway waits before the rule result is used |
| DF-AGT-013 | agent_policy | daily_cost_cap_thb | NUMBER | numeric(12,2) | 12,2 | Yes | None | None | None | None | Workbench | None | No | Daily model cost limit per agent, baht |
| DF-AGT-014 | agent_policy | price_per_1k_tokens_thb | NUMBER | numeric(10,4) | 10,4 | Yes | None | None | None | None | Workbench | None | No | Model price per 1,000 tokens, baht |
| DF-AGT-015 | agent_policy | alert_role | LOV | varchar(20) | 20 | Yes | None | LOV-ROLE | None | None | Workbench | None | No | Role that receives cost and drift alerts |
| DF-AGT-016 | agent_policy | review_date | DATE | date |  | No | None | None | None | None | Workbench | None | No | Date the version is reviewed again, for a parked or shadow agent |
| DF-AGT-017 | agent_policy | evaluation_run_id | CROSS_REF | uuid |  | No | None | None | FK | agent_evaluation_run | Workbench | None | No | Evaluation run an autonomy step is based on |
| DF-AGT-018 | agent_policy | promotion_conditions | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Conditions the evaluation must meet for the stated mode |
| DF-AGT-019 | agent_policy | watch_measures | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Measures and limits to watch after the step, including the drift threshold and minimum feedback |
| DF-AGT-020 | agent_policy | fallback_rule | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | Rule applied when the agent does not answer, for example R-UNI-32 |
| DF-AGT-021 | agent_policy | status | LOV | varchar(12) | 12 | Yes | LOADED | LOV-CONFIG-STATUS | None | None | Workbench | None | No | Loaded, approved or retired |
| DF-AGT-022 | agent_policy | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the version takes effect |
| DF-AGT-023 | agent_policy | valid_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Last date the version is in force |
| DF-AGT-024 | agent_policy | loaded_by | USER_REF | uuid |  | Yes | None | None | None | None | Workbench | None | No | Who loaded the version |
| DF-AGT-025 | agent_policy | approved_by | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Who approved the version |
| DF-AGT-026 | agent_prompt | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the agent prompt version |
| DF-AGT-027 | agent_prompt | agent_code | LOV | varchar(30) | 30 | Yes | None | LOV-AGENT | UK | None | Workbench | None | No | Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER |
| DF-AGT-028 | agent_prompt | prompt_version | TEXT | varchar(20) | 20 | Yes | None | None | UK | None | Workbench | None | No | Prompt version, for example PR1 |
| DF-AGT-029 | agent_prompt | body_text | TEXT | text |  | Yes | None | None | None | None | Workbench | None | No | Prompt text with placeholders; no personal data |
| DF-AGT-030 | agent_prompt | body_hash | TEXT | char(64) | 64 | Yes | None | None | None | None | Workbench | None | No | SHA-256 of the prompt text |
| DF-AGT-031 | agent_prompt | status | LOV | varchar(12) | 12 | Yes | LOADED | LOV-CONFIG-STATUS | None | None | Workbench | None | No | Loaded, approved or retired |
| DF-AGT-032 | agent_prompt | valid_from | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Date the version takes effect |
| DF-AGT-033 | agent_prompt | valid_to | DATE | date |  | No | None | None | None | None | Workbench | None | No | Last date the version is in force |
| DF-AGT-034 | agent_prompt | loaded_by | USER_REF | uuid |  | Yes | None | None | None | None | Workbench | None | No | Who loaded the version |
| DF-AGT-035 | agent_prompt | approved_by | USER_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Who approved the version |
| DF-AGT-036 | agent_run | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the agent run |
| DF-AGT-037 | agent_run | agent_code | LOV | varchar(30) | 30 | Yes | None | LOV-AGENT | None | None | Workbench | None | No | Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER |
| DF-AGT-038 | agent_run | agent_version | TEXT | varchar(40) | 40 | Yes | None | None | None | None | Workbench | None | No | Agent, policy and prompt version as <agent>@<policy>/<prompt> |
| DF-AGT-039 | agent_run | prompt_version | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | Prompt version used |
| DF-AGT-040 | agent_run | model_version | TEXT | varchar(40) | 40 | Yes | None | None | None | None | Workbench | None | No | Model version used |
| DF-AGT-041 | agent_run | case_id | CROSS_REF | uuid |  | No | None | None | FK | recovery_case | Workbench | None | No | The case the run is for |
| DF-AGT-042 | agent_run | subject_id | CROSS_REF | uuid |  | No | None | None | None | None | Workbench | None | No | Document, legal action or treatment the run is about, where not the case |
| DF-AGT-043 | agent_run | autonomy_mode | LOV | varchar(10) | 10 | Yes | None | LOV-AUTONOMY | None | None | Workbench | None | No | Mode the run used: shadow or L1 |
| DF-AGT-044 | agent_run | trigger_event | TEXT | varchar(30) | 30 | Yes | None | None | None | None | Workbench | None | No | CaseCreated, DocumentStored, STEP or EVALUATION |
| DF-AGT-045 | agent_run | idempotency_key | TEXT | varchar(120) | 120 | Yes | None | None | UK | None | Workbench | None | No | Unique key of the run request |
| DF-AGT-046 | agent_run | status | LOV | varchar(20) | 20 | Yes | None | LOV-AGENT-RUN | None | None | Workbench | None | No | Answered, timed out, guardrail failed, below floor, tool unavailable, model error or disabled |
| DF-AGT-047 | agent_run | fallback | BOOLEAN | boolean |  | Yes | false | None | None | None | Workbench | None | No | True when the rule result was used instead of the answer |
| DF-AGT-048 | agent_run | guardrail_result | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Failed check codes and details |
| DF-AGT-049 | agent_run | output | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Checked answer, masked; never returned for shadow runs |
| DF-AGT-050 | agent_run | confidence | NUMBER | numeric(5,4) | 5,4 | No | None | None | None | None | Workbench | None | No | Confidence of the answer |
| DF-AGT-051 | agent_run | latency_ms | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Time from call to answer or timeout, milliseconds |
| DF-AGT-052 | agent_run | tokens_in | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Input tokens returned by the endpoint |
| DF-AGT-053 | agent_run | tokens_out | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Output tokens returned by the endpoint |
| DF-AGT-054 | agent_run | cost_thb | NUMBER | numeric(12,4) | 12,4 | No | None | None | None | None | Workbench | None | No | Cost of the run, baht |
| DF-AGT-055 | agent_run | data_as_of | DATE | date |  | No | None | None | None | None | Workbench | None | No | Oldest business date of the inputs used |
| DF-AGT-056 | agent_run | run_at | DATE | timestamptz |  | Yes | None | None | None | None | Workbench | None | No | When the run started |
| DF-AGT-057 | agent_run | evaluation_run_id | CROSS_REF | uuid |  | No | None | None | FK | agent_evaluation_run | Workbench | None | No | Evaluation run the run belongs to, if any |
| DF-AGT-058 | agent_run | decision_log_id | CROSS_REF | uuid |  | No | None | None | FK | decision_log_entry | Workbench | None | No | Decision log entry written for the step that used the run |
| DF-AGT-059 | agent_run | segment_product_group | LOV | varchar(15) | 15 | No | None | LOV-PRODUCT | None | None | Workbench | None | No | Product group of the case at run time |
| DF-AGT-060 | agent_run | segment_region_code | LOV | varchar(10) | 10 | No | None | LOV-REGION | None | None | Workbench | None | No | Region of the case at run time |
| DF-AGT-061 | agent_sample | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the sample row |
| DF-AGT-062 | agent_sample | agent_code | LOV | varchar(30) | 30 | Yes | None | LOV-AGENT | None | None | Workbench | None | No | Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER |
| DF-AGT-063 | agent_sample | sample_code | TEXT | varchar(30) | 30 | Yes | None | None | UK | None | Workbench | None | No | Sample code, for example INTAKE-S1 |
| DF-AGT-064 | agent_sample | sample_version | NUMBER | integer |  | Yes | None | None | UK | None | Workbench | None | No | Version of the sample |
| DF-AGT-065 | agent_sample | subject_type | LOV | varchar(15) | 15 | Yes | None | LOV-SUBJECT-TYPE | None | None | Workbench | None | No | Case, document or legal action |
| DF-AGT-066 | agent_sample | subject_id | CROSS_REF | uuid |  | Yes | None | None | None | None | Workbench | None | No | The case, document or legal action labeled |
| DF-AGT-067 | agent_sample | label_key | TEXT | varchar(60) | 60 | Yes | None | None | UK | None | Workbench | None | No | Gap type, deviation code, field name or checklist item |
| DF-AGT-068 | agent_sample | expected_value | TEXT | varchar(1000) | 1000 | No | None | None | None | None | Workbench | None | No | Labeled value; SHA-256 hash for personal values |
| DF-AGT-069 | agent_sample | labeled_by | USER_REF | uuid |  | Yes | None | None | None | None | Workbench | None | No | Who labeled the row |
| DF-AGT-070 | agent_evaluation_run | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the evaluation run |
| DF-AGT-071 | agent_evaluation_run | agent_code | LOV | varchar(30) | 30 | Yes | None | LOV-AGENT | None | None | Workbench | None | No | Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER |
| DF-AGT-072 | agent_evaluation_run | sample_code | TEXT | varchar(30) | 30 | Yes | None | None | None | None | Workbench | None | No | Sample used |
| DF-AGT-073 | agent_evaluation_run | sample_version | NUMBER | integer |  | Yes | None | None | None | None | Workbench | None | No | Sample version used |
| DF-AGT-074 | agent_evaluation_run | policy_version | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | Policy version evaluated |
| DF-AGT-075 | agent_evaluation_run | prompt_version | TEXT | varchar(20) | 20 | No | None | None | None | None | Workbench | None | No | Prompt version evaluated |
| DF-AGT-076 | agent_evaluation_run | model_version | TEXT | varchar(40) | 40 | No | None | None | None | None | Workbench | None | No | Model version evaluated |
| DF-AGT-077 | agent_evaluation_run | status | LOV | varchar(12) | 12 | Yes | RUNNING | LOV-EVAL-STATUS | None | None | Workbench | None | No | Running, done or failed |
| DF-AGT-078 | agent_evaluation_run | started_at | DATE | timestamptz |  | Yes | None | None | None | None | Workbench | None | No | When the run started |
| DF-AGT-079 | agent_evaluation_run | finished_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the run ended |
| DF-AGT-080 | agent_evaluation_run | requested_by | USER_REF | uuid |  | Yes | None | None | None | None | Workbench | None | No | Who started the run |
| DF-AGT-081 | agent_evaluation_run | total_cost_thb | NUMBER | numeric(12,4) | 12,4 | No | None | None | None | None | Workbench | None | No | Cost of all runs in the evaluation, baht |
| DF-AGT-082 | agent_evaluation_run | p95_latency_ms | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | 95th percentile latency, milliseconds |
| DF-AGT-083 | agent_evaluation_run | failure_counts | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Count of runs by failure status and check code |
| DF-AGT-084 | agent_evaluation_run | proposal | TEXT | jsonb |  | No | None | None | None | None | Workbench | None | No | Proposed approach and confidence threshold per document type |
| DF-AGT-085 | agent_evaluation_run | review_count | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | Proposals below the confidence floor, scored separately |
| DF-AGT-086 | agent_evaluation | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the evaluation score |
| DF-AGT-087 | agent_evaluation | evaluation_run_id | CROSS_REF | uuid |  | Yes | None | None | FK | agent_evaluation_run | Workbench | None | No | Evaluation run the score belongs to |
| DF-AGT-088 | agent_evaluation | approach | LOV | varchar(20) | 20 | Yes | None | LOV-EXTRACT-APPROACH | None | None | Workbench | None | No | Agent, OCR template, model, or OCR and model |
| DF-AGT-089 | agent_evaluation | label_key | TEXT | varchar(60) | 60 | Yes | None | None | None | None | Workbench | None | No | Gap type, code, field or item scored |
| DF-AGT-090 | agent_evaluation | sample_size | NUMBER | integer |  | Yes | None | None | None | None | Workbench | None | No | Labeled subjects scored |
| DF-AGT-091 | agent_evaluation | true_positive | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | True positives |
| DF-AGT-092 | agent_evaluation | false_positive | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | False positives |
| DF-AGT-093 | agent_evaluation | false_negative | NUMBER | integer |  | No | None | None | None | None | Workbench | None | No | False negatives |
| DF-AGT-094 | agent_evaluation | agreement_rate | NUMBER | numeric(5,4) | 5,4 | No | None | None | None | None | Workbench | None | No | Share of subjects where the answer equals the label |
| DF-AGT-095 | agent_evaluation | precision_value | FORMULA | numeric(5,4) | 5,4 | No | None | None | None | None | Workbench | None | No | TP / (TP + FP) |
| DF-AGT-096 | agent_evaluation | recall_value | FORMULA | numeric(5,4) | 5,4 | No | None | None | None | None | Workbench | None | No | TP / (TP + FN) |
| DF-AGT-097 | agent_feedback | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the feedback |
| DF-AGT-098 | agent_feedback | agent_run_id | CROSS_REF | uuid |  | Yes | None | None | FK | agent_run | Workbench | None | No | Agent run the feedback is on |
| DF-AGT-099 | agent_feedback | item_key | TEXT | varchar(20) | 20 | Yes | None | None | None | None | Workbench | None | No | SUMMARY for the intake summary, or the deviation code |
| DF-AGT-100 | agent_feedback | verdict | LOV | varchar(10) | 10 | Yes | None | LOV-FEEDBACK | None | None | Workbench | None | No | Accepted, corrected or rejected |
| DF-AGT-101 | agent_feedback | reason | TEXT | varchar(1000) | 1000 | No | None | None | None | None | Workbench | None | No | Reason for a correction or a rejection |
| DF-AGT-102 | agent_feedback | decision_log_id | CROSS_REF | uuid |  | No | None | None | FK | decision_log_entry | Workbench | None | No | Decision log entry written for the feedback |
| DF-AGT-103 | agent_alert | id | TEXT | uuid |  | Yes | gen_random_uuid() | None | PK | None | Workbench | None | No | Record identifier of the alert |
| DF-AGT-104 | agent_alert | agent_code | LOV | varchar(30) | 30 | Yes | None | LOV-AGENT | None | None | Workbench | None | No | Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER |
| DF-AGT-105 | agent_alert | alert_type | LOV | varchar(12) | 12 | Yes | None | LOV-AGENT-ALERT | None | None | Workbench | None | No | Cost cap or drift |
| DF-AGT-106 | agent_alert | segment | TEXT | varchar(30) | 30 | Yes | None | None | None | None | Workbench | None | No | Product group and region, or ALL |
| DF-AGT-107 | agent_alert | business_date | DATE | date |  | Yes | None | None | None | None | Workbench | None | No | Business date measured |
| DF-AGT-108 | agent_alert | measured_value | NUMBER | numeric(14,4) | 14,4 | Yes | None | None | None | None | Workbench | None | No | Cost in baht or acceptance rate measured |
| DF-AGT-109 | agent_alert | threshold_value | NUMBER | numeric(14,4) | 14,4 | Yes | None | None | None | None | Workbench | None | No | Limit the value was compared with |
| DF-AGT-110 | agent_alert | sent_to_role | LOV | varchar(20) | 20 | Yes | None | LOV-ROLE | None | None | Workbench | None | No | Role notified |
| DF-AGT-111 | agent_alert | sent_at | DATE | timestamptz |  | No | None | None | None | None | Workbench | None | No | When the notification was sent; empty until sent |

## Standard columns

| Standard columns |  |  |  |  |  |
|---|---|---|---|---|---|
| Every entity carries these seven columns in addition to its own fields, as in bank TSD section T3.0. |  |  |  |  |  |
| Field | Data type | Physical type | Mandatory | Default | Meaning |
| is_active | BOOLEAN | boolean | Yes | true | The active or inactive status of the record |
| state | TEXT | varchar(40) | No | None | Record lifecycle state |
| version | NUMBER | integer | Yes | 1 | Optimistic lock version |
| created_at | DATE | timestamptz | Yes | now() | When the record was created |
| created_by | USER_REF | uuid | No | None | Who or which service identity created it |
| updated_at | DATE | timestamptz | Yes | now() | When the record last changed |
| updated_by | USER_REF | uuid | No | None | Who or which service identity last changed it |

## Lists of values

| Lists of values |  |  |  |  |
|---|---|---|---|---|
| 124 closed lists with 598 values. Each value carries an English and a Thai label; Thai labels follow decision DL10. |  |  |  |  |
| List | Value code | English label | Thai label | Order |
| LOV-PRODUCT | MORTGAGE | Mortgage | Pending | 1 |
| LOV-PRODUCT | HIRE_PURCHASE | Hire purchase | Pending | 2 |
| LOV-PRODUCT | SSME | SSME | Pending | 3 |
| LOV-PRODUCT | UNSECURED | Unsecured | Pending | 4 |
| LOV-CASE-STATUS | NEW | New | Pending | 1 |
| LOV-CASE-STATUS | ASSIGNED | Assigned | Pending | 2 |
| LOV-CASE-STATUS | IN_PROGRESS | In progress | Pending | 3 |
| LOV-CASE-STATUS | WAITING_CUSTOMER | Waiting customer | Pending | 4 |
| LOV-CASE-STATUS | WAITING_PARTNER | Waiting partner | Pending | 5 |
| LOV-CASE-STATUS | WAITING_APPROVAL | Waiting approval | Pending | 6 |
| LOV-CASE-STATUS | ON_HOLD | On hold | Pending | 7 |
| LOV-CASE-STATUS | CLOSED | Closed | Pending | 8 |
| LOV-STAGE | RESTRUCTURE | Restructure | Pending | 1 |
| LOV-STAGE | SETTLEMENT | Settlement | Pending | 2 |
| LOV-STAGE | DEED_IN_LIEU | Deed in lieu | Pending | 3 |
| LOV-STAGE | GUARANTEE_CLAIM | Guarantee claim | Pending | 4 |
| LOV-STAGE | LITIGATION | Litigation | Pending | 5 |
| LOV-STAGE | ASSET_DISPOSAL | Asset disposal | Pending | 6 |
| LOV-STAGE | DEBT_SALE | Debt sale | Pending | 7 |
| LOV-STAGE | WRITE_OFF | Write-off | Pending | 8 |
| LOV-STAGE | DEVIATIONS | Deviations | Pending | 9 |
| LOV-ROUTE | R1 | Restructure | Pending | 1 |
| LOV-ROUTE | R2 | Settlement | Pending | 2 |
| LOV-ROUTE | R3 | Deed in lieu | Pending | 3 |
| LOV-ROUTE | R4 | Guarantee claim | Pending | 4 |
| LOV-ROUTE | R5 | Litigation | Pending | 5 |
| LOV-ROUTE | R6 | Asset disposal | Pending | 6 |
| LOV-ROUTE | R7 | Debt sale | Pending | 7 |
| LOV-ROUTE | R8 | Write-off | Pending | 8 |
| LOV-CLOSURE | CURED | Cured | Pending | 1 |
| LOV-CLOSURE | SETTLED | Settled | Pending | 2 |
| LOV-CLOSURE | REALIZED | Realized | Pending | 3 |
| LOV-CLOSURE | SOLD | Sold | Pending | 4 |
| LOV-CLOSURE | WRITTEN_OFF | Written off | Pending | 5 |
| LOV-CLOSURE | INSURANCE_SETTLED | Insurance settled | Pending | 6 |
| LOV-CLOSURE | MERGED | Merged | Pending | 7 |
| LOV-CLOSURE | CANCELED | Canceled | Pending | 8 |
| LOV-PARTY-ROLE | BORROWER | Borrower | Pending | 1 |
| LOV-PARTY-ROLE | CO_BORROWER | Co-borrower | Pending | 2 |
| LOV-PARTY-ROLE | GUARANTOR | Guarantor | Pending | 3 |
| LOV-PARTY-ROLE | AUTHORIZED_SIGNATORY | Authorized signatory | Pending | 4 |
| LOV-PARTY-ROLE | HEIR | Heir | Pending | 5 |
| LOV-DEVIATION | X1 | Dispute or complaint | Pending | 1 |
| LOV-DEVIATION | X2 | Vulnerable customer or hardship | Pending | 2 |
| LOV-DEVIATION | X3 | Deceased customer | Pending | 3 |
| LOV-DEVIATION | X4 | Fraud | Pending | 4 |
| LOV-DEVIATION | X5 | Bankruptcy or external seizure | Pending | 5 |
| LOV-DEVIATION | X6 | Lost contact | Pending | 6 |
| LOV-DEVIATION | X7 | Collateral event | Pending | 7 |
| LOV-DEV-OUTCOME | RETURNED | Returned | Pending | 1 |
| LOV-DEV-OUTCOME | RE_ROUTED | Re-routed | Pending | 2 |
| LOV-DEV-OUTCOME | CASE_ENDED | Case ended | Pending | 3 |
| LOV-RAISED-BY | SCREENING_AGENT | Screening agent | Pending | 1 |
| LOV-RAISED-BY | RULE | Rule | Pending | 2 |
| LOV-RAISED-BY | OFFICER | Officer | Pending | 3 |
| LOV-RAISED-BY | CUSTOMER_CONTACT | Customer contact | Pending | 4 |
| LOV-ASSIGN | ROUND_ROBIN | Round robin | Pending | 1 |
| LOV-ASSIGN | LOWEST_LOAD | Lowest load | Pending | 2 |
| LOV-ASSIGN | NAMED_OWNER | Named owner | Pending | 3 |
| LOV-ASSIGN | SKILL | Skill | Pending | 4 |
| LOV-ASSIGN-REASON | ALLOCATION | Allocation | Pending | 1 |
| LOV-ASSIGN-REASON | TRANSFER | Transfer | Pending | 2 |
| LOV-ASSIGN-REASON | REBALANCE | Rebalance | Pending | 3 |
| LOV-ASSIGN-REASON | MANUAL | Manual | Pending | 4 |
| LOV-ASSIGN-REASON | ESCALATION | Escalation | Pending | 5 |
| LOV-ELEMENT | HUMAN_TASK | Human task | Pending | 1 |
| LOV-ELEMENT | CUSTOMER_TASK | Customer task | Pending | 2 |
| LOV-ELEMENT | PARTNER_TASK | Partner task | Pending | 3 |
| LOV-ELEMENT | DECISION_TASK | Decision task | Pending | 4 |
| LOV-ELEMENT | STAGE_ENTRY | Stage entry | Pending | 5 |
| LOV-ELEMENT | MILESTONE | Milestone | Pending | 6 |
| LOV-ELEMENT | EVENT_LISTENER | Event listener | Pending | 7 |
| LOV-DISCRETION | AUTOMATIC | Automatic | Pending | 1 |
| LOV-DISCRETION | DISCRETIONARY | Discretionary | Pending | 2 |
| LOV-DISCRETION | REQUIRED | Required | Pending | 3 |
| LOV-TASK-STATUS | OPEN | Open | Pending | 1 |
| LOV-TASK-STATUS | IN_PROGRESS | In progress | Pending | 2 |
| LOV-TASK-STATUS | DONE | Done | Pending | 3 |
| LOV-TASK-STATUS | CANCELED | Canceled | Pending | 4 |
| LOV-TIMER | SERVICE_LEVEL | Service level | Pending | 1 |
| LOV-TIMER | NOTICE_PERIOD | Notice period | Pending | 2 |
| LOV-TIMER | CURE_PERIOD | Cure period | Pending | 3 |
| LOV-TIMER | PRESCRIPTION | Prescription | Pending | 4 |
| LOV-TIMER | HEARING_DEADLINE | Hearing deadline | Pending | 5 |
| LOV-TIMER | OFFER_VALIDITY | Offer validity | Pending | 6 |
| LOV-TIMER | HOLDING_AGE | Holding age | Pending | 7 |
| LOV-TIMER | CLAIM_DEADLINE | Claim deadline | Pending | 8 |
| LOV-TIMER | INSTALLMENT_DUE | Installment due | Pending | 9 |
| LOV-TIMER-STATUS | RUNNING | Running | Pending | 1 |
| LOV-TIMER-STATUS | PAUSED | Paused | Pending | 2 |
| LOV-TIMER-STATUS | EXPIRED | Expired | Pending | 3 |
| LOV-TIMER-STATUS | STOPPED | Stopped | Pending | 4 |
| LOV-PARTY-TYPE | INDIVIDUAL | Individual | Pending | 1 |
| LOV-PARTY-TYPE | JURISTIC_PERSON | Juristic person | Pending | 2 |
| LOV-ID-TYPE | THAI_NATIONAL_ID | Thai national ID | Pending | 1 |
| LOV-ID-TYPE | PASSPORT | Passport | Pending | 2 |
| LOV-ID-TYPE | COMPANY_REGISTRATION | Company registration | Pending | 3 |
| LOV-SEGMENT | RETAIL | Retail | Pending | 1 |
| LOV-SEGMENT | SSME | SSME | Pending | 2 |
| LOV-SEGMENT | CORPORATE | Corporate | Pending | 3 |
| LOV-CHANNEL | MOBILE | Mobile | Pending | 1 |
| LOV-CHANNEL | HOME_PHONE | Home phone | Pending | 2 |
| LOV-CHANNEL | WORK_PHONE | Work phone | Pending | 3 |
| LOV-CHANNEL | LINE | LINE | Pending | 4 |
| LOV-CHANNEL | EMAIL | Email | Pending | 5 |
| LOV-CHANNEL | POSTAL_ADDRESS | Postal address | Pending | 6 |
| LOV-CHANNEL | CALL | Call | Pending | 7 |
| LOV-CHANNEL | VISIT | Visit | Pending | 8 |
| LOV-CHANNEL | SMS | SMS | Pending | 9 |
| LOV-CHANNEL | LETTER | Letter | Pending | 10 |
| LOV-CHANNEL | PORTAL | Portal | Pending | 11 |
| LOV-CHANNEL | BRANCH | Branch | Pending | 12 |
| LOV-CONTACT-SRC | BANK_RECORD | Bank record | Pending | 1 |
| LOV-CONTACT-SRC | FIELD_VISIT | Field visit | Pending | 2 |
| LOV-CONTACT-SRC | AGENCY | Agency | Pending | 3 |
| LOV-CONTACT-SRC | BUREAU_TRACE | Bureau trace | Pending | 4 |
| LOV-CONTACT-SRC | CUSTOMER | Customer | Pending | 5 |
| LOV-CONSENT | GIVEN | Given | Pending | 1 |
| LOV-CONSENT | WITHDRAWN | Withdrawn | Pending | 2 |
| LOV-CONSENT | UNKNOWN | Unknown | Pending | 3 |
| LOV-COLL-TYPE | LAND | Land | Pending | 1 |
| LOV-COLL-TYPE | HOUSE | House | Pending | 2 |
| LOV-COLL-TYPE | CONDOMINIUM | Condominium | Pending | 3 |
| LOV-COLL-TYPE | VEHICLE | Vehicle | Pending | 4 |
| LOV-COLL-TYPE | DEPOSIT | Deposit | Pending | 5 |
| LOV-COLL-TYPE | OTHER | Other | Pending | 6 |
| LOV-OCCUPANCY | OWNER | Owner | Pending | 1 |
| LOV-OCCUPANCY | TENANT | Tenant | Pending | 2 |
| LOV-OCCUPANCY | VACANT | Vacant | Pending | 3 |
| LOV-OCCUPANCY | UNKNOWN | Unknown | Pending | 4 |
| LOV-ENCUMBRANCE | CLEAR | Clear | Pending | 1 |
| LOV-ENCUMBRANCE | OTHER_CREDITOR | Other creditor | Pending | 2 |
| LOV-ENCUMBRANCE | SEIZED | Seized | Pending | 3 |
| LOV-ENCUMBRANCE | UNDER_DISPUTE | Under dispute | Pending | 4 |
| LOV-APPRAISAL | MARKET | Market | Pending | 1 |
| LOV-APPRAISAL | OFFICIAL | Official | Pending | 2 |
| LOV-APPRAISAL | FORCED_SALE | Forced sale | Pending | 3 |
| LOV-APPRAISAL | DESKTOP | Desktop | Pending | 4 |
| LOV-APPRAISAL | AGENT_ESTIMATE | Agent estimate | Pending | 5 |
| LOV-ASSET-TYPE | DETACHED_HOUSE | Detached house | Pending | 1 |
| LOV-ASSET-TYPE | TOWNHOUSE | Townhouse | Pending | 2 |
| LOV-ASSET-TYPE | CONDOMINIUM | Condominium | Pending | 3 |
| LOV-ASSET-TYPE | LAND | Land | Pending | 4 |
| LOV-ASSET-TYPE | COMMERCIAL_BUILDING | Commercial building | Pending | 5 |
| LOV-ASSET-TYPE | VEHICLE | Vehicle | Pending | 6 |
| LOV-TRANSFER-IN | AUCTION_PURCHASE | Auction purchase | Pending | 1 |
| LOV-TRANSFER-IN | DEED_IN_LIEU | Deed in lieu | Pending | 2 |
| LOV-TRANSFER-IN | REPOSSESSION | Repossession | Pending | 3 |
| LOV-HOLDING | HELD | Held | Pending | 1 |
| LOV-HOLDING | LISTED | Listed | Pending | 2 |
| LOV-HOLDING | UNDER_OFFER | Under offer | Pending | 3 |
| LOV-HOLDING | SOLD | Sold | Pending | 4 |
| LOV-HOLDING | TRANSFERRED | Transferred | Pending | 5 |
| LOV-HOLDING | RENTED | Rented | Pending | 6 |
| LOV-TREATMENT | RESTRUCTURE | Restructure | Pending | 1 |
| LOV-TREATMENT | SETTLEMENT | Settlement | Pending | 2 |
| LOV-TREATMENT | DEED_IN_LIEU | Deed in lieu | Pending | 3 |
| LOV-TREATMENT | BUY_BACK | Buy-back | Pending | 4 |
| LOV-TREATMENT | GUARANTEE_CLAIM | Guarantee claim | Pending | 5 |
| LOV-TREATMENT | REPOSSESSION | Repossession | Pending | 6 |
| LOV-TREATMENT | AUCTION | Auction | Pending | 7 |
| LOV-TREATMENT | DEBT_SALE | Debt sale | Pending | 8 |
| LOV-TREATMENT | WRITE_OFF | Write-off | Pending | 9 |
| LOV-TREATMENT | RAMC_TRANSFER | RAMC transfer | Pending | 10 |
| LOV-TREATMENT | RENTAL | Rental | Pending | 11 |
| LOV-PROPOSER | AGENT | Agent | Pending | 1 |
| LOV-PROPOSER | RULE | Rule | Pending | 2 |
| LOV-PROPOSER | PERSON | Person | Pending | 3 |
| LOV-APPROVAL-LEVEL | L1 | Board of Directors | Pending | 1 |
| LOV-APPROVAL-LEVEL | L2 | Executive Committee | Pending | 2 |
| LOV-APPROVAL-LEVEL | L3 | Problem Asset Resolution Committee or Management Committee | Pending | 3 |
| LOV-APPROVAL-LEVEL | L4 | Head of Recovery, function level, or Problem Asset Resolution Committee | Pending | 4 |
| LOV-APPROVAL-LEVEL | L5 | Recovery executive, division level | Pending | 5 |
| LOV-APPROVAL-LEVEL | L6 | Recovery executive, department level | Pending | 6 |
| LOV-TRT-OUTCOME | KEPT | Kept | Pending | 1 |
| LOV-TRT-OUTCOME | BROKEN | Broken | Pending | 2 |
| LOV-TRT-OUTCOME | COMPLETED | Completed | Pending | 3 |
| LOV-TRT-OUTCOME | CANCELED | Canceled | Pending | 4 |
| LOV-TRT-OUTCOME | DECLINED | Declined | Pending | 5 |
| LOV-CLAIM-TYPE | TCG | TCG | Pending | 1 |
| LOV-CLAIM-TYPE | CREDIT_LIFE_INSURANCE | Credit life insurance | Pending | 2 |
| LOV-CLAIM-TYPE | MORTGAGE_INSURANCE | Mortgage insurance | Pending | 3 |
| LOV-CLAIM-TYPE | COLLATERAL_INSURANCE | Collateral insurance | Pending | 4 |
| LOV-CLAIM-STATUS | PREPARING | Preparing | Pending | 1 |
| LOV-CLAIM-STATUS | FILED | Filed | Pending | 2 |
| LOV-CLAIM-STATUS | DEFECT | Defect | Pending | 3 |
| LOV-CLAIM-STATUS | PAID | Paid | Pending | 4 |
| LOV-CLAIM-STATUS | REJECTED | Rejected | Pending | 5 |
| LOV-LEGAL-TYPE | NOTICE | Notice | Pending | 1 |
| LOV-LEGAL-TYPE | CIVIL_CASE | Civil case | Pending | 2 |
| LOV-LEGAL-TYPE | APPEAL | Appeal | Pending | 3 |
| LOV-LEGAL-TYPE | ENFORCEMENT | Enforcement | Pending | 4 |
| LOV-LEGAL-TYPE | BANKRUPTCY_PETITION | Bankruptcy petition | Pending | 5 |
| LOV-LEGAL-TYPE | LED_AUCTION | LED auction | Pending | 6 |
| LOV-LEGAL-STATUS | OPEN | Open | Pending | 1 |
| LOV-LEGAL-STATUS | FILED | Filed | Pending | 2 |
| LOV-LEGAL-STATUS | JUDGMENT | Judgment | Pending | 3 |
| LOV-LEGAL-STATUS | ENFORCING | Enforcing | Pending | 4 |
| LOV-LEGAL-STATUS | CLOSED | Closed | Pending | 5 |
| LOV-LEGAL-STATUS | WITHDRAWN | Withdrawn | Pending | 6 |
| LOV-NOTICE | DEMAND | Demand | Pending | 1 |
| LOV-NOTICE | RECALL | Recall | Pending | 2 |
| LOV-NOTICE | STATUTORY_SALE_NOTICE | Statutory sale notice | Pending | 3 |
| LOV-NOTICE | GUARANTOR_NOTICE | Guarantor notice | Pending | 4 |
| LOV-DELIVERY | DELIVERED | Delivered | Pending | 1 |
| LOV-DELIVERY | REFUSED | Refused | Pending | 2 |
| LOV-DELIVERY | UNDELIVERABLE | Undeliverable | Pending | 3 |
| LOV-DELIVERY | PENDING | Pending | Pending | 4 |
| LOV-SENT-TYPE | BEFORE_NPL | Before NPL | Pending | 1 |
| LOV-SENT-TYPE | NPL | NPL | Pending | 2 |
| LOV-HEARING | FIRST_HEARING | First hearing | Pending | 1 |
| LOV-HEARING | WITNESS | Witness | Pending | 2 |
| LOV-HEARING | JUDGMENT_READING | Judgment reading | Pending | 3 |
| LOV-HEARING | MEDIATION | Mediation | Pending | 4 |
| LOV-HEARING-OUTCOME | HELD | Held | Pending | 1 |
| LOV-HEARING-OUTCOME | ADJOURNED | Adjourned | Pending | 2 |
| LOV-HEARING-OUTCOME | SETTLED | Settled | Pending | 3 |
| LOV-HEARING-OUTCOME | JUDGMENT | Judgment | Pending | 4 |
| LOV-PARTNER-TYPE | AGENCY | Agency | Pending | 1 |
| LOV-PARTNER-TYPE | LAW_FIRM | Law firm | Pending | 2 |
| LOV-PARTNER-TYPE | VALUER | Valuer | Pending | 3 |
| LOV-PARTNER-TYPE | AUCTION_VENDOR | Auction vendor | Pending | 4 |
| LOV-PARTNER-TYPE | BROKER | Broker | Pending | 5 |
| LOV-PARTNER-TYPE | DEBT_BUYER | Debt buyer | Pending | 6 |
| LOV-PARTNER-TYPE | AMC | AMC | Pending | 7 |
| LOV-PARTNER-TYPE | RAMC | RAMC | Pending | 8 |
| LOV-PANEL | ACTIVE | Active | Pending | 1 |
| LOV-PANEL | ON_NOTICE | On notice | Pending | 2 |
| LOV-PANEL | SUSPENDED | Suspended | Pending | 3 |
| LOV-PANEL | EXITED | Exited | Pending | 4 |
| LOV-INSTRUCTION | COLLECT | Collect | Pending | 1 |
| LOV-INSTRUCTION | FILE_SUIT | File suit | Pending | 2 |
| LOV-INSTRUCTION | ENFORCE | Enforce | Pending | 3 |
| LOV-INSTRUCTION | APPRAISE | Appraise | Pending | 4 |
| LOV-INSTRUCTION | REPOSSESS | Repossess | Pending | 5 |
| LOV-INSTRUCTION | LIST | List | Pending | 6 |
| LOV-INSTRUCTION | SELL | Sell | Pending | 7 |
| LOV-INSTR-STATUS | SENT | Sent | Pending | 1 |
| LOV-INSTR-STATUS | ACCEPTED | Accepted | Pending | 2 |
| LOV-INSTR-STATUS | DECLINED | Declined | Pending | 3 |
| LOV-INSTR-STATUS | IN_PROGRESS | In progress | Pending | 4 |
| LOV-INSTR-STATUS | DONE | Done | Pending | 5 |
| LOV-INSTR-STATUS | RECALLED | Recalled | Pending | 6 |
| LOV-SALE-CHANNEL | DUTCH_AUCTION | Dutch auction | Pending | 1 |
| LOV-SALE-CHANNEL | BROKER | Broker | Pending | 2 |
| LOV-SALE-CHANNEL | DIRECT | Direct | Pending | 3 |
| LOV-SALE-CHANNEL | LED_AUCTION | LED auction | Pending | 4 |
| LOV-SALE-CHANNEL | RAMC | RAMC | Pending | 5 |
| LOV-LISTING | DRAFT | Draft | Pending | 1 |
| LOV-LISTING | LIVE | Live | Pending | 2 |
| LOV-LISTING | UNDER_OFFER | Under offer | Pending | 3 |
| LOV-LISTING | SOLD | Sold | Pending | 4 |
| LOV-LISTING | WITHDRAWN | Withdrawn | Pending | 5 |
| LOV-BUYER-CLASS | AMC | AMC | Pending | 1 |
| LOV-BUYER-CLASS | NON_AMC | Non-AMC | Pending | 2 |
| LOV-LOT-STATUS | BUILDING | Building | Pending | 1 |
| LOV-LOT-STATUS | OFFERED | Offered | Pending | 2 |
| LOV-LOT-STATUS | AWARDED | Awarded | Pending | 3 |
| LOV-LOT-STATUS | TRANSFERRED | Transferred | Pending | 4 |
| LOV-LOT-STATUS | CLOSED | Closed | Pending | 5 |
| LOV-PUTBACK | NONE | None | Pending | 1 |
| LOV-PUTBACK | CLAIMED | Claimed | Pending | 2 |
| LOV-PUTBACK | ACCEPTED | Accepted | Pending | 3 |
| LOV-PUTBACK | REJECTED | Rejected | Pending | 4 |
| LOV-DIRECTION | INBOUND | Inbound | Pending | 1 |
| LOV-DIRECTION | OUTBOUND | Outbound | Pending | 2 |
| LOV-CONTACT-RESULT | RIGHT_PARTY | Right party | Pending | 1 |
| LOV-CONTACT-RESULT | THIRD_PARTY | Third party | Pending | 2 |
| LOV-CONTACT-RESULT | NO_ANSWER | No answer | Pending | 3 |
| LOV-CONTACT-RESULT | WRONG_NUMBER | Wrong number | Pending | 4 |
| LOV-CONTACT-RESULT | REFUSED | Refused | Pending | 5 |
| LOV-CONDUCT | PASSED | Passed | Pending | 1 |
| LOV-CONDUCT | BLOCKED | Blocked | Pending | 2 |
| LOV-CONDUCT | NOT_APPLICABLE | Not applicable | Pending | 3 |
| LOV-SOURCE | EFS | EFS | Pending | 1 |
| LOV-SOURCE | WORKBENCH | Workbench | Pending | 2 |
| LOV-DOC-SOURCE | SCAN | Scan | Pending | 1 |
| LOV-DOC-SOURCE | UPLOAD | Upload | Pending | 2 |
| LOV-DOC-SOURCE | GENERATED | Generated | Pending | 3 |
| LOV-DOC-SOURCE | PARTNER | Partner | Pending | 4 |
| LOV-DOC-SOURCE | EMAIL | Email | Pending | 5 |
| LOV-REVIEW | NOT_NEEDED | Not needed | Pending | 1 |
| LOV-REVIEW | PENDING | Pending | Pending | 2 |
| LOV-REVIEW | CONFIRMED | Confirmed | Pending | 3 |
| LOV-REVIEW | CORRECTED | Corrected | Pending | 4 |
| LOV-CUSTODY | VAULT | Vault | Pending | 1 |
| LOV-CUSTODY | BRANCH | Branch | Pending | 2 |
| LOV-CUSTODY | POST | Post | Pending | 3 |
| LOV-CUSTODY | LAWYER | Lawyer | Pending | 4 |
| LOV-CUSTODY | COURT | Court | Pending | 5 |
| LOV-CUSTODY | LAND_OFFICE | Land office | Pending | 6 |
| LOV-PROCEEDS-SRC | CUSTOMER | Customer | Pending | 1 |
| LOV-PROCEEDS-SRC | LED | LED | Pending | 2 |
| LOV-PROCEEDS-SRC | AUCTION | Auction | Pending | 3 |
| LOV-PROCEEDS-SRC | BUYER | Buyer | Pending | 4 |
| LOV-PROCEEDS-SRC | AGENCY | Agency | Pending | 5 |
| LOV-PROCEEDS-SRC | INSURER | Insurer | Pending | 6 |
| LOV-PROCEEDS-SRC | GUARANTOR | Guarantor | Pending | 7 |
| LOV-MATCH | INSTALLMENT | Installment | Pending | 1 |
| LOV-MATCH | SETTLEMENT | Settlement | Pending | 2 |
| LOV-MATCH | FEE | Fee | Pending | 3 |
| LOV-MATCH | SALE_PROCEEDS | Sale proceeds | Pending | 4 |
| LOV-MATCH | UNMATCHED | Unmatched | Pending | 5 |
| LOV-ROUTE-SET | RESTRUCTURE | Restructure | Pending | 1 |
| LOV-ROUTE-SET | SETTLEMENT | Settlement | Pending | 2 |
| LOV-ROUTE-SET | DEED_IN_LIEU | Deed in lieu | Pending | 3 |
| LOV-ROUTE-SET | GUARANTEE_CLAIM | Guarantee claim | Pending | 4 |
| LOV-ROUTE-SET | LITIGATION | Litigation | Pending | 5 |
| LOV-ROUTE-SET | ASSET_DISPOSAL | Asset disposal | Pending | 6 |
| LOV-ROUTE-SET | DEBT_SALE | Debt sale | Pending | 7 |
| LOV-ROUTE-SET | WRITE_OFF | Write-off | Pending | 8 |
| LOV-ROUTE-SET | DEVIATIONS | Deviations | Pending | 9 |
| LOV-ROUTE-SET | UNIVERSAL_RULES | Universal rules | Pending | 10 |
| LOV-ROLE-CLASS | BANK_USER | Bank user | Pending | 1 |
| LOV-ROLE-CLASS | PARTNER_USER | Partner user | Pending | 2 |
| LOV-ROLE-CLASS | NON_HUMAN_ACTOR | Non-human actor | Pending | 3 |
| LOV-SCOPE | OWN | Own | Pending | 1 |
| LOV-SCOPE | TEAM | Team | Pending | 2 |
| LOV-SCOPE | REGION | Region | Pending | 3 |
| LOV-SCOPE | ALL | All | Pending | 4 |
| LOV-CAPABILITY | CASE_RECORD | Case record | Pending | 1 |
| LOV-CAPABILITY | QUEUE_AND_ALLOCATION | Queue and allocation | Pending | 2 |
| LOV-CAPABILITY | TREATMENT_AND_OFFER | Treatment and offer | Pending | 3 |
| LOV-CAPABILITY | LITIGATION | Litigation | Pending | 4 |
| LOV-CAPABILITY | ASSET_AND_DISPOSAL | Asset and disposal | Pending | 5 |
| LOV-CAPABILITY | DEBT_SALE | Debt sale | Pending | 6 |
| LOV-CAPABILITY | WRITE_OFF_AND_POSTING | Write-off and posting | Pending | 7 |
| LOV-CAPABILITY | DOCUMENTS | Documents | Pending | 8 |
| LOV-CAPABILITY | RULES_AND_PARAMETERS | Rules and parameters | Pending | 9 |
| LOV-CAPABILITY | REFERENCE_DATA | Reference data | Pending | 10 |
| LOV-CAPABILITY | DECISION_LOG | Decision log | Pending | 11 |
| LOV-CAPABILITY | PARTNER_PORTAL | Partner portal | Pending | 12 |
| LOV-CAPABILITY | REPORTING | Reporting | Pending | 13 |
| LOV-CAPABILITY | PLATFORM_ADMINISTRATION | Platform administration | Pending | 14 |
| LOV-LANG | TH | TH | Pending | 1 |
| LOV-LANG | EN | EN | Pending | 2 |
| LOV-DATA-PRODUCT | DP01 | Account and arrears | Pending | 1 |
| LOV-DATA-PRODUCT | DP02 | Customer and party | Pending | 2 |
| LOV-DATA-PRODUCT | DP03 | Case and ownership | Pending | 3 |
| LOV-DATA-PRODUCT | DP04 | Treatment and offers | Pending | 4 |
| LOV-DATA-PRODUCT | DP05 | Contact and promises | Pending | 5 |
| LOV-DATA-PRODUCT | DP06 | Collateral and assets | Pending | 6 |
| LOV-DATA-PRODUCT | DP07 | Legal events and cases | Pending | 7 |
| LOV-DATA-PRODUCT | DP08 | Partner performance | Pending | 8 |
| LOV-DATA-PRODUCT | DP09 | Debt sale | Pending | 9 |
| LOV-DATA-PRODUCT | DP10 | Documents and extracted fields | Pending | 10 |
| LOV-DATA-PRODUCT | DP11 | Scores and route economics | Pending | 11 |
| LOV-DATA-PRODUCT | DP12 | Decision log | Pending | 12 |
| LOV-DATA-PRODUCT | DP13 | Money and closure | Pending | 13 |
| LOV-DATA-PRODUCT | DP14 | Reference data | Pending | 14 |
| LOV-REFRESH | DAILY | Daily | Pending | 1 |
| LOV-REFRESH | WEEKLY | Weekly | Pending | 2 |
| LOV-REFRESH | MONTHLY | Monthly | Pending | 3 |
| LOV-REFRESH | ON_CHANGE | On change | Pending | 4 |
| LOV-FRESHNESS | LOADED | Loaded | Pending | 1 |
| LOV-FRESHNESS | STALE | Stale | Pending | 2 |
| LOV-CONTRACT-STATUS | DRAFT | Draft | Pending | 1 |
| LOV-CONTRACT-STATUS | PUBLISHED | Published | Pending | 2 |
| LOV-CONTRACT-STATUS | SUPERSEDED | Superseded | Pending | 3 |
| LOV-LOAD-STATUS | RUNNING | Running | Pending | 1 |
| LOV-LOAD-STATUS | COMPLETED | Completed | Pending | 2 |
| LOV-LOAD-STATUS | REFUSED | Refused | Pending | 3 |
| LOV-LOAD-STATUS | LATE | Late | Pending | 4 |
| LOV-LOAD-STATUS | FAILED | Failed | Pending | 5 |
| LOV-LOAD-STATUS | SUPERSEDED | Superseded | Pending | 6 |
| LOV-DQ-STATUS | OPEN | Open | Pending | 1 |
| LOV-DQ-STATUS | CLEARED | Cleared | Pending | 2 |
| LOV-DQ-RULE-TYPE | NOT_NULL | Not null | Pending | 1 |
| LOV-DQ-RULE-TYPE | UNIQUE_ACROSS | Unique across | Pending | 2 |
| LOV-DQ-RULE-TYPE | RANGE | Range | Pending | 3 |
| LOV-DQ-RULE-TYPE | SUM_EQUALS | Sum equals | Pending | 4 |
| LOV-DQ-RULE-TYPE | EXISTS_LINK | Exists link | Pending | 5 |
| LOV-DQ-RULE-TYPE | MAX_AGE_DAYS | Max age days | Pending | 6 |
| LOV-DQ-RULE-TYPE | FIELD_BEFORE | Field before | Pending | 7 |
| LOV-TRACKER-LOCATION | EXCEL | Excel | Pending | 1 |
| LOV-TRACKER-LOCATION | SHAREPOINT | SharePoint | Pending | 2 |
| LOV-TRACKER-LOCATION | LOCAL_FILE | Local file | Pending | 3 |
| LOV-TRACKER-LOCATION | NONE | None | Pending | 4 |
| LOV-UPDATE-CYCLE | DAILY | Daily | Pending | 1 |
| LOV-UPDATE-CYCLE | WEEKLY | Weekly | Pending | 2 |
| LOV-UPDATE-CYCLE | MONTHLY | Monthly | Pending | 3 |
| LOV-UPDATE-CYCLE | AD_HOC | Ad hoc | Pending | 4 |
| LOV-TRACKER-DECISION | LOAD | Load | Pending | 1 |
| LOV-TRACKER-DECISION | RETIRE | Retire | Pending | 2 |
| LOV-TRACKER-DECISION | KEEP | Keep | Pending | 3 |
| LOV-TRACKER-STATUS | LISTED | Listed | Pending | 1 |
| LOV-TRACKER-STATUS | LOADED | Loaded | Pending | 2 |
| LOV-TRACKER-STATUS | SIGNED_OFF | Signed off | Pending | 3 |
| LOV-TRACKER-STATUS | RETIRED | Retired | Pending | 4 |
| LOV-TRACKER-STATUS | KEPT | Kept | Pending | 5 |
| LOV-PUBLISH-STATUS | PENDING | Pending | Pending | 1 |
| LOV-PUBLISH-STATUS | HELD | Held | Pending | 2 |
| LOV-PUBLISH-STATUS | RELEASED | Released | Pending | 3 |
| LOV-REC-RESULT | PASS | Pass | Pending | 1 |
| LOV-REC-RESULT | BREAK | Break | Pending | 2 |
| LOV-RETENTION-END | ARCHIVE | Archive | Pending | 1 |
| LOV-RETENTION-END | REVIEW | Review | Pending | 2 |
| LOV-TRANSPORT | SFTP | SFTP | Pending | 1 |
| LOV-TRANSPORT | COLLINS | COLLINS | Pending | 2 |
| LOV-INTERFACE-RUN | RECEIVED | Received | Pending | 1 |
| LOV-INTERFACE-RUN | LOADED | Loaded | Pending | 2 |
| LOV-INTERFACE-RUN | REFUSED | Refused | Pending | 3 |
| LOV-INTERFACE-RUN | MISSING | Missing | Pending | 4 |
| LOV-INTERFACE-RUN | DUPLICATE | Duplicate | Pending | 5 |
| LOV-INTERFACE-RUN | FAILED | Failed | Pending | 6 |
| LOV-OUTBOUND-STATUS | PENDING | Pending | Pending | 1 |
| LOV-OUTBOUND-STATUS | SENT | Sent | Pending | 2 |
| LOV-OUTBOUND-STATUS | RETRY | Retry | Pending | 3 |
| LOV-OUTBOUND-STATUS | EXCEPTION | Exception | Pending | 4 |
| LOV-OUTBOUND-STATUS | ACKNOWLEDGED | Acknowledged | Pending | 5 |
| LOV-OUTBOX-DELIVERY | PENDING | Pending | Pending | 1 |
| LOV-OUTBOX-DELIVERY | RETRYING | Retrying | Pending | 2 |
| LOV-OUTBOX-DELIVERY | DELIVERED | Delivered | Pending | 3 |
| LOV-OUTBOX-DELIVERY | EXCEPTION | Exception | Pending | 4 |
| LOV-ENVIRONMENT | DEV | DEV | Pending | 1 |
| LOV-ENVIRONMENT | SIT | SIT | Pending | 2 |
| LOV-ENVIRONMENT | UAT | UAT | Pending | 3 |
| LOV-ENVIRONMENT | PROD | PROD | Pending | 4 |
| LOV-PRODUCT-STATUS | ACTIVE | Active | Pending | 1 |
| LOV-PRODUCT-STATUS | DELINQUENT | Delinquent | Pending | 2 |
| LOV-PRODUCT-STATUS | CLOSED | Closed | Pending | 3 |
| LOV-PRODUCT-STATUS | WRITTEN_OFF | Written off | Pending | 4 |
| LOV-EXCLUSION-REASON | DECEASED | Deceased | Pending | 1 |
| LOV-EXCLUSION-REASON | FRAUD | Fraud | Pending | 2 |
| LOV-EXCLUSION-REASON | BANKRUPTCY | Bankruptcy | Pending | 3 |
| LOV-EXCLUSION-REASON | ACTIVE_PLAN | Active plan | Pending | 4 |
| LOV-EXCLUSION-REASON | OPEN_DISPUTE | Open dispute | Pending | 5 |
| LOV-SNAPSHOT-STATUS | TAKEN | Taken | Pending | 1 |
| LOV-SNAPSHOT-STATUS | PUBLISHED | Published | Pending | 2 |
| LOV-SNAPSHOT-STATUS | HELD | Held | Pending | 3 |
| LOV-PARAM-SCOPE | PRODUCT | Product | Pending | 1 |
| LOV-PARAM-SCOPE | GLOBAL | Global | Pending | 2 |
| LOV-VERSION-STATUS | VALIDATED | Validated | Pending | 1 |
| LOV-VERSION-STATUS | APPROVED | Approved | Pending | 2 |
| LOV-VERSION-STATUS | IN_FORCE | In force | Pending | 3 |
| LOV-VERSION-STATUS | SUPERSEDED | Superseded | Pending | 4 |
| LOV-VERSION-STATUS | ROLLED_BACK | Rolled back | Pending | 5 |
| LOV-VERSION-STATUS | REFUSED | Refused | Pending | 6 |
| LOV-TEST-RESULT | PASSED | Passed | Pending | 1 |
| LOV-TEST-RESULT | FAILED | Failed | Pending | 2 |
| LOV-REF-TABLE | PRODUCT | Product | Pending | 1 |
| LOV-REF-TABLE | REGION | Region | Pending | 2 |
| LOV-REF-TABLE | EXPOSURE_BAND | Exposure band | Pending | 3 |
| LOV-REF-TABLE | ROLE | Role | Pending | 4 |
| LOV-REF-TABLE | TEAM | Team | Pending | 5 |
| LOV-REF-TABLE | QUEUE | Queue | Pending | 6 |
| LOV-REF-TABLE | QUEUE_MEMBER | Queue member | Pending | 7 |
| LOV-REF-TABLE | SERVICE_LEVEL | Service level | Pending | 8 |
| LOV-REF-TABLE | DOCUMENT_TYPE | Document type | Pending | 9 |
| LOV-REF-TABLE | DOCUMENT_CHECKLIST | Document checklist | Pending | 10 |
| LOV-REF-TABLE | RETENTION_CLASS | Retention class | Pending | 11 |
| LOV-REF-TABLE | TEMPLATE | Template | Pending | 12 |
| LOV-REF-TABLE | DELEGATION_LIMIT | Delegation limit | Pending | 13 |
| LOV-REF-TABLE | PERMISSION | Permission | Pending | 14 |
| LOV-REF-TABLE | MASKING_RULE | Masking rule | Pending | 15 |
| LOV-REF-TABLE | PARTNER_USER | Partner user | Pending | 16 |
| LOV-REF-TABLE | LEGAL_PERIOD | Legal period | Pending | 17 |
| LOV-REF-TABLE | HOLIDAY | Holiday | Pending | 18 |
| LOV-REF-TABLE | PRODUCT_PARAMETER | Product parameter | Pending | 19 |
| LOV-REF-TABLE | PARAMETER | Parameter | Pending | 20 |
| LOV-REF-TABLE | ENTRY | Entry | Pending | 21 |
| LOV-REF-TABLE | EXCLUSION | Exclusion | Pending | 22 |
| LOV-REF-TABLE | ALLOCATION | Allocation | Pending | 23 |
| LOV-REF-TABLE | ASSIGNMENT | Assignment | Pending | 24 |
| LOV-REF-TABLE | TRANSFER | Transfer | Pending | 25 |
| LOV-RULE-TABLE | ENTRY | Entry | Pending | 1 |
| LOV-RULE-TABLE | EXCLUSION | Exclusion | Pending | 2 |
| LOV-RULE-TABLE | ALLOCATION | Allocation | Pending | 3 |
| LOV-RULE-TABLE | ASSIGNMENT | Assignment | Pending | 4 |
| LOV-RULE-TABLE | TRANSFER | Transfer | Pending | 5 |
| LOV-TRANSFER-REASON | R01 | Capacity | Pending | 1 |
| LOV-TRANSFER-REASON | R02 | Customer deceased | Pending | 2 |
| LOV-TRANSFER-REASON | R03 | Skill | Pending | 3 |
| LOV-TRANSFER-REASON | R04 | Owner absent | Pending | 4 |
| LOV-TRANSFER-REASON | R05 | Legal referral | Pending | 5 |
| LOV-TRANSFER-REASON | R06 | Wrong queue | Pending | 6 |
| LOV-PLAN-STATUS | CREATED | Created | Pending | 1 |
| LOV-PLAN-STATUS | APPROVED | Approved | Pending | 2 |
| LOV-PLAN-STATUS | BOOKED | Booked | Pending | 3 |
| LOV-PLAN-STATUS | BROKEN | Broken | Pending | 4 |
| LOV-LEDGER-EVENT | CONTACT | Contact | Pending | 1 |
| LOV-LEDGER-EVENT | LETTER | Letter | Pending | 2 |
| LOV-LEDGER-EVENT | PROMISE | Promise | Pending | 3 |
| LOV-LEDGER-EVENT | PAYMENT | Payment | Pending | 4 |
| LOV-LEDGER-EVENT | HANDOVER | Handover | Pending | 5 |
| LOV-LEDGER-EVENT | CASE_CREATED | Case created | Pending | 6 |
| LOV-LEDGER-EVENT | CASE_ALLOCATED | Case allocated | Pending | 7 |
| LOV-LEDGER-EVENT | CASE_TRANSFERRED | Case transferred | Pending | 8 |
| LOV-LEDGER-EVENT | CASE_ESCALATED | Case escalated | Pending | 9 |
| LOV-LEDGER-EVENT | DOCUMENT_ATTACHED | Document attached | Pending | 10 |
| LOV-LEDGER-EVENT | DECISION_TAKEN | Decision taken | Pending | 11 |
| LOV-LEDGER-EVENT | CORRECTION | Correction | Pending | 12 |
| LOV-LEDGER-EVENT | PARTNER_RESULT | Partner result | Pending | 13 |
| LOV-LEDGER-EVENT | OFFER | Offer | Pending | 14 |
| LOV-ACTOR-TYPE | USER | User | Pending | 1 |
| LOV-ACTOR-TYPE | SERVICE | Service | Pending | 2 |
| LOV-ACTOR-TYPE | PARTNER | Partner | Pending | 3 |
| LOV-SEND-STATUS | SENT | Sent | Pending | 1 |
| LOV-SEND-STATUS | DELIVERED | Delivered | Pending | 2 |
| LOV-SEND-STATUS | READ | Read | Pending | 3 |
| LOV-SEND-STATUS | FAILED | Failed | Pending | 4 |
| LOV-CAPTURE-KIND | PHOTO | Photo | Pending | 1 |
| LOV-CAPTURE-KIND | BILL | Bill | Pending | 2 |
| LOV-CAPTURE-KIND | CHECKLIST | Checklist | Pending | 3 |
| LOV-SCAN-RESULT | CLEAN | Clean | Pending | 1 |
| LOV-SCAN-RESULT | INFECTED | Infected | Pending | 2 |
| LOV-OCR-STATUS | PENDING | Pending | Pending | 1 |
| LOV-OCR-STATUS | DONE | Done | Pending | 2 |
| LOV-OCR-STATUS | RESCAN | Rescan | Pending | 3 |
| LOV-OCR-STATUS | FAILED | Failed | Pending | 4 |
| LOV-INTAKE-MATCH | PENDING | Pending | Pending | 1 |
| LOV-INTAKE-MATCH | MATCHED | Matched | Pending | 2 |
| LOV-INTAKE-MATCH | NO_MATCH | No match | Pending | 3 |
| LOV-INTAKE-MATCH | MULTIPLE | Multiple | Pending | 4 |
| LOV-INTAKE-MATCH | CONFLICT | Conflict | Pending | 5 |
| LOV-INTAKE-MATCH | CASE_CLOSED | Case closed | Pending | 6 |
| LOV-INTAKE-MATCH | NO_TYPE | No type | Pending | 7 |
| LOV-EXTRACT-STATUS | PENDING | Pending | Pending | 1 |
| LOV-EXTRACT-STATUS | DONE | Done | Pending | 2 |
| LOV-EXTRACT-STATUS | FAILED | Failed | Pending | 3 |
| LOV-INTAKE-REVIEW | RESCAN | Rescan | Pending | 1 |
| LOV-INTAKE-REVIEW | UNREADABLE_FILE | Unreadable file | Pending | 2 |
| LOV-INTAKE-REVIEW | LOW_CONFIDENCE | Low confidence | Pending | 3 |
| LOV-INTAKE-REVIEW | MODEL_UNAVAILABLE | Model unavailable | Pending | 4 |
| LOV-INTAKE-REVIEW | UNKNOWN_TYPE | Unknown type | Pending | 5 |
| LOV-INTAKE-OUTCOME | ATTACHED | Attached | Pending | 1 |
| LOV-INTAKE-OUTCOME | DISCARDED | Discarded | Pending | 2 |
| LOV-RETENTION-ACTION | ARCHIVED | Archived | Pending | 1 |
| LOV-RETENTION-ACTION | LISTED | Listed | Pending | 2 |
| LOV-RETENTION-ACTION | HELD | Held | Pending | 3 |
| LOV-RETENTION-ACTION | EXCEPTION | Exception | Pending | 4 |
| LOV-SIGN-METHOD | E_SIGNATURE | E-signature | Pending | 1 |
| LOV-SIGN-METHOD | BRANCH | Branch | Pending | 2 |
| LOV-SIGN-METHOD | PAPER | Paper | Pending | 3 |
| LOV-SIGN-STATUS | QUEUED | Queued | Pending | 1 |
| LOV-SIGN-STATUS | SENT | Sent | Pending | 2 |
| LOV-SIGN-STATUS | SIGNED | Signed | Pending | 3 |
| LOV-SIGN-STATUS | DECLINED | Declined | Pending | 4 |
| LOV-SIGN-STATUS | EXPIRED | Expired | Pending | 5 |
| LOV-SIGNATURE-BASIS | E_SIGNATURE_ALLOWED | E-signature allowed | Pending | 1 |
| LOV-SIGNATURE-BASIS | WET_INK_REQUIRED | Wet ink required | Pending | 2 |
| LOV-TRT-SIGNATURE | PENDING | Pending | Pending | 1 |
| LOV-TRT-SIGNATURE | SIGNED | Signed | Pending | 2 |
| LOV-TRT-SIGNATURE | NOT_SIGNED | Not signed | Pending | 3 |
| LOV-CREDIT-RESULT | APPROVED | Approved | Pending | 1 |
| LOV-CREDIT-RESULT | REFUSED | Refused | Pending | 2 |
| LOV-APPROVAL-STATUS | WAITING | Waiting | Pending | 1 |
| LOV-APPROVAL-STATUS | HELD_NO_LIMIT | Held, no limit | Pending | 2 |
| LOV-APPROVAL-STATUS | APPROVED | Approved | Pending | 3 |
| LOV-APPROVAL-STATUS | REFUSED | Refused | Pending | 4 |
| LOV-APPROVAL-STATUS | RETURNED | Returned | Pending | 5 |
| LOV-MATCH-TYPE | EXACT | Exact | Pending | 1 |
| LOV-MATCH-TYPE | WINDOW | Window | Pending | 2 |
| LOV-MATCH-TYPE | PARTIAL | Partial | Pending | 3 |
| LOV-MEASURE-UNIT | COUNT | Count | Pending | 1 |
| LOV-MEASURE-UNIT | THB | Baht | Pending | 2 |
| LOV-MEASURE-UNIT | DAYS | Days | Pending | 3 |
| LOV-MEASURE-UNIT | PERCENT | Percent | Pending | 4 |
| LOV-MEASURE-DIM | ROUTE | Route | Pending | 1 |
| LOV-MEASURE-DIM | AGE_BAND | Age band | Pending | 2 |
| LOV-MEASURE-DIM | QUEUE | Queue | Pending | 3 |
| LOV-MEASURE-DIM | STAGE | Stage | Pending | 4 |
| LOV-MEASURE-DIM | AGENT | Agent | Pending | 5 |
| LOV-MEASURE-PUBLISH | PUBLISHED | Published | Pending | 1 |
| LOV-MEASURE-PUBLISH | HELD | Held | Pending | 2 |
| LOV-AGENT | INTAKE | Intake | Pending | 1 |
| LOV-AGENT | SCREENING | Screening | Pending | 2 |
| LOV-AGENT | LEGAL_DOC | Legal doc | Pending | 3 |
| LOV-AGENT | EXTRACT | Extract | Pending | 4 |
| LOV-AGENT | TDR_OFFER | Tdr offer | Pending | 5 |
| LOV-AUTONOMY | OFF | Off | Pending | 1 |
| LOV-AUTONOMY | SHADOW | Shadow | Pending | 2 |
| LOV-AUTONOMY | L1 | L1 | Pending | 3 |
| LOV-CONFIG-STATUS | LOADED | Loaded | Pending | 1 |
| LOV-CONFIG-STATUS | APPROVED | Approved | Pending | 2 |
| LOV-CONFIG-STATUS | RETIRED | Retired | Pending | 3 |
| LOV-AGENT-RUN | ANSWERED | Answered | Pending | 1 |
| LOV-AGENT-RUN | TIMED_OUT | Timed out | Pending | 2 |
| LOV-AGENT-RUN | GUARDRAIL_FAILED | Guardrail failed | Pending | 3 |
| LOV-AGENT-RUN | BELOW_FLOOR | Below floor | Pending | 4 |
| LOV-AGENT-RUN | TOOL_UNAVAILABLE | Tool unavailable | Pending | 5 |
| LOV-AGENT-RUN | MODEL_ERROR | Model error | Pending | 6 |
| LOV-AGENT-RUN | DISABLED | Disabled | Pending | 7 |
| LOV-SUBJECT-TYPE | CASE | Case | Pending | 1 |
| LOV-SUBJECT-TYPE | DOCUMENT | Document | Pending | 2 |
| LOV-SUBJECT-TYPE | LEGAL_ACTION | Legal action | Pending | 3 |
| LOV-EVAL-STATUS | RUNNING | Running | Pending | 1 |
| LOV-EVAL-STATUS | DONE | Done | Pending | 2 |
| LOV-EVAL-STATUS | FAILED | Failed | Pending | 3 |
| LOV-EXTRACT-APPROACH | AGENT | Agent | Pending | 1 |
| LOV-EXTRACT-APPROACH | OCR_TEMPLATE | OCR template | Pending | 2 |
| LOV-EXTRACT-APPROACH | MODEL | Model | Pending | 3 |
| LOV-EXTRACT-APPROACH | OCR_AND_MODEL | OCR and model | Pending | 4 |
| LOV-FEEDBACK | ACCEPTED | Accepted | Pending | 1 |
| LOV-FEEDBACK | CORRECTED | Corrected | Pending | 2 |
| LOV-FEEDBACK | REJECTED | Rejected | Pending | 3 |
| LOV-AGENT-ALERT | COST_CAP | Cost cap | Pending | 1 |
| LOV-AGENT-ALERT | DRIFT | Drift | Pending | 2 |

## Loaded lists

| Lists loaded from data |  |  |
|---|---|---|
| 14 lists whose values come from a source system or another reference table rather than a closed set. |  |  |
| List | Where the values come from | Used by |
| LOV-ACTION-CODE | EFS action codes, 1,106 values loaded from EFS | interaction.action_code, case_list_row.last_action_code, collections_history.action_code, efs_ledger_outcome.action_code |
| LOV-BU | Business units, loaded from the core | loan_account.business_unit |
| LOV-BUCKET | Arrears buckets as reported by collections | loan_account.bucket |
| LOV-CLASS | BOT loan classification and stages | loan_account.classification |
| LOV-DECISION | D1 to D9 with sub-decisions, X1 to X7 | decision_log_entry.decision_code, delegation_limit.decision_code, approval.decision_code |
| LOV-DOC-TYPE | Document types from the document checklist | document.document_type, document_checklist_item.document_type, document_intake.predicted_type |
| LOV-EXPOSURE | Exposure bands, set by the center of excellence | recovery_case.exposure_band |
| LOV-PAY-CHANNEL | Payment channels, loaded from the core | account_payment.payment_channel |
| LOV-PRODUCT-CODE | Core bank product codes, loaded from the core | loan_account.product_code |
| LOV-PROVINCE | The 77 provinces of Thailand | collateral.province |
| LOV-REGION | Regions, from the organization structure | recovery_case.region_code, agent_policy.segment_region_code, agent_run.segment_region_code |
| LOV-RETENTION | Retention classes from the bank retention schedule | interaction.retention_class, document.retention_class, document_type.retention_class |
| LOV-ROLE | The 54 roles in the roles table | recovery_case.next_action_owner_role, queue.role_code, task.owner_role, timer.escalated_to_role, rule_row.owner_role, data_product.owner_role, data_product_access.role_code, sys_fields.owner_role, interface_config.owner_role, interface_config.alert_role, outbound_item.owner_role, job_catalog.owner_role, parameter_catalog.owner_role, rule_test_case.expected_owner_role, masking_rule.role_code, role_conflict.role_code, partner_user.role_code, approval.route_role_code, agent_policy.alert_role, agent_alert.sent_to_role |
| LOV-TEAM | Teams, from the organization structure | recovery_case.team_code, queue.team_code, tracker_inventory.team_code, case_list_row.team_code |

## Relationships

| Relationships |  |  |  |  |
|---|---|---|---|---|
| 119 references between entities, each held as a CROSS_REF field, as in bank TSD section T3.3. |  |  |  |  |
| Entity | Field | Refers to | Cardinality | Mandatory |
| recovery_case | primary_customer_id | party | N:1 | Yes |
| recovery_case | queue_id | queue | N:0..1 | No |
| case_account | case_id | recovery_case | N:1 | Yes |
| case_account | account_id | loan_account | N:1 | Yes |
| case_party | case_id | recovery_case | N:1 | Yes |
| case_party | party_id | party | N:1 | Yes |
| deviation | case_id | recovery_case | N:1 | Yes |
| queue | overflow_queue_id | queue | N:0..1 | No |
| assignment | case_id | recovery_case | N:1 | Yes |
| assignment | task_id | task | N:0..1 | No |
| assignment | queue_id | queue | N:0..1 | No |
| task | case_id | recovery_case | N:1 | Yes |
| timer | case_id | recovery_case | N:1 | Yes |
| timer | task_id | task | N:0..1 | No |
| timer | treatment_id | treatment | N:0..1 | No |
| contact_point | party_id | party | N:1 | Yes |
| account_payment | account_id | loan_account | N:1 | Yes |
| account_collateral | account_id | loan_account | N:1 | Yes |
| account_collateral | collateral_id | collateral | N:1 | Yes |
| valuation | collateral_id | collateral | N:0..1 | No |
| valuation | asset_id | asset | N:0..1 | No |
| valuation | valuer_partner_id | partner | N:0..1 | No |
| asset | case_id | recovery_case | N:0..1 | No |
| asset | collateral_id | collateral | N:0..1 | No |
| treatment | case_id | recovery_case | N:1 | Yes |
| treatment | decision_log_id | decision_log_entry | N:0..1 | No |
| guarantee_claim | case_id | recovery_case | N:1 | Yes |
| legal_action | case_id | recovery_case | N:1 | Yes |
| legal_action | law_firm_id | partner | N:0..1 | No |
| notice | case_id | recovery_case | N:1 | Yes |
| notice | document_id | document | N:0..1 | No |
| notice | party_id | party | N:0..1 | No |
| notice | template_id | template | N:0..1 | No |
| notice | dispatch_file_id | outbound_item | N:0..1 | No |
| hearing | legal_action_id | legal_action | N:1 | Yes |
| partner_instruction | case_id | recovery_case | N:1 | Yes |
| partner_instruction | partner_id | partner | N:1 | Yes |
| listing | asset_id | asset | N:1 | Yes |
| asset_sale | asset_id | asset | N:1 | Yes |
| asset_sale | listing_id | listing | N:0..1 | No |
| debt_sale_lot | buyer_partner_id | partner | N:0..1 | No |
| debt_sale_account | lot_id | debt_sale_lot | N:1 | Yes |
| debt_sale_account | account_id | loan_account | N:1 | Yes |
| interaction | case_id | recovery_case | N:1 | Yes |
| interaction | party_id | party | N:0..1 | No |
| interaction | decision_log_id | decision_log_entry | N:0..1 | No |
| interaction | corrects_entry_id | interaction | N:0..1 | No |
| interaction | contact_point_id | contact_point | N:0..1 | No |
| interaction | treatment_id | treatment | N:0..1 | No |
| interaction | proceeds_id | proceeds | N:0..1 | No |
| document | case_id | recovery_case | N:1 | Yes |
| document | party_id | party | N:0..1 | No |
| document | previous_version_id | document | N:0..1 | No |
| document | template_id | template | N:0..1 | No |
| document | treatment_id | treatment | N:0..1 | No |
| document_field | document_id | document | N:1 | Yes |
| document_custody | document_id | document | N:1 | Yes |
| decision_log_entry | case_id | recovery_case | N:0..1 | No |
| decision_log_entry | corrects_entry_id | decision_log_entry | N:0..1 | No |
| score | account_id | loan_account | N:0..1 | No |
| score | case_id | recovery_case | N:0..1 | No |
| proceeds | case_id | recovery_case | N:1 | Yes |
| proceeds | treatment_id | treatment | N:0..1 | No |
| proceeds | account_payment_id | account_payment | N:0..1 | No |
| write_off | case_id | recovery_case | N:1 | Yes |
| write_off | decision_log_id | decision_log_entry | N:0..1 | No |
| permission | role_id | role | N:1 | Yes |
| load_run | interface_run_id | interface_run | N:0..1 | No |
| load_run | tracker_id | tracker_inventory | N:0..1 | No |
| dq_exception | load_run_id | load_run | N:1 | Yes |
| tracker_inventory | last_load_run_id | load_run | N:0..1 | No |
| tracker_row | tracker_id | tracker_inventory | N:1 | Yes |
| tracker_row | load_run_id | load_run | N:1 | Yes |
| case_list_row | case_id | recovery_case | N:1 | Yes |
| case_list_row | account_id | loan_account | N:1 | Yes |
| retention_rule | reference_version_id | reference_version | N:0..1 | No |
| dp_treatment | treatment_id | treatment | N:1 | Yes |
| dp_treatment | case_id | recovery_case | N:1 | Yes |
| dp_treatment | decision_log_id | decision_log_entry | N:0..1 | No |
| dp_guarantee_claim | guarantee_claim_id | guarantee_claim | N:1 | Yes |
| dp_guarantee_claim | case_id | recovery_case | N:1 | Yes |
| processed_event | event_id | outbox_event | N:0..1 | No |
| outbox_event | case_id | recovery_case | N:0..1 | No |
| outbox_delivery | event_id | outbox_event | N:1 | Yes |
| outbox_delivery | task_id | task | N:0..1 | No |
| party_product | party_id | party | N:1 | Yes |
| case_entry_exclusion | account_id | loan_account | N:1 | Yes |
| queue_member | queue_id | queue | N:1 | Yes |
| queue_measure | queue_id | queue | N:1 | Yes |
| reference_row | version_id | reference_version | N:1 | Yes |
| partner_user | partner_id | partner | N:1 | Yes |
| document_type | reference_version_id | reference_version | N:0..1 | No |
| document_checklist_item | reference_version_id | reference_version | N:0..1 | No |
| case_document_check | case_id | recovery_case | N:1 | Yes |
| case_document_check | last_event_id | outbox_event | N:0..1 | No |
| document_hub_parameter | reference_version_id | reference_version | N:0..1 | No |
| document_intake | partner_id | partner | N:0..1 | No |
| document_intake | run_id | load_run | N:0..1 | No |
| document_intake | case_id | recovery_case | N:0..1 | No |
| document_intake | document_id | document | N:0..1 | No |
| document_text | intake_id | document_intake | N:1 | Yes |
| document_text | document_id | document | N:0..1 | No |
| retention_action | document_id | document | N:1 | Yes |
| retention_action | decision_log_id | decision_log_entry | N:0..1 | No |
| signature_request | case_id | recovery_case | N:1 | Yes |
| signature_request | treatment_id | treatment | N:0..1 | No |
| signature_request | document_id | document | N:1 | Yes |
| signature_request | party_id | party | N:1 | Yes |
| signature_request | signed_document_id | document | N:0..1 | No |
| approval | case_id | recovery_case | N:1 | Yes |
| approval | delegation_limit_id | delegation_limit | N:0..1 | No |
| approval | decision_log_id | decision_log_entry | N:0..1 | No |
| agent_policy | evaluation_run_id | agent_evaluation_run | N:0..1 | No |
| agent_run | case_id | recovery_case | N:0..1 | No |
| agent_run | evaluation_run_id | agent_evaluation_run | N:0..1 | No |
| agent_run | decision_log_id | decision_log_entry | N:0..1 | No |
| agent_evaluation | evaluation_run_id | agent_evaluation_run | N:1 | Yes |
| agent_feedback | agent_run_id | agent_run | N:1 | Yes |
| agent_feedback | decision_log_id | decision_log_entry | N:0..1 | No |

## Sources

| Fields by source system |  |  |  |
|---|---|---|---|
| Where each field comes from and how it reaches the Workbench. Counts are of fields, not records. |  |  |  |
| Source system | How it reaches the Workbench | Fields | Entities |
| Workbench | Written by the Workbench | 1123 | account_collateral, account_payment, agent_alert, agent_evaluation, agent_evaluation_run, agent_feedback, agent_policy, agent_prompt, agent_run, agent_sample, approval, asset, asset_sale, assignment, case_account, case_document_check, case_entry_exclusion, case_list_row, case_party, collateral, collections_history, contact_point, data_contract, data_product, data_product_access, data_product_load, debt_sale_account, debt_sale_lot, decision_log_entry, delegation_limit, deviation, document, document_checklist_item, document_custody, document_field, document_hub_parameter, document_intake, document_text, document_type, dp_guarantee_claim, dp_treatment, dq_exception, dq_rule, efs_ledger_outcome, feature_flag, feature_flag_change, guarantee_claim, hearing, idempotency_key, interaction, interface_config, interface_run, interface_signoff, job_catalog, lake_copy_watermark, legal_action, listing, load_run, loan_account, lov_value, masking_rule, measure_definition, measure_publish, measure_snapshot, merge_field, notice, outbound_item, outbox_delivery, outbox_event, parameter_catalog, parameter_value, partner, partner_instruction, partner_user, party, party_product, payment_match_rule, permission, proceeds, processed_event, queue, queue_measure, queue_member, reconciliation_result, recovery_case, reference_row, reference_version, retention_action, retention_rule, role, role_conflict, rule_row, rule_test_case, score, signature_request, source_code_map, source_field_map, sys_field_version, sys_fields, sys_objects, task, template, timer, tracker_inventory, tracker_row, treatment, valuation, write_off |
| Core bank (ALS) via COLLINS | COLLINS daily batch | 36 | account_payment, debt_sale_account, dp_treatment, loan_account, proceeds, recovery_case, treatment |
| AMIS | File load, monthly | 15 | asset, asset_sale |
| SCBPDM via COLLINS | COLLINS daily batch | 13 | contact_point, party, party_product |
| EFS via COLLINS | COLLINS daily batch | 11 | collections_history, interaction, loan_account |
| CCMS | File load, weekly | 11 | account_collateral, collateral |
| LIT | COLLINS daily batch for status; partner portal for court events | 11 | hearing, legal_action |
| COLLINS | COLLINS daily batch | 7 | decision_log_entry, score |
| SVAF | File load, weekly | 5 | valuation |
| WIN | File load, weekly | 5 | notice |
| GL | File load, monthly | 5 | write_off |
| ACE | ACE restructure calculation | 4 | recovery_case, treatment |
| NLEADS |  | 4 | treatment |
| RPS | File load, weekly | 2 | asset |
| Aric via COLLINS |  | 1 | party |
| LIT via COLLINS | COLLINS daily batch | 1 | legal_action |
| Entra ID | Sign-in | 1 | role |
| EasyApp |  | 1 | signature_request |

## Key

| Key |  |  |
|---|---|---|
| What each column, value and code means. |  |  |
| Item | Term | Meaning |
| Column | BR Field ID | DF, the subject area code and a number, as in bank TSD section T3.1 |
| Column | Data type | The TSD data type: TEXT, NUMBER, DATE, BOOLEAN, LOV, USER_REF, CROSS_REF, FORMULA or ATTACHMENT |
| Column | Physical type | The PostgreSQL type in the ACE database |
| Column | Length | Characters for text; precision and scale for numbers |
| Column | Source field | The field name in the source system or the bank file that carries it today |
| Column | Personal data | Yes where the field identifies or describes a person. Masked unless the role is allowed to see it |
| Value | PK | Primary key |
| Value | UK | Unique key, alone or with the other UK fields of the entity |
| Value | FK | Reference to another entity |
| Value | N:1 | Many records refer to exactly one record |
| Value | N:0..1 | Many records refer to one record or to none |
| Value | None | No value applies |
| Value | Pending | Thai label not yet approved |
| Subject area code | CAS | Case |
| Subject area code | WRK | Work management |
| Subject area code | PTY | Party |
| Subject area code | ACC | Account and arrears |
| Subject area code | COL | Collateral and asset |
| Subject area code | TRT | Treatment |
| Subject area code | LEG | Legal |
| Subject area code | PRT | Partner |
| Subject area code | SAL | Disposal and debt sale |
| Subject area code | INT | Interaction |
| Subject area code | DOC | Document |
| Subject area code | DEC | Decision and control |
| Subject area code | FIN | Money and closure |
| Subject area code | REF | Reference and access |
| Subject area code | OPS | Loads and operations |
| Subject area code | AGT | Agent runtime |
| Subject area code | RPT | Reporting |

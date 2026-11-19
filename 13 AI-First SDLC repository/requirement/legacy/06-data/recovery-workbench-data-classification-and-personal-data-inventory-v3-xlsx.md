<!-- source: 06 Data/Recovery Workbench Data Classification and Personal Data Inventory v3.xlsx -->
<!-- converted: 2026-11-04 from XLSX -->

> **Source:** `06 Data/Recovery Workbench Data Classification and Personal Data Inventory v3.xlsx`  
> **Converted from:** XLSX

## Fields

| Every field, classified |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|
| 1256 fields. Each carries a personal data category, a classification and a handling rule. Classes are proposed until the bank scheme is applied (DL26). |  |  |  |  |  |  |  |  |  |
| BR Field ID | Entity | Field | Personal data category | Classification | Personal data | On screen | Lawful basis, proposed | Retention | Meaning |
| DF-CAS-001 | recovery_case | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the case |
| DF-CAS-002 | recovery_case | case_no | Indirect identifier | Confidential | Yes | Shown within the role's scope; masked in UAT | Contract (PDPA section 24) | Per data product (DL26) | Case number RW-YYYY-NNNNNN, issued at creation and never reused |
| DF-CAS-003 | recovery_case | product_group | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Mortgage, hire purchase, SSME or unsecured |
| DF-CAS-004 | recovery_case | primary_customer_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The borrower the case is opened for |
| DF-CAS-005 | recovery_case | status | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed |
| DF-CAS-006 | recovery_case | stage_code | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | The stage the case is on |
| DF-CAS-007 | recovery_case | route_state | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | The routing state from the rule set, for example FIRM_INSTRUCTED |
| DF-CAS-008 | recovery_case | route_code | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | The approved route R1 to R8 |
| DF-CAS-009 | recovery_case | owner_user_id | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | The case owner |
| DF-CAS-010 | recovery_case | queue_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The queue the case is in |
| DF-CAS-011 | recovery_case | team_code | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | The owning team, used by scope rules |
| DF-CAS-012 | recovery_case | region_code | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | The owning region, used by scope rules |
| DF-CAS-013 | recovery_case | entry_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | The date the case entered recovery |
| DF-CAS-014 | recovery_case | dpd_at_entry | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Days past due on the entry date |
| DF-CAS-015 | recovery_case | exposure_band | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Exposure band set from the outstanding balance at entry |
| DF-CAS-016 | recovery_case | total_outstanding_at_entry | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Total outstanding across linked accounts at entry, in baht |
| DF-CAS-017 | recovery_case | prescription_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | The earliest date a legal claim on the case expires |
| DF-CAS-018 | recovery_case | stage_clock_start | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When the current state started, for the service level |
| DF-CAS-019 | recovery_case | deviation_open | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | True while any deviation X1 to X7 is open |
| DF-CAS-020 | recovery_case | legal_hold | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | True while a legal hold stops normal routing |
| DF-CAS-021 | recovery_case | rule_version | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | The rule version the current state was entered under |
| DF-CAS-022 | recovery_case | closed_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | The date the case closed |
| DF-CAS-023 | recovery_case | closure_reason | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Cured, settled, realized, sold, written off, insurance settled, merged, canceled |
| DF-CAS-046 | recovery_case | plan_ref | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Reference of the ACE restructure plan on the case |
| DF-CAS-047 | recovery_case | plan_status | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | ACE plan status: created, approved, booked or broken |
| DF-CAS-048 | recovery_case | plan_status_as_of | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Date of the plan status in ACE |
| DF-CAS-049 | recovery_case | next_action_text | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | The next action, copied from action_text of the rule that moved the case |
| DF-CAS-050 | recovery_case | next_action_owner_role | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Owner role of the next action, from owner_role of the rule |
| DF-CAS-051 | recovery_case | next_action_due_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Due date from the rule's timer_spec or the service levels and timers table |
| DF-CAS-052 | recovery_case | next_action_rule_id | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Rule ID that set the next action |
| DF-CAS-053 | recovery_case | next_action_waiting | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | True when the next action waits on a customer, party or partner |
| DF-CAS-054 | recovery_case | last_allocation_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Business date of the last allocation run that decided the case |
| DF-CAS-055 | recovery_case | status_before_hold | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | The case status when a legal hold was placed, restored when it is lifted |
| DF-CAS-024 | case_account | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the case account link |
| DF-CAS-025 | case_account | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The recovery_case this record belongs to |
| DF-CAS-026 | case_account | account_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The loan_account this record belongs to |
| DF-CAS-027 | case_account | is_primary | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | True for the account the case was opened on |
| DF-CAS-028 | case_account | linked_from | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Date the account joined the case |
| DF-CAS-029 | case_account | linked_to | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Date the account left the case |
| DF-CAS-030 | case_party | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the case party link |
| DF-CAS-031 | case_party | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The recovery_case this record belongs to |
| DF-CAS-032 | case_party | party_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The party this record belongs to |
| DF-CAS-033 | case_party | party_role | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Borrower, co-borrower, guarantor, authorized signatory, heir |
| DF-CAS-034 | case_party | role_from | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Date the role starts |
| DF-CAS-035 | case_party | role_to | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Date the role ends |
| DF-CAS-036 | deviation | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the deviation |
| DF-CAS-037 | deviation | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The recovery_case this record belongs to |
| DF-CAS-038 | deviation | deviation_code | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | X1 to X7 |
| DF-CAS-039 | deviation | raised_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When it was raised |
| DF-CAS-040 | deviation | raised_by | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Screening agent, rule, officer, customer contact |
| DF-CAS-041 | deviation | paused_state | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | The routing state the case was in when paused |
| DF-CAS-042 | deviation | handler_user_id | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | The named handler |
| DF-CAS-043 | deviation | contact_stop | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | True when customer contact is stopped |
| DF-CAS-044 | deviation | cleared_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When it cleared |
| DF-CAS-045 | deviation | outcome | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Returned, re-routed, case ended |
| DF-WRK-001 | queue | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the queue |
| DF-WRK-002 | queue | queue_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Queue code |
| DF-WRK-003 | queue | queue_name | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Queue name |
| DF-WRK-004 | queue | team_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Team the queue belongs to |
| DF-WRK-005 | queue | role_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Role that works the queue |
| DF-WRK-006 | queue | assignment_method | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Round robin, lowest load, named owner, skill |
| DF-WRK-007 | queue | capacity_cap | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Most open cases one person may hold in the queue |
| DF-WRK-008 | queue | overflow_queue_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Queue that receives overflow |
| DF-WRK-037 | queue | rr_cursor_user_id | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | The member last given a case by round robin in the queue |
| DF-WRK-038 | queue | table_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The QUEUE reference version applied to the row |
| DF-WRK-009 | assignment | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the assignment |
| DF-WRK-010 | assignment | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The recovery_case this record belongs to |
| DF-WRK-011 | assignment | task_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The task this record belongs to |
| DF-WRK-012 | assignment | assignee_user_id | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | The person or service identity assigned |
| DF-WRK-013 | assignment | assigned_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When assigned |
| DF-WRK-014 | assignment | ended_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When the assignment ended |
| DF-WRK-015 | assignment | reason | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Allocation, transfer, rebalance, manual, escalation |
| DF-WRK-016 | assignment | rule_id | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | The rule that made the assignment |
| DF-WRK-039 | assignment | queue_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The queue the assignment placed the case in |
| DF-WRK-040 | assignment | transfer_reason_code | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Coded reason for a manual transfer or move |
| DF-WRK-017 | task | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the task |
| DF-WRK-018 | task | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The recovery_case this record belongs to |
| DF-WRK-019 | task | task_code | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | The task in the case model, for example VERIFY_PACK |
| DF-WRK-020 | task | element_type | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Human, customer, partner or decision task, milestone, event listener |
| DF-WRK-021 | task | discretion | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Automatic, discretionary, required |
| DF-WRK-022 | task | status | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Open, in progress, done, canceled |
| DF-WRK-023 | task | owner_role | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Role that owns the task |
| DF-WRK-024 | task | due_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When the task is due |
| DF-WRK-025 | task | completed_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When it completed |
| DF-WRK-026 | task | outcome_code | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | The event the task produced |
| DF-WRK-027 | timer | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the timer |
| DF-WRK-028 | timer | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The recovery_case this record belongs to |
| DF-WRK-029 | timer | task_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The task this record belongs to |
| DF-WRK-030 | timer | timer_type | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Service level, notice period, cure period, prescription, hearing deadline, offer validity, holding age, claim deadline |
| DF-WRK-031 | timer | started_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When it started |
| DF-WRK-032 | timer | expires_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When it expires |
| DF-WRK-033 | timer | warn_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When the warning is raised |
| DF-WRK-034 | timer | paused | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | True while paused by a deviation. A prescription timer never pauses |
| DF-WRK-035 | timer | status | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Running, paused, expired, stopped |
| DF-WRK-036 | timer | escalation_level | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | How many times it has escalated |
| DF-WRK-041 | timer | warned_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When the warning was sent, so it is sent once |
| DF-WRK-042 | timer | treatment_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The treatment a plan timer belongs to |
| DF-WRK-043 | timer | escalated_to_role | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Role the breach was last escalated to |
| DF-WRK-044 | timer | escalated_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When the timer last escalated |
| DF-PTY-001 | party | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the party |
| DF-PTY-002 | party | cif_no | Indirect identifier | Confidential | Yes | Shown within the role's scope; masked in UAT | Contract (PDPA section 24) | Per data product (DL26) | Customer number in the bank |
| DF-PTY-003 | party | party_type | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Individual or juristic person |
| DF-PTY-004 | party | first_name | Direct identifier | Restricted | Yes | Masked unless the role may see it | Contract (PDPA section 24); legal obligation for statutory notices | Per data product (DL26) | First name or company name |
| DF-PTY-005 | party | last_name | Direct identifier | Restricted | Yes | Masked unless the role may see it | Contract (PDPA section 24); legal obligation for statutory notices | Per data product (DL26) | Last name |
| DF-PTY-006 | party | id_type | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Thai national ID, passport, company registration |
| DF-PTY-007 | party | id_no_token | Direct identifier | Restricted | Yes | Masked unless the role may see it | Contract (PDPA section 24); legal obligation for statutory notices | Per data product (DL26) | Tokenized identity number. The clear value is never stored in the Workbench |
| DF-PTY-008 | party | date_of_birth | Direct identifier | Restricted | Yes | Masked unless the role may see it | Contract (PDPA section 24); legal obligation for statutory notices | Per data product (DL26) | Date of birth |
| DF-PTY-009 | party | segment | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Retail, SSME, corporate |
| DF-PTY-010 | party | vulnerable_flag | Sensitive | Restricted | Yes | Masked unless the role handles the deviation | Explicit consent, or the legal claims exemption for sensitive data (PDPA section 26) | Per data product (DL26) | Vulnerable customer or hardship confirmed |
| DF-PTY-011 | party | deceased_flag | Sensitive | Restricted | Yes | Masked unless the role handles the deviation | Explicit consent, or the legal claims exemption for sensitive data (PDPA section 26) | Per data product (DL26) | Death confirmed |
| DF-PTY-012 | party | bankruptcy_flag | Sensitive | Restricted | Yes | Masked unless the role handles the deviation | Explicit consent, or the legal claims exemption for sensitive data (PDPA section 26) | Per data product (DL26) | Bankruptcy or receivership confirmed |
| DF-PTY-021 | party | fraud_flag | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | True while fraud is confirmed or under investigation for the party |
| DF-PTY-013 | contact_point | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the contact point |
| DF-PTY-014 | contact_point | party_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The party this record belongs to |
| DF-PTY-015 | contact_point | channel | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Mobile, home phone, work phone, LINE, email, postal address |
| DF-PTY-016 | contact_point | value_token | Direct identifier | Restricted | Yes | Masked unless the role may see it | Contract (PDPA section 24); legal obligation for statutory notices | Per data product (DL26) | The number, handle or address, stored masked |
| DF-PTY-017 | contact_point | source | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Bank record, field visit, agency, bureau trace, customer |
| DF-PTY-018 | contact_point | consent_status | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Given, withdrawn, unknown |
| DF-PTY-019 | contact_point | verified_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When it last reached the right party |
| DF-PTY-020 | contact_point | failed_count | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Failed attempts since last success |
| DF-ACC-001 | loan_account | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the account |
| DF-ACC-002 | loan_account | account_no | Indirect identifier | Confidential | Yes | Shown within the role's scope; masked in UAT | Contract (PDPA section 24) | Per data product (DL26) | Account number |
| DF-ACC-003 | loan_account | contract_no | Indirect identifier | Confidential | Yes | Shown within the role's scope; masked in UAT | Contract (PDPA section 24) | Per data product (DL26) | Contract number |
| DF-ACC-004 | loan_account | product_code | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Core bank product code |
| DF-ACC-005 | loan_account | product_category_efs | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Product category in EFS |
| DF-ACC-006 | loan_account | business_unit | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Owning business unit |
| DF-ACC-007 | loan_account | contract_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Contract date |
| DF-ACC-008 | loan_account | interest_rate | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Contract interest rate, percent |
| DF-ACC-009 | loan_account | principal_outstanding | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Principal outstanding, baht |
| DF-ACC-010 | loan_account | interest_outstanding | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Accrued interest outstanding, baht |
| DF-ACC-011 | loan_account | fees_outstanding | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Fees outstanding, baht |
| DF-ACC-012 | loan_account | total_balance | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Total balance, baht |
| DF-ACC-013 | loan_account | accounting_balance | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Accounting balance, baht |
| DF-ACC-014 | loan_account | days_past_due | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Days past due |
| DF-ACC-015 | loan_account | bucket | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Arrears bucket, for example 91-120, 180+ |
| DF-ACC-016 | loan_account | classification | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Loan classification and stage |
| DF-ACC-017 | loan_account | last_payment_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Date of the last payment |
| DF-ACC-018 | loan_account | next_installment_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Next installment date |
| DF-ACC-019 | loan_account | tdr_flag | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | True when the account is under a restructure |
| DF-ACC-020 | loan_account | last_tdr_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Date of the last restructure |
| DF-ACC-021 | loan_account | data_as_of | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | The business date of the load |
| DF-ACC-029 | loan_account | dispute_open | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | True while the customer disputes the balance or the security on the account |
| DF-ACC-030 | loan_account | settlement_booked_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Date a settlement was booked in ALS; source field to confirm with the system owner |
| DF-ACC-031 | loan_account | settlement_booked_amount | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Settlement amount booked in ALS, baht; source field to confirm with the system owner |
| DF-ACC-022 | account_payment | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the account payment |
| DF-ACC-023 | account_payment | account_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The loan_account this record belongs to |
| DF-ACC-024 | account_payment | payment_code | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Payment reference |
| DF-ACC-025 | account_payment | payment_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Value date |
| DF-ACC-026 | account_payment | payment_amount | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Amount, baht |
| DF-ACC-027 | account_payment | payment_channel | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Channel the payment came through |
| DF-ACC-028 | account_payment | data_as_of | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | The business date of the load |
| DF-COL-001 | collateral | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the collateral |
| DF-COL-002 | collateral | collateral_no | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Collateral number |
| DF-COL-003 | collateral | collateral_type | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Land, house, condominium, vehicle, deposit, other |
| DF-COL-004 | collateral | title_doc_no | Indirect identifier | Confidential | Yes | Shown within the role's scope; masked in UAT | Contract (PDPA section 24) | Per data product (DL26) | Title deed or registration number |
| DF-COL-005 | collateral | plot_no | Indirect identifier | Confidential | Yes | Shown within the role's scope; masked in UAT | Contract (PDPA section 24) | Per data product (DL26) | Plot number |
| DF-COL-006 | collateral | area_text | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Land area in rai-ngan-wa |
| DF-COL-007 | collateral | province | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Province |
| DF-COL-008 | collateral | district | Indirect identifier | Confidential | Yes | Shown within the role's scope; masked in UAT | Contract (PDPA section 24) | Per data product (DL26) | District |
| DF-COL-009 | collateral | subdistrict | Indirect identifier | Confidential | Yes | Shown within the role's scope; masked in UAT | Contract (PDPA section 24) | Per data product (DL26) | Subdistrict |
| DF-COL-010 | collateral | occupancy | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Occupied by owner, tenant, vacant, unknown |
| DF-COL-011 | collateral | encumbrance_status | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Clear, other creditor, seized, under dispute |
| DF-COL-012 | collateral | insured_value | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Insured value, baht |
| DF-COL-013 | collateral | insurance_expiry | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Insurance expiry date |
| DF-COL-014 | account_collateral | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the account collateral link |
| DF-COL-015 | account_collateral | account_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The loan_account this record belongs to |
| DF-COL-016 | account_collateral | collateral_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The collateral this record belongs to |
| DF-COL-017 | account_collateral | lien_rank | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Rank of the bank's lien |
| DF-COL-018 | valuation | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the valuation |
| DF-COL-019 | valuation | collateral_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The collateral this record belongs to |
| DF-COL-020 | valuation | asset_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The asset this record belongs to |
| DF-COL-021 | valuation | appraisal_no | Indirect identifier | Confidential | Yes | Shown within the role's scope; masked in UAT | Contract (PDPA section 24) | Per data product (DL26) | Appraisal number |
| DF-COL-022 | valuation | appraisal_type | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Market, official, forced sale, desktop, agent estimate |
| DF-COL-023 | valuation | appraised_value | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Appraised value, baht |
| DF-COL-024 | valuation | forced_sale_value | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Forced sale value, baht |
| DF-COL-025 | valuation | appraisal_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Appraisal date |
| DF-COL-026 | valuation | valuer_partner_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The valuer |
| DF-COL-027 | valuation | accepted | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | True once accepted for the route decision |
| DF-COL-043 | valuation | stale_flag | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | True when the appraisal is older than appraisal.max.age at the load business date |
| DF-COL-044 | valuation | age_days | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Age of the appraisal in days at the load business date |
| DF-COL-028 | asset | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the asset |
| DF-COL-029 | asset | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The recovery_case this record belongs to |
| DF-COL-030 | asset | collateral_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The collateral this record belongs to |
| DF-COL-031 | asset | asset_ref | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Asset reference |
| DF-COL-032 | asset | asset_code | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Asset code |
| DF-COL-033 | asset | asset_type | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Detached house, townhouse, condominium, land, vehicle |
| DF-COL-034 | asset | transfer_in_type | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Auction purchase, deed in lieu, repossession |
| DF-COL-035 | asset | from_segment | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Segment the asset came from |
| DF-COL-036 | asset | transfer_in_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Date ownership passed to the bank |
| DF-COL-037 | asset | book_value | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Book value, baht |
| DF-COL-038 | asset | auction_purchase_price | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Price paid at auction, baht |
| DF-COL-039 | asset | repossessed_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Date the vehicle was repossessed |
| DF-COL-040 | asset | stock_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Date the vehicle entered stock |
| DF-COL-041 | asset | holding_status | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Held, listed, under offer, sold, transferred, rented |
| DF-COL-042 | asset | holding_cost_to_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Holding cost to date, baht |
| DF-TRT-001 | treatment | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the treatment |
| DF-TRT-002 | treatment | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The recovery_case this record belongs to |
| DF-TRT-003 | treatment | decision_log_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The decision that approved it |
| DF-TRT-004 | treatment | treatment_type | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Restructure, settlement, deed in lieu, buy-back, guarantee claim, repossession, auction, debt sale, write-off, RAMC transfer, rental |
| DF-TRT-005 | treatment | proposed_by | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Agent, rule, person |
| DF-TRT-006 | treatment | proposed_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When proposed |
| DF-TRT-007 | treatment | offer_amount | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Amount offered or agreed, baht |
| DF-TRT-008 | treatment | haircut_amount | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Amount forgiven, baht |
| DF-TRT-009 | treatment | installments | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Number of installments in a plan |
| DF-TRT-010 | treatment | valid_until | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Offer validity |
| DF-TRT-011 | treatment | approval_level | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Approval level that approved it |
| DF-TRT-012 | treatment | booked_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When booked in the core |
| DF-TRT-013 | treatment | outcome | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Kept, broken, completed, canceled, declined |
| DF-TRT-014 | treatment | outcome_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When the outcome was recorded |
| DF-TRT-023 | treatment | nleads_ref | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | NLEADS reference of the credit approval |
| DF-TRT-024 | treatment | credit_result | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Approved or refused, from NLEADS |
| DF-TRT-025 | treatment | credit_result_reason | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Reason given by NLEADS; required when refused |
| DF-TRT-026 | treatment | credit_result_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When the result was given in NLEADS |
| DF-TRT-027 | treatment | interest_rate | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Approved interest rate of the plan, percent |
| DF-TRT-028 | treatment | booking_difference | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Each term that differs between approval and booking: term, approved, booked, business date |
| DF-TRT-029 | treatment | first_due_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Date the first installment is due |
| DF-TRT-030 | treatment | signature_status | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Pending, signed or not signed, read by the routing rules |
| DF-TRT-031 | treatment | installment_amount | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Amount due per plan installment, baht |
| DF-TRT-032 | treatment | installments_paid | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Installments matched so far |
| DF-TRT-033 | treatment | installment_shortfall | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Shortfall left on the plan by a partial payment, baht |
| DF-TRT-015 | guarantee_claim | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the guarantee claim |
| DF-TRT-016 | guarantee_claim | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The recovery_case this record belongs to |
| DF-TRT-017 | guarantee_claim | claim_type | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | TCG, credit life insurance, mortgage insurance, collateral insurance |
| DF-TRT-018 | guarantee_claim | claim_deadline | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Last date the claim can be filed |
| DF-TRT-019 | guarantee_claim | claimed_amount | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Amount claimed, baht |
| DF-TRT-020 | guarantee_claim | filed_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Date filed |
| DF-TRT-021 | guarantee_claim | paid_amount | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Amount paid, baht |
| DF-TRT-022 | guarantee_claim | status | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Preparing, filed, defect, paid, rejected |
| DF-LEG-001 | legal_action | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the legal action |
| DF-LEG-002 | legal_action | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The recovery_case this record belongs to |
| DF-LEG-003 | legal_action | law_firm_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The law firm instructed |
| DF-LEG-004 | legal_action | action_type | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Notice, civil case, appeal, enforcement, bankruptcy petition, LED auction |
| DF-LEG-005 | legal_action | lawsuit_no | Indirect identifier | Confidential | Yes | Shown within the role's scope; masked in UAT | Contract (PDPA section 24) | Per data product (DL26) | Lawsuit reference in LIT |
| DF-LEG-006 | legal_action | black_case_no | Indirect identifier | Confidential | Yes | Shown within the role's scope; masked in UAT | Contract (PDPA section 24) | Per data product (DL26) | Court black case number |
| DF-LEG-007 | legal_action | red_case_no | Indirect identifier | Confidential | Yes | Shown within the role's scope; masked in UAT | Contract (PDPA section 24) | Per data product (DL26) | Court red case number after judgment |
| DF-LEG-008 | legal_action | court_name | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Court |
| DF-LEG-009 | legal_action | claim_amount | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Amount sued for, baht |
| DF-LEG-010 | legal_action | filed_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Date filed |
| DF-LEG-011 | legal_action | judgment_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Date of judgment |
| DF-LEG-012 | legal_action | judgment_amount | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Amount awarded, baht |
| DF-LEG-013 | legal_action | lit_status | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Latest status text in LIT |
| DF-LEG-014 | legal_action | status | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Open, filed, judgment, enforcing, closed, withdrawn |
| DF-LEG-015 | notice | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the notice |
| DF-LEG-016 | notice | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The recovery_case this record belongs to |
| DF-LEG-017 | notice | document_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The generated notice |
| DF-LEG-018 | notice | notice_type | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Demand, recall, statutory sale notice, guarantor notice |
| DF-LEG-019 | notice | sent_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Date sent |
| DF-LEG-020 | notice | barcode | Indirect identifier | Confidential | Yes | Shown within the role's scope; masked in UAT | Contract (PDPA section 24) | Per data product (DL26) | Registered mail barcode |
| DF-LEG-021 | notice | callback_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Date the proof of delivery came back |
| DF-LEG-022 | notice | delivery_status | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Delivered, refused, undeliverable, pending |
| DF-LEG-023 | notice | sent_type | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Before NPL or NPL |
| DF-LEG-030 | notice | party_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Party the notice is addressed to |
| DF-LEG-031 | notice | template_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Template version the notice was generated from |
| DF-LEG-032 | notice | hold_reason | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Why the notice is held: missing merge field, TEMPLATE_WITHDRAWN, CONTACT_STOP_Xn, LEGAL_HOLD |
| DF-LEG-033 | notice | dispatch_file_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | WIN file the notice was last written to |
| DF-LEG-034 | notice | dispatch_attempts | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Number of WIN files the notice has been sent in without acknowledgment |
| DF-LEG-024 | hearing | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the hearing |
| DF-LEG-025 | hearing | legal_action_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The legal_action this record belongs to |
| DF-LEG-026 | hearing | hearing_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Hearing date |
| DF-LEG-027 | hearing | hearing_type | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | First hearing, witness, judgment reading, mediation |
| DF-LEG-028 | hearing | outcome | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Held, adjourned, settled, judgment |
| DF-LEG-029 | hearing | next_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Next date set |
| DF-PRT-001 | partner | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the partner |
| DF-PRT-002 | partner | partner_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Partner code |
| DF-PRT-003 | partner | partner_name | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Registered name |
| DF-PRT-004 | partner | partner_type | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Agency, law firm, valuer, auction vendor, broker, debt buyer, AMC, RAMC |
| DF-PRT-005 | partner | panel_status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Active, on notice, suspended, exited |
| DF-PRT-006 | partner | contract_end | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Contract end date |
| DF-PRT-007 | partner | score | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Latest scorecard result |
| DF-PRT-008 | partner_instruction | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the partner instruction |
| DF-PRT-009 | partner_instruction | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The recovery_case this record belongs to |
| DF-PRT-010 | partner_instruction | partner_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The partner this record belongs to |
| DF-PRT-011 | partner_instruction | instruction_type | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Collect, file suit, enforce, appraise, repossess, list, sell |
| DF-PRT-012 | partner_instruction | instructed_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When instructed |
| DF-PRT-013 | partner_instruction | due_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When the result is due |
| DF-PRT-014 | partner_instruction | status | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Sent, accepted, declined, in progress, done, recalled |
| DF-PRT-015 | partner_instruction | result_code | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Result reported by the partner |
| DF-PRT-016 | partner_instruction | fee_amount | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Fee payable, baht |
| DF-SAL-001 | listing | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the listing |
| DF-SAL-002 | listing | asset_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The asset this record belongs to |
| DF-SAL-003 | listing | sale_channel | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Dutch auction, broker, direct, LED auction, RAMC |
| DF-SAL-004 | listing | start_price | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Start price, baht |
| DF-SAL-005 | listing | floor_price | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Floor price approved, baht |
| DF-SAL-006 | listing | round_no | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Current price round |
| DF-SAL-007 | listing | listed_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When listed |
| DF-SAL-008 | listing | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Draft, live, under offer, sold, withdrawn |
| DF-SAL-009 | asset_sale | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the asset sale |
| DF-SAL-010 | asset_sale | asset_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The asset this record belongs to |
| DF-SAL-011 | asset_sale | listing_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The listing this record belongs to |
| DF-SAL-012 | asset_sale | contract_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Sale contract date |
| DF-SAL-013 | asset_sale | sale_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Sale date |
| DF-SAL-014 | asset_sale | sale_price | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Sale price, baht |
| DF-SAL-015 | asset_sale | transfer_fee | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Transfer fee, baht |
| DF-SAL-016 | asset_sale | specific_business_tax | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Specific business tax, baht |
| DF-SAL-017 | asset_sale | corporate_income_tax | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Corporate income tax, baht |
| DF-SAL-018 | asset_sale | gain_loss | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Sale price less book value and costs |
| DF-SAL-019 | asset_sale | incentive_amount | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Incentive paid on the sale, baht |
| DF-SAL-020 | debt_sale_lot | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the debt sale lot |
| DF-SAL-021 | debt_sale_lot | lot_no | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Lot number, for example 1/2024 |
| DF-SAL-022 | debt_sale_lot | cut_off_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Balance cut-off date |
| DF-SAL-023 | debt_sale_lot | segment | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Segment of the lot |
| DF-SAL-024 | debt_sale_lot | reserve_price | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Reserve price, baht |
| DF-SAL-025 | debt_sale_lot | buyer_partner_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Winning buyer |
| DF-SAL-026 | debt_sale_lot | buyer_class | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | AMC or non-AMC |
| DF-SAL-027 | debt_sale_lot | signing_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the sale was signed |
| DF-SAL-028 | debt_sale_lot | approval_authority | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Authority that approved the sale |
| DF-SAL-029 | debt_sale_lot | payment_terms | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Deposit and payment terms |
| DF-SAL-030 | debt_sale_lot | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Building, offered, awarded, transferred, closed |
| DF-SAL-031 | debt_sale_account | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the debt sale account |
| DF-SAL-032 | debt_sale_account | lot_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The debt_sale_lot this record belongs to |
| DF-SAL-033 | debt_sale_account | account_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The loan_account this record belongs to |
| DF-SAL-034 | debt_sale_account | borrower_code | Indirect identifier | Confidential | Yes | Shown within the role's scope; masked in UAT | Contract (PDPA section 24) | Per data product (DL26) | Borrower code |
| DF-SAL-035 | debt_sale_account | outstanding | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Outstanding at cut-off, baht |
| DF-SAL-036 | debt_sale_account | selling_price | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Price allocated to the account, baht |
| DF-SAL-037 | debt_sale_account | put_back_status | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | None, claimed, accepted, rejected |
| DF-INT-001 | interaction | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the interaction |
| DF-INT-002 | interaction | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The recovery_case this record belongs to |
| DF-INT-003 | interaction | party_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The party this record belongs to |
| DF-INT-004 | interaction | occurred_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When it happened |
| DF-INT-005 | interaction | channel | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Call, visit, SMS, LINE, email, letter, portal, branch; empty for Workbench events such as CASE_CREATED |
| DF-INT-006 | interaction | direction | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Inbound or outbound; empty for Workbench events such as CASE_CREATED |
| DF-INT-007 | interaction | action_code | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Action code |
| DF-INT-008 | interaction | contact_result | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Right party, third party, no answer, wrong number |
| DF-INT-009 | interaction | promise_amount | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Amount promised, baht |
| DF-INT-010 | interaction | promise_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Date promised |
| DF-INT-011 | interaction | summary | Direct identifier | Restricted | Yes | Masked unless the role may see it | Contract (PDPA section 24); legal obligation for statutory notices | Per data product (DL26) | Summary of what was said |
| DF-INT-012 | interaction | conduct_check | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Passed, blocked, not applicable |
| DF-INT-013 | interaction | source_system | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | EFS for collections history, or the Workbench |
| DF-INT-014 | interaction | event_code | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Ledger event |
| DF-INT-015 | interaction | actor_type | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | User, service or partner |
| DF-INT-016 | interaction | actor_ref | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | User ID or service identity code that acted |
| DF-INT-017 | interaction | source_ref | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Producing module and event, or the interface, for example EV-02 CaseAllocated or INT-07 |
| DF-INT-018 | interaction | idempotency_key | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Unique key of the event or request; repeats are rejected; unique on its own |
| DF-INT-019 | interaction | case_seq | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Gap-free sequence of the entry within its case; unique with case_id |
| DF-INT-020 | interaction | decision_log_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Decision log entry the entry records, for DECISION_TAKEN |
| DF-INT-021 | interaction | corrects_entry_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Entry this entry corrects |
| DF-INT-022 | interaction | contact_point_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The contact point reached; the number or address stays masked in contact_point |
| DF-INT-023 | interaction | from_holder_ref | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Who held the case before a hand-over: USER:<user id> or PARTNER:<partner code> |
| DF-INT-024 | interaction | to_holder_ref | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Who holds the case after a hand-over: USER:<user id> or PARTNER:<partner code> |
| DF-INT-025 | interaction | treatment_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The treatment offered, for an OFFER entry |
| DF-INT-026 | interaction | proceeds_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The proceeds matched, for a PAYMENT entry |
| DF-INT-027 | interaction | retention_class | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Retention class of the entry, set by entry type |
| DF-INT-028 | interaction | delivery_status | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Delivery state of an outbound SMS, LINE message or letter |
| DF-INT-029 | interaction | external_ref | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Reference returned by NSS, LINE OA or WIN |
| DF-DOC-001 | document | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the document |
| DF-DOC-002 | document | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The recovery_case this record belongs to |
| DF-DOC-003 | document | party_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The party this record belongs to |
| DF-DOC-004 | document | document_type | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Type from the document checklist |
| DF-DOC-005 | document | source | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Scan, upload, generated, partner, email |
| DF-DOC-006 | document | storage_ref | Indirect identifier | Confidential | Yes | Shown within the role's scope; masked in UAT | Contract (PDPA section 24) | Per data product (DL26) | Reference to the stored file |
| DF-DOC-007 | document | classification_confidence | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | OCR classification confidence |
| DF-DOC-008 | document | review_status | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Not needed, pending, confirmed, corrected |
| DF-DOC-009 | document | retention_class | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Retention class |
| DF-DOC-010 | document | write_once | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | True for legal documents held write-once |
| DF-DOC-011 | document | doc_version | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Document version |
| DF-DOC-025 | document | previous_version_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The document row this version supersedes; empty for version 1 |
| DF-DOC-026 | document | content_sha256 | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | SHA-256 of the stored file, for the duplicate check and the integrity check |
| DF-DOC-027 | document | captured_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Device time when the field app captured the file |
| DF-DOC-028 | document | capture_latitude | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | GPS latitude at capture |
| DF-DOC-029 | document | capture_longitude | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | GPS longitude at capture |
| DF-DOC-030 | document | client_file_id | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Field app file ID, unique per case, for repeat syncs |
| DF-DOC-031 | document | capture_kind | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Photo, bill or checklist |
| DF-DOC-032 | document | template_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Template version a generated document was made from |
| DF-DOC-033 | document | treatment_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Treatment a generated document belongs to |
| DF-DOC-012 | document_field | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the document field |
| DF-DOC-013 | document_field | document_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The document this record belongs to |
| DF-DOC-014 | document_field | field_name | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Field name from the document type |
| DF-DOC-015 | document_field | field_value | Direct identifier | Restricted | Yes | Masked unless the role may see it | Contract (PDPA section 24); legal obligation for statutory notices | Per data product (DL26) | Value read, masked where personal |
| DF-DOC-016 | document_field | confidence | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Extraction confidence |
| DF-DOC-017 | document_field | confirmed_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Who confirmed a low confidence value |
| DF-DOC-034 | document_field | extracted_value | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | The value as first read by the extractor, kept when a person corrects field_value; masked by role |
| DF-DOC-035 | document_field | extractor_version | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Extraction approach and model version that produced the value |
| DF-DOC-018 | document_custody | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the custody movement |
| DF-DOC-019 | document_custody | document_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The document this record belongs to |
| DF-DOC-020 | document_custody | moved_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When it moved |
| DF-DOC-021 | document_custody | from_location | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Vault, branch, post, lawyer, court, land office |
| DF-DOC-022 | document_custody | to_location | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Where it went |
| DF-DOC-023 | document_custody | held_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Person or firm holding it |
| DF-DOC-024 | document_custody | due_back | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When it is due back |
| DF-DEC-001 | decision_log_entry | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the decision log entry |
| DF-DEC-002 | decision_log_entry | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The recovery_case this record belongs to; empty only for access events (decision code AC-...) with no case |
| DF-DEC-003 | decision_log_entry | decision_code | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | D5.1 to D9.3, X1 to X7, or an access event |
| DF-DEC-004 | decision_log_entry | rule_id | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Rule that fired |
| DF-DEC-005 | decision_log_entry | rule_version | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Rule version |
| DF-DEC-006 | decision_log_entry | model_version | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Model version used |
| DF-DEC-007 | decision_log_entry | agent_version | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Agent and prompt version used |
| DF-DEC-008 | decision_log_entry | inputs_ref | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Reference to the inputs snapshot, with the freshness of each input |
| DF-DEC-009 | decision_log_entry | recommendation | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Option, reasons, confidence and alternatives |
| DF-DEC-010 | decision_log_entry | approver_user_id | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Who approved |
| DF-DEC-011 | decision_log_entry | approval_level | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Approval level applied |
| DF-DEC-012 | decision_log_entry | final_call | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | The option decided |
| DF-DEC-013 | decision_log_entry | override_reason | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Reason when the person did not follow the recommendation |
| DF-DEC-014 | decision_log_entry | actions | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Target system, result and timestamps of each action |
| DF-DEC-015 | decision_log_entry | outcome | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Cash, cure, loss and time, written when known |
| DF-DEC-016 | decision_log_entry | decided_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | When decided |
| DF-DEC-017 | decision_log_entry | prev_hash | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Hash of the previous entry |
| DF-DEC-018 | decision_log_entry | entry_hash | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Hash of this entry |
| DF-DEC-028 | decision_log_entry | chain_seq | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Position of the entry in the hash chain; prev_hash is the entry_hash of chain_seq minus 1; unique on its own |
| DF-DEC-029 | decision_log_entry | corrects_entry_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The entry this entry corrects |
| DF-DEC-030 | decision_log_entry | actor_user_id | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | The person or service identity whose action, preparation or access the entry records |
| DF-DEC-031 | decision_log_entry | idempotency_key | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Event ID of the calling module; a repeat returns the first entry; unique on its own |
| DF-DEC-019 | score | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the score |
| DF-DEC-020 | score | account_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The loan_account this record belongs to |
| DF-DEC-021 | score | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The recovery_case this record belongs to |
| DF-DEC-022 | score | model_code | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Model, for example CRR_RET_380 asset pricing |
| DF-DEC-023 | score | model_version | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Model version |
| DF-DEC-024 | score | score_value | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Score |
| DF-DEC-025 | score | estimate_value | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Estimated amount, baht, for example return by route or sale price |
| DF-DEC-026 | score | route_code | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Route the estimate is for |
| DF-DEC-027 | score | scored_at | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Score date |
| DF-FIN-001 | proceeds | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the proceeds |
| DF-FIN-002 | proceeds | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The recovery_case this record belongs to |
| DF-FIN-003 | proceeds | treatment_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The treatment this record belongs to |
| DF-FIN-004 | proceeds | account_payment_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The account_payment this record belongs to |
| DF-FIN-005 | proceeds | source | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Customer, LED, auction, buyer, agency, insurer, guarantor |
| DF-FIN-006 | proceeds | amount | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Amount, baht |
| DF-FIN-007 | proceeds | received_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Date received |
| DF-FIN-008 | proceeds | matched_to | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Installment, settlement, fee, sale proceeds, unmatched |
| DF-FIN-009 | proceeds | posting_ref | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Posting reference in the core or GL |
| DF-FIN-010 | write_off | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the write-off |
| DF-FIN-011 | write_off | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The recovery_case this record belongs to |
| DF-FIN-012 | write_off | decision_log_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The decision_log_entry this record belongs to |
| DF-FIN-013 | write_off | amount | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Amount written off, baht |
| DF-FIN-014 | write_off | tax_criteria_met | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | True when the tax criteria are met |
| DF-FIN-015 | write_off | committee_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Committee approval date |
| DF-FIN-016 | write_off | posted_date | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Posting date |
| DF-FIN-017 | write_off | responsibility_center | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Responsibility center |
| DF-FIN-018 | write_off | cost_center | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Operating cost center |
| DF-FIN-019 | write_off | gl_product | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | GL product code |
| DF-FIN-020 | write_off | recovered_after | Customer data | Confidential | Yes | Shown within the role's scope | Contract (PDPA section 24); legal obligation for regulatory reporting | Per data product (DL26) | Recovered after charge-off to date, baht |
| DF-REF-001 | rule_row | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the rule row |
| DF-REF-002 | rule_row | rule_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Rule ID, for example R-LIT-12 |
| DF-REF-003 | rule_row | rule_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Version |
| DF-REF-004 | rule_row | route_set | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Route set |
| DF-REF-005 | rule_row | from_state | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | From state |
| DF-REF-006 | rule_row | event_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Event |
| DF-REF-007 | rule_row | condition_expr | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Condition |
| DF-REF-008 | rule_row | action_text | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Action |
| DF-REF-009 | rule_row | to_state | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | To state |
| DF-REF-010 | rule_row | owner_role | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Owner of the next state |
| DF-REF-011 | rule_row | timer_spec | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Timer |
| DF-REF-012 | rule_row | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Valid from |
| DF-REF-013 | rule_row | valid_to | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Valid to |
| DF-REF-014 | rule_row | approved_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Who approved the version |
| DF-REF-015 | rule_row | test_case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Test case that proves the rule |
| DF-REF-052 | rule_row | rule_table | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The Epic 1 rule table a row belongs to |
| DF-REF-053 | rule_row | row_order | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Order in which rows of one rule table are evaluated; first match wins |
| DF-REF-054 | rule_row | target_queue_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The queue an allocation or transfer row places the case in |
| DF-REF-016 | delegation_limit | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the delegation limit |
| DF-REF-017 | delegation_limit | decision_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Decision the limit applies to |
| DF-REF-018 | delegation_limit | approval_level | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Level 1 to 6 under Regulation กกค.540031 |
| DF-REF-019 | delegation_limit | product_group | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Product group |
| DF-REF-020 | delegation_limit | principal_limit | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Principal limit, baht; empty means no limit |
| DF-REF-021 | delegation_limit | loss_pct_limit | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Loss limit as a percentage |
| DF-REF-022 | delegation_limit | min_price_pct_fmv | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Lowest sale price as a percentage of fair market value |
| DF-REF-023 | delegation_limit | holder_user_id | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Person holding the level |
| DF-REF-024 | delegation_limit | substitute_user_id | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Substitute when the holder is absent |
| DF-REF-025 | delegation_limit | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Valid from |
| DF-REF-026 | delegation_limit | valid_to | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Valid to |
| DF-REF-055 | delegation_limit | limit_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Delegation version the row belongs to, for example DOA-2026.11 |
| DF-REF-056 | delegation_limit | regulation_item | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Item of Regulation กกค.540031, for example 2.1.1; one decision code covers several items |
| DF-REF-057 | delegation_limit | applies_when | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Case condition that selects the row, WO_CRITERIA_MET or WO_CRITERIA_NOT_MET for item 2.1.10 |
| DF-REF-058 | delegation_limit | max_loss_amount | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Maximum loss the level may approve, baht |
| DF-REF-059 | delegation_limit | max_delay_count | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Most delays of legal action, seizure or auction the level may approve on a case |
| DF-REF-060 | delegation_limit | min_price_pct_principal | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Lowest sale price as a percentage of principal outstanding |
| DF-REF-061 | delegation_limit | min_received_pct | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Lowest amount received against the total debt, percent |
| DF-REF-062 | delegation_limit | max_term_years | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Longest lease term the level may approve, years |
| DF-REF-027 | lov_value | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the list value |
| DF-REF-028 | lov_value | lov_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | List code, for example LOV-ROUTE |
| DF-REF-029 | lov_value | value_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Value code |
| DF-REF-030 | lov_value | label_en | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | English label |
| DF-REF-031 | lov_value | label_th | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Thai label |
| DF-REF-032 | lov_value | sort_order | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Display order |
| DF-REF-033 | lov_value | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Valid from |
| DF-REF-034 | role | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the role |
| DF-REF-035 | role | role_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Role code, for example RW-CASEOWN |
| DF-REF-036 | role | role_name | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Role name |
| DF-REF-037 | role | role_class | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Bank user, partner user, non-human actor |
| DF-REF-038 | role | default_scope | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Own, team, region, all |
| DF-REF-039 | role | entra_group | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Entra ID group mapped to the role |
| DF-REF-040 | permission | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the permission |
| DF-REF-041 | permission | role_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The role this record belongs to |
| DF-REF-042 | permission | capability_area | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | One of the 14 capability areas |
| DF-REF-043 | permission | letters | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | C, R, U, D and A, or a dash for none |
| DF-REF-044 | permission | matrix_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Permission matrix version |
| DF-REF-045 | template | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the template |
| DF-REF-046 | template | template_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Template code |
| DF-REF-047 | template | template_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Version; unique with template_code, since a template holds several versions |
| DF-REF-048 | template | language | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Thai or English |
| DF-REF-049 | template | product_group | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Product group it applies to |
| DF-REF-050 | template | body_ref | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Stored template body |
| DF-REF-051 | template | approved_by_legal | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | True once Legal approves the wording |
| DF-REF-063 | template | approved_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Legal counsel who approved the version |
| DF-REF-064 | template | approved_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the version was approved |
| DF-REF-065 | template | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date from which the approved version is current |
| DF-REF-066 | template | channel | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Channel the template is for: letter, SMS or LINE |
| DF-REF-067 | template | notice_type | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Notice type for a notice template; empty for other documents |
| DF-REF-068 | template | signature_basis | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | How Legal allows the document to be signed |
| DF-REF-069 | template | merge_codes | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The merge codes the template body uses |
| DF-REF-070 | data_product | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the data product |
| DF-REF-071 | data_product | product_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Data product code DP01 to DP14 |
| DF-REF-072 | data_product | product_name | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Data product name, for example Account and arrears |
| DF-REF-073 | data_product | definition | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Definition of the product |
| DF-REF-074 | data_product | system_of_record | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The one system of record for the product |
| DF-REF-075 | data_product | owner_role | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Role of the owner, normally RW-DATASTEW |
| DF-REF-076 | data_product | owner_user_id | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | The named owner of the product; required by the catalog load, empty in the seed |
| DF-REF-077 | data_product | refresh_cycle | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Daily, weekly, monthly or on change |
| DF-REF-078 | data_product | expected_by | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Time the load is expected by, for example 08:00 or MON 08:00 |
| DF-REF-079 | data_product | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the catalog version comes into force |
| DF-REF-080 | data_product_access | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the data product access row |
| DF-REF-081 | data_product_access | product_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Data product the row grants |
| DF-REF-082 | data_product_access | role_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Role the row applies to |
| DF-REF-083 | data_product_access | can_read | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | True when the role may read the product |
| DF-REF-084 | data_product_access | access_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Version of the access table, for example DPA-2026.11 |
| DF-REF-085 | data_product_access | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the row comes into force |
| DF-REF-086 | data_product_access | valid_to | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the row ends |
| DF-OPS-001 | data_product_load | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the freshness stamp |
| DF-OPS-002 | data_product_load | product_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Data product loaded |
| DF-OPS-003 | data_product_load | source_system | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Source system of the load |
| DF-OPS-004 | data_product_load | business_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Business date of the load |
| DF-OPS-005 | data_product_load | source_extracted_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the source extract was taken, from the COLLINS control record or the file |
| DF-OPS-006 | data_product_load | loaded_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the load committed in the Workbench |
| DF-OPS-007 | data_product_load | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Loaded or stale |
| DF-OPS-008 | data_product_load | stale_flagged_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the product was flagged stale |
| DF-OPS-009 | data_product_load | duplicate_count | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Repeat stamps ignored for the same product and business date |
| DF-OPS-010 | data_contract | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the data contract |
| DF-OPS-011 | data_contract | contract_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Contract code per source system, for example DC-ALS |
| DF-OPS-012 | data_contract | source_system | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Source system |
| DF-OPS-013 | data_contract | interface_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Interfaces covered, for example INT-01, INT-02 |
| DF-OPS-014 | data_contract | contract_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Contract version |
| DF-OPS-015 | data_contract | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Draft, published or superseded |
| DF-OPS-016 | data_contract | confirmed_by_role | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Role of the system owner who confirmed, for example ALS system owner |
| DF-OPS-017 | data_contract | confirmed_on | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date of the confirmation |
| DF-OPS-018 | data_contract | confirmation_document_ref | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Stored confirmation from the system owner |
| DF-OPS-019 | data_contract | published_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the contract was published |
| DF-OPS-020 | data_contract | published_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Who published the contract |
| DF-REF-087 | sys_objects | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the registered object |
| DF-REF-088 | sys_objects | object_name | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Table name |
| DF-REF-089 | sys_objects | business_name | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Business name of the object |
| DF-REF-090 | sys_objects | subject_area | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Subject area code |
| DF-REF-091 | sys_objects | data_product | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Data product the object belongs to, DP01 to DP14 or None |
| DF-REF-092 | sys_objects | system_of_record | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | System of record of the object |
| DF-REF-093 | sys_objects | description | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | What the object holds |
| DF-REF-094 | sys_fields | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the registered field |
| DF-REF-095 | sys_fields | field_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | BR Field ID, for example DF-CAS-001 |
| DF-REF-096 | sys_fields | object_name | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Table the field belongs to, from sys_objects |
| DF-REF-097 | sys_fields | field_name | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Column name; unique with object_name |
| DF-REF-098 | sys_fields | data_type | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | TSD data type: TEXT, NUMBER, DATE, BOOLEAN, LOV, USER_REF, CROSS_REF, FORMULA or ATTACHMENT |
| DF-REF-099 | sys_fields | physical_type | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | PostgreSQL type |
| DF-REF-100 | sys_fields | is_mandatory | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | True when the field is required |
| DF-REF-101 | sys_fields | lov_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | List of values the field takes its values from |
| DF-REF-102 | sys_fields | references_object | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Table a cross-reference field points to |
| DF-REF-103 | sys_fields | source_system | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Source system of the value |
| DF-REF-104 | sys_fields | source_field | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Field name in the source system |
| DF-REF-105 | sys_fields | is_personal | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | True for personal data under PDPA |
| DF-REF-106 | sys_fields | description | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Meaning of the field |
| DF-REF-107 | sys_fields | owner_role | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Owner of the field definition |
| DF-REF-108 | sys_fields | refresh_cycle | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Refresh frequency, for example Daily, end of day |
| DF-REF-109 | sys_fields | late_behavior | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | What the Workbench does when the value is missing or late |
| DF-REF-110 | sys_fields | interface_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Interface that carries the field, INT-01 to INT-34; empty for Workbench fields |
| DF-REF-111 | sys_field_version | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the field version |
| DF-REF-112 | sys_field_version | field_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Field the version belongs to, from sys_fields |
| DF-REF-113 | sys_field_version | field_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Version number |
| DF-REF-114 | sys_field_version | definition | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The full field definition at this version |
| DF-REF-115 | sys_field_version | change_reason | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Reason for the change |
| DF-OPS-021 | load_run | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the load or job run |
| DF-OPS-022 | load_run | interface_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Interface loaded, for example INT-01; TRACKER for tracker loads; empty for job steps |
| DF-OPS-023 | load_run | job_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Job the run belongs to, for example JOB-01 |
| DF-OPS-024 | load_run | product_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Data product loaded or built |
| DF-OPS-025 | load_run | business_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Business date of the load |
| DF-OPS-026 | load_run | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Running, completed, refused, late, failed or superseded |
| DF-OPS-027 | load_run | started_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the run started |
| DF-OPS-028 | load_run | ended_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the run ended |
| DF-OPS-029 | load_run | rows_read | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Records read from the source |
| DF-OPS-030 | load_run | rows_loaded | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Records written |
| DF-OPS-031 | load_run | rows_held | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Records held in the exception list |
| DF-OPS-032 | load_run | rows_rejected | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Rows rejected |
| DF-OPS-033 | load_run | failed_check | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Check that refused the load, for example DQ-003 |
| DF-OPS-034 | load_run | check_results | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Result per check code, plus the sample and other counts |
| DF-OPS-035 | load_run | mapping_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Source field mapping version used |
| DF-OPS-036 | load_run | interface_run_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The P2 interface run the file load belongs to |
| DF-OPS-037 | load_run | tracker_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Tracker of a tracker load |
| DF-OPS-038 | load_run | loaded_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | User who uploaded the file |
| DF-OPS-039 | load_run | source_file_name | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Name of the loaded file |
| DF-OPS-040 | load_run | source_file_hash | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | SHA-256 of the loaded file |
| DF-OPS-041 | dq_exception | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the data quality exception |
| DF-OPS-042 | dq_exception | load_run_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The load run that raised it |
| DF-OPS-043 | dq_exception | product_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Data product of the record |
| DF-OPS-044 | dq_exception | check_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Load check (DQ-nnn), row rule (DQnn), reconciliation (REC-nn) or tracker check (TRK-nn) |
| DF-OPS-045 | dq_exception | record_key | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Business key of the failing record, for example the account number; never personal data |
| DF-OPS-046 | dq_exception | reason_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Reason code shown to the data product owner |
| DF-OPS-047 | dq_exception | detail | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Short reason without personal data |
| DF-OPS-048 | dq_exception | raised_on | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Business date raised |
| DF-OPS-049 | dq_exception | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Open or cleared |
| DF-OPS-050 | dq_exception | rule_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Rule version that raised the exception |
| DF-OPS-051 | dq_exception | cleared_on | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the record passed again |
| DF-OPS-052 | dq_rule | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the data quality rule |
| DF-OPS-053 | dq_rule | rule_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Rule code, for example DQ02 |
| DF-OPS-054 | dq_rule | rule_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Rule version |
| DF-OPS-055 | dq_rule | rule_name | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Rule name |
| DF-OPS-056 | dq_rule | product_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Data product the rule runs for |
| DF-OPS-057 | dq_rule | target_entity | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | P1 table the rule checks |
| DF-OPS-058 | dq_rule | rule_type | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Not null, unique across, range, sum equals, exists link, maximum age in days, field before |
| DF-OPS-059 | dq_rule | rule_params | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Fields and values for the rule type |
| DF-OPS-060 | dq_rule | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the version comes into force |
| DF-OPS-061 | dq_rule | valid_to | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Last date the version is in force |
| DF-OPS-062 | dq_rule | approved_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Who approved the version |
| DF-OPS-063 | dq_rule | test_case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Test case that proves the rule |
| DF-OPS-064 | source_field_map | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the source field mapping |
| DF-OPS-065 | source_field_map | interface_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Interface the mapping is for |
| DF-OPS-066 | source_field_map | mapping_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Mapping version |
| DF-OPS-067 | source_field_map | source_field | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Field name in the source |
| DF-OPS-068 | source_field_map | target_entity | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Workbench entity |
| DF-OPS-069 | source_field_map | target_field | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Workbench field |
| DF-OPS-070 | source_field_map | transformation | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Transformation type and parameters: COPY_TRIM, SUM, TO_DATE_BE, TO_NUMERIC_2, BOOLEAN_YN, CODE_MAP, BUSINESS_DATE |
| DF-OPS-071 | source_field_map | approved_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Who approved the mapping version |
| DF-OPS-072 | source_field_map | approved_on | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Approval date |
| DF-OPS-073 | source_field_map | approval_ref | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Reference of the system owner's sign-off on the mapping version |
| DF-OPS-074 | source_field_map | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the version comes into force |
| DF-OPS-075 | source_code_map | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the source code mapping |
| DF-OPS-076 | source_code_map | interface_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Interface the code map is for |
| DF-OPS-077 | source_code_map | lov_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Target list of values |
| DF-OPS-078 | source_code_map | source_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Code in the source |
| DF-OPS-079 | source_code_map | value_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Workbench list value |
| DF-OPS-080 | source_code_map | map_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Code map version |
| DF-OPS-081 | source_code_map | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the version comes into force |
| DF-OPS-082 | source_code_map | valid_to | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Last date the version is in force |
| DF-OPS-083 | tracker_inventory | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the tracker |
| DF-OPS-084 | tracker_inventory | tracker_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Tracker code |
| DF-OPS-085 | tracker_inventory | inventory_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Inventory version |
| DF-OPS-086 | tracker_inventory | team_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Owning team |
| DF-OPS-087 | tracker_inventory | tracker_name | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Tracker name |
| DF-OPS-088 | tracker_inventory | location_type | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Excel, SharePoint, local file or none |
| DF-OPS-089 | tracker_inventory | location_ref | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Where the tracker is kept |
| DF-OPS-090 | tracker_inventory | owner_user_id | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Tracker owner |
| DF-OPS-091 | tracker_inventory | field_list | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Field names with the personal data tag and the optional mapped-to field |
| DF-OPS-092 | tracker_inventory | update_cycle | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Daily, weekly, monthly or ad hoc |
| DF-OPS-093 | tracker_inventory | target_product | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Target data product for a LOAD decision |
| DF-OPS-094 | tracker_inventory | decision | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Load, retire or keep |
| DF-OPS-095 | tracker_inventory | decision_reason | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Reason for the decision |
| DF-OPS-096 | tracker_inventory | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Listed, loaded, signed off, retired or kept |
| DF-OPS-097 | tracker_inventory | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the inventory version comes into force |
| DF-OPS-098 | tracker_inventory | file_rows | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Rows in the loaded file |
| DF-OPS-099 | tracker_inventory | loaded_rows | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Rows loaded |
| DF-OPS-100 | tracker_inventory | rejected_rows | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Rows rejected |
| DF-OPS-101 | tracker_inventory | last_load_run_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Latest load run of the tracker |
| DF-OPS-102 | tracker_inventory | signed_off_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Team manager who signed off the load |
| DF-OPS-103 | tracker_inventory | signed_off_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Sign-off time |
| DF-OPS-104 | tracker_inventory | source_file_ref | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Stored tracker file in the write-once store |
| DF-OPS-105 | tracker_inventory | archive_ref | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Read-only archive location of the retired tracker |
| DF-OPS-106 | tracker_inventory | retired_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Retirement time |
| DF-OPS-107 | tracker_inventory | retire_confirmed_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Team manager who confirmed the retirement |
| DF-OPS-108 | tracker_inventory | unfed_fields | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Non-personal tracker fields no data product field carries |
| DF-OPS-109 | tracker_row | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the tracker row |
| DF-OPS-110 | tracker_row | tracker_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Tracker the row came from |
| DF-OPS-111 | tracker_row | load_run_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Load run that loaded the row |
| DF-OPS-112 | tracker_row | row_no | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Row number in the file |
| DF-OPS-113 | tracker_row | account_no | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Account number |
| DF-OPS-114 | tracker_row | target_product | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Target data product |
| DF-OPS-115 | tracker_row | source_file_name | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Source file name |
| DF-OPS-116 | tracker_row | field_values | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Non-personal tracker fields of the row |
| DF-OPS-117 | tracker_row | loaded_on | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Load date |
| DF-RPT-001 | case_list_row | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the case list row |
| DF-RPT-002 | case_list_row | business_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Business date of the list |
| DF-RPT-003 | case_list_row | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Case |
| DF-RPT-004 | case_list_row | case_no | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Case number |
| DF-RPT-005 | case_list_row | account_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Loan account; unique with business_date |
| DF-RPT-006 | case_list_row | account_no | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Account number |
| DF-RPT-007 | case_list_row | product_group | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Product group |
| DF-RPT-008 | case_list_row | stage_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Stage |
| DF-RPT-009 | case_list_row | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Case status |
| DF-RPT-010 | case_list_row | owner_user_id | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Case owner |
| DF-RPT-011 | case_list_row | queue_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Queue code |
| DF-RPT-012 | case_list_row | team_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Team |
| DF-RPT-013 | case_list_row | route_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Route |
| DF-RPT-014 | case_list_row | total_balance | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Total balance, baht |
| DF-RPT-015 | case_list_row | days_past_due | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Days past due |
| DF-RPT-016 | case_list_row | refreshed_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the row was built |
| DF-RPT-017 | case_list_row | last_contact_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Latest EFS contact across the case's accounts |
| DF-RPT-018 | case_list_row | last_action_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Action code of the latest contact |
| DF-RPT-019 | case_list_row | publish_status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Pending, held or released for the date's extract |
| DF-INT-030 | collections_history | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the collections history record |
| DF-INT-031 | collections_history | account_no | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Account number |
| DF-INT-032 | collections_history | efs_record_key | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | EFS record key |
| DF-INT-033 | collections_history | contact_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Contact date and time |
| DF-INT-034 | collections_history | action_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | EFS action code |
| DF-INT-035 | collections_history | action_contact_status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | EFS action contact status |
| DF-INT-036 | collections_history | contact_result | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Call result |
| DF-INT-037 | collections_history | promise_amount | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Amount promised, baht |
| DF-INT-038 | collections_history | promise_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date promised |
| DF-INT-039 | collections_history | business_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Business date of the load |
| DF-OPS-118 | reconciliation_result | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the reconciliation result |
| DF-OPS-119 | reconciliation_result | rec_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Reconciliation, REC-01 or REC-02 |
| DF-OPS-120 | reconciliation_result | business_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Business date |
| DF-OPS-121 | reconciliation_result | product_group | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Product group |
| DF-OPS-122 | reconciliation_result | source_count | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | ALS count |
| DF-OPS-123 | reconciliation_result | workbench_count | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Case list count |
| DF-OPS-124 | reconciliation_result | source_amount | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | ALS balance sum, baht |
| DF-OPS-125 | reconciliation_result | workbench_amount | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Case list balance sum, baht |
| DF-OPS-126 | reconciliation_result | variance_count | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Count difference |
| DF-OPS-127 | reconciliation_result | variance_pct | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Variance, percent |
| DF-OPS-128 | reconciliation_result | tolerance_pct | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Tolerance used, percent |
| DF-OPS-129 | reconciliation_result | result | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Pass or break |
| DF-OPS-130 | lake_copy_watermark | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the lake copy watermark |
| DF-OPS-131 | lake_copy_watermark | copy_name | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Name of the copy; DECISION_LOG for the decision log lake copy |
| DF-OPS-132 | lake_copy_watermark | last_entry_hash | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Entry hash of the last decision log entry copied and matched |
| DF-OPS-133 | lake_copy_watermark | last_decided_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | decided_at of the last entry copied |
| DF-OPS-134 | lake_copy_watermark | rows_copied_total | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Cumulative count of entries in the lake copy |
| DF-OPS-135 | lake_copy_watermark | business_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Business date of the last complete partition |
| DF-REF-116 | retention_rule | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the retention rule |
| DF-REF-117 | retention_rule | product_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Data product the rule applies to |
| DF-REF-118 | retention_rule | table_name | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Table the rule applies to, from sys_objects; never decision_log_entry |
| DF-REF-119 | retention_rule | record_class | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Retention class from LOV-RETENTION, or LAKE_COPY for the decision log lake copy |
| DF-REF-120 | retention_rule | retention_months | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Retention period in months, 1 to 600 |
| DF-REF-121 | retention_rule | age_basis_field | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Field the age is measured from, for example interaction.occurred_at |
| DF-REF-122 | retention_rule | end_action | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Archive or review at the end of the period |
| DF-REF-123 | retention_rule | rule_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Version, for example RET-2026.11 |
| DF-REF-124 | retention_rule | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the version comes into force |
| DF-REF-125 | retention_rule | valid_to | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Last date the version is in force |
| DF-REF-126 | retention_rule | approved_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Who approved the version |
| DF-REF-127 | retention_rule | reference_version_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Reference version that brought the row |
| DF-TRT-034 | dp_treatment | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the treatment copy |
| DF-TRT-035 | dp_treatment | treatment_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The treatment copied; unique with business_date |
| DF-TRT-036 | dp_treatment | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The case of the treatment |
| DF-TRT-037 | dp_treatment | decision_log_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The decision that approved the treatment |
| DF-TRT-038 | dp_treatment | treatment_type | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Treatment type |
| DF-TRT-039 | dp_treatment | proposed_by | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Agent, rule or person |
| DF-TRT-040 | dp_treatment | proposed_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When proposed |
| DF-TRT-041 | dp_treatment | offer_amount | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Amount offered or agreed, baht |
| DF-TRT-042 | dp_treatment | haircut_amount | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Amount forgiven, baht |
| DF-TRT-043 | dp_treatment | installments | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Number of installments in a plan |
| DF-TRT-044 | dp_treatment | valid_until | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Offer validity |
| DF-TRT-045 | dp_treatment | approval_level | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Approval level that approved it |
| DF-TRT-046 | dp_treatment | booked_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When booked in the core |
| DF-TRT-047 | dp_treatment | outcome | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Kept, broken, completed, canceled or declined |
| DF-TRT-048 | dp_treatment | outcome_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the outcome was recorded |
| DF-TRT-049 | dp_treatment | business_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Business date of the build |
| DF-TRT-050 | dp_treatment | contract_no | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Contract number of the case's primary account |
| DF-TRT-051 | dp_treatment | contract_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Contract date of the case's primary account |
| DF-TRT-052 | dp_guarantee_claim | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the guarantee claim copy |
| DF-TRT-053 | dp_guarantee_claim | guarantee_claim_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The guarantee claim copied; unique with business_date |
| DF-TRT-054 | dp_guarantee_claim | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The case of the claim |
| DF-TRT-055 | dp_guarantee_claim | claim_type | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | TCG, credit life insurance, mortgage insurance or collateral insurance |
| DF-TRT-056 | dp_guarantee_claim | claim_deadline | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Last date the claim can be filed |
| DF-TRT-057 | dp_guarantee_claim | claimed_amount | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Amount claimed, baht |
| DF-TRT-058 | dp_guarantee_claim | filed_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date filed |
| DF-TRT-059 | dp_guarantee_claim | paid_amount | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Amount paid, baht |
| DF-TRT-060 | dp_guarantee_claim | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Preparing, filed, defect, paid or rejected |
| DF-TRT-061 | dp_guarantee_claim | business_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Business date of the build |
| DF-OPS-136 | interface_config | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the interface setting |
| DF-OPS-137 | interface_config | interface_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Interface ID, for example INT-10 |
| DF-OPS-138 | interface_config | direction | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Inbound or outbound |
| DF-OPS-139 | interface_config | transport | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | SFTP or COLLINS |
| DF-OPS-140 | interface_config | inbound_path | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Inbound or outbound folder |
| DF-OPS-141 | interface_config | file_pattern | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | File name pattern with the business date |
| DF-OPS-142 | interface_config | data_product | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Data product the file feeds, for example DP06 |
| DF-OPS-143 | interface_config | max_attempts | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Most send attempts before the exception queue |
| DF-OPS-144 | interface_config | retry_intervals_min | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Minutes between attempts, comma separated, for example 5,15,45 |
| DF-OPS-145 | interface_config | owner_role | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Role that receives the exception task |
| DF-OPS-146 | interface_config | alert_role | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Role alerted on a refused or missing file |
| DF-OPS-147 | interface_config | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the version comes into force |
| DF-OPS-148 | interface_config | valid_to | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Last date the version is in force |
| DF-OPS-149 | interface_run | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the interface run |
| DF-OPS-150 | interface_run | interface_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Interface ID |
| DF-OPS-151 | interface_run | file_name | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | File name |
| DF-OPS-152 | interface_run | file_hash | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | SHA-256 of the file |
| DF-OPS-153 | interface_run | business_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Business date of the file |
| DF-OPS-154 | interface_run | record_count | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Records read |
| DF-OPS-155 | interface_run | control_total | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Control total from the trailer |
| DF-OPS-156 | interface_run | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Received, loaded, refused, missing, duplicate or failed |
| DF-OPS-157 | interface_run | failed_check | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Load check ID and name that refused the file |
| DF-OPS-158 | interface_run | checks | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Result of each check and the run summary counts |
| DF-OPS-159 | interface_run | started_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Run start |
| DF-OPS-160 | interface_run | ended_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Run end |
| DF-OPS-161 | interface_signoff | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the interface sign-off |
| DF-OPS-162 | interface_signoff | interface_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Interface whose manual handling is retired |
| DF-OPS-163 | interface_signoff | from_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | First clean day counted |
| DF-OPS-164 | interface_signoff | to_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Last clean day counted |
| DF-OPS-165 | interface_signoff | clean_days | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Clean days in a row at sign-off |
| DF-OPS-166 | interface_signoff | signed_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Data steward who signed off |
| DF-OPS-167 | interface_signoff | signed_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When signed off |
| DF-OPS-168 | outbound_item | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the outbound item |
| DF-OPS-169 | outbound_item | interface_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Interface ID |
| DF-OPS-170 | outbound_item | idempotency_key | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Unique key of the outbound work |
| DF-OPS-171 | outbound_item | payload_ref | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Stored file to send |
| DF-OPS-172 | outbound_item | case_ids | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Cases whose step waits on the file |
| DF-OPS-173 | outbound_item | attempt_count | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Attempts made |
| DF-OPS-174 | outbound_item | next_attempt_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the next attempt is due |
| DF-OPS-175 | outbound_item | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Pending, sent, retry, exception or acknowledged |
| DF-OPS-176 | outbound_item | last_error | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Last transfer error, no personal data |
| DF-OPS-177 | outbound_item | owner_role | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Role that owns the exception task |
| DF-OPS-178 | processed_event | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the processed event |
| DF-OPS-179 | processed_event | consumer | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Consumer name |
| DF-OPS-180 | processed_event | idempotency_key | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Event or work key |
| DF-OPS-181 | processed_event | event_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Outbox event of the first delivery, where the key came from an event |
| DF-OPS-182 | processed_event | hit_count | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Deliveries seen, 1 on first |
| DF-OPS-183 | processed_event | last_seen_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the last repeat arrived |
| DF-OPS-184 | idempotency_key | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the idempotent request |
| DF-OPS-185 | idempotency_key | idempotency_key | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Idempotency-Key header value |
| DF-OPS-186 | idempotency_key | endpoint | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Method and path of the request |
| DF-OPS-187 | idempotency_key | request_hash | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | SHA-256 of the request body |
| DF-OPS-188 | idempotency_key | response | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Stored response returned to a repeat |
| DF-OPS-189 | outbox_event | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the outbox event |
| DF-OPS-190 | outbox_event | event_type | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Event name from EV-01 to EV-28, or an outbound work request type such as WIN_DISPATCH |
| DF-OPS-191 | outbox_event | schema_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Schema version of the payload; consumers accept the current and previous version |
| DF-OPS-192 | outbox_event | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The case the event belongs to; empty for events with no case; unique with case_seq |
| DF-OPS-193 | outbox_event | case_seq | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Order of the event among the events of its case |
| DF-OPS-194 | outbox_event | idempotency_key | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Key passed to every consumer so a repeat is dropped; unique on its own |
| DF-OPS-195 | outbox_event | payload | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | References and codes only; no personal data |
| DF-OPS-196 | outbox_event | actor_ref | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | User ID or service identity that caused the event |
| DF-OPS-197 | outbox_event | occurred_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the change happened |
| DF-OPS-198 | outbox_delivery | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the outbox delivery |
| DF-OPS-199 | outbox_delivery | event_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The outbox event delivered |
| DF-OPS-200 | outbox_delivery | consumer | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Consumer name from the consumer list; unique with event_id |
| DF-OPS-201 | outbox_delivery | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Pending, retrying, delivered or exception |
| DF-OPS-202 | outbox_delivery | attempt_count | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Delivery attempts made |
| DF-OPS-203 | outbox_delivery | next_attempt_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the next attempt is due |
| DF-OPS-204 | outbox_delivery | last_error_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Code of the last failure returned by the consumer |
| DF-OPS-205 | outbox_delivery | delivered_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the consumer succeeded |
| DF-OPS-206 | outbox_delivery | task_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The RESOLVE_OUTBOX_DELIVERY task raised when the delivery entered the exception queue |
| DF-OPS-207 | feature_flag | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the feature flag |
| DF-OPS-208 | feature_flag | flag_key | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Flag key rwb.<module>.<short-name> |
| DF-OPS-209 | feature_flag | description | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | What the flag switches |
| DF-OPS-210 | feature_flag | owner_user_id | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Owner of the flag |
| DF-OPS-211 | feature_flag | owner_team | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Owning squad |
| DF-OPS-212 | feature_flag | default_on | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Default value |
| DF-OPS-213 | feature_flag | dev_on | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Value in DEV |
| DF-OPS-214 | feature_flag | sit_on | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Value in SIT |
| DF-OPS-215 | feature_flag | uat_on | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Value in UAT |
| DF-OPS-216 | feature_flag | prod_on | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Value in PROD |
| DF-OPS-217 | feature_flag | removal_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date by which the flag and its old path are removed |
| DF-OPS-218 | feature_flag_change | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the feature flag change |
| DF-OPS-219 | feature_flag_change | flag_key | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Flag changed |
| DF-OPS-220 | feature_flag_change | environment | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | DEV, SIT, UAT or PROD |
| DF-OPS-221 | feature_flag_change | old_value | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Value before |
| DF-OPS-222 | feature_flag_change | new_value | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Value after |
| DF-OPS-223 | feature_flag_change | reason | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Reason for the change |
| DF-OPS-224 | job_catalog | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the job |
| DF-OPS-225 | job_catalog | job_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Job ID JOB-nn |
| DF-OPS-226 | job_catalog | job_name | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Job name from the batch schedule |
| DF-OPS-227 | job_catalog | owner_role | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Role that owns failures |
| DF-OPS-228 | job_catalog | schedule_text | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Schedule as in the batch schedule |
| DF-OPS-229 | job_catalog | runbook_path | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Path of the run book in the repository |
| DF-OPS-230 | job_catalog | expected_minutes | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Expected duration in minutes |
| DF-OPS-231 | job_catalog | alert_after_minutes | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Duration after which the owner is alerted |
| DF-OPS-232 | job_catalog | first_release | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Epic of first release, for example E1 |
| DF-PTY-022 | party_product | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the party product |
| DF-PTY-023 | party_product | party_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The party that holds the product |
| DF-PTY-024 | party_product | product_type | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Product type from the customer profile |
| DF-PTY-025 | party_product | account_no | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Account number of the product, masked by role |
| DF-PTY-026 | party_product | product_status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Active, delinquent, closed or written off |
| DF-PTY-027 | party_product | data_as_of | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Business date of the customer profile load |
| DF-REF-128 | efs_ledger_outcome | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the EFS ledger outcome row |
| DF-REF-129 | efs_ledger_outcome | action_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | EFS action code named for the ledger |
| DF-REF-130 | efs_ledger_outcome | channel | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Ledger channel for the action code |
| DF-REF-131 | efs_ledger_outcome | in_ledger | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | True when rows with this action code enter the ledger |
| DF-CAS-056 | case_entry_exclusion | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the case entry exclusion |
| DF-CAS-057 | case_entry_exclusion | account_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The account excluded; unique with business_date |
| DF-CAS-058 | case_entry_exclusion | business_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Business date of the exclusion |
| DF-CAS-059 | case_entry_exclusion | reason_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Deceased, fraud, bankruptcy, active plan or open dispute |
| DF-CAS-060 | case_entry_exclusion | rule_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Exclusion rule that blocked the entry |
| DF-CAS-061 | case_entry_exclusion | rule_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Version of that rule |
| DF-WRK-045 | queue_member | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the queue member |
| DF-WRK-046 | queue_member | queue_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The queue |
| DF-WRK-047 | queue_member | user_id | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | The person |
| DF-WRK-048 | queue_member | capacity | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Most open cases the person may hold in the queue |
| DF-WRK-049 | queue_member | skill_codes | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Skills of the person, comma separated |
| DF-WRK-050 | queue_member | table_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | QUEUE_MEMBER reference version the row belongs to |
| DF-WRK-051 | queue_member | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the row comes into force |
| DF-WRK-052 | queue_member | valid_to | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Last date the row is in force |
| DF-RPT-020 | queue_measure | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the queue measure |
| DF-RPT-021 | queue_measure | queue_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The queue measured; unique with as_of |
| DF-RPT-022 | queue_measure | as_of | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the snapshot was taken |
| DF-RPT-023 | queue_measure | depth | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Open cases in the queue |
| DF-RPT-024 | queue_measure | unassigned | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Open cases with no owner |
| DF-RPT-025 | queue_measure | avg_age_days | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Average age of the open cases, days |
| DF-RPT-026 | queue_measure | max_age_days | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Age of the oldest open case, days |
| DF-RPT-027 | queue_measure | owner_min | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Fewest open cases held by one owner |
| DF-RPT-028 | queue_measure | owner_max | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Most open cases held by one owner |
| DF-RPT-029 | queue_measure | breached | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Open cases past their service level |
| DF-RPT-030 | queue_measure | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Taken, published or held |
| DF-REF-132 | parameter_catalog | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the parameter definition |
| DF-REF-133 | parameter_catalog | param_key | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Parameter key, for example case.entry.dpd |
| DF-REF-134 | parameter_catalog | kind | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Kind of parameter, for example ENVIRONMENT for an environment setting |
| DF-REF-135 | parameter_catalog | value_type | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Type of the value |
| DF-REF-136 | parameter_catalog | unit | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Unit, for example CALENDAR_DAYS, WORKING_DAYS, BAHT, PERCENT, COUNT, CODE_LIST |
| DF-REF-137 | parameter_catalog | min_value | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Lowest allowed value |
| DF-REF-138 | parameter_catalog | max_value | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Highest allowed value |
| DF-REF-139 | parameter_catalog | default_value | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Default value |
| DF-REF-140 | parameter_catalog | scope | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Product, when the parameter is keyed by product group, or global |
| DF-REF-141 | parameter_catalog | required | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | True when every product in force must have a row |
| DF-REF-142 | parameter_catalog | owner_role | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Role that owns the parameter |
| DF-REF-143 | parameter_catalog | environments | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Environments the parameter is set in |
| DF-REF-144 | parameter_catalog | used_by | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Modules and stories that read the parameter |
| DF-REF-145 | parameter_catalog | secret | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | True for a secret; its value is never returned |
| DF-REF-146 | parameter_catalog | description | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | What the parameter controls |
| DF-REF-147 | parameter_value | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the parameter value |
| DF-REF-148 | parameter_value | param_key | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Parameter, from parameter_catalog |
| DF-REF-149 | parameter_value | environment | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | DEV, SIT, UAT or PROD |
| DF-REF-150 | parameter_value | param_value | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Value as text |
| DF-REF-151 | parameter_value | product_group | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Product group for a product-scoped parameter |
| DF-REF-152 | parameter_value | version_no | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Version number |
| DF-REF-153 | parameter_value | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the value comes into force |
| DF-REF-154 | parameter_value | valid_to | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Last date the value is in force |
| DF-REF-155 | parameter_value | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Validated, approved, in force, superseded, rolled back or refused |
| DF-REF-156 | parameter_value | author_user_id | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Who loaded the value |
| DF-REF-157 | parameter_value | approver_user_id | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Who approved the value; never the author |
| DF-REF-158 | parameter_value | approved_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the value was approved |
| DF-REF-159 | reference_version | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the reference version |
| DF-REF-160 | reference_version | table_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The reference or rule table the version belongs to, for example EXPOSURE_BAND or ALLOCATION |
| DF-REF-161 | reference_version | version_no | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Version number, one above the previous version of the table |
| DF-REF-162 | reference_version | version_label | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Version label the rows carry, for example DOCTYPE-2026.11 |
| DF-REF-163 | reference_version | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the version comes into force |
| DF-REF-164 | reference_version | valid_to | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Last date the version is in force; set when the next version is approved |
| DF-REF-165 | reference_version | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Validated, approved, in force, superseded, rolled back or refused |
| DF-REF-166 | reference_version | author_user_id | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Who loaded the version |
| DF-REF-167 | reference_version | approver_user_id | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Who approved the version; never the author |
| DF-REF-168 | reference_version | approved_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the version was approved |
| DF-REF-169 | reference_version | row_count | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Rows in the version |
| DF-REF-170 | reference_version | content_hash | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | SHA-256 of the rows sorted by key; used for idempotency |
| DF-REF-171 | reference_version | load_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Identifier of the reference load request that created the version |
| DF-REF-172 | reference_version | dry_run_counts | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Counts of live cases each changed rule row would move, from the dry run |
| DF-REF-173 | reference_version | rollback_reason | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Reason given for a rollback |
| DF-REF-174 | reference_version | change_request_ref | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Reference of the change request in the bank's request tool |
| DF-REF-175 | reference_version | impact_summary | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | What the change affects, for example the open cases it touches |
| DF-REF-176 | reference_version | test_result | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Passed or failed, from the load checks or the rule table test harness |
| DF-REF-177 | reference_version | rollback_plan | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | How to return to the previous version |
| DF-REF-178 | reference_version | verified_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Who verified the change after it took effect |
| DF-REF-179 | reference_version | verified_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the change was verified |
| DF-REF-180 | reference_version | verify_note | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | What was checked |
| DF-REF-181 | reference_row | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the reference row |
| DF-REF-182 | reference_row | version_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The reference version the row belongs to; unique with row_key |
| DF-REF-183 | reference_row | row_key | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Key of the row inside its table |
| DF-REF-184 | reference_row | row_data | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Column values of the row |
| DF-REF-185 | rule_test_case | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the rule test case |
| DF-REF-186 | rule_test_case | test_case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The test case named by rule_row.test_case_id |
| DF-REF-187 | rule_test_case | route_set | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Route set |
| DF-REF-188 | rule_test_case | rule_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Rule version tested |
| DF-REF-189 | rule_test_case | rule_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Rule the test expects to hit |
| DF-REF-190 | rule_test_case | from_state | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Input state |
| DF-REF-191 | rule_test_case | event_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Input event |
| DF-REF-192 | rule_test_case | facts | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Synthetic case file facts the condition reads |
| DF-REF-193 | rule_test_case | expected_to_state | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Expected to state |
| DF-REF-194 | rule_test_case | expected_owner_role | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Expected owner role |
| DF-REF-195 | rule_test_case | expected_timer_spec | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Expected timer |
| DF-REF-196 | rule_test_case | result | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Passed or failed |
| DF-REF-197 | rule_test_case | result_detail | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Expected against actual, and the rows that hit |
| DF-REF-198 | masking_rule | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the masking rule |
| DF-REF-199 | masking_rule | role_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Role the rule applies to |
| DF-REF-200 | masking_rule | field_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | BR Field ID of a personal data field (sys_fields.is_personal true) |
| DF-REF-201 | masking_rule | unmasked | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | True when the role sees the field unmasked; no row means masked |
| DF-REF-202 | masking_rule | masking_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Version of the masking rules, for example MASK-2026.11 |
| DF-REF-203 | masking_rule | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the version comes into force |
| DF-REF-204 | masking_rule | valid_to | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Last date the version is in force |
| DF-REF-205 | role_conflict | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the role conflict |
| DF-REF-206 | role_conflict | role_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Role that may not be held with the other |
| DF-REF-207 | role_conflict | conflicts_with | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Role code, or ANY_BUSINESS_ROLE or ANY_OTHER_ROLE, per the Separation of duty sheet |
| DF-REF-208 | role_conflict | reason | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Why the pair is not allowed |
| DF-REF-209 | role_conflict | conflict_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Version of the conflict table, for example SOD-2026.11 |
| DF-REF-210 | role_conflict | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the version comes into force |
| DF-REF-211 | role_conflict | valid_to | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Last date the version is in force |
| DF-REF-212 | partner_user | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the partner user |
| DF-REF-213 | partner_user | identity_ref | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Partner identity directory ID |
| DF-REF-214 | partner_user | partner_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The firm the partner user works for |
| DF-REF-215 | partner_user | role_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The one partner role held, for example PT-LAWFIRM |
| DF-REF-216 | partner_user | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the binding starts |
| DF-REF-217 | partner_user | valid_to | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the binding ends; no later than the firm's contract end |
| DF-REF-218 | document_type | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the document type |
| DF-REF-219 | document_type | doc_type_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Document type code, the value set of LOV-DOC-TYPE |
| DF-REF-220 | document_type | label_en | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | English label |
| DF-REF-221 | document_type | label_th | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Thai label |
| DF-REF-222 | document_type | write_once | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | True for a legal type held in the write-once container |
| DF-REF-223 | document_type | retention_class | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Retention class of the type |
| DF-REF-224 | document_type | field_definitions | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Fields extracted from the type: name, label, data type, personal flag, required flag, extraction method (TEMPLATE or MODEL), review only flag and optional pattern |
| DF-REF-225 | document_type | legal_signoff_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Legal counsel user who signed the type and its fields |
| DF-REF-226 | document_type | legal_signoff_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date of the Legal sign-off |
| DF-REF-227 | document_type | npa_signoff_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Head of NPA user who signed the type and its fields |
| DF-REF-228 | document_type | npa_signoff_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date of the NPA sign-off |
| DF-REF-229 | document_type | table_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Version of the type table, for example DOCTYPE-2026.11 |
| DF-REF-230 | document_type | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the version comes into force |
| DF-REF-231 | document_type | valid_to | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Last date the version is in force |
| DF-REF-232 | document_type | reference_version_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Reference version that brought the row |
| DF-REF-233 | document_type | classify_threshold | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Confidence below which a document of this type goes to the review queue |
| DF-REF-234 | document_checklist_item | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the checklist item |
| DF-REF-235 | document_checklist_item | stage_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Case stage the row applies to |
| DF-REF-236 | document_checklist_item | route_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Route the row applies to; empty for every route |
| DF-REF-237 | document_checklist_item | document_type | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Document type |
| DF-REF-238 | document_checklist_item | required | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | True when the type is required for the stage and route |
| DF-REF-239 | document_checklist_item | sort_order | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Order of the item on the checklist |
| DF-REF-240 | document_checklist_item | table_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Version of the checklist, for example CHK-2026.11 |
| DF-REF-241 | document_checklist_item | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the version comes into force |
| DF-REF-242 | document_checklist_item | valid_to | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Last date the version is in force |
| DF-REF-243 | document_checklist_item | reference_version_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Reference version that brought the row |
| DF-DOC-036 | case_document_check | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the completeness check |
| DF-DOC-037 | case_document_check | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Case checked; one row per case; unique |
| DF-DOC-038 | case_document_check | checklist_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Checklist version used |
| DF-DOC-039 | case_document_check | required_count | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Number of required types |
| DF-DOC-040 | case_document_check | present_count | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Number of required types present |
| DF-DOC-041 | case_document_check | missing_types | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Required types not present |
| DF-DOC-042 | case_document_check | complete | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | True when every required type is present; empty when the stage has no checklist |
| DF-DOC-043 | case_document_check | checked_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the check last ran |
| DF-DOC-044 | case_document_check | last_event_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Event that triggered the last check, for repeat detection |
| DF-REF-244 | document_hub_parameter | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the document hub parameter |
| DF-REF-245 | document_hub_parameter | param_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Parameter code, for example INTAKE_MAX_FILE_MB, OCR_MIN_QUALITY, CLASSIFY_THRESHOLD, CASE_NO_PATTERN, SEARCH_MAX_RESULTS |
| DF-REF-246 | document_hub_parameter | param_value | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Parameter value as text, typed by the reader |
| DF-REF-247 | document_hub_parameter | unit | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Unit of the value, for example MB, seconds, ratio |
| DF-REF-248 | document_hub_parameter | table_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Version of the parameter load |
| DF-REF-249 | document_hub_parameter | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the value comes into force |
| DF-REF-250 | document_hub_parameter | valid_to | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Last date the value is in force |
| DF-REF-251 | document_hub_parameter | reference_version_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Reference version that brought the row |
| DF-DOC-045 | document_intake | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the intake item |
| DF-DOC-046 | document_intake | source | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Source of the file |
| DF-DOC-047 | document_intake | source_ref | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Path, partner reference or email message ID at the channel |
| DF-DOC-048 | document_intake | channel_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Branch code, MAILROOM, partner code or mailbox code |
| DF-DOC-049 | document_intake | file_name | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | File name as received; personal where it names a customer |
| DF-DOC-050 | document_intake | file_size | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | File size in bytes |
| DF-DOC-051 | document_intake | captured_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Scan time recorded by the scanner, for scanner files |
| DF-DOC-052 | document_intake | sender_address | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Sender email address for mailbox items; masked by role |
| DF-DOC-053 | document_intake | partner_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Partner that sent the file by SFTP |
| DF-DOC-054 | document_intake | run_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | JOB-12 run that took the item in |
| DF-DOC-055 | document_intake | received_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the Workbench received the file |
| DF-DOC-056 | document_intake | file_sha256 | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | SHA-256 of the file |
| DF-DOC-057 | document_intake | intake_ref | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Received file in the intake container |
| DF-DOC-058 | document_intake | scan_result | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Malware scan result: clean or infected; empty until scanned |
| DF-DOC-059 | document_intake | scanned_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the malware scan ran |
| DF-DOC-060 | document_intake | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Case the item belongs to once known |
| DF-DOC-061 | document_intake | document_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Document created from the item, or the uploaded document |
| DF-DOC-062 | document_intake | ocr_ref | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | OCR JSON output (text and layout) in the standard container |
| DF-DOC-063 | document_intake | ocr_status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Pending, done, rescan or failed |
| DF-DOC-064 | document_intake | ocr_attempts | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Number of OCR calls made for the item |
| DF-DOC-065 | document_intake | page_count | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Number of pages read |
| DF-DOC-066 | document_intake | rescan_pages | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Page numbers below the OCR quality threshold |
| DF-DOC-067 | document_intake | ocr_quality | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Lowest page quality of the item |
| DF-DOC-068 | document_intake | languages | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Languages found, for example th,en |
| DF-DOC-069 | document_intake | ocr_engine_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Version of the OCR service that read the item |
| DF-DOC-070 | document_intake | predicted_type | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Type with the highest classification score |
| DF-DOC-071 | document_intake | classification_confidence | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Score of the predicted type |
| DF-DOC-072 | document_intake | type_candidates | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Top two types with their scores |
| DF-DOC-073 | document_intake | classifier_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Model version that classified the item |
| DF-DOC-074 | document_intake | classify_fallback | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | True when the classifier did not answer and the item went to a person |
| DF-DOC-075 | document_intake | match_status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Pending, matched, no match, multiple, conflict, case closed or no type |
| DF-DOC-076 | document_intake | candidate_case_ids | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Cases found for the item when more than one or none can be chosen by rule |
| DF-DOC-077 | document_intake | extracted_fields | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Fields read before the item is attached: field name, value, extracted value, confidence, state, extractor version, personal flag |
| DF-DOC-078 | document_intake | extract_status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Pending, done or failed |
| DF-DOC-079 | document_intake | extract_attempts | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Number of extraction attempts |
| DF-DOC-080 | document_intake | review_reason | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Why the item needs a person: rescan, unreadable file, low confidence, model unavailable, unknown type |
| DF-DOC-081 | document_intake | review_outcome | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Attached or discarded once a person resolves the review item |
| DF-DOC-082 | document_intake | resolved_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Who resolved the review item |
| DF-DOC-083 | document_intake | resolved_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the review item was resolved |
| DF-DOC-084 | document_intake | discard_reason | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Reason given when a review item is discarded |
| DF-DOC-085 | document_text | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the page text |
| DF-DOC-086 | document_text | intake_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Intake item the page belongs to; unique with page_no |
| DF-DOC-087 | document_text | document_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Document the page belongs to once attached |
| DF-DOC-088 | document_text | page_no | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Page number |
| DF-DOC-089 | document_text | text_content | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | OCR text of the page; masked by role on read |
| DF-DOC-090 | document_text | quality | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Mean word confidence of the page |
| DF-DOC-091 | retention_action | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the retention action |
| DF-DOC-092 | retention_action | document_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Document acted on; unique with run_month |
| DF-DOC-093 | retention_action | run_month | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Month of the JOB-17 run, YYYY-MM |
| DF-DOC-094 | retention_action | action | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Archived, listed, held or exception |
| DF-DOC-095 | retention_action | decision_log_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | DOCRET decision log entry for an archive |
| DF-REF-252 | merge_field | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the merge field |
| DF-REF-253 | merge_field | merge_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Code written in the template body, for example CASE_NO |
| DF-REF-254 | merge_field | source_entity | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Entity that holds the value |
| DF-REF-255 | merge_field | source_field | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Field that holds the value |
| DF-REF-256 | merge_field | field_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | BR Field ID of the source field in the data dictionary |
| DF-REF-257 | merge_field | is_required | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | True when generation holds on an empty value |
| DF-REF-258 | merge_field | personal_data | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | True when the value is personal data, detokenized only at generation |
| DF-REF-259 | merge_field | catalog_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Version of the catalog load |
| DF-REF-260 | merge_field | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the catalog version comes into force |
| DF-DOC-096 | signature_request | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the signature request |
| DF-DOC-097 | signature_request | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Case |
| DF-DOC-098 | signature_request | treatment_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Treatment the agreement belongs to |
| DF-DOC-099 | signature_request | document_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Generated document sent for signature |
| DF-DOC-100 | signature_request | party_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Signing party |
| DF-DOC-101 | signature_request | method | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | E-signature, branch or paper |
| DF-DOC-102 | signature_request | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Queued, sent, signed, declined or expired |
| DF-DOC-103 | signature_request | external_ref | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | EasyApp reference |
| DF-DOC-104 | signature_request | sent_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the request was sent |
| DF-DOC-105 | signature_request | signed_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the party signed |
| DF-DOC-106 | signature_request | signed_document_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Signed copy or branch scan |
| DF-DOC-107 | signature_request | expires_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | End of the offer validity |
| DF-DEC-032 | approval | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the approval |
| DF-DEC-033 | approval | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The case |
| DF-DEC-034 | approval | decision_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Decision to approve |
| DF-DEC-035 | approval | regulation_item | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Delegation item, for example 2.1.1 |
| DF-DEC-036 | approval | capability_area | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Area whose A letter the approver needs |
| DF-DEC-037 | approval | route_role_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Role for a decision with no amount limit, for example RW-LITOFF |
| DF-DEC-038 | approval | approval_level | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Required level L1 to L6 |
| DF-DEC-039 | approval | delegation_limit_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Delegation row that covers the item |
| DF-DEC-040 | approval | limit_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Delegation version the item routed under |
| DF-DEC-041 | approval | product_group | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Product group |
| DF-DEC-042 | approval | amount | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Principal used for the limit, baht |
| DF-DEC-043 | approval | terms | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Proposed and changed terms |
| DF-DEC-044 | approval | prepared_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Person or service identity that prepared the item |
| DF-DEC-045 | approval | assigned_user_id | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Holder the item is assigned to; empty for a role route |
| DF-DEC-046 | approval | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Waiting, held with no limit, approved, refused or returned |
| DF-DEC-047 | approval | due_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the service level ends |
| DF-DEC-048 | approval | escalation_level | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Times escalated |
| DF-DEC-049 | approval | source_type | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | What asked for approval, for example NOTICE or TREATMENT |
| DF-DEC-050 | approval | source_ref | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | ID of the source record, for example the notice ID |
| DF-DEC-051 | approval | rule_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Rule that asked for approval |
| DF-DEC-052 | approval | rule_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Version of that rule |
| DF-DEC-053 | approval | decision_log_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Decision log entry of the outcome |
| DF-REF-261 | payment_match_rule | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the payment match rule |
| DF-REF-262 | payment_match_rule | rule_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Row code, for example EXACT |
| DF-REF-263 | payment_match_rule | rule_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Parameter version, for example PM-2026.12 |
| DF-REF-264 | payment_match_rule | match_type | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Exact, window or partial |
| DF-REF-265 | payment_match_rule | amount_tolerance_pct | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Allowed difference from the installment, 0 to 100 percent |
| DF-REF-266 | payment_match_rule | window_days_before | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Days before the due date a payment may arrive |
| DF-REF-267 | payment_match_rule | window_days_after | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Days after the due date a payment may arrive |
| DF-REF-268 | payment_match_rule | grace_days | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Days after the due date before PaymentMissed is raised |
| DF-REF-269 | payment_match_rule | partial_floor_pct | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Lowest share of the installment matched as partial, percent |
| DF-REF-270 | payment_match_rule | priority | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Order in which rows are tried |
| DF-REF-271 | payment_match_rule | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the version comes into force |
| DF-REF-272 | payment_match_rule | valid_to | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Last date the version is in force |
| DF-REF-273 | payment_match_rule | approved_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Credit Administration approver |
| DF-RPT-031 | measure_definition | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the measure definition |
| DF-RPT-032 | measure_definition | measure_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Measure code |
| DF-RPT-033 | measure_definition | name | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Measure name |
| DF-RPT-034 | measure_definition | formula | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Formula in plain terms |
| DF-RPT-035 | measure_definition | data_product | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Data product the measure reads |
| DF-RPT-036 | measure_definition | unit | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Count, baht, days or percent |
| DF-RPT-037 | measure_definition | definition_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Definition version, for example MD-2026.11 |
| DF-RPT-038 | measure_definition | approved_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Tribe lead who approved |
| DF-RPT-039 | measure_definition | approved_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Approval time |
| DF-RPT-040 | measure_definition | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the definition comes into force |
| DF-RPT-041 | measure_snapshot | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the measure snapshot |
| DF-RPT-042 | measure_snapshot | measure_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Measure, from measure_definition |
| DF-RPT-043 | measure_snapshot | definition_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Definition version used |
| DF-RPT-044 | measure_snapshot | business_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Business date measured |
| DF-RPT-045 | measure_snapshot | product_group | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Product group |
| DF-RPT-046 | measure_snapshot | dimension_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Dimension: route, age band, queue, stage or agent |
| DF-RPT-047 | measure_snapshot | dimension_value | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Value of the dimension |
| DF-RPT-048 | measure_snapshot | value | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Measure value |
| DF-RPT-049 | measure_snapshot | case_count | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Cases behind the value |
| DF-RPT-050 | measure_snapshot | is_baseline | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | True for a row of the baseline date |
| DF-RPT-051 | measure_snapshot | frozen | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | True when the row may not change |
| DF-RPT-052 | measure_snapshot | published_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When published |
| DF-RPT-053 | measure_publish | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the measure publish |
| DF-RPT-054 | measure_publish | business_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Business date |
| DF-RPT-055 | measure_publish | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Published or held |
| DF-RPT-056 | measure_publish | case_list_count | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Open cases on the case list at the cut-off |
| DF-RPT-057 | measure_publish | dashboard_count | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Open cases in the dashboard facts |
| DF-RPT-058 | measure_publish | held_reason | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Why the publish is held |
| DF-AGT-001 | agent_policy | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the agent policy version |
| DF-AGT-002 | agent_policy | agent_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER |
| DF-AGT-003 | agent_policy | policy_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Policy version, for example P1 |
| DF-AGT-004 | agent_policy | model_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Model deployment the agent calls through the gateway |
| DF-AGT-005 | agent_policy | model_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Model version the policy uses |
| DF-AGT-006 | agent_policy | output_schema_ref | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Reference to the JSON Schema the answer must meet |
| DF-AGT-007 | agent_policy | allowed_tools | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Tools the agent may call through the tool gateway |
| DF-AGT-008 | agent_policy | autonomy_mode | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Off, shadow or L1 |
| DF-AGT-009 | agent_policy | segment_product_group | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Product group the mode applies to; empty for all |
| DF-AGT-010 | agent_policy | segment_region_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Region the mode applies to; empty for all |
| DF-AGT-011 | agent_policy | confidence_floor | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Answers below this confidence fall back or are marked for review |
| DF-AGT-012 | agent_policy | timeout_seconds | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Seconds the gateway waits before the rule result is used |
| DF-AGT-013 | agent_policy | daily_cost_cap_thb | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Daily model cost limit per agent, baht |
| DF-AGT-014 | agent_policy | price_per_1k_tokens_thb | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Model price per 1,000 tokens, baht |
| DF-AGT-015 | agent_policy | alert_role | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Role that receives cost and drift alerts |
| DF-AGT-016 | agent_policy | review_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the version is reviewed again, for a parked or shadow agent |
| DF-AGT-017 | agent_policy | evaluation_run_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Evaluation run an autonomy step is based on |
| DF-AGT-018 | agent_policy | promotion_conditions | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Conditions the evaluation must meet for the stated mode |
| DF-AGT-019 | agent_policy | watch_measures | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Measures and limits to watch after the step, including the drift threshold and minimum feedback |
| DF-AGT-020 | agent_policy | fallback_rule | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Rule applied when the agent does not answer, for example R-UNI-32 |
| DF-AGT-021 | agent_policy | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Loaded, approved or retired |
| DF-AGT-022 | agent_policy | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the version takes effect |
| DF-AGT-023 | agent_policy | valid_to | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Last date the version is in force |
| DF-AGT-024 | agent_policy | loaded_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Who loaded the version |
| DF-AGT-025 | agent_policy | approved_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Who approved the version |
| DF-AGT-026 | agent_prompt | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the agent prompt version |
| DF-AGT-027 | agent_prompt | agent_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER |
| DF-AGT-028 | agent_prompt | prompt_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Prompt version, for example PR1 |
| DF-AGT-029 | agent_prompt | body_text | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Prompt text with placeholders; no personal data |
| DF-AGT-030 | agent_prompt | body_hash | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | SHA-256 of the prompt text |
| DF-AGT-031 | agent_prompt | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Loaded, approved or retired |
| DF-AGT-032 | agent_prompt | valid_from | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Date the version takes effect |
| DF-AGT-033 | agent_prompt | valid_to | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Last date the version is in force |
| DF-AGT-034 | agent_prompt | loaded_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Who loaded the version |
| DF-AGT-035 | agent_prompt | approved_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Who approved the version |
| DF-AGT-036 | agent_run | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the agent run |
| DF-AGT-037 | agent_run | agent_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER |
| DF-AGT-038 | agent_run | agent_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Agent, policy and prompt version as <agent>@<policy>/<prompt> |
| DF-AGT-039 | agent_run | prompt_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Prompt version used |
| DF-AGT-040 | agent_run | model_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Model version used |
| DF-AGT-041 | agent_run | case_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The case the run is for |
| DF-AGT-042 | agent_run | subject_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Document, legal action or treatment the run is about, where not the case |
| DF-AGT-043 | agent_run | autonomy_mode | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Mode the run used: shadow or L1 |
| DF-AGT-044 | agent_run | trigger_event | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | CaseCreated, DocumentStored, STEP or EVALUATION |
| DF-AGT-045 | agent_run | idempotency_key | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Unique key of the run request |
| DF-AGT-046 | agent_run | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Answered, timed out, guardrail failed, below floor, tool unavailable, model error or disabled |
| DF-AGT-047 | agent_run | fallback | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | True when the rule result was used instead of the answer |
| DF-AGT-048 | agent_run | guardrail_result | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Failed check codes and details |
| DF-AGT-049 | agent_run | output | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Checked answer, masked; never returned for shadow runs |
| DF-AGT-050 | agent_run | confidence | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Confidence of the answer |
| DF-AGT-051 | agent_run | latency_ms | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Time from call to answer or timeout, milliseconds |
| DF-AGT-052 | agent_run | tokens_in | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Input tokens returned by the endpoint |
| DF-AGT-053 | agent_run | tokens_out | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Output tokens returned by the endpoint |
| DF-AGT-054 | agent_run | cost_thb | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Cost of the run, baht |
| DF-AGT-055 | agent_run | data_as_of | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Oldest business date of the inputs used |
| DF-AGT-056 | agent_run | run_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the run started |
| DF-AGT-057 | agent_run | evaluation_run_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Evaluation run the run belongs to, if any |
| DF-AGT-058 | agent_run | decision_log_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Decision log entry written for the step that used the run |
| DF-AGT-059 | agent_run | segment_product_group | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Product group of the case at run time |
| DF-AGT-060 | agent_run | segment_region_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Region of the case at run time |
| DF-AGT-061 | agent_sample | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the sample row |
| DF-AGT-062 | agent_sample | agent_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER |
| DF-AGT-063 | agent_sample | sample_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Sample code, for example INTAKE-S1 |
| DF-AGT-064 | agent_sample | sample_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Version of the sample |
| DF-AGT-065 | agent_sample | subject_type | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Case, document or legal action |
| DF-AGT-066 | agent_sample | subject_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | The case, document or legal action labeled |
| DF-AGT-067 | agent_sample | label_key | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Gap type, deviation code, field name or checklist item |
| DF-AGT-068 | agent_sample | expected_value | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Labeled value; SHA-256 hash for personal values |
| DF-AGT-069 | agent_sample | labeled_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Who labeled the row |
| DF-AGT-070 | agent_evaluation_run | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the evaluation run |
| DF-AGT-071 | agent_evaluation_run | agent_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER |
| DF-AGT-072 | agent_evaluation_run | sample_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Sample used |
| DF-AGT-073 | agent_evaluation_run | sample_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Sample version used |
| DF-AGT-074 | agent_evaluation_run | policy_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Policy version evaluated |
| DF-AGT-075 | agent_evaluation_run | prompt_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Prompt version evaluated |
| DF-AGT-076 | agent_evaluation_run | model_version | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Model version evaluated |
| DF-AGT-077 | agent_evaluation_run | status | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Running, done or failed |
| DF-AGT-078 | agent_evaluation_run | started_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the run started |
| DF-AGT-079 | agent_evaluation_run | finished_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the run ended |
| DF-AGT-080 | agent_evaluation_run | requested_by | Staff identifier | Internal | Yes | Shown as the person's name to bank users | Employment and legitimate interest (PDPA section 24) | Per data product (DL26) | Who started the run |
| DF-AGT-081 | agent_evaluation_run | total_cost_thb | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Cost of all runs in the evaluation, baht |
| DF-AGT-082 | agent_evaluation_run | p95_latency_ms | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | 95th percentile latency, milliseconds |
| DF-AGT-083 | agent_evaluation_run | failure_counts | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Count of runs by failure status and check code |
| DF-AGT-084 | agent_evaluation_run | proposal | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Proposed approach and confidence threshold per document type |
| DF-AGT-085 | agent_evaluation_run | review_count | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Proposals below the confidence floor, scored separately |
| DF-AGT-086 | agent_evaluation | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the evaluation score |
| DF-AGT-087 | agent_evaluation | evaluation_run_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Evaluation run the score belongs to |
| DF-AGT-088 | agent_evaluation | approach | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Agent, OCR template, model, or OCR and model |
| DF-AGT-089 | agent_evaluation | label_key | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Gap type, code, field or item scored |
| DF-AGT-090 | agent_evaluation | sample_size | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Labeled subjects scored |
| DF-AGT-091 | agent_evaluation | true_positive | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | True positives |
| DF-AGT-092 | agent_evaluation | false_positive | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | False positives |
| DF-AGT-093 | agent_evaluation | false_negative | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | False negatives |
| DF-AGT-094 | agent_evaluation | agreement_rate | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Share of subjects where the answer equals the label |
| DF-AGT-095 | agent_evaluation | precision_value | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | TP / (TP + FP) |
| DF-AGT-096 | agent_evaluation | recall_value | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | TP / (TP + FN) |
| DF-AGT-097 | agent_feedback | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the feedback |
| DF-AGT-098 | agent_feedback | agent_run_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Agent run the feedback is on |
| DF-AGT-099 | agent_feedback | item_key | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | SUMMARY for the intake summary, or the deviation code |
| DF-AGT-100 | agent_feedback | verdict | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Accepted, corrected or rejected |
| DF-AGT-101 | agent_feedback | reason | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Reason for a correction or a rejection |
| DF-AGT-102 | agent_feedback | decision_log_id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Decision log entry written for the feedback |
| DF-AGT-103 | agent_alert | id | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Record identifier of the alert |
| DF-AGT-104 | agent_alert | agent_code | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Agent or model, for example INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER |
| DF-AGT-105 | agent_alert | alert_type | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Cost cap or drift |
| DF-AGT-106 | agent_alert | segment | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Product group and region, or ALL |
| DF-AGT-107 | agent_alert | business_date | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Business date measured |
| DF-AGT-108 | agent_alert | measured_value | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Cost in baht or acceptance rate measured |
| DF-AGT-109 | agent_alert | threshold_value | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Limit the value was compared with |
| DF-AGT-110 | agent_alert | sent_to_role | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | Role notified |
| DF-AGT-111 | agent_alert | sent_at | Not personal | Internal | No | Shown by permission | Not applicable | Per data product (DL26) | When the notification was sent; empty until sent |

## Summary

| Fields by category |  |  |
|---|---|---|
| Calculated from the Fields tab. |  |  |
| Category | Classification | Fields |
| Direct identifier | Restricted |  |
| Sensitive | Restricted |  |
| Indirect identifier | Confidential |  |
| Customer data | Confidential |  |
| Staff identifier | Internal |  |
| Not personal | Internal |  |
| Total |  |  |

## Identifiers

| Fields that identify a person |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| 25 fields that identify a person directly or indirectly, or carry sensitive data. These drive masking, test data and agent prompts. |  |  |  |  |  |  |
| BR Field ID | Entity | Field | Category | Classification | On screen | Meaning |
| DF-CAS-002 | recovery_case | case_no | Indirect identifier | Confidential | Shown within the role's scope; masked in UAT | Case number RW-YYYY-NNNNNN, issued at creation and never reused |
| DF-PTY-002 | party | cif_no | Indirect identifier | Confidential | Shown within the role's scope; masked in UAT | Customer number in the bank |
| DF-PTY-004 | party | first_name | Direct identifier | Restricted | Masked unless the role may see it | First name or company name |
| DF-PTY-005 | party | last_name | Direct identifier | Restricted | Masked unless the role may see it | Last name |
| DF-PTY-007 | party | id_no_token | Direct identifier | Restricted | Masked unless the role may see it | Tokenized identity number. The clear value is never stored in the Workbench |
| DF-PTY-008 | party | date_of_birth | Direct identifier | Restricted | Masked unless the role may see it | Date of birth |
| DF-PTY-010 | party | vulnerable_flag | Sensitive | Restricted | Masked unless the role handles the deviation | Vulnerable customer or hardship confirmed |
| DF-PTY-011 | party | deceased_flag | Sensitive | Restricted | Masked unless the role handles the deviation | Death confirmed |
| DF-PTY-012 | party | bankruptcy_flag | Sensitive | Restricted | Masked unless the role handles the deviation | Bankruptcy or receivership confirmed |
| DF-PTY-016 | contact_point | value_token | Direct identifier | Restricted | Masked unless the role may see it | The number, handle or address, stored masked |
| DF-ACC-002 | loan_account | account_no | Indirect identifier | Confidential | Shown within the role's scope; masked in UAT | Account number |
| DF-ACC-003 | loan_account | contract_no | Indirect identifier | Confidential | Shown within the role's scope; masked in UAT | Contract number |
| DF-COL-004 | collateral | title_doc_no | Indirect identifier | Confidential | Shown within the role's scope; masked in UAT | Title deed or registration number |
| DF-COL-005 | collateral | plot_no | Indirect identifier | Confidential | Shown within the role's scope; masked in UAT | Plot number |
| DF-COL-008 | collateral | district | Indirect identifier | Confidential | Shown within the role's scope; masked in UAT | District |
| DF-COL-009 | collateral | subdistrict | Indirect identifier | Confidential | Shown within the role's scope; masked in UAT | Subdistrict |
| DF-COL-021 | valuation | appraisal_no | Indirect identifier | Confidential | Shown within the role's scope; masked in UAT | Appraisal number |
| DF-LEG-005 | legal_action | lawsuit_no | Indirect identifier | Confidential | Shown within the role's scope; masked in UAT | Lawsuit reference in LIT |
| DF-LEG-006 | legal_action | black_case_no | Indirect identifier | Confidential | Shown within the role's scope; masked in UAT | Court black case number |
| DF-LEG-007 | legal_action | red_case_no | Indirect identifier | Confidential | Shown within the role's scope; masked in UAT | Court red case number after judgment |
| DF-LEG-020 | notice | barcode | Indirect identifier | Confidential | Shown within the role's scope; masked in UAT | Registered mail barcode |
| DF-SAL-034 | debt_sale_account | borrower_code | Indirect identifier | Confidential | Shown within the role's scope; masked in UAT | Borrower code |
| DF-INT-011 | interaction | summary | Direct identifier | Restricted | Masked unless the role may see it | Summary of what was said |
| DF-DOC-006 | document | storage_ref | Indirect identifier | Confidential | Shown within the role's scope; masked in UAT | Reference to the stored file |
| DF-DOC-015 | document_field | field_value | Direct identifier | Restricted | Masked unless the role may see it | Value read, masked where personal |

## Handling

| Handling rule by classification |  |  |
|---|---|---|
| What each classification means for storage, screens, logs, prompts, test data and export. |  |  |
| Classification | Where | Rule |
| Restricted | Stored | Identity numbers tokenized; other fields encrypted at rest |
| Restricted | On screen | Masked unless the role is allowed to see the field for cases in its scope |
| Restricted | In logs | Never written to application logs. Every read is logged through PII Kafka |
| Restricted | In agent prompts | Removed or masked before a prompt is built |
| Restricted | In test data | Synthetic in DEV. Masked copies in SIT and UAT |
| Restricted | Export | Blocked except through an approved extract, logged with the requester |
| Restricted | Debt sale tape | Only the fields the sale terms allow, after the award |
| Confidential | Stored | Encrypted at rest and in transit |
| Confidential | On screen | Shown within the role's scope. Indirect identifiers masked in UAT |
| Confidential | In agent prompts | Only the fields the agent's step needs |
| Confidential | Export | Within the role's scope, logged |
| Internal | Stored | Encrypted at rest and in transit |
| Internal | On screen | By permission |
| All | Retention | Set per data product and document type by Compliance (DL26). A legal hold overrides retention |
| All | Data subject request | Access, correction or erasure routed to Compliance inside the statutory period; automated processing on the case is held (R-UNI-11) |

## Who sees what

| Who sees personal data unmasked |  |  |  |
|---|---|---|---|
| Proposed until Compliance issues the masking rules (DL26). Held as data, so a change needs no release. |  |  |  |
| Role | Scope | Direct identifiers | Sensitive flags |
| Case owner | Own cases | Unmasked | Masked unless the case has the deviation |
| Team manager | Team | Unmasked | Masked |
| Restructuring, litigation, enforcement, guarantee, sale, NPA and debt sale officers | Team | Unmasked | Masked |
| Hardship and vulnerability specialist, complaint officer, fraud investigator | Cases with their deviation | Unmasked | Unmasked |
| Legal counsel | All | Unmasked | Unmasked |
| Phone and field collectors | Own cases | Name and contact points only | Masked |
| Credit Administration and the write-off team | All | Unmasked | Masked |
| Compliance and PDPA officer | All | Unmasked | Unmasked |
| Internal audit | All | Unmasked, read only, logged | Unmasked, read only, logged |
| Center of excellence, reporting and BI, data steward, Risk | All | Masked | Masked |
| Platform, security and reference data administrators | All | Masked | Masked |
| Partner users | Placed cases | Name, contact points and what the instruction needs | Masked |
| Agents | As the step needs | Removed or masked | Removed or masked |

## Key

| Key |  |  |
|---|---|---|
| What each category and class means. |  |  |
| Item | Term | Meaning |
| Category | Direct identifier | Identifies a person on its own: name, identity number, date of birth, contact point, free text about them |
| Category | Sensitive | May reveal health, death or insolvency. Handled as sensitive data under PDPA section 26 |
| Category | Indirect identifier | Identifies a person when joined to other data: account, contract, case, lawsuit, title deed |
| Category | Customer data | Data about an identified customer's debt, case, assets or contacts |
| Category | Staff identifier | Identifies a bank employee or a partner user |
| Category | Not personal | Reference, configuration, partner company or asset data |
| Class | Restricted | Highest protection: tokenized or masked, never in logs or prompts |
| Class | Confidential | Customer data shown within scope, encrypted |
| Class | Internal | Bank internal data shown by permission |
| Standard | Thai PDPA | Personal Data Protection Act B.E. 2562 |

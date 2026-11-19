<!-- source: 07 Screens and experience/Recovery Workbench Screen Specifications v1.md -->
<!-- converted: 2026-11-04 from Markdown (copied) -->

> **Source:** `07 Screens and experience/Recovery Workbench Screen Specifications v1.md`  
> **Converted from:** Markdown (copied)

# Recovery Workbench screen specifications

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

Each screen with its fields, states, validation and messages, and the stories that build it. Components and states follow the design system; wording follows the error and message standard and the content and label standard. How the front end is split into modules is open under DL07; the screen design owner is DL31.

## SCR-01 My work

| Item | Value |
|---|---|
| Menu | Home |
| What it is for | The person's open tasks, cases near a deadline and approvals waiting |
| Reached from | Sign-in |
| Module | P3 |
| Access | Case record, checked on every request |
| Who reaches it | All bank roles |
| First in | E2 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Loading; empty; list.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| task.task_code | The task in the case model, for example VERIFY_PACK | varchar(60) | Yes | None | Edit | No |
| task.element_type | Human, customer, partner or decision task, milestone, event listener | varchar(20) | Yes | LOV-ELEMENT | Edit | No |
| task.discretion | Automatic, discretionary, required | varchar(15) | Yes | LOV-DISCRETION | Edit | No |
| task.status | Open, in progress, done, canceled | varchar(15) | Yes | LOV-TASK-STATUS | Edit | No |
| task.owner_role | Role that owns the task | varchar(20) | No | LOV-ROLE | Edit | No |
| task.due_at | When the task is due | timestamptz | No | None | Read | No |
| task.completed_at | When it completed | timestamptz | No | None | Read | No |
| task.outcome_code | The event the task produced | varchar(40) | No | None | Edit | No |
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | Edit | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | Read | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | Edit | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | Edit | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | Edit | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | Edit | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | Edit | No |
| recovery_case.team_code | The owning team, used by scope rules | varchar(20) | No | LOV-TEAM | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P3-011 | Allocation summary, cases in overflow (RWB-E1-020) | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P3-012 | Allocation summary, no row matched (RWB-E1-020) | {count} new cases matched no allocation row and are in the exception queue. |
| MSG-P3-001 | A transfer without a reason | Choose a reason for the transfer. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-02 Case list

| Item | Value |
|---|---|
| Menu | Cases |
| What it is for | Every case in the person's scope, with filters by product, stage, owner, age and deviation |
| Reached from | Menu |
| Module | P3 |
| Access | Case record, checked on every request |
| Who reaches it | Case owner, team manager, officers, product heads, control functions |
| First in | E1 |
| Stories | RWB-E1-018, RWB-E1-019, RWB-E1-020, RWB-E1-021, RWB-E1-023, RWB-E1-028, RWB-E1-029, RWB-E1-031, RWB-E1-042, RWB-E1-044, RWB-E1-045, RWB-E1-048, RWB-E2-004, RWB-E2-011, RWB-E2-015 |

**States.** Loading; empty; list; filtered.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | Edit | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | Read | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | Edit | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | Edit | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | Edit | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | Edit | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | Edit | No |
| recovery_case.team_code | The owning team, used by scope rules | varchar(20) | No | LOV-TEAM | Edit | No |
| recovery_case.region_code | The owning region, used by scope rules | varchar(10) | No | LOV-REGION | Edit | No |
| recovery_case.entry_date | The date the case entered recovery | date | Yes | None | Edit | No |
| recovery_case.dpd_at_entry | Days past due on the entry date | integer | Yes | None | Read | No |
| recovery_case.exposure_band | Exposure band set from the outstanding balance at entry | varchar(10) | No | LOV-EXPOSURE | Edit | No |
| recovery_case.total_outstanding_at_entry | Total outstanding across linked accounts at entry, in baht | numeric(18,2) | Yes | None | Read | No |
| recovery_case.prescription_date | The earliest date a legal claim on the case expires | date | No | None | Edit | No |
| recovery_case.stage_clock_start | When the current state started, for the service level | timestamptz | No | None | Edit | No |
| recovery_case.deviation_open | True while any deviation X1 to X7 is open | boolean | Yes | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P3-011 | Allocation summary, cases in overflow (RWB-E1-020) | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P3-002 | Transfer to an owner at the caseload cap | {owner} is at the caseload cap. Choose another owner or the team queue. |
| MSG-P3-004 | Case on hold for a deviation | This case is on hold for {deviation}. The prescription date is still {date}. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-03 Case record

| Item | Value |
|---|---|
| Menu | Cases |
| What it is for | One case: accounts, parties, stage, owner, clocks, deviations, documents, decisions and history on one timeline |
| Reached from | Case list; my work; search |
| Module | P3 |
| Access | Case record, checked on every request |
| Who reaches it | Every bank role in scope |
| First in | E1 read only; E2 full |
| Stories | RWB-E1-018, RWB-E1-021, RWB-E1-023, RWB-E1-028, RWB-E1-035, RWB-E1-042, RWB-E2-004, RWB-E2-015, RWB-E2-016 |

**States.** Loading; read only; editable; on hold.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | Edit | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | Read | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | Edit | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | Edit | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | Edit | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | Edit | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | Edit | No |
| recovery_case.team_code | The owning team, used by scope rules | varchar(20) | No | LOV-TEAM | Edit | No |
| recovery_case.region_code | The owning region, used by scope rules | varchar(10) | No | LOV-REGION | Edit | No |
| recovery_case.entry_date | The date the case entered recovery | date | Yes | None | Edit | No |
| recovery_case.dpd_at_entry | Days past due on the entry date | integer | Yes | None | Read | No |
| recovery_case.exposure_band | Exposure band set from the outstanding balance at entry | varchar(10) | No | LOV-EXPOSURE | Edit | No |
| recovery_case.total_outstanding_at_entry | Total outstanding across linked accounts at entry, in baht | numeric(18,2) | Yes | None | Read | No |
| recovery_case.prescription_date | The earliest date a legal claim on the case expires | date | No | None | Edit | No |
| recovery_case.stage_clock_start | When the current state started, for the service level | timestamptz | No | None | Edit | No |
| recovery_case.deviation_open | True while any deviation X1 to X7 is open | boolean | Yes | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P3-002 | Transfer to an owner at the caseload cap | {owner} is at the caseload cap. Choose another owner or the team queue. |
| MSG-P3-011 | Allocation summary, cases in overflow (RWB-E1-020) | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P3-001 | A transfer without a reason | Choose a reason for the transfer. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-04 Case timeline

| Item | Value |
|---|---|
| Menu | Cases |
| What it is for | Every action, decision, transfer, letter and document on the case, with filters |
| Reached from | Case record |
| Module | P3 |
| Access | Case record, checked on every request |
| Who reaches it | Every bank role in scope |
| First in | E2 |
| Stories | RWB-E2-016 |

**States.** Loading; filtered.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| interaction.occurred_at | When it happened | timestamptz | Yes | None | Read | No |
| interaction.channel | Call, visit, SMS, LINE, email, letter, portal, branch | varchar(15) | Yes | LOV-CHANNEL | Edit | No |
| interaction.direction | Inbound or outbound | varchar(8) | Yes | LOV-DIRECTION | Edit | No |
| interaction.action_code | Action code | varchar(10) | No | LOV-ACTION-CODE | Read | No |
| interaction.contact_result | Right party, third party, no answer, wrong number | varchar(20) | No | LOV-CONTACT-RESULT | Read | No |
| interaction.promise_amount | Amount promised, baht | numeric(18,2) | No | None | Edit | No |
| interaction.promise_date | Date promised | date | No | None | Edit | No |
| interaction.summary | Summary of what was said | varchar(2000) | No | None | Edit | Masked by role |
| interaction.conduct_check | Passed, blocked, not applicable | varchar(15) | No | LOV-CONDUCT | Edit | No |
| interaction.source_system | EFS for collections history, or the Workbench | varchar(10) | Yes | LOV-SOURCE | Edit | No |
| decision_log_entry.decision_code | D5.1 to D9.3, X1 to X7, or an access event | varchar(8) | Yes | LOV-DECISION | Edit | No |
| decision_log_entry.rule_id | Rule that fired | varchar(20) | No | None | Edit | No |
| decision_log_entry.rule_version | Rule version | varchar(20) | No | None | Edit | No |
| decision_log_entry.model_version | Model version used | varchar(40) | No | None | Read | No |
| decision_log_entry.agent_version | Agent and prompt version used | varchar(40) | No | None | Edit | No |
| decision_log_entry.inputs_ref | Reference to the inputs snapshot, with the freshness of each input | varchar(400) | Yes | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P3-001 | A transfer without a reason | Choose a reason for the transfer. |
| MSG-P3-002 | Transfer to an owner at the caseload cap | {owner} is at the caseload cap. Choose another owner or the team queue. |
| MSG-P3-011 | Allocation summary, cases in overflow (RWB-E1-020) | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-05 Transfer case

| Item | Value |
|---|---|
| Menu | Cases |
| What it is for | Move a case to another owner or queue with a reason |
| Reached from | Case record; team queues |
| Module | P3 |
| Access | Queue and allocation, checked on every request |
| Who reaches it | Team manager |
| First in | E2 |
| Stories | RWB-E2-012 |

**States.** Form; at cap warning; saved.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| assignment.assignee_user_id | The person or service identity assigned | uuid | Yes | None | Edit | No |
| assignment.assigned_at | When assigned | timestamptz | Yes | None | Read | No |
| assignment.ended_at | When the assignment ended | timestamptz | No | None | Read | No |
| assignment.reason | Allocation, transfer, rebalance, manual, escalation | varchar(20) | Yes | LOV-ASSIGN-REASON | Edit | No |
| assignment.rule_id | The rule that made the assignment | varchar(20) | No | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P3-002 | Transfer to an owner at the caseload cap | {owner} is at the caseload cap. Choose another owner or the team queue. |
| MSG-P3-001 | A transfer without a reason | Choose a reason for the transfer. |
| MSG-P3-011 | Allocation summary, cases in overflow (RWB-E1-020) | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-06 Raise deviation

| Item | Value |
|---|---|
| Menu | Cases |
| What it is for | Raise X1 to X7 on a case with the reason and the evidence |
| Reached from | Case record |
| Module | S8 |
| Access | Case record, checked on every request |
| Who reaches it | Case owner, officers, specialists |
| First in | E2 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Form; saved.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| deviation.deviation_code | X1 to X7 | varchar(3) | Yes | LOV-DEVIATION | Edit | No |
| deviation.raised_at | When it was raised | timestamptz | Yes | None | Read | No |
| deviation.raised_by | Screening agent, rule, officer, customer contact | varchar(20) | Yes | LOV-RAISED-BY | Edit | No |
| deviation.paused_state | The routing state the case was in when paused | varchar(60) | Yes | None | Edit | No |
| deviation.handler_user_id | The named handler | uuid | No | None | Edit | No |
| deviation.contact_stop | True when customer contact is stopped | boolean | Yes | None | Edit | No |
| deviation.cleared_at | When it cleared | timestamptz | No | None | Read | No |
| deviation.outcome | Returned, re-routed, case ended | varchar(20) | No | LOV-DEV-OUTCOME | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-S8-001 | Deviation flagged | {deviation} was raised. The case is with {handler}. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-07 Team queues

| Item | Value |
|---|---|
| Menu | Queues |
| What it is for | Cases by queue with age, cap use and overflow |
| Reached from | Menu |
| Module | P3 |
| Access | Queue and allocation, checked on every request |
| Who reaches it | Team manager, capacity and workforce planner |
| First in | E2 |
| Stories | RWB-E2-011 |

**States.** Loading; list.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| queue.queue_code | Queue code | varchar(30) | Yes | None | Edit | No |
| queue.queue_name | Queue name | varchar(100) | Yes | None | Edit | No |
| queue.team_code | Team the queue belongs to | varchar(20) | Yes | LOV-TEAM | Edit | No |
| queue.role_code | Role that works the queue | varchar(20) | Yes | LOV-ROLE | Edit | No |
| queue.assignment_method | Round robin, lowest load, named owner, skill | varchar(20) | Yes | LOV-ASSIGN | Edit | No |
| queue.capacity_cap | Most open cases one person may hold in the queue | integer | No | None | Edit | No |
| assignment.assignee_user_id | The person or service identity assigned | uuid | Yes | None | Edit | No |
| assignment.assigned_at | When assigned | timestamptz | Yes | None | Read | No |
| assignment.ended_at | When the assignment ended | timestamptz | No | None | Read | No |
| assignment.reason | Allocation, transfer, rebalance, manual, escalation | varchar(20) | Yes | LOV-ASSIGN-REASON | Edit | No |
| assignment.rule_id | The rule that made the assignment | varchar(20) | No | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P3-011 | Allocation summary, cases in overflow (RWB-E1-020) | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P3-012 | Allocation summary, no row matched (RWB-E1-020) | {count} new cases matched no allocation row and are in the exception queue. |
| MSG-P3-002 | Transfer to an owner at the caseload cap | {owner} is at the caseload cap. Choose another owner or the team queue. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-08 Deviation queue

| Item | Value |
|---|---|
| Menu | Queues |
| What it is for | Open deviations by type, handler and age |
| Reached from | Menu |
| Module | S8 |
| Access | Case record, checked on every request |
| Who reaches it | Specialists, complaint officer, fraud investigator, legal counsel |
| First in | E2 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Loading; list.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| deviation.deviation_code | X1 to X7 | varchar(3) | Yes | LOV-DEVIATION | Edit | No |
| deviation.raised_at | When it was raised | timestamptz | Yes | None | Read | No |
| deviation.raised_by | Screening agent, rule, officer, customer contact | varchar(20) | Yes | LOV-RAISED-BY | Edit | No |
| deviation.paused_state | The routing state the case was in when paused | varchar(60) | Yes | None | Edit | No |
| deviation.handler_user_id | The named handler | uuid | No | None | Edit | No |
| deviation.contact_stop | True when customer contact is stopped | boolean | Yes | None | Edit | No |
| deviation.cleared_at | When it cleared | timestamptz | No | None | Read | No |
| deviation.outcome | Returned, re-routed, case ended | varchar(20) | No | LOV-DEV-OUTCOME | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-S8-001 | Deviation flagged | {deviation} was raised. The case is with {handler}. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-09 Exception queue

| Item | Value |
|---|---|
| Menu | Queues |
| What it is for | Cases and records that no rule matched, failed outbound actions and held receipts |
| Reached from | Menu |
| Module | P3 |
| Access | Queue and allocation, checked on every request |
| Who reaches it | Team manager, platform administrator |
| First in | E1 |
| Stories | RWB-E1-019, RWB-E1-020, RWB-E1-029, RWB-E1-030, RWB-E1-031, RWB-E1-044, RWB-E1-045, RWB-E1-048, RWB-E2-012 |

**States.** Loading; list.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| recovery_case.case_no | Case number RW-YYYY-NNNNNN, issued at creation and never reused | varchar(18) | Yes | None | Edit | No |
| recovery_case.product_group | Mortgage, hire purchase, SSME or unsecured | varchar(15) | Yes | LOV-PRODUCT | Read | No |
| recovery_case.status | Case status: new, assigned, in progress, waiting customer, waiting partner, waiting approval, on hold, closed | varchar(20) | Yes | LOV-CASE-STATUS | Edit | No |
| recovery_case.stage_code | The stage the case is on | varchar(20) | No | LOV-STAGE | Edit | No |
| recovery_case.route_state | The routing state from the rule set, for example FIRM_INSTRUCTED | varchar(60) | No | None | Edit | No |
| recovery_case.route_code | The approved route R1 to R8 | varchar(4) | No | LOV-ROUTE | Edit | No |
| recovery_case.owner_user_id | The case owner | uuid | No | None | Edit | No |
| recovery_case.team_code | The owning team, used by scope rules | varchar(20) | No | LOV-TEAM | Edit | No |
| recovery_case.region_code | The owning region, used by scope rules | varchar(10) | No | LOV-REGION | Edit | No |
| recovery_case.entry_date | The date the case entered recovery | date | Yes | None | Edit | No |
| recovery_case.dpd_at_entry | Days past due on the entry date | integer | Yes | None | Read | No |
| recovery_case.exposure_band | Exposure band set from the outstanding balance at entry | varchar(10) | No | LOV-EXPOSURE | Edit | No |
| recovery_case.total_outstanding_at_entry | Total outstanding across linked accounts at entry, in baht | numeric(18,2) | Yes | None | Read | No |
| recovery_case.prescription_date | The earliest date a legal claim on the case expires | date | No | None | Edit | No |
| recovery_case.stage_clock_start | When the current state started, for the service level | timestamptz | No | None | Edit | No |
| recovery_case.deviation_open | True while any deviation X1 to X7 is open | boolean | Yes | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P3-012 | Allocation summary, no row matched (RWB-E1-020) | {count} new cases matched no allocation row and are in the exception queue. |
| MSG-P3-011 | Allocation summary, cases in overflow (RWB-E1-020) | {count} new cases are waiting in the overflow queue for {team}. Every owner is at the caseload cap. |
| MSG-P3-002 | Transfer to an owner at the caseload cap | {owner} is at the caseload cap. Choose another owner or the team queue. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-10 Approval queue

| Item | Value |
|---|---|
| Menu | Approvals |
| What it is for | Decisions waiting for the person's approval level, with the facts and the recommendation |
| Reached from | Menu; my work |
| Module | P7 |
| Access | Decision log, checked on every request |
| Who reaches it | Approvers at each level, committees |
| First in | E2 |
| Stories | RWB-E2-013, RWB-E2-014 |

**States.** Loading; list.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| decision_log_entry.decision_code | D5.1 to D9.3, X1 to X7, or an access event | varchar(8) | Yes | LOV-DECISION | Edit | No |
| decision_log_entry.rule_id | Rule that fired | varchar(20) | No | None | Edit | No |
| decision_log_entry.rule_version | Rule version | varchar(20) | No | None | Edit | No |
| decision_log_entry.model_version | Model version used | varchar(40) | No | None | Read | No |
| decision_log_entry.agent_version | Agent and prompt version used | varchar(40) | No | None | Edit | No |
| decision_log_entry.inputs_ref | Reference to the inputs snapshot, with the freshness of each input | varchar(400) | Yes | None | Edit | No |
| decision_log_entry.recommendation | Option, reasons, confidence and alternatives | jsonb | No | None | Edit | No |
| decision_log_entry.approver_user_id | Who approved | uuid | No | None | Edit | No |
| decision_log_entry.approval_level | Approval level applied | varchar(4) | No | LOV-APPROVAL-LEVEL | Edit | No |
| decision_log_entry.final_call | The option decided | varchar(40) | Yes | None | Edit | No |
| decision_log_entry.override_reason | Reason when the person did not follow the recommendation | varchar(1000) | No | None | Edit | No |
| decision_log_entry.actions | Target system, result and timestamps of each action | jsonb | No | None | Edit | No |
| decision_log_entry.outcome | Cash, cure, loss and time, written when known | jsonb | No | None | Edit | No |
| decision_log_entry.decided_at | When decided | timestamptz | Yes | None | Read | No |
| decision_log_entry.prev_hash | Hash of the previous entry | char(64) | Yes | None | Edit | No |
| decision_log_entry.entry_hash | Hash of this entry | char(64) | Yes | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P7-001 | Approval above the approver's limit | This needs approval at level {level}. It has been sent to {approver}. |
| MSG-P7-005 | Override without a reason | Enter the reason you are not following the recommendation. |
| MSG-P7-002 | Approver prepared the decision | You prepared this decision, so you cannot approve it. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-11 Decision screen

| Item | Value |
|---|---|
| Menu | Approvals |
| What it is for | The recommendation with reasons, the expected return by route, the limit check and approve, return or refuse |
| Reached from | Approval queue; case record |
| Module | P7 |
| Access | Decision log, checked on every request |
| Who reaches it | Approvers at each level |
| First in | E2 |
| Stories | RWB-E2-005, RWB-E2-013, RWB-E2-014 |

**States.** Ready; above limit; stale input; decided.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| decision_log_entry.decision_code | D5.1 to D9.3, X1 to X7, or an access event | varchar(8) | Yes | LOV-DECISION | Edit | No |
| decision_log_entry.rule_id | Rule that fired | varchar(20) | No | None | Edit | No |
| decision_log_entry.rule_version | Rule version | varchar(20) | No | None | Edit | No |
| decision_log_entry.model_version | Model version used | varchar(40) | No | None | Read | No |
| decision_log_entry.agent_version | Agent and prompt version used | varchar(40) | No | None | Edit | No |
| decision_log_entry.inputs_ref | Reference to the inputs snapshot, with the freshness of each input | varchar(400) | Yes | None | Edit | No |
| decision_log_entry.recommendation | Option, reasons, confidence and alternatives | jsonb | No | None | Edit | No |
| decision_log_entry.approver_user_id | Who approved | uuid | No | None | Edit | No |
| decision_log_entry.approval_level | Approval level applied | varchar(4) | No | LOV-APPROVAL-LEVEL | Edit | No |
| decision_log_entry.final_call | The option decided | varchar(40) | Yes | None | Edit | No |
| decision_log_entry.override_reason | Reason when the person did not follow the recommendation | varchar(1000) | No | None | Edit | No |
| decision_log_entry.actions | Target system, result and timestamps of each action | jsonb | No | None | Edit | No |
| decision_log_entry.outcome | Cash, cure, loss and time, written when known | jsonb | No | None | Edit | No |
| decision_log_entry.decided_at | When decided | timestamptz | Yes | None | Read | No |
| decision_log_entry.prev_hash | Hash of the previous entry | char(64) | Yes | None | Edit | No |
| decision_log_entry.entry_hash | Hash of this entry | char(64) | Yes | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P7-002 | Approver prepared the decision | You prepared this decision, so you cannot approve it. |
| MSG-P7-006 | A decision input is past its age limit | {input} is {days} days old, past its limit. Refresh it before you decide. |
| MSG-P7-003 | Decision log write failed (principle 5) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-12 Committee pack

| Item | Value |
|---|---|
| Menu | Approvals |
| What it is for | The pack for a committee decision with each member's vote |
| Reached from | Approval queue |
| Module | P7 |
| Access | Decision log, checked on every request |
| Who reaches it | Credit approval committee, write-off committee |
| First in | E4 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Draft; circulated; decided.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| decision_log_entry.decision_code | D5.1 to D9.3, X1 to X7, or an access event | varchar(8) | Yes | LOV-DECISION | Edit | No |
| decision_log_entry.rule_id | Rule that fired | varchar(20) | No | None | Edit | No |
| decision_log_entry.rule_version | Rule version | varchar(20) | No | None | Edit | No |
| decision_log_entry.model_version | Model version used | varchar(40) | No | None | Read | No |
| decision_log_entry.agent_version | Agent and prompt version used | varchar(40) | No | None | Edit | No |
| decision_log_entry.inputs_ref | Reference to the inputs snapshot, with the freshness of each input | varchar(400) | Yes | None | Edit | No |
| decision_log_entry.recommendation | Option, reasons, confidence and alternatives | jsonb | No | None | Edit | No |
| decision_log_entry.approver_user_id | Who approved | uuid | No | None | Edit | No |
| decision_log_entry.approval_level | Approval level applied | varchar(4) | No | LOV-APPROVAL-LEVEL | Edit | No |
| decision_log_entry.final_call | The option decided | varchar(40) | Yes | None | Edit | No |
| decision_log_entry.override_reason | Reason when the person did not follow the recommendation | varchar(1000) | No | None | Edit | No |
| decision_log_entry.actions | Target system, result and timestamps of each action | jsonb | No | None | Edit | No |
| decision_log_entry.outcome | Cash, cure, loss and time, written when known | jsonb | No | None | Edit | No |
| decision_log_entry.decided_at | When decided | timestamptz | Yes | None | Read | No |
| decision_log_entry.prev_hash | Hash of the previous entry | char(64) | Yes | None | Edit | No |
| decision_log_entry.entry_hash | Hash of this entry | char(64) | Yes | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P7-002 | Approver prepared the decision | You prepared this decision, so you cannot approve it. |
| MSG-P7-003 | Decision log write failed (principle 5) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-004 | Decision approved | Approved. The case moves to {state}. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-13 Route decision

| Item | Value |
|---|---|
| Menu | Treatment |
| What it is for | The route recommendation with the expected return of each route and the reasons |
| Reached from | Case record |
| Module | S1 |
| Access | Treatment and offer, checked on every request |
| Who reaches it | Case owner |
| First in | E4 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Loading; recommendation; overridden; submitted.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| score.model_code | Model, for example CRR_RET_380 asset pricing | varchar(30) | Yes | None | Read | No |
| score.model_version | Model version | varchar(20) | Yes | None | Read | No |
| score.score_value | Score | numeric(12,4) | No | None | Read | No |
| score.estimate_value | Estimated amount, baht, for example return by route or sale price | numeric(18,2) | No | None | Read | No |
| score.route_code | Route the estimate is for | varchar(4) | No | LOV-ROUTE | Read | No |
| score.scored_at | Score date | date | Yes | None | Read | No |
| decision_log_entry.decision_code | D5.1 to D9.3, X1 to X7, or an access event | varchar(8) | Yes | LOV-DECISION | Edit | No |
| decision_log_entry.rule_id | Rule that fired | varchar(20) | No | None | Edit | No |
| decision_log_entry.rule_version | Rule version | varchar(20) | No | None | Edit | No |
| decision_log_entry.model_version | Model version used | varchar(40) | No | None | Read | No |
| decision_log_entry.agent_version | Agent and prompt version used | varchar(40) | No | None | Edit | No |
| decision_log_entry.inputs_ref | Reference to the inputs snapshot, with the freshness of each input | varchar(400) | Yes | None | Edit | No |
| decision_log_entry.recommendation | Option, reasons, confidence and alternatives | jsonb | No | None | Edit | No |
| decision_log_entry.approver_user_id | Who approved | uuid | No | None | Edit | No |
| decision_log_entry.approval_level | Approval level applied | varchar(4) | No | LOV-APPROVAL-LEVEL | Edit | No |
| decision_log_entry.final_call | The option decided | varchar(40) | Yes | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-14 Treatment record

| Item | Value |
|---|---|
| Menu | Treatment |
| What it is for | The restructure, settlement or deed in lieu offer, its terms, its status and the booking confirmation |
| Reached from | Case record |
| Module | S2 |
| Access | Treatment and offer, checked on every request |
| Who reaches it | Case owner, restructuring officer (FCR) |
| First in | E2 record; E3 full |
| Stories | Built in its first release; story written one epic ahead |

**States.** Draft; submitted; approved; booked; broken.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| treatment.treatment_type | Restructure, settlement, deed in lieu, buy-back, guarantee claim, repossession, auction, debt sale, write-off, RAMC transfer, rental | varchar(20) | Yes | LOV-TREATMENT | Edit | No |
| treatment.proposed_by | Agent, rule, person | varchar(10) | Yes | LOV-PROPOSER | Edit | No |
| treatment.proposed_at | When proposed | timestamptz | Yes | None | Read | No |
| treatment.offer_amount | Amount offered or agreed, baht | numeric(18,2) | No | None | Edit | No |
| treatment.haircut_amount | Amount forgiven, baht | numeric(18,2) | No | None | Edit | No |
| treatment.installments | Number of installments in a plan | integer | No | None | Read | No |
| treatment.valid_until | Offer validity | date | No | None | Edit | No |
| treatment.approval_level | Approval level that approved it | varchar(4) | No | LOV-APPROVAL-LEVEL | Edit | No |
| treatment.booked_at | When booked in the core | timestamptz | No | None | Read | No |
| treatment.outcome | Kept, broken, completed, canceled, declined | varchar(12) | No | LOV-TRT-OUTCOME | Edit | No |
| treatment.outcome_at | When the outcome was recorded | timestamptz | No | None | Read | No |

| Message | When | Text |
|---|---|---|
| MSG-S2-001 | Settlement below the floor without approval (R-SET-05) | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-003 | Offer validity ending | The offer to the customer ends on {date}. |
| MSG-S2-002 | Payoff figure stale (R-SET-03) | The payoff is from {date}. A new figure has been requested. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-15 Settlement offer

| Item | Value |
|---|---|
| Menu | Treatment |
| What it is for | Payoff, offer range, floor and the gap to the floor |
| Reached from | Treatment record |
| Module | S2 |
| Access | Treatment and offer, checked on every request |
| Who reaches it | Case owner, restructuring officer (FCR) |
| First in | E3 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Draft; below floor; approved; sent; accepted.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| treatment.treatment_type | Restructure, settlement, deed in lieu, buy-back, guarantee claim, repossession, auction, debt sale, write-off, RAMC transfer, rental | varchar(20) | Yes | LOV-TREATMENT | Edit | No |
| treatment.proposed_by | Agent, rule, person | varchar(10) | Yes | LOV-PROPOSER | Edit | No |
| treatment.proposed_at | When proposed | timestamptz | Yes | None | Read | No |
| treatment.offer_amount | Amount offered or agreed, baht | numeric(18,2) | No | None | Edit | No |
| treatment.haircut_amount | Amount forgiven, baht | numeric(18,2) | No | None | Edit | No |
| treatment.installments | Number of installments in a plan | integer | No | None | Read | No |
| treatment.valid_until | Offer validity | date | No | None | Edit | No |
| treatment.approval_level | Approval level that approved it | varchar(4) | No | LOV-APPROVAL-LEVEL | Edit | No |
| treatment.booked_at | When booked in the core | timestamptz | No | None | Read | No |
| treatment.outcome | Kept, broken, completed, canceled, declined | varchar(12) | No | LOV-TRT-OUTCOME | Edit | No |
| treatment.outcome_at | When the outcome was recorded | timestamptz | No | None | Read | No |

| Message | When | Text |
|---|---|---|
| MSG-S2-001 | Settlement below the floor without approval (R-SET-05) | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-002 | Payoff figure stale (R-SET-03) | The payoff is from {date}. A new figure has been requested. |
| MSG-S2-003 | Offer validity ending | The offer to the customer ends on {date}. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-16 Deed in lieu

| Item | Value |
|---|---|
| Menu | Treatment |
| What it is for | Readiness checks, appraisal order, transfer and asset take-on |
| Reached from | Treatment record |
| Module | S2 |
| Access | Treatment and offer, checked on every request |
| Who reaches it | Case owner, sale officer |
| First in | E3 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Checks; appraisal; approved; transferred.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| treatment.treatment_type | Restructure, settlement, deed in lieu, buy-back, guarantee claim, repossession, auction, debt sale, write-off, RAMC transfer, rental | varchar(20) | Yes | LOV-TREATMENT | Edit | No |
| treatment.proposed_by | Agent, rule, person | varchar(10) | Yes | LOV-PROPOSER | Edit | No |
| treatment.proposed_at | When proposed | timestamptz | Yes | None | Read | No |
| treatment.offer_amount | Amount offered or agreed, baht | numeric(18,2) | No | None | Edit | No |
| treatment.haircut_amount | Amount forgiven, baht | numeric(18,2) | No | None | Edit | No |
| treatment.installments | Number of installments in a plan | integer | No | None | Read | No |
| treatment.valid_until | Offer validity | date | No | None | Edit | No |
| treatment.approval_level | Approval level that approved it | varchar(4) | No | LOV-APPROVAL-LEVEL | Edit | No |
| treatment.booked_at | When booked in the core | timestamptz | No | None | Read | No |
| treatment.outcome | Kept, broken, completed, canceled, declined | varchar(12) | No | LOV-TRT-OUTCOME | Edit | No |
| treatment.outcome_at | When the outcome was recorded | timestamptz | No | None | Read | No |
| valuation.appraisal_no | Appraisal number | varchar(20) | Yes | None | Read | No |
| valuation.appraisal_type | Market, official, forced sale, desktop, agent estimate | varchar(15) | Yes | LOV-APPRAISAL | Read | No |
| valuation.appraised_value | Appraised value, baht | numeric(18,2) | Yes | None | Read | No |
| valuation.forced_sale_value | Forced sale value, baht | numeric(18,2) | No | None | Read | No |
| valuation.appraisal_date | Appraisal date | date | Yes | None | Read | No |

| Message | When | Text |
|---|---|---|
| MSG-S2-001 | Settlement below the floor without approval (R-SET-05) | The offer is below the floor of {floor}. It has been sent for approval. |
| MSG-S2-002 | Payoff figure stale (R-SET-03) | The payoff is from {date}. A new figure has been requested. |
| MSG-S2-003 | Offer validity ending | The offer to the customer ends on {date}. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-17 Guarantee claim

| Item | Value |
|---|---|
| Menu | Treatment |
| What it is for | The guarantee, the claim deadline, the checklist and the claim result |
| Reached from | Case record |
| Module | S3 |
| Access | Treatment and offer, checked on every request |
| Who reaches it | Guarantee officer |
| First in | E4 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Not due; due; submitted; paid; refused.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| guarantee_claim.claim_type | TCG, credit life insurance, mortgage insurance, collateral insurance | varchar(25) | Yes | LOV-CLAIM-TYPE | Edit | No |
| guarantee_claim.claim_deadline | Last date the claim can be filed | date | Yes | None | Edit | No |
| guarantee_claim.claimed_amount | Amount claimed, baht | numeric(18,2) | Yes | None | Edit | No |
| guarantee_claim.filed_at | Date filed | date | No | None | Read | No |
| guarantee_claim.paid_amount | Amount paid, baht | numeric(18,2) | No | None | Edit | No |
| guarantee_claim.status | Preparing, filed, defect, paid, rejected | varchar(12) | Yes | LOV-CLAIM-STATUS | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-18 Notice approval

| Item | Value |
|---|---|
| Menu | Litigation |
| What it is for | Generated demand and recall notices for approval before dispatch |
| Reached from | Case record; my work |
| Module | S4 |
| Access | Litigation, checked on every request |
| Who reaches it | Litigation officer, legal counsel |
| First in | E2 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Generated; approved; sent; delivered; unserved.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| notice.notice_type | Demand, recall, statutory sale notice, guarantor notice | varchar(25) | Yes | LOV-NOTICE | Edit | No |
| notice.sent_date | Date sent | date | No | None | Read | No |
| notice.barcode | Registered mail barcode | varchar(40) | No | None | Read | No |
| notice.callback_date | Date the proof of delivery came back | date | No | None | Read | No |
| notice.delivery_status | Delivered, refused, undeliverable, pending | varchar(15) | No | LOV-DELIVERY | Read | No |
| notice.sent_type | Before NPL or NPL | varchar(10) | No | LOV-SENT-TYPE | Read | No |

| Message | When | Text |
|---|---|---|
| MSG-S4-001 | Pack incomplete at filing | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Prescription date near | The claim on this case expires on {date}. File before then. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-19 Litigation workspace

| Item | Value |
|---|---|
| Menu | Litigation |
| What it is for | Pack, instruction, court dates, hearings and judgment for a case |
| Reached from | Case record |
| Module | S4 |
| Access | Litigation, checked on every request |
| Who reaches it | Litigation officer, Head of Litigation |
| First in | E5 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Pack; instructed; filed; hearing; judgment.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| legal_action.action_type | Notice, civil case, appeal, enforcement, bankruptcy petition, LED auction | varchar(20) | Yes | LOV-LEGAL-TYPE | Edit | No |
| legal_action.lawsuit_no | Lawsuit reference in LIT | varchar(30) | No | None | Read | No |
| legal_action.black_case_no | Court black case number | varchar(30) | No | None | Read | No |
| legal_action.red_case_no | Court red case number after judgment | varchar(30) | No | None | Read | No |
| legal_action.court_name | Court | varchar(120) | No | None | Read | No |
| legal_action.claim_amount | Amount sued for, baht | numeric(18,2) | No | None | Read | No |
| legal_action.filed_date | Date filed | date | No | None | Read | No |
| legal_action.judgment_date | Date of judgment | date | No | None | Read | No |
| legal_action.judgment_amount | Amount awarded, baht | numeric(18,2) | No | None | Read | No |
| legal_action.lit_status | Latest status text in LIT | varchar(200) | No | None | Read | No |
| legal_action.status | Open, filed, judgment, enforcing, closed, withdrawn | varchar(15) | Yes | LOV-LEGAL-STATUS | Edit | No |
| hearing.hearing_date | Hearing date | timestamptz | Yes | None | Read | No |
| hearing.hearing_type | First hearing, witness, judgment reading, mediation | varchar(20) | No | LOV-HEARING | Read | No |
| hearing.outcome | Held, adjourned, settled, judgment | varchar(20) | No | LOV-HEARING-OUTCOME | Edit | No |
| hearing.next_date | Next date set | timestamptz | No | None | Read | No |

| Message | When | Text |
|---|---|---|
| MSG-S4-001 | Pack incomplete at filing | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Prescription date near | The claim on this case expires on {date}. File before then. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-20 Enforcement workspace

| Item | Value |
|---|---|
| Menu | Litigation |
| What it is for | Enforcement steps with the Legal Execution Department and the result |
| Reached from | Case record |
| Module | S4 |
| Access | Litigation, checked on every request |
| Who reaches it | Enforcement owner |
| First in | E5 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Requested; seized; auctioned; closed.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| legal_action.action_type | Notice, civil case, appeal, enforcement, bankruptcy petition, LED auction | varchar(20) | Yes | LOV-LEGAL-TYPE | Edit | No |
| legal_action.lawsuit_no | Lawsuit reference in LIT | varchar(30) | No | None | Read | No |
| legal_action.black_case_no | Court black case number | varchar(30) | No | None | Read | No |
| legal_action.red_case_no | Court red case number after judgment | varchar(30) | No | None | Read | No |
| legal_action.court_name | Court | varchar(120) | No | None | Read | No |
| legal_action.claim_amount | Amount sued for, baht | numeric(18,2) | No | None | Read | No |
| legal_action.filed_date | Date filed | date | No | None | Read | No |
| legal_action.judgment_date | Date of judgment | date | No | None | Read | No |
| legal_action.judgment_amount | Amount awarded, baht | numeric(18,2) | No | None | Read | No |
| legal_action.lit_status | Latest status text in LIT | varchar(200) | No | None | Read | No |
| legal_action.status | Open, filed, judgment, enforcing, closed, withdrawn | varchar(15) | Yes | LOV-LEGAL-STATUS | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-S4-001 | Pack incomplete at filing | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Prescription date near | The claim on this case expires on {date}. File before then. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-21 Asset list

| Item | Value |
|---|---|
| Menu | Assets |
| What it is for | Assets held, with age, holding cost, value and sale status |
| Reached from | Menu |
| Module | S5 |
| Access | Asset and disposal, checked on every request |
| Who reaches it | Sale officer, NPA and asset manager, Head of NPA |
| First in | E3 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Loading; list.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| asset.asset_ref | Asset reference | varchar(20) | Yes | None | Read | No |
| asset.asset_code | Asset code | varchar(20) | No | None | Read | No |
| asset.asset_type | Detached house, townhouse, condominium, land, vehicle | varchar(20) | Yes | LOV-ASSET-TYPE | Read | No |
| asset.transfer_in_type | Auction purchase, deed in lieu, repossession | varchar(20) | Yes | LOV-TRANSFER-IN | Read | No |
| asset.from_segment | Segment the asset came from | varchar(20) | No | LOV-SEGMENT | Read | No |
| asset.transfer_in_date | Date ownership passed to the bank | date | Yes | None | Read | No |
| asset.book_value | Book value, baht | numeric(18,2) | Yes | None | Read | No |
| asset.auction_purchase_price | Price paid at auction, baht | numeric(18,2) | No | None | Read | No |
| asset.repossessed_date | Date the vehicle was repossessed | date | No | None | Read | No |
| asset.stock_date | Date the vehicle entered stock | date | No | None | Read | No |
| asset.holding_status | Held, listed, under offer, sold, transferred, rented | varchar(15) | Yes | LOV-HOLDING | Edit | No |
| asset.holding_cost_to_date | Holding cost to date, baht | numeric(18,2) | No | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-S5-001 | Floor price below the approver's limit | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Appraisal older than one year | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-22 Asset record

| Item | Value |
|---|---|
| Menu | Assets |
| What it is for | One asset: title, condition, photographs, valuations, costs, listing and sale history |
| Reached from | Asset list; case record |
| Module | S5 |
| Access | Asset and disposal, checked on every request |
| Who reaches it | Sale officer, NPA and asset manager |
| First in | E3 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Take-on; held; listed; sold.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| asset.asset_ref | Asset reference | varchar(20) | Yes | None | Read | No |
| asset.asset_code | Asset code | varchar(20) | No | None | Read | No |
| asset.asset_type | Detached house, townhouse, condominium, land, vehicle | varchar(20) | Yes | LOV-ASSET-TYPE | Read | No |
| asset.transfer_in_type | Auction purchase, deed in lieu, repossession | varchar(20) | Yes | LOV-TRANSFER-IN | Read | No |
| asset.from_segment | Segment the asset came from | varchar(20) | No | LOV-SEGMENT | Read | No |
| asset.transfer_in_date | Date ownership passed to the bank | date | Yes | None | Read | No |
| asset.book_value | Book value, baht | numeric(18,2) | Yes | None | Read | No |
| asset.auction_purchase_price | Price paid at auction, baht | numeric(18,2) | No | None | Read | No |
| asset.repossessed_date | Date the vehicle was repossessed | date | No | None | Read | No |
| asset.stock_date | Date the vehicle entered stock | date | No | None | Read | No |
| asset.holding_status | Held, listed, under offer, sold, transferred, rented | varchar(15) | Yes | LOV-HOLDING | Edit | No |
| asset.holding_cost_to_date | Holding cost to date, baht | numeric(18,2) | No | None | Edit | No |
| valuation.appraisal_no | Appraisal number | varchar(20) | Yes | None | Read | No |
| valuation.appraisal_type | Market, official, forced sale, desktop, agent estimate | varchar(15) | Yes | LOV-APPRAISAL | Read | No |
| valuation.appraised_value | Appraised value, baht | numeric(18,2) | Yes | None | Read | No |
| valuation.forced_sale_value | Forced sale value, baht | numeric(18,2) | No | None | Read | No |

| Message | When | Text |
|---|---|---|
| MSG-S5-001 | Floor price below the approver's limit | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Appraisal older than one year | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-23 Listing and price

| Item | Value |
|---|---|
| Menu | Assets |
| What it is for | List price, floor and the price ladder for an asset |
| Reached from | Asset record |
| Module | S5 |
| Access | Asset and disposal, checked on every request |
| Who reaches it | Sale officer |
| First in | E3 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Draft; below limit; approved; published.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| listing.sale_channel | Dutch auction, broker, direct, LED auction, RAMC | varchar(15) | Yes | LOV-SALE-CHANNEL | Edit | No |
| listing.start_price | Start price, baht | numeric(18,2) | Yes | None | Edit | No |
| listing.floor_price | Floor price approved, baht | numeric(18,2) | Yes | None | Edit | No |
| listing.round_no | Current price round | integer | Yes | None | Edit | No |
| listing.listed_at | When listed | timestamptz | No | None | Read | No |
| listing.status | Draft, live, under offer, sold, withdrawn | varchar(12) | Yes | LOV-LISTING | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-S5-001 | Floor price below the approver's limit | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Appraisal older than one year | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-24 Auction rounds

| Item | Value |
|---|---|
| Menu | Assets |
| What it is for | Auction rounds, bids and results for an asset |
| Reached from | Asset record |
| Module | S5 |
| Access | Asset and disposal, checked on every request |
| Who reaches it | Sale officer, auction vendor |
| First in | E4 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Scheduled; open; result; settled.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| asset_sale.contract_date | Sale contract date | date | Yes | None | Read | No |
| asset_sale.sale_date | Sale date | date | Yes | None | Read | No |
| asset_sale.sale_price | Sale price, baht | numeric(18,2) | Yes | None | Read | No |
| asset_sale.transfer_fee | Transfer fee, baht | numeric(18,2) | No | None | Read | No |
| asset_sale.specific_business_tax | Specific business tax, baht | numeric(18,2) | No | None | Read | No |
| asset_sale.corporate_income_tax | Corporate income tax, baht | numeric(18,2) | No | None | Read | No |
| asset_sale.gain_loss | Sale price less book value and costs | numeric(18,2) | No | None | Edit | No |
| asset_sale.incentive_amount | Incentive paid on the sale, baht | numeric(18,2) | No | None | Read | No |

| Message | When | Text |
|---|---|---|
| MSG-S5-001 | Floor price below the approver's limit | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Appraisal older than one year | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-25 Lot builder

| Item | Value |
|---|---|
| Menu | Debt sale |
| What it is for | Select accounts, build lots, set the reserve and send for approval |
| Reached from | Menu |
| Module | S6 |
| Access | Debt sale, checked on every request |
| Who reaches it | Debt sale officer, Head of Asset Liquidity |
| First in | E5 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Draft; priced; approved.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| debt_sale_lot.lot_no | Lot number, for example 1/2024 | varchar(15) | Yes | None | Edit | No |
| debt_sale_lot.cut_off_date | Balance cut-off date | date | Yes | None | Edit | No |
| debt_sale_lot.segment | Segment of the lot | varchar(20) | Yes | LOV-SEGMENT | Edit | No |
| debt_sale_lot.reserve_price | Reserve price, baht | numeric(18,2) | No | None | Edit | No |
| debt_sale_lot.buyer_class | AMC or non-AMC | varchar(10) | No | LOV-BUYER-CLASS | Edit | No |
| debt_sale_lot.signing_date | Date the sale was signed | date | No | None | Edit | No |
| debt_sale_lot.approval_authority | Authority that approved the sale | varchar(60) | No | None | Edit | No |
| debt_sale_lot.payment_terms | Deposit and payment terms | varchar(400) | No | None | Edit | No |
| debt_sale_lot.status | Building, offered, awarded, transferred, closed | varchar(12) | Yes | LOV-LOT-STATUS | Edit | No |
| debt_sale_account.borrower_code | Borrower code | varchar(20) | No | None | Edit | No |
| debt_sale_account.outstanding | Outstanding at cut-off, baht | numeric(18,2) | Yes | None | Read | No |
| debt_sale_account.selling_price | Price allocated to the account, baht | numeric(18,2) | No | None | Edit | No |
| debt_sale_account.put_back_status | None, claimed, accepted, rejected | varchar(12) | No | LOV-PUTBACK | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-S6-001 | Account with an open deviation selected for a lot (R-DS-02) | {account} has an open deviation and cannot be sold. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-26 Award

| Item | Value |
|---|---|
| Menu | Debt sale |
| What it is for | Bids against the reserve and the award decision |
| Reached from | Lot builder |
| Module | S6 |
| Access | Debt sale, checked on every request |
| Who reaches it | Debt sale officer, Head of Asset Liquidity |
| First in | E6 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Open; closed; awarded; transferred.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| debt_sale_lot.lot_no | Lot number, for example 1/2024 | varchar(15) | Yes | None | Edit | No |
| debt_sale_lot.cut_off_date | Balance cut-off date | date | Yes | None | Edit | No |
| debt_sale_lot.segment | Segment of the lot | varchar(20) | Yes | LOV-SEGMENT | Edit | No |
| debt_sale_lot.reserve_price | Reserve price, baht | numeric(18,2) | No | None | Edit | No |
| debt_sale_lot.buyer_class | AMC or non-AMC | varchar(10) | No | LOV-BUYER-CLASS | Edit | No |
| debt_sale_lot.signing_date | Date the sale was signed | date | No | None | Edit | No |
| debt_sale_lot.approval_authority | Authority that approved the sale | varchar(60) | No | None | Edit | No |
| debt_sale_lot.payment_terms | Deposit and payment terms | varchar(400) | No | None | Edit | No |
| debt_sale_lot.status | Building, offered, awarded, transferred, closed | varchar(12) | Yes | LOV-LOT-STATUS | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-S6-001 | Account with an open deviation selected for a lot (R-DS-02) | {account} has an open deviation and cannot be sold. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-27 Write-off proposal

| Item | Value |
|---|---|
| Menu | Write-off |
| What it is for | The monthly population, the pack per case and removals with reasons |
| Reached from | Menu |
| Module | S7 |
| Access | Write-off and posting, checked on every request |
| Who reaches it | Write-off team member |
| First in | E6 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Scan; proposed; in committee; approved.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| write_off.amount | Amount written off, baht | numeric(18,2) | Yes | None | Read | No |
| write_off.tax_criteria_met | True when the tax criteria are met | boolean | Yes | None | Edit | No |
| write_off.committee_date | Committee approval date | date | No | None | Edit | No |
| write_off.posted_date | Posting date | date | No | None | Read | No |
| write_off.responsibility_center | Responsibility center | varchar(10) | No | None | Read | No |
| write_off.cost_center | Operating cost center | varchar(10) | No | None | Read | No |
| write_off.gl_product | GL product code | varchar(10) | No | None | Read | No |
| write_off.recovered_after | Recovered after charge-off to date, baht | numeric(18,2) | Yes | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-S7-001 | Write-off without the tax criteria version (R-WO-03) | The scan is on hold until Finance publishes the tax criteria. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-28 Proceeds matching

| Item | Value |
|---|---|
| Menu | Money |
| What it is for | Receipts matched to cases and the unmatched list |
| Reached from | Menu |
| Module | P8 |
| Access | Write-off and posting, checked on every request |
| Who reaches it | Credit Administration officer |
| First in | E2 skeleton; E4 full |
| Stories | RWB-E2-008, RWB-E2-027 |

**States.** Loading; matched; unmatched.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| proceeds.source | Customer, LED, auction, buyer, agency, insurer, guarantor | varchar(12) | Yes | LOV-PROCEEDS-SRC | Edit | No |
| proceeds.amount | Amount, baht | numeric(18,2) | Yes | None | Read | No |
| proceeds.received_date | Date received | date | Yes | None | Read | No |
| proceeds.matched_to | Installment, settlement, fee, sale proceeds, unmatched | varchar(15) | Yes | LOV-MATCH | Edit | No |
| proceeds.posting_ref | Posting reference in the core or GL | varchar(40) | No | None | Read | No |

| Message | When | Text |
|---|---|---|
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-29 Posting

| Item | Value |
|---|---|
| Menu | Money |
| What it is for | Approved bookings and postings with the confirmation from the next load |
| Reached from | Menu |
| Module | P8 |
| Access | Write-off and posting, checked on every request |
| Who reaches it | Credit Administration officer |
| First in | E4 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Pending; confirmed; missing.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| proceeds.source | Customer, LED, auction, buyer, agency, insurer, guarantor | varchar(12) | Yes | LOV-PROCEEDS-SRC | Edit | No |
| proceeds.amount | Amount, baht | numeric(18,2) | Yes | None | Read | No |
| proceeds.received_date | Date received | date | Yes | None | Read | No |
| proceeds.matched_to | Installment, settlement, fee, sale proceeds, unmatched | varchar(15) | Yes | LOV-MATCH | Edit | No |
| proceeds.posting_ref | Posting reference in the core or GL | varchar(40) | No | None | Read | No |
| treatment.treatment_type | Restructure, settlement, deed in lieu, buy-back, guarantee claim, repossession, auction, debt sale, write-off, RAMC transfer, rental | varchar(20) | Yes | LOV-TREATMENT | Edit | No |
| treatment.proposed_by | Agent, rule, person | varchar(10) | Yes | LOV-PROPOSER | Edit | No |
| treatment.proposed_at | When proposed | timestamptz | Yes | None | Read | No |
| treatment.offer_amount | Amount offered or agreed, baht | numeric(18,2) | No | None | Edit | No |
| treatment.haircut_amount | Amount forgiven, baht | numeric(18,2) | No | None | Edit | No |
| treatment.installments | Number of installments in a plan | integer | No | None | Read | No |
| treatment.valid_until | Offer validity | date | No | None | Edit | No |
| treatment.approval_level | Approval level that approved it | varchar(4) | No | LOV-APPROVAL-LEVEL | Edit | No |
| treatment.booked_at | When booked in the core | timestamptz | No | None | Read | No |
| treatment.outcome | Kept, broken, completed, canceled, declined | varchar(12) | No | LOV-TRT-OUTCOME | Edit | No |
| treatment.outcome_at | When the outcome was recorded | timestamptz | No | None | Read | No |

| Message | When | Text |
|---|---|---|
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-30 Case documents

| Item | Value |
|---|---|
| Menu | Documents |
| What it is for | Documents on a case by type, with the extracted fields and versions |
| Reached from | Case record |
| Module | P5 |
| Access | Documents, checked on every request |
| Who reaches it | Every bank role in scope |
| First in | E1 |
| Stories | RWB-E1-024, RWB-E1-025, RWB-E1-026, RWB-E1-032, RWB-E1-033, RWB-E1-040, RWB-E1-049, RWB-E1-053, RWB-E1-054, RWB-E2-017, RWB-E2-024, RWB-E2-025, RWB-E2-026 |

**States.** Loading; list; upload.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| document.document_type | Type from the document checklist | varchar(30) | Yes | LOV-DOC-TYPE | Edit | No |
| document.source | Scan, upload, generated, partner, email | varchar(12) | Yes | LOV-DOC-SOURCE | Edit | No |
| document.storage_ref | Reference to the stored file | varchar(400) | Yes | None | Edit | No |
| document.classification_confidence | OCR classification confidence | numeric(5,4) | No | None | Edit | No |
| document.review_status | Not needed, pending, confirmed, corrected | varchar(12) | Yes | LOV-REVIEW | Edit | No |
| document.retention_class | Retention class | varchar(10) | Yes | LOV-RETENTION | Edit | No |
| document.write_once | True for legal documents held write-once | boolean | Yes | None | Edit | No |
| document.doc_version | Document version | integer | Yes | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P5-002 | Change to a write-once legal document | Legal documents cannot be changed. Add a new version instead. |
| MSG-P5-003 | Low-confidence extraction sent for review | Some fields need checking. The document is in the review queue. |
| MSG-P5-001 | Upload of a file type not allowed | This file type cannot be stored. Use PDF, JPG or PNG. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-31 Document review queue

| Item | Value |
|---|---|
| Menu | Documents |
| What it is for | Low-confidence extractions to check and correct |
| Reached from | Menu |
| Module | P5 |
| Access | Documents, checked on every request |
| Who reaches it | Document services, case owner |
| First in | E1 |
| Stories | RWB-E1-024, RWB-E1-025, RWB-E1-026, RWB-E1-032, RWB-E1-033, RWB-E1-040, RWB-E1-041, RWB-E1-049, RWB-E1-050, RWB-E1-053, RWB-E1-054, RWB-E1-057, RWB-E2-017, RWB-E2-024, RWB-E2-025, RWB-E2-026, RWB-AD-021 |

**States.** Loading; list; reviewed.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| document_field.field_name | Field name from the document type | varchar(60) | Yes | None | Edit | No |
| document_field.field_value | Value read, masked where personal | varchar(1000) | No | None | Edit | Masked by role |
| document_field.confidence | Extraction confidence | numeric(5,4) | No | None | Edit | No |
| document_field.confirmed_by | Who confirmed a low confidence value | uuid | No | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P5-003 | Low-confidence extraction sent for review | Some fields need checking. The document is in the review queue. |
| MSG-P5-004 | An original document is overdue back | {document} is due back from {holder} since {date}. |
| MSG-P5-001 | Upload of a file type not allowed | This file type cannot be stored. Use PDF, JPG or PNG. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-32 Document custody

| Item | Value |
|---|---|
| Menu | Documents |
| What it is for | Originals out, their holder and their due-back date |
| Reached from | Menu; case documents |
| Module | P5 |
| Access | Documents, checked on every request |
| Who reaches it | Document services, legal counsel |
| First in | E2 |
| Stories | RWB-AD-021 |

**States.** Out; overdue; returned.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| document_custody.moved_at | When it moved | timestamptz | Yes | None | Read | No |
| document_custody.from_location | Vault, branch, post, lawyer, court, land office | varchar(20) | Yes | LOV-CUSTODY | Edit | No |
| document_custody.to_location | Where it went | varchar(20) | Yes | LOV-CUSTODY | Edit | No |
| document_custody.held_by | Person or firm holding it | varchar(120) | Yes | None | Edit | No |
| document_custody.due_back | When it is due back | date | No | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P5-004 | An original document is overdue back | {document} is due back from {holder} since {date}. |
| MSG-P5-003 | Low-confidence extraction sent for review | Some fields need checking. The document is in the review queue. |
| MSG-P5-001 | Upload of a file type not allowed | This file type cannot be stored. Use PDF, JPG or PNG. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-33 Template approval

| Item | Value |
|---|---|
| Menu | Documents |
| What it is for | Letter and notice templates and their approval |
| Reached from | Menu |
| Module | P6 |
| Access | Documents, checked on every request |
| Who reaches it | Legal counsel |
| First in | E2 |
| Stories | RWB-E2-021, RWB-E2-022, RWB-AD-017 |

**States.** Draft; approved; withdrawn.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| template.template_code | Template code | varchar(30) | Yes | None | Edit | No |
| template.template_version | Version | integer | Yes | None | Edit | No |
| template.language | Thai or English | varchar(2) | Yes | LOV-LANG | Edit | No |
| template.product_group | Product group it applies to | varchar(15) | No | LOV-PRODUCT | Edit | No |
| template.body_ref | Stored template body | varchar(400) | Yes | None | Edit | No |
| template.approved_by_legal | True once Legal approves the wording | boolean | Yes | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P6-003 | Template withdrawn (R-LIT-04) | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P6-004 | Notice dispatched | {notice} was sent for registered mail on {date}. |
| MSG-P6-001 | Contact attempted while a contact stop is in force | Contact with this customer is stopped for {reason}. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-34 Partner list

| Item | Value |
|---|---|
| Menu | Partners |
| What it is for | Partners, contracts, panel status and scorecards |
| Reached from | Menu |
| Module | S9 |
| Access | Partner portal, checked on every request |
| Who reaches it | Partner and agency manager |
| First in | E2 identities; E6 full |
| Stories | RWB-AD-022 |

**States.** Loading; list.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| partner.partner_code | Partner code | varchar(20) | Yes | None | Edit | No |
| partner.partner_name | Registered name | varchar(160) | Yes | None | Edit | No |
| partner.partner_type | Agency, law firm, valuer, auction vendor, broker, debt buyer, AMC, RAMC | varchar(15) | Yes | LOV-PARTNER-TYPE | Edit | No |
| partner.panel_status | Active, on notice, suspended, exited | varchar(12) | Yes | LOV-PANEL | Edit | No |
| partner.contract_end | Contract end date | date | No | None | Edit | No |
| partner.score | Latest scorecard result | numeric(5,2) | No | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-35 Placement and allocation

| Item | Value |
|---|---|
| Menu | Partners |
| What it is for | Work placed with partners by rule, with recalls and re-selection |
| Reached from | Partner list |
| Module | S9 |
| Access | Partner portal, checked on every request |
| Who reaches it | Partner and agency manager |
| First in | E6 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Loading; list.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| partner_instruction.instruction_type | Collect, file suit, enforce, appraise, repossess, list, sell | varchar(20) | Yes | LOV-INSTRUCTION | Edit | No |
| partner_instruction.instructed_at | When instructed | timestamptz | Yes | None | Read | No |
| partner_instruction.due_at | When the result is due | timestamptz | No | None | Read | No |
| partner_instruction.status | Sent, accepted, declined, in progress, done, recalled | varchar(12) | Yes | LOV-INSTR-STATUS | Edit | No |
| partner_instruction.result_code | Result reported by the partner | varchar(40) | No | None | Edit | No |
| partner_instruction.fee_amount | Fee payable, baht | numeric(18,2) | No | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-36 Partner scorecard

| Item | Value |
|---|---|
| Menu | Partners |
| What it is for | Monthly score per partner against its measures |
| Reached from | Partner list |
| Module | S9 |
| Access | Partner portal, checked on every request |
| Who reaches it | Partner and agency manager, Head of Litigation |
| First in | E7 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Loading; scored.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| partner.partner_code | Partner code | varchar(20) | Yes | None | Edit | No |
| partner.partner_name | Registered name | varchar(160) | Yes | None | Edit | No |
| partner.partner_type | Agency, law firm, valuer, auction vendor, broker, debt buyer, AMC, RAMC | varchar(15) | Yes | LOV-PARTNER-TYPE | Edit | No |
| partner.panel_status | Active, on notice, suspended, exited | varchar(12) | Yes | LOV-PANEL | Edit | No |
| partner.contract_end | Contract end date | date | No | None | Edit | No |
| partner.score | Latest scorecard result | numeric(5,2) | No | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-37 Steering dashboard

| Item | Value |
|---|---|
| Menu | Reports |
| What it is for | Inflow, stock, cures, recovery, turnaround and cost, by product and route |
| Reached from | Menu |
| Module | P9 |
| Access | Reporting, checked on every request |
| Who reaches it | Product heads, sponsors, team managers |
| First in | E2 |
| Stories | RWB-E2-009 |

**States.** Loading; filtered.

Measures and status from the reporting and monitoring data; no record fields are edited on this screen.

| Message | When | Text |
|---|---|---|
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-38 Decision log query

| Item | Value |
|---|---|
| Menu | Reports |
| What it is for | Search the decision log by case, rule, approver and date, with export |
| Reached from | Menu |
| Module | P7 |
| Access | Decision log, checked on every request |
| Who reaches it | Internal audit, Risk, center of excellence |
| First in | E2 |
| Stories | RWB-E2-005 |

**States.** Loading; results; export.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| decision_log_entry.decision_code | D5.1 to D9.3, X1 to X7, or an access event | varchar(8) | Yes | LOV-DECISION | Edit | No |
| decision_log_entry.rule_id | Rule that fired | varchar(20) | No | None | Edit | No |
| decision_log_entry.rule_version | Rule version | varchar(20) | No | None | Edit | No |
| decision_log_entry.model_version | Model version used | varchar(40) | No | None | Read | No |
| decision_log_entry.agent_version | Agent and prompt version used | varchar(40) | No | None | Edit | No |
| decision_log_entry.inputs_ref | Reference to the inputs snapshot, with the freshness of each input | varchar(400) | Yes | None | Edit | No |
| decision_log_entry.recommendation | Option, reasons, confidence and alternatives | jsonb | No | None | Edit | No |
| decision_log_entry.approver_user_id | Who approved | uuid | No | None | Edit | No |
| decision_log_entry.approval_level | Approval level applied | varchar(4) | No | LOV-APPROVAL-LEVEL | Edit | No |
| decision_log_entry.final_call | The option decided | varchar(40) | Yes | None | Edit | No |
| decision_log_entry.override_reason | Reason when the person did not follow the recommendation | varchar(1000) | No | None | Edit | No |
| decision_log_entry.actions | Target system, result and timestamps of each action | jsonb | No | None | Edit | No |
| decision_log_entry.outcome | Cash, cure, loss and time, written when known | jsonb | No | None | Edit | No |
| decision_log_entry.decided_at | When decided | timestamptz | Yes | None | Read | No |
| decision_log_entry.prev_hash | Hash of the previous entry | char(64) | Yes | None | Edit | No |
| decision_log_entry.entry_hash | Hash of this entry | char(64) | Yes | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P7-002 | Approver prepared the decision | You prepared this decision, so you cannot approve it. |
| MSG-P7-001 | Approval above the approver's limit | This needs approval at level {level}. It has been sent to {approver}. |
| MSG-P7-003 | Decision log write failed (principle 5) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-39 Rules and parameters

| Item | Value |
|---|---|
| Menu | Administration |
| What it is for | Rule versions, route sets, thresholds and timers, with the load and approval |
| Reached from | Menu |
| Module | P4 |
| Access | Rules and parameters, checked on every request |
| Who reaches it | Center of excellence analyst, reference data administrator, Risk |
| First in | E8; by file load before |
| Stories | RWB-AD-002, RWB-AD-007, RWB-AD-009, RWB-AD-010, RWB-AD-011, RWB-AD-012, RWB-AD-015, RWB-AD-016 |

**States.** Versions; load; approval.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| rule_row.rule_id | Rule ID, for example R-LIT-12 | varchar(20) | Yes | None | Edit | No |
| rule_row.rule_version | Version | varchar(20) | Yes | None | Edit | No |
| rule_row.route_set | Route set | varchar(15) | Yes | LOV-ROUTE-SET | Edit | No |
| rule_row.from_state | From state | varchar(60) | Yes | None | Edit | No |
| rule_row.event_code | Event | varchar(60) | Yes | None | Edit | No |
| rule_row.condition_expr | Condition | varchar(1000) | No | None | Edit | No |
| rule_row.action_text | Action | varchar(1000) | Yes | None | Edit | No |
| rule_row.to_state | To state | varchar(60) | Yes | None | Edit | No |
| rule_row.owner_role | Owner of the next state | varchar(20) | Yes | LOV-ROLE | Edit | No |
| rule_row.timer_spec | Timer | varchar(60) | No | None | Edit | No |
| rule_row.valid_from | Valid from | date | Yes | None | Edit | No |
| rule_row.valid_to | Valid to | date | No | None | Edit | No |
| rule_row.approved_by | Who approved the version | uuid | Yes | None | Edit | No |
| rule_row.test_case_id | Test case that proves the rule | varchar(20) | Yes | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P4-001 | Sign-in with no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A record outside the role's scope | This case is not in your scope. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-40 Reference data

| Item | Value |
|---|---|
| Menu | Administration |
| What it is for | Lists of values and reference tables with versions |
| Reached from | Menu |
| Module | P4 |
| Access | Reference data, checked on every request |
| Who reaches it | Reference data administrator |
| First in | E8; by file load before |
| Stories | RWB-AD-002, RWB-AD-007, RWB-AD-009, RWB-AD-010, RWB-AD-013 |

**States.** Versions; load.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| lov_value.lov_code | List code, for example LOV-ROUTE | varchar(30) | Yes | None | Edit | No |
| lov_value.value_code | Value code | varchar(30) | Yes | None | Edit | No |
| lov_value.label_en | English label | varchar(120) | Yes | None | Edit | No |
| lov_value.label_th | Thai label | varchar(120) | No | None | Edit | No |
| lov_value.sort_order | Display order | integer | Yes | None | Edit | No |
| lov_value.valid_from | Valid from | date | Yes | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P4-001 | Sign-in with no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A record outside the role's scope | This case is not in your scope. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-41 Delegation of authority

| Item | Value |
|---|---|
| Menu | Administration |
| What it is for | Approval levels, holders, limits and substitutes |
| Reached from | Menu |
| Module | P4 |
| Access | Rules and parameters, checked on every request |
| Who reaches it | Reference data administrator, Risk |
| First in | E8; by file load before |
| Stories | RWB-AD-008, RWB-AD-016 |

**States.** Versions; load; approval.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| delegation_limit.decision_code | Decision the limit applies to | varchar(8) | Yes | LOV-DECISION | Edit | No |
| delegation_limit.approval_level | Level 1 to 6 under Regulation กกค.540031 | varchar(4) | Yes | LOV-APPROVAL-LEVEL | Edit | No |
| delegation_limit.product_group | Product group | varchar(15) | Yes | LOV-PRODUCT | Edit | No |
| delegation_limit.principal_limit | Principal limit, baht; empty means no limit | numeric(18,2) | No | None | Edit | No |
| delegation_limit.loss_pct_limit | Loss limit as a percentage | numeric(5,2) | No | None | Edit | No |
| delegation_limit.min_price_pct_fmv | Lowest sale price as a percentage of fair market value | numeric(5,2) | No | None | Edit | No |
| delegation_limit.holder_user_id | Person holding the level | uuid | No | None | Edit | No |
| delegation_limit.substitute_user_id | Substitute when the holder is absent | uuid | No | None | Edit | No |
| delegation_limit.valid_from | Valid from | date | Yes | None | Edit | No |
| delegation_limit.valid_to | Valid to | date | No | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P4-001 | Sign-in with no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A record outside the role's scope | This case is not in your scope. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-42 Queues and service levels

| Item | Value |
|---|---|
| Menu | Administration |
| What it is for | Queues, caps, overflow and service levels per state |
| Reached from | Menu |
| Module | P4 |
| Access | Queue and allocation, checked on every request |
| Who reaches it | Reference data administrator, team manager |
| First in | E8; by file load before |
| Stories | RWB-AD-014, RWB-AD-015 |

**States.** Versions; load.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| queue.queue_code | Queue code | varchar(30) | Yes | None | Edit | No |
| queue.queue_name | Queue name | varchar(100) | Yes | None | Edit | No |
| queue.team_code | Team the queue belongs to | varchar(20) | Yes | LOV-TEAM | Edit | No |
| queue.role_code | Role that works the queue | varchar(20) | Yes | LOV-ROLE | Edit | No |
| queue.assignment_method | Round robin, lowest load, named owner, skill | varchar(20) | Yes | LOV-ASSIGN | Edit | No |
| queue.capacity_cap | Most open cases one person may hold in the queue | integer | No | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P4-001 | Sign-in with no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A record outside the role's scope | This case is not in your scope. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-43 Roles and access

| Item | Value |
|---|---|
| Menu | Administration |
| What it is for | Roles, permissions, scope and the group mapping, with the access log |
| Reached from | Menu |
| Module | P4 |
| Access | Platform administration, checked on every request |
| Who reaches it | Security administrator, application owner |
| First in | E8; by file load before |
| Stories | RWB-AD-001, RWB-AD-003, RWB-AD-004, RWB-AD-005, RWB-AD-006, RWB-AD-008 |

**States.** List; access log.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| role.role_code | Role code, for example RW-CASEOWN | varchar(20) | Yes | None | Edit | No |
| role.role_name | Role name | varchar(80) | Yes | None | Edit | No |
| role.role_class | Bank user, partner user, non-human actor | varchar(15) | Yes | LOV-ROLE-CLASS | Edit | No |
| role.default_scope | Own, team, region, all | varchar(8) | Yes | LOV-SCOPE | Edit | No |
| role.entra_group | Entra ID group mapped to the role | varchar(120) | No | None | Read | No |
| permission.capability_area | One of the 14 capability areas | varchar(30) | Yes | LOV-CAPABILITY | Edit | No |
| permission.letters | C, R, U, D and A, or a dash for none | varchar(5) | Yes | None | Edit | No |
| permission.matrix_version | Permission matrix version | varchar(20) | Yes | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P4-003 | A record outside the role's scope | This case is not in your scope. |
| MSG-P4-004 | Break-glass access is active | Emergency access is on until {time}. Every action is recorded. |
| MSG-P4-001 | Sign-in with no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-44 Interface and job monitor

| Item | Value |
|---|---|
| Menu | Administration |
| What it is for | Loads, files, jobs and outbound actions with status and reruns |
| Reached from | Menu |
| Module | P1 |
| Access | Platform administration, checked on every request |
| Who reaches it | Platform administrator, data steward |
| First in | E2; E8 full |
| Stories | RWB-AD-018 |

**States.** Running; failed; complete.

Measures and status from the reporting and monitoring data; no record fields are edited on this screen.

| Message | When | Text |
|---|---|---|
| MSG-P1-001 | Data product stale after a late or failed load | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Load refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-45 Data quality

| Item | Value |
|---|---|
| Menu | Administration |
| What it is for | Load check results, reconciliation breaks and stale data products |
| Reached from | Menu |
| Module | P1 |
| Access | Platform administration, checked on every request |
| Who reaches it | Data steward and data product owner |
| First in | E2; E8 full |
| Stories | RWB-E2-010, RWB-AD-018, RWB-AD-019 |

**States.** Loading; breaks.

Measures and status from the reporting and monitoring data; no record fields are edited on this screen.

| Message | When | Text |
|---|---|---|
| MSG-P1-001 | Data product stale after a late or failed load | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Load refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-46 Agent monitor

| Item | Value |
|---|---|
| Menu | Administration |
| What it is for | Agent runs, fallbacks, evaluation results and autonomy levels |
| Reached from | Menu |
| Module | P10 |
| Access | Platform administration, checked on every request |
| Who reaches it | Risk and model risk officer, center of excellence analyst |
| First in | E2; E8 full |
| Stories | RWB-E2-028, RWB-E2-029, RWB-E2-030, RWB-E2-031, RWB-AD-020 |

**States.** Shadow; live; paused.

Measures and status from the reporting and monitoring data; no record fields are edited on this screen.

| Message | When | Text |
|---|---|---|
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## SCR-47 Personal data

| Item | Value |
|---|---|
| Menu | Administration |
| What it is for | Retention classes, masking rules, consent log and data subject requests |
| Reached from | Menu |
| Module | P4 |
| Access | Platform administration, checked on every request |
| Who reaches it | Compliance and PDPA officer |
| First in | E8; by file load before |
| Stories | RWB-AD-004, RWB-AD-011, RWB-AD-012 |

**States.** Loading; list.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| document.document_type | Type from the document checklist | varchar(30) | Yes | LOV-DOC-TYPE | Edit | No |
| document.source | Scan, upload, generated, partner, email | varchar(12) | Yes | LOV-DOC-SOURCE | Edit | No |
| document.storage_ref | Reference to the stored file | varchar(400) | Yes | None | Edit | No |
| document.classification_confidence | OCR classification confidence | numeric(5,4) | No | None | Edit | No |
| document.review_status | Not needed, pending, confirmed, corrected | varchar(12) | Yes | LOV-REVIEW | Edit | No |
| document.retention_class | Retention class | varchar(10) | Yes | LOV-RETENTION | Edit | No |
| document.write_once | True for legal documents held write-once | boolean | Yes | None | Edit | No |
| document.doc_version | Document version | integer | Yes | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P4-001 | Sign-in with no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A record outside the role's scope | This case is not in your scope. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## PRT-01 Partner home

| Item | Value |
|---|---|
| Menu | Partner portal |
| What it is for | The partner's open instructions, due dates and messages |
| Reached from | Partner sign-in |
| Module | S9 |
| Access | Partner portal, checked on every request |
| Who reaches it | All partner users |
| First in | E2 |
| Stories | RWB-AD-022 |

**States.** Loading; list.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| partner_instruction.instruction_type | Collect, file suit, enforce, appraise, repossess, list, sell | varchar(20) | Yes | LOV-INSTRUCTION | Edit | No |
| partner_instruction.instructed_at | When instructed | timestamptz | Yes | None | Read | No |
| partner_instruction.due_at | When the result is due | timestamptz | No | None | Read | No |
| partner_instruction.status | Sent, accepted, declined, in progress, done, recalled | varchar(12) | Yes | LOV-INSTR-STATUS | Edit | No |
| partner_instruction.result_code | Result reported by the partner | varchar(40) | No | None | Edit | No |
| partner_instruction.fee_amount | Fee payable, baht | numeric(18,2) | No | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## PRT-02 Instruction

| Item | Value |
|---|---|
| Menu | Partner portal |
| What it is for | One instruction with its documents, due dates and the result to record |
| Reached from | Partner home |
| Module | S9 |
| Access | Partner portal, checked on every request |
| Who reaches it | Law firm, valuer, collection agency |
| First in | E4 |
| Stories | Built in its first release; story written one epic ahead |

**States.** New; accepted; in progress; result; closed.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| partner_instruction.instruction_type | Collect, file suit, enforce, appraise, repossess, list, sell | varchar(20) | Yes | LOV-INSTRUCTION | Edit | No |
| partner_instruction.instructed_at | When instructed | timestamptz | Yes | None | Read | No |
| partner_instruction.due_at | When the result is due | timestamptz | No | None | Read | No |
| partner_instruction.status | Sent, accepted, declined, in progress, done, recalled | varchar(12) | Yes | LOV-INSTR-STATUS | Edit | No |
| partner_instruction.result_code | Result reported by the partner | varchar(40) | No | None | Edit | No |
| partner_instruction.fee_amount | Fee payable, baht | numeric(18,2) | No | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## PRT-03 Upload result

| Item | Value |
|---|---|
| Menu | Partner portal |
| What it is for | Record a result and upload its documents |
| Reached from | Instruction |
| Module | S9 |
| Access | Partner portal, checked on every request |
| Who reaches it | Law firm, valuer, auction vendor, collection agency |
| First in | E4 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Form; saved.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| partner_instruction.instruction_type | Collect, file suit, enforce, appraise, repossess, list, sell | varchar(20) | Yes | LOV-INSTRUCTION | Edit | No |
| partner_instruction.instructed_at | When instructed | timestamptz | Yes | None | Read | No |
| partner_instruction.due_at | When the result is due | timestamptz | No | None | Read | No |
| partner_instruction.status | Sent, accepted, declined, in progress, done, recalled | varchar(12) | Yes | LOV-INSTR-STATUS | Edit | No |
| partner_instruction.result_code | Result reported by the partner | varchar(40) | No | None | Edit | No |
| partner_instruction.fee_amount | Fee payable, baht | numeric(18,2) | No | None | Edit | No |
| document.document_type | Type from the document checklist | varchar(30) | Yes | LOV-DOC-TYPE | Edit | No |
| document.source | Scan, upload, generated, partner, email | varchar(12) | Yes | LOV-DOC-SOURCE | Edit | No |
| document.storage_ref | Reference to the stored file | varchar(400) | Yes | None | Edit | No |
| document.classification_confidence | OCR classification confidence | numeric(5,4) | No | None | Edit | No |
| document.review_status | Not needed, pending, confirmed, corrected | varchar(12) | Yes | LOV-REVIEW | Edit | No |
| document.retention_class | Retention class | varchar(10) | Yes | LOV-RETENTION | Edit | No |
| document.write_once | True for legal documents held write-once | boolean | Yes | None | Edit | No |
| document.doc_version | Document version | integer | Yes | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## PRT-04 Invoice

| Item | Value |
|---|---|
| Menu | Partner portal |
| What it is for | Submit a fee invoice against completed instructions |
| Reached from | Instruction |
| Module | S9 |
| Access | Partner portal, checked on every request |
| Who reaches it | Law firm, valuer, auction vendor, collection agency |
| First in | E6 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Draft; submitted; approved; paid.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| partner_instruction.instruction_type | Collect, file suit, enforce, appraise, repossess, list, sell | varchar(20) | Yes | LOV-INSTRUCTION | Edit | No |
| partner_instruction.instructed_at | When instructed | timestamptz | Yes | None | Read | No |
| partner_instruction.due_at | When the result is due | timestamptz | No | None | Read | No |
| partner_instruction.status | Sent, accepted, declined, in progress, done, recalled | varchar(12) | Yes | LOV-INSTR-STATUS | Edit | No |
| partner_instruction.result_code | Result reported by the partner | varchar(40) | No | None | Edit | No |
| partner_instruction.fee_amount | Fee payable, baht | numeric(18,2) | No | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## PRT-05 Data room

| Item | Value |
|---|---|
| Menu | Partner portal |
| What it is for | Lot data tapes and documents for admitted buyers, with bids |
| Reached from | Partner home |
| Module | S6 |
| Access | Partner portal, checked on every request |
| Who reaches it | Debt buyer and AMC |
| First in | E5 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Admitted; bidding; closed.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| debt_sale_lot.lot_no | Lot number, for example 1/2024 | varchar(15) | Yes | None | Edit | No |
| debt_sale_lot.cut_off_date | Balance cut-off date | date | Yes | None | Edit | No |
| debt_sale_lot.segment | Segment of the lot | varchar(20) | Yes | LOV-SEGMENT | Edit | No |
| debt_sale_lot.reserve_price | Reserve price, baht | numeric(18,2) | No | None | Edit | No |
| debt_sale_lot.buyer_class | AMC or non-AMC | varchar(10) | No | LOV-BUYER-CLASS | Edit | No |
| debt_sale_lot.signing_date | Date the sale was signed | date | No | None | Edit | No |
| debt_sale_lot.approval_authority | Authority that approved the sale | varchar(60) | No | None | Edit | No |
| debt_sale_lot.payment_terms | Deposit and payment terms | varchar(400) | No | None | Edit | No |
| debt_sale_lot.status | Building, offered, awarded, transferred, closed | varchar(12) | Yes | LOV-LOT-STATUS | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-S6-001 | Account with an open deviation selected for a lot (R-DS-02) | {account} has an open deviation and cannot be sold. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

## PRT-06 Transfer confirmation

| Item | Value |
|---|---|
| Menu | Partner portal |
| What it is for | Confirm a transfer of assets or accounts |
| Reached from | Partner home |
| Module | S5 |
| Access | Partner portal, checked on every request |
| Who reaches it | RAMC user, debt buyer |
| First in | E4 |
| Stories | Built in its first release; story written one epic ahead |

**States.** Pending; confirmed.

| Field | Meaning | Type | Required | List | Edit | Personal data |
|---|---|---|---|---|---|---|
| asset.asset_ref | Asset reference | varchar(20) | Yes | None | Read | No |
| asset.asset_code | Asset code | varchar(20) | No | None | Read | No |
| asset.asset_type | Detached house, townhouse, condominium, land, vehicle | varchar(20) | Yes | LOV-ASSET-TYPE | Read | No |
| asset.transfer_in_type | Auction purchase, deed in lieu, repossession | varchar(20) | Yes | LOV-TRANSFER-IN | Read | No |
| asset.from_segment | Segment the asset came from | varchar(20) | No | LOV-SEGMENT | Read | No |
| asset.transfer_in_date | Date ownership passed to the bank | date | Yes | None | Read | No |
| asset.book_value | Book value, baht | numeric(18,2) | Yes | None | Read | No |
| asset.auction_purchase_price | Price paid at auction, baht | numeric(18,2) | No | None | Read | No |
| asset.repossessed_date | Date the vehicle was repossessed | date | No | None | Read | No |
| asset.stock_date | Date the vehicle entered stock | date | No | None | Read | No |
| asset.holding_status | Held, listed, under offer, sold, transferred, rented | varchar(15) | Yes | LOV-HOLDING | Edit | No |
| asset.holding_cost_to_date | Holding cost to date, baht | numeric(18,2) | No | None | Edit | No |

| Message | When | Text |
|---|---|---|
| MSG-S5-001 | Floor price below the approver's limit | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Appraisal older than one year | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-P4-002 | An action outside the role's permission | You cannot {action} here. Your role does not include it. |
| MSG-GEN-004 | Record changed by someone else | Someone else changed this record. Reload it to see their change. |

---

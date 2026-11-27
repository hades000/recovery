# RWB-P6-E1063-APP Agent monitoring dashboard v1 [E2c]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E1063-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-063 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-P6-I |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P10-E1063-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to REQ-DRI-009) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split of RWB-E1-063 for rwb-comms, carrying the cost-alert notification only, with no data lake and no dashboard copy. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P6-E1063-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **risk and model risk officer (RW-RISK) and a centre of excellence analyst holding the policy alert role (RW-COE)**, I want **the cost alert of an agent that spends above its daily limit delivered as one notice through the rwb-comms notification contract, with the legacy MSG-P10-004 text, the two recipient roles, the notice readable by its identifier, and the send kept and retried by the JOB-11 outbox relay when the notification path is down**, so that **a spend breach is seen in the first week of shadow running, is delivered once and only once, and survives an outage without P6 recomputing a measure or holding a copy of the agent data**.

### 2. Business rationale

An agent in shadow that spends twice its budget must be seen in the first week, not at the L1 review. RWB-E1-063 met that need with two deliveries in one module: a daily copy of the agent run figures to the data lake table `agent_run_daily`, matched by row count so the Power BI page read the copy and not the live tables (REQ-DRI-009), and a daily check that wrote one `agent_alert` row when the cost of an agent on a business date passed `agent_policy.daily_cost_cap_thb`, then sent MSG-P10-004 through the P6 notification interface to the policy alert role and to RW-RISK.

The target removes the data lake. Arch v5 slide 37 replaces "Data lake and Power BI feed (INT-19/20)" with "Removed: reports from rwb-reporting", and DP-17 records it as a decoupling with no dependency added. The legacy `agent_run_daily` lake table therefore has no target, and the Power BI claim of a lake copy has no source. The daily measures become a P9 rwb-reporting read model built from `rwb.agent.AgentRunCompleted.v1` and from the daily step that P10 runs, read through `GET /api/recovery/reporting/v1/reports/measures`; the daily step, the `agent_run`, `agent_policy` and `agent_alert` tables, the cap, the alert role and the alert row all stay with P10 rwb-agent; the session, the rights and the refusals stay with P4 rwb-access. The Power BI page and the SCR-46 agent monitor screen are not built here either. That removal is the change recorded for this key, and this story carries no lake, no dashboard copy and no recomputation of an agent measure.

What remains in rwb-comms is the one thing the legacy assigned to the notification interface: the delivery of MSG-P10-004. The integration story that fixes this story's boundary states it in its own words. RWB-ITG-E1063-ITG precondition: "RWB-P6-E1063-APP is done: rwb-comms (P6) serves the case message send and the notice read of section 12.2 through its published notification contract." Its AC2: "Then MSG-P10-004 is sent to the holders of RW-COE and RW-RISK through the P6 notification contract". Its BR7: "MSG-P10-004 goes to the holders of the policy alert role and to RW-RISK through the P6 notification contract; the alert is not case-bound, so the message is proved at the P6 boundary". Its contract table reads the send at `POST /api/recovery/comms/v1/cases/{caseId}/messages` and the result at `GET /api/recovery/comms/v1/notices/{noticeId}`, and its assumption ASM-0528 places the send on that operation with the JOB-11 outbox retry.

So this story is the notification slice and nothing else: one consumed contract of P10 for the alert facts, one template of the P6 template set, one notice, one send on the ACE notification path, one outbox retry, and one read. `notice`, `template` and `merge_field` are written only in schema `rwb_comms` by this service (DP-01). The cap, the alert role, the measured value and the threshold are P10 policy and alert values and are read, never recomputed and never copied (DP-11, DP-17). The operation sits on the service's own base `/api/recovery/comms/v1` (DP-13), the send waits in the outbox and is published as a CloudEvents fact (DP-09), and the reader reaches the notice through the gateway-bff composite route (DP-19). The service connects as the rwb-comms login; the one-login-per-service rule is DP-02, which is not in the pattern set of this key and is therefore not claimed here.

The alert is not case-bound, and the two sources do not name an operation or an event for it. P6 therefore serves it on the published message operation, with the alert's own reference in the path position of the case identifier and no case lookup, and the notice read returns that reference so the reader can tie the notice to the alert; the missing event name and the non-case binding are carried as GAP-1211 with ASM-2164 and ASM-2165.

### 3. Preconditions

- RWB-P10-E1063-CON is published: the shape of the alert facts of a business date — alert identifier, agent code, alert type "COST_CAP", business date, measured value, threshold value, policy alert role and the policy cap in force — and the contract of the event that announces the alert (DP-11, DP-09). The event name is Not specified in the source documents (GAP-1211; ASM-2165).
- P10 rwb-agent serves `GET /api/recovery/agent/v1/admin/agent-metrics` for a business date and returns the alert rows, the sums of runs and the source counts; it is the only reader of `agent_run`, `agent_policy`, `agent_alert`, `agent_evaluation` and the other tables of schema `rwb_agent` (DP-01).
- The "agent cost alert" template of the P6 template set, named by RWB-E1-063 section 13, is current and approved in `template` and carries the MSG-P10-004 text with the merge codes for the agent, the amount, the date and the limit. Its template code, version, language, channel and body are Not specified in the source documents (GAP-1209; ASM-2167).
- `merge_field` holds a merge code for each of the four values the message needs, so no value is written in code; the merge codes are rows of the P6 catalog and their source is the alert fact of the P10 contract, not a case field (DP-01).
- The ACE notification path to NSS SMS and LINE OA is available in the environment (legacy DL30), and its request and result shapes are carried by the stub of section 12.8 until the path publishes them (GAP-1209; ASM-2167).
- The outbox, inbox and idempotency library is live in schema `rwb_comms`, and JOB-11 Outbox sender runs every minute in every service (DP-09; Architecture v5 slide 44). The retry window and the attempt limit are Not specified in the source documents (GAP-1209; ASM-2167).
- The P3 rwb-case parameters contract serves the template code and the channel as versioned parameter rows, so neither is written in code (DP-06). The parameter codes are Not specified in the source documents (GAP-1209; ASM-2167); until RWB-P3-E1042-CON is published the read is answered by its contract fake.
- The reference data of the channel and the notice type is read through the P3 rwb-case reference-data contract (DP-07); the cost alert has no entry in LOV-NOTICE of the module specification, which carries DEMAND, RECALL, STATUTORY_SALE_NOTICE and GUARANTOR_NOTICE only (GAP-1209; ASM-2167).
- The per-service Flyway sequence of `rwb_comms` is in place, so this story's migration runs in `rwb_comms` and in no other schema (DP-15).
- The gateway-bff composite route is in place for the notice read (DP-19); no screen is built here.
- The right that guards the cost-alert notice read is Not specified in the source documents (GAP-1209; ASM-2167); the refusal is declared at gateway-bff and no authorisation logic is written in this story, because DP-08 is not in the pattern set of this key.
- No `agent_run`, `agent_alert`, `agent_policy`, `agent_evaluation`, `recovery_case`, `case_party` or `decision_log_entry` row is read or written directly: each arrives through its owner's contract (DP-01).
- The alert announced by the consumed event is a fact; the alert facts are read back through the P10 contract and the event carries no value this story acts on (GAP-1211; ASM-2165).
- The release date 30 November 2026 is tentative; a date is not a condition of this story.

### 4. Flow

1. P10 rwb-agent: the JOB-15 daily step of the business date finds the cost of the agent above the cap of its policy, writes one `agent_alert` row of type "COST_CAP" and announces it on `rwb.agent.events.v1` through its outbox. The alert row, the cap, the alert role and the measured and threshold values are P10 data.
2. rwb-comms: consumes the announcement once, deduping on the event identifier through the inbox, and treats the event as a trigger only; the event is not a carrier of a value this story acts on (DP-09).
3. rwb-comms: reads the alert facts of the alert through `GET /api/recovery/agent/v1/admin/agent-metrics` with one hop and a 2 s budget — the alert identifier, the agent code, the alert type, the business date, the measured value, the threshold value and the policy alert role (DP-11).
4. rwb-comms: writes no notice when the read returns no "COST_CAP" alert for the business date, so a cost at or below the cap, an agent with no runs and an agent with no alert produce no notice and no message (AC2, AC3, AC4). The comparison of the cost with the cap is P10's and is not repeated here.
5. rwb-comms: resolves the "agent cost alert" template as the current approved version for the alert type and the configured channel, and resolves its four merge codes — agent, amount, date and limit — against the alert facts, so the text is the MSG-P10-004 sentence with "SCREENING", 2,310.5000, 2026-12-01 and 2,000 in it and no business value in code.
6. rwb-comms: checks the alert identifier against the notice key. A notice already written for the alert is returned and no second notice and no second send follow, so a redelivered event or a rerun of the daily step produces one notice (AC5; R-UNI-40).
7. rwb-comms: writes the `notice` row in schema `rwb_comms` with the alert reference, the template and its version, the rendered text, the two recipient roles and the state, and writes one `NoticeGenerated` row in the outbox in the same transaction.
8. rwb-comms: calls the ACE notification path once for the two recipient roles and records the answer. The path accepted is state SENT with the send time; the path unavailable is state GENERATED with `sent_at` empty and `dispatch_attempts` 0, and the answer to the caller is MSG-GEN-006 naming the notification path (AC6).
9. Outbox relay JOB-11: publishes `rwb.comms.NoticeGenerated.v1` on `rwb.comms.events.v1` keyed by the alert reference, and the dispatch of step 8 writes `rwb.comms.NoticeDispatched.v1` on the same topic, so every send that eventually succeeds leaves one dispatched fact and no duplicate (R-UNI-33, R-UNI-35).
10. Reader: `GET /api/recovery/comms/v1/notices/{noticeId}` returns the notice with its state, its send time, its dispatch attempts, the template version, the two recipient roles and the alert reference. The read changes no row. A reader without the right is refused with 403 and MSG-P4-002 at gateway-bff (TC-E1-063-08).
11. rwb-comms: writes no measure, no daily row, no dashboard copy and no lake row: the measures stay in the P9 read model and the alert stays in P10 (DP-17).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The ACE notification path is unavailable at 01:40 | The notice is kept in state GENERATED with `sent_at` empty and `dispatch_attempts` 0; JOB-11 retries the send and exactly one message reaches the two recipient roles when the path answers | MSG-GEN-006 | AC6, TC-E1-063-07 |
| X2 | The same alert is announced twice, or the daily step is rerun for a business date already notified | The notice key on the alert identifier returns the first notice; no second notice and no second message | None | AC5, TC-E1-063-04 |
| X3 | The alert facts read does not answer inside 2 s, or answers with a partial body | No notice is written on a partial answer; the caller is told the system is unavailable and the request is retried on the redelivery of the alert | MSG-GEN-006 | AC1, TC-E1-063-02 |
| X4 | The alert facts read returns no "COST_CAP" alert for the business date | No notice and no message; the reason is the P10 alert row and not a P6 decision | None | AC2, AC3, AC4 |
| X5 | The cost equals the cap exactly | No alert row at P10 and therefore no notice; the strict greater-than comparison stays P10's | None | AC3, TC-E1-063-06 |
| X6 | The "agent cost alert" template is withdrawn and no later version is approved | The notice is held with `hold_reason` "TEMPLATE_WITHDRAWN" and no message leaves; the task is raised to the role that owns the template set, whose name is Not specified in the source documents (GAP-1209; ASM-2167) | MSG-P6-003 | AC1 |
| X7 | A reader without the right asks for the cost-alert notice | The read is refused at gateway-bff; nothing is returned | MSG-P4-002 | TC-E1-063-08 |
| X8 | The consumed event arrives twice with the same event identifier | The inbox drops the second one and records the idempotency hit; no second notice | None | AC5, TC-E1-063-04 |
| X9 | The notice reference of the alert is not a case identifier | The published message operation is used with the alert reference in the path position of the case identifier, no case lookup is made and no case value is read (GAP-1211; ASM-2164) | None | AC1 |

X1 to X7 are the legacy exception paths of RWB-E1-063 that fall inside the notification slice; the row-count and lake-write paths X1, X2 and the dashboard access path X6 of the legacy story belong to P9, P10 and P4 and are not carried here. X8 and X9 are the failures that appear only once the send sits behind a consumed event and a published operation.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P10-E1063-CON and its fake; the alert, the cap, the alert role, the agent runs and the measures are stubbed, and no `rwb_agent` table and no P10 code is touched |
| Negotiable | The template code, the channel, the retry window and the recipient role list are configuration or P10 answers; the message text, the strict greater-than rule, the one-notice key and the outage behaviour are fixed |
| Valuable | A spend breach reaches the two roles that must see it as one notice, once, through the path the bank already operates and with a retry the platform already runs |
| Estimable | One service, one consumed read, one template, two events, one notice read and one migration of no new agent column |
| Small | Fits one sprint with its tests |
| Testable | Each criterion is a component or end-to-end test on fixed alert facts of one business date, with the P10 contract faked and the notification path recorded |

### 7. Acceptance criteria

```gherkin
Feature: Agent monitoring dashboard v1 [E2c], the cost-alert notification

  Background:
    Given agents "INTAKE" (policy "P1", prompt "PR1") and "SCREENING" (policy "P1", prompt "PR1") run in shadow on 2026-12-01
    Given on business date 2026-12-01 "INTAKE" has 120 runs, 9 with fallback, cost 1,840.0000 baht
    Given on 2026-12-01 "SCREENING" has 150 runs, 21 with fallback, cost 2,310.5000 baht
    Given both policies have daily_cost_cap_thb 2,000 and alert_role "RW-COE"
    Given the "agent cost alert" template of the P6 template set is current and approved with the MSG-P10-004 text and the merge codes for agent, amount, date and limit
    Given the template code and the channel are versioned parameter rows read through the rwb-case parameters contract, not values in code

  Scenario: AC1 A cost above the cap produces one notice for RW-COE and RW-RISK (new, D-RCV-60)
    Given the rwb-agent contract mock returns the "COST_CAP" alert of "SCREENING" for business date 2026-12-01 with measured 2,310.5000, threshold 2,000, cap 2,000 and alert role "RW-COE"
    When the alert is announced on rwb.agent.events.v1 and rwb-comms is asked to notify
    Then one notice exists for the alert with the exact legacy text "SCREENING used 2,310.5000 baht of model calls on 2026-12-01, above the daily limit of 2,000 baht."
    Then the notice is addressed to the holders of RW-COE and to RW-RISK
    Then GET /api/recovery/comms/v1/notices/{noticeId} returns the notice with its text, its two recipient roles and the alert reference
    Then one rwb.comms.NoticeGenerated.v1 and one rwb.comms.NoticeDispatched.v1 are written for the notice

  Scenario: AC2 A cost below the cap produces no message (new, D-RCV-60)
    Given the rwb-agent contract mock returns no "COST_CAP" alert for "INTAKE" on 2026-12-01, because 1,840.0000 baht is below the cap of 2,000
    When the daily step of the business date completes
    Then no notice is written for "INTAKE"
    Then the ACE notification path receives no message for 2026-12-01

  Scenario: AC3 A cost equal to the cap produces no message (new, D-RCV-60)
    Given the rwb-agent contract mock returns no "COST_CAP" alert for "INTAKE" on 2026-12-02, because 2,000.0000 baht equals the cap of 2,000
    When the daily step of 2026-12-02 completes
    Then no notice is written for "INTAKE" on 2026-12-02
    Then no message is sent for that alert

  Scenario: AC4 An agent with no runs produces no message (new, D-RCV-60)
    Given agent "EXTRACT" has an approved policy and no runs on 2026-12-01
    Given the rwb-agent contract mock returns "EXTRACT" with runs 0 and cost 0.0000 and no "COST_CAP" alert for 2026-12-01
    When the daily step of the business date completes
    Then no notice is written for "EXTRACT"
    Then the ACE notification path receives no message for "EXTRACT"

  Scenario: AC5 The same alert notified again produces one notice (new, D-RCV-60)
    Given one notice exists for the "COST_CAP" alert of "SCREENING" on 2026-12-01
    Given the rwb-agent contract mock returns the same alert when the alert is announced again for 2026-12-01
    When rwb-comms is asked to notify a second time
    Then the same notice is returned and no second notice is written
    Then the ACE notification path receives one message for the alert

  Scenario: AC6 A notification outage keeps the notice for the outbox retry (new, D-RCV-60)
    Given the rwb-agent contract mock returns a "COST_CAP" alert of "SCREENING" with measured 2,310.5000 and threshold 2,000 for a fresh business date after 2026-12-02
    Given the ACE notification path is unavailable at 01:40
    When rwb-comms is asked to notify
    Then the notice is kept with sent_at empty and its dispatch attempts at 0
    Then the notice is sent when the JOB-11 outbox sender succeeds (R-UNI-33, R-UNI-35)
    Then exactly one message reaches the holders of RW-COE and RW-RISK

  Scenario: AC7 No personal data in the notice or the message (new, D-RCV-60)
    Given the notice, the two events and the log lines of the "COST_CAP" alert of "SCREENING" on 2026-12-01
    When the scan runs
    Then they hold the agent code, the business date and the amounts only
    Then the scan finds no national ID number, phone number, name or account number
```

Every criterion of this story is new (D-RCV-60), because the legacy criteria of RWB-E1-063 speak either to the lake copy and the count check, which DP-17 removes, or to the dashboard read and the dashboard refusal, which are P9's and P4's. The legacy values are copied character for character so that a reader can follow the legacy story beside this one: the two agents "INTAKE" and "SCREENING", policy "P1", prompt "PR1", the business dates 2026-12-01 and 2026-12-02, INTAKE 120 runs with 9 fallbacks and 1,840.0000 baht, SCREENING 150 runs with 21 fallbacks and 2,310.5000 baht, `daily_cost_cap_thb` 2,000, `alert_role` "RW-COE", the alert type "COST_CAP", measured 2,310.5000, threshold 2,000, agent "EXTRACT" with no runs, 2,000.0000 baht on 2026-12-02, MSG-P10-004 and the JOB-11 outbox relay under R-UNI-33 and R-UNI-35. The alert facts arrive on a `rwb-agent contract mock` line, so the component test runs before P10 is live and every value stays the legacy value.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A cost alert is notified when the cost of an agent on a business date is above `agent_policy.daily_cost_cap_thb` (2,000 baht, assumed; DL33); a cost equal to the cap raises no alert and therefore no notice | RWB-E1-063 BR3; DF-AGT-013 |
| BR2 | One notice per agent alert: a rerun of the daily step, a redelivery of the event or a repeated request produces no second notice and no second message | RWB-E1-063 BR4; R-UNI-40; notice key on the alert reference |
| BR3 | The notice text is MSG-P10-004 verbatim, with the agent, the amount, the date and the limit bound from the alert facts and from no other source | RWB-E1-063 section 14; merge_field catalog |
| BR4 | The notice goes to the holders of the policy alert role and to RW-RISK | RWB-E1-063 BR6; DF-AGT-015; RWB-ITG-E1063-ITG BR7 |
| BR5 | When the ACE notification path is unavailable the notice is kept with `sent_at` empty and is sent by the JOB-11 outbox relay; exactly one message results from the alert | R-UNI-33; R-UNI-35; R-UNI-40; RWB-ITG-E1063-ITG BR8 |
| BR6 | This service owns the notice only: the alert row, the policy, the cap, the alert role, the runs, the evaluations and the measures stay with P10 rwb-agent, and the dashboard read stays with P9 rwb-reporting | DP-01; DP-17; Arch v5 slides 15, 16, 37 and 41; `_work/msr/plan/ownership.json` |
| BR7 | There is no data lake and no dashboard copy in this story: no `agent_run_daily` table, no lake schema, no INT-19 and no INT-20 connection, and no measure recomputed or stored in `rwb_comms` | DP-17; Arch v5 slide 37; GAP-1210 |
| BR8 | No business value in code: the template code, the channel, the agent codes, the cap, the alert role, the amounts and the dates are parameter rows, reference rows or contract answers read at run time | RWB-E1-063 section 17; Principle 1 |
| BR9 | The notice, the two events and the log hold the agent code, the business date and amounts only; no national ID number, phone number, name or account number appears in any of them | RWB-E1-063 section 17; CTL-11; AC7 |
| BR10 | Every consumed call is one hop to the owning service on its own base with a 2 s client budget, a breaker per downstream and a single GET retry with jitter; no service reads another service's table | DP-11; ADR-020 |
| BR11 | The delivery target is 15 minutes after the end of the daily step (target, DL11, NFR-068); it is a target and not a value in code | RWB-E1-063 BR6 |
| BR12 | A withdrawn template holds the notice with `hold_reason` "TEMPLATE_WITHDRAWN" and no message leaves | FSD P6 VR-P6-001-1; R-LIT-04; MSG-P6-003 |
| BR13 | The strict greater-than comparison of cost with the cap is P10's and is not repeated here; this story notifies an alert that P10 has already raised | RWB-E1-063 section 5 X4; RWB-ITG-E1063-ITG BR4 |

### 9. State transitions

None of a case: the story changes no case status and touches no case row. The agent alert is P10's row and its RAISED and SENT states belong to RWB-P10-E1063-APP. This story sets the notice state (standard column `state`) and the notice's own send time:

| From | Event | Condition | To |
|---|---|---|---|
| None | The alert is announced and the facts are read | The "COST_CAP" alert exists for the business date and the template is current and approved | GENERATED, then SENT with `sent_date` set when the path accepts |
| None | The alert is announced | The ACE notification path is unavailable at 01:40 | GENERATED with `sent_at` empty and `dispatch_attempts` 0 |
| GENERATED with `sent_at` empty | The JOB-11 outbox sender succeeds | None | SENT with `sent_date` set, and one `NoticeDispatched` in the outbox |
| None | The alert is announced | The template is withdrawn and no later version is approved | HELD with `hold_reason` "TEMPLATE_WITHDRAWN", no send |
| None | The alert is announced | The facts read returns no "COST_CAP" alert for the business date | No row |
| SENT | A redelivery of the same alert or a rerun of the daily step | A notice already exists for the alert reference | No transition and no second row |
| Any | A read of the notice | Never | The same state; a read changes no row |

The word `sent_at` in the criteria and in the legacy exception path X5 is the alert's field (DF-AGT-111) and is P10's to write. In rwb-comms the same fact is the notice's own send time, held on `sent_date` (DF-LEG-019) and empty until a send succeeds; the notice read returns it as the notice send time and returns the alert reference so a reader can tie the two. This story writes no `agent_alert` column (DP-01).

### 10. Authority

The roles below are taken from the rwb-comms RBAC matrix of the module specification, from the legacy authority table, and from the alert role the legacy story names; no other table is used.

| Who | What they may do in this story |
|---|---|
| rwb-comms service identity (the rwb-comms login) | Serves the two operations, reads the one P10 contract and the P3 parameter and reference contracts, writes `rwb_comms` only |
| RW-COE, centre of excellence analyst | Receives the cost alert as the policy alert role; reads the notice for the alert |
| RW-RISK, risk and model risk officer | Receives the cost alert; reads the notice for the alert |
| RW-BIANAL, BI analyst | Reads the notice for the alert; builds no dashboard in this story, because the dashboard read is P9's |
| RW-PLATADM, platform administrator | Reads the notice record and the dispatch attempts of the alert; reruns no job in this story, because the rerun is P1's and P10's |
| RW-CASEOWN, case owner | Nothing in this story: the cost-alert notice read is refused with 403 and MSG-P4-002 (TC-E1-063-08) |
| No role | Writes an `agent_alert`, `agent_policy` or `agent_run` row from outside P10, recomputes a measure, connects a data lake, or takes production data into a test |

No delegation-of-authority level applies: the alert is not a credit or route decision, and this story approves nothing. The right that guards the cost-alert notice read is Not specified in the source documents (GAP-1209; ASM-2167), and the refusal itself is enforced at gateway-bff and not in this story, because DP-08 is not in the pattern set of this key.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice (P6 rwb_comms) | id | Write |
| DF-LEG-016 | notice (P6 rwb_comms) | case_id | Write the alert reference in this position, because the alert is not case-bound (GAP-1211; ASM-2164) |
| DF-LEG-018 | notice (P6 rwb_comms) | notice_type | Write the type carried on the request; the list of values has no entry for an agent cost alert (GAP-1209; ASM-2167) |
| DF-LEG-019 | notice (P6 rwb_comms) | sent_date | Write on a successful send; empty while the notice waits for the retry |
| DF-LEG-030 | notice (P6 rwb_comms) | party_id | Not written: the recipient is a role, not a party |
| DF-LEG-031 | notice (P6 rwb_comms) | template_id | Write |
| DF-LEG-032 | notice (P6 rwb_comms) | hold_reason | Write on the withdrawn-template path |
| DF-LEG-034 | notice (P6 rwb_comms) | dispatch_attempts | Write, starting at 0 and incremented by the retry |
| Standard column | notice (P6 rwb_comms) | state, version, created_at, updated_at | Write |
| DF-REF-045 to DF-REF-047 | template (P6 rwb_comms) | id, template_code, template_version | Read |
| DF-REF-048 to DF-REF-051 | template (P6 rwb_comms) | language, product_group, body_ref, approved_by_legal | Read |
| DF-REF-065, DF-REF-066, DF-REF-067 | template (P6 rwb_comms) | valid_from, channel, notice_type | Read |
| DF-REF-069 | template (P6 rwb_comms) | merge_codes | Read |
| DF-REF-252 to DF-REF-260 | merge_field (P6 rwb_comms) | id, merge_code, source_entity, source_field, field_id, is_required, personal_data, catalog_version, valid_from | Read |
| DF-AGT-103 to DF-AGT-111 | agent_alert (P10 rwb_agent) | id, agent_code, alert_type, business_date, measured_value, threshold_value, sent_to_role, sent_at | Read through the P10 contract only; no column written here |
| DF-AGT-013, DF-AGT-015 | agent_policy (P10 rwb_agent) | daily_cost_cap_thb, alert_role | Read through the P10 contract only |
| DF-AGT-037, DF-AGT-054 | agent_run (P10 rwb_agent) | agent_code, cost_thb | Read through the P10 contract only, for the alert the contract returns; no run is aggregated here |
| Not a BR field of this key | alert reference and rendered text of the notice | the alert identifier, the notice text and the two recipient roles | Written on the notice row; the reference columns are Not specified in the source documents (GAP-1209; ASM-2167) |
| Not a BR field of this key | outbox_event, processed_event, idempotency_key (PLT library in `rwb_comms`) | event, topic, key, payload, dedupe key | Write and read (DP-09) |

Field IDs are those of RWB-E1-063 and of the module specification and are copied unchanged. The legacy lake table `agent_run_daily` is not listed because it has no target: the data lake is removed and the daily measure is a P9 read model (DP-17; GAP-1210). No `document`, `recovery_case`, `case_party`, `task`, `agent_alert`, `agent_policy`, `agent_run`, `agent_evaluation` or `decision_log_entry` row is read or written directly. The schema is `rwb_comms`, its migration runs in the per-service Flyway sequence (DP-15), and the service holds no foreign key into another schema (DP-01). This story stores no case of record, no copy of the alert and no daily row.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`; naming per the service catalog and DP-13.

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| API-P6-008 | POST | `/cases/{caseId}/messages` | Send the cost-alert notification for an alert: read the alert facts through the P10 contract, resolve the "agent cost alert" template, render the MSG-P10-004 text and send it to the two recipient roles; answer with the notice | Case record, right C, scope applied; the guard right of the cost-alert notice is Not specified in the source documents (GAP-1209; ASM-2167) | `Idempotency-Key` header, and the alert reference as the natural key |
| API-P6-002 | GET | `/notices/{noticeId}` | Read one notice with its state, its send time, its dispatch attempts, the template version, the two recipient roles and the alert reference; answer 200 with the notice | Litigation, right R, scope applied; refused with 403 and MSG-P4-002 for a role without the right | Not applicable |

Errors for API-P6-008: 401, 403, 404, 409, 422, 503. Errors for API-P6-002: 401, 403, 404, 503. The two paths, their identifiers and their error sets are those of the module specification, read on the service base of DP-13. The request and answer shapes and the field names of the Notice resource are Not specified in the source documents (GAP-1209; ASM-2167); RWB-P10-E1063-CON fixes only the consumed alert-fact shape, not this side.

The path position `{caseId}` carries the alert reference in this story, because the cost alert is not case-bound and the published operation is the only notification send of the service (GAP-1211; ASM-2164). No case read is made and no `recovery_case` row is required.

#### 12.2 REST operations consumed

| Method and path | Owner | Use in this story | Budget |
|---|---|---|---|
| GET `/api/recovery/agent/v1/admin/agent-metrics` | P10 rwb-agent | AC1 to AC6: the "COST_CAP" alert of a business date with its alert identifier, agent code, alert type, business date, measured value 2,310.5000, threshold value 2,000, policy cap 2,000 and alert role "RW-COE", and no alert for "INTAKE" at 1,840.0000 or at 2,000.0000 and none for "EXTRACT" | 2 s |
| GET `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The template code and the channel as versioned parameter rows, filtered by parameter code, so neither is written in code (DP-06); the parameter codes are Not specified in the source documents (GAP-1209; ASM-2167) | 2 s |
| GET `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | The channel and notice-type lists, so the channel is a data row (DP-07) | 2 s |

Every row is one hop on the owner's base with a 2 s timeout, a breaker per downstream and a single GET retry with jitter (DP-11, ADR-020). The P3 rows are answered by their contract fake until RWB-P3-E1042-CON and RWB-P3-E1043-CON are published; the plan's H and C lists do not carry those two contracts and the omission is carried as GAP-1212 with ASM-2166.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Schema element (IDs and facts only) |
|---|---|---|---|---|
| `rwb.comms.NoticeGenerated.v1` (EV-13) | `rwb.comms.events.v1` | P6 rwb-comms | the alert reference | noticeId, alertReference, alertType "COST_CAP", agentCode, businessDate, measuredValue, thresholdValue, templateCode, templateVersion, generatedAt |
| `rwb.comms.NoticeDispatched.v1` (EV-14) | `rwb.comms.events.v1` | P6 rwb-comms | the alert reference | noticeId, alertReference, sentToRole (RW-COE, RW-RISK), sentAt, dispatchAttempts |

Both events are written to the outbox in the same transaction as the notice row and the send, and neither carries a notice body, a personal value or a measure that P9 owns. The two event names and the topic are the ones of Architecture v5 slides 17 and 42; the element list is not enumerated in the source documents beyond the legacy payload, so each field is carried with the placeholder of GAP-1209 and ASM-2167.

#### 12.4 Events consumed

| Event | Topic | Owner | Declared shape | Handler in this story |
|---|---|---|---|---|
| `rwb.agent.AgentAlertRaised.v1` (proposed name; Not specified in the source documents (GAP-1211; ASM-2165)) | `rwb.agent.events.v1` | P10 rwb-agent | alertReference, agentCode, alertType "COST_CAP", businessDate, raisedAt | One trigger per alert; the inbox dedupes on the event identifier and the handler reads the alert facts back through the P10 contract of 12.2 before it writes anything |

The name of the event is not in the event catalogue of Architecture v5 slides 42 and 43, which carries `AgentRunCompleted` only, and it is not in the legacy payload either. The proposed name follows the naming rule `rwb.<short>.<Event>.v1` of section R4 and is flagged for P10 to confirm. The event carries the alert reference and the facts that identify the alert and no value that this story acts on, so a wrong or stale event body cannot put a wrong amount in a notice.

#### 12.5 Workflows and activities

None. The send is synchronous inside rwb-comms: the POST answers with the notice and its state, and the retry is the platform outbox relay and not a workflow. No workflow, activity or Nexus operation is started here, and no workflow input carries an alert amount or a personal value. `NoticeDispatchWorkflow` exists in the service (Architecture v5 slide 17) and belongs to the WIN letter loop, which is RWB-P6-E2021-APP; it is not started for a cost alert, and no Schedule of it is registered here.

#### 12.6 Schedules

| Job | Owner | When | Mechanism | What the story asserts |
|---|---|---|---|---|
| JOB-11 Outbox sender | every service, including rwb-comms | every minute | outbox relay to Kafka, with the send retried from the outbox | A notice kept with `sent_at` empty after the 01:40 outage is retried until exactly one message reaches RW-COE and RW-RISK, and no second notice is written (AC6; R-UNI-33, R-UNI-35) |

JOB-15 Reporting extract at 01:30 is owned by P9 rwb-reporting as an Airflow trigger that calls the P10 daily step, and it is not registered, started or rerun by this story. No Quartz table, no Temporal Schedule and no shared job table is read (DP-10; Architecture v5 slide 44).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| notice | P6 (rwb_comms) | The cost-alert notice: the alert reference, the template, the rendered text, the two recipient roles, the send time, the dispatch attempts and the state |
| template | P6 (rwb_comms) | The "agent cost alert" template and its approved version; written by RWB-P6-E1046-APP |
| merge_field | P6 (rwb_comms) | The four merge codes of the message and their source field; written by RWB-P6-E1046-APP |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The outbox of the two published events, the inbox of the one consumed event and the `Idempotency-Key` answer store (DP-09) |

Not owned and never read directly: `agent_run`, `agent_policy`, `agent_alert`, `agent_evaluation`, `agent_evaluation_run` and the other agent tables (P10 rwb_agent); the reporting measures and the daily read model (P9 rwb_reporting); `recovery_case`, `case_party`, `task`, `timer` and `parameter_value` (P3 rwb_case); `role`, `permission` and `masking_rule` (P4 rwb_access); `document` (P5 rwb_document); `decision_log_entry` (P7 rwb_decision). No lake table, no lake schema and no reporting copy is created or read (DP-17).

#### 12.8 Contract fakes

| Fake | Serves | Documented answers |
|---|---|---|
| rwb-agent WireMock | RWB-P10-E1063-CON | The "COST_CAP" alert of "SCREENING" for 2026-12-01 with measured 2,310.5000, threshold 2,000, cap 2,000, alert role "RW-COE" and the alert reference; no alert for "INTAKE" at 1,840.0000 on 2026-12-01 or at 2,000.0000 on 2026-12-02; "EXTRACT" with runs 0, cost 0.0000 and no alert; the same alert on a redelivery; an empty answer for a date with no alert; a partial body; and a delayed answer beyond 2 s |
| rwb-case parameters WireMock | RWB-P3-E1042-CON | The template code and the channel as versioned parameter rows; a parameter absent answer; and a delayed answer beyond 2 s |
| rwb-case reference-data WireMock | RWB-P3-E1043-CON | LOV-CHANNEL with SMS, LINE, LETTER and PORTAL; LOV-NOTICE with DEMAND, RECALL, STATUTORY_SALE_NOTICE and GUARANTOR_NOTICE; and a delayed answer beyond 2 s |
| Notification path capture stub | The ACE notification path to NSS SMS and LINE OA (INT-17 and INT-18) | Records the message and its two recipient roles, returns accepted, returns unavailable at 01:40 and then accepted on the retry, so that a message can be read without an SMS or a LINE message leaving the building (GAP-1209; ASM-2167) |

The four fakes are the only elements outside the service. The template, the merge codes and the notice are this service's own rows and are not faked.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 | 3 | API-P6-008 and API-P6-002 provided; the P10 alert read and the two P3 parameter and list reads consumed, one hop each with a 2 s budget (DP-11, DP-13) |
| Kafka | 2 events published | 1 event type consumed | `NoticeGenerated` and `NoticeDispatched` on `rwb.comms.events.v1`; the proposed `rwb.agent.AgentAlertRaised.v1` on `rwb.agent.events.v1`; CloudEvents 1.0, outbox and inbox (DP-09) |
| Temporal | None | None | No workflow, no activity and no Schedule in this story (12.5, 12.6) |
| File | None | None | No file: the cost alert is a message on the ACE notification path and no letter, no PDF and no reporting file is produced |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `notifications`, Java package `th.co.scb.ace.workbench.recovery.comms.notifications`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_comms`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency, which is RWB-P10-E1063-CON) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**How each pattern lands, and DP-17 in particular.** DP-01 holds because `notice`, `template` and `merge_field` are the only business tables written, all in `rwb_comms`, and the alert is read through the P10 contract and never from `rwb_agent`. DP-06 and DP-07 hold because the template code, the channel and the lists are parameter and reference rows of rwb-case and no value of either is written in code. DP-09 holds because both published events go to the outbox in the same transaction as the notice row and the consumed alert event is deduped through the inbox. DP-10 holds because the legacy Quartz shape of JOB-15 is gone: the alert arrives as an event, the retry is the JOB-11 outbox relay of Architecture v5 slide 44, and this service registers no Schedule and no cron entry. DP-11 and DP-13 hold because every consumed call is one hop on the owner's base with a 2 s budget, and the two provided operations sit on `/api/recovery/comms/v1`. DP-15 holds because the migration runs in the rwb-comms Flyway sequence. DP-19 holds because the notice read is served for the gateway-bff composite route.

DP-17 is the change of this key and it removes work rather than adding it: there is no data lake, no `agent_run_daily` table, no lake schema, no INT-19 or INT-20 connection, no dashboard copy and no reporting file in this story. The daily measures are a P9 rwb-reporting read model and the dashboard is a P9 report read; this story neither computes a measure nor holds a copy of one, and it does not build the Power BI page of the legacy story, which has no source without a lake. DP-17 adds no dependency; the removal of the dashboard from P6 is the gap GAP-1210 with ASM-2168.

The six platform contracts and the two P3 contracts that DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 add are not in the H and C lists of the plan for this story, which carry None and RWB-P10-E1063-CON only. They are carried as GAP-1212 with ASM-2166: the platform libraries and the gateway route are the service template baseline that every wave-1 service already has, and the two P3 reads are answered by their contract fakes until the contracts are published, so neither blocks the Day-1 start.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| NotificationController | Controller | `POST /cases/{caseId}/messages` and `GET /notices/{noticeId}`, with validation and the problem mapping of the error envelope |
| CostAlertNoticeService | Service | Steps 2 to 9 of the flow: the dedupe, the alert-fact read, the no-alert paths, the template resolution, the notice write, the send and the state |
| AlertFactReader | Client | The P10 alert read of 12.2, one hop with the 2 s budget, and the empty, the partial and the delayed answers |
| NoticeTemplateSelector | Service | The current approved "agent cost alert" version for the alert type and the configured channel, from `template` |
| AlertMergeResolver | Service | Binds each of the four merge codes to the alert fact named by `merge_field.source_field` and renders the MSG-P10-004 sentence |
| NotificationPathClient | Client | Calls the ACE notification path once for the two recipient roles and returns accepted or unavailable |
| NoticeRepository | Repository | Reads and writes `notice`; finds by the alert reference and by the notice identifier |
| CommsEventPublisher | Service | Writes `NoticeGenerated` and `NoticeDispatched` to the outbox, and reads the inbox dedupe of the consumed alert event |
| NoticeReadService | Service | Answers the notice read with its state, its send time, its dispatch attempts, the template version, the two recipient roles and the alert reference |

**Database and migrations**

- Writes `notice`, reads `template` and `merge_field`, all in schema `rwb_comms`, and writes the outbox, inbox and idempotency rows of the platform library (DP-01, DP-09).
- Migration `V1063_1__agent_cost_alert_notice.sql` in the rwb-comms Flyway sequence: the unique index on the alert reference, so one notice per alert, and the check constraint on `state` in ('GENERATED','HELD','APPROVED','SENT','DELIVERED','UNSERVED'). No agent column, no daily row, no lake table and no measure column is added (DP-15, DP-17).
- The alert reference column and the rendered text column are new columns of `notice` whose names are Not specified in the source documents (GAP-1209; ASM-2167).

**Configuration and reference data**

- The template code and the channel are versioned parameter rows read through the P3 parameters contract (DP-06); their codes and values are Not specified in the source documents (GAP-1209; ASM-2167).
- The cap 2,000, the alert role "RW-COE", the measured value, the threshold value and the business date are P10 policy and alert values read through the alert read; they are never P6 configuration, never a default and never a value in code (BR1, BR8).
- LOV-CHANNEL and the notice-type list are reference rows read through the P3 reference-data contract (DP-07).
- The retry window and the attempt limit of the outbox relay are platform configuration; the legacy names no value for them (GAP-1209; ASM-2167).
- The feature flag is `rwb.comms.agent-cost-alert`. Off: the consumed alert event is left in the inbox and no notice is written; the P10 alert row and its `sent_at` stay as P10 left them.
- The login is the rwb-comms login; its name is allocated by the platform database story and is not fixed here.

**Build steps**

1. Migration and `NoticeEntity`: the unique index on the alert reference, the state check and a test for each.
2. `AlertFactReader` against the rwb-agent WireMock, with the alert of "SCREENING", the no-alert answers for "INTAKE" and "EXTRACT", the partial body and the delayed answer (AC1 to AC4, X3, X4).
3. `NoticeTemplateSelector` and `AlertMergeResolver` with the four merge codes and the exact MSG-P10-004 sentence of AC1, and the withdrawn-template hold of X6.
4. `CostAlertNoticeService` with the dedupe on the alert reference and the inbox, and the one-notice test of AC5 behind a redelivery and a rerun.
5. `NotificationPathClient` against the capture stub, with the accepted answer, the unavailable answer at 01:40 and the single send after the retry (AC6).
6. `CommsEventPublisher` with the two events, their key and their element list; assert that no notice body and no personal value is in either.
7. `NoticeReadService` and the refusal of the read for a role without the right (TC-E1-063-08, X7).
8. The feature flag, the parameters and the reference reads, each against its fake.
9. The personal-data scan of AC7 over the notice, the two events and the log lines.
10. The contract-fake run of the four stubs, so the story builds before P10, P3 and the notification path are live, and the absence test that no lake table, no lake schema and no `agent_run_daily` row is created.

**Done when.** The eight test cases of section 16 pass, the exact MSG-P10-004 sentence reaches the holders of RW-COE and RW-RISK once for the "SCREENING" alert of 2026-12-01, no notice exists for "INTAKE" or for "EXTRACT" and none for the 2,000.0000 baht case of 2026-12-02, the notice kept at 01:40 is sent exactly once after the JOB-11 retry, no lake table and no dashboard copy exists in the service, and the scan finds no personal data.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-004 | Agent cost on a business date above its daily limit | {agent} used {amount} baht of model calls on {date}, above the daily limit of {limit} baht. |
| MSG-GEN-006 | The ACE notification path is unavailable, so the send is queued and retried | {system} is not available. Your request is queued and will be retried. |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P4-002 | The caller holds no right for the operation | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The record is outside the caller's scope | This case is not in your scope. |

MSG-P10-004 is copied character for character from RWB-E1-063 section 14; MSG-P6-003 is from the module specification and its wording is shared with the notice stories of this service; MSG-GEN-006, MSG-P4-002 and MSG-P4-003 are from the platform message catalogue. In AC1 the {agent} value is "SCREENING", the {amount} value is 2,310.5000, the {date} value is 2026-12-01 and the {limit} value is 2,000; the same four values fill the notice of the 2026-12-01 alert and no other value is substituted. Thai text for each message follows decision DL10. This story adds no message ID of its own and changes no wording.

### 15. Screens and states

No screen is built in this story. The legacy dashboard is not a P6 deliverable: the Power BI page "Agent monitor v1" has no source without the lake, and the measures are read from the P9 report read by the P9 stories. The one read this story answers is reached through the gateway-bff composite route (DP-19) by a support or audit reader:

| Read | What it shows for this story | State read |
|---|---|---|
| The cost-alert notice through `GET /api/recovery/comms/v1/notices/{noticeId}` | The message text, the two recipient roles, the alert reference, the template version, the send time and the dispatch attempts | GENERATED with `sent_at` empty while the retry waits; SENT when a send succeeded; HELD with its hold reason |
| The agent monitor screen SCR-46 | Not built here; it comes in RWB-E2-031 and reads the P9 and P10 contracts | None in this story |

The composite route, its field list, its masking rules and its timeout budget belong to RWB-PLT-N001-CON; this story fixes only the answer the route reads. The loaded and stale states of the legacy report are the P9 read model's and are not built or stored here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-063-08 | Access, BR9 | Component | RW-CASEOWN without the right for the cost-alert notice calls `GET /notices/{noticeId}`; refused with 403 and MSG-P4-002 and no field returned |
| TC-E1-063-01 | AC1, BR3, BR4, BR9 | End to end | "SCREENING" cost 2,310.5000 baht against cap 2,000 on 2026-12-01; one notice with the exact MSG-P10-004 text to RW-COE and RW-RISK, readable through `GET /notices/{noticeId}`; one `NoticeGenerated` and one `NoticeDispatched` |
| TC-E1-063-02 | AC2 | End to end | "INTAKE" cost 1,840.0000 baht on 2026-12-01; no `COST_CAP` alert and no notice and no message |
| TC-E1-063-03 | AC3, BR1, BR13 | End to end | "INTAKE" cost 2,000.0000 baht on 2026-12-02, equal to the cap; no alert and no notice and no message |
| TC-E1-063-04 | AC5, BR2 | End to end | The "SCREENING" alert of 2026-12-01 announced again and the daily step rerun for the date; one notice and one message |
| TC-E1-063-05 | AC4 | End to end | "EXTRACT" with an approved policy and no runs on 2026-12-01; runs 0 and cost 0.0000 and no notice and no message |
| TC-E1-063-06 | AC6, BR5 | End to end | The ACE notification path unavailable at 01:40; the notice kept with `sent_at` empty and dispatch attempts 0; one send after the JOB-11 outbox retry (R-UNI-33, R-UNI-35) |
| TC-E1-063-07 | AC7, BR9 | NFR | The notice, the two events and the log lines of 2026-12-01 scanned for national ID number, phone number, name and account number patterns |

The eight cases are the legacy cases of this key, kept with their legacy identifiers in the order of the work package, with their covers and data unchanged apart from what the split moves. The legacy `System` level becomes `End to end` and the legacy `Access` level becomes `Component`, per Template and Rules section R7.2; TC-E1-063-07 is the personal-data scan and is `NFR`. TC-E1-063-08 carries the legacy access test from the agent workspace page to the cost-alert notice read, which is the only read this story owns, and TC-E1-063-01 to TC-E1-063-07 carry the legacy alert and no-alert cases onto the notice. The lake cases of the legacy story, TC-E1-063-01's dashboard figures, TC-E1-063-03's count mismatch and TC-E1-063-04's lake rows, are owned by RWB-P10-E1063-APP, RWB-ITG-E1063-ITG and the P9 measure read, and are proved there. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the template code, the channel, the alert role, the cap, the agent codes, the business dates and the amounts are parameter rows, reference rows or contract answers read at run time (BR8).
- No personal data in events, logs, workflow inputs or tests: the notice, the two events and the log hold the agent code, the business date and amounts only, and no national ID number, phone number, name or account number appears in any of them (BR9, AC7).
- ACE data only through the owner's contract: the alert facts come from P10 rwb-agent and the parameter and reference rows from P3 rwb-case; this service reads no ACE view, holds no foreign key into another schema and reads no `rwb_agent` table (DP-01, DP-11).
- No data lake and no dashboard copy: no `agent_run_daily` table, no lake schema, no INT-19 or INT-20 connection, no reporting file and no measure recomputed or stored in `rwb_comms` (DP-17, BR7).
- The alert stays P10's: no `agent_alert`, `agent_policy` or `agent_run` column is written here, and the strict greater-than comparison of cost with the cap is not repeated (BR13).
- The send is delivered once: it is keyed on the alert reference, goes to the holders of RW-COE and RW-RISK only, and a redelivery, a rerun or a retry adds no second notice and no second message (BR2, BR5, R-UNI-40).
- One hop and a 2 s client budget on every consumed call, with a breaker and a single GET retry; a POST is retried only with the same `Idempotency-Key` (DP-11, ADR-020).
- The notice row and the outbox rows commit together or not at all, so a failed write means no notice and no message.
- No production data, no production copy and no production connection in any test, fixture or stub: the alert facts are synthetic or legacy fixture values.
- No screen is built here and no route is declared here: the one read is served for gateway-bff (DP-19).

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-009 | The daily agent figures are available for reporting with the row counts matched against the source; in the target the reporting is the P9 read model built from `rwb.agent.AgentRunCompleted.v1`, and the notification of a cost breach is what remains in P6 | `GET /api/recovery/agent/v1/admin/agent-metrics`, `rwb.comms.NoticeGenerated.v1`, `rwb.comms.NoticeDispatched.v1` and the proposed `rwb.agent.AgentAlertRaised.v1` | TC-E1-063-01, TC-E1-063-02, TC-E1-063-03, TC-E1-063-04, TC-E1-063-05, TC-E1-063-06 |
| RWB-E1-063 | The legacy key whose cost-alert notification this story owns; its lake copy, its count check and its dashboard read are owned elsewhere | The seven new criteria of section 7 and the legacy values they carry | TC-E1-063-01 to TC-E1-063-07 |
| DP-01 | Owner's schema per service; no cross-service table read | `notice`, `template` and `merge_field` in `rwb_comms` and the not-owned list of 12.7 | TC-E1-063-01, TC-E1-063-04 |
| DP-06 | Parameters contract of rwb-case and the client library | The template code and the channel read as parameter rows | TC-E1-063-01 |
| DP-07 | Reference-data contract of rwb-case | LOV-CHANNEL and the notice-type list read as data | TC-E1-063-01, TC-E1-063-03 |
| DP-09 | Outbox, inbox and CloudEvents | The two published events, the inbox dedupe of the consumed alert event and the JOB-11 retry | TC-E1-063-01, TC-E1-063-04, TC-E1-063-06 |
| DP-10 | Quartz jobs become the workflow kit, and Arch v5 slide 44 sets the mechanism per job | The alert arrives as an event and the retry is the JOB-11 outbox relay; no Quartz table and no Temporal Schedule | TC-E1-063-06 |
| DP-11 | One hop and a 2 s timeout | The three consumed rows of 12.2 and the four fakes of 12.8 | TC-E1-063-01 to TC-E1-063-06 |
| DP-13 | `/api/recovery/<short>/v1` | `/api/recovery/comms/v1` for both provided operations | Every test case |
| DP-15 | Per-service Flyway and migration ownership | `V1063_1__agent_cost_alert_notice.sql` in `rwb_comms` | TC-E1-063-04 |
| DP-17 | Data lake, INT-19 and INT-20 removed; reporting from events into rwb-reporting | The absence of a lake row, a dashboard copy and a recomputed measure; GAP-1210 and ASM-2168 | TC-E1-063-01, TC-E1-063-07 |
| DP-19 | Screen route through gateway-bff | The notice read served for the composite route of section 15 | TC-E1-063-08 |
| ASM-2164 | The alert is not case-bound, so the send uses the published message operation with the alert reference in the path position of the case identifier | API-P6-008 and the notice read | TC-E1-063-01, TC-E1-063-06 |
| ASM-2165 | The alert is announced by a proposed event named `rwb.agent.AgentAlertRaised.v1`, and the facts are read back through the P10 contract | 12.4 and `GET /api/recovery/agent/v1/admin/agent-metrics` | TC-E1-063-01, TC-E1-063-04 |
| ASM-2166 | The six platform contracts and the two P3 contracts of the DP table are the service template baseline and do not block the Day-1 start | 13 pattern application and 12.8 | Every test case |
| ASM-2167 | The template code, the channel, the template body and the retry window are configuration, and the guard right of the read is declared at gateway-bff | 13 configuration and 12.1 | TC-E1-063-01, TC-E1-063-08 |
| ASM-2168 | No lake, no dashboard copy and no Power BI page in P6; the measures stay P9's and the alert stays P10's | DP-17 and section 15 | TC-E1-063-01, TC-E1-063-07 |
| GAP-1209 | The template code, the channel, the notice type, the field names, the retry window and the guard right are not named for the target | The placeholders of sections 3, 11, 12 and 13 | Every test case |
| GAP-1211 | The alert event name, the alert operation name and the non-case binding are not named for the target | 12.1 and 12.4 | TC-E1-063-01, TC-E1-063-06 |

### 19. Out of scope

- The application, contract and operations stories of the agent side of this key: RWB-P10-E1063-APP, RWB-P10-E1063-CON and RWB-P10-E1063-OPS, which own `agent_run`, `agent_policy`, `agent_alert`, `agent_evaluation`, the daily step, the cap, the alert role and the alert row.
- The alert facts themselves and the strict greater-than comparison of cost with the cap: P10 raises the alert and this story notifies it.
- The access session and the rights that prove a role holds or holds not a right: RWB-P4-E1063-APP, and the refusal itself at gateway-bff.
- The measures, the daily read model and the dashboard read: the P9 rwb-reporting build and `GET /api/recovery/reporting/v1/reports/measures`, which is P9's and not this story's.
- The end-to-end proof across P1, P2, P4, P6, P9 and P10, the count check between the reporting read and the P10 source, the JOB-15 trigger, the rerun through P1 and the absence proof of the lake: RWB-ITG-E1063-ITG.
- The Power BI page "Agent monitor v1", the Workbench reporting workspace, its stale banner and the SCR-46 agent monitor screen (RWB-E2-031), and the steering dashboard of Epic 2.
- Acceptance and override per segment, drift alerts and drift detection (FEAT-AGT-13, Epic 3).
- The template authoring, approval and withdrawal and the merge field catalog of this service: RWB-P6-E1046-APP.
- The WIN letter loop, the `NoticeDispatchWorkflow` and the proof-of-delivery capture: RWB-P6-E2021-APP and RWB-P6-E1055-APP.
- SMS and LINE dispatch of a case message to a customer party, with the conduct check and the contact stop: RWB-P6-E2022-APP; the cost alert goes to role holders and not to a customer.
- The contract, database, infrastructure and operations stories of the legacy key.

# RWB-P4-E1063-APP Agent monitoring dashboard v1 [E2c]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: secondary slice of RWB-E1-063 for `rwb-access` — the session and Reporting-read answer that opens the agent monitor, the refusal with MSG-P4-002 and its record, one access entry for every read of the dashboard, the agent-monitor object on the access log, the composite route that merges the answer with the metric rows of `rwb-agent`, and the Platform administration update right that guards the manual start of the daily rollup. The measures, the held-date status, the cost alert and the daily step are the `rwb-agent` slice's (RWB-P10-E1063-APP and RWB-P10-E1063-CON), the notice is `rwb-comms`'s (RWB-P6-E1063-APP), the journey is RWB-ITG-E1063-ITG, and the data-lake copy of the legacy story is removed (DP-17). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P4-E1063-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-E1063-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-063 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | L-P4-Z |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P10-E1063-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-DRI-009) |
| Status | Draft (realignment v1) |

### 1. Story

As a **risk and model risk officer (RW-RISK)**, I want **the `rwb-access` half of the agent monitoring dashboard — the session answer that carries the Reporting read which opens the dashboard, the refusal with MSG-P4-002 and its own access entry when a role holds no such read, one access entry per read of the dashboard, the agent-monitor object on `GET /admin/access-log`, the route that merges the answer with the metric rows of `rwb-agent`, and the Platform administration update right that guards a manual start of the daily rollup**, so that **only a role that holds the right watches an agent, every look at its runs, fallback and cost is recorded and reviewable where the lake copy used to be recorded, and a spend or a fallback that is seen in the first week is a recorded fact and not a private glance**.

- **Service facts.** REST base `/api/recovery/access/v1` (DP-13), schema `rwb_access`, topic `rwb.access.events.v1` (this slice declares no event of its own), task queue `rwb-access` (no workflow is started here), Java package `th.co.scb.ace.workbench.recovery.access`.
- **The boundary.** RWB-P10-E1063-APP owns the measures (runs, answered, fallback rate, latency p50 and p95, tokens, cost, evaluation score), the held-date status, the Schedule `AgentRunDailyRollup`, the cost alerts and the reporting feed. This story builds none of them and reads the two agent operations through the published contract and its fake.
- **What this story owns.** Who may open the dashboard (legacy section 10: RW-RISK and RW-COE hold Reporting R; RW-BIANAL holds Reporting CRUD), the refusal and its record (legacy X6 with MSG-P4-002), one access entry per read, the agent-monitor object on the access log, the route that composes the screen, and the Platform administration U right of a manual start (legacy sections 10 and 12).
- **The lake that is gone.** The legacy story copied the daily figures to a lake table and matched the copy by row count, because the dashboard read the copy and never the live tables (legacy BR1). DP-17 removes the lake, INT-19, INT-20 and the Power BI feed; the dashboard is the aggregate `rwb-agent` serves, and the record of a read is an access entry in this service instead of a row of a lake copy — **Not specified in the source documents (GAP-2333; ASM-3875)**.
- **The right this slice keeps.** The legacy names Reporting R; the metric read of `rwb-agent` keeps Rules and parameters R at its own owner (RWB-P10-E1063-CON). The route checks Reporting R before it asks for a metric row, and the two answers are not merged into one right — **Not specified in the source documents (GAP-2333; ASM-3876)**.
- **The entry, the read and the route.** An entry carries the screen, the event code, the agent codes, the business date or range, the caller reference, the outcome and the time, and no metric value, agent output, prompt or personal field (legacy section 17); the codes, the field list and the page bounds are **Not specified in the source documents (GAP-2332; ASM-3875)**. `GET /api/recovery/access/v1/admin/access-log` (API-P4-008, Platform administration R) answers them paged with the total of the period. The screen is served by the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON), the answer and the metric rows in parallel, one hop each, inside the 2 s budget of slide 10; one Flyway step in the service's own sequence (DP-15) adds the read index and seeds the event code, and adds no table.

### 2. Business rationale

An agent in shadow that times out on one case in five, or that spends twice its budget, must be seen in the first week and not at the first-line review. In the monolith one module kept the runs, the policy, the alert and the copy the Power BI page read, so "what did the agent do" and "who was allowed to look" were one query in one schema. The target puts the measures with the agent owner and the answer to "may this person see an agent's figures" here, with the roles, the letters, the scope and the access log.

Keeping the two apart is what makes the dashboard reviewable. `rwb-agent` computes acceptance, fallback and cost and knows nothing of roles; this service knows the roles and holds no measure. A reviewer with Platform administration R reads the access log and sees which analyst opened which agent, for which date and when; a person with the measures but no access-log right cannot see who else looked. The split also gives the removal of the lake a replacement: the copy that was once the record is now an append-only access entry, written in the transaction window of the read it describes. The slice keeps the PDPA boundary of the screen (legacy section 17; FSD P4 REQ-ACA-005) and treats a wrong right as a recordable event, the pattern FSD P4 fixes for a refused action (AC-EXC-P4-001-05).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| The `rwb-access` service baseline | Schema `rwb_access`, one login, the base `/api/recovery/access/v1` and the two operations of section 12.1 published by RWB-P4-E1022-CON and RWB-P4-E1039-CON. This story adds the filter and the object of the log read and opens no path |
| RWB-P4-E1022-APP | The session: sign-in through ACE Common, the short-lived JWT and the roles and letters the answer carries |
| RWB-P4-E1037-APP and its rows | `role`, `permission` and `masking_rule` in force, so an area, a letter and a scope are rows of the version in force and no role code is written in code |
| RWB-P4-E1039-APP | The access-entry writer and the log read: the entry is appended through the same writer, and this story supplies the event code, the object and the filter |
| RWB-P10-E1063-CON and its fake | The metric read with its element and held-date status, and the run read `GET /api/recovery/agent/v1/admin/agent-runs` for the drill-down |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` that carries the entry (DP-09). Not in the Work Package H list (GAP-2333) |
| RWB-PLT-E1042-CON and RWB-P3-E1042-CON | The parameters client library and the parameters contract of `rwb-case` (DP-06): the event codes, the page bounds and the 2 s budget. Neither is in the Work Package lists (GAP-2333) |
| RWB-PLT-E1043-CON and RWB-P3-E1043-CON | The reference-data client library and the contract of `rwb-case` (DP-07): LOV-CAPABILITY with its `REPORTING` value and the access-event list in force. Neither is in the Work Package lists (GAP-2333) |
| RWB-PLT-TE006-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON | The outbox library (DP-09), the per-service Flyway sequence (DP-15) and the gateway-bff route (DP-19). None is in the Work Package H list (GAP-2333) |
| The roles and their letters | RW-RISK and RW-COE hold Reporting R, RW-BIANAL holds Reporting CRUD and RW-PLATADM holds Platform administration CRUD, so it holds U (legacy section 10; TSD P4 T6.1). A role with no Reporting letter does not open the screen |
| The closed values | The event code of a read and of a refusal, the entry field list, the page bounds, the read-index name and the Flyway step are **Not specified in the source documents (GAP-2332; ASM-3875)** |
| The release date | 30 November 2026, tentative and copied unchanged |

### 4. Flow

1. RW-RISK selects the agent monitor from the menu; the browser calls the gateway-bff route of the screen.
2. The route asks this service for the session answer and `rwb-agent` for the metric rows of the filter in force — two calls in parallel, one hop each, 2 s timeout and a breaker per downstream (DP-11; slide 10).
3. `SessionAuthoriseService` reads the caller's roles from the session, resolves their Reporting letters from the `permission` rows of the version in force, applies the scope and answers allowed with the area, the right `R`, the scope and the masking version.
4. On an allowed answer the route merges the answer with the metric rows and the screen renders one row per agent, policy version, prompt version, model version and business date; the figures are the agent owner's and this story adds none.
5. `DashboardAccessRecorder` appends one entry per read — the open of the screen, a drill-down to the runs, an open of the alert detail — through the library, in the transaction window of the read, holding the screen, the event code, the agent codes, the business date, the caller reference, the outcome and the time, and writes its outbox row in the same transaction (DP-09).
6. A refusal answers 403 with MSG-P4-002 before any metric row is asked and writes one entry with the area, the right and the result `REFUSED`.
7. A held business date answers its held status and the previous published date; the screen shows that date with the banner of MSG-P1-001, which the agent owner sends, and the read is still one entry.
8. A reviewer with Platform administration R opens the access log of SCR-43 Roles and access, filters by the access-event code, a caller and a date range, and reads the entries in time order with the total of the period.
9. A caller with Platform administration U asks for a manual start of the rollup for a business date; the session answer carries that right, the start itself is the agent owner's, and a caller without U is refused with one entry.
10. If the entry or the refusal cannot be appended, the read is withheld: the route answers 503 with MSG-P7-003 and no metric row reaches the screen, because a read that cannot be recorded is not served.

### 5. Exception paths

| Exception | Answer | What is left unchanged |
|---|---|---|
| No session or no Workbench role | 401 with MSG-P4-001 | Nothing is read, nothing is written |
| A caller whose roles hold no Reporting read | 403 with MSG-P4-002 naming the action, before any metric row is asked | No entry of a read; one refusal entry |
| A caller who asks a manual start without Platform administration U | 403 with MSG-P4-002 | The rollup is not started and one refusal entry is written |
| A date filter absent, or `from` after `to` | 422 with MSG-GEN-001 or MSG-GEN-003 | No page is answered |
| A page bound outside the declared range | 422 with MSG-GEN-001 | No page is answered |
| An event code not in the list in force | 422 with MSG-GEN-001; the filter offers only list values | The list in force is untouched |
| The parameters or the lists read is unavailable | 503; no filter value and no event code comes from code | Fail closed: no read is served |
| The decision-record append fails | 503 with MSG-P7-003 and no metric row answered (ASM-3880) | The read is not served and is not recorded |
| The metric read of `rwb-agent` times out | 503 for that part of the composite; the answer alone is not shown as if the screen were open | The breaker per downstream trips and no entry of a partial read is written |
| A break-glass grant is active for the caller | The read is allowed and the entry carries the grant reference; the MSG-P4-004 banner shows | The grant itself is RWB-P4-E1039-APP's |

### 6. INVEST check

| Letter | Finding |
|---|---|
| Independent | Builds against the published `rwb-agent` contract and its fake, the parameters and reference-data fakes and the two operations of its own service; waits for no in-lane story (H is None) |
| Negotiable | The event code, the entry field list, the page bounds and the index name are contract values and data rows, not code |
| Valuable | REQ-DRI-009, FEAT-AGT-06, REQ-ACA-006 and REQ-ACA-010: the dashboard opens only for the right role, every read is recorded and the record is reviewable |
| Estimable | One session answer, one entry writer, one filter on an existing read, one route step and one migration step |
| Small | No workflow, no Schedule, no new table, no screen of its own, one package |
| Testable | Each criterion is a Component, Contract or End-to-end check on fixed roles, one agent and three business dates |

### 7. Acceptance criteria

```gherkin
Feature: Agent monitoring dashboard v1 [E2c]

  Background:
    Given the rwb-agent contract mock returns the metric rows of agents "INTAKE" and "SCREENING" for the business dates 2026-11-30 and 2026-12-01
    Given the permission rows in force give RW-RISK the Reporting letter R, RW-COE the letters R and RW-BIANAL the letters CRUD
    Given the permission rows in force give RW-PLATADM the Platform administration letters CRUD and RW-CASEOWN no Reporting letter

  Scenario: AC1 The Reporting read opens the dashboard (new, D-RCV-60)
    Given the rwb-agent contract mock returns one AgentMetric row for agent "INTAKE" for 2026-12-01
    And a caller holding RW-RISK, whose Reporting letter is R
    When the route asks GET /api/recovery/access/v1/me/session for that caller
    Then the answer allows the read with area "REPORTING", right "R", the scope in force and the masking version
    Then the route merges the answer with the metric rows of rwb-agent, one hop each

  Scenario: AC2 A role without the read is refused and the refusal is recorded (new, D-RCV-60)
    Given the rwb-agent contract mock returns the metric rows of the dashboard
    And a caller holding only RW-CASEOWN, whose Reporting letter is the dash
    When it opens the agent monitor
    Then the route answers 403 with MSG-P4-002 naming the action "open the agent monitor"
    Then no metric row is asked of rwb-agent
    Then one access entry is written with area "REPORTING", right "R" and result "REFUSED"

  Scenario: AC3 One access entry per read of the dashboard (new, D-RCV-60)
    Given the caller of AC1 has opened the dashboard for agent "INTAKE" on 2026-12-01
    When it then drills down to the runs of "INTAKE" for 2026-12-01
    Then two access entries are appended, one for the open of the screen and one for the drill-down
    Then each entry holds the screen, the event code, the agent code, the business date, the caller reference, the outcome and the time
    Then no entry holds a metric value, an agent output, a prompt text or a personal field

  Scenario: AC4 The access log answers the dashboard reads (new, D-RCV-60)
    Given three access entries of the agent monitor for "INTAKE" and one for "SCREENING" on 2026-12-01
    When a caller holding RW-AUDIT reads GET /api/recovery/access/v1/admin/access-log with the access-event code, caller "U-3001" and the date range 2026-12-01 to 2026-12-01
    Then the answer is one page holding the entries of that caller in time order and the total that equals them
    Then a from date after the to date is refused with 422 and MSG-GEN-003

  Scenario: AC5 A held date is shown as held and the read is still recorded (new, D-RCV-60)
    Given the rwb-agent contract mock answers the held status of 2026-12-01 with 2026-11-30 as the previous published date
    When the caller of AC1 opens the dashboard for 2026-12-01
    Then the screen shows 2026-11-30 and the banner of MSG-P1-001
    Then exactly one access entry is appended for that read and it carries 2026-12-01 as the date asked

  Scenario: AC6 The manual start needs the Platform administration update right (new, D-RCV-60)
    Given a caller holding RW-PLATADM, whose Platform administration letters are CRUD
    When it asks for a manual start of the daily rollup for 2026-12-01
    Then the session answer allows the start with area "PLATFORM_ADMINISTRATION" and right "U"
    Then a caller holding only RW-RISK is refused with 403 and MSG-P4-002, and one access entry with result "REFUSED" is written
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The dashboard opens only for a caller whose roles hold Reporting R, with the scope applied, and the letters are rows of the version in force | Legacy section 10; FSD P4 AC-P4-001-01; legacy X6 |
| BR2 | A refusal answers 403 with MSG-P4-002 and writes one entry with the area, the right and the result `REFUSED` | FSD P4 AC-EXC-P4-001-05; legacy X6 |
| BR3 | Every read of the screen wants one access entry, and a read that cannot be recorded is not served | REQ-ACA-006; NFR-042; ASM-3880 |
| BR4 | An entry holds the screen, the event code, the agent codes, the business date or range, the caller reference, the outcome and the time, and no metric value, agent output, prompt or personal field | Legacy section 17; REQ-ACA-005 |
| BR5 | The agent figures reach this service only through the `rwb-agent` contract, and the dashboard reads nothing from a lake, a file or another schema | Legacy BR1; DP-01, DP-17 |
| BR6 | A manual start of the daily rollup needs Platform administration U, and a caller without it is refused and recorded | Legacy section 10 and section 12; TSD P4 T6.1 |
| BR7 | An area, a letter, an event code and a page bound are data rows or parameters and never constants in code | FSD P4 VR-P4-004-1; DP-06, DP-07 |
| BR8 | An agent runs under a service identity and is subject to the same role rows as a person | REQ-ACA-010; TSD P4 T6.2 |
| BR9 | The access entries of the screen are append only and are read back through the access log of this service | FSD P4 A2.8; REQ-ACA-006 |

### 9. State transitions

None. This story changes no case or workflow state. An access entry is an append and is never edited, deleted or re-sequenced; a failed append leaves nothing written and withholds the read, so the log stays a record of the reads that happened. The rollup states COMPLETE, HELD and FAILED are the agent owner's and are read here as the held status only.

### 10. Authority

| Capability area | Right | Roles | Where used in this story |
|---|---|---|---|
| Reporting | R | RW-RISK, RW-COE (legacy section 10) | the session answer that opens the dashboard |
| Reporting | CRUD | RW-BIANAL (legacy section 10) | the read of the measures the analyst maintains, not performed here |
| Platform administration | R | RW-AUDIT, RW-COE, RW-DATASTEW, RW-COMPLY, RW-PLATADM, RW-SECADM (TSD P4 T6.1) | the access-log read of section 12.1 |
| Platform administration | U | RW-PLATADM (TSD P4 T6.1) | the right that guards a manual start of the rollup |
| the service identity | — | SY-AGENT (TSD P4 T6.1) | subject to the same rows as a person (BR8) |

A caller holding no Reporting letter is refused with MSG-P4-002 before any metric row is asked; the letters are read from the `permission` rows of the version in force and never from a table of another service. RW-DATASTEW receives the count-mismatch notice of the agent owner and needs no read of this screen.

### 11. Data

| Table or view | Schema | Fields (BR Field IDs) | Use |
|---|---|---|---|
| `role` | `rwb_access` | `role_code` DF-REF-034 to `default_scope` DF-REF-038 | Read only: the caller's role codes |
| `permission` | `rwb_access` | the role, area and letter rows of the matrix in force | Read only: the Reporting and Platform administration letters |
| `masking_rule` | `rwb_access` | DF-REF-198 to DF-REF-204 | Read only: the masking version the answer carries |
| the local decision-record table of the library | `rwb_access` | the entry: code, inputs reference, caller, time and the two hashes | Append and read: the access entries of the screen |
| `AgentMetric`, `AgentRun` | consumed, not stored | agent, policy version, prompt version, model version, business date, runs, answered, fallback, the rates, latency p50 and p95, tokens, cost, eval score, held status | Read through RWB-P10-E1063-CON; no copy is stored |
| LOV-CAPABILITY, the access-event list | consumed, not stored | value code and label | Read through the `rwb-case` reference-data contract (DP-07) |

No `agent_run`, `agent_policy`, `agent_alert` or `agent_evaluation` row is read, joined or copied: the agent tables are `rwb_agent`'s and reach this story only as contract fields. No lake table, no lake credential and no extract file exists (DP-17). No personal field is held by any row of this story.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/access/v1`; owner P4 `rwb-access`. Both operations exist in the service baseline; this story adds the agent-monitor object, the access-event filter and the rights of the answer to them and opens no new path.

| Operation | Path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|
| GET | `/api/recovery/access/v1/me/session` (API-P4-012) | No body | The caller's roles, their capability-area letters with the scope, the masking version in force | 401 (MSG-P4-001); 503 | None R — a session is required | Not applicable, read only |
| GET | `/api/recovery/access/v1/admin/access-log` (API-P4-008) | Query `event`, `user`, `from`, `to`, `page`, `size` | `AccessLogPage`: `items[]` with the screen, the event code, the agent codes, the business date, the caller reference, the outcome and the time; `page`, `size`, `total` | 401 (MSG-P4-001); 403 (MSG-P4-002); 422 (MSG-GEN-001, MSG-GEN-003); 503 (MSG-P7-003) | Platform administration R, scope applied | Not applicable, read only |

The access-event code of a dashboard read, the code of a refusal, the page bounds and the exact entry member names are fixed by the next version of the access-log contract of RWB-P4-E1039-CON — **Not specified in the source documents (GAP-2332; ASM-3875)**. The read imposes no 92-day cap; the date range of the measures is the agent owner's.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/agent/v1/admin/agent-metrics` | P10 `rwb-agent`, RWB-P10-E1063-CON | The metric rows the screen shows and the held-date status |
| GET | `/api/recovery/agent/v1/admin/agent-runs` | P10 `rwb-agent`, RWB-P10-E1063-CON (restated from RWB-P10-E1058-CON) | The drill-down of a metric row, recorded as its own read |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 `rwb-case`, RWB-P3-E1042-CON (DP-06) | The access-event codes, the page bounds and the 2 s budget, as parameter rows in force |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 `rwb-case`, RWB-P3-E1043-CON (DP-07) | LOV-CAPABILITY with its `REPORTING` value and the access-event list, at the version in force |

One hop per call, 2 s timeout and a breaker per downstream (DP-11). The two `rwb-agent` reads are built against the contract and its fake from Day 1; the parameters and reference-data reads are behind their client libraries and fakes. `RWB-P3-E1042-CON` and `RWB-P3-E1043-CON` are not in the Work Package C list (GAP-2333).

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | one access entry of the screen: screen, event code, agent codes, business date or range, caller reference, outcome, time and masking version, and the entry of a refusal with its area and right |

CloudEvents 1.0 envelope, from the outbox of the transaction that appends the entry. No `rwb.access.<Event>.v1` message is published, because this slice declares no event of its own and the two access events of the service belong to the mapping, scope, delegation and reference-data stories; the entry rides the shared decision-record topic and is not a policy change (GAP-2333).

#### 12.4 Events consumed

None. The screen is read on request; no topic starts a read of this service and no `processed_event` row is written. The announcement of a cost alert is `rwb-comms`'s to consume (RWB-P6-E1063-APP).

#### 12.5 Workflows and activities

None. The answer and the entry are synchronous inside the request; the queue `rwb-access` is not used by this story and no child workflow is started.

#### 12.6 Schedules

None. The legacy nightly step is the `AgentRunDailyRollup` Schedule that RWB-P10-E1063-OPS registers on queue `rwb-agent`, and a rerun is a manual start of the same workflow identity; this slice owns no Schedule, no job row and no job admin read. JOB-18 Access review list stays with RWB-P4-AD008-APP.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| the local decision-record table of the library | P4, in `rwb_access` | The access entries and the refusal entries of the screen, with the read index on event code, caller and business date |
| `role`, `permission` | P4 (`rwb_access`) | Read only: the caller's roles, letters and scope |
| `masking_rule` | P4 (`rwb_access`) | Read only: the masking version carried on the answer and the entry |
| `outbox_event`, `idempotency_key` | Platform library, in `rwb_access` | The record row of an entry |

No table of another service is named (DP-01): `agent_run`, `agent_policy`, `agent_alert` and `agent_evaluation` are `rwb_agent`'s, the lists and the parameters are `rwb-case`'s, and no lake table exists (DP-17).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| agent-metrics fake | One `AgentMetric` per agent, version and business date for 2026-11-30 and 2026-12-01, the held status with 2026-11-30 as the previous published date, and the drill-down `AgentRun[]` | This story, contract tests, harness |
| parameters fake | The access-event codes, the page bounds and the 2 s budget, and a parameter row that is missing | This story, contract tests |
| reference-data fake | LOV-CAPABILITY holding `REPORTING` and the access-event list, at the version in force, and a value absent from the list | This story, contract tests |
| session fake | The own operation answered for RW-RISK with Reporting R and scope `OWN`, for RW-PLATADM with Platform administration CRUD, and a 401 with MSG-P4-001 | This story, contract tests |
| decision-record fake | The append with its `prev_hash` and `entry_hash`, a forced failure and a reader over the entries of a period | This story, contract tests |
| gateway-bff fake | The route: the answer of this service and the metric rows merged, one hop each | Screen route, harness |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | Session and access log provided; two `rwb-agent` reads, one parameters read and one lists read consumed; one hop, 2 s timeout |
| Kafka | 1 published, 0 consumed | `rwb.decision-record.DecisionRecorded.v1` through the outbox |
| Temporal | 0 | No workflow, no activity, no Schedule |
| File | 0 | No file input and no file answer |

### 13. Solution plan

**Deliverables.** `SessionAuthoriseService` (the roles, the Reporting and Platform administration letters, the scope and the masking version), `DashboardAccessRecorder` (the event code, the entry and the outbox row in one transaction), `AccessLogQuery` (the event, caller and date filters, the order and the paging on API-P4-008), `ParametersClient` and `ListsClient` (DP-06, DP-07), `AgentMetricsClient` (RWB-P10-E1063-CON), the migration of DP-15, the six fakes of section 12.8 and the eight test cases of section 16.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_access`; the agent figures are consumed as contract fields and never read as tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of `rwb-case` and the client library: the access-event codes, the page bounds and the 2 s budget | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON — neither is in the Work Package lists (GAP-2333; ASM-3878) |
| DP-07 | Reference data, LOV | Reference-data contract of `rwb-case` for LOV-CAPABILITY and the access-event list | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON — neither is in the Work Package lists (GAP-2333; ASM-3878) |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library, CloudEvents, the shared decision-record topic | H RWB-PLT-TE006-CON — not in the Work Package H list (GAP-2333; ASM-3879) |
| DP-10 | Quartz, JOB-nn | The legacy nightly step is `rwb-agent`'s `AgentRunDailyRollup` Schedule; here only the Platform administration U right of a manual start | none here; the Schedule and the workflow kit (H RWB-PLT-E1071-CON) stay with RWB-P10-E1063-APP (GAP-2333; ASM-3881) |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout and a breaker per downstream | none (C from the legacy dependency: RWB-P10-E1063-CON) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/access/v1` on both operations and on the consumed paths | none |
| DP-15 | V0001 baseline, migration | One step in the service's own Flyway sequence: the read index on the record table and the seed of the event code | H RWB-PLT-E1044-CON — not in the Work Package H list (GAP-2333; ASM-3879) |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); the read is recorded as an access entry instead of a lake copy, and reporting comes from events into `rwb-reporting` | none; gap raised because the legacy story needs lake data (GAP-2333; ASM-3875) |
| DP-19 | Screen, ace-web | gateway-bff composite route of the screen, the answer and the metric rows in parallel | H RWB-PLT-N001-CON — not in the Work Package H list (GAP-2333; ASM-3879) |

The dependency column records the row the DP table adds. The Work Package H list is empty and the metadata row copies it, so the platform contracts above and the two `rwb-case` C rows are stated here and in section 3 rather than added to the rows (GAP-2333).

**Build steps**

1. `SessionAuthoriseService`: the roles from the session answer, the Reporting and Platform administration letters from the `permission` rows in force, the scope and the masking version (BR1, BR6).
2. The refusal paths: 403 with MSG-P4-002 before any metric row is asked, and one entry with the area, the right and `REFUSED` (BR2, AC2, AC6).
3. `DashboardAccessRecorder`: the event code, the entry fields and the outbox row in the transaction window of the read (BR3, BR4, AC3).
4. The held-date pass-through: the status and the previous published date of the metric answer are shown and the read is recorded once (AC5).
5. `AccessLogQuery` on API-P4-008: the event, caller and date filters, the order, the paging and the two date refusals (AC4).
6. `ParametersClient`, `ListsClient` and the `rwb-agent` client with the 2 s budget and the breaker, and the composite route against the gateway-bff fake (BR7).
7. The migration (read index and event-code seed in the service's own sequence, DP-15), the six fakes and the eight test cases, with the withheld read proved against the forced append failure (ASM-3880).

**Feature switch.** None of its own. The legacy flag `rwb.agent.monitor` is the screen's and belongs to RWB-P10-E1063-APP; with it off no read of the dashboard arrives, so this story's path is idle and writes nothing.

**Done when.** The eight test cases pass, the answer opens the dashboard for RW-RISK, RW-COE and RW-BIANAL and refuses RW-CASEOWN with MSG-P4-002, one entry per read is readable from the access log with the total of the period, a manual start is answered only with Platform administration U, and no entry holds a metric value or a personal field.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A caller whose roles hold no Reporting read, or no Platform administration U for a manual start | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field or a page bound is outside its rule | Enter {field}. |
| MSG-GEN-003 | The `from` date is after the `to` date on the log read | {field} cannot be before {other}. |
| MSG-P7-003 | The access entry or the refusal cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

MSG-P4-002 is the legacy message of RWB-E1-063 and keeps its wording character for character; MSG-P10-004 and MSG-P1-001 stay with the agent and communications slices and are not sent by this story.

### 15. Screens and states

| Screen | State | What the screen consumes |
|---|---|---|
| Agent monitor, menu route | Allowed | The session answer with the area, the right and the scope, and the metric rows of the merged route |
| Agent monitor | Loading | The skeleton rows while the two calls are in flight |
| Agent monitor | Refused | The 403 of the envelope with MSG-P4-002 and no metric row |
| Agent monitor | Held date | The previous published date of the metric answer with the MSG-P1-001 banner over it |
| Agent monitor | Not recorded | The 503 of the envelope with MSG-P7-003 and no row |
| Agent monitor | Error | The message at the top of the screen and the breaker state of the failed downstream |
| Agent monitor | Break-glass | The MSG-P4-004 banner over the screen while a grant is active |
| SCR-43 Roles and access, access-log panel | Dashboard reads | The page of section 12.1 filtered by the access-event code, a caller and a date range |

The screen fields, the figure columns, the held status and the alert detail are the agent owner's; this story renders no screen of its own and supplies the answer, the entries and the log page. The legacy Power BI page "Agent monitor v1" has no target, because the lake it read is removed (DP-17).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-063-01 | Legacy AC1 and BR5; AC1 and AC3 — the per-agent figures are reached through the Reporting answer and the read is recorded | End to end | INTAKE 120 runs, 9 fallback; SCREENING 150 runs, 21 fallback on 2026-12-01 |
| TC-E1-063-02 | Legacy AC2 and BR3, BR6; AC3 — the alert the screen shows is one object of the read entry | End to end | SCREENING cost 2,310.5000 baht, cap 2,000 on 2026-12-01 |
| TC-E1-063-03 | Legacy AC3 and BR2; AC5 — a held date shows 2026-11-30 and the read is recorded once | End to end | The held status with 2026-11-30 as the previous published date |
| TC-E1-063-04 | Legacy AC4 and BR4; AC6 — a manual start passes the Platform administration U answer, and a rerun is one more recorded start | Component | The rollup started for 2026-12-01 by RW-PLATADM, then by RW-RISK |
| TC-E1-063-05 | Legacy AC5; AC1 — a date with no runs still opens and is recorded | Component | EXTRACT with no runs on 2026-12-01 |
| TC-E1-063-06 | Legacy AC6 and BR3; AC1 — a cost equal to the cap is read as a figure and raises nothing at this slice | Contract | INTAKE cost 2,000.0000 baht on 2026-12-02 |
| TC-E1-063-07 | Legacy AC7; AC3 — the read is recorded once while the notice is retried | Component | The notice path down at 01:40 |
| TC-E1-063-08 | Legacy X6 and AC2, AC5 — a role without the Reporting read is refused with MSG-P4-002 and one refusal entry is written | Component | RW-CASEOWN opens the agent monitor |

The eight legacy ids are kept on this slice with the Covers values the legacy story states, remapped to the Level set of the template; the behaviour each one names is proved with the `rwb-agent` slice, and this slice proves the answer, the record and the log of the same read. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. No `-ITG` copy appears here, because the journey is RWB-ITG-E1063-ITG.

### 17. Guardrails

- No business value in code: the area, the letters, the event codes, the page bounds and the index name are data rows, parameter rows or library codes (BR7).
- No personal data in the entry, the event or the log: role codes, agent codes, a business date, a caller reference, an outcome and a time only (BR4, REQ-ACA-005).
- No read of another service's table: the figures come from the `rwb-agent` contract and the lists and parameters from the `rwb-case` contracts (BR5, DP-01).
- No lake table, lake credential, extract file or INT-19 or INT-20 path exists in this story (DP-17).
- The entry is append only: no entry is edited, deleted or re-sequenced, and a failed append withholds the read (BR3).
- One REST base and one topic per service; the two paths sit on `/api/recovery/access/v1` and no `rwb.access.<Event>.v1` message is declared (DP-13).
- Every fixture is synthetic: no production agent row, no customer reference and no personal field is copied into a test or a fake.
- The metric answer is never cached or stored: a row on the screen is a row read under the right of the moment.

### 18. Traceability

| Requirement ID | Requirement (short) | Element in this story | Test cases |
|---|---|---|---|
| REQ-DRI-009 | Copied daily for reporting, with row counts matched | The read of the daily figures is recorded as an access entry and answered back from the access log, so the report of who watched the measures is built from this service's entries and not from a lake copy (BR3, BR9, AC3, AC4) | TC-E1-063-01, TC-E1-063-02, TC-E1-063-03 |

The requirement ID is the legacy story's own section 18 row and is carried unchanged; the access rules of this slice are cited in section 8 from FSD P4 (REQ-ACA-005, REQ-ACA-006, REQ-ACA-010) and are not restated as rows here. The removal of the lake is the DP-17 row of section 13.

### 19. Out of scope

- The measures, the held-date status, the cost alerts, the daily step and its Schedule: RWB-P10-E1063-APP, RWB-P10-E1063-CON and RWB-P10-E1063-OPS.
- The delivery of MSG-P10-004 and the notice read: RWB-P6-E1063-APP.
- Any data-lake copy, Power BI feed, INT-19 and INT-20 (removed, DP-17) and the reporting read model of `rwb-reporting`.
- The sign-in, the role matrix, the scope, the masking profiles and the break-glass grant: RWB-P4-E1022-APP, RWB-P4-E1037-APP, RWB-P4-AD003-APP, RWB-P4-AD006-APP.
- The access-entry writer and the access-log search and export as a journey: RWB-P4-E1039-APP and RWB-P4-AD007-APP. This story extends the object of their read and duplicates neither.
- The central decision ledger and its chain: `rwb-decision` (RWB-P7-E1008-APP); this story appends local entries whose fact is relayed, and reads no ledger.
- The screen build, the field list and the composite route itself: RWB-PLT-N001-CON and the Epic 2 screen work; SCR-46 Agent monitor belongs to RWB-E2-031 and is not changed here.
- The schema migration of other services, the grants, the deployment, the Helm chart, the dashboards and the runbook: the DB, OPS and INF slices of this key outside this Work Package.
- The cross-service journey and its evidence: RWB-ITG-E1063-ITG.

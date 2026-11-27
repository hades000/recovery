# RWB-P4-E2031-APP Agent monitoring dashboard v2 [E3d]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: secondary slice of RWB-E2-031 for `rwb-access` — the authority answer that opens SCR-46 Agent monitor, the agent-monitor object on the access log, one access event per read of the screen, and the gateway-bff composite route that merges the answer with the metric rows of `rwb-agent`. The measures, the segment filter, the drift check and the reconciliation of the same legacy key are the `rwb-agent` slice's (RWB-P10-E2031-APP) and are not restated here. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P4-E2031-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 20 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P4-E2031-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-031 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P4-E2031-APP-16) |
| Patterns applied | DP03, DP07, DP10, DP13, DP15, DP19 |
| Parallel lane | L-P4-AS |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P10-E2031-CON |
| Contract version | rwb-access.yaml info.version 5.0.0 (Recovery Workbench API Specification v5); REST base /api/recovery/access/v1 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (no FR mapped to REQ-DRI-009, REQ-APD-005) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the `rwb-access` half of SCR-46 Agent monitor — the session and authorise answer that opens the screen on Platform administration R, one access event for every read of the screen, the agent-monitor object on the access log so a reviewer can see who watched which agent and when, and the composite route that merges this answer with the metric rows of `rwb-agent`**, so that **only a role that holds the right watches an agent, and every look at its acceptance, override and fallback is recorded and reviewable**.

- **Service facts.** REST base `/api/recovery/access/v1` (DP-13), schema `rwb_access`, topic `rwb.access.events.v1` (this service declares no event of its own), task queue `rwb-access` in namespace `rwb-recovery` (not used — this story starts no workflow), Java package `th.co.scb.ace.workbench.recovery.access`.
- **The boundary.** RWB-P10-E2031-APP owns the measures (acceptance, correction, override, fallback, latency, cost and the feedback count per agent, version, segment and date), the segment filter, the two date refusals, the daily drift check and the month reconciliation. This story builds none of them and reads its two operations through the published contract and its fake.
- **What this story owns.** Who may open SCR-46 (legacy precondition and section 10: Platform administration R), the refusal and its record, one access event per read of the screen, the agent-monitor object on `GET /admin/access-log` so an auditor can answer "who looked at agent INTAKE in December", and the route that composes the screen.
- **The authority answer.** The right comes from the session answer `GET /api/recovery/access/v1/me/session` (API-P4-012) and the authorise gate `POST /api/recovery/access/v1/authorise` (DP-08), both already published. The area is `PLATFORM_ADMINISTRATION` and the right is `R`; the roles that hold it are matrix rows in force and no role code is written in code (DP-07).
- **The conflict this slice resolves.** The legacy story names Platform administration R, and the `rwb-agent` contract names Rules and parameters R for the metric read (TSD P10 API-P10-009). Both are kept as they stand: the screen route checks Platform administration R before it asks for metrics, and the metric read keeps its own right at its owner. The two answers are not merged into one and the disagreement is recorded — **Not specified in the source documents (GAP-2318; ASM-3843)**.
- **The object and the filter.** An entry of this screen carries the object type of the agent monitor, the agent codes on screen, the segment (the product group and the region of the case at run time, legacy BR6) and the date range; it carries no metric value, no agent output and no prompt text (legacy section 17). The object-type code is **Not specified in the source documents (GAP-2316; ASM-3841)**.
- **The access event.** One append per read — an open of the screen, a drill-down to the runs, an open of the override-reason panel — as one entry of the local decision-record chain written through the DP-03 library, under the library's record code — **Not specified in the source documents (GAP-2316; ASM-3842)**.
- **The read.** `GET /api/recovery/access/v1/admin/access-log` (API-P4-008, Platform administration R) answers the agent-monitor object filtered by agent, segment and dates, paged, with a total that equals the events appended for the period.
- **The route and the migration.** SCR-46 is served by the gateway-bff composite route of DP-19 (RWB-PLT-N001-CON), the answer and the metric rows asked in parallel, one hop each, inside the 2 s budget of slide 10; one Flyway step in the service's own sequence (DP-15) adds the read index of the log and seeds the object-type value, and adds no table — **Not specified in the source documents (GAP-2316; ASM-3845)**.

### 2. Business rationale

An agent at L1 acts on a customer's case, so the question an auditor asks is not only "what did the agent do" but "who was allowed to watch it, and who did". The monolith answered both from one schema and one role table. In the target the measures belong to `rwb-agent` and the answer to "may this person see agent measures" belongs here, with the roles, the letters, the scope and the access log, so that a right is granted and withdrawn as data and every read of the screen is a recorded event.

Keeping the two apart is what makes the dashboard reviewable. The agent owner computes acceptance, override and cost and knows nothing of roles; this service knows the roles and holds no measure. A reviewer with Platform administration R reads the access log of the agent monitor and sees which analyst opened which agent, for which segment and which date range, and when — and a person with the measures but no access-log right cannot see who else looked.

The slice also protects the PDPA boundary of the screen — codes, a segment, a date range and a time, never a metric value, an agent output, a prompt or a personal field (legacy section 17, REQ-ACA-005) — and it treats a wrong right as a recordable event: every refusal carries the area, the right and the result, the pattern FSD P4 already fixes for the roles read (AC-ALT-P4-001-01).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| The `rwb-access` service baseline | Schema `rwb_access`, one login, the base `/api/recovery/access/v1`, and the three operations of section 12.1 already published by RWB-P4-E1022-CON, RWB-P4-E1037-CON and RWB-P4-E1039-CON. This story extends their object set and adds no path |
| RWB-P4-E1022-APP | The session: sign-in through ACE Common, the short-lived JWT and the roles the session answer carries |
| RWB-P4-E1037-APP and its rows | `role`, `permission` and `masking_rule` in force, so the letters of a role and the scope are data. The matrix is loaded by RWB-P4-AD002-APP and RWB-P4-E1037-APP |
| RWB-P4-E1039-APP | The access-entry writer and the decision-log linkage: the entry of a read is one append through the same writer, and this story supplies the object, the codes and the filter |
| RWB-P10-E2031-CON and its fake | The metric read and the drill-down: `AgentMetric` with agent, policy version, prompt version, model version, segment, mode, date, runs, the rates, the feedback count, latency p50 and p95, tokens, cost and reconciled; and `AgentRun[]` for a row |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the entry of every read and of every refusal. Not in the Work Package H list — stated in section 13 (GAP-2317) |
| RWB-PLT-E1043-CON and `RWB-P3-E1043-CON` | The reference-data client library and the contract of `rwb-case` (DP-07): LOV-PRODUCT, LOV-CAPABILITY and the object-type list at the version in force. Neither is in the Work Package lists (GAP-2317) |
| RWB-PLT-N001-CON | The gateway-bff composite route of DP-19 that serves SCR-46 and merges the two answers. Not in the Work Package H list (GAP-2317) |
| The roles and their letters | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM and RW-SECADM hold Platform administration R (TSD P4 T6.1); a role with "-" in that area does not open the screen |
| The closed values | The object-type code, the record code of an access event and the read index name are **Not specified in the source documents (GAP-2316; ASM-3841)** |

### 4. Flow

1. RW-COE selects SCR-46 Agent monitor from the Administration menu; the browser calls the gateway-bff route of the screen.
2. The route asks this service for the session and the authorise answer, and asks `rwb-agent` for the metric rows of the filter in force — two calls in parallel, one hop each, 2 s timeout and a breaker per downstream (DP-11).
3. `SessionAuthoriseService` reads the caller's roles from the session, resolves their `PLATFORM_ADMINISTRATION` letters from the `permission` rows of the version in force, applies the scope, and answers allowed with the area, the right `R`, the scope and the masking version.
4. On an allowed answer the route merges the answer with the metric rows and the screen renders: one row per agent, policy version, prompt version, model version, segment and date, with the state of the agent (Shadow, live or paused) as the agent owner answers it.
5. `AgentMonitorAccessEvents` appends one entry per read — the open of the screen, a drill-down to the runs and an open of the override-reason panel — through the DP-03 library, in the transaction window of the read it describes, holding the screen, the object type, the agent codes, the segment, the date range, the caller, the outcome and the time.
6. A refusal writes one refusal event with the area, the right and the result `REFUSED`, and the route answers 403 with MSG-P4-002 before any metric row is asked of `rwb-agent`.
7. A reviewer opens the access log of SCR-43 Roles and access, filters by the agent-monitor object, an agent, a segment and a date range, and reads the events in time order with the total of the period.
8. If the entry or the refusal event cannot be appended, the read is withheld: the route answers 503 with MSG-P7-003 and no metric row reaches the screen, because a read that cannot be recorded is not served (ASM-3844).

Screen states for SCR-46 Agent monitor and SCR-43 Roles and access: no access is Not specified in the source documents (CG-ALL-5349); a read that cannot be recorded or served shows MSG-P7-003 with the 503 of step 8; the loading states of both screens are Not specified in the source documents (DOR-RWB-P4-E2031-APP-10).

### 5. Exception paths

| Exception | Answer | What is left unchanged | Covered by |
|---|---|---|---|
| No session or no Workbench role | 401 with MSG-P4-001 | Nothing is read, nothing is written | AC6 |
| A caller whose roles hold no Platform administration R | 403 with MSG-P4-002 naming the action, before any metric row is asked | No event of a read; one refusal event | AC2 |
| A segment value absent from the list in force | 422 with MSG-GEN-001; no read and no event | The list in force and the screen state are untouched | AC5 |
| A `from` date after the `to` date on the log read | 422 with MSG-GEN-003 | No page is answered | AC4 |
| An agent code that the metric answer does not hold | 404 with MSG-P4-003 for the drill-down | No row, no count and no case number in the answer | AC7 |
| The reference-data read of a list is unavailable | 503; the filter is not offered with a value from code | Fail closed: no list, no filter value | AC8 |
| The decision-record append fails | 503 with MSG-P7-003 and no metric row answered | The read is not served and is not recorded (ASM-3844) | AC9 |
| A break-glass grant is active for the caller | The read is allowed and every event carries the grant reference; the banner MSG-P4-004 shows | The grant itself is RWB-P4-E1039-APP's | AC10 |
| The metric read of `rwb-agent` times out | 503 for that part of the composite; the authority answer is not shown alone as if the screen were open | The breaker per downstream trips and the event of a partial read is not written | AC11 |

### 6. INVEST check

| Letter | Finding | Result |
|---|---|---|
| Independent | Builds against the published `rwb-agent` contract and its fake, the reference-data fake and the session and authorise operations of its own service; waits for no in-lane story (H is None) | Pass |
| Negotiable | The object-type code, the record code, the page bounds and the index name are data and contract values, not code | Pass |
| Valuable | FEAT-ACA-07, FEAT-ACA-16, REQ-ACA-006 and REQ-ACA-010: the agent monitor opens only for the right role and every read is recorded and reviewable | Pass |
| Estimable | One authority answer, one event writer, one filter on an existing read, one route and one migration | Pass |
| Small | No workflow, no Schedule, no new table, no new screen of its own, one package | Pass |
| Testable | Each criterion is a Component, Contract or End-to-end check on fixed roles, agents, a segment and two date ranges | Pass |

### 7. Acceptance criteria

```gherkin
Feature: Agent monitoring dashboard v2 [E3d]

  Background:
    Given the rwb-agent contract mock returns the metric rows of agents "INTAKE" and "SCREENING" for 2026-12-01 to 2026-12-14
    Given the permission rows in force give RW-COE the Platform administration letter R and RW-PHONECOL the dash

  Scenario: AC1 The right that opens the agent monitor (new, D-RCV-60)
    Given the rwb-agent contract mock returns one AgentMetric row for agent "INTAKE", segment "MORTGAGE/BKK" and date 2026-12-01
    And a caller holding RW-COE, whose Platform administration letter is R
    When the SCR-46 route asks the session answer and the authorise gate for the read of the agent monitor for 2026-12-01 to 2026-12-14
    Then the answer allows the read with area "PLATFORM_ADMINISTRATION", right "R" and the scope in force
    Then the route merges the answer with the metric rows of rwb-agent, one hop each
    Then the metric read of rwb-agent is gated separately by a right Not specified in the source documents (GAP-2318), and both gates are recorded in the access-review run of wave 2

  Scenario: AC2 A role without the right is refused and the refusal is recorded (new, D-RCV-60)
    Given the rwb-agent contract mock returns the metric rows of SCR-46
    And a caller holding only RW-PHONECOL, whose Platform administration letter is the dash
    When it opens SCR-46
    Then the route answers 403 with MSG-P4-002 naming the action "open the agent monitor"
    Then no metric row is asked of rwb-agent
    Then one refusal event is written with area "PLATFORM_ADMINISTRATION", right "R" and result "REFUSED"

  Scenario: AC3 One access event per read of the screen (new, D-RCV-60)
    Given the caller of AC1 has opened SCR-46 for agent "INTAKE", segment "MORTGAGE/BKK" and 2026-12-01 to 2026-12-14
    When the metric rows are answered and the caller then opens the override reasons of "INTAKE" for November 2026
    Then two access events are appended to the local decision-record chain, one for the screen read and one for the override panel
    Then each event holds the screen, the object type, the agent codes, the segment, the date range, the outcome and the time
    Then no event holds a metric value, an agent output, a prompt text or a personal field

  Scenario: AC4 The access log answers the agent-monitor reads (new, D-RCV-60)
    Given three access events of SCR-46 for agent "INTAKE" and one for "SCREENING" between 2026-12-01 and 2026-12-14
    When a caller holding RW-AUDIT reads GET /api/recovery/access/v1/admin/access-log with the agent-monitor object, agent "INTAKE" and those dates
    Then the answer is one page holding the three events in time order and the total 3
    Then the page holds no metric value and no personal field
    Then a from date after the to date is refused with 422 and MSG-GEN-003

  Scenario: AC5 The segment filter comes from the lists in force (new, D-RCV-60)
    Given the rwb-case reference-data contract mock returns the product-group list in force holding "MORTGAGE" and the region list in force holding "BKK"
    When the segment filter of the access log and of the screen is built
    Then the filter offers "MORTGAGE" and "BKK" from the lists in force
    Then no product group and no region is a constant in code
    Then a segment value absent from the list in force is refused with 422 and MSG-GEN-001

  Scenario: AC6 A request with no session is refused and nothing is read (new, D-RCV-60)
    Given a request with no session
    When it opens SCR-46 or reads the access log
    Then the answer is 401 with MSG-P4-001
    Then nothing is read and nothing is written

  Scenario: AC7 A drill-down to an agent the metric answer does not hold is refused (new, D-RCV-60)
    Given the rwb-agent contract mock returns the metric rows of agent "INTAKE" for 2026-12-01 to 2026-12-14
    When a caller holding RW-COE drills down to an agent code the metric answer does not hold
    Then the answer is 404 with MSG-P4-003
    Then no row, no count and no case number is in the answer

  Scenario: AC8 The reference-data read is unavailable and the filter fails closed (new, D-RCV-60)
    Given the rwb-case reference-data contract is unavailable
    When the segment filter of the access log and of the screen is built
    Then the answer is 503
    Then no list and no filter value is offered

  Scenario: AC9 A read that cannot be recorded is not served (new, D-RCV-60)
    Given the decision-record append of the access entry fails
    When the caller of AC1 opens SCR-46 for agent "INTAKE"
    Then the answer is 503 with MSG-P7-003
    Then no metric row is answered and the read is not recorded

  Scenario: AC10 A break-glass grant keeps the read allowed and marked (new, D-RCV-60)
    Given a break-glass grant is active for the caller of AC1
    When the caller opens SCR-46
    Then the read is allowed and every event carries the grant reference
    Then the banner MSG-P4-004 is shown

  Scenario: AC11 A timed-out metric read gives no partial authority answer (new, D-RCV-60)
    Given the rwb-agent metric read of SCR-46 times out
    When the caller of AC1 opens SCR-46
    Then the answer is 503 for the metric part of the composite
    Then the authority answer is not shown alone and no partial-read event is written

  Scenario: AC12 A consumed call that fails or does not answer gives no partial authority answer (new, D-RCV-60)
    Given the rwb-agent contract call of SCR-46 fails or returns no answer
    When the caller of AC1 opens SCR-46
    Then the answer is 503 for the metric part of the composite
    Then the authority answer is not shown alone and no partial-read event is written
```

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | SCR-46 opens only for a caller whose roles hold Platform administration R, with the scope applied | Legacy section 3 and 10; TSD P4 T6.1 | AC1; TC-E2-031-01 |
| BR2 | A refusal answers 403 with MSG-P4-002 and writes one refusal event with the area, the right and the result `REFUSED` | FSD A2.1 AC-ALT-P4-001-01; legacy X6 | AC2; TC-E2-031-08 |
| BR3 | Every read of the screen writes one access event, and a read that cannot be recorded is not served | FEAT-ACA-07; REQ-ACA-006; ASM-3844 | AC3, AC9; TC-E2-031-01, TC-E2-031-14 |
| BR4 | The entry holds the screen, the object type, the agent codes, the segment, the date range, the caller, the outcome and the time, and no metric value, agent output, prompt or personal field | Legacy section 17; REQ-ACA-005 | AC3, AC4; TC-E2-031-03 |
| BR5 | A segment is the product group and the region of the case at run time, read as a list value in force and never as a constant | Legacy BR6; FSD BR-P4-005 | AC5, AC8; TC-E2-031-13 |
| BR6 | A role, an area code and a letter are data rows of the version in force, and no role code or letter is written in code | FSD VR-P4-005-1; DP-07 | AC1; TC-E2-031-01 |
| BR7 | No service reads another service's tables: the measures come from the `rwb-agent` contract and the lists from the `rwb-case` contract | DP-01, DP-05 | AC1; TC-E2-031-09 |
| BR8 | An agent runs under a service identity and is subject to the same role rows as a person | REQ-ACA-010 | AC1; TC-E2-031-09 |

### 9. State transitions

None. This story changes no case or workflow state. An access event is an append and an access entry is never edited or deleted (REQ-DRI-002 pattern); a failure appends nothing, so the chain stays a record of reads that happened.

### 10. Authority

| Capability area | Right | Roles | Where used in this story |
|---|---|---|---|
| Platform administration | R | RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM (TSD P4 T6.1) | the session and authorise answer of SCR-46 and the agent-monitor read of the access log |
| Platform administration | C | RW-PLATADM, RW-SECADM | the break-glass grant that a read may carry (RWB-P4-E1039-APP), not performed here |
| Reporting | R | RW-RISK | the reporting copy of the drift figures; RW-RISK holds no Platform administration, so it does not open SCR-46 (legacy section 10) |
| the service identity | — | SY-AGENT | subject to the same rows as a person (BR8) |

A caller holding no right in Platform administration is refused with MSG-P4-002 before any metric row is asked; the letters are read from the `permission` rows of the version in force and never from a table of another service.

### 11. Data

| Table or view | Schema | Fields (BR Field IDs) | Use |
|---|---|---|---|
| `role` | `rwb_access` | `role_code` DF-REF-034 to `default_scope` DF-REF-038 | Read only: the caller's role codes |
| `permission` | `rwb_access` | the role, area and letter rows of the matrix in force | Read only: the Platform administration letters |
| `masking_rule` | `rwb_access` | DF-REF-198 to DF-REF-204 | Read only: the masking version the session answer carries |
| the local decision-record table of the DP-03 library | `rwb_access` | the entry: code, inputs reference, caller, time and the two hashes | Append and read: the access events of the screen |
| `AgentMetric`, `AgentRun` | consumed, not stored | agent, policy version, prompt version, model version, segment, mode, date, runs, the rates, the feedback count, latency p50 and p95, tokens, cost, reconciled | Read through RWB-P10-E2031-CON; no copy is stored |
| LOV-PRODUCT, LOV-CAPABILITY, the object-type list | consumed, not stored | value code and label | Read through the `rwb-case` reference-data contract (DP-07) |

No `agent_run`, `agent_policy`, `agent_alert` or `agent_feedback` row is read, joined or copied: the agent tables are `rwb_agent`'s and reach this story only as contract fields. No personal field is held by any row of this story.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/access/v1`; owner P4 `rwb-access`. All three exist in the service baseline; this story adds the agent-monitor object and the SCR-46 answer to them and opens no new path.

| Operation | Path | Request | Response | Errors | Authorization | Idempotency |
|---|---|---|---|---|---|---|
| GET | `/api/recovery/access/v1/me/session` (API-P4-012) | No body | The caller's roles, their capability-area letters with the scope, and the masking version in force | 401 (MSG-P4-001); 503 | None R — a session is required | Not applicable, read only |
| POST | `/api/recovery/access/v1/authorise` (DP-08) | `area` `PLATFORM_ADMINISTRATION`, `right` `R`, the object reference of the screen read | Allowed with the scope and the masking version, or refused | 401 (MSG-P4-001); 403 (MSG-P4-002); 503 | the session's own rows | Read-only decision; no key |
| GET | `/api/recovery/access/v1/admin/access-log` (API-P4-008) | Query `objectType`, `agent`, `segment`, `from`, `to`, `page`, `size` | `AccessEntryPage`: `items[]` with the screen, the object type, the agent codes, the segment, the date range, the caller, the outcome and the time; `page`, `size`, `total` | 401 (MSG-P4-001); 403 (MSG-P4-002); 422 (MSG-GEN-001, MSG-GEN-003); 503 (MSG-P7-003) | Platform administration R, scope applied | Not applicable, read only |

The `objectType` value of the agent monitor, the field names of the entry and the page bounds are fixed by the access-log contract and its next version — **Not specified in the source documents (GAP-2316; ASM-3841)**. The read imposes no 92-day cap: the cap belongs to the metric read of `rwb-agent`.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/agent/v1/admin/agent-metrics` | P10 `rwb-agent`, RWB-P10-E2031-CON | The metric rows the screen shows and the agent codes the event records |
| GET | `/api/recovery/agent/v1/admin/agent-runs` | P10 `rwb-agent`, RWB-P10-E2031-CON | The drill-down of a metric row, recorded as its own read |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 `rwb-case`, RWB-P3-E1043-CON (DP-07) | LOV-PRODUCT, LOV-CAPABILITY and the object-type list at the version in force |

One hop per call, 2 s timeout and a breaker per downstream (DP-11). The two `rwb-agent` reads are built against the contract and its fake from Day 1 and never against the `rwb-agent` build; the reference-data read is behind the client library and its own fake. `RWB-P3-E1043-CON` is not in the Work Package C list (GAP-2317).

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | PLT library; consumed by P7 | entryId | the entry of one read of SCR-46: screen, object type, agent codes, segment, date range, caller reference, outcome, time and masking version, and the entry of a refusal with its area and right |

CloudEvents 1.0 envelope, from the outbox of the transaction that appends the entry. No `rwb.access.<Event>.v1` message is published, because this service declares no event of its own and the administration events of `rwb-access` belong to RWB-P4-E1037-APP and RWB-P4-E8008-APP.

#### 12.4 Events consumed

None. The screen is read on request; no topic starts a read of this service and no `processed_event` row is written.

#### 12.5 Workflows and activities

None. The authorise answer and the entry are synchronous inside the request; the queue `rwb-access` is not used by this story and no child workflow is started.

#### 12.6 Schedules

None. The legacy nightly step is the `agentDrift` activity of the `AgentRunDailyRollup` Schedule that RWB-P10-E2031-APP registers on queue `rwb-agent`; this slice owns no Schedule and no job row. JOB-18 Access review list stays with RWB-P4-AD008-APP.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| the local decision-record table of the DP-03 library | P4, in `rwb_access` | The access entries and the refusal entries of the screen, with the read index on object type, agent code and business date (index name: Not specified in the source documents (GAP-2316)) |
| `role`, `permission` | P4 (rwb_access) | Read only: the caller's roles, letters and scope |
| `masking_rule` | P4 (rwb_access) | Read only: the masking version carried on the answer and the entry |
| `idempotency_key`, `outbox_event` | Platform library, in `rwb_access` | The record row of an entry |

No table of another service is named (DP-01): `agent_run`, `agent_policy`, `agent_alert` and `agent_feedback` are `rwb_agent`'s, the lists are `rwb-case`'s, and `case` and `decision_log_entry` are never read.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| agent-metrics fake (rwb-agent) | One `AgentMetric` per agent, version, segment and date for 2026-12-01 to 2026-12-14, and the drill-down `AgentRun[]` | This story, contract tests, harness |
| reference-data fake | LOV-PRODUCT holding "MORTGAGE", the region list holding "BKK", LOV-CAPABILITY with its values and the object-type list, at the version in force | This story, contract tests |
| authorise fake | Allowed for RW-COE with scope `MORTGAGE/BKK`, refused for RW-PHONECOL with MSG-P4-002 | This story, contract tests |
| decision-record fake | The append with its `prev_hash` and `entry_hash`, a forced failure and a reader over the entries of a period | This story, contract tests |
| gateway-bff fake | The SCR-46 route: the answer of this service and the metric rows merged, one hop each | Screen route, harness |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 3 consumed | Session, authorise and access log provided; two `rwb-agent` reads and one `rwb-case` list consumed; one hop, 2 s timeout |
| Kafka | 1 published, 0 consumed | `rwb.decision.DecisionRecorded.v1` through the DP-03 outbox |
| Temporal | 0 | No workflow, no activity, no Schedule |
| File | 0 | No file input and no file answer |

### 13. Solution plan

**Deliverables.** `SessionAuthoriseService` (the roles, the letters, the scope and the masking version), `AgentMonitorAccessService` (the object, the key and the entry), `AccessEntryAppender` (the DP-03 append and its outbox in one transaction), `AgentMonitorLogQuery` (the filter, the order and the paging on API-P4-008), `ListsClient` (DP-07), `AgentMetricsClient` and `AgentRunsClient` (RWB-P10-E2031-CON), the migration of DP-15, the five fakes of section 12.8 and the eight test cases of section 16.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; one entry per read and per refusal | H RWB-PLT-E1027-CON — not in the Work Package H list (GAP-2317) |
| DP-07 | Reference data, LOV | Reference-data contract of `rwb-case` for LOV-PRODUCT, LOV-CAPABILITY and the object-type list, through the client library | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON — neither is in the Work Package lists (GAP-2317) |
| DP-10 | Quartz, JOB-nn | The legacy nightly step is a Temporal Schedule; it is `rwb-agent`'s `AgentRunDailyRollup`, on queue `rwb-agent` | none here; the Schedule and its workflow kit (H RWB-PLT-E1071-CON) stay with RWB-P10-E2031-APP |
| DP-13 | `/api/recovery/v1` | `/api/recovery/access/v1` on all three operations and on the consumed paths | none |
| DP-15 | V0001 baseline, migration | One step in the service's own Flyway sequence: the read index on the record table and the seed of the object-type value | H RWB-PLT-E1044-CON — not in the Work Package H list (GAP-2317) |
| DP-19 | Screen, ace-web | gateway-bff composite route on SCR-46, the answer and the metric rows in parallel | H RWB-PLT-N001-CON — not in the Work Package H list (GAP-2317) |

The dependency column records the row the DP table adds. The Work Package H list is empty and the metadata row copies it, so the four platform contracts above and the reference-data C are stated here and in section 3 rather than added to the rows (GAP-2317; ASM-3846).

**Build steps**

1. `SessionAuthoriseService`: the roles from the session answer, the letters from the `permission` rows in force, the scope and the masking version (BR1, BR6).
2. The refusal path: 403 with MSG-P4-002 before any metric row is asked, and the refusal entry with the area, the right and `REFUSED` (BR2, AC2).
3. `AgentMonitorAccessService` and `AccessEntryAppender`: the object, the key, the filter values and the entry, appended in the transaction window of the read (BR3, BR4, AC3).
4. `AgentMonitorLogQuery` on API-P4-008: the `objectType` filter, the agent, segment and date filters, the order and the paging (AC4).
5. `ListsClient`: the product-group and region lists in force, the object-type list and the empty-value refusal (BR5, AC5).
6. The two `rwb-agent` clients with the 2 s budget and the breaker, and the composite route against the gateway-bff fake.
7. The migration: the read index and the object-type seed in the service's own sequence (DP-15, ASM-3845).
8. The five fakes and the eight test cases, with the withheld read proved against the forced append failure (ASM-3844).

**Feature switch.** None of its own. The legacy flag `rwb.agent.monitor-v2` is the screen's and belongs to RWB-P10-E2031-APP; with it off no read of the agent monitor arrives, so this story's path is idle and writes nothing.

**Done when.** The eight test cases pass, the answer opens SCR-46 for the six roles of section 10 and refuses RW-PHONECOL and RW-CASEOWN with MSG-P4-002, one entry per read is readable from the access log with the total of the period, and no entry holds a metric value or a personal field.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | A caller whose roles hold no Platform administration R opens the screen or reads the log | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A segment value is not in the list in force, or a page bound is outside its row | Enter {field}. |
| MSG-GEN-003 | The `from` date is after the `to` date on the log read | {field} cannot be before {other}. |
| MSG-P7-003 | The access entry or the refusal entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-003 | A drill-down names an agent the metric answer does not hold | {record} was not found. |
| MSG-P4-004 | A break-glass grant is active for the caller; the banner shows | Not specified in the source documents (DOR-RWB-P4-E2031-APP-9) |

The texts are copied unchanged from the legacy story RWB-E2-031 and from the FSD P4 message set; MSG-P10-006 stays with the drift check of RWB-P10-E2031-APP and is not sent by this story.

### 15. Screens and states

| Screen | State | What the screen consumes |
|---|---|---|
| SCR-46 Agent monitor, Administration menu | Allowed | The session answer with the area, the right and the scope, and the metric rows of the merged route |
| SCR-46 Agent monitor | Loading | The skeleton rows while the two calls are in flight |
| SCR-46 Agent monitor | Refused | The 403 of the envelope with MSG-P4-002 and no metric row |
| SCR-46 Agent monitor | Not recorded | The 503 of the envelope with MSG-P7-003 and no row |
| SCR-46 Agent monitor | No access | Not specified in the source documents (CG-ALL-5349) |
| SCR-46 Agent monitor | Empty | "No agent runs in this period." |
| SCR-46 Agent monitor | Error | The message at the top of the screen; the breaker state of the failed downstream |
| SCR-46 Agent monitor | Break-glass | The MSG-P4-004 banner over the screen while a grant is active |
| SCR-43 Roles and access, access-log panel | Agent-monitor reads | The page of section 12.1 filtered by the agent-monitor object, an agent, a segment and a date range |
| SCR-43 Roles and access, access-log panel | Empty | Not specified in the source documents (CG-ALL-5348) |
| SCR-43 Roles and access, access-log panel | Loading | Not specified in the source documents (CG-ALL-5348) |
| SCR-43 Roles and access, access-log panel | Error | Not specified in the source documents (CG-ALL-5348) |
| SCR-43 Roles and access, access-log panel | No access | Not specified in the source documents (CG-ALL-5348) |

The screen fields, the agent state badges (Shadow, live or paused) and the override-reason panel are the `rwb-agent` slice's; this story renders no screen of its own and supplies the authority answer, the events and the log page.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-031-01 | Legacy AC1 and BR1 to BR3; AC1 and AC3 of this slice — the per-agent row reaches the screen through the authority answer and the read is recorded | End to end | INTAKE, segment MORTGAGE/BKK: 140 feedback entries, 119 accepted |
| TC-E2-031-02 | Legacy AC2 and BR3; AC1 and AC3 — the daily drift read passes the same answer and is recorded | End to end | Acceptance 0.8600 then 0.7500, 20 or more entries in each week |
| TC-E2-031-03 | Legacy AC3 and BR4; AC4 — the month read of the cost is one object of the access log | End to end | November 2026: 3,100 runs, 2,945,000 and 465,000 tokens |
| TC-E2-031-04 | Legacy AC4 and BR3; AC3 — a segment with too little feedback is still a recorded read | End to end | 12 feedback entries in the week to 2026-12-14 |
| TC-E2-031-05 | Legacy AC5; AC4 — the from-after-to refusal of the log read | Component | From 2026-12-14 to 2026-12-01 |
| TC-E2-031-06 | Run by RWB-P10-E2031-APP: legacy AC6, the 92-day cap; this slice proves only the answer of that read | End to end | From 2026-08-01 to 2026-12-14 |
| TC-E2-031-07 | Run by RWB-P10-E2031-APP: legacy AC7 and BR5, the unique alert key; the rerun of the read is recorded once | End to end | The drift step rerun for 2026-12-14 |
| TC-E2-031-08 | Legacy X6 and AC2 — a role without Platform administration R is refused with MSG-P4-002 and the refusal is recorded | Component | RW-CASEOWN opens SCR-46 |
| TC-E2-031-09 | AC1 and AC4; the operations of §12, API-P4-008 (GET /api/recovery/access/v1/admin/access-log) and the SCR-46 route answer | Contract | Agent-monitor object, agent "INTAKE", 2026-12-01 to 2026-12-14 |
| TC-E2-031-10 | §12.7 tables: the read index on object type, agent code and business date; AC3 — the entry is written on the index keys | Component | Three access events of INTAKE and one of SCREENING in the week to 2026-12-14 |
| TC-E2-031-11 | AC6 — a request without a session is refused with MSG-P4-001 and nothing is read | Component | No session on SCR-46 and on the log read |
| TC-E2-031-12 | AC7 — a drill-down to an agent the metric answer does not hold is refused with MSG-P4-003 | Component | Agent code not in the metric answer for 2026-12-01 to 2026-12-14 |
| TC-E2-031-13 | AC8 — the reference-data read is unavailable and the filter fails closed | Component | The rwb-case reference-data contract is unavailable |
| TC-E2-031-14 | AC9 — the access entry cannot be written and the read is not served | End to end | Decision-record append fails on the SCR-46 read of INTAKE |
| TC-E2-031-15 | AC10 — a break-glass grant keeps the read allowed, marked and bannered | End to end | Break-glass grant active for RW-COE |
| TC-E2-031-16 | AC11 — a timed-out metric read gives no partial authority answer and no partial-read event | End to end | The rwb-agent metric read times out |
| TC-E2-031-17 | AC12 — a consumed call that fails or does not answer gives no partial authority answer and no partial-read event | End to end | The rwb-agent metric call fails or returns no answer |

The eight legacy ids are kept on this slice with the Covers values the legacy story states, remapped to the Level set of the template; the behaviour each one names is proved end to end with the `rwb-agent` slice, and this slice proves the authority answer and the record of the same read. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. No `-ITG` copy appears here, because no integration slice is split from this key in this Work Package.

### 17. Guardrails

- No business value in code: the area, the right, the object type, the record code, the page bounds and the index name are data rows or library codes (BR5, BR6).
- No personal data in the entry, the event or the log: role codes, agent codes, a segment, a date range, a caller reference, an outcome and a time only (BR4, REQ-ACA-005).
- No read of another service's table: the measures come from the `rwb-agent` contract and the lists from the `rwb-case` contract (BR7, DP-01, DP-05).
- The entry is append only: no access entry is edited, deleted or re-sequenced, and a failed append withholds the read (BR3).
- One REST base and one topic per service; the three paths sit on `/api/recovery/access/v1` and no `rwb.access.<Event>.v1` message is declared (DP-13).
- Every fixture is synthetic: no production agent row, no customer reference and no personal field is copied into a test or a fake.
- The metric answer is never cached or stored: a row on the screen is a row read under the right of the moment.

### 18. Traceability

| Requirement ID | Feature | L3 process | Requirement (short) | Element in this story | Test cases |
|---|---|---|---|---|---|
| REQ-DRI-009 | Not specified in the source documents (DOR-RWB-P4-E2031-APP-2) | Not specified in the source documents (DOR-RWB-P4-E2031-APP-2) | Copied daily for reporting, with row counts matched | The access events of the agent-monitor reads are the rows the reporting read model counts, and the log read answers a total that equals the appended events of the period (BR3, AC4) | TC-E2-031-01, TC-E2-031-03, TC-E2-031-04 |
| REQ-APD-005 | Not specified in the source documents (DOR-RWB-P4-E2031-APP-2) | Not specified in the source documents (DOR-RWB-P4-E2031-APP-2) | An override needs a coded reason, reported monthly | The override-reason panel is one object of the access log, so the monthly override report can be traced to the reads of the panel (BR4, AC3) | TC-E2-031-01, TC-E2-031-03 |
| REQ-ACA-005 | Not specified in the source documents (DOR-RWB-P4-E2031-APP-2) | Not specified in the source documents (DOR-RWB-P4-E2031-APP-2) | Not specified in the source documents (DOR-RWB-P4-E2031-APP-2) | The entry holds the screen, the object type, the agent codes, the segment, the date range, the caller, the outcome and the time, with no metric value or personal field (BR4, AC3, AC4) | TC-E2-031-01, TC-E2-031-03 |
| REQ-ACA-006 | Not specified in the source documents (DOR-RWB-P4-E2031-APP-2) | Not specified in the source documents (DOR-RWB-P4-E2031-APP-2) | Not specified in the source documents (DOR-RWB-P4-E2031-APP-2) | Every read of the screen writes one access event, and an unrecordable read is not served (BR3, AC3, AC9) | TC-E2-031-01, TC-E2-031-14 |
| REQ-ACA-007 | Not specified in the source documents (DOR-RWB-P4-E2031-APP-2) | Not specified in the source documents (DOR-RWB-P4-E2031-APP-2) | Not specified in the source documents (DOR-RWB-P4-E2031-APP-2) | Not specified in the source documents (DOR-RWB-P4-E2031-APP-2) | Not specified in the source documents (DOR-RWB-P4-E2031-APP-2) |
| REQ-ACA-010 | Not specified in the source documents (DOR-RWB-P4-E2031-APP-2) | Not specified in the source documents (DOR-RWB-P4-E2031-APP-2) | Not specified in the source documents (DOR-RWB-P4-E2031-APP-2) | An agent runs under a service identity and is subject to the same role rows as a person (BR8) | TC-E2-031-09 |

The two requirement IDs are the legacy story's own section 18 rows and are carried unchanged; the access rules of this slice from FSD P4 (REQ-ACA-005, REQ-ACA-006, REQ-ACA-007, REQ-ACA-010) are added as rows above, with their Feature and L3 process not specified in the source documents (DOR-RWB-P4-E2031-APP-2).

### 19. Out of scope

- The measures, the segment filter, the two date refusals, the drift check, the reconciliation and the override-reason figures: RWB-P10-E2031-APP and its contract RWB-P10-E2031-CON.
- The role matrix, the scope, the masking profiles and the sign-in: RWB-P4-E1037-APP, RWB-P4-AD002-APP, RWB-P4-AD003-APP, RWB-P4-E1022-APP.
- The access-entry writer, the break-glass grant and the access-log search and export as a journey: RWB-P4-E1039-APP, RWB-P4-AD006-APP, RWB-P4-AD007-APP. This story extends the object set of their read and duplicates neither.
- The central decision ledger and its chain: rwb-decision (RWB-P7-E1008-APP); this story appends local entries only.
- The reporting read model of the agent measures (rwb-reporting) and any data-lake copy (removed, DP-17).
- The screen build, the field list and the composite route itself: RWB-PLT-N001-CON and the Epic 2 screen work.
- The schema migration of other services, the grants, the deployment, the Helm chart, the dashboards and the runbook: the DB, OPS and INF slices of this key outside this Work Package.
- The cross-service journey harness and its evidence: the wave 2 integration epic.

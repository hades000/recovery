# RWB-P10-E1063-CON Agent monitoring dashboard v1 [E2c]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E1063-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-063 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement (DOR-RWB-P10-E1063-CON-16) |
| Contract version | v1 (path /api/recovery/agent/v1) |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON; H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON; H RWB-PLT-TE006-CON; H RWB-PLT-E1071-CON; H RWB-PLT-E1044-CON; H RWB-PLT-N001-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (no FR mapped to REQ-DRI-009) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-063 for rwb-agent. This is the monitoring contract slice of the legacy key: the metric read and its aggregate shape on `/api/recovery/agent/v1` (DP-13), with the run read and the case agent-outputs read restated against the baseline of RWB-P10-E1058-CON, the report of a held business date, the event contract that feeds the aggregate - `rwb.agent.AgentRunCompleted.v1` (EV-28) on `rwb.agent.events.v1` with its retry and `.dlt` topics (DP-09) - the Schedule contract the dashboard reads (`AgentRunDailyRollup`, DP-10), the rwb-reporting measures read and the four fakes. **DP-17 applies here as everywhere in this key:** there is no data lake, so the contract declares no lake table, no extract and no INT-19 or INT-20 path; the aggregate is served on the read and the feed is the event topic into rwb-reporting. The cost cap and the alert role are named as parameter values of the rwb-case contract and the lists as reference data (DP-06, DP-07). It does not restate the whole rwb-agent contract, whose baseline is RWB-P10-E1058-CON, and it builds no business behaviour. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 20 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the rwb-agent side of the agent monitoring dashboard fixed as a contract on Day 1: the metric read on `/api/recovery/agent/v1/admin/agent-metrics` with its query parameters and its paging, the aggregate shape per agent, version and business date with the runs, the fallback count and the cost, the run read and the case agent-outputs read restated against the baseline, the status of a held business date, the event contract of `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` that feeds the aggregate and the published measures, the `AgentRunDailyRollup` Schedule contract the dashboard reads, the rwb-reporting measures read, and the four contract fakes**, so that **the app story, the deployment story, rwb-reporting, the access and communications slices of this key and every reader of a daily agent figure build against one agreed, testable shape without waiting for the rollup to be complete, and no reader is offered a lake table that no longer exists**.

### 2. Business rationale

The legacy key RWB-E1-063 was written against objects inside the monolith: a Spring Batch step of JOB-15 wrote a data lake table `agent_run_daily`, a Power BI report read that table, an in-process `AgentRunExtractSource` served the rows, and the cost alert called the P6 notification interface of the same deployment (legacy sections 4, 12 and 13). In the target every one of those is a boundary or is gone.

- The data lake and its Power BI feed are removed by Architecture v5 (slide 37; ADR-018; DP-17), so the aggregate is not copied anywhere: rwb-agent serves it on its own read and rwb-reporting builds its published measures from the events on `rwb.agent.events.v1`.
- The batch step and its Quartz entry become the Temporal Schedule `AgentRunDailyRollup` in namespace `rwb-recovery` on the task queue `rwb-agent`, whose run record is the only place a held date or a failed rollup is visible (DP-10).
- The in-process source interface becomes the metric read under `/api/recovery/agent/v1` with one hop and a client budget (DP-11, DP-13; ADR-020).
- The notification interface becomes the rwb-comms contract of the communications slice of this key, and the alert row keeps the retry of the outbox (DP-09).
- The cost cap and the alert role are parameter values of the approved policy row, reached through the rwb-case parameters contract, and the lists through the reference-data contract (DP-06, DP-07).

Contract-first only works if the seam is written down once. The seam here is small and load-bearing: one read whose answer carries a per-agent, per-version, per-day element with the legacy figures, one status for a date that is held, one event payload that feeds a published measure with run facts and no personal data, one Schedule contract that names the workflow identity and the rerun rule, and one fake set that makes the app and the deployment testable on Day 1.

If the shape is agreed and faked on Day 1, four teams move at once. The app story RWB-P10-E1063-APP builds the aggregate, the count check, the alerts and the read against these fakes; RWB-P9-E1063-APP in rwb-reporting builds the measure projection from the event payload declared here; RWB-P6-E1063-APP and RWB-P4-E1063-APP take the notice request and the refusal of this read; and RWB-P10-E1063-OPS registers the Schedule and the consumer group against the same names. Without it, each caller invents its own answer, the fallback count of the dashboard and the published measure drift apart, and a held date is invisible.

This story defines the provided side of the dashboard read and the consumed side of the key, and never restates what another owner holds: the run and configuration reads are baselined in RWB-P10-E1058-CON, the parameters and lists are rwb-case's, the measures are rwb-reporting's, the notice is rwb-comms's and the right is rwb-access's (DP-01).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL), so the REST base, the topic and the event names follow the platform rule and not a local choice (§R4; DP-13, DP-14).
- The CloudEvents 1.0 envelope and the platform error envelope are the platform baseline; this document narrows them where it must and says so.
- The agent runtime baseline contract of RWB-P10-E1058-CON is in force: `GET /admin/agent-runs`, `GET /admin/agent-configs`, the run resource, the error taxonomy and the publication of EV-28 are its elements, and this story reuses them rather than redefining them. Its task queue is `rwb-agent` and its namespace `rwb-recovery` (§R4).
- The outbox and retry library of RWB-PLT-TE006-CON publishes the outbox and inbox envelope, the relay, the retry topic and the `.dlt` rule (DP-09).
- The workflow kit of RWB-PLT-E1071-CON publishes the Schedule registration contract with namespace `rwb-recovery`, the overlap policy and the catch-up window (DP-10).
- The parameter and reference-data contracts of rwb-case are published by RWB-PLT-E1042-CON and RWB-PLT-E1043-CON with their client libraries (DP-06, DP-07).
- The measure shapes of rwb-reporting and the measure named "Agent fallback rate" (FSD P10 Agent runtime v3 A2.6.1) are known, and the rwb-reporting fake is available for the measures read.
- The notification contract of the communications slice of this key, RWB-P6-E1063-APP, is known; its operation is Not specified in the source documents (GAP-0617; ASM-0896).
- The Schedule name `AgentRunDailyRollup` is the name this contract fixes, because no source names it: Not specified in the source documents (GAP-0617; ASM-0895).
- No build dependency: this story is Day 1 by rule (§R5.7) and sits in contract group CG-W1.

### 4. Flow

1. Draft the metric read that replaces the legacy `AgentRunExtractSource`: its method, its path under `/api/recovery/agent/v1`, its query parameters, its paging, its answer element, its status for a held date and its refusals.
2. Fix the aggregate shape per agent, policy version, prompt version, model version and business date: runs, answered, fallback, fallback rate at four decimals, median and 95th percentile latency, tokens, cost and the latest evaluation score, with "no L1 runs" for acceptance and override.
3. Restate the two reads the dashboard uses and that this story does not own: the run read with its query and its rights, and the case agent-outputs read, both as baselined in RWB-P10-E1058-CON.
4. Declare the event contract that feeds the aggregate: EV-28 `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1`, its envelope, its key, its payload members and its registry subject, with the retry and `.dlt` topics, and state that rwb-reporting builds its daily projection from it.
5. Fix the Schedule contract the dashboard reads: the name, the namespace, the task queue, the workflow identity equal to the business date, the 01:30 Asia/Bangkok cadence, the overlap policy, the catch-up window, the rerun rule and the run states the read exposes.
6. Fix the rwb-reporting measures read and the parameter and reference-data reads at the boundary, with one hop and the 2 s budget, and name the values the contract expects.
7. Write the four fakes: rwb-reporting, rwb-case, rwb-comms and the gateway-bff route, each with the answers, the errors and the timings this key's tests need.
8. Publish the nine sub-tables of section 12 and the contract tests, and tag the baseline for the app and the deployment stories.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A member of the aggregate element drifts from this document: a renamed member, a retyped amount, a dropped count | The contract test fails and the merge is blocked | None | AC1, AC2 |
| X2 | A caller asks for a date range or a page the contract does not allow, or omits a required query member | The read refuses with 422 and names the member; nothing is read | MSG-GEN-001 | AC1 |
| X3 | The contract declares a lake table, an extract, a lake credential or an INT-19 or INT-20 path | The review refuses the document, because no data lake exists | None | AC6 |
| X4 | A payload gains a personal field, or fails its registry subject | The data-steward review and the contract test refuse the payload; a produced message that fails is routed to `.dlt` with an alert | None | AC4 |
| X5 | The Schedule name, the workflow identity or the rerun rule in the document drifts from the registration of RWB-P10-E1063-OPS | The contract test between the document and the registration fails and one of the two is corrected; the deployment owns the registration | None | AC5 |
| X6 | A restated operation drifts from the baseline of RWB-P10-E1058-CON | The contract test fails on the baseline and this document is aligned, because the baseline is the owner | None | AC3 |
| X7 | A field-level detail of a consumed operation, of a payload member or of the paging is missing from the source material | The element carries the placeholder, one gap row and one assumption row, and the fake is written to the assumed shape | None | AC1, AC4, AC6 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the workflow kit, the agent runtime baseline contract, the outbox library and the rwb-case contracts as published |
| Negotiable | Field-level detail of the consumed operations and the page size are settled with their owners; the read shape, the aggregate element, the event payload, the Schedule contract and the boundary mapping are fixed by this realignment |
| Valuable | Unblocks the app, reporting, access, communications and deployment stories of this key on Day 1 and gives every reader of a daily agent figure one shape |
| Estimable | One provided read, three restated reads, one event, one Schedule contract, three consumed boundaries and four fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact - the schema file, the payload, the fake, the document - and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Agent monitoring contract slice for rwb-agent

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the agent runtime baseline contract of RWB-P10-E1058-CON is in force
    Given the workflow kit of RWB-PLT-E1071-CON and the outbox library of RWB-PLT-TE006-CON are in force

  Scenario: AC1 The metric read is contracted on the agent base (new, D-RCV-60)
    Given the contract file of this story and a running rwb-agent on the base /api/recovery/agent/v1
    When the dashboard asks for the measures of 2026-12-01 with agent "INTAKE" and "SCREENING", segment, version, from and to
    Then one operation answers on GET /api/recovery/agent/v1/admin/agent-metrics with 200 and an AgentMetric[] in the member names and types of this document
    Then the query takes agent, segment, version, from and to, the paging is declared with its page size and its cursor, and a request outside the declared range or paging is refused with 422 and MSG-GEN-001
    Then the refusals are 401 without a session, 403 without the Rules and parameters right with MSG-P4-002, and 503 when the store or a consumed contract is unavailable
    Then the read is one hop under the base /api/recovery/agent/v1 with the 2 s client budget of DP-11, and the paging default and maximum are Not specified in the source documents (GAP-0617; ASM-0893)
    Then the rwb-case and rwb-reporting fakes answer the read and a drift between a fake and this document fails the contract test

  Scenario: AC2 The aggregate shape is one element per agent, version and day (new, D-RCV-60)
    Given the aggregate element declared in this document
    When the answer for 2026-12-01 is read for "INTAKE" and "SCREENING"
    Then each element carries agent, policy version, prompt version, model version and business date
    Then it carries runs, answered, fallback, fallback rate at four decimals, latency p50, latency p95, tokens, cost and the latest evaluation score
    Then "INTAKE" answers 120 runs, 9 fallbacks, fallback rate 0.0750 and cost 1,840.0000 baht, and "SCREENING" answers 150 runs, 21 fallbacks, fallback rate 0.1400 and cost 2,310.5000 baht
    Then acceptance and override carry the value "no L1 runs" for both agents, because no agent runs at L1 in Epic 1
    Then the element names and their types are fixed by this document and are the ones the app story and the published measure read

  Scenario: AC3 The run read and the case agent-outputs read are restated, not redefined (new, D-RCV-60)
    Given the agent runtime baseline contract of RWB-P10-E1058-CON
    When the two reads are reviewed against it
    Then GET /api/recovery/agent/v1/admin/agent-runs takes the query agent, from and to, answers AgentRun[] and declares 401, 403 and 503 under Platform administration R with scope applied
    Then GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs answers AgentOutput[] and declares 401, 403, 404 and 503 under the Case record read with scope applied
    Then neither read is declared as owned by this story, and a drift is corrected against the baseline and never against this document
    Then the gateway-bff route in front of the reads is a pass-through of one hop, and its route name and path are Not specified in the source documents (GAP-0617; ASM-0894)

  Scenario: AC4 The event contract that feeds the aggregate is declared (new, D-RCV-60)
    Given a run of agent "SCREENING" for case "RW-2026-001001" on 2026-12-01
    When the run completes and the outbox relay publishes it
    Then the message type is rwb.agent.AgentRunCompleted.v1 on rwb.agent.events.v1, keyed by the case ID, with the retry topic and the .dlt topic of the agent topic
    Then the envelope carries the CloudEvents 1.0 attributes id, source, type, specversion, time, subject and datacontenttype, with the run ID as its subject
    Then the payload carries the run facts this document names from the agent_run fields of TSD P10 Agent runtime v2 T3.1: run ID, agent_code, agent_version, prompt_version, model_version, case_id, autonomy_mode, trigger_event, status, fallback, confidence, latency_ms, tokens_in, tokens_out, cost_thb, run_at
    Then rwb-reporting builds its daily projection and the measure "Agent fallback rate" from this payload alone, and no daily event and no lake write is declared by this document
    Then a payload that fails the registry subject is refused before the relay and routed to .dlt with an alert, and no personal data is carried

  Scenario: AC5 The Schedule contract the dashboard reads is fixed (new, D-RCV-60)
    Given the workflow kit of RWB-PLT-E1071-CON
    When the Schedule contract of this document is reviewed
    Then it names AgentRunDailyRollup in namespace rwb-recovery on the task queue rwb-agent, with the workflow identity equal to the business date
    Then the cadence is daily at 01:30 Asia/Bangkok for the previous business date, the overlap policy is SKIP, the catch-up window is one business date and a manual start for any business date is allowed on the same identity
    Then the run states the metric read exposes are COMPLETE, HELD and FAILED, and a HELD date answers its status with the previous published date 2026-11-30
    Then the legacy job table and the legacy job admin read are declared nowhere in the contract, and the name of the Schedule is Not specified in the source documents (GAP-0617; ASM-0895)
    Then a drift between this contract and the registration of RWB-P10-E1063-OPS fails the contract test

  Scenario: AC6 The rwb-reporting measures read and the four fakes are complete (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables and the four fakes are reviewed
    Then each of 12.1 to 12.9 is present, names its owner from the Ownership Map and writes None where it is empty
    Then GET /api/recovery/reporting/v1/reports/measures is consumed with one hop and the 2 s budget and answers the measure "Agent fallback rate" with its business date, its definition and its value
    Then the fakes rwb-reporting, rwb-case, rwb-comms and the gateway-bff route answer every consumed path and payload of this document
    Then no sub-table declares a lake table, an extract, a lake credential or an INT-19 or INT-20 path
    Then a drift between a fake and this document fails the contract test, and the four fake fixtures are synthetic

  Scenario: AC7 The contract keeps the business rules of section 8 (new, D-RCV-60)
    Given the contract files of this story and the rules BR1 to BR10 of section 8
    When the contract review and the contract tests check the files against each rule
    Then the metric read is one operation under /api/recovery/agent/v1 with one element per agent, policy version, prompt version, model version and business date, and no caller reads the tables of rwb-agent (BR1)
    Then the element keeps every legacy figure, and no member is dropped or renamed without a new version (BR2)
    Then no lake table, extract, INT-19 or INT-20 path is declared, and EV-28 on rwb.agent.events.v1 feeds rwb-reporting (BR3)
    Then EV-28 carries run facts only, with no account number, customer name or personal field (BR4)
    Then each message is a CloudEvents 1.0 message on the owner's topic, keyed by the case ID, validated against its registry subject before the relay and routed to .dlt on failure (BR5)
    Then the Schedule contract fixes one identity per business date, the 01:30 cadence, overlap policy SKIP and the rerun rule, and names no legacy job table or admin read (BR6)
    Then the run read and the case agent-outputs read are restated from RWB-P10-E1058-CON and not declared as owned here (BR7)
    Then the cost cap, the alert role and the agent list are only named, as rows read through the rwb-case contracts (BR8)
    Then no path or topic of another service is declared as owned by this contract (BR9)
    Then a held business date answers its status and the previous published date (BR10)
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The metric read is one operation under `/api/recovery/agent/v1` with one answer element per agent, policy version, prompt version, model version and business date; no caller reads the tables of rwb-agent | DP-11; DP-13; legacy section 12 |
| BR2 | The aggregate element carries the legacy figures - runs, answered, fallback, fallback rate, median and 95th percentile latency, tokens, cost and the latest evaluation score - and no member is dropped or renamed without a new version | Legacy sections 4 and 11; TSD P10 Agent runtime v2 T-A.2 API-P10-009 |
| BR3 | The contract declares no data lake: there is no `agent_run_daily`, no extract and no INT-19 or INT-20 path, and the feed of the published measures is EV-28 on `rwb.agent.events.v1` into rwb-reporting | DP-17; ADR-018; Arch v5 slide 37 |
| BR4 | EV-28 carries run facts only: the payload is the `agent_run` fields named here, with no account number, no customer name and no personal field | Arch v5 slides 42 and 43; Template and Rules §R7.2 s17 |
| BR5 | Every message is a CloudEvents 1.0 message on the owner's topic, keyed by the case ID, validated against its registry subject before the relay, and routed to `.dlt` on failure | DP-09; DP-14; Arch v5 slide 42 |
| BR6 | The Schedule contract fixes one identity per business date, the 01:30 cadence, overlap policy SKIP and the rerun rule, and never names the legacy job table or its admin read | DP-10; Arch v5 slides 31 and 44 |
| BR7 | The run read and the case agent-outputs read belong to the agent runtime baseline; this document restates only the members this key reads and never declares them as its own | RWB-P10-E1058-CON; DP-13 |
| BR8 | No business value in the contract: the cost cap 2,000, the alert role "RW-COE" and the agent list are rows of the policy and reference data read through the rwb-case contracts, and the contract only names them | Template and Rules §R7.2 s17; DP-06; DP-07; DL33 (open; assumptions ASM-0135, ASM-0140, ASM-0890 confirmed) |
| BR9 | One base and one topic per service: this contract declares `/api/recovery/agent/v1` and `rwb.agent.events.v1` for rwb-agent and never another service's path or topic as its own | DP-13; DP-14; Arch v5 slide 41 |
| BR10 | A held business date is part of the contract: the read answers its status and the previous published date, so no reader has to infer a hold from a missing row | Legacy AC3; DP-17 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The read, the aggregate element, the restated reads, the event payload, the Schedule contract and the measures read are described | In review |
| In review | Consumer sign-off | The app, deployment, reporting, access and communications stories of this key accept the document and the fakes | Baselined |
| Baselined | Additive change | A member, a query parameter or a payload field is added without removing one | Baselined |
| Baselined | Breaking change to the read or to a payload | A member of the aggregate element or of the event is removed, renamed or retyped | In review, with the owner of the affected contract |
| Baselined | Drift in a fake or against the baseline | A contract test fails | In review |
| Baselined | The agent runtime baseline changes a restated read | RWB-P10-E1058-CON publishes a new shape | Baselined, aligned to the baseline |

These are the states of this document, not of a case, a run or a business date. The run and date states themselves are COMPLETE, HELD and FAILED and belong to RWB-P10-E1063-APP.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-agent | Owns the read shape, the aggregate element, the event payload, the Schedule contract, the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change to the read, the element or the event, and any change to the Schedule contract |
| The rwb-reporting owner | Owns the measure shapes, the measure "Agent fallback rate" and the event consumer, and signs off the payload taken from EV-28 |
| The rwb-case, rwb-comms and rwb-access owners | Own the consumed operations and sign off the shapes taken from their documents |
| The app and deployment stories of this key | Review and accept the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the naming rule, the outbox library and the workflow kit this document reuses |
| Data steward | Confirms that no personal data field is declared in the event or in the answer |

The identity that reads the measures and the parameters is the rwb-agent service identity (DP-02); its name is Not specified in the source documents (GAP-0617; ASM-0893) and is fixed with the deployment story. Every operation of the provided read is authorised by the rwb-access authorise check (DP-08) before it runs; the check is named here, not restated.

### 11. Data

The contract declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Metric query | agent, segment, version, from, to, with the declared page size and cursor | Not specified in the source documents (DOR-RWB-P10-E1063-CON-7) |
| Metric answer element | agent, policyVersion, promptVersion, modelVersion, businessDate, runs, answered, fallback, fallbackRate, latencyP50Ms, latencyP95Ms, tokensIn, tokensOut, costThb, evalScore, acceptance "no L1 runs", override "no L1 runs" | Not specified in the source documents (DOR-RWB-P10-E1063-CON-7) |
| Held date status | businessDate, status COMPLETE, HELD or FAILED, publishedDate, the count-check result | Not specified in the source documents (DOR-RWB-P10-E1063-CON-7) |
| Run read answer | AgentRun[] as published by RWB-P10-E1058-CON; the members this key reads are the run ID, the agent, the case, the status, fallback, latency, cost and the run time | Not specified in the source documents (DOR-RWB-P10-E1063-CON-7) |
| Case agent-outputs answer | AgentOutput[] as published by RWB-P10-E1058-CON | Not specified in the source documents (DOR-RWB-P10-E1063-CON-7) |
| EV-28 payload | runid, agent, caseid, fallback, outcome | Not specified in the source documents (DOR-RWB-P10-E1063-CON-7) |
| Schedule contract | name, namespace, task queue, workflow identity, cadence, overlap policy, catch-up window, rerun rule, the run states | Not specified in the source documents (DOR-RWB-P10-E1063-CON-7) |
| Consumed values | the daily cost cap and the alert role through the parameters contract; LOV-AGENT, LOV-AGENT-ALERT and LOV-PRODUCT through the reference-data contract; the published measure through the measures operation | Not specified in the source documents (DOR-RWB-P10-E1063-CON-7) |
| Refusal | the platform problem response: status, code, detail, the message ID when a business message applies | Not specified in the source documents (DOR-RWB-P10-E1063-CON-7) |

The page size, the cursor form, the exact types of `fallbackRate` and `costThb` beyond four decimals and the member names of the held-date status are Not specified in the source documents (GAP-0617; ASM-0893); this document fixes the element names and leaves the types to the review with their owners. No table of any schema, and no lake table, is declared as an answer source: the read answers from `rwb_agent` and the measures from rwb-reporting (DP-01, DP-17).

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Purpose | Rights |
|---|---|---|---|
| GET | `/api/recovery/agent/v1/admin/agent-metrics` | Read agent measures per agent, version, segment and business date for the agent monitor: query agent, segment, version, from, to; 200 AgentMetric[]; a held date answers its status and its previous published date | Rules and parameters R, scope applied; errors 401, 403, 422, 503; one hop, 2 s to the caller |

The run read `GET /api/recovery/agent/v1/admin/agent-runs` and the case read `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` are provided by rwb-agent and baselined in RWB-P10-E1058-CON; section 12 of that document owns their full shape. This contract restates only the members this key reads and declares no other operation of its own.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this contract |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The daily cost cap 2,000 and the alert role "RW-COE" of the approved policy row, read at run time (DP-06) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-AGENT, LOV-AGENT-ALERT and LOV-PRODUCT, checked before a daily row or an alert is written (DP-07) |
| GET | `/api/recovery/reporting/v1/reports/measures` | P9 rwb-reporting | The published measure "Agent fallback rate" for a business date, with its definition and its value |
| POST | the rwb-comms notification operation: Not specified in the source documents (GAP-0617; ASM-0896) | P6 rwb-comms | The notice of MSG-P10-004 to the alert role and to RW-RISK, and the notice to the data steward of a held date |

Every operation is one hop with a 2 s client budget (DP-11, ADR-020). The delivery of a notice beyond rwb-comms is the contract RWB-P2-E1007-CON and is not called by this service. No lake operation and no INT-19 or INT-20 path is consumed (DP-17).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` (EV-28) | `rwb.agent.events.v1` | P10 | the case ID | runid, agent, caseid, fallback, outcome |

The event is inserted in the outbox in the same transaction as the run row and relayed by the outbox library; the payload is validated against its registry subject before the relay (DP-09; BR5). Its publication belongs to the run path of RWB-P10-E1058-APP; this document fixes the payload this key's readers depend on. No daily event, no aggregate event and no lake copy is declared (DP-17; BR3).

#### 12.4 Events consumed

None. The dashboard is read on request and the rollup reads the rows of `rwb_agent`; no topic is consumed by this key on the agent side. The consumers of EV-28 are rwb-decision, rwb-document, rwb-deviation and rwb-reporting (Arch v5 slide 43), and the projection rwb-reporting builds from it is its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunDailyRollupWorkflow | Workflow, one per business date, workflow ID = the business date | `rwb-agent` | Input: business date, the requested-by role and the manual-start flag. Output: the run state COMPLETE, HELD or FAILED and the counts of the date |
| aggregateAgentRuns | Activity | `rwb-agent` | Output: the daily aggregate rows and the count-check result |
| raiseCostAlerts | Activity | `rwb-agent` | Output: the `agent_alert` rows on the unique key of agent, type, segment and date |
| dispatchAgentAlerts | Activity | `rwb-agent` | Output: the notice requests and the outbox rows; no partial write |

The workflow identity, the queue and the namespace are the Schedule contract of 12.6; the activity names and their inputs and outputs are this story's and are accepted by RWB-P10-E1063-APP.

#### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| AgentRunDailyRollup | Daily at 01:30 Asia/Bangkok for the previous business date; overlap policy SKIP; catch-up window one business date; a manual start for any business date on the same identity; run states COMPLETE, HELD and FAILED | Namespace `rwb-recovery`, task queue `rwb-agent`, registered through RWB-PLT-E1071-CON by RWB-P10-E1063-OPS; the name is Not specified in the source documents (GAP-0617; ASM-0895) | The legacy Quartz entry of JOB-15 at 01:30 and its `agentRunDaily` step |

The legacy job table, its admin read and the legacy rerun operation are declared nowhere: a rerun is a manual start of the same workflow identity for the business date (DP-10; BR6).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| agent_alert | P10 (`rwb_agent`) | The alert rows the contract exposes through MSG-P10-004 and the held-date status; the unique key of agent, type, segment and date; no column added here |
| agent_run | P10 (`rwb_agent`) | The run facts of the EV-28 payload and the input of the aggregate; no column added |
| agent_evaluation | P10 (`rwb_agent`) | The latest DONE score of an agent and version, read for the element of the aggregate; no column added |
| agent_policy | P10 (`rwb_agent`) | The approved policy version of the agent; its cap and alert role are reached through the parameters contract; no column added |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | The outbox and idempotency envelope of the alerts (DP-09) |

No table of another service is declared and no foreign key crosses a schema (DP-01). `parameter_catalog`, `parameter_value`, `reference_version` and `reference_row` are P3's, `measure_definition`, `measure_publish` and `measure_snapshot` are P9's, and both sets are reached through their contracts. No lake table is declared, because no data lake exists (DP-17; BR3).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-reporting WireMock | The published measure "Agent fallback rate" for 2026-12-01 with its definition and its value; the measure of 2026-11-30; a measure that is not published for the date; a delay beyond 2 s | Contract tests, app story, reporting story |
| rwb-case WireMock | `daily_cost_cap_thb` 2,000 and `alert_role` "RW-COE" for INTAKE, SCREENING and EXTRACT; a policy row with no cap; LOV-AGENT, LOV-AGENT-ALERT and LOV-PRODUCT; a delay beyond 2 s | Contract tests, app story |
| rwb-comms WireMock | An accepted notice with its reference for MSG-P10-004; a 503 at 01:40; an accepted notice for the data steward of a held date | Contract tests, app story, communications story |
| gateway-bff route stub | A pass-through route in front of the metric read and the two restated reads, one hop, JSON media type preserved, the refusal passed through unchanged | Contract tests, app story, deployment story |

The outbox stub, the workflow kit stub and the access guard stub are the platform's and are used but not declared here. Every fixture is synthetic and holds no personal data.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 2 restated and used, 4 consumed | The metric read provided; the run read and the case agent-outputs read restated from the baseline; the parameters, the lists, the measures and the notice consumed, one hop and 2 s each |
| Kafka | 1 published, 0 consumed | EV-28 on `rwb.agent.events.v1` with the retry and `.dlt` topics, keyed by the case ID, through the outbox; no lake write |
| Temporal | 1 workflow, 3 activities, 1 Schedule | AgentRunDailyRollupWorkflow with aggregateAgentRuns, raiseCostAlerts and dispatchAgentAlerts on the queue `rwb-agent`, started by AgentRunDailyRollup at 01:30 |
| File | None | No file is read or written and no extract exists: the answer is the body of the read and the feed is the topic (DP-17) |

### 13. Solution plan

**Deliverables.** `contract/agent-metric-read.yaml` (the read, its query, its paging, its element and its held-date status), `contract/agent-metric-element.md` (the aggregate element and its legacy figures), `contract/agent-admin-reads.md` (the run read and the case agent-outputs read restated from the baseline), `contract/agent-run-completed.asyncapi.yaml` (EV-28 on `rwb.agent.events.v1`, its envelope, its subject and the `.dlt` route), `contract/agent-rollup-schedule.md` (the Schedule contract, its identity, its run states and the rerun rule), `contract/agent-monitor-boundaries.md` (the measures, parameters, lists and notice reads with their budgets) and the four WireMock mappings with their fixtures.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON for the app story; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON for the app story; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON for the app story |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON for the app story |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | H RWB-P10-E1063-CON for the app story; none here |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON for the app story |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON for the app story |

This story is Day 1 and holds no build dependency of its own (§R5.7): the platform contracts it names are those its consumers add, and the C dependencies of the key are the published contracts of rwb-case and rwb-integration. DP-17 adds no dependency and removes the legacy lake dependency; the lake is not contracted anywhere.

**Build steps**

1. Write the metric read contract: method, path under the base, the five query parameters, the declared paging, the element with its members and types, the held-date status and the refusal codes.
2. Write the aggregate element document with the legacy figures of 2026-12-01 and the "no L1 runs" values, and the rule that a member is removed only with a new version.
3. Restate the run read and the case agent-outputs read against the baseline, with their query, answer, rights and errors, and mark the baseline as owner.
4. Write the EV-28 AsyncAPI document: the envelope, the key, the payload members, the registry subject and the `.dlt` route, and the statement that rwb-reporting projects the daily measure from it.
5. Write the Schedule contract: the name, the namespace, the queue, the identity, the cadence, the overlap policy, the catch-up window, the rerun rule and the run states.
6. Write the boundary document for the measures, parameters, lists and notice reads, with one hop and the 2 s budget.
7. Build the four WireMock mappings and their synthetic fixtures, including the 503 of the notice and the silent measure read.
8. Add the contract tests of section 16, including the drift test between each fake and this document and between the Schedule contract and the registration.
9. Tag the baseline and collect the sign-off of the app, deployment, reporting, access and communications stories of this key.

**Done when.** The six contract files validate in the pipeline, the six contract tests pass, the four fakes answer every consumed path and payload, no sub-table declares a lake artefact, and the app and deployment stories of this key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-004 | Agent cost on a business date above its daily limit | {agent} used {amount} baht of model calls on {date}, above the daily limit of {limit} baht. |
| MSG-P1-001 | The report shows the previous day after a held publish | {product} is from {date}. Today's load has not arrived. |
| MSG-P4-002 | A role without the right reads the metric read | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required query member is empty or the paging is outside the declared range | Enter {field}. |

The three business messages are the legacy messages of RWB-E1-063 and keep their wording character for character; MSG-GEN-001 is the platform message of an empty required field. This contract adds no message.

### 15. Screens and states

None in this story. The contract serves the agent monitoring dashboard indirectly: the dashboard is composed by the gateway-bff route (DP-19) and belongs to RWB-P10-E1063-APP, SCR-46 Agent monitor belongs to RWB-E2-031 and is not changed here, and the run read and the configuration reads belong to RWB-P10-E1058-CON. The contract fixes no screen field, no order and no masking rule. The states of SCR-46 (empty, loading, error and no access) are Not specified in the source documents (CG-ALL-2668). The exact path of the gateway-bff route in front of the metric read is Not specified in the source documents (GAP-0617; ASM-0894).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-E1063-CON-01 | AC1 | Contract | The read validated against its schema: the five query parameters, the declared paging, a request outside the range refused with 422 and MSG-GEN-001, and the four refusal codes |
| TC-P10-E1063-CON-02 | AC2 | Contract | The element for 2026-12-01: INTAKE 120 runs, 9 fallbacks, 0.0750 and 1,840.0000; SCREENING 150 runs, 21 fallbacks, 0.1400 and 2,310.5000; acceptance and override "no L1 runs" |
| TC-P10-E1063-CON-03 | AC3 | Contract | The run read and the case agent-outputs read against the baseline: query, answer, rights, errors, and the route pass-through of one hop |
| TC-P10-E1063-CON-04 | AC4 | Contract | EV-28 for a run of SCREENING: the envelope, the key, the payload members, a status outside LOV-AGENT-RUN, a registry refusal and the `.dlt` route |
| TC-P10-E1063-CON-05 | AC5 | Contract | The Schedule contract against the registration: the name, the namespace, the queue, the identity equal to the business date, the 01:30 cadence, SKIP, the catch-up window and the three run states |
| TC-P10-E1063-CON-06 | AC6 | Contract | The nine sub-tables with None where empty, no lake artefact in any sub-table, and the four fakes answering every consumed path and payload |
| TC-P10-E1063-CON-07 | AC6 | Contract | Boundary of the tables of section 12.7: each table kept to its owner and contracted use, no column added, no foreign key across a schema, no table of another service declared |
| TC-P10-E1063-CON-08 | BR1 | Contract | One operation under `/api/recovery/agent/v1` with one element per agent, policy version, prompt version, model version and business date; no caller reads the tables of rwb-agent |
| TC-P10-E1063-CON-09 | BR2 | Contract | The aggregate element carries runs, answered, fallback, fallback rate, median and 95th percentile latency, tokens, cost and latest evaluation score; no member dropped or renamed |
| TC-P10-E1063-CON-10 | BR3 | Contract | No lake table, extract, INT-19 or INT-20 path declared; the feed of the published measures is EV-28 on `rwb.agent.events.v1` into rwb-reporting |
| TC-P10-E1063-CON-11 | BR4 | Contract | The EV-28 payload carries the agent_run fields only, with no account number, customer name or personal field |
| TC-P10-E1063-CON-12 | BR5 | Contract | Each message is a CloudEvents 1.0 message on the owner's topic, keyed by case ID, validated against its registry subject before relay, and routed to `.dlt` on failure |
| TC-P10-E1063-CON-13 | BR6 | Contract | The Schedule contract fixes one identity per business date, the 01:30 cadence, overlap policy SKIP and the rerun rule, and names no legacy job table or admin read |
| TC-P10-E1063-CON-14 | BR7 | Contract | The run read and case agent-outputs read are declared as baseline members of RWB-P10-E1058-CON and not as members of this document |
| TC-P10-E1063-CON-15 | BR8 | Contract | Cost cap, alert role and agent list appear only as parameter or reference-data names read through the rwb-case contracts, with no business value in the contract |
| TC-P10-E1063-CON-16 | BR9 | Contract | The contract declares only `/api/recovery/agent/v1` and `rwb.agent.events.v1`, with no other service's path or topic declared as its own |
| TC-P10-E1063-CON-17 | BR10 | Contract | A held business date: the read answers its status and the previous published date, so no row absence is needed to infer a hold |
| TC-P10-E1063-CON-18 | AC7 | Contract | The contract files checked against BR1 to BR10: one read and element, no dropped member, no lake artefact, EV-28 facts and envelope, the Schedule rules, the restated reads, named values only, own base and topic, and the held date |

### 17. Guardrails

- No business value in the contract: the cost cap 2,000, the alert role "RW-COE", the agent list and the cadence stay rows of the policy, the reference data and the registration, and the contract only names them.
- No personal data in an event, an answer, an example or a fake: identifiers and facts only, and the fixtures are synthetic.
- The contract names the agent read and the agent topic as rwb-agent's and consumes every other operation and topic; a document that declares another service's path or topic as provided fails the review (DP-13, DP-14).
- No lake table, extract, lake credential or INT-19 or INT-20 path is declared anywhere in this contract (DP-17; BR3).
- The run read and the case agent-outputs read are restated, never redefined: the baseline RWB-P10-E1058-CON owns them and a drift is corrected there.
- Every payload is validated against its registry subject before the relay, and a refusal is routed to `.dlt` and alerted (DP-09).
- The Schedule contract never names the legacy job table, its admin read or its rerun operation (DP-10).
- Every fixture is synthetic; no production run, case, model answer or measure is copied into a schema, a payload or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-009 | Copied daily for reporting, with row counts matched (the legacy text names the data lake copy, which DP-17 removes; the copy becomes the event feed) | EV-28 and the held-date status of the metric read | TC-P10-E1063-CON-02, TC-P10-E1063-CON-04 |
| D-RCV-60 DP-09 | Kafka with outbox, inbox and CloudEvents | The EV-28 AsyncAPI document, its registry subject and its `.dlt` route | TC-P10-E1063-CON-04 |
| D-RCV-60 DP-10 | Temporal Schedules replace Quartz | The Schedule contract with its identity, its cadence and the rerun rule | TC-P10-E1063-CON-05 |
| D-RCV-60 DP-11 | Contract-first REST, one hop, 2 s timeout | The provided read and the four consumed reads with their budgets | TC-P10-E1063-CON-01, TC-P10-E1063-CON-03 |
| D-RCV-60 DP-13 | One REST base per service | The base `/api/recovery/agent/v1` and the two restated reads | TC-P10-E1063-CON-01, TC-P10-E1063-CON-03 |
| D-RCV-60 DP-17 | No data lake; reporting from events | No lake artefact in any sub-table, and the event feed into rwb-reporting | TC-P10-E1063-CON-04, TC-P10-E1063-CON-06 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The read shapes and the four fakes | TC-P10-E1063-CON-01, TC-P10-E1063-CON-03 |

### 19. Out of scope

- The implementation of the aggregate, the count check, the alerts and the read (RWB-P10-E1063-APP).
- The chart, the Schedule registration, the consumer group, the dashboards, the alerts and the runbook (RWB-P10-E1063-OPS).
- The whole agent runtime contract, its configuration resources and the full shape of the run read and the case read (RWB-P10-E1058-CON).
- The evaluation harness, the score rows and the proposal (RWB-P10-E1060-APP, RWB-P10-E1061-CON).
- The measure definitions, the projections, the snapshots and the steering dashboard (P9 rwb-reporting; RWB-E2-009).
- The notification path, the message template and the delivery of MSG-P10-004 (RWB-P6-E1063-APP), and the delivery beyond it through rwb-integration (RWB-P2-E1007-CON).
- The right check and the refusal of a role without the reporting read (RWB-P4-E1063-APP).
- The parameters, reference data and access rights themselves (rwb-case, rwb-access).
- The agent monitor screen SCR-46 and its dashboard (RWB-E2-031), and drift detection (FEAT-AGT-13).
- The end-to-end proof across services (RWB-ITG-E1063-ITG).
- Any lake table, extract, lake credential or lake path, which DP-17 removes (GAP-0617).

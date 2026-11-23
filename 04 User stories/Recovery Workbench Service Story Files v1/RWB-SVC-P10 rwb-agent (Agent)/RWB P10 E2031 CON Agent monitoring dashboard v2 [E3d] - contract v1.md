# RWB-P10-E2031-CON Agent monitoring dashboard v2 [E3d]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E2031-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-031 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP07, DP10, DP13, DP15, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-018, FR-P10-026) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract slice of RWB-E2-031 for rwb-agent, the Day-1 baseline that the app and deployment slices of the key build against. It fixes the version 2 of the metric read on `/api/recovery/agent/v1/admin/agent-metrics` - its five query parameters, its paging, its answer element, its two filter refusals and the status of a held business date - and adds to the element of RWB-P10-E1063-CON the segment, the mode, the acceptance and correction rates, the override rate and override count, the decision-quality score, the feedback count, the reconciled flag with the token difference and the two threshold echoes (DP-13, DP-15). It fixes the two reads the dashboard uses and does not own - `GET /admin/agent-runs` and `GET /cases/{caseId}/agent-outputs` - as restatements of the RWB-P10-E1063-CON baseline and never as redefinitions, and it fixes at the boundary the decision-quality and override read of RWB-P7-E2005-CON through `GET /api/recovery/decision/v1/decision-log`, the reference-data read of RWB-P3-E1043-CON, the published measures of rwb-reporting and the notification path of rwb-comms (DP-03, DP-07). It fixes the Schedule contract of the daily rollup and the cost sweep - one identity, `AgentRunDailyRollup`, in namespace `rwb-recovery` on the task queue `rwb-agent`, with its cadence, its overlap policy, its catch-up window, its rerun rule, its four steps and its three run states - because the legacy Quartz entry of the key has no target (DP-10). It fixes the gateway-bff route in front of the read and the four fakes (DP-19). It declares no data lake, no extract and no lake path anywhere: the data lake does not exist in Architecture v5 and the aggregate is served on the read (DP-17 is not applied by this key, and the reason is stated in section 12). It builds no business behaviour. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead of rwb-agent**, I want **the version 2 of the agent monitoring contract fixed on Day 1 - the metric read on `/api/recovery/agent/v1/admin/agent-metrics` with its five query parameters, its paging, its answer element per agent, policy version, prompt version, model version, segment and business date, its two filter refusals and its held-date status; the override and decision-quality elements that come from the decision log of rwb-decision; the run read and the case agent-outputs read restated against the baseline of RWB-P10-E1063-CON; the decision-quality, reference-data, measures and notification reads at the boundary; the Schedule contract of the daily rollup and the cost sweep with its identity, cadence, overlap policy, catch-up window, rerun rule and three run states; the gateway-bff route; and the four contract fakes**, so that **the app slice RWB-P10-E2031-APP, the deployment slice RWB-P10-E2031-OPS, the access, decision, reporting and communications slices of this key and every reader of a daily agent figure build against one agreed, testable shape on Day 1, without waiting for a schedule to be registered, a policy to be approved or a ledger to hold a row, and without any reader being offered a lake table that does not exist**.

### 2. Business rationale

The legacy key RWB-E2-031 was written inside the monolith. A Spring Batch step of JOB-15 wrote the data lake table `agent_run_daily`, another step `agentDrift` read it, a Power BI page read it, an in-process `P7 DecisionLogQuery.byAgentVersion(agentVersion, from, to)` supplied the override figures, and the cost alert called the P6 notification interface of the same deployment (legacy sections 4, 12 and 13). In the target each of those is a boundary or is gone:

- The data lake and its Power BI feed are removed by Architecture v5 (slide 37; ADR-018). DP-17 is not one of this key's patterns, so this contract applies no lake replacement: instead the aggregate is served on the read of the service that owns the rows, and rwb-reporting builds its published measures from the events of `rwb.agent.events.v1` that the run path already publishes. The word "lake" appears in this document only to say that no such artefact is declared.
- The two legacy batch steps become the four steps of one Temporal Schedule, `AgentRunDailyRollup`, in namespace `rwb-recovery` on the task queue `rwb-agent` (DP-10). There is no shared job table, no Quartz entry and no `POST /admin/jobs/{jobId}/rerun` in the target: a rerun is a manual start of the same workflow identity for the business date.
- The in-process `DecisionLogQuery` becomes `GET /api/recovery/decision/v1/decision-log` on rwb-decision, one hop with the 2 s budget (DP-03, DP-11 at the boundary). Its recommendation, its final call and its override reason are the only source of the override rate, the override count and the decision-quality score.
- The in-process `recovery_case.product_group` read becomes the segment the run row already carries, `agent_run.segment_product_group` and `agent_run.segment_region_code`, so the service reads its own table and never `rwb_case`.
- The notification interface becomes the rwb-comms contract of the communications slice, with the outbox retry the platform library provides.
- The Power BI page becomes SCR-46 behind the gateway-bff composite route (DP-19).

Contract-first only works if the seam is written down once. The seam here is small and load-bearing: one read whose element now carries the L1 measures, the segment and the reconciled flag; two run reads that must not drift from the baseline that owns them; one decision-log read at the boundary that three figures depend on; one Schedule contract that four steps and two team types depend on; one route; and four fakes that make the app and the deployment testable on Day 1. If the shape is agreed and faked on Day 1, five teams move at once. Without it, each caller invents its own element, the acceptance of the dashboard and the measures of rwb-reporting drift apart, and a held business date is invisible to the reader.

This story defines the provided side of the version 2 read and the consumed side of the key, and it never restates what another owner holds: the decision log is rwb-decision's, the lists are rwb-case's, the measures are rwb-reporting's, the notice is rwb-comms's, the right is rwb-access's and the aggregate of a business date is the baseline's (DP-01).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL), so the REST base, the topic and the event names follow the platform rule and not a local choice (DP-13, DP-14).
- The CloudEvents 1.0 envelope, the platform error envelope and the platform message catalogue are the baseline; this document narrows them where it must and says so.
- The monitoring baseline contract of RWB-P10-E1063-CON is in force: the version 1 metric read, its aggregate element, the `AgentRunDailyRollup` Schedule contract, the `agent_alert` table and the publication of `rwb.agent.AgentRunCompleted.v1` are its elements, and this document adds to them rather than redefining them.
- The agent runtime baseline of RWB-P10-E1058-CON is in force for the run resource, the error taxonomy and the run path that writes `agent_run.segment_product_group`, `agent_run.segment_region_code` and the `agent_feedback` verdicts.
- The decision-record library of RWB-PLT-E1027-CON publishes the local record shape and the shared topic `rwb.decision-record.v1` that carries a decision record into the central ledger of rwb-decision (DP-03).
- The workflow kit of RWB-PLT-E1071-CON publishes the Schedule registration contract with namespace `rwb-recovery`, the overlap policy, the catch-up window and the manual start on the same identity (DP-10).
- The reference-data contract and the client library of rwb-case are published by RWB-PLT-E1043-CON (DP-07); the per-service Flyway sequence is published by RWB-PLT-E1044-CON (DP-15); the gateway-bff route contract and its stub are published by RWB-PLT-N001-CON (DP-19).
- The decision-quality and override read of RWB-P7-E2005-CON is published: `GET /api/recovery/decision/v1/decision-log` with its query, its page and its entry, carrying the recommendation, the final call, the override reason, the agent version and the decided-at time. Its agent-version filter and its override-reason element are Not specified in the source documents (GAP-0630; ASM-0960).
- The published measures of rwb-reporting are known by their shape and the notification path of the communications slice of this key is known by its request; the operation of the notice is Not specified in the source documents (GAP-0630; ASM-0961).
- The name of the read's right is Not specified in the source documents (GAP-0630; ASM-0970): TSD P10 Agent runtime v2 T-A.1 API-P10-009 declares Rules and parameters R and the legacy story names Platform administration R.
- The page size default and maximum, the cursor form and the exact types of the rate and amount members beyond four decimals are Not specified in the source documents (GAP-0630; ASM-0971).
- The name of the service login used by the contract tests is Not specified in the source documents (GAP-0630; ASM-0966).
- No build dependency: this story is Day 1 by rule (§R5.7) and sits in contract group CG-W2. The release date 31 December 2026 is tentative and is copied unchanged.

### 4. Flow

1. Draft the version 2 of the metric read that extends the version 1 element: its method and its path under `/api/recovery/agent/v1`, its five query parameters, its declared paging, its answer element, its two filter refusals, its held-date status and its refusal codes.
2. Fix the nine version 2 members of the element and the rule that no version 1 member is removed, renamed or retyped within major version 1 (AC2).
3. Fix the override and decision-quality members with their definition, their source in the decision-log read of rwb-decision and the behaviour when that read does not answer (AC2).
4. Restate the run read and the case agent-outputs read from the baseline of RWB-P10-E1063-CON: query, answer, rights, errors and the route they are published on (AC3).
5. Fix at the boundary the decision-log read, the reference-data read, the published measures and the notification path, each with one hop and the 2 s budget, and state the parameter read the key does not consume and why (AC4, AC5).
6. Fix the Schedule contract of the daily rollup and the cost sweep: the name, the namespace, the task queue, the workflow identity, the cadence, the overlap policy, the catch-up window, the rerun rule, the four steps and the three run states (AC6).
7. Fix the gateway-bff route in front of the read and the four fakes with the answers, the errors and the timings this key's tests need (AC7).
8. State in every sub-table that no lake artefact is declared, and fail the review of a document that declares one (AC8).
9. Publish the nine sub-tables of section 12, the contract tests and the baseline tag for the app and the deployment stories.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A member of the version 2 element drifts from this document: a renamed member, a retyped rate, a dropped count | The contract test fails and the merge is blocked | None | AC1, AC2 |
| X2 | A caller asks for a range or a page the contract does not allow, or omits a required query member | The read refuses with 422 and names the member; nothing is read | MSG-GEN-001 | AC1 |
| X3 | A caller filters from a date after the to date, or over a range above 92 days | The read refuses with 422 and the message of the legacy screen | MSG-GEN-003, MSG-GEN-002 | AC1 |
| X4 | The contract declares a lake table, an extract, a lake credential or a lake path | The review refuses the document, because no data lake exists | None | AC8 |
| X5 | A version 1 member is removed, renamed or retyped by the version 2 element | The contract test fails and a new major version is required | None | AC2 |
| X6 | A payload of the agent topic gains a personal field, or fails its registry subject | The data-steward review and the contract test refuse the payload; a produced message that fails is routed to `.dlt` with an alert | None | AC4 |
| X7 | The Schedule name, the workflow identity, the step list or the rerun rule in the document drifts from the registration of RWB-P10-E2031-OPS | The contract test between the document and the registration fails and one of the two is corrected; the deployment owns the registration | None | AC6 |
| X8 | A restated operation drifts from the baseline of RWB-P10-E1063-CON | The contract test fails on the baseline and this document is aligned, because the baseline is the owner | None | AC3 |
| X9 | A field-level detail of a consumed operation, of a member or of the paging is missing from the source material | The element carries the placeholder, the gap row and its assumption rows, and the fake is written to the assumed shape | None | AC1, AC4, AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the workflow kit, the decision-record library, the monitoring and runtime baselines and the P3, P7, P9 and P6 contracts as published |
| Negotiable | The page size, the cursor form and the field-level detail of the consumed operations are settled with their owners; the element, the Schedule contract and the boundary mapping are fixed by this realignment |
| Valuable | Unblocks the app, deployment, access, decision, reporting and communications slices of this key on Day 1 and gives every reader of a daily agent figure one shape |
| Estimable | One provided read, two restated reads, four consumed boundaries, one Schedule contract, one route and four fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact - the schema file, the element document, the fake, the Schedule contract - and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Agent monitoring contract slice version 2 for rwb-agent

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the monitoring baseline contract of RWB-P10-E1063-CON and the agent runtime baseline of RWB-P10-E1058-CON are in force
    Given the workflow kit of RWB-PLT-E1071-CON and the decision-record library of RWB-PLT-E1027-CON are in force

  Scenario: AC1 The version 2 metric read is contracted on the agent base (new, D-RCV-60)
    Given the contract file of this story and a running rwb-agent on the base /api/recovery/agent/v1
    When the dashboard asks for the measures of 2026-12-01 to 2026-12-14 with agent "INTAKE" and "SCREENING", segment MORTGAGE/BKK, version and the from and to dates
    Then one operation answers on GET /api/recovery/agent/v1/admin/agent-metrics with 200 and an AgentMetric[] in the member names and types of this document
    Then the query takes agent, segment, version, from and to, the paging is declared with its page size and its cursor, and a request outside the declared range or paging is refused with 422 and MSG-GEN-001
    Then a from after the to date is refused with 422 and MSG-GEN-003, and a range above 92 days with 422 and MSG-GEN-002 naming 1 and 92 days
    Then the refusals are 401 without a session, 403 without the right of the read with MSG-P4-002, and 503 when the store or a consumed contract is unavailable
    Then a business date that is HELD answers its status with the previous published date, so no reader has to infer a hold from a missing element
    Then the page size default and maximum, the cursor form and the name of the right are Not specified in the source documents (GAP-0630; ASM-0971)

  Scenario: AC2 The version 2 element adds the L1, segment and quality members without breaking version 1 (new, D-RCV-60)
    Given the element of RWB-P10-E1063-CON and the element declared in this document
    When the two are compared member by member for 2026-12-14
    Then every version 1 member is present with the same name and type, and no member is removed, renamed or retyped within major version 1
    Then the element adds segment, mode, acceptanceRate, correctionRate, overrideRate, overrideCount, decisionQualityScore, feedbackCount, reconciled, tokenDifference, driftThreshold and costCapThb
    Then "INTAKE" for segment MORTGAGE/BKK answers 140 feedback entries with 119 accepted, acceptanceRate 0.8500, and "SCREENING" answers mode "L1" for MORTGAGE/BKK and "SHADOW" elsewhere
    Then overrideRate is the decisions of the agent version whose final call differs from the recommendation over the decisions of the agent version at four decimals, overrideCount is that numerator, and decisionQualityScore is the complement at four decimals, all read through the decision-log read of RWB-P7-E2005-CON
    Then an element whose decision-log read did not answer answers the override and quality members as null with a reason code and never guesses a figure
    Then driftThreshold and costCapThb are read-only echoes of the approved policy row and are not members a caller may set
    Then the agent-version filter and the override-reason element of the decision-log read are Not specified in the source documents (GAP-0630; ASM-0960)

  Scenario: AC3 The run read and the case agent-outputs read are restated, not redefined (new, D-RCV-60)
    Given the baseline of RWB-P10-E1063-CON and the runtime baseline of RWB-P10-E1058-CON
    When the two reads the dashboard uses are reviewed against them
    Then GET /api/recovery/agent/v1/admin/agent-runs takes the query agent, from and to, answers AgentRun[], and declares 401, 403 and 503 under the right of the read with scope applied
    Then GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs answers AgentOutput[] and declares 401, 403, 404 and 503 under the Case record read with scope applied
    Then neither read is declared as owned by this story, and a drift is corrected against the baseline and never against this document
    Then the members this key reads from a run are the run ID, the agent, the case, the status, the fallback, the latency, the cost and the run time, and the segment of the run is read for the version 2 element

  Scenario: AC4 The decision-quality and override read and the measures read are fixed at the boundary (new, D-RCV-60)
    Given the decision-log read of RWB-P7-E2005-CON and the published measures of rwb-reporting
    When the boundary of this contract is reviewed
    Then GET /api/recovery/decision/v1/decision-log is consumed with one hop, the 2 s budget and a breaker, with the query of an agent version over a date range, and answers the recommendation, the final call, the override reason and the decided-at time
    Then GET /api/recovery/reporting/v1/reports/measures is consumed with one hop and the 2 s budget and answers the published measures of a business date or a month with their definition and their value
    Then the override rate, the override count and the decision-quality score are declared to come from the first read only, and the measure of rwb-reporting is declared as a copy shown beside the figure and never as a second source of it
    Then a refusal or a timeout of either read is declared to leave the figure null with a reason code, and no figure is derived from a partial answer

  Scenario: AC5 The reference-data read is consumed and the parameter read is named as not consumed (new, D-RCV-60)
    Given the reference-data contract of RWB-P3-E1043-CON and the parameter operation of rwb-case
    When the boundary of this contract is reviewed
    Then GET /api/recovery/case/v1/admin/lists/{listCode} is consumed with one hop and the 2 s budget for LOV-PRODUCT, LOV-REGION, LOV-AGENT, LOV-AGENT-ALERT and LOV-ROLE with the version in force
    Then the band of the segment filter and the alert type written by the rollup are checked against those lists before they are used
    Then no parameter read is consumed by this key, because DP-06 is not one of its patterns and the cap, the alert role and the drift values are approved policy rows of agent_policy that the service reads from its own schema, while the two range limits of the screen are configuration values of the release
    Then the parameter operation is named in this document only so that no reader invents one, and it appears in no sub-table of section 12 as consumed

  Scenario: AC6 The Schedule contract of the daily rollup and the cost sweep is fixed (new, D-RCV-60)
    Given the workflow kit of RWB-PLT-E1071-CON and the baseline Schedule of RWB-P10-E1063-CON
    When the Schedule contract of this document is reviewed
    Then it names AgentRunDailyRollup in namespace rwb-recovery on the task queue rwb-agent, with the workflow identity equal to the business date
    Then the cadence is daily at 01:30 Asia/Bangkok for the previous business date, the overlap policy is SKIP, the catch-up window is one business date and a manual start for any business date is allowed on the same identity
    Then the run executes four steps in order: aggregateAgentRuns for the daily rollup, raiseCostAlerts for the cost sweep of the date and its month-to-date totals, agentDrift for the drift check and dispatchAgentAlerts for the notices
    Then the run states the metric read exposes are COMPLETE, HELD and FAILED, and a HELD date answers its status with the previous published date
    Then no second Schedule is declared, because the cost sweep of a business date shares the identity, the overlap policy and the catch-up window of the rollup it reads
    Then the legacy job table, its admin read and its rerun operation are declared nowhere in the contract
    Then the name of the Schedule and of its steps beyond the baseline and the legacy step names is Not specified in the source documents (GAP-0630; ASM-0958)

  Scenario: AC7 The gateway-bff route and the four fakes are complete (new, D-RCV-60)
    Given the route contract of RWB-PLT-N001-CON and the contract section of this story
    When the route and the four fakes are reviewed
    Then the read and the two restated reads are declared to be reached through the gateway-bff route, one hop, with the JSON media type and the refusal passed through unchanged
    Then the route is declared in front of the metric read, the run drill-down and the override panel, and no screen is declared to call rwb-agent directly
    Then the fakes rwb-decision, rwb-case, rwb-reporting and rwb-comms answer every consumed path and payload of this document, and the route stub answers the three reads
    Then a drift between a fake and this document fails the contract test, and every fixture is synthetic
    Then the route name and path are Not specified in the source documents (GAP-0630; ASM-0967)

  Scenario: AC8 No lake artefact is declared anywhere in the contract (new, D-RCV-60)
    Given the nine sub-tables of section 12 and the element document of this story
    When the whole contract is scanned
    Then no table, no extract, no credential, no data-set job and no file path of a data lake is declared as an answer source or as a consumed operation
    Then the aggregate is declared to be answered from the rows of rwb_agent on the read, and the published measures of rwb-reporting are declared to be built from rwb.agent.events.v1 by their owner
    Then a document that declares one lake artefact fails the review and the contract test, with the row or the sentence named
    Then the absence is stated as a positive rule of the contract and not as an omission
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The metric read is one operation under `/api/recovery/agent/v1` with one answer element per agent, policy version, prompt version, model version, segment and business date; no caller reads the tables of rwb-agent | DP-11; DP-13; legacy section 12 |
| BR2 | The element carries the version 1 members unchanged and adds the version 2 members; a member is removed, renamed or retyped only with a new major version | RWB-P10-E1063-CON; legacy sections 4 and 11; TSD P10 Agent runtime v2 T-A.2 API-P10-009 |
| BR3 | The override rate, the override count and the decision-quality score come from the decision-log read of rwb-decision only, and are null with a reason code when that read does not answer | REQ-APD-005; DF-DEC-009, DF-DEC-012, DF-DEC-013; RWB-P7-E2005-CON |
| BR4 | The segment of an element is the product group and the region the run row carries; the contract never names a table of rwb-case as an answer source | DF-AGT-059, DF-AGT-060; DP-01 |
| BR5 | A from after the to date is refused with 422 and MSG-GEN-003, and a range above 92 days with 422 and MSG-GEN-002; the two limits are named by the messages and held as configuration, not as literals | Legacy AC5, AC6; legacy section 14 |
| BR6 | A held business date is part of the contract: the read answers its status and the previous published date, so no reader infers a hold from a missing element | Legacy AC3; RWB-P10-E1063-CON |
| BR7 | The Schedule contract fixes one identity per business date for the daily rollup and the cost sweep, the 01:30 cadence, overlap policy SKIP, the catch-up window and the rerun rule, and never names the legacy job table or its admin read | DP-10; Arch v5 slides 31 and 44 |
| BR8 | The run read and the case agent-outputs read belong to the baseline; this document restates only the members this key reads and never declares them as its own | RWB-P10-E1063-CON; RWB-P10-E1058-CON; DP-13 |
| BR9 | No business value in the contract: the cost cap, the alert role, the drift values and the agent list are rows of the policy and of the reference data, and the contract only names them | §R7.2 s17; DP-07; DL33 |
| BR10 | One base and one topic per service: this contract declares `/api/recovery/agent/v1` and `rwb.agent.events.v1` for rwb-agent and never another service's path or topic as its own | DP-13; DP-14; Arch v5 slide 41 |
| BR11 | No lake table, extract, credential or file path is declared in any sub-table, because the data lake does not exist and the aggregate is served on the read | Arch v5 slide 37; ADR-018 |
| BR12 | Every consumed call is one hop with the 2 s client budget and a breaker per downstream | DP-11; ADR-020 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The read, the element, the restated reads, the boundary, the Schedule contract and the fakes are described | In review |
| In review | Consumer sign-off | The app, deployment, access, decision, reporting and communications slices accept the document and the fakes | Baselined |
| Baselined | Additive change | A member, a query parameter or a step is added without removing one | Baselined |
| Baselined | Breaking change to the read or to the element | A member of the element or a refusal code is removed, renamed or retyped | In review, with the owner of the affected contract |
| Baselined | The baseline changes a restated read | RWB-P10-E1063-CON publishes a new shape | Baselined, aligned to the baseline |
| Baselined | Drift in a fake, in the route or against the registration | A contract test fails | In review |

These are the states of this document, not of a case, a run or a business date. The run and date states themselves are COMPLETE, HELD and FAILED and belong to RWB-P10-E2031-APP; the document states of the version 1 read belong to RWB-P10-E1063-CON.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-agent | Owns the read shape, the element, the boundary, the Schedule contract, the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change to the read or to the element, and any change to the Schedule contract |
| The rwb-decision owner | Owns the decision log, the recommendation, the final call and the override reason, and signs off the shapes taken from `GET /decision-log` |
| The rwb-reporting owner | Owns the measure shapes and the published measures, and signs off the measure shape this contract reads |
| The rwb-case, rwb-comms and rwb-access owners | Own the consumed operations and the right of the read, and sign off the shapes taken from their documents |
| The app and deployment slices of this key | Review and accept the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the naming rule, the decision-record library and the workflow kit this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, a fake or a payload |

The identity that reads the decision log, the lists and the measures is the rwb-agent service identity (DP-02); its name is Not specified in the source documents (GAP-0630; ASM-0966) and is fixed with the deployment slice.

### 11. Data

The contract declares shapes, not business values.

| Item | Content |
|---|---|
| Metric query | agent, segment, version, from, to, with the declared page size and cursor |
| Version 1 members | agent, policyVersion, promptVersion, modelVersion, businessDate, runs, answered, fallback, fallbackRate, latencyP50Ms, latencyP95Ms, tokensIn, tokensOut, costThb, evalScore, acceptance, override |
| Version 2 members | segment, mode, acceptanceRate, correctionRate, overrideRate, overrideCount, decisionQualityScore, feedbackCount, reconciled, tokenDifference, driftThreshold, costCapThb |
| Held date status | businessDate, status COMPLETE, HELD or FAILED, publishedDate, the count-check result, the drift state |
| Override panel | the count per override reason code for an agent and a month, read from the decision-log page |
| Restated run read | AgentRun[] as baselined in RWB-P10-E1063-CON; the members this key reads are the run ID, the agent, the case, the status, the fallback, the latency, the cost, the run time and the segment |
| Restated case read | AgentOutput[] as baselined in RWB-P10-E1063-CON |
| Run event | `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1`, its envelope, its key and its payload as fixed by RWB-P10-E1063-CON; this document adds no member |
| Schedule contract | name, namespace, task queue, workflow identity, cadence, overlap policy, catch-up window, rerun rule, the four steps and the three run states |
| Consumed values | the recommendation, the final call, the override reason and the agent version through the decision-log read; LOV-PRODUCT, LOV-REGION, LOV-AGENT, LOV-AGENT-ALERT and LOV-ROLE through the reference-data read; the published measures through the measures read |
| Refusal | the platform problem response: status, code, detail, the message ID when a business message applies |

The page size, the cursor form, the exact types of the rate and amount members beyond four decimals and the reason codes of the override panel are Not specified in the source documents (GAP-0630; ASM-0971); this document fixes the member names and leaves the types to the review with their owners. No table of any schema is declared as an answer source: the read answers from `rwb_agent` and the measures from rwb-reporting (DP-01). No lake table is declared, because no data lake exists (BR11).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/api/recovery/agent/v1/admin/agent-metrics` | Read the agent measures per agent, policy version, prompt version, model version, segment and business date: query agent, segment, version, from and to with the declared paging; 200 AgentMetric[] with the version 1 members and the version 2 members of section 11; 422 on the two filter rules; a held date answers its status and its previous published date | The right of the read with scope applied; errors 401, 403, 422, 503 | Not applicable: the call writes nothing |

The run read `GET /api/recovery/agent/v1/admin/agent-runs` and the case read `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` are provided by rwb-agent and baselined in RWB-P10-E1063-CON; section 12 of that document owns their full shape. This contract restates only the members this key reads (12.2 of the baseline) and declares no other operation of its own.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this contract | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision (RWB-P7-E2005-CON) | The decision-quality and override read: the recommendation, the final call, the override reason, the agent version and the decided-at time of a date range, from which the override rate, the override count, the override panel and the decision-quality score are defined; the agent-version filter is Not specified in the source documents (GAP-0630; ASM-0960) | One hop, 2 s |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case (RWB-P3-E1043-CON) | LOV-PRODUCT, LOV-REGION, LOV-AGENT, LOV-AGENT-ALERT and LOV-ROLE with the version in force, checked before a segment filter is applied and before an alert row is written (DP-07) | One hop, 2 s |
| GET | `/api/recovery/reporting/v1/reports/measures` | P9 rwb-reporting | The published measures of a business date or a month, with their definition and their value, shown beside the aggregate | One hop, 2 s |
| POST | the rwb-comms notification operation: Not specified in the source documents (GAP-0630; ASM-0961) | P6 rwb-comms | The notice of MSG-P10-006 to the alert role and to the risk role, and the notice to the data steward of a held date | One hop, 2 s |

Every operation is one hop with the 2 s client budget and a breaker per downstream (BR12, DP-11 at the boundary, ADR-020). No parameter read is consumed by this key: DP-06 is not one of its patterns, the cap, the alert role and the drift values are approved rows of `agent_policy` in the service's own schema, and the two range limits are configuration values of the release (AC5). The delivery of a notice beyond rwb-comms is the contract RWB-P2-E1007-CON and is not called by this service.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload |
|---|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` (EV-28) | `rwb.agent.events.v1` with the retry topic and the `.dlt` topic | P10 | the case ID | run ID, agent_code, agent_version, prompt_version, model_version, case_id, autonomy_mode, trigger_event, status, fallback, confidence, latency_ms, tokens_in, tokens_out, cost_thb, run_at |

The event and its payload are fixed by RWB-P10-E1063-CON and published by the run path of RWB-P10-E1058-APP through the outbox relay; this document adds no member, because a drift alert is one `agent_alert` row and one notice and not an event, and LOV-AGENT-ALERT already holds COST_CAP and DRIFT.

#### 12.4 Events consumed

None. The read is answered on request from the rows of `rwb_agent` and the four boundaries of 12.2, and the rollup reads the same rows; no topic is consumed by this key on the agent side. The consumers of EV-28 are rwb-decision, rwb-document, rwb-deviation and rwb-reporting, and the projection rwb-reporting builds from it is its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunDailyRollupWorkflow | Workflow, one per business date, workflow ID = the business date | `rwb-agent` | Input: the business date, the requested-by role and the manual-start flag. Output: the run state COMPLETE, HELD or FAILED with the counts of the date and the drift state |
| aggregateAgentRuns | Activity, the daily rollup step | `rwb-agent` | Output: the daily element rows of the date per agent, version and segment, with the count-check result |
| raiseCostAlerts | Activity, the cost sweep step | `rwb-agent` | Output: the cost and token totals of the date and the month to date, the reconciled flag with the token difference, and the `agent_alert` rows of type COST_CAP on the unique key |
| agentDrift | Activity, the drift step | `rwb-agent` | Output: the `agent_alert` rows of type DRIFT on the unique key, and the segments not checked for want of feedback |
| dispatchAgentAlerts | Activity, the notice step | `rwb-agent` | Output: the notice requests and the outbox rows; no partial write |

The workflow identity, the queue and the namespace are the Schedule contract of 12.6; the step names are this story's and of the baseline, and the app slice accepts them.

#### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| AgentRunDailyRollup, carrying the daily rollup and the cost sweep | Daily at 01:30 Asia/Bangkok for the previous business date; overlap policy SKIP; catch-up window one business date; a manual start for any business date on the same identity; run states COMPLETE, HELD and FAILED; steps aggregateAgentRuns, raiseCostAlerts, agentDrift and dispatchAgentAlerts | Namespace `rwb-recovery`, task queue `rwb-agent`, registered and updated through RWB-PLT-E1071-CON by RWB-P10-E2031-OPS; the name is the baseline name and no second Schedule is declared (GAP-0630; ASM-0958) | The legacy Quartz entry of JOB-15 at 01:30 with its `agentRunDaily` and `agentDrift` steps (legacy sections 4 and 12) |

The cost sweep is the second step of the same run and not a second identity, because it reads the same business date, must share the overlap policy and the catch-up window of the rollup, and a rerun of the date must rewrite both together. The legacy job table, its admin read and its rerun operation are declared nowhere: a rerun is a manual start of the same workflow identity for the business date (DP-10; BR7).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| agent_alert | P10 (`rwb_agent`) | The COST_CAP and DRIFT rows the contract exposes through MSG-P10-006 and the held-date status; the unique key of agent, type, segment and date; created by the baseline migration, no column added |
| agent_run | P10 (`rwb_agent`) | The runs, the fallback, the latency, the tokens, the cost and the segment of the element; no column added |
| agent_feedback | P10 (`rwb_agent`) | The verdicts of the L1 output behind the acceptance and correction rates and the two 7-day windows; no column added |
| agent_policy | P10 (`rwb_agent`) | The mode, the segment, `watch_measures` and the alert role the element echoes; no column added |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | The outbox and idempotency envelope of the notices (DP-03, DP-09 at the library) |

No table of another service is declared and no foreign key crosses a schema (DP-01). The decision records are rwb-decision's, the lists and the parameters are rwb-case's and the measures are rwb-reporting's, and each is reached through its contract. The only schema change the app slice adds is the index migration `V10_007__agent_monitor_index.sql` in the rwb-agent Flyway sequence, which creates indexes and no column and touches no other schema (DP-15). No lake table, extract or file path is declared (BR11).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision WireMock | The decision records of an agent version over 2026-12-01 to 2026-12-14 with their recommendation, final call, override reason and decided-at time; an override reason code with its count; a page with no record for a segment; a 403; a delay beyond 2 s | Contract tests, app slice, decision slice |
| rwb-case WireMock | LOV-PRODUCT with MORTGAGE, LOV-REGION with BKK, LOV-AGENT with INTAKE and SCREENING, LOV-AGENT-ALERT with COST_CAP and DRIFT and LOV-ROLE with the alert and risk roles; a list that is not in force; a delay beyond 2 s | Contract tests, app slice |
| rwb-reporting WireMock | The published token and cost measures of November 2026 for INTAKE with their definition and their value; a measure that is not published for the date; a delay beyond 2 s | Contract tests, app slice, reporting slice |
| rwb-comms WireMock | An accepted notice with its reference for MSG-P10-006; a 503; an accepted notice for the data steward of a held date | Contract tests, app slice, communications slice |
| gateway-bff route stub | A pass-through route in front of the metric read, the run drill-down and the override panel, one hop, the JSON media type preserved and the refusal passed through unchanged | Contract tests, app slice, deployment slice |

The outbox stub, the workflow kit stub and the access guard stub are the platform's and are used but not declared here. Every fixture is synthetic and holds no personal data.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 2 restated and used, 4 consumed | The version 2 metric read provided; the run read and the case agent-outputs read restated from the baseline; the decision log, the lists, the measures and the notice consumed, one hop and 2 s each |
| Kafka | 1 published by the run path, 0 consumed | `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` with the retry and `.dlt` topics, keyed by the case ID; this document adds no member and no lake write |
| Temporal | 1 workflow, 4 activities, 1 Schedule | AgentRunDailyRollupWorkflow with aggregateAgentRuns, raiseCostAlerts, agentDrift and dispatchAgentAlerts on the queue `rwb-agent`, started by AgentRunDailyRollup at 01:30 |
| File | None | No file is read or written and no extract exists: the answer is the body of the read and the feed is the topic (BR11) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.agent.contract`, module `contract`, inside the rwb-agent service; the contract artefacts live under `contract/` of the service repository.

**Deliverables**

| Artefact | Content |
|---|---|
| `contract/agent-metric-read-v2.yaml` | The read, its five query parameters, its paging, its element, its two filter refusals, its held-date status and its refusal codes |
| `contract/agent-metric-element-v2.md` | The version 1 and version 2 members, their types, their sources and the rule that a member is removed only with a new major version |
| `contract/agent-admin-reads.md` | The run read and the case agent-outputs read restated from the baseline, with the members this key reads and the owner of the shape |
| `contract/agent-monitor-boundaries.md` | The decision-log read, the reference-data read, the measures read and the notification path, each with its budget, its breaker and its null rule; the parameter read named as not consumed |
| `contract/agent-rollup-schedule.md` | The Schedule contract: the name, the namespace, the queue, the identity, the cadence, the overlap policy, the catch-up window, the rerun rule, the four steps and the three run states |
| `contract/agent-monitor-route.md` | The gateway-bff route in front of the three reads and its one-hop rule |
| Four WireMock mappings with their fixtures | The answers, the errors and the timings of section 12.8 |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON for the app slice; C RWB-P7-E2005-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON for the app slice; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON for the app and deployment slices |
| DP-13 | `/api/recovery/` with one version segment for every module | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON for the app slice |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON for the app and deployment slices |

This story is Day 1 and holds no build dependency of its own (§R5.7): the platform contracts in the last column are the ones its consumers add, and the two C dependencies of the key are the published contracts of rwb-case and rwb-decision.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ContractSpecPublisher | Build step | Publishes the read, the element, the Schedule and the route documents and tags the baseline |
| ElementDiffCheck | Contract test | Applies BR2: compares the version 1 and version 2 members and fails a removal, a rename or a retype |
| BoundaryContractTest | Contract test | Applies BR3, BR12 and the null rule of AC4 against the four fakes |
| ScheduleContractTest | Contract test | Applies BR7 and AC6 against the workflow kit stub and the registration of the deployment slice |
| RouteContractTest | Contract test | Applies BR10 and AC7 against the route stub and the OpenAPI document of the read |
| LakeArtefactScan | Contract test | Applies BR11: fails a document or a fake that declares a lake table, an extract, a credential or a file path |

**Build steps**

1. Write the version 2 read contract with the five query parameters, the declared paging, the element and the four refusal codes (AC1).
2. Write the element document with the version 1 members, the version 2 members, their sources and the diff rule (AC2).
3. Write the boundary document with the decision-log read, the lists, the measures, the notice and the parameter read named as not consumed (AC4, AC5).
4. Write the Schedule contract with the four steps and the three run states, and the rule that the cost sweep shares the identity (AC6).
5. Restate the two baseline reads against RWB-P10-E1063-CON and mark the baseline as owner (AC3).
6. Write the route document and the route stub in front of the three reads (AC7).
7. Build the four WireMock mappings and their synthetic fixtures, including the null answer of the decision-log read and the 503 of the notice.
8. Add the contract tests of section 16, including the element diff, the Schedule and registration drift and the lake scan (AC8).
9. Tag the baseline and collect the sign-off of the app, deployment, decision, reporting and communications slices of this key.

**Done when.** The seven contract artefacts validate in the pipeline, the eight contract tests pass, the four fakes answer every consumed path and payload, no sub-table or fixture declares a lake artefact, and the app and deployment slices of this key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-006 | Acceptance falls by 10 points or more | {agent} acceptance for {segment} fell from {from} to {to} percent in the week to {date}. |
| MSG-GEN-003 | Filter dates in the wrong order | {field} cannot be before {other}. |
| MSG-GEN-002 | Filter range above 92 days | {field} must be between {min} and {max}. |
| MSG-GEN-001 | A required query member is empty or the paging is outside the declared range | Enter {field}. |
| MSG-P4-002 | A role without the right of the read calls the read | You cannot {action} here. Your role does not include it. |

The four business texts are the legacy messages of RWB-E2-031 and keep their wording character for character; MSG-GEN-001 is the platform message of an empty required field. This contract adds no message ID. In MSG-P10-006 the {agent} value is "INTAKE", {segment} is "MORTGAGE/BKK", {from} is 0.8600, {to} is 0.7500 and {date} is 2026-12-14. In MSG-GEN-002 {min} is 1 and {max} is 92. In MSG-GEN-003 {field} is "from" and {other} is "to". In MSG-P4-002 the {action} value is "read the agent monitoring dashboard".

### 15. Screens and states

No screen is declared in this story: SCR-46 Agent monitor belongs to RWB-P10-E2031-APP and the route that serves it belongs to RWB-PLT-N001-CON. The contract nevertheless fixes the four states every reader of the read relies on, so the app slice and the deployment slice name the same ones: loaded (the element rows of the latest published business date), empty (a date with no runs, answered as an empty page and never as an error), held business date (the status of the date with its previous published date and the count-check result), and error (a refusal or an unavailable store, answered with the platform problem response and its message ID). The two screen states of the key that are not a state of the read - not enough feedback and override unavailable - are carried as the drift state of the element and as a null override member with a reason code. The screen field list, its order and its masking rule belong to the app slice; the route path is Not specified in the source documents (GAP-0630; ASM-0967).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-E2031-CON-01 | AC1, BR1, BR5, BR10 | Contract | The read validated against its schema: the five query parameters, the declared paging, a request outside the range refused with 422 and MSG-GEN-001, the from-after-to refusal with MSG-GEN-003, the 92-day refusal with MSG-GEN-002 naming 1 and 92, and the four refusal codes |
| TC-P10-E2031-CON-02 | AC2, BR2, BR3, BR4 | Contract | The element of 2026-12-14: every version 1 member unchanged, the twelve version 2 members present, INTAKE 140 feedback with 119 accepted and 0.8500, the override rate and the decision-quality score at four decimals, and the null answer of the decision-log read with its reason code |
| TC-P10-E2031-CON-03 | AC3, BR8 | Contract | The run read and the case agent-outputs read against the baseline: query, answer, rights, errors, the members this key reads and the statement that the baseline owns the shape |
| TC-P10-E2031-CON-04 | AC4, BR3, BR12 | Contract | The decision-log read and the measures read at the boundary: one hop, the 2 s budget, a breaker, a refusal, a timeout and the null rule of both figures |
| TC-P10-E2031-CON-05 | AC5, BR9 | Contract | The reference-data read for the five lists with their version, a list that is not in force, and the parameter read absent from every sub-table |
| TC-P10-E2031-CON-06 | AC6, BR7 | Contract | The Schedule contract against the registration: the name, the namespace, the queue, the identity equal to the business date, the 01:30 cadence, SKIP, the catch-up window, the four steps, the three run states and the absence of a second Schedule |
| TC-P10-E2031-CON-07 | AC7, BR10 | Contract | The route stub in front of the three reads, one hop and the JSON media type preserved, and the four fakes answering every consumed path and payload |
| TC-P10-E2031-CON-08 | AC8, BR11 | Contract | The nine sub-tables and the fixtures scanned: no lake table, extract, credential, data-set job or file path, and a document that declares one failing the test |

The eight test cases are this story's own (D-RCV-60) and test the artefacts of the key rather than its business outcomes: the legacy test cases TC-E2-031-01 to TC-E2-031-08 stay with RWB-P10-E2031-APP and are not copied here. Every case is Level Contract, because each one proves a document, a fake or a registration and none proves a business figure.

### 17. Guardrails

- No business value in the contract: the cost cap, the alert role, the drift values, the agent list and the two range limits stay rows of the policy, of the reference data and of the configuration, and the contract only names them (BR9).
- No personal data in an event, an answer, an example or a fake: identifiers, counts, rates and amounts only, and every fixture is synthetic.
- The contract names the agent read and the agent topic as rwb-agent's and consumes every other operation and topic; a document that declares another service's path or topic as provided fails the review (DP-13, DP-14).
- No lake table, extract, credential, data-set job or file path is declared anywhere in this contract (BR11).
- The run read and the case agent-outputs read are restated, never redefined: the baseline owns them and a drift is corrected there (BR8).
- Every payload is validated against its registry subject before the relay, and a refusal is routed to `.dlt` and alerted.
- The Schedule contract never names the legacy job table, its admin read or its rerun operation, and declares no second identity for the cost sweep (BR7).
- Every consumed call is one hop with the 2 s budget and a breaker; no read of another service's table and no schema client exists in this key (BR12).
- Every fixture is synthetic; no production run, case, model answer, decision record or measure is copied into a schema, a payload or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-009 | Copied daily for reporting, with row counts matched (the legacy text names the data lake copy, which has no target; the copy becomes the event feed into rwb-reporting and the aggregate is served on the read) | The held-date status and the reconciled flag of the read, and the measures read at the boundary | TC-P10-E2031-CON-01, TC-P10-E2031-CON-02, TC-P10-E2031-CON-04 |
| REQ-APD-005 | An override of a recommendation needs a coded reason, and the reason is reported monthly | The overrideRate, overrideCount and decisionQualityScore members and the override panel of the decision-log read | TC-P10-E2031-CON-02, TC-P10-E2031-CON-04 |
| D-RCV-60 DP-03 | Local decision record plus central ledger | The decision-log read and the decision-record library the element depends on | TC-P10-E2031-CON-02, TC-P10-E2031-CON-04 |
| D-RCV-60 DP-07 | Reference data through the owner's contract | The reference-data read of the five lists | TC-P10-E2031-CON-05 |
| D-RCV-60 DP-10 | Temporal Schedules replace Quartz | The Schedule contract with its identity, its four steps and its rerun rule | TC-P10-E2031-CON-06 |
| D-RCV-60 DP-13 | One REST base per service | The base `/api/recovery/agent/v1` and the two restated reads | TC-P10-E2031-CON-01, TC-P10-E2031-CON-03 |
| D-RCV-60 DP-15 | Per-service Flyway and migration ownership | The index migration in the service's own sequence and the statement that no column is added | TC-P10-E2031-CON-02 |
| D-RCV-60 DP-19 | gateway-bff composite route | The route in front of the three reads and its one-hop rule | TC-P10-E2031-CON-07 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The provided read, the two restated reads, the four consumed boundaries and the fakes | TC-P10-E2031-CON-01, TC-P10-E2031-CON-04 |

The gap GAP-0630 records the areas the sources leave open for this contract - the decision-log filter and its override element, the notice operation, the name of the right, the paging and member types, the route path, the login and the Schedule step names - and each default it raises is settled by ASM-0958, ASM-0960, ASM-0961, ASM-0966, ASM-0967, ASM-0970 and ASM-0971.

### 19. Out of scope

- The implementation of the version 2 read, the drift check, the reconciliation, the alerts and the screen (RWB-P10-E2031-APP).
- The chart, the migration job, the worker, the Schedule registration, the contract wiring, the alerts, the route publication, the runbook and the rollback (RWB-P10-E2031-OPS).
- The whole monitoring baseline and the version 1 element, the run read, the case read and the publication of the run event (RWB-P10-E1063-CON, RWB-P10-E1058-APP).
- The decision log, the recommendation, the final call, the override reason and the decision-quality record (P7 rwb-decision, RWB-P7-E2005-CON).
- The reference lists and the parameter values themselves (rwb-case), and the right of the read (rwb-access).
- The measure definitions, the projections, the snapshots and the published measures (P9 rwb-reporting), and the steering dashboard of RWB-E2-009.
- The notification path, the message template and the delivery of MSG-P10-006 (rwb-comms), and the delivery beyond it (RWB-P2-E1007-CON).
- The evaluation harness and the score rows (RWB-P10-E1060-APP, RWB-P10-E1061-CON), and the recording of the L1 verdict (RWB-P10-E2028-APP, RWB-P10-E2029-APP).
- The screen field list and the composite route specification of SCR-46 (the app slice and the edge story).
- The end-to-end proof across services (RWB-ITG-E2031-ITG).
- Any lake table, extract, lake credential or lake path, of which none is declared (BR11; GAP-0630).

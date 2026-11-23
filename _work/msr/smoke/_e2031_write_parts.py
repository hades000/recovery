import json, os

gaps = [
 {
  "id": "CG-B-P10-02-E2031-1",
  "title": "The app slice of the agent monitoring dashboard v2: the drift step's place, the segment on the run row, the decision-log filter and elements, the notice operation, the policy values, the migration number, the range limits, the login, the route path and the name of the right are not fixed by any source",
  "source": "Legacy story RWB-E2-031 sections 2, 3, 4, 5, 7, 11, 12, 13 and 15; FSD P10 Agent runtime v3 A2.6 (FEAT-AGT-06); TSD P10 Agent runtime v2 T3.1, T3.2, T6.1 and T-A.1 to T-A.2 (API-P10-009); Architecture v5 Text Extract v1 slides 13 to 20 and 41 to 44; Ownership Map v1 (eight P10 tables, eleven P10 operations, EV-28, AgentRunWorkflow); Template and Rules v1 §R4, §R5.5, §R7.3 and §R9; the published contracts of RWB-P10-E1063-CON and RWB-P7-E2005-CON",
  "section": "3. Preconditions; 5. Exception paths; 7. Acceptance criteria AC1 to AC7; 9. State transitions; 10. Authority; 11. Data; 12.1; 12.2; 12.5; 12.6; 13. Solution plan; 15. Screens and states",
  "description": "Nine values the app slice needs are absent from the sources or disagree between them, and none may be invented. (1) The drift check: the legacy story puts the step agentDrift after agentRunDaily inside JOB-15 at 01:30, no source names a Schedule for it in the target, and JOB-15 is the reporting extract of rwb-reporting in the job map, so the place of the step in the target is a decision. (2) The segment: the legacy story reads recovery_case.product_group and recovery_case.region_code, the target carries the same facts on the run row as DF-AGT-059 and DF-AGT-060, and no source states that this story reads them only and never the case table. (3) The override figures: the legacy P7 query interface DecisionLogQuery.byAgentVersion(agentVersion, from, to) becomes the rwb-decision contract of RWB-P7-E2005-CON, which declares the query parameters caseId, caseIds, decision, ruleId, ruleVersion, approver, from, to, page and size and the answer elements of the audit read, and declares no filter on the agent version and none of recommendation, final_call and override_reason that the override rate and the override reasons need. (4) The notice: no source names the operation of the rwb-comms notification path. (5) The policy values: the legacy story assumes drift_points 10 and a minimum of 20 feedback entries per week and segment, adds no window length, and no source states the key, the shape or the loading of agent_policy.watch_measures beyond the field DF-AGT-019. (6) The migration: only V10_001 of the service is named by a source, and the legacy migration V10_007 adds two segment columns that TSD P10 v2 T3.1 already declares, so the number, the content and the index names of the migration are open. (7) The limits: MSG-GEN-002 names 1 and 92 days and no source names the parameter key that holds them. (8) The login: DP-02 requires one login per service and no source names it. (9) The route: the gateway-bff route in front of SCR-46 and the read has no name and no path. One conflict is recorded here: the read is authorised under Platform administration R in the legacy story section 12 and TSD P10 v2 T6.1, and under Rules and parameters R in TSD P10 v2 T-A.1 API-P10-009.",
  "evidence": "Legacy RWB-E2-031 section 3 ('RWB-E1-063 is done: agent_run_daily is written by JOB-15', 'RWB-E2-005 is done: the P7 decision log query interface', 'each L1 policy holds watch_measures with drift_points 10 (assumed) and minimum feedback 20 per week per segment (assumed)'), section 4 step 5 ('JOB-15 Reporting extract: after the daily rows, runs the drift check'), section 12 ('GET /api/recovery/v1/admin/agent-metrics', 'Job: JOB-15 ... this story adds step agentDrift after agentRunDaily', 'Interface called: P7 DecisionLogQuery.byAgentVersion(agentVersion, from, to)'), section 13 ('migration V10_007__agent_run_segment.sql adds segment_product_group varchar(15) and segment_region_code varchar(10) to agent_run'), section 14 (MSG-GEN-002 'naming 1 and 92 days'); TSD P10 Agent runtime v2 T3.1 (DF-AGT-059, DF-AGT-060, DF-AGT-019), T6.1 (Platform administration R), T-A.1 API-P10-009 (Rules and parameters R) and T-A.2 API-P10-009; Architecture v5 Text Extract v1 slide 44 (JOB-15 Reporting extract, owner rwb-reporting) and slide 16 (P10 contracts); RWB-P7-E2005-CON section 12.1 and its data table (the ten query parameters and the eleven audit elements); Template and Rules v1 §R5.5 DP-02, DP-03, DP-07, DP-10 and DP-13.",
  "type": "Missing",
  "area": "Application",
  "severity": "P2",
  "needed_by_wave": 2,
  "legacy_ref": "RWB-E2-031",
  "owner_role": "Solution architect",
  "asm": "ASM-B-P10-02-E2031-1, ASM-B-P10-02-E2031-2, ASM-B-P10-02-E2031-3, ASM-B-P10-02-E2031-4, ASM-B-P10-02-E2031-5, ASM-B-P10-02-E2031-6, ASM-B-P10-02-E2031-9, ASM-B-P10-02-E2031-10, ASM-B-P10-02-E2031-11, ASM-B-P10-02-E2031-13",
  "proposed": "Put the drift step in the workflow of the v1 Schedule rather than in a new one; read the segment from the run row; read the override figures through the rwb-decision contract with the agent-version filter and the three elements added as an additive change; name the notice path by its owner; hold the policy values in watch_measures; name the migration V10_007 with the legacy index and one index on agent_feedback; hold the two range limits as configuration; name the login 'the rwb-agent login (DP-02)'; register the screen route under RWB-PLT-N001-CON; and take the right of API-P10-009 as the declaring source while recording the legacy name.",
  "wp": "B-P10-02"
 },
 {
  "id": "CG-B-P10-02-E2031-2",
  "title": "The contract slice of the agent monitoring dashboard v2: the member types of the v2 element, the paging, the names of the drift inputs, the agent-version filter, the notice operation and the route path are not fixed by any source",
  "source": "Legacy story RWB-E2-031 sections 7, 11 and 12; FSD P10 Agent runtime v3 A2.6; TSD P10 Agent runtime v2 T3.1, T3.2 and T-A.2 API-P10-009; Architecture v5 Text Extract v1 slides 41 to 44; the published contracts of RWB-P10-E1063-CON and RWB-P7-E2005-CON; Template and Rules v1 §R4, §R5.5 and §R9",
  "section": "3. Preconditions; 5. Exception paths; 7. Acceptance criteria AC1 to AC6; 10. Authority; 11. Data; 12.1; 12.2; 12.5; 12.6; 12.8; 13. Solution plan",
  "description": "Six elements of the v2 contract are open in the sources. (1) The element types: TSD P10 v2 T-A.2 gives only the names of AgentMetric[] and no type or length for members beyond four decimals, and the legacy section 12 gives one flat list of names with no type at all. (2) The paging: the legacy section 12 declares no page size and the v1 contract fixed the paging of the same read, so v2 must not respecify it and cannot derive it. (3) The names of the drift inputs and of the verdict members of the element are not fixed by any source, although DF-AGT-019 declares watch_measures as jsonb and DF-AGT-100 declares the verdict list. (4) The agent-version filter of the decision-log read and the three elements the override figures need are not declared by RWB-P7-E2005-CON, so the consumed side of the contract cannot be completed from a source. (5) The operation of the rwb-comms notification path is named by no source. (6) The gateway-bff route in front of the read and the override panel has no name and no path. The contract fixes the member names and leaves the types to the review with their owners, which is the only position the sources support.",
  "evidence": "Legacy RWB-E2-031 section 12 ('Response: 200, array of AgentMetric (agent, policyVersion, promptVersion, modelVersion, segment, mode, date, runs, fallbackRate, acceptanceRate, correctionRate, overrideRate, feedbackCount, latencyP50Ms, latencyP95Ms, tokens, costThb, reconciled)'), section 11 (the DF ids of decision_log_entry and agent_alert); TSD P10 Agent runtime v2 T-A.2 API-P10-009 ('Response AgentMetric[]', 'Request Query: agent, segment, version, from, to'), T3.1 (DF-AGT-019 watch_measures jsonb, DF-AGT-100 verdict LOV-FEEDBACK) and T3.2 (LOV-AGENT-ALERT COST_CAP and DRIFT); RWB-P7-E2005-CON section 12.1 and its data table; Architecture v5 Text Extract v1 slide 41 (naming notes) and slide 43 (EV-28); Template and Rules v1 §R4.",
  "type": "Missing",
  "area": "Contract",
  "severity": "P2",
  "needed_by_wave": 2,
  "legacy_ref": "RWB-E2-031",
  "owner_role": "Tech lead of rwb-agent",
  "asm": "ASM-B-P10-02-E2031-1, ASM-B-P10-02-E2031-2, ASM-B-P10-02-E2031-3, ASM-B-P10-02-E2031-4, ASM-B-P10-02-E2031-5, ASM-B-P10-02-E2031-7, ASM-B-P10-02-E2031-8, ASM-B-P10-02-E2031-10, ASM-B-P10-02-E2031-11",
  "proposed": "Fix the seven added member names, their four-decimal rule and the additive rule of major version 1; keep the paging and the held-date status of RWB-P10-E1063-CON unchanged; name the drift inputs after the watch_measures members; declare the agent-version filter and the three elements of the decision record as an additive change of the rwb-decision contract; name the notice path by its owner; and register the route under RWB-PLT-N001-CON.",
  "wp": "B-P10-02"
 },
 {
  "id": "CG-B-P10-02-E2031-3",
  "title": "The deployment slice of the agent monitoring dashboard v2: the topology, alert thresholds, login, route path, the Schedule update path and the consumer group ownership are not specified",
  "source": "Legacy story RWB-E2-031 sections 3, 4, 5, 12 and 13; Architecture v5 Text Extract v1 slides 16, 20, 37, 41 and 44; TSD P10 Agent runtime v2 T6.2 and T7; the published contracts of RWB-P10-E2031-CON; Template and Rules v1 §R4, §R5.5 and §R9",
  "section": "3. Preconditions; 5. Exception paths; 7. Acceptance criteria AC1 to AC6; 10. Authority; 11. Data; 12.2; 12.6; 13. Solution plan; 19. Out of scope",
  "description": "Six deployment values of this key are absent from every source. (1) The login: DP-02 requires one login per service and no source names the rwb-agent login, the ACE database administrator's grants or the secret entry. (2) The route: the gateway-bff route in front of the v2 read and the override panel has no name and no path, and the edge story owns the specification. (3) The alert thresholds: no source gives a threshold, a window or a percentile for the sent-empty, short-week, unreconciled-month or step-not-run alerts, and no measurement point is named for the 2 s client budget. (4) The topology: cluster names, node pools, replica counts, resource sizes, probe timings, the host, the SKU and the budget are absent. (5) The Schedule update path: the v1 release registered AgentRunDailyRollup and no source states how the added step is re-registered without creating a second Schedule or a second run. (6) The consumer group: the group of rwb.agent.events.v1 belongs to rwb-reporting and no source states what the agent release verifies about it. Retention and partition values of the topic are likewise unstated and are not invented here.",
  "evidence": "Legacy RWB-E2-031 section 12 (the job and its idempotency key), section 13 (the feature flag rwb.agent.monitor-v2 and the migration); Architecture v5 Text Extract v1 slide 41 ('schema rwb_<name> with its own login; REST under /api/recovery/<name>/v1 behind gateway-bff; Kafka topic rwb.<name>.events.v1; Temporal task queue rwb-<name> in namespace rwb-recovery') and slide 44 (Schedule with overlap policy SKIP and catch-up window); TSD P10 Agent runtime v2 T6.2 (service identities) and T7 (NFR-008, NFR-010); Template and Rules v1 §R4 and §R5.5 DP-02, DP-03, DP-10 and DP-19.",
  "type": "Missing",
  "area": "Operations",
  "severity": "P3",
  "needed_by_wave": 2,
  "legacy_ref": "RWB-E2-031",
  "owner_role": "Platform administrator",
  "asm": "ASM-B-P10-02-E2031-1, ASM-B-P10-02-E2031-4, ASM-B-P10-02-E2031-6, ASM-B-P10-02-E2031-9, ASM-B-P10-02-E2031-10, ASM-B-P10-02-E2031-12",
  "proposed": "Reference the login through a secret reference and name it 'the rwb-agent login (DP-02)'; register the route under RWB-PLT-N001-CON and leave its path to the edge story; expose every threshold and topology value as a chart value with a name and the rule that it is not hard-coded; update the Schedule in place and verify the two steps on one workflow identity; and verify the consume right of rwb-reporting without creating its consumer group.",
  "wp": "B-P10-02"
 }
]

asm = [
 {
  "id": "ASM-B-P10-02-E2031-1",
  "text": "The legacy step agentDrift of JOB-15 becomes the activity agentDrift of the workflow AgentRunDailyRollupWorkflow, run after the activity aggregateAgentRuns (the legacy agentRunDaily step) inside the workflow identity of the business date, under the Schedule AgentRunDailyRollup that RWB-P10-E1063-OPS registered in namespace rwb-recovery on the task queue rwb-agent at 01:30 Asia/Bangkok with overlap policy SKIP and the one-business-date catch-up window. No separate Schedule, no Quartz entry and no shared job table is created, and a rerun is a manual start of the same identity.",
  "why": "The legacy story adds the step agentDrift to JOB-15 after agentRunDaily at 01:30; Architecture v5 slide 44 gives JOB-15 to rwb-reporting as a reporting extract with no data lake, and DP-10 moves overnight work to a Temporal Schedule of the owning service; no source names a Schedule for a drift check.",
  "read": "Legacy RWB-E2-031 section 4 step 5 and section 12 (the job, the step order and the restart rule); Architecture v5 Text Extract v1 slide 44 (job map) and slide 31; Template and Rules v1 §R5.5 DP-10",
  "gap": "CG-B-P10-02-E2031-1",
  "applied_in": "RWB P10 E2031 APP: section 2, section 4, section 8 BR7, section 12.5, section 12.6, section 13; RWB P10 E2031 CON: section 7 AC5, section 12.5, section 12.6; RWB P10 E2031 OPS: section 4 step 4, section 7 AC3, section 12.6, section 13",
  "confidence": "High",
  "confirm": "Solution architect with the DevOps team at the wave 2 build start",
  "impact": "If a separate Schedule is wanted, it is a second registration on the same queue with the same cadence; the workflow, the activity, the alert row and the read do not change.",
  "wp": "B-P10-02"
 },
 {
  "id": "ASM-B-P10-02-E2031-2",
  "text": "The segment of a metric row is read from agent_run.segment_product_group and agent_run.segment_region_code (DF-AGT-059, DF-AGT-060), which the run path of RWB-P10-E1058-APP sets at run time from the case read, so this story reads its own table and never reads rwb_case.product_group or rwb_case.region_code.",
  "why": "The legacy story reads recovery_case.product_group and recovery_case.region_code and also writes the same facts on the run row; TSD P10 Agent runtime v2 T3.1 declares both members on agent_run and the Ownership Map gives agent_run to P10 and the case to P3.",
  "read": "Legacy RWB-E2-031 section 8 BR6 and section 11 (DF-AGT-059, DF-AGT-060); TSD P10 Agent runtime v2 T3.1; Architecture v5 Text Extract v1 slide 16; Ownership Map v1 (agent_run owner P10)",
  "gap": "CG-B-P10-02-E2031-1",
  "applied_in": "RWB P10 E2031 APP: section 2, section 3, section 8 BR6, section 11; RWB P10 E2031 CON: section 7 AC2, section 8 BR7",
  "confidence": "High",
  "confirm": "Tech lead of rwb-agent with the owner of RWB-P10-E1058-APP at the wave 2 build start",
  "impact": "If the run row carries no segment for an older run, that run is grouped under an empty segment and shown as such; no case table is read and no value is invented.",
  "wp": "B-P10-02"
 },
 {
  "id": "ASM-B-P10-02-E2031-3",
  "text": "The override rate and the override reasons are read through the rwb-decision decision-log read of RWB-P7-E2005-CON, and the contract gains a filter on the agent version and the elements recommendation, final call and override reason as an additive change within its major version 1, agreed with its owner; until it is published the v2 fakes supply them. The legacy read DecisionLogQuery.byAgentVersion(agentVersion, from, to) is that read.",
  "why": "The legacy story reads decision_log_entry through the P7 query interface; the target ledger is rwb-decision's, and the published contract declares neither the agent-version filter nor the three elements the override figures need.",
  "read": "Legacy RWB-E2-031 section 8 BR2, section 11 (DF-DEC-007, 009, 012, 013 and 016) and section 12 (the interface called); RWB-P7-E2005-CON section 7 AC2 and AC3, section 11 and section 12.1; Template and Rules v1 §R5.5 DP-03 and DP-11",
  "gap": "CG-B-P10-02-E2031-1",
  "applied_in": "RWB P10 E2031 APP: section 2, section 3, section 4 step 9, section 7 AC1, section 8 BR2, section 12.2, section 12.8, section 13; RWB P10 E2031 CON: section 7 AC1 and AC6, section 8 BR3, section 12.2; RWB P10 E2031 OPS: section 12.2",
  "confidence": "Medium",
  "confirm": "Solution architect with the rwb-decision owner at the wave 2 contract freeze",
  "impact": "If the filter is refused, the read pages by date and filters on the answer, which costs more calls at the same 2 s budget; the element and its rates do not change.",
  "wp": "B-P10-02"
 },
 {
  "id": "ASM-B-P10-02-E2031-4",
  "text": "MSG-P10-006 leaves through the rwb-comms notification path, whose operation path no source names; the notice request is written to the outbox in the same transaction as the agent_alert row, sent_at stays empty until the path accepts it, and a permanent failure is routed to the .dlt topic with an alert. A DRIFT alert publishes no event on the agent topic.",
  "why": "The legacy story sends the drift message through the P6 notification interface of the same deployment; in the target the notification path is rwb-comms's and the retry is the platform outbox, and no source names the operation.",
  "read": "Legacy RWB-E2-031 section 4 step 6, section 12 (MSG-P10-006 through the P6 notification interface) and section 14; Architecture v5 Text Extract v1 slide 17 (rwb-comms POST /notices) and slide 42 (the outbox note); Template and Rules v1 §R5.5 DP-09",
  "gap": "CG-B-P10-02-E2031-1",
  "applied_in": "RWB P10 E2031 APP: section 2, section 4 step 7, section 12.2, section 12.3, section 12.8; RWB P10 E2031 CON: section 3, section 7 AC6, section 12.2; RWB P10 E2031 OPS: section 3, section 12.2, section 12.8",
  "confidence": "Medium",
  "confirm": "Tech lead of rwb-agent with the rwb-comms owner at the wave 2 contract freeze",
  "impact": "If the path answers with a queued reference rather than a delivered one, sent_at follows the accepted reference and the delivered proof stays rwb-comms's; the alert row does not change.",
  "wp": "B-P10-02"
 },
 {
  "id": "ASM-B-P10-02-E2031-5",
  "text": "The drift rule is held in agent_policy.watch_measures (DF-AGT-019) as drift_points 10, min_feedback 20 and window_days 7 (assumed values, as the legacy story assumes 10 and 20 and adds no window), loaded by RW-COE and approved by RW-RISK; both weeks are 7 calendar days ending on the business date, so the earlier week is days 8 to 14 back, the threshold of the alert is the acceptance of the earlier week less 10 points (0.8600 less 0.10 = 0.7600), and a fall of exactly 10 points raises the alert.",
  "why": "The legacy story states drift_points 10 and a minimum of 20 feedback entries as assumed values of watch_measures and describes the two weeks without a length; DF-AGT-019 declares the field as jsonb and no source gives its members.",
  "read": "Legacy RWB-E2-031 section 3, section 4 step 5, section 7 AC2 and AC4, section 8 BR3 and section 13 (watch_measures drift_points 10, min_feedback 20, window_days 7); TSD P10 Agent runtime v2 T3.1 (DF-AGT-019); Template and Rules v1 §R5.5 DP-06 as the ruling that moves parameters to rwb-case, read here from the policy row",
  "gap": "CG-B-P10-02-E2031-1",
  "applied_in": "RWB P10 E2031 APP: section 3, section 4 step 5, section 7 (Target reading), section 8 BR3, section 13; RWB P10 E2031 CON: section 7 AC3, section 8 BR7, section 11; RWB P10 E2031 OPS: section 3, section 11",
  "confidence": "Medium",
  "confirm": "RW-COE with RW-RISK at the loading of the L1 policies in SIT",
  "impact": "A different window or threshold changes the numbers of the alert and the fixture only; the shape of the row, the notice and the screen do not change.",
  "wp": "B-P10-02"
 },
 {
  "id": "ASM-B-P10-02-E2031-6",
  "text": "The migration of this story is V10_007__agent_monitor_index.sql in the rwb-agent Flyway sequence: it creates the index ix_agent_run_segment on agent_run (agent_code, segment_product_group, segment_region_code, run_at) that the legacy migration named, and one index over agent_feedback (created_at) for the two 7-day windows, and it creates no table. The two segment columns the legacy migration also added arrive with the runtime migrations of RWB-P10-E1058-APP, because TSD P10 Agent runtime v2 T3.1 already declares DF-AGT-059 and DF-AGT-060.",
  "why": "Only V10_001 of the service is named by a source, the legacy migration V10_007 adds two columns that the TSD already declares, and no source names an index on agent_feedback.",
  "read": "Legacy RWB-E2-031 section 13 ('migration V10_007__agent_run_segment.sql adds segment_product_group ... with index (agent_code, segment_product_group, segment_region_code, run_at)'); TSD P10 Agent runtime v2 T3.1 (DF-AGT-059, DF-AGT-060) and section T2; Template and Rules v1 §R5.5 DP-15",
  "gap": "CG-B-P10-02-E2031-1",
  "applied_in": "RWB P10 E2031 APP: section 8 BR11, section 12.7, section 13; RWB P10 E2031 OPS: section 4 step 2, section 7 AC1, section 12.7, section 13",
  "confidence": "Medium",
  "confirm": "ACE database administrator with the tech lead of rwb-agent at the wave 2 build start",
  "impact": "If the earlier migrations already hold the index, the migration is a no-op and the sequence records it; no table and no column is created twice.",
  "wp": "B-P10-02"
 },
 {
  "id": "ASM-B-P10-02-E2031-7",
  "text": "The v2 element is an additive change within major version 1 of the read that RWB-P10-E1063-CON fixed: it adds segment, mode, acceptanceRate, correctionRate, overrideRate, feedbackCount and reconciled and removes, renames and retypes no v1 member; the member types beyond four decimals, the paging and the held-date status stay as that contract fixed them, and the drift inputs take the member names of watch_measures.",
  "why": "The legacy response list of section 12 is a flat list of names with no type, TSD P10 v2 T-A.2 gives only AgentMetric[], and the v1 contract of the same read already fixed its paging and its held-date status.",
  "read": "Legacy RWB-E2-031 section 12; TSD P10 Agent runtime v2 T-A.2 API-P10-009; RWB-P10-E1063-CON section 11 and section 12.1; Template and Rules v1 §R5.5 DP-13",
  "gap": "CG-B-P10-02-E2031-2",
  "applied_in": "RWB P10 E2031 APP: section 3, section 8 BR8, section 12.1; RWB P10 E2031 CON: section 7 AC2, section 8 BR2, section 11",
  "confidence": "High",
  "confirm": "Tech lead of rwb-agent with the app story at the wave 2 contract freeze",
  "impact": "If a v1 member must change type, the read raises major version 2 and the screen and the integration copy follow it; no other element changes.",
  "wp": "B-P10-02"
 },
 {
  "id": "ASM-B-P10-02-E2031-8",
  "text": "The state of an agent and segment on SCR-46 is the mode of the approved policy row: agent_policy.autonomy_mode (DF-AGT-008) SHADOW is shown as Shadow, L1 as live and OFF as paused, and a segment with no policy row of its own takes the mode of the policy row whose segment is empty.",
  "why": "The legacy story shows the state words Shadow, live and paused and reads agent_policy.autonomy_mode and the policy segment, but no source maps a code to a word or says how a segment without a policy row is shown.",
  "read": "Legacy RWB-E2-031 section 4 step 4, section 7 AC1, section 11 (DF-AGT-008, DF-AGT-009, DF-AGT-010) and section 15; TSD P10 Agent runtime v2 T3.1 and T3.2 (LOV-AUTONOMY OFF, SHADOW, L1)",
  "gap": "CG-B-P10-02-E2031-2",
  "applied_in": "RWB P10 E2031 APP: section 4 step 4, section 9, section 15; RWB P10 E2031 CON: section 7 AC2",
  "confidence": "High",
  "confirm": "RW-COE at the SIT walkthrough of SCR-46",
  "impact": "If a different word is wanted, only the display text changes; the policy row, the read and the alert do not change.",
  "wp": "B-P10-02"
 },
 {
  "id": "ASM-B-P10-02-E2031-9",
  "text": "The per-service login of rwb-agent under DP-02 is not named by any source; the stories name it 'the rwb-agent login (DP-02)', with grants on schema rwb_agent only and the naming taken from the platform at build time, and the chart references it through a secret reference rather than a literal.",
  "why": "Template and Rules §R4 and DP-02 require one login per service, TSD P10 v2 T6.2 speaks of service identities, and no source names the login, its grants or its secret entry.",
  "read": "Template and Rules v1 §R4 and §R5.5 DP-02; TSD P10 Agent runtime v2 T6.2; Architecture v5 Text Extract v1 slide 41 and its note ('schema rwb_<name> with its own login')",
  "gap": "CG-B-P10-02-E2031-1",
  "applied_in": "RWB P10 E2031 APP: section 10; RWB P10 E2031 CON: section 10; RWB P10 E2031 OPS: section 10",
  "confidence": "High",
  "confirm": "DevOps team with the ACE database team at the wave 2 build start",
  "impact": "Only the identity name in the configuration, the grants and the tests; no business value, table or message changes.",
  "wp": "B-P10-02"
 },
 {
  "id": "ASM-B-P10-02-E2031-10",
  "text": "SCR-46 and the v2 read are reached through the gateway-bff composite route of RWB-PLT-N001-CON, one hop; the route that carries the read, the run drill-down and the override panel has no name and no path in any source, and its specification and its path are the edge story's.",
  "why": "DP-19 moves a screen behind a gateway-bff composite route, the legacy story is a monolith screen that calls the endpoint directly, and no source names the route of this screen.",
  "read": "Legacy RWB-E2-031 section 4 step 1 and section 15 (SCR-46 from the Administration menu); Architecture v5 Text Extract v1 slide 41 ('REST under /api/recovery/<name>/v1 behind gateway-bff'); Template and Rules v1 §R5.5 DP-19",
  "gap": "CG-B-P10-02-E2031-1",
  "applied_in": "RWB P10 E2031 APP: section 2, section 15; RWB P10 E2031 CON: section 7 AC1, section 8 BR10, section 15; RWB P10 E2031 OPS: section 7 AC5, section 15",
  "confidence": "Medium",
  "confirm": "Solution architect with the edge owner at the wave 2 contract freeze",
  "impact": "Only the route name and path in the configuration and the tests; the read, the answer and the screen fields do not change.",
  "wp": "B-P10-02"
 },
 {
  "id": "ASM-B-P10-02-E2031-11",
  "text": "The screen range is 1 to 92 days, as MSG-GEN-002 states, and the two limits are configuration values of the service rather than literals in code; no source names the parameter key that holds them, and a from after a to is refused before the range is measured.",
  "why": "The legacy story refuses a range above 92 days with MSG-GEN-002 naming 1 and 92 and refuses a from after a to with MSG-GEN-003, and no source states where the two limits are held or in which order the two checks run.",
  "read": "Legacy RWB-E2-031 section 5 X2 and X3, section 7 AC5 and AC6 and section 14 (MSG-GEN-003, MSG-GEN-002); FSD P10 Agent runtime v3 A2.6 VR-P10-006-1",
  "gap": "CG-B-P10-02-E2031-1",
  "applied_in": "RWB P10 E2031 APP: section 8 BR10, section 13; RWB P10 E2031 CON: section 7 AC1, section 8 BR4, section 11",
  "confidence": "Medium",
  "confirm": "Tech lead of rwb-agent with the platform configuration owner at the wave 2 build start",
  "impact": "If the limits are held as parameters of rwb-case, the read gains one consumed operation and the message values do not change.",
  "wp": "B-P10-02"
 },
 {
  "id": "ASM-B-P10-02-E2031-12",
  "text": "The deployment topology (cluster, node pools, replica counts, resource sizes, zone spread, ingress class, probe paths and timings), the alert thresholds and the window of the sent-empty alert, the host, the SKU and the budget of the release are not specified by any source; the chart and the alert rules expose them as values, and this story fixes only their names and the rule that they are not hard-coded.",
  "why": "No source carries an environment value for this release, and Template and Rules §R7.2 s17 forbids a business or environment value in the chart.",
  "read": "Architecture v5 Text Extract v1 slide 41 (naming only); TSD P10 Agent runtime v2 T7 (NFR-008, NFR-010 as targets with no measurement point); Template and Rules v1 §R7.2 s17 and §R9",
  "gap": "CG-B-P10-02-E2031-3",
  "applied_in": "RWB P10 E2031 OPS: section 7 AC6, section 11, section 13",
  "confidence": "High",
  "confirm": "Release manager with the platform administrator before the SIT promotion",
  "impact": "Only the values files and the alert rules; no business value, contract element or message changes.",
  "wp": "B-P10-02"
 },
 {
  "id": "ASM-B-P10-02-E2031-13",
  "text": "The metric read is authorised under Rules and parameters R with the scope applied, as TSD P10 Agent runtime v2 T-A.1 API-P10-009 declares; the legacy story and TSD P10 v2 T6.1 name Platform administration R for the same roles, the two names are read as one right of the same roles, and the refusal is MSG-P4-002 either way. The check is rwb-access's and this story proves the refusal through the route.",
  "why": "Two sources of different precedence disagree on the capability area of API-P10-009, R-PREC puts the TSD above the story master, and the legacy screen and its access test use the other name.",
  "read": "Legacy RWB-E2-031 section 3 ('The user holds Platform administration R'), section 5 X6, section 10 and section 16 TC-E2-031-08; TSD P10 Agent runtime v2 T-A.1 API-P10-009 ('Rules and parameters R') and T6.1 (Platform administration R for RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM and RW-SECADM); Template and Rules v1 §R3",
  "gap": "CG-B-P10-02-E2031-1",
  "applied_in": "RWB P10 E2031 APP: section 3, section 8 BR12, section 12.1; RWB P10 E2031 CON: section 7 AC1",
  "confidence": "Medium",
  "confirm": "Solution architect with the rwb-access owner at the wave 2 contract freeze",
  "impact": "If the right is renamed, one row of the access matrix and the message text change; the refusal code and the test do not.",
  "wp": "B-P10-02"
 }
]

gp = r"_work/msr/gaps/B-P10-02-E2031.part.jsonl"
ap = r"_work/msr/assumptions/B-P10-02-E2031.part.jsonl"
with open(gp, "w", encoding="utf-8", newline="\n") as f:
    for r in gaps:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
with open(ap, "w", encoding="utf-8", newline="\n") as f:
    for r in asm:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("gaps", len(gaps), "asm", len(asm))
for p in (gp, ap):
    n = 0
    for line in open(p, encoding="utf-8"):
        if line.strip():
            json.loads(line)
            n += 1
    print(p, "valid rows", n)

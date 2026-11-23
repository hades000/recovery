import json
from pathlib import Path

WP = "B-P10-02"
K = "E2029"
G = f"CG-{WP}-{K}-1"
G2 = f"CG-{WP}-{K}-2"

rows = [
 ("1", "The per-service login of rwb-agent is not named by any source; the story names it \"the rwb-agent login (DP-02)\" until it is agreed, and SY-AGENT stays the actor name of the run",
  "DP-02 requires one login per service and no source names the rwb-agent login string", "Template and Rules v1 R4 and R5.5 DP-02; Ownership Map v1 service table; no login name in any P10 source",
  G, "3 Preconditions; 10 Authority; 13 Solution plan", "Medium", "DevOps with the DBA who owns the ACE logins", "The login string is settled before the wave 2 build; until then the story and the fakes use the phrase \"the rwb-agent login (DP-02)\""),
 ("2", "The rwb-deviation raise is consumed as a REST contract with a mock, one hop and a 2 s budget; the S8 story that publishes the raise is not named by any source",
  "The legacy story raised a deviation through an in-process DeviationService; DP-11 replaces it with a one-hop REST contract and no source names the S8 slice story",
  "Legacy RWB-E2-029 section 12 (DeviationService.raise); Template and Rules v1 R5.5 DP-11; Architecture v5 Text Extract v1 slide 15 (rwb-deviation IN: GET/POST /deviations)",
  G, "3 Preconditions; 12.2 REST operations consumed; 12.8 Contract fakes", "Medium", "Tech lead of rwb-agent with the S8 service owner", "The app story builds against the rwb-deviation fake of section 12.8 until the S8 story is agreed"),
 ("3", "The raise request carries raisedBy \"SCREENING_AGENT\" and the agent run ID, and its answer carries the deviation ID and the decision record entry ID the feedback maps",
  "API Specification v4 DeviationRequest carries deviationCode, reason and documentIds only, and the Deviation answer has no decisionLogEntryId, while the legacy interface passes raisedBy and agentRunId and returns both IDs",
  "Legacy RWB-E2-029 section 12; API Specification v4 DeviationRequest and Deviation; TSD P10 Agent runtime v2 T3.1 agent_feedback",
  G, "7 Acceptance criteria AC2; 12.1; 12.2", "Medium", "Solution architect with the owners of rwb-deviation and rwb-decision", "The extra request and answer members are added to the published contract by their owners; the story states them and tests them against the fake"),
 ("4", "The decision-log entry read of rwb-decision has no named operation; it is consumed as one hop with the 2 s budget to read the sealed entry the local decision record names",
  "The legacy story read the decision log entry inside the monolith; in the target the central ledger is P7 rwb-decision and no source names the read by entry ID",
  "Legacy RWB-E2-029 section 12; Architecture v5 Text Extract v1 slide 14 (rwb-decision central decision ledger); Ownership Map v1 GET /decision-log/{entryId} owner P7",
  G, "12.2 REST operations consumed", "Medium", "Tech lead of rwb-agent with the P7 owner", "GET /decision-log/{entryId} of the Ownership Map is used as the read until the contract is published"),
 ("5", "The parameter keys of the confidence floor and of the promotion condition are not named by any source; both are read as parameters in force at run time and appear nowhere in code",
  "DP-06 sends parameters to the rwb-case contract and the legacy story names the values but not the parameter keys",
  "Template and Rules v1 R5.5 DP-06; FSD P10 Agent runtime v3 A2.5; legacy RWB-E2-029 sections 3 and 8",
  G, "3 Preconditions; 12.2 REST operations consumed; 17 Guardrails", "Medium", "Business analyst with the P3 owner and the model risk officer", "The keys are agreed with rwb-case and loaded as parameter rows; no value is written in code"),
 ("6", "The open-deviation read of rwb-deviation has no named operation for the case query; it is consumed as one hop with the 2 s budget so a code already open is not proposed again",
  "No source names the operation; Architecture v5 slide 15 gives rwb-deviation GET/POST /deviations and the ownership map fixes the base path only",
  "Architecture v5 Text Extract v1 slide 15 and 41; Ownership Map v1 (deviation owner S8)",
  G, "3 Preconditions; 12.2 REST operations consumed", "Medium", "Tech lead of rwb-agent with the S8 owner", "The read is declared in section 12.2 and stubbed in the rwb-deviation fake"),
 ("7", "The interaction-ledger read of rwb-source-data and the window it takes are not named by any source; the story reads a case-scoped window as one hop with the 2 s budget",
  "DP-05 and the R-PREC default ruling put the ledger with P1 rwb-source-data, and the legacy in-process reader had a case query and a window",
  "Template and Rules v1 R3 default ruling and R5.5 DP-05; legacy RWB-E2-029 sections 4 and 11",
  G, "12.2 REST operations consumed; 12.8 Contract fakes", "Medium", "Tech lead of rwb-agent with the P1 owner", "The operation and its window are agreed with P1; the story uses the contract mock of section 12.8"),
 ("8", "The gateway-bff route in front of the proposal panel has no name and no path; it is a pass-through of one hop in front of the panel read and the feedback write",
  "DP-19 requires the dashboard and panel reads to be reached through the gateway-bff route and no source names the route",
  "Template and Rules v1 R5.5 DP-19; Architecture v5 Text Extract v1 slide 20 (edge and gateway); legacy RWB-E2-029 section 15",
  G, "3 Preconditions; 12.2; 15 Screens and states", "Medium", "Solution architect with the edge owner", "The route name and path are agreed with RWB-PLT-N001-CON; the route passes the read and the refusal through unchanged"),
 ("9", "The gateway-bff route name and path for the contract operations are not fixed by any source, and this key adds no migration, so the rwb_agent Flyway numbering is not extended",
  "DP-19 requires the route and no source names it; the legacy story states \"no new table\" and DP-15 is not a pattern of this key, so no numbering can be cited",
  "Template and Rules v1 R5.5 DP-15 and DP-19; legacy RWB-E2-029 section 13 (\"no new table\"); TSD P10 Agent runtime v2 T3.1",
  G2, "5 Exception paths; 12.1; 12.2; 13 Solution plan", "Medium", "Solution architect with the edge owner and the P10 service owner", "The route is agreed with RWB-PLT-N001-CON, and the columns this key reads arrive with RWB-P10-E1062-APP and RWB-P10-E2028-APP"),
 ("10", "The five score-row members beyond the baseline AgentEvaluation are added from the TSD field names; the member types and the page size of the evaluation list are agreed at the review, and the legacy feature flag rwb.agent.screening-l1 is kept as a reference read through the platform flag library",
  "API Specification v4 AgentEvaluation carries approach, labelKey, sampleSize, agreementRate and failureCount only, while AC1 reads precision, recall and the three counts; the member types and the page size are named by no source, and the legacy flag has no target owner",
  "API Specification v4 AgentEvaluation and AgentEvaluationReport; TSD P10 Agent runtime v2 T3.1 agent_evaluation DF-AGT-086 to DF-AGT-096; legacy RWB-E2-029 sections 7 and 8",
  G, "7 Acceptance criteria AC1; 12.1; 12.3; 13 Solution plan; 15 Screens and states", "Medium", "Tech lead of rwb-agent with the solution architect", "The five members are declared with the TSD names and four decimals; the types and page size are settled at the review; the flag stays a reference and gates the segment"),
 ("11", "The decision record entry ID a confirmed proposal returns is mapped to agent_feedback.decision_log_id, and one feedback pair per run is kept",
  "The legacy story wrote the entry ID on the feedback row and the target keeps one decision record per feedback; no source fixes the mapping name",
  "Legacy RWB-E2-029 section 12; TSD P10 Agent runtime v2 T3.1 agent_feedback (decision_log_id); Template and Rules v1 R5.5 DP-03",
  G, "12.2; 12.7 Tables owned", "Medium", "Tech lead of rwb-agent with the P7 owner", "The mapping is declared in section 12.7 and proved by the contract test; a second feedback on the same run is refused with 409"),
 ("12", "The two segment members and the run facts on the completion payload are named by no source; the segment, floor, evaluation and promotion columns arrive with RWB-P10-E1062-APP and RWB-P10-E2028-APP, so this key adds no migration",
  "The legacy story read the segment fields of agent_policy and nothing names them on the event payload; DP-15 is not a pattern of this key",
  "Legacy RWB-E2-029 sections 7, 11 and 13; TSD P10 Agent runtime v2 T3.1 agent_policy; Architecture v5 Text Extract v1 slide 16 and 43 (rwb.agent.events.v1)",
  G2, "12.3 Events published; 12.7 Tables owned; 13 Solution plan", "Medium", "Tech lead of rwb-agent with the P10 service owner", "The payload members are declared in section 12.3 and the columns stay with the earlier P10 stories"),
 ("13", "The ACE valuation fact DF-ACE-193 is read through the rwb-source-data contract, one hop with the 2 s budget, and never from an ACE view of another owner",
  "DP-05 allows a read through rwb-source-data's contract or the service's own ACE views; the fact is not rwb-agent's and no source puts a copy in rwb_agent",
  "Template and Rules v1 R5.5 DP-05; Architecture v5 Text Extract v1 slide 41 (extension tables owner P1); Ownership Map v1 valuation_ext owner P1",
  G, "11 Data; 12.2 REST operations consumed", "Medium", "Tech lead of rwb-agent with the P1 owner", "The read is declared in section 12.2 and stubbed in the rwb-source-data fake; no foreign key and no copy"),
]

out = Path("_work/msr/logs") / f"{WP}-{K}.asm.jsonl"
lines = []
for n, text, why, read, gap, applied, conf, confirm, impact in rows:
    lines.append(json.dumps({
        "id": f"ASM-{WP}-{K}-{n}",
        "text": text,
        "why": why,
        "read": read,
        "gap": gap,
        "applied_in": applied,
        "confidence": conf,
        "confirm": confirm,
        "impact": impact,
        "wp": WP,
    }, ensure_ascii=False))
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("wrote", out, len(lines))

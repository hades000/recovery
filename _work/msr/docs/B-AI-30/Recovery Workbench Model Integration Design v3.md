SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Recovery Workbench

Model integration design

Version 3, 22 November 2026. The version 2 text is dated 28 October 2026.

| Item | Detail |
| Document | Recovery Workbench model integration design |
| Version | 3 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | arc42 building block view, C4 container view |
| Decision | D-RCV-60 microservice realignment |
| Supersedes | Version 2, 28 October 2026 |
| Status | Draft |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Change log | 3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

# 1. How models reach the Workbench

The bank's models run in COLLINS and ACE under the bank model risk standard. The Workbench does not run models. It reads their output from the daily COLLINS load (INT-08) and, for agents, calls the model endpoint through the agent platform (DL33).

In the target architecture (D-RCV-60) the agent platform of version 2 is the rwb-agent service (P10, Agent runtime, wave 1). Every call to the model endpoint is made from an activity on the rwb-agent task queue: no other service makes that call and no workflow code makes it, so workflows stay deterministic and a replay reuses the recorded result (Architecture v5 slide 16; Temporal and Drools Design v1 slides 11 and 27). The daily COLLINS load lands in the ACE database, and rwb-source-data (P1) is the only service that reads the ACE recovery.v_ace_* views (ADR-010, DP-05). Every other service therefore receives the score through rwb-source-data's contract and never reads the ACE tables or another service's tables (DP-01).

| Model | Model inventory IDs | What it predicts | Runs in | Used by | Score read by (target) |
|---|---|---|---|---|---|
| C-score, Mortgage | CRR_RET_353, CRR_RET_376, CRR_RET_334 | Likelihood an account cures by bucket | COLLINS | Route agent; reassessment | rwb-source-data (P1) |
| C-score, Hire purchase | CRR_RET_203, CRR_RET_313, CRR_RET_323 | Likelihood an account cures by bucket | COLLINS | Route agent; reassessment | rwb-source-data (P1) |
| C-score, SSME | CRR_RET_349, CRR_RET_350, CRR_RET_340, CRR_RET_346, CRR_RET_345, CRR_RET_366, CRR_RET_356, CRR_RET_355 | Likelihood an account cures by bucket and channel | COLLINS | Route agent; reassessment | rwb-source-data (P1) |
| T-grade | CRR_RET_285, CRR_RET_351 | Risk grade for SSME and hire purchase | COLLINS | Route agent | rwb-source-data (P1) |
| TDR scheme suggester | CRR_RET_372 Mortgage, CRR_RET_373 SSME | The restructure scheme that fits the customer | ACE and COLLINS | D5.1, D5.2 | rwb-source-data (P1) |
| Asset pricing | CRR_RET_380 | Fair value of an asset | COLLINS | Valuation agent; pricing agent | rwb-source-data (P1) |
| Asset auction sale price | CRR_RET_392 | Expected auction price of a property | COLLINS | Pricing agent | rwb-source-data (P1) |
| Asset auction sale success rate | CRR_RET_393 | Likelihood a property sells at auction | COLLINS | Pricing agent | rwb-source-data (P1) |
| Car auction sell price | CRR_RET_371 | Expected auction price of a vehicle | COLLINS | Pricing agent | rwb-source-data (P1) |
| Car auction sell rate | CRR_RET_370 | Likelihood a vehicle sells at auction | COLLINS | Pricing agent | rwb-source-data (P1) |

The score is read once, by rwb-source-data (P1), through the v_ace_score view over public.collins_score; the score, band and model version then reach the other services as the DP11 data product (GET /data-products/{productCode}/records on rwb-source-data's REST base, DP-05). The agent names in the last-but-one column keep their version 2 wording; the run that uses a model is an rwb-agent run in every case (section 4). The target owner of the INT-08 interface is Not specified in the source documents (CG-B-AI-30-4; ASM-B-AI-30-4).

# 2. Inputs and outputs

| Item | Design |
|---|---|
| Inputs | Prepared by COLLINS from the bank's data; the Workbench sends no data to the models |
| Output | One row per account and model each day: score, band, model ID, model version and business date (score entity, DP11) |
| Use | Rules read the band; agents read the score and reasons; the decision log records the model ID and version used |
| Freshness | End of day; monthly for some models. A score older than its age limit is not used and the rule result is used instead |
| Data product | DP11, Scores and route economics (Logical Data Model and Data Dictionary v8, LOV-DATA-PRODUCT) |
| Owner (Ownership Map) | Score entity and v_ace_score view: rwb-source-data (P1). Model ID and version on a decision: the decision record of the owning service, sealed in the central ledger of rwb-decision (P7, DP-03). Prompt, policy and run records: rwb-agent (P10). |

The three uses keep their version 2 wording and gain their target owner. Rules read the band inside an activity of the owning service, from the embedded Drools kit (DP-04), and the band arrives as a step input from rwb-source-data's contract (DP-05). Agents read the score and reasons through the read-only tool of rwb-agent (P10), which calls rwb-source-data's contract and holds no credential of its own. The decision log is the local decision record of the owning service, sealed to the central ledger in rwb-decision (P7) on the shared topic rwb.decision-record.v1 (DP-03).

A score older than its age limit is not used and the rule result is used instead; for an agent run the same fallback applies after 60 seconds (R-UNI-32, DL11).

# 3. Changing a model without a release

- Model Risk validates the new version under the bank standard.
- COLLINS publishes the new version's output with its version in the load.
- The model version in force for each decision step is reference data; the center of excellence loads the change and Risk approves it.
- Decisions from the valid from date use the new version; earlier decisions keep theirs.
- Champion and challenger runs are set by the same table, with a share of cases per version.

Steps and owners in the target architecture:

| Step | Owner (Ownership Map) | Where it is held |
|---|---|---|
| Model Risk validates the new version under the bank standard | Model Risk (role) | Outside the Workbench |
| COLLINS publishes the new version's output with its version in the load | COLLINS (outside) | ACE database; read by rwb-source-data (P1) through v_ace_score |
| The model version in force for each decision step is reference data | rwb-case (P3), reference-data contract (DP-07, RWB-P3-E1043-CON) | rwb_case reference data |
| The approval of a change | rwb-decision (P7) | rwb_decision approvals and the central ledger |
| Champion and challenger runs, with a share of cases per version | rwb-case (P3) | The same reference data |

The table that holds the model version in force is Not specified in the source documents (CG-B-AI-30-3; ASM-B-AI-30-3). Under the R3 default ruling it is reference data, which belongs to rwb-case (P3) and is reached through its reference-data contract (DP-07); it is not the rule package registry, which stays with rwb-decision (P7, DP-04). The approval is recorded in rwb-decision like every other approval (P7, Ownership Map approval table), and each decision keeps the model ID and version it used, so an earlier decision never changes when a version is promoted.

# 4. The large language model endpoint

- Reached only through the agent platform's tool gateway; no Workbench code calls it directly.
- A private endpoint in the SCB tenant (DL33).
- Prompts carry only the fields the step needs; no clear identifiers.
- Prompt, policy and model versions are recorded on each run.

In the target architecture the four points read as follows.

- The agent platform is rwb-agent (P10, wave 1). The only caller of the model endpoint is an activity on the rwb-agent task queue; no other service and no workflow code calls it (Temporal and Drools Design v1 slide 27: workflow code decides the order, activity code does the real work).
- The endpoint is Enterprise AI's private endpoint, INT-23, and rwb-agent is its only Recovery caller (Architecture v5 slides 22 and 28). DL33 stands.
- A run is started by the owning service as a child workflow on queue rwb-agent: AgentRunWorkflow, the kit template "Agent run with rule fallback". It has 60 seconds, then the rule result is used and the fallback is recorded (Architecture v5 slide 16; R-UNI-32, DL11).
- The tool gateway is the only way the agent reaches data or acts: read-only tools to source data (case facts) and to documents (extracted fields). The gateway holds the permissions and the agent holds no credential (Architecture v5 slide 16).
- Guardrails are checked before the output is used and recorded in rwb_agent: schema, allowed actions and confidence floor, with a fallback row (agent_policy, agent_run, agent_alert, agent_feedback, P10).
- Prompts carry only the fields the step needs, as DL26 requires; the personal fields are masked, the prompts are versioned in rwb_agent.agent_prompt (P10), and the PDPA rule applies: no personal data in events, workflow inputs or logs.
- Each run records the prompt, policy and model versions in rwb_agent (agent_prompt, agent_policy, agent_run, P10), and the model ID and version used go into the decision record of the owning service and the central ledger of rwb-decision (P7, DP-03). The run ends with AgentRunCompleted (EV-28) on rwb.agent.events.v1, consumed by rwb-decision (P7), rwb-document (P5) and rwb-deviation (S8).

| Call | Caller | Runs in | Contract |
|---|---|---|---|
| Enterprise AI private endpoint (INT-23, DL33) | rwb-agent (P10) only | Activity on queue rwb-agent, inside AgentRunWorkflow | HTTPS private endpoint |
| Case facts and score read | rwb-agent (P10), through the tool gateway | Activity on queue rwb-agent | Data-product contract of rwb-source-data (P1, DP-05) |
| Extracted document fields read | rwb-agent (P10), through the tool gateway | Activity on queue rwb-agent | REST contract of rwb-document (P5) |
| AgentRunCompleted (EV-28) | rwb-agent (P10) | Outbox to rwb.agent.events.v1 | CloudEvents (DP-09) |

# 5. Monitoring

| Measure | Owner | Reviewed |
|---|---|---|
| Score coverage: accounts with a current score | Data steward | Daily |
| Drift against the development sample | Model Risk | Monthly |
| Outcome against prediction by band | Center of excellence | Quarterly |

The three owner roles are governance roles and stay as version 2 states them. The data each measure reads has a service owner in the Ownership Map:

| Measure | Data and its owner (Ownership Map) |
|---|---|
| Score coverage: accounts with a current score | The DP11 score data product and the v_ace_score view, rwb-source-data (P1) |
| Drift against the development sample | The model ID and version kept on each run (rwb_agent, P10) and on each decision (decision record, central ledger rwb-decision, P7) |
| Outcome against prediction by band | The DP11 band read through rwb-source-data (P1) and the outcome sealed in the central ledger of rwb-decision (P7) |

# 6. Change log

| Version, date, change, tool |
|---|
| 3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

What changed in version 3, and nothing else:

- The header lines are the Template and Rules R8.1 header; the title block and the metadata table keep the version 2 rows and add the decision, the superseded version, the status, the tool and the change-log row.
- Section 1 names rwb-agent (P10) as the agent platform of DL33, states that model calls are made only from rwb-agent activities, and adds the score read column with its owner from the Ownership Map.
- Section 2 keeps every row word for word, adds the data product and the owner row, and restates the three uses against DP-03, DP-04 and DP-05.
- Section 3 keeps its five steps word for word and adds the owner of each step from the Ownership Map.
- Section 4 keeps its four points word for word and restates them for rwb-agent activities, INT-23, AgentRunWorkflow, the 60-second fallback and the guardrail records, with the call table.
- Section 5 keeps its three measures and roles word for word and adds the data owner of each measure.
- Every model inventory ID, the D5.1 and D5.2 references, DP11, DL33, INT-08, the date of 28 October 2026 and the version 2 wording that did not change are kept.

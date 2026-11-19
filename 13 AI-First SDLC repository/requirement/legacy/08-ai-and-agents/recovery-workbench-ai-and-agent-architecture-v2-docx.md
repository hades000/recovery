<!-- source: 08 AI and agents/Recovery Workbench AI and Agent Architecture v2.docx -->
<!-- converted: 2026-11-04 from DOCX -->

> **Source:** `08 AI and agents/Recovery Workbench AI and Agent Architecture v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

AI and agent architecture

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench AI and agent architecture |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | arc42 with C4 component views and ISO/IEC/IEEE 42010 viewpoints |

# 1. The design on one page

| Element | Design |
|---|---|
| Where AI is used | 25 sub-decisions and steps: 10 automated, 13 advised, 2 decided by a person or acted on by a partner |
| Agents | 12 agents, each with a list of allowed actions, run through one orchestrator and one tool gateway |
| Models | 10 bank models from the model inventory, run in COLLINS and ACE and read from the daily load |
| Platform | The Enterprise AI agent platform; the model endpoint is a private endpoint in the SCB tenant (DL33) |
| Autonomy | Shadow first, then L1 recommend; step-ups approved by the strategy and model committee |
| Fallback | If an agent does not answer in 60 seconds, the rule result is used and the case still routes |
| Record | Every proposal and action in the decision log with the prompt, policy, model and agent versions |

# 2. Where decisions are automated, advised or made by a person

Automated: a rule, a model or an agent decides within policy. Advised: a model or an agent recommends with reasons and a person or committee decides. Person: a person decides alone. Partner: a partner acts on the bank's instruction.

| ID | Sub-decision | How it is made | Mode | Run by | Autonomy | First in |
|---|---|---|---|---|---|---|
| D5.1 | Affordability | Rule and model in ACE | Automated | ACE restructure calculator | L0 to L0 | E2 |
| D5.2 | Plan to offer | Agent, final within the limit | Automated | Settlement and restructure agent | L2 to L3 | E3 |
| D5.3 | Reassess after a broken plan | Agent proposes, person approves | Advised | Settlement and restructure agent | L1 to L2 | E3 |
| D6.1 | Accept the appraisal value | Rule check, agent flags outliers, person accepts | Advised | Valuation agent | L1 to L2 | E3 |
| D6.2 | Return by route | COLLINS model | Automated | COLLINS | L0 to L0 | E4 |
| D6.3 | Route | Agent recommends, person approves, committee above the limit | Advised | Route agent | L1 to L2 | E4 |
| D6.4 | Settlement amount and terms | Rule payoff, agent range, person negotiates and approves | Advised | Settlement and restructure agent | L1 to L2 | E3 |
| D6.5 | Thai Credit Guarantee claim | Agent prepares, person approves | Advised | Guarantee claim agent | L1 to L2 | E4 |
| D6.6 | Guarantor and co-borrower pursuit | Rule sends notices, person negotiates | Person | Case owner | L0 to L0 | E4 |
| D7.1 | Demand and recall notices | Rule | Automated | Rules component | L0 to L0 | E2 |
| D7.2 | Document pack complete | Agent assembles and checks, person verifies | Advised | Legal document agent | L1 to L3 | E5 |
| D7.3 | Which law firm | Rule from the panel | Automated | Rules component | L0 to L0 | E5 |
| D7.4 | Settle before judgment, appeal, fees | Agent proposes, person approves | Advised | Legal document agent | L1 to L1 | E5 |
| D7.5 | Enforce: trace, writ, seizure, auction | Agent traces, partner acts, person approves a bankruptcy petition | Partner | Tracing agent; law firm | L1 to L2 | E5 |
| D8.1 | Asset on the books, holding age, reappraisal | Rule | Automated | Rules component | L0 to L0 | E3 |
| D8.2 | Start and floor price | Agent with COLLINS, person approves the floor | Advised | Pricing agent | L1 to L2 | E3 |
| D8.3 | RAMC transfer, buy-back, rental | Agent proposes, person approves | Advised | Pricing agent | L1 to L1 | E4 |
| D8.4 | Debt sale lots, buyer terms, award | Agent builds lots, rules check eligibility, person approves | Advised | Debt sale agent | L1 to L2 | E5 |
| D9.1 | Eligibility and tax criteria | Rule | Automated | Rules component | L0 to L0 | E6 |
| D9.2 | Write off or pursue | Agent proposes, committee approves | Advised | Write-off agent | L1 to L1 | E6 |
| D9.3 | Recovery after charge-off | Agent proposes, person approves a sale | Advised | Write-off agent | L1 to L2 | E6 |
| X1-X7 | Deviation screening at entry and on events | Agent flags, rule raises, handler decides | Advised | Screening agent | L1 to L2 | E2 |
| X6 | Trace a lost customer | Agent traces within policy | Automated | Tracing agent | L2 to L3 | E7 |
| P8 | Match receipts to cases | Agent matches, officer clears exceptions | Automated | Reconciliation agent | L2 to L3 | E4 |
| P5 | Classify and extract documents | OCR pipeline extracts, agent classifies, person reviews low confidence | Automated | Intake agent | L2 to L3 | E2 |

# 3. Components

| Component | What it does | Owner |
|---|---|---|
| Orchestrator | Runs the decision steps and applies the autonomy level | Enterprise AI team |
| Tool gateway | The only way an agent reaches a system. No agent holds a credential | Enterprise AI team |
| Guardrail checker | Checks every output against its schema, the allowed actions and a confidence floor | Enterprise AI team |
| Prompt and policy store | Versioned, so a run can be reproduced | Enterprise AI team |
| Evaluation harness | Labeled sets scored before a result is used | Enterprise AI team |
| Model endpoint | On the approved endpoint in the SCB tenant (DL33) | CTO with Enterprise AI |
| Agent runtime module (P10) | The Workbench side: calls the orchestrator, applies the autonomy level, records the result and falls back to the rule | Recovery squads |

# 4. The agents

| Agent | What it does | Inputs | May call | Output | Live |
|---|---|---|---|---|---|
| Intake agent | Classifies inbound documents and checks extracted fields against the case | Document, OCR output, case record | Read case; write document fields; raise review task | Document type, fields with confidence | E2 |
| Screening agent | Screens a case at entry and on events for signs of X1 to X7 | Case record, interaction ledger, documents | Read case; propose deviation | Proposed deviation with reasons | E2 |
| Settlement and restructure agent | Proposes the plan or the settlement range within policy | Account, payments, payoff, affordability, policy | Read case; call the ACE calculator; propose treatment | Proposed terms with reasons | E3 |
| Valuation agent | Flags appraisal values outside the expected range | Appraisal, comparable sales, pricing model output | Read asset; read model output | Accept or flag with reasons | E3 |
| Pricing agent | Proposes the start price, floor price and disposal route for an asset | Asset, valuations, auction models, holding cost | Read asset; read model output; propose listing | Prices and route with expected return | E3 |
| Route agent | Recommends the route for a case with the expected return of each route | Case, accounts, collateral, scores, route return by route | Read case; read COLLINS output; propose route | Recommended route with reasons | E4 |
| Guarantee claim agent | Prepares the TCG and guarantee claim and checks the checklist | Guarantee, case, documents | Read case; assemble claim; raise task | Claim pack with checklist result | E4 |
| Reconciliation agent | Matches receipts to cases and accounts | Payments, proceeds, open treatments | Read payments; match proceeds; raise exception | Match or exception | E4 |
| Legal document agent | Assembles the litigation pack and checks it against the defect list | Documents, case, legal template | Read documents; assemble pack; raise retrieval request | Pack with defect list | E5 |
| Debt sale agent | Builds lots from eligible accounts and prepares the masked data tape | Eligible accounts, balances, history | Read case list; build lot; build tape | Proposed lots and tape | E5 |
| Write-off agent | Prepares the write-off pack and proposes write off or pursue | Balance, provision, route history, legal and asset state | Read case; build pack | Pack and proposal | E6 |
| Tracing agent | Finds a lost customer through permitted sources | Contact points, interaction ledger, partner results | Read case; request trace from partner; propose contact update | Contact found or trace exhausted | E7 |

# 5. The models

| Model | Model inventory IDs | What it predicts | Runs in | Used by |
|---|---|---|---|---|
| C-score, Mortgage | CRR_RET_353, CRR_RET_376, CRR_RET_334 | Likelihood an account cures by bucket | COLLINS | Route agent; reassessment |
| C-score, Hire purchase | CRR_RET_203, CRR_RET_313, CRR_RET_323 | Likelihood an account cures by bucket | COLLINS | Route agent; reassessment |
| C-score, SSME | CRR_RET_349, CRR_RET_350, CRR_RET_340, CRR_RET_346, CRR_RET_345, CRR_RET_366, CRR_RET_356, CRR_RET_355 | Likelihood an account cures by bucket and channel | COLLINS | Route agent; reassessment |
| T-grade | CRR_RET_285, CRR_RET_351 | Risk grade for SSME and hire purchase | COLLINS | Route agent |
| TDR scheme suggester | CRR_RET_372 Mortgage, CRR_RET_373 SSME | The restructure scheme that fits the customer | ACE and COLLINS | D5.1, D5.2 |
| Asset pricing | CRR_RET_380 | Fair value of an asset | COLLINS | Valuation agent; pricing agent |
| Asset auction sale price | CRR_RET_392 | Expected auction price of a property | COLLINS | Pricing agent |
| Asset auction sale success rate | CRR_RET_393 | Likelihood a property sells at auction | COLLINS | Pricing agent |
| Car auction sell price | CRR_RET_371 | Expected auction price of a vehicle | COLLINS | Pricing agent |
| Car auction sell rate | CRR_RET_370 | Likelihood a vehicle sells at auction | COLLINS | Pricing agent |

# 6. How a decision runs

- An event reaches the case: a load, a screen action, a partner result or a timer.

- The rules component finds the step and reads its autonomy level from the reference data.

- The agent runtime module calls the orchestrator with only the fields the step needs.

- The agent calls tools through the tool gateway. The gateway checks each call against the agent's allowed actions.

- The guardrail checker tests the output against its schema, the allowed actions and the confidence floor.

- At L1 the output is shown to the person as a recommendation with reasons. At L2 and above the agent acts inside its band.

- The decision log writer records the inputs, the versions, the output, the decision and the approver. A failed write stops the action.

- If the agent does not answer in 60 seconds, or a guardrail fails, the rule result is used and the fallback is recorded.

# 7. Guardrails

| Guardrail | What it does |
|---|---|
| Tool gateway | The only way an agent reaches data or acts. The gateway holds the permissions; the agent holds no credential |
| Allowed actions | Each agent has a list of the actions it may propose or take at its autonomy level |
| Schema check | Every output is checked against its schema before it is used |
| Confidence floor | An output below the floor goes to a person; the rule result is used meanwhile |
| Fallback | If the agent does not answer within 60 seconds, the rule result is used and the fallback is recorded |
| No personal data in prompts beyond need | Each agent receives only the fields its step needs; the PDPA lint checks prompts |
| Versioned prompts and policies | Each run records the prompt, policy, model and agent versions, so it can be reproduced |
| Decision log | Every agent proposal and action is written to the decision log on the same terms as a person's |

# 8. Autonomy steps

| Step | What the agent does | Measured before the next step |
|---|---|---|
| Shadow | The agent runs beside the rule; its output is logged and not shown | Agreement with the rule and with people's decisions on a labeled set |
| L1 recommend | The output is shown as a recommendation; a person decides every case | Acceptance rate, override reasons, outcome against the rule |
| L2 act in a band | The agent acts inside a narrow band; a person reviews a sample and the exceptions | Sample error rate, exception rate, outcome measures |
| L3 act across the decision | The agent acts across the decision; people review by exception | Outcome measures by route and product; complaints |
| L4 act and close | The agent acts and closes; people monitor the measures | Outcome measures; model risk review |

| Level | What the agent does | What a person does |
|---|---|---|
| L0 | Nothing. The rule decides | Everything |
| L1 | Recommends, with its reasons | Decides. Every decision starts here after a shadow run |
| L2 | Acts inside a narrow band | Reviews a sample and the exceptions |
| L3 | Acts across the decision | Reviews by exception |
| L4 | Acts and closes | Monitors the measures |

# 9. Governance

| Who | Accountable for |
|---|---|
| Strategy and model committee | Approves each autonomy step on the measured results, and agent changes |
| Model Risk | Validates models and agents before use and at each step-up, under the bank model risk standard |
| Center of excellence | Owns prompts, policies and evaluation sets; proposes changes |
| Enterprise AI team | Runs the agent platform, the model endpoint and the evaluation harness |
| Risk and model risk officer | Monitors acceptance, overrides, fallbacks and drift each month |
| Internal audit | Reads the decision log for agent decisions |

# 10. Measures

| Measure | Meaning | Reviewed |
|---|---|---|
| Acceptance rate | Recommendations approved without override | Monthly |
| Override reasons | Coded reasons when a person departs from the recommendation | Monthly |
| Fallback rate | Steps where the rule result was used because the agent did not answer or a guardrail failed | Weekly |
| Latency | Time from call to answer at the 95th percentile | Weekly |
| Cost | Model cost per decision | Monthly |
| Outcome | Recovery, turnaround and loss for agent-advised decisions against rule-only decisions | Quarterly |

# 11. Open decisions

| Decision | What is needed | Answer used until decided |
|---|---|---|
| DL33 | The model endpoint the agents call and where it is hosted | A private endpoint in the SCB tenant |
| DL11 | Agent response target | 60 seconds, then the rule result is used |
| DL26 | Which personal fields each agent may receive | Only the fields the step needs; masked otherwise |

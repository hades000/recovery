## Slide 1

SCB

COLLECTIONS AND RECOVERY TRANSFORMATION
Recovery Workbench: AI and agent architecture

Henka Group, 28 October 2026
(C) Siam Commercial Bank and Henka Pte Ltd

## Slide 2

Who decides at each step

2

10
Automated
A rule, a model or an agent decides within policy and the result is logged

13
Advised
A model or an agent recommends with reasons; a person or a committee decides

2
Person or partner
A person decides alone, or a partner acts on the bank's instruction

Counts are the 25 sub-decisions and automated steps from day 90 to close. The approver for every advised decision is set by the approval authority regulation and the delegation of authority table.

## Slide 3

Decisions D5 to D7

3

|  | Sub-decision | Mode | Run by | Autonomy | First in |
|---|---|---|---|---|---|
| D5.1 | Affordability | Automated | ACE restructure calculator | L0 to L0 | E2 |
| D5.2 | Plan to offer | Automated | Settlement and restructure agent | L2 to L3 | E3 |
| D5.3 | Reassess after a broken plan | Advised | Settlement and restructure agent | L1 to L2 | E3 |
| D6.1 | Accept the appraisal value | Advised | Valuation agent | L1 to L2 | E3 |
| D6.2 | Return by route | Automated | COLLINS | L0 to L0 | E4 |
| D6.3 | Route | Advised | Route agent | L1 to L2 | E4 |
| D6.4 | Settlement amount and terms | Advised | Settlement and restructure agent | L1 to L2 | E3 |
| D6.5 | Thai Credit Guarantee claim | Advised | Guarantee claim agent | L1 to L2 | E4 |
| D6.6 | Guarantor and co-borrower pursuit | Person | Case owner | L0 to L0 | E4 |
| D7.1 | Demand and recall notices | Automated | Rules component | L0 to L0 | E2 |
| D7.2 | Document pack complete | Advised | Legal document agent | L1 to L3 | E5 |
| D7.3 | Which law firm | Automated | Rules component | L0 to L0 | E5 |
| D7.4 | Settle before judgment, appeal, fees | Advised | Legal document agent | L1 to L1 | E5 |
| D7.5 | Enforce: trace, writ, seizure, auction | Partner | Tracing agent; law firm | L1 to L2 | E5 |


## Slide 4

Decisions D8 and D9, deviations and automated steps

4

|  | Sub-decision | Mode | Run by | Autonomy | First in |
|---|---|---|---|---|---|
| D8.1 | Asset on the books, holding age, reappraisal | Automated | Rules component | L0 to L0 | E3 |
| D8.2 | Start and floor price | Advised | Pricing agent | L1 to L2 | E3 |
| D8.3 | RAMC transfer, buy-back, rental | Advised | Pricing agent | L1 to L1 | E4 |
| D8.4 | Debt sale lots, buyer terms, award | Advised | Debt sale agent | L1 to L2 | E5 |
| D9.1 | Eligibility and tax criteria | Automated | Rules component | L0 to L0 | E6 |
| D9.2 | Write off or pursue | Advised | Write-off agent | L1 to L1 | E6 |
| D9.3 | Recovery after charge-off | Advised | Write-off agent | L1 to L2 | E6 |
| X1-X7 | Deviation screening at entry and on events | Advised | Screening agent | L1 to L2 | E2 |
| X6 | Trace a lost customer | Automated | Tracing agent | L2 to L3 | E7 |
| P8 | Match receipts to cases | Automated | Reconciliation agent | L2 to L3 | E4 |
| P5 | Classify and extract documents | Automated | Intake agent | L2 to L3 | E2 |


## Slide 5

How an agent reaches a decision

5

Event
A load, a screen action, a partner result or a timer

Rule
The rules component finds the step and its autonomy level

Agent
The orchestrator calls the agent through the tool gateway

Guardrails
Schema, allowed actions and confidence floor

Decision
Recommend to a person, or act within the band

Log
Inputs, versions, output and approver in the decision log

| Component | What it does |
|---|---|
| Orchestrator | Runs the decision steps and applies the autonomy level |
| Tool gateway | The only way an agent reaches a system. No agent holds a credential |
| Guardrail checker | Checks every output against its schema, the allowed actions and a confidence floor |
| Prompt and policy store | Versioned, so a run can be reproduced |
| Evaluation harness | Labeled sets scored before a result is used |
| Model endpoint | On the approved endpoint in the SCB tenant (DL33) |


## Slide 6

The agents

6

| Agent | What it does | Live | Shadow |
|---|---|---|---|
| Intake agent | Classifies inbound documents and checks extracted fields against the case | E2 | E1 |
| Screening agent | Screens a case at entry and on events for signs of X1 to X7 | E2 | E1 |
| Settlement and restructure agent | Proposes the plan or the settlement range within policy | E3 | E2 |
| Valuation agent | Flags appraisal values outside the expected range | E3 | E2 |
| Pricing agent | Proposes the start price, floor price and disposal route for an asset | E3 | E2 |
| Route agent | Recommends the route for a case with the expected return of each route | E4 | E3 |
| Guarantee claim agent | Prepares the TCG and guarantee claim and checks the checklist | E4 | E3 |
| Reconciliation agent | Matches receipts to cases and accounts | E4 | E3 |
| Legal document agent | Assembles the litigation pack and checks it against the defect list | E5 | E4 |
| Debt sale agent | Builds lots from eligible accounts and prepares the masked data tape | E5 | E4 |
| Write-off agent | Prepares the write-off pack and proposes write off or pursue | E6 | E5 |
| Tracing agent | Finds a lost customer through permitted sources | E7 | E6 |


## Slide 7

The models the agents use

7

| Model | Model inventory IDs | What it predicts | Used by |
|---|---|---|---|
| C-score, Mortgage | CRR_RET_353, CRR_RET_376, CRR_RET_334 | Likelihood an account cures by bucket | Route agent; reassessment |
| C-score, Hire purchase | CRR_RET_203, CRR_RET_313, CRR_RET_323 | Likelihood an account cures by bucket | Route agent; reassessment |
| C-score, SSME | CRR_RET_349, CRR_RET_350, CRR_RET_340, CRR_RET_346, CRR_RET_345, CRR_RET_366, CRR_RET_356, CRR_RET_355 | Likelihood an account cures by bucket and channel | Route agent; reassessment |
| T-grade | CRR_RET_285, CRR_RET_351 | Risk grade for SSME and hire purchase | Route agent |
| TDR scheme suggester | CRR_RET_372 Mortgage, CRR_RET_373 SSME | The restructure scheme that fits the customer | D5.1, D5.2 |
| Asset pricing | CRR_RET_380 | Fair value of an asset | Valuation agent; pricing agent |
| Asset auction sale price | CRR_RET_392 | Expected auction price of a property | Pricing agent |
| Asset auction sale success rate | CRR_RET_393 | Likelihood a property sells at auction | Pricing agent |
| Car auction sell price | CRR_RET_371 | Expected auction price of a vehicle | Pricing agent |
| Car auction sell rate | CRR_RET_370 | Likelihood a vehicle sells at auction | Pricing agent |


Models run in COLLINS and ACE under the bank model risk standard. The Workbench reads their output from the daily load.

## Slide 8

Guardrails

8

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


## Slide 9

How autonomy steps up

9

| Step | What the agent does | Measured before the next step |
|---|---|---|
| Shadow | The agent runs beside the rule; its output is logged and not shown | Agreement with the rule and with people's decisions on a labeled set |
| L1 recommend | The output is shown as a recommendation; a person decides every case | Acceptance rate, override reasons, outcome against the rule |
| L2 act in a band | The agent acts inside a narrow band; a person reviews a sample and the exceptions | Sample error rate, exception rate, outcome measures |
| L3 act across the decision | The agent acts across the decision; people review by exception | Outcome measures by route and product; complaints |
| L4 act and close | The agent acts and closes; people monitor the measures | Outcome measures; model risk review |


Every step up is approved by the strategy and model committee on the measured results, with Model Risk validation.

## Slide 10

Who governs the agents

10

| Who | Accountable for |
|---|---|
| Strategy and model committee | Approves each autonomy step on the measured results, and agent changes |
| Model Risk | Validates models and agents before use and at each step-up, under the bank model risk standard |
| Center of excellence | Owns prompts, policies and evaluation sets; proposes changes |
| Enterprise AI team | Runs the agent platform, the model endpoint and the evaluation harness |
| Risk and model risk officer | Monitors acceptance, overrides, fallbacks and drift each month |
| Internal audit | Reads the decision log for agent decisions |


## Slide 11

Open decisions

11

|  | What is needed | Answer used until decided |
|---|---|---|
| DL33 | The model endpoint the agents call and where it is hosted | A private endpoint in the SCB tenant |
| DL11 | Agent response target | 60 seconds, then the rule result is used |
| DL26 | Which personal fields each agent may receive | Only the fields the step needs; masked otherwise |


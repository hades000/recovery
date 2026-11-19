# Recovery Workbench agent catalog and specifications

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

Each agent runs through the orchestrator and the tool gateway, at the autonomy level the strategy and model committee approves. If it does not answer in 60 seconds or fails a guardrail, the rule result is used.

## Intake agent

| Item | Specification |
|---|---|
| Watches | Documents arriving in the intake |
| Does | Classifies inbound documents and checks extracted fields against the case |
| Inputs | Document, OCR output, case record |
| May call | Read case; write document fields; raise review task |
| Output | Document type, fields with confidence |
| May decide alone | Document type and fields above the confidence floor |
| Escalates | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons |
| Measured on | Classification accuracy; field precision and recall |
| Shadow from | E1 |
| Live from | E2 |

| Step | Sub-decision | Autonomy at go-live | Target |
|---|---|---|---|
| P5 | Classify and extract documents | L2 | L3 |

## Screening agent

| Item | Specification |
|---|---|
| Watches | Case entry and events on open cases |
| Does | Screens a case at entry and on events for signs of X1 to X7 |
| Inputs | Case record, interaction ledger, documents |
| May call | Read case; propose deviation |
| Output | Proposed deviation with reasons |
| May decide alone | Nothing; it proposes deviations |
| Escalates | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons |
| Measured on | Deviations confirmed against proposed |
| Shadow from | E1 |
| Live from | E2 |

| Step | Sub-decision | Autonomy at go-live | Target |
|---|---|---|---|
| X1-X7 | Deviation screening at entry and on events | L1 | L2 |

## Settlement and restructure agent

| Item | Specification |
|---|---|
| Watches | Route approved to restructure or settlement; broken plans |
| Does | Proposes the plan or the settlement range within policy |
| Inputs | Account, payments, payoff, affordability, policy |
| May call | Read case; call the ACE calculator; propose treatment |
| Output | Proposed terms with reasons |
| May decide alone | Plan terms within the policy band at L2 |
| Escalates | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons |
| Measured on | Acceptance, cure after 6 months |
| Shadow from | E2 |
| Live from | E3 |

| Step | Sub-decision | Autonomy at go-live | Target |
|---|---|---|---|
| D5.2 | Plan to offer | L2 | L3 |
| D5.3 | Reassess after a broken plan | L1 | L2 |
| D6.4 | Settlement amount and terms | L1 | L2 |

## Valuation agent

| Item | Specification |
|---|---|
| Watches | New appraisals |
| Does | Flags appraisal values outside the expected range |
| Inputs | Appraisal, comparable sales, pricing model output |
| May call | Read asset; read model output |
| Output | Accept or flag with reasons |
| May decide alone | Nothing; it flags outliers |
| Escalates | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons |
| Measured on | Outliers confirmed |
| Shadow from | E2 |
| Live from | E3 |

| Step | Sub-decision | Autonomy at go-live | Target |
|---|---|---|---|
| D6.1 | Accept the appraisal value | L1 | L2 |

## Pricing agent

| Item | Specification |
|---|---|
| Watches | Assets ready to sell |
| Does | Proposes the start price, floor price and disposal route for an asset |
| Inputs | Asset, valuations, auction models, holding cost |
| May call | Read asset; read model output; propose listing |
| Output | Prices and route with expected return |
| May decide alone | Nothing; a person approves the floor |
| Escalates | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons |
| Measured on | Sale price against the floor; days to sell |
| Shadow from | E2 |
| Live from | E3 |

| Step | Sub-decision | Autonomy at go-live | Target |
|---|---|---|---|
| D8.2 | Start and floor price | L1 | L2 |
| D8.3 | RAMC transfer, buy-back, rental | L1 | L1 |

## Route agent

| Item | Specification |
|---|---|
| Watches | Cases reaching the route decision |
| Does | Recommends the route for a case with the expected return of each route |
| Inputs | Case, accounts, collateral, scores, route return by route |
| May call | Read case; read COLLINS output; propose route |
| Output | Recommended route with reasons |
| May decide alone | Nothing; a person approves the route |
| Escalates | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons |
| Measured on | Acceptance; recovery by route against the rule |
| Shadow from | E3 |
| Live from | E4 |

| Step | Sub-decision | Autonomy at go-live | Target |
|---|---|---|---|
| D6.3 | Route | L1 | L2 |

## Guarantee claim agent

| Item | Specification |
|---|---|
| Watches | Guarantees meeting claim conditions |
| Does | Prepares the TCG and guarantee claim and checks the checklist |
| Inputs | Guarantee, case, documents |
| May call | Read case; assemble claim; raise task |
| Output | Claim pack with checklist result |
| May decide alone | Nothing; the guarantee officer approves |
| Escalates | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons |
| Measured on | Claims accepted first time |
| Shadow from | E3 |
| Live from | E4 |

| Step | Sub-decision | Autonomy at go-live | Target |
|---|---|---|---|
| D6.5 | Thai Credit Guarantee claim | L1 | L2 |

## Reconciliation agent

| Item | Specification |
|---|---|
| Watches | Unmatched receipts |
| Does | Matches receipts to cases and accounts |
| Inputs | Payments, proceeds, open treatments |
| May call | Read payments; match proceeds; raise exception |
| Output | Match or exception |
| May decide alone | Matches with one candidate case and an exact amount |
| Escalates | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons |
| Measured on | Auto-match accuracy; exceptions |
| Shadow from | E3 |
| Live from | E4 |

| Step | Sub-decision | Autonomy at go-live | Target |
|---|---|---|---|
| P8 | Match receipts to cases | L2 | L3 |

## Legal document agent

| Item | Specification |
|---|---|
| Watches | Notice periods ending |
| Does | Assembles the litigation pack and checks it against the defect list |
| Inputs | Documents, case, legal template |
| May call | Read documents; assemble pack; raise retrieval request |
| Output | Pack with defect list |
| May decide alone | Pack assembly; a person verifies |
| Escalates | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons |
| Measured on | Packs accepted first time |
| Shadow from | E4 |
| Live from | E5 |

| Step | Sub-decision | Autonomy at go-live | Target |
|---|---|---|---|
| D7.2 | Document pack complete | L1 | L3 |
| D7.4 | Settle before judgment, appeal, fees | L1 | L1 |

## Debt sale agent

| Item | Specification |
|---|---|
| Watches | Debt sale cycle opened |
| Does | Builds lots from eligible accounts and prepares the masked data tape |
| Inputs | Eligible accounts, balances, history |
| May call | Read case list; build lot; build tape |
| Output | Proposed lots and tape |
| May decide alone | Nothing; the committee approves |
| Escalates | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons |
| Measured on | Lots approved without change |
| Shadow from | E4 |
| Live from | E5 |

| Step | Sub-decision | Autonomy at go-live | Target |
|---|---|---|---|
| D8.4 | Debt sale lots, buyer terms, award | L1 | L2 |

## Write-off agent

| Item | Specification |
|---|---|
| Watches | Monthly write-off scan |
| Does | Prepares the write-off pack and proposes write off or pursue |
| Inputs | Balance, provision, route history, legal and asset state |
| May call | Read case; build pack |
| Output | Pack and proposal |
| May decide alone | Nothing; the committee approves |
| Escalates | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons |
| Measured on | Packs accepted; removals |
| Shadow from | E5 |
| Live from | E6 |

| Step | Sub-decision | Autonomy at go-live | Target |
|---|---|---|---|
| D9.2 | Write off or pursue | L1 | L1 |
| D9.3 | Recovery after charge-off | L1 | L2 |

## Tracing agent

| Item | Specification |
|---|---|
| Watches | X6 lost contact |
| Does | Finds a lost customer through permitted sources |
| Inputs | Contact points, interaction ledger, partner results |
| May call | Read case; request trace from partner; propose contact update |
| Output | Contact found or trace exhausted |
| May decide alone | Trace requests within policy; a new contact point is verified before use |
| Escalates | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons |
| Measured on | Contacts restored |
| Shadow from | E6 |
| Live from | E7 |

| Step | Sub-decision | Autonomy at go-live | Target |
|---|---|---|---|
| D7.5 | Enforce: trace, writ, seizure, auction | L1 | L2 |
| X6 | Trace a lost customer | L2 | L3 |

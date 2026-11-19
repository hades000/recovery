<!-- source: 08 AI and agents/Recovery Workbench Agent Catalog and Specifications v2.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `08 AI and agents/Recovery Workbench Agent Catalog and Specifications v2.xlsx`  
> **Converted from:** XLSX

## Agents

| Agent catalog |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|
| 12 agents. What each may decide alone is the position used until the strategy and model committee approves each step. |  |  |  |  |  |  |  |  |  |
| Agent | Watches | Does | Inputs | May call | May decide alone | Escalates | Measured on | Live | Shadow from |
| Intake agent | Documents arriving in the intake | Classifies inbound documents and checks extracted fields against the case | Document, OCR output, case record | Read case; write document fields; raise review task | Document type and fields above the confidence floor | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons | Classification accuracy; field precision and recall | E2 | E1 |
| Screening agent | Case entry and events on open cases | Screens a case at entry and on events for signs of X1 to X7 | Case record, interaction ledger, documents | Read case; propose deviation | Nothing; it proposes deviations | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons | Deviations confirmed against proposed | E2 | E1 |
| Settlement and restructure agent | Route approved to restructure or settlement; broken plans | Proposes the plan or the settlement range within policy | Account, payments, payoff, affordability, policy | Read case; call the ACE calculator; propose treatment | Plan terms within the policy band at L2 | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons | Acceptance, cure after 6 months | E3 | E2 |
| Valuation agent | New appraisals | Flags appraisal values outside the expected range | Appraisal, comparable sales, pricing model output | Read asset; read model output | Nothing; it flags outliers | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons | Outliers confirmed | E3 | E2 |
| Pricing agent | Assets ready to sell | Proposes the start price, floor price and disposal route for an asset | Asset, valuations, auction models, holding cost | Read asset; read model output; propose listing | Nothing; a person approves the floor | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons | Sale price against the floor; days to sell | E3 | E2 |
| Route agent | Cases reaching the route decision | Recommends the route for a case with the expected return of each route | Case, accounts, collateral, scores, route return by route | Read case; read COLLINS output; propose route | Nothing; a person approves the route | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons | Acceptance; recovery by route against the rule | E4 | E3 |
| Guarantee claim agent | Guarantees meeting claim conditions | Prepares the TCG and guarantee claim and checks the checklist | Guarantee, case, documents | Read case; assemble claim; raise task | Nothing; the guarantee officer approves | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons | Claims accepted first time | E4 | E3 |
| Reconciliation agent | Unmatched receipts | Matches receipts to cases and accounts | Payments, proceeds, open treatments | Read payments; match proceeds; raise exception | Matches with one candidate case and an exact amount | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons | Auto-match accuracy; exceptions | E4 | E3 |
| Legal document agent | Notice periods ending | Assembles the litigation pack and checks it against the defect list | Documents, case, legal template | Read documents; assemble pack; raise retrieval request | Pack assembly; a person verifies | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons | Packs accepted first time | E5 | E4 |
| Debt sale agent | Debt sale cycle opened | Builds lots from eligible accounts and prepares the masked data tape | Eligible accounts, balances, history | Read case list; build lot; build tape | Nothing; the committee approves | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons | Lots approved without change | E5 | E4 |
| Write-off agent | Monthly write-off scan | Prepares the write-off pack and proposes write off or pursue | Balance, provision, route history, legal and asset state | Read case; build pack | Nothing; the committee approves | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons | Packs accepted; removals | E6 | E5 |
| Tracing agent | X6 lost contact | Finds a lost customer through permitted sources | Contact points, interaction ledger, partner results | Read case; request trace from partner; propose contact update | Trace requests within policy; a new contact point is verified before use | Below the confidence floor, outside the band, or a guardrail failure: to the owner's queue with reasons | Contacts restored | E7 | E6 |

## Decision steps

| Steps by agent |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
| Sub-decisions each agent serves, with the autonomy level at go-live and the target. |  |  |  |  |  |  |  |
| Step | Sub-decision | Mode | Run by | Model | Autonomy at go-live | Target | First in |
| D5.1 | Affordability | Automated | ACE restructure calculator | TDR scheme suggester models (CRR_RET_372 Mortgage, CRR_RET_373 SSME) | L0 | L0 | E2 |
| D5.2 | Plan to offer | Automated | Settlement and restructure agent | TDR scheme suggester | L2 | L3 | E3 |
| D5.3 | Reassess after a broken plan | Advised | Settlement and restructure agent | C-score models | L1 | L2 | E3 |
| D6.1 | Accept the appraisal value | Advised | Valuation agent | Asset pricing model (CRR_RET_380) | L1 | L2 | E3 |
| D6.2 | Return by route | Automated | COLLINS | Route return models | L0 | L0 | E4 |
| D6.3 | Route | Advised | Route agent | Route return models; C-score models | L1 | L2 | E4 |
| D6.4 | Settlement amount and terms | Advised | Settlement and restructure agent | None | L1 | L2 | E3 |
| D6.5 | Thai Credit Guarantee claim | Advised | Guarantee claim agent | None | L1 | L2 | E4 |
| D6.6 | Guarantor and co-borrower pursuit | Person | Case owner | None | L0 | L0 | E4 |
| D7.1 | Demand and recall notices | Automated | Rules component | None | L0 | L0 | E2 |
| D7.2 | Document pack complete | Advised | Legal document agent | OCR and extraction | L1 | L3 | E5 |
| D7.3 | Which law firm | Automated | Rules component | Partner scorecard | L0 | L0 | E5 |
| D7.4 | Settle before judgment, appeal, fees | Advised | Legal document agent | None | L1 | L1 | E5 |
| D7.5 | Enforce: trace, writ, seizure, auction | Partner | Tracing agent; law firm | None | L1 | L2 | E5 |
| D8.1 | Asset on the books, holding age, reappraisal | Automated | Rules component | None | L0 | L0 | E3 |
| D8.2 | Start and floor price | Advised | Pricing agent | Asset auction sale price (CRR_RET_392); success rate (CRR_RET_393); car auction price and sell rate (CRR_RET_371, CRR_RET_370) | L1 | L2 | E3 |
| D8.3 | RAMC transfer, buy-back, rental | Advised | Pricing agent | Asset pricing model (CRR_RET_380) | L1 | L1 | E4 |
| D8.4 | Debt sale lots, buyer terms, award | Advised | Debt sale agent | None | L1 | L2 | E5 |
| D9.1 | Eligibility and tax criteria | Automated | Rules component | None | L0 | L0 | E6 |
| D9.2 | Write off or pursue | Advised | Write-off agent | None | L1 | L1 | E6 |
| D9.3 | Recovery after charge-off | Advised | Write-off agent | None | L1 | L2 | E6 |
| X1-X7 | Deviation screening at entry and on events | Advised | Screening agent | None | L1 | L2 | E2 |
| X6 | Trace a lost customer | Automated | Tracing agent | None | L2 | L3 | E7 |
| P8 | Match receipts to cases | Automated | Reconciliation agent | None | L2 | L3 | E4 |
| P5 | Classify and extract documents | Automated | Intake agent | OCR and extraction | L2 | L3 | E2 |

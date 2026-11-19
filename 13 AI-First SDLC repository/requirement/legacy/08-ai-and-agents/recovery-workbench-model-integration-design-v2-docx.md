<!-- source: 08 AI and agents/Recovery Workbench Model Integration Design v2.docx -->
<!-- converted: 2026-11-04 from DOCX -->

> **Source:** `08 AI and agents/Recovery Workbench Model Integration Design v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Model integration design

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench model integration design |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | arc42 building block view, C4 container view |

# 1. How models reach the Workbench

The bank's models run in COLLINS and ACE under the bank model risk standard. The Workbench does not run models. It reads their output from the daily COLLINS load (INT-08) and, for agents, calls the model endpoint through the agent platform (DL33).

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

# 2. Inputs and outputs

| Item | Design |
|---|---|
| Inputs | Prepared by COLLINS from the bank's data; the Workbench sends no data to the models |
| Output | One row per account and model each day: score, band, model ID, model version and business date (score entity, DP11) |
| Use | Rules read the band; agents read the score and reasons; the decision log records the model ID and version used |
| Freshness | End of day; monthly for some models. A score older than its age limit is not used and the rule result is used instead |

# 3. Changing a model without a release

- Model Risk validates the new version under the bank standard.

- COLLINS publishes the new version's output with its version in the load.

- The model version in force for each decision step is reference data; the center of excellence loads the change and Risk approves it.

- Decisions from the valid from date use the new version; earlier decisions keep theirs.

- Champion and challenger runs are set by the same table, with a share of cases per version.

# 4. The large language model endpoint

- Reached only through the agent platform's tool gateway; no Workbench code calls it directly.

- A private endpoint in the SCB tenant (DL33).

- Prompts carry only the fields the step needs; no clear identifiers.

- Prompt, policy and model versions are recorded on each run.

# 5. Monitoring

| Measure | Owner | Reviewed |
|---|---|---|
| Score coverage: accounts with a current score | Data steward | Daily |
| Drift against the development sample | Model Risk | Monthly |
| Outcome against prediction by band | Center of excellence | Quarterly |

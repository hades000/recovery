<!-- source: 06 Data/Recovery Workbench Reporting and Analytics Data Model v2.xlsx -->
<!-- converted: 2026-11-04 from XLSX -->

> **Source:** `06 Data/Recovery Workbench Reporting and Analytics Data Model v2.xlsx`  
> **Converted from:** XLSX

## Facts

| Fact tables |  |  |  |  |  |
|---|---|---|---|---|---|
| Star schema in the data lake for Power BI, refreshed from the nightly extract. |  |  |  |  |  |
| Table | Grain | Dimensions | Measures | Source entities | Refresh |
| fact_case_daily | One row per open case per day | case, date, product, stage, route, owner, team, queue | open flag, days in state, breached flag, balance | recovery_case, timer, loan_account | Nightly |
| fact_decision | One row per decision log entry | case, date, decision, rule, approver, agent | count, override flag, fallback flag, amount | decision_log_entry | Nightly |
| fact_treatment | One row per treatment | case, date, product, treatment type, status | offer amount, approved amount, booked amount, days to book | treatment | Nightly |
| fact_legal | One row per legal action | case, date, firm, court, status | days to file, days to judgment, court fees | legal_action, hearing | Nightly |
| fact_asset | One row per asset per month | asset, month, type, region, status | book value, holding cost, list price, sale price, days held | asset, listing, asset_sale | Nightly |
| fact_lot | One row per lot | lot, buyer, date | balance, reserve, price, put-backs | debt_sale_lot, debt_sale_account | Nightly |
| fact_recovery | One row per receipt | case, date, route, product, source | amount, principal resolved | proceeds, write_off | Nightly |
| fact_partner | One row per instruction | partner, case, date, type | days to complete, breached flag, fee | partner_instruction | Nightly |
| fact_flow | One row per bucket per month | month, product, bucket | opening balance, forward flow balance, flow rate | COLLINS | Monthly |

## Dimensions

| Dimensions |  |
|---|---|
| Shared by every fact table. |  |
| Table | Holds |
| dim_date | Calendar with bank holidays and business days |
| dim_product | Mortgage, hire purchase, SSME and the product codes |
| dim_route | Routes from LOV-ROUTE |
| dim_stage | Stages from LOV-STAGE |
| dim_org | Team, region, queue and owner, with history |
| dim_partner | Partner firm and type |
| dim_rule | Rule and version |
| dim_decision | D1 to D9 and sub-decisions |

## Measures

| Measure definitions |  |  |
|---|---|---|
| Each management measure, its formula and the fact table it reads. |  |  |
| Measure | Formula | From |
| Recovery rate | Sum of amount / sum of principal resolved | fact_recovery |
| Turnaround to book | Median days to book | fact_treatment |
| Litigation turnaround | Median days to file | fact_legal |
| NPA sales cycle | Median days held at sale | fact_asset |
| Cases inside the service level | Open cases not breached / open cases | fact_case_daily |
| Recommendations accepted | Decisions without override / decisions with a recommendation | fact_decision |
| Agent fallback rate | Fallbacks / agent steps | fact_decision |
| Flow rate by bucket | Forward flow balance / opening balance | fact_flow |
| Loss on NPL sale | 1 - price / balance sold | fact_lot |
| Partner service level met | Instructions not breached / instructions | fact_partner |

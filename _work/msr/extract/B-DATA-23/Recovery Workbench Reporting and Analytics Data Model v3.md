## Sheet: Facts

| Fact tables |  |  |  |  |  |
|---|---|---|---|---|---|
| Star schema in the data lake for Power BI. ACE source rows are read through recovery.v_ace_* views; Workbench rows come from the recovery tables. No source system is loaded directly. |  |  |  |  |  |
| Table | Grain | Dimensions | Measures | Source entities | Refresh |
| fact_case_daily | One row per open case per day | case, date, product, stage, route, owner, team, queue | open flag, days in state, breached flag, balance | recovery_case, timer, v_ace_account | Read through v_ace_account; nightly |
| fact_decision | One row per decision log entry | case, date, decision, rule, approver, agent | count, override flag, fallback flag, amount | decision_log_entry | Nightly from the Workbench |
| fact_treatment | One row per treatment | case, date, product, treatment type, status | offer amount, approved amount, booked amount, days to book | treatment, v_ace_plan | Read through v_ace_plan; nightly |
| fact_legal | One row per legal action | case, date, firm, court, status | days to file, days to judgment, court fees | legal_action, v_ace_lawsuit, v_ace_hearing | Read through v_ace_lawsuit and v_ace_hearing; nightly |
| fact_asset | One row per asset per month | asset, month, type, region, status | book value, holding cost, list price, sale price, days held | v_ace_asset, v_ace_npa_asset, listing, asset_sale | Read through v_ace_asset and v_ace_npa_asset; nightly |
| fact_lot | One row per lot | lot, buyer, date | balance, reserve, price, put-backs | debt_sale_lot, debt_sale_account | Nightly from the Workbench |
| fact_recovery | One row per receipt | case, date, route, product, source | amount, principal resolved | proceeds, write_off, v_ace_payment, v_ace_write_off | Read through v_ace_payment and v_ace_write_off; nightly |
| fact_partner | One row per instruction | partner, case, date, type | days to complete, breached flag, fee | partner_instruction | Nightly from the Workbench |
| fact_flow | One row per bucket per month | month, product, bucket | opening balance, forward flow balance, flow rate | v_ace_bucket_log | Read through v_ace_bucket_log; monthly |

## Sheet: Dimensions

| Dimensions |  |
|---|---|
| Shared by every fact table. |  |
| Table | Holds |
| dim_date | Calendar with bank holidays and business days; holidays read through v_ace_holiday |
| dim_product | Mortgage, hire purchase, SSME and the product codes; product codes read through v_ace_product |
| dim_route | Routes from LOV-ROUTE |
| dim_stage | Stages from LOV-STAGE |
| dim_org | Team, region, queue and owner, with history |
| dim_partner | Partner firm and type |
| dim_rule | Rule and version |
| dim_decision | D1 to D9 and sub-decisions |

## Sheet: Measures

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

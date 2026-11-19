<!-- source: 03 Requirements and specifications/Recovery Workbench Reporting and Management Information Requirements v2.docx -->
<!-- converted: 2026-11-04 from DOCX -->

> **Source:** `03 Requirements and specifications/Recovery Workbench Reporting and Management Information Requirements v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Reporting and management information requirements

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench reporting and management information requirements |
| Version | 1 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Structure | ISO/IEC/IEEE 29148 |

# 1. Reports and dashboards

| ID | Report | Who reads it | How often | Decision it supports |
|---|---|---|---|---|
| RPT-01 | CEO update | CEO, sponsors | Every two weeks | Whether recovery and the program are on track |
| RPT-02 | Steering committee pack | Steering committee | Monthly | Scope, budget, risks and decisions above the program |
| RPT-03 | Steering dashboard | Product heads, Chief Debt Recovery Management Office | Daily | Where recovery is behind and why |
| RPT-04 | Queue and caseload | Team managers | Daily | Who needs help and which cases are at risk |
| RPT-05 | Litigation service levels | Head of Litigation | Weekly | Which packs and firms are late |
| RPT-06 | Settlement and deed in lieu | Product heads | Weekly | Whether treatments reach booking |
| RPT-07 | NPA stock and sales | Head of NPA | Weekly | What is unsold and why |
| RPT-08 | Debt sale and internal AMC | Head of Asset Liquidity | Per lot; monthly | Whether lots achieve their reserve and the uplift against debt sale |
| RPT-09 | Write-off and recovery after charge-off | Finance and CFO delegate | Monthly | What is written off and recovered |
| RPT-10 | Partner scorecard | Partner and agency manager | Monthly | Which partners get more or less work |
| RPT-11 | Decision and agent monitor | Risk and model risk officer, center of excellence | Weekly | Whether rules and agents decide well |
| RPT-12 | Data health | Data steward | Daily | Whether the data can be trusted today |
| RPT-13 | Audit and controls | Internal audit, Compliance | Quarterly | Whether controls ran |
| RPT-14 | Regulatory returns | Compliance, Finance | As the regulator requires | BOT reporting obligations |

# 2. Measures on each

| ID | Measures | Built in | First in |
|---|---|---|---|
| RPT-01 | Flow rate B1 to B3, % recovery, NPL reduction, NPA sales, program status by epic, decisions needed | Steering dashboard | E2 |
| RPT-02 | Project KPIs against the scorecard; benefits; risks; decisions | Steering dashboard | E2 |
| RPT-03 | Inflow, stock, cures, recovery by route and product, turnaround, cost | Power BI from the data lake | E2 |
| RPT-04 | Cases per owner against the cap, age in state, breached service levels, exception queues | Workbench | E2 |
| RPT-05 | Document preparation SLA (target 60%), legal SLA (target 95%), time to file, firm scorecard | Power BI | E5 |
| RPT-06 | Offers, approvals, bookings, turnaround, below-floor approvals | Power BI | E3 |
| RPT-07 | Stock by age, holding cost, listings, sales against floor, NPA sales amount | Power BI | E3 |
| RPT-08 | Lots, bids against reserve, recovery uplift versus debt sales (target 45%), put-backs | Power BI | E6 |
| RPT-09 | Population, approvals, postings, recovery after write-off | Power BI | E6 |
| RPT-10 | Results, service levels, cost, conduct by partner | Workbench | E7 |
| RPT-11 | Acceptance, overrides by reason, fallbacks, outcomes by route against rule-only | Workbench and Power BI | E2 |
| RPT-12 | Loads, checks, breaks, stale products | Workbench | E1 |
| RPT-13 | Control evidence by control ID; access reviews; decision log chain | Workbench export | E2 |
| RPT-14 | Repossessed vehicles and loss on sale; relief scheme results | Power BI | E8 |

# 3. Rules

- Every number comes from the decision log, the Workbench records or a named system of record; none is counted by hand.

- Each report shows the business date of its data.

- Reports carry the masking of the reader's role; management reports carry no personal data.

- Definitions follow the business measures and targets workbook.

# 4. Refresh

| Source | Refresh |
|---|---|
| Workbench screens | Live |
| Power BI from the data lake | Nightly after the reporting extract (JOB-15) |
| Scorecard measures | Monthly at the fifth working day |

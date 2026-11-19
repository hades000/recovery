<!-- source: 06 Data/Recovery Workbench Volume and Scale Forecast v2.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `06 Data/Recovery Workbench Volume and Scale Forecast v2.xlsx`  
> **Converted from:** XLSX

## Inputs

| Inputs: facts and assumptions |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| Every figure in the forecast is calculated from these rows. Facts come from bank files; assumptions are named, with the effect if they move. Change a value here to rerun the forecast. |  |  |  |  |  |  |
| ID | Measure | Value | Unit | Kind | Source or basis | Effect if it moves |
| I01 | Mortgage accounts at 90 days past due or more | 12256 | accounts | Fact | Inventory reports, 30 June 2026 | Opening open cases |
| I02 | Hire purchase accounts at 90 days past due or more, active inventory | 12960 | accounts | Fact | Inventory reports, 30 June 2026 | Opening open cases |
| I03 | Hire purchase accounts at 90 days past due or more, all on the books | 169311 | accounts | Fact | Inventory reports, 30 June 2026 | Case history to load once; storage |
| I04 | SSME accounts at 90 days past due or more | 2903 | accounts | Fact | Inventory reports, 30 June 2026 | Opening open cases |
| I05 | New Mortgage accounts reaching 90 days past due each month | 808 | accounts a month | Fact | Inventory reports, average July 2025 to June 2026 | Every monthly volume |
| I06 | New hire purchase accounts reaching 90 days past due each month | 1816 | accounts a month | Fact | Inventory reports, average July 2025 to June 2026 | Every monthly volume |
| I07 | New SSME accounts reaching 90 days past due each month | 486 | accounts a month | Fact | Inventory reports, average July 2025 to June 2026 | Every monthly volume |
| I08 | Accounts per case | 1.2 | accounts | Assumption | One case per customer per product (DL17) | Cases fall as it rises |
| I09 | Growth in new accounts a year | 0.15 | percent | Assumption | The last six months ran 24 to 42 percent above the six before | At 35 percent, 2031 inflow is about 2.5 times the base |
| I10 | Share of open cases that close each month | 0.11 | percent | Assumption | Monthly inflow over the active stock at 30 June 2026 | Open cases rise if it falls |
| I11 | Documents per new case | 15 | documents | Assumption | Hand-over pack, notices and agreements | Storage scales with it |
| I12 | Documents per open case each month | 1 | documents | Assumption | Letters, proofs of delivery, partner reports | Storage scales with it |
| I13 | Average document size | 0.5 | MB | Assumption | Scanned A4 pages | Storage scales with it |
| I14 | Interactions per open case each month | 4 | entries | Assumption | Contacts, letters, promises, payments, hand-overs | Ledger size scales with it |
| I15 | Decisions per new case at entry | 3 | entries | Assumption | Entry, allocation and the deviation screen | Decision log size |
| I16 | Decisions per open case each month | 2 | entries | Assumption | Route steps, approvals, timers | Decision log size |
| I17 | Rule evaluations per open case each month | 12 | evaluations | Assumption | Events per state, from the routing rules | Rules component load |
| I18 | Decision log entry size | 4 | KB | Assumption | Inputs reference, recommendation and actions as JSON | Database size |
| I19 | Interaction entry size | 2 | KB | Assumption | Summary text and codes | Database size |
| I20 | Lawsuits filed each month, Mortgage and SSME | 667 | lawsuits a month | Fact | Litigation sent file, average July 2025 to June 2026 | Litigation work |
| I21 | Vehicles repossessed each month | 720 | vehicles a month | Fact | Repossession file, average July 2025 to June 2026 | Asset records |
| I22 | Registered letters each month | 1909 | letters a month | Fact | Registered letter file, July 2025 to June 2026 | Notice dispatch and proof of delivery |
| I23 | NPA properties held | 4736 | assets | Fact | NPA stock file, 6 July 2026 | Asset records |
| I24 | NPA properties sold each month | 29 | assets a month | Fact | NPA sales file, 2025 | Disposal work |
| I25 | Accounts sold in debt sales each year | 3783 | accounts a year | Fact | Debt sale file, 2024 to June 2026 | Debt sale records |
| I26 | Accounts under restructure | 173807 | accounts | Fact | Restructure list, 30 June 2026 | Restructure monitoring |
| I27 | Recovery staff who work cases in the Workbench | 466 | people | Fact | Staff by job role, 30 June 2026, less phone and field collections | Named users |
| I28 | Collections staff who read the case record | 448 | people | Fact | Phone and field collections officers, 30 June 2026 | Named users |
| I29 | Partner users | 320 | people | Assumption | 73 agencies, 11 to 12 law firms, valuers, 4 auction vendors, buyers | Named users |
| I30 | Share of bank users online in the busiest hour | 0.4 | percent | Assumption | Office hours work on queues | Peak load |
| I31 | Share of partner users online in the busiest hour | 0.15 | percent | Assumption | Partners enter results in batches | Peak load |
| I32 | Requests per active user a minute | 3 | requests | Assumption | Screen loads and saves | Peak requests a second |

## Monthly

| Monthly forecast, first 14 months |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|
| Calculated from the Inputs tab. Open cases start from the active stock at go-live and change by new cases less closures. |  |  |  |  |  |  |  |  |
| Month | New accounts at 90 days past due | New cases | Open cases | Documents added | Document storage added (GB) | Interactions | Decision log entries | Rule evaluations |
| Nov 2026 |  |  |  |  |  |  |  |  |
| Dec 2026 |  |  |  |  |  |  |  |  |
| Jan 2027 |  |  |  |  |  |  |  |  |
| Feb 2027 |  |  |  |  |  |  |  |  |
| Mar 2027 |  |  |  |  |  |  |  |  |
| Apr 2027 |  |  |  |  |  |  |  |  |
| May 2027 |  |  |  |  |  |  |  |  |
| Jun 2027 |  |  |  |  |  |  |  |  |
| Jul 2027 |  |  |  |  |  |  |  |  |
| Aug 2027 |  |  |  |  |  |  |  |  |
| Sep 2027 |  |  |  |  |  |  |  |  |
| Oct 2027 |  |  |  |  |  |  |  |  |
| Nov 2027 |  |  |  |  |  |  |  |  |
| Dec 2027 |  |  |  |  |  |  |  |  |

## Five years

| Five-year forecast |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|
| Calculated from the Inputs tab. Open cases are the steady state for the year's inflow. Storage and database size are cumulative from go-live. |  |  |  |  |  |  |  |  |
| Year | New accounts at 90 days past due | New cases | Open cases, steady state | Documents added | Documents held | Document storage (TB) | Decision log entries | Log and ledger size (GB) |
| 2027 |  |  |  |  |  |  |  |  |
| 2028 |  |  |  |  |  |  |  |  |
| 2029 |  |  |  |  |  |  |  |  |
| 2030 |  |  |  |  |  |  |  |  |
| 2031 |  |  |  |  |  |  |  |  |

## Users and load

| Users and peak load |  |  |  |  |
|---|---|---|---|---|
| Calculated from the Inputs tab. |  |  |  |  |
| Group | Named users | Online in the busiest hour | Concurrent users | Requests a second |
| Recovery staff |  |  |  |  |
| Collections staff reading the case record |  |  |  |  |
| Partner users |  |  |  |  |
| Total |  |  |  |  |

## Route activity

| Route activity today |  |  |
|---|---|---|
| The work each route produces, from bank files. Calculated from the Inputs tab. |  |  |
| Activity | A month | A year |
| Lawsuits filed |  |  |
| Vehicles repossessed |  |  |
| Registered letters |  |  |
| NPA properties sold |  |  |
| Accounts sold in debt sales |  |  |

## Key

| Key |  |  |
|---|---|---|
| What each kind and term means. |  |  |
| Item | Term | Meaning |
| Kind | Fact | Taken from a bank file, named in the Source column |
| Kind | Assumption | Set by the forecast, with the effect if it moves. Confirmed by the bank |
| Term | Active inventory | Accounts at 90 days past due or more that the bank works now |
| Term | Open cases | Cases on the Workbench that have not closed |
| Standard | ISO/IEC 25010 | Performance efficiency: time behavior, resource use and capacity |

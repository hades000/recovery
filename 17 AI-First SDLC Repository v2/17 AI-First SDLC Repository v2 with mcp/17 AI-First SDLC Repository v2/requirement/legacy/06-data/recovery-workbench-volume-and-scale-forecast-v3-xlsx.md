<!-- source: 06 Data/Recovery Workbench Volume and Scale Forecast v3.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `06 Data/Recovery Workbench Volume and Scale Forecast v3.xlsx`  
> **Converted from:** XLSX

## Inputs

| Inputs: facts and assumptions |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| Every figure in the forecast is calculated from these rows. Facts come from bank files; assumptions are named, with the effect if they move. Change a value here to rerun the forecast. |  |  |  |  |  |  |
| ID | Measure | Value | Unit | Kind | Source or basis | Effect if it moves |
| I01 | Mortgage accounts at 90 days past due or more | 12256 | accounts | Fact | Inventory reports, 30 June 2026 | Opening open cases |
| I02 | Hire purchase accounts at 90 days past due or more, active inventory | 12960 | accounts | Fact | Inventory reports, 30 June 2026 | Opening open cases |
| I03 | Hire purchase accounts at 90 days past due or more, all on the books | 169311 | accounts | Fact | Inventory reports, 30 June 2026 | Nothing in the Workbench: the accounts stay in ACE and are read through v_ace_account |
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
| I33 | Share of screen actions that read a v_ace_* view | 0.6 | percent | Assumption | Account, party and contact facts on every case screen | View read load rises with it |
| I34 | View reads per screen action | 2 | reads | Assumption | One account read and one party or contact read | Each read is one view query |

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

| Five-year forecast |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|
| Calculated from the Inputs tab. Open cases are the steady state for the year's inflow. Storage and database size are cumulative from go-live. |  |  |  |  |  |  |  |  |  |
| Year | New accounts at 90 days past due | New cases | Open cases, steady state | Documents added | Documents held | Document storage (TB) | Decision log entries | Log and ledger size (GB) | ACE growth, cumulative (GB) |
| 2027 |  |  |  |  |  |  |  |  |  |
| 2028 |  |  |  |  |  |  |  |  |  |
| 2029 |  |  |  |  |  |  |  |  |  |
| 2030 |  |  |  |  |  |  |  |  |  |
| 2031 |  |  |  |  |  |  |  |  |  |

## Users and load

| Users and peak load |  |  |  |  |
|---|---|---|---|---|
| Calculated from the Inputs tab. |  |  |  |  |
| Group | Named users | Online in the busiest hour | Concurrent users | Requests a second |
| Recovery staff |  |  |  |  |
| Collections staff reading the case record |  |  |  |  |
| Partner users |  |  |  |  |
| Total |  |  |  |  |

## Read path

_Merged ranges: C15:D15, C14:D14, C13:D13, C16:D16_

| Read path and load window |  |  |  |
|---|---|---|---|
| The Workbench reads ACE through recovery.v_ace_* views. It runs no inbound load, so the cost is the read concurrency below and the growth the 14 new ACE tables add. |  |  |  |
| Measure | Value | Unit | Basis |
| Named users |  | people | Recovery staff, collections staff and partner users |
| Concurrent users in the busiest hour |  | users | 40 percent of bank users and 15 percent of partner users are online |
| Share of screen actions that read a view |  | percent | Account, party and contact facts on every case screen |
| Concurrent view reads |  | reads | One for each concurrent user whose current action reads a view |
| Requests a second at peak |  | requests | Three requests a minute for each active user |
| View reads a second at peak |  | reads a second | Two view reads for each action that reads a view |
| Peak view reads a second with a 3x burst |  | reads a second | Covers queue refresh, report open and a batch of saves |
| Item | Answer | Note |  |
| Workbench inbound load window | None | No source batch runs in the Workbench. Every source row lands in ACE through ACE ingestion. |  |
| Scheduled Workbench jobs | 3 | Outbound queue dispatch, lake refresh and case list reconciliation; none reads a source system. | Outbound queue dispatch, lake refresh and case list reconciliation; none reads a source system. |
| Source freshness | v_ace_batch_status | data_product_load is the Workbench freshness stamp. It is sourced from ace_batch_run, read through v_ace_batch_status, which gives the ACE per-source business date. | data_product_load is the Workbench freshness stamp. It is sourced from ace_batch_run, read through v_ace_batch_status, which gives the ACE per-source business date. |

## ACE growth

| ACE database growth from the 14 new tables |  |  |  |  |
|---|---|---|---|---|
| What RWB-ACE-001 adds to ACE, at the 2027 volumes in this forecast. The tables are read-only for the Workbench; the storage belongs to the ACE database. |  |  |  |  |
| ACE object | Rows a year | KB a row | KB a year | Basis |
| ace_batch_run |  | 0.5 |  | One row per source per business day, 14 sources |
| valuation |  | 1.5 |  | One appraisal for every second new case |
| collateral_detail |  | 2 |  | One detail row per appraised collateral |
| npa_asset |  | 2 |  | 720 vehicles and 29 properties a month |
| npa_sale |  | 1.5 |  | 29 NPA properties sold a month |
| lawsuit |  | 2 |  | 667 lawsuits filed a month |
| hearing |  | 0.5 |  | Two hearings for each lawsuit |
| pod_receipt |  | 1 |  | 1,909 registered letters a month |
| gl_write_off |  | 1 |  | Three write-offs for every ten new cases |
| collins_score |  | 1 |  | Two scores for each new case |
| party_product |  | 0.5 |  | One row for each account in the active inventory |
| credit_decision |  | 1 |  | One credit decision for each new case |
| esign_request |  | 1 |  | Four signature requests for every ten new cases |
| iam_group | 40 | 0.5 |  | One row per Entra group mapped to a role |
| Total, 14 tables |  |  |  | 166 columns in all; 12 further columns are added to existing ACE tables |
| Five-year rows |  | rows |  | At 15 percent growth a year from the 2027 rate |
| Five-year size |  | GB |  | Cumulative from go-live |
| Share of a 2 TB ACE database |  | percent |  | Under a tenth of one percent |

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
| Term | View read | A SELECT on a recovery.v_ace_* view by a screen or by the lake refresh |
| Term | Load window | A period set aside to load source data. The Workbench has none |
| Term | Tier 2 | The 14 tables and 12 columns that RWB-ACE-001 adds to ACE |
| Term | ACE growth | The storage the 14 new tables add to the ACE database, cumulative from go-live |

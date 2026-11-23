<!-- source: 06 Data/Recovery Workbench Volume and Scale Forecast v3.pptx -->
<!-- converted: 2026-11-16 from PPTX -->

> **Source:** `06 Data/Recovery Workbench Volume and Scale Forecast v3.pptx`  
> **Converted from:** PPTX

## Slide 1

SCB

COLLECTIONS AND RECOVERY TRANSFORMATION Recovery Workbench: volume and scale forecast

Henka Group, 15 November 2026 (C) Siam Commercial Bank and Henka Pte Ltd

## Slide 2

The volumes on one page

2

28,119 Accounts at 90 days past due, active Mortgage, hire purchase and SSME, 30 June 2026

3,110 New accounts at 90 days past due a month Average of the last 12 months

26,479 Open cases at the end of 2027 With 15 percent growth a year

414 Concurrent users in the busiest hour Of 1,234 named users

5,809,312 Documents held at the end of 2031 2.8 TB of storage

36 GB Decision log and ledger at the end of 2031 In the ACE database

Counts are accounts from the bank's inventory reports. Cases are accounts divided by 1.2, one case per customer per product (DL17). The bank confirms the growth assumption.

## Slide 3

Where the volumes start

3

Hire purchase holds 156,351 further accounts at 90 days past due outside the active inventory. They stay in ACE and are read through v_ace_account: nothing is loaded, and they are not counted as open cases.

| Measure | Value | Basis |
|---|---|---|
| Mortgage accounts at 90 days past due or more | 12,256 | Inventory reports, 30 June 2026 |
| Hire purchase accounts at 90 days past due or more, active inventory | 12,960 | Inventory reports, 30 June 2026 |
| Hire purchase accounts at 90 days past due or more, all on the books | 169,311 | Inventory reports, 30 June 2026 |
| SSME accounts at 90 days past due or more | 2,903 | Inventory reports, 30 June 2026 |
| New Mortgage accounts reaching 90 days past due each month | 808 | Inventory reports, average July 2025 to June 2026 |
| New hire purchase accounts reaching 90 days past due each month | 1,816 | Inventory reports, average July 2025 to June 2026 |
| New SSME accounts reaching 90 days past due each month | 486 | Inventory reports, average July 2025 to June 2026 |
| Accounts under restructure | 173,807 | Restructure list, 30 June 2026 |

## Slide 4

The first 14 months

4

| Month | New accounts at 90 days | New cases | Open cases | Documents added | Decision log entries | Rule evaluations |
|---|---|---|---|---|---|---|
| Nov 2026 | 3,258 | 2,715 | 23,570 | 64,299 | 55,286 | 282,842 |
| Dec 2026 | 3,296 | 2,747 | 23,725 | 64,931 | 55,690 | 284,694 |
| Jan 2027 | 3,335 | 2,779 | 23,894 | 65,583 | 56,126 | 286,729 |
| Feb 2027 | 3,374 | 2,812 | 24,078 | 66,255 | 56,591 | 288,931 |
| Mar 2027 | 3,414 | 2,845 | 24,274 | 66,945 | 57,082 | 291,285 |
| Apr 2027 | 3,454 | 2,878 | 24,482 | 67,653 | 57,598 | 293,781 |
| May 2027 | 3,494 | 2,912 | 24,701 | 68,377 | 58,136 | 296,406 |
| Jun 2027 | 3,535 | 2,946 | 24,929 | 69,118 | 58,696 | 299,153 |
| Jul 2027 | 3,576 | 2,980 | 25,168 | 69,874 | 59,276 | 302,011 |
| Aug 2027 | 3,618 | 3,015 | 25,414 | 70,644 | 59,875 | 304,974 |
| Sep 2027 | 3,661 | 3,051 | 25,670 | 71,429 | 60,491 | 308,034 |
| Oct 2027 | 3,704 | 3,086 | 25,932 | 72,228 | 61,124 | 311,187 |
| Nov 2027 | 3,747 | 3,123 | 26,202 | 73,041 | 61,772 | 314,427 |
| Dec 2027 | 3,791 | 3,159 | 26,479 | 73,866 | 62,436 | 317,750 |

## Slide 5

Five years

5

Open cases are the steady state for each year's inflow at an 11 percent monthly closure rate. Documents and the log are kept from go-live; retention is DL26. The 14 ACE tables that RWB-ACE-001 adds grow to 1.8 GB over the five years, and there is no Workbench load window: every source field and the case list are read through recovery.v_ace_* views.

| Year | New accounts at 90 days | New cases | Open cases | Documents held | Storage (TB) | Log and ledger (GB) |
|---|---|---|---|---|---|---|
| 2027 | 42,918 | 35,765 | 27,095 | 861,611 | 0.4 | 5 |
| 2028 | 49,356 | 41,130 | 31,159 | 1,852,464 | 0.9 | 12 |
| 2029 | 56,759 | 47,299 | 35,833 | 2,991,945 | 1.4 | 19 |
| 2030 | 65,273 | 54,394 | 41,208 | 4,302,349 | 2.1 | 27 |
| 2031 | 75,064 | 62,553 | 47,389 | 5,809,312 | 2.8 | 36 |

## Slide 6

Users and peak load

6

At three requests a minute for each active user, the busiest hour runs about 21 requests a second, well inside one ACE service on the shared AKS clusters. Six actions in ten read a v_ace_* view, so 248 users read a view at once and the peak is 25 view reads a second, or 74 with a 3x burst.

| Group | Named users | Online in the busiest hour | Concurrent | Requests a second |
|---|---|---|---|---|
| Recovery staff | 466 | 40% | 186 | 9 |
| Collections staff reading the case record | 448 | 40% | 179 | 9 |
| Partner users | 320 | 15% | 48 | 2 |
| Total | 1,234 |  | 414 | 21 |

## Slide 7

The work each route produces today

7

| Activity | A month | A year | Basis |
|---|---|---|---|
| Lawsuits filed, Mortgage and SSME | 667 | 8,004 | Litigation sent file |
| Vehicles repossessed | 720 | 8,640 | Repossession file |
| Registered letters | 1,909 | 22,908 | Registered letter file |
| NPA properties sold | 29 | 348 | NPA sales file |
| Accounts sold in debt sales | 315 | 3,783 | Debt sale file |
| NPA properties held |  | 4,736 | NPA stock file |

## Slide 8

The assumptions, and what moves if they do

8

|  | Assumption | Value | Effect if it moves |
|---|---|---|---|
| I08 | Accounts per case | 1.2 | Cases fall as it rises |
| I09 | Growth in new accounts a year | 15% | At 35 percent, 2031 inflow is about 2.5 times the base |
| I10 | Share of open cases that close each month | 11% | Open cases rise if it falls |
| I11 | Documents per new case | 15 | Storage scales with it |
| I12 | Documents per open case each month | 1 | Storage scales with it |
| I13 | Average document size | 0.5 | Storage scales with it |
| I14 | Interactions per open case each month | 4 | Ledger size scales with it |
| I15 | Decisions per new case at entry | 3 | Decision log size |
| I16 | Decisions per open case each month | 2 | Decision log size |
| I17 | Rule evaluations per open case each month | 12 | Rules component load |
| I18 | Decision log entry size | 4 | Database size |
| I19 | Interaction entry size | 2 | Database size |
| I29 | Partner users | 320 | Named users |
| I30 | Share of bank users online in the busiest hour | 40% | Peak load |
| I31 | Share of partner users online in the busiest hour | 15% | Peak load |
| I32 | Requests per active user a minute | 3 | Peak requests a second |
| I33 | Share of screen actions that read a v_ace_* view | 60% | View read load rises with it |
| I34 | View reads per screen action | 2 | Each read is one view query |

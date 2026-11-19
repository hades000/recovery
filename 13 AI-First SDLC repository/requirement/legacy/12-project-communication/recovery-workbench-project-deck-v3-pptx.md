<!-- source: 12 Project communication/Recovery Workbench Project Deck v3.pptx -->
<!-- converted: 2026-11-04 from PPTX -->

> **Source:** `12 Project communication/Recovery Workbench Project Deck v3.pptx`  
> **Converted from:** PPTX

## Slide 1

SCB

COLLECTIONS AND RECOVERY TRANSFORMATION Recovery Workbench

Henka Group, 28 October 2026 (C) Siam Commercial Bank and Henka Pte Ltd

## Slide 2

What the Recovery Workbench is

2

The Recovery Workbench is the system that owns every recovery case from 90 days past due to close, for Mortgage, Hire Purchase and SSME. It is built as the recovery module of ACE, the bank's collection engine, so collection and recovery work in one application with one case view.

From day 90 to close One case per customer and product, with one owner, one clock and one history

Mortgage, Hire Purchase, SSME Every route: restructure, settlement, deed in lieu, guarantee claim, litigation, asset disposal, debt sale and write-off

Built on ACE One service, one repository and one front end, with data through COLLINS

## Slide 3

Recovery today

3

28,119 Accounts at 90 days past due or more in the active inventory, 30 June 2026

3,110 New accounts reaching 90 days past due each month

667 Lawsuits filed each month for Mortgage and SSME

720 Vehicles repossessed each month

4,736 NPA properties held

916 Staff in the Chief Debt Recovery Management Office

## Slide 4

The problem the Workbench solves

4

Work is spread across systems Collections and recovery staff use 42 applications. A case's facts are held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and the document stores, and no screen shows them together.

Cases are run from spreadsheets Teams keep their own case lists in Excel and SharePoint, build account plans by hand and approve by email. Hand-overs between teams are manual.

Decisions are not recorded in one place Why a route was chosen, who approved it and on what figures is spread across emails and files. Audit findings and fraud cases number 50.

Cases take too long Turnaround is 21 days for litigation, 23 days for a restructure and 26 days for a deed in lieu. The NPA sales cycle is 1,486 days.

## Slide 5

What changes

5

| Area | Today | With the Workbench |
|---|---|---|
| Case list | Each team's Excel and SharePoint list | One case list for every account at 90 days past due or more, reconciled to the core bank |
| Ownership | Agreed between teams by email | One owner per case by rule, with transfers recorded and a clock on every state |
| Choosing the route | Officer judgment, written up in an account plan | Expected return of each route from COLLINS, a recommendation with reasons, approved within the delegation of authority |
| Approvals | Email and paper | Routed to the right approval level, with the limit checked and the decision logged |
| Documents | Folders, shared drives and couriers | One document hub per case, with types read and fields extracted, and custody of originals tracked |
| Partners | Email and spreadsheets | Instructions, results and fees through a partner portal, with a scorecard per partner |
| Rules and limits | In procedures and people's heads | Versioned data rows, changed by a validated load without a code release |
| Evidence | Rebuilt for each audit | One decision log entry per decision, append only |

## Slide 6

How a case moves from day 90 to close

6

Receive the case

Choose the route

Resolve with the customer

Enforce

Realize the asset

Close

| Stage | What it produces |
|---|---|
| Receive the case | One owner, the history from collections, running deadlines and a deviation screen |
| Choose the route | An approved route with the expected return of each option and the reasons |
| Resolve with the customer | A settlement, deed in lieu, guarantee claim or guarantor agreement, booked and reconciled |
| Enforce | A judgment enforced, a settlement before judgment, or proceeds matched to the case |
| Realize the asset | Cash from the asset or the debt: auction, RAMC, buy-back, rental or debt sale |
| Close | The balance written off and posted, recovery after charge-off, the case closed |

## Slide 7

The process architecture

7

19 L1 processes 84 L2 sub-processes and 247 L3 processes. Processes 01 to 05 run in collections before day 90.

| L1 | Process | Decision | L3 | Owner |
|---|---|---|---|---|
| 06 | Take over and own the case | D6 entry | 3 | Recovery Strategy with Risk |
| 07 | Route, settle and claim | D6 | 17 | Recovery Strategy with Risk |
| 08 | Litigate and enforce | D7 | 16 | Head of Litigation |
| 09 | Dispose assets and sell debt | D8 | 28 | Head of NPA; Head of Asset Liquidity |
| 10 | Write off and recover after charge-off | D9 | 9 | Credit Administration with Risk |
| 11 | Handle customer care and deviations | X1 to X7 | 31 | Shared operations |
| 12 | Manage partners | All | 13 | Partner and agency manager |
| 13 | Manage documents and correspondence | All | 14 | Shared operations |
| 14 | Set strategy, policy and decision rules | All | 12 | Center of excellence |
| 15 | Manage performance, data and AI | All | 20 | Center of excellence with Model Risk |
| 16 | Manage risk, control and compliance | All | 14 | Product heads, center of excellence |
| 17 | Run the decision center | D1 to D9 | 6 | Center of excellence |
| 18 | Plan capacity and allocate work | D2, D4 | 6 | Shared operations |
| 19 | Manage payments and reconciliation | D3, D5, D6 | 6 | Credit Administration |

## Slide 8

Who carries out the work

8

Every decision follows five steps: information, decide, outcome, act, log. The approver is set by the approval authority regulation.

| From day 90 to close | L3 processes | Share |
|---|---|---|
| Automated | 38 | 52% |
| AI prepares, a person decides | 17 | 23% |
| A person decides | 7 | 10% |
| Partner | 9 | 12% |
| Manual | 2 | 3% |
| Total | 73 | 100% |

## Slide 9

Decisions and deviations

9

A deviation pauses the stage clock and goes to a named handler. The prescription clock keeps running.

|  | Decision | Where it runs |
|---|---|---|
| D5 | Offer a restructure | EFS and ACE |
| D6 | Which route | Workbench |
| D7 | Next legal step | Workbench |
| D8 | How to dispose | Workbench |
| D9 | Write off or pursue | Workbench |

|  | Deviation |
|---|---|
| X1 | Dispute or complaint |
| X2 | Vulnerable customer or hardship |
| X3 | Deceased customer |
| X4 | Fraud |
| X5 | Bankruptcy or external seizure |
| X6 | Lost contact |
| X7 | Collateral event |

## Slide 10

The architecture on one page

10

Bank staff Entra ID single sign-on

Partners Partner portal (DL03)

Customers Existing bank channels only

ACE: one service, one repository, one front end, on the shared ACE AKS clusters

Front end React on Vite with Radix. Recovery screens in the recovery module folder

Common module ACE team. Sign-in, access checks, audit and PII logging, the shared case view, shared entities

Collection module Collection squad. Phone, field, FCR and restructure work

Recovery module TechX squads. Stages and tasks, rules component, decision log, document hub, partner portal

ACE database, PostgreSQL Case state, records, reference data, decision log, interaction ledger

Blob storage Documents, with a write-once container for legal types

In: COLLINS daily batch Core bank, EFS, SCBPDM, UDP, AAL, LIT, scores

In: file loads CCMS, SVAF, AMIS, RPS, WIN, GL

Out Bookings by the officer; WIN files; NSS and LINE OA; data lake for Power BI and COLLINS; partners

Platform services Entra ID, bank IAM, PII Kafka, audit and SOC logs, model endpoint

## Slide 11

Architecture principles

11

|  | Principle |
|---|---|
| 1 | Everything that a business person may want to change is a versioned data row, changed through a validated load without a code release |
| 2 | One service, one repository, one front end. A module calls another only through its published interface or an application event |
| 3 | Each module owns its tables. No module reads another module's tables |
| 4 | No component calls a system of record directly. Data comes in through COLLINS or a file load and leaves through existing ACE paths |
| 5 | A decision that cannot be written to the decision log does not proceed |
| 6 | An agent reaches a system only through the tool gateway and holds no credential. When it does not answer, the rule result is used |
| 7 | Personal data is tokenized or masked unless the role is allowed to see it. No personal data in code, tests, logs or prompts |
| 8 | Every loaded value carries its business date, so every decision can show the age of its inputs |

## Slide 12

Platform and stage modules

12

|  | Platform module | First in |
|---|---|---|
| P1 | Recovery data engine | E1 |
| P2 | Integration | E1 |
| P3 | Case and workflow | E1 core, E2 screens |
| P4 | Access and administration | E1; E2 partners; E8 full administration |
| P5 | Document hub | E1 store and OCR; E2 generation |
| P6 | Communications | E1 notices; E2 dispatch; E4 self-service |
| P7 | Decision center and log | E1 log; E2 routing; E3 center |
| P8 | Payments and posting | E2 matching; E4 |
| P9 | Reporting | E1 baseline; E2 dashboard |
| P10 | Agent runtime | E1 shadow; E2 L1 |

|  | Stage module | First in |
|---|---|---|
| S1 | Valuation and route | E4 |
| S2 | TDR, settlement and deed in lieu | E2 foundations; E3 |
| S3 | Guarantees and guarantors | E4 |
| S4 | Litigation and enforcement | E2 notices; E5 |
| S5 | Assets and auction | E3; E4 |
| S6 | Debt sale | E5 data; E6 screens |
| S7 | Write-off and recovery | E6 |
| S8 | Deviation handling | E2 screening; E7 |
| S9 | Partner management | E6 panel; E7 scoring |

## Slide 13

The data that comes from other systems

13

|  | Data product | System of record | How it arrives | Freshness |
|---|---|---|---|---|
| DP01 | Account and arrears | Core bank (ALS) | COLLINS daily batch | End of day; next morning in the Workbench |
| DP02 | Customer and party | SCBPDM and core bank | COLLINS daily batch | End of day; next morning in the Workbench |
| DP05 | Contact and promises | EFS before day 90; the Workbench after | COLLINS daily batch from EFS; held in the Workbench | End of day for EFS history; as it changes after |
| DP06 | Collateral and assets | CCMS, SVAF, AMIS, RPS | File load until a batch feed exists | Weekly or monthly today |
| DP07 | Legal events and cases | LIT for court records; the Workbench for instructions | COLLINS daily batch for litigation status; held in the Workbench | End of day for LIT status |
| DP11 | Scores and route economics | COLLINS | COLLINS daily batch | End of day; monthly for some models |
| DP13 | Money and closure | Core bank (ALS) and GL | COLLINS daily batch for payments; file load for GL | End of day for payments; monthly for GL |

## Slide 14

The data the Workbench holds

14

14 data products and the platform tables, across 108 entities and 1,256 fields.

|  | Data product | System of record | How it arrives | Freshness |
|---|---|---|---|---|
| DP03 | Case and ownership | Recovery Workbench | Held in the Workbench | As it changes |
| DP04 | Treatment and offers | Recovery Workbench; restructure plans in ACE | Held in the Workbench | As it changes |
| DP08 | Partner performance | Recovery Workbench | Held in the Workbench; partner results through the partner portal | As it changes |
| DP09 | Debt sale | Recovery Workbench | Held in the Workbench | As it changes |
| DP10 | Documents and extracted fields | Recovery Workbench document hub | Held in the Workbench | As it changes |
| DP12 | Decision log | Recovery Workbench | Held in the Workbench | As it changes |
| DP14 | Reference data | Recovery Workbench | Held in the Workbench | By versioned load |

## Slide 15

How information reaches the Workbench

15

There is no real-time feed today. Which interfaces need same-day data is DL06.

| Route | What comes or goes | How often |
|---|---|---|
| In through COLLINS | Accounts, payments, customers, collections history, litigation status, scores | Daily, end of day |
| In by file | Collateral and appraisals; assets held; repossessed vehicles; proof of delivery; write-off postings | Weekly or monthly |
| Entered in the Workbench | Partner results, documents, guarantee quota and claim deadlines | As entered |
| Out | Notices to WIN; SMS and LINE through ACE; reporting and model data to the data lake; data tapes to debt buyers | Daily or as sent |
| Booked by the officer | Restructures, settlements and write-offs in the core bank, confirmed on the next day's load | As approved |

## Slide 16

The organization that runs recovery

16

Product heads Mortgage, Hire Purchase, SSME Own cures, realized recovery and cost to collect. Approve above set limits.

Shared operations Collections and recovery for all products Carry out the work. Approve within set limits.

Center of excellence Strategy, analytics, testing, QA, rules Set strategy, rules and limits as data.

Platform EFS, ACE and the Workbench, COLLINS, agents, data Run the systems. Approve system and agent releases.

| Role class | Roles |
|---|---|
| 37 bank roles | Case owners, team managers, restructuring, litigation, enforcement, NPA, sale, debt sale, write-off, guarantee, partner management, control functions, administrators |
| 7 partner roles | Collection agency, law firm, valuer, auction vendor, debt buyer, RAMC, Legal Execution Department |
| 4 customer parties | Borrower, guarantor and co-borrower, heir, retail asset bidder |
| 6 non-human actors | Case workflow module, rules component, data load, OCR pipeline, decision log writer, agent platform |

## Slide 17

What changes for staff

17

| Area | Today | Target |
|---|---|---|
| Ownership | The case moves between units, with hand-overs by email and file | One owner from day 90 to close; specialists work tasks on the case |
| Allocation | Managers allocate from spreadsheets | Rules allocate; managers rebalance and handle exceptions |
| Preparing decisions | Officers gather data from several systems | The Workbench gathers the facts, the expected return by route and a recommendation |
| Approvals | By email and paper, limits checked by hand | Routed to the approval level, limit checked, logged once |
| Documents | Prepared, checked and couriered by document services | Generated, read and indexed; people review the exceptions |
| Partners | Managed by email and spreadsheet | Instructions, results and fees in the partner portal, scored each month |

## Slide 18

The plan: eight monthly releases

18

| Epic | Release | Theme | What the business gets |
|---|---|---|---|
| E1 | 30 Nov 2026 | Foundation 1 | One case list for every account at 90 days past due or more, reconciled to the core bank. Documents found by case. Decision log store. Read-only case record view |
| E2 | 31 Dec 2026 | Foundation 2 | One owner and a timer on every case, full history on one screen, approval routing, litigation notices generated and approved, steering dashboard |
| E3 | 31 Jan 2027 | Settle, deed in lieu, assets | Settlements and deeds in lieu end to end to booking. Asset record, floor price and listing on HOME.SCB |
| E4 | 28 Feb 2027 | Route decision | The route recommended with reasons and approved within the delegation of authority for every new case. Guarantee and TCG claims. Auction rounds and RAMC transfer |
| E5 | 31 Mar 2027 | Litigation | Litigation instructed and tracked end to end, law firms through the partner portal. Debt sale lot data and the buyer data room |
| E6 | 30 Apr 2027 | Debt sale and write-off | Debt sale screens and award, write-off committee, partner panel, allocation and fees |
| E7 | 31 May 2027 | Deviations and partners | Deviations X1 to X7 end to end. Partner scoring, conduct and the field app |
| E8 | 30 Jun 2027 | Administration and hardening | Full administration, conduct checks, autonomy step-ups, regulatory returns, hardening |

## Slide 19

When each team starts working in the Workbench

19

| Epic | Release | Roles that receive real users |
|---|---|---|
| E1 | 30 Nov 2026 | Center of excellence analyst, Data steward and data product owner, Internal audit, Compliance and PDPA officer, Platform administrator, Reference data administrator, Security administrator |
| E2 | 31 Dec 2026 | Case owner, Team manager, Phone collector, Litigation officer, Capacity and workforce planner, Product head (Mortgage, HP, SSME), Head of Litigation, Risk and model risk officer, Reporting and BI analyst, Tribe lead and squad members |
| E3 | 31 Jan 2027 | Restructuring officer (FCR), Legal counsel, Sale officer, NPA and asset manager, Credit Administration officer, Head of NPA |
| E4 | 28 Feb 2027 | Guarantee officer, Credit approval committee member, Valuer, Auction vendor, RAMC user |
| E5 | 31 Mar 2027 | Enforcement owner, Law firm user, Debt buyer and AMC |
| E6 | 30 Apr 2027 | Debt sale officer, Write-off team member, Partner and agency manager, Head of Asset Liquidity, Write-off committee member, Finance and CFO delegate, Collection agency (OA) user |
| E7 | 31 May 2027 | Field collector, Hardship and vulnerability specialist, Complaint officer, Fraud investigator |
| E8 | 30 Jun 2027 | Conduct and QA officer |

## Slide 20

The benefits

20

| Measure | Today | 2027 target |
|---|---|---|
| Recovery rate on NPL | 66.3% (2026 to date) | 73% |
| Litigation turnaround | 21 days | 6 days |
| Deed in lieu turnaround | 26 days | 12 days |
| Restructure turnaround | 23 days | 5 days |
| Debt sale turnaround | No baseline | 45 days |
| Manual processes removed | Near zero | 80% of the selected list |
| Audit findings and fraud cases | 50 | 13 |
| NPA sales cycle | 1,486 days | 1,095 days |

## Slide 21

Volume and scale

21

| Measure | Value | Basis |
|---|---|---|
| Open cases at go-live | About 23,600 | Active inventory at 1.2 accounts per case |
| Open cases at the end of 2027 | About 26,500 | 15 percent inflow growth a year |
| New cases a year in 2027 | About 35,800 | From 3,110 new accounts a month |
| Concurrent users in the busiest hour | About 410 | Of 1,234 named users, including partners |
| Documents held at the end of 2031 | About 5.8 million | 2.8 TB of storage |
| Decision log and ledger at the end of 2031 | About 36 GB | In the ACE database |

## Slide 22

Risks and how the plan answers them

22

| Risk | Effect | Answer |
|---|---|---|
| Data arrives a day late | End of day data for decisions that need today's position | Officers confirm payoff figures in the core; same-day triggers named under DL06 |
| Files instead of feeds | Collateral, appraisals and assets arrive weekly or monthly | Age limits on decision inputs; batch feeds requested under DL12 |
| Two squads, one repository | One squad's change holds the other's release | Feature flags, code owners and the module boundary test (DL04, DL37) |
| Rules component is new to ACE | ACE has rule based logic and no engine | A decision table evaluator in the recovery module, tested rule by rule against its test case |
| Volume grows faster than forecast | Loads, storage and queues sized too small | Sized at 15 percent inflow growth a year from the 30 June 2026 inventory; reviewed each quarter (DL15) |
| Partner access from outside | One to three months of lead time | Change raised in November; law firms first needed at Epic 5 (DL03) |

## Slide 23

What the project needs from the bank

23

Each decision has a recommended answer. The build goes ahead on that answer until the bank decides.

| Decision | Decision log | Needed by |
|---|---|---|
| Who grants access and who owns the application | DL01, DL02 | 28 Oct |
| Which interfaces need real-time data | DL06 | 30 Oct |
| Coding tool and model endpoint for the build | DL32, DL33 | 30 Oct |
| Which legacy systems are kept | DL12 | 7 Nov |
| What counts as one case, and entry at 90 or 91 days | DL16, DL17 | 6 Nov |
| Service levels per case state, caseload caps | DL22, DL23 | 13 Nov |
| Delegation of authority: holders, limits and substitutes | DL18 | 30 Nov |

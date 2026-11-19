<!-- source: 02 Business architecture and process/Recovery Workbench Business Architecture v4.pptx -->
<!-- converted: 2026-11-16 from PPTX -->

> **Source:** `02 Business architecture and process/Recovery Workbench Business Architecture v4.pptx`  
> **Converted from:** PPTX

## Slide 1

SCB

COLLECTIONS AND RECOVERY TRANSFORMATION Recovery Workbench: business architecture

Henka Group, 28 October 2026 (C) Siam Commercial Bank and Henka Pte Ltd

## Slide 2

Who and what the Workbench works with

2

Recovery Workbench The recovery module of ACE. One case record per customer and product from day 90 to close, with the routing rules, the decision log and the document hub.

Bank people Case owners and team managers Restructuring officers Litigation officers and enforcement owners NPA, sale and debt sale officers Write-off and credit administration Approvers and committees Center of excellence, Risk, Compliance, Audit 37 bank roles

Partners 73 collection agencies, 11 to 12 law firms, panel valuers, 4 vehicle auction vendors, 35 debt buyers, RAMC, the Legal Execution Department

Customers Borrowers, guarantors and co-borrowers, heirs, retail asset bidders. They reach the bank through SCB Easy, LINE OA, branches and the contact center

Systems it reads through COLLINS Core bank (ALS), EFS, UDP, SCBPDM, AAL

Systems it works alongside CCMS, SVAF, LIT, AMIS, NLEADS, WIN, SCIS, NCB, Aric, Power BI

## Slide 3

The value stream: six stages from day 90 to close

3

Receive the case D6 entry

Choose the route D6

Resolve with the customer D6

Enforce D7

Realize the asset D8

Close D9

A case can return to the route decision at any stage: on a cure, a payment, a deviation or an override.

| Stage | Decision | L1 and L2 | What the stage produces |
|---|---|---|---|
| Receive the case | D6 entry | 06 | One owner, the case history from collections, running deadlines and a deviation screen |
| Choose the route | D6 | 07.1, 07.2 | An approved route with the expected return of each option and the reasons |
| Resolve with the customer | D6 | 07.3 to 07.5 | A settlement, deed in lieu, guarantee claim or guarantor agreement, booked and reconciled |
| Enforce | D7 | 08 | A judgment enforced, a settlement before judgment, or proceeds matched to the case |
| Realize the asset | D8 | 09 | Cash from the asset or the debt: auction, RAMC, buy-back, rental or debt sale |
| Close | D9 | 10 | The balance written off and posted, recovery after charge-off, the case closed |

## Slide 4

Capability map

4

Manage: set the rules and read the results Strategy and treatment policy  ·  Decision rules and limits  ·  Fees and waivers  ·  Performance reporting  ·  Strategy testing  ·  Model and agent monitoring  ·  Data quality  ·  Benefits tracking  ·  Quality assurance  ·  Conduct control  ·  Audit and regulator response  ·  Access and data protection  ·  Capacity planning

Core: the case from day 90 to close Case takeover  ·  Case valuation  ·  Route decision  ·  Settlement and deed in lieu  ·  Guarantee claims  ·  Guarantor pursuit  ·  Litigation  ·  Judgment enforcement  ·  Asset holding  ·  Asset sale  ·  Debt sale  ·  Write-off  ·  Recovery after charge-off

Support: used across every core stage Customer care  ·  Deviation handling X1 to X7  ·  Partner management  ·  Document management and custody  ·  Correspondence  ·  Payments and reconciliation

Across all: at every decision Decision routing and approval  ·  Decision log  ·  Feedback to models

Before day 90, collections runs detect, contact, promise, escalate and restructure on EFS and ACE. The Workbench takes the case over from collections at 90 days past due.

## Slide 5

Capabilities, the processes under each, and the modules that build them

5

| Capability | Processes | Modules |
|---|---|---|
| Case takeover | 06.1 | P1 recovery data engine, P3 case and workflow |
| Case valuation and route decision | 07.1, 07.2 | S1 valuation and route, P7 decision center, P10 agent runtime |
| Settlement and deed in lieu | 07.3 | S2 TDR, settlement and deed in lieu, P8 payments and posting |
| Guarantee claims and guarantor pursuit | 07.4, 07.5 | S3 guarantees and guarantors |
| Litigation and enforcement | 08.1 to 08.4 | S4 litigation and enforcement, P6 communications |
| Asset holding and sale | 09.1 to 09.5, 09.7 | S5 assets and auction |
| Debt sale | 09.6 | S6 debt sale |
| Write-off and recovery after charge-off | 10.1 to 10.3 | S7 write-off and recovery, P8 payments and posting |
| Deviation handling and customer care | 11.1 to 11.8 | S8 deviation handling |
| Partner management | 12.1 to 12.5 | S9 partner management |
| Document management and correspondence | 13.1 to 13.4 | P5 document hub, P6 communications |
| Decision routing, approval and log | 17.1 to 17.3 | P7 decision center and log, P4 access and administration |
| Rules, limits and reference data | 14.1 to 14.3 | P3 case and workflow, P4 access and administration |
| Reporting, data quality and model monitoring | 15.1 to 15.8 | P9 reporting, P1 recovery data engine, P10 agent runtime |
| Control, conduct and data protection | 16.1 to 16.7 | P4 access and administration, P7 decision log |
| Payments and reconciliation | 19.1 to 19.3 | P8 payments and posting, P2 integration |

## Slide 6

The six capabilities the Workbench commits

6

| Capability | What it provides | The gap it closes | First in |
|---|---|---|---|
| One case record | A single record per customer and product, with the accounts linked, from day 90 to close | Cases, accounts and debtors are held in separate files and systems | Epic 1 |
| Stage clock | Days in each state against a service level, with escalation, and a prescription clock that keeps running when a stage pauses | Queues are visible but nothing escalates from them | Epic 1 |
| Interaction ledger | Every contact, offer, promise, payment and hand-over on the case, in order | Contact history is spread across four systems | Epic 1 |
| Document management | Case documents held against the case, indexed, with retention and custody of originals | Documents are kept outside the case and gaps are found late | Epic 1 |
| Next action | An owned, dated action on every case, produced by the routing rules | Each unit receives its part with no owner where value is lost | Epic 2 |
| Model-writable queue | A queue that analytical models write to directly | Daily model decisions arrive in a weekly manual process | Epic 2 |

## Slide 7

The nine decisions, and who owns each

7

Every decision runs on one pattern: information, decide, outcome, act, log. Who approves is set by the bank approval authority regulation and the delegation of authority table.

|  | What is decided | Owner | How it is decided | Where it runs |
|---|---|---|---|---|
| D1 | Act on the signal | Product head with the center of excellence | Agent, within policy | EFS |
| D2 | Reach the customer | Center of excellence with Compliance | Agent, within policy | EFS |
| D3 | Promise kept | Center of excellence | Agent, within policy | EFS |
| D4 | Escalate | Product head with the agency unit | Agent; a person on exception | EFS |
| D5 | Offer a restructure | Product head with Credit Risk | Agent proposes; a person approves above the limit | EFS and ACE |
| D6 | Which route | Recovery Strategy with Risk | Agent proposes; a person approves | Recovery Workbench |
| D7 | Next legal step | Head of Litigation, with the enforcement owner after judgment | Agent proposes; a person approves | Recovery Workbench |
| D8 | How to dispose | Head of NPA and Head of Auto Recovery | Agent runs; a person approves the floor price | Recovery Workbench |
| D9 | Write off or pursue | Credit Administration with Risk | Agent proposes; the committee approves | Recovery Workbench |

## Slide 8

Sub-decisions D5 and D6 and how each is made

8

A automated.  A+H AI prepares, a person decides.  H human.  P partner.

|  | Sub-decision | How it is made | Mode |
|---|---|---|---|
| D5.1 | Affordability | Rule and model in ACE | A |
| D5.2 | Plan to offer | Agent, final within the limit | A |
| D5.3 | Reassess after a broken plan | Agent proposes, person approves | A+H |
| D6.1 | Accept the appraisal value | Rule check, agent flags outliers, person accepts | A+H |
| D6.2 | Return by route | COLLINS model | A |
| D6.3 | Route | Agent recommends, person approves, committee above the limit | A+H |
| D6.4 | Settlement amount and terms | Rule payoff, agent range, person negotiates and approves | A+H |
| D6.5 | Thai Credit Guarantee claim | Agent prepares, person approves | A+H |
| D6.6 | Guarantor and co-borrower pursuit | Rule sends notices, person negotiates | H |

## Slide 9

Sub-decisions D7 to D9 and how each is made

9

A automated.  A+H AI prepares, a person decides.  H human.  P partner.

|  | Sub-decision | How it is made | Mode |
|---|---|---|---|
| D7.1 | Demand and recall notices | Rule | A |
| D7.2 | Document pack complete | Agent assembles and checks, person verifies | A+H |
| D7.3 | Which law firm | Rule from the panel | A |
| D7.4 | Settle before judgment, appeal, fees | Agent proposes, person approves | A+H |
| D7.5 | Enforce: trace, writ, seizure, auction | Agent traces, partner acts, person approves a bankruptcy petition | P |
| D8.1 | Asset on the books, holding age, reappraisal | Rule | A |
| D8.2 | Start and floor price | Agent with COLLINS, person approves the floor | A+H |
| D8.3 | RAMC transfer, buy-back, rental | Agent proposes, person approves | A+H |
| D8.4 | Debt sale lots, buyer terms, award | Agent builds lots, rules check eligibility, person approves | A+H |
| D9.1 | Eligibility and tax criteria | Rule | A |
| D9.2 | Write off or pursue | Agent proposes, committee approves | A+H |
| D9.3 | Recovery after charge-off | Agent proposes, person approves a sale | A+H |

## Slide 10

The seven deviations that interrupt a decision

10

A deviation pauses the stage clock. The prescription clock keeps running, because a court deadline does not wait for a complaint to be resolved.

|  | What has happened | Who decides | Where the case goes next |
|---|---|---|---|
| X1 | Dispute or complaint | Complaint officer | The same decision. The case timers resume |
| X2 | Vulnerable customer or hardship | Hardship specialist | D5 |
| X3 | Deceased customer | Specialist; Legal for claims against the estate | Closed if insurance settles; otherwise D6 |
| X4 | Fraud | Fraud team | D9, or D2 if fraud is not confirmed |
| X5 | Bankruptcy or external seizure | Legal | D7, then D9 |
| X6 | Lost contact | Agent, within policy | D2 if found; D4 or D6 if not |
| X7 | Collateral event | Agent proposes; a person approves the claim | D6 |

## Slide 11

The partners, and how each is managed

11

Every partner type is managed on the same six points Selection  ·  Contract and fees  ·  Targets and incentives  ·  Communication and data exchange  ·  Performance reviews  ·  Notice and exit

| Partner type | How many | Owner in the bank | How work is allocated |
|---|---|---|---|
| Collection agencies | 73 | Partner and agency manager | Share set by measured return on a matched population |
| Law firms | 11 to 12 | Head of Litigation | Cases allocated on the panel scorecard; fees reviewed against results |
| Valuers | Panel | Head of NPA | Appraisal orders through SVAF |
| Vehicle auction vendors | 4 | Head of Auto Recovery | Allocated on the scorecard |
| Debt buyers and asset management companies | 35 | Head of Asset Liquidity | Tiered terms, a reserve price, recovery tracked by lot and buyer |
| RAMC | 1 | Head of Asset Liquidity | Secured pools transferred on agreed terms |

## Slide 12

The organization that runs recovery

12

Product heads Mortgage, Auto HP, SSME Own cures, realized recovery and cost to collect for their product. Approve above set limits.

Shared operations Collections and recovery for all products Carry out the work, including outside agency management. Approve within set limits.

Center of excellence Strategy, analytics, testing, QA Propose strategy, rule and agent changes to the strategy and model committee.

Platform EFS, ACE and the Workbench, COLLINS, agents, data Approve system and agent releases.

| Role class | Roles |
|---|---|
| 37 bank roles | Case owner, team manager, restructuring officer, litigation officer, enforcement owner, sale, NPA and debt sale officers, write-off and credit administration, conduct and QA, Risk, Audit, Compliance, administrators |
| 7 partner roles | Collection agency, law firm, valuer, auction vendor, debt buyer, RAMC, Legal Execution Department |
| 4 customer parties | Borrower, guarantor and co-borrower, heir and estate representative, retail asset bidder |
| 6 non-human actors | Case workflow module, rules component, data load from COLLINS, OCR and extraction pipeline, decision log writer, agent platform |

## Slide 13

Process owners

13

A process owner answers for the outcome of the process end to end: its measures, rules, exceptions and the people who run it. Processes 01 to 05 are owned in collections.

| L1 | Process | Process owner |
|---|---|---|
| 06 | Take over and own the case | Recovery Strategy with Risk; the case owner for each case |
| 07 | Route, settle and claim | Recovery Strategy with Risk |
| 08 | Litigate and enforce | Head of Litigation; the enforcement owner after judgment |
| 09 | Dispose assets and sell debt | Head of NPA and Head of Auto Recovery; Head of Asset Liquidity for debt sale |
| 10 | Write off and recover after charge-off | Credit Administration with Risk |
| 11 | Handle customer care and deviations | Shared operations, with a named handler for each deviation |
| 12 | Manage partners | Partner and agency manager |
| 13 | Manage documents and correspondence | Shared operations |
| 14 | Set strategy, policy and decision rules | Center of excellence |
| 15 | Manage performance, data and AI | Center of excellence with Model Risk |
| 16 | Manage risk, control and compliance | Product heads for limits; center of excellence for QA; Shared operations for conduct |
| 17 | Run the decision center | Center of excellence |
| 18 | Plan capacity and allocate work | Shared operations |
| 19 | Manage payments and reconciliation | Credit Administration |

## Slide 14

Forums and decision rights

14

| Forum | What it decides | Chair |
|---|---|---|
| Collections and Recovery steering | Progress of the operating model, waves and releases; issues across products | Collections and Recovery head |
| Credit approval | Restructuring, deed in lieu and write-offs above set limits | Product head, with Risk |
| Strategy and model | Champion and challenger results, agent and model changes, agent risk | Center of excellence head |
| Partner review | Agency and partner results, incentives, notices and exits | Partner and agency manager |
| Process and quality assurance | Procedure changes, QA results and the improvement backlog | Shared operations head |

| Control area | Owner |
|---|---|
| Quality assurance | Center of excellence |
| Approval limits | Product heads |
| Conduct | Shared operations |
| Model risk | Center of excellence with Model Risk |
| Agent risk | Strategy and model committee |
| Partner controls | Partner and agency manager |

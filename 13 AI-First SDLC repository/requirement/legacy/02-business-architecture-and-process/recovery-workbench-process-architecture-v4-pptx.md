<!-- source: 02 Business architecture and process/Recovery Workbench Process Architecture v4.pptx -->
<!-- converted: 2026-11-04 from PPTX -->

> **Source:** `02 Business architecture and process/Recovery Workbench Process Architecture v4.pptx`  
> **Converted from:** PPTX

## Slide 1

SCB

COLLECTIONS AND RECOVERY TRANSFORMATION Recovery Workbench: process architecture

Henka Group, 28 October 2026 (C) Siam Commercial Bank and Henka Pte Ltd

## Slide 2

The process architecture on one page

2

Core, before day 90, on EFS 01  Detect and act on signals   2 L2, 6 L3 02  Contact the customer   6 L2, 15 L3 03  Manage promises   3 L2, 6 L3 04  Escalate   4 L2, 10 L3 05  Restructure   5 L2, 15 L3

Core, from day 90, on the Recovery Workbench 06  Take over and own the case   1 L2, 3 L3 07  Route, settle and claim   5 L2, 17 L3 08  Litigate and enforce   4 L2, 16 L3 09  Dispose assets and sell debt   7 L2, 28 L3 10  Write off and recover after charge-off   3 L2, 9 L3

Support 11  Handle customer care and deviations 12  Manage partners 13  Manage documents and correspondence 19  Manage payments and reconciliation

Manage 14  Set strategy, policy and decision rules 15  Manage performance, data and AI 16  Manage risk, control and compliance 18  Plan capacity and allocate work

Across all 17  Run the decision center Every recommendation goes to the person with the authority to decide it, and every decision is logged once.

19 L1 processes, 84 L2 sub-processes, 247 L3 processes. A case can return to the route decision at any stage.

## Slide 3

How the architecture is numbered and read

3

| Level | What it is |
|---|---|
| L1 | A process area, 01 to 19. Each carries one decision or serves all of them |
| L2 | A sub-process inside one L1, numbered L1.n, for example 7.3 |
| L3 | A process inside one L2, numbered 07.3.1. The items under an L2 are always L3 processes |

| Step | In every decision |
|---|---|
| Information | Gather and check the facts the decision needs. |
| Decide | Apply a rule, a model or an agent to choose an option. |
| Outcome | Make the choice final, or route it to the person with the authority to approve it. |
| Act | Carry out the choice in the Workbench, another system or through a partner. |
| Log | Record the decision, the action and the result once, in the decision log. |

| Mode | Who carries out the L3 process |
|---|---|
| A | A rule, engine or agent completes the step. No person is involved; the result is in the log. |
| A+H | An agent or engine prepares, recommends or drafts. A person decides, approves or completes. |
| H | A bank employee carries out the step. The Workbench prepares the task and records the result. |
| M | A physical or legal act done outside any system, such as a title transfer. The Workbench records that it happened. |
| P | A partner carries out the step: an agency, law firm, valuer, auction house, broker or court officer. |

## Slide 4

L1 processes: core

4

| L1 | Process | What it covers | Decision | L2 | L3 |
|---|---|---|---|---|---|
| 01 | Detect and act on signals | Watch every performing and early-arrears account and decide whether, when and how to act before or at the first missed payment. | D1 | 2 | 6 |
| 02 | Contact the customer | Reach the customer through the right channel at the right time, within contact limits and customer standards, and record the outcome. | D2 | 6 | 15 |
| 03 | Manage promises | Record each promise to pay, track it to the payment and move the case on when the promise is broken. | D3 | 3 | 6 |
| 04 | Escalate | Raise the intensity of collection by senior phone contact, field visits or outside agencies when lighter treatment has failed. | D4 | 4 | 10 |
| 05 | Restructure | Assess affordability, offer and book a restructure plan, and monitor it until the customer pays as agreed or the plan fails. | D5 | 5 | 15 |
| 06 | Take over and own the case | Take the case from collections at 90 days past due, with its history, and give it one owner and a running set of deadlines. | D6 entry | 1 | 3 |
| 07 | Route, settle and claim | Value the case, decide the route, and resolve it with the customer by settlement, deed in lieu, guarantee claim or guarantor pursuit. | D6 | 5 | 17 |
| 08 | Litigate and enforce | Take the case through notices, filing, judgment and enforcement until the debt is paid, settled or proven unrecoverable. | D7 | 4 | 16 |
| 09 | Dispose assets and sell debt | Take assets onto the books, hold them, and turn them into cash by auction or other routes, or sell the debt. | D8 | 7 | 28 |
| 10 | Write off and recover after charge-off | Write off the balance that cannot be recovered, post it, and keep recovering after charge-off until the case closes. | D9 | 3 | 9 |

## Slide 5

L1 processes: support, manage and across all

5

| L1 | Process | What it covers | Decision | L2 | L3 |
|---|---|---|---|---|---|
| 11 | Handle customer care and deviations | Answer customer contacts and handle the seven deviations that interrupt a decision, then return the case to the right decision. | X1 to X7 | 8 | 31 |
| 12 | Manage partners | Select, instruct, measure, pay and govern the partners who work cases for the bank, and end the contract when needed. | All | 5 | 13 |
| 13 | Manage documents and correspondence | Read and file inbound documents, send letters and notices with proof of delivery, and keep documents and originals under control. | All | 4 | 14 |
| 19 | Manage payments and reconciliation | Receive payments from every channel, apply them to the right account and case, and reconcile cash to the case and the core. | D3, D5, D6 | 3 | 6 |
| 14 | Set strategy, policy and decision rules | Set the segments, treatment policy, decision rules, limits, fees and the reference data every decision reads. | All | 3 | 12 |
| 15 | Manage performance, data and AI | Report results, test strategies, monitor agents and models, keep data correct and feed what is learned back to policy. | All | 8 | 20 |
| 16 | Manage risk, control and compliance | Run quality assurance, conduct control, model and agent risk, audit response, access control, incidents and data subject rights. | All | 7 | 14 |
| 18 | Plan capacity and allocate work | Forecast inflow, plan staff and partner capacity, and build and allocate the work lists that collectors and partners work from. | D2, D4 | 3 | 6 |
| 17 | Run the decision center | Route every recommendation to the person with the authority to decide it, record one log entry per decision, and feed results back. | D1 to D9 | 3 | 6 |

## Slide 6

L2 sub-processes: collections before day 90

6

| ID | Process and L2 sub-processes | L3 |
|---|---|---|
| 01 | Detect and act on signals | 6 |
| 1.1 | Monitor accounts | 3 |
| 1.2 | Decide whether to act | 3 |
| 02 | Contact the customer | 15 |
| 2.1 | Choose the channel | 2 |
| 2.2 | Contact by digital channels | 3 |
| 2.3 | Contact by phone | 5 |
| 2.4 | Hold within the grace period | 1 |
| 2.5 | Manage contact data and consent | 3 |
| 2.6 | Handle inbound contact | 1 |
| 03 | Manage promises | 6 |
| 3.1 | Record the promise | 2 |
| 3.2 | Track the promise | 2 |
| 3.3 | Handle broken promises | 2 |

| ID | Process and L2 sub-processes | L3 |
|---|---|---|
| 04 | Escalate | 10 |
| 4.1 | Recommend the escalation | 2 |
| 4.2 | Run higher-intensity phone contact | 1 |
| 4.3 | Run field visits | 3 |
| 4.4 | Allocate to outside agencies | 4 |
| 05 | Restructure | 15 |
| 5.1 | Assess affordability | 2 |
| 5.2 | Offer a plan | 3 |
| 5.3 | Approve and book | 3 |
| 5.4 | Monitor plans | 4 |
| 5.5 | Run relief and government schemes | 3 |

## Slide 7

L2 sub-processes on the Recovery Workbench

7

| ID | Process and L2 sub-processes | L3 |
|---|---|---|
| 06 | Take over and own the case | 3 |
| 6.1 | Take over the case at 90 days past due | 3 |
| 07 | Route, settle and claim | 17 |
| 7.1 | Value the case | 5 |
| 7.2 | Decide the route | 3 |
| 7.3 | Negotiate settlement or deed in lieu | 5 |
| 7.4 | Claim guarantees | 2 |
| 7.5 | Pursue guarantors and co-borrowers | 2 |
| 08 | Litigate and enforce | 16 |
| 8.1 | Prepare pre-litigation | 3 |
| 8.2 | Instruct and file | 3 |
| 8.3 | Manage to judgment | 5 |
| 8.4 | Enforce judgment | 5 |

| ID | Process and L2 sub-processes | L3 |
|---|---|---|
| 09 | Dispose assets and sell debt | 28 |
| 9.1 | Take assets onto the books | 3 |
| 9.2 | Hold and manage assets | 5 |
| 9.3 | Decide the disposal route | 1 |
| 9.4 | Sell assets by Dutch auction | 5 |
| 9.5 | Other disposal routes | 4 |
| 9.6 | Sell debt | 7 |
| 9.7 | Manage the shortfall after sale | 3 |
| 10 | Write off and recover after charge-off | 9 |
| 10.1 | Assess write-off | 3 |
| 10.2 | Approve and post | 3 |
| 10.3 | Recover after charge-off | 3 |

## Slide 8

L2 sub-processes: support

8

| ID | Process and L2 sub-processes | L3 |
|---|---|---|
| 11 | Handle customer care and deviations | 31 |
| 11.1 | Answer customer contacts | 3 |
| 11.2 | X1 Dispute or complaint | 4 |
| 11.3 | X2 Vulnerable customer or hardship | 4 |
| 11.4 | X3 Deceased customer | 5 |
| 11.5 | X4 Fraud | 4 |
| 11.6 | X5 Bankruptcy or external seizure | 4 |
| 11.7 | X6 Lost contact | 3 |
| 11.8 | X7 Collateral event | 4 |

| ID | Process and L2 sub-processes | L3 |
|---|---|---|
| 12 | Manage partners | 13 |
| 12.1 | Select and contract partners | 3 |
| 12.2 | Exchange work with partners | 2 |
| 12.3 | Track performance and pay fees | 2 |
| 12.4 | Govern partners | 4 |
| 12.5 | Issue notices and exit | 2 |
| 13 | Manage documents and correspondence | 14 |
| 13.1 | Read inbound documents | 4 |
| 13.2 | Send letters and notices | 3 |
| 13.3 | Store and retain documents | 4 |
| 13.4 | Control document custody | 3 |
| 19 | Manage payments and reconciliation | 6 |
| 19.1 | Receive payments | 2 |
| 19.2 | Apply payments to accounts | 2 |
| 19.3 | Reconcile and correct | 2 |

## Slide 9

L2 sub-processes: manage and across all

9

| ID | Process and L2 sub-processes | L3 |
|---|---|---|
| 14 | Set strategy, policy and decision rules | 12 |
| 14.1 | Set strategy and treatment policy | 3 |
| 14.2 | Set decision rules and limits | 6 |
| 14.3 | Set fees, charges and waivers | 3 |
| 15 | Manage performance, data and AI | 20 |
| 15.1 | Report performance | 2 |
| 15.2 | Test strategies | 2 |
| 15.3 | Monitor agents and models | 3 |
| 15.4 | Manage data quality | 3 |
| 15.5 | Improve processes | 2 |
| 15.6 | Track benefits and value | 3 |
| 15.7 | Feed results back to credit policy and origination | 2 |
| 15.8 | Classify, stage and re-age accounts | 3 |

| ID | Process and L2 sub-processes | L3 |
|---|---|---|
| 16 | Manage risk, control and compliance | 14 |
| 16.1 | Run quality assurance | 2 |
| 16.2 | Control conduct | 2 |
| 16.3 | Manage model and agent risk | 2 |
| 16.4 | Answer audit and regulatory requests | 2 |
| 16.5 | Control access and data protection | 1 |
| 16.6 | Manage incidents and continuity | 3 |
| 16.7 | Handle data subject requests | 2 |
| 17 | Run the decision center | 6 |
| 17.1 | Route recommendations for approval | 3 |
| 17.2 | Keep the decision log | 2 |
| 17.3 | Feed results back | 1 |
| 18 | Plan capacity and allocate work | 6 |
| 18.1 | Forecast inflow and workload | 2 |
| 18.2 | Plan capacity and rosters | 2 |
| 18.3 | Build and allocate work lists | 2 |

## Slide 10

How each L1 process is carried out

10

## Slide 11

L3 processes: take over, and route, settle and claim

11

A automated.  A+H AI prepares, a person decides.  H human.  M manual.  P partner.

| ID | L2 sub-process and L3 processes | Mode |
|---|---|---|
| 6.1 | Take over the case at 90 days past due |  |
| 06.1.1 | Transfer case and history from EFS | A |
| 06.1.2 | Track prescription deadlines | A |
| 06.1.3 | Screen the case for deviations X1 to X7 | A |
| 7.1 | Value the case |  |
| 07.1.1 | Order collateral appraisal | A |
| 07.1.2 | Inspect collateral | P |
| 07.1.3 | Accept appraisal value | A+H |
| 07.1.4 | Estimate return by route | A |
| 07.1.5 | Calculate payoff and settlement amounts | A |
| 7.2 | Decide the route |  |
| 07.2.1 | Recommend route with reasons | A |
| 07.2.2 | Approve route | A+H |

| ID | L2 sub-process and L3 processes | Mode |
|---|---|---|
| 07.2.3 | Hold the case and set a review date | A |
| 7.3 | Negotiate settlement or deed in lieu |  |
| 07.3.1 | Negotiate settlement | H |
| 07.3.2 | Approve settlement | A+H |
| 07.3.3 | Process deed in lieu | H |
| 07.3.4 | Reconcile settlement payments to case | A |
| 07.3.5 | Release collateral and return title | A+H |
| 7.4 | Claim guarantees |  |
| 07.4.1 | Prepare and submit TCG claim | A+H |
| 07.4.2 | Track claim to payment | A |
| 7.5 | Pursue guarantors and co-borrowers |  |
| 07.5.1 | Notify guarantors of default | A |
| 07.5.2 | Negotiate with guarantors | H |

## Slide 12

L3 processes: litigate and enforce, and write off

12

A automated.  A+H AI prepares, a person decides.  H human.  M manual.  P partner.

| ID | L2 sub-process and L3 processes | Mode |
|---|---|---|
| 8.1 | Prepare pre-litigation |  |
| 08.1.1 | Issue demand and recall notices | A |
| 08.1.2 | Assemble litigation document pack | A |
| 08.1.3 | Verify document pack | A+H |
| 8.2 | Instruct and file |  |
| 08.2.1 | Select law firm from panel | A |
| 08.2.2 | Instruct firm through portal | A |
| 08.2.3 | File case in court | P |
| 8.3 | Manage to judgment |  |
| 08.3.1 | Recommend the next litigation step with reasons | A |
| 08.3.2 | Track hearings and deadlines | A |
| 08.3.3 | Approve settlement before judgment | A+H |
| 08.3.4 | Decide and manage appeals | A+H |
| 08.3.5 | Pay court fees and legal expenses | A+H |
| 8.4 | Enforce judgment |  |
| 08.4.1 | Trace assets | A |

| ID | L2 sub-process and L3 processes | Mode |
|---|---|---|
| 08.4.2 | Apply for writ and seizure | P |
| 08.4.3 | Follow LED auction | P |
| 08.4.4 | Match proceeds to case | A |
| 08.4.5 | File bankruptcy petition against debtor | A+H |
| 10.1 | Assess write-off |  |
| 10.1.1 | Identify eligible accounts | A |
| 10.1.2 | Prepare write-off pack | A |
| 10.1.3 | Check tax criteria for write-off | A |
| 10.2 | Approve and post |  |
| 10.2.1 | Approve write-off in committee | H |
| 10.2.2 | Post write-off to core and GL | A |
| 10.2.3 | Send provision inputs to Finance | A |
| 10.3 | Recover after charge-off |  |
| 10.3.1 | Place for soft recovery | A |
| 10.3.2 | Sell post charge-off accounts | A+H |
| 10.3.3 | Close case | A |

## Slide 13

L3 processes: dispose assets and sell debt

13

A automated.  A+H AI prepares, a person decides.  H human.  M manual.  P partner.

| ID | L2 sub-process and L3 processes | Mode |
|---|---|---|
| 9.1 | Take assets onto the books |  |
| 09.1.1 | Repossess vehicle | P |
| 09.1.2 | Serve notice and prove delivery | A |
| 09.1.3 | Record property | A |
| 9.2 | Hold and manage assets |  |
| 09.2.1 | Track holding age against provision steps | A |
| 09.2.2 | Store repossessed vehicles | P |
| 09.2.3 | Maintain property: tax, insurance, security | P |
| 09.2.4 | Evict occupants from property | P |
| 09.2.5 | Reappraise held assets on cycle | A |
| 9.3 | Decide the disposal route |  |
| 09.3.1 | Recommend the disposal route with reasons | A |
| 9.4 | Sell assets by Dutch auction |  |
| 09.4.1 | Set start and floor price | A+H |
| 09.4.2 | Publish listing | A |
| 09.4.3 | Run auction rounds | A |
| 09.4.4 | Complete sale and transfer title | M |
| 09.4.5 | Transfer vehicle registration | M |

| ID | L2 sub-process and L3 processes | Mode |
|---|---|---|
| 9.5 | Other disposal routes |  |
| 09.5.1 | Transfer to RAMC | A+H |
| 09.5.2 | Arrange customer buy-back | H |
| 09.5.3 | Sell through broker | P |
| 09.5.4 | Rent asset to a third party | H |
| 9.6 | Sell debt |  |
| 09.6.1 | Select accounts and build lots | A |
| 09.6.2 | Set buyer terms | A+H |
| 09.6.3 | Run bid and award | A+H |
| 09.6.4 | Transfer account data to buyer | A |
| 09.6.5 | Track realized recovery by lot | A |
| 09.6.6 | Check buyer eligibility and KYC | A+H |
| 09.6.7 | Handle buyer put-back claims | H |
| 9.7 | Manage the shortfall after sale |  |
| 09.7.1 | Calculate the shortfall after sale and notify the debtor | A |
| 09.7.2 | Offer affordable terms on the shortfall | A+H |
| 09.7.3 | Move an unpaid shortfall to D9 | A |

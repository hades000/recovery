## Slide 1: SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd
Recovery Workbench Project Overview, version 5. Decision D-RCV-60 microservice realignment.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Status: Draft.
Supersedes version 4 of 28 October 2026, which stays unchanged next to this file.
Change log: v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash.
Bank approval of D-RCV-60 and of DL44 to DL49: Not specified in the source documents (CG-D2-OVR-4; ASM-D2-OVR-4).

1

## Slide 2

SCB

COLLECTIONS AND RECOVERY TRANSFORMATION
Recovery Workbench: project overview

Henka Group, 28 October 2026
(C) Siam Commercial Bank and Henka Pte Ltd

## Slide 3

What the Recovery Workbench is

2

The Recovery Workbench is the system that owns every recovery case from 90 days past due to close, for Mortgage, Hire Purchase and SSME. It is built as the recovery module of ACE, the bank's collection engine, so collection and recovery work in one application with one case view.

From day 90 to close
One case per customer and product, with one owner, one clock and one history

Mortgage, Hire Purchase, SSME
Every route: restructure, settlement, deed in lieu, guarantee claim, litigation, asset disposal, debt sale and write-off

Built on ACE
One service, one repository and one front end, with data through COLLINS

## Slide 4

The problem it solves

3

Work is spread across systems
Collections and recovery staff use 42 applications. A case's facts are held in the core bank, EFS, LIT, CCMS, SVAF, AMIS and the document stores, and no screen shows them together.

Cases are run from spreadsheets
Teams keep their own case lists in Excel and SharePoint, build account plans by hand and approve by email. Hand-overs between teams are manual.

Decisions are not recorded in one place
Why a route was chosen, who approved it and on what figures is spread across emails and files. Audit findings and fraud cases number 50.

Cases take too long
Turnaround is 21 days for litigation, 23 days for a restructure and 26 days for a deed in lieu. The NPA sales cycle is 1,486 days.

## Slide 5

What changes

4

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

5

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


A deviation such as a complaint, a death, fraud or lost contact pauses the stage at any point and returns the case when it clears.

## Slide 7

How decisions are made

6

Information
Gather and check the facts

Decide
A rule, a model or an agent

Outcome
Final, or sent to the approver

Act
Carry it out in the systems

Log
Record it once

| Who carries out the step, from day 90 to close | L3 processes | Share |
|---|---|---|
| Automated | 38 | 52% |
| AI prepares, a person decides | 17 | 23% |
| A person decides | 7 | 10% |
| Partner | 9 | 12% |
| Manual | 2 | 3% |
| Total | 73 | 100% |


Every decision follows the same five steps. The approver is set by the bank approval authority regulation and the delegation of authority table.

## Slide 8

What it is built on

7

ACE
The Workbench is a module of ACE: one service, one repository, one front end. It reuses ACE sign-in, access control, audit and logging.

COLLINS
Account, customer, collections history, litigation status and scores arrive by daily batch through COLLINS.

Case model
Stages, milestones, tasks and timers in CMMN 1.1 terms, the standard shared with the collection module.

Rules as data
Every rule, limit, threshold, template, queue, role, timer and route is a versioned data row.

Decision log
Every decision is recorded once, with its inputs, the rule and model versions, the approver and the outcome.

AI agents
Agents prepare and recommend. They start in shadow, then recommend to a person, and move up only on evidence.

## Slide 9

The plan: eight monthly releases

8

| Epic | Release | Theme | What the business gets |
|---|---|---|---|
| E1 | 30 Nov 2026 (tentative) | Foundation 1 | One case list for every account at 90 days past due or more, reconciled to the core bank. Documents found by case. Decision log store. Read-only case record view |
| E2 | 31 Dec 2026 (tentative) | Foundation 2 | One owner and a timer on every case, full history on one screen, approval routing, litigation notices generated and approved, steering dashboard |
| E3 | 31 Jan 2027 (tentative) | Settle, deed in lieu, assets | Settlements and deeds in lieu end to end to booking. Asset record, floor price and listing on HOME.SCB |
| E4 | 28 Feb 2027 (tentative) | Route decision | The route recommended with reasons and approved within the delegation of authority for every new case. Guarantee and TCG claims. Auction rounds and RAMC transfer |
| E5 | 31 Mar 2027 (tentative) | Litigation | Litigation instructed and tracked end to end, law firms through the partner portal. Debt sale lot data and the buyer data room |
| E6 | 30 Apr 2027 (tentative) | Debt sale and write-off | Debt sale screens and award, write-off committee, partner panel, allocation and fees |
| E7 | 31 May 2027 (tentative) | Deviations and partners | Deviations X1 to X7 end to end. Partner scoring, conduct and the field app |
| E8 | 30 Jun 2027 (tentative) | Administration and hardening | Full administration, conduct checks, autonomy step-ups, regulatory returns, hardening |


One production release at each month end. What slips moves to the next epic; the release date does not move.

## Slide 10

The benefits the Workbench is measured on

9

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


Each measure is taken from the decision log per decision, with the baseline set in Epic 1.

## Slide 11

What the project needs from the bank

10

| Decision | Decision log | Needed by |
|---|---|---|
| Who grants access and who owns the application | DL01, DL02 | 28 Oct |
| Which interfaces need real-time data | DL06 | 30 Oct |
| Coding tool and model endpoint for the build | DL32, DL33 | 30 Oct |
| Which legacy systems are kept | DL12 | 7 Nov |
| What counts as one case, and entry at 90 or 91 days | DL16, DL17 | 6 Nov |
| Service levels per case state, caseload caps | DL22, DL23 | 13 Nov |
| Delegation of authority: holders, limits and substitutes | DL18 | 30 Nov |


Each decision has a recommended answer. The build goes ahead on that answer until the bank decides.

## Slide 12: Realignment summary: 19 services inside ACE

D-RCV-60 adopts Architecture v5. Recovery stays part of ACE: same AKS cluster and App Gateway, ACE Common shared services, ACE PostgreSQL database.
recovery-core is split into 19 services, one per business module: P1 to P10 for the shared capability, S1 to S9 for the case and route services.
Each service owns schema rwb_<name>, REST base /api/recovery/<name>/v1, topic rwb.<name>.events.v1, task queue rwb-<name> in namespace rwb-recovery, and epic RWB-SVC-<code>.
One schema and login per service in the ACE database; Kafka with outbox and inbox; one reusable Temporal layer; embedded Drools with the rule registry in rwb-decision.
Why: one service per module gives each capability its own release, owner and contract, so it can be reused or replaced alone.
What does not change: the six-stage journey, the eight routes, the five decision steps, the CMMN 1.1 case model, rules as versioned data, one decision log entry per decision.

12

## Slide 13: The 19 services, their owners and waves

Wave 1: P1 rwb-source-data (Source data), P2 rwb-integration (Integration), P3 rwb-case (Case and workflow), P4 rwb-access (Access and authority).
Wave 1 continued: P5 rwb-document (Document), P6 rwb-comms (Communications), P7 rwb-decision (Decision and rules), P9 rwb-reporting (Reporting), P10 rwb-agent (Agent).
Wave 2: P8 rwb-payment (Payment), S2 rwb-treatment (Treatment and offer), S5 rwb-asset (Asset), S8 rwb-deviation (Deviation).
Wave 3: S1 rwb-valuation (Valuation and route), S3 rwb-guarantee (Guarantee), S4 rwb-litigation (Litigation), S6 rwb-debtsale (Debt sale).
Wave 4: S7 rwb-writeoff (Write-off), S9 rwb-partner (Partner).
Every owner above is the row of that service in the Ownership Map v1 Services sheet; the service epic is RWB-SVC-<code>.
Service wave to the eight releases on slide 9: Not specified in the source documents (CG-D2-OVR-2; ASM-D2-OVR-2).

13

## Slide 14: How the realignment touches this overview

Slides 3 and 8 keep their text. "One service, one repository and one front end" is read as 19 services with one repository and schema each, and one ACE front end behind gateway-bff (CG-D2-OVR-1).
Slide 5 holds, service by service: case list P3 rwb-case, document hub P5 rwb-document, partner portal S9 rwb-partner, decision log P7 rwb-decision, parameters and reference data P3 rwb-case, DoA table P4 rwb-access.
Slide 6: receive P1 and P3, choose the route S1 with the rules in P7, resolve S2 and S3, enforce S4, realize S5 and S6, close S7, deviate S8.
Slide 7: decide and log in P7 rwb-decision, AI prepares in P10 rwb-agent, act in the owning service.
Slide 10 measures and slide 11 decisions are unchanged; DL01 to DL33 stay open and D-RCV-60 adds DL44 to DL49.
Which service serves each screen route behind gateway-bff: Not specified in the source documents (CG-D2-OVR-3; ASM-D2-OVR-3).

14

## Slide 15: Where the realignment is written down

Architecture v5, slides 13 to 20 and 41 to 44: services, contracts, service catalogue and job map.
Decision Log: D-RCV-60 and DL44 to DL49. Architecture Decision Records: ADR-013 to ADR-023.
Delivery: one epic per service, RWB-SVC-P1 to RWB-SVC-S9, 7 platform epics (RWB-PLT-TPL, LIB, WF, DB, EVT, EDGE, OBS) and 5 integration epics (RWB-ITG-W1 to W4 and NFR).
Every story also carries its business epic EP01 to EP08 as a tag; the owner is a suggestion only and any team may pick up the story.
Run material: Template and Rules v1, Ownership Map v1, Change Register v1; gaps and assumptions in the registers in folder 23.
All release dates on slide 9 are marked tentative and are unchanged (U7, DL48).
Slide numbers follow version 5, where this document-control slide is slide 1.

15

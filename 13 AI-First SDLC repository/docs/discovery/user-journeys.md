<!-- working-copy-of: requirement/legacy/02-business-architecture-and-process/recovery-workbench-user-journeys-v2-pptx.md -->
> **Working copy.** Canonical source: `requirement/legacy/02-business-architecture-and-process/recovery-workbench-user-journeys-v2-pptx.md`. Edit the source, not this copy.

## Slide 1

SCB

COLLECTIONS AND RECOVERY TRANSFORMATION Recovery Workbench: user journeys

Henka Group, 28 October 2026 (C) Siam Commercial Bank and Henka Pte Ltd

## Slide 2

One page per role

2

Six non-human actors also act on cases: the case workflow module, the rules component, the data load, the OCR pipeline, the decision log writer and the agent platform.

| Group | Roles | Each page shows |
|---|---|---|
| Bank business roles | 30 | The work, the screens, how the person gets access and what they do when something goes wrong |
| Administration and control roles | 7 | The work, the screens, how the person gets access and what they do when something goes wrong |
| Partner roles | 7 | The work, the screens, how the person gets access and what they do when something goes wrong |
| Customer parties | 4 | The work, the screens, how the person gets access and what they do when something goes wrong |

## Slide 3

Bank business roles 30 roles

3

## Slide 4

Case owner

4

The work Owns the case from day 90 to close. Accepts the hand-over, reads expected net recovery after cost per route, approves inside the limit, answers for ageing against the service level Shared operations. Processes: 06 to 10.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: Own; real users from E2 (31 Dec 2026)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager A decision that cannot be recorded is not taken (MSG-P7-003); try again or raise an incident

| Screen | What it is for |
|---|---|
| Case record | One case: accounts, parties, stage, owner, clocks, deviations, documents, decisions and history on one timeline |
| Deviation queue | Open deviations by type, handler and age |
| Exception queue | Cases and records that no rule matched, failed outbound actions and held receipts |
| Approval queue | Decisions waiting for the person's approval level, with the facts and the recommendation |

## Slide 5

Team manager

5

The work Runs the team: allocation overrides, reassignment, caseload and service level breaches, coaching, the spread between collectors Shared operations. Processes: 06 to 10.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: Team; real users from E2 (31 Dec 2026)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role An approval above the limit is routed to the next level (MSG-P7-001); a decision they prepared goes to another approver (MSG-P7-002) Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager

| Screen | What it is for |
|---|---|
| Transfer case | Move a case to another owner or queue with a reason |
| Team queues | Cases by queue with age, cap use and overflow |
| Deviation queue | Open deviations by type, handler and age |
| Exception queue | Cases and records that no rule matched, failed outbound actions and held receipts |

## Slide 6

Phone collector

6

The work Works the pre-90 list on EFS. Reads the case record for accounts that have moved to recovery so the customer is not called twice Shared operations. Processes: pre-06.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: Own; real users from E2 (31 Dec 2026)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager A decision that cannot be recorded is not taken (MSG-P7-003); try again or raise an incident

| Screen | What it is for |
|---|---|
| Case record | One case: accounts, parties, stage, owner, clocks, deviations, documents, decisions and history on one timeline |
| My work | The person's open tasks, cases near a deadline and approvals waiting |
| Case list | Every case in the person's scope, with filters by product, stage, owner, age and deviation |
| Case timeline | Every action, decision, transfer, letter and document on the case, with filters |

## Slide 7

Field collector

7

The work Visits the customer or the asset, captures photos, bills and signed documents into the case through the field app Shared operations, field. Processes: 06, 09.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: Own; real users from E7 (31 May 2027)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager A decision that cannot be recorded is not taken (MSG-P7-003); try again or raise an incident

| Screen | What it is for |
|---|---|
| Case record | One case: accounts, parties, stage, owner, clocks, deviations, documents, decisions and history on one timeline |
| Asset record | One asset: title, condition, photographs, valuations, costs, listing and sale history |
| My work | The person's open tasks, cases near a deadline and approvals waiting |
| Case list | Every case in the person's scope, with filters by product, stage, owner, age and deviation |

## Slide 8

Restructuring officer (FCR)

8

The work Builds and sends the restructure offer inside the band, records affordability, books the plan. Exceptions only reach a person FCR, restructuring. Processes: 07.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: Team; real users from E3 (31 Jan 2027)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role An approval above the limit is routed to the next level (MSG-P7-001); a decision they prepared goes to another approver (MSG-P7-002) Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager

| Screen | What it is for |
|---|---|
| Decision screen | The recommendation with reasons, the expected return by route, the limit check and approve, return or refuse |
| Treatment record | The restructure, settlement or deed in lieu offer, its terms, its status and the booking confirmation |
| Settlement offer | Payoff, offer range, floor and the gap to the floor |
| My work | The person's open tasks, cases near a deadline and approvals waiting |

## Slide 9

Hardship and vulnerability specialist

9

The work Takes cases flagged X2 or X3, sets contact limits, decides a hardship plan or a BOT relief program Shared operations. Processes: 11 deviations.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: Team; real users from E7 (31 May 2027)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager A decision that cannot be recorded is not taken (MSG-P7-003); try again or raise an incident

| Screen | What it is for |
|---|---|
| Case record | One case: accounts, parties, stage, owner, clocks, deviations, documents, decisions and history on one timeline |
| Raise deviation | Raise X1 to X7 on a case with the reason and the evidence |
| Deviation queue | Open deviations by type, handler and age |
| Exception queue | Cases and records that no rule matched, failed outbound actions and held receipts |

## Slide 10

Complaint officer

10

The work Takes X1 disputes and complaints, applies the contact stop, builds the evidence pack, resolves inside the service level and returns the case to the same decision Conduct, shared operations. Processes: 11 deviations.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: Team; real users from E7 (31 May 2027)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager A decision that cannot be recorded is not taken (MSG-P7-003); try again or raise an incident

| Screen | What it is for |
|---|---|
| Raise deviation | Raise X1 to X7 on a case with the reason and the evidence |
| Deviation queue | Open deviations by type, handler and age |
| Exception queue | Cases and records that no rule matched, failed outbound actions and held receipts |
| Approval queue | Decisions waiting for the person's approval level, with the facts and the recommendation |

## Slide 11

Fraud investigator

11

The work Takes X4 referrals, investigates, confirms or clears, which sends the case to D9 or back to D2 Fraud. Processes: 11 deviations.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E7 (31 May 2027)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager A decision that cannot be recorded is not taken (MSG-P7-003); try again or raise an incident

| Screen | What it is for |
|---|---|
| Case record | One case: accounts, parties, stage, owner, clocks, deviations, documents, decisions and history on one timeline |
| Raise deviation | Raise X1 to X7 on a case with the reason and the evidence |
| Deviation queue | Open deviations by type, handler and age |
| Exception queue | Cases and records that no rule matched, failed outbound actions and held receipts |

## Slide 12

Litigation officer

12

The work Checks the agent-assembled case pack against the defect list, instructs the law firm, files, manages to judgment Legal and litigation. Processes: 08.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: Team; real users from E2 (31 Dec 2026)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role An approval above the limit is routed to the next level (MSG-P7-001); a decision they prepared goes to another approver (MSG-P7-002) Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager

| Screen | What it is for |
|---|---|
| Litigation workspace | Pack, instruction, court dates, hearings and judgment for a case |
| Enforcement workspace | Enforcement steps with the Legal Execution Department and the result |
| Partner scorecard | Monthly score per partner against its measures |
| Notice approval | Generated demand and recall notices for approval before dispatch |

## Slide 13

Enforcement owner

13

The work Owns enforcement after judgment: seizure, LED auction entry, or a coded deferral with its reason. One of the three points with no owner today Legal and litigation. Processes: 08.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: Team; real users from E5 (31 Mar 2027)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager A decision that cannot be recorded is not taken (MSG-P7-003); try again or raise an incident

| Screen | What it is for |
|---|---|
| Litigation workspace | Pack, instruction, court dates, hearings and judgment for a case |
| Enforcement workspace | Enforcement steps with the Legal Execution Department and the result |
| My work | The person's open tasks, cases near a deadline and approvals waiting |
| Case list | Every case in the person's scope, with filters by product, stage, owner, age and deviation |

## Slide 14

Legal counsel

14

The work Approves notice and contract templates, rules on estate and bankruptcy claims, joins X3 and X5 deviations Legal. Processes: 08, 11.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E3 (31 Jan 2027)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role An approval above the limit is routed to the next level (MSG-P7-001); a decision they prepared goes to another approver (MSG-P7-002) Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager

| Screen | What it is for |
|---|---|
| Raise deviation | Raise X1 to X7 on a case with the reason and the evidence |
| Deviation queue | Open deviations by type, handler and age |
| Approval queue | Decisions waiting for the person's approval level, with the facts and the recommendation |
| Notice approval | Generated demand and recall notices for approval before dispatch |

## Slide 15

Sale officer

15

The work Runs the auction schedule, the listing and the price ladder, approves inside the floor, sends anything below it for a second signature Shared operations with the product head. Processes: 09.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: Team; real users from E3 (31 Jan 2027)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role An approval above the limit is routed to the next level (MSG-P7-001); a decision they prepared goes to another approver (MSG-P7-002) Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager

| Screen | What it is for |
|---|---|
| Asset list | Assets held, with age, holding cost, value and sale status |
| Asset record | One asset: title, condition, photographs, valuations, costs, listing and sale history |
| Listing and price | List price, floor and the price ladder for an asset |
| Document review queue | Low-confidence extractions to check and correct |

## Slide 16

NPA and asset manager

16

The work Holds and manages repossessed assets: custody, insurance, maintenance, the stock balance. The stock balance is one of the three unowned points today Asset liquidity. Processes: 09.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: Team; real users from E3 (31 Jan 2027)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager A decision that cannot be recorded is not taken (MSG-P7-003); try again or raise an incident

| Screen | What it is for |
|---|---|
| Asset list | Assets held, with age, holding cost, value and sale status |
| Asset record | One asset: title, condition, photographs, valuations, costs, listing and sale history |
| My work | The person's open tasks, cases near a deadline and approvals waiting |
| Case list | Every case in the person's scope, with filters by product, stage, owner, age and deviation |

## Slide 17

Debt sale officer

17

The work Builds the lots, sets the reserve from the model, runs the buyer process, transfers the data on award Asset liquidity. Processes: 09.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: Team; real users from E6 (30 Apr 2027)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role An approval above the limit is routed to the next level (MSG-P7-001); a decision they prepared goes to another approver (MSG-P7-002) Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager

| Screen | What it is for |
|---|---|
| Decision screen | The recommendation with reasons, the expected return by route, the limit check and approve, return or refuse |
| Lot builder | Select accounts, build lots, set the reserve and send for approval |
| Award | Bids against the reserve and the award decision |
| My work | The person's open tasks, cases near a deadline and approvals waiting |

## Slide 18

Write-off team member

18

The work Runs the monthly scan on both tracks, proposes the population, prepares the committee pack Credit administration. Processes: 10.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: Team; real users from E6 (30 Apr 2027)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager A decision that cannot be recorded is not taken (MSG-P7-003); try again or raise an incident

| Screen | What it is for |
|---|---|
| Committee pack | The pack for a committee decision with each member's vote |
| Write-off proposal | The monthly population, the pack per case and removals with reasons |
| My work | The person's open tasks, cases near a deadline and approvals waiting |
| Case list | Every case in the person's scope, with filters by product, stage, owner, age and deviation |

## Slide 19

Credit Administration officer

19

The work Posts the approved write-off, releases the provision, publishes completeness, records post charge-off recovery Credit administration. Processes: 10.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: Team; real users from E3 (31 Jan 2027)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role An approval above the limit is routed to the next level (MSG-P7-001); a decision they prepared goes to another approver (MSG-P7-002) Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager

| Screen | What it is for |
|---|---|
| Decision screen | The recommendation with reasons, the expected return by route, the limit check and approve, return or refuse |
| Posting | Approved bookings and postings with the confirmation from the next load |
| Proceeds matching | Receipts matched to cases and the unmatched list |
| My work | The person's open tasks, cases near a deadline and approvals waiting |

## Slide 20

Guarantee officer

20

The work Files and tracks TCG and insurance claims, records the subrogation position Shared operations. Processes: 07.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: Team; real users from E4 (28 Feb 2027)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager A decision that cannot be recorded is not taken (MSG-P7-003); try again or raise an incident

| Screen | What it is for |
|---|---|
| Guarantee claim | The guarantee, the claim deadline, the checklist and the claim result |
| Litigation workspace | Pack, instruction, court dates, hearings and judgment for a case |
| Enforcement workspace | Enforcement steps with the Legal Execution Department and the result |
| My work | The person's open tasks, cases near a deadline and approvals waiting |

## Slide 21

Partner and agency manager

21

The work Runs every partner type on the same six points: selection, contract and fees, targets and incentives, data exchange, performance reviews, notice and exit. Sets placements by measured return OA management team. Processes: 06 to 10, 12.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E6 (30 Apr 2027)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role An approval above the limit is routed to the next level (MSG-P7-001); a decision they prepared goes to another approver (MSG-P7-002) Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager

| Screen | What it is for |
|---|---|
| Decision screen | The recommendation with reasons, the expected return by route, the limit check and approve, return or refuse |
| Partner list | Partners, contracts, panel status and scorecards |
| Placement and allocation | Work placed with partners by rule, with recalls and re-selection |
| Partner scorecard | Monthly score per partner against its measures |

## Slide 22

Conduct and QA officer

22

The work Reviews contacts blocked by the contact check, matches complaints to the preceding contact, samples decisions against the rule version applied Conduct, center of excellence. Processes: all.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E8 (30 Jun 2027)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager A decision that cannot be recorded is not taken (MSG-P7-003); try again or raise an incident

| Screen | What it is for |
|---|---|
| Document review queue | Low-confidence extractions to check and correct |
| My work | The person's open tasks, cases near a deadline and approvals waiting |
| Case list | Every case in the person's scope, with filters by product, stage, owner, age and deviation |
| Case record | One case: accounts, parties, stage, owner, clocks, deviations, documents, decisions and history on one timeline |

## Slide 23

Capacity and workforce planner

23

The work Sets next week's roster from inflow by product, bucket and region, the answer curve and the field coverage map. A role with no structure chart today Shared operations. Processes: all.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E2 (31 Dec 2026)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager A decision that cannot be recorded is not taken (MSG-P7-003); try again or raise an incident

| Screen | What it is for |
|---|---|
| Team queues | Cases by queue with age, cap use and overflow |
| My work | The person's open tasks, cases near a deadline and approvals waiting |
| Case list | Every case in the person's scope, with filters by product, stage, owner, age and deviation |
| Case record | One case: accounts, parties, stage, owner, clocks, deviations, documents, decisions and history on one timeline |

## Slide 24

Product head (Mortgage, HP, SSME)

24

The work Owns approval limits for the product, approves above the case owner limit, owns the floor price and the band Product. Processes: 07 to 10.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E2 (31 Dec 2026)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role An approval above the limit is routed to the next level (MSG-P7-001); a decision they prepared goes to another approver (MSG-P7-002) Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager

| Screen | What it is for |
|---|---|
| Deviation queue | Open deviations by type, handler and age |
| Exception queue | Cases and records that no rule matched, failed outbound actions and held receipts |
| Approval queue | Decisions waiting for the person's approval level, with the facts and the recommendation |
| Notice approval | Generated demand and recall notices for approval before dispatch |

## Slide 25

Head of Litigation

25

The work Approves legal spend above the limit, rules on panel conflicts and escalations Legal and litigation. Processes: 08.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E2 (31 Dec 2026)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role An approval above the limit is routed to the next level (MSG-P7-001); a decision they prepared goes to another approver (MSG-P7-002) Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager

| Screen | What it is for |
|---|---|
| Deviation queue | Open deviations by type, handler and age |
| Exception queue | Cases and records that no rule matched, failed outbound actions and held receipts |
| Approval queue | Decisions waiting for the person's approval level, with the facts and the recommendation |
| Notice approval | Generated demand and recall notices for approval before dispatch |

## Slide 26

Head of NPA

26

The work Approves holding, price steps below the floor and transfers to RAMC Asset liquidity. Processes: 09.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E3 (31 Jan 2027)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role An approval above the limit is routed to the next level (MSG-P7-001); a decision they prepared goes to another approver (MSG-P7-002) Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager

| Screen | What it is for |
|---|---|
| Deviation queue | Open deviations by type, handler and age |
| Approval queue | Decisions waiting for the person's approval level, with the facts and the recommendation |
| Notice approval | Generated demand and recall notices for approval before dispatch |
| Asset list | Assets held, with age, holding cost, value and sale status |

## Slide 27

Head of Asset Liquidity

27

The work Approves lots, reserve prices and buyer panel changes Asset liquidity. Processes: 09.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E6 (30 Apr 2027)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role An approval above the limit is routed to the next level (MSG-P7-001); a decision they prepared goes to another approver (MSG-P7-002) Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager

| Screen | What it is for |
|---|---|
| Deviation queue | Open deviations by type, handler and age |
| Approval queue | Decisions waiting for the person's approval level, with the facts and the recommendation |
| Notice approval | Generated demand and recall notices for approval before dispatch |
| Lot builder | Select accounts, build lots, set the reserve and send for approval |

## Slide 28

Credit approval committee member

28

The work Approves restructures and settlements above the delegated limit Credit. Processes: 07.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E4 (28 Feb 2027)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role An approval above the limit is routed to the next level (MSG-P7-001); a decision they prepared goes to another approver (MSG-P7-002) Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager

| Screen | What it is for |
|---|---|
| Deviation queue | Open deviations by type, handler and age |
| Approval queue | Decisions waiting for the person's approval level, with the facts and the recommendation |
| Committee pack | The pack for a committee decision with each member's vote |
| Document review queue | Low-confidence extractions to check and correct |

## Slide 29

Write-off committee member

29

The work Approves the write-off population inside the delegation, rules on the exception loop Credit, Finance, Risk. Processes: 10.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E6 (30 Apr 2027)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role An approval above the limit is routed to the next level (MSG-P7-001); a decision they prepared goes to another approver (MSG-P7-002) Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager

| Screen | What it is for |
|---|---|
| Deviation queue | Open deviations by type, handler and age |
| Approval queue | Decisions waiting for the person's approval level, with the facts and the recommendation |
| Committee pack | The pack for a committee decision with each member's vote |
| Document review queue | Low-confidence extractions to check and correct |

## Slide 30

Risk and model risk officer

30

The work Reviews drift and calibration, raises a decision with an owner and a date on a breach, signs rule version changes Risk. Processes: all.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E2 (31 Dec 2026)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role An approval above the limit is routed to the next level (MSG-P7-001); a decision they prepared goes to another approver (MSG-P7-002) Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager

| Screen | What it is for |
|---|---|
| My work | The person's open tasks, cases near a deadline and approvals waiting |
| Case list | Every case in the person's scope, with filters by product, stage, owner, age and deviation |
| Case record | One case: accounts, parties, stage, owner, clocks, deviations, documents, decisions and history on one timeline |
| Case timeline | Every action, decision, transfer, letter and document on the case, with filters |

## Slide 31

Finance and CFO delegate

31

The work Reviews benefit realisation monthly, owns the provision and posting rules Finance. Processes: 10.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E6 (30 Apr 2027)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role An approval above the limit is routed to the next level (MSG-P7-001); a decision they prepared goes to another approver (MSG-P7-002) Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager

| Screen | What it is for |
|---|---|
| Posting | Approved bookings and postings with the confirmation from the next load |
| Steering dashboard | Inflow, stock, cures, recovery, turnaround and cost, by product and route |
| My work | The person's open tasks, cases near a deadline and approvals waiting |
| Case list | Every case in the person's scope, with filters by product, stage, owner, age and deviation |

## Slide 32

Reporting and BI analyst

32

The work Builds and runs the steering dashboard, the queue measures and the regulatory extracts Data and analytics. Processes: all.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E2 (31 Dec 2026)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager A decision that cannot be recorded is not taken (MSG-P7-003); try again or raise an incident

| Screen | What it is for |
|---|---|
| Litigation workspace | Pack, instruction, court dates, hearings and judgment for a case |
| Enforcement workspace | Enforcement steps with the Legal Execution Department and the result |
| Lot builder | Select accounts, build lots, set the reserve and send for approval |
| My work | The person's open tasks, cases near a deadline and approvals waiting |

## Slide 33

Tribe lead and squad members

33

The work Run the weekly squad review, own the backlog and the release train Collections and Recovery Tribe. Processes: all.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E2 (31 Dec 2026)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role Stale data (MSG-P1-001): the decision waits for the next load, or the input is refreshed A case that does not fit any rule goes to the exception queue for the team manager A decision that cannot be recorded is not taken (MSG-P7-003); try again or raise an incident

| Screen | What it is for |
|---|---|
| My work | The person's open tasks, cases near a deadline and approvals waiting |
| Case list | Every case in the person's scope, with filters by product, stage, owner, age and deviation |
| Case record | One case: accounts, parties, stage, owner, clocks, deviations, documents, decisions and history on one timeline |
| Case timeline | Every action, decision, transfer, letter and document on the case, with filters |

## Slide 34

Administration and control roles 7 roles

34

## Slide 35

Center of excellence analyst

35

The work Owns the rule tables, the parameter catalog, the measure definitions and the QA program. Loads and rolls back rule versions Center of excellence. Processes: all.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E1 (30 Nov 2026)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role A failed load or job shows on the interface and job monitor; rerun after the source is fixed, or raise an incident A bad rule or reference version is rolled back by loading the previous version A decision that cannot be recorded is not taken (MSG-P7-003); try again or raise an incident

| Screen | What it is for |
|---|---|
| Reference data | Lists of values and reference tables with versions |
| Rules and parameters | Rule versions, route sets, thresholds and timers, with the load and approval |
| Agent monitor | Agent runs, fallbacks, evaluation results and autonomy levels |
| My work | The person's open tasks, cases near a deadline and approvals waiting |

## Slide 36

Data steward and data product owner

36

The work Owns a data product: definition, quality rules, freshness, access. Signs the daily reconciliation to ALS Data and analytics. Processes: all.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E1 (30 Nov 2026)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role A failed load or job shows on the interface and job monitor; rerun after the source is fixed, or raise an incident A bad rule or reference version is rolled back by loading the previous version A decision that cannot be recorded is not taken (MSG-P7-003); try again or raise an incident

| Screen | What it is for |
|---|---|
| Data quality | Load check results, reconciliation breaks and stale data products |
| My work | The person's open tasks, cases near a deadline and approvals waiting |
| Case list | Every case in the person's scope, with filters by product, stage, owner, age and deviation |
| Case record | One case: accounts, parties, stage, owner, clocks, deviations, documents, decisions and history on one timeline |

## Slide 37

Internal audit

37

The work Queries the decision log, samples cases, tests that every action carries a rule version and an approver Audit. Processes: all.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E1 (30 Nov 2026)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role A failed load or job shows on the interface and job monitor; rerun after the source is fixed, or raise an incident A bad rule or reference version is rolled back by loading the previous version A decision that cannot be recorded is not taken (MSG-P7-003); try again or raise an incident

| Screen | What it is for |
|---|---|
| Decision screen | The recommendation with reasons, the expected return by route, the limit check and approve, return or refuse |
| Route decision | The route recommendation with the expected return of each route and the reasons |
| Decision log query | Search the decision log by case, rule, approver and date, with export |
| My work | The person's open tasks, cases near a deadline and approvals waiting |

## Slide 38

Compliance and PDPA officer

38

The work Rules on data subject requests, consent, retention and masking. Approves regulatory reporting content Compliance. Processes: all.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E1 (30 Nov 2026)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role A failed load or job shows on the interface and job monitor; rerun after the source is fixed, or raise an incident A bad rule or reference version is rolled back by loading the previous version A decision that cannot be recorded is not taken (MSG-P7-003); try again or raise an incident

| Screen | What it is for |
|---|---|
| Personal data | Retention classes, masking rules, consent log and data subject requests |
| My work | The person's open tasks, cases near a deadline and approvals waiting |
| Case list | Every case in the person's scope, with filters by product, stage, owner, age and deviation |
| Case record | One case: accounts, parties, stage, owner, clocks, deviations, documents, decisions and history on one timeline |

## Slide 39

Platform administrator

39

The work Runs the environment: configuration service, feature flags, jobs, interfaces, incident handling, break-glass TechX platform. Processes: all.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E1 (30 Nov 2026)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role A failed load or job shows on the interface and job monitor; rerun after the source is fixed, or raise an incident A bad rule or reference version is rolled back by loading the previous version A decision that cannot be recorded is not taken (MSG-P7-003); try again or raise an incident

| Screen | What it is for |
|---|---|
| Interface and job monitor | Loads, files, jobs and outbound actions with status and reruns |
| Agent monitor | Agent runs, fallbacks, evaluation results and autonomy levels |
| Exception queue | Cases and records that no rule matched, failed outbound actions and held receipts |
| My work | The person's open tasks, cases near a deadline and approvals waiting |

## Slide 40

Reference data administrator

40

The work Maintains the versioned reference tables: queues, roles, templates, document checklists, action codes, product parameters Center of excellence. Processes: all.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E1 (30 Nov 2026)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role A failed load or job shows on the interface and job monitor; rerun after the source is fixed, or raise an incident A bad rule or reference version is rolled back by loading the previous version A decision that cannot be recorded is not taken (MSG-P7-003); try again or raise an incident

| Screen | What it is for |
|---|---|
| Reference data | Lists of values and reference tables with versions |
| Rules and parameters | Rule versions, route sets, thresholds and timers, with the load and approval |
| Delegation of authority | Approval levels, holders, limits and substitutes |
| Approval queue | Decisions waiting for the person's approval level, with the facts and the recommendation |

## Slide 41

Security administrator

41

The work Owns the role to permission matrix, joiner mover leaver, break-glass approval, the access log SCB IT security. Processes: all.

How they get access The line manager requests the role in the bank IAM; the role owner approves The person joins the Entra ID group for the role in each environment (DL40) Sign-in through the ACE front end with multi-factor authentication Scope: All; real users from E1 (30 Nov 2026)

When something goes wrong A screen or action refused (MSG-P4-002 or MSG-P4-003): ask the team manager to request the right role An approval above the limit is routed to the next level (MSG-P7-001); a decision they prepared goes to another approver (MSG-P7-002) A failed load or job shows on the interface and job monitor; rerun after the source is fixed, or raise an incident A bad rule or reference version is rolled back by loading the previous version

| Screen | What it is for |
|---|---|
| Roles and access | Roles, permissions, scope and the group mapping, with the access log |
| Approval queue | Decisions waiting for the person's approval level, with the facts and the recommendation |
| Decision screen | The recommendation with reasons, the expected return by route, the limit check and approve, return or refuse |
| Committee pack | The pack for a committee decision with each member's vote |

## Slide 42

Partner roles 7 roles

42

## Slide 43

Collection agency (OA) user

43

The work Receives placements, records contact outcomes and payments, returns the account at recall or panel exit 73 agencies on a fixed 20 percent share. Processes: 06, 10.

How they get access The partner and agency manager requests the user for the firm; the role owner approves A partner identity, separate from bank identities, with multi-factor authentication Through the external gateway once external access is approved (DL03); until then the current channels Scope: the instructions placed with the firm; real users from E6

When something goes wrong An instruction they cannot take is declined with a reason; the next firm is selected A missed service level is raised to the partner and agency manager A portal problem goes to the partner and agency manager, who raises it with the platform administrator

| Screen | What it is for |
|---|---|
| Partner home | The partner's open instructions, due dates and messages |
| Instruction | One instruction with its documents, due dates and the result to record |
| Upload result | Record a result and upload its documents |
| Invoice | Submit a fee invoice against completed instructions |

## Slide 44

Law firm user

44

The work Receives the instruction and the case pack, files, reports court state and hearing dates, invoices against the fee schedule 11 to 12 firms on the panel. Processes: 08.

How they get access The partner and agency manager requests the user for the firm; the role owner approves A partner identity, separate from bank identities, with multi-factor authentication Through the external gateway once external access is approved (DL03); until then the current channels Scope: the instructions placed with the firm; real users from E5

When something goes wrong An instruction they cannot take is declined with a reason; the next firm is selected A missed service level is raised to the partner and agency manager A portal problem goes to the partner and agency manager, who raises it with the platform administrator

| Screen | What it is for |
|---|---|
| Partner home | The partner's open instructions, due dates and messages |
| Instruction | One instruction with its documents, due dates and the result to record |
| Invoice | Submit a fee invoice against completed instructions |
| Upload result | Record a result and upload its documents |

## Slide 45

Valuer

45

The work Receives the valuation instruction, uploads the report and the value, which feeds the band and the floor Panel valuers. Processes: 07, 09.

How they get access The partner and agency manager requests the user for the firm; the role owner approves A partner identity, separate from bank identities, with multi-factor authentication Through the external gateway once external access is approved (DL03); until then the current channels Scope: the instructions placed with the firm; real users from E4

When something goes wrong An instruction they cannot take is declined with a reason; the next firm is selected A missed service level is raised to the partner and agency manager A portal problem goes to the partner and agency manager, who raises it with the platform administrator

| Screen | What it is for |
|---|---|
| Partner home | The partner's open instructions, due dates and messages |
| Instruction | One instruction with its documents, due dates and the result to record |
| Upload result | Record a result and upload its documents |
| Invoice | Submit a fee invoice against completed instructions |

## Slide 46

Auction vendor

46

The work Runs the auction rounds on the ladder, reports results per round, settles proceeds 4 vendors allocated by distance. Processes: 09.

How they get access The partner and agency manager requests the user for the firm; the role owner approves A partner identity, separate from bank identities, with multi-factor authentication Through the external gateway once external access is approved (DL03); until then the current channels Scope: the instructions placed with the firm; real users from E4

When something goes wrong An instruction they cannot take is declined with a reason; the next firm is selected A missed service level is raised to the partner and agency manager A portal problem goes to the partner and agency manager, who raises it with the platform administrator

| Screen | What it is for |
|---|---|
| Partner home | The partner's open instructions, due dates and messages |
| Upload result | Record a result and upload its documents |
| Invoice | Submit a fee invoice against completed instructions |

## Slide 47

Debt buyer and AMC

47

The work Qualifies, views the lot data room, bids, receives the data transfer on award, confirms remittance 35 buyers. Processes: 09.

How they get access The partner and agency manager requests the user for the firm; the role owner approves A partner identity, separate from bank identities, with multi-factor authentication Through the external gateway once external access is approved (DL03); until then the current channels Scope: the instructions placed with the firm; real users from E5

When something goes wrong An instruction they cannot take is declined with a reason; the next firm is selected A missed service level is raised to the partner and agency manager A portal problem goes to the partner and agency manager, who raises it with the platform administrator

| Screen | What it is for |
|---|---|
| Partner home | The partner's open instructions, due dates and messages |
| Transfer confirmation | Confirm a transfer of assets or accounts |
| Data room | Lot data tapes and documents for admitted buyers, with bids |

## Slide 48

RAMC user

48

The work Takes the transfer of assets and accounts that move to RAMC and confirms the position SCB asset management company. Processes: 09.

How they get access The partner and agency manager requests the user for the firm; the role owner approves A partner identity, separate from bank identities, with multi-factor authentication Through the external gateway once external access is approved (DL03); until then the current channels Scope: the instructions placed with the firm; real users from E4

When something goes wrong An instruction they cannot take is declined with a reason; the next firm is selected A missed service level is raised to the partner and agency manager A portal problem goes to the partner and agency manager, who raises it with the platform administrator

| Screen | What it is for |
|---|---|
| Partner home | The partner's open instructions, due dates and messages |
| Transfer confirmation | Confirm a transfer of assets or accounts |

## Slide 49

Legal Execution Department and court officer

49

The work Runs the enforcement auction on the 100 / 90 / 80 / 70 percent ladder and issues the official value. Reached by interface and filing, not by a Workbench login Government. Processes: 08, 09.

Screens No login: filing and result interfaces

How they get access No sign-in. Filings and results reach the case through the law firms in the partner portal Court and LED results are recorded against the legal action

When something goes wrong An instruction they cannot take is declined with a reason; the next firm is selected A missed service level is raised to the partner and agency manager A portal problem goes to the partner and agency manager, who raises it with the platform administrator

## Slide 50

Customer parties 4 roles

50

## Slide 51

Customer (borrower)

51

The work Is told who owns the case, supplies documents, accepts or declines an offer, signs, pays, hands over an asset Retail and SSME customers. Processes: 06 to 10.

Screens Notices, HOME.SCB, e-signature link

How they get access No Workbench sign-in Reached through bank channels: HOME.SCB, LINE, SMS, letter Notices and offers are generated by the Workbench and sent through those channels

When something goes wrong A complaint or dispute through the contact center or a branch raises X1 and stops contact on the disputed item Hardship raises X2 and the vulnerable customer treatment applies A data request follows the bank's PDPA process

## Slide 52

Guarantor and co-borrower

52

The work Receives the demand, answers it, may pay, settle or be pursued Connected parties. Processes: 07, 08.

Screens Notices, e-signature link

How they get access No Workbench sign-in Reached through bank channels: Letter, SMS Notices and offers are generated by the Workbench and sent through those channels

When something goes wrong A complaint or dispute through the contact center or a branch raises X1 and stops contact on the disputed item Hardship raises X2 and the vulnerable customer treatment applies A data request follows the bank's PDPA process

## Slide 53

Heir and estate representative

53

The work Is notified on a death, supplies the certificate, deals with the estate claim Connected parties. Processes: 11 deviations.

Screens Notices

How they get access No Workbench sign-in Reached through bank channels: Letter Notices and offers are generated by the Workbench and sent through those channels

When something goes wrong A complaint or dispute through the contact center or a branch raises X1 and stops contact on the disputed item Hardship raises X2 and the vulnerable customer treatment applies A data request follows the bank's PDPA process

## Slide 54

Retail asset bidder

54

The work Views the listing and bids in an auction round Public. Processes: 09.

Screens Public listing, auction portal

How they get access No Workbench sign-in Reached through bank channels: Auction portals Notices and offers are generated by the Workbench and sent through those channels

When something goes wrong A complaint or dispute through the contact center or a branch raises X1 and stops contact on the disputed item Hardship raises X2 and the vulnerable customer treatment applies A data request follows the bank's PDPA process

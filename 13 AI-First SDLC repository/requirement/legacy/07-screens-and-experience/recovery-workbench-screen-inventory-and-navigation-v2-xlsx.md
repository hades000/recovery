<!-- source: 07 Screens and experience/Recovery Workbench Screen Inventory and Navigation v2.xlsx -->
<!-- converted: 2026-11-04 from XLSX -->

> **Source:** `07 Screens and experience/Recovery Workbench Screen Inventory and Navigation v2.xlsx`  
> **Converted from:** XLSX

## Screens

| Every screen |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|
| 53 screens: 47 in the Workbench and 6 in the partner portal. Every screen is in the ACE front end; the access check runs on each request. |  |  |  |  |  |  |  |  |  |
| ID | Menu | Screen | What it is for | Reached from | Module | Capability area | Who reaches it | First in | States |
| SCR-01 | Home | My work | The person's open tasks, cases near a deadline and approvals waiting | Sign-in | P3 | Case record | All bank roles | E2 | Loading; empty; list |
| SCR-02 | Cases | Case list | Every case in the person's scope, with filters by product, stage, owner, age and deviation | Menu | P3 | Case record | Case owner, team manager, officers, product heads, control functions | E1 | Loading; empty; list; filtered |
| SCR-03 | Cases | Case record | One case: accounts, parties, stage, owner, clocks, deviations, documents, decisions and history on one timeline | Case list; my work; search | P3 | Case record | Every bank role in scope | E1 read only; E2 full | Loading; read only; editable; on hold |
| SCR-04 | Cases | Case timeline | Every action, decision, transfer, letter and document on the case, with filters | Case record | P3 | Case record | Every bank role in scope | E2 | Loading; filtered |
| SCR-05 | Cases | Transfer case | Move a case to another owner or queue with a reason | Case record; team queues | P3 | Queue and allocation | Team manager | E2 | Form; at cap warning; saved |
| SCR-06 | Cases | Raise deviation | Raise X1 to X7 on a case with the reason and the evidence | Case record | S8 | Case record | Case owner, officers, specialists | E2 | Form; saved |
| SCR-07 | Queues | Team queues | Cases by queue with age, cap use and overflow | Menu | P3 | Queue and allocation | Team manager, capacity and workforce planner | E2 | Loading; list |
| SCR-08 | Queues | Deviation queue | Open deviations by type, handler and age | Menu | S8 | Case record | Specialists, complaint officer, fraud investigator, legal counsel | E2 | Loading; list |
| SCR-09 | Queues | Exception queue | Cases and records that no rule matched, failed outbound actions and held receipts | Menu | P3 | Queue and allocation | Team manager, platform administrator | E1 | Loading; list |
| SCR-10 | Approvals | Approval queue | Decisions waiting for the person's approval level, with the facts and the recommendation | Menu; my work | P7 | Decision log | Approvers at each level, committees | E2 | Loading; list |
| SCR-11 | Approvals | Decision screen | The recommendation with reasons, the expected return by route, the limit check and approve, return or refuse | Approval queue; case record | P7 | Decision log | Approvers at each level | E2 | Ready; above limit; stale input; decided |
| SCR-12 | Approvals | Committee pack | The pack for a committee decision with each member's vote | Approval queue | P7 | Decision log | Credit approval committee, write-off committee | E4 | Draft; circulated; decided |
| SCR-13 | Treatment | Route decision | The route recommendation with the expected return of each route and the reasons | Case record | S1 | Treatment and offer | Case owner | E4 | Loading; recommendation; overridden; submitted |
| SCR-14 | Treatment | Treatment record | The restructure, settlement or deed in lieu offer, its terms, its status and the booking confirmation | Case record | S2 | Treatment and offer | Case owner, restructuring officer (FCR) | E2 record; E3 full | Draft; submitted; approved; booked; broken |
| SCR-15 | Treatment | Settlement offer | Payoff, offer range, floor and the gap to the floor | Treatment record | S2 | Treatment and offer | Case owner, restructuring officer (FCR) | E3 | Draft; below floor; approved; sent; accepted |
| SCR-16 | Treatment | Deed in lieu | Readiness checks, appraisal order, transfer and asset take-on | Treatment record | S2 | Treatment and offer | Case owner, sale officer | E3 | Checks; appraisal; approved; transferred |
| SCR-17 | Treatment | Guarantee claim | The guarantee, the claim deadline, the checklist and the claim result | Case record | S3 | Treatment and offer | Guarantee officer | E4 | Not due; due; submitted; paid; refused |
| SCR-18 | Litigation | Notice approval | Generated demand and recall notices for approval before dispatch | Case record; my work | S4 | Litigation | Litigation officer, legal counsel | E2 | Generated; approved; sent; delivered; unserved |
| SCR-19 | Litigation | Litigation workspace | Pack, instruction, court dates, hearings and judgment for a case | Case record | S4 | Litigation | Litigation officer, Head of Litigation | E5 | Pack; instructed; filed; hearing; judgment |
| SCR-20 | Litigation | Enforcement workspace | Enforcement steps with the Legal Execution Department and the result | Case record | S4 | Litigation | Enforcement owner | E5 | Requested; seized; auctioned; closed |
| SCR-21 | Assets | Asset list | Assets held, with age, holding cost, value and sale status | Menu | S5 | Asset and disposal | Sale officer, NPA and asset manager, Head of NPA | E3 | Loading; list |
| SCR-22 | Assets | Asset record | One asset: title, condition, photographs, valuations, costs, listing and sale history | Asset list; case record | S5 | Asset and disposal | Sale officer, NPA and asset manager | E3 | Take-on; held; listed; sold |
| SCR-23 | Assets | Listing and price | List price, floor and the price ladder for an asset | Asset record | S5 | Asset and disposal | Sale officer | E3 | Draft; below limit; approved; published |
| SCR-24 | Assets | Auction rounds | Auction rounds, bids and results for an asset | Asset record | S5 | Asset and disposal | Sale officer, auction vendor | E4 | Scheduled; open; result; settled |
| SCR-25 | Debt sale | Lot builder | Select accounts, build lots, set the reserve and send for approval | Menu | S6 | Debt sale | Debt sale officer, Head of Asset Liquidity | E5 | Draft; priced; approved |
| SCR-26 | Debt sale | Award | Bids against the reserve and the award decision | Lot builder | S6 | Debt sale | Debt sale officer, Head of Asset Liquidity | E6 | Open; closed; awarded; transferred |
| SCR-27 | Write-off | Write-off proposal | The monthly population, the pack per case and removals with reasons | Menu | S7 | Write-off and posting | Write-off team member | E6 | Scan; proposed; in committee; approved |
| SCR-28 | Money | Proceeds matching | Receipts matched to cases and the unmatched list | Menu | P8 | Write-off and posting | Credit Administration officer | E2 skeleton; E4 full | Loading; matched; unmatched |
| SCR-29 | Money | Posting | Approved bookings and postings with the confirmation from the next load | Menu | P8 | Write-off and posting | Credit Administration officer | E4 | Pending; confirmed; missing |
| SCR-30 | Documents | Case documents | Documents on a case by type, with the extracted fields and versions | Case record | P5 | Documents | Every bank role in scope | E1 | Loading; list; upload |
| SCR-31 | Documents | Document review queue | Low-confidence extractions to check and correct | Menu | P5 | Documents | Document services, case owner | E1 | Loading; list; reviewed |
| SCR-32 | Documents | Document custody | Originals out, their holder and their due-back date | Menu; case documents | P5 | Documents | Document services, legal counsel | E2 | Out; overdue; returned |
| SCR-33 | Documents | Template approval | Letter and notice templates and their approval | Menu | P6 | Documents | Legal counsel | E2 | Draft; approved; withdrawn |
| SCR-34 | Partners | Partner list | Partners, contracts, panel status and scorecards | Menu | S9 | Partner portal | Partner and agency manager | E2 identities; E6 full | Loading; list |
| SCR-35 | Partners | Placement and allocation | Work placed with partners by rule, with recalls and re-selection | Partner list | S9 | Partner portal | Partner and agency manager | E6 | Loading; list |
| SCR-36 | Partners | Partner scorecard | Monthly score per partner against its measures | Partner list | S9 | Partner portal | Partner and agency manager, Head of Litigation | E7 | Loading; scored |
| SCR-37 | Reports | Steering dashboard | Inflow, stock, cures, recovery, turnaround and cost, by product and route | Menu | P9 | Reporting | Product heads, sponsors, team managers | E2 | Loading; filtered |
| SCR-38 | Reports | Decision log query | Search the decision log by case, rule, approver and date, with export | Menu | P7 | Decision log | Internal audit, Risk, center of excellence | E2 | Loading; results; export |
| SCR-39 | Administration | Rules and parameters | Rule versions, route sets, thresholds and timers, with the load and approval | Menu | P4 | Rules and parameters | Center of excellence analyst, reference data administrator, Risk | E8; by file load before | Versions; load; approval |
| SCR-40 | Administration | Reference data | Lists of values and reference tables with versions | Menu | P4 | Reference data | Reference data administrator | E8; by file load before | Versions; load |
| SCR-41 | Administration | Delegation of authority | Approval levels, holders, limits and substitutes | Menu | P4 | Rules and parameters | Reference data administrator, Risk | E8; by file load before | Versions; load; approval |
| SCR-42 | Administration | Queues and service levels | Queues, caps, overflow and service levels per state | Menu | P4 | Queue and allocation | Reference data administrator, team manager | E8; by file load before | Versions; load |
| SCR-43 | Administration | Roles and access | Roles, permissions, scope and the group mapping, with the access log | Menu | P4 | Platform administration | Security administrator, application owner | E8; by file load before | List; access log |
| SCR-44 | Administration | Interface and job monitor | Loads, files, jobs and outbound actions with status and reruns | Menu | P1 | Platform administration | Platform administrator, data steward | E2; E8 full | Running; failed; complete |
| SCR-45 | Administration | Data quality | Load check results, reconciliation breaks and stale data products | Menu | P1 | Platform administration | Data steward and data product owner | E2; E8 full | Loading; breaks |
| SCR-46 | Administration | Agent monitor | Agent runs, fallbacks, evaluation results and autonomy levels | Menu | P10 | Platform administration | Risk and model risk officer, center of excellence analyst | E2; E8 full | Shadow; live; paused |
| SCR-47 | Administration | Personal data | Retention classes, masking rules, consent log and data subject requests | Menu | P4 | Platform administration | Compliance and PDPA officer | E8; by file load before | Loading; list |
| PRT-01 | Partner portal | Partner home | The partner's open instructions, due dates and messages | Partner sign-in | S9 | Partner portal | All partner users | E2 | Loading; list |
| PRT-02 | Partner portal | Instruction | One instruction with its documents, due dates and the result to record | Partner home | S9 | Partner portal | Law firm, valuer, collection agency | E4 | New; accepted; in progress; result; closed |
| PRT-03 | Partner portal | Upload result | Record a result and upload its documents | Instruction | S9 | Partner portal | Law firm, valuer, auction vendor, collection agency | E4 | Form; saved |
| PRT-04 | Partner portal | Invoice | Submit a fee invoice against completed instructions | Instruction | S9 | Partner portal | Law firm, valuer, auction vendor, collection agency | E6 | Draft; submitted; approved; paid |
| PRT-05 | Partner portal | Data room | Lot data tapes and documents for admitted buyers, with bids | Partner home | S6 | Partner portal | Debt buyer and AMC | E5 | Admitted; bidding; closed |
| PRT-06 | Partner portal | Transfer confirmation | Confirm a transfer of assets or accounts | Partner home | S5 | Partner portal | RAMC user, debt buyer | E4 | Pending; confirmed |

## Navigation

| Menu structure |  |
|---|---|
| The menus in the order they appear, and the screens under each. The menu shows only the items a role may open. |  |
| Menu | Screens |
| Home | My work |
| Cases | Case list, Case record, Case timeline, Transfer case, Raise deviation |
| Queues | Team queues, Deviation queue, Exception queue |
| Approvals | Approval queue, Decision screen, Committee pack |
| Treatment | Route decision, Treatment record, Settlement offer, Deed in lieu, Guarantee claim |
| Litigation | Notice approval, Litigation workspace, Enforcement workspace |
| Assets | Asset list, Asset record, Listing and price, Auction rounds |
| Debt sale | Lot builder, Award |
| Write-off | Write-off proposal |
| Money | Proceeds matching, Posting |
| Documents | Case documents, Document review queue, Document custody, Template approval |
| Partners | Partner list, Placement and allocation, Partner scorecard |
| Reports | Steering dashboard, Decision log query |
| Administration | Rules and parameters, Reference data, Delegation of authority, Queues and service levels, Roles and access, Interface and job monitor, Data quality, Agent monitor, Personal data |
| Partner portal | Partner home, Instruction, Upload result, Invoice, Data room, Transfer confirmation |

## Role to screen

| Screens each role can open |  |  |  |  |
|---|---|---|---|---|
| Derived from the permission matrix: a role opens a screen when it holds a right in the screen's capability area. Scope still limits the records shown. |  |  |  |  |
| Role code | Role name | Screen ID | Screen | Capability area |
| RW-CASEOWN | Case owner | SCR-01 | My work | Case record |
| RW-CASEOWN | Case owner | SCR-02 | Case list | Case record |
| RW-CASEOWN | Case owner | SCR-03 | Case record | Case record |
| RW-CASEOWN | Case owner | SCR-04 | Case timeline | Case record |
| RW-CASEOWN | Case owner | SCR-05 | Transfer case | Queue and allocation |
| RW-CASEOWN | Case owner | SCR-06 | Raise deviation | Case record |
| RW-CASEOWN | Case owner | SCR-07 | Team queues | Queue and allocation |
| RW-CASEOWN | Case owner | SCR-08 | Deviation queue | Case record |
| RW-CASEOWN | Case owner | SCR-09 | Exception queue | Queue and allocation |
| RW-CASEOWN | Case owner | SCR-10 | Approval queue | Decision log |
| RW-CASEOWN | Case owner | SCR-11 | Decision screen | Decision log |
| RW-CASEOWN | Case owner | SCR-12 | Committee pack | Decision log |
| RW-CASEOWN | Case owner | SCR-13 | Route decision | Treatment and offer |
| RW-CASEOWN | Case owner | SCR-14 | Treatment record | Treatment and offer |
| RW-CASEOWN | Case owner | SCR-15 | Settlement offer | Treatment and offer |
| RW-CASEOWN | Case owner | SCR-16 | Deed in lieu | Treatment and offer |
| RW-CASEOWN | Case owner | SCR-17 | Guarantee claim | Treatment and offer |
| RW-CASEOWN | Case owner | SCR-18 | Notice approval | Litigation |
| RW-CASEOWN | Case owner | SCR-19 | Litigation workspace | Litigation |
| RW-CASEOWN | Case owner | SCR-20 | Enforcement workspace | Litigation |
| RW-CASEOWN | Case owner | SCR-21 | Asset list | Asset and disposal |
| RW-CASEOWN | Case owner | SCR-22 | Asset record | Asset and disposal |
| RW-CASEOWN | Case owner | SCR-23 | Listing and price | Asset and disposal |
| RW-CASEOWN | Case owner | SCR-24 | Auction rounds | Asset and disposal |
| RW-CASEOWN | Case owner | SCR-30 | Case documents | Documents |
| RW-CASEOWN | Case owner | SCR-31 | Document review queue | Documents |
| RW-CASEOWN | Case owner | SCR-32 | Document custody | Documents |
| RW-CASEOWN | Case owner | SCR-33 | Template approval | Documents |
| RW-CASEOWN | Case owner | SCR-34 | Partner list | Partner portal |
| RW-CASEOWN | Case owner | SCR-35 | Placement and allocation | Partner portal |
| RW-CASEOWN | Case owner | SCR-36 | Partner scorecard | Partner portal |
| RW-CASEOWN | Case owner | SCR-37 | Steering dashboard | Reporting |
| RW-CASEOWN | Case owner | SCR-38 | Decision log query | Decision log |
| RW-CASEOWN | Case owner | SCR-39 | Rules and parameters | Rules and parameters |
| RW-CASEOWN | Case owner | SCR-40 | Reference data | Reference data |
| RW-CASEOWN | Case owner | SCR-41 | Delegation of authority | Rules and parameters |
| RW-CASEOWN | Case owner | SCR-42 | Queues and service levels | Queue and allocation |
| RW-TEAMMGR | Team manager | SCR-01 | My work | Case record |
| RW-TEAMMGR | Team manager | SCR-02 | Case list | Case record |
| RW-TEAMMGR | Team manager | SCR-03 | Case record | Case record |
| RW-TEAMMGR | Team manager | SCR-04 | Case timeline | Case record |
| RW-TEAMMGR | Team manager | SCR-05 | Transfer case | Queue and allocation |
| RW-TEAMMGR | Team manager | SCR-06 | Raise deviation | Case record |
| RW-TEAMMGR | Team manager | SCR-07 | Team queues | Queue and allocation |
| RW-TEAMMGR | Team manager | SCR-08 | Deviation queue | Case record |
| RW-TEAMMGR | Team manager | SCR-09 | Exception queue | Queue and allocation |
| RW-TEAMMGR | Team manager | SCR-10 | Approval queue | Decision log |
| RW-TEAMMGR | Team manager | SCR-11 | Decision screen | Decision log |
| RW-TEAMMGR | Team manager | SCR-12 | Committee pack | Decision log |
| RW-TEAMMGR | Team manager | SCR-13 | Route decision | Treatment and offer |
| RW-TEAMMGR | Team manager | SCR-14 | Treatment record | Treatment and offer |
| RW-TEAMMGR | Team manager | SCR-15 | Settlement offer | Treatment and offer |
| RW-TEAMMGR | Team manager | SCR-16 | Deed in lieu | Treatment and offer |
| RW-TEAMMGR | Team manager | SCR-17 | Guarantee claim | Treatment and offer |
| RW-TEAMMGR | Team manager | SCR-18 | Notice approval | Litigation |
| RW-TEAMMGR | Team manager | SCR-19 | Litigation workspace | Litigation |
| RW-TEAMMGR | Team manager | SCR-20 | Enforcement workspace | Litigation |
| RW-TEAMMGR | Team manager | SCR-21 | Asset list | Asset and disposal |
| RW-TEAMMGR | Team manager | SCR-22 | Asset record | Asset and disposal |
| RW-TEAMMGR | Team manager | SCR-23 | Listing and price | Asset and disposal |
| RW-TEAMMGR | Team manager | SCR-24 | Auction rounds | Asset and disposal |
| RW-TEAMMGR | Team manager | SCR-30 | Case documents | Documents |
| RW-TEAMMGR | Team manager | SCR-31 | Document review queue | Documents |
| RW-TEAMMGR | Team manager | SCR-32 | Document custody | Documents |
| RW-TEAMMGR | Team manager | SCR-33 | Template approval | Documents |
| RW-TEAMMGR | Team manager | SCR-34 | Partner list | Partner portal |
| RW-TEAMMGR | Team manager | SCR-35 | Placement and allocation | Partner portal |
| RW-TEAMMGR | Team manager | SCR-36 | Partner scorecard | Partner portal |
| RW-TEAMMGR | Team manager | SCR-37 | Steering dashboard | Reporting |
| RW-TEAMMGR | Team manager | SCR-38 | Decision log query | Decision log |
| RW-TEAMMGR | Team manager | SCR-39 | Rules and parameters | Rules and parameters |
| RW-TEAMMGR | Team manager | SCR-40 | Reference data | Reference data |
| RW-TEAMMGR | Team manager | SCR-41 | Delegation of authority | Rules and parameters |
| RW-TEAMMGR | Team manager | SCR-42 | Queues and service levels | Queue and allocation |
| RW-PHONECOL | Phone collector | SCR-01 | My work | Case record |
| RW-PHONECOL | Phone collector | SCR-02 | Case list | Case record |
| RW-PHONECOL | Phone collector | SCR-03 | Case record | Case record |
| RW-PHONECOL | Phone collector | SCR-04 | Case timeline | Case record |
| RW-PHONECOL | Phone collector | SCR-05 | Transfer case | Queue and allocation |
| RW-PHONECOL | Phone collector | SCR-06 | Raise deviation | Case record |
| RW-PHONECOL | Phone collector | SCR-07 | Team queues | Queue and allocation |
| RW-PHONECOL | Phone collector | SCR-08 | Deviation queue | Case record |
| RW-PHONECOL | Phone collector | SCR-09 | Exception queue | Queue and allocation |
| RW-PHONECOL | Phone collector | SCR-30 | Case documents | Documents |
| RW-PHONECOL | Phone collector | SCR-31 | Document review queue | Documents |
| RW-PHONECOL | Phone collector | SCR-32 | Document custody | Documents |
| RW-PHONECOL | Phone collector | SCR-33 | Template approval | Documents |
| RW-PHONECOL | Phone collector | SCR-37 | Steering dashboard | Reporting |
| RW-PHONECOL | Phone collector | SCR-40 | Reference data | Reference data |
| RW-PHONECOL | Phone collector | SCR-42 | Queues and service levels | Queue and allocation |
| RW-FIELDCOL | Field collector | SCR-01 | My work | Case record |
| RW-FIELDCOL | Field collector | SCR-02 | Case list | Case record |
| RW-FIELDCOL | Field collector | SCR-03 | Case record | Case record |
| RW-FIELDCOL | Field collector | SCR-04 | Case timeline | Case record |
| RW-FIELDCOL | Field collector | SCR-05 | Transfer case | Queue and allocation |
| RW-FIELDCOL | Field collector | SCR-06 | Raise deviation | Case record |
| RW-FIELDCOL | Field collector | SCR-07 | Team queues | Queue and allocation |
| RW-FIELDCOL | Field collector | SCR-08 | Deviation queue | Case record |
| RW-FIELDCOL | Field collector | SCR-09 | Exception queue | Queue and allocation |
| RW-FIELDCOL | Field collector | SCR-21 | Asset list | Asset and disposal |
| RW-FIELDCOL | Field collector | SCR-22 | Asset record | Asset and disposal |
| RW-FIELDCOL | Field collector | SCR-23 | Listing and price | Asset and disposal |
| RW-FIELDCOL | Field collector | SCR-24 | Auction rounds | Asset and disposal |
| RW-FIELDCOL | Field collector | SCR-30 | Case documents | Documents |
| RW-FIELDCOL | Field collector | SCR-31 | Document review queue | Documents |
| RW-FIELDCOL | Field collector | SCR-32 | Document custody | Documents |
| RW-FIELDCOL | Field collector | SCR-33 | Template approval | Documents |
| RW-FIELDCOL | Field collector | SCR-40 | Reference data | Reference data |
| RW-FIELDCOL | Field collector | SCR-42 | Queues and service levels | Queue and allocation |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-01 | My work | Case record |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-02 | Case list | Case record |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-03 | Case record | Case record |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-04 | Case timeline | Case record |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-05 | Transfer case | Queue and allocation |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-06 | Raise deviation | Case record |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-07 | Team queues | Queue and allocation |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-08 | Deviation queue | Case record |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-09 | Exception queue | Queue and allocation |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-10 | Approval queue | Decision log |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-11 | Decision screen | Decision log |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-12 | Committee pack | Decision log |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-13 | Route decision | Treatment and offer |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-14 | Treatment record | Treatment and offer |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-15 | Settlement offer | Treatment and offer |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-16 | Deed in lieu | Treatment and offer |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-17 | Guarantee claim | Treatment and offer |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-30 | Case documents | Documents |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-31 | Document review queue | Documents |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-32 | Document custody | Documents |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-33 | Template approval | Documents |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-37 | Steering dashboard | Reporting |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-38 | Decision log query | Decision log |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-39 | Rules and parameters | Rules and parameters |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-40 | Reference data | Reference data |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-41 | Delegation of authority | Rules and parameters |
| RW-RESTRUCT | Restructuring officer (FCR) | SCR-42 | Queues and service levels | Queue and allocation |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-01 | My work | Case record |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-02 | Case list | Case record |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-03 | Case record | Case record |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-04 | Case timeline | Case record |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-05 | Transfer case | Queue and allocation |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-06 | Raise deviation | Case record |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-07 | Team queues | Queue and allocation |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-08 | Deviation queue | Case record |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-09 | Exception queue | Queue and allocation |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-10 | Approval queue | Decision log |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-11 | Decision screen | Decision log |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-12 | Committee pack | Decision log |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-13 | Route decision | Treatment and offer |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-14 | Treatment record | Treatment and offer |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-15 | Settlement offer | Treatment and offer |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-16 | Deed in lieu | Treatment and offer |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-17 | Guarantee claim | Treatment and offer |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-30 | Case documents | Documents |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-31 | Document review queue | Documents |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-32 | Document custody | Documents |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-33 | Template approval | Documents |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-37 | Steering dashboard | Reporting |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-38 | Decision log query | Decision log |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-39 | Rules and parameters | Rules and parameters |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-40 | Reference data | Reference data |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-41 | Delegation of authority | Rules and parameters |
| RW-SPECIAL | Hardship and vulnerability specialist | SCR-42 | Queues and service levels | Queue and allocation |
| RW-COMPLAIN | Complaint officer | SCR-01 | My work | Case record |
| RW-COMPLAIN | Complaint officer | SCR-02 | Case list | Case record |
| RW-COMPLAIN | Complaint officer | SCR-03 | Case record | Case record |
| RW-COMPLAIN | Complaint officer | SCR-04 | Case timeline | Case record |
| RW-COMPLAIN | Complaint officer | SCR-05 | Transfer case | Queue and allocation |
| RW-COMPLAIN | Complaint officer | SCR-06 | Raise deviation | Case record |
| RW-COMPLAIN | Complaint officer | SCR-07 | Team queues | Queue and allocation |
| RW-COMPLAIN | Complaint officer | SCR-08 | Deviation queue | Case record |
| RW-COMPLAIN | Complaint officer | SCR-09 | Exception queue | Queue and allocation |
| RW-COMPLAIN | Complaint officer | SCR-10 | Approval queue | Decision log |
| RW-COMPLAIN | Complaint officer | SCR-11 | Decision screen | Decision log |
| RW-COMPLAIN | Complaint officer | SCR-12 | Committee pack | Decision log |
| RW-COMPLAIN | Complaint officer | SCR-13 | Route decision | Treatment and offer |
| RW-COMPLAIN | Complaint officer | SCR-14 | Treatment record | Treatment and offer |
| RW-COMPLAIN | Complaint officer | SCR-15 | Settlement offer | Treatment and offer |
| RW-COMPLAIN | Complaint officer | SCR-16 | Deed in lieu | Treatment and offer |
| RW-COMPLAIN | Complaint officer | SCR-17 | Guarantee claim | Treatment and offer |
| RW-COMPLAIN | Complaint officer | SCR-18 | Notice approval | Litigation |
| RW-COMPLAIN | Complaint officer | SCR-19 | Litigation workspace | Litigation |
| RW-COMPLAIN | Complaint officer | SCR-20 | Enforcement workspace | Litigation |
| RW-COMPLAIN | Complaint officer | SCR-21 | Asset list | Asset and disposal |
| RW-COMPLAIN | Complaint officer | SCR-22 | Asset record | Asset and disposal |
| RW-COMPLAIN | Complaint officer | SCR-23 | Listing and price | Asset and disposal |
| RW-COMPLAIN | Complaint officer | SCR-24 | Auction rounds | Asset and disposal |
| RW-COMPLAIN | Complaint officer | SCR-30 | Case documents | Documents |
| RW-COMPLAIN | Complaint officer | SCR-31 | Document review queue | Documents |
| RW-COMPLAIN | Complaint officer | SCR-32 | Document custody | Documents |
| RW-COMPLAIN | Complaint officer | SCR-33 | Template approval | Documents |
| RW-COMPLAIN | Complaint officer | SCR-37 | Steering dashboard | Reporting |
| RW-COMPLAIN | Complaint officer | SCR-38 | Decision log query | Decision log |
| RW-COMPLAIN | Complaint officer | SCR-39 | Rules and parameters | Rules and parameters |
| RW-COMPLAIN | Complaint officer | SCR-40 | Reference data | Reference data |
| RW-COMPLAIN | Complaint officer | SCR-41 | Delegation of authority | Rules and parameters |
| RW-COMPLAIN | Complaint officer | SCR-42 | Queues and service levels | Queue and allocation |
| RW-FRAUD | Fraud investigator | SCR-01 | My work | Case record |
| RW-FRAUD | Fraud investigator | SCR-02 | Case list | Case record |
| RW-FRAUD | Fraud investigator | SCR-03 | Case record | Case record |
| RW-FRAUD | Fraud investigator | SCR-04 | Case timeline | Case record |
| RW-FRAUD | Fraud investigator | SCR-05 | Transfer case | Queue and allocation |
| RW-FRAUD | Fraud investigator | SCR-06 | Raise deviation | Case record |
| RW-FRAUD | Fraud investigator | SCR-07 | Team queues | Queue and allocation |
| RW-FRAUD | Fraud investigator | SCR-08 | Deviation queue | Case record |
| RW-FRAUD | Fraud investigator | SCR-09 | Exception queue | Queue and allocation |
| RW-FRAUD | Fraud investigator | SCR-10 | Approval queue | Decision log |
| RW-FRAUD | Fraud investigator | SCR-11 | Decision screen | Decision log |
| RW-FRAUD | Fraud investigator | SCR-12 | Committee pack | Decision log |
| RW-FRAUD | Fraud investigator | SCR-13 | Route decision | Treatment and offer |
| RW-FRAUD | Fraud investigator | SCR-14 | Treatment record | Treatment and offer |
| RW-FRAUD | Fraud investigator | SCR-15 | Settlement offer | Treatment and offer |
| RW-FRAUD | Fraud investigator | SCR-16 | Deed in lieu | Treatment and offer |
| RW-FRAUD | Fraud investigator | SCR-17 | Guarantee claim | Treatment and offer |
| RW-FRAUD | Fraud investigator | SCR-18 | Notice approval | Litigation |
| RW-FRAUD | Fraud investigator | SCR-19 | Litigation workspace | Litigation |
| RW-FRAUD | Fraud investigator | SCR-20 | Enforcement workspace | Litigation |
| RW-FRAUD | Fraud investigator | SCR-27 | Write-off proposal | Write-off and posting |
| RW-FRAUD | Fraud investigator | SCR-28 | Proceeds matching | Write-off and posting |
| RW-FRAUD | Fraud investigator | SCR-29 | Posting | Write-off and posting |
| RW-FRAUD | Fraud investigator | SCR-30 | Case documents | Documents |
| RW-FRAUD | Fraud investigator | SCR-31 | Document review queue | Documents |
| RW-FRAUD | Fraud investigator | SCR-32 | Document custody | Documents |
| RW-FRAUD | Fraud investigator | SCR-33 | Template approval | Documents |
| RW-FRAUD | Fraud investigator | SCR-37 | Steering dashboard | Reporting |
| RW-FRAUD | Fraud investigator | SCR-38 | Decision log query | Decision log |
| RW-FRAUD | Fraud investigator | SCR-39 | Rules and parameters | Rules and parameters |
| RW-FRAUD | Fraud investigator | SCR-40 | Reference data | Reference data |
| RW-FRAUD | Fraud investigator | SCR-41 | Delegation of authority | Rules and parameters |
| RW-FRAUD | Fraud investigator | SCR-42 | Queues and service levels | Queue and allocation |
| RW-LITOFF | Litigation officer | SCR-01 | My work | Case record |
| RW-LITOFF | Litigation officer | SCR-02 | Case list | Case record |
| RW-LITOFF | Litigation officer | SCR-03 | Case record | Case record |
| RW-LITOFF | Litigation officer | SCR-04 | Case timeline | Case record |
| RW-LITOFF | Litigation officer | SCR-05 | Transfer case | Queue and allocation |
| RW-LITOFF | Litigation officer | SCR-06 | Raise deviation | Case record |
| RW-LITOFF | Litigation officer | SCR-07 | Team queues | Queue and allocation |
| RW-LITOFF | Litigation officer | SCR-08 | Deviation queue | Case record |
| RW-LITOFF | Litigation officer | SCR-09 | Exception queue | Queue and allocation |
| RW-LITOFF | Litigation officer | SCR-10 | Approval queue | Decision log |
| RW-LITOFF | Litigation officer | SCR-11 | Decision screen | Decision log |
| RW-LITOFF | Litigation officer | SCR-12 | Committee pack | Decision log |
| RW-LITOFF | Litigation officer | SCR-13 | Route decision | Treatment and offer |
| RW-LITOFF | Litigation officer | SCR-14 | Treatment record | Treatment and offer |
| RW-LITOFF | Litigation officer | SCR-15 | Settlement offer | Treatment and offer |
| RW-LITOFF | Litigation officer | SCR-16 | Deed in lieu | Treatment and offer |
| RW-LITOFF | Litigation officer | SCR-17 | Guarantee claim | Treatment and offer |
| RW-LITOFF | Litigation officer | SCR-18 | Notice approval | Litigation |
| RW-LITOFF | Litigation officer | SCR-19 | Litigation workspace | Litigation |
| RW-LITOFF | Litigation officer | SCR-20 | Enforcement workspace | Litigation |
| RW-LITOFF | Litigation officer | SCR-21 | Asset list | Asset and disposal |
| RW-LITOFF | Litigation officer | SCR-22 | Asset record | Asset and disposal |
| RW-LITOFF | Litigation officer | SCR-23 | Listing and price | Asset and disposal |
| RW-LITOFF | Litigation officer | SCR-24 | Auction rounds | Asset and disposal |
| RW-LITOFF | Litigation officer | SCR-30 | Case documents | Documents |
| RW-LITOFF | Litigation officer | SCR-31 | Document review queue | Documents |
| RW-LITOFF | Litigation officer | SCR-32 | Document custody | Documents |
| RW-LITOFF | Litigation officer | SCR-33 | Template approval | Documents |
| RW-LITOFF | Litigation officer | SCR-34 | Partner list | Partner portal |
| RW-LITOFF | Litigation officer | SCR-35 | Placement and allocation | Partner portal |
| RW-LITOFF | Litigation officer | SCR-36 | Partner scorecard | Partner portal |
| RW-LITOFF | Litigation officer | SCR-37 | Steering dashboard | Reporting |
| RW-LITOFF | Litigation officer | SCR-38 | Decision log query | Decision log |
| RW-LITOFF | Litigation officer | SCR-39 | Rules and parameters | Rules and parameters |
| RW-LITOFF | Litigation officer | SCR-40 | Reference data | Reference data |
| RW-LITOFF | Litigation officer | SCR-41 | Delegation of authority | Rules and parameters |
| RW-LITOFF | Litigation officer | SCR-42 | Queues and service levels | Queue and allocation |
| RW-ENFORCE | Enforcement owner | SCR-01 | My work | Case record |
| RW-ENFORCE | Enforcement owner | SCR-02 | Case list | Case record |
| RW-ENFORCE | Enforcement owner | SCR-03 | Case record | Case record |
| RW-ENFORCE | Enforcement owner | SCR-04 | Case timeline | Case record |
| RW-ENFORCE | Enforcement owner | SCR-05 | Transfer case | Queue and allocation |
| RW-ENFORCE | Enforcement owner | SCR-06 | Raise deviation | Case record |
| RW-ENFORCE | Enforcement owner | SCR-07 | Team queues | Queue and allocation |
| RW-ENFORCE | Enforcement owner | SCR-08 | Deviation queue | Case record |
| RW-ENFORCE | Enforcement owner | SCR-09 | Exception queue | Queue and allocation |
| RW-ENFORCE | Enforcement owner | SCR-10 | Approval queue | Decision log |
| RW-ENFORCE | Enforcement owner | SCR-11 | Decision screen | Decision log |
| RW-ENFORCE | Enforcement owner | SCR-12 | Committee pack | Decision log |
| RW-ENFORCE | Enforcement owner | SCR-18 | Notice approval | Litigation |
| RW-ENFORCE | Enforcement owner | SCR-19 | Litigation workspace | Litigation |
| RW-ENFORCE | Enforcement owner | SCR-20 | Enforcement workspace | Litigation |
| RW-ENFORCE | Enforcement owner | SCR-21 | Asset list | Asset and disposal |
| RW-ENFORCE | Enforcement owner | SCR-22 | Asset record | Asset and disposal |
| RW-ENFORCE | Enforcement owner | SCR-23 | Listing and price | Asset and disposal |
| RW-ENFORCE | Enforcement owner | SCR-24 | Auction rounds | Asset and disposal |
| RW-ENFORCE | Enforcement owner | SCR-30 | Case documents | Documents |
| RW-ENFORCE | Enforcement owner | SCR-31 | Document review queue | Documents |
| RW-ENFORCE | Enforcement owner | SCR-32 | Document custody | Documents |
| RW-ENFORCE | Enforcement owner | SCR-33 | Template approval | Documents |
| RW-ENFORCE | Enforcement owner | SCR-34 | Partner list | Partner portal |
| RW-ENFORCE | Enforcement owner | SCR-35 | Placement and allocation | Partner portal |
| RW-ENFORCE | Enforcement owner | SCR-36 | Partner scorecard | Partner portal |
| RW-ENFORCE | Enforcement owner | SCR-37 | Steering dashboard | Reporting |
| RW-ENFORCE | Enforcement owner | SCR-38 | Decision log query | Decision log |
| RW-ENFORCE | Enforcement owner | SCR-39 | Rules and parameters | Rules and parameters |
| RW-ENFORCE | Enforcement owner | SCR-40 | Reference data | Reference data |
| RW-ENFORCE | Enforcement owner | SCR-41 | Delegation of authority | Rules and parameters |
| RW-ENFORCE | Enforcement owner | SCR-42 | Queues and service levels | Queue and allocation |
| RW-LEGAL | Legal counsel | SCR-01 | My work | Case record |
| RW-LEGAL | Legal counsel | SCR-02 | Case list | Case record |
| RW-LEGAL | Legal counsel | SCR-03 | Case record | Case record |
| RW-LEGAL | Legal counsel | SCR-04 | Case timeline | Case record |
| RW-LEGAL | Legal counsel | SCR-06 | Raise deviation | Case record |
| RW-LEGAL | Legal counsel | SCR-08 | Deviation queue | Case record |
| RW-LEGAL | Legal counsel | SCR-10 | Approval queue | Decision log |
| RW-LEGAL | Legal counsel | SCR-11 | Decision screen | Decision log |
| RW-LEGAL | Legal counsel | SCR-12 | Committee pack | Decision log |
| RW-LEGAL | Legal counsel | SCR-13 | Route decision | Treatment and offer |
| RW-LEGAL | Legal counsel | SCR-14 | Treatment record | Treatment and offer |
| RW-LEGAL | Legal counsel | SCR-15 | Settlement offer | Treatment and offer |
| RW-LEGAL | Legal counsel | SCR-16 | Deed in lieu | Treatment and offer |
| RW-LEGAL | Legal counsel | SCR-17 | Guarantee claim | Treatment and offer |
| RW-LEGAL | Legal counsel | SCR-18 | Notice approval | Litigation |
| RW-LEGAL | Legal counsel | SCR-19 | Litigation workspace | Litigation |
| RW-LEGAL | Legal counsel | SCR-20 | Enforcement workspace | Litigation |
| RW-LEGAL | Legal counsel | SCR-21 | Asset list | Asset and disposal |
| RW-LEGAL | Legal counsel | SCR-22 | Asset record | Asset and disposal |
| RW-LEGAL | Legal counsel | SCR-23 | Listing and price | Asset and disposal |
| RW-LEGAL | Legal counsel | SCR-24 | Auction rounds | Asset and disposal |
| RW-LEGAL | Legal counsel | SCR-30 | Case documents | Documents |
| RW-LEGAL | Legal counsel | SCR-31 | Document review queue | Documents |
| RW-LEGAL | Legal counsel | SCR-32 | Document custody | Documents |
| RW-LEGAL | Legal counsel | SCR-33 | Template approval | Documents |
| RW-LEGAL | Legal counsel | SCR-34 | Partner list | Partner portal |
| RW-LEGAL | Legal counsel | SCR-35 | Placement and allocation | Partner portal |
| RW-LEGAL | Legal counsel | SCR-36 | Partner scorecard | Partner portal |
| RW-LEGAL | Legal counsel | SCR-37 | Steering dashboard | Reporting |
| RW-LEGAL | Legal counsel | SCR-38 | Decision log query | Decision log |
| RW-LEGAL | Legal counsel | SCR-39 | Rules and parameters | Rules and parameters |
| RW-LEGAL | Legal counsel | SCR-40 | Reference data | Reference data |
| RW-LEGAL | Legal counsel | SCR-41 | Delegation of authority | Rules and parameters |
| RW-SALEOFF | Sale officer | SCR-01 | My work | Case record |
| RW-SALEOFF | Sale officer | SCR-02 | Case list | Case record |
| RW-SALEOFF | Sale officer | SCR-03 | Case record | Case record |
| RW-SALEOFF | Sale officer | SCR-04 | Case timeline | Case record |
| RW-SALEOFF | Sale officer | SCR-05 | Transfer case | Queue and allocation |
| RW-SALEOFF | Sale officer | SCR-06 | Raise deviation | Case record |
| RW-SALEOFF | Sale officer | SCR-07 | Team queues | Queue and allocation |
| RW-SALEOFF | Sale officer | SCR-08 | Deviation queue | Case record |
| RW-SALEOFF | Sale officer | SCR-09 | Exception queue | Queue and allocation |
| RW-SALEOFF | Sale officer | SCR-10 | Approval queue | Decision log |
| RW-SALEOFF | Sale officer | SCR-11 | Decision screen | Decision log |
| RW-SALEOFF | Sale officer | SCR-12 | Committee pack | Decision log |
| RW-SALEOFF | Sale officer | SCR-18 | Notice approval | Litigation |
| RW-SALEOFF | Sale officer | SCR-19 | Litigation workspace | Litigation |
| RW-SALEOFF | Sale officer | SCR-20 | Enforcement workspace | Litigation |
| RW-SALEOFF | Sale officer | SCR-21 | Asset list | Asset and disposal |
| RW-SALEOFF | Sale officer | SCR-22 | Asset record | Asset and disposal |
| RW-SALEOFF | Sale officer | SCR-23 | Listing and price | Asset and disposal |
| RW-SALEOFF | Sale officer | SCR-24 | Auction rounds | Asset and disposal |
| RW-SALEOFF | Sale officer | SCR-25 | Lot builder | Debt sale |
| RW-SALEOFF | Sale officer | SCR-26 | Award | Debt sale |
| RW-SALEOFF | Sale officer | SCR-30 | Case documents | Documents |
| RW-SALEOFF | Sale officer | SCR-31 | Document review queue | Documents |
| RW-SALEOFF | Sale officer | SCR-32 | Document custody | Documents |
| RW-SALEOFF | Sale officer | SCR-33 | Template approval | Documents |
| RW-SALEOFF | Sale officer | SCR-34 | Partner list | Partner portal |
| RW-SALEOFF | Sale officer | SCR-35 | Placement and allocation | Partner portal |
| RW-SALEOFF | Sale officer | SCR-36 | Partner scorecard | Partner portal |
| RW-SALEOFF | Sale officer | SCR-37 | Steering dashboard | Reporting |
| RW-SALEOFF | Sale officer | SCR-38 | Decision log query | Decision log |
| RW-SALEOFF | Sale officer | SCR-39 | Rules and parameters | Rules and parameters |
| RW-SALEOFF | Sale officer | SCR-40 | Reference data | Reference data |
| RW-SALEOFF | Sale officer | SCR-41 | Delegation of authority | Rules and parameters |
| RW-SALEOFF | Sale officer | SCR-42 | Queues and service levels | Queue and allocation |
| RW-NPAMGR | NPA and asset manager | SCR-01 | My work | Case record |
| RW-NPAMGR | NPA and asset manager | SCR-02 | Case list | Case record |
| RW-NPAMGR | NPA and asset manager | SCR-03 | Case record | Case record |
| RW-NPAMGR | NPA and asset manager | SCR-04 | Case timeline | Case record |
| RW-NPAMGR | NPA and asset manager | SCR-06 | Raise deviation | Case record |
| RW-NPAMGR | NPA and asset manager | SCR-08 | Deviation queue | Case record |
| RW-NPAMGR | NPA and asset manager | SCR-10 | Approval queue | Decision log |
| RW-NPAMGR | NPA and asset manager | SCR-11 | Decision screen | Decision log |
| RW-NPAMGR | NPA and asset manager | SCR-12 | Committee pack | Decision log |
| RW-NPAMGR | NPA and asset manager | SCR-18 | Notice approval | Litigation |
| RW-NPAMGR | NPA and asset manager | SCR-19 | Litigation workspace | Litigation |
| RW-NPAMGR | NPA and asset manager | SCR-20 | Enforcement workspace | Litigation |
| RW-NPAMGR | NPA and asset manager | SCR-21 | Asset list | Asset and disposal |
| RW-NPAMGR | NPA and asset manager | SCR-22 | Asset record | Asset and disposal |
| RW-NPAMGR | NPA and asset manager | SCR-23 | Listing and price | Asset and disposal |
| RW-NPAMGR | NPA and asset manager | SCR-24 | Auction rounds | Asset and disposal |
| RW-NPAMGR | NPA and asset manager | SCR-25 | Lot builder | Debt sale |
| RW-NPAMGR | NPA and asset manager | SCR-26 | Award | Debt sale |
| RW-NPAMGR | NPA and asset manager | SCR-30 | Case documents | Documents |
| RW-NPAMGR | NPA and asset manager | SCR-31 | Document review queue | Documents |
| RW-NPAMGR | NPA and asset manager | SCR-32 | Document custody | Documents |
| RW-NPAMGR | NPA and asset manager | SCR-33 | Template approval | Documents |
| RW-NPAMGR | NPA and asset manager | SCR-34 | Partner list | Partner portal |
| RW-NPAMGR | NPA and asset manager | SCR-35 | Placement and allocation | Partner portal |
| RW-NPAMGR | NPA and asset manager | SCR-36 | Partner scorecard | Partner portal |
| RW-NPAMGR | NPA and asset manager | SCR-37 | Steering dashboard | Reporting |
| RW-NPAMGR | NPA and asset manager | SCR-38 | Decision log query | Decision log |
| RW-NPAMGR | NPA and asset manager | SCR-39 | Rules and parameters | Rules and parameters |
| RW-NPAMGR | NPA and asset manager | SCR-40 | Reference data | Reference data |
| RW-NPAMGR | NPA and asset manager | SCR-41 | Delegation of authority | Rules and parameters |
| RW-DEBTSALE | Debt sale officer | SCR-01 | My work | Case record |
| RW-DEBTSALE | Debt sale officer | SCR-02 | Case list | Case record |
| RW-DEBTSALE | Debt sale officer | SCR-03 | Case record | Case record |
| RW-DEBTSALE | Debt sale officer | SCR-04 | Case timeline | Case record |
| RW-DEBTSALE | Debt sale officer | SCR-05 | Transfer case | Queue and allocation |
| RW-DEBTSALE | Debt sale officer | SCR-06 | Raise deviation | Case record |
| RW-DEBTSALE | Debt sale officer | SCR-07 | Team queues | Queue and allocation |
| RW-DEBTSALE | Debt sale officer | SCR-08 | Deviation queue | Case record |
| RW-DEBTSALE | Debt sale officer | SCR-09 | Exception queue | Queue and allocation |
| RW-DEBTSALE | Debt sale officer | SCR-10 | Approval queue | Decision log |
| RW-DEBTSALE | Debt sale officer | SCR-11 | Decision screen | Decision log |
| RW-DEBTSALE | Debt sale officer | SCR-12 | Committee pack | Decision log |
| RW-DEBTSALE | Debt sale officer | SCR-18 | Notice approval | Litigation |
| RW-DEBTSALE | Debt sale officer | SCR-19 | Litigation workspace | Litigation |
| RW-DEBTSALE | Debt sale officer | SCR-20 | Enforcement workspace | Litigation |
| RW-DEBTSALE | Debt sale officer | SCR-21 | Asset list | Asset and disposal |
| RW-DEBTSALE | Debt sale officer | SCR-22 | Asset record | Asset and disposal |
| RW-DEBTSALE | Debt sale officer | SCR-23 | Listing and price | Asset and disposal |
| RW-DEBTSALE | Debt sale officer | SCR-24 | Auction rounds | Asset and disposal |
| RW-DEBTSALE | Debt sale officer | SCR-25 | Lot builder | Debt sale |
| RW-DEBTSALE | Debt sale officer | SCR-26 | Award | Debt sale |
| RW-DEBTSALE | Debt sale officer | SCR-27 | Write-off proposal | Write-off and posting |
| RW-DEBTSALE | Debt sale officer | SCR-28 | Proceeds matching | Write-off and posting |
| RW-DEBTSALE | Debt sale officer | SCR-29 | Posting | Write-off and posting |
| RW-DEBTSALE | Debt sale officer | SCR-30 | Case documents | Documents |
| RW-DEBTSALE | Debt sale officer | SCR-31 | Document review queue | Documents |
| RW-DEBTSALE | Debt sale officer | SCR-32 | Document custody | Documents |
| RW-DEBTSALE | Debt sale officer | SCR-33 | Template approval | Documents |
| RW-DEBTSALE | Debt sale officer | SCR-34 | Partner list | Partner portal |
| RW-DEBTSALE | Debt sale officer | SCR-35 | Placement and allocation | Partner portal |
| RW-DEBTSALE | Debt sale officer | SCR-36 | Partner scorecard | Partner portal |
| RW-DEBTSALE | Debt sale officer | SCR-37 | Steering dashboard | Reporting |
| RW-DEBTSALE | Debt sale officer | SCR-38 | Decision log query | Decision log |
| RW-DEBTSALE | Debt sale officer | SCR-39 | Rules and parameters | Rules and parameters |
| RW-DEBTSALE | Debt sale officer | SCR-40 | Reference data | Reference data |
| RW-DEBTSALE | Debt sale officer | SCR-41 | Delegation of authority | Rules and parameters |
| RW-DEBTSALE | Debt sale officer | SCR-42 | Queues and service levels | Queue and allocation |
| RW-WRITEOFF | Write-off team member | SCR-01 | My work | Case record |
| RW-WRITEOFF | Write-off team member | SCR-02 | Case list | Case record |
| RW-WRITEOFF | Write-off team member | SCR-03 | Case record | Case record |
| RW-WRITEOFF | Write-off team member | SCR-04 | Case timeline | Case record |
| RW-WRITEOFF | Write-off team member | SCR-06 | Raise deviation | Case record |
| RW-WRITEOFF | Write-off team member | SCR-08 | Deviation queue | Case record |
| RW-WRITEOFF | Write-off team member | SCR-10 | Approval queue | Decision log |
| RW-WRITEOFF | Write-off team member | SCR-11 | Decision screen | Decision log |
| RW-WRITEOFF | Write-off team member | SCR-12 | Committee pack | Decision log |
| RW-WRITEOFF | Write-off team member | SCR-18 | Notice approval | Litigation |
| RW-WRITEOFF | Write-off team member | SCR-19 | Litigation workspace | Litigation |
| RW-WRITEOFF | Write-off team member | SCR-20 | Enforcement workspace | Litigation |
| RW-WRITEOFF | Write-off team member | SCR-21 | Asset list | Asset and disposal |
| RW-WRITEOFF | Write-off team member | SCR-22 | Asset record | Asset and disposal |
| RW-WRITEOFF | Write-off team member | SCR-23 | Listing and price | Asset and disposal |
| RW-WRITEOFF | Write-off team member | SCR-24 | Auction rounds | Asset and disposal |
| RW-WRITEOFF | Write-off team member | SCR-25 | Lot builder | Debt sale |
| RW-WRITEOFF | Write-off team member | SCR-26 | Award | Debt sale |
| RW-WRITEOFF | Write-off team member | SCR-27 | Write-off proposal | Write-off and posting |
| RW-WRITEOFF | Write-off team member | SCR-28 | Proceeds matching | Write-off and posting |
| RW-WRITEOFF | Write-off team member | SCR-29 | Posting | Write-off and posting |
| RW-WRITEOFF | Write-off team member | SCR-30 | Case documents | Documents |
| RW-WRITEOFF | Write-off team member | SCR-31 | Document review queue | Documents |
| RW-WRITEOFF | Write-off team member | SCR-32 | Document custody | Documents |
| RW-WRITEOFF | Write-off team member | SCR-33 | Template approval | Documents |
| RW-WRITEOFF | Write-off team member | SCR-37 | Steering dashboard | Reporting |
| RW-WRITEOFF | Write-off team member | SCR-38 | Decision log query | Decision log |
| RW-WRITEOFF | Write-off team member | SCR-39 | Rules and parameters | Rules and parameters |
| RW-WRITEOFF | Write-off team member | SCR-40 | Reference data | Reference data |
| RW-WRITEOFF | Write-off team member | SCR-41 | Delegation of authority | Rules and parameters |
| RW-CREDITAD | Credit Administration officer | SCR-01 | My work | Case record |
| RW-CREDITAD | Credit Administration officer | SCR-02 | Case list | Case record |
| RW-CREDITAD | Credit Administration officer | SCR-03 | Case record | Case record |
| RW-CREDITAD | Credit Administration officer | SCR-04 | Case timeline | Case record |
| RW-CREDITAD | Credit Administration officer | SCR-06 | Raise deviation | Case record |
| RW-CREDITAD | Credit Administration officer | SCR-08 | Deviation queue | Case record |
| RW-CREDITAD | Credit Administration officer | SCR-10 | Approval queue | Decision log |
| RW-CREDITAD | Credit Administration officer | SCR-11 | Decision screen | Decision log |
| RW-CREDITAD | Credit Administration officer | SCR-12 | Committee pack | Decision log |
| RW-CREDITAD | Credit Administration officer | SCR-18 | Notice approval | Litigation |
| RW-CREDITAD | Credit Administration officer | SCR-19 | Litigation workspace | Litigation |
| RW-CREDITAD | Credit Administration officer | SCR-20 | Enforcement workspace | Litigation |
| RW-CREDITAD | Credit Administration officer | SCR-21 | Asset list | Asset and disposal |
| RW-CREDITAD | Credit Administration officer | SCR-22 | Asset record | Asset and disposal |
| RW-CREDITAD | Credit Administration officer | SCR-23 | Listing and price | Asset and disposal |
| RW-CREDITAD | Credit Administration officer | SCR-24 | Auction rounds | Asset and disposal |
| RW-CREDITAD | Credit Administration officer | SCR-25 | Lot builder | Debt sale |
| RW-CREDITAD | Credit Administration officer | SCR-26 | Award | Debt sale |
| RW-CREDITAD | Credit Administration officer | SCR-27 | Write-off proposal | Write-off and posting |
| RW-CREDITAD | Credit Administration officer | SCR-28 | Proceeds matching | Write-off and posting |
| RW-CREDITAD | Credit Administration officer | SCR-29 | Posting | Write-off and posting |
| RW-CREDITAD | Credit Administration officer | SCR-30 | Case documents | Documents |
| RW-CREDITAD | Credit Administration officer | SCR-31 | Document review queue | Documents |
| RW-CREDITAD | Credit Administration officer | SCR-32 | Document custody | Documents |
| RW-CREDITAD | Credit Administration officer | SCR-33 | Template approval | Documents |
| RW-CREDITAD | Credit Administration officer | SCR-37 | Steering dashboard | Reporting |
| RW-CREDITAD | Credit Administration officer | SCR-38 | Decision log query | Decision log |
| RW-CREDITAD | Credit Administration officer | SCR-39 | Rules and parameters | Rules and parameters |
| RW-CREDITAD | Credit Administration officer | SCR-40 | Reference data | Reference data |
| RW-CREDITAD | Credit Administration officer | SCR-41 | Delegation of authority | Rules and parameters |
| RW-GUARANT | Guarantee officer | SCR-01 | My work | Case record |
| RW-GUARANT | Guarantee officer | SCR-02 | Case list | Case record |
| RW-GUARANT | Guarantee officer | SCR-03 | Case record | Case record |
| RW-GUARANT | Guarantee officer | SCR-04 | Case timeline | Case record |
| RW-GUARANT | Guarantee officer | SCR-05 | Transfer case | Queue and allocation |
| RW-GUARANT | Guarantee officer | SCR-06 | Raise deviation | Case record |
| RW-GUARANT | Guarantee officer | SCR-07 | Team queues | Queue and allocation |
| RW-GUARANT | Guarantee officer | SCR-08 | Deviation queue | Case record |
| RW-GUARANT | Guarantee officer | SCR-09 | Exception queue | Queue and allocation |
| RW-GUARANT | Guarantee officer | SCR-10 | Approval queue | Decision log |
| RW-GUARANT | Guarantee officer | SCR-11 | Decision screen | Decision log |
| RW-GUARANT | Guarantee officer | SCR-12 | Committee pack | Decision log |
| RW-GUARANT | Guarantee officer | SCR-13 | Route decision | Treatment and offer |
| RW-GUARANT | Guarantee officer | SCR-14 | Treatment record | Treatment and offer |
| RW-GUARANT | Guarantee officer | SCR-15 | Settlement offer | Treatment and offer |
| RW-GUARANT | Guarantee officer | SCR-16 | Deed in lieu | Treatment and offer |
| RW-GUARANT | Guarantee officer | SCR-17 | Guarantee claim | Treatment and offer |
| RW-GUARANT | Guarantee officer | SCR-18 | Notice approval | Litigation |
| RW-GUARANT | Guarantee officer | SCR-19 | Litigation workspace | Litigation |
| RW-GUARANT | Guarantee officer | SCR-20 | Enforcement workspace | Litigation |
| RW-GUARANT | Guarantee officer | SCR-30 | Case documents | Documents |
| RW-GUARANT | Guarantee officer | SCR-31 | Document review queue | Documents |
| RW-GUARANT | Guarantee officer | SCR-32 | Document custody | Documents |
| RW-GUARANT | Guarantee officer | SCR-33 | Template approval | Documents |
| RW-GUARANT | Guarantee officer | SCR-34 | Partner list | Partner portal |
| RW-GUARANT | Guarantee officer | SCR-35 | Placement and allocation | Partner portal |
| RW-GUARANT | Guarantee officer | SCR-36 | Partner scorecard | Partner portal |
| RW-GUARANT | Guarantee officer | SCR-37 | Steering dashboard | Reporting |
| RW-GUARANT | Guarantee officer | SCR-38 | Decision log query | Decision log |
| RW-GUARANT | Guarantee officer | SCR-39 | Rules and parameters | Rules and parameters |
| RW-GUARANT | Guarantee officer | SCR-40 | Reference data | Reference data |
| RW-GUARANT | Guarantee officer | SCR-41 | Delegation of authority | Rules and parameters |
| RW-GUARANT | Guarantee officer | SCR-42 | Queues and service levels | Queue and allocation |
| RW-AGENCYMG | Partner and agency manager | SCR-01 | My work | Case record |
| RW-AGENCYMG | Partner and agency manager | SCR-02 | Case list | Case record |
| RW-AGENCYMG | Partner and agency manager | SCR-03 | Case record | Case record |
| RW-AGENCYMG | Partner and agency manager | SCR-04 | Case timeline | Case record |
| RW-AGENCYMG | Partner and agency manager | SCR-05 | Transfer case | Queue and allocation |
| RW-AGENCYMG | Partner and agency manager | SCR-06 | Raise deviation | Case record |
| RW-AGENCYMG | Partner and agency manager | SCR-07 | Team queues | Queue and allocation |
| RW-AGENCYMG | Partner and agency manager | SCR-08 | Deviation queue | Case record |
| RW-AGENCYMG | Partner and agency manager | SCR-09 | Exception queue | Queue and allocation |
| RW-AGENCYMG | Partner and agency manager | SCR-10 | Approval queue | Decision log |
| RW-AGENCYMG | Partner and agency manager | SCR-11 | Decision screen | Decision log |
| RW-AGENCYMG | Partner and agency manager | SCR-12 | Committee pack | Decision log |
| RW-AGENCYMG | Partner and agency manager | SCR-18 | Notice approval | Litigation |
| RW-AGENCYMG | Partner and agency manager | SCR-19 | Litigation workspace | Litigation |
| RW-AGENCYMG | Partner and agency manager | SCR-20 | Enforcement workspace | Litigation |
| RW-AGENCYMG | Partner and agency manager | SCR-21 | Asset list | Asset and disposal |
| RW-AGENCYMG | Partner and agency manager | SCR-22 | Asset record | Asset and disposal |
| RW-AGENCYMG | Partner and agency manager | SCR-23 | Listing and price | Asset and disposal |
| RW-AGENCYMG | Partner and agency manager | SCR-24 | Auction rounds | Asset and disposal |
| RW-AGENCYMG | Partner and agency manager | SCR-25 | Lot builder | Debt sale |
| RW-AGENCYMG | Partner and agency manager | SCR-26 | Award | Debt sale |
| RW-AGENCYMG | Partner and agency manager | SCR-30 | Case documents | Documents |
| RW-AGENCYMG | Partner and agency manager | SCR-31 | Document review queue | Documents |
| RW-AGENCYMG | Partner and agency manager | SCR-32 | Document custody | Documents |
| RW-AGENCYMG | Partner and agency manager | SCR-33 | Template approval | Documents |
| RW-AGENCYMG | Partner and agency manager | SCR-34 | Partner list | Partner portal |
| RW-AGENCYMG | Partner and agency manager | SCR-35 | Placement and allocation | Partner portal |
| RW-AGENCYMG | Partner and agency manager | SCR-36 | Partner scorecard | Partner portal |
| RW-AGENCYMG | Partner and agency manager | SCR-37 | Steering dashboard | Reporting |
| RW-AGENCYMG | Partner and agency manager | SCR-38 | Decision log query | Decision log |
| RW-AGENCYMG | Partner and agency manager | SCR-39 | Rules and parameters | Rules and parameters |
| RW-AGENCYMG | Partner and agency manager | SCR-40 | Reference data | Reference data |
| RW-AGENCYMG | Partner and agency manager | SCR-41 | Delegation of authority | Rules and parameters |
| RW-AGENCYMG | Partner and agency manager | SCR-42 | Queues and service levels | Queue and allocation |
| RW-CONDUCT | Conduct and QA officer | SCR-01 | My work | Case record |
| RW-CONDUCT | Conduct and QA officer | SCR-02 | Case list | Case record |
| RW-CONDUCT | Conduct and QA officer | SCR-03 | Case record | Case record |
| RW-CONDUCT | Conduct and QA officer | SCR-04 | Case timeline | Case record |
| RW-CONDUCT | Conduct and QA officer | SCR-05 | Transfer case | Queue and allocation |
| RW-CONDUCT | Conduct and QA officer | SCR-06 | Raise deviation | Case record |
| RW-CONDUCT | Conduct and QA officer | SCR-07 | Team queues | Queue and allocation |
| RW-CONDUCT | Conduct and QA officer | SCR-08 | Deviation queue | Case record |
| RW-CONDUCT | Conduct and QA officer | SCR-09 | Exception queue | Queue and allocation |
| RW-CONDUCT | Conduct and QA officer | SCR-10 | Approval queue | Decision log |
| RW-CONDUCT | Conduct and QA officer | SCR-11 | Decision screen | Decision log |
| RW-CONDUCT | Conduct and QA officer | SCR-12 | Committee pack | Decision log |
| RW-CONDUCT | Conduct and QA officer | SCR-13 | Route decision | Treatment and offer |
| RW-CONDUCT | Conduct and QA officer | SCR-14 | Treatment record | Treatment and offer |
| RW-CONDUCT | Conduct and QA officer | SCR-15 | Settlement offer | Treatment and offer |
| RW-CONDUCT | Conduct and QA officer | SCR-16 | Deed in lieu | Treatment and offer |
| RW-CONDUCT | Conduct and QA officer | SCR-17 | Guarantee claim | Treatment and offer |
| RW-CONDUCT | Conduct and QA officer | SCR-18 | Notice approval | Litigation |
| RW-CONDUCT | Conduct and QA officer | SCR-19 | Litigation workspace | Litigation |
| RW-CONDUCT | Conduct and QA officer | SCR-20 | Enforcement workspace | Litigation |
| RW-CONDUCT | Conduct and QA officer | SCR-21 | Asset list | Asset and disposal |
| RW-CONDUCT | Conduct and QA officer | SCR-22 | Asset record | Asset and disposal |
| RW-CONDUCT | Conduct and QA officer | SCR-23 | Listing and price | Asset and disposal |
| RW-CONDUCT | Conduct and QA officer | SCR-24 | Auction rounds | Asset and disposal |
| RW-CONDUCT | Conduct and QA officer | SCR-25 | Lot builder | Debt sale |
| RW-CONDUCT | Conduct and QA officer | SCR-26 | Award | Debt sale |
| RW-CONDUCT | Conduct and QA officer | SCR-27 | Write-off proposal | Write-off and posting |
| RW-CONDUCT | Conduct and QA officer | SCR-28 | Proceeds matching | Write-off and posting |
| RW-CONDUCT | Conduct and QA officer | SCR-29 | Posting | Write-off and posting |
| RW-CONDUCT | Conduct and QA officer | SCR-30 | Case documents | Documents |
| RW-CONDUCT | Conduct and QA officer | SCR-31 | Document review queue | Documents |
| RW-CONDUCT | Conduct and QA officer | SCR-32 | Document custody | Documents |
| RW-CONDUCT | Conduct and QA officer | SCR-33 | Template approval | Documents |
| RW-CONDUCT | Conduct and QA officer | SCR-34 | Partner list | Partner portal |
| RW-CONDUCT | Conduct and QA officer | SCR-35 | Placement and allocation | Partner portal |
| RW-CONDUCT | Conduct and QA officer | SCR-36 | Partner scorecard | Partner portal |
| RW-CONDUCT | Conduct and QA officer | SCR-37 | Steering dashboard | Reporting |
| RW-CONDUCT | Conduct and QA officer | SCR-38 | Decision log query | Decision log |
| RW-CONDUCT | Conduct and QA officer | SCR-39 | Rules and parameters | Rules and parameters |
| RW-CONDUCT | Conduct and QA officer | SCR-40 | Reference data | Reference data |
| RW-CONDUCT | Conduct and QA officer | SCR-41 | Delegation of authority | Rules and parameters |
| RW-CONDUCT | Conduct and QA officer | SCR-42 | Queues and service levels | Queue and allocation |
| RW-CAPACITY | Capacity and workforce planner | SCR-01 | My work | Case record |
| RW-CAPACITY | Capacity and workforce planner | SCR-02 | Case list | Case record |
| RW-CAPACITY | Capacity and workforce planner | SCR-03 | Case record | Case record |
| RW-CAPACITY | Capacity and workforce planner | SCR-04 | Case timeline | Case record |
| RW-CAPACITY | Capacity and workforce planner | SCR-05 | Transfer case | Queue and allocation |
| RW-CAPACITY | Capacity and workforce planner | SCR-06 | Raise deviation | Case record |
| RW-CAPACITY | Capacity and workforce planner | SCR-07 | Team queues | Queue and allocation |
| RW-CAPACITY | Capacity and workforce planner | SCR-08 | Deviation queue | Case record |
| RW-CAPACITY | Capacity and workforce planner | SCR-09 | Exception queue | Queue and allocation |
| RW-CAPACITY | Capacity and workforce planner | SCR-34 | Partner list | Partner portal |
| RW-CAPACITY | Capacity and workforce planner | SCR-35 | Placement and allocation | Partner portal |
| RW-CAPACITY | Capacity and workforce planner | SCR-36 | Partner scorecard | Partner portal |
| RW-CAPACITY | Capacity and workforce planner | SCR-37 | Steering dashboard | Reporting |
| RW-CAPACITY | Capacity and workforce planner | SCR-39 | Rules and parameters | Rules and parameters |
| RW-CAPACITY | Capacity and workforce planner | SCR-40 | Reference data | Reference data |
| RW-CAPACITY | Capacity and workforce planner | SCR-41 | Delegation of authority | Rules and parameters |
| RW-CAPACITY | Capacity and workforce planner | SCR-42 | Queues and service levels | Queue and allocation |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-01 | My work | Case record |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-02 | Case list | Case record |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-03 | Case record | Case record |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-04 | Case timeline | Case record |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-05 | Transfer case | Queue and allocation |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-06 | Raise deviation | Case record |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-07 | Team queues | Queue and allocation |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-08 | Deviation queue | Case record |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-09 | Exception queue | Queue and allocation |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-10 | Approval queue | Decision log |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-11 | Decision screen | Decision log |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-12 | Committee pack | Decision log |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-13 | Route decision | Treatment and offer |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-14 | Treatment record | Treatment and offer |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-15 | Settlement offer | Treatment and offer |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-16 | Deed in lieu | Treatment and offer |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-17 | Guarantee claim | Treatment and offer |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-18 | Notice approval | Litigation |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-19 | Litigation workspace | Litigation |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-20 | Enforcement workspace | Litigation |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-21 | Asset list | Asset and disposal |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-22 | Asset record | Asset and disposal |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-23 | Listing and price | Asset and disposal |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-24 | Auction rounds | Asset and disposal |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-25 | Lot builder | Debt sale |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-26 | Award | Debt sale |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-27 | Write-off proposal | Write-off and posting |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-28 | Proceeds matching | Write-off and posting |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-29 | Posting | Write-off and posting |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-30 | Case documents | Documents |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-31 | Document review queue | Documents |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-32 | Document custody | Documents |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-33 | Template approval | Documents |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-34 | Partner list | Partner portal |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-35 | Placement and allocation | Partner portal |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-36 | Partner scorecard | Partner portal |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-37 | Steering dashboard | Reporting |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-38 | Decision log query | Decision log |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-39 | Rules and parameters | Rules and parameters |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-40 | Reference data | Reference data |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-41 | Delegation of authority | Rules and parameters |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | SCR-42 | Queues and service levels | Queue and allocation |
| RW-HEADLIT | Head of Litigation | SCR-01 | My work | Case record |
| RW-HEADLIT | Head of Litigation | SCR-02 | Case list | Case record |
| RW-HEADLIT | Head of Litigation | SCR-03 | Case record | Case record |
| RW-HEADLIT | Head of Litigation | SCR-04 | Case timeline | Case record |
| RW-HEADLIT | Head of Litigation | SCR-05 | Transfer case | Queue and allocation |
| RW-HEADLIT | Head of Litigation | SCR-06 | Raise deviation | Case record |
| RW-HEADLIT | Head of Litigation | SCR-07 | Team queues | Queue and allocation |
| RW-HEADLIT | Head of Litigation | SCR-08 | Deviation queue | Case record |
| RW-HEADLIT | Head of Litigation | SCR-09 | Exception queue | Queue and allocation |
| RW-HEADLIT | Head of Litigation | SCR-10 | Approval queue | Decision log |
| RW-HEADLIT | Head of Litigation | SCR-11 | Decision screen | Decision log |
| RW-HEADLIT | Head of Litigation | SCR-12 | Committee pack | Decision log |
| RW-HEADLIT | Head of Litigation | SCR-18 | Notice approval | Litigation |
| RW-HEADLIT | Head of Litigation | SCR-19 | Litigation workspace | Litigation |
| RW-HEADLIT | Head of Litigation | SCR-20 | Enforcement workspace | Litigation |
| RW-HEADLIT | Head of Litigation | SCR-21 | Asset list | Asset and disposal |
| RW-HEADLIT | Head of Litigation | SCR-22 | Asset record | Asset and disposal |
| RW-HEADLIT | Head of Litigation | SCR-23 | Listing and price | Asset and disposal |
| RW-HEADLIT | Head of Litigation | SCR-24 | Auction rounds | Asset and disposal |
| RW-HEADLIT | Head of Litigation | SCR-30 | Case documents | Documents |
| RW-HEADLIT | Head of Litigation | SCR-31 | Document review queue | Documents |
| RW-HEADLIT | Head of Litigation | SCR-32 | Document custody | Documents |
| RW-HEADLIT | Head of Litigation | SCR-33 | Template approval | Documents |
| RW-HEADLIT | Head of Litigation | SCR-34 | Partner list | Partner portal |
| RW-HEADLIT | Head of Litigation | SCR-35 | Placement and allocation | Partner portal |
| RW-HEADLIT | Head of Litigation | SCR-36 | Partner scorecard | Partner portal |
| RW-HEADLIT | Head of Litigation | SCR-37 | Steering dashboard | Reporting |
| RW-HEADLIT | Head of Litigation | SCR-38 | Decision log query | Decision log |
| RW-HEADLIT | Head of Litigation | SCR-39 | Rules and parameters | Rules and parameters |
| RW-HEADLIT | Head of Litigation | SCR-40 | Reference data | Reference data |
| RW-HEADLIT | Head of Litigation | SCR-41 | Delegation of authority | Rules and parameters |
| RW-HEADLIT | Head of Litigation | SCR-42 | Queues and service levels | Queue and allocation |
| RW-HEADNPA | Head of NPA | SCR-01 | My work | Case record |
| RW-HEADNPA | Head of NPA | SCR-02 | Case list | Case record |
| RW-HEADNPA | Head of NPA | SCR-03 | Case record | Case record |
| RW-HEADNPA | Head of NPA | SCR-04 | Case timeline | Case record |
| RW-HEADNPA | Head of NPA | SCR-06 | Raise deviation | Case record |
| RW-HEADNPA | Head of NPA | SCR-08 | Deviation queue | Case record |
| RW-HEADNPA | Head of NPA | SCR-10 | Approval queue | Decision log |
| RW-HEADNPA | Head of NPA | SCR-11 | Decision screen | Decision log |
| RW-HEADNPA | Head of NPA | SCR-12 | Committee pack | Decision log |
| RW-HEADNPA | Head of NPA | SCR-18 | Notice approval | Litigation |
| RW-HEADNPA | Head of NPA | SCR-19 | Litigation workspace | Litigation |
| RW-HEADNPA | Head of NPA | SCR-20 | Enforcement workspace | Litigation |
| RW-HEADNPA | Head of NPA | SCR-21 | Asset list | Asset and disposal |
| RW-HEADNPA | Head of NPA | SCR-22 | Asset record | Asset and disposal |
| RW-HEADNPA | Head of NPA | SCR-23 | Listing and price | Asset and disposal |
| RW-HEADNPA | Head of NPA | SCR-24 | Auction rounds | Asset and disposal |
| RW-HEADNPA | Head of NPA | SCR-25 | Lot builder | Debt sale |
| RW-HEADNPA | Head of NPA | SCR-26 | Award | Debt sale |
| RW-HEADNPA | Head of NPA | SCR-30 | Case documents | Documents |
| RW-HEADNPA | Head of NPA | SCR-31 | Document review queue | Documents |
| RW-HEADNPA | Head of NPA | SCR-32 | Document custody | Documents |
| RW-HEADNPA | Head of NPA | SCR-33 | Template approval | Documents |
| RW-HEADNPA | Head of NPA | SCR-34 | Partner list | Partner portal |
| RW-HEADNPA | Head of NPA | SCR-35 | Placement and allocation | Partner portal |
| RW-HEADNPA | Head of NPA | SCR-36 | Partner scorecard | Partner portal |
| RW-HEADNPA | Head of NPA | SCR-37 | Steering dashboard | Reporting |
| RW-HEADNPA | Head of NPA | SCR-38 | Decision log query | Decision log |
| RW-HEADNPA | Head of NPA | SCR-39 | Rules and parameters | Rules and parameters |
| RW-HEADNPA | Head of NPA | SCR-40 | Reference data | Reference data |
| RW-HEADNPA | Head of NPA | SCR-41 | Delegation of authority | Rules and parameters |
| RW-HEADASL | Head of Asset Liquidity | SCR-01 | My work | Case record |
| RW-HEADASL | Head of Asset Liquidity | SCR-02 | Case list | Case record |
| RW-HEADASL | Head of Asset Liquidity | SCR-03 | Case record | Case record |
| RW-HEADASL | Head of Asset Liquidity | SCR-04 | Case timeline | Case record |
| RW-HEADASL | Head of Asset Liquidity | SCR-06 | Raise deviation | Case record |
| RW-HEADASL | Head of Asset Liquidity | SCR-08 | Deviation queue | Case record |
| RW-HEADASL | Head of Asset Liquidity | SCR-10 | Approval queue | Decision log |
| RW-HEADASL | Head of Asset Liquidity | SCR-11 | Decision screen | Decision log |
| RW-HEADASL | Head of Asset Liquidity | SCR-12 | Committee pack | Decision log |
| RW-HEADASL | Head of Asset Liquidity | SCR-18 | Notice approval | Litigation |
| RW-HEADASL | Head of Asset Liquidity | SCR-19 | Litigation workspace | Litigation |
| RW-HEADASL | Head of Asset Liquidity | SCR-20 | Enforcement workspace | Litigation |
| RW-HEADASL | Head of Asset Liquidity | SCR-21 | Asset list | Asset and disposal |
| RW-HEADASL | Head of Asset Liquidity | SCR-22 | Asset record | Asset and disposal |
| RW-HEADASL | Head of Asset Liquidity | SCR-23 | Listing and price | Asset and disposal |
| RW-HEADASL | Head of Asset Liquidity | SCR-24 | Auction rounds | Asset and disposal |
| RW-HEADASL | Head of Asset Liquidity | SCR-25 | Lot builder | Debt sale |
| RW-HEADASL | Head of Asset Liquidity | SCR-26 | Award | Debt sale |
| RW-HEADASL | Head of Asset Liquidity | SCR-30 | Case documents | Documents |
| RW-HEADASL | Head of Asset Liquidity | SCR-31 | Document review queue | Documents |
| RW-HEADASL | Head of Asset Liquidity | SCR-32 | Document custody | Documents |
| RW-HEADASL | Head of Asset Liquidity | SCR-33 | Template approval | Documents |
| RW-HEADASL | Head of Asset Liquidity | SCR-34 | Partner list | Partner portal |
| RW-HEADASL | Head of Asset Liquidity | SCR-35 | Placement and allocation | Partner portal |
| RW-HEADASL | Head of Asset Liquidity | SCR-36 | Partner scorecard | Partner portal |
| RW-HEADASL | Head of Asset Liquidity | SCR-37 | Steering dashboard | Reporting |
| RW-HEADASL | Head of Asset Liquidity | SCR-38 | Decision log query | Decision log |
| RW-HEADASL | Head of Asset Liquidity | SCR-39 | Rules and parameters | Rules and parameters |
| RW-HEADASL | Head of Asset Liquidity | SCR-40 | Reference data | Reference data |
| RW-HEADASL | Head of Asset Liquidity | SCR-41 | Delegation of authority | Rules and parameters |
| RW-CREDCOMM | Credit approval committee member | SCR-01 | My work | Case record |
| RW-CREDCOMM | Credit approval committee member | SCR-02 | Case list | Case record |
| RW-CREDCOMM | Credit approval committee member | SCR-03 | Case record | Case record |
| RW-CREDCOMM | Credit approval committee member | SCR-04 | Case timeline | Case record |
| RW-CREDCOMM | Credit approval committee member | SCR-06 | Raise deviation | Case record |
| RW-CREDCOMM | Credit approval committee member | SCR-08 | Deviation queue | Case record |
| RW-CREDCOMM | Credit approval committee member | SCR-10 | Approval queue | Decision log |
| RW-CREDCOMM | Credit approval committee member | SCR-11 | Decision screen | Decision log |
| RW-CREDCOMM | Credit approval committee member | SCR-12 | Committee pack | Decision log |
| RW-CREDCOMM | Credit approval committee member | SCR-13 | Route decision | Treatment and offer |
| RW-CREDCOMM | Credit approval committee member | SCR-14 | Treatment record | Treatment and offer |
| RW-CREDCOMM | Credit approval committee member | SCR-15 | Settlement offer | Treatment and offer |
| RW-CREDCOMM | Credit approval committee member | SCR-16 | Deed in lieu | Treatment and offer |
| RW-CREDCOMM | Credit approval committee member | SCR-17 | Guarantee claim | Treatment and offer |
| RW-CREDCOMM | Credit approval committee member | SCR-30 | Case documents | Documents |
| RW-CREDCOMM | Credit approval committee member | SCR-31 | Document review queue | Documents |
| RW-CREDCOMM | Credit approval committee member | SCR-32 | Document custody | Documents |
| RW-CREDCOMM | Credit approval committee member | SCR-33 | Template approval | Documents |
| RW-CREDCOMM | Credit approval committee member | SCR-37 | Steering dashboard | Reporting |
| RW-CREDCOMM | Credit approval committee member | SCR-38 | Decision log query | Decision log |
| RW-CREDCOMM | Credit approval committee member | SCR-39 | Rules and parameters | Rules and parameters |
| RW-CREDCOMM | Credit approval committee member | SCR-40 | Reference data | Reference data |
| RW-CREDCOMM | Credit approval committee member | SCR-41 | Delegation of authority | Rules and parameters |
| RW-WOCOMM | Write-off committee member | SCR-01 | My work | Case record |
| RW-WOCOMM | Write-off committee member | SCR-02 | Case list | Case record |
| RW-WOCOMM | Write-off committee member | SCR-03 | Case record | Case record |
| RW-WOCOMM | Write-off committee member | SCR-04 | Case timeline | Case record |
| RW-WOCOMM | Write-off committee member | SCR-06 | Raise deviation | Case record |
| RW-WOCOMM | Write-off committee member | SCR-08 | Deviation queue | Case record |
| RW-WOCOMM | Write-off committee member | SCR-10 | Approval queue | Decision log |
| RW-WOCOMM | Write-off committee member | SCR-11 | Decision screen | Decision log |
| RW-WOCOMM | Write-off committee member | SCR-12 | Committee pack | Decision log |
| RW-WOCOMM | Write-off committee member | SCR-27 | Write-off proposal | Write-off and posting |
| RW-WOCOMM | Write-off committee member | SCR-28 | Proceeds matching | Write-off and posting |
| RW-WOCOMM | Write-off committee member | SCR-29 | Posting | Write-off and posting |
| RW-WOCOMM | Write-off committee member | SCR-30 | Case documents | Documents |
| RW-WOCOMM | Write-off committee member | SCR-31 | Document review queue | Documents |
| RW-WOCOMM | Write-off committee member | SCR-32 | Document custody | Documents |
| RW-WOCOMM | Write-off committee member | SCR-33 | Template approval | Documents |
| RW-WOCOMM | Write-off committee member | SCR-37 | Steering dashboard | Reporting |
| RW-WOCOMM | Write-off committee member | SCR-38 | Decision log query | Decision log |
| RW-WOCOMM | Write-off committee member | SCR-39 | Rules and parameters | Rules and parameters |
| RW-WOCOMM | Write-off committee member | SCR-40 | Reference data | Reference data |
| RW-WOCOMM | Write-off committee member | SCR-41 | Delegation of authority | Rules and parameters |
| RW-RISK | Risk and model risk officer | SCR-01 | My work | Case record |
| RW-RISK | Risk and model risk officer | SCR-02 | Case list | Case record |
| RW-RISK | Risk and model risk officer | SCR-03 | Case record | Case record |
| RW-RISK | Risk and model risk officer | SCR-04 | Case timeline | Case record |
| RW-RISK | Risk and model risk officer | SCR-05 | Transfer case | Queue and allocation |
| RW-RISK | Risk and model risk officer | SCR-06 | Raise deviation | Case record |
| RW-RISK | Risk and model risk officer | SCR-07 | Team queues | Queue and allocation |
| RW-RISK | Risk and model risk officer | SCR-08 | Deviation queue | Case record |
| RW-RISK | Risk and model risk officer | SCR-09 | Exception queue | Queue and allocation |
| RW-RISK | Risk and model risk officer | SCR-10 | Approval queue | Decision log |
| RW-RISK | Risk and model risk officer | SCR-11 | Decision screen | Decision log |
| RW-RISK | Risk and model risk officer | SCR-12 | Committee pack | Decision log |
| RW-RISK | Risk and model risk officer | SCR-13 | Route decision | Treatment and offer |
| RW-RISK | Risk and model risk officer | SCR-14 | Treatment record | Treatment and offer |
| RW-RISK | Risk and model risk officer | SCR-15 | Settlement offer | Treatment and offer |
| RW-RISK | Risk and model risk officer | SCR-16 | Deed in lieu | Treatment and offer |
| RW-RISK | Risk and model risk officer | SCR-17 | Guarantee claim | Treatment and offer |
| RW-RISK | Risk and model risk officer | SCR-18 | Notice approval | Litigation |
| RW-RISK | Risk and model risk officer | SCR-19 | Litigation workspace | Litigation |
| RW-RISK | Risk and model risk officer | SCR-20 | Enforcement workspace | Litigation |
| RW-RISK | Risk and model risk officer | SCR-21 | Asset list | Asset and disposal |
| RW-RISK | Risk and model risk officer | SCR-22 | Asset record | Asset and disposal |
| RW-RISK | Risk and model risk officer | SCR-23 | Listing and price | Asset and disposal |
| RW-RISK | Risk and model risk officer | SCR-24 | Auction rounds | Asset and disposal |
| RW-RISK | Risk and model risk officer | SCR-25 | Lot builder | Debt sale |
| RW-RISK | Risk and model risk officer | SCR-26 | Award | Debt sale |
| RW-RISK | Risk and model risk officer | SCR-27 | Write-off proposal | Write-off and posting |
| RW-RISK | Risk and model risk officer | SCR-28 | Proceeds matching | Write-off and posting |
| RW-RISK | Risk and model risk officer | SCR-29 | Posting | Write-off and posting |
| RW-RISK | Risk and model risk officer | SCR-30 | Case documents | Documents |
| RW-RISK | Risk and model risk officer | SCR-31 | Document review queue | Documents |
| RW-RISK | Risk and model risk officer | SCR-32 | Document custody | Documents |
| RW-RISK | Risk and model risk officer | SCR-33 | Template approval | Documents |
| RW-RISK | Risk and model risk officer | SCR-34 | Partner list | Partner portal |
| RW-RISK | Risk and model risk officer | SCR-35 | Placement and allocation | Partner portal |
| RW-RISK | Risk and model risk officer | SCR-36 | Partner scorecard | Partner portal |
| RW-RISK | Risk and model risk officer | SCR-37 | Steering dashboard | Reporting |
| RW-RISK | Risk and model risk officer | SCR-38 | Decision log query | Decision log |
| RW-RISK | Risk and model risk officer | SCR-39 | Rules and parameters | Rules and parameters |
| RW-RISK | Risk and model risk officer | SCR-40 | Reference data | Reference data |
| RW-RISK | Risk and model risk officer | SCR-41 | Delegation of authority | Rules and parameters |
| RW-RISK | Risk and model risk officer | SCR-42 | Queues and service levels | Queue and allocation |
| RW-COE | Center of excellence analyst | SCR-01 | My work | Case record |
| RW-COE | Center of excellence analyst | SCR-02 | Case list | Case record |
| RW-COE | Center of excellence analyst | SCR-03 | Case record | Case record |
| RW-COE | Center of excellence analyst | SCR-04 | Case timeline | Case record |
| RW-COE | Center of excellence analyst | SCR-05 | Transfer case | Queue and allocation |
| RW-COE | Center of excellence analyst | SCR-06 | Raise deviation | Case record |
| RW-COE | Center of excellence analyst | SCR-07 | Team queues | Queue and allocation |
| RW-COE | Center of excellence analyst | SCR-08 | Deviation queue | Case record |
| RW-COE | Center of excellence analyst | SCR-09 | Exception queue | Queue and allocation |
| RW-COE | Center of excellence analyst | SCR-10 | Approval queue | Decision log |
| RW-COE | Center of excellence analyst | SCR-11 | Decision screen | Decision log |
| RW-COE | Center of excellence analyst | SCR-12 | Committee pack | Decision log |
| RW-COE | Center of excellence analyst | SCR-13 | Route decision | Treatment and offer |
| RW-COE | Center of excellence analyst | SCR-14 | Treatment record | Treatment and offer |
| RW-COE | Center of excellence analyst | SCR-15 | Settlement offer | Treatment and offer |
| RW-COE | Center of excellence analyst | SCR-16 | Deed in lieu | Treatment and offer |
| RW-COE | Center of excellence analyst | SCR-17 | Guarantee claim | Treatment and offer |
| RW-COE | Center of excellence analyst | SCR-18 | Notice approval | Litigation |
| RW-COE | Center of excellence analyst | SCR-19 | Litigation workspace | Litigation |
| RW-COE | Center of excellence analyst | SCR-20 | Enforcement workspace | Litigation |
| RW-COE | Center of excellence analyst | SCR-21 | Asset list | Asset and disposal |
| RW-COE | Center of excellence analyst | SCR-22 | Asset record | Asset and disposal |
| RW-COE | Center of excellence analyst | SCR-23 | Listing and price | Asset and disposal |
| RW-COE | Center of excellence analyst | SCR-24 | Auction rounds | Asset and disposal |
| RW-COE | Center of excellence analyst | SCR-25 | Lot builder | Debt sale |
| RW-COE | Center of excellence analyst | SCR-26 | Award | Debt sale |
| RW-COE | Center of excellence analyst | SCR-27 | Write-off proposal | Write-off and posting |
| RW-COE | Center of excellence analyst | SCR-28 | Proceeds matching | Write-off and posting |
| RW-COE | Center of excellence analyst | SCR-29 | Posting | Write-off and posting |
| RW-COE | Center of excellence analyst | SCR-30 | Case documents | Documents |
| RW-COE | Center of excellence analyst | SCR-31 | Document review queue | Documents |
| RW-COE | Center of excellence analyst | SCR-32 | Document custody | Documents |
| RW-COE | Center of excellence analyst | SCR-33 | Template approval | Documents |
| RW-COE | Center of excellence analyst | SCR-34 | Partner list | Partner portal |
| RW-COE | Center of excellence analyst | SCR-35 | Placement and allocation | Partner portal |
| RW-COE | Center of excellence analyst | SCR-36 | Partner scorecard | Partner portal |
| RW-COE | Center of excellence analyst | SCR-37 | Steering dashboard | Reporting |
| RW-COE | Center of excellence analyst | SCR-38 | Decision log query | Decision log |
| RW-COE | Center of excellence analyst | SCR-39 | Rules and parameters | Rules and parameters |
| RW-COE | Center of excellence analyst | SCR-40 | Reference data | Reference data |
| RW-COE | Center of excellence analyst | SCR-41 | Delegation of authority | Rules and parameters |
| RW-COE | Center of excellence analyst | SCR-42 | Queues and service levels | Queue and allocation |
| RW-COE | Center of excellence analyst | SCR-43 | Roles and access | Platform administration |
| RW-COE | Center of excellence analyst | SCR-44 | Interface and job monitor | Platform administration |
| RW-COE | Center of excellence analyst | SCR-45 | Data quality | Platform administration |
| RW-COE | Center of excellence analyst | SCR-46 | Agent monitor | Platform administration |
| RW-COE | Center of excellence analyst | SCR-47 | Personal data | Platform administration |
| RW-DATASTEW | Data steward and data product owner | SCR-01 | My work | Case record |
| RW-DATASTEW | Data steward and data product owner | SCR-02 | Case list | Case record |
| RW-DATASTEW | Data steward and data product owner | SCR-03 | Case record | Case record |
| RW-DATASTEW | Data steward and data product owner | SCR-04 | Case timeline | Case record |
| RW-DATASTEW | Data steward and data product owner | SCR-06 | Raise deviation | Case record |
| RW-DATASTEW | Data steward and data product owner | SCR-08 | Deviation queue | Case record |
| RW-DATASTEW | Data steward and data product owner | SCR-10 | Approval queue | Decision log |
| RW-DATASTEW | Data steward and data product owner | SCR-11 | Decision screen | Decision log |
| RW-DATASTEW | Data steward and data product owner | SCR-12 | Committee pack | Decision log |
| RW-DATASTEW | Data steward and data product owner | SCR-30 | Case documents | Documents |
| RW-DATASTEW | Data steward and data product owner | SCR-31 | Document review queue | Documents |
| RW-DATASTEW | Data steward and data product owner | SCR-32 | Document custody | Documents |
| RW-DATASTEW | Data steward and data product owner | SCR-33 | Template approval | Documents |
| RW-DATASTEW | Data steward and data product owner | SCR-37 | Steering dashboard | Reporting |
| RW-DATASTEW | Data steward and data product owner | SCR-38 | Decision log query | Decision log |
| RW-DATASTEW | Data steward and data product owner | SCR-39 | Rules and parameters | Rules and parameters |
| RW-DATASTEW | Data steward and data product owner | SCR-40 | Reference data | Reference data |
| RW-DATASTEW | Data steward and data product owner | SCR-41 | Delegation of authority | Rules and parameters |
| RW-DATASTEW | Data steward and data product owner | SCR-43 | Roles and access | Platform administration |
| RW-DATASTEW | Data steward and data product owner | SCR-44 | Interface and job monitor | Platform administration |
| RW-DATASTEW | Data steward and data product owner | SCR-45 | Data quality | Platform administration |
| RW-DATASTEW | Data steward and data product owner | SCR-46 | Agent monitor | Platform administration |
| RW-DATASTEW | Data steward and data product owner | SCR-47 | Personal data | Platform administration |
| RW-FINANCE | Finance and CFO delegate | SCR-01 | My work | Case record |
| RW-FINANCE | Finance and CFO delegate | SCR-02 | Case list | Case record |
| RW-FINANCE | Finance and CFO delegate | SCR-03 | Case record | Case record |
| RW-FINANCE | Finance and CFO delegate | SCR-04 | Case timeline | Case record |
| RW-FINANCE | Finance and CFO delegate | SCR-06 | Raise deviation | Case record |
| RW-FINANCE | Finance and CFO delegate | SCR-08 | Deviation queue | Case record |
| RW-FINANCE | Finance and CFO delegate | SCR-10 | Approval queue | Decision log |
| RW-FINANCE | Finance and CFO delegate | SCR-11 | Decision screen | Decision log |
| RW-FINANCE | Finance and CFO delegate | SCR-12 | Committee pack | Decision log |
| RW-FINANCE | Finance and CFO delegate | SCR-21 | Asset list | Asset and disposal |
| RW-FINANCE | Finance and CFO delegate | SCR-22 | Asset record | Asset and disposal |
| RW-FINANCE | Finance and CFO delegate | SCR-23 | Listing and price | Asset and disposal |
| RW-FINANCE | Finance and CFO delegate | SCR-24 | Auction rounds | Asset and disposal |
| RW-FINANCE | Finance and CFO delegate | SCR-25 | Lot builder | Debt sale |
| RW-FINANCE | Finance and CFO delegate | SCR-26 | Award | Debt sale |
| RW-FINANCE | Finance and CFO delegate | SCR-27 | Write-off proposal | Write-off and posting |
| RW-FINANCE | Finance and CFO delegate | SCR-28 | Proceeds matching | Write-off and posting |
| RW-FINANCE | Finance and CFO delegate | SCR-29 | Posting | Write-off and posting |
| RW-FINANCE | Finance and CFO delegate | SCR-37 | Steering dashboard | Reporting |
| RW-FINANCE | Finance and CFO delegate | SCR-38 | Decision log query | Decision log |
| RW-FINANCE | Finance and CFO delegate | SCR-39 | Rules and parameters | Rules and parameters |
| RW-FINANCE | Finance and CFO delegate | SCR-40 | Reference data | Reference data |
| RW-FINANCE | Finance and CFO delegate | SCR-41 | Delegation of authority | Rules and parameters |
| RW-AUDIT | Internal audit | SCR-01 | My work | Case record |
| RW-AUDIT | Internal audit | SCR-02 | Case list | Case record |
| RW-AUDIT | Internal audit | SCR-03 | Case record | Case record |
| RW-AUDIT | Internal audit | SCR-04 | Case timeline | Case record |
| RW-AUDIT | Internal audit | SCR-05 | Transfer case | Queue and allocation |
| RW-AUDIT | Internal audit | SCR-06 | Raise deviation | Case record |
| RW-AUDIT | Internal audit | SCR-07 | Team queues | Queue and allocation |
| RW-AUDIT | Internal audit | SCR-08 | Deviation queue | Case record |
| RW-AUDIT | Internal audit | SCR-09 | Exception queue | Queue and allocation |
| RW-AUDIT | Internal audit | SCR-10 | Approval queue | Decision log |
| RW-AUDIT | Internal audit | SCR-11 | Decision screen | Decision log |
| RW-AUDIT | Internal audit | SCR-12 | Committee pack | Decision log |
| RW-AUDIT | Internal audit | SCR-13 | Route decision | Treatment and offer |
| RW-AUDIT | Internal audit | SCR-14 | Treatment record | Treatment and offer |
| RW-AUDIT | Internal audit | SCR-15 | Settlement offer | Treatment and offer |
| RW-AUDIT | Internal audit | SCR-16 | Deed in lieu | Treatment and offer |
| RW-AUDIT | Internal audit | SCR-17 | Guarantee claim | Treatment and offer |
| RW-AUDIT | Internal audit | SCR-18 | Notice approval | Litigation |
| RW-AUDIT | Internal audit | SCR-19 | Litigation workspace | Litigation |
| RW-AUDIT | Internal audit | SCR-20 | Enforcement workspace | Litigation |
| RW-AUDIT | Internal audit | SCR-21 | Asset list | Asset and disposal |
| RW-AUDIT | Internal audit | SCR-22 | Asset record | Asset and disposal |
| RW-AUDIT | Internal audit | SCR-23 | Listing and price | Asset and disposal |
| RW-AUDIT | Internal audit | SCR-24 | Auction rounds | Asset and disposal |
| RW-AUDIT | Internal audit | SCR-25 | Lot builder | Debt sale |
| RW-AUDIT | Internal audit | SCR-26 | Award | Debt sale |
| RW-AUDIT | Internal audit | SCR-27 | Write-off proposal | Write-off and posting |
| RW-AUDIT | Internal audit | SCR-28 | Proceeds matching | Write-off and posting |
| RW-AUDIT | Internal audit | SCR-29 | Posting | Write-off and posting |
| RW-AUDIT | Internal audit | SCR-30 | Case documents | Documents |
| RW-AUDIT | Internal audit | SCR-31 | Document review queue | Documents |
| RW-AUDIT | Internal audit | SCR-32 | Document custody | Documents |
| RW-AUDIT | Internal audit | SCR-33 | Template approval | Documents |
| RW-AUDIT | Internal audit | SCR-34 | Partner list | Partner portal |
| RW-AUDIT | Internal audit | SCR-35 | Placement and allocation | Partner portal |
| RW-AUDIT | Internal audit | SCR-36 | Partner scorecard | Partner portal |
| RW-AUDIT | Internal audit | SCR-37 | Steering dashboard | Reporting |
| RW-AUDIT | Internal audit | SCR-38 | Decision log query | Decision log |
| RW-AUDIT | Internal audit | SCR-39 | Rules and parameters | Rules and parameters |
| RW-AUDIT | Internal audit | SCR-40 | Reference data | Reference data |
| RW-AUDIT | Internal audit | SCR-41 | Delegation of authority | Rules and parameters |
| RW-AUDIT | Internal audit | SCR-42 | Queues and service levels | Queue and allocation |
| RW-AUDIT | Internal audit | SCR-43 | Roles and access | Platform administration |
| RW-AUDIT | Internal audit | SCR-44 | Interface and job monitor | Platform administration |
| RW-AUDIT | Internal audit | SCR-45 | Data quality | Platform administration |
| RW-AUDIT | Internal audit | SCR-46 | Agent monitor | Platform administration |
| RW-AUDIT | Internal audit | SCR-47 | Personal data | Platform administration |
| RW-COMPLY | Compliance and PDPA officer | SCR-01 | My work | Case record |
| RW-COMPLY | Compliance and PDPA officer | SCR-02 | Case list | Case record |
| RW-COMPLY | Compliance and PDPA officer | SCR-03 | Case record | Case record |
| RW-COMPLY | Compliance and PDPA officer | SCR-04 | Case timeline | Case record |
| RW-COMPLY | Compliance and PDPA officer | SCR-06 | Raise deviation | Case record |
| RW-COMPLY | Compliance and PDPA officer | SCR-08 | Deviation queue | Case record |
| RW-COMPLY | Compliance and PDPA officer | SCR-10 | Approval queue | Decision log |
| RW-COMPLY | Compliance and PDPA officer | SCR-11 | Decision screen | Decision log |
| RW-COMPLY | Compliance and PDPA officer | SCR-12 | Committee pack | Decision log |
| RW-COMPLY | Compliance and PDPA officer | SCR-18 | Notice approval | Litigation |
| RW-COMPLY | Compliance and PDPA officer | SCR-19 | Litigation workspace | Litigation |
| RW-COMPLY | Compliance and PDPA officer | SCR-20 | Enforcement workspace | Litigation |
| RW-COMPLY | Compliance and PDPA officer | SCR-30 | Case documents | Documents |
| RW-COMPLY | Compliance and PDPA officer | SCR-31 | Document review queue | Documents |
| RW-COMPLY | Compliance and PDPA officer | SCR-32 | Document custody | Documents |
| RW-COMPLY | Compliance and PDPA officer | SCR-33 | Template approval | Documents |
| RW-COMPLY | Compliance and PDPA officer | SCR-34 | Partner list | Partner portal |
| RW-COMPLY | Compliance and PDPA officer | SCR-35 | Placement and allocation | Partner portal |
| RW-COMPLY | Compliance and PDPA officer | SCR-36 | Partner scorecard | Partner portal |
| RW-COMPLY | Compliance and PDPA officer | SCR-37 | Steering dashboard | Reporting |
| RW-COMPLY | Compliance and PDPA officer | SCR-38 | Decision log query | Decision log |
| RW-COMPLY | Compliance and PDPA officer | SCR-39 | Rules and parameters | Rules and parameters |
| RW-COMPLY | Compliance and PDPA officer | SCR-40 | Reference data | Reference data |
| RW-COMPLY | Compliance and PDPA officer | SCR-41 | Delegation of authority | Rules and parameters |
| RW-COMPLY | Compliance and PDPA officer | SCR-43 | Roles and access | Platform administration |
| RW-COMPLY | Compliance and PDPA officer | SCR-44 | Interface and job monitor | Platform administration |
| RW-COMPLY | Compliance and PDPA officer | SCR-45 | Data quality | Platform administration |
| RW-COMPLY | Compliance and PDPA officer | SCR-46 | Agent monitor | Platform administration |
| RW-COMPLY | Compliance and PDPA officer | SCR-47 | Personal data | Platform administration |
| RW-PLATADM | Platform administrator | SCR-01 | My work | Case record |
| RW-PLATADM | Platform administrator | SCR-02 | Case list | Case record |
| RW-PLATADM | Platform administrator | SCR-03 | Case record | Case record |
| RW-PLATADM | Platform administrator | SCR-04 | Case timeline | Case record |
| RW-PLATADM | Platform administrator | SCR-05 | Transfer case | Queue and allocation |
| RW-PLATADM | Platform administrator | SCR-06 | Raise deviation | Case record |
| RW-PLATADM | Platform administrator | SCR-07 | Team queues | Queue and allocation |
| RW-PLATADM | Platform administrator | SCR-08 | Deviation queue | Case record |
| RW-PLATADM | Platform administrator | SCR-09 | Exception queue | Queue and allocation |
| RW-PLATADM | Platform administrator | SCR-10 | Approval queue | Decision log |
| RW-PLATADM | Platform administrator | SCR-11 | Decision screen | Decision log |
| RW-PLATADM | Platform administrator | SCR-12 | Committee pack | Decision log |
| RW-PLATADM | Platform administrator | SCR-30 | Case documents | Documents |
| RW-PLATADM | Platform administrator | SCR-31 | Document review queue | Documents |
| RW-PLATADM | Platform administrator | SCR-32 | Document custody | Documents |
| RW-PLATADM | Platform administrator | SCR-33 | Template approval | Documents |
| RW-PLATADM | Platform administrator | SCR-34 | Partner list | Partner portal |
| RW-PLATADM | Platform administrator | SCR-35 | Placement and allocation | Partner portal |
| RW-PLATADM | Platform administrator | SCR-36 | Partner scorecard | Partner portal |
| RW-PLATADM | Platform administrator | SCR-37 | Steering dashboard | Reporting |
| RW-PLATADM | Platform administrator | SCR-38 | Decision log query | Decision log |
| RW-PLATADM | Platform administrator | SCR-39 | Rules and parameters | Rules and parameters |
| RW-PLATADM | Platform administrator | SCR-40 | Reference data | Reference data |
| RW-PLATADM | Platform administrator | SCR-41 | Delegation of authority | Rules and parameters |
| RW-PLATADM | Platform administrator | SCR-42 | Queues and service levels | Queue and allocation |
| RW-PLATADM | Platform administrator | SCR-43 | Roles and access | Platform administration |
| RW-PLATADM | Platform administrator | SCR-44 | Interface and job monitor | Platform administration |
| RW-PLATADM | Platform administrator | SCR-45 | Data quality | Platform administration |
| RW-PLATADM | Platform administrator | SCR-46 | Agent monitor | Platform administration |
| RW-PLATADM | Platform administrator | SCR-47 | Personal data | Platform administration |
| RW-REFADM | Reference data administrator | SCR-10 | Approval queue | Decision log |
| RW-REFADM | Reference data administrator | SCR-11 | Decision screen | Decision log |
| RW-REFADM | Reference data administrator | SCR-12 | Committee pack | Decision log |
| RW-REFADM | Reference data administrator | SCR-37 | Steering dashboard | Reporting |
| RW-REFADM | Reference data administrator | SCR-38 | Decision log query | Decision log |
| RW-REFADM | Reference data administrator | SCR-39 | Rules and parameters | Rules and parameters |
| RW-REFADM | Reference data administrator | SCR-40 | Reference data | Reference data |
| RW-REFADM | Reference data administrator | SCR-41 | Delegation of authority | Rules and parameters |
| RW-SECADM | Security administrator | SCR-10 | Approval queue | Decision log |
| RW-SECADM | Security administrator | SCR-11 | Decision screen | Decision log |
| RW-SECADM | Security administrator | SCR-12 | Committee pack | Decision log |
| RW-SECADM | Security administrator | SCR-37 | Steering dashboard | Reporting |
| RW-SECADM | Security administrator | SCR-38 | Decision log query | Decision log |
| RW-SECADM | Security administrator | SCR-39 | Rules and parameters | Rules and parameters |
| RW-SECADM | Security administrator | SCR-40 | Reference data | Reference data |
| RW-SECADM | Security administrator | SCR-41 | Delegation of authority | Rules and parameters |
| RW-SECADM | Security administrator | SCR-43 | Roles and access | Platform administration |
| RW-SECADM | Security administrator | SCR-44 | Interface and job monitor | Platform administration |
| RW-SECADM | Security administrator | SCR-45 | Data quality | Platform administration |
| RW-SECADM | Security administrator | SCR-46 | Agent monitor | Platform administration |
| RW-SECADM | Security administrator | SCR-47 | Personal data | Platform administration |
| RW-BIANAL | Reporting and BI analyst | SCR-01 | My work | Case record |
| RW-BIANAL | Reporting and BI analyst | SCR-02 | Case list | Case record |
| RW-BIANAL | Reporting and BI analyst | SCR-03 | Case record | Case record |
| RW-BIANAL | Reporting and BI analyst | SCR-04 | Case timeline | Case record |
| RW-BIANAL | Reporting and BI analyst | SCR-05 | Transfer case | Queue and allocation |
| RW-BIANAL | Reporting and BI analyst | SCR-06 | Raise deviation | Case record |
| RW-BIANAL | Reporting and BI analyst | SCR-07 | Team queues | Queue and allocation |
| RW-BIANAL | Reporting and BI analyst | SCR-08 | Deviation queue | Case record |
| RW-BIANAL | Reporting and BI analyst | SCR-09 | Exception queue | Queue and allocation |
| RW-BIANAL | Reporting and BI analyst | SCR-10 | Approval queue | Decision log |
| RW-BIANAL | Reporting and BI analyst | SCR-11 | Decision screen | Decision log |
| RW-BIANAL | Reporting and BI analyst | SCR-12 | Committee pack | Decision log |
| RW-BIANAL | Reporting and BI analyst | SCR-13 | Route decision | Treatment and offer |
| RW-BIANAL | Reporting and BI analyst | SCR-14 | Treatment record | Treatment and offer |
| RW-BIANAL | Reporting and BI analyst | SCR-15 | Settlement offer | Treatment and offer |
| RW-BIANAL | Reporting and BI analyst | SCR-16 | Deed in lieu | Treatment and offer |
| RW-BIANAL | Reporting and BI analyst | SCR-17 | Guarantee claim | Treatment and offer |
| RW-BIANAL | Reporting and BI analyst | SCR-18 | Notice approval | Litigation |
| RW-BIANAL | Reporting and BI analyst | SCR-19 | Litigation workspace | Litigation |
| RW-BIANAL | Reporting and BI analyst | SCR-20 | Enforcement workspace | Litigation |
| RW-BIANAL | Reporting and BI analyst | SCR-21 | Asset list | Asset and disposal |
| RW-BIANAL | Reporting and BI analyst | SCR-22 | Asset record | Asset and disposal |
| RW-BIANAL | Reporting and BI analyst | SCR-23 | Listing and price | Asset and disposal |
| RW-BIANAL | Reporting and BI analyst | SCR-24 | Auction rounds | Asset and disposal |
| RW-BIANAL | Reporting and BI analyst | SCR-25 | Lot builder | Debt sale |
| RW-BIANAL | Reporting and BI analyst | SCR-26 | Award | Debt sale |
| RW-BIANAL | Reporting and BI analyst | SCR-27 | Write-off proposal | Write-off and posting |
| RW-BIANAL | Reporting and BI analyst | SCR-28 | Proceeds matching | Write-off and posting |
| RW-BIANAL | Reporting and BI analyst | SCR-29 | Posting | Write-off and posting |
| RW-BIANAL | Reporting and BI analyst | SCR-34 | Partner list | Partner portal |
| RW-BIANAL | Reporting and BI analyst | SCR-35 | Placement and allocation | Partner portal |
| RW-BIANAL | Reporting and BI analyst | SCR-36 | Partner scorecard | Partner portal |
| RW-BIANAL | Reporting and BI analyst | SCR-37 | Steering dashboard | Reporting |
| RW-BIANAL | Reporting and BI analyst | SCR-38 | Decision log query | Decision log |
| RW-BIANAL | Reporting and BI analyst | SCR-39 | Rules and parameters | Rules and parameters |
| RW-BIANAL | Reporting and BI analyst | SCR-40 | Reference data | Reference data |
| RW-BIANAL | Reporting and BI analyst | SCR-41 | Delegation of authority | Rules and parameters |
| RW-BIANAL | Reporting and BI analyst | SCR-42 | Queues and service levels | Queue and allocation |
| RW-TRIBE | Tribe lead and squad members | SCR-01 | My work | Case record |
| RW-TRIBE | Tribe lead and squad members | SCR-02 | Case list | Case record |
| RW-TRIBE | Tribe lead and squad members | SCR-03 | Case record | Case record |
| RW-TRIBE | Tribe lead and squad members | SCR-04 | Case timeline | Case record |
| RW-TRIBE | Tribe lead and squad members | SCR-05 | Transfer case | Queue and allocation |
| RW-TRIBE | Tribe lead and squad members | SCR-06 | Raise deviation | Case record |
| RW-TRIBE | Tribe lead and squad members | SCR-07 | Team queues | Queue and allocation |
| RW-TRIBE | Tribe lead and squad members | SCR-08 | Deviation queue | Case record |
| RW-TRIBE | Tribe lead and squad members | SCR-09 | Exception queue | Queue and allocation |
| RW-TRIBE | Tribe lead and squad members | SCR-10 | Approval queue | Decision log |
| RW-TRIBE | Tribe lead and squad members | SCR-11 | Decision screen | Decision log |
| RW-TRIBE | Tribe lead and squad members | SCR-12 | Committee pack | Decision log |
| RW-TRIBE | Tribe lead and squad members | SCR-13 | Route decision | Treatment and offer |
| RW-TRIBE | Tribe lead and squad members | SCR-14 | Treatment record | Treatment and offer |
| RW-TRIBE | Tribe lead and squad members | SCR-15 | Settlement offer | Treatment and offer |
| RW-TRIBE | Tribe lead and squad members | SCR-16 | Deed in lieu | Treatment and offer |
| RW-TRIBE | Tribe lead and squad members | SCR-17 | Guarantee claim | Treatment and offer |
| RW-TRIBE | Tribe lead and squad members | SCR-18 | Notice approval | Litigation |
| RW-TRIBE | Tribe lead and squad members | SCR-19 | Litigation workspace | Litigation |
| RW-TRIBE | Tribe lead and squad members | SCR-20 | Enforcement workspace | Litigation |
| RW-TRIBE | Tribe lead and squad members | SCR-21 | Asset list | Asset and disposal |
| RW-TRIBE | Tribe lead and squad members | SCR-22 | Asset record | Asset and disposal |
| RW-TRIBE | Tribe lead and squad members | SCR-23 | Listing and price | Asset and disposal |
| RW-TRIBE | Tribe lead and squad members | SCR-24 | Auction rounds | Asset and disposal |
| RW-TRIBE | Tribe lead and squad members | SCR-25 | Lot builder | Debt sale |
| RW-TRIBE | Tribe lead and squad members | SCR-26 | Award | Debt sale |
| RW-TRIBE | Tribe lead and squad members | SCR-27 | Write-off proposal | Write-off and posting |
| RW-TRIBE | Tribe lead and squad members | SCR-28 | Proceeds matching | Write-off and posting |
| RW-TRIBE | Tribe lead and squad members | SCR-29 | Posting | Write-off and posting |
| RW-TRIBE | Tribe lead and squad members | SCR-30 | Case documents | Documents |
| RW-TRIBE | Tribe lead and squad members | SCR-31 | Document review queue | Documents |
| RW-TRIBE | Tribe lead and squad members | SCR-32 | Document custody | Documents |
| RW-TRIBE | Tribe lead and squad members | SCR-33 | Template approval | Documents |
| RW-TRIBE | Tribe lead and squad members | SCR-34 | Partner list | Partner portal |
| RW-TRIBE | Tribe lead and squad members | SCR-35 | Placement and allocation | Partner portal |
| RW-TRIBE | Tribe lead and squad members | SCR-36 | Partner scorecard | Partner portal |
| RW-TRIBE | Tribe lead and squad members | SCR-37 | Steering dashboard | Reporting |
| RW-TRIBE | Tribe lead and squad members | SCR-38 | Decision log query | Decision log |
| RW-TRIBE | Tribe lead and squad members | SCR-39 | Rules and parameters | Rules and parameters |
| RW-TRIBE | Tribe lead and squad members | SCR-40 | Reference data | Reference data |
| RW-TRIBE | Tribe lead and squad members | SCR-41 | Delegation of authority | Rules and parameters |
| RW-TRIBE | Tribe lead and squad members | SCR-42 | Queues and service levels | Queue and allocation |
| PT-AGENCY | Collection agency (OA) user | PRT-01 | Partner home | Partner portal |
| PT-AGENCY | Collection agency (OA) user | PRT-02 | Instruction | Partner portal |
| PT-AGENCY | Collection agency (OA) user | PRT-03 | Upload result | Partner portal |
| PT-AGENCY | Collection agency (OA) user | PRT-04 | Invoice | Partner portal |
| PT-AGENCY | Collection agency (OA) user | PRT-05 | Data room | Partner portal |
| PT-AGENCY | Collection agency (OA) user | PRT-06 | Transfer confirmation | Partner portal |
| PT-LAWFIRM | Law firm user | PRT-01 | Partner home | Partner portal |
| PT-LAWFIRM | Law firm user | PRT-02 | Instruction | Partner portal |
| PT-LAWFIRM | Law firm user | PRT-03 | Upload result | Partner portal |
| PT-LAWFIRM | Law firm user | PRT-04 | Invoice | Partner portal |
| PT-LAWFIRM | Law firm user | PRT-05 | Data room | Partner portal |
| PT-LAWFIRM | Law firm user | PRT-06 | Transfer confirmation | Partner portal |
| PT-VALUER | Valuer | PRT-01 | Partner home | Partner portal |
| PT-VALUER | Valuer | PRT-02 | Instruction | Partner portal |
| PT-VALUER | Valuer | PRT-03 | Upload result | Partner portal |
| PT-VALUER | Valuer | PRT-04 | Invoice | Partner portal |
| PT-VALUER | Valuer | PRT-05 | Data room | Partner portal |
| PT-VALUER | Valuer | PRT-06 | Transfer confirmation | Partner portal |
| PT-AUCTION | Auction vendor | PRT-01 | Partner home | Partner portal |
| PT-AUCTION | Auction vendor | PRT-02 | Instruction | Partner portal |
| PT-AUCTION | Auction vendor | PRT-03 | Upload result | Partner portal |
| PT-AUCTION | Auction vendor | PRT-04 | Invoice | Partner portal |
| PT-AUCTION | Auction vendor | PRT-05 | Data room | Partner portal |
| PT-AUCTION | Auction vendor | PRT-06 | Transfer confirmation | Partner portal |
| PT-BUYER | Debt buyer and AMC | PRT-01 | Partner home | Partner portal |
| PT-BUYER | Debt buyer and AMC | PRT-02 | Instruction | Partner portal |
| PT-BUYER | Debt buyer and AMC | PRT-03 | Upload result | Partner portal |
| PT-BUYER | Debt buyer and AMC | PRT-04 | Invoice | Partner portal |
| PT-BUYER | Debt buyer and AMC | PRT-05 | Data room | Partner portal |
| PT-BUYER | Debt buyer and AMC | PRT-06 | Transfer confirmation | Partner portal |
| PT-RAMC | RAMC user | PRT-01 | Partner home | Partner portal |
| PT-RAMC | RAMC user | PRT-02 | Instruction | Partner portal |
| PT-RAMC | RAMC user | PRT-03 | Upload result | Partner portal |
| PT-RAMC | RAMC user | PRT-04 | Invoice | Partner portal |
| PT-RAMC | RAMC user | PRT-05 | Data room | Partner portal |
| PT-RAMC | RAMC user | PRT-06 | Transfer confirmation | Partner portal |

## Common states

| States every screen handles |  |
|---|---|
| The wording comes from the error and message standard. |  |
| State | How it shows |
| Loading | Skeleton rows while data arrives; no spinner over the whole page |
| Empty | A plain sentence saying there is nothing to show, and the action to take if one applies |
| Read only | Fields shown without edit controls; the reason is shown when the role cannot change them |
| On hold | A banner with the deviation or legal hold and the prescription date |
| Stale input | A warning with the age of the data (MSG-P7-006, MSG-P1-001) |
| Error | The message from the error and message standard next to the field or at the top |

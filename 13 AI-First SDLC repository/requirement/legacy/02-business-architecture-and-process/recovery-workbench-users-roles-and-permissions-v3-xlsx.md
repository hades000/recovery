<!-- source: 02 Business architecture and process/Recovery Workbench Users Roles and Permissions v3.xlsx -->
<!-- converted: 2026-11-04 from XLSX -->

> **Source:** `02 Business architecture and process/Recovery Workbench Users Roles and Permissions v3.xlsx`  
> **Converted from:** XLSX

## Roles

| Users and roles |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|
| 54 roles: 37 bank users, 7 partner users, 4 customer parties and 6 non-human actors. One row is one role, held as data in the roles table. |  |  |  |  |  |  |  |  |  |
| Role code | Role name | Class | Group | Unit or organization | What the role does | L1 processes | Main screens | Default scope | First release with real users |
| RW-CASEOWN | Case owner | Bank user | Shared operations | Shared operations | Owns the case from day 90 to close. Accepts the hand-over, reads expected net recovery after cost per route, approves inside the limit, answers for ageing against the service level | 06 to 10 | Case list, case record, my queue | Own | E2 |
| RW-TEAMMGR | Team manager | Bank user | Shared operations | Shared operations | Runs the team: allocation overrides, reassignment, caseload and service level breaches, coaching, the spread between collectors | 06 to 10 | Team queues, transfer screen, queue measures | Team | E2 |
| RW-PHONECOL | Phone collector | Bank user | Shared operations | Shared operations | Works the pre-90 list on EFS. Reads the case record for accounts that have moved to recovery so the customer is not called twice | pre-06 | Case record read only | Own | E2 |
| RW-FIELDCOL | Field collector | Bank user | Shared operations | Shared operations, field | Visits the customer or the asset, captures photos, bills and signed documents into the case through the field app | 06, 09 | Field app intake, case record | Own | E7 |
| RW-RESTRUCT | Restructuring officer (FCR) | Bank user | Shared operations | FCR, restructuring | Builds and sends the restructure offer inside the band, records affordability, books the plan. Exceptions only reach a person | 07 | Treatment screen, offer builder, plan view | Team | E3 |
| RW-SPECIAL | Hardship and vulnerability specialist | Bank user | Shared operations | Shared operations | Takes cases flagged X2 or X3, sets contact limits, decides a hardship plan or a BOT relief program | 11 deviations | Deviation queue, case record | Team | E7 |
| RW-COMPLAIN | Complaint officer | Bank user | Shared operations | Conduct, shared operations | Takes X1 disputes and complaints, applies the contact stop, builds the evidence pack, resolves inside the service level and returns the case to the same decision | 11 deviations | Deviation queue, contact stop | Team | E7 |
| RW-FRAUD | Fraud investigator | Bank user | Control functions and committees | Fraud | Takes X4 referrals, investigates, confirms or clears, which sends the case to D9 or back to D2 | 11 deviations | Deviation queue, case record | All | E7 |
| RW-LITOFF | Litigation officer | Bank user | Shared operations | Legal and litigation | Checks the agent-assembled case pack against the defect list, instructs the law firm, files, manages to judgment | 08 | Litigation workspace, case pack, panel scorecard | Team | E2 |
| RW-ENFORCE | Enforcement owner | Bank user | Shared operations | Legal and litigation | Owns enforcement after judgment: seizure, LED auction entry, or a coded deferral with its reason. One of the three points with no owner today | 08 | Enforcement workspace, LED tracker | Team | E5 |
| RW-LEGAL | Legal counsel | Bank user | Control functions and committees | Legal | Approves notice and contract templates, rules on estate and bankruptcy claims, joins X3 and X5 deviations | 08, 11 | Template approval, deviation queue | All | E3 |
| RW-SALEOFF | Sale officer | Bank user | Shared operations | Shared operations with the product head | Runs the auction schedule, the listing and the price ladder, approves inside the floor, sends anything below it for a second signature | 09 | Asset list, listing, price ladder, bid review | Team | E3 |
| RW-NPAMGR | NPA and asset manager | Bank user | Shared operations | Asset liquidity | Holds and manages repossessed assets: custody, insurance, maintenance, the stock balance. The stock balance is one of the three unowned points today | 09 | Asset list, holding cost, stock balance | Team | E3 |
| RW-DEBTSALE | Debt sale officer | Bank user | Shared operations | Asset liquidity | Builds the lots, sets the reserve from the model, runs the buyer process, transfers the data on award | 09 | Lot builder, buyer portal admin, award screen | Team | E6 |
| RW-WRITEOFF | Write-off team member | Bank user | Shared operations | Credit administration | Runs the monthly scan on both tracks, proposes the population, prepares the committee pack | 10 | Write-off proposal, committee pack | Team | E6 |
| RW-CREDITAD | Credit Administration officer | Bank user | Shared operations | Credit administration | Posts the approved write-off, releases the provision, publishes completeness, records post charge-off recovery | 10 | Posting screen, completeness report | Team | E3 |
| RW-GUARANT | Guarantee officer | Bank user | Shared operations | Shared operations | Files and tracks TCG and insurance claims, records the subrogation position | 07 | Guarantee claim workspace | Team | E4 |
| RW-AGENCYMG | Partner and agency manager | Bank user | Shared operations | OA management team | Runs every partner type on the same six points: selection, contract and fees, targets and incentives, data exchange, performance reviews, notice and exit. Sets placements by measured return | 06 to 10, 12 | Partner portal, scorecard, placement screen | All | E6 |
| RW-CONDUCT | Conduct and QA officer | Bank user | Center of excellence | Conduct, center of excellence | Reviews contacts blocked by the contact check, matches complaints to the preceding contact, samples decisions against the rule version applied | all | Conduct review, QA sample, contact log | All | E8 |
| RW-CAPACITY | Capacity and workforce planner | Bank user | Shared operations | Shared operations | Sets next week's roster from inflow by product, bucket and region, the answer curve and the field coverage map. A role with no structure chart today | all | Capacity planner, inflow forecast | All | E2 |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | Bank user | Product heads | Product | Owns approval limits for the product, approves above the case owner limit, owns the floor price and the band | 07 to 10 | Approval queue, delegation view | All | E2 |
| RW-HEADLIT | Head of Litigation | Bank user | Shared operations | Legal and litigation | Approves legal spend above the limit, rules on panel conflicts and escalations | 08 | Approval queue, panel console | All | E2 |
| RW-HEADNPA | Head of NPA | Bank user | Shared operations | Asset liquidity | Approves holding, price steps below the floor and transfers to RAMC | 09 | Approval queue, asset list | All | E3 |
| RW-HEADASL | Head of Asset Liquidity | Bank user | Shared operations | Asset liquidity | Approves lots, reserve prices and buyer panel changes | 09 | Approval queue, lot builder | All | E6 |
| RW-CREDCOMM | Credit approval committee member | Bank user | Control functions and committees | Credit | Approves restructures and settlements above the delegated limit | 07 | Approval queue, committee pack | All | E4 |
| RW-WOCOMM | Write-off committee member | Bank user | Control functions and committees | Credit, Finance, Risk | Approves the write-off population inside the delegation, rules on the exception loop | 10 | Committee pack, approval queue | All | E6 |
| RW-RISK | Risk and model risk officer | Bank user | Control functions and committees | Risk | Reviews drift and calibration, raises a decision with an owner and a date on a breach, signs rule version changes | all | Model monitor, rule version log | All | E2 |
| RW-COE | Center of excellence analyst | Bank user | Center of excellence | Center of excellence | Owns the rule tables, the parameter catalog, the measure definitions and the QA program. Loads and rolls back rule versions | all | Rule console, parameter catalog, reference data | All | E1 |
| RW-DATASTEW | Data steward and data product owner | Bank user | Platform | Data and analytics | Owns a data product: definition, quality rules, freshness, access. Signs the daily reconciliation to ALS | all | Data quality console, catalog, reconciliation report | All | E1 |
| RW-FINANCE | Finance and CFO delegate | Bank user | Control functions and committees | Finance | Reviews benefit realisation monthly, owns the provision and posting rules | 10 | Benefit dashboard, posting report | All | E6 |
| RW-AUDIT | Internal audit | Bank user | Control functions and committees | Audit | Queries the decision log, samples cases, tests that every action carries a rule version and an approver | all | Decision log query, audit export | All | E1 |
| RW-COMPLY | Compliance and PDPA officer | Bank user | Control functions and committees | Compliance | Rules on data subject requests, consent, retention and masking. Approves regulatory reporting content | all | PDPA console, retention classes, consent log | All | E1 |
| RW-PLATADM | Platform administrator | Bank user | Platform | TechX platform | Runs the environment: configuration service, feature flags, jobs, interfaces, incident handling, break-glass | all | Admin console, job monitor, interface monitor | All | E1 |
| RW-REFADM | Reference data administrator | Bank user | Center of excellence | Center of excellence | Maintains the versioned reference tables: queues, roles, templates, document checklists, action codes, product parameters | all | Reference data service, versioned tables | All | E1 |
| RW-SECADM | Security administrator | Bank user | Control functions and committees | SCB IT security | Owns the role to permission matrix, joiner mover leaver, break-glass approval, the access log | all | Access admin, permission matrix, access log | All | E1 |
| RW-BIANAL | Reporting and BI analyst | Bank user | Platform | Data and analytics | Builds and runs the steering dashboard, the queue measures and the regulatory extracts | all | Power BI workspace, report builder | All | E2 |
| RW-TRIBE | Tribe lead and squad members | Bank user | Platform | Collections and Recovery Tribe | Run the weekly squad review, own the backlog and the release train | all | Backlog, release board | All | E2 |
| PT-AGENCY | Collection agency (OA) user | Partner user | Partner user | 73 agencies on a fixed 20 percent share | Receives placements, records contact outcomes and payments, returns the account at recall or panel exit | 06, 10 | Partner portal: placement list, outcome capture | Placed cases | E6 |
| PT-LAWFIRM | Law firm user | Partner user | Partner user | 11 to 12 firms on the panel | Receives the instruction and the case pack, files, reports court state and hearing dates, invoices against the fee schedule | 08 | Partner portal: instruction, court state, invoice | Placed cases | E5 |
| PT-VALUER | Valuer | Partner user | Partner user | Panel valuers | Receives the valuation instruction, uploads the report and the value, which feeds the band and the floor | 07, 09 | Partner portal: instruction, report upload | Placed cases | E4 |
| PT-AUCTION | Auction vendor | Partner user | Partner user | 4 vendors allocated by distance | Runs the auction rounds on the ladder, reports results per round, settles proceeds | 09 | Partner portal: schedule, round result, settlement | Placed cases | E4 |
| PT-BUYER | Debt buyer and AMC | Partner user | Partner user | 35 buyers | Qualifies, views the lot data room, bids, receives the data transfer on award, confirms remittance | 09 | Partner portal: data room, bid, award, transfer | Placed cases | E5 |
| PT-RAMC | RAMC user | Partner user | Partner user | SCB asset management company | Takes the transfer of assets and accounts that move to RAMC and confirms the position | 09 | Partner portal: transfer, confirmation | Placed cases | E4 |
| PT-LED | Legal Execution Department and court officer | Partner user | Partner user | Government | Runs the enforcement auction on the 100 / 90 / 80 / 70 percent ladder and issues the official value. Reached by interface and filing, not by a Workbench login | 08, 09 | No login: filing and result interfaces | Placed cases | No login |
| CU-BORROW | Customer (borrower) | Customer party | Customer party | Retail and SSME customers | Is told who owns the case, supplies documents, accepts or declines an offer, signs, pays, hands over an asset | 06 to 10 | Notices, HOME.SCB, e-signature link | Own case | E4 self-service through bank channels |
| CU-GUARANT | Guarantor and co-borrower | Customer party | Customer party | Connected parties | Receives the demand, answers it, may pay, settle or be pursued | 07, 08 | Notices, e-signature link | Own case | Through bank channels |
| CU-HEIR | Heir and estate representative | Customer party | Customer party | Connected parties | Is notified on a death, supplies the certificate, deals with the estate claim | 11 deviations | Notices | Own case | Through bank channels |
| CU-BIDDER | Retail asset bidder | Customer party | Customer party | Public | Views the listing and bids in an auction round | 09 | Public listing, auction portal | Own case | Through bank channels |
| SY-CASEWF | Case workflow module | Non-human actor | Non-human actor | Recovery module | Holds the case state, runs every stage clock, timer, escalation and prescription date, and moves the case on each rule result | all | None | All | E1 |
| SY-RULES | Rules component | Non-human actor | Non-human actor | Recovery module | Evaluates the versioned rule tables for allocation, assignment, transfer, route and approval routing | all | None | All | E1 |
| SY-DATALOAD | Data load from COLLINS | Non-human actor | Non-human actor | Recovery module | Loads and checks the COLLINS batch and the file loads, and writes the outbound files | all | None | All | E1 |
| SY-OCR | OCR and extraction pipeline | Non-human actor | Non-human actor | Autonomous Ops | Classifies an incoming document, extracts its fields into the index and attaches it to the case | all | Review queue for low confidence | All | E1 |
| SY-DECLOG | Decision log writer | Non-human actor | Non-human actor | Recovery module | Writes an append-only, hash-chained entry for every decision with the rule ID and version, the inputs and the approver | all | None | All | E1 |
| SY-AGENT | Agent platform | Non-human actor | Non-human actor | Enterprise AI | Runs the recovery agents through the tool gateway at autonomy levels L0 to L4 | all | Agent monitor | All | E1 |

## Permissions

| Permission matrix |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Each role against the 14 capability areas. C create, R read, U update, D delete, A approve, a dash for none. Every approve right works within the delegation of authority table. |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Role code | Role name | Class | Case record | Queue and allocation | Treatment and offer | Litigation | Asset and disposal | Debt sale | Write-off and posting | Documents | Rules and parameters | Reference data | Decision log | Partner portal | Reporting | Platform administration |
| RW-CASEOWN | Case owner | Bank user | CRU | R | CRU | R | R | - | - | CRU | R | R | R | R | R | - |
| RW-TEAMMGR | Team manager | Bank user | R | CRUA | R | R | R | - | - | R | R | R | R | R | R | - |
| RW-PHONECOL | Phone collector | Bank user | R | R | - | - | - | - | - | R | - | R | - | - | R | - |
| RW-FIELDCOL | Field collector | Bank user | R | R | - | - | R | - | - | CR | - | R | - | - | - | - |
| RW-RESTRUCT | Restructuring officer (FCR) | Bank user | RU | R | CRUA | - | - | - | - | CRU | R | R | R | - | R | - |
| RW-SPECIAL | Hardship and vulnerability specialist | Bank user | RU | R | CRU | - | - | - | - | CRU | R | R | R | - | R | - |
| RW-COMPLAIN | Complaint officer | Bank user | RU | R | R | R | R | - | - | CRU | R | R | R | - | R | - |
| RW-FRAUD | Fraud investigator | Bank user | RU | R | R | R | - | - | R | CRU | R | R | R | - | R | - |
| RW-LITOFF | Litigation officer | Bank user | RU | R | R | CRUA | R | - | - | CRU | R | R | R | CRU | R | - |
| RW-ENFORCE | Enforcement owner | Bank user | RU | R | - | CRU | CRU | - | - | CRU | R | R | R | CRU | R | - |
| RW-LEGAL | Legal counsel | Bank user | R | - | R | RA | R | - | - | CRUA | R | RU | R | R | R | - |
| RW-SALEOFF | Sale officer | Bank user | RU | R | - | R | CRUA | R | - | CRU | R | R | R | CRU | R | - |
| RW-NPAMGR | NPA and asset manager | Bank user | R | - | - | R | CRU | R | - | CRU | R | R | R | CRU | R | - |
| RW-DEBTSALE | Debt sale officer | Bank user | RU | R | - | R | R | CRUA | R | CRU | R | R | R | CRU | R | - |
| RW-WRITEOFF | Write-off team member | Bank user | R | - | - | R | R | R | CRU | CRU | R | R | R | - | R | - |
| RW-CREDITAD | Credit Administration officer | Bank user | R | - | - | R | R | R | CRUA | CRU | R | R | R | - | R | - |
| RW-GUARANT | Guarantee officer | Bank user | RU | R | CRU | R | - | - | - | CRU | R | R | R | CRU | R | - |
| RW-AGENCYMG | Partner and agency manager | Bank user | R | R | - | R | R | R | - | R | R | RU | R | CRUDA | R | - |
| RW-CONDUCT | Conduct and QA officer | Bank user | R | R | R | R | R | R | R | R | R | R | R | R | R | - |
| RW-CAPACITY | Capacity and workforce planner | Bank user | R | RU | - | - | - | - | - | - | R | R | - | R | R | - |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | Bank user | R | R | RA | RA | RA | RA | RA | R | R | R | R | R | R | - |
| RW-HEADLIT | Head of Litigation | Bank user | R | R | - | RA | R | - | - | R | R | R | R | RA | R | - |
| RW-HEADNPA | Head of NPA | Bank user | R | - | - | R | RA | R | - | R | R | R | R | RA | R | - |
| RW-HEADASL | Head of Asset Liquidity | Bank user | R | - | - | R | RA | RA | - | R | R | R | R | RA | R | - |
| RW-CREDCOMM | Credit approval committee member | Bank user | R | - | RA | - | - | - | - | R | R | R | R | - | R | - |
| RW-WOCOMM | Write-off committee member | Bank user | R | - | - | - | - | - | RA | R | R | R | R | - | R | - |
| RW-RISK | Risk and model risk officer | Bank user | R | R | R | R | R | R | R | R | RA | R | R | R | R | - |
| RW-COE | Center of excellence analyst | Bank user | R | R | R | R | R | R | R | R | CRUD | CRUD | R | R | R | R |
| RW-DATASTEW | Data steward and data product owner | Bank user | R | - | - | - | - | - | - | R | R | RU | R | - | CRU | R |
| RW-FINANCE | Finance and CFO delegate | Bank user | R | - | - | - | R | R | RA | - | R | R | R | - | R | - |
| RW-AUDIT | Internal audit | Bank user | R | R | R | R | R | R | R | R | R | R | R | R | R | R |
| RW-COMPLY | Compliance and PDPA officer | Bank user | R | - | - | R | - | - | - | RU | R | RU | R | R | R | R |
| RW-PLATADM | Platform administrator | Bank user | R | R | - | - | - | - | - | R | R | R | R | R | R | CRUD |
| RW-REFADM | Reference data administrator | Bank user | - | - | - | - | - | - | - | - | R | CRUD | R | - | R | - |
| RW-SECADM | Security administrator | Bank user | - | - | - | - | - | - | - | - | R | R | R | - | R | CRUDA |
| RW-BIANAL | Reporting and BI analyst | Bank user | R | R | R | R | R | R | R | - | R | R | R | R | CRUD | - |
| RW-TRIBE | Tribe lead and squad members | Bank user | R | R | R | R | R | R | R | R | R | R | R | R | R | - |
| PT-AGENCY | Collection agency (OA) user | Partner user | R | - | - | - | - | - | - | CR | - | - | - | RU | - | - |
| PT-LAWFIRM | Law firm user | Partner user | R | - | - | RU | - | - | - | CRU | - | - | - | RU | - | - |
| PT-VALUER | Valuer | Partner user | - | - | - | - | R | - | - | CR | - | - | - | RU | - | - |
| PT-AUCTION | Auction vendor | Partner user | - | - | - | - | RU | - | - | CR | - | - | - | RU | - | - |
| PT-BUYER | Debt buyer and AMC | Partner user | - | - | - | - | - | RU | - | R | - | - | - | RU | - | - |
| PT-RAMC | RAMC user | Partner user | - | - | - | - | RU | R | - | R | - | - | - | RU | - | - |
| PT-LED | Legal Execution Department and court officer | Partner user | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| CU-BORROW | Customer (borrower) | Customer party | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| CU-GUARANT | Guarantor and co-borrower | Customer party | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| CU-HEIR | Heir and estate representative | Customer party | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| CU-BIDDER | Retail asset bidder | Customer party | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| SY-CASEWF | Case workflow module | Non-human actor | CRU | CRU | R | R | R | R | R | R | R | R | C | - | - | - |
| SY-RULES | Rules component | Non-human actor | R | R | R | R | R | R | R | R | R | R | C | - | - | - |
| SY-DATALOAD | Data load from COLLINS | Non-human actor | CU | - | - | U | CU | - | U | - | - | R | C | - | - | - |
| SY-OCR | OCR and extraction pipeline | Non-human actor | R | - | - | - | - | - | - | CRU | - | R | C | - | - | - |
| SY-DECLOG | Decision log writer | Non-human actor | - | - | - | - | - | - | - | - | - | - | C | - | - | - |
| SY-AGENT | Agent platform | Non-human actor | R | R | R | R | R | R | R | R | R | R | C | - | - | - |

## Separation of duty

| Separation of duty |  |  |
|---|---|---|
| Role pairs one person may not hold. Checked by the role owner at each grant and by the Workbench at each sign-in. A person may not approve a decision they proposed or prepared. |  |  |
| Role | May not also hold | Reason |
| Security administrator | Any business role | The person who maps groups to roles could grant themselves business access |
| Platform administrator | Any business role | Technical access combined with business access passes around scope and masking |
| Access administrator position | Role owner for the same roles | One person would approve and carry out the same grant |
| Reference data administrator | Risk and model risk officer | Loading a delegation or rule version and approving it are separate steps |
| Center of excellence analyst | Risk and model risk officer | Writing a rule and approving it are separate steps |
| Restructuring officer | Credit approval committee member | Proposing a restructure and approving it are separate steps |
| Write-off team member | Write-off committee member | Proposing a write-off and approving it are separate steps |
| Internal audit | Any other role | Audit reads and changes nothing |

## Access flow

| Request, grant, review and removal |  |  |  |  |
|---|---|---|---|---|
| Who does what at each step. The review interval, the leaver response time and the break-glass window are DL38. |  |  |  |  |
| Event | Step | Who | Action | Where |
| Joiner | 1 | Line manager | Raises a request naming the person, the role and the reason | Bank IAM |
| Joiner | 2 | Role owner | Approves or rejects, after checking the separation of duty table | Bank IAM |
| Joiner | 3 | Access administrator | Adds the person to the Entra ID group for the role in each environment requested | Bank IAM to Entra ID |
| Joiner | 4 | The person | Signs in with multi-factor authentication | Workbench |
| Joiner | 5 | Workbench | Resolves the roles, scope and masking and writes the session to the access log | Workbench |
| Mover | 1 | Line manager | One request removes the previous roles and adds the new ones in the same change | Bank IAM |
| Mover | 2 | Role owners | The owners of the old and the new roles approve. A mover never holds both sets | Bank IAM |
| Leaver | 1 | Line manager or HR leaver record | Starts removal from every Workbench group | Bank IAM |
| Leaver | 2 | Workbench | Ends the open session at the next request and refuses a new one | Workbench |
| Review | 1 | Role owner | Recertifies every holder of the role at each review. A holder not recertified is removed | Bank IAM |
| Review | 2 | Application owner | Signs the review result | Bank IAM |
| Break-glass | 1 | Platform administrator | Requests access beyond the role, naming the open incident, the area, the scope and the reason | Bank IAM |
| Break-glass | 2 | Security administrator | Approves. A request with no open incident is refused | Bank IAM |
| Break-glass | 3 | Workbench | Marks every action under break-glass in the access log. The grant ends when its window ends | Workbench |
| Break-glass | 4 | Security administrator | Reviews the use inside the review window. An unreviewed use goes to the head of SCB IT security and to Compliance | Bank IAM |

## Single sign-on

| Single sign-on mapping |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| One Entra ID group per role per environment, granted through the bank IAM. Group names follow the pattern shown until SCB IT security issues the bank standard names (DL40). |  |  |  |  |  |  |
| Role code | Role name | Identity | DEV | SIT | UAT | PROD |
| RW-CASEOWN | Case owner | Entra ID group | RWB-DEV-RW-CASEOWN | RWB-SIT-RW-CASEOWN | RWB-UAT-RW-CASEOWN | RWB-PROD-RW-CASEOWN |
| RW-TEAMMGR | Team manager | Entra ID group | RWB-DEV-RW-TEAMMGR | RWB-SIT-RW-TEAMMGR | RWB-UAT-RW-TEAMMGR | RWB-PROD-RW-TEAMMGR |
| RW-PHONECOL | Phone collector | Entra ID group | RWB-DEV-RW-PHONECOL | RWB-SIT-RW-PHONECOL | RWB-UAT-RW-PHONECOL | RWB-PROD-RW-PHONECOL |
| RW-FIELDCOL | Field collector | Entra ID group | RWB-DEV-RW-FIELDCOL | RWB-SIT-RW-FIELDCOL | RWB-UAT-RW-FIELDCOL | RWB-PROD-RW-FIELDCOL |
| RW-RESTRUCT | Restructuring officer (FCR) | Entra ID group | RWB-DEV-RW-RESTRUCT | RWB-SIT-RW-RESTRUCT | RWB-UAT-RW-RESTRUCT | RWB-PROD-RW-RESTRUCT |
| RW-SPECIAL | Hardship and vulnerability specialist | Entra ID group | RWB-DEV-RW-SPECIAL | RWB-SIT-RW-SPECIAL | RWB-UAT-RW-SPECIAL | RWB-PROD-RW-SPECIAL |
| RW-COMPLAIN | Complaint officer | Entra ID group | RWB-DEV-RW-COMPLAIN | RWB-SIT-RW-COMPLAIN | RWB-UAT-RW-COMPLAIN | RWB-PROD-RW-COMPLAIN |
| RW-FRAUD | Fraud investigator | Entra ID group | RWB-DEV-RW-FRAUD | RWB-SIT-RW-FRAUD | RWB-UAT-RW-FRAUD | RWB-PROD-RW-FRAUD |
| RW-LITOFF | Litigation officer | Entra ID group | RWB-DEV-RW-LITOFF | RWB-SIT-RW-LITOFF | RWB-UAT-RW-LITOFF | RWB-PROD-RW-LITOFF |
| RW-ENFORCE | Enforcement owner | Entra ID group | RWB-DEV-RW-ENFORCE | RWB-SIT-RW-ENFORCE | RWB-UAT-RW-ENFORCE | RWB-PROD-RW-ENFORCE |
| RW-LEGAL | Legal counsel | Entra ID group | RWB-DEV-RW-LEGAL | RWB-SIT-RW-LEGAL | RWB-UAT-RW-LEGAL | RWB-PROD-RW-LEGAL |
| RW-SALEOFF | Sale officer | Entra ID group | RWB-DEV-RW-SALEOFF | RWB-SIT-RW-SALEOFF | RWB-UAT-RW-SALEOFF | RWB-PROD-RW-SALEOFF |
| RW-NPAMGR | NPA and asset manager | Entra ID group | RWB-DEV-RW-NPAMGR | RWB-SIT-RW-NPAMGR | RWB-UAT-RW-NPAMGR | RWB-PROD-RW-NPAMGR |
| RW-DEBTSALE | Debt sale officer | Entra ID group | RWB-DEV-RW-DEBTSALE | RWB-SIT-RW-DEBTSALE | RWB-UAT-RW-DEBTSALE | RWB-PROD-RW-DEBTSALE |
| RW-WRITEOFF | Write-off team member | Entra ID group | RWB-DEV-RW-WRITEOFF | RWB-SIT-RW-WRITEOFF | RWB-UAT-RW-WRITEOFF | RWB-PROD-RW-WRITEOFF |
| RW-CREDITAD | Credit Administration officer | Entra ID group | RWB-DEV-RW-CREDITAD | RWB-SIT-RW-CREDITAD | RWB-UAT-RW-CREDITAD | RWB-PROD-RW-CREDITAD |
| RW-GUARANT | Guarantee officer | Entra ID group | RWB-DEV-RW-GUARANT | RWB-SIT-RW-GUARANT | RWB-UAT-RW-GUARANT | RWB-PROD-RW-GUARANT |
| RW-AGENCYMG | Partner and agency manager | Entra ID group | RWB-DEV-RW-AGENCYMG | RWB-SIT-RW-AGENCYMG | RWB-UAT-RW-AGENCYMG | RWB-PROD-RW-AGENCYMG |
| RW-CONDUCT | Conduct and QA officer | Entra ID group | RWB-DEV-RW-CONDUCT | RWB-SIT-RW-CONDUCT | RWB-UAT-RW-CONDUCT | RWB-PROD-RW-CONDUCT |
| RW-CAPACITY | Capacity and workforce planner | Entra ID group | RWB-DEV-RW-CAPACITY | RWB-SIT-RW-CAPACITY | RWB-UAT-RW-CAPACITY | RWB-PROD-RW-CAPACITY |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | Entra ID group | RWB-DEV-RW-PRODHEAD | RWB-SIT-RW-PRODHEAD | RWB-UAT-RW-PRODHEAD | RWB-PROD-RW-PRODHEAD |
| RW-HEADLIT | Head of Litigation | Entra ID group | RWB-DEV-RW-HEADLIT | RWB-SIT-RW-HEADLIT | RWB-UAT-RW-HEADLIT | RWB-PROD-RW-HEADLIT |
| RW-HEADNPA | Head of NPA | Entra ID group | RWB-DEV-RW-HEADNPA | RWB-SIT-RW-HEADNPA | RWB-UAT-RW-HEADNPA | RWB-PROD-RW-HEADNPA |
| RW-HEADASL | Head of Asset Liquidity | Entra ID group | RWB-DEV-RW-HEADASL | RWB-SIT-RW-HEADASL | RWB-UAT-RW-HEADASL | RWB-PROD-RW-HEADASL |
| RW-CREDCOMM | Credit approval committee member | Entra ID group | RWB-DEV-RW-CREDCOMM | RWB-SIT-RW-CREDCOMM | RWB-UAT-RW-CREDCOMM | RWB-PROD-RW-CREDCOMM |
| RW-WOCOMM | Write-off committee member | Entra ID group | RWB-DEV-RW-WOCOMM | RWB-SIT-RW-WOCOMM | RWB-UAT-RW-WOCOMM | RWB-PROD-RW-WOCOMM |
| RW-RISK | Risk and model risk officer | Entra ID group | RWB-DEV-RW-RISK | RWB-SIT-RW-RISK | RWB-UAT-RW-RISK | RWB-PROD-RW-RISK |
| RW-COE | Center of excellence analyst | Entra ID group | RWB-DEV-RW-COE | RWB-SIT-RW-COE | RWB-UAT-RW-COE | RWB-PROD-RW-COE |
| RW-DATASTEW | Data steward and data product owner | Entra ID group | RWB-DEV-RW-DATASTEW | RWB-SIT-RW-DATASTEW | RWB-UAT-RW-DATASTEW | RWB-PROD-RW-DATASTEW |
| RW-FINANCE | Finance and CFO delegate | Entra ID group | RWB-DEV-RW-FINANCE | RWB-SIT-RW-FINANCE | RWB-UAT-RW-FINANCE | RWB-PROD-RW-FINANCE |
| RW-AUDIT | Internal audit | Entra ID group | RWB-DEV-RW-AUDIT | RWB-SIT-RW-AUDIT | RWB-UAT-RW-AUDIT | RWB-PROD-RW-AUDIT |
| RW-COMPLY | Compliance and PDPA officer | Entra ID group | RWB-DEV-RW-COMPLY | RWB-SIT-RW-COMPLY | RWB-UAT-RW-COMPLY | RWB-PROD-RW-COMPLY |
| RW-PLATADM | Platform administrator | Entra ID group | RWB-DEV-RW-PLATADM | RWB-SIT-RW-PLATADM | RWB-UAT-RW-PLATADM | RWB-PROD-RW-PLATADM |
| RW-REFADM | Reference data administrator | Entra ID group | RWB-DEV-RW-REFADM | RWB-SIT-RW-REFADM | RWB-UAT-RW-REFADM | RWB-PROD-RW-REFADM |
| RW-SECADM | Security administrator | Entra ID group | RWB-DEV-RW-SECADM | RWB-SIT-RW-SECADM | RWB-UAT-RW-SECADM | RWB-PROD-RW-SECADM |
| RW-BIANAL | Reporting and BI analyst | Entra ID group | RWB-DEV-RW-BIANAL | RWB-SIT-RW-BIANAL | RWB-UAT-RW-BIANAL | RWB-PROD-RW-BIANAL |
| RW-TRIBE | Tribe lead and squad members | Entra ID group | RWB-DEV-RW-TRIBE | RWB-SIT-RW-TRIBE | RWB-UAT-RW-TRIBE | RWB-PROD-RW-TRIBE |
| PT-AGENCY | Collection agency (OA) user | Entra ID group | RWB-DEV-PT-AGENCY | RWB-SIT-PT-AGENCY | RWB-UAT-PT-AGENCY | RWB-PROD-PT-AGENCY |
| PT-LAWFIRM | Law firm user | Entra ID group | RWB-DEV-PT-LAWFIRM | RWB-SIT-PT-LAWFIRM | RWB-UAT-PT-LAWFIRM | RWB-PROD-PT-LAWFIRM |
| PT-VALUER | Valuer | Entra ID group | RWB-DEV-PT-VALUER | RWB-SIT-PT-VALUER | RWB-UAT-PT-VALUER | RWB-PROD-PT-VALUER |
| PT-AUCTION | Auction vendor | Entra ID group | RWB-DEV-PT-AUCTION | RWB-SIT-PT-AUCTION | RWB-UAT-PT-AUCTION | RWB-PROD-PT-AUCTION |
| PT-BUYER | Debt buyer and AMC | Entra ID group | RWB-DEV-PT-BUYER | RWB-SIT-PT-BUYER | RWB-UAT-PT-BUYER | RWB-PROD-PT-BUYER |
| PT-RAMC | RAMC user | Entra ID group | RWB-DEV-PT-RAMC | RWB-SIT-PT-RAMC | RWB-UAT-PT-RAMC | RWB-PROD-PT-RAMC |
| SY-CASEWF | Case workflow module | Managed identity | RWB-DEV-SY-CASEWF | RWB-SIT-SY-CASEWF | RWB-UAT-SY-CASEWF | RWB-PROD-SY-CASEWF |
| SY-RULES | Rules component | Managed identity | RWB-DEV-SY-RULES | RWB-SIT-SY-RULES | RWB-UAT-SY-RULES | RWB-PROD-SY-RULES |
| SY-DATALOAD | Data load from COLLINS | Managed identity | RWB-DEV-SY-DATALOAD | RWB-SIT-SY-DATALOAD | RWB-UAT-SY-DATALOAD | RWB-PROD-SY-DATALOAD |
| SY-OCR | OCR and extraction pipeline | Managed identity | RWB-DEV-SY-OCR | RWB-SIT-SY-OCR | RWB-UAT-SY-OCR | RWB-PROD-SY-OCR |
| SY-DECLOG | Decision log writer | Managed identity | RWB-DEV-SY-DECLOG | RWB-SIT-SY-DECLOG | RWB-UAT-SY-DECLOG | RWB-PROD-SY-DECLOG |
| SY-AGENT | Agent platform | Managed identity | RWB-DEV-SY-AGENT | RWB-SIT-SY-AGENT | RWB-UAT-SY-AGENT | RWB-PROD-SY-AGENT |

## Systems by role

| Systems each bank role uses |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R read, W write, R/W both, blank none. Every bank role also uses the Workbench and signs in through Entra ID. |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Role code | Role name | ALS core and GL | EFS | COLLINS | ACE and TDR | NLEADS | CCMS | SVAF | AMIS and RPS | LIT | Document hub | NCB | Aric | WIN | Partner portal | Power BI | Entra ID |
| RW-CASEOWN | Case owner | R | R/W | R |  |  |  |  |  |  | R/W |  |  | W |  | R | R |
| RW-TEAMMGR | Team manager |  | R |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| RW-PHONECOL | Phone collector | R | R/W |  |  |  |  |  |  |  |  | R |  |  |  |  | R |
| RW-FIELDCOL | Field collector |  | R |  |  |  |  |  |  |  | W |  |  |  |  |  | R |
| RW-RESTRUCT | Restructuring officer (FCR) | W | R | R/W | R/W | W |  |  |  |  | R/W |  |  |  |  |  | R |
| RW-SPECIAL | Hardship and vulnerability specialist |  | R/W |  |  |  |  |  |  |  | R |  |  |  |  |  | R |
| RW-COMPLAIN | Complaint officer |  | R/W |  |  |  |  |  |  |  | R/W |  |  |  |  |  | R |
| RW-FRAUD | Fraud investigator |  | R |  |  |  |  |  |  |  |  |  | R/W |  |  |  | R |
| RW-LITOFF | Litigation officer |  |  |  |  |  |  |  |  | R/W | R/W |  |  |  | R/W |  | R |
| RW-ENFORCE | Enforcement owner |  |  |  |  |  |  |  | R | R/W |  |  |  |  | R/W |  | R |
| RW-LEGAL | Legal counsel |  |  |  |  |  |  |  |  | R | R/W |  |  | R |  |  | R |
| RW-SALEOFF | Sale officer | R |  |  |  |  |  | R | R/W |  |  |  |  |  | R/W |  | R |
| RW-NPAMGR | NPA and asset manager | R |  |  |  |  |  | R | R/W |  |  |  |  |  |  |  | R |
| RW-DEBTSALE | Debt sale officer | R/W |  |  |  |  |  |  |  |  |  |  |  |  | R/W | R | R |
| RW-WRITEOFF | Write-off team member | R |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| RW-CREDITAD | Credit Administration officer | R/W |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| RW-GUARANT | Guarantee officer | R |  |  |  |  |  |  |  |  | R/W |  |  |  | R/W |  | R |
| RW-AGENCYMG | Partner and agency manager |  |  |  |  |  |  |  |  |  |  |  |  |  | R/W | R | R |
| RW-CONDUCT | Conduct and QA officer |  | R |  |  |  |  |  |  |  | R |  |  |  |  | R | R |
| RW-CAPACITY | Capacity and workforce planner |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| RW-PRODHEAD | Product head (Mortgage, HP, SSME) | R |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| RW-HEADLIT | Head of Litigation |  |  |  |  |  |  |  |  | R |  |  |  |  |  | R | R |
| RW-HEADNPA | Head of NPA |  |  |  |  |  |  |  | R |  |  |  |  |  |  | R | R |
| RW-HEADASL | Head of Asset Liquidity |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R | R |
| RW-CREDCOMM | Credit approval committee member |  |  | R | R |  |  |  |  |  |  |  |  |  |  |  | R |
| RW-WOCOMM | Write-off committee member | R |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| RW-RISK | Risk and model risk officer |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| RW-COE | Center of excellence analyst |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| RW-DATASTEW | Data steward and data product owner | R | R |  |  |  | R | R |  |  |  |  |  |  |  | R | R |
| RW-FINANCE | Finance and CFO delegate | R |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| RW-AUDIT | Internal audit |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R |
| RW-COMPLY | Compliance and PDPA officer |  |  |  |  |  |  |  |  |  | R |  |  |  |  | R | R |
| RW-PLATADM | Platform administrator | R | R |  |  |  |  |  |  |  | R |  |  |  | R |  | R/W |
| RW-REFADM | Reference data administrator |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R |
| RW-SECADM | Security administrator |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R/W |
| RW-BIANAL | Reporting and BI analyst |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R/W | R |
| RW-TRIBE | Tribe lead and squad members |  |  |  |  |  |  |  |  |  |  |  |  |  |  | R | R |

## Counts

| Roles by class and first release |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|
| Calculated from the Roles tab. |  |  |  |  |  |  |  |  |  |
| Class | Roles | E1 | E2 | E3 | E4 | E5 | E6 | E7 | E8 |
| Bank user |  |  |  |  |  |  |  |  |  |
| Partner user |  |  |  |  |  |  |  |  |  |
| Customer party |  |  |  |  |  |  |  |  |  |
| Non-human actor |  |  |  |  |  |  |  |  |  |
| Total |  |  |  |  |  |  |  |  |  |

## Key

| Key |  |  |
|---|---|---|
| What each letter, scope and value means. |  |  |
| Item | Term | Meaning |
| Letter | C | Create |
| Letter | R | Read |
| Letter | U | Update |
| Letter | D | Delete |
| Letter | A | Approve, within the limit set for the role in the delegation of authority table |
| Letter | - | No access to the area |
| Scope | Own | Cases the person owns or has a task on |
| Scope | Team | Cases in the person's team queues |
| Scope | All | Every case |
| Scope | Placed cases | Cases placed with the partner firm |
| Release | E1 to E8 | The release that gives the role a screen and real users. Before it, the role has named test users in SIT and UAT |
| Release | No login | Reached by filing and result interfaces, not by a Workbench login |
| Standard | NIST RBAC | Users, roles, permissions and sessions as in ANSI/INCITS 359 |

<!-- source: 05 Technical architecture/Recovery Workbench Information Flow v5.pptx -->
<!-- converted: 2026-11-16 from PPTX -->

> **Source:** `05 Technical architecture/Recovery Workbench Information Flow v5.pptx`  
> **Converted from:** PPTX

## Slide 1

SCB

COLLECTIONS AND RECOVERY TRANSFORMATION Recovery Workbench: information flow

Henka Group, 15 November 2026 (C) Siam Commercial Bank and Henka Pte Ltd

## Slide 2

How information reaches the Workbench

2

Into ACE (ACE team), daily Core bank (ALS) EFS SCBPDM LIT COLLINS models NLEADS, EasyApp, Entra ID, on change

Into ACE (ACE team), less often CCMS and SVAF, weekly AMIS, monthly RPS and WIN, weekly GL, monthly

ACE ingestion ACE team. Lands each source in ACE tables at the end of its business day

ACE checks ACE ingestion checks each feed, takes it whole or not at all and records it in ace_batch_run

ACE ACE database: source data in Tier 1 and Tier 2 ACE tables, and everything the Workbench writes 30 recovery.v_ace_* views, SELECT only: the only read path out of ACE source data Recovery Workbench module: reads those views only; case, rules, decision log, document hub, partner portal People and partners write directly through the screens and the partner portal

Out of the Workbench Core bank: bookings made by the officer WIN: notices for registered mail NSS and LINE OA: messages Power BI and COLLINS: daily batch to the data lake Partners: instructions Debt buyers: data tape Bank log services: audit, PII and SOC events

The Workbench loads no source data: ACE ingests it and the Workbench reads views. Source data is end of day or older; what people enter is current.

## Slide 3

Integration patterns and the ones the Workbench uses

3

The Workbench calls no system of record directly. Data comes in through ACE ingestion and is read through recovery.v_ace_* views; it leaves through ACE paths that already exist.

| Pattern | Available at the bank | Used by the Workbench |
|---|---|---|
| Real time | REST, SOAP, MQ, HTTPS | Not used for data from other systems in Epics 1 and 2. Same-day candidates stay open under DL06 |
| Event | Kafka | PII Kafka for personal data access logging. ACE batch status reaches the Workbench as AceDataReady and AceDataLate |
| Batch | File, SFTP, Azure Data Factory, Control-M, COLLINS | ACE ingestion, owned by the ACE team, for every inbound source. The Workbench runs no inbound load and reads 30 views |
| Manual | Excel file | Trackers leave system scope and retire through the Cutover plan. Data no system holds is entered on the case |
| Direct entry | Workbench screens and the partner portal | Everything the Workbench is the system of record for |

## Slide 4

Information that comes in daily through ACE

4

ACE ingests each source after the business day closes, into Tier 1 tables or the Tier 2 tables and columns in RWB-ACE-001. The Workbench reads the views the next morning, so a payment made today is seen tomorrow. Data products: I01 DP01; I02 DP01, DP13; I03 DP02; I04 DP05; I05 DP11; I06 DP07.

| ID | Information | Source, ACE table | How often | Read through |
|---|---|---|---|---|
| I01 | Loan accounts: balances, interest, fees, days past due, bucket, classification, restructure flag | ALS, account | Daily, end of day | v_ace_account |
| I02 | Payments posted to each account | ALS, payment | Daily, end of day | v_ace_payment |
| I03 | Customer profile, identifiers and contact details | SCBPDM, customer and contacts | Daily, end of day | v_ace_customer, v_ace_contact |
| I04 | Collections history: contacts, action codes, promises | EFS, efs_action | Daily, end of day | v_ace_efs_action |
| I05 | Scores, expected return by route, sale price and sale success estimates, restructure scheme suggestions | COLLINS, collins_score | Daily; monthly for some models | v_ace_score |
| I06 | Litigation status and lawsuit numbers | LIT, lawsuit | Daily, end of day | v_ace_lawsuit |

## Slide 5

Information that comes in weekly or monthly, or is entered

5

| ID | Information | From | Path and how often | Read through; data product |
|---|---|---|---|---|
| I07 | Collateral records | CCMS | ACE ingestion to collateral_detail, weekly | v_ace_collateral; DP06 |
| I08 | Appraisals | SVAF | ACE ingestion to valuation, weekly | v_ace_valuation; DP06 |
| I09 | Assets held and asset sales | AMIS | ACE ingestion to npa_asset and npa_sale, monthly | v_ace_npa_asset, v_ace_npa_sale; DP06 |
| I10 | Repossessed vehicles and stock | RPS | ACE ingestion to npa_asset, weekly | v_ace_npa_asset; DP06 |
| I11 | Registered letters and proof of delivery | WIN | ACE ingestion to pod_receipt, weekly | v_ace_pod; DP07 |
| I12 | Write-off postings | GL | ACE ingestion to gl_write_off, monthly | v_ace_write_off; DP13 |
| I13 | Partner results: court dates, enforcement steps, appraisal reports, sale results | Partners | Partner portal in the Workbench, as entered | Entered in the Workbench; DP06, DP07, DP08 |
| I14 | Documents | Scans, uploads, email, partners | Document hub, as received | Entered in the Workbench; DP10 |
| I15 | Thai Credit Guarantee quota and claim deadlines | Thai Credit Guarantee Corporation | Entered by the guarantee officer, as received | Entered in the Workbench; DP04 |
| I16 | Users and the roles they hold | Entra ID and the bank IAM | ACE sign-in; groups through ACE ingestion to iam_group | v_ace_iam_group; DP14 |

## Slide 6

Information that leaves the Workbench

6

| ID | Information | To | Path | How often |
|---|---|---|---|---|
| O01 | Restructure, settlement and write-off bookings | Core bank (ALS) | The officer books in the core bank. The Workbench confirms the booking from ACE on the next business date | As approved |
| O02 | Demand, recall and sale notices for registered mail | WIN | File from the Workbench | Daily |
| O03 | SMS and LINE messages to customers | NSS and LINE OA | The ACE notification path | As sent |
| O04 | Case, queue, decision and outcome data for reporting | Power BI | Daily batch to the data lake | Daily |
| O05 | Decisions and outcomes for model learning | COLLINS | Daily batch to the data lake | Daily |
| O06 | Instructions to partners | Partners | Partner portal | As sent |
| O07 | Debt sale data tape | Debt buyers | File, through the data room for the lot | Per lot |
| O08 | Audit, personal data access and security events | Bank log services | The ACE audit, PII Kafka and SOC logs | As they happen |

## Slide 7

How fresh each decision's inputs are

7

| Decision | Inputs it uses | How fresh, per ace_batch_run | What that means |
|---|---|---|---|
| D6 entry | Account, arrears, customer, collections history | End of day | A case enters the morning after ACE shows it at 90 days past due |
| D5 restructure | Account, payments, restructure calculation, scheme suggestion | End of day | The offer is built on yesterday's balance. The officer confirms the figure in the core bank before booking |
| D6 route | Account, collateral value, scores, contact history | End of day; collateral weekly | An appraisal older than its age limit holds the route decision until replaced |
| D7 legal | Litigation status, notices and proof of delivery | End of day; proof of delivery weekly | A notice period starts from the delivery date, which can arrive up to a week late |
| D8 disposal | Asset, appraisal, price and sale success estimates | Monthly for assets; weekly for appraisals | The floor price uses the latest appraisal and the latest model estimate |
| D9 write-off | Balance, recoveries, GL posting | End of day; GL monthly | The posting is confirmed against the GL data in ACE each month |

## Slide 8

When information does not arrive

8

| What happens | What the Workbench does | Who is told | What the user sees |
|---|---|---|---|
| An ACE source is late | Raises AceDataLate at the source cut-off and marks the data product stale. The previous ACE business date stays in use | Data steward, platform administrator, ACE team | The age of the data on every screen that uses it |
| ACE refuses a feed | Reads the last complete business date from ace_batch_run. The previous ACE data stays in use | Data steward, ACE team | The same, with the product marked stale |
| A weekly or monthly source is late | Raises AceDataLate and marks the data product stale one business day after the ACE batch was due | ACE team, data steward | The age of the data on the case |
| A decision input is older than its age limit | Holds the decision. The task names the input and its age | Case owner | Which input is out of date and how to refresh it |
| A score is missing for an account | Shows the route decision without the score. The decision log records the missing input | Case owner, Risk and model risk officer | No score, and the reason |
| A booking is not seen on the next ACE business date | Raises a task to the officer who recorded the booking. The case stays in its waiting state | Officer, team manager | The booking marked as not confirmed |
| An outbound file is not acknowledged | Sends it again. After the third failure, raises a task to the owning team. A notice timer starts only on confirmed dispatch | Owning team, platform administrator | The notice marked as not sent |

## Slide 9

The checks ACE data passes

9

ACE ingestion records each feed's business date, record count and result in ace_batch_run. Each view carries the business date, so a decision can show the age of every input.

| Check | What it tests | If it fails |
|---|---|---|
| Business date | ACE ingestion: the feed is for the expected business date and is not a repeat of one already taken | ACE refuses the feed |
| Structure | Every expected field is present with the expected type and length | ACE refuses the feed |
| Control totals | Record count and balance totals match the totals the source sends | ACE refuses the feed |
| Keys | Every record has its business key, and no key appears twice | ACE refuses the feed |
| View conformance | Workbench build: every v_ace_* view compiles, nothing references public and the role cannot write | The build fails and nothing deploys |
| Batch complete | ace_batch_run shows the source complete for the expected business date by its cut-off | AceDataLate; the data product is marked stale |
| Reconciliation | Case accounts reconcile to v_ace_account; every business key resolves | Alert the data steward |

## Slide 10

Where same-day information would change the result

10

Assumed: ACE end of day data for all Epic 1 and Epic 2 work (D-RCV-35), with events added later for named same-day triggers. Which interfaces need real-time data stays open under DL06.

| Information | What a day's delay can cause | How the Workbench works without it |
|---|---|---|
| A payment | A customer who paid this morning is contacted this afternoon | Staff check the core bank for today's payments before a call or a letter |
| A complaint or dispute | Contact continues while a complaint is open | Raised on the case by the person who receives it. Contact stops at once |
| A death or bankruptcy notice | Collection action against an estate or a debtor under protection | Raised on the case by the officer. Contact and legal steps stop at once |
| A promise kept or broken | The next step is a day late | The next step runs on the next ACE business date |
| A court date change | A hearing prepared for the wrong date | The law firm records the new date in the partner portal |

## Slide 11

Gaps and the assumptions taken

11

| What is open | Assumption the flow takes | Decision |
|---|---|---|
| Which interfaces need real-time data | ACE end of day data for every source; events added later for named triggers | DL06; D-RCV-35 |
| Whether any legacy system is enhanced | None. The Workbench reads ACE through views and writes through ACE paths only | D-RCV-35, was DL12 |
| Which systems carry the case identifier | The Workbench only. The account number is the join | DL21 |
| The difference accepted between an ACE feed and its source | Zero. ACE refuses a feed that does not reconcile; cases reconcile to v_ace_account | DL25 |
| How much EFS history ACE holds | The contact outcomes the business lead names, for the collection period only | DL29 |
| Who builds SMS and LINE dispatch | A bank-wide service where one exists; the Workbench squads otherwise | DL30 |
| How partners reach the partner portal from outside the bank | The architecture change is raised in November. Law firms first need the console at Epic 5 | DL03 |
| Whether the ACE team accepts RWB-ACE-001 and its dates | Tier 2 tables needed by 21 November; until then the Tier 2 views and their features stay behind flags | DL43, open |

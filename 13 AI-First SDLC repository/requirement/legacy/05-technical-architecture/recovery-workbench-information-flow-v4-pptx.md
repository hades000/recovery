<!-- source: 05 Technical architecture/Recovery Workbench Information Flow v4.pptx -->
<!-- converted: 2026-11-04 from PPTX -->

> **Source:** `05 Technical architecture/Recovery Workbench Information Flow v4.pptx`  
> **Converted from:** PPTX

## Slide 1

SCB

COLLECTIONS AND RECOVERY TRANSFORMATION Recovery Workbench: information flow

Henka Group, 28 October 2026 (C) Siam Commercial Bank and Henka Pte Ltd

## Slide 2

How information reaches the Workbench

2

Through COLLINS Core bank (ALS) EFS SCBPDM and UDP AAL LIT COLLINS models

By file CCMS and SVAF, weekly AMIS, monthly RPS and WIN, weekly GL, monthly

COLLINS Databricks ETL batch. Loads each source at the end of the business day

File load A scheduled batch job in ACE checks each file and loads it whole or not at all

ACE ACE database: end of day data and everything the Workbench writes Recovery Workbench module: case, rules, decision log, document hub, partner portal People and partners write directly through the screens and the partner portal

Out of the Workbench Core bank: bookings made by the officer WIN: notices for registered mail NSS and LINE OA: messages Power BI and COLLINS: daily batch to the data lake Partners: instructions Debt buyers: data tape Bank log services: audit, PII and SOC events

There is no real-time feed today. Everything loaded is end of day or older; everything people and partners enter is current.

## Slide 3

Integration patterns and the ones the Workbench uses

3

The Workbench calls no system of record directly. Data comes in through COLLINS or a file load, and leaves through ACE paths that already exist.

| Pattern | Available at the bank | Used by the Workbench |
|---|---|---|
| Real time | REST, SOAP, MQ, HTTPS | Not used for data from other systems in Epics 1 and 2. Candidates are listed for decision DL06 |
| Event | Kafka | Used for personal data access logging (PII Kafka). Not used for business data in Epics 1 and 2 |
| Batch | File, SFTP, Azure Data Factory, Control-M, COLLINS | COLLINS for every source it carries. File loads for CCMS, SVAF, AMIS, RPS, WIN and the GL |
| Manual | Excel file | Replaced by file loads with checks. Data the bank does not hold in a system is entered on the case |
| Direct entry | Workbench screens and the partner portal | Everything the Workbench is the system of record for |

## Slide 4

Information that comes in through COLLINS

4

COLLINS loads each source after the business day closes. The Workbench uses it the next morning, so a payment made today is seen tomorrow.

| ID | Information | From | How often | Data product |
|---|---|---|---|---|
| I01 | Loan accounts: balances, interest, fees, days past due, bucket, classification, restructure flag | Core bank (ALS) | Daily, end of day | DP01 |
| I02 | Payments posted to each account | Core bank (ALS) | Daily, end of day | DP01, DP13 |
| I03 | Customer profile, identifiers and contact details | SCBPDM, UDP and the core bank | Daily, end of day | DP02 |
| I04 | Collections history: contacts, action codes, promises | EFS | Daily, end of day | DP05 |
| I05 | Scores, expected return by route, sale price and sale success estimates, restructure scheme suggestions | COLLINS models | Daily; monthly for some models | DP11 |
| I06 | Litigation status and lawsuit numbers | LIT | Daily, end of day | DP07 |

## Slide 5

Information that comes in by file or is entered

5

| ID | Information | From | Path and how often | Data product |
|---|---|---|---|---|
| I07 | Collateral records | CCMS | File load, weekly | DP06 |
| I08 | Appraisals | SVAF | File load, weekly | DP06 |
| I09 | Assets held and asset sales | AMIS | File load, monthly | DP06 |
| I10 | Repossessed vehicles and stock | RPS | File load, weekly | DP06 |
| I11 | Registered letters and proof of delivery | WIN | File load, weekly | DP07 |
| I12 | Write-off postings | GL | File load, monthly | DP13 |
| I13 | Partner results: court dates, enforcement steps, appraisal reports, sale results | Partners | Partner portal in the Workbench, as entered | DP06, DP07, DP08 |
| I14 | Documents | Scans, uploads, email, partners | Document hub, as received | DP10 |
| I15 | Thai Credit Guarantee quota and claim deadlines | Thai Credit Guarantee Corporation | Entered by the guarantee officer, as received | DP04 |
| I16 | Users and the roles they hold | Entra ID and the bank IAM | Sign-in, at each sign-in | DP14 |

## Slide 6

Information that leaves the Workbench

6

| ID | Information | To | Path | How often |
|---|---|---|---|---|
| O01 | Restructure, settlement and write-off bookings | Core bank (ALS) | The officer books in the core bank. The Workbench confirms the booking on the next day's load | As approved |
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

| Decision | Inputs it uses | How fresh they are | What that means |
|---|---|---|---|
| D6 entry | Account, arrears, customer, collections history | End of day | A case enters the morning after it reaches 90 days past due |
| D5 restructure | Account, payments, restructure calculation, scheme suggestion | End of day | The offer is built on yesterday's balance. The officer confirms the figure in the core bank before booking |
| D6 route | Account, collateral value, scores, contact history | End of day; collateral weekly | An appraisal older than its age limit holds the route decision until replaced |
| D7 legal | Litigation status, notices and proof of delivery | End of day; proof of delivery weekly | A notice period starts from the delivery date, which can arrive up to a week late |
| D8 disposal | Asset, appraisal, price and sale success estimates | Monthly for assets; weekly for appraisals | The floor price uses the latest appraisal and the latest model estimate |
| D9 write-off | Balance, recoveries, GL posting | End of day; GL monthly | The posting is confirmed against the GL file each month |

## Slide 8

When information does not arrive

8

| What happens | What the Workbench does | Who is told | What the user sees |
|---|---|---|---|
| A COLLINS load is late | Keeps the previous load in use and marks the data product stale. Checks again each hour until the load window closes | Data steward, platform administrator | The age of the data on every screen that uses it |
| A load fails its checks | Refuses the whole load. The previous load stays in use | Data steward, platform administrator | The same, with the product marked stale |
| A file is late | Marks the data product stale one business day after the file was due | The team that sends the file, data steward | The age of the data on the case |
| A decision input is older than its age limit | Holds the decision. The task names the input and its age | Case owner | Which input is out of date and how to refresh it |
| A score is missing for an account | Shows the route decision without the score. The decision log records the missing input | Case owner, Risk and model risk officer | No score, and the reason |
| A booking is not seen in the next day's load | Raises a task to the officer who recorded the booking. The case stays in its waiting state | Officer, team manager | The booking marked as not confirmed |
| An outbound file is not acknowledged | Sends it again. After the third failure, raises a task to the owning team. A notice timer starts only on confirmed dispatch | Owning team, platform administrator | The notice marked as not sent |

## Slide 9

The checks every load passes

9

Each load records its business date, record count, control totals and result. Each loaded record carries the business date, so a decision can show the age of every input.

| Check | What it tests | If it fails |
|---|---|---|
| Business date | The load is for the expected business date and is not a repeat of a load already taken | Refuse the load |
| Structure | Every expected field is present with the expected type and length | Refuse the load |
| Control totals | Record count and balance totals match the totals the source sends | Refuse the load |
| Keys | Every record has its key, and no key appears twice | Refuse the load |
| References | Each account, customer or asset is one the Workbench can match | Hold the record in an exception list and try it again with the next load |
| Lists of values | Each coded value is in its list of values | Hold the record in an exception list; add the value through a versioned load if it is new |
| Movement | Changes against the previous load are within the expected range | Load, and alert the data steward |

## Slide 10

Where same-day information would change the result

10

Assumed: the daily batch for all Epic 1 and Epic 2 data, with events added later for named same-day triggers. Which interfaces need real-time data is decision DL06.

| Information | What a day's delay can cause | How the Workbench works without it |
|---|---|---|
| A payment | A customer who paid this morning is contacted this afternoon | Staff check the core bank for today's payments before a call or a letter |
| A complaint or dispute | Contact continues while a complaint is open | Raised on the case by the person who receives it. Contact stops at once |
| A death or bankruptcy notice | Collection action against an estate or a debtor under protection | Raised on the case by the officer. Contact and legal steps stop at once |
| A promise kept or broken | The next step is a day late | The next step runs on the next day's load |
| A court date change | A hearing prepared for the wrong date | The law firm records the new date in the partner portal |

## Slide 11

Gaps and the assumptions taken

11

| What is open | Assumption the flow takes | Decision |
|---|---|---|
| Which interfaces need real-time data | Daily batch for everything loaded; events added later for named triggers | DL06 |
| Whether any legacy system is enhanced | None. The Workbench reads and writes through ACE and COLLINS only | DL12 |
| Which systems carry the case identifier | The Workbench only. The account number is the join | DL21 |
| The difference accepted between a load and its source | Zero. A load that does not reconcile is refused whole | DL25 |
| How much EFS history comes in | The contact outcomes the business lead names, for the collection period only | DL29 |
| Who builds SMS and LINE dispatch and the EFS file automation | A bank-wide service where one exists; the Workbench squads otherwise | DL30 |
| How partners reach the partner portal from outside the bank | The architecture change is raised in November. Law firms first need the console at Epic 5 | DL03 |
| When CCMS, SVAF, AMIS and RPS data comes through COLLINS | File loads at the frequencies shown until a batch feed exists | DL06, DL12 |

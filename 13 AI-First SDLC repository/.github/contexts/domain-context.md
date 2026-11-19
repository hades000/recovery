# Recovery Workbench — domain context

**Purpose:** the industry, banking and system vocabulary an agent needs to read the requirements
correctly. This file does not restate requirements or rules; those live in `project-context.md`.
**Source:** `requirement/legacy/02-business-architecture-and-process/recovery-workbench-business-glossary-v2-xlsx.md`
(98 terms) and `docs/discovery/business-glossary.md`. Thai terms are proposed and approved by Legal
and Compliance under DL10.

## 1. Recovery and collections terms

| Term | Meaning | Do not use |
|---|---|---|
| Recovery | The work from 90 days past due to close: restructure, settlement, deed in lieu, guarantee claim, litigation, enforcement, asset disposal, debt sale and write-off. | Collections (that is before day 90) |
| Collections | Contact, promise, escalation and restructure work before day 90, run on EFS and the ACE collection module. | Recovery |
| Days past due (DPD) | Days since the oldest unpaid instalment fell due. The Workbench takes over at 90 DPD. | Delinquency age |
| Non-performing loan (NPL) | A loan at 90 days past due or more. | Bad loan |
| Non-performing asset (NPA) | An asset the bank holds after repossession, deed in lieu or auction purchase. | Repossessed asset, when the accounting class is meant |
| Case | One customer and one product, from 90 days past due to close, with a case ID in the form RW-YYYY-NNNNNN. | Account, ticket |
| Case owner | The person who holds the case from day 90 to close and answers for its outcome. | Collector, handler |
| Case status | One of New, Assigned, In progress, Waiting customer, Waiting partner, Waiting approval, On hold, Closed. | Stage, step |
| Stage | One of the six value-stream stages: receive, route, resolve, enforce, realise, close. | Status |
| Milestone | A point the case reaches that matters to the bank, such as judgment obtained or asset sold. | Checkpoint |
| Case file item | A piece of information the case holds, such as an account, a document or a decision. | Field |
| Deviation | An event that stops the normal route: X1–X7. | Exception, issue |
| Contact stop | An instruction that no one contacts the customer while it is in force. Statutory notices continue. | Do not call |
| Cure | Arrears cleared so the account falls below 90 DPD and the case closes. | Recovery |
| Prescription date | The legal date after which a claim may be time-barred; set from the legal periods table at case creation. | Deadline |
| Service level | The time allowed in a queue or status, with warning and escalation thresholds, held as data. | SLA, when the contractual service is meant |
| Caseload cap | The most open cases one person may hold in a queue. | Quota |
| Allocation | Placing a new case in a queue and giving it an owner by rule. | Distribution |
| Assignment | Giving a case to a person by round robin, lowest load or continuity, within the cap. | Allocation |
| Transfer | Moving a case between queues or roles by rule, with a reason code. | Reassignment, when the rule is meant |
| Next action | The owned, dated action on every open case, produced by the rule that moved the case. | To-do |
| Override | A decision that does not follow the recommendation, with the reason recorded. | Exception |

## 2. Treatment and legal terms

| Term | Meaning | Do not use |
|---|---|---|
| Treatment | A resolution put to the customer or carried out on the case: restructure, settlement, deed in lieu, buy-back or guarantee claim. | Offer, when the record is meant |
| Restructure | A change to the loan terms, including TDR, to make the debt serviceable. | Refinance |
| TDR | Troubled debt restructuring, the bank's restructure scheme and calculator in ACE. | Restructure, when the scheme is meant |
| Settlement | A discounted payoff accepted in full and final settlement. | Compromise |
| Haircut | The amount forgiven in a settlement. | Discount |
| Deed in lieu (DIL) | Transfer of the collateral to the bank in settlement of the debt. | Voluntary surrender |
| Buy-back | The customer buying back an asset transferred in lieu. | Repurchase |
| Guarantee claim | A claim against a Thai Credit Guarantee Corporation guarantee or an insurer. | TCG claim, when an insurer is meant |
| Guarantor | A party who guaranteed the loan. | Surety |
| Subrogation | The bank's right to pursue the debtor after paying a guarantee claim. | Recovery right |
| Demand notice | A notice demanding payment before legal action. | Letter |
| Recall notice | A notice recalling the whole facility. | Acceleration letter |
| Proof of delivery | Evidence that a notice reached the customer; a notice period starts from it. | Delivery report |
| Litigation | A civil case filed against the borrower or guarantor. | Lawsuit, when the process is meant |
| Lawsuit | One civil case. | Litigation, when one suit is meant |
| Black case number | The court number given when a case is filed. | Case number (that is the Workbench case ID) |
| Judgment | The court's decision on the claim. | Order |
| Enforcement | Steps after judgment to seize and sell assets. | Execution, when the legal process is meant |
| Legal Execution Department (LED) | The government department that runs enforcement auctions on the 100/90/80/70 percent ladder. | Court |
| Legal hold | A hold that stops routing while a legal matter is decided. | Retention hold |

## 3. Disposal and debt sale terms

| Term | Meaning | Do not use |
|---|---|---|
| Asset held for sale | An asset the bank holds after repossession, deed in lieu or auction purchase. | Inventory |
| Book value | The value of an asset held for sale in the bank's books. | Market value |
| Appraisal | A valuation of collateral or an asset. | Valuation report |
| Forced sale value | The value expected in a quick sale. | Liquidation value |
| Floor price | The lowest price approved for a sale. | Reserve price, for an asset |
| Listing | An asset offered for sale, with its prices and rounds. | Advertisement |
| Auction round | One round of a Dutch auction on the price ladder. | Bid event |
| RAMC | SCB's asset management company, which takes transfers of assets and accounts. | AMC, when RAMC is meant |
| Debt sale | Sale of accounts to a debt buyer. | Portfolio sale |
| Lot | A group of accounts offered to debt buyers together. | Pool, portfolio |
| Data room | The controlled buyer view of lot data after qualification and NDA. | Data pack |
| Put-back | The return of an account to the bank under the sale terms. | Refund |
| Write-off | The accounting removal of an uncollectible balance, approved by the committee and posted. | Charge-off, when the posting is meant |
| Recovery after charge-off | Follow-up on written-off debt until the bank's criteria end it. | Post-write-off collection |

## 4. Decision, data and control terms

| Term | Meaning | Do not use |
|---|---|---|
| Decision | One of D1–D9 or their sub-decisions, made by a rule, a model, an agent or a person. | Approval |
| Decision log | The append-only, hash-chained record of every decision with inputs, versions, approver and outcome. | Audit trail, history |
| Delegation of authority table | The limits each approval level may approve, by decision, product and amount. | DOA matrix |
| Approval level | One of the six levels of the bank approval authority regulation. | Authority, sign-off |
| Separation of duty | The preparer of a decision cannot approve it. | Four-eyes |
| Data product | A set of entities with one system of record, one way in and one freshness. | Data mart, dataset |
| Freshness | How old a loaded value is, from its business date. | Timeliness |
| Interaction ledger | The ordered record of every contact, letter, promise, payment and hand-over on a case. | Contact history, notes |
| Document hub | The Workbench store and index for recovery documents, including extracted fields and custody. | DMS, folder |
| Document type | The class a document belongs to on the document checklist. | Category |
| Custody | Where an original document is and who holds it. | Storage |
| Masking | Hiding a personal data field from a role not allowed to see it. | Redaction |
| Break-glass | Emergency access beyond a role, with a reason and a review. | Super user |
| Autonomy level | How far an agent may act on a decision, from L0 (no action) to L4 (acts within policy). | Automation level |
| Agent | An AI component that prepares and recommends through the tool gateway. | Bot, robot |
| Tool gateway | The controlled interface through which an agent calls a tool or a model. | API gateway, when the agent path is meant |

## 5. Systems and organisations

| Name | What it is | Role in the Workbench |
|---|---|---|
| ACE | The bank's collection engine and the service the Workbench is a module of. One service, one repository, one front end. | Host, common module, case view, sign-in, access, audit, PII logging |
| COLLINS | The bank's collections data platform on Databricks. | Daily batch in: core bank (ALS), EFS, UDP, SCBPDM, AAL, LIT status, scores |
| EFS | The collections case system used before day 90. | Source of contact history, promises and hand-over data |
| ALS | The core bank / loan system. | Source of balances, arrears, payments and classification; booking target |
| CCMS | Collateral management system. | Collateral records; file load |
| SVAF | Collateral appraisal system. | Appraisal values; file load |
| AMIS | Asset management information system for property. | Asset records; file load |
| RPS | Vehicle asset system. | Vehicle asset records; file load |
| LIT | Litigation system. | Court case numbers, hearings and judgment status |
| WIN | Print and dispatch system. | Notices and letters out; proof of delivery back |
| NLEADS | The bank's credit approval and booking system for restructures. | Plan submission and booking confirmation |
| SCBPDM | The party and customer master. | Customer, guarantor and co-borrower facts via COLLINS |
| UDP | The customer product and relationship platform. | Customer and product facts via COLLINS |
| AAL | The bank's application and authentication layer. | Identity and access context |
| PACMAN | The bank's customer, product and account 360 view. | Customer and account facts referenced by the process map |
| HOME.SCB | The bank's public property listing channel. | Asset listings |
| SCIS | The bank's security and incident system. | Security events |
| NCB | The National Credit Bureau. | Credit data used in deviation and fraud screening |
| Aric | The bank's fraud and risk analytics system. | Fraud and risk signals |
| Power BI | The bank's reporting platform. | Case list, queue measures, steering dashboard, regulatory extracts |
| TCG | Thai Credit Guarantee Corporation. | Guarantee claims |
| BOT | Bank of Thailand. | Conduct and regulatory obligations |
| PDPA | Thailand's Personal Data Protection Act B.E. 2562. | Personal data classification, lawful basis, masking, retention |
| CMMN 1.1 | Case Management Model and Notation. | Case, stage, milestone, task, sentry, event listener, case file item |
| Drools decision tables | Drools XLS decision tables, evaluated by the embedded Drools engine (ADR-012); DMN is not used. | Decision tables for the 448 routing rules |
| OpenAPI 3.1 | REST API description standard. | API specification |
| AsyncAPI 3.0 | Event-driven API description standard. | Event and messaging design |

## 6. How to use this file

- Use the glossary names in code, data and conversation. One concept has one name.
- If a term is not here, check the full glossary before inventing one.
- If the source documents use a synonym, record it as a `CLAR-*` item rather than normalising it
  silently.
- Thai terms are proposed; do not treat them as approved until DL10 closes.

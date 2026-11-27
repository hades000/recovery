SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

---
title: Recovery Workbench Business Requirements Epics 3 to 8
description: Business requirements, business rules, success measures and governance for Epics 3 to 8 of the Recovery Workbench, produced under decision D-RCV-60 on the 19-service microservice target.
status: Draft
---

# Recovery Workbench Business Requirements Epics 3 to 8 v1

## 1. Document control

| Item | Detail |
|---|---|
| Document | Recovery Workbench business requirements, Epics 3 to 8 |
| Version | 1 |
| Date | 22 November 2026 |
| Author | BRD Builder (AI draft) |
| Status | Draft |
| Covers | Epics E3, E4, E5, E6, E7 and E8: 181 features and stories |
| Releases | E3 31 January 2027, E4 28 February 2027, E5 31 March 2027, E6 30 April 2027, E7 31 May 2027, E8 30 June 2027, all (tentative) |
| Structure | ISO/IEC/IEEE 29148, until the SCB X requirement template is adopted (DL13) |
| Decision | D-RCV-60 microservice realignment, which adopts Architecture v5 (19 services inside ACE, waves, contract-first, Kafka, Temporal, embedded Drools) |
| Superseded reading | Nothing in business intent. The delivery model behind these requirements was re-based on D-RCV-60; D-RCV-35 and D-RCV-36 stand |
| Prepared for | The Product Owner, the business owners of Epics 3 to 8, architecture, security and compliance |
| Reviewers | Product Owner; business owners for settle and deed in lieu, route decision, litigation, debt sale and write-off, deviations and partners, administration; solution architect; security administrator; Compliance and PDPA officer |

### 1.1 Change log

| Change | Version | Date | Detail |
|---|---|---|---|
| v1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash | 1 | 22 November 2026 | First issue. Business requirements, business rules, success measures, assumptions, constraints, dependencies, risks, open questions, governance and traceability for Epics 3 to 8. The requirement set is written at business level so that the 181 thin stories carry a rationale, a testable outcome and a source line. Every owner comes from the Microservice Ownership Map v1. Release dates are copied from the source and marked (tentative). |
| v1 update, 26 November 2026, in place from the source documents | 1 | 26 November 2026 | Backlog story codes removed from every requirement, rule and trace cell; the scope and trace tables give feature counts instead of story key ranges; the program citations point to Program v5, which keeps the IDs, text and sections 1 to 9 of v4. No requirement, rule, measure or question changes (GAP-3266; GAP-3269; ASM-5684; ASM-5688). |

### 1.2 Sources

| Source | Version and date | Used for |
|---|---|---|
| Recovery Workbench Epics 3 to 8 Specification | v3, 15 November 2026, decision D-RCV-35 | The 181 features, the 28 endpoints first available in these epics, the integration rows, the document control |
| Recovery Workbench User Stories Epics 3 to 8 | v3, 28 October 2026 | The 181 story keys, their priority, their scope, their roles |
| Recovery Workbench Business Requirements Program | v5, 22 November 2026 (requirement IDs, text and sections 1 to 9 unchanged from v4) | Business outcomes, the process architecture, the program requirement IDs REQ-*, the constraints, the release plan, the open decisions |
| Business Rules and Routing Logic | v4 | 448 rules in ten route sets, their states, conditions, actions and owners |
| Recovery Workbench Architecture v5 Text Extract | v1, November 2026 | The 19 services, the waves, the event, job and workflow catalogues |
| Recovery Workbench Temporal and Drools Design Text Extract | v1, November 2026 | How a case runs and how a decision is made and recorded |
| Microservice Ownership Map | v1, 22 November 2026 | The service owner of every capability, endpoint, event and job named here |
| Microservice Story Template and Rules | v1, 22 November 2026 | Header, versions, placeholders, gap and assumption rows |
| Open decisions DL06, DL10, DL11, DL13, DL18, DL22, DL23, DL26, DL43 | Decision Log, Program BRD v5 section 9 | The questions this document cannot answer from its sources |

## 2. Executive summary

Epics 3 to 8 take a recovery case from the route decision to the end of its life. Epic 3 settles, agrees a deed in lieu and takes assets onto the books. Epic 4 decides the route with reasons and runs the guarantee and auction paths. Epic 5 litigates to judgment and enforcement and prepares a debt sale. Epic 6 awards and settles a debt sale, writes off and recovers after charge-off, and manages the partner panel. Epic 7 runs the seven deviations end to end and scores and governs partners. Epic 8 puts administration, conduct, autonomy and regulatory reporting in place.

The six epics carry 181 features and 181 stories: 31 in E3, 50 in E4, 26 in E5, 37 in E6, 18 in E7 and 19 in E8. They release month by month from 31 January 2027 to 30 June 2027 (tentative). The business result is measured on eight program measures, from a 66.3 percent recovery rate on non performing loans towards 73 percent, and a litigation turnaround from 21 days to 6 days (Program BRD v5 section 2).

Under D-RCV-60 the same business intent is delivered as 19 service epics inside ACE, one service per business module, in four waves, with a published contract per service, Kafka events for facts, a Temporal workflow per case and embedded Drools for every rule. The business requirements in this document do not change with that split: what changes is which service owns each capability and which wave delivers it. Section 7.3 maps every epic to its service epics and waves.

What this document adds to the source is business rationale, business rules, success measures and a governance frame for stories that were written thin. Nothing is asserted where the sources are silent: 27 open questions are recorded in section 12, each with its gap and assumption row, and 34 assumptions are listed for confirmation in section 11.1.

## 3. Business context and problem statement

### 3.1 Context

The Workbench is the recovery module of ACE. It takes every case from 90 days past due, for Mortgage, Hire Purchase and SSME, and carries decisions D6 to D9 with their sub-decisions, D5 once the restructure program is live, and deviations X1 to X7 after day 90. Epics 1 and 2 put the case list, the case layer, the owner, the timer and the approval path in place; Epics 3 to 8 are where the recovery money is actually made and lost.

Source data arrives through ACE ingestion and is read only through the read-only `recovery.v_ace_*` views (D-RCV-35, ADR-010). The Workbench loads no source data and holds only the case, its decisions, reference data and four extension tables. From Epic 3 the case lifecycle runs on Temporal, one workflow per case, and every rule is a versioned data row evaluated by embedded Drools inside a workflow step (D-RCV-36, ADR-011, ADR-012). Under D-RCV-60 the module is delivered as 19 services inside the ACE platform, each with its own schema, contract, topic and task queue (Architecture v5, ADR-013 to ADR-023).

### 3.2 Problem statement

| # | Problem the business has today | Evidence in the sources |
|---|---|---|
| 1 | Recovery takes too long. Litigation runs at 21 days, deed in lieu at 26 days, restructure at 23 days, and an NPA takes 1,486 days to sell. | Program BRD v5 section 2 |
| 2 | Money and decisions are re-keyed across ALS, COLLINS, EFS, AMIS, RPS, LIT and WIN, so the case and the system of record disagree. | Program BRD v5 sections 5.2, 5.3, 5.8 to 5.16; Epics 3 to 8 Specification v3 integrations sheet |
| 3 | Some end-to-end steps have no owner at all: the NPA stock balance, an eviction, enforcement after judgment, and the write-off exception loop. | Epics 3 to 8 Specification v3, features FEAT-AST-06, FEAT-AST-08, FEAT-LIT-20, FEAT-WOF-12 |
| 4 | Deviations from the policy are common and are not measured. 44 percent of TDR cases deviate today. | Business Rules and Routing Logic v4, rule R-RES-10 |
| 5 | Decisions are not reproducible after the fact: the rule, model and prompt versions and the inputs used are not held in one place per decision. | Program BRD v5 sections 5.7 and 6.6 |
| 6 | Assets, debt sales and write-offs are run on spreadsheets and local lists, so the population, the price and the provision cannot be reconciled to the book. | Program BRD v5 sections 5.12 to 5.14, 7 |
| 7 | Personal data leaves the bank in a debt sale data tape and in partner exchanges, with masking done by hand. | Program BRD v5 NFR-041, NFR-042; Specification v3 FEAT-DBS-03 |
| 8 | Partner performance, conduct and fees are managed by memory and by email, and a partner exit does not recall its open cases. | Program BRD v5 sections 5.16, REQ-S9-001 to REQ-S9-008 |

## 4. Business objectives and expected outcomes

### 4.1 Objectives

| ID | Objective |
|---|---|
| OBJ-1 | A case reaches a route decision with a recommendation, a reason and an approval inside the delegation, every time, without a person assembling the inputs. |
| OBJ-2 | Settlements, TDR plans and deeds in lieu reach a booking in ALS and NLEADS without re-keying, and the bought-back or transferred asset reaches the asset record in the same step. |
| OBJ-3 | Litigation is instructed, tracked and enforced with one named owner from judgment to the end of enforcement, and enforcement proceeds are matched to the case. |
| OBJ-4 | Debt sale and write-off run as rule-driven populations against a policy cap, with the committee decision, the posting and the provision reconciled. |
| OBJ-5 | Deviations X1 to X7 run end to end with a named owner, contact stops that hold, and a return point that keeps the clocks right. |
| OBJ-6 | Partners are selected, instructed, scored, paid and exited on measured evidence through the portal, not by email. |
| OBJ-7 | Administration, rule change, autonomy and regulatory reporting are done through versioned data and screens, with no code release. |

### 4.2 What each epic gives the business

| Epic | Theme | Release (tentative) | What the business gets | Outcome measure |
|---|---|---|---|---|
| E3 | Settle, deed in lieu, assets | 31 January 2027 | Settlements and deeds in lieu end to end to booking. Asset record, floor price and listing on HOME.SCB | Deed in lieu turnaround 26 to 12 days; restructure 23 to 5 days |
| E4 | Route decision | 28 February 2027 | The route recommended with reasons and approved inside the delegation for every new case. Guarantee and TCG claims. Auction rounds and RAMC transfer | Recovery rate on NPL 66.3 to 73 percent; NPA sales cycle 1,486 to 1,095 days |
| E5 | Litigation | 31 March 2027 | Litigation instructed and tracked end to end, law firms through the partner portal. Debt sale lot data and the buyer data room | Litigation turnaround 21 to 6 days; debt sale turnaround 45 days |
| E6 | Debt sale and write-off | 30 April 2027 | Debt sale screens and award, write-off committee, partner panel, allocation and fees | Manual processes removed towards 80 percent of the selected list; audit findings and fraud cases 50 to 13 |
| E7 | Deviations and partners | 31 May 2027 | Deviations X1 to X7 end to end. Partner scoring, conduct and the field app | Audit findings and fraud cases 50 to 13; override rate reported monthly |
| E8 | Administration and hardening | 30 June 2027 | Full administration, conduct checks, autonomy step-ups, regulatory returns, hardening | No code release for a rule, limit, template or panel change |

### 4.3 Expected outcomes by audience

| Audience | What changes |
|---|---|
| Customer (borrower) | Sees and accepts an offer, pays and raises a dispute on the bank's channels; receives statutory notices on a consented channel |
| Case owner | Works one list with a next action, a recommendation and the reasons, and is not asked to assemble data from four systems |
| Restructuring officer | Builds a settlement or TDR offer inside a range, sends it, and sees the booking confirmed from ACE |
| Sale and NPA officer | Sees the asset, its holding age, its costs and its price ladder on one screen, and sets a floor with the approval the policy names |
| Litigation officer and law firm | Prepare, verify and instruct a pack through the portal, and track hearings, fees and judgment on the case |
| Debt sale officer and buyer | Select, lot, tape, award and transfer on one path, with a masked tape and a data room |
| Write-off team and committee | Scan, pack, decide and post a write-off, and reconcile what was approved to what was posted |
| Partner and agency manager | Allocates on measured return, scores monthly, pays against results, and recalls every open case on exit |
| Risk, Compliance and audit | Reads one decision log with the rule, model and prompt versions; sees masked personal data; gets a data subject request answered inside the statutory period |
| Center of excellence | Changes a rule, limit, template or panel as a versioned load with a test and a rollback |

### 4.4 Delivery model under D-RCV-60

| Item | Statement |
|---|---|
| Services | 19 services inside ACE, one per business module P1 to P10 and S1 to S9, each with its own schema, login, REST base, Kafka topic and Temporal task queue (Architecture v5 slide 41, ADR-013, ADR-014) |
| Waves | Platform and Epic 1 wave 1, Epic 2 and Epic 3 wave 2, Epics 4 and 5 wave 3, Epics 6, 7 and 8 wave 4 (Template and Rules v1 R5.6) |
| Contracts | Contract-first REST, one hop from the gateway, 2 second timeout; a consuming service builds against the published contract and its fake (ADR-020) |
| Events | Kafka with an outbox per producer, an inbox per consumer, CloudEvents on `rwb.<service>.events.v1`, key `caseId` (ADR-015) |
| Workflow | A parent CaseWorkflow with a child workflow per stage, Temporal Schedules replacing the shared scheduler table, durable timers replacing the timer check job (ADR-016, D-RCV-036) |
| Rules | Rule packages governed in the decision service and evaluated by embedded Drools inside a workflow activity, with the package version written to the decision log (ADR-017, D-RCV-036 T7) |
| Reporting | No data lake; the reporting service builds its read model from events and holds the measures and regulatory extracts (ADR-018) |
| Edge | gateway-bff for staff screens, the partner gateway in the DMZ for partner users (ADR-019) |
| Releases | One production release at each month end, shared with the collection squad (Program BRD v5 section 7). Release dates in this document are unchanged and (tentative) |

## 5. Stakeholders and user groups

| Role | Interest | Decision rights |
|---|---|---|
| Product Owner | That the six epics deliver the business outcomes and stay inside scope | Approves scope and this document; decides priority between Must items |
| Business owner, settle and deed in lieu | Settlements, TDR plans and deeds in lieu reach booking and release | Approves the treatment policy for their product within the delegation |
| Business owner, route decision | That every case gets a route with reasons inside the delegation | Owns the route measure; decides the recommendation is fit to approve |
| Head of Litigation | That litigation is instructed and tracked and enforcement has an owner | Approves settlement before judgment, appeals and fee payment inside the delegation |
| Head of NPA | That assets are priced, listed and sold with an owner and a floor | Approves the floor price; approves RAMC and joint venture transfers |
| Head of Asset Liquidity | That debt sale runs against the policy cap and the reserve | Approves lots, reserve and tiered terms; approves the award |
| Write-off committee member | That the write-off population is eligible, packed and decided | Approves, rejects or defers a write-off inside the delegation |
| Credit approval committee | That a route above the case owner's limit is decided by committee | Decides a route above the delegated limit |
| Case owner | One list, one next action, a recommendation with reasons | Decides inside the case owner limit; refers up when above it |
| Restructuring officer (FCR) | Offers inside the range reach the customer and book | Builds and sends an offer; escalates an out-of-range offer |
| Sale officer | Assets and auctions, from floor price to transfer | Sets the start price; requests the floor; runs auction rounds |
| NPA and asset manager | The asset record, holding cost and provision step | Owns the asset stock position per case |
| Litigation officer | The pack, the firm, the hearing and the filing | Verifies the pack and approves filing |
| Law firm user | Instruction, filing and results through the portal | Records the filing and its results for its own firm |
| Enforcement owner | Enforcement from judgment to the end, with a review date | Defers enforcement with a coded reason and a review date |
| Debt sale officer | The sale population, the award and the transfer | Runs the sale and the award within the approval taken |
| Debt buyer and AMC | The data room, the bid and the transfer | Bids inside the bid window |
| Write-off team member | The scan, the pack and the population | Removes a case from the proposed population with a reason |
| Partner and agency manager | Panel, allocation, fees, scorecard, conduct and exit | Onboards a partner, approves fees, issues notice, ends a contract |
| Auction vendor | Auction rounds and bids | Runs a round and reports bids |
| Field collector | Field visits, photographs and bills | Records field evidence against the case |
| Guarantee officer | TCG and insurance claims inside the deadline | Prepares and files a claim |
| Complaint officer | Dispute and complaint resolution inside the service level | Resolves a complaint and returns the case |
| Hardship and vulnerability specialist | Contact limits and the hardship decision; deceased customer cases | Decides the hardship outcome; stops contact |
| Fraud investigator | The fraud referral and its outcome | Routes the case on the investigation outcome |
| Legal counsel | Notices, litigation, bankruptcy and estate positions | Approves a notice template; decides a legal position |
| Conduct and QA officer | That conduct is measured and a breach is raised | Samples decisions and contacts; raises a breach |
| Risk and model risk officer | Autonomy, drift, overrides and agent risk | Changes an autonomy level; approves a step-up |
| Center of excellence analyst | Rules, criteria and criteria changes as versioned data | Loads a validated rule version; runs a champion and challenger test |
| Platform administrator | Configuration, incidents and rollback | Rolls a configuration version back; manages an incident |
| Security administrator | Access by role and by agent | Approves access and reports the matrix |
| Compliance and PDPA officer | Masking, consent, retention and data subject rights | Approves masking and retention; answers a data subject request |
| Finance and CFO delegate | Provision inputs and benefit realisation | Accepts the provision inputs and the benefit report |
| Internal audit | The decision history of a population of cases | Requests the audit population and its decisions |
| Tribe lead | Volume, ageing, route mix, turnaround and recovery against the baseline | Owns the steering measures |
| ACE team lead | The ACE tables, columns and ingestion the views depend on | Accepts the ACE additions and their dates (DL43) |

Personal data classification for every row above: business roles only, `PII` where the role reads a customer identifier or contact point, `SENSITIVE_FINANCIAL` where the role reads balances, arrears, write-off or sale values. No customer data is copied into this document.

## 6. Current state and challenges

| # | Current state | Challenge it creates | Source |
|---|---|---|---|
| 1 | Recovery steps are spread across ALS, COLLINS, EFS, AMIS, RPS, LIT and WIN, with the case re-keyed at each hand-over | The case and the system of record disagree, and nobody can prove which version a decision used | Program BRD v5 sections 5.2, 5.3, 5.8 to 5.16 |
| 2 | Litigation takes 21 days of internal handling; a deed in lieu takes 26 days; a restructure takes 23 days; an NPA sale takes 1,486 days | Recovery value leaks in the waiting, and the customer experience is a series of unanswered steps | Program BRD v5 section 2 |
| 3 | The NPA stock balance, an eviction, enforcement after judgment and the write-off exception loop have no named owner | Nobody owes the next action; the case sits until someone notices | Specification v3 FEAT-AST-06, FEAT-AST-08, FEAT-LIT-20, FEAT-WOF-12 |
| 4 | 44 percent of TDR cases deviate from the approved range today | Deviation is normal, unmeasured and unaudited, and the approval path is bypassed | Business Rules v4 R-RES-10 |
| 5 | Asset prices, lot reserves and write-off populations sit in local spreadsheets | The population and the price cannot be reconciled to the book or defended to audit | Program BRD v5 sections 5.12 to 5.14, section 7 |
| 6 | Debt sale tapes are masked by hand, and partner work is exchanged by email | Personal data can leave the bank unmasked; instructions and results are not on the case | Program BRD v5 NFR-041, REQ-S9-008, Specification v3 FEAT-DBS-03 |
| 7 | Partner performance and fees are managed by memory, and a partner exit does not recall its cases | Cases stay with a firm that has left the panel; fees are paid without a measured result | Program BRD v5 REQ-S9-001 to REQ-S9-008 |
| 8 | Decisions are recorded in several places and not always with the rule, model and prompt version | An audit or regulatory question cannot be answered from one source | Program BRD v5 sections 5.7, 6.6 |
| 9 | Retention, masking and data subject rights are applied by discipline, not by class and role | A data subject request, a legal hold or a disposal cannot be proved | Program BRD v5 NFR-028, NFR-043, NFR-074 |

## 7. Scope

### 7.1 In scope

| Epic | Capabilities in scope | Features |
|---|---|---|
| E3 | Treatment record, settlement and TDR offer, validity and return, booking and schedule, broken plan, deed in lieu, buy-back rental, collateral release, asset take-on, holding age and provision step, stock balance, held property, floor price, listing, autonomy and drift | 31 features |
| E4 | Valuation and route decision, guarantee and TCG claims, insurance claim, auction rounds and vendor allocation, title transfer, proceeds and shortfall, RAMC, buy-back, rental, broker, self-service, contact repository, custody, payments and reconciliation | 50 features |
| E5 | Demand and recall notices, litigation pack, firm selection and instruction, filing, hearings and fees, settlement and appeal, judgment, enforcement, asset tracing, LED ladder, bankruptcy, debt sale lot building and data room | 26 features |
| E6 | Lot approval, buyer qualification, bidding, award, transfer and posting, put-back, write-off scan, pack, committee, posting and provision, exception loop, closure, criteria change, post charge-off recovery, partner panel, allocation, fees, benefit realisation | 37 features |
| E7 | X1 to X7 deviations end to end, override review, complaint matching, contact breach, partner scorecard, fees, review, notice, exit, conduct, extra asset costs, field app | 18 features |
| E8 | Regulatory returns, classification and re-ageing, champion and challenger, autonomy with approval, agent risk, administration screens, rule and limit change, treatment policy, template, rollback, panel change, QA sample, defective pack, hash chain, data subject request, incident, Aric referral, access control | 19 features |

### 7.2 Out of scope

| Out of scope | Where it is handled |
|---|---|
| Collections before day 90 and decisions D1 to D4 | EFS and the ACE collection module |
| Booking logic in the core bank (ALS) and credit approval in NLEADS | ALS and NLEADS; the Workbench records the result and reads the booked position back |
| COLLINS model development and the affordability calculation | Data and AI; the ACE restructure calculator |
| ACE ingestion, the ACE tables and columns, and the read-only views | The ACE team under the ACE DB additions (DL43) |
| Tracker retirement and local file archives | The Cutover plan (D-RCV-35 U5) |
| Partner systems and their internal processes | Each partner |
| Bank policy itself: the levels, limits and periods that the rules read | The policy owners, through DL18, DL22, DL23 and DL26 |
| Technical design beyond the confirmed v5 constraints | The PRDs per service and the architecture set |

### 7.3 Epics, services and waves under D-RCV-60

| Epic | Service epics that deliver it | Service wave | Business epic wave | Capability owner from the Ownership Map |
|---|---|---|---|---|
| E3 | RWB-SVC-S2 treatment, RWB-SVC-S5 asset, RWB-SVC-P8 payment, RWB-SVC-P10 agent | S2 2, S5 2, P8 2, P10 1 | 2 | S2 rwb-treatment, S5 rwb-asset, P8 rwb-payment, P10 rwb-agent |
| E4 | RWB-SVC-S1 valuation, RWB-SVC-S3 guarantee, RWB-SVC-S5 asset, RWB-SVC-P6 comms, RWB-SVC-P8 payment, RWB-SVC-S9 partner | S1 3, S3 3, S5 2, P6 1, P8 2, S9 4 | 3 | S1 rwb-valuation, S3 rwb-guarantee, S5 rwb-asset, P6 rwb-comms, P8 rwb-payment, S9 rwb-partner |
| E5 | RWB-SVC-S4 litigation, RWB-SVC-S6 debtsale, RWB-SVC-S9 partner | S4 3, S6 3, S9 4 | 3 | S4 rwb-litigation, S6 rwb-debtsale, S9 rwb-partner |
| E6 | RWB-SVC-S6 debtsale, RWB-SVC-S7 writeoff, RWB-SVC-S9 partner, RWB-SVC-P8 payment, RWB-SVC-P9 reporting | S6 3, S7 4, S9 4, P8 2, P9 1 | 4 | S6 rwb-debtsale, S7 rwb-writeoff, S9 rwb-partner, P8 rwb-payment, P9 rwb-reporting |
| E7 | RWB-SVC-S8 deviation, RWB-SVC-S9 partner | S8 2, S9 4 | 4 | S8 rwb-deviation, S9 rwb-partner |
| E8 | RWB-SVC-P4 access, RWB-SVC-P9 reporting, RWB-SVC-P10 agent | P4 1, P9 1, P10 1 | 4 | P4 rwb-access, P9 rwb-reporting, P10 rwb-agent |
| All | RWB-PLT-* platform epics and RWB-ITG-W1 to W4 | 0 and 1 to 4 | — | Platform and integration |

## 8. Business requirements

Epics 3 to 8 carry 181 features, written as 181 stories, of which 166 are Must and 15 are Should. The requirement set below states the same intent at business level: one testable need per row, a rationale, a priority that follows the stories it covers, and the source it comes from. Every row names the program requirements and features it comes from, so a reader can go from the business need to the feature. The backlog stories that test a requirement are held in the backlog and are not listed here, so a change to the backlog does not change this document. Requirement IDs are new in this document (ASM-2591); the program requirement IDs of the source are carried in the source column.

### 8.1 E3 Settle, deed in lieu and assets (31 stories)

| ID | Requirement | Priority | Rationale | Source |
|---|---|---|---|---|
| BR-001 | Every offer made to a customer exists as one treatment record holding its type, terms, approval and outcome. | Must | Without one record, the offer, the approval and the booking cannot be reconciled, and a dispute cannot be answered from the case | REQ-S2-001, REQ-CHO-006; FEAT-TRT-01 |
| BR-002 | A settlement is offered only inside the rule range, and an offer below the floor price goes to the approver or committee named by the limit before it is sent. | Must | Protects the recovery floor and puts the deviation in front of the authority that owns it | REQ-S2-004; FEAT-TRT-02, FEAT-TRT-03; R-SET-04, R-SET-05 |
| BR-003 | A TDR plan offer carries the affordability result from ACE and the model installment with the range the officer may move within. | Must | The plan must be affordable on the bank's own calculation, not on an officer's estimate | REQ-S2-002; FEAT-TRT-04, FEAT-TRT-05, FEAT-TRT-06 |
| BR-004 | An offer carries a validity period, and a decline or an expiry returns the case to the status it held before the offer. | Must | A case must not sit in an offer state after the customer has gone | REQ-S2-002, REQ-S2-003; FEAT-TRT-07, FEAT-TRT-09; R-RES-09, R-RES-17, R-RES-18 |
| BR-005 | A signed offer routes to operations for booking, and the booking is recorded on the case and confirmed from the next ACE account data. | Must | The case is only settled when the core bank says it is | REQ-S2-003, REQ-S2-008, REQ-CHO-008; FEAT-TRT-08, FEAT-TRT-10 |
| BR-006 | A broken plan raises an event and returns the case to the decision the rule names, rather than leaving it in a plan state. | Must | A plan that has failed is a recovery decision again, not a status to watch | REQ-S2-009; FEAT-TRT-11; R-RES-27 to R-RES-31 |
| BR-007 | A deed in lieu proves encumbrance and title eligibility before negotiation, and the transfer runs through documents and inspection to the asset record. | Must | A deed in lieu negotiated on an asset that cannot transfer wastes the negotiation and the holding cost | REQ-S2-005, REQ-S2-007; FEAT-TRT-12, FEAT-TRT-13, FEAT-TRT-14 |
| BR-008 | The treatment document set is generated from approved templates, and a deed in lieu buy-back rental runs its own record, auto-debit and receipt loop. | Must | Re-keying a contract is the defect the program exists to remove | REQ-S2-006, REQ-S2-010; FEAT-TRT-16, FEAT-TRT-18 |
| BR-009 | The collateral is released to CCMS only after the settlement has cleared, and the release is recorded on the case. | Must | A released security on an uncleared settlement is an unrecoverable loss | REQ-S2-008; FEAT-TRT-17 |
| BR-010 | Every repossessed or surrendered asset is recorded with its source, the date taken in, its holding cost and its provision step, and the statutory notice with proof of delivery is held on the case. | Must | The asset position and the notice are the two facts an auditor asks for first | REQ-S5-001; FEAT-AST-01, FEAT-AST-02, FEAT-AST-03, FEAT-AST-04 |
| BR-011 | Holding age drives the re-appraisal order and the provision step at each threshold the policy sets. | Must | Provision is a function of time held; leaving it to a person leaves it undone | REQ-S5-003; FEAT-AST-05, FEAT-AST-09 |
| BR-012 | The non performing asset stock balance has one named owner and is reported monthly. | Must | The balance has no owner today, so no one can be held to it | REQ-S5-002; FEAT-AST-06 |
| BR-013 | Maintenance, insurance and custody costs of a held property are recorded against the asset. | Must | Costs that are not recorded are not recovered from a sale | REQ-S5-001; FEAT-AST-07 |
| BR-014 | A disposal route is recommended with the expected return on each option, a start price and a floor are set with the floor approved by the named role, and the listing is published from one action. | Must | Price discipline is where the NPA sales cycle is won or lost | REQ-S5-004, REQ-S5-005; FEAT-AST-10, FEAT-AST-11, FEAT-AST-12 |
| BR-015 | An agent autonomy level is a versioned configuration row changed by the risk owner, and model drift raises a decision with an owner and a date. | Should | An agent that drifts without a decision is an uncontrolled credit decision | FEAT-AGT-12, FEAT-AGT-13 |

### 8.2 E4 Route decision, guarantees and auction (50 stories)

| ID | Requirement | Priority | Rationale | Source |
|---|---|---|---|---|
| BR-016 | An appraisal older than the policy limit triggers a new valuation order with no person asking for it. | Must | A route decided on a stale value is a wrong route | REQ-S1-001; FEAT-VAL-01 |
| BR-017 | The appraisal value arrives from SVAF through ACE, is linked to the collateral by business key, records the valuer, and is flagged before acceptance when it is an outlier against the market and the last value. | Must | Value is the largest single input to the route; it must be current, sourced and questioned | FEAT-VAL-02, FEAT-VAL-03, FEAT-VAL-04 |
| BR-018 | The expected return on each route is available at the decision with its model version, and the payoff and settlement range are calculated by rule from current balances with the floor applied. | Must | A route recommended without its return and its floor is an opinion | REQ-S1-003, REQ-S1-004; FEAT-VAL-05, FEAT-VAL-06 |
| BR-019 | The recommendation names the route, the reasons, the confidence and the alternatives considered. | Must | The approver must be able to see why, not only what | REQ-S1-005; FEAT-VAL-07 |
| BR-020 | A route is approved inside the delegation, goes to committee above the limit, is held with a review date where no route fits, and is reconsidered when a value, a payment or a deviation changes the picture. | Must | The decision is taken by the role that owns it, and it stays live while the facts move | REQ-S1-006, REQ-S1-008; FEAT-VAL-08, FEAT-VAL-09, FEAT-VAL-10, FEAT-VAL-11; R-UNI-01 to R-UNI-50 |
| BR-021 | Approving a route starts its flow and its timers in the same step. | Must | A route that is approved but not started is a case with no clock | REQ-S1-007; FEAT-VAL-12 |
| BR-022 | A TCG claim is prepared from case facts and filed inside the scheme deadline with the submission reference on the case, and is tracked to payment with a service level breach raised when it stalls. | Must | A claim filed late or untracked is money the bank never collects | REQ-S3-001, REQ-S3-002; FEAT-GUA-01, FEAT-GUA-02, FEAT-GUA-03; R-GUA-01 to R-GUA-32 |
| BR-023 | The subrogation position is recorded, the case closes when a guarantee payment clears the debt, and a rejected or reduced claim raises its reason and routes the residual to the next decision. | Must | What the guarantor may reclaim must not be lost, and a shortfall is a live recovery position | REQ-S3-003, REQ-S3-006; FEAT-GUA-04, FEAT-GUA-07 |
| BR-024 | Guarantors and co-borrowers are notified by rule on the approved template, and a guarantor who answers a demand enters the same treatment paths as a borrower. | Must | The guarantor is a party to the debt and must be reached on the same terms | REQ-S3-004, REQ-S3-005; FEAT-GUA-05, FEAT-GUA-06 |
| BR-025 | A collateral event (stolen, written off or damaged) files an insurance claim and triggers a re-appraisal before the next decision. | Must | The insurance recovery and the new value both change the route | FEAT-GUA-08 |
| BR-026 | An eviction of occupants from a held property is opened, tracked and closed with Legal named on it. | Must | The eviction has no legal owner today and blocks the sale | FEAT-AST-08 |
| BR-027 | Auction rounds step the price down the ladder until a bid clears the floor, a round with no bid re-lists at the next step, and the asset is allocated to a vendor by distance and capacity. | Must | A ladder run by hand is a price run by memory | REQ-S5-006; FEAT-AST-13, FEAT-AST-14, FEAT-AST-15, FEAT-AST-17; R-DIS-01 to R-DIS-72 |
| BR-028 | A bid below the floor needs a second signature, and the winning bidder's five-day payment term is enforced with the asset released when it is missed. | Must | A below-floor sale and an unpaid bid are the two ways an auction loses money | REQ-S5-007; FEAT-AST-16, FEAT-AST-18 |
| BR-029 | The title transfer is prepared and submitted for a vehicle through SCIS and recorded for a property at the Land Office. | Must | The bank does not own what it cannot transfer | REQ-S5-008; FEAT-AST-19, FEAT-AST-20 |
| BR-030 | Sale proceeds are applied to the case and any shortfall is raised to the next decision, and a pool transfer to RAMC or the joint venture, a customer buy-back, a third-party rental and a broker sale each carry their recorded approval. | Must | Every exit from a held asset ends in the same place: money applied or a residual decision | REQ-S5-009, REQ-S5-010; FEAT-AST-21, FEAT-AST-22, FEAT-AST-23, FEAT-AST-24, FEAT-AST-25 |
| BR-031 | The customer can see an offer, accept it, pay against it and raise a dispute on the bank's own channels, without a call or a branch visit. | Must | Every avoided call is capacity returned to the recovery floor | REQ-OCC-011; FEAT-COM-01 to FEAT-COM-04 |
| BR-032 | Contact points are held with verification and consent state per channel, custody movements of a document are recorded, a legal or audit document request is answered from the hub, and retention is applied when the case closes. | Must | A consent state and a custody trail are what makes a contact and a document defensible | REQ-OCC-006, REQ-DCM-019; FEAT-COM-05, FEAT-COM-06, FEAT-COM-07, FEAT-COM-08 |
| BR-033 | Settlement payments, auction and enforcement proceeds and fees are matched to the case, posted to ALS and the general ledger, and reconciled to the ACE position and the ledger every day. | Must | A recovery that is not matched is a recovery the book does not see | REQ-CHO-009; FEAT-PAY-03, FEAT-PAY-04, FEAT-PAY-05, FEAT-PAY-06, FEAT-PAY-07, FEAT-PAY-09, FEAT-PAY-10, FEAT-PAY-11 |

### 8.3 E5 Litigation and enforcement, debt sale preparation (26 stories)

| ID | Requirement | Priority | Rationale | Source |
|---|---|---|---|---|
| BR-034 | Demand and recall notices are produced and sent by rule, approved on the approval path, and their notice periods are timed from proof of delivery. | Must | The notice is the legal step that starts everything after it, and the period runs from delivery, not from posting | REQ-S4-001, REQ-APD-006; FEAT-LIT-01, FEAT-LIT-02, FEAT-LIT-03; R-LIT-01 to R-LIT-79 |
| BR-035 | The litigation pack is assembled from the document index and the case facts, tested against the known defect list, and a missing or lost document opens its recovery path. | Must | A pack filed with a known defect is the defect rate the program is trying to remove | REQ-S4-002; FEAT-LIT-04, FEAT-LIT-05, FEAT-LIT-06 |
| BR-036 | The litigation officer verifies the pack and approves filing, and a pack that fails the check returns to its owner with the defects named. | Must | The officer's signature is the control; it must be given against a checked pack | REQ-S4-003; FEAT-LIT-07, FEAT-ADM-09 |
| BR-037 | The law firm is selected from the panel by rule on scorecard, capacity, court and conflict, and instructed with the pack through the partner portal. | Must | Firm selection by habit is the largest uncontrolled legal cost | REQ-S4-004; FEAT-LIT-08, FEAT-LIT-09 |
| BR-038 | The filing confirmation and the court case number are recorded from the firm and matched to the lawsuit ACE ingests from LIT. | Must | A court number held only by the firm is a case the bank cannot trace | FEAT-LIT-10 |
| BR-039 | Hearings, deadlines and fees are tracked from the LIT hearings read through ACE and the firm's entries, each deadline is raised, and the next litigation step is recommended with reasons. | Must | Deadlines missed by email reading are the litigation turnaround | REQ-S4-005; FEAT-LIT-11, FEAT-LIT-12 |
| BR-040 | A settlement before judgment and an appeal each need the approval the limit names, and court fees and legal expenses are checked against the fee schedule and paid on approval. | Must | Money leaving the bank in a legal case leaves on an approval, not on a request | REQ-S4-006; FEAT-LIT-13, FEAT-LIT-14, FEAT-LIT-15 |
| BR-041 | The judgment is recorded with its date and amount, enforcement opens with one named owner from judgment to the end, and a deferral carries a coded reason and a review date. | Must | Enforcement after judgment has no owner today, which is where recovery stops | REQ-S4-007, REQ-S4-008; FEAT-LIT-16, FEAT-LIT-20 |
| BR-042 | Assets are traced for enforcement, the writ and seizure are applied for through the firm, the enforcement auction follows the 100, 90, 80 and 70 percent ladder of official value, and a bankruptcy petition is filed through the approver and the firm. | Must | Enforcement only pays if there is an asset, and the ladder is the statutory price path | FEAT-LIT-17, FEAT-LIT-18, FEAT-LIT-19, FEAT-LIT-21 |
| BR-043 | Enforcement proceeds are matched to the case and applied to the balance. | Must | Enforcement money that is not matched is money in suspense | REQ-S4-010; FEAT-LIT-22 |
| BR-044 | Accounts eligible for sale are selected by rule inside the policy cap, lots are built with an estimated price and an approved reserve, the data tape is masked before it reaches the data room, and the data room opens only to qualified buyers. | Must | The sale population and the tape are where a debt sale is won, and where personal data is lost | REQ-S6-001, REQ-S6-002, REQ-S6-003; FEAT-DBS-01, FEAT-DBS-02, FEAT-DBS-03, FEAT-DBS-04; R-DS-01 to R-DS-41 |

### 8.4 E6 Debt sale, write-off and partners (37 stories)

| ID | Requirement | Priority | Rationale | Source |
|---|---|---|---|---|
| BR-045 | A buyer passes the KYC, licensing and eligibility checks before it can bid, and a buyer that fails is barred and the lot released to the next bidder. | Must | An unqualified buyer cannot hold a bank's debt book | REQ-S6-004, REQ-S6-005; FEAT-DBS-06, FEAT-DBS-07 |
| BR-046 | A qualified buyer bids on a lot inside the bid window through the portal. | Must | The bid must come in on the case, not in an email | FEAT-DBS-08 |
| BR-047 | The lot is awarded against the reserve and the model with the approval the limit requires, and the sale agreement and the customer notices are generated from templates. | Must | The award price is the last control on the sale, and the customer has a right to be told | REQ-S6-006; FEAT-DBS-09, FEAT-DBS-10 |
| BR-048 | The awarded account data is transferred to the buyer and recorded, the sold accounts are derecognized and posted without re-keying, and the buyer remittance is confirmed against the award. | Must | The sale is only complete when the book and the money agree | REQ-S6-008; FEAT-DBS-11, FEAT-DBS-12, FEAT-DBS-15 |
| BR-049 | A put-back claim is reviewed against the sale terms and settled or refused with a reason, and an account awarded in a sold lot stops every other open action on its case the same day and the case closes. | Must | A sold case that keeps working creates work against a book the bank no longer owns | REQ-S6-007, REQ-S6-009; FEAT-DBS-13, FEAT-DBS-14 |
| BR-050 | The debt sale population is held inside the policy cap and the headroom is reported. | Must | The cap is a regulatory and board limit, not a target | FEAT-DBS-16 |
| BR-051 | The monthly eligibility scan runs on both tracks and each proposed account is tested against the tax criteria with the result recorded. | Must | An ineligible write-off is a tax and audit exposure | REQ-S7-001; FEAT-WOF-01, FEAT-WOF-02; R-WO-01 to R-WO-51 |
| BR-052 | The committee pack is assembled from the case facts, documents and recovery history, a case can be taken out of the population with a reason, and the population is routed to the committee queue and booked into the meeting. | Must | The committee decides on a pack, and a pack built by hand is a pack that arrives late | REQ-S7-002; FEAT-WOF-03, FEAT-WOF-04, FEAT-WOF-05 |
| BR-053 | The committee approves, rejects or defers a write-off per account inside its delegation, records the limit applied, and a rejection returns the case to recovery. | Must | The decision, the limit and the reason are the audit trail of a write-off | REQ-S7-003; FEAT-WOF-06, FEAT-WOF-07, FEAT-WOF-08 |
| BR-054 | An approved write-off posts to ALS and the general ledger, the provision is released, completeness is published, and the provision inputs reach Finance from the posted population. | Must | A write-off that is approved but not posted leaves an overstated book | REQ-S7-005; FEAT-WOF-09, FEAT-WOF-10; FEAT-PAY-08 |
| BR-055 | The approved and posted populations are reconciled, and every difference is raised. | Must | The difference between what the committee approved and what posted is the control that catches a wrong population | FEAT-WOF-11 |
| BR-056 | The write-off exception loop has one named owner and a time limit. | Must | This loop has no owner today, so its cases do not close | REQ-S7-004; FEAT-WOF-12 |
| BR-057 | A case closes after its retention period with no action open, and reopening a closed case needs a written rule, a reason and an approver. | Must | Closure without a control is how a written-off case returns to the list | REQ-S7-008; FEAT-WOF-13 |
| BR-058 | The write-off eligibility and tax criteria change as a versioned rule load by the center of excellence. | Should | Criteria are policy; a policy change must not need a release | FEAT-WOF-14 |
| BR-059 | A customer payment after charge-off is applied and recorded as a recovery, and a charged-off account is placed with an agency or sold under the placement and sale rules. | Must | Recovery after charge-off is a revenue stream, and its treatment is a rule | REQ-S7-006, REQ-S7-007; FEAT-WOF-15, FEAT-WOF-16, FEAT-PRM-06 |
| BR-060 | Every partner type is onboarded with its contract, fee schedule, service levels and scope, is allocated work by measured return with an override that carries a reason, and has its result on the case the same day with its recovery matched and its fee calculated. | Must | Allocation by measured return is the difference between a panel and a rota | REQ-S9-001 to REQ-S9-004; FEAT-PRM-01, FEAT-PRM-02, FEAT-PRM-03, FEAT-PRM-04, FEAT-PRM-05, FEAT-PRM-07 |
| BR-061 | Benefit realisation is tracked monthly against the baseline. | Must | A program that does not measure its own benefit cannot defend its cost | FEAT-RPT-06 |

### 8.5 E7 Deviations and partners (18 stories)

| ID | Requirement | Priority | Rationale | Source |
|---|---|---|---|---|
| BR-062 | X1 dispute and complaint runs end to end from detection through the evidence pack to resolution, inside its service level, and returns the case to the same decision with its timers resumed. | Must | A complaint that stops the case becomes a conduct finding | REQ-S8-001, REQ-S8-003; FEAT-DVF-01; R-DEV-01 to R-DEV-22 |
| BR-063 | X2 vulnerability and hardship follows the contact limits set for it and reaches a hardship or relief decision. | Must | Contact outside the limit is a regulatory breach against a vulnerable customer | REQ-S8-002; FEAT-DVF-02 |
| BR-064 | X3 deceased customer stops all contact, notifies the heirs and the estate, files the insurance claim and settles the estate position. | Must | Contact after a death is the most serious conduct failure the bank can have | REQ-DVH-008; FEAT-DVF-03 |
| BR-065 | X4 fraud refers the case to the fraud team, holds recovery action until the flag is confirmed or cleared, tracks the investigation and routes the case on the outcome. | Must | Recovery action against a fraud case destroys evidence and creates a complaint | REQ-DVH-010; FEAT-DVF-04, FEAT-ADM-13 |
| BR-066 | X5 bankruptcy and external seizure stop direct collection and file the claim with the receiver or the Legal Execution Department before the deadline. | Must | A missed claim deadline is a debt that can never be recovered | REQ-DVH-009; FEAT-DVF-05 |
| BR-067 | X6 lost contact runs the skip trace through the bureau, internal data and agency sources and returns the case to a decision whether or not contact is restored. | Must | A case that waits on contactability is a case that never moves | REQ-S8-004; FEAT-DVF-06 |
| BR-068 | X7 collateral event files the insurance claim, re-appraises the collateral and returns the case to the route decision. | Must | The value and the insurance position both change the route | REQ-S8-005; FEAT-DVF-07 |
| BR-069 | Overrides are put to the review forum monthly with the reason and the outcome of each, a complaint is matched to the contact that preceded it, and a contact sent while a block is on opens the breach path. | Must | Override and conduct are measurable only if they are collected on purpose | REQ-S8-006, REQ-DVH-007; FEAT-DVF-08, FEAT-DVF-09, FEAT-DVF-10 |
| BR-070 | Every partner is scored monthly from the measured results, its fees are checked against the schedule and the result and approved, it is reviewed on the six points every partner type is managed on, a missed target sends the contractual notice and starts the cure period, an exit recalls every open case, and conduct is sampled with breaches raised. | Must | A panel that is not scored, reviewed and exited is an unmanaged cost base | REQ-S9-005, REQ-S9-006, REQ-S9-007; FEAT-PRM-08, FEAT-PRM-09, FEAT-PRM-10, FEAT-PRM-11, FEAT-PRM-12, FEAT-PRM-13 |
| BR-071 | Additional partner costs and services on a held asset are recorded and approved, and field visits, photographs and bills are captured through the field app, including with no network connection. | Must | Field evidence that is not captured on the case is not evidence | REQ-S9-009; FEAT-PRM-14, FEAT-PRM-15 |

### 8.6 E8 Administration, conduct, autonomy and reporting (19 stories)

| ID | Requirement | Priority | Rationale | Source |
|---|---|---|---|---|
| BR-072 | Administration is one place for roles, queues, parameters, templates, panels and autonomy. | Should | Six change paths in six screens is how a parameter drifts from the policy | REQ-ACA-013; FEAT-ADM-01 |
| BR-073 | A decision rule is changed by the center of excellence, tested and put in force as a new version, and any versioned table is rolled back to its previous version with the rollback recorded. | Should | A rule change with no test and no rollback is a production risk taken on policy | REQ-CWC-013; FEAT-ADM-02, FEAT-ADM-06 |
| BR-074 | A delegated approval limit is moved with Risk approving and the change versioned, and the treatment policy of a product is set by its product head. | Should | The delegation of authority is the control that a limit change most easily breaks | REQ-APD-010; FEAT-ADM-03, FEAT-ADM-04 |
| BR-075 | A letter template is added through the Compliance approval path with the approver recorded against the version. | Should | An unapproved template is an unapproved legal communication | REQ-OCC-002; FEAT-ADM-05 |
| BR-076 | A partner panel change is published with an effective date. | Should | A panel change that is not dated cannot be applied to a case fairly | FEAT-ADM-07 |
| BR-077 | A QA sample of closed decisions is tested against the rule version that was in force when each was taken. | Must | Testing a decision against today's rule tests nothing | FEAT-ADM-08 |
| BR-078 | A pack that fails the check is returned to its owner with the defects named, and a broken hash chain in the decision log raises a control breach. | Must | The two integrity controls that tell the bank its evidence can be trusted | FEAT-ADM-09, FEAT-ADM-10; REQ-DRI-003 |
| BR-079 | A data subject access, correction or erasure request is worked inside the statutory period. | Must | Statutory duty, and a measure Compliance reports on | NFR-043, REQ-S8-007; FEAT-ADM-11 |
| BR-080 | An incident runs the path detect, hold, fix, record and report. | Should | An incident that is not held and recorded becomes a second incident | FEAT-ADM-12 |
| BR-081 | What each role and each agent may read and do is reviewed, set and reported as a matrix. | Should | An agent holds a permission; someone must be able to say which | REQ-ACA-003, REQ-ACA-010; FEAT-ADM-14 |
| BR-082 | Regulatory returns are produced from the data products and the decision log. | Must | The return must agree with the decision record, not with a separate count | FEAT-RPT-07 |
| BR-083 | The classification, staging and re-ageing rules are applied, and the segment is recomputed when they change. | Must | A stale classification misstates the book to the regulator | FEAT-RPT-10 |
| BR-084 | Two rule or model versions run side by side and are compared, an autonomy level is raised or lowered on measured evidence with the approval each change needs, and agent performance, overrides and incidents go to the strategy and model committee. | Must | Autonomy is earned on evidence and reviewed, or it is a decision nobody watches | FEAT-AGT-14, FEAT-AGT-15, FEAT-AGT-16 |

## 9. Business rules and policies

The Workbench holds 448 routing rules in ten route sets, with hit policy Unique, and every rule is a versioned data row (Business Rules and Routing Logic v4). The rules below are the business rules and policies that bind Epics 3 to 8. Each names the rule family that implements it.

| ID | Rule or policy | Priority | Applies to | Source |
|---|---|---|---|---|
| RULE-001 | Every threshold, limit, timer, queue, role, template and route is a versioned data row, changed through a validated load without a code release, and rolled back by one call. | Must | All epics | REQ-CWC-013, REQ-CWC-014; Program BRD v5 section 7 Principle 1; D-RCV-036 T4 |
| RULE-002 | Every decision writes one append-only record with the rule, model, agent and prompt versions, an inputs snapshot, the recommendation, the approval and the outcome, and no action proceeds if the record cannot be written. | Must | All epics | REQ-DRI-001, REQ-DRI-002, REQ-DRI-005; R-UNI-01 to R-UNI-50 |
| RULE-003 | A settlement is offered only between the settlement range low and high; an offer below the floor price goes to the approver named by the limit. | Must | E3 | R-SET-04, R-SET-05, R-SET-06; REQ-S2-004 |
| RULE-004 | An offer carries a validity period from reference data; a decline or an expiry returns the case to the status it held before the offer. | Must | E3, E4 | R-RES-09, R-RES-17, R-RES-18, R-SET-11; REQ-S2-002, REQ-S2-003 |
| RULE-005 | A missed installment starts the cure period; when the cure period expires the plan is broken, and beyond the maximum number of breaks a further restructure is barred and the route is re-run. | Must | E3 | R-RES-27 to R-RES-32; REQ-S2-009 |
| RULE-006 | A deed in lieu runs only after the encumbrance and title check passes, and the asset is unlocked as a non performing asset only where the auto-unlock rule qualifies. | Must | E3 | R-DIL-01 to R-DIL-37; REQ-S2-005, REQ-S2-007 |
| RULE-007 | An asset price steps down the ladder at each round, a round with no bid re-lists at the next step, and a bid below the floor needs a second signature. | Must | E3, E4 | R-DIS-01 to R-DIS-72; REQ-S5-006, REQ-S5-007 |
| RULE-008 | The winning bidder's payment is due inside the five-day term, and the asset is released where the term is missed. | Must | E4 | FEAT-AST-18 |
| RULE-009 | The enforcement auction follows the 100, 90, 80 and 70 percent steps of official value. | Must | E5 | FEAT-LIT-19 |
| RULE-010 | A decision that departs from the recommendation needs a coded override reason, and the reasons are reported monthly. | Must | E3 to E8 | REQ-APD-005; R-UNI-01 to R-UNI-50 |
| RULE-011 | A decision that needs approval goes to the approver the delegation of authority table names for that decision, product and amount; a request above a limit escalates to the next approver and is never silently approved. | Must | E3 to E8 | REQ-APD-001, REQ-APD-004, REQ-APD-009, REQ-APD-010 |
| RULE-012 | A deviation pauses the stage clock, keeps the prescription clock running and does not replace the case state. | Must | E3 to E8 | REQ-DVH-002 |
| RULE-013 | Contact stops apply automatically for a dispute or complaint, a vulnerable or hardship case and a deceased customer, and a statutory notice continues where a channel consent is withdrawn. | Must | E3, E7 | REQ-DVH-004, REQ-OCC-006, REQ-DVH-008 |
| RULE-014 | A deviation code with no named owner routes to the team manager and is recorded as unmapped. | Must | E7 | REQ-DVH-003 |
| RULE-015 | The debt sale population stays inside the policy cap, and no unmasked personal data leaves the bank in a tape or a data room. | Must | E5, E6 | REQ-S6-001, REQ-S6-003; NFR-041; FEAT-DBS-01, FEAT-DBS-03 |
| RULE-016 | A buyer is admitted to bid only after the KYC, licensing and eligibility checks pass; a licence breach bars the buyer and releases the lot to the next bidder. | Must | E6 | R-DS-01 to R-DS-41; REQ-S6-004, REQ-S6-005 |
| RULE-017 | A lot is awarded only against the reserve and the model test, with the approval the limit requires. | Must | E6 | REQ-S6-006 |
| RULE-018 | An account awarded in a sold lot stops every other open action on its case the same day, and a put-back claim is decided against the sale terms with a reason. | Must | E6 | REQ-S6-007, REQ-S6-009 |
| RULE-019 | Write-off eligibility and the tax criteria are tested by rule on a monthly scan of both tracks, and the committee decides inside its delegation with the limit recorded. | Must | E6 | REQ-S7-001, REQ-S7-003; R-WO-01 to R-WO-51 |
| RULE-020 | The approved and posted write-off populations are reconciled and every difference is raised, and no write-off is posted without its approval. | Must | E6 | FEAT-WOF-11, REQ-S7-005 |
| RULE-021 | Post charge-off treatment, including placement with an agency and the sale of a charged-off population, is set by rule. | Must | E6 | REQ-S7-006; R-WO-01 to R-WO-51 |
| RULE-022 | A case closes after its retention period with no action open, and a reopening needs a written rule, a reason and an approver. | Must | E6 | REQ-S7-008 |
| RULE-023 | Partner work is allocated on measured return against the scorecard, an override carries a reason, and a fee is calculated from the contracted schedule and paid against a recorded result. | Must | E6, E7 | REQ-S9-003, REQ-S9-004 |
| RULE-024 | A partner that misses its service level is chased once and then has its work recalled, and a panel exit, a declared conflict, insolvency or an upheld conduct breach recalls every open case it holds. | Must | E7 | REQ-S9-005, REQ-S9-006 |
| RULE-025 | A prescription warning forces a litigation review ahead of every other open action on the case. | Must | E5 | REQ-S4-009 |
| RULE-026 | Enforcement after judgment has one named owner, and a deferral carries a coded reason and a review date. | Must | E5 | REQ-S4-007, REQ-S4-008 |
| RULE-027 | Every outbound contact carries a conduct check, and a contact without one, or one against a block or a withdrawn consent, is held. | Must | E3 to E7 | REQ-OCC-005, REQ-OCC-006; NFR-038 |
| RULE-028 | Personal data is masked by role on every screen and in every agent call, and the customer identification number leaves ACE masked. | Must | All epics | REQ-ACA-005, REQ-RDF-010; NFR-039, NFR-040 |
| RULE-029 | Agents run under service identities and pass the same role checks as people, and an autonomy level changes only as a versioned configuration row with the approval the change needs. | Must | E3, E8 | REQ-ACA-010; FEAT-AGT-12, FEAT-AGT-15; NFR-078 |
| RULE-030 | No source data is copied into the Workbench: ACE ingests it, the Workbench reads the read-only views and links by ACE business key, with no foreign key into ACE. | Must | All epics | D-RCV-35 U1, U4; REQ-DRI-006; ADR-010 |
| RULE-031 | A rule answer is deterministic: it is evaluated inside a workflow step, the package version is chosen at evaluation and written to the decision log, and an agent failure falls back to the rule result. | Must | All epics | D-RCV-036 T5, T7; NFR-024, NFR-055; ADR-017 |
| RULE-032 | Release dates are copied unchanged from the source and are tentative. | Must | All epics | Template and Rules v1 U7, DL48 |

## 10. Success measures

The eight program measures are the business case for Epics 3 to 8, and each is read from the decision log per decision (Program BRD v5 section 2). Epic-level measures are added where the sources give a target. A measure with no target in the sources is recorded as such and carried as an open question.

| ID | Measure | Baseline | Target | How it is measured | Source |
|---|---|---|---|---|---|
| KPI-001 | Recovery rate on non performing loans | 66.3% (2026 to date) | 73% | Realized recovery against the non performing book, per decision, from the decision log | Program BRD v5 section 2 |
| KPI-002 | Litigation turnaround | 21 days | 6 days | Median days from the notice decision to filing, by case | Program BRD v5 section 2 |
| KPI-003 | Deed in lieu turnaround | 26 days | 12 days | Median days from the route decision to the asset record, by case | Program BRD v5 section 2 |
| KPI-004 | Restructure turnaround | 23 days | 5 days | Median days from the route decision to the booking, by case | Program BRD v5 section 2 |
| KPI-005 | Debt sale turnaround | Not specified in the source documents (GAP-1485; ASM-2597) | 45 days | Days from lot selection to award and transfer, per lot | Program BRD v5 section 2 |
| KPI-006 | Manual processes removed | Near zero | 80% of the selected list | Count of manual steps removed against the selected list agreed with the Tribe | Program BRD v5 section 2 |
| KPI-007 | Audit findings and fraud cases | 50 | 13 | Count of findings raised against the recovery process and its cases, per audit cycle | Program BRD v5 section 2 |
| KPI-008 | NPA sales cycle | 1,486 days | 1,095 days | Median days from asset take-on to sale completion | Program BRD v5 section 2 |
| KPI-009 | Case packs and write-off returns right first time | Not specified in the source documents (GAP-1486; ASM-2598) | 90% | QA sample of closed packs and returns, tested against the rule version applied | NFR-037; FEAT-ADM-08 |
| KPI-010 | Document classification correct on the labelled sample | Not specified in the source documents (GAP-1487; ASM-2599) | 90% correct | Labelled sample, with everything below the confidence threshold counted to the review queue | NFR-017 |
| KPI-011 | Override rate per decision and product | Not specified in the source documents (GAP-1488; ASM-2600) | Reported monthly, no target | Overrides with a coded reason against recommendations, per decision and product | REQ-APD-005 |
| KPI-012 | Agent acceptance, override, latency and cost | Not specified in the source documents (GAP-1489; ASM-2601) | Measured per agent, no target | Agent runs, their outcome, the override applied and the elapsed time, from the agent run record | NFR-066 |
| KPI-013 | Case list reconciles to the ACE account view | Not specified in the source documents (GAP-1490; ASM-2602) | No unexplained variance | Daily reconciliation of the case list to the account view, variance reported by data product | REQ-RDF-007; NFR-018 |
| KPI-014 | Benefit realisation against the baseline | Not specified in the source documents (GAP-1483; ASM-2588) | Tracked monthly, targets not set | Benefit model measures against the baseline, monthly | FEAT-RPT-06 |

## 11. Assumptions, constraints, dependencies and risks

### 11.1 Assumptions

| ID | Assumption | Confidence | Register row | Confirm with |
|---|---|---|---|---|
| ASM-001 | This document stays at status Draft until the Product Owner approves it; the run does not wait for that approval. | High | ASM-2590 | Product Owner |
| ASM-002 | Release dates are the ones in the Program BRD release plan, copied unchanged and tentative. | High | ASM-2591 | Program manager |
| ASM-003 | Business owners are named by role only; no person is named anywhere in this document or in its source. | High | ASM-2592 | Product Owner |
| ASM-004 | Requirement IDs BR-001 to BR-084 are new in this document; the program IDs REQ-* are carried in the source column so the two sets reconcile. | Medium | ASM-2593 | Business analyst |
| ASM-005 | Every owner named in a requirement is the business role of the source plus the service that owns the capability in the Ownership Map. | Medium | ASM-2594 | Solution architect |
| ASM-006 | The D-RCV-60 split into 19 services changes who delivers a capability and in which wave, not what the business needs. | Medium | ASM-2595 | Solution architect |
| ASM-007 | Program requirements from Epics 1 and 2 stay valid at their published version where Epics 3 to 8 rely on them. | High | ASM-2596 | Product Owner |
| ASM-008 | The approval limits, ranges, floors, periods and criteria that the rules read are loaded from reference data and are not restated here. | High | ASM-2569 | Risk with the product heads |
| ASM-009 | The settlement range and the floor are read from reference data per product; no value is asserted in this document. | High | ASM-2570 | Product head |
| ASM-010 | The offer validity, cure period, maximum breaks and the queue and approval timers are parameters, not fixed values. | High | ASM-2571 | Business lead |
| ASM-011 | The statutory notice periods are held in the legal periods reference table and are not restated here. | High | ASM-2572 | Legal counsel |
| ASM-012 | The provision step thresholds and the re-appraisal interval are policy parameters held as data. | High | ASM-2573 | NPA and asset manager |
| ASM-013 | The write-off tax criteria and the meaning of both tracks are held as a versioned rule package. | Medium | ASM-2574 | Write-off committee member |
| ASM-014 | The write-off exception loop is owned by the write-off team until a named owner is decided. | Low | ASM-2575 | Head of recovery |
| ASM-015 | Enforcement after judgment is owned by the enforcement owner role, and an eviction is owned by the sale officer with Legal named on it. | Medium | ASM-2576 | Head of Litigation |
| ASM-016 | The non performing asset stock balance is owned by the NPA and asset manager role. | Medium | ASM-2577 | Head of NPA |
| ASM-017 | The debt sale cap is the 54 percent figure in the specification, applied to the eligible population of the period the policy names. | Medium | ASM-2578 | Head of Asset Liquidity |
| ASM-018 | Buyer qualification uses the existing bank KYC and licensing checks applied by the debt sale officer, held as data. | Medium | ASM-2579 | Compliance and PDPA officer |
| ASM-019 | Retention periods and masking rules by record class and role come from DL26 and are applied as reference data. | High | ASM-2580 | Compliance and PDPA officer |
| ASM-020 | The TCG quota and claim deadlines are held as reference data per scheme. | Low | ASM-2581 | Guarantee officer |
| ASM-021 | The measured evidence and threshold for an autonomy change are set by Risk before the first change is made. | Low | ASM-2582 | Risk and model risk officer |
| ASM-022 | The deceased customer flow is read as an E7 deviation flow, with the E3 program requirement served through it. | Medium | ASM-2583 | Product Owner |
| ASM-023 | E3 stories that depend on an E4 feature are tested against the published contract and its fake until the E4 feature lands. | Medium | ASM-2584 | Solution architect |
| ASM-024 | An E3 autonomy change is served by the E1 configuration path until the E8 administration screen arrives. | Medium | ASM-2585 | Risk and model risk officer |
| ASM-025 | Regulatory extracts are built from the reporting read model and the decision log, with no data lake. | High | ASM-2586 | Solution architect |
| ASM-026 | The partner instruction capability is read as E4 for the API and E6 for allocation, as the two sources say. | Low | ASM-2587 | Partner and agency manager |
| ASM-027 | The benefit model measures and baselines are supplied by the business case before benefit realisation is reported. | Low | ASM-2588 | Finance and CFO delegate |
| ASM-028 | The S6 service wave of 3 and the E6 business epic wave of 4 are sequenced so that lot building lands in E5 and award in E6. | Medium | ASM-2589 | Solution architect |
| ASM-029 | The debt sale turnaround is measured from lot selection to award and transfer, and the 45 day target stands until a baseline is set. | Medium | ASM-2597 | Head of Asset Liquidity |
| ASM-030 | First-time-right on case packs and write-off returns is measured on the QA sample of closed items, at the 90 percent target. | Medium | ASM-2598 | Conduct and QA officer |
| ASM-031 | Document classification is measured on the labelled sample, at the 90 percent target. | Medium | ASM-2599 | Platform administrator |
| ASM-032 | The override rate is reported monthly by decision and product with no target until one is set. | Medium | ASM-2600 | Center of excellence analyst |
| ASM-033 | Agent acceptance, override, latency and cost are measured per agent from the agent run record, with no target until one is set. | Medium | ASM-2601 | Risk and model risk officer |
| ASM-034 | The daily case list reconciliation reports variance by data product until a tolerance is agreed. | Medium | ASM-2602 | Data steward and data product owner |

### 11.2 Constraints

| ID | Constraint | What it means |
|---|---|---|
| CON-001 | Built on ACE | The Workbench stays inside ACE: the same cluster, the same App Gateway, the shared ACE services and the ACE database |
| CON-002 | 19 services inside ACE | One service per business module, each with its own schema, login, contract, topic and task queue; a module never reads another module's tables (ADR-013, ADR-014) |
| CON-003 | Contract-first | A service builds against the published contract and its fake; one hop from the gateway, 2 second timeout (ADR-020) |
| CON-004 | Source data through ACE ingestion | Every source lands in ACE; the Workbench reads the read-only views and holds no copy, load or staging table (D-RCV-35, ADR-010) |
| CON-005 | Temporal from Epic 3 | The case lifecycle runs as one parent workflow per case with a child workflow per stage; a wait is a durable timer, not a routed state (D-RCV-036, ADR-016) |
| CON-006 | Embedded Drools | Rules are versioned data evaluated in-process; no rules server, no external engine (D-RCV-036 T3, ADR-017) |
| CON-007 | No data lake | Reporting reads events and the decision log; the data lake copy is retired (ADR-018) |
| CON-008 | Monthly releases | One production release at each month end, shared with the collection squad (Program BRD v5 section 7) |
| CON-009 | ACE team dependency on the data | The ACE team owns every table and column the views read, and its additions gate the features that need them (DL43) |
| CON-010 | Personal data | No production data in a prompt, a test or a log; masking is by role and the customer identifier leaves ACE masked (NFR-039, NFR-045) |
| CON-011 | Language | Customer documents in Thai by default, Thai and English for screens and messages (NFR-057 to NFR-059) |
| CON-012 | Policy is not changed here | The levels, limits and periods the rules read are the policy owners' decision (DL18, DL22, DL23, DL26) |

### 11.3 Dependencies

| ID | Dependency | Depends on | Needed by |
|---|---|---|---|
| DEP-001 | Case layer, owner, queue, timer and approval path | Epics 1 and 2 | E3 start |
| DEP-002 | Read-only ACE views, freshness stamp and reconciliation | rwb-source-data and the ACE additions (DL43) | E3 valuation and asset take-on |
| DEP-003 | Decision log, rule package governance and the approval workflow | rwb-decision | E3 onward |
| DEP-004 | Document hub, templates and the evidence pack | rwb-document and rwb-comms | E3 treatment documents, E5 pack |
| DEP-005 | Payment and proceeds matching, fees and posting | rwb-payment | E3 booking, E4 proceeds, E6 write-off |
| DEP-006 | Collateral and appraisal data from CCMS and SVAF, ingested by ACE | The ACE team and SVAF | E3 deed in lieu, E4 valuation |
| DEP-007 | Lawsuit, hearing and ledger data from LIT and the LED | The ACE team and the law firms in the partner portal | E5 |
| DEP-008 | Asset and stock data from AMIS and RPS | The ACE team | E3 asset record |
| DEP-009 | Partner portal and the external gateway | rwb-partner and the edge | E4 instructions, E5 firms, E6 buyers, E7 field app |
| DEP-010 | Reporting read model and regulatory extracts | rwb-reporting | E6 benefit tracking, E8 returns |

### 11.4 Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| RISK-001 | The ACE additions (DL43) land late and the E4 valuation and E3 asset features cannot run on real data | Medium | High | Build against the contract and the fake, keep the features behind their flags, and run the reconciliation on synthetic data until the additions land |
| RISK-002 | The 19-service split delays a business epic because a capability sits in a later wave than the epic (ASM-2589) | Medium | High | Sequence by contract: consume the published contract and its fake, and confirm the E5 and E6 lot sequence with the solution architect |
| RISK-003 | Approval limits and ranges stay undecided (DL18) and the authorization rules cannot be tested | High | High | Load the regulation's levels now, keep the values as data, and let the test use a documented test set |
| RISK-004 | The write-off cap, tax criteria and exception ownership stay undecided, and the write-off population cannot be defended | Medium | High | Hold the criteria as a versioned package, reconcile approved to posted, and name the exception owner before E6 |
| RISK-005 | Debt sale personal data leaves the bank unmasked | Low | High | Masking before the tape is built, a masking check in the release gate, and an access log per read |
| RISK-006 | A deviation carries no owner and the case stalls (RULE-014) | Medium | Medium | Route an unmapped code to the team manager and report it monthly |
| RISK-007 | Partners keep work after an exit or a conduct breach | Medium | Medium | Recall by rule on the exit event, and report every recalled case |
| RISK-008 | Autonomy steps up on evidence that is not measured | Medium | High | Autonomy changes only through a versioned row with the approval each change needs, and agent measures are reported per agent |
| RISK-009 | Retention and masking rules are not set (DL26) and a disposal or a data subject request cannot be proved | Medium | Medium | Apply a record class to every document and hold the disposal as a recorded decision |
| RISK-010 | A rule change reaches production without its test or its rollback | Low | High | Validated load, test cases and one-call rollback, with the rollback recorded |

## 12. Open questions

Each question is a gap row in the register and has its assumption listed in section 11.1. None of them stops this document from being read or reviewed; each one must be answered before the requirement it names is accepted.

| ID | Question | Owner role | Blocks | Gap | Assumption |
|---|---|---|---|---|---|
| Q-001 | What is each approval limit, by decision, product and amount, and who is the substitute for each (DL18)? | Risk with the product heads | BR-002, BR-020, BR-028, BR-040, BR-053, RULE-011 | GAP-1464 | ASM-2569 |
| Q-002 | What is the settlement range, and what is the floor price basis, for each product? | Product head (Mortgage, HP, SSME) | BR-002, BR-018, RULE-003 | GAP-1465 | ASM-2570 |
| Q-003 | What are the offer validity period, the cure period, the maximum number of breaks, and the queue and approval timers (DL22, DL23)? | Business lead | BR-004, BR-006, RULE-004, RULE-005 | GAP-1466 | ASM-2571 |
| Q-004 | What are the statutory notice periods, and what service level applies to each litigation step? | Legal counsel | BR-034, RULE-025 | GAP-1467 | ASM-2572 |
| Q-005 | What are the provision step thresholds and the re-appraisal interval for a held asset? | NPA and asset manager | BR-010, BR-011 | GAP-1468 | ASM-2573 |
| Q-006 | What are the write-off tax criteria, and what are the two tracks the monthly scan runs on? | Write-off committee member | BR-051, RULE-019 | GAP-1469 | ASM-2574 |
| Q-007 | Which role owns the write-off exception loop, and what is its time limit? | Head of recovery | BR-056, RULE-020 | GAP-1470 | ASM-2575 |
| Q-008 | Which role owns enforcement after judgment, and which role owns the eviction of a held property? | Head of Litigation | BR-026, BR-041, RULE-026 | GAP-1471 | ASM-2576 |
| Q-009 | Which role owns the non performing asset stock balance? | Head of NPA | BR-012, RULE-001 | GAP-1472 | ASM-2577 |
| Q-010 | What is the basis and the period of the debt sale cap, beyond the 54 percent figure? | Head of Asset Liquidity | BR-050, BR-044, RULE-015 | GAP-1473 | ASM-2578 |
| Q-011 | What licensing and eligibility criteria must a debt buyer meet, and who may bar it? | Compliance and PDPA officer | BR-045, RULE-016 | GAP-1474 | ASM-2579 |
| Q-012 | What are the retention periods and the masking rules, by record class and by role (DL26)? | Compliance and PDPA officer | BR-032, BR-057, BR-079, RULE-028 | GAP-1475 | ASM-2580 |
| Q-013 | What is the TCG quota and the claim deadline for each scheme? | Guarantee officer | BR-022, RULE-001 | GAP-1476 | ASM-2581 |
| Q-014 | What measured evidence and threshold justify raising or lowering an agent autonomy level? | Risk and model risk officer | BR-015, BR-084, RULE-029 | GAP-1477 | ASM-2582 |
| Q-015 | Which epic owns the deceased customer flow: E3 (REQ-DVH-008) or E7 (FEAT-DVF-03)? | Product Owner | BR-064, the E3 and E7 scope | GAP-1478 | ASM-2583 |
| Q-016 | How is E3 released before the E4 features it depends on (FEAT-VAL-01, FEAT-VAL-06)? | Solution architect | BR-002, BR-018, BR-020, the E3 release | GAP-1479 | ASM-2584 |
| Q-017 | How does an E3 feature depend on an E8 administration feature (FEAT-CWC-22 for FEAT-AGT-12)? | Solution architect | BR-015, the E3 release | GAP-1480 | ASM-2585 |
| Q-018 | FEAT-RPT-07 names a data lake, which ADR-018 removes: where do the regulatory extracts read from? | Solution architect | BR-082, KPI-014 | GAP-1481 | ASM-2586 |
| Q-019 | Is the partner instruction capability in E4 (the endpoint list) or in E6 (FEAT-PRM-03)? | Partner and agency manager | BR-037, BR-060, the E4 release | GAP-1482 | ASM-2587 |
| Q-020 | What benefit model measures and baselines does benefit realisation report against? | Finance and CFO delegate | KPI-005, KPI-009 to KPI-014, BR-061 | GAP-1483 | ASM-2588 |
| Q-021 | How are the S6 service wave (3) and the E6 business epic wave (4) sequenced, so that lot building lands in E5 and award in E6? | Solution architect | BR-044, BR-047, the E5 and E6 releases | GAP-1484 | ASM-2589 |
| Q-022 | What is the debt sale turnaround baseline, given that the sources state a target of 45 days and no baseline? | Head of Asset Liquidity | KPI-005 | GAP-1485 | ASM-2597 |
| Q-023 | What is the baseline for case packs and write-off returns right first time, against the 90 percent target? | Conduct and QA officer | KPI-009 | GAP-1486 | ASM-2598 |
| Q-024 | What is the baseline for document classification accuracy on the labelled sample, against the 90 percent target? | Platform administrator | KPI-010 | GAP-1487 | ASM-2599 |
| Q-025 | What target applies to the override rate, which is reported monthly with no target set? | Center of excellence analyst | KPI-011 | GAP-1488 | ASM-2600 |
| Q-026 | What targets apply to agent acceptance, override rate, latency and cost? | Risk and model risk officer | KPI-012 | GAP-1489 | ASM-2601 |
| Q-027 | What variance tolerance applies to the daily case list reconciliation (DL25)? | Data steward and data product owner | KPI-013 | GAP-1490 | ASM-2602 |

## 13. Governance and approval

| Gate | What is decided | Evidence |
|---|---|---|
| Requirements approval | The business needs, rules, measures and scope of Epics 3 to 8 are accepted and this document moves to Approved | This document, its traceability table and the open questions in section 12 |
| Requirement ownership | Each requirement has one business owner role and one capability owner service | Section 8 owners and section 7.3 |
| Change control | A change to a requirement is a new version of this document, with the change in the change log and the IDs kept stable | Change log, section 1.1 |
| Open questions | Each question is answered by the role named in section 12 before the requirement it blocks is accepted | The gap and assumption registers |
| Traceability | Every requirement, rule and measure resolves to a source document and a section | Section 14 |

| Approver | Name | Decision | Date |
|---|---|---|---|
| Product Owner | | | |
| Business owner, settle and deed in lieu (E3) | | | |
| Business owner, route decision (E4) | | | |
| Head of Litigation (E5) | | | |
| Head of Asset Liquidity and Head of NPA (E6) | | | |
| Business owner, deviations and partners (E7) | | | |
| Business owner, administration and reporting (E8) | | | |
| Solution architect | | | |
| Security administrator | | | |
| Compliance and PDPA officer | | | |

## 14. Traceability to sources

### 14.1 Requirement to source

| Requirement | Source document | Section | Program ID and features |
|---|---|---|---|
| BR-001 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.9; features sheet E3 S2 | REQ-S2-001, REQ-CHO-006; FEAT-TRT-01 |
| BR-002 | Business Requirements Program v5; Business Rules v4 | 5.9; Settlement route set | REQ-S2-004; FEAT-TRT-02, FEAT-TRT-03; R-SET-04, R-SET-05 |
| BR-003 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.9; features sheet E3 S2 | REQ-S2-002; FEAT-TRT-04 to FEAT-TRT-06 |
| BR-004 | Business Rules v4; Business Requirements Program v5 | Restructure route set; 5.9 | REQ-S2-002, REQ-S2-003; R-RES-09, R-RES-17, R-RES-18 |
| BR-005 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.9; features sheet E3 S2 | REQ-S2-003, REQ-S2-008, REQ-CHO-008; FEAT-TRT-08, FEAT-TRT-10 |
| BR-006 | Business Rules v4; Business Requirements Program v5 | Restructure route set R-RES-27 to R-RES-32; 5.9 | REQ-S2-009; FEAT-TRT-11 |
| BR-007 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.9; features sheet E3 S2 | REQ-S2-005, REQ-S2-007; FEAT-TRT-12 to FEAT-TRT-14 |
| BR-008 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.9; features sheet E3 S2 | REQ-S2-006, REQ-S2-010; FEAT-TRT-16, FEAT-TRT-18 |
| BR-009 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.9; features sheet E3 S2 | REQ-S2-008; FEAT-TRT-15, FEAT-TRT-17 |
| BR-010 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.12; features sheet E3 S5 | REQ-S5-001; FEAT-AST-01 to FEAT-AST-04 |
| BR-011 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.12; features sheet E3 S5 | REQ-S5-003; FEAT-AST-05, FEAT-AST-09 |
| BR-012 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.12; features sheet E3 S5 | REQ-S5-002; FEAT-AST-06 |
| BR-013 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.12; features sheet E3 S5 | REQ-S5-001; FEAT-AST-07 |
| BR-014 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.12; features sheet E3 S5; integrations INT-27 | REQ-S5-004, REQ-S5-005; FEAT-AST-10 to FEAT-AST-12 |
| BR-015 | Epics 3 to 8 Specification v3; Recovery Workbench Temporal and Drools Design v1 | features sheet E3 P10; slides 15 to 17 | FEAT-AGT-12, FEAT-AGT-13 |
| BR-016 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.8; features sheet E4 S1 | REQ-S1-001; FEAT-VAL-01 |
| BR-017 | Epics 3 to 8 Specification v3; Business Requirements Program v5 | features sheet E4 S1; 5.8 | REQ-S1-002; FEAT-VAL-02 to FEAT-VAL-04 |
| BR-018 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.8; features sheet E4 S1 | REQ-S1-003, REQ-S1-004; FEAT-VAL-05, FEAT-VAL-06 |
| BR-019 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.8; features sheet E4 S1 | REQ-S1-005; FEAT-VAL-07 |
| BR-020 | Business Requirements Program v5; Business Rules v4 | 5.8; Universal route set | REQ-S1-006, REQ-S1-008, REQ-APD-001, REQ-APD-004; FEAT-VAL-08 to FEAT-VAL-11 |
| BR-021 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.8; features sheet E4 S1 | REQ-S1-007; FEAT-VAL-12 |
| BR-022 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.10; features sheet E4 S3; integrations INT-29 | REQ-S3-001, REQ-S3-002; FEAT-GUA-01 to FEAT-GUA-03 |
| BR-023 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.10; features sheet E4 S3 | REQ-S3-003, REQ-S3-006; FEAT-GUA-04, FEAT-GUA-07 |
| BR-024 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.10; features sheet E4 S3 | REQ-S3-004, REQ-S3-005; FEAT-GUA-05, FEAT-GUA-06 |
| BR-025 | Epics 3 to 8 Specification v3 | features sheet E4 S3 | FEAT-GUA-08 |
| BR-026 | Epics 3 to 8 Specification v3 | features sheet E4 S5 | FEAT-AST-08 |
| BR-027 | Business Requirements Program v5; Business Rules v4 | 5.12; Asset disposal route set | REQ-S5-006; FEAT-AST-13 to FEAT-AST-15, FEAT-AST-17; R-DIS-01 to R-DIS-72 |
| BR-028 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.12; features sheet E4 S5 | REQ-S5-007; FEAT-AST-16, FEAT-AST-18 |
| BR-029 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.12; features sheet E4 S5; integrations INT-28 | REQ-S5-008; FEAT-AST-19, FEAT-AST-20 |
| BR-030 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.12; features sheet E4 S5 | REQ-S5-009, REQ-S5-010; FEAT-AST-21 to FEAT-AST-25 |
| BR-031 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.6; features sheet E4 P6 | REQ-OCC-011; FEAT-COM-01 to FEAT-COM-04 |
| BR-032 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.5, 5.6; features sheet E4 P6 | REQ-OCC-006, REQ-DCM-019; FEAT-COM-05 to FEAT-COM-08 |
| BR-033 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.14; features sheet E4 P8 | REQ-CHO-009; FEAT-PAY-03 to FEAT-PAY-07, FEAT-PAY-09 to FEAT-PAY-11 |
| BR-034 | Business Requirements Program v5; Business Rules v4 | 5.11; Litigation route set | REQ-S4-001, REQ-APD-006; FEAT-LIT-01 to FEAT-LIT-03; R-LIT-01 to R-LIT-79 |
| BR-035 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.11; features sheet E5 S4 | REQ-S4-002; FEAT-LIT-04 to FEAT-LIT-06 |
| BR-036 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.11; features sheet E5 S4 and E8 P4 | REQ-S4-003; FEAT-LIT-07, FEAT-ADM-09 |
| BR-037 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.11; features sheet E5 S4 | REQ-S4-004; FEAT-LIT-08, FEAT-LIT-09 |
| BR-038 | Epics 3 to 8 Specification v3 | features sheet E5 S4; integrations INT-33 | FEAT-LIT-10 |
| BR-039 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.11; features sheet E5 S4 | REQ-S4-005; FEAT-LIT-11, FEAT-LIT-12 |
| BR-040 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.11; features sheet E5 S4 | REQ-S4-006; FEAT-LIT-13 to FEAT-LIT-15 |
| BR-041 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.11; features sheet E5 S4 | REQ-S4-007, REQ-S4-008; FEAT-LIT-16, FEAT-LIT-20 |
| BR-042 | Epics 3 to 8 Specification v3 | features sheet E5 S4; integrations INT-33 | FEAT-LIT-17 to FEAT-LIT-19, FEAT-LIT-21 |
| BR-043 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.11; features sheet E5 S4 | REQ-S4-010; FEAT-LIT-22 |
| BR-044 | Business Requirements Program v5; Business Rules v4 | 5.13; Debt sale route set | REQ-S6-001 to REQ-S6-003; FEAT-DBS-01 to FEAT-DBS-04; R-DS-01 to R-DS-41 |
| BR-045 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.13; features sheet E6 S6 | REQ-S6-004, REQ-S6-005; FEAT-DBS-06, FEAT-DBS-07 |
| BR-046 | Epics 3 to 8 Specification v3 | features sheet E6 S6 | FEAT-DBS-08 |
| BR-047 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.13; features sheet E6 S6 | REQ-S6-006; FEAT-DBS-05, FEAT-DBS-09, FEAT-DBS-10 |
| BR-048 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.13; features sheet E6 S6 | REQ-S6-008; FEAT-DBS-11, FEAT-DBS-12, FEAT-DBS-15 |
| BR-049 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.13; features sheet E6 S6 | REQ-S6-007, REQ-S6-009; FEAT-DBS-13, FEAT-DBS-14 |
| BR-050 | Epics 3 to 8 Specification v3 | features sheet E6 S6 | FEAT-DBS-16 |
| BR-051 | Business Requirements Program v5; Business Rules v4 | 5.14; Write-off route set | REQ-S7-001; FEAT-WOF-01, FEAT-WOF-02; R-WO-01 to R-WO-51 |
| BR-052 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.14; features sheet E6 S7 | REQ-S7-002; FEAT-WOF-03 to FEAT-WOF-05 |
| BR-053 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.14; features sheet E6 S7 | REQ-S7-003; FEAT-WOF-06 to FEAT-WOF-08 |
| BR-054 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.14; features sheet E6 S7 and E6 P8 | REQ-S7-005; FEAT-WOF-09, FEAT-WOF-10, FEAT-PAY-08 |
| BR-055 | Epics 3 to 8 Specification v3 | features sheet E6 S7 | FEAT-WOF-11 |
| BR-056 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.14; features sheet E6 S7 | REQ-S7-004; FEAT-WOF-12 |
| BR-057 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.14; features sheet E6 S7 | REQ-S7-008; FEAT-WOF-13 |
| BR-058 | Epics 3 to 8 Specification v3 | features sheet E6 S7 | FEAT-WOF-14 |
| BR-059 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.14, 5.16; features sheet E6 S7 and S9 | REQ-S7-006, REQ-S7-007; FEAT-WOF-15, FEAT-WOF-16, FEAT-PRM-06 |
| BR-060 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.16; features sheet E6 S9 | REQ-S9-001 to REQ-S9-004, REQ-S9-008; FEAT-PRM-01 to FEAT-PRM-05, FEAT-PRM-07 |
| BR-061 | Epics 3 to 8 Specification v3 | features sheet E6 P9 | FEAT-RPT-06 |
| BR-062 | Business Requirements Program v5; Business Rules v4 | 5.15; Deviations route set | REQ-S8-001, REQ-S8-003; FEAT-DVF-01; R-DEV-01 to R-DEV-22 |
| BR-063 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.15; features sheet E7 S8 | REQ-S8-002; FEAT-DVF-02 |
| BR-064 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.15; features sheet E7 S8 | REQ-DVH-008; FEAT-DVF-03 |
| BR-065 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.15; features sheet E7 S8 and E8 P4; integrations INT-31 | REQ-DVH-010; FEAT-DVF-04, FEAT-ADM-13 |
| BR-066 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.15; features sheet E7 S8 | REQ-DVH-009; FEAT-DVF-05 |
| BR-067 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.15; features sheet E7 S8; integrations INT-30 | REQ-S8-004; FEAT-DVF-06 |
| BR-068 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.15; features sheet E7 S8 | REQ-S8-005; FEAT-DVF-07 |
| BR-069 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.15; features sheet E7 S8 | REQ-S8-006, REQ-DVH-007; FEAT-DVF-08 to FEAT-DVF-10 |
| BR-070 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.16; features sheet E7 S9 | REQ-S9-005 to REQ-S9-007; FEAT-PRM-08 to FEAT-PRM-13 |
| BR-071 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.16; features sheet E7 S9 | REQ-S9-009; FEAT-PRM-14, FEAT-PRM-15 |
| BR-072 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.4; features sheet E8 P4 | REQ-ACA-013; FEAT-ADM-01 |
| BR-073 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.3; features sheet E8 P4 | REQ-CWC-013; FEAT-ADM-02, FEAT-ADM-06 |
| BR-074 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.7; features sheet E8 P4 | REQ-APD-010; FEAT-ADM-03, FEAT-ADM-04 |
| BR-075 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.6; features sheet E8 P4 | REQ-OCC-002; FEAT-ADM-05 |
| BR-076 | Epics 3 to 8 Specification v3 | features sheet E8 P4 | FEAT-ADM-07 |
| BR-077 | Epics 3 to 8 Specification v3; Non Functional Specification | features sheet E8 P4; section 6.6 | FEAT-ADM-08; NFR-037 |
| BR-078 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.7; features sheet E8 P4 | REQ-DRI-003; FEAT-ADM-09, FEAT-ADM-10 |
| BR-079 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 6.7 and 5.15; features sheet E8 P4 | NFR-043, REQ-S8-007; FEAT-ADM-11 |
| BR-080 | Epics 3 to 8 Specification v3 | features sheet E8 P4 | FEAT-ADM-12 |
| BR-081 | Business Requirements Program v5; Epics 3 to 8 Specification v3 | 5.4; features sheet E8 P4 | REQ-ACA-003, REQ-ACA-010; FEAT-ADM-14 |
| BR-082 | Epics 3 to 8 Specification v3 | features sheet E8 P9 | FEAT-RPT-07 |
| BR-083 | Epics 3 to 8 Specification v3 | features sheet E8 P9 | FEAT-RPT-10 |
| BR-084 | Epics 3 to 8 Specification v3; Recovery Workbench Temporal and Drools Design v1 | features sheet E8 P10; slides 15 to 17 | FEAT-AGT-14 to FEAT-AGT-16 |

### 14.2 Rule, measure and assumption to source

| Item | Source document | Section |
|---|---|---|
| RULE-001 to RULE-002 | Business Requirements Program v5; Decision Log v10 | sections 5.3, 5.7, 7; D-RCV-036 T4 |
| RULE-003 to RULE-009 | Business Rules v4 | Settlement, Restructure, Deed in lieu and Asset disposal route sets; FEAT-AST-18, FEAT-LIT-19 |
| RULE-010 to RULE-011 | Business Requirements Program v5; Business Rules v4 | 5.7; Universal route set |
| RULE-012 to RULE-014 | Business Requirements Program v5; Business Rules v4 | 5.15; Deviations route set |
| RULE-015 to RULE-018 | Business Requirements Program v5; Business Rules v4 | 5.13; Debt sale route set |
| RULE-019 to RULE-022 | Business Requirements Program v5; Business Rules v4 | 5.14; Write-off route set |
| RULE-023 to RULE-024 | Business Requirements Program v5 | 5.16 |
| RULE-025 to RULE-026 | Business Requirements Program v5 | 5.11 |
| RULE-027 to RULE-029 | Business Requirements Program v5; Non Functional Specification v3 | 5.4, 5.6, 6.6, 6.9 |
| RULE-030 to RULE-031 | Decision Log v10; Recovery Workbench Temporal and Drools Design v1; Architecture v5 Text Extract v1 | D-RCV-035, D-RCV-036 T5 and T7; slides 2 to 4; slide 41 |
| RULE-032 | Microservice Story Template and Rules v1 | R1 U7; Decision Log v10 DL48 |
| KPI-001 to KPI-008 | Business Requirements Program v5 | section 2 |
| KPI-009 to KPI-013 | Non Functional Specification v3; Business Requirements Program v5 | 6.6, 6.3; 5.7 |
| KPI-014 | Epics 3 to 8 Specification v3 | features sheet E6 P9 |
| ASM-001 to ASM-007 | Microservice Story Template and Rules v1; Business Requirements Program v5 | R1, R8.1, R9; section 8 |
| ASM-008 to ASM-028 | Business Requirements Program v5; Decision Log v10; Epics 3 to 8 Specification v3 | sections 5.8 to 5.16 and 9; DL18, DL22, DL23, DL26, DL43; features sheet |

### 14.3 Epic to service epic to business epic

| Business epic | Service epic and owner | Wave | Features served |
|---|---|---|---|
| EP03 E3 | RWB-SVC-S2 rwb-treatment; RWB-SVC-S5 rwb-asset; RWB-SVC-P8 rwb-payment; RWB-SVC-P10 rwb-agent | 2 | 31 features |
| EP04 E4 | RWB-SVC-S1 rwb-valuation; RWB-SVC-S3 rwb-guarantee; RWB-SVC-S5 rwb-asset; RWB-SVC-P6 rwb-comms; RWB-SVC-P8 rwb-payment; RWB-SVC-S9 rwb-partner | 3 | 50 features |
| EP05 E5 | RWB-SVC-S4 rwb-litigation; RWB-SVC-S6 rwb-debtsale; RWB-SVC-S9 rwb-partner | 3 | 26 features |
| EP06 E6 | RWB-SVC-S6 rwb-debtsale; RWB-SVC-S7 rwb-writeoff; RWB-SVC-S9 rwb-partner; RWB-SVC-P8 rwb-payment; RWB-SVC-P9 rwb-reporting | 4 | 37 features |
| EP07 E7 | RWB-SVC-S8 rwb-deviation; RWB-SVC-S9 rwb-partner | 4 | 18 features |
| EP08 E8 | RWB-SVC-P4 rwb-access; RWB-SVC-P9 rwb-reporting; RWB-SVC-P10 rwb-agent | 4 | 19 features |

### 14.4 Coverage check

| Check | Count |
|---|---|
| Features in the specification | 181 |
| Stories in the user story master | 181 (count only; the backlog holds the keys) |
| Business requirements in this document | 84 |
| Business rules and policies | 32 |
| Success measures | 14 |
| Assumptions | 34 |
| Constraints | 12 |
| Dependencies | 10 |
| Risks | 10 |
| Open questions and gap rows | 27 |
| Requirement rows traced to a source section | 84 of 84 |
| Stories covered by a requirement or a rule | 181 of 181 |

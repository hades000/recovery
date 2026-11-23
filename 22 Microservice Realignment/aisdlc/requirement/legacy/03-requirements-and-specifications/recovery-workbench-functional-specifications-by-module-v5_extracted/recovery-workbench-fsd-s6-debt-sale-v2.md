<!-- source: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v5.zip!Recovery Workbench FSD S6 Debt sale v2.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v5.zip!Recovery Workbench FSD S6 Debt sale v2.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench S6 Debt sale

Functional specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD S6 Debt sale |
| Document ID | S6-RWB-FSD-v2 |
| Version | 2 |
| Status | In review |
| Classification | Confidential |
| Date | 28 October 2026 |
| FSD owner | Business analyst, S6 |
| Business owner | Business lead |

| Module code | Module name | First in |
|---|---|---|
| S6 | Debt sale | E5 data; E6 screens |

**Feature scope.** Lot building, data room, buyer terms, award, transfer.

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification S6 Debt sale | TSD | Pair |
| Recovery Workbench User Stories Epic 1 and Epic 2 | Backlog | Traceability |

## Existing capability check

| Capability | Verdict | Owning document | Note |
|---|---|---|---|
| Sign-in, access check, audit and PII logging | REUSE | ACE common module | No build in this module |
| Case record and shared entities | REUSE | ACE common module; Case and Workflow Model | Read through the P3 interfaces |
| Notification path | REUSE | ACE notification path | Recovery templates only |
| Workflow and state machine | REUSE | Workflow Engine Design | Stages and sentries from P3 |
| Decision record and audit trail | REUSE | Audit and Logging Design | Writes through P7 |
| Attachments and evidence | REUSE | Document Management Design | Through P5 |
| Role and permission matrix | REUSE | Users Roles and Permissions | Capability areas from P4 |
| Restructure calculator | REUSE | ACE common module | Not used |

## A1. Context and scope

### A1.1 Scope of work and deliverables

**In scope.** Lot building, data room, buyer terms, award, transfer.

**Out of scope.** Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces.

**Dependencies.** FEAT-APD-01; FEAT-DBS-01; FEAT-DBS-03; FEAT-DBS-04; FEAT-DBS-06; FEAT-DBS-08; FEAT-DBS-09; FEAT-DBS-11

**Constraints.** Built in the ACE service as part of the recovery module; data through COLLINS and file loads; every value a business person may change is a versioned data row (principle 1).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section |
|---|---|---|---|---|---|---|
| S6 | FEAT-DBS-01 | Select eligible accounts for sale by rule | System | Applies the eligibility rules, including the 54 percent cap, to pick the sale population. | E5 | A2.1 |
| S6 | FEAT-DBS-02 | Build the lots and estimate the price | System | Groups the accounts into lots and estimates the price from the COLLINS lot economics. | E5 | A2.2 |
| S6 | FEAT-DBS-03 | Prepare the masked data tape | System | Builds the data tape with personal data masked under PDPA, ready for the data room. | E5 | A2.3 |
| S6 | FEAT-DBS-04 | Open the buyer data room | System | Publishes the lot and the masked tape to the data room for qualified buyers. | E5 | A2.4 |
| S6 | FEAT-DBS-05 | Approve lots, reserve and tiered terms | User | Takes the lot, the reserve price and the terms to the committee for approval. | E6 | A2.5 |
| S6 | FEAT-DBS-06 | Qualify a buyer against KYC and licensing | System | Runs the KYC, licensing and eligibility checks before a buyer can bid. | E6 | A2.6 |
| S6 | FEAT-DBS-07 | Bar a buyer that fails qualification | System | Removes a buyer from the panel on a license breach and releases the lot to the next bidder. | E6 | A2.7 |
| S6 | FEAT-DBS-08 | Take buyer bids | User | Lets a qualified buyer bid on a lot through the portal, inside the bid window. | E6 | A2.8 |
| S6 | FEAT-DBS-09 | Award the lot and test the price | User | Compares the best bid to the reserve and the model, and awards with the approval the limit requires. | E6 | A2.9 |
| S6 | FEAT-DBS-10 | Generate the sale agreement and notices | System | Produces the agreement and the customer notices the sale requires. | E6 | A2.10 |
| S6 | FEAT-DBS-11 | Transfer the data to the buyer | System | Sends the awarded account data to the buyer and records the transfer. | E6 | A2.11 |
| S6 | FEAT-DBS-12 | Derecognize and post to the general ledger | System | Removes the sold accounts from the book and posts the result to ALS and the ledger. | E6 | A2.12 |
| S6 | FEAT-DBS-13 | Handle a buyer put-back claim | User | Reviews a claim that an account should not have been sold, and settles or rejects it. | E6 | A2.13 |
| S6 | FEAT-DBS-14 | Close a case awarded in a sold lot | System | Stops every open action on a case whose account is sold in a lot, and closes it. | E6 | A2.14 |
| S6 | FEAT-DBS-15 | Confirm buyer remittance | System | Matches the buyer's payment to the award and closes the money side of the lot. | E6 | A2.15 |
| S6 | FEAT-DBS-16 | Apply the debt sale cap | System | Holds the sale population inside the policy cap and reports the headroom. | E6 | A2.16 |

### A1.3 Background

Debt sales run on spreadsheets with no baseline turnaround.

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date, or show their date as stale.

## A2. Functional decomposition

### A2.1 Select eligible accounts for sale by rule

#### A2.1.1 Intent

**Business objective.** Applies the eligibility rules, including the 54 percent cap, to pick the sale population.

**Problem.** Debt sales run on spreadsheets with no baseline turnaround.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Debt sale turnaround | 45 days | Decision log and Workbench records | Monthly |

#### A2.1.2 Description

**Functional overview.** Applies the eligibility rules, including the 54 percent cap, to pick the sale population.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Select eligible accounts for sale by rule | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, COLLINS

**Prerequisites.** FEAT-DRI-07

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S6-001-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-DS-01 | Select the accounts for sale from the case list, when eligibility rule passes and deviation_open = none | Moves to LOT_BUILT |
| BR-S6-001 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Debt sale officer | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S6-001-01 | Select eligible accounts for sale by rule | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S6-001-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S6-001-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.1.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.2 Build the lots and estimate the price

#### A2.2.1 Intent

**Business objective.** Groups the accounts into lots and estimates the price from the COLLINS lot economics.

**Problem.** Debt sales run on spreadsheets with no baseline turnaround.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Debt sale turnaround | 45 days | Decision log and Workbench records | Monthly |

#### A2.2.2 Description

**Functional overview.** Groups the accounts into lots and estimates the price from the COLLINS lot economics.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Build the lots and estimate the price | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** COLLINS, Model gateway

**Prerequisites.** FEAT-DBS-01

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S6-002-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-S6-002 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Debt sale officer | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S6-002-01 | Build the lots and estimate the price | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S6-002-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S6-002-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.2.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.3 Prepare the masked data tape

#### A2.3.1 Intent

**Business objective.** Builds the data tape with personal data masked under PDPA, ready for the data room.

**Problem.** Debt sales run on spreadsheets with no baseline turnaround.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Debt sale turnaround | 45 days | Decision log and Workbench records | Monthly |

#### A2.3.2 Description

**Functional overview.** Builds the data tape with personal data masked under PDPA, ready for the data room.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Prepare the masked data tape | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ACE database, PII service

**Prerequisites.** FEAT-RDF-15

#### A2.3.3 Business rules and structure

##### A2.3.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S6-003-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-DS-10 | Build the masked data tape under the PII masking rules, when the event occurs | Moves to TAPE_PREPARED |
| BR-S6-003 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.3.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Debt sale officer | Also uses |

#### A2.3.4 Acceptance criteria

##### A2.3.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S6-003-01 | Prepare the masked data tape | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.3.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.3.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S6-003-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S6-003-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.3.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.4 Open the buyer data room

#### A2.4.1 Intent

**Business objective.** Publishes the lot and the masked tape to the data room for qualified buyers.

**Problem.** Debt sales run on spreadsheets with no baseline turnaround.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Debt sale turnaround | 45 days | Decision log and Workbench records | Monthly |

#### A2.4.2 Description

**Functional overview.** Publishes the lot and the masked tape to the data room for qualified buyers.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Open the buyer data room | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Partner portal

**Prerequisites.** FEAT-DBS-03

#### A2.4.3 Business rules and structure

##### A2.4.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S6-004-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-S6-004 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.4.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Debt sale officer | Also uses |

#### A2.4.4 Acceptance criteria

##### A2.4.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S6-004-01 | Open the buyer data room | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.4.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.4.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S6-004-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S6-004-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.4.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.5 Approve lots, reserve and tiered terms

#### A2.5.1 Intent

**Business objective.** Takes the lot, the reserve price and the terms to the committee for approval.

**Problem.** Debt sales run on spreadsheets with no baseline turnaround.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Debt sale turnaround | 45 days | Decision log and Workbench records | Monthly |

#### A2.5.2 Description

**Functional overview.** Takes the lot, the reserve price and the terms to the committee for approval.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Head of Asset Liquidity | Opens the screen and approve lots, reserve and tiered terms | Checks the role, the capability area and the scope |
| 2 | Head of Asset Liquidity | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-APD-01

#### A2.5.3 Business rules and structure

##### A2.5.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S6-005-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-DS-06 | Approve the lot, the reserve and the tiered terms, and log the decision, when reserve and terms approved inside the delegation | Moves to LOT_APPROVED |
| R-DS-04 | Propose the lots, the tiered buyer terms and the reserve price, when lot agent estimate returned with COLLINS | Moves to LOT_WITH_COMMITTEE |
| R-DS-07 | Reprice the lot and return it to the committee, when committee raises the reserve | Moves to LOT_WITH_COMMITTEE |
| BR-S6-005 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.5.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| debt_sale_lot.lot_no | Lot number, for example 1/2024 | varchar(15) | Yes | None | No |
| debt_sale_lot.cut_off_date | Balance cut-off date | date | Yes | None | No |
| debt_sale_lot.segment | Segment of the lot | varchar(20) | Yes | LOV-SEGMENT | No |
| debt_sale_lot.reserve_price | Reserve price, baht | numeric(18,2) | No | None | No |
| debt_sale_lot.buyer_partner_id | Winning buyer | uuid | No | None | No |
| debt_sale_lot.buyer_class | AMC or non-AMC | varchar(10) | No | LOV-BUYER-CLASS | No |
| debt_sale_lot.signing_date | Date the sale was signed | date | No | None | No |
| debt_sale_lot.approval_authority | Authority that approved the sale | varchar(60) | No | None | No |

##### A2.5.3.3 Roles and permissions

| Role | Use |
|---|---|
| Head of Asset Liquidity | Primary |
| Debt sale officer, Credit approval committee member | Also uses |

#### A2.5.4 Acceptance criteria

##### A2.5.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S6-005-01 | Approve lots, reserve and tiered terms | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.5.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.5.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S6-005-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S6-005-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.5.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.6 Qualify a buyer against KYC and licensing

#### A2.6.1 Intent

**Business objective.** Runs the KYC, licensing and eligibility checks before a buyer can bid.

**Problem.** Debt sales run on spreadsheets with no baseline turnaround.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Debt sale turnaround | 45 days | Decision log and Workbench records | Monthly |

#### A2.6.2 Description

**Functional overview.** Runs the KYC, licensing and eligibility checks before a buyer can bid.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Qualify a buyer against KYC and licensing | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Partner portal, Workbench

**Prerequisites.** FEAT-DBS-04

#### A2.6.3 Business rules and structure

##### A2.6.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S6-006-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-DS-14 | Run the KYC, licensing and eligibility check on the bidder, when nda_signed_at present | Moves to BUYER_PENDING_KYC |
| R-DS-18 | Record the bid against the lot and the buyer, when the event occurs | Moves to BIDS_RECEIVED |
| R-DS-26 | Cancel the award and score the cancellation against the buyer, when cancellation recorded with a reason | Moves to AWARD_CANCELED_DS |
| BR-S6-006 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.6.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Debt sale officer | Also uses |

#### A2.6.4 Acceptance criteria

##### A2.6.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S6-006-01 | Qualify a buyer against KYC and licensing | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.6.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.6.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S6-006-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S6-006-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.6.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.7 Bar a buyer that fails qualification

#### A2.7.1 Intent

**Business objective.** Removes a buyer from the panel on a license breach and releases the lot to the next bidder.

**Problem.** Debt sales run on spreadsheets with no baseline turnaround.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Debt sale turnaround | 45 days | Decision log and Workbench records | Monthly |

#### A2.7.2 Description

**Functional overview.** Removes a buyer from the panel on a license breach and releases the lot to the next bidder.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Bar a buyer that fails qualification | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Partner portal

**Prerequisites.** FEAT-DBS-06

#### A2.7.3 Business rules and structure

##### A2.7.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S6-007-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-DS-41 | Remove the buyer from the panel and release the lot to the next bidder, when no evidence supplied inside the window, or the failure is a license breach | Moves to BACK_TO_CASE_LIST |
| R-DS-14 | Run the KYC, licensing and eligibility check on the bidder, when nda_signed_at present | Moves to BUYER_PENDING_KYC |
| R-DS-40 | Re-open the qualification check, when the buyer supplies the missing KYC or license evidence inside the window | Moves to BUYER_PENDING_KYC |
| BR-S6-007 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.7.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Head of Asset Liquidity | Also uses |

#### A2.7.4 Acceptance criteria

##### A2.7.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S6-007-01 | Bar a buyer that fails qualification | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.7.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.7.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S6-007-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S6-007-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.7.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.8 Take buyer bids

#### A2.8.1 Intent

**Business objective.** Lets a qualified buyer bid on a lot through the portal, inside the bid window.

**Problem.** Debt sales run on spreadsheets with no baseline turnaround.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Debt sale turnaround | 45 days | Decision log and Workbench records | Monthly |

#### A2.8.2 Description

**Functional overview.** Lets a qualified buyer bid on a lot through the portal, inside the bid window.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Debt buyer and AMC | Opens the screen and take buyer bids | Checks the role, the capability area and the scope |
| 2 | Debt buyer and AMC | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Partner portal

**Prerequisites.** FEAT-DBS-06

#### A2.8.3 Business rules and structure

##### A2.8.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S6-008-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-DS-34 | Close the lot and record realized recovery by lot and by buyer, when no put-back claim inside the claim window | Moves to LOT_CLOSED |
| BR-S6-008 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.8.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| debt_sale_lot.lot_no | Lot number, for example 1/2024 | varchar(15) | Yes | None | No |
| debt_sale_lot.cut_off_date | Balance cut-off date | date | Yes | None | No |
| debt_sale_lot.segment | Segment of the lot | varchar(20) | Yes | LOV-SEGMENT | No |
| debt_sale_lot.reserve_price | Reserve price, baht | numeric(18,2) | No | None | No |
| debt_sale_lot.buyer_partner_id | Winning buyer | uuid | No | None | No |
| debt_sale_lot.buyer_class | AMC or non-AMC | varchar(10) | No | LOV-BUYER-CLASS | No |
| debt_sale_lot.signing_date | Date the sale was signed | date | No | None | No |
| debt_sale_lot.approval_authority | Authority that approved the sale | varchar(60) | No | None | No |

##### A2.8.3.3 Roles and permissions

| Role | Use |
|---|---|
| Debt buyer and AMC | Primary |
| Debt sale officer | Also uses |

#### A2.8.4 Acceptance criteria

##### A2.8.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S6-008-01 | Take buyer bids | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.8.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.8.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S6-008-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S6-008-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.8.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.9 Award the lot and test the price

#### A2.9.1 Intent

**Business objective.** Compares the best bid to the reserve and the model, and awards with the approval the limit requires.

**Problem.** Debt sales run on spreadsheets with no baseline turnaround.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Debt sale turnaround | 45 days | Decision log and Workbench records | Monthly |

#### A2.9.2 Description

**Functional overview.** Compares the best bid to the reserve and the model, and awards with the approval the limit requires.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Debt sale officer | Opens the screen and award the lot and test the price | Checks the role, the capability area and the scope |
| 2 | Debt sale officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, Partner portal

**Prerequisites.** FEAT-DBS-08

#### A2.9.3 Business rules and structure

##### A2.9.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S6-009-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-DS-19 | Test the price against the reserve and the 54 percent cap, and route the award, when best_bid at or above reserve_price | Moves to AWARD_PENDING |
| R-DS-04 | Propose the lots, the tiered buyer terms and the reserve price, when lot agent estimate returned with COLLINS | Moves to LOT_WITH_COMMITTEE |
| BR-S6-009 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.9.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| debt_sale_lot.lot_no | Lot number, for example 1/2024 | varchar(15) | Yes | None | No |
| debt_sale_lot.cut_off_date | Balance cut-off date | date | Yes | None | No |
| debt_sale_lot.segment | Segment of the lot | varchar(20) | Yes | LOV-SEGMENT | No |
| debt_sale_lot.reserve_price | Reserve price, baht | numeric(18,2) | No | None | No |
| debt_sale_lot.buyer_partner_id | Winning buyer | uuid | No | None | No |
| debt_sale_lot.buyer_class | AMC or non-AMC | varchar(10) | No | LOV-BUYER-CLASS | No |
| debt_sale_lot.signing_date | Date the sale was signed | date | No | None | No |
| debt_sale_lot.approval_authority | Authority that approved the sale | varchar(60) | No | None | No |

##### A2.9.3.3 Roles and permissions

| Role | Use |
|---|---|
| Debt sale officer | Primary |
| Head of Asset Liquidity | Also uses |

#### A2.9.4 Acceptance criteria

##### A2.9.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S6-009-01 | Award the lot and test the price | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.9.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.9.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S6-009-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S6-009-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.9.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.10 Generate the sale agreement and notices

#### A2.10.1 Intent

**Business objective.** Produces the agreement and the customer notices the sale requires.

**Problem.** Debt sales run on spreadsheets with no baseline turnaround.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Debt sale turnaround | 45 days | Decision log and Workbench records | Monthly |

#### A2.10.2 Description

**Functional overview.** Produces the agreement and the customer notices the sale requires.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Generate the sale agreement and notices | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, WIN

**Prerequisites.** FEAT-OCC-07

#### A2.10.3 Business rules and structure

##### A2.10.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S6-010-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-DS-23 | Award the lot and generate the sale agreement and the customer notices, when price tested against the reserve and the 54 percent cap, and recorded | Moves to LOT_AWARDED |
| BR-S6-010 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.10.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Debt sale officer | Also uses |

#### A2.10.4 Acceptance criteria

##### A2.10.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S6-010-01 | Generate the sale agreement and notices | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.10.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.10.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S6-010-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S6-010-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.10.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.11 Transfer the data to the buyer

#### A2.11.1 Intent

**Business objective.** Sends the awarded account data to the buyer and records the transfer.

**Problem.** Debt sales run on spreadsheets with no baseline turnaround.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Debt sale turnaround | 45 days | Decision log and Workbench records | Monthly |

#### A2.11.2 Description

**Functional overview.** Sends the awarded account data to the buyer and records the transfer.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Transfer the data to the buyer | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Partner portal

**Prerequisites.** FEAT-DBS-09

#### A2.11.3 Business rules and structure

##### A2.11.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S6-011-1 | Account with an open deviation selected for a lot (R-DS-02) | MSG-S6-001 {account} has an open deviation and cannot be sold. |
| R-DS-29 | Transfer the account data to the buyer, when the event occurs | Moves to DATA_TRANSFERRED |
| R-DS-25 | Confirm settlement and release the data transfer, when payment received in full | Moves to SETTLED |
| BR-S6-011 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.11.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Debt sale officer | Also uses |

#### A2.11.4 Acceptance criteria

##### A2.11.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S6-011-01 | Transfer the data to the buyer | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.11.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.11.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S6-011-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S6-011-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.11.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.12 Derecognize and post to the general ledger

#### A2.12.1 Intent

**Business objective.** Removes the sold accounts from the book and posts the result to ALS and the ledger.

**Problem.** Debt sales run on spreadsheets with no baseline turnaround.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Debt sale turnaround | 45 days | Decision log and Workbench records | Monthly |

#### A2.12.2 Description

**Functional overview.** Removes the sold accounts from the book and posts the result to ALS and the ledger.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Derecognize and post to the general ledger | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL

**Prerequisites.** FEAT-DBS-11

#### A2.12.3 Business rules and structure

##### A2.12.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S6-012-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-DS-31 | Post to the general ledger and send the provision input to Finance, when the event occurs | Moves to GL_POSTED |
| R-DS-33 | Re-post to ALS and the general ledger, when the rejection cause is cleared | Moves to GL_POSTED |
| BR-S6-012 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.12.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Credit Administration officer | Also uses |

#### A2.12.4 Acceptance criteria

##### A2.12.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S6-012-01 | Derecognize and post to the general ledger | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.12.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.12.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S6-012-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S6-012-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.12.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.13 Handle a buyer put-back claim

#### A2.13.1 Intent

**Business objective.** Reviews a claim that an account should not have been sold, and settles or rejects it.

**Problem.** Debt sales run on spreadsheets with no baseline turnaround.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Debt sale turnaround | 45 days | Decision log and Workbench records | Monthly |

#### A2.13.2 Description

**Functional overview.** Reviews a claim that an account should not have been sold, and settles or rejects it.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Debt sale officer | Opens the screen and handle a buyer put-back claim | Checks the role, the capability area and the scope |
| 2 | Debt sale officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Partner portal, ALS and GL

**Prerequisites.** FEAT-DBS-11

#### A2.13.3 Business rules and structure

##### A2.13.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S6-013-1 | Account with an open deviation selected for a lot (R-DS-02) | MSG-S6-001 {account} has an open deviation and cannot be sold. |
| R-DS-29 | Transfer the account data to the buyer, when the event occurs | Moves to DATA_TRANSFERRED |
| R-DS-34 | Close the lot and record realized recovery by lot and by buyer, when no put-back claim inside the claim window | Moves to LOT_CLOSED |
| BR-S6-013 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.13.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| debt_sale_lot.lot_no | Lot number, for example 1/2024 | varchar(15) | Yes | None | No |
| debt_sale_lot.cut_off_date | Balance cut-off date | date | Yes | None | No |
| debt_sale_lot.segment | Segment of the lot | varchar(20) | Yes | LOV-SEGMENT | No |
| debt_sale_lot.reserve_price | Reserve price, baht | numeric(18,2) | No | None | No |
| debt_sale_lot.buyer_partner_id | Winning buyer | uuid | No | None | No |
| debt_sale_lot.buyer_class | AMC or non-AMC | varchar(10) | No | LOV-BUYER-CLASS | No |
| debt_sale_lot.signing_date | Date the sale was signed | date | No | None | No |
| debt_sale_lot.approval_authority | Authority that approved the sale | varchar(60) | No | None | No |

##### A2.13.3.3 Roles and permissions

| Role | Use |
|---|---|
| Debt sale officer | Primary |
| Head of Asset Liquidity | Also uses |

#### A2.13.4 Acceptance criteria

##### A2.13.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S6-013-01 | Handle a buyer put-back claim | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.13.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.13.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S6-013-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S6-013-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.13.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.14 Close a case awarded in a sold lot

#### A2.14.1 Intent

**Business objective.** Stops every open action on a case whose account is sold in a lot, and closes it.

**Problem.** Debt sales run on spreadsheets with no baseline turnaround.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Debt sale turnaround | 45 days | Decision log and Workbench records | Monthly |

#### A2.14.2 Description

**Functional overview.** Stops every open action on a case whose account is sold in a lot, and closes it.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Close a case awarded in a sold lot | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, ALS and GL

**Prerequisites.** FEAT-DBS-09

#### A2.14.3 Business rules and structure

##### A2.14.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S6-014-1 | Account with an open deviation selected for a lot (R-DS-02) | MSG-S6-001 {account} has an open deviation and cannot be sold. |
| VR-S6-014-2 | An action outside the role's permission | MSG-P4-002 You cannot {action} here. Your role does not include it. |
| BR-S6-014 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.14.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Debt sale officer | Also uses |

#### A2.14.4 Acceptance criteria

##### A2.14.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S6-014-01 | Close a case awarded in a sold lot | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.14.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.14.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S6-014-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S6-014-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.14.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.15 Confirm buyer remittance

#### A2.15.1 Intent

**Business objective.** Matches the buyer's payment to the award and closes the money side of the lot.

**Problem.** Debt sales run on spreadsheets with no baseline turnaround.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Debt sale turnaround | 45 days | Decision log and Workbench records | Monthly |

#### A2.15.2 Description

**Functional overview.** Matches the buyer's payment to the award and closes the money side of the lot.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Confirm buyer remittance | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL

**Prerequisites.** FEAT-DBS-12

#### A2.15.3 Business rules and structure

##### A2.15.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S6-015-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-DS-25 | Confirm settlement and release the data transfer, when payment received in full | Moves to SETTLED |
| R-DS-26 | Cancel the award and score the cancellation against the buyer, when cancellation recorded with a reason | Moves to AWARD_CANCELED_DS |
| R-DS-27 | Cancel the award and score the buyer, when payment absent and the settlement period passed | Moves to AWARD_CANCELED_DS |
| BR-S6-015 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.15.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Credit Administration officer | Also uses |

#### A2.15.4 Acceptance criteria

##### A2.15.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S6-015-01 | Confirm buyer remittance | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.15.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.15.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S6-015-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S6-015-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.15.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.16 Apply the debt sale cap

#### A2.16.1 Intent

**Business objective.** Holds the sale population inside the policy cap and reports the headroom.

**Problem.** Debt sales run on spreadsheets with no baseline turnaround.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Debt sale turnaround | 45 days | Decision log and Workbench records | Monthly |

#### A2.16.2 Description

**Functional overview.** Holds the sale population inside the policy cap and reports the headroom.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Apply the debt sale cap | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench

**Prerequisites.** FEAT-DBS-01

#### A2.16.3 Business rules and structure

##### A2.16.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S6-016-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| BR-S6-016 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.16.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Debt sale officer | Also uses |

#### A2.16.4 Acceptance criteria

##### A2.16.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S6-016-01 | Apply the debt sale cap | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.16.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.16.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S6-016-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S6-016-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.16.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|
| REQ-S6-001 | Accounts eligible for sale are selected by rule against the policy cap. | Must | E5 |
| REQ-S6-002 | Lots are built with an estimated price, and the reserve price is approved before the lot is offered. | Must | E5 |
| REQ-S6-003 | The data room holds a masked data tape, and no unmasked personal data leaves the bank. | Must | E5 |
| REQ-S6-004 | Buyers pass a know your customer, licensing and eligibility check before they bid. | Must | E6 |
| REQ-S6-005 | A buyer who fails the check is given a remediation window and is removed from the panel if it is not met. | Must | E6 |
| REQ-S6-006 | The award of a lot is approved and recorded with the price achieved against the reserve. | Must | E6 |
| REQ-S6-007 | An account awarded in a lot stops every other open action on its case the same day. | Must | E6 |
| REQ-S6-008 | Data transfer, derecognition and the general ledger posting follow the award without re-keying. | Must | E6 |
| REQ-S6-009 | A put-back claim from a buyer is reviewed against the sale terms and either accepted or refused with a reason. | Must | E6 |

## Screens

| Screen | What it is for | First in |
|---|---|---|
| SCR-25 Lot builder | Select accounts, build lots, set the reserve and send for approval | E5 |
| SCR-26 Award | Bids against the reserve and the award decision | E6 |
| PRT-05 Data room | Lot data tapes and documents for admitted buyers, with bids | E5 |

## Document sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| FSD owner, business analyst | | | |
| Business owner | | | |
| Solution architect | | | |
| QA lead | | | |

## Appendix A. Business glossary

Terms follow the Recovery Workbench Business Glossary.

| Term | Thai | Meaning |
|---|---|---|
| Debt sale | การขายหนี้ | Sale of accounts to a debt buyer |
| Lot | กองหนี้ | A group of accounts offered to debt buyers together |
| Reserve price | ราคาสงวน | The lowest price approved for a debt sale lot |
| Put-back | การขอคืนบัญชี | A buyer returning an account under the sale terms |

## Appendix B. UI behavior

Components, field states, error display, confirmations and colors follow the Recovery Workbench Design System and Component Library. Message wording follows the Error and Message Standard.

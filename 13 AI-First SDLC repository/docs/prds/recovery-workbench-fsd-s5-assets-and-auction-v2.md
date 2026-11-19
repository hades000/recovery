<!-- working-copy-of: requirement/legacy/03-requirements-and-specifications/recovery-workbench-functional-specifications-by-module-v4_extracted/Recovery Workbench FSD S5 Assets and auction v2.md -->
> **Working copy.** Canonical source: `requirement/legacy/03-requirements-and-specifications/recovery-workbench-functional-specifications-by-module-v4_extracted/Recovery Workbench FSD S5 Assets and auction v2.md`. Edit the source, not this copy.

# Recovery Workbench S5 Assets and auction

Functional specification. SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD S5 Assets and auction |
| Document ID | S5-RWB-FSD-v2 |
| Version | 2 |
| Status | In review |
| Classification | Confidential |
| Date | 28 October 2026 |
| FSD owner | Business analyst, S5 |
| Business owner | Business lead |

| Module code | Module name | First in |
|---|---|---|
| S5 | Assets and auction | E3; E4 |

**Feature scope.** Asset record, holding, floor price, listing, auction rounds, RAMC.

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification S5 Assets and auction | TSD | Pair |
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

**In scope.** Asset record, holding, floor price, listing, auction rounds, RAMC.

**Out of scope.** Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces.

**Dependencies.** FEAT-APD-01; FEAT-AST-01; FEAT-AST-05; FEAT-AST-07; FEAT-AST-10; FEAT-AST-11; FEAT-AST-12; FEAT-AST-13

**Constraints.** Built in the ACE service as part of the recovery module; data through COLLINS and file loads; every value a business person may change is a versioned data row (principle 1).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section |
|---|---|---|---|---|---|---|
| S5 | FEAT-AST-01 | Take a repossessed vehicle onto the books | System | Creates the asset record from the repossession result and starts the holding clock. | E3 | A2.1 |
| S5 | FEAT-AST-02 | Take a property onto the books after a deed in lieu | System | Creates the asset record when a deed in lieu transfer completes. | E3 | A2.2 |
| S5 | FEAT-AST-03 | Take a property onto the books after an LED auction | System | Creates the asset record when the bank takes the property at the enforcement auction. | E3 | A2.3 |
| S5 | FEAT-AST-04 | Serve the statutory notice and prove delivery | System | Sends the notice the repossession requires and records the proof. | E3 | A2.4 |
| S5 | FEAT-AST-05 | Track holding age against the provision steps | System | Counts the days held and applies the provision step the policy sets at each threshold. | E3 | A2.5 |
| S5 | FEAT-AST-06 | Record and track the asset stock balance | User | Gives the stock balance an owner and a number on one screen. It has no owner today. | E3 | A2.6 |
| S5 | FEAT-AST-07 | Maintain a held property | User | Records maintenance, insurance and custody costs against the asset. | E3 | A2.7 |
| S5 | FEAT-AST-08 | Evict occupants from a held property | User | Opens and tracks the eviction, which needs Legal and has no legal owner today. | E4 | A2.8 |
| S5 | FEAT-AST-09 | Re-appraise a held asset on cycle | System | Raises the re-appraisal order when the holding period passes the re-appraisal interval. | E3 | A2.9 |
| S5 | FEAT-AST-10 | Recommend the disposal route | System | Proposes auction, broker, RAMC, buy-back or rental with the expected return on each. | E3 | A2.10 |
| S5 | FEAT-AST-11 | Set the start and floor price | User | Lets the sale officer set the opening price and the floor, with the head of NPA approving the floor. | E3 | A2.11 |
| S5 | FEAT-AST-12 | Publish the listing | System | Puts the asset on HOME.SCB and the auction portal with its price and schedule. | E3 | A2.12 |
| S5 | FEAT-AST-13 | Run the descending price schedule | System | Steps the price down on the ladder at each round until a bid clears the floor. | E4 | A2.13 |
| S5 | FEAT-AST-14 | Allocate the asset to an auction vendor by distance | System | Picks one of the four vendors by distance and capacity, as the current rule does. | E4 | A2.14 |
| S5 | FEAT-AST-15 | Run auction rounds and report bids | User | Lets the vendor run each round and report the bids back into the case. | E4 | A2.15 |
| S5 | FEAT-AST-16 | Accept a bid below the floor with a second signature | User | Routes any bid under the floor for a second approval before it can be accepted. | E4 | A2.16 |
| S5 | FEAT-AST-17 | Re-list on no bid | System | Puts the asset back on the schedule at the next price step when a round closes with no bid. | E4 | A2.17 |
| S5 | FEAT-AST-18 | Enforce the five-day payment term | System | Tracks the winning bidder's payment against the term and releases the asset if it is missed. | E4 | A2.18 |
| S5 | FEAT-AST-19 | Transfer vehicle registration | System | Prepares and submits the registration transfer through SCIS. | E4 | A2.19 |
| S5 | FEAT-AST-20 | Record a property transfer at the Land Office | User | Tracks the Land Office transfer, which stays a person and officer step. | E4 | A2.20 |
| S5 | FEAT-AST-21 | Apply proceeds and raise the shortfall | System | Applies the sale money to the balance and raises any residual to the next decision. | E4 | A2.21 |
| S5 | FEAT-AST-22 | Transfer a pool to RAMC or the joint venture | User | Takes a pool of assets to RAMC with committee approval, and records the transfer. | E4 | A2.22 |
| S5 | FEAT-AST-23 | Arrange a customer buy-back | User | Opens the buy-back where the former owner repurchases, with the approval the limit requires. | E4 | A2.23 |
| S5 | FEAT-AST-24 | Rent a held asset to a third party | User | Records the rental, the debit and the arrears follow-up while the asset is held. | E4 | A2.24 |
| S5 | FEAT-AST-25 | Sell through a broker | User | Opens the broker route with its fee and terms, and tracks it to the sale. | E4 | A2.25 |

### A1.3 Background

The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date, or show their date as stale.

## A2. Functional decomposition

### A2.1 Take a repossessed vehicle onto the books

#### A2.1.1 Intent

**Business objective.** Creates the asset record from the repossession result and starts the holding clock.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.1.2 Description

**Functional overview.** Creates the asset record from the repossession result and starts the holding clock.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Take a repossessed vehicle onto the books | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** RPS, AMIS

**Prerequisites.** FEAT-CWC-02

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-001-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-DIS-06 | Start the holding age clock and the provision step clock, and charge cost of carry monthly, when title_status in (clear, under_transfer) | Moves to ASSET_HELD |
| R-DIS-01 | Create the asset record from RPS with condition, photographs and location, when asset_type = vehicle and statutory_notice_proved = Y | Moves to ASSET_ON_BOOKS |
| R-DIS-03 | Record the LED result and create the asset record, when led_result = handed_over after the 100, 90, 80 then 70 percent ladder | Moves to ASSET_ON_BOOKS |
| BR-S5-001 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Sale officer | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-001-01 | Take a repossessed vehicle onto the books | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-001-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-001-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.1.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.2 Take a property onto the books after a deed in lieu

#### A2.2.1 Intent

**Business objective.** Creates the asset record when a deed in lieu transfer completes.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.2.2 Description

**Functional overview.** Creates the asset record when a deed in lieu transfer completes.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Take a property onto the books after a deed in lieu | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** AMIS, CCMS

**Prerequisites.** FEAT-TRT-14

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-002-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-DIS-02 | Create the asset record from AMIS with the opening book value, when asset_type = property and transfer registered | Moves to ASSET_ON_BOOKS |
| R-DIS-01 | Create the asset record from RPS with condition, photographs and location, when asset_type = vehicle and statutory_notice_proved = Y | Moves to ASSET_ON_BOOKS |
| R-DIS-03 | Record the LED result and create the asset record, when led_result = handed_over after the 100, 90, 80 then 70 percent ladder | Moves to ASSET_ON_BOOKS |
| BR-S5-002 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Sale officer | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-002-01 | Take a property onto the books after a deed in lieu | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-002-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-002-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.2.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.3 Take a property onto the books after an LED auction

#### A2.3.1 Intent

**Business objective.** Creates the asset record when the bank takes the property at the enforcement auction.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.3.2 Description

**Functional overview.** Creates the asset record when the bank takes the property at the enforcement auction.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Take a property onto the books after an LED auction | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** AMIS, LED portal

**Prerequisites.** FEAT-LIT-19

#### A2.3.3 Business rules and structure

##### A2.3.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-003-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-DIS-01 | Create the asset record from RPS with condition, photographs and location, when asset_type = vehicle and statutory_notice_proved = Y | Moves to ASSET_ON_BOOKS |
| R-DIS-02 | Create the asset record from AMIS with the opening book value, when asset_type = property and transfer registered | Moves to ASSET_ON_BOOKS |
| R-DIS-03 | Record the LED result and create the asset record, when led_result = handed_over after the 100, 90, 80 then 70 percent ladder | Moves to ASSET_ON_BOOKS |
| BR-S5-003 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.3.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Sale officer | Also uses |

#### A2.3.4 Acceptance criteria

##### A2.3.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-003-01 | Take a property onto the books after an LED auction | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.3.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.3.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-003-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-003-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.3.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.4 Serve the statutory notice and prove delivery

#### A2.4.1 Intent

**Business objective.** Sends the notice the repossession requires and records the proof.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.4.2 Description

**Functional overview.** Sends the notice the repossession requires and records the proof.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Serve the statutory notice and prove delivery | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** WIN

**Prerequisites.** FEAT-OCC-02

#### A2.4.3 Business rules and structure

##### A2.4.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-004-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-DIS-04 | Hold the take-on, raise a failed notice task and re-serve on a confirmed address, when delivery_proved = N | Moves to FAILED_NOTICE_QUEUE |
| R-DIS-05 | Re-serve the statutory notice and resume the take-on, when new_address_confirmed = Y | Moves to ASSET_PENDING_TAKE_ON |
| BR-S5-004 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.4.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Sale officer | Also uses |

#### A2.4.4 Acceptance criteria

##### A2.4.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-004-01 | Serve the statutory notice and prove delivery | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.4.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.4.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-004-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-004-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.4.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.5 Track holding age against the provision steps

#### A2.5.1 Intent

**Business objective.** Counts the days held and applies the provision step the policy sets at each threshold.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.5.2 Description

**Functional overview.** Counts the days held and applies the provision step the policy sets at each threshold.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Track holding age against the provision steps | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** AMIS, ALS and GL

**Prerequisites.** FEAT-AST-01

#### A2.5.3 Business rules and structure

##### A2.5.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-005-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-DIS-06 | Start the holding age clock and the provision step clock, and charge cost of carry monthly, when title_status in (clear, under_transfer) | Moves to ASSET_HELD |
| BR-S5-005 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.5.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| NPA and asset manager | Also uses |

#### A2.5.4 Acceptance criteria

##### A2.5.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-005-01 | Track holding age against the provision steps | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.5.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.5.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-005-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-005-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.5.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.6 Record and track the asset stock balance

#### A2.6.1 Intent

**Business objective.** Gives the stock balance an owner and a number on one screen. It has no owner today.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.6.2 Description

**Functional overview.** Gives the stock balance an owner and a number on one screen. It has no owner today.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | NPA and asset manager | Opens the screen and record and track the asset stock balance | Checks the role, the capability area and the scope |
| 2 | NPA and asset manager | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** AMIS, RPS

**Prerequisites.** FEAT-AST-05

#### A2.6.3 Business rules and structure

##### A2.6.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-006-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-DIS-01 | Create the asset record from RPS with condition, photographs and location, when asset_type = vehicle and statutory_notice_proved = Y | Moves to ASSET_ON_BOOKS |
| R-DIS-02 | Create the asset record from AMIS with the opening book value, when asset_type = property and transfer registered | Moves to ASSET_ON_BOOKS |
| R-DIS-03 | Record the LED result and create the asset record, when led_result = handed_over after the 100, 90, 80 then 70 percent ladder | Moves to ASSET_ON_BOOKS |
| BR-S5-006 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.6.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| asset.case_id | The recovery_case this record belongs to | uuid | No | None | No |
| asset.collateral_id | The collateral this record belongs to | uuid | No | None | No |
| asset.asset_ref | Asset reference | varchar(20) | Yes | None | No |
| asset.asset_code | Asset code | varchar(20) | No | None | No |
| asset.asset_type | Detached house, townhouse, condominium, land, vehicle | varchar(20) | Yes | LOV-ASSET-TYPE | No |
| asset.transfer_in_type | Auction purchase, deed in lieu, repossession | varchar(20) | Yes | LOV-TRANSFER-IN | No |
| asset.from_segment | Segment the asset came from | varchar(20) | No | LOV-SEGMENT | No |
| asset.transfer_in_date | Date ownership passed to the bank | date | Yes | None | No |

##### A2.6.3.3 Roles and permissions

| Role | Use |
|---|---|
| NPA and asset manager | Primary |
| Head of NPA | Also uses |

#### A2.6.4 Acceptance criteria

##### A2.6.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-006-01 | Record and track the asset stock balance | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.6.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.6.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-006-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-006-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.6.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.7 Maintain a held property

#### A2.7.1 Intent

**Business objective.** Records maintenance, insurance and custody costs against the asset.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.7.2 Description

**Functional overview.** Records maintenance, insurance and custody costs against the asset.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | NPA and asset manager | Opens the screen and maintain a held property | Checks the role, the capability area and the scope |
| 2 | NPA and asset manager | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** AMIS

**Prerequisites.** FEAT-AST-05

#### A2.7.3 Business rules and structure

##### A2.7.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-007-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-DIS-37 | Record the bid against the round and the asset, when the event occurs | Moves to BID_RECEIVED |
| BR-S5-007 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.7.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| asset.case_id | The recovery_case this record belongs to | uuid | No | None | No |
| asset.collateral_id | The collateral this record belongs to | uuid | No | None | No |
| asset.asset_ref | Asset reference | varchar(20) | Yes | None | No |
| asset.asset_code | Asset code | varchar(20) | No | None | No |
| asset.asset_type | Detached house, townhouse, condominium, land, vehicle | varchar(20) | Yes | LOV-ASSET-TYPE | No |
| asset.transfer_in_type | Auction purchase, deed in lieu, repossession | varchar(20) | Yes | LOV-TRANSFER-IN | No |
| asset.from_segment | Segment the asset came from | varchar(20) | No | LOV-SEGMENT | No |
| asset.transfer_in_date | Date ownership passed to the bank | date | Yes | None | No |

##### A2.7.3.3 Roles and permissions

| Role | Use |
|---|---|
| NPA and asset manager | Primary |
| Partner and agency manager | Also uses |

#### A2.7.4 Acceptance criteria

##### A2.7.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-007-01 | Maintain a held property | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.7.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.7.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-007-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-007-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.7.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.8 Evict occupants from a held property

#### A2.8.1 Intent

**Business objective.** Opens and tracks the eviction, which needs Legal and has no legal owner today.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.8.2 Description

**Functional overview.** Opens and tracks the eviction, which needs Legal and has no legal owner today.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Sale officer | Opens the screen and evict occupants from a held property | Checks the role, the capability area and the scope |
| 2 | Sale officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** LIT, AMIS

**Prerequisites.** FEAT-AST-07

#### A2.8.3 Business rules and structure

##### A2.8.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-008-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-DIS-13 | Raise the eviction instruction to Legal, when occupancy_status = occupied | Moves to EVICTION_REQUIRED |
| BR-S5-008 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.8.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| asset.case_id | The recovery_case this record belongs to | uuid | No | None | No |
| asset.collateral_id | The collateral this record belongs to | uuid | No | None | No |
| asset.asset_ref | Asset reference | varchar(20) | Yes | None | No |
| asset.asset_code | Asset code | varchar(20) | No | None | No |
| asset.asset_type | Detached house, townhouse, condominium, land, vehicle | varchar(20) | Yes | LOV-ASSET-TYPE | No |
| asset.transfer_in_type | Auction purchase, deed in lieu, repossession | varchar(20) | Yes | LOV-TRANSFER-IN | No |
| asset.from_segment | Segment the asset came from | varchar(20) | No | LOV-SEGMENT | No |
| asset.transfer_in_date | Date ownership passed to the bank | date | Yes | None | No |

##### A2.8.3.3 Roles and permissions

| Role | Use |
|---|---|
| Sale officer | Primary |
| Legal counsel | Also uses |

#### A2.8.4 Acceptance criteria

##### A2.8.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-008-01 | Evict occupants from a held property | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.8.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.8.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-008-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-008-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.8.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.9 Re-appraise a held asset on cycle

#### A2.9.1 Intent

**Business objective.** Raises the re-appraisal order when the holding period passes the re-appraisal interval.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.9.2 Description

**Functional overview.** Raises the re-appraisal order when the holding period passes the re-appraisal interval.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Re-appraise a held asset on cycle | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** SVAF

**Prerequisites.** FEAT-VAL-01

#### A2.9.3 Business rules and structure

##### A2.9.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-009-1 | Appraisal older than one year | MSG-S5-002 The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| R-DIS-44 | Re-list the asset and order a re-appraisal where the cycle is due, when relist_count below the re-list limit | Moves to RELISTED |
| R-DIS-15 | Order the re-appraisal through SVAF, when appraisal_date older than 12 months and one_year_rule_applied = N | Moves to REAPPRAISAL_ORDERED |
| R-DIS-06 | Start the holding age clock and the provision step clock, and charge cost of carry monthly, when title_status in (clear, under_transfer) | Moves to ASSET_HELD |
| BR-S5-009 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.9.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Sale officer | Also uses |

#### A2.9.4 Acceptance criteria

##### A2.9.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-009-01 | Re-appraise a held asset on cycle | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.9.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.9.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-009-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-009-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.9.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.10 Recommend the disposal route

#### A2.10.1 Intent

**Business objective.** Proposes auction, broker, RAMC, buy-back or rental with the expected return on each.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.10.2 Description

**Functional overview.** Proposes auction, broker, RAMC, buy-back or rental with the expected return on each.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Recommend the disposal route | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, COLLINS

**Prerequisites.** FEAT-AST-05

#### A2.10.3 Business rules and structure

##### A2.10.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-010-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-DIS-14 | Return the asset to hold and resume the disposal route, when occupancy_status = vacant | Moves to ASSET_HELD |
| R-DIS-08 | Release the asset to hold and to the disposal route, when title_status = clear | Moves to ASSET_HELD |
| R-DIS-19 | Pricing agent recommends the disposal route with reasons and the COLLINS economics, when current_appraisal = Y and title_status = clear | Moves to ROUTE_RECOMMENDED |
| BR-S5-010 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.10.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Sale officer | Also uses |

#### A2.10.4 Acceptance criteria

##### A2.10.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-010-01 | Recommend the disposal route | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.10.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.10.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-010-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-010-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.10.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.11 Set the start and floor price

#### A2.11.1 Intent

**Business objective.** Lets the sale officer set the opening price and the floor, with the head of NPA approving the floor.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.11.2 Description

**Functional overview.** Lets the sale officer set the opening price and the floor, with the head of NPA approving the floor.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Sale officer | Opens the screen and set the start and floor price | Checks the role, the capability area and the scope |
| 2 | Sale officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench, COLLINS

**Prerequisites.** FEAT-AST-10

#### A2.11.3 Business rules and structure

##### A2.11.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-011-1 | Floor price below the approver's limit | MSG-S5-001 The floor is {pct} of fair market value, below the {limit} this level may approve. |
| R-DIS-28 | Pricing agent proposes the opening price and the floor price as the reserve, when the event occurs | Moves to PRICE_PROPOSED |
| R-DIS-17 | Update the appraised value and reset the list and floor price inputs, when outlier_flag = N or officer_accepted = Y | Moves to ASSET_HELD |
| R-DIS-29 | Fix the floor as the reserve and set the step schedule by asset class, when officer_approved = Y | Moves to FLOOR_APPROVED |
| BR-S5-011 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.11.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| asset.case_id | The recovery_case this record belongs to | uuid | No | None | No |
| asset.collateral_id | The collateral this record belongs to | uuid | No | None | No |
| asset.asset_ref | Asset reference | varchar(20) | Yes | None | No |
| asset.asset_code | Asset code | varchar(20) | No | None | No |
| asset.asset_type | Detached house, townhouse, condominium, land, vehicle | varchar(20) | Yes | LOV-ASSET-TYPE | No |
| asset.transfer_in_type | Auction purchase, deed in lieu, repossession | varchar(20) | Yes | LOV-TRANSFER-IN | No |
| asset.from_segment | Segment the asset came from | varchar(20) | No | LOV-SEGMENT | No |
| asset.transfer_in_date | Date ownership passed to the bank | date | Yes | None | No |

##### A2.11.3.3 Roles and permissions

| Role | Use |
|---|---|
| Sale officer | Primary |
| Head of NPA | Also uses |

#### A2.11.4 Acceptance criteria

##### A2.11.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-011-01 | Set the start and floor price | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.11.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.11.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-011-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-011-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.11.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.12 Publish the listing

#### A2.12.1 Intent

**Business objective.** Puts the asset on HOME.SCB and the auction portal with its price and schedule.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.12.2 Description

**Functional overview.** Puts the asset on HOME.SCB and the auction portal with its price and schedule.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Publish the listing | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** HOME.SCB, auction portals

**Prerequisites.** FEAT-AST-11

#### A2.12.3 Business rules and structure

##### A2.12.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-012-1 | Floor price below the approver's limit | MSG-S5-001 The floor is {pct} of fair market value, below the {limit} this level may approve. |
| R-DIS-33 | Publish the listing to HOME.SCB, the EASY app and the auction portal, with the floor not published, when photographs_count above 0 and inspection_report present and title_status = clear | Moves to LISTING_LIVE |
| R-DIS-67 | Pause the listing and the price schedule, when deviation_open in (X1, X4, X5) | Moves to DISPOSAL_PAUSED_DEVIATION |
| R-DIS-21 | Approve the portal auction route and log the decision, when route = auction and inside the limit | Moves to ROUTE_APPROVED_AUCTION |
| BR-S5-012 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.12.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Sale officer | Also uses |

#### A2.12.4 Acceptance criteria

##### A2.12.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-012-01 | Publish the listing | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.12.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.12.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-012-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-012-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.12.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.13 Run the descending price schedule

#### A2.13.1 Intent

**Business objective.** Steps the price down on the ladder at each round until a bid clears the floor.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.13.2 Description

**Functional overview.** Steps the price down on the ladder at each round until a bid clears the floor.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Run the descending price schedule | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Auction portals

**Prerequisites.** FEAT-AST-12

#### A2.13.3 Business rules and structure

##### A2.13.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-013-1 | Floor price below the approver's limit | MSG-S5-001 The floor is {pct} of fair market value, below the {limit} this level may approve. |
| R-DIS-38 | Step the price down on the published schedule and open the next round, when bid_count = 0 and price_at_round above floor_price | Moves to ROUND_OPEN |
| R-DIS-17 | Update the appraised value and reset the list and floor price inputs, when outlier_flag = N or officer_accepted = Y | Moves to ASSET_HELD |
| R-DIS-28 | Pricing agent proposes the opening price and the floor price as the reserve, when the event occurs | Moves to PRICE_PROPOSED |
| BR-S5-013 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.13.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Sale officer | Also uses |

#### A2.13.4 Acceptance criteria

##### A2.13.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-013-01 | Run the descending price schedule | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.13.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.13.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-013-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-013-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.13.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.14 Allocate the asset to an auction vendor by distance

#### A2.14.1 Intent

**Business objective.** Picks one of the four vendors by distance and capacity, as the current rule does.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.14.2 Description

**Functional overview.** Picks one of the four vendors by distance and capacity, as the current rule does.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Allocate the asset to an auction vendor by distance | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Partner portal

**Prerequisites.** FEAT-PRM-03

#### A2.14.3 Business rules and structure

##### A2.14.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-014-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-DIS-30 | Allocate the asset to the vendor with the highest predicted price on the scorecard, not by distance, when asset_type = vehicle | Moves to VENDOR_ALLOCATED |
| R-DIS-31 | Re-allocate to the next vendor on the scorecard, when vendor_capacity = N or panel_status = suspended | Moves to VENDOR_ALLOCATED |
| R-DIS-32 | Vendor lists the asset at the starting bid on the portal, when vendor_capacity = Y and inspection form complete | Moves to LISTING_LIVE |
| BR-S5-014 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.14.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Sale officer | Also uses |

#### A2.14.4 Acceptance criteria

##### A2.14.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-014-01 | Allocate the asset to an auction vendor by distance | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.14.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.14.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-014-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-014-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.14.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.15 Run auction rounds and report bids

#### A2.15.1 Intent

**Business objective.** Lets the vendor run each round and report the bids back into the case.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.15.2 Description

**Functional overview.** Lets the vendor run each round and report the bids back into the case.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Auction vendor | Opens the screen and run auction rounds and report bids | Checks the role, the capability area and the scope |
| 2 | Auction vendor | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Partner portal, auction portals

**Prerequisites.** FEAT-AST-14

#### A2.15.3 Business rules and structure

##### A2.15.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-015-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-DIS-49 | Cancel the award, score the vendor and reopen the round, when payment absent and payment_due_date passed | Moves to AWARD_CANCELED |
| BR-S5-015 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.15.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| asset.case_id | The recovery_case this record belongs to | uuid | No | None | No |
| asset.collateral_id | The collateral this record belongs to | uuid | No | None | No |
| asset.asset_ref | Asset reference | varchar(20) | Yes | None | No |
| asset.asset_code | Asset code | varchar(20) | No | None | No |
| asset.asset_type | Detached house, townhouse, condominium, land, vehicle | varchar(20) | Yes | LOV-ASSET-TYPE | No |
| asset.transfer_in_type | Auction purchase, deed in lieu, repossession | varchar(20) | Yes | LOV-TRANSFER-IN | No |
| asset.from_segment | Segment the asset came from | varchar(20) | No | LOV-SEGMENT | No |
| asset.transfer_in_date | Date ownership passed to the bank | date | Yes | None | No |

##### A2.15.3.3 Roles and permissions

| Role | Use |
|---|---|
| Auction vendor | Primary |
| Sale officer | Also uses |

#### A2.15.4 Acceptance criteria

##### A2.15.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-015-01 | Run auction rounds and report bids | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.15.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.15.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-015-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-015-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.15.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.16 Accept a bid below the floor with a second signature

#### A2.16.1 Intent

**Business objective.** Routes any bid under the floor for a second approval before it can be accepted.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.16.2 Description

**Functional overview.** Routes any bid under the floor for a second approval before it can be accepted.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Sale officer | Opens the screen and accept a bid below the floor with a second signature | Checks the role, the capability area and the scope |
| 2 | Sale officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-APD-01

#### A2.16.3 Business rules and structure

##### A2.16.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-016-1 | Floor price below the approver's limit | MSG-S5-001 The floor is {pct} of fair market value, below the {limit} this level may approve. |
| VR-S5-016-2 | Appraisal older than one year | MSG-S5-002 The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| R-DIS-42 | Accept the bid below the floor and agree the sale, when second_signature_by present | Moves to SALE_AGREED |
| R-DIS-41 | Route the bid for a second signature, when bid_amount below floor_price | Moves to SECOND_SIGNATURE_PENDING |
| R-DIS-17 | Update the appraised value and reset the list and floor price inputs, when outlier_flag = N or officer_accepted = Y | Moves to ASSET_HELD |
| BR-S5-016 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.16.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| asset.case_id | The recovery_case this record belongs to | uuid | No | None | No |
| asset.collateral_id | The collateral this record belongs to | uuid | No | None | No |
| asset.asset_ref | Asset reference | varchar(20) | Yes | None | No |
| asset.asset_code | Asset code | varchar(20) | No | None | No |
| asset.asset_type | Detached house, townhouse, condominium, land, vehicle | varchar(20) | Yes | LOV-ASSET-TYPE | No |
| asset.transfer_in_type | Auction purchase, deed in lieu, repossession | varchar(20) | Yes | LOV-TRANSFER-IN | No |
| asset.from_segment | Segment the asset came from | varchar(20) | No | LOV-SEGMENT | No |
| asset.transfer_in_date | Date ownership passed to the bank | date | Yes | None | No |

##### A2.16.3.3 Roles and permissions

| Role | Use |
|---|---|
| Sale officer | Primary |
| Head of NPA | Also uses |

#### A2.16.4 Acceptance criteria

##### A2.16.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-016-01 | Accept a bid below the floor with a second signature | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.16.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.16.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-016-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-016-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.16.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.17 Re-list on no bid

#### A2.17.1 Intent

**Business objective.** Puts the asset back on the schedule at the next price step when a round closes with no bid.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.17.2 Description

**Functional overview.** Puts the asset back on the schedule at the next price step when a round closes with no bid.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Re-list on no bid | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Auction portals

**Prerequisites.** FEAT-AST-13

#### A2.17.3 Business rules and structure

##### A2.17.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-017-1 | Floor price below the approver's limit | MSG-S5-001 The floor is {pct} of fair market value, below the {limit} this level may approve. |
| R-DIS-38 | Step the price down on the published schedule and open the next round, when bid_count = 0 and price_at_round above floor_price | Moves to ROUND_OPEN |
| R-DIS-29 | Fix the floor as the reserve and set the step schedule by asset class, when officer_approved = Y | Moves to FLOOR_APPROVED |
| R-DIS-30 | Allocate the asset to the vendor with the highest predicted price on the scorecard, not by distance, when asset_type = vehicle | Moves to VENDOR_ALLOCATED |
| BR-S5-017 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.17.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Sale officer | Also uses |

#### A2.17.4 Acceptance criteria

##### A2.17.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-017-01 | Re-list on no bid | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.17.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.17.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-017-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-017-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.17.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.18 Enforce the five-day payment term

#### A2.18.1 Intent

**Business objective.** Tracks the winning bidder's payment against the term and releases the asset if it is missed.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.18.2 Description

**Functional overview.** Tracks the winning bidder's payment against the term and releases the asset if it is missed.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Enforce the five-day payment term | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Auction portals, ALS and GL

**Prerequisites.** FEAT-AST-16

#### A2.18.3 Business rules and structure

##### A2.18.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-018-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-DIS-11 | Release the invoice for payment and return the asset to hold, when sale_officer_accepted = Y | Moves to ASSET_HELD |
| R-DIS-37 | Record the bid against the round and the asset, when the event occurs | Moves to BID_RECEIVED |
| BR-S5-018 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.18.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Sale officer | Also uses |

#### A2.18.4 Acceptance criteria

##### A2.18.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-018-01 | Enforce the five-day payment term | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.18.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.18.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-018-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-018-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.18.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.19 Transfer vehicle registration

#### A2.19.1 Intent

**Business objective.** Prepares and submits the registration transfer through SCIS.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.19.2 Description

**Functional overview.** Prepares and submits the registration transfer through SCIS.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Transfer vehicle registration | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** SCIS, RPS

**Prerequisites.** FEAT-AST-18

#### A2.19.3 Business rules and structure

##### A2.19.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-019-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-DIS-51 | Transfer the registration through SCIS, when asset_type = vehicle | Moves to ASSET_SOLD |
| BR-S5-019 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.19.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Sale officer | Also uses |

#### A2.19.4 Acceptance criteria

##### A2.19.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-019-01 | Transfer vehicle registration | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.19.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.19.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-019-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-019-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.19.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.20 Record a property transfer at the Land Office

#### A2.20.1 Intent

**Business objective.** Tracks the Land Office transfer, which stays a person and officer step.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.20.2 Description

**Functional overview.** Tracks the Land Office transfer, which stays a person and officer step.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Sale officer | Opens the screen and record a property transfer at the Land Office | Checks the role, the capability area and the scope |
| 2 | Sale officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Land Office, AMIS

**Prerequisites.** FEAT-AST-18

#### A2.20.3 Business rules and structure

##### A2.20.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-020-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-DIS-52 | Release the documents from custody and record the transfer at the Land Office, when asset_type = property | Moves to ASSET_SOLD |
| R-DIS-02 | Create the asset record from AMIS with the opening book value, when asset_type = property and transfer registered | Moves to ASSET_ON_BOOKS |
| BR-S5-020 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.20.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| asset.case_id | The recovery_case this record belongs to | uuid | No | None | No |
| asset.collateral_id | The collateral this record belongs to | uuid | No | None | No |
| asset.asset_ref | Asset reference | varchar(20) | Yes | None | No |
| asset.asset_code | Asset code | varchar(20) | No | None | No |
| asset.asset_type | Detached house, townhouse, condominium, land, vehicle | varchar(20) | Yes | LOV-ASSET-TYPE | No |
| asset.transfer_in_type | Auction purchase, deed in lieu, repossession | varchar(20) | Yes | LOV-TRANSFER-IN | No |
| asset.from_segment | Segment the asset came from | varchar(20) | No | LOV-SEGMENT | No |
| asset.transfer_in_date | Date ownership passed to the bank | date | Yes | None | No |

##### A2.20.3.3 Roles and permissions

| Role | Use |
|---|---|
| Sale officer | Primary |
| Legal counsel | Also uses |

#### A2.20.4 Acceptance criteria

##### A2.20.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-020-01 | Record a property transfer at the Land Office | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.20.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.20.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-020-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-020-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.20.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.21 Apply proceeds and raise the shortfall

#### A2.21.1 Intent

**Business objective.** Applies the sale money to the balance and raises any residual to the next decision.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.21.2 Description

**Functional overview.** Applies the sale money to the balance and raises any residual to the next decision.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: a load, an event or a timer | Reads the version of the rules in force |
| 2 | System | Apply proceeds and raise the shortfall | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ALS and GL

**Prerequisites.** FEAT-PAY-10

#### A2.21.3 Business rules and structure

##### A2.21.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-021-1 | Data product stale after a late or failed load | MSG-P1-001 {product} is from {date}. Today's load has not arrived. |
| R-DIS-55 | Raise the residual for the D9 decision, when shortfall_amount above 0 | Moves to SHORTFALL_RAISED |
| R-DIS-54 | Apply the proceeds to the case and the loan account, and match the vendor fee, when the event occurs | Moves to PROCEEDS_APPLIED |
| R-DIS-71 | Hold the case, name the missing field and raise a task for the owner, when residual_route is not set | Moves to UNMATCHED_EXCEPTION |
| BR-S5-021 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.21.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Sale officer | Also uses |

#### A2.21.4 Acceptance criteria

##### A2.21.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-021-01 | Apply proceeds and raise the shortfall | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.21.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.21.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-021-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-021-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.21.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.22 Transfer a pool to RAMC or the joint venture

#### A2.22.1 Intent

**Business objective.** Takes a pool of assets to RAMC with committee approval, and records the transfer.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.22.2 Description

**Functional overview.** Takes a pool of assets to RAMC with committee approval, and records the transfer.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Sale officer | Opens the screen and transfer a pool to RAMC or the joint venture | Checks the role, the capability area and the scope |
| 2 | Sale officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Partner portal, AMIS

**Prerequisites.** FEAT-APD-01

#### A2.22.3 Business rules and structure

##### A2.22.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-022-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-DIS-59 | Instruct the RAMC or joint venture transfer on the portal, when transfer_price from the template version | Moves to RAMC_TRANSFER_PENDING |
| BR-S5-022 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.22.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| asset.case_id | The recovery_case this record belongs to | uuid | No | None | No |
| asset.collateral_id | The collateral this record belongs to | uuid | No | None | No |
| asset.asset_ref | Asset reference | varchar(20) | Yes | None | No |
| asset.asset_code | Asset code | varchar(20) | No | None | No |
| asset.asset_type | Detached house, townhouse, condominium, land, vehicle | varchar(20) | Yes | LOV-ASSET-TYPE | No |
| asset.transfer_in_type | Auction purchase, deed in lieu, repossession | varchar(20) | Yes | LOV-TRANSFER-IN | No |
| asset.from_segment | Segment the asset came from | varchar(20) | No | LOV-SEGMENT | No |
| asset.transfer_in_date | Date ownership passed to the bank | date | Yes | None | No |

##### A2.22.3.3 Roles and permissions

| Role | Use |
|---|---|
| Sale officer | Primary |
| Head of NPA, RAMC user | Also uses |

#### A2.22.4 Acceptance criteria

##### A2.22.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-022-01 | Transfer a pool to RAMC or the joint venture | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.22.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.22.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-022-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-022-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.22.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.23 Arrange a customer buy-back

#### A2.23.1 Intent

**Business objective.** Opens the buy-back where the former owner repurchases, with the approval the limit requires.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.23.2 Description

**Functional overview.** Opens the buy-back where the former owner repurchases, with the approval the limit requires.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Sale officer | Opens the screen and arrange a customer buy-back | Checks the role, the capability area and the scope |
| 2 | Sale officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** AMIS, ALS and GL

**Prerequisites.** FEAT-AST-10

#### A2.23.3 Business rules and structure

##### A2.23.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-023-1 | Floor price below the approver's limit | MSG-S5-001 The floor is {pct} of fair market value, below the {limit} this level may approve. |
| R-DIS-66 | Pause the disposal, stop contact where required and route to the deviation owner, when deviation_open in (X1, X2, X3, X4, X5, X7) | Moves to DISPOSAL_PAUSED_DEVIATION |
| BR-S5-023 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.23.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| asset.case_id | The recovery_case this record belongs to | uuid | No | None | No |
| asset.collateral_id | The collateral this record belongs to | uuid | No | None | No |
| asset.asset_ref | Asset reference | varchar(20) | Yes | None | No |
| asset.asset_code | Asset code | varchar(20) | No | None | No |
| asset.asset_type | Detached house, townhouse, condominium, land, vehicle | varchar(20) | Yes | LOV-ASSET-TYPE | No |
| asset.transfer_in_type | Auction purchase, deed in lieu, repossession | varchar(20) | Yes | LOV-TRANSFER-IN | No |
| asset.from_segment | Segment the asset came from | varchar(20) | No | LOV-SEGMENT | No |
| asset.transfer_in_date | Date ownership passed to the bank | date | Yes | None | No |

##### A2.23.3.3 Roles and permissions

| Role | Use |
|---|---|
| Sale officer | Primary |
| Head of NPA, Customer (borrower) | Also uses |

#### A2.23.4 Acceptance criteria

##### A2.23.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-023-01 | Arrange a customer buy-back | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.23.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.23.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-023-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-023-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.23.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.24 Rent a held asset to a third party

#### A2.24.1 Intent

**Business objective.** Records the rental, the debit and the arrears follow-up while the asset is held.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.24.2 Description

**Functional overview.** Records the rental, the debit and the arrears follow-up while the asset is held.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Sale officer | Opens the screen and rent a held asset to a third party | Checks the role, the capability area and the scope |
| 2 | Sale officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** AMIS, ATS

**Prerequisites.** FEAT-AST-05

#### A2.24.3 Business rules and structure

##### A2.24.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-024-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-DIS-25 | Set the rental terms and the auto-debit, and hold the asset as rented, when route = rental | Moves to RENTAL_ACTIVE |
| BR-S5-024 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.24.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| asset.case_id | The recovery_case this record belongs to | uuid | No | None | No |
| asset.collateral_id | The collateral this record belongs to | uuid | No | None | No |
| asset.asset_ref | Asset reference | varchar(20) | Yes | None | No |
| asset.asset_code | Asset code | varchar(20) | No | None | No |
| asset.asset_type | Detached house, townhouse, condominium, land, vehicle | varchar(20) | Yes | LOV-ASSET-TYPE | No |
| asset.transfer_in_type | Auction purchase, deed in lieu, repossession | varchar(20) | Yes | LOV-TRANSFER-IN | No |
| asset.from_segment | Segment the asset came from | varchar(20) | No | LOV-SEGMENT | No |
| asset.transfer_in_date | Date ownership passed to the bank | date | Yes | None | No |

##### A2.24.3.3 Roles and permissions

| Role | Use |
|---|---|
| Sale officer | Primary |
| NPA and asset manager | Also uses |

#### A2.24.4 Acceptance criteria

##### A2.24.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-024-01 | Rent a held asset to a third party | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.24.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.24.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-024-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-024-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.24.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.25 Sell through a broker

#### A2.25.1 Intent

**Business objective.** Opens the broker route with its fee and terms, and tracks it to the sale.

**Problem.** The NPA sales cycle is 1,486 days; listings and floor prices are checked by hand.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| NPA sales cycle | 1,095 days | Decision log and Workbench records | Monthly |

#### A2.25.2 Description

**Functional overview.** Opens the broker route with its fee and terms, and tracks it to the sale.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Sale officer | Opens the screen and sell through a broker | Checks the role, the capability area and the scope |
| 2 | Sale officer | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Partner portal

**Prerequisites.** FEAT-AST-10

#### A2.25.3 Business rules and structure

##### A2.25.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S5-025-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| R-DIS-24 | Agree the buy-back terms at the template price, when route = buy_back and second_signature given | Moves to ROUTE_APPROVED_BUYBACK |
| R-DIS-25 | Set the rental terms and the auto-debit, and hold the asset as rented, when route = rental | Moves to RENTAL_ACTIVE |
| R-DIS-26 | Instruct the broker on the portal for a fixed term, when route = broker and asset_type in (commercial_property, land) | Moves to BROKER_INSTRUCTED |
| BR-S5-025 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.25.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| asset.case_id | The recovery_case this record belongs to | uuid | No | None | No |
| asset.collateral_id | The collateral this record belongs to | uuid | No | None | No |
| asset.asset_ref | Asset reference | varchar(20) | Yes | None | No |
| asset.asset_code | Asset code | varchar(20) | No | None | No |
| asset.asset_type | Detached house, townhouse, condominium, land, vehicle | varchar(20) | Yes | LOV-ASSET-TYPE | No |
| asset.transfer_in_type | Auction purchase, deed in lieu, repossession | varchar(20) | Yes | LOV-TRANSFER-IN | No |
| asset.from_segment | Segment the asset came from | varchar(20) | No | LOV-SEGMENT | No |
| asset.transfer_in_date | Date ownership passed to the bank | date | Yes | None | No |

##### A2.25.3.3 Roles and permissions

| Role | Use |
|---|---|
| Sale officer | Primary |
| Partner and agency manager | Also uses |

#### A2.25.4 Acceptance criteria

##### A2.25.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S5-025-01 | Sell through a broker | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.25.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.25.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S5-025-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S5-025-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.25.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|
| REQ-S5-001 | Every repossessed or surrendered asset is recorded with its source, date taken in, holding cost and provision step. | Must | E3 |
| REQ-S5-002 | The non performing asset stock balance has one named owner and is reported monthly. | Must | E3 |
| REQ-S5-003 | Holding age drives re-appraisal and the provision step by rule. | Must | E3 |
| REQ-S5-004 | A start price and a floor price are proposed for every asset, and the floor is approved by the named role. | Must | E3 |
| REQ-S5-005 | Listings are published to the bank's channel and the auction portal from one action. | Must | E3 |
| REQ-S5-006 | Auction rounds run down the price ladder to the floor, and a round with no bid re-lists by rule. | Must | E4 |
| REQ-S5-007 | A price below the floor needs a second signature. | Must | E4 |
| REQ-S5-008 | Title transfer is prepared and recorded for vehicles and for property. | Must | E4 |
| REQ-S5-009 | Proceeds are applied to the case and any residual routes to the next decision or closes the case. | Must | E4 |
| REQ-S5-010 | A transfer to the asset management company, a buy-back and a rental each follow a recorded approval. | Must | E4 |

## Screens

| Screen | What it is for | First in |
|---|---|---|
| SCR-21 Asset list | Assets held, with age, holding cost, value and sale status | E3 |
| SCR-22 Asset record | One asset: title, condition, photographs, valuations, costs, listing and sale history | E3 |
| SCR-23 Listing and price | List price, floor and the price ladder for an asset | E3 |
| SCR-24 Auction rounds | Auction rounds, bids and results for an asset | E4 |
| PRT-06 Transfer confirmation | Confirm a transfer of assets or accounts | E4 |

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
| Asset held for sale | ทรัพย์สินรอการขาย | An asset the bank holds after repossession, deed in lieu or auction purchase |
| Book value | มูลค่าตามบัญชี | The value of an asset held for sale in the bank's books |
| Floor price | ราคาขั้นต่ำ | The lowest price approved for a sale |
| Listing | รายการประกาศขาย | An asset offered for sale, with its prices and rounds |
| Repossession | การยึดรถ | Taking back a vehicle under a hire purchase contract |

## Appendix B. UI behavior

Components, field states, error display, confirmations and colors follow the Recovery Workbench Design System and Component Library. Message wording follows the Error and Message Standard.

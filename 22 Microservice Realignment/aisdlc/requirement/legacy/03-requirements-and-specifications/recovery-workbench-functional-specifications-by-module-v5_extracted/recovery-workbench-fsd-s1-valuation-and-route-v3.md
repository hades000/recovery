<!-- source: 03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v5.zip!Recovery Workbench FSD S1 Valuation and route v3.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `03 Requirements and specifications/Recovery Workbench Functional Specifications by Module v5.zip!Recovery Workbench FSD S1 Valuation and route v3.md`  
> **Converted from:** Markdown (extracted)

# Recovery Workbench S1 Valuation and route

Functional specification. SCB Collections and Recovery. Henka Group, 15 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

## Document control

| Attribute | Value |
|---|---|
| Document title | FSD S1 Valuation and route |
| Document ID | S1-RWB-FSD-v3 |
| Version | 3 |
| Status | In review |
| Classification | Confidential |
| Date | 15 November 2026 |
| FSD owner | Business analyst, S1 |
| Business owner | Business lead |
| Decision | D-RCV-35 (U1 to U5); ADR-010; open point DL43 |

| Module code | Module name | First in |
|---|---|---|
| S1 | Valuation and route | E4 |

**Feature scope.** D6 route decision with the COLLINS return by route read through ACE and the route agent. The SVAF appraisal is read through the ACE views; S1 loads no source data.

| Document | Type | Relationship |
|---|---|---|
| Recovery Workbench Business Requirements Program | BRD | Source |
| Recovery Workbench Technical Specification S1 Valuation and route | TSD | Pair |
| Recovery Workbench User Stories Epic 1 and Epic 2 | Backlog | Traceability |
| Recovery Workbench ACE DB Alignment Change Register v1 | Decision record | D-RCV-35, ADR-010, Appendix C field disposition |
| Recovery Workbench ACE Data Tier Map v1 | Frozen input | v_ace_valuation, v_ace_score, valuation_ext, removed valuation and score |
| Recovery Workbench ACE Source Views v1.sql | Frozen input | v_ace_valuation, v_ace_collateral_detail, v_ace_score, v_ace_account |

### Change note, version 3

| Version | Date | Change |
|---|---|---|
| 2 | 28 October 2026 | Baseline: valuation received from SVAF in a file load, score called from COLLINS |
| 3 | 15 November 2026 | Re-based on the ACE database under D-RCV-35 and ADR-010. The SVAF appraisal is read through `v_ace_valuation` once ACE has ingested it; acceptance and staleness live in `valuation_ext`, and `valuation` leaves the schema. Expected return by route is read through `v_ace_score`; payoff balances through `v_ace_account`. Links to an ACE record are business keys with no foreign key (`valuation_ext.valuation_key`). New section A1.5; the field catalog in A2.1 to A2.12 is re-pointed to the view and the extension table; features 01, 02, 05 and 06 reworded. FEAT-RDF-06 is removed and its place in the dependency list is taken by FEAT-RDF-01. No other section changed. |

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

**In scope.** D6 route decision with COLLINS return by route and the route agent.

**Out of scope.** Collections before day 90 on EFS; booking in the core bank, which the officer does; work owned by other modules, reached through their interfaces.

**Dependencies.** FEAT-AGT-01; FEAT-APD-02, FEAT-VAL-07; FEAT-APD-05; FEAT-CWC-11; FEAT-DRI-07; FEAT-RDF-01; FEAT-VAL-01; FEAT-VAL-02

**Constraints.** Built in the ACE service as part of the recovery module. Appraisal, score and account data is read from the ACE database through the read-only `recovery.v_ace_*` views and is never loaded or copied (D-RCV-35, ADR-010). A link to an ACE record is a business key with no foreign key. Every value a business person may change is a versioned data row (principle 1).

### A1.2 Feature overview

| Module | Feature code | Feature name | Kind | Description | First in | Section |
|---|---|---|---|---|---|---|
| S1 | FEAT-VAL-01 | Order an appraisal when the last one is stale | System | Checks `valuation_ext.age_days` against the limit and raises the order to SVAF with no person involved. | E4 | A2.1 |
| S1 | FEAT-VAL-02 | Receive the appraisal value from SVAF | System | Reads the value and date from `v_ace_valuation` once ACE has ingested the SVAF result, links it by `asset_key`, and records the valuer in `valuation_ext`. | E4 | A2.2 |
| S1 | FEAT-VAL-03 | Flag appraisal outliers against market and last value | System | Compares the new value to the market and the previous value and flags the gap for a person. | E4 | A2.3 |
| S1 | FEAT-VAL-04 | Accept the appraisal value | User | Lets the case owner accept the value, which fixes the band the route decision runs on. | E4 | A2.4 |
| S1 | FEAT-VAL-05 | Call COLLINS for return by route | System | Reads the expected return on each route from `v_ace_score`, which ACE ingests from COLLINS, and records the answer with its model version. | E4 | A2.5 |
| S1 | FEAT-VAL-06 | Calculate the payoff and settlement range | System | Works out the payoff from the balances read through `v_ace_account` and the settlement range from the rules, with the floor applied. | E4 | A2.6 |
| S1 | FEAT-VAL-07 | Score the routes and recommend one with reasons | System | Runs the route agent, which recommends a route and states the reasons and the alternatives. | E4 | A2.7 |
| S1 | FEAT-VAL-08 | Approve a route inside the limit | User | Lets the case owner approve the recommended route within their delegated limit. | E4 | A2.8 |
| S1 | FEAT-VAL-09 | Approve a route above the limit at committee | User | Takes the route to the credit committee when it is beyond the case owner's limit. | E4 | A2.9 |
| S1 | FEAT-VAL-10 | Hold the case and set a review date | User | Lets the owner hold a case where no route is right yet, with a date the hold is reviewed. | E4 | A2.10 |
| S1 | FEAT-VAL-11 | Reconsider the route after new information | User | Reopens the route decision when a value, a payment or a deviation changes the picture. | E4 | A2.11 |
| S1 | FEAT-VAL-12 | Start the route flow and set its timers | System | Opens the chosen route, creates its tasks and starts its clocks. | E4 | A2.12 |

### A1.3 Background

The route is chosen on officer judgment written up in an account plan.

### A1.4 Preconditions

- The user holds a Workbench role with the right in the capability area of the screen or action.
- The data products the module reads carry today's business date, or show their date as stale. Freshness comes from the ACE batch record, `v_ace_batch_status`.

### A1.5 Source data read path (D-RCV-35)

The module reads ACE through the `recovery.v_ace_*` views only. A direct read of a `public` table, a copy of a source record or a foreign key into ACE is a defect (Tier Map section 9).

| What S1 needs | View | Key the Workbench holds | Replaces (v2) |
|---|---|---|---|
| SVAF appraisal value, date, type and forced sale value | `v_ace_valuation` (Tier 2) | `valuation_ext.valuation_key` | `valuation` |
| Collateral title, location, insurance and lien rank | `v_ace_collateral_detail` (Tier 2) | `asset_key` | the CCMS collateral copy |
| Expected return by route and model version | `v_ace_score` (Tier 2) | `score_key` | `score` |
| Payoff balance, classification and days past due | `v_ace_account` | `account_key` | `loan_account` |
| Accepted value, stale flag and age | `valuation_ext` | `valuation_key` | `valuation.accepted`, `valuation.stale_flag` |
| Batch business date and completion | `v_ace_batch_status` (Tier 2) | none | `load_run`, the SVAF load report |

**Trigger.** The staleness check runs on EV-26 AceDataReady for the expected business date, or on the case timer where the appraisal has aged since entry. The value is read only after ACE reports the SVAF batch `COMPLETED` in `v_ace_batch_status`. No S1 job reads a file or loads a row.

## A2. Functional decomposition

### A2.1 Order an appraisal when the last one is stale

#### A2.1.1 Intent

**Business objective.** Checks `valuation_ext.age_days` against the limit and raises the order to SVAF with no person involved.

**Problem.** The route is chosen on officer judgment written up in an account plan.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Recommendations accepted | Baseline in the first three months | Decision log and Workbench records | Monthly |

#### A2.1.2 Description

**Functional overview.** Checks `valuation_ext.age_days` against the limit, takes the collateral from `v_ace_collateral_detail` by `asset_key`, and raises the order to SVAF with no person involved.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Order an appraisal when the last one is stale | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** SVAF; ACE database (`v_ace_valuation`, `v_ace_collateral_detail`)

**Prerequisites.** FEAT-RDF-01; RWB-E1-069

#### A2.1.3 Business rules and structure

##### A2.1.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S1-001-1 | Data product stale: the ACE batch for the business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-S1-001 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.1.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.1.4 Acceptance criteria

##### A2.1.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S1-001-01 | Order an appraisal when the last one is stale | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.1.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.1.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S1-001-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S1-001-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.1.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.2 Receive the appraisal value from SVAF

#### A2.2.1 Intent

**Business objective.** Reads the value and date from `v_ace_valuation` once ACE has ingested the SVAF result, links it to the collateral by `asset_key`, and records the valuer in `valuation_ext`.

**Problem.** The route is chosen on officer judgment written up in an account plan.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Recommendations accepted | Baseline in the first three months | Decision log and Workbench records | Monthly |

#### A2.2.2 Description

**Functional overview.** Reads the value and date from `v_ace_valuation` once ACE has ingested the SVAF result, links it to the collateral by `asset_key`, and records the valuer in `valuation_ext`.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Receive the appraisal value from SVAF | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ACE database (`v_ace_valuation`)

**Prerequisites.** FEAT-VAL-01

#### A2.2.3 Business rules and structure

##### A2.2.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S1-002-1 | Data product stale: the ACE batch for the business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-S1-002 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.2.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.2.4 Acceptance criteria

##### A2.2.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S1-002-01 | Receive the appraisal value from SVAF | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.2.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.2.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S1-002-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S1-002-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.2.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.3 Flag appraisal outliers against market and last value

#### A2.3.1 Intent

**Business objective.** Compares the new value to the market and the previous value and flags the gap for a person.

**Problem.** The route is chosen on officer judgment written up in an account plan.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Recommendations accepted | Baseline in the first three months | Decision log and Workbench records | Monthly |

#### A2.3.2 Description

**Functional overview.** Compares the new value to the market and the previous value and flags the gap for a person.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Flag appraisal outliers against market and last value | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ACE database (`v_ace_valuation`); Model gateway

**Prerequisites.** FEAT-VAL-02

#### A2.3.3 Business rules and structure

##### A2.3.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S1-003-1 | Data product stale: the ACE batch for the business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-S1-003 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.3.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.3.4 Acceptance criteria

##### A2.3.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S1-003-01 | Flag appraisal outliers against market and last value | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.3.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.3.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S1-003-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S1-003-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.3.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.4 Accept the appraisal value

#### A2.4.1 Intent

**Business objective.** Lets the case owner accept the value in `valuation_ext`, which fixes the band the route decision runs on.

**Problem.** The route is chosen on officer judgment written up in an account plan.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Recommendations accepted | Baseline in the first three months | Decision log and Workbench records | Monthly |

#### A2.4.2 Description

**Functional overview.** Shows the value from `v_ace_valuation` and writes `valuation_ext.accepted`, `accepted_at` and `accepted_by`, which fixes the band the route decision runs on.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and accept the appraisal value | Checks the role, the capability area and the scope |
| 2 | Case owner | Confirms the view value and accepts it | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes `valuation_ext.accepted`, `accepted_at` and `accepted_by`; writes the decision log entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-VAL-03

#### A2.4.3 Business rules and structure

##### A2.4.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S1-004-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S1-004 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.4.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| v_ace_valuation.valuation_key | ACE business key of the appraisal | varchar(255) | Yes | None | No |
| v_ace_valuation.asset_key | The collateral asset this appraisal values | varchar(255) | Yes | None | No |
| v_ace_valuation.appraisal_no | Appraisal number | varchar(20) | Yes | None | No |
| v_ace_valuation.appraisal_type | Market, official, forced sale, desktop, agent estimate | varchar(15) | Yes | LOV-APPRAISAL | No |
| v_ace_valuation.appraised_value | Appraised value, baht | numeric(18,2) | Yes | None | No |
| v_ace_valuation.forced_sale_value | Forced sale value, baht | numeric(18,2) | No | None | No |
| v_ace_valuation.appraisal_date | Appraisal date | date | Yes | None | No |
| v_ace_valuation.data_as_of | ACE business date of the appraisal | date | Yes | None | No |
| valuation_ext.accepted | True when the case owner has accepted the value | boolean | Yes | None | No |
| valuation_ext.accepted_at | When it was accepted | timestamptz | No | None | No |
| valuation_ext.accepted_by | Who accepted it | uuid | No | None | No |
| valuation_ext.valuer_partner_id | The valuer, as a Workbench partner record | uuid | No | None | No |
| valuation_ext.stale_flag | True when the appraisal is older than the policy limit | boolean | Yes | None | No |
| valuation_ext.age_days | Age in days at the ACE business date | integer | No | None | No |

##### A2.4.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Sale officer | Also uses |

#### A2.4.4 Acceptance criteria

##### A2.4.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S1-004-01 | Accept the appraisal value | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.4.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.4.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S1-004-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S1-004-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.4.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.5 Call COLLINS for return by route

#### A2.5.1 Intent

**Business objective.** Reads the expected return on each route from `v_ace_score`, which ACE ingests from COLLINS, and records the answer with its model version.

**Problem.** The route is chosen on officer judgment written up in an account plan.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Recommendations accepted | Baseline in the first three months | Decision log and Workbench records | Monthly |

#### A2.5.2 Description

**Functional overview.** Reads the expected return on each route from `v_ace_score`, which ACE ingests from COLLINS, and records the answer with its model version.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Call COLLINS for return by route | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ACE database (`v_ace_score`); Model gateway

**Prerequisites.** FEAT-AGT-01

#### A2.5.3 Business rules and structure

##### A2.5.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S1-005-1 | Data product stale: the ACE batch for the business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-S1-005 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.5.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.5.4 Acceptance criteria

##### A2.5.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S1-005-01 | Call COLLINS for return by route | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.5.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.5.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S1-005-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S1-005-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.5.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.6 Calculate the payoff and settlement range

#### A2.6.1 Intent

**Business objective.** Works out the payoff from the balances read through `v_ace_account` and the settlement range from the rules, with the floor applied.

**Problem.** The route is chosen on officer judgment written up in an account plan.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Recommendations accepted | Baseline in the first three months | Decision log and Workbench records | Monthly |

#### A2.6.2 Description

**Functional overview.** Works out the payoff from the balances read through `v_ace_account` and the settlement range from the rules, with the floor applied.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Calculate the payoff and settlement range | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** ACE database (`v_ace_account`); Rules component

**Prerequisites.** FEAT-DRI-07

#### A2.6.3 Business rules and structure

##### A2.6.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S1-006-1 | Data product stale: the ACE batch for the business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-S1-006 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.6.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.6.4 Acceptance criteria

##### A2.6.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S1-006-01 | Calculate the payoff and settlement range | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.6.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.6.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S1-006-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S1-006-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.6.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.7 Score the routes and recommend one with reasons

#### A2.7.1 Intent

**Business objective.** Runs the route agent, which recommends a route and states the reasons and the alternatives.

**Problem.** The route is chosen on officer judgment written up in an account plan.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Recommendations accepted | Baseline in the first three months | Decision log and Workbench records | Monthly |

#### A2.7.2 Description

**Functional overview.** Runs the route agent, which recommends a route and states the reasons and the alternatives.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Score the routes and recommend one with reasons | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Model gateway

**Prerequisites.** FEAT-VAL-05, FEAT-VAL-06

#### A2.7.3 Business rules and structure

##### A2.7.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S1-007-1 | Data product stale: the ACE batch for the business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-S1-007 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.7.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.7.4 Acceptance criteria

##### A2.7.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S1-007-01 | Score the routes and recommend one with reasons | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.7.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.7.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S1-007-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S1-007-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.7.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.8 Approve a route inside the limit

#### A2.8.1 Intent

**Business objective.** Lets the case owner approve the recommended route within their delegated limit.

**Problem.** The route is chosen on officer judgment written up in an account plan.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Recommendations accepted | Baseline in the first three months | Decision log and Workbench records | Monthly |

#### A2.8.2 Description

**Functional overview.** Lets the case owner approve the recommended route within their delegated limit.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and approve a route inside the limit | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-APD-02, FEAT-VAL-07

#### A2.8.3 Business rules and structure

##### A2.8.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S1-008-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S1-008 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.8.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| v_ace_valuation.valuation_key | ACE business key of the appraisal | varchar(255) | Yes | None | No |
| v_ace_valuation.asset_key | The collateral asset this appraisal values | varchar(255) | Yes | None | No |
| v_ace_valuation.appraisal_no | Appraisal number | varchar(20) | Yes | None | No |
| v_ace_valuation.appraisal_type | Market, official, forced sale, desktop, agent estimate | varchar(15) | Yes | LOV-APPRAISAL | No |
| v_ace_valuation.appraised_value | Appraised value, baht | numeric(18,2) | Yes | None | No |
| v_ace_valuation.forced_sale_value | Forced sale value, baht | numeric(18,2) | No | None | No |
| v_ace_valuation.appraisal_date | Appraisal date | date | Yes | None | No |
| v_ace_valuation.data_as_of | ACE business date of the appraisal | date | Yes | None | No |
| valuation_ext.accepted | True when the case owner has accepted the value | boolean | Yes | None | No |
| valuation_ext.accepted_at | When it was accepted | timestamptz | No | None | No |
| valuation_ext.accepted_by | Who accepted it | uuid | No | None | No |
| valuation_ext.valuer_partner_id | The valuer, as a Workbench partner record | uuid | No | None | No |
| valuation_ext.stale_flag | True when the appraisal is older than the policy limit | boolean | Yes | None | No |
| valuation_ext.age_days | Age in days at the ACE business date | integer | No | None | No |

##### A2.8.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Product head (Mortgage, HP, SSME) | Also uses |

#### A2.8.4 Acceptance criteria

##### A2.8.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S1-008-01 | Approve a route inside the limit | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.8.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.8.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S1-008-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S1-008-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.8.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.9 Approve a route above the limit at committee

#### A2.9.1 Intent

**Business objective.** Takes the route to the credit committee when it is beyond the case owner's limit.

**Problem.** The route is chosen on officer judgment written up in an account plan.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Recommendations accepted | Baseline in the first three months | Decision log and Workbench records | Monthly |

#### A2.9.2 Description

**Functional overview.** Takes the route to the credit committee when it is beyond the case owner's limit.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Credit approval committee member | Opens the screen and approve a route above the limit at committee | Checks the role, the capability area and the scope |
| 2 | Credit approval committee member | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-APD-05

#### A2.9.3 Business rules and structure

##### A2.9.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S1-009-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S1-009 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.9.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| v_ace_valuation.valuation_key | ACE business key of the appraisal | varchar(255) | Yes | None | No |
| v_ace_valuation.asset_key | The collateral asset this appraisal values | varchar(255) | Yes | None | No |
| v_ace_valuation.appraisal_no | Appraisal number | varchar(20) | Yes | None | No |
| v_ace_valuation.appraisal_type | Market, official, forced sale, desktop, agent estimate | varchar(15) | Yes | LOV-APPRAISAL | No |
| v_ace_valuation.appraised_value | Appraised value, baht | numeric(18,2) | Yes | None | No |
| v_ace_valuation.forced_sale_value | Forced sale value, baht | numeric(18,2) | No | None | No |
| v_ace_valuation.appraisal_date | Appraisal date | date | Yes | None | No |
| v_ace_valuation.data_as_of | ACE business date of the appraisal | date | Yes | None | No |
| valuation_ext.accepted | True when the case owner has accepted the value | boolean | Yes | None | No |
| valuation_ext.accepted_at | When it was accepted | timestamptz | No | None | No |
| valuation_ext.accepted_by | Who accepted it | uuid | No | None | No |
| valuation_ext.valuer_partner_id | The valuer, as a Workbench partner record | uuid | No | None | No |
| valuation_ext.stale_flag | True when the appraisal is older than the policy limit | boolean | Yes | None | No |
| valuation_ext.age_days | Age in days at the ACE business date | integer | No | None | No |

##### A2.9.3.3 Roles and permissions

| Role | Use |
|---|---|
| Credit approval committee member | Primary |
| Product head (Mortgage, HP, SSME) | Also uses |

#### A2.9.4 Acceptance criteria

##### A2.9.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S1-009-01 | Approve a route above the limit at committee | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.9.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.9.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S1-009-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S1-009-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.9.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.10 Hold the case and set a review date

#### A2.10.1 Intent

**Business objective.** Lets the owner hold a case where no route is right yet, with a date the hold is reviewed.

**Problem.** The route is chosen on officer judgment written up in an account plan.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Recommendations accepted | Baseline in the first three months | Decision log and Workbench records | Monthly |

#### A2.10.2 Description

**Functional overview.** Lets the owner hold a case where no route is right yet, with a date the hold is reviewed.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and hold the case and set a review date | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-CWC-11

#### A2.10.3 Business rules and structure

##### A2.10.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S1-010-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S1-010 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.10.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| v_ace_valuation.valuation_key | ACE business key of the appraisal | varchar(255) | Yes | None | No |
| v_ace_valuation.asset_key | The collateral asset this appraisal values | varchar(255) | Yes | None | No |
| v_ace_valuation.appraisal_no | Appraisal number | varchar(20) | Yes | None | No |
| v_ace_valuation.appraisal_type | Market, official, forced sale, desktop, agent estimate | varchar(15) | Yes | LOV-APPRAISAL | No |
| v_ace_valuation.appraised_value | Appraised value, baht | numeric(18,2) | Yes | None | No |
| v_ace_valuation.forced_sale_value | Forced sale value, baht | numeric(18,2) | No | None | No |
| v_ace_valuation.appraisal_date | Appraisal date | date | Yes | None | No |
| v_ace_valuation.data_as_of | ACE business date of the appraisal | date | Yes | None | No |
| valuation_ext.accepted | True when the case owner has accepted the value | boolean | Yes | None | No |
| valuation_ext.accepted_at | When it was accepted | timestamptz | No | None | No |
| valuation_ext.accepted_by | Who accepted it | uuid | No | None | No |
| valuation_ext.valuer_partner_id | The valuer, as a Workbench partner record | uuid | No | None | No |
| valuation_ext.stale_flag | True when the appraisal is older than the policy limit | boolean | Yes | None | No |
| valuation_ext.age_days | Age in days at the ACE business date | integer | No | None | No |

##### A2.10.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |
| Team manager | Also uses |

#### A2.10.4 Acceptance criteria

##### A2.10.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S1-010-01 | Hold the case and set a review date | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.10.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.10.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S1-010-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S1-010-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.10.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.11 Reconsider the route after new information

#### A2.11.1 Intent

**Business objective.** Reopens the route decision when a value, a payment or a deviation changes the picture.

**Problem.** The route is chosen on officer judgment written up in an account plan.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Recommendations accepted | Baseline in the first three months | Decision log and Workbench records | Monthly |

#### A2.11.2 Description

**Functional overview.** Reopens the route decision when a value, a payment or a deviation changes the picture.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | Case owner | Opens the screen and reconsider the route after new information | Checks the role, the capability area and the scope |
| 2 | Case owner | Enters or confirms the values | Validates the fields and applies the rules |
| 3 | System | Records the action | Writes the decision log or interaction ledger entry and moves the case |

**Integration points.** Workbench

**Prerequisites.** FEAT-VAL-07

#### A2.11.3 Business rules and structure

##### A2.11.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S1-011-1 | Required field empty | MSG-GEN-001 Enter {field}. |
| BR-S1-011 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.11.3.2 Field catalog

| Field | Meaning | Type | Required | List | Personal data |
|---|---|---|---|---|---|
| v_ace_valuation.valuation_key | ACE business key of the appraisal | varchar(255) | Yes | None | No |
| v_ace_valuation.asset_key | The collateral asset this appraisal values | varchar(255) | Yes | None | No |
| v_ace_valuation.appraisal_no | Appraisal number | varchar(20) | Yes | None | No |
| v_ace_valuation.appraisal_type | Market, official, forced sale, desktop, agent estimate | varchar(15) | Yes | LOV-APPRAISAL | No |
| v_ace_valuation.appraised_value | Appraised value, baht | numeric(18,2) | Yes | None | No |
| v_ace_valuation.forced_sale_value | Forced sale value, baht | numeric(18,2) | No | None | No |
| v_ace_valuation.appraisal_date | Appraisal date | date | Yes | None | No |
| v_ace_valuation.data_as_of | ACE business date of the appraisal | date | Yes | None | No |
| valuation_ext.accepted | True when the case owner has accepted the value | boolean | Yes | None | No |
| valuation_ext.accepted_at | When it was accepted | timestamptz | No | None | No |
| valuation_ext.accepted_by | Who accepted it | uuid | No | None | No |
| valuation_ext.valuer_partner_id | The valuer, as a Workbench partner record | uuid | No | None | No |
| valuation_ext.stale_flag | True when the appraisal is older than the policy limit | boolean | Yes | None | No |
| valuation_ext.age_days | Age in days at the ACE business date | integer | No | None | No |

##### A2.11.3.3 Roles and permissions

| Role | Use |
|---|---|
| Case owner | Primary |

#### A2.11.4 Acceptance criteria

##### A2.11.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S1-011-01 | Reconsider the route after new information | The data and rules it needs are in place | The user acts | The result is recorded with its rule version | Written one epic ahead |

##### A2.11.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.11.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S1-011-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S1-011-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.11.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

### A2.12 Start the route flow and set its timers

#### A2.12.1 Intent

**Business objective.** Opens the chosen route, creates its tasks and starts its clocks.

**Problem.** The route is chosen on officer judgment written up in an account plan.

| Metric | Target | Measurement | Review |
|---|---|---|---|
| Recommendations accepted | Baseline in the first three months | Decision log and Workbench records | Monthly |

#### A2.12.2 Description

**Functional overview.** Opens the chosen route, creates its tasks and starts its clocks.

| Step | Actor | Action | System response |
|---|---|---|---|
| 1 | System | Receives its trigger: the ACE batch-complete record (EV-26), an event or a timer | Reads the version of the rules in force |
| 2 | System | Start the route flow and set its timers | Applies the rules |
| 3 | System | Records the result | Writes the decision log entry; raises a task where a person is needed |

**Integration points.** Workbench, Quartz scheduler

**Prerequisites.** FEAT-VAL-08

#### A2.12.3 Business rules and structure

##### A2.12.3.1 Validation rules, business rules and constraints

| Rule ID | Rule | Message |
|---|---|---|
| VR-S1-012-1 | Data product stale: the ACE batch for the business date is not complete in `v_ace_batch_status` | MSG-P1-001 {product} is from {date}. Today's data is not yet complete. |
| BR-S1-012 | No value a business person may change is written in code; it is read from reference data with its version | None |

##### A2.12.3.3 Roles and permissions

| Role | Use |
|---|---|
| None; runs unattended | Primary |
| Case owner | Also uses |

#### A2.12.4 Acceptance criteria

##### A2.12.4.1 Main success flow

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-S1-012-01 | Start the route flow and set its timers | The data and rules it needs are in place | The trigger arrives | The result is recorded with its rule version | Written one epic ahead |

##### A2.12.4.2 Alternate flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| None | No alternate path | | | | |

##### A2.12.4.3 Exception flows

| AC ID | Scenario | Given | When | Then | Story |
|---|---|---|---|---|---|
| AC-EXC-S1-012-01 | Role without the right | A user without the right in the capability area | They try the action | Refused with MSG-P4-002; nothing changes | All |
| AC-EXC-S1-012-02 | Decision cannot be recorded | The decision log store is unavailable | The action is taken | Nothing changes; MSG-P7-003; incident raised | All |

##### A2.12.4.4 System background events

| AC ID | Event | Trigger | How often | What happens | Expected result | Why |
|---|---|---|---|---|---|---|
| None | No background event | | | | | |

---

## Requirements served

| Requirement | Text | Priority | Epic |
|---|---|---|---|
| REQ-S1-001 | An appraisal older than the policy limit triggers a new valuation order without a person asking for it. | Must | E4 |
| REQ-S1-002 | A valuation that is an outlier against the market and the last value is flagged before it is accepted. | Must | E4 |
| REQ-S1-003 | The expected return by route is available for every case at the route decision. | Must | E4 |
| REQ-S1-004 | The payoff amount and the settlement range are calculated by rule from current balances. | Must | E4 |
| REQ-S1-005 | The route recommendation names the option, the reasons, the confidence and the alternatives considered. | Must | E4 |
| REQ-S1-006 | The route decision is approved inside the delegation of authority, and above the limit it reaches the committee. | Must | E4 |
| REQ-S1-007 | A route decision starts the route flow and sets its timers in the same step. | Must | E4 |
| REQ-S1-008 | A change in the exposure band, the valuation or the classification after a route decision triggers a fresh decision. | Should | E4 |

## Screens

| Screen | What it is for | First in |
|---|---|---|
| SCR-13 Route decision | The route recommendation with the expected return of each route and the reasons | E4 |

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
| Score | คะแนนจากแบบจำลอง | A value COLLINS returns for an account or a case, such as a risk score or a price estimate |
| Return by route | ผลตอบแทนตามแนวทาง | The expected recovery after cost of each route for a case |
| Appraisal | การประเมินราคา | A valuation of collateral or an asset |
| Forced sale value | ราคาขายบังคับ | The value expected in a quick sale |

## Appendix B. UI behavior

Components, field states, error display, confirmations and colors follow the Recovery Workbench Design System and Component Library. Message wording follows the Error and Message Standard.

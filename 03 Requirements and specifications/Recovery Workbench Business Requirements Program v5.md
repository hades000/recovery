SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Recovery Workbench

Business requirements, program

SCB Collections and Recovery. Henka Group, 22 November 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench business requirements, program |
| Version | 5 |
| Date | 22 November 2026 |
| Prepared by | Henka Group |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Covers | All eight epics, November 2026 to June 2027 |
| Structure | ISO/IEC/IEEE 29148, until the SCB X requirement template is adopted (DL13) |
| Change | Version 4 re-bases the program requirements on the ACE database under D-RCV-35 (U1 to U5) and ADR-010, which supersedes ADR-005. Sections 1.1, 5 (intro and 5.1 to 5.3), 6.3, 6.5 (NFR-032), 7 and 9 change: section 5.1 states the four-tier read model and its counts, 5.2 is outbound only and 5.3 states the business-key link to ACE; the Workbench runs no inbound source load, reads source data only through the read-only recovery.v_ace_* views, and leaves Excel and SharePoint trackers to the Cutover plan. Requirement IDs are kept. REQ-RDF-005 and 006 are marked removed with their later home, and REQ-RDF-008 is re-worded to the reconciliation duty that stays in the Workbench, leaving 229 of 231 requirements live. DL43 is added as open. Other sections are unchanged. |
| Change (version 5) | Version 5 is the D-RCV-60 microservice realignment. Requirement IDs, requirement text, targets, decision dates and the numbering of sections 1 to 9 are unchanged. Section 7 restates the three constraints that D-RCV-60 supersedes: the platform shape, the schema per service and the workflow engine. In section 9 the four owner cells that named persons are replaced by the placeholder in section 12 (root rule 4). New section 10 gives the delivery model: 19 service epics, seven platform and five integration epics, four waves and the contract-first build order. New section 11 traces every business requirement to its service epic and its business epic. New section 12 lists the gaps and assumptions this version raises. Release dates are marked tentative (U7, DL48). |
| Change (update of 26 November 2026) | Version 5 is updated in place from its source documents. Section 2.1 adds the 27 business measures; section 6.2 adds NFR-079 and NFR-080, so section 6 holds 80 non-functional requirements; section 9 adds fifteen open decisions from the Decision Log v11; section 12 prints the register identifiers and adds section 12.3; new sections 13 to 16 carry the 32 regulatory obligations, the 42 audit findings, the 44 controls and the 14 reports. The ACE DB additions are named by DL43 and the one backlog story code is replaced by the Epic 1 requirement ID. Requirement IDs, requirement text and the numbering of sections 1 to 12 do not change. |

| Version | Date | Change | Author |
|---|---|---|---|
| 4 | 15 November 2026 | Version 4, as described in the Change row above | Henka Group |
| 5 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| 5 (update) | 26 November 2026 | Updated in place from the source documents, as in the Change row above | Henka Group |


# 1. Purpose and scope

This document sets the business requirements for the Recovery Workbench across the eight epics: what it must do, for whom, how well, and under which constraints. Each epic has its own document at development detail.

## 1.1 In scope

- Every recovery case from 90 days past due to close, for Mortgage, Hire Purchase and SSME.

- Decisions D6 to D9 with their sub-decisions, D5 once the restructure program is live, and deviations X1 to X7 after day 90.

- Partners, documents, the decision log and the interaction ledger.

- The recovery module of ACE, with data through ACE ingestion; the Workbench reads read-only ACE views (D-RCV-35).

## 1.2 Out of scope

| Out of scope | Where it is handled |
|---|---|
| Collections before day 90, decisions D1 to D4 | EFS and the ACE collection module |
| Dialer and messaging channels | Existing bank channels, reached through the ACE notification path |
| Core bank booking logic | ALS |
| COLLINS model development | Data and AI |
| Restructure affordability and plan calculation | The ACE restructure calculator |
| Partner systems | Each partner |
| Changes to bank policy | The policy owners |


# 2. Business outcomes

The Workbench is measured on the 2027 targets below. Each measure is read from the decision log per decision, with the baseline set in Epic 1.

| Measure | Today | 2027 target |
|---|---|---|
| Recovery rate on NPL | 66.3% (2026 to date) | 73% |
| Litigation turnaround | 21 days | 6 days |
| Deed in lieu turnaround | 26 days | 12 days |
| Restructure turnaround | 23 days | 5 days |
| Debt sale turnaround | No baseline | 45 days |
| Manual processes removed | Near zero | 80% of the selected list |
| Audit findings and fraud cases | 50 | 13 |
| NPA sales cycle | 1,486 days | 1,095 days |

## 2.1 Full measure set

The eight measures above are the program's headline targets. The Business Measures and Targets v2 workbook holds 27 measures; all of them are listed here with the baseline and the 2027 target as the workbook states them. A value of To set is copied as the workbook writes it: the baseline or the target has not been set (GAP-3260; ASM-5686). The definitions, formulas, sources and quarterly path stay in the workbook.

| ID | Group | Measure | Unit | Baseline | 2027 target | Direction | Owner |
|---|---|---|---|---|---|---|---|
| BM-01 | Outcome | Recovery rate on NPL | % | 66.3% | 73.0% | Up | Chief Debt Recovery Management Office |
| BM-02 | Outcome | Recovery rate after write-off | % | To set | To set | Up | Finance and CFO delegate |
| BM-03 | Outcome | Forward flow rate, bucket 3 | % | 25.7% | To set | Down | Product heads |
| BM-04 | Outcome | Cure rate, total | % | To set | To set | Up | Product heads |
| BM-05 | Outcome | Cure rate, restructuring | % | To set | To set | Up | Product heads |
| BM-06 | Outcome | Restructure performing | % | To set | To set | Up | Product heads |
| BM-07 | Outcome | First payment success after restructure | % | To set | To set | Up | Product heads |
| BM-08 | Outcome | Loss on settlement | % | To set | To set | Down | Product heads |
| BM-09 | Outcome | Loss on repossession | % | To set | To set | Down | Head of Asset Liquidity |
| BM-10 | Outcome | Loss on NPL sale | % | To set | To set | Down | Head of Asset Liquidity |
| BM-11 | Cost | Cost to collect | % | To set | To set | Down | Finance and CFO delegate |
| BM-12 | Cost | Agency cost efficiency | Ratio | To set | To set | Up | Partner and agency manager |
| BM-13 | Speed | Litigation turnaround | days | 21 | 6 | Down | Head of Litigation |
| BM-14 | Speed | Deed in lieu turnaround | days | 26 | 12 | Down | Head of NPA |
| BM-15 | Speed | Restructure turnaround | days | 23 | 5 | Down | Product heads |
| BM-16 | Speed | Debt sale turnaround | days | To set | 45 | Down | Head of Asset Liquidity |
| BM-17 | Speed | NPA sales cycle | days | 1,486 | 1,095 | Down | Head of NPA |
| BM-18 | Control | Audit findings and fraud cases | count | 50 | 13 | Down | Chief Debt Recovery Management Office |
| BM-19 | Control | Decisions within the delegation of authority | % | To set | 100.0% | Up | Risk |
| BM-20 | Control | Cases with a breached prescription date | count | To set | 0 | Down | Head of Litigation |
| BM-21 | Operations | Manual processes removed | % | 0.0% | 80.0% | Up | Business lead |
| BM-22 | Operations | Cases inside the service level | % | To set | To set | Up | Team managers |
| BM-23 | Operations | Cases per owner against the cap | cases | To set | To set | Within cap | Team managers |
| BM-24 | Operations | Recommendations accepted | % | To set | To set | Up | Center of excellence |
| BM-25 | Operations | Agent fallback rate | % | To set | To set | Down | Risk and model risk officer |
| BM-26 | Data | Loads on time and complete | % | To set | 99.0% | Up | Data steward and data product owner |
| BM-27 | Data | Reconciliation breaks | count | To set | 0 | Down | Data steward and data product owner |


# 3. Users

| Class | Roles |
|---|---|
| Bank user | 37 |
| Partner user | 7 |
| Customer party | 4 |
| Non-human actor | 6 |


Every role, its permissions and the release that gives it real users are in the Users, roles and permissions workbook.

# 4. Process architecture

19 L1 processes, 84 L2 sub-processes and 247 L3 processes. Processes 01 to 05 run in collections before day 90; the Workbench runs 06 to 19.

| L1 | Process | Decision | L2 | L3 | Process owner |
|---|---|---|---|---|---|
| 01 | Detect and act on signals | D1 | 2 | 6 | Collections, on EFS and ACE |
| 02 | Contact the customer | D2 | 6 | 15 | Collections, on EFS and ACE |
| 03 | Manage promises | D3 | 3 | 6 | Collections, on EFS and ACE |
| 04 | Escalate | D4 | 4 | 10 | Collections, on EFS and ACE |
| 05 | Restructure | D5 | 5 | 15 | Collections, on EFS and ACE |
| 06 | Take over and own the case | D6 entry | 1 | 3 | Recovery Strategy with Risk; the case owner for each case |
| 07 | Route, settle and claim | D6 | 5 | 17 | Recovery Strategy with Risk |
| 08 | Litigate and enforce | D7 | 4 | 16 | Head of Litigation; the enforcement owner after judgment |
| 09 | Dispose assets and sell debt | D8 | 7 | 28 | Head of NPA and Head of Auto Recovery; Head of Asset Liquidity for debt sale |
| 10 | Write off and recover after charge-off | D9 | 3 | 9 | Credit Administration with Risk |
| 11 | Handle customer care and deviations | X1 to X7 | 8 | 31 | Shared operations, with a named handler for each deviation |
| 12 | Manage partners | All | 5 | 13 | Partner and agency manager |
| 13 | Manage documents and correspondence | All | 4 | 14 | Shared operations |
| 14 | Set strategy, policy and decision rules | All | 3 | 12 | Center of excellence |
| 15 | Manage performance, data and AI | All | 8 | 20 | Center of excellence with Model Risk |
| 16 | Manage risk, control and compliance | All | 7 | 14 | Product heads for limits; center of excellence for QA; Shared operations for conduct |
| 17 | Run the decision center | D1 to D9 | 3 | 6 | Center of excellence |
| 18 | Plan capacity and allocate work | D2, D4 | 3 | 6 | Shared operations |
| 19 | Manage payments and reconciliation | D3, D5, D6 | 3 | 6 | Credit Administration |


# 5. Business requirements by module

231 business requirements across the platform and stage modules, of which 2 are removed by D-RCV-35 (229 live). Must is needed for the epic to release; Should is planned in the epic; Could is taken if capacity allows.

## 5.1 P1 Recovery data engine

P1 is the read-only data position for the whole program. ACE ingests every source and holds it; the Workbench reads it only through SELECT-only recovery.v_ace_* views and holds only Workbench-owned data: the case, its decisions, reference data and the extension tables (D-RCV-35, ADR-010).

The read model has four tiers. Tier 1 is 22 ACE tables that exist today; the recovery data in them is read through 16 Section A views, and the Workbench never alters them. Tier 2 is 14 ACE tables and 12 columns the ACE team adds under the ACE DB additions (DL43) for 80 source fields; the new tables are read through 14 Section B views and the new columns extend v_ace_account, v_ace_customer and v_ace_efs_action. Tier 3 is 4 Workbench extension tables keyed by ACE business keys. Tier 4 is 88 retained Workbench tables. The recovery schema is 92 tables; with the 30 views the dictionary holds 122 sys_objects and 1,366 sys_fields.

Two migrations carry the views, because a view cannot be created over a table that does not exist. Section A ships with the read-only ACE source views requirement of Epic 1 (BR-E1-020), the next free sequence after the V0001 baseline. Section B ships when the ACE DB additions (DL43) land, and until then the features that read the Tier 2 additions stay behind their flags. DL43 is open: the ACE team has yet to accept the scope of the ACE DB additions and its dates. No copy, load or tracker table remains in the recovery schema; source content is read through the views and the trackers are retired through the Cutover plan.

| ID | Requirement | Priority | Owner | Epic |
|---|---|---|---|---|
| REQ-RDF-001 | Recovery data is held in 14 data products, each with exactly one named system of record, ACE (ingested from the named source) or the Workbench, and one named owner. Source data in a data product is read from the ACE database through the read-only recovery.v_ace_* views and is not copied into the Workbench (D-RCV-35, ADR-010). | Must | Data steward and data product owner | E1 |
| REQ-RDF-002 | Account balance, arrears, payments and classification for every account at 90 or more days past due are read from ACE through v_ace_account and v_ace_payment, current to the latest completed ACE batch for the previous working day. | Must | Data steward and data product owner | E1 |
| REQ-RDF-003 | Collections contact history, promises and case status from EFS are read from ACE through v_ace_efs_action and v_ace_efs_assignment, so that the case carries what happened before day 90. | Must | Data steward and data product owner | E1 |
| REQ-RDF-004 | Collateral records and appraisal values are available on the case without a person looking them up in CCMS or SVAF. ACE ingests them under the ACE DB additions (DL43), and the Workbench reads them through v_ace_collateral, v_ace_collateral_detail and v_ace_valuation (DL43). The Workbench's acceptance of an appraisal is held in valuation_ext. | Must | Data steward and data product owner | E1 |
| REQ-RDF-005 | Removed by D-RCV-35 (U5). Excel and SharePoint trackers leave system scope. Later home: the tracker retirement procedure in the Cutover plan. Was: every recovery team's Excel file, SharePoint list and local file is listed with its owner, fields and update cycle, and each one has a decision to load it or record it as out of scope. | Removed | Program manager | E1 |
| REQ-RDF-006 | Removed by D-RCV-35 (U5). No tracker is loaded into the Workbench. Later home: the Cutover plan, which retires each local copy with the owner's confirmation and a read-only archive. Was: every file with a load decision is loaded, its row counts reconciled, and its local copy retired with the owner's confirmation and a read-only archive kept. | Removed | Data steward and data product owner | E1 |
| REQ-RDF-007 | The case list reconciles daily to the count of accounts at 90 or more days past due in v_ace_account, with no variance (DL25), and every business key on a Workbench table resolves to an ACE row. | Must | Data steward and data product owner | E1 |
| REQ-RDF-008 | Data quality checks on source data run in ACE ingestion (the ACE DB additions, DL43). The Workbench reports reconciliation breaks, referential completeness and its quality measures, each break with a reason visible to the data product owner. | Must | Data steward and data product owner | E1 |
| REQ-RDF-009 | Every data product carries a freshness stamp taken from the ACE batch record (v_ace_batch_status), and every decision records the freshness of the data it used. | Must | Center of excellence | E1 |
| REQ-RDF-010 | Access to each data product is controlled per role, and personal data is masked by role in line with PDPA. The recovery service identity holds SELECT on the recovery.v_ace_* views only, and the customer identification number leaves ACE masked. | Must | Compliance | E1 |
| REQ-RDF-011 | Every data product has a catalog entry stating its definition, owner, system of record, refresh cycle and retention, and, for source data, the ACE table and the view it is read through. | Must | Data steward and data product owner | E1 |
| REQ-RDF-012 | Baseline measures for cases by route, age and queue, realized recovery, time in stage and turnaround per route are published, with definitions agreed by the Tribe. | Must | Center of excellence | E1 |
| REQ-RDF-013 | Workbench recovery records carry a retention and archive rule by record class; ACE data is retained by ACE. | Should | Compliance | E1 |
| REQ-RDF-014 | Stage 2 data products for contracts, plans and treatments exist before the first treatment goes live. | Must | Data steward and data product owner | E2 |


## 5.2 P2 Integration

P2 is outbound only. It provides one adapter pattern for the WIN registered-mail notice file, the data lake and Power BI extract, the decision and outcome feed to COLLINS through the data lake, the debt buyer tape and the GL write-off event. It uses the ACE logging path to the SOC, and the transport used by the partner and document channels. It runs no inbound file feed, no file-load adapter and no inbound run record or sign-off: every inbound source lands in ACE through ACE ingestion and is read through the P1 views (D-RCV-35, U1; ADR-010).

| ID | Requirement | Priority | Owner | Epic |
|---|---|---|---|---|
| REQ-DRI-006 | No component calls a system of record directly. Source data lands in the ACE database through ACE ingestion and is read only through the recovery.v_ace_* views; data leaves through paths ACE already has (D-RCV-35, ADR-010). | Must | Solution architect | E1 |
| REQ-DRI-007 | The integration adapters log every outbound file, retry on a defined schedule, and place anything that fails after the retry limit in an exception queue with a task for a named owner. Inbound files belong to ACE ingestion (D-RCV-35). | Must | Platform administrator | E1 |
| REQ-DRI-008 | The Workbench runs no inbound batch or file load. Source data reaches it at the frequency ACE ingests it, and work that depends on a source starts when the ACE batch for that source is complete. Interfaces that need same-day data are named under DL06 before any is built. | Must | Solution architect | E1 |
| REQ-DRI-013 | Case hand-over from EFS is read from ACE through v_ace_efs_assignment once the ACE batch for EFS is complete, and plan status is read from the ACE common module, so a case is current the morning after it changes. | Must | Data steward and data product owner | E2 |


## 5.3 P3 Case and workflow

P3 covers the case and workflow layer, which the Workbench owns. A case links to an ACE customer by person_key and to each account by account_key, with asset_key, payment_code and contact_key used where the case refers to an asset, a payment or a contact point; no link is a foreign key into ACE. Workbench-only facts sit in the extension tables. The case layer never copies a source record and never writes to the ACE schema.

| ID | Requirement | Priority | Owner | Epic |
|---|---|---|---|---|
| REQ-CWC-001 | Every account at 90 or more days past due that is not excluded carries one recovery case, created by rule from the daily case list once the ACE batch for ALS is complete. | Must | Business lead | E1 |
| REQ-CWC-002 | Each case carries a case ID in the form RW-YYYY-NNNNNN, issued once, never reused, and printed on every letter and document. | Must | Business lead | E1 |
| REQ-CWC-003 | One case covers one customer and one product, with its accounts linked to it. The case links to the customer by the ACE person_key and to each account by the ACE account_key, with no foreign key into ACE (D-RCV-35, U4). | Must | Business lead | E1 |
| REQ-CWC-004 | Exclusion rules for deceased, fraud, bankruptcy, an active restructure plan and an open dispute are held as data and applied at creation. The inputs are read from the ACE views and from the Workbench extension tables keyed by person_key and account_key. | Must | Risk | E1 |
| REQ-CWC-005 | The case state model covers stage, status within stage, route and the deviation flags X1 to X7, and a case holds exactly one state at a time. | Must | Business lead | E1 |
| REQ-CWC-006 | Roles, teams, queues, queue membership and capacity are held as versioned reference data and change without a code release. | Must | Center of excellence | E1 |
| REQ-CWC-007 | Every new case is placed in a queue and assigned to a person by rule, and no case is allocated by hand as a matter of course. | Must | Team manager | E1 |
| REQ-CWC-008 | Allocation rules read product, region, exposure band, stage, route, deviation flag, customer segment and collateral type, apply first match, and always have a default row. | Must | Center of excellence | E1 |
| REQ-CWC-009 | Assignment rules support round robin, lowest load and a named owner for continuity, with a capacity cap and an overflow queue. | Must | Team manager | E1 |
| REQ-CWC-010 | Cases move between queues and roles by transfer rules on stage change, route decision, timer expiry, deviation raised or cleared, approval needed, document received, payment missed, and manual request with a reason code. | Must | Center of excellence | E1 |
| REQ-CWC-011 | Service levels per queue and status, warning thresholds and escalation targets are held as data, and a breach raises an event without moving the case. | Must | Team manager | E1 |
| REQ-CWC-012 | Prescription dates are set from the legal periods table at case creation and are visible at all times. | Must | Legal counsel | E1 |
| REQ-CWC-013 | A rule change goes from a validated template load to production with a version stamp and no code release, and rolls back to the previous version by one call. | Must | Center of excellence | E1 |
| REQ-CWC-014 | Rule loads are validated for schema, overlapping rows, unreachable rows, a missing default and a set of test cases before they take effect. | Must | Center of excellence | E1 |
| REQ-CWC-015 | Unassigned and over-capacity cases are rebalanced daily, and queue counts, ageing and service level breaches are reported. | Must | Team manager | E1 |
| REQ-CWC-016 | Every allocation, assignment, transfer and timer event is logged with the rule ID and the rule version that caused it. | Must | Center of excellence | E1 |
| REQ-CWC-017 | A queue accepts a write from an analytical model or an agent, carrying the case, the score, the priority and the reason, so that a daily decision reaches a queue the day it is made. | Must | Product owner | E2 |
| REQ-CWC-018 | A model or agent writing to a queue passes the same permission checks as a person, runs under a service identity, and its write is logged with the model or agent version. | Must | Security administrator | E2 |
| REQ-CWC-019 | The queue write interface ships behind a feature flag and is switched on when the first model is approved to use it. | Must | Platform administrator | E2 |
| REQ-CWC-020 | A queue holds work written by a model and work allocated by rule in the same queue, ordered by the same priority, so a person works one list. | Must | Team manager | E2 |
| REQ-CHO-001 | A case transferred from collections reaches the Workbench on the day of transfer, with its full contact and promise history read from ACE through the EFS views. Case transferred from EFS is a named same-day trigger under DL06. | Must | Business lead | E2 |
| REQ-CHO-002 | A change to a restructure plan status in ACE is visible on the case through the ACE common module. | Must | Data steward and data product owner | E2 |
| REQ-CHO-003 | Customer, product and account facts reach the case from ACE, which ingests them from SCBPDM and the core bank, read through v_ace_customer, v_ace_party_product and v_ace_account (DL20 as amended by D-RCV-35). | Must | Solution architect | E2 |
| REQ-CHO-004 | The hand-over point is one agreed number of days past due, used by every rule and every report. | Must | Risk with the ACE team | E2 |
| REQ-CHO-005 | The Workbench is the system of record for case state after hand-over. | Must | Solution architect | E2 |
| REQ-CHO-006 | A treatment record exists for every offer made to a customer, holding its type, terms, approval and outcome. | Must | Business lead | E2 |
| REQ-CHO-007 | Plan timers run from the treatment record, and a missed payment raises an event. | Must | Business lead | E2 |
| REQ-CHO-008 | A plan submitted for credit approval and terms booked in the core system are recorded on the case, and the booking is confirmed from the next business date's ACE account data in v_ace_account. | Must | Data steward and data product owner | E2 |
| REQ-CHO-009 | Payments received, read from ACE through v_ace_payment, are matched to the plan, the settlement or the fee they belong to by the ACE payment_code, and anything unmatched goes to an exception list. | Must | Autonomous Ops | E2 |
| REQ-CHO-010 | A duplicate case for the same customer and product, by ACE person_key and product, merges into the earlier case, carrying its documents and decision log. | Should | Case owner | E2 |
| REQ-WKM-001 | A case owner sees their own queue with ageing and service level state. | Must | Case owner | E2 |
| REQ-WKM-002 | A team manager sees every queue in their team, filters by status, product and ageing, and exports the view. | Must | Team manager | E2 |
| REQ-WKM-003 | A case is transferred or reassigned manually only with a reason code from the agreed list. | Must | Team manager | E2 |
| REQ-WKM-004 | A case that breaches its service level is visible to the named escalation role without the case moving. | Must | Team manager | E2 |
| REQ-WKM-005 | Timers, escalation state and the deviation flag are visible on the case record view. | Must | Case owner | E2 |
| REQ-WKM-006 | Queue counts, ageing and breaches are reported daily and reconcile to the case list. | Must | Team manager | E2 |
| REQ-WKM-007 | An owner who leaves, is absent beyond the threshold or breaches the caseload cap has their cases reallocated inside the team, keeping the state and the clocks. | Must | Team manager | E2 |
| REQ-WKM-008 | Queue and transfer history is visible on the case so that a reader sees where the case has been. | Must | Case owner | E2 |
| REQ-WKM-009 | A steering dashboard reports volume, ageing, route mix, turnaround and recovery against the baseline. | Must | Tribe lead | E2 |
| REQ-WKM-010 | A capacity view shows inflow by product, bucket and region against available capacity. | Could | Capacity and workforce planner | E7 |
| REQ-WKM-011 | Work allocated to a partner is visible in the same queue view as internal work. | Should | Partner and agency manager | E2 |
| REQ-WKM-012 | Every open case carries one next action: what has to happen, who owns it and the date it is due. | Must | Case owner | E2 |
| REQ-WKM-013 | The next action is produced from the rule that moved the case, taking the action, the owner of the next state and the timer that rule already carries. It is not entered by hand as a matter of course. | Must | Center of excellence | E2 |
| REQ-WKM-014 | The next action is visible to whoever picks the case up, on the case record and in every queue view, without opening the history. | Must | Case owner | E2 |
| REQ-WKM-015 | A next action that passes its due date raises the same escalation as any other service level breach, and the case does not move. | Must | Team manager | E2 |
| REQ-WKM-016 | A case with no next action is reported as an exception, because a case nobody owes anything on is the state this program exists to remove. | Must | Team manager | E2 |


## 5.4 P4 Access and administration

| ID | Requirement | Priority | Owner | Epic |
|---|---|---|---|---|
| REQ-ACA-001 | Every user signs on through Entra ID single sign-on with multi-factor authentication. | Must | Security administrator | E1 |
| REQ-ACA-002 | Roles are held as data, and a role change takes effect without a code release. | Must | Security administrator | E1 |
| REQ-ACA-003 | The role to permission matrix is held as data and is the only source of what a role may see and do. | Must | Security administrator | E1 |
| REQ-ACA-004 | The delegation of authority table is held as reference data and sets every approval limit. | Must | Risk with Credit | E1 |
| REQ-ACA-005 | Personal data is masked by role on every screen and in every agent call. | Must | Compliance | E1 |
| REQ-ACA-006 | Every read of the case store, the document store and the data lake copy is written to the access log. | Must | Compliance | E1 |
| REQ-ACA-007 | Access requested outside the authority matrix is refused and the refusal is recorded. | Must | Security administrator | E1 |
| REQ-ACA-008 | A break-glass path exists for an emergency, needs its own approval, and writes to the access log. | Must | Security administrator | E1 |
| REQ-ACA-009 | A user sees only the cases and queues their role and scope allow. | Must | Security administrator | E1 |
| REQ-ACA-010 | Agents run under service identities and are subject to the same role checks as people. | Must | Platform administrator | E1 |
| REQ-ACA-011 | Joiner, mover and leaver changes reach the Workbench so that access matches the current organization. | Must | Security administrator | E2 |
| REQ-ACA-012 | Partner users reach the Workbench only through the external gateway, with multi-factor authentication, scoped to their own cases. | Must | Security administrator | E2 |
| REQ-ACA-013 | Full administration screens for roles, permissions and delegation are available to the security administrator. | Should | Security administrator | E8 |


## 5.5 P5 Document hub

| ID | Requirement | Priority | Owner | Epic |
|---|---|---|---|---|
| REQ-DCM-001 | Every document is stored against its case with type, date, source and extracted fields. | Must | Legal counsel | E1 |
| REQ-DCM-002 | The Workbench document hub is the system of record for recovery documents. No other store holds the authoritative copy. | Must | IT lead | E1 |
| REQ-DCM-003 | Legal document types are held in a write-once container that cannot be altered or deleted. | Must | Legal counsel | E1 |
| REQ-DCM-004 | The document types and their key fields are agreed and signed before the extraction pipeline is built. | Must | Business lead with Legal | E1 |
| REQ-DCM-005 | Inbound documents are classified into one of the agreed types with a confidence score, and anything below the threshold goes to a review queue. | Must | Autonomous Ops | E1 |
| REQ-DCM-006 | Fields are extracted into the index for the agreed document types, in Thai and in English. | Must | Autonomous Ops | E1 |
| REQ-DCM-007 | A classified document attaches to its case without a person doing it. | Must | Autonomous Ops | E1 |
| REQ-DCM-008 | Documents are searchable by case ID, type and date from the case record view. | Must | Case owner | E1 |
| REQ-DCM-009 | Documents arrive from branches, the mailroom, partner file transfer and email through the same intake. | Must | Autonomous Ops | E1 |
| REQ-DCM-010 | Every document carries a retention class, and intake runs a virus scan before the document is stored. | Must | Compliance | E1 |
| REQ-DCM-011 | A document checklist per case type is held as reference data so that a missing document is visible. | Must | Center of excellence | E1 |
| REQ-DCM-012 | Contracts, credit applications and mortgage documents are generated from approved templates with case data and no re-keying. | Must | Legal counsel | E2 |
| REQ-DCM-013 | Field photographs and bills reach the same intake and index as scanned documents. | Should | Autonomous Ops | E2 |
| REQ-DCM-014 | New scope. Document storage is sized, provisioned and costed for the inbound volume and its growth, and the cost belongs to the program's running cost. | Must | Solution architect | E1 |
| REQ-DCM-015 | New scope. Documents are backed up on a stated schedule, and a restore is tested before the first production release and at each subsequent release. | Must | IT lead | E1 |
| REQ-DCM-016 | New scope. A legal hold applied to a case or a document stops deletion and expiry for as long as the hold is in place, overriding the retention class. | Must | Legal counsel with Compliance | E1 |
| REQ-DCM-017 | New scope. The hub answers an electronic discovery request by producing every document for a named population, with its metadata, its version history and the date each version was created. | Must | Legal counsel | E2 |
| REQ-DCM-018 | New scope. A document produced from the hub carries what a court needs to accept it: its origin, the date it entered the hub, whether it has been altered since, and who has read it. | Must | Legal counsel | E2 |
| REQ-DCM-019 | New scope. Records retention runs by class, and a document reaching the end of its retention period is disposed of or extended by a recorded decision, never silently. | Must | Compliance | E2 |
| REQ-DCM-020 | New scope. The hub carries a records management position signed by Compliance and Legal covering storage, backup, legal hold, discovery and disposal. | Must | Solution architect with Compliance | E1 |


## 5.6 P6 Communications

| ID | Requirement | Priority | Owner | Epic |
|---|---|---|---|---|
| REQ-OCC-001 | Notices are generated from templates approved by Legal, with merge fields from case data and no re-keying. | Must | Legal counsel | E1 |
| REQ-OCC-002 | Letter templates are versioned, and the Legal approval is recorded against the version. | Must | Legal counsel | E1 |
| REQ-OCC-003 | Letters are dispatched for print and post, and proof of delivery returns to the case. | Must | Autonomous Ops | E2 |
| REQ-OCC-004 | Messages are sent by SMS and LINE through the bank's channel platforms, with the result recorded on the case. | Must | Autonomous Ops | E2 |
| REQ-OCC-005 | Every outbound contact carries a conduct check result, and a contact that fails the check is held. | Must | Conduct and QA officer | E2 |
| REQ-OCC-006 | A customer who withdraws consent for a channel stops receiving on that channel, and statutory notices continue. | Must | Compliance | E2 |
| REQ-OCC-007 | The case record view shows account, arrears, owner, queue, stage, status, route, timers, contact history, promises, documents and decisions on one screen. | Must | Case owner | E1 |
| REQ-OCC-008 | The case record view carries a history timeline showing every state change, transfer, contact, document and decision in order. | Must | Case owner | E2 |
| REQ-OCC-009 | A customer signs an agreement electronically where Legal permits it, and by wet ink where Legal requires it. | Must | Legal counsel | E2 |
| REQ-OCC-010 | A new verified contact point updates the contact data and clears a lost contact deviation. | Must | Case owner | E2 |
| REQ-OCC-011 | Customer self-service for an offer, a signature, a payment and a dispute is available on the bank's digital channels. | Should | Business lead | E4 |


## 5.7 P7 Decision center and log

| ID | Requirement | Priority | Owner | Epic |
|---|---|---|---|---|
| REQ-DRI-001 | Every decision writes one record holding case and decision, the rule, model, agent and prompt versions, an inputs snapshot, the recommendation, the approval, the actions taken and the outcome. | Must | Center of excellence | E1 |
| REQ-DRI-002 | The decision log is append only. A record cannot be changed or deleted, and a correction is a new record naming the one it corrects. | Must | Compliance | E1 |
| REQ-DRI-003 | The decision log is hash chained, and the chain integrity is checked every day with a break reported to Compliance the same day. | Must | Compliance | E1 |
| REQ-DRI-004 | Records are written from Epic 1 for case creation, owner assignment, case transfer and document attachment. | Must | Center of excellence | E1 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written. | Must | Center of excellence | E1 |
| REQ-DRI-009 | The decision log is copied to the data lake copy daily for reporting, with row counts matched. | Must | Data steward and data product owner | E1 |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold, limit and name, versioned, changed without a code release. | Must | Center of excellence | E1 |
| REQ-DRI-011 | A reference data service holds every versioned table with its valid from and valid to dates, author and approver. | Must | Reference data administrator | E1 |
| REQ-DRI-012 | Audit can query the decision log for a population of cases and receive the decision history with inputs, versions, approver and final call. | Must | Internal audit | E2 |
| REQ-APD-001 | A decision that needs approval is routed to the approver named by the delegation of authority table for that decision, product and amount. | Must | Risk with Credit | E2 |
| REQ-APD-002 | An approver sees the recommendation, the reasons behind it, the inputs used and the limit that applies, on one screen. | Must | Business lead | E2 |
| REQ-APD-003 | An approver can accept, change, reject or return the item with a question, and each outcome is recorded. | Must | Business lead | E2 |
| REQ-APD-004 | A request above the approver's limit is refused and raised to the next approver in the matrix, with no silent approval. | Must | Risk | E2 |
| REQ-APD-005 | An override of a recommendation needs a coded reason, and the reason is reported monthly. | Must | Center of excellence | E2 |
| REQ-APD-006 | Demand and recall notices are approved through this path as the first use of approval routing. | Must | Legal counsel | E2 |
| REQ-APD-007 | An approval that is not answered inside its service level escalates to the named role. | Must | Team manager | E2 |
| REQ-APD-008 | A committee decision is recorded against the item with the members present and the decision taken. | Must | Business lead | E2 |
| REQ-APD-009 | The limit, the rule version and the approver are written to the decision log with every approval. | Must | Center of excellence | E2 |
| REQ-APD-010 | A change to the delegation of authority table is versioned, approved and dated, and open items keep the version they were decided under. | Must | Risk | E2 |
| REQ-APD-011 | Approval routing works with no person available in a role, by escalating rather than stalling. | Should | Team manager | E2 |
| REQ-ILG-001 | One ledger holds every interaction on a case, and no other record is the authoritative history of what happened with the customer. | Must | Case owner | E1 |
| REQ-ILG-002 | Every entry carries the case ID, the event, the timestamp, the actor and the source that produced it. | Must | Case owner | E1 |
| REQ-ILG-003 | Entries carry the channel, who or what was reached, and the outcome, where the interaction had one. | Must | Case owner | E1 |
| REQ-ILG-004 | An offer, a promise, a payment or a hand-over made during an interaction is recorded against that interaction. | Must | Case owner | E1 |
| REQ-ILG-005 | Every action the Workbench takes on a case writes to the ledger as it happens: case creation, allocation, transfer, escalation, document attachment and decisions taken. | Must | Center of excellence | E1 |
| REQ-ILG-006 | The ledger reads back in one ordered sequence, filterable by channel, actor and date range, through one interface. | Must | Case owner | E1 |
| REQ-ILG-007 | The same event arriving twice with the same key produces one entry, and the repeat is counted. | Must | Platform administrator | E1 |
| REQ-ILG-008 | A ledger write that fails raises an incident. An entry is never discarded, because a ledger with silent gaps is trusted and wrong. | Must | Platform administrator | E1 |
| REQ-ILG-009 | Contact outcomes from collections reach the ledger, so that contactability found before day 90 is not lost at hand-over. | Must | The data lead with the business lead | E2 |
| REQ-ILG-010 | Letters, messages and calls dispatched by the Workbench write their result to the ledger, including proof of delivery where it returns. | Must | Autonomous Ops | E2 |
| REQ-ILG-011 | A hand-over to or from a partner writes to the ledger, naming who held the case, who holds it now, and when. | Must | Partner and agency manager | E2 |
| REQ-ILG-012 | The case record view shows the ledger as an ordered timeline. | Must | Case owner | E2 |
| REQ-ILG-013 | Ledger entries carry their own retention class, set independently of the decision log. | Must | Compliance | E2 |
| REQ-ILG-014 | Personal data in the ledger is masked by role on the same rules as the case record. | Must | Compliance | E1 |


## 5.8 S1 Valuation and route

| ID | Requirement | Priority | Owner | Epic |
|---|---|---|---|---|
| REQ-S1-001 | An appraisal older than the policy limit triggers a new valuation order without a person asking for it. | Must | Sale officer | E4 |
| REQ-S1-002 | A valuation that is an outlier against the market and the last value is flagged before it is accepted. | Must | Sale officer | E4 |
| REQ-S1-003 | The expected return by route is available for every case at the route decision. | Must | Center of excellence | E4 |
| REQ-S1-004 | The payoff amount and the settlement range are calculated by rule from current balances. | Must | Center of excellence | E4 |
| REQ-S1-005 | The route recommendation names the option, the reasons, the confidence and the alternatives considered. | Must | Business lead | E4 |
| REQ-S1-006 | The route decision is approved inside the delegation of authority, and above the limit it reaches the committee. | Must | Credit approval committee | E4 |
| REQ-S1-007 | A route decision starts the route flow and sets its timers in the same step. | Must | Business lead | E4 |
| REQ-S1-008 | A change in the exposure band, the valuation or the classification after a route decision triggers a fresh decision. | Should | Case owner | E4 |


## 5.9 S2 TDR, settlement and deed in lieu

| ID | Requirement | Priority | Owner | Epic |
|---|---|---|---|---|
| REQ-S2-001 | A restructure proposed in the collections system reaches the restructuring officer with the case, and the case does not leave the Workbench. | Must | Restructuring officer | E3 |
| REQ-S2-002 | An offer to a customer carries a validity period, and expiry returns the case to the status it came from. | Must | Restructuring officer | E3 |
| REQ-S2-003 | A signed offer routes to operations for booking, and an unsigned or declined offer returns the case to its prior status. | Must | Restructuring officer | E3 |
| REQ-S2-004 | Settlement terms are negotiated inside a rule-set range, and anything outside the range needs approval. | Must | Product head | E3 |
| REQ-S2-005 | Deed in lieu readiness, including the encumbrance check and an early valuation, is established before negotiation starts. | Must | Sale officer | E3 |
| REQ-S2-006 | The credit application, contract and mortgage documents for a deed in lieu are generated from templates. | Must | Legal counsel | E3 |
| REQ-S2-007 | An asset accepted under a deed in lieu is unlocked as a non performing asset by rule, with exceptions summarized for the approver. | Must | NPA and asset manager | E3 |
| REQ-S2-008 | Booked terms, settled accounts and released collateral are posted to their systems of record without re-keying. | Must | Credit Administration | E3 |
| REQ-S2-009 | A broken plan raises an event and returns the case to a decision rather than leaving it in a plan state. | Must | Case owner | E3 |
| REQ-S2-010 | Buyback rental, auto-debit, receipts and arrears follow-up run without a person for a standard arrangement. | Should | NPA and asset manager | E3 |


## 5.10 S3 Guarantees and guarantors

| ID | Requirement | Priority | Owner | Epic |
|---|---|---|---|---|
| REQ-S3-001 | A guarantee claim is prepared from case data and submitted inside the guarantor's deadline. | Must | Guarantee officer | E4 |
| REQ-S3-002 | Claim status, payment and any shortfall are recorded on the case. | Must | Guarantee officer | E4 |
| REQ-S3-003 | A guarantee payment that clears the balance closes the case and records the subrogation position. | Must | Guarantee officer | E4 |
| REQ-S3-004 | Guarantor and co-borrower notices are generated by rule and sent on the same path as customer notices. | Must | Case owner | E4 |
| REQ-S3-005 | A guarantor who answers a demand enters the same treatment paths as a borrower. | Must | Case owner | E4 |
| REQ-S3-006 | A rejected or reduced claim raises a reason and routes the residual to the next decision. | Must | Guarantee officer | E4 |
| REQ-S3-007 | Claims are filtered for eligibility before submission so that ineligible claims are not filed. | Should | Guarantee officer | E4 |


## 5.11 S4 Litigation and enforcement

| ID | Requirement | Priority | Owner | Epic |
|---|---|---|---|---|
| REQ-S4-001 | Demand and recall notices are generated by rule, approved, dispatched, and their notice periods are timed. | Must | Legal counsel | E5 |
| REQ-S4-002 | A litigation pack is assembled and checked against the document checklist, and missing documents are requested. | Must | Litigation officer | E5 |
| REQ-S4-003 | The litigation officer verifies the pack against the defect list before filing is approved. | Must | Litigation officer | E5 |
| REQ-S4-004 | A law firm is selected from the panel by rule using panel performance, and instructed through the partner portal. | Must | Partner and agency manager | E5 |
| REQ-S4-005 | Court state, hearing dates, deadlines and fees are tracked on the case without a person reading an email. | Must | Litigation officer | E5 |
| REQ-S4-006 | Settlement before judgment, an appeal and fee payment each need approval inside the delegation. | Must | Head of Litigation | E5 |
| REQ-S4-007 | Enforcement after judgment has one named owner from judgment to the end of enforcement. | Must | Enforcement owner | E5 |
| REQ-S4-008 | A deferred enforcement step carries a coded reason and a review date. | Must | Enforcement owner | E5 |
| REQ-S4-009 | Prescription warnings force a litigation review ahead of every other open action on the case. | Must | Litigation officer | E5 |
| REQ-S4-010 | Proceeds from enforcement are matched to the case and posted. | Must | Credit Administration | E5 |


## 5.12 S5 Assets and auction

| ID | Requirement | Priority | Owner | Epic |
|---|---|---|---|---|
| REQ-S5-001 | Every repossessed or surrendered asset is recorded with its source, date taken in, holding cost and provision step. | Must | NPA and asset manager | E3 |
| REQ-S5-002 | The non performing asset stock balance has one named owner and is reported monthly. | Must | Head of NPA | E3 |
| REQ-S5-003 | Holding age drives re-appraisal and the provision step by rule. | Must | NPA and asset manager | E3 |
| REQ-S5-004 | A start price and a floor price are proposed for every asset, and the floor is approved by the named role. | Must | Head of NPA | E3 |
| REQ-S5-005 | Listings are published to the bank's channel and the auction portal from one action. | Must | Sale officer | E3 |
| REQ-S5-006 | Auction rounds run down the price ladder to the floor, and a round with no bid re-lists by rule. | Must | Sale officer | E4 |
| REQ-S5-007 | A price below the floor needs a second signature. | Must | Head of NPA | E4 |
| REQ-S5-008 | Title transfer is prepared and recorded for vehicles and for property. | Must | Sale officer | E4 |
| REQ-S5-009 | Proceeds are applied to the case and any residual routes to the next decision or closes the case. | Must | Credit Administration | E4 |
| REQ-S5-010 | A transfer to the asset management company, a buy-back and a rental each follow a recorded approval. | Must | Head of NPA | E4 |


## 5.13 S6 Debt sale

| ID | Requirement | Priority | Owner | Epic |
|---|---|---|---|---|
| REQ-S6-001 | Accounts eligible for sale are selected by rule against the policy cap. | Must | Debt sale officer | E5 |
| REQ-S6-002 | Lots are built with an estimated price, and the reserve price is approved before the lot is offered. | Must | Head of Asset Liquidity | E5 |
| REQ-S6-003 | The data room holds a masked data tape, and no unmasked personal data leaves the bank. | Must | Compliance | E5 |
| REQ-S6-004 | Buyers pass a know your customer, licensing and eligibility check before they bid. | Must | Debt sale officer | E6 |
| REQ-S6-005 | A buyer who fails the check is given a remediation window and is removed from the panel if it is not met. | Must | Head of Asset Liquidity | E6 |
| REQ-S6-006 | The award of a lot is approved and recorded with the price achieved against the reserve. | Must | Head of Asset Liquidity | E6 |
| REQ-S6-007 | An account awarded in a lot stops every other open action on its case the same day. | Must | Debt sale officer | E6 |
| REQ-S6-008 | Data transfer, derecognition and the general ledger posting follow the award without re-keying. | Must | Credit Administration | E6 |
| REQ-S6-009 | A put-back claim from a buyer is reviewed against the sale terms and either accepted or refused with a reason. | Must | Debt sale officer | E6 |


## 5.14 S7 Write-off and recovery

| ID | Requirement | Priority | Owner | Epic |
|---|---|---|---|---|
| REQ-S7-001 | Write-off eligibility and the tax criteria are tested by rule on a monthly scan of both tracks. | Must | Write-off team member | E6 |
| REQ-S7-002 | The committee pack is prepared from case and provision data with no manual assembly. | Must | Write-off team member | E6 |
| REQ-S7-003 | The committee decision to approve, reject or defer is recorded against each account. | Must | Write-off committee member | E6 |
| REQ-S7-004 | The write-off exception loop has one named owner and a time limit. | Must | Write-off committee member | E6 |
| REQ-S7-005 | Approved write-offs post to the core system and the general ledger, the provision is released, and completeness is published. | Must | Credit Administration | E6 |
| REQ-S7-006 | Post charge-off treatment is set by rule, including placement with an agency. | Must | Credit Administration | E6 |
| REQ-S7-007 | Recoveries after charge-off are matched to the account, with income and agency fees recorded. | Must | Credit Administration | E6 |
| REQ-S7-008 | A case closes after its retention period, and reopening a closed case needs a written rule, a reason and an approver. | Must | Compliance | E6 |


## 5.15 S8 Deviation handling

| ID | Requirement | Priority | Owner | Epic |
|---|---|---|---|---|
| REQ-DVH-001 | Deviations X1 to X7 are detected by rule from case data, call notes, documents and external flags. | Must | Center of excellence | E2 |
| REQ-DVH-002 | A deviation pauses the stage clock, keeps the prescription clock running, and does not replace the case state. | Must | Business lead | E2 |
| REQ-DVH-003 | Each deviation code routes to its named owner, and a code with no owner routes to the team manager and is recorded as unmapped. | Must | Center of excellence | E2 |
| REQ-DVH-004 | Contact stops apply automatically for a dispute or complaint, a vulnerable or hardship case, and a deceased customer. | Must | Compliance | E2 |
| REQ-DVH-005 | A resolved deviation returns the case to the state it paused in, or to the route decision where the outcome changes the route. | Must | Case owner | E2 |
| REQ-DVH-006 | A deviation flag is visible on the case record view and in every queue view. | Must | Case owner | E2 |
| REQ-DVH-007 | A complaint is matched to the contact that preceded it. | Must | Conduct and QA officer | E2 |
| REQ-DVH-008 | A death stops all contact, notifies the heirs and the estate, and starts the insurance claim path. | Must | Legal counsel | E3 |
| REQ-DVH-009 | A bankruptcy or external seizure stops direct collection and starts the claim deadline clock. | Must | Legal counsel | E2 |
| REQ-DVH-010 | A fraud flag refers the case to the fraud team and holds recovery action until it is confirmed or cleared. | Must | Fraud | E2 |
| REQ-DVH-011 | The full deviation flows with their approvers, contact stops and return points run end to end. | Must | Center of excellence | E7 |
| REQ-S8-001 | Each of X1 to X7 runs end to end with its own flow, approver, contact rules and return point. | Must | Center of excellence | E7 |
| REQ-S8-002 | A hardship or vulnerability case follows the contact limits set for it and reaches a hardship or relief decision. | Must | Hardship and vulnerability specialist | E7 |
| REQ-S8-003 | A complaint is resolved inside its service level and the case returns to the same decision with its timers resumed. | Must | Complaint officer | E7 |
| REQ-S8-004 | A lost contact case runs skip tracing and returns to a decision whether or not contact is restored. | Must | Case owner | E7 |
| REQ-S8-005 | A collateral event triggers an insurance claim and a re-appraisal before the next decision. | Must | NPA and asset manager | E7 |
| REQ-S8-006 | Override and deviation patterns are reviewed monthly by the center of excellence. | Must | Center of excellence | E7 |
| REQ-S8-007 | A data subject request holds automated processing on the case and routes to Compliance inside the statutory period. | Must | Compliance | E7 |


## 5.16 S9 Partner management

| ID | Requirement | Priority | Owner | Epic |
|---|---|---|---|---|
| REQ-S9-001 | Every partner type is managed on the same six points: selection, contract and fees, targets and incentives, data exchange, performance reviews, notice and exit. | Must | Partner and agency manager | E6 |
| REQ-S9-002 | Each partner type has one named owner. | Must | Partner and agency manager | E6 |
| REQ-S9-003 | Work is allocated to partners by measured return against a scorecard, not by a fixed share. | Must | Partner and agency manager | E6 |
| REQ-S9-004 | Fees are calculated from the contracted schedule and paid against recorded results. | Must | Partner and agency manager | E6 |
| REQ-S9-005 | A partner that misses its service level is chased once and then has the work recalled. | Must | Partner and agency manager | E7 |
| REQ-S9-006 | A partner panel exit, a declared conflict of interest, insolvency or an upheld conduct breach recalls every open case held by that partner. | Must | Partner and agency manager | E7 |
| REQ-S9-007 | Partner performance, conduct and complaint data are reported to the partner review forum. | Must | Partner and agency manager | E7 |
| REQ-S9-008 | Partners exchange data through the partner portal and the external gateway, and not by email. | Must | IT lead | E6 |
| REQ-S9-009 | Field work and its evidence reach the case through the field application. | Should | Partner and agency manager | E7 |


# 6. Non-functional requirements

80 non-functional requirements. NFR-079 and NFR-080 are added from the Non Functional Specification v4, where D-RCV-60 states the one-hop call rule (GAP-3258). Proposed targets apply until the bank sets a value. Open targets are held under DL11, and retention and protection targets under DL26.

## 6.1 Volume and capacity

| ID | Requirement | Target | Status | Owner |
|---|---|---|---|---|
| NFR-001 | The case store holds one case per customer and product for every account at 90 or more days past due across Mortgage, Hire Purchase and SSME. | About 23,600 open cases at go-live and 26,500 at the end of 2027, from 3,110 new accounts at 90 days past due a month. Confirmed under DL15 | Proposed from the volume forecast | Risk with the data product owner |
| NFR-002 | The system supports the peak number of staff users signed on at once. | About 370 staff online in the busiest hour, of 914 named users | Proposed from the volume forecast | Business lead |
| NFR-003 | The system supports the peak number of partner users signed on at once across 73 agencies, 11 to 12 law firms, 4 auction vendors and 35 buyers. | About 50 partner users online in the busiest hour, of about 320 named users | Proposed from the volume forecast | Partner and agency manager |
| NFR-004 | The document store holds the annual inbound document volume with its growth rate. | About 860,000 documents in 2027, rising with 15 percent inflow growth a year | Proposed from the volume forecast | Legal with Autonomous Ops |
| NFR-005 | The restructure path carries the monthly case volume reaching the Workbench. | About 3,000 restructure accounts a month reach the bank's restructure process today | Proposed | Solution architect |
| NFR-006 | The deed in lieu path carries its target monthly volume. | 1,000 cases a month in 2027, from 685 today | Proposed | Solution architect |
| NFR-007 | The decision log holds one record for every decision on every case for the full retention period without degrading query time. | About 36 GB for the decision log and the interaction ledger by the end of 2031; a single case history query under 2 seconds at that size | Proposed, DL11 | Compliance with the solution architect |
| NFR-069 | The document hub holds the full recovery document estate as a system of record, including every version and every held document, with storage sized for growth. | About 5.8 million documents and 2.8 TB by the end of 2031, with every version and held document | Proposed, DL11 | Solution architect with Compliance |
| NFR-070 | The interaction ledger holds every interaction on every open and closed case within its retention period, and reads a single case history inside the user wait. | One case history reads in under 2 seconds with the ledger at its 2031 size | Proposed, DL11 | Data lead with the solution architect |


## 6.2 Response time

| ID | Requirement | Target | Status | Owner |
|---|---|---|---|---|
| NFR-008 | A screen responds within its target under normal load. | Under 2 seconds | Proposed | Solution architect |
| NFR-009 | The case record view loads for a case with 50 documents. | Under 2 seconds | Proposed | Solution architect |
| NFR-010 | An agent returns an answer within its target, after which the rule result is used and the case still routes. | Under 60 seconds | Proposed | Solution architect |
| NFR-011 | A rule evaluation at a routing decision completes inside the user's wait. | Under 300 milliseconds per rule evaluation at the 95th percentile | Proposed, DL11 | Solution architect |
| NFR-012 | A search across cases and documents returns within its target. | Under 3 seconds for a search across cases; under 5 seconds across documents | Proposed, DL11 | Business lead |
| NFR-079 | A REST call between services completes inside its timeout, and no call chain is deeper than one hop from gateway-bff. | 2 seconds per REST call; one hop only; GET retried once with jitter; circuit breaker and bulkhead per downstream | Proposed, D-RCV-60 | Solution architect |
| NFR-080 | A composite screen is composed by gateway-bff from parallel one-hop calls to the owning services, and never by one service calling another for a screen. | One hop per call; about 1.05 seconds budgeted at the 95th percentile, about 1.2 seconds planned, against the 2 second target | Proposed, D-RCV-60 | Solution architect |


## 6.3 ACE ingestion and freshness

The Workbench runs no inbound load (D-RCV-35, U1). Work that depends on source data starts when ACE records the batch for that source and business date as complete in v_ace_batch_status: case creation and the case list on the ALS batch, hand-over on the EFS batch. A late batch delays the work and raises an alert; it never starts a Workbench load. NFR-016, NFR-017 and NFR-019 are Workbench document and scheduling jobs; they load no source data.

| ID | Requirement | Target | Status | Owner |
|---|---|---|---|---|
| NFR-013 | Under D-RCV-35 (U1 and U4) and ADR-010, the Workbench reads source data only through the recovery.v_ace_* views, and every case list and decision states the business date and load time of the ACE source batches behind it. | Case list available by 07:00 on the latest completed ACE batch | Proposed, DL43 | Solution architect |
| NFR-014 | Freshness is read from recovery.v_ace_batch_status, one row per source and business date; a missing, failed or late batch is visible on the case list and alerts the data steward. | Start of day, on the ACE business date | Proposed, DL43 | Solution architect |
| NFR-015 | The Workbench holds no load window: a late ACE batch delays the case list and raises an alert rather than starting a Workbench load, catch-up job or staging table. | End of day; in the Workbench the next morning. Same-day needs are named under DL06 | Proposed | Solution architect |
| NFR-016 | The document intake pipeline processes its throughput in the test environment. | 500 pages per hour | Proposed | Solution architect |
| NFR-017 | Document classification is correct on the labeled sample, and anything below the confidence threshold goes to a review queue. | 90 percent correct | Proposed | Solution architect |
| NFR-018 | The case list reconciles to the ACE account view daily. | No unexplained variance; tolerance per data product under DL25 | Proposed, DL25 | Solution architect |
| NFR-019 | The daily rebalancing job completes before the working day starts. | Complete by 07:00 | Proposed, DL11 | Team manager |


## 6.4 Availability and recovery

| ID | Requirement | Target | Status | Owner |
|---|---|---|---|---|
| NFR-020 | The Workbench is available during business hours. | 99.9 percent in business hours | Proposed | Solution architect |
| NFR-021 | Availability outside business hours, when batch, dispatch and partner exchange run. | 99.5 percent outside business hours, excluding the change window | Proposed, DL11 | IT lead |
| NFR-022 | Recovery point objective: the maximum data loss the business accepts. | The ACE recovery point objective | Open, DL11 | IT lead with Operational Risk |
| NFR-023 | Recovery time objective: the maximum time to restore service. | The ACE recovery time objective | Open, DL11 | IT lead with Operational Risk |
| NFR-024 | An agent or model outage falls back to the rule result, and the case still routes. | Fallback always on | Proposed | Solution architect |
| NFR-025 | A system of record outage queues the outbound action and retries on a schedule, and does not lose it. | Queue and retry | Proposed | Solution architect |
| NFR-026 | An interface failure after the retry limit moves the item to an exception queue with a task for a named owner. | Three retries per item, then the exception queue | Proposed, DL11 | Platform administrator |
| NFR-027 | A production release rolls back by redeploying the previous tag. | Rollback by previous tag | Proposed | Solution architect |
| NFR-071 | Documents in the hub are backed up on a stated schedule, and a restore is tested before the first production release and at each release after it. | Backup on the bank schedule; restore tested before the first production release and at each release | Open, DL27 | IT lead |


## 6.5 Retention

| ID | Requirement | Target | Status | Owner |
|---|---|---|---|---|
| NFR-028 | Every document type carries a retention class, and the class sets how long the document is kept. | Retention classes defined per type; periods not set | Open, DL26 | Compliance with Legal |
| NFR-029 | Legal documents are held in a write-once container and cannot be altered or deleted inside their retention period. | Write-once for legal types | Proposed | Solution architect |
| NFR-030 | The decision log is retained for the period the regulator and internal audit require. | Log retention is set by Compliance | Open, DL26 | Compliance |
| NFR-031 | Case records carry a retention and archive rule by record class, and a case closes after its retention period. | Not set | Open, DL26 | Compliance |
| NFR-032 | Under D-RCV-35 (U5), retired local files and Excel and SharePoint trackers are handled through the Cutover plan, which keeps each as a read-only archive at a recorded location. The Workbench loads and holds no tracker. | Archive location recorded per file in the Cutover plan | Proposed | Solution architect |
| NFR-072 | A legal hold stops deletion and expiry for the case or document it covers, for as long as it is in place, overriding the retention class. | Hold overrides retention | Proposed | Solution architect |
| NFR-073 | An electronic discovery request is answered with every document for a named population, its metadata, its version history and the date each version was created. | Not set as a response time | Open, DL26 | Legal counsel |
| NFR-074 | A document reaching the end of its retention period is disposed of or extended by a recorded decision, and is never removed silently. | Recorded decision on every disposal | Proposed | Solution architect |
| NFR-075 | Interaction ledger entries carry their own retention period, set independently of the decision log. | Not set | Open, DL26 | Compliance |


## 6.6 Auditability

| ID | Requirement | Target | Status | Owner |
|---|---|---|---|---|
| NFR-033 | Every decision is reproducible from the log, including the rule, model, agent and prompt versions and the inputs used. | Every decision reproducible | Proposed | Solution architect |
| NFR-034 | Every action carries the rule version applied and the approver who allowed it. | Every action | Proposed | Solution architect |
| NFR-035 | The decision log hash chain is checked daily, and a break is reported to Compliance the same day. | Daily check, same-day report | Proposed | Solution architect |
| NFR-036 | An audit or regulatory request is answered inside its deadline with the decision history and the supporting documents. | Inside the deadline set by the requester | Proposed | Solution architect |
| NFR-037 | Quality assurance reaches first-time-right on case packs and write-off returns. | 90 percent | Proposed | Solution architect |
| NFR-038 | Every outbound contact carries a conduct check result, and a contact without one is held. | Every contact | Proposed | Solution architect |
| NFR-076 | A document produced from the hub carries its origin, the date it entered the hub, whether it has been altered since, and who has read it, to the standard a court applies. | Every document produced | Proposed | Solution architect |
| NFR-077 | A failed write to the interaction ledger raises an incident, and no entry is discarded. | No silent gaps | Proposed | Solution architect |
| NFR-078 | A model or agent write to a queue is logged with the model or agent version, on the same terms as a decision taken by a person. | Every write | Proposed | Solution architect |


## 6.7 Data protection

| ID | Requirement | Target | Status | Owner |
|---|---|---|---|---|
| NFR-039 | Party identifiers are masked at rest in the case store, and on every screen and every agent call, by role. | Masked at rest and in use | Proposed | Solution architect |
| NFR-040 | Each screen and each agent receives only the personal data it needs. | Data minimization per screen and per agent | Proposed | Solution architect |
| NFR-041 | The debt sale data tape is masked before it reaches the data room. | Masked tape | Proposed | Solution architect |
| NFR-042 | Every read of the case store, the document store and the data lake copy is logged. | Every read | Proposed | Solution architect |
| NFR-043 | A data subject access, correction or erasure request is answered inside the statutory period. | Statutory period, Not set as a working service level | Open, DL26 | Compliance |
| NFR-044 | Consent state per channel is held and applied, and statutory notices continue when consent is withdrawn. | Applied on every send | Proposed | Solution architect |
| NFR-045 | No production data is used in the development environment, and the user acceptance environment uses masked copies. | Synthetic in development, masked in user acceptance | Proposed | Solution architect |


## 6.8 Data residency and classification

| ID | Requirement | Target | Status | Owner |
|---|---|---|---|---|
| NFR-046 | Workbench data stays in the bank's own cloud tenancy in the agreed region. | SCB Azure, Southeast Asia | Proposed | Solution architect |
| NFR-047 | Every data product and every document type carries a data classification, and the classification sets its handling. | Classification scheme to be applied | Open, DL26 | Compliance with Security |
| NFR-048 | The approved large language model endpoint is reached over a private endpoint inside the bank's tenancy. | Private endpoint | Proposed | Solution architect |


## 6.9 Security

| ID | Requirement | Target | Status | Owner |
|---|---|---|---|---|
| NFR-049 | Staff authenticate with single sign-on and multi-factor authentication. | Entra ID single sign-on with multi-factor | Proposed | Solution architect |
| NFR-050 | Partner accounts authenticate with multi-factor and are scoped to their own cases. | Multi-factor, scoped | Proposed | Solution architect |
| NFR-051 | Agents run under service identities and are subject to the same role checks as people. | Service identities | Proposed | Solution architect |
| NFR-052 | Secrets are held in the key store and never in code, configuration files or prompts. | No secrets in code or prompts | Proposed | Solution architect |
| NFR-053 | Data is encrypted at rest and in transit. | Encrypted | Proposed | Solution architect |
| NFR-054 | The build pipeline blocks a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency. | Pipeline checks pass | Proposed | Solution architect |
| NFR-055 | Agent outputs are schema checked against an allowed-action list with a confidence threshold, and fall back to rules when the check fails. | Schema check on every output | Proposed | Solution architect |
| NFR-056 | Penetration testing and a security review are completed before the first production release. | Before the first production release and before the partner portal opens to users outside the bank | Proposed, DL11 | SCB IT security with the IT lead |


## 6.10 Language

| ID | Requirement | Target | Status | Owner |
|---|---|---|---|---|
| NFR-057 | Document text is read and extracted in Thai and in English. | Thai and English | Proposed | Solution architect |
| NFR-058 | Customer-facing documents and messages are produced in the customer's language. | Thai by default; English where the customer has chosen English | Proposed, DL10 | Legal counsel with Compliance |
| NFR-059 | Screen labels, validation messages and error messages are available in Thai and in English. | Every screen, label and message in Thai and English | Proposed, DL10 | Business lead |


## 6.11 Accessibility and devices

| ID | Requirement | Target | Status | Owner |
|---|---|---|---|---|
| NFR-060 | Screens meet the bank's accessibility standard. | WCAG 2.1 level AA for every screen | Proposed, DL11 | Tech leads with the ACE team |
| NFR-061 | Screens work on the browsers and versions the bank supports. | The current and previous major versions of Microsoft Edge and Google Chrome | Proposed, DL11 | IT lead |
| NFR-062 | The field application captures evidence with no network connection and uploads when it reconnects. | Offline capture | Proposed | Solution architect |
| NFR-063 | Partner-facing screens work on the devices partners actually use. | Desktop browsers as in NFR-061 and tablets for field and auction partners | Proposed, DL11 | Partner and agency manager |


## 6.12 Observability

| ID | Requirement | Target | Status | Owner |
|---|---|---|---|---|
| NFR-064 | Logs, traces and metrics are produced across the workflow, the decision service and the agents. | Across all three | Proposed | Solution architect |
| NFR-065 | Business measures per decision are produced from the decision log and not from a separate count. | From the log | Proposed | Solution architect |
| NFR-066 | Agent acceptance, override rate, latency and cost are measured and reported. | Measured per agent | Proposed | Solution architect |
| NFR-067 | Every scheduled job has a run book, monitoring and an alert to the operations channel. | Every job | Proposed | Solution architect |
| NFR-068 | A failing interface, job or agent raises an alert to a named owner within its target. | Alert within 15 minutes to the named owner | Proposed, DL11 | Platform administrator |


# 7. Constraints

| Constraint | What it means |
|---|---|
| Built on ACE | The Workbench is a module of ACE: 19 services in one ACE platform, one ACE database and one front end, with shape given by D-RCV-60 and ADR-013 (GAP-1495; ASM-2605) |
| Modular monolith | Superseded by D-RCV-60 and ADR-014: the recovery module is split into 19 services, each with its own schema, login, topic and task queue in the ACE database, and the boundaries are checked at build time (GAP-1495; ASM-2606) |
| Programmatic workflow | Superseded by D-RCV-60 and ADR-016: case, stage and task state is still held in the owner's database and is still described in CMMN 1.1 terms, but a case is moved by a durable workflow, with one parent case workflow and one child workflow per stage, and a schedule per job (GAP-1495; ASM-2607) |
| Principle 1 | Every rule, limit, threshold, template, name, queue, role, timer and route is a versioned data row, changed through a validated load without a code release |
| Data through ACE ingestion | Source data lands in the ACE database through ACE ingestion, including sources ACE does not hold today. The recovery module reads it only through the read-only recovery.v_ace_* views, links to it by ACE business keys and holds no copy, load or staging table (D-RCV-35, ADR-010). No real-time feed today; same-day needs are named under DL06 |
| ACE team dependency | The ACE team owns every ACE table and column the views read, and adds 14 tables, 12 columns and 80 source fields under the ACE DB additions (DL43) by 21 November 2026 for the 30 November release (tentative) (DL43). Features that read the Tier 2 additions stay behind their feature flags until the additions land |
| Document hub | The Workbench is the system of record for recovery documents |
| Monthly releases | One production release at each month end, shared with the collection squad |


# 8. Release plan

| Epic | Release | Theme | What the business gets |
|---|---|---|---|
| E1 | 30 Nov 2026 (tentative) | Foundation 1 | One case list for every account at 90 days past due or more, reconciled to the core bank. Documents found by case. Decision log store. Read-only case record view |
| E2 | 31 Dec 2026 (tentative) | Foundation 2 | One owner and a timer on every case, full history on one screen, approval routing, litigation notices generated and approved, steering dashboard |
| E3 | 31 Jan 2027 (tentative) | Settle, deed in lieu, assets | Settlements and deeds in lieu end to end to booking. Asset record, floor price and listing on HOME.SCB |
| E4 | 28 Feb 2027 (tentative) | Route decision | The route recommended with reasons and approved within the delegation of authority for every new case. Guarantee and TCG claims. Auction rounds and RAMC transfer |
| E5 | 31 Mar 2027 (tentative) | Litigation | Litigation instructed and tracked end to end, law firms through the partner portal. Debt sale lot data and the buyer data room |
| E6 | 30 Apr 2027 (tentative) | Debt sale and write-off | Debt sale screens and award, write-off committee, partner panel, allocation and fees |
| E7 | 31 May 2027 (tentative) | Deviations and partners | Deviations X1 to X7 end to end. Partner scoring, conduct and the field app |
| E8 | 30 Jun 2027 (tentative) | Administration and hardening | Full administration, conduct checks, autonomy step-ups, regulatory returns, hardening |


# 9. Open decisions that change these requirements

DL43 is the new open decision. The others keep their v3 answers, with the wording changed where D-RCV-35 supersedes the COLLINS route or the read and write position. The update of 26 November 2026 adds the fifteen open decisions of the Decision Log v11 that change a business requirement and were carried only in the epic documents or not at all: DL01, DL02, DL03, DL09, DL14, DL19, DL21, DL24, DL25, DL28, DL29, DL30, DL31, DL39 and DL40 (GAP-3265; ASM-5687). Rows already in an epic document are copied from it; DL01, DL02 and DL14 are copied from the Decision Log, with its recommendation as the answer the build uses. The delivery and tooling decisions DL04, DL05, DL07, DL08 and DL32 to DL38 do not change a business requirement and stay in the Decision Log.

| Decision | Question | Answer the build uses until decided | Owner | Needed by |
|---|---|---|---|---|
| DL01 | Is access to the Workbench granted centrally or by the application owner? | B. SCB IT administers business applications this way today, and the Workbench build is the same under both options. | Not specified in the source documents (GAP-0117; ASM-0189) | 28 Oct |
| DL02 | Who owns the Workbench as an application? | A, with the ACE team as technical custodian. ACE holds the collection and recovery modules in one service. | Not specified in the source documents (GAP-0117; ASM-0189) | 28 Oct |
| DL03 | Who makes the architecture change that lets partners reach the Workbench from outside the bank, given a lead time of one to three months? | A or B, raised in November. Law firms are first needed at Epic 5, litigation, in March 2027. | Architecture lead with the architecture team | 29 Oct |
| DL06 | Which interfaces need real time data, and which take the daily batch? | Option A, daily batch through COLLINS, is superseded by D-RCV-35: ACE ingests all source data, so the Workbench runs no source batch load and reads ACE once its batch is complete. Option B for the named same-day triggers. ACE has no real time feed today. Name the same-day triggers now: case transferred from EFS, payment received, legal event. | Not specified in the source documents (GAP-1491; ASM-2608) | 30 Oct |
| DL09 | Who tests from the business, and when? | Business testers work with the squads two to three hours a day during the build, then a one-week UAT before each release. | Not specified in the source documents (GAP-1458; ASM-2559) | 31 Oct |
| DL10 | What is the Thai name for each field, label and message? | The business lead drafts per module one epic ahead; Legal and Compliance approve. | Business lead with Legal and Compliance | 5 Nov |
| DL11 | What is the value for each non-functional target, or the owner and date for it? | Use the ACE values where ACE has them; the solution architect proposes the rest; Risk agrees. | Solution architect with Risk | 5 Nov |
| DL12 | Which legacy systems are kept, and does any need enhancing? | No legacy enhancement, with a list of the systems kept and what the Workbench reads from each. The read and write part of option A is superseded by D-RCV-35: source data is read only, through the SELECT-only recovery.v_ace_* views, not a direct read of ACE or COLLINS. | Not specified in the source documents (GAP-1491; ASM-2608) | 7 Nov |
| DL13 | The SCB X consortium template for AI code generation arrives on 29 October. Are the Epic 1 and Epic 2 requirements rewritten to it before the build? | Remap the Epic 1 requirements by 4 November and use the template from Epic 2. TechX, SCB and Henka agree one template and keep it for every later epic. | Not specified in the source documents (GAP-1491; ASM-2608) | 30 Oct |
| DL14 | Are TDR, phone, FCR, OA and DIL built by the ACE team, and litigation, debt sale and NPA by the Workbench team? | A. One case model in CMMN 1.1 terms covers both teams, so the split is a team assignment and not a design change. | Not specified in the source documents (GAP-0117; ASM-0189) and the product owner | 6 Nov |
| DL15 | Are the inventory counts and the growth assumption the right base for sizing? | A: Mortgage 12,256, hire purchase 12,960 and SSME 2,903 accounts; 3,110 new accounts a month; 15 percent growth a year. | Data lead | 6 Nov |
| DL16 | Does a case enter the Workbench at 90 or 91 days past due? | 90 days past due. The target operating model has the case owner holding the case from day 90. | Business lead | 6 Nov |
| DL17 | Is a case one per customer per product, one per account, or one per customer? | One per customer per product, with the accounts linked. | Product owner with the solution architect | 6 Nov |
| DL18 | Which person holds each approval level, with the limit by decision, amount and product, and the substitute for each? | Load the regulation's levels and limits now; add names and substitutes when signed. | Risk with the product heads | 30 Nov |
| DL19 | Which document types and fields does the document hub classify and extract? | B where the bank has one; A until then. | Business lead with Legal | 6 Nov |
| DL20 | Where do customer facts come from? | The customer facts ACE holds, which ACE ingests from SCBPDM and the core bank; the Workbench reads them through v_ace_customer. Amended by D-RCV-35, which removes the COLLINS route. | Solution architect with Not specified in the source documents (GAP-1491; ASM-2608) | 30 Oct |
| DL21 | Which systems store the Workbench case identifier? | A for Epics 1 and 2. Each system added later is an interface change. | Solution architect with the IT lead | 6 Nov |
| DL22 | How long may a case stay in each state before it escalates? | Load the values as parameters; escalation runs from the day they are loaded. | Business lead | 13 Nov |
| DL23 | What is the most cases a person holds, and how is a queue ordered? | Load as parameters. | Product owner | 13 Nov |
| DL24 | Which rules does the rules component load in Epic 1? | Allocation, assignment and transfer only. The route decision goes live in a later epic. | Product owner | 30 Oct |
| DL25 | How large a difference between the case list and the ACE account view is accepted? | Zero; any difference holds the publish. | Data lead | 6 Nov |
| DL26 | How long is each data product and document type kept, and which fields are masked for which role? | Provide per data product and document type. | Compliance | 13 Nov |
| DL27 | How are storage, backup, legal hold and e-discovery provided for the document hub? | The ACE storage pattern with a write-once container and the bank backup service. | Solution architect with Compliance | 13 Nov |
| DL28 | Who owns the letter templates and the fields filled into them? | The document module owns templates and fields; Legal approves wording. | Product owner | 13 Nov |
| DL29 | Which EFS contact outcomes come into the interaction ledger, and how far back? | A named list of outcomes for the case's collection period only. named by the business lead. | Data lead with the business lead | 13 Nov |
| DL30 | Who builds SMS and LINE dispatch, EFS file automation, stage 2 and 3 extraction, and document generation? | B where a bank-wide service exists; A otherwise. | IT lead with the product owner | 13 Nov |
| DL31 | Who owns screen design for the Workbench? | The TechX designer under the product owner. using the ACE components. | Product owner | 6 Nov |
| DL39 | Which roles receive real users at each release? | Administration roles at Epic 1; business roles from the release that gives them a screen, starting with Epic 2. | Business lead | 20 Nov |
| DL40 | What are the Entra ID group names and the bank IAM entry for the Workbench roles? | One group per role per environment. | SCB IT security | 6 Nov |
| DL43 | Does the ACE team accept the scope of the ACE DB additions and its dates? The scope is 14 new ACE tables, 12 new columns and 80 source fields. | Open. The build assumes the scope is accepted: 14 new ACE tables, 12 new columns and 80 source fields. Dates to confirm, and the Tier 2 features stay behind their flags until the additions land. | ACE team lead | 21 Nov |

# 10. Delivery model

Under D-RCV-60 the program is delivered as 19 service epics, seven platform epics and five integration epics, and every story also carries its business epic EP01 to EP08 as a tag (U1, DL45). The eight business epics keep the releases in section 8. The requirement IDs in section 5, their text, their priorities, their business owners and their epic column do not change; what this section adds is which epic delivers each requirement, in which wave, and in what order the work can start.

## 10.1 Epic structure

| Epic group | Epics | Count | What the epic delivers |
|---|---|---|---|
| Platform | RWB-PLT-TPL, RWB-PLT-LIB, RWB-PLT-WF, RWB-PLT-DB, RWB-PLT-EVT, RWB-PLT-EDGE, RWB-PLT-OBS | 7 | Service template and repositories, shared libraries, the workflow platform, the ACE database schemas and logins, the event platform, the edge and gateway, and observability |
| Service | RWB-SVC-P1 to RWB-SVC-S9 | 19 | One epic per service, covering the contract, application, database, infrastructure, operations and integration work of that service |
| Integration | RWB-ITG-W1, RWB-ITG-W2, RWB-ITG-W3, RWB-ITG-W4, RWB-ITG-NFR | 5 | One integration harness per wave, and the non-functional work of section 6 |
| Business epic tag | EP01 to EP08 | 8 | The business release a requirement lands in; carried as a tag on every story, alongside the service epic |

The platform epics deliver first, as wave 0, because every service epic builds on the template, the libraries, the workflow platform, the schemas and logins, the event platform, the edge and the observability baseline. RWB-PLT-EVT carries the event platform; the shared topic that every service writes its decision record to is rwb.decision-record.v1, and the Temporal namespace is rwb-recovery.

## 10.2 The 19 service epics and their waves

Each service epic is one service in the ACE platform, with its own schema and login in the ACE database, and each is reusable or replaceable on its own. The service, schema and wave are the Ownership Map entries (Ownership Map, Services sheet), which follow the Architecture v5 service catalogue (R-PREC rank 1).

| Service epic | Module | Service | Schema | Wave | Business epics served |
|---|---|---|---|---|---|
| RWB-SVC-P1 | P1 | rwb-source-data | rwb_source_data | 1 | EP01 to EP02 |
| RWB-SVC-P2 | P2 | rwb-integration | rwb_integration | 1 | EP01 to EP02 |
| RWB-SVC-P3 | P3 | rwb-case | rwb_case | 1 | EP01, EP02, EP07 |
| RWB-SVC-P4 | P4 | rwb-access | rwb_access | 1 | EP01, EP02, EP08 |
| RWB-SVC-P5 | P5 | rwb-document | rwb_document | 1 | EP01 to EP02 |
| RWB-SVC-P6 | P6 | rwb-comms | rwb_comms | 1 | EP01, EP02, EP04 |
| RWB-SVC-P7 | P7 | rwb-decision | rwb_decision | 1 | EP01 to EP02 |
| RWB-SVC-P8 | P8 | rwb-payment | rwb_payment | 2 | EP02 to EP08 |
| RWB-SVC-P9 | P9 | rwb-reporting | rwb_reporting | 1 | EP01 to EP08 |
| RWB-SVC-P10 | P10 | rwb-agent | rwb_agent | 1 | EP01 to EP08 |
| RWB-SVC-S1 | S1 | rwb-valuation | rwb_valuation | 3 | EP04 |
| RWB-SVC-S2 | S2 | rwb-treatment | rwb_treatment | 2 | EP03 |
| RWB-SVC-S3 | S3 | rwb-guarantee | rwb_guarantee | 3 | EP04 |
| RWB-SVC-S4 | S4 | rwb-litigation | rwb_litigation | 3 | EP05 |
| RWB-SVC-S5 | S5 | rwb-asset | rwb_asset | 2 | EP03 to EP04 |
| RWB-SVC-S6 | S6 | rwb-debtsale | rwb_debtsale | 3 | EP05 to EP06 |
| RWB-SVC-S7 | S7 | rwb-writeoff | rwb_writeoff | 4 | EP06 |
| RWB-SVC-S8 | S8 | rwb-deviation | rwb_deviation | 2 | EP02, EP03, EP07 |
| RWB-SVC-S9 | S9 | rwb-partner | rwb_partner | 4 | EP06 to EP07 |

Owner in delivery terms is a suggestion only: every service epic is picked up by TechX (suggested; any team may pick up this story), and the database, infrastructure and operations work inside it by the ACE team, SCB IT infrastructure and the DevOps team as their suggested owners. No owner is a named person (U3, DL46).

## 10.3 Waves and releases

A wave groups the monthly releases that can be built together. The wave of a business epic is fixed: EP01 in wave 1, EP02 and EP03 in wave 2, EP04 and EP05 in wave 3, and EP06 to EP08 in wave 4, with platform and non-functional work in wave 0. A service is created in the wave shown in 10.2, so a service that a later wave needs first is created earlier rather than the requirement moving.

| Wave | Business epics in the wave | Service epics created in the wave | Release (tentative) |
|---|---|---|---|
| 0 | Platform and non-functional | The seven platform epics and RWB-ITG-NFR | Before EP01, November 2026 |
| 1 | EP01 | RWB-SVC-P1, P2, P3, P4, P5, P6, P7, P9, P10 | 30 Nov 2026 |
| 2 | EP02, EP03 | RWB-SVC-P8, S2, S5, S8 | 31 Dec 2026 and 31 Jan 2027 |
| 3 | EP04, EP05 | RWB-SVC-S1, S3, S4, S6 | 28 Feb 2027 and 31 Mar 2027 |
| 4 | EP06, EP07, EP08 | RWB-SVC-S7, S9 | 30 Apr 2027, 31 May 2027 and 30 Jun 2027 |
| per wave | All | RWB-ITG-W1 to RWB-ITG-W4, one harness per wave | The same wave dates, tentative |

The dates are the section 8 dates, unchanged and tentative (U7, DL48). The program finishes inside eight months of the first release.

## 10.4 Contract-first delivery

Every service publishes its contract before its build starts, and no service waits for another service to be built (ADR-020).

- The contract of a service is four things: its REST resources under /api/recovery/<short>/v1 behind gateway-bff, its topic rwb.<short>.events.v1 with its event names, its Temporal task queue rwb-<short> in the namespace rwb-recovery, and the call types it offers and accepts (REST, Kafka, Temporal, file).
- A contract story is Day 1 in every service epic and has no build dependency. Application stories build against the published contract and its fake, so a dependency on another service's contract never blocks a build.
- One hop from the gateway, a two second timeout, and no service reads another service's tables or schema: each service owns its own schema and login, and only rwb-source-data holds SELECT on the ACE views (ADR-014, ADR-020).
- Events carry identifiers and facts, never personal data; each service writes to its own outbox in the same transaction as its state change and deduplicates through its inbox (ADR-015).
- Rules are governed in rwb-decision and evaluated in the owning service; a decision record is written locally and sealed in the central ledger (ADR-017, ADR-022).
- A case is moved by one parent case workflow with one child workflow per stage, and a job is a Temporal Schedule or an event-started workflow in the owning service; no shared scheduler table remains (ADR-016).
- There is no data lake: reporting is a read model built from events into rwb-reporting, and the data lake interfaces and the daily copy are removed (ADR-018).
- Users reach the Workbench through gateway-bff, and partners through the partner gateway in the DMZ (ADR-019).

## 10.5 Ownership of the shared items

Where a requirement in section 5 needs a shared item, the owner is taken from the Ownership Map, not from the module the requirement happens to sit under.

| Shared item | Owner | Basis |
|---|---|---|
| Parameters and reference data | P3 rwb-case | Ownership Map, Parameters sheet; the default ruling of R-PREC |
| Case list API and screen | P3 rwb-case; the daily case list row is P1 | Ownership Map, Rulings sheet (the API, not the row table) |
| Rule package registry | P7 rwb-decision | The default ruling of R-PREC |
| Interaction ledger | P1 rwb-source-data; the case timeline and the interaction API stay with P3 | Ownership Map, Rulings sheet; DP-18 |
| Delegation of authority table | P4 rwb-access | Ownership Map, Rulings sheet |
| Feature flags | The platform library | The default ruling of R-PREC |
| Outbox, inbox and idempotency tables | The platform library, with one copy created in each service schema | Ownership Map, Rulings sheet; DP-09 |

## 10.6 What this changes in section 5

- No requirement ID, requirement text, priority, business owner or epic column in section 5 changes.
- The requirements in 5.7 that concern the interaction ledger are delivered by RWB-SVC-P1, and those that concern parameters and reference data by RWB-SVC-P3, because the Ownership Map gives those items to P1 and P3. They stay written where they are, under P7, so that the IDs remain stable (GAP-1496; ASM-2610; ASM-2612).
- The requirements in 5.7 that concern approvals are delivered by RWB-SVC-P7, and the delegation of authority table they read is P4's (GAP-1497; ASM-2611).
- Section 4 stays the business process view of 19 L1 processes; it is not a service list, and no service is mapped to a process here.


# 11. Business requirement trace: requirement to service epic to business epic

Every business requirement in section 5 appears exactly once in this table, with the service epic that delivers it, the service, the wave and the business epic whose release it lands in. The business epic is taken from the Epic column of the requirement's own table (E1 to E8), read as EP01 to EP08 (ASM-2614). The service epic is taken from the module the requirement sits under, corrected where the Ownership Map gives the item to another service (GAP-1492; GAP-1496; GAP-1497; ASM-2609; ASM-2610; ASM-2611; ASM-2612).

| Business requirements | Count | Service epic | Service | Wave | Business epic |
|---|---|---|---|---|---|
| REQ-RDF-001 to REQ-RDF-013 | 13 | RWB-SVC-P1 | rwb-source-data | 1 | EP01 |
| REQ-RDF-014 | 1 | RWB-SVC-P1 | rwb-source-data | 1 | EP02 |
| REQ-ILG-001 to REQ-ILG-008, REQ-ILG-014 | 9 | RWB-SVC-P1 | rwb-source-data | 1 | EP01 |
| REQ-ILG-009 to REQ-ILG-013 | 5 | RWB-SVC-P1 | rwb-source-data | 1 | EP02 |
| REQ-DRI-006 to REQ-DRI-008 | 3 | RWB-SVC-P2 | rwb-integration | 1 | EP01 |
| REQ-DRI-013 | 1 | RWB-SVC-P2 | rwb-integration | 1 | EP02 |
| REQ-CWC-001 to REQ-CWC-016 | 16 | RWB-SVC-P3 | rwb-case | 1 | EP01 |
| REQ-CWC-017 to REQ-CWC-020 | 4 | RWB-SVC-P3 | rwb-case | 1 | EP02 |
| REQ-CHO-001 to REQ-CHO-010 | 10 | RWB-SVC-P3 | rwb-case | 1 | EP02 |
| REQ-WKM-001 to REQ-WKM-009, REQ-WKM-011 to REQ-WKM-016 | 15 | RWB-SVC-P3 | rwb-case | 1 | EP02 |
| REQ-WKM-010 | 1 | RWB-SVC-P3 | rwb-case | 1 | EP07 |
| REQ-DRI-010, REQ-DRI-011 | 2 | RWB-SVC-P3 | rwb-case | 1 | EP01 |
| REQ-ACA-001 to REQ-ACA-010 | 10 | RWB-SVC-P4 | rwb-access | 1 | EP01 |
| REQ-ACA-011, REQ-ACA-012 | 2 | RWB-SVC-P4 | rwb-access | 1 | EP02 |
| REQ-ACA-013 | 1 | RWB-SVC-P4 | rwb-access | 1 | EP08 |
| REQ-DCM-001 to REQ-DCM-011, REQ-DCM-014 to REQ-DCM-016, REQ-DCM-020 | 15 | RWB-SVC-P5 | rwb-document | 1 | EP01 |
| REQ-DCM-012, REQ-DCM-013, REQ-DCM-017 to REQ-DCM-019 | 5 | RWB-SVC-P5 | rwb-document | 1 | EP02 |
| REQ-OCC-001, REQ-OCC-002, REQ-OCC-007 | 3 | RWB-SVC-P6 | rwb-comms | 1 | EP01 |
| REQ-OCC-003 to REQ-OCC-006, REQ-OCC-008 to REQ-OCC-010 | 7 | RWB-SVC-P6 | rwb-comms | 1 | EP02 |
| REQ-OCC-011 | 1 | RWB-SVC-P6 | rwb-comms | 1 | EP04 |
| REQ-DRI-001 to REQ-DRI-005, REQ-DRI-009 | 6 | RWB-SVC-P7 | rwb-decision | 1 | EP01 |
| REQ-DRI-012 | 1 | RWB-SVC-P7 | rwb-decision | 1 | EP02 |
| REQ-APD-001 to REQ-APD-011 | 11 | RWB-SVC-P7 | rwb-decision | 1 | EP02 |
| REQ-S1-001 to REQ-S1-008 | 8 | RWB-SVC-S1 | rwb-valuation | 3 | EP04 |
| REQ-S2-001 to REQ-S2-010 | 10 | RWB-SVC-S2 | rwb-treatment | 2 | EP03 |
| REQ-S3-001 to REQ-S3-007 | 7 | RWB-SVC-S3 | rwb-guarantee | 3 | EP04 |
| REQ-S4-001 to REQ-S4-010 | 10 | RWB-SVC-S4 | rwb-litigation | 3 | EP05 |
| REQ-S5-001 to REQ-S5-005 | 5 | RWB-SVC-S5 | rwb-asset | 2 | EP03 |
| REQ-S5-006 to REQ-S5-010 | 5 | RWB-SVC-S5 | rwb-asset | 2 | EP04 |
| REQ-S6-001 to REQ-S6-003 | 3 | RWB-SVC-S6 | rwb-debtsale | 3 | EP05 |
| REQ-S6-004 to REQ-S6-009 | 6 | RWB-SVC-S6 | rwb-debtsale | 3 | EP06 |
| REQ-S7-001 to REQ-S7-008 | 8 | RWB-SVC-S7 | rwb-writeoff | 4 | EP06 |
| REQ-DVH-001 to REQ-DVH-007, REQ-DVH-009, REQ-DVH-010 | 9 | RWB-SVC-S8 | rwb-deviation | 2 | EP02 |
| REQ-DVH-008 | 1 | RWB-SVC-S8 | rwb-deviation | 2 | EP03 |
| REQ-DVH-011 | 1 | RWB-SVC-S8 | rwb-deviation | 2 | EP07 |
| REQ-S8-001 to REQ-S8-007 | 7 | RWB-SVC-S8 | rwb-deviation | 2 | EP07 |
| REQ-S9-001 to REQ-S9-004, REQ-S9-008 | 5 | RWB-SVC-S9 | rwb-partner | 4 | EP06 |
| REQ-S9-005 to REQ-S9-007, REQ-S9-009 | 4 | RWB-SVC-S9 | rwb-partner | 4 | EP07 |
| Total | 231 |  |  |  |  |

The 80 non-functional requirements of section 6 are not business requirements and are delivered as non-functional work: RWB-ITG-NFR for the harness and the measured targets, and the platform epics RWB-PLT-OBS, RWB-PLT-EDGE, RWB-PLT-EVT, RWB-PLT-DB and RWB-PLT-WF for the mechanism each one relies on, in wave 0 and then in every wave that a target first applies to (ASM-2616).

Three modules have no requirement section of their own: P8 payment, P9 reporting and P10 agent. Their requirements are carried inside other sections: payment matching and posting in 5.3 and 5.12 to 5.14, the steering and management information duties in 5.3, 5.6 and 5.7, and the agent and model duties in 5.3, 5.5, 5.7 and 6.9. Their service epics therefore appear in 10.2 with no row of their own in this table (GAP-1498; ASM-2615).


# 12. Gaps and assumptions raised by this version

The rows below are the gaps and assumptions this version raises, under the identifiers the Gap Register v1 and the Assumptions Register v1 give them. Version 5 first printed the candidate identifiers CG-1 to CG-8 and ASM-1 to ASM-14; the update of 26 November 2026 replaces them with the register identifiers (GAP-3268).

## 12.1 Gaps

| ID | Type | What it affects |
|---|---|---|
| GAP-1491 | Conflict | Decision owners in section 9 are person names |
| GAP-1492 | Ambiguous | One requirement prefix, REQ-DRI, is used by two modules |
| GAP-1493 | Missing | No delivery model or service-epic mapping in version 4 |
| GAP-1494 | Missing | Business epic codes EP01 to EP08 are not defined in this document |
| GAP-1495 | Conflict | Three constraints in section 7 contradict the target architecture |
| GAP-1496 | Ambiguous | Interaction ledger requirements sit under P7 but the ledger is P1's |
| GAP-1497 | Ambiguous | Approval requirements sit under P7 but the authority table is P4's |
| GAP-1498 | Missing | No requirement section for P8 payment, P9 reporting or P10 agent |

## 12.2 Assumptions

| ID | Assumption | Why |
|---|---|---|
| ASM-2603 | The document stays in Draft in this run | Overlay D-RCV-60; no human approval in this run |
| ASM-2604 | EP01 to EP08 are Epic 1 to Epic 8 of section 8 | The wave map names the codes; section 8 names the epics |
| ASM-2605 | Built on ACE is read as 19 services inside ACE | D-RCV-60, ADR-013 |
| ASM-2606 | Modular monolith is read as one schema and login per service | D-RCV-60, ADR-014 |
| ASM-2607 | No Temporal is read as superseded by the workflow platform | D-RCV-60, ADR-016 |
| ASM-2608 | The four named owners are replaced by the section 12 placeholder | Root rule 4 |
| ASM-2609 | REQ-DRI-001 to 005 and 009 to 012 are P7; 006 to 008 and 013 are P2 | Section 5.2 and 5.7 |
| ASM-2610 | The REQ-ILG requirements are delivered by P1 | Ownership Map, Rulings sheet; DP-18 |
| ASM-2611 | REQ-APD is P7; the authority table it reads is P4 | Ownership Map, Rulings sheet |
| ASM-2612 | REQ-DRI-010 and 011 are delivered by P3 | Default ruling of R-PREC |
| ASM-2613 | Release dates carry (tentative) | U7, DL48 |
| ASM-2614 | The Epic column E1 to E8 is read as EP01 to EP08 | Section 5 tables |
| ASM-2615 | P8, P9 and P10 have no requirement section of their own | Section 5 has 16 sections |
| ASM-2616 | The 80 non-functional requirements are delivered as non-functional work | Section 6; RWB-ITG-NFR |

The document stays in Draft until the Product Owner and the business owner approve it. No approval is recorded in this version (ASM-2603).

## 12.3 Gaps and assumptions raised by the update of 26 November 2026

The update compares this document with its source documents. Rows marked resolved are closed in the Gap Register by this update; the others stay open.

| ID | Type | What it affects |
|---|---|---|
| GAP-3254 | Missing | No source maps the 32 regulatory obligations to business requirement IDs; section 13 traces them to processes, rules and controls only |
| GAP-3255 | Missing | 29 of the 32 regulatory obligations are not confirmed: 23 wait for Compliance and 6 for Legal |
| GAP-3256 | Missing | The 42 audit findings, 24 of them open, are not traced to business requirement IDs; section 14 traces them to controls and releases |
| GAP-3257 | Missing | The 44 controls were not in the BRD; section 15 now lists them (resolved by this update) |
| GAP-3258 | Outdated | The BRD carried 78 non-functional requirements while the Non Functional Specification v4 carries 80 (resolved by this update) |
| GAP-3259 | Missing | 19 of the 27 business measures were not in the BRD (resolved by section 2.1) |
| GAP-3260 | Missing | 20 of the 27 business measures have a baseline or a 2027 target of To set; 13 of them have both |
| GAP-3261 | Missing | The 14 reports of the reporting and MI requirements were not in the BRD (resolved by section 16) |
| GAP-3262 | Missing | L2 processes 18.1 Forecast inflow and workload and 18.2 Plan capacity and rosters have no business requirement |
| GAP-3263 | Missing | L2 process 14.3 Set fees, charges and waivers has no business requirement |
| GAP-3264 | Missing | L2 process 15.2 Test strategies (champion and challenger) has no program requirement; it is named only in the Epics 3 to 8 BRD scope for E8 |
| GAP-3265 | Missing | Fifteen open decisions that change a business requirement were not in section 9 (resolved by this update) |
| GAP-3266 | Conflict | The epic BRDs keyed their requirements on backlog story codes, which the backlog re-slices (resolved by this update) |
| GAP-3267 | Conflict | DL09 has a different owner in the Epic 1 BRD and the Epic 2 BRD |
| GAP-3268 | Conflict | Section 12 printed candidate identifiers, not the register identifiers (resolved by this update) |

| ID | Assumption | Why |
|---|---|---|
| ASM-5684 | The epic requirements are re-keyed BR-E1-nnn and BR-E2-nnn in the order of their section 3, and the old story codes are kept only in the run edit log | User instruction of 26 November 2026 |
| ASM-5685 | The regulatory, audit, control and report tables are copied unchanged from their workbooks; the owner service is the one the workbook names | Rule 8, copy values character for character |
| ASM-5686 | A measure value of To set is copied as written and means the value is not set | Business Measures and Targets v2 |
| ASM-5687 | A decision row already in an epic BRD is copied from it; DL01, DL02 and DL14 take the Decision Log recommendation as the answer the build uses | Decision Log v11; epic BRDs section 7 |
| ASM-5689 | The ACE DB additions are named by their decision DL43 and not by the ACE team's backlog story code | User instruction of 26 November 2026 |

# 13. Regulatory obligations

The Regulatory Requirements Map v3 lists 32 obligations from the law, BOT rules and bank policy. Each is copied below with the L2 process, the rule and the controls that satisfy it, its owner and the owner service. Compliance and Legal confirm the obligations in scope; the status column says which are confirmed (GAP-3255). No source maps an obligation to a business requirement ID (GAP-3254; ASM-5685).

| ID | Source | Obligation | Process | Rule | Controls | Owner | Status | Owner service |
|---|---|---|---|---|---|---|---|---|
| REG-01 | Debt Collection Act B.E. 2558 | Contact the debtor only at the permitted times and places, identify the collector, and do not disclose the debt to third parties | 11.1 Answer customer contacts | Contact rules; R-UNI-04 | CTL-16, CTL-17, CTL-39 | Compliance | To confirm with Compliance | P6 rwb-comms; P9 rwb-reporting |
| REG-02 | Debt Collection Act B.E. 2558 | No threats, insults, false or misleading statements, or unfair collection practices | 11.1 Answer customer contacts; 16.2 Control conduct | Conduct rules | CTL-39 | Compliance | To confirm with Compliance | P9 rwb-reporting |
| REG-03 | Debt Collection Act B.E. 2558 | Collection agencies acting for the bank are registered and the bank oversees their conduct | 12.1 Select and contract partners; 12.4 Govern partners | Panel rules | CTL-35, CTL-37 | Partner and agency manager | To confirm with Compliance | S9 rwb-partner |
| REG-04 | Debt Collection Act B.E. 2558 | Collection fees charged to the debtor are within the permitted rate and disclosed | 14.3 Set fees, charges and waivers; 13.2 Send letters and notices | Fee rules | CTL-14 | Compliance | To confirm with Compliance | P6 rwb-comms |
| REG-05 | BOT Responsible Lending | Offer debt restructuring to a debtor in difficulty before the account becomes non-performing and before legal action or debt sale | 7.2 Decide the route; 7.3 Negotiate settlement or deed in lieu | R-RES-01 to R-RES-09 | CTL-26, CTL-04 | Product heads | To confirm with Compliance | S2 rwb-treatment; P7 rwb-decision |
| REG-06 | BOT Responsible Lending | Inform the debtor before the debt is sold or transferred | 9.6 Sell debt; 13.2 Send letters and notices | Debt sale rules | CTL-14, CTL-15 | Head of Asset Liquidity | To confirm with Compliance | P6 rwb-comms |
| REG-07 | BOT Responsible Lending | Debtors in difficulty are contacted and offered help; no account is left without contact | 6.1 Take over the case at 90 days past due; 11.1 Answer customer contacts | Allocation rules | CTL-01, CTL-03 | Business lead | To confirm with Compliance | P3 rwb-case |
| REG-08 | BOT market conduct | Treat vulnerable customers fairly and apply the vulnerable customer treatment | 11.3 X2 Vulnerable customer or hardship | R-UNI-06 | CTL-16, CTL-39 | Hardship and vulnerability specialist | To confirm with Compliance | P6 rwb-comms; P9 rwb-reporting |
| REG-09 | BOT market conduct | Handle complaints within the set time and stop disputed recovery until resolved | 11.2 X1 Dispute or complaint | R-UNI-04, R-UNI-09 | CTL-16 | Complaint officer | To confirm with Compliance | P6 rwb-comms |
| REG-10 | BOT relief schemes | Apply relief scheme terms correctly, report scheme results accurately and claim compensation only for eligible debtors | 6.1 Take over the case at 90 days past due; 7.3 Negotiate settlement or deed in lieu; 15.1 Report performance | R-UNI-13 | CTL-23, CTL-25 | Product heads | To confirm with Compliance | S2 rwb-treatment |
| REG-11 | BOT asset classification and provisioning | Classify, stage and provision accounts correctly, with the right product type for restructured hire purchase | 15.8 Classify, stage and re-age accounts | R-UNI-22 | CTL-02, CTL-25 | Finance and CFO delegate | To confirm with Compliance | P1 rwb-source-data; S2 rwb-treatment |
| REG-12 | BOT asset classification and provisioning | Revalue collateral for Stage 3 accounts within the required period | 9.2 Hold and manage assets | R-DIS-15 | CTL-27 | Head of NPA | To confirm with Compliance | S5 rwb-asset |
| REG-13 | BOT asset classification and provisioning | Write off only accounts that meet the write-off criteria, with the approval required | 10.1 Assess write-off; 10.2 Approve and post | R-WO-01 to R-WO-19 | CTL-33, CTL-04 | Write-off committee | To confirm with Compliance | S7 rwb-writeoff; P7 rwb-decision |
| REG-14 | BOT NPA holding rules | Hold foreclosed assets within the permitted period and provision them on schedule | 9.2 Hold and manage assets | R-DIS-06, R-DIS-09 | CTL-30 | Head of NPA | To confirm with Compliance | S5 rwb-asset |
| REG-15 | BOT reporting | Report repossessed vehicles and loss on sale in the BOT format | 15.1 Report performance | Reporting | CTL-38 | Reporting and BI analyst | To confirm with Compliance | S5 rwb-asset |
| REG-16 | Civil and Commercial Code: guarantee | Send the guarantor notice within the period after the debtor's default | 7.5 Pursue guarantors and co-borrowers | R-GUA-06 | CTL-20, CTL-15 | Guarantee officer | To confirm with Legal | S3 rwb-guarantee; P6 rwb-comms |
| REG-17 | Civil and Commercial Code: mortgage | Send the mortgagor notice and wait the notice period before enforcing the mortgage | 8.1 Prepare pre-litigation | R-LIT-01, R-LIT-07, R-LIT-15 | CTL-14, CTL-15 | Head of Litigation | To confirm with Legal | P6 rwb-comms |
| REG-18 | Civil and Commercial Code: prescription | File before the claim expires under the prescription period for the claim type | 8.1 Prepare pre-litigation; 8.2 Instruct and file | R-UNI-31, R-LIT-11, R-LIT-20 | CTL-18 | Head of Litigation | To confirm with Legal | P3 rwb-case |
| REG-19 | Civil Procedure Code | Serve the claim correctly and keep proof of service | 8.2 Instruct and file; 8.3 Manage to judgment | R-LIT-07 to R-LIT-10 | CTL-15, CTL-19 | Legal counsel | To confirm with Legal | P6 rwb-comms; S4 rwb-litigation |
| REG-20 | Hire purchase contract rules | Give the hirer notice before terminating the contract and repossessing, and notify the hirer and guarantor before the vehicle is sold | 9.1 Take assets onto the books; 9.4 Sell assets by Dutch auction | R-DIS-01, R-DIS-04, R-DIS-05 | CTL-14, CTL-15, CTL-38 | Head of Asset Liquidity | To confirm with Legal | P6 rwb-comms; S5 rwb-asset |
| REG-21 | Bankruptcy Act | Stop enforcement and file the claim with the official receiver within the deadline | 11.6 X5 Bankruptcy or external seizure | R-UNI-07 | CTL-22 | Legal counsel | To confirm with Legal | S8 rwb-deviation |
| REG-22 | Personal Data Protection Act s.24 and s.26 | Process personal data only on a lawful basis; process sensitive data only where the Act allows | 16.5 Control access and data protection | Data classification | CTL-09, CTL-11 | Compliance and PDPA officer | To confirm with Compliance | P4 rwb-access |
| REG-23 | Personal Data Protection Act | Answer data subject requests within the statutory period | 16.7 Handle data subject requests | R-UNI-11 | CTL-42 | Compliance and PDPA officer | To confirm with Compliance | P3 rwb-case |
| REG-24 | Personal Data Protection Act | Keep personal data no longer than the retention period and protect it with security measures | 13.3 Store and retain documents; 16.5 Control access and data protection | Retention classes (DL26) | CTL-11, CTL-12 | Compliance and PDPA officer | To confirm with Compliance | P4 rwb-access; P5 rwb-document |
| REG-25 | Personal Data Protection Act | Notify the regulator of a personal data breach within the required time | 16.6 Manage incidents and continuity | Incident process | CTL-37 | Compliance and PDPA officer | To confirm with Compliance | S9 rwb-partner |
| REG-26 | Personal Data Protection Act | Share personal data with partners and debt buyers only under agreements and masking | 9.6 Sell debt; 12.2 Exchange work with partners | R-DS-10 to R-DS-13 | CTL-31, CTL-32 | Compliance and PDPA officer | To confirm with Compliance | S6 rwb-debtsale |
| REG-27 | Credit Information Business Act | Report and correct credit information for recovery accounts accurately | 15.8 Classify, stage and re-age accounts | Reporting | CTL-02 | Credit Administration | To confirm with Compliance | P1 rwb-source-data |
| REG-28 | Thai Credit Guarantee Corporation rules | Claim within the TCG deadline with the required documents | 7.4 Claim guarantees | R-GUA-01 to R-GUA-07 | CTL-20 | Guarantee officer | To confirm with Compliance | S3 rwb-guarantee |
| REG-29 | Bank policy: NPL resolution policy (1 Jul 2026) | Resolve non-performing debt by the routes, criteria and approvals the policy sets | 7.2 Decide the route; 14.1 Set strategy and treatment policy | Route rules | CTL-04, CTL-08 | Product heads | In force | P7 rwb-decision |
| REG-30 | Bank regulation: approval authority for problem loans and NPA (กกค.540031, amended by กกค.690070) | Approve each recovery decision at the level and within the limit the regulation sets | 17.1 Route recommendations for approval | Delegation of authority table | CTL-04, CTL-05 | Risk with the product heads | In force | P7 rwb-decision; P4 rwb-access |
| REG-31 | Bank policy and regulation: sale of NPA (1 Jul 2026) | Sell NPA by the permitted channels, at approved prices, with complete public listings | 9.3 Decide the disposal route; 9.4 Sell assets by Dutch auction; 9.5 Other disposal routes | R-DIS-19 to R-DIS-29 | CTL-28, CTL-29 | Head of NPA | In force | S5 rwb-asset |
| REG-32 | BOT IT risk and outsourcing | Control access, keep audit trails and oversee outsourced service providers | 16.5 Control access and data protection; 12.4 Govern partners | Permission matrix | CTL-06, CTL-09, CTL-10, CTL-37 | Application owner | To confirm with Compliance | P7 rwb-decision; P4 rwb-access; S9 rwb-partner |

# 14. Audit findings

The Audit Findings Response Map v2 lists 42 findings from the collections and recovery audit and review lists. Each is copied with the controls and the release that answer it. The program measure Audit findings and fraud cases (section 2, 50 to 13) counts these findings (GAP-3256).

| ID | Source | Finding | Area | Status today | Controls | Workbench change | Release |
|---|---|---|---|---|---|---|---|
| AF-01 | Collections audit | Suspicious transactions linked to staff; staff accounts linked to suspicious parties | Approval and authority | Open | CTL-40, CTL-39 | Staff payment flag on customer accounts; conduct sample | E8 |
| AF-02 | Collections audit | Staff paid installments on behalf of debtors | Approval and authority | On process, 31 Aug 2026 | CTL-40 | Payments from staff accounts flagged daily | E8 |
| AF-03 | Collections audit | Unsuitable user access to EFS and the voice bot | Approval and authority | Open | CTL-09, CTL-10 | Role-based access, scope, access review every six months | E1 |
| AF-04 | Collections audit | Incentive and commission rules not suitable | Approval and authority | Open | CTL-08 | Incentive inputs read from the decision log; rules as versioned data | E8 |
| AF-05 | Collections audit | Fleet fuel spending not controlled | Approval and authority | Complete | None | Outside the Workbench | None |
| AF-06 | Collections audit | Litigation not filed for debtors meeting the procedure criteria | Approval and authority | Open | CTL-18, CTL-15 | Prescription watch; litigation route by rule | E2 |
| AF-07 | Collections audit | Cost of collection between field staff and agencies not managed | Approval and authority | Open | CTL-35 | Placement by measured return; cost per partner | E6 |
| AF-08 | Collections audit | Governance and authority in the SCBP closure and work transfer unclear | Approval and authority | Open | CTL-03 | Allocation and transfer by rule with reasons | E1 |
| AF-09 | Collections audit | Staff sent debtor data to personal email | Documentation and audit trail | Open | CTL-11, CTL-31 | No export beyond the role; masking; data stays in the Workbench | E1 |
| AF-10 | Collections audit | Field staff did not record results in EFS in full | Documentation and audit trail | Open | CTL-07 | Interaction ledger; override reason required | E2 |
| AF-11 | Collections audit | Evidence for decisions incomplete or unreliable | Documentation and audit trail | Open | CTL-06, CTL-12, CTL-13 | Decision log; write-once legal documents; custody | E1 |
| AF-12 | Collections audit | IT security, SDLC and system governance documents incomplete | Documentation and audit trail | Open | None | This document set: architecture, security, test and run documents | E1 |
| AF-13 | BOT | Risk assessment, governance and transition plan for the SCBP closure incomplete | Documentation and audit trail | Open | None | Outside the Workbench | None |
| AF-14 | Collections audit | Interest not reduced under TDR terms after full payment | Fee, interest and debt amount | Open | CTL-25 | Exception list for completed plans without the rate change | E2 |
| AF-15 | Collections audit | Relief scheme report inaccurate | Fee, interest and debt amount | Open | CTL-23 | Scheme results read from treatment records | E3 |
| AF-16 | Collections audit | Installments and interest plan set wrongly in a relief scheme | Fee, interest and debt amount | On process, 31 Aug 2026 | CTL-23, CTL-26 | Terms checked by rule before approval | E3 |
| AF-17 | Collections audit | Payment or compensation calculated wrongly in a relief scheme | Fee, interest and debt amount | Open | CTL-23, CTL-24 | Payoff age check; settlement against the floor | E3 |
| AF-18 | BOT | Demand fee notice to customers incomplete | Fee, interest and debt amount | Open | CTL-14 | Notices from approved templates with the fee fields | E2 |
| AF-19 | Collections audit | Debtors meeting criteria not transferred to the responsible unit | Debt collection practice | Open | CTL-01, CTL-03 | Case entry and allocation by rule | E1 |
| AF-20 | Collections audit | Staff welfare loans over 115 days without an owner | Debt collection practice | Open | CTL-01 | Every account at 90 days past due has a case and an owner | E1 |
| AF-21 | Collections audit | Debtors not removed from a relief scheme when no longer eligible | Debt collection practice | Open | CTL-25 | Scheme eligibility re-tested on each load | E3 |
| AF-22 | Collections audit | Deceased debtors and guarantors not followed per procedure | Debt collection practice | Complete | CTL-21 | X3 by rule | E7 |
| AF-23 | Collections audit | EFS did not allocate work, leaving gaps in follow-up | Debt collection practice | Open | CTL-01, CTL-03 | Daily reconciliation; allocation by rule | E1 |
| AF-24 | Collections audit | Ransomware attack at an outsource agency | Agency governance | Open | CTL-37 | Partner security review; suspension and recall | E6 |
| AF-25 | Collections audit | Work allocation to agencies not based on performance | Agency governance | Open | CTL-35 | Placement by scorecard | E6 |
| AF-26 | Collections audit | Agency case progress not tracked in full | Agency governance | Open | CTL-36 | Partner service level clocks | E5 |
| AF-27 | Collections audit | Recoverable court fees not tracked in full | Agency governance | Open | CTL-36 | Fee ledger to receipt | E5 |
| AF-28 | Collections audit | Photograph standard for repossessed vehicles unclear | Agency governance | Open | CTL-38 | Condition record with photographs required at take-on | E7 |
| AF-29 | Recovery audit 2026 | Credit model selection not suited to the debtor in two cases | Recovery | Complete | None | Model version recorded per decision | E4 |
| AF-30 | Recovery audit 2026 | Relief scheme compensation where the first-year installment exceeds 50 percent | Recovery | On process, 31 Aug 2026 | CTL-23 | Terms checked by rule | E3 |
| AF-31 | Recovery audit 2026 | Hire purchase TDR accounts classified with the wrong product type | Recovery | On process | CTL-02 | Product type from the core load checked against the list | E1 |
| AF-32 | Recovery review 2026 | Collection process delayed TCG claims | Recovery | Complete | CTL-20 | Claim deadline timer | E4 |
| AF-33 | Recovery review 2026 | Write-off not done per the bank's criteria | Recovery | Complete | CTL-33 | Write-off eligibility by rule | E6 |
| AF-34 | Recovery review 2026 | Bad debt follow-up not canceled for bankruptcy cases | Recovery | Complete | CTL-22, CTL-34 | X5 and follow-up end by rule | E6 |
| AF-35 | Recovery review 2026 | SSME unsecured debt over 180 days not managed effectively | Recovery | On process, 31 Oct 2026 | CTL-19, CTL-01 | Every case owned; litigation pack by rule | E5 |
| AF-36 | Compliance review 2026 | 26 Responsible Lending accounts with no contact in the period | Recovery | Complete | CTL-01, CTL-16 | Every case owned with a contact plan | E2 |
| AF-37 | Recovery audit 2025 | Stage 3 collateral not revalued within the required period | Recovery | Complete | CTL-27 | Re-appraisal cycle by rule | E3 |
| AF-38 | Recovery audit 2025 | NPA transferred but not actioned or actioned late | Recovery | Complete | CTL-30 | Take-on exception list | E3 |
| AF-39 | Recovery audit 2025 | NPA listings on the website and app incomplete or wrong | Recovery | Complete | CTL-29 | Listing completeness check | E3 |
| AF-40 | Recovery audit 2025 | Brokers set prices below the bank's listed price | Recovery | Complete | CTL-28 | Floor price within the limit | E3 |
| AF-41 | Recovery audit 2025 | Not every account of a debtor restructured | Recovery | Complete | CTL-26 | Treatment covers every account | E3 |
| AF-42 | Recovery audit 2025 | Monitoring of accounts in TDR status not enough | Recovery | Complete | CTL-25 | Restructure performing measure and exceptions | E2 |

# 15. Controls

The Controls Catalog v4 lists 44 controls on the recovery process. Each answers an audit finding or a regulatory obligation. The catalog holds how each control is performed, its evidence and its test; this table carries what it checks and what it answers (GAP-3257).

| ID | L2 | Process | What it checks | Type | Obligations | Audit finding it answers | First in | Owner service |
|---|---|---|---|---|---|---|---|---|
| CTL-01 | 6.1 | Take over the case at 90 days past due | Every account at 90 days past due or more in v_ace_account has exactly one open case, and the five ACE reconciliations REC-01 to REC-05 close with zero unexplained on each business date | Detective | REG-07 | EFS did not allocate work and left gaps in follow-up | E1 | P3 rwb-case |
| CTL-02 | 6.1 | Take over the case at 90 days past due | Each ACE ingestion job for a recovery source completes for the business date and passes the business date, structure, control total, key, reference and list checks before the views serve it | Preventive | REG-11, REG-27 | Collateral data repaired in WIN was recorded wrongly | E1 | P1 rwb-source-data |
| CTL-03 | 18.3 | Build and allocate work lists | Each new case is allocated by the allocation table within the caseload cap, with the rule row recorded | Preventive | REG-07 | Debtors meeting the criteria were not transferred to the responsible unit | E1 | P3 rwb-case |
| CTL-04 | 17.1 | Route recommendations for approval | The approver holds the approval level and the amount is within the limit for the decision, product and level | Preventive | REG-05, REG-13, REG-29, REG-30 | Approval and authority governance findings (9 of 29) | E2 | P7 rwb-decision |
| CTL-05 | 17.1 | Route recommendations for approval | The person who prepared a decision cannot approve it | Preventive | REG-30 | Approval and authority governance findings | E2 | P4 rwb-access |
| CTL-06 | 17.2 | Keep the decision log | No action proceeds unless its decision log entry is written | Preventive | REG-32 | Documentation and audit trail findings (5 of 29) | E1 | P7 rwb-decision |
| CTL-07 | 17.2 | Keep the decision log | A person who departs from the recommendation records a coded reason | Preventive | None | Collection officers did not record results in EFS in full | E2 | P7 rwb-decision |
| CTL-08 | 14.2 | Set decision rules and limits | A rule, limit or list changes only through a validated load approved by its owner, and by Risk where a limit moves | Preventive | REG-29 | Collection procedure not followed because rules lived in documents | E1 | P7 rwb-decision |
| CTL-09 | 16.5 | Control access and data protection | Every request is checked against the role, the capability and the scope; out of scope records are refused | Preventive | REG-22, REG-32 | Unsuitable user access to EFS and the voice bot | E1 | P4 rwb-access |
| CTL-10 | 16.5 | Control access and data protection | Role owners confirm each person's roles every six months; leavers lose access the same working day | Detective | REG-32 | Unsuitable user access to EFS and the voice bot | E2 | P4 rwb-access |
| CTL-11 | 16.5 | Control access and data protection | Personal fields are masked unless the role is allowed to see them; no personal data leaves the bank by email | Preventive | REG-22, REG-24 | Staff sent debtor data to personal email | E1 | P4 rwb-access |
| CTL-12 | 13.3 | Store and retain documents | Legal documents cannot be changed or deleted; a new version is added instead | Preventive | REG-24 | Evidence for decisions incomplete or unreliable | E1 | P5 rwb-document |
| CTL-13 | 13.4 | Control document custody | Each original document has a holder and a due-back date; overdue originals raise a task | Detective | None | Evidence for decisions incomplete or unreliable | E2 | P5 rwb-document |
| CTL-14 | 13.2 | Send letters and notices | Every notice is generated from the current template version approved by Legal | Preventive | REG-04, REG-06, REG-17, REG-20 | Demand fee notice to customers incomplete (BOT finding) | E2 | P6 rwb-comms |
| CTL-15 | 13.2 | Send letters and notices | A notice period starts only from the delivery date on the proof of delivery | Preventive | REG-06, REG-16, REG-17, REG-19, REG-20 | Litigation not filed for debtors meeting the procedure criteria | E2 | P6 rwb-comms |
| CTL-16 | 11.1 | Answer customer contacts | No contact is made while a contact stop is in force; statutory notices continue | Preventive | REG-01, REG-08, REG-09 | Debt collection practice findings | E2 | P6 rwb-comms |
| CTL-17 | 11.1 | Answer customer contacts | Messages go only on channels the customer has consented to | Preventive | REG-01 | Debt collection practice findings | E2 | P6 rwb-comms |
| CTL-18 | 8.1 | Prepare pre-litigation | Every case has a prescription date; a warning forces a litigation review ahead of other actions | Preventive | REG-18 | Litigation not filed for debtors meeting the procedure criteria | E2 | P3 rwb-case |
| CTL-19 | 8.2 | Instruct and file | The pack holds every required document before filing | Preventive | REG-19 | SSME unsecured debt over 180 days not managed effectively | E5 | S4 rwb-litigation |
| CTL-20 | 7.4 | Claim guarantees | Each guarantee has a claim deadline timer from the date the default conditions are met | Preventive | REG-16, REG-28 | Collection process delayed TCG claims | E4 | S3 rwb-guarantee |
| CTL-21 | 11.4 | X3 Deceased customer | A death raises X3, stops contact and routes the case to the specialist and Legal | Preventive | None | Deceased debtors and guarantors not followed per procedure | E7 | S8 rwb-deviation |
| CTL-22 | 11.6 | X5 Bankruptcy or external seizure | A bankruptcy stops enforcement, starts the claim deadline and ends bad debt follow-up where the rule applies | Preventive | REG-21 | Bad debt follow-up not canceled for bankruptcy cases | E7 | S8 rwb-deviation |
| CTL-23 | 7.3 | Negotiate settlement or deed in lieu | A settlement below the floor goes for approval with the gap shown | Preventive | REG-10 | Payment and compensation amounts calculated wrongly in relief schemes | E3 | S2 rwb-treatment |
| CTL-24 | 7.3 | Negotiate settlement or deed in lieu | A payoff figure older than its limit is refreshed before an offer is sent | Preventive | None | Fee, interest and debt amount findings (5 of 29) | E3 | S2 rwb-treatment |
| CTL-25 | 6.1 | Take over the case at 90 days past due | Interest is reduced under the restructure terms once the customer has paid as agreed | Detective | REG-10, REG-11 | Interest not reduced per TDR conditions after full payment | E2 | S2 rwb-treatment |
| CTL-26 | 6.1 | Take over the case at 90 days past due | A restructure covers every account of the customer in the case | Preventive | REG-05 | Some debtors did not have every account restructured | E3 | S2 rwb-treatment |
| CTL-27 | 9.2 | Hold and manage assets | An asset is priced only on an appraisal inside its age limit; Stage 3 collateral is revalued on schedule | Preventive | REG-12 | Stage 3 collateral not revalued within the required period | E3 | S5 rwb-asset |
| CTL-28 | 9.4 | Sell assets by Dutch auction | The floor price is within the approver's limit as a share of fair market value | Preventive | REG-31 | Brokers set prices below the bank's listed price | E3 | S5 rwb-asset |
| CTL-29 | 9.4 | Sell assets by Dutch auction | Every asset ready to sell is listed on HOME.SCB and the app with the approved price and details | Detective | REG-31 | NPA listings on the website and app incomplete or wrong | E3 | S5 rwb-asset |
| CTL-30 | 9.1 | Take assets onto the books | An asset whose title has transferred is taken onto the books and moved to sale without delay | Detective | REG-14 | NPA assets transferred but not actioned or actioned late | E3 | S5 rwb-asset |
| CTL-31 | 9.6 | Sell debt | The data tape passes the masking check before the data room opens | Preventive | REG-26 | Staff sent debtor data to personal email | E5 | S6 rwb-debtsale |
| CTL-32 | 9.6 | Sell debt | Only buyers who pass KYC, licensing and eligibility and sign the non-disclosure agreement reach the data room | Preventive | REG-26 | Outsource agency governance findings | E5 | S6 rwb-debtsale |
| CTL-33 | 10.1 | Assess write-off | Only cases meeting the eligibility rule and the tax criteria version enter the write-off population; cases with open deviations are held out | Preventive | REG-13 | Asset write-off not done per the bank's criteria | E6 | S7 rwb-writeoff |
| CTL-34 | 10.3 | Recover after charge-off | Follow-up on written-off debt ends when the bank's criteria are met, and the case is handed to the right unit | Detective | None | Bad debt follow-up not canceled per regulation and procedure | E6 | S7 rwb-writeoff |
| CTL-35 | 12.3 | Track performance and pay fees | Work goes to partners by the scorecard and the panel rules, not by hand | Preventive | REG-03 | Work allocation to agencies not based on performance | E6 | S9 rwb-partner |
| CTL-36 | 12.3 | Track performance and pay fees | Every partner instruction has a service level; court fees due back are tracked to receipt | Detective | None | Agency case progress and recoverable court fees not tracked in full | E5 | S9 rwb-partner |
| CTL-37 | 12.4 | Govern partners | Partners meet the bank's security and conduct requirements; a breach suspends allocation and recalls work | Detective | REG-03, REG-25, REG-32 | Ransomware attack at an outsource agency | E6 | S9 rwb-partner |
| CTL-38 | 9.1 | Take assets onto the books | Each repossessed vehicle has a condition record with photographs in the set standard | Preventive | REG-15, REG-20 | Photograph standard for repossessed vehicles unclear | E7 | S5 rwb-asset |
| CTL-39 | 16.2 | Control conduct | A sample of contacts, notices and decisions is checked each month against the conduct rules | Detective | REG-01, REG-02, REG-08 | Employee conduct and suspicious transactions | E8 | P9 rwb-reporting |
| CTL-40 | 16.2 | Control conduct | Payments from staff accounts to customer loans are flagged for review | Detective | None | Staff paid installments on behalf of debtors | E8 | P8 rwb-payment |
| CTL-41 | 19.3 | Reconcile and correct | Every receipt is matched to the case and the account, or held on the exception list | Detective | None | Fee, interest and debt amount findings | E4 | P8 rwb-payment |
| CTL-42 | 16.7 | Handle data subject requests | A data subject request holds automated processing on the case and reaches Compliance within the statutory period | Preventive | REG-23 | PDPA obligations | E2 | P3 rwb-case |
| CTL-43 | 16.5 | Control access and data protection | Every read of ACE source data goes through recovery.v_ace_*; the view-owner role holds SELECT on the listed ACE tables and nothing else; the recovery role has no privilege on an ACE table and cannot write a view | Preventive | REG-22, REG-32 | Unsuitable user access to EFS and the voice bot | E1 | P1 rwb-source-data |
| CTL-44 | 16.4 | Answer audit and regulatory requests | Every recovery.v_ace_* view exists with the columns and types the dictionary and the data contract publish: 30 views, 122 objects and 1,366 fields | Detective | REG-11, REG-27 | None | E1 | P1 rwb-source-data |

# 16. Reports and management information

The Reporting and Management Information Requirements v2 lists 14 reports. Each is copied with its readers, frequency, the decision it supports, its measures and its first epic. The source's Built in column names Power BI and the data lake, which ADR-018 removes; under D-RCV-60 every report is built from the reporting read model of P9 rwb-reporting, and the source of the regulatory extract is open (GAP-1657; GAP-3261).

| ID | Report | Who reads it | How often | Decision it supports | Measures | First in |
|---|---|---|---|---|---|---|
| RPT-01 | CEO update | CEO, sponsors | Every two weeks | Whether recovery and the program are on track | Flow rate B1 to B3, % recovery, NPL reduction, NPA sales, program status by epic, decisions needed | E2 |
| RPT-02 | Steering committee pack | Steering committee | Monthly | Scope, budget, risks and decisions above the program | Project KPIs against the scorecard; benefits; risks; decisions | E2 |
| RPT-03 | Steering dashboard | Product heads, Chief Debt Recovery Management Office | Daily | Where recovery is behind and why | Inflow, stock, cures, recovery by route and product, turnaround, cost | E2 |
| RPT-04 | Queue and caseload | Team managers | Daily | Who needs help and which cases are at risk | Cases per owner against the cap, age in state, breached service levels, exception queues | E2 |
| RPT-05 | Litigation service levels | Head of Litigation | Weekly | Which packs and firms are late | Document preparation SLA (target 60%), legal SLA (target 95%), time to file, firm scorecard | E5 |
| RPT-06 | Settlement and deed in lieu | Product heads | Weekly | Whether treatments reach booking | Offers, approvals, bookings, turnaround, below-floor approvals | E3 |
| RPT-07 | NPA stock and sales | Head of NPA | Weekly | What is unsold and why | Stock by age, holding cost, listings, sales against floor, NPA sales amount | E3 |
| RPT-08 | Debt sale and internal AMC | Head of Asset Liquidity | Per lot; monthly | Whether lots achieve their reserve and the uplift against debt sale | Lots, bids against reserve, recovery uplift versus debt sales (target 45%), put-backs | E6 |
| RPT-09 | Write-off and recovery after charge-off | Finance and CFO delegate | Monthly | What is written off and recovered | Population, approvals, postings, recovery after write-off | E6 |
| RPT-10 | Partner scorecard | Partner and agency manager | Monthly | Which partners get more or less work | Results, service levels, cost, conduct by partner | E7 |
| RPT-11 | Decision and agent monitor | Risk and model risk officer, center of excellence | Weekly | Whether rules and agents decide well | Acceptance, overrides by reason, fallbacks, outcomes by route against rule-only | E2 |
| RPT-12 | Data health | Data steward | Daily | Whether the data can be trusted today | Loads, checks, breaks, stale products | E1 |
| RPT-13 | Audit and controls | Internal audit, Compliance | Quarterly | Whether controls ran | Control evidence by control ID; access reviews; decision log chain | E2 |
| RPT-14 | Regulatory returns | Compliance, Finance | As the regulator requires | BOT reporting obligations | Repossessed vehicles and loss on sale; relief scheme results | E8 |

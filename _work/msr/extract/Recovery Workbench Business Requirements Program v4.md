Recovery Workbench

Business requirements, program

SCB Collections and Recovery. Henka Group, 15 November 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench business requirements, program |
| Version | 4 |
| Date | 15 November 2026 |
| Prepared by | Henka Group |
| Covers | All eight epics, November 2026 to June 2027 |
| Structure | ISO/IEC/IEEE 29148, until the SCB X requirement template is adopted (DL13) |
| Change | Version 4 re-bases the program requirements on the ACE database under D-RCV-35 (U1 to U5) and ADR-010, which supersedes ADR-005. Sections 1.1, 5 (intro and 5.1 to 5.3), 6.3, 6.5 (NFR-032), 7 and 9 change: section 5.1 states the four-tier read model and its counts, 5.2 is outbound only and 5.3 states the business-key link to ACE; the Workbench runs no inbound source load, reads source data only through the read-only recovery.v_ace_* views, and leaves Excel and SharePoint trackers to the Cutover plan. Requirement IDs are kept. REQ-RDF-005 and 006 are marked removed with their later home, and REQ-RDF-008 is re-worded to the reconciliation duty that stays in the Workbench, leaving 229 of 231 requirements live. DL43 is added as open. Other sections are unchanged. |


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

The read model has four tiers. Tier 1 is 22 ACE tables that exist today; the recovery data in them is read through 16 Section A views, and the Workbench never alters them. Tier 2 is 14 ACE tables and 12 columns the ACE team adds under RWB-ACE-001 for 80 source fields; the new tables are read through 14 Section B views and the new columns extend v_ace_account, v_ace_customer and v_ace_efs_action. Tier 3 is 4 Workbench extension tables keyed by ACE business keys. Tier 4 is 88 retained Workbench tables. The recovery schema is 92 tables; with the 30 views the dictionary holds 122 sys_objects and 1,366 sys_fields.

Two migrations carry the views, because a view cannot be created over a table that does not exist. Section A ships with RWB-E1-069, the next free sequence after the V0001 baseline. Section B ships when RWB-ACE-001 lands, and until then the features that read the Tier 2 additions stay behind their flags. DL43 is open: the ACE team has yet to accept the RWB-ACE-001 scope and its dates. No copy, load or tracker table remains in the recovery schema; source content is read through the views and the trackers are retired through the Cutover plan.

| ID | Requirement | Priority | Owner | Epic |
|---|---|---|---|---|
| REQ-RDF-001 | Recovery data is held in 14 data products, each with exactly one named system of record, ACE (ingested from the named source) or the Workbench, and one named owner. Source data in a data product is read from the ACE database through the read-only recovery.v_ace_* views and is not copied into the Workbench (D-RCV-35, ADR-010). | Must | Data steward and data product owner | E1 |
| REQ-RDF-002 | Account balance, arrears, payments and classification for every account at 90 or more days past due are read from ACE through v_ace_account and v_ace_payment, current to the latest completed ACE batch for the previous working day. | Must | Data steward and data product owner | E1 |
| REQ-RDF-003 | Collections contact history, promises and case status from EFS are read from ACE through v_ace_efs_action and v_ace_efs_assignment, so that the case carries what happened before day 90. | Must | Data steward and data product owner | E1 |
| REQ-RDF-004 | Collateral records and appraisal values are available on the case without a person looking them up in CCMS or SVAF. ACE ingests them under RWB-ACE-001, and the Workbench reads them through v_ace_collateral, v_ace_collateral_detail and v_ace_valuation (DL43). The Workbench's acceptance of an appraisal is held in valuation_ext. | Must | Data steward and data product owner | E1 |
| REQ-RDF-005 | Removed by D-RCV-35 (U5). Excel and SharePoint trackers leave system scope. Later home: the tracker retirement procedure in the Cutover plan. Was: every recovery team's Excel file, SharePoint list and local file is listed with its owner, fields and update cycle, and each one has a decision to load it or record it as out of scope. | Removed | Program manager | E1 |
| REQ-RDF-006 | Removed by D-RCV-35 (U5). No tracker is loaded into the Workbench. Later home: the Cutover plan, which retires each local copy with the owner's confirmation and a read-only archive. Was: every file with a load decision is loaded, its row counts reconciled, and its local copy retired with the owner's confirmation and a read-only archive kept. | Removed | Data steward and data product owner | E1 |
| REQ-RDF-007 | The case list reconciles daily to the count of accounts at 90 or more days past due in v_ace_account, with no variance (DL25), and every business key on a Workbench table resolves to an ACE row. | Must | Data steward and data product owner | E1 |
| REQ-RDF-008 | Data quality checks on source data run in ACE ingestion (RWB-ACE-001). The Workbench reports reconciliation breaks, referential completeness and its quality measures, each break with a reason visible to the data product owner. | Must | Data steward and data product owner | E1 |
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

78 non-functional requirements. Proposed targets apply until the bank sets a value. Open targets are held under DL11, and retention and protection targets under DL26.

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
| Built on ACE | The Workbench is a module of ACE: one service, one repository, one front end |
| Modular monolith | Common, collection and recovery modules, with boundaries checked at build time |
| Programmatic workflow | Case, stage and task state held in the database and moved by code, in CMMN 1.1 terms. No Temporal |
| Principle 1 | Every rule, limit, threshold, template, name, queue, role, timer and route is a versioned data row, changed through a validated load without a code release |
| Data through ACE ingestion | Source data lands in the ACE database through ACE ingestion, including sources ACE does not hold today. The recovery module reads it only through the read-only recovery.v_ace_* views, links to it by ACE business keys and holds no copy, load or staging table (D-RCV-35, ADR-010). No real-time feed today; same-day needs are named under DL06 |
| ACE team dependency | The ACE team owns every ACE table and column the views read, and adds 14 tables, 12 columns and 80 source fields under RWB-ACE-001 by 21 November 2026 for the 30 November release (DL43). Features that read the Tier 2 additions stay behind their feature flags until the additions land |
| Document hub | The Workbench is the system of record for recovery documents |
| Monthly releases | One production release at each month end, shared with the collection squad |


# 8. Release plan

| Epic | Release | Theme | What the business gets |
|---|---|---|---|
| E1 | 30 Nov 2026 | Foundation 1 | One case list for every account at 90 days past due or more, reconciled to the core bank. Documents found by case. Decision log store. Read-only case record view |
| E2 | 31 Dec 2026 | Foundation 2 | One owner and a timer on every case, full history on one screen, approval routing, litigation notices generated and approved, steering dashboard |
| E3 | 31 Jan 2027 | Settle, deed in lieu, assets | Settlements and deeds in lieu end to end to booking. Asset record, floor price and listing on HOME.SCB |
| E4 | 28 Feb 2027 | Route decision | The route recommended with reasons and approved within the delegation of authority for every new case. Guarantee and TCG claims. Auction rounds and RAMC transfer |
| E5 | 31 Mar 2027 | Litigation | Litigation instructed and tracked end to end, law firms through the partner portal. Debt sale lot data and the buyer data room |
| E6 | 30 Apr 2027 | Debt sale and write-off | Debt sale screens and award, write-off committee, partner panel, allocation and fees |
| E7 | 31 May 2027 | Deviations and partners | Deviations X1 to X7 end to end. Partner scoring, conduct and the field app |
| E8 | 30 Jun 2027 | Administration and hardening | Full administration, conduct checks, autonomy step-ups, regulatory returns, hardening |


# 9. Open decisions that change these requirements

DL43 is the new open decision. The others keep their v3 answers, with the wording changed where D-RCV-35 supersedes the COLLINS route or the read and write position.

| Decision | Question | Answer the build uses until decided | Owner | Needed by |
|---|---|---|---|---|
| DL06 | Which interfaces need real time data, and which take the daily batch? | Option A, daily batch through COLLINS, is superseded by D-RCV-35: ACE ingests all source data, so the Workbench runs no source batch load and reads ACE once its batch is complete. Option B for the named same-day triggers. ACE has no real time feed today. Name the same-day triggers now: case transferred from EFS, payment received, legal event. | K. Book with K. Pipat | 30 Oct |
| DL10 | What is the Thai name for each field, label and message? | The business lead drafts per module one epic ahead; Legal and Compliance approve. | Business lead with Legal and Compliance | 5 Nov |
| DL11 | What is the value for each non-functional target, or the owner and date for it? | Use the ACE values where ACE has them; the solution architect proposes the rest; Risk agrees. | Solution architect with Risk | 5 Nov |
| DL12 | Which legacy systems are kept, and does any need enhancing? | No legacy enhancement, with a list of the systems kept and what the Workbench reads from each. The read and write part of option A is superseded by D-RCV-35: source data is read only, through the SELECT-only recovery.v_ace_* views, not a direct read of ACE or COLLINS. | K. Tony with K. Book | 7 Nov |
| DL13 | The SCB X consortium template for AI code generation arrives on 29 October. Are the Epic 1 and Epic 2 requirements rewritten to it before the build? | Remap the Epic 1 requirements by 4 November and use the template from Epic 2. TechX, SCB and Henka agree one template and keep it for every later epic. | K. Tee with TechX and Henka | 30 Oct |
| DL15 | Are the inventory counts and the growth assumption the right base for sizing? | A: Mortgage 12,256, hire purchase 12,960 and SSME 2,903 accounts; 3,110 new accounts a month; 15 percent growth a year. | Data lead | 6 Nov |
| DL16 | Does a case enter the Workbench at 90 or 91 days past due? | 90 days past due. The target operating model has the case owner holding the case from day 90. | Business lead | 6 Nov |
| DL17 | Is a case one per customer per product, one per account, or one per customer? | One per customer per product, with the accounts linked. | Product owner with the solution architect | 6 Nov |
| DL18 | Which person holds each approval level, with the limit by decision, amount and product, and the substitute for each? | Load the regulation's levels and limits now; add names and substitutes when signed. | Risk with the product heads | 30 Nov |
| DL20 | Where do customer facts come from? | The customer facts ACE holds, which ACE ingests from SCBPDM and the core bank; the Workbench reads them through v_ace_customer. Amended by D-RCV-35, which removes the COLLINS route. | Solution architect with K. Book | 30 Oct |
| DL22 | How long may a case stay in each state before it escalates? | Load the values as parameters; escalation runs from the day they are loaded. | Business lead | 13 Nov |
| DL23 | What is the most cases a person holds, and how is a queue ordered? | Load as parameters. | Product owner | 13 Nov |
| DL26 | How long is each data product and document type kept, and which fields are masked for which role? | Provide per data product and document type. | Compliance | 13 Nov |
| DL27 | How are storage, backup, legal hold and e-discovery provided for the document hub? | The ACE storage pattern with a write-once container and the bank backup service. | Solution architect with Compliance | 13 Nov |
| DL43 | Does the ACE team accept the RWB-ACE-001 scope and its dates? The scope is 14 new ACE tables, 12 new columns and 80 source fields. | Open. The build assumes the scope is accepted: 14 new ACE tables, 12 new columns and 80 source fields. Dates to confirm, and the Tier 2 features stay behind their flags until the additions land. | ACE team lead | 21 Nov |


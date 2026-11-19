<!-- working-copy-of: requirement/legacy/03-requirements-and-specifications/recovery-workbench-lean-brd-epic-1-v3-docx.md -->
> **Working copy.** Canonical source: `requirement/legacy/03-requirements-and-specifications/recovery-workbench-lean-brd-epic-1-v3-docx.md`. Edit the source, not this copy.

Recovery Workbench

Lean BRD, Epic 1

SCB Collections and Recovery. Henka Group, 15 November 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench lean BRD, Epic 1 |
| Version | 3 |
| Date | 15 November 2026 |
| Prepared by | Henka Group |
| Structure | ISO/IEC/IEEE 29148, lean |
| Release | 30 November 2026 |
| Status | For business scope approval |

# 1. Problem and outcome

## 1.1 What is wrong today

An account that reaches 90 days past due waits for the weekly manual transfer file at day 91 and is first worked at about day 100. For about ten days the case has no owner and no clock. There is no single case list: each team keeps its own Excel and SharePoint lists, 42 applications hold parts of a case and none owns it, and 650 action codes have no agreed meaning. Documents are kept outside the case, so a gap in a filing set is found on the court date. Approvals are replies to email and cannot be counted.

| Baseline | Figure today |
|---|---|
| Accounts at 90 days past due or more, 30 June 2026 (DL15) | 28,119: Mortgage 12,256, hire purchase 12,960, SSME 2,903 |
| New accounts reaching 90 days past due | 3,110 a month; 15 percent growth a year assumed (DL15) |
| Mapped recovery steps run in Excel | 40.5 percent |
| Hand-off points on one case; email hand-offs | 310, of which 191 pass through three or more people; 346 |
| Litigation filings that breach their service level | 30 to 40 percent |
| Time to resolution | 380 days |
| Open audit findings and fraud cases in recovery | 50 |

## 1.2 Outcome when Epic 1 is live

Epic 1, Foundation 1, releases on 30 November 2026. The bank has one case list for every account at 90 days past due or more, reconciled each day to ALS. Every case has a case ID, a queue, an owner set by rule, timers and a prescription date. Documents are found by case. Every case creation, assignment, transfer and document attachment is in the decision log with the rule version that caused it. The case record view is read only; there are no workflow screens.

Administration and control roles receive real users: center of excellence analyst, data steward and data product owner, internal audit, compliance and PDPA officer, platform administrator, reference data administrator and security administrator. Business roles follow in Epic 2 (DL39). The stories serve data product owners first (10), then product owners, case owners and litigation officers (8 each) and team managers (7).

# 2. Scope

## 2.1 In scope

Mortgage, hire purchase and SSME. Product differences are reference data keyed by product. Source data is read from the ACE database through the 30 read-only recovery.v_ace_* views. The Workbench adds no source data, no staging table and no tracker load; the four extension tables hold only Workbench decisions, keyed by ACE business keys (D-RCV-35, ADR-010).

| Module | Capability |
|---|---|
| P1 Recovery data engine | 14 data products with owners, read from ACE through 30 read-only v_ace_* views. No source load, staging table or tracker load. Freshness from the ACE batch record (v_ace_batch_status). Interaction ledger. Daily reconciliation to the ACE account view. |
| P2 Integration | One pattern for outbound files with checks, retry and an exception queue. Scheduled jobs with monitoring and run books. Feature flags. |
| P3 Case and workflow | Case created by rule with case ID. Roles, teams and queues as data. Allocation, assignment and transfer by rule. Service levels, timers, escalation, prescription dates. Daily rebalancing. Read-only case record view with timeline. |
| P4 Access and administration | Entra ID single sign-on with multi-factor authentication. Role to permission matrix as data. Masking by role. Delegation of authority table. Access log and break-glass. |
| P5 Document hub | Store and index with write-once storage for legal types. One intake from branches, mailroom, partner file transfer and email. OCR, classification into six types, field extraction, review queue. Checklist per case type. Retention class and virus scan. |
| P6 Communications | Templates and merge fields as versioned data with the Legal approval. Demand, recall and guarantor notices generated. |
| P7, P9, P10 | Append-only, hash-chained decision log. Baseline measures in Power BI. Case intake and deviation screening agents scored in shadow; no user sees their output. |

## 2.2 Out of scope

| Excluded from Epic 1 | Where it is done |
|---|---|
| Queue, transfer and approval screens; hand-over with full EFS history; letter dispatch, SMS and LINE; payment matching; steering dashboard; business users | Epic 2 |
| Deviation screening on live cases | Epic 2; end to end in Epic 7 |
| Settlement and deed in lieu to booking; asset record and listing | Epic 3 |
| The route decision D6 and the 448 routing rules | Epic 4 (DL24) |
| Litigation with law firms on the partner portal | Epic 5 |
| Debt sale, write-off and the partner panel | Epic 6 |
| Full administration, agent autonomy step-ups, regulatory returns | Epic 8 |
| Excel and SharePoint tracker inventory, load and retirement | Cutover and Go Live Plan (U5; E1-005, E1-010, E1-012 removed) |
| Collections before 90 days past due (D1 to D4); bank policy changes | Not in the Workbench: EFS and the ACE collection module; the policy owners |

# 3. Business rules

## 3.1 Eligibility

- An account enters recovery at 90 days past due (DL16). The case is created by rule from the daily case list, which reads v_ace_account.

- Accounts that are deceased, under fraud review, bankrupt, on an active restructure plan or in an open dispute are excluded at creation. The exclusion list is reference data owned by Risk.

- One case covers one customer and one product, with its accounts linked (DL17).

- The case ID has the form RW-YYYY-NNNNNN, is issued once, never reused and printed on every letter. Only the Workbench stores it; the account number joins it to other systems (DL21).

## 3.2 Case status and how a case moves

A case holds one status at a time. Epic 1 builds all eight. In Epic 1 a case moves from New to Assigned; the other moves are used from Epic 2.

| Status | Meaning | Moves to |
|---|---|---|
| New | Created at 90 days past due with its history; no owner yet | Assigned, when the allocation rule matches |
| Assigned | Owner and queue set by rule; the stage clock starts | In progress, when the first task starts |
| In progress | The owner or the Workbench is working a task | A waiting status, when an offer, instruction or approval request goes out |
| Waiting customer | Offer, notice or request with the customer; validity timer runs | In progress, on reply or timer expiry |
| Waiting partner | Instruction with a partner; service level timer runs | In progress, on result or timer expiry |
| Waiting approval | Recommendation with the approver the delegation of authority names | In progress, on decision or escalation |
| On hold | Paused by a deviation or legal hold; prescription clock keeps running | The status it paused in, or Closed |
| Closed | Cured, settled, sold, or written off with recovery ended | No further action |

- A move the model does not define is refused and recorded with its reason. A change of queue or owner changes neither the status nor the clocks.

- Every status change writes an event to the decision log and the interaction ledger.

## 3.3 Allocation and routing

- Allocation reads product, region, exposure band, stage, route, deviation flag, segment and collateral type, applies the first matching row and always has a default row.

- Assignment uses round robin, lowest load or a named owner, up to the caseload cap (DL23). Cases over the cap go to the overflow queue. A daily job rebalances unassigned and over-cap cases.

- Transfer moves a case on stage change, route decided, timer expired, deviation raised or cleared, approval needed, document received, payment missed, or a manual request with a reason code.

- Each queue and status has a service level and an escalation role (DL22). A breach alerts the escalation role and does not move the case. Prescription dates come from the legal periods table.

## 3.4 Exception handling

| Exception | What happens |
|---|---|
| The case list differs from the ACE account view | The publish is held; tolerance is zero (DL25) |
| An account fails a reconciliation check | The account carries a reason code for the data product owner |
| A file fails after the retry limit | Exception queue, with a task for a named owner |
| A document is unmatched or below the confidence threshold | Review queue; the correction trains the model |
| The decision log entry cannot be written | The action does not proceed |
| A ledger write fails | An incident is raised; no entry is discarded |
| Access outside the authority matrix | Refused and recorded; emergencies use break-glass with approval |
| An ACE batch is late or missing | The case list waits and shows the last completed business date; the data steward is alerted; no Workbench catch-up load runs |

## 3.5 Rule governance

- Every rule, limit, threshold, template, name, queue, role, timer and route is a versioned data row, changed by a validated load with no code release (DT02).

- A load is checked for schema, overlapping rows, unreachable rows, a missing default row and a set of test cases. A load that fails a check is refused.

- Each version carries a valid from date, author and approver, and the previous version is restored by one action. The center of excellence analyst loads; the risk and model risk officer approves. One person may not hold both roles.

- A policy owner decides a policy change. The Workbench applies it as a new data version.

- Epic 1 loads allocation, assignment and transfer rules only (DL24).

# 4. Process and ownership

The process architecture has 19 L1 processes, 84 L2 sub-processes and 247 L3 processes. Epic 1 touches these L3 processes.

| L3 | L3 process | Today | After Epic 1 | Business owner |
|---|---|---|---|---|
| 06.1.1 | Transfer case and history from EFS | Weekly file at day 91 | Case created by rule at 90 days past due | Recovery Strategy with Risk |
| 06.1.2 | Track prescription deadlines | No date on a shared case record | Set at creation from the legal periods table | Recovery Strategy with Risk; Legal counsel |
| 18.3.2 | Allocate work by rule | By hand from team lists | By rule, rebalanced daily | Shared operations |
| 13.1.1 to 13.1.4 | Read, classify, check and attach documents | Kept outside the case | One intake; attached without a person | Shared operations; Legal |
| 13.2.1 | Generate letters from templates | Typed from case files | Generated from approved templates | Shared operations; Legal counsel |
| 13.3.1 | Apply retention rules | No class per document | Retention class; write-once legal types | Compliance |
| 14.2.2, 14.2.3, 14.2.5 | Write and release rules; manage org, teams and queues | No rule tables; 650 codes | Versioned data with validation and rollback | Center of excellence |
| 15.4.1, 15.4.3 | Reconcile to ALS; fix reconciliation breaks | No single list | Daily, zero tolerance, reason codes | Data steward and data product owner |
| 16.5.1 | Apply PDPA access by role | Set per application | Matrix as data; masking; access log | Compliance |
| 17.2.1 | Record one log entry per decision | In email | Hash-chained decision log | Center of excellence |

# 5. Constraints

## 5.1 Policies and regulation

- Personal Data Protection Act: personal data masked by role and every read logged. Retention and masking per data product and document type come from Compliance (DL26); until then every personal field stays masked.

- Records retention and legal hold: legal document types are held write-once, and a legal hold stops deletion. Compliance and Legal sign a records management position before the first production release.

- Delegation of authority follows Regulation กกค.540031 as amended by กกค.690070, loaded as reference data (DL18).

## 5.2 Systems and architecture

- Built inside ACE as a modular monolith with programmatic workflow; ACE sign-in, access control and audit are reused (DT07 to DT09).

- Source data arrives through ACE ingestion. The Workbench reads it through read-only views and holds no load, staging or tracker table (D-RCV-35, ADR-010; DT12 superseded). There is no real-time feed today; same-day needs are named under DL06.

- The document hub is the system of record for recovery documents (DT06).

- Partner access needs an architecture change with one to three months lead time (DL03). No partner uses Epic 1.

- Kanban delivery with a sponsor progress review every two weeks. Build from 2 November, SIT 16 to 20 November, UAT 23 to 27 November. A requirement that fails is switched off by its feature flag and the release goes ahead (DL34 sets the window).

# 6. Dependencies

## 6.1 Teams, systems and data

| ID | What is needed | From | Needed by | Decision | Decision owner, date |
|---|---|---|---|---|---|
| DEP-01, 02 | Recovery module place, merge rules and code owners in ACE | ACE team | 2 Nov | DL05, DL04 | K. Pipat, 29 Oct; K. Book, 29 Oct |
| DEP-03 | DEV and SIT deployment slots | ACE team | 6 Nov | DL35 | K. Tee, 6 Nov |
| DEP-05 | Monthly release window | SCB IT | 13 Nov | DL34 | SCB IT, 30 Oct |
| DEP-14 | ACE batch business date record (ace_batch_run) for account, payment and customer data, in addition to the existing ACE ingestion | ACE team | 21 Nov | D-RCV-35, DL43 | ACE team lead; scope 15 Nov, date under DL43 |
| DEP-15 | ACE additions for CCMS, SVAF, AMIS, RPS, WIN, GL, COLLINS, SCBPDM, NLEADS, EasyApp and Entra ID (RWB-ACE-001) | ACE team | 21 Nov | D-RCV-35, DL43 | ACE team lead; scope 15 Nov, date under DL43 |
| DEP-16 | Masked test data in SIT and UAT | Data engineering | 13 Nov | DL26 | Compliance, 13 Nov |
| DEP-18 | Entra ID groups for the Workbench roles | SCB IT security | 9 Nov | DL40 | SCB IT security, 6 Nov |
| DEP-20 | Model endpoint and agent platform | Enterprise AI | 16 Nov | DL33 | CTO with Enterprise AI, 30 Oct |
| DEP-22 | OCR and extraction for the first document types | Autonomous Ops | 16 Nov | DL19 | Business lead with Legal, 6 Nov |
| DEP-26 | Business testers named | Business lead | 6 Nov | DL09 | K. Tee with K. Jao, 31 Oct |

The Workbench reads ACE through the 30 recovery.v_ace_* views. It creates no inbound load, staging table or tracker load. The ACE team adds 14 tables, 12 columns and 80 source fields under RWB-ACE-001; the view grant, the four extension tables and the boundary test are in RWB-E1-069.

## 6.2 Open decisions

The build uses the stated answer until the owner decides. Dates are 2026.

| ID | Question | Answer the build uses | Owner | By |
|---|---|---|---|---|
| DL01 | Who grants access? | The application owner; role owners approve each grant | K. Tee | 28 Oct |
| DL02 | Who owns the application? | The Tribe lead; the ACE team as technical custodian | K. Tee with K. Bell | 28 Oct |
| DL15 | Base for sizing? | 28,119 accounts; 3,110 new a month; 15 percent growth | Data lead | 6 Nov |
| DL16 | Entry at 90 or 91 days past due? | 90 days past due | Business lead | 6 Nov |
| DL17 | What counts as one case? | One per customer per product | Product owner with the solution architect | 6 Nov |
| DL22, DL23 | Service levels per status; caseload cap and queue order | Loaded as parameters when supplied | Business lead; Product owner | 13 Nov |
| DL25 | Reconciliation tolerance? | Zero | Data lead | 6 Nov |
| DL27 | Storage, backup, legal hold, e-discovery? | ACE storage with write-once container and bank backup | Solution architect with Compliance | 13 Nov |
| DL28 | Owner of letter templates? | The document module; Legal approves wording | Product owner | 13 Nov |
| DL29 | Which EFS contact outcomes enter the ledger? | A named list for the collection period | Data lead with the business lead | 13 Nov |
| DL39 | Roles with real users per release? | Administration roles at Epic 1 | Business lead | 20 Nov |
| DL43 | Does the ACE team accept the RWB-ACE-001 scope and its dates? | Assume the scope is accepted; dates to confirm, and Tier 2 features stay behind their flags until the additions land | ACE team lead | 21 Nov |

## 6.3 Support needed from the business

| Support | From | When |
|---|---|---|
| Confirm the count of accounts at 90 days past due by product and month | Data lead | 6 Nov |
| Confirm the tracker retirement list and cutover owners | Team managers | Before cutover |
| Provide allocation rows, caseload caps and service levels as data | Business lead, product owner | 13 Nov |
| Approve the demand, recall and guarantor notice wording | Legal counsel | Before UAT |
| Test two to three hours a day, then run UAT | Business testers | Build; 23 to 27 Nov |

# 7. Success measures

Read from the Workbench records and the decision log. The benefit check (gate G6) is on 31 December 2026.

| Measure | Baseline | Target | By when | Owner |
|---|---|---|---|---|
| Case list reconciled to ALS through v_ace_account | No single case list | Zero variance five business days in a row; no break open beyond one day | 31 Dec 2026 | Data steward and data product owner |
| ACE batches complete on time, and the case list shows the latest business date | Baseline from the first month live | 99 percent | From 30 Nov 2026 | Data steward and data product owner |
| New cases assigned by rule | By hand from team lists | 100 percent | 31 Dec 2026 | Team managers |
| Team Excel and SharePoint lists retired | 40.5 percent of mapped steps in Excel | All retired or out of scope; retired after ten clean days in parallel under the Cutover and Go Live Plan retirement procedure (U5) | 13 Dec 2026 | Program manager |
| Documents attached to their case without a person | Baseline from the first month live | All through one intake; unmatched in the review queue | 31 Dec 2026 | Business lead with Legal |
| Rule changes made by data load | No rule tables | 100 percent, no code release | 31 Dec 2026 | Center of excellence |
| Case events in the decision log with the rule version | Recorded in email | 100 percent; chain checked daily | From 30 Nov 2026 | Center of excellence |
| Workbench inbound loads and staging tables | 20 tables and the load estate today | None; every source read through recovery.v_ace_* | From 30 Nov 2026 | Platform administrator |

# 8. Business scope approval

The Epic 1 design was signed on 23 October 2026 (gate G1). This approval confirms the business scope before the build starts on 2 November 2026.

| Role | Approves | Status |
|---|---|---|
| Sponsor | Problem, outcome, scope and success measures | To approve |
| Business lead | Entry rule, exclusions, statuses, allocation rules and service levels | To approve |
| Product owner | Scope boundary and the story set | To approve |
| Data lead | Baseline figures and the reconciliation measure | To approve |
| Risk | Exclusion list, delegation of authority table and rule governance | To approve |
| Compliance | Masking, retention, access log and records management | To approve |
| Legal counsel | Document types, legal periods, legal hold and notice templates | To approve |
| Tribe lead | Process ownership and constraints | To approve |

# 9. How the user stories follow

Epic 1 meets 77 program requirements through 67 stories in Recovery Workbench User Stories Epic 1. Each story carries its acceptance criteria and test cases.

| Requirement group | Requirement IDs | Count |
|---|---|---|
| Recovery data | REQ-RDF-001 to 013 | 13 |
| Case and workflow core | REQ-CWC-001 to 016 | 16 |
| Document hub | REQ-DCM-001 to 011, 014 to 016, 020 | 15 |
| Decision record and integration | REQ-DRI-001 to 011 | 11 |
| Access and authority | REQ-ACA-001 to 010 | 10 |
| Outbound contact and case view | REQ-OCC-001 to 002, 007 | 3 |
| Interaction ledger | REQ-ILG-001 to 008, 014 | 9 |

| Module | Stories | Must | Points |
|---|---|---|---|
| P1 Recovery data engine | 19 | 17 | 87 |
| P2 Integration | 4 | 3 | 21 |
| P3 Case and workflow | 15 | 13 | 114 |
| P4 Access and administration | 4 | 4 | 16 |
| P5 Document hub | 12 | 10 | 62 |
| P6 Communications | 4 | 2 | 16 |
| P7 Decision center and log | 2 | 2 | 11 |
| P9 Reporting | 1 | 1 | 5 |
| P10 Agent runtime | 6 | 5 | 42 |
| Total | 67 | 57 | 374 |

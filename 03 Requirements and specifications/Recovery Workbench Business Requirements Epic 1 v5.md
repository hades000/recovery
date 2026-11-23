SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Recovery Workbench

Business requirements, Epic 1

| Item | Detail |
|---|---|
| Document | Recovery Workbench business requirements, Epic 1 |
| Version | 5 |
| Date | 22 November 2026 |
| Prepared by | Henka Group |
| Release | 30 November 2026 (tentative) |
| Structure | ISO/IEC/IEEE 29148, until the SCB X requirement template is adopted (DL13) |
| Change log | below, one row per version |
| Change | Version 5 is the D-RCV-60 microservice realignment. Sections 1 to 7 are copied from version 4 with every key, number, requirement, role and date unchanged; the release date is marked tentative. Section 8 adds the delivery model: 19 service epics inside ACE, four waves, platform and integration epics, and contract-first delivery. Section 9 adds the trace from each business requirement to its service epic and business epic. No business requirement is rewritten, added or removed by this version. Three delivery positions are recorded rather than edited into the text: RWB-E1-014 is retired by D-RCV-60, and RWB-E1-029 and RWB-E1-048 were cancelled before this run. Four decision-owner cells in section 7 named people; they carry the register placeholder of Template and Rules section R9 (GAP-1458; ASM-2559) and their question and answer cells are unchanged. |

| Version | Date | Change | Owner |
|---|---|---|---|
| 4 | 15 November 2026 | Version 4 applies D-RCV-35 and ADR-010, which supersedes ADR-005. Section 3.1 states the four-tier read model, the 30 views, the dictionary, reconciliation and freshness position; section 3.2 is outbound only. Section 4 marks the removed requirements and re-words the data requirements, section 7 records DL43, and the requirement and role counts follow. RWB-E1-069 and RWB-ACE-001 are added; removed requirements keep their keys. Other sections are unchanged. | Henka Group |
| 5 | 22 November 2026 | D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash. Sections 1 to 7 unchanged, release marked tentative, section 8 delivery model and section 9 trace added. | Henka Group |

# 1. What this epic delivers

Epic 1, Foundation 1, releases on 30 November 2026 (tentative).

One case list for every account at 90 days past due or more, reconciled to the core bank. Documents found by case. The decision log store. A read-only case record view. Allocation, assignment and transfer by rule, with timers and prescription dates, and no workflow screens.

| Measure | Value |
|---|---|
| Requirements at development detail | 61 |
| Must | 51 |
| Program requirements this epic meets | 75 |


# 2. Who benefits

| Who | Requirements that serve them |
|---|---|
| A product owner | 8 |
| A case owner | 8 |
| A litigation officer | 8 |
| A team manager | 7 |
| A developer | 6 |
| A document hub owner | 6 |
| An AI product owner | 5 |
| A data product owner | 4 |
| A center of excellence analyst | 2 |
| The Tribe lead | 1 |
| The case workflow module | 1 |
| A head of recovery | 1 |
| A security reviewer | 1 |
| An operations engineer | 1 |
| A business analyst | 1 |
| The ACE team lead | 1 |


# 3. Requirements at development detail

Each requirement is one backlog story. The requirement states what the Workbench does, the benefit states what changes for the user, and the scenarios are the acceptance criteria in the story.

## 3.1 P1 Recovery data engine

P1 is the read-only data position of the recovery module. ACE ingests every source and holds it; the Workbench reads it through the 30 SELECT-only recovery.v_ace_* views and holds only Workbench-owned data: the case, its decisions, reference data and the extension tables (D-RCV-35, ADR-010). Links to ACE records use business keys, with no foreign key into ACE.

The read model has four tiers. Tier 1 is 22 ACE tables that exist today; the recovery data in them is read through 16 Section A views, and the Workbench never alters them. Tier 2 is 14 ACE tables and 12 columns the ACE team adds under RWB-ACE-001 for 80 source fields; the new tables are read through 14 Section B views and the new columns extend v_ace_account, v_ace_customer and v_ace_efs_action. Tier 3 is 4 Workbench extension tables keyed by ACE business keys. Tier 4 is 88 retained Workbench tables. The recovery schema is 92 tables; with the 30 views the dictionary holds 122 sys_objects and 1,366 sys_fields.

P1 delivers the recovery tables, the extension tables, the two view migrations, the data dictionary, the daily reconciliation of the case list to v_ace_account (REC-01 to REC-05) and the freshness stamp read from the ACE batch record (ace_batch_run through v_ace_batch_status). Section A ships with RWB-E1-069; Section B waits on the ACE additions in RWB-ACE-001 (DL43). The 20 copy, load and tracker tables leave the recovery schema. Source content is read through the views, Workbench-only facts sit in the extension tables, and the trackers are retired through the Cutover plan. A requirement for an inbound load, a data quality check on load or a tracker is removed. It keeps its key and names its later home.

| Key | Requirement | What the Workbench does | For | User benefit | Priority | Tests |
|---|---|---|---|---|---|---|
| RWB-E1-001 | Recovery tables for the 14 data products | The recovery schema in the ACE database for the 14 data products: 92 tables, being 88 retained Workbench tables and 4 extension tables keyed by ACE business keys, with a data dictionary and one system of record, read path and owner per product. Source data is read through the 30 ACE views and is never copied. | A data product owner | Every product has one source and one read path | Must | 3 |
| RWB-E1-002 | Case list v1 with case ID, owner and queue | One case list with case ID, account, product, stage, status, owner, queue, route, balance and days past due for every 90 days past due or more account, read from the ACE account view (v_ace_account) each day after the ACE batch completes, and available in Power BI | A team manager | Every team works from one list | Must | 3 |
| RWB-E1-003 | ALS daily extract load | Removed by D-RCV-35 (U1). ACE ingests ALS, and the Workbench reads v_ace_account and v_ace_payment. Later home: ACE ingestion | A data product owner | - | Removed | - |
| RWB-E1-004 | EFS extract load | Removed by D-RCV-35 (U1). ACE ingests EFS, and the Workbench reads v_ace_efs_action and v_ace_efs_assignment. Later home: ACE ingestion | A data product owner | - | Removed | - |
| RWB-E1-005 | Excel and SharePoint inventory | Removed by D-RCV-35 (U5). Excel and SharePoint trackers leave system scope. Later home: the Cutover plan | A program manager | - | Removed | - |
| RWB-E1-006 | Data quality rules v1 | Removed by D-RCV-35 (U1). Data quality checks on source data run in ACE ingestion. The daily gate moves into RWB-E1-015. Later home: ACE ingestion checks | A data product owner | - | Removed | - |
| RWB-E1-009 | CCMS and SVAF loads | Removed by D-RCV-35 (U1). ACE ingests CCMS and SVAF through RWB-ACE-001, and the Workbench reads v_ace_collateral, v_ace_collateral_detail and v_ace_valuation. Later home: ACE ingestion | A data product owner | - | Removed | - |
| RWB-E1-010 | Excel and SharePoint loads | Removed by D-RCV-35 (U5). No tracker is loaded. Later home: the Cutover plan | A data product owner | - | Removed | - |
| RWB-E1-011 | Reconciliation and data quality report | A daily reconciliation of the case list to the ACE account view (v_ace_account), with the variance and the results of reconciliation rules REC-01 to REC-05 in one Power BI report | A team manager | Everyone sees whether today's list can be trusted | Must | 2 |
| RWB-E1-012 | Retire local copies | Removed by D-RCV-35 (U5). Each team retires its tracker through the Cutover plan. Later home: the Cutover plan | A program manager | - | Removed | - |
| RWB-E1-014 | Decision log copy to the data lake | The decision log copied to the data lake each night and a retention rule per data product and table | A center of excellence analyst | Reporting reads the log without touching the live log and nothing is kept longer than its rule | Should | 2 |
| RWB-E1-015 | Freshness stamp per data product | Every data product row to carry the business date and load time of its ACE batch, taken from the ACE batch record (ace_batch_run, read through v_ace_batch_status), exposed to every consumer and shown on the case record view. The case list waits for a completed ACE batch and shows the last completed business date | A data product owner | Every decision input states how old it is and stale facts are visible | Must | 3 |
| RWB-E1-016 | Access control per data product and catalog entries | Read access to each data product granted by role through the read-only views, PDPA fields tagged, every read logged, and a catalog entry per product with owner, system of record (ACE, ingested from the named source), freshness and fields | A data product owner | Personal data is read only by the roles that need it and every product is findable | Must | 3 |
| RWB-E1-017 | Retention and archive rule for the data store | A retention rule per data product and table, held as reference data, applied by a job that archives rows past their rule and logs the action | A data product owner | The store holds what the policy allows and nothing older | Should | 3 |
| RWB-E1-064 | Data dictionary for the 14 data products | Every field in the 14 data products typed, sourced and owned. The dictionary covers the Workbench tables, the 4 extension tables and the 30 ACE views: 122 objects and 1,366 fields | A business analyst | A data contract can be agreed with the ACE team for every field the Workbench reads | Must | 3 |
| RWB-E1-065 | Sandbox database with synthetic recovery data | A sandbox database holding the ACE schema, the ACE views and synthetic recovery data | A developer | I can build and test before the ACE additions and the real data are available | Must | 3 |
| RWB-E1-066 | Interaction ledger store and writer | Every contact, letter, promise, payment and hand-over on the case written to one ledger when it is recorded | A case owner | The history of the case is never assembled after the fact | Must | 4 |
| RWB-E1-067 | Every Workbench action into the interaction ledger | Every action the Workbench takes on my case written to the ledger when it is taken | A case owner | I can read the history without assembling it from four systems | Must | 3 |
| RWB-E1-068 | Interaction ledger read interface | To read a case's ledger in one ordered sequence | A case owner | I can see what has happened to it before I decide anything | Must | 3 |
| RWB-E1-069 | Read-only ACE source views, grants and boundary rule | The 30 SELECT-only recovery.v_ace_* views: 16 over ACE tables that exist today (Section A) and 14 over the ACE additions (Section B, when RWB-ACE-001 lands). The 4 extension tables. SELECT on the views for the recovery service identity and nothing else. A test that fails the build on a direct read of a public table, a write to ACE or a foreign key into ACE | A developer | Source data has one copy and one read path, and a wrong read fails the build | Must | - |
| RWB-ACE-001 | ACE DB additions for the Recovery Workbench | Not built by the Workbench. The ACE team adds 14 tables and 12 columns to the ACE database for the 80 source fields ACE does not hold, with the ACE batch record ace_batch_run, all filled by ACE ingestion. The Section B views and the features that need them stay behind their flags until it lands (DL43) | The ACE team lead | The recovery module reads one copy of source data and no recovery load is built | Must | 8 |


## 3.2 P2 Integration

P2 is outbound only. It sends files and events and receives no source file: every inbound source lands in ACE through ACE ingestion and is read through the P1 views (D-RCV-35, U1; ADR-010).

P2 covers one adapter pattern for the WIN registered-mail notice file, the data lake and Power BI extract, the decision and outcome feed to COLLINS through the data lake, the debt buyer tape and the GL write-off event. It uses the ACE logging path to the SOC, and the transport used by the partner portal and the document hub. It also covers feature flags and the run books for Workbench jobs. No inbound file feed, file-load adapter, inbound run record or inbound sign-off remains.

| Key | Requirement | What the Workbench does | For | User benefit | Priority | Tests |
|---|---|---|---|---|---|---|
| RWB-E1-007 | Outbound integration adapters for files and events | One adapter pattern for every outbound file and event: the WIN registered-mail notice file, the data lake and Power BI extract, the decision and outcome feed to COLLINS through the data lake, the debt buyer tape and the GL write-off event, plus the transport used by the partner portal and the document hub, with checks, logging, retry and an exception queue. SOC and audit events leave through the ACE logging path, and no inbound file load runs in the Workbench. | A developer | Every outbound channel follows one pattern and no inbound source file enters the Workbench | Must | 3 |
| RWB-E1-047 | Feature flags for module release with a removal date | A feature flag service with flags defined as data (name, owner, environments, removal date) and read by every service at run time | A developer | A feature can be released dark and switched on without a deployment | Should | 3 |
| RWB-E1-051 | Legacy feed jobs on ADF and Control-M | Removed by D-RCV-35 (U1). No ADF or Control-M job carries recovery source data; ACE ingestion does. Later home: ACE ingestion | A data product owner | - | Removed | - |
| RWB-E1-056 | Run books and monitoring for every Epic 1 job | A run book for every Workbench scheduled job and service (purpose, schedule, owner, failure signs, restart steps, escalation) and monitoring for each. Source loads are ACE jobs and sit in the ACE run books | An operations engineer | Any Epic 1 job can be restarted by the operations team without the developer | Must | 3 |


## 3.3 P3 Case and workflow

| Key | Requirement | What the Workbench does | For | User benefit | Priority | Tests |
|---|---|---|---|---|---|---|
| RWB-E1-018 | Case ID issuance and case record v1 | Every 90 days past due or more account on one recovery case with a case ID (RW-YYYY-NNNNNN) issued at creation and never reused, a stage, a status and linked accounts, created by rule when an account reaches 90 days past due and is not excluded | A product owner | Every team, letter and document refers to one ID | Must | 6 |
| RWB-E1-019 | Roles, teams and queues as data | Roles, teams, queues, queue membership and capacity held as versioned reference data loaded from the Excel template | A product owner | The organization changes without a code release | Must | 3 |
| RWB-E1-020 | Allocation and assignment engine v1 | Each new case placed in a queue and assigned to a person by the allocation and assignment rule tables | A team manager | Nobody allocates cases by hand | Must | 4 |
| RWB-E1-021 | Transfer rules and engine v1 | Cases moved between queues and roles by the transfer rule table on stage change, route decided, timer expired, deviation raised or cleared, approval needed, document received, payment missed or manual request with a reason | A team manager | Hand-offs run without email | Must | 5 |
| RWB-E1-023 | Case record view v1, read only | One screen per case with case ID, accounts, arrears, owner, queue, stage, status, contact history and documents, read from the data products | A case owner | I stop searching files | Must | 3 |
| RWB-E1-028 | Service levels, timers, escalation and prescription dates | A service level per queue and status, a timer engine, warning and escalation to the next role by rule, and prescription dates from the legal periods table | A team manager | No case waits past its limit unseen | Must | 3 |
| RWB-E1-029 | Rule load, validation and rollback | An Excel template for the five rule tables, validation on load (schema, overlaps, unreachable rows, missing default, 50 test cases), load with a version, rollback by one call and a change log | A product owner | A rule change goes from template to production without a code release | Must | 4 |
| RWB-E1-030 | Daily rebalancing and queue measures | A daily job that moves unassigned and over-capacity cases by the assignment rules, with queue counts, ageing and service level breaches in Power BI | A team manager | Queues stay balanced and visible | Must | 3 |
| RWB-E1-031 | Queue and owner on the case list with filters | The queue and owner columns on the case list with filters by queue, team and status and an export | A team manager | I see my queues without a new screen | Must | 2 |
| RWB-E1-035 | Case record view v1.1 with documents and history timeline | A timeline on the case record view with contacts, documents, assignments, transfers and status changes in time order | A case owner | I see what happened to the case without asking | Should | 2 |
| RWB-E1-042 | Central configuration service and parameter catalog | Every environment setting and business parameter read from one configuration service, listed in a parameter catalog with name, type, default, owner, environment and where it is used | A developer | No value is hard-coded and every parameter has an owner | Must | 3 |
| RWB-E1-043 | Reference data service with versioned tables | Products, regions, exposure bands, roles, teams, queues, service levels, document types, templates, delegation of authority, legal periods and holidays held as versioned reference data with valid from, valid to, author and approver | A product owner | Business values change by a data release and not by code | Must | 3 |
| RWB-E1-044 | Database migrations versioned with parameterized schema names | Every schema change applied by a versioned migration (Flyway or Liquibase), one migration per story, forward-only in PROD, with schema names taken from parameters | A developer | The database in every environment is the sum of known migrations and nothing else | Must | 3 |
| RWB-E1-045 | Multi-product parameters for Mortgage, HP and SSME | Every product-specific value (entry rule, exclusion list, service levels, templates, exposure bands) keyed by product in the reference data | A product owner | A new product or a product change needs no code change | Must | 3 |
| RWB-E1-048 | Rule change audit report | The parameter change and rule change checklists (request, impact, test cases, approver, load, verify, rollback plan) in the Engineering Standards and followed for every change | A product owner | A configuration change is as controlled as a code change | Should | 2 |


## 3.4 P4 Access and administration

| Key | Requirement | What the Workbench does | For | User benefit | Priority | Tests |
|---|---|---|---|---|---|---|
| RWB-E1-022 | Sign-on with SSO, MFA and the first roles | To sign in with Entra ID SSO and see only the screens my role allows, with roles case owner, team lead, admin and read only | A case owner | Access is controlled from day one | Must | 3 |
| RWB-E1-037 | Role to permission matrix as data and PDPA field masking by role | The mapping of roles to screens, actions, data products and PDPA fields held as a versioned table, applied by every screen and API, with masking by role | A product owner | A change of rights is a data change and personal data shows only to roles that need it | Must | 3 |
| RWB-E1-038 | Delegation of authority table as reference data | The delegation of authority (who may approve what, by decision, amount band, product and exposure) held as a versioned table that the approval router reads | A head of recovery | Approval limits change by a data load and every approval can be checked against the limit that applied | Must | 3 |
| RWB-E1-039 | Access log into the decision log and break-glass admin | Every read of a case record and every export written to the decision log store, and a break-glass admin role granted for a limited time with approval and full logging | A security reviewer | Every access can be audited and emergency access is controlled | Must | 3 |


## 3.5 P5 Document hub

| Key | Requirement | What the Workbench does | For | User benefit | Priority | Tests |
|---|---|---|---|---|---|---|
| RWB-E1-024 | Document store and index | Every scanned document stored against its case with type, date, source and extracted fields, in a Blob store with a write-once container for legal types, searchable by case ID, type and date | A litigation officer | Documents are found by case | Must | 3 |
| RWB-E1-025 | Document types and fields agreed | The first six document types (demand letter, court notice, appraisal report, title deed, settlement agreement, guarantor notice) with their key fields agreed with Legal and NPA and held as reference data | A product owner | The OCR pipeline has a target | Must | 2 |
| RWB-E1-026 | Attach and search screen | To upload, see and search documents from the case record view | A case owner | The case file is complete | Must | 3 |
| RWB-E1-032 | Automatic attach from the OCR intake | Documents from the OCR intake attached to their case automatically when the case ID or account number is read, with unmatched documents sent to the review queue | A case owner | No document is filed by hand | Must | 3 |
| RWB-E1-033 | Search across cases | A search across all cases by document type, date range, extracted field and free text, with results limited to the cases my role may see | A litigation officer | A document is found in seconds without opening cases one by one | Should | 3 |
| RWB-E1-040 | Document checklist per case type as reference data | The required documents per case type and route held as a reference table that the case record view and the review queue read | A litigation officer | A missing document shows on the case without a person checking a list | Should | 3 |
| RWB-E1-041 | Retention classes and virus scan on intake | Every uploaded or scanned file checked for malware before storage, and a retention class per document type that the store applies | A document hub owner | The store holds only safe files and keeps each for the time the policy sets | Must | 3 |
| RWB-E1-049 | OCR pipeline on the Workbench document hub | Inbound scans read by the OCR service and output as text plus layout | A document hub owner | Extraction can start | Must | 3 |
| RWB-E1-050 | Document classification | Each scanned document classified into one of the six types with a confidence score | A document hub owner | It is attached to the right checklist | Must | 2 |
| RWB-E1-053 | Field extraction for the six types into the index | The key fields of each of the six types extracted and written to the document index with a confidence per field | A document hub owner | Documents are searchable by their content | Must | 2 |
| RWB-E1-054 | Review queue for low-confidence documents | A queue of documents with low classification or extraction confidence, each correctable in one screen, with the correction fed back to the labeled set | A litigation officer | No document is attached wrongly and the models improve | Must | 2 |
| RWB-E1-057 | Intake from branches, mailroom, partner SFTP and email | Scans from branch scanners and the mailroom, partner files by SFTP and attachments from the recovery mailboxes to enter the same OCR intake with the source recorded | A document hub owner | Every document path ends in the document hub | Must | 3 |


## 3.6 P6 Communications

| Key | Requirement | What the Workbench does | For | User benefit | Priority | Tests |
|---|---|---|---|---|---|---|
| RWB-E1-034 | Letter template management | A screen to upload a template version, record the Legal approval and set it current | A litigation officer | Templates are managed without a developer | Should | 2 |
| RWB-E1-046 | Template and merge field catalog as data | Letter and document templates and their merge fields held as versioned data with the Legal approval record | A litigation officer | A template change is a data release approved by Legal | Must | 3 |
| RWB-E1-052 | Notice generation v1 | Demand, recall and guarantor notices generated from approved templates with case data merged | A litigation officer | Letters are produced without re-keying | Must | 3 |
| RWB-E1-055 | Proof of delivery capture design with WIN | Generated notices sent to WIN for print and post, with the dispatch and proof-of-delivery status written back on the case | A litigation officer | The case shows what was sent and when it arrived | Should | 3 |


## 3.7 P7 Decision center and log

| Key | Requirement | What the Workbench does | For | User benefit | Priority | Tests |
|---|---|---|---|---|---|---|
| RWB-E1-008 | Decision log store v1, append only and hash chained | An append-only decision log store with the seven field groups and a hash chain | A center of excellence analyst | Every decision from Epic 1 is recorded and cannot be changed | Must | 4 |
| RWB-E1-027 | Decision log writer v1 | A writer that records case created, owner assigned, case transferred and document attached, with the rule ID and version used | The case workflow module | The first records exist in Epic 1 | Must | 2 |


## 3.8 P9 Reporting

| Key | Requirement | What the Workbench does | For | User benefit | Priority | Tests |
|---|---|---|---|---|---|---|
| RWB-E1-013 | Baseline measures | Cases by route, age and queue, realized recovery, time in stage and TAT per route published as the baseline with definitions agreed with the Tribe | The Tribe lead | Every later epic is measured against the same baseline | Must | 3 |


## 3.9 P10 Agent runtime

| Key | Requirement | What the Workbench does | For | User benefit | Priority | Tests |
|---|---|---|---|---|---|---|
| RWB-E1-058 | Agent platform set-up [E1a] | The LLM gateway, prompt and policy store, guardrail checker and evaluation suite deployed in the Workbench namespace | An AI product owner | Agents can be built and tested | Must | 5 |
| RWB-E1-059 | Case intake agent in shadow [E1b] | The case intake agent to build a case file summary and flag gaps for Epic 1 cases in shadow mode | An AI product owner | It is scored before anyone sees it | Must | 2 |
| RWB-E1-060 | Extraction evaluation [E1c] | Field extraction for the six document types evaluated against the labeled sample | A document hub owner | The extraction approach (OCR template, LLM or both) is chosen | Must | 2 |
| RWB-E1-061 | Intake agent evaluation and L1 proposal [E2a] | The evaluation report of the case intake agent with the proposal to run it at L1 in Epic 2 | An AI product owner | The autonomy step is decided on evidence | Must | 2 |
| RWB-E1-062 | Deviation screening agent in shadow [E2b] | The deviation screening agent flagging X1 to X7 from data, call notes and documents in shadow on Epic 1 data | An AI product owner | The Epic 2 deviation flags start from a scored agent | Must | 2 |
| RWB-E1-063 | Agent monitoring dashboard v1 [E2c] | A dashboard with acceptance, override, latency and cost per agent and version | An AI product owner | Every agent is watched from its first shadow run | Should | 2 |


# 4. Program requirements met in this epic

The table carries the 77 program requirements this epic meets, of which 75 are live and 2 are removed by D-RCV-35 (U5). Removed requirements keep their IDs and name their later home. The data requirements are read from ACE through the 30 views; the 20 copy, load and tracker tables are gone and no source load job remains.

| ID | Requirement | Priority | Owner |
|---|---|---|---|
| REQ-RDF-001 | Recovery data is organized in 14 data products, each with exactly one named system of record, one read path and one named owner. Source data is read from ACE through read-only views and is not copied. | Must | Data steward and data product owner |
| REQ-RDF-002 | Account balance, arrears, payments and classification for every account at 90 or more days past due are read from ACE and are current to the previous working day of the ACE batch. | Must | Data steward and data product owner |
| REQ-RDF-003 | Collections contact history, promises and case status from EFS are read from ACE, which ingests them, so that the case carries what happened before day 90. | Must | Data steward and data product owner |
| REQ-RDF-004 | Collateral records and appraisal values are available on the case without a person looking them up in CCMS or SVAF. ACE ingests them under RWB-ACE-001. | Must | Data steward and data product owner |
| REQ-RDF-005 | Removed by D-RCV-35 (U5). Excel and SharePoint trackers leave system scope. Later home: the Cutover plan lists and retires them. | Removed | Program manager |
| REQ-RDF-006 | Removed by D-RCV-35 (U5). No tracker file is loaded. Later home: the Cutover plan retires each local copy with the owner's confirmation and a read-only archive. | Removed | Data steward and data product owner |
| REQ-RDF-007 | The case list reconciles daily to the count of accounts at 90 or more days past due in v_ace_account, which ACE ingests from ALS, with no variance (DL25), and every business key on a Workbench table resolves to an ACE row. | Must | Data steward and data product owner |
| REQ-RDF-008 | Data quality checks on source data run in ACE ingestion (RWB-ACE-001). The Workbench reports reconciliation breaks, referential completeness and its quality measures, each break with a reason visible to the data product owner. | Must | Data steward and data product owner |
| REQ-RDF-009 | Every data product carries a freshness stamp from the ACE batch record, and every decision records the freshness of the data it used. | Must | Center of excellence |
| REQ-RDF-010 | Access to each data product is controlled per role through the read-only views, and personal data is masked by role in line with PDPA. | Must | Compliance |
| REQ-RDF-011 | Every data product has a catalog entry stating its definition, owner, system of record (ACE, ingested from the named source), refresh cycle and retention. | Must | Data steward and data product owner |
| REQ-RDF-012 | Baseline measures for cases by route, age and queue, realized recovery, time in stage and turnaround per route are published, with definitions agreed by the Tribe. | Must | Center of excellence |
| REQ-RDF-013 | Workbench recovery records carry a retention and archive rule by record class; ACE data is retained by ACE. | Should | Compliance |
| REQ-CWC-001 | Every account at 90 or more days past due that is not excluded carries one recovery case, created by rule from the daily ACE batch. | Must | Business lead |
| REQ-CWC-002 | Each case carries a case ID in the form RW-YYYY-NNNNNN, issued once, never reused, and printed on every letter and document. | Must | Business lead |
| REQ-CWC-003 | One case covers one customer and one product, with its accounts linked to it. | Must | Business lead |
| REQ-CWC-004 | Exclusion rules for deceased, fraud, bankruptcy, an active restructure plan and an open dispute are held as data and applied at creation. | Must | Risk |
| REQ-CWC-005 | The case state model covers stage, status within stage, route and the deviation flags X1 to X7, and a case holds exactly one state at a time. | Must | Business lead |
| REQ-CWC-006 | Roles, teams, queues, queue membership and capacity are held as versioned reference data and change without a code release. | Must | Center of excellence |
| REQ-CWC-007 | Every new case is placed in a queue and assigned to a person by rule, and no case is allocated by hand as a matter of course. | Must | Team manager |
| REQ-CWC-008 | Allocation rules read product, region, exposure band, stage, route, deviation flag, customer segment and collateral type, apply first match, and always have a default row. | Must | Center of excellence |
| REQ-CWC-009 | Assignment rules support round robin, lowest load and a named owner for continuity, with a capacity cap and an overflow queue. | Must | Team manager |
| REQ-CWC-010 | Cases move between queues and roles by transfer rules on stage change, route decision, timer expiry, deviation raised or cleared, approval needed, document received, payment missed, and manual request with a reason code. | Must | Center of excellence |
| REQ-CWC-011 | Service levels per queue and status, warning thresholds and escalation targets are held as data, and a breach raises an event without moving the case. | Must | Team manager |
| REQ-CWC-012 | Prescription dates are set from the legal periods table at case creation and are visible at all times. | Must | Legal counsel |
| REQ-CWC-013 | A rule change goes from a validated template load to production with a version stamp and no code release, and rolls back to the previous version by one call. | Must | Center of excellence |
| REQ-CWC-014 | Rule loads are validated for schema, overlapping rows, unreachable rows, a missing default and a set of test cases before they take effect. | Must | Center of excellence |
| REQ-CWC-015 | Unassigned and over-capacity cases are rebalanced daily, and queue counts, ageing and service level breaches are reported. | Must | Team manager |
| REQ-CWC-016 | Every allocation, assignment, transfer and timer event is logged with the rule ID and the rule version that caused it. | Must | Center of excellence |
| REQ-DCM-001 | Every document is stored against its case with type, date, source and extracted fields. | Must | Legal counsel |
| REQ-DCM-002 | The Workbench document hub is the system of record for recovery documents. No other store holds the authoritative copy. | Must | IT lead |
| REQ-DCM-003 | Legal document types are held in a write-once container that cannot be altered or deleted. | Must | Legal counsel |
| REQ-DCM-004 | The document types and their key fields are agreed and signed before the extraction pipeline is built. | Must | Business lead with Legal |
| REQ-DCM-005 | Inbound documents are classified into one of the agreed types with a confidence score, and anything below the threshold goes to a review queue. | Must | Autonomous Ops |
| REQ-DCM-006 | Fields are extracted into the index for the agreed document types, in Thai and in English. | Must | Autonomous Ops |
| REQ-DCM-007 | A classified document attaches to its case without a person doing it. | Must | Autonomous Ops |
| REQ-DCM-008 | Documents are searchable by case ID, type and date from the case record view. | Must | Case owner |
| REQ-DCM-009 | Documents arrive from branches, the mailroom, partner file transfer and email through the same intake. | Must | Autonomous Ops |
| REQ-DCM-010 | Every document carries a retention class, and intake runs a virus scan before the document is stored. | Must | Compliance |
| REQ-DCM-011 | A document checklist per case type is held as reference data so that a missing document is visible. | Must | Center of excellence |
| REQ-DCM-014 | New scope. Document storage is sized, provisioned and costed for the inbound volume and its growth, and the cost belongs to the program's running cost. | Must | Solution architect |
| REQ-DCM-015 | New scope. Documents are backed up on a stated schedule, and a restore is tested before the first production release and at each subsequent release. | Must | IT lead |
| REQ-DCM-016 | New scope. A legal hold applied to a case or a document stops deletion and expiry for as long as the hold is in place, overriding the retention class. | Must | Legal counsel with Compliance |
| REQ-DCM-020 | New scope. The hub carries a records management position signed by Compliance and Legal covering storage, backup, legal hold, discovery and disposal. | Must | Solution architect with Compliance |
| REQ-DRI-001 | Every decision writes one record holding case and decision, the rule, model, agent and prompt versions, an inputs snapshot, the recommendation, the approval, the actions taken and the outcome. | Must | Center of excellence |
| REQ-DRI-002 | The decision log is append only. A record cannot be changed or deleted, and a correction is a new record naming the one it corrects. | Must | Compliance |
| REQ-DRI-003 | The decision log is hash chained, and the chain integrity is checked every day with a break reported to Compliance the same day. | Must | Compliance |
| REQ-DRI-004 | Records are written from Epic 1 for case creation, owner assignment, case transfer and document attachment. | Must | Center of excellence |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written. | Must | Center of excellence |
| REQ-DRI-006 | No component calls a system of record directly. Source data is read from the ACE database through the read-only recovery.v_ace_* views, and leaves through paths ACE already has (D-RCV-35, ADR-010). | Must | Solution architect |
| REQ-DRI-007 | The integration adapters log every outbound file and event, retry on a defined schedule, and place anything that fails after the retry limit in an exception queue with a task for a named owner. | Must | Platform administrator |
| REQ-DRI-008 | Data from other systems reaches the Workbench only through ACE ingestion and the ACE views. Interfaces that need same-day data are named under DL06 before any is built. | Must | Solution architect |
| REQ-DRI-009 | The decision log is copied to the data lake copy daily for reporting, with row counts matched. | Must | Data steward and data product owner |
| REQ-DRI-010 | A parameter catalog and a configuration service hold every threshold, limit and name, versioned, changed without a code release. | Must | Center of excellence |
| REQ-DRI-011 | A reference data service holds every versioned table with its valid from and valid to dates, author and approver. | Must | Reference data administrator |
| REQ-ACA-001 | Every user signs on through Entra ID single sign-on with multi-factor authentication. | Must | Security administrator |
| REQ-ACA-002 | Roles are held as data, and a role change takes effect without a code release. | Must | Security administrator |
| REQ-ACA-003 | The role to permission matrix is held as data and is the only source of what a role may see and do. | Must | Security administrator |
| REQ-ACA-004 | The delegation of authority table is held as reference data and sets every approval limit. | Must | Risk with Credit |
| REQ-ACA-005 | Personal data is masked by role on every screen and in every agent call. | Must | Compliance |
| REQ-ACA-006 | Every read of the case store, the document store and the data lake copy is written to the access log. | Must | Compliance |
| REQ-ACA-007 | Access requested outside the authority matrix is refused and the refusal is recorded. | Must | Security administrator |
| REQ-ACA-008 | A break-glass path exists for an emergency, needs its own approval, and writes to the access log. | Must | Security administrator |
| REQ-ACA-009 | A user sees only the cases and queues their role and scope allow. | Must | Security administrator |
| REQ-ACA-010 | Agents run under service identities and are subject to the same role checks as people. | Must | Platform administrator |
| REQ-OCC-001 | Notices are generated from templates approved by Legal, with merge fields from case data and no re-keying. | Must | Legal counsel |
| REQ-OCC-002 | Letter templates are versioned, and the Legal approval is recorded against the version. | Must | Legal counsel |
| REQ-OCC-007 | The case record view shows account, arrears, owner, queue, stage, status, route, timers, contact history, promises, documents and decisions on one screen. | Must | Case owner |
| REQ-ILG-001 | One ledger holds every interaction on a case, and no other record is the authoritative history of what happened with the customer. | Must | Case owner |
| REQ-ILG-002 | Every entry carries the case ID, the event, the timestamp, the actor and the source that produced it. | Must | Case owner |
| REQ-ILG-003 | Entries carry the channel, who or what was reached, and the outcome, where the interaction had one. | Must | Case owner |
| REQ-ILG-004 | An offer, a promise, a payment or a hand-over made during an interaction is recorded against that interaction. | Must | Case owner |
| REQ-ILG-005 | Every action the Workbench takes on a case writes to the ledger as it happens: case creation, allocation, transfer, escalation, document attachment and decisions taken. | Must | Center of excellence |
| REQ-ILG-006 | The ledger reads back in one ordered sequence, filterable by channel, actor and date range, through one interface. | Must | Case owner |
| REQ-ILG-007 | The same event arriving twice with the same key produces one entry, and the repeat is counted. | Must | Platform administrator |
| REQ-ILG-008 | A ledger write that fails raises an incident. An entry is never discarded, because a ledger with silent gaps is trusted and wrong. | Must | Platform administrator |
| REQ-ILG-014 | Personal data in the ledger is masked by role on the same rules as the case record. | Must | Compliance |


# 5. Support needed from users

The epic releases on time only if the business gives the support below during the build.

| Support | From | When |
|---|---|---|
| Confirm the count of accounts at 90 days past due by product and month | Data lead | 6 Nov |
| Confirm the data dictionary sources and owners for each data product | Data steward and data product owner | During the build |
| Agree the document types and fields the document hub reads | Business lead with Legal | 6 Nov |
| Approve the wording of the demand, recall and guarantor notice templates | Legal counsel | Before UAT |
| Provide the allocation rows, caseload caps and service levels as data | Business lead and product owner | 13 Nov |
| Set retention and masking per data product and document type | Compliance | 13 Nov |
| Name the Entra ID groups for the Workbench roles | SCB IT security | 6 Nov |
| Test with the squads during the build and run UAT in the week before release | Business testers | Two to three hours a day, then UAT |
| Draft Thai names for fields, labels and messages one epic ahead | Business lead with Legal and Compliance | From 5 Nov |


Excel and SharePoint trackers are retired through the Cutover plan (U5).

# 6. Acceptance

- Business testers see each requirement working during the build and confirm it against its scenarios.

- SIT runs for one week before the release, and UAT for one week, against the business scripts.

- The business lead signs the UAT exit. A requirement that fails has its feature flag switched off and the release goes ahead without it.

- The product owner accepts each story against its acceptance criteria.

# 7. Open decisions for this epic

DL43 is new and open. The other decisions keep their v3 answers, with the wording changed where D-RCV-35 supersedes the COLLINS route or the read and write position.

| Decision | Question | Answer the build uses until decided | Owner | Needed by |
|---|---|---|---|---|
| DL06 | Which interfaces need real-time data, and which take the daily batch? | Option A, a daily batch through COLLINS, is superseded by D-RCV-35: ACE ingests all source data and the Workbench runs no source batch load. Same-day triggers are named under option B: case transferred from EFS, payment received, legal event. | Not specified in the source documents (GAP-1458; ASM-2559) | 30 Oct |
| DL09 | Who tests from the business, and when? | Business testers work with the squads two to three hours a day during the build, then a one-week UAT before each release. | Not specified in the source documents (GAP-1458; ASM-2559) | 31 Oct |
| DL10 | What is the Thai name for each field, label and message? | The business lead drafts per module one epic ahead; Legal and Compliance approve. | Business lead with Legal and Compliance | 5 Nov |
| DL12 | Which legacy systems are kept, and does any need enhancing? | No legacy enhancement. The read and write wording of option A is superseded by D-RCV-35: source data is read only, through the recovery.v_ace_* views. | Not specified in the source documents (GAP-1458; ASM-2559) | 7 Nov |
| DL15 | Are the inventory counts and the growth assumption the right base for sizing? | A: Mortgage 12,256, hire purchase 12,960 and SSME 2,903 accounts; 3,110 new accounts a month; 15 percent growth a year. | Data lead | 6 Nov |
| DL16 | Does a case enter the Workbench at 90 or 91 days past due? | 90 days past due. The target operating model has the case owner holding the case from day 90. | Business lead | 6 Nov |
| DL17 | Is a case one per customer per product, one per account, or one per customer? | One per customer per product, with the accounts linked. | Product owner with the solution architect | 6 Nov |
| DL19 | Which document types and fields does the document hub classify and extract? | B where the bank has one; A until then. | Business lead with Legal | 6 Nov |
| DL20 | Where do customer facts come from? | The customer facts ACE holds, ingested from SCBPDM and the core bank, read through v_ace_customer. Amended by D-RCV-35. | Not specified in the source documents (GAP-1458; ASM-2559) | 30 Oct |
| DL21 | Which systems store the Workbench case identifier? | A for Epics 1 and 2. Each system added later is an interface change. | Solution architect with the IT lead | 6 Nov |
| DL24 | Which rules does the rules component load in Epic 1? | Allocation, assignment and transfer only. The route decision goes live in a later epic. | Product owner | 30 Oct |
| DL25 | How large a difference between the case list and the ACE account view is accepted? | Zero; any difference holds the publish. | Data lead | 6 Nov |
| DL26 | How long is each data product and document type kept, and which fields are masked for which role? | Provide per data product and document type. | Compliance | 13 Nov |
| DL29 | Which EFS contact outcomes come into the interaction ledger, and how far back? | A named list of outcomes for the case's collection period only. named by the business lead. | Data lead with the business lead | 13 Nov |
| DL39 | Which roles receive real users at each release? | Administration roles at Epic 1; business roles from the release that gives them a screen, starting with Epic 2. | Business lead | 20 Nov |
| DL40 | What are the Entra ID group names and the bank IAM entry for the Workbench roles? | One group per role per environment. | SCB IT security | 6 Nov |
| DL43 | Does the ACE team accept the RWB-ACE-001 scope and its dates? | Open. The build assumes the scope is accepted: 14 tables, 12 columns and 80 source fields by 21 November. Until they land, the Section B views and the features that need them stay behind their flags. | ACE team lead | 21 Nov |


# 8. Delivery model

Version 5 records how Epic 1 is delivered after D-RCV-60 adopts Architecture v5. The requirements in
section 3 are unchanged and keep their keys. What changes is the way they are built: the Workbench is
one module inside ACE, built as 19 services, ordered in waves 0 to 4, and every service starts with its
published contract.

## 8.1 One epic per service

The Workbench is a module in the ACE platform built as 19 services (ADR-013). Each service is one
development epic, `RWB-SVC-<code>`, with its own schema and login in ACE PostgreSQL (ADR-014), its own
REST base, its own event topic with a retry and a dead-letter topic (ADR-015) and its own Temporal task
queue (ADR-016). A requirement is delivered by the service that owns the data or the action. The
Ownership Map v1 is the single source for that ownership, and it is used for every owner named in this
section and in section 9.

| Code | Service epic | Service | Scope | Wave |
|---|---|---|---|---|
| P1 | RWB-SVC-P1 | rwb-source-data | Source data | 1 |
| P2 | RWB-SVC-P2 | rwb-integration | Integration | 1 |
| P3 | RWB-SVC-P3 | rwb-case | Case and workflow | 1 |
| P4 | RWB-SVC-P4 | rwb-access | Access and authority | 1 |
| P5 | RWB-SVC-P5 | rwb-document | Document | 1 |
| P6 | RWB-SVC-P6 | rwb-comms | Communications | 1 |
| P7 | RWB-SVC-P7 | rwb-decision | Decision and rules | 1 |
| P8 | RWB-SVC-P8 | rwb-payment | Payment | 2 |
| P9 | RWB-SVC-P9 | rwb-reporting | Reporting | 1 |
| P10 | RWB-SVC-P10 | rwb-agent | Agent | 1 |
| S1 | RWB-SVC-S1 | rwb-valuation | Valuation and route | 3 |
| S2 | RWB-SVC-S2 | rwb-treatment | Treatment and offer | 2 |
| S3 | RWB-SVC-S3 | rwb-guarantee | Guarantee | 3 |
| S4 | RWB-SVC-S4 | rwb-litigation | Litigation | 3 |
| S5 | RWB-SVC-S5 | rwb-asset | Asset | 2 |
| S6 | RWB-SVC-S6 | rwb-debtsale | Debt sale | 3 |
| S7 | RWB-SVC-S7 | rwb-writeoff | Write-off | 4 |
| S8 | RWB-SVC-S8 | rwb-deviation | Deviation | 2 |
| S9 | RWB-SVC-S9 | rwb-partner | Partner | 4 |
| ITG | RWB-ITG-W1 to RWB-ITG-W4, RWB-ITG-NFR | Integration harness per wave, and non-functional | Integration | 0 |

The service names above are the Ownership Map v1 service names; the requirement headings in section 3 keep the module names of version 4 (ASM-2556). The seven platform epics are RWB-PLT-TPL, RWB-PLT-LIB, RWB-PLT-WF, RWB-PLT-DB, RWB-PLT-EVT, RWB-PLT-EDGE and RWB-PLT-OBS.

## 8.2 Waves

Wave 0 is the platform: the service template, the shared libraries, the workflow platform, the event
platform, the edge and gateway, observability, the ACE schemas and logins, and the integration harness.
Waves 1 to 4 follow the business epics. A story takes the earlier of its business-epic wave and its
service's wave, so an Epic 1 requirement is built in wave 1 even where its service is scheduled later
(GAP-1456).

| Wave | Business epic | Theme | Release (tentative) | Service epics that start in the wave |
|---|---|---|---|---|
| 0 | Platform and non-functional | Service template, libraries, workflow, events, edge, observability, ACE schemas, integration harness | Before wave 1 | RWB-PLT-TPL, RWB-PLT-LIB, RWB-PLT-WF, RWB-PLT-DB, RWB-PLT-EVT, RWB-PLT-EDGE, RWB-PLT-OBS, RWB-ITG-W1, RWB-ITG-W2, RWB-ITG-W3, RWB-ITG-W4, RWB-ITG-NFR |
| 1 | EP01 Foundation 1 | One case list, documents by case, decision log store, read-only case record view | 30 November 2026 (tentative) | RWB-SVC-P1, RWB-SVC-P2, RWB-SVC-P3, RWB-SVC-P4, RWB-SVC-P5, RWB-SVC-P6, RWB-SVC-P7, RWB-SVC-P9, RWB-SVC-P10 |
| 2 | EP02 Foundation 2; EP03 Settle, deed in lieu, assets | One owner and a timer on every case, approval routing, litigation notices; settlements and deeds in lieu end to end, asset record and listing | 31 December 2026 (tentative); 31 January 2027 (tentative) | RWB-SVC-P8, RWB-SVC-S2, RWB-SVC-S5, RWB-SVC-S8 |
| 3 | EP04 Route decision; EP05 Litigation | Route recommended and approved within the delegation of authority, guarantees and TCG claims; litigation instructed and tracked | 28 February 2027 (tentative); 31 March 2027 (tentative) | RWB-SVC-S1, RWB-SVC-S3, RWB-SVC-S4, RWB-SVC-S6 |
| 4 | EP06 Debt sale and write-off; EP07 Deviations and partners; EP08 Administration and hardening | Debt sale and write-off; deviations X1 to X7 and partner management; full administration and hardening | 30 April 2027 (tentative); 31 May 2027 (tentative); 30 June 2027 (tentative) | RWB-SVC-S7, RWB-SVC-S9 |

## 8.3 Contract first

Every service epic opens with a contract story. The contract is published as an OpenAPI file, an
AsyncAPI file and an activity jar before application work starts, and application stories build against
the published contract and its fake. A service therefore never waits for another service's code. Each
service calls one hop over REST with a 2 second timeout (ADR-020), publishes CloudEvents on
`rwb.<short>.events.v1` with retries and a dead-letter topic (ADR-015), and runs its workflows on its
own Temporal task queue (ADR-016). Scheduled work is a Temporal Schedule and not a Quartz job. There is
no data lake: reporting is built from events into the reporting read model (ADR-018).

Contract stories are Day 1 work. An application story that depends on another service's contract builds
against the published contract and its fake, so the dependency never blocks a lane.

## 8.4 Work types and soft ownership

Each story is one of six work types, and each work type carries a suggested owner by team type. The
suggestion is not binding: any team may pick up a story, and no person is named in any output.

| Work type | Work | Suggested owner |
|---|---|---|
| CON | Contract | TechX (suggested; any team may pick up this story) |
| APP | App development | TechX (suggested; any team may pick up this story) |
| DB | ACE DB | ACE team (suggested; any team may pick up this story) |
| INF | Infrastructure | SCB IT infrastructure (suggested; any team may pick up this story) |
| OPS | DevOps | DevOps team (suggested; any team may pick up this story) |
| ITG | Integration, harness and non-functional | TechX for integration and QA team for harness and non-functional (suggested; any team may pick up this story) |

## 8.5 Requirements kept, changed, retired and cancelled

The business content of section 3 is unchanged. The delivery model changes only how a requirement is
built. Five positions apply.

| Position | Requirements | What the delivery model does |
|---|---|---|
| Built or in build, kept | RWB-E1-042, RWB-E1-043, RWB-E1-044 | The as-built content is kept word for word. The microservice change is separate delta stories: one schema and one contract per service, parameters and reference data behind the rwb-case contract, and Flyway per service. No built code changes until a delta story is picked up. |
| Must change | RWB-E1-001 | The built single-schema migration (92 tables, 14 data products, dictionary) is kept. The split into one schema per service is new work under RWB-PLT-DB and the per-service DB stories, and it is recorded in the Change Register. |
| Retired by D-RCV-60 | RWB-E1-014 | Architecture v5 has no data lake. The decision log is read from events into the reporting read model. The requirement keeps its key and its text, and no story is built (GAP-1453). |
| Already cancelled before this run | RWB-E1-029, RWB-E1-048 | No story is built. The keys and the text stay in section 3.3 (GAP-1454 and GAP-1455). |
| Removed by D-RCV-35 | RWB-E1-003, RWB-E1-004, RWB-E1-005, RWB-E1-006, RWB-E1-009, RWB-E1-010, RWB-E1-012, RWB-E1-051 | Already marked Removed in section 3, each naming its later home: ACE ingestion, or the Cutover plan. Nothing further changes. |

## 8.6 Dates

Every release date in this document is unchanged from version 4, and every one is tentative
(DL48). Epic 1 releases on 30 November 2026 (tentative), and the programme finishes within eight
months.

# 9. Business requirement to service epic trace

Every requirement in section 3 keeps its key. The key is the business requirement ID of this epic and
it does not change between versions. The primary service epic is the chapter that owns the largest part
of the requirement in the Ownership Map v1; where a key has several stories, the other service epics
carry the linked stories of the same key. Every requirement that is built belongs to business epic EP01
Foundation 1, which is wave 1 and releases on 30 November 2026 (tentative). The story count is the
number of story slices the plan holds for the key.

| Business requirement | Requirement | Primary service epic | Service | Wave | Business epic | Stories |
|---|---|---|---|---|---|---|
| RWB-E1-001 | Recovery tables for the 14 data products | RWB-SVC-P1 | P1 rwb-source-data | 1 | EP01 | Must change, 5 stories |
| RWB-E1-002 | Case list v1 with case ID, owner and queue | RWB-SVC-P1 | P1 rwb-source-data | 1 | EP01 | Split into 5 stories |
| RWB-E1-003 | ALS daily extract load | None | - | - | - | Removed by D-RCV-35, no story |
| RWB-E1-004 | EFS extract load | None | - | - | - | Removed by D-RCV-35, no story |
| RWB-E1-005 | Excel and SharePoint inventory | None | - | - | - | Removed by D-RCV-35, no story |
| RWB-E1-006 | Data quality rules v1 | None | - | - | - | Removed by D-RCV-35, no story |
| RWB-E1-009 | CCMS and SVAF loads | None | - | - | - | Removed by D-RCV-35, no story |
| RWB-E1-010 | Excel and SharePoint loads | None | - | - | - | Removed by D-RCV-35, no story |
| RWB-E1-011 | Reconciliation and data quality report | RWB-SVC-P1 | P1 rwb-source-data | 1 | EP01 | Split into 7 stories |
| RWB-E1-012 | Retire local copies | None | - | - | - | Removed by D-RCV-35, no story |
| RWB-E1-014 | Decision log copy to the data lake | None | - | - | - | No story: retired by D-RCV-60 |
| RWB-E1-015 | Freshness stamp per data product | RWB-SVC-P1 | P1 rwb-source-data | 1 | EP01 | Split into 4 stories |
| RWB-E1-016 | Access control per data product and catalog entries | RWB-SVC-P1 | P1 rwb-source-data | 1 | EP01 | Split into 6 stories |
| RWB-E1-017 | Retention and archive rule for the data store | RWB-SVC-P1 | P1 rwb-source-data | 1 | EP01 | Split into 6 stories |
| RWB-E1-064 | Data dictionary for the 14 data products | RWB-SVC-P1 | P1 rwb-source-data | 1 | EP01 | Split into 5 stories |
| RWB-E1-065 | Sandbox database with synthetic recovery data | RWB-SVC-P1 | P1 rwb-source-data | 1 | EP01 | Split into 8 stories |
| RWB-E1-066 | Interaction ledger store and writer | RWB-SVC-P1 | P1 rwb-source-data | 1 | EP01 | Split into 5 stories |
| RWB-E1-067 | Every Workbench action into the interaction ledger | RWB-SVC-P1 | P1 rwb-source-data | 1 | EP01 | Split into 5 stories |
| RWB-E1-068 | Interaction ledger read interface | RWB-SVC-P1 | P1 rwb-source-data | 1 | EP01 | Moved unchanged, 1 story |
| RWB-E1-069 | Read-only ACE source views, grants and boundary rule | RWB-SVC-P1 | P1 rwb-source-data | 1 | EP01 | Split into 4 stories |
| RWB-ACE-001 | ACE DB additions for the Recovery Workbench | RWB-SVC-P1 | P1 rwb-source-data | 1 | EP01 | Split into 1 story |
| RWB-E1-007 | Outbound integration adapters for files and events | RWB-SVC-P2 | P2 rwb-integration | 1 | EP01 | Split into 9 stories |
| RWB-E1-047 | Feature flags for module release with a removal date | RWB-PLT-LIB | Platform | 1 | EP01 | Split into 3 stories |
| RWB-E1-051 | Legacy feed jobs on ADF and Control-M | None | - | - | - | Removed by D-RCV-35, no story |
| RWB-E1-056 | Run books and monitoring for every Epic 1 job | RWB-PLT-OBS | Platform | 1 | EP01 | Split into 1 story |
| RWB-E1-018 | Case ID issuance and case record v1 | RWB-SVC-P3 | P3 rwb-case | 1 | EP01 | Split into 8 stories |
| RWB-E1-019 | Roles, teams and queues as data | RWB-SVC-P3 | P3 rwb-case | 1 | EP01 | Split into 6 stories |
| RWB-E1-020 | Allocation and assignment engine v1 | RWB-SVC-P3 | P3 rwb-case | 1 | EP01 | Split into 7 stories |
| RWB-E1-021 | Transfer rules and engine v1 | RWB-SVC-P3 | P3 rwb-case | 1 | EP01 | Split into 8 stories |
| RWB-E1-023 | Case record view v1, read only | RWB-SVC-P3 | P3 rwb-case | 1 | EP01 | Split into 5 stories |
| RWB-E1-028 | Service levels, timers, escalation and prescription dates | RWB-SVC-P3 | P3 rwb-case | 1 | EP01 | Split into 6 stories |
| RWB-E1-029 | Rule load, validation and rollback | None | - | - | - | No story: already cancelled before this run |
| RWB-E1-030 | Daily rebalancing and queue measures | RWB-SVC-P3 | P3 rwb-case | 1 | EP01 | Split into 5 stories |
| RWB-E1-031 | Queue and owner on the case list with filters | RWB-SVC-P3 | P3 rwb-case | 1 | EP01 | Split into 3 stories |
| RWB-E1-035 | Case record view v1.1 with documents and history timeline | RWB-SVC-P3 | P3 rwb-case | 1 | EP01 | Split into 2 stories |
| RWB-E1-042 | Central configuration service and parameter catalog | RWB-SVC-P3 | P3 rwb-case | 1 | EP01 | Kept as built, 5 stories including the delta |
| RWB-E1-043 | Reference data service with versioned tables | RWB-SVC-P3 | P3 rwb-case | 1 | EP01 | Kept as built, 4 stories including the delta |
| RWB-E1-044 | Database migrations versioned with parameterized schema names | RWB-PLT-TPL | Platform | 1 | EP01 | Kept as built, 4 stories including the delta |
| RWB-E1-045 | Multi-product parameters for Mortgage, HP and SSME | RWB-SVC-P3 | P3 rwb-case | 1 | EP01 | Moved unchanged, 1 story |
| RWB-E1-048 | Rule change audit report | None | - | - | - | No story: already cancelled before this run |
| RWB-E1-022 | Sign-on with SSO, MFA and the first roles | RWB-SVC-P4 | P4 rwb-access | 1 | EP01 | Split into 4 stories |
| RWB-E1-037 | Role to permission matrix as data and PDPA field masking by role | RWB-SVC-P4 | P4 rwb-access | 1 | EP01 | Split into 5 stories |
| RWB-E1-038 | Delegation of authority table as reference data | RWB-SVC-P4 | P4 rwb-access | 1 | EP01 | Moved unchanged, 1 story |
| RWB-E1-039 | Access log into the decision log and break-glass admin | RWB-SVC-P4 | P4 rwb-access | 1 | EP01 | Split into 7 stories |
| RWB-E1-024 | Document store and index | RWB-SVC-P5 | P5 rwb-document | 1 | EP01 | Moved unchanged, 2 stories |
| RWB-E1-025 | Document types and fields agreed | RWB-SVC-P5 | P5 rwb-document | 1 | EP01 | Moved unchanged, 2 stories |
| RWB-E1-026 | Attach and search screen | RWB-SVC-P5 | P5 rwb-document | 1 | EP01 | Moved unchanged, 2 stories |
| RWB-E1-032 | Automatic attach from the OCR intake | RWB-SVC-P5 | P5 rwb-document | 1 | EP01 | Split into 9 stories |
| RWB-E1-033 | Search across cases | RWB-SVC-P5 | P5 rwb-document | 1 | EP01 | Moved unchanged, 1 story |
| RWB-E1-040 | Document checklist per case type as reference data | RWB-SVC-P5 | P5 rwb-document | 1 | EP01 | Moved unchanged, 1 story |
| RWB-E1-041 | Retention classes and virus scan on intake | RWB-SVC-P5 | P5 rwb-document | 1 | EP01 | Moved unchanged, 2 stories |
| RWB-E1-049 | OCR pipeline on the Workbench document hub | RWB-SVC-P5 | P5 rwb-document | 1 | EP01 | Split into 6 stories |
| RWB-E1-050 | Document classification | RWB-SVC-P5 | P5 rwb-document | 1 | EP01 | Split into 5 stories |
| RWB-E1-053 | Field extraction for the six types into the index | RWB-SVC-P5 | P5 rwb-document | 1 | EP01 | Moved unchanged, 2 stories |
| RWB-E1-054 | Review queue for low-confidence documents | RWB-SVC-P5 | P5 rwb-document | 1 | EP01 | Split into 6 stories |
| RWB-E1-057 | Intake from branches, mailroom, partner SFTP and email | RWB-SVC-P5 | P5 rwb-document | 1 | EP01 | Split into 6 stories |
| RWB-E1-034 | Letter template management | RWB-SVC-P6 | P6 rwb-comms | 1 | EP01 | Moved unchanged, 2 stories |
| RWB-E1-046 | Template and merge field catalog as data | RWB-SVC-P6 | P6 rwb-comms | 1 | EP01 | Split into 5 stories |
| RWB-E1-052 | Notice generation v1 | RWB-SVC-P6 | P6 rwb-comms | 1 | EP01 | Split into 6 stories |
| RWB-E1-055 | Proof of delivery capture design with WIN | RWB-SVC-P6 | P6 rwb-comms | 1 | EP01 | Split into 8 stories |
| RWB-E1-008 | Decision log store v1, append only and hash chained | RWB-SVC-P7 | P7 rwb-decision | 1 | EP01 | Split into 6 stories |
| RWB-E1-027 | Decision log writer v1 | RWB-SVC-P7 | P7 rwb-decision | 1 | EP01 | Split into 5 stories |
| RWB-E1-013 | Baseline measures | RWB-SVC-P9 | P9 rwb-reporting | 1 | EP01 | Split into 6 stories |
| RWB-E1-058 | Agent platform set-up [E1a] | RWB-SVC-P10 | P10 rwb-agent | 1 | EP01 | Split into 5 stories |
| RWB-E1-059 | Case intake agent in shadow [E1b] | RWB-SVC-P10 | P10 rwb-agent | 1 | EP01 | Split into 3 stories |
| RWB-E1-060 | Extraction evaluation [E1c] | RWB-SVC-P10 | P10 rwb-agent | 1 | EP01 | Moved unchanged, 2 stories |
| RWB-E1-061 | Intake agent evaluation and L1 proposal [E2a] | RWB-SVC-P10 | P10 rwb-agent | 1 | EP01 | Moved unchanged, 2 stories |
| RWB-E1-062 | Deviation screening agent in shadow [E2b] | RWB-SVC-P10 | P10 rwb-agent | 1 | EP01 | Split into 6 stories |
| RWB-E1-063 | Agent monitoring dashboard v1 [E2c] | RWB-SVC-P10 | P10 rwb-agent | 1 | EP01 | Split into 6 stories |

A key with no service epic is not built: RWB-E1-014 is retired by D-RCV-60 and RWB-E1-029 and RWB-E1-048 were cancelled before this run (section 8.5). The eight removed keys keep their text and their later home. No requirement text, key, count or date in sections 1 to 7 is changed by this version; the five positions in section 8.5 and the positions in this table are the only delivery statements added.

<!-- source: 05 Technical architecture/Recovery Workbench Target Architecture v5.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `05 Technical architecture/Recovery Workbench Target Architecture v5.docx`  
> **Converted from:** DOCX

Recovery Workbench

Target architecture, all eight epics

SCB Collections and Recovery. Henka Group, 15 November 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench target architecture |
| Version | 5 |
| Date | 15 November 2026 |
| Prepared by | Henka Group |
| Structure | arc42, with C4 context and container views and ISO/IEC/IEEE 42010 viewpoints |

# 1. Goals

The Recovery Workbench owns every recovery case from 90 days past due to close for Mortgage, Hire Purchase and SSME. It is the recovery module of ACE.

| Goal | What it means |
|---|---|
| One case record from day 90 to close | Every recovery case is held once, with one owner, one clock and one history, in the same application as collection |
| Change without a release | Every rule, limit, threshold, template, queue, role, timer and route is a versioned data row |
| Every decision traceable | Each decision is logged once with its inputs, the rule and model versions, the approver and the outcome |
| Safe use of AI | Agents prepare and recommend through one runtime, start in shadow and fall back to the rules when they do not answer |
| Monthly releases | One production release at each month end, shared with the collection squad, from November 2026 to June 2027 |

# 2. Constraints

| Constraint | What it means | Status |
|---|---|---|
| Built on ACE | The Workbench is a module of ACE: one service, one repository, one front end | Taken |
| Modular monolith | Common, collection and recovery modules by folder, with boundaries checked at build time | Taken |
| Programmatic workflow | Case, stage and task state held in the database and moved by code. No Temporal | Taken |
| CMMN 1.1 | Case, stage, milestone, task, sentry, event listener and case file item mean the same in both modules | Taken |
| Data through ACE | Source data lands in the ACE database through ACE ingestion. The recovery module reads it through 30 read-only views and holds no copy | Taken; D-RCV-35, ADR-010; ACE additions DL43 |
| ACE technology | Spring Boot, React on Vite, PostgreSQL, Entra ID, the bank IAM, PII Kafka, audit and SOC logs | Taken |
| Document hub built here | The Workbench holds recovery documents as their system of record | Taken; storage pattern DL27 |
| No legacy enhancement | The Workbench reads source data through ACE and writes through ACE only | Taken; D-RCV-35 (supersedes DL12 option A) |

# 3. Context

No component calls a system of record directly. Source data lands in the ACE database through ACE ingestion, and the recovery module reads it through recovery.v_ace_* views. Work for other systems leaves through paths ACE already has.

| Actor or system | What passes | How |
|---|---|---|
| Bank staff | Case owners, officers, approvers, committees, control functions | Workbench screens in the ACE front end, signed in through Entra ID |
| Partners | Law firms, agencies, valuers, auction vendors, debt buyers, RAMC | Partner portal, once partner access from outside the bank is in place (DL03) |
| Customers | Borrowers, guarantors, heirs, bidders | Existing bank channels only: SCB Easy, LINE OA, SMS, branches, HOME.SCB |
| COLLINS | Account, customer, collections history, litigation status, scores | ACE ingestion, daily batch into the ACE database |
| CCMS, SVAF, AMIS, RPS, LIT, WIN, GL, SCBPDM, NLEADS, EasyApp, Entra ID | Collateral detail, appraisals, assets, litigation, registered mail, write-off postings, product holding, credit decisions, signature requests, group mapping | ACE ingestion into the ACE database. No Workbench load |
| Core bank (ALS) | Bookings for restructures, settlements and write-offs | Made by the officer; confirmed in ACE on the next business date |
| NSS and LINE OA | SMS and LINE messages | The ACE notification path |
| Power BI and the data lake | Reporting and model learning | Daily batch out |
| Enterprise AI platform | The model endpoint the agents call | Private endpoint in the SCB tenant (DL33) |

# 4. Solution strategy

|  | Principle |
|---|---|
| 1 | Everything that a business person may want to change is a versioned data row, changed through a validated load without a code release |
| 2 | One service, one repository, one front end. A module calls another only through its published interface or an application event |
| 3 | Each module owns its tables. No module reads another module's tables directly; the recovery module reads ACE source data only through its own read-only views |
| 4 | No component calls a system of record directly. ACE ingests the source data and the recovery module reads it through read-only views; outbound work leaves through existing ACE paths |
| 5 | A decision that cannot be written to the decision log does not proceed |
| 6 | An agent reaches a system only through the tool gateway and holds no credential. When it does not answer, the rule result is used |
| 7 | Personal data is masked in the views and at the API unless the role is allowed to see it. No personal data in code, tests, logs or prompts |
| 8 | Every value read from ACE carries its business date, so every decision can show the age of its inputs |

# 5. Building blocks

## 5.1 The modular monolith

| Module | Built by | Holds |
|---|---|---|
| Common | ACE team | Sign-in and access checks, audit and PII logging, the shared case view, shared entities (customer, account, product, collateral, asset), shared tasks such as the restructure calculator, the notification path |
| Collection | Collection squad | Phone, field, FCR and restructure work, as split under DL14 |
| Recovery | TechX recovery squads | Recovery stages, tasks and screens, the rules component, the decision center and log, the document hub, the partner portal, the read-only ACE views and the extension tables |

- A module calls another only through its published interface or an application event.

- Each module owns its tables; another module reads them only through the owning module's interface.

- The recovery module reads ACE source data only through recovery.v_ace_* views: no direct read of a public table, no write and no foreign key into ACE (ADR-010).

- A boundary test runs in every build and fails it on any violation.

- A recovery component the collection module also needs moves to the common module by agreement with the ACE team.

## 5.2 Platform modules

|  | Module | Where it lives | What it owns | First in |
|---|---|---|---|---|
| P1 | Recovery data engine | Recovery | Read-only ACE source views, the extension tables, reconciliation to the ACE account list, freshness from the ACE batch record | E1 |
| P2 | Integration | Common and recovery | Outbound files and adapters, the ACE integration paths | E1 |
| P3 | Case and workflow | Recovery, with the common case view | Case record, CMMN state, queues, allocation, timers, the rules component | E1 core, E2 screens |
| P4 | Access and administration | Common, with recovery roles as data | Roles, permissions, scope, masking, delegation of authority table, access log | E1; E2 partners; E8 full administration |
| P5 | Document hub | Recovery | Store, index, OCR, classification, extraction, review queue, retention, custody | E1 store and OCR; E2 generation |
| P6 | Communications | Common path, recovery templates | Letters, notices, SMS, LINE, proof of delivery | E1 notices; E2 dispatch; E4 self-service |
| P7 | Decision center and log | Recovery | Recommendation with reasons, approval within delegation, decision log store and writer | E1 log; E2 routing; E3 center |
| P8 | Payments and posting | Recovery | Payment and proceeds matching, fees, posting files | E2 matching; E4 |
| P9 | Reporting | Recovery, with Power BI | Baseline measures, steering dashboard, operational and regulatory reports | E1 baseline; E2 dashboard |
| P10 | Agent runtime | Recovery, calling the Enterprise AI platform | Orchestrator, tool gateway, guardrails, prompt store, evaluation, autonomy levels | E1 shadow; E2 L1 |

## 5.3 Stage modules

|  | Module | What it owns | First in |
|---|---|---|---|
| S1 | Valuation and route | D6 route decision with COLLINS return by route and the route agent | E4 |
| S2 | TDR, settlement and deed in lieu | Treatment record, contracts, booking, plan timers | E2 foundations; E3 |
| S3 | Guarantees and guarantors | TCG and insurance claims, guarantor notices and pursuit | E4 |
| S4 | Litigation and enforcement | Notices, law firm instruction, hearings, judgment, enforcement | E2 notices; E5 |
| S5 | Assets and auction | Asset record, holding, floor price, listing, auction rounds, RAMC | E3; E4 |
| S6 | Debt sale | Lot building, data room, buyer terms, award, transfer | E5 data; E6 screens |
| S7 | Write-off and recovery | Eligibility, committee, posting, recovery after charge-off | E6 |
| S8 | Deviation handling | X1 to X7: screening, pause, handling, return | E2 screening; E7 |
| S9 | Partner management | Panel, allocation, fees, scorecards, conduct | E6 panel; E7 scoring |

# 6. Runtime

## 6.1 How the case workflow runs

| Step | What happens |
|---|---|
| Event arrives | An ACE refresh, a screen action, a partner result, a timer or another module |
| Rules evaluated | The rules component finds the rule for the state and the event |
| Decision logged | Rule version, inputs and approver written. A failed write stops here |
| Action taken | Next state, tasks, owner, queue, documents or notices |
| Timer set | The next due date is stored for the scheduler |
| Work queued | Work for other systems goes to an outbox with retry |

Case, stage and task state are rows in the ACE database. A wait of weeks is a row with a state and a stored due date. Timers run on Quartz. Automated chains to other systems run on Spring Batch with an outbox, retry and an exception queue. No workflow engine is used.

| Case model, CMMN 1.1 | Count |
|---|---|
| Stages | 10 |
| Milestones | 30 |
| Tasks | 150 |
| Event listeners | 53 |
| Sentries (rules) | 448 |
| Case file items | 12 |

## 6.2 The rules component

| What | How it works |
|---|---|
| Rules as rows | Each route set is a decision table: from state, event and condition in; action, next state, owner and timer out. Each row has an ID, a version, valid from and valid to dates, an approver and a test case |
| Hit policy Unique | For one state and one event in a route set, at most one condition holds, so one rule fires |
| Evaluator | A decision table evaluator in the recovery module reads the rows in force and returns the action. ACE has no rules engine today |
| Loading a change | A new version is loaded, checked against the schema and the completeness checks, and refused whole if any check fails |
| Open cases | A case keeps the rule version it was decided under. New decisions use the version in force on the day |
| Universal rules | Rules that apply in every state, such as a cure, a hold or a death, are evaluated before the route rules |
| Epic 1 | Allocation, assignment and transfer rules only. The route decision follows in Epic 4 (DL24) |

## 6.3 The agent runtime

| Part | What it does |
|---|---|
| Orchestrator | Runs the decision steps and applies the autonomy level |
| Tool gateway | The only way an agent reaches a system. No agent holds a credential |
| Guardrail checker | Checks every output against its schema, the allowed actions and a confidence floor |
| Prompt and policy store | Versioned, so a run can be reproduced |
| Evaluation harness | Labeled sets scored before a result is used |
| Model endpoint | On the approved endpoint in the SCB tenant (DL33) |

| Level | The agent | A person |
|---|---|---|
| L0 | Nothing. The rule decides | Everything |
| L1 | Recommends, with its reasons | Decides. Every decision starts here after a shadow run |
| L2 | Acts inside a narrow band | Reviews a sample and the exceptions |
| L3 | Acts across the decision | Reviews by exception |
| L4 | Acts and closes | Monitors the measures |

Agents run in shadow first. A decision moves up one level on evidence and drops one level on a guardrail breach. When an agent does not answer in time, the rule result is used and the case still routes.

# 7. Deployment

| Environment | Data | Deployed | Notes |
|---|---|---|---|
| DEV | Synthetic data | On every merge into main | Four slots planned, one available (DL35) |
| SIT | Masked data | On a release tag | Two slots planned, one available (DL35) |
| UAT | Masked data | In the week before each release | Shared with the collection squad |
| PROD | Live data | In the monthly change window (DL34) | ACE namespace on the shared ACE AKS clusters |

Nine pipeline gates run before every merge: build and unit tests, lint, secret scan, PDPA lint, container scan, module boundary, integration and contract tests, AI first-pass review, and human approval. A change that fails SIT or UAT has its feature flag switched off and the release goes ahead without it.

# 8. Crosscutting concepts

## 8.1 Data

The Workbench holds no source data. ACE holds it, and the Workbench reads it through 30 read-only views.

### 8.1.1 Data tiers

| Tier | Owner | What it holds | Count |
|---|---|---|---|
| 1 | ACE team, read only | ACE tables that exist today, read through a view and never altered | 22 tables, 16 views |
| 2 | ACE team | New ACE tables and columns for source data that ACE does not hold | 14 tables, 12 columns, 14 views |
| 3 | Workbench | 1:1 extension tables keyed by ACE business keys | 4 tables |
| 4 | Workbench | Case, workflow, treatment, legal, partner, debt sale, documents, decision log, reference, outbox, flags, agents | 88 tables |
| Removed | - | Source copies, load machinery and the 6 columns the ACE story absorbs | 20 tables, 243 fields |

The Workbench schema is 92 tables: 4 extension tables and 88 retained tables. With the 30 views, the dictionary holds 122 objects and 1,366 fields, in place of 108 tables and 1,256 fields. Tier 1 views ship with RWB-E1-069; the Tier 2 views ship when RWB-ACE-001 lands (DL43).

The tier table above is the normative data tier diagram for this document. Slide 11 of the Recovery Workbench Target Architecture v5 deck draws the same four tiers and the single read path.

The elements that hold the Workbench's own data:

| Element | What it holds |
|---|---|
| ACE database (PostgreSQL) | Case, workflow, treatment, legal, partner, disposal and money records; reference data; the decision log and the interaction ledger. ACE also holds the source data the Workbench reads, written by ACE ingestion |
| Blob storage, write-once container | Documents. Legal document types cannot be overwritten |
| 14 data products | Each with one system of record, one read path and one freshness |
| 92 tables, 30 views, 1,366 fields | In the bank TSD section T3 form, with seven standard columns on every entity. 122 dictionary objects: 92 tables and 30 views |
| Decision log | Append only, hash chained, one entry per decision |
| Out to the data lake | Case, queue, decision and outcome data by daily batch for Power BI and COLLINS |

## 8.2 Security and access

| Control | How it works |
|---|---|
| Sign-in | Entra ID single sign-on with multi-factor authentication |
| Roles | 54 roles held as data, granted by Entra ID group membership through the bank IAM |
| Permissions | A matrix of roles against 14 capability areas, held as versioned data, checked on every endpoint |
| Scope | Own cases, team, region or all, set per role |
| Masking | Personal data masked in the views and at the API unless the role is allowed to see it |
| Approval limits | The delegation of authority table as reference data, checked before an approval is accepted |
| Logs | Access to personal data through PII Kafka; security events to the SOC log; every decision to the decision log |
| Break-glass | Emergency access with a reason and a review window |
| Partners | Their own identities, scoped to the cases placed with them (DL03) |

# 9. What each epic adds

| Epic | Release | Added |
|---|---|---|
| E1 | 30 Nov 2026 | P1 read-only ACE views for Tier 1 (RWB-E1-069) and the extension tables, reconciliation and freshness; P3 case record, state model and rules component with allocation rules; P4 sign-in and roles; P5 document store and OCR; P6 notice generation; P7 decision log store; P9 baseline; P10 agent runtime in shadow; Tier 2 after RWB-ACE-001: the Tier 2 views ship when the ACE additions land (DL43) |
| E2 | 31 Dec 2026 | P3 queue and transfer screens; P4 partner identities; P5 document generation; P6 dispatch and proof of delivery; P7 approval routing; P8 matching skeleton; P9 steering dashboard; S2 treatment record; S4 notice approval; S8 deviation screening |
| E3 | 31 Jan 2027 | S2 settlement and deed in lieu to booking; S5 asset record, floor price and listing; P7 decision center |
| E4 | 28 Feb 2027 | S1 route decision with COLLINS and the route agent; S3 guarantee and TCG claims; S5 auction rounds and RAMC; P6 customer self-service; P8 posting |
| E5 | 31 Mar 2027 | S4 litigation end to end with law firms through the partner portal; S6 lot data and data room |
| E6 | 30 Apr 2027 | S6 debt sale screens and award; S7 write-off and committee; S9 partner panel, allocation and fees |
| E7 | 31 May 2027 | S8 deviations end to end; S9 partner scoring, conduct and the field app |
| E8 | 30 Jun 2027 | P4 full administration; conduct checks; autonomy step-ups; regulatory returns; hardening |

# 10. Quality targets

| Quality | Target or position | Status |
|---|---|---|
| Availability | 99.9% in business hours | Proposed, DL11 |
| Screen response | Under 2 seconds | Proposed, DL11 |
| Agent response | Within 60 seconds; after that the rule result is used | Proposed, DL11 |
| Recovery point and time | Set by SCB IT | Open, DL11 |
| Volume | About 23,600 open cases at go-live and 26,500 at the end of 2027; about 410 concurrent users | Sized; bank confirms under DL15 |
| Retention and masking | Per data product and document type | Open, DL26 |
| Data freshness | End of day for ACE data; the view reports the ACE batch date. Tier 2 sources arrive at the frequency ACE ingests them | Taken; DL06 for same-day needs, DL43 for the ACE additions |
| Auditability | Every decision reproducible from the log with its rule version and approver | Designed |
| Resilience | An agent or model outage falls back to rules. A source that has not refreshed shows its age on the view and through the data product freshness stamp | Designed |

# 11. Risks

| Risk | Effect | Answer |
|---|---|---|
| Data arrives a day late | End of day data for decisions that need today's position | Officers confirm payoff figures in the core; same-day triggers named under DL06 |
| A source is not ingested by ACE | That source reopens U1 for it and needs a Workbench staging table and a load | Each source confirmed with the ACE team under DL43; the gap list names them one by one |
| RWB-ACE-001 lands late | The Tier 2 views, and the features that read them, cannot ship on their planned release | Tier 2 features stay behind their feature flags until RWB-ACE-001 lands; Tier 1 views ship with RWB-E1-069; scope and dates confirmed under DL43 |
| Two squads, one repository | One squad's change holds the other's release | Feature flags, code owners and the module boundary test (DL04, DL37) |
| Rules component is new to ACE | ACE has rule based logic and no engine | A decision table evaluator in the recovery module, tested rule by rule against its test case |
| Volume grows faster than forecast | Reads, storage and queues sized too small | Sized at 15 percent inflow growth a year from the 30 June 2026 inventory; reviewed each quarter (DL15) |
| Partner access from outside | One to three months of lead time | Change raised in November; law firms first needed at Epic 5 (DL03) |

# 12. Open architecture decisions

| Decision | What is needed |
|---|---|
| DL03 | How partners reach the partner portal from outside the bank |
| DL05 | Who creates the recovery module in ACE |
| DL06 | Which interfaces need real-time data |
| DL07 | How the front end is split into modules |
| DL11 | Non-functional target values |
| DL12 | Which legacy systems are kept |
| DL21 | Which systems carry the case identifier |
| DL27 | Storage, backup, legal hold and e-discovery for the document hub |
| DL33 | The model endpoint the agents call |
| DL35 | Further ACE deployment slots |
| DL43 | Whether the ACE team accepts the RWB-ACE-001 scope and its dates (needed by 21 November 2026) |

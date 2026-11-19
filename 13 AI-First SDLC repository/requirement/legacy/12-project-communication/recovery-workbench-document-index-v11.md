<!-- source: 12 Project communication/Recovery Workbench Document Index v11.md -->
<!-- converted: 2026-11-04 from Markdown (copied) -->

> **Source:** `12 Project communication/Recovery Workbench Document Index v11.md`  
> **Converted from:** Markdown (copied)

# Recovery Workbench document index

SCB Collections and Recovery. Henka Group, 2 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

Every asset in the document set, who reads it and the file that holds it. Functional and technical specifications are one file per module, in the two specification archives.

## Decisions

Read by: Sponsors, product owner, decision owners.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 1 | Admin and access model | Whether access is granted centrally or by the application owner, who the application owner is, and the authority levels. | NIST RBAC | Recovery Workbench Admin and Access Model v4.docx |
| 2 | Decision log | Every open decision with the question, the options, the owner, the date needed and what it blocks. | Henka excel rules | Recovery Workbench Decision Log v8.xlsx |

## Delivery

Read by: Program manager, sponsors, SCB IT.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 3 | Engineering practices | The agreed practices: branching, merging, code review, tests, feature flags, pipeline gates and who owns the merge. | Henka word rules | Recovery Workbench Engineering Practices v4.docx |
| 19 | Ways of working and governance | The daily and weekly cadence, who attends, what each forum decides, and how a decision is recorded. | Henka word rules | Recovery Workbench Ways of Working and Governance v3.docx, Recovery Workbench Ways of Working and Governance v3.pptx |
| 40 | Release plan | The eight epics across eight months, what each release contains, and the gates between them. | Henka slide rules | Recovery Workbench Release Plan v3.pptx, Recovery Workbench Release Plan v3.xlsx |
| 41 | Dependency map | Every dependency on the ACE team, the collection squad, the architecture team, data engineering and the partners, with the date each is needed. | Henka excel rules | Recovery Workbench Dependency Map v2.xlsx |
| 42 | Resource plan and team structure | Who is on the squads, from which organization, for how long, and what each person is accountable for. | Henka excel rules | Recovery Workbench Resource Plan and Team Structure v2.xlsx |
| 53 | Build sequence, Epic 1 and Epic 2 | Stories in pull order with their dependencies, the review windows and the critical path. | Henka excel rules | Recovery Workbench Build Sequence Epic 1 and Epic 2 v4.xlsx |
| 123 | Story build order | The order the stories are built in, with the window each falls in, what each one waits for and the critical path through them. | Henka word rules | Recovery Workbench Story Build Order v1.docx |
| 67 | Risks, assumptions, issues and dependencies | Each one with an owner, a date and the action being taken. | Henka excel rules | Recovery Workbench Risks Assumptions Issues and Dependencies v2.xlsx |
| 103 | Benefit tracking plan | Each benefit with its baseline, its measure, the source of the number, who publishes it and how often. | Henka excel rules | Recovery Workbench Benefit Tracking Plan v2.xlsx |
| 104 | Cutover and go-live plan | The sequence, the rehearsal, the rollback, and who decides to go. | Henka word rules | Recovery Workbench Cutover and Go Live Plan v2.docx |
| 105 | Run operating model | The teams, shifts, service levels, escalation and support tiers that run the Workbench after go-live. | Henka slide rules | Recovery Workbench Run Operating Model v2.docx, Recovery Workbench Run Operating Model v2.pptx |
| 106 | Training and change plan | Who needs to learn what, when, how they are trained, and how readiness is measured. | Henka word rules | Recovery Workbench Training and Change Plan v2.docx, Recovery Workbench Training and Change Plan v2.pptx |

## AI

Read by: Enterprise AI team, Risk and Model Risk, center of excellence.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 4 | AI assisted development approach | How the squads use AI to build: the standards file, the story file, the review step and the quality gates. | Henka word rules | Recovery Workbench AI Assisted Development Approach v1.md, Recovery Workbench AI Assisted Development Approach v3.pptx |
| 56 | AI and agent architecture | Where decisions are automated, where a model advises a person, and where a person decides alone. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench AI and Agent Architecture v2.docx, Recovery Workbench AI and Agent Architecture v2.pptx |
| 82 | Agent catalog and specifications | Each agent: what it watches, what it does, what it may decide alone, what it escalates, and how it is measured. | Henka excel rules | Recovery Workbench Agent Catalog and Specifications v2.md, Recovery Workbench Agent Catalog and Specifications v2.xlsx |
| 86 | Model integration design | Which models are called, with what inputs, how the output is used, and how a model is changed without a release. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Model Integration Design v2.docx |
| 93 | AI decision governance | How an automated decision is recorded, explained, reviewed, challenged and reversed. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench AI Decision Governance v2.docx |

## Business

Read by: Business lead, product heads, process owners, analysts.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 5 | Process architecture | L1 and L2 definitions and the L3 processes, numbered and named. | APQC process classification | Recovery Workbench Process Architecture v3.xlsx, Recovery Workbench Process Architecture v4.pptx |
| 6 | Business architecture | Capabilities, the processes under each, the decisions taken, the partners and the organization that runs it. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Business Architecture v4.pptx |
| 7 | Business rules and routing logic | Every rule that moves a case: event, condition, action, owner, timer, from state and to state, with the completeness checks. | Decision Model and Notation 1.4 | Recovery Workbench Business Rules and Routing Logic v4.html, Recovery Workbench Business Rules and Routing Logic v4.xlsx |
| 8 | Case and workflow model | The stages, milestones, tasks, event listeners and sentries, with the state machine and the case file items. | CMMN 1.1 | Recovery Workbench Case and Workflow Model v5.html, Recovery Workbench Case and Workflow Model v5.xlsx |
| 15 | Target operating model | The future state organization, the work split, spans and layers, and what changes from today. | Henka slide rules | Recovery Workbench Target Operating Model v3.pptx |
| 16 | Users, roles and permissions | Every role, bank, partner, customer and non-human, with the permission per role, the access request and grant flow, and single sign-on mapping. | NIST RBAC | Recovery Workbench Users Roles and Permissions v3.xlsx |
| 21 | Business glossary | Every business term with one definition, the Thai equivalent, and the object or field it maps to. | Domain driven design | Recovery Workbench Business Glossary v2.xlsx |
| 22 | Detailed process flows | Every step in every journey across the actor and system lanes, with the rules that enter and leave each step. | BPMN 2.0 | Recovery Workbench Detailed Process Flows v4.html, Recovery Workbench Detailed Process Flows v4.xlsx |
| 23 | Deviation and exception catalog | Every deviation type: what raises it, what it suspends, who handles it, and how the case returns. | CMMN 1.1 | Recovery Workbench Deviation and Exception Catalog v3.xlsx |
| 24 | Feature list | Every feature in the product, by module, split user, administration and system. | Henka excel rules | Recovery Workbench Feature List v3.xlsx |
| 31 | Case journeys | One page per route: how a case moves from entry to closure. | Henka slide rules | Recovery Workbench Case Journeys v3.pptx |
| 33 | Delegation of authority matrix | Every approval and its limit by role, amount and product, with the substitute when the holder is absent. | NIST RBAC | Recovery Workbench Delegation of Authority Matrix v2.xlsx |
| 43 | Role to system access matrix | Every role against every system, each intersection marked read, write, read and write, or no access, covering bank, partner, customer and non-human roles. | NIST RBAC | Recovery Workbench Role to System Access Matrix v2.xlsx |
| 48 | User journeys | One page per role, bank, partner, customer and administration: the work the person does, the screens they use, how they get access and what they do when something goes wrong. | Henka slide rules | Recovery Workbench User Journeys v2.pptx |
| 58 | Business measures and targets | Every measure with its definition, formula, source, owner and target by quarter. | Henka excel rules | Recovery Workbench Business Measures and Targets v2.xlsx |
| 64 | Partner operating model | How law firms, collection agencies, auction vendors, valuers, buyers and the asset management companies are placed, instructed, paid and measured. | Henka slide rules | Recovery Workbench Partner Operating Model v2.docx, Recovery Workbench Partner Operating Model v2.pptx |
| 115 | Process map | The recovery process as one picture, from first missed payment to close, with the owner of each step. | Henka slide rules | Recovery Workbench Process Map v1.html |

## Data

Read by: Data steward, data engineering, squads.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 9 | Conceptual data model | The subject areas and the data products, and what each one holds. | ISO/IEC/IEEE 29148, bank TSD section T3 | Recovery Workbench Conceptual Data Model v5.pptx, Recovery Workbench Conceptual Data Model v5.xlsx |
| 11 | Logical data model and data dictionary | Every entity with every field: name, type, length, mandatory, default, list of values, key, and the source system each field comes from. | ISO/IEC/IEEE 29148, bank TSD section T3 | Recovery Workbench Logical Data Model and Data Dictionary v6.xlsx |
| 12 | Entity relationship diagram | The entities and their relationships with cardinality, grouped by data product. | IDEF1X notation | Recovery Workbench Entity Relationship Diagram v3.html, Recovery Workbench Entity Relationship Diagram v3.pdf |
| 26 | Physical schema | Create statements with indexes, constraints and seed reference data, for Postgres. | ISO/IEC/IEEE 29148 | Recovery Workbench Physical Schema v4.sql |
| 27 | Volume and scale forecast | Cases, accounts, documents, interactions, decisions and events by product and stage, with the monthly and five year projection and the concurrent user load. Each figure carries its assumption, its source and the effect if the assumption moves. | ISO/IEC 25010 | Recovery Workbench Volume and Scale Forecast v2.pptx, Recovery Workbench Volume and Scale Forecast v2.xlsx |
| 32 | Data classification and personal data inventory | Every field classified by sensitivity, with the personal data fields named and the handling rule for each. | Thai PDPA | Recovery Workbench Data Classification and Personal Data Inventory v3.xlsx |
| 38 | Reference data and lists of values | Every code list with its values, meanings, owner and change process. | ISO/IEC/IEEE 29148, bank TSD section T3 | Recovery Workbench Reference Data and Lists of Values v3.xlsx |
| 46 | Source to target mapping | Each Workbench field mapped to its source field in ACE, Collins, UDP, SCBPDM, EFS and corebank, with the transformation and the refresh. | ISO/IEC/IEEE 29148, bank TSD section T3 | Recovery Workbench Source to Target Mapping v3.xlsx |
| 60 | Data ownership and stewardship | Who owns each data product, who may change it, and how a change is requested. | Henka excel rules | Recovery Workbench Data Ownership and Stewardship v2.xlsx |
| 61 | Data quality and reconciliation rules | What is checked on each load, the tolerance, and what happens when a check fails. | ISO/IEC/IEEE 29148, bank TSD section T3 | Recovery Workbench Data Quality and Reconciliation Rules v2.xlsx |
| 65 | Party and customer master data design | How one customer, guarantor or partner is identified across systems, and how duplicates are resolved. | ISO/IEC/IEEE 29148, bank TSD section T3 | Recovery Workbench Party and Customer Master Data Design v2.docx, Recovery Workbench Party and Customer Master Data Design v2.xlsx |
| 89 | Reporting and analytics data model | The measures, dimensions and refresh for management reporting, and where each number comes from. | ISO/IEC/IEEE 29148, bank TSD section T3 | Recovery Workbench Reporting and Analytics Data Model v2.xlsx |
| 99 | Data migration approach | What moves, how much history, what happens to cases in flight, and whether there is a parallel run. | Henka word rules | Recovery Workbench Data Migration Approach v2.docx |

## Technical

Read by: TechX squads, ACE team, solution architect.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 10 | Information flow | Where each piece of information comes from, how it reaches the Workbench, how often, and what happens when it does not arrive. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Information Flow v4.pptx |
| 14 | Target architecture, all eight epics | The architecture on ACE: modular monolith, one service, one repository, one front end, the case workflow layer, and what each epic adds. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Target Architecture v4.docx, Recovery Workbench Target Architecture v4.pptx |
| 20 | Architecture decision records | One page per decision taken: the workflow approach, the module structure, the front end split, the integration route. | MADR | Recovery Workbench Architecture Decision Records v1.md |
| 25 | System disposition and integration inventory | Every system recovery uses today, what happens to each and when, and every interface with its route, direction and frequency. | OpenAPI 3.1, AsyncAPI 3.0 | Recovery Workbench System Disposition and Integration Inventory v2.xlsx |
| 34 | Environment and deployment design | The environments, the namespaces, the pipeline, the feature flag approach, the branching model and the release path. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Environment and Deployment Design v2.docx |
| 36 | Interface specifications | Per interface: approach, trigger, payload fields, frequency, volume, error handling, retry and owner. | OpenAPI 3.1, AsyncAPI 3.0 | Recovery Workbench Interface Specifications v2.md, Recovery Workbench Interface Specifications v2.xlsx |
| 45 | Security and access design | Single sign-on, identity and access management, the permission check, personal data masking and the session rules. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Security and Access Design v2.docx |
| 57 | API specification | Every endpoint: method, path, request, response, error codes and authorization. | OpenAPI 3.1 | Recovery Workbench API Specification v2.html, Recovery Workbench API Specification v2.yaml |
| 63 | Event and messaging design | Every event the Workbench publishes and consumes, the payload, the order guarantee and the duplicate handling. | AsyncAPI 3.0 | Recovery Workbench Event and Messaging Design v2.md, Recovery Workbench Event and Messaging Design v2.xlsx |
| 68 | Rules engine design | How the rules are authored, versioned, tested, deployed and rolled back, and how a decision is recorded. | Decision Model and Notation 1.4 | Recovery Workbench Rules Engine Design v2.docx |
| 71 | Workflow engine design | How the case model runs: stages, tasks, sentries and timers, and how a case in flight survives a change to the model. | CMMN 1.1 | Recovery Workbench Workflow Engine Design v2.docx |
| 72 | Audit and logging design | What is logged, in what form, where it is held, who can read it, and how an action is traced end to end. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Audit and Logging Design v2.docx |
| 74 | Batch and scheduling design | Every scheduled job: what it does, when it runs, what it depends on, and what happens when it fails or runs late. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Batch and Scheduling Design v2.docx, Recovery Workbench Batch and Scheduling Design v2.xlsx |
| 76 | Document management design | Storage, indexing, extraction, attachment to a case, versions, physical originals and custody. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Document Management Design v2.docx |
| 77 | Error handling and resilience standard | How every failure is caught, retried, reported and recovered, and what the user sees meanwhile. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Error Handling and Resilience Standard v2.docx |
| 79 | Notification and correspondence design | How letters, messages and alerts are generated, approved, sent, tracked and proved. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Notification and Correspondence Design v2.docx |
| 83 | Availability, performance and recovery design | The service levels, the scaling approach, the backup and the recovery time and point objectives. | ISO/IEC 25010 | Recovery Workbench Availability Performance and Recovery Design v2.docx |
| 87 | Observability and monitoring design | What is measured, what raises an alert, who receives it, and the dashboards that show the system is healthy. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Observability and Monitoring Design v2.docx |
| 92 | Technical specification per module | Components, data model, state machine, interfaces, access control and API endpoints, one per module. | Bank TSD template | Recovery Workbench Technical Specifications by Module v3.zip |
| 113 | ACE architecture decision | The decision to build the Workbench inside ACE, with the workflow, structure and data options compared. | ISO/IEC/IEEE 42010 | Recovery Workbench ACE Architecture Decision v2.docx |

## Communication

Read by: Sponsors, executives, all teams.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 13 | Project overview | What the Workbench is, the problem it solves, what changes, the plan and the benefits, for any audience in ten minutes. | Henka slide rules | Recovery Workbench Project Overview v4.docx, Recovery Workbench Project Overview v4.pptx |
| 37 | Recovery Workbench project deck | The full account: today, the target, the process, the architecture, the data, the eight epics, the organization and the plan. | Henka slide rules | Recovery Workbench Project Deck v3.pptx |
| 47 | Stakeholder map and communication plan | Who needs to know what, how often, through which forum, and who tells them. | Henka excel rules | Recovery Workbench Stakeholder Map and Communication Plan v3.xlsx |
| 54 | Team start pack | What the Workbench is, how the work runs, and what each role does in the first month. | Henka slide rules | Recovery Workbench Team Start Pack v2.html, Recovery Workbench Team Start Pack v2.pptx |
| 70 | Weekly status pack | Progress against the plan, what is blocked, what is decided and what is needed, in one page per workstream. | Henka slide rules | Recovery Workbench Weekly Status Pack v2.pptx |
| 107 | Executive presentation, CEO | The outcome, the plan, the benefits and the decisions needed. | Henka slide rules | Recovery Workbench Executive Presentation CEO v2.pptx |
| 108 | Executive presentation, CTO | The architecture, the data, the integration and the build approach. | C4 model, arc42, ISO/IEC/IEEE 42010 | Recovery Workbench Executive Presentation CTO v3.pptx |
| 110 | Document index | Every asset, who reads it, and where it is. | Henka word rules | Recovery Workbench Document Index v11.md |
| 114 | Document control sheet | Every document with its upload priority, reviewer, sign-off owner and status. | Henka excel rules | Recovery Workbench Document Control Sheet v10.xlsx |
| 116 | Project hub for the squads | Every story, build note, code, term and original file in one page that works with no network and no sign-in. | Henka writing rules | Recovery Workbench Project Hub v14.html |

## Backlog

Read by: Squads, analysts, product owner.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 17 | User story, worked example | One story in the agreed format, as the template the three parties lock for the next releases. | Connextra form, INVEST, Gherkin | Recovery Workbench User Story Worked Example v6.md |
| 49 | Administration stories | User and role administration, reference data, rule versions, queue and timer configuration, interface monitoring and the audit log. | Connextra form, INVEST, Gherkin | Recovery Workbench Administration Stories v2.md, Recovery Workbench Administration Stories v2.xlsx |
| 51 | Technical enabler stories | Stories with no business user that the Epic 1 and Epic 2 stories build on, in the same format. | Connextra form, INVEST, Gherkin | Recovery Workbench Technical Enabler Stories v5.md, Recovery Workbench Technical Enabler Stories v5.xlsx |
| 52 | User stories, Epic 1 | Every Epic 1 story for build: requirement IDs, business rationale, preconditions, flow, exception paths, acceptance criteria, rules, data with field IDs, contract, solution plan, messages, screens, tests and traceability. One file, a workbook and one file per story. | Connextra form, INVEST, Gherkin | Recovery Workbench User Stories Epic 1 Story Files v5.zip, Recovery Workbench User Stories Epic 1 v7.md, Recovery Workbench User Stories Epic 1 v7.xlsx |
| 55 | User stories, Epic 2 | The same for Epic 2, with the three agent stories that go live in Epic 3. | Connextra form, INVEST, Gherkin | Recovery Workbench User Stories Epic 2 Story Files v4.zip, Recovery Workbench User Stories Epic 2 v5.md, Recovery Workbench User Stories Epic 2 v5.xlsx |
| 101 | Data migration stories | Extract, transform, load, reconcile and cut over, one story per data product. | Connextra form, INVEST, Gherkin | Recovery Workbench Data Migration Stories v2.md, Recovery Workbench Data Migration Stories v2.xlsx |
| 109 | User stories, Epics 3 to 8 | Step by step detail for each epic, written one epic ahead of its build month. | Connextra form, INVEST, Gherkin | Recovery Workbench User Stories Epics 3 to 8 v2.md, Recovery Workbench User Stories Epics 3 to 8 v2.xlsx |
| 117 | How to read the acceptance criteria | How a Given, When, Then line is read, what each keyword means, and the twelve patterns the criteria use, written for a reader whose first language is not English. | Gherkin | Recovery Workbench How To Read The Acceptance Criteria v1.docx |
| 118 | Acceptance criteria glossary | Every term and code that appears in the acceptance criteria, with its meaning in English and Thai. | Henka excel rules | Recovery Workbench Acceptance Criteria Glossary v1.xlsx |
| 119 | Build notes, Epic 1 | Every flow step of every Epic 1 story written out in full: who acts, what runs on its own, and what has to be built. | Henka writing rules | Recovery Workbench Build Notes Epic 1 v4.md |
| 120 | Build notes, Epic 2 | Every flow step of every Epic 2 story written out in full, in the same form as the Epic 1 notes. | Henka writing rules | Recovery Workbench Build Notes Epic 2 v2.md |
| 122 | Build notes, technical enablers | Every flow step of the 13 technical enabler stories written out in full. | Henka writing rules | Recovery Workbench Build Notes Technical Enablers v1.md |
| 121 | Story defects | Every contradiction found inside a story by reading each flow step against the rest of that story, with its status and who rules on it. | Henka excel rules | Recovery Workbench Story Defects Epic 1 Epic 2 and Enablers v2.xlsx |

## Quality

Read by: QA engineers, business testers.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 18 | Definition of ready and definition of done | What a story carries before it is built, and what is true before it is accepted. | Henka word rules | Recovery Workbench Definition of Ready and Done v3.docx |
| 69 | Test strategy | The levels, the environments, the entry and exit criteria, the data, and who tests what. | ISO/IEC/IEEE 29119 | Recovery Workbench Test Strategy v2.docx |
| 84 | Defect management process | How a defect is raised, graded, assigned, fixed, retested and closed, and the severity definitions. | Henka word rules | Recovery Workbench Defect Management Process v2.docx |
| 95 | Non-functional test plan | How performance, load, resilience, security and penetration testing are run, and the pass marks. | ISO/IEC/IEEE 29119 | Recovery Workbench Non Functional Test Plan v2.docx |
| 96 | Test cases | Cases from the stories and the routing rules, with expected results and traceability. | ISO/IEC/IEEE 29119 | Recovery Workbench Test Cases v5.xlsx |
| 97 | Requirements traceability matrix | Requirement to feature to story to specification section to test, with priority and acceptance criteria. | Bank RTM template | Recovery Workbench Requirements Traceability Matrix v4.xlsx |
| 98 | Test data plan | The data each test needs, where it comes from, and how personal data is handled. | ISO/IEC/IEEE 29119 | Recovery Workbench Test Data Plan v2.docx |
| 100 | User acceptance test plan and scripts | What the business tests, in what order, with the script for each case and the sign-off. | ISO/IEC/IEEE 29119 | Recovery Workbench User Acceptance Test Plan v2.docx, Recovery Workbench User Acceptance Test Scripts v2.xlsx |
| 102 | Regression suite | The cases that run on every release, and how the suite grows as modules are added. | ISO/IEC/IEEE 29119 | Recovery Workbench Regression Suite v5.xlsx |

## Requirements

Read by: Squads, analysts, QA engineers.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 28 | Business requirements, program | Scope, outcomes, the process architecture, the requirements and the non-functional requirements across all eight epics. | ISO/IEC/IEEE 29148 | Recovery Workbench Business Requirements Program v3.docx |
| 29 | Business requirements, Epic 1 | The requirements at development detail, with the user benefit and the support needed from users. | ISO/IEC/IEEE 29148 | Recovery Workbench Business Requirements Epic 1 v3.docx |
| 30 | Business requirements, Epic 2 | The requirements at development detail, with the user benefit and the support needed from users. | ISO/IEC/IEEE 29148 | Recovery Workbench Business Requirements Epic 2 v2.docx |
| 50 | Non-functional specification | Targets with a measure and a test for each, with volumes, concurrency, growth and external partner access. | ISO/IEC 25010 | Recovery Workbench Non Functional Specification v2.docx |
| 78 | Functional specification per module | What each module does: screens, fields, business rules, validation, messages and the process steps it serves. | Bank FSD template | Recovery Workbench Functional Specifications by Module v4.zip |
| 85 | Epics 3 to 8 at specification level | Each remaining epic at architecture, API and integration detail. | ISO/IEC/IEEE 29148 | Recovery Workbench Epics 3 to 8 Specification v2.docx, Recovery Workbench Epics 3 to 8 Specification v2.xlsx |
| 90 | Reporting and management information requirements | Every report and dashboard: who reads it, what decision it supports, the measures on it and the refresh. | ISO/IEC/IEEE 29148 | Recovery Workbench Reporting and Management Information Requirements v2.docx, Recovery Workbench Reporting and Management Information Requirements v2.xlsx |
| 111 | Lean BRD, Epic 1 | The business scope of Epic 1 for sign-off: problem and outcome, scope, rules, process ownership, constraints, dependencies and success measures. | ISO/IEC/IEEE 29148 | Recovery Workbench Lean BRD Epic 1 v2.docx |
| 112 | Lean BRD, Epic 2 | The business scope of Epic 2 for sign-off: problem and outcome, scope, rules, process ownership, constraints, dependencies and success measures. | ISO/IEC/IEEE 29148 | Recovery Workbench Lean BRD Epic 2 v2.docx |

## Experience

Read by: Front end developers, analysts, business testers.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 35 | Error and message standard | The wording pattern for every error, warning and confirmation, in Thai and English, with the rules that raise each one. | Henka word rules | Recovery Workbench Error and Message Standard v3.docx |
| 44 | Screen inventory and navigation | Every screen, who reaches it, from where, and what it is for. | Henka excel rules | Recovery Workbench Screen Inventory and Navigation v2.xlsx |
| 62 | Design system and component library | The components, states, spacing, type and color the screens are built from. | Bank web standards | Recovery Workbench Design System and Component Library v1.html |
| 75 | Content and label standard | Every label, heading, button and help text in Thai and English, matched to the business glossary. | Domain driven design | Recovery Workbench Content and Label Standard v2.xlsx |
| 80 | Screen specifications | Each screen with its fields, states, validation and messages, attached to the stories that build it. | Connextra form, INVEST, Gherkin | Recovery Workbench Screen Specifications v1.html, Recovery Workbench Screen Specifications v1.md |
| 81 | Accessibility standard | The level the screens meet, the rules that follow from it, and how each screen is checked. | WCAG 2.2 AA | Recovery Workbench Accessibility Standard v2.docx |
| 91 | Screen prototype | Working screens for the developers and the business to use before the build. | Bank web standards | Recovery Workbench Screen Prototype v1.html |
| 94 | Customer and partner correspondence templates | Every letter, notice and message sent outside the bank, with the fields that fill it and the approval it needs. | Henka word rules | Recovery Workbench Customer and Partner Correspondence Templates v2.docx |

## Policy

Read by: Compliance, Risk, internal audit, Legal.

| # | Document | What it is | Standard | Files |
|---|---|---|---|---|
| 39 | Regulatory requirements map | Each regulatory obligation mapped to the process step, the rule and the control that satisfies it. | ISO/IEC/IEEE 29148 | Recovery Workbench Regulatory Requirements Map v2.xlsx |
| 59 | Controls catalog | Every control point on the process: what it checks, who performs it, the evidence it produces and how it is tested. | Henka excel rules | Recovery Workbench Controls Catalog v2.xlsx |
| 66 | Personal data protection design | What personal data is held, the lawful basis, consent, masking, access, retention and the subject rights path. | Thai PDPA | Recovery Workbench Personal Data Protection Design v2.docx |
| 73 | Audit findings response map | Each open audit finding mapped to the change in the Workbench that closes it. | Henka excel rules | Recovery Workbench Audit Findings Response Map v2.xlsx |
| 88 | Records retention and archiving | How long each record and document is held, where it moves, and when it is destroyed. | Thai PDPA, bank policy | Recovery Workbench Records Retention and Archiving v2.docx |

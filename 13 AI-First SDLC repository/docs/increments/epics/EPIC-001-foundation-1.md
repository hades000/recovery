# Epic Increment Card — EPIC-001 Foundation 1

## Identification

| Field | Value |
|---|---|
| Epic ID | `EPIC-001` |
| Title | Epic 1 — Foundation 1: one case list, case record, documents and decision log |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1` (Jira project and issue keys TBC — `CTX-GAP-023`) |
| Story increments | 78 story cards, `INC-001-epic-1-RWB-E1-044.md` to `INC-078-epic-1-RWB-E1-055.md` (see `INDEX.md`) |
| RUN_ID | Not applicable at epic level; each story card carries its own RUN_ID |
| Status | In delivery |

## Project type (playbook section 2.2)

| Question | Answer |
|---|---|
| Is this a completely new capability? | Yes for the Workbench module; it is new product capability inside an existing platform. |
| Does a running application already exist? | Yes — ACE, the bank's collection engine. |
| Are business requirements documented and approved? | Yes — Lean BRD Epic 1 v2, Business Requirements Epic 1 v3, Business Requirements Program v3. |
| Is business logic embedded mainly in source code? | No. The business rules are 448 versioned data rows; the case model is documented. |
| Is the goal enhancement, replacement, modernisation or upgrade? | New product capability on an existing platform, with integration constraints. |
| Is the target technology already approved? | Yes — Spring Boot/Java, React/Vite, PostgreSQL, Entra ID, ACE AKS. |
| Is there a current architecture and dependency inventory? | Yes — Target Architecture v4, ADRs, System Disposition and Integration Inventory v2. |
| Are user journeys and design-system standards available? | Yes — User Journeys v2, Case Journeys v3, Design System v1, Screen Inventory v2, Screen Specifications v1. |
| Is the change primarily integration or localisation? | Neither; it is a product build with heavy integration. |
| Is a production-safe rollback path available? | Yes — feature flags (ADR-008) and rollback by previous tag (NFR-027). |
| Which lifecycle artefacts can be reused? | Discovery, BRDs, PRDs/FSDs, architecture, ADRs, data model, API spec, test strategy, engineering practices. |
| Which artefacts must be recovered or regenerated? | A canonical Epic 1 requirement file and a per-story specification; no approved Figma file. |

**Selected path:** Greenfield development for the new Workbench module, with brownfield ACE
integration constraints. Recorded per the playbook rule to classify the increment, not the programme.

**Starting context:** Approved Epic 1 business requirements, Lean BRD, FSD/TSD modules P1–P10,
Target Architecture, nine ADRs, logical data model, physical schema, API specification, 448 routing
rules and the Epic 1 story files.

## Scope

**In scope**

- P1 recovery data engine: 14 data products, ALS/EFS/CCMS/SVAF loads, file loads, data quality,
  reconciliation, freshness, access control, interaction ledger.
- P2 integration: adapter pattern, ADF/Control-M jobs, run books and monitoring.
- P3 case and workflow core: case creation, case ID, state model, queues, allocation, assignment,
  transfer, service levels, timers, prescription dates, rule load and rollback, rebalancing, case list
  and read-only case record view.
- P4 access: Entra ID SSO/MFA, first roles, role-to-permission matrix, PDPA masking, delegation of
  authority, access log, break-glass admin.
- P5 document hub: store and index, six document types, OCR, classification, field extraction, review
  queue, retention classes, virus scan, intake from branches/mailroom/SFTP/email.
- P6 communications: notice generation v1, template and merge field catalogue, proof-of-delivery
  capture design with WIN.
- P7 decision centre and log: append-only hash-chained store, writer v1.
- P9 reporting: baseline measures.
- P10 agent runtime: platform set-up, case intake agent in shadow, extraction evaluation, deviation
  screening agent in shadow, monitoring dashboard.
- Cross-cutting: configuration service, reference data service, multi-product parameters, feature
  flags, migrations, rule change audit, data dictionary, sandbox, synthetic data, masked data in
  SIT/UAT.

**Out of scope**

- E2 queue and transfer screens, approval routing, steering dashboard, treatment record, notice
  approval and deviation screening live.
- E3–E8: settlement/deed in lieu booking, route decision, guarantees, litigation full, assets, debt
  sale, write-off, full administration.
- Partner portal screens beyond identities needed for later epics.
- Any change to collections before day 90 or to ACE common module internals.

**Business outcome and value hypothesis:** One case list for every account at 90+ days past due,
reconciled to the core bank; documents found by case; every decision recorded once; allocation,
assignment and transfer by rule. The value hypothesis is that one list, one owner and one decision
record remove the spreadsheet hand-off and make the 2027 turnaround and audit targets achievable.

**Constraints:** ACE one service/repository/front end; modular monolith boundaries; CMMN 1.1; rules as
data; COLLINS daily batch and file loads; PostgreSQL; monthly release; PDPA; no production data in
prompts or tests.

## Reused approved artefacts

| Artefact | Owner | Version / link | Confirmed suitable for this increment (by, date) |
|---|---|---|---|
| Lean BRD Epic 1 | Business lead | v2, `docs/brds/lean-brd-epic-1.md` | TBC |
| Business Requirements Epic 1 | Product owner | v3, `docs/brds/business-requirements-epic-1.md` | TBC |
| Business Requirements Program | Product owner | v3, `docs/brds/business-requirements-program.md` | TBC |
| FSD P1–P10 | Solution architect | v2, `docs/prds/` | TBC |
| TSD P1–P10 | Solution architect | v2, `requirement/legacy/05-technical-architecture/` | TBC |
| Target Architecture | Solution architect | v4, `docs/architecture/decisions/` and legacy | TBC |
| ADR-001 to ADR-009 | Solution architect | v1, `docs/architecture/decisions/` | TBC |
| Logical Data Model and Data Dictionary | Data steward | v6, `requirement/legacy/06-data/` | TBC |
| Physical Schema | Data steward | v4, `requirement/legacy/06-data/recovery-workbench-physical-schema-v4.sql` | TBC |
| API Specification | Solution architect | v2, `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v2.yaml` | TBC |
| Business Rules and Routing Logic | Centre of excellence | v4, `requirement/legacy/02-business-architecture-and-process/` | TBC |
| Users, Roles and Permissions | Security administrator | v3, `requirement/legacy/02-business-architecture-and-process/` | TBC |
| Error and Message Standard | Business lead | v3, `requirement/legacy/07-screens-and-experience/` | TBC |
| Test Strategy | QA lead | v2, `requirement/legacy/09-testing-and-quality/` | TBC |
| Definition of Ready and Done | Product owner | v3, `requirement/legacy/09-testing-and-quality/` | TBC |
| Engineering Practices | Tech lead | v4, `requirement/legacy/11-delivery-and-operations/` | TBC |
| AI Assisted Development Approach | Solution architect | v1, `AGENTS.md` and legacy | TBC |

## Lifecycle tailoring

Link to the completed record: `docs/increments/epics/EPIC-001-tailoring.md` (shared by all Epic 1
story cards).

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Intake approval | Product Owner | TBC | |
| Context readiness | Forward Deployed Engineer | TBC | |
| Requirements approval (BRD / PRD) | Product Owner, FDA | TBC | |
| Design and architecture approval | Forward Deployed Architect | TBC | |
| Backlog and specification approval | Product Owner | TBC | |
| Plan approval | Forward Deployed Architect | TBC | |
| Task approval | Forward Deployed Engineer | TBC | |
| Pull request approval (code review) | Forward Deployed Engineer | TBC | |
| Quality and security gate | FDA, Quality Engineer, Security | TBC | |
| Release readiness | Forward Deployed Engineer | TBC | |
| Deployment approval | Product Owner / PM | TBC | |
| Operate and learn review | Ops / System Manager | TBC | |

## Agents selected (playbook section 2.5)

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder | Applicable | Creates the context package from the document set. |
| Requirements and discovery | BRD Builder | Not used | Lean BRD Epic 1 v2 is approved; reuse it. |
| Requirements and discovery | PRD Builder | Not used | FSD P1–P10 v2 are approved; reuse them. |
| Design, backlog and spec | Jira Backlog Manager | Optional | The local backlog is the story files; Jira import is TBC. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec per story. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md` per story. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in the ACE repository. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Conditional | Applies when `API In Scope: YES`. |
| Quality and release | Functional Automation Test | Conditional | Applies when `UI In Scope: YES`. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline; no Azure Deploy agent. |

## Risk, rollback and stop signals

- **Rollback route:** every unfinished or cross-squad change is behind a feature flag (ADR-008); a
  release rolls back by redeploying the previous tag (NFR-027).
- **Feature-control / coexistence strategy:** the Workbench coexists with EFS, Excel and SharePoint
  until the case list is reconciled and the local copies are retired (RWB-E1-012).
- **Stop and rollback signals:** case list variance to ALS is unexplained; a COLLINS or file load
  fails its control total; a decision log write fails; a data quality rule breaches its tolerance;
  a security or PDPA test fails; SIT has an open severity 1 or 2.
- **Open risks:** R-01 late data, R-02 weekly/monthly collateral data, R-03 cross-squad release
  contention, R-04 new rules component, R-05 volume growth, R-08 deployment slots, R-10 business
  tester availability, R-11 Thai wording, R-12 model endpoint.
- **Key dependencies:** DEP-01 module folder, DEP-02 code owners, DEP-03 deployment slots, DEP-04
  common services, DEP-05 release window, DEP-11 model endpoint, DEP-12 NFR targets.

## Story increments

The 78 Epic 1 story cards are in `docs/increments/` and indexed in `docs/increments/INDEX.md`.
Each card carries its own `RUN_ID`, its own scope and approvals, and links back to this epic card and
`EPIC-001-tailoring.md`. The epic card and tailoring record are shared; do not duplicate them per
story.

## Evidence links

| Evidence | Location |
|---|---|
| Story cards | `docs/increments/INC-<NNN>-epic-1-<KEY>.md` and `docs/increments/INDEX.md` |
| Specification | `output/INC-<NNN>-epic-1-<KEY>/specify/spec.md` |
| Plan and tasks | `output/INC-<NNN>-epic-1-<KEY>/plan/` |
| Implementation evidence | `output/INC-<NNN>-epic-1-<KEY>/implement/` |
| API / functional test reports | `output/INC-<NNN>-epic-1-<KEY>/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-<NNN>-epic-1-<KEY>/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |
| Release and deployment logs | TBC — ACE pipeline |

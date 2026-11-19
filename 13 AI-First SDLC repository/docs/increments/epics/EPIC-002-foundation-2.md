# Epic Increment Card — EPIC-002 Foundation 2

## Identification

| Field | Value |
|---|---|
| Epic ID | `EPIC-002` |
| Title | Epic 2 — Foundation 2: one owner and timer, full history, approvals, notices and steering |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E2` / `RWB-E2` (Jira project and issue keys TBC — `CTX-GAP-023`) |
| Story increments | None yet; assigned when the Epic 2 specification batch starts |
| RUN_ID | Not applicable at epic level; each story card will carry its own RUN_ID |
| Status | Mobilised |

## Project type (playbook section 2.2)

| Question | Answer |
|---|---|
| Is this a completely new capability? | It extends the Workbench module delivered in EPIC-001. |
| Does a running application already exist? | Yes — ACE, plus the Epic 1 Workbench increment. |
| Are business requirements documented and approved? | Yes — Business Requirements Epic 2 v2; Business Requirements Program v3. |
| Is business logic embedded mainly in source code? | No. Rules, queues, timers and templates are versioned data. |
| Is the goal enhancement, replacement, modernisation or upgrade? | Enhancement of the Workbench module on ACE. |
| Is the target technology already approved? | Yes — the Epic 1 stack. |
| Is there a current architecture and dependency inventory? | Yes — Target Architecture v4, ADRs, Epic 1 implementation evidence. |
| Are user journeys and design-system standards available? | Yes — User Journeys v2, Case Journeys v3, Design System v1, Screen Inventory v2, Screen Specifications v1. |
| Is the change primarily integration or localisation? | Enhancement with partner identity and notice-dispatch integration. |
| Is a production-safe rollback path available? | Yes — feature flags and rollback by previous tag. |
| Which lifecycle artefacts can be reused? | Epic 1 context, BRDs, FSD/TSD, ADRs, data model, API spec, test strategy, engineering practices, and the Epic 1 implementation. |
| Which artefacts must be recovered or regenerated? | The Epic 2 canonical requirement file and per-story specifications; no approved Figma file. |

**Selected path:** Brownfield enhancement of the Workbench module, with the ACE integration
constraints retained. The epic is classified separately from EPIC-001.

**Starting context:** Epic 1 released; Epic 2 business requirements v2; the Epic 2 story files;
the shared Epic 2 items with the collection squad (notice path, contact stop, shared tasks); the
partner identity design; the treatment record and notice approval designs.

## Scope

**In scope**

- P3 queue and transfer screens: my work, team queues, transfer with reason, service-level visibility,
  next action, case timeline.
- P4 partner identities: partner user accounts, partner scope, partner access checks.
- P5 document generation: document generation from templates, document custody, template approval.
- P6 dispatch and proof of delivery: WIN dispatch, proof-of-delivery write-back, contact stop.
- P7 approval routing: approval queue, decision screen, delegation check, separation of duty.
- P8 matching skeleton: receipt matching and unmatched exception list.
- P9 steering dashboard: inflow, stock, cures, recovery, turnaround and cost.
- S2 treatment record foundations: treatment record, plan timers, treatment status.
- S4 notice approval: demand and recall notices, legal approval, dispatch.
- S8 deviation screening: X1–X7 screening at entry and on events, in shadow/live as approved.
- Shared Epic 2 items with the collection squad: notice path, customer contact stop, shared tasks.

**Out of scope**

- E3–E8: settlement/deed in lieu booking, route decision, guarantees, litigation full, assets, debt
  sale, write-off, full administration.
- Partner portal full screens beyond identities and the notice path.
- Any change to collections before day 90 or to ACE common module internals.

**Business outcome and value hypothesis:** One owner and a timer on every case; full history on one
screen; approval routing within the delegation; litigation notices generated, approved and dispatched
with proof of delivery; a steering dashboard. The value hypothesis is that the case owner stops
assembling history from four systems and the approval and notice paths become auditable by default.

**Constraints:** the Epic 1 constraints continue. The collection squad shares the notice path, contact
stop and shared tasks; the split is under DL30. Partner identities need the partner access design;
external partner access is not live until E5 (DL03).

## Reused approved artefacts

| Artefact | Owner | Version / link | Confirmed suitable for this increment (by, date) |
|---|---|---|---|
| Business Requirements Epic 2 | Product owner | v2, `docs/brds/business-requirements-epic-2.md` | TBC |
| Business Requirements Program | Product owner | v3, `docs/brds/business-requirements-program.md` | TBC |
| FSD P1–P10 / S1–S9 | Solution architect | v2, `docs/prds/` | TBC |
| TSD P1–P10 / S1–S9 | Solution architect | v2, `requirement/legacy/05-technical-architecture/` | TBC |
| Target Architecture / ADRs | Solution architect | v4 / v1, `docs/architecture/decisions/` | TBC |
| Epic 1 implementation evidence | FDE | `output/INC-001..INC-078` from EPIC-001 | TBC |
| Users, Roles and Permissions | Security administrator | v3, `requirement/legacy/02-business-architecture-and-process/` | TBC |
| Error and Message Standard | Business lead | v3, `requirement/legacy/07-screens-and-experience/` | TBC |
| Test Strategy / DoR and DoD | QA lead / product owner | v2 / v3, `requirement/legacy/09-testing-and-quality/` | TBC |
| Engineering Practices / AI standards | Tech lead / solution architect | v4 / v1, `AGENTS.md` | TBC |

## Lifecycle tailoring

Link to the completed record: `docs/increments/epics/EPIC-002-tailoring.md`.

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
| Requirements and discovery | Context Builder | Not used | The context package from EPIC-001 is current; use Context Updater for the Epic 2 delta. |
| Requirements and discovery | BRD Builder | Not used | Business Requirements Epic 2 v2 is approved. |
| Requirements and discovery | PRD Builder | Not used | FSD/TSD modules are approved. |
| Design, backlog and spec | Jira Backlog Manager | Optional | The local backlog is the story files; Jira import is TBC. |
| Design, backlog and spec | Technical Specifier | Applicable | Per-story specification. |
| Plan and build | Implementation Planner | Applicable | Plan and tasks. |
| Plan and build | Implementation Builder | Applicable | Build the approved plan. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Conditional | When `API In Scope: YES`. |
| Quality and release | Functional Automation Test | Conditional | When `UI In Scope: YES`. |
| Quality and release | Azure Deploy pipeline | Not used | ACE pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flags (ADR-008); rollback by previous tag (NFR-027).
- **Coexistence:** the Epic 1 case list and decision log remain the source; Epic 2 adds ownership,
  timers, approvals and notices without replacing them.
- **Stop signals:** shared-item split with the collection squad unresolved (DL30); partner identity
  design not approved; notice template not approved by Legal; contact stop not enforced; SIT severity
  1 or 2 open.
- **Open risks:** R-03 cross-squad release contention, R-06 partner access timeline, R-10 business
  tester availability, R-11 Thai wording, R-12 model endpoint.
- **Key dependencies:** DEP-06 restructure calculator and plan status, DEP-07 EFS hand-over data,
  DEP-08 shared Epic 2 items with the collection squad.

## Evidence links

| Evidence | Location |
|---|---|
| Story cards | Not created yet; see `docs/increments/INDEX.md` when the Epic 2 batch starts |
| Specification | `output/INC-<NNN>-epic-2-<KEY>/specify/spec.md` when available |
| Plan and tasks | `output/INC-<NNN>-epic-2-<KEY>/plan/` when available |
| Implementation evidence | `output/INC-<NNN>-epic-2-<KEY>/implement/` when available |
| API / functional test reports | `output/INC-<NNN>-epic-2-<KEY>/api-tests/`, `functional-tests/` when available |
| Review findings | `output/INC-<NNN>-epic-2-<KEY>/review/` when available |
| Traceability | `requirement/Traceability_Matrix.md` |
| Release and deployment logs | TBC — ACE pipeline |

# Epic Increment Card — EPIC-001 Foundation 1

## Identification

| Field | Value |
|---|---|
| Epic ID | `EPIC-001` |
| Title | Foundation 1: case list, case record, documents, decision log and the ACE data read path |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-*`, `RWB-TE-*` |
| Story increments | 72 active cards, `INC-001` to `INC-072` (see `../INDEX.md`) |
| RUN_ID | Not applicable at epic level; each story card carries its own RUN_ID |
| Release | 30 November 2026 |
| Status | In delivery |
| Baseline | Document set v14, 16 November 2026 |

## Project type

| Question | Answer |
|---|---|
| Is this a completely new capability? | Yes for the Workbench module; it is new product capability inside an existing platform. |
| Does a running application already exist? | Yes — ACE, the bank's collection engine. |
| Are business requirements documented and approved? | Yes — Lean BRD Epic 1 v3, Business Requirements Epic 1 v4, Business Requirements Program v4. |
| Is business logic embedded mainly in source code? | No. Rules remain versioned data; from Epic 3 they are authored as Drools XLS packages (ADR-012). |
| Is the goal enhancement, replacement, modernisation or upgrade? | New product capability on an existing platform, with integration constraints. |
| Is the target technology already approved? | Yes — Spring Boot/Java, React/Vite, PostgreSQL, Entra ID, ACE AKS, Temporal and embedded Drools. |
| Is there a current architecture and dependency inventory? | Yes — Target Architecture v6, ADR-001–012, System Disposition and Integration Inventory v3. |
| Are journeys and design standards available? | Yes — User Journeys v2, Case Journeys v3, Design System v1, Screen Inventory v2, Screen Specifications v1. |
| Is the change primarily integration or localisation? | Neither; it is a product build with a read-only ACE data boundary. |
| Is a production-safe rollback path available? | Yes — feature flags (ADR-008) and rollback by previous tag (NFR-027). |
| Which lifecycle artefacts can be reused? | Discovery, BRDs, FSDs, architecture, ADRs, data model, API specification, test strategy, engineering practices. |
| Which artefacts must be recovered or regenerated? | Per-story specifications and plans after the 15–16 November re-baseline. |

**Selected path:** Greenfield development for the new Workbench module, with brownfield ACE integration constraints.

## Scope

**In scope**

- **P1 Recovery data engine** — recovery tables, the read-only `recovery.v_ace_*` views and grants, data dictionary, synthetic sandbox, access control per data product, freshness, reconciliation, interaction ledger.
- **P2 Integration** — outbound-only adapters, outbox and retry, run books and monitoring.
- **P3 Case and workflow** — configuration service and parameter catalog, reference data, case ID and record, allocation/assignment, transfer, service levels and timers, rebalancing, case list and read-only case record, Temporal platform and worker, Drools runtime and package store, rule authoring and rollback.
- **P4 Access** — Entra ID SSO/MFA, roles, role-to-permission matrix, PDPA masking, delegation of authority, access log and break-glass admin.
- **P5 Document hub** — store and index, document types, OCR, classification, extraction, review queue, retention and virus scan, intake.
- **P6 Communications** — notice generation, template and merge-field catalog, proof-of-delivery design.
- **P7 Decision centre and log** — append-only hash-chained store and writer.
- **P9 Reporting** — baseline measures.
- **P10 Agent runtime** — platform set-up, case intake agent in shadow, extraction evaluation, deviation screening in shadow, monitoring dashboard.
- Cross-cutting: parameter catalog, multi-product parameters, feature flags, migrations, data dictionary, synthetic and masked data.

**Out of scope for EPIC-001**

- Inbound source loads and tracker inventory. ACE ingests source data (D-RCV-35 U1/U5).
- Case lifecycle execution on Temporal workflows. Temporal is installed and the worker is built in Epic 1; case workflows start in Epic 3 (D-RCV-36 T1).
- Route screens and collections processes owned by other epics.
- `RWB-E1-036` (no story file exists) and the retired stories in `docs/retirements/story-retirement-register.md`.

## Dependencies

| Dependency | Owner | Needed by |
|---|---|---|
| ACE schema `recovery`, role grants and the 21 Tier 1 tables | ACE team | `RWB-E1-069` |
| `RWB-ACE-001` — 14 Tier 2 tables and 12 columns | ACE team | Section B views, `RWB-E1-069` |
| Temporal cluster on ACE AKS | SCB IT / ACE platform | `RWB-E1-070`, `RWB-E1-071` |
| Approved Drools libraries | Recovery tech lead | `RWB-E1-072`, `RWB-E1-073` |
| Entra ID application registration | ACE identity team | `RWB-E1-022` |
| Oracle/ACE test data and synthetic generator | Data team | `RWB-E1-065` |

## Reused approved artefacts

| Artefact | Version |
|---|---|
| Lean BRD Epic 1 | v3 |
| Business Requirements Epic 1 | v4 |
| Business Requirements Program | v4 |
| Module FSDs P1–P10, S1–S9 | v6 (P3 v4) |
| Module TSDs | v5 (P3 v3, P4 v3) |
| Target Architecture | v6 |
| ADRs | ADR-001–012 |
| Logical Data Model and Data Dictionary | v8 |
| Physical Schema | v6 |
| API Specification | v4 |
| Error and Message Standard | v4 |
| Test Strategy, Test Cases, Regression Suite | v3/v7/v6 |
| Engineering Practices | v5 |
| AI Assisted Development Approach | v1 |

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Intake approval | Product Owner | Chitchaya Muanchonchana | Document set v14, 16 Nov 2026 |
| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | `output/CONTEXT-20261116/` |
| Requirements approval | Product Owner, FDA | Chitchaya Muanchonchana, Jesniphat Pukkham | Source BRD/FSD set v14 |
| Design and architecture approval | Forward Deployed Architect | Jesniphat Pukkham | ADR-001–012 |
| Backlog and specification approval | Product Owner | Chitchaya Muanchonchana | Per story |
| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per story |
| Pull request approval | Forward Deployed Engineer | Recovery tech lead | Per MR into `develop-recovery` |
| Release readiness | Forward Deployed Engineer | Jesniphat Pukkham | Before 30 Nov 2026 |

Named approvers for every story gate are recorded per card. `TBC` is not an approval.

## Risk, rollback and stop signals

| Risk | Control |
|---|---|
| ACE Tier 1 tables lag the story baseline | `RWB-E1-069` checks the 21 tables before views compile; Section B stays behind flags. |
| Temporal platform is not ready | `rwb.p3.temporal` off returns the previous path; Epic 1 jobs stay on Quartz and Spring Batch. |
| Drools package has an invalid decision table | Upload compiles and runs scenarios before approval; rollback is one call. |
| A recovery class reads ACE directly | Boundary rule BND-6 fails the build. |
| A schema literal or a non-`V<seq>__<story>_<name>` migration appears | Migration lint fails the build (D-RCV-28). |
| A removed load story is rebuilt | The retirement register and `AGENTS.md` forbid it. |

**Rollback:** feature flag off or redeploy the previous image tag. Migrations are forward-only; a corrective script takes the next sequence and keeps the story key (D-RCV-28).

**Stop signals:** a view cannot compile; a Tier 2 table is missing; a rule package cannot be rolled back; a story needs a source copy; a guardrail in the story file is breached.

## Evidence links

| Evidence | Location |
|---|---|
| Increment index | `docs/increments/INDEX.md` |
| Story manifest | `output/EPIC1-STORY-MANIFEST.json` |
| Context package | `.github/contexts/`, `output/CONTEXT-20261116/` |
| Story cards | `docs/increments/INC-0NN-*.md` |
| Per-story output | `output/INC-0NN-*/` |
| Traceability | `requirement/Traceability_Matrix.md` |

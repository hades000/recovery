# Increment Card — INC-018-epic-1-RWB-TE-004

**RWB-TE-004 — Masked data in SIT and UAT**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-018` |
| Title | Masked data in SIT and UAT |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-TE-004` |
| RUN_ID | `INC-018-epic-1-RWB-TE-004` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | Enabler |
| Priority | Must |
| Window | Window 1 |
| Critical path | No |
| Depends on | RWB-E1-065 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P1 Recovery data engine. **Build group:** P1a.

## Scope

**Story:** As a **Tribe lead and squad member (RW-TRIBE)**, I want **masked copies of recovery data loaded into SIT and UAT from the PII service**, so that **tests run on realistic volumes without exposing customers**.

**Main flow:**
1. PII service: writes the masked extract files and the manifest to the intake container of SIT or UAT.
2. Platform administrator: starts the masked copy load in the pipeline for the target environment.
3. MaskedCopyLoader: refuses to run when the target environment is DEV or PROD.
4. MaskedCopyLoader: checks the manifest: extract ID not loaded before, masking rule version equal to the version in force, schema version equal to the target.
5. MaskedCopyLoader: runs the load checks of CTL-02 on each file: business date, structure, control totals (row count and balance sum), keys.
6. MaskingVerifier: scans every column tagged is_personal for values that look personal: a 13-digit number with a valid Thai national ID check digit, a Thai mobile number or an email address.

**Out of scope:**
- Synthetic data in DEV (RWB-E1-065).
- The masking rule values per field and role (DL26, Compliance) and masking on screens (RWB-E1-037).
- The PII service itself, which the bank runs.
- The masked debt sale data tape (FEAT-DBS-03, Epic 5).

**Business outcome and value hypothesis:** SIT and UAT must show that loads, allocation, reconciliation and reports work at production volume and with production data shapes, which synthetic data does not prove. NFR-045 allows masked copies in user acceptance and forbids production data in development. The bank's PII service produces the masked copy under the Compliance masking rules; this story loads it into SIT and UAT only, refuses any copy that still holds a personal value, and keeps balances, dates and keys unchanged so counts and reconciliations behave as in production. Serves REQ-RDF-010 and REQ-ACA-005; decision DL26 sets the masking rules.

**Constraints and guardrails:**
- No business value in code: the masking rules and their version belong to Compliance; allowed environments are properties.
- No personal data in logs, tests or prompts: the load report holds counts, totals and check names, never a value; test extracts are built from synthetic data.
- No read of another module's tables at runtime: the loader is a tool outside the ACE service and runs only in SIT and UAT.
- No masked copy ever reaches DEV, and no copy is made from SIT or UAT to another environment.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 004 Masked data in SIT and UAT v1.md` |
| Requirement IDs | REQ-RDF-010, REQ-ACA-005 |
| BRD section | Business Requirements Epic 1, section 4 (REQ-RDF-010, REQ-ACA-005); Business Requirements Program, section 6.7 (NFR-045) |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| Logical data model and data dictionary | `requirement/legacy/06-data/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v2.yaml` |
| Business rules and routing logic | `requirement/legacy/02-business-architecture-and-process/` |
| Error and message standard | `requirement/legacy/07-screens-and-experience/` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Role | Rights in this story |
|---|---|
| RW-PLATADM, platform administrator | Starts the load in SIT or UAT; owns the intake containers |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rules and their version (DL26) |
| RW-TRIBE, Tribe lead and squad members | Run tests on the loaded copy with their test users' rights |
| SY-DATALOAD, data load | Identity the loader runs under in SIT and UAT |

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

`TBC` is not an approval (`GAP-006`). The story is in delivery at the specification stage; the human gates remain open until named.

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder | Not used | The context package exists; reuse `.github/contexts/` and `EPIC-001`. |
| Requirements and discovery | BRD Builder | Not used | The BRD is approved; reuse it. |
| Requirements and discovery | PRD Builder | Not used | The FSD/PRD is approved; reuse it. |
| Design, backlog and spec | Jira Backlog Manager | Optional | The local story file is the backlog; Jira import is TBC. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in the ACE repository. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Not used | API is not in scope. |
| Quality and release | Functional Automation Test | Not used | UI is not in scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** `rwb.dataengine.masked-copy`.
- **Critical path:** No; **depends on:** RWB-E1-065.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: the masking rules and their version belong to Compliance; allowed environments are properties.
  - No personal data in logs, tests or prompts: the load report holds counts, totals and check names, never a value; test extracts are built from synthetic data.
  - No read of another module's tables at runtime: the loader is a tool outside the ACE service and runs only in SIT and UAT.
  - No masked copy ever reaches DEV, and no copy is made from SIT or UAT to another environment.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 004 Masked data in SIT and UAT v1.md` |
| Specification | `output/INC-018-epic-1-RWB-TE-004/specify/spec.md` |
| Compliance validation | `output/INC-018-epic-1-RWB-TE-004/specify/compliance-validation.md` |
| Agent run log | `output/INC-018-epic-1-RWB-TE-004/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-018-epic-1-RWB-TE-004/plan/` (TBC) |
| Implementation evidence | `output/INC-018-epic-1-RWB-TE-004/implement/` (TBC) |
| API / functional test reports | `output/INC-018-epic-1-RWB-TE-004/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-018-epic-1-RWB-TE-004/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — cleaned against the current story on 2026-11-05; no removed ACs are mapped |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-018-epic-1-RWB-TE-004/specify/compliance-validation.md`) |
| Acceptance criteria | 0 — engineering enabler; no business ACs (see §7 note) |
| AC numbering | Not applicable — no ACs |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 004 Masked data in SIT and UAT v1.md` |
| Output run | `output/INC-018-epic-1-RWB-TE-004/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |

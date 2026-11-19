# Increment Card — INC-060-epic-1-RWB-E1-015

**RWB-E1-015 — Freshness stamp per data product**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-060` |
| Title | Freshness stamp per data product |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-015` |
| RUN_ID | `INC-060-epic-1-RWB-E1-015` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-003, RWB-E1-001, RWB-E1-064, RWB-E1-006 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine. **Build group:** P1b.

## Scope

**Story:** As a **data steward and data product owner (RW-DATASTEW)**, I want **every data product to carry the source extract time and the load time, exposed to every consumer and shown on the case record view**, so that **every decision input states how old it is and stale facts are visible**.

**Main flow:**
1. Load job (JOB-01 or JOB-09): commits a load for product DP01 and business date D.
2. FreshnessStampService: in the same transaction, writes one data_product_load row with business date D, the source extract time from the COLLINS control record and the load time.
3. JOB-01 freshness step: at each product's expected-by time, checks that a load for the expected business date exists.
4. FreshnessStampService: for a product with no load, sets the latest row to status STALE, writes a data quality exception with check FRESHNESS and sends the operations alert.
5. StaleMarkerListener: on LoadRefused, marks the product STALE at once.
6. Consumer (case record view, P3 or P7): calls FreshnessQuery or GET /data-products/freshness and receives business date, source extract time, load time and status per product.

**Out of scope:**
- The MSG-P7-006 warning on a decision screen when an input is past its age limit (decision screens, Epic 2).
- Same-day data for named triggers (DL06).
- The data quality console SCR-45 (Epic 2) and the reconciliation report (RWB-E1-011).
- Freshness of the stage 2 data products (RWB-E2-010).

**Business outcome and value hypothesis:** Recovery data arrives by end of day batch and weekly or monthly file loads (ADR-005), so a fact on the case can be one day or one week old, and nobody can see which. A stamp per product and load, shown on the case record and copied into each decision's inputs snapshot, makes the age of every input visible to the person deciding and to audit. A product whose load has not arrived by its expected time is flagged stale the same morning. Serves REQ-RDF-009; measure: loads on time and complete on 99 percent of days (FSD P1 A2.14.1).

**Constraints and guardrails:**
- No business value in code: expected-by times, cycles and the alert channel are data rows or properties.
- No personal data in logs, tests or prompts; stamps carry product codes and times only.
- No read of another module's tables: P3 and P7 read stamps only through FreshnessQuery; this story writes no P7 table.
- The stale check never deletes or changes loaded rows; the previous load stays in use.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 015 Freshness stamp per data product v1.md` |
| Requirement IDs | REQ-RDF-009 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-RDF-009) |
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
| SY-DATALOAD, data load | Writes data_product_load rows; marks products stale; writes the FRESHNESS exception |
| SY-DECLOG, decision log writer | Reads stamps through FreshnessQuery for the inputs snapshot |
| RW-DATASTEW, data steward | Reads stamps and stale exceptions (Platform administration R) |
| RW-PLATADM, platform administrator | Reads stamps and stale exceptions; receives the operations alert |
| Case roles with Case record R, for example RW-CASEOWN, RW-TEAMMGR | Read the stamp in the case record data panel |

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
| Quality and release | API Tester | Applicable | Required by the spec's API scope. |
| Quality and release | Functional Automation Test | Applicable | Required by the spec's UI scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** `rwb.dataengine.freshness-stamp`.
- **Critical path:** No; **depends on:** RWB-E1-003, RWB-E1-001, RWB-E1-064, RWB-E1-006.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: expected-by times, cycles and the alert channel are data rows or properties.
  - No personal data in logs, tests or prompts; stamps carry product codes and times only.
  - No read of another module's tables: P3 and P7 read stamps only through FreshnessQuery; this story writes no P7 table.
  - The stale check never deletes or changes loaded rows; the previous load stays in use.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 015 Freshness stamp per data product v1.md` |
| Specification | `output/INC-060-epic-1-RWB-E1-015/specify/spec.md` |
| Compliance validation | `output/INC-060-epic-1-RWB-E1-015/specify/compliance-validation.md` |
| Agent run log | `output/INC-060-epic-1-RWB-E1-015/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-060-epic-1-RWB-E1-015/plan/` (TBC) |
| Implementation evidence | `output/INC-060-epic-1-RWB-E1-015/implement/` (TBC) |
| API / functional test reports | `output/INC-060-epic-1-RWB-E1-015/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-060-epic-1-RWB-E1-015/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-060-epic-1-RWB-E1-015/specify/compliance-validation.md`) |
| Acceptance criteria | 8 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 015 Freshness stamp per data product v1.md` |
| Output run | `output/INC-060-epic-1-RWB-E1-015/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |

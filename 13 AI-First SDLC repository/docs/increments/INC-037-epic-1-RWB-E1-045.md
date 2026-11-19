# Increment Card — INC-037-epic-1-RWB-E1-045

**RWB-E1-045 — Multi-product parameters for Mortgage, HP and SSME**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-037` |
| Title | Multi-product parameters for Mortgage, HP and SSME |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-045` |
| RUN_ID | `INC-037-epic-1-RWB-E1-045` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | Enabler |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-042, RWB-E1-043, RWB-E1-012 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P3 Case and workflow. **Build group:** P3a.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **every product-specific value (entry rule, exclusion list, service levels, notice and cure periods, exposure bands) keyed by product in the reference data**, so that **a new product or a product change needs no code change**.

**Main flow:**
1. Center of excellence analyst: prepares a PRODUCT_PARAMETER load with one row per product group and parameter code, and a SERVICE_LEVEL load with one row per product group and case status.
2. Reference data administrator: loads each file through `POST /admin/reference-loads`.
3. Reference data service: runs the RWB-E1-043 checks, then the product completeness check: every product in the PRODUCT version in force on the valid from date has a row for every catalog parameter with scope PRODUCT and required yes, and a SERVICE_LEVEL row for every status in the parameter `servicelevel.required-statuses`.
4. Reference data service: checks each value against the catalog type and range.
5. Approver: approves the version; it takes effect on its valid from date.
6. Timer engine: when it starts a notice timer for a case, calls `ProductParameterService.get(productGroup, "NOTICE_PERIOD_DAYS", businessDate)` and sets `expires_at` from the value and its unit.

**Out of scope:**
- Letter and notice templates per product (P6, DL28).
- Treatment bands, floors and ranges per product (FEAT-ADM-04, Epic 8).
- Delegation limits per product (RWB-E1-038).
- The timer engine, warnings and escalations themselves (RWB-E1-028).
- Product parameter screens (SCR-39 and SCR-42, Epic 8).

**Business outcome and value hypothesis:** Mortgage, hire purchase and SSME follow different notice periods, service levels and bands, and today each difference is held in a team procedure. If the engines carry these values as constants, every product change waits for a release. This story keys each value by product group in the versioned reference tables of RWB-E1-043 and refuses a load that leaves a product without a required value. It meets REQ-DRI-010 and REQ-CWC-011. The measure is that a product is added or changed by a reference load with no deployment.

**Constraints and guardrails:**
- No business value in code. No product group code, period, threshold or band is written in Java or TypeScript; the generated API types treat product group as a string checked against LOV-PRODUCT, not as a closed enum.
- No personal data in logs, tests or prompts. Test cases use synthetic case numbers and no customer data.
- No read of another module's tables. Reference rows are read through `ReferenceDataService`; LOV-PRODUCT through the P4 published interface.
- A running timer is never recalculated when a parameter changes.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md` |
| Requirement IDs | REQ-DRI-010, REQ-CWC-011 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, sections 5.3 and 5.7 |
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
| RW-COE, center of excellence analyst | Prepares and loads PRODUCT_PARAMETER and SERVICE_LEVEL versions (Reference data C) |
| RW-REFADM, reference data administrator | Loads PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL versions (Reference data C) |
| RW-PRODHEAD, product head | Owns the values for the product (LOV-PRODUCT owner in refdata.txt); reads versions (Reference data R) |
| RW-RISK, risk and model risk officer | Approves a version where a limit or threshold moves (refdata.txt Change process step 4; assumed approve right as in RWB-E1-043) |
| SY-CASEWF, case workflow module | Reads product values and writes timers |
| SY-RULES, rules component | Reads product values for allocation |

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
- **Feature flag:** `rwb.p3.product-parameters`. Off: the engines use the values they read before this story.
- **Critical path:** No; **depends on:** RWB-E1-042, RWB-E1-043, RWB-E1-012.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code. No product group code, period, threshold or band is written in Java or TypeScript; the generated API types treat product group as a string checked against LOV-PRODUCT, not as a closed enum.
  - No personal data in logs, tests or prompts. Test cases use synthetic case numbers and no customer data.
  - No read of another module's tables. Reference rows are read through `ReferenceDataService`; LOV-PRODUCT through the P4 published interface.
  - A running timer is never recalculated when a parameter changes.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md` |
| Specification | `output/INC-037-epic-1-RWB-E1-045/specify/spec.md` |
| Compliance validation | `output/INC-037-epic-1-RWB-E1-045/specify/compliance-validation.md` |
| Agent run log | `output/INC-037-epic-1-RWB-E1-045/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-037-epic-1-RWB-E1-045/plan/` (TBC) |
| Implementation evidence | `output/INC-037-epic-1-RWB-E1-045/implement/` (TBC) |
| API / functional test reports | `output/INC-037-epic-1-RWB-E1-045/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-037-epic-1-RWB-E1-045/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-037-epic-1-RWB-E1-045/specify/compliance-validation.md`) |
| Acceptance criteria | 8 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md` |
| Output run | `output/INC-037-epic-1-RWB-E1-045/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |

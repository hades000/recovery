# Increment Card — INC-031-epic-1-RWB-E1-045

**RWB-E1-045 — Multi-product parameters for Mortgage, HP and SSME**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-031` |
| Title | Multi-product parameters for Mortgage, HP and SSME |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-045` |
| RUN_ID | `INC-031-epic-1-RWB-E1-045` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | Enabler |
| Priority | Must |
| Build order | 31 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-042, RWB-E1-043 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P3 Case and workflow.

## Scope

**Story:** As a **center of excellence analyst (RW-COE)**, I want **every product-specific value (entry rule, exclusion list, service levels, notice and cure periods, exposure bands) keyed by product in the reference data**, so that **a new product or a product change needs no code change**.

**Business outcome:** Mortgage, hire purchase and SSME follow different notice periods, service levels and bands, and today each difference is held in a team procedure. If the engines carry these values as constants, every product change waits for a release. This story keys each value by product group in the versioned reference tables of RWB-E1-043 and refuses a load that leaves a product without a required value. It meets REQ-DRI-010 and REQ-CWC-011. The measure is that a product is added or changed by a reference load with no deployment.

**Main flow:**
1. Center of excellence analyst: prepares a PRODUCT_PARAMETER load with one row per product group and parameter code, and a SERVICE_LEVEL load with one row per product group and case status.
2. Reference data administrator: loads each file through `POST /admin/reference-loads`.
3. Reference data service: runs the RWB-E1-043 checks, then the product completeness check: every product in the PRODUCT version in force on the valid from date has a row for every catalog parameter with scope PRODUCT and required yes, and a SERVICE_LEVEL row for every status in the parameter `servicelevel.required-statuses`.
4. Reference data service: checks each value against the catalog type and range.
5. Approver: approves the version; it takes effect on its valid from date.
6. Timer engine: when it starts a notice timer for a case, calls `ProductParameterService.get(productGroup, "NOTICE_PERIOD_DAYS", businessDate)` and sets `expires_at` from the value and its unit.

**Acceptance criteria:**
- AC1: Product value differs
- AC2: New product added
- AC3: Missing parameter blocked
- AC4: Value outside its range
- AC5: Duplicate product row
- AC6: Product removed while cases are open
- AC7: No parameter in force at run time
- AC8: Value changes while a timer runs

**Out of scope:**
- Letter and notice templates per product (P6, DL28).
- Treatment bands, floors and ranges per product (FEAT-ADM-04, Epic 8).
- Delegation limits per product (RWB-E1-038).
- The timer engine, warnings and escalations themselves (RWB-E1-028).
- Product parameter screens (SCR-39 and SCR-42, Epic 8).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-045-multi-product-parameters-for-mortgage-hp-and-ssme-v1.md` |
| Requirement IDs | REQ-DRI-010, REQ-CWC-011 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, sections 5.3 and 5.7 |
| Decision | D6 entry |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| Physical schema | `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Prepares and loads PRODUCT_PARAMETER and SERVICE_LEVEL versions (Reference data C) |
| RW-REFADM, reference data administrator | Loads PRODUCT, PRODUCT_PARAMETER and SERVICE_LEVEL versions (Reference data C) |
| RW-PRODHEAD, product head | Owns the values for the product (LOV-PRODUCT owner in refdata.txt); reads versions (Reference data R) |
| RW-RISK, risk and model risk officer | Approves a version where a limit or threshold moves (refdata.txt Change process step 4; assumed approve right as in RWB-E1-043) |
| SY-CASEWF, case workflow module | Reads product values and writes timers |
| SY-RULES, Drools evaluator | Reads product values for allocation |

## Contract extract

**POST /api/recovery/v1/admin/reference-loads** (P4 endpoint; the completeness check runs inside the RWB-E1-043 registry) | Item | Value | |---|---| | Request | multipart/form-data: `file`, `table` (PRODUCT, PRODUCT_PARAMETER or SERVICE_LEVEL), `validFrom` | | Response | 201 `ReferenceLoad` (`id`, `table`, `validFrom`, `status`, `rows`) | | Errors | 401 (MSG-P4-001); 403 (MSG-P4-002); 409 open cases on a removed product (MSG-P3-027); 422 missing required row (MSG-P3-034), value out of range (MSG-GEN-002), duplicate key (MSG-P3-027); 503 | | Authorization | Reference data, right C | | Idempotency | As RWB-E1-043: table code, valid from and content hash | **GET /api/recovery/v1/cases/{caseId}/timers** (P3) returns `Timer[]` (`timerType`, `startedAt`, `expiresAt`, `warnAt`, `status`). Case record R. Errors 401, 403, 404 (MSG-P4-003), 503. Used to check AC1, AC2 and AC8. **Published interfa…

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Requirements approval | Product Owner | Chitchaya Muanchonchana | Source story set v7/v6, 16 Nov 2026 |
| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | CONTEXT-20261116 |
| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per-story plan gate |
| Pull request approval | Forward Deployed Engineer | Recovery tech lead | Per MR |

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder / Updater | Applicable | Context package CONTEXT-20261116. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in ACE. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Per API scope | Driven by the spec. |
| Quality and release | Functional Automation Test | Per UI scope | Driven by the spec. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Stop signals:** any guardrail in story §17; a migration that is not `V<seq>__<story>_<name>.sql`; a direct read of an ACE table outside `recovery.v_ace_*`.

**Guardrails:**

- No business value in code. No product group code, period, threshold or band is written in Java or TypeScript; the generated API types treat product group as a string checked against LOV-PRODUCT, not as a closed enum. - No personal data in logs, tests or prompts. Test cases use synthetic case numbers and no customer data. - No read of another module's tables. Reference rows are read through `ReferenceDataService`; LOV-PRODUCT through the P4 published interface. - A running timer is never recalculated when a parameter changes.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-045-multi-product-parameters-for-mortgage-hp-and-ssme-v1.md` |
| Specification | `output/INC-031-epic-1-RWB-E1-045/specify/spec.md` |
| Compliance validation | `output/INC-031-epic-1-RWB-E1-045/specify/compliance-validation.md` |
| Agent run log | `output/INC-031-epic-1-RWB-E1-045/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-031-epic-1-RWB-E1-045/plan/` |
| Implementation evidence | `output/INC-031-epic-1-RWB-E1-045/implement/` |
| API / functional test reports | `output/INC-031-epic-1-RWB-E1-045/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-031-epic-1-RWB-E1-045/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 8 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-045-multi-product-parameters-for-mortgage-hp-and-ssme-v1.md` |
| Output run | `output/INC-031-epic-1-RWB-E1-045/` |


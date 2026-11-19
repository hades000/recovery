# Increment Card — INC-015-epic-1-RWB-TE-004

**RWB-TE-004 — Masked data in SIT and UAT**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-015` |
| Title | Masked data in SIT and UAT |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-TE-004` |
| RUN_ID | `INC-015-epic-1-RWB-TE-004` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | Enabler |
| Priority | Must |
| Build order | 15 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-065 |
| Blocks | See the build sequence |
| Status | Ready for specify |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P1 Recovery data engine.

## Scope

**Story:** As a **Tribe lead and squad member (RW-TRIBE)**, I want **masked copies of recovery data loaded into SIT and UAT from the PII service**, so that **tests run on realistic volumes without exposing customers**.

**Business outcome:** SIT and UAT must show that loads, allocation, reconciliation and reports work at production volume and with production data shapes, which synthetic data does not prove. NFR-045 allows masked copies in user acceptance and forbids production data in development. The bank's PII service produces the masked copy under the Compliance masking rules; this story loads it into SIT and UAT only, refuses any copy that still holds a personal value, and keeps dates, keys and row counts unchanged so counts and reconciliations behave as in production. Serves REQ-RDF-010 and REQ-ACA-005; decision DL26 sets the masking rules.

**Main flow:**
1. PII service: writes the masked extract files and the manifest to the intake container of SIT or UAT.
2. Platform administrator: starts the masked copy load in the pipeline for the target environment.
3. MaskedCopyLoader: refuses to run when the target environment is DEV or PROD.
4. MaskedCopyLoader: checks the manifest: extract ID not loaded before, masking rule version equal to the version in force, schema version equal to the target.
5. MaskedCopyLoader: runs the load checks of CTL-02 on each file: business date, structure, control totals (row count per table), keys.
6. MaskingVerifier: scans every column tagged is_personal for values that look personal: a 13-digit number with a valid Thai national ID check digit, a Thai mobile number or an email address.

**Acceptance criteria:**
- AC1: Masked copy
- AC2: A personal value left in the copy
- AC3: Totals that do not match the manifest
- AC4: A copy aimed at DEV
- AC5: The same extract twice
- AC6: A masking rule version that is not in force
- AC7: A second load while one runs

**Out of scope:**
- Synthetic data in DEV (RWB-E1-065).
- The masking rule values per field and role (DL26, Compliance) and masking on screens (RWB-E1-037).
- The PII service itself, which the bank runs.
- The masked debt sale data tape (FEAT-DBS-03, Epic 5).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-004-masked-data-in-sit-and-uat-v1.md` |
| Requirement IDs | REQ-RDF-010, REQ-ACA-005 |
| BRD section | Business Requirements Epic 1, section 4 (REQ-RDF-010, REQ-ACA-005); Business Requirements Program, section 6.7 (NFR-045) |
| Decision | DL26 |
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
| RW-PLATADM, platform administrator | Starts the load in SIT or UAT; owns the intake containers |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rules and their version (DL26) |
| RW-TRIBE, Tribe lead and squad members | Run tests on the loaded copy with their test users' rights |
| SY-DATALOAD, data load | Identity the loader runs under in SIT and UAT |

## Contract extract

**Pipeline stage** | Item | Value | |---|---| | Trigger | Manual start by the platform administrator for SIT or UAT after the PII service delivers an extract | | Job name | Masked copy load, a SIT and UAT pipeline stage; not a scheduled job and not in the production job list (batch.txt) | | Schedule | On request | | Input | Masked extract files and manifest from the PII service in the environment's intake container | | Output | Recovery schema in SIT or UAT replaced by the masked copy; load report with extract ID, business date, masking rule version, rows and totals per table and the check results | | Events published | None | | Idempotency key | Extract ID; a repeat is skipped | | Restart behavior | Files load into staging schema `recovery_next`; the swap happens only after every check passes, so a failure leaves the previous copy | **Endpoint used in SIT on the loaded copy** | Method…

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

- No business value in code: the masking rules and their version belong to Compliance; allowed environments are properties. - No personal data in logs, tests or prompts: the load report holds counts, totals and check names, never a value; test extracts are built from synthetic data. - No read of another module's tables at runtime: the loader is a tool outside the ACE service and runs only in SIT and UAT. - No masked copy ever reaches DEV, and no copy is made from SIT or UAT to another environment.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-004-masked-data-in-sit-and-uat-v1.md` |
| Specification | `output/INC-015-epic-1-RWB-TE-004/specify/spec.md` |
| Compliance validation | `output/INC-015-epic-1-RWB-TE-004/specify/compliance-validation.md` |
| Agent run log | `output/INC-015-epic-1-RWB-TE-004/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-015-epic-1-RWB-TE-004/plan/` |
| Implementation evidence | `output/INC-015-epic-1-RWB-TE-004/implement/` |
| API / functional test reports | `output/INC-015-epic-1-RWB-TE-004/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-015-epic-1-RWB-TE-004/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Ready for specify |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 7 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-004-masked-data-in-sit-and-uat-v1.md` |
| Output run | `output/INC-015-epic-1-RWB-TE-004/` |


# Increment Card — INC-010-epic-1-RWB-E1-069

**RWB-E1-069 — Read-only ACE source views, grants and boundary rule**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-010` |
| Title | Read-only ACE source views, grants and boundary rule |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-069` |
| RUN_ID | `INC-010-epic-1-RWB-E1-069` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Build order | 10 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-001 (V0001); RWB-ACE-001 for the 14 Section B views (DL43) |
| Blocks | RWB-E1-002, RWB-E1-016, RWB-E1-018 |
| Status | Ready for specify |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine.

## Scope

**Story:** As a **recovery developer (RW-TRIBE)**, I want **the recovery module to read ACE source data only through SELECT-only recovery.v_ace_* views, with the database grants and the build-time rule that enforce the boundary**, so that **there is one copy of source data, the Workbench cannot alter or copy it, and a direct read of an ACE table fails in the database and in the build**.

**Business outcome:** The Workbench takes no inbound source data. ACE ingests every source, and the recovery module reads it through 30 SELECT-only views: 16 over the ACE tables that exist today, 177 fields, and 14 over the tables RWB-ACE-001 adds, 127 fields. The views are owned by a dedicated role that holds SELECT on the ACE tables; the recovery service role holds SELECT on the views and no privilege on anything in `public`. PUBLIC holds no privilege, and no write is granted on a view. The Workbench keeps its own decisions about an ACE record in four extension tables keyed by the ACE business key, never in a copy of an ACE column.

**Main flow:**
1. Recovery developer: takes Section A of `15 ACE DB Alignment/Recovery Workbench ACE Source Views v1.sql` into `V0002__rwb_e1_069_ace_source_views.sql`: the 16 views, the three helper functions and the grant block. The four extension tables ship in V0001 with RWB-E1-001, which runs first; this story verifies them rather than creating them.
2. Recovery developer: writes no environment name in the file. The schema is `${recoverySchema}` and the two role names come from the Environment and Deployment Design (D-RCV-28; RWB-E1-044).
3. Pipeline: applies V0001 then V0002 in DEV, then in SIT.
4. Pipeline: runs the conformance test: 16 of 16 views compile, no constraint in `recovery` references `public`, every view has dictionary rows, and `recovery_svc` has no privilege in `public` and no write on a view.
5. Recovery developer: adds boundary rule BND-6 to `RecoveryBoundaryTest` in RWB-TE-001 and the 30 view names to `recovery-modules.yaml` as the only allowed source objects.
6. ACE team: applies RWB-ACE-001 with the 14 Tier 2 tables, and its migration grants SELECT on those tables to `ace_view_owner` (DL43).

**Acceptance criteria:**
- AC1: The 16 Section A views compile
- AC2: The recovery role reads only through the views
- AC3: The 14 Section B views compile after RWB-ACE-001
- AC4: No recovery constraint references public
- AC5: Every view has dictionary rows
- AC6: The dictionary returns days_past_due from the ACE delay days
- AC7: The four extension tables are 1:1 on the ACE key
- AC8: The boundary test allows only recovery.v_ace_*

**Out of scope:**
- The 14 Tier 2 tables and the 12 columns that RWB-ACE-001 adds to `account`, `customer` and `efs_action`: the ACE team owns them, and this story neither creates nor alters them.
- The features that read a Section B view: their own stories, behind their flags until V0003 is applied.
- Masking at the API and the PII access log: RWB-E1-037 and RWB-E1-016.
- The data dictionary content and its maintenance: RWB-E1-001 for the metadata rows and RWB-E1-064 for the dictionary of the 14 data products.
- The rest of RWB-TE-001: this story adds boundary rule BND-6 and the `sourceViews` list only.
- Any change to the 30-view list: the data architect and the recovery tech lead, with a new version of the ACE Data Tier Map v1.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-069-read-only-ace-source-views-grants-and-boundary-rule-v1.md` |
| Requirement IDs | REQ-RDF-002, REQ-DRI-006 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-RDF-002); Business Requirements Program, sections 5.2 and 7 (REQ-DRI-006) |
| Decision | D-RCV-35 (U1, U4); ADR-010; DL43 |
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
| Recovery squad (RW-TRIBE) | Writes V0002, V0003 and boundary rule BND-6 |
| ACE team lead and ACE DBA | Own schema `public`; approve the 21 Tier 1 table list and grant SELECT to `ace_view_owner` (RWB-ACE-001) |
| Recovery tech lead and data architect | Approve a change to the 30-view list, which is frozen in the ACE Data Tier Map v1 |
| Recovery migration account | Applies V0002 and V0003 and runs the conformance test in DEV and SIT |
| RW-PLATADM, platform administrator | Reads the deployment result on SCR-44 Migration runs (Platform administration R); may not change a grant |
| RW-AUDIT, internal audit | Reads the view list and the grants (Platform administration R) |
| RW-DATASTEW, data steward | Reads the dictionary rows for the views (Data product catalog R) |
| No approval level from the delegation of authority applies | The story takes no business decision |

## Contract extract

No endpoint and no event. The contract is the migration set and the grant. | Item | Value | |---|---| | Migration V0002 | `V0002__rwb_e1_069_ace_source_views.sql`: the four extension tables, the 16 Section A views, the Section A grant | | Migration V0003 | `V0003__rwb_e1_069_ace_tier2_views.sql`: the 14 Section B views, the Section B grant | | Published interface | The 30 `recovery.v_ace_*` views: one row per ACE object, no primary key, no foreign key. Every module reads source data here and nowhere else | | Grantees | `ace_view_owner` owns the views and holds SELECT on the ACE tables; `recovery_svc` holds SELECT on the views only; PUBLIC holds nothing | | Trigger | The pipeline step `migrate` at deployment (RWB-E1-044) | | Idempotency | The Flyway version. An applied version is never applied again; a repeated GRANT changes nothing | | Restart | A failed migration rolls back. A fix is m…

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

- No business value in code: the view list and the role names are configuration and data, not constants in a service. - No personal data in logs, tests or prompts: test rows are synthetic; the customer view returns `id_no_masked` and `id_no_last4` only and never the clear identity number. - No read of a `public` table and no write to an ACE table: the database grants and boundary rule BND-6 enforce it, and a breach is a defect. - The views are forward only in PROD; a wrong view is corrected by a new migration, never by editing an applied one.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-069-read-only-ace-source-views-grants-and-boundary-rule-v1.md` |
| Specification | `output/INC-010-epic-1-RWB-E1-069/specify/spec.md` |
| Compliance validation | `output/INC-010-epic-1-RWB-E1-069/specify/compliance-validation.md` |
| Agent run log | `output/INC-010-epic-1-RWB-E1-069/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-010-epic-1-RWB-E1-069/plan/` |
| Implementation evidence | `output/INC-010-epic-1-RWB-E1-069/implement/` |
| API / functional test reports | `output/INC-010-epic-1-RWB-E1-069/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-010-epic-1-RWB-E1-069/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Ready for specify |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 8 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-069-read-only-ace-source-views-grants-and-boundary-rule-v1.md` |
| Output run | `output/INC-010-epic-1-RWB-E1-069/` |


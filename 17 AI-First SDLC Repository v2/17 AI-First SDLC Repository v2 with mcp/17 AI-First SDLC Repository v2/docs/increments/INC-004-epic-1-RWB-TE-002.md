# Increment Card — INC-004-epic-1-RWB-TE-002

**RWB-TE-002 — Code owners for the recovery module**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-004` |
| Title | Code owners for the recovery module |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-TE-002` |
| RUN_ID | `INC-004-epic-1-RWB-TE-002` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P2 Integration |
| Story type | Enabler |
| Priority | Must |
| Build order | 4 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-TE-001 |
| Blocks | See the build sequence |
| Status | Ready for specify |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P2 Integration.

## Scope

**Story:** As a **squad member (RW-TRIBE)**, I want **a code owners entry that maps every recovery folder to the TechX tech leads and the common module to the ACE team, with review by a code owner required before merge**, so that **every change in the recovery module is reviewed by its owners**.

**Business outcome:** The recovery and collection squads and the ACE team merge into one repository and one monthly release. Without named owners per folder, a change to the recovery module or to the common module can merge without the team that answers for it. The code owners file names the reviewing team per folder and the branch rule on main blocks a merge until that team approves. It supports REQ-DRI-006, because the integration adapter folder, the only place allowed to reach other systems, cannot change without a TechX tech lead, and it applies DL04 option A and DL37. The measure is the share of merged pull requests on recovery folders approved by a code owner, which must be 100 percent.

**Main flow:**
1. Squad member: writes `.github/CODEOWNERS` with the entries in BR1 to BR5, ordered so that the most specific path is last.
2. Squad member: adds the code owners validation step to the pull request pipeline.
3. ACE team repository administrator: sets the branch rule on main: one approval from a code owner required, stale approvals dismissed on a new commit.
4. Developer: opens a pull request that changes a recovery folder.
5. Repository host: requests review from the owning team named for each changed path.
6. Pipeline: runs the validation step; an owner that does not exist or a path that matches no file fails the check.

**Acceptance criteria:**
- AC1: Review required
- AC2: A common module change needs the ACE team
- AC3: A change across both modules needs both teams
- AC4: Front end, migrations and the module map are covered
- AC5: An author cannot approve their own change
- AC6: A new commit needs a new approval
- AC7: An owner that does not exist fails the check

**Out of scope:**
- The boundary test that checks the code: RWB-TE-001.
- Code owners inside the collection module: the ACE team under DL04.
- The browser test runner in the pipeline: RWB-TE-010 (DL37).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-002-code-owners-for-the-recovery-module-v1.md` |
| Requirement IDs | REQ-DRI-006 |
| BRD section | Business Requirements Program, section 7 (constraints Built on ACE and Modular monolith) |
| Decision | DL37 |
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
| TechX recovery tech leads | Approve changes to recovery folders and the module map |
| ACE team | Approves changes to the common module and the code owners file; sets the branch rule on main |
| RW-TRIBE, tribe lead and squad members | Open pull requests; cannot satisfy a code owner review unless in the owning team |
| No Workbench capability area applies | Access is a repository right, not a Workbench role right |

## Contract extract

| Item | Value | |---|---| | File | `.github/CODEOWNERS` at the repository root | | Entries | `/ace-service/src/main/java/**/common/ @scb-ace/ace-team`; `/ace-service/src/main/java/**/recovery/ @scb-ace/techx-recovery-tech-leads`; `/ace-service/src/test/java/**/recovery/ @scb-ace/techx-recovery-tech-leads`; `/ace-service/src/main/resources/db/migration/recovery/ @scb-ace/techx-recovery-tech-leads`; `/ace-web/src/modules/recovery/ @scb-ace/techx-recovery-tech-leads`; `/architecture/recovery-modules.yaml @scb-ace/techx-recovery-tech-leads`; `/.github/CODEOWNERS @scb-ace/ace-team @scb-ace/techx-recovery-tech-leads` | | Branch rule on main | Require a pull request; require review from code owners; 1 approval; dismiss stale approvals; the author's approval does not count | | Pipeline step | Code owners validation: syntax, every owner exists and has write access, every pattern matches at leas…

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

- No business value in code; the file holds paths and team names only. - No personal data in logs, tests or prompts; test pull requests change fixture files only. - No read of another module's tables; the file is the review control for the boundary of RWB-TE-001. - Team handles are teams, never single people, so absence of one person does not block a merge.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-002-code-owners-for-the-recovery-module-v1.md` |
| Specification | `output/INC-004-epic-1-RWB-TE-002/specify/spec.md` |
| Compliance validation | `output/INC-004-epic-1-RWB-TE-002/specify/compliance-validation.md` |
| Agent run log | `output/INC-004-epic-1-RWB-TE-002/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-004-epic-1-RWB-TE-002/plan/` |
| Implementation evidence | `output/INC-004-epic-1-RWB-TE-002/implement/` |
| API / functional test reports | `output/INC-004-epic-1-RWB-TE-002/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-004-epic-1-RWB-TE-002/review/` |
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
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-002-code-owners-for-the-recovery-module-v1.md` |
| Output run | `output/INC-004-epic-1-RWB-TE-002/` |


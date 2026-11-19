# Increment Card — INC-002-epic-1-RWB-TE-001

**RWB-TE-001 — Recovery module folder and boundary test**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-002` |
| Title | Recovery module folder and boundary test |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-TE-001` |
| RUN_ID | `INC-002-epic-1-RWB-TE-001` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P2 Integration |
| Story type | Enabler |
| Priority | Must |
| Build order | 2 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | None |
| Blocks | See the build sequence |
| Status | Implemented — module boundary built; spec and plan rebaselined 16 Nov 2026 |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P2 Integration.

## Scope

**Story:** As a **squad member (RW-TRIBE)**, I want **the recovery module folder and packages in the ACE repository with a build-time boundary test**, so that **no module calls the inside of another module and no recovery code calls a system of record directly**.

**Business outcome:** Three teams build in one ACE service. Without a checked boundary, a change in one team's code breaks another's, and a direct call to a core system could bypass the COLLINS and file load path. The skeleton gives each Workbench module one package with a published part and an internal part, and a test in every build refuses a call into another module's internal part, a cross-module table read and a direct system call outside the integration adapters. It meets REQ-DRI-006 and applies DT08, ADR-002 and DL05 (option B from 2 November: TechX creates the recovery module in its own package). The measure is the count of boundary violations merged to main, which must stay at zero.

**Main flow:**
1. Squad member: creates the recovery folders and packages for the 19 Workbench modules, each with an `api` package and an `internal` package.
2. Squad member: writes the module map `architecture/recovery-modules.yaml` with each module code, its package and its published packages.
3. Squad member: writes RecoveryBoundaryTest with the rules BR1 to BR5, reading the module map.
4. Squad member: writes the front end boundary rules for `src/modules/recovery`.
5. Squad member: wires the common module access check for `/api/recovery/v1/**` through RecoveryAccessGuard.
6. Pipeline: on each pull request runs the back end tests, including RecoveryBoundaryTest, and the front end dependency check.

**Acceptance criteria:**
- AC1: Boundary enforced
- AC2: Published interface allowed
- AC3: Recovery modules meet only through their api package
- AC4: A module uses only its own tables
- AC5: No direct call to a system of record
- AC6: Front end boundary
- AC7: A package missing from the module map

**Out of scope:**
- Code owners for the recovery folders: RWB-TE-002.
- Types and contract tests from the API specification: RWB-TE-003.
- Boundaries inside the common and collection modules: the ACE team under DL05 option A.
- The integration adapter pattern itself: RWB-E1-007.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-001-recovery-module-folder-and-boundary-test-v1.md` |
| Requirement IDs | REQ-DRI-006 |
| BRD section | Business Requirements Program, section 7 (constraint Modular monolith) and section 5.2 |
| Decision | DL05 |
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
| RW-TRIBE, tribe lead and squad members | Create the folders, the module map and the boundary test |
| TechX tech leads (code owners, RWB-TE-002) | Approve a change to the module map or to the boundary rules |
| ACE team | Names the common and collection published packages (DL05) |
| RW-PLATADM, platform administrator | Runs the pipeline |
| No approval level from the delegation of authority applies | The story takes no business decision |

## Contract extract

| Item | Value | |---|---| | Trigger | Every pull request build and every build of main | | Back end check | RecoveryBoundaryTest, run in the unit test phase | | Front end check | The dependency rules for `src/modules/recovery`, run in the front end lint step | | Output | Pass, or fail with the rule code, the class or file and the dependency that broke it | | Idempotency | The same commit always gives the same result | | Restart | Rerun the pipeline; the check holds no state | **Recovery side of the published access check** ```java // Wired for /api/recovery/v1/**; calls the common module access check (published interface, INT-34) void RecoveryAccessGuard.require(String capabilityArea, Right right, ScopeTarget target); // throws AccessDeniedException mapped to 403 Problem with messageCode MSG-P4-002 ```

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

- No business value in code; module names and packages are in the module map. - No personal data in logs, tests or prompts; fixtures hold class names only. - No read of another module's tables; this story builds the check that enforces it. - The breaking fixtures stay in `src/test` and never ship.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-001-recovery-module-folder-and-boundary-test-v1.md` |
| Specification | `output/INC-002-epic-1-RWB-TE-001/specify/spec.md` |
| Compliance validation | `output/INC-002-epic-1-RWB-TE-001/specify/compliance-validation.md` |
| Agent run log | `output/INC-002-epic-1-RWB-TE-001/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-002-epic-1-RWB-TE-001/plan/` |
| Implementation evidence | `output/INC-002-epic-1-RWB-TE-001/implement/` |
| API / functional test reports | `output/INC-002-epic-1-RWB-TE-001/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-002-epic-1-RWB-TE-001/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Implemented — module boundary built; spec and plan rebaselined 16 Nov 2026 |
| Specification | SUCCESS — new v2 spec 16 Nov 2026 |
| Compliance review | PASS |
| Acceptance criteria | 7 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation | IMPLEMENTED. Module boundary and BND-1..BND-5 built and merged (ACE MR !285); evidence `output/INC-002-epic-1-RWB-TE-001/implement/`. |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-001-recovery-module-folder-and-boundary-test-v1.md` |
| Output run | `output/INC-002-epic-1-RWB-TE-001/` |


# Increment Card — INC-005-epic-1-RWB-TE-003

**RWB-TE-003 — Types and contract tests from the API specification**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-005` |
| Title | Types and contract tests from the API specification |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-TE-003` |
| RUN_ID | `INC-005-epic-1-RWB-TE-003` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P2 Integration |
| Story type | Enabler |
| Priority | Must |
| Build order | 5 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-TE-001 |
| Blocks | See the build sequence |
| Status | Ready for specify |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P2 Integration.

## Scope

**Story:** As a **squad member (RW-TRIBE)**, I want **server interfaces and front end types generated from the OpenAPI file, with a contract test and an access test per endpoint**, so that **the front end and the service never drift from the specification and no endpoint skips its access check**.

**Business outcome:** The recovery API has 79 operations specified in one OpenAPI 3.1 file. When server code, front end code and the file are kept by hand, a field renamed on one side breaks a screen in SIT, and an endpoint can ship without the capability check its specification states. Generating both sides from the file and testing every implemented operation against it in each build stops both faults before merge. It meets REQ-DRI-007, where the FSD requires every interface to have a contract test (AC-P2-001-01), and REQ-ACA-003, because each endpoint is tested against the right its specification declares from the permission matrix. The measure is the count of contract defects found in SIT, with a target of zero.

**Main flow:**
1. Build: lints the specification with the recovery rule set; a missing operationId, x-capability or error response fails the build.
2. Build: generates the Spring server interfaces and models from the specification.
3. Build: generates the TypeScript types and the typed client for the front end.
4. Build: compiles the service against the generated interfaces and the front end against the generated types.
5. Contract test: lists every operation with x-first-release at or before `rwb.release` and finds its implementing controller method.
6. Contract test: calls each implemented operation with its fixture and validates the request and the response against the specification.

**Acceptance criteria:**
- AC1: Types generated
- AC2: Contract broken
- AC3: The specification is checked before generation
- AC4: An undocumented status fails
- AC5: A current operation with no implementation fails
- AC6: A later operation is pending
- AC7: The front end cannot use a removed field
- AC8: An endpoint that skips its access check fails the build

**Out of scope:**
- Contract tests for file interfaces: RWB-E1-007.
- Browser tests on the screens that use the generated client: RWB-TE-010.
- The permission matrix content: RWB-E1-037.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-003-types-and-contract-tests-from-the-api-specification-v1.md` |
| Requirement IDs | REQ-DRI-007, REQ-ACA-003 |
| BRD section | Business Requirements Program, section 5.2 and section 5.4 |
| Decision | None |
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
| RW-TRIBE, tribe lead and squad members | Change the specification and the implementations; run the build |
| TechX tech leads (code owners, RWB-TE-002) | Approve a change to the specification file |
| RW-SECADM, security administrator | Owns the permission matrix that the access tests read |
| No approval level from the delegation of authority applies | The story takes no business decision |

## Contract extract

| Item | Value | |---|---| | Input | `api/recovery-api.yaml` (OpenAPI 3.1, base path /api/recovery/v1) | | Lint | Recovery rule set for BR2, run first | | Server generation | Spring interfaces and models, interface only, Spring Boot 3, one interface per tag, into the shared generated package listed in the module map | | Front end generation | TypeScript types and a typed fetch client into `src/modules/recovery/api/generated` | | Contract test | One success test per implemented operation: request and response validated against the specification, including status, content type and schema | | Access test | One test per implemented operation: a role whose letters in the declared capability area lack the right, taken from the permission matrix seed, expects 403, `application/problem+json` and messageCode MSG-P4-002 | | Output | A report of passed, failed and pending operations in the build a…

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

- No business value in code: capability areas and rights come from the specification and the permission matrix. - No personal data in logs, tests or prompts; fixtures are synthetic and the test report holds operation names only. - No read of another module's tables; each module's controller implements its own generated interface. - Generated code is never edited; a change goes into the specification.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-003-types-and-contract-tests-from-the-api-specification-v1.md` |
| Specification | `output/INC-005-epic-1-RWB-TE-003/specify/spec.md` |
| Compliance validation | `output/INC-005-epic-1-RWB-TE-003/specify/compliance-validation.md` |
| Agent run log | `output/INC-005-epic-1-RWB-TE-003/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-005-epic-1-RWB-TE-003/plan/` |
| Implementation evidence | `output/INC-005-epic-1-RWB-TE-003/implement/` |
| API / functional test reports | `output/INC-005-epic-1-RWB-TE-003/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-005-epic-1-RWB-TE-003/review/` |
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
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-003-types-and-contract-tests-from-the-api-specification-v1.md` |
| Output run | `output/INC-005-epic-1-RWB-TE-003/` |


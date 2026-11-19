# Increment Card — INC-005-epic-1-RWB-TE-003

**RWB-TE-003 — Types and contract tests from the API specification**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-005` |
| Title | Types and contract tests from the API specification |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-TE-003` |
| RUN_ID | `INC-005-epic-1-RWB-TE-003` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P2 Integration |
| Story type | Enabler |
| Priority | Must |
| Window | Window 1 |
| Critical path | No |
| Depends on | RWB-TE-001 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P2 Integration. **Build group:** P2.

## Scope

**Story:** As a **squad member (RW-TRIBE)**, I want **server interfaces and front end types generated from the OpenAPI file, with a contract test and an access test per endpoint**, so that **the front end and the service never drift from the specification and no endpoint skips its access check**.

**Main flow:**
1. Build: lints the specification with the recovery rule set; a missing operationId, x-capability or error response fails the build.
2. Build: generates the Spring server interfaces and models from the specification.
3. Build: generates the TypeScript types and the typed client for the front end.
4. Build: compiles the service against the generated interfaces and the front end against the generated types.
5. Contract test: lists every operation with x-first-release at or before `rwb.release` and finds its implementing controller method.
6. Contract test: calls each implemented operation with its fixture and validates the request and the response against the specification.

**Out of scope:**
- Contract tests for file interfaces: RWB-E1-007.
- Browser tests on the screens that use the generated client: RWB-TE-010.
- The permission matrix content: RWB-E1-037.

**Business outcome and value hypothesis:** The recovery API has 79 operations specified in one OpenAPI 3.1 file. When server code, front end code and the file are kept by hand, a field renamed on one side breaks a screen in SIT, and an endpoint can ship without the capability check its specification states. Generating both sides from the file and testing every implemented operation against it in each build stops both faults before merge. It meets REQ-DRI-007, where the FSD requires every interface to have a contract test (AC-P2-001-01), and REQ-ACA-003, because each endpoint is tested against the right its specification declares from the permission matrix. The measure is the count of contract defects found in SIT, with a target of zero.

**Constraints and guardrails:**
- No business value in code: capability areas and rights come from the specification and the permission matrix.
- No personal data in logs, tests or prompts; fixtures are synthetic and the test report holds operation names only.
- No read of another module's tables; each module's controller implements its own generated interface.
- Generated code is never edited; a change goes into the specification.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 003 Types and contract tests from the API specification v1.md` |
| Requirement IDs | REQ-DRI-007, REQ-ACA-003 |
| BRD section | Business Requirements Program, section 5.2 and section 5.4 |
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
| RW-TRIBE, tribe lead and squad members | Change the specification and the implementations; run the build |
| TechX tech leads (code owners, RWB-TE-002) | Approve a change to the specification file |
| RW-SECADM, security administrator | Owns the permission matrix that the access tests read |
| No approval level from the delegation of authority applies | The story takes no business decision |

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
- **Feature flag:** None. A build check has no runtime path to switch off.
- **Critical path:** No; **depends on:** RWB-TE-001.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: capability areas and rights come from the specification and the permission matrix.
  - No personal data in logs, tests or prompts; fixtures are synthetic and the test report holds operation names only.
  - No read of another module's tables; each module's controller implements its own generated interface.
  - Generated code is never edited; a change goes into the specification.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 003 Types and contract tests from the API specification v1.md` |
| Specification | `output/INC-005-epic-1-RWB-TE-003/specify/spec.md` |
| Compliance validation | `output/INC-005-epic-1-RWB-TE-003/specify/compliance-validation.md` |
| Agent run log | `output/INC-005-epic-1-RWB-TE-003/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-005-epic-1-RWB-TE-003/plan/` (TBC) |
| Implementation evidence | `output/INC-005-epic-1-RWB-TE-003/implement/` (TBC) |
| API / functional test reports | `output/INC-005-epic-1-RWB-TE-003/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-005-epic-1-RWB-TE-003/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — cleaned against the current story on 2026-11-05; no removed ACs are mapped |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-005-epic-1-RWB-TE-003/specify/compliance-validation.md`) |
| Acceptance criteria | 0 — engineering enabler; no business ACs (see §7 note) |
| AC numbering | Not applicable — no ACs |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 003 Types and contract tests from the API specification v1.md` |
| Output run | `output/INC-005-epic-1-RWB-TE-003/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |

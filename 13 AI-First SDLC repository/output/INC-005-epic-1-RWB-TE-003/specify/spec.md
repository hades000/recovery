# Technical Specification — RWB-TE-003 Types and contract tests from the API specification

| Field | Value |
|---|---|
| Story | RWB-TE-003 — Types and contract tests from the API specification |
| Epic / module | E1 / P2 Integration (technical enabler) |
| RUN_ID | `INC-005-epic-1-RWB-TE-003` |
| Source requirement | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 003 Types and contract tests from the API specification v1.md`; REQ-DRI-007; REQ-ACA-003; BRD Program §5.2, §5.4 |
| Upstream IDs | REQ-DRI-007; REQ-ACA-003; CTL-09; ADR-006; API Specification v2; TSD P2 appendix T-A; RWB-E1-037 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | TechX tech leads (code owners); RW-SECADM for the permission matrix; see `compliance-validation.md` |
## Change Scope Declaration
| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen, component, route, label, state or validation presentation changes. Generated front-end types and the typed client are build artefacts consumed by existing screens; the type check is the verification. |
| Logic In Scope | `YES` — specification lint, operation catalog, release gating, contract validation and the per-operation access test. |
| API In Scope | `NO` — no endpoint or schema change. The story makes the existing OpenAPI contract executable and enforced. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `api/recovery-api.yaml` (OpenAPI 3.1, base `/api/recovery/v1`); every implemented controller; front-end API layer; ACE pull request pipeline; permission matrix seed (RWB-E1-037). |
| New Nodes Required | `YES` — `recovery-api` lint rule set; server and front-end generators; `OperationCatalog`; `RecoveryContractTest`; `RecoveryAccessContractTest`; `ContractFixtures`; build report. |
| Inherited Existing Behavior | Recovery folders and module map (RWB-TE-001); permission matrix and roles (RWB-E1-037); generated type policy (ADR-006); existing controllers and fixtures. |
| Frontend Changes Required | `NO` — no hand-written front-end change; generated types and client are produced at build time. |
| Backend Changes Required | `YES` |
## Requirement-to-SPEC Logic Coverage
| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | The OpenAPI file is the only source of endpoints, request and response schemas. | SPEC-RWB-TE-003-001 | DIRECT | No hand-written server model or front-end type for an operation in the file. | COVERED |
| BR2 | Every operation carries `operationId`, `x-module`, `x-capability` (area and right) and `x-first-release`; every error response uses the Problem schema. | SPEC-RWB-TE-003-002 | DIRECT | Lint runs before generation; a missing field fails the build. | COVERED |
| BR3 | Every operation first in the current release or earlier has an implementation and a passing contract test. | SPEC-RWB-TE-003-005, SPEC-RWB-TE-003-006, SPEC-RWB-TE-003-008 | DIRECT | `rwb.release` filters the catalog; current operations are mandatory. | COVERED |
| BR4 | Every operation refuses a role whose permission lacks the declared right with 403 and `messageCode` MSG-P4-002. | SPEC-RWB-TE-003-012, SPEC-RWB-TE-003-013 | DIRECT | One 403 test per implemented operation; role chosen from the permission matrix seed. | COVERED |
| BR5 | Generated code is produced at build time and is not edited by hand. | SPEC-RWB-TE-003-003, SPEC-RWB-TE-003-004 | DIRECT | Generated packages are marked generated; a hand edit fails the diff check. | COVERED |
| X1 | A response no longer matches the specification. | SPEC-RWB-TE-003-008, SPEC-RWB-TE-003-009 | DIRECT | Build log: `contract broken: {operationId} at {path}`. | COVERED |
| X2 | The specification breaks a lint rule. | SPEC-RWB-TE-003-002 | DIRECT | Build fails before generation. | COVERED |
| X3 | An operation returns a status not in its specification. | SPEC-RWB-TE-003-010 | DIRECT | `undocumented status {status}`. | COVERED |
| X4 | A current-release operation has no implementation. | SPEC-RWB-TE-003-006 | DIRECT | `{operationId} has no implementation`. | COVERED |
| X5 | A later-release operation has no implementation. | SPEC-RWB-TE-003-007 | DIRECT | Listed as pending; build passes. | COVERED |
| X6 | The front end uses a field removed from the specification. | SPEC-RWB-TE-003-011 | DIRECT | Type check fails with file and line. | COVERED |
| X7 | An operation answers 200 to a role without the right. | SPEC-RWB-TE-003-013 | DIRECT | `access not enforced for {operationId}`. | COVERED |
| X8 | A role without the right calls an operation. | SPEC-RWB-TE-003-012 | DIRECT | 403, `application/problem+json`, MSG-P4-002. | COVERED |
> **AC cleanup (4 November 2026):** all previous acceptance criteria in this story were development-process criteria and were removed from story §7. This engineering enabler has no business acceptance criteria; the coverage table above maps the business rules and exception paths only.

## User story intent interpretation
As a **squad member (RW-TRIBE)**, I want **server interfaces and front-end types generated from the OpenAPI file, with a contract test and an access test per endpoint**, so that **the front end and the service never drift from the specification and no endpoint skips its access check**.

The story turns the API specification into the build's source of truth. The service compiles against generated interfaces, the front end against generated types, and every implemented operation is called with a fixture and checked against the file. A second parameterized test calls each operation as a role without the declared right and expects the specified 403. It adds no screen and no endpoint; it prevents drift and missing access checks.
## Entry trigger and preconditions
| Item | Value |
|---|---|
| Trigger | Every pull request and every build of `main`. |
| Preconditions | RWB-TE-001 done; `api/recovery-api.yaml` in the repository with `x-module`, `x-capability` and `x-first-release` on every operation; permission matrix seed available (RWB-E1-037); build property `rwb.release` set to `E1` for the 30 November 2026 release. |
| Input | OpenAPI file; generated server interfaces and models; generated front-end types and client; permission matrix seed; synthetic fixtures per operation. |
| Output | Compiled service and front end; a report of passed, failed and pending operations; a failing build on any contract or access defect. |
| Feature flag | None — a build check has no runtime path. |
## Field-level behaviour matrix
| Entity / artefact | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| OpenAPI operation | `operationId` | API file | Editable by pull request | Unique; camel case; required by lint |
| OpenAPI operation | `x-module` | API file | Editable by pull request | One of P1–P10, S1–S9 |
| OpenAPI operation | `x-capability.area`, `x-capability.right` | API file | Editable by pull request | Area from the permission matrix; right C/R/U/D/A |
| OpenAPI operation | `x-first-release` | API file | Editable by pull request | E1–E6; compared with `rwb.release` |
| OpenAPI response | status, schema | API file | Editable by pull request | Error responses use the Problem schema |
| Generated server model | fields | OpenAPI schema | Not hand-edited | Regenerated at build time |
| Generated front-end type | fields | OpenAPI schema | Not hand-edited | Regenerated before the type check |
| Report | operation, release, status, reason | Test run | Read-only | Operation names only; no payload or personal data |
## Status-transition matrix
| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| Operation pending | `x-first-release` at or before `rwb.release` | Controller exists and contract passes | Passed | Build proceeds |
| Operation pending | `x-first-release` at or before `rwb.release` | No controller or contract failure | Failed | Build fails; report names the operation |
| Operation pending | `x-first-release` after `rwb.release` | No controller | Pending | Build passes; report lists it |
| Build passed | A contract or access defect is introduced | Any failure | Build failed | Merge blocked |
| No case status change | — | — | — | This story does not touch `recovery_case` |
## Exceptional-case behaviour
| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Response no longer matches the file | Contract test fails naming operation and JSON path | Build log: `contract broken` |
| X2 | Specification breaks a lint rule | Build fails before generation | Build log: lint rule broken |
| X3 | Undeclared status returned | Contract test fails | `undocumented status {status} for {operationId}` |
| X4 | E1 operation has no implementation | Build fails | `{operationId} has no implementation` |
| X5 | E2 operation has no implementation | Pending; build passes | Report: pending |
| X6 | Front end uses a removed field | Type check fails | Build log: type error with file and line |
| X7 | Operation answers 200 to a role without the right | Build fails | `access not enforced for {operationId}` |
| X8 | Role without the right calls an operation | 403 Problem; nothing changes | MSG-P4-002 |
## API change assessment
| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | All operations in `api/recovery-api.yaml`; 76 are first in E1 and 68 are first in E2–E6 at the time of writing. |
| Contract delta | None. The story consumes the file; it does not add or change an operation or schema. |
| Backward compatibility | Unchanged. Generated code replaces hand-written models with the same contract. |
| Authorization | Each operation's `x-capability.area` and `right` are tested; 403 with `messageCode` MSG-P4-002. |
| Error behaviour | 401, 403, 404, 409, 422 and 503 as declared per operation; every error uses the Problem schema. |
| Versioning | No version change; `rwb.release` selects the release under build. |
## Unit Test Applicability
| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE |, SPEC-RWB-TE-003-004, SPEC-RWB-TE-003-011 | No hand-written component, screen, route or state change. The front-end output is generated types and a typed client; the type check and the contract test are the verification. | The front end compiles against the regenerated types; a removed field fails the type check with file and line. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | BR1–BR5; SPEC-RWB-TE-003-001..021 | New lint rule set, generators, `OperationCatalog`, contract test, access test and fixtures. | Unit tests cover catalog release filtering, missing implementation, pending operation, lint failure, schema mismatch, undocumented status and access-not-enforced detection. |
## Detailed design
### Components
| Component | Type | Responsibility |
|---|---|---|
| `recovery-api` rule set | Rule table | Lint rules for BR2: required fields, unique `operationId`, Problem error schema. |
| Server generator configuration | Job | Generates Spring interfaces and models into the shared generated package; one interface per tag. |
| Front-end generator script | Job | Generates TypeScript types and a typed fetch client into `ace-web/src/modules/recovery/api/generated`. |
| `OperationCatalog` | Service | Reads operations, release and capability; joins each operation to its controller method. |
| `RecoveryContractTest` | Service | Parameterized success test per implemented operation; validates status, content type and schema. |
| `RecoveryAccessContractTest` | Service | Parameterized 403 test per implemented operation; chooses a role without the right from the seed. |
| `ContractFixtures` | Repository | Synthetic fixture data per operation; no production data. |

### Package and build outputs
Generated server code in `<ACE base package>.recovery.generated.web` and `.model`; contract tests in `ace-service/src/test/java/<ACE base path>/recovery/contract`; front-end output in `ace-web/src/modules/recovery/api/generated`. Both generated packages are listed as shared in `architecture/recovery-modules.yaml` (RWB-TE-001). No hand edit is permitted; a change goes into the OpenAPI file.

### Data and migration
No database object and no Flyway migration. Tests use an in-memory PostgreSQL-compatible database with synthetic rows. No business field is read or written; the only data read is the permission matrix seed and the fixtures.

### Rules
1. Lint runs first; a missing `operationId`, `x-module`, `x-capability`, `x-first-release` or Problem error schema fails the build.
2. Generation runs from the file only; a generated file that differs from a clean regeneration fails the build.
3. `OperationCatalog` selects operations with `x-first-release` at or before `rwb.release`; later operations are pending.
4. Every selected operation must have a controller method and a passing contract test.
5. The contract test validates status, content type and schema, and reports the first JSON path that differs.
6. The access test selects a role whose permission in the declared area lacks the right, calls the operation, and expects 403 with `application/problem+json` and `messageCode` MSG-P4-002.
7. The report lists passed, failed and pending operations; any failure fails the build.

### Transaction and events
None. The build is deterministic for the same commit and the same permission seed. No event is published; no runtime path exists.

### Security and authority
| Actor | What they may do |
|---|---|
| RW-TRIBE, tribe lead, squad members | Change the specification and implementations; run the build |
| TechX tech leads | Approve a change to the specification file (code owners, RWB-TE-002) |
| RW-SECADM | Owns the permission matrix that the access tests read |
| No Workbench capability area applies to the build | The access tests exercise the endpoint rights |

The access test is the control that every endpoint enforces its declared right; a 200 is a build failure, not a test warning.

### Observability and operations
- The build report lists each operation, its release, status and failure reason.
- The measure is contract defects found in SIT, target zero.
- The report is published in the build artefacts and kept with the pull request.
- No runtime metric, alert or run book.

### Performance
No runtime path. The contract suite runs in the pull request pipeline; no numeric target is stated. Keep the suite parallel by operation so the build stays inside the pipeline budget; record duration in the report.

### Feature flag and rollback
None. A build check has no runtime path. Rollback is a revert of the specification or rule change through a pull request.

### No UI change
No screen. Developers read the report in the build artefacts. Existing screens consume the generated client; a removed field fails their type check, which is the intended early warning.
## Test scenarios
| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-TE-003-01 | BR1, BR5 | System | Specification change adding `warnAt` to `Timer` | Server model and front-end type hold `warnAt`; both compile |
| TC-TE-003-02 | BR3 | System | Fixture returns text for `escalationLevel` | Build fails; names operation and `$[0].escalationLevel` |
| TC-TE-003-03 | BR2 | System | Operation with no `x-capability` | Lint fails naming the operation |
| TC-TE-003-04 | BR3 | System | Fixture returns 400 not in the file | `undocumented status 400` |
| TC-TE-003-05 | BR3 | System | `getAdminJobs` with no implementation in E1 | `getAdminJobs has no implementation` |
| TC-TE-003-06 | Engineering verification | System | `postQueuesQueueidPlacements` first in E2 | Build passes; listed as pending |
| TC-TE-003-07 | BR1 | System | `legalHold` removed from `Case` | Type check fails with file and line |
| TC-TE-003-08 | BR4 | System | Fixture controller with no access check | `access not enforced` |
| TC-TE-003-09 | X8 | Security | RW-REFADM calls `getCasesCaseidTimers` | 403; Problem; MSG-P4-002 |
| TC-TE-003-10 | BR2, BR5 | Unit | Spec with duplicate `operationId` and a hand-edited generated file | Lint fails; regeneration diff fails |
| TC-TE-003-11 | BR3 | Unit | Catalog with E1, E2 and E3 operations at `rwb.release=E1` | Only E1 is mandatory; E2/E3 pending |
## Guardrails
- No business value in code: capability areas and rights come from the specification and the permission matrix.
- No personal data in logs, tests or prompts; fixtures are synthetic and the report holds operation names only.
- No read of another module's tables; each module's controller implements its own generated interface.
- Generated code is never edited; a change goes into the specification.
- The 79-operation figure in the story is not hard-coded; the catalog enumerates the file.
## Out of scope
- Contract tests for file interfaces: RWB-E1-007.
- Browser tests on the screens that use the generated client: RWB-TE-010.
- The permission matrix content: RWB-E1-037.
## Traceability
| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Adapters log, retry and follow one pattern with a contract test | Program §5.2 | None | All recovery processes | None | TC-TE-003-01..TC-TE-003-07, TC-TE-003-10, TC-TE-003-11 |
| REQ-ACA-003 | The permission matrix is the only source of what a role may do | Program §5.4 | None | All recovery processes | None | TC-TE-003-08, TC-TE-003-09 |
## Clarification Log
| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | §2; SPEC-005 | The story says 79 operations; the API specification v2 holds 144 operations, of which 76 are first in E1. | A hard-coded count would fail immediately. | The file is the source (BR1); the catalog enumerates it and the report prints the counts. The 79 figure is historical and is not used. | RESOLVED | SPEC-005, SPEC-015 |
| CLAR-002 | BR2; SPEC-002 | Does the lint require an `If-Match` header where a story uses optimistic concurrency? | Two stories add the header; a missing declaration would be invisible. | The lint checks the fields the story names. The endpoint stories that use `If-Match` add it to the file as part of their contract delta. | RESOLVED | SPEC-002 |
| CLAR-003 | §3; SPEC-012 | The permission matrix seed is a precondition from RWB-E1-037. | The access test cannot choose a role without it. | The seed is available to tests; the build fails clearly if it is absent. | RESOLVED | SPEC-012 |
| CLAR-004 | BR5; SPEC-003, SPEC-004 | Where do generated packages sit in the module map? | TE-001's map must list them as shared. | TE-001 lists `recovery.generated.*` as shared; TE-003 adds the entry if it is absent. | RESOLVED | SPEC-003 |
| CLAR-005 | SPEC-007 | What makes an operation "later"? | Determines pending versus failed. | `x-first-release` after `rwb.release`; the release property is E1 for this build. | RESOLVED | SPEC-005, SPEC-007 |
| CLAR-006 | SPEC-012 | Which role is used when several lack the right? | Determinism of the access test. | Choose the first role in the seed, ordered by role code, that lacks the right; record it in the report. | RESOLVED | SPEC-012 |

`CLARIFICATION_STATUS: RESOLVED` — all six items are answered from the story, the API file or the permission model. No item changes behaviour.
## Status reporting
```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this build-tooling story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New generation, contract-test and access-test build capability over the existing OpenAPI file; no endpoint or schema change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: contract enforcement only; the file is unchanged]
REQUIREMENT_COVERAGE_SUMMARY: No business acceptance criteria (story §7); all 5 business rules, 8 exception paths and the access path are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 5] [COVERED_RULES: 5] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

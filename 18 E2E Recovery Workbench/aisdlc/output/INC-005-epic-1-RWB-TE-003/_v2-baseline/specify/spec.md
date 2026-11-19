# Technical Specification — RWB-TE-003 Types and contract tests from the API specification

| Field | Value |
|---|---|
| Story | RWB-TE-003 — Types and contract tests from the API specification |
| Epic / module | E1 / P2 Integration (technical enabler); build tooling, generated interfaces and contract/access tests; no business endpoint |
| RUN_ID | `INC-005-epic-1-RWB-TE-003` |
| Source requirement | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-003-types-and-contract-tests-from-the-api-specification-v1.md` (v1, 28 October 2026); `requirement/RecoveryWorkbench_Requirements.md`; increment card `docs/increments/INC-005-epic-1-RWB-TE-003.md` |
| Upstream IDs | `REQ-DRI-007`; `REQ-ACA-003`; `US-RWB-TE-003`; `BR-RWB-013` / `FR-RWB-013` in the traceability matrix (technical-enabler grouping only); API Specification v4; TE-001 module map; D-RCV-05, D-RCV-11, D-RCV-37, D-RCV-39, D-RCV-40, D-RCV-43; MSG-P4-002 |
| Governing decisions | D-RCV-05 (no pipeline change), D-RCV-06/40 (80% coverage), D-RCV-11 (Modulith), D-RCV-37 (module map), D-RCV-39 (frontend imports), L-RCV-11 (contract baseline), L-RCV-14 (generated package), `AGENTS.md` §3/§4, `CLAUDE.md` two-repository rule |
| Status | `SUCCESS` — spec gate PASS; 0 Critical/High/Medium findings; 6 Low findings carried |
| API audit | `output/INC-005-epic-1-RWB-TE-003/specify/api-audit.md` |
| Prepared | 2026-11-17 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner spec gate (source story set v7/v6, 16 Nov 2026); Compliance Reviewer `REVIEW-RWB-TE-003-SPEC-001` |

## v2 baseline delta (17 November 2026)

| Change | Effect on this story | Source |
|---|---|---|
| Build order 5, before any controller | The contract suite cannot require all 73 E1 operations to be implemented on day one. `L-RCV-11` introduces a versioned enforcement baseline: an E1 operation is pending with its owning story until that story sets `enforce: true`. AC5 is proven with a fixture operation in the baseline that has no controller. | Build Sequence v6; story defect row 93; `OPEN-039` |
| API Specification v4 | The story narrative says 79 operations. v4 has 141 operationIds: 73 E1, 38 E2, 8 E3, 10 E4, 8 E5 and 4 E6. The build reads the file; the E1 build selects 73. `getAdminJobs` is E1; `postQueuesQueueidPlacements` is E2; both still exist. | API Specification v4; `OPEN-039` |
| Generated package | Generated server code is a published package of the P2 `integration` module: `recovery.integration.generated.web` and `.model`. This avoids a 20th nested module in the TE-001 map. The map's published list is extended; the generator writes the `@NamedInterface` package-info files. This resolves `REVIEW-RWB-TE-001-009` by relocation; the TE-001 spec text is left as implemented history and is not edited. | TE-001 module map; D-RCV-37; L-RCV-14 |
| FSD AC | Story §2 cites `AC-P2-001-01`, which is the outbound file-interface contract test (INT-25), not the API contract test. This spec treats the API contract requirement as BR1/BR3 and `REQ-DRI-007`; it does not claim `AC-P2-001-01`. | FSD P2 v6; story defect row 92/93 |
| Front end | The typed client is generated into `frontend/src/modules/recovery/api/generated` (gitignored). No screen is built. | D-RCV-39; frontend context |

## Assumptions

| ID | Assumption | Basis | Effect if wrong |
|---|---|---|---|
| `ASM-TE003-01` | The ACE repository holds the canonical OpenAPI file at `api/recovery-api.yaml`; the document-set copy is the source of the copy. | Story §3; API Specification v4. | A drift between the two files is a contract defect; the plan adds a byte-equality check. |
| `ASM-TE003-02` | The repository host and Gradle/Node toolchain can run an OpenAPI generator and a front-end generator in the existing build. | TE-001 build evidence; story §3. | The plan gate approves the pinned plugin/dependency versions; no new runtime service. |
| `ASM-TE003-03` | The 73 E1 operations each have an owning story in the Build Sequence. The story map is a versioned data file, `api/recovery-api-implementation.yaml`. | Build Sequence v6; story §13 "pending with a named story". | A missing story mapping is a lint failure; no operation is silently pending. |
| `ASM-TE003-04` | The permission matrix seed is available to the access suite; until E1-037 loads it, a synthetic test fixture with RW-REFADM is used for the harness. | Story §3; RWB-E1-037. | The live access case remains blocked; no mocked role is recorded as passing. |
| `ASM-TE003-05` | The generated server interfaces use the operationId as the Java method name and one interface per OpenAPI tag. | OpenAPI Generator `spring` behaviour; story §12. | The catalog's implemented-operation resolver changes; the contract does not. |
| `ASM-TE003-06` | The generated packages are published under P2 `integration` as `generated.web` and `generated.model`; no hand-written code lives there. | TE-001 module map; D-RCV-37; L-RCV-14. | A new root `recovery.generated` would need a 20th module and a map-schema change; the plan uses the published-package route. |
| `ASM-TE003-07` | `warnAt` is already in API v4's `Timer`; the AC1 fixture adds it to a minimal copy to prove generation, and the live generated model also contains it. | API Specification v4 line 6602. | The AC1 evidence is fixture-only; the live type still contains `warnAt`. |
| `ASM-TE003-08` | New build/test/runtime dependencies are acceptable only with plan-gate approval and pinned versions. | `AGENTS.md` §4.4; README known limits. | The plan gate rejects the dependency and the story is re-planned; no unpinned dependency is merged. |
| `ASM-TE003-09` | `x-capability.area: None` marks an authentication-only operation. The access suite records it `NOT_APPLICABLE_AUTHENTICATED` and tests 401 without a session; it does not record a 403 pass. This applies to `getFeatureFlags` and `getMeSession` in v4. | API Specification v4; BR4; AC8. | The API owner assigns a real capability area or confirms the exception (`OPEN-042`); no code change to the suite. |
| `L-RCV-03` | No question was asked; the sequencing, count and package ambiguities are recorded here and in `docs/open-items.md`. | No-question rule. | A wrong default is visible at the plan gate. |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen, route, component, label, state or i18n key. The generated client is build output, not a screen. |
| Logic In Scope | `YES` — lint rules, generation, operation catalog, release baseline, contract validation and access-test harness. |
| API In Scope | `YES` — the API specification is the source of generated server/front-end types and the contract suite. No endpoint is added or changed. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `api/recovery-api.yaml`; TE-001 module map (`backend/src/test/resources/architecture/recovery-modules.yaml`); `backend/build.gradle.kts`; `frontend/package.json`, frontend build/typecheck; `git` ignore rules; ACE CI `check` (no pipeline change, D-RCV-05). |
| New Nodes Required | `YES` — `api/recovery-api-implementation.yaml`; Gradle lint/generate/contract tasks; `OperationCatalog`, `ContractBaseline`, `ImplementedOperationResolver`, `RecoveryContractTest`, `RecoveryAccessContractTest`, `ContractFixtures`; front-end generator wrapper and its unit test; generated packages `recovery.integration.generated.web` and `.model`; report artifact. |
| Inherited Existing Behavior | TE-001 module map and boundary tests; ACE Gradle build and `check`; frontend Nx `check` and Vitest; API Specification v4; MSG-P4-002 wording; Spring Security method checks from RWB-E1-022. |
| Frontend Changes Required | `YES` — a generator wrapper, generated types/client (gitignored) and build wiring. No hand-written screen or component. |
| Backend Changes Required | `YES` — build/test tooling, generated interfaces/models (build output) and the contract/access suites. No production endpoint, entity or migration. |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | The OpenAPI file is the only source of endpoints, request and response schemas. | SPEC-RWB-TE-003-001 | DIRECT | No hand-written endpoint or DTO duplicates the file. | COVERED |
| BR2 | Every operation carries operationId, x-module, x-capability with area and right, and x-first-release; every error response uses the Problem schema. | SPEC-RWB-TE-003-002 | DIRECT | Lint resolves `$ref` through `components.responses` to `Problem`. | COVERED |
| BR3 | Every operation first in the current release or earlier has an implementation and a passing contract test. | SPEC-RWB-TE-003-005, -006, -007 | DIRECT | Enforced through the versioned implementation baseline; pending E1 operations name their story (`L-RCV-11`). | COVERED |
| BR4 | Every operation refuses a role whose permission lacks the declared right with 403 and messageCode MSG-P4-002. | SPEC-RWB-TE-003-008 | DIRECT | Access suite; live case blocked by E1-022/E1-037. | COVERED |
| BR5 | Generated code is produced at build time and is not edited by hand. | SPEC-RWB-TE-003-003, -004, -010 | DIRECT | Generated packages and client are build artifacts; no hand edit. | COVERED |
| AC1 | A property added to the OpenAPI file appears in both the generated server model and the front-end type; both compile. | SPEC-RWB-TE-003-003, -004, -013 | DIRECT | Fixture adds `warnAt` to a minimal Timer; live v4 already has it. | COVERED |
| AC2 | A response field of the wrong type fails the contract test, naming the operation and `$[0].escalationLevel`. | SPEC-RWB-TE-003-007, -012 | DIRECT | Raw JSON fixture bypasses the generated model. | COVERED |
| AC3 | An operation with no x-capability fails the lint before generation, naming the operation. | SPEC-RWB-TE-003-002 | DIRECT | Lint runs before `openApiGenerate`. | COVERED |
| AC4 | A status not in the specification fails the contract test with `undocumented status 400`. | SPEC-RWB-TE-003-007, -012 | DIRECT | 400 is absent from the fixture's declared responses. | COVERED |
| AC5 | A current-release operation in the baseline with no controller method fails the build. | SPEC-RWB-TE-003-005, -006, -007 | DIRECT | Fixture baseline: `getAdminJobs`, `enforce: true`, no controller. | COVERED |
| AC6 | A later-release operation with no controller is listed pending and the E1 build passes. | SPEC-RWB-TE-003-005, -006, -009 | DIRECT | `postQueuesQueueidPlacements` E2, not in the E1 baseline. | COVERED |
| AC7 | A front-end screen that reads a removed field fails the type check, naming the file and line. | SPEC-RWB-TE-003-004, -013 | DIRECT | Fixture screen reads `Case.legalHold`; fixture spec removes it. | COVERED |
| AC8 | An endpoint that skips its access check returns 200 to a role without the right and fails the build with `access not enforced`. | SPEC-RWB-TE-003-008 | DIRECT | Fixture controller without the check; live suite uses the E1-022 guard. | COVERED |
| Flow 1–8 | Lint, generate server, generate front end, compile, catalog current operations, contract-test each implemented operation, access-test each, report passed/failed/pending. | SPEC-RWB-TE-003-001..-012 | DIRECT | The build tasks follow the flow order. | COVERED |
| X1–X8 | Contract broken; lint broken; undocumented status; current operation with no implementation; later operation pending; front-end removed field; access not enforced; 403 with MSG-P4-002. | SPEC-RWB-TE-003-002, -006, -007, -008, -012, -013 | DIRECT | Each exception has a fixture or a report state. | COVERED |
| §12 Contract | Input, lint, server generation, front-end generation, contract test, access test, output, trigger, idempotency. | SPEC-RWB-TE-003-001..-010 | DIRECT | The contract is the build pipeline contract. | COVERED |
| §17 Guardrails | No business value in code; no personal data; no read of another module's tables; generated code never edited. | SPEC-RWB-TE-003-002, -010, -011 | DIRECT | Capability and rights come from the file; fixtures are synthetic; no cross-module table read. | COVERED |
| §19 Out of scope | File-interface contract tests (E1-007); browser tests (TE-010); permission matrix content (E1-037). | SPEC-RWB-TE-003-012 | DIRECT | Not built here. | COVERED |

## User story intent interpretation

As a **squad member (RW-TRIBE)**, I want **server interfaces and front end types generated from the OpenAPI file, with a contract test and an access test per endpoint**, so that **the front end and the service never drift from the specification and no endpoint skips its access check**.

The story is an API-governance enabler. It makes one OpenAPI file the source of the Spring interfaces,
the TypeScript types and the typed client, and it adds a build-time suite that fails when an
implemented operation's request, response or status drifts from the file, or when an implemented
operation answers a role that lacks its declared right. At build order 5 no controller exists yet, so
the suite starts with an empty enforcement baseline; each endpoint story flips its operations to
enforced in the same merge request. The report always shows what is implemented, what is pending and
which story owns it.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Every pull request and every build of the main branch; the `check` task runs the lint, generation, contract and access suites. |
| Preconditions | RWB-TE-001 done (module map and folders); `api/recovery-api.yaml` present; `rwb.release` names the release (`E1`); the permission matrix seed or its synthetic test fixture is available; the build can run the pinned generators; code-owner approval for the API file (TE-002). |
| Input | `api/recovery-api.yaml`; `api/recovery-api-implementation.yaml`; `rwb.release`; permission matrix seed; synthetic fixtures. |
| Output | Generated Spring interfaces/models; generated TypeScript types/client; a contract report of passed, failed and pending operations; a pass/fail build. |
| Feature flag | None. A build check has no runtime path to switch off. |

## Field-level behaviour matrix

No business field is read or written (story §11). The fields below belong to the API contract and the
test data artefacts.

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| Operation | `operationId` | API Specification v4 | Reviewed change to the file | Unique; non-empty; matches the generated Java method name. |
| Operation | `x-module` | API Specification v4 | Reviewed change | Required; one of P1–P10 or S1–S9 (the 19 modules). |
| Operation | `x-capability.area`, `x-capability.right` | API Specification v4 | Reviewed change | Required; area is a capability area or `None` (authentication-only, right `R`); right is `R`, `C`, `U`, `D` or `A`. |
| Operation | `x-first-release` | API Specification v4 | Reviewed change | Required; `E1`–`E6`; selects the release gate. |
| Operation | Error responses | API Specification v4 | Reviewed change | At least one 4xx/5xx; each resolves to `Problem`; `application/problem+json`. |
| Baseline | `release` | `api/recovery-api-implementation.yaml` | Reviewed change | Current build release (`E1`). |
| Baseline | `operationId`, `story`, `enforce` | Story map + Build Sequence | Reviewed change per endpoint story | Every E1 operation has a story; `enforce: true` only when the controller is in the same MR. |
| Report | `operationId`, release, status, story, reason | Build | Generated | Passed, failed or pending; no personal data. |

## Status-transition matrix

No case status changes (story §9). The build result and the report state change:

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| Not built | Lint | A BR2 rule fails | FAILED | Build stops before generation; the log names the operation and rule. |
| Lint passed | Generation | Generator succeeds | GENERATED | Server interfaces/models and front-end types/client emitted. |
| Generated | Contract run | An enforced operation has no controller | FAILED | `{operationId} has no implementation`. |
| Generated | Contract run | A response/status/schema differs | FAILED | `contract broken: {operationId} at {path}: {reason}` or `undocumented status {status} for {operationId}`. |
| Generated | Contract run | An enforced operation passes | PASSED | Report row. |
| Generated | Contract run | A current/later operation is not enforced | PENDING | Report row names the owning story. |
| Contract passed | Access run | A role without the right gets 200 | FAILED | `access not enforced for {operationId}`. |
| Contract passed | Access run | The role gets 403 + Problem + MSG-P4-002 | PASSED | Report row. |
| Any | Any failure | — | FAILED | Merge blocked; report artifact retained. |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / report |
|---|---|---|---|
| X1 | A response no longer matches the specification | Contract test fails naming operation and JSON path | `contract broken: {operationId} at {path}: {reason}` |
| X2 | The specification breaks a lint rule | Build fails before generation | `lint rule broken: {operationId} {rule}` |
| X3 | An operation returns a status not in its specification | Contract test fails | `undocumented status {status} for {operationId}` |
| X4 | An enforced current-release operation has no controller | Build fails | `{operationId} has no implementation` |
| X5 | A later-release operation has no controller | Listed pending; build passes | `pending: {operationId} ({story})` |
| X6 | The front end uses a field removed from the specification | Type check fails naming file and line | TypeScript error |
| X7 | An operation answers 200 to a role without the declared right | Build fails | `access not enforced for {operationId}` |
| X8 | A role without the right calls an operation | 403 Problem with MSG-P4-002 | `MSG-P4-002` |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Endpoints delivered | None. The story consumes API Specification v4 and generates interfaces/types; it adds no path, request or response. |
| Contract delta | None. The file is the contract; the story adds `api/recovery-api.yaml` as the repository copy and a test-only baseline file, not an API change. |
| Backward compatibility | Additive tooling only; no runtime change. |
| Authorization | The access suite reads the declared `x-capability` and the permission matrix; it does not change an endpoint's authorization. |
| Versioning | No API version change. The OpenAPI file stays v4. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | YES — generator wrapper + generated types/client + build wiring; no screen | REQUIRED | 80% lines, statements, branches and functions on `frontend/scripts/recovery-api/**` | SPEC-004, -013; AC1, AC7 | The wrapper is hand-written logic (read spec, emit `schema.d.ts` and `client.ts`, write package-info); the generated output itself is not hand-written. Vitest with synthetic fixture specs. | Deterministic output; `warnAt` reaches the generated type; a removed `legalHold` makes the fixture screen fail typecheck; no network. |
| Backend | YES — lint/catalog/baseline/contract/access tooling; generated interfaces/models are build output | REQUIRED | 80% lines, statements, branches and functions on `th.co.scb.ace.demo.recovery.contract` and the lint task classes | SPEC-001..-012; AC1–AC8 | `OperationCatalog`, `SpecLint`, `ContractBaseline`, `ImplementedOperationResolver` are hand-written; the contract/access suites are integration tests. JaCoCo. | Lint rules; release selection; implemented resolver; baseline pending/enforced; contract failure text; access failure text; no PII. |

Separately required system/contract/access tests remain in scope (story §16). They are not replaced by
unit tests.

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `api/recovery-api.yaml` | Contract | The single OpenAPI 3.1 source; repository copy of API Specification v4. |
| `api/recovery-api-implementation.yaml` | Data | Release, operationId, owning story and `enforce` flag for the E1 baseline. |
| `RecoveryApiLint` | Build task | Run the BR2 lint before generation; fail on a missing operationId, x-module, x-capability, x-first-release, duplicate operationId, unresolved `$ref`, or an error response that is not Problem. |
| `OperationCatalog` | Test-support service | Read the OpenAPI file; expose operations by release, capability and story; select current-release operations. |
| `ContractBaseline` | Test-support service | Read the implementation baseline; answer `enforced`, `pending`, and the owning story. |
| `ImplementedOperationResolver` | Test-support service | Find controller beans whose methods implement the generated interfaces and whose names match operationIds. |
| `RecoveryContractTest` | Parameterised test | For each enforced implemented operation: call it with a synthetic fixture; validate request, response, status, content type and schema against the file. |
| `RecoveryAccessContractTest` | Parameterised test | For each enforced implemented operation: choose a role from the permission matrix seed/fixture that lacks the declared right; expect 403, `application/problem+json`, `messageCode = MSG-P4-002`; fail `access not enforced` on 200. |
| `ContractFixtures` | Test fixture registry | Synthetic fixture request/response per operation; no production data. |
| `RecoveryApiReport` | Build output | `build/reports/recovery-contract/contract-report.json` and `.md`; passed/failed/pending, operationId, release, story, reason. |
| `RecoveryFrontendGenerator` | Node/TS wrapper | Run `openapi-typescript`; write `schema.d.ts`, `client.ts` and the `package-info.java` files; deterministic. |

### Packages and boundaries

- Server generation: `th.co.scb.ace.demo.recovery.integration.generated.web` (one interface per tag)
  and `th.co.scb.ace.demo.recovery.integration.generated.model` (schemas).
- The TE-001 module map's P2 `integration` `published` list is extended with `generated.web` and
  `generated.model`; the generator writes a `package-info.java` with `@NamedInterface("generated.web")`
  and `@NamedInterface("generated.model")`. No hand-written code lives in either package.
- Contract/access tests and support: `th.co.scb.ace.demo.recovery.contract` in `src/test`.
- Front end: `frontend/src/modules/recovery/api/generated/schema.d.ts` and `client.ts` (gitignored,
  generated before typecheck); wrapper and unit test in `frontend/scripts/recovery-api/`.
- The generated code is committed only if the build decides to pin it; the default is build output, not
  source. If committed, it is generated, not edited (BR5).

### Lint rules (BR2)

The lint reads the YAML and fails on:

1. A missing or duplicate `operationId`.
2. A missing or invalid `x-module`.
3. A missing `x-capability.area` or `x-capability.right`; `area: None` is accepted only with
   `right: R` and is treated as authentication-only.
4. A missing or invalid `x-first-release` (not E1–E6).
5. `$ref` that does not resolve.
6. An operation with no 4xx/5xx response.
7. A 4xx/5xx response that does not resolve to `application/problem+json` + `Problem`.
8. A schema in `components.schemas` not referenced or a referenced schema not defined (warning only;
   the first seven are hard failures).

The lint runs as a Gradle task before `openApiGenerate`; a failure stops the build before any generated
code is emitted.

### Generation

**Server.** `org.openapi.generator` Gradle plugin, pinned at the plan gate; generator `spring`,
`interfaceOnly=true`, `useSpringBoot3=true`, `useTags=true`, `apiPackage=...integration.generated.web`,
`modelPackage=...integration.generated.model`, `generateApiTests=false`, `generateModelTests=false`.
One interface per tag, one method per operationId. The generated source is in `build/generated`.

**Front end.** `openapi-typescript` (dev dependency) produces `schema.d.ts`; `openapi-fetch` (runtime
dependency) is used by the generated `client.ts` to expose the typed client. Both versions are pinned
at the plan gate. The wrapper runs before `typecheck`; the generated folder is in `.gitignore` and is
not edited. A byte-for-byte second run proves determinism.

### Operation catalog and release baseline

`api/recovery-api-implementation.yaml`:

```yaml
release: E1
operations:
  - operationId: getCases
    story: RWB-E1-002
    enforce: false
  - operationId: getCasesCaseidTimers
    story: RWB-E1-028
    enforce: false
  # ... one row for each of the 73 E1 operations
```

- Every E1 operation has one row. `story` comes from the Build Sequence and the story set; the plan
  task creates the initial 73 rows. A missing row is a lint failure.
- `enforce: false` means the operation is pending with its story; the report shows it. An endpoint
  story sets `enforce: true` in the same MR that adds the controller, and that MR must pass the
  contract and access tests.
- A controller method found for an operation with no baseline row is a failure (`operation not in
  baseline`); a baseline row with `enforce: true` and no controller is `has no implementation`.
- `rwb.release` selects the rows; `E1` is the current build. Later releases add their own rows when
  their increments open.

### Contract test

- For every enforced, implemented operation, `RecoveryContractTest` uses `MockMvc` with the generated
  interface and the controller bean.
- It validates the request against the file (parameters, body, content type), the response status
  against the declared responses, the response content type and the response body against the schema.
- It uses `swagger-request-validator-mockmvc` (pinned test dependency) and synthetic fixtures.
- A mismatch reports `contract broken: {operationId} at {jsonPath}: {reason}`; an undeclared status
  reports `undocumented status {status} for {operationId}`.
- A fixture controller can return raw JSON for the negative AC2/AC4 cases; the live path uses the
  generated model.

### Access test

- For every enforced, implemented operation, `RecoveryAccessContractTest` reads the declared capability
  area and right from the file.
- It chooses a role from the permission matrix seed whose letters in that area lack the right; until
  E1-037 loads the real matrix, the test uses a synthetic fixture with `RW-REFADM` and records the live
  case as blocked.
- An operation with `x-capability.area: None` is authentication-only. The suite records
  `NOT_APPLICABLE_AUTHENTICATED` and tests 401 without a session; it does not record a 403 pass. The
  two v4 operations are `getFeatureFlags` and `getMeSession` (`ASM-TE003-09`, `OPEN-042`).
- It calls the operation with that role and expects 403, `application/problem+json` and
  `messageCode = MSG-P4-002`. A 200 means the endpoint skipped its check: `access not enforced for
  {operationId}`.
- A fixture controller without the check proves AC8; a fixture with the check proves the pass path.
- `TC-TE-003-09` (live `RW-REFADM` calls `getCasesCaseidTimers`) stays `BLOCKED` until E1-022/E1-037;
  no mocked role is recorded as a pass.

### Report

`build/reports/recovery-contract/contract-report.json` and `.md` list every E1 operation with:

| Field | Value |
|---|---|
| `operationId` | The operation. |
| `release` | `E1` (or the build release). |
| `story` | Owning story from the baseline. |
| `status` | `PASSED`, `FAILED` or `PENDING`. |
| `reason` | Failure text, or `pending: story not yet merged`. |
| `contract`, `access` | Per-suite result. |

The report is retained as build evidence. A failure fails the build; a pending row does not.

### Module map

`backend/src/test/resources/architecture/recovery-modules.yaml` gains `generated.web` and
`generated.model` in the P2 `integration` `published` list. `ModuleMapLoader` already validates a list
of published sub-packages; the boundary rule already allows a dependency on a published package. The
generated `package-info.java` files carry `@NamedInterface("generated.web")` and
`@NamedInterface("generated.model")`. TE-001's rule that a published package has `@NamedInterface` is
satisfied. No new module is added.

### Build integration

| Task | When | Fails on |
|---|---|---|
| `recoveryApiLint` | Before `openApiGenerate` | BR2 rule breach. |
| `openApiGenerate` | After lint | Generator error. |
| `generateRecoveryFrontendTypes` | Before frontend `typecheck` | Generator error; non-deterministic output. |
| `recoveryContractTest` | `test` / `check` | Enforced operation missing or contract mismatch. |
| `recoveryAccessContractTest` | `test` / `check` | Access not enforced or wrong error body. |
| `recoveryApiReport` | After both suites | Always writes; a failed suite fails the build. |

No pipeline file changes (D-RCV-05): the tasks join the existing Gradle/frontend `check`. The build
property `rwb.release` defaults to `E1` and is overridable with `-Prwb.release=...` or an environment
variable; it is not a business value in code.

### Security, privacy and audit

- The access suite uses synthetic roles and the permission matrix seed/fixture; no production user.
- Fixtures are synthetic; no personal data, account number, secret or production data.
- The API file and generated code contain schema names and operationIds, not personal data.
- The generated client uses the existing ACE API client boundary; no direct `fetch` in a screen.
- A failure report contains operationIds and paths only; no request body with personal data.

### Performance, determinism and rollback

- Lint and generation run once per build; the contract/access suites call each implemented operation
  once with a synthetic fixture. At TE-003 the enforced set is empty; the suite grows with the
  endpoint stories.
- The same commit and `rwb.release` produce the same generated code and the same report (determinism
  test: run twice, diff).
- Rollback: revert the build wiring and the baseline file; no database, no migration and no runtime
  path. The generated code is not a deployed artifact until an endpoint story uses it.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-TE-003-01 | AC1, BR1, BR5 | System | Fixture spec adds `warnAt` to Timer | Server model and front-end type hold `warnAt`; both compile. |
| TC-TE-003-02 | AC2, BR3 | System | Fixture returns `"two"` for `escalationLevel` | Build fails; report names `getCasesCaseidTimers` and `$[0].escalationLevel`. |
| TC-TE-003-03 | AC3, BR2 | System | Operation with no x-capability | Lint fails before generation, naming the operation. |
| TC-TE-003-04 | AC4, BR3 | System | Fixture returns 400; spec lists 200,401,403,404,503 | `undocumented status 400 for getCasesCaseidTimers`. |
| TC-TE-003-05 | AC5, BR3 | System | Baseline `getAdminJobs enforce: true`, no controller | `getAdminJobs has no implementation`. |
| TC-TE-003-06 | AC6 | System | `postQueuesQueueidPlacements` E2, no controller, E1 build | Build passes; report lists it pending. |
| TC-TE-003-07 | AC7, BR1 | System | Fixture spec removes `legalHold`; fixture screen reads it | Front-end type check fails, naming file and line. |
| TC-TE-003-08 | AC8, BR4 | System | Fixture controller skips the access check; `RW-REFADM` | Returns 200; build fails `access not enforced`. |
| TC-TE-003-09 | Access | Access | `RW-REFADM` calls `getCasesCaseidTimers` | `BLOCKED` live until E1-022/E1-037; fixture-level check passes; expect 403 + MSG-P4-002 when live. |

The full Given/When/Then is in Recovery Workbench Test Cases v7, tab Story test cases, under the same
IDs. `TC-TE-003-09` is recorded as `BLOCKED`, not `PASSED`, until the live role/matrix exists.

## Guardrails and out of scope

Guardrails (story §17):

- No business value in code: capability areas and rights come from the specification and the permission
  matrix.
- No personal data in logs, tests or prompts; fixtures are synthetic and the report holds operation
  names only.
- No read of another module's tables; each module's controller implements its own generated interface.
- Generated code is never edited; a change goes into the specification.

Out of scope (story §19):

- Contract tests for file interfaces: RWB-E1-007.
- Browser tests on the screens that use the generated client: RWB-TE-010.
- The permission matrix content: RWB-E1-037.
- Any endpoint, controller, entity, migration or screen as a business deliverable.

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | Story §4 step 5, AC5, §13 Done when; build order 5; story defect row 93 | No controller exists at build order 5, so a strict current-release failure cannot pass, while the story allows an E1 operation to be pending with a named story. | The suite needs a versioned enforcement baseline or the first build fails for 73 operations. | `L-RCV-11`: an E1 operation is pending with its story until the owning endpoint story sets `enforce: true`; AC5 is proven with a fixture. `OPEN-039` records the plan-gate acceptance. | RESOLVED | SPEC-005, -006, -007, -009 |
| CLAR-002 | Story §2; API Specification v4 | The story says 79 operations; v4 has 141 (73 E1). | A fixed count would be wrong; the suite must read the file. | Read the file; select by `rwb.release`; E1 is 73. The count delta is recorded in `OPEN-039`. | RESOLVED | SPEC-001, -005 |
| CLAR-003 | Story §12; TE-001 module map; `ASM-TE003-06` | The story says a "shared generated package listed in the module map"; TE-001 has no shared-package entry. | A new root `recovery.generated` would need a 20th module and a map-schema change. | Use the P2 `integration` published packages `generated.web` and `generated.model`; the generator writes the `@NamedInterface` package-info files. `L-RCV-14`. | RESOLVED | SPEC-003, -011 |
| CLAR-004 | Story §13; `ASM-TE003-03` | Where does the "named story" for a pending operation come from? | The report needs a story per operation. | `api/recovery-api-implementation.yaml` is the versioned E1 baseline; it names the owning story and the `enforce` flag. | RESOLVED | SPEC-005, -006, -009 |
| CLAR-005 | Story §2; FSD P2 v6 | `AC-P2-001-01` is the outbound file-interface contract test, not the API contract test. | The story's traceability would overclaim an AC. | The API contract requirement is BR1/BR3 and `REQ-DRI-007`; `AC-P2-001-01` is not claimed. | RESOLVED | SPEC-001, -007 |
| CLAR-006 | Story §16 TC-TE-003-09; `ASM-TE003-04` | The live access test needs roles and the permission matrix from E1-022/E1-037, which are later. | The live case cannot pass at TE-003 time. | Build the harness and fixture-level AC8 now; record TC-TE-003-09 as `BLOCKED` until E1-022/E1-037. `OPEN-040`. | RESOLVED | SPEC-008 |
| CLAR-007 | Story §13; `ASM-TE003-08` | Which generator/validator dependencies and versions are allowed? | A new dependency needs plan approval. | Pin them at the plan gate: OpenAPI Generator, swagger-request-validator, openapi-typescript, openapi-fetch. No unpinned dependency. | RESOLVED | SPEC-002, -003, -004 |
| CLAR-008 | Story §12; `ASM-TE003-05` | What is unit-tested on the front end if no screen is built? | The generated client is not hand-written. | The generator wrapper is the hand-written logic; Vitest covers it at 80%. The generated output is verified by determinism and typecheck. | RESOLVED | SPEC-004, -013 |
| CLAR-009 | BR4, AC8; `ASM-TE003-09` | Two E1 operations (`getFeatureFlags`, `getMeSession`) declare `x-capability.area: None`; there is no capability right to test. | The access suite cannot choose a role that lacks a right in a non-existent area. | Treat `None` as authentication-only: record `NOT_APPLICABLE_AUTHENTICATED` and test 401 without a session; no 403 pass. The API owner confirms or assigns a real area (`OPEN-042`). | RESOLVED | SPEC-008 |

`CLARIFICATION_STATUS: RESOLVED` — all 9 items are answered from the story, TE-001, API Specification
v4 or the no-question decisions. No question was asked.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this API-tooling story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: Generate server interfaces and front-end types from API Specification v4; add contract and access suites; no endpoint, screen or schema change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NO_API_CHANGE] [REASON: build-time API contract tooling over the existing v4 file]
REQUIREMENT_COVERAGE_SUMMARY: 5 business rules, 8 ACs, 8 flow steps, 8 exception paths, contract and guardrails are mapped across 18 requirement rows.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 18] [COVERED_RULES: 18] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```

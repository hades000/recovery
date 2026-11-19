---
run_id: INC-005-epic-1-RWB-TE-003
story: RWB-TE-003
stage: specify
round: remediation 1 (answers review/spec-gate-review.md, REVIEW-RWB-TE-003-SG2)
status: DRAFT — pending spec gate review-2 (review/spec-gate-review-2.md)
date: 2026-11-17
---

# Technical Specification — RWB-TE-003 Types and contract tests from the API specification

| Field | Value |
|---|---|
| Story | RWB-TE-003 — Types and contract tests from the API specification |
| Epic / module | E1 / P2 Integration (technical enabler). Build tooling, generated server interfaces and models, front-end type drift check, contract and access suites. No business endpoint, screen or migration. |
| RUN_ID | `INC-005-epic-1-RWB-TE-003` |
| Source requirement | Epic 1 Story Files v7, `rwb-te-003-types-and-contract-tests-from-the-api-specification-v1.md` (story v1, 28 Oct 2026), path `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/`; increment card `aisdlc/docs/increments/INC-005-epic-1-RWB-TE-003.md` |
| Upstream IDs | `REQ-DRI-007`, `REQ-ACA-003` (story §18); `BR-RWB-013` / `FR-RWB-013` (Traceability Matrix v2.0 §3, INC 005) |
| API source | API Specification v4 (OpenAPI 3.1.0, `info.version` 4.0.0), document-set path `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml`; repository copy `api/recovery-api-v4.yaml`, SHA-256 `535cb46594190f0bf535a2ad3f034e9f50f987a92fe19c0524a2755f5923b891` (byte-identical, verified in `review/spec-gate-review.md` §1 and again in this run) |
| Code baseline | This repository, commit `c22ee73` (`AI-SDLC-BUILD-LOG.md` §5). Spring Boot 4.1.2, Java 21, Jackson 3, Spring Modulith 2.1.1 (`backend/build.gradle.kts`; `RUN-BRIEF.md` "Local stack facts"); React 19, TypeScript 5.9.3, `openapi-typescript` 7.13.0, `openapi-fetch` 0.17.0 (`frontend/package.json`) |
| Governing decisions | D-RCV-05 (no pipeline change), D-RCV-06 and D-RCV-40 (80% coverage), D-RCV-37 (module map location), D-RCV-39 (front-end import allow-list), D-RCV-43 (test-scope tooling measured), D-RCV-44 (Testcontainers outside `check`), L-RCV-03 (no questions), L-RCV-11 (enforcement baseline, premise restated in SPEC-009), L-RCV-14 (generated packages under P2, restated in SPEC-018), D-RUN-05 (fresh gate in this repository) — `aisdlc/docs/decisions/decision-register.md`, `AI-SDLC-BUILD-LOG.md` §1 |
| Earlier versions | `_v2-baseline/specify/` (17 v2 workspace, ACE monorepo). Kept: requirement reading, counts, `area: None` handling, BLOCKED live access case, synthetic fixtures (confirmed correct in `review/spec-gate-review.md` §1). Replaced: everything SG2-01..SG2-12 found wrong. Map: `gate-response.md`. |
| Status | **DRAFT — pending spec gate review-2.** No gate result applies yet. `REVIEW-RWB-TE-003-SPEC-001` (17 v2 workspace) does not apply here (D-RUN-05); `REVIEW-RWB-TE-003-SG2` was **FAIL** (2 High, 7 Medium, 3 Low). |
| Author | Technical Specifier (agent run) |

## 1. Preconditions that gate the build (not the spec)

| ID | Precondition | Source | If not met |
|---|---|---|---|
| PRE-1 | **RWB-TE-001 is merged in this repository**, with its module map at `backend/src/test/resources/architecture/recovery-modules.yaml`, its module-map rule and its boundary tests. RWB-TE-001's remediated spec (`aisdlc/output/INC-002-epic-1-RWB-TE-001/specify/`, being written in parallel) owns the map. TE-003 is planned and built after it (Build Sequence v6: TE-003 order 5 "Depends on RWB-TE-001"; D-RUN-01 dependency waves). | Story v7 §3 bullet 1; increment card "Depends on"; `review/spec-gate-review.md` SG2-07; audit A-01, A-02 (owner RWB-TE-001) | The Implementation Planner stops and reports. TE-003 does not create a module map, a module skeleton or a nested module. |
| PRE-2 | The merged TE-001 map names a module whose `code` is `P2` and gives it a package root (written `<P2>` in this spec; `th.co.scb.ace.demo.recovery.integration` in the TE-001 v2 spec, `_v2-baseline/specify/spec.md` field matrix). That package is a Spring Modulith nested module. | TE-001 v2 spec SPEC-001/-002; story v7 §3 "the generated packages are listed in the module map as shared"; L-RCV-14 | The planner stops. TE-003 never assumes `recovery.integration` exists. |
| PRE-3 | RWB-TE-001 merged with an approved backend coverage scope that passes `recoveryCoverageVerification` (TE-001 finding `REVIEW-RWB-TE-001-020`). | `output/INC-002-epic-1-RWB-TE-001/review/spec-gate-review.md` finding 020 | SPEC-017 wires the global gate only on that approved scope; if none exists the planner stops on SPEC-017 (b) and reports. |
| PRE-4 | Plan-gate spikes S-1..S-4 (§9) have a recorded result and, where a spike fails, the named fallback is approved. | `review/spec-gate-review.md` SG2-10 | The planner records the failure; fallback F-1b is a human decision (stop). |

## 2. Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` — no prior trace chain for RWB-TE-003 in this repository (Traceability Matrix v2.0 §3 row 005 has no SPEC IDs; `review/spec-gate-review.md` SG2-09). |
| UI In Scope | `NO` — no screen, route, component, label, state or i18n key (story v7 §15 "No screen"). |
| Logic In Scope | `YES` — lint, server generation, front-end drift check, operation catalog, enforcement baseline, resolver, contract, access and method-security suites, report. |
| API In Scope | `YES` — API Specification v4 is the input. No endpoint is added or changed. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `api/recovery-api-v4.yaml` (read only); `backend/build.gradle.kts`; `workflow/internal/TemporalAdminController.java` (or its TE-001 location) — retrofit only; `platform/internal/ApiExceptionHandler.java` and `ProblemFactory.java` — `traceId` only; TE-001 module map (P2 `published` list); `frontend/package.json` (scripts only); `frontend/src/contexts/ApiClientContext.tsx` (type only). |
| New Nodes Required | `YES` — `api/recovery-api-implementation.yaml`, `api/recovery-api-ruleset.yaml`, `api/recovery-api-v4.sha256`; Gradle source set `apiTooling`; Gradle tasks `recoveryApiLint`, `recoveryApiGenerate`, `recoveryApiPackageInfo`, `recoveryApiFixtureGenerate`, `recoveryContractCoverageVerification`; test package `th.co.scb.ace.demo.recovery.contract`; Vitest file `frontend/src/modules/recovery/__tests__/contract/apiTypes.test.ts`; `npm` script `api:verify`. |
| Inherited Existing Behavior | `api:generate` → committed `frontend/src/api/schema.d.ts` (deterministic; regenerated identical in `review/spec-gate-review.md` §1); `ApiClientContext` typed `openapi-fetch` client `Client<paths>`; D-RCV-39 ESLint block (`frontend/eslint.config.js`) and its `src/api/schema.d.ts` ignore; `SecurityConfig` filter chain (bearer JWT, `RW-` role gate, E401/E403 entry points); `ApiExceptionHandler` / `ProblemFactory` Problem bodies; `ModulithTest.verify()`; `RecoveryBoundaryTest`; JaCoCo tasks; `.gitlab-ci.yml` jobs `backend-unit` (`./gradlew test recoveryCoverageReport`) and `frontend-check` (`npm run check`, `npm run build`); `PlatformE2ETest` smoke cases. |
| Frontend Changes Required | `YES` — `package.json` scripts, one type alias in `ApiClientContext.tsx`, one Vitest file. No screen, no new dependency, no second type set or client. |
| Backend Changes Required | `YES` — build/test tooling, generated code (build output), retrofit of one existing controller onto its generated interface, `traceId` on the 500 Problem. No new endpoint, entity or migration. |

## 3. Requirement-to-SPEC Logic Coverage

All rows cite story v7 sections unless marked. SPEC IDs are defined in §6.

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | The OpenAPI file is the only source of endpoints, request and response schemas. | 001, 003, 006, 007, 014 | DIRECT | Every recovery handler is a v4 operation or on the README-decision-6 allow-list; one front-end type set; generated models replace hand-written DTOs on spec operations. | COVERED |
| BR2 | Every operation carries operationId, x-module, x-capability (area, right), x-first-release; every error response uses Problem. | 002, 011 | DIRECT | Lint L1–L7 before generation; Problem completeness asserted at runtime because v4 `Problem` has no `required` list. | COVERED |
| BR3 | Every operation first in the current release or earlier has an implementation and a passing contract test. | 008, 009, 010, 011 | DIRECT | Through the versioned baseline (L-RCV-11, premise restated). | COVERED |
| BR4 | Every operation refuses a role lacking the declared right with 403 and MSG-P4-002. | 005, 012 | DIRECT | Access suite per enforced operation; all-handler method-security check. | COVERED |
| BR5 | Generated code is produced at build time and is not edited by hand. | 003, 006, 019 | DIRECT | Server code in `build/` only; front-end file committed but drift-checked on every `check`. | COVERED |
| AC1 | `warnAt` added to Timer appears in the server model and the front-end type; both compile. | 003, 006, 021 | DIRECT | Live v4 Timer has `warnAt` (line 6602); fixture generation proves a change propagates on both sides. | COVERED |
| AC2 | Wrong-typed `escalationLevel` fails, naming the operation and `$[0].escalationLevel`. | 011, 015 | DIRECT | Raw-JSON fixture controller. | COVERED |
| AC3 | An operation with no x-capability fails at lint, naming the operation. | 002 | DIRECT | Lint runs before `recoveryApiGenerate`. | COVERED |
| AC4 | A 400 not in the spec fails with `undocumented status 400`. | 011 | DIRECT | `getCasesCaseidTimers` declares 200, 401, 403, 404, 503 (API v4). | COVERED |
| AC5 | A current-release operation with no controller fails with `getAdminJobs has no implementation`. | 009 | DIRECT | Fixture baseline `getAdminJobs enforce: true`, no controller. | COVERED |
| AC6 | A later-release operation with no controller is pending; E1 build passes. | 008, 009, 015 | DIRECT | `postQueuesQueueidPlacements` is E2 in v4; live report lists it. | COVERED |
| AC7 | A screen reading removed `legalHold` fails the type check naming file and line. | 006, 021 | DIRECT | In-test fixture spec and fixture screen; TypeScript compiler diagnostic. | COVERED |
| AC8 | An endpoint skipping its access check answers 200 to RW-REFADM and fails with `access not enforced`. | 005, 012 | DIRECT | Fixture controller without a check, in a fixture context. | COVERED |
| Flow 1 | Lint first; missing operationId, x-capability or error response fails. | 002 | DIRECT | | COVERED |
| Flow 2 | Generate Spring server interfaces and models. | 003, 004 | DIRECT | One interface per operation, abstract methods only. | COVERED |
| Flow 3 | Generate TypeScript types and typed client. | 006 | DIRECT | Existing `api:generate` + `ApiClientContext`; drift check added. | COVERED |
| Flow 4 | Compile service and front end against generated code. | 003, 006, 014 | DIRECT | `compileJava` depends on generation; `check` verifies types before `typecheck`. | COVERED |
| Flow 5 | List operations with x-first-release ≤ `rwb.release`; find implementing controller method. | 008, 010 | DIRECT | Resolver reads MVC handler mappings. | COVERED |
| Flow 6 | Call each implemented operation with its fixture; validate request and response. | 011 | DIRECT | | COVERED |
| Flow 7 | Call each operation as a role lacking the right; expect 403 MSG-P4-002. | 012 | DIRECT | | COVERED |
| Flow 8 | Report passed, failed, pending; any failure fails the build. | 015, 016 | DIRECT | | COVERED |
| X1 | Response mismatch → `contract broken`. | 011 | DIRECT | | COVERED |
| X2 | Lint rule broken → fail before generation. | 002 | DIRECT | | COVERED |
| X3 | Undocumented status → fail. | 011 | DIRECT | Includes 500 (no v4 operation declares 500). | COVERED |
| X4 | Current-release operation without implementation → fail. | 009 | DIRECT | Only for baseline rows with `enforce: true`. | COVERED |
| X5 | Later-release operation without implementation → pending. | 009, 015 | DIRECT | | COVERED |
| X6 | Front end uses removed field → type error. | 006, 021 | DIRECT | | COVERED |
| X7 | 200 to a role without the right → `access not enforced`. | 012 | DIRECT | | COVERED |
| X8 | Role without the right → 403 Problem MSG-P4-002. | 012 | DIRECT | Fixture level now; live TC-TE-003-09 BLOCKED (OPEN-040). | COVERED |
| §12 Contract | Input, lint, server and front-end generation, contract and access test, output, trigger, idempotency. | 001–016, 019 | DIRECT | Deviations from §12 wording recorded in `document-gaps.md` (TE003-SG-DG-01..03, TE003-SP-DG-01). | COVERED |
| §13 step 2 | Make one existing controller implement its generated interface. | 014 | DIRECT | `postAdminWorkflowsSmoke`. | COVERED |
| §17 G1 | No business value in code; areas and rights from the spec and the matrix. | 002, 012, 020 | DIRECT | Rule set and fixture matrix are data files. | COVERED |
| §17 G2 | No personal data; report holds operation names only. | 015, 020 | DIRECT | | COVERED |
| §17 G3 | No read of another module's tables; each module's controller implements its own generated interface. | 003, 010, 018 | DIRECT | Per-operation interfaces; module-ownership check against the TE-001 map. | COVERED |
| §17 G4 | Generated code never edited. | 003, 006, 019 | DIRECT | | COVERED |
| §19 | Out of scope: file-interface contracts (RWB-E1-007), browser tests (RWB-TE-010), permission matrix content (RWB-E1-037). | §12 of this spec | INHERITED_EXISTING_BEHAVIOR | Not built. | COVERED |

36 rows, 0 BLOCKED.

### 3.1 Phase-0 audit items assigned to this story

Source: `aisdlc/evidence/phase0-standards-audit.md` (Owner column). Each item is taken into scope with SPEC, acceptance criteria and tests, or excluded with a cited reason and the owning story.

| Item | Part | Disposition | SPEC / owner | Reason (source) |
|---|---|---|---|---|
| A-03 | No test proves every endpoint has a method check | **In scope** | SPEC-005, T-TE003-12/13 | AGENTS §3.3; BS-3.2. |
| A-03 | Checks name roles or `isAuthenticated()`, not the capability area; role literals in code | **Excluded** → RWB-E1-022 and RWB-E1-037 | OPEN-040 (amended) | E1-022 v7 §13 component `AccessCheckInterceptor` "reads the capability area and right declared on each endpoint (x-capability)"; E1-037 v7 BR1 makes the matrix the only source of rights. TE-003 cannot name a capability check that does not exist yet. |
| A-04 | `api:generate` already exists | **In scope (extend, never duplicate)** | SPEC-006, SPEC-007 | RUN-BRIEF "extend or correct it, never duplicate it"; FS-4.2. |
| A-08 | `messageCode` and `traceId` on every 4xx/5xx Problem | **In scope** | SPEC-011 (assertion), SPEC-013 (`traceId` on 500) | BR2; BS-3.3 (`traceId`); API v4 `Problem` has no `required` list, so schema validation alone cannot catch it. |
| A-08 | 500 has no `messageCode` | **Excluded** → message-standard owner (new open item NEW-TE003-B) | `document-gaps.md` TE003-SG-DG-04 | Error and Message Standard v4 §4 has no message ID for an unexpected error, and API v4 declares no 500. TE-003 must not invent a message ID (AGENTS §4.10). Any 500 already fails the contract suite as an undocumented status (SPEC-011). |
| A-08 | No 400/422 mapping for binding/validation failures; `field` never set | **Excluded** → AISDLC-HARDENING (audit header rule), open item NEW-TE003-C | `document-gaps.md` TE003-SP-DG-03 | (1) API v4 gives no status for a malformed request on operations that declare neither 400 nor 422 (e.g. `getCasesCaseidTimers`: 200, 401, 403, 404, 503); 4 of 141 operations declare 400 and 64 declare 422. (2) AGENTS §3.6 requires validation messages from the message table, which is not seeded (README decision 5). (3) The only operation enforced at TE-003, `postAdminWorkflowsSmoke`, has no parameter or body. |
| A-08 | `{action}` filled with English "do this", also in `messageTh` | **Excluded** → RWB-E1-022 | OPEN-040 (amended) | E1-022 v7 AC2 fixes the action text per call ("MSG-P4-002 with action 'read roles'") and owns the 403 refusal (X1). Error and Message Standard v4 §3 ("formatted for the language") gives no Thai action values. The access suite asserts `messageCode` only (story §12). |
| A-09 | Contract job missing | **In scope** | SPEC-016 | Suites run inside the `test` task that `backend-unit` already runs; front-end drift check inside `npm run check` that `frontend-check` already runs (D-RCV-05: no pipeline change). |
| A-09 | Coverage verification job missing | **In scope** | SPEC-017 | Wired in Gradle as a finalizer of `test` (D-RCV-05 compatible). |
| A-09 | PDPA lint job | **Excluded** → RWB-TE-011 | — | TE-011 v7 §1/§4 step 7 is "a pipeline check that finds personal data". |
| A-09 | Playwright/axe job | **Excluded** → RWB-TE-010 | — | Story v7 §19 "Browser tests …: RWB-TE-010"; testing-standards §1 Accessibility row names RWB-TE-010. |
| A-09 | Dependency scan and ZAP baseline jobs | **Excluded** → AISDLC-HARDENING (no story owns them), open item NEW-TE003-D | `document-gaps.md` TE003-SP-DG-04 | testing-standards §1 Security row requires them; no Epic 1 TE story in v7 (TE-001..TE-013) names them; TE-011 v7 covers PDPA lint only. |
| A-11 | Hand-written `Problem` in `ApiClientContext.tsx:32-41` | **In scope** | SPEC-007 | FS-4.2; D-RCV-39. |
| A-11 | Hand-written `PlatformInfo`, `TemporalHealth` (`platform.ts:8-21`) | **Excluded as a recorded exception** (README decision 6), open item NEW-TE003-A | SPEC-001 allow-list | Their endpoints are not in API v4, so nothing can be generated for them. |
| A-11 | No ESLint fixture test for D-RCV-39 | **Excluded** → RWB-TE-001 | — | D-RCV-40 assigns the "ESLint Node-API fixture test" to RWB-TE-001; `REVIEW-RWB-TE-001-024` reduces TE-001's front-end work to that fixture test. |
| A-15 | `QueryState.tsx` has no 401 / expired-session state | **Excluded** → AISDLC-HARDENING or the first story with a screen, open item NEW-TE003-E | — | Story v7 §15 "No screen"; FS-3.1 applies to screens. |

## 4. User story intent interpretation

As a **squad member (RW-TRIBE)**, I want **server interfaces and front end types generated from the OpenAPI file, with a contract test and an access test per endpoint**, so that **the front end and the service never drift from the specification and no endpoint skips its access check** (story v7 §1).

In this repository the story does five things:

1. Lints API Specification v4 before anything is generated (BR2).
2. Generates one Spring interface **per operation**, with no default method, plus the models. A controller implements only the interfaces of the operations it delivers, so an operation that is not built is never a reachable handler (SPEC-003/-004; §7.1).
3. Keeps the one existing front-end type set (`api:generate` → `src/api/schema.d.ts`, `@/api/schema`, `ApiClientContext`) and makes `npm run check` fail when it is stale (SPEC-006).
4. Tests every implemented operation against the file (contract), against a role without the right (access), and tests every recovery handler for a Spring Security method check (SPEC-005, -011, -012).
5. Reports every operation as passed, failed or pending with its owning story (SPEC-015).

**Restated premise (replaces "no controller exists", SG2-03).** At build order 5 one E1 operation is already implemented in the platform baseline: `postAdminWorkflowsSmoke` (`TemporalAdminController.java:89-108`, registered only when `rwb.p3.temporal=true`, line 44). Its owning story is RWB-E1-071 (E1-071 v7 §4 step 9 and §12 "POST /api/recovery/v1/admin/workflows/smoke"). Two further handlers under `/api/recovery/v1` are not in API v4: `GET /platform/info` and `GET /admin/temporal/health` (README decision 6). The other 72 E1 operations have no controller.

## 5. Entry trigger and preconditions

| Item | Value | Source |
|---|---|---|
| Trigger | Every merge request and every build of `develop-recovery` / `main`: CI jobs `backend-unit` and `frontend-check`; locally `./scripts/dev.ps1 test`. | Story v7 §12 "Trigger"; `.gitlab-ci.yml`; `scripts/dev.ps1` `test` |
| Preconditions | PRE-1..PRE-4 (§1); `api/recovery-api-v4.yaml` present; `rwb.release` set (default `E1`). | Story v7 §3 |
| Input | `api/recovery-api-v4.yaml`; `api/recovery-api-v4.sha256`; `api/recovery-api-ruleset.yaml`; `api/recovery-api-implementation.yaml`; TE-001 module map; Gradle property `rwb.release`; test-scope fixture permission matrix (until the E1-037 seed). | Story v7 §3, §12, §13 |
| Output | Generated server interfaces and models under `backend/build/generated/recovery-api/`; verified `frontend/src/api/schema.d.ts`; `backend/build/reports/recovery-contract/contract-report.json` and `.md`; pass/fail build. | Story v7 §12 "Output" |
| Feature flag | None. A build check has no runtime path to switch off. | Story v7 §13 "Feature flag" |

## 6. SPEC items

| SPEC ID | Statement | FR / REQ | Story ref | Tests |
|---|---|---|---|---|
| SPEC-RWB-TE-003-001 | **BR1 handler conformance.** Every request-mapping handler under `/api/recovery/v1` registered in the contract context (SPEC-010) maps, by HTTP method and normalised path template (base path `/api/recovery/v1` stripped, every `{name}` compared as `{}`), to exactly one API v4 operation, or to a row of `outsideSpecification` in `api/recovery-api-implementation.yaml`. Initial rows: `GET /platform/info` and `GET /admin/temporal/health`, each with `decision: README decision 6`, `owner: API owner`, `openItem: NEW-TE003-A`. Otherwise the build fails: `operation not in specification: {METHOD} {path}`. Allow-listed handlers still need a method check (SPEC-005) and are reported as `OUTSIDE_SPECIFICATION`. | FR-RWB-013; REQ-DRI-007 | BR1; §12 | T-TE003-10, -11 |
| SPEC-RWB-TE-003-002 | **Lint (BR2) before generation.** Gradle task `recoveryApiLint` reads `api/recovery-api-v4.yaml` and fails before `recoveryApiGenerate` on: L1 operationId missing, duplicate, or not a valid Java identifier; L2 `x-module` missing or not a `code` in the TE-001 map; L3 `x-capability.area` or `.right` missing, right not in the rule set's letters, area not in the rule set's areas or `None`, or `None` with a right other than `R`; L4 `x-first-release` missing or not in the rule set's releases; L5 no 4xx/5xx response; L6 a 4xx/5xx response (followed through `components.responses`) whose content is not the rule set's error media type with a `$ref` to the rule set's error schema; L7 an unresolved `$ref`; L8 (warning only) a schema never referenced; L9 baseline consistency (every operation with x-first-release ≤ `rwb.release` has one baseline row; every row names an existing operationId and a story key matching `RWB-(E[0-9]+|TE)-[0-9]{3}`; no duplicate row; `enforce` is boolean; no `outsideSpecification` row collides with a v4 path); L10 the file's SHA-256 differs from `api/recovery-api-v4.sha256`. Failure text: `lint rule broken: {operationId} {rule}` (L10: `lint rule broken: api/recovery-api-v4.yaml L10 — update api/recovery-api-v4.sha256 in the same merge request`). The rule set `api/recovery-api-ruleset.yaml` holds the rights letters `C R U D A` (E1-037 v7 BR2), the releases `E1`–`E6` (API v4 values), the 14 capability areas as declared in API v4 (replaced by LOV-CAPABILITY once RWB-E1-037 seeds it), the error media type `application/problem+json` and the error schema `Problem` (API v4 `components.responses`). Module codes are read from the TE-001 map, not repeated. | FR-RWB-013; REQ-DRI-007 | BR2; AC3; Flow 1; X2; §13 "recovery-api rule set" | TC-TE-003-03; T-TE003-14 |
| SPEC-RWB-TE-003-003 | **Server generation.** Gradle task `recoveryApiGenerate` (OpenAPI Generator Gradle plugin, `spring` generator, pinned at the plan gate — a new build dependency under BS-1.5 / AGENTS §4.4) runs after `recoveryApiLint` and before `compileJava`, into `backend/build/generated/recovery-api/` (never committed). Required output properties: (a) **one Java interface per operation**, named from the operationId, holding exactly one method; (b) **no `default` method and no generated controller class** in any interface (interface only, story v7 §12); (c) models for every schema in `<P2>.generated.model`, interfaces in `<P2>.generated.web` (`<P2>` per PRE-2); (d) target Spring Boot 4.1.2 / Spring Framework 7 / Jackson 3 and Java 21 — generated code may use `com.fasterxml.jackson.annotation` (kept by Jackson 3) but no Jackson 2 `databind` type and no `jackson-databind-nullable`; no Swagger/springdoc annotation dependency; (e) deterministic output (SPEC-019). Candidate settings, proven in spike S-1: `interfaceOnly=true`, `skipDefaultInterface=true`, `useSpringBoot3=true` until a Boot 4 option is proven, `useJakartaEe=true`, `openApiNullable=false`, `annotationLibrary=none`, `documentationProvider=none`, `useTags=true` on a copy whose tags are set to the operationId (generator normalizer rule `SET_TAGS_TO_OPERATIONID` or an equivalent derived-copy step). Rationale in §7.1. | FR-RWB-013; REQ-DRI-007 | BR5; AC1; Flow 2, 4; §12 Server generation; §17 G3 | TC-TE-003-01; T-TE003-15 |
| SPEC-RWB-TE-003-004 | **Generated-handler guard.** A unit test reflects over every type in `<P2>.generated.web` and fails when a type is not an interface, holds other than one method, or holds a `default` method: `generated interface {type} has a default method {method}`. | FR-RWB-013; REQ-ACA-003 | BR4; AGENTS §3.3 | T-TE003-15 |
| SPEC-RWB-TE-003-005 | **Method-security coverage (A-03, hard constraint).** `RecoveryMethodSecurityTest` imports the main classes under `th.co.scb.ace.demo.recovery` (no test classes, no property conditions: every controller class counts, including `@ConditionalOnProperty` ones). For each class meta-annotated `@Controller`, it takes every method that is a handler — a method with a merged `@RequestMapping` found on the class or on any implemented interface, including inherited `default` methods — and fails unless a merged `@PreAuthorize` is present on that method or its declaring class: `no method-security check: {class}#{method} {METHOD} {path}`. The test covers handlers outside the specification and handlers of pending operations. It checks presence only; naming the capability area is RWB-E1-022 (§3.1). | FR-RWB-013; REQ-ACA-003 | BR4; AC8; AGENTS §3.3; BS-3.2 | T-TE003-12, -13 |
| SPEC-RWB-TE-003-006 | **Front-end generation (extend, one type set).** `api:generate` stays the only generator, writing the committed `frontend/src/api/schema.d.ts` read through `@/api/schema` by `ApiClientContext` (`Client<paths>`). New script `api:verify` regenerates and compares (candidate: `openapi-typescript ../api/recovery-api-v4.yaml -o src/api/schema.d.ts --check`, spike S-3; fallback F-3: `npm run api:generate && git diff --exit-code -- src/api/schema.d.ts`). `check` becomes `npm run api:verify && npm run typecheck && npm run lint && npm run coverage`. A stale or hand-edited file fails `check` before `typecheck`. No `src/modules/recovery/api/generated/`, no second client, no new dependency (`openapi-typescript` 7.13.0 and `openapi-fetch` 0.17.0 are already pinned). | FR-RWB-013; REQ-DRI-007 | BR1; BR5; AC1; AC7; Flow 3, 4; X6 | TC-TE-003-01, -07; T-TE003-16 |
| SPEC-RWB-TE-003-007 | **Generated `Problem` type (A-11).** `ApiClientContext.tsx` drops the hand-written `interface Problem` and uses `type Problem = components["schemas"]["Problem"]` from `@/api/schema`. `ApiError` keeps its public shape. `PlatformInfo` and `TemporalHealth` in `platform.ts` stay hand-written under README decision 6 until their endpoints enter API v4 (NEW-TE003-A). | FR-RWB-013 | BR1; FS-4.2 | T-TE003-17 |
| SPEC-RWB-TE-003-008 | **Operation catalog and release selection.** `OperationCatalog` (tooling) reads the file and exposes, per operation: operationId, method, path, x-module, capability area and right, x-first-release, declared statuses and their media types. `rwb.release` (Gradle property, default `E1`, override `-Prwb.release=`; passed to the test JVM) selects operations with x-first-release ≤ release by the order `E1 < … < E6`. No count is coded (API v4 has 141; 73 E1). | FR-RWB-013 | Flow 5; BR3; §3 | T-TE003-18 |
| SPEC-RWB-TE-003-009 | **Enforcement baseline (L-RCV-11, premise restated).** `api/recovery-api-implementation.yaml` holds `release`, `operations[]` (`operationId`, `story`, `enforce`) and `outsideSpecification[]` (`method`, `path`, `decision`, `owner`, `openItem`). Initial content: 73 E1 rows; `postAdminWorkflowsSmoke` `story: RWB-E1-071`, `enforce: true`; the other 72 `enforce: false` with their owning story (the plan fills the story keys from Epic 1 Story Files v7 / Build Sequence v6; an operation no story names is an open item, never a blank row). Outcomes: enforced and not implemented → FAILED `{operationId} has no implementation`; implemented and `enforce: false` → FAILED `{operationId} is implemented but not enforced` (so no reachable operation goes untested); implemented with no row → FAILED `operation not in baseline: {operationId}`; not implemented, `enforce: false`, current release → PENDING `pending: {operationId} ({story})`; later release, not implemented → PENDING `pending: {operationId} (first in {release})`. An endpoint story sets `enforce: true` in the merge request that adds its controller. | FR-RWB-013; REQ-DRI-007 | BR3; AC5; AC6; X4; X5; §13 "Done when" | TC-TE-003-05, -06; T-TE003-19, -20 |
| SPEC-RWB-TE-003-010 | **Implemented-operation resolver.** `ImplementedOperationResolver` (test scope) reads `RequestMappingHandlerMapping.getHandlerMethods()` from the contract context — not interface inheritance — so hand-written handlers count. The contract context sets every property that guards a recovery controller to on (today `rwb.p3.temporal=true`). For each resolved operation it also checks module ownership: the handler's package belongs, per the TE-001 map, to the module whose `code` equals the operation's `x-module`; else FAILED `module mismatch: {operationId} is {x-module} but implemented in {module}`. | FR-RWB-013 | Flow 5; §17 G3 | T-TE003-21 |
| SPEC-RWB-TE-003-011 | **Contract suite.** `RecoveryContractTest`, parameterised over enforced, implemented operations, calls each once with its synthetic fixture (`ContractFixtures`) through MockMvc, as a role holding the right, and validates against the file: request (parameters, body, content type), response status ∈ declared statuses, response content type, response body against the schema. Additionally, for every 4xx/5xx body it asserts `application/problem+json` and non-null `messageCode` and `traceId`. Failure texts: `contract broken: {operationId} at {jsonPath}: {reason}` (JSON Pointer from the validator rendered as JSONPath, `/0/escalationLevel` → `$[0].escalationLevel`); `undocumented status {status} for {operationId}`; `contract broken: {operationId} at $.messageCode: missing` (and `$.traceId`). Validator: `swagger-request-validator-mockmvc`, pinned test dependency (spike S-2; fallback F-2: `com.networknt:json-schema-validator` on schemas resolved by `OperationCatalog`, with status and content-type checks in the suite). Collaborators are stubbed; no database, Temporal server or Docker. | FR-RWB-013; REQ-DRI-007 | BR2; BR3; AC2; AC4; Flow 6; X1; X3 | TC-TE-003-02, -04; T-TE003-22, -23 |
| SPEC-RWB-TE-003-012 | **Access suite.** `RecoveryAccessContractTest`, parameterised over enforced, implemented operations. For an operation with a capability area it picks a role whose letters in that area lack the declared right, from the permission matrix seed when RWB-E1-037 provides it, else from the test-scope fixture `contract/permission-matrix.fixture.yaml`. Fixture rows come only from cited story text: `RW-REFADM` holds no Case record right (TE-003 v7 AC8); `RW-CASEOWN` lacks Platform administration C (E1-071 v7 TC-E1-071-08). It calls the operation with a test JWT (`spring-security-test`) carrying that role and expects 403, `application/problem+json`, `messageCode = MSG-P4-002`, non-null `traceId`. A 2xx → FAILED `access not enforced for {operationId}`. No fixture row and no seed → FAILED `no role without the right for {operationId}`. Operations with `area: None` (`getFeatureFlags`, `getMeSession`) are tested without a token and expect 401 `MSG-P4-001`; reported `NOT_APPLICABLE_AUTHENTICATED`, never a 403 pass (OPEN-042). Each row records `roleSource: SEED | FIXTURE`. Live `TC-TE-003-09` stays `BLOCKED` until RWB-E1-022 and RWB-E1-037 (OPEN-040). | FR-RWB-013; REQ-ACA-003 | BR4; AC8; Flow 7; X7; X8; §12 Access test | TC-TE-003-08, -09; T-TE003-24, -25 |
| SPEC-RWB-TE-003-013 | **`traceId` on every Problem the module writes (A-08 part).** `ApiExceptionHandler.unexpected` sets `traceId` the same way `ProblemFactory` does; the 500 body keeps no `messageCode` (no message ID exists: NEW-TE003-B). The contract context runs with tracing active so the request has a span (spike S-4; fallback F-4: the `traceId` assertion moves to the API Tester REST Assured run against the running stack and the plan says so). | FR-RWB-013 | BR2; BS-3.3 | T-TE003-26 |
| SPEC-RWB-TE-003-014 | **Retrofit of `postAdminWorkflowsSmoke` (story §13 step 2).** The controller that maps `POST /api/recovery/v1/admin/workflows/smoke` (today `workflow/internal/TemporalAdminController`; its TE-001 location if TE-001 moves it) implements the generated `PostAdminWorkflowsSmokeApi` (name per generator), returns the generated 202 model, keeps `@PreAuthorize`, `@ConditionalOnProperty(rwb.p3.temporal)` and the 503 / duplicate-ID behaviour. The hand-written `SmokeStarted` record is removed. Its baseline row is `enforce: true`. `PlatformE2ETest` smoke cases pass unchanged. `GET /admin/temporal/health` in the same class stays hand-written (SPEC-001 allow-list). | FR-RWB-013; REQ-DRI-007 | §13 step 2; AC1; BR1 | T-TE003-27 |
| SPEC-RWB-TE-003-015 | **Report.** After both suites, `backend/build/reports/recovery-contract/contract-report.json` and `contract-report.md` list every v4 operation and every allow-listed handler: `operationId` (or method + path), `xModule`, `release`, `story`, `status` (`PASSED`, `FAILED`, `PENDING`, `OUTSIDE_SPECIFICATION`), `contract`, `access` (`PASSED`, `FAILED`, `NOT_APPLICABLE_AUTHENTICATED`, `NOT_RUN`), `roleSource`, `reason`, plus totals and the input file SHA-256. No timestamp, no request or response body, no token, no personal data. Written even when a suite fails; CI already keeps `backend/build/reports/` (`.gitlab-ci.yml` `backend-unit` artifacts, `when: always`). Expected at TE-003 merge: E1 1 `PASSED`, 72 `PENDING`; E2–E6 68 `PENDING`; 2 `OUTSIDE_SPECIFICATION`. | FR-RWB-013 | Flow 8; §12 Output; §15; §17 G2 | T-TE003-28 |
| SPEC-RWB-TE-003-016 | **Build and CI wiring (A-09 contract part).** Task chain: `recoveryApiLint` → `recoveryApiGenerate` → `recoveryApiPackageInfo` → `compileJava`; `recoveryApiFixtureGenerate` → `compileTestJava`. The contract, access, method-security, guard and tooling tests run inside the existing `test` task (no tag), so `./gradlew test` (CI `backend-unit`, `dev.ps1 test`) runs them; `check` inherits them. Front end: `api:verify` inside `npm run check` (CI `frontend-check`). `.gitlab-ci.yml` is not changed (D-RCV-05). | FR-RWB-013 | §12 Trigger; Flow 8 | T-TE003-29 |
| SPEC-RWB-TE-003-017 | **Coverage (A-09 coverage part).** (a) `recoveryClasses` excludes `**/generated/**` (generated code is not hand-written, BR5; BS-7.2 measures recovery code). (b) `recoveryCoverageVerification` (LINE, BRANCH 80%) becomes a finalizer of `test` on the scope RWB-TE-001 approved (PRE-3), generated packages excluded. (c) New `recoveryContractCoverageVerification`, finalizer of `test`, 80% LINE, BRANCH, INSTRUCTION and METHOD on the `apiTooling` output and on test-scope support classes in `th.co.scb.ace.demo.recovery.contract.support` (D-RCV-43 precedent for measuring test-scope tooling; testing-standards §6). A finalizer failure fails `./gradlew test`. | FR-RWB-013 | BS-7.2; D-RCV-06; D-RCV-40; D-RCV-43 | T-TE003-30 |
| SPEC-RWB-TE-003-018 | **Module map (TE-001 dependency).** TE-003 adds `generated.web` and `generated.model` to the `published` list of the P2 module in the merged TE-001 map, and nothing else (no new module, no schema change). `recoveryApiPackageInfo` — the only writer — writes `package-info.java` with `@NamedInterface("generated.web")` and `@NamedInterface("generated.model")` into the generated source directory. `ModulithTest.verify()`, the TE-001 module-map rule and `RecoveryBoundaryTest` pass with the retrofitted controller depending on P2's published packages. | FR-RWB-013 | §3 bullet 1; §12 "shared generated package listed in the module map"; §17 G3; L-RCV-14 | T-TE003-31 |
| SPEC-RWB-TE-003-019 | **Determinism and no hand edits.** Same commit and `rwb.release` → byte-identical generated server sources, front-end types and report. Server sources live only in `build/`; the front-end file is guarded by `api:verify`. | FR-RWB-013 | BR5; §12 Idempotency; §17 G4 | T-TE003-16, -32 |
| SPEC-RWB-TE-003-020 | **Data guardrails.** Fixtures, fixture JWT subjects and the fixture matrix are synthetic, carry the story key and purpose, and hold no personal data, account number, secret or production data. Capability areas, rights and roles come from API v4, the rule set and the matrix (seed or fixture), never from a literal in suite code. | FR-RWB-013 | §17 G1, G2; testing-standards §2 | T-TE003-33 |
| SPEC-RWB-TE-003-021 | **AC1 / AC7 fixtures.** Back end: `recoveryApiFixtureGenerate` runs the same generator settings on a test fixture spec (`src/test/resources/contract/fixtures/timer-warnat.yaml`, minimal Timer with `warnAt`) into the test source set, package `th.co.scb.ace.demo.recovery.contract.fixture.generated`; a test asserts the generated Timer exposes `warnAt` and the test source set compiles. Front end: `apiTypes.test.ts` (Vitest, `node` environment) uses the `openapi-typescript` and `typescript` Node APIs on in-test fixture specs: (i) Timer with `warnAt` → the type holds it and a fixture usage compiles with 0 diagnostics; (ii) Case without `legalHold` → a fixture screen reading `legalHold` gives a diagnostic naming the fixture file and line. Fixture files are written to a temp directory, never under `src/`, so `npm run typecheck` is unaffected. Live: the generated `Timer` (server and front end) already holds `warnAt` (API v4 line 6602). | FR-RWB-013; REQ-DRI-007 | AC1; AC7; X6 | TC-TE-003-01, -07 |

21 SPEC IDs, each defined once.

## 7. Backend Specification

### 7.1 Contract approach decision (SG2-02 hard constraint)

**Constraint.** No operation may become reachable without a Spring Security method check, including a generated default handler (orchestrator triage SG2-02; AGENTS §3.3; BS-3.2).

| Option | Result against the constraint and the story | Chosen? |
|---|---|---|
| One interface per tag (story v7 §12) | Tags cross `x-module` in API v4: `Administration` spans P1, P2, P3, P4, P6, P10; `Cases` spans P1, P2, P3, P10, S8; `Treatment` spans P2, P6, S1, S2, S3 (16 tags; 33 module-tag pairs; parse of `api/recovery-api-v4.yaml`). With default methods, every unbuilt method is a live 501 handler with no method check (`review/spec-gate-review.md` SG2-02). Breaks §17 G3. | No |
| One interface per owning module, abstract methods | Keeps G3, but a controller must implement every operation of its module (P3 has 27 operations, 17 in E1), so unbuilt operations need hand-written stubs, which are reachable handlers. Breaks the constraint. | No |
| No server generation; contract tests only | Meets the constraint, but drops story v7 §4 step 2, §12 "Server generation" and the server half of AC1. | Fallback F-1b only, by human decision |
| **One interface per operation, abstract method only, plus contract validation of implemented endpoints** | Each interface belongs to one operation and so to one `x-module` (G3). A controller implements only what it delivers; an interface that no bean implements is never a handler. No default method exists (SPEC-003 (b)), and SPEC-004 proves it. SPEC-005 independently fails any handler — generated, inherited or hand-written — without `@PreAuthorize`. Story v7 §6 allows it: "Generator settings are build configuration". | **Yes** |

Interface-declared `@RequestMapping` annotations are honoured by Spring MVC for the implementing controller bean (Spring Framework reference, Web MVC annotated controllers; behaviour proven for this repository in spike S-1). Hence SPEC-005 searches implemented interfaces.

### 7.2 Endpoints, schemas, status codes

No endpoint, schema or status is added or changed (`NO_API_CHANGE`). Reused contract for the one enforced operation:

| Operation | Method / path | x-module | Capability | Declared statuses (API v4) | Owner story |
|---|---|---|---|---|---|
| `postAdminWorkflowsSmoke` | POST `/admin/workflows/smoke` | P3 | Platform administration, C | 202 (`workflowId`, `workflowType`), 401, 403, 404, 503 | RWB-E1-071 |

Example operations used by fixtures: `getCasesCaseidTimers` (P3, Case record R, E1; 200 array of Timer, 401, 403, 404, 503), `getAdminJobs` (P1, Platform administration R, E1; 200, 401, 403, 503), `postQueuesQueueidPlacements` (P3, Queue and allocation C, E2). Source: API v4; `_v2-baseline/specify/api-audit.md` (counts confirmed by `review/spec-gate-review.md` §1).

### 7.3 Authorization, errors, audit

- Authorization is unchanged: `SecurityConfig` requires a bearer JWT and an `RW-` role for `/api/recovery/**`; method security decides the right. Access tests use `spring-security-test` JWTs, not the mock OIDC personas (no `RW-REFADM` persona exists locally; `README.md` "Signing in locally").
- A method-security denial reaches `ApiExceptionHandler.forbidden` → 403 Problem `MSG-P4-002`. No audit or access-log entry is added (A-18 is RWB-E1-039, audit "Low").
- Error change: only SPEC-013 (`traceId` on 500).

### 7.4 Persistence and configuration

No database, migration or reference-data table. Story v7 §11/§13 "in-memory test database" is not available here (OPEN-007 ruling; D-RCV-44): contract fixtures stub collaborators (`JdbcTemplate`, `WorkflowClient`, `WorkflowServiceStubs`, `JwtDecoder`) in a MockMvc context that holds every production recovery controller, `SecurityConfig`, method security and `ApiExceptionHandler` (plan input 4; gap TE003-SP-DG-02). Configuration: `rwb.release` (Gradle property); `rwb.p3.temporal=true` in the contract context only.

### 7.5 Packages and files (this repository)

| Path | Kind | Notes |
|---|---|---|
| `api/recovery-api-v4.yaml` | Input, unchanged | Name kept; `api:generate` reads it (plan input 1; gap TE003-SP-DG-01). |
| `api/recovery-api-v4.sha256`, `api/recovery-api-ruleset.yaml`, `api/recovery-api-implementation.yaml` | New data | SPEC-002, -009. Code-owner approval per RWB-TE-002 once merged (story v7 §10). |
| `backend/build.gradle.kts` | Changed | Plugin, `apiTooling` source set, tasks, test system properties, JaCoCo changes. |
| `backend/src/apiTooling/java/th/co/scb/ace/tooling/recoveryapi/` | New | `RecoveryApiLint`, lint rules, `OperationCatalog`, `ContractBaseline`, `ContractReportWriter`. Package is outside `th.co.scb.ace.demo` so `ModulithTest` and `RecoveryBoundaryTest` imports do not change (ASM-TE003-09). SnakeYAML already on the classpath through Spring Boot. |
| `backend/build/generated/recovery-api/` → `<P2>.generated.web`, `<P2>.generated.model` | Build output | SPEC-003, -018. |
| `backend/src/test/java/th/co/scb/ace/demo/recovery/contract/` | New tests | `RecoveryContractTest`, `RecoveryAccessContractTest`, `RecoveryMethodSecurityTest`, `GeneratedInterfaceGuardTest`, `ContractFixtures`, `support/ImplementedOperationResolver`, `fixture/**` (fixture controllers and contexts). |
| `backend/src/test/java/th/co/scb/ace/tooling/recoveryapi/` | New tests | Unit tests of the tooling. |
| `backend/src/test/resources/contract/` | New fixtures | Fixture specs, fixture baselines, `permission-matrix.fixture.yaml`. |
| Controller mapping `POST /admin/workflows/smoke` | Changed | SPEC-014. |
| `platform/internal/ApiExceptionHandler.java`, `ProblemFactory.java` | Changed | SPEC-013 only. |

### 7.6 Lint, contract and access behaviour

Defined in SPEC-002, -008..-013. Order inside `test`: guard and method-security tests have no ordering dependency on the suites; the report writer runs after both suites (a JUnit `@AfterAll` in a suite listener or a `test` finalizer — plan choice).

## 8. Frontend Specification

| Item | Value | Source |
|---|---|---|
| Screens, routes, states, i18n, accessibility | `NOT_APPLICABLE` — no screen. | Story v7 §15 |
| Design evidence | `NOT_REQUIRED` (UI In Scope = NO). | specification-execution-gates "Design Evidence" |
| API service usage | Unchanged: all calls through `ApiClientContext` (FS-4.1); `client.POST("/admin/workflows/smoke")` already uses generated types (`platform.ts`). | FS-4.1, FS-4.2 |
| Type source | One set: `src/api/schema.d.ts` from `api:generate`, imported as `@/api/schema` (D-RCV-39 allow-list; `eslint.config.js` regex). | SPEC-006 |
| Changes | `package.json` scripts (`api:verify`, `check`); `ApiClientContext.tsx` `Problem` alias; `src/modules/recovery/__tests__/contract/apiTypes.test.ts`. | SPEC-006, -007, -021 |
| Not changed | `platform.ts` (README decision 6 exception), `eslint.config.js`, `vite.config.ts`, `QueryState.tsx` (A-15 excluded). | §3.1 |
| Endpoint-to-screen mapping | Backend-only story; no endpoint delivered. | — |

## 9. Plan-gate spikes and fallbacks (SG2-10)

| Spike | Proves | Pass condition | Fallback |
|---|---|---|---|
| S-1 | Server generation on Spring Boot 4.1.2, Spring Framework 7, Jackson 3, Java 21, OpenAPI 3.1.0 | All 141 operations and 172 schemas generate; one interface per operation; no default method; `compileJava` passes; `TemporalAdminController` compiles against its interface; a MockMvc call reaches it through the interface mapping. | F-1a: `useSpringBoot3=true` output with `openApiNullable=false`, `annotationLibrary=none`, `documentationProvider=none`, compiled on 4.1.2. F-1b (if F-1a fails): **stop**; human decision between "no server generation, contract tests only" (AC1 server half becomes a recorded deviation) and a newer generator version. |
| S-2 | Validator on Spring 7 MockMvc and OpenAPI 3.1.0 | AC2 and AC4 fixtures produce the SPEC-011 texts; a valid smoke response passes. | F-2: `com.networknt:json-schema-validator` (draft 2020-12) on schemas from `OperationCatalog`; status and content type checked by the suite. |
| S-3 | `openapi-typescript` 7.13.0 `--check` | Exit ≠ 0 on a stale file, 0 on a current one, on Windows and on the `node:22` CI image. | F-3: `api:generate` then `git diff --exit-code -- src/api/schema.d.ts`. |
| S-4 | A trace span exists in the contract context | `traceId` non-null on a 401, a 403 and a 503 Problem. | F-4: assert `traceId` in the API Tester run against the running stack; the plan states the move. |

New dependencies to approve at the plan gate (BS-1.5; AGENTS §4.4): OpenAPI Generator Gradle plugin (build), `swagger-request-validator-mockmvc` or the F-2 validator (test). No runtime dependency. No front-end dependency.

## 10. Field-level behaviour matrix

No business field is read or written (story v7 §11).

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| Operation | `operationId` | API v4 | Reviewed change to the file | Present, unique, valid Java identifier (L1). |
| Operation | `x-module` | API v4 | Reviewed change | A `code` in the TE-001 map (L2). |
| Operation | `x-capability.area`, `.right` | API v4 | Reviewed change | Area in rule set or `None` (only with `R`); right in `C R U D A` (L3). |
| Operation | `x-first-release` | API v4 | Reviewed change | In `E1`–`E6` (L4). |
| Operation | 4xx/5xx responses | API v4 | Reviewed change | ≥ 1; `application/problem+json` + `Problem` (L5, L6). |
| Baseline | `release` | `api/recovery-api-implementation.yaml` | Reviewed change | Equals `rwb.release` for the build. |
| Baseline row | `operationId`, `story`, `enforce` | Plan from story files v7 / Build Sequence v6 | Endpoint story flips `enforce` | L9; `enforce: true` only with a controller in the same MR. |
| Allow-list row | `method`, `path`, `decision`, `owner`, `openItem` | README decision 6 | Reviewed change | No collision with a v4 path (L9). |
| Fixture matrix row | `role`, `area`, `letters`, `source` | Cited story text only | Test change | Replaced by the E1-037 seed. |
| Report row | see SPEC-015 | Build | Generated | No personal data. |
| Build property | `rwb.release` | Gradle, default `E1` | Command line | `E1`–`E6`. |

## 11. Status-transition matrix

No case status changes (story v7 §9). Build and report states:

| From | Event | Condition | To | Side effect |
|---|---|---|---|---|
| Not built | `recoveryApiLint` | Any L1–L7, L9, L10 breach | FAILED | Stops before generation; log names operation and rule. |
| Lint passed | `recoveryApiGenerate` | Generator error | FAILED | — |
| Generated | `compileJava` / `api:verify` / `typecheck` | Compile error, stale types, removed field used | FAILED | Log names file and line. |
| Compiled | Guard / method-security tests | Default method or handler without `@PreAuthorize` | FAILED | Text per SPEC-004 / -005. |
| Compiled | Resolver | Unknown handler, not in baseline, implemented-not-enforced, module mismatch | FAILED | Text per SPEC-001 / -009 / -010. |
| Compiled | Contract run | Mismatch, undocumented status, incomplete Problem | FAILED | Text per SPEC-011. |
| Compiled | Contract run | Enforced, no implementation | FAILED | `{operationId} has no implementation`. |
| Compiled | Contract + access run | Enforced operation passes both | PASSED | Report row. |
| Compiled | Catalog | Not enforced / later release, not implemented | PENDING | Report row with story or release. |
| Compiled | Access run | 2xx to a role without the right | FAILED | `access not enforced for {operationId}`. |
| Suites done | Coverage finalizers | Below 80% | FAILED | JaCoCo message. |
| Any | Any failure | — | FAILED | Merge blocked; report kept as artifact. |

## 12. Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / report | SPEC |
|---|---|---|---|---|
| X1 | Response does not match | Fail | `contract broken: {operationId} at {jsonPath}: {reason}` | 011 |
| X2 | Lint rule broken | Fail before generation | `lint rule broken: {operationId} {rule}` | 002 |
| X3 | Undeclared status (incl. 500) | Fail | `undocumented status {status} for {operationId}` | 011 |
| X4 | Enforced current operation, no controller | Fail | `{operationId} has no implementation` | 009 |
| X5 | Later operation, no controller | Pending; build passes | `pending: {operationId} (first in {release})` | 009 |
| X6 | Front end uses removed field | Type check fails | TypeScript diagnostic with file and line | 006, 021 |
| X7 | 2xx to a role without the right | Fail | `access not enforced for {operationId}` | 012 |
| X8 | Role without the right calls | 403 Problem | `MSG-P4-002` | 012 |
| X-S1 | Handler not in spec, not allow-listed | Fail | `operation not in specification: {METHOD} {path}` | 001 |
| X-S2 | Handler without method check | Fail | `no method-security check: {class}#{method} {METHOD} {path}` | 005 |
| X-S3 | Generated default method | Fail | `generated interface {type} has a default method {method}` | 004 |
| X-S4 | Implemented but not enforced / not in baseline | Fail | `{operationId} is implemented but not enforced` / `operation not in baseline: {operationId}` | 009 |
| X-S5 | Module mismatch | Fail | `module mismatch: {operationId} is {x-module} but implemented in {module}` | 010 |
| X-S6 | Problem without `messageCode` / `traceId` | Fail | `contract broken: {operationId} at $.messageCode: missing` | 011 |
| X-S7 | No role without the right | Fail | `no role without the right for {operationId}` | 012 |
| X-S8 | Stale or hand-edited `schema.d.ts` | `check` fails | `api:verify` output | 006 |
| X-S9 | API file changed without hash update | Lint fails | L10 text | 002 |

Build-log text is for developers and is not part of the message standard (story v7 §14).

## 13. API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Endpoints delivered | None. |
| Contract delta | None to API v4. `postAdminWorkflowsSmoke` keeps its HTTP contract; only its Java signature moves to the generated interface. |
| Backward compatibility | No runtime change for callers; `PlatformE2ETest` smoke cases unchanged. |
| Authorization | No access rule changed. |
| Versioning | API stays v4 / `/api/recovery/v1` (BS-3.7). |

## 14. Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | YES — scripts, one type alias, one test file; no screen | REQUIRED | 80% lines, statements, branches, functions on `src/modules/recovery/**` (existing `vite.config.ts` thresholds; must not drop). The changed `ApiClientContext.tsx` lines are type-only (no executable statement). | SPEC-006, -007, -021; AC1, AC7; BR1, BR5 | `frontend/package.json`, `ApiClientContext.tsx:32-41`; Vitest includes `src/**/*.test.{ts,tsx}` and measures `src/modules/recovery/**` (`vite.config.ts`). No hand-written generator script is added (SG2-01). | Positive: fixture Timer with `warnAt` compiles with 0 diagnostics. Negative: fixture screen reading removed `legalHold` yields a diagnostic naming file and line. Boundary: empty fixture `components.schemas` generates without error. Error: `api:verify` fails on a stale file (S-3 evidence). `typecheck` passes with the generated `Problem` alias. |
| Backend | YES — tooling, tests, retrofit, `traceId` | REQUIRED | 80% LINE, BRANCH, INSTRUCTION (statements), METHOD (functions) on `apiTooling` output and `recovery.contract.support` (`recoveryContractCoverageVerification`); global `recoveryCoverageVerification` (LINE, BRANCH 80%) on the TE-001-approved scope with `**/generated/**` excluded; changed main lines in the retrofit and `ApiExceptionHandler` covered by the suites. | SPEC-001..-005, -008..-021; AC1–AC8; BR1–BR5 | `build.gradle.kts:131-160`; CI runs `test recoveryCoverageReport` only (`.gitlab-ci.yml:15`); D-RCV-43 precedent; `implementation-execution-gates.md`. | Per lint rule L1–L10: one passing and one failing fixture. Catalog: release boundary E1 vs E2, invalid release. Baseline: each of the five outcomes in SPEC-009. Resolver: path-variable normalisation, unknown handler, module mismatch. Contract: AC2, AC4, missing `messageCode`, valid smoke. Access: AC8, 403 pass, area `None` → 401, no-role case. Guard: default-method fixture interface. Method security: handler without and with `@PreAuthorize`, inherited default method. Report: content and absence of bodies. |

Separately required system, contract and access tests (story v7 §16) are not replaced by unit tests. Measured results belong to the Implementation Builder; none is claimed here.

## 15. Test scenarios

Story test cases (story v7 §16; Given/When/Then in Recovery Workbench Test Cases v7, tab Story test cases):

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-TE-003-01 | AC1, BR1, BR5 | System | Fixture spec adds `warnAt` to Timer; live v4 Timer | Server model (fixture and live) and front-end type hold `warnAt`; both compile. |
| TC-TE-003-02 | AC2, BR3 | System | Fixture controller returns `"two"` for `escalationLevel` | Fails; report names `getCasesCaseidTimers` and `$[0].escalationLevel`. |
| TC-TE-003-03 | AC3, BR2 | System | Fixture spec operation without `x-capability` | Lint fails before generation, naming the operation. |
| TC-TE-003-04 | AC4, BR3 | System | Fixture controller returns 400 | `undocumented status 400 for getCasesCaseidTimers`. |
| TC-TE-003-05 | AC5, BR3 | System | Fixture baseline `getAdminJobs enforce: true`, no controller | `getAdminJobs has no implementation`. |
| TC-TE-003-06 | AC6 | System | Live E1 build; `postQueuesQueueidPlacements` E2, no controller | Build passes; report lists it `PENDING`. |
| TC-TE-003-07 | AC7, BR1 | System | Fixture spec without `legalHold`; fixture screen reads it | Type check fails naming file and line. |
| TC-TE-003-08 | AC8, BR4 | System | Fixture controller without check; JWT role `RW-REFADM` | 200 → `access not enforced for getCasesCaseidTimers`. |
| TC-TE-003-09 | Access | Access | Live `RW-REFADM` calls `getCasesCaseidTimers` | **BLOCKED** until RWB-E1-022 / RWB-E1-037 and the operation's own story (OPEN-040); never recorded as passed from a fixture. |

Specification tests added by this spec:

| ID | SPEC | Level | Expected |
|---|---|---|---|
| T-TE003-10 | 001 | Unit (resolver) | Fixture handler `GET /unknown` → `operation not in specification: GET /unknown`. |
| T-TE003-11 | 001 | Contract context | Live: `/platform/info`, `/admin/temporal/health` reported `OUTSIDE_SPECIFICATION`; nothing else unknown. |
| T-TE003-12 | 005 | Unit (fixture classes) | Handler without `@PreAuthorize`, and controller inheriting a default interface handler → fail with SPEC-005 text. |
| T-TE003-13 | 005 | Unit (main classes) | Live: all three baseline handlers pass. |
| T-TE003-14 | 002 | Unit | One failing fixture per L1–L7, L9, L10; L8 warns only; live v4 passes. |
| T-TE003-15 | 003, 004 | Unit | Live generated web package: one method per interface, no default method; fixture interface with a default method fails. |
| T-TE003-16 | 006, 019 | Script (S-3) | `api:verify` passes on the committed file; fails after a one-character hand edit. |
| T-TE003-17 | 007 | Typecheck | `npm run typecheck` passes; no `interface Problem` left in `ApiClientContext.tsx`. |
| T-TE003-18 | 008 | Unit | `E1` selects 73; `E2` selects 111; unknown release rejected. |
| T-TE003-19 | 009 | Unit | Implemented with `enforce: false` → fail; implemented with no row → fail. |
| T-TE003-20 | 009 | Unit | Live baseline: 73 E1 rows; only `postAdminWorkflowsSmoke` enforced. |
| T-TE003-21 | 010 | Unit | `{caseId}` vs `{id}` match; fixture controller in the wrong module → `module mismatch`. |
| T-TE003-22 | 011 | Contract | Live `postAdminWorkflowsSmoke` 202 passes with stubbed `WorkflowClient`. |
| T-TE003-23 | 011 | Contract fixture | Fixture 403 body without `messageCode` → `contract broken … $.messageCode: missing`; fixture 500 → `undocumented status 500`. |
| T-TE003-24 | 012 | Access | Live smoke as `RW-CASEOWN` (fixture matrix) → 403, `application/problem+json`, `MSG-P4-002`, `roleSource: FIXTURE`. |
| T-TE003-25 | 012 | Access fixture | Area `None` fixture operation without token → 401 `MSG-P4-001`, `NOT_APPLICABLE_AUTHENTICATED`; enforced operation with no fixture role → `no role without the right`. |
| T-TE003-26 | 013 | Contract (S-4) | 500 body carries `traceId`; 401/403/503 bodies carry `traceId`. |
| T-TE003-27 | 014 | Contract + E2E | Smoke retrofitted: 202, 503 on `UNAVAILABLE`, duplicate ID returns same ID; `PlatformE2ETest` unchanged and green (API Tester stage). |
| T-TE003-28 | 015 | Unit | Report has 141 + 2 rows, totals, SHA-256; no body, token or timestamp. |
| T-TE003-29 | 016 | Build evidence | `./gradlew test` log shows lint → generate → compile → suites; `npm run check` log shows `api:verify` first. |
| T-TE003-30 | 017 | Build evidence | Both verification tasks run as finalizers of `test`; a drop below 80% fails `test`. |
| T-TE003-31 | 018 | Unit | `ModulithTest`, TE-001 module-map rule, `RecoveryBoundaryTest` green with generated packages and retrofit. |
| T-TE003-32 | 019 | Unit / build | Two generations from one commit are byte-identical (server and report). |
| T-TE003-33 | 020 | Unit | Fixture files scanned: no value matching the TE-011 personal-data patterns once available; until then a reviewer check recorded in the plan. |

## 16. Guardrails and out of scope

Guardrails (story v7 §17): no business value in code; no personal data in logs, tests or prompts, and the report holds operation names only; no read of another module's tables, and each module's controller implements its own generated interface; generated code is never edited.

Out of scope:

- Contract tests for file interfaces: RWB-E1-007 (story v7 §19).
- Browser tests on the screens that use the generated client: RWB-TE-010 (story v7 §19).
- The permission matrix content: RWB-E1-037 (story v7 §19).
- Capability-named method checks and the per-language `{action}` value: RWB-E1-022 (§3.1).
- 400/422 validation mapping, 500 message ID, dependency scan, ZAP baseline, expired-session UI state (A-15): §3.1 owners and open items.
- ESLint fixture test for D-RCV-39: RWB-TE-001 (D-RCV-40).
- Any endpoint, entity, migration or screen as a business deliverable.

## 17. Clarification Log

No question was asked (L-RCV-03; AGENTS §10.6). Every item is settled by a cited source, a decision or a labelled assumption in `assumptions.md`.

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | Story §4 step 5, AC5, §13 Done when | Strict current-release failure vs "pending with a named story". | Versioned baseline needed. | L-RCV-11, premise restated: one E1 operation already implemented (§4). OPEN-039. | RESOLVED | 009 |
| CLAR-002 | Story §2 | 79 vs 141 operations. | No coded count. | Read the file; select by `rwb.release`. OPEN-039. | RESOLVED | 008 |
| CLAR-003 | Story §3, §12, §13; L-RCV-14 | Where the generated packages live. | Module boundary. | `<P2>.generated.web` / `.model`, `<P2>` from the merged TE-001 map (PRE-2); no `integration` assumed. | RESOLVED | 003, 018 |
| CLAR-004 | Story §13 | Source of the named story for pending operations. | Report. | Baseline rows. | RESOLVED | 009 |
| CLAR-005 | Story §2 | AC-P2-001-01 is the file-interface contract test. | Traceability. | Not claimed (TE003-SG-DG-07). | RESOLVED | 011 |
| CLAR-006 | Story §16 TC-TE-003-09 | Live access needs E1-022/E1-037. | Live case. | BLOCKED; OPEN-040. | RESOLVED | 012 |
| CLAR-007 | Story §13; AGENTS §4.4 | Dependencies. | Plan approval. | Front end: none new. Back end: generator plugin and validator, pinned at plan gate; spikes S-1..S-4. | RESOLVED | 003, 011 |
| CLAR-008 | BR4; AC8 | `area: None` operations. | Access suite. | Authentication-only, 401 test; OPEN-042; E1-022 v7 §12 (`GET /me/session` "no capability area"). | RESOLVED | 012 |
| CLAR-009 | Story §12 "one interface per tag" vs §17 | Interface grouping. | Reachable unbuilt operations. | One interface per operation, abstract only (§7.1). | RESOLVED | 003, 004, 005 |
| CLAR-010 | Story §12 front-end path | Second type set vs `@/api/schema`. | Duplication (FS-4.2). | Extend `api:generate`; drift check (TE003-SG-DG-01). | RESOLVED | 006, 007 |
| CLAR-011 | Story §12 "Spring Boot 3" | Boot line. | Generator target. | Boot 4.1.2 / Jackson 3; spike S-1 (TE003-SG-DG-03). | RESOLVED | 003 |
| CLAR-012 | Audit A-03, A-08, A-09, A-11, A-15 | Ownership. | Scope. | §3.1 dispositions. | RESOLVED | 005, 011, 013, 016, 017, 007 |
| CLAR-013 | README decision 6 | Handlers outside the spec. | BR1. | Allow-list with owner and open item. | RESOLVED | 001 |

`CLARIFICATION_STATUS: NOT_REQUIRED` for the BA (no open question); all 13 items resolved by source, decision or assumption.

## 18. Status reporting

```text
MCP_STATUS_SUMMARY: No Figma or design source applies to this API-tooling story; no MCP connected (RUN-BRIEF rule 5).
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: Lint API v4, generate per-operation server interfaces and verify the existing front-end types, add contract, access and method-security suites in the existing test task; no endpoint, screen or schema change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NO_API_CHANGE] [REASON: build-time API contract tooling over the existing v4 file and baseline code]
REQUIREMENT_COVERAGE_SUMMARY: 5 BRs, 8 ACs, 8 flow steps, 8 exception paths, §12, §13 step 2, 4 guardrails and §19 mapped in 36 rows; 6 audit items dispositioned.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 36] [COVERED_RULES: 36] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: NOT_REQUIRED [OPEN_ITEMS: 0]
NEXT_STEP: Compliance Reviewer spec gate review-2; Implementation Planner only after PASS and after RWB-TE-001 is merged (PRE-1).
```

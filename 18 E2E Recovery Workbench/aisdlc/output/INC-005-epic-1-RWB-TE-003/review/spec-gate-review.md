# Spec gate review: RWB-TE-003, types and contract tests from the API specification

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-003-SG2` (fresh spec gate under D-RUN-05; supersedes `REVIEW-RWB-TE-003-SPEC-001` for this repository) |
| RUN_ID | `INC-005-epic-1-RWB-TE-003` |
| Artifact | `aisdlc/output/INC-005-epic-1-RWB-TE-003/_v2-baseline/specify/` (`spec.md`, `api-audit.md`, `compliance-validation.md`, `assumptions.md`, `contracts/*.json`) |
| Reviewer | Compliance Reviewer (spec gate) |
| Date | 2026-11-17 |
| **Status** | **FAIL** |
| Findings | 2 High, 7 Medium, 3 Low (12 in all) |
| Handoff | **Blocked.** High and Medium findings block the Implementation Planner until the spec is fixed and re-reviewed (`aisdlc/.github/rules/pdlc.md`, Human Checkpoints). |

## 1. What was checked

- **Baseline documents.** I checked the spec against these sources:
  - the increment card `aisdlc/docs/increments/INC-005-epic-1-RWB-TE-003.md`;
  - the story file v7 `rwb-te-003-types-and-contract-tests-from-the-api-specification-v1.md`, sections 1 to 19;
  - Story Defects v4, the RWB-TE-003 rows;
  - ADR v3, ADR-006;
  - Decision Log v10, DL07;
  - D-RCV-35 and D-RCV-36, and D-RCV-05, -06, -37, -39, -40, -43 and -44 in `aisdlc/docs/decisions/`;
  - Error and Message Standard v4, sections 2 to 4;
  - FSD P2 v3 (set v6), AC-P2-001-01;
  - the contexts `backend-standards.md`, `frontend-standards.md`, `frontend-context.md` and `testing-standards.md`.
- **API Specification v4.** `api/recovery-api-v4.yaml` is byte-identical to the document set's `05-technical-architecture/recovery-workbench-api-specification-v4.yaml`: both have SHA-256 `535cb46594190f0bf535a2ad3f034e9f50f987a92fe19c0524a2755f5923b891`.
- **`api-audit.md` counts.** I re-derived every count with a YAML parse of the file, and every count is correct:
  - 141 operations, with no duplicate `operationId`;
  - by release: 73 E1, 38 E2, 8 E3, 10 E4, 8 E5 and 4 E6;
  - 16 tags, 172 schemas and 903 `$ref` values;
  - 0 inline error responses;
  - 2 operations with `area: None`: `getFeatureFlags` and `getMeSession`;
  - `warnAt` is in `Timer` at line 6602, and `legalHold` is in `Case`;
  - `getCasesCaseidTimers` declares 200, 401, 403, 404 and 503, which matches AC4.
- **This repository at `c22ee73`.** I read these files:
  - `backend/build.gradle.kts`, `SecurityConfig`, `ApiExceptionHandler`, `ProblemFactory`, `ApiError`, `PlatformInfoController`, `TemporalAdminController` and `RecoveryBoundaryTest`;
  - `frontend/package.json`, `eslint.config.js`, `vite.config.ts`, `src/api/schema.d.ts`, `src/contexts/ApiClientContext.tsx`, `src/modules/recovery/api/platform.ts` and `QueryState.tsx`;
  - `.gitlab-ci.yml`, `README.md` and `aisdlc/evidence/phase0-standards-audit.md`.
- **Generated types.** I regenerated `schema.d.ts` with the repository's own `openapi-typescript` 7.13.0. The output is identical to the committed file, so the baseline generation is current and deterministic.

**What is correct.** The spec reads the requirements correctly:
- The story intent is right, and all of AC1–AC8, BR1–BR5, flow steps 1–8 and X1–X8 are mapped.
- The pending baseline (`L-RCV-11`) handles the story's own contradiction between step 5/AC5 and §13: Story Defects v4 records this as the RWB-TE-003 step 8 row, "Open".
- The release selection reads the file and does not rely on a fixed count.
- The handling of `area: None` is sound.
- The live access case `TC-TE-003-09` is kept `BLOCKED`, not passed.
- Fixtures are synthetic and contain no personal data.

The failures are elsewhere: the spec designs against the ACE monorepo, not against the code in this repository. It also neither covers nor excludes five phase-0 findings that are assigned to this story.

## 2. Findings

### REVIEW-RWB-TE-003-SG2-01: High. The front-end generation duplicates the baseline types and typed client

**Affects:** SPEC-004 and SPEC-013; AC1 and AC7; BR1 and BR5; `contracts/frontend-integrations.json`.

**Evidence**
- The spec has the generator write a second `schema.d.ts` and a new `client.ts` into `frontend/src/modules/recovery/api/generated/`. It does this through a new wrapper, `frontend/scripts/recovery-api/`, and gitignores the output. See spec "Packages and boundaries" and "Generation"; also CLAR-007, which says to "pin" `openapi-typescript`/`openapi-fetch`.
- This repository already has both of these things (audit A-04):
  - `frontend/package.json` `api:generate` runs `openapi-typescript ../api/recovery-api-v4.yaml -o src/api/schema.d.ts`. The output is committed and current, as I verified by regenerating it.
  - `frontend/src/contexts/ApiClientContext.tsx:1-3,69` builds the typed `openapi-fetch` client `Client<paths>` from `@/api/schema`.
  - Both tools are already pinned: `openapi-typescript` 7.13.0 and `openapi-fetch` 0.17.0.
- `frontend-standards.md` FS-4.2 says "Use generated types from `@/api/schema`; no duplicate hand-written type". `frontend-context.md` (API client row) and D-RCV-39 name `@/api/schema` as the shared entry point.
- `RUN-BRIEF.md` says: "extend or correct it, never duplicate it".
- With two type sets, AC7 only proves drift for whichever file a screen happens to import.

**Required fix**
- Specify one generated type set and one typed client.
- Either:
  - extend `api:generate`, `src/api/schema.d.ts` and `ApiClientContext`; or
  - move them deliberately and update `ApiClientContext`, the D-RCV-39 allow-list and the ESLint ignore together.
- Record the deviation from the story v7 §12 path as a document gap. This review records it as TE003-SG-DG-01.
- Make generation, or a regenerate-and-diff drift check, run before `typecheck` in `npm run check`. Today `check` does not regenerate, so a changed YAML file would not reach the type check.
- Drop the "new dependency" items for tools that are already pinned.

### REVIEW-RWB-TE-003-SG2-02: High. "One interface per tag" breaks the module guardrail and exposes operations that are not implemented

**Affects:** SPEC-003 and SPEC-011; BR5; story §17; AGENTS §3.11.

**Evidence**
- The spec configures `useTags=true`, "one interface per tag", and `interfaceOnly=true` (spec "Generation"). The guardrail says "each module's controller implements its own generated interface" (spec "Guardrails"; story v7 §17).
- In API Specification v4, tags cross `x-module`:
  - `Administration` spans P1, P2, P3, P4, P6 and P10;
  - `Cases` spans P1, P2, P3, P10 and S8;
  - `Treatment` spans P2, P6, S1, S2 and S3.
- So the existing P3 handler `postAdminWorkflowsSmoke` (`TemporalAdminController.java:89-91`) could only implement an `AdministrationApi` that also carries P1, P2, P4, P6 and P10 operations.
- The spec does not set the generator's behaviour for operations that are not implemented. With the generator's default (`skipDefaultInterface=false`), every unimplemented method in the interface becomes a live default handler that returns 501. That status is undocumented, and the handler has no method check.
- `ImplementedOperationResolver` matches methods "whose names match operationIds". It would therefore treat every default method as implemented.

**Required fix**
- Specify an interface grouping that keeps each interface inside one `x-module`. For example, re-tag by `x-module` or split by module and tag before generation. Story v7 §6 lets the squad negotiate this: "Generator settings are build configuration".
- Specify how operations that are not implemented behave: either no default handlers, or the generator's `skipDefaultInterface`.
- Specify that the resolver counts only methods the controller overrides or maps, not default interface methods.
- Record the conflict between story §12 and §17 as TE003-SG-DG-02.

### REVIEW-RWB-TE-003-SG2-03: Medium. The premise "no controller exists" is false here, so the existing handlers fall outside the suite

**Affects:** SPEC-005, -006, -007 and -009; `L-RCV-11`; story §13 build step 2.

**Evidence**
- The spec, `L-RCV-11` and CLAR-001 all say that at build order 5 "no controller exists" and that "the enforced set is empty".
- In this repository the E1 operation `postAdminWorkflowsSmoke` is already implemented by hand (`TemporalAdminController.java:89-108`), with no generated interface. The controller is registered only when `rwb.p3.temporal=true` (line 44).
- Two further handlers are under `/api/recovery/v1` but are not in the specification: `GET /platform/info` (`PlatformInfoController.java:30`) and `GET /admin/temporal/health` (`TemporalAdminController.java:65`). README decision 6 records them as local operational endpoints.
- The spec's resolver discovers only controllers that implement generated interfaces. It would not see any of these three handlers, so the "operation not in baseline" rule could not fire on them.
- BR1, "only source of endpoints", has no stated exception for the two endpoints in README decision 6.
- The spec also drops story §13 build step 2, "make one existing controller implement its generated interface (AC1)".

**Required fix**
- Restate the baseline for this repository. `postAdminWorkflowsSmoke` gets a baseline row with its owning story, and the spec decides whether TE-003 retrofits it onto its generated interface and enforces it (story §13 step 2), or leaves it pending with a named owner.
- Resolve implemented operations from the MVC handler mappings (method and path), not only from interface inheritance, so that hand-written handlers are caught.
- Add a reviewed allow-list for the README decision 6 endpoints, citing the decision and naming an owner. BR1 then holds for everything else.
- State that the contract and access runs set `rwb.p3.temporal` on, so the conditional controller is present.

### REVIEW-RWB-TE-003-SG2-04: Medium. Audit A-03 is neither covered nor excluded

**Affects:** SPEC-008; BR4; AC8; BS-3.2; AGENTS §3.3.

**Evidence**
- A-03, which the audit assigns to this story, says:
  - method checks name roles or `isAuthenticated()`, not the `x-capability`;
  - role literals are in code;
  - "No test proves that every endpoint has a method check".
- The current method checks are:
  - `PlatformInfoController.java:31` `@PreAuthorize("isAuthenticated()")`;
  - `TemporalAdminController.java:66` `hasAnyAuthority('RW-PLATADM', 'RW-AUDIT')`;
  - `TemporalAdminController.java:91` `hasAuthority('RW-PLATADM')`.
- The spec's access suite tests only operations that are enforced and resolved. At TE-003 that is none (spec "Performance"). The spec has no check that every handler under `/api/recovery/**` carries a method-security check, and it does not mention role literals.

**Required fix**
- Add a check over all request-mapping handlers in `th.co.scb.ace.demo.recovery` that fails when a handler has no method-security check. This includes handlers outside the specification and handlers that are still pending.
- State plainly that replacing role literals with a capability-area-and-right check depends on RWB-E1-022 and RWB-E1-037, and is excluded from this story with those owners. Alternatively, define the capability-naming check now.

### REVIEW-RWB-TE-003-SG2-05: Medium. Audit A-08 (gaps in the Problem body) is neither covered nor excluded

**Affects:** SPEC-007 and SPEC-008; BR2 and BR4; X8.

**Evidence**
- `ApiExceptionHandler.java:49-56` catches every `Exception`, including Spring's validation and binding exceptions. It returns a 500 `ProblemDetail` with no `messageCode` and no `traceId`. As a result:
  - there is no 400 or 422 mapping, and `field` is never set;
  - no operation in API Specification v4 declares a 500;
  - E400 is declared on 4 operations, and E422 on 64 operations (25 of them E1).
- `ApiExceptionHandler.java:41` and `SecurityConfig.java:76` fill MSG-P4-002 `{action}` with the English text "do this", including in `messageTh`. Error and Message Standard v4 §2 and §3 require English and Thai to carry the same placeholders, each "formatted for the language".
- The v4 `Problem` schema has no `required` list. Schema validation alone therefore cannot detect a Problem body that lacks `messageCode` or `traceId`.
- The spec does not mention any of these points.

**Required fix**
- Either cover A-08, or exclude it with an owner and an open item. Covering it means:
  - the contract and access suites assert that `messageCode` and `traceId` are not null on every 4xx and 5xx body;
  - request-validation failures map to the status the operation declares (400 or 422), with `field` and the MSG-GEN message;
  - `{action}` is filled per language.
- Record the missing message ID for a 500 as TE003-SG-DG-04.

### REVIEW-RWB-TE-003-SG2-06: Medium. Audit A-09: the CI and coverage wiring does not fit this repository

**Affects:** the Build integration table; Unit Test Applicability; D-RCV-05, -40 and -43.

**Evidence**
- The spec says the tasks "join the existing Gradle/frontend `check`" and run in "`test` / `check`".
- This repository's CI does not run `check`:
  - the `backend-unit` job runs `./gradlew test recoveryCoverageReport` (`.gitlab-ci.yml:15`);
  - the frontend job runs `npm run check`, which does no generation (finding 01).
- `recoveryCoverageVerification` is "not yet part of `check`" (`README.md:86-87`; `build.gradle.kts:148-160`), and no job runs it.
- The 80% backend gate in the spec targets `th.co.scb.ace.demo.recovery.contract` in `src/test` and the "lint task classes". `recoveryClasses` (`build.gradle.kts:131-133`) measures only main output. D-RCV-43 is the precedent for measuring test-scope tooling.
- A-09, which the audit assigns to this story, is "contract and coverage jobs missing".

**Required fix**
- Specify where each suite runs so that the existing CI job runs it. Examples: inside `test`, or as a `test` dependency or finalizer.
- Specify how `recoveryCoverageVerification` becomes a gate. Either wire it in Gradle, which is compatible with D-RCV-05, or record a decision to change the pipeline file.
- Specify how coverage of the test-scope and build-logic tooling is measured.
- State which parts of A-09 TE-011 owns.

### REVIEW-RWB-TE-003-SG2-07: Medium. The spec assumes RWB-TE-001 artefacts that do not exist in this repository

**Affects:** SPEC-003 and SPEC-011; `L-RCV-14`; Preconditions.

**Evidence**
- The spec says:
  - "`ModuleMapLoader` already validates a list of published sub-packages";
  - the boundary rule "already allows" a dependency on a published package;
  - generated code goes into `recovery.integration.generated.*`.
- In this repository:
  - `backend/src/test/resources/architecture/` is empty;
  - there is no `ModuleMapLoader`;
  - the nested modules are `platform`, `rules`, `workflow` and `documents`, and there is no `integration` (audit A-01 and A-02, owned by RWB-TE-001);
  - `RecoveryBoundaryTest` is the local subset.
- RWB-TE-001 here is only at its fresh spec gate, as INC-002 `_v2-baseline`.

**Required fix**
- Make "RWB-TE-001 merged in this repository" an explicit precondition.
- Name the generated package as the package that this repository's RWB-TE-001 map publishes for P2, and do not assume `recovery.integration`.
- State what TE-003 adds to the map, and that `ModulithTest.verify()` must still pass.

### REVIEW-RWB-TE-003-SG2-08: Medium. Audit A-11 is neither covered nor excluded

**Affects:** SPEC-004; FS-4.2; D-RCV-40.

**Evidence**
- `ApiClientContext.tsx:32-41` writes `interface Problem` by hand. That type duplicates the generated `components["schemas"]["Problem"]`.
- `platform.ts:8-21` writes `PlatformInfo` and `TemporalHealth` by hand. These belong to endpoints outside the specification (README decision 6), so they cannot be generated yet.
- There is no ESLint fixture test proving that the D-RCV-39 rule fires. D-RCV-40 assigns the "ESLint Node-API fixture test" to RWB-TE-001.
- The spec mentions none of this.

**Required fix**
- Replace the hand-written `Problem` with the generated type.
- Record the two operational types as a legitimate exception under README decision 6, with an open item to add those endpoints to the API specification.
- State that the ESLint fixture test belongs to RWB-TE-001 (D-RCV-40), or adopt it here.

### REVIEW-RWB-TE-003-SG2-09: Medium. The SPEC IDs are referenced but never defined, and the matrix has no SPEC rows

**Affects:** traceability (traceability-standards; specification-execution-gates, Final Validation 2 and 3).

**Evidence**
- The coverage table maps rows to `SPEC-RWB-TE-003-001..-013`, but `spec.md` has no table that defines those IDs (grep finds references only).
- The v2 `compliance-validation.md` says "each defined once", which is not true.
- `aisdlc/requirement/Traceability_Matrix.md:53` lists the story but no `SPEC-RWB-TE-003-*` IDs.

**Required fix**
- Add a SPEC table: ID, statement, `FR-RWB-013`/REQ link, and AC/TC link.
- Write the matrix rows to `specify/shared-updates.md` for the orchestrator.

### REVIEW-RWB-TE-003-SG2-10: Low. The generator and validator targets do not match the repository's stack

**Affects:** SPEC-002, -003 and -007; CLAR-007; `ASM-TE003-08`.

**Evidence**
- The spec fixes `useSpringBoot3=true`, following story v7 §12, "Spring Boot 3".
- This repository runs:
  - Spring Boot 4.1.2 (`build.gradle.kts:9`; README decision 2);
  - Jackson 3, as `tools.jackson.databind` (`ProblemFactory.java:14`);
  - an OpenAPI 3.1.0 file.
- The spec does not require proof that the generated code and `swagger-request-validator-mockmvc` work on this stack.

**Required fix**
- Set the target to the repository's Boot and Jackson line.
- Require a compile and validation spike at the plan gate, with a named fallback.
- This review records the conflict with story §12 as TE003-SG-DG-03.

### REVIEW-RWB-TE-003-SG2-11: Low. Audit A-15 (no 401 state) is not explicitly excluded

**Affects:** Out of scope.

**Evidence**
- `QueryState.tsx:34-43` handles 403 but has no 401 or expired-session state (FS-3.1; frontend-context, "Session expired").
- Story v7 §15 says "No screen" and the spec says UI In Scope = NO, so excluding A-15 is legitimate. However, the spec does not say so.

**Required fix**
- Add A-15 to Out of scope, with hardening (or the first screen story) as the owner.

### REVIEW-RWB-TE-003-SG2-12: Low. The spec carries a stale gate status and contradicts itself on package-info files

**Affects:** spec header; "Components".

**Evidence**
- The header says "`SUCCESS` — spec gate PASS; 0 Critical/High/Medium" and names `REVIEW-RWB-TE-003-SPEC-001` as its approval. That gate result came from the 17 v2 workspace.
- "Components" has the front-end wrapper write "the `package-info.java` files", while "Packages and boundaries" has the server generator write them.

**Required fix**
- Reset the status to pending this gate, and name this review.
- Make the server-side build the only writer of `package-info.java`.

## 3. Phase-0 audit items assigned to this story

| Item | Covered by the spec? | Verdict |
|---|---|---|
| A-03 | No. The access suite covers only enforced operations, and there is no all-handlers method-check test | Not covered: SG2-04 |
| A-04 (`api:generate`, `schema.d.ts`) | No. The spec builds a second generator, types and client | Duplicated: SG2-01 |
| A-08 | No | Not covered: SG2-05 |
| A-09 | Partly. The spec says no pipeline change, but the suites do not reach the CI job, and coverage verification is not wired | Not covered: SG2-06 |
| A-11 | No | Not covered: SG2-08 |
| A-15 | No. The spec does not say it is excluded | Legitimately excludable: SG2-11 |

## 4. Plan inputs (ACE monorepo paths are not findings)

1. **API file.** The specification file is `api/recovery-api-v4.yaml`, not `api/recovery-api.yaml`. `api:generate` reads it.
   - It is byte-identical to document-set v4, which satisfies `ASM-TE003-01`.
   - Rename it only together with `api:generate`.
   - The byte-equality check can compare against the SHA-256 recorded in this review.
2. **Build and generated output.**
   - The backend build is `backend/build.gradle.kts`, not `ace-service`.
   - The frontend has no Nx. `frontend/package.json` `check` = typecheck + lint + coverage.
   - The ESLint config ignores `src/api/schema.d.ts`.
3. **Packages.** The root package is `th.co.scb.ace.demo.recovery`, and the tests go in `th.co.scb.ace.demo.recovery.contract`.
4. **Test database.** There is no in-memory database. Testcontainers PG runs under `recovery-it`, outside `check` (D-RCV-44). The contract fixtures should stub module APIs or use MockMvc slices; the plan picks one and says why.
5. **Authentication.** The local API is a stateless Entra bearer JWT; "without a session" means no token.
   - The local mock personas (`README.md`) have no `RW-REFADM` persona.
   - The AC8 fixture should use test JWTs from `spring-security-test`.
6. **Vitest scope.** Vitest runs only `src/**/*.test.{ts,tsx}` and measures coverage on `src/modules/recovery/**`. A script outside `src/` is neither tested nor measured unless the plan changes that, and it should not need to if SG2-01 reuses `api:generate`.
7. **Temporal-dependent controllers.** `TemporalAdminController` needs `rwb.p3.temporal=true` and Temporal stubs in the contract context.
8. **Carried items.** `OPEN-039` to `OPEN-042` exist in `aisdlc/docs/open-items.md` and carry forward. The `L-RCV-11` premise has to be restated (SG2-03).

## 5. Gate result

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 2] [MEDIUM: 7] [LOW: 3]
BLOCKING: YES — SG2-01..SG2-09 must be fixed in a re-issued spec (written to output/INC-005-epic-1-RWB-TE-003/specify/) and re-reviewed (spec-gate-review-2.md).
DOCUMENT_GAPS: 8 recorded in review/document-gaps.md, 0 blockers.
NEXT_STEP: Technical Specifier re-issues the spec against this repository; then re-run this gate. Do not start the Implementation Planner.
```

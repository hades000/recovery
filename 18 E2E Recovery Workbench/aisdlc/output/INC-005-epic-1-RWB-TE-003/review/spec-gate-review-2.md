# Spec gate review 2: RWB-TE-003, types and contract tests from the API specification

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-003-SG3` (spec gate round 2; follows `REVIEW-RWB-TE-003-SG2` in `spec-gate-review.md`) |
| RUN_ID | `INC-005-epic-1-RWB-TE-003` |
| Artifact | `aisdlc/output/INC-005-epic-1-RWB-TE-003/specify/` (remediation 1): `spec.md`, `gate-response.md`, `assumptions.md`, `document-gaps.md`, `shared-updates.md`, `compliance-validation.md`, `agent-run-log.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json` |
| Reviewer | Compliance Reviewer (spec gate) |
| Date | 2026-11-17 |
| **Status** | **FAIL** |
| Findings | 0 Critical, 0 High, 1 Medium, 5 Low (6 in all) |
| Handoff | **Blocked** by the Medium finding SG3-01 (`aisdlc/.github/rules/pdlc.md`). The fix is narrow (SPEC-017, §14, one decision request, one gap row). Low findings are carried for human disposition. |

## 1. What was checked

- **Instructions.** `.claude/agents/compliance-reviewer.md`, adapted by `aisdlc/RUN-BRIEF.md`; `pdlc.md`, `specification-execution-gates.md`, `implementation-execution-gates.md` (IEG), `traceability-standards.md`; contexts `backend-standards.md` (BS), `frontend-standards.md` (FS), `testing-standards.md`.
- **Earlier round.** `review/spec-gate-review.md` (SG2-01..12, plan inputs 1-8), `review/document-gaps.md`.
- **Audit.** `aisdlc/evidence/phase0-standards-audit.md`, items A-03, A-04, A-08, A-09, A-11, A-15.
- **Decisions.** `aisdlc/docs/decisions/decision-register.md` and `INC-001-decisions.md` (D-RCV-05, -06, -28, -39, -40, -43, -44; L-RCV-11, L-RCV-14); `AI-SDLC-BUILD-LOG.md` D-RUN-01..08; `README.md` "Decisions taken while setting this up".
- **Dependency spec.** `aisdlc/output/INC-002-epic-1-RWB-TE-001/specify/` now exists (TE-001 spec revision v3, written 17 Nov 2026 after the TE-003 remediation checked for it): `spec.md` (field matrix, SPEC-004 (g), -020, -022, -023, -024, relocation table), `shared-updates.md` (SU-09, SU-10).
- **Story sources (read only, document set v14).** Story file v7 RWB-TE-003 v1 (§6, §11, §12, §13, §16); RWB-E1-071 v1 (§4 step 9, X6, TC-E1-071-08); RWB-E1-022 v1 (AC2, §12 Authorization row, §13 `AccessCheckInterceptor`).
- **API Specification v4.** `api/recovery-api-v4.yaml` parsed with PyYAML. SHA-256 `535cb465…b891` re-computed: matches the spec and the SG2 review. Confirmed: OpenAPI 3.1.0, server `/api/recovery/v1`; 141 operations, 73 E1, 111 at E1+E2; 14 capability areas plus `None` (2 operations); rights used R, U, C, A; 16 tags, 33 tag-module pairs; no two operations share a normalised method and path; every operationId is a valid Java identifier; `Problem` has no `required` list; `Timer` holds `warnAt` (line 6602) and `escalationLevel`; `Case` holds `legalHold`; 400 on 4 operations, 422 on 64, no 500. `postAdminWorkflowsSmoke` is POST `/admin/workflows/smoke`, P3, Platform administration C, E1, statuses 202 (inline schema `workflowId`, `workflowType`), 401, 403, 404, 503. `getCasesCaseidTimers` 200, 401, 403, 404, 503; `getAdminJobs` P1; `postQueuesQueueidPlacements` E2. No path for `/platform/info` or `/admin/temporal/health`.
- **Repository code.** `backend/build.gradle.kts`; `SecurityConfig`, `ApiExceptionHandler`, `ProblemFactory`, `ApiError`, `PlatformInfoController`, `TemporalAdminController`, all `package-info.java`; `.gitlab-ci.yml`; `.gitattributes`; `scripts/dev.ps1` (`test` = `gradlew test` + `npm run check`); `frontend/package.json`, `eslint.config.js`, `vite.config.ts`, `tsconfig.json`, `src/contexts/ApiClientContext.tsx`, `src/api/schema.d.ts` (`Problem` all-optional).
- **External reference (no project data sent).** OpenAPI Generator documentation, `openapi-generator.tech/docs/generators/spring` and `/docs/customization` (read 17 Nov 2026), for the generator options and normalizer rules the spec relies on.

## 2. Orchestrator constraints

| Constraint | Verdict | Evidence |
|---|---|---|
| SG2-01: extend `api:generate` → `src/api/schema.d.ts`, `@/api/schema`, `ApiClientContext`; no second type set or client | **Met** | SPEC-006, -007; `contracts/frontend-integrations.json` `new_dependencies: []`. `api:generate` and both tools are already pinned (`package.json`). ESLint D-RCV-39 regex allows bare package imports (`typescript`, `openapi-typescript`) in the new Vitest file. `ApiError` takes `Partial<Problem>`, so the generated all-optional `Problem` keeps it type-correct. |
| SG2-02: no operation reachable without a Spring Security method check, including a generated default handler; approach justified with a cited source | **Met** (citation detail is Low SG3-03) | §7.1 compares four options against the constraint, citing story v7 §6 ("Generator settings are build configuration"), the API v4 tag/module parse (re-derived: 16 tags, 33 pairs) and AGENTS §3.3. SPEC-003 (b) forbids default methods; SPEC-004 proves it; SPEC-005 fails any handler (generated, inherited default, hand-written, conditional) without `@PreAuthorize`; SPEC-009 fails an implemented operation that is not enforced, so every reachable operation reaches the access suite. `SET_TAGS_TO_OPERATIONID` exists in the generator's normalizer documentation, which supports ASM-TE003-05. |
| SG2-07: TE-001 owns the module map; referenced as a dependency; no `integration` module assumed | **Met** (staleness is Low SG3-02) | PRE-1, PRE-2, SPEC-018, ASM-TE003-06 use `<P2>` from the merged map. TE-001 v3 now names P2 `integration` with `published [api, flags.api]` and tells TE-003 to use `integration.generated.web` / `.model` (TE-001 SPEC-004 (g), SU-09), which agrees with the spec. |
| A-03, A-08, A-09, A-11, A-15: in scope with ACs and tests, or excluded with cited reason and owner | **Met**, except the A-09 coverage part (Medium SG3-01) | Spec §3.1. A-03 in: SPEC-005, T-TE003-12/-13; out: capability naming to RWB-E1-022 (E1-022 v7 §13 `AccessCheckInterceptor`, verified) and RWB-E1-037. A-08 in: SPEC-011, -013; out: 500 message ID (OPEN-044 proposed), 400/422 mapping (OPEN-045), `{action}` per language to RWB-E1-022 (E1-022 v7 AC2 "read roles", verified). A-09 contract part in: SPEC-016; PDPA lint to TE-011; Playwright/axe to TE-010; dependency scan and ZAP to hardening (testing-standards §1 Security row, verified; OPEN-046). A-11 in: SPEC-007; operational types excepted (README decision 6, OPEN-043); ESLint fixture test to TE-001 (TE-001 v3 SPEC-015 builds it). A-15 out: OPEN-047. |
| SG2-10: Spring Boot 4.1.2 and Jackson 3 | **Met as the required target** (candidate settings are Low SG3-03) | SPEC-003 (d), §9 S-1, F-1a/F-1b; `build.gradle.kts:9` 4.1.2; `ProblemFactory` uses `tools.jackson.databind`. |
| Every statement traces to a cited source (name and version) or a labelled assumption | **Mostly met** | 15 labelled assumptions; SPEC table §6 with FR/REQ, story ref and tests. Exceptions: Spring Framework reference cited without version (SG3-03); fixture matrix positive role has no source (SG3-04). |

## 3. SG2 findings: resolution check

| SG2 | Severity | Resolved? | Verification |
|---|---|---|---|
| 01 | High | **Yes** | One type set and one client; `api:verify` runs before `typecheck` in `check`; path deviation recorded (TE003-SG-DG-01); no new front-end dependency. |
| 02 | High | **Yes** | Per-operation abstract interfaces (§7.1); guards SPEC-004, -005; resolver reads `RequestMappingHandlerMapping` (SPEC-010); §12/§17 conflict recorded (TE003-SG-DG-02). |
| 03 | Medium | **Yes** | Premise restated (§4); `postAdminWorkflowsSmoke` retrofitted and `enforce: true`, owner RWB-E1-071 (E1-071 v7 §4 step 9 confirms the endpoint); `outsideSpecification` allow-list with decision, owner, open item; contract context sets `rwb.p3.temporal=true`. |
| 04 | Medium | **Yes** | SPEC-005 covers every `@Controller` handler in main classes, including conditional and out-of-spec ones; capability naming excluded with owners. |
| 05 | Medium | **Yes** | In/out split with owners and open items; TE003-SG-DG-04 recorded. |
| 06 | Medium | **Partly** | Suites inside `test` (CI `backend-unit`, `dev.ps1 test`) and `api:verify` inside `npm run check` (CI `frontend-check`), no pipeline change: correct. TE-011 share stated. The coverage gate wiring conflicts with active decisions and with TE-001 v3, and omits two IEG metrics: **SG3-01**. |
| 07 | Medium | **Yes** | PRE-1/PRE-2; `<P2>`; map additions stated; `ModulithTest`, TE-001 rule, `RecoveryBoundaryTest` must pass (T-TE003-31). |
| 08 | Medium | **Yes** | SPEC-007; README decision 6 exception with OPEN-043; ESLint fixture test owned by TE-001 (D-RCV-40; TE-001 v3 SPEC-015). |
| 09 | Medium | **Yes** | §6 defines SPEC-RWB-TE-003-001..021 once each; 36 coverage rows re-counted (5 BR + 8 AC + 8 flow + 8 X + §12 + §13 step 2 + 4 guardrails + §19); 21 matrix rows in `shared-updates.md` §3.2. |
| 10 | Low | **Yes** (see SG3-03) | Target Boot 4.1.2 / Jackson 3; spikes S-1..S-4 with named fallbacks. |
| 11 | Low | **Yes** | A-15 out of scope with owner (OPEN-047). |
| 12 | Low | **Yes** | Header "DRAFT — pending spec gate review-2"; `recoveryApiPackageInfo` is the only writer of `package-info.java`. |

Plan inputs 1-8 of the SG2 review are all used (`gate-response.md` "Plan inputs"; checked against spec §7.3-§7.5, SPEC-010, SPEC-021).

## 4. Findings

### REVIEW-RWB-TE-003-SG3-01: Medium. The coverage gate wiring contradicts two active decisions and the TE-001 spec it depends on, and plans only two of the four required metrics

**Affects:** SPEC-RWB-TE-003-017; §14 Unit Test Applicability (backend row); PRE-3; T-TE003-30; A-09 (coverage part).

**Evidence**
- SPEC-017 (b) and (c) make `recoveryCoverageVerification` and a new `recoveryContractCoverageVerification` finalizers of `test`. `check` depends on `test`, so both gates then run inside `check` and inside `./scripts/dev.ps1 test`.
- Active decisions say the opposite: D-RCV-28 (3) "JaCoCo checks run in recovery-only tasks outside `check`"; D-RCV-40 "`recoveryCoverageReport` / `recoveryCoverageVerification` (… outside `check`)". The spec lists D-RCV-40 among its governing decisions but neither reconciles the conflict nor asks for a superseding decision. `README.md:86-87` ("Add it once the first story's code lands") and audit A-09 support wiring the gate, so the sources disagree and the conflict must be recorded, not silently resolved.
- TE-001 v3 SPEC-020 (the story this one depends on, PRE-1/PRE-3) sets `recoveryCoverageVerification` to four limits, LINE, INSTRUCTION, BRANCH and METHOD, over all main classes, "No main class is excluded", and keeps the tasks outside `check` (d); its SU-10 hands CI wiring to TE-003/TE-011. TE-003 SPEC-017 (b) and §14 still say "(LINE, BRANCH 80%)".
- IEG requires 80% on lines, statements, branches and functions "where supported"; JaCoCo supports all four. The global gate as specified plans two.
- SPEC-017 (a) adds the exclusion `**/generated/**` to `recoveryClasses`. IEG: "Do not … add coverage exclusions to make the run pass". The rationale given (BR5, generated output is not hand-written) is reasonable but is not recorded as a scope decision, conflicts with TE-001 v3 "No main class is excluded", and is not listed for plan-gate approval.

**Required fix**
1. Record the conflict (D-RCV-28 (3) and D-RCV-40 against A-09 and `README.md`) as a gap (this review: TE003-SG3-DG-03) and add a decision request in `shared-updates.md` for the recovery tech lead: either supersede the "outside `check`" clause for the verification task, or keep it outside `check` and state how CI then runs it without a pipeline change (D-RCV-05). Make SPEC-017 conditional on that decision, with the planner stopping if it is refused.
2. Align the global gate with TE-001 v3 SPEC-020: LINE, INSTRUCTION, BRANCH and METHOD at 80%, in SPEC-017 and the §14 backend row.
3. State the `**/generated/**` exclusion as an explicit coverage-scope rule with its source (BR5; BS-7.2 "recovery packages"), reconcile it with TE-001 v3 "No main class is excluded", require it to be listed in the implementation `report.md` (IEG "exclusions and rationale"), and list it for plan-gate approval.
4. Either add the TE-003 tooling class directories to the existing verification task, as D-RCV-43 and TE-001 SPEC-020 (b) do, or give the reason for a separate `recoveryContractCoverageVerification` task.

### REVIEW-RWB-TE-003-SG3-02: Low. The spec predates TE-001 v3 and names baseline paths that TE-001 relocates

**Affects:** §2 Impacted Existing Nodes; §7.5; SPEC-013, -014; PRE-2; `agent-run-log.md`; `compliance-validation.md` §4.

**Evidence**
- The spec and run log say TE-001's remediated spec does not exist. It now does (`INC-002-epic-1-RWB-TE-001/specify/spec.md`, revision v3).
- TE-001 v3 relocation table moves `ApiExceptionHandler`, `ProblemFactory` and `SecurityConfig` to `access.internal` (P4), `TemporalAdminController` to `casewf.admin` (P3), `PlatformInfoController` to `integration.internal` (P2), and splits `RecoveryProperties` into per-module records (SPEC-022, -023).
- TE-003 hedges the controller path ("or its TE-001 location") but names `platform/internal/ApiExceptionHandler.java` and `ProblemFactory.java` without that hedge (§2, §7.5). PRE-2 cites the TE-001 v2 field matrix, not v3 SPEC-004 (g) and SU-09.
- Substance is unaffected: `<P2>` resolves to `integration` under v3, the smoke operation's x-module P3 matches `casewf.admin` for the SPEC-010 module-ownership check, and the `rwb.p3.temporal` key is unchanged. PRE-1 stops the planner if TE-001 is not merged.

**Required fix**
- Cite TE-001 v3 (SPEC-004 (g), SPEC-020, SPEC-022, SU-09, SU-10) in PRE-1/PRE-2.
- Write every baseline path that TE-001 moves as "TE-001 location" (for example `access.internal.ApiExceptionHandler`), or add a single rule that all baseline paths are read after TE-001's relocation.
- Correct the "does not exist" statements in the run log and `compliance-validation.md` §4.

### REVIEW-RWB-TE-003-SG3-03: Low. Generator settings and citations behind the server approach are incomplete

**Affects:** SPEC-003, SPEC-004, SPEC-014; §7.1; §9 S-1 and F-1a; ASM-TE003-05, -11.

**Evidence**
- SPEC-003 lists `useSpringBoot3=true` "until a Boot 4 option is proven", and F-1a is Boot 3 output. The OpenAPI Generator `spring` documentation describes `useSpringBoot4` (Spring Boot 4.x) and `useJackson3` (allowed only with `useSpringBoot4`). These are the options that match the required target (SG2-10).
- No generator option or behaviour is cited to a source with a version (`interfaceOnly`, `skipDefaultInterface`, `useTags`, the `SET_TAGS_TO_OPERATIONID` normalizer). §7.1 and ASM-TE003-11 cite "Spring Framework reference" with no version or section; the repository runs Spring Framework 7 under Boot 4.1.2.
- `requestMappingMode` defaults to `controller`, so with `interfaceOnly=true` the generated interface carries no class-level base path. `TemporalAdminController` has the class mapping `/api/recovery/v1/admin` (line 43), and the interface path is `/admin/workflows/smoke`, so a naive retrofit maps `/api/recovery/v1/admin/admin/workflows/smoke`. `GET /admin/temporal/health` shares that class mapping. S-1 and T-TE003-27 would catch this, but the spec does not name the mechanism.
- SPEC-004 fails "when a type is not an interface" in `<P2>.generated.web`. The spring generator can write supporting classes (for example `ApiUtil`) into the API package. The guard's scope is not defined for them.

**Required fix**
- Make `useSpringBoot4=true` and `useJackson3=true` the primary candidate in SPEC-003 and S-1, and keep the Boot 3 output as F-1a.
- Cite the OpenAPI Generator documentation for each option and normalizer rule, at the version pinned at the plan gate, and cite the Spring Framework 7 reference section for interface-declared `@RequestMapping`.
- State the base-path handling (`requestMappingMode` value, or the controller keeps `/api/recovery/v1` as its class mapping), and that `GET /admin/temporal/health` keeps its path.
- Scope SPEC-004 to the generated `*Api` types, or require that no supporting class is generated into the web package.

### REVIEW-RWB-TE-003-SG3-04: Low. The fixture permission matrix has no source for the "role holding the right", and its one cited row rests on a conflicting story

**Affects:** SPEC-011, -012, -020; ASM-TE003-04; T-TE003-22, -24.

**Evidence**
- SPEC-011 calls each enforced operation "as a role holding the right". SPEC-012 and ASM-TE003-04 define only roles that lack a right, and SPEC-020 forbids roles as literals in suite code. Nothing says where the positive role for `postAdminWorkflowsSmoke` comes from. (RW-PLATADM is supported by E1-071 v7 §1 and §4 step 9.)
- The row "`RW-CASEOWN` lacks Platform administration C" cites TC-E1-071-08. That test case only says RW-CASEOWN is refused. E1-071 v7 X6 frames the refusal as a role "without Platform administration U", while API v4 declares right C for `postAdminWorkflowsSmoke` (and the code comment at `TemporalAdminController.java:91` says C). This conflict is not recorded (this review: TE003-SG3-DG-01).
- E1-071 v7 §4 step 9 says the smoke response gives "workflow ID, run ID and status"; API v4 202 gives `workflowId`, `workflowType`. SPEC-014 keeps API v4, which is right under TE-003 BR1, but the conflict is not recorded (TE003-SG3-DG-02).

**Required fix**
- Add positive rows to the fixture matrix (role, area, letters, cited source), or state the source of the role holding the right.
- Record the two E1-071 conflicts as gaps (Blocker No) and say that API v4 governs the TE-003 suites (TE-003 v7 BR1).

### REVIEW-RWB-TE-003-SG3-05: Low. The handler checks cover only annotated controllers, not other handler mappings

**Affects:** SPEC-001, -005, -010; AGENTS §2, §3.3.

**Evidence**
- SPEC-005 inspects classes meta-annotated `@Controller`. SPEC-001 and SPEC-010 read `RequestMappingHandlerMapping` only.
- AGENTS §2 lists Spring Data REST as part of the stack (absent today; audit A-13: "added only when a story needs them"). Repository endpoints and `RouterFunction` routes are served by other handler mappings, so a later story could expose a `/api/recovery/**` path that neither the conformance check nor the method-security check sees. The filter chain's `HOLDS_WORKBENCH_ROLE` would still apply, but no method check would.

**Required fix**
- Add to SPEC-001 a check that fails when any handler mapping other than `RequestMappingHandlerMapping` (actuator and static resources aside) maps a path under `/api/recovery/v1`. Alternatively, name this as a seam owned by the first story that adds such a mapping, with an open item.

### REVIEW-RWB-TE-003-SG3-06: Low. The tooling source set sits outside the recovery package on an assumption only

**Affects:** §7.5; ASM-TE003-09; SPEC-002, -008, -015, -017 (c).

**Evidence**
- The lint, catalog, baseline and report code is placed in `backend/src/apiTooling/java/th/co/scb/ace/tooling/recoveryapi/`. AGENTS §3.1 says "Put recovery code in the recovery module folder only", and BS-1.1 scopes code to `th.co.scb.ace.demo.recovery`.
- ASM-TE003-09 labels the choice and gives a fallback, but cites no rule that allows build tooling outside the recovery folder. The choice also creates a new Gradle source set and a separate coverage task (see SG3-01 item 4).

**Required fix**
- List the tooling location as a plan-gate approval item (`shared-updates.md` OPEN-039 amendment or a new open item for the recovery tech lead). Otherwise, adopt the ASM-TE003-09 fallback, test-scope `recovery.contract.support`, which TE-001's tooling precedent (`ModuleMapLoader`, test scope) already follows.

## 5. Phase-0 audit items owned by this story

| Item | Disposition in the spec | Verdict |
|---|---|---|
| A-03 | In: all-handler method-check test (SPEC-005). Out: capability naming and role literals to RWB-E1-022 / RWB-E1-037 (OPEN-040 amendment) | Accepted |
| A-04 | Extend `api:generate`; no duplicate (SPEC-006, -007) | Accepted |
| A-08 | In: `messageCode`/`traceId` asserted, `traceId` on 500 (SPEC-011, -013). Out: 500 message ID (OPEN-044), 400/422 mapping (OPEN-045), `{action}` per language (RWB-E1-022) | Accepted |
| A-09 | In: contract job via `test` and `check` (SPEC-016); coverage gate (SPEC-017). Out: PDPA lint to TE-011, Playwright/axe to TE-010, dependency scan and ZAP to hardening (OPEN-046) | Contract part accepted. **Coverage part not accepted: SG3-01** |
| A-11 | In: generated `Problem` (SPEC-007). Excepted: `PlatformInfo`/`TemporalHealth` (README decision 6, OPEN-043). Out: ESLint fixture test to TE-001 | Accepted |
| A-15 | Out: first screen story or hardening (OPEN-047) | Accepted |

## 6. Required checks (reviewer instructions)

| Check | Result |
|---|---|
| Authentication and authorization | PASS with SG3-05 (Low). Method-security presence on every annotated handler; access suite per enforced operation; area `None` tested as 401; live TC-TE-003-09 kept `BLOCKED` (OPEN-040). |
| Customer and account data protection | PASS. No personal data in fixtures, JWT subjects or the report (SPEC-015, -020). |
| Audit logging | N/A. No sensitive financial action; A-18 is RWB-E1-039. |
| KYC, AML, suitability, consent, approval | N/A for a build-tooling story. |
| Frontend integration versioning and error contract | PASS. One type set; `NO_API_CHANGE`; Problem completeness asserted. |
| Secrets and environment configuration | PASS. Test JWTs from `spring-security-test`; no secret in fixtures. |
| Test coverage and evidence (planning) | **FAIL: SG3-01.** Both surfaces REQUIRED. The frontend gate is inherited and correct. The backend global gate plans two of four metrics and conflicts with active decisions. |

## 7. Gate result

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 1] [LOW: 5]
BLOCKING: YES. SG3-01 must be fixed in the specify/ folder and re-reviewed (spec-gate-review-3.md). SG3-02..06 are Low: fix with SG3-01, or carry them with human disposition.
SG2 RESOLUTION: 11 of 12 resolved; SG2-06 partly (coverage part becomes SG3-01).
ORCHESTRATOR CONSTRAINTS: SG2-01 met; SG2-02 met; SG2-07 met; A-03/A-08/A-11/A-15 met, A-09 coverage part open (SG3-01); SG2-10 met as the target.
DOCUMENT_GAPS: 3 new in review/document-gaps-2.md, 0 blockers.
NEXT_STEP: Technical Specifier re-issues SPEC-017, §14 and shared-updates (decision request), then this gate runs again. Do not start the Implementation Planner. PRE-1 (RWB-TE-001 merged) still applies after a PASS.
```

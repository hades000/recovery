# Spec gate review, round 3: RWB-TE-012, document storage containers

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-012-SG3` (new findings `REVIEW-RWB-TE-012-SG-18` to `-25`) |
| RUN_ID | `INC-007-epic-1-RWB-TE-012` |
| Artifact | `aisdlc/output/INC-007-epic-1-RWB-TE-012/specify/`: `spec.md` v3, `assumptions.md`, `document-gaps.md`, `shared-updates.md` v3, `compliance-validation.md`, `gate-response.md` (section "Round 2"), `contracts/backend-apis.json` v3, `contracts/frontend-integrations.json`, `agent-run-log.md` |
| Previous rounds | `review/spec-gate-review.md` (round 1: FAIL, 0C/1H/5M/5L); `review/spec-gate-review-2.md` (round 2: FAIL, 0C/0H/2M/4L, review gap TE012-SG2-DG-01) |
| Reviewer | Compliance Reviewer (spec gate), `.claude/agents/compliance-reviewer.md` with `aisdlc/RUN-BRIEF.md` |
| Date | 2026-11-18 |
| **Status** | **FAIL** |
| Findings | 0 Critical, 0 High, 1 Medium, 7 Low (8 new). Round 2: SG-12, SG-13, SG-15, SG-16, SG-17, TE012-SG2-DG-01 and review input 3 FIXED; SG-14 PARTIAL (residual carried as SG-18) |
| Handoff | **Blocked.** SG-19 is Medium and blocks the Implementation Planner (`aisdlc/.github/rules/pdlc.md`). Under D-RUN-09 the Lows are fixed in the same pass |

## 1. What was checked

**Inputs read.**
- All specify files listed above, diffed against `*.run2.*` (spec, assumptions, shared-updates, compliance-validation, backend contract). `gate-response.md` Round 2 was checked claim by claim against the files, not taken as evidence.
- Round 2 review `review/spec-gate-review-2.md` (findings SG-12 to SG-17, gap TE012-SG2-DG-01, section 6 inputs).
- Story files v7: RWB-TE-012 v1 (flow §4, X6, X7, AC9, AC10, §12, §13, flag); RWB-E1-017 v1 (§3, flow 7-9, BR4); RWB-E1-032 v1 (flow 5-6, BR4, X8, AC10, §17); RWB-E1-054 v1 (precondition, flow 2-9, BR1, BR6, states, `ReviewResolutionService`).
- Decision Log v10 D-RCV-31 (full text); Users, Roles and Permissions v4 (retired actor note, SY-DATALOAD under D-RCV-35 U1).
- Rules: `specification-execution-gates.md` (coverage table vocabulary lines 77-79, status line format line 118), `pdlc.md` (Low-only rule).

**Code verified in this repository (baseline, read only).** `scripts/dev.ps1` (`Initialize-EnvFile` 28-42, `Import-EnvFile` 44-50, called at 86-87; `backend` sets `SPRING_PROFILES_ACTIVE=local` at 110; `test` 114-117; `it` 118); `application-local.yaml` (no `rwb.blob`, no `rwb.dochub`; `rwb.p3.temporal` and `drools` default `true`, lines 12-14); `application.yaml` (`rwb.blob` block, P3 flags default `false`); `docker-compose.yml` (Azurite `3.37.0` with `--skipApiVersionCheck` at 99-100; backend `depends_on` at 121; `SPRING_PROFILES_ACTIVE: local` at 128; Blob variable at 135); `RecoveryDatabaseIT.java` (`@SpringBootTest` with P3 off and no profile, line 31; line 61 sets `rwb.blob.connection-string`); `build.gradle.kts` (Blob SDK `12.37.2`, `azure-identity`, Testcontainers JUnit and PostgreSQL; the "DocumentStorageConfig" comment is at line 59).

**What is correct in v3.**
- The `store()` source rule now carries the D-RCV-31 re-store without a second operation: intake (any name) or, only with `writeOnce=true`, the standard container at the same `{caseId}/{documentId}/v{docVersion}`. This matches D-RCV-31 ("re-stores the file … into the write-once container rwb-docs-legal at {caseId}/{documentId}/v{docVersion}", "keeps the standard-container object"). The source is never deleted, the refusals are listed and unit-tested, and the contract file states the rule.
- The E1-017 archive-container conflict is recorded with sound precedence reasoning and an owner.
- The flag-off behaviour of `DocumentContainers` is defined and tested, so `RecoveryDatabaseIT` can drop line 61.
- An unreachable Azurite no longer fails or delays startup, and `depends_on` is left alone for a stated reason.
- The ARM JSON choice removes the tooling problem: Jackson is on the test classpath, and the test package and path are named.
- The emulator guard now also requires the `local` profile. Both the compose backend (`docker-compose.yml:128`) and `dev.ps1 backend` (`:110`) activate that profile, so local runs are not broken.

## 2. Verification of round-2 findings

| Finding | Severity | Result | Evidence in v3 |
|---|---|---|---|
| SG-12 E1-017 archive container | Medium | **FIXED** | Header "Consumed by RWB-E1-017 (17, archive container: not delivered here, DGAP-22)"; SPEC-019 row "Not delivered: `[S]` §4 defines four containers…"; DGAP-22 cites E1-017 §3, BR4 and §13, TE-012 §4 and AC5, URP v4 "Retired actor" and D-RCV-31; Blocker = No with a reason; CLAR-018; `shared-updates.md` §3 open item (owner solution architect with Compliance, needed by E1-017 specify) and §7 note; coverage row and CONTRADICTIONS line updated. Citations verified in the source files. The way the coverage row and the count are expressed is a new issue: SG-23 |
| SG-13 D-RCV-31 re-store | Medium | **FIXED** | Field matrix `source`: "only when `writeOnce = true`, the standard container with `blobName` equal to the target name"; SPEC-011 steps 2, 4, 8; SPEC-010 "The same `store()` carries the D-RCV-31 re-store"; T-TE012-04 covers the accepted re-store and four refusals; SPEC-019 row "the same `docVersion`" with RWB-E1-054 (70) named; `contracts/backend-apis.json` `BlobWriteRequest_source_rule`. "Same docVersion" agrees with the D-RCV-31 wording quoted above, so no gap is needed. The consumer story silence is a separate gap (SG-25) |
| SG-14 Emulator property claim | Low | **PARTIAL** | Fixed in the properties table ("can be overridden by an environment variable or system property"), SPEC-017 (`Environment.acceptsProfiles(Profiles.of("local"))`), ASM-TE012-11 and T-TE012-02 ("each of the five conditions false in turn"). Not fixed: `shared-updates.md` §5 (b), listed under "Affects" in round 2, is unchanged since v2. It still describes emulator mode as "`rwb.dochub.storage.emulator=true` (set only in `application-local.yaml`)" plus the account and host, and does not mention the `local` profile. Carried as SG-18 |
| SG-15 `DocumentContainers` flag off | Low | **FIXED** | SPEC-008 "Flag off: the `DocumentContainers` bean is present … every container accessor throws `StorageUnavailableException(NOT_READY)` … `readiness()` returns `ready=false`, `reasons=[FLAG_OFF]`"; SPEC-006; SPEC-016; SPEC-019 E1-026/E1-057 row; T-TE012-02; ASM-TE012-29; contract `flag_off` |
| SG-16 Azurite unreachable | Low | **FIXED** | SPEC-017 "logs one WARN line, readiness becomes NOT_READY (`UNREACHABLE`), and startup is neither failed nor delayed"; reason given for leaving `depends_on` unchanged; T-TE012-11 unreachable case; ASM-TE012-28. Re-running the bootstrap inside `store()` creates a timing issue, raised as SG-19 |
| SG-17 Bicep parsing | Low | **FIXED** | ASM-TE012-03, DGAP-09, CLAR-010 and the open item now say ARM JSON; T-TE012-15 names `azuredeploy.json`, `azuredeploy.<env>.parameters.json`, the package `dochub/storage/` and the path `../infra/azure/document-storage/`, with Jackson. New issues with the ARM content (lock, missing assertions) are raised as SG-22 |
| TE012-SG2-DG-01 (review gap) | Gap | **FIXED** | DGAP-22, Blocker = No, with the reason and the open item |
| Review input 3 (T-TE012-13 unset case) | Input | **FIXED** | T-TE012-13: "with the property set explicitly to blank (not relying on the variable being absent, because `dev.ps1` imports `.env` into the Gradle process)". Verified at `dev.ps1:44-50`, `:86-87` |

## 3. New findings

### REVIEW-RWB-TE-012-SG-18: Low. Residual of SG-14: the README decision text in `shared-updates.md` §5 (b) leaves out the `local` profile condition

**Affects:** `shared-updates.md` §5 (b); SPEC-017 (plan-gate item); ASM-TE012-11.

**Evidence**
- `shared-updates.md` §5 (b) is unchanged from `shared-updates.run2.md`. It says emulator mode applies "With `rwb.dochub.storage.emulator=true` (set only in `application-local.yaml`) and the Azurite development account on a loopback or `azurite` host".
- SPEC-017 v3 makes the `local` profile a required condition and says the property "can be overridden from the environment, which is why it is not the only condition".
- The README "Decisions taken" row is the durable record of this local deviation, and SPEC-017 makes it a plan-gate item. As written it states a weaker guard than the one the spec defines.

**Required fix:** Rewrite §5 (b) to list all five conditions of SPEC-017: the `local` profile, the property, a non-blank string, `devstoreaccount1`, and a loopback or `azurite` host. Drop "set only in `application-local.yaml`" as a guarantee.

### REVIEW-RWB-TE-012-SG-19: Medium. The readiness re-evaluation inside `store()` has no time bound, so a store while the hub is not READY can take several timeouts, contrary to AC10, and concurrent re-evaluations are not defined

**Affects:** Status-transition matrix rows 3-4 (lines 289-291); SPEC-009 (line 395); SPEC-011 step 3; SPEC-017 (bootstrap "runs again inside the `store()` re-evaluation"); T-TE012-04, T-TE012-11, T-TE012-12; ASM-TE012-08, -24, -28.

**Evidence**
- RWB-TE-012 v1 AC10: "Given the storage account does not answer within 10 seconds … Then it raises StorageUnavailableException after 10 seconds". X7 points to AC10.
- SPEC-007 bounds each SDK call by `timeout-seconds`. The SPEC-009 evaluation makes one call per container, four in all (get properties, with the legal policy read from the legal container's properties), and SPEC-011 step 3 runs "one re-evaluation" synchronously before the write. No overall deadline applies to the re-evaluation.
- When storage is down, the start evaluation leaves the hub NOT_READY (`UNREACHABLE`), so every later `store()` re-evaluates first. That is up to four 10-second timeouts (about 40 s) before `StorageUnavailableException(NOT_READY)`, and in emulator mode up to eight calls (about 80 s) because the bootstrap's four `createIfNotExists` calls run first. ASM-TE012-24 already treats "up to four timeouts" as too long for startup, yet the same delay is allowed on the request path.
- The spec does not say what happens when `store()` runs while the background start evaluation is still running (state NOT_EVALUATED), or when many concurrent `store()` calls each find NOT_READY. As written, each caller issues its own four (or eight) storage calls, which multiplies traffic against an account that is already failing.
- T-TE012-12 checks "no answer → `TIMEOUT` within 1 s plus a bound" only after a successful start. No test covers a store while the hub is not READY because storage is unreachable.

**Required fix**
- Bound the whole `store()` path, including the re-evaluation and the emulator bootstrap, by `timeout-seconds`. For example, use one deadline shared by all checks, or run the checks in parallel under that deadline.
- Define a single-flight rule: concurrent callers wait for, or reuse, one in-progress evaluation, including the background start evaluation.
- State the resulting exception reason (`NOT_READY` or `TIMEOUT`) for the AC10 case.
- Add unit tests: storage unreachable at start, then `store()` raises within `timeout-seconds` plus a bound; two concurrent `store()` calls cause one evaluation; a `store()` during NOT_EVALUATED does not start a second evaluation.

### REVIEW-RWB-TE-012-SG-20: Low. In emulator mode the hub can never become READY as specified, because the READY guard needs the SY-OCR client ID, which the local profile does not set

**Affects:** Configuration properties table (line 203, `ocr-identity-client-id` "blank gives NOT_READY `IDENTITY_NOT_CONFIGURED:rwb-quarantine`", local column "—"); Status-transition matrix line 289 ("both identities configured"); SPEC-009 line 394; SPEC-017; T-TE012-11; Azurite integration tests.

**Evidence**
- The READY guard (line 289) requires "All four containers present, legal policy present or `EMULATED`, both identities configured". SPEC-009 says "A blank OCR client ID gives `IDENTITY_NOT_CONFIGURED:rwb-quarantine` without a call", and attaches no emulator exception to it.
- In emulator mode there is "one shared-key client for all four containers" (SPEC-017), and SPEC-021 gives `application-local.yaml` no OCR client ID.
- Read literally, the local stack and the Azurite `recovery-it` tests (copy from intake, standard overwrite, write-once upload) would see NOT_READY and fail. The spec exempts the legal policy check in emulator mode (`EMULATED`) but not the identity check.

**Required fix**
- State that in emulator mode the identity checks are skipped, or report `EMULATED`, and that quarantine uses the shared-key client.
- Add this to the transition guard and SPEC-009.
- Assert READY in T-TE012-11 when all four containers exist and no client IDs are set.

### REVIEW-RWB-TE-012-SG-21: Low. Tests that rely on the `local` profile or emulator mode do not say how they activate the profile or pin the emulator string

**Affects:** T-TE012-09 ("local-profile context runner"), T-TE012-11, T-TE012-12 ("emulator mode"), the Azurite `recovery-it` tests; SPEC-017 guard.

**Evidence**
- Since v3, emulator mode requires `Environment.acceptsProfiles(Profiles.of("local"))`. SPEC-018 states how T-TE012-13 sets the profile and the string, but not how T-TE012-11, T-TE012-12 or the Azurite integration tests meet the five conditions.
- A full `@SpringBootTest` with the `local` profile also loads `application-local.yaml`, which turns on `rwb.p3.temporal` and `rwb.p3.drools` by default (lines 12-14). `RecoveryDatabaseIT` switches them off explicitly (line 31) for this reason.
- T-TE012-09 uses a "local-profile context runner" but does not pin `rwb.dochub.storage.emulator-connection-string`. `application-local.yaml` takes that value from `${RWB_DOCHUB_EMULATOR_CONNECTION_STRING:}`, so the test depends on whether `dev.ps1` has imported `.env` (`dev.ps1:86-87`). With `emulator=true` and a blank string, SPEC-017 fails startup, so the test would fail under a plain `./gradlew test`, for example in the CI wiring of audit item A-09. This is the same trap as review input 3.

**Required fix**
- For each emulator-mode or local-profile test, state how the profile is activated (for example an initializer that sets the active profile on a P5-only context runner) and set the emulator string explicitly. Alternatively, have T-TE012-09 run without `emulator`.
- For the Azurite integration tests, state either a P5-only context, or a full context with `rwb.p3.temporal=false` and `rwb.p3.drools=false` as in `RecoveryDatabaseIT`, with the Testcontainers host and mapped port in the string.

### REVIEW-RWB-TE-012-SG-22: Low. With the format now fixed as ARM JSON, the PROD lock is left conditional, and the conformance test asserts a lock parameter and leaves out the private endpoint and the required inputs

**Affects:** SPEC-004 (line 362, "Where the template format cannot express the lock, it is a separate PROD-only pipeline step"); ASM-TE012-04; SPEC-009 (line 397, "Lock state … checked by the template conformance test and SIT"); T-TE012-15 (line 494); SPEC-001 (private endpoint; region, SKU and tier as "Required parameters with no default").

**Evidence**
- In ARM, a container's time-based policy is the `immutabilityPolicies` child resource of the container. It takes the period and the protected-append flags; its `state` is read-only. Locking is a separate `lock` action (for example `az storage container immutability-policy lock`), which a template deployment does not invoke. Now that ASM-TE012-03 fixes the format as ARM JSON, the condition in SPEC-004 and ASM-TE012-04 is decided: the lock is a pipeline step. Yet the spec still leaves it conditional and does not describe the step.
- T-TE012-15 asserts "lock true only in the PROD parameter file". In ARM that parameter drives nothing in the template, so the test gives assurance for a control the template does not apply. The control is RWB-TE-012 v1 BR1 "locked in PROD", which supports CTL-12 and NFR-029.
- T-TE012-15 asserts no private endpoint resource (blob sub-resource, ACE network: SPEC-001, `[S]` §4 step 1). It also does not assert that region, redundancy SKU and access tier have no default (SPEC-001, ASM-TE012-12). AC8 is covered only in SIT.

**Required fix**
- Resolve ASM-TE012-04 for ARM. State the PROD-only lock step: what runs it, when (after the policy apply), who approves it (the step is irreversible) and how its result is evidenced. Show how TC-TE-012-09 or a PROD check verifies the `Locked` state.
- Change T-TE012-15 to assert what the template expresses: the policy resource and its period on the legal container; no lock asserted as a template effect, or the lock step asserted as a pipeline definition if one is committed.
- Add assertions for the private endpoint resource (group `blob`, subnet parameter) and for region, SKU and tier as parameters without a `defaultValue`.

### REVIEW-RWB-TE-012-SG-23: Low. The new E1-017 coverage row and the CONTRADICTIONS field use values outside the gate vocabulary and count conflicts inconsistently

**Affects:** Requirement-to-SPEC coverage row `[E1-017]` §3, BR4 (line 172); summary line 174; `REQUIREMENT_COVERAGE_RESULT` (line 606).

**Evidence**
- `specification-execution-gates.md` lines 77-79 allow `Coverage Type` `DIRECT` or `INHERITED_EXISTING_BEHAVIOR` and `Status` `COVERED` or `BLOCKED`. Line 172 uses "DIRECT (recorded conflict)" and "COVERED (seam)" for a requirement the same row calls "Not in `[S]`" and that SPEC-019 says is "Not delivered". A row cannot be both covered and not delivered.
- Line 118 defines `[CONTRADICTIONS: <n>]`. Line 606 has "[CONTRADICTIONS: 1 (DGAP-22, recorded; settled for this story, seam to RWB-E1-017)]".
- The count of 1 is also inconsistent. DGAP-01 (story v7 against D-RCV-31), DGAP-14 (X9 against AC12) and DGAP-17 (AC9 against E1-024 flow) are source conflicts settled by precedence in the same way, and they are not counted. Line 613 then says "none is left open in this spec".

**Required fix**
- Take the E1-017 row out of the coverage table. It is a consumer's expectation, not a TE-012 rule, and it stays in DGAP-22, CLAR-018 and SPEC-019.
- Use one counting rule for CONTRADICTIONS: either all precedence-settled conflicts (with the DGAP IDs listed elsewhere) or only unresolved ones (then 0). Write the field as a bare number and recompute TOTAL and COVERED.

### REVIEW-RWB-TE-012-SG-24: Low. Version and count metadata in the companion files was not updated for v3

**Affects:** `compliance-validation.md`, `assumptions.md`, `spec.md` "Assumptions", `shared-updates.md` §1, `agent-run-log.md`.

**Evidence**
- `compliance-validation.md`: "Artifact … `spec.md` v2"; "36 rows"; "Clarification Log | Yes, 17 rows"; "ASM-TE012-01 to -27"; "20 active rows, DGAP-18 withdrawn"; "Previous version | `compliance-validation.run1.md`". v3 has 38 rows, 19 CLAR rows, 29 assumptions and 21 active DGAP rows. Only the Stage line changed from `.run2`.
- `assumptions.md` line 3 says "Revision v2" but holds the v3 revisions (ASM-03, -11, -21 "Revised in v3", and -28, -29).
- `spec.md` "Assumptions" says "`ASM-TE012-01` to `-27`" (line 97) but lists -28 and -29.
- `shared-updates.md` §1 cites "spec.md v3" but its status cell still says "spec v2 18 Nov 2026; spec gate round 2 in `review/spec-gate-review-2.md`".
- `agent-run-log.md` "Remediation run 2" Outputs leaves out `compliance-validation.md`, although it was changed and backed up as `.run2`.

**Required fix:** Update each item to v3: version, row counts, ASM range, DGAP count, previous-version pointer, Traceability status text (spec v3, gate round 3) and the run-log outputs.

### REVIEW-RWB-TE-012-SG-25: Low. The re-store seam names RWB-E1-054 as the confirm flow, but RWB-E1-054 v1 has no step that re-types and re-stores a stored document, and the spec records no gap for it

**Affects:** SPEC-019 row "Legal re-store after type confirmation" (line 518); `shared-updates.md` §7 row RWB-E1-032/RWB-E1-054; `document-gaps.md`.

**Evidence**
- Decision Log v10 D-RCV-31 lists "RWB-E1-054 confirm flow" as a consumer of the re-store. RWB-E1-032 v1 flow step 6 and BR4 hold a LOW_CONFIDENCE document "in rwb-docs" "until a person confirms its type" (RWB-E1-054).
- RWB-E1-054 v1 changes the type only for intake items (flow steps 4 and 7: Attach calls `DocumentStore.store`). For stored documents it only confirms or corrects fields (step 9, "POST review"; BR1). Its precondition defines a stored document's PENDING as "when a field is in REVIEW", not as a low-confidence type.
- No E1-054 step, state or service re-stores a stored document into `rwb-docs-legal` or moves `storage_ref`. The seam therefore points at an owner whose story file does not describe the call. The RUN-BRIEF requires such a silence to be recorded.

**Required fix**
- Record a DGAP with the two citations above: D-RCV-31 and E1-032 v1 BR4 against E1-054 v1 flow steps 4, 7 and 9 and the precondition. Set Blocker = No: TE-012's contract already carries the re-store (SG-13), and Decision Log v10 ranks above story files v7.
- Add an open item: owner solution architect with the analyst, needed by RWB-E1-032 and RWB-E1-054 specify, to name the step that calls `store()` for a stored document. Reference it in the SPEC-019 row and the §7 note.

## 4. Requirement and control checks

| Check | Result |
|---|---|
| Authentication and authorization | No endpoint (story §12). Managed identity only; container-scope roles; `open()` is not an authorization point and callers own the check. Pass |
| Customer data protection | UUID blob names; `sha256` metadata only; IDs-only logs; audit `actorId` is the staff subject. Pass |
| Audit of sensitive actions | `DOCUMENT_CHANGE_REFUSED` through the service (T-TE012-10); direct attempts are DGAP-11. Pass |
| KYC, AML, suitability, consent | Not in scope |
| Frontend integration versioning and error contract | `UI In Scope: NO`, `NO_API_CHANGE` verified; 409/503 mappings are seams. Published Java contract now carries the D-RCV-31 re-store. Pass |
| Secrets and environment configuration | Published Azurite key only, local only; five-condition guard. README record incomplete (SG-18) |
| Feature flag off path (AGENTS §3.13) | `DocumentStorage`, `DocumentContainers` and health defined and tested. Pass |
| Write-once control (CTL-12, NFR-029, BR1) | Service-side guard and policy defined; PROD lock step unspecified for ARM (SG-22) |
| AC timing (AC10) | Not met when the hub is not READY (SG-19) |
| Test coverage and evidence | Frontend `NOT_APPLICABLE` correct. Backend four-counter gate, per-class rule and Azurite IT evidence planned. Gaps: SG-19, SG-20, SG-21, SG-22 |
| Module boundaries | RWB-TE-001 v4 map (BND-5 `dochub.storage`; `dochub.api` free of Azure types). Pass |
| Migration rule (D-RUN-07) | No migration. Pass |
| Dependencies (D-RUN-08, AGENTS §4.4) | No new library; E1-017 and E1-054 named. Owner-story silence for the re-store: SG-25 |
| Traceability and status lines | FR, REQ, NFR and CTL rows present; coverage vocabulary and CONTRADICTIONS format (SG-23); stale companion metadata (SG-24) |

## 5. Review-level document gap

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why (blocker or not) | How this stage proceeded |
|---|---|---|---|---|---|---|
| TE012-SG3-DG-01 | Decision Log v10, D-RCV-31 (consumers: "RWB-E1-054 confirm flow"); RWB-E1-032 v1 (story files v7) flow step 6 and BR4 (low-confidence document held in rwb-docs "until a person confirms its type") | A stored, low-confidence document is to be re-stored into rwb-docs-legal when its type is confirmed, through the E1-054 confirm flow. | RWB-E1-054 v1 (story files v7) flow steps 4, 7 and 9, BR1 and its precondition: type is set only for intake items; for stored documents only fields are confirmed (POST review); PENDING means "a field is in REVIEW". No step re-stores a stored document or moves `storage_ref`. | No | Decision Log v10 ranks above story files v7, so the re-store must happen. RWB-TE-012 provides the operation (SG-13), and the missing caller step belongs to E1-032 or E1-054 specification, not to this story's deliverable. | Raised as SG-25 for the specifier; owner solution architect with the analyst via DOCUMENT-GAPS. |

The specifier's DGAP-01 to -17 and -19 to -22 are evidenced and correctly marked non-blocking. DGAP-18 stays withdrawn. DGAP-22's citations were checked in RWB-E1-017 v1 (§3, BR4) and in Users, Roles and Permissions v4 ("Retired actor").

## 6. Gate result

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 1] [LOW: 7]
BLOCKING: YES. SG-19 (store() readiness re-evaluation unbounded; AC10 "after 10 seconds" not met while not READY; no single-flight rule) is Medium. SG-18 and SG-20 to SG-25 are Low and are fixed in the same pass (D-RUN-09). Round 2: SG-12, SG-13, SG-15, SG-16, SG-17, TE012-SG2-DG-01 and review input 3 FIXED; SG-14 PARTIAL (residual is SG-18).
DOCUMENT_GAPS: 1 review-level gap (TE012-SG3-DG-01, Blocker = No); 0 blockers. Specifier DGAP rows accepted.
NEXT_STEP: Technical Specifier re-issues spec v4 for SG-18 to SG-25 (specify/), then this gate is re-run as review/spec-gate-review-4.md. Do not start the Implementation Planner. Triage of whether a further self-run round is allowed is the orchestrator's (Claude Code); no human acceptance is recorded.
```

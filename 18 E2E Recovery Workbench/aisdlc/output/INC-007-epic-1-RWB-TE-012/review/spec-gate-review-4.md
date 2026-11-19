# Spec gate review, round 4: RWB-TE-012, document storage containers

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-012-SG4` (new findings `REVIEW-RWB-TE-012-SG-26` to `-32`) |
| RUN_ID | `INC-007-epic-1-RWB-TE-012` |
| Artifact | `aisdlc/output/INC-007-epic-1-RWB-TE-012/specify/`: `spec.md` v4, `assumptions.md` v4, `document-gaps.md` v4, `shared-updates.md` v4, `compliance-validation.md` v4, `gate-response.md` (section "Round 3"), `contracts/backend-apis.json` v4, `contracts/frontend-integrations.json`, `agent-run-log.md` |
| Previous rounds | `review/spec-gate-review.md` (round 1: FAIL, 0C/1H/5M/5L); `review/spec-gate-review-2.md` (round 2: FAIL, 0C/0H/2M/4L); `review/spec-gate-review-3.md` (round 3: FAIL, 0C/0H/1M/7L, review gap TE012-SG3-DG-01) |
| Reviewer | Compliance Reviewer (spec gate), `.claude/agents/compliance-reviewer.md` with `aisdlc/RUN-BRIEF.md` |
| Date | 2026-11-18 |
| **Status** | **FAIL** |
| Findings | 0 Critical, 0 High, 2 Medium, 5 Low (7 new). Round 3: SG-18, SG-19, SG-20, SG-22, SG-23, SG-24, SG-25 and TE012-SG3-DG-01 FIXED; SG-21 PARTIAL (residual carried as SG-30) |
| Handoff | **Blocked.** SG-26 and SG-27 are Medium and block the Implementation Planner (`aisdlc/.github/rules/pdlc.md`). Under D-RUN-09 the Lows are fixed in the same pass |

## 1. What was checked

**Inputs read.**
- All specify files listed above, diffed against `*.run3.*` (spec, assumptions, document-gaps, shared-updates, both contracts). `gate-response.md` Round 3 was checked claim by claim against the files, not taken as evidence.
- Round 3 review `review/spec-gate-review-3.md` and the orchestrator's round-3 triage conditions for SG-18 to SG-25.
- Story files v7: RWB-TE-012 v1 (§4 step 2, X7, AC9, AC10, BR1, §10 Authority, §13 template parameters and "Done when", §15); RWB-E1-054 v1 (§3 precondition, §4 flow steps 4, 7, 9, BR1); RWB-E1-032 v1 (flow step 6, BR4).
- Decision Log v10 D-RCV-31; Environment and Deployment Design v4 §4.1 (gates), §4.2 (release path and approvers); Error Handling and Resilience Standard v3 §1 to §3; Users, Roles and Permissions v4 (RW-PLATADM "Runs the environment"). A search of the whole `requirement/legacy/` tree found no template format named (Bicep, Terraform, ARM or `azuredeploy`), which confirms DGAP-09.
- Rules: `specification-execution-gates.md`, `pdlc.md` (Low-only rule, overridden here by D-RUN-09).

**Code verified in this repository (baseline, read only).** `backend/build.gradle.kts:60` (comment "DocumentStorageConfig"); `RecoveryDatabaseIT.java:61` (`rwb.blob.connection-string`); `.env.example:23`, `:24`; `docker-compose.yml:135`; `application-local.yaml` (`rwb.p3.temporal`, `drools` default `true`, no `rwb.dochub`). Every line reference in the spec matches.

**What is correct in v4.**
- The `store()` readiness path is now bounded and shared: one probe future, checks in parallel under one `timeout-seconds` deadline, a caller wait bounded by the same value, a stated freshness window with its source labelled as an assumption, and T-TE012-17 for N concurrent callers, the start-probe join and the fresh-NOT_READY fast path.
- Emulator mode reaches READY without client IDs, consistently in the guard, SPEC-009, SPEC-017, the health detail, the contract and the README text.
- The test-mechanism table removes every dependency on `.env` and commits no key; the Azurite tests use a P5-only runner, so `rwb.p3.*` is not involved.
- The template format gap, the PROD lock runbook step (owner, approver, timing, evidence) and the removal of `legalPolicyLocked` are cited correctly. Environment and Deployment Design v4 §4.2 names "Release owner in the ACE team with the application owner" for "Deploy to PROD … In the monthly change window", as SPEC-004 says.

## 2. Verification of round-3 findings

| Finding | Severity | Result | Evidence in v4 |
|---|---|---|---|
| SG-18 README `local` condition | Low | **FIXED** | `shared-updates.md` §5 (b): "Emulator mode is on only when all five conditions hold: the `local` Spring profile is active; …"; "the property alone is not a guard". "Set only in `application-local.yaml`" removed |
| SG-19 unbounded re-evaluation in `store()` | Medium | **FIXED** | Properties table: `readiness-recheck-seconds` 30, range 1–300, ASM-TE012-30 "(assumed; no document gives a value)"; SPEC-009 "Probe deadline", "Single-flight: at most one probe is in flight, held as one shared future", "waits at most `timeout-seconds` from its own entry", "Numbers and where they come from"; exception reasons `NOT_READY` / `TIMEOUT`, both 503 MSG-GEN-006 (existing message ID); T-TE012-17 "20 concurrent `store()` calls … exactly one probe … within 1 s plus a 1 s bound"; contract `store_when_not_ready`. The new rule "READY is left when … `UNAVAILABLE`" creates a new issue: SG-26 |
| SG-20 emulator never READY | Low | **FIXED** | Transition guard "(in emulator mode the identity checks are `EMULATED`, SPEC-017)"; SPEC-009 "the identity checks are reported `EMULATED` (no client ID is needed)"; SPEC-017 "quarantine included"; health detail `identities`; T-TE012-11 "**no** service or OCR client ID set → READY"; Azurite IT case "READY with no client IDs set"; README text in §5 (b); ASM-TE012-31 |
| SG-21 test profile and emulator string | Low | **PARTIAL** | Fixed for every emulator-mode and local-profile test: SPEC-018 "How tests set the profile and the emulator string" (initializer `setActiveProfiles("local")` on a P5-only runner, explicit property names, string built at run time with a per-run random key, `AZURITE_ACCOUNTS` for Testcontainers; "no key is committed"). Not fixed: T-TE012-09, moved to the default profile, sets only the flag and `emulator=false`, so its flag-on case breaks a startup rule. Carried as SG-30 |
| SG-22 template format, PROD lock, conformance | Low | **FIXED** | Format: SPEC-001 "The document set names no format (`[S]` §13 …; `[ENV]` §4 …): DGAP-09", with the reason; DGAP-09 re-cited, Blocker = No. Lock: SPEC-004 "PROD lock: a runbook step outside the template", table with what, where (`RUNBOOK.md`), when, who runs (RW-PLATADM), who approves, evidence, never; `legalPolicyLocked` removed (DGAP-24, Blocker = No). T-TE012-15 asserts the `immutabilityPolicies` resource and period, "**no** parameter or property for a lock", the private endpoint (`groupIds` [`blob`], `privateEndpointSubnetId`) and the six required inputs with no `defaultValue`. Two new issues with the runbook and the required-input assertion: SG-27, SG-28 |
| SG-23 coverage vocabulary and CONTRADICTIONS | Low | **FIXED** | E1-017 row removed; "37 rows, 37 covered, 0 blocked" (37 rows counted); counting rule stated; `[CONTRADICTIONS: 0]` bare; settled conflicts listed by DGAP ID |
| SG-24 stale companion metadata | Low | **FIXED** | `compliance-validation.md` "spec.md v4", "37 rows", "23 rows", "ASM-TE012-01 to -31", "23 active rows", previous versions `.run1` to `.run3`; `assumptions.md` "Revision v4 … 31 assumptions" (31 rows counted); spec "Assumptions" "`-31`"; `shared-updates.md` §1 "spec v4 … spec gate round 4"; `agent-run-log.md` run-2 Outputs now list `compliance-validation.md` |
| SG-25 E1-054 has no re-store step | Low | **FIXED** | DGAP-23 cites D-RCV-31 and RWB-E1-032 v1 step 6, BR4 against RWB-E1-054 v1 steps 4, 7, 9, BR1 and the precondition; Blocker = No with the precedence reason; open item (solution architect with the analyst, needed by E1-032 and E1-054 specify); SPEC-019 row and §7 note reference it; CLAR-022. Citations checked in the story files. DGAP-22 unchanged (diff against `.run3`) |
| TE012-SG3-DG-01 (review gap) | Gap | **FIXED** | Recorded as DGAP-23, Blocker = No |

## 3. New findings

### REVIEW-RWB-TE-012-SG-26: Medium. Any `UNAVAILABLE` result, including a missing blob on `open()`, turns the whole hub NOT_READY (`UNREACHABLE`), contrary to the transition matrix's own qualifier, and the mapper, tests and contract do not state the rule

**Affects:** SPEC-009 "READY is left" (line 423); Status-transition matrix row "READY | … `TIMEOUT` or `UNAVAILABLE` (5xx or I/O after SDK retries)" (line 300); SPEC-013 table (lines 476-480); SPEC-015; SPEC-020; T-TE012-06, -07, -17; `contracts/backend-apis.json` `store_when_not_ready`; ASM-TE012-08, -13, -15.

**Evidence**
- SPEC-009: "READY is left when a `store()` or `open()` call … ends in `TIMEOUT` or `UNAVAILABLE` (NOT_READY `UNREACHABLE`)". No qualifier.
- SPEC-013 maps "`BlobNotFound` on `open()`" to `StorageUnavailableException(UNAVAILABLE)` (also ASM-TE012-15, T-TE012-07). Read together, one read of a document whose blob is missing (a single-record fault) marks the hub NOT_READY `UNREACHABLE`. For `readiness-recheck-seconds` (30 s) every `store()` is then refused with 503 MSG-GEN-006, and SPEC-020 turns `documentHub` `DOWN`, so the root `/actuator/health` answers 503. The reason `UNREACHABLE` would also be false. Any user who can open documents can trigger this.
- The transition matrix limits the trigger to "`UNAVAILABLE` (5xx or I/O after SDK retries)", so the two normative statements disagree. `open()` is also "Not gated by readiness" (ASM-TE012-13), but it now changes readiness, and no assumption says so.
- SPEC-013 says "readiness set to NOT_READY" only on the `ContainerNotFound` row, not on the `TIMEOUT` and 5xx/I/O rows. T-TE012-06 checks only "`ContainerNotFound` setting NOT_READY". T-TE012-17 covers a `store()` `TIMEOUT` only. No test shows that a `BlobNotFound` leaves READY unchanged. The contract's `store_when_not_ready` does not tell consumers that a failed call makes later stores fail fast.

**Required fix**
- In SPEC-009, the matrix and SPEC-013, state one rule: only `TIMEOUT` and transport-level `UNAVAILABLE` (5xx or I/O after SDK retries) from `store()` or `open()` set NOT_READY `UNREACHABLE`. `BlobNotFound`, 4xx codes and `ACCESS_REFUSED` leave the state unchanged. Mark the affected rows in the SPEC-013 table.
- Record in ASM-TE012-13 that `open()` failures can change readiness.
- Add tests: T-TE012-06 (or -17) shows that `BlobNotFound` on `open()` leaves READY and that 5xx/I/O on `open()` sets NOT_READY. Add one sentence to the contract.

### REVIEW-RWB-TE-012-SG-27: Medium. T-TE012-15 requires non-blank values for every required input in all four parameter files at unit-test time, but those values belong to open decisions and are supplied only "before the first apply in that environment"

**Affects:** SPEC-001 (line 360, "Every required parameter has a non-blank value in each parameter file; the platform team supplies the environment values before the first apply in that environment"); T-TE012-15 (line 523); `shared-updates.md` §3 open item ("T-TE012-15 fails while any of these is blank", needed by "Before SIT"); Unit Test Applicability (every T-TE012 unit test passes in `test`).

**Evidence**
- T-TE012-15 runs in the `test` task, which is pipeline gate 1 "The service builds and every unit … test passes" (Environment and Deployment Design v4 §4.1). It asserts that "each of the four parameter files gives every one of them a non-blank value": `location`, `skuName`, `accessTier`, `privateEndpointSubnetId`, `aceServicePrincipalId` and `ocrPrincipalId`.
- Several of these values depend on open decisions recorded by this spec: region (DGAP-13, Personal Data Protection Design v2 §8, the bank's position "to confirm"), redundancy and tier (DGAP-05, -07; DL27 open). The PROD and UAT subnet and object IDs are not needed until those environments are applied. RWB-TE-012 v1 §13 "Done when" requires the template to be applied in DEV and SIT only.
- So at merge the test either fails, turning `./scripts/dev.ps1 test` red for this and every later story until UAT and PROD inputs exist, or the parameter files carry invented non-blank placeholders. Placeholders make the assertion prove nothing and put undecided values (for example a region) into the repository as if they were decided. Neither result agrees with "supplied before the first apply in that environment".

**Required fix:** Make the unit assertion match the decision timeline. For example, require real non-blank values only in the DEV (and SIT) parameter files. Let UAT and PROD files hold one documented placeholder token that T-TE012-15 recognises, and add a pre-apply check (a runbook or pipeline step, owned by RW-PLATADM) that refuses to apply while a placeholder remains. Update SPEC-001, T-TE012-15 and the open item's "Needed by" for each environment.

### REVIEW-RWB-TE-012-SG-28: Low. The spec does not say what a later PROD template apply does to the policy once the runbook step has locked it

**Affects:** SPEC-004 ("The policy is unlocked after every apply"; runbook table); ASM-TE012-04; `RUNBOOK.md` (plan-gate item); T-TE012-15.

**Evidence**
- SPEC-004 declares the legal container's `immutabilityPolicies` child resource in every apply. After the first PROD lock, every later PROD apply of the same template, for example one that changes a tag, an SKU or a role, sends that resource again.
- Azure's create-or-update operation for a container immutability policy is documented for an unlocked policy. A locked policy accepts only the extend action, which can only increase the period. As written, a later PROD apply may fail on the locked policy, or need its own handling. Either way, "The policy is unlocked after every apply" is not true in PROD after the lock. Neither the spec nor the runbook entry covers the case, so the irreversible step has no defined effect on later deployments.

**Required fix:** In SPEC-004 and the `RUNBOOK.md` content, state how later PROD applies treat the locked policy. Examples: the policy resource is deployed conditionally, under a parameter that is true only for the first apply in an environment; or the runbook names the extend action as the only allowed change after the lock. Add the matching T-TE012-15 assertion. If the behaviour cannot be confirmed before PROD, record it as an assumption with its effect and add it to the DGAP-03 DEV spike scope on a disposable account.

### REVIEW-RWB-TE-012-SG-29: Low. X7, the transition matrix and the READY guard each state the new readiness rules differently from SPEC-009

**Affects:** Exceptional-case X7 (line 313); Status-transition matrix (lines 294-298); SPEC-009 (lines 419, 422); properties table (`service-identity-client-id`, line 206).

**Evidence**
- X7: "`StorageUnavailableException(TIMEOUT)` after `timeout-seconds`; this holds also when the hub is not READY". SPEC-009, the contract (`store_when_not_ready`) and `shared-updates.md` §7 say that when the hub is not READY, a fresh NOT_READY refuses at once with `NOT_READY` and a probe result NOT_READY gives `NOT_READY`. `TIMEOUT` occurs only when the caller's wait ends first. X7 states the wrong reason for the usual not-READY case (both map to 503 MSG-GEN-006, so callers are unaffected).
- SPEC-009 says that in state NOT_EVALUATED "the caller joins **or starts** the probe". The matrix has only "`store()` called while the start probe runs → … joins the start probe". It has no row for a `store()` before `ApplicationReadyEvent`, when no probe is in flight (for example a job started by a lifecycle bean), and it does not say what the start probe does if such a probe has already set the state.
- The READY guard requires "both identities configured". The properties table says a blank service-identity client ID "uses the default managed identity", and SPEC-009 checks only a blank OCR client ID. "Both identities configured" can be read as also refusing a blank service ID.

**Required fix:** Reword X7 to "`TIMEOUT` or `NOT_READY` (SPEC-009) within `timeout-seconds`". Add the matrix row "NOT_EVALUATED | `store()` called, no probe in flight → starts the single probe" and state what the start probe does afterwards. Write the guard as "OCR client ID set (service identity: configured or default managed identity)".

### REVIEW-RWB-TE-012-SG-30: Low. Residual of SG-21: T-TE012-09's flag-on case sets no `account-url`, so as specified its context fails a startup rule or depends on an environment variable

**Affects:** T-TE012-09 (line 517); SPEC-018 test-mechanism table row T-TE012-09 (line 532); properties startup rules (line 215).

**Evidence**
- T-TE012-09 runs "Default profile, emulator off: `ApplicationContextRunner` with `ConfigDataApplicationContextInitializer` (loads `application.yaml` only)". Its properties are "`rwb.dochub.storage-containers` as each case needs, `rwb.dochub.storage.emulator=false`".
- The NOT_READY → root `DOWN` case needs the flag on. Line 215: startup fails when "the flag is on, `emulator` is false and `account-url` is blank or not `https`". `application.yaml` gives `${RWB_DOCHUB_ACCOUNT_URL:}`, which is blank unless the variable is set in the Gradle process. That is the same environment dependence that SG-21 removed for the emulator string.
- The row does not say which configuration classes the runner holds, so a reader cannot tell whether `DocumentStorageProperties` validation runs.

**Required fix:** For T-TE012-09, name the configuration classes in the runner. Either set `rwb.dochub.storage.account-url=https://<synthetic>.blob.core.windows.net` explicitly for the flag-on cases, or state that the runner holds only the health indicator, with a stubbed state and no `DocumentStorageProperties`.

### REVIEW-RWB-TE-012-SG-31: Low. The SPEC-001 settings table is broken by the inserted paragraph, and SPEC-004 cites the wrong story section for RW-PLATADM

**Affects:** SPEC-001 (lines 351-361); SPEC-004 runbook table "Who runs it" (line 382); ASM-TE012-04.

**Evidence**
- In v4 the "Template format: …" paragraph (line 360) was inserted between the table rows. The row "| Encryption at rest | Platform default (Microsoft-managed keys) … |" (line 361) now stands alone after the paragraph, without a header, so the encryption setting is no longer in the SPEC-001 settings table. In `spec.run3.md` it was part of the table.
- SPEC-004 "Who runs it | RW-PLATADM … | `[S]` §15 (applies the infrastructure template)", and ASM-TE012-04 cites "§15 (RW-PLATADM applies the template)". In RWB-TE-012 v1, §15 is "Screens and states", and the spec itself cites it as "No screen in this story". The RW-PLATADM row "Applies the infrastructure template" is in §10 Authority.

**Required fix:** Move the encryption row back into the SPEC-001 table, above the paragraph. Change both citations to `[S]` §10.

### REVIEW-RWB-TE-012-SG-32: Low. Cross-references and counts that the round-3 changes made stale

**Affects:** SPEC-023 (line 594); T-TE012-01 (line 509); ASM-TE012-24; SPEC-009 "Numbers" bullet (line 424) and ASM-TE012-30; `shared-updates.md` §2.

**Evidence**
- SPEC-023: "T-TE012-01 to -13 are the tests that cover them". T-TE012-17 (`StorageReadinessProbeTest`), the unit test for the new probe logic in `StorageReadinessIndicator`, is left out.
- T-TE012-01 lists the defaults it checks as "timeout 10, four names, flag false, emulator false". The new default `readiness-recheck-seconds` = 30 is not listed. Its range is covered by "every startup-failure rule".
- ASM-TE012-24 "Effect if wrong": "Synchronous evaluation would delay the readiness probe by up to 40 s when storage is down". With the v4 probe bound (SPEC-009, "never takes longer than `timeout-seconds`") the figure is 10 s.
- SPEC-009 and ASM-TE012-30 say Error Handling and Resilience Standard v3 §3 "gives retry intervals only for outbound files, agents and Temporal". §3 also gives "Inbound loads: Check each hour". The conclusion (no value for storage) still holds.
- `shared-updates.md` §2 asks for DGAP-01 to -17 and -19 to -24 to be copied, but its "Suggested owners" list names no owner for DGAP-22, -23 or -24.

**Required fix:** Change SPEC-023 to "T-TE012-01 to -13 and -17". Add `readiness-recheck-seconds` 30 to T-TE012-01. Change ASM-TE012-24 to 10 s. Add inbound loads to the §3 statement. Add owners for DGAP-22 (solution architect with Compliance), DGAP-23 (solution architect with the analyst) and DGAP-24 (platform team with the release owner), consistent with the open items.

## 4. Requirement and control checks

| Check | Result |
|---|---|
| Authentication and authorization | No endpoint (story §12). Managed identity only; container-scope roles; `open()` is not an authorization point. Pass |
| Customer data protection | UUID blob names; `sha256` metadata only; IDs-only logs; tests use generated keys and synthetic data. Pass |
| Audit of sensitive actions | `DOCUMENT_CHANGE_REFUSED` (T-TE012-10); direct attempts DGAP-11. Pass |
| KYC, AML, suitability, consent | Not in scope |
| Frontend integration versioning and error contract | `UI In Scope: NO`, `NO_API_CHANGE`; 409/503 mappings are seams. The contract does not state that a failed call changes readiness (SG-26) |
| Secrets and environment configuration | Five-condition guard and README text consistent; no committed test key. Pass |
| Feature flag off path (AGENTS §3.13) | Defined and tested. Pass |
| Write-once control (CTL-12, NFR-029, BR1) | Policy in the template; PROD lock runbook step with owner, approver and evidence. A later PROD apply after the lock is undefined (SG-28) |
| AC timing (AC10) | Bounded by the single-flight probe and the caller wait (SG-19 fixed). X7 wording (SG-29) |
| Availability of the write path | One missing-blob read can block all stores for 30 s and turn the root health 503 (SG-26) |
| Test coverage and evidence | Frontend `NOT_APPLICABLE` correct. Backend four-counter gate, per-class rule, Azurite IT evidence planned. Gaps: SG-26 (tests), SG-27 (a unit test that cannot pass honestly at merge), SG-30, SG-32 |
| Module boundaries | RWB-TE-001 v4 map; no Azure type in `dochub.api`. Pass |
| Migration rule (D-RUN-07) | No migration. Pass |
| Dependencies (D-RUN-08, AGENTS §4.4) | No new library (virtual threads are in JDK 21). Pass |
| Traceability and status lines | 37 rows; vocabulary and `CONTRADICTIONS` format correct; companion counts correct. Stale references: SG-32 |

## 5. Document gaps

No new review-level gap. SG-27 depends on decisions the specifier already records (DGAP-05, -07, -13; DL27). SG-28 is about the Azure platform's behaviour, not a silence in the document set.

The specifier's new rows were checked:
- **DGAP-23** cites Decision Log v10 D-RCV-31 and RWB-E1-032 v1 step 6 and BR4, against RWB-E1-054 v1 steps 4, 7, 9, BR1 and the §3 precondition ("review_status PENDING when a field is in REVIEW"). Verified. Blocker = No is correct: Decision Log v10 ranks above story files v7.
- **DGAP-24** cites RWB-TE-012 v1 §13 ("legalPolicyLocked true in PROD only") against Environment and Deployment Design v4 §4.2 (no infrastructure or lock step), with BR1 kept. Verified. Blocker = No is correct.
- **DGAP-09** re-cited: no template format is named anywhere in `requirement/legacy/`. Verified.

DGAP-01 to -17 and -19 to -22 stay accepted. DGAP-18 stays withdrawn. 0 blockers.

## 6. Gate result

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 2] [LOW: 5]
BLOCKING: YES. SG-26 (any UNAVAILABLE, including BlobNotFound on open(), sets the hub NOT_READY for readiness-recheck-seconds; spec, matrix, mapper, tests and contract disagree) and SG-27 (T-TE012-15 requires non-blank UAT/PROD and undecided inputs at unit-test time) are Medium. SG-28 to SG-32 are Low and are fixed in the same pass (D-RUN-09). Round 3: SG-18, SG-19, SG-20, SG-22, SG-23, SG-24, SG-25 and TE012-SG3-DG-01 FIXED; SG-21 PARTIAL (residual is SG-30).
DOCUMENT_GAPS: 0 new review-level gaps; 0 blockers. Specifier DGAP-23 and DGAP-24 verified and accepted (Blocker = No); DGAP-09 re-citation verified.
NEXT_STEP: Technical Specifier re-issues spec v5 for SG-26 to SG-32 (specify/), then this gate is re-run as review/spec-gate-review-5.md. Do not start the Implementation Planner. Whether a further self-run round is allowed is decided by the orchestrator's (Claude Code) triage; no human acceptance is recorded.
```

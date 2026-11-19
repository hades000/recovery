# Spec gate review, round 5: RWB-TE-012, document storage containers

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-012-SG5` (new findings `REVIEW-RWB-TE-012-SG-33` to `-36`) |
| RUN_ID | `INC-007-epic-1-RWB-TE-012` |
| Artifact | `aisdlc/output/INC-007-epic-1-RWB-TE-012/specify/`: `spec.md` v5, `assumptions.md` v5, `document-gaps.md` v5, `shared-updates.md` v5, `compliance-validation.md` v5, `gate-response.md` (section "Round 4"), `contracts/backend-apis.json` v5, `contracts/frontend-integrations.json` (unchanged), `agent-run-log.md` |
| Previous rounds | `review/spec-gate-review.md` (round 1: FAIL, 0C/1H/5M/5L); `review/spec-gate-review-2.md` (round 2: FAIL, 0C/0H/2M/4L); `review/spec-gate-review-3.md` (round 3: FAIL, 0C/0H/1M/7L); `review/spec-gate-review-4.md` (round 4: FAIL, 0C/0H/2M/5L) |
| Reviewer | Compliance Reviewer (spec gate), `.claude/agents/compliance-reviewer.md` |
| Date | 2026-11-18 |
| **Status** | **FAIL** |
| Findings | 0 Critical, 0 High, 0 Medium, 4 Low (4 new). Round 4: SG-27, SG-29, SG-30, SG-31, SG-32 FIXED; SG-26 and SG-28 PARTIAL (substance fixed; Low residuals carried as SG-33 and SG-35) |
| Handoff | No Critical, High or Medium finding remains. The gate result is still FAIL because Low findings exist. Under D-RUN-09 the Lows are fixed in the same pass; whether a further round runs is the orchestrator's triage. No human acceptance is recorded |

## 1. What was checked

**Inputs read.**
- All specify files listed above, diffed against `*.run4.*` (spec, assumptions, document-gaps, shared-updates, compliance-validation, backend contract). `gate-response.md` Round 4 was checked claim by claim against the files, not taken as evidence.
- Round 4 review `review/spec-gate-review-4.md` and the orchestrator's round-4 triage conditions for SG-26 to SG-32 (given in the review brief).
- Document set, read only: RWB-TE-012 story file v1 (§4, §5 X6/X7, §7 AC9/AC10, §8 BR1, §10 Authority, §13, §14, §15); RWB-E1-024 v1 (§5 X8, §12 GET document and GET content error lists, §14 messages); Error and Message Standard v4 (whole MSG-GEN and MSG-P5 tables); Error Handling and Resilience Standard v3 §3; Environment and Deployment Design v4 §2, §3, §4.1, §4.2, §6, §7, §8.
- External citations introduced in v5, checked on Microsoft Learn: `[AZ-IMM]` "Immutable storage for blob data overview" (ms.date 18 August 2026, as cited), section "Locked versus unlocked policies"; `[AZ-REST]` "Blob Containers - Create Or Update Immutability Policy", api-version 2026-09-01 (as cited). Also read for SG-35: Microsoft Learn "Conditional deployment with templates" (ARM), section "Complete mode".
- Rules: `specification-execution-gates.md`; compliance-reviewer agent definition.

**Citations verified against the source.**
- `[S]` §10 Authority: "RW-PLATADM, platform administrator | Applies the infrastructure template and reads the readiness check". SPEC-004 and ASM-TE012-04, -32 now cite §10. Correct.
- Error and Message Standard v4: no message exists for a stored file whose blob is missing. MSG-GEN-006 ("{system} is not available …") is the only storage-availability message. The claim in ASM-TE012-15, SPEC "Exceptional-case behaviour" and the contract is correct. RWB-E1-024 v1 §12 GET content lists "404; 503 while state is COPY_PENDING (MSG-GEN-006)" and has no case for a STORED row with a missing blob, so "the caller owns the mapping" is correct.
- `[ERR]` §3: rows for outbound files, inbound loads ("Check each hour until the load window closes"), agent calls and Temporal; none for storage. SPEC-009 and ASM-TE012-30 now state this correctly.
- `[ENV]` §4.1 gate 1 "The service builds and every unit, rule package and rule scenario test passes"; §4.2 has no infrastructure or lock step and names "Release owner in the ACE team with the application owner" for "Deploy to PROD". Correct as cited.
- `[AZ-IMM]`: "You can't delete a locked time-based retention policy. You can extend the retention period, but you can't decrease it. A maximum of five increases to the effective retention period is allowed over the lifetime of a locked policy that is defined at the container level." SPEC-004 and ASM-TE012-33 paraphrase it correctly.
- `[AZ-REST]`: "Creates or updates an unlocked immutability policy." Quoted correctly in SPEC-004.

**Governance checks.** No document-set file and no shared file (Traceability Matrix, `DOCUMENT-GAPS.md`, `open-items.md`, README, code, `infra/`) was modified after round 4 (file times checked; `agent-run-log.md` run 4 "No git run, no code edited, no document-set file changed, no shared file changed"). No credential, key or personal data was added. The only new values are synthetic: an all-zero subscription GUID, location `conformance` and the URL `https://rwbconformance.blob.core.windows.net` (never called). No new dependency: PowerShell is already used by `scripts/dev.ps1`, Jackson is on the test classpath, and the parameter schema is a plain JSON list.

**Counts verified.** 37 coverage rows (37 COVERED); 26 CLAR rows; 33 assumption rows (`ASM-TE012-01` to `-33`); 18 open items in `shared-updates.md` §3, as `compliance-validation.md` states; 23 active DGAP rows.

## 2. Verification of round-4 findings

| Finding | Severity | Result | Evidence in v5 |
|---|---|---|---|
| SG-26 only the probe changes readiness | Medium | **PARTIAL** (substance fixed; Low residual SG-33) | Matrix (line 292): "**Only the readiness probe (SPEC-009) writes it**; an operation's own outcome never does". Probe-only rows 298–300 (`checkedAt` = probe end). Row 306: an operation's `TIMEOUT`, transport `UNAVAILABLE` or `ContainerNotFound` only requests one background probe ("Unchanged; only that probe's result can change the state"). Row 307: `BLOB_MISSING`, `ACCESS_REFUSED`, write-once refusal, conflict, other 4xx, size or type refusal → "Unchanged; no probe requested". SPEC-009 "Only the probe writes readiness", "Background probe request", "Reuse window: the 30 s reuse applies to probe results only". SPEC-013 marks each row; `BlobNotFound` → `BLOB_MISSING`, "no probe"; "The mapper never writes readiness". SPEC-015 and ASM-TE012-13 say `open()` never changes readiness. New `Reason.BLOB_MISSING` mapped to 503 MSG-GEN-006 at the caller, with the standard's silence stated (verified). Tests: T-TE012-06 (mapper never writes readiness; probe request per row); T-TE012-18 "`open()` of a missing blob → `BLOB_MISSING`; `documentHub` stays `UP`, readiness and `checkedAt` unchanged, root HTTP 200, zero probes" and "Probe failure … → NOT_READY `UNREACHABLE`, `documentHub` `DOWN`, root HTTP 503". Contract `readiness_writer`, `per_operation_outcome`, `probe_failure`. Matrix, mapper, tests and contract agree. Residual: the health-detail definition of `checkedAt` (line 286) still says an operation can set NOT_READY (SG-33). The wording of the background-request rule also differs between sections (SG-34) |
| SG-27 template unit test vs undecided values | Medium | **FIXED** | SPEC-001 "Required inputs, parameter files and the pre-deploy check": `azuredeploy.parameters.schema.json` lists every required input, `privateEndpointSubnetId` included, with name, type, shape pattern, owner and needed-by. T-TE012-15 checks the template against the schema list and the synthetic `azuredeploy.local.parameters.json`, and checks only presence and shape (value or exactly `__SET_BEFORE_APPLY__`) in the four environment files. "It never needs an undecided value, so it passes in `test` at merge." Pre-deploy check `Test-DeployParameters.ps1`: not a unit test; step 1 of every `RUNBOOK.md` apply and the first step of any future ACE infrastructure stage; refuses the local file, missing, blank, placeholder or shape-invalid values; run by RW-PLATADM (`[S]` §10), maintained by the platform team; Builder evidence stated. One open item per undecided value with owner and needed-by (`shared-updates.md` §3: location, skuName, accessTier, encryption key type, subnet, ACE object ID, OCR object ID, plus the check itself). Gaps only where the document set should hold the value (DGAP-05, -07, -13, re-checked, Blocker = No); subnet and object IDs are treated as environment facts. ASM-TE012-32, CLAR-025. Stale scope lines: SG-36 |
| SG-28 later PROD applies after the lock | Low | **PARTIAL** (Low residual SG-35) | SPEC-004 "Later PROD applies after the lock": the policy resource has `condition` `[parameters('deployLegalPolicy')]` (`false` in the PROD file); the first PROD apply overrides it once; later PROD applies skip it; period changes only by the runbook "Extend" step (increase only, at most five times); shortening or removal "not possible and not attempted". `[AZ-IMM]` and `[AZ-REST]` cited and verified. Enforced by the pre-deploy check and T-TE012-15. ASM-TE012-33, CLAR-026, DGAP-03 spike scope. Residual: the deployment mode is not fixed, and in complete mode ARM deletes a resource whose condition is false; the pre-deploy check cannot see the first-apply override as specified (SG-35) |
| SG-29 X7, start-event row, READY guard | Low | **FIXED** | X7: "`TIMEOUT` or `(NOT_READY)` (SPEC-009) within `timeout-seconds`", with both cases explained. Matrix rows 301 (start event joins an in-flight probe or starts one) and 302 (`store()` before `ApplicationReadyEvent` starts the single probe; the start event later joins it, or starts none within the window). Guard row 298 and properties table line 210: "OCR client ID set (service identity: configured client ID or the default managed identity)" |
| SG-30 T-TE012-09 runner | Low | **FIXED** | T-TE012-09 names the runner contents (`ConfigDataApplicationContextInitializer`, health endpoint auto-configuration, `DocumentStorageProperties` "so its startup rules run", `StorageReadinessIndicator` with a stub `ReadinessProbe`, no Blob client). Flag-on cases set `rwb.dochub.storage.account-url=https://rwbconformance.blob.core.windows.net`, in both the test row and the "How tests set the profile" table |
| SG-31 SPEC-001 table and §15 citation | Low | **FIXED** | Encryption row is back inside the SPEC-001 table (line 367), above the "Template format" paragraph. SPEC-004 "Who runs it" and ASM-TE012-04 cite `[S]` §10 Authority (verified) |
| SG-32 stale cross-references | Low | **FIXED** | SPEC-023 "T-TE012-01 to -13, -17 and -18"; T-TE012-01 asserts `readiness-recheck-seconds` 30; ASM-TE012-24 "up to `timeout-seconds` (10 s)"; SPEC-009 and ASM-TE012-30 add inbound loads to the §3 statement; `shared-updates.md` §2 gives owners for DGAP-22, -23 and -24, matching the open items |

## 3. New findings

### REVIEW-RWB-TE-012-SG-33: Low. The `documentHub` detail `checkedAt` still says an operation can set NOT_READY, contrary to the probe-only rule

**Affects:** Field-level matrix "Health component `documentHub` (SPEC-020)", row `checkedAt` (line 286); `StorageReadiness.checkedAt` (SPEC-010); T-TE012-18.

**Evidence**
- Line 286: "`checkedAt` | UTC instant the last probe ended, or the last store/open call that set NOT_READY (absent when never evaluated)".
- In v5 a store or open call can no longer set NOT_READY. The matrix (line 292, rows 299–300, "`checkedAt` = probe end"), SPEC-009 ("`store()`, `open()` and `StorageErrorMapper` never write it") and the contract (`readiness_writer`) say only the probe writes the state. T-TE012-18 asserts that "`checkedAt` [is] unchanged" after a per-operation failure.
- This is the v4 wording that SG-26 replaced elsewhere. A Builder who implements the field matrix would write `checkedAt` from operations and would fail T-TE012-18.

**Required fix:** Change the row to "UTC instant the last probe ended (absent when never evaluated)".

### REVIEW-RWB-TE-012-SG-34: Low. The background-probe rule is stated differently in the matrix, SPEC-009 and the tests, and one SPEC-009 claim does not hold

**Affects:** Status-transition matrix rows 298–300 and 306; SPEC-009 "Background probe request" (line 457); ASM-TE012-08; T-TE012-17 (line 560); `contracts/backend-apis.json` `readiness_writer`.

**Evidence**
- Matrix row 306 limits the background request to state **READY** ("READY | A `store()` or `open()` operation ends in `TIMEOUT` …"). SPEC-009, ASM-TE012-08 ("Effect if wrong": "until the next store or failing operation after the window") and the contract apply it in any flag-on state: "unless one is in flight or one ended less than `readiness-recheck-seconds` before". In state NOT_READY, an `open()` (not gated) that fails with `TIMEOUT` therefore requests a probe under SPEC-009 but not under the matrix.
- SPEC-009: "During an outage the first failing operation therefore leads, within `timeout-seconds`, to NOT_READY and `documentHub` `DOWN`". Under the suppression rule this is false when a probe ended within the window. Example: the start probe ends READY at t = 0 and storage fails at t = 5 s. Every operation until t = 30 s raises `TIMEOUT` and requests no probe, so `documentHub` stays `UP` for up to `readiness-recheck-seconds` + `timeout-seconds` (40 s). The behaviour is acceptable, because the suppression comes from the triage requirement that reuse applies only to probe results. The stated bound is wrong.
- T-TE012-17 "READY then a `store()` ending in `TIMEOUT` → … exactly one background probe is requested" does not state the clock precondition (last probe older than the window). No test covers the suppression branch: a failure within the window after a READY probe requests no probe.
- The matrix has no row for a probe that ends READY while the state is READY (`checkedAt` refreshed). Rows 298 and 300 cover only NOT_EVALUATED → READY and NOT_READY → READY.

**Required fix:** Make matrix row 306 "any flag-on state", or say in SPEC-009 that it applies only in READY, and make the two agree. Add a row "READY | Probe ends | All checks pass | READY (`checkedAt` = probe end)". Correct the SPEC-009 sentence to "within `readiness-recheck-seconds` + `timeout-seconds` at most". In T-TE012-17, state the clock precondition and add the suppression case.

### REVIEW-RWB-TE-012-SG-35: Low. The PROD apply procedure does not fix the deployment mode, and the pre-deploy check cannot see the first-apply override (residual of SG-28)

**Affects:** SPEC-004 "Later PROD applies after the lock" table (lines 409–418); SPEC-001 pre-deploy check (line 381); ASM-TE012-33; `RUNBOOK.md` content; DGAP-03 "How this stage proceeded".

**Evidence**
- Deployment mode. SPEC-001 and SPEC-004 say the policy is protected because the resource "is skipped" when `deployLegalPolicy=false`, and the apply is `az deployment group create`. Microsoft Learn, "Conditional deployment with templates", section "Complete mode", says a resource whose condition is false "is deleted" in complete mode (REST API 2019-05-10 or later and current Azure CLI). The spec names no mode, and neither the runbook content nor the pre-deploy check forbids `--mode Complete`. In complete mode, a later PROD apply would try to delete the locked policy (refused by Azure, so the apply fails). In UAT, a `false` value would delete the unlocked policy. ASM-TE012-33 "Effect if wrong" ("if it shows a skipped resource is removed") depends on the mode and does not name it.
- Override visibility. SPEC-004: "First PROD apply | Run once with the override `deployLegalPolicy=true` … Pre-deploy check: in PROD, `deployLegalPolicy=true` is accepted only when … no policy". SPEC-001 says the check reads the environment parameter file, where PROD holds `false` (T-TE012-15). The override is given on the deploy command line, so as specified the check never sees `true` and cannot apply the guard. The irreversible-path control is therefore unenforced.
- Spike scope. DGAP-03 v5 says the DEV spike also "runs the runbook 'Extend' step on a disposable account". The extend operation acts on a locked policy, so the spike needs a lock in DEV, while SPEC-004 says the lock is "Never | Run in DEV, SIT or UAT". SPEC-004 line 418 describes a smaller spike scope with no extend. The two are inconsistent.

**Required fix:** In SPEC-004 and the `RUNBOOK.md` content, fix incremental mode for every apply (`--mode Incremental`), and have the pre-deploy check refuse any other mode. Pass the `deployLegalPolicy` value to `Test-DeployParameters.ps1` as an argument, and have the runbook pass the same value to the deploy command, so that the check sees the effective value. Add the matching Builder-evidence case: PROD with `true` while a policy exists is refused. Align the spike scope in DGAP-03 and SPEC-004. If the extend step is in the spike, state that the lock is made only on a disposable account with an empty container, outside the environment's account, and that this is not the "Never" case. Otherwise remove extend from DGAP-03.

### REVIEW-RWB-TE-012-SG-36: Low. Scope and metadata lines not updated for the v5 additions

**Affects:** Change Scope Declaration "New Nodes Required" (line 134); ASM-TE012-03 (spec line 106 and `assumptions.md`); `shared-updates.md` §1 row 007 status column.

**Evidence**
- Line 134 lists "ARM JSON template, four JSON parameter files and `RUNBOOK.md` with the PROD lock step". v5 adds three new nodes in `infra/azure/document-storage/`: `azuredeploy.parameters.schema.json`, `azuredeploy.local.parameters.json` and `Test-DeployParameters.ps1` (SPEC-001). The section that the gate rules require to name every new node does not list them, so the Planner could leave them out of the file list.
- ASM-TE012-03 still says "one JSON parameter file per environment". The local and schema files are not mentioned.
- `shared-updates.md` §1 row 007: the SPEC column now says "`spec.md` v5", but the status column still says "Specified — spec v4 18 Nov 2026; spec gate round 4 in `review/spec-gate-review-4.md` (rounds 1–3 FAIL …)".

**Required fix:** Add the three files to "New Nodes Required". Extend ASM-TE012-03 to the schema list and local file. Update the row-007 status to "spec v5; spec gate round 5 in `review/spec-gate-review-5.md` (rounds 1–4 FAIL, all answered in `gate-response.md`)".

## 4. Requirement and control checks

| Check | Result |
|---|---|
| Authentication and authorization | No endpoint (story §12). Managed identity only; container-scope roles; `open()` is not an authorization point. Pass |
| Customer data protection | UUID blob names; `sha256` metadata only; IDs-only logs; synthetic test data and generated keys; new parameter values are synthetic. Pass |
| Audit of sensitive actions | `DOCUMENT_CHANGE_REFUSED` (T-TE012-10); direct attempts DGAP-11. Pass |
| KYC, AML, suitability, consent | Not in scope |
| Frontend integration versioning and error contract | `UI In Scope: NO`, `NO_API_CHANGE`; `BLOB_MISSING` added to the published `Reason` enum and the contract; the 503 MSG-GEN-006 mapping is a seam with the standard's silence stated. Pass |
| Secrets and environment configuration | Five-condition emulator guard unchanged; no committed key; template inputs are object IDs and subnet IDs (not secrets), with placeholders refused before deploy. Pass |
| Feature flag off path (AGENTS §3.13) | Unchanged; no background probe when the flag is off. Pass |
| Write-once control (CTL-12, NFR-029, BR1) | Policy in the template; PROD lock runbook step; later PROD applies skip the policy (SG-28). Deployment mode and the override check are not fixed (SG-35) |
| AC timing (AC10) | Bounded single-flight probe and caller wait, unchanged. Pass |
| Availability of the write path | A per-operation fault no longer blocks stores or turns the root health 503 (SG-26 fixed, T-TE012-18). Rule wording: SG-33, SG-34 |
| Test coverage and evidence | Frontend `NOT_APPLICABLE` correct. Backend four-counter gate, per-class rule and no-drop rule cover T-TE012-01 to -13, -17, -18; Azurite IT evidence planned; T-TE012-15 passes at merge without undecided values. Gaps: SG-34 (suppression branch untested) |
| Module boundaries | RWB-TE-001 v4 map; no Azure type in `dochub.api`; `ReadinessProbe` in `dochub.storage`. Pass |
| Migration rule (D-RUN-07) | No migration. Pass |
| Dependencies (D-RUN-08, AGENTS §4.4) | None added (PowerShell already used; Jackson on the test classpath; no JSON-schema library). Pass |
| Traceability and status lines | 37 rows; counts correct; status lines consistent. Stale row-007 status and scope list: SG-36 |
| Shared and document-set files | Untouched. Pass |

## 5. Document gaps

No new review-level gap (no `TE012-SG5-DG-nn` row).
- The missing message for a stored file whose blob is missing is recorded as an assumption, ASM-TE012-15. The standard is silent, and RWB-E1-024 v1 §12 gives 503 MSG-GEN-006 as its only storage-failure response, so the caller story can map the reason. This is a seam, not a gap that blocks or changes this story.
- SG-35 concerns Azure Resource Manager behaviour, not a silence in the document set.
- The specifier's decision to record no gap for subnet and object IDs was checked: Environment and Deployment Design v4 §3 names "Private endpoints to storage and the database" but, as expected for a design document, no environment identifiers. The open items are the right vehicle. DGAP-05, -07 and -13 were re-read; they are cited correctly with Blocker = No.

Specifier rows changed in v5:
- **DGAP-03** "How this stage proceeded": the extended spike scope is noted. Its extend step conflicts with SPEC-004 (see SG-35). The gap itself and Blocker = No are unchanged and correct.
- **DGAP-24** "How this stage proceeded": the conditional-policy rule is added with the `[AZ-IMM]` citation (verified). Blocker = No correct.

DGAP-01 to -17 and -19 to -24 stay accepted. DGAP-18 stays withdrawn. 0 blockers.

## 6. Gate result

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 4]
BLOCKING: No Critical, High or Medium finding. FAIL because Low findings exist: SG-33 (checkedAt definition contradicts probe-only rule), SG-34 (background-probe rule wording, a false detection bound, suppression branch untested), SG-35 (deployment mode not fixed; pre-deploy check cannot see the first-PROD override; spike scope inconsistent), SG-36 (new nodes and row-007 status stale). Under D-RUN-09 these are fixed in the same pass. Round 4: SG-27, SG-29, SG-30, SG-31, SG-32 FIXED; SG-26 PARTIAL (residual SG-33); SG-28 PARTIAL (residual SG-35).
DOCUMENT_GAPS: 0 new review-level gaps; 0 blockers. DGAP-03 and DGAP-24 v5 updates checked; DGAP-05, -07, -13 re-confirmed (Blocker = No).
NEXT_STEP: The orchestrator (Claude Code) triages: either the Technical Specifier issues spec v6 for SG-33 to SG-36 and the gate is re-run as review/spec-gate-review-6.md, or the Low-only handling in aisdlc/.github/rules/pdlc.md applies. No human acceptance is recorded.
```

SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 4]

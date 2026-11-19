# Spec gate review, round 6: RWB-TE-012, document storage containers

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-012-SG6` (new findings `REVIEW-RWB-TE-012-SG-37` and `-38`) |
| RUN_ID | `INC-007-epic-1-RWB-TE-012` |
| Artifact | `aisdlc/output/INC-007-epic-1-RWB-TE-012/specify/`: `spec.md` v6, `assumptions.md` v6, `document-gaps.md` v6, `shared-updates.md` v6, `compliance-validation.md` v6, `gate-response.md` (section "Round 5"), `contracts/backend-apis.json` (unchanged since v5), `contracts/frontend-integrations.json` (unchanged), `agent-run-log.md` |
| Previous rounds | `review/spec-gate-review.md` (round 1: FAIL, 0C/1H/5M/5L); `-2.md` (round 2: FAIL, 0C/0H/2M/4L); `-3.md` (round 3: FAIL, 0C/0H/1M/7L); `-4.md` (round 4: FAIL, 0C/0H/2M/5L); `-5.md` (round 5: FAIL, 0C/0H/0M/4L) |
| Reviewer | Compliance Reviewer (spec gate), `.claude/agents/compliance-reviewer.md` |
| Date | 2026-11-18 |
| **Status** | **FAIL** |
| Findings | 0 Critical, 0 High, 0 Medium, 2 Low (2 new). Round 5: SG-33, SG-34, SG-35, SG-36 FIXED. Round-4 residuals SG-26 and SG-28 now fully closed |
| Handoff | No Critical, High or Medium finding remains. The gate result is still FAIL because Low findings exist. Whether a further round runs, or the Low-only handling in `aisdlc/.github/rules/pdlc.md` applies, is the orchestrator's triage. No human acceptance is recorded |

## 1. What was checked

**Inputs read.**
- All specify files listed above, diffed against `*.run5.*` (spec, assumptions, document-gaps, shared-updates, compliance-validation, gate-response, agent-run-log, both contracts). The v5→v6 spec diff is small: revision lines, `[AZ-COND]` source row, ASM-TE012-03 short form, New Nodes Required, `checkedAt` detail, two matrix rows, the pre-deploy check paragraph, the two SPEC-004 later-apply rows and spike paragraph, the SPEC-009 background-request bullet, T-TE012-17, and the status lines. `gate-response.md` Round 5 was checked claim by claim against the files, not taken as evidence.
- Round 5 review `review/spec-gate-review-5.md` (SG-33 to SG-36 and the partial verdicts on SG-26 and SG-28).
- Document set, read only, hashes checked against `aisdlc/evidence/document-set-baseline.sha256`: RWB-TE-012 story file v1 (§4, BR1, §10 Authority, §13), RWB-E1-024 v1, Error and Message Standard v4, Error Handling and Resilience Standard v3, Environment and Deployment Design v4, Decision Log v10. All six match the baseline. No file under `requirement/legacy/` is newer than the round-5 review.
- External citations, checked on Microsoft Learn:
  - `[AZ-COND]` "Conditional deployment with templates" (ms.date 26 June 2026, as cited), section "Complete mode". The citation is verified for complete mode (SG-35). The incremental-mode claim made under the same citation is checked in SG-38.
  - "Deployment modes" (ARM, ms.date 26 June 2026), sections "Incremental mode" and "Complete mode". Not cited by the spec; read for SG-38.
- Rules: `specification-execution-gates.md`; compliance-reviewer agent definition; `AGENTS.md`; `CLAUDE.md`.

**Governance checks.** No shared file was modified after round 5: `Traceability_Matrix.md` 04:57, `open-items.md` 04:56, `DOCUMENT-GAPS.md` 00:33, `README.md` 17 Nov. The round-5 review was written at 05:23. No `infra/azure/` folder exists, so no code was written. `agent-run-log.md` run 5 says "No git run, no code edited, no document-set file changed, no shared file changed". No credential, key or personal data was added. v6 adds no value except Azure CLI command names. No new dependency: the check is PowerShell, as `scripts/dev.ps1` is.

**Counts verified.** 37 coverage rows (37 COVERED); 26 CLAR rows; 33 assumption rows (`ASM-TE012-01` to `-33`); 24 DGAP rows (23 active, DGAP-18 withdrawn); 18 open items in `shared-updates.md` §3. These match `compliance-validation.md`. Both contract files parse as JSON.

## 2. Verification of round-5 findings

| Finding | Severity | Result | Evidence in v6 |
|---|---|---|---|
| SG-33 `checkedAt` detail | Low | **FIXED** | Health detail (line 287): "UTC instant the last probe ended (absent when never evaluated); an operation's outcome never sets it (SPEC-009)". This matches matrix rows 300 and 302 ("`checkedAt` = probe end"), SPEC-009 "Only the probe writes readiness", the contract's `readiness_writer`, and T-TE012-18 ("`checkedAt` unchanged"). No other text says an operation sets NOT_READY or `checkedAt` (grep of spec, assumptions and contract) |
| SG-34 background-probe scope, bound, test, READY → READY | Low | **FIXED** | **Scope.** Matrix row 308 now applies in "any (NOT_EVALUATED, READY or NOT_READY)" state, with "otherwise none (suppressed)". SPEC-009: "The same rule applies in every state". ASM-TE012-08 (assumptions): "in any state, unless a probe is in flight or ended within `readiness-recheck-seconds`". The contract `readiness_writer` puts no state restriction on the request, only the in-flight and window suppression, so all four agree. **Bound.** SPEC-009 now says "within `readiness-recheck-seconds` + `timeout-seconds` (40 s with the defaults) of the first failing operation", and "within `timeout-seconds` when no probe ended in the window". Checked against the round-5 example: probe READY at t = 0, first failure ends at t ≈ 0⁺, failures continue, the first failure ending at t ≥ 30 requests a probe, and the probe ends by t = 40. The bound holds when measured from the end of the first failing operation (the matrix event is "operation ends in"), under the stated precondition "while operations keep failing". **Test.** T-TE012-17 states the clock precondition ("last probe ended more than `readiness-recheck-seconds` before on the controllable clock"). It adds **Suppression**: a probe within the window, then `open()` with `UNAVAILABLE` → no probe and state READY; after the window, the next failure → exactly one probe, ending NOT_READY. It also adds "A background probe that ends with all checks passing → READY with `checkedAt` updated". **Row.** Matrix line 302 "READY / Probe ends / All checks pass / READY (`checkedAt` = probe end)" |
| SG-35 deployment mode, effective override, spike scope | Low | **FIXED** (citation precision residual SG-38; new check-input gap SG-37) | **Mode.** SPEC-001 says the pre-deploy check "exits non-zero … when … the mode is not `Incremental`", and that it prints `az deployment group create --mode Incremental`. SPEC-004 later-apply row: "mode `Incremental`: the policy resource is skipped and, in incremental mode, not deleted". ASM-TE012-32 and -33 and open item OPEN-`<next>` (pre-deploy check) agree. Builder evidence: "refuses mode `Complete`". The `[AZ-COND]` "Complete mode" citation is verified (ms.date 26 June 2026): with API version 2019-05-10 or later, and with current Azure CLI and PowerShell, complete mode deletes a resource whose condition is false. **Effective value.** The check "takes … the effective `deployLegalPolicy` value (the file value, or the one-time override for the first PROD apply)" and prints the one command that "step 2 runs unchanged … `deployLegalPolicy` set to the same effective value, so the value checked is the value applied". SPEC-004 first-PROD row matches. Builder evidence adds the PROD refusal when a policy exists. **Spike.** DGAP-03 now says: on a disposable account, apply with `deployLegalPolicy=true` then `false` in incremental mode, then check that the unlocked policy is unchanged; "the lock and the 'Extend' step are never run outside PROD". SPEC-004 line 420, ASM-TE012-33 and `compliance-validation.md` §3 say the same. SPEC-004 "Never: Run in DEV, SIT or UAT" is now consistent |
| SG-36 stale scope and metadata | Low | **FIXED** | New Nodes Required (line 135) lists `azuredeploy.json`, the four environment files, `azuredeploy.parameters.schema.json`, `azuredeploy.local.parameters.json` (T-TE012-15 only), `Test-DeployParameters.ps1` and `RUNBOOK.md` with the Apply, PROD lock and Extend steps. ASM-TE012-03 is updated in the spec (line 107) and in `assumptions.md` (line 9) to name the four environment files, the required-input list and the local file. `shared-updates.md` §1 row 007 status: "Specified — spec v6 18 Nov 2026; spec gate round 6 in `review/spec-gate-review-6.md` (rounds 1–5 FAIL, all answered in `gate-response.md`)" |

**Round-4 requirements re-confirmed in v6.**

| Requirement | Holds | Evidence |
|---|---|---|
| Only the probe writes readiness | Yes | Matrix intro (line 293), SPEC-009 first bullet, SPEC-013 "The mapper never writes readiness", SPEC-015, contract `readiness_writer` |
| Per-operation outcomes, such as a missing blob, never change readiness | Yes | Matrix row 309; SPEC-013 `BlobNotFound` → `BLOB_MISSING`, no probe; T-TE012-18 (`documentHub` stays `UP`, root 200, zero probes); contract `per_operation_outcome` |
| Template unit test needs no undecided value | Yes | SPEC-001 "never needs an undecided value, so it passes in `test` at merge"; T-TE012-15 checks only presence and shape (value or exactly `__SET_BEFORE_APPLY__`) in the environment files |
| Placeholders refused by a pre-deploy check, with owner and place | Yes | SPEC-001: `Test-DeployParameters.ps1`, step 1 of the `RUNBOOK.md` Apply procedure in every environment, run by RW-PLATADM (`[S]` §10, verified), maintained by the platform team; open item with owner and needed-by |
| Later PROD applies never change the locked policy | Yes | SPEC-004: PROD file `false`, incremental mode only, policy resource skipped and not deleted; period changes only through "Extend"; T-TE012-15 asserts the condition and per-file values |

## 3. New findings

### REVIEW-RWB-TE-012-SG-37: Low. The pre-deploy check's inputs do not name the deployment target, and the result of `show` before the first PROD apply is not defined

**Affects:** SPEC-001 "pre-deploy check" paragraph (line 383); SPEC-004 "First PROD apply" row (line 415); ASM-TE012-32; `RUNBOOK.md` content; Builder evidence for the check.

**Evidence**
- Target not named. v6 sets the check's inputs: it "takes the environment, the parameter file, the deployment mode and the effective `deployLegalPolicy` value". The check then (a) runs `az storage container immutability-policy show` on `rwb-docs-legal`, and (b) prints "the one deploy command step 2 runs unchanged: `az deployment group create --mode Incremental` with that parameter file and `deployLegalPolicy`". Both need a target. `show` needs the storage account name and resource group. `az deployment group create` needs `--resource-group` and the template file. None of these is an input of the check. The storage account name is not in the required-input list either (`location`, `skuName`, `accessTier`, `privateEndpointSubnetId`, `aceServicePrincipalId`, `ocrPrincipalId`, `deployLegalPolicy`), and no part of the spec says how the template names the account (a parameter with a default, or a derived name). As specified, the printed command cannot run "unchanged", and the PROD policy check has no account to query.
- First-apply outcome not defined. The PROD guard accepts an effective `true` "only when `az storage container immutability-policy show` finds no policy on `rwb-docs-legal`". Before the first PROD apply the container, and possibly the account, does not exist yet, so `show` ends in a not-found error rather than "no policy". The spec does not say which `show` results count as "no policy" (account or container not found, container without a policy) and which make the check refuse (an access, subscription or network error). If the check fails closed on every error, the first PROD apply can never pass. If it fails open on every error, a wrong subscription context lets `true` through. The Builder evidence covers only the refusal case (a policy exists). It has no accept case for a first PROD apply.
- Impact is limited. Azure acts on an unlocked policy only (`[AZ-REST]`), so a wrongly accepted `true` after the lock would make the apply fail rather than change the locked policy. That is why this finding is Low.

**Required fix:** In SPEC-001 and ASM-TE012-32, add the resource group and storage account name to the check's inputs, or say where the check reads them, for example a template parameter listed in the schema. Have the printed command include `--resource-group` and `--template-file`. Say how the template names the account. Define the `show` outcomes: account or container not found, or no policy, means no policy, so accept; a policy in any state means refuse; any other error means refuse. Add the Builder-evidence case: a first PROD-style run with effective `deployLegalPolicy=true` against an account with no legal container is accepted.

### REVIEW-RWB-TE-012-SG-38: Low. The incremental-mode claim cites a section that covers complete mode only, and the self-check's source list leaves out `[AZ-COND]`

**Affects:** SPEC-004 "Every later PROD apply" row (line 416); "Sources cited" (line 32); ASM-TE012-33 (assumptions); `compliance-validation.md` §2 row 1.

**Evidence**
- SPEC-004 line 416 says the skipped policy resource is "in incremental mode, not deleted (`[AZ-COND]`)". `[AZ-COND]` is defined as the "Complete mode" section of "Conditional deployment with templates". That section describes complete mode only: whether a resource with a false condition is deleted depends on the REST API version, and current CLI and PowerShell delete it. It says nothing about incremental mode.
- The incremental behaviour is stated on another Microsoft Learn page, "Deployment modes" (ARM, ms.date 26 June 2026), section "Incremental mode": Resource Manager "leaves unchanged resources that exist in the resource group but aren't specified". So the claim is correct and the DGAP-03 spike confirms it (ASM-TE012-33), but the cited source does not support it.
- `compliance-validation.md` §2 "Every statement cites a source …" names only `[AZ-IMM]` and `[AZ-REST]` as external sources. Row "Later PROD applies" in the same table lists `[AZ-COND]`.

**Required fix:** Add a source row for "Deployment modes", section "Incremental mode" (for example `[AZ-MODES]`). Cite it for the incremental clause in SPEC-004 and ASM-TE012-33, and keep `[AZ-COND]` for the complete-mode deletion. Add `[AZ-COND]`, and `[AZ-MODES]` if introduced, to the `compliance-validation.md` §2 source row.

## 4. Requirement and control checks

| Check | Result |
|---|---|
| Authentication and authorization | No endpoint (story §12). Managed identity only; container-scope roles; `open()` is not an authorization point. Pass |
| Customer data protection | UUID blob names; `sha256` metadata only; IDs-only logs; synthetic test data and generated keys. No new values in v6. Pass |
| Audit of sensitive actions | `DOCUMENT_CHANGE_REFUSED` (T-TE012-10); direct attempts DGAP-11. Pass |
| KYC, AML, suitability, consent | Not in scope |
| Frontend integration versioning and error contract | `UI In Scope: NO`, `NO_API_CHANGE`; contract unchanged and consistent with the v6 background-probe rule. Pass |
| Secrets and environment configuration | Emulator guard unchanged; no committed key; placeholders refused before deploy. Check target inputs not defined: SG-37 |
| Feature flag off path (AGENTS §3.13) | Unchanged. Pass |
| Write-once control (CTL-12, NFR-029, BR1) | Policy in the template; PROD lock and Extend runbook steps only in PROD; incremental mode enforced; effective override checked and applied by one command. Residuals: SG-37 (check target and first-apply outcome), SG-38 (citation) |
| AC timing (AC10) | Bounded single-flight probe and caller wait, unchanged. Pass |
| Availability and health signal | Probe-only writer; background request in every state; detection bound stated and correct (SG-34 fixed). Pass |
| Test coverage and evidence | Frontend `NOT_APPLICABLE` correct. Backend four-counter gate, per-class and no-drop rules cover T-TE012-01 to -13, -17, -18. T-TE012-17 now covers the suppression branch and READY → READY. Pre-deploy check Builder evidence lacks the first-apply accept case (SG-37) |
| Module boundaries | Unchanged; RWB-TE-001 v4 map. Pass |
| Migration rule (D-RUN-07) | No migration. Pass |
| Dependencies (D-RUN-08, AGENTS §4.4) | None added. Pass |
| Traceability and status lines | 37 rows; counts correct; row-007 status current; status lines name round 6. Pass |
| Shared and document-set files | Untouched (times and baseline hashes checked). Pass |

## 5. Document gaps

No new review-level gap (no `TE012-SG6-DG-nn` row).
- SG-37 and SG-38 are about how the spec defines the check and cites Azure Resource Manager behaviour. Neither is a silence or a contradiction in the document set. The storage account name and resource group are environment facts, like the subnet and object IDs, which round 5 confirmed the document set is not expected to hold.
- Specifier row changed in v6: **DGAP-03** "How this stage proceeded" now scopes the spike to an incremental-mode apply on a disposable account, with no lock and no Extend outside PROD. This is consistent with SPEC-004 and `[S]` BR1 ("unlocked in DEV, SIT and UAT so test data can be removed", verified). Blocker = No is correct.
- DGAP-24 still describes the v5 later-apply rule without the mode. The statement is still true and the mode is in SPEC-004, so this is not a finding.

DGAP-01 to -17 and -19 to -24 stay accepted. DGAP-18 stays withdrawn. 0 blockers.

## 6. Gate result

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]
BLOCKING: No Critical, High or Medium finding. FAIL because Low findings exist: SG-37 (the pre-deploy check's inputs do not name the resource group or storage account it queries and deploys to, and the first-PROD-apply `show` result is not defined), SG-38 (the incremental-mode claim cites the complete-mode section; the self-check's source list leaves out [AZ-COND]). Round 5: SG-33, SG-34, SG-35, SG-36 FIXED; round-4 SG-26 and SG-28 residuals closed.
DOCUMENT_GAPS: 0 new review-level gaps; 0 blockers. DGAP-03 v6 update checked and consistent with SPEC-004 and BR1.
NEXT_STEP: The orchestrator (Claude Code) triages: either the Technical Specifier issues spec v7 for SG-37 and SG-38 and the gate is re-run as review/spec-gate-review-7.md, or the Low-only handling in aisdlc/.github/rules/pdlc.md applies. No human acceptance is recorded.
```

SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]

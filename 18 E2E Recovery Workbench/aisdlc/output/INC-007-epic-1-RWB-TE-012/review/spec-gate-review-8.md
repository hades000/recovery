# Spec gate review, round 8: RWB-TE-012, document storage containers

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-012-SG8` (new findings `REVIEW-RWB-TE-012-SG-41` and `-42`) |
| RUN_ID | `INC-007-epic-1-RWB-TE-012` |
| Artifact | `aisdlc/output/INC-007-epic-1-RWB-TE-012/specify/`: `spec.md` v8, `assumptions.md` v8, `document-gaps.md` v8, `shared-updates.md` v8, `compliance-validation.md` v8, `gate-response.md` (section "Round 7"), `contracts/backend-apis.json` (unchanged since v5), `contracts/frontend-integrations.json` (unchanged), `agent-run-log.md` |
| Previous rounds | `review/spec-gate-review.md` (round 1: FAIL, 0C/1H/5M/5L); `-2.md` (round 2: FAIL, 0C/0H/2M/4L); `-3.md` (round 3: FAIL, 0C/0H/1M/7L); `-4.md` (round 4: FAIL, 0C/0H/2M/5L); `-5.md` (round 5: FAIL, 0C/0H/0M/4L); `-6.md` (round 6: FAIL, 0C/0H/0M/2L); `-7.md` (round 7: FAIL, 0C/0H/0M/2L) |
| Reviewer | Compliance Reviewer (spec gate) |
| Date | 2026-11-18 |
| **Status** | **FAIL** |
| Findings | 0 Critical, 0 High, 0 Medium, 2 Low (2 new). Round 7: SG-39 FIXED, SG-40 FIXED |
| Handoff | No Critical, High or Medium finding remains. The gate result is FAIL because Low findings exist. Whether a further round runs, or the Low-only handling in `aisdlc/.github/rules/pdlc.md` applies, is the orchestrator's triage. No human acceptance is recorded |

Severity scale (as in rounds 1–7): Critical, High and Medium block the next stage until fixed and re-reviewed. Low is a spec defect with limited impact: it is reported, it makes the gate FAIL, and it does not by itself block the handoff (`pdlc.md` Low-only handling).

## 1. What was checked

**Inputs read.**
- All specify files listed above, diffed against `*.run7.*`. The v7→v8 spec diff covers:
  - the revision and spec-gate lines;
  - the pre-deploy check paragraph (new refusal: `-Environment` not equal to the `<env>` in `azuredeploy.<env>.parameters.json`);
  - the "no policy" lead-in (legal container name `<legal>` read from the parameter file or the template `defaultValue`, printed, and used by the lock and "Extend" steps; separate input shapes for `storageAccountName` and the resource group);
  - table rows 1, 2 and 5;
  - the new paragraph labelling the row-1 and row-2 output shapes an assumption;
  - the Builder evidence (row-3 accept case, environment/file mismatch refusal);
  - the SPEC-004 lock, evidence and "Extend" rows;
  - the status block.
- Other diffs: ASM-TE012-32 (v8 sentence); `shared-updates.md` row 007 and the account and resource group open item; `compliance-validation.md` round lines and the "Later PROD applies" row; the `document-gaps.md` revision note; `agent-run-log.md` run 7. Both contracts are byte-identical to `*.run7.json`.
- I checked the claims in `gate-response.md` Round 7 against the files and did not take them as evidence.
- Round 7 review `review/spec-gate-review-7.md` (SG-39, SG-40).
- Document set, read only. All 1,257 `17 AI-First SDLC Repository v2/requirement/legacy/` entries in `aisdlc/evidence/document-set-baseline.sha256` match (`sha256sum -c`, no mismatch). No file under `requirement/legacy/` is newer than the round-7 review.
- External citations, each read live on Microsoft Learn on 2026-11-18 (§2 table).
- Rules: `aisdlc/.github/rules/specification-execution-gates.md`; `aisdlc/.github/agents/reviewer.agent.md`; `aisdlc/.github/rules/pdlc.md` (Low-only handling); `AGENTS.md`; `CLAUDE.md`.

**Governance checks.** These shared files were not changed by this run:
- `Traceability_Matrix.md`: 04:57.
- `DOCUMENT-GAPS.md`: 00:33.
- `docs/open-items.md`: 05:37, the same write noted in round 7, still with no `RWB-TE-012` or `INC-007` row.
- `README.md`: 17 Nov.

Every file in the repository newer than the round-7 review is either in this run's `specify/` folder or in the folders of other runs (`INC-003`, `INC-008`), which are separate stories running in parallel.

Other governance results:
- No `infra/azure/` folder exists, so no code was written.
- `agent-run-log.md` run 7: "No git run, no code edited, no document-set file changed, no shared file changed".
- v8 adds no credential, key, token or personal data. The only literals added are environment names, a file-name pattern and a length range.
- No new dependency (PowerShell and Azure CLI, as before).

**Counts verified.** All of these match `compliance-validation.md` v8:
- 37 coverage rows, all 37 COVERED.
- 26 CLAR rows.
- 33 assumption rows (`ASM-TE012-01` to `-33`).
- 24 DGAP rows: 23 active, DGAP-18 withdrawn.
- 19 open items in `shared-updates.md` §3.

Both contract files parse as JSON.

## 2. Verification of round-7 findings

| Finding | Severity | Result | Evidence in v8 |
|---|---|---|---|
| SG-39 "no policy" output shapes and row-3 evidence | Low | **FIXED** (residual on shape completeness: SG-41) | **Rows 1 and 2 labelled as assumptions.** Row 1 now reads "output shape assumed, ASM-TE012-32" and row 2 reads "`[AZ-CLI-CRM]` 'exists' (output shape assumed, ASM-TE012-32)" (lines 394–395). Line 400 states that the shapes are "not stated on the cited reference pages", that the Builder evidence confirms them before the first SIT apply, and that "any other output falls under row 5 and is refused, so a wrong assumption can only refuse an apply". ASM-TE012-32 in `assumptions.md` carries the same text. **Other output refused.** Row 5 (line 398) now includes "returns any output other than the exact shapes in rows 1–4". **Row-3 accept case.** The Builder evidence (line 404) accepts the case where "the template has been applied once with `deployLegalPolicy=false` so the legal container exists with `hasImmutabilityPolicy` false (row 3)", and checks the printed `<legal>` and command. The live check confirms the label is correct: neither page documents the output (table below). The fix takes the second option the round-7 review offered. One gap remains: the set of "exact shapes" leaves out the account-exists output, which rows 2 and 3 depend on. See SG-41 |
| SG-40 PROD guard input binding | Low | **FIXED** (residual on verifying the legal-container read: SG-42) | **(1) Environment bound to the file.** The check exits non-zero when "`-Environment` (one of `dev`, `sit`, `uat`, `prod`) does not equal the `<env>` in the parameter file name `azuredeploy.<env>.parameters.json`" (line 388). The Builder evidence refuses "`-Environment dev` with the PROD file". The local file (`<env>` = `local`) is outside the allowed set. The binding is by file name, which the round-7 fix allowed. A renamed PROD file would still pass, but the existing rule that `-StorageAccountName` must equal the file's `storageAccountName` ties any run to that file's account. **(2) Legal container name not a literal.** `<legal>` is "the value of the legal container parameter in the parameter file, or, when the file does not set it, the template's `defaultValue` (`rwb-docs-legal`)". It is used in row 2 (`--name <legal>`), row 3, the PROD lock ("the name the pre-deploy check printed"), the evidence step and "Extend" (lines 390, 395, 424, 429, 438). The read and the deploy use the same file, so the container the check reads is the one the template targets. **(3) Shapes stated separately.** `storageAccountName` `^[a-z0-9]{3,24}$` (`[AZ-GET]` `accountName`); resource group "1–90 characters (`[AZ-GET]` `resourceGroupName`)" (line 390). The `shared-updates.md` §3 open item now gives the two shapes separately. Each part of the required fix is met. The read-from-file branch has no evidence case, and the spec never names the parameter. See SG-42 |

**Live check of each Microsoft Learn citation (2026-11-18).**

| Short name | Page | Live result | Claim the spec makes | Supported? |
|---|---|---|---|---|
| `[AZ-IMM]` | "Immutable storage for blob data overview" | ms.date 18 August 2026, as cited. "Locked versus unlocked policies": a locked time-based policy cannot be deleted; its period can be extended, not decreased; at most five increases for a container-level locked policy | Later applies cannot change the locked policy; "Extend" only, at most five times | Yes |
| `[AZ-MODES]` | "Deployment modes" (ARM) | ms.date 26 June 2026, as cited. Incremental mode "leaves unchanged" resources that exist but are not in the template. In complete mode, a condition-false resource is deleted with REST 2019-05-10 or later and with current CLI and PowerShell | Incremental required; complete deletes | Yes (unchanged from round 7) |
| `[AZ-COND]` | "Conditional deployment with templates" | ms.date 26 June 2026, as cited. When the condition is false, "the resource isn't created". The "Complete mode" section matches | Policy resource not created when `deployLegalPolicy` is false | Yes |
| `[AZ-GET]` | REST "Blob Containers - Get", api-version 2026-09-01 | ms.date 23 October 2026, as cited. `accountName`: 3–24, `^[a-z0-9]+$`. `resourceGroupName`: minLength 1, maxLength 90, no pattern on this page. `containerName`: 3–63. The `hasImmutabilityPolicy` text matches | Account shape; resource group "1–90 characters"; row-3 quotation | Yes. The resource group claim is new in v8 and matches the page exactly |
| `[AZ-CLI-CRM]` | Azure CLI "az storage container-rm" | ms.date 9 November 2026, as cited. `exists`: "Check for the existence of a container."; no output sample or field documented. `show` is listed; the global `--output` default is `json` | Commands and arguments exist; output shape is an assumption | Yes. v8 no longer claims the page documents `"exists": false` |
| Azure CLI `az storage account` (row 1; not a short name) | Azure CLI "az storage account" | ms.date 1 September 2026. `list`: "List storage accounts.", `[--resource-group]`, global `--query` (JMESPath). No sample output | The command exists; output shape is an assumption | Yes. Row 1 now cites the command and marks the shape as assumed. It has no `Sources cited` row, which is acceptable because no claim rests on the page's content |
| `[AZ-CLI-IMM]` | Azure CLI "az storage container immutability-policy" | Unchanged since round 7 (verified live then) | `show`, `lock` and `extend` use the ETag | Yes |

**Earlier-round requirements re-confirmed in v8.**

| Requirement | Holds | Evidence |
|---|---|---|
| Only the probe writes readiness | Yes | SPEC-009 line 475 "Only the probe writes readiness"; SPEC-013 line 541 "The mapper never writes readiness"; contract `readiness_writer` (unchanged) |
| Per-operation outcomes never change readiness | Yes | Matrix line 332 (`BLOB_MISSING`: "readiness unchanged, no probe"); SPEC-013; T-TE012-18 (line 584); CLAR-024; contract `per_operation_outcome` |
| Template unit test needs no undecided value | Yes | Line 386; T-TE012-15 (line 581) "needs no undecided value". v8 adds no template input, so the schema list (line 382) is unchanged |
| Placeholders refused by the pre-deploy check, with owner and place | Yes | Line 388 (step 1 of the RUNBOOK Apply procedure, every environment); line 404 (RW-PLATADM runs it, the platform team maintains it); open item with owner and needed-by (`shared-updates.md` §3) |
| Explicit resource group and account inputs | Yes | Six explicit inputs (line 388); account mismatch refused; the printed command carries `--resource-group <rg>` and `@<parameter file>` |
| Observable "no policy" | Yes | Five ordered rows (lines 392–398) that fail closed; row 3 reads the documented `hasImmutabilityPolicy`; row 5 refuses anything else (precision residual SG-41) |
| Later PROD applies never change the locked policy | Yes | SPEC-004 line 437: PROD file `false`, incremental only, policy not created and the existing one left unchanged (`[AZ-COND]`, `[AZ-MODES]`); period changes only by "Extend" on `<legal>` (line 438); T-TE012-15 asserts the condition and per-file values |
| Incremental mode | Yes | Check refuses any other mode; printed command fixes `--mode Incremental`; Builder evidence refuses `Complete` |
| Microsoft Learn citations for locked policies, deployment modes and conditional deployment | Yes | `[AZ-IMM]`, `[AZ-MODES]`, `[AZ-COND]` in Sources cited with page dates matching the live pages (table above) |

## 3. New findings

### REVIEW-RWB-TE-012-SG-41: Low. The "exact shapes" that row 5 accepts leave out the account-exists output, so a literal reading refuses every case in which the account exists

**Affects:** SPEC-001 "no policy" table rows 1, 2 and 5 (lines 394–398) and the shape paragraph (line 400); ASM-TE012-32; Builder evidence (line 404).

**Evidence**
- v8 changes row 5 to refuse any output "other than the exact shapes in rows 1–4". Line 400 lists the assumed shapes for rows 1 and 2 as "`[]` for an empty filtered list; a JSON object with a boolean `exists`". ASM-TE012-32 lists the same two.
- To reach rows 2 and 3, the check first runs the row-1 read (`az storage account list … --query "[?name=='<account>']"`) and gets a non-empty array, meaning the account exists. No row and no assumption states this shape. Row 2 starts with "The account exists" but gives no output for that read.
- A Builder who implements row 5 as written therefore refuses whenever the account exists. That makes the row-2 and row-3 accept paths unreachable. Those are the accept paths the Builder evidence requires on line 404, including the row-3 case added for SG-39. The rule and the evidence contradict each other, and the Builder has to guess which one to follow.
- **Impact is limited.** The error is on the refusing side: a check that refuses too often blocks a first PROD apply but cannot accept one wrongly. The Builder evidence would expose the contradiction before SIT. That is why this is Low.

**Required fix:**
- In SPEC-001 and ASM-TE012-32, add the account-exists output to the assumed shapes: a one-element array whose element's `name` equals `<account>`. This leads to the row-2 read.
- State that `"exists": true` leads to the row-3 read.
- State the row-3 and row-4 shape: an object with a boolean `properties.hasImmutabilityPolicy`. A missing or non-boolean value falls to row 5.
- Keep row 5 as "any other output".

### REVIEW-RWB-TE-012-SG-42: Low. The new read of the legal container name from the parameter file is not specified by parameter name and is never exercised

**Affects:** SPEC-001 "no policy" lead-in (line 390) and Builder evidence (line 404); SPEC-002 (line 410); T-TE012-15 (line 581).

**Evidence**
- v8 reads `<legal>` from "the legal container parameter in the parameter file", falling back to the template `defaultValue`. Neither SPEC-002 ("named by parameters with the defaults …") nor T-TE012-15 names that parameter. T-TE012-15 checks that the `immutabilityPolicies` resource is "on the legal container", but it does not check which parameter names that container or what its default is. The check and the template must agree on the name. No rule or test makes them agree.
- Every Builder evidence case uses "a completed copy of the PROD file", which holds only the schema inputs. The container-name parameters have defaults and are not schema inputs (line 382), so the file-override branch is never run. A check that ignores the file and always uses `rwb-docs-legal` would pass every listed case. That is the SG-40 defect this branch was added to remove.
- The round-7 review offered an alternative to reading the name: forbid the override and assert that in T-TE012-15. v8 took the read option but added no check for it. The other two parts of the SG-40 fix each have an evidence case.
- **Impact is limited.** As in SG-40, Azure refuses changes to a locked policy (`[AZ-REST]`), so a wrong `<legal>` makes a later apply or lock fail rather than change a locked policy. That is why this is Low.

**Required fix:**
- In SPEC-002, name the legal container template parameter (for example `legalContainerName`, default `rwb-docs-legal`). Use that name in SPEC-001 line 390.
- Add a T-TE012-15 assertion: that parameter exists with that default, and the `immutabilityPolicies` resource's parent container is named by it.
- Add a Builder evidence case: a copy of the PROD file that sets the parameter to another name on which the template has already created a policy. The check refuses under row 4 and prints that name as `<legal>`.
- Alternative: state that environment files never set container-name parameters, have the check refuse a file that does, and assert this in T-TE012-15.

## 4. Requirement and control checks

| Check | Result |
|---|---|
| Authentication and authorization | No endpoint (story §12). Managed identity only; container-scope roles. The check runs as RW-PLATADM (`[S]` §10). Pass |
| Customer data protection | UUID blob names; `sha256` metadata only; IDs-only logs; synthetic test data. v8 adds no data values. Pass |
| Audit of sensitive actions | `DOCUMENT_CHANGE_REFUSED` (T-TE012-10); check output (now including `<legal>`) kept with the apply record. Pass |
| KYC, AML, suitability, consent | Not in scope |
| Frontend integration versioning and error contract | `UI In Scope: NO`, `NO_API_CHANGE`; contracts unchanged. Pass |
| Secrets and environment configuration | No committed key; account name and resource group are open items with separate shapes; placeholders refused before deploy; environment bound to the file name. Pass |
| Feature flag off path (AGENTS §3.13) | Unchanged. Pass |
| Write-once control (CTL-12, NFR-029, BR1) | Policy in template; PROD lock and Extend only in PROD on the printed `<legal>`; incremental mode enforced; fail-closed "no policy" decision with explicit target; environment/file binding. Residuals: SG-41 (shape completeness), SG-42 (legal container parameter not named or exercised) |
| AC timing (AC10) | Unchanged. Pass |
| Availability and health signal | Unchanged (probe-only writer). Pass |
| Test coverage and evidence | Frontend `NOT_APPLICABLE` correct. Backend four-counter gate, per-class and no-drop rules unchanged. Pre-deploy Builder evidence now covers rows 1–5, account mismatch, environment/file mismatch, placeholder and `Complete`. It does not cover the `<legal>` file-override branch (SG-42) |
| Module boundaries | Unchanged; RWB-TE-001 v4 map. Pass |
| Migration rule (D-RUN-07) | No migration. Pass |
| Dependencies (D-RUN-08, AGENTS §4.4) | None added. Pass |
| Traceability and status lines | Counts correct. Row-007 status names spec v8 and round 8. Spec `Status: SUCCESS` with `REVIEW_GATE_RESULT: PENDING` follows the earlier pattern before a gate. Pass |
| Shared and document-set files | Document set unchanged (1,257 baseline hashes match). Shared files not changed by this run. Pass |

**Minor editorial notes, not findings.**
- `spec.md` short-form ASM-TE012-32 (line 125) still describes only placeholders. The output-shape assumption that rows 1 and 2 cite is only in `assumptions.md`. ASM-TE012-33 (line 126) still has its v6 wording, which remains true.
- ASM-TE012-32 in `assumptions.md` lists five explicit inputs and leaves out `-Environment`, although its v8 sentence adds a rule on `-Environment` and SPEC-001 lists six.
- Line 390 gives the resource group an "input shape" and also says it is "passed to Azure as given". One sentence saying whether the check enforces the 1–90 length locally would remove the doubt. Either reading is safe, because a wrong name ends in row 5.
- `document-gaps.md` lists its revision notes in the order v5, v8, v7, v6.

## 5. Document gaps

No new review-level gap (no `TE012-SG8-DG-nn` row).
- SG-41 and SG-42 concern how the spec states the check's assumed CLI outputs and how it names and verifies a template parameter. Neither is a silence or contradiction in the document set.
- The v8 `document-gaps.md` note ("the document set has no naming rule for the storage account or resource group") is consistent with my round-7 search, and no document-set file has changed since.
- DGAP-01 to -17 and -19 to -24 stay accepted; DGAP-18 stays withdrawn. 0 blockers.

## 6. Gate result

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]
BLOCKING: No Critical, High or Medium finding. FAIL because Low findings exist: SG-41 (the "exact shapes" row 5 accepts omit the account-exists output of the row-1 read, so a literal implementation refuses whenever the account exists and contradicts the row-2 and row-3 accept evidence), SG-42 (the legal container template parameter read by the check is not named and the read-from-file branch has no test or evidence case). Round 7: SG-39 FIXED, SG-40 FIXED; every cited Microsoft Learn page verified live with matching dates; earlier-round requirements still hold.
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
DOCUMENT_GAPS: 0 new review-level gaps; 0 blockers.
NEXT_STEP: The orchestrator (Claude Code) triages under the Low-only handling in aisdlc/.github/rules/pdlc.md: either the Technical Specifier issues spec v9 for SG-41 and SG-42 and the gate is re-run as review/spec-gate-review-9.md, or the findings go to human disposition. No human acceptance is recorded.
```

SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]

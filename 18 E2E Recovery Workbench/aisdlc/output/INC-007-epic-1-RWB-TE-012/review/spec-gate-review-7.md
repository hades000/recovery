# Spec gate review, round 7: RWB-TE-012, document storage containers

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-012-SG7` (new findings `REVIEW-RWB-TE-012-SG-39` and `-40`) |
| RUN_ID | `INC-007-epic-1-RWB-TE-012` |
| Artifact | `aisdlc/output/INC-007-epic-1-RWB-TE-012/specify/`: `spec.md` v7, `assumptions.md` v7, `document-gaps.md` v7, `shared-updates.md` v7, `compliance-validation.md` v7, `gate-response.md` (section "Round 6"), `contracts/backend-apis.json` (unchanged since v5), `contracts/frontend-integrations.json` (unchanged), `agent-run-log.md` |
| Previous rounds | `review/spec-gate-review.md` (round 1: FAIL, 0C/1H/5M/5L); `-2.md` (round 2: FAIL, 0C/0H/2M/4L); `-3.md` (round 3: FAIL, 0C/0H/1M/7L); `-4.md` (round 4: FAIL, 0C/0H/2M/5L); `-5.md` (round 5: FAIL, 0C/0H/0M/4L); `-6.md` (round 6: FAIL, 0C/0H/0M/2L) |
| Reviewer | Compliance Reviewer (spec gate) |
| Date | 2026-11-18 |
| **Status** | **FAIL** |
| Findings | 0 Critical, 0 High, 0 Medium, 2 Low (2 new). Round 6: SG-37 FIXED, SG-38 FIXED |
| Handoff | No Critical, High or Medium finding remains. The gate result is FAIL because Low findings exist. Whether a further round runs, or the Low-only handling in `aisdlc/.github/rules/pdlc.md` applies, is the orchestrator's triage. No human acceptance is recorded |

## 1. What was checked

**Inputs read.**
- All specify files listed above, diffed against `*.run6.*`. The v6→v7 spec diff covers: status and revision lines; four new source rows (`[AZ-MODES]`, `[AZ-GET]`, `[AZ-CLI-CRM]`, `[AZ-CLI-IMM]`); the new SPEC-001 "Storage account name" setting row; `storageAccountName` added to the schema input list; the rewritten pre-deploy check paragraph with six explicit inputs, the printed command, the five-row "no policy" table, the paragraph on why `immutability-policy show` was dropped, and the new Builder evidence; the two SPEC-004 PROD rows; the status reporting block. Other diffs: ASM-TE012-32 and -33; one new open item and one updated one in `shared-updates.md` §3; the `compliance-validation.md` source row and later-apply row; the `document-gaps.md` revision note. Both contracts are byte-identical to `*.run6.json`. I checked the claims in `gate-response.md` Round 6 against the files and did not take them as evidence.
- Round 6 review `review/spec-gate-review-6.md` (SG-37, SG-38).
- Document set, read only. All 1,257 `17 AI-First SDLC Repository v2/requirement/legacy/` entries in `aisdlc/evidence/document-set-baseline.sha256` match (`sha256sum -c`, no mismatch). No file under `requirement/legacy/` is newer than the round-6 review. I searched the set for a storage account or resource group naming rule and found none, so the v7 claim "environment fact, not a gap" holds.
- External citations, each read live on Microsoft Learn on 2026-11-18 (results in §2, SG-38).
- Rules: `aisdlc/.github/rules/specification-execution-gates.md`; `AGENTS.md`; `CLAUDE.md`.

**Governance checks.** These shared files were not changed by this run:
- `Traceability_Matrix.md`: 04:57.
- `DOCUMENT-GAPS.md`: 00:33.
- `README.md`: 17 Nov.

`aisdlc/docs/open-items.md` was written at 05:37, after the round-6 review (05:31). It contains no `RWB-TE-012` or `INC-007` row, and the new v7 open items are not in it. So the change does not come from this run, and the run-log line "no shared file changed" is not contradicted. The orchestrator may want to confirm who wrote it.

Other governance results:
- No `infra/azure/` folder exists, so no code was written.
- `agent-run-log.md` run 6: "No git run, no code edited, no document-set file changed, no shared file changed".
- v7 adds no credential, key, token or personal data. The spec holds no account or resource group values; they are open items, and the only literal added is a shape pattern.
- No new dependency. The check is PowerShell calling Azure CLI, as the v6 check and the RUNBOOK already did.

**Counts verified.** All of these match `compliance-validation.md` v7:
- 37 coverage rows, all 37 COVERED.
- 26 CLAR rows.
- 33 assumption rows (`ASM-TE012-01` to `-33`).
- 24 DGAP rows: 23 active, DGAP-18 withdrawn.
- 19 open items in `shared-updates.md` §3.

Both contract files parse as JSON.

## 2. Verification of round-6 findings

| Finding | Severity | Result | Evidence in v7 |
|---|---|---|---|
| SG-37 pre-deploy check target and "no policy" outcome | Low | **FIXED** (citation and evidence precision residual SG-39; binding residual SG-40) | Each part of the orchestrator's triage is met. **(1) Explicit inputs.** SPEC-001 (line 388) gives `Test-DeployParameters.ps1` six explicit inputs, including `-ResourceGroup` and `-StorageAccountName`. The account is named by the new required template input `storageAccountName`, with no default and shape `^[a-z0-9]{3,24}$` (SPEC-001 line 373; schema list line 382). A `-StorageAccountName` that differs from the file is refused. The printed command now carries `--resource-group <rg> --template-file azuredeploy.json --parameters @<parameter file> deployLegalPolicy=<effective value> --mode Incremental`, so it can run unchanged. **(2) "No policy" is an observable state, with the command cited.** Lines 390–398 define five ordered rows: account absent (`az storage account list … --query`) → accept; container absent (`az storage container-rm exists`) → accept; `properties.hasImmutabilityPolicy` false (`az storage container-rm show`, REST "Blob Containers - Get") → accept; `hasImmutabilityPolicy` true in either state → refuse; any failed read → refuse. This is the fail-closed rule the round-6 fix asked for. Line 400 says why `immutability-policy show` is not used for the decision. **(3) Builder accept case.** Line 402 accepts the first PROD-style apply with `-DeployLegalPolicy true` for row 1 and row 2, and checks the printed command. **(4) Refusal cases.** Row 4 (after the template has created the unlocked policy), row 5 (resource group missing), account-name mismatch, placeholder, and mode `Complete`. Evidence runs on disposable DEV resources with no lock, consistent with BR1. SPEC-004 First PROD apply row (line 434), ASM-TE012-32/-33, `compliance-validation.md` row "Later PROD applies" and both open items agree |
| SG-38 incremental-mode citation and source row | Low | **FIXED** | `[AZ-MODES]` is added to Sources cited (line 33). It is cited for the incremental clause in SPEC-001 (line 388), SPEC-004 (line 435) and ASM-TE012-33. `[AZ-COND]` is kept for the complete-mode deletion. The `compliance-validation.md` §2 source row (line 39) now names `[AZ-IMM]`, `[AZ-REST]`, `[AZ-COND]`, `[AZ-MODES]`, `[AZ-GET]`, `[AZ-CLI-CRM]` and `[AZ-CLI-IMM]`. The live check of each page is in the table below |

**Live check of each Microsoft Learn citation (2026-11-18).**

| Short name | Page | Live result | Claim the spec makes | Supported? |
|---|---|---|---|---|
| `[AZ-MODES]` | "Deployment modes" (ARM) | ms.date 26 June 2026, as cited. "Incremental mode": Resource Manager "leaves unchanged resources that exist in the resource group but aren't specified in the template". "Complete mode": a resource not deployed because its condition is false is deleted with REST API 2019-05-10 or later, and current CLI and PowerShell delete it | Complete mode deletes a condition-false resource. Incremental mode "leaves unchanged" resources not in the deployment | Yes. The page states "aren't specified in the template". Applying that to a condition-false resource is an inference, consistent with the page's complete-mode paragraph, and the DGAP-03 spike in ASM-TE012-33 confirms it. Acceptable as worded |
| `[AZ-COND]` | "Conditional deployment with templates" | ms.date 26 June 2026, as cited. A false condition means "the resource isn't created". The "Complete mode" section matches the text above. The page says nothing about incremental mode | "the policy resource is not created" (SPEC-004); the complete-mode deletion | Yes. It is no longer cited for incremental behaviour |
| `[AZ-GET]` | REST "Blob Containers - Get", api-version 2026-09-01 | ms.date 23 October 2026, as cited. `accountName`: minLength 3, maxLength 24, pattern `^[a-z0-9]+$`. `properties.hasImmutabilityPolicy`: "set to false by SRP if ImmutabilityPolicy has not been created for this container", true once created. `ImmutabilityPolicyState` is `Locked` or `Unlocked`. Responses: 200, or "Other Status Codes" as an ErrorResponse | Shape `^[a-z0-9]{3,24}$`. The row-3 quotation. Row 4 "whatever state" | Yes. The quotation is verbatim, and the shape is the page's pattern combined with its length limits |
| `[AZ-CLI-CRM]` | Azure CLI "az storage container-rm" | ms.date 9 November 2026, as cited. `exists` "Check for the existence of a container." and `show` "Show the properties for a specified container." are both listed GA. Both accept `--resource-group`, `--storage-account`, `--name` | The commands exist and take these arguments (rows 2, 3) | Yes, for the commands and arguments. **No**, for the output value `"exists": false` in row 2, which the page does not document: see SG-39 |
| `[AZ-CLI-IMM]` | Azure CLI "az storage container immutability-policy" | ms.date 9 November 2026, as cited. `show`: "Gets the existing immutability policy along with the corresponding ETag…". `lock` and `extend` require `--if-match` | `show` "documents only the existing-policy case"; lock and Extend use the ETag | Yes |

**Earlier-round requirements re-confirmed in v7.**

| Requirement | Holds | Evidence |
|---|---|---|
| Only the probe writes readiness | Yes | SPEC-009 line 473 "Only the probe writes readiness"; SPEC-013 line 539 "The mapper never writes readiness"; contract `readiness_writer` (unchanged); matrix unchanged from v6 |
| Per-operation outcomes never change readiness | Yes | Matrix line 313 (`BLOB_MISSING`, `ACCESS_REFUSED`, … → unchanged, no probe); line 332; SPEC-013 line 536; T-TE012-18; contract `per_operation_outcome` |
| Template unit test needs no undecided value | Yes | Line 386; T-TE012-15 (line 579) is generic: "the template parameters without `defaultValue` are exactly the schema list", and the local file gives each a shape-valid value. So `storageAccountName` (no default) must be in the schema list (it is, line 382) and in the local file ("every required input", line 383). No contradiction with the new input |
| Placeholders refused by the pre-deploy check, with owner and place | Yes | Line 388 (step 1 of the RUNBOOK Apply procedure, every environment); RW-PLATADM runs it and the platform team maintains it (line 402); open item with owner and needed-by (`shared-updates.md` §3) |
| Later PROD applies never change the locked policy | Yes | SPEC-004 line 435: PROD file `false`, incremental only, policy not created and existing one left unchanged (`[AZ-COND]`, `[AZ-MODES]`); period changes only by "Extend"; T-TE012-15 asserts the condition and per-file values |
| Incremental mode | Yes | The check refuses any mode other than `Incremental`; the printed command fixes `--mode Incremental`; Builder evidence refuses `Complete` |

## 3. New findings

### REVIEW-RWB-TE-012-SG-39: Low. Two of the "no policy" observations rest on output values no cited source documents, and one accept row is never exercised

**Affects:** SPEC-001 "no policy" table rows 1–3 (lines 394–396) and Builder evidence (line 402); ASM-TE012-33; `compliance-validation.md` §2 source row.

**Evidence**
- **Row 2.** The accept decision depends on `az storage container-rm exists` returning `"exists": false`, attributed to `[AZ-CLI-CRM]` "exists". The live page (ms.date 9 November 2026) says only "Check for the existence of a container." It shows no output and no field name or value. Line 400 drops `immutability-policy show` on the ground that its absent-policy result "would surface as an undocumented error rather than an observable value". By the spec's own test, the row-2 output value is not documented either.
- **Row 1.** The decision depends on `az storage account list --resource-group <rg> --query "[?name=='<account>']"` returning `[]`. Its source is "Azure CLI", with no page in Sources cited. The compliance self-check says every external statement is cited to a page "checked live".
- **Row 3.** Row 3 (container present, `hasImmutabilityPolicy` = `false` → accept) is the only accept row whose decision parses `properties.hasImmutabilityPolicy`. It is not in the Builder evidence. The evidence exercises rows 1, 2, 4 and 5. A wrong JSON path, or treating a missing property as `false`, would go unnoticed for the accept branch. Row 3 is also the state a PROD retry reaches after a first apply that created the container but failed before the policy.
- **Impact is limited.** The behaviour is very likely as stated. Azure refuses to change a locked policy (`[AZ-REST]`), so a wrong accept makes the apply fail rather than change the policy. That is why this is Low.

**Required fix:** Do one of the following for rows 1 and 2:
- cite a page that documents the observed value, for example the Azure CLI "az storage account" reference for `list` (and `--query`), plus a page showing the `exists` output; or
- state in SPEC-001 and ASM-TE012-33 that the output shapes are labelled assumptions, confirmed by the Builder evidence, and that any other output falls to row 5 (refuse).

Then add a Builder evidence case for row 3. On the disposable account, apply once with `deployLegalPolicy=false`, so the legal container exists without a policy. Run the check with environment `prod` and `-DeployLegalPolicy true`. It is accepted and prints the command.

### REVIEW-RWB-TE-012-SG-40: Low. The PROD guard's inputs are not bound: `-Environment` is not tied to the parameter file, the legal container name is a literal although the template parameterises it, and the resource group has no shape

**Affects:** SPEC-001 pre-deploy check paragraph (line 388), table rows 2–3 (lines 395–396) and Builder evidence (line 402); SPEC-002 (line 408); `shared-updates.md` §3 open item for `storageAccountName` and the resource group.

**Evidence**
- **Environment not bound to the file.** The "no policy" read runs only "in PROD with an effective `deployLegalPolicy` of true", and PROD is taken from the free input `-Environment`. No rule ties `-Environment` to `-ParameterFile`. The only file rule is "the file is the local file". So `-Environment dev -ParameterFile azuredeploy.prod.parameters.json -DeployLegalPolicy true -ResourceGroup <PROD rg>` skips the PROD guard and prints a PROD deploy command with `deployLegalPolicy=true`. That is the exact case SG-37 was meant to close. The Builder evidence has no refusal case for an environment/file mismatch. Also, "accepts a completed copy of the local file renamed as an environment file for a non-PROD environment" shows that the file name, not its contents, is what identifies the file.
- **Legal container name is a literal.** SPEC-002 says the four containers are "named by parameters with the defaults `rwb-intake`, `rwb-docs`, `rwb-docs-legal`, `rwb-quarantine`". Rows 2 and 3 query the literal `--name rwb-docs-legal`. If a parameter file sets the legal container parameter to another name, row 2 returns `exists: false` and the check accepts, whatever the policy on the container the template actually targets. The spec does not say that environment files must not override container names, and T-TE012-15 does not assert it. The same literal is in the PROD lock and Extend steps (lines 422, 427). This was already so in v6, where `show` was run on `rwb-docs-legal`. v7 makes the literal part of the decision table.
- **Resource group shape.** `-ResourceGroup` is used in every read and in the printed command, but the spec gives it no shape and does not validate it. The `shared-updates.md` §3 open item lists "`storageAccountName` and the target resource group … (names only; shape `^[a-z0-9]{3,24}$`)". That pattern is the account-name shape. A resource group allows 1–90 characters (`[AZ-GET]` `resourceGroupName`), including upper case and hyphens, so the open item gives the resource group a wrong shape.
- **Impact is limited.** As in SG-37, Azure refuses changes to a locked policy (`[AZ-REST]`), so a bypass makes the apply fail rather than change the locked policy. That is why this is Low.

**Required fix:**
1. In SPEC-001, have the check refuse when `-Environment` does not match the parameter file. For example, the file name must be `azuredeploy.<environment>.parameters.json`, or the file carries an environment value the check compares. Add that refusal to the Builder evidence.
2. Have the check read the legal container name from the parameter file, or the template default when the file does not set it, and use that name in rows 2–3, the lock and Extend. Alternatively, state that environment files never set container-name parameters and add that assertion to T-TE012-15.
3. In the open item, give the account shape only to `storageAccountName`, and either state the resource-group shape (1–90 characters as Azure allows) or say the resource group is not shape-checked.

## 4. Requirement and control checks

| Check | Result |
|---|---|
| Authentication and authorization | No endpoint (story §12). Managed identity only; container-scope roles. The check runs as RW-PLATADM (`[S]` §10). Pass |
| Customer data protection | UUID blob names; `sha256` metadata only; IDs-only logs; synthetic test data. v7 adds no data values. Pass |
| Audit of sensitive actions | `DOCUMENT_CHANGE_REFUSED` (T-TE012-10); check output kept with the apply record. Pass |
| KYC, AML, suitability, consent | Not in scope |
| Frontend integration versioning and error contract | `UI In Scope: NO`, `NO_API_CHANGE`; contracts unchanged. Pass |
| Secrets and environment configuration | No committed key; the account name and resource group are open items, not values; placeholders refused before deploy. Input binding: SG-40 |
| Feature flag off path (AGENTS §3.13) | Unchanged. Pass |
| Write-once control (CTL-12, NFR-029, BR1) | Policy in template; PROD lock and Extend only in PROD; incremental mode enforced; fail-closed "no policy" decision with explicit target. Residuals: SG-39 (sources and row-3 evidence), SG-40 (environment/file binding, container-name literal) |
| AC timing (AC10) | Unchanged. Pass |
| Availability and health signal | Unchanged since v6 (probe-only writer, background request in every state, detection bound). Pass |
| Test coverage and evidence | Frontend `NOT_APPLICABLE` correct. Backend four-counter gate, per-class and no-drop rules unchanged. T-TE012-15 consistent with the new required input. Pre-deploy Builder evidence lacks row 3 (SG-39) and an environment/file mismatch refusal (SG-40) |
| Module boundaries | Unchanged; RWB-TE-001 v4 map. Pass |
| Migration rule (D-RUN-07) | No migration. Pass |
| Dependencies (D-RUN-08, AGENTS §4.4) | None added (PowerShell and Azure CLI were already used by the check and runbook). Pass |
| Traceability and status lines | Counts correct. Row-007 status names spec v7 and round 7. Spec `Status: SUCCESS` with `REVIEW_GATE_RESULT: PENDING` follows the v5 pattern before a gate. Pass |
| Shared and document-set files | Document set unchanged (1,257 baseline hashes match). Shared files not changed by this run (`open-items.md` 05:37 write has no TE-012 content; §1). Pass |

**Minor editorial notes, not findings.**
- `document-gaps.md` puts the "Revision v7" sentence before "Revision v6" in its revision paragraph.
- `spec.md` ASM-TE012-33 short form (line 124) still reads as in v6. It remains true.

## 5. Document gaps

No new review-level gap (no `TE012-SG7-DG-nn` row).
- I searched the document set for a storage account or resource group naming rule (`storage account name`, `naming convention`, `resource group`) and found none relevant to this story. The v7 treatment of `storageAccountName` and the resource group as environment facts (open item, not a gap) is consistent with round 5's ruling on subnet and object IDs.
- SG-39 and SG-40 concern how the spec cites Azure CLI behaviour and binds the check's inputs. Neither is a silence or contradiction in the document set.
- `document-gaps.md` v7 has no change of substance. DGAP-01 to -17 and -19 to -24 stay accepted; DGAP-18 stays withdrawn. 0 blockers.

## 6. Gate result

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]
BLOCKING: No Critical, High or Medium finding. FAIL because Low findings exist: SG-39 (row 1 and row 2 "no policy" outputs are not documented by any cited page, and the row-3 accept path has no Builder evidence case), SG-40 (-Environment is not bound to the parameter file so the PROD guard can be skipped; the legal container name is a literal though SPEC-002 parameterises it; the resource-group open item carries the account-name shape). Round 6: SG-37 FIXED, SG-38 FIXED; every cited Microsoft Learn page verified live with matching dates; earlier-round requirements still hold.
DOCUMENT_GAPS: 0 new review-level gaps; 0 blockers.
NEXT_STEP: The orchestrator (Claude Code) triages: either the Technical Specifier issues spec v8 for SG-39 and SG-40 and the gate is re-run as review/spec-gate-review-8.md, or the Low-only handling in aisdlc/.github/rules/pdlc.md applies. No human acceptance is recorded.
```

SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]

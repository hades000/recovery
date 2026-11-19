# Spec gate review, round 10: RWB-TE-012, document storage containers

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-012-SG10` (no new findings; the next free finding ID is `SG-45`) |
| RUN_ID | `INC-007-epic-1-RWB-TE-012` |
| Artifact | `aisdlc/output/INC-007-epic-1-RWB-TE-012/specify/`: `spec.md` v10, `assumptions.md` v10, `document-gaps.md` v10, `shared-updates.md` v10, `compliance-validation.md` v10, `gate-response.md` (section "Round 9"), `agent-run-log.md` (remediation run 9), `contracts/backend-apis.json` and `contracts/frontend-integrations.json` (both byte-identical to `*.run9.json`) |
| Previous rounds | `review/spec-gate-review.md` (round 1: FAIL, 0C/1H/5M/5L); `-2.md` (FAIL, 0C/0H/2M/4L); `-3.md` (FAIL, 0C/0H/1M/7L); `-4.md` (FAIL, 0C/0H/2M/5L); `-5.md` (FAIL, 0C/0H/0M/4L); `-6.md` (FAIL, 0C/0H/0M/2L); `-7.md` (FAIL, 0C/0H/0M/2L); `-8.md` (FAIL, 0C/0H/0M/2L); `-9.md` (FAIL, 0C/0H/0M/2L) |
| Reviewer | Compliance Reviewer (general-purpose agent, spawned for this gate) |
| Date | 2026-11-18 |
| **Status** | **PASS** |
| Findings | 0 Critical, 0 High, 0 Medium, 0 Low (0 new). Round 9: SG-43 FIXED, SG-44 FIXED |
| Handoff | No finding remains. The spec gate passes; the Plan stage may start. The plan gate is the next independent gate. No human acceptance is required for a PASS |

Severity scale (as in rounds 1–9): Critical, High and Medium block the next stage until fixed and re-reviewed. Low is a spec defect with limited impact; it is reported and makes the gate FAIL, but it does not by itself block the handoff (`pdlc.md` Low-only handling). A review with no findings is PASS.

## 1. What was checked

**Inputs read.**
- **Spec diff, v9 → v10.** `git diff --no-index --ignore-space-at-eol spec.run9.md spec.md` returns changes in exactly these places:
  - the Revision and Spec gate rows (lines 10 and 15);
  - the `[AZ-CLI-CRM]` source row (line 35) and the new `[AZ-CLI-REST]` row (line 37);
  - the short-form ASM-TE012-32 (line 124);
  - the pre-deploy check paragraph, its two stage bullets and the new "Report, on every outcome" paragraph (lines 389–394);
  - the "no policy" paragraph and the seven-row table (lines 396–406);
  - the shape paragraph (line 408);
  - the Builder evidence preamble, table and BE-01 to BE-13 (lines 414–430);
  - the SPEC-018 Builder evidence pointer (line 623);
  - the status block (lines 740–741).
  Every added sentence was re-read against the story, the `[AZ-GET]`/`[AZ-CLI-REST]`/`[AZ-CLI-CRM]` citations, SPEC-001, SPEC-002, SPEC-004, SPEC-018 and the Builder evidence table. No other section of `spec.md` changed.
- **Other diffs.** Each specify file was diffed against `*.run9.*`:
  - `assumptions.md`: the revision header and ASM-TE012-32 (line 38);
  - `document-gaps.md`: the revision header only;
  - `shared-updates.md`: the revision header and the pre-deploy check open item;
  - `compliance-validation.md`: the revision/round rows, the source row, the later-PROD row, the shared-updates count and the round-9 summary;
  - `gate-response.md`: the Round 9 section only;
  - `agent-run-log.md`: the run-8 gate result and the run-9 section.
  No unrelated edits. `contracts/*.json` are byte-identical to the run-9 backups and parse as JSON.
- **Claims checked, not trusted.** Every claim in `gate-response.md` Round 9 (lines 124–131) and in `compliance-validation.md` v10 (lines 42, 47, 91–93) was checked against the spec text. All hold; none was taken as evidence.
- **Story.** The story file `rwb-te-012-document-storage-containers-v1.md` (RWB-TE-012 story file v1, Epic 1 story files v7), read only: §4 steps 1–2, §6, §10, §12, §13, §15, §16, §17, §18, §19. Every story rule, acceptance criterion, field, message and test case still maps to the spec (section 4 below).
- **Document set.** The 1,257 files under `17 AI-First SDLC Repository v2/requirement/legacy/` have no modification after the baseline: the newest is 16 Nov 2026 07:55; none is newer than 17 Nov 2026 23:03 (the baseline manifest). The v10 external citations are Microsoft Learn pages, not document-set files.
- **Rules.** `aisdlc/.github/rules/specification-execution-gates.md` (required structure, coverage columns, status lines); `.claude/agents/compliance-reviewer.md`; `pdlc.md` (PASS/FAIL semantics); `AGENTS.md`; `CLAUDE.md`.
- **Governance.**
  - `Traceability_Matrix.md`: 04:57. `DOCUMENT-GAPS.md`: 00:33. `docs/increments/INDEX.md`: 17 Nov. `README.md`: 17 Nov. `docs/open-items.md`: 05:37, the orchestrator's OPEN-050 write, not this run; `agent-run-log.md` run 9 records the same.
  - `AI-SDLC-BUILD-LOG.md` was written at 07:23 by the orchestrator (round-9 gate row and D-RUN-22), not by this stage.
  - No code: `infra/azure/` does not exist; no backend or frontend file is newer than review-9. The only files newer are the orchestrator's build log and resume note and other runs' stage outputs.
  - No secrets or personal data: v10 adds an external CLI command, container names, a resource-group/account placeholder and a report rule. No key, token, account value or personal data.
  - No new dependency: `az rest` is in the Azure CLI already used by the pre-deploy check; no library, tool or engine is added.
  - **Counts verified.** 37 coverage rows (all COVERED); 26 CLAR rows; 33 assumption rows; 24 DGAP rows (23 active, DGAP-18 withdrawn); 19 open items. Both contract files parse.
  - **Status block.** Line 3 `Status: SUCCESS`; line 740 `REVIEW_GATE_RESULT: PENDING — review/spec-gate-review-10.md` with the round-9 result quoted; line 741 `NEXT_STEP: Spec gate round 10`; `compliance-validation.md` line 93 "Round 10: pending". This is the consistent pre-gate state, the same pattern as v9 before round 9.

## 2. Verification of round-9 findings

| Finding | Severity | Result | Evidence in v10 |
|---|---|---|---|
| SG-43 rows 5–6 read `properties.hasImmutabilityPolicy` from `az storage container-rm show`, whose CLI output the cited page does not document, so the row-5 accept and BE-03 were unreachable as written | Low | **FIXED** | **Option (b) taken.** Read 3 is now `az rest --method get --url "/subscriptions/{subscriptionId}/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<account>/blobServices/default/containers/<legal>?api-version=2026-09-01" --output-file <report folder>/legal-container.json` (`spec.md` line 404). `[AZ-CLI-REST]` (new source row, line 37) states the three behaviours used: a URL without a host is an ARM resource ID, `{subscriptionId}` is the current subscription, and `--output-file` saves the response payload. `[AZ-GET]` documents exactly that GET path and `properties.hasImmutabilityPolicy` in the response. Rows 5 and 6 now read "the payload's `properties.hasImmutabilityPolicy`" (lines 404–405); row 7 still refuses a non-zero exit, a missing payload, a missing/non-boolean property or any other output (line 406). **Claims corrected.** Line 408 says only reads 1 and 2 are assumed and that the saved payload is documented; v9's line 390 "every result below is reachable" is gone, replaced by "each output leads to exactly one row" (line 396); SPEC-004 line 462 still cites rows 1, 3 and 5 (accept), 6 and 7 (refuse). **Reachability.** BE-01 gives row 1; BE-02 to BE-06 give row 2; BE-02 and BE-06 give row 3; BE-03 to BE-05 give row 4; BE-03 gives row 5; BE-04 gives row 6; BE-07 gives row 7. The live pages support the command and the response path (section 3). No new defect on the read-3 path |
| SG-44 several Builder evidence expectations were not produced by the check's rules: output printed on refusal, deciding row, order of checks, BE-06 set-up | Low | **FIXED** | **Print on every outcome.** `spec.md` line 394 now defines a report printed on every outcome: the result; on refusal the reason (the stage 1 rule or the deciding "no policy" row); `<legal>` once the parameter file has been read; in stage 2 the command and raw output of each read and the deciding row; on accept the one deploy command; the report is kept with the apply record. **Order of checks.** Line 389 says "checks in two stages, stops at the first refusal"; line 391 defines stage 1 as local, no Azure call, always first in every environment; line 392 runs stage 2 only after stage 1 passes, for PROD with an effective `true`. The Round 8 note that the resource-group length is checked locally is now true of the spec (line 391), and `gate-response.md` Round 9 says so. **BE-06.** "As BE-02 (account exists)" (line 423). **BE-05.** `<legal>` = `rwbdocslegalalt`, rows 2 and 4, payload true, row 6, refuse, with the proof that a literal would have accepted (line 422); the report rule produces the printed name on that refusal. **Attribution.** Line 408 and ASM-TE012-32 name the cases from the printed raw outputs: row 1 BE-01; row 2 BE-02 to BE-06; row 3 BE-02 and BE-06; row 4 BE-03 to BE-05; row 5 BE-03; row 6 BE-04. The BE table's expected column is "Expected report" and each case names the observable outputs (lines 418–430) |

**Live check of the external citations used by the changed text (2026-11-18).**

| Short name | Page | Live result | Claim the spec makes | Supported? |
|---|---|---|---|---|
| `[AZ-CLI-REST]` | Azure CLI reference "az", command `az rest` (ms.date 1 September 2026) | `--uri --url`: "If it doesn't start with a host, CLI assumes it as an Azure resource ID and prefixes it with the ARM endpoint of the current cloud"; "Common token {subscriptionId} will be replaced with the current subscription ID"; `--output-file`: "Save response payload to a file". The page's own VM example uses `--method get --uri /subscriptions/{subscriptionId}/resourceGroups/...?api-version=...` | Read 3 sends an ARM resource-ID URL with `{subscriptionId}`, and the check parses the saved response payload (lines 37, 404, 408) | Yes |
| `[AZ-GET]` | "Blob Containers - Get", api-version 2026-09-01 (ms.date 23 October 2026) | GET path is exactly `/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Storage/storageAccounts/{accountName}/blobServices/default/containers/{containerName}?api-version=2026-09-01`; `properties.hasImmutabilityPolicy` is a boolean "set to false by SRP if ImmutabilityPolicy has not been created"; the sample response nests it under `properties`; `accountName` 3–24 `^[a-z0-9]+$`; `containerName` 3–63, numbers/lower-case letters/dash with each dash between a letter or number; `resourceGroupName` 1–90 | Rows 5 and 6 read the documented REST property from the saved payload; the account/container/resource-group shapes used in stage 1 | Yes |
| `[AZ-CLI-CRM]` | Azure CLI reference "az storage container-rm" (ms.date 9 November 2026) | `exists` and `show` take `--name`, `--resource-group`, `--storage-account` (and `--ids`); no output sample for either; the `migrate-vlw` example queries `show` output as `immutableStorageWithVersioning.migrationState` at top level | Read 2 uses `exists`; its `exists` object remains an assumption (ASM-TE012-32), confirmed by BE-02/BE-06 (false) and BE-03 to BE-05 (true). v10 no longer uses `show`, so the undocumented `show` output is no longer on the accept path | Yes for `exists`; the assumption is used as labelled |
| `[AZ-CLI-IMM]` | Azure CLI reference "az storage container immutability-policy" (ms.date 9 November 2026) | `show`, `lock`, `extend`; `lock`/`extend` require the policy ETag; locked policy only allows Extend | PROD lock evidence and the "Extend" step use the printed `<legal>` and the ETag (SPEC-004 lines 450–455, 464) | Yes (unchanged from round 9) |
| `[AZ-IMM]` | "Immutable storage for blob data overview" (ms.date 18 August 2026) | "You can't delete a locked time-based retention policy"; extend but not decrease; "A maximum of five increases ... over the lifetime of a locked policy that is defined at the container level" | Later PROD applies cannot change/remove the locked policy; Extend at most five times (SPEC-004 lines 458–465) | Yes |

`[AZ-REST]`, `[AZ-COND]` and `[AZ-MODES]` support text unchanged by v10 and were verified live in round 9; v10 adds no new claim from them.

## 3. Earlier-round requirements re-confirmed (no regression)

| Requirement | Holds | Evidence |
|---|---|---|
| Only the probe writes readiness | Yes | `spec.md` line 501 "Only the probe writes readiness"; line 561 "The mapper never writes readiness"; contract `readiness_writer` unchanged |
| Per-operation outcomes never change readiness | Yes | Line 332 (`BLOB_MISSING`: "readiness unchanged, no probe"); T-TE012-18; CLAR-024 |
| Template unit test needs no undecided value | Yes | Line 387; T-TE012-15 "needs no undecided value"; the container-name parameters keep defaults and stay outside the schema list (lines 383, 436) |
| Placeholders refused before deploy, with owner and place | Yes | Line 391 (stage 1); line 412 (owner and evidence); BE-10; open item in `shared-updates.md` §3 |
| Explicit resource group, account and environment inputs | Yes | Six inputs (line 389); environment/file-name binding; account mismatch refused; resource group 1–90; printed command carries `--resource-group <rg>` and `@<parameter file>` |
| Local file never applied | Yes | Line 391 refuses `azuredeploy.local.parameters.json` (`local` is not an allowed environment); BE-12 |
| Incremental mode | Yes | Line 391 refuses any other mode; printed `--mode Incremental`; BE-11 |
| Later PROD applies never change the locked policy | Yes | Line 458 (PROD `false`, `[AZ-COND]`, `[AZ-MODES]`); line 459 "Extend" only on the printed `<legal>`; T-TE012-15 per-file values |
| Lock, evidence and Extend use the printed name, not a literal | Yes | Lines 450, 455, 464 ("the name the pre-deploy check printed", "the printed `<legal>`") |
| Role scopes follow the parameters | Yes | Lines 475–476 name each container "by its SPEC-002 parameter"; T-TE012-15 "six container-scope role assignments" equals 3 + 3 |
| Name consistency | Yes | `legalContainerName` is spelled the same in lines 390, 404, 436, 444, 418-423, 623; `assumptions.md` line 38; `gate-response.md` line 119. The properties table (lines 220-223) keeps the `rwb.dochub.container.*` keys, which SPEC-002 ties to the parameters |
| Row-number references | Yes | SPEC-004 line 462 (1, 3, 5 / 6 / 7); line 396 "up to three reads"; line 408 "rows 1–4", "BE-03 ... row 5 and BE-04 row 6"; BE-01 to BE-07 row labels; `assumptions.md` line 38 "rows 1–7"; `gate-response.md` line 131. All match the 7-row table |
| SG-41 account-exists output | Yes | Rows 1 and 2 still define `[]` and the one-element array; BE-01 and BE-02 to BE-06 confirm |
| SG-42 legal container parameter | Yes | SPEC-002 line 436 names all four parameters and defaults; T-TE012-15 asserts them; BE-05/BE-06 set `legalContainerName` in the file |

## 4. Requirement and control checks

| Check | Result |
|---|---|
| Authentication and authorization | No endpoint (story §12). Managed identity only; container-scope roles by parameter (lines 475–476). The check runs as RW-PLATADM (story §10). Pass |
| Customer data protection | UUID blob names; IDs-only logs; synthetic test data. v10 adds no data value. Pass |
| Audit of sensitive actions | `DOCUMENT_CHANGE_REFUSED` (T-TE012-10); the check's report is kept with the apply record, accepted or refused; the report content is now defined (line 394). Pass |
| KYC, AML, suitability, consent | Not in scope |
| Frontend integration versioning and error contract | `UI In Scope: NO`, `NO_API_CHANGE`; contracts unchanged. Pass |
| Secrets and environment configuration | No committed key; account, resource group and container names have stated shapes; placeholders refused; environment bound to file name; `az rest` uses the logged-in CLI credential, no new secret. Pass |
| Feature flag off path (AGENTS §3.13) | Unchanged. Pass |
| Write-once control (CTL-12, NFR-029, BR1) | Policy in template on `legalContainerName`; PROD lock and Extend on the printed `<legal>`; incremental mode; fail-closed "no policy" decision through the documented REST response; rows 1–7. SG-43 and SG-44 fixed. Pass |
| Test coverage and evidence | Frontend `NOT_APPLICABLE` correct. Backend four-counter gate, per-class and no-drop rules unchanged (SPEC-023). T-TE012-15 covers container-name parameters. BE-01 to BE-13 covers every row, the file override and every local refusal, with expected reports produced by the report rule. Pass |
| Module boundaries | Unchanged; RWB-TE-001 v4 map. Pass |
| Migration rule (D-RUN-07) | No migration. Pass |
| Dependencies (D-RUN-08, AGENTS §4.4) | None added; `az rest` is in the existing Azure CLI. Pass |
| Traceability and status lines | Counts correct. Row 007 names spec v10 and round 10. Status SUCCESS with the PENDING gate follows the pre-gate pattern. Pass |
| Shared and document-set files | Document set unchanged (1,257 files; newest 16 Nov 07:55); shared files not changed by this run. Pass |

**Minor editorial notes, not findings (no action required before the plan gate).**
- **Stale source in ASM-TE012-33's basis.** `assumptions.md` line 39 still lists "`[AZ-CLI-CRM]` `exists`, `show`", but v10 no longer uses `show`; the source row (line 35) now says "`exists`, used by read 2". The normative sentence is correct ("legal container absent per `az storage container-rm exists`, or `hasImmutabilityPolicy` false per 'Blob Containers - Get'"). Remove `show` at the next edit.
- **BE-10's "naming the input".** The report rule (line 394) requires "the reason (the stage 1 rule that failed)"; naming the input holding the placeholder is a specific reason, so the expectation is attainable and a Builder following the table will name it. No rule change needed.
- **The intermediate row numbers.** The report prints the raw output of each read and the deciding row; the BE table's "Rows 2 and 4" are the rows those outputs select, verifiable from the printed raw outputs. No rule change needed.
- **The `legal-container.json` path.** The report folder is per apply and the check refuses on a non-zero exit before parsing; a one-line RUNBOOK note to clear or uniquely name the file is enough. No spec change needed.
- **The `rwb.dochub.container.*` match.** SPEC-002 requires each container parameter value to equal the matching property, but no automated check enforces it; a mismatch fails safe through the readiness probe `CONTAINER_MISSING:<name>`. This is pre-existing and already noted in round 9.

## 5. Findings

| ID (next from SG-44) | Severity | Finding | Evidence | Required fix |
|---|---|---|---|---|
| — | — | No new finding. SG-43 and SG-44 are fixed; no earlier finding is reopened; no new finding. The next free ID is SG-45 | Sections 2–4 | None |

## 6. Document gaps

No new review-level gap (no `TE012-SG10-DG-nn` row).
- **Not a document-set gap.** SG-43 concerns the output of an external CLI command and the REST response; SG-44 concerns how the spec states its own evidence. Neither is a silence or contradiction in the document set. The v10 revision note says the `az rest` read and the report are tool facts, not gaps; that is correct.
- **Defaults remain sourced.** The SPEC-002 defaults trace to the story (§4 step 1, §13) and Decision Log v10 D-RCV-31. The parameter names are a design choice the story leaves open: §13 says "in the format the ACE team uses", and DGAP-09 already covers the template format.
- **Existing gaps.** DGAP-01 to -17 and -19 to -24 stay accepted; DGAP-18 stays withdrawn. 0 blockers.

## 7. Gate result

```text
SPEC_GATE: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]
BLOCKING: None.
DOCUMENT_GAPS: 0 new review-level gaps; 0 blockers.
NEXT_STEP: The orchestrator may start the Plan stage; the plan gate is the next independent gate.
```

SPEC_GATE: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]

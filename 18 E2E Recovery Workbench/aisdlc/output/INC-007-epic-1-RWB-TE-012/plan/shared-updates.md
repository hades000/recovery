# Shared-file updates proposed by the Implementation Planner — INC-007-epic-1-RWB-TE-012

This stage did not edit any shared file (RUN-BRIEF rule 3). The orchestrator applies these rows in order. IDs marked `<next>` take the next free number in the target register. The spec stage's proposals (`../specify/shared-updates.md` v10) are applied first; this file adds the plan-stage rows and does not repeat them. Section 0 holds the shared Gradle, YAML, `.env`, compose and `dev.ps1` rows the plan gate asked for (PLAN-001); the Implementation Builder does not write those files.

## 0. Shared configuration and local-stack files — orchestrator applies (SH-01 to SH-07)

D-RUN-06 (18 Nov 2026) and `RUN-BRIEF.md` rule 3 reserve the shared files to the orchestrator. Each row below is the exact change; no Builder task edits these files. The Builder stops at the consuming task and reports `SHARED_FILE_DEPENDENCY: SH-nn` until the row is applied, then verifies the applied state. `README.md` is not in this table: SPEC-021 names it a Builder edit (see §6).

### 0.1 `backend/src/main/resources/application.yaml`

**SH-01 — add the `rwb.dochub` block (needed by TASK-08).**

| Field | Value |
|---|---|
| File | `backend/src/main/resources/application.yaml` |
| Line or section | `rwb:` block, after `drools.kiebase-cache-max: 20` (line 97), before `blob:` (line 98) |
| Current (old) | No `dochub` key; line 97 is the last `rwb.drools` entry and line 98 starts `blob:` |
| Proposed (new) | Insert, at two-space indent under `rwb:`:<br>`  dochub:`<br>`    storage-containers: ${RWB_DOCHUB_STORAGE_CONTAINERS:false}`<br>`    storage:`<br>`      account-url: ${RWB_DOCHUB_ACCOUNT_URL:}`<br>`      timeout-seconds: 10`<br>`      readiness-recheck-seconds: 30`<br>`      service-identity-client-id: ${RWB_DOCHUB_SERVICE_MI_CLIENT_ID:}`<br>`      ocr-identity-client-id: ${RWB_DOCHUB_OCR_MI_CLIENT_ID:}`<br>`      emulator: false`<br>`    container:`<br>`      intake: rwb-intake`<br>`      standard: rwb-docs`<br>`      legal: rwb-docs-legal`<br>`      quarantine: rwb-quarantine` |
| Reason and source | SPEC-006 (properties table), SPEC-016 (`rwb.dochub` replaces `rwb.blob`); `plan.md` "Configuration properties". Eleven keys; `emulator-connection-string` is local-only (SH-03) |
| Needed by | TASK-08 (T-TE012-01 binds these defaults) |

**SH-02 — remove the `rwb.blob` block (needed by TASK-16).** Kept separate from SH-01 on purpose: the baseline `BlobDocumentStore.BlobProperties` bean still starts from `rwb.blob` until TASK-16 deletes the class, so removing it earlier would break every Spring context that includes the baseline bean.

| Field | Value |
|---|---|
| File | `backend/src/main/resources/application.yaml` |
| Line or section | `rwb.blob:` block (currently lines 98–102; the anchor is the key, not the number, because SH-01 shifts the line numbers) |
| Current (old) | `  blob:` / `    connection-string: ${RWB_BLOB_CONNECTION_STRING:}` / `    endpoint: ${RWB_BLOB_ENDPOINT:}` / `    document-container: rwb-documents` / `    legal-container: rwb-documents-legal` |
| Proposed (new) | Delete the whole `rwb.blob:` block; nothing replaces it. No other line changes |
| Reason and source | SPEC-016 baseline evolution (no baseline class remains beside its successor); SPEC-007 (no runtime container creation); TASK-16 deletes `BlobDocumentStore` |
| Needed by | TASK-16 (apply with or after the class deletions, before the green run and TASK-17) |

### 0.2 `backend/src/main/resources/application-local.yaml`

**SH-03 — add the local profile's `rwb.dochub` entries (needed by TASK-08).**

| Field | Value |
|---|---|
| File | `backend/src/main/resources/application-local.yaml` |
| Line or section | `rwb:` block, after `drools: ${RWB_P3_DROOLS:true}` (line 14) |
| Current (old) | No `dochub` key; `rwb.p3.drools` is the last line (line 14) |
| Proposed (new) | Append, at two-space indent under `rwb:`:<br>`  dochub:`<br>`    storage-containers: true`<br>`    storage:`<br>`      emulator: true`<br>`      emulator-connection-string: ${RWB_DOCHUB_EMULATOR_CONNECTION_STRING:}` |
| Reason and source | SPEC-006, SPEC-017, SPEC-021 (`application-local.yaml` row: flag `true`, `emulator: true`, string placeholder); `plan.md` "Configuration properties" |
| Needed by | TASK-08; TASK-09/TASK-10 (T-TE012-13 loads `application-local.yaml`) |

### 0.3 `.env.example`, `docker-compose.yml`, `scripts/dev.ps1` (SPEC-021)

**SH-04 — rename the two local Blob keys (needed by TASK-18).**

| Field | Value |
|---|---|
| File | `.env.example` |
| Line or section | Lines 23 and 24 |
| Current (old) | `RWB_BLOB_CONNECTION_STRING=<published Azurite development key, loopback>` and `RWB_BLOB_CONNECTION_STRING_DOCKER=<same key, azurite host>` |
| Proposed (new) | `RWB_DOCHUB_EMULATOR_CONNECTION_STRING=<same value as line 23>` and `RWB_DOCHUB_EMULATOR_CONNECTION_STRING_DOCKER=<same value as line 24>` |
| Reason and source | SPEC-021 lines 1–2; the property is `rwb.dochub.storage.emulator-connection-string`. Values are unchanged; only the key names change |
| Needed by | TASK-18 |

The value is the existing line's value, unchanged character for character; only the key name changes. The value is the published Azurite development key, not a secret (SPEC-017), and it is not reproduced here.

**SH-05 — pass the renamed Docker value to the backend (needed by TASK-18).**

| Field | Value |
|---|---|
| File | `docker-compose.yml` |
| Line or section | Line 135, the `backend` service `environment:` list |
| Current (old) | `      RWB_BLOB_CONNECTION_STRING: ${RWB_BLOB_CONNECTION_STRING_DOCKER}` |
| Proposed (new) | `      RWB_DOCHUB_EMULATOR_CONNECTION_STRING: ${RWB_DOCHUB_EMULATOR_CONNECTION_STRING_DOCKER}` |
| Reason and source | SPEC-021 line 3. No other compose key, service or `depends_on` changes |
| Needed by | TASK-18 |

**SH-06 — heal an existing `.env` with the missing keys (needed by TASK-18).**

| Field | Value |
|---|---|
| File | `scripts/dev.ps1` |
| Line or section | `Initialize-EnvFile` (lines 28–42): after the copy-when-absent block (lines 29–32), before `$content = Get-Content $EnvFile -Raw` (line 33) |
| Current (old) | The function copies `.env.example` only when `.env` is absent, then runs the codec-key block. No append-missing-keys loop |
| Proposed (new) | Insert the block below between the copy-when-absent block and the codec-key block. Existing lines are never changed or removed; the message is exactly `Added <KEY> to .env from .env.example` |
| Reason and source | SPEC-021 line 4 (append only; no existing line changed or removed; `Added <KEY> to .env from .env.example`); ASM-TE012-22 |
| Needed by | TASK-18 |

```powershell
  $envText = Get-Content $EnvFile -Raw
  if (-not $envText.EndsWith("`n")) { $envText += "`n" }
  $added = $false
  foreach ($line in Get-Content (Join-Path $Root ".env.example")) {
    if ($line -notmatch "^([A-Za-z_][A-Za-z0-9_]*)=") { continue }
    $key = $Matches[1]
    if ($envText -notmatch "(?m)^$([regex]::Escape($key))=") {
      $envText += "$line`n"
      $added = $true
      Write-Host "Added $key to .env from .env.example"
    }
  }
  if ($added) { Set-Content -Path $EnvFile -Value $envText -Encoding utf8 -NoNewline }
```

### 0.4 `backend/build.gradle.kts`

**SH-07 — correct the comment only (needed by TASK-19).** No dependency, repository, task or JaCoCo line changes.

| Field | Value |
|---|---|
| File | `backend/build.gradle.kts` |
| Line or section | Line 60, the second line of the "Documents" comment (lines 59–60) |
| Current (old) | `	// so the SDK is wired directly in DocumentStorageConfig.` |
| Proposed (new) | `	// so the SDK is wired directly in DocumentContainersConfig.` |
| Reason and source | SPEC-016 ("correct the `build.gradle.kts:60` comment"); SPEC-007 (the config class is `DocumentContainersConfig`) |
| Needed by | TASK-19 |

### 0.5 Order and stop rule

Apply SH-01 and SH-03 before TASK-08's green run; SH-02 with or after TASK-16's class deletions and before its green run; SH-04 to SH-06 before TASK-18; SH-07 before TASK-19. The Builder's `plan/tasks.md` "Shared-file dependencies" section carries the same order. If a row is not applied, the Builder stops, reports `SHARED_FILE_DEPENDENCY: SH-nn, <file>` in its run log, and does not edit the file itself. TASK-23 checks that the Builder diff contains none of the six files.

## 1. `aisdlc/requirement/Traceability_Matrix.md` — row 007

Replace the row (the spec stage's §1 already replaces it with the spec reference; this version adds the plan and the task set):

| 007 | `RWB-TE-012` | `BR-RWB-007` | `FR-RWB-007` | `output/INC-007-epic-1-RWB-TE-012/specify/spec.md` v10 (SPEC-001 to -023; FR-RWB-007 → SPEC-001 to -017, -020; REQ-DCM-003 → SPEC-004, -011 to -013; REQ-DCM-002 → SPEC-010, -011, -015; NFR-029 → SPEC-004, -009, -012; NFR-053 → SPEC-001; CTL-12 → SPEC-004, -010 to -014, -018; CTL-09 → SPEC-005, -015); `output/INC-007-epic-1-RWB-TE-012/plan/plan.md` v2 (TASK-00 to TASK-24) and `tasks.md` v2 | Specified and planned — spec v10 and plan v2, 18 Nov 2026; spec gate round 10 PASS; plan gate round 1 FAIL 0C/1H/1M/1L, findings PLAN-001 to PLAN-003 remediated in plan run 2 (plan-gate-review-2 pending); depends on RWB-TE-001 merged |

## 2. Increment card and index (PG-01, PG-02)

Update `aisdlc/docs/increments/INC-007-epic-1-RWB-TE-012.md` "Card status":

| Field | Proposed value |
|---|---|
| Specification | `RUN` — `output/INC-007-epic-1-RWB-TE-012/specify/spec.md` v10, spec gate round 10 PASS |
| Compliance review | Spec gate PASS 0/0/0/0; plan gate round 1 FAIL 0C/1H/1M/1L, remediated in plan run 2; round 2 pending |
| Test cases in story | `13` (TC-TE-012-01 to TC-TE-012-13, story §16) — replaces the stale `0` |
| Plan and tasks | `output/INC-007-epic-1-RWB-TE-012/plan/plan.md` v2 and `tasks.md` v2 (TASK-00 to TASK-24) |
| Status | `Planned` after plan-gate-review-2 passes; not changed by this stage |

Update `aisdlc/docs/increments/INDEX.md` with the same status and the plan path when the plan gate passes. Do not change the story scope text.

## 3. `aisdlc/DOCUMENT-GAPS.md` — rows from this stage

The spec stage's §2 proposes copying DGAP-01 to DGAP-17 and DGAP-19 to DGAP-24 as `DG-<next>` onward (DGAP-18 not copied). Add one plan-stage row:

| Proposed ID | Story | Gap (short) | Second source | Blocker | Owner |
|---|---|---|---|---|---|
| `DG-<next>` | RWB-TE-012 | `AGENTS.md` §7/§9 "touches one module" is undefined; this build reads it as the ACE module under D-RUN-21, ratification OPEN-050 | RWB-TE-001 plan PA-12 and RWB-E1-042 CLAR-025 read it in opposite ways; D-RUN-21; OPEN-050 | No | Recovery tech lead (AGENTS.md §9 "Plan approved" owner) |

PG-01 and PG-02 are workspace-index staleness, not document-set gaps; they are handled in §2 above and do not go to `DOCUMENT-GAPS.md`. PG-04 (SIT apply owner, date and record) is an open item (§4), not a document-set gap.

## 4. `aisdlc/docs/open-items.md` — new rows

The spec stage's §3 rows remain and are applied first. Add:

| ID | Item | Stories affected | Owner | Needed by | Raised in |
|---|---|---|---|---|---|
| OPEN-`<next>` | SIT template apply and the RW-SECADM role listing: name the date, the record and the person who runs the apply. The story "Done when" requires both; no document names the SIT step (PG-04). | RWB-TE-012 | Platform team (RW-PLATADM) with RW-SECADM | SIT exit for the release | INC-007 plan |
| OPEN-`<next>` | `.gitlab-ci.yml` `backend-recovery-it` rules do not include `infra/azure/**` or `backend/src/test/**`, so this MR's Azurite and `RecoveryDatabaseIT` changes would not trigger the job. TE-012 runs `./scripts/dev.ps1 it` as ASM-TE012-23 states; consider adding `infra/azure/**` to the rules. This is audit item A-09, not a TE-012 change (PA-19). | RWB-TE-012 and later P5 stories | RWB-TE-003 / RWB-TE-011 owners | Next pipeline change | INC-007 plan |
| OPEN-`<next>` | Approve the README "Decisions taken while setting this up" item (b) (local emulator mode) at the plan gate before the first code merge; the Builder writes it in the story branch (`../specify/shared-updates.md` §5). No human approval is claimed by this stage. | RWB-TE-012 | Plan-gate reviewer (orchestrator) and the recovery tech lead | Plan gate and merge | INC-007 plan |

Do not duplicate the spec's open items for the template values, the SY-OCR identity, resource logs, storage account and resource group names, the pre-deploy check pipeline step, the template format, E1-024 contract conformance, SCR-44, the archive container, the re-store caller, or health aggregation. They stay as the spec stage wrote them.

## 5. `aisdlc/docs/increments/story-defects.md` — RWB-TE-012 step 5

Keep the proposed resolution text from the spec stage: "Spec INC-007 SPEC-RWB-TE-012-012: hash compared first; same hash returns the existing blob with no write; the conditional upload follows; a concurrent `BlobAlreadyExists` triggers one more hash compare. AC12 is the testable rule." The plan implements it in TASK-13/TASK-14 and tests both branches in T-TE012-05. The status remains the orchestrator's call; this stage does not close the defect row.

## 6. `README.md` — Builder edit in the story worktree (plan-gate item)

The README stays a Builder edit: SPEC-021 names `README.md:25` a "Builder edit", and it is a repository document, not one of the shared Gradle, YAML, `.env`, compose or `dev.ps1` files in §0. The Builder edits line 25 to the P5 `dochub/` line and adds the "Decisions taken while setting this up" item (b), both exactly as `../specify/shared-updates.md` §5 (a) and (b) state. The plan lists them in TASK-19. The plan gate must approve item (b) before any code merges (SPEC-017; round 1 finding SG-11). No approval is recorded here.

## 7. Notes to later-story specifiers (seams, D-RUN-08)

The spec stage's §7 stays authoritative. The plan adds:

| To | Note |
|---|---|
| RWB-E1-024 | The published types and signatures are fixed in `plan/contracts/backend-apis.json`; `DocumentStore`, `StoreRequest` and `StoredDocument` remain free for E1-024. The `documentHub` health component and `DocumentStorage.readiness()` exist after TASK-10/TASK-16. `BLOB_MISSING` maps to 503 MSG-GEN-006 unless E1-024 names another message; no message exists for a missing stored file. |
| RWB-E1-026, RWB-E1-057 | `DocumentContainers.intake()` is public in `dochub.storage`; with the flag off it raises NOT_READY. Azure types in `dochub.casedocs` or `dochub.intake` need those packages in the P5 `clientPackages` (D-RCV-41) or code under `dochub.storage`. |
| RWB-E1-041 | `DocumentContainers.quarantine()` uses SY-OCR and raises NOT_READY when the OCR client ID is blank; the same BND-5 rule applies to `dochub.scan`. |
| RWB-E1-032, RWB-E1-054 | The re-store call is `store()` with `writeOnce=true`, the same `docVersion` and the standard-container `BlobRef` at the same name; the standard object is kept and the caller moves `storage_ref`. The caller step is still DGAP-23. |
| All callers | Only the readiness probe writes readiness; a `store()` while not READY raises NOT_READY or TIMEOUT within `timeout-seconds`, and both map to 503 MSG-GEN-006. `open()` is not an authorization point and a missing blob is BLOB_MISSING. |
| Epic 2 / SCR-44 owner | The `documentHub` component and `DocumentStorage.readiness()` expose the value; the screen is still unowned (DGAP-20). |

## 8. Shared files not edited

This stage did not edit any shared register or configuration file. `aisdlc/requirement/Traceability_Matrix.md`, `aisdlc/docs/open-items.md`, `aisdlc/docs/increments/INDEX.md`, the increment cards, `aisdlc/DOCUMENT-GAPS.md`, the six shared configuration files in §0, `README.md` and every file under the document set are unchanged by this stage. Only `aisdlc/output/INC-007-epic-1-RWB-TE-012/plan/` was written; §0 is the proposal set for the orchestrator, not an edit.

# Shared-file updates proposed by the Technical Specifier — INC-007-epic-1-RWB-TE-012

Revision v4 (spec gate round 3 remediation; v3 kept as `shared-updates.run3.md`, v2 as `shared-updates.run2.md`, v1 as `shared-updates.run1.md`). This stage did not edit any shared file (RUN-BRIEF rule 3). The orchestrator applies these rows in order. IDs marked `<next>` take the next free number in the target register.

## 1. `aisdlc/requirement/Traceability_Matrix.md` — row 007

Replace the row:

| 007 | `RWB-TE-012` | `BR-RWB-007` | `FR-RWB-007` | `output/INC-007-epic-1-RWB-TE-012/specify/spec.md` v4 (SPEC-RWB-TE-012-001 to -023; FR-RWB-007 → SPEC-001 to -017, -020; REQ-DCM-003 → SPEC-004, -011 to -013; REQ-DCM-002 → SPEC-010, -011, -015; NFR-029 → SPEC-004, -009, -012; NFR-053 → SPEC-001; CTL-12 → SPEC-004, -010 to -014, -018; CTL-09 → SPEC-005, -015) | Specified — spec v4 18 Nov 2026; spec gate round 4 in `review/spec-gate-review-4.md` (rounds 1–3 FAIL, all answered in `gate-response.md`); plan not started; depends on RWB-TE-001 merged |

## 2. `aisdlc/DOCUMENT-GAPS.md` — candidate rows

Copy rows DGAP-01 to DGAP-17 and DGAP-19 to DGAP-24 from `specify/document-gaps.md` as `DG-<next>` onward, story RWB-TE-012, all Blocker = No. Do not copy DGAP-18 (withdrawn). Suggested owners: DGAP-01, -02, -17, -19 solution architect; DGAP-03, -07, -11 DL27 owner (solution architect with Compliance); DGAP-04, -05 Compliance with Legal (DL26); DGAP-06, -13 Compliance and security; DGAP-08, -09, -10, -12, -21 platform team; DGAP-14, -15, -16 analyst (story file v7); DGAP-20 product owner (screen inventory and Epic 2 backlog).

## 3. `aisdlc/docs/open-items.md` — new rows

| ID | Item | Stories affected | Owner | Needed by | Raised in |
|---|---|---|---|---|---|
| OPEN-`<next>` | E1-024 must call `DocumentStorage.readiness()` before inserting the document row, so TE-012 AC9 "writes no document row" holds while E1-024 X8 still covers a failure after commit (DGAP-17). | RWB-E1-024, RWB-TE-012 | Analyst with tech lead | E1-024 specify | INC-007 specify |
| OPEN-`<next>` | Account-wide blob versioning and soft delete next to the container-level write-once policy on `rwb-docs-legal`: confirm in an early DEV spike, before SIT (DGAP-03). | RWB-TE-012, RWB-E1-041 | DL27 owner | TE-012 build (DEV) | INC-007 specify |
| OPEN-`<next>` | How the service process obtains the RWB-{ENV}-SY-OCR identity (client ID, workload identity federation) for the quarantine container (DGAP-10). | RWB-TE-012, RWB-E1-041, RWB-E1-057 | Platform team with security | Before SIT | INC-007 specify |
| OPEN-`<next>` | Storage resource logs for refused attempts made directly on the container, not through the service (DGAP-11). | RWB-TE-012, RWB-E1-024 | DL27 owner with security | Before SIT | INC-007 specify |
| OPEN-`<next>` | Storage account region, redundancy SKU, default access tier and encryption key type are template inputs with no documented value (DGAP-05, -06, -07, -13). The platform team also supplies, per environment, the private endpoint subnet ID and the object IDs of the ACE service identity and RWB-{ENV}-SY-OCR; T-TE012-15 fails while any of these is blank in a parameter file. | RWB-TE-012 | Platform team, Compliance | Before SIT | INC-007 specify |
| OPEN-`<next>` | ACE infrastructure template format and folder; this build uses an ARM JSON template with JSON parameter files in `infra/azure/document-storage/` (DGAP-09). | RWB-TE-012 | Platform team | Plan gate | INC-007 specify |
| OPEN-`<next>` | E1-024 conforms to the TE-012 contract: `StoreRequest.intakeBlobRef` and the `BlobRef file` parameters use `dochub.api.BlobRef`; `DocumentStorage.store(BlobWriteRequest)` copies from intake; `storage_ref` is read back with `BlobRef.fromStorageRef` (DGAP-19; SPEC-010, -019). | RWB-E1-024, RWB-E1-026, RWB-E1-032, RWB-E1-041, RWB-E1-049 | Solution architect | E1-024 specify | INC-007 specify (round 1 review input 4) |
| OPEN-`<next>` | No story builds SCR-44 Interface and job monitor, which shows the document hub readiness (TE-012 §4 step 7). Name the owning story (DGAP-20). | RWB-TE-012, RWB-E1-056, Epic 2 | Product owner | Before Epic 2 planning | INC-007 specify |
| OPEN-`<next>` | RWB-E1-017 expects a write-once archive container from RWB-TE-012, "writable by SY-DATALOAD"; TE-012 defines four containers and SY-DATALOAD is retired (D-RCV-35 U1). Decide whether an archive container is added (by which story), which identity writes it, and which `dochub.api` operation P1 uses, since no blob is written except through DocumentStorage (D-RCV-31) (DGAP-22). | RWB-E1-017, RWB-TE-012 | Solution architect with Compliance | RWB-E1-017 specify | INC-007 specify |
| OPEN-`<next>` | No story step re-stores a stored, low-confidence document into rwb-docs-legal when its type is confirmed: D-RCV-31 names the "RWB-E1-054 confirm flow" and RWB-E1-032 BR4 holds the document in rwb-docs until then, but RWB-E1-054 v1 re-types intake items only. Name the step that calls `DocumentStorage.store()` with the standard source and `writeOnce=true`, moves `storage_ref` and writes DOCATT (DGAP-23). | RWB-E1-032, RWB-E1-054, RWB-TE-012 | Solution architect with the analyst | RWB-E1-032 and RWB-E1-054 specify | INC-007 specify |
| OPEN-`<next>` | ACE rule for how a module's health component affects the root `/actuator/health` status (DGAP-21). TE-012 uses `UNKNOWN` when off and `DOWN` when not ready. | RWB-TE-012 and later modules with health components | Platform team | Before SIT | INC-007 specify |

Existing rows to reference, not duplicate: OPEN-010 (retention not signed) for DGAP-04.

## 4. `aisdlc/docs/increments/story-defects.md` — RWB-TE-012 step 5 row

Proposed resolution text (status stays the orchestrator's call): "Spec INC-007 SPEC-RWB-TE-012-012: hash compared first; same hash returns the existing blob with no write; the conditional upload follows; a concurrent `BlobAlreadyExists` triggers one more hash compare. AC12 is the testable rule."

## 5. `README.md` — Builder edits in the story worktree (plan-gate item)

The README is edited in the code repository by the Implementation Builder in the RWB-TE-012 branch, not by this stage. The plan gate must approve item (b) before any code merges (SPEC-017; round 1 finding SG-11).

(a) Line 25 (code tree): replace "`documents/             Azure Blob DocumentStore, write-once container for legal types`" with "`dochub/                P5 document hub: published DocumentStorage (api/), Blob adapter and readiness (storage/)`". If RWB-TE-001 has already rewritten the tree, change only the P5 line.

(b) "Decisions taken while setting this up" — new item: "**Local document storage.** Azurite has no managed identity and no immutability policy. Emulator mode is on only when all five conditions hold: the `local` Spring profile is active; `rwb.dochub.storage.emulator=true` (the property alone is not a guard, because an environment variable can override it); `RWB_DOCHUB_EMULATOR_CONNECTION_STRING` is non-blank; its account is `devstoreaccount1`; and its blob host is `127.0.0.1`, `localhost` or `azurite`. In that mode the service uses one shared-key client for all four containers, creates them at startup (it still starts when Azurite is down), reports the legal policy and the identity checks as `EMULATED` (no managed-identity client ID is needed), and write-once is the conditional upload plus the hash guard. SIT, UAT and PROD use managed identity and the template (RWB-TE-012 SPEC-017). Precedent: the 'Local versus target' Blob row."

(c) "Local versus target" Blob row: no change needed; it already states the local conditional write.

## 6. Environment and Deployment Design v4 §6 / §6.1 (document owner, not this repository)

For the document owner via DOCUMENT-GAPS (DGAP-12): add flag `rwb.dochub.storage-containers` (owner P5, story RWB-TE-012) and the `rwb.dochub.*` parameters.

## 7. Notes to later-story specifiers (seams, D-RUN-08)

| To | Note |
|---|---|
| RWB-E1-024 (order 42) | `dochub.api` holds `DocumentStorage`, `BlobRef`, `BlobWriteRequest`, `StoredBlob`, `StorageReadiness`, `WriteOnceViolationException`, `StorageUnavailableException`. The names `DocumentStore`, `StoreRequest` and `StoredDocument` are free for E1-024. If E1-024 publishes types in a P5 published package, it updates T-TE001-14's expected list and the map in its own merge request. Call `readiness()` before inserting the row. `store()` does not delete the intake blob. |
| RWB-E1-026 (58), RWB-E1-057 (61) | Intake writes use `DocumentContainers.intake()` in `dochub.storage`; with the flag off it throws `StorageUnavailableException(NOT_READY)`. Code in `dochub.casedocs` or `dochub.intake` that touches `com.azure.storage` must be added to the P5 `clientPackages` by that story (D-RCV-41) or sit under `dochub.storage`. |
| RWB-E1-041 (54) | `DocumentContainers.quarantine()` uses SY-OCR; same BND-5 rule for `dochub.scan` and `dochub.retention`. |
| RWB-E1-049 (49) | `open()` refuses intake refs; OCR of intake files reads through `DocumentContainers` under the same BND-5 rule. |
| RWB-E1-032 (63), RWB-E1-054 (70) | Legal re-store (D-RCV-31): `store()` with `writeOnce=true`, the same `docVersion`, and `source` = the current standard-container `BlobRef` at `{caseId}/{documentId}/v{docVersion}`. The standard object is kept; the caller moves `storage_ref` to the returned ref and writes the DOCATT entry. RWB-E1-054 v1 has no step that does this for a stored document; the open item in §3 (DGAP-23) must name it. |
| All callers of `store()` | `store()` refuses within `timeout-seconds` (10 s) when the hub is not READY: `NOT_READY` (probe found a problem, or a fresh NOT_READY result is reused for `readiness-recheck-seconds`) or `TIMEOUT` (probe still running at the caller's deadline). Both map to 503 MSG-GEN-006 (SPEC-009). |
| RWB-E1-017 (17) | No archive container is delivered by TE-012 (DGAP-22). A P1 writer cannot use `DocumentContainers` (P5 internal, BND-5); it needs a `dochub.api` operation and a writer identity, both open. |
| All callers of `open()` | `open()` is not an authorization point: apply the Documents R right and scope check, and the PII access-log entry (RWB-E1-024 step 8, §17; RWB-E1-039). |

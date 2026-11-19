# Shared-file updates proposed by the Technical Specifier — INC-007-epic-1-RWB-TE-012

This stage did not edit any shared file (RUN-BRIEF rule 3). The orchestrator applies these rows in order. IDs marked `<next>` take the next free number in the target register.

## 1. `aisdlc/requirement/Traceability_Matrix.md` — row 007

Replace the row:

| 007 | `RWB-TE-012` | `BR-RWB-007` | `FR-RWB-007` | `output/INC-007-epic-1-RWB-TE-012/specify/spec.md` (SPEC-RWB-TE-012-001 to -019) | Specified — spec 17 Nov 2026; source REQ-DCM-003, REQ-DCM-002, D-RCV-31; spec gate in `review/spec-gate-review.md`; plan not started |

## 2. `aisdlc/DOCUMENT-GAPS.md` — candidate rows

Copy rows DGAP-01 to DGAP-18 from `specify/document-gaps.md` as `DG-<next>` onward, story RWB-TE-012, all Blocker = No. Suggested owners: DGAP-01, -02, -17, -18 solution architect; DGAP-03, -07, -11 DL27 owner (solution architect with Compliance); DGAP-04, -05 Compliance with Legal (DL26); DGAP-06, -13 Compliance and security; DGAP-08, -09, -10, -12 platform team; DGAP-14, -15, -16 analyst (story file v7).

## 3. `aisdlc/docs/open-items.md` — new rows

| ID | Item | Stories affected | Owner | Needed by | Raised in |
|---|---|---|---|---|---|
| OPEN-`<next>` | E1-024 must call `DocumentStorage.readiness()` before inserting the document row, so TE-012 AC9 "writes no document row" holds while E1-024 X8 still covers a failure after commit (DGAP-17). | RWB-E1-024, RWB-TE-012 | Analyst with tech lead | E1-024 specify | INC-007 specify |
| OPEN-`<next>` | Account-wide blob versioning and soft delete next to the container-level write-once policy on `rwb-docs-legal`: confirm at template apply in DEV and SIT (DGAP-03). | RWB-TE-012, RWB-E1-041 | DL27 owner | Before SIT | INC-007 specify |
| OPEN-`<next>` | How the service process obtains the RWB-{ENV}-SY-OCR identity (client ID, workload identity federation) for the quarantine container (DGAP-10). | RWB-TE-012, RWB-E1-041, RWB-E1-057 | Platform team with security | Before SIT | INC-007 specify |
| OPEN-`<next>` | Storage resource logs for refused attempts made directly on the container, not through the service (DGAP-11). | RWB-TE-012, RWB-E1-024 | DL27 owner with security | Before SIT | INC-007 specify |
| OPEN-`<next>` | Storage account region, redundancy SKU, default access tier and encryption key type are template inputs with no documented value (DGAP-05, -06, -07, -13). | RWB-TE-012 | Platform team, Compliance | Before SIT | INC-007 specify |
| OPEN-`<next>` | ACE infrastructure template format and folder; this build uses Bicep in `infra/azure/document-storage/` (DGAP-09). | RWB-TE-012 | Platform team | Plan gate | INC-007 specify |

Existing rows to reference, not duplicate: OPEN-010 (retention not signed) for DGAP-04.

## 4. `aisdlc/docs/increments/story-defects.md` — RWB-TE-012 step 5 row

Proposed resolution text (status stays the orchestrator's call): "Spec INC-007 SPEC-RWB-TE-012-012: hash compared first; same hash returns the existing blob with no write; the conditional upload follows; a concurrent `BlobAlreadyExists` triggers one more hash compare. AC12 is the testable rule."

## 5. `README.md` "Decisions taken while setting this up" — new item (Builder adds it in the worktree)

"**Local document storage.** Azurite has no managed identity and no immutability policy. In DEV only, with the Azurite development account on a loopback or `azurite` host, the service uses the emulator connection string, creates the four containers at startup and reports the legal policy as `EMULATED`; write-once is the conditional upload plus the hash guard. SIT, UAT and PROD use managed identity and the template (RWB-TE-012 SPEC-017)."

## 6. Environment and Deployment Design v4 §6 / §6.1 (document owner, not this repository)

For the document owner via DOCUMENT-GAPS (DGAP-12): add flag `rwb.dochub.storage-containers` (owner P5, story RWB-TE-012) and the `rwb.dochub.*` parameters.

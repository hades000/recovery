# Shared-file updates proposed by the Implementation Planner — INC-007-epic-1-RWB-TE-012

This stage did not edit any shared file (RUN-BRIEF rule 3). The orchestrator applies these rows in order. IDs marked `<next>` take the next free number in the target register. The spec stage's proposals (`../specify/shared-updates.md` v10) are applied first; this file adds the plan-stage rows and does not repeat them.

## 1. `aisdlc/requirement/Traceability_Matrix.md` — row 007

Replace the row (the spec stage's §1 already replaces it with the spec reference; this version adds the plan and the task set):

| 007 | `RWB-TE-012` | `BR-RWB-007` | `FR-RWB-007` | `output/INC-007-epic-1-RWB-TE-012/specify/spec.md` v10 (SPEC-001 to -023; FR-RWB-007 → SPEC-001 to -017, -020; REQ-DCM-003 → SPEC-004, -011 to -013; REQ-DCM-002 → SPEC-010, -011, -015; NFR-029 → SPEC-004, -009, -012; NFR-053 → SPEC-001; CTL-12 → SPEC-004, -010 to -014, -018; CTL-09 → SPEC-005, -015); `output/INC-007-epic-1-RWB-TE-012/plan/plan.md` v1 (TASK-00 to TASK-24) | Specified and planned — spec v10 and plan v1, 18 Nov 2026; spec gate round 10 PASS; plan gate not run at the time of writing (orchestrator runs it); depends on RWB-TE-001 merged |

## 2. Increment card and index (PG-01, PG-02)

Update `aisdlc/docs/increments/INC-007-epic-1-RWB-TE-012.md` "Card status":

| Field | Proposed value |
|---|---|
| Specification | `RUN` — `output/INC-007-epic-1-RWB-TE-012/specify/spec.md` v10, spec gate round 10 PASS |
| Compliance review | Spec gate PASS 0/0/0/0; plan gate pending at the time of writing |
| Test cases in story | `13` (TC-TE-012-01 to TC-TE-012-13, story §16) — replaces the stale `0` |
| Plan and tasks | `output/INC-007-epic-1-RWB-TE-012/plan/plan.md` v1 and `tasks.md` v1 (TASK-00 to TASK-24) |
| Status | `Planned` after the plan gate; not changed by this stage |

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

## 6. `README.md` — Builder edits in the story worktree (plan-gate item)

The README is edited by the Builder in the RWB-TE-012 branch, not by this stage: line 25 becomes the P5 `dochub/` line and the "Decisions taken while setting this up" section gains item (b), both exactly as `../specify/shared-updates.md` §5 (a) and (b) state. The plan lists them in TASK-19. The plan gate must approve item (b) before any code merges (SPEC-017; round 1 finding SG-11). No approval is recorded here.

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

`aisdlc/requirement/Traceability_Matrix.md`, `aisdlc/docs/open-items.md`, `aisdlc/docs/increments/INDEX.md`, the increment cards, `aisdlc/DOCUMENT-GAPS.md`, `README.md` and every file under the document set are unchanged by this stage. Only `aisdlc/output/INC-007-epic-1-RWB-TE-012/plan/` was written.

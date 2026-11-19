# Document gaps — RWB-TE-003 specify (INC-005-epic-1-RWB-TE-003, remediation 1)

Candidate gaps for the orchestrator to number into `aisdlc/DOCUMENT-GAPS.md`. The document set was not edited.

Paths are relative to `17 AI-First SDLC Repository v2/requirement/legacy/`. "Story v7" = `04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-003-types-and-contract-tests-from-the-api-specification-v1.md`.

Precedence applied: D-RCV-35/36 → ADR v3 → Decision Log v10 → story files v7 → older documents (`RUN-BRIEF.md`).

**Blockers: 0.**

## Carried from the gate (`review/document-gaps.md`)

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why (blocker or not) | How this stage proceeded |
|---|---|---|---|---|---|---|
| TE003-SG-DG-01 | Story v7 §12 "Front end generation", §13 Package | Front-end types and client in `src/modules/recovery/api/generated`. | Frontend standards FS-4.2 ("generated types from `@/api/schema`; no duplicate"); `frontend/package.json` `api:generate` → `src/api/schema.d.ts` | No | D-RCV-39 allows both; FS-4.2 needs one set; location is build configuration. | Kept the existing location (SPEC-006, -007). |
| TE003-SG-DG-02 | Story v7 §12 "one interface per tag" | Conflicts with §17 G3 of the same story. | API Specification v4 tags vs `x-module` (`Administration`, `Cases`, `Treatment` cross modules) | No | §6 makes generator settings build configuration; G3 and AGENTS §3.3 are musts. | One interface per operation, abstract only (spec §7.1). |
| TE003-SG-DG-03 | Story v7 §12 "Spring Boot 3"; Technical Enabler Build Notes v2, RWB-TE-003 | Boot 3 target. | `backend/build.gradle.kts` Spring Boot 4.1.2; README decision 2 | No | Generator option, not a business rule; repository line governs. | Target Boot 4.1.2 / Jackson 3; spike S-1 (spec §9). |
| TE003-SG-DG-04 | API Specification v4 `components.responses`, `Problem`; Error and Message Standard v4 §4 | No 500 response, `Problem` has no `required`, no message ID for an unexpected error. | Backend standards BS-3.3 (message ID and trace ID on errors) | No | 500 fails as undocumented; `messageCode`/`traceId` asserted explicitly. | SPEC-011, -013; 500 message ID to NEW-TE003-B. |
| TE003-SG-DG-05 | Story v7 §2 "79 operations"; Technical Enabler Build Notes v2 | Stale count. | API Specification v4: 141 operations (73 E1) | No | Count read from the file. | SPEC-008 (OPEN-039). |
| TE003-SG-DG-06 | Story v7 §4 step 5, AC5 vs §13 "Done when" | Strict fail vs "pending with a named story". | Story Defects Epic 1, Epic 2 and Enablers v4, RWB-TE-003 step 8 row (Open) | No | L-RCV-11 baseline; premise restated (spec §4). | SPEC-009. |
| TE003-SG-DG-07 | Story v7 §2, BR3 source "AC-P2-001-01" | AC-P2-001-01 is the INT-25 file-interface contract test. | FSD P2 Integration v3, AC-P2-001-01 | No | BR3 stands on REQ-DRI-007. | Not claimed. |
| TE003-SG-DG-08 | Story v7 BR5 source "ADR-006" | ADR-006 does not state the rule. | ADR v3, ADR-006 (Proposed) | No | BR5 binds on its own. | Applied as written. |

## New in this run

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why (blocker or not) | How this stage proceeded |
|---|---|---|---|---|---|---|
| TE003-SP-DG-01 | Story v7 §3, §12 Input: `api/recovery-api.yaml` | File name differs from the repository and the document-set name. | Repository `api/recovery-api-v4.yaml` (read by `api:generate`); document set `05-technical-architecture/recovery-workbench-api-specification-v4.yaml` | No | Same content (SHA-256 equal); name is repository layout. | Kept `recovery-api-v4.yaml` (ASM-TE003-01). |
| TE003-SP-DG-02 | Story v7 §11, §13 Database: "in-memory PostgreSQL-compatible test database" | No in-memory database in this repository. | OPEN-007 ruling (no H2; Testcontainers); D-RCV-44 (Testcontainers outside `check`) | No | Local decisions settle it; contract fixtures need no rows. | MockMvc context with stubbed collaborators (spec §7.4, ASM-TE003-10). |
| TE003-SP-DG-03 | API Specification v4, operations without 400 and 422 (e.g. `getCasesCaseidTimers`: 200, 401, 403, 404, 503) | No status is given for a malformed request on most operations (400 on 4, 422 on 64 of 141). | AGENTS §3.6 (validation messages from the message table); README decision 5 (message table not seeded) | No | TE-003 enforces one operation with no input; mapping belongs to the first story with input. | A-08 validation part excluded (spec §3.1); NEW-TE003-C. |
| TE003-SP-DG-04 | Testing standards §1 Security row (dependency scan, ZAP baseline) | No Epic 1 TE story owns these jobs. | Epic 1 Story Files v7 TE-001..TE-013 (TE-011 is PDPA lint only); Phase-0 audit A-09 | No | Not a TE-003 requirement; hardening owner exists in the audit rule. | Excluded (spec §3.1); NEW-TE003-D. |
| TE003-SP-DG-05 | Error and Message Standard v4 §3 ("formatted for the language"), §4 MSG-P4-002 `{action}` | No source gives Thai (or per-call) values for `{action}`. | RWB-E1-022 v7 AC2 ("action 'read roles'"); `ApiExceptionHandler` fills "do this" in both languages | No | E1-022 owns the 403 refusal text. | Access suite asserts `messageCode` only; excluded to E1-022 (OPEN-040 amendment). |
| TE003-SP-DG-06 | Story v7 §13 Package: `<ACE base package>.recovery.generated.web` / `.model` | Story puts generated code at the recovery root. | L-RCV-14 (generated packages are P2 published packages) | No | Local ruling settles it. | `<P2>.generated.*` (SPEC-003, -018). |

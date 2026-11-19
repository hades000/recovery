# Document gaps — Technical Documenter, RWB-E1-042

RUN_ID `INC-003-epic-1-RWB-E1-042`. Candidates for `aisdlc/DOCUMENT-GAPS.md`; not numbered DG-nnn
here. None blocks the story. No approval recorded (D-RUN-09).

## 1. Document-set gaps (carried and new)

| Candidate | Document (name, version, section) | Gap | Blocker | Code behaviour now |
|---|---|---|---|---|
| DG-E042-ENV-422 | API Specification v4, `GET /admin/parameters` | Responses list 200, 401, 403, 503 only; `environment` has no enum. The code answers 422 MSG-GEN-002 (field `environment`, min DEV, max PROD) for any other value (DEV-14; SEC-042-01). E422 already defines MSG-GEN-002 | No | 422 before any read |
| OI-E1-042-011 (identical repeat) | API Specification v4, `postAdminReferenceLoads` | The response to an identical repeat load is not stated; also missing `required`, `format: date`, LOV on `table` | No | Spec default: 201 with the existing load, `repeat=true` |
| DG-E042-ROLLBACK-EVENT | Event and Messaging Design v4; spec §12.8 | `ParameterLoadRolledBack` is still published inside the rollback transaction, while the approval event is after commit | No | In-process only; must move after commit when RWB-TE-006 adds the outbox |
| Event `ParameterVersionApproved` | Event and Messaging Design v4 | Event not listed (CLAR-016) | No | In-process event, fields per spec §11.4 |
| Credential word list | Spec §7.1 (story-derived); Personal Data Protection Design | §7.1 lists 11 substrings; the code refuses 17 (adds `connection-string`, `connectionstring`, `pwd`, `accountkey`, `passphrase`, `sas-token`; DEV-15) | No | Stricter than the spec |
| Three `parameter_value` columns | Physical Schema v6 lines 1386–1434 | `load_id`, `content_hash`, `rollback_reason` not in v6 (OI-E1-042-008) | No | Added by the migration with guards |
| Event publication table | Physical Schema v6 | No `event_publication` table for Spring Modulith's registry (DG-E1042-IM-01; OI-E1-042-012; DEV-08) | No | afterCommit synchronization instead |
| DG-E1042-IM-02, DG-E1042-IM-03 | as recorded in `implement/document-gaps.md` | Carried unchanged | No | — |
| Message table | Error and Message Standard v4 | No message table or owner (OI-E1-042-004); 503 on GET has no message ID | No | `FixedMessageCatalog`; status-only 503 |
| Access matrix | Users, Roles and Permissions v4 | Matrix PM-2026.11 and the RW-PHONECOL identity are other stories' (TC-E1-042-12 Blocked, OI-E1-042-001) | No | Interim grants file |

## 2. Run decisions not ratified

D-RUN-18, D-RUN-19 (`CatalogParameterReader`), D-RUN-20 (PARAMETER dispatcher branch) and D-RUN-21
("one module" = the ACE module) are orchestrator decisions (OPEN-050). OPEN-016: no per-story approver,
so no human sign-off is recorded. Blocker No.

## 3. Post-gate drifts between the run's evidence files

These are inconsistencies inside the run's artefacts, not document-set gaps.

| # | Where | Drift |
|---|---|---|
| 1 | `implement/implementation-report.md`; branch migration file | The file is `V0001__…` on the branch; the report says `<seq>` is unfixed. Docs write `V<seq>` (D-RUN-07); renumber at merge |
| 2 | `implement/traceability.md` CODE-08 | "11 constants"; generated `ParameterKeys` has 19 |
| 3 | `api-tests/report.md` header | Says tip `9056ed2` / run4; run table says run5 at `25c8f94` is current |
| 4 | `implement/shared-updates.md` §5 | Garbled advisory-lock text ("author-supplied? no: content hash"); code locks `validFrom + "|" + hash`; DEV-13 says `hashtext(:key)` |
| 5 | `implement/shared-updates.md` §2 | Cites `implementation-builder/implement/traceability.md` (no such path) |
| 6 | Spec §12.8, SPEC-018 vs code | `@TransactionalEventListener(AFTER_COMMIT)` in the spec; afterCommit synchronization in the code (DEV-08) |
| 7 | `plan/tests/scenarios.md` | Six planned method names do not exist (TC-04, -10(b), -17, -28, -32, -44); CODE3-001; mapped by DEV-20, closed in code gate round 4 |
| 8 | `implement/merge-gate.log`, `implement/review-fix/merge-gate.log` | Predate tip `25c8f94`; superseded by `code-gate-fix/round2/` |

**Known evidence issues (open; builder files not edited by this stage):** rows 2 (CODE-08 constant
count), 4 and 5 (`implement/shared-updates.md` §5 lock text, §2 path) and 8 (stale merge-gate logs).
None affects code, tests or the gate result. Proposed corrections: `shared-updates.md` SU-DOC-E042-07, -09.

# Document gaps: RWB-E1-042 specification, revision 3

RUN_ID `INC-003-epic-1-RWB-E1-042`, stage `specify`, 2026-11-17. Candidate rows for `aisdlc/DOCUMENT-GAPS.md`;
the orchestrator numbers them (rows also listed in `shared-updates.md` §2).

- Precedence: D-RCV-35 and D-RCV-36, then ADR v3, then Decision Log v10, then story files v7, then older maps.
- `legacy/` = `<docset>/17 AI-First SDLC Repository v2/requirement/legacy/`. `docs/` and `.github/` are under `<repo>/aisdlc/`.
- The review stage's E1042-RV-DG-01 to -15 (`review/document-gaps.md`) are carried, not repeated; this file
  states how the spec now proceeds on each and adds the new gaps.

**Blockers: none.** Every row below is settled by precedence or a documented default.

## New gaps raised by this stage

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why (blocker or not) | How this stage proceeded |
|---|---|---|---|---|---|---|
| E1042-SP-DG-01 | User Stories Epic 1 Story Files v7, RWB-E1-042 §13 (`legacy/04-user-stories/...-v7_extracted/rwb-e1-042-...-v1.md`): environment settings "come from the environment and the secret store; only their catalog entries are in the tables" | AC8 of the same story loads table values (30 SIT, 300 PROD) for `refdata.cache.ttl-seconds`, an ENVIRONMENT-kind key | Same story §7 AC8 and §3 (default 300) | No | AC8 is a testable criterion; story §6 allows catalog columns to be tuned | Added `value_source` column (A-03, CLAR-014): TABLE unless the setting already comes from a Spring property or the secret store |
| E1042-SP-DG-02 | Story v7 RWB-E1-042 §5 X3 ("does not start") | AC4 says the health check fails and no traffic is routed | Same story §7 AC4 | No | AC4 is the testable statement; the process stays up | Readiness DOWN (SPEC-016, CLAR-012) |
| E1042-SP-DG-03 | Users, Roles and Permissions v4, matrix sheet (`legacy/02-business-architecture-and-process/recovery-workbench-users-roles-and-permissions-v4-xlsx.md` lines 73-110) | No role holds Reference data A, which approve requires | API Specification v4 `postAdminReferenceLoadsLoadidApprove` (line 3232); story v7 §3 line 41 (owner and RW-RISK, DL01) | No | The endpoint and its capability check are RWB-E1-043's (D-RUN-10); this story enforces author <> approver regardless of role | Recorded for RWB-E1-043 and RWB-E1-037 (CLAR-013, A-13); carries review finding 118 |
| E1042-SP-DG-04 | Story v7 RWB-E1-042 §12, event `ParameterVersionApproved` payload `(paramKeys, versionNo, validFrom)` | One `versionNo` cannot describe a load of several keys and environments, which the same story's load format allows (`key,environment,value` rows) | Story §12 load endpoint; pack §3.3 | No | The story owns the payload; a per-row version list keeps its intent | §11.4 delta (A-21, CLAR-016); event catalog update requested |
| E1042-SP-DG-05 | RWB-E1-043 v7 §3 line 45 (business date from `v_ace_batch_status`) | RWB-E1-042's load check (valid-from not before the business date) needs a business date, but the view arrives with RWB-E1-069 (order 10) after this story (order 3); story RWB-E1-042 does not name a source | Build Sequence v6 (`docs/increments/build-sequence.md`); story RWB-E1-042 §12 | No | D-RUN-08: later work is a seam | `BusinessDateProvider` seam, interim Asia/Bangkok date (A-20, CLAR-015) |
| E1042-SP-DG-06 | E1-042 Clarification Pack (10 Nov 2026) messages CSV, MSG-P4-001 Thai text (`legacy/e1-042-migration-and-clarifications/rwb-e1-042-clarification-pack.md`; `_v2-baseline/implement/`) | The pack's Thai differs from the Standard | Error and Message Standard v4 line 163 (`legacy/07-screens-and-experience/recovery-workbench-error-and-message-standard-v4-docx.md`) | No | The Standard outranks a draft pack | Standard v4 text used (§10.1) |
| E1042-SP-DG-07 | RWB-E1-043 v7 §3 line 41: needs RWB-E1-042 to serve "the list of reference table codes" | RWB-E1-042 v7 specifies no table-code list; LOV-REF-TABLE is RWB-E1-043's reference data | Story RWB-E1-042 §12 (no such interface); run decisions D-RUN-10, D-RUN-11 (`AI-SDLC-BUILD-LOG.md` lines 33-34) | No | D-RUN-10/11 place dispatch and the handler map in RWB-E1-043 | Not served here; `ParameterLoadHandler.TABLE = "PARAMETER"` (CLAR-022) |
| E1042-SP-DG-08 | API Specification v4 `postAdminReferenceLoads` (shared endpoint for all table codes) and story v7 RWB-E1-042 §12 ("P4 endpoint; this story builds the PARAMETER handler") | No document states which story owns the shared endpoint or how it dispatches to the `PARAMETER` handler (gap G-R05 in the run log) | RWB-E1-043 v7 §6 line 75 ("The P4 load endpoint calls this story's interface"); Build Sequence v6 (RWB-E1-043 order 8 after RWB-E1-042 order 3) | No | Run decision D-RUN-10 settles it: RWB-E1-043 owns the endpoint and calls RWB-E1-042's published interface | `ParameterLoadHandler` in `platform.api`; endpoint is a seam (SPEC-017, §11.2). Supersedes the registry option in E1042-RV-DG-15 |
| E1042-SP-DG-09 | Error and Message Standard v4 (line 56, messages "held in the message table") | No message exists for an unknown reference load (`loadId`), nor a settled 503 ID | API v4 approve/rollback 404 response (no message ID); pack §3.6 (MSG-GEN-006 candidate) | No | Existing MSG-P4-003 and the pack candidate are documented defaults | A-15, A-16 (CLAR-019, CLAR-021) |

## Carried gaps (review stage) and how the spec now proceeds

| Carried ID | Blocker? | Spec revision 3 |
|---|---|---|
| E1042-RV-DG-01 (two migration files) | No | One file `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql` (SPEC-001) |
| E1042-RV-DG-02 (V0001 reserved vs merge order) | No | No number fixed (D-RUN-07); raised for RWB-E1-001 in `shared-updates.md` |
| E1042-RV-DG-03 (D-RCV-34 ID clash) | No | Not used |
| E1042-RV-DG-04 (seed ownership in squad map) | No | Seed in this story's migration (SPEC-006) |
| E1042-RV-DG-05 (no load-to-rows link) | No | `load_id`, `content_hash`, `rollback_reason` (SPEC-002, A-18); Physical Schema update requested |
| E1042-RV-DG-06 (full Epic 1 catalog absent) | No | 19-row bootstrap (A-06) |
| E1042-RV-DG-07 (no message table) | No | `MessageResolver` with fixed catalog (A-14) |
| E1042-RV-DG-08 (event not in catalog) | No | Delta §11.4 |
| E1042-RV-DG-09 (PRODUCT rows have no default) | No | Exempt (SPEC-003) |
| E1042-RV-DG-10 (D-RCV-36 keys under-specified) | No | §12.4 with labelled assumptions A-07..A-10 |
| E1042-RV-DG-11 (PK and FK differ from v6) | No | Follow v6; additions listed (§12.3) |
| E1042-RV-DG-12 (`${schema}` placeholder) | No | `${recoverySchema}` only |
| E1042-RV-DG-13 (backend-context V0042 / "Implemented") | No | Not used; correction requested |
| E1042-RV-DG-14 (TC-12 needs later stories) | No | TC-12 Blocked with exit criterion |
| E1042-RV-DG-15 (who builds the P4 endpoint) | No | Superseded by E1042-SP-DG-08 / D-RUN-10 |

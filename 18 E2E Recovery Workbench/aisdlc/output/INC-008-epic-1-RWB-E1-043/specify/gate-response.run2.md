# Gate response: RWB-E1-043 spec gate round 1 (INC-008-epic-1-RWB-E1-043)

Remediation run 1, 2026-11-18. Technical Specifier response to `review/spec-gate-review.md` (round 1,
FAIL: 3 High, 7 Medium, 9 Low, gaps G-R01..G-R10). The review file is not edited. Files revised in
place; each was first copied to `<name>.run1.md`.

**Triage.** The triage below was given by the orchestrator, Claude Code, an AI agent, as run rulings
D-RUN-09 (fix every finding, Lows included), D-RUN-10 (this story owns the shared endpoint and
dispatches by table code; PARAMETER goes only through RWB-E1-042's published interface; the dispatch gap
is Blocker = No), D-RUN-11 (this story publishes the handler registry) and a cross-story input on
dictionary loads. No human gave these rulings; they are not human acceptance. Owner acceptance of the
behaviour-changing assumptions is still required at the plan gate (finding 116).

Abbreviations: SPEC-nnn = SPEC-RWB-E1-043-nnn in `spec.md` revision 2; A-nn in `assumptions.md`;
GAP-nn in `document-gaps.md`; SU = `shared-updates.md`.

## 1. Findings

| Finding | Sev | Resolution | Where |
|---|---|---|---|
| 101 Rollback dropped but COVERED | High | Option (a): rollback is **built and tested here**. Registry `rollback(loadId, actorUserId, reason)`, endpoint `POST /admin/reference-loads/{loadId}/rollback` (API4 `RollbackRequest`), preconditions in order (reason, unknown, repeat, not approved, not latest, no earlier → MSG-P3-015, handler without rollback), effect on status, `rollback_reason`, `valid_to` of the restored version, cache eviction, handler `onRolledBack`. S7 §9 and FR-RWB-011 rows now point at SPEC-024. GAP-10 corrected: D-RUN-10 places the endpoint here; RWB-E1-019 implements `onRolledBack` and drops its build step 5. Status line counts corrected: 50 rows, CONTRADICTIONS 26 (equal to the C-type gaps) | SPEC-001 (`rollback_reason`, CHECK), SPEC-024, SPEC-013; TC-RB-01, TC-RB-02; A-27; GAP-10, GAP-20; SU RWB-E1-019 row |
| 102 Version logging vs AC3/BR7 | High | Logging is bound to the reader, not the cache fill: `ReferenceDataReaders.forReader(name)` writes one INFO line `event=REFERENCE_READ reader= table= version= validFrom= businessDate=` per `(reader, table, version, businessDate)` per TTL window, on hit and miss alike. The engine is named by a non-personal component name. TC-E1-043-03 now uses two consumers on one cache and asserts one line per consumer per table | SPEC-014; A-29; TC-E1-043-03; SU engine-stories row |
| 103 Shared endpoint with RWB-E1-042 | High | D-RUN-10: this story owns the controller and dispatches by table code. `PARAMETER` → RWB-E1-042's published `ParameterLoadHandler` only (load, approve, rollback, find) through an `ObjectProvider`; approve and rollback resolve `loadId` in `reference_version` first, then `ParameterLoadHandler.find`, else 404. "Later story" wording removed. The 12 column definitions are catalog keys added through RWB-E1-042's catalog file and loaded as PARAMETER values through this endpoint before the first table load. GAP-24 recorded with Blocker = No per D-RUN-10 | SPEC-015, 016, 018, 022, 026, 029, 030; A-14, A-25, A-28; GAP-24, GAP-35; TC-PB-01, TC-FL-01 |
| 104 Rights per area only | Medium | Fail closed per table: besides the area right (RWB-E1-042 `CapabilityCheck` + interim grants rows), the caller's role must be in `rwb.refload.loader.<code>` (load, rollback) or `rwb.refload.approver.<code>` (approve); a missing key or empty value refuses. RW-COE gets no built-in table until ownership data names one. Per-table approver conflict recorded | SPEC-027, SPEC-029; A-08, A-31; GAP-19, GAP-22; SEC-06, SEC-08, SEC-10, SEC-11 |
| 105 Story lines missing from coverage | Medium | Each line now has an owner in "Requirement lines built by another story": separation of duty RWB-E1-022/037; SY-RULES RWB-E1-072; RW-AUDIT read and GET lists (owner to be named, GAP-34); DQ report RWB-E1-011 (GAP-33); BR6 sentence 2 engine part RWB-E1-018/020/028 with RWB-E1-027. S7 §10 row corrected | spec.md §Coverage, §Requirement lines built by another story; SU open items |
| 106 Audit of admin actions and refusals | Medium | `ReferenceLoadAudit` port with interim `LoggingReferenceLoadAudit`: one `event=REFERENCE_LOAD_AUDIT` line per load, approve and rollback, done and refused, with no user ID. TC-E1-043-11 "the refusal is logged" restored. RWB-E1-039 replaces the adapter (seam, open item) | SPEC-028; A-30; GAP-26; TC-E1-043-11, SEC-05..SEC-11; SU RWB-E1-039 row |
| 107 Catalog rows bypass RWB-E1-042 | Medium | 38 rows added to RWB-E1-042's `config/parameter-catalog.csv` in this story's pull request for the catalog owner's review; generator emits the keys; every row has owner, type, default, environments, used-by; `required=false` keeps RWB-E1-042 BR7 green; GLOBAL rows have a default (`none` / role lists) so `CatalogCompletenessCheck` passes. Same rows in the migration with `ON CONFLICT` | SPEC-001, SPEC-029; A-09, A-34; GAP-13, GAP-23, GAP-30; TC-CAT-01 |
| 108 RWB-E1-001 not told | Medium | SU open item to RWB-E1-001 citing both sources (Physical Schema v6 lines 8, 1437, 1471-1483; DL10 D-RCV-28 with BS6 orders 8 and 9): no plain `CREATE TABLE` for the two tables, no `uk_reference_row UNIQUE (row_key)`, guard or leave to this story, per-version key in its dictionary rows and tests; required order E1-043 first; numbers at merge (D-RUN-07, GAP-15) | SU §3 first row; GAP-01, GAP-02, GAP-15, GAP-25 |
| 109 RWB-E1-019 missing from GAP-08 | Medium | D-RUN-11 places the per-table hook in the registry (`ReferenceTableHandler.validate`, `apply`, `onRolledBack`). GAP-08 now names `ReferenceTableCheck`, `ReferenceRollbackHandler` and `QueueVersionApplier` and maps them onto the SPI. "First row" vs "every row" recorded; `detail` lists every failed row (max 100) and `{check}` names the first | SPEC-003, SPEC-025; A-11; GAP-08, GAP-21; SU RWB-E1-019 row |
| 110 Security tests | Medium | SEC-01..SEC-14 per endpoint: missing method check (reflection test with a fixture controller), no token 401 on each endpoint, wrong capability and wrong table on each endpoint with "nothing written" and an audit event on refusal, author approving, unknown `loadId` 404, no business date 503 and the cache never holding a non-approved version. 400 not used, with the reason | spec.md §Test scenarios (security table); A-12; GAP-28 |
| 111 Wrong citation for message seam | Low | Citation is now E1-042 clarification pack §6.2 and OI-E1-042-004; `MessageResolver` from RWB-E1-042. GAP-06 kept | SPEC-020 |
| 112 Story requirement IDs not traced | Low | REQ-DRI-011, REQ-CWC-006, CTL-08, R-UNI-38 in §0, coverage rows and SU trace rows; crosswalk gap recorded | spec.md §0; SU §1; GAP-29 |
| 113 NFR applicability | Low | One line per NFR-RWB-001..010 with applicable or N/A and the reason | spec.md §NFR applicability |
| 114 Trigger exemption too wide | Low | Exemption narrowed to status, `approver_user_id`, `approved_at`, `valid_to`, `rollback_reason`, `version`, `updated_at`, `updated_by`; `created_*` and `is_active` are refused. Recorded as a deviation from S7 §13 | SPEC-001; A-33; GAP-11; TC-MG-01 |
| 115 "No CREATE" wording | Low | Reworded: no `CREATE SCHEMA`/`ROLE`, `GRANT`, `REVOKE`, `SET search_path` or `R__` | SPEC-001 |
| 116 Owner acceptance | Low | Listed for the plan gate with owners: A-01, A-08, A-09/A-34, A-16, A-17, A-27, A-31, A-33 | spec.md §Owner acceptance; compliance-validation §3; SU open item |
| 117 Message and status mismatches | Low | Recorded: MSG-P4-003 wording for an unknown load; 400 vs 422 | GAP-27, GAP-28; SU open item |
| 118 Capability check overlap; multi-module | Low | No P4 `CapabilityCheck` of this story's own: RWB-E1-042's published `CapabilityCheck` is reused (replaced by RWB-E1-037; shaped for RWB-E1-022 `AccessCheck`). Multi-module scope (P3, P4, platform) flagged for the plan gate | SPEC-027; Change Scope "Module scope" row; Seams table; SU open item |
| 119 Flag-off bean | Low | Read beans always present; `ReferenceDataReaders.enabled()` returns the flag; write side gated; controller mapped when either flag is on, an off branch returns 404 | SPEC-018; A-23; TC-FL-01 |

## 2. Gaps raised by the gate (G-R01..G-R10)

| Gate gap | Recorded as | Blocker | Resolution |
|---|---|---|---|
| G-R01 registry has no rollback | GAP-20 | No | Rollback built (SPEC-024) |
| G-R02 check plug-in, every failed row | GAP-21 | No | SPI `validate` (SPEC-025); every row in `detail` (SPEC-003) |
| G-R03 approver per table | GAP-22 | No | Per-table lists (SPEC-027) |
| G-R04 catalog file bypassed | GAP-23 | No | Catalog file + generator (SPEC-029) |
| G-R05 shared endpoint dispatch | GAP-24 | **No** (D-RUN-10, D-RUN-11) | SPEC-026, SPEC-030 |
| G-R06 RWB-E1-001 V0001 tables | GAP-25 | No for this story | Guarded DDL (SPEC-001); SU open item to RWB-E1-001 |
| G-R07 refusal logging | GAP-26 | No | SPEC-028 with RWB-E1-039 seam |
| G-R08 MSG-P4-003 wording | GAP-27 | No | Message ID governs |
| G-R09 400 vs 422 | GAP-28 | No | API4 and S7 followed (A-12) |
| G-R10 REQ-CWC-006 crosswalk | GAP-29 | No | Traced to FR-RWB-011 by content |

## 3. D-RUN-11: handler registry (orchestrator ruling)

This story publishes `ReferenceTableHandler` in `casewf.refdata.api` (signature in SPEC-025: the first
three methods verbatim from story v7 RWB-E1-001 §12, plus `supportsRollback`, `onRolledBack` and
`changeSummary` with defaults). At start-up `ReferenceTableHandlers` maps each table code to its handler
bean; two beans for one code, or one for `PARAMETER`, fail start-up. A registered code is dispatched to
its handler (generic checks, then `validate`; `apply` in the approve transaction; `onRolledBack` on
rollback); an unknown code is refused 422 MSG-P3-027. **`data_product` is not refused by design**:
RWB-E1-001 (BS6 order 9) registers it with its three catalog keys and column definition; until then it
is an unknown code (TC-HD-03 proves both states). This resolves GAP-08 and RWB-E1-001's gate finding
003. The SPI sits in P3, not P4 as story v7 RWB-E1-001 §12 says, because the P3 registry calls it
(GAP-36). Pack §3.1's "in LOV-REF-TABLE and has a handler" rule is superseded for handler codes (GAP-31).

## 4. Dictionary loads and the `is_personal` mark (orchestrator cross-story input, 2026-11-18)

Input from the orchestrator (Claude Code, not a human): under DL10 D-RCV-29 later dictionary changes are
reference loads; the RWB-TE-011 PDPA lint reads only files; a load that changes `sys_fields.is_personal`
must be recorded in audit and version log, and a removal without the PDPA approval must be refused, if
the sources support it.

| Part | Source support | Result |
|---|---|---|
| Dictionary changes go through this story's load path | DL10 D-RCV-29 | **In scope.** A handler code (SPEC-025); the dictionary handler and its code are RWB-E1-001's because `sys_objects`/`sys_fields` are its V0001 tables (GAP-37) |
| Change recorded in the version log | S7 §13, §17; D-RCV-29 | **In scope, built.** Every load is an immutable version with its rows (SPEC-001, 007) |
| Change recorded in the audit | BS-4.4; FR-RWB-012 | **In scope, built.** `changeSummary` items (field ID, old and new mark, no values) in the LOAD, APPROVE and ROLLBACK audit events (SPEC-028, SPEC-031; A-35); TC-HD-04 |
| Approval of a dictionary change | S7 TE-011 §10 (RW-COMPLY owns which fields are personal, DL26); S7-037 key pattern | **In scope, built.** Non-author approval by a role in `rwb.refload.approver.<dictionary code>`, fail closed; RWB-E1-001 asked to set it to `RW-COMPLY` (A-36) |
| Refuse removal of `is_personal` without a separate PDPA approval | None: Personal Data Protection Design v2, Data Classification and Personal Data Inventory v4 and DL26 define no such approval | **Not built: seam with open item** (owner RW-COMPLY with the data architect; implementer the dictionary handler's `validate`, which can compare with the version in force) |
| TE-011 lint sees loaded changes | S7 TE-011 §12 reads the schema seed only | Conflict recorded (GAP-38); SU open item to RWB-TE-011 |

## 5. Result

All 19 findings and 10 gate gaps are addressed. 50 requirement rows COVERED (built and tested here),
14 lines owned elsewhere, 36 assumptions, 38 gaps (26 conflicts, 12 missing), no blocker for this story.
Round 2 of the spec gate is `review/spec-gate-review-2.md`.

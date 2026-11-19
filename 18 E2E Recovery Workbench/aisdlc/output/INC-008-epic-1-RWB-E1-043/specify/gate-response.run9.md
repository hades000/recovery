# Gate response: RWB-E1-043 spec gate rounds 1 to 8 (INC-008-epic-1-RWB-E1-043)

Remediation run 1, 2026-11-18 (§1-§5; round 2 is §6; round 3 is §7; round 4 is §8; round 5 is §9; round 6 is §10; round 7 is §11; round 8 is §12). Technical Specifier response to `review/spec-gate-review.md` (round 1,
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

> **Superseded in part (finding 137).** This section is the round-1 text, kept as history. The
> `data_product` handler supplies two catalog keys and no column definition (§6.1, finding 120), and the
> reason given for the SPI in P3 ("the P3 registry calls it" with P4 depending on P3) is replaced by
> RWB-TE-001 v4 SU-08 and SPEC-022 (d) (§7.1, finding 131). Current text: `spec.md` revision 4 SPEC-025.

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

> **Superseded (finding 137).** This section is the round-1 text, kept as history. The dictionary is
> RWB-E1-064's, not RWB-E1-001's (§6.1, finding 121); the `is_personal` protection is a stated
> requirement on RWB-E1-064 (§6.4); the TE-011 open item is withdrawn; the approver is RW-COMPLY only,
> labelled inferred, with no data architect role (§7.1, finding 135). Current text: `spec.md` revision 4
> SPEC-031 and `shared-updates.md` §3.2.

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

## 6. Round 2 (remediation run 2, 2026-11-18)

Response to `review/spec-gate-review-2.md` (round 2, FAIL: 4 Medium, 7 Low, gaps G2-R01..G2-R05). The
review file is not edited. Files were first copied to `<name>.run2.*` (`spec.run2.md`,
`assumptions.run2.md`, `document-gaps.run2.md`, `shared-updates.run2.md`,
`compliance-validation.run2.md`, `gate-response.run2.md`, `agent-run-log.run2.md`,
`contracts/backend-apis.run2.json`). SPEC-nnn below refers to `spec.md` revision 3.

**Triage.** The round-2 triage, the RWB-E1-001 addendum and the GAP-38 correction were given by the
orchestrator, Claude Code, an AI agent. No human gave them. They are not human acceptance or
ratification. Open item R1 in `shared-updates.md` §3 asks the engagement lead to ratify or reject
D-RUN-10, D-RUN-11 and D-RUN-08 as applied here.

### 6.1 Findings 120-130

| Finding | Sev | Resolution | Where |
|---|---|---|---|
| 120 Handler SPI conflicts with its consumers | Medium | The SPI now carries a full contract. (a) The check order is L1-L14. The column definition (L11) is optional for a handler code, and when present it runs before `validate`. `keyColumns()` sets `row_key` (A-37). (b) The handler's own message ID, placeholders and field are returned unchanged. MSG-P3-027 is used only for the registry's own checks. (c) There is one repeat behaviour, with an optional handler `repeatMessage` (409, nothing written; A-38). `data_product` is concrete: K0-K5 IDs pass through; MSG-P1-011 on a repeat; no `refdata.columns.data_product`; loader RW-REFADM, approver RW-DATASTEW (A-40). The remaining differences are recorded: GAP-39 (G2-R01) and GAP-44 (S7-001 repeat "version in force" vs `(table, validFrom, hash)`, and 409 vs 422) | SPEC-003, 006, 025; A-37, A-38, A-40; GAP-39, GAP-44; TC-HD-01, TC-HD-03, TC-HD-05; SU §3.1 |
| 121 Dictionary route given to the wrong story | Medium | Story v7 RWB-E1-064 has now been read. It owns `sys_fields` (BS6 order 13). It registers a `ReferenceTableHandler` that adapts its `DataDictionaryLoader`, and this story never calls P1 (D-RUN-08, D-RUN-11; GAP-40 records S7-064 §12's opposite direction). SPEC-031 now covers the registry and the generic checks only. The RWB-E1-001 dictionary rows are withdrawn, and the forward note goes to RWB-E1-064 (SU §3.2). `data_product` stays with RWB-E1-001 (D-RUN-11). GAP-37 is corrected, and A-36 is re-pointed | SPEC-031; not-built and seams tables; A-36; GAP-08, GAP-37, GAP-40; SU R3, §3.2 |
| 122 Access lists rewritable by a PARAMETER load; A-31 claimed acceptance | Medium | Closed by design. `ParameterLoadBranch` reads the CSV `key` column before calling RWB-E1-042. Any `rwb.refload.*` key gets 422 MSG-P1-002 for the whole load; `load` is never called and a REFUSED audit is written. So no load, approval or rollback can change a list, and the PARAMETER approver list cannot widen itself. Until RWB-E1-037 provides a governed path, the lists change only by a reviewed catalog-file pull request plus a migration row (A-39; GAP-41 = G2-R03). The acceptance wording is removed from A-31, and the risk is recorded as open (R7, R11) | SPEC-026, 027, 029; A-31, A-39; GAP-41; SEC-15, TC-CAT-01; SU R6(d), R7 |
| 123 Two COVERED rows not built | Medium | Both rows are removed from coverage and listed under "built by another story". The HTTP read of versions has no owner (GAP-34, R18); only the Java `versions()` is built and tested here. The SIT done-when is a seam with each table's owner. PRODUCT, REGION and EXPOSURE_BAND have no named owner (GAP-43 = G2-R05; R10). SPEC-022 is rewritten as a seam. Coverage is now 48 rows, with 15 lines owned elsewhere | spec.md §Coverage, §Requirement lines built by another story; SPEC-022; GAP-43 |
| 124 IF NOT EXISTS option still offered to RWB-E1-001 | Low | The option is removed. RWB-E1-001 creates neither table and no `uk_reference_row` (D-RUN-12, an AI-orchestrator ruling, not ratified). Its dictionary describes the per-version key | SU §3.1 item 1 |
| 125 Rollback bypasses the dictionary approver | Low | Rollback is stated as a single-person action by a U holder on the loader list. It restores a version that a non-author already approved and is not a new approval (A-27). For `sys_fields`, `onRolledBack` must never write `is_personal` (stated requirement), so a rollback cannot restore an earlier mark | SPEC-024, 025, 031; A-27; SU §3.2 item 3 |
| 126 Interim grants miss named approvers | Low | Interim Reference data A is added for RW-DATASTEW (S7-001 step 9), RW-TEAMMGR (S7-019 step 4), RW-COMPLY and RW-SECADM (S7-037 line 46), besides RW-RISK and RW-COE. It lands in this story's merge, before RWB-E1-001 and RWB-E1-064. The seed list is completed (RW-COMPLY RU; R for the other seeded roles). The RWB-E1-037 row replaces the grants and no longer carries a "before SIT exit" date | SPEC-027; A-08; SEC-17; SU R7 |
| 127 `sub` is not a UUID in Entra ID | Low | `ActorIdResolver` (P4 internal seam) uses `oid` if it is a UUID, else `sub` if it is a UUID, else 401 MSG-P4-001. RWB-E1-022 replaces it. The environment risk is recorded | SPEC-015, 016; field matrix; A-07; SEC-16; CLAR-018; SU R8 |
| 128 Baseline on RWB-E1-042 revision 3 | Low | Re-baselined on revision 4. A-26 now uses `byName(String key, Class<T> type)`. The consumed interfaces in the contracts are updated. No behaviour change | spec §0, P2; A-25, A-26; `contracts/backend-apis.json` revision 3; SU R6(a) |
| 129 Refusals not attributable; backend-context conflict | Low | Recorded as GAP-42 (G2-R04): backend context v2.0 line 138 against BS-4.6 and the inventory v4. Until RWB-E1-039, only `traceId` links a refusal to its request. Open item for the DPO and the E1-039 owner | SPEC-028; A-30; GAP-42; SU R9 |
| 130 AI-orchestrator rulings need human ratification | Low | No ratification is claimed. The owner-acceptance section lists D-RUN-08, D-RUN-10, D-RUN-11, D-RUN-12 and the 2026-11-18 rulings as "not ratified". Open item R1 asks the engagement lead to ratify D-RUN-10, D-RUN-11 and D-RUN-08 as applied here | spec §Owner acceptance; SU R1 |

### 6.2 Gate gaps G2-R01..G2-R05

| Gate gap | Local row | Handling |
|---|---|---|
| G2-R01 handler messages and repeat | GAP-39 (C) | SPEC-025 pass-through and repeat message |
| G2-R02 dictionary owner and direction | GAP-40 (C); GAP-37 corrected | SPEC-031; SU §3.2 |
| G2-R03 who approves the access lists | GAP-41 (M) | SPEC-026 guard; A-39; R7 |
| G2-R04 logs carry the user ID | GAP-42 (C) | SPEC-028; R9 |
| G2-R05 SIT done-when owners | GAP-43 (M) | SPEC-022 seam; R10 |

New in this run: GAP-44 (C), the S7-001 repeat definition. GAP-38 is re-typed C → M (§6.4). Totals: 44
gaps (29 C, 15 M), CONTRADICTIONS 29. No blocker.

### 6.3 RWB-E1-001 addendum (orchestrator, 2026-11-18; RWB-E1-001 is held until review 3)

- **Contract, defined completely.** SU §3.1 states everything RWB-E1-001 needs:
  - which checks run before the handler, and in what order (L1-L11), then `validate` and `row_key`;
  - what the handler supplies: `keyColumns` = `product_code`, its K0-K5 failures, and `repeatMessage` MSG-P1-011;
  - that its MSG-P1-* codes pass through unchanged (422; repeat 409);
  - its seed rows: exactly two catalog rows (`rwb.refload.loader.data_product` = RW-REFADM, `rwb.refload.approver.data_product` = RW-DATASTEW) in its catalog file and its own migration, and **no** `refdata.columns.data_product`.
- **RWB-E1-001 finding 017.** The `is_personal` protection is stated in the RWB-E1-064 forward note (SU §3.2 item 3) as a requirement: `validate` refuses a change, and `apply`/`onRolledBack` never write `is_personal`. It is protective, so it applies unless RW-COMPLY rules otherwise. Open item R4 is owned by RW-COMPLY.
- **LOV-REF-TABLE.** No fix is needed from RWB-E1-001. The rows to add and the rows to remove are both "none". RWB-E1-043 refuses the rule codes and HOLIDAY itself, and `data_product` and `sys_fields` need no LOV row. Revision 2's request is withdrawn (GAP-04; SU §3.1 item 6).

### 6.4 GAP-38 correction (orchestrator, 2026-11-18)

- **Runtime protection.** Protection of `is_personal` against a dictionary load belongs to RWB-E1-064. It is a seam, with open item R4 owned by RW-COMPLY.
- **TE-011 lint.** The RWB-TE-011 lint covers only committed SQL, fixtures and logs; it is not a runtime check. The revision-2 request to RWB-TE-011 is withdrawn.
- **This story.** RWB-E1-043 publishes the registry and runs its generic checks, and does nothing more for the dictionary (SPEC-031). It is tested with a synthetic handler (TC-HD-04).
- **GAP-38 itself.** It is rewritten as a missing runtime check, typed M.

### 6.5 Result of run 2

- All 11 round-2 findings and 5 gate gaps are addressed.
- 48 requirement rows are COVERED (built and tested here), and 15 lines are owned elsewhere.
- 40 assumptions (14 need owner acceptance, none accepted).
- 44 gaps; no blocker for this story.
- Round 3 of the spec gate is `review/spec-gate-review-3.md`.

## 7. Round 3 (remediation run 3, 2026-11-18)

Response to `review/spec-gate-review-3.md` (REVIEW-RWB-E1-043-SPEC-003, FAIL: 1 High, 1 Medium, 5 Low,
gaps G3-R01..G3-R05). The review file is not edited. Files were first copied to `<name>.run3.*`
(`spec.run3.md`, `assumptions.run3.md`, `document-gaps.run3.md`, `shared-updates.run3.md`,
`compliance-validation.run3.md`, `gate-response.run3.md`, `agent-run-log.run3.md`,
`contracts/backend-apis.run3.json`, `contracts/frontend-integrations.run3.json`). SPEC-nnn below refers
to `spec.md` revision 4.

**Triage.** The round-3 triage (placement per RWB-TE-001 v4, the effective-date defaults, the gap
treatment of 134 and 135, Lows fixed under D-RUN-09) was given by the orchestrator, Claude Code, an AI
agent, on 2026-11-18. No human gave it; it is not human acceptance or ratification (open item R1).

### 7.1 Findings 131-137

| Finding | Sev | Resolution | Where |
|---|---|---|---|
| 131 Module placement and cycle | High | Rebased on RWB-TE-001 v4 (SPEC-022 (d), SPEC-023, SU-08) and RWB-E1-042 revision 5. All story code, including the controller, dispatcher, PARAMETER branch, authority, audit and actor resolver, is in P3 `casewf.refdata.internal`; `casewf.refdata.api` is published as `refdata.api` and added to `recovery-modules.yaml`. `ReferenceTableCodeSource` is dropped. The LOV-REF-TABLE read goes through a new P4 published `access.api.ListOfValuesReader`, because S7 §11 and §17 require "the P4 published interface"; this differs from the review's suggestion (LOV read in P3) and is explained in SPEC-002 (A-41). Names from E42S revision 5: `casewf.config.api` (`ParameterService`, `ParameterKeys.byName`, `ParameterLoadHandler`, `ParameterLoadResult`, `BusinessDateProvider`) and `access.api` (`CapabilityCheck`, `MessageResolver`, `ApiProblemException`, `ApiError`); R6 asks RWB-E1-042 to keep them stable. `VersionDecisionRecorder` is not published, so AC-VERS goes through this story's package-private `ReferenceDecisionRecorder` with the same pattern and 503 MSG-P7-003 (A-43; GAP-50). Flag bound by `@ConditionalOnProperty`, a module record and `@ConditionalOnExpression`; no `RecoveryFlags` change (A-44). Grants rows in `access/interim-capability-grants.csv`. SPEC-019 holds the dependency table: P3 → P4 only, no P4 or P2 type refers to `casewf`, so no P3 ↔ P4 cycle. The latent P1 ↔ P3 risk (P1 handlers plus a planned P3 → P1 business-date reader) is GAP-51 with open item R24, Blocker = No here. S7 §12's "P4 endpoint" wording is GAP-53 | Change Scope; SPEC-002, 008, 015-020, 025-030; A-10, A-24, A-25, A-41, A-43, A-44; SU R6, R15, R22, R24, R25, §3.1 items 2 and 4; contracts `module`, `consumedInterfaces`; TC-BD-01 |
| 132 Apply timing, out-of-order approval, rollback | Medium | Rules taken from the sources: S7 BR3 and BR8, S7-019 BR3, AC2, AC9 and flow step 5, data dictionary v8 DF-REF-079, DF-REF-163/164, DF-WRK-038, DF-WRK-051/052; Decision Log v10 is silent. New SPEC-032: approval writes a new version effective from `validFrom` and never overwrites the version in force; reads select by business date; versions are independent, so out-of-order approval is allowed; rollback withdraws only the latest approved version. The handler contract carries the same rule (`apply` stores a dated version; a current-state table is updated by the owner's own job on the valid-from date). The orchestrator's default "refuse once effective" is **not** applied, because S7-019 AC2 rolls back the version in force and a story rule outranks a default meant for silent sources; recorded as GAP-52 with open item R28. Tests TC-TM-01..04 | SPEC-008, 010, 024, 025 *Effective date*, 032; A-18, A-27, A-42; GAP-45, GAP-52; SU R5, §3.1 item 8, §3.2 item 6 |
| 133 Repeat before the date check | Low | The repeat check (L9) now runs before the valid-from check (L10), so RWB-E1-001 AC10 answers MSG-P1-011 for any business date. A handler may also return MSG-P1-011 from `validate` for the wider X7 case; that is a pass-through 422. Unparseable values are hashed as text (A-13). Test TC-RP-01 | SPEC-006, 025; A-13; GAP-44; SU §3.1 items 3, 7 |
| 134 RW-DATASTEW holds U, approval needs A | Low | Recorded as GAP-46 with two citations: S7-001 §10 and S7-064 §10 (U), URP4 line 102 and PS6 (RU), against S7 §10 and API4 (A). The higher-precedence source for the operation, S7 §10, requires A; RW-DATASTEW's interim A stays an assumption (A-08, A-40), not a source grant. Open item R26 | SPEC-027; A-08, A-40; SU R26, §3.1 item 5, §3.2 item 2 |
| 135 No role code for a data architect | Low | Recorded as GAP-47: S7-069 line 203 and DL10 name a data architect, URP4 has no role code. The `sys_fields` approver is RW-COMPLY only, labelled inferred from TE011 §10; no code is invented. Open item R27 | SPEC-031; A-36; SU R4, R27, §3.2 item 2 |
| 136 Load with no `table`; 404 and 500 not in API4 | Low | (a) `table` presence is L3, before the loader list (L4); `mayLoad` grants the table right when `table` is absent, so the answer is 422 MSG-GEN-001 `{field}` = `table`; test TC-FD-01. (b) API4 lists no 404 for the load and no 500: recorded as GAP-48, request to the API owner (R21) | SPEC-015, 025; GAP-48; contracts |
| 137 Stale text | Low | §3 and §4 of this file are marked superseded; `contracts/frontend-integrations.json` is now revision 3; the S7-019 line 38 QUEUE_MEMBER LOV wording is recorded as GAP-49 with a note to RWB-E1-019 (no LOV row needed) | §3, §4; contracts; SPEC-025 QUEUE paragraph; SU R5 |

### 7.2 Gate gaps G3-R01..G3-R05

| Gate gap | Local row | Handling |
|---|---|---|
| G3-R01 apply timing | GAP-45 (M) | SPEC-025 *Effective date*, SPEC-032 |
| G3-R02 U vs A | GAP-46 (C) | SPEC-027; R26 |
| G3-R03 no dictionary approver role | GAP-47 (M) | SPEC-031; A-36; R27 |
| G3-R04 API 404 and 500 | GAP-48 (C) | R21 |
| G3-R05 QUEUE_MEMBER LOV row | GAP-49 (C) | SPEC-025; R5 |

New in this run: GAP-50 (M, recorder not published), GAP-51 (C, latent P1 ↔ P3 cycle), GAP-52 (C,
rollback default vs S7-019 AC2), GAP-53 (C, "P4 endpoint" wording). GAP-36 corrected. Totals: 53 gaps
(35 C, 18 M), no blocker for this story.

### 7.3 Result of run 3

- All 7 round-3 findings and 5 gate gaps are addressed.
- 49 requirement rows are COVERED (built and tested here), and 16 lines are owned elsewhere.
- 44 assumption rows (A-32 withdrawn; 16 need owner acceptance, none accepted).
- 53 gaps; no blocker for this story.
- Round 4 of the spec gate is `review/spec-gate-review-4.md`.

## 8. Round 4 (remediation run 4, 2026-11-18)

Response to `review/spec-gate-review-4.md` (REVIEW-RWB-E1-043-SPEC-004, FAIL: 0 Critical, 0 High,
1 Medium, 8 Low, gaps G4-R01..G4-R03). The review file is not edited. Files were first copied to
`<name>.run4.*` (`spec.run4.md`, `assumptions.run4.md`, `document-gaps.run4.md`, `shared-updates.run4.md`,
`compliance-validation.run4.md`, `gate-response.run4.md`, `agent-run-log.run4.md`,
`contracts/backend-apis.run4.json`, `contracts/frontend-integrations.run4.json`). SPEC-nnn below refers
to `spec.md` revision 5.

**Triage.** The round-4 triage was given by the orchestrator (Claude Code, an AI agent), logged at
2026-11-18 04:55 under D-RUN-09 (Lows fixed, not accepted), together with run decision D-RUN-18 (the
reference-load handler SPI is published by P4 `access.api`; decisions table line 41 of
`AI-SDLC-BUILD-LOG.md`). No human gave either; neither is human acceptance or ratification. D-RUN-18
waits for ratification by the recovery tech lead (shared update R24); the triage is listed in R1.

### 8.1 Findings 138-146

| Finding | Severity | Change | Where |
|---|---|---|---|
| 138 Current-state tables approved early | Medium | Each handler declares `dating()` (`DATED` or `CURRENT_STATE`; default `CURRENT_STATE`, the protective reading). For a `CURRENT_STATE` handler code, approval while `validFrom` is after the business date is refused with 409 MSG-P3-027 `{check}` = "it can be approved only on its valid from date <validFrom>" (MSG4 line 151; no new message ID); nothing is written and `apply` is not called. Approval with `validFrom` on or before the business date applies at once; with A-17 that means on the date. Out-of-order approval cannot occur; rollback re-applies the restored version at once. No owner job and no schema change. `data_product` and `sys_fields` are `CURRENT_STATE` (PS6 `uk_data_product`, `uk_sys_fields`). New test TC-TM-05 (future-dated approval refused, same-day approval applied, rollback re-apply). G4-R01 and G4-R02 recorded as GAP-54 and GAP-55 (Blocker = No; owner: the data owner, R31) | SPEC-008, 025 (*Effective date*, `data_product`, QUEUE), 032 rule 6; status and exception matrices; A-42; §3.1 items 2 and 8; §3.2 item 6; R5; both contracts (backend `effectiveDate`, approve 409; frontend revision only) |
| 139 T-TE001-14 not listed | Low | T-TE001-14 is listed as a changed test in the Change Scope; SPEC-019 states its expected sets after RWB-E1-042 TC-45 and this story (`access.api` 10 types, casewf named interfaces `api`, `config.api`, `refdata.api`, `rules`, `timers`, `workflow`; `casewf.refdata.api` 6 types); TC-BD-01 asserts them; coordination with RWB-E1-042 revision 7 or later is R29 | Change Scope; SPEC-019; TC-BD-01; R25, R29 |
| 140 Repeat before validity for every code | Low | The early repeat check (L9) runs only for a handler code whose `repeatMessage(file)` is present; every other code keeps the S7 §13 order (L11: validity checks, then the hash and the idempotent return). TC-RP-01 covers both paths. G4-R03 recorded as GAP-56 (Blocker = No) | SPEC-006, 025 L9/L11; A-38; TC-RP-01; GAP-44, GAP-56; backend contract load 409 and `loadCheckOrder` |
| 141 SPI placement and P1 → P3 | Low | Settled by D-RUN-18: `ReferenceTableHandler` (nested `Dating`), `ReferenceLoadFile`, `HandlerMessage`, `ValidationReport` and `RowCheckFailure` move to P4 `access.api`; the registry stays in P3 `casewf.refdata` and collects handler beans by the P4 type. P1 never depends on P3; P3 → P1 reads (S7-028 flow step 3, S7 §12 line 270, the E42S §4.3 business date) stay allowed. SPEC-019 edge table shows no cycle; new `RecoveryBoundaryTest` rule (3) forbids `dataengine` → `casewf`. GAP-51 and R24 updated as "settled by D-RUN-18, pending tech-lead ratification"; GAP-36 and GAP-53 updated with them | Change Scope; SPEC-019, 025, 031; GAP-36, GAP-51, GAP-53; R16, R22, R24, R25; §3.1 item 2; §3.2 item 1; backend contract `publishedJavaInterfaces.p4HandlerSpi`, `dependencyDirection` |
| 142 403 text "do this" | Low | `ReferenceLoadAuthority` uses `CapabilityCheck.require(auth, "Reference data", right, action)` and, for a table-right refusal, throws the same `ApiProblemException(ApiError.NOT_PERMITTED, Map.of("action", action), null)` form after the REFUSED audit. Actions "load reference data", "approve reference data", "roll back reference data" (new A-45, inferred, not owner-accepted). SEC tests assert the `{action}` text, never "do this" | SPEC-020, 027; A-45; tests (SEC note); backend contract 403 `action` |
| 143 Context fails with the flag off | Low | Only the controller and dispatcher stay conditional; `ReferenceTableHandlers` (empty map when no handler bean) and `LoggingReferenceDecisionRecorder` are registered whatever the flag; `RefdataSettings` gates the writes. TC-FL-01 starts the context in all four flag combinations, including only `rwb.p3.configservice` on | SPEC-018; A-44; TC-FL-01; backend contract `featureFlags` |
| 144 Stale RWB-E1-042 baseline | Low | Re-baselined on RWB-E1-042 spec revision 7 (remediation run 5; file written 2026-11-18 01:35:53), naming `MessageResolver.english` / `thai(String messageId, Map<String, String> placeholders)` and the six-argument `ApiProblemException` form with `detail`, which carries this story's capped multi-failure text | §0 E42S row; SPEC-020; A-25 (and A-08, A-26, A-43, A-44 cites); R6; compliance-validation §3; backend contract `consumedInterfaces` |
| 145 RWB-E1-042 row 25 not answered | Low | New TC-PB-02 (`@Tag("recovery-it")`): the real `ParameterLoadHandler` with `rwb.p3.configservice` on, through the three endpoints, for E42S TC-05, -06, -07, -10 part (a), -11, -16 to -20 and -23 with E42S's expected results; TC-10 part (b) stays in E42S. Row 25 answered in R30 | SPEC-026; tests; Unit Test Applicability; R30; backend contract tests |
| 146 Wording | Low | (a) A-37 now reads "L12 before L13"; (b) SPEC-027 and GAP-46 no longer claim a higher-precedence source: RUN-BRIEF ranks the v7 story files at one level, so the operation owner's story is followed, settled by assumption A-08; (c) `compliance-validation.md` is revision 5 | A-37; SPEC-027; GAP-46; compliance-validation |

### 8.2 Gate gaps G4-R01..G4-R03

| Gate gap | Local row | Handling |
|---|---|---|
| G4-R01 `data_product` is current-state | GAP-54 (C), Blocker = No, owner the data owner | SPEC-025, 032 rule 6; A-42; TC-TM-05; R31 |
| G4-R02 `sys_fields` is current-state | GAP-55 (C), Blocker = No, owner the data owner | SPEC-025, 031, 032 rule 6; A-42; R31 |
| G4-R03 early repeat departs from S7 §13 order | GAP-56 (C), Blocker = No | SPEC-006, 025 L9; A-38; TC-RP-01 |

Updated in this run: GAP-36, GAP-51, GAP-53 (D-RUN-18), GAP-44 (repeat limited), GAP-46 (precedence
wording), GAP-50 (E42S revision 7 cite). Totals: 56 gaps (38 C, 18 M), no blocker for this story.

### 8.3 Result of run 4

- All 9 round-4 findings and 3 gate gaps are addressed.
- 49 requirement rows are COVERED (built and tested here), and 16 lines are owned elsewhere.
- 45 assumption rows (A-32 withdrawn; A-45 new; none accepted by an owner).
- 56 gaps; no blocker for this story. CONTRADICTIONS 38.
- Round 5 of the spec gate is `review/spec-gate-review-5.md`.

## 9. Round 5 (remediation run 5, 2026-11-18)

Response to `review/spec-gate-review-5.md` (REVIEW-RWB-E1-043-SPEC-005, FAIL: 0 Critical, 0 High,
0 Medium, 4 Low, gap G5-R01). The review file is not edited. Files were first copied to `<name>.run5.*`
(`spec.run5.md`, `assumptions.run5.md`, `document-gaps.run5.md`, `shared-updates.run5.md`,
`compliance-validation.run5.md`, `gate-response.run5.md`, `agent-run-log.run5.md`,
`contracts/backend-apis.run5.json`, `contracts/frontend-integrations.run5.json`). SPEC-nnn below refers
to `spec.md` revision 6.

**Triage.** The orchestrator (Claude Code, an AI agent), in its round-4 triage of 2026-11-18 04:55,
allowed one more round if review 5 failed on Low findings only. All four are fixed under D-RUN-09 (Lows
fixed, not accepted). No human gave this triage; it is not human acceptance or ratification.

### 9.1 Findings 147-150

| Finding | Severity | Change | Where |
|---|---|---|---|
| 147 TC-TM-05 steps (c) and (e) impossible | Low | TC-TM-05 rewritten: v3 uses `validFrom` 2026-12-04 on business date 2026-12-04; a corrected v5 for the same date is refused at load (409 MSG-P3-027 at L11, one approved version per date); v4 (2026-12-05) is refused after its date (A-17); v3, the latest approved version, is rolled back. (Corrected in run 6, finding 151: the same-date step tests a load refusal, not an approval refusal, and now runs right after the same-day approval as step (d); the A-17 and rollback steps are (e) and (f).) SPEC-025 *Effective date*, SPEC-032 rule 6 and A-42 state that a table has at most one APPROVED version per `validFrom`, so a same-day correction of a current-state table needs a rollback first (which needs an earlier approved version, else 409 MSG-P3-015; added in run 7, finding 154) or waits for a later date | SPEC-025, 032; A-42; TC-TM-05; backend contract `effectiveDate` |
| 148 RWB-E1-042 moved to revision 9 | Low | Re-baselined on RWB-E1-042 spec revision 9 (remediation run 7; file 2026-11-18 05:16:37); revision 7 named as kept in `spec.run6.md`; names used are unchanged. The T-TE001-14 `access.api` set is defined as RWB-E1-042's merged set (at revision 9 it includes `CatalogParameterReader` with nested `Value`, D-RUN-19) plus this story's six types | §0; SPEC-019; TC-BD-01; A-25; R6, R29; compliance-validation §3; backend contract `source`, `consumedInterfaces.basis`, `tTe001_14` |
| 149 `PARAMETER` route not recorded | Low | The spec keeps `PARAMETER` a dispatcher branch (`ParameterLoadBranch`, implements no `access.api` type; a `PARAMETER` handler bean fails start-up) and now says so in SPEC-025 and SPEC-026, with the source reasons (no second load record beside `parameter_value.load_id`, E42S R7-1; flag-off result kept). R24 corrected. G5-R01 recorded as GAP-57 (Blocker = No); R32 asks RWB-E1-042 to align §4.3 line 144, A-51 and R7-1 and asks the orchestrator to note D-RUN-18's wording | SPEC-025, 026; GAP-57; R24, R32; backend contract `implementedBy` |
| 150 Stale cross-references | Low | (a) SPEC-024 now points to SPEC-006 rule (2) and qualifies the reload for handler repeat messages (409) and past dates (422); A-27 qualified the same way. (b) Backend contract `source` cites RWB-E1-042 revision 9 | SPEC-024; A-27; backend contract `source` |

### 9.2 Gate gap G5-R01

| Gate gap | Local row | Handling |
|---|---|---|
| G5-R01 `PARAMETER` route | GAP-57 (C), Blocker = No | SPEC-025, 026; R32 |

Totals: 57 gaps (39 C, 18 M), no blocker for this story.

### 9.3 Result of run 5

- All 4 round-5 findings and 1 gate gap are addressed.
- 49 requirement rows are COVERED (built and tested here), and 16 lines are owned elsewhere.
- 45 assumption rows (A-32 withdrawn; none accepted by an owner).
- 57 gaps; no blocker for this story. CONTRADICTIONS 39.
- Round 6 of the spec gate is `review/spec-gate-review-6.md`.

## 10. Round 6 (remediation run 6, 2026-11-18)

Response to `review/spec-gate-review-6.md` (REVIEW-RWB-E1-043-SPEC-006, FAIL: 0 Critical, 0 High,
0 Medium, 2 Low; no new gate gap). The review file is not edited. Files were first copied to
`<name>.run6.*` (`spec.run6.md`, `assumptions.run6.md`, `document-gaps.run6.md`, `shared-updates.run6.md`,
`compliance-validation.run6.md`, `gate-response.run6.md`, `agent-run-log.run6.md`,
`contracts/backend-apis.run6.json`, `contracts/frontend-integrations.run6.json`). SPEC-nnn below refers
to `spec.md` revision 7.

**Triage.** Given by the orchestrator (Claude Code, an AI agent), logged at 2026-11-18 05:32 under
D-RUN-09 (Lows fixed, not accepted), with an instruction to re-baseline on the current RWB-E1-042 spec and
check D-RUN-19. No human gave it; it is not human acceptance or ratification.

### 10.1 Findings 151-152 and the re-baseline

| Item | Severity | Change | Where |
|---|---|---|---|
| 151 TC-TM-05 step order; §9.1 wording | Low | The same-date step now runs right after the same-day approval, as step (d), while v3 is APPROVED on 2026-12-04: a corrected v5 for 2026-12-04 is refused at load (409 MSG-P3-027 at L11). The A-17 step is (e) and the rollback of v3 is (f). §9.1 row 147 now says the step tests a load refusal | TC-TM-05; §9.1 |
| 152 R24 misquotes D-RUN-18 | Low | R24 quotes the ruling exactly ("P1 (RWB-E1-001) and P3 (RWB-E1-042) handlers implement it"), says it names no other handler implementer, and states separately which handlers this spec lists (RWB-E1-001, RWB-E1-064, RWB-E1-019) and that `PARAMETER` is a dispatcher branch | R24; GAP-57; R32 |
| Re-baseline (orchestrator) | — | Re-baselined on RWB-E1-042 spec revision 10 (remediation run 8; `spec.md` written 2026-11-18 05:28:14, `assumptions.md` 05:27:34). The names this story uses are unchanged. Revision 10 states the same `PARAMETER` route as this spec (§4.3 line 145, A-51, R7-1 line 983), so R32 part (a) is done and GAP-57 now concerns only D-RUN-18's wording | §0; A-25; GAP-50, GAP-51, GAP-57; R6, R29, R32; compliance-validation §3; backend contract `source`, `consumedInterfaces.basis`, `p4HandlerSpi` |
| D-RUN-19 check (orchestrator) | — | D-RUN-19 (decisions table line 42) publishes `access.api.CatalogParameterReader`, implemented in P3 `casewf.config`, for parameter readers outside P3. It was checked against the registry, the SPI and GAP-57: this story's code is all in P3 and reads its keys through `casewf.config.api` (allowed for P3 callers); the implementation is a P3 → P4 edge; the SPI has no parameter type, so a P1 handler that needs a parameter uses `CatalogParameterReader`; the T-TE001-14 set already counts the reader. No mismatch was found, and SPEC-019 now says so | SPEC-019 *Parameter reads under D-RUN-19* |

Totals unchanged: 57 gaps (39 C, 18 M), no blocker; 45 assumptions; CONTRADICTIONS 39.

### 10.2 Result of run 6

- Both round-6 findings are addressed; the re-baseline and the D-RUN-19 check are done.
- Round 7 of the spec gate is `review/spec-gate-review-7.md`.

## 11. Round 7 (remediation run 7, 2026-11-18)

Response to `review/spec-gate-review-7.md` (REVIEW-RWB-E1-043-SPEC-007, FAIL: 0 Critical, 0 High,
0 Medium, 2 Low; gate gap G7-R01). The review file is not edited. Files were first copied to
`<name>.run7.*` (`spec.run7.md`, `assumptions.run7.md`, `document-gaps.run7.md`, `shared-updates.run7.md`,
`compliance-validation.run7.md`, `gate-response.run7.md`, `agent-run-log.run7.md`,
`contracts/backend-apis.run7.json`, `contracts/frontend-integrations.run7.json`). SPEC-nnn below refers
to `spec.md` revision 8.

**Triage.** The orchestrator (Claude Code, an AI agent) allowed one more round on Lows in its triage
message of 2026-11-18 05:32 (D-RUN-09; run-8 correction for finding 158: the 05:32 build-log row does not
state this allowance; the row of 2026-11-18 05:52:36, line 304, states that each triage message allows one
further Low-only round), and later sent a note to apply D-RUN-20 (decisions table line 43,
05:34) to GAP-57 and R24 and to re-baseline on the RWB-E1-042 spec read. No human gave either; neither is
human acceptance or ratification.

### 11.1 Findings 153-154, G7-R01, D-RUN-20 and the re-baseline

| Item | Severity | Change | Where |
|---|---|---|---|
| 153 "all code in P3" premise | Low | SPEC-019 now says the story's code is in P3 `casewf.refdata` except the P4 additions of SPEC-002 (`ListOfValuesReader`, `LovValueReader`) and SPEC-025 (SPI types). The D-RUN-19 check point (1) now covers both: P3 code reads its keys through `casewf.config.api`; the P4 additions read no catalog parameter, so D-RUN-19 asks nothing of them. §10.1's D-RUN-19 row ("this story's code is all in P3") is corrected by this row | SPEC-019; §10.1 |
| 154 same-day correction when no earlier approved version exists | Low | SPEC-025 *Effective date*, SPEC-032 rule 6, A-42, the backend contract `handlerContract.effectiveDate` and §9.1 row 147 now add that the rollback needs an earlier approved version (else 409 MSG-P3-015, SPEC-024 rule 6), so without one the correction waits for a later `validFrom`. TC-TM-05 gains (g) rollback then reload and same-day approval of a corrected file, and (h) the MSG-P3-015 case on a second current-state test code | SPEC-025; SPEC-032; A-42; TC-TM-05; §9.1 |
| G7-R01 RWB-E1-019 P3 handlers under D-RUN-20 | Gap | Recorded as GAP-58 (C, not blocking): D-RUN-20 names the P4 SPI for handlers outside the registry's module and gives a P3 route only for `PARAMETER`. Interim A-46 keeps RWB-E1-019's P3 handlers on the P4 SPI (no new module edge); R33 asks the orchestrator to confirm before the plan gate, at the latest before the RWB-E1-019 spec | GAP-58; A-46; R33; SPEC-019 later-edge table; SPEC-025 QUEUE paragraph; contract `p4HandlerSpi.implementedBy` |
| D-RUN-20 (orchestrator note) | — | GAP-57 and R24 cite D-RUN-20 and are marked settled, pending tech-lead ratification; R32 is answered by D-RUN-20; the SPEC-025 `PARAMETER` paragraph, §0 BLOG row, owner-acceptance list, compliance-validation §3 and the backend contract `source` cite it | GAP-57; R24; R32; SPEC-025; §0; compliance-validation |
| Re-baseline (orchestrator note) | — | The RWB-E1-042 spec read for this story is revision 10 (`spec.md` written 2026-11-18 05:28:14 +07:00). Revision 11 (remediation run 9) was written at 05:41:44, after the note; it was checked in this run: the names this story uses are unchanged, the `PARAMETER` route row is now line 146 and R7-1 line 1005, and CLAR-027 is settled by D-RUN-20. Revision 10 is kept there as `spec.run9.md`, and this spec's line cites are to revision 10 | §0 E42S; A-25 |

Totals: 58 gaps (40 C, 18 M), no blocker; 46 assumptions; CONTRADICTIONS 40.

### 11.2 Result of run 7

- Both round-7 findings and G7-R01 are addressed; D-RUN-20 is applied; the re-baseline is stated.
- Round 8 of the spec gate is `review/spec-gate-review-8.md`. Per the orchestrator's triage, no further
  remediation round follows it in this run.

## 12. Round 8 (remediation run 8, 2026-11-18)

Response to `review/spec-gate-review-8.md` (REVIEW-RWB-E1-043-SPEC-008, FAIL: 0 Critical, 0 High,
0 Medium, 4 Low; gate gap G8-R01). The review file is not edited. Files were first copied to
`<name>.run8.*` (`spec.run8.md`, `assumptions.run8.md`, `document-gaps.run8.md`, `shared-updates.run8.md`,
`compliance-validation.run8.md`, `gate-response.run8.md`, `agent-run-log.run8.md`,
`contracts/backend-apis.run8.json`, `contracts/frontend-integrations.run8.json`). SPEC-nnn below refers
to `spec.md` revision 9.

**Triage.** Given by the orchestrator (Claude Code, an AI agent) under D-RUN-09. The triage message gave
05:48; the build-log row is logged at 2026-11-18 05:52:36 (`AI-SDLC-BUILD-LOG.md` line 304) and is the
row cited here. It answers R33 and states that each triage message allows one further Low-only round.
No human gave it; it is not human acceptance or ratification.

### 12.1 Findings 155-158 and G8-R01

| Item | Severity | Change | Where |
|---|---|---|---|
| 155 D-RUN-21 not applied to plan routing | Low | The Module scope row, A-24, R22, CHANGE_CLASSIFICATION_SUMMARY and compliance-validation now cite D-RUN-21 (decisions table line 44, 05:36; ratification open, OPEN-050): "touches one module" in AGENTS §7 and §9 means the ACE module (recovery); this P3 + P4 plan changes neither the common nor the collection module, so the rule sends nothing to the analyst. R22 is now a plan-gate check of that reading; no tech-lead approval is claimed. D-RUN-21 is added to the §0 BLOG row, R1 and the owner-acceptance list. The "all story code in P3" wording in the Module scope row and A-24 now names the P4 additions (as finding 153 did for SPEC-019) | Module scope row; summary line; A-24; R1; R22; §0 BLOG; compliance-validation |
| 156 GAP-58 over-reads D-RUN-18 | Low | GAP-58 quotes D-RUN-18 exactly ("P1 (RWB-E1-001) and P3 (RWB-E1-042) handlers implement it") and says neither D-RUN-18 nor D-RUN-20 names RWB-E1-019. Its support is SPEC-019, SPEC-025, TE001 SPEC-022 (d) and Story v7 RWB-E1-019 lines 18 and 261, and now the orchestrator's R33 answer in the 05:52:36 row: a P3 handler may implement the P4 SPI (P3 → P4 is an existing edge), and D-RUN-20 makes only `PARAMETER` a dispatcher branch. GAP-58 and A-46 are settled and R33 is answered, citing that row; the SPEC-019 later-edge row, the SPEC-025 QUEUE paragraph, R24 and the contract `p4HandlerSpi.implementedBy` say the same | GAP-58; A-46; R24; R33; SPEC-019; SPEC-025; backend contract |
| 157 re-baseline only for `spec.md` | Low | Every RWB-E1-042 cite now uses one revision: revision 12 (remediation run 10), the current revision when read in this run: `spec.md` 2026-11-18 05:50:36 +07:00; `assumptions.md` and `shared-updates.md` 05:50:52. Line cites were re-checked: §4.3 `PARAMETER` route row line 147, business-date seam line 153, T-2 line 982, R7-1 line 1006, R7-3 line 1008, CLAR-025 line 1198, CLAR-027 line 1200; its `shared-updates.md` rows at lines 25, 26, 32, 34, 38, 39 and 84; A-51 present. R6 now says RWB-E1-043 revision 9 is baselined on its revision 12. Names used here are unchanged through revision 12 | §0 E42S; A-25; R6; R29; R32; GAP-51; GAP-57; SPEC-019; SPEC-025; compliance-validation; backend contract |
| 158 allowance cite | Low | The run-8 allowance is cited to the 05:52:36 triage row (line 304), which states it. §11's sentence on the 05:32 triage now carries a correction note: the allowance came in the 05:32 triage message, and the 05:32 build-log row does not state it. The run-7 entries in `agent-run-log.md` are append-only; the run-8 section records the same correction | Front matter; §11; agent-run-log run 8 |
| G8-R01 "module" undefined | Gap | Recorded as GAP-59 (M, Blocker = No), settled for this build by D-RUN-21, pending OPEN-050, and kept as a cross-reference to RWB-E1-042 E1042-SP-DG-16 and RWB-TE-001 PG-04/GC-1 (not a new `DOCUMENT-GAPS.md` entry) | GAP-59; A-24; R22; INDEX note |

Totals: 59 gaps (40 C, 19 M), no blocker; 46 assumptions (A-32 withdrawn); CONTRADICTIONS 40.

### 12.2 Result of run 8

- All four round-8 findings and G8-R01 are addressed; R33 is answered by the orchestrator's triage.
- Round 9 of the spec gate is `review/spec-gate-review-9.md`.

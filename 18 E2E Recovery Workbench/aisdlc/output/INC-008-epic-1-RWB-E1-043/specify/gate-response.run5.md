# Gate response: RWB-E1-043 spec gate rounds 1 to 4 (INC-008-epic-1-RWB-E1-043)

Remediation run 1, 2026-11-18 (§1-§5; round 2 is §6; round 3 is §7; round 4 is §8). Technical Specifier response to `review/spec-gate-review.md` (round 1,
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

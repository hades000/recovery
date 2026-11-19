# Shared updates requested: RWB-E1-043 specify (INC-008-epic-1-RWB-E1-043)

Revision 9, 2026-11-18 (remediation run 8; revisions 1 to 8 kept as `shared-updates.run1.md` to
`shared-updates.run8.md`). The Technical Specifier does not edit shared files (RUN-BRIEF). The
orchestrator applies these rows in order. Every ruling cited here (D-RUN-07..12, D-RUN-18..21, the 2026-11-18 triage of rounds 2 to 6)
was made by the orchestrator, Claude Code, an AI agent; none has been ratified by a human (§3, row R1).

## 1. `aisdlc/requirement/Traceability_Matrix.md`

Replace the INC-008 row in the increment trace:

| 008 | `RWB-E1-043` | `BR-RWB-011` | `FR-RWB-011` (REQ-DRI-011, REQ-CWC-006; R-UNI-38, CTL-08, REQ-CWC-016) | `output/INC-008-epic-1-RWB-E1-043/specify/spec.md` (revision 9, 18 Nov 2026) | Specified — remediation run 8; spec gate see `review/spec-gate-review-9.md`; plan not started |

SPEC trace (CTX `CTX-BACKEND-RWB-V2`, `CTX-PROJECT-RWB-V2` CTX-FEAT-012; US `RWB-E1-043`; TASK and later
columns empty). REQ-CWC-006 has no canonical FR in REQ-RWB-002 §12; it is traced to FR-RWB-011 by
content (GAP-29).

| SPEC ID | FR/NFR | Story refs |
|---|---|---|
| SPEC-RWB-E1-043-001 | FR-RWB-011, NFR-RWB-010 | §13 Database, BR2, §17 |
| SPEC-RWB-E1-043-002 | FR-RWB-011 | BR1, §11 DF-REF-028/029 |
| SPEC-RWB-E1-043-003 | FR-RWB-011 | BR5, X2, AC4, §13 step 2 |
| SPEC-RWB-E1-043-004 | FR-RWB-011 | X7, AC10 |
| SPEC-RWB-E1-043-005 | FR-RWB-011 | BR6 (R-UNI-38), X3, AC6 |
| SPEC-RWB-E1-043-006 | FR-RWB-011 | X4, AC7, §12 idempotency |
| SPEC-RWB-E1-043-007 | FR-RWB-011 | BR2, AC1 |
| SPEC-RWB-E1-043-008 | FR-RWB-011, NFR-RWB-005 | BR4 (CTL-08), X1, AC2, AC5, §12 approve |
| SPEC-RWB-E1-043-009 | FR-RWB-011 | X5, AC8 |
| SPEC-RWB-E1-043-010 | FR-RWB-011 | BR8, AC1 |
| SPEC-RWB-E1-043-011 | FR-RWB-011 | BR3 (R-UNI-38), AC1, AC5, §9 |
| SPEC-RWB-E1-043-012 | FR-RWB-011, NFR-RWB-008 | BR9, X6, AC9 |
| SPEC-RWB-E1-043-013 | FR-RWB-011 | §13 cache, §17 |
| SPEC-RWB-E1-043-014 | FR-RWB-011, NFR-RWB-006, NFR-RWB-008 | BR7 (REQ-CWC-016), AC3 |
| SPEC-RWB-E1-043-015 | FR-RWB-011, NFR-RWB-005 | §12 load, TC-E1-043-11 |
| SPEC-RWB-E1-043-016 | FR-RWB-011, NFR-RWB-005 | §10, §12 approve |
| SPEC-RWB-E1-043-017 | FR-RWB-011 | §3 business date |
| SPEC-RWB-E1-043-018 | NFR-RWB-009 | §13 feature flag |
| SPEC-RWB-E1-043-019 | FR-RWB-011 | §13 done-when, §17 |
| SPEC-RWB-E1-043-020 | FR-RWB-011 | §14 |
| SPEC-RWB-E1-043-021 | FR-RWB-011 | BR1, §17 |
| SPEC-RWB-E1-043-022 | FR-RWB-011 | §13 done-when (SIT): seam, not covered here; content owned by the table stories (GAP-43) |
| SPEC-RWB-E1-043-023 | NFR-RWB-006 | §17 |
| SPEC-RWB-E1-043-024 | FR-RWB-011, NFR-RWB-005 | §9 rollback |
| SPEC-RWB-E1-043-025 | FR-RWB-011 (REQ-CWC-006) | §13 step 7; D-RUN-11, D-RUN-18; S7-001 §12, X4-X7; S7-019 AC4, AC5 |
| SPEC-RWB-E1-043-026 | FR-RWB-011, NFR-RWB-005 | §13 step 7; D-RUN-10; access-list guard (gate finding 122) |
| SPEC-RWB-E1-043-027 | NFR-RWB-005 | §10 |
| SPEC-RWB-E1-043-028 | FR-RWB-012, NFR-RWB-005, NFR-RWB-008 | TC-E1-043-11 |
| SPEC-RWB-E1-043-029 | FR-RWB-011 | §13 step 2 |
| SPEC-RWB-E1-043-030 | FR-RWB-011 | §13 step 7; D-RUN-10, D-RUN-11 |
| SPEC-RWB-E1-043-031 | FR-RWB-011, NFR-RWB-006 | DL10 D-RCV-29 (registry part); S7-064 §3, §12 |
| SPEC-RWB-E1-043-032 | FR-RWB-011 | BR3 (R-UNI-38), BR8, §9 row 4; S7-019 BR3, AC2, AC9 (gate findings 132, 138); S7-001 flow step 10 |

## 2. `aisdlc/docs/increments/INDEX.md`

Row 008: status `Specified (revision 9)`, result per `review/spec-gate-review-9.md`.

## 3. `aisdlc/docs/open-items.md`

- OPEN-036: E1-043 half — spec revision 9 on 2026-11-18; plan still historical. Keep open until the plan
  is re-baselined.
- Close or replace revision 1's rows "Name the handler interface" (settled by D-RUN-11) and "Name the
  owner of reference-table rollback" (built here, D-RUN-10).
- Withdrawn from revision 2 (do not apply): "RWB-E1-001 registers the data-dictionary handler" (owner is
  RWB-E1-064, gate finding 121); "RWB-TE-011's lint reads the loaded dictionary versions" (the lint is not
  a runtime check; orchestrator ruling 2026-11-18); "Correct the LOV-REF-TABLE seed" (not needed, §3.1
  item 6); the "CREATE TABLE IF NOT EXISTS" option for RWB-E1-001 (gate finding 124).
- New items (IDs assigned by the orchestrator). Owners are roles; nothing here names a person.

| # | Item | Story | Owner | Needed by | Source |
|---|---|---|---|---|---|
| R1 | **Ratify or reject the AI-orchestrator rulings as applied in RWB-E1-043 spec revision 9.** D-RUN-10 (this story owns the shared load, approve and rollback endpoint and the PARAMETER branch; rollback built here, not by RWB-E1-019); D-RUN-11 (handler registry; `data_product` registered by RWB-E1-001, not refused by design); D-RUN-08 (later-story work as seams, including the `sys_fields` handler of RWB-E1-064 and the 12 tables' SIT content). Also listed, not required here: D-RUN-12, D-RUN-18 (handler SPI published by P4 `access.api`; see R24), D-RUN-19, D-RUN-20 (see R24, R33), D-RUN-21 (one-module rule; see R22; OPEN-050), the orchestrator's triage of 2026-11-18 05:52:36 (R33 answer) and the 2026-11-18 triage of rounds 2 to 4 (placement in P3, the effective-date default, Lows fixed under D-RUN-09; round 4 at 04:55: current-state handlers refused before `validFrom`, the early repeat limited to handler codes with a repeat message). All were made by Claude Code (the orchestrator, an AI agent); none is ratified | RWB-E1-043 | Engagement lead, with the tech lead and the RWB-E1-001, RWB-E1-019 and RWB-E1-064 owners | Plan gate | `AI-SDLC-BUILD-LOG.md` §1; spec §"Owner acceptance"; gate finding 130 |
| R2 | **RWB-E1-001 forward contract: §3.1 below** (handler contract on the P4 SPI, `CURRENT_STATE` dating, catalog rows, messages, repeat, no LOV change, no reference tables in its migration) | RWB-E1-001 | RWB-E1-001 owner | RWB-E1-001 specify (held until review 3) | SPEC-025; D-RUN-11, D-RUN-12, D-RUN-18; gate findings 120, 124, 138, 140, 141; E1-001 gate 2 finding 014 |
| R3 | **RWB-E1-064 forward note: §3.2 below** (`sys_fields` handler on the P4 SPI, `CURRENT_STATE` dating, and the `is_personal` protection, stated requirement) | RWB-E1-064 | RWB-E1-064 owner | RWB-E1-064 specify | SPEC-031; gate findings 121, 138, 141; D-RUN-18; E1-001 gate 2 finding 017 |
| R4 | Decide which governed path may change an `is_personal` mark in `sys_fields` (no source defines one; until then the RWB-E1-064 handler refuses any change by a load). Protective default applies unless RW-COMPLY rules otherwise | RWB-E1-064 | RW-COMPLY | Before the first dictionary load | S7-064 §11; TE011 §10; DL26; GAP-38 |
| R5 | RWB-E1-019 implements `access.api.ReferenceTableHandler` (P4 SPI, D-RUN-18) for QUEUE and QUEUE_MEMBER: `ReferenceTableCheck` becomes `validate` (its MSG-P1-002 and MSG-GEN-002 failures pass through unchanged, SPEC-025); `ReferenceRollbackHandler` becomes `supportsRollback = true` and `onRolledBack`; each handler declares `dating()`: `DATED` if `apply` and `onRolledBack` store dated versions only and never change `queue` or `queue_member` before the valid-from date (its `QueueVersionApplier` then applies the version in force on the valid-from date, its flow step 5, BR3, AC9), else `CURRENT_STATE`, in which case RWB-E1-043 refuses approval until the valid-from date and `apply` writes at once (RWB-E1-043 SPEC-025 *Effective date*, SPEC-032 rules 5-6; the choice is RWB-E1-019's); QUEUE_MEMBER needs no LOV-REF-TABLE row although its line 38 says it is added (GAP-49); its build step 5 (rollback endpoint) is replaced by RWB-E1-043's endpoint; it seeds `rwb.refload.approver.queue` (RW-TEAMMGR per its flow step 4) and the QUEUE_MEMBER keys (catalog file + its migration); a QUEUE column definition, if kept, holds types and keys only so its own messages lead | RWB-E1-019 | RWB-E1-019 owner | RWB-E1-019 specify | G-R01, G-R02; GAP-39, GAP-45, GAP-49; SPEC-024, 025, 032; gate finding 138 |
| R6 | RWB-E1-042: (a) RWB-E1-043 revision 9 is baselined on its revision 12 (`spec.md` 2026-11-18 05:50:36, `assumptions.md` and `shared-updates.md` 05:50:52, the files current when read; earlier revisions used its revisions 5, 7, 9 and 10, and revision 11 was checked; the names below are unchanged; findings 144, 148, 157); **keep these names stable** through its gate, or tell RWB-E1-043 of any rename: `casewf.config.api` `ParameterService`, `ParameterKeys.byName(String key, Class<T> type)`, `ParameterLoadHandler` (`load`, `approve`, `rollback`, `find`), `ParameterLoadResult`, `BusinessDateProvider`; `access.api` `CapabilityCheck` (`has`, `require(Authentication, String area, String right, String action)`), `MessageResolver` (`english(String messageId, Map<String, String> placeholders)`, `thai(...)`), `ApiProblemException` (form `(HttpStatus status, String messageId, Map<String, String> placeholders, String field, String detail, Throwable cause)` and `(ApiError, Map, Throwable)`), `ApiError`; grants file `access/interim-capability-grants.csv`; flag binding by `@ConditionalOnProperty` only; (e) its `VersionDecisionRecorder` stays package-private, so RWB-E1-043 records AC-VERS through its own port with the same pattern and the same 503 MSG-P7-003 rule (GAP-50); (b) consider aligning repeat approve/rollback with RWB-E1-043 §12 (200 same body) on the shared endpoint (GAP-35); (c) note that RWB-E1-043 adds Reference data rows to the interim grants file and 38 catalog rows; (d) optional defence in depth: add `rwb.refload.*` to the keys its check 5 refuses (RWB-E1-043 already refuses them before calling `load`) | RWB-E1-042 | RWB-E1-042 owner | RWB-E1-042 gate | D-RUN-10; SPEC-008, 018, 026, 027, 029; gate findings 122, 128, 131, 144 |
| R7 | Deliver a governed path for changing the `rwb.refload.*` loader and approver lists, with its own approver (not the PARAMETER approver list); until then they change only by a reviewed catalog-file pull request plus a migration row. Also load Reference data A for the approver roles in the permission matrix and replace the interim grants (RWB-E1-043 adds A for RW-RISK, RW-COE, RW-DATASTEW, RW-TEAMMGR, RW-COMPLY, RW-SECADM) | RWB-E1-037 | Risk / access owner | RWB-E1-037 | GAP-14, GAP-22, GAP-41; A-08, A-39; gate findings 122, 126 |
| R8 | Replace `ActorIdResolver` (`oid` if a UUID, else `sub` if a UUID, else 401) with the session user; confirm which claim Entra ID tokens carry in each environment | RWB-E1-022 | E1-022 owner; platform owner | RWB-E1-022; before SIT | A-07; gate finding 127 |
| R9 | Rule on backend context v2.0 line 138 (logs carry the user ID) against BS-4.6 and the inventory v4; until RWB-E1-039 a refused reference load cannot be attributed to an actor from RWB-E1-043's records (only `traceId`) | RWB-E1-043, RWB-E1-039 | DPO, with the E1-039 owner | Before SIT | GAP-42; A-30; gate finding 129 |
| R10 | Name owners for the content and column definitions of PRODUCT, REGION and EXPOSURE_BAND, and confirm the release SIT exit for the 12 tables waits on the latest content story (RWB-E1-028, order 47) | RWB-E1-043 / BA | BA; QA lead | Before release SIT | GAP-43; SPEC-022; gate finding 123 |
| R11 | Accept the default loader and approver lists, and name RW-COE's tables if any (by reviewed catalog change) | RWB-E1-043 | Access owner; Risk | Plan gate | A-31, A-39; GAP-19 |
| R12 | Owner acceptance of A-01, A-07, A-08, A-09, A-16, A-17, A-27, A-31, A-33, A-34, A-37, A-38, A-39, A-40, A-41, A-42 (revised in revision 5: `DATED` / `CURRENT_STATE`) (none accepted yet) | RWB-E1-043 | BA, Risk, tech lead, data owner, access owner, E1-001 owner | Plan gate | Gate findings 116, 130 |
| R13 | Person-level separation of duty (RW-REFADM vs RW-RISK) in the role assignment check | RWB-E1-022 | E1-022 owner | RWB-E1-022 | S7 §10; S7-022 SOD-2026.11 |
| R14 | Replace `LoggingReferenceLoadAudit` with the access log (AC-DENY on 403) | RWB-E1-039 | E1-039 owner | RWB-E1-039 | SPEC-028; GAP-26 |
| R15 | Replace RWB-E1-043's interim `LoggingReferenceDecisionRecorder` (package-private port `ReferenceDecisionRecorder` in `casewf.refdata.internal`) with a call to P7 `DecisionLogWriter` for AC-VERS, as for RWB-E1-042's recorder | RWB-E1-027 | E1-027 owner | RWB-E1-027 | GAP-07, GAP-50; A-43 |
| R16 | Replace RWB-E1-042's interim `BusinessDateProvider` with the `v_ace_batch_status` rule (latest complete date); a P3 → P1 call is allowed under D-RUN-18, because P1 never depends on P3 (R24) | Story reading the view after RWB-E1-069 | Tech lead; ACE batch owner | Before SIT | A-01; GAP-12, GAP-51 |
| R17 | Engines read through `ReferenceDataReaders.forReader("<component>")` at start and expiry, stop on `NoVersionInForceException`, and record the version used with each decision (BR6) | RWB-E1-018, -020, -028; RWB-E1-072 (SY-RULES) | Those owners | Their specify | A-02; S7 §10 |
| R18 | Name the owner of `GET /admin/lists/{listCode}` and the HTTP read of versions by RW-AUDIT and RW-REFADM (only the Java `versions()` is built here) | RWB-E1-043 / BA | BA | Before RWB-E1-025 | GAP-34; gate finding 123 |
| R19 | List the reference load result in the daily data quality report | RWB-E1-011 | E1-011 owner | RWB-E1-011 | GAP-33 |
| R20 | Supply the column definition values for each built-in table (A-34 grammar, at most 400 characters) | RWB-E1-019, -025, -038, -045, -046; Legal (LEGAL_PERIOD); R10 for the rest | Table owners | Before SIT loads of version 1 | GAP-13, GAP-30 |
| R21 | MSG-P4-003 wording for an unknown load; 400 vs 422 in REQ §10; API v4: add 404 (branch off) to the load and 500 (handler defect) to load, approve and rollback, and retag the three operations from P4 to P3 `casewf.refdata` | Message / API owners | BA; API owner | Next document set | GAP-27, GAP-28, GAP-48, GAP-53 |
| R22 | **Plan-gate check of the module scope under D-RUN-21.** The plan touches P3 `casewf.refdata` and P4 (`access.api.ListOfValuesReader` and its interim reader, the handler SPI types under D-RUN-18 and D-RUN-20, grants rows), all inside the ACE recovery module, and no common or collection module. Under D-RUN-21 (orchestrator run decision, 2026-11-18 05:36, decisions table line 44; tech-lead ratification open, OPEN-050), "touches one module" in AGENTS §7 and §9 means the ACE module, so the plan does not go back to the analyst; the plan gate checks this reading. No tech-lead approval is claimed; if the tech lead rejects D-RUN-21, the module question returns to the plan gate and the analyst | RWB-E1-043 | Plan gate; recovery tech lead (OPEN-050) | Plan gate | AGENTS §7, §9; D-RUN-21; GAP-59; RWB-E1-042 revision 12 R7-3 (line 1008) and CLAR-025 (line 1198); gate findings 118, 131, 155 |
| R23 | Assign `<seq>` for `V<seq>__rwb_e1_043_reference_versions.sql` before RWB-E1-001's file | RWB-E1-043 | Orchestrator | Merge | D-RUN-07; GAP-15 |
| R24 | **P1 ↔ P3 cycle and the `PARAMETER` route: settled by D-RUN-18 and D-RUN-20, pending ratification by the recovery tech lead.** The orchestrator (Claude Code) ruled at 2026-11-18 04:55 (D-RUN-18) that the reference-load handler SPI is published by P4 `access.api` (as Story v7 RWB-E1-001 §12 says); the ruling reads "P1 (RWB-E1-001) and P3 (RWB-E1-042) handlers implement it" and that the RWB-E1-043 registry in P3 collects the beans by the P4 type; it names no other story as a handler implementer. In this spec the implementers are the P1 handlers of RWB-E1-001 and RWB-E1-064 and the P3 handlers of RWB-E1-019 (SPEC-025), while `PARAMETER` (RWB-E1-042) is a dispatcher branch that implements no SPI type, as RWB-E1-042 revision 12 also states and D-RUN-20 (orchestrator run decision, 2026-11-18 05:34, decisions table line 43; ratification by the recovery tech lead is an open item) rules: the P4 SPI is for handlers outside the registry's module, and `PARAMETER` is a dispatcher branch of the registry calling `casewf.config.api` inside P3 (GAP-57 settled, pending ratification; R32; finding 152). RWB-E1-019's P3 handlers implement the P4 SPI, as the orchestrator's triage of 2026-11-18 05:52:36 answers R33 (GAP-58 settled). P1 never depends on P3, so P3 → P1 reads (RWB-E1-042 §4.3 business date; Story v7 RWB-E1-028 flow step 3; Story v7 RWB-E1-043 §12 working-day calculator) are allowed. RWB-E1-043 revision 9 is built that way (SPEC-019 edge table, SPEC-025). Ratify or reject; a rejection reopens GAP-36, GAP-51, GAP-53 and GAP-57 | RWB-TE-001, RWB-E1-001, RWB-E1-064, RWB-E1-069, RWB-E1-042, RWB-E1-043 | Recovery tech lead, with the RWB-TE-001 owner | Before RWB-E1-001 plan | D-RUN-18, D-RUN-20; GAP-36, GAP-51, GAP-53, GAP-57; SPEC-019, 025; TE-001 SPEC-022 (d); gate finding 141 |
| R25 | RWB-TE-001 module map: add `refdata.api` to the casewf `published` list of `recovery-modules.yaml` (done in RWB-E1-043's merge request); note the new edge `casewf.refdata` → `access.api` and the new P4 published types `access.api.ListOfValuesReader`, `ReferenceTableHandler` (nested `Dating`), `ReferenceLoadFile`, `HandlerMessage`, `ValidationReport` and `RowCheckFailure` (D-RUN-18); T-TE001-14's expected sets change as in R29 | RWB-TE-001 | RWB-TE-001 owner | RWB-E1-043 merge | TE-001 SU-08, SPEC-025, T-TE001-14; SPEC-019; A-41; D-RUN-18 |
| R26 | Approve right of RW-DATASTEW: Story v7 RWB-E1-001 §10 and RWB-E1-064 §10 give Reference data U, Users, Roles and Permissions v4 line 102 RU, while approving a reference load needs A (S7 §10, API v4). Load A in the matrix or name another approver for `data_product`; until then the interim A row (A-08) stands as an assumption | RWB-E1-037 | Access owner; data steward | RWB-E1-037 | GAP-46; A-08, A-40 |
| R27 | No role code exists for the "data architect" named in Story v7 RWB-E1-069 line 203 and DL10; decide whether the dictionary approver list needs a second role and, if so, add its code to Users, Roles and Permissions | RWB-E1-064, RWB-E1-037 | Access owner; RW-COMPLY | Before the first dictionary load | GAP-47; A-36 |
| R28 | The orchestrator's round-3 default (rollback refuses a version already in force) conflicts with Story v7 RWB-E1-019 AC2; RWB-E1-043 follows AC2 (latest approved version, in force or not). Confirm | RWB-E1-043 | Orchestrator; BA | Plan gate | GAP-52; A-27 |
| R29 | **T-TE001-14 alignment with RWB-E1-042 (revision 10 or later).** RWB-E1-042 TC-45 and §12.12 T-2 extend T-TE001-14; at its revisions 9 to 12 its `access.api` set is `ApiError`, `ApiProblemException`, `MessageResolver`, `CapabilityCheck`, `CatalogParameterReader` (nested `Value`, D-RUN-19), and its casewf named interfaces are `api`, `config.api`, `rules`, `timers`, `workflow`; it merges first (BS6 order 3). RWB-E1-043 (order 8) extends the same test in its merge request: `access.api` = RWB-E1-042's merged set + `ListOfValuesReader`, `ReferenceTableHandler`, `ReferenceLoadFile`, `HandlerMessage`, `ValidationReport`, `RowCheckFailure`; named interfaces + `refdata.api`; `casewf.refdata.api` = `ReferenceVersionRegistry`, `ReferenceDataService`, `ReferenceDataReaders`, `ReferenceVersion`, `VersionedRows`, `NoVersionInForceException`. No assertion is relaxed; RWB-E1-042's "a further public type fails" rule stays and the later merge edits the list. Part (b) of revision 5 (RWB-E1-042 wording on `casewf.refdata.api` and the business-date route) is done in RWB-E1-042 revisions 9 to 12 (its §4.3 line 153, `shared-updates.md` line 26) | RWB-E1-042, RWB-TE-001 | RWB-E1-042 owner; RWB-TE-001 owner | RWB-E1-043 merge | T-TE001-14 (TE001 line 279); E42S revision 12 TC-45, §12.12 T-2 (line 982), `shared-updates.md` line 84; D-RUN-18, D-RUN-19; gate findings 139, 148 |
| R30 | **Answer to RWB-E1-042 `shared-updates.md` row 25.** RWB-E1-043 adds TC-PB-02 (`@Tag("recovery-it")`): the real `ParameterLoadHandler` (`rwb.p3.configservice` on) through the load, approve and rollback endpoints for RWB-E1-042 TC-05, -06, -07, -10 part (a), -11, -16 to -20 and -23, each with RWB-E1-042's expected result. TC-10 part (b) (forced commit failure) is not an HTTP case and stays in RWB-E1-042. RWB-E1-042 may mark row 25 answered | RWB-E1-042 | RWB-E1-042 owner | RWB-E1-043 merge | SPEC-026; E42S row 25; gate finding 145 |
| R31 | **Current-state reference tables (data owner).** PS6 `data_product` (`UNIQUE (product_code)`, one `valid_from`) and `sys_fields` (`UNIQUE (field_id)`, no date) hold one row per key, so a future-dated version cannot be stored without changing what is in force. Interim rule (orchestrator triage round 4, 04:55; A-42): such a handler declares `CURRENT_STATE`; its approval is refused (409 MSG-P3-027) while `validFrom` is after the business date and applied at once on the date. Confirm the rule, or ask for dated catalog tables in a later schema version | RWB-E1-043, RWB-E1-001, RWB-E1-064 | Data owner, with the RWB-E1-001 and RWB-E1-064 owners | Before RWB-E1-001 plan | GAP-54 (G4-R01), GAP-55 (G4-R02); SPEC-025, 032; gate finding 138 |
| R32 | **`PARAMETER` route (G5-R01): answered by D-RUN-20, pending tech-lead ratification.** RWB-E1-043 keeps `PARAMETER` a dispatcher branch: `ParameterLoadBranch` (P3, `casewf.refdata.internal`) takes `ObjectProvider<ParameterLoadHandler>`, answers 404 MSG-P4-003 when it is absent, implements no `access.api` type, and a `PARAMETER` handler bean fails start-up (RWB-E1-043 SPEC-025, SPEC-026, SPEC-030, TC-HD-02). RWB-E1-042 revision 12 states the same route (§4.3 line 147, A-51, R7-1 line 1006), and D-RUN-20 (orchestrator run decision, 2026-11-18 05:34, decisions table line 43; ratification by the recovery tech lead is an open item) rules it. Nothing is left to ask; ratification goes with R24 | Orchestrator | Recovery tech lead with R24 | Before the RWB-E1-043 plan | GAP-57; D-RUN-10, D-RUN-18, D-RUN-20; E42S revision 12 line 147, A-51, R7-1; gate findings 149, 152 |
| R33 | **RWB-E1-019's P3 handlers under D-RUN-20 (G7-R01): answered by the orchestrator's triage row of 2026-11-18 05:52:36 (`AI-SDLC-BUILD-LOG.md` line 304).** The answer: a P3 handler may implement the P4 SPI because P3 → P4 is an existing edge, and D-RUN-20 makes only `PARAMETER` a dispatcher branch; so the QUEUE and QUEUE_MEMBER handlers of RWB-E1-019 implement the P4 SPI, as RWB-E1-043 SPEC-019 and SPEC-025 plan (A-46). Nothing is left to ask; ratification goes with OPEN-050 | RWB-E1-043, RWB-E1-019 | Orchestrator (Claude Code); recovery tech lead (OPEN-050); RWB-E1-019 owner to note | Before the RWB-E1-019 spec | GAP-58; A-46; D-RUN-18, D-RUN-20; triage row 05:52:36; gate review 7 G7-R01, review 8 finding 156 |

### 3.1 Forward contract to RWB-E1-001 (row R2; replaces revision 2's rows)

RWB-E1-001 (BS6 order 9) can conform to the following without other input. Source: RWB-E1-043 spec
revision 9 SPEC-019, SPEC-025, SPEC-026, SPEC-027, SPEC-029, SPEC-032.

1. **Tables.** RWB-E1-001's migration does not create `reference_version` or `reference_row` and does not
   create `uk_reference_row UNIQUE (row_key)`. Each table is created by exactly one migration (D-RUN-12,
   an AI-orchestrator ruling, not ratified); these two are RWB-E1-043's. Its data-dictionary rows and
   conformance tests describe them with `UNIQUE (version_id, row_key)`. (Gate finding 108, 124; GAP-01,
   GAP-25.)
2. **Handler.** A Spring bean implementing `recovery.access.api.ReferenceTableHandler` (published by P4,
   D-RUN-18, as its own §12 says; settled for the build, pending tech-lead ratification, R24), behind
   RWB-E1-001's own flag. It depends on P4 only and imports nothing from `recovery.casewf..` (a
   `RecoveryBoundaryTest` rule; SPEC-019): `tableCode()` = `data_product`; `keyColumns()` =
   `List.of("product_code")`; `dating()` = `CURRENT_STATE` (the default; PS6 `uk_data_product`; GAP-54);
   `validate` returns its K0-K5 failures as `RowCheckFailure(row, column, messageCode, placeholders)` with
   its own IDs (MSG-GEN-001; MSG-P3-027 for its K0; MSG-P1-003; MSG-P1-004; MSG-P1-007), reading only its
   own tables; `repeatMessage` returns `HandlerMessage("MSG-P1-011", {source="data product catalog",
   date=<validFrom>})`; `apply` is called only when `validFrom` is on or before the business date and
   writes the 14 rows in the approve transaction with `data_product.valid_from` = `validFrom` (its flow
   step 10; Data Dictionary v8 DF-REF-079); `supportsRollback` per its own story (if true, `onRolledBack`
   writes the restored version's rows at once).
3. **Checks that run before the handler, in order** (SPEC-025 L1-L12): authenticated and actor ID (401
   MSG-P4-001); Reference data C (403 MSG-P4-002); `table` present (422 MSG-GEN-001 `table`); role in
   `rwb.refload.loader.data_product` (403); flag (404 MSG-P4-003); `file` and `validFrom` present (422
   MSG-GEN-001); file readable (422 MSG-P3-027); at least one row (422 MSG-GEN-001 `rows`); repeat
   `(table, validFrom, content_hash)` → 409 MSG-P1-011 from `repeatMessage`, nothing written, for any
   business date (so its AC10 holds after the business date passes `validFrom`); `validFrom` not before
   the business date (422 MSG-P3-027); approved twin with this `validFrom` (409 MSG-P3-027); column
   definition: none for `data_product`, so skipped. Then `validate` (L13); then `row_key` uniqueness (L14).
   Because `repeatMessage` is present, its repeat check runs before the valid-from check (L9); codes
   without a repeat message keep the story order (findings 133, 140; GAP-56).
   `validate` may also return MSG-P1-011 for the wider X7 case (equal to the version in force under a
   different `validFrom`); that is a pass-through 422.
4. **Message pass-through.** The first failure's `messageCode`, placeholders and column are returned
   unchanged as the Problem (422), `detail` lists every failure; never re-mapped to MSG-P3-027. It raises
   them through `recovery.access.api.ApiProblemException` (P4; E42S revision 12 §10.2, §12.2), the same
   P4 dependency as the SPI. Its IDs must be in RWB-E1-042's message catalog. An `ApiProblemException` it throws passes through; another
   exception in `validate` is 500, in `apply` 409 MSG-GEN-004.
5. **Seed rows in RWB-E1-001's catalog file and migration** (`INSERT ... ON CONFLICT (param_key) DO
   NOTHING`; E42S line 106): exactly two `parameter_catalog` rows, both CODE_LIST, kind BUSINESS, scope
   GLOBAL, `required=false`, environments DEV,SIT,UAT,PROD, `secret=false`, owner RW-RISK:
   `rwb.refload.loader.data_product` default `RW-REFADM` (S7-001 X8) and
   `rwb.refload.approver.data_product` default `RW-DATASTEW` (S7-001 flow step 9) (A-40). **No**
   `refdata.columns.data_product` row (E01S SPEC-013). Interim Reference data A for RW-DATASTEW is added
   by RWB-E1-043 (A-08) as an assumption: the sources give RW-DATASTEW U or RU (GAP-46; R26), so
   RWB-E1-001 edits no grants file.
6. **LOV-REF-TABLE: no change.** `data_product` needs no LOV row (D-RUN-11). RWB-E1-043 refuses the rule
   codes and HOLIDAY itself (no column definition), so RWB-E1-001 seeds the PS6 LOV-REF-TABLE rows
   unchanged. Rows to add: none. Rows to remove: none. Revision 2's request is withdrawn (GAP-04).
7. **Repeat behaviour.** S7-001 X7 says a repeat is a file matching "the version in force"; the registry
   tests `(table, validFrom, content_hash)`, before the valid-from check only for handler codes with a
   repeat message (such as `data_product`). Differences recorded as GAP-44 and GAP-56 for the RWB-E1-001
   owner and the BA.
8. **Effective date.** `data_product` is a current-state table: RWB-E1-043 refuses approval of a
   catalog version with 409 MSG-P3-027 while its `validFrom` is after the business date, and approval on
   the date writes the rows at once (SPEC-032 rule 6; A-42; GAP-54). With A-17, out-of-order approval
   cannot occur. A test of its handler shows that it writes nothing before approval and that approval on
   the valid-from date makes the new rows the ones in force (RWB-E1-043 TC-TM-05 proves the registry
   side).

### 3.2 Forward note to RWB-E1-064 (row R3; replaces revision 2's dictionary rows to RWB-E1-001)

Source: S7-064 §3, §4 steps 2-3, §10, §11, §12; RWB-E1-043 spec revision 9 SPEC-019, SPEC-025, SPEC-031, SPEC-032;
D-RUN-08, D-RUN-11 and D-RUN-18 (AI-orchestrator rulings, not ratified).

1. RWB-E1-064 registers an `access.api.ReferenceTableHandler` (P4 SPI, D-RUN-18) for `sys_fields` that
   adapts its `DataDictionaryLoader`; RWB-E1-043 does not call P1 code (GAP-40; S7-064 §12 says the
   opposite direction). The handler depends on P4 only, never on P3, so no cycle arises (SPEC-019; R24;
   GAP-51 settled by D-RUN-18, pending tech-lead ratification).
2. It seeds `rwb.refload.loader.sys_fields` (RW-REFADM, S7-064 §10) and `rwb.refload.approver.sys_fields`
   (RW-COMPLY, **inferred** from TE011 §10, A-36) in the catalog file and its migration; until then every
   `sys_fields` load and approval is refused. No role code exists for a data architect (Users, Roles and
   Permissions v4), so none is named (GAP-47; R27). RW-DATASTEW holds Reference data U in S7-064 §10, not
   the A an approval needs (GAP-46).
3. **Stated requirement (protective; applies unless RW-COMPLY rules otherwise):** `validate` refuses a
   file whose `is_personal` value for an existing field differs from the value in force, 422 MSG-P1-002
   `{check}` = "is_personal cannot be changed by a load"; `apply` and `onRolledBack` never write
   `is_personal`, so a rollback cannot restore an earlier mark. Open item R4 (owner RW-COMPLY) decides the
   governed path for changing a mark. (E1-001 gate 2 finding 017; S7-064 §11 DF-REF-105 Read.)
4. `changeSummary` reports changed field IDs and attributes only, never values (A-35).
5. RWB-TE-011's lint covers committed SQL, fixtures and logs; it is not a runtime check. Nothing is
   asked of RWB-TE-011 by RWB-E1-043.
6. Effective date: `sys_fields` and `sys_field_version` hold no date (PS6), so the handler declares
   `dating()` = `CURRENT_STATE` (the default; GAP-55). RWB-E1-043 refuses approval with 409 MSG-P3-027
   while `validFrom` is after the business date; approval on the date calls `apply`, which writes the
   definitions at once (SPEC-032 rule 6; A-42). Owner of the rule: the data owner (R31).

## 4. `aisdlc/DOCUMENT-GAPS.md`

Candidate rows GAP-01 to GAP-59 are in `specify/document-gaps.md` (no blocker for this story). Number
them `DG-nnn` with "Raised by: INC-008 specify GAP-xx"; GAP-20 to GAP-29 also carry "spec gate review 1
G-R01..G-R10", GAP-39 to GAP-43 "spec gate review 2 G2-R01..G2-R05" and GAP-45 to GAP-49 "spec gate
review 3 G3-R01..G3-R05" GAP-54 to GAP-56 "spec gate review 4 G4-R01..G4-R03" GAP-57 "spec gate review 5 G5-R01" (settled by D-RUN-20) GAP-58 "spec gate review 7 G7-R01" (settled by the orchestrator's triage of 2026-11-18 05:52:36) and GAP-59 "spec gate review 8 G8-R01" (a cross-reference to RWB-E1-042 E1042-SP-DG-16 and RWB-TE-001 PG-04, not a new entry). GAP-37 and GAP-38 are corrected in revision 3, GAP-36 in revision 4, and GAP-36, GAP-51 and GAP-53 in revision 5 (D-RUN-18, pending tech-lead ratification); GAP-04's seed correction request is withdrawn. GAP-24 (G-R05) is Blocker = No under
D-RUN-10 and D-RUN-11.

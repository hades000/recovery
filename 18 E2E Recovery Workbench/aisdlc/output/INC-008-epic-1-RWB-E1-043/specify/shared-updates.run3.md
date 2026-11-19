# Shared updates requested: RWB-E1-043 specify (INC-008-epic-1-RWB-E1-043)

Revision 3, 2026-11-18 (remediation run 2; revisions 1 and 2 kept as `shared-updates.run1.md` and
`shared-updates.run2.md`). The Technical Specifier does not edit shared files (RUN-BRIEF). The
orchestrator applies these rows in order. Every ruling cited here (D-RUN-07..12, the 2026-11-18 triage)
was made by the orchestrator, Claude Code, an AI agent; none has been ratified by a human (§3, row R1).

## 1. `aisdlc/requirement/Traceability_Matrix.md`

Replace the INC-008 row in the increment trace:

| 008 | `RWB-E1-043` | `BR-RWB-011` | `FR-RWB-011` (REQ-DRI-011, REQ-CWC-006; R-UNI-38, CTL-08, REQ-CWC-016) | `output/INC-008-epic-1-RWB-E1-043/specify/spec.md` (revision 3, 18 Nov 2026) | Specified — remediation run 2; spec gate see `review/spec-gate-review-3.md`; plan not started |

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
| SPEC-RWB-E1-043-025 | FR-RWB-011 (REQ-CWC-006) | §13 step 7; D-RUN-11; S7-001 §12, X4-X7; S7-019 AC4, AC5 |
| SPEC-RWB-E1-043-026 | FR-RWB-011, NFR-RWB-005 | §13 step 7; D-RUN-10; access-list guard (gate finding 122) |
| SPEC-RWB-E1-043-027 | NFR-RWB-005 | §10 |
| SPEC-RWB-E1-043-028 | FR-RWB-012, NFR-RWB-005, NFR-RWB-008 | TC-E1-043-11 |
| SPEC-RWB-E1-043-029 | FR-RWB-011 | §13 step 2 |
| SPEC-RWB-E1-043-030 | FR-RWB-011 | §13 step 7; D-RUN-10, D-RUN-11 |
| SPEC-RWB-E1-043-031 | FR-RWB-011, NFR-RWB-006 | DL10 D-RCV-29 (registry part); S7-064 §3, §12 |

## 2. `aisdlc/docs/increments/INDEX.md`

Row 008: status `Specified (revision 3)`, result per `review/spec-gate-review-3.md`.

## 3. `aisdlc/docs/open-items.md`

- OPEN-036: E1-043 half — spec revision 3 on 2026-11-18; plan still historical. Keep open until the plan
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
| R1 | **Ratify or reject the AI-orchestrator rulings as applied in RWB-E1-043 spec revision 3.** D-RUN-10 (this story owns the shared load, approve and rollback endpoint and the PARAMETER branch; rollback built here, not by RWB-E1-019); D-RUN-11 (handler registry; `data_product` registered by RWB-E1-001, not refused by design); D-RUN-08 (later-story work as seams, including the `sys_fields` handler of RWB-E1-064 and the 12 tables' SIT content). Also listed, not required here: D-RUN-12 and the 2026-11-18 triage. All were made by Claude Code (the orchestrator, an AI agent); none is ratified | RWB-E1-043 | Engagement lead, with the tech lead and the RWB-E1-001, RWB-E1-019 and RWB-E1-064 owners | Plan gate | `AI-SDLC-BUILD-LOG.md` §1; spec §"Owner acceptance"; gate finding 130 |
| R2 | **RWB-E1-001 forward contract: §3.1 below** (handler contract, catalog rows, messages, repeat, no LOV change, no reference tables in its migration) | RWB-E1-001 | RWB-E1-001 owner | RWB-E1-001 specify (held until review 3) | SPEC-025; D-RUN-11, D-RUN-12; gate findings 120, 124; E1-001 gate 2 finding 014 |
| R3 | **RWB-E1-064 forward note: §3.2 below** (`sys_fields` handler and the `is_personal` protection, stated requirement) | RWB-E1-064 | RWB-E1-064 owner | RWB-E1-064 specify | SPEC-031; gate finding 121; E1-001 gate 2 finding 017 |
| R4 | Decide which governed path may change an `is_personal` mark in `sys_fields` (no source defines one; until then the RWB-E1-064 handler refuses any change by a load). Protective default applies unless RW-COMPLY rules otherwise | RWB-E1-064 | RW-COMPLY, with the data architect | Before the first dictionary load | S7-064 §11; TE011 §10; DL26; GAP-38 |
| R5 | RWB-E1-019 implements `ReferenceTableHandler` for QUEUE and QUEUE_MEMBER: `ReferenceTableCheck` becomes `validate` (its MSG-P1-002 and MSG-GEN-002 failures pass through unchanged, SPEC-025); `QueueVersionApplier` becomes `apply` and `onRolledBack` (`supportsRollback = true`); its build step 5 (rollback endpoint) is replaced by RWB-E1-043's endpoint; it seeds `rwb.refload.approver.queue` (RW-TEAMMGR per its flow step 4) and the QUEUE_MEMBER keys (catalog file + its migration); a QUEUE column definition, if kept, holds types and keys only so its own messages lead | RWB-E1-019 | RWB-E1-019 owner | RWB-E1-019 specify | G-R01, G-R02; GAP-39; SPEC-024, 025 |
| R6 | RWB-E1-042: (a) RWB-E1-043 revision 3 is baselined on its revision 4 (`ParameterKeys.byName(String, Class<T>)`); (b) consider aligning repeat approve/rollback with RWB-E1-043 §12 (200 same body) on the shared endpoint (GAP-35); (c) note that RWB-E1-043 adds Reference data rows to the interim grants file and 38 catalog rows; (d) optional defence in depth: add `rwb.refload.*` to the keys its check 5 refuses (RWB-E1-043 already refuses them before calling `load`) | RWB-E1-042 | RWB-E1-042 owner | RWB-E1-042 gate | D-RUN-10; SPEC-026, 027, 029; gate findings 122, 128 |
| R7 | Deliver a governed path for changing the `rwb.refload.*` loader and approver lists, with its own approver (not the PARAMETER approver list); until then they change only by a reviewed catalog-file pull request plus a migration row. Also load Reference data A for the approver roles in the permission matrix and replace the interim grants (RWB-E1-043 adds A for RW-RISK, RW-COE, RW-DATASTEW, RW-TEAMMGR, RW-COMPLY, RW-SECADM) | RWB-E1-037 | Risk / access owner | RWB-E1-037 | GAP-14, GAP-22, GAP-41; A-08, A-39; gate findings 122, 126 |
| R8 | Replace `ActorIdResolver` (`oid` if a UUID, else `sub` if a UUID, else 401) with the session user; confirm which claim Entra ID tokens carry in each environment | RWB-E1-022 | E1-022 owner; platform owner | RWB-E1-022; before SIT | A-07; gate finding 127 |
| R9 | Rule on backend context v2.0 line 138 (logs carry the user ID) against BS-4.6 and the inventory v4; until RWB-E1-039 a refused reference load cannot be attributed to an actor from RWB-E1-043's records (only `traceId`) | RWB-E1-043, RWB-E1-039 | DPO, with the E1-039 owner | Before SIT | GAP-42; A-30; gate finding 129 |
| R10 | Name owners for the content and column definitions of PRODUCT, REGION and EXPOSURE_BAND, and confirm the release SIT exit for the 12 tables waits on the latest content story (RWB-E1-028, order 47) | RWB-E1-043 / BA | BA; QA lead | Before release SIT | GAP-43; SPEC-022; gate finding 123 |
| R11 | Accept the default loader and approver lists, and name RW-COE's tables if any (by reviewed catalog change) | RWB-E1-043 | Access owner; Risk | Plan gate | A-31, A-39; GAP-19 |
| R12 | Owner acceptance of A-01, A-07, A-08, A-09, A-16, A-17, A-27, A-31, A-33, A-34, A-37, A-38, A-39, A-40 (none accepted yet) | RWB-E1-043 | BA, Risk, tech lead, access owner, E1-001 owner | Plan gate | Gate findings 116, 130 |
| R13 | Person-level separation of duty (RW-REFADM vs RW-RISK) in the role assignment check | RWB-E1-022 | E1-022 owner | RWB-E1-022 | S7 §10; S7-022 SOD-2026.11 |
| R14 | Replace `LoggingReferenceLoadAudit` with the access log (AC-DENY on 403) | RWB-E1-039 | E1-039 owner | RWB-E1-039 | SPEC-028; GAP-26 |
| R15 | Implement `VersionDecisionRecorder` for reference-table approvals (AC-VERS) | RWB-E1-027 | E1-027 owner | RWB-E1-027 | GAP-07 |
| R16 | Replace RWB-E1-042's interim `BusinessDateProvider` with the `v_ace_batch_status` rule (latest complete date) | Story reading the view after RWB-E1-069 | Tech lead; ACE batch owner | Before SIT | A-01; GAP-12 |
| R17 | Engines read through `ReferenceDataReaders.forReader("<component>")` at start and expiry, stop on `NoVersionInForceException`, and record the version used with each decision (BR6) | RWB-E1-018, -020, -028; RWB-E1-072 (SY-RULES) | Those owners | Their specify | A-02; S7 §10 |
| R18 | Name the owner of `GET /admin/lists/{listCode}` and the HTTP read of versions by RW-AUDIT and RW-REFADM (only the Java `versions()` is built here) | RWB-E1-043 / BA | BA | Before RWB-E1-025 | GAP-34; gate finding 123 |
| R19 | List the reference load result in the daily data quality report | RWB-E1-011 | E1-011 owner | RWB-E1-011 | GAP-33 |
| R20 | Supply the column definition values for each built-in table (A-34 grammar, at most 400 characters) | RWB-E1-019, -025, -038, -045, -046; Legal (LEGAL_PERIOD); R10 for the rest | Table owners | Before SIT loads of version 1 | GAP-13, GAP-30 |
| R21 | MSG-P4-003 wording for an unknown load; 400 vs 422 in REQ §10 | Message / API owners | BA | Next document set | GAP-27, GAP-28 |
| R22 | Plan gate decision on the multi-module scope (P3, P4, platform) | RWB-E1-043 | Tech lead / analyst | Plan gate | AGENTS §7; gate finding 118 |
| R23 | Assign `<seq>` for `V<seq>__rwb_e1_043_reference_versions.sql` before RWB-E1-001's file | RWB-E1-043 | Orchestrator | Merge | D-RUN-07; GAP-15 |

### 3.1 Forward contract to RWB-E1-001 (row R2; replaces revision 2's rows)

RWB-E1-001 (BS6 order 9) can conform to the following without other input. Source: RWB-E1-043 spec
revision 3 SPEC-025, SPEC-026, SPEC-027, SPEC-029.

1. **Tables.** RWB-E1-001's migration does not create `reference_version` or `reference_row` and does not
   create `uk_reference_row UNIQUE (row_key)`. Each table is created by exactly one migration (D-RUN-12,
   an AI-orchestrator ruling, not ratified); these two are RWB-E1-043's. Its data-dictionary rows and
   conformance tests describe them with `UNIQUE (version_id, row_key)`. (Gate finding 108, 124; GAP-01,
   GAP-25.)
2. **Handler.** A Spring bean implementing `recovery.casewf.refdata.api.ReferenceTableHandler` (P3, not
   P4; GAP-36), behind RWB-E1-001's own flag: `tableCode()` = `data_product`; `keyColumns()` =
   `List.of("product_code")`; `validate` returns its K0-K5 failures as `RowCheckFailure(row, column,
   messageCode, placeholders)` with its own IDs (MSG-GEN-001; MSG-P3-027 for its K0; MSG-P1-003;
   MSG-P1-004; MSG-P1-007); `repeatMessage` returns `HandlerMessage("MSG-P1-011", {source="data product
   catalog", date=<validFrom>})`; `apply` writes its rows in the approve transaction; `supportsRollback`
   per its own story.
3. **Checks that run before the handler, in order** (SPEC-025 L1-L11): authenticated and actor ID (401
   MSG-P4-001); Reference data C (403 MSG-P4-002); role in `rwb.refload.loader.data_product` (403); flag
   (404 MSG-P4-003); fields present (422 MSG-GEN-001); file readable (422 MSG-P3-027); at least one row
   (422 MSG-GEN-001 `rows`); `validFrom` not before the business date (422 MSG-P3-027); repeat
   `(table, validFrom, content_hash)` → 409 MSG-P1-011 from `repeatMessage`, nothing written; approved
   twin with this `validFrom` (409 MSG-P3-027); column definition: none for `data_product`, so skipped.
   Then `validate` (L12); then `row_key` uniqueness (L13).
4. **Message pass-through.** The first failure's `messageCode`, placeholders and column are returned
   unchanged as the Problem (422), `detail` lists every failure; never re-mapped to MSG-P3-027. Its IDs
   must be in RWB-E1-042's message catalog. An `ApiProblemException` it throws passes through; another
   exception in `validate` is 500, in `apply` 409 MSG-GEN-004.
5. **Seed rows in RWB-E1-001's catalog file and migration** (`INSERT ... ON CONFLICT (param_key) DO
   NOTHING`; E42S line 106): exactly two `parameter_catalog` rows, both CODE_LIST, kind BUSINESS, scope
   GLOBAL, `required=false`, environments DEV,SIT,UAT,PROD, `secret=false`, owner RW-RISK:
   `rwb.refload.loader.data_product` default `RW-REFADM` (S7-001 X8) and
   `rwb.refload.approver.data_product` default `RW-DATASTEW` (S7-001 flow step 9) (A-40). **No**
   `refdata.columns.data_product` row (E01S SPEC-013). Interim Reference data A for RW-DATASTEW is added
   by RWB-E1-043 (A-08), so RWB-E1-001 edits no grants file.
6. **LOV-REF-TABLE: no change.** `data_product` needs no LOV row (D-RUN-11). RWB-E1-043 refuses the rule
   codes and HOLIDAY itself (no column definition), so RWB-E1-001 seeds the PS6 LOV-REF-TABLE rows
   unchanged. Rows to add: none. Rows to remove: none. Revision 2's request is withdrawn (GAP-04).
7. **Repeat behaviour.** S7-001 X7 says a repeat is a file matching "the version in force"; the registry
   tests `(table, validFrom, content_hash)` for every code. Difference recorded as GAP-44 for the
   RWB-E1-001 owner and the BA.

### 3.2 Forward note to RWB-E1-064 (row R3; replaces revision 2's dictionary rows to RWB-E1-001)

Source: S7-064 §3, §4 steps 2-3, §10, §11, §12; RWB-E1-043 spec revision 3 SPEC-025, SPEC-031; D-RUN-08
and D-RUN-11 (AI-orchestrator rulings, not ratified).

1. RWB-E1-064 registers a `ReferenceTableHandler` for `sys_fields` that adapts its `DataDictionaryLoader`;
   RWB-E1-043 does not call P1 code (GAP-40; S7-064 §12 says the opposite direction).
2. It seeds `rwb.refload.loader.sys_fields` (RW-REFADM, S7-064 §10) and `rwb.refload.approver.sys_fields`
   (RW-COMPLY and the data architect's role, A-36) in the catalog file and its migration; until then
   every `sys_fields` load and approval is refused.
3. **Stated requirement (protective; applies unless RW-COMPLY rules otherwise):** `validate` refuses a
   file whose `is_personal` value for an existing field differs from the value in force, 422 MSG-P1-002
   `{check}` = "is_personal cannot be changed by a load"; `apply` and `onRolledBack` never write
   `is_personal`, so a rollback cannot restore an earlier mark. Open item R4 (owner RW-COMPLY) decides the
   governed path for changing a mark. (E1-001 gate 2 finding 017; S7-064 §11 DF-REF-105 Read.)
4. `changeSummary` reports changed field IDs and attributes only, never values (A-35).
5. RWB-TE-011's lint covers committed SQL, fixtures and logs; it is not a runtime check. Nothing is
   asked of RWB-TE-011 by RWB-E1-043.

## 4. `aisdlc/DOCUMENT-GAPS.md`

Candidate rows GAP-01 to GAP-44 are in `specify/document-gaps.md` (no blocker for this story). Number
them `DG-nnn` with "Raised by: INC-008 specify GAP-xx"; GAP-20 to GAP-29 also carry "spec gate review 1
G-R01..G-R10" and GAP-39 to GAP-43 "spec gate review 2 G2-R01..G2-R05". GAP-37 and GAP-38 are corrected
in revision 3; GAP-04's seed correction request is withdrawn. GAP-24 (G-R05) is Blocker = No under
D-RUN-10 and D-RUN-11.

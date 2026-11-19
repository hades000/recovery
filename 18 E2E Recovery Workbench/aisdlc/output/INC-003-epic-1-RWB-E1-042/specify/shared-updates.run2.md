# Shared updates requested: RWB-E1-042 specification, revision 3

RUN_ID `INC-003-epic-1-RWB-E1-042`, stage `specify`, 2026-11-17. This stage did not edit any shared file
(RUN-BRIEF rule 3). The orchestrator applies these rows in order and assigns IDs (`OPEN-0NN`, `DG-0NN`).
Per triage decision (e), the clarification pack's open items are carried **open**; none is marked resolved.

## 1. `aisdlc/docs/open-items.md` (append to "Open")

Columns as the register: ID, Item, Stories affected, Owner, Needed by, Raised in.

| ID | Item | Stories affected | Owner | Needed by | Raised in |
|---|---|---|---|---|---|
| (new) | OI-E1-042-001: run TC-E1-042-12 (RW-PHONECOL reads parameters: 403 MSG-P4-002 "read parameters", one refusal event) after RWB-E1-037 loads PM-2026.11 and RWB-E1-022 resolves the RW-PHONECOL test identity. Until then `Blocked`, not passed | RWB-E1-042, RWB-E1-022, RWB-E1-037 | QA lead / recovery tech lead | Before the live access suite runs | E1-042 Clarification Pack §5, OI-E1-042-001; spec CLAR-001 |
| (new) | OI-E1-042-002: the story's two-file migration names fail D-RCV-28 and the lint. Spec uses one file `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql`, number at merge (D-RUN-07). Story text to be reissued | RWB-E1-042 | BA (story owner) / recovery tech lead | Next story issue | Pack OI-E1-042-002; spec CLAR-002 |
| (new) | OI-E1-042-003: full Epic 1 `config/parameter-catalog.csv` absent; spec seeds a 19-row bootstrap; each later story adds its rows by PR and migration | All Epic 1 stories reading parameters | RW-COE | Before each reading story's spec | Pack OI-E1-042-003; spec CLAR-003 |
| (new) | OI-E1-042-004: no message table and no owner; spec uses a fixed catalog behind `MessageResolver` | All stories with messages | Solution architect (assign owner; RWB-E1-043 or a new story) | Before Epic 1 UAT | Pack OI-E1-042-004; spec CLAR-004 |
| (new) | OI-E1-042-005: no per-table-code CSV template register; spec defines only the PARAMETER header `key,environment,value` | RWB-E1-043, owners of each table code | RWB-E1-043 specifier / data architect | Before RWB-E1-043 spec | Pack OI-E1-042-005; spec CLAR-005 |
| (new) | OI-E1-042-006: naming conflicts (`case.entry.dpd` / `case.entry.dpd_threshold` / `ENTRY_DPD`; prescription and tolerance keys). Spec default: `case.entry.dpd` GLOBAL, `ENTRY_DPD` RWB-E1-045 product key, others not seeded | RWB-E1-042, RWB-E1-045, RWB-E1-018 | RW-COE / BA | Before RWB-E1-045 spec | Pack OI-E1-042-006, Appendix A; spec CLAR-006 |
| (new) | OI-E1-042-007: PRODUCT-scope rows have no default; spec exempts them from the default rule (owner, type, range still required). Story §13 text to be aligned | RWB-E1-042, RWB-E1-045 | BA (story owner) | Next story issue | Pack OI-E1-042-007; spec CLAR-007 |
| (new) | OI-E1-042-008: no load-to-rows link in Physical Schema v6; spec adds `parameter_value.load_id`, `content_hash`, `rollback_reason` (pack option A). Physical Schema to be updated (§4 below) | RWB-E1-042, RWB-E1-043 | Data architect | Next Physical Schema issue | Pack OI-E1-042-008; review finding 104; spec CLAR-008 |
| (new) | OI-E1-042-009: placeholder property. In this repository `RecoveryFlywayConfig.java:37` sets `recoverySchema` from `rwb.schema`; the pack's `spring.flyway.placeholders.recoverySchema` is not needed here. Owner to confirm the ACE deployment (Jenkins, OPEN-019) does the same before closing | RWB-E1-042, every recovery migration | Recovery tech lead | Before the first migration deploys | Pack OI-E1-042-009; spec CLAR-009 |
| (new) | OI-E1-042-010: PRODUCT target table, `DOCUMENT_HUB_PARAMETER` (no LOV-REF-TABLE row) and `RETENTION_CLASS` dispatch; outside RWB-E1-042 (D-RUN-10, D-RUN-11) | RWB-E1-043, RWB-E1-045, RWB-E1-001 | RWB-E1-043 specifier / data architect | Before RWB-E1-043 spec | Pack OI-E1-042-010; spec CLAR-010 |
| (new) | OI-E1-042-011: OpenAPI `postAdminReferenceLoads` lacks `required: [file, table, validFrom]`, `format: date`, LOV on `table`, and the identical-repeat status. Spec default: identical repeat 201 with the same body; conflict 409 MSG-P3-027 | RWB-E1-042, RWB-E1-043, RWB-TE-003 | API owner | Before RWB-E1-043 build | Pack OI-E1-042-011; review finding 106; spec CLAR-011 |
| (new) | Reference data A (approve) is held by no role in Users, Roles and Permissions v4; story assumes the parameter owner (RW-COE) and RW-RISK (DL01); routing "Risk where a threshold moves" is undefined | RWB-E1-043, RWB-E1-037 | Business (RW-COE, RW-RISK) / RWB-E1-037 | Before RWB-E1-043 build | Review finding 118; spec CLAR-013 |
| (new) | `ParameterLoadHandler` (platform.api) is the interface RWB-E1-043's PARAMETER branch calls (D-RUN-10); RWB-E1-043's spec must map multipart input, capability checks C/A/U and HTTP status onto it, and add HTTP tests for TC-05..07, 10, 11, 16-20, 23 | RWB-E1-043 | RWB-E1-043 specifier | Before RWB-E1-043 spec | D-RUN-10, D-RUN-11; spec SPEC-017, §11.2 |
| (new) | Interim seams to replace: `CapabilityCheck` grants file (RWB-E1-037), `VersionDecisionRecorder` (RWB-E1-027), outbox write of `ParameterVersionApproved` (RWB-TE-006), `BusinessDateProvider` (story reading `v_ace_batch_status`), flag to the flag table (RWB-E1-047), Temporal/Drools reads to `ParameterService` (RWB-E1-071, RWB-E1-072) | Named stories | Each named story's specifier | Before each story's spec | Spec §4.3 |
| (new) | `outbox_event.case_seq` is nullable and `UNIQUE (case_seq, idempotency_key)` does not de-duplicate rows with null `case_seq`; non-case events need another idempotency guard | RWB-TE-006 | Data architect / RWB-TE-006 specifier | Before RWB-TE-006 spec | Physical Schema v6 lines 1206-1225; plan input 11 |

## 2. `aisdlc/DOCUMENT-GAPS.md` (candidates)

Append the rows of `specify/document-gaps.md` table "New gaps raised by this stage" (E1042-SP-DG-01 to -09),
all Blocker = No, and the review-stage rows E1042-RV-DG-01 to -15 (`review/document-gaps.md`) if not already
applied. E1042-SP-DG-08 is gap G-R05 of the run log (shared endpoint dispatch, settled by D-RUN-10) and
supersedes the "How this stage proceeded" column of E1042-RV-DG-15.

## 3. `aisdlc/requirement/Traceability_Matrix.md`

| Change | Row |
|---|---|
| Story row 003 (line 51), status column | Replace "Implemented — migration applied and tested; spec and plan rebaselined 16 Nov 2026" with "Specified — spec revision 3 (17 Nov 2026) in this repository; plan and build not started. The 10 Nov implementation was the ACE monorepo pack, not this repository" |
| Add SPEC trace for `FR-RWB-010` | `FR-RWB-010` -> `SPEC-RWB-E1-042-001` .. `-027` -> `output/INC-003-epic-1-RWB-E1-042/specify/spec.md` §5 -> tests `TC-E1-042-01` .. `-31` (TC-12 Blocked, OI-E1-042-001) -> code: pending (plan stage) |

## 4. Requests to document owners (no repository file edited)

| Target | Request | Evidence |
|---|---|---|
| Physical Schema v6 owner (data architect) | Add `parameter_value.load_id uuid`, `content_hash char(64)`, `rollback_reason varchar(400)`; FK `fk_parameter_value_catalog`; checks and indexes of spec §12.3; dictionary rows for the three columns (not personal) | Spec SPEC-002, §12.3; review finding 104, 112 |
| Event and Messaging Design v4 owner | Add `ParameterVersionApproved` (producer platform; payload `loadId, paramKeys[], validFrom, versions[{paramKey, environment, versionNo}], occurredAt`; consumers: parameter cache of every instance) | Spec §11.4; review finding 116 |
| API owner (`api/recovery-api-v4.yaml`) | Hardening of `postAdminReferenceLoads` per OI-E1-042-011; document identical-repeat 201 | Spec §11.3 |
| Story owner, RWB-E1-042 v7 | Reissue §13 migration names to D-RCV-28; align `CatalogCompletenessCheck` with the PRODUCT exemption; X3 wording vs AC4; event payload; package name after the RWB-TE-001 module map | Document gaps E1042-RV-DG-01, -09, E1042-SP-DG-02, -04 |
| Story owner, RWB-E1-043 v7 | §3 line 41 "list of reference table codes" from RWB-E1-042: reword to D-RUN-10/11 (RWB-E1-043 owns dispatch) | E1042-SP-DG-07 |
| RWB-TE-001 (module map) | Map the configuration service (design module P3 `casewf.config`) to the `platform` module or move it | Spec §12.1, A-01, CLAR-020 |
| RWB-E1-001 specifier | `V0001` is reserved for RWB-E1-001 in D-RCV-28, but merge order puts RWB-E1-042 first; RWB-E1-001's baseline must not recreate the parameter tables | E1042-RV-DG-02 |

## 5. Increment card and index

| File | Change |
|---|---|
| `aisdlc/docs/increments/INC-003-epic-1-RWB-E1-042.md`, lines 21 and 147 (Status) | "Specified — spec revision 3, 17 Nov 2026, spec gate re-run (`review/spec-gate-review-2.md`); the 10 Nov 'Implemented' status refers to the ACE monorepo pack" |
| `aisdlc/docs/increments/INDEX.md`, line 18 (status column) and line 94 (summary) | Status "Specified" instead of "Implemented"; remove RWB-E1-042 from the "Implemented" summary |

## 6. Workspace context (orchestrator / Context Updater)

| File | Change |
|---|---|
| `aisdlc/.github/contexts/backend-context.md` line 100 | "Implemented: RWB-E1-042 ... migration" is not true in this repository; replace with "Specified (revision 3); migration number assigned at merge (D-RUN-07)" |
| `aisdlc/.github/contexts/backend-context.md` line 237 | Corrective example `V0043__rwb_e1_042_parameter_seed_fix.sql` implies `V0042` for RWB-E1-042; use `V<seq>__rwb_e1_042_<name>.sql` |

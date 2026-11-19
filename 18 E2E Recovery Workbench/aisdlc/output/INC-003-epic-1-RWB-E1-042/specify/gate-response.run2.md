# Gate response: REVIEW-RWB-E1-042-SPEC-003

RUN_ID `INC-003-epic-1-RWB-E1-042`, stage `specify`, 2026-11-17. Responds to `review/spec-gate-review.md`
(4 High, 7 Medium, 7 Low; findings 101-118; plan inputs 1-14) and to the coordinator's course correction
under run decision D-RUN-10. All references are to `specify/spec.md` revision 3 unless stated.

## 1. Findings

| Finding | Severity | Resolution in revision 3 | Where |
|---|---|---|---|
| 101 | High | One rule only: one file `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql`, `<seq>` assigned at merge (D-RUN-07), line 1 `-- Story: RWB-E1-042`, DDL and seed together, `${recoverySchema}` only, no `SET search_path`, guarded DDL for both an empty schema and a Physical Schema v6 schema. The 10 Nov SQL is input to adapt (renamed, Physical Schema v6 basis, `V0042` removed); the "must not rewrite" rule is deleted. `RWB_SCHEMA` and `${schema}` are gone | SPEC-001; §12.3; TC-13, TC-14, TC-15 |
| 102 | High | AC2 and AC3 restored as rows mapped to SPEC-004 and SPEC-003; TC-02 and TC-03 restored to System level on fixture modules (story §13 build step 7); "AC cleanup" note deleted; counts corrected (11 ACs, 57 rules) | §6 rows AC2, AC3; §15 TC-02, TC-03; §20 |
| 103 | High | Every later dependency is a seam table row with what this story builds now and how it is filled (§4.3). (a) The P4 endpoint: per D-RUN-10 RWB-E1-043 owns the shared reference-load endpoint; this story publishes `ParameterLoadHandler` in `platform.api` and builds no controller (§2 below). (b) In-process `ParameterVersionApproved` after commit plus TTL; outbox by RWB-TE-006. (c) `VersionDecisionRecorder` with an interim log implementation; AC-VERS writer by RWB-E1-027. (d) `CapabilityCheck` with an interim grants file; RWB-E1-037/022 replace it. TC-12 `Blocked` with exit criterion (OI-E1-042-001). Nothing is listed as inherited that the repository does not have | §2 "Inherited Existing Behavior"; §4.3; SPEC-017..020; TC-12 |
| 104 | High | Link chosen: `parameter_value.load_id` (indexed) plus `content_hash` and `rollback_reason`, added by this story's migration (pack option A); assumption A-18; Physical Schema update requested; approve and rollback by `loadId` in field matrix, transitions and tests | SPEC-002, 013-015; §7.3; §8; §12.3; TC-07, 10, 16-20; `shared-updates.md` §4 |
| 105 | Medium | All 11 OI-E1-042 items are in the Clarification Log (CLAR-001..011) with status, plus CLAR-012..023; all kept OPEN per triage decision (e) (OI-002 and OI-009 marked "settled for this spec" with the evidence, not closed); each has a row in `shared-updates.md` §1; status line `OPEN_ITEMS_RECORDED [OPEN_ITEMS: 23] [BLOCKING: 0]` | §19; §20; `shared-updates.md` §1 |
| 106 | Medium | Idempotency key `(PARAMETER, validFrom, content_hash)`, hash stored in `content_hash`, canonical form defined; identical repeat returns the existing load (`repeat = true`, endpoint 201 same body); conflict 409 MSG-P3-027; rollback `reason` required, max 400, 422 MSG-GEN-001; `changeRequestRef`, `impactSummary`, `rollbackPlan` deferred to RWB-E2-041; contract deltas listed | SPEC-013, 015; §7.4; §11.3; §12.6 |
| 107 | Medium | `CatalogCompletenessCheck` exempts `scope=PRODUCT` (and secret / ENV rows) from the default rule only; owner, type and range still required; fixture TC-21 | SPEC-003; §7.1; TC-21 |
| 108 | Medium | Six D-RCV-36 keys fully defined (kind, type, unit, range, required, value source, default) in §12.4; owners and used-by are labelled assumptions A-07..A-10; existing `rwb.*` literals become ENV-sourced catalog entries naming their property (readers unchanged; RWB-E1-071/072 move reads); `RwbMagicNumberCheck` starts from a reviewed baseline file of today's literals with a ratchet, so the first build is neither red nor silently exempt | SPEC-004, 024; §12.4; §12.11; TC-25, TC-26 |
| 109 | Medium | `MessageResolver` seam with interim `FixedMessageCatalog`; EN and TH from Error and Message Standard v4, Thai "Proposed" (DL10); MSG-P4-001 added; missing message table = OI-E1-042-004 | SPEC-022; §10; TC-30 |
| 110 | Medium | Seed: author = synthetic system identity, approver NULL, APPROVED baseline approved by the reviewed catalog PR (A-05), `valid_from = 2026-11-02` (A-04). Readiness ignores `valid_from` (triage decision (f)): DOWN only when a required key has no APPROVED row at all and no default (TABLE), or its property is unresolved (ENV). Reads before `valid_from` fall back to the default (versionNo 0). Business date for loads from `BusinessDateProvider` | SPEC-006, 007, 016, 023; §12.9; TC-04, TC-13 |
| 111 | Medium | SPEC catalogue §5 defines SPEC-RWB-E1-042-001..027 once each with statement, source and tests; all references in §6, §15 and §19 use those IDs | §5 |
| 112 | Low | Follows v6 (`id uuid` PK, `uk_parameter_catalog`, `uk_parameter_value`); FK, checks and indexes listed as this story's additions; Physical Schema update requested | SPEC-002; §7.2; §12.3 |
| 113 | Low | Change checklist and audit report attributed to RWB-E2-041 | §18; §7.4 |
| 114 | Low | RW-REFADM (Reference data C) and the parameter owner as approver added to the authority table | §16 |
| 115 | Low | Source requirement cites the Traceability Matrix rows (lines 33, 51) and story file v7 | Header table |
| 116 | Low | `ParameterVersionApproved` declared as a delta (producer, consumers, payload); event catalog update requested | §11.4; SPEC-018; `shared-updates.md` §4 |
| 117 | Low | `case.entry.dpd` GLOBAL, `ENTRY_DPD` RWB-E1-045 product key, other names not seeded; recorded as open item OI-E1-042-006 | CLAR-006; A-22; §12.4 |
| 118 | Low | Kept as assumption A-13 (RW-COE owner and RW-RISK, DL01); grant loaded through RWB-E1-037; the approve capability check is on RWB-E1-043's endpoint (D-RUN-10); this story enforces author <> approver | CLAR-013; §16; §12.10 |

## 2. Coordinator course correction (D-RUN-10, D-RUN-11)

| Instruction | Reflected in spec.md |
|---|---|
| RWB-E1-043 owns the shared reference-load endpoint and dispatches by table code | §4.3 first seam row; §11.2; §18 out of scope; CLAR-010, CLAR-022; document gap E1042-SP-DG-08 (G-R05, Blocker = No) |
| RWB-E1-042 publishes a module interface in its api package that validates and applies a PARAMETER load, including approve and rollback | `ParameterLoadHandler` (load, approve, rollback, find) and `ParameterLoadResult` in `th.co.scb.ace.demo.recovery.platform.api` (SPEC-017, SPEC-026, §12.1, §12.2). All checks, versioning, maker-checker, idempotency and refusals live behind it (SPEC-012..015) and are thrown as `ApiProblemException`, so RWB-E1-043 renders them unchanged (§10.2) |
| E1-043's PARAMETER branch calls that interface | §4.3; §11.2 maps each API v4 operation to a method; D-RUN-11 handler map may wrap it |
| Until E1-043 merges, nothing exposes the endpoint: a seam under D-RUN-08 | §3 item 4; §4.1 trigger row; §11.2 last paragraph; tests at interface level in a Spring context (§15 "System (interface)"); HTTP tests handed to RWB-E1-043 (`shared-updates.md` §1) |
| Consequences | API scope narrowed to `GET /admin/parameters` (§2, §11.1); load/approve/rollback capability checks (C, A, U) move to RWB-E1-043 (§12.10, §16); flag off = no `ParameterLoadHandler` bean (SPEC-021); FL5, CON2, CON3 coverage rows updated (§6) |

## 3. Plan inputs (acknowledged; no spec finding)

| # | Plan input | Acknowledgement in spec revision 3 |
|---|---|---|
| 1 | Migration folder and lint regex | SPEC-001 names `backend/src/main/resources/db/modulemigration/recovery/` and the lint; no `V0042` |
| 2 | Placeholder from `rwb.schema` in `RecoveryFlywayConfig` | SPEC-001; CLAR-009 (settled for this spec, register item kept open) |
| 3 | Local schema built from Physical Schema v6 | Guarded DDL; TC-13 (empty) and TC-14 (v6 schema) |
| 4 | Testcontainers tests tagged `recovery-it` instead of the pack's shell script | §15 levels; TC-13, TC-14 |
| 5 | Package `th.co.scb.ace.demo.recovery.<module>` | SPEC-026, §12.1, A-01, CLAR-020 |
| 6 | Build checks as Gradle tasks / unit tests; catalog file absent | §12.11; A-25, A-26 |
| 7 | Flag in the `RecoveryFlags` / `RecoveryProperties.P3` pattern | SPEC-021, §12.12 (two-argument constructor kept for `DroolsRuleEngineTest`) |
| 8 | Method checks by capability are later work | `CapabilityCheck` seam (SPEC-020); TC-12 Blocked |
| 9 | RFC 7807 through `ProblemFactory` / `ApiExceptionHandler` | SPEC-025, §10.2 (additive constructor) |
| 10 | Readiness group | SPEC-016, §12.9 |
| 11 | Outbox `case_seq` nullability | §4.3 outbox row; `shared-updates.md` §1 |
| 12 | Coverage verification not in `check` | §14: the plan adds `recoveryCoverageVerification` to `check` |
| 13 | Gradle `JAVA_TOOL_OPTIONS` on this workstation | Plan/build concern; noted in `agent-run-log.md` |
| 14 | OpenAPI already has all operations; no regeneration | §2, §11.3, §13 |

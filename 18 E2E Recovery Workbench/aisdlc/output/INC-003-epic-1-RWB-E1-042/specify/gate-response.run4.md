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

# Round 2: REVIEW-RWB-E1-042-SPEC-004

RUN_ID `INC-003-epic-1-RWB-E1-042`, stage `specify`, 2026-11-18 (remediation run 2). Responds to
`review/spec-gate-review-2.md` (0 Critical, 0 High, 1 Medium, 9 Low; findings 119-128; plan inputs P1-P6)
and to the orchestrator triage of 2026-11-18T00:09:40+07:00. All references are to `specify/spec.md`
revision 4 unless stated. Revision 3 of every changed file is kept as `<name>.run2.md`.

## R2.1 Findings

| Finding | Severity | Resolution in revision 4 | Where |
|---|---|---|---|
| 119 | Medium | Flag-off contract stated from this side. With `rwb.p3.configservice` off no `ParameterLoadHandler` bean is registered and no bean of this story depends on it, so the context starts. RWB-E1-043 obtains the handler through `ObjectProvider` and refuses the PARAMETER code with 404 MSG-P4-003, "as if the operation were absent" (E43S SPEC-RWB-E1-043-018 and -026; its test TC-PB-01). That is the defined refusal under D-RUN-11 and the D-RCV-36 flag rule; RWB-E1-043's spec governs it (A-28). Story §14 lists no message for "value loads are refused", and the wording of MSG-P4-003 is case-oriented: gap E1042-SP-DG-10, Blocker = No | SPEC-021; §4.3 first seam row; §9 E10; §10.3; §11.2; §12.12; TC-22; CLAR-021; A-28 |
| 120 | Low | `CapabilityCheck.require(...)` throws `ApiProblemException(ApiError.NOT_PERMITTED, Map.of("action", action), null)` so the 403 carries MSG-P4-002 and the action text; `has(...)` returns a boolean with no side effect | SPEC-020; §12.2; §12.10; TC-24; A-31 |
| 121 | Low | One metadata source: the generated `ParameterKeys` holds every metadata column, including the default, and publishes `all()` and `byName(String, Class<T>)`; `parameter_catalog` is a database mirror written by the migration; SPEC-007 reads the default from the key. Drift check TC-27 compares the mirror with `ParameterKeys.all()` after all migrations, with a negative fixture | SPEC-005; SPEC-007; §7.5; §12.2; §12.3; TC-04; TC-27; A-29, A-30 |
| 122 | Low | Precondition PRE-6: RWB-E1-044's identifier-only, quote-aware lint (D-RUN-13, E44S SPEC-RWB-E1-044-007, its test T-044-21) is merged before this story. The seed values are not changed to satisfy today's lint | §4.2 PRE-6; SPEC-001; §2; TC-15 |
| 123 | Low | Readiness uses the value in force on the business date, else the generated default. Every seeded key has a default, so a future seeded `valid_from` cannot make readiness DOWN. Source: the orchestrator's triage item (f), logged as "Gate triage (late record)" in `AI-SDLC-BUILD-LOG.md` timeline line 140 | SPEC-016; §12.9; TC-32; A-04 |
| 124 | Low | §14: 80% on LINE, INSTRUCTION, BRANCH and METHOD (E44S SPEC-RWB-E1-044-014); `recoveryCoverageVerification` stays **outside** `check` (D-RCV-40, `INC-001-decisions.md` line 87); it reads `test` execution data only. The README note that says otherwise is recorded as gap E1042-SP-DG-13 | §14; S-24; §R2.3 below |
| 125 | Low | The approval transaction runs the row lock, the checks, the status change, the `valid_to` recomputation and `VersionDecisionRecorder.recorded(...)`, in that order, before commit. Recorders join the transaction (`Propagation.MANDATORY`) and throw on failure; a failure rolls everything back and no event is published (`AFTER_COMMIT` listener) | SPEC-014; SPEC-019; §12.7; §9 E11; TC-29; A-32 |
| 126 | Low | MSG-GEN-006 is no longer used: its Standard v4 text says the request "will be retried", which is untrue for a synchronous read. No message in the Standard fits, so the 503 is a status-only Problem (type `urn:rwb:problem:unavailable`, no `messageCode`); message owner to decide (CLAR-019). Gap E1042-SP-DG-11 | SPEC-025; §9 E7; §10.2; §10.3; TC-34; A-15 |
| 127 | Low | Settled: this story does not provide the column definitions. RWB-E1-043 v7 line 298 has the reference data administrator load them, and E43S SPEC-RWB-E1-043-003 and -029 add the `refdata.columns.<code>` keys, their grammar and the row check. Values come from each table's owner story (RWB-E1-038, RWB-E1-019, RWB-E1-045, RWB-E1-025, RWB-E1-046). Line 303 conflicts with line 298: gap E1042-SP-DG-12 | CLAR-022; §18; `shared-updates.md` §1 |
| 128 | Low | The four required headings now use the exact text (`## Change Scope Declaration`, `## Requirement-to-SPEC Logic Coverage`, `## Unit Test Applicability`, `## Clarification Log`), each followed by "Section N." so the section numbering still reads | §2, §6, §14, §19 headings |

## R2.2 Plan inputs P1-P6 (acknowledged)

| # | Plan input | Acknowledgement in revision 4 |
|---|---|---|
| P1 | Protocol literals and the magic-number baseline | §12.11: statuses through `HttpStatus` constants; 400 (reason length) and 64 (hash length) as named constants added to the reviewed baseline in the same PR |
| P2 | ENV rows read through `Environment` | SPEC-024; §12.2 |
| P3 | Concurrent identical loads | SPEC-013: the unique violation is caught, the load re-read and returned with `repeat = true`, else 409 MSG-GEN-004; never a 500; §9 E12; TC-33 |
| P4 | Access-log seam | §4.3 seam row: RWB-E1-039 (Build Sequence order 28) owns the access log; nothing is built here; §17, §18 |
| P5 | Interface tests at the same assertion depth as the HTTP tests | §15 note: each interface test asserts status, `messageCode`, field and the rows written, as the HTTP test would |
| P6 | METHOD and INSTRUCTION counters, outside `check` | §14 (finding 124) |

## R2.3 Correction to Round 1

The Round 1 table §3, plan input 12 ("the plan adds `recoveryCoverageVerification` to `check`") is withdrawn.
The gate (`spec-gate-review-2.md` §2) showed that the later Active decision D-RCV-40 keeps the task outside
`check`; revision 4 §14 follows D-RCV-40.

## R2.4 Orchestrator triage (attributed to the orchestrator, Claude Code)

The triage below was given by the orchestrator (Claude Code), not by a human. It is logged in
`AI-SDLC-BUILD-LOG.md` timeline lines 140 ("Gate triage (late record)", item (f)) and 141 ("Gate triage",
REMEDIATE).

| Triage item | How revision 4 applies it |
|---|---|
| 119: flag off, handler not registered; RWB-E1-043's registry refuses PARAMETER with a defined message (D-RUN-11); contract and test from this side, with the message ID or a gap | SPEC-021, TC-22; 404 MSG-P4-003 cited from E43S; gap E1042-SP-DG-10 |
| 123: cite the "Gate triage (late record)" entry | SPEC-016 and A-04 cite timeline line 140 |
| 124: coverage verification outside `check` (D-RCV-40); correct §14 and plan input 12 | §14; R2.3 |
| 121: one place for the default, or a drift check with a test | Both: generated keys are the source; TC-27 checks the mirror |
| 125: recorder tied to the approval transaction | SPEC-014, §12.7, TC-29 |
| 126: MSG-GEN-006 must not promise a retry; source wording or a gap | Status-only 503; gap E1042-SP-DG-11 |
| 127: settle with citations whether this story provides the column definitions, else name the owner | Not provided here; owners named in CLAR-022; gap E1042-SP-DG-12 |
| Every other Low fixed or answered with evidence (D-RUN-09) | 120, 122 and 128 fixed (R2.1) |

## R2.5 Requests from RWB-E1-043's spec

E43S `shared-updates.md` line 70 asks RWB-E1-042 for (a) to (d). Answers are in this stage's
`shared-updates.md` §4: (a) the revision 3 names are kept; (b) `byName` added; (c) repeat approve and
rollback not aligned, left to the owner under E43S GAP-35; (d) noted.

# Round 3: REVIEW-RWB-E1-042-SPEC-005

RUN_ID `INC-003-epic-1-RWB-E1-042`, stage `specify`, 2026-11-18 (remediation run 3). Responds to
`review/spec-gate-review-3.md` (0 Critical, 1 High, 0 Medium, 5 Low; findings 129-134; plan inputs 1-4; gap
candidates E1042-RV3-DG-01 to -03) under the orchestrator's triage (R3.4). All references are to
`specify/spec.md` revision 5 unless stated. Revision 4 of every changed file is kept as `<name>.run3.md`.

## R3.1 Findings

| # | Severity | Finding (short) | Resolution | Where |
|---|---|---|---|---|
| 129 | High | Module placement contradicts RWB-TE-001 | Rebased on TE1S v4 and SU-08: implementation in P3 `casewf.config`, published types in `casewf.config.api` (`@NamedInterface(name = "config.api", propagate = false)`, `casewf` map entry added in the same MR); `MessageResolver` and `CapabilityCheck` in P4 `access.api` with `access.internal` implementations; flag by `@ConditionalOnProperty`, no `RecoveryFlags` / property-record change and no `/platform/info` field; `ApiProblemException` constructor through `access.api`; grants file under `access/`; every class named at its TE1S home; PRE-7 added; A-01 replaced; CLAR-020 resolved. `ParameterLoadHandler` location published under D-RUN-10 is now `th.co.scb.ace.demo.recovery.casewf.config.api.ParameterLoadHandler`; `shared-updates.md` §1 tells RWB-E1-043 to import it (and `ParameterLoadResult`, `ParameterKeys`, `BusinessDateProvider`) from there and `CapabilityCheck` from `access.api` | §2, §4.2 PRE-7, §4.3, SPEC-017, -020, -021, -022, -026, §11.3, §11.4, §12.1, §12.2, §12.10-§12.12, TC-22, TC-24, TC-45; A-01, A-33, A-34; E1042-SP-DG-14, -16; CLAR-020, -025 |
| 130 | Low | `usedBy` split on comma breaks seeded values | `used_by` is `;`-separated (no seeded value contains `;`; several contain `,`); entry rules; pack comma lists rewritten; exact values and expected arrays listed; TC-41 runs on the real catalog rows plus negative fixtures | §7.1, §7.5, §12.4, SPEC-003, TC-41, A-35 |
| 131 | Low | Coverage leaves out build-check and generator code | Check logic moved to test-scope `architecture.parameters`, in the TOOLING class set measured by `recoveryToolingCoverageVerification` at 0.80 on four counters (E44S SPEC-014, D-RCV-43 (2)); unit tests TC-41, -43, -44. Generator: recorded exception (build-script code, outside both class sets, not measurable from `test` data; D-RCV-40 scope), output verified by TC-42 against the parsed catalog, plus TC-26, -27 | §12.11, §14, SPEC-005, TC-42, A-38 |
| 132 | Low | Recorder failure should be 503 MSG-P7-003 | Any recorder `RuntimeException` becomes `ApiProblemException` 503 MSG-P7-003 with cause, inside the transaction; API v4 approve 503 `E503` (lines 6028-6029) and Standard v4 line 208 followed; no higher-precedence source says otherwise. The MSG-GEN-006 alternative is recorded with both citations in E1042-SP-DG-11, Blocker = No | SPEC-014, -019, -025, §8, E11, §10.2, §10.3, §12.7, TC-29 (b), A-36 |
| 133 | Low | Refusal paths without a test | TC-35 (unknown loadId on approve and rollback, incl. a seeded row id), TC-36 (approve after validFrom passed), TC-37 (rollback of VALIDATED / ROLLED_BACK), TC-38 (approve of APPROVED / ROLLED_BACK), TC-39 (reason 400 / 401), TC-40 (`find` hit and miss) | §15; SPEC-014, -015, -017 test columns; §14 |
| 134 | Low | Run log title stale; gate section missing | Title now covers revisions 3-5; "Gate (run 2)" present; run 3 and "Gate (run 3)" sections appended | `agent-run-log.md` |

## R3.2 Plan inputs 1-4 (carried into the spec as "Plan inputs")

Spec §12.14 holds the four inputs with where each is applied and its test: (1) `load`, `approve`, `rollback`
in their own `REQUIRES_NEW` transactions, catch-and-re-read outside the failed transaction (SPEC-013, -017,
§12.7, A-39; RWB-E1-043 told); (2) ENV rows may not name a credential-bearing property (SPEC-003, §7.1,
TC-44); (3) rollback cache rebuild after commit, other instances by TTL (SPEC-015, §12.8, TC-10); (4) the
`ApiExceptionHandler.problem` message-ID branch in `access.internal` (§10.2, TC-30).

## R3.3 Reviewer gap candidates

| Candidate | Two citations | Disposition |
|---|---|---|
| E1042-RV3-DG-01 (503 message on recorder failure) | Standard v4 lines 73, 208; API v4 `E503` lines 6028-6029 | Kept, merged into E1042-SP-DG-11 (extended), Blocker = No |
| E1042-RV3-DG-02 (story package vs baseline module) | Story v7 RWB-E1-042 line 237; RUN-BRIEF / phase0 A-01 baseline; settled by TE1S SPEC-022 and SU-08 | Kept as E1042-SP-DG-14, Blocker = No |
| E1042-RV3-DG-03 (author / approver personal flag) | Personal Data Inventory v4 lines 676-677 (personal "Yes"); Physical Schema v6 lines 4345-4346 (`is_personal` false) | Kept as E1042-SP-DG-15, Blocker = No; protective reading applied (SPEC-027, CLAR-024, A-37) |

One gap added by this stage: E1042-SP-DG-16 (AGENTS one-module rule vs the P4 additions of SU-08 (c), (d)),
Blocker = No (CLAR-025).

## R3.4 Orchestrator triage (attributed to the orchestrator, Claude Code)

The triage below was given by the orchestrator (Claude Code), not by a human.

| Triage item | How revision 5 applies it |
|---|---|
| 129: rebase onto RWB-TE-001's module homes (TE1S v4, SU-08, stable); code in `recovery.casewf.config` and `.api`; `MessageResolver` and `CapabilityCheck` where TE-001 places them; update every path, package and the `ParameterLoadHandler` location published under D-RUN-10; tell RWB-E1-043 to import from the new package | R3.1 row 129; `shared-updates.md` §1 (rev 5) import row |
| 130: a delimiter seeded values cannot contain, tested against the real seed rows | `;`; TC-41 on the real catalog |
| 131: bring build-check and generator code under the coverage gate, or record why D-RCV-40 excludes it | Check logic under the TOOLING gate; generator exception recorded with its reason (A-38) |
| 132: conform to API v4 (503 MSG-P7-003) unless a higher source says otherwise; record any MSG-GEN-006 conflict in SP-DG-11 with both citations, Blocker = No | Done; none higher found |
| RV3-DG-01..03: keep each only with two citations; author / approver personal under the protective reading unless Inventory v4 says otherwise | All three kept with two citations; Inventory v4 says personal "Yes", so the protective reading stands |
| Review plan inputs 1-4 carried into the spec as "Plan inputs" | §12.14 |
| 133, 134 fixed; re-gate as `review/spec-gate-review-4.md` | R3.1; gate in `agent-run-log.md` "Gate (run 3)" |

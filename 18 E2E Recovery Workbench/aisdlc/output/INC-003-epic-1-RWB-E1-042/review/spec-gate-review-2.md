# Spec gate review 2: RWB-E1-042 (RUN_ID `INC-003-epic-1-RWB-E1-042`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-042-SPEC-004` |
| Gate | Specification gate, re-review of revision 3 |
| Artifacts under review | `specify/spec.md` revision 3 (799 lines), `compliance-validation.md`, `assumptions.md` (A-01 to A-27), `document-gaps.md` (E1042-SP-DG-01 to -09), `shared-updates.md`, `gate-response.md` |
| Compared with | `review/spec-gate-review.md` (`REVIEW-RWB-E1-042-SPEC-003`, findings 101-118, plan inputs 1-14) and `review/document-gaps.md` (E1042-RV-DG-01 to -15) |
| Baseline | Document set v14: User Stories Epic 1 Story Files v7 (RWB-E1-042, RWB-E1-043, RWB-E1-044), API Specification v4 (`api/recovery-api-v4.yaml`), Physical Schema v6, Error and Message Standard v4, Users, Roles and Permissions v4, ADR v3, Decision Log v10, D-RCV-35, D-RCV-36; run decisions D-RUN-07 to D-RUN-13 (`AI-SDLC-BUILD-LOG.md`); squad decisions `aisdlc/docs/decisions/INC-001-decisions.md` (D-RCV-38 to D-RCV-49) |
| Repository | `<repo>` working tree as read on 2026-11-18 (backend code, `build.gradle.kts`, `RecoveryMigrationLintTest.java`, `application.yaml`, `infra/postgres/init/20-grants.sql.inc`) |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18 |
| Supersedes | `REVIEW-RWB-E1-042-SPEC-003` for revision 3. That review stays as history. |

## Status

**`SPEC_GATE: FAIL`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 1 | Blocks the handoff to the Implementation Planner |
| Low | 9 | Visible; human disposition required (D-RUN-09: the specifier fixes Lows too) |

Revision 3 is a real revision, not a relabelling. All 18 earlier findings are resolved in the text and
the resolutions hold against story v7, API v4, Physical Schema v6 and the code. The migration design,
the seam table, the load link, the SPEC catalogue and the AC coverage are now sound.

One new Medium remains. The cross-story interface `ParameterLoadHandler` disappears when the feature
flag is off, and the flag is off by default outside local. The spec does not define what RWB-E1-043
gets in that state, so a required bean can fail application start. The nine Lows are smaller
contract gaps. Two of them (122 and 124) come from repository facts that the earlier review got wrong
or did not check.

## 1. Earlier findings (101-118): verification

Each row was checked in the revised text and against the source, not taken from `gate-response.md`.

| Finding | Severity | Verdict | Evidence checked |
|---|---|---|---|
| 101 | High | RESOLVED | SPEC-001 (spec line 136): one file `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql`, line 1 `-- Story: RWB-E1-042`, `${recoverySchema}` only, no `SET search_path`, no GRANT, guarded DDL. No `V0042`, `RWB_SCHEMA` or `${schema}` remains (grep). Matches D-RCV-28 (Decision Log v10), D-RUN-07 and `RecoveryMigrationLintTest.java:25, 82-84, 94-95`. No GRANT is correct: `infra/postgres/init/20-grants.sql.inc` gives `recovery_svc` DML on `rwb_migrator` objects through default privileges. See finding 122 for the lint itself |
| 102 | High | RESOLVED | §6 has rows AC1-AC11 including AC2 and AC3 (story v7 §7 lines 85-150); TC-02 and TC-03 are System level on fixture modules (story §13 build step 7); counts 11 ACs and 57 rows agree with §20 |
| 103 | High | RESOLVED | §4.3 seam table names owner, build order and what this story builds for each later dependency. D-RUN-08 and D-RUN-10 applied: no controller for loads, `ParameterLoadHandler` published instead. TC-12 `Blocked` with exit criterion (OI-E1-042-001). One gap remains in how the seam behaves with the flag off (new finding 119) and the access log seam is missing (plan input P4) |
| 104 | High | RESOLVED | `parameter_value.load_id` (indexed), `content_hash`, `rollback_reason` added by this story's guarded migration (§12.3, SPEC-002); option A of the E1-042 Clarification Pack §3.7; A-18; Physical Schema v6 update requested in `shared-updates.md` §4. Approve and rollback by `loadId` in §7.3, §8 and TC-07, TC-10, TC-16 to TC-20 |
| 105 | Medium | RESOLVED | CLAR-001 to CLAR-011 carry all 11 OI-E1-042 items; CLAR-012 to CLAR-023 added; all OPEN; `shared-updates.md` §1 has one row each; status line `OPEN_ITEMS_RECORDED [OPEN_ITEMS: 23] [BLOCKING: 0]` |
| 106 | Medium | RESOLVED | SPEC-013 and SPEC-015, §7.4, §11.3, §12.6: idempotency key `(PARAMETER, validFrom, content_hash)` with canonical form; repeat returns the existing load; conflict 409 MSG-P3-027 (Error and Message Standard v4 line 151, `{table} {check}`); rollback reason required, max 400, 422 MSG-GEN-001; RollbackRequest in API v4 (line 9818) matches |
| 107 | Medium | RESOLVED | SPEC-003 and §7.1 exempt `scope=PRODUCT`, secret and ENV rows from the default rule only; TC-21 fixture. Consistent with RWB-E1-045 v7 BR2 |
| 108 | Medium | RESOLVED | §12.4 defines the six D-RCV-36 keys fully; owners A-07 to A-10; existing `rwb.*` literals become ENV rows naming the property (SPEC-024; properties exist in `application.yaml` lines 75-97); `RwbMagicNumberCheck` starts from a reviewed baseline (§12.11). The baseline list matches today's code (ApiError 401/403/404/503; DroolsRuleEngine 16, 0.75f; PdpaPayloadCodec 12, 128, 16, 24, 32; PlatformSmokeWorkflow 5, 3; TemporalAdminController `Duration.ofMinutes(1)`). See plan input P1 for this story's own literals |
| 109 | Medium | RESOLVED | SPEC-022, §10: `MessageResolver` with `FixedMessageCatalog`; EN and TH taken from Error and Message Standard v4 (Thai "Proposed" status noted, line 19); MSG-P4-001 added; missing message table recorded (OI-E1-042-004). See finding 126 for one message choice |
| 110 | Medium | RESOLVED (with new Low 123) | Seed author synthetic, approver NULL, A-05; `valid_from = 2026-11-02` (A-04); business date from `BusinessDateProvider`. The readiness rule now ignores `valid_from`; that choice is a new Low (123) |
| 111 | Medium | RESOLVED | §5 defines SPEC-RWB-E1-042-001 to -027 once each; grep found no SPEC ID outside that range and no TC beyond TC-31 |
| 112 | Low | RESOLVED | Follows Physical Schema v6 (`id uuid` PK, `uk_parameter_catalog`, `uk_parameter_value`, lines 1386-1433); FK, checks and indexes listed as this story's additions |
| 113 | Low | RESOLVED | Change checklist and audit report attributed to RWB-E2-041 (§18, §7.4) |
| 114 | Low | RESOLVED | §16 lists RW-REFADM (Reference data C) and the parameter owner as approver; checked against Users, Roles and Permissions v4 matrix |
| 115 | Low | RESOLVED | Header cites the Traceability Matrix rows and story file v7 |
| 116 | Low | RESOLVED | §11.4 and SPEC-018 declare `ParameterVersionApproved` (producer, consumers, payload); event catalog update requested in `shared-updates.md` §4 |
| 117 | Low | RESOLVED | CLAR-006, A-22, §12.4: `case.entry.dpd` GLOBAL; `ENTRY_DPD` is RWB-E1-045's product key |
| 118 | Low | RESOLVED | A-13 (RW-COE owner, RW-RISK approver, DL01); approve capability check sits on RWB-E1-043's endpoint (D-RUN-10); author <> approver enforced in the interface and the DB (SPEC-014). API v4 approve text ("Reference data A ... held by no role") confirms the gap is real and recorded (CLAR-013) |

Earlier document-gap candidates E1042-RV-DG-01 to -15 are all reflected: the spec's own
`document-gaps.md` (SP-DG-01 to -09) carries the ones that still need a document owner, and the rest
are settled by the revised design (DG-01, -04, -05, -09, -11, -12, -14, -15).

## 2. Earlier plan inputs (1-14)

| # | Status | Note |
|---|---|---|
| 1-11, 13, 14 | Acknowledged correctly | As listed in `gate-response.md` §3; checked against the code named in each |
| 12 | Acknowledged, but the earlier plan input was wrong | `REVIEW-RWB-E1-042-SPEC-003` said the first story's code is meant to add `recoveryCoverageVerification` to `check` (from `README.md`). The later squad decision D-RCV-40 (`INC-001-decisions.md` line 87, Active) keeps it "outside `check`", and build log row 120 (RWB-TE-003) repeats that. This review corrects plan input 12; the spec text that followed it is finding 124 |

## 3. New findings

### REVIEW-RWB-E1-042-SPEC-004-119 (Medium): `ParameterLoadHandler` has no defined flag-off contract

- **Maps to:** SPEC-RWB-E1-042-017, -021; story v7 §13 feature flag; FL5, CON2, CON3; TC-22.
- **Evidence:** SPEC-021 (spec line 156): with `rwb.p3.configservice` off, "the `ParameterLoadHandler`
  bean is not registered, so loads cannot be applied". The flag defaults to `false` outside the local
  profile (SPEC-021; the `rwb.p3.*` pattern in `application.yaml` lines 75-77). `ParameterLoadHandler`
  is the published cross-story interface that RWB-E1-043's PARAMETER branch calls (D-RUN-10, D-RUN-11;
  RWB-E1-043 v7 §6 line 75). Story v7 §13 says that with the flag off "value loads are refused", which
  is a defined refusal, not an absent bean. The spec gives RWB-E1-043 no rule: a constructor-injected
  handler fails application start in every environment where the flag is off, and an `Optional`
  or `ObjectProvider` consumer has no specified problem, status or message to return. AGENTS §3.13 asks
  for a flag that "returns the previous code path when off"; for a load, that is a refusal.
- **Failure scenario:** RWB-E1-043 merges with a constructor-injected `ParameterLoadHandler` (or a
  handler-map entry per D-RUN-11). In DEV or SIT the flag is off, the bean is missing, and the
  service does not start; or a PARAMETER load returns an unmapped 500.
- **Fix required:** register the bean in both states and, when the flag is off, throw a defined
  `ApiProblemException` from `load`, `approve` and `rollback` (name the status and message ID, and the
  behaviour of `find`), or state the consumer contract explicitly (how RWB-E1-043 must inject it and what
  it returns). Add the rule to the `shared-updates.md` row for RWB-E1-043 and add an interface-level test
  (flag off: load refused with the named problem; context starts).

### REVIEW-RWB-E1-042-SPEC-004-120 (Low): the 403 action text "read parameters" cannot be produced as specified

- **Maps to:** SPEC-RWB-E1-042-020, -025; §12.10; TC-24.
- **Evidence:** SPEC-020 says a refusal is 403 MSG-P4-002 with action "read parameters", using
  `@PreAuthorize("@capabilityCheck.require(authentication, 'Rules and parameters', 'R', 'read parameters')")`.
  Today `ApiExceptionHandler.forbidden` returns `problems.problem(ApiError.NOT_PERMITTED, Map.of("action", "do this"))`
  and the `SecurityConfig` access-denied handler also hard-codes "do this". A `@PreAuthorize` expression
  that returns `false` raises `AccessDeniedException` and reaches that handler. The spec does not say
  whether `require(...)` returns a boolean or throws `ApiProblemException` carrying the action, nor that
  the handler changes.
- **Fix required:** state that `CapabilityCheck.require` throws `ApiProblemException(ApiError.NOT_PERMITTED, Map.of("action", ...))`
  on refusal (or that the handler reads the action from the denial), and list the handler change under
  §2 impacted nodes if needed. TC-24 asserts the action text.

### REVIEW-RWB-E1-042-SPEC-004-121 (Low): the source of a default is not single

- **Maps to:** SPEC-RWB-E1-042-005, -007, -016, -021; TC-04, TC-22.
- **Evidence:** the default appears twice: in the generated `ParameterKeys` (SPEC-005, from the catalog
  file) and in `parameter_catalog.default_value` (seeded by the migration, §7.1 line 237, §12.3 step 8).
  SPEC-021 says the flag-off path uses "catalog defaults from the generated keys". The spec does not say
  which source `ParameterService` uses with the flag on, which one `ParameterStartupCheck` reads, or what
  happens when the two differ (for example after a catalog-file change without a migration).
- **Fix required:** name one source for each reader, and add a build or startup check that the two agree
  (or state why drift cannot happen). TC-04 names the source it asserts.

### REVIEW-RWB-E1-042-SPEC-004-122 (Low): the seed fails the current migration lint; the spec says the lint is unchanged

- **Maps to:** SPEC-RWB-E1-042-001; §12.3; TC-15.
- **Evidence:** `RecoveryMigrationLintTest.java:102` rejects `(?i)(?<![\w$])(recovery|ace|public)\.[a-z_]`
  after removing only `--` comment lines, not string literals. The seed's `used_by` values are of the form
  `'recovery.casewf...'` (12 occurrences of `'recovery.` in the pack SQL `_v2-baseline/implement/sql/V0042...sql`,
  for example line 356), and §12.4 keeps module-qualified `used_by` values. TC-15 (spec line 691) expects
  the "existing `RecoveryMigrationLintTest`" to pass. D-RUN-13 (build log) decides that the schema-prefix
  lint ignores string literals and comments, and RWB-E1-044's revised spec delivers that quote-aware,
  identifier-only lint (SPEC-RWB-E1-044-007, T-044-21). RWB-E1-044 is order 1, before this story.
- **Fix required:** cite D-RUN-13 and RWB-E1-044 SPEC-007 as the precondition for TC-15 (the lint as
  RWB-E1-044 leaves it), and add a seam or precondition row. Do not change the seed values to dodge the lint.

### REVIEW-RWB-E1-042-SPEC-004-123 (Low): readiness ignores `valid_from` on an unrecorded decision

- **Maps to:** SPEC-RWB-E1-042-016; AC4, BR7, X3; TC-04.
- **Evidence:** SPEC-016 (spec line 151): readiness is UP when a required key has an `APPROVED` row with
  any `valid_from`, citing "triage decision (f)". The build log row for the RWB-E1-042 triage (row 91) lists
  no decision (f), and no D-RUN or D-RCV entry records it. Story v7 BR7 requires a value in force (or a
  default) for each required key. A required key with no default and only a future-dated approved row
  passes readiness, then `ParameterService` throws `ParameterNotInForceException` on the business date.
  The seed itself is safe (A-04: `valid_from = 2026-11-02`, before the run), so the risk is for later
  loads, not the bootstrap.
- **Fix required:** use the value in force on the business date from `BusinessDateProvider` (with the
  default as fallback), or record the deviation as a decision with its source and add a test for the
  future-dated, no-default case.

### REVIEW-RWB-E1-042-SPEC-004-124 (Low): §14 adds coverage verification to `check`, against D-RCV-40, and claims four counters

- **Maps to:** §14 Unit Test Applicability; security-quality-standards 80% gate; plan input 12.
- **Evidence:** §14 (spec line 663): "80% lines, statements, branches and functions (methods) ... measured
  by `recoveryCoverageVerification` (JaCoCo); the plan adds it to `check`". D-RCV-40 (Active squad decision,
  `INC-001-decisions.md` line 87) keeps `recoveryCoverageVerification` "outside `check`"; build log row 120
  (RWB-TE-003) repeats it. `backend/build.gradle.kts` enforces only `LINE` and `BRANCH` at 0.80, so the
  task as it is does not measure statements (`INSTRUCTION`) or functions (`METHOD`). The earlier review's
  plan input 12 led the spec here; this review corrects it (§2).
- **Fix required:** keep the task outside `check` and run it as stage evidence (D-RCV-40); state that the
  plan adds `METHOD` and `INSTRUCTION` counters at 0.80 (or record which metric is not supported and why).
  The 80% gate is otherwise planned for all four metrics, as the agent rule requires.

### REVIEW-RWB-E1-042-SPEC-004-125 (Low): the decision record write has no transaction rule

- **Maps to:** SPEC-RWB-E1-042-014, -019; AC7, BR4; AGENTS §3.4.
- **Evidence:** SPEC-014 says "one `VersionDecisionRecorder` call" on approve, and "one `ParameterVersionApproved`
  after commit". It does not say the recorder call happens inside the approval transaction, before commit,
  or that a recorder failure fails the approval. Backend standards §4.3, ADR-009 and backend-context §14.5
  require the decision record in the same transaction as the change.
- **Fix required:** state that the recorder runs inside the approval transaction and that its failure rolls
  the approval back; add the case to TC-07 or a new test with a failing recorder.

### REVIEW-RWB-E1-042-SPEC-004-126 (Low): MSG-GEN-006 is used for a read outage, but its text promises a retry

- **Maps to:** §9 E7, §10 (spec lines 338, 368, 382); CLAR-019; SPEC-025.
- **Evidence:** Error and Message Standard v4 line 73: MSG-GEN-006 says the request is "queued and will be
  retried". A failed `GET /admin/parameters` is neither queued nor retried, so the user is told something
  false. CLAR-019 records the ID as undecided but defaults to this one.
- **Fix required:** choose a message whose text fits a failed read (or keep MSG-GEN-006 and record a
  document gap with the wording conflict), and keep CLAR-019 open with the message owner.

### REVIEW-RWB-E1-042-SPEC-004-127 (Low): RWB-E1-043's column-definition dependency on this catalog is not answered

- **Maps to:** CLAR-022; §4.3; §18 out of scope.
- **Evidence:** RWB-E1-043 v7 line 303 says to "build the column definitions per reference table code ...
  from the parameter catalog of RWB-E1-042". RWB-E1-043 v7 line 298 says the column definitions are loaded
  by the reference data administrator. CLAR-022 (spec line 777) answers only line 41 (the list of table
  codes). The RWB-E1-042 spec neither provides column definitions nor says it does not.
- **Fix required:** extend CLAR-022 (or add a CLAR) to cover the column definitions: state that this
  catalog does not hold them, cite RWB-E1-043 line 298 versus line 303 as a document gap, and add the row
  for RWB-E1-043 in `shared-updates.md`.

### REVIEW-RWB-E1-042-SPEC-004-128 (Low): required section headings are not exact

- **Maps to:** specification-execution-gates (required headings).
- **Evidence:** the gates require `## Change Scope Declaration`, `## Requirement-to-SPEC Logic Coverage` and
  `## Unit Test Applicability`. The spec has `## 2. Change Scope Declaration`, `## 6. Requirement-to-SPEC Logic Coverage`
  and `## 14. Unit Test Applicability`. A heading check that matches the exact text fails. The RWB-E1-044
  spec gate raised the same point (S10).
- **Fix required:** use the exact headings (keep the numbering in the text below, or drop it).

## 4. Plan inputs (not findings)

| # | Input for the Implementation Planner |
|---|---|
| P1 | The magic-number baseline (§12.11) lists today's literals. This story adds protocol literals (409, 422, 400, max reason length 400, hash length 64). Put them in `ApiError` / named constants or in the reviewed baseline in the same PR, so the ratchet does not fail on the story's own code |
| P2 | ENV catalog rows (SPEC-024) read properties that other modules bind (`rwb.temporal.*`, `rwb.drools.*`). Read them through `Environment`, not by importing another module's properties class (AGENTS §3.11, BND-3) |
| P3 | Two concurrent identical loads both pass the idempotency check and one hits `uk_parameter_value` (or the `content_hash` index). Map the unique violation to the repeat result or to 409 MSG-GEN-004; do not let it surface as a 500 |
| P4 | The access-log seam (RWB-E1-039) is not in §4.3. If `GET /admin/parameters` must be logged as a read of configuration, add the seam row; if not, say so |
| P5 | HTTP tests for load, approve and rollback are handed to RWB-E1-043 (`shared-updates.md` §1). Keep the interface-level tests in this story at the same assertion depth |
| P6 | JaCoCo: add `METHOD` and `INSTRUCTION` counters to `recoveryCoverageVerification` and run it as evidence outside `check` (finding 124, D-RCV-40) |

## 5. Checks performed

| Check | Result |
|---|---|
| Earlier findings 101-118 resolved in text and against sources | 18 of 18 resolved (§1) |
| Required sections present (Change Scope, Requirement-to-SPEC coverage, Unit Test Applicability) | Present; headings not exact (128) |
| Every AC and BR of story v7 mapped to a SPEC ID and a test | Yes: AC1-AC11, BR1-BR7, X1-X9, FL, CON rows (57); TC-12 Blocked with exit criterion |
| SPEC IDs unique and in range | 001-027 only; no orphan TC beyond TC-31 |
| 80% unit-test gate for lines, statements, branches and functions | Planned in §14; enforcement mismatch and `check` wiring conflict (124) |
| Migration rules (D-RCV-28, D-RUN-07, D-RUN-12) | One file, placeholder name, one creator per table, guarded DDL; lint dependency (122) |
| Run decisions D-RUN-08, D-RUN-10, D-RUN-11 | Seams and published interface in place; flag-off contract missing (119) |
| API v4 alignment | GET operation and the load, approve and rollback operations map to methods; schemas ReferenceLoad, Problem, RollbackRequest, Parameter agree |
| Physical Schema v6 alignment | Tables, constraints and LOVs (LOV-VERSION-STATUS, LOV-REF-TABLE PARAMETER) agree; additions listed |
| Messages exist in Error and Message Standard v4 | All IDs exist; one wording mismatch (126) |
| Roles and rights against Users, Roles and Permissions v4 | Agree; Reference data A gap recorded (CLAR-013) |
| Security: method check, no personal data, no credentials | Method check specified (120 on the action text); DF-REF-147 to -158 are not personal; secrets not seeded |
| Module boundaries and package | `th.co.scb.ace.demo.recovery.platform.api` / `internal`; no other module's tables read |
| Database grants | No GRANT needed; default privileges in `20-grants.sql.inc` cover new tables |

## 6. Document-gap candidates (for `aisdlc/DOCUMENT-GAPS.md`; the orchestrator numbers them)

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why (blocker or not) | How this stage proceeded |
|---|---|---|---|---|---|---|
| E1042-RV2-DG-01 | User Stories Epic 1 Story Files v7, RWB-E1-043 §13 (line 303): column definitions per table code come "from the parameter catalog of RWB-E1-042" | RWB-E1-042 v7 defines no column definitions in its catalog; RWB-E1-043's own line 298 says the reference data administrator loads them | RWB-E1-043 v7 line 298; RWB-E1-042 v7 §12-§13 (no column-definition field) | No | Line 298 and RWB-E1-042's contract agree that this catalog does not hold them | Finding 127 asks the spec to say so and route the row to RWB-E1-043 |
| E1042-RV2-DG-02 | Error and Message Standard v4, MSG-GEN-006 (line 73) | The only "dependency unavailable" message promises the request is queued and retried; no message fits a failed synchronous read | E1-042 Clarification Pack §3.6 (503 message ID undecided), spec CLAR-019 | No | A message choice or a new message ID from the message owner settles it | Finding 126 |
| E1042-RV2-DG-03 | `<repo>/README.md`, coverage note ("not yet part of check. Add it once the first story's code lands") | The README contradicts the Active squad decision D-RCV-40 ("outside `check`") | `aisdlc/docs/decisions/INC-001-decisions.md` line 87; build log row 120 | No | D-RCV-40 is the later decision | Finding 124; README owner to align the note |

## Gate decision

```text
SPEC_GATE: FAIL
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 1] [LOW: 9]
BLOCKING: YES (Medium 119 blocks the handoff to the Implementation Planner)
NEXT_STEP: Technical Specifier fixes 119-128 (D-RUN-09: Lows too) in spec revision 4, then this gate re-runs (spec-gate-review-3.md).
```

If the Medium is fixed and only Lows remain at the next round, the result stays FAIL with:
`REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.`

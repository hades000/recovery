# Spec gate review 3: RWB-E1-042 (RUN_ID `INC-003-epic-1-RWB-E1-042`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-042-SPEC-005` |
| Gate | Specification gate, re-review of revision 4 (round 3) |
| Artifacts under review | `specify/spec.md` revision 4 (911 lines), `assumptions.md` (A-01 to A-32), `document-gaps.md` (E1042-SP-DG-01 to -13), `shared-updates.md`, `compliance-validation.md`, `gate-response.md` (Rounds 1 and 2), `agent-run-log.md` |
| Compared with | `review/spec-gate-review-2.md` (`REVIEW-RWB-E1-042-SPEC-004`, findings 119-128, plan inputs P1-P6, gaps E1042-RV2-DG-01 to -03); revision 3 snapshots `specify/*.run2.md` |
| Baseline | Document set v14: User Stories Epic 1 Story Files v7 (RWB-E1-042 v1, RWB-E1-043 v2), Build Sequence v6, API Specification v4 (`api/recovery-api-v4.yaml`), Physical Schema v6, Error and Message Standard v4, Decision Log v10, D-RCV-35, D-RCV-36; run decisions D-RUN-07 to D-RUN-13 (`AI-SDLC-BUILD-LOG.md` lines 30-36); squad decisions `aisdlc/docs/decisions/INC-001-decisions.md` (D-RCV-40, D-RCV-42, D-RCV-43) |
| Cross-story specs read | RWB-TE-001 spec v4 and `shared-updates.md` (INC-002, build order 2); RWB-E1-044 spec v14-3 (INC-001, order 1, "E44S"); RWB-E1-043 spec revision 2 and `review/spec-gate-review-2.md` (INC-008, order 8, "E43S") |
| Repository | `<repo>` working tree as read on 2026-11-18: `backend/build.gradle.kts`, `ApiError`, `ApiProblemException`, `ApiExceptionHandler`, `ProblemFactory`, `SecurityConfig`, `application.yaml`; pack `_v2-baseline/implement/` (catalog CSV, `V0042` SQL) |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18 |
| Supersedes | `REVIEW-RWB-E1-042-SPEC-004` for revision 4. That review stays as history. |

## Status

**`SPEC_GATE: FAIL`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 1 | Blocks the handoff to the Implementation Planner |
| Medium | 0 | |
| Low | 5 | Visible; human disposition required (D-RUN-09: the specifier fixes Lows too) |

Revision 4 resolves all ten round-2 findings. The flag-off contract, the `require` path, the single
metadata source, readiness, the four coverage counters, the recorder transaction and the 503 wording
each hold against the code, E43S and E44S. The exact headings are present.

One new High. The spec places every type in the baseline `platform` module and extends
`RecoveryFlags`, `RecoveryProperties`, `ApiError`, `ProblemFactory` and `ApiExceptionHandler` where
they are today. RWB-TE-001 (Build Sequence v6 order 2) merges before this story (order 3). Its spec
removes `platform`, moves those classes to other modules, and fails any package outside its module
map. Its `shared-updates.md` SU-08 addresses this run by name and gives the target homes. Revision 4
does not cite the RWB-TE-001 spec and keeps the premise (A-01, CLAR-020) that SU-08 (e) shows to be
false. As written, the planned code would not build on the branch it merges into.

The five Lows are a parsing rule that breaks seeded data, a coverage gap on test-scope tooling, an
unmapped recorder failure, refusal paths with no test, and housekeeping.

## 1. Earlier findings (119-128): verification

Each row was checked in the revised text and against the source, not taken from `gate-response.md`.

| Finding | Severity | Verdict | Evidence checked |
|---|---|---|---|
| 119 Flag-off contract | Medium | **Resolved** | SPEC-021, §12.12 bean table, §4.3 first seam row and E10: with the flag off no `ParameterLoadHandler` bean exists and the context starts. The consumer side matches E43S SPEC-018 (controller mapped if either flag is on; flag-off branch gives 404 MSG-P4-003) and SPEC-026 (`ObjectProvider`), with E43S TC-PB-01 and TC-FL-01. TC-22 starts the context with a probe bean that takes `ObjectProvider<ParameterLoadHandler>`. Wording gap DG-10 recorded. |
| 120 403 action text | Low | **Resolved** | SPEC-020: `require` throws `ApiProblemException(ApiError.NOT_PERMITTED, Map.of("action", action), null)`. Verified in code: `ApiExceptionHandler.problem` calls `problems.problem(ex.error(), ex.placeholders())`, and the MSG-P4-002 template "You cannot {action} here" takes the placeholder, so the text names the action rather than "do this". TC-24 asserts it. (Placement of `CapabilityCheck`: see finding 129.) |
| 121 Default in two places | Low | **Resolved** | SPEC-005: generated `ParameterKeys` holds every metadata column; `parameter_catalog` is a mirror; SPEC-007 takes the default from the generated key; TC-27 drift check with negative fixture (A-29). |
| 122 Lint versus seed literals | Low | **Resolved** | PRE-6 requires RWB-E1-044's lint. E44S SPEC-007 (one-pass quote-aware tokenizer, identifier text only, D-RUN-13) and T-044-21 confirm that `'${recoverySchema}.x'` inside a string and bare catalog names pass. TC-15 runs after RWB-E1-044. |
| 123 Readiness and `valid_from` | Low | **Resolved** | SPEC-016 and §12.9: value in force on the business date, else the generated default; cites build log line 140, triage item (f). TC-32. |
| 124 Coverage | Low | **Resolved, with residual** | §14: LINE, INSTRUCTION, BRANCH, METHOD at 0.80 (matches E44S SPEC-014); `recoveryCoverageVerification` outside `check` (D-RCV-40). Residual: test-scope tooling is not covered. Raised as new finding 131. |
| 125 Recorder in transaction | Low | **Resolved, with residual** | SPEC-014 transaction rule, §12.7 steps 1-7, recorder `Propagation.MANDATORY`, `AFTER_COMMIT` event, TC-29 (a) and (b). Residual: the HTTP outcome of a recorder failure is not mapped to the source contract. Raised as new finding 132. |
| 126 MSG-GEN-006 retry promise | Low | **Resolved** | SPEC-025 and §10.2: status-only Problem, type `urn:rwb:problem:unavailable`; MSG-GEN-006 removed from §10.3; TC-34. Error and Message Standard v4 confirms MSG-GEN-006 says the request is "queued and will be retried", and no other "try again" message fits a failed read. DG-11 should also cite API v4 `components/responses/E503`, which names MSG-P7-003 and MSG-GEN-006 for every 503 (gap candidate RV3-DG-01). |
| 127 Column definitions | Low | **Resolved** | CLAR-022 and DG-12: not in this catalog; keys, grammar and row check by RWB-E1-043 (E43S SPEC-003, SPEC-029 confirm 12 `refdata.columns.<code>` rows). |
| 128 Exact headings | Low | **Resolved** | `## Change Scope Declaration`, `## Requirement-to-SPEC Logic Coverage`, `## Unit Test Applicability`, `## Clarification Log` present with the exact text; §14 has the seven required columns. |

## 2. Plan inputs P1-P6 (from review 2)

| Input | Status |
|---|---|
| P1 Read-only literals | Addressed (§12.11 `HttpStatus` constants, named baseline constants). |
| P2 ENV values through `Environment` | Addressed (SPEC-024). Carry forward plan input 4.2 below. |
| P3 Concurrent identical loads | Addressed (SPEC-013, E12, TC-33). |
| P4 Interim recorder | Addressed (SPEC-019, §12.7). |
| P5 `ProblemFactory` change | Addressed in text; superseded by finding 129 because the class moves. |
| P6 Gradle on this workstation | Recorded in `agent-run-log.md`; plan concern only. |

## 3. New findings

| ID | Severity | Finding |
|---|---|---|
| `REVIEW-RWB-E1-042-129` | High | Module placement contradicts RWB-TE-001, which merges first |
| `REVIEW-RWB-E1-042-130` | Low | `usedBy[]` "split on comma" breaks seeded values |
| `REVIEW-RWB-E1-042-131` | Low | 80% gate does not cover the build checks or the key generator |
| `REVIEW-RWB-E1-042-132` | Low | Recorder failure maps to an unmapped 500, not 503 MSG-P7-003 |
| `REVIEW-RWB-E1-042-133` | Low | Specified refusal paths have no test case |
| `REVIEW-RWB-E1-042-134` | Low | Housekeeping: run log title and missing section |

### REVIEW-RWB-E1-042-129 (High): module placement contradicts RWB-TE-001, which merges first

**Maps to:** SPEC-020, -021, -022, -025, -026; §2 impacted nodes; §10.2; §12.1; §12.2; §12.10; §12.12;
A-01; CLAR-020; `compliance-validation.md` "Module boundaries" row and residual risk "`platform`
placement"; `shared-updates.md` §4 (answers to E43S).

**Evidence:**

- Spec SPEC-026 (line 173): "All code is in the `platform` module: published types in
  `th.co.scb.ace.demo.recovery.platform.api`". §2 lists `RecoveryFlags`, `RecoveryProperties`,
  `PlatformConfig`, `ApiProblemException`, `ProblemFactory` and `ApiExceptionHandler` as impacted in
  place. CLAR-020 (line 883) defaults to `platform` and says the module map is RWB-TE-001's; §12.1
  says moving the package "is RWB-TE-001's change".
- Build Sequence v6: RWB-TE-001 is order 2, RWB-E1-042 order 3. D-RUN-08: a spec depends only on
  existing code or an earlier story.
- RWB-TE-001 spec v4: SPEC-001 (d) removes the baseline packages `platform`, `rules`, `workflow`,
  `documents`. SPEC-004 (a) fails any package under the root that is not in the module map ("package
  {package} is not in the module map"); (d) requires `@NamedInterface(..., propagate = false)`.
  SPEC-022 moves `ApiError` and `ApiProblemException` to `access.api`, `ApiExceptionHandler`,
  `ProblemFactory` and `SecurityConfig` to `access.internal`, `RecoveryFlags` to
  `integration.flags.api`, `PlatformConfig` to `integration.flags`; SPEC-023 replaces
  `RecoveryProperties` with module records. SPEC-022 (g) moves classes of an earlier-merged story
  only; this story is later.
- RWB-TE-001 `shared-updates.md` SU-08 (round 2), addressed to "INC-003 RWB-E1-042": (a) code goes to
  P3 `recovery.casewf.config`, published `recovery.casewf.config.api` (story v7 RWB-E1-042 v1 §13);
  (b) no `RecoveryProperties`; (c) problem types are in P4; (d) any type P4 code calls, "for example
  `MessageResolver`, `CapabilityCheck`", must not live in P3, or `ModulithTest` fails on a cycle
  (D-RCV-11); (e) the premise that moving is RWB-TE-001's change "holds only if E1-042 merges before
  TE-001".
- Story v7 RWB-E1-042 line 89 names `recovery.casewf.casecreation` as a consumer and §13 names
  `recovery.casewf.config`, so A-01 "this repository has no `casewf` module" describes the baseline,
  not the branch this story is planned on.
- Revision 4 inputs (`agent-run-log.md` run 2, line 47) list E43S and E44S but not the RWB-TE-001
  spec. E43S still assumes `platform.api` for these types (E43S line 69), so the error propagates.

**Failure scenario:** The builder implements revision 4 on `develop-recovery` after RWB-TE-001 has
merged. `platform` no longer exists; `RecoveryFlags`, `RecoveryProperties`, `ApiError`,
`ProblemFactory` are at new paths or gone. Re-creating `platform.api` fails TE-001's module-map rule.
Placing `MessageResolver` (called by `ProblemFactory`, §10.2, SPEC-022) and `CapabilityCheck` in the
P3 module while P3 already depends on P4 creates a P3/P4 cycle that `ModulithTest` rejects (D-RCV-11,
D-RCV-42). The plan cannot be written from this spec without re-deciding module homes, which AGENTS
§7 says goes back to the analyst.

**Fix required:** Rebase revision 5 on RWB-TE-001's homes per SU-08: (1) put the implementation in
`recovery.casewf.config` and published types (`ParameterService`, `ParameterKey`, `ParameterKeys`,
`ParameterLoadHandler`, `ParameterLoadResult`, `ParameterValue`, `ParameterLoadedEvent`) in
`recovery.casewf.config.api`, adding `config.api` to the P3 published list with
`@NamedInterface(name = "config.api", propagate = false)` in the same merge request; (2) bind
`rwb.p3.configservice` in a `casewf.config` record or `@ConditionalOnProperty`, not in
`RecoveryProperties`/`RecoveryFlags`; (3) plan any `ApiError` addition through `access.api`; (4) place
`MessageResolver` and `CapabilityCheck` in `access.api` or in a module P4 already depends on, and
state the dependency direction; (5) replace A-01 and close CLAR-020 against TE-001 SPEC-022 and SU-08;
(6) update §2, §12.1, §12.2, §12.10, §12.12 and the class names in tests; (7) add a `shared-updates.md`
row telling E43S the new package of `ParameterLoadHandler` and `CapabilityCheck`. Cite the RWB-TE-001
spec as a source.

### REVIEW-RWB-E1-042-130 (Low): `usedBy[]` "split on comma" breaks seeded values

**Maps to:** §7.5 (line 308); §12.4; SPEC-011; TC-09, TC-31.

**Evidence:** §7.5 builds `usedBy[]` by "split on comma". §12.4 seeds values such as
`recovery.workflow (RWB-E1-070, RWB-E1-071)`, which contain a comma inside parentheses. The pack
catalog `_v2-baseline/implement/config/parameter-catalog.csv` has quoted comma lists
(`"recovery.casewf.casecreation, recovery.casewf.allocation"`) and free text (`ACE common module`).
API v4 `Parameter.usedBy` is an array of string, so each element should be one consumer.

**Failure scenario:** GET `/admin/parameters` returns `["recovery.workflow (RWB-E1-070", "
RWB-E1-071)"]` for that key: broken elements with a leading space. A consumer filtering on module
name gets no match.

**Fix required:** Define the `used_by` grammar (separator, trimming, whether parentheses are allowed)
in §7.5 and §12.4, make the seed rows conform, have the catalog check (SPEC-003) reject a value that
does not parse, and add a test row for it.

### REVIEW-RWB-E1-042-131 (Low): the 80% gate does not cover the build checks or the key generator

**Maps to:** §14 backend row (line 759); §12.11; SPEC-003, -004, -005; TC-02, TC-03, TC-21, TC-25,
TC-26.

**Evidence:** §12.11 puts the two build checks, with a hand-written tokenizer, in
`backend/src/test/java/.../architecture/`, and generates `ParameterKeys` by a Gradle task in
`build.gradle.kts`. `backend/build.gradle.kts` lines 131-160: `recoveryClasses` covers main output
only (`th/co/scb/ace/demo/recovery/**`). §14 says nothing about these surfaces. D-RCV-40 and D-RCV-43
(2) (`INC-001-decisions.md` line 87) add test-scope tooling classes to `recoveryCoverageReport` and
`recoveryCoverageVerification` at 80%; E44S does the same with a separate row (E44S line 523).

**Failure scenario:** The tokenizer that enforces AC2/AC3 (no literal, no uncatalogued key) ships
untested beyond two fixtures. A tokenizer branch for text blocks or comments regresses, and the 80%
gate still passes because those classes are not measured.

**Fix required:** Add §14 rows for the test-scope build checks (measured at 80% on the four counters
by adding the test class directory, per D-RCV-43 (2)) and for the generator (either move the
generation logic into a testable class under coverage, or state the exception with its rationale and
the test that covers its output, TC-26/TC-27).

### REVIEW-RWB-E1-042-132 (Low): recorder failure maps to an unmapped 500, not 503 MSG-P7-003

**Maps to:** E11 (line 357); SPEC-014, -019; §10.3; TC-29 (b).

**Evidence:** E11: "The recorder's problem, else 500 (existing handler)". The existing
`ApiExceptionHandler.unexpected(Exception)` returns 500 with no `messageCode`. API v4, approve
operation (line 3214): approval "writes a decision log entry with decision code AC-VERS" and lists
503 `E503`; `components/responses/E503` (line 6028): "The decision could not be recorded ... Messages
MSG-P7-003, MSG-GEN-006". Error and Message Standard v4 line 208 defines MSG-P7-003 "Decision log
write failed (principle 5)" with user text that the action was not taken. AGENTS §3.6 requires
messages by ID.

**Failure scenario:** The decision recorder (RWB-E1-038 later; interim now) throws. The approver sees
a 500 with no message ID, and RWB-E1-043's endpoint returns a status the API v4 contract does not
list for approve.

**Fix required:** State that a recorder failure surfaces as 503 MSG-P7-003 (through the recorder
contract or a mapped exception), add MSG-P7-003 to §10.3 with its EN/TH text, and assert status and
message in TC-29 (b).

### REVIEW-RWB-E1-042-133 (Low): specified refusal paths have no test case

**Maps to:** §7.4 line 297; §8 lines 324, 325, 328; E4, E6; SPEC-014, -015, -017; CLAR-023; §15.

**Evidence:** §15 (TC-01 to TC-34) has no case for: E6 unknown `loadId` on approve and rollback (404
MSG-P4-003); §8 approve after `validFrom` has passed (409 MSG-P3-027, line 324); §8 rollback of a
`VALIDATED` or `ROLLED_BACK` load (409 MSG-P3-027, line 328); approve of an already `APPROVED` or
`ROLLED_BACK` load (409 MSG-GEN-004, line 325; TC-20 covers concurrency only); the 400/401-character
rollback reason boundary (TC-18 tests blank only); and `find(loadId)` (SPEC-017, used by E43S for
dispatch). Two of these rules are the specifier's own defaults (CLAR-023), which makes a test more
important, not less.

**Failure scenario:** The builder omits the state guard on rollback of a `VALIDATED` load; no test
fails, and a rollback against unapproved rows reaches the version-rewrite step.

**Fix required:** Add test rows for each path above with input and expected status and message ID,
and a `find` test (hit and miss).

### REVIEW-RWB-E1-042-134 (Low): housekeeping

**Maps to:** `agent-run-log.md` lines 1 and 60.

**Evidence:** The title still reads "(revision 3)", while the file now records run 2 / revision 4.
Run 2 step 6 says "See 'Gate (run 2)'", but no such section exists.

**Failure scenario:** A reader tracing the evidence trail finds a title that contradicts the content
and a dangling reference.

**Fix required:** Retitle the log for revision 4 (or revisions 3-4) and add the "Gate (run 2)"
section with this review's result.

## 4. Plan inputs (not findings)

1. **Transaction boundary of `load`.** SPEC-013 recovers from a unique violation by re-reading. In
   PostgreSQL the failed statement aborts the transaction, so the catch and re-read must sit outside
   it (or use a savepoint). State also whether `load` joins an outer RWB-E1-043 transaction.
2. **ENV values on GET.** SPEC-024 reads ENV values through `Environment`. No ENV row may point at a
   credential-bearing property; the catalog check should enforce `secret = true` for any such key.
3. **Cache rebuild after rollback.** Run it after commit, as for approval; other instances learn of a
   rollback only by TTL (no event), which should be stated next to FL8.
4. **`ApiExceptionHandler.problem` with message-ID constructors.** If a problem is built from a
   message ID rather than an `ApiError`, `ex.error()` is null; the handler change belongs to the P4
   home after finding 129.

## 5. Checks performed

| Check (compliance-reviewer.md) | Result |
|---|---|
| Authentication and authorisation | `GET /admin/parameters` method check (SPEC-020) holds against `SecurityConfig` (`@EnableMethodSecurity`); actuator health details limited to RW-PLATADM in `application.yaml`. Placement of `CapabilityCheck`: finding 129. |
| Data protection | No personal data in seed or tests (synthetic UUIDs, label "U-41"). Secret values never returned (SPEC-010, TC-09). Author/approver classification differs from E43S: gap candidate RV3-DG-03. |
| Audit logging | Decision record in the approval transaction (SPEC-014); failure contract: finding 132. Access log is a seam to RWB-E1-039. |
| Error contract | problem+json via `ProblemFactory`; message IDs in §10.3; gaps 130 (data shape) and 132 (503). |
| Secrets | None in code or config; ENV read through `Environment`; plan input 4.2. |
| Test coverage per AC | AC1-AC11 mapped; TC-12 `Blocked` honestly; missing refusal tests: finding 133. |
| 80% gate per changed surface | Four counters on main code; test-scope tooling and generator missing: finding 131. |
| Migration rules (D-RCV-28, D-RUN-07, D-RUN-12, D-RUN-13) | One file, `<seq>` at merge, `${recoverySchema}`, one table per migration; passes E44S rules (PRE-6). |
| Dependencies (D-RUN-08, D-RUN-10, D-RUN-11) | Load endpoint not built here; interface published. Earlier-story contract with RWB-TE-001 broken: finding 129. |
| D-RCV-35 / D-RCV-36 | No `public` read, no inbound load, no Temporal or Drools call. |
| Required headings and §14 columns | Present (finding 128 resolved). |
| MCP | None connected; N/A. |

## 6. Document-gap candidates

| ID | Source and conflict | Blocker | Suggested handling |
|---|---|---|---|
| E1042-RV3-DG-01 | API Specification v4 `components/responses/E503` names only MSG-P7-003 and MSG-GEN-006 for every 503, including `getAdminParameters`; neither fits a failed read (Error and Message Standard v4). Extends E1042-SP-DG-11. | No | Message owner adds a read-failure message or the API marks the 503 as status-only for reads. |
| E1042-RV3-DG-02 | Story v7 RWB-E1-042 v1 §13 names `recovery.casewf.config`; the baseline repository has only `platform`. Settled by RWB-TE-001 SPEC-022 and SU-08 (finding 129). | No | Record as resolved by RWB-TE-001; the specifier follows SU-08. |
| E1042-RV3-DG-03 | Personal-data classification of load author and approver: this spec SPEC-027 says not personal (DF-REF-156); E43S SPEC-028 classifies them as personal (DF-REF-166/167, Personal Data Inventory v4). Not verified further in this review. | No | Data protection owner confirms one classification; both specs align. |

## Gate decision

```text
SPEC_GATE: FAIL
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 1] [MEDIUM: 0] [LOW: 5]
BLOCKING: YES (High 129)
EARLIER_FINDINGS: 119-128 resolved (124 and 125 with residuals raised as 131 and 132)
NEXT_STEP: Technical Specifier revision 5 (rebase on RWB-TE-001 module homes per SU-08; fix 130-134), then spec-gate-review-4.md
```

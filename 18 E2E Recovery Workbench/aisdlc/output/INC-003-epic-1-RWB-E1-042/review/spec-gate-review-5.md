# Spec gate review 5: RWB-E1-042 (RUN_ID `INC-003-epic-1-RWB-E1-042`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-042-SPEC-007` |
| Gate | Specification gate, re-review of revision 6 (round 5) |
| Artifacts under review | `specify/spec.md` revision 6 (1108 lines), `assumptions.md` (A-01 to A-47), `document-gaps.md` (E1042-SP-DG-01 to -17), `shared-updates.md` (rev 6 rows), `compliance-validation.md`, `gate-response.md` (Rounds 1-4), `agent-run-log.md` (runs 1-4) |
| Compared with | `review/spec-gate-review-4.md` (`REVIEW-RWB-E1-042-SPEC-006`: Medium 135, Lows 136-142, plan inputs 1-6, candidate E1042-RV4-DG-01); revision 5 snapshots `specify/*.run4.md` |
| Baseline | Document set v14: User Stories Epic 1 Story Files v7 (RWB-E1-042 v1; RWB-E1-069 v1 header), Physical Schema v6 (`parameter_value`, lines 1412-1434), Data Classification and Personal Data Inventory v4 (Fields sheet), API Specification v4, Error and Message Standard v4, Build Sequence v6; run decisions D-RUN-07 to D-RUN-17 (`AI-SDLC-BUILD-LOG.md` lines 30-40); build log timeline lines 188-209 |
| Cross-story specs read | RWB-TE-001 spec v4 ("TE1S": SPEC-003, SPEC-020, SPEC-022, SPEC-024, SPEC-025, field-level matrix, T-TE001-14; `shared-updates.md` SU-08, SU-14); RWB-E1-043 spec revision 4 ("E43S", on disk 01:24: SPEC-003, -018, -019, -020, -025 L13, -026, TC-HD-01, GAP-51, shared-updates R16, R24); RWB-E1-044 spec v14-6 ("E44S": SPEC-014, and `gate-response.md` S22); RWB-TE-003 spec (SPEC-022, T-TE003-35) |
| Repository | `<repo>` working tree as read 2026-11-18: `platform/api/ApiProblemException.java`, `platform/internal/ApiExceptionHandler.java`, `ProblemFactory.java` (baseline homes; `access.*` after RWB-TE-001) |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18 |
| Supersedes | `REVIEW-RWB-E1-042-SPEC-006` for revision 6. That review stays as history. |

## Status

**`SPEC_GATE: FAIL`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 0 | |
| Low | 6 | Visible; not accepted by the orchestrator under D-RUN-09, so fixed in the next run |

Revision 6 resolves Medium 135 and Lows 136-142. Each fix was checked in the revised text and, where it rests
on another source, against that source. The E7 503 is now raised as the published `ApiProblemException` in a
status-only form and rendered in `access.internal`. No P3 code calls `ProblemFactory`.

The six new Lows are about drift between this spec and specs revised in parallel, plus two precision points.
In order: the tooling coverage task this spec relies on has been withdrawn by RWB-E1-044 (143). The new
`ApiProblemException` form does not carry the multi-failure `detail` that RWB-E1-043 now expects from it (144).
The business-date seam prescribes a P3 → P1 edge that RWB-E1-043 has recorded as a latent cycle (145). TC-29 (b)
asserts handler output in a test where the handler never runs (146). The `parameter_value` field matrix leaves
out four Physical Schema v6 columns, including `created_by`, which this revision declares personal (147). One
housekeeping item (148).

## 1. Earlier findings (135-142): verification

| Finding | Severity | Verdict | Evidence checked |
|---|---|---|---|
| 135 E7 called package-private `ProblemFactory` from P3 | Medium | **Resolved** | §10.2 adds `ApiProblemException(HttpStatus, String messageId, Map, String field, Throwable)` with `status()`, `messageId()`, `field()`, and `error()` null for this form. E7 throws it with a null message ID. `ApiExceptionHandler.problem` keeps its `ApiError` branch and, when `error()` is null, calls `ProblemFactory` in the same package. §12.1 lists the change under `access.api` / `access.internal`; SPEC-022, -025 and -026 agree; TC-30 (c) and TC-34 test it. Checked against the code: the handler today only has the `ex.error()` path, so the branch is a real addition, and it is planned. TE1S SPEC-022/-025 keep `ProblemFactory` package-private, which this design respects. |
| 136 T-TE001-14 pins the published surface | Low | **Resolved** | §2 Impacted Existing Nodes, §12.12, §12.14 T-1 and T-2, TC-45 and `shared-updates.md` (rev 6 row) all name the T-TE001-14 extension. The `access.api` set gains two types. The eleven `casewf.config.api` types match the §12.1 list (I counted them). The named interfaces become `api`, `config.api`, `rules`, `timers`, `workflow`. Nothing is removed, and TC-45 fails if a further type is added. A-40 (the map has no per-type field) matches the TE1S field-level matrix and SPEC-003 (unknown keys fail the loader). |
| 137 Handler-branch logging | Low | **Resolved, with residual (146)** | §10.2 and §12.13 log one WARN line: message ID (or `none`), status, `traceId`, cause class and "cause suppressed". The cause message, stack trace, placeholders, field and user IDs are never logged (D-RUN-15, SPEC-027). TC-30 asserts that the synthetic marker is absent for forms (b) and (c), and TC-34 does the same over HTTP. TC-29 (b) also claims the log assertion, but it can't observe it (finding 146). |
| 138 Two wordings of the credential rule | Low | **Resolved** | SPEC-003 and §7.1 now give the same rule word for word: split on `.`, case-insensitive substring list, no allow-list. Checked by hand: the eight TC-44 fixtures fail and the two clean ones pass; the three real ENV properties (`rwb.temporal.target`, `rwb.temporal.namespace`, `rwb.drools.kiebase-cache-max`) pass. A-44 agrees. |
| 139 TC-10 (b) not executable | Low | **Resolved** | The failure is forced inside the rollback's own `REQUIRES_NEW` transaction by a test `BEFORE_COMMIT` listener on `ParameterLoadRolledBack`. In Spring, an exception from a before-commit synchronization rolls the transaction back and propagates, so the assertions are reachable. Package visibility is left as plan input 4. |
| 140 Two-module plan presumed approved | Low | **Resolved** | CLAR-025 is "OPEN (analyst; before the build)". A-33's owner is now the analyst. DG-16 quotes AGENTS §7 correctly ("back to the analyst before any code is written"), and the Why column cites AGENTS §10 rule 6. The shared-updates rev 6 row replaces the rev 5 row and is due "Before the build (plan stage)". No approval is claimed. |
| 141 Consumer direction of `casewf.config.api` | Low | **Resolved** | §4.3 first seam row, §12.1, SPEC-026 and shared-updates row 32 all say callers sit in P3, never P4 (TE1S SU-08, SU-14). Checked against E43S revision 4: all its code is in P3 `casewf.refdata`, and its SPEC-019 edge table has `casewf.refdata.internal` → `casewf.config.api` inside P3, with no P4 → P3 edge. §11.2 doesn't repeat the constraint, but SPEC-026 covers it. |
| 142 Housekeeping | Low | **Resolved** | `gate-response.md` is retitled "SPEC-003 to -006". R3.1 row 134 and R3.4 now say that "Gate (run 3)" was appended after review 4. That section exists (run log lines 106-116). The forward reference in run 4 step 5 to "Gate (run 4)" is disclosed in `compliance-validation.md` and R4.4 as added after this review, so it is not a false claim. |

## 2. Review-4 plan inputs 1-6 and gap candidate RV4-DG-01

| Item | Status |
|---|---|
| Plan input 1 (flag in always-registered beans) | Applied: SPEC-021 and §12.12 use `@Value("${rwb.p3.configservice:false}")` in `ParameterServiceImpl` and `ParameterStartupCheck`, `@ConditionalOnProperty` elsewhere, and add no `RecoveryFlags` field (A-45). |
| Plan input 2 (MAIN coverage from `test`) | Applied in §14 (unit tests named). The tooling half of §14 is now stale (finding 143). |
| Plan input 3 (bean name `capabilityCheck`) | Applied: §12.10; shared-updates row to RWB-E1-037. |
| Plan input 4 (RFC 4180 load file) | Applied: §7.4, §12.6, TC-16. |
| Plan input 5 (recorder flush) | Applied: SPEC-019. |
| Plan input 6 (E43S revision in force) | Applied as A-28 and §12.14 R4-6. E43S is now at revision 4 (see plan input 1 below). |
| RV4-DG-01 | Recorded as E1042-SP-DG-17. Verified: Inventory v4 lines 652-678 have no `created_by`/`updated_by` row for either table; DF-EXT-010/-012 (lines 1339, 1341) say "Staff identifier", personal "Yes"; Physical Schema v6 lines 1406, 1408, 1429, 1431 define the columns. The protective reading is applied in SPEC-027, §7.2, §7.3, §12.13 and §17. |

## 3. New findings

| ID | Severity | Finding |
|---|---|---|
| `REVIEW-RWB-E1-042-143` | Low | Tooling coverage relies on `recoveryToolingCoverageVerification`, which RWB-E1-044 has withdrawn |
| `REVIEW-RWB-E1-042-144` | Low | The new `ApiProblemException` form can't carry the multi-failure `detail` that RWB-E1-043 expects from it; RWB-TE-003 is not told about the new branch |
| `REVIEW-RWB-E1-042-145` | Low | Business-date seam prescribes a P3 → P1 call that RWB-E1-043 records as a latent P1 ↔ P3 cycle |
| `REVIEW-RWB-E1-042-146` | Low | TC-29 (b) asserts handler rendering and the handler's log line in a test where the handler never runs |
| `REVIEW-RWB-E1-042-147` | Low | §7.3 leaves out four `parameter_value` columns, including `created_by`, now declared personal |
| `REVIEW-RWB-E1-042-148` | Low | Housekeeping: run-decision citations and the §12.14 heading |

### REVIEW-RWB-E1-042-143 (Low): tooling coverage relies on a task RWB-E1-044 has withdrawn

**Maps to:** §12.11 (lines 813-821); §14 backend row; S-23; A-38; `compliance-validation.md` rows "Build-check and
generator coverage" and "Backend unit-test applicability"; TC-41, TC-43, TC-44.

**Evidence:**

- The spec says the build-check classes "are in the TOOLING class set of E44S SPEC-RWB-E1-044-014" and are
  "measured by `recoveryToolingCoverageVerification` at 0.80". It also says "E44S SPEC-RWB-E1-044-014 ... adds
  `INSTRUCTION` and `METHOD` at 0.80".
- E44S v14-6 SPEC-014 says: "Withdrawn from v14-4. The split into rule MAIN and rule TOOLING ... is replaced";
  "`recoveryToolingCoverageVerification` and `recoveryToolingCoverageReport` are not built". It also says E44S
  makes "no change to a counter or threshold". E44S `gate-response.md` S22 records that RWB-TE-001 SPEC-020 (b)
  "wins" (triage at build log 00:55, before this run started at 01:13).
- TE1S SPEC-020: (a) gives `recoveryCoverageVerification` the four limits at 0.80; (b) "both tasks add the
  test-output class directory of the tooling package to `classDirectories`", which is one combined bundle.

**Failure scenario:** The planner names `recoveryToolingCoverageVerification` as the evidence task. The task
doesn't exist. The builder then either adds it to `build.gradle.kts`, a shared file that RWB-TE-001 owns and
E44S says must not gain it, or produces no tooling evidence. Either way the gate isn't run as planned.

**Fix required:** Restate §12.11 and §14 on TE1S SPEC-020 (a)-(b) and E44S v14-6 SPEC-014. Keep one combined
`BUNDLE` in `recoveryCoverageReport` / `recoveryCoverageVerification` (LINE, INSTRUCTION, BRANCH, METHOD at
0.80; `test` data; outside `check`). Add the test-output classes of `architecture.parameters`, excluding JUnit
classes, to `classDirectories` of both tasks, or state that RWB-TE-001's filter already covers them, as E44S
does for its own tooling package. Attribute the four counters to TE1S SPEC-020 (a). Update S-23, A-38 if
needed, the two self-check rows and the TC labels. Record the `build.gradle.kts` edit in `shared-updates.md`.

### REVIEW-RWB-E1-042-144 (Low): the new `ApiProblemException` form doesn't serve its named consumers

**Maps to:** §10.2 (lines 386-406); §12.2 (lines 577-579); SPEC-022, SPEC-025, SPEC-026; `shared-updates.md`
row 32 (rev 6 text); A-33.

**Evidence:**

- §10.2: in the message-ID form, `detail` is "EN from `MessageResolver`". The constructor takes status, message
  ID, placeholders, field and cause. There is no way to supply a `detail`.
- E43S revision 4 SPEC-003: a refused load answers 422 MSG-P3-027 where "`detail` lists every failed row and
  column, capped at 100". SPEC-025 L13: "`detail` = every failure's rendered text, in order, joined by '; '".
  TC-HD-01 and TC-E1-043-04 assert it. SPEC-020 says these are "rendered by RWB-E1-042's
  `access.api.ApiProblemException`". The E43S Change Scope says there is "no change to `ApiExceptionHandler`,
  `ProblemFactory` ... or `ApiProblemException` beyond what RWB-E1-042 delivers".
- This spec's shared-updates row 32 tells RWB-E1-043 that refusals arrive in this form and that it "does not
  call `ProblemFactory`".
- The RWB-TE-003 spec, SPEC-022, rewrites the logging of the same `problem` handler (D-RUN-15), and T-TE003-35
  tests it. RWB-TE-003 is Build Sequence order 5, after this story. No row in this spec's `shared-updates.md`
  tells RWB-TE-003 that `problem` gains a second branch and that `error()` is null for that form.

**Failure scenario:** RWB-E1-043 can't produce its multi-failure `detail` through the published form, so it
must change P4 again, which its spec says it won't do, or drop the behaviour its ACs test. The two specs are
gated separately and can both pass with the mismatch. Separately, RWB-TE-003 applies its logging rewrite to the
`ApiError` path and dereferences `ex.error()` on the new form.

**Fix required:** Agree the published form with its consumer. Either add an optional detail to the form now
(for example a `List<String> details`, or a `detail` override rendered in place of the resolver text, capped
as E43S needs), with a TC-30 case; or state in §10.2 and shared-updates row 32 that the form has no detail
override and that RWB-E1-043 adds one as its own P4 change, under its own AGENTS §7 open item. Add a
shared-updates row for RWB-TE-003: the handler has a message-ID branch, `error()` is null for it, and its
logging already meets D-RUN-15.

### REVIEW-RWB-E1-042-145 (Low): the business-date seam prescribes a P3 → P1 edge that would close a cycle

**Maps to:** §4.3 business-date row (line 146); SPEC-023; CLAR-015; A-20; `shared-updates.md` "Interim seams to
replace" row.

**Evidence:**

- §4.3: the later story "replaces the implementation with one in P3 that calls the view owner's published reader
  (P3 depends on that module)".
- Story v7 RWB-E1-069 v1 header: "Module | P1 Recovery data engine". The view owner is P1.
- D-RUN-11: RWB-E1-001 (P1) registers its handler on RWB-E1-043's registry. E43S revision 4 places that SPI in
  P3 `casewf.refdata.api` (SPEC-025, GAP-36), so the edge is P1 → P3.
- E43S GAP-51 and shared-updates R24 ("Latent P1 ↔ P3 cycle") cite this spec's §4.3 by name. They list
  RWB-E1-042 among the affected stories and ask for a decision "before RWB-E1-001 plan". TE1S SPEC-022 (d) and
  D-RCV-11 make `ModulithTest` reject a cycle.

**Failure scenario:** The story that fills the seam follows §4.3 as written. When RWB-E1-001's handlers have
merged, `ModulithTest` fails on P1 ↔ P3. Or the seam's fill route is changed later without this spec's guidance
being corrected.

**Fix required:** In the §4.3 row, keep the interface and the interim implementation, but don't prescribe the
P3 → P1 call. State the constraint instead: the fill must not add a P3 → P1 edge while P1 implements a P3 SPI.
Cite E43S GAP-51/R24 and TE1S SPEC-022 (d), and leave the route to the tech lead's R24 decision. Point the
shared-updates seam row at R24.

### REVIEW-RWB-E1-042-146 (Low): TC-29 (b) asserts handler output where the handler never runs

**Maps to:** TC-29 (b) (line 963); §15 preamble (lines 924-929); §10.2 logging paragraph (line 413-414);
finding 137.

**Evidence:** The §15 preamble says interface tests call "the `ParameterLoadHandler` bean ... directly". TC-29 is
"System (interface)". Its (b) column expects the exception "rendered through `ProblemFactory`: `status` 503,
`messageCode` ..., EN and TH text", and expects "the log line has MSG-P7-003, status, `traceId` and the cause
class". Both are produced by `ApiExceptionHandler` (`@RestControllerAdvice`), which runs only during MVC
dispatch. `ApiExceptionHandler` and `ProblemFactory` are package-private in `access.internal` (TE1S SPEC-022),
so a test in `casewf.config` can't call them either.

**Failure scenario:** The builder can't write TC-29 (b) as specified. Either the assertions are dropped ad hoc
(a test quietly narrowed), or reflection is used across a module boundary.

**Fix required:** Choose one. (i) Drive TC-29 (b) through MockMvc with a test-only controller under
`th.co.scb.ace.demo.recovery` (inside the advice's `basePackages`) that calls `approve`. (ii) Keep TC-29 (b) to
the exception fields, database state, event and cache, and leave rendering and the handler log line to TC-30,
which already covers both. In that case TC-29 (b) asserts only that no line logged by `casewf.config` code holds
the marker. Correct the §10.2 sentence to match.

### REVIEW-RWB-E1-042-147 (Low): §7.3 leaves out four `parameter_value` columns

**Maps to:** §7.3 (lines 277-296); SPEC-006; SPEC-027; §7.2; E1042-SP-DG-17.

**Evidence:** Physical Schema v6 `parameter_value` (lines 1412-1434) has `is_active boolean NOT NULL DEFAULT
true`, `state varchar(40)`, `created_at` and `created_by uuid`. §7.3 lists every other column but not these four.
SPEC-027 and §7.3's last row now declare `created_by` personal data and say it is "stored only in
`parameter_value` (and ... `parameter_catalog`)". No row says what `load` writes to `parameter_value.created_by`
(the author, the caller or NULL), nor what the 40 seeded value rows carry (§7.2 gives the seed identity for
catalog rows only). `is_active` has no stated meaning beside `status` (for example after a rollback).

**Failure scenario:** One builder writes the author into `created_by` and another leaves it NULL. TC-13 and the
SPEC-006 self-check can't assert it. If a later reader treats `is_active` as "in force", it disagrees with the
status-and-date rule of SPEC-007.

**Fix required:** Add the four rows to §7.3. For `created_by`: on load, the author user ID (or NULL, decided
and stated); on seed, the seed identity. For `created_at`: the default. For `is_active`: default `true`, never
changed by this story, and not read ("in force" comes from status and dates, §8). For `state`: NULL, unused.
Extend TC-13 to assert the seeded values.

### REVIEW-RWB-E1-042-148 (Low): housekeeping

**Maps to:** spec header line 6 and S-14 (line 50); `compliance-validation.md` line 14; §12.14 heading (line 880).

**Evidence:**

- The header and the self-check cite "D-RUN-07 to D-RUN-17". The self-check gives "`AI-SDLC-BUILD-LOG.md` lines
  30-36", but D-RUN-14 to -17 are at lines 37-40.
- S-14 lists D-RUN-07 to -13 only. The spec relies on D-RUN-15 (§10.2, §12.13, A-43) without a source row.
- §12.14 is headed "Plan inputs (REVIEW-RWB-E1-042-SPEC-005, inputs 1-4)", but it now also holds the review-4
  inputs R4-1 to R4-6 and T-1, T-2.

**Failure scenario:** A reader tracing a decision to its source finds a line range that doesn't contain it.

**Fix required:** Add D-RUN-15 and D-RUN-17 (and any others relied on) to S-14 with build log lines 38 and 40.
Correct the line range in the self-check. Retitle §12.14 to cover reviews 3 and 4.

## 4. Plan inputs (not findings)

1. **E43S revision 4.** E43S is now at revision 4, on disk at 01:24 and rebased on this spec's revision 5. Its
   SPEC-019 import list matches shared-updates row 32, and its flag-off refusal is still 404 MSG-P4-003
   (lines 401-403). It also edits this story's resources: 38 catalog rows, the grants file and `ListOfValuesReader`
   in `access.api`. So T-TE001-14's `access.api` set is extended again by RWB-E1-043, in the same way (A-41).
   Re-check against the E43S revision that passes its gate.
2. **New constructor guards.** Reject a null `messageId` unless the status is 503. At plan time, list every
   caller of `ApiProblemException.error()` (today only `ApiExceptionHandler.problem`), so that none dereferences
   it for the new form.
3. **Other data-access failures on GET.** E7 catches two exception types. Any other `DataAccessException` reaches
   the existing `unexpected` handler, which logs the full exception until RWB-TE-003. State in the plan that this
   is accepted as inherited behaviour, or widen the catch.
4. **TC-10 (b) package.** `ParameterLoadRolledBack` is package-private, so the test `BEFORE_COMMIT` listener must
   sit in the `casewf.config` test package.

## 5. Checks performed

| Check (compliance-reviewer.md) | Result |
|---|---|
| Authentication and authorisation | Method check on `GET /admin/parameters` through `CapabilityCheck` (`access.api`), bean `capabilityCheck`; 401 from `SecurityConfig`; load, approve and rollback rights on RWB-E1-043's endpoint (D-RUN-10). No defect. |
| Customer and account data protection | No customer data. Author, approver, rollback caller and the audit columns are personal (SPEC-027; SP-DG-15, -17). `rollback_reason` follows Inventory v4 DF-REF-173 (`reference_version.rollback_reason`, not personal). `created_by` write rule: finding 147. |
| Audit logging | AC-VERS through the recorder inside the approval transaction; 503 MSG-P7-003 on failure; handler logging safe (137 resolved). |
| KYC, AML, suitability, consent, approval | Not in scope beyond maker-checker (SPEC-014, DB check). |
| Frontend integration and error contract | No frontend (§13). Problem contract: 135 resolved; consumer fit: finding 144. |
| Secrets and environment configuration | Secrets listed, never served; one credential-name rule (138 resolved). |
| Test coverage per AC | AC1-AC11 and X1-X10 mapped; TC-12 honestly `Blocked`. TC-29 (b): finding 146. |
| 80% gate per changed surface | Backend REQUIRED at 0.80 on four counters, outside `check`. Tooling wiring is stale: finding 143. Generator exception recorded (A-38). Frontend `NOT_APPLICABLE` with evidence. |
| Migration rules (D-RCV-28, D-RUN-07, -12, -13) | One file, `<seq>` at merge, `${recoverySchema}`, guarded DDL, PRE-6. Field matrix: finding 147. |
| Module boundaries (D-RUN-08, -10, -11; TE1S) | P3 → P4 only; T-TE001-14 extended (136); P3 caller (141). Later seam: finding 145. |
| D-RCV-35 / D-RCV-36 | No `public` read; no Temporal or Drools call; six keys catalogued. |
| Required headings and §14 columns | Present. |
| Personal data in this run's files | None found: synthetic UUIDs and the label "U-41" only; no name reproduced from `INC-001-decisions.md`. |
| MCP | None connected; N/A. |

## 6. Document-gap candidates

None. The six findings are about drift between specs and the precision of this spec. Each is settled by an
earlier story's spec (TE1S, E44S) or by a decision already routed (E43S R24). None is a silence or conflict in
the document set that this review has not already seen recorded (E1042-SP-DG-01 to -17; E43S GAP-51).

## Gate decision

```text
SPEC_GATE: FAIL
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 6]
BLOCKING: NO by severity; not accepted under D-RUN-09 (fix and re-gate)
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
EARLIER_FINDINGS: 135, 136, 138-142 resolved; 137 resolved with residual 146
NEXT_STEP: Technical Specifier revision 7 (fix 143-148), then spec-gate-review-6.md
```

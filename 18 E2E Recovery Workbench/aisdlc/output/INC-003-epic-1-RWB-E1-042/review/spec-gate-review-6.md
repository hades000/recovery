# Spec gate review 6: RWB-E1-042 (RUN_ID `INC-003-epic-1-RWB-E1-042`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-042-SPEC-008` |
| Gate | Specification gate, re-review of revision 7 (round 6) |
| Artifacts under review | `specify/spec.md` revision 7 (1147 lines), `assumptions.md` (A-01 to A-50), `document-gaps.md` (E1042-SP-DG-01 to -17, none added), `shared-updates.md` (rev 7 rows), `compliance-validation.md`, `gate-response.md` (Rounds 1-5), `agent-run-log.md` (runs 1-5) |
| Compared with | `review/spec-gate-review-5.md` (`REVIEW-RWB-E1-042-SPEC-007`: Lows 143-148, plan inputs 1-4); revision 6 snapshots `specify/*.run5.md` |
| Baseline | Document set v14: User Stories Epic 1 Story Files v7 (RWB-E1-042 v1), Physical Schema v6 (`parameter_catalog` lines 1386-1409, `parameter_value` lines 1412-1434), Data Classification and Personal Data Inventory v4, API Specification v4, Error and Message Standard v4, Build Sequence v6; run decisions D-RUN-07 to D-RUN-17 (`AI-SDLC-BUILD-LOG.md` lines 30-40); build log timeline to 04:54 |
| Cross-story specs read | RWB-TE-001 spec v4 ("TE1S": SPEC-020 (a)-(e), SPEC-022 (d), SPEC-024; `shared-updates.md` SU-08, SU-14); RWB-E1-043 spec revision 4 ("E43S", on disk 01:24: SPEC-003 lines 258-265, SPEC-020 line 434, SPEC-025 L13 line 556, Change Scope line 74, TC-HD-01, TC-E1-043-04; `shared-updates.md` R24 line 94; `document-gaps.md` GAP-36, GAP-51); RWB-E1-044 spec v14-7 ("E44S", on disk 01:35: SPEC-014 lines 359-375); RWB-TE-003 spec (SPEC-022, T-TE003-35; spec gate PASS round 6, build log 04:54) |
| Repository | Read only; no change since review 5 relevant to this spec |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18 |
| Supersedes | `REVIEW-RWB-E1-042-SPEC-007` for revision 7. That review stays as history. |

## Status

**`SPEC_GATE: FAIL`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 0 | |
| Low | 2 | Visible; Low-only failure (REVIEW_GATE_WARNING). Under D-RUN-09 the orchestrator does not accept it |

Revision 7 resolves all six review-5 findings (143-148). Each fix was checked in the revised text and against
the source it rests on. The tooling coverage now sits in RWB-TE-001's one combined bundle. The new
`ApiProblemException` form carries the optional `detail` that E43S needs, with constructor guards, and
RWB-TE-003 has a routing row. The business-date seam no longer prescribes a P3 → P1 edge. TC-29 (b) asserts only
what a direct call can observe. §7.3 lists all `parameter_value` columns.

Two new Lows remain, both small. The load-side `created_by` assertion added for finding 147 points at a test that
writes nothing (149). Some text left over from earlier revisions still names the withdrawn class sets and the old
E43S revision, and some E44S line citations have drifted (150).

## 1. Earlier findings (143-148): verification

| Finding | Severity | Verdict | Evidence checked |
|---|---|---|---|
| 143 Tooling coverage on a withdrawn task | Low | **Resolved, with residual (150 a)** | §12.11 and §14 now use one `BUNDLE` rule in `recoveryCoverageReport` / `recoveryCoverageVerification`, with LINE, INSTRUCTION, BRANCH and METHOD at 0.80. The counters are attributed to TE1S SPEC-020 (a) ("four limits at 0.80"). Execution data is `test` only and the task stays outside `check` (SPEC-020 (c), (d)). The `architecture.parameters` test-output classes go into `classDirectories` of both tasks, with JUnit classes and fixtures excluded, or the plan shows RWB-TE-001's filter already covers them. This matches E44S v14-7 SPEC-014 line 369. `recoveryToolingCoverageVerification` is named only as withdrawn (E44S line 375, verified). S-23, A-38, both self-check rows and a new shared-updates row (to the RWB-TE-001 owner) agree. Residual: §2 and §14 still use the withdrawn "class set" wording (150 a). |
| 144 Published form lacks `detail`; RWB-TE-003 not told | Low | **Resolved** | §10.2 and §12.2 add `String detail` to the constructor and a `detail()` accessor. When `detail` is set, the handler renders it in place of the resolver's EN text. `messageCode` and `messageTh` still come from the message ID, which matches E43S SPEC-025 L13 ("first failure's `messageCode`, `placeholders` and `field`; `detail` = every failure's rendered text"). The producer applies E43S's cap of 100 plus the total. The override is never logged, and the exception message stays the message ID. Guards: `status` is required, and `messageId` may be null only for a 503 with no placeholders, field or detail. TC-30 (d) and (e) test them. E43S line 74 ("no change ... beyond what RWB-E1-042 delivers") now holds. The shared-updates row to RWB-E1-043 (rev 7 text) and a new row to RWB-TE-003 (`error()` is null on the second branch; logging already meets D-RUN-15) are present. The RWB-TE-003 spec, which passed its gate, keeps SPEC-022 generic ("the `messageCode` where one exists"), so it doesn't conflict (plan input 2). |
| 145 Business-date seam P3 → P1 | Low | **Resolved** | The §4.3 row keeps the interface and the interim implementation. It prescribes no route and states the constraint (no P3 → P1 edge while P1 implements a P3 SPI). It cites TE1S SPEC-022 (d), D-RCV-11 and E43S R24 / GAP-51. Verified: E43S `shared-updates.md` line 94 is R24, it names "RWB-E1-042 §4.3", and its decision is due "Before RWB-E1-001 plan". The shared-updates seam row and A-50 agree. |
| 146 TC-29 (b) asserts handler output | Low | **Resolved** | TC-29 (b) now asserts `messageId()`, `status()`, no placeholders, `detail()` null, the cause, rows, event and cache, and that no `casewf.config` log line holds the marker. Rendering and the handler log line are in TC-30, a unit test in `access.internal` that can reach the package-private handler. E7 over HTTP is in TC-34 (MockMvc). The §10.2 paragraph and the §15 preamble say the same. No assertion was dropped from the test set: the generic WARN-line format is covered by TC-30 (b)-(d). |
| 147 §7.3 missing columns | Low | **Resolved, with residual (149)** | §7.3 now has `created_at` (default), `created_by` (author on load; seed identity on seed), `is_active` (default `true`, never changed or read) and `state` (NULL), as Physical Schema v6 lines 1426-1431 define them. A-49 records the choice. TC-13 asserts the seeded values. The load-side assertion is not executable as written (149). |
| 148 Housekeeping | Low | **Resolved, with residual (150 b, c)** | S-14 adds D-RUN-15 (line 38) and D-RUN-17 (line 40). I checked the build log, and those lines hold them. The self-check range is now "lines 30-40". §12.14 is retitled for reviews 3-5. Other stale text is in 150. |

## 2. Review-5 plan inputs 1-4

| Item | Status |
|---|---|
| 1 (E43S revision in force) | Carried as §12.14 R5-1. E43S is still at revision 4 and in its gate round 4 (build log 04:54). Its imports match shared-updates row 32, and its flag-off refusal is still 404 MSG-P4-003. |
| 2 (constructor guards; callers of `error()`) | Applied in §10.2 and TC-30 (e); the planner lists the callers. |
| 3 (other `DataAccessException` on GET) | Applied: §10.2 E7 accepts the inherited 500 path until RWB-TE-003 (D-RUN-15). |
| 4 (TC-10 (b) package) | Applied: TC-10 (b) puts the listener in the `casewf.config` test package. |

## 3. New findings

| ID | Severity | Finding |
|---|---|---|
| `REVIEW-RWB-E1-042-149` | Low | TC-13's load-side `created_by` assertion points at TC-05, a refused load that writes nothing |
| `REVIEW-RWB-E1-042-150` | Low | Housekeeping: withdrawn "class set" wording, stale E43S revision label, drifted E44S line citations |

### REVIEW-RWB-E1-042-149 (Low): the load-side `created_by` assertion has no executable test

**Maps to:** TC-E1-042-13 (spec line 979); §7.3 `created_by` row (line 298); A-49; finding 147.

**Evidence:**

- TC-13's data is "empty schema" (a migration test). Its expected column adds "a row written by `load` has
  `created_by` = its `author_user_id` (TC-05)".
- TC-05 (line 971) loads `case.entry.dpd,PROD,400`, which is refused with 422 MSG-GEN-002, and its expected
  result is "nothing written". No row exists to assert on.
- The tests that write rows through `load` are TC-07, TC-11, TC-16 and TC-40. None of them asserts `created_by`.

**Failure scenario:** The builder can't run the assertion where the spec places it. Either it's dropped, and the
§7.3 rule (load writes the author into `created_by`) has no test, or someone attaches it to a test that isn't
named. One builder might leave `created_by` NULL on load, and no test would fail. That is the drift finding 147
was meant to close.

**Fix required:** Move the load-side assertion to a test that writes rows, for example TC-40 (a fresh load is
read back by `find`) or TC-16. Assert `created_by` = `author_user_id`, `is_active` true, `state` NULL, and,
after approval in TC-07 or TC-11, that `created_by` is unchanged and `updated_by` is the approver. Remove
"(TC-05)" from TC-13. Use synthetic UUIDs only, and don't put them in any log assertion (SPEC-027).

### REVIEW-RWB-E1-042-150 (Low): housekeeping

**Maps to:** §2 Impacted Existing Nodes (line 79); §14 backend row (line 949); path-abbreviation paragraph (line 28);
S-22 (line 58); S-23 (line 59).

**Evidence:**

- (a) §2 says `backend/build.gradle.kts` holds the "parameter tooling classes in the tooling class set, §14".
  §14 says the generator is "in neither class set". E44S v14-7 line 375 withdraws the MAIN/TOOLING class sets,
  and §12.11 now correctly says the generator is not in "the combined bundle's class directories". This is
  residue from finding 143.
- (b) Line 28 defines "E43S" as "the RWB-E1-043 spec revision 3 (in remediation ...)". S-22 says "revision 3, in
  remediation ... (as read 2026-11-18 00:13)". But §10.2 and §12.14 R5-1 rely on E43S revision 4 (SPEC-003,
  SPEC-025 L13), and A-48 cites "E43S revision 4".
- (c) S-23 cites E44S "lines 203, 330-345, 359-375, 391, 470". In E44S v14-7 (on disk 01:35), SPEC-007 is at line
  227, SPEC-016 at line 398 and T-044-21 at line 526. Lines 203, 391 and 470 now hold unrelated text. Lines
  359-375 are still correct. E44S was revised in parallel with this run, so the drift is not the specifier's
  doing, but the citation no longer leads to its source.

**Failure scenario:** A planner who reads §2 or §14 looks for a "tooling class set" that no longer exists. A
reader who traces E43S or E44S from the source table lands on the wrong revision or the wrong line.

**Fix required:** In §2, change the `build.gradle.kts` item to the combined-bundle wording of §12.11
("`architecture.parameters` test-output classes added to `classDirectories`"). In §14, say "not in the
combined bundle's class directories". Redefine E43S as revision 4 (on disk 01:24) in line 28 and S-22, and keep
A-28's re-check at plan time. Re-read E44S v14-7 for S-23 line numbers, or cite E44S by SPEC ID and test ID only.

## 4. Plan inputs (not findings)

1. **Shared coverage filter.** Three stories edit the same `classDirectories` include in `backend/build.gradle.kts`:
   RWB-TE-001 (its boundary tooling), RWB-E1-044 (its lint tooling) and this story. E44S v14-7 SPEC-014 line 369
   says RWB-TE-001 plan v1 takes in only `architecture/boundary/**`. The plan extends the filter as merged and
   doesn't replace it. It reads the include in RWB-TE-001's gated plan and the merged file, and the builder
   stops on a mismatch, as E44S does.
2. **RWB-TE-003 handover.** RWB-TE-003 passed its spec gate (round 6, 04:54) without mentioning the second branch.
   Its SPEC-022 is generic and compatible. The orchestrator should apply the rev 7 shared-updates row before
   RWB-TE-003's plan, so that T-TE003-35 also exercises an `ApiProblemException` in the message-ID form (where
   `error()` is null) and its rewrite keeps that branch's `detail` out of the log.
3. **E43S at its gate.** Check that the E43S revision that passes its gate builds its multi-failure `detail`
   through this constructor's `detail` argument, as its line 74 implies, and adds no P4 change of its own.
4. **Constructor guard coverage.** TC-30 (e) tests a null `messageId`. At plan time, also cover a null `status`,
   and a 503 with no message ID and non-empty placeholders, both named in the §10.2 guards.

## 5. Checks performed

| Check (compliance-reviewer.md) | Result |
|---|---|
| Authentication and authorisation | Method check on `GET /admin/parameters` through `CapabilityCheck` (bean `capabilityCheck`); 401 from `SecurityConfig`; load, approve and rollback rights on RWB-E1-043's endpoint (D-RUN-10). No defect. |
| Customer and account data protection | No customer data. Author, approver, caller and audit columns personal (SPEC-027; SP-DG-15, -17); `created_by` write rule now stated (§7.3); its load-side test: finding 149. `detail` override never logged. |
| Audit logging | AC-VERS through the recorder inside the approval transaction; 503 MSG-P7-003 on failure; handler branch logs no cause text (D-RUN-15). No defect. |
| KYC, AML, suitability, consent, approval | Not in scope beyond maker-checker (SPEC-014, DB check). |
| Frontend integration and error contract | No frontend (§13). Problem contract now fits E43S's multi-failure `detail` (144 resolved). |
| Secrets and environment configuration | Secrets listed, never served; one credential-name rule. No defect. |
| Test coverage per AC | AC1-AC11, X1-X10 mapped; TC-12 honestly `Blocked`; TC-29 (b) executable. Load-side `created_by`: finding 149. |
| 80% gate per changed surface | Backend REQUIRED, four counters at 0.80 in one bundle, `test` data, outside `check`; tooling joins the bundle; generator exception recorded (A-38). Frontend `NOT_APPLICABLE` with evidence. Wording residue: finding 150 (a). |
| Migration rules (D-RCV-28, D-RUN-07, -12, -13) | One file, `<seq>` at merge, `${recoverySchema}`, guarded DDL, PRE-6; §7.3 complete. No defect. |
| Module boundaries (D-RUN-08, -10, -11; TE1S) | P3 → P4 only; T-TE001-14 extended; P3 caller; business-date seam adds no cycle (145 resolved). |
| D-RCV-35 / D-RCV-36 | No `public` read; no Temporal or Drools call; six keys catalogued. |
| Required headings and §14 columns | Present. |
| Personal data in this run's files | None found: synthetic UUIDs and the label "U-41" only. No name from `INC-001-decisions.md` is reproduced. |
| MCP | None connected; N/A. |

## 6. Document-gap candidates

None. Both findings are about this spec's own precision and its citations of specs revised in parallel. Neither
is a silence or conflict in the document set beyond those already recorded (E1042-SP-DG-01 to -17; E43S GAP-51).

## Gate decision

```text
SPEC_GATE: FAIL
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]
BLOCKING: NO by severity; not accepted under D-RUN-09 (fix and re-gate, or route to the engagement lead for a human disposition)
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
EARLIER_FINDINGS: 144, 145, 146 resolved; 143, 147, 148 resolved with residuals 150 (a), 149, 150 (b, c)
PLAN_INPUTS: 4
DOCUMENT_GAP_CANDIDATES: 0
NEXT_STEP: Orchestrator triage of 149-150 (Technical Specifier revision 8, then spec-gate-review-7.md)
```

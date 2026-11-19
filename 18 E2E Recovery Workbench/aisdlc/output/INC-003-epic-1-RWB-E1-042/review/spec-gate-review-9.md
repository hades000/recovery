# Spec gate review 9: RWB-E1-042 (RUN_ID `INC-003-epic-1-RWB-E1-042`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-042-SPEC-011` |
| Gate | Specification gate, re-review of revision 10 (remediation run 8) |
| Artifacts under review | `specify/spec.md` revision 10 (1230 lines), `assumptions.md` (A-01 to A-55), `document-gaps.md` (E1042-SP-DG-01 to -18), `shared-updates.md` (rev 10 rows), `compliance-validation.md`, `gate-response.md` (Rounds 1-8), `agent-run-log.md` (runs 1-8). No `contracts/` folder (spec §20 explains why) |
| Compared with | `review/spec-gate-review-8.md` (`REVIEW-RWB-E1-042-SPEC-010`: Lows 155-158, plan inputs 1-4, no gap candidate); revision 9 snapshots `specify/*.run8.md` (full diff of all seven files read) |
| Run decisions | D-RUN-07 to D-RUN-19, `AI-SDLC-BUILD-LOG.md` decisions table. Triage that allows this round: "2026-11-18T05:10:44, RWB-E1-042, Gate triage, REMEDIATE (D-RUN-09)". D-RUN-18 (timeline row 2026-11-18T04:55:55, ALL, Decision) and D-RUN-19 (2026-11-18T05:10:44, ALL, Decision) were made by the orchestrator (Claude Code). Neither is ratified, and this review does not treat either as human-ratified |
| Cross-story specs read | RWB-E1-043 spec ("E43S") revision 6 (`spec.md`, written 2026-11-18 05:24, not yet gated: its `review/` folder ends at `spec-gate-review-5.md`, which gated revision 5), lines 44, 599-617, 738-752, 787-788, 829-830; E43S `document-gaps.md` GAP-57; E43S `shared-updates.md` R24, R32. RWB-TE-001 spec v4 ("TE1S") SPEC-022 (d) as cited in review 8. `backend/build.gradle.kts` (test dependencies) |
| Document set | Story files v7: RWB-E1-042 v1 (X2 line 62, AC3 line 103, TC-E1-042-03 line 301); RWB-E1-037 v1 (lines 46, 192 BR3). Build Notes Epic 1 v4 line 2089 (per-table approver role "from the parameter catalog") |
| Repository | Read only; not changed by this review |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18 |
| Supersedes | `REVIEW-RWB-E1-042-SPEC-010` for revision 10. That review stays as history. |

## Status

**`SPEC_GATE: FAIL`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 0 | |
| Low | 2 | Visible; Low-only failure (REVIEW_GATE_WARNING). Under D-RUN-09 the orchestrator does not accept it |

Revision 10 resolves 155, 156 and 158. It resolves 157 in its requirement text: SPEC-003 now defines the key
read, refuses non-literal keys, and TC-03 has fixtures (b) and (c). How the check finds a
`CatalogParameterReader.get` call is still undefined, though, and the specified tooling cannot find one as
written (159). The spec handles E43S correctly. It cites revision 6 as read in run 8, "not yet gated", and defers
to the revision in force at plan time (S-22, A-28, R7-1, R8-1). One defining note still says revision 4 (160).
No ratification or human acceptance is recorded anywhere, and CLAR-027 stays OPEN. This story's placement still
adds no module cycle.

The two new Lows:

- 159: Under the new SPEC-003 rule, a key read is "the first argument of a call to
  `access.api.CatalogParameterReader.get`", which must be a string literal. The check is a source scanner with no
  type resolution and no new dependency, and its fixtures are not compiled. A real reader calls an injected
  instance (`reader.get(...)`), and nothing in the spec says how the scanner knows that the receiver is a
  `CatalogParameterReader`. The TC-03 fixtures are written in a static-call form that no real caller uses. The
  implementation class itself is recovery main code, and the spec does not say whether its own delegation is
  exempt.
- 160: Housekeeping. The header note still defines E43S as revision 4. In `assumptions.md`, a blank line cuts A-54
  and A-55 off from the table. R8-1 says it "supersedes" R7-1 wording that revision 10 has already rewritten.

## 1. Earlier findings 155-158: verification

| Finding | Fix required (review 8) | Verdict | Evidence in revision 10 |
|---|---|---|---|
| 155 `PARAMETER` route described as an SPI implementation; E43S revision cited as 4 | (1) Describe the route as E43S specifies it in §4.3, A-51, `shared-updates.md` row 32 and R7-1. (2) Record the D-RUN-18 wording difference in CLAR-027 without deciding it. (3) Cite the E43S revision now on disk or defer to the revision in force; relabel TC-22 (b) | **Resolved** (residual wording in 160 (a), (c)) | (1) §4.3 line 145: "`PARAMETER` is not an SPI handler, and no `PARAMETER` SPI bean exists". The dispatcher separates it (E43S SPEC-030). The branch is `ParameterLoadBranch` in `casewf.refdata.internal` (E43S SPEC-026), "which implements no `access.api` type", obtains the handler only through `ObjectProvider`, and answers 404 MSG-P4-003. A-51, `shared-updates.md` row 32 (the rev 10 sentence replaces the rev 9 one, and the rev 8 sentence is corrected) and R7-1 (line 983) match. This agrees with E43S revision 6 lines 599-617 ("a bean for `PARAMETER`, fails start-up"; "*`PARAMETER` is not an SPI handler*") and lines 750-752. (2) CLAR-027 (line 1157) and `shared-updates.md` row 39 record the difference: "this spec does not decide which governs; the flag-off contract is the same either way". (3) S-22 (line 58): "revision 6 on disk at 2026-11-18 05:24 and not yet gated, read in run 8". A-28 defers ("the plan re-checks the revision in force"), and so do R7-1 and R8-1. The file time (05:24) and the gate state were checked against the E43S folder. TC-22 (b) (line 1050) is now "a test-only adapter standing for RWB-E1-043's `PARAMETER` branch". E43S GAP-57 and R32 (a) asked this story to make exactly this alignment. |
| 156 Business date for a P4 caller | Add `get(key, type)` that reads the date from `BusinessDateProvider`; keep the three-argument form; extend TC-46 | **Resolved** | §12.2 line 610 `<T> Value<T> get(String key, Class<T> type);`. The prose (lines 638-640) says that a P4 caller "passes no date and reads on the same business date as P3". SPEC-023 (line 184) is extended and now lists TC-46. A-54 is added. The `shared-updates.md` rev 9 R row (line 38) now tells RWB-E1-011 and RWB-E1-037 about both forms. TC-46 (line 1074) asserts that "the two-argument `get` passes the provider's date to `ParameterService`". Edges: the P4 caller depends only on `access.api`. The implementation (P3) uses `BusinessDateProvider` in its own module. A later P3 → P1 provider is allowed under D-RUN-18. No new static edge and no cycle. The overload adds no type, so T-TE001-14's expected set is unchanged. |
| 157 String-key rule not in SPEC-003, untested, non-literal keys unaddressed | (1) Put the rule in SPEC-003. (2) Add a TC-03 fixture. (3) State the non-literal treatment | **Resolved in the requirement text; implementability residual (159)** | (1) SPEC-003 (line 164) defines a key read as "a `ParameterKeys` constant, a `ParameterKey.of` call, or the first argument of a call to `access.api.CatalogParameterReader.get`". A non-literal first argument "fails the build naming the file and line". (2) TC-03 (line 1031) has fixtures (b) and (c), and §12.11 (line 881) lists them. (3) A-55 records the protective reading. However, the spec never says how a source scanner recognises such a call. See 159. |
| 158 Housekeeping | "Three" in §2 and A-40; new type and implementation in §2 New Nodes and the §12.1 Types column; §12.12 bean row and TC-22 flag-off assertion; §12.4 annotation moved; run-log gate section | **Resolved** | (a) §2 line 83: "the three new `access.api` types (and the nested `CatalogParameterReader.Value`)". A-40 is updated, and T-1 (line 958) is annotated "two at review 4; three since revision 9". (b) §2 line 84 lists `CatalogParameterReader` and `CatalogParameterReaderImpl`. (c) §12.1 line 546 Types column. (d) §12.12 line 924, and the TC-22 expected results add "the `CatalogParameterReader` bean is present and returns the same default, `versionNo` 0". (e) The §12.4 cell is now the bare value `recovery.dataengine.caselist`, with a note under the table (lines 758-759). (f) `agent-run-log.md` line 217 "Gate (run 7)". Run 8 step 4 now says "once returned" and no longer points to a missing section. |
| Review-8 plan inputs 1-4 | Carry | **Carried** | §12.14 R8-1 to R8-4 (lines 993-996). |

## 2. Handling of E43S (revised in parallel)

| Check | Result | Evidence |
|---|---|---|
| Cites the revision it read | Yes, except one defining note | S-22 cites revision 6, its file time and its not-gated state. A-28 cites "revision 6, in run 8". The §1 header note (line 28) still defines "E43S" as "revision 4" (160 (a)). |
| Defers to the revision in force at plan time | Yes | A-28 ("the plan re-checks the revision in force"), §4.3 line 145 ("the plan re-checks the E43S revision in force (A-28)"), R7-1, R8-1. |
| Content agrees with revision 6 | Yes | Dispatcher branch, `ObjectProvider`, 404 MSG-P4-003, no `PARAMETER` SPI bean, no second load record beside `parameter_value.load_id` (E43S lines 606-617). The multi-failure `detail` of SPEC-003 and SPEC-025 L13, still cited as "revision 4" at line 403 and A-48, is unchanged in revision 6 (E43S line 636), so those citations remain true. |
| E43S revision 6 reads this spec at revision 9 | Noted, plan input 1 | E43S line 44 cites "RWB-E1-042 spec revision 9 ... §4.3 line 144". In revision 10 the row is at line 145, and `get(key, type)` is added. No type or name that E43S relies on changed. |

## 3. D-RUN-18 and D-RUN-19: attribution and ratification

| Check | Result | Evidence |
|---|---|---|
| Credited to the orchestrator | Yes | CLAR-027 "made by the orchestrator, Claude Code". `shared-updates.md` row 39 "both made by the orchestrator (Claude Code)". |
| No ratification or acceptance recorded | Yes | A search of every line added in revision 10 finds only "no ratification is recorded", "No ratification is recorded" and the owner column "Recovery tech lead (ratifies D-RUN-19, CLAR-027)". `gate-response.md` Round 8: "No human acceptance or ratification is recorded". |
| D-RUN-18 wording against E43S | Recorded, not decided | CLAR-027 and row 39, as review 8 asked. Whether D-RUN-18's text is reworded is the orchestrator's or the tech lead's call (E43S R32 (b)). This spec does not decide it. |
| Authority for this round | Consistent with the brief | `gate-response.md` Round 8 and `agent-run-log.md` run 8 cite the 05:10:44 triage under D-RUN-09. The build log has no row yet for the review-8 result. Recording that row is the orchestrator's task, so this is not a finding against the spec. |

## 4. New findings

| ID | Severity | Finding |
|---|---|---|
| `REVIEW-RWB-E1-042-159` | Low | The SPEC-003 rule for `CatalogParameterReader.get` keys cannot be implemented as specified. The source-scanning check has no way to recognise an instance call, the TC-03 fixtures use a call shape no real reader writes, and the implementation's own delegation is not addressed |
| `REVIEW-RWB-E1-042-160` | Low | Housekeeping: the header note defines E43S as revision 4; a blank line cuts A-54 and A-55 out of the assumptions table; R8-1 "supersedes" wording that R7-1 no longer has |

### REVIEW-RWB-E1-042-159 (Low): the `CatalogParameterReader.get` key rule names a call the specified check cannot find

**Maps to:** SPEC-RWB-E1-042-003 (line 164); §12.2 (lines 635-637); §12.11 (lines 862-882: build checks, tooling
classes, fixtures); TC-E1-042-03 (line 1031); A-55; `shared-updates.md` row 38 (rev 10 clause); story v7 RWB-E1-042
AC3 (line 103), X2 (line 62); GR1; finding 157.

**Evidence:**

- The checks are source scanners. §12.11 names the tooling as "`JavaLiteralTokenizer` (strips comments, reads
  literals), `MagicNumberScanner`, `CatalogFileParser` ... and `CatalogCompletenessRules`", and says "No new
  dependency (AGENTS §4.4)". The fixtures "are not compiled" (line 882). `backend/build.gradle.kts` has no Java
  parser with symbol resolution. ArchUnit is present (test scope). It sees call targets in compiled classes, but
  it does not see argument values, and it cannot run on uncompiled fixtures.
- The two key reads SPEC-003 already had are recognisable by name in the source: `ParameterKeys.X` and
  `ParameterKey.of("...")`. The new one is an instance method. Real readers in P1 and P4 hold an injected
  `CatalogParameterReader` and call `reader.get("...", T.class)`. Without the receiver's type, a scanner cannot
  tell that call from `Map.get`, `Optional.get` or any other `get`. The spec gives no rule for this, for example
  "a `get(` call on a field, parameter or local declared as `CatalogParameterReader` in the same file".
- TC-03 (b) and (c) are specified as calls to "`CatalogParameterReader.get("allocation.retry.limit", Integer.class, d)`"
  and "`CatalogParameterReader.get(key, Integer.class)`", which is the static-call text. A builder who matches
  the literal text `CatalogParameterReader.get(` passes both fixtures and misses every real call.
- `CatalogParameterReaderImpl` is "recovery main code" (package-private in `casewf.config`, §12.2 line 640). Its
  two-argument `get` naturally delegates with the caller's `key` variable, which is a non-literal first argument
  to `get`. The spec neither exempts the implementation nor tells it to delegate only to `ParameterService`.

**Failure scenario:** This is the same scenario review 8 gave for 157, and it is still open. The builder writes a
text match for `CatalogParameterReader.get(`, and TC-03 (a)-(c) pass. Later, RWB-E1-011 writes
`tolerances.get("recon.tolerence.pct", BigDecimal.class)` against an injected field, the key is misspelt, the build
passes, and AC3 ("Build fails naming the key", X2) is broken for every reader outside P3. The opposite outcome is
also possible. A builder who flags every `.get(` with a non-literal first argument fails the build on ordinary
`Map.get(key)` calls, and on `CatalogParameterReaderImpl` itself.

**Why Low:** No reader outside P3 exists in this story, and the defect is in how the check is specified, not in
the runtime behaviour. The fix is text inside this story's own spec.

**Fix required:**

1. In SPEC-003 or §12.11, define how the scanner recognises a call. A suitable rule: within one source file, a
   call `<name>.get(` where `<name>` is a field, constructor or method parameter, or local variable declared with
   type `CatalogParameterReader` (the imported simple name or the fully qualified name). State the limits, for
   example that a method reference or a receiver obtained some other way is refused or out of scope, and test
   whatever is chosen.
2. State how `CatalogParameterReaderImpl` is treated. Either it is excluded by path, or it delegates only to
   `ParameterService` and never calls `get` on itself or on another `CatalogParameterReader`.
3. Rewrite the TC-03 (b) and (c) fixtures as instance calls through an injected field, and add a fixture where the
   receiver is a constructor parameter. Add a negative case: a `Map<String, ?>.get(key)` call with a non-literal key
   in the same fixture is not a finding.

### REVIEW-RWB-E1-042-160 (Low): housekeeping

**Maps to:** spec §1 header note (line 28); S-22 (line 58); `assumptions.md` lines 60-63; §12.14 R7-1 (line 983)
and R8-1 (line 993).

**Evidence:**

- (a) Line 28 still reads "\"E43S\" is the RWB-E1-043 spec revision 4 (in remediation on 18 Nov 2026 ...)". S-22,
  A-28 and §4.3 now cite revision 6. The defining note is the first place a planner reads, and it gives the
  wrong revision. Review 8's fix item 3 asked for revision 6 to be cited in S-22, A-28 and §4.3, and revision 10
  did that, but the definition was left behind.
- (b) `assumptions.md` line 61 is blank, and A-54 and A-55 follow it on lines 62-63. In Markdown, a blank line
  ends a table. The two rows therefore render as plain text with no header, outside the A-01 to A-53 table, and
  the file has no final newline. The content is intact, but a reader who scans the table, or a tool that parses
  it, misses the two new assumptions.
- (c) R8-1 says it "supersedes the 'SPI route' wording of R7-1", but revision 10 rewrote R7-1 in place ("a
  dispatcher branch, not an SPI handler"). Both rows now describe the same check, with no conflict, so a planner
  may wonder what is superseded.

**Fix required:** In line 28, define E43S as "the RWB-E1-043 spec, revision 6 as read in run 8 (S-22), with the
revision in force re-checked at plan time". Remove the blank line before A-54 and add a final newline. Either drop
"supersedes ..." from R8-1, or say that R7-1 was reworded in revision 10 and R8-1 adds the T-TE001-14 check.

## 5. Plan inputs (not findings)

1. **E43S revision in force.** When E43S revision 6 (or a later one) passes its gate, re-check the `PARAMETER` branch
   (`ObjectProvider`, 404 MSG-P4-003), the P4 type set (SPI types and `ListOfValuesReader` only), and that E43S has
   re-read this spec at revision 10. E43S line 44 cites revision 9 and "§4.3 line 144", and the row is now at
   line 145. This carries R8-1.
2. **Computed keys outside P3.** E43S reads `rwb.refload.approver.<code>` by name in P3 (E43S lines 258, 787-788),
   which SPEC-003 does not count as a key read. RWB-E1-037 (P4) is named as a reader of `rwb.refload.approver.*`
   (story v7 RWB-E1-037 line 46). Its BR3 (line 192) has the approver role read "for the table", and Build Notes
   Epic 1 v4 line 2089 does the same. If RWB-E1-037 needs a per-table key, A-55's literal-only rule forbids
   `"rwb.refload.approver." + code`, and RWB-E1-037 would need one literal per table. `shared-updates.md` row 38
   already tells RWB-E1-037 that a non-literal key fails the build. Its specifier should raise the need, if it
   exists, before the rule is relaxed. This is not a defect in this spec.
3. **Ratification (CLAR-027) and module scope (CLAR-025).** Both stay OPEN. While they are open the plan must not
   treat D-RUN-18 or D-RUN-19 as ratified (R8-2), and no code may start before the analyst decides (R8-3, AGENTS §7).
4. **Coverage.** The new detection logic of 159 belongs in `CatalogCompletenessRules` (test-scope tooling in the
   combined bundle). Give it unit cases next to TC-41 and TC-44 so the 0.80 counters cover it.

## 6. CLAR-025 (two-module plan, AGENTS §7)

| Check | Result | Evidence |
|---|---|---|
| Recorded as open | Yes | CLAR-025 is unchanged, "OPEN (analyst; before the build)", with three P4 types. R8-3 is added. |
| No approval claimed | Yes | No revision 10 line claims analyst approval. |
| Revision 10 changes the module count | No | The overload is on an existing P4 type, and its implementation is in P3. |

## 7. Checks performed

| Check (compliance-reviewer.md) | Result |
|---|---|
| Authentication and authorisation | Unchanged. `GET /admin/parameters` goes through `CapabilityCheck` (R). The reader is an in-process call with no endpoint. No defect. |
| Customer and account data protection | No customer data. The new overload adds no field. Exception messages still carry "the key only". No defect. |
| Audit logging | Unchanged (AC-VERS; rollback write tested by TC-10). No defect. |
| KYC, AML, suitability, consent, approval | Out of scope beyond maker-checker. |
| Frontend integration and error contract | No frontend (§13). No message ID added. No defect. |
| Message IDs | Revision 10 adds none, and MSG-P4-003 is used as before. |
| No literal business values | Unchanged. The build-time key check for readers outside P3 depends on 159. |
| Secrets and environment configuration | The reader still refuses `secret=true` keys (SPEC-010, TC-46). No defect. |
| AC → requirement → test coverage | 57 of 57 rules mapped. SPEC-003 adds TC-03 (b), (c), and SPEC-023 adds TC-46. Gap: the TC-03 fixture shape and the detection rule (159). |
| 80% gate per changed surface | Backend REQUIRED: four counters at 0.80 in one bundle, outside `check`. Frontend `NOT_APPLICABLE`, with evidence. Planned (R8-4), not measured, which is correct at this stage. |
| Migration rules | No change in revision 10. |
| Module boundaries (D-RUN-08, -10, -11, -18, -19; TE1S) | No new edge or cycle (§1, finding 156 row). |
| Consistency with E43S | The content agrees with revision 6, and the citation and deferral are correct (§2). One defining note is stale (160 (a)). |
| Run-decision attribution | D-RUN-18 and D-RUN-19 are credited to the orchestrator and marked unratified in every file (§3). |
| Personal data in this run's files | None found in the revision 10 changes. Test identities are synthetic. |
| MCP | None connected; N/A. |

## 8. Document-gap candidates

None new. Findings 159 and 160 concern this spec's own text, not the document set. The computed-key question in
plan input 2 can be settled from story v7 RWB-E1-037 once that story is specified. It is not yet a conflict
between two sources.

## Gate decision

```text
REVIEW_STATUS: FAIL
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2] (159, 160)
BLOCKING: NO by severity; not accepted under D-RUN-09 (fix and re-gate, or route to the engagement lead for a human disposition)
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
EARLIER_FINDINGS: 155, 156, 158 resolved; 157 resolved in requirement text (implementability residual in 159)
E43S: revision 6 cited as read in run 8, not yet gated; plan re-checks the revision in force; header note stale (160)
D_RUN_18_19: credited to the orchestrator (Claude Code); not ratified (CLAR-027 OPEN); no human acceptance recorded
CLAR_025: OPEN to the analyst; three P4 types; no approval claimed
PLAN_INPUTS: 4
DOCUMENT_GAP_CANDIDATES: 0
NEXT_STEP: Orchestrator triage of 159-160 (Technical Specifier revision 11, then spec-gate-review-10.md; or route to the engagement lead for a human disposition under D-RUN-09)
```

SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]

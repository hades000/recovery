# Spec gate review 10: RWB-E1-042 (RUN_ID `INC-003-epic-1-RWB-E1-042`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-042-SPEC-012` |
| Gate | Specification gate, re-review of revision 11 (remediation run 9) |
| Artifacts under review | `specify/spec.md` revision 11 (1270 lines, file 2026-11-18 05:41:44), `assumptions.md` (A-01 to A-56), `document-gaps.md` (E1042-SP-DG-01 to -18), `shared-updates.md` (rev 11 rows), `compliance-validation.md`, `gate-response.md` (Rounds 1-9), `agent-run-log.md` (runs 1-9). No `contracts/` folder (spec §20 explains why) |
| Compared with | `review/spec-gate-review-9.md` (`REVIEW-RWB-E1-042-SPEC-011`: Lows 159-160, plan inputs 1-4, no gap candidate); revision 10 snapshots `specify/*.run9.md` (full diff of all seven files read) |
| Run decisions | D-RUN-07 to D-RUN-21, `AI-SDLC-BUILD-LOG.md` decisions table. Triage that allows this round: "2026-11-18T05:34:56, RWB-E1-042, Gate triage, REMEDIATE (D-RUN-09)". D-RUN-20 (timeline 2026-11-18T05:34:56, ALL, Decision) and D-RUN-21 (2026-11-18T05:36:54, ALL, Decision) were made by the orchestrator (Claude Code), as were D-RUN-18 and D-RUN-19. None is ratified. Ratification of D-RUN-18 to D-RUN-21 is open item OPEN-050 in `aisdlc/docs/open-items.md`. This review treats none of them as ratified |
| Cross-story specs read | RWB-E1-043 spec ("E43S"): `spec.md` revision 7 (file 05:34:41), snapshots `spec.run6.md` (revision 6) and `spec.run7.md` (revision 7, taken 05:40:49 for a revision 8 run); E43S `review/spec-gate-review-6.md` (`REVIEW-RWB-E1-043-SPEC-006`, 05:31:20) and `-7.md` (`REVIEW-RWB-E1-043-SPEC-007`, 05:40:14), summary and re-baseline sections only |
| Rules and code | `.github/rules/specification-execution-gates.md` (Step 3, Required Spec Structure), `pdlc.md`; `.github/agents/planner.agent.md` (Clarification Readiness Gate); `backend/build.gradle.kts` (ArchUnit 1.5.1, test scope; no Java parser); `aisdlc/RUN-BRIEF.md` (base package `th.co.scb.ace.demo.recovery`) |
| Repository | Read only; not changed by this review |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18 |
| Supersedes | `REVIEW-RWB-E1-042-SPEC-011` for revision 11. That review stays as history. |

## Status

**`SPEC_GATE: FAIL`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 0 | |
| Low | 2 | Visible; Low-only failure (REVIEW_GATE_WARNING). Under D-RUN-09 the orchestrator does not accept it |

Revision 11 resolves 159 and 160. The new §12.11 reader-call rule is a sound, implementable source-level rule.
It recognises the receiver by its declared type in the same file, gives both the instance form and the static
form, lists the refused forms, does not count `Map.get` or `Optional.get`, states its limit and exempts
`CatalogParameterReaderImpl` by path. TC-03 now has fixtures (a) to (i), which cover each case review 9 asked
for. D-RUN-20 and D-RUN-21 are applied as the triage described, are credited to the orchestrator, and are
marked as pending ratification (OPEN-050) in every file. CLAR-028 records the RWB-E1-037 per-table key question
without designing or deciding anything.

The two new Lows are both regressions in revision 11's own edits:

- 161: Several lines were joined in revision 11. The `## Change Scope Declaration` heading, which
  `specification-execution-gates.md` requires, is now glued to the end of the S-35 source row. The TC-E1-042-04
  row is glued to the end of TC-E1-042-03. In `compliance-validation.md`, two rows of the checklist are joined.
  This is the same class of defect as 160 (b).
- 162: Housekeeping. In `shared-updates.md` row 39, three decisions are now described as "both". The run log
  records a "further Low-only round" allowance that no build-log row records. Run-log steps 3 and 4 are slightly
  off.

## 1. Earlier findings 159-160: verification

| Finding | Fix required (review 9) | Verdict | Evidence in revision 11 |
|---|---|---|---|
| 159 The `CatalogParameterReader.get` key rule names a call the specified check cannot find | (1) Define how the scanner recognises a call (declared type in the file), state its limits, test it. (2) State how `CatalogParameterReaderImpl` is treated. (3) Rewrite TC-03 (b), (c) as instance calls through a field and a constructor parameter; add a `Map.get(key)` negative case | **Resolved** | (1) §12.11 line 881 "Reader-call rule". `CatalogCompletenessRules` works on the `JavaLiteralTokenizer` token stream, one file at a time, and uses no new dependency. The spec says why ArchUnit is not used ("sees compiled call targets but not argument values"), which is true of argument values. Reader names are fields, constructor and method parameters, record components, typed lambda parameters and locals declared with type `CatalogParameterReader`. The type is written either as the imported simple name (single-type import of `th.co.scb.ace.demo.recovery.access.api.CatalogParameterReader`, or `access.api.*`) or as the fully qualified name. The base package matches RUN-BRIEF. A reader call is `<name>.get(`, `this.<name>.get(` or the static text. A call whose first argument is not one string literal is refused with file and line, and so are a method reference, a `var` local initialised from a reader, and an ambiguous name. `get(` on any other receiver is not a key read. Limit (5), a reader reached through a getter or a call chain, is stated, and `shared-updates.md` row 38 tells readers outside P3 to hold the reader in a declared field or parameter. Unit cases for (1) to (6) sit beside TC-41 and TC-44 (R9-4, line 1028). SPEC-003 (line 165) points to the rule, and A-56 records it. (2) Both options are applied. §12.2 (lines 638-639): the implementation "delegates only to `ParameterService`", and the check "skips its file by path". §12.11 (6) names the path. (3) TC-03 (line 1063): (b) is an injected field `tolerances`, (c) a constructor parameter `reader`, (d) the static form, (e) a non-literal key, (f) `tolerances::get` and `var r = tolerances;`, (g) `Map<String, Integer> limits` with `limits.get(key)` and `Optional.get()` as negatives, (h) a catalogued key (`config.cache.ttl-seconds` is catalogued, §7 line 712), and (i) the exempt path. The expected results agree with the rule. The failure scenario of review 9 is closed: a text match on `CatalogParameterReader.get(` alone fails (b) and (c), and a match on every `.get(` fails (g) |
| 160 Housekeeping | (a) Define E43S as revision 6 as read in run 8, re-checked at plan time. (b) Remove the blank line before A-54; add a final newline. (c) Fix the R8-1 "supersedes" wording | **Resolved** | (a) Line 28: "revision 6 as read in run 8 (S-22 ...), with the revision in force re-checked at plan time". (b) `assumptions.md` lines 58-64 form one continuous table (A-56 added), and the file ends with a newline. (c) R8-1 (line 1015): "R7-1 was reworded in place in revision 10; R8-1 adds the T-TE001-14 check" |
| Review-9 plan inputs 1-4 | Carry | **Carried** | §12.14 R9-1 to R9-4 (lines 1025-1028). Plan input 2 is also CLAR-028 and `shared-updates.md` rows 41 and 91 |

## 2. Handling of E43S (revised in parallel)

| Check | Result | Evidence |
|---|---|---|
| Cites the revision it read | Yes | The line 28 note, S-22 and A-28 all cite revision 6 "as read in run 8". The run 9 inputs in `agent-run-log.md` list no new E43S read, so the citation is an accurate record of what was read. S-22's "not yet gated" is anchored to the 05:24 read, and it was true then. |
| Defers to the revision in force at plan time | Yes | Line 28, A-28, §4.3 line 146, R7-1, R8-1, R9-1 ("check ... that it has re-read this spec at revision 11"). |
| State of E43S now | Moved on, as expected | E43S revision 6 was gated at 05:31:20 (`REVIEW-RWB-E1-043-SPEC-006`, FAIL, 2 Low). Revision 7 (`spec.md` 05:34:41) re-baselines on this spec's revision 10 and was gated at 05:40:14 (`REVIEW-RWB-E1-043-SPEC-007`, FAIL, 2 Low, findings 153-154, gap G7-R01 on RWB-E1-019's handlers under D-RUN-20). A revision 8 run has started (snapshot `spec.run7.md`, 05:40:49). E43S review 7 verified E43S revision 7 against this spec's revision 10 and found the `PARAMETER` branch, `ObjectProvider`, 404 MSG-P4-003, T-TE001-14 set and consumed names consistent. It also found that this spec's SPEC-003 literal rule does not touch E43S, because E43S reads its per-code keys through `ParameterKeys.byName` in P3. Revision 11 changes none of the names E43S consumes and adds no type, so nothing there is invalidated. Plan input 1. |
| D-RUN-20 against E43S | Consistent | §4.3 line 146 now says D-RUN-20 settles the wording ("the P4 SPI is for handlers outside P3"). This matches build-log D-RUN-20 and the dispatcher-branch route of E43S revisions 6 and 7. |

## 3. D-RUN-18 to D-RUN-21: attribution and ratification

| Check | Result | Evidence |
|---|---|---|
| Credited to the orchestrator | Yes | S-14 ("same maker"), CLAR-025 and CLAR-027 ("SETTLED by D-RUN-2x (orchestrator)"), `shared-updates.md` rows 32, 34 and 39, `gate-response.md` Round 9. |
| No ratification or human acceptance recorded | Yes | Every added line that mentions ratification, approval or acceptance was searched. Each one reads "pending", "not presumed ratified", "does not treat it as ratified", "no ratification is recorded" or "no ... approval is claimed". `gate-response.md` Round 9: "no human acceptance or ratification is recorded". |
| OPEN-050 cited correctly | Yes | `open-items.md` OPEN-050 covers D-RUN-18, -19, -20 and -21 and the at-source definition of "module". It names the recovery tech lead and is due "Before the first of these stories merges". `shared-updates.md` rows 34 and 39 rely on it instead of adding a new register entry, which is correct. |
| D-RUN-21 applied within its terms | Yes | D-RUN-21 sends a plan back to the analyst only when it changes the common or collection module that the story file does not name. §12.1 (d) line 555 and CLAR-025 state that this plan "changes neither the common nor the collection module". R7-3 (line 1007) and R8-3 are rewritten, and R9-3 says the plan "treats none as ratified". E1042-SP-DG-16 stays as the definition gap at source (Blocker = No), as the triage note asked. |
| CLAR-027 closed as the triage said | Yes, with a planning note | CLAR-027 is "SETTLED by D-RUN-20". The ratification it used to carry now lives in OPEN-050, and R8-2 and R9-3 keep the "not ratified" constraint in the plan inputs. The count is correct: 28 CLAR rows (CLAR-020 RESOLVED; CLAR-025 and CLAR-027 SETTLED; 25 OPEN, rechecked by parsing the Status column). `SPEC_CLARIFICATION_STATUS` reports `OPEN_ITEMS: 25`. "SETTLED" is not a status the planner's Clarification Readiness Gate recognises (it reads `RESOLVED`). See plan input 4. |
| CLAR-028 records without designing | Yes | CLAR-028 (line 1189): "Nothing is decided here". `shared-updates.md` row 41 (§1) and row 91 (§4) are addressed to the RWB-E1-037 specifier. They name two candidate shapes, a declared key family or a dedicated reader method, and choose neither. The literal-only rule stands until RWB-E1-037 proposes otherwise. |

## 4. New findings

| ID | Severity | Finding |
|---|---|---|
| `REVIEW-RWB-E1-042-161` | Low | Revision 11 joined lines that must stay separate. The required `## Change Scope Declaration` heading now sits at the end of the S-35 row, so it no longer exists as a heading. TC-E1-042-04 is glued to the end of the TC-03 row. Two `compliance-validation.md` checklist rows are joined. S-34 and S-35 render outside the sources table |
| `REVIEW-RWB-E1-042-162` | Low | Housekeeping and provenance. `shared-updates.md` row 39 calls three decisions "both" and says "if either changes". The run log records a "further Low-only round" allowance that no build-log row holds. Run-log step 3 omits A-33, and step 4 names a gate section that does not exist yet |

### REVIEW-RWB-E1-042-161 (Low): joined lines remove a required heading and a test-case row

**Maps to:** spec §1 S-34, S-35 and the §2 heading (lines 70-73); §15 TC-E1-042-03 and TC-E1-042-04 (line 1063);
`compliance-validation.md` line 26; `specification-execution-gates.md` "Step 3: Emit Scope Declaration" and
"Required Spec Structure" (`spec.md` "MUST include" `## Change Scope Declaration`); AC4; finding 160 (b) and
finding 128 (review 2, required headings).

**Evidence:**

- (a) In revision 10, line 72 was the heading `## Change Scope Declaration`. In revision 11, line 72 is blank and
  line 73 reads ``| S-35 | ... spec-gate-review-9.md` |## Change Scope Declaration``. A search for lines that
  start with `## ` finds `## 1. Sources` and then `## 3. User story intent interpretation`, with no §2 heading
  between them. The section's content (Change Type to Backend Changes Required, lines 74-87) is intact, but the
  section it belongs to has no heading. Because blank lines come before both rows, S-34 (since revision 10;
  review 9 missed this) and S-35 render as paragraph text, not as rows of the S-01 to S-33 table.
- (b) Line 1063 holds the whole TC-E1-042-03 row followed by `|| TC-E1-042-04 | AC4, BR7, X3 | ...`. GitHub
  Flavored Markdown ignores cells beyond the header's column count. So TC-E1-042-04, the only test case for AC4
  (the UAT readiness failure with MSG-P3-032), does not render, and a tool that parses the test table by rows
  finds no TC-04 row. The AC4 row of the coverage table (line 207) still points to it.
- (c) `compliance-validation.md` line 26 ends the "Clarification status matches the log" row with
  ``OPEN_ITEMS: 25` || Pack open items carried open | PASS | ...``, so the triage (e) check is lost from the
  rendered checklist.

**Failure scenario:** The planner, or the Traceability Manager, locates the scope declaration by its required
heading and the AC4 test case by its row. Neither is found. A mechanical spec-structure check would fail the spec
on the missing `## Change Scope Declaration` alone, and a coverage tool reports AC4 without a test case.

**Why Low:** No content is lost. Each line is still in the file, and the fix is to insert three line breaks (and
remove two blank lines). Review 2 rated a required heading that was not exact as Low (128), and review 9 rated
an assumptions-table break of this kind as Low (160 (b)). This finding is kept consistent with both.

**Fix required:** In `spec.md`, put `## Change Scope Declaration` on its own line, preceded by a blank line, and
remove the blank lines before S-34 and S-35 so that S-01 to S-35 form one table. Split line 1063 so that
TC-E1-042-04 starts its own row. In `compliance-validation.md`, split line 26 so that "Pack open items carried
open" starts its own row. Then check every file of the set for `||` and for a table row followed by text on the
same line.

### REVIEW-RWB-E1-042-162 (Low): housekeeping and provenance

**Maps to:** `shared-updates.md` row 39; `agent-run-log.md` lines 249-252 and the run 9 steps (lines 267-269);
build-log timeline row 2026-11-18T05:34:56 (RWB-E1-042, Gate triage); D-RUN-09.

**Evidence:**

- (a) Row 39 now lists D-RUN-18, "D-RUN-20 (rev 11, below)" and D-RUN-19, in that order, and then says "both
  made by the orchestrator" and "if either changes". The row also says the register holds "D-RUN-18 to
  D-RUN-21" as OPEN-050, which is correct, but the row itself names only three of the four decisions.
- (b) `agent-run-log.md` line 251: "One further Low-only round allowed after review 10." The RWB-E1-042 triage
  row at 2026-11-18T05:34:56 says only "Re-gate as review-10". The D-RUN-21 row at 05:36:54 says nothing about
  rounds. Other stories' triage rows record such an allowance explicitly (for example RWB-TE-011 at 05:31:18).
  For this story, the claim has no source in the build log.
- (c) Run 9 step 3 lists "A-51, A-55 changed, A-56 added", but `assumptions.md` (header and diff) also changes
  A-33. Step 4 says "Recorded under 'Gate (run 9)'", but there is no such section yet. Run 8's step used "once
  returned" for this, which review 9 accepted.

**Failure scenario:** A reader of row 39 counts two decisions to ratify where the register has four. A reader of
the run log assumes a round allowance that the orchestrator never logged for this story.

**Why Low:** These are wording and provenance errors. No requirement, test or decision changes.

**Fix required:** In row 39, list D-RUN-18, -19 and -20 in order (and D-RUN-21 by reference to OPEN-050), and say
"all made by the orchestrator" and "if any changes". In the run log, either cite the build-log row that grants the
further round or remove the sentence (the orchestrator records allowances; the specifier does not). Add A-33 to
step 3, and say "once returned" in step 4.

## 5. Plan inputs (not findings)

1. **E43S revision in force.** When planning starts, re-check the E43S revision in force. That is revision 7
   (gated 05:40:14, FAIL 2 Low) or a later revision 8 (in progress since 05:40:49). E43S revision 7 cites this
   spec at revision 10. Check that the revision in force has re-read revision 11 (R9-1), and that G7-R01 (RWB-E1-019's
   handlers under D-RUN-20) leaves the `PARAMETER` dispatcher branch unchanged. This carries R8-1 and R9-1.
2. **Closing limit (5) of the reader-call rule (optional).** The source rule cannot see a reader reached through a
   getter or a call chain, or a reader inherited from a field declared in another file. Limit (5) names the first
   two; the inherited field falls under the same "declared in the file" condition, and the plan should say so.
   ArchUnit 1.5.1 is already a test dependency, and it reports every compiled call site of
   `CatalogParameterReader.get` with its source file and line. A plan task could cross-check that each such call
   site (outside `CatalogParameterReaderImpl`) is one the source rule recognised, and fail otherwise. This
   needs no new dependency. The plan decides. The spec as written is acceptable, because it states the limit
   and the human-review backstop.
3. **CLAR-028 option "dedicated reader method".** If RWB-E1-037 chooses a new method on `CatalogParameterReader`,
   it changes a P4 `access.api` type that this story publishes. That changes T-TE001-14's expected set and
   `CatalogParameterReaderImpl`, after this story merges (RWB-E1-037 is later in the build sequence). The
   RWB-E1-037 specifier should raise it as a shared update to RWB-E1-042. A declared key family needs no change
   to the type.
4. **Clarification readiness at plan time.** The planner's Clarification Readiness Gate (`planner.agent.md`)
   reads each `CLAR-*` Status as `RESOLVED`, and treats `OPEN` as blocking. Revision 11 has 25 OPEN rows (all
   marked non-blocking) and two `SETTLED` rows, a status the planner does not define. The plan must say under
   which recorded orchestrator ruling it proceeds. It must treat CLAR-025 and CLAR-027 as settled only by
   unratified orchestrator decisions (OPEN-050, R9-3), and must not report them as `RESOLVED` by a human.
5. **Coverage.** The reader-call logic (rules (1) to (6)) is test-scope tooling in the combined bundle (R9-4).
   Plan its unit cases next to TC-41 and TC-44 so that the four 0.80 counters cover it, including the refused
   forms and the path exemption.

## 6. CLAR-025 (module scope, AGENTS §7 and §9)

| Check | Result | Evidence |
|---|---|---|
| Recorded as settled by an orchestrator decision, not approved | Yes | CLAR-025 Status: "SETTLED by D-RUN-21 (orchestrator); pending tech-lead ratification (OPEN-050)". A-33 now names the tech lead as the owner of the ratification ("not presumed ratified"). `shared-updates.md` row 34 names the tech lead (OPEN-050) as the owner from revision 11. |
| Definition gap kept | Yes | E1042-SP-DG-16 is kept, Blocker = No, and its resolution column has a revision 11 note. `document-gaps.md` adds no gap, which is correct, because D-RUN-21 itself says the definition gap "is still recorded for the document owners". |
| Revision 11 changes the module count | No | It adds no type and no edge. The P4 change is still the three `access.api` types plus the `ApiProblemException` constructor and its rendering. |

## 7. Checks performed

| Check (compliance-reviewer.md) | Result |
|---|---|
| Authentication and authorisation | Unchanged. `GET /admin/parameters` goes through `CapabilityCheck` (R). The reader is an in-process call. No defect. |
| Customer and account data protection | No customer data. Revision 11 adds no field and no log line. No defect. |
| Audit logging | Unchanged (AC-VERS; the rollback write is tested by TC-10). No defect. |
| KYC, AML, suitability, consent, approval | Out of scope beyond maker-checker. |
| Frontend integration and error contract | No frontend (§13). No message ID is added or changed. No defect. |
| No literal business values | The build-time key check for readers outside P3 is now specified so that it can be implemented (159 resolved). Limit (5) is stated (plan input 2). |
| Secrets and environment configuration | Unchanged. The reader refuses `secret=true` keys (SPEC-010, TC-46). |
| AC → requirement → test coverage | 57 of 57 rules mapped. SPEC-003 is covered by TC-03 (a) to (i), TC-21, TC-41 and TC-44. AC4's TC-04 is present in the file but does not render as a row (161 (b)). |
| Required spec structure (specification-execution-gates) | The Change Scope Declaration content is present, but the required heading is lost (161 (a)). The other required headings are present: Requirement-to-SPEC Logic Coverage, Unit Test Applicability and Clarification Log. |
| 80% gate per changed surface | Backend REQUIRED: four counters at 0.80 in one bundle, outside `check`, and the new rule logic is in that bundle (R9-4). Frontend `NOT_APPLICABLE`, with evidence. Planned, not measured, which is correct at this stage. |
| Migration rules | Unchanged in revision 11. |
| Module boundaries (D-RUN-08, -10, -11, -18 to -21; TE1S) | No new edge or cycle. D-RUN-21 changes how the plan is routed, not the module graph. |
| Consistency with E43S | Correct citation and deferral. E43S has moved to revision 7 or later, which is a plan-time check (§2, plan input 1). |
| Run-decision attribution | D-RUN-18 to D-RUN-21 are credited to the orchestrator and recorded as unratified everywhere (§3). One wording slip is in 162 (a). |
| Personal data in this run's files | None found in the revision 11 changes. The fixture names and test identities are synthetic. |
| MCP | None connected; N/A. |

## 8. Document-gap candidates

None new. Findings 161 and 162 concern this run's own files. E1042-SP-DG-16 (the definition of "module") stays as
recorded, Blocker = No. D-RUN-21 settles it for this build only, and OPEN-050 asks for the definition at source.

## Gate decision

```text
REVIEW_STATUS: FAIL
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2] (161, 162)
BLOCKING: NO by severity; not accepted under D-RUN-09 (fix and re-gate, or route to the engagement lead for a human disposition)
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
EARLIER_FINDINGS: 159, 160 resolved
REGRESSIONS: 161 (joined lines: required Change Scope heading, TC-E1-042-04 row, compliance-validation row); 162 (wording, provenance)
E43S: revision 6 cited as read in run 8; plan re-checks the revision in force (now revision 7, gated FAIL 2L at 05:40:14; revision 8 in progress)
D_RUN_18_21: credited to the orchestrator (Claude Code); none ratified (OPEN-050); no human acceptance recorded
CLAR_025: SETTLED by D-RUN-21 pending ratification; E1042-SP-DG-16 kept, Blocker = No
CLAR_027: SETTLED by D-RUN-20 pending ratification
CLAR_028: OPEN (RWB-E1-037 specifier); nothing designed or decided
PLAN_INPUTS: 5
DOCUMENT_GAP_CANDIDATES: 0
NEXT_STEP: Orchestrator triage of 161-162 (Technical Specifier revision 12, then spec-gate-review-11.md; or route to the engagement lead for a human disposition under D-RUN-09)
```

SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]

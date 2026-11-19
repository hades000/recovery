# Spec gate review 11: RWB-E1-042 (RUN_ID `INC-003-epic-1-RWB-E1-042`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-042-SPEC-013` |
| Gate | Specification gate, re-review of revision 12 (remediation run 10) |
| Artifacts under review | `specify/spec.md` revision 12 (1287 lines, file 2026-11-18 05:50:36), `assumptions.md` (A-01 to A-56), `document-gaps.md` (E1042-SP-DG-01 to -18), `shared-updates.md` (revision 12), `compliance-validation.md`, `gate-response.md` (Rounds 1-10), `agent-run-log.md` (runs 1-10). No `contracts/` folder (spec §20 explains why) |
| Compared with | `review/spec-gate-review-10.md` (`REVIEW-RWB-E1-042-SPEC-012`: Lows 161-162, plan inputs 1-5, no gap candidate); revision 11 snapshots `specify/*.run10.md`. All seven files were diffed in full |
| Run decisions | D-RUN-07 to D-RUN-21, `AI-SDLC-BUILD-LOG.md` decisions table. The latest RWB-E1-042 triage row is "2026-11-18T05:34:56, RWB-E1-042, Gate triage, REMEDIATE (D-RUN-09)" ("Re-gate as review-10"). The orchestrator (Claude Code) allowed this further Low-only round in its message to the specifier. The build log does not hold that allowance (see §3). D-RUN-18 to D-RUN-21 are orchestrator decisions, and none is ratified. Their ratification is open item OPEN-050 in `aisdlc/docs/open-items.md`. This review treats none of them as ratified |
| Cross-story specs read | RWB-E1-043 spec ("E43S"): `spec.md` front matter (revision 8, file 05:45:08); E43S `review/spec-gate-review-8.md` (`REVIEW-RWB-E1-043-SPEC-008`, 05:51:43), header, status and RWB-E1-042 re-baseline sections only |
| Rules | `compliance-reviewer.md`; `.github/rules/specification-execution-gates.md` (Required Spec Structure); `pdlc.md` (REVIEW_GATE_WARNING); GitHub Flavored Markdown tables extension (escaped pipes in cells) |
| Repository | Read only; not changed by this review |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18 |
| Supersedes | `REVIEW-RWB-E1-042-SPEC-012` for revision 12. That review stays as history. |

## Status

**`SPEC_GATE: FAIL`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 0 | |
| Low | 1 | Visible. This is a Low-only failure, so REVIEW_GATE_WARNING applies. Under D-RUN-09 the orchestrator does not accept it |

Revision 12 resolves 161 and 162. The required `## Change Scope Declaration` heading is back on its own line.
S-01 to S-36 form one table. TC-E1-042-04 is a row of its own. The joined `compliance-validation.md` rows are
split. No `||` remains in any of the seven files. No blank line remains inside a table: the same scan finds
S-34 and S-35 in `spec.run10.md`, and the two rev 11 rows in `shared-updates.run10.md`, and finds nothing in
revision 12. The diff confirms that revision 12 changes layout and wording only:

- No SPEC row, CLAR row or TC row changed. TC-03 and TC-04 are the same text, now split.
- The counts are unchanged: 27 SPEC rows, 46 TC rows, and 28 CLAR rows (25 OPEN, 1 RESOLVED, 2 SETTLED).
- The `assumptions.md` and `document-gaps.md` bodies are byte-identical apart from the title and history
  lines.
- The status block in §20 is unchanged.

The one new Low (163) is small, and revision 12's own edits caused it. The row in `compliance-validation.md`
that certifies the layout fix uses an unescaped `|` inside a code span. GFM therefore splits that row into four
cells and drops the end of its evidence. Two citation slips in `gate-response.md` and one long-stale self-check
cell are listed with it. `spec.md` is not affected.

## 1. Earlier findings 161-162: verification

| Finding | Fix required (review 10) | Verdict | Evidence in revision 12 |
|---|---|---|---|
| 161 Joined lines remove a required heading and a test-case row | Heading on its own line; S-34/S-35 inside the table; split TC-03/TC-04; split `compliance-validation.md` row; scan every file for a double pipe and text glued after a row | **Resolved** | `spec.md` lines 69-74: S-33, S-34, S-35 and S-36 are consecutive table rows, line 73 is blank, and line 74 is `## Change Scope Declaration`. The heading list now reads `## 1. Sources`, `## Change Scope Declaration`, `## 3. ...`. The four required headings are present: Change Scope Declaration, Requirement-to-SPEC Logic Coverage, Unit Test Applicability and Clarification Log. Lines 1074-1075 hold TC-03 and TC-04 as separate rows with the header's column count. `compliance-validation.md` lines 26-27 are separate rows. `shared-updates.md` lines 39-40 and 89-90 are now inside their tables, which fixes two blank-line breaks review 10 did not list. A file-wide search finds no double pipe. A column-count check finds one mismatch, which is new (see 163 (a)) |
| 162 Housekeeping and provenance | (a) Row 39: "all", "if any changes", the decisions in order, D-RUN-21 by reference to OPEN-050. (b) Cite or remove the further-round allowance. (c) A-33 in step 3; "once returned" in step 4 | **Resolved** (one cosmetic residue) | (a) Row 39 now reads "all made by the orchestrator" and "if any of them changes", and keeps "OPEN-050 (D-RUN-18 to D-RUN-21)". The order is still D-RUN-18, D-RUN-20, D-RUN-19. D-RUN-20 is labelled "(rev 11, below)", so nobody can miscount, and the failure scenario of 162 (a) is closed. (b) `agent-run-log.md` lines 251-252 now cite "the orchestrator's triage message (not the build-log row, which says only 'Re-gate as review-10')". This matches what the orchestrator states for this review: its message to the specifier allowed one further Low-only round. The statement is accurate and is not attributed to a log row that lacks it. (c) Run 9 step 3 lists A-33. The "Gate (run 9)" section exists (lines 271-277). Run 10 step 4 says "Recorded under 'Gate (run 10)' after the result", which is equivalent to "once returned" |
| Review-10 plan inputs 1-5 | Carry | **Carried** | §12.14 R10-1 to R10-5 (`spec.md` lines 1031-1040). R10-2, the ArchUnit cross-check, is correctly recorded as a plan option, not a requirement. R10-4 says the plan "treats none as ratified" |

## 2. Handling of E43S (revised in parallel)

| Check | Result | Evidence |
|---|---|---|
| Cites the revision it read | Yes | The `spec.md` line 28 note, S-22 and A-28 cite revision 6 "as read in run 8". Run 10's inputs (`agent-run-log.md`, run 10 table) list no new E43S read, so the citation is still a true record. R10-1 says "revision 7 or later at the time of review 10, not read by this run", which is also true. |
| Defers to the revision in force at plan time | Yes | Line 28 ("revision in force re-checked at plan time"), A-28, R8-1, R9-1 and R10-1. |
| State of E43S now | Moved on, as expected | E43S revision 8 (`spec.md` 05:45:08) is "rebased on ... RWB-E1-042 spec revision 10". E43S review 8 (`REVIEW-RWB-E1-043-SPEC-008`, 05:51:43, FAIL 4 Low) checked this spec's revision 11. It found the names E43S consumes unchanged, and it flagged as E43S's own finding 157 that E43S cites this spec's `shared-updates.md` by line number. Revision 12 changes no type, name or contract that E43S consumes. It does move two `shared-updates.md` rows, the rev 11 §1 row (line 41 to 40) and the §4 RWB-E1-037 row (line 91 to 90). It also shifts `spec.md` lines after line 72. Rows 25, 26, 32, 38, 39 and 83 are where they were. This is a plan-time check (plan input 1), not a finding here. |

## 3. D-RUN-18 to D-RUN-21: attribution and ratification

| Check | Result | Evidence |
|---|---|---|
| Credited to the orchestrator | Yes | Unchanged from revision 11. Revision 12 adds "all made by the orchestrator (Claude Code)" (`shared-updates.md` row 39), and `gate-response.md` Round 10 credits the triage message to "The orchestrator's (Claude Code) message". |
| No ratification or human acceptance recorded | Yes | Every added line was searched. Round 10: "No human acceptance or ratification is recorded". R10-4: the plan "treats none as ratified". No added text presents a run decision or a triage as approved by a person. |
| OPEN-050 cited correctly | Yes | `open-items.md` OPEN-050 covers D-RUN-18 to D-RUN-21. Row 39 relies on it. No duplicate register entry is requested. |
| Further-round allowance | Accurately cited | It is cited to the orchestrator's message, not to the build log (162 (b) above). The build log still has no row for review 10 or for this allowance. Recording it there is the orchestrator's task, not the specifier's, so this is not a finding against the spec. |

## 4. New findings

| ID | Severity | Finding |
|---|---|---|
| `REVIEW-RWB-E1-042-163` | Low | Revision 12's own edits leave layout and citation slips. The self-check row that certifies the layout fix splits on an unescaped `\|` inside a code span and loses the end of its evidence. `gate-response.md` Round 10 cites "§18" for the test table, which is §15. Line 3 of that file drops an "and". A self-check cell still names snapshots `*.run2.md` to `*.run7.md` |

### REVIEW-RWB-E1-042-163 (Low): residual layout and citation slips in revision 12's own edits

**Maps to:** `compliance-validation.md` line 91 (finding 161 row) and line 102; `gate-response.md` line 3 and
line 339 (Round 10, row 161); finding 161 ("check every file of the set ... for a table row followed by text");
GFM tables extension (a pipe in cell content must be escaped, including inside a code span).

**Evidence:**

- (a) `compliance-validation.md` line 91 is the "Layout: every table row and heading on its own line (finding
  161)" row. Its evidence ends "checked by a scan for joined `` `|` `` rows and blank lines inside tables". The
  pipe inside the backticks is not escaped. In GitHub Flavored Markdown a table cell ends at an unescaped pipe,
  even inside a code span. So the row has four cells under a three-column header, and GFM drops the extra cell.
  The rendered evidence stops at "checked by a scan for joined" and shows a stray backtick, and the words "rows
  and blank lines inside tables" are lost. Across the 14 files (revision 12 and revision 11), this is the only
  table row with a pipe inside a code span. Revision 12 introduced it.
- (b) `gate-response.md` line 339 (Round 10, finding 161, "Where" column) cites "§18 TC-03/TC-04". The test
  table is `## 15. Test scenarios`, and §18 is "Out of scope". The run log (run 10 step 2) and the spec's own
  revision note do not name a section number, so only this cell is wrong.
- (c) `gate-response.md` line 3 reads "Round 8 SPEC-010 Round 9 SPEC-011 (with D-RUN-20 and D-RUN-21) and Round
  10 SPEC-012". A comma or "and" is missing after "SPEC-010". The slip dates from revision 11, and review 10
  missed it.
- (d) Carried, and not introduced by revision 12: `compliance-validation.md` line 102 says "snapshots
  `*.run2.md` to `*.run7.md`". The folder holds snapshots up to `*.run10.md`, and the cell has been stale since
  revision 9 (`compliance-validation.run8.md` line 88). Line 103 ("Rounds 3 to 7") is stale in the same way,
  because Rounds 8 to 10 also record orchestrator triage.

**Failure scenario:** A reader of the rendered self-check sees the finding-161 evidence cut off after "checked by a
scan for joined". It does not say what the scan checked. That is the row meant to show the layout class is closed.
A reader who follows Round 10's "§18" to find the restored TC-04 row lands in Out of scope.

**Why Low:** No requirement, test, open item, decision or `spec.md` content is affected. All four items are
one-line edits in two of the companion files. Review 10 rated the same class (161, 162) Low, and this finding is
kept consistent with it.

**Fix required:**

- (a) Write the pipe as `` `\|` `` or as the word "pipe" in `compliance-validation.md` line 91.
- (b) Change "§18" to "§15" in `gate-response.md` line 339.
- (c) Insert ", and" (or a comma) after "Round 8 SPEC-010" in line 3.
- (d) Update `compliance-validation.md` lines 102-103 to "`*.run2.md` to `*.run10.md`" and "Rounds 3 to 10".
- Optional: put row 39's decisions in numeric order (D-RUN-18, -19, -20).
- Add a check for unescaped pipes inside code spans to the layout scan.

Because this is the further round the orchestrator allowed, the orchestrator may instead route 163 to the
engagement lead for a human disposition under D-RUN-09. This review does not decide that.

## 5. Plan inputs (not findings)

1. **E43S revision in force and line-number citations.** At plan time E43S is at revision 8 or later. Revision 8
   (05:45:08) is rebased on this spec's revision 10, and E43S review 8 (05:51:43, FAIL 4 Low) checked revision 11.
   Confirm that the revision in force has read revision 11 or later (R10-1). Revision 12 changes no consumed name.
   Confirm also that E43S's GAP-58 and G8-R01 leave the `PARAMETER` dispatcher branch (`ObjectProvider`, 404
   MSG-P4-003) unchanged. Revision 12 moves `shared-updates.md` rows 41 and 91 to lines 40 and 90, and shifts
   `spec.md` lines after line 72. Any cross-story cite should use the section or row ID, not the line number.
2. **Carry R10-2 to R10-5 unchanged.** These are the optional ArchUnit cross-check of the reader-call limit, the
   CLAR-028 dedicated-reader consequence, readiness under `SETTLED` rows that rest on unratified orchestrator
   decisions (OPEN-050), and unit cases for reader-call rules (1) to (6) inside the combined 0.80 bundle.
3. **Clarification readiness.** The status is unchanged: 25 OPEN rows (none blocking), CLAR-020 RESOLVED, and
   CLAR-025 and CLAR-027 SETTLED by D-RUN-21 and D-RUN-20. The plan must name the orchestrator rulings it proceeds
   under. It must not report CLAR-025 or CLAR-027 as `RESOLVED` by a person (R10-4).

## 6. Checks performed

| Check (compliance-reviewer.md) | Result |
|---|---|
| Authentication and authorisation | Unchanged in revision 12. `GET /admin/parameters` goes through `CapabilityCheck` (R). No defect. |
| Customer and account data protection | Unchanged. No field, log line or fixture was added. No defect. |
| Audit logging | Unchanged (AC-VERS; TC-10). No defect. |
| KYC, AML, suitability, consent, approval | Out of scope beyond maker-checker (SPEC-014). |
| Frontend integration and error contract | No frontend (§13). No message ID changed. No defect. |
| Secrets and environment configuration | Unchanged (SPEC-010, TC-44, TC-46). No defect. |
| AC → requirement → test coverage | 57 of 57 rules mapped. AC4's TC-E1-042-04 now renders as a row (161 resolved). TC-01 to TC-46 are unchanged. |
| Required spec structure | All four required headings are present with the exact text. The Change Scope Declaration is restored. |
| 80% gate per changed surface | Unchanged. Backend is REQUIRED, with four counters at 0.80 in one bundle outside `check`. The reader-call rule logic is in that bundle (R10-5). Frontend is `NOT_APPLICABLE`, with evidence. The gate is planned, not measured, which is correct at this stage. |
| Migration rules (D-RCV-28, D-RUN-07) | Unchanged. One `V<seq>__...` file, with no number fixed. |
| Module boundaries (D-RUN-08, -10, -11, -18 to -21) | No new edge, type or cycle. |
| Consistency with E43S | The citation and the deferral are correct (§2). E43S is now at revision 8, so the plan re-checks it (plan input 1). |
| Run-decision attribution and ratification | All credited to the orchestrator. None is ratified. No human acceptance is recorded (§3). |
| Revision 12 limited to layout and wording | Confirmed by full diff of all seven files against `*.run10.md` (§1, Status). |
| Personal data in this run's files | None in the revision 12 changes. The test identities are synthetic. |
| MCP | None connected; N/A. |

## 7. Document-gap candidates

None new. Finding 163 concerns this run's own files. E1042-SP-DG-16, the definition of "module", stays as
recorded with Blocker = No. D-RUN-21 settles it for this build only, pending ratification under OPEN-050. E43S's
G8-R01 on the same AGENTS.md §7 question belongs to E43S and is consistent with E1042-SP-DG-16.

## Gate decision

```text
REVIEW_STATUS: FAIL
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 1] (163)
BLOCKING: NO by severity; not accepted under D-RUN-09 (fix, or route to the engagement lead for a human disposition)
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
EARLIER_FINDINGS: 161, 162 resolved (162 (a): decision order 18, 20, 19 left as is; cosmetic)
REGRESSIONS: 163 (self-check row split by an unescaped pipe in a code span; gate-response "§18" for §15; missing "and"; stale snapshot and round ranges)
REVISION_12_SCOPE: layout and wording only; no SPEC, CLAR or TC row changed; open items 25 (0 blocking); tests TC-E1-042-01 to -46
E43S: revision 6 cited as read in run 8; plan re-checks the revision in force (now revision 8, gated FAIL 4L at 05:51:43)
D_RUN_18_21: credited to the orchestrator (Claude Code); none ratified (OPEN-050); no human acceptance recorded
FURTHER_ROUND_ALLOWANCE: cited to the orchestrator's message; not in the build log (orchestrator to record)
PLAN_INPUTS: 3
DOCUMENT_GAP_CANDIDATES: 0
NEXT_STEP: Orchestrator triage of 163 (one-line fixes in compliance-validation.md and gate-response.md, then spec-gate-review-12.md; or route to the engagement lead for a human disposition under D-RUN-09)
```

SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 1]

# Spec gate review, round 9: RWB-E1-043 (RUN_ID `INC-008-epic-1-RWB-E1-043`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-043-SPEC-009` |
| Gate | Specification gate, round 9 (Compliance Reviewer, bounded review after remediation run 8) |
| Artefacts reviewed | `specify/spec.md` revision 9 (file 2026-11-18 05:58:43), `assumptions.md` revision 9 (A-01..A-46, A-32 withdrawn), `document-gaps.md` revision 9 (GAP-01..GAP-59), `shared-updates.md` revision 9 (R1..R33, §3.1, §3.2), `compliance-validation.md` revision 9, `contracts/backend-apis.json` revision 9, `contracts/frontend-integrations.json` revision 8 (no content change), `gate-response.md` (§11 correction, §12), `agent-run-log.md` (run 8). `spec.run8.md` was diffed against the current spec as the audit trail; the other `*.run8.*` backups were checked for presence and headers. |
| Previous round | `review/spec-gate-review-8.md` (`REVIEW-RWB-E1-043-SPEC-008`, FAIL: 4 Low, findings 155-158, gate gap G8-R01) |
| Sources checked | `AI-SDLC-BUILD-LOG.md` (file 2026-11-18 07:23:54, 334 lines): decisions table lines 41-44 (D-RUN-18..21); timeline rows 301-306, of which row 305 is the RWB-E1-043 triage of 05:52:36 and row 306 the log correction. `aisdlc/docs/open-items.md` OPEN-050. RWB-E1-042 `specify/`: `spec.md` revision 13 (file 06:01:50) and the kept revision 12 (`spec.run11.md`, file 05:57:12); `assumptions.md` A-51; `shared-updates.md` and `shared-updates.run11.md`. RWB-TE-001 spec v4. Story file v7 RWB-E1-043. `AGENTS.md` §2, §3.1, §7, §9. `specification-execution-gates.md`; `pdlc.md`. All read only. |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18. No question asked (L-RCV-03). No file other than this review was written. |

**About the run rulings.** D-RUN-09, D-RUN-18, D-RUN-19, D-RUN-20, D-RUN-21 and the triage of
2026-11-18 05:52:36 were given by the orchestrator (Claude Code), an AI agent. They are not human
decisions, acceptance or ratification, and this review does not treat them as such. A search of every
reviewed artefact for ratification, acceptance, approval and "settled" wording found only disclaimers
or explicitly qualified statements. The spec says "No tech-lead approval is claimed"
(spec.md:83), A-46 and GAP-58 say the ruling is "not a human decision" with ratification under
OPEN-050, and R22 says "No tech-lead approval is claimed".

## Status

**`SPEC_GATE: FAIL`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 0 | |
| Low | 2 | Visible; do not block by severity; not accepted under D-RUN-09 without an orchestrator triage or a human disposition |

Findings 155-157 are closed with no new design defect. Finding 158 is closed in substance: the spec
now cites the 05:52:36 triage that does state the run-8 allowance. Two Low defects remain, both
citation defects in revision-9 text: the triage row is cited as build-log line 304 when it is line 305
(159), and the RWB-E1-042 line cites are pinned to revision 12 while the live file has moved to
revision 13, with R6 recording no revision-13 check (160). GAP-59 is recorded correctly (M,
Blocker = No, OPEN-050). D-RUN-21 is applied to plan routing correctly. No human ratification or
approval is claimed.

## Round-8 findings: resolution check

| Round-8 ID | Sev | Verdict | Evidence checked |
|---|---|---|---|
| 155 D-RUN-21 not applied to plan routing | Low | **Resolved** | The Module scope row (spec.md:83), A-24 (assumptions.md:38), R22 (shared-updates.md:92), CHANGE_CLASSIFICATION_SUMMARY (spec.md:1184) and compliance-validation (line 16, §3 lines 71-73) all cite D-RUN-21 (decisions table line 44, 05:36; ratification open, OPEN-050) and state the ACE-module reading: "touches one module" means the ACE module (recovery); this P3 + P4 plan changes neither the common nor the collection module; the rule sends nothing to the analyst; the plan gate checks the reading; no tech-lead approval is claimed. The prior "AGENTS §7 still sends a plan that touches two modules back to the analyst" sentence is gone. GAP-59 records the source-level definition gap. |
| 156 GAP-58 over-reads D-RUN-18 | Low | **Resolved** | GAP-58 quotes D-RUN-18 exactly ("P1 (RWB-E1-001) and P3 (RWB-E1-042) handlers implement it") and says neither D-RUN-18 nor D-RUN-20 names RWB-E1-019. Its support is SPEC-019, SPEC-025, TE001 SPEC-022 (d) and Story v7 RWB-E1-019 lines 18 and 261, plus the orchestrator's R33 answer. A-46, the SPEC-019 later-edge row, the SPEC-025 QUEUE paragraph, R24 and the contract `p4HandlerSpi.implementedBy` say the same. No "D-RUN-18 (P3 handlers implement the SPI)" claim remains. |
| 157 Re-baseline covered only `spec.md` | Low | **Resolved for the named revision; live source has moved (see 160)** | The §0 E42S row names revision 12 and all three files with times (05:50:36; 05:50:52 for `assumptions.md` and `shared-updates.md`). All seven `spec.md` line cites were checked against the kept revision 12 (`spec.run11.md`) and are correct: §4.3 line 147, business-date seam line 153, §12.12 T-2 line 982, §12.14 R7-1 line 1006, R7-3 line 1008, CLAR-025 line 1198, CLAR-027 line 1200. A-51 exists. The `shared-updates.md` line cites 25, 26, 32, 34, 38, 39 and 84 were checked against `shared-updates.run11.md` and are correct. R6 says "RWB-E1-043 revision 9 is baselined on its revision 12". The fix is structurally complete; the live file has since become revision 13, which 160 addresses. |
| 158 Allowance cited to a row that does not say it | Low | **Resolved in substance; line number wrong (159)** | The front matter and §0 BLOG tag now cite the orchestrator's triage of 2026-11-18 05:52:36, which does state "Each triage message allows one further Low-only round". The 05:32 claim is corrected in `gate-response.md` §11 and §12 and in `agent-run-log.md` run 8. But the cited build-log line 304 is the round-8 gate row; the triage row is line 305 (findings 159). |

### D-RUN-21 plan routing: verified

| Claim in revision 9 | Checked against | Result |
|---|---|---|
| D-RUN-21 is logged at decisions table line 44, 05:36; "touches one module" in AGENTS.md §7 and §9 means the ACE module (recovery); a plan that changes the common or collection module still goes back to the analyst unless the story file names it; tech-lead ratification is open | Build log line 44; OPEN-050 (ratify or replace D-RUN-18..21 and define "module") | Correct, word for word in substance |
| The story's plan is P3 `casewf.refdata` plus P4 published types and grants rows, all inside the recovery ACE module; no common or collection change | spec.md:79, 83; TE001 SPEC-022 (d); A-24 | Correct; the P4 `access` package and the P3 registry are both in `th.co.scb.ace.demo.recovery` |
| Under D-RUN-21 the rule sends nothing to the analyst; the plan gate checks that reading (R22); no tech-lead approval is claimed | spec.md:83, 1184; assumptions.md:38; shared-updates.md:92; compliance-validation.md:16, 71-73; GAP-59 | Correct; every occurrence carries the qualification and OPEN-050 |
| The source-level definition gap is recorded, not hidden | GAP-59 (document-gaps.md:88), with cross-references to RWB-E1-042 E1042-SP-DG-16 and RWB-TE-001 PG-04/GC-1 | Correct; Blocker = No; no new `DOCUMENT-GAPS.md` entry is claimed |

### GAP-59: verified

GAP-59 is row 88 of `document-gaps.md`: type M, "Module" undefined in AGENTS.md §7 and §9, second
sources AGENTS.md §2 and §3.1 plus D-RUN-21, **Blocker = No**, why "Settled for this build by D-RUN-21,
pending OPEN-050: the plan touches only the recovery ACE module, with no common or collection change
(A-24; R22)", and how "AGENTS.md owner (solution architect with the TechX tech leads) to define
'module'; before the RWB-E1-043 plan gate". The row cites OPEN-050 twice (second source and why). It is
recorded as a cross-reference to RWB-E1-042 E1042-SP-DG-16 and RWB-TE-001 PG-04/GC-1, not as a new
`DOCUMENT-GAPS.md` entry. Counts are consistent: 59 gaps (40 C, 19 M), none a blocker; 46 assumptions
(A-32 withdrawn); `CLARIFICATION_STATUS` says 59 gaps and 0 blockers.

### No human ratification or approval: verified

| Place | Statement checked | Result |
|---|---|---|
| spec.md:8, 23-24, 51, 1144-1148 | All triage and rulings are the orchestrator's (Claude Code, an AI agent); none is a human decision; D-RUN-21 ratification open, OPEN-050 | Correct; no claim of ratification |
| spec.md:1124-1133 | Owner acceptance list: "None has been accepted" | Correct; no owner acceptance claimed |
| assumptions.md:9-11, 60 (A-46) | No assumption accepted; no ruling ratified; A-46 is an orchestrator ruling, not a human decision; OPEN-050 | Correct |
| document-gaps.md:7-9, 87-88 | Rulings are the orchestrator's, not human; GAP-57/GAP-58/GAP-59 settled for the build, pending ratification | Correct |
| shared-updates.md:5-6, 71, 92, 103 | R1 ratification request; R22 "No tech-lead approval is claimed"; R33 ratification with OPEN-050 | Correct |
| compliance-validation.md:28, 64-66, 72 | No ratification or acceptance claimed; D-RUN-18, D-RUN-20, D-RUN-21 and OPEN-050 named | Correct in the spec text; the self-check list omits D-RUN-19..21 (observation 4, not a finding) |
| gate-response.md §12 | Triage is the orchestrator's, not human acceptance or ratification | Correct |

## What holds (verified)

- The run-8 diff touches only the revision headers, §0 E42S and BLOG rows, the Module scope row, the P2
  precondition text, SPEC-019 (later-edge row and T-TE001-14 line refs), SPEC-020/025/026 revision
  refs, the SPEC-025 QUEUE paragraph, the owner-acceptance list, CLAR-019, the closing status lines,
  A-24, A-25, A-46, GAP-51, GAP-57, GAP-58, GAP-59, R1, R6, R22, R24, R29, R32, R33, row 008, the
  INDEX and OPEN-036 notes, compliance-validation and the contract revision. No run-8 edit reopens
  findings 138-154.
- Check order L1-L15, maker-checker, the append-only trigger, message pass-through, the 403 action
  texts, flag-off start-up and the SPI signature are unchanged. TC-TM-05 steps (a)-(h) are unchanged.
- Counts verified: 46 assumption rows (A-01..A-46, A-32 withdrawn); 59 gaps (40 C, 19 M, 0 blockers);
  49 COVERED rows; 16 requirement lines owned elsewhere; CONTRADICTIONS 40, equal to the C count.
- GAP-57/D-RUN-20 remains applied to the `PARAMETER` route, R24 and R32; GAP-58/the R33 answer is
  applied to SPEC-019, SPEC-025, A-46 and the contract; D-RUN-18 and D-RUN-19 edges remain as
  before.
- Every message ID used exists in Error and Message Standard v4; revision 9 adds no message ID.
- No business value, role or threshold is a literal. No personal data, secret or production data
  appears; test codes (`test_current`, `test_current_2`) and dates are synthetic.
- Frontend `NOT_APPLICABLE` (contract revision 8, no content change); the 80% backend unit-test gate
  stays planned. Both contract files parse as JSON.
- No module edge points into P3 from another module; P4 refers to no P1 or P3 type; no cycle.
- The RWB-E1-001 handler contract is complete: check order, what the handler supplies, message
  pass-through, repeat behaviour (GAP-56) and effective date (including the MSG-P3-015 case from
  finding 154) are unchanged from revision 8.

## Observations (no finding)

1. **Build-log line numbers are not stable.** The timeline has been reflowed between earlier snapshots
   (review 8 cited D-RUN-21 at line 300; it is line 295 now), and row 306 was added after the triage.
   The durable citation is the timestamp or the row's stage/result, not a line number. This is the
   cause of 159.
2. **RWB-E1-042 revision 13 cites this story at revision 8.** Its front matter says it "re-baselines
   E43S citations on its revision 8" (05:45:08), while this story is at revision 9. The names this
   story consumes are unchanged through revision 13, so no design impact; the RWB-E1-042 gate should
   reconcile its cross-story cites.
3. **The increment card is stale.** `aisdlc/docs/increments/INC-008-epic-1-RWB-E1-043.md` still shows
   "Compliance review PASS (2026-11-10)" and "Specification SUCCESS — 10 Nov 2026". The orchestrator's
   shared-update pass should refresh the card; this is not a spec finding.
4. **Self-check list incomplete.** `compliance-validation.md:28` lists D-RUN-08, -10, -11, -12, -18 and
   the 2026-11-18 triage as not ratified but omits D-RUN-19..21, although the spec text qualifies
   them. The claim itself remains true; align the row when 159/160 are edited.
5. **`(R6)` is not a check record.** The E42S row's "A later revision (for example 13) is checked by
   name only (R6)" points to a shared-update row that asks RWB-E1-042 to keep names stable, not to a
   recorded revision-13 check. This is part of 160.

## Findings

### Low

| ID | Severity | Finding | Evidence | Affected | Fix required |
|---|---|---|---|---|---|
| `REVIEW-RWB-E1-043-159` | Low | **The 05:52:36 triage row is cited as build-log line 304; it is line 305.** In the file as reviewed (334 lines, 2026-11-18 07:23:54), line 304 is the RWB-E1-043 "Spec gate (round 8)" row; line 305 is the "Gate triage" row that says "Run 8 (rev 9): 155-158 ... R33 answer: a P3 handler may implement the P4 SPI ... Each triage message allows one further Low-only round; this row states that so the allowance can be cited". The timestamp is right and the content is right; only the line number is wrong. The same line-304 cite appears in the front matter, the §0 BLOG row, SPEC-025 QUEUE paragraph, A-46, GAP-58, R33, `gate-response.md` §11/§12 and `agent-run-log.md`; `agent-run-log.md` also gives the range "300-305" and the log correction at 306. This is the same class of defect as 158. | `AI-SDLC-BUILD-LOG.md` lines 304-306 (line 305 triage, line 306 log correction); spec.md:8, 51, 737; assumptions.md:60; document-gaps.md:87; shared-updates.md:103; gate-response.md:342, 375, 386; agent-run-log.md:381, 391-392 | spec front matter; §0 BLOG; SPEC-025 QUEUE paragraph; A-46; GAP-58; R33; `gate-response.md` §11/§12; `agent-run-log.md` run 8 | Cite line 305 (or, durably, "triage row of 2026-11-18 05:52:36"), and correct the "300-305" range to "300-306". No design text changes. |
| `REVIEW-RWB-E1-043-160` | Low | **The E42S line cites are pinned to revision 12, but the live RWB-E1-042 `spec.md` is revision 13 and the line numbers have moved.** Revision 13 was written at 06:01:50, after this spec's 05:58:43 run. In the live file, line 147 is a table separator, not the §4.3 seam row (now 148); the business-date seam is line 154 (cited 153); T-2 is 983 (cited 982); R7-1 is 1007 (cited 1006); R7-3 is 1009 (cited 1008); CLAR-025 is 1207 (cited 1198); CLAR-027 is 1209 (cited 1200). The §0 E42S row says a later revision "is checked by name only (R6)", but R6 records no revision-13 check and does not name the kept revision-12 copy (`spec.run11.md`). A planner who follows the live path and line numbers reads the wrong rows; the names this story consumes are unchanged. The revision-12 cites were correct when written (157 is resolved for that revision); the defect is the missing durable pointer after the source moved. | E42S `spec.md` revision 13, file 06:01:50, front matter and lines 148, 154, 983, 1007, 1009, 1207, 1209; kept revision 12 `spec.run11.md` lines 147, 153, 982, 1006, 1008, 1198, 1200; spec.md:46; shared-updates.md:76 (R6) | §0 E42S row; A-25; R6; SPEC-019 T-TE001-14 bullet; SPEC-025 PARAMETER paragraph; GAP-51; compliance-validation; backend contract | Name `spec.run11.md` (revision 12) for the line cites, or cite by section/row ID (which the E42S triage of 05:57:05 itself asks for cross-story cites). Record the revision-13 name check in R6. No design text changes. |

## Gate gaps (document and decision gaps not recorded by the specify stage)

**None new.** G8-R01 is closed as GAP-59 (M, Blocker = No), recorded with OPEN-050 and cross-referenced
to RWB-E1-042 E1042-SP-DG-16 and RWB-TE-001 PG-04/GC-1. GAP-59 is the only gap this review needed to
check; its type and Blocker value are consistent with the gap table and the closing status lines. No
new document or decision gap was found in revision 9.

## RWB-E1-001 handler contract: completeness

| Point | Judgement | Where |
|---|---|---|
| Check order | Complete, unchanged. L1-L15. | SPEC-025; §3.1 item 3 |
| What the handler supplies | Complete, unchanged. | SPEC-025; §3.1 item 2 |
| Message pass-through | Complete. | SPEC-025; §3.1 item 4 |
| Repeat behaviour | Complete; order departure recorded (GAP-56). | SPEC-025 L9; §3.1 items 3, 7 |
| Effective date | Complete, including the MSG-P3-015 case (154 closed). | SPEC-008, 024, 025, 032 rule 6; A-42; TC-TM-05 |
| SPI home | D-RUN-18 and D-RUN-20, both pending tech-lead ratification (R24, OPEN-050). RWB-E1-001 is a P1 handler outside the registry's module, so D-RUN-20 confirms it uses the SPI. | SPEC-019, 025 |

RWB-E1-001 can conform to this contract. None of 159-160 changes the SPI signature, the check order or
what RWB-E1-001 supplies.

## Gate decision

There is no Critical, High or Medium finding, so nothing blocks the handoff by severity (`pdlc.md`).
The review status stays `FAIL`. Under D-RUN-09 the orchestrator does not accept a Low-only failure, so
159 and 160 go to the orchestrator for triage, or to the engagement lead for a human disposition. Both
are local citation edits: the build-log line number, and the revision-12 kept-copy pointer plus the R6
check. They change no design, contract, interface or test. G8-R01 is closed as GAP-59, Blocker = No, and
D-RUN-21 is applied to plan routing without a ratification claim. OPEN-050 remains open before the plan
gate.

REVIEW_STATUS: FAIL
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2] (159, 160)
BLOCKING: NO by severity; not accepted under D-RUN-09 (orchestrator triage or human disposition)
ROUND_8_FINDINGS: 155 resolved; 156 resolved; 157 resolved for revision 12 (160 on the live revision 13); 158 resolved in substance (159 on the line number)
G8_R01: recorded as GAP-59 (M, Blocker No), cites OPEN-050, cross-references E1042-SP-DG-16 and PG-04/GC-1
D_RUN_21: applied to plan routing (Module scope, A-24, R22, summary, compliance-validation); no tech-lead approval claimed
GAP_59: Blocker No; OPEN-050 cited; counts 59 gaps (40 C, 19 M, 0 blockers)
RATIFICATION_CLAIMS: none found
RWB_E1_001_CONTRACT: COMPLETE
DOCUMENT_GAPS_ADDED: 0 (G8-R01 closed as GAP-59)
NEXT_STEP: Orchestrator triage of 159-160 (or engagement-lead disposition under D-RUN-09), then plan gate; OPEN-050 remains
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]

# Spec gate review, round 8: RWB-E1-043 (RUN_ID `INC-008-epic-1-RWB-E1-043`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-043-SPEC-008` |
| Gate | Specification gate, round 8 (Compliance Reviewer, bounded review after remediation run 7) |
| Artefacts reviewed | `specify/spec.md` revision 8 (file 2026-11-18 05:45:08), `assumptions.md` revision 8 (A-01..A-46, A-32 withdrawn), `document-gaps.md` revision 8 (GAP-01..GAP-58), `shared-updates.md` revision 8 (R1..R33, §3.1, §3.2), `compliance-validation.md` revision 8, `contracts/backend-apis.json` revision 8, `contracts/frontend-integrations.json` revision 7 (no content change), `gate-response.md` (§9.1 row 147 extended, §11 new), `agent-run-log.md` (run 7). The `*.run7.*` files were diffed against the current files as the audit trail. |
| Previous round | `review/spec-gate-review-7.md` (`REVIEW-RWB-E1-043-SPEC-007`, FAIL: 2 Low, findings 153-154, gate gap G7-R01) |
| Sources checked | `AI-SDLC-BUILD-LOG.md` (file 2026-11-18 05:37:02): decisions table lines 41 (D-RUN-18), 42 (D-RUN-19), 43 (D-RUN-20), 44 (D-RUN-21); timeline rows 277 (RWB-E1-043 triage 05:32:00), the RWB-TE-012 triage of 05:32:32, 288 (D-RUN-20) and 300 (D-RUN-21, OPEN-050). RWB-E1-042 `specify/`: `spec.md` revision 11 (05:41:44) diffed against `spec.run9.md` (revision 10, 05:35:12); `assumptions.md` (05:41:44) against `assumptions.run9.md`; `shared-updates.md` (05:41:20) against `shared-updates.run9.md`. `aisdlc/docs/open-items.md` OPEN-050. All read only. |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18. No question asked (L-RCV-03). No file other than this review was written. |

**About the run rulings.** D-RUN-09, D-RUN-18, D-RUN-19, D-RUN-20, D-RUN-21 and every triage were given by
the orchestrator (Claude Code), an AI agent. They are not human decisions, acceptance or ratification, and
this review does not treat them as such. A search of every reviewed artefact for ratification, acceptance
and "settled" wording found no text that presents a run ruling or a triage as human-ratified or accepted.
Revision 8 qualifies D-RUN-20 as "ratification by the recovery tech lead is an open item" (spec SPEC-025,
§0 BLOG row, owner-acceptance list; GAP-57; R24; R32) and `gate-response.md` §11 states "neither is human
acceptance or ratification". The bare phrase "(settled by D-RUN-20)" in `shared-updates.md` line 198 names
the AI ruling and claims no human act; the same row family carries the qualifier elsewhere.

## Status

**`SPEC_GATE: FAIL`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 0 | |
| Low | 4 | Visible; do not block by severity; not accepted under D-RUN-09 without an orchestrator triage or a human disposition |

Findings 153 and 154 are closed with no new defect in the design. G7-R01 is recorded correctly (GAP-58,
A-46, R33). D-RUN-20 is applied to GAP-57, R24 and R32 with correct quotes and attribution. The four new Lows
are citation and housekeeping defects: D-RUN-21 (logged before this revision and read by the specifier) is
not reflected where the spec still routes the plan to the analyst (155); GAP-58 cites D-RUN-18 for a
point D-RUN-18 does not make (156); the re-baseline note covers `spec.md` but not the RWB-E1-042
`assumptions.md` and `shared-updates.md` cites, and R6 still names revision 7 (157); the "one more round"
authority is cited to a logged triage row that does not contain it (158).

## Round-7 findings: resolution check

| Round-7 ID | Sev | Verdict | Evidence checked |
|---|---|---|---|
| 153 "all code in P3" premise | Low | **Resolved** | SPEC-019 (spec.md:424-426) now says the code is in P3 `casewf.refdata` "except the P4 additions of SPEC-002 (`access.api.ListOfValuesReader`, `access.internal.LovValueReader`) and SPEC-025 (the handler SPI types)". D-RUN-19 point (1) (spec.md:481-484) covers both halves: P3 code reads through `casewf.config.api`; the P4 additions read no catalog parameter. This is true: SPEC-002 has `LovValueReader` read `lov_value` only (spec.md:246-247), and the SPI types refer only to JDK types and each other (spec.md:440-441). CLAR-019 and CHANGE_CLASSIFICATION_SUMMARY (spec.md:1184) were aligned. `gate-response.md` §11.1 states that it corrects the §10.1 D-RUN-19 row instead of editing that history, which is acceptable. Residual wording at spec.md:82 and A-24 is an observation (below). |
| 154 MSG-P3-015 case of a same-day correction | Low | **Resolved** | SPEC-025 *Effective date* (spec.md:697-702), SPEC-032 rule 6 (spec.md:926-927), A-42, the contract `handlerContract.effectiveDate` and `gate-response.md` §9.1 row 147 now carry "an earlier approved version exists; otherwise ... 409 MSG-P3-015". MSG-P3-015 is in Message Standard v4 (spec.md:508, "no earlier version of {table}"); SPEC-024 rule 6 (spec.md:550) and the state table (spec.md:964) agree. TC-TM-05 adds (g) and (h); walked below. "Proved with TC-TM-05 steps (a)-(h)" now matches what the steps test. |

### TC-TM-05 steps (g) and (h): walked against SPEC-006, SPEC-008, SPEC-024 and the check order

| Step | Check | Result |
|---|---|---|
| (g) load v6, `validFrom` 2026-12-06 on business date 2026-12-06 | L9 skipped (no repeat message); L10 `validFrom` = business date passes (SPEC-005, A-05); L11 no same hash, and no APPROVED version for 2026-12-06 (v3 is ROLLED_BACK, v4 VALIDATED for 12-05) | VALIDATED |
| (g) approve v6 | SPEC-008: not author (test fixture), VALIDATED, `validFrom` not before the business date (A-17), no APPROVED twin, `CURRENT_STATE` and `validFrom` not after the business date | APPROVED, `apply` called |
| (g) roll back v6 | SPEC-024 rule 5: no later APPROVED version; rule 6: earlier APPROVED versions v1 and v2 exist; restored version = APPROVED with greatest earlier `valid_from` = v2 (v3 is ROLLED_BACK) | ROLLED_BACK, `onRolledBack` writes v2's rows, as stated |
| (g) load and approve corrected v7, `validFrom` 2026-12-06 | L11: different hash; the partial unique index `(table_code, valid_from) WHERE status = 'APPROVED'` (spec.md:224-225) no longer holds v6 | APPROVED, table holds v7's values, as stated |
| (h) roll back w1, the only approved version of `test_current_2` | Rule 5 passes; rule 6: no earlier APPROVED version | 409 MSG-P3-015, nothing written, as stated |

Every step can run in sequence. The labels v5, v6 and v7 are names, not `version_no` values (observation 2).

### Orchestrator note: D-RUN-20 applied to GAP-57, R24 and R32: verified

| Claim | Checked against | Result |
|---|---|---|
| D-RUN-20 is logged 2026-11-18 05:34 at decisions table line 43; the P4 SPI is "for handlers that live outside the registry's module"; `PARAMETER` is "served by a dispatcher branch of the RWB-E1-043 registry that calls `casewf.config.api` inside P3"; ratification joins the D-RUN-18/19 open item | Build log line 43 and timeline row 288 ("closes E1-042 CLAR-027 and E1-043 GAP-57") | Correct, word for word |
| GAP-57 Blocker = No, "Settled for the build by D-RUN-20 ... pending tech-lead ratification" | Line 43; OPEN-050 | Correct; no human act claimed |
| R24 retitled "settled by D-RUN-18 and D-RUN-20, pending ratification"; still quotes D-RUN-18 exactly; rejection reopens GAP-57 too | Lines 41, 43 | Correct |
| R32 "answered by D-RUN-20, pending tech-lead ratification. ... Nothing is left to ask" | Line 43; review 7 observation 1 | Correct |
| SPEC-025 `PARAMETER` paragraph, SPEC-019 point (4), §0 BLOG row, owner-acceptance list, contract `source` and `implementedBy` | Line 43 | Correct and consistently qualified |

### Orchestrator note: re-baseline on RWB-E1-042: verified, with one defect

| Claim in revision 8 | Checked against | Result |
|---|---|---|
| RWB-E1-042 revision 11 is `spec.md` written 05:41:44; revision 10 is kept there as `spec.run9.md` | File times; revision 11 front matter ("previous: spec.run9.md (revision 10 ...)") | Correct |
| The names used here are unchanged in revision 11 | Full diff `spec.run9.md` → `spec.md`: no change to `MessageResolver`, `CapabilityCheck`, `ApiProblemException`, `ParameterKeys.byName`, `ParameterLoadHandler`, `BusinessDateProvider`, `CatalogParameterReader`, §12.12 T-2 or TC-45 (T-TE001-14 set) | Correct |
| The `PARAMETER` route row is now line 146; R7-1 is line 1005; CLAR-027 is settled by D-RUN-20 | Revision 11 lines 146, 1005, 1188 | Correct |
| A-51 "(file 2026-11-18 05:27:34)" and RWB-E1-042 `shared-updates.md` rows at lines 25, 26, 32, 38, 39 and 83 | `assumptions.md` is now 05:41:44 (A-51 gained D-RUN-20 as a source); `shared-updates.md` is now 05:41:20 with a new row at line 41, so line 83 is now a different row | Stale; see 157 |
| `shared-updates.md` R6 | R6 (line 76) still says "RWB-E1-043 revision 7 is baselined on its revision 10" | Stale; see 157 |

Revision 11 also adds R9-1 (RWB-E1-043 to have re-read RWB-E1-042 at revision 11), R9-2 / CLAR-028 (RWB-E1-037
per-table approver keys cannot be read with a computed key outside P3) and applies D-RUN-21 to its CLAR-025.
R9-1 is met in substance: the run-7 log records the revision-11 check. CLAR-028 asks nothing of this story,
whose P3 registry reads `rwb.refload.approver.<code>` by name through `casewf.config.api` (A-26). D-RUN-21
is the subject of 155.

### What holds (verified)

- The run-7 diff touches only the revision headers, §0 E42S and BLOG rows, SPEC-019 (scope sentence,
  later-edge row, D-RUN-19 points (1) and (4)), SPEC-025 (`PARAMETER` paragraph, *Effective date*, QUEUE
  paragraph), SPEC-032 rule 6, TC-TM-05, the owner-acceptance list, CLAR-019, the closing status lines,
  A-25, A-42, A-46 (new), GAP-57, GAP-58 (new), the document-gaps header, R1, R24, R32, R33 (new), row 008,
  the INDEX and OPEN-036 notes, compliance-validation §2-§3, the contract `revision`, `source`,
  `implementedBy` and `effectiveDate`, and `gate-response.md` §9.1 row 147 and §11. No run-7 edit reopens
  findings 1-154. Check order L1-L15, maker-checker, the append-only trigger, message pass-through, the 403
  action texts, flag-off start-up and the SPI signature are unchanged.
- Counts verified: 46 assumption rows (A-01..A-46, A-32 withdrawn); 58 gaps, 40 C and 18 M, none a blocker;
  49 COVERED rows; CONTRADICTIONS 40, equal to the C count; `CLARIFICATION_STATUS` `[ASSUMPTIONS: 46]
  [GAPS: 58, BLOCKERS: 0]`. Stale totals in `gate-response.md` lines 292, 299 and 324 and
  `agent-run-log.md` line 280 belong to earlier rounds and are history.
- G7-R01 is recorded as GAP-58 (C, Blocker = No) with interim A-46, labelled **Inferred**, and R33 to the
  orchestrator before the plan gate. A-46's quote of D-RUN-20 is exact. The SPEC-019 later-edge row, the
  SPEC-025 QUEUE paragraph and the contract `implementedBy` all point to A-46, GAP-58 and R33.
- Every message ID used exists in Error and Message Standard v4; no new message ID.
- No business value, role or threshold is a literal. No personal data, secret or production data appears;
  test codes (`test_current`, `test_current_2`) and dates are synthetic.
- Frontend `NOT_APPLICABLE` (contract revision 7, no content change); the 80% backend unit-test gate stays
  planned. Both contract files parse as JSON.
- No module edge points into P3 from another module; P4 refers to no P1 or P3 type; no cycle.

### Observations (no finding)

1. **Residual "all code in P3" wording.** spec.md:82 (Change Scope Declaration) and A-24 still open with "All
   story code is in P3", then list the P4 additions in the next sentence. The meaning is clear, so this is not
   a finding. Align them with SPEC-019 when 155 edits the same row and assumption.
2. **TC-TM-05 labels.** `version_no` is max + 1 per table (SPEC-007), and the refused load in (d) writes
   nothing, so "v6" and "v7" in (g) are stored as version 5 and 6. If the test asserts `version_no`, use the
   stored numbers; otherwise rename the labels.
3. **No logged triage of round 7.** The build log was last written at 05:37:02, before review 7 (05:40), and
   holds no RWB-E1-043 row after line 277. The run-8 outcome needs its own timeline row (see 158).

## Findings

### Low

| ID | Severity | Finding | Evidence | Affected | Fix required |
|---|---|---|---|---|---|
| `REVIEW-RWB-E1-043-155` | Low | **D-RUN-21 is not reflected where the spec routes the plan to the analyst.** D-RUN-21 (decisions table line 44, 05:36) rules that "touches one module" in AGENTS.md §7 and §9 means the ACE module (recovery), so a plan that touches only the recovery module passes that check. It was logged before this revision (05:45) and the run-7 log records reading it, with the note "plan-stage one-module rule; no change to this spec". The spec does carry that rule: the Change Scope row says "AGENTS §7 still sends a plan that touches two modules back to the analyst; the plan gate must take that decision". A-24, R22, CHANGE_CLASSIFICATION_SUMMARY ("two-module plan-gate decision") and compliance-validation (row "Change Scope Declaration" and §3) say the same. RWB-E1-042 revision 11 applied D-RUN-21 to the same question (CLAR-025 settled, R7-3, R9-3), so the two specs now disagree on plan routing for the same P3 + P4 shape. | spec.md:82, 1184; assumptions.md:38 (A-24); shared-updates.md:92 (R22); compliance-validation.md:16, 70-72; agent-run-log.md:343-344; build log lines 44, 300; E42S revision 11 lines 555, 1007, 1186 | Change Scope Declaration; A-24; R22; CHANGE_CLASSIFICATION_SUMMARY; compliance-validation; §0 BLOG row; R1 | Cite D-RUN-21 (orchestrator run decision, 2026-11-18 05:36; tech-lead ratification open, OPEN-050) in the Change Scope row, A-24, R22 and the summary line. State that under D-RUN-21 this recovery-only P3 + P4 plan does not go back to the analyst under AGENTS §7, that it changes neither the common nor the collection module, and that no tech-lead approval is claimed. Turn R22 into a plan-gate check of that reading. Add D-RUN-21 to the §0 BLOG row and to the "also listed" rulings of R1. Point to the source-level definition gap (G8-R01). |
| `REVIEW-RWB-E1-043-156` | Low | **GAP-58 cites D-RUN-18 for a point it does not make.** GAP-58's second-source column reads "D-RUN-18 (P3 handlers implement the SPI)". D-RUN-18's words are "P1 (RWB-E1-001) and P3 (RWB-E1-042) handlers implement it". The only P3 handler it names is RWB-E1-042's `PARAMETER`, which D-RUN-20 and this spec say is not an SPI handler. D-RUN-18 says nothing about RWB-E1-019, so it gives no support for RWB-E1-019's P3 handlers implementing the SPI. This is the same kind of misquote as finding 152. R24 (line 94) quotes the ruling correctly. | document-gaps.md:86 (GAP-58); build log line 41; spec-gate-review-6.md finding 152 | GAP-58; A-46 source column (cites D-RUN-18 without a claim, so no change is needed there) | In GAP-58, quote D-RUN-18 exactly ("P1 (RWB-E1-001) and P3 (RWB-E1-042) handlers implement it"). Add that neither D-RUN-18 nor D-RUN-20 names RWB-E1-019, and that the support for P3 handlers on the SPI is this spec's SPEC-019 and SPEC-025 with TE001 SPEC-022 (d) and Story v7 RWB-E1-019 line 261. |
| `REVIEW-RWB-E1-043-157` | Low | **The re-baseline note covers only `spec.md`.** The §0 E42S row now says revision 10 is kept as `spec.run9.md` and that the line cites are revision 10's, but it still points to the live paths. It cites A-51 with "(file 2026-11-18 05:27:34)" and the RWB-E1-042 `shared-updates.md` rows "at lines 25, 26, 32, 38, 39 and 83". Both files were rewritten for revision 11: `assumptions.md` at 05:41:44 (A-51 gained D-RUN-20 as a source; revision 10 is `assumptions.run9.md`) and `shared-updates.md` at 05:41:20, with a new row at line 41, so live line 83 is now the "(rev 6)" RWB-TE-001 row instead of the revision-9 T-TE001-14 row (revision 10 is `shared-updates.run9.md`). Also, R6, the row that tells RWB-E1-042 the baseline, still says "RWB-E1-043 revision 7 is baselined on its revision 10" and does not mention the revision-11 check. A planner who follows the cites reads the wrong row. | spec.md:45 (E42S row); shared-updates.md:76 (R6); E42S `assumptions.md` and `shared-updates.md` file times; diff of E42S `shared-updates.run9.md` → `shared-updates.md` (new line 41; line 83 shifted) | §0 E42S row; R6; A-25 source column | In the E42S row, name the revision-10 copies used for line cites: `spec.run9.md`, `assumptions.run9.md` (A-51) and `shared-updates.run9.md` (lines 25, 26, 32, 38, 39, 83). Alternatively, re-cite revision 11 (A-51; `shared-updates.md` lines 25, 26, 32, 38, 39, 84). Update R6 to "revision 8 is baselined on its revision 10; revision 11 (05:41:44) checked, names unchanged". |
| `REVIEW-RWB-E1-043-158` | Low | **The authority for run 7 is cited to a log row that does not say it.** The spec header says "one more round allowed by the orchestrator's triage of 2026-11-18 05:32 (D-RUN-09)". `gate-response.md` §11 says the orchestrator "allowed one more round on Lows in its triage logged at 2026-11-18 05:32", and §11.2 says "Per the orchestrator's triage, no further remediation round follows it in this run". The logged RWB-E1-043 triage (build log line 277, 05:32:00) reads only "Run 6 (rev 7): 151 and 152 as the gate states; re-baseline ...; re-gate as review-7". It allows no further round and limits none. The RWB-TE-012 triage logged a few seconds later does say "one further Low-only round allowed", which shows the wording was not given for RWB-E1-043. No RWB-E1-043 triage of round 7 is logged. The instruction may have reached the specifier directly, but the cited record does not contain it. | spec.md:8; gate-response.md:340-343, 360-361; agent-run-log.md:336-338; build log line 277 and the RWB-TE-012 triage row of 05:32:32; build log file time 05:37:02 | spec front matter; `gate-response.md` §11, §11.2; `agent-run-log.md` run 7 | Cite the source as the orchestrator's run-7 instruction (not logged), not the logged 05:32 triage. Add a `shared-updates.md` row asking the orchestrator to log the RWB-E1-043 round-7 triage (run 7 allowed, D-RUN-09) and the round-8 outcome. Remove "Per the orchestrator's triage, no further remediation round follows", or cite where it was given. |

## Gate gaps (document and decision gaps not recorded by the specify stage)

| Gate ID | Source | Gap or conflict | Second source | Blocker? | Why | Owner / when |
|---|---|---|---|---|---|---|
| G8-R01 | AGENTS.md (v2, 16 Nov 2026) §7 ("A plan that touches more than one module ... goes back to the analyst") and §9 Plan approved ("touches one module") | "Module" is not defined: the design modules P1-P5 or the ACE module (recovery). This spec's plan touches P3 `casewf` and P4 `access`, so the answer decides its routing. This spec records no gap for it (A-24 and R22 treat it as a plan-gate decision) | AGENTS.md §2 ("the recovery module of the ACE service") and §3.1 (recovery, common, collection); RWB-TE-001 plan PA-12 and RWB-E1-042 CLAR-025 read it in opposite ways; D-RUN-21 (build log line 44) settles it for this build and says "The definition gap is still recorded for the document owners"; RWB-E1-042 records it as E1042-SP-DG-16 and RWB-TE-001 as PG-04/GC-1 | No | D-RUN-21 settles it for the build (orchestrator; ratification open under OPEN-050), and the plan of this story touches only the recovery ACE module, with no common or collection change | Orchestrator: record it in this story's `document-gaps.md` as a cross-reference to the existing RWB-E1-042 and RWB-TE-001 gap, not as a new `DOCUMENT-GAPS.md` entry. AGENTS.md owner (solution architect with the TechX tech leads) to define "module". Before the RWB-E1-043 plan gate |

G7-R01 is closed as a gate gap: it is recorded as GAP-58 / A-46 / R33. The orchestrator's answer to R33 is
still due before the plan gate.

## RWB-E1-001 handler contract: completeness

| Point | Judgement | Where |
|---|---|---|
| Check order | Complete, unchanged. L1-L15. | SPEC-025; §3.1 item 3 |
| What the handler supplies | Complete, unchanged. | SPEC-025; §3.1 item 2 |
| Message pass-through | Complete. | SPEC-025; §3.1 item 4 |
| Repeat behaviour | Complete; order departure recorded (GAP-56). | SPEC-025 L9; §3.1 items 3, 7 |
| Effective date | Complete, including the MSG-P3-015 case of a same-day correction (154 closed). | SPEC-008, 024, 025, 032 rule 6; A-42; TC-TM-05 |
| SPI home | D-RUN-18 and D-RUN-20, both pending tech-lead ratification (R24, OPEN-050). RWB-E1-001 is a P1 handler outside the registry's module, so D-RUN-20 confirms it uses the SPI. | SPEC-019, 025 |

RWB-E1-001 can conform to this contract. None of 155-158 changes the SPI signature or what RWB-E1-001
supplies.

## Gate decision

There is no Critical, High or Medium finding, so nothing blocks the handoff by severity (`pdlc.md`). The
review status stays `FAIL`. Under D-RUN-09 the orchestrator does not accept a Low-only failure, so 155-158
go to the orchestrator for triage, or to the engagement lead for a human disposition. All four are local text
and citation edits in the Change Scope row, A-24, R22, R6, GAP-58, the §0 E42S row, the front matter and
`gate-response.md` §11. They change no design, contract, interface or test. G8-R01 is Blocker = No.
The orchestrator's answer to R33 (GAP-58) is still due before the plan gate.

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 4]
REVIEW_STATUS: FAIL
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 4] (155, 156, 157, 158)
BLOCKING: NO by severity; not accepted under D-RUN-09 (orchestrator triage or human disposition)
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
ROUND_7_FINDINGS: 153 resolved; 154 resolved (TC-TM-05 (g)-(h) walked, every step runs)
G7_R01: recorded as GAP-58 (C, Blocker No), A-46 (Inferred), R33; orchestrator answer due before the plan gate
D_RUN_20: applied to GAP-57, R24, R32, SPEC-025, contract; quotes exact; ratification correctly shown as open
RWB_E1_042: baseline revision 10 with revision 11 checked, names unchanged (verified); assumptions/shared-updates cites and R6 stale (157)
D_RUN_21: not reflected in plan routing (155)
COUNTS: assumptions 46 (A-32 withdrawn); gaps 58 (40 C, 18 M, 0 blockers); COVERED 49; CONTRADICTIONS 40 (verified)
RATIFICATION_CLAIMS: none found
RWB_E1_001_CONTRACT: COMPLETE
DOCUMENT_GAPS_ADDED: 1 (G8-R01, Blocker = No)
NEXT_STEP: Orchestrator triage of 155-158 and answer to R33 (or engagement-lead disposition under D-RUN-09)
```

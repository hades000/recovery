# Spec gate review, round 7: RWB-E1-043 (RUN_ID `INC-008-epic-1-RWB-E1-043`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-043-SPEC-007` |
| Gate | Specification gate, round 7 (Compliance Reviewer, bounded review after the orchestrator's run-6 triage of 2026-11-18 05:32 under D-RUN-09) |
| Artefacts reviewed | `specify/spec.md` revision 7 (file 2026-11-18 05:34:41), `assumptions.md` revision 7 (A-01..A-45, A-32 withdrawn), `document-gaps.md` revision 7 (GAP-01..GAP-57), `shared-updates.md` revision 7 (R1..R32, §3.1, §3.2), `compliance-validation.md` revision 7, `contracts/backend-apis.json` revision 7, `contracts/frontend-integrations.json` revision 6 (no content change), `gate-response.md` (§9.1 row 147 corrected, §10 new). The `*.run6.*` files were diffed against the current files as the audit trail. |
| Previous round | `review/spec-gate-review-6.md` (`REVIEW-RWB-E1-043-SPEC-006`, FAIL: 2 Low, findings 151-152, no gate gap) |
| Sources checked | `AI-SDLC-BUILD-LOG.md` decisions table lines 41 (D-RUN-18), 42 (D-RUN-19) and 43 (D-RUN-20, 05:34, logged after this spec) and the RWB-E1-043 rows of 2026-11-18 05:32; RWB-E1-042 `spec.md` (revision 10, file 2026-11-18 05:28:14: header, §4.3 lines 145 and 151, SPEC-RWB-E1-042-003, §12.2, §12.12 T-2 line 959, §12.14 R7-1 line 983, TC-E1-042-45), its `assumptions.md` A-51 (file 05:27:34) and `shared-updates.md` lines 25, 26, 32, 38, 39 and 83; Story file v7 RWB-E1-019 (lines 18, 261) and RWB-E1-037 (line 46) in `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/`. All read only. |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18. No question asked (L-RCV-03). No file other than this review was written. |

**About the run rulings.** D-RUN-09, D-RUN-10, D-RUN-18, D-RUN-19, D-RUN-20 and the triage of every round were
given by the orchestrator (Claude Code), an AI agent. They are not human decisions, acceptance or
ratification, and this review does not treat them as such. Revision 7 attributes them correctly (spec §0
BLOG row and the owner-acceptance list, `assumptions.md` line 10, `shared-updates.md` line 6, R1, R24, R32,
GAP-57, `gate-response.md` §10 "not human acceptance or ratification"). A search of every reviewed artefact
found no text that presents a run ruling or a triage as ratified or human-accepted.

## Status

**`SPEC_GATE: FAIL`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 0 | |
| Low | 2 | Visible; do not block by severity; not accepted under D-RUN-09 without an orchestrator triage or a human disposition |

Finding 152 is closed. Finding 151 is closed for the step order and the §9.1 wording; the "Minor" part of its
fix (the MSG-P3-015 case in SPEC-025 and A-42) was not applied and is carried as 154. The re-baseline on
RWB-E1-042 revision 10 is correct. The new D-RUN-19 check in SPEC-019 reaches the right conclusion but rests on
a false premise ("all code here is in P3") (153). D-RUN-20, logged 15 seconds after this spec was written,
answers R32 and GAP-57 and raises one question for RWB-E1-019's handlers (G7-R01, Blocker = No).

## Round-6 findings: resolution check

| Round-6 ID | Sev | Verdict | Evidence checked |
|---|---|---|---|
| 151 TC-TM-05 step (f); §9.1 wording | Low | **Resolved** for the test sequence and §9.1. **Not applied:** the SPEC-025 / A-42 qualifier (154) | TC-TM-05 (spec.md:1070) now runs: (c) 2026-12-04, v3 `validFrom` 2026-12-04 approved and applied; (d) same date, corrected v5 for 2026-12-04 while v3 is APPROVED → 409 MSG-P3-027 "an approved version already has this valid from" at L11, nothing written. Walked against the check order: L9 is skipped (`test_current` has no repeat message, and the corrected file has another hash anyway); L10 passes (`validFrom` = business date, spec.md:643); L11 finds the APPROVED twin (spec.md:644, SPEC-006 (3) wording at spec.md:293). (e) v4 `validFrom` 2026-12-05 loaded on 12-04 (VALIDATED), approved on 12-06 → 409 (A-17). (f) rollback of v3: v3 is the latest APPROVED version (v4 is VALIDATED), v2 exists (SPEC-024 rule 6), `supportsRollback` true → ROLLED_BACK, `onRolledBack` writes v2's rows. Every step can run in sequence. `gate-response.md` §9.1 row 147 (line 281) now says the step tests a load refusal; §10.1 maps it. The round-6 fix also asked for "or no earlier approved version exists (MSG-P3-015)" in SPEC-025 and A-42; neither changed (diff of `spec.run6.md` and `assumptions.run6.md`), and §10.1 does not mention it. The orchestrator's triage wording named only the step move and §9.1. |
| 152 R24 misquotes D-RUN-18 | Low | **Resolved** | R24 (shared-updates.md:94) now quotes "P1 (RWB-E1-001) and P3 (RWB-E1-042) handlers implement it", which matches build log line 41 word for word, adds the registry clause the ruling contains, states "it names no other story as a handler implementer" (true), and gives this spec's own list (RWB-E1-001, RWB-E1-064, RWB-E1-019; `PARAMETER` a dispatcher branch) as a separate sentence. SPEC-025 (spec.md:625) and GAP-57 quote the same words. |

### Re-baseline on RWB-E1-042 (orchestrator instruction): verified

| Claim in revision 7 | Checked against | Result |
|---|---|---|
| RWB-E1-042 is at revision 10, `spec.md` 2026-11-18 05:28:14, `assumptions.md` 05:27:34 | File header ("revision: 10 (remediation run 8 …)") and file times | Correct; the file has not changed since |
| §4.3 line 145 "`PARAMETER` route": not an SPI handler; branch `ParameterLoadBranch` in `casewf.refdata.internal`; `ObjectProvider`; 404 MSG-P4-003; no second load record | E42S line 145 | Correct |
| Line 151 business-date seam is a P3 → P1 read under D-RUN-18, and P1 parameter readers use `CatalogParameterReader` | E42S line 151 | Correct |
| §12.12 T-2 line 959 adds `CatalogParameterReader`; R7-1 line 983 "a dispatcher branch, not an SPI handler" | E42S lines 959, 983 | Correct |
| A-51 "`PARAMETER` is not an SPI handler" | E42S `assumptions.md` line 59 | Correct |
| E42S `shared-updates.md` lines 25, 26, 32, 38, 39, 83 | Those lines | Correct (line 38 is the D-RUN-19 reader row; line 39 the ratification row) |
| Names consumed unchanged (`english`/`thai`, six-argument `ApiProblemException`, `has`/`require`, `byName`, `ParameterLoadHandler`, `BusinessDateProvider`) | E42S §10.2, §12.2, SPEC-005 (line 166), line 592 | Unchanged |
| T-TE001-14 `access.api` set at revision 10 | E42S TC-E1-042-45 (line 1073), lines 83, 547 | `ApiError`, `ApiProblemException`, `MessageResolver`, `CapabilityCheck`, `CatalogParameterReader`, `.Value`: matches SPEC-019, R29 and contract `tTe001_14` |

Revision 10 also adds a build rule (SPEC-RWB-E1-042-003, line 164): a `CatalogParameterReader.get` call whose
key is not a string literal fails the build. This story reads its per-code keys through
`ParameterKeys.byName(String, Class<T>)` in P3 (A-26), which the rule does not cover, so nothing here changes.

### D-RUN-19 check in SPEC-019: verified, with one defect

D-RUN-19 (line 42): a module outside P3 reads the parameter catalog through a P4 `access.api` interface
implemented in P3 `casewf.config`; "P3 callers may keep using `casewf.config.api`"; no P1, P2 or P4 to P3 edge.
SPEC-019 *Parameter reads under D-RUN-19* (spec.md:478-485):

| Point | Verdict |
|---|---|
| (1) "all code here is in P3" and reads `rwb.refload.*`, `refdata.columns.*`, `refdata.cache.ttl-seconds` through `casewf.config.api` | The keys and the read path are right (SPEC-003, SPEC-027, SPEC-013 read them in `casewf.refdata.internal`). The premise is wrong: the story also adds P4 code, `access.internal.LovValueReader` and six `access.api` types (spec.md:78, edge table row at spec.md:438). See 153 |
| (2) `CatalogParameterReaderImpl` in `casewf.config` is a P3 → P4 edge | Correct (E42S lines 84, 546) |
| (3) the SPI refers to no parameter type, so a P1 handler that needs a parameter uses `CatalogParameterReader` | Correct; the SPI types refer only to JDK types and each other (spec.md:440) |
| (4) the `PARAMETER` route is the dispatcher branch, as E42S revision 10 states | Correct |
| Registry and GAP-57 agree with RWB-E1-042's current route and with D-RUN-18/19 | Yes. The registry collects SPI beans by the P4 type; a `PARAMETER` bean fails start-up (TC-HD-02); GAP-57 now concerns only D-RUN-18's wording, which D-RUN-20 has since addressed (observation below) |

### What holds (verified)

- The run-6 diff touches only the revision headers, §0 E42S and BLOG rows, the inherited and P2 rows,
  SPEC-019 (re-baseline and the D-RUN-19 paragraph), SPEC-020 (citation), SPEC-025 (`PARAMETER` paragraph),
  SPEC-026 (citation), TC-TM-05, the owner-acceptance list, A-08, A-25, A-26, A-43-A-45 (citations), GAP-50,
  GAP-51, GAP-57, R1, R6, R24, R29, R32, the contract `source`, `implementedBy`, `tTe001_14` and `basis`.
  No run-6 edit reopens findings 1-150. Check order L1-L15, maker-checker, the append-only trigger, message
  pass-through, the 403 action texts and flag-off start-up are unchanged.
- Counts verified: 57 gaps (39 C, 18 M), no blocker; 45 assumption rows; 49 COVERED rows; CONTRADICTIONS 39.
- Every message ID used exists in Error and Message Standard v4; no new message ID.
- No business value, role or threshold is a literal; no personal data, secret or production data appears.
- Frontend `NOT_APPLICABLE` (contract revision 6, no content change); the 80% backend unit-test gate stays
  planned. Both contract files parse as JSON.
- No module edge points into P3 from another module; P4 refers to no P1 or P3 type; no cycle.

### Observations (no finding)

1. **D-RUN-20 (build log line 43, 2026-11-18 05:34:56).** Logged after this spec (05:34:41). It states that
   `PARAMETER` "is served by a dispatcher branch of the RWB-E1-043 registry" and says it closes E1-042 CLAR-027
   and E1-043 GAP-57. That is the remaining ask of R32, so R32 and GAP-57 can be marked answered by the
   orchestrator ruling (still pending tech-lead ratification with D-RUN-18/19). The spec text does not need to
   change for the build. Its first sentence raises one question for a later story (G7-R01).
2. **RWB-E1-042 run 9 snapshot.** `spec.run9.md` and `assumptions.run9.md` (05:35:12) are byte-identical to the
   current revision 10 files, so RWB-E1-042 has started another remediation run. Nothing has changed yet; the
   Implementation Planner should re-check the revision in force (A-25, R6).
3. **RWB-E1-042 `shared-updates.md` line 38** names RWB-E1-037 (P4) as a reader of `rwb.refload.approver.*`
   through `CatalogParameterReader`. In this spec those keys are read only by the P3 registry (SPEC-027), and
   Story v7 RWB-E1-037 line 46 says only that two such keys are in the catalog. If RWB-E1-037 does read them,
   it must pass literal keys (E42S SPEC-003). No change here.
4. **TC-TM-05 labels.** The refused corrected file in step (d) is labelled v5 and the later file in (e) v4.
   The refused load writes nothing, so no version number is used; the labels are only names. Optional: call
   the refused file "v3-corrected".

## Findings

### Low

| ID | Severity | Finding | Evidence | Affected | Fix required |
|---|---|---|---|---|---|
| `REVIEW-RWB-E1-043-153` | Low | **The D-RUN-19 check rests on a false premise.** The new paragraph says "(1) all code here is in P3", repeating SPEC-019's opening "All code of this story is in P3 `casewf.refdata`". The story also adds P4 code: `access.internal.LovValueReader` and the `access.api` types `ListOfValuesReader`, `ReferenceTableHandler`, `ReferenceLoadFile`, `HandlerMessage`, `ValidationReport`, `RowCheckFailure`, all listed in the same spec. D-RUN-19 is about code outside P3, so that P4 code is exactly what the check had to cover. The conclusion holds, because `LovValueReader` reads `lov_value` and no catalog parameter, and the SPI types are interfaces, but the check does not say so. The orchestrator asked for this check to be stated and verified. | spec.md:423, 478-485 (new in run 6), 78 ("P4 additions"), 245-247, 438; build log line 42 | SPEC-019; `gate-response.md` §10.1 D-RUN-19 row; compliance-validation §3 | In SPEC-019, change "All code of this story is in P3" and point (1) to say the story's code is in P3 `casewf.refdata` except the P4 additions of SPEC-002 and SPEC-025. Add that those P4 additions read no catalog parameter (`LovValueReader` reads `lov_value`; the SPI types are interfaces), so D-RUN-19 asks nothing of them. |
| `REVIEW-RWB-E1-043-154` | Low | **Part of finding 151's fix was not applied.** SPEC-025 *Effective date* says a same-day correction "needs a rollback of that day's version first (when the handler supports rollback), after which a corrected file with the same `validFrom` can be loaded and approved; otherwise it waits for a later `validFrom`", and that this is "Proved with … TC-TM-05". When that day's version is the table's first approved version, the rollback is refused with 409 MSG-P3-015 (SPEC-024 rule 6) even though the handler supports rollback. SPEC-032 rule 6, A-42 and `gate-response.md` §9.1 row 147 say "needs a rollback first" without the condition. TC-TM-05 tests the refusal (d) and a rollback (f), but not the reload and approval after a rollback that SPEC-025 says it proves. Round 6 asked for the MSG-P3-015 wording in SPEC-025 and A-42. | spec.md:690-694 (SPEC-025), 547 (SPEC-024 rule 6), 914-915 (SPEC-032 rule 6), 1070 (TC-TM-05); assumptions.md A-42; gate-response.md:281, 319; spec-gate-review-6.md finding 151 "Fix required" | SPEC-025 *Effective date*; SPEC-032 rule 6; A-42 | Add "and an earlier approved version exists (otherwise 409 MSG-P3-015)" next to "when the handler supports rollback" in SPEC-025, and the same condition in SPEC-032 rule 6 and A-42. Either add a TC-TM-05 step (g): after (f), a corrected file with `validFrom` 2026-12-04 loads and is approved on a 2026-12-04 business date, or narrow "Proved with TC-TM-05" to the steps it covers. |

## Gate gaps (document and decision gaps not recorded by the specify stage)

| Gate ID | Source | Gap or conflict | Second source | Blocker? | Why | Owner / when |
|---|---|---|---|---|---|---|
| G7-R01 | Run decision D-RUN-20 (`AI-SDLC-BUILD-LOG.md` decisions table line 43; orchestrator, Claude Code; not ratified): "The P4 handler SPI is for handlers that live outside the registry's module (P1 RWB-E1-001, and any later P1 or P2 owner)" | Read as an exclusive rule, the P3 handlers of RWB-E1-019 (QUEUE, QUEUE_MEMBER) may not implement the P4 SPI. The ruling defines a route only for `PARAMETER`, and says nothing about the RWB-E1-019 tables | This spec SPEC-019 later-edge table ("P3 handlers (QUEUE, QUEUE_MEMBER) → P4 `access.api`", RWB-E1-019 order 25), SPEC-025, R24 and contract `p4HandlerSpi.implementedBy`; Story v7 RWB-E1-019 line 18 (module P3) and line 261 ("P3 checks plugged into the RWB-E1-043 registry") | No | RWB-E1-019 is a later story (order 25; D-RUN-08). Nothing this story builds or tests changes: a P3 class implementing a P4 type uses the P3 → P4 edge that already exists. If the orchestrator rules that P3 tables need a route other than the SPI, the registry design for those codes is decided before RWB-E1-019 is specified | Orchestrator (Claude Code), recovery tech lead with R24. Confirm whether RWB-E1-019's P3 handlers implement the P4 SPI under D-RUN-20. Decide before the RWB-E1-043 plan gate; at the latest before the RWB-E1-019 spec |

## RWB-E1-001 handler contract: completeness

| Point | Judgement | Where |
|---|---|---|
| Check order | Complete, unchanged. L1-L15. | SPEC-025; §3.1 item 3 |
| What the handler supplies | Complete, unchanged. | SPEC-025; §3.1 item 2 |
| Message pass-through | Complete. | SPEC-025; §3.1 item 4 |
| Repeat behaviour | Complete; order departure recorded (GAP-56). | SPEC-025 L9; §3.1 items 3, 7 |
| Effective date | Complete for RWB-E1-001's `CURRENT_STATE` handler. The same-day correction wording needs the MSG-P3-015 case (154). | SPEC-008, 025, 032 rule 6; A-42 |
| SPI home | D-RUN-18 (`access.api`) and D-RUN-20 (`PARAMETER` a dispatcher branch), both pending tech-lead ratification (R24). RWB-E1-001 is a P1 handler, so D-RUN-20 confirms it uses the SPI. | SPEC-019, 025 |

RWB-E1-001 can conform to this contract. Neither 153 nor 154 changes the SPI signature or what RWB-E1-001
supplies.

## Gate decision

There is no Critical, High or Medium finding, so nothing blocks the handoff by severity (`pdlc.md`). The
review status stays `FAIL`. Under D-RUN-09 the orchestrator does not accept a Low-only failure, so 153 and 154
go to the orchestrator for triage, or to the engagement lead for a human disposition. Both are local text
edits in SPEC-019, SPEC-025, SPEC-032 and A-42, with an optional test step. They change no design, contract or
interface. G7-R01 is Blocker = No and needs an orchestrator answer before the plan gate.

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]
REVIEW_STATUS: FAIL
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2] (153, 154)
BLOCKING: NO by severity; not accepted under D-RUN-09 (orchestrator triage or human disposition)
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
ROUND_6_FINDINGS: 152 resolved; 151 resolved for TC-TM-05 order and gate-response §9.1, its SPEC-025/A-42 MSG-P3-015 part not applied (154)
RWB_E1_042: re-baseline on revision 10 (spec.md 05:28:14, assumptions.md 05:27:34) verified; consumed names and T-TE001-14 set unchanged; run-9 snapshot exists, no change yet (observation)
D_RUN_19: check verified; conclusion holds; premise "all code here is in P3" wrong (153)
D_RUN_20: logged 05:34:56, after this spec; answers R32 and GAP-57 (observation); raises G7-R01 for RWB-E1-019's P3 handlers (Blocker = No)
RWB_E1_001_CONTRACT: COMPLETE
DOCUMENT_GAPS_ADDED: 1 (G7-R01, Blocker = No)
NEXT_STEP: Orchestrator triage of 153-154 and answer to G7-R01 (or engagement-lead disposition under D-RUN-09)
```

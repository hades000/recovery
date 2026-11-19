# Spec gate review, round 6: RWB-E1-043 (RUN_ID `INC-008-epic-1-RWB-E1-043`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-043-SPEC-006` |
| Gate | Specification gate, round 6 (Compliance Reviewer, bounded review; the last round allowed in this run by the orchestrator's round-4 triage of 2026-11-18 04:55) |
| Artefacts reviewed | `specify/spec.md` revision 6 (2026-11-18 05:24), `assumptions.md` revision 6 (A-01..A-45, A-32 withdrawn), `document-gaps.md` revision 6 (GAP-01..GAP-57), `shared-updates.md` revision 6 (R1..R32, §3.1, §3.2), `compliance-validation.md` revision 6, `contracts/backend-apis.json` revision 6, `contracts/frontend-integrations.json` revision 5, `gate-response.md` (§9). The `*.run5.*` files were diffed against the current files as the audit trail. |
| Previous round | `review/spec-gate-review-5.md` (`REVIEW-RWB-E1-043-SPEC-005`, FAIL: 4 Low, findings 147-150, gap G5-R01) |
| Sources checked | `AI-SDLC-BUILD-LOG.md` decisions table (D-RUN-18 line 41, D-RUN-19 line 42) and the RWB-E1-043 triage rows; RWB-E1-042 spec revision 9 (kept as `spec.run8.md`: §4.3 line 144 `PARAMETER` seam row, line 150 business-date seam, SPEC-RWB-E1-042-017, §12.12 T-2 line 948, §12.14 R7-1 line 972) and `assumptions.run8.md` A-51; RWB-E1-042 current `spec.md` (revision 10, file 2026-11-18 05:27:34, written after this spec) and `assumptions.md` A-51; RWB-E1-042 `shared-updates.md` lines 25, 26, 32, 39, 83. All read only. |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18. No question asked (L-RCV-03). No file other than this review was written. |

**About the run rulings.** D-RUN-09, D-RUN-10, D-RUN-18, D-RUN-19 and the round-4 triage were given by the
orchestrator (Claude Code), an AI agent. They are not human decisions, acceptance or ratification, and this
review does not treat them as such. Revision 6 attributes them correctly: spec §0 BLOG row, `assumptions.md`
header (line 10), `document-gaps.md` header (line 9), `shared-updates.md` header (line 6), R1, R24, R32,
GAP-57 and `gate-response.md` §9 all say "not ratified" or "pending". A search of every reviewed artefact found
no text that presents a run ruling or triage as ratified or human-accepted.

## Status

**`SPEC_GATE: FAIL`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 0 | |
| Low | 2 | Visible; do not block by severity; not accepted by the orchestrator under D-RUN-09. This is the last round allowed in this run, so they go to the engagement lead for a human disposition, or back to the orchestrator for triage |

Findings 147, 148 and 150 are closed. Finding 149 is closed in substance: the spec states one `PARAMETER`
route, gives source reasons, records GAP-57 and asks for alignment in R32. Two new Low findings come from the
run-5 edits. TC-TM-05's new step (f) needs a state that steps (d) and (e) have already changed (151). R24's
corrected paraphrase of D-RUN-18 credits the ruling with naming stories it does not name (152).

## Round-5 findings: resolution check

| Round-5 ID | Sev | Verdict | Evidence checked |
|---|---|---|---|
| 147 TC-TM-05 (c), (e) | Low | **Resolved** for (c) and (e); new step (f) is defective (151) | TC-TM-05 (spec.md:1060): (c) now moves the business date to 2026-12-04 and loads v3 with `validFrom` 2026-12-04, so L11 finds no APPROVED twin (v2 is 2026-12-03); (d) v4 `validFrom` 2026-12-05 approved on 2026-12-06 → 409 (A-17, SPEC-008 line 307); (e) rolls back v3, the latest APPROVED version (v4 is VALIDATED, so SPEC-024 rule 5 does not refuse; rule 6 finds v2; `supportsRollback` true), and `onRolledBack` writes v2's rows. The one-approved-version-per-`validFrom` rule is stated in SPEC-025 *Effective date* (spec.md:680-684), SPEC-032 rule 6 (spec.md:904-905), A-42 and the contract `effectiveDate`. Checked against SPEC-001 (partial unique index on APPROVED, `UNIQUE (table_code, valid_from, content_hash)`) and SPEC-006 (3): after a rollback, a corrected file (other hash) with the same `validFrom` loads and approves, as the new text says. |
| 148 RWB-E1-042 baseline and T-TE001-14 | Low | **Resolved** | §0 E42S row, A-25, R6, R29, `compliance-validation.md` §3 and the contract `source` and `consumedInterfaces.basis` cite revision 9 (05:16:37) and name revision 7 as `spec.run6.md`. SPEC-019 (spec.md:457-467) now defines the `access.api` set as RWB-E1-042's merged set plus exactly six types, names `CatalogParameterReader` and `CatalogParameterReader.Value` (E42S revision 9 T-2, line 948: "(rev 9) + `CatalogParameterReader`"), and says what happens if RWB-E1-042 merges another set. TC-BD-01 and contract `tTe001_14` match. Names consumed (`english`/`thai`, the six-argument `ApiProblemException`, `has`/`require`, `byName`) unchanged in revisions 9 and 10 (checked). |
| 149 `PARAMETER` route | Low | **Resolved in the spec**; R24 wording defective (152) | SPEC-025 *`PARAMETER` is not an SPI handler* (spec.md:606-618) and SPEC-026 (spec.md:750-751) state the route: `ParameterLoadBranch` in P3, `ObjectProvider<ParameterLoadHandler>`, 404 MSG-P4-003, no `access.api` type; a `PARAMETER` handler bean fails start-up (SPEC-021, TC-HD-02). Reasons checked: E42S revision 9 line 144 and SPEC-017 keep `PARAMETER` versions behind `ParameterLoadHandler` with `parameter_value.load_id`; R7-1 (line 972) asks for "no second load record beside `parameter_value.load_id`", which the registry path (its own `reference_version` row) would create; D-RUN-10 has the dispatcher separate `PARAMETER`. The departure from D-RUN-18's wording ("P3 (RWB-E1-042) handlers implement it", quoted correctly) and from E42S revision 9 A-51 ("implements it", `assumptions.run8.md`) is stated and sourced; GAP-57 (C, Blocker = No) and R32 record it; contract `implementedBy` says the same. The choice is coherent: two orchestrator rulings point different ways, the spec follows D-RUN-10, keeps RWB-E1-042's flag-off contract and asks the orchestrator to rule (R32 (b)). |
| 150 Cross-references | Low | **Resolved** | (a) SPEC-024 (spec.md:547-552) now cites SPEC-006 rule (2) for the 201 return, rule (1) for the 409 repeat message of a handler code (L9 runs before L10, so no date condition, correct), and L10 for the 422 once `validFrom` has passed; A-27 says the same. (b) contract `source` cites RWB-E1-042 revision 9. |
| G5-R01 | — | **Carried in** | GAP-57, "Raised by: spec gate review 5 (G5-R01)", Blocker = No, owners in R32. Counts verified: 57 gaps (39 C, 18 M), 49 COVERED rows, 45 assumption rows, CONTRADICTIONS 39. |

### What holds (verified)

- No run-5 edit reopens findings 1-146. The diff of revision 5 to revision 6 touches only §0, the inherited and
  P2 rows, SPEC-019, SPEC-020 (citation), SPEC-024, SPEC-025, SPEC-026, SPEC-032 rule 6, TC-TM-05, TC-BD-01,
  CLAR-019 and the counts. Check order L1-L15, maker-checker, the append-only trigger, message pass-through,
  the 403 action texts and flag-off start-up are unchanged.
- Every message ID used exists in Error and Message Standard v4; no new message ID.
- No business value, role or threshold is a literal; no personal data, secret or production data appears.
- The frontend is correctly `NOT_APPLICABLE` (contract revision 5, no content change); the 80% backend
  unit-test gate stays planned.
- No module edge points into P3 from another module; P4 refers to no P1 or P3 type; no cycle.

### Observation (no finding): RWB-E1-042 revision 10

RWB-E1-042's `spec.md` and `assumptions.md` were rewritten at 05:27:34 (revision 10, its findings 155-158),
after this spec (05:24). Revision 10 adopts this spec's route: A-51 and the §4.3 seam row (now line 145) say
"`PARAMETER` is not an SPI handler", R7-1 says "a dispatcher branch, not an SPI handler", new plan input R8-1
supersedes the "SPI route" wording, and CLAR-027 carries the D-RUN-18 wording question to the tech lead. R32
(a) is therefore done on RWB-E1-042's side; R32 (b) (the orchestrator) stays open. Revision 10 adds the method
`CatalogParameterReader.get(key, type)` and no type, so the T-TE001-14 set of SPEC-019 and every name this
story consumes are unchanged. This spec's references to "revision 9 §4.3 line 144" and to A-51 "implements it"
are correct for revision 9 (now `spec.run8.md`, `assumptions.run8.md`) but no longer describe the file at the
cited path. Nothing in the build changes, so this is not a finding; the Implementation Planner should
re-baseline on the RWB-E1-042 revision in force (A-25, R6) and close R32 (a).

## Findings

### Low

| ID | Severity | Finding | Evidence | Affected | Fix required |
|---|---|---|---|---|---|
| `REVIEW-RWB-E1-043-151` | Low | **TC-TM-05 step (f) cannot run where it stands.** Step (d) moves the business date to 2026-12-06 and step (e) rolls v3 back. Step (f) then loads a corrected v5 "on business date 2026-12-04 … while v3 is APPROVED" and expects 409 "an approved version already has this valid from". After (e), v3 is ROLLED_BACK and the date is 2026-12-06. Run in sequence, (f) is refused 422 at L10 (`test_current` has no repeat message, and `validFrom` has passed). Even with the date set back, no APPROVED twin exists any more, so the load is accepted. The state (f) needs exists only between (c) and (d). Also, `gate-response.md` §9.1 says (f) shows "a second approval for the same date is refused", but (f) tests a load refusal at L11 (SPEC-006 (3)), not an approval. Minor: SPEC-025's new sentence says a same-day correction "waits for a later `validFrom`" only when the handler does not support rollback; for a table's first approved version, rollback is also refused (409 MSG-P3-015, SPEC-024 rule 6). | spec.md:1060 (TC-TM-05 (d)-(f)), 291 (SPEC-006 (3)), 633-634 (L10, L11), 537 (SPEC-024 rule 6), 680-684; gate-response.md:281 | TC-TM-05; SPEC-025 *Effective date*; gate-response §9.1 | Move the same-day refusal to just after (c), as (c2): business date 2026-12-04, v3 APPROVED, corrected v5 `validFrom` 2026-12-04 → 409 MSG-P3-027. Then run (d) and (e). Optionally add, after (e), the positive case the new text claims: a corrected file with v3's `validFrom`, loaded and approved on that date, is applied. Say "or no earlier approved version exists (MSG-P3-015)" next to "when the handler supports rollback" in SPEC-025 and A-42. Correct the §9.1 wording in the next gate response. |
| `REVIEW-RWB-E1-043-152` | Low | **R24 misstates what D-RUN-18 says.** D-RUN-18 (build log line 41) reads "P1 (RWB-E1-001) and P3 (RWB-E1-042) handlers implement it". Corrected R24 presents the ruling as "P1 (RWB-E1-001, RWB-E1-064) and P3 (RWB-E1-019) handlers implement it (D-RUN-18 also names RWB-E1-042 …)". "Also" implies the ruling names RWB-E1-019, and it names neither RWB-E1-019 nor RWB-E1-064. R32 (b) asks the orchestrator to confirm that reading ("read as the RWB-E1-019 handlers, `PARAMETER` excepted, or rules otherwise"), so the reading is the spec's interpretation and not the ruling. R24 is the row the tech lead is asked to ratify, so it should quote the ruling and keep the interpretation apart. SPEC-025 and GAP-57 quote the ruling correctly; only R24 is wrong. | `AI-SDLC-BUILD-LOG.md` line 41; shared-updates.md:94 (R24), :102 (R32 (b)); spec.md:613-614; document-gaps.md:84 | R24 | Quote D-RUN-18 in R24 as written ("P1 (RWB-E1-001) and P3 (RWB-E1-042) handlers"). Then state separately that this spec applies it to the RWB-E1-001 and RWB-E1-064 P1 handlers and the RWB-E1-019 P3 handlers, keeps `PARAMETER` off the SPI (GAP-57), and asks the orchestrator to confirm in R32 (b). |

## RWB-E1-001 handler contract: completeness

| Point | Judgement | Where |
|---|---|---|
| Check order | Complete, unchanged. L1-L15; `data_product` takes the early repeat (L9) and skips L12. | SPEC-025; §3.1 item 3 |
| What the handler supplies | Complete, unchanged. | SPEC-025; §3.1 item 2 |
| Message pass-through | Complete. | SPEC-025; §3.1 item 4 |
| Repeat behaviour | Complete; order departure recorded (GAP-56). | SPEC-025 L9; §3.1 items 3, 7 |
| Effective date | Complete. Now also says one APPROVED version per `validFrom` and that a same-day correction needs a rollback first. | SPEC-008, 025, 032 rule 6; A-42 |
| SPI home | Settled for the build by D-RUN-18 (`access.api`), pending tech-lead ratification (R24); `PARAMETER` stays off the SPI (GAP-57, R32). | SPEC-019, 025 |

RWB-E1-001 can conform to this contract. Neither finding 151 nor 152 changes the SPI signature or what
RWB-E1-001 supplies.

## Document gaps not recorded by the specify stage

None. The RWB-E1-042 revision-10 change above aligns two artefacts and is not a document gap.

## Gate decision

There is no Critical, High or Medium finding, so nothing blocks the handoff by severity (`pdlc.md`). The
review status stays `FAIL`. Under D-RUN-09 the orchestrator does not accept a Low-only failure. The
orchestrator's round-4 triage allowed this round as the last in this run, so findings 151 and 152 go to the
engagement lead for a human disposition, or back to the orchestrator for a triage decision. Both are local
text edits (one test row and one shared-update row) and change no design, contract or interface. No finding
needs a Blocker = Yes gap.

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]
REVIEW_STATUS: FAIL
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2] (151, 152)
BLOCKING: NO by severity; not accepted under D-RUN-09 (last round allowed in this run: route to the engagement lead for a human disposition, or orchestrator triage)
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
ROUND_5_FINDINGS: 147, 148, 150 resolved; 149 resolved in the spec (R24 wording in 152); 147's new step (f) defective (151); G5-R01 carried in as GAP-57
D_RUN_18: applied as a run ruling; PARAMETER kept as a dispatcher branch, departure from the ruling's wording recorded (GAP-57, R32); no ratification claimed anywhere
RWB_E1_042: revision 10 (05:27:34, after this spec) adopts the dispatcher-branch route; T-TE001-14 set and consumed names unchanged; planner to re-baseline (observation, no finding)
RWB_E1_001_CONTRACT: COMPLETE
DOCUMENT_GAPS_ADDED: 0
NEXT_STEP: Orchestrator triage of 151-152 (route to the engagement lead for a human disposition under D-RUN-09, since round 6 is the last round allowed in this run)
```

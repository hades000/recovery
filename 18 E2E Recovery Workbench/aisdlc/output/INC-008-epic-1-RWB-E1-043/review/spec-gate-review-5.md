# Spec gate review, round 5: RWB-E1-043 (RUN_ID `INC-008-epic-1-RWB-E1-043`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-043-SPEC-005` |
| Gate | Specification gate, round 5 (Compliance Reviewer, bounded review) |
| Artefacts reviewed | `specify/spec.md` revision 5 (2026-11-18 05:09), `assumptions.md` revision 5 (A-01..A-45, A-32 withdrawn), `document-gaps.md` revision 5 (GAP-01..GAP-56), `shared-updates.md` revision 5 (R1..R31, §3.1, §3.2), `compliance-validation.md` revision 5, `contracts/backend-apis.json` revision 5, `contracts/frontend-integrations.json` revision 4, `gate-response.md` (§8). The `*.run4.*` files were used as the audit trail only. |
| Previous round | `review/spec-gate-review-4.md` (`REVIEW-RWB-E1-043-SPEC-004`, FAIL: 1 Medium, 8 Low, G4-R01..G4-R03) |
| Sources checked | `AI-SDLC-BUILD-LOG.md` decisions table (D-RUN-18 line 41, D-RUN-19 line 42) and the 04:55 triage rows; Story files v7 RWB-E1-001 (§4 steps 7-10, AC3, §12 line 222), RWB-E1-064 (§4 steps 1-10); RWB-TE-001 spec v4 (SPEC-022 (d), module-map fields, T-TE001-14 line 279) and `shared-updates.md` SU-08; RWB-E1-042 spec revision 7 (now kept as `spec.run6.md`: §10.1, §10.2, §12.2 signatures, §12.12 bean table, SPEC-RWB-E1-042-020/-021, TC-E1-042-05..-23, TC-45) and the current `spec.md` (revision 9, 05:16:37: §4.3 seam row, §12 T-2, A-51) with its `review/spec-gate-review-7.md`; Physical Schema v6 (`data_product`, `sys_fields`); Error and Message Standard v4 (lines 85, 151, 164); `platform/internal/ApiExceptionHandler.java` (line 41) and `platform/api/ApiProblemException.java` (read only). |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18. No question asked (L-RCV-03). No file other than this review was written. |

**About the run rulings.** The round-4 triage (2026-11-18 04:55) and run decision D-RUN-18 were given by
the orchestrator (Claude Code), an AI agent. They are not human decisions, acceptance or ratification,
and this review does not treat them as such. D-RUN-18 is applied here as a valid run ruling for the
build. Revision 5 attributes both correctly: spec §0 BLOG row and §"Owner acceptance", `assumptions.md`
header, `document-gaps.md` header, GAP-36/51/53 ("pending ratification by the recovery tech lead"),
`shared-updates.md` header, R1 and R24, `compliance-validation.md` §1 and §3, and `gate-response.md` §8 all
say "not ratified" or "pending". A search of every reviewed artefact found no text that presents D-RUN-18,
any D-RUN entry or any triage as ratified or human-accepted.

## Status

**`SPEC_GATE: FAIL`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 0 | |
| Low | 4 | Visible; do not block by severity; not accepted by the orchestrator under D-RUN-09 (fix and re-gate, or route to the engagement lead for a human disposition) |

All nine round-4 findings (138-146) and the three round-4 gaps (G4-R01..G4-R03) are closed in the files.
The Medium 138 is fixed: each handler declares `DATED` or `CURRENT_STATE`, the current-state rule is
consistent across SPEC-008, SPEC-025, SPEC-032 rule 6, A-42, the status and exception matrices, §3.1 items
2 and 8, §3.2 item 6, R5, R31 and the backend contract, and it needs no schema change or owner job. The four
new Low findings are: an impossible step in the new test TC-TM-05 (147); drift of RWB-E1-042 after the
revision-7 baseline, which makes the stated T-TE001-14 set stale (148); an unrecorded disagreement on
whether the `PARAMETER` route implements the P4 SPI (149); and stale cross-references (150).

## Round-4 findings: resolution check

| Round-4 ID | Sev | Verdict | Evidence checked |
|---|---|---|---|
| 138 Current-state tables | Medium | **Resolved** | SPEC-025 `Dating { DATED, CURRENT_STATE }`, default `CURRENT_STATE` (spec.md:569-589); SPEC-008 adds the refusal "it can be approved only on its valid from date <validFrom>" with 409 MSG-P3-027, `apply` not called (spec.md:307-310); with A-17 approval happens on the valid-from date (spec.md:648-658); out-of-order cannot occur; rollback re-applies at once; SPEC-032 rule 6. PS6 checked: `data_product` has `uk_data_product UNIQUE (product_code)` and one `valid_from`; `sys_fields` has `uk_sys_fields UNIQUE (field_id)` and no date. MSG4 line 151 MSG-P3-027 carries `{table}` and `{check}`; no new message ID. S7-001 flow step 10 (rows written by `apply` "with the valid from date") is now cited and met. Same text in A-42, §3.1 items 2, 8, §3.2 item 6, R5, R31, status matrix row 910, exception row 941 and contract `handlerContract.effectiveDate`, approve 409. TC-TM-05 added; one of its steps is defective (147). |
| 139 T-TE001-14 | Low | **Resolved** against RWB-E1-042 revision 7 | Change Scope "Impacted Existing Nodes" lists T-TE001-14 as a changed test; SPEC-019 (spec.md:456-469) states the expected sets; TC-BD-01 asserts them; R29 coordinates with RWB-E1-042. Revision 7 TC-45 / T-2 checked: `access.api` + `MessageResolver`, `CapabilityCheck`; named interface `config.api`. RWB-E1-042 has since added a type (148). |
| 140 Early repeat | Low | **Resolved** | L9 runs only when `repeatMessage(file)` is present; every other code keeps S7 §13 order at L11 (spec.md:281-292, 610-612, 628-635); A-38; TC-RP-01 (a)-(d) cover both paths; GAP-56 recorded; contract `loadCheckOrder` matches. |
| 141 SPI placement | Low | **Resolved under D-RUN-18** | D-RUN-18 (build log line 41) verified: SPI in P4 `access.api`, registry stays in P3, no P1 → P3 edge, P3 → P1 reads allowed. SPEC-019 edge tables (spec.md:431-449), SPEC-025 package line 556, `RecoveryBoundaryTest` rule (3), GAP-36/51/53, R16, R22, R24, R25, §3.1 item 2, §3.2 item 1 and contract `p4HandlerSpi` agree. S7-001 §12 line 222 ("published interface of P4 that P1 implements") verified. TE-001's map has no per-module allow list, only the cycle rule, so P1 → P4 and P3 → P1 edges are legal. Every mention is "pending tech-lead ratification". The `PARAMETER` part of D-RUN-18's wording is not addressed (149). |
| 142 403 "do this" | Low | **Resolved** | SPEC-027 uses `CapabilityCheck.require(auth, "Reference data", right, action)` and, for the table right, the same `ApiProblemException(ApiError.NOT_PERMITTED, Map.of("action", action), null)`; checked against RWB-E1-042 revision 7 (`boolean require(...)` "true, or throws" that form) and the existing `ApiProblemException(ApiError, Map, Throwable)` constructor. `ApiExceptionHandler` line 41 still fills "do this" for `AccessDeniedException`, which this path avoids. A-45 labels the action texts as inferred; the SEC note asserts `{action}`. |
| 143 Flag-off start-up | Low | **Resolved** | SPEC-018: only controller and dispatcher are conditional; `ReferenceTableHandlers` (empty map), `LoggingReferenceDecisionRecorder`, `ParameterLoadBranch` (`ObjectProvider`) always present; `RefdataSettings` gates writes. RWB-E1-042 revision 7 §12.12 keeps `ParameterService`, `BusinessDateProvider`, `MessageResolver`, `CapabilityCheck` registered with its flag off, so every injected dependency exists. TC-FL-01 covers all four flag combinations. |
| 144 RWB-E1-042 baseline | Low | **Resolved for names; residual cite (150 (b))** | Revision 7 names verified in `spec.run6.md`: `english`/`thai(String messageId, Map<String, String> placeholders)`, the six-argument `ApiProblemException`, `has`/`require`, `byName(String, Class<T>)`; the same strings are unchanged in revision 9. §0, A-25, R6, `compliance-validation.md` §3 and contract `consumedInterfaces.basis` cite revision 7. The contract's top-level `source` still says revision 5. |
| 145 Row 25 | Low | **Resolved** | TC-PB-02 runs the real `ParameterLoadHandler` through the three endpoints; each expected result matches RWB-E1-042 revision 7 TC-05, -06, -07, -10 (a), -11, -16..-20, -23; TC-10 (b) left with RWB-E1-042; R30 answers row 25. |
| 146 Wording | Low | **Resolved** | A-37 "L12 before L13"; SPEC-027 and GAP-46 say precedence does not settle it and A-08 does; `compliance-validation.md` is revision 5. |
| G4-R01..G4-R03 | — | **Carried in** | GAP-54, GAP-55, GAP-56, each "Raised by: spec gate review 4", Blocker = No, owner named (data owner via R31; BA and RWB-E1-001 owner). Counts verified: 56 gaps (38 C, 18 M), 49 COVERED rows, 45 assumption rows. |

### What holds (verified)

- Maker-checker, the narrowed append-only trigger, per-version `row_key`, the cache serving only APPROVED
  versions, message pass-through and the L1-L15 check order are unchanged and consistent across
  `spec.md`, §3.1 and the contract.
- Every message ID used exists in Error and Message Standard v4; MSG-P4-002 (line 164) has `{action}`.
- No module edge points into P3 from another module, and P4 refers to no P1 or P3 type; no cycle.
- No business value, role or threshold is a literal; no personal data, secret or production data appears.
- The frontend is correctly `NOT_APPLICABLE`; the unit-test row plans the 80% backend gate.
- No artefact claims ratification or owner acceptance.

## Findings

### Low

| ID | Severity | Finding | Evidence | Affected | Fix required |
|---|---|---|---|---|---|
| `REVIEW-RWB-E1-043-147` | Low | **TC-TM-05 steps (c) and (e) cannot happen as written.** After step (b) the business date is 2026-12-03 and v2 is APPROVED with `validFrom` 2026-12-03. Step (c) loads v3 "with `validFrom` = business date", that is 2026-12-03 again, and expects it to be approved and applied. `test_current` has no repeat message, so L11 refuses that load with 409 MSG-P3-027 "an approved version already has this valid from" (SPEC-006 (3)), and SPEC-008 and the partial unique index would refuse its approval anyway. Step (e) then rolls back a v3 that cannot exist. The spec also does not say that a current-state code can have only one approved version per day, so a same-day correction needs a rollback first. | spec.md:1032 (TC-TM-05), 290-291 (SPEC-006 (3)), 307 (SPEC-008 twin), 612 (L11), 223 (partial unique index) | TC-TM-05; SPEC-025 *Effective date* | Give v3 a later date (move the business date to 2026-12-04 before step (c)) or restructure the steps, and keep (e) as the rollback of the latest approved version. State in SPEC-025 *Effective date* and A-42 that a `CURRENT_STATE` code has at most one approved version per `validFrom`, so a same-day correction needs a rollback (if the handler supports it) or waits for the next date. |
| `REVIEW-RWB-E1-043-148` | Low | **RWB-E1-042 has moved past the revision-7 baseline, and the stated T-TE001-14 set is now stale.** Revision 8 (05:00) and revision 9 (05:16:37, after D-RUN-19 at 05:10) exist. Revision 9 adds `access.api.CatalogParameterReader` with a nested `Value` to the same test (its T-2: "(rev 9) + `CatalogParameterReader`"). SPEC-019 lists `access.api` exactly, the contract `tTe001_14` and R29 repeat that list, and TC-BD-01 makes the test fail "when a further public type is added". Built as written after RWB-E1-042 merges, T-TE001-14 would fail or need an edit that this spec does not describe. The path cited in §0 and A-25 (`.../INC-003-epic-1-RWB-E1-042/specify/spec.md`) now holds revision 9; revision 7 is kept as `spec.run6.md`. The names this story consumes are unchanged in revision 9 (verified). | spec.md:43, 456-469, 1036; shared-updates.md R29; backend-apis.json `p4HandlerSpi.tTe001_14`; E42S `spec.md` revision 9 line 948 (T-2), D-RUN-19 (build log line 42); E42S `spec.run6.md` | SPEC-019; TC-BD-01; R29; contract; §0; A-25 | Define the `access.api` expected set as RWB-E1-042's merged set plus this story's six SPI and LOV types, naming `CatalogParameterReader` (and its nested `Value`) as RWB-E1-042's under D-RUN-19. Cite revision 7 as `spec.run6.md`, or re-baseline on revision 9 and say what changed for this story (the T-TE001-14 set and the SPI wording of 149). |
| `REVIEW-RWB-E1-043-149` | Low | **Whether the `PARAMETER` route implements the P4 SPI is contradicted and not recorded.** D-RUN-18 says "P1 (RWB-E1-001) and P3 (RWB-E1-042) handlers implement it". RWB-E1-042 revision 9 (§4.3 seam row, A-51, plan input R7-1) says the `PARAMETER` implementation of the SPI is a P3 adapter in RWB-E1-043's package, `ParameterLoadBranch`, and names "RWB-E1-043 specifier" to confirm. This spec's R24 also says P3 "RWB-E1-042" handlers implement the SPI. But SPEC-021, SPEC-025 *Registration* and TC-HD-02 make a handler bean for `PARAMETER` fail start-up. SPEC-030 separates `PARAMETER` in the dispatcher, SPEC-026's `ParameterLoadBranch` implements no `access.api` type, and the contract's `implementedBy` leaves `PARAMETER` out. A builder who followed RWB-E1-042 or D-RUN-18 and made `ParameterLoadBranch` a `ReferenceTableHandler` for `PARAMETER` would get a context that does not start. This spec's route is coherent and meets RWB-E1-042's flag-off contract (`ObjectProvider`, 404). The departure from the ruling's wording and from RWB-E1-042's text is recorded nowhere. | Build log line 41 (D-RUN-18); E42S `spec.md` revision 9 line 144 and `assumptions.md` A-51; shared-updates.md:94 (R24); spec.md:495-496, 594, 712-719, 813-817, 1019; backend-apis.json `p4HandlerSpi.implementedBy` | SPEC-025, 026, 030; R24; contract; GAP rows | Choose one route and state it in SPEC-025 and SPEC-026. The spec's current choice (`PARAMETER` stays a dispatcher branch under D-RUN-10, is not an SPI handler, and a `PARAMETER` handler bean fails start-up) fits its design. Correct R24, record G5-R01, and add a shared-update row asking RWB-E1-042 to align §4.3, A-51 and R7-1 and asking the orchestrator to note the D-RUN-18 wording. If the SPI route is chosen instead, change the start-up rule, TC-HD-02 and the dispatcher together. |
| `REVIEW-RWB-E1-043-150` | Low | Housekeeping. (a) SPEC-024 says an identical reload of rolled-back content "returns the ROLLED_BACK load (SPEC-006 rule 1)". Since finding 140, rule (1) is the early repeat for handler codes with a repeat message, which answers 409, and the idempotent return is rule (2). A-27 states the same return without exceptions, but a handler code with a repeat message answers 409 (for example MSG-P1-011 for `data_product`), and any other code is refused 422 at L10 once `validFrom` has passed. (b) `backend-apis.json` top-level `source` still cites "RWB-E1-042 spec revision 5" (residual of 144); `consumedInterfaces.basis` is correct. | spec.md:542-544; assumptions.md A-27; backend-apis.json line 5 | Correct the reference to SPEC-006 rule (2) and qualify the reload sentence in SPEC-024 and A-27 for handler repeat messages and past dates; update the contract `source` to the RWB-E1-042 revision used. |

## RWB-E1-001 handler contract: completeness

| Point | Judgement | Where |
|---|---|---|
| Check order | Complete. L1-L15; `data_product` takes the early repeat (L9) and skips L12. | SPEC-025; §3.1 item 3 |
| What the handler supplies | Complete. P4 type, own flag, `keyColumns`, `validate`, `repeatMessage`, `apply`, `dating()` = `CURRENT_STATE`, `supportsRollback` per its story; imports nothing from `casewf`. | SPEC-025; §3.1 item 2 |
| Message pass-through | Complete. | SPEC-025; §3.1 item 4 |
| Repeat behaviour | Complete; order departure recorded (GAP-56). | SPEC-025 L9; §3.1 items 3, 7 |
| Seed rows | Complete. | §3.1 item 5; A-40 |
| LOV-REF-TABLE | Complete. No change. | §3.1 item 6 |
| Effective date | Complete. Current-state rule implementable on PS6 `data_product`; approval on the valid-from date writes the rows (S7-001 flow step 10). | SPEC-008, 025, 032 rule 6; §3.1 item 8; R31 |
| SPI home | Settled for the build by D-RUN-18 (`access.api`), pending tech-lead ratification (R24). | SPEC-019, 025 |

RWB-E1-001 can conform to this contract. None of findings 147-150 changes the SPI signature or what
RWB-E1-001 supplies.

## Document gaps not recorded by the specify stage

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why (blocker or not) | How this stage proceeded |
|---|---|---|---|---|---|---|
| G5-R01 | Run decision D-RUN-18 (`AI-SDLC-BUILD-LOG.md` decisions table line 41; orchestrator, Claude Code; not ratified) and RWB-E1-042 spec revision 9 §4.3 seam row and A-51 | The `PARAMETER` route is described as an implementation of the P4 handler SPI (in `ParameterLoadBranch`) | D-RUN-10 (build log; the dispatcher separates `PARAMETER` and calls `ParameterLoadHandler`); RWB-E1-043 spec revision 5 SPEC-021, SPEC-025 *Registration*, SPEC-030 and TC-HD-02 (a `PARAMETER` handler bean fails start-up) | No | Either route meets RWB-E1-042's flag-off contract; the spec only needs to choose one and say so | Finding 149 |

## Gate decision

There is no Critical, High or Medium finding, so nothing blocks the handoff by severity (`pdlc.md`). The
review status stays `FAIL`. Under D-RUN-09 the orchestrator does not accept a Low-only failure: the Technical
Specifier should fix 147-150 and record G5-R01, and this gate then re-runs as
`review/spec-gate-review-6.md`. Otherwise the Lows go to the engagement lead for a human disposition. No
finding needs a Blocker = Yes gap.

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 4]
REVIEW_STATUS: FAIL
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 4] (147, 148, 149, 150)
BLOCKING: NO by severity; not accepted under D-RUN-09 (fix and re-gate, or route to the engagement lead for a human disposition)
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
ROUND_4_FINDINGS: 138-146 resolved (144 residual in 150 (b)); G4-R01..G4-R03 carried in as GAP-54..GAP-56
D_RUN_18: applied as a run ruling (SPI in access.api, registry in P3, no cycle); no ratification claimed anywhere; PARAMETER wording conflict open (149)
RWB_E1_001_CONTRACT: COMPLETE (check order, supply, pass-through, repeat, seed rows, LOV-REF-TABLE, effective date, SPI home pending ratification)
DOCUMENT_GAPS_ADDED: 1 (G5-R01; no blocker)
NEXT_STEP: Orchestrator triage of 147-150 (Technical Specifier remediation run 5, then review/spec-gate-review-6.md; or route to the engagement lead for a human disposition under D-RUN-09)
```

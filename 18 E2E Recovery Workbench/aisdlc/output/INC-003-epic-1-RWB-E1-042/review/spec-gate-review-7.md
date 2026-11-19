# Spec gate review 7: RWB-E1-042 (RUN_ID `INC-003-epic-1-RWB-E1-042`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-042-SPEC-009` |
| Gate | Specification gate, re-review of revision 8 (round 7) |
| Artifacts under review | `specify/spec.md` revision 8 (1163 lines), `assumptions.md` (A-01 to A-51), `document-gaps.md` (E1042-SP-DG-01 to -17; none added in rev 8), `shared-updates.md` (rev 8 rows), `compliance-validation.md`, `gate-response.md` (Rounds 1-6), `agent-run-log.md` (runs 1-6). No `contracts/` folder (spec §20 explains why) |
| Compared with | `review/spec-gate-review-6.md` (`REVIEW-RWB-E1-042-SPEC-008`: Lows 149-150, plan inputs 1-4), `review/spec-gate-review-5.md` (Lows 143-148); revision 7 snapshots `specify/*.run6.md` |
| Run decisions | D-RUN-07 to D-RUN-18, `AI-SDLC-BUILD-LOG.md` decisions table lines 30-41; D-RUN-18 at line 41 and timeline line 243 (2026-11-18T04:55:55) |
| Cross-story specs read | RWB-TE-001 spec v4 ("TE1S": SPEC-022 (a)-(h), field-level matrix line 114, `shared-updates.md` SU-02, SU-08, SU-09, SU-14); RWB-E1-044 spec v14-7 ("E44S", on disk 01:35, passed at review-7 04:59: SPEC-007 line 227, SPEC-014 lines 359-375, SPEC-016 line 398, T-044-21 line 526); RWB-E1-043 spec revision 4 ("E43S", on disk 01:24; remediation run 4 started, `*.run4.md` snapshots 04:57, `spec.md` not yet changed: SPEC-018 line 385, SPEC-019 lines 415-426, SPEC-025 line 505, SPEC-026 line 634; review-4 finding 141) |
| Document set | Story files v7 RWB-E1-042 v1 (lines 47, 237, 318), RWB-E1-011 v1 (lines 18, 91, 113, 303), RWB-E1-037 v1 (lines 18, 46), RWB-E1-028 v2 (line 54); Error and Message Standard v4 (lines 19, 56, 68-208); Build Sequence v6 working copy |
| Repository | Read only; not changed by this review |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18 |
| Supersedes | `REVIEW-RWB-E1-042-SPEC-008` for revision 8. That review stays as history. |

## Status

**`SPEC_GATE: FAIL`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 0 | |
| Low | 4 | Visible; Low-only failure (REVIEW_GATE_WARNING). Under D-RUN-09 the orchestrator does not accept it |

Revision 8 resolves both review-6 findings (149, 150), and 143-148 stay resolved. D-RUN-18 is applied correctly where
the spec names it. The business-date seam in §4.3 now allows a P3 → P1 read. The handler SPI is placed in P4
`access.api`, and RWB-E1-043 implements it later (A-51). This story's own placement adds no module cycle under the
TE1S v4 map.

Four new Lows remain:

- 151: D-RUN-18 has a consequence for this story's own published service that the spec does not record. The spec
  bans a P1 → P3 edge, yet it seeds a P1 consumer of `ParameterService` and still says "other modules" read through
  `casewf.config.api`.
- 152: The new §4.3 option to put the SPI on `ParameterLoadHandlerImpl` is not reconciled with the SPEC-021
  flag-off contract.
- 153: The rollback write of `updated_by` has no test.
- 154: Housekeeping. Several build-log timeline line citations have drifted, and A-28 is stale.

## 1. Earlier findings 143-150: verification

| Finding | Verdict | Evidence in revision 8 |
|---|---|---|
| 143 Tooling coverage on a withdrawn task | **Resolved** | §12.11: "They are measured in RWB-TE-001's one combined bundle (finding 143): `recoveryCoverageReport` and `recoveryCoverageVerification` carry one `BUNDLE` rule, `LINE`, `INSTRUCTION`, `BRANCH` and `METHOD` each at 0.80". The same section continues: "No new task, rule, counter or threshold; no `recoveryToolingCoverageVerification` (withdrawn, E44S line 375)". Checked against E44S line 375 ("Withdrawn from v14-4") and line 369 (the `classDirectories` addition). |
| 144 `detail` on the new form; RWB-TE-003 told | **Resolved** | §10.2 has "`ApiProblemException(HttpStatus status, String messageId, Map<String, String> placeholders, String field, String detail, Throwable cause)`", with guards ("`messageId` may be null only when `status` is 503"). The rev 7 RWB-TE-003 row is in `shared-updates.md` line 37. E43S rev 4 line 74 ("No change to ... `ApiProblemException` ... beyond what RWB-E1-042 delivers") still holds. |
| 145 Business-date seam P3 → P1 | **Resolved; superseded by D-RUN-18** | The §4.3 row (line 148) says: "Under D-RUN-18 [S-14] this is allowed: the reference-load handler SPI is published by P4 `access.api`, so P1 handlers add no P1 → P3 edge". A residual consequence is finding 151. |
| 146 TC-29 (b) asserts handler output | **Resolved** | TC-29 (b) (line 1006): "rendering and the handler's log line are TC-30's (finding 146)". TC-30 is a unit test in `access.internal`. |
| 147 §7.3 missing columns | **Resolved** | §7.3 lines 298-301 have `created_at`, `created_by`, `is_active` and `state`, as Physical Schema v6 `parameter_value` defines them. |
| 148 Housekeeping | **Resolved** | S-14 cites "Build log §1 lines 30-36 (D-RUN-07 to -13), 38 (D-RUN-15), 40 (D-RUN-17), 41 (D-RUN-18)". All four were verified against the build log. §12.14 is headed "reviews 3 to 6". |
| 149 Load-side `created_by` test | **Resolved** | TC-40 (line 1017): "each written row has `created_by` = `author_user_id`, `is_active` true, `state` NULL, `created_at` set". TC-11 (line 988): "after approval each v2 row keeps `created_by` = the author and has `updated_by` = the approver". TC-13 (line 990) now covers seed rows only, and "(TC-05)" is gone. The rollback side is not covered (finding 153). |
| 150 (a) class-set wording | **Resolved** | §2 (line 80): "the test-output classes of `architecture.parameters` added to `classDirectories` of RWB-TE-001's combined coverage bundle". §14 (line 960): "not in the combined bundle's class directories". A search finds no "class set" in `spec.md`. |
| 150 (b) E43S revision | **Resolved, with residual (154 b)** | Line 28: "'E43S' is the RWB-E1-043 spec revision 4". S-22: "RWB-E1-043 spec revision 4, in remediation". A-28 still says "revisions 2 and 3" (154 b). |
| 150 (c) E44S line citations | **Resolved** | S-23 cites "SPEC-007 line 227, SPEC-014 lines 359-375, SPEC-016 line 398, T-044-21 line 526". Each line was checked in E44S v14-7: 227 is the SPEC-007 heading, 359 the SPEC-014 heading, 375 "Withdrawn from v14-4", 398 the SPEC-016 heading, and 526 the T-044-21 row. |

## 2. D-RUN-18: how it is applied

D-RUN-18 (build log line 41) says the SPI that RWB-E1-043's registry calls is "published by P4 (`access.api`)". It
goes on: "P1 (RWB-E1-001) and P3 (RWB-E1-042) handlers implement it", "No P1 to P3 edge is allowed", and the P3 to
P1 reads that the story files plan "stay legal, so the business-date seam of RWB-E1-042 §4.3 may be filled by a P3 to
P1 call". The decision was made by the orchestrator (Claude Code), and ratification by the tech lead is open.

| Check | Result | Evidence |
|---|---|---|
| §4.3 business-date row | Consistent | Line 148 allows "a P3 → P1 read" and says "No P1 → P3 edge is ever added; no class in another module implements this P3 interface". It cites TE1S SPEC-022 (d) and D-RCV-11, and RWB-E1-028 flow step 3. That step was verified: story v7 RWB-E1-028 line 54 reads "through the P1 interface", and the story's module is P3 (line 18). The row also says "pending ratification by the tech lead", so no ratification is claimed. |
| §4.3 first seam row (SPI) | Consistent with D-RUN-18; one gap (152) | The row says the SPI "is published by P4 `access.api`", that RWB-E1-043 delivers it (order 8), and that this story "cannot implement it now (D-RUN-08)". The added edge is "only a P3 → P4 edge that already exists". The option to implement it "on `ParameterLoadHandlerImpl`" is finding 152. |
| A-50, A-51 | Consistent | A-50: "no P1 → P3 edge exists because the reference-load handler SPI is published by P4 `access.api`"; it is confirmed by "Tech lead (ratifies D-RUN-18)". A-51: "RWB-E1-043 makes the `PARAMETER` handler implement it in P3 `casewf` and extends T-TE001-14's `access.api` set". |
| shared-updates seam row (line 26) and RWB-E1-043 row (line 32) | Consistent | Line 26: "(rev 8) per D-RUN-18 the fill may be a P3 → P1 read ... no P1 → P3 edge". Line 32 (rev 8) carries the SPI to RWB-E1-043. |
| TE1S SPEC-022 (d) | Consistent | TE1S (d) says "P3 depends on P2 and P4, so neither `integration` nor `access` may depend on `casewf`". It also says "Today no P3 → P1 edge exists". D-RUN-18 adds a future P3 → P1 edge and forbids P1 → P3, so TE1S (d) holds as long as no P1 → P3 edge appears. Finding 151 shows a planned one. |
| Module cycle from this story's placement (TE1S v4 map) | **No cycle** | After TE1S, the edges are `casewf.rules` → `integration.flags.api` and `casewf.admin` → `access.api`, and no other. This story adds `casewf.config` → `access.api`, which is P3 → P4 and already exists. `MessageResolver`, `CapabilityCheck` and the new `ApiProblemException` constructor refer only to JDK and Spring types. The interim implementations stay in `access.internal`, and no P4 type names a P3 type (§12.1, SPEC-026). The `@PreAuthorize` SpEL bean reference is not a type dependency. Nothing in this story touches P1, P2 or P7. T-TE001-14 is extended, not relaxed (TC-45, A-41). |

## 3. New findings

| ID | Severity | Finding |
|---|---|---|
| `REVIEW-RWB-E1-042-151` | Low | Under D-RUN-18 and TE1S SPEC-022 (d), modules P1, P2 and P4 may not call `casewf.config.api`. Yet the spec seeds a P1 consumer, tells "other modules" to read through it, and records no open item for the planned P1 and P4 readers |
| `REVIEW-RWB-E1-042-152` | Low | §4.3 lets RWB-E1-043 put the P4 SPI on `ParameterLoadHandlerImpl`, a conditional bean in this story's internal package. That path bypasses the SPEC-021 flag-off contract and the TC-22 consumer pattern |
| `REVIEW-RWB-E1-042-153` | Low | §7.3's rollback write (`updated_by` = caller, `version` +1) has no test |
| `REVIEW-RWB-E1-042-154` | Low | Housekeeping: build-log timeline line citations have drifted, A-28 and §4.3 cite a superseded E43S triage, and a sentence in §20 is repeated |

### REVIEW-RWB-E1-042-151 (Low): `ParameterService` consumers outside P3 are not reconciled with D-RUN-18 and TE1S SPEC-022 (d)

**Maps to:** SPEC-026 (line 184, "Other modules use only `casewf.config.api` and `access.api`"); §12.1 (line 550, "Other
modules read values only through `casewf.config.api` (GR3)", and line 551, "Callers of `casewf.config.api` sit in P3");
§4.3 business-date row (line 148, "no P1 ↔ P3 cycle can form"); §6 GR3; §12.4 `used_by` row for
`recon.caselist.tolerance.pct` (line 713); TC-41; A-50.

**Evidence:**

- §12.4 seeds `recon.caselist.tolerance.pct` with `used_by` = `recovery.dataengine.caselist`. `dataengine` is P1
  (TE1S module list; Build Sequence v6 lists P1 as "Recovery data engine"). TC-41 asserts this value.
- D-RUN-18 (build log line 41) says "No P1 to P3 edge is allowed". TE1S SPEC-022 (d) says neither P2 nor P4 "may
  depend on `casewf`". The §4.3 recorder seam also plans P3 → P7, so a P7 caller would close a cycle too (§4.3 line
  144).
- Story files v7 plan readers outside P3:
  - RWB-E1-011 v1 has module "P1 Recovery data engine" (line 18). Line 303 reads "Parameters `recon.tolerance.pct`
    ... `case.entry.dpd` from the parameter catalog", and AC lines 91 and 113 change the tolerance by reference load.
    Its build order is 57.
  - RWB-E1-037 v1 has module "P4 Access and administration" (line 18). Line 46 reads "Parameters
    `rwb.refload.approver.permission` ... are in the parameter catalog (RWB-E1-042)". Its build order is 27.
- Story v7 RWB-E1-042 line 318 says "other modules read values only through ParameterService", and line 47 says "code
  reads a value only through ParameterService".
- The spec says two incompatible things. Line 551 says "Callers of `casewf.config.api` sit in P3". Line 184 and line
  550 say "Other modules" use `casewf.config.api`. §4.3 concludes that "no P1 ↔ P3 cycle can form", but checks only the
  handler side and not the readers of this story's own service. No open item, shared-updates row or gap tells the
  RWB-E1-011 or RWB-E1-037 owners, or the tech lead ratifying D-RUN-18.

**Failure scenario:** RWB-E1-011 (P1) follows story line 303 and the spec's GR3 note. It injects `ParameterService`
to read `recon.tolerance.pct`. That adds P1 → P3. Once the business-date reader adds P3 → P1, as D-RUN-18 now allows,
`ModulithTest` rejects the cycle (D-RCV-11). Alternatively, P1 hard-codes the tolerance, which breaks AGENTS §3.2 and
§4.8. RWB-E1-037 (P4) hits the P3 ↔ P4 cycle at once, because P3 already depends on P4. Either story finds the
problem at build time, not at spec time. The spec that publishes the service is the place to say who may call it.

**Why Low:** This story's code and build are not affected, and nothing in this story adds the edge. The defect is an
unrecorded cross-story constraint and an internal contradiction in the spec text. It has the same shape as findings
145 (this story) and 141 (E43S), both rated Low.

**Fix required:**

1. State one rule in SPEC-026, §12.1 and the GR3 note. Callers of `casewf.config.api` are P3 code, or modules that
   P3 does not depend on now or by a planned seam. The rule excludes P1 (D-RUN-18), P2 and P4 (TE1S SPEC-022 (d)) and
   P7 (§4.3 recorder seam). Remove "Other modules use only ..." or qualify it.
2. Qualify the §4.3 "no P1 ↔ P3 cycle can form" sentence. It holds only if no P1 code reads `ParameterService`.
3. For the seeded `recovery.dataengine.caselist` `used_by` entry, keep the pack value as metadata. Record that a P1
   reader cannot call `ParameterService` directly.
4. Add an open item, and shared-updates rows to the RWB-E1-011 and RWB-E1-037 specifiers and to the tech lead with
   the D-RUN-18 ratification. How P1, P2 and P4 code reads catalog parameters is undecided. One option follows the
   D-RUN-18 pattern: a read port published by the lower module and implemented in P3. Another is for a P3 caller to
   pass the value in. Do not decide it here.
5. Record the document conflict below (RV7-DG-01).

### REVIEW-RWB-E1-042-152 (Low): the SPI-on-`ParameterLoadHandlerImpl` option bypasses the flag-off contract

**Maps to:** §4.3 first seam row (line 142, "on `ParameterLoadHandlerImpl` or a P3 adapter that delegates to
`ParameterLoadHandler`"); SPEC-021 (1), (2); §12.12 bean table; TC-22; A-27, A-51; `shared-updates.md` lines 27 and 32.

**Evidence:**

- `ParameterLoadHandlerImpl` carries `@ConditionalOnProperty(... "configservice" ...)` (§12.2, §12.12). When the flag
  is off it is absent.
- D-RUN-18 says the registry "collects the beans by that P4 type". If the SPI sits directly on
  `ParameterLoadHandlerImpl`, then with the flag off no `PARAMETER` handler bean exists for the registry to collect.
  What the caller receives then depends on how RWB-E1-043 treats a table code with no handler bean. The spec does not
  say.
- SPEC-021 states the contract for this case. Consumers obtain the handler "only through
  `ObjectProvider<ParameterLoadHandler>`", and the consumer refuses `PARAMETER` with 404 MSG-P4-003. TC-22 tests that
  probe pattern. The direct-SPI option takes neither path, and neither SPEC-021 nor TC-22 covers it.
- The two designs do not match. E43S rev 4's SPI (`ReferenceTableHandler`, SPEC-025 line 505) has the registry
  assign the `loadId` (`apply(UUID loadId, ...)`). `ParameterLoadHandler` creates its own `load_id` and runs its own
  approve and rollback (SPEC-012 to -015). E43S rev 4 SPEC-026 (line 634) therefore keeps a separate adapter,
  `ParameterLoadBranch` (P3 `casewf.refdata.internal`), which uses `ObjectProvider`.
- The direct option also means RWB-E1-043 edits this story's internal class in `casewf.config`. That is the same
  module, but a different story's internals.

**Failure scenario:** RWB-E1-043's remediation for D-RUN-18 takes the first option this spec offers. It adds the P4
SPI to `ParameterLoadHandlerImpl`. With `rwb.p3.configservice` off, `PARAMETER` silently drops out of the registry. A
`PARAMETER` load then gets the registry's unknown-code answer (for example a 422 LOV-REF-TABLE refusal), not the
404 MSG-P4-003 that SPEC-021, A-27 and E43S TC-PB-01 and TC-FL-01 specify. TC-22 still passes, because it tests only
the `ObjectProvider` probe.

**Fix required:** Choose one of these.

- Name a single route. The `PARAMETER` SPI implementation is a P3 adapter in RWB-E1-043's own package. It obtains
  `ParameterLoadHandler` only through `ObjectProvider` and refuses with the SPEC-021 problem when the handler is
  absent. This keeps SPEC-021, TC-22 and E43S SPEC-026 valid.
- Keep the direct option, but state its flag-off result in SPEC-021, A-27 and shared-updates row 27. The result is no
  `PARAMETER` bean, with RWB-E1-043 refusing an unhandled `PARAMETER` code with 404 MSG-P4-003. Also state that the SPI's
  `loadId` and lifecycle must match `ParameterLoadHandler`'s.

### REVIEW-RWB-E1-042-153 (Low): the rollback audit write has no test

**Maps to:** §7.3 row `version, updated_at, updated_by` (line 302: on rollback "+1, now, caller"); SPEC-015, SPEC-027;
TC-10, TC-19, TC-37, TC-39; finding 149, which closed the load and approve sides.

**Evidence:** TC-10 (a) asserts "v1 in force, 90; v2 ROLLED_BACK" and the cache rebuild. TC-39 asserts
`rollback_reason`. TC-19 and TC-37 are refusals. No test asserts that after a successful rollback `updated_by` equals
the caller and `version` has gone up by one. The caller is the third personal identifier §7.3 introduces, and
SPEC-027 covers it.

**Failure scenario:** A builder writes `ROLLED_BACK` and the reason but leaves `updated_by` as the approver, or skips
the optimistic-lock increment. No test fails. The audit trail then names the wrong person for the rollback, which is
the same drift finding 149 closed for load and approve.

**Fix required:** In TC-10 (a), roll back with a caller that is a synthetic UUID distinct from the author and the
approver. Assert that each rolled-back row has `updated_by` = the caller, `created_by` unchanged and `version` = the
previous value + 1. Do not use the UUID in any log assertion (SPEC-027).

### REVIEW-RWB-E1-042-154 (Low): housekeeping

**Maps to:** S-14 (line 50); S-24 (line 60); §4.3 first row (line 142); SPEC-016 (line 174); §12.9 (line 803); §14
(line 960); A-04, A-27, A-28; §20 (line 1158).

**Evidence:**

- (a) The build-log decisions table has grown, with D-RUN-14 to D-RUN-18 added above the timeline, so the timeline
  line citations have moved:

  | Citation | Points to now | Should point to |
  |---|---|---|
  | "line 140" (triage item (f), cited as "Gate triage (late record)"; SPEC-016, §12.9, A-04, S-14) | RWB-TE-011's round-4 gate | Line 145 (2026-11-18T00:09:40, "Gate triage (late record)") |
  | "line 141" (finding 119 triage; S-14, A-27) | RWB-TE-011's triage | Line 146 |
  | "line 91" (S-14) | RWB-TE-003's gate | The 23:26 triage is line 96 |
  | "line 120" (D-RCV-40 outside `check`; S-24, §14) | The D-RUN-11 to -13 row | The TE-003 triage citing D-RCV-40 is line 125 |
  | "line 193" (§4.3, A-28) | RWB-E1-043's round-3 gate | The run-3 triage is line 194 |

  Line 243 (D-RUN-18) is correct.
- (b) A-28 still says "as E43S revisions 2 and 3 state it" and "build log timeline line 193: its run 3 rebases on TE1S
  SU-08". §4.3 (line 142) calls the same row "RWB-E1-043's current triage". The current E43S triage is its run 4 under
  D-RUN-18 (timeline line 242, 04:55:55), and E43S is at revision 4.
- (c) §20 line 1158 repeats "Housekeeping (148)."

**Failure scenario:** A planner or auditor who follows a line citation lands on another story's row. One example is
the readiness rule's authority, "triage item (f)", which would lead to a RWB-TE-011 gate row.

**Fix required:** Cite build-log timeline rows by timestamp and action, for example "2026-11-18T00:09:40, Gate triage
(late record)", not by line number. The decisions table will keep growing. Update A-28 and the §4.3 row to E43S
revision 4 and its run-4 triage (04:55:55). Remove the repeated sentence.

## 4. Plan inputs (not findings)

1. **E43S under D-RUN-18.** When RWB-E1-043's revision 5 passes its gate, check three things. The `PARAMETER` route to
   the P4 SPI must keep the SPEC-021 flag-off result (152). The SPI's `loadId` and approval lifecycle must not create a
   second load record next to `parameter_value.load_id`. E43S must add no P4 change beyond the SPI and its
   `ListOfValuesReader`, and must extend T-TE001-14's `access.api` set as A-41 describes.
2. **D-RUN-18 ratification.** The §4.3 business-date route rests on a decision that the tech lead has not yet ratified.
   If the decision changes, revert the §4.3 row to the revision 7 constraint, which prescribed no route. The plan
   prescribes no business-date route in any case: that is the later story's work.
3. **CLAR-025.** The plan must not start code before the analyst's decision on the two-module scope (AGENTS §7). See §5.
4. **Review-6 plan inputs 1-4** are carried as §12.14 R6-1 to R6-4. They were checked and need no further action at
   the spec stage.

## 5. CLAR-025 (two-module plan, AGENTS §7)

| Check | Result | Evidence |
|---|---|---|
| Recorded as open | Yes | The CLAR-025 row (line 1103) reads "OPEN (analyst; before the build)". Also: `shared-updates.md` line 34 ("Analyst to decide on the two-module scope before any code is written"), A-33 and E1042-SP-DG-16 (Blocker = No) |
| No approval claimed | Yes | Line 1103: "The spec continues; no analyst approval is claimed". Line 34: "no analyst approval is claimed". §12.1 line 551: "not presumed approved". None of the run's files records a human approval or ratification. |
| Reason stated, with citations | Yes | The plan changes P3 `casewf` and P4 `access`: two new `access.api` types and the additive `ApiProblemException` constructor with its rendering. Cited: AGENTS §7 ("goes back to the analyst before any code is written") and §9 ("touches one module"), TE1S SU-08 (c) and (d) ("Place such types in `access.api`"), and D-RCV-11 (the resolver cannot sit in P3, because `ProblemFactory` calls it and P4 may not depend on P3). The quotes were checked against `AGENTS.md` §7 and §9 and TE1S `shared-updates.md` SU-08. |
| D-RUN-18 changes the module count | No | The SPI is RWB-E1-043's (A-51). This story adds no P1 or P7 code. |

## 6. Checks performed

| Check (compliance-reviewer.md) | Result |
|---|---|
| Authentication and authorisation | `GET /admin/parameters` has a method check through `CapabilityCheck` (bean `capabilityCheck`, area "Rules and parameters", R). 401 comes from `SecurityConfig`. The C, A and U rights are checked on RWB-E1-043's endpoint (D-RUN-10). No defect. |
| Customer and account data protection | No customer data. Author, approver, caller and the audit columns are treated as personal (SPEC-027, SP-DG-15, -17). The rollback-side test is missing (153). |
| Audit logging | AC-VERS goes through the recorder inside the approval transaction, with 503 MSG-P7-003 on failure. The handler branch logs no cause text (D-RUN-15). No defect. |
| KYC, AML, suitability, consent, approval | Out of scope beyond maker-checker (SPEC-014 and a DB check). |
| Frontend integration and error contract | No frontend (§13). The Problem forms and `detail` override match E43S rev 4 (SPEC-025 L13). |
| Message IDs | All IDs used exist in Error and Message Standard v4 at the cited lines (68, 69, 71, 73, 76, 139, 151, 156, 163, 164, 165, 207, 208), and their placeholders match. The Thai text status is "Proposed" (line 19). No invented ID. |
| No literal business values | Seed values are data in the migration. HTTP statuses use `HttpStatus` constants. Schema limits are named constants in the baseline file. The magic-number ratchet is in place (SPEC-004). No defect. |
| Secrets and environment configuration | Secrets are listed and never served, under one credential-name rule. No defect. |
| AC → requirement → test coverage | AC1-AC11, BR1-BR7, X1-X10, FL1-FL10, ST1-ST3, CON1-CON5 and GR1-GR4 are all mapped to SPEC items and tests. TC-12 is honestly marked `Blocked`. The gap is the rollback audit write (153). |
| 80% gate per changed surface | Backend is REQUIRED: four counters at 0.80 in one bundle, from `test` data, outside `check`. The tooling joins the bundle, and the generator exception is recorded (A-38). Frontend is `NOT_APPLICABLE`, with evidence. Planned, not measured, which is correct at the spec stage. |
| Migration rules (D-RCV-28, D-RUN-07, -12, -13) | One file, `<seq>` assigned at merge, `${recoverySchema}`, guarded DDL, PRE-6. No defect. |
| Module boundaries (D-RUN-08, -10, -11, -18; TE1S) | This story's placement adds no cycle (§2). D-RUN-18 is applied in §4.3, A-50, A-51 and the shared-updates rows. Gaps: the consumer-side consequence (151) and the flag-off route (152). |
| Consistency with E44S v14-7 (PASS) | Coverage wiring matches SPEC-014 line 369. The lint dependency matches SPEC-007 and T-044-21. No conflict. |
| Consistency with E43S rev 4 (in remediation) | Imports, `ObjectProvider` flag-off, 404 MSG-P4-003, the `detail` override and the P3 caller (`ParameterLoadBranch`, SPEC-026) all match. The D-RUN-18 SPI route is open on both sides (152, plan input 1). |
| D-RCV-35 / D-RCV-36 | No `public` read and no Temporal or Drools call. The six keys are catalogued. |
| Personal data in this run's files | None found. The only UUID is the synthetic seed identity, and "U-41" is a synthetic label. |
| Triage attribution | Triage is credited to the orchestrator (Claude Code). D-RUN-18 is marked pending ratification. No human approval is recorded. |
| MCP | None connected; N/A. |

**Observation (not a finding against this spec):** The build-log row at 2026-11-18T05:00:32 for remediation run 6
says "SP-DG-17 added". `document-gaps.md` (rev 8 header) says revision 8 "adds none". SP-DG-17 was added in revision
6. The orchestrator may want to correct the log by appending a row.

## 7. Document-gap candidates

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why | How this stage proceeded |
|---|---|---|---|---|---|---|
| E1042-RV7-DG-01 | User Stories Epic 1 Story Files v7, RWB-E1-042 v1 (`legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-042-central-configuration-service-and-parameter-catalog-v1.md`) line 237 (service in P3 `recovery.casewf.config`), line 318 ("other modules read values only through ParameterService") | Readers in P1 and P4 are planned to read catalog parameters. Under the dependency direction that the run follows, they cannot call a P3 service: TE1S SPEC-022 (d) says P4 may not depend on P3, and D-RUN-18 says "No P1 to P3 edge is allowed" | Same story files v7: RWB-E1-011 v1 (module P1, line 18; line 303, "Parameters `recon.tolerance.pct` ... from the parameter catalog") and RWB-E1-037 v1 (module P4, line 18; line 46, "Parameters `rwb.refload.approver.permission` ... are in the parameter catalog (RWB-E1-042)") | No | Not for RWB-E1-042. The precedence (story file v7 §13) settles where the service lives, and this story's build is unaffected. The readers are later stories (Build Sequence v6 orders 27 and 57). How they read parameters is a tech-lead decision, alongside the D-RUN-18 ratification | Raised as finding 151. The spec is to state who may call `casewf.config.api` and to record an open item for the RWB-E1-011 and RWB-E1-037 owners and the tech lead |

## Gate decision

```text
REVIEW_STATUS: FAIL
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 4] (151, 152, 153, 154)
BLOCKING: NO by severity; not accepted under D-RUN-09 (fix and re-gate, or route to the engagement lead for a human disposition)
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
EARLIER_FINDINGS: 143-150 resolved (150 (b) residual in 154 (b))
D_RUN_18: applied in §4.3, A-50, A-51 and shared-updates; no module cycle from this story's placement; consumer-side consequence open (151); flag-off route open (152)
CLAR_025: OPEN to the analyst; no approval claimed; reason and citations present
PLAN_INPUTS: 4
DOCUMENT_GAP_CANDIDATES: 1 (E1042-RV7-DG-01, Blocker = No)
NEXT_STEP: Orchestrator triage of 151-154 (Technical Specifier revision 9, then spec-gate-review-8.md; or route to the engagement lead for a human disposition under D-RUN-09)
```

SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 4]

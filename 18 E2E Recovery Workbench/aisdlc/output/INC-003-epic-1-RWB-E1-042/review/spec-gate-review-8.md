# Spec gate review 8: RWB-E1-042 (RUN_ID `INC-003-epic-1-RWB-E1-042`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-042-SPEC-010` |
| Gate | Specification gate, re-review of revision 9 (round 8) |
| Artifacts under review | `specify/spec.md` revision 9 (1202 lines), `assumptions.md` (A-01 to A-53), `document-gaps.md` (E1042-SP-DG-01 to -18), `shared-updates.md` (rev 9 rows), `compliance-validation.md`, `gate-response.md` (Rounds 1-7), `agent-run-log.md` (runs 1-7). No `contracts/` folder (spec §20 explains why) |
| Compared with | `review/spec-gate-review-7.md` (`REVIEW-RWB-E1-042-SPEC-009`: Lows 151-154, plan inputs 1-4, candidate E1042-RV7-DG-01); revision 8 snapshots `specify/*.run7.md` (full diff of all seven files read) |
| Run decisions | D-RUN-07 to D-RUN-19, `AI-SDLC-BUILD-LOG.md` decisions table. D-RUN-19 is dated 2026-11-18T05:10 in the table, with the timeline row "2026-11-18T05:10:44, ALL, Decision". The triage row is "2026-11-18T05:10:44, RWB-E1-042, Gate triage, REMEDIATE (D-RUN-09)". Both D-RUN-18 and D-RUN-19 were made by the orchestrator (Claude Code), and both are unratified |
| Cross-story specs read | RWB-TE-001 spec v4 ("TE1S": SPEC-022 (d), SPEC-025, T-TE001-14, field-level matrix line 114). RWB-E1-043 spec ("E43S"): revision 4 (`spec.run4.md`, lines 536-538) and revision 5 (`spec.md`, on disk at 05:09, not yet logged DONE or gated): lines 398-402, 591-596, 712-719, 813-817. RWB-E1-044 spec v14-7 (no change relied on in rev 9) |
| Document set | Story files v7: RWB-E1-042 v1 (lines 237, 318), RWB-E1-011 v1 (lines 18, 34-49, 303), RWB-E1-037 v1 (lines 18, 46) |
| Repository | Read only; not changed by this review |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18 |
| Supersedes | `REVIEW-RWB-E1-042-SPEC-009` for revision 9. That review stays as history. |

## Status

**`SPEC_GATE: FAIL`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 0 | |
| Low | 4 | Visible; Low-only failure (REVIEW_GATE_WARNING). Under D-RUN-09 the orchestrator does not accept it |

Revision 9 resolves 151, 153 and 154. It resolves 152 in substance: the conditional-bean option is gone, the route
follows SPEC-021, and TC-22 (b) and a reflection check are added. D-RUN-19 is applied the way the decision
states it. No ratification or human acceptance is recorded anywhere (CLAR-027 is OPEN). This story's own
placement still adds no module cycle.

The four new Lows come from the revision 9 changes:

- 155: The §4.3 row, A-51 and the rev 9 shared-updates row call RWB-E1-043's `ParameterLoadBranch` "the `PARAMETER`
  implementation of the SPI". E43S (revisions 4 and 5) has no such implementation. In E43S a `PARAMETER` handler
  bean fails start-up, and `PARAMETER` goes through a separate dispatcher branch. The spec also still cites E43S
  revision 4, although revision 5 is on disk.
- 156: The new `CatalogParameterReader.get` requires a `businessDate`. A P4 caller such as RWB-E1-037 has no legal
  source for it: `BusinessDateProvider` is in P3, and the batch-status reader is in P1.
- 157: `CatalogCompletenessCheck` is said to treat string keys passed to `CatalogParameterReader.get` as key reads.
  That rule is not in SPEC-003, and no test covers it.
- 158: Housekeeping. Some "two `access.api` types" wording is stale. `CatalogParameterReaderImpl` is missing from the
  §12.1 types and the §12.12 bean table, and §12.4 has an annotation inside its column of exact values.

## 1. Earlier findings 151-154: verification

| Finding | Triage (2026-11-18T05:10:44) | Verdict | Evidence in revision 9 |
|---|---|---|---|
| 151 Readers outside P3 | Settled by D-RUN-19. P4 `access.api` read interface implemented in P3 `casewf.config`. P3 callers may use `casewf.config.api`. No P1/P2/P4 → P3 edge. Seeded consumer on the interface. R rows to RWB-E1-011, RWB-E1-037 and RWB-TE-001 T-TE001-14. Open item for ratification. Gap kept, Blocker = No | **Resolved** (new residuals 156, 157) | SPEC-026 (line 186) now has a single caller rule: "`casewf.config.api` is called only by P3 code; every module outside P3 ... reads catalog parameters only through `access.api.CatalogParameterReader`". The old "Other modules use only ..." sentence is gone. §12.1 prose and GR3 (line 246) match. §4.3 business-date row (line 150) is qualified: "P1 parameter readers use the P4 `CatalogParameterReader` ... so no P1 ↔ P3 cycle can form". §12.2 (lines 601-634) defines the interface and how it behaves. §12.4 annotates the `recovery.dataengine.caselist` consumer. TC-45 extends the expected `access.api` types, and TC-46 is new. `shared-updates.md` line 38 (R row to RWB-E1-011, RWB-E1-037 and any P1/P2 reader), line 39 (ratification), line 80 (story line 318 reword) and line 83 (T-TE001-14). CLAR-027 is "OPEN (non-blocking; recovery tech lead)". E1042-SP-DG-18 carries the review-7 citations, Blocker = No. The interface matches D-RUN-19 as the decisions table states it ("published by P4 (`access.api`) and implemented in P3 `casewf.config`"). |
| 152 SPI option on conditional bean | Remove the option. The SPI follows SPEC-021 (`ObjectProvider`, then 404 MSG-P4-003). TC-22 covers the SPI path | **Resolved in substance; wording residual (155)** | §4.3 line 144: "`ParameterLoadHandlerImpl` never implements the SPI or any other `access.api` type, and no other story edits it". The route obtains the handler "only through `ObjectProvider<ParameterLoadHandler>`" and refuses with 404 MSG-P4-003. TC-22 (line 1029) adds (b): a test-only adapter, flag off 404 MSG-P4-003 with nothing written, flag on delegates, and a reflection check that `ParameterLoadHandlerImpl` implements no `access.api` interface. A-51 and `shared-updates.md` line 32 (rev 9) match. The flag-off result is now fixed. What the text says the route *is* does not match E43S (155). |
| 153 Rollback write untested | Add a test | **Resolved** | TC-10 (line 1017): "the rollback caller is a synthetic UUID distinct from the author and the approver, and each rolled-back row has `updated_by` = the caller, `created_by` unchanged and `version` = its previous value + 1 ... no UUID in any log assertion". This is the fix review-7 asked for. |
| 154 Housekeeping | As review-7 stated; build-log rows cited by timestamp and stage | **Resolved, with residual (155, E43S revision)** | (a) Every build-log citation in the rev 9 files is by timestamp and stage. Each one was checked against the log: 2026-11-17T23:26:20 RWB-E1-042 Gate triage; 2026-11-17T23:53:05 RWB-TE-003 Gate triage (D-RCV-40 "verification stays outside check"); 2026-11-18T00:09:40 "Gate triage (late record)" and the Gate triage of 119; 2026-11-18T04:55:55 RWB-E1-043 Gate triage (run 4) and Decision D-RUN-18; 2026-11-18T05:10:44 RWB-E1-042 Gate triage and Decision D-RUN-19. A search finds no remaining "timeline line" citation, except the historical run-2 entry in `agent-run-log.md`. (b) A-28 and §4.3 now cite E43S revision 4 and its 04:55:55 triage. However, E43S revision 5 was on disk at 05:09, before this revision was written (see 155). (c) §20: the duplicated "Housekeeping (148)." is removed. A-53 records the citation rule. |
| Gap candidate E1042-RV7-DG-01 | Kept with the review citations, Blocker = No | **Recorded** | As E1042-SP-DG-18, with the same sources (story v7 RWB-E1-042 lines 237 and 318; RWB-E1-011 lines 18 and 303; RWB-E1-037 lines 18 and 46). The row also says "Settled by D-RUN-19 (orchestrator, Claude Code; tech-lead ratification open, CLAR-027)". |
| Review-7 plan inputs 1-4 | Carry | **Carried** | §12.14 R7-1 to R7-4 (lines 972-975). |

## 2. D-RUN-19: how it is applied

| Check | Result | Evidence |
|---|---|---|
| Interface home and implementation | Consistent | `access.api.CatalogParameterReader` with nested `Value` (§12.2 line 603). `CatalogParameterReaderImpl` is package-private in `casewf.config` and always registered. It delegates to `ParameterService`, logs nothing and caches nothing of its own (line 624 onward). |
| Module edges | No cycle from this story | The implementation adds `casewf.config` → `access.api` (P3 → P4). That edge already exists (TE1S SPEC-022 (d), `casewf.admin` → `access.api`). The interface takes and returns JDK types only, so no P4 type names a P3 type. P1/P2/P4 readers depend only on `access.api`. TE1S SPEC-022 (d) says "access must not depend on any such module", so the rule holds as long as P4 depends on nothing that reads through it. That constraint is RWB-TE-001's and is already sent to the owners (TE1S SU-02, SU-14). |
| Ratification | Not claimed | CLAR-027 (line 1136): "no ratification is recorded". `shared-updates.md` line 39 says "No ratification is recorded". `gate-response.md` Round 7 says "no human acceptance or ratification is recorded". A search of all seven files finds no human approval, acceptance or ratification. |
| Scope (AGENTS §7, CLAR-025) | Recorded | The P4 change grows to three new types. CLAR-025, A-33, E1042-SP-DG-16 and `shared-updates.md` line 34 are updated, and each still says no analyst approval is claimed. A-52 explains why this story delivers the interface: "its implementation is this story's module". That is consistent with D-RUN-08, because nothing depends on a later story. |
| Interface usability for its named callers | Gap | See 156 (business date for P4 callers) and 157 (key-read check for string keys). |

## 3. New findings

| ID | Severity | Finding |
|---|---|---|
| `REVIEW-RWB-E1-042-155` | Low | The spec calls `ParameterLoadBranch` the `PARAMETER` implementation of the P4 SPI. E43S revisions 4 and 5 forbid a `PARAMETER` SPI bean and route `PARAMETER` through a dispatcher branch. The spec also cites E43S revision 4 although revision 5 is on disk |
| `REVIEW-RWB-E1-042-156` | Low | `CatalogParameterReader.get` requires a `businessDate`, and a P4 caller (RWB-E1-037) has no legal source for one |
| `REVIEW-RWB-E1-042-157` | Low | The new key-read rule for `CatalogParameterReader.get` string keys is not in SPEC-003 and has no test, so AC3 is unproven for every reader outside P3 |
| `REVIEW-RWB-E1-042-158` | Low | Housekeeping: stale "two types" wording, `CatalogParameterReaderImpl` missing from §12.1 types and the §12.12 bean table, an annotation inside the §12.4 exact-value column, and a forward reference in the run log |

### REVIEW-RWB-E1-042-155 (Low): the `PARAMETER` route is described as an SPI implementation that RWB-E1-043 forbids

**Maps to:** §4.3 first seam row (line 144: "the `PARAMETER` implementation of the SPI is a P3 adapter in RWB-E1-043's
own package (E43S revision 4 `ParameterLoadBranch` ...)", and "P1 and P3 handlers, the `PARAMETER` handler included,
implement that P4 type"); A-51; A-28; S-22; `shared-updates.md` line 32 (rev 9: "the SPI implementation is RWB-E1-043's
P3 adapter (`ParameterLoadBranch`)"); §12.14 R7-1 ("its `PARAMETER` SPI route"); TC-22 (b) ("standing for the SPI
route"); SPEC-021.

**Evidence:**

- E43S revision 4 (`spec.run4.md` line 536) and revision 5 (`spec.md` line 594) both say that a second bean for the
  same code, "or a bean for `PARAMETER`, fails start-up naming both classes". Both also say "the dispatcher only
  separates `PARAMETER` (SPEC-030)" (rev 4 line 538, rev 5 line 596).
- In E43S rev 5, `ParameterLoadBranch` is a dispatcher branch, not a handler. SPEC-026 (line 712) says it "calls only
  RWB-E1-042's published `casewf.config.api.ParameterLoadHandler`" and gets the bean through an `ObjectProvider`. When
  the bean is absent, it answers "404 per SPEC-018". SPI registration (line 591) is "a Spring bean of the P4 type
  `access.api.ReferenceTableHandler`", and the handler "depends on P4 only, never on P3". `ParameterLoadBranch`
  calls `casewf.config.api`, so it cannot be such a handler.
- E43S revision 5 was written at 05:09, before this revision (05:16) and before its triage (05:10:44). This spec
  still calls RWB-E1-043 "revision 4, in remediation" (S-22, A-28 "in remediation at revision 4", §4.3).
- D-RUN-18 says "P1 (RWB-E1-001) and P3 (RWB-E1-042) handlers implement it". E43S keeps `PARAMETER` off the SPI on
  purpose. The spec repeats the D-RUN-18 wording and pins it to a class that, in E43S, is not an SPI implementation.
- Review 7's fix text for 152 used the same "SPI implementation ... P3 adapter" wording. The residual is partly
  inherited from that review.

**Failure scenario:** The RWB-E1-043 specifier follows `shared-updates.md` row 32 (rev 9) and makes
`ParameterLoadBranch` implement `access.api.ReferenceTableHandler` for `PARAMETER`. `ReferenceTableHandlers` then
fails start-up, because E43S forbids a `PARAMETER` handler bean. A second outcome is also possible: a later reviewer
running R7-1 ("its `PARAMETER` SPI route keeps the SPEC-021 flag-off result") finds no SPI route and cannot close
the check. The runtime contract that matters to this story is the same in both specs: `ObjectProvider`, then 404
MSG-P4-003, and `ParameterLoadHandlerImpl` untouched. That is why this is Low.

**Why Low:** This story's code and tests are unaffected. TC-22 (b) asserts the same behaviour either way. The defect
is a wrong cross-story statement in a shared-updates row that tells another story what to build.

**Fix required:**

1. In §4.3, A-51, `shared-updates.md` row 32 (rev 9 sentence) and R7-1, describe the `PARAMETER` route as E43S
   specifies it. `PARAMETER` is separated by RWB-E1-043's dispatcher (E43S SPEC-030) and served by its P3
   `ParameterLoadBranch` (E43S SPEC-026). That branch obtains `ParameterLoadHandler` only through `ObjectProvider` and
   refuses with 404 MSG-P4-003 when the handler is absent. It is not an implementation of the P4 SPI, and no
   `PARAMETER` SPI bean exists. Keep "`ParameterLoadHandlerImpl` implements no `access.api` type".
2. Record in CLAR-027 that E43S departs from the D-RUN-18 phrase "P3 (RWB-E1-042) handlers implement it" for
   `PARAMETER`, for the tech lead's ratification. The spec should not decide which of the two governs. It should
   state that the flag-off contract is the same either way.
3. Cite E43S revision 5 (on disk, not yet gated) in S-22, A-28 and §4.3, or say that the plan re-checks the revision
   in force. Relabel TC-22 (b) as a stand-in for "RWB-E1-043's `PARAMETER` branch".

### REVIEW-RWB-E1-042-156 (Low): `CatalogParameterReader` needs a business date that a P4 caller cannot obtain

**Maps to:** §12.2 `CatalogParameterReader.get(String key, Class<T> type, LocalDate businessDate)` (line 603 onward);
SPEC-023 (line 183: "The business date ... comes from `BusinessDateProvider`"; "`ParameterService` callers pass their
own business date"); SPEC-026 caller rule; A-52; `shared-updates.md` line 38 (rev 9 R row to RWB-E1-037); TC-46.

**Evidence:**

- The interface has one method, and it requires `businessDate`. No overload reads the date for the caller.
- The business date has two sources. `BusinessDateProvider` is in `casewf.config.api` (P3, §12.1 line 544). After the
  §4.3 seam, it is filled from the view owner's published reader in P1 (line 150).
- A P4 caller cannot reach either source. P4 → P3 is excluded by TE1S SPEC-022 (d) ("neither `integration` nor
  `access` may depend on `casewf`"). P4 → P1 would close a cycle, because under D-RUN-19 P1 depends on P4
  (`CatalogParameterReader`), and TE1S SPEC-022 (d) adds "access must not depend on any such module".
- RWB-E1-037 is P4 (story v7 line 18). Its parameters `rwb.refload.approver.*` are in the catalog (line 46). The rev 9
  R row names it as a reader of this interface.
- A P1 caller is not affected. RWB-E1-011 reads the batch-status business date itself (story v7 lines 47-48).

**Failure scenario:** RWB-E1-037 needs `rwb.refload.approver.permission`. It cannot inject `BusinessDateProvider` or
the P1 reader, so it passes `LocalDate.now(...)`. Once the §4.3 seam reads the ACE batch date, that system date can
differ from the business date that P3 uses for the same key around a date change or a late batch. A future-dated
approver list then takes effect in P4 on a different day than everywhere else. SPEC-023 says the business date
comes from one provider, and nothing in the spec or the R row tells RWB-E1-037 what to pass.

**Why Low:** The affected reader is a later story (Build Sequence v6 order 27). This story's code is not affected.
The fix is small and stays inside this story's own module.

**Fix required:** Add `<T> Value<T> get(String key, Class<T> type)` to `CatalogParameterReader`. The P3
implementation reads the date from `BusinessDateProvider`. Keep the three-argument form for callers that hold their
own business date, such as P1 batch steps. Alternatively, state in §12.2 and the rev 9 R row which date a P4 caller
passes, and why that keeps SPEC-023. Either way, extend TC-46 with an assertion that the one-argument form uses the
provider's date.

### REVIEW-RWB-E1-042-157 (Low): the string-key read rule for `CatalogParameterReader` is not specified in SPEC-003 or tested

**Maps to:** SPEC-003 (line 163: "fails the build naming every key read in recovery main code that the catalog lacks");
§12.2 (lines 631-632: "`CatalogCompletenessCheck` (SPEC-003) treats a string-literal key passed to
`CatalogParameterReader.get` in recovery main code as a key read"); §12.11 fixtures (a reader of
`ParameterKey.of("allocation.retry.limit", Integer.class)`); TC-03 (line 1010); AC3, BR2; GR1.

**Evidence:**

- Inside P3, keys are typed constants generated from the catalog (`ParameterKeys`, SPEC-005), so a missing key fails
  at compile time or through the `ParameterKey.of` fixture of TC-03.
- Under D-RUN-19, readers outside P3 pass a plain `String` key. The only build-time protection for them is the new
  rule in §12.2 prose. SPEC-003 itself was not changed in revision 9. Its tests (TC-03, TC-21, TC-41, TC-44) have no
  fixture that calls `CatalogParameterReader.get`. TC-46 is a runtime Mockito test of the implementation, not of the
  build check.
- The spec does not say what the check does with a key that is not a literal, such as a constant or a computed
  string. Line 632 covers literals only.

**Failure scenario:** RWB-E1-011 writes `reader.get("recon.tolerence.pct", BigDecimal.class, d)` with a typo. The
builder implements the TC-03 path (`ParameterKey.of`) and does not implement the new path, because SPEC-003 does not
list it and no test fails. The build passes, which breaks story AC3 ("build fails naming an uncatalogued key"). The
first failure is an `IllegalArgumentException` in the daily reconciliation job.

**Why Low:** No reader outside P3 exists in this story. The rule is stated, but it is not in the requirement item and
not tested.

**Fix required:**

1. Add the rule to SPEC-003: a string literal passed as the first argument of `CatalogParameterReader.get` in recovery
   main code is a key read.
2. Add a TC-03 fixture, a reader of `CatalogParameterReader.get("allocation.retry.limit", Integer.class, d)`, which
   fails naming the key.
3. State how a key that is not a literal is treated: either refuse it in recovery main code, or accept it as a known
   limit with a test of the stated behaviour.

### REVIEW-RWB-E1-042-158 (Low): housekeeping

**Maps to:** §2 Impacted Existing Nodes (line 82), New Nodes Required (line 83); §12.1 `casewf.config` row (line 545);
§12.12 bean table (line 913); §12.4 `used_by` table (`recon.caselist.tolerance.pct` row); A-40; §12.14 T-1 (line 947);
`agent-run-log.md` run 7 step 4.

**Evidence:**

- (a) Line 82 now says "three new published types" and then, later in the same cell, "so the two `access.api` types
  are recorded in T-TE001-14's expected set". A-40 still says "the two `access.api` types". T-1 is historical, but the
  plan reads it next to T-2, which says three.
- (b) Line 83 (New Nodes Required) lists `MessageResolver` and `CapabilityCheck` only. It omits
  `CatalogParameterReader` and `CatalogParameterReaderImpl`.
- (c) §12.1 line 545 names `CatalogParameterReaderImpl` in the Visibility column ("adds ...") but not in the Types
  column.
- (d) §12.12 bean table (line 913) lists the always-registered beans without `CatalogParameterReaderImpl`, although
  §12.2 says it is "always registered whatever the flag". TC-22 does not assert it with the flag off.
- (e) §12.4 introduces its table as "the exact catalog-file values". The `recon.caselist.tolerance.pct` cell now
  carries a prose annotation after the code span. The temporal rows show that parentheses can be part of a value, so
  the cell is ambiguous to a builder copying values.
- (f) `agent-run-log.md` run 7 step 4 says "See 'Gate (run 7)'", but there is no such section yet.

**Fix required:** Say "three" (or list the types) in line 82 and A-40. Add the new type and its implementation to
line 83 and to the §12.1 Types column. Add `CatalogParameterReaderImpl` to the §12.12 "registered / registered" row,
and add a flag-off assertion to TC-22 that it is present and serves defaults. Move the §12.4 annotation to a note
under the table. Add the gate section to the run log when the gate result is known.

## 4. Plan inputs (not findings)

1. **E43S revision 5 at its gate.** When it passes, re-check that the `PARAMETER` route (155) still uses
   `ObjectProvider` with a 404 MSG-P4-003 refusal. Re-check that it adds no P4 type beyond the SPI types and
   `ListOfValuesReader`, and that T-TE001-14 is extended for them. This supersedes R7-1's "SPI route" wording.
2. **Ratification of D-RUN-18 and D-RUN-19 (CLAR-027).** If either decision changes, §4.3, §12.2 and
   `CatalogParameterReader` are revised. While ratification is open, the plan must not treat either decision as
   ratified.
3. **CLAR-025.** It is still OPEN to the analyst, now with three P4 types. No code may start before the analyst
   decides (AGENTS §7).
4. **Coverage.** `CatalogParameterReaderImpl` is main code in the combined bundle. TC-46 is its unit test, and the
   §14 list of unit-tested classes should include it when the plan is written.

## 5. CLAR-025 (two-module plan, AGENTS §7)

| Check | Result | Evidence |
|---|---|---|
| Recorded as open | Yes | CLAR-025 reads "OPEN (analyst; before the build)", with three types. `shared-updates.md` line 34, A-33 and E1042-SP-DG-16 are updated to match. |
| No approval claimed | Yes | "no analyst approval is claimed" in CLAR-025 and in `shared-updates.md` line 34. §12.1 says "not presumed approved". |
| D-RUN-19 changes the module count | No | Still P3 and P4. The new type is P4, and its implementation is P3. |

## 6. Checks performed

| Check (compliance-reviewer.md) | Result |
|---|---|
| Authentication and authorisation | Unchanged. `GET /admin/parameters` is checked through `CapabilityCheck` (R). The C, A and U rights belong to RWB-E1-043 (D-RUN-10). The new reader is an in-process call with no endpoint. No defect. |
| Customer and account data protection | No customer data. Exceptions from `CatalogParameterReader` carry the key only, "never a value, a user ID or a cause message" (§12.2). TC-10 keeps UUIDs out of log assertions. No defect. |
| Audit logging | Unchanged (AC-VERS in the approval transaction; the rollback write is now tested, TC-10). No defect. |
| KYC, AML, suitability, consent, approval | Out of scope beyond maker-checker. |
| Frontend integration and error contract | No frontend (§13). The reader uses no message ID because no API answer is involved, and that is stated. No defect. |
| Message IDs | Revision 9 adds none. MSG-P4-003 is used as before. No invented ID. |
| No literal business values | Unchanged. String keys outside P3 depend on 157. |
| Secrets and environment configuration | The reader refuses `secret=true` keys with `IllegalStateException` (SPEC-010). TC-46 covers it. No defect. |
| AC → requirement → test coverage | 57 of 57 rules mapped. TC-46 is added and TC-10 and TC-22 are extended. Gap: the build-time key check for string keys (157). |
| 80% gate per changed surface | Backend REQUIRED, with four counters at 0.80 in one bundle, outside `check`. Frontend `NOT_APPLICABLE`, with evidence. Planned, not measured, which is correct at this stage. |
| Migration rules | No change in revision 9. |
| Module boundaries (D-RUN-08, -10, -11, -18, -19; TE1S) | No cycle from this story's placement (§2). Residuals 155 and 156. |
| Consistency with E43S | The flag-off contract matches: `ObjectProvider` and 404 MSG-P4-003. Described route and revision citation do not (155). |
| Run-decision attribution | D-RUN-18 and D-RUN-19 are credited to the orchestrator (Claude Code) and marked unratified in every file. |
| Personal data in this run's files | None found in the revision 9 changes. Test identities are synthetic. |
| MCP | None connected; N/A. |

**Observation for the orchestrator (not a finding against this spec):** D-RUN-18's text says P3 (RWB-E1-042) handlers
implement the P4 SPI. E43S revisions 4 and 5 instead forbid a `PARAMETER` SPI bean and use a separate dispatcher
branch. The orchestrator may want to reconcile the decision text, or E43S, when it triages RWB-E1-043's round-5
gate.

## 7. Document-gap candidates

None new. The review-7 candidate E1042-RV7-DG-01 is recorded as E1042-SP-DG-18 (Blocker = No), and its citations
were checked against story files v7. Findings 155 to 158 concern run decisions and other specs, not the document set.

## Gate decision

```text
REVIEW_STATUS: FAIL
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 4] (155, 156, 157, 158)
BLOCKING: NO by severity; not accepted under D-RUN-09 (fix and re-gate, or route to the engagement lead for a human disposition)
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
EARLIER_FINDINGS: 151, 153, 154 resolved; 152 resolved in substance (wording residual in 155)
D_RUN_19: applied as stated (P4 access.api CatalogParameterReader, implemented in P3 casewf.config; no P1/P2/P4 -> P3 edge); not ratified (CLAR-027 OPEN); residuals 156, 157
CLAR_025: OPEN to the analyst; three P4 types; no approval claimed
PLAN_INPUTS: 4
DOCUMENT_GAP_CANDIDATES: 0 new (E1042-RV7-DG-01 recorded as E1042-SP-DG-18, Blocker = No)
NEXT_STEP: Orchestrator triage of 155-158 (Technical Specifier revision 10, then spec-gate-review-9.md; or route to the engagement lead for a human disposition under D-RUN-09)
```

SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 4]

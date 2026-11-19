# Spec gate review 4: RWB-E1-042 (RUN_ID `INC-003-epic-1-RWB-E1-042`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-042-SPEC-006` |
| Gate | Specification gate, re-review of revision 5 (round 4) |
| Artifacts under review | `specify/spec.md` revision 5 (1056 lines), `assumptions.md` (A-01 to A-39), `document-gaps.md` (E1042-SP-DG-01 to -16), `shared-updates.md`, `compliance-validation.md`, `gate-response.md` (Rounds 1-3), `agent-run-log.md` |
| Compared with | `review/spec-gate-review-3.md` (`REVIEW-RWB-E1-042-SPEC-005`: High 129, Lows 130-134, plan inputs 1-4, candidates E1042-RV3-DG-01 to -03); revision 4 snapshots `specify/*.run3.md` |
| Baseline | Document set v14: User Stories Epic 1 Story Files v7 (RWB-E1-042 v1 §12-§14), API Specification v4 (approve operation, `E503`, `ReferenceLoad`), Error and Message Standard v4, Physical Schema v6 (parameter tables, `sys_fields`), Data Classification and Personal Data Inventory v4 (Fields sheet), Build Sequence v6; run decisions D-RUN-07 to D-RUN-17 (`AI-SDLC-BUILD-LOG.md` lines 30-40); D-RCV-40, D-RCV-43 |
| Cross-story specs read | RWB-TE-001 spec v4 ("TE1S": SPEC-004, SPEC-020, SPEC-022 relocation table, SPEC-023, SPEC-025, field-level matrix line 114, T-TE001-14) and its `shared-updates.md` SU-08, SU-14; RWB-E1-043 spec revision 3 ("E43S", as on disk 00:45); RWB-E1-044 spec v14-4 ("E44S": SPEC-014 class sets, SPEC-016) |
| Repository | `<repo>` working tree as read 2026-11-18: `platform/internal/ApiExceptionHandler.java`, `ProblemFactory.java`, `platform/api/ApiProblemException.java` |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18 |
| Supersedes | `REVIEW-RWB-E1-042-SPEC-005` for revision 5. That review stays as history. |

## Status

**`SPEC_GATE: FAIL`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 1 | Blocks the handoff to the Implementation Planner |
| Low | 7 | Visible; fixed in the next run (D-RUN-09) |

Revision 5 resolves High 129 in substance: every class is named at its TE1S home, the published package
`casewf.config.api` matches the slot TE1S reserves for this story, `MessageResolver` and `CapabilityCheck`
sit in `access.api`, the flag binds by `@ConditionalOnProperty`, and no `platform` reference is left. Lows
130-133 are fixed and verified. 134 is fixed for what it named, but the same dangling-reference defect
recurs (finding 142).

One Medium remains from the relocation: the E7 503 on `GET /admin/parameters` is still built by calling
`ProblemFactory` from the P3 controller. After RWB-TE-001 that class is package-private in `access.internal`,
so the path can't be compiled as written. Fixing it needs a change to P4's published surface that the spec
doesn't decide. The seven Lows are: a TE-001 test that pins the published surface this story changes;
exception-cause logging against the personal-data rule; an inconsistent credential-property rule; a test
that can't run under the spec's own transaction rule; a misread of the AGENTS one-module rule; consumer
guidance that leaves out the dependency direction; and housekeeping.

## 1. Earlier findings (129-134): verification

Each row was checked in the revised text and against the source, not taken from `gate-response.md`.

| Finding | Severity | Verdict | Evidence checked |
|---|---|---|---|
| 129 Module placement vs RWB-TE-001 | High | **Resolved, with residual (135, 136)** | SPEC-026 and §12.1: implementation in `casewf.config`, published types in `casewf.config.api` with `@NamedInterface(name = "config.api", propagate = false)` and the map entry in the same merge request. This matches TE1S field-level matrix line 114, which reserves `casewf` `config.api` for RWB-E1-042, and TE1S SPEC-004 (d). `ApiError` and `ApiProblemException` are in `access.api`; `ProblemFactory`, `ApiExceptionHandler` and `SecurityConfig` in `access.internal`; `RecoveryFlags` in `integration.flags.api`; `RecoveryFlywayConfig` in `casewf.migration`; no `RecoveryProperties`. All of these match the TE1S relocation table and SPEC-023. `MessageResolver` and `CapabilityCheck` are in `access.api` (SU-08 (d)). The flag binds by `@ConditionalOnProperty` (SU-08 (b)). PRE-7 was added and A-01 replaced. CLAR-020 is resolved with citations. `shared-updates.md` row 32 gives RWB-E1-043 the new packages. A grep finds no `platform.` package reference. The replaceable-seam direction is stated (A-34; §4.3 recorder and business-date rows). Two residuals: §10.2 still calls the now package-private `ProblemFactory` from P3 (finding 135), and TE1S T-TE001-14 pins the published surface this story extends (finding 136). |
| 130 `usedBy` split on comma | Low | **Resolved** | §7.1: `;` grammar (trimmed, non-empty, at most 100 characters per entry, at most 400 in total). The 400-character total matches Physical Schema v6 `used_by varchar(400)` (line 1399). §12.4 lists every catalog value and its expected array; no seeded value contains `;`. §7.5 splits on `;`. SPEC-003 rejects a value that does not parse. TC-41 runs on the real catalog plus six negative fixtures. |
| 131 Coverage of build checks and generator | Low | **Resolved** | §12.11 and §14: the check logic is in test-scope `architecture.parameters` classes, measured by `recoveryToolingCoverageVerification` at 0.80 on LINE, INSTRUCTION, BRANCH and METHOD. E44S SPEC-014 defines TOOLING as the test-scope tooling package with JUnit classes excluded and accepts more than one directory; the plan adds the package to the include pattern if needed. Generator: the exception and its reason are recorded (A-38), and the output is checked by TC-42 against the parsed file on every column, plus TC-26 and TC-27. |
| 132 Recorder failure 503 MSG-P7-003 | Low | **Resolved** | SPEC-014, SPEC-019, E11, §8, §10.2, §10.3 and §12.7 step 5 all say 503 MSG-P7-003, with the cause kept. Checked against API v4: the approve operation lists 503 `E503`, `E503` (line 6029) names MSG-P7-003 for "The decision could not be recorded", and Standard v4 line 208 defines MSG-P7-003. TC-29 (b) asserts status, message ID, TH text and rollback. The MSG-GEN-006 conflict is in SP-DG-11 with both citations. The logging side of the kept cause is raised as finding 137. |
| 133 Refusal paths without tests | Low | **Resolved** | TC-35 (unknown `loadId`, including a seeded row id), TC-36 (approve after `validFrom` has passed), TC-37 (rollback of `VALIDATED` and `ROLLED_BACK`), TC-38 (approve of `APPROVED` and `ROLLED_BACK`), TC-39 (reason of 400 and 401 characters), TC-40 (`find` hit and miss). Each test gives its input, status and message ID. |
| 134 Housekeeping | Low | **Resolved for its items; recurs (142)** | The title covers revisions 3-5 and "Gate (run 2)" is present. However, run 3 step 5 points to a "Gate (run 3)" section that does not exist, while `gate-response.md` R3.1 row 134 and R3.4 say it was appended. |

## 2. Review-3 plan inputs 1-4 and gap candidates RV3-DG-01..03

| Item | Status |
|---|---|
| Plan input 1 (transaction boundary of `load`) | Applied: `REQUIRES_NEW` for `load`, `approve` and `rollback`; catch outside, then re-read in a new read-only transaction (SPEC-013, §12.7, A-39). RWB-E1-043 is told (shared-updates row 32). |
| Plan input 2 (no credential-bearing ENV row) | Applied, but the rule is stated two ways (finding 138). |
| Plan input 3 (rollback cache rebuild after commit) | Applied (§12.8 `ParameterRollbackCommitted`, `AFTER_COMMIT`), but its test TC-10 (b) can't run as described (finding 139). |
| Plan input 4 (handler message-ID branch) | Applied (§10.2 handler path, TC-30); its logging is not specified (finding 137). |
| RV3-DG-01 | Merged into E1042-SP-DG-11 with Standard v4 lines 73, 208 and API v4 lines 6028-6029. Verified. |
| RV3-DG-02 | Recorded as E1042-SP-DG-14 (story v7 line 237; TE1S SU-08). Verified. |
| RV3-DG-03 | Recorded as E1042-SP-DG-15. Verified: Inventory v4 lines 676-677 say personal "Yes"; Physical Schema v6 `sys_fields` lines 4345-4346 say `is_personal` false. The protective reading is applied in SPEC-027. |

## 3. New findings

| ID | Severity | Finding |
|---|---|---|
| `REVIEW-RWB-E1-042-135` | Medium | The E7 503 is built by calling P4's package-private `ProblemFactory` from P3 |
| `REVIEW-RWB-E1-042-136` | Low | TE1S T-TE001-14 pins the published surface this story extends; spec says no other test changes |
| `REVIEW-RWB-E1-042-137` | Low | Exception causes reach the log through the handler; the personal-data rule is not specified there |
| `REVIEW-RWB-E1-042-138` | Low | Credential-property rule stated two ways; under §7.1 the `api-key` fixture of TC-44 passes |
| `REVIEW-RWB-E1-042-139` | Low | TC-10 (b) can't run under the spec's own `REQUIRES_NEW` rule |
| `REVIEW-RWB-E1-042-140` | Low | Two-module plan default contradicts AGENTS §7 ("before any code is written") |
| `REVIEW-RWB-E1-042-141` | Low | Import guidance to RWB-E1-043 leaves out the dependency direction its own placement creates |
| `REVIEW-RWB-E1-042-142` | Low | Housekeeping: dangling "Gate (run 3)" reference claimed as done |

### REVIEW-RWB-E1-042-135 (Medium): the E7 503 is built by calling P4's package-private `ProblemFactory` from P3

**Maps to:** SPEC-025, SPEC-026; E7; §10.2 (lines 389-391); §12.1 (lines 508-509); TC-34; AGENTS §3.11, §4.2.

**Evidence:**

- Spec §10.2: "The 503 of E7 is built by `ProblemFactory` as a status-only Problem ... from a handler
  local to the parameter catalog controller." The controller is in P3 `casewf.config` (§12.1 line 507).
- TE1S SPEC-022 relocation table: `ApiExceptionHandler`, `ProblemFactory` and `SecurityConfig` go to
  `access.internal` with visibility "pp" (package-private). In the code today `ProblemFactory` is a
  package-private class with package-private methods (`platform/internal/ProblemFactory.java`).
- §12.1 lists the P4 additions as `MessageResolver`, `CapabilityCheck` and the message-ID constructor of
  `ApiProblemException`. None of them yields a status-only Problem. The message-ID constructor carries a
  message ID, and E7 deliberately has none (SPEC-025).
- AGENTS §4.2 says never "call or read the inside of another module". TE1S SU-08 (c) says extending the
  problem types is a change that this story plans through `access.api`.

**Failure scenario:** The builder writes the `@ExceptionHandler` in the parameter catalog controller as
specified. It doesn't compile, because `ProblemFactory` is not visible from `casewf.config`. Making
`ProblemFactory` public, or moving it, breaks TE1S SPEC-022 and the module-map rule. Building the Problem by
hand in P3 duplicates P4 and loses the shared `traceId` handling. Any working option changes P4's published
surface, which the spec leaves undecided. AGENTS §7 sends a decision the agent "cannot default" back to the
analyst before code is written.

**Fix required:** Decide the P4 mechanism and add it to the §12.1 `access.api` row and §2. One option: an
`ApiProblemException` form that carries only a status (for example a factory method for 503 with no message
ID), which the message-ID branch of `ApiExceptionHandler.problem` renders as type
`urn:rwb:problem:unavailable` with title, status and `traceId`. The P3 controller then catches the two
data-access exceptions of E7 and throws it. Change §10.2 accordingly, and have TC-30 cover the status-only
branch alongside TC-34.

### REVIEW-RWB-E1-042-136 (Low): TE1S T-TE001-14 pins the published surface this story extends

**Maps to:** §2 Impacted Existing Nodes (line 77); §12.12 (line 836, "no other module's test changes");
TC-45; `compliance-validation.md` "No test weakened" row ("existing tests unchanged").

**Evidence:** TE1S T-TE001-14 checks the real main classes. It expects the public types in each published
package to equal the SPEC-025 list, where `access.api` has `ApiError` and `ApiProblemException` only, and it
expects Modulith to report the `casewf` named interfaces `api`, `rules`, `timers` and `workflow`. This story
adds `MessageResolver` and `CapabilityCheck` to `access.api` and the `config.api` named interface to
`casewf`. TC-45 says the existing boundary tests "pass" with the new map entry, and §2 does not list
T-TE001-14 as impacted.

**Failure scenario:** After this story's change, T-TE001-14 fails in `test`. The builder must then edit
another story's test without a spec basis. That edit is either undeclared or looks like weakening a test
(AGENTS §4.5).

**Fix required:** List T-TE001-14 (and any other TE1S test that pins published types or named interfaces)
under Impacted Existing Nodes. State the new expected lists: `access.api` plus `MessageResolver` and
`CapabilityCheck`; `casewf` named interfaces plus `config.api`, holding exactly the §12.1 published types.
Change TC-45 to assert the updated lists. Correct §12.12 and the self-check row.

### REVIEW-RWB-E1-042-137 (Low): exception causes reach the log through the handler

**Maps to:** SPEC-014, SPEC-027; §10.2 handler path (lines 393-397); §12.13 (lines 849-850); TC-29 (b), TC-30;
D-RUN-15.

**Evidence:**

- The existing handler, `ApiExceptionHandler.problem`, logs
  `log.warn("Recovery API problem {}", ex.error().messageCode(), ex.getCause())`. That writes the cause
  with its message and stack trace.
- D-RUN-15 (build log line 38) gives the removal of raw exception text from that handler to RWB-TE-003,
  which is Build Sequence order 5, after this story.
- SPEC-014 and §12.7 attach the recorder's exception as the cause of MSG-P7-003. §12.13 promises that a
  recorder failure logs "the cause's class, not the cause's message".
- §10.2 adds a message-ID branch to the same handler but says nothing about its log line.
- SPEC-027 says the approver ID appears in no log line. A database failure in the later decision-log
  writer can echo row values, such as a PostgreSQL constraint "Key (...)=(...)" detail.

**Failure scenario:** RWB-E1-027's writer fails on a constraint. The handler's new branch copies the
existing pattern and logs the cause's message, which carries the approver UUID. §12.13 and SPEC-027 are
broken, and no test notices.

**Fix required:** State that the message-ID branch logs the message ID, status and cause class only, never
the cause message or stack text, in line with D-RUN-15. Add a log assertion to TC-29 (b) or TC-30: the
cause's message is absent from the captured log.

### REVIEW-RWB-E1-042-138 (Low): credential-property rule stated two ways

**Maps to:** SPEC-003 (line 158); §7.1 `env_property` row (line 267); TC-44; review-3 plan input 2.

**Evidence:** SPEC-003 refuses an ENV row whose property has "a segment containing" one of the listed words.
§7.1 refuses one where "any dot- or dash-separated segment matches" the list. That list includes `api-key`
and `private-key`, which contain a dash, so with the split on dashes they can never equal a segment. TC-44
expects `rwb.api-key` to fail. Under "matches", a camel-case property such as `rwb.clientSecret` also passes.

**Failure scenario:** The builder follows §7.1 to the letter. `rwb.api-key` splits into `rwb`, `api` and
`key`, so nothing matches and TC-44 fails. Or the builder follows SPEC-003 instead, and the two statements
disagree on which properties are refused.

**Fix required:** Give one rule: split on `.` only, then test each segment case-insensitively for a listed
substring (or say "matches" and list `api`, `key` and the camel-case forms). Use the same wording in SPEC-003
and §7.1. Add a camel-case fixture to TC-44.

### REVIEW-RWB-E1-042-139 (Low): TC-10 (b) can't run under the spec's own `REQUIRES_NEW` rule

**Maps to:** TC-10 (b) (line 903); SPEC-015; §12.7 transaction boundaries (lines 718-723); §12.8.

**Evidence:** TC-10 (b) runs "a rollback inside a test transaction template whose commit is forced to fail" and
expects "rows unchanged and the cache still serves v2". But SPEC-015 and §12.7 say `rollback` always starts
its own `PROPAGATION_REQUIRES_NEW` transaction and never joins a caller's. When the outer test transaction
fails to commit, the inner rollback has already committed.

**Failure scenario:** The test is written as specified. The rows are `ROLLED_BACK` and the cache serves v1,
so the test fails even though the code is correct. Or the test is changed in an ad hoc way to pass, and the
after-commit rebuild is never actually tested.

**Fix required:** Force the failure inside the rollback's own transaction, for example with a test
`TransactionSynchronization` registered by a test hook that throws in `beforeCommit`, or with a deferred
constraint that fails at commit. Keep the expected result, and state the mechanism in TC-10 (b).

### REVIEW-RWB-E1-042-140 (Low): two-module plan default contradicts AGENTS §7

**Maps to:** CLAR-025 (line 1019); A-33; E1042-SP-DG-16; `shared-updates.md` row 34.

**Evidence:** AGENTS §7 says that a plan which touches more than one module "goes back to the analyst before
any code is written". §9 makes "touches one module" a condition of the Plan approved gate. CLAR-025 defaults
to "the tech lead approves the two-module plan on the merge request", which happens after the code exists.
E1042-SP-DG-16 explains Blocker = No with "AGENTS §7 routes a multi-module plan to review, not to a stop",
which is not what §7 says. E43S records the same situation as a decision "the plan gate must take" (E43S §2,
module scope row).

**Failure scenario:** The plan is approved and built with P4 changes, and the AGENTS §7 decision is first
taken at merge. If it is refused there, the P4 seams (and finding 135's change) are reworked after the build.

**Fix required:** Change CLAR-025, A-33, DG-16 and shared-updates row 34 so that the two-module decision is a
plan-gate precondition: the analyst or tech lead records it before the build starts, with SU-08 (c) and (d)
as the basis. Change the DG-16 "Why" text to quote §7 correctly. Blocker = No can stay, since a documented
route exists.

### REVIEW-RWB-E1-042-141 (Low): import guidance to RWB-E1-043 leaves out the dependency direction

**Maps to:** `shared-updates.md` row 32; §4.3 first and CapabilityCheck seam rows (lines 139, 143); §11.2;
SPEC-026.

**Evidence:** Row 32 tells RWB-E1-043 to import `ParameterLoadHandler`, `ParameterLoadResult`,
`ParameterKeys`, `ParameterService` and `BusinessDateProvider` from `casewf.config.api`. This spec makes
`casewf.config` depend on `access.api` (P3 → P4, §12.1) and states "P3 may depend on P2 and P4, never the
reverse" (§4.3). E43S revision 3 places `ReferenceLoadController` and `ParameterLoadBranch` in P4
`access.refload` (E43S §2, New Nodes), which is a P4 → P3 call. TE1S SU-08 (INC-008 part) already says this
makes a cycle that `ModulithTest` rejects, and E43S's own round-3 gate raised it (build log line 192,
finding 131 there). §4.3 even justifies `CapabilityCheck` in P4 "because RWB-E1-043 and later P4 code call
it", without saying that this P4 code may not call `casewf.config.api`.

**Failure scenario:** RWB-E1-043 follows row 32 and keeps its caller in P4. When it merges, `ModulithTest`
fails on a P3↔P4 cycle, and the published seam of D-RUN-10 can't be consumed as designed.

**Fix required:** In row 32, §4.3 and §11.2, state the consumer constraint: callers of `casewf.config.api`
must sit in P3 (for example `casewf.refdata`, as SU-08 proposes) or in a module that P3 does not depend on.
Code in P4 may call no type of this package. Cite TE1S SU-08 and SU-14.

### REVIEW-RWB-E1-042-142 (Low): housekeeping

**Maps to:** `agent-run-log.md` line 98; `gate-response.md` lines 137, 170; `compliance-validation.md` row
"Run log title and sections".

**Evidence:** Run 3 step 5 says 'See "Gate (run 3)"', but there is no such section. Three files say it was
appended: gate-response R3.1 row 134 ("run 3 and 'Gate (run 3)' sections appended"), R3.4 and the
self-check (PASS). This is the same dangling-reference pattern that finding 134 raised for run 2. In
addition, `gate-response.md` is still titled "Gate response: REVIEW-RWB-E1-042-SPEC-003" although it holds
three rounds.

**Failure scenario:** A reader tracing the evidence finds a claim that the evidence file contradicts.

**Fix required:** Add the "Gate (run 3)" section with this review's result, change the three claims so they
match the file, and retitle `gate-response.md` to cover all rounds.

## 4. Plan inputs (not findings)

1. **Flag state in always-registered beans.** `ParameterService` and `ParameterStartupCheck` are registered
   whether the flag is on or off but behave differently (§12.12), and the flag binds "only" by
   `@ConditionalOnProperty`. Name the mechanism: two conditional implementations (`havingValue = "true"`
   and `"false"` with `matchIfMissing`), or one bean that reads the property. Do not add a `RecoveryFlags`
   field (SU-08 (b)).
2. **MAIN coverage from `test` only.** §14 counts `test` execution data only, and almost every behaviour
   test in §15 is System (`recovery-it`). Plan unit tests in `test` (Mockito, MVC slice) for
   `ParameterServiceImpl`, the §12.5 checks, the validity recomputation, the content hash, the cache,
   `ParameterStartupCheck`, the controller and `ParameterLoadHandlerImpl`, so that the four counters reach
   0.80.
3. **SpEL bean name.** `@PreAuthorize("@capabilityCheck.require(...)")` resolves the bean named
   `capabilityCheck`. Register `InterimCapabilityCheck` under that name, and tell RWB-E1-037 to keep it.
4. **Load-file quoting.** CODE_LIST values contain commas (for example `servicelevel.required-statuses`).
   State that the PARAMETER load file is RFC 4180 (quoted fields), parsed by the same CSV reader as the
   catalog, and that the §12.6 hash uses the unquoted value.
5. **Recorder failure at commit.** A later JPA-based recorder must flush inside `recorded(...)`, so that its
   failure surfaces at step 5 as MSG-P7-003 and not at commit as an unmapped exception.
6. **RWB-E1-043 revision.** S-22 and A-28 cite E43S revision 2. E43S is now at revision 3 and is being
   remediated for its round-3 gate. Re-check the flag-off refusal (404 MSG-P4-003) and the import packages
   against the E43S revision in force when the plan is written.

## 5. Checks performed

| Check (compliance-reviewer.md) | Result |
|---|---|
| Authentication and authorisation | Method check on `GET /admin/parameters` through `CapabilityCheck` in `access.api` (SPEC-020, §12.10); 401 from `SecurityConfig`. Load, approve and rollback rights are on RWB-E1-043's endpoint (D-RUN-10). Bean name: plan input 3. |
| Customer and account data protection | No customer data. Author and approver are treated as personal (SPEC-027, Inventory v4). Audit columns `created_by`/`updated_by` are unclassified: gap candidate RV4-DG-01. Cause logging: finding 137. |
| Audit logging | AC-VERS through the recorder inside the approval transaction; 503 MSG-P7-003 on failure (API v4). Access log is a seam to RWB-E1-039. |
| KYC, AML, suitability, consent, approval | Not in scope beyond maker-checker (SPEC-014, DB check). |
| Frontend integration and error contract | No frontend (§13). Problem contract via `access` types; E7 path: finding 135. |
| Secrets and environment configuration | Secrets listed, never served; ENV credential rule: finding 138. |
| Test coverage per AC | AC1-AC11, X1-X10 mapped; TC-12 honestly `Blocked`; refusal paths now tested (133). TC-10 (b): finding 139. |
| 80% gate per changed surface | Backend MAIN and TOOLING sets at 0.80 on four counters, outside `check` (D-RCV-40, E44S SPEC-014); generator exception recorded. Unit coverage source: plan input 2. Frontend `NOT_APPLICABLE` with evidence. |
| Migration rules (D-RCV-28, D-RUN-07, D-RUN-12, D-RUN-13) | One file, `<seq>` at merge, `${recoverySchema}`, guarded DDL; PRE-6 for the lint. |
| Dependencies and module boundaries (D-RUN-08, D-RUN-10, D-RUN-11; TE1S) | Homes match TE1S (129 resolved). Residuals: 135, 136, 141. |
| D-RCV-35 / D-RCV-36 | No `public` read; no Temporal or Drools call; six keys catalogued. |
| Required headings and §14 columns | Present. |
| Personal data in this run's files | None found; synthetic UUIDs and the label "U-41" only. |
| MCP | None connected; N/A. |

## 6. Document-gap candidates

| ID | Source and conflict (two citations) | Blocker | Suggested handling |
|---|---|---|---|
| E1042-RV4-DG-01 | Data Classification and Personal Data Inventory v4, Fields sheet (`legacy/06-data/...personal-data-inventory-v4-xlsx.md` lines 652-678) has no row for `parameter_catalog.created_by`/`updated_by` or `parameter_value.created_by`/`updated_by`. Physical Schema v6 defines those columns (`legacy/06-data/recovery-workbench-physical-schema-v6.sql` lines 1406, 1408, 1429, 1431), and the same Inventory classifies the same audit columns on other tables as "Staff identifier", personal "Yes" (DF-EXT-010, DF-EXT-012, lines 1339, 1341). This spec writes the approver or rollback caller into `parameter_value.updated_by` (§7.3). | No | Apply the protective reading: SPEC-027 names `updated_by`/`created_by` and the rollback caller ID alongside author and approver (§12.13 already keeps them out of logs). The data protection owner adds the Inventory rows. |

## Gate decision

```text
SPEC_GATE: FAIL
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 1] [LOW: 7]
BLOCKING: YES (Medium 135)
EARLIER_FINDINGS: 129 resolved with residuals (135, 136); 130-133 resolved; 134 resolved for its items, pattern recurs as 142
NEXT_STEP: Technical Specifier revision 6 (decide the P4 status-only problem path for E7; fix 136-142), then spec-gate-review-5.md
```

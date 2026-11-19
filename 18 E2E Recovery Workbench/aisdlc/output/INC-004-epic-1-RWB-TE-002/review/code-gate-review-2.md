# Code gate review, round 2: RWB-TE-002 (RUN_ID `INC-004-epic-1-RWB-TE-002`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-002-CODE-002` |
| Gate | Code gate, pre-merge, round 2 (re-review after the round-1 fix) |
| Story | RWB-TE-002 Code owners for the recovery module (EPIC-001, P2 technical enabler) |
| Range | `git diff develop-recovery...feature/RWB-TE-002-code-owners` (merge base = `develop-recovery` tip `0b87102`) |
| Tip | `d018cf7` (`d018cf73c75d635fe2304fc5cd19e8c04e4d7576`). This is the branch ref and the worktree `HEAD`, and `git status --short` in `rwb-wt/RWB-TE-002` is empty. The fix commits are `f61f133` (red) and `d018cf7` (green). |
| Round 1 | `review/code-gate-review.md` (FAIL 0C/0H/0M/3L at `c740d25`: CODE1-001, CODE1-002, CODE1-003) |
| Inputs read independently | `git diff c740d25 d018cf7` (code: `.gitlab/host-settings.md`, `CodeOwnersValidator.java`, `CodeOwnersValidationTest.java`); `git show f61f133`; the full `CodeOwnersValidator.java` at `d018cf7`; `implement/backend/red-code1-001.txt`, `final-tip-{codeowners,test}.log`, `final-tip-counts.txt`, `final-tip-scope.txt`, `superseded-c740d25/`; native JUnit XML `backend/build/test-results/{codeOwnersTest,test}` and the native JaCoCo XML in the worktree and in `implement/backend/coverage-final/`; `implement/deviations.md` (DEV-08, DEV-10), `plan-addendum.md`, `document-gaps.md` (IM-DG-03, -04), `shared-updates.md` (IM-SU-04, -05), `implementation-report.md`, `handoff.md`; `docs/README.md`, `docs/COMPLIANCE.md`, `docs/document-gaps.md`; the session transcript that DEV-10 cites |
| Re-runs | No Gradle run. The tip XML is from 21:28-21:30 and is byte-identical to the saved copy (JaCoCo SHA-256 `f71b594d10c1…`). One read-only probe: a single-file Java program, run outside the repository, that copies `UNSUPPORTED`, `NON_NORMAL`, `supported()` and `matchesAFile()` as they are at `d018cf7`. |
| Repository | Read only apart from this file. |
| Human sign-off | **Not recorded.** OPEN-016. This review records no approval, acceptance or ratification (D-RUN-09). |

## Status

**PASS**: 0 Critical, 0 High, 0 Medium, 0 Low. All three round-1 findings are closed, and this round
raises no new finding.

## Round-1 findings: verification

| ID | Round-1 severity | Status | How it was verified (files, logs and code, not the summary) |
|---|---|---|---|
| CODE1-001 | Low | **Closed** | **Code** (`CodeOwnersValidator.java:31` and `:146-169` at `d018cf7`, read directly). `NON_NORMAL = (^|/)\.{1,2}(/|$)|//|:` is part of `supported()` (V4). `matchesAFile` now takes `base = root.toAbsolutePath().normalize()` and `target = base.resolve(pattern.substring(1)).normalize()`, and returns `false` unless `target.startsWith(base)`. The containment check runs before any `isRegularFile`, `isDirectory` or `Files.walk` call. `checkFile` still calls `matchesAFile` only for supported patterns, so the two checks act as two layers. **Probe** (same logic, against `rwb-wt/RWB-TE-002`):<br>• `//Windows/`: `supported=false`, `matchesAFile=false`<br>• `/C:/Windows/`: `false` / `false`<br>• `/backend//src/`: `supported=false` (V4 stops it)<br>• `..` escapes to the real sibling worktree, `/backend/../../RWB-E1-042/` and `/../RWB-E1-042/backend/build.gradle.kts` (that file exists): `false` / `false`<br>• in-root patterns `/backend/src/main/java/th/co/scb/ace/demo/recovery/` and `/AGENTS.md`: `true` / `true`<br>• `/../RWB-TE-002/AGENTS.md` normalises back inside the root: `matchesAFile=true`, which is correct because it never leaves the root, and V4 rejects it anyway.<br>`Path.startsWith` compares whole path segments, so a sibling such as `RWB-TE-002x` does not count as inside. **Red first.** `red-code1-001.txt`: base `c740d25` plus the uncommitted red tests, "no probe file". It shows "35 tests completed, 2 failed" (`patternResolvingOutsideTheRootMatchesNoFile` at `:444`, and `emptySegmentAndColonPatternsAreRejected` with an `AccessDeniedException` while walking `C:\Windows`, which shows the old code reading outside the root), then BUILD FAILED, EXITCODE=1. `f61f133` commits only the tests plus the visibility change of `matchesAFile` to package-private, and the commit message records that change. At the tip, both tests pass in the native XML. **Records.** `plan-addendum.md` C2, DEV-08 and IM-SU-04 all name the widened V4/V9. The comment at `:30` now matches what the code does. |
| CODE1-002 | Low | **Closed** | (a) DEV-08 (`deviations.md:12`) now names **C2** (V4/V9 widened beyond the spec text), **C4** (cache key `gradle-codeowners` instead of the `gradle` key in SPEC-013 and `data-model.md` §7) and **H1** (HC-09). `plan-addendum.md` has row H1. IM-SU-04 (`shared-updates.md:10`) now lists A1-A6, R1, C2, C4 and HC-09 for ratification. (b) `.gitlab/host-settings.md` adds **HC-09** "use separate caches for protected branches", On, Project. The row is labelled "not in the spec or story: ratification by the tech lead pending (IM-SU-04)", is verified by HV-07, and the owner line now reads HC-01..HC-09. Gap row **IM-DG-03** has Blocker No, with a reason. (c) **IM-DG-04**: the image is not pinned by digest. SPEC-013 fixes the tag, `backend-unit` uses the same tag, and no digest was invented (Blocker No, OPEN-038). `docs/COMPLIANCE.md:132-133` lists both gaps in §6, and `COMPLIANCE.md:104` shows C2, C4 and H1 under DEV-08. Nothing claims ratification. |
| CODE1-003 | Low | **Closed** | (a) **DEV-10** (`deviations.md:14`) says the precedence guard cannot be red against code. It records that a temporary root `CODEOWNERS` probe file was written, the red run made, and the file removed, and it cites the session transcript and the timestamps. I checked the cited transcript: it exists and holds the `Set-Content … "# temporary red-run probe"` and `Remove-Item "$wt\CODEOWNERS"` calls. `implementation-report.md` no longer lists the guard as an ordinary red test. The new round-1 red log states "no probe file". (b) The stale text is fixed. The `branch` and `sources` front matter in `docs/README.md:9-10` now say `d018cf7` (first written at `ae61b08`). The header of `implementation-report.md:3` says final code tip `d018cf7`, original base `7bee04d`. (c) `docs/document-gaps.md` DOC-DG-02 is marked "corrected after code gate round 1 … closed" and names both N/A reports. |

## Findings (this round)

| ID | Severity | Finding | Evidence | Remediation |
|---|---|---|---|---|
| — | — | None. | — | — |

## Figures against native reports (tip `d018cf7`)

| Figure | Claimed (report, counts, handoff, README, COMPLIANCE, IM-SU-05) | Native | Match |
|---|---|---|---|
| `codeOwnersTest` | 35, 0 F / 0 E / 0 S | `test-results/codeOwnersTest`: 35 / 0 / 0 / 0 (21:28); `final-tip-codeowners.log` TIP `d018cf7`, BUILD SUCCESSFUL, EXITCODE=0 | Yes |
| Backend `test` | 423, 0 failures | `test-results/test`: 423 / 0 / 0 / 0 (21:28-21:30); `final-tip-test.log` TIP `d018cf7`, EXITCODE=0 | Yes |
| LINE | 95.77 (204/213) | 204/213 | Yes |
| BRANCH | 95.90 (117/122) | 117/122 | Yes |
| INSTRUCTION | 96.85 (1262/1303) | 1262/1303 | Yes |
| METHOD | 100.00 (43/43) | 43/43; 11 classes, no `*Test` class | Yes |
| Saved XML | `coverage-final/codeOwnersCoverageReport.xml` | Byte-identical to the worktree report | Yes |

**No `c740d25` figure is cited as current.** Every mention of 33 / 421 / 95.71 / 95.83 / 96.83 is in the
sentence "Figures at `c740d25` … are superseded; their logs are in `implement/backend/superseded-c740d25/`"
(`implementation-report.md:7`, `handoff.md:16`, `docs/README.md:78`, `docs/COMPLIANCE.md:65`). The
`ae61b08` figures stay labelled superseded, as in round 1. IM-SU-05 (the traceability row) carries
`d018cf7`, 35 methods, and 95.77/95.90/96.85/100. `final-tip-counts.txt` lists both new methods.

## Diff `ae61b08..d018cf7` (security first)

Round 1 reviewed `ae61b08..c740d25`. The new part, `c740d25..d018cf7`, has 3 code files (+46/-6):

- **Validator.** V4 is stricter (it rejects `//` and `:`), and V9 is now contained in the root. The
  only other change in the commit is that `matchesAFile` became package-private. It is test scope, in a
  `final` class, and adds no exposure. Nothing in the code writes or runs anything, and it adds no new
  file-system access. A note on symlinks: normalisation is lexical, so a symlink that lies inside the root
  is still followed by `isRegularFile` and `isDirectory`. That is correct for V9, because GitLab matches
  the tracked symlink path itself, and `Files.walk` still does not follow links below the start folder.
  This is not a finding.
- **Over-restriction, recorded.** V4 now rejects any `:`, even though a file name may legally contain one
  on Linux. The live tree has no such path, `liveFileAndRegisterPass` passes, and this widening is part of
  C2, which IM-SU-04 covers.
- **`host-settings.md`.** One row (HC-09) is added, marked as an addendum and pending ratification. It
  holds no person and no value taken from outside the record.
- **Tests.** Two new methods, using `@TempDir` only (the `outside/` files sit beside the fixture repository inside the temporary folder).

Scope at `d018cf7` is unchanged. The three-dot diff has 16 files, and the diff over `frontend api backend/src/main` is empty (`final-tip-scope.txt`, rechecked). The API and functional `NOT_APPLICABLE` reports still hold, because the surfaces did not change. No dependency was added. The only e-mail-shaped text is the synthetic UT-08 value `someone@example.test`.

## Gate checklist (full code gate at `d018cf7`)

| # | Gate | Result | Evidence |
|---|---|---|---|
| 1 | SPEC-001..019, AC1..AC7, BR1..BR7 trace | **PASS** | Same as round 1, plus two V4/V9 tests. HV-01..HV-11 stay `OPEN — NOT_TESTED_HERE`. |
| 2 | Governance files | **PASS** | CODEOWNERS and the register are unchanged since round 1 (spec block plus the D-RUN-25 addendum). `host-settings.md` is HC-01..HC-08 as in the spec, plus HC-09, recorded as addendum H1. |
| 3 | Validator and UT-01..UT-26 | **PASS** | 35/35 pass. Every V-rule has a passing and a failing case. |
| 4 | `codeOwnersTest` and the 80% gate | **PASS** | Figures above. Defined here, run on the host (HV-07). |
| 5 | `codeowners-validation` CI job | **PASS** (definition) | Unchanged since round 1. The C4 deviation is recorded. DEV-07 / IM-SU-02 are carried. |
| 6 | AGENTS.md §5 fix | **PASS** | Unchanged. UT-22 passes. |
| 7 | No main-source, `frontend/` or `api/` change | **PASS** | Empty diff over those paths. |
| 8 | No dependency added | **PASS** | `build.gradle.kts` is unchanged since round 1. |
| 9 | No personal data, no secret | **PASS** | — |
| 10 | No invented owner names | **PASS** | The four register handles only. F3 is a recorded gap under OPEN-038. |
| 11 | Pre-merge reviews closed | **PASS** | F7 is now fully closed (CODE1-001). F8: the key change, HC-09 and IM-DG-04 are recorded. F3 and F5 are recorded gaps, not accepted. |
| 12 | D-RUN-25 addendum | **PASS** | It is bounded and documented, uses only existing owners, and lists A1-A6, R1, C2, C4 and H1 for ratification (IM-SU-04). No ratification is claimed. |
| 13 | Deviations visible | **PASS** | DEV-01..DEV-10 with unique IDs. DEV-09 and DEV-10 state openly that the guards were not red against code. |
| 14 | Local completion state | **PASS** | `BUILT — ACCEPTANCE PENDING HV-01..HV-11`. No "Done" claim. The merge carriers are written by the orchestrator at merge and are not checked by this gate. |
| 15 | AGENTS.md §9 human sign-off | **NOT RECORDED** | OPEN-016. |

## Candidate document gaps

| Candidate | Document (name, version, section) | Gap | Blocker | Reason |
|---|---|---|---|---|
| None new | — | The three round-1 candidates are now recorded by the run as IM-DG-03 and IM-DG-04, plus the A4 ownership choice under IM-SU-04. | No | The precedence rules and recorded defaults let the story proceed. Ratification by the tech lead is pending, not claimed. |

## Verdict

CODE1-001 is fixed in the code. V4 rejects `.`, `..`, empty segments and `:`. V9 normalises the path
and refuses any target outside the repository root. My copy of the logic, checked against the code
itself, gives the expected result for every probe pattern, including an escape to an existing sibling
worktree. The red log shows both new tests failing before the fix. CODE1-002 and CODE1-003 are fixed in
the records: DEV-08 and IM-SU-04 now list C2, C4 and H1; HC-09, IM-DG-03 and IM-DG-04 are recorded; DEV-10
explains the probe-file red run, and its source exists; and the stale text is corrected. The figures
match the native reports at `d018cf7`, and no superseded figure is presented as current. This review
records no approval, acceptance or ratification. The tech-lead ratification of the D-RUN-25 addendum
(IM-SU-04) and the AGENTS.md §9 human sign-off (OPEN-016) are still outstanding.

CODE_GATE: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]

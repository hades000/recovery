# Code gate review, round 1: RWB-TE-002 (RUN_ID `INC-004-epic-1-RWB-TE-002`)

> Orchestrator note (19 Nov 2026, REVIEW-001 H-10): where this review says the pre-merge reviewer "accepted" the
> remaining up-to-date case of the `test` task, that is the reviewer's wording. Nothing was accepted by the
> orchestrator (D-RUN-09); the residual is registered as open in OPEN-056.

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-002-CODE-001` |
| Gate | Code gate, pre-merge, round 1 |
| Story | RWB-TE-002 Code owners for the recovery module (EPIC-001, P2 technical enabler) |
| Range | `git diff develop-recovery...feature/RWB-TE-002-code-owners` (merge base = `develop-recovery` tip `0b87102`, RWB-E1-042 merged) |
| Tip | `c740d25` (`c740d2503198fddd7b4a2841b3126c4f18605cc8`). This is the branch ref and the worktree `HEAD`; `git status --short` in `rwb-wt/RWB-TE-002` is empty. The branch merged `develop-recovery` at `a3af237`. |
| Spec / plan | `specify/spec.md` (remediation run 4; spec gate round 5 PASS), `plan/plan.md` v2, `plan/tasks.md`, `plan/data-model.md`, `plan/tests/scenarios.md` (plan gate round 1 PASS); D-RUN-24, D-RUN-25 and the RWB-TE-002 rows of `AI-SDLC-BUILD-LOG.md` |
| Inputs read independently | The 16-file diff; `.gitlab/CODEOWNERS`, register, host settings, MR template at `c740d25`; the four helper classes and five test classes; `review/ponytail-review.md`, `review/security-review.md` (both at `ae61b08`); `implement/plan-addendum.md`, `deviations.md`, `document-gaps.md`, `shared-updates.md`, `implementation-report.md`, `handoff.md`; `implement/backend/{red-remediation,red-magic-number,green-remediation}.txt`, `final-tip-{codeowners,test}.log`, `final-tip-counts.txt`, `final-tip-scope.txt`; native JUnit XML `backend/build/test-results/{codeOwnersTest,test}` and native JaCoCo XML in the worktree and in `implement/backend/coverage-final/`; `docs/README.md`, `docs/COMPLIANCE.md`, `docs/ARCHITECTURE.md`, `docs/document-gaps.md`; `api-tests/report.md` + `summary.json`; `functional-tests/report.md` + `attempt-1/` |
| Re-runs | No Gradle run: the native XML at the tip (21:11-21:12) and the saved copy agree byte for byte (JaCoCo SHA-256 `94c5f422e621…` in both places), and no claim needed a re-run. One read-only probe: a single-file Java program, run outside the repository, that copies `supported()` and `matchesAFile()` from `CodeOwnersValidator` (CODE1-001). |
| Repository | Read only apart from this file. |
| Human sign-off | **Not recorded.** OPEN-016. This review records no approval, acceptance or ratification (D-RUN-09). |

## Status

**FAIL** (Low only): 0 Critical, 0 High, 0 Medium, 3 Low.

REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.

The build, the scope and the trace are sound. After the 11 D-RUN-25 addendum lines are taken out, the
code owners file matches the spec block exactly (with `{te001FixtureRoot}` = `th/co/scb/ace/boundaryfixture`).
All 26 planned UT methods ran and passed, and the figures match the native reports. The three Low
findings are: an incomplete containment fix for security F7 (CODE1-001); parts of the F8 fix that are
not fully recorded (CODE1-002); and evidence records that do not explain one red result and still
carry some stale `ae61b08` text (CODE1-003).

## Findings

| ID | Severity | Maps to | Finding | Evidence | Remediation |
|---|---|---|---|---|---|
| CODE1-001 | Low | SPEC-008 (V4, V9); security F7; ponytail Nice 2; CODE-TE002-03 | **The root-containment part of F7 is not fixed, but the fix is described as if it were.** C2 rejects `.` and `..` segments only (`CodeOwnersValidator.java:32`, `:147`). The comment there says it closes the root escape (F7). The second half of the F7 fix ("normalise `target` and require `target.startsWith(root.normalize())`") was not done, so `matchesAFile` (`:150-151`) still resolves `root.resolve(pattern.substring(1))` with no containment check. A pattern that starts with two slashes, or that holds a drive letter, passes V4 and V9 while it names a folder outside the checkout. Probe (same logic, this workstation): `//Windows/` → `C:\Windows`, `supported=true`, `dir=true`, `insideRoot=false`. `/C:/Windows/` gives the same result. On a Linux runner `//etc/` resolves to `/etc` in the same way. A related case: `/backend//src/` passes V9, because the path normalises to `backend/src`, but `OwnershipResolver.matches` (`:223`) never matches it, and GitLab does not either. This is the same "V9 green, nothing owned on the host" class of problem that Nice 2 describes. The impact is the same as F7 (Low): only metadata is read, nothing is written or run, and the file is owned by both teams. But the record presents F7 as closed (`plan-addendum.md` C2; `deviations.md` DEV-08 "F6-F8"; build log 21:16:24 "Fixed with tests: … F7"). | `CodeOwnersValidator.java:31-32, 146-164`; `review/security-review.md` F7 "Fix"; the probe output is quoted here | In V4, also reject an empty segment (`//`) and a `:`. In `matchesAFile`, normalise and require `target.startsWith(root)`, as F7 asked. Add `//x/` and `/C:/x/` (or `/x//y/`) cases to `dotSegmentPatternsAreRejected`. Alternatively, record the remaining part of F7 as an open residual and stop calling it closed. |
| CODE1-002 | Low | SPEC-013; `data-model.md` §7; UT-24; security F8; D-RUN-25; IM-SU-04 | **The F8 fix is only partly recorded, and two changes to spec or plan text are left out of the ratification list.** (a) Change C4 sets the cache key to `gradle-codeowners`. SPEC-013 says "gradle cache as `backend-unit`" and `data-model.md:368` says `key: gradle`, so C4 departs from both texts, and UT-24 now asserts the opposite (`PipelineDefinitionTest.java:39-40`). C2 widens V4 beyond its spec text (V4 lists `*`, `?`, `[`, `!` and `\` only). Both changes are in `plan-addendum.md`, but DEV-08 and the ratification item IM-SU-04 list only the CODEOWNERS lines and the reserved patterns. (b) A separate key alone does not stop cache poisoning: a pipeline on an unprotected branch can still write the `gradle-codeowners` key. The control that works is the host setting the reviewer named, "separate caches for protected branches", with a request to add that check to `host-settings.md`. That was not done, and no open item or gap row carries it. (c) Not pinning the image by digest is a **legitimate gap**: SPEC-013 fixes `eclipse-temurin:21-jdk`, the existing `backend-unit` job uses the same tag, and the document set gives no digest, so pinning would invent a value. But the gap is written down only as one bullet under "Not changed" in `plan-addendum.md:41`. It has no gap row (Blocker Yes/No) and no row in `docs/COMPLIANCE.md` §6. | `.gitlab-ci.yml:36-38`; `spec.md:116`; `plan/data-model.md:368`; `implement/deviations.md:12`; `implement/shared-updates.md:10`; `.gitlab/host-settings.md` (HC-01..HC-08, no cache row); `implement/document-gaps.md` (IM-DG-01, -02 only) | Add C2 and C4 to DEV-08 and to the IM-SU-04 ratification text. Record one gap or open-item row, Blocker No, for (b) the protected-branch cache setting (a host-settings row once ratified, or with OPEN-038) and (c) the image digest, and list both in `docs/COMPLIANCE.md` §6. Do not invent a digest. |
| CODE1-003 | Low | AGENTS.md §1.3 / §3.10 (tests first); DEV-09; evidence integrity | **The evidence does not explain one red result, and some stale text remains.** (a) `red-remediation.txt:29-30` shows `noHigherPrecedenceCodeOwnersFileExists()` failing with an `AssertionError` at `CodeOwnersValidationTest.java:418`, which is `assertThat(root.resolve("CODEOWNERS")).doesNotExist()`. That can fail only if a root `CODEOWNERS` file existed in the worktree at `1948f97`. No commit adds or removes one, the tip worktree has none, and no file records that a probe file was placed and later removed. Like the Nice-3 guard (DEV-09), this test cannot be red against code: it guards the state of the repository. `implementation-report.md:11` lists it as an ordinary red test. (b) Stale text: the `sources` front matter in `docs/README.md:10` still says "code and .gitlab/ files at ae61b08". The header of `implementation-report.md:3` still says "base `7bee04d`, code tip `ae61b08`" (line 5 supersedes it). `docs/document-gaps.md` DOC-DG-02 still says no API or functional N/A report exists, but both exist now. | `implement/backend/red-remediation.txt:29-30`; `git show 1948f97 --stat` (test files only); worktree root listing at `c740d25`; `docs/README.md:10`; `implement/implementation-report.md:3, 11`; `docs/document-gaps.md:8` | Add a DEV-10 row, or extend DEV-09, to say how the precedence guard was made red (a temporary probe file, then removed) or that it is a guard test that was never red against code. Correct the three stale lines, or mark them superseded. |

## Required verification (on files and logs)

### 1. Pre-merge reviews closed

| Review item | Closure | Verified on files and logs |
|---|---|---|
| Ponytail Must 1 (empty register fails open) | **Closed** | `CodeOwnersValidator.java:111`: `register.problems().isEmpty() && !handles.contains(owner)`. `emptyOwnerListStillChecksEveryOwner` was red at `1948f97` (`red-remediation.txt:26`) and passes at `c740d25` (native XML). A broken register is still an ERROR (V11), so the rule fails closed either way. |
| Ponytail Nice 2 (`..` pattern) | **Closed for dot segments**; see CODE1-001 for other non-normal forms | `dotSegmentPatternsAreRejected` (red `:20`, now green). It covers `/backend/../x/`, `/./AGENTS.md` and `/x/..`. |
| Ponytail Nice 3 (stale up-to-date) | **Closed as the reviewer proposed** | `build.gradle.kts`: `outputs.upToDateWhen { false }` on `codeOwnersTest` only, which is the reviewer's own proposed fix. A note on what remains: the `test` task (the `dev.ps1 test` path) can still be UP-TO-DATE after a file outside its six declared inputs is deleted. The reviewer accepted this ("or accept it as is since CI covers it"), and no document claims otherwise (`ARCHITECTURE.md:85` describes `codeOwnersTest` only). Guard test `codeOwnersTestIsNeverUpToDate`: see DEV-09 below. |
| Security F1 (High, `/CODEOWNERS` precedence) | **Closed** | Addendum A2/A3 put `/CODEOWNERS` and `/docs/CODEOWNERS` in both control sections, so adding either file needs both teams under the target branch's `.gitlab/CODEOWNERS`. R1 adds them as reserved patterns. `noHigherPrecedenceCodeOwnersFileExists` and `addendumPathsHaveOwners` pass. `liveFileAndRegisterPass` asserts the four V10 warnings at lines 34, 35, 41 and 42, which match the file. |
| Security F2 (High, `application*.yaml`) | **Closed** (ratification pending) | A4/A5: both files need `[Common module]` (`@scb-ace/ace-team`) and `[Recovery module]`. `addendumPathsHaveOwners` asserts exactly these two sections. |
| Security F3 (Medium, placeholder groups) | **Legitimate recorded gap, Blocker No** | SPEC-017 requires the two `@role-placeholder/` handles. The real group names are not in the document set (OPEN-038). HC-08 and HV-11 require replacement before host use. The merge carrier text is required by spec "Local completion state". The reviewer's other fixes (a CI error on PLACEHOLDER, ACE team as second owner) would depart from the spec and invent a decision. It is recorded in `docs/COMPLIANCE.md:129`, `handoff.md:62` and `implementation-report.md:43`, with "not accepted". |
| Security F4 (Medium, Dockerfile) | **Closed** (owner is a placeholder, so F3 applies) | A6 in `[Pipeline gates]`; `addendumPathsHaveOwners`. `COMPLIANCE.md:129` states that F3 now also covers `backend/Dockerfile`. |
| Security F5 (Low, fixtures unowned) | **Recorded gap** | `PROP-OI-4`, IM-DG-02 (Blocker No, with reason), `COMPLIANCE.md:127`. |
| Security F6 (Low) | **Closed** | Same as Must 1. |
| Security F7 (Low) | **Partly closed** | Dot segments are rejected. Root containment is not implemented. See **CODE1-001**. |
| Security F8 (Low) | **Cache: key changed; host control not recorded. Image pin: legitimate gap, under-recorded** | See **CODE1-002**. |

### 2. D-RUN-25 addendum (A1..A6, R1, C1..C4)

- **Documented deviation:** yes. `plan-addendum.md:6` says "a deviation from the spec block, not a
  reading of it". DEV-08 covers it, and so does D-RUN-25 in the build log. I removed lines 8-9, 19, 26-27, 34-35, 41-42 and
  58-59 from `.gitlab/CODEOWNERS`, and what remains matches the spec block (`spec.md:263-317`, 55 lines)
  exactly, with the fixture-root substitution. Nothing else in the block changed.
- **Justified:** yes. A1 is needed for BR1 and UT-26 after the RWB-E1-042 merge (`red-magic-number.txt:56`,
  EXITCODE=1, then green). A2/A3 close High F1, A4/A5 close High F2, and A6 closes Medium F4. All of
  them follow D-RUN-09: the findings are fixed, not accepted.
- **Bounded:** yes. 11 CODEOWNERS lines, 2 register entries and 4 code or CI changes, each named, and
  each with a test that ran (list above). The shadowing check (V6) and the duplicate check (V5) pass on the live file.
- **Existing owners only:** yes. The diff uses exactly the four handles in the register, plus the
  synthetic fixture handle `@scb-ace/recovery-leads-typo` (UT-07). No owner was added or renamed.
- **Flagged for ratification, none claimed:** yes. IM-SU-04 is proposed (not yet in `aisdlc/docs/open-items.md`;
  the orchestrator applies it at merge). D-RUN-25 ends "Nothing here is an approval", and a search of
  `implement/`, `docs/` and the test folders finds no claim of ratification, acceptance or "Done".
  The IM-SU-04 text leaves out C2 and C4 (CODE1-002).
- Point for the tech lead, not a finding: A4 puts `application*.yaml` in the section named `[Common module]`,
  which BR3 defines as the common module folder. The security review asked for "a section that the ACE
  team owns", and this placement follows that request. The section name is part of what the ratification decides.

### 3. Figures against native reports

| Figure | Claimed (report, counts, README, COMPLIANCE) | Native | Match |
|---|---|---|---|
| `codeOwnersTest` methods | 33, 0 F / 0 E / 0 S | 5 XML files in `test-results/codeOwnersTest`: tests 33, failures 0, errors 0, skipped 0 | Yes |
| Backend `test` | 421, 0 failures | `test-results/test`: 421 / 0 / 0 / 0; `final-tip-test.log` TIP `c740d25`, BUILD SUCCESSFUL, EXITCODE=0 | Yes |
| LINE | 95.71 (201/210) | 201/210 = 95.71 | Yes |
| BRANCH | 95.83 (115/120) | 115/120 = 95.83 | Yes |
| INSTRUCTION | 96.83 (1251/1292) | 1251/1292 = 96.83 | Yes |
| METHOD | 100.00 (43/43) | 43/43 | Yes |
| Coverage scope | Four helper classes | 11 classes (4 top-level plus 7 nested records and enums), no `*Test` class; `executionData(codeOwnersTest)` on both JaCoCo tasks; verification `dependsOn(codeOwnersTest)`; minimum 0.80 on all four counters | Yes |
| Saved XML | `coverage-final/codeOwnersCoverageReport.xml` | Byte-identical to the worktree `build/reports/jacoco/codeOwnersCoverageReport.xml` (21:11:54) | Yes |

`implement/backend/coverage/` (XML, HTML, `counters.txt`) holds the `ae61b08` figures (95.69/95.76/96.80/100). It is labelled superseded wherever it is cited.

### 4. API Tester and Functional Automation Test

Both `NOT_APPLICABLE`, with evidence that agrees with the spec: API In Scope `NO`, `NO_API_CHANGE`
(`spec.md:27-28, 202-211, 568`), empty contracts; UI In Scope `NO`, design evidence `NOT_REQUIRED`
(`spec.md:25, 32, 571`). Both reports checked the diff at `ae61b08`. At `c740d25` the 16-file list is the
same (`final-tip-scope.txt`), and I confirmed that `git diff --name-status develop-recovery...feature/RWB-TE-002-code-owners -- frontend api backend/src/main` is empty. Each report notes that the orchestrator saved it from the agent's returned text. Neither records an approval.

### 5. DEV-09

DEV-09 is recorded openly (`deviations.md:13`, `COMPLIANCE.md:105`, build log 21:16:24) and is acceptable as a
deviation record. Nice 3 named no test. The guard checks a build-script property, so it cannot be red
against Java code. It is additive and weakens nothing. The precedence guard has the same nature but is
not recorded that way (CODE1-003).

### 6. Remediation diff `ae61b08..c740d25`

The TE-002 part is 8 files, +317/-5: CODEOWNERS +11, register +4, CI cache key, `upToDateWhen`, 8 lines in the
validator, and 4 test files. The other changes in this range come from the `develop-recovery` merge
(RWB-E1-042, gated separately by its code gate round 4, PASS). This includes the E1-042 `build.gradle.kts`
hunks, which are not part of the three-dot diff. The pre-merge reviews cover `ae61b08`. I reviewed the
remediation for security myself, so a separate ponytail or security round is not needed beyond the findings above:

- **CODEOWNERS bypass:** the `/CODEOWNERS` and `/docs/CODEOWNERS` precedence gap is closed (F1). The new lines create no
  shadowing (V6 clean). Control files still need both teams (`controlFilesNeedBothTeams`). A6 depends on a placeholder owner (F3, recorded).
- **Reserved paths:** the reserved list is keyed by the exact pattern string. A reserved pattern only turns
  a V9 error into a V10 warning, and the register that holds the list is owned by both teams. The F1 guard test fails if either file appears. No bypass.
- **Glob and `..` handling:** wildcards are still rejected, and `.`/`..` segments are now rejected. The `//` and drive-letter
  forms are still accepted: **CODE1-001**.
- **File-system access:** read only (`isRegularFile`, `isDirectory`, `Files.walk` without `FOLLOW_LINKS`). There are no writes outside `@TempDir`, no process
  execution, and YAML is loaded with `SafeConstructor`. The only exposure is the containment gap in CODE1-001 (existence checks outside the root).
- **V7 change:** it fails closed on `owners: []`, and a register with problems is already an ERROR, so the change opens no new path.
- **CI:** no secret, service or privileged setting is added. On the cache key, see CODE1-002.

## Gate checklist (full code gate at `c740d25`)

| # | Gate | Result | Evidence |
|---|---|---|---|
| 1 | SPEC-001..019, AC1..AC7, BR1..BR7 trace | **PASS** | Each locally testable row maps to a passing method (`plan/tests/scenarios.md:50-75`, and each name is in `final-tip-counts.txt`). The host rows (SPEC-006, -010..-012, -018) are documented in `.gitlab/host-settings.md` HC-01..HC-08 and HV-01..HV-11, all `OPEN — NOT_TESTED_HERE`, and none is claimed as passed. SPEC-019 exclusions are in `COMPLIANCE.md` §6. |
| 2 | Governance files | **PASS** | `.gitlab/CODEOWNERS`: spec block plus the D-RUN-25 addendum. Register: the spec block plus R1. `host-settings.md` matches the spec table HC-01..HC-08 word for word. MR template: eight headings in order, no person (UT-21). |
| 3 | Validator and UT-01..UT-26 | **PASS** | 26 planned methods plus 5 remediation tests plus 2 guards = 33, all passing. Every V-rule has a passing and a failing case. |
| 4 | `codeOwnersTest` and the 80% gate on four counters | **PASS** | Section 3 above. The gate is defined here and runs on the host (HV-07); the Builder's run is implementation evidence, not a `TESTED_LOCALLY` claim. |
| 5 | `codeowners-validation` CI job | **PASS** (definition) | Stage `verify`, image, script, JUnit path and no `rules:` are as SPEC-013 states. UT-24 checks this. The cache key departs from the spec text (CODE1-002). The XML is not in the artifact (DEV-07 / IM-SU-02, recorded). |
| 6 | AGENTS.md §5 fix | **PASS** | The diff changes exactly the five path cells and the coding-standard cell, as SPEC-016 requires. UT-22 passes. |
| 7 | No main-source, `frontend/` or `api/` change | **PASS** | The `--name-status` diff over those paths is empty. All Java is test scope. |
| 8 | No dependency added | **PASS** | The `build.gradle.kts` diff adds a block at the end of the file and adds no dependency or plugin line. SnakeYAML was already on the test classpaths (preflight #3). |
| 9 | No personal data, no secret | **PASS** | The diff holds group handles only. `someone@example.test` is the synthetic UT-08 value. No token or credential appears. |
| 10 | No invented owner names | **PASS** | Only the register's handles (2 `ASSUMED`, 2 `PLACEHOLDER`), under OPEN-038. F3 is a recorded gap. |
| 11 | Pre-merge reviews closed | **PASS with Low findings** | Section 1. F7 is only partly closed (CODE1-001). The F8 record is incomplete (CODE1-002). |
| 12 | D-RUN-25 addendum | **PASS** | Section 2. The ratification is pending (IM-SU-04) and is not claimed. |
| 13 | Deviations visible | **PASS with Low finding** | DEV-01..DEV-09 are present and the IDs are unique. One red result is unexplained (CODE1-003). |
| 14 | Local completion state | **PASS** | `BUILT — ACCEPTANCE PENDING HV-01..HV-11` everywhere. No "Done" or "§13 met" claim. The merge carriers (the `--no-ff` merge commit and `README.md`) are written by the orchestrator at merge and are not checked by this gate (spec, "Local completion state"). |
| 15 | AGENTS.md §9 human sign-off | **NOT RECORDED** | OPEN-016. |

## Candidate document gaps

| Candidate | Document (name, version, section) | Gap | Blocker | Reason |
|---|---|---|---|---|
| CI image digest | RWB-TE-002 spec run 4, SPEC-013 (image `eclipse-temurin:21-jdk`); Engineering Practices v5 (no image or digest policy found for the ACE pipeline) | The document set names a tag and no digest, so security F8's request to pin by digest has no source value. | No | The spec fixes the tag, and the existing jobs use the same tag. Pinning is ACE host or pipeline work under OPEN-038. Record it, do not invent it (CODE1-002). |
| Protected-branch cache separation | Story file v7 RWB-TE-002 §12 (branch rule list); spec "Host configuration record" HC-01..HC-08 | No host setting covers GitLab's "separate caches for protected branches", which is the control that makes a distinct cache key effective. | No | It concerns host hardening of the CI job, not the story's acceptance. It can be added as a host-settings row after ratification, or carried under OPEN-038. |
| Ownership of shared service settings | RWB-TE-002 story §12 / BR3 (common module = a folder) versus the D-RUN-25 addendum A4 (`application*.yaml` in `[Common module]`) | The document set does not say which team owns the shared `application*.yaml`, so the addendum's choice has no source. | No | It is recorded as a deviation with tech-lead ratification (IM-SU-04). Both teams are required, which is the safer reading. |

## Verdict

The story delivers what the spec requires inside the local boundary. The file and register match the
gated block plus a bounded addendum that is documented and awaits ratification. Every V-rule and every
UT ran and passed. The coverage figures match the native JaCoCo XML exactly. The tree has no main,
frontend or API change and no new dependency, and the API and functional N/A reports are supported by
evidence. Both pre-merge reviews are answered on file: High F1 and F2 are fixed with tests, F3 and F5
are gaps recorded with reasons and are not accepted, and DEV-09 is open about the guard test. Three
Low findings remain: containment for F7 (CODE1-001), the F8 and ratification records (CODE1-002), and
the red-evidence and stale-text records (CODE1-003). This review records no approval, acceptance or
ratification. The AGENTS.md §9 human sign-off is still outstanding (OPEN-016).

CODE_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 3]

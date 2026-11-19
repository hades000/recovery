# Spec gate re-review (round 3): RWB-TE-002 Code owners for the recovery module

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-002-SG-2026111703` |
| RUN_ID | `INC-004-epic-1-RWB-TE-002` |
| Gate | Specification gate, re-review after remediation run 2. Under D-RUN-09 the orchestrator re-ran the Technical Specifier for SG-012 to SG-016 instead of accepting the Low-only failure (`AI-SDLC-BUILD-LOG.md` line 32, timeline line 100). The orchestrator is Claude Code, the AI agent running this pipeline. Every remediation choice reviewed here is that orchestrator's triage, as written in `specify/gate-response.md` "Round 2". No person decided or approved any of it. |
| Previous reviews | `REVIEW-RWB-TE-002-SG-2026111701` (`review/spec-gate-review.md`), `FAIL` 0C/2H/6M/3L, SG-001 to SG-011. `REVIEW-RWB-TE-002-SG-2026111702` (`review/spec-gate-review-2.md`), `FAIL` 0C/0H/0M/5L, SG-012 to SG-016 |
| Artefacts reviewed | `specify/spec.md` (551 lines), `specify/compliance-validation.md`, `specify/assumptions.md`, `specify/document-gaps.md`, `specify/gate-response.md` (Round 1 and Round 2), `specify/shared-updates.md`, `specify/agent-run-log.md`, `specify/contracts/backend-apis.json`, `specify/contracts/frontend-integrations.json`. I used the `*.run2.md` copies only to diff what changed. |
| Baseline | As in review 2: Story Files v7, RWB-TE-002 story file v1 (`requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-002-code-owners-for-the-recovery-module-v1.md`); Decision Log v10; Engineering Practices v5 §4.2, §7, §10; AI Assisted Development Approach v1 §3, §6; Test Cases v7; Story Defects v4; `aisdlc/docs/decisions/decision-register.md`; `aisdlc/docs/open-items.md`; `aisdlc/evidence/phase0-standards-audit.md` A-05, A-10 |
| Rules applied | `aisdlc/.github/rules/pdlc.md` (lines 22–25, 31), `specification-execution-gates.md`, `implementation-execution-gates.md` (lines 41–43, 55–63, 67), `security-quality-standards.md`, `traceability-standards.md`, `versioning-standards.md` (line 24); `aisdlc/.github/contexts/testing-standards.md`; RUN-BRIEF; D-RUN-05, -06, -07, -08, -09 |
| Repository check | I read these files on 2026-11-17 and ran no git command: `scripts/dev.ps1`, `.gitlab-ci.yml`, `backend/build.gradle.kts`, `backend/settings.gradle.kts`, `backend/Dockerfile`, the three `.gitignore` files, `RecoveryMigrationLintTest.java`, `RecoveryBoundaryTest.java`, `ModulithTest.java`, `README.md`. I also listed the directory of every pattern in the spec's code owners block. |
| Reviewer | Compliance Reviewer (agent run) |
| Date | 2026-11-17 |

## Status

**`FAIL`** (Low-only; does not block the handoff automatically)

| Severity | Count | IDs |
|---|---|---|
| Critical | 0 | none |
| High | 0 | none |
| Medium | 0 | none |
| Low | 1 | SG-017 |

- SG-012 to SG-016 are resolved. Each fix was checked against the repository files (disposition table below).
- The fixes did not reopen any of SG-001 to SG-011.
- There is one new Low finding, SG-017: the merge condition added for SG-015 depends on an MR body. This repository has no MR, so nothing carries that body.
- Under `pdlc.md` lines 23–24 the status stays `FAIL`, and the finding stays visible. The fix is one paragraph of spec text.

## Disposition of the round 2 findings (SG-012 to SG-016)

### SG-012: CI job and coverage gate reported as tested locally — Resolved

**Change in the spec**

- **Boundary groups.** The local boundary now has four groups (`spec.md:36-46`).
  - Group (a) claims only what runs under `./scripts/dev.ps1 test`.
  - The CI job `codeowners-validation`, `codeOwnersTest`, the two codeowners JaCoCo tasks and the 80% gate are in group (b), "Defined here, run on the host" (`spec.md:44`).
- **Flow 2.** It uses the new value `DEFINED_HERE_RUN_ON_HOST`, and its pipeline run is `HUMAN_VERIFICATION` (HV-07) (`spec.md:81`).
- **Flow 6.** Only the rules are `TESTED_LOCALLY`. The pipeline run is HV-07 (`spec.md:85`).
- **HV-07.** It is extended to the job run and the 80% gate (`spec.md:416`).

**Required fix (1), local proof command.** Done. SPEC-014 and the Unit Test Applicability row name `cd backend; ./gradlew codeOwnersTest codeOwnersCoverageVerification` as the Builder's implementation-evidence command, with command, exit code and native XML/HTML saved (`spec.md:116`, `:217`). ASM-TE002-16 records why it is build evidence and not a local-test claim. This was one of the two options review 2 offered.

**Required fix (2), execution data.** Done. Both codeowners JaCoCo tasks take `executionData(codeOwnersTest)` (`spec.md:116`, `:238`).

**Required fix (3), job run as human verification.** Done.

**Optional item, YAML parse.** Taken. UT-24 parses the job definition and says it proves the definition only (`spec.md:491`).

**Repository check**

- `scripts/dev.ps1` lines 114–117 run only `Invoke-Gradle test` and `Invoke-Npm run check`. This matches `spec.md:38-39` and ASM-TE002-16.
- `.gitlab-ci.yml` has a `verify` stage, image `eclipse-temurin:21-jdk` and cache `{ key: gradle, paths: [.gradle-home/] }`, which SPEC-013 reuses. It uses no custom YAML tags, so SnakeYAML can parse it (UT-24).
- `backend/build.gradle.kts` has no `codeowners` task yet, so no claim about existing tasks is made. The Jacoco plugin is applied (line 8), so the new Test task gets the agent.
- `test` excludes only `recovery-it` and `e2e` (line 106), so tag `codeowners` runs in `dev.ps1 test` as the spec says.
- `backend/Dockerfile` builds with `bootJar -x test`, so tests that need the repository root never run in the backend image context.

### SG-013: section names not checked for uniqueness — Resolved

**Change in the spec**

- **V12.** New rule (`spec.md:374`): section names unique after trimming, compared without regard to case, ERROR `line {n}: duplicate section {s}`.
- **UT-23.** Two negative fixtures (case variant, trailing-space variant) and one positive fixture (`spec.md:490`).
- **UT-18.** A live assertion: each of the three BR4 control files is matched by at least two sections, the sections have names that differ without regard to case, and their owner sets do not overlap (`spec.md:485`).
- **Rule set.** SPEC-001, -005 and -008, the field matrix (`spec.md:152`) and the components table (`spec.md:235`) now say V1–V12.
- **ASM-TE002-11.** It records the GitLab same-name merge as an assumption, not a fact (`assumptions.md:19`).

**Check against the code owners block**

- `/.gitlab/CODEOWNERS`, the register and the host record are matched only by `[Code owners control ACE team]` and `[Code owners control recovery]` (`spec.md:270-279`).
- No other section has a `/.gitlab/` pattern that covers them, because `[Repository standards]` owns `/.gitlab/merge_request_templates/` only. So the UT-18 assertion holds for the file as written.

### SG-014: `backend/build.gradle.kts` unowned — Resolved

**Change in the spec.** The spec takes the `[Pipeline gates]` option that review 2 offered.

- **Paths owned.** `/backend/build.gradle.kts`, `/backend/settings.gradle.kts`, `/backend/gradle/`, `/backend/gradlew`, `/backend/gradlew.bat`, the six frontend root build files and `/scripts/dev.ps1` are owned by `@role-placeholder/techx-devops-with-scb-it` (`spec.md:288-301`).
- **Status.** The owner is `PLACEHOLDER` under OPEN-038 and HV-11.
- **Supporting changes.** SPEC-017 (`spec.md:119`), the path basis (`spec.md:318-320`), UT-25 (`spec.md:492`), ASM-TE002-17, and the out-of-scope row, which no longer lists these files (`spec.md:515`).

**Repository check**

- **Files.** Every new path exists: `backend/gradle/wrapper/gradle-wrapper.{jar,properties}` and the frontend files `package.json`, `package-lock.json`, `vite.config.ts`, `tsconfig.json`, `eslint.config.js` and `playwright.config.ts`.
- **Git-ignore.** None is ignored. `backend/.gitignore` un-ignores `gradle/wrapper/gradle-wrapper.jar`, and the root and frontend ignores do not match these files, so V9 holds in a CI checkout.
- **V6 shadowing.** There is none in the section. `/backend/gradle/` keeps its trailing `/`, so it does not cover `/backend/gradlew` under the SPEC-007 prefix rule.

### SG-015: no local completion state; OPEN-038 due date — Resolved (new issue SG-017)

**Change in the spec**

- **SPEC-018.** It now has the end state `BUILT — ACCEPTANCE PENDING HV-01..HV-11` and the rule that the story is never reported as Done or accepted against story §13 (`spec.md:120`).
- **New section.** "Local completion state (story §13)" (`spec.md:422-435`).
- **Coverage row.** A §13 "Done when" row was added (`spec.md:90`), so the table now has 38 rows. My count: 7 BR + 9 AC + 7 X + 7 flows + 8 others = 38. `compliance-validation.md:25` and the status block agree.
- **Status line.** `LOCAL_COMPLETION_STATE` was added to the status block (`spec.md:548`).
- **Open item.** `PROP-OI-1` (e) proposes moving OPEN-038 "Needed by" from "Before TE-002 build" to "Before TE-002 is used on the ACE host". It cites L-RCV-03 and the orchestrator's triage (`shared-updates.md:10`).
- **Card and matrix.** The card and matrix proposals carry the done state (`shared-updates.md:24`, `:35`).

**Repository check.** `aisdlc/docs/open-items.md` still says "Before TE-002 build" for OPEN-038. This is expected: shared files are applied by the orchestrator (RUN-BRIEF rule 3).

**New issue.** The merge condition added in the same section (`spec.md:433`) has no local carrier. See SG-017.

### SG-016: real-looking migration number in UT-15 — Resolved

**Change in the spec.** UT-15 now uses `…/recovery/V9999__rwb_te_002_resolver_fixture.sql` as a resolver input that is never written (`spec.md:482`).

**Repository check**

- **Name pattern.** The name matches `RecoveryMigrationLintTest.NAME` (`^V(\d{4})__(rwb_[a-z0-9]+_\d{3})_[a-z0-9_]+\.sql$`, line 25 of the test). `rwb_te_002` fits `rwb_[a-z0-9]+_\d{3}`.
- **Old pairing.** A grep of the current `specify/*.md` (excluding `*.run2.md`) finds no `V0001` or `rwb_e1_001`. The only mention is in `gate-response.md:49`, which describes the removal.
- **Lint scope.** The lint reads only the migration folder (`MIGRATIONS`, line 24), so the input can never reach it.

## Regression check of SG-001 to SG-011

I diffed `spec.md` against `spec.run2.md`. Every removed line was replaced by an extended version: the three-group boundary became four groups, V1–V11 became V1–V12, UT-01–UT-22 became UT-01–UT-25, and Flow 2, Flow 6, UT-15, UT-18, HV-07 and the out-of-scope row were rewritten. No content that closed an earlier finding was lost.

| Finding | Disposition in round 3 | Evidence (current line numbers) |
|---|---|---|
| SG-001 (High) No local boundary for host-only controls | **Still resolved** (strengthened) | Four groups `spec.md:41-46`; legend `:50-53`; HV-01–HV-11 `OPEN — NOT_TESTED_HERE` with owner and unblock `:402-420`; `:219-221` (no unit-test or Builder-run substitute for an HV item); no branch or test MR created `:518` |
| SG-002 (High) Common pattern matches no file | **Still resolved** | SPEC-004 `:106`; register `reservedPatterns` `:354-356`; V9/V10 `:371-372`; UT-10, UT-16, UT-17 `:477,483-484` |
| SG-003 (Medium) GitHub form | **Still resolved** | `.gitlab/CODEOWNERS` sections `:250-302`; HC-01–HC-08 `:388-397`; CLAR-001 `:527` |
| SG-004 (Medium) Owner existence needs host API | **Still resolved** | SPEC-009 `:111`; register `:330-357`; V7 `:369`; UT-07 `:474`; HC-08/HV-07 `:397,416`; ASM-TE002-06 |
| SG-005 (Medium) A-05 | **Still resolved** | SPEC-016 `:118`; UT-22 `:489`; SPEC-017 `:119`; exclusions `:513-514`; `PROP-OI-3` |
| SG-006 (Medium) A-10 MR template | **Still resolved** | SPEC-015 `:117`; UT-21 `:488`; HC-07/HV-09 `:396,418` |
| SG-007 (Medium) SPEC IDs undefined | **Still resolved** | Catalogue `:101-121`, 001–019 once each; every coverage-table ID resolves |
| SG-008 (Medium) Validator tests and applicability | **Still resolved** | Backend `YES`/`REQUIRED` 80% `:217`; V1–V12 each with a failing and a passing case (UT-01–UT-12, UT-23); resolver UT-13–UT-20, UT-25 |
| SG-009 (Low) Control files unowned | **Still resolved** (extended by SG-014) | Control sections `:270-279`; `[Pipeline gates]` `:288-301`; HV-11 `:420` |
| SG-010 (Low) TC-TE-002-08 | **Still resolved** | TC mapping `:494-497`; HV-06 `:415`; SP-DG-06 |
| SG-011 (Low) Stale status | **Still resolved** | Header `:7`, `:13` cite review 2 and this review; status block `:539-550` (38 rows, 11 HV open) |

## New findings

### REVIEW-RWB-TE-002-SG-017: the placeholder merge condition depends on an MR body that does not exist in this repository

| Field | Value |
|---|---|
| Severity | Low |
| Affects | SPEC-017 (`spec.md:119`, last sentence); SPEC-018 (`spec.md:120`); "Local completion state (story §13)", row "Merge condition for placeholders" (`spec.md:433`); `shared-updates.md:10` (`PROP-OI-1`) |
| Evidence | `spec.md:433` says the two `@role-placeholder/…` and two `ASSUMED` handles are acceptable at the merge into `develop-recovery` "only if the MR body shows the open item". The code gate checks that text, and without it "the MR is not ready to merge". This repository has no repository host (RUN-BRIEF hard rule 5; `spec.md:8`, `:36`). Merges into `develop-recovery` are made by the orchestrator from per-story worktrees (D-RUN-06, `AI-SDLC-BUILD-LOG.md` line 29), not through an MR. No lifecycle agent in `aisdlc/.github/agents/` writes an MR or PR description, and `README.md` names no local MR record. The spec does not say which local file carries the required text, or which stage writes it. |
| Problem | The code gate has nothing to check, so a later stage will do one of two things. It may treat the missing MR body as a block, although no stage can produce one. Or it may skip the check, and the placeholders then reach `develop-recovery` with no visible statement that OPEN-038 is open. Either way, the control that SG-015 asked for (`pdlc.md:31`: checks outside automation stay visible) is not enforceable here. |
| Required fix | Name the local carrier and its writer in the "Merge condition for placeholders" row and in SPEC-017. One option: the Implementation Builder writes `output/INC-004-epic-1-RWB-TE-002/implement/merge-request.md` from `.gitlab/merge_request_templates/Default.md`, with the required sentence under `Acceptance criteria covered`. The code gate checks that file, and the orchestrator uses its text as the merge commit body. Keep the MR-body wording for the ACE host, where an MR exists. Any equivalent local file is acceptable if the spec names its path and the stage that writes it. |

## Observations (not findings)

1. **TC count.** `spec.md:425` says "Six of the eight §16 cases are host-only or only partly checked here". By the TC mapping (`spec.md:494-496`) all eight depend on an HV item: five are partly checked by a UT and three are host-only. The conclusion is unchanged. The wrong count came from review 2 (SG-015 evidence), and this review corrects it. Fix the count in the next spec edit.
2. **Triage evidence pointer.** `agent-run-log.md:63` says the orchestrator's per-finding triage "is logged in `AI-SDLC-BUILD-LOG.md`". The build log has the policy (D-RUN-09, line 32) and one generic row (line 100, "Remediation run 2 for SG-012..SG-016"). The per-finding triage text is only in `gate-response.md` "Round 2", column "Orchestrator triage". The orchestrator may add a triage row to the build log, or the run log may point to `gate-response.md`.
3. **Contracts.** `contracts/*.json` are unchanged since run 1 and still correct: `NO_API_CHANGE`, no integrations, and `backend/build.gradle.kts` listed as a backend-only change.

## Document gaps

SP-DG-01 to SP-DG-10 are unchanged since review 2 and still correct, and none is a blocker. Neither run-2 change nor SG-017 needs a new document gap: SG-017 is a spec defect about this repository's merge path, not a silence or conflict in the document set.

## Plan inputs (not findings)

1. **Sequencing (P1).** `backend/src/test/resources/architecture/` is still empty. RWB-TE-001 now has a remediated spec (`output/INC-002-epic-1-RWB-TE-001/specify/spec.md`), and it keeps the module map path `backend/src/test/resources/architecture/recovery-modules.yaml`, which matches `spec.md:264`.
2. **SnakeYAML on the compile classpath.** The validator, register reader and UT-24 import SnakeYAML types, so the library must be on `testCompileClasspath`, not only on `testRuntimeClasspath` (ASM-TE002-09, P2). Confirm both with `gradlew dependencies`. Add no dependency (AGENTS.md §4.4).
3. **Carried from review 2, plan input 2.** The spec still does not decide these three files:
   - `backend/src/test/java/th/co/scb/ace/demo/ModulithTest.java`;
   - `backend/src/main/resources/application*.yaml` (the `rwb.*` settings);
   - `frontend/src/i18n/index.ts`.

   Decide each against BR1/BR2 and record the decision in the plan.
4. **Cross-story consistency.** RWB-TE-011 now adds `/tools/pdpa-lint/` to `[Recovery module]` of `.gitlab/CODEOWNERS` and depends on RWB-TE-002 merging first (`output/INC-006-epic-1-RWB-TE-011/specify/spec.md:393-401`). This is consistent with SPEC-001 and V4/V7/V9. The "exact content" in SPEC-001 is the content at the RWB-TE-002 merge, so UT-12, UT-18 and UT-25 must not assert the whole file byte for byte.
5. **Spec status for the Builder.** `implementation-execution-gates.md:67` requires `Status: SUCCESS` in `spec.md` before implementation. The spec header says `DRAFT — awaiting spec gate re-review` (`spec.md:13`). Update it when the gate result allows.

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 1]
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
REVIEW_GATE: WARNING — Low-only (SG-017); SG-012..SG-016 resolved; SG-001..SG-011 remain resolved.
NEXT_STEP: Under D-RUN-09 the orchestrator either re-runs the Technical Specifier to fix SG-017 (name the local merge-request record and its writer) and re-gates as review/spec-gate-review-4.md, or routes SG-017 to the engagement lead for a human disposition. The Implementation Planner then starts after RWB-TE-001 merges the module map (precondition P1).
```

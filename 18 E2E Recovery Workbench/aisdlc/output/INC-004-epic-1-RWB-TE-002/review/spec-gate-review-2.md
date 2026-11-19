# Spec gate re-review: RWB-TE-002 Code owners for the recovery module

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-002-SG-2026111702` |
| RUN_ID | `INC-004-epic-1-RWB-TE-002` |
| Gate | Specification gate, re-review after remediation run 1 (orchestrator gate triage, `AI-SDLC-BUILD-LOG.md` timeline 2026-11-17T23:21:27) |
| Previous review | `REVIEW-RWB-TE-002-SG-2026111701` (`review/spec-gate-review.md`), `FAIL` 0C/2H/6M/3L, findings SG-001 to SG-011 |
| Artefacts reviewed | `specify/spec.md`, `specify/compliance-validation.md`, `specify/assumptions.md`, `specify/document-gaps.md`, `specify/gate-response.md`, `specify/shared-updates.md`, `specify/contracts/backend-apis.json`, `specify/contracts/frontend-integrations.json` |
| Baseline | Story Files v7, RWB-TE-002 story file v1 (`requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-002-code-owners-for-the-recovery-module-v1.md`); Decision Log v10 (DL04, DL05, DL32, DL36, DL37, DT11); Engineering Practices v5 §4.2, §7, §10; AI Assisted Development Approach v1 §3, §6; Recovery Workbench Test Cases v7 row TC-TE-002-08; Story Defects v4 (RWB-TE-002 defect 1); `aisdlc/docs/decisions/decision-register.md` (D-RCV-10, -19, -21, -37, -50; L-RCV-03, -12, -13); `aisdlc/docs/open-items.md` (OPEN-024, OPEN-038, OPEN-041); `aisdlc/evidence/phase0-standards-audit.md` A-05, A-10 |
| Rules applied | `aisdlc/.github/rules/specification-execution-gates.md`, `pdlc.md`, `implementation-execution-gates.md`, `security-quality-standards.md`, `traceability-standards.md`; `aisdlc/.github/contexts/testing-standards.md` §6; RUN-BRIEF; D-RUN-01, -05, -07, -08 |
| Repository check | File tree read on 2026-11-17 (no git command run). Every pattern in the spec's code owners block was checked against the tree. |
| Reviewer | Compliance Reviewer (agent run) |
| Date | 2026-11-17 |

## Status

**`FAIL`** (Low-only; does not block the handoff automatically)

| Severity | Count | IDs |
|---|---|---|
| Critical | 0 | none |
| High | 0 | none |
| Medium | 0 | none |
| Low | 5 | SG-012 to SG-016 |

All eleven findings of the first review are resolved (disposition table below). The five new findings
are Low. Under `pdlc.md` (lines 23 and 28–29) the status stays `FAIL`, every finding stays visible, and
the handoff to the Implementation Planner may go ahead with the warning below once a human records a
disposition. Each new finding is small enough to fix in the plan, or in a short spec edit, without
another gate round.

### What is right in the remediated spec

- **Three-way boundary (orchestrator triage).** `spec.md:34-43` separates (a) what is built and tested
  here, (b) host settings that are documented only (HC-01 to HC-08, `spec.md:358-376`), and (c) human
  verification (HV-01 to HV-11, `spec.md:378-396`). Each HV item is `OPEN — NOT_TESTED_HERE`. It has a
  document-set role as owner ("ACE team repository administrator with the recovery tech lead",
  `spec.md:380`) and an unblock condition (OPEN-038 and proposed `PROP-OI-2`). The coverage table has
  a "Verification here" column that never reports a host-only clause as tested (`spec.md:47-88`).
  `spec.md:213` says unit tests do not stand in for host clauses. SPEC-018 (`spec.md:114`) forbids any
  stage from reporting an HV item as passed on local evidence.
- **Paths.** Every pattern in `spec.md:248-281` was checked against this repository.
  `backend/src/main/java/th/co/scb/ace/demo/recovery/`, `backend/src/test/java/th/co/scb/ace/demo/recovery/`,
  `backend/src/test/java/th/co/scb/ace/demo/e2e/` (`PlatformE2ETest.java`),
  `backend/src/main/resources/db/modulemigration/recovery/` (contains `README.md`),
  `frontend/src/modules/recovery/`, `frontend/e2e/` (`platform.spec.ts`), `api/recovery-api-v4.yaml`,
  `frontend/src/api/schema.d.ts`, `AGENTS.md`, `CLAUDE.md`, `.claude/`, `aisdlc/.github/` and
  `.gitlab-ci.yml` all exist. Three patterns do not match a file today, and the spec handles each one:
  - `.gitlab/` and the validator package are created by this story.
  - `backend/src/test/resources/architecture/recovery-modules.yaml` is created by RWB-TE-001. This is
    precondition P1 (`spec.md:133`), which D-RUN-01 and D-RUN-08 permit. V9 stops the build if TE-001
    has not merged.
  - `…/demo/common/` is a reserved pattern (SPEC-004).
- **The common-module rule.** No `th/co/scb/ace/demo/common` path exists here. The spec keeps BR3 as a
  reserved pattern, listed with its basis in the reviewed register (`spec.md:331-333`). V10 warns on it
  instead of failing (`spec.md:349`), V9 still fails every other pattern that matches no file
  (`spec.md:348`), and no file is created under `common/` (`spec.md:100`). The basis is correct:
  Decision Log v10 DL05 (option B, then A); TE-001 v2 SPEC-RWB-TE-001-006 (root
  `th.co.scb.ace.demo.common`, `allowEmptyShould(true)`, D-RCV-19); OPEN-024.
- **Owners.** No person is named, and no team handle is invented. The two story handles come from
  Story Files v7 RWB-TE-002 §3 and are marked `ASSUMED` with OPEN-038. The two document-set roles from
  Engineering Practices v5 §10 ("Repository standards file (AGENTS.md)" and "Pipeline gates") carry the
  marked placeholders `@role-placeholder/…` with status `PLACEHOLDER`. The validator raises a warning
  for them (`spec.md:351`), and HV-11 requires them to be replaced before the file is used on a host.
  D-RCV-21 names a person in the register. The spec uses only the membership rule from it and does not
  copy the name. A grep of `specify/` for personal names and e-mail domains found nothing.
- **GitLab form (L-RCV-12).** The file is `.gitlab/CODEOWNERS` in section format. The GitLab
  semantics the spec relies on are stated as an assumption, not as fact (`ASM-TE002-11`,
  `assumptions.md:19`):
  - within a section, the last matching pattern wins;
  - a file matched in several sections needs one approval per section;
  - several owners on one line means either owner can approve.

  This is also why BR4 is written as two sections (SP-DG-10). SP-DG-10 is a correct new gap: the
  story's single §12 line `/.github/CODEOWNERS @a @b` could be satisfied by either team, which
  contradicts BR7 "reviewed by both teams".
- **Unit-test applicability.** Backend `YES`/`REQUIRED` with 80% line, branch, instruction and method
  on the test-scope package (`spec.md:211`). Frontend `NO`/`NOT_APPLICABLE` with evidence
  (`spec.md:210`). This agrees with the Change Scope Declaration (`spec.md:31-32`). The placement
  beside `RecoveryMigrationLintTest` is safe: `RecoveryBoundaryTest` imports with
  `DO_NOT_INCLUDE_TESTS`, and `ModulithTest` scans main classes only.
- **Traceability.** SPEC-RWB-TE-002-001 to -019 are each defined once (`spec.md:95-115`), and every
  ID in the coverage table resolves. 37 requirement rows: 7 BR, 9 AC clauses, 7 X, 7 flow steps, plus
  §12, §14, §2, §17, §19, A-05 and A-10.
- **Change classification.** `NEW_STORY`, UI NO, Logic YES, API NO, `NO_API_CHANGE`. The contracts
  record empty sets. All required spec sections and status lines are present.
- **Sources.** The cited sources were re-checked against the document set and match:
  - Story Files v7 §3, §12, §13, §16, §17;
  - Engineering Practices v5 §4.2 "Description", §7 and §10;
  - AI Assisted Development Approach v1 §3 ("with a section for the recovery module") and §6;
  - Test Cases v7 row TC-TE-002-08;
  - Story Defects v4, RWB-TE-002 defect 1 (Open);
  - Decision Log v10 DL05, DL32, DL36 and DL37.

## Findings

### REVIEW-RWB-TE-002-SG-012: the CI job and the coverage gate are reported as tested locally, with no local command that runs them

| Field | Value |
|---|---|
| Severity | Low |
| Affects | Flow 2 row (`spec.md:76`); Local implementation boundary group (a) "Proof here" (`spec.md:41`); SPEC-013, SPEC-014 (`spec.md:109-110`); HV-07 |
| Evidence | `spec.md:76` marks Flow 2 as "TESTED_LOCALLY (job and task defined; run evidence at build)". `spec.md:41` gives the proof of group (a) as "JUnit tests in `./scripts/dev.ps1 test` and the `codeowners-validation` job; 80% coverage gate (SPEC-014)". This repository has no GitLab runner (RUN-BRIEF hard rule 5), so the `.gitlab-ci.yml` job cannot run here. `scripts/dev.ps1` lines 114–116 run only `gradlew test` and `npm run check`, so `codeOwnersCoverageVerification` is not on the local path. SPEC-014 does not say which test task supplies the JaCoCo execution data for `codeOwnersCoverageReport` and `codeOwnersCoverageVerification`. `implementation-execution-gates.md` requires the coverage gate to be executed, with native report evidence. `pdlc.md` line 31 says checks outside automation must stay visible and must not be reported as passed. |
| Problem | A later stage could report "codeowners-validation passed" when no pipeline has run, and the 80% gate has no defined local command. |
| Required fix | (1) State the local proof as the command `cd backend; ./gradlew codeOwnersTest codeOwnersCoverageVerification`, the same script as the job, and either add it to `dev.ps1 test` or name it as the implementation-evidence command. (2) Set the execution data of both codeowners JaCoCo tasks to `codeOwnersTest`. (3) In the Flow 2 row and in group (a), mark the job's run inside a GitLab pipeline as `HUMAN_VERIFICATION` (extend HV-07), not `TESTED_LOCALLY`. A YAML parse of `.gitlab-ci.yml` may be added as local evidence of the job definition. |

### REVIEW-RWB-TE-002-SG-013: section names are not checked for uniqueness, so the BR4 two-section design can collapse without a validator error

| Field | Value |
|---|---|
| Severity | Low |
| Affects | BR4, BR7; SPEC-001, SPEC-005; validation rules V1–V11 (`spec.md:336-351`); field matrix (`spec.md:146`) |
| Evidence | The field matrix says section names are "Unique names … (V1)" (`spec.md:146`). V1 only checks that a line is a header or an entry (`spec.md:340`). No rule or test checks duplicate section names. BR4 relies on two separate sections, `[Code owners control ACE team]` and `[Code owners control recovery]` (`spec.md:262-271`, `ASM-TE002-11`). GitLab combines sections that share a name, and compares the names without regard to case. UT-18 (`spec.md:444`) checks only the live file as it is written today. |
| Problem | If a later edit gives both control sections the same name (in any letter case), the host would accept an approval from either team for `.gitlab/CODEOWNERS`. BR7 says both teams review. The validator would still pass. The edit itself needs both teams' approval, so this is a hardening gap, not an open bypass. |
| Required fix | Extend V1, or add V12: section names are unique, compared without regard to case (ERROR, `line {n}: duplicate section {s}`). Add a negative fixture test for it. Add a live-file assertion that every BR4 control file is matched by at least two sections whose owner sets do not overlap. |

### REVIEW-RWB-TE-002-SG-014: `backend/build.gradle.kts` now holds part of the control but is left unowned

| Field | Value |
|---|---|
| Severity | Low |
| Affects | SPEC-005, SPEC-013, SPEC-014, SPEC-017; Out of scope table (`spec.md:470`) |
| Evidence | SPEC-013 and SPEC-014 put `codeOwnersTest`, `codeOwnersCoverageReport` and `codeOwnersCoverageVerification` in `backend/build.gradle.kts` (`spec.md:109-110`, `spec.md:230`). The `codeowners-validation` job calls those tasks. `spec.md:470` lists `backend/build.gradle.kts` as "Left unowned". SG-009 asked that the files holding the control be owned, or that the spec record why they are left unowned. The spec owns `.gitlab-ci.yml`, the register and the validator package, but not the build file that defines the tasks. |
| Problem | An unreviewed change to the build file could empty `codeOwnersTest`, for example with an exclude filter, or lower the coverage minimum. The job would still pass, and no code owner would be asked to review. The reason given at `spec.md:470` ("not recovery folders") covers the local-stack files, but not the part of this file that this story adds. |
| Required fix | Either own `/backend/build.gradle.kts` in `[Pipeline gates]` (placeholder, `PLACEHOLDER`, OPEN-038) or in both control sections. Or record explicitly that the build file stays unowned and why: it is a shared ACE file reviewed in the `develop-recovery` → `develop` MR (D-RCV-50). The planner can apply either choice. |

### REVIEW-RWB-TE-002-SG-015: no local completion state for story §13 "Done when", and OPEN-038 is due "Before TE-002 build"

| Field | Value |
|---|---|
| Severity | Low |
| Affects | SPEC-018; HV-01 to HV-11; `shared-updates.md` `PROP-OI-1`, increment card row; story §13 |
| Evidence | Story Files v7 RWB-TE-002 §13: "Done when. The tests in section 16 pass and the branch rule on main shows code owner review as required". Six of the eight §16 test cases are only partly checked here, or are host-only (TC mapping, `spec.md:450-452`). `aisdlc/docs/open-items.md` line 28: OPEN-038 "Needed by: Before TE-002 build". The spec builds with OPEN-038 still open, as the orchestrator triage directs. `PROP-OI-1` (`shared-updates.md:10`) amends what OPEN-038 asks for. Its "Needed by" column says "Before TE-002 is used on the ACE host", but the row does not say that it replaces the current "Before TE-002 build". |
| Problem | Two stages could disagree here. The plan gate could block on OPEN-038's current due date, or a later stage could report RWB-TE-002 as Done when §13 is not met. |
| Required fix | (1) Add one line to SPEC-018: in this repository the story ends as "built; acceptance pending HV-01..HV-11". It is never reported as Done or accepted against story §13 until the HV items pass. (2) In `PROP-OI-1`, propose changing OPEN-038 "Needed by" to "Before TE-002 is used on the ACE host". Cite L-RCV-03 and the orchestrator triage as the reason the local build goes ahead. |

### REVIEW-RWB-TE-002-SG-016: a test input uses a real-looking migration number

| Field | Value |
|---|---|
| Severity | Low |
| Affects | UT-15 (`spec.md:441`) |
| Evidence | UT-15 uses `backend/src/main/resources/db/modulemigration/recovery/V0001__rwb_e1_001_recovery_schema.sql` as a synthetic changed path. D-RUN-07 (`AI-SDLC-BUILD-LOG.md` line 29): "No spec or plan fixes a migration number". The build log records the card's "E1-001 `V0001`" as a document gap. |
| Problem | The path is only resolver input, but it repeats the V0001 / RWB-E1-001 pairing that D-RUN-07 withdrew, and a later reader could copy it. |
| Required fix | Use a clearly synthetic name that cannot clash with a real migration, for example `V9999__rwb_te_002_fixture.sql`, or any name under the folder. The resolver only needs the folder prefix. |

## Disposition of the first review's findings (SG-001 to SG-011)

| Finding | Severity (first review) | Disposition | Evidence |
|---|---|---|---|
| SG-001 No local boundary for host-only controls | High | **Resolved** | `spec.md:34-43` (groups a/b/c); "Verification here" column `spec.md:47-88`; HC-01–HC-08 `spec.md:358-376`; HV-01–HV-11 `OPEN — NOT_TESTED_HERE` with role owner and unblock `spec.md:378-396`; SPEC-018 `spec.md:114`; `spec.md:213`; `spec.md:472` (no `main`/`develop` created, no test MRs). Wording at `spec.md:41`, `:76` refined by SG-012 (Low). |
| SG-002 Common pattern matches no file | High | **Resolved** | SPEC-004 `spec.md:100`; `reservedPatterns` with basis `spec.md:331-333`; V9/V10 `spec.md:348-349`; UT-10, UT-16, UT-17 `spec.md:436,442-443` (synthetic path, no file under `common/`); CLAR-004 `spec.md:484`; `ASM-TE002-05` `assumptions.md:13`; SP-DG-07 `document-gaps.md:22`; dependency on DL05/OPEN-024 recorded. The register is used instead of the module map `external[]`, with a valid reason (`gate-response.md:10`, `ASM-TE002-14`). |
| SG-003 GitHub format; repository stands in for GitLab | Medium | **Resolved** | `.gitlab/CODEOWNERS` in GitLab section format SPEC-001 `spec.md:97`, block `spec.md:242-282`; BR4 on `/.gitlab/CODEOWNERS` `spec.md:263,269`; GitLab protected-branch/approval/merge-check settings HC-01–HC-07 `spec.md:364-373`; `ASM-TE002-01` restated for ACE only `assumptions.md:9`; CLAR-001 "RESOLVED for this repository; ACE part in OPEN-038" `spec.md:481`. |
| SG-004 Owner existence needs a host API | Medium | **Resolved** | Owner register SPEC-009 `spec.md:105`, content `spec.md:307-334` (handle, role, source, status, openItem; no person or membership); V7 `spec.md:346`; UT-07 with `@scb-ace/recovery-leads-typo` `spec.md:433`; host check HC-08 / HV-07, fail-closed in ACE `spec.md:353-356`, `ASM-TE002-06` `assumptions.md:14`. |
| SG-005 Audit A-05 not covered or excluded | Medium | **Resolved** | Coverage row A-05 `spec.md:87`; SPEC-016 AGENTS.md §5 path fix `spec.md:112` (all five target files exist under `aisdlc/.github/contexts/`); UT-22 `spec.md:448`; SPEC-017 role-owned entries `spec.md:113`, `spec.md:273-278`; exclusions with reason and receiving owner `spec.md:468-469`; `PROP-OI-3` `shared-updates.md:12`. |
| SG-006 Audit A-10 MR template missing | Medium | **Resolved** | SPEC-015 `spec.md:111` (union of AGENTS.md §8, AI Assisted Development Approach v1 §6, Engineering Practices v5 §4.2, plus trailers); owned `spec.md:278`; UT-21 `spec.md:447`; HC-07 / HV-09 `spec.md:372,394`; SP-DG-08 `document-gaps.md:23`. |
| SG-007 SPEC IDs not defined | Medium | **Resolved** | SPEC catalogue `spec.md:90-115`, IDs 001–019 each defined once with statement, source and tests; every coverage-table ID resolves; `compliance-validation.md:25-26`. |
| SG-008 Validator tests and applicability not specified | Medium | **Resolved** | Backend `YES` / `REQUIRED`, 80% LINE/BRANCH/INSTRUCTION/METHOD on the codeowners package `spec.md:211`; SPEC-014 `spec.md:110`; failing cases per rule UT-01–UT-11 and live pass UT-12, resolver UT-13–UT-20 `spec.md:427-446`; surface named (backend test tree, `ASM-TE002-13`). Duplicate-section rule gap raised as SG-013 (Low). |
| SG-009 Control files unowned; no role basis | Low | **Resolved** | Register and host record in both control sections `spec.md:262-271`; validator package in ACE control section `spec.md:266` (`ASM-TE002-12`); `.gitlab-ci.yml` in `[Pipeline gates]` with role placeholder `spec.md:280-281`; role basis Engineering Practices v5 §10 `spec.md:113`; HV-11 `spec.md:396`. The build file that now holds the tasks is raised as SG-014 (Low). |
| SG-010 TC-TE-002-08 follows the workbook | Low | **Resolved** | TC mapping `spec.md:450-452` (follows story §16, ranks above Test Cases v7); X7 `spec.md:188`; HV-06 `spec.md:391`; SP-DG-06 `document-gaps.md:21`. Verified: Test Cases v7 row TC-TE-002-08 carries the MSG-P4-002 Then-clause and the story §16 data text side by side. |
| SG-011 Stale gate status and counts | Low | **Resolved** | Header `spec.md:7` and `spec.md:13` (`DRAFT — awaiting spec gate re-review`; v2 result does not apply, D-RUN-05); status block `spec.md:501` (`CLAR_OPEN: 0`, open items OPEN-024, OPEN-038, OPEN-041, `PROP-OI-2`; 11 HV open); `compliance-validation.md:8-9`. |

## Document gaps

The specify-stage gaps SP-DG-01 to SP-DG-10 (`specify/document-gaps.md`) were re-checked against the
sources. SP-DG-01 to SP-DG-09 match the first review's DG-01 to DG-09. SP-DG-10 is new and correct.
None is a blocker. This review adds no new document gap: SG-012 to SG-016 are spec defects, not
silences or conflicts in the document set.

## Plan inputs (not findings)

1. **Sequencing.** Build after RWB-TE-001 merges the module map (precondition P1; `ASM-TE002-14`). The
   folder `backend/src/test/resources/architecture/` is empty today, and RWB-TE-001 has no remediated
   spec yet (`output/INC-002-epic-1-RWB-TE-001/` holds `_v2-baseline` and `review` only). Confirm
   that its remediated spec keeps the D-RCV-37 path.
2. **Recovery-related files not covered by the spec's unowned list** (`spec.md:470`): 
   - `backend/src/test/java/th/co/scb/ace/demo/ModulithTest.java`, the BND-3/BND-4 check on the
     recovery nested modules;
   - `backend/src/main/resources/application*.yaml`, which holds the `rwb.*` settings;
   - `frontend/src/i18n/index.ts`, which registers the recovery namespace.

   Decide each one against BR1/BR2 and record the decision in the plan.
3. **Owner form (V8).** `@name/name` rejects nested GitLab subgroup handles (`@a/b/c`). If the ACE
   handles turn out to be nested (OPEN-038), V8 and the register change. This is not needed for the
   story's handles.
4. **SnakeYAML.** Confirm `org.yaml:snakeyaml` is on `testRuntimeClasspath` (`ASM-TE002-09`). Do not
   add a dependency (AGENTS.md §4.4).
5. **Cross-story consistency.** RWB-TE-011's spec still refers to `.github/CODEOWNERS`
   (`output/INC-006-epic-1-RWB-TE-011/specify/spec.md:65`). Under L-RCV-12 and this spec, its entry
   belongs in `.gitlab/CODEOWNERS`. The orchestrator should route this to that run.
6. **Duplicate test execution.** Tag `codeowners` runs in both `backend-unit` (`gradlew test`) and
   `codeowners-validation`. This is acceptable. The plan may exclude the tag from one task if
   pipeline time matters, but must keep a local path that runs it (SG-012).

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 5]
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
REVIEW_GATE: WARNING — Low-only (SG-012..SG-016); SG-001..SG-011 resolved; human disposition required before the Implementation Planner starts.
NEXT_STEP: Human records a disposition for SG-012..SG-016 (fix in spec or carry into the plan), then starts the Implementation Planner for RWB-TE-002, sequenced after RWB-TE-001 merges the module map (precondition P1).
```

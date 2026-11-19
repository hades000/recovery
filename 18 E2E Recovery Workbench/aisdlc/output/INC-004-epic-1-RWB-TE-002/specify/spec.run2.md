# Technical Specification — RWB-TE-002 Code owners for the recovery module

| Field | Value |
|---|---|
| Story | RWB-TE-002 — Code owners for the recovery module (Story Files v7, story file v1, 28 Oct 2026) |
| Epic / module | E1 / P2 Integration, technical enabler. Repository governance: code owners file, its validator and tests, MR template, host configuration record. No application runtime code. |
| RUN_ID | `INC-004-epic-1-RWB-TE-002` (remediation run 1 after spec gate `REVIEW-RWB-TE-002-SG-2026111701`, `FAIL` 0C/2H/6M/3L) |
| Target repository | This repository (`<repo>`), the local stand-in for the ACE GitLab project (RUN-BRIEF "Paths"; orchestrator gate triage, `AI-SDLC-BUILD-LOG.md` timeline 2026-11-17T23:21:27). Branch `develop-recovery` only. No repository host is connected (RUN-BRIEF hard rule 5). |
| Source requirement | Story Files v7, `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-002-code-owners-for-the-recovery-module-v1.md` (cited below as "story §n"); increment card `aisdlc/docs/increments/INC-004-epic-1-RWB-TE-002.md` |
| Upstream IDs | `REQ-DRI-006` (story §18); `BR-RWB-013` / `FR-RWB-013` (technical-enabler grouping only, `Traceability_Matrix.md` §6); DL04 option A, DL05, DL36, DL37 (Decision Log v10); ADR-008 (Architecture Decision Records v3); DT11 |
| Governing decisions | D-RCV-10, D-RCV-19, D-RCV-21, D-RCV-37, D-RCV-50; L-RCV-03, L-RCV-12, L-RCV-13 (`aisdlc/docs/decisions/decision-register.md`); D-RUN-01, D-RUN-05 (`AI-SDLC-BUILD-LOG.md` §1) |
| Audit items owned | A-05 and A-10 (`aisdlc/evidence/phase0-standards-audit.md`, Owner RWB-TE-002) |
| Status | `DRAFT — awaiting spec gate re-review` (`review/spec-gate-review-2.md`). The v2 result `REVIEW-RWB-TE-002-SPEC-001` does not apply to this repository (D-RUN-05). |
| Prepared | 2026-11-17, Technical Specifier (agent run) |

Assumptions `ASM-TE002-*` are in `assumptions.md`; candidate document gaps `SP-DG-*` are in
`document-gaps.md`; the finding-by-finding response to the failed gate is `gate-response.md`.

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` — no TASK/CODE history: `Traceability_Matrix.md` §3 row 004 says "build not started"; `.gitlab/` does not exist in this repository. |
| UI In Scope | `NO` — no screen, route, component, label, state or i18n key (story §15). |
| Logic In Scope | `YES` — the ownership rules BR1–BR7 as a file, its validation rules and an ownership resolver. |
| API In Scope | `NO` — no endpoint (story §14, §16). |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | `.gitlab-ci.yml` (one job added); `backend/build.gradle.kts` (test task and coverage tasks added); `AGENTS.md` §5 (paths corrected, A-05). |
| New Nodes Required | `YES` — `.gitlab/CODEOWNERS`, `.gitlab/codeowners-register.yaml`, `.gitlab/host-settings.md`, `.gitlab/merge_request_templates/Default.md`, and the test-scope package `th.co.scb.ace.demo.recovery.architecture.codeowners`. |
| Inherited Existing Behavior | Test-scope repository lint pattern of `RecoveryMigrationLintTest` (same package `recovery.architecture`); `./scripts/dev.ps1 test` runs `gradlew test` (`scripts/dev.ps1` line 114–115); CI job `backend-unit`; D-RCV-50 branch flow; the TE-001 folder layout and module map path (D-RCV-37). |
| Frontend Changes Required | `NO` — no file under `frontend/` changes. The code owners file names front-end paths; naming a path is not a front-end change. |
| Backend Changes Required | `YES` — test-scope Java only (validator, resolver, register reader, their tests) plus Gradle tasks. No main-source class, endpoint, entity or migration. |

### Local implementation boundary (D-RUN-05)

This repository has no repository host. The story's controls split into three groups. Nothing in
group (b) or (c) is claimed as tested.

| Group | What | Where specified | Proof here |
|---|---|---|---|
| (a) Built and tested here | `.gitlab/CODEOWNERS` (GitLab form, L-RCV-12); owner register; validator (rules V1–V11); ownership resolver; unit and negative tests; MR template; AGENTS.md §5 path fix; `codeowners-validation` CI job and the `dev.ps1 test` path | SPEC-001–005, -007–009, -013–017 | JUnit tests in `./scripts/dev.ps1 test` and the `codeowners-validation` job; 80% coverage gate (SPEC-014) |
| (b) Host settings, documented only | Protected branches, code-owner approval, approval count, author approval ignored, approvals removed on a new commit, pipelines must succeed, default MR template, owner existence and write access | SPEC-006, -010, -011, -012; configuration record HC-01–HC-08 in `.gitlab/host-settings.md` | None here. The ACE team repository administrator applies it (story §3, §4 step 3). |
| (c) Human verification, visible and open | Every acceptance clause that only a host can show | SPEC-018; HV-01–HV-11 | `NOT_TESTED_HERE`. Open until run on the ACE host (OPEN-038 and proposed open item `PROP-OI-2`, `shared-updates.md`). |

## Requirement-to-SPEC Logic Coverage

`Status` = specified. `Verification here` says how this repository proves it: `TESTED_LOCALLY`,
`HOST_CONFIG_DOCUMENTED`, or `HUMAN_VERIFICATION` (open, never reported as passed).

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Verification here | Status |
|---|---|---|---|---|---|---|
| BR1 | Recovery back end, test and migration folders owned by the TechX recovery tech leads | SPEC-002 | DIRECT | Paths of this repository (SPEC-002 table). Team membership per D-RCV-21. | TESTED_LOCALLY (UT-13, UT-14) | COVERED |
| BR2 | Recovery front end folder and module map owned by the TechX recovery tech leads | SPEC-003 | DIRECT | `frontend/src/modules/recovery/`; module map per D-RCV-37. | TESTED_LOCALLY (UT-15) | COVERED |
| BR3 | Common module folder owned by the ACE team | SPEC-004 | DIRECT | Reserved pattern: the folder does not exist here (DL05, OPEN-024). | TESTED_LOCALLY (UT-10, UT-16) | COVERED |
| BR4 | The code owners file is owned by both teams | SPEC-005 | DIRECT | Two sections, one per team, so both must approve (ASM-TE002-11). | TESTED_LOCALLY (UT-18); host effect HUMAN_VERIFICATION (HV-08) | COVERED |
| BR5 | Last matching pattern decides; specific after general | SPEC-001, -007, -008 | DIRECT | Resolver applies last match per section; validator V6 fails a shadowed pattern. | TESTED_LOCALLY (UT-06, UT-19) | COVERED |
| BR6 | Merge to main needs one code-owner approval per changed path; author approval does not count; new commit dismisses | SPEC-006, -010, -011, -012 | DIRECT | Host settings HC-01–HC-05. | HOST_CONFIG_DOCUMENTED; HUMAN_VERIFICATION (HV-01, HV-03, HV-04, HV-05) | COVERED |
| BR7 | Team names are values in the file; a team change is a file change reviewed by both teams | SPEC-005, -009 | DIRECT | Handles live in the file and the register; both are owned by both teams. | TESTED_LOCALLY (UT-18) | COVERED |
| AC1 (clause 1) | A recovery change requires a TechX tech lead | SPEC-002, -007 | DIRECT | Resolver on the story's path mapped to this repository. | TESTED_LOCALLY (UT-13) | COVERED |
| AC1 (clause 2) | An outside squad member's approval leaves the merge blocked | SPEC-006, -018 | DIRECT | Host only. | HUMAN_VERIFICATION (HV-01) | COVERED |
| AC2 | A common module change needs `@scb-ace/ace-team` | SPEC-004, -007 | DIRECT | Synthetic changed path; no file created under `common/`. | TESTED_LOCALLY (UT-16); host display HV-02 | COVERED |
| AC3 (required) | A change across both modules requires both teams | SPEC-007 | DIRECT | Resolver returns both sections. | TESTED_LOCALLY (UT-17) | COVERED |
| AC3 (blocked) | Merge stays blocked until the ACE team also approves | SPEC-006, -018 | DIRECT | Host only. | HUMAN_VERIFICATION (HV-03) | COVERED |
| AC4 | Front end, migrations and module map require the recovery team | SPEC-003, -007 | DIRECT | Three synthetic changed paths. | TESTED_LOCALLY (UT-15) | COVERED |
| AC5 | An author cannot approve their own change | SPEC-010, -018 | DIRECT | HC-04. | HUMAN_VERIFICATION (HV-04) | COVERED |
| AC6 | A new commit needs a new approval | SPEC-011, -018 | DIRECT | HC-05. | HUMAN_VERIFICATION (HV-05) | COVERED |
| AC7 | An owner that does not exist fails the check and is named | SPEC-008, -009, -013 | DIRECT | Local existence = listed in the register (SPEC-009). Host existence and write access: HC-08. | TESTED_LOCALLY (UT-07); host part HUMAN_VERIFICATION (HV-07) | COVERED |
| X1 | Only a non-owner approves a recovery change → blocked | SPEC-006, -018 | DIRECT | As AC1 clause 2. | HUMAN_VERIFICATION (HV-01) | COVERED |
| X2 | Common module change → ACE team required | SPEC-004, -007 | DIRECT | As AC2. | TESTED_LOCALLY (UT-16) | COVERED |
| X3 | Both modules → both teams approve | SPEC-007, -018 | DIRECT | As AC3. | TESTED_LOCALLY (UT-17) + HUMAN_VERIFICATION (HV-03) | COVERED |
| X4 | Author's own approval does not count | SPEC-010, -018 | DIRECT | As AC5. | HUMAN_VERIFICATION (HV-04) | COVERED |
| X5 | New commit dismisses approval | SPEC-011, -018 | DIRECT | As AC6. | HUMAN_VERIFICATION (HV-05) | COVERED |
| X6 | Owner that does not exist fails the build, `owner {team} not found` | SPEC-008, -013 | DIRECT | Message text from story §14. | TESTED_LOCALLY (UT-07); host part HV-07 | COVERED |
| X7 / TC-TE-002-08 | Non-owner squad member cannot satisfy the review | SPEC-018 | DIRECT | Follows story §16, not Test Cases v7 row text (SP-DG-06). | HUMAN_VERIFICATION (HV-06) | COVERED |
| Flow 1 | Write the code owners file, most specific last | SPEC-001–005, -017 | DIRECT | `.gitlab/CODEOWNERS` (L-RCV-12). | TESTED_LOCALLY (UT-12) | COVERED |
| Flow 2 | Add the validation step to the pipeline | SPEC-013 | DIRECT | `codeowners-validation` job; also in `dev.ps1 test`. | TESTED_LOCALLY (job and task defined; run evidence at build) | COVERED |
| Flow 3 | Administrator sets the branch rule | SPEC-006, -010, -011, -012 | DIRECT | HC-01–HC-06. | HOST_CONFIG_DOCUMENTED; HUMAN_VERIFICATION (HV-01–HV-05) | COVERED |
| Flow 4 | Developer opens an MR on a recovery folder | SPEC-018 | DIRECT | Host only. | HUMAN_VERIFICATION (HV-02) | COVERED |
| Flow 5 | Host requests the owning team per changed path | SPEC-007, -018 | DIRECT | Resolver computes the same set locally. | TESTED_LOCALLY (UT-13–UT-18) + HUMAN_VERIFICATION (HV-02) | COVERED |
| Flow 6 | Pipeline runs validation; missing owner or no-match path fails | SPEC-008, -013 | DIRECT | V7, V9. | TESTED_LOCALLY (UT-07, UT-09) | COVERED |
| Flow 7 | Merge allowed once every owning team approved | SPEC-006, -018 | DIRECT | Host only. | HUMAN_VERIFICATION (HV-03) | COVERED |
| §12 Contract | File, entries, branch rule, pipeline step, trigger, idempotency | SPEC-001–013 | DIRECT | File path per L-RCV-12; paths per SPEC-002–005; idempotency UT-20. | Mixed, as rows above | COVERED |
| §14 Messages | `Review required from code owners` (host); `owner {team} not found` (build log) | SPEC-008, -018 | DIRECT | Host text is the host's; build text is exact. | TESTED_LOCALLY (UT-07); host text HV-01 | COVERED |
| §2 Measure | 100% of merged recovery MRs approved by a code owner | SPEC-018 | DIRECT | Needs host MR history. | HUMAN_VERIFICATION (HV-10) | COVERED |
| §17 Guardrails | No business value; no personal data; review control for TE-001 boundary; teams, never people | SPEC-001, -008 (V8), -009 | DIRECT | V8 rejects an owner that is not a team. | TESTED_LOCALLY (UT-08) | COVERED |
| §19 Out of scope | TE-001 boundary test; collection code owners; TE-010 browser runner | SPEC-019 | DIRECT | Not built. | n/a | COVERED |
| A-05 | AGENTS.md §5 paths do not resolve; no package AGENTS.md; no coding-standard file | SPEC-016, -017, -019 | DIRECT | Paths corrected and tested; AGENTS.md owned; two parts excluded with reason. | TESTED_LOCALLY (UT-22) | COVERED |
| A-10 | No CODEOWNERS and no MR template | SPEC-001, -015 | DIRECT | MR template fields = union of AGENTS.md §8 and Engineering Practices v5 §4.2. | TESTED_LOCALLY (UT-21); default-template setting HV-09 | COVERED |

## SPEC catalogue

IDs 001–012 keep the subject the v2 coverage table gave them; 013–019 are new. Every ID is defined
once here.

| SPEC ID | Statement | Source | Tests / verification |
|---|---|---|---|
| SPEC-RWB-TE-002-001 | **Code owners file.** `.gitlab/CODEOWNERS` in GitLab section format. Grammar: blank lines and `#` comments; section header `[Name]` alone on a line (no `^` optional prefix, no `[n]` approval count, no default owners); entry `pattern owner…` inside a section. Patterns are anchored (`/` first), name a directory (trailing `/`, covers everything below) or one file, and contain no `*`, `?`, `[`, `!` or `\`. Within a section, general patterns come before specific ones. Content is exactly the block in "Code owners file" below. | Story §4 step 1, §12, BR5; L-RCV-12; SG-003 | UT-01–UT-06, UT-12 |
| SPEC-RWB-TE-002-002 | **Recovery back-end entries (BR1)** owned by `@scb-ace/techx-recovery-tech-leads`: recovery main package, recovery test package, recovery e2e test package, recovery migration folder. | BR1; D-RCV-21; RUN-BRIEF local stack facts; ASM-TE002-02, -08 | UT-13, UT-14 |
| SPEC-RWB-TE-002-003 | **Recovery front end, module map and recovery contract (BR2)** owned by `@scb-ace/techx-recovery-tech-leads`: `frontend/src/modules/recovery/`, `frontend/e2e/`, the module map, `api/recovery-api-v4.yaml`, `frontend/src/api/schema.d.ts`. | BR2; D-RCV-10; D-RCV-37; RUN-BRIEF; ASM-TE002-08 | UT-15 |
| SPEC-RWB-TE-002-004 | **Common module entry (BR3), reserved.** `/backend/src/main/java/th/co/scb/ace/demo/common/` owned by `@scb-ace/ace-team`, listed in the register's `reservedPatterns`. The validator warns, and does not fail, while it matches no file. No file is created under `common/`. | BR3; DL05; TE-001 v2 SPEC-RWB-TE-001-006 (root `th.co.scb.ace.demo.common`, D-RCV-19); OPEN-024; SG-002; ASM-TE002-05 | UT-10, UT-16 |
| SPEC-RWB-TE-002-005 | **Control files owned by both teams (BR4, BR7).** `.gitlab/CODEOWNERS`, `.gitlab/codeowners-register.yaml` and `.gitlab/host-settings.md` appear in section `[Code owners control ACE team]` (owner `@scb-ace/ace-team`) and in section `[Code owners control recovery]` (owner `@scb-ace/techx-recovery-tech-leads`). The validator package is also in the ACE control section; the recovery section already owns it through the recovery test package. | BR4, BR7; L-RCV-13; ASM-TE002-07, -11, -12; SG-009 | UT-18; HV-08 |
| SPEC-RWB-TE-002-006 | **Host: code-owner approval and merge blocking (BR6), documented only.** HC-02 code-owner approval required, HC-03 one approval, HC-06 pipelines must succeed, on the branches of SPEC-012. | BR6; ADR-008; DT11; story §12; L-RCV-12 | HV-01, HV-03, HV-07 |
| SPEC-RWB-TE-002-007 | **Ownership resolver.** Pure function: input = parsed file + set of changed repository-relative paths; output = for each section with at least one matching entry, the owners of the **last** matching entry in that section. A path is matched by a directory pattern when it starts with the pattern without its leading `/`, and by a file pattern when it is equal to it. Every returned section needs one approval from one of its owners (ASM-TE002-11). A path with no match returns no section. Same input → same output. | BR5; story §4 step 5, §12 idempotency; SG-001 | UT-13–UT-20 |
| SPEC-RWB-TE-002-008 | **Validator.** Runs rules V1–V11 (table "Validation rules") over the live file and register, collects every finding, and fails when any finding is `ERROR`. `WARNING` and `INFO` findings are printed and do not fail. Output names line, pattern and owner. It prints no token: none is used. | Story §4 step 6, §12 pipeline step, §14; SG-004, SG-008 | UT-01–UT-12 |
| SPEC-RWB-TE-002-009 | **Owner register** `.gitlab/codeowners-register.yaml`: the only local source of valid owners. Each owner: `handle`, `role` (document-set role), `source`, `status` ∈ {`ASSUMED`, `PLACEHOLDER`, `CONFIRMED`}, `openItem`. Plus `reservedPatterns`: `pattern`, `basis`. No person, no membership, no e-mail. Content is exactly the block in "Owner register" below. | BR7; story §3 (handles "assumed until DL37 and DL36"); SG-004; ASM-TE002-03 | UT-07, UT-11 |
| SPEC-RWB-TE-002-010 | **Host: author approval does not count (AC5), documented only.** HC-04. | BR6; AC5; X4 | HV-04 |
| SPEC-RWB-TE-002-011 | **Host: a new commit removes approvals (AC6), documented only.** HC-05. | BR6; AC6; X5 | HV-05 |
| SPEC-RWB-TE-002-012 | **Host: protected branches `main`, `develop-recovery`, `develop`, documented only.** HC-01. Only `develop-recovery` exists locally; no branch is created for testing. | L-RCV-13; D-RCV-50; story §12; SG-001 | HV-01–HV-05 |
| SPEC-RWB-TE-002-013 | **Pipeline step.** (1) JUnit tag `codeowners` on every test class in the codeowners package; they run in `gradlew test`, hence in `./scripts/dev.ps1 test` and CI job `backend-unit`. (2) Gradle task `codeOwnersTest` (Test, `includeTags("codeowners")`), finalized by `codeOwnersCoverageReport`. (3) New `.gitlab-ci.yml` job `codeowners-validation`, stage `verify`, image `eclipse-temurin:21-jdk`, gradle cache as `backend-unit`, script `cd backend && ./gradlew --no-daemon codeOwnersTest codeOwnersCoverageVerification`, no `rules:` (runs on every pipeline, story §12 trigger), JUnit report `backend/build/test-results/codeOwnersTest/*.xml`. Repository root = parent of the Gradle project directory. | Story §4 steps 2 and 6, §12 trigger; SG-001; `.gitlab-ci.yml` existing jobs | Build evidence (implementation stage) |
| SPEC-RWB-TE-002-014 | **Tests and coverage gate.** Unit tests UT-01–UT-22 (table "Test scenarios"), positive and negative per rule, against fixture files in `@TempDir` plus the live files. JaCoCo tasks `codeOwnersCoverageReport` and `codeOwnersCoverageVerification` over test-output classes in `th/co/scb/ace/demo/recovery/architecture/codeowners/**`, excluding `**/*Test.class`, with minimum 0.80 for LINE, BRANCH, INSTRUCTION and METHOD. `recoveryCoverageReport`/`Verification` are not changed. | security-quality-standards.md (positive and negative tests); implementation-execution-gates.md; testing-standards §3 (enabler: one test per rule and test case), §6 (test-scope tooling coverage precedent); BS-7.2; SG-008 | Implementation unit-test evidence |
| SPEC-RWB-TE-002-015 | **MR template** `.gitlab/merge_request_templates/Default.md` with headings, in this order: `Story key`, `Plan file`, `Acceptance criteria covered`, `Coding tool used`, `AI first-pass review summary`, `Reviewer`, `Test results`, `AISDLC trailers` (the commit trailers `AISDLC-Run` and `AISDLC-Plan`). Each heading is followed by an empty line for the author. The `Reviewer` section says the reviewer is named on the MR by the host's approval record; the template holds no person. | AGENTS.md §8; AI Assisted Development Approach v1 §6; Engineering Practices v5 §4.2 "Description"; CLAUDE.md (commit trailers); A-10; SG-006; SP-DG-08 | UT-21; HV-09 |
| SPEC-RWB-TE-002-016 | **AGENTS.md §5 path fix (A-05).** In the §5 table, replace `.github/contexts/` with `aisdlc/.github/contexts/` in the five path cells, and write the coding-standard cell as `` `aisdlc/.github/contexts/backend-standards.md` / `aisdlc/.github/contexts/frontend-standards.md` ``. No other AGENTS.md text changes. | phase0 audit A-05; RUN-BRIEF "Paths" (coding standard mapping); AI Assisted Development Approach v1 §3 (standards file changes by pull request); SG-005 | UT-22 |
| SPEC-RWB-TE-002-017 | **Role-owned governance entries with placeholders.** Section `[Repository standards]`: `/AGENTS.md`, `/CLAUDE.md`, `/.claude/`, `/aisdlc/.github/`, `/.gitlab/merge_request_templates/` owned by `@role-placeholder/solution-architect-with-tech-leads`. Section `[Pipeline gates]`: `/.gitlab-ci.yml` owned by `@role-placeholder/techx-devops-with-scb-it`. Both handles are `PLACEHOLDER` in the register, tied to OPEN-038 (amendment `PROP-OI-1`). They are not team handles and must be replaced before the file is used on a host (HV-11). | Engineering Practices v5 §10 ("Repository standards file (AGENTS.md)": solution architect with the tech leads; "Pipeline gates": TechX DevOps with SCB IT); AGENTS.md header "Owner"; SG-005, SG-009; SP-DG-09 | UT-11, UT-12; HV-11 |
| SPEC-RWB-TE-002-018 | **Human-verification items HV-01–HV-11** (table below). Each is `OPEN — NOT_TESTED_HERE` until a person runs it on the ACE host after HC-01–HC-08 are applied, and records the MR link and result. No stage may report an HV item as passed from local evidence. | pdlc.md (acceptance checks outside automation stay visible as human-verification gaps); SG-001 | — |
| SPEC-RWB-TE-002-019 | **Scope exclusions** (section "Out of scope"). | Story §19; A-05; SG-005 | — |

## User story intent interpretation

As a **squad member (RW-TRIBE)**, I want **a code owners entry that maps every recovery folder to the
TechX tech leads and the common module to the ACE team, with review by a code owner required before
merge**, so that **every change in the recovery module is reviewed by its owners** (story §1).

The story is a repository-governance enabler with no application behaviour. In this repository it
delivers the file, the proof that the file is well-formed and means what the story says (validator and
resolver), and a configuration record for the host. The merge-blocking itself is host behaviour and is
carried as human verification (Local implementation boundary).

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Every pipeline (every MR, every new commit) runs `codeowners-validation` and `backend-unit`; locally every `./scripts/dev.ps1 test` (story §12 "Every pull request that changes any file"). |
| Precondition P1 | RWB-TE-001 has merged the module map `backend/src/test/resources/architecture/recovery-modules.yaml` into `develop-recovery` (story §3; Build Sequence v6 order 2 before order 4; D-RUN-01). Today the folder is empty, so V9 would fail on that entry. The plan must sequence the build after TE-001; it must not reserve or drop the entry. |
| Precondition P2 | SnakeYAML is on the test runtime classpath through the existing Spring Boot starters (ASM-TE002-09). The plan confirms this with `gradlew dependencies`; no dependency is added (AGENTS.md §4.4, BS-1.5). |
| Host preconditions | Not needed to build here. Needed for HV items: the ACE GitLab project, the tier that offers code-owner approval, the groups for both handles, and HC-01–HC-08 applied (OPEN-038). |
| Input | `.gitlab/CODEOWNERS`, `.gitlab/codeowners-register.yaml`, the working tree (for V9), and for the resolver a list of changed paths. |
| Output | Validator findings (pass/fail); resolver result (required sections and owners). |
| Feature flag | None. A file and a test have no runtime path (story §13 "Feature flag"). |

## Field-level behaviour matrix

The story reads and writes no business field (story §11). The rule tables are the data.

| Artefact | Field | Source | Who may change | Constraint |
|---|---|---|---|---|
| CODEOWNERS | Section `[Name]` | This spec | MR approved per SPEC-005 | Unique names; header alone on the line (V1). |
| CODEOWNERS | Pattern | SPEC-002–005, -017 | Same | Anchored, no wildcard (V4); not duplicated or shadowed in its section (V5, V6); matches a file unless reserved (V9, V10). |
| CODEOWNERS | Owner | Register | Same | `@group/name` form, never a single user or e-mail (V8, story §17); listed in the register (V7). |
| CODEOWNERS | Comment | Free text | Same | No business value, no personal data, no credential (story §17). |
| Register | `handle`, `role`, `source`, `status`, `openItem` | SPEC-009 | Same (owned by both teams) | `status` in {`ASSUMED`, `PLACEHOLDER`, `CONFIRMED`}; all fields present (V11). |
| Register | `reservedPatterns[].pattern`, `.basis` | SPEC-004 | Same | Basis cites a source. |
| Host settings record | HC rows | SPEC-006, -010–-012 | Same; applied by the ACE team repository administrator (story §10) | Values as in "Host configuration record". |
| MR template | Headings | SPEC-015 | MR approved per `[Repository standards]` | All eight headings present (UT-21). |

## Status-transition matrix

No case status changes (story §9). Two state sets exist.

Local validation (built here):

| From | Event | Condition | To | Side effect |
|---|---|---|---|---|
| Not run | Pipeline or `dev.ps1 test` starts | — | Running | — |
| Running | Validation ends | No `ERROR` finding | Passed | Warnings and infos printed. |
| Running | Validation ends | One or more `ERROR` findings | Failed | Every finding printed; test and job fail. |

Host MR review state (host only, HV items; story §9):

| From | Event | Condition | To |
|---|---|---|---|
| Open | MR created | A changed path matches a section | Review required for each matched section |
| Review required | Approval | Approver is an owner of that section and not the author | Section approved |
| Review required | Approval | Approver outside the section, or the author | Review required (not counted) |
| Section approved | New commit | HC-05 on | Review required |
| Any | Pipeline fails | HC-06 on | Merge blocked |
| All sections approved and pipeline passed | Merge | — | Merged |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message | Here |
|---|---|---|---|---|
| X1 | Only a non-owner approves a recovery MR | Merge stays blocked | Host: review required from code owners | HV-01 |
| X2 | MR changes the common module | ACE team section required | Host: review required from code owners | UT-16; HV-02 |
| X3 | MR changes recovery and common | Both sections required | Host: review required from code owners | UT-17; HV-03 |
| X4 | Author approves own MR | Not counted | Host: review required from code owners | HV-04 |
| X5 | New commit after approval | Approvals removed | Host: review required from code owners | HV-05 |
| X6 | File names an owner not in the register | Validation fails | `line {n}: owner {team} not found` | UT-07; host part HV-07 |
| X7 | Non-owner tries to satisfy review | Merge refused; no Workbench endpoint, so MSG-P4-002 is not shown (story §16) | Host: review required from code owners | HV-06 |
| X8 (derived) | Register file missing or malformed | Validation fails closed | `register: {problem}` | UT-11 |
| X9 (derived) | Code owners file missing | Validation fails closed | `.gitlab/CODEOWNERS not found` | UT-01 |

X8 and X9 are derived from story §12 ("syntax") so the step never passes on a missing input; they add
no business rule.

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Endpoints delivered | None. `contracts/backend-apis.json` and `contracts/frontend-integrations.json` record the empty sets. |
| Contract delta | None. `api/recovery-api-v4.yaml` gains an owner, not a change. |
| Backward compatibility | Not applicable. |
| Authorization | Repository right, not a Workbench capability area (story §10). |
| Versioning | None. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No file under `frontend/` is added or changed. The code owners file only names `frontend/` paths. Existing `npm run check` (Vitest 80% on `src/modules/recovery/**`) stays green. | Existing frontend checks pass unchanged. |
| Backend | YES | REQUIRED | 80% LINE, BRANCH, INSTRUCTION (statements) and METHOD (functions) on the test-scope package `th.co.scb.ace.demo.recovery.architecture.codeowners`, `*Test` classes excluded, via `codeOwnersCoverageVerification` (SPEC-014). `recoveryCoverageVerification` unchanged: no main-source change. | BR1–BR7, AC1–AC4, AC7, X2, X3, X6; SPEC-001–005, -007–009, -013–017 | Validator, resolver and register reader are new hand-written logic in the backend Gradle test tree, as `RecoveryMigrationLintTest` is. Testing-standards §6 already measures test-scope tooling for TE-001. | UT-01–UT-22 pass; every V-rule has a passing and a failing case; coverage report XML and HTML saved as implementation evidence. |

Host-only clauses are not unit-testable and are not replaced by unit tests: they stay HV-01–HV-11.

## Detailed design

### Components

| Component | Type | Location | Responsibility |
|---|---|---|---|
| Code owners file | Rule table | `.gitlab/CODEOWNERS` | Path → section → owners (SPEC-001–005, -017). |
| Owner register | Reference data | `.gitlab/codeowners-register.yaml` | Valid owners with role and status; reserved patterns (SPEC-009). |
| Host configuration record | Document | `.gitlab/host-settings.md` | HC-01–HC-08 for the ACE administrator, each with its HV item (SPEC-006, -010–-012). |
| MR template | Template | `.gitlab/merge_request_templates/Default.md` | AGENTS.md §8 fields (SPEC-015). |
| `CodeOwnersFile` | Test-scope class | `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/codeowners/` | Parse the file into sections and entries with line numbers. |
| `OwnerRegister` | Test-scope class | Same | Read the register (SnakeYAML). |
| `CodeOwnersValidator` | Test-scope class | Same | Rules V1–V11; returns findings. |
| `OwnershipResolver` | Test-scope class | Same | SPEC-007. |
| `CodeOwnersValidationTest`, `OwnershipResolverTest`, `MergeRequestTemplateTest`, `AgentsContextPathsTest` | JUnit 5 tests, tag `codeowners` | Same | UT-01–UT-22. |
| Gradle tasks | Build | `backend/build.gradle.kts` | `codeOwnersTest`, `codeOwnersCoverageReport`, `codeOwnersCoverageVerification` (SPEC-013, -014). |
| CI job | Pipeline | `.gitlab-ci.yml` | `codeowners-validation` (SPEC-013). |

Class names are the specifier's proposal; the planner may rename them inside the same package. The
package sits beside the existing `RecoveryMigrationLintTest` and `RecoveryBoundaryTest`. The planner
checks that the existing architecture tests import main classes only, so these test classes are not
scanned as recovery module code.

### Code owners file

Exact content of `.gitlab/CODEOWNERS`:

```text
# RWB-TE-002 code owners, GitLab format (L-RCV-12). Paths and owner handles only.
# Owner handles and their status are in .gitlab/codeowners-register.yaml (OPEN-038).
# Within a section the last matching pattern wins (BR5): general paths first, specific paths last.
# A file matched in several sections needs one approval from each of those sections.

[Common module]
/backend/src/main/java/th/co/scb/ace/demo/common/ @scb-ace/ace-team

[Recovery module]
/backend/src/main/java/th/co/scb/ace/demo/recovery/ @scb-ace/techx-recovery-tech-leads
/backend/src/test/java/th/co/scb/ace/demo/recovery/ @scb-ace/techx-recovery-tech-leads
/backend/src/test/java/th/co/scb/ace/demo/e2e/ @scb-ace/techx-recovery-tech-leads
/backend/src/main/resources/db/modulemigration/recovery/ @scb-ace/techx-recovery-tech-leads
/backend/src/test/resources/architecture/recovery-modules.yaml @scb-ace/techx-recovery-tech-leads
/frontend/src/modules/recovery/ @scb-ace/techx-recovery-tech-leads
/frontend/e2e/ @scb-ace/techx-recovery-tech-leads
/api/recovery-api-v4.yaml @scb-ace/techx-recovery-tech-leads
/frontend/src/api/schema.d.ts @scb-ace/techx-recovery-tech-leads

[Code owners control ACE team]
/.gitlab/CODEOWNERS @scb-ace/ace-team
/.gitlab/codeowners-register.yaml @scb-ace/ace-team
/.gitlab/host-settings.md @scb-ace/ace-team
/backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/codeowners/ @scb-ace/ace-team

[Code owners control recovery]
/.gitlab/CODEOWNERS @scb-ace/techx-recovery-tech-leads
/.gitlab/codeowners-register.yaml @scb-ace/techx-recovery-tech-leads
/.gitlab/host-settings.md @scb-ace/techx-recovery-tech-leads

[Repository standards]
/AGENTS.md @role-placeholder/solution-architect-with-tech-leads
/CLAUDE.md @role-placeholder/solution-architect-with-tech-leads
/.claude/ @role-placeholder/solution-architect-with-tech-leads
/aisdlc/.github/ @role-placeholder/solution-architect-with-tech-leads
/.gitlab/merge_request_templates/ @role-placeholder/solution-architect-with-tech-leads

[Pipeline gates]
/.gitlab-ci.yml @role-placeholder/techx-devops-with-scb-it
```

Path basis, checked against this repository on 2026-11-17 (directory listing):

| Pattern | Exists today | Basis |
|---|---|---|
| `…/demo/common/` | No — reserved (SPEC-004) | Story BR3; DL05; TE-001 v2 SPEC-006; OPEN-024 |
| `…/demo/recovery/` (main, test) | Yes | BR1; RUN-BRIEF package `th.co.scb.ace.demo.recovery` |
| `…/demo/e2e/` (test) | Yes (`PlatformE2ETest.java`, tests `/api/recovery/v1`) | BR1 "test"; ASM-TE002-08 |
| `…/db/modulemigration/recovery/` | Yes (`README.md`; no migration yet) | BR1 "migration"; RUN-BRIEF; story path `db/migration/recovery/` replaced (SP-DG-02) |
| `…/architecture/recovery-modules.yaml` | No — created by RWB-TE-001 (precondition P1) | BR2; D-RCV-37 |
| `frontend/src/modules/recovery/` | Yes | BR2; D-RCV-10 |
| `frontend/e2e/` | Yes (`platform.spec.ts`, recovery journey) | BR2; ASM-TE002-08 |
| `api/recovery-api-v4.yaml`, `frontend/src/api/schema.d.ts` | Yes | RUN-BRIEF (types generated from the contract); ASM-TE002-08 |
| `.gitlab/*` files, validator package | Created by this story | SPEC-005, -009, -015 |
| `AGENTS.md`, `CLAUDE.md`, `.claude/`, `aisdlc/.github/`, `.gitlab-ci.yml` | Yes | SPEC-017 |

The story's `ace-service/…`, `ace-web/…`, `db/migration/recovery/` and `/architecture/…` paths are
replaced by the paths above (ASM-TE002-02). The story's single line `/.github/CODEOWNERS @a @b` becomes
two sections because one line with two owners can be approved by either team (ASM-TE002-11, SP-DG-10).

### Owner register

Exact content of `.gitlab/codeowners-register.yaml`:

```yaml
# Owner register for .gitlab/CODEOWNERS (RWB-TE-002). The local source of valid owners.
# No person, no membership, no e-mail. A handle changes only by an MR approved by both teams (BR7).
owners:
  - handle: "@scb-ace/techx-recovery-tech-leads"
    role: "TechX recovery tech leads (recovery tech lead plus the squad developers, D-RCV-21)"
    source: "Story Files v7, RWB-TE-002 section 3"
    status: ASSUMED
    openItem: OPEN-038
  - handle: "@scb-ace/ace-team"
    role: "ACE team"
    source: "Story Files v7, RWB-TE-002 section 3"
    status: ASSUMED
    openItem: OPEN-038
  - handle: "@role-placeholder/solution-architect-with-tech-leads"
    role: "Repository standards file owner: solution architect with the tech leads"
    source: "Engineering Practices v5 section 10; AI Assisted Development Approach v1 section 3"
    status: PLACEHOLDER
    openItem: OPEN-038
  - handle: "@role-placeholder/techx-devops-with-scb-it"
    role: "Pipeline gates owner: TechX DevOps with SCB IT"
    source: "Engineering Practices v5 section 10"
    status: PLACEHOLDER
    openItem: OPEN-038
reservedPatterns:
  - pattern: "/backend/src/main/java/th/co/scb/ace/demo/common/"
    basis: "BR3; DL05; RWB-TE-001 common root th.co.scb.ace.demo.common; OPEN-024"
```

### Validation rules

| Rule | Check | Level | Message (exact; `{…}` filled) |
|---|---|---|---|
| V1 | Each non-blank, non-comment line is a section header `[Name]` or an entry `pattern owner…` | ERROR | `line {n}: syntax error` |
| V2 | Every entry is inside a section | ERROR | `line {n}: entry outside a section` |
| V3 | Every entry has at least one owner | ERROR | `line {n}: pattern {p} has no owner` |
| V4 | Pattern starts with `/` and has no `*`, `?`, `[`, `!`, `\` | ERROR | `line {n}: unsupported pattern {p}` |
| V5 | No pattern twice in one section | ERROR | `line {n}: duplicate pattern {p} in section {s}` |
| V6 | No pattern is fully covered by a later directory pattern in the same section (BR5) | ERROR | `line {n}: pattern {p} is shadowed by later pattern {q} in section {s}` |
| V7 | Every owner is listed in the register (AC7) | ERROR | `line {n}: owner {team} not found` |
| V8 | Every owner has the form `@name/name` (a group), never `@user` or an e-mail (story §17) | ERROR | `line {n}: owner {o} is not a team` |
| V9 | Every non-reserved pattern matches a file: the path is a regular file, or a directory with at least one regular file below it (story §12) | ERROR | `line {n}: pattern {p} matches no file` |
| V10 | A reserved pattern that matches no file | WARNING | `line {n}: reserved pattern {p} matches no file ({basis})` |
| V11 | Register well-formed: file present, every owner has all five fields, `status` valid, handles unique | ERROR | `register: {problem}` |
| — | Owner with status `PLACEHOLDER` / `ASSUMED` | WARNING / INFO | `owner {o} is a placeholder for {role} ({openItem})` / `owner {o} is assumed ({openItem})` |

V9 uses the working tree. In CI the checkout holds the tracked files only, so it equals "matches a
tracked file". The host check "every owner exists and has write access" (story §12) is not run here:
it needs a host API and token (SG-004). It is HC-08 and HV-07, and when it is built in ACE it must fail
closed if its token is absent (ASM-TE002-06).

### Host configuration record

`.gitlab/host-settings.md` holds this table for the ACE team repository administrator. GitLab setting
names are the specifier's mapping of story §12 under L-RCV-12 (ASM-TE002-10); the administrator
confirms each on the target tier (OPEN-038).

| ID | GitLab setting | Value | Branches | Source | Verified by |
|---|---|---|---|---|---|
| HC-01 | Repository > Protected branches: allowed to push and merge | No one (changes arrive by MR) | `main`, `develop-recovery`, `develop` | Story §12 "Require a pull request"; L-RCV-13 | HV-01 |
| HC-02 | Protected branch: code owner approval required | On | Same | Story §12 "require review from code owners"; BR6 | HV-01, HV-03 |
| HC-03 | Merge request approvals: required approvals | 1 | Same | Story §12 "1 approval" | HV-01 |
| HC-04 | Approval settings: prevent approval by author | On | Project | Story §12 "the author's approval does not count"; AC5 | HV-04 |
| HC-05 | Approval settings: when a commit is added, remove all approvals | On | Project | Story §12 "dismiss stale approvals"; AC6 | HV-05 |
| HC-06 | Merge checks: pipelines must succeed | On | Project | Story §4 step 6 (a failed check blocks); Engineering Practices v5 §7 gates block merge | HV-07 |
| HC-07 | Default MR description template | `Default` | Project | SPEC-015; A-10 | HV-09 |
| HC-08 | Groups for every `ASSUMED` handle exist with at least write (Developer) access to the project; `PLACEHOLDER` handles replaced first | Per register | Project | Story §12 "every owner exists and has write access"; §3 | HV-07, HV-11 |

"Allowed to merge" roles are not set by this story: D-RCV-50 and Engineering Practices v5 §4.2 decide
who merges; the administrator applies them.

### Human-verification items (open; not tested here)

Owner of every item: ACE team repository administrator with the recovery tech lead (story §3, §4 step 3;
D-RCV-50). Unblock: OPEN-038 answered and HC-01–HC-08 applied; tracked by proposed open item
`PROP-OI-2`. Test MRs change fixture files only and are closed unmerged (story §17).

| ID | Covers | Steps on the ACE host | Expected | Status |
|---|---|---|---|---|
| HV-01 | AC1 clause 2, X1, BR6 | MR changing a recovery Java file; a squad member outside the recovery group approves | Merge blocked; host shows code-owner review required | OPEN — NOT_TESTED_HERE |
| HV-02 | AC1 clause 1, AC2, AC4, flow 4–5 | MRs as UT-13, UT-15, UT-16 | Host lists the same sections and owners as the resolver | OPEN — NOT_TESTED_HERE |
| HV-03 | AC3, X3, flow 7 | MR changing one recovery and one common file; recovery owner approves | Blocked until an ACE-team member approves | OPEN — NOT_TESTED_HERE (needs a common file on the host; OPEN-024) |
| HV-04 | AC5, X4 | Recovery owner opens and approves own MR | Approval not counted; a second member is needed | OPEN — NOT_TESTED_HERE |
| HV-05 | AC6, X5 | Push a commit to an approved MR | Approvals removed; review required again | OPEN — NOT_TESTED_HERE |
| HV-06 | X7, TC-TE-002-08 | Non-owner squad member approves | Merge refused; no MSG-P4-002 (story §16) | OPEN — NOT_TESTED_HERE |
| HV-07 | AC7 host part, X6, HC-06, HC-08 | MR with `@scb-ace/recovery-leads-typo`; and a host check of owner existence and write access | `codeowners-validation` fails and the merge is blocked | OPEN — NOT_TESTED_HERE |
| HV-08 | BR4, BR7 | MR changing `.gitlab/CODEOWNERS`; one team approves | Blocked until the other team approves | OPEN — NOT_TESTED_HERE |
| HV-09 | A-10, HC-07 | Open a new MR | Description pre-filled with the eight headings | OPEN — NOT_TESTED_HERE |
| HV-10 | Story §2 measure | Monthly MR report on recovery paths | 100% merged with code-owner approval | OPEN — NOT_TESTED_HERE |
| HV-11 | SPEC-017 | Before host adoption | No `@role-placeholder/` handle left in the file or register | OPEN — NOT_TESTED_HERE |

### Security, privacy and authority

| Actor | What they may do (story §10) |
|---|---|
| TechX recovery tech leads | Approve changes in `[Recovery module]` and `[Code owners control recovery]`. |
| ACE team | Approve changes in `[Common module]` and `[Code owners control ACE team]`; set the host rules (HC). |
| RW-TRIBE, tribe lead, squad members | Open MRs; cannot satisfy a section unless in its group. |
| Roles with placeholders | Solution architect with the tech leads; TechX DevOps with SCB IT — no handle until OPEN-038. |

- No person, e-mail, personal data, token or credential in any file, test, fixture or log (story §17;
  AGENTS.md §4.1, §4.7). Fixtures use the synthetic handle `@scb-ace/recovery-leads-typo` (story AC7) and
  synthetic paths.
- No Workbench capability area applies; no MSG-P4-002 (story §10, §16).

### Observability, performance, idempotency, rollback

- Findings name the line, pattern and owner; the job's JUnit report is kept as an artefact.
- Static file checks only; no database, cache or scheduled job. The resolver is a pure function, so
  the same file and paths always give the same owners (story §12 idempotency; UT-20).
- Rollback: revert the files in a reviewed MR (owned per SPEC-005); host settings are reverted by the
  administrator from the record.

## Test scenarios

All are JUnit 5, tag `codeowners`, run by `gradlew test` and `codeOwnersTest`. "Fixture" = files
written to `@TempDir`; "live" = the repository files.

| ID | Covers | Data | Expected |
|---|---|---|---|
| UT-01 | V1, X9 | Fixture with a malformed line; and a missing file | `syntax error` on that line; missing file fails closed |
| UT-02 | V2 | Entry before any section | `entry outside a section` |
| UT-03 | V3 | `/x/` with no owner | `pattern /x/ has no owner` |
| UT-04 | V4 | `x/`, `/x/*.java`, `/x/**/y/` | `unsupported pattern` for each |
| UT-05 | V5 | Same pattern twice in a section; same pattern in two sections | Error for the first case only |
| UT-06 | V6, BR5 | `/a/b/` then `/a/` in one section; and `/a/` then `/a/b/` | Shadowed error in the first order only |
| UT-07 | V7, AC7, X6 | Recovery path owned by `@scb-ace/recovery-leads-typo` | `line {n}: owner @scb-ace/recovery-leads-typo not found`; validation fails |
| UT-08 | V8, §17 | Owners `@someone`, `someone@example.test` | `is not a team` for each |
| UT-09 | V9 | Pattern to a missing folder; and to an empty folder | `matches no file` for each |
| UT-10 | V10, BR3 | Reserved pattern with no file | Warning only; validation passes |
| UT-11 | V11, placeholders | Register missing a field; bad status; duplicate handle; a `PLACEHOLDER` owner | Errors for the first three; warning for the placeholder |
| UT-12 | All rules, flow 1 | Live `.gitlab/CODEOWNERS` and register | No `ERROR`; warnings list the reserved common pattern and the two placeholders |
| UT-13 | AC1 clause 1, BR1 | Live file; `backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/internal/AllocationService.java` (story AC1 path in this layout, synthetic) | `[Recovery module]` → `@scb-ace/techx-recovery-tech-leads` only |
| UT-14 | BR1 | Live file; one path each in recovery test, e2e test and migration folders | `[Recovery module]` for each |
| UT-15 | AC4, BR2 | Live file; `frontend/src/modules/recovery/caselist/CaseListPage.tsx`, `backend/src/main/resources/db/modulemigration/recovery/V0001__rwb_e1_001_recovery_schema.sql`, `backend/src/test/resources/architecture/recovery-modules.yaml` | `[Recovery module]` for all three |
| UT-16 | AC2, BR3, X2 | Live file; `backend/src/main/java/th/co/scb/ace/demo/common/ExampleService.java` (synthetic, not created) | `[Common module]` → `@scb-ace/ace-team` |
| UT-17 | AC3, X3 | Live file; the paths of UT-13 and UT-16 together | Both sections required |
| UT-18 | BR4, BR7 | Live file; `.gitlab/CODEOWNERS`, `.gitlab/codeowners-register.yaml`, a validator class path | Both control sections (both teams) required for each |
| UT-19 | BR5 | Fixture: general then specific pattern with different owners | Specific owner wins for a path under it; general owner for a sibling |
| UT-20 | §12 idempotency; unowned | Live file; same input twice; `README.md` | Equal results; `README.md` → no section |
| UT-21 | A-10, SPEC-015 | Live template | File exists; all eight headings present in order |
| UT-22 | A-05, SPEC-016 | Live `AGENTS.md` | Every back-quoted path in the §5 table exists from the repository root |

TC mapping (story §16): TC-TE-002-01 → UT-13 + HV-01; -02 → UT-16 + HV-02; -03 → UT-17 + HV-03;
-04 → UT-15 + HV-02; -05 → HV-04; -06 → HV-05; -07 → UT-07 + HV-07; -08 → HV-06. TC-TE-002-08 follows
story §16, which ranks above Test Cases v7 (RUN-BRIEF precedence; SP-DG-06).

## Guardrails and out of scope

Guardrails (story §17): no business value in any file; no personal data in logs, tests or prompts;
the file is the review control for the TE-001 boundary and reads no table; owners are groups, never
people (V8).

Out of scope (SPEC-019):

| Item | Reason | Receiving owner |
|---|---|---|
| Boundary test that checks the code | Story §19 | RWB-TE-001 |
| Code owners inside the collection module (and a collection pattern) | Story §19; DL04 | ACE team |
| Browser test runner in the pipeline | Story §19; DL37 | RWB-TE-010 |
| Common module test folder | Story §12 names the main folder only (ASM-TE002-05) | ACE team, by a reviewed MR once the folder exists (OPEN-038) |
| Package-level AGENTS.md (A-05) | No document-set content: AI Assisted Development Approach v1 §3 defines one root standards file "with a section for the recovery module", which this AGENTS.md already is | AISDLC-HARDENING (proposed `PROP-OI-3`) |
| Separate coding-standard file (A-05) | RUN-BRIEF "Paths" maps the coding standard to `aisdlc/.github/contexts/backend-standards.md` and `frontend-standards.md`; SPEC-016 names them in AGENTS.md §5 | AISDLC-HARDENING (proposed `PROP-OI-3`) |
| `infra/`, `scripts/`, `docker-compose.yml`, `backend/build.gradle.kts`, `frontend/eslint.config.js`, `AceRecoveryApplication.java`, `frontend/src/{components/ui,lib,contexts}` | Not recovery folders: README marks them as the local stack or local stand-ins for ACE shell entry points; story §12 does not name them | Left unowned; a later reviewed MR may add them (BR7) |
| Host check of owner existence and write access | Needs a host API and token (RUN-BRIEF rule 5) | ACE, HC-08 / HV-07 |
| Creating `main` or `develop`, or test MRs | No host here (SG-001, plan input 5) | HV items |

## Clarification Log

No question was asked (L-RCV-03). Each item is settled by a cited source or a labelled assumption.
Items that need an outside answer for the ACE host are carried as open items, not as open CLAR items.

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | Story §3, §12; L-RCV-12 | GitHub or GitLab format? | File path, syntax, host settings | No response (L-RCV-03). This repository stands in for GitLab (`.gitlab-ci.yml`, D-RCV-50 "MR"), so L-RCV-12 applies: `.gitlab/CODEOWNERS`. The real ACE host stays OPEN-038. | RESOLVED for this repository; ACE part in OPEN-038 | SPEC-001, -006 |
| CLAR-002 | Story §7, §12; ASM-TE002-02 | Story paths do not exist | Patterns would match nothing | Paths of this repository (SPEC-002, -003). | RESOLVED | SPEC-002, -003 |
| CLAR-003 | BR4 vs §10; Story Defects v4 row 91 | Who owns the code owners file? | Single-team edits | BR4 wins (L-RCV-13); two sections (ASM-TE002-11). Source fix is OPEN-041. | RESOLVED | SPEC-005 |
| CLAR-004 | BR3; story §12 | Common module absent here; common test folder | V9 would fail; AC2/AC3 need a file | Reserved pattern (SPEC-004); AC2/AC3 via resolver with synthetic paths; test folder excluded (ASM-TE002-05). | RESOLVED | SPEC-004, -007 |
| CLAR-005 | BR6; D-RCV-50 | Branch rule only on `main`? | Bypass via `develop-recovery` | Three branches (L-RCV-13), host-only (SPEC-012). | RESOLVED | SPEC-012 |
| CLAR-006 | AC5; D-RCV-21 | Who is in the recovery group? | Who can approve | Membership per D-RCV-21; handle per story §3, `ASSUMED`. | RESOLVED | SPEC-002, -009 |
| CLAR-007 | Story §12; AC7 | Owner existence without a host | AC7 untestable | Local register (SPEC-009); host check HC-08/HV-07. | RESOLVED | SPEC-008, -009 |
| CLAR-008 | A-05; Engineering Practices v5 §10 | Owner of AGENTS.md and the pipeline file has no handle | Control files unowned | Placeholders for the document-set roles (SPEC-017), OPEN-038 amendment `PROP-OI-1`. | RESOLVED | SPEC-017 |
| CLAR-009 | A-10; AGENTS.md §8; Engineering Practices v5 §4.2 | Which MR template fields? | Template content | Union of both lists (SP-DG-08). | RESOLVED | SPEC-015 |

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma link and no Jira/GitLab MCP; repository-governance story with no screen.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: Code owners file, register, validator, resolver, MR template and AGENTS.md path fix built here; host rules documented; host-only checks carried as human verification.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: repository review control; test-scope backend code only]
REQUIREMENT_COVERAGE_SUMMARY: 37 requirement rows (7 BR, 9 AC clauses, 7 X, 7 flow steps, contract, messages, measure, guardrails, out of scope, A-05, A-10) map to SPEC-001..019; host-only clauses are carried as 11 open human-verification items (HV-01..HV-11), none claimed as tested.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 37] [COVERED_RULES: 37] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [CLAR_OPEN: 0] [OPEN_ITEMS: 4 — OPEN-024, OPEN-038, OPEN-041, proposed PROP-OI-2] [HUMAN_VERIFICATION_OPEN: 11]
NEXT_STEP: Spec gate re-review (review/spec-gate-review-2.md); then, if it passes, a human starts the Implementation Planner, sequenced after RWB-TE-001 (precondition P1).
```

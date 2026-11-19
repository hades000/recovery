---
title: "RWB-TE-002 Code owners for the recovery module — documentation index"
run_id: "INC-004-epic-1-RWB-TE-002"
story: "RWB-TE-002"
epic: "EPIC-001"
stage: "docs (final documentation)"
date: "2026-11-18"
status: "DOCUMENTED — BUILT, ACCEPTANCE PENDING HV-01..HV-11; code gate PENDING_ORCHESTRATOR; no approval, merge or acceptance recorded (D-RUN-09)"
branch: "feature/RWB-TE-002-code-owners @ d018cf7 (code gate round 1 remediation; contains develop-recovery 0b87102, RWB-E1-042 merged; review remediation D-RUN-25; first written at ae61b08)"
sources: "specify/spec.md (spec gate round 5 PASS), plan/ (plan gate round 1 PASS), implement/implementation-report.md, handoff.md, deviations.md, preflight.md, document-gaps.md, shared-updates.md, code and .gitlab/ files at d018cf7 (first written at ae61b08)"
---

# Code owners for the recovery module (RWB-TE-002)

**DOC ID:** DOC-RWB-TE-002-001 · **Maps to:** SPEC-RWB-TE-002-001..-019, AC1–AC7, BR1–BR7, TASK-00..TASK-11, CODE-TE002-01..08

RWB-TE-002 gives the repository a GitLab code owners file (`.gitlab/CODEOWNERS`, L-RCV-12) that makes
every change to the recovery module need an approval from the TechX recovery tech leads, every
change to the reserved common module need the ACE team, and every change to the code owners
control files need both teams. A test-scope validator checks the file on every build, a resolver
computes which teams a set of changed paths needs, and the host settings that turn the file into a
merge block are written down for the ACE repository administrator.

**Local state: `BUILT — ACCEPTANCE PENDING HV-01..HV-11`.** This is not Done. Story §13 needs the
branch rule on `main` to show code-owner review as required; that, and every acceptance clause only a
host can show, is human verification HV-01..HV-11, all `OPEN — NOT_TESTED_HERE` (SPEC-018). No human
approval, acceptance or ratification is recorded or claimed (D-RUN-09). The code gate has not run
yet; the orchestrator runs it.

## 1. What was built

| Deliverable | Where (repository root) | SPEC | CODE | TASK |
|---|---|---|---|---|
| Code owners file, 6 sections, 66 lines (55 from the spec block + 11 from the D-RUN-25 addendum, `../implement/plan-addendum.md`) | `.gitlab/CODEOWNERS` | 001–005, 017 | CODE-TE002-06 | TASK-05 |
| Owner register (4 handles, 3 reserved patterns: common root, `/CODEOWNERS`, `/docs/CODEOWNERS`) | `.gitlab/codeowners-register.yaml` | 009 | CODE-TE002-06 | TASK-05 |
| Host configuration record HC-01..HC-08 (`OPEN — NOT_APPLIED_HERE`) | `.gitlab/host-settings.md` | 006, 010–012 | CODE-TE002-06 | TASK-05 |
| MR template, eight headings | `.gitlab/merge_request_templates/Default.md` | 015 | CODE-TE002-07 | TASK-06 |
| AGENTS.md §5 path fix (A-05) | `AGENTS.md` | 016 | CODE-TE002-07 | TASK-06 |
| Parser, register reader, validator (V1–V12), resolver | `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/codeowners/` | 001, 007–009 | CODE-TE002-01..04 | TASK-04 |
| 35 JUnit methods (UT-01..UT-26 plus 4 pre-merge remediation tests, 1 guard test and 2 code gate round 1 tests), tag `codeowners` | same package, five `*Test` classes | 001–005, 007–009, 013, 015–017 | CODE-TE002-05 | TASK-01..03 |
| Gradle tasks `codeOwnersTest`, `codeOwnersCoverageReport`, `codeOwnersCoverageVerification` | `backend/build.gradle.kts` (appended block) | 013, 014 | CODE-TE002-08 | TASK-07 |
| CI job `codeowners-validation` (defined, never run here) | `.gitlab-ci.yml` | 013 | CODE-TE002-08 | TASK-07 |

Change classification: `NEW_STORY`; UI In Scope `NO`; API In Scope `NO`; `NO_API_CHANGE`; no
main-source class, endpoint, entity, migration, dependency or frontend file changes. All Java is
test scope. Commits (tests first): `9f2ece0` red, `f28ada1`, `3e281c2`, `b9fe59b`, `ae61b08`; review remediation `1948f97` red, `a3af237` merge of `develop-recovery`, `c740d25` green; code gate round 1 `f61f133` red, `d018cf7` green.

## 2. Who owns what

**DOC ID:** DOC-RWB-TE-002-002 · **Maps to:** SPEC-RWB-TE-002-001..-005, -017; BR1–BR5, BR7; AC1, AC2, AC4; TASK-05; CODE-TE002-06; UT-12..UT-18, UT-25, UT-26

| Section | Owner handle (register status) | What it covers |
|---|---|---|
| `[Common module]` | `@scb-ace/ace-team` (ASSUMED) | `/backend/src/main/java/th/co/scb/ace/demo/common/`: **reserved**, the folder does not exist here (OPEN-024); the validator warns, not fails (V10). Addendum A4: `backend/src/main/resources/application.yaml`, `application-local.yaml` |
| `[Recovery module]` | `@scb-ace/techx-recovery-tech-leads` (ASSUMED) | Recovery main and test packages (all 19 TE-001 modules), e2e tests, `ModulithTest.java`, TE-001 fixture root `boundaryfixture/`, recovery migration folder, module map `recovery-modules.yaml`, `architecture/fixtures/`, `frontend/src/modules/recovery/`, `frontend/e2e/`, `api/recovery-api-v4.yaml`, `frontend/src/api/schema.d.ts`, `frontend/eslint.config.js`; addendum A1 `architecture/magic-number-baseline.csv`, A5 `application.yaml`, `application-local.yaml` |
| `[Code owners control ACE team]` | `@scb-ace/ace-team` | The three `.gitlab/` control files and the validator package; addendum A2: reserved `/CODEOWNERS`, `/docs/CODEOWNERS` (must not exist, `noHigherPrecedenceCodeOwnersFileExists`) |
| `[Code owners control recovery]` | `@scb-ace/techx-recovery-tech-leads` | The three `.gitlab/` control files (the validator package is already recovery-owned through the test package); addendum A3: reserved `/CODEOWNERS`, `/docs/CODEOWNERS` |
| `[Repository standards]` | `@role-placeholder/solution-architect-with-tech-leads` (PLACEHOLDER) | `AGENTS.md`, `CLAUDE.md`, `.claude/`, `aisdlc/.github/`, `.gitlab/merge_request_templates/` |
| `[Pipeline gates]` | `@role-placeholder/techx-devops-with-scb-it` (PLACEHOLDER) | `.gitlab-ci.yml`, backend and frontend root build files, `scripts/dev.ps1`; addendum A6 `backend/Dockerfile`, `backend/.dockerignore` |

A file matched in several sections needs one approval from each section (BR4: the control files need
both teams; `frontend/eslint.config.js` needs recovery and pipeline gates). Within a section the last
matching pattern wins (BR5). The two `@role-placeholder/` handles are not team handles; they must be
replaced before host use (OPEN-038, `PROP-OI-1`, HV-11).

## 3. Running it

**DOC ID:** DOC-RWB-TE-002-003 · **Maps to:** SPEC-RWB-TE-002-013, -014; TASK-07, TASK-08, TASK-10; CODE-TE002-08; UT-24

| What | Command (from repository root) | Status here |
|---|---|---|
| Backend unit suite (includes the 35 codeowners tests) | `cd backend; ./gradlew test` | **Run** at `d018cf7`: exit 0; 423 tests, 0 failures (`../implement/backend/final-tip-test.log`, `final-tip-counts.txt`). Superseded: `./scripts/dev.ps1 test` at `ae61b08` (backend 271, frontend Vitest 28/28, `../implement/dev-test.log`); frontend not re-run, no frontend change (`final-tip-scope.txt`) |
| Codeowners tests and 80% gate only | `cd backend; ./gradlew codeOwnersTest codeOwnersCoverageVerification` | **Run** at `d018cf7`: exit 0; 35 tests, 0 failures (`../implement/backend/final-tip-codeowners.log`) |
| CI job `codeowners-validation` (stage `verify`) | runs the command above on the host | **Defined only**; never run here (HV-07) |

Coverage of the four helper classes (native JaCoCo XML
`../implement/backend/coverage-final/codeOwnersCoverageReport.xml`, at `d018cf7`): LINE 95.77 (204/213),
BRANCH 95.90 (117/122), INSTRUCTION 96.85 (1262/1303), METHOD 100 (43/43); gate 80% on each. Figures at `c740d25` (33 / 421 tests; 95.71/95.83/96.83/100) are superseded; their logs are in `implement/backend/superseded-c740d25/`.

A failed check names the line, the pattern and the owner, for example `line 12: owner
@scb-ace/recovery-leads-typo not found` (V7). To change an owner, edit the file and the register in
one MR that both teams approve (BR7).

## 4. Open facts the reader must know

**DOC ID:** DOC-RWB-TE-002-004 · **Maps to:** SPEC-RWB-TE-002-002, -018; BR1; UT-26; DEV-01; IM-DG-01, IM-DG-02; IM-SU-01; `PROP-OI-4`

1. **RWB-E1-042 and the D-RUN-25 addendum (resolved, ratification pending).** RWB-E1-042 adds
   `backend/src/test/resources/architecture/magic-number-baseline.csv`. After `develop-recovery` was
   merged into this branch (`a3af237`), UT-26 failed on it (`../implement/backend/red-magic-number.txt`).
   The D-RUN-25 plan addendum (`../implement/plan-addendum.md`, a deviation from the exact spec block,
   DEV-08) adds that line and, from the pre-merge security review, reserved `/CODEOWNERS` and
   `/docs/CODEOWNERS` (F1), `application.yaml` and `application-local.yaml` (F2), and `backend/Dockerfile`
   and `backend/.dockerignore` (F4). UT-26 passes at `c740d25` and `d018cf7`. The tech lead must ratify the addendum
   (IM-SU-04). Placeholder owners (F3) stay open under OPEN-038.
2. **Other recovery-owned files have no line** and no test covers them: RWB-E1-044
   `backend/src/test/resources/migration-lint/`, `flyway-fixtures/`; RWB-E1-042
   `backend/src/main/resources/config/parameter-catalog.csv`, `access/interim-capability-grants.csv`
   (IM-DG-02, `PROP-OI-4`).
3. **Host-only acceptance**: HV-01..HV-11 are `OPEN — NOT_TESTED_HERE`; HC-01..HC-08 are
   `OPEN — NOT_APPLIED_HERE` (`COMPLIANCE.md` §4).
4. **Deviations** DEV-01..DEV-09 (`COMPLIANCE.md` §5; DEV-08 is the D-RUN-25 addendum, DEV-09 the Nice-3 guard test), including DEV-07: the CI artifact keeps the
   JaCoCo HTML only, not the XML (IM-SU-02).
5. **Open items left open**: OPEN-016, OPEN-024, OPEN-038, OPEN-041, OPEN-050; proposed
   `PROP-OI-1`..`PROP-OI-4` and IM-SU-04 (ratify the addendum) (`COMPLIANCE.md` §6).

## 5. Documents in this folder

| File | DOC IDs | Content |
|---|---|---|
| `README.md` | 001–004 | This index, ownership map, commands, open facts |
| `ARCHITECTURE.md` | 005–009 | Components, validation rules, resolver, build and CI wiring, governance files |
| `COMPLIANCE.md` | 010–015 | AC and BR trace, host settings and HV items, deviations, open items, guardrails |
| `assumptions.md` | — | Documentation-stage assumptions |
| `document-gaps.md` | — | Gaps and evidence inconsistencies found by this stage |
| `shared-updates.md` | — | Rows for shared files (orchestrator / Traceability Manager) |

No `OPERATIONS.md`: the story adds no runtime job, endpoint or monitor. The host procedure is
`.gitlab/host-settings.md` plus the HV table in `COMPLIANCE.md` §4.

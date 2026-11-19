---
title: "RWB-TE-002 Code owners for the recovery module — compliance record"
run_id: "INC-004-epic-1-RWB-TE-002"
story: "RWB-TE-002"
stage: "docs (final documentation)"
date: "2026-11-18"
status: "DOCUMENTED — BUILT, ACCEPTANCE PENDING HV-01..HV-11; code gate PENDING_ORCHESTRATOR; no approval, merge or acceptance recorded (D-RUN-09)"
---

# Compliance record — RWB-TE-002

Sections 2–7 carry `DOC-RWB-TE-002-010`..`-015`; §1 is their shared scope. This record states what
is evidenced locally and what stays open. It is written **before** the code gate, which the
orchestrator runs; it adds no review and claims no approval.

## 1. Scope

| Field | Value |
|---|---|
| Story | RWB-TE-002 Code owners for the recovery module, EPIC-001 |
| Acceptance basis | AC1–AC7, BR1–BR7, X1–X7, TC-TE-002-01..08 of story files v7, as restated in the gated spec (spec gate round 5 PASS; plan gate round 1 PASS) |
| Change classification | `NEW_STORY`; UI `NO`; API `NO`; `NO_API_CHANGE`; test-scope Java, Gradle, CI and `.gitlab/` files only |
| API / functional test stages | NOT_APPLICABLE by scope (no endpoint, no screen); no stage report file exists in the evidence folder (see `document-gaps.md` DOC-DG-02) |
| Personal data | None. Owners are groups; synthetic paths only (V8; story §17) |
| Banking compliance documentation | Not required: no customer data, financial value or account field |
| Local end state | `BUILT — ACCEPTANCE PENDING HV-01..HV-11`; never Done (SPEC-018) |

## 2. Acceptance criteria trace

**DOC ID:** DOC-RWB-TE-002-010 · **Maps to:** AC1–AC7; X1–X7; SPEC-RWB-TE-002-002..-013, -018; TASK-01..TASK-07; CODE-TE002-03..06; UT-07, UT-13..UT-17; HV-01..HV-07

| AC | Requirement | SPEC | Local test (result) | Host item |
|---|---|---|---|---|
| AC1 cl.1 | A recovery change requires a TechX tech lead | 002, 007 | UT-13 `recoveryMainPathNeedsRecoveryTeam` (PASS) | HV-02 |
| AC1 cl.2 / X1 | Outside squad member's approval leaves merge blocked | 006, 018 | — | HV-01 OPEN — NOT_TESTED_HERE |
| AC2 / X2 | Common module change needs `@scb-ace/ace-team` | 004, 007 | UT-16 `commonModulePathNeedsAceTeam` (PASS) | HV-02 |
| AC3 / X3 | Change across both modules needs both teams; blocked until ACE approves | 007, 006, 018 | UT-17 `bothModulesNeedBothTeams` (PASS) | HV-03 (needs a common file, OPEN-024) |
| AC4 | Front end, migrations, module map need the recovery team | 003, 007 | UT-15 (PASS) | HV-02 |
| AC5 / X4 | Author cannot approve own change | 010, 018 | — (HC-04) | HV-04 |
| AC6 / X5 | New commit needs new approval | 011, 018 | — (HC-05) | HV-05 |
| AC7 / X6 | Missing owner fails the check, `owner {team} not found` | 008, 009, 013 | UT-07 `ownerNotInTheRegisterIsRejected` (PASS) | HV-07 (host existence and write access, pipeline run) |
| X7 / TC-TE-002-08 | Non-owner cannot satisfy the review | 018 | — | HV-06 |

TC mapping (spec): TC-01 → UT-13 + HV-01; -02 → UT-16 + HV-02; -03 → UT-17 + HV-03; -04 → UT-15 +
HV-02; -05 → HV-04; -06 → HV-05; -07 → UT-07 + HV-07; -08 → HV-06. A UT is a partial local check; the
TC passes only when its HV item passes.

## 3. Business rules trace

**DOC ID:** DOC-RWB-TE-002-011 · **Maps to:** BR1–BR7; story §12, §13, §17; SPEC-RWB-TE-002-001..-017; UT-01..UT-26

| BR | SPEC | Evidence |
|---|---|---|
| BR1 recovery back end, tests, migrations → recovery tech leads | 002 | UT-13, UT-14, UT-26 PASS at `c740d25`, after RWB-E1-042 was merged in and addendum line A1 added (`README.md` §4) |
| BR2 front end and module map → recovery tech leads | 003 | UT-15, UT-26 |
| BR3 common module → ACE team (reserved) | 004 | UT-10, UT-16 |
| BR4 code owners file owned by both teams | 005 | UT-18, UT-23; HV-08 |
| BR5 last match wins, specific after general | 001, 007, 008 | UT-06, UT-19 |
| BR6 code-owner approval per path, author excluded, new commit dismisses | 006, 010–012 | HC-01..HC-05; HV-01, -03, -04, -05 |
| BR7 team names are file values changed by reviewed MR | 005, 009 | UT-18, UT-23 |

Suite at `d018cf7`: 35 JUnit methods for UT-01..UT-26 and the review and code gate remediation, 0 failures,
0 skipped (`../implement/backend/final-tip-codeowners.log`). Backend `gradlew test` exit 0, 423 tests,
0 failures (`../implement/backend/final-tip-test.log`). Codeowners coverage: LINE 95.77, BRANCH 95.90,
INSTRUCTION 96.85, METHOD 100 (gate 80; `../implement/backend/final-tip-counts.txt`). Figures at `c740d25` (33 / 421 tests; 95.71/95.83/96.83/100) are superseded; their logs are in `implement/backend/superseded-c740d25/`. Superseded figures
at `ae61b08`: 28 methods; `dev.ps1 test` backend 271, frontend Vitest 28/28; coverage 95.69/95.76/96.80/100.
Frontend not re-run: no frontend change (`../implement/backend/final-tip-scope.txt`).

## 4. Host settings and human verification

**DOC ID:** DOC-RWB-TE-002-012 · **Maps to:** SPEC-RWB-TE-002-006, -010, -011, -012, -018; HC-01..HC-08; HV-01..HV-11; `PROP-OI-2`; story §13

Owner of every row: the ACE team repository administrator with the recovery tech lead. HC-01..HC-08
(`.gitlab/host-settings.md`) are `OPEN — NOT_APPLIED_HERE`: protected `main`, `develop-recovery`,
`develop`; code-owner approval on; 1 approval; author approval prevented; approvals removed on a new
commit; pipelines must succeed; default MR template; owner groups exist with write access.

| HV | Covers | Status |
|---|---|---|
| HV-01 | AC1 cl.2, X1, BR6 | OPEN — NOT_TESTED_HERE |
| HV-02 | AC1 cl.1, AC2, AC4, flows 4–5 | OPEN — NOT_TESTED_HERE |
| HV-03 | AC3, X3, flow 7 | OPEN — NOT_TESTED_HERE |
| HV-04 | AC5, X4 | OPEN — NOT_TESTED_HERE |
| HV-05 | AC6, X5 | OPEN — NOT_TESTED_HERE |
| HV-06 | X7, TC-TE-002-08 | OPEN — NOT_TESTED_HERE |
| HV-07 | AC7 host part, X6, HC-06, HC-08; first pipeline run of `codeowners-validation` and its coverage gate | OPEN — NOT_TESTED_HERE |
| HV-08 | BR4, BR7 | OPEN — NOT_TESTED_HERE |
| HV-09 | A-10, HC-07 | OPEN — NOT_TESTED_HERE |
| HV-10 | Story §2 measure (100% of merged recovery MRs code-owner approved) | OPEN — NOT_TESTED_HERE |
| HV-11 | SPEC-017: no `@role-placeholder/` handle left | OPEN — NOT_TESTED_HERE |

No HV item is passed from local evidence. Merge record (orchestrator only, `handoff.md`): the
`--no-ff` merge commit message and `aisdlc/output/INC-004-epic-1-RWB-TE-002/README.md` carry
"Acceptance pending HV-01..HV-11 (PROP-OI-2). OPEN-038 open: role placeholders and assumed team
handles must be replaced or confirmed before host use (HV-11)."

## 5. Deviations from the plan

**DOC ID:** DOC-RWB-TE-002-013 · **Maps to:** DEV-01..DEV-09 (`../implement/deviations.md`); TASK-00, TASK-09; UT-20, UT-23, UT-26; IM-SU-01, IM-SU-02

| ID | Summary | Effect |
|---|---|---|
| DEV-01 | TASK-00 did not stop on RWB-E1-042's `magic-number-baseline.csv`: on base `7bee04d` every UT-26 file is owned. Block kept exact, UT-26 not weakened | Resolved at `c740d25`: addendum line A1 (`../implement/plan-addendum.md`, DEV-08) adds `/backend/src/test/resources/architecture/magic-number-baseline.csv @scb-ace/techx-recovery-tech-leads` to `[Recovery module]` |
| DEV-08 | D-RUN-25 plan addendum: C2 (V4/V9 widened: `.`, `..`, `//`, `:` rejected, target kept under the root), C4 (cache key `gradle-codeowners`, departs from SPEC-013), H1 (HC-09), and 11 CODEOWNERS lines beyond the exact spec block (A1 magic-number baseline; A2/A3 reserved `/CODEOWNERS`, `/docs/CODEOWNERS`; A4/A5 `application.yaml`, `application-local.yaml`; A6 `backend/Dockerfile`, `.dockerignore`) and two reserved patterns | Deviation from the spec; tech lead must ratify (IM-SU-04) |
| DEV-09 | Guard test `codeOwnersTestIsNeverUpToDate` for ponytail Nice 3, written after the fix | Additive |
| DEV-10 | `noHigherPrecedenceCodeOwnersFileExists` is a repository-state guard; at `1948f97` it was red only because a temporary, uncommitted root `CODEOWNERS` probe file existed during the red run (session transcript evidence in `../implement/deviations.md`) | Guard shown to work; not a code-driven red test |
| DEV-11 | CODE1-001 tests first: red `f61f133` (`../implement/backend/red-code1-001.txt`), green `d018cf7` | No assertion weakened |
| DEV-02 | No baseline `gradlew test` before work | Regression evidence is the single `dev.ps1 test` at the tip |
| DEV-03 | Dependency diff replaced by a `build.gradle.kts` diff | Append-only, no dependency line |
| DEV-04 | UT-26 lists all unowned paths in one assertion | Stronger diagnostics |
| DEV-05 | V5 keyed per section block, not section name | V12 still fails a repeated header |
| DEV-06 | UT-20 adds a backslash-path normalisation assertion | Additive |
| DEV-07 | CI artifact path kept exactly; XML report lies outside it | HTML only in artifact; follow-up IM-SU-02 |

## 6. Open items and out of scope

**DOC ID:** DOC-RWB-TE-002-014 · **Maps to:** SPEC-RWB-TE-002-017, -018, -019; OPEN-016, -024, -038, -041, -050; `PROP-OI-1`..`-4`; IM-DG-01, IM-DG-02

| Item | What stays open | Effect on this story |
|---|---|---|
| OPEN-016 | Per-story approver names are not in Jira | No named approver is recorded anywhere for this story (D-RUN-09) |
| OPEN-024 | Real root and published packages of common | Common pattern stays reserved (V10 warning); HV-03 needs a common file |
| OPEN-038 | Host, real team handles, tier, token scope, branch names | Handles `ASSUMED`/`PLACEHOLDER`; HC rows unapplied |
| OPEN-041 | Story Defects v4 row 91 (BR4 vs §10) to be closed in the source | BR4 applied (two control sections) |
| OPEN-050 | Ratify D-RUN-18..21 (D-RUN-21: "one module" = ACE recovery module) | Plan's one-module check rests on D-RUN-21 |
| `PROP-OI-1` | Amend OPEN-038 (replace placeholders, confirm tier and setting names, "needed by" host use) | HV-11 |
| `PROP-OI-2` | Run HV-01..HV-11 on the ACE host | Acceptance pending |
| `PROP-OI-3` | A-05 exclusions: package-level AGENTS.md, separate coding-standard file | Out of scope (SPEC-019) |
| `PROP-OI-4` | Ownership of recovery files outside the block (E1-044 `migration-lint/`, `flyway-fixtures/`; E1-042 `config/parameter-catalog.csv`, `access/interim-capability-grants.csv`) | No line, no test; extended by IM-SU-01; security review F5 |
| IM-SU-04 (proposed) | Tech lead to ratify the D-RUN-25 addendum paths and owners | Open |
| Security F3 | `@role-placeholder/` groups give no real approval on `[Repository standards]` and `[Pipeline gates]` (now including `backend/Dockerfile`) | Recorded gap, Blocker No, under OPEN-038; not accepted |
| IM-DG-03 | Protected-branch cache separation (security F8): HC-09 in `.gitlab/host-settings.md`, `OPEN — NOT_APPLIED_HERE`, ratification pending (IM-SU-04) | Recorded gap, Blocker No |
| IM-DG-04 | CI image `eclipse-temurin:21-jdk` not pinned by digest (security F8): SPEC-013 fixes the tag, the document set has no digest; none invented | Recorded gap, Blocker No, OPEN-038 |

Out of scope (SPEC-019, story §19): the TE-001 boundary test itself, collection-module code owners,
the TE-010 browser runner, the host owner-existence API check (HC-08/HV-07), and the two A-05 parts
in `PROP-OI-3`.

## 7. Guardrails, security and privacy

**DOC ID:** DOC-RWB-TE-002-015 · **Maps to:** story §17; SPEC-RWB-TE-002-001, -008 (V8), -009, -015; TASK-09; AGENTS.md §4

- No business value, threshold or route in any file; the code owners file holds paths and group
  handles only.
- No personal data: register has no person, membership or e-mail; MR template names no reviewer;
  test paths are synthetic (`AllocationService.java`, `ExampleService.java`, not created).
- No credential or token is used or printed; the host API check that would need one is not built.
- No new dependency (SnakeYAML 2.6 already on the test classpaths; `preflight.md` #3).
- Scope check: `git diff --name-status develop-recovery` at `d018cf7` lists 16 files, none under
  `backend/src/main/`, `frontend/` or `api/` (`../implement/backend/final-tip-scope.txt`; earlier `../implement/scope-check.md` at `ae61b08`).

# Handoff: RWB-TE-002 (TASK-11)

Local state: `BUILT — ACCEPTANCE PENDING HV-01..HV-11`

This is not Done. No human approval, acceptance or ratification is recorded or claimed.

## What runs here and what is only defined

| Item | Where it runs | Evidence |
|---|---|---|
| UT-01..UT-26 (35 JUnit methods at `d018cf7`, tag `codeowners`) | `gradlew test`, hence `./scripts/dev.ps1 test`; also `gradlew codeOwnersTest` | `backend/final-tip-codeowners.log`, `backend/final-tip-test.log` (superseded: `backend/coverage.log`, `dev-test.log`) |
| `codeOwnersCoverageVerification` (80% LINE, BRANCH, INSTRUCTION, METHOD) | Run locally by this Builder | `backend/coverage/codeOwnersCoverageReport.xml`, `backend/coverage/counters.txt` |
| CI job `codeowners-validation` | Defined in `.gitlab-ci.yml` and checked as a definition by UT-24; **never run here** (no GitLab runner) | HV-07 |
| Host settings HC-01..HC-09 | Recorded in `.gitlab/host-settings.md`, status `OPEN — NOT_APPLIED_HERE` | HV items below |

Figures at `c740d25` (33 / 421 tests; 95.71/95.83/96.83/100) are superseded; their logs are in `implement/backend/superseded-c740d25/`.

## Coverage at the final tip `d018cf7` (native JaCoCo XML `backend/coverage-final/codeOwnersCoverageReport.xml`, log `backend/final-tip-codeowners.log`)

| Counter | Covered / total | % | Gate |
|---|---|---|---|
| LINE | 204 / 213 | 95.77 | ≥ 80 PASS |
| BRANCH | 117 / 122 | 95.90 | ≥ 80 PASS |
| INSTRUCTION | 1262 / 1303 | 96.85 | ≥ 80 PASS |
| METHOD | 43 / 43 | 100.00 | ≥ 80 PASS |

Tests at `d018cf7`: codeowners 35 / 0 failed; backend `gradlew test` 423 / 0 failed (`backend/final-tip-counts.txt`).

## [Superseded, ae61b08] Coverage (TASK-08, native JaCoCo XML)

| Counter | Covered / total | % | Gate |
|---|---|---|---|
| LINE | 200 / 209 | 95.69 | ≥ 80 PASS |
| BRANCH | 113 / 118 | 95.76 | ≥ 80 PASS |
| INSTRUCTION | 1242 / 1283 | 96.80 | ≥ 80 PASS |
| METHOD | 43 / 43 | 100.00 | ≥ 80 PASS |

## Human verification (owner: ACE team repository administrator with the recovery tech lead)

| ID | Covers | Status |
|---|---|---|
| HV-01 | AC1 clause 2, X1, BR6 | OPEN — NOT_TESTED_HERE |
| HV-02 | AC1 clause 1, AC2, AC4, flows 4-5 | OPEN — NOT_TESTED_HERE |
| HV-03 | AC3, X3, flow 7 | OPEN — NOT_TESTED_HERE |
| HV-04 | AC5, X4 | OPEN — NOT_TESTED_HERE |
| HV-05 | AC6, X5 | OPEN — NOT_TESTED_HERE |
| HV-06 | X7, TC-TE-002-08 | OPEN — NOT_TESTED_HERE |
| HV-07 | AC7 host part, X6, HC-06, HC-08, pipeline run of `codeowners-validation` | OPEN — NOT_TESTED_HERE |
| HV-08 | BR4, BR7 | OPEN — NOT_TESTED_HERE |
| HV-09 | A-10, HC-07 | OPEN — NOT_TESTED_HERE |
| HV-10 | Story §2 measure | OPEN — NOT_TESTED_HERE |
| HV-11 | SPEC-017 (no `@role-placeholder/` handle left) | OPEN — NOT_TESTED_HERE |

## Merge record (orchestrator only)

The Builder writes neither carrier. At merge the orchestrator runs `git merge --no-ff --no-commit feature/RWB-TE-002-code-owners`, writes `aisdlc/output/INC-004-epic-1-RWB-TE-002/README.md`, then commits; the merge commit message and the README carry exactly: "Acceptance pending HV-01..HV-11 (PROP-OI-2). OPEN-038 open: role placeholders and assumed team handles must be replaced or confirmed before host use (HV-11)." (plan SU-P06).

## Before merge: RWB-E1-042 (resolved)

`develop-recovery` (with RWB-E1-042) was merged into this branch at `a3af237`; UT-26 went red on `magic-number-baseline.csv` (`backend/red-magic-number.txt`) and is green at `c740d25` with the D-RUN-25 addendum line A1 (`plan-addendum.md`). The tech lead must ratify the addendum (IM-SU-04).

## Open items left open

OPEN-024, OPEN-038, OPEN-041, OPEN-050; proposed `PROP-OI-1`..`PROP-OI-4` (IM-SU-01 extends `PROP-OI-4`); proposed IM-SU-04 (ratify the D-RUN-25 addendum). Security F3 stays a recorded gap under OPEN-038 (Blocker No); F5 stays under PROP-OI-4.

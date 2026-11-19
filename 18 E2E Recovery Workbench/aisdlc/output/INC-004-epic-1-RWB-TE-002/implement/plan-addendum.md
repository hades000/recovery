# Plan addendum: RWB-TE-002 review remediation (D-RUN-25)

RUN_ID `INC-004-epic-1-RWB-TE-002`. Final code tip `d018cf7` (code gate round 1 remediation: red `f61f133`, green `d018cf7`; first written at `c740d25`) on `feature/RWB-TE-002-code-owners`
(merge of `develop-recovery` 0b87102 at `a3af237`, red tests at `1948f97`).

**This is a deviation from the spec block, not a reading of it.** The spec's "Code owners file" block
(`specify/spec.md:255-260`, "nothing else in the block changes") is exact. D-RUN-25 adds the lines below
after the pre-merge reviews (`review/ponytail-review.md`, `review/security-review.md`). Every owner is
one already in `.gitlab/codeowners-register.yaml`; no owner was added or renamed.

**Ratification needed:** the tech lead must ratify the added paths and owners at the merge request
(new open item proposed in `shared-updates.md` IM-SU-04; it covers A1-A6, R1, C2, C4 and H1). Nothing here is an approval.

## Lines added to `.gitlab/CODEOWNERS` (now 66 lines; was 55 at `ae61b08`)

| # | Section | Line | Reason | Test |
|---|---|---|---|---|
| A1 | `[Recovery module]` | `/backend/src/test/resources/architecture/magic-number-baseline.csv @scb-ace/techx-recovery-tech-leads` | RWB-E1-042 adds the file; UT-26 failed on it after the merge (IM-SU-01, DEV-01) | UT-26 `everyRecoveryTestFileResolvesToTheRecoveryTeam` (red at `a3af237`: `backend/red-magic-number.txt`) |
| A2 | `[Code owners control ACE team]` | `/CODEOWNERS @scb-ace/ace-team`, `/docs/CODEOWNERS @scb-ace/ace-team` | Security F1: GitLab reads these before `.gitlab/CODEOWNERS` | `addendumPathsHaveOwners`, `noHigherPrecedenceCodeOwnersFileExists` |
| A3 | `[Code owners control recovery]` | `/CODEOWNERS @scb-ace/techx-recovery-tech-leads`, `/docs/CODEOWNERS @scb-ace/techx-recovery-tech-leads` | Security F1 (same owners as `.gitlab/CODEOWNERS`) | same |
| A4 | `[Common module]` | `/backend/src/main/resources/application.yaml @scb-ace/ace-team`, `/backend/src/main/resources/application-local.yaml @scb-ace/ace-team` | Security F2: shared service settings (OIDC issuer, migrator, migration location) | `addendumPathsHaveOwners` |
| A5 | `[Recovery module]` | the same two `application*.yaml` paths `@scb-ace/techx-recovery-tech-leads` | Security F2: the files also carry recovery settings | `addendumPathsHaveOwners` |
| A6 | `[Pipeline gates]` | `/backend/Dockerfile`, `/backend/.dockerignore` `@role-placeholder/techx-devops-with-scb-it` | Security F4 | `addendumPathsHaveOwners` |

## Register and code changes

| # | File | Change | Finding | Test |
|---|---|---|---|---|
| R1 | `.gitlab/codeowners-register.yaml` | `reservedPatterns` gains `/CODEOWNERS` and `/docs/CODEOWNERS` (basis: F1, D-RUN-25), so V10 reports them as WARNING, not a V9 error | F1 | `liveFileAndRegisterPass` (four expected warnings, lines 34, 35, 41, 42) |
| C1 | `CodeOwnersValidator.java` | V7 skips "not found" only when the register already has a problem (fail closed on `owners: []`) | Ponytail Must 1, F6 | `emptyOwnerListStillChecksEveryOwner` |
| C2 | `CodeOwnersValidator.java` | V4 rejects a `.`, `..` or empty (`//`) path segment and any `:`; V9 normalises the target and requires it under the repository root (`d018cf7`, code gate CODE1-001). Widens V4 beyond its spec text | Ponytail Nice 2, F7 | `dotSegmentPatternsAreRejected`, `emptySegmentAndColonPatternsAreRejected`, `patternResolvingOutsideTheRootMatchesNoFile` |
| C3 | `backend/build.gradle.kts` | `codeOwnersTest`: `outputs.upToDateWhen { false }` | Ponytail Nice 3 | `codeOwnersTestIsNeverUpToDate` |
| C4 | `.gitlab-ci.yml` | `codeowners-validation` cache key `gradle-codeowners`; departs from SPEC-013 and `data-model.md` §7 (`key: gradle`) | F8 | `validationJobIsDefinedAsSpecified` |
| H1 | `.gitlab/host-settings.md` | HC-09: separate caches for protected branches, `OPEN — NOT_APPLIED_HERE` (code gate CODE1-002; IM-DG-03) | F8 | — (host item, HV-07) |

## Not changed

- F3 (placeholder groups give no real approval): the real group names are not in the document set
  (OPEN-038). Recorded gap, Blocker No, for the tech lead; not accepted.
- F5 (migration-lint and Flyway test fixtures, E1-042 `parameter-catalog.csv` and
  `interim-capability-grants.csv` unowned): PROP-OI-4, stays open.
- F8 second half (image tag not pinned by digest): SPEC-013 fixes the tag and the document set has no digest; recorded gap IM-DG-04 (Blocker No); no digest invented.

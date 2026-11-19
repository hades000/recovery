# Post-merge code-quality review: RWB-E1-044, RWB-TE-001, RWB-E1-042, RWB-TE-002

| Field | Value |
|---|---|
| Reviewed | `develop-recovery` at `27567ed` (the four merges `dc2d25b`, `b1d7424`, `0b87102`, `27567ed`, and the hardening commit `e566360`) |
| Reviewer | Independent review agent (Claude Opus 5.5, high effort, ponytail-review method), read only. It ran no tests |
| Requested by | orchestrator (Claude Code), 18 Nov 2026, before the repository is handed to the bank |
| Why | A whole-codebase review after the four merges. Each story's pre-merge review looked at that story's diff only. This review looks at the merged result |
| Disposition | See `README.md` in this folder. Each finding is fixed under the playbook or registered with an owner. None is accepted without a record (D-RUN-09) |

> Provenance: the agent returned this report as text. The orchestrator saved it here. The wording is
> condensed slightly; the IDs, files, lines and fixes are unchanged.

The orchestrator re-checked H1, H2 and H3 against the code before acting:
- H1: `ParameterLoadHandlerImpl.approve` locks only its own load's rows, then runs `countApprovedFrom`.
- H2: `@Value("${rwb.environment:DEV}")` appears in three classes, and `application.yaml:76` sets `${RWB_ENVIRONMENT:DEV}`.
- H3: `.gitlab-ci.yml` `backend-unit` runs `test recoveryCoverageReport` only.

## High

| ID | Story | Where | Finding | Smallest fix |
|---|---|---|---|---|
| H1 | E1-042 | `casewf/config/ParameterLoadHandlerImpl.java:192-211, 243-260`; `ParameterValueEntity.java:63-64` | Two different loads for the same key and environment, with different valid-from dates, can be approved at the same moment. Each approval checks "no approved row on or after this date" (`countApprovedFrom`) but locks only its own rows, so both commit. `ParameterValidity.recompute` then rewrites `valid_to` on the shared rows in both transactions, and `version` is not `@Version`, so the validity history can end up wrong. Rollback running alongside an approval has the same race. Reads stay correct, because `inForce` picks the latest valid-from. The concurrency IT covers only two approvals of the *same* load | At the start of approve and rollback, take `pg_advisory_xact_lock` on each (key, environment), in sorted order |
| H2 | E1-042 | `application.yaml:76`; `ParameterServiceImpl:41`, `ParameterCatalogController:45`, `ParameterStartupCheck:50` | If `RWB_ENVIRONMENT` is unset in production, the service silently serves DEV parameter values. A wrong-case value such as `prod` serves catalog defaults, and readiness reports UP | Remove the defaults. Validate against DEV/SIT/UAT/PROD on a properties record, as `RecoveryMigrationProperties` does for `rwb.schema` |
| H3 | TE-001 | `.gitlab-ci.yml:15`; `build.gradle.kts:363` | The 80% coverage verification task is defined, but no CI job and no `check` dependency runs it | Add `recoveryCoverageVerification` to the `backend-unit` script |
| H4 | TE-002 | `.gitlab/CODEOWNERS` | These paths have no owner line: `access/interim-capability-grants.csv` (decides who may read parameters), `config/parameter-catalog.csv`, `infra/postgres/`, `test/resources/migration-lint/`, `flyway-fixtures/`. The gate sections name only placeholder groups, which the validator reports as WARNING (known: OPEN-038) | Add the missing paths. The placeholder groups stay open under OPEN-038 |

## Medium

| ID | Story | Where | Finding | Smallest fix |
|---|---|---|---|---|
| M1 | E1-042/E1-044 | `.gitlab-ci.yml:57-62` | The database ITs run only when `db/**`, `RecoveryFlywayConfig.java` or `infra/postgres` change, not when `casewf/config` or `casewf/migration` Java changes | Add those paths to `changes` |
| M2 | E1-042 | `parameter-catalog.csv:3-5,18`; `ParameterLoadValidator.withinRange:152` | Four numeric parameters (two cache TTLs, an export limit, a retention period) have no bounds, so 0 or a negative value can be loaded | Give the rows min 1 and a max (a catalog change, so it needs the next migration) |
| M3 | E1-042 | `ParameterCache.java:55-58` | The cache read-then-put is not atomic. Invalidation is per pod. The same mutable JPA entities are handed to every thread | Cache immutable records. Use `compute` or a generation counter. Document the cross-pod TTL |
| M4 | E1-042 | `ParameterLoadHandlerImpl.java:261`; `ParameterLoadRolledBack.java` | The rollback event is published inside the transaction and has no listener. Its Javadoc claims it is handled after commit | Delete the event, or publish it after commit |
| M5 | E1-042 | `InterimVersionDecisionRecorder.java:27`; rollback | Rollback writes no decision record (AGENTS 3.4). The approval record is a log line written before commit | Call the recorder in rollback. Note the interim gap against RWB-E1-008 |
| M6 | E1-042 | `ParameterStartupCheck.java:79,98-102` | A database outage is reported as missing parameters, and a WARN line is logged for every key on every probe | Report database-unavailable separately. Log only when the state changes |
| M7 | E1-042 | `ParameterLoadValidator.java:53-103` | The `{check}` placeholder text is English built in code, and is substituted into the Thai message too (AGENTS 3.6) | Use message-table wording |
| M8 | E1-042 | `magic-number-baseline.csv:16-17` | The baseline allows the literals `rwb-recovery` and `rwb-platform`, which equal loadable catalog parameters (AGENTS 3.2) | Read the values through `CatalogParameterReader`, or mark the keys "not yet consumed" |
| M9 | E1-042 | `ParameterCacheTest.java:91-95` | The test for the TTL recursion guard cannot fail on the guard | Build the service so that it calls back into the same cache instance |
| M10 | E1-044 | `infra/postgres/init/20-grants.sql.inc:16-18` | `SET ROLE ace_view_owner` gives the migrator read access to ACE public tables. The comment understates this (D-RUN-14) | Correct the comment. Record the risk under OPEN-051 |
| M11 | hardening `e566360` | `frontend/e2e/platform.spec.ts:17-20` | `page.goto("/recovery/platform")` after sign-in could hide a redirect bug (AGENTS 4.5) | Find the root cause in the mock sign-in, or assert the URL after the callback |

## Low

| ID | Finding |
|---|---|
| L1 | Dead or speculative code: `ParameterValueRepository.approved(key, env, productGroup)`; the product-group branch in `ParameterServiceImpl.resolve`; `ParameterService.get(key, productGroup, date)` and `entry()` have no production caller; the PRODUCT check is repeated |
| L2 | Defensive code for cases that cannot happen: `cause.getCause() == cause`; the `afterCommit` no-transaction branch; `statusOf` warn-and-continue; the repeated null test in `ParameterStartupCheck:105` |
| L3 | `InterimBusinessDateProvider` Javadoc says "configured time zone", but `Asia/Bangkok` is hard-coded and repeated |
| L4 | `ParameterCatalogController` environment list is a literal. An invalid environment gets the wrong MSG-GEN-002 wording ("between DEV and PROD") |
| L5 | `InterimCapabilityCheck:50` checks only the first letter of a right, and has its own CSV split |
| L6 | `ParameterContentHash` canonical form `key|env|value` is ambiguous when a value contains `|` or a newline |
| L7 | Any `DataIntegrityViolationException` becomes 409. `maxVersionNo` runs per row. `save()` on an assigned UUID costs an extra SELECT |
| L8 | V0001: `uk_parameter_value` is ineffective for null `product_group` (the partial index does the work); there is no index for `findByContent`; the seeded APPROVED rows have a null approver |
| L9 | The `build.gradle.kts` generator validates the trimmed value but generates code from the untrimmed one |
| L10 | Older controllers moved by TE-001 use literal role names or `isAuthenticated()` instead of capability checks |
| L11 | The codeowners tests run twice in CI |

## Good (not to be churned)

1. Maker-checker is enforced in code and by the database CHECK constraint. The partial unique index with a narrow conflict mapping gives a clean 409.
2. The concurrency tests use latches and barriers, not sleeps. Identical loads are serialised with an advisory lock.
3. CSV upload is strict UTF-8 with one RFC 4180 reader, and it has tests.
4. The problem handler never logs cause text. Message IDs exist in English and Thai. The 503 response carries a status only.
5. The migration is forward-only, has the `-- Story:` header, uses the schema placeholder, guards its constraints by name and ends with a self-check.
6. Parameter keys are generated from the catalog. Drift tests compare the CSV, the migration and the code.
7. Module boundaries are checked by ArchUnit, Modulith and ESLint, with fixtures that must fail.
8. The CODEOWNERS validator fails closed, normalises paths and keeps them inside the repository root.

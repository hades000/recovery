# Deviations introduced by the pre-merge review fixes

Run `INC-003-epic-1-RWB-E1-042`, commit `8e51eb8`. These are added to `../deviations.md` (DEV-01..12);
none weakens a gate, and each is a fix the reviews asked for.

| ID | Item | What the code does | Why | Effect |
|---|---|---|---|---|
| DEV-13 | No native query in main code (security review "checked and clean") | `ParameterValueRepository.lockContent` is a `nativeQuery` calling `pg_advisory_xact_lock(hashtext(:key))` with a bound parameter | Ponytail Must 1's reload and Should 3's 409 need two identical loads to be serialised; the unique index alone let a second load pick a different version number. A transaction-scoped advisory lock is the only way to serialise on a value that has no unique constraint | PostgreSQL-only, which the story already is; the argument is bound, never formatted |
| DEV-14 | `GET /admin/parameters` documents 401/403/503 only | An `environment` outside DEV/SIT/UAT/PROD answers **422 MSG-GEN-002** before any read | SEC-042-01: an unvalidated value becomes a cache key. MSG-GEN-002 is in the E422 message set; the OpenAPI delta is requested in `shared-updates.md` (it belongs with OI-E1-042-011 already open) | Contract delta for the API owner, no value served |
| DEV-15 | §7.1 lists eleven credential substrings | The rule also refuses `connection-string`, `connectionstring`, `pwd`, `accountkey`, `passphrase`, `sas-token` | SEC-042-03: `rwb.blob.connection-string` carries `AccountKey=`. The spec is read-only; the widened list is recorded for the document owner | A false positive is fixed by renaming the property, as §7.1 already says |
| DEV-16 | TASK-22's `readinessIsUpOnTheSeededCatalog` | Replaced by a real assertion on the `parameterCatalog` indicator **and** the readiness group, UP and DOWN | Ponytail Should 5: the old helper ran `SELECT now()` | TC-32's system half is now covered |
| DEV-17 | TASK-20: TC-22 asserts the flag-off GET is 404 | The status is asserted; the `MSG-P4-003` body is not | The flag-off refusal body for `PARAMETER` is RWB-E1-043's branch (D-RUN-10, E43S SPEC-018/-026); an unmapped path in this context answers Boot's empty 404 | The guardrail (handler and endpoint absent) is proven; the body stays E43S's contract |
| DEV-18 | The generator reads only the fixed catalog path | It also accepts `-PparameterCatalog=<path>` | SEC-042-02 needs a negative test; without a new dependency (no Gradle TestKit) the only way to prove the guard is to run the task against a bad fixture | A build property, default unchanged |

## Test-count note

The review fixes add 7 unit tests and 5 system tests (including the three `FlagOff` cases): 377 → 384
unit, 46 → 54 container.

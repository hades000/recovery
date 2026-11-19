# TASK-25 scope, guardrail and evidence check

Run `INC-003-epic-1-RWB-E1-042`. Checked on the branch `feature/RWB-E1-042-parameter-catalog` against
`develop-recovery` at `7bee04d`.

| # | Check | Result |
|---|---|---|
| 1 | The diff touches only the plan's file scope | **Pass, with the recorded exceptions in `deviations.md`**: main Java of `casewf/config`, `casewf/config/api`, the three `access/api` additions, the two `access/internal` additions and the three changed `access` classes; the two main CSV resources, the one migration, the two `application*.yaml`; test sources (new) plus `RecoveryBoundaryTest`, `ApiExceptionHandlerTest` and `ModuleMapLoaderTest` (DEV-05); test resources (`recovery-modules.yaml`, `magic-number-baseline.csv`, the `parameter-checks` corpus); `backend/build.gradle.kts`. **Not created**: `ParameterCatalogEntity` and `ParameterCatalogRepository` (DEV-01). No change under `api/**`, `frontend/**`, `.gitlab-ci.yml`, `scripts/dev.ps1`, `docker-compose.yml`, `backend/Dockerfile` or `infra/**`. |
| 2 | No new dependency | Pass: the diff of `backend/build.gradle.kts` adds no `implementation`, `testImplementation` or `runtimeOnly` line (only the generator task, the generated `srcDir`, the `compileJava` dependency and `parameterToolingClasses`). |
| 3 | Exactly one migration, line 1 `-- Story: RWB-E1-042`, no number fixed elsewhere | Pass: one file; the plan and this evidence call `<seq>` unfixed; `${recoverySchema}` is the only qualifier; no `SET search_path`, no `GRANT`, no `REVOKE`. |
| 4 | No secret value and no user ID in a table, log line, event payload, exception message or response | Pass: no UUID literal in `backend/src/main/java` or `src/main/resources`; `password` appears only as a key name or a property name; `ace.db.password` is seeded with no default and no value row; the recorder line carries load ID, table, keys, date and code only. |
| 5 | No out-of-scope work | Pass: no reference-load controller, no `/verify`, no dispatch branch, no access-log filter, no product parameter service, no flag table, no screen, no change checklist, no decision-log writer, no outbox, no permission matrix, no Temporal or Drools read. |
| 6 | `ParameterLoadHandlerImpl` implements no `access.api` type; no `PARAMETER` SPI bean | Pass: it implements `casewf.config.api.ParameterLoadHandler` only. The flag-off contract for `PARAMETER` stays RWB-E1-043's. |
| 7 | The merged RWB-TE-001 artefacts change additively | Pass: `config.api` added to the module map; T-TE001-14's expected sets extended; `ApiProblemException`'s constructor added with its rendering; `ModuleMapLoaderTest` gains the same map entry (DEV-05). Nothing removed, no assertion relaxed. |
| 8 | Results table per surface | `implement/unit-tests/report.md`: backend `PASS` with the four counters; frontend `NOT_APPLICABLE` with the story evidence. |

## Guardrails re-checked in code

- No business value in code: the catalog is the only source; `ParameterSchemaLimits` names the two schema
  widths and both are in the baseline; the baseline holds only protocol literals, map/AES sizes, the two
  Temporal strings and the CSV column indices.
- No PII: every test identity is a synthetic UUID (`…b001`, `…b002`, `…b003`, `…a001`, `…a002`); no
  name, ID number, account number or address appears in code, fixtures, logs or evidence.
- No direct ACE `public` read: only `${recoverySchema}` DDL and the two new tables.
- One module: recovery only (D-RUN-21); `casewf.config` and `access` are nested design modules.

## Verification commands at this commit

> **Superseded figures** (TASK-22 run, before the pre-merge reviews). The figures of record are at tip
> `25c8f94`: see `implementation-report.md` "Results" and `code-gate-fix/README.md`.

```text
./gradlew test                                  exit 0   377 tests
./gradlew test recoveryCoverageVerification     exit 0   LINE 90.7 % INSTRUCTION 90.3 % BRANCH 81.0 % METHOD 94.9 %
./gradlew recoveryIntegrationTest               exit 0   46 tests (24 + 4 + 12 + 6)
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/dev.ps1 test   exit 0
```

Logs: `backend/coverage.log`, `backend/it.log`, `merge-gate.log`, `backend/task-*.log`.

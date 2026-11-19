# Implementation report — RWB-E1-042 central configuration service and parameter catalog

> Orchestrator note (19 Nov 2026, REVIEW-001 L-06): this is the first, shorter implementation report. The
> complete record, including the code-gate remediation rounds, is `implementation-report.md` in this folder.
> The branch was merged at `0b87102` on 18 Nov 2026 20:46; any "not merged" text below is as of writing.

Run `INC-003-epic-1-RWB-E1-042` · Stage `implement` · Branch `feature/RWB-E1-042-parameter-catalog`
Worktree `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-E1-042`
Base `develop-recovery` at `7bee04d` (RWB-TE-001 and RWB-E1-044 merged).

> **Superseded** by `implementation-report.md`. The counts below are the TASK-22 run before the
> pre-merge reviews; the figures of record are at tip `25c8f94` (`code-gate-fix/README.md`).

```text
IMPLEMENTATION_STATUS_SUMMARY: SUCCESS — 26 tasks (TASK-00..TASK-25) executed on one worktree; the catalog file, its two build checks, the generated typed keys, the published P3 and P4 surface, the problem and message seams, one guarded migration with 19 catalog rows and 40 value rows, the read service with its cache, the catalog endpoint and readiness, the load/approve/rollback handler, the flag, the coverage wiring and the gates.
IMPLEMENTATION_STATUS_DETAIL: SUCCESS [REASON: spec revision 13 and plan v2 followed task by task; 377 unit and build-check tests green; coverage 90.7 % LINE, 81.0 % BRANCH, 94.9 % METHOD, 90.3 % INSTRUCTION on the merged BUNDLE rule; 46 container tests green; dev.ps1 test exits 0] [UNBLOCK_ACTION: n/a]
IMPLEMENTATION_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 25 carried from the spec, none blocking; TC-E1-042-12 stays Blocked by OI-E1-042-001] [UNBLOCK_ACTION: n/a]
IMPLEMENTATION_DESIGN_SOURCE: NOT_REQUIRED [NOTE: UI In Scope NO; 0 screens; no Figma link]
FRONTEND_STATUS: NOT_APPLICABLE
BACKEND_STATUS: REQUIRED — PASS
GATE_REVIEW: PENDING_ORCHESTRATOR
STATUS: SUCCESS
NEXT_STEP: Human review of implementation evidence, then manually start API Tester with RUN_ID=INC-003-epic-1-RWB-E1-042
```

## Commits on `feature/RWB-E1-042-parameter-catalog`

| SHA | Subject |
|---|---|
| `b038730` | catalog file, CSV reader and the two build-check tooling classes |
| `bf2ddcd` | completeness and magic-number build checks with the reviewed baseline |
| `203028f` | generated typed keys and the published config.api and access.api surface |
| `11cd8ce` | problem forms, message catalogue and the interim capability seam |
| `dd4ad63` | one guarded migration for the parameter catalog and its seed |
| `5ad5594` | parameter read service, cache, readiness, catalog endpoint and P4 reader |
| `5777d4f` | load, approve and rollback handler with the decision recorder and cache refresh |
| `1ffb659` | system suite, coverage wiring and the full container suite |

## Migration

`backend/src/main/resources/db/modulemigration/recovery/V0001__rwb_e1_042_parameter_catalog_and_seed.sql`

Line 1 `-- Story: RWB-E1-042`. **`<seq>` is not fixed** (D-RUN-07): `V0001` is the next free number in
this branch, because the folder held only `README.md`; the orchestrator assigns the merge number. One
file for the story: both tables exactly as Physical Schema v6 lines 1386-1434, the three added columns,
the guarded constraints, the four indexes, the comments, the 19 catalog rows and the 40 approved value
rows, then the self-check block. `${recoverySchema}` is the only qualifier; no `SET search_path`, no
`GRANT`, no `REVOKE`. It is never edited after merge.

## Coverage

`./gradlew test recoveryCoverageVerification` → exit 0. One `BUNDLE` rule, four counters, threshold
0.80: LINE 2543/2803 = 90.7 %, INSTRUCTION 13845/15333 = 90.3 %, BRANCH 1267/1564 = 81.0 %, METHOD
543/572 = 94.9 %. `architecture.parameters` is measured inside the same bundle (TASK-21 case 1: the
merged filter did not take it). Reports: `backend/build/reports/jacoco/recoveryCoverageReport.xml`
and its HTML. Frontend `NOT_APPLICABLE`.

## What was built (by story scope bullet)

| S | Delivered |
|---|---|
| S-1 | `config/parameter-catalog.csv` (19 rows, the 13 pack descriptions verbatim, six D-RCV-36 rows), `CsvRows`, and the two build checks in `architecture/parameters` with their fixtures and the reviewed magic-number baseline |
| S-2 | `ParameterKey<T>`, the `generateParameterKeys` Gradle task, the generated `ParameterKeys` (11 typed constants, `all()`, `byName`) and the drift test |
| S-3 | `casewf.config.api` (11 types, `@NamedInterface(name = "config.api", propagate = false)`), the three `access.api` types, the module map entry and the extended published-surface test |
| S-4 | `ApiProblemException`'s status-and-message-ID form, its rendering and one safe WARN line, `FixedMessageCatalog` (nine IDs, EN + TH verbatim), `InterimCapabilityCheck` over the 37 RW- roles' "Rules and parameters" rights |
| S-5 | The one migration above, with the self-check block |
| S-6 | `ParameterServiceImpl`, `ParameterValues`, `ParameterCache`, `CatalogParameterReaderImpl`, `InterimBusinessDateProvider` |
| S-7 | `GET /api/recovery/v1/admin/parameters` with its four filters and the method check, the status-only 503, and the `parameterCatalog` readiness indicator |
| S-8 | `ParameterLoadValidator` (twelve checks), `ParameterContentHash`, `ParameterValidity`, `ParameterLoadHandlerImpl` with its own transactions, maker-checker and the refusals |
| S-9 | `ParameterVersionApproved` and `ParameterLoadRolledBack`, the after-commit cache rebuild, `VersionDecisionRecorder` + `InterimVersionDecisionRecorder` (see DEV-08) |
| S-10 | `rwb.p3.configservice` in both YAML files, `@ConditionalOnProperty` on the handler and the controller, `@Value` in the two always-registered beans |
| S-11 | No secret stored or served, no user ID in a log line, event, exception or response; `AC-VERS` written inside the approval transaction |
| S-12 | The tooling in the combined bundle, the unit gate, the container suite |
| S-13 | `dev.ps1 test` exit 0, scope and guardrail check, no new dependency, no file outside the list except as recorded in `deviations.md` |

## Files

89 files changed against `7bee04d` (+7555/−19): the main Java of `casewf.config` and `casewf.config.api`,
the three `access.api` additions, the two `access.internal` additions and the three changed
`access` classes, the two main CSV resources, the migration, the two YAML files, `backend/build.gradle.kts`,
the test sources and resources, and the two merged-test extensions recorded in `deviations.md`.

## Not done, and why

- TC-E1-042-12 (live RW-PHONECOL identity and PM-2026.11) stays **Blocked** by RWB-E1-022 and
  RWB-E1-037; the seam it covers is tested. It is never reported as passed.
- No OpenAPI change, no frontend change, no controller for the three load operations (D-RUN-10), no
  `PARAMETER` SPI bean (D-RUN-20), no new dependency, no schema change outside the one migration.

# Shared updates this story asks the orchestrator to apply

Run `INC-003-epic-1-RWB-E1-042`. Written per RUN-BRIEF rule 3: the orchestrator applies these rows in
order; this stage does not edit the shared files.

## 1. `aisdlc/docs/open-items.md`

| ID | Owner | Raised by | Item | Default if unanswered |
|---|---|---|---|---|
| OI-E1-042-012 | Platform owner (RWB-TE-001/TE-003) | RWB-E1-042 implementation | Spring Modulith's persistent event-publication registry writes `recovery.event_publication`, which Physical Schema v6 does not create. Either a platform migration adds it, or the registry stays off and cache refresh uses a transaction synchronization (what this story does) | Registry stays off; the after-commit synchronization is the pattern |
| OI-E1-042-013 | Recovery tech lead | RWB-E1-042 implementation | Spring Modulith 2.1.1 does not surface `@NamedInterface` on `casewf.config.api` (a nested sub-package). The module map is the source of published packages; confirm that the map entry plus the annotation is sufficient evidence | Yes, sufficient |

## 2. `aisdlc/requirement/Traceability_Matrix.md`

| Story | SPEC | Code | Test |
|---|---|---|---|
| RWB-E1-042 | SPEC-001..-027 | `implementation-builder/implement/traceability.md` (CODE-01..CODE-30) | `implement/unit-tests/report.md` |

## 3. `aisdlc/docs/increments/INDEX.md`

RWB-E1-042 implemented on `feature/RWB-E1-042-parameter-catalog`; merge pending the orchestrator; one
migration `V0001__rwb_e1_042_parameter_catalog_and_seed.sql` whose `<seq>` the orchestrator assigns at
merge (D-RUN-07).

## 4. For later stories

| Story | Row |
|---|---|
| RWB-E1-043 | `casewf.config.api.ParameterLoadHandler` is the PARAMETER branch (D-RUN-10, D-RUN-20). `load`, `approve`, `rollback` and `find` refuse with `access.api.ApiProblemException` — render it unchanged. `TABLE = "PARAMETER"`. |
| RWB-E1-043 | `ParameterLoadResult.repeat` has no API v4 field; the flag stays internal (OI-E1-042-011). |
| RWB-E1-037 | `CapabilityCheck` is published at `access.api`; the bean name `capabilityCheck` must survive; `backend/src/main/resources/access/interim-capability-grants.csv` is deleted by that story. |
| RWB-E1-037 | The two-argument `CatalogParameterReader.get(String, Class)` takes the business date from the provider inside P3, so a P4 caller passes no date (D-RUN-19, SPEC-023). |
| RWB-TE-003 | `ApiExceptionHandler.problem` now has a null-`error()` branch that renders the message-ID form through `ProblemFactory` and logs one safe WARN line (message ID or `none`, status, `traceId`, cause class, "cause suppressed"). Its own D-RUN-15 work should keep that branch. |
| RWB-TE-006 | `ParameterVersionApproved` and `ParameterLoadRolledBack` are in-process only today; the outbox takes them over. |
| RWB-E1-045 | `ENTRY_DPD`, `EXCLUSION_LIST`, `NOTICE_PERIOD_DAYS`, `CURE_PERIOD_DAYS` and `EXPOSURE_BAND_SET` are PRODUCT keys with no value rows; a PRODUCT read refuses with `ParameterNotInForceException`. |
| RWB-E1-001 | `parameter_catalog` is created and seeded by this story's migration; RWB-E1-001's dictionary describes it and does not create it (D-RUN-12). |
| RWB-TE-002 | The new files are under `th/co/scb/ace/demo/recovery/casewf/config/**`, `casewf/config/api/**` and `access/**`; the CODEOWNERS paths should cover them with the recovery module. |

## 5. Added by the pre-merge review fixes (commit 8e51eb8)

| Story / owner | Row |
|---|---|
| API owner (OI-E1-042-011) | `GET /api/recovery/v1/admin/parameters` now answers **422 MSG-GEN-002** (`field=environment`, `min=DEV`, `max=PROD`) for an `environment` outside DEV/SIT/UAT/PROD (SEC-042-01). The OpenAPI must document the query parameter as an enum and add the 422 to the operation. |
| Document owner (Error and Message Standard / spec §7.1) | The credential-name rule now also refuses `connection-string`, `connectionstring`, `pwd`, `accountkey`, `passphrase` and `sas-token`; `rwb.blob.connection-string` is the property that motivated it (SEC-042-03). §7.1 still lists eleven substrings. |
| RWB-TE-003 | `ParameterVersionApproved` is now published **after commit** (SEC-042-04). A listener may assume the approval is durable. `ParameterLoadRolledBack` is still published inside the rollback transaction and observed after commit, which is what TC-10(b) forces. |
| Platform owner | `ParameterValueRepository.lockContent` takes a PostgreSQL advisory lock (`pg_advisory_xact_lock(hashtext(author-supplied? no: content hash)`)) inside the load transaction, so two identical loads serialise. Any port away from PostgreSQL must replace it. |
| RWB-E1-043 | An identical repeat is now decided **inside** the load transaction under that lock; the `repeat` flag is unchanged. |
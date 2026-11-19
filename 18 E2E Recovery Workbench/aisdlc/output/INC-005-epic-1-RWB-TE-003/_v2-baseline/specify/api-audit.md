# API audit — API Specification v4 (input to RWB-TE-003)

Source: `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml`
(OpenAPI 3.1.0, version 4.0.0). Audited 2026-11-17 for the RWB-TE-003 specification.

## Counts

| Measure | Value |
|---|---:|
| Operations (`operationId`) | 141 |
| E1 | 73 |
| E2 | 38 |
| E3 | 8 |
| E4 | 10 |
| E5 | 8 |
| E6 | 4 |
| Tags | 16 |
| Schemas | 172 |
| `$ref` values | 903 |

The story narrative says 79 operations; that is the count at its 28 October 2026 authoring. The suite
reads the file and selects by `rwb.release`; the E1 build selects 73.

## BR2 lint pre-check

| Check | Result |
|---|---|
| `operationId` present and unique | PASS — 141/141, 0 duplicates |
| `x-module` present | PASS — 141/141; modules are P1–P10 and S1–S9 |
| `x-capability.area` and `right` present | PASS with exception — 139 with a capability area, 2 with `area: None` |
| `x-first-release` present and in E1–E6 | PASS — 141/141 |
| At least one 4xx/5xx response | PASS — 141/141 |
| Error response resolves to `Problem` | PASS — `components.responses.E4xx/E5xx` all use `application/problem+json` + `Problem` |
| `$ref` resolves | PASS — 0 unresolved |

## Authentication-only operations

| Operation | Method | Path | Capability |
|---|---|---|---|
| `getFeatureFlags` | GET | `/feature-flags` | `area: None`, `right: R` |
| `getMeSession` | GET | `/me/session` | `area: None`, `right: R` |

`ASM-TE003-09` and `CLAR-009` treat these as authentication-only: the access suite records
`NOT_APPLICABLE_AUTHENTICATED` and tests 401 without a session. `OPEN-042` asks the API owner to confirm
or assign a real capability area. They are not recorded as a 403 pass.

## Contract examples used by the story

| Operation | Release | Capability | Used by |
|---|---|---|---|
| `getCasesCaseidTimers` | E1 | Case record R | AC2, AC4, AC8 fixture |
| `postQueuesQueueidPlacements` | E2 | Queue and allocation C | AC6 pending fixture |
| `getAdminJobs` | E1 | Platform administration R | AC5 no-implementation fixture |
| `warnAt` in `Timer` | — | — | AC1; already present in v4 line 6602 |
| `legalHold` in `Case` | — | — | AC7; present in v4 and removed only in the fixture |

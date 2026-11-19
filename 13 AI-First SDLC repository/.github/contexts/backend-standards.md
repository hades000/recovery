---
title: "Backend standards for the new module (USER-PROVIDED)"
description: "Squad decisions for backend work on ACE that cannot be read from the code; Context Builder incorporates them into backend-context.md"
---

Status: Draft, owner FDA. Every row is `USER-PROVIDED`. Rows marked **TBD** are open decisions:
agents must not fill them in and must raise them as open items when a story depends on them.

ACE rules still apply and are not repeated here: `ace-monorepo/AGENTS.md`,
`ace-monorepo/backend/AGENTS.md`, `ace-monorepo/docs/coding-standard.md` (Spring Data REST with HAL,
entities identified by URI, OpenAPI types to the front end, `AceException` errors, BDD and e2e tests).
Where this file and the ACE rules disagree, the ACE rules win until the FDA records an exception here.

## BS-1 Module structure (Spring Modulith)

| ID | Standard |
|---|---|
| BS-1.1 | New capability is one Spring Modulith application module under `th.co.scb.ace.demo.<module>`, declared with `@ApplicationModule` in `package-info.java`. Module name: **`recovery`** → `th.co.scb.ace.demo.recovery` (D-RCV-02) |
| BS-1.2 | The 19 design modules (P1–P10, S1–S9) are **nested application modules** inside `recovery` (for example `recovery.casewf`, `recovery.decision`, `recovery.integration`), each with an `api` package (published: interfaces, DTOs, events; `@NamedInterface`) and an `internal` package; extra published packages (for example `decision.writer`) only where the RWB-TE-001 module map lists them. Package names come from the module map (D-RCV-02) |
| BS-1.3 | Modules talk to each other only through another module's `api` package or through application events (`@ApplicationModuleListener`); never through another module's entity, repository or table |
| BS-1.4 | Boundaries are tested in every build by unit tests, not by pipeline stages (D-RCV-05): `ApplicationModules.of(DemoApplication.class).verify()` (existing `ModulithTest`) plus the RWB-TE-001 rules as JUnit tests. Extra test libraries (for example ArchUnit) need plan approval |
| BS-1.5 | Existing ACE packages (`controller`, `service`, `model`, ...) are not extended for the new module; new code lives in the module package |

## BS-2 Database and migrations

| ID | Standard |
|---|---|
| BS-2.1 | Each module owns its tables and migrations in `backend/src/main/resources/db/modulemigration/<module>/`, run by the module's own Flyway bean with its own history table `flyway_schema_history_<module>` (pattern: `samplemodule/config/SampleModuleConfig.java` on ACE `develop`) |
| BS-2.2 | DL42 decided by D-RCV-28 (5 November 2026): files named `V<seq>__<story>_<name>.sql`, where `<seq>` is a four-digit sequence taken in merge order (for example `V0001__rwb_e1_001_recovery_schema.sql`). Line 1 is `-- Story: <story key>`. A corrective migration takes the next sequence, keeps the original story key and adds line 2 `-- Fix: <reason>`. The schema is referenced only as `${recoverySchema}`. This supersedes DL42 option A / D-RCV-04. |
| BS-2.3 | Own schema `recovery` for all recovery tables in every environment, never written literally (`${recoverySchema}`), as in Physical Schema v4 (D-RCV-03, D-RCV-17). The value is not `rwb_case`. |
| BS-2.4 | No module reads another module's tables; cross-module data goes through `api` or events (BS-1.3) |
| BS-2.5 | Never run migrations or tests against a shared database; ACE allows Flyway clean in the default profile |
| BS-2.6 | Migration checks (literal schema name, one story key per file, no undo file) run as unit tests in the build, not as a pipeline stage (D-RCV-05, gap report #30–32) |

## BS-3 API

| ID | Standard |
|---|---|
| BS-3.1 | Recovery API follows Recovery Workbench API Specification v2: custom REST controllers, plain JSON, uuid identifiers; no HAL and no Spring Data REST export of recovery entities. Recorded exception to the ACE HAL/URI rule: `docs/architecture/decisions/ADR-RCV-001-recovery-api-style.md` (2026-11-04). OpenAPI types to the frontend still apply |
| BS-3.2 | Base path `/api/recovery/v1` (ADR-RCV-001) |
| BS-3.3 | Error responses use the API specification's error schema with `MSG-*` codes from Error and Message Standard v3 (ADR-RCV-001); how they map onto `AceException` is decided per plan |

## BS-4 Security, privacy and audit

| ID | Standard |
|---|---|
| BS-4.1 | Authentication and roles reuse ACE security (existing `/auth`, IAM user); no separate login for the module. Role names for the module: **TBD** |
| BS-4.2 | Personal data (PDPA) is classified per field (`[PII]`, `[SENSITIVE_FINANCIAL]`, `[CONFIDENTIAL]`, `[PUBLIC]`) in the specification; masking rules by role: **TBD** |
| BS-4.3 | No real customer data in code, tests, fixtures or logs; synthetic data only. Never log personal data or credentials |
| BS-4.4 | Business actions are recorded in the ACE audit log (existing `audit` capability); event list per story |
| BS-4.5 | Secrets come from environment or key store, never from the repository |

## BS-5 Batch and scheduling

| ID | Standard |
|---|---|
| BS-5.1 | Scheduled work uses ACE Quartz; bulk processing uses Spring Batch; jobs are idempotent and restartable |
| BS-5.2 | Calls to external systems go through one integration package per system inside the module, with timeout, retry and fallback stated in the specification |

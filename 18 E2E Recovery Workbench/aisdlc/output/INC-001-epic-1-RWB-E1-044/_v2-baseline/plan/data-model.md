---
title: "Data model — RWB-E1-044"
run_id: "INC-001-epic-1-RWB-E1-044"
story: "RWB-E1-044"
---

# Data model — RWB-E1-044

No JPA entity, repository, table definition or production migration file in this story (SPEC-006, §13 step 2). The models below are the Flyway history table, the migration-file convention, the activation rules, the message parameters and the test fixtures.

## 1. `flyway_schema_history_recovery` (schema `ace`, Flyway-managed)

Created by Flyway on the first recovery migrate (D-RCV-47, -48); never written by a migration or by hand. Standard Flyway 12 history columns:

| Column | Meaning in this story |
|---|---|
| `installed_rank` | Order of application |
| `version` | `0` for the baseline row (non-empty `ace`, first run only); `0001..N` for recovery files |
| `description`, `type`, `script` | From the file name; baseline row has type `BASELINE` |
| `checksum` | Validated on every migrate (`validateOnMigrate(true)`) |
| `installed_by`, `installed_on`, `execution_time` | Run evidence until the job monitor exists (SPEC-013) |
| `success` | `false` never persists on PostgreSQL (per-migration transaction rolls back, SPEC-010) |

Holds recovery versions only. ACE core `flyway_schema_history` and `flyway_schema_history_samplemodule` are untouched (T-044-16).

## 2. Migration file convention (CON-RWB-E1-044-002)

| Element | Rule |
|---|---|
| Folder | `backend/src/main/resources/db/modulemigration/recovery/` (created by the first migration story; none here) |
| Name | `^V[0-9]{4}__rwb_(e[0-9]+\|te)_[0-9]{3}_[a-z0-9_]+\.sql$`; `<seq>` unique, contiguous `0001..N` |
| Line 1 | `-- Story: <KEY>`, `<KEY>` `^RWB-(E[0-9]+\|TE)-[0-9]{3}$`; equals the name's `<story>` part in upper case with dashes; exactly one per file |
| Line 2 (fix only) | `-- Fix: <non-empty reason>`; needs one non-fix file of the same key with a lower `<seq>` |
| Per key | At most one non-fix file |
| Forbidden files | `R__*.sql`; any file starting `U`/`u` and ending `.sql` |
| Object names | Unqualified; every table, sequence and index identifier starts with `rwb_` (case-insensitive after removing double quotes); positions per SPEC-007 (5) |
| Forbidden statements | Schema qualifier (except `information_schema`/`pg_catalog` reads), qualified types, statements naming a schema, `SET search_path`, `GRANT`, `REVOKE`, `ALTER DEFAULT PRIVILEGES`; also inside dollar-quoted bodies |

## 3. Activation truth table (`RecoveryFlywayCondition`, runner, initializer)

`PG` = `spring.datasource.url` starts with `jdbc:postgresql:`. `MAE` = `recovery.flyway.migrate-and-exit=true`. `FE` = `spring.flyway.enabled=true`. `DBM` = profile `db-migrate` active. `DBMR` = profile `db-migrate-recovery` active.

`recoveryFlyway` exists ⇔ `PG ∧ (DBMR ∨ (FE ∧ ¬DBM))`. Initializer exists ⇔ `PG ∧ FE ∧ ¬DBM`. Runner exists ⇔ `DBMR`; it migrates only when `MAE` and the bean exist, otherwise it fails fast. Activation is keyed on profiles, not on `MAE`, so `MAE` set from an environment variable, system property or `.env` in the core `db-migrate` step creates nothing (D-RCV-45; plan gate REVIEW-RWB-E1-044-028).

| Case | Profiles | `FE` | `MAE` | URL | `recoveryFlyway` | Initializer | Runner | Test |
|---|---|---|---|---|---|---|---|---|
| ACE default / ACE tests | — | true | — | H2 | no (INFO skip line) | no | no | T-044-11, P-044-03 |
| Local developer, PostgreSQL | — | true | — | PG | yes | yes, after core when present | no | P-044-01, P-044-03 |
| Deployed pods | `scb-aks` | false | — | PG | no | no | no | P-044-03 |
| Core Jenkins step | `db-migrate` | true | — | PG | no (D-RCV-45) | no | no | T-044-15, P-044-03 |
| Core Jenkins step with stray switch | `db-migrate` | true | true | PG | no (D-RCV-45) | no | no | P-044-03 |
| Recovery Jenkins step | `db-migrate,db-migrate-recovery` | false | true | PG | yes | no | yes: migrate, exit 0 / 1 | T-044-12, P-044-03, P-044-04 |
| Recovery step misconfigured: data source | `db-migrate,db-migrate-recovery` | false | true | not PG / missing | no | no | yes: ERROR `object=recoveryFlyway`, exit 1, no migrate | T-044-12, P-044-04 |
| Recovery step misconfigured: switch overridden | `db-migrate,db-migrate-recovery` | false | false / absent | PG | yes | no | yes: ERROR `object=recoveryFlyway` (reason names the switch), exit 1, no migrate | P-044-04 |

## 4. `MSG-P3-016` parameters (SPEC-018, CLAR-004 A)

| Source | `schema` | `object` | Extra |
|---|---|---|---|
| Recovery migrate failure (checksum, failed migration, missing schema) | `currentSchema` parsed from the JDBC URL string given to `migrateOrReport` (`spring.datasource.url`, or the test's URL); omitted if the URL has none; no connection opened | Flyway version, or `recoveryFlyway` | Flyway reason |
| Runner fail-fast (no bean / not PG / switch not `true`) | as above if available | `recoveryFlyway` | — |
| Lint failure | omitted | `file` or `file:line` | rule code |
| Schema comparison | connection schema | `<schema object>` (e.g. `rwb_x.c`) | extra / missing |
| Refused clean | — | — | Flyway's own message (D-RCV-28 (4)) |

No message text in code or resources; no URL host, user or password in a log line.

## 5. Lint fixture matrix (`src/test/resources/recovery-migration-lint/<case>/`)

One fixture file per case; the file name is valid unless the case tests the name. Forbidden ⇒ one failure with file, line, rule; allowed ⇒ no failure.

| Group | Forbidden (fail) | Allowed (pass) |
|---|---|---|
| Schema (SPEC-007 (1)–(4)) | `ace.rwb_x`, `"ace".rwb_x`, `public.rwb_x`, `${recoverySchema}.rwb_x`, `::ace.rwb_t`, `CAST(.. AS ace.rwb_t)`, `CREATE SCHEMA rwb`, `SET search_path`, `COMMENT ON COLUMN ace.rwb_x.c` | `information_schema.x`, `pg_catalog.pg_class`, commented-out `ace.x`, `'ace.efs_account'` in a literal (accepted gap) |
| Prefix, DDL names | `CREATE TABLE case_x`, `CREATE SEQUENCE case_seq`, `CREATE INDEX idx_x ON rwb_t`, `CONSTRAINT pk_x PRIMARY KEY`, `ALTER TABLE rwb_t RENAME TO t2` | `CREATE TABLE IF NOT EXISTS rwb_case`, `CREATE TABLE "RWB_Case"`, `CREATE SEQUENCE rwb_case_seq`, `CREATE UNIQUE INDEX rwb_case_ix1 ON rwb_case`, `CONSTRAINT rwb_case_pk PRIMARY KEY`, `CREATE TABLE rwb_x (id bigserial PRIMARY KEY)` |
| Prefix, targets and references | `ALTER TABLE efs_account …`, `REFERENCES cfsc_case(id)`, `INSERT INTO staff_x`, `DROP TABLE sample_model`, `ALTER SEQUENCE efs_seq RESTART`, `ALTER INDEX efs_ix SET TABLESPACE t`, `ALTER TABLE efs_x OWNER TO r`, `CREATE TRIGGER rwb_tg … ON efs_x`, `CREATE POLICY p ON efs_x`, `LOCK TABLE efs_x`, `COMMENT ON TABLE efs_x`, `COMMENT ON INDEX efs_ix`, `COMMENT ON COLUMN efs_x.c`, `CREATE TABLE rwb_x (LIKE efs_y)`, `nextval('efs_seq')`, `'efs_seq'::regclass` | `REFERENCES rwb_case(id)`, `nextval('rwb_case_seq')`, `CREATE TRIGGER rwb_tg … ON rwb_x`, `COMMENT ON COLUMN rwb_x.c`, `CREATE VIEW v_x AS SELECT * FROM rwb_y` (view name: accepted gap) |
| Prefix, relations | `INSERT INTO rwb_x SELECT * FROM efs_account`, `SELECT … FROM rwb_x JOIN efs_account`, `UPDATE rwb_x SET … FROM efs_y`, `DELETE FROM rwb_x USING efs_y`, `CREATE TABLE rwb_x AS SELECT * FROM efs_y`, `CREATE VIEW rwb_v AS SELECT * FROM efs_y`, `FROM pg_class` (unqualified catalog) | `INSERT INTO rwb_x SELECT … FROM rwb_y JOIN rwb_z`, `WITH c AS (SELECT … FROM rwb_y) SELECT … FROM c`, `FROM generate_series(1, 3)`, `FROM (VALUES (1)) v`, `SELECT rwb_x.c FROM rwb_x` |
| Non-relation `FROM`/`USING` (REVIEW-022) | — | `EXTRACT(YEAR FROM d)`, `SUBSTRING(x FROM 2)`, `TRIM(BOTH FROM x)`, `OVERLAY(x PLACING 'a' FROM 2)`, `a IS DISTINCT FROM b`, `a IS NOT DISTINCT FROM b`, `CREATE INDEX rwb_i ON rwb_t USING gin (c)`, `ALTER TABLE rwb_t ALTER COLUMN c TYPE int USING c::int`, `JOIN rwb_y USING (id)` |
| Privileges (SPEC-007 (6)) | `GRANT SELECT ON rwb_x TO r`, `REVOKE ALL ON rwb_x FROM r`, `GRANT USAGE ON SCHEMA ace TO r`, `ALTER DEFAULT PRIVILEGES … GRANT …` | — |
| Dollar-quoted | `DO $$ … ace.rwb_x … $$`, `$fn$ … SET search_path … $fn$`, `$$ … UPDATE efs_account … $$`, `$$ … GRANT … $$` | `DO $$ … UPDATE rwb_x … $$` |
| Headers and keys (SPEC-008) | Two non-fix files one key; fix without base; two `-- Story:` lines; key/name mismatch; bad key | Valid fix pair |
| Names and files (SPEC-009) | `V1__x.sql`, `V0001__x.sql`, duplicate `V0002`, gap `0001,0003`, `R__x.sql`, `U0001__x.sql`, `u0001__x.sql` | Empty folder; missing folder |

## 6. Container migration fixtures (`src/test/resources/recovery-migration-fixtures/<case>/`)

All files: line 1 `-- Story: <KEY>` matching the file's own key (`RWB-E1-999`; `RWB-E1-998` for `V0002__rwb_e1_998_fixture_b.sql`), synthetic DDL, `rwb_` names, no schema, no data rows.

| Case | Files | Used by |
|---|---|---|
| `base` | `V0001__rwb_e1_999_fixture.sql` (`CREATE TABLE rwb_fixture (id bigint PRIMARY KEY, c text NOT NULL)`) | T-044-01, -02, -03, -16, -12, -15, P-044-01 |
| `edited` | `V0001__rwb_e1_999_fixture.sql` with one changed statement | T-044-04 |
| `two` | `base` + `V0002__rwb_e1_998_fixture_b.sql` | T-044-13 (DB at 2, classpath `base`) |
| `failing` | `V0001__rwb_e1_999_fixture.sql`: statement 1 `CREATE TABLE rwb_part …`, statement 2 invalid | T-044-08, T-044-12 failing case |
| `slow` | `V0001__rwb_e1_999_fixture.sql` with `SELECT pg_sleep(2);` then `CREATE TABLE rwb_slow …` | T-044-09 |

Container fixtures are not in the real folder, so the lint's real-folder check does not see them.

## 7. Coverage scope

| Class directory | Filter | Excludes |
|---|---|---|
| `sourceSets.main.output` | `th/co/scb/ace/demo/recovery/**` | — |
| `sourceSets.test.output` (this story) | `th/co/scb/ace/demo/recovery/casewf/internal/migration/**` | `**/*Test.class`, `**/*Test$*.class`, `**/*IT.class`, `**/*IT$*.class` |
| `sourceSets.test.output` (RWB-TE-001) | `th/co/scb/ace/demo/recovery/architecture/**` | `**/*Test.class`, `**/*Test$*.class` |

| Gate | Execution data | Classes | Blocking |
|---|---|---|---|
| Unit (plan gate REVIEW-RWB-E1-044-026, -037, -041) | `test` only (`recoveryIntegrationTest.exec` absent before and after) | Every class under `build/classes/java/main/th/co/scb/ace/demo/recovery/` (selected by directory); a listed class file with no XML `<class>` entry fails the gate unless it has no code (`package-info`, an interface with no method bodies), and those excluded names are printed and saved; lint tooling printed separately for information | Yes, 80% LINE, INSTRUCTION, BRANCH, METHOD |
| Combined (`recoveryCoverageVerification`) | `test` + `recoveryIntegrationTest` | Every class in the class directories above (incl. `SchemaComparator`, `RecoveryPostgres`) | Yes, same thresholds |

---
title: "Test scenarios: RWB-E1-044"
run_id: "INC-001-epic-1-RWB-E1-044"
revision: "v1 (18 Nov 2026): first scenario set for this run, matching plan.md v1 and spec v14-7 Tests section (T-044-01 to T-044-22)."
---

# Test scenarios: RWB-E1-044

Source: `../../specify/spec.md` v14-7 "Tests" and "Restated acceptance criteria"; `../plan.md` v1; `../data-model.md` v1. Test IDs are the spec's (`T-044-*`); fixture folders are `data-model.md` section 3 (lint) and section 4 (Flyway). Commands run in `backend/` unless a script is named.

## 1. Acceptance criteria to test ID

| AC (restated in spec v14-7) | Test IDs | Level | Task |
|---|---|---|---|
| AC1 — a pending migration applies once, version and checksum recorded, a rerun applies nothing | T-044-10 | Container | TASK-14 |
| AC2 — drift between the migration result and a target fails with MSG-P3-016 naming `<schema>.<table>.<column>` | T-044-15 (container), T-044-19 (unit) | Container, unit | TASK-14, TASK-05 |
| AC3 — the same file produces the table in schema `recovery` in two databases; checksums equal | T-044-11 (container), T-044-08 case (5) (unit) | Container, unit | TASK-14, TASK-07 |
| AC4 — an applied migration edited later fails validation with the version, and the service does not start | T-044-12 (container), T-044-09 (unit) | Container, unit | TASK-14, TASK-09 |
| AC5 — a literal schema qualifier fails the build with MSG-P3-016 naming file and line | T-044-02, T-044-06 | Unit | TASK-03 |
| AC6 — two non-fix files with the same key, or a file with no key, fail naming both files and the key | T-044-03 | Unit | TASK-03 |
| AC7 — clean is refused; undo files are refused; forward only | T-044-13 (container), T-044-04 (unit) | Container, unit | TASK-14, TASK-03 |
| AC8 — a migration that fails part way rolls back fully; the failure is recorded; the service does not start | T-044-14 (container), T-044-09 (unit) | Container, unit | TASK-14, TASK-09 |
| AC9 — two instances starting together apply a pending migration exactly once; both start | T-044-16 | Container | TASK-14 |
| BR1–BR8 and the non-AC requirement rows | see §2 (all 22 tests) | Unit and container | TASK-01..-14 |

No AC is left without a test. The job-monitor part of AC8 and the access case TC-E1-044-10 have no test by decision (SPEC-017; DG-L10; OI-E044-G); TASK-19 checks they were not built.

## 2. Test list

| Test | Level | Scenario | Fixture or setup | Expected | Task |
|---|---|---|---|---|---|
| T-044-01 | Unit | Each file-level rule fires on its fixture and passes on a compliant one | `t01-name-fail`, `t01-nonsql-fail`, `t01-undo-fail`, `t01-repeatable-fail`, `t01-seqgap-fail`, `t01-seqdup-fail`, `t01-pass`, `t01-readme-pass` | `L-NAME`, `L-UNDO`, `L-REPEATABLE`, `L-SEQ-GAP`, `L-SEQ-DUP` each exactly once, on the stated file and line 0; the pass folders give no finding | TASK-03, TASK-04 |
| T-044-02 | Unit | Every listed object-name position, every qualified type, a bare schema, a quoted identifier and a dollar-quoted body fail; the allowed qualifiers, a comment and a string literal pass; the seam marker fails | `t02-positions-fail`, `t02-types-fail`, `t02-schema-bare-fail`, `t02-quoted-fail`, `t02-dollar-body-fail`, `t02-allowed-pass`, `t02-comment-string-pass`, `t02-seam-marker-fail` | As `data-model.md` §3: one `L-LITERAL-SCHEMA` per line and schema name, detail `literal schema <name>`; the allowed folder gives none; the seam marker gives one at :2 | TASK-03, TASK-04 |
| T-044-03 | Unit | Header, second header line, duplicate key, fix line 2 and fix without base | `t03-header-fail`, `t03-header-multi-fail`, `t03-keydup-fail`, `t03-fix-line2-fail`, `t03-fix-nobase-fail`, `t03-fix-pass` | `L-HEADER` :1; `L-HEADER-MULTI` :3; one `L-KEY-DUP` naming both files and `RWB-E1-028`; `L-FIX-LINE2` :2; `L-FIX-NO-BASE` :0; the pass folder gives none | TASK-03, TASK-04 |
| T-044-04 | Unit | An undo file is refused by its own rule, not by the name rule | `t01-undo-fail` | exactly one `L-UNDO` :0 and no `L-NAME` for `U0001__rwb_e1_044_undo.sql` | TASK-03 |
| T-044-05 | Unit | A qualified foreign key outside `recovery` is refused; an unqualified or parameterised one passes | `t05-fk-public-fail`, `t05-fk-pgcatalog-fail`, `t05-fk-pass` | `public`: exactly `L-FK-OUTSIDE` and `L-LITERAL-SCHEMA` at :2; `pg_catalog`: exactly one `L-FK-OUTSIDE` at :2; pass folder: none | TASK-03, TASK-04 |
| T-044-06 | Unit | The finding text format, the 1-based line and the all-findings listing | `t06-format-fail` | the complete list, each line matching `MSG-P3-016 schema=recovery object=<file>:<line> rule=<RULE-ID> <detail>`, in file order | TASK-03, TASK-04 |
| T-044-07 | Unit | The production folder is clean (README only) | `src/main/resources/db/modulemigration/recovery` | no finding | TASK-04 |
| T-044-08 | Unit | The schema is pinned on the binding of the migration properties record, unconditionally | `MigrationPropertiesConfigTest`, cases (1)–(6) of `plan.md`/`tasks.md` TASK-07 | cases (1)–(4): context fails, `ConfigurationPropertiesBindException` for the record in the chain, root cause `BindValidationException` naming `rwb.schema`, the value (except blank) and `D-RCV-28`, and no `NullPointerException`, `FlywayException` or `NoSuchBeanDefinitionException`; case (5): context starts, one record bean with `recovery`, no `Flyway` bean; case (6): direct construction of `rwb_case`, blank and null throws nothing | TASK-07, TASK-08 |
| T-044-09 | Unit | Each failure kind logs exactly one `MSG-P3-016` line with the right `object` and rethrows; the success path logs nothing; both data-source branches work | `RecoveryMigrationRunnerTest` with a mocked `Flyway` | `object=7` for a validation failure; `object=2` for a part-way failure; `object=recoveryFlyway` with no version; one ERROR line each; the same exception rethrown; no SQL or credential in the line; both branches reachable | TASK-09, TASK-10 |
| T-044-10 | Container | A pending migration applies once and a rerun applies nothing | `apply-once`, one fresh database | version `1` and a non-null checksum in `flyway_schema_history_recovery`; the table exists; a second context starts and the history row count does not change | TASK-14 |
| T-044-11 | Container | The same file produces the table in two databases with equal checksums | `create-timer`, one database on each container | `recovery.timer` exists in both; the checksum recorded in both is equal | TASK-14 |
| T-044-12 | Container | An applied file edited afterwards fails validation, names the version and stops the start | `invalid-checksum`, copied to a `@TempDir` and edited | `context.getStartupFailure()` holds a `FlywayException`; the captured ERROR line is `MSG-P3-016 schema=recovery object=1`; the edited migration is not applied | TASK-14 |
| T-044-13 | Container | `clean()` is refused and changes nothing; a previous tag starts; a lower pending version fails with its version | `apply-once` for clean; `previous-tag`; `higher-applied` + `lower-pending` | `clean()` throws Flyway's own message (not MSG-P3-016) and the object count is unchanged; the previous-tag start succeeds and applies nothing; the lower version fails with `object=2` in the ERROR line and a failed context | TASK-14 |
| T-044-14 | Container | A migration that fails part way rolls back fully, records the failure and stops the start | `failed-migration` | the first statement's table is absent, no history row for version `2`, the ERROR line is `MSG-P3-016 schema=recovery object=2`, the context fails | TASK-14 |
| T-044-15 | Container | Drift comparison finds exactly the hand-made change | `drift` applied to two databases; `ALTER TABLE recovery.queue ADD COLUMN note_x text` in one | exactly one difference, `MSG-P3-016 schema=recovery object=recovery.queue.note_x` | TASK-14 |
| T-044-16 | Container | Two contexts migrate concurrently and both start | `apply-once`, one fresh database, two threads | one history row for version `1`; both contexts start; no exception | TASK-14 |
| T-044-17 | Container | The two D-RUN-14 rights exist, no table privilege exists, and the database refuses an FK into `public` | the init of this story's branch, `fk-probe` | (a) USAGE true, CREATE false; (b) exactly one `pg_auth_members` row, `ace_view_owner`, inherit false, set true, admin false; (c) the four role attributes false; (d) zero `public` relations with any of the seven privileges; (e) SQLSTATE 42501; (f) SQLSTATE 42501 and no history row | TASK-11, TASK-12 |
| T-044-18 | Container | The first migrate on a non-empty `recovery` with no history table baselines at 0 and applies `V0001` | `non-empty-baseline`, `recovery` pre-filled with a synthetic table | a baseline row at version `0` and version `1` applied above it | TASK-14 |
| T-044-19 | Unit | The comparator reports added, missing and changed column, constraint, index and view; equal snapshots give none; the row mapping works from in-memory rows | `SchemaComparatorTest` | one difference per change, each in the MSG-P3-016 format; equal gives none | TASK-05, TASK-06 |
| T-044-20 | Unit | Every search-path form fails; GRANT and REVOKE fail at line and at statement start and pass in comments | `t20-searchpath-fail`, `t20-grant-fail`, `t20-grant-pass` | eight `L-SEARCH-PATH`; three `L-GRANT`; the pass folder gives none | TASK-03, TASK-04 |
| T-044-21 | Unit | Literals and comments never hide or trigger a schema finding; a real reference after them is still found on its own line | `t21-literals-pass`, `t21-literal-negatives-fail` | pass: none; negatives: exactly four findings, on the right lines | TASK-03, TASK-04 |
| T-044-22 | Unit | Adversarial tokenizer cases: a real `public.` reference after an opener inside another token is still found; the positive cases give nothing; the statement view is correct | `t22-n1`..`t22-n15`, `t22-p1`..`t22-p3`, `t22-s1` | the complete list of §3 below, counted by the multiplicity rule; S1 asserts the parsed model | TASK-01, TASK-02, TASK-03, TASK-04 |

## 3. T-044-22 cases

Negative cases (fixture text from line 2; line 1 is the header `-- Story: RWB-E1-044`):

| Case | Fixture text | Expected findings |
|---|---|---|
| N1 `'/*'` in a literal | L2 `INSERT INTO ${recoverySchema}.t1 (v) VALUES ('/*');` L3 `CREATE TABLE public.x (id int);` L4 `-- */` | `L-LITERAL-SCHEMA` :3 |
| N2 `'--'` in a literal, code after it | L2 `INSERT INTO ${recoverySchema}.t1 (v) VALUES ('--'); CREATE TABLE public.x (id int);` | `L-LITERAL-SCHEMA` :2 |
| N3 `''` escape before an opener | L2 `INSERT INTO ${recoverySchema}.t1 (v) VALUES ('it''s /*');` L3 `CREATE TABLE public.x (id int);` L4 `-- */` | `L-LITERAL-SCHEMA` :3 |
| N4 `E'…'` with `\'` | L2 `INSERT INTO ${recoverySchema}.t1 (v) VALUES (E'\'--'); CREATE TABLE public.x (id int);` | `L-LITERAL-SCHEMA` :2 |
| N5 Quoted identifier holding `--` | L2 `CREATE TABLE ${recoverySchema}."a--b" (id int); CREATE TABLE public.x (id int);` | `L-LITERAL-SCHEMA` :2 |
| N6 `--` inside a `$$` body | L2 `CREATE FUNCTION ${recoverySchema}.f() RETURNS int LANGUAGE sql AS $$ SELECT 1 -- $$; CREATE TABLE public.x (id int);` | `L-LITERAL-SCHEMA` :2 |
| N7 `/*` inside a `$fn$` body | L2 `CREATE FUNCTION ${recoverySchema}.g() RETURNS int LANGUAGE sql AS $fn$ SELECT 1 /* $fn$;` L3 `CREATE TABLE public.x (id int);` L4 `-- */` | `L-LITERAL-SCHEMA` :3 |
| N8 `'` left open inside a `$$` body | L2 `DO $$ BEGIN PERFORM '''; END $$;` L3 `CREATE TABLE public.x (id int);` | `L-LITERAL-SCHEMA` :3; no `L-LEX` |
| N9 `public.` inside a dollar body | L2 `CREATE FUNCTION ${recoverySchema}.h() RETURNS int LANGUAGE sql AS $$` L3 `-- reads the source` L4 `SELECT a.id FROM public.t1 a` L5 `$$;` | `L-LITERAL-SCHEMA` :4 |
| N10 Placeholder is not a dollar quote | L2 `CREATE TABLE ${recoverySchema}.t1 (id int); CREATE TABLE public.x (id int);` | exactly one `L-LITERAL-SCHEMA` :2, for `public.x`, none for `${recoverySchema}` |
| N11 Unterminated literal | L2 `INSERT INTO ${recoverySchema}.t1 (v) VALUES ('abc);` L3 `CREATE TABLE public.x (id int);` | `L-LEX` :2; `L-LITERAL-SCHEMA` :3 |
| N12 Unterminated block comment | L2 `/* not closed` L3 `CREATE TABLE public.x (id int);` | `L-LEX` :2; `L-LITERAL-SCHEMA` :3 |
| N13 Unterminated dollar body | L2 `DO $q$ BEGIN NULL; END;` L3 `CREATE TABLE public.x (id int);` | `L-LEX` :2; `L-LITERAL-SCHEMA` :3 |
| N14 Search path after a literal opener | L2 `INSERT INTO ${recoverySchema}.t1 (v) VALUES ('--'); SET search_path TO x;` | `L-SEARCH-PATH` :2 |
| N15 Qualified `REFERENCES` after a `'--'` literal | L2 `INSERT INTO ${recoverySchema}.t1 (v) VALUES ('--'); CREATE TABLE ${recoverySchema}.c (t_id int REFERENCES public.t1(id));` | exactly two: `L-FK-OUTSIDE` :2 and `L-LITERAL-SCHEMA` :2 |

Where a name matches more than one L-LITERAL-SCHEMA item, the expected result is **one** finding.

Positive cases (no finding at all):

| Case | Fixture text | Why it matters |
|---|---|---|
| P1 Nested block comment | L2 `/* outer /* inner */ public.x */` L3 `SELECT 1;` | A lexer without nesting ends the comment early |
| P2 String inside a dollar body | L2 `CREATE FUNCTION ${recoverySchema}.f() RETURNS text LANGUAGE sql AS $$ SELECT 'public.x' $$;` | Strings inside a body are data |
| P3 `$` inside a string inside a body | L2 `CREATE FUNCTION ${recoverySchema}.f(p text) RETURNS boolean LANGUAGE sql AS $$ SELECT p ~ '^\d{8}$' $$;` | A `$` inside a string opens no dollar quote and gives no `L-LEX` |

Statement-view case (asserted on the parsed file model):

| Case | Fixture text | Expected |
|---|---|---|
| S1 Leading comments do not supply the statement kind | L2 `/* CREATE VIEW v */ -- GRANT x` L3 `CREATE TABLE ${recoverySchema}.t1 (id int); INSERT INTO ${recoverySchema}.t1 (id) VALUES (1);` | exactly two statements; the first starts at line 3 with kind `CREATE TABLE`; the second starts at line 3 with kind `INSERT`; no finding at all (no `L-GRANT`) |

## 4. Story v7 test cases to spec tests

| Story v7 §16 | Spec tests | Note |
|---|---|---|
| TC-E1-044-01 (AC1) | T-044-10 | The `V12` fixture is restated to `V0001` (DG-L01) |
| TC-E1-044-02 (AC2) | T-044-15, T-044-19 | SIT drift is restated to a container-to-container check (D-RCV-05) |
| TC-E1-044-03 (AC3) | T-044-11, T-044-08 | `RWB_SCHEMA=rwb_case` is restated to `recovery` |
| TC-E1-044-04 (AC4) | T-044-12, T-044-09 | — |
| TC-E1-044-05 (AC5) | T-044-02, T-044-06 | — |
| TC-E1-044-06 (AC6) | T-044-03 | — |
| TC-E1-044-07 (AC7) | T-044-13, T-044-04 | There is no PROD profile here; clean is disabled in every profile (inherited) |
| TC-E1-044-08 (AC8) | T-044-14, T-044-09 | The job-monitor part is out of scope (SPEC-017) |
| TC-E1-044-09 (AC9) | T-044-16 | — |
| TC-E1-044-10 (access) | None | Out of scope, no owner named (SPEC-017; DG-L10; OI-E044-G); TASK-19 checks it was not built |

## 5. Coverage checks

- Every AC1–AC9 has at least one test (§1).
- Every rule ID has at least one failing fixture and one passing fixture (`data-model.md` §3): `L-NAME`, `L-UNDO`, `L-REPEATABLE`, `L-SEQ-GAP`, `L-SEQ-DUP`, `L-HEADER`, `L-HEADER-MULTI`, `L-KEY-DUP`, `L-FIX-LINE2`, `L-FIX-NO-BASE`, `L-SEARCH-PATH`, `L-LITERAL-SCHEMA`, `L-FK-OUTSIDE`, `L-GRANT`, `L-LEX` (`L-LEX` fails in `t22-n11` to `t22-n13` and passes in the whole corpus).
- Every token kind, the nesting, both escape forms, the placeholder, the body end inside a body and each unterminated form are reached by T-044-22 or `MigrationLexerTest`.
- Boundaries: line 1 versus line 2 (`t03-header-fail` versus `t01-pass`), `0001` start and contiguity (`t01-seqgap-fail`, `t03-fix-pass`), empty folder, `README.md` only.
- Error paths: unreadable or non-`.sql` file (`t01-nonsql-fail`), missing folder, and a file whose name does not match the pattern (`t01-name-fail`).
- No test is skipped. The container suite fails (not skips) without Docker (D-RCV-28 (3)); the unit suite needs no database.

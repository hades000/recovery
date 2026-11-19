---
title: "Data model: RWB-E1-044"
run_id: "INC-001-epic-1-RWB-E1-044"
revision: "v2 (18 Nov 2026): remediation of plan gate round 1 (PLAN-001, PLAN-002, PLAN-006; data-model consistency), matching plan.md v2 and spec v14-7. v1 (18 Nov 2026): first data model for this run, matching plan.md v1 and spec v14-7."
---

# Data model: RWB-E1-044

No database change. No table, column, view, index, constraint or migration is added or changed by this story (D-RUN-07 not exercised: `plan.md` "Migrations"; Decision Log v10 D-RCV-28 and story v7 §13 say E1-044 ships no production migration file). The "data" of this story is test-scope: the parsed migration file model, the lint finding model, the schema snapshot model, the fixture corpora, and the two configuration records the main code gains or extends. No field holds personal data.

## 1. Parsed migration file model (test scope, SPEC-007, SPEC-016)

Package `th.co.scb.ace.demo.recovery.architecture.migration`. The tokenizer runs once per file; every rule reads the same token boundaries.

| Type | Fields | Notes |
|---|---|---|
| `MigrationLexer` | none (static entry `parse(Path)` returning `ParsedMigrationFile`) | One left-to-right pass over the raw text. At each position outside a token it checks the openers below in this order and takes the first match. |
| `ParsedMigrationFile` | `Path path`, `String fileName`, `List<String> rawLines`, `String codeText`, `String identifierText`, `List<MigrationStatement> statements`, `List<LexProblem> unterminated` | `codeText` and `identifierText` have the same length as the raw text, character for character, so an offset means the same position in both. |
| `MigrationStatement` | `int startOffset`, `int endOffset`, `int startLine`, `String firstWord`, `String kind` | Cut from `identifierText` at top-level `;` tokens only. `kind` is the first one or two words (`CREATE TABLE`, `CREATE OR REPLACE VIEW`, `GRANT`, …). A range with no non-blank character in `identifierText` is not a statement. |
| `LexProblem` | `String kind`, `int line`, `int offset` | One per unterminated opener (`string`, `escape string`, `quoted identifier`, `block comment`, `dollar-quoted body`). Feeds `L-LEX`. |
| `FolderContext` | `List<ParsedMigrationFile> parsedFiles`, `List<String> otherEntries` | The folder's parsed `.sql` files and every other folder entry name. `MigrationLint` builds it from a listing of **all** entries, not only `*.sql`, so `NameRule` sees `notes.txt` (ASM-E044-05). `README.md` is in `otherEntries` and is the one name `NameRule` ignores. |

`MigrationRule` exposes `ruleId()`, `check(ParsedMigrationFile, FolderContext)` and a default `checkFolder(FolderContext)` that returns no finding. `MigrationLint` calls the folder hook once per folder and the file check once per parsed file; `NameRule` overrides the folder hook for the non-`.sql` entries.

Token table (authoritative in spec v14-7 SPEC-007; restated here for the builder):

| Token | Opens with | Ends with | Recognised inside |
|---|---|---|---|
| Line comment | `--` | End of line | Nothing |
| Block comment | `/*` | Matching `*/`, nesting counted | Only `/*` and `*/` for the nesting count |
| Escape string | `E'` or `e'`, where `E` does not continue an identifier | `'` | `''` and `\'` are escaped quotes; `\\` is an escaped backslash |
| Standard string | `'` (also `U&'`, `B'`, `X'`, `N'`) | `'` not followed by `'` | `''` is an escaped quote; backslash is ordinary |
| Quoted identifier | `"` (also `U&"`) | `"` not followed by `"` | `""` is an escaped quote |
| Flyway placeholder | `${` | `}` | Nothing. `${recoverySchema}` is identifier text, never a dollar quote |
| Dollar-quoted body | `$tag$` with an empty or `[A-Za-z_][A-Za-z0-9_]*` tag, and the `$` does not continue an identifier. `$1` is a parameter | Next literal occurrence of the same `$tag$`; the end is found first | Body tokenized again with the same rules, bounded by its end |
| Code | Anything else | — | — |

Three views, all line-preserving (blanked characters become spaces, newlines are kept):

| View | Comments | String literals | Quoted identifiers | Dollar delimiters | Dollar bodies | Used by |
|---|---|---|---|---|---|---|
| (a) `codeText` | Blanked | Kept | Kept | Kept | Kept, with their own comments blanked | `L-SEARCH-PATH`, `L-GRANT` |
| (b) `identifierText` | Blanked | Blanked, quotes included | Kept | Blanked | Kept as code, with their own comments and strings blanked | `L-LITERAL-SCHEMA`, `L-FK-OUTSIDE`, statement cut |
| (c) `statements` | — | — | — | — | Never split | Statement kind and start line; `L-GRANT`; `isAllowedQualifier` |

## 2. Lint finding model (test scope, SPEC-004)

`MigrationFinding(String ruleId, String file, int line, String key, String detail)`; `String format()` returns exactly:

```text
MSG-P3-016 schema=recovery object=<file>:<line> rule=<RULE-ID> <detail>
```

`line` is 1-based, or `0` for a file-level rule. One finding per (rule, file, line, key):

| Rule | Key |
|---|---|
| `L-LITERAL-SCHEMA` | The disallowed schema name as PostgreSQL resolves it (unquoted folded to lower case; quoted as written without quotes) |
| `L-FK-OUTSIDE` | The qualifier after `REFERENCES`, resolved the same way |
| `L-SEARCH-PATH`, `L-GRANT` | None (at most one finding per line) |
| `L-LEX` | The offset of the unterminated opener |
| File-level rules (`L-NAME`, `L-UNDO`, `L-REPEATABLE`, `L-SEQ-GAP`, `L-SEQ-DUP`, `L-HEADER`, `L-HEADER-MULTI`, `L-KEY-DUP`, `L-FIX-LINE2`, `L-FIX-NO-BASE`) | The file, the story key, or the sequence, as the rule needs; line 0 |

Details: `L-LITERAL-SCHEMA` is `literal schema <name>`; `L-FK-OUTSIDE` is `BR8 foreign key outside recovery schema`; the file-level details name the second file, the key or the expected sequence (spec SPEC-004, -005, -006, -008).

`SequenceGapRule` compares the **distinct** sorted sequence numbers against `1..N`, so `V0001` twice is one `L-SEQ-DUP` finding and no `L-SEQ-GAP` (PA-E044-06).

## 3. Lint fixture corpus (`backend/src/test/resources/migration-lint/`)

One folder per case. Every file's line 1 is `-- Story: <KEY>` derived from its name; each non-fix file has a distinct key; every sequence starts at `V0001` and is contiguous except where the case is the violation. Names, table names and column names are synthetic (`queue`, `timer`, `t1`, `c1`, `a`, `b`, `account_id`); the only real names are the ACE table `public.account` and the schema names the rules name.

`<KEY>` is `rwb_e1_044` unless the case needs another key: `rwb_e1_028` for the two-file key case, `rwb_044` for the broken-name case, and `rwb_e1_045` for the second file of `t01-seqgap-fail` and `t01-seqdup-fail`, so only the sequence rule fires there (PA-E044-12).

| Folder | Files | Expected findings (rule at line, detail) |
|---|---|---|
| `t01-pass` | `V0001__rwb_e1_044_ok.sql` | none |
| `t01-readme-pass` | `V0001__rwb_e1_044_ok.sql`, `README.md` | none |
| `t01-name-fail` | `V0001__rwb_e1_044_ok.sql`, `V0002__rwb_044_bad.sql` | `L-NAME` :0 on the bad file |
| `t01-nonsql-fail` | `V0001__rwb_e1_044_ok.sql`, `notes.txt` | `L-NAME` :0 on `notes.txt` (ASM-E044-05) |
| `t01-undo-fail` | `V0001__rwb_e1_044_ok.sql`, `U0001__rwb_e1_044_undo.sql` | `L-UNDO` :0 (and no `L-NAME` for it) |
| `t01-repeatable-fail` | `V0001__rwb_e1_044_ok.sql`, `R__views.sql` | `L-REPEATABLE` :0 |
| `t01-seqgap-fail` | `V0001__rwb_e1_044_ok.sql`, `V0003__rwb_e1_045_third.sql` (line 1 `-- Story: RWB-E1-045`) | `L-SEQ-GAP` :0, detail names `V0002`; no `L-KEY-DUP` |
| `t01-seqdup-fail` | `V0001__rwb_e1_044_ok.sql`, `V0001__rwb_e1_045_dup.sql` (line 1 `-- Story: RWB-E1-045`) | one `L-SEQ-DUP` :0 naming both files; no `L-SEQ-GAP`, no `L-KEY-DUP` |
| `t03-header-fail` | `V0001__rwb_e1_044_ok.sql` with line 1 `-- Story: RWB-E1-045` | `L-HEADER` :1 |
| `t03-header-multi-fail` | `V0001__rwb_e1_044_ok.sql` with a second `-- Story: RWB-E1-044` on line 3 | `L-HEADER-MULTI` :3 |
| `t03-keydup-fail` | `V0001__rwb_e1_028_a.sql`, `V0002__rwb_e1_028_b.sql`, both non-fix | one `L-KEY-DUP` :0 naming both files and `RWB-E1-028` |
| `t03-fix-line2-fail` | `V0001__rwb_e1_044_ok.sql`, `V0002__rwb_e1_044_fix.sql` with line 2 `-- Fix:` and no reason | `L-FIX-LINE2` :2 |
| `t03-fix-nobase-fail` | `V0001__rwb_e1_044_ok.sql`, `V0002__rwb_e1_028_fix.sql` with line 2 `-- Fix: backfill` | `L-FIX-NO-BASE` :0 |
| `t03-fix-pass` | `V0001__rwb_e1_044_ok.sql`, `V0002__rwb_e1_044_fix.sql` with line 2 `-- Fix: add index` | none |
| `t02-positions-fail` | `V0001__rwb_e1_044_ok.sql`, one position per line | one `L-LITERAL-SCHEMA` per line, detail `literal schema <name>`; positions in order from line 2: `CREATE TABLE public.t1`, `CREATE VIEW public.v1`, `CREATE MATERIALIZED VIEW public.mv1`, `CREATE SEQUENCE public.s1`, `CREATE INDEX i1 ON public.t1`, `CREATE TRIGGER tr1 AFTER INSERT ON public.t1`, `CREATE FUNCTION public.f1()`, `CREATE PROCEDURE public.p1()`, `CREATE TYPE public.ty1`, `CREATE DOMAIN public.d1`, `CREATE TABLE ${recoverySchema}.c1 (id int REFERENCES public.t1(id))` (also `L-FK-OUTSIDE`), `SELECT 1 FROM public.t1`, `SELECT 1 FROM ${recoverySchema}.t1 JOIN public.t1 ON true`, `INSERT INTO public.t1 VALUES (1)`, `UPDATE public.t1 SET id = 1`, `TRUNCATE public.t1`, `COMMENT ON TABLE public.t1 IS 'x'`, `CREATE TABLE ${recoverySchema}.c2 (id int) OWNED BY public.t1` |
| `t02-types-fail` | `V0001__rwb_e1_044_ok.sql` | three `L-LITERAL-SCHEMA`: `x::public.t1`, `CAST(x AS public.t1)`, and a column typed `public.t1` |
| `t02-schema-bare-fail` | `V0001__rwb_e1_044_ok.sql` | one `L-LITERAL-SCHEMA`, detail `literal schema public`, on the `CREATE SCHEMA public` line |
| `t02-allowed-pass` | `V0001__rwb_e1_044_ok.sql` using `${recoverySchema}.t1`, `information_schema.tables` and `pg_catalog.pg_class` | none |
| `t02-comment-string-pass` | `V0001__rwb_e1_044_ok.sql` with `-- SELECT * FROM public.account`, `/* public.t1 */` and `VALUES ('public.account')` | none |
| `t02-dollar-body-fail` | `V0001__rwb_e1_044_ok.sql` with a `LANGUAGE sql` body containing `SELECT a.id FROM public.t1 a` | one `L-LITERAL-SCHEMA` on the body line |
| `t02-quoted-fail` | `V0001__rwb_e1_044_ok.sql` with `CREATE TABLE "public".account (id int);` | one `L-LITERAL-SCHEMA` :2, detail `literal schema public` |
| `t02-seam-marker-fail` | `V0001__rwb_e1_044_ok.sql` with `CREATE VIEW ${recoverySchema}.v_ace_x AS SELECT a.id FROM public.t1 a;` on line 2 | one `L-LITERAL-SCHEMA` :2 (SEAM-E044-01 marker; RWB-E1-069 replaces this fixture with its own pass/fail pair) |
| `t05-fk-public-fail` | `V0001__rwb_e1_044_ok.sql` with `REFERENCES public.account(id)` on line 2 | exactly `L-FK-OUTSIDE` :2 and `L-LITERAL-SCHEMA` :2 |
| `t05-fk-pgcatalog-fail` | `V0001__rwb_e1_044_ok.sql` with `REFERENCES pg_catalog.t1(id)` | exactly one finding, `L-FK-OUTSIDE` :2 |
| `t05-fk-pass` | `V0001__rwb_e1_044_ok.sql` with `REFERENCES ${recoverySchema}.t1(id)` and an unqualified `REFERENCES t1(id)` | none |
| `t06-format-fail` | `V0001__rwb_044_bad.sql`, `V0002__rwb_e1_044_ok.sql` with a `CREATE TABLE recovery.q (id int)` on line 2 | two findings, format and order asserted |
| `t20-searchpath-fail` | `V0001__rwb_e1_044_ok.sql`, one form per line | eight `L-SEARCH-PATH`, one per line: `SET search_path`, `SET LOCAL search_path`, `SET SESSION search_path`, `SELECT set_config('search_path', …)`, `ALTER ROLE … SET search_path`, `ALTER DATABASE … SET search_path`, `ALTER FUNCTION … SET search_path`, `RESET search_path` |
| `t20-grant-fail` | `V0001__rwb_e1_044_ok.sql` | three `L-GRANT`: `GRANT` at line start, `REVOKE` at line start, `SELECT 1; GRANT …` on one line |
| `t20-grant-pass` | `V0001__rwb_e1_044_ok.sql` with `-- GRANT …` and a `/* REVOKE … */` block | none |
| `t21-literals-pass` | `V0001__rwb_e1_044_ok.sql` | none: `VALUES ('public.account.account_key')`, `VALUES ('it''s public.account')`, `VALUES (E'public.branch')`, a trailing `-- reads public.account`, a multi-line `/* public.product */` |
| `t21-literal-negatives-fail` | `V0001__rwb_e1_044_ok.sql` with a noise literal and comment on earlier lines | `FROM public.account` (one), `"public".account` (one), `REFERENCES public.account(id)` (two: `L-FK-OUTSIDE` and `L-LITERAL-SCHEMA`), each on its own line |
| `t22-n1` … `t22-n15` | one file each, `V0001__rwb_e1_044_ok.sql`, lines 2+ exactly as the spec T-044-22 negative table (N1 to N15) | the findings in that table, counted by the multiplicity rule; `t22-n15` gives exactly two |
| `t22-p1` … `t22-p3` | one file each, lines 2+ as the spec T-044-22 positive table | none |
| `t22-s1` | one file, lines 2–3 as the spec statement-view case S1 | none; asserted on the parsed model: exactly two statements, the first at line 3 with kind `CREATE TABLE`, the second at line 3 with kind `INSERT` |

`MigrationLint` lists every folder entry: `.sql` entries are parsed, and every other name goes to `FolderContext`, where `NameRule` reports all names except `README.md`. That is how `notes.txt` in `t01-nonsql-fail` reaches `L-NAME` (ASM-E044-05). An empty folder gives no finding. A `.sql` entry that cannot be read makes the lint throw an `UncheckedIOException` naming it, so the corpus cannot pass by skipping a file. The two boundary cases are `@TempDir` methods in `RecoveryMigrationLintTest`, not resource folders.

Every fixture folder is scanned on its own. `RecoveryMigrationLintTest` asserts the complete list, so an extra finding fails the case.

## 4. Flyway fixture corpus (`backend/src/test/resources/flyway-fixtures/`)

Fixture names follow D-RCV-28 and use key `rwb_e1_044`. Numbers are test-only (ASM-E044-14); the production folder stays empty.

| Folder | Files | Used by |
|---|---|---|
| `apply-once` | `V0001__rwb_e1_044_add_queue.sql` (`CREATE TABLE ${recoverySchema}.queue (id bigint, team_code text)`) | T-044-10, T-044-16, T-044-18 |
| `drift` | the same file as `apply-once` | T-044-15, applied to two databases |
| `create-timer` | `V0001__rwb_e1_044_create_timer.sql` | T-044-11 |
| `invalid-checksum` | `V0001__rwb_e1_044_add_queue.sql` (copied to `@TempDir` and edited before the second start) | T-044-12 |
| `previous-tag` | `V0001__rwb_e1_044_ok.sql`, `V0002__rwb_e1_044_later.sql` (the second removed from the `@TempDir` copy before the previous-tag start) | T-044-13 |
| `higher-applied` | `V0001__rwb_e1_044_ok.sql`, `V0003__rwb_e1_044_higher.sql` | T-044-13 (sets the highest applied version) |
| `lower-pending` | `V0001__rwb_e1_044_ok.sql`, `V0002__rwb_e1_044_late.sql` | T-044-13 (lower version pending under `outOfOrder(false)`) |
| `failed-migration` | `V0001__rwb_e1_044_ok.sql`, `V0002__rwb_e1_044_broken.sql` (second statement references a missing table) | T-044-14 |
| `non-empty-baseline` | `V0001__rwb_e1_044_add_queue.sql` | T-044-18 |
| `fk-probe` | `V0001__rwb_e1_044_fk_probe.sql` (`CREATE TABLE ${recoverySchema}.fk_probe (account_id bigint REFERENCES public.account(id))`) | T-044-17 (f) |

The `fk-probe` folder is outside the lint's production scan. No fixture holds personal data; `public.account` is an ACE table name, never content.

## 5. Schema snapshot model (test scope, SPEC-012)

| Type | Fields | Notes |
|---|---|---|
| `SchemaSnapshot` | `Set<TableSnapshot> tables`, `Set<ViewSnapshot> views` | Immutable copies |
| `TableSnapshot` | `String name`, `Map<String, ColumnSnapshot> columns`, `Set<String> constraints`, `Set<String> indexes` | Names are unqualified inside schema `recovery` |
| `ColumnSnapshot` | `String name`, `String dataType`, `boolean nullable` | From `information_schema.columns` |
| `ViewSnapshot` | `String name`, `Set<String> columns` | From `information_schema.views` plus its columns |
| `SchemaDifference` | `Kind kind` (`ADDED`, `MISSING`, `CHANGED`), `String objectPath` | `objectPath` is `recovery.<table>.<column>`, `recovery.<table>.<constraint>`, `recovery.<index>` or `recovery.<view>` |
| `SchemaSnapshotReader` | `read(Connection, String schema)`; package-private pure `fromRows(...)` | Only `read` touches a database; `fromRows` takes the catalog rows and is what T-044-19 exercises |
| `SchemaComparator` | `compare(SchemaSnapshot left, SchemaSnapshot right)` returning `List<SchemaDifference>`; `format(SchemaDifference)` | Pure. Formats `MSG-P3-016 schema=recovery object=recovery.<…>` |

## 6. Configuration and bean model (main, SPEC-001, SPEC-002, SPEC-003)

| Item | Type and package | Content |
|---|---|---|
| Migration properties record `[TE-001]` | `RecoveryMigrationProperties`, `casewf.migration`, package-private, `@ConfigurationProperties(prefix = "rwb")`, `@Validated` added by this story | `String schema` (`@NotNull`, `@Pattern(regexp = "recovery", message = "rwb.schema must be recovery (D-RCV-28)")`), nested `Flyway(boolean enabled, String url, String user, String password, String location)`. Keys, defaults and components unchanged from RWB-TE-001; no constructor check. |
| Registration | `MigrationPropertiesConfig`, `casewf.migration`, package-private, `@Configuration(proxyBeanMethods = false)` + `@EnableConfigurationProperties(RecoveryMigrationProperties.class)`, **no condition** | New. Holds the pin when `rwb.flyway.enabled=false`. |
| Flyway bean `[TE-001]` | `RecoveryFlywayConfig`, `casewf.migration`, package-private, `@ConditionalOnProperty(name = "rwb.flyway.enabled", havingValue = "true", matchIfMissing = true)` | `recoveryFlyway(RecoveryMigrationProperties, DataSource, DataSourceProperties)` returns the configured `Flyway`, with no init method and `validateOnMigrate(true)` added. |
| Migrate runner | `RecoveryMigrationRunner`, `casewf.migration`, package-private | `migrate()` wraps `flyway.migrate()`, logs one ERROR `MSG-P3-016 schema={} object={}` and rethrows; `failureObject` maps a `FlywayException` to the version(s) or `recoveryFlyway` as spec SPEC-003 states. Registered by `@Bean(initMethod = "migrate") recoveryMigrationRunner(Flyway, RecoveryMigrationProperties)`. |

Defaults bound from `backend/src/main/resources/application.yaml` (unchanged): `rwb.schema` = `recovery` (literal, line 74); `rwb.flyway.enabled` = `true`; `rwb.flyway.url` = `jdbc:postgresql://localhost:5433/ace`; `rwb.flyway.user` = `rwb_migrator`; empty password; `rwb.flyway.location` = `classpath:db/modulemigration/recovery`.

## 7. Database and local infrastructure changes

The only database-adjacent change is in the local init, not in a migration: `rwb_migrator` gains `USAGE ON SCHEMA public` and the `ace_view_owner` membership `WITH INHERIT FALSE, SET TRUE`. It gains no table privilege, no `CREATE` on `public`, no `ADMIN` and no other membership, so `pg_auth_members` holds exactly one membership row for `rwb_migrator` and an FK into `public` is still refused (T-044-17 (b), (d), (f)). The container test creates each case's database with `CREATE DATABASE <name> TEMPLATE ace` (the container is built with `RWB_LOAD_REFERENCE_SCHEMA=false` and `RWB_ACE_TIER2_PROBE=false`), so the ACE `public` schema of 62 tables and the init grants are present; (d) is therefore a real zero-privilege count, not an empty schema. `recovery` and its objects keep their owner `rwb_migrator`, and `ace_view_owner` keeps `USAGE, CREATE ON SCHEMA recovery` (needed by the owner change).

## 8. Personal data and synthetic data

No field holds personal data. Lint fixtures use synthetic identifiers, and the values in T-044-21's dictionary rows are the literal text `public.account.account_key` and similar schema-shaped strings, not customer data. The container fixtures use `queue`, `timer`, `team_code`, `note_x` and `account_id` with no rows of personal data. Roles are named by database role (`rwb_migrator`, `ace_view_owner`, `recovery_svc`), not by a person.

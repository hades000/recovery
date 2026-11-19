---
title: "RWB-E1-044 Database migrations versioned with parameterized schema names — architecture"
run_id: "INC-001-epic-1-RWB-E1-044"
story: "RWB-E1-044"
stage: "docs (final documentation)"
date: "2026-11-18"
status: "DOCUMENTED against branch tip 89477bc"
---

# Architecture — recovery migration tooling

Sections 2–7 carry `DOC-RWB-E1-044-007`..`-012`; §1 is their shared context.

This story adds no runtime component of its own except two package-private beans in
`casewf.migration` and the start-up check on their properties. The rest is **test-scope tooling**:
a tokenizer, a lint, a snapshot reader and a comparator. Everything below is exercised by
`./gradlew test`, except the container proof and the D-RUN-14 grant proof, which run in
`recoveryIntegrationTest`.

## 1. Context

| Fact | Value | Source |
|---|---|---|
| Service | ACE service, recovery module, one repository and one front end | AGENTS.md §2 |
| Story module | P3 Case and workflow, package `th.co.scb.ace.demo.recovery.casewf.migration` | story v7 §13; RWB-TE-001 SPEC-022 |
| Lint and drift package | `th.co.scb.ace.demo.recovery.architecture.migration` (test scope) | SPEC-016 |
| Migration location | `classpath:db/modulemigration/recovery` | SPEC-001 |
| History table | `flyway_schema_history_recovery` (`RecoveryFlywayConfig.HISTORY_TABLE`) | BR6 |
| Schema | `recovery`, pinned (D-RCV-28) | SPEC-002 |
| Flyway version | 12.4.0 (resolved dependency; `javap` pre-flight) | `../implement/backend/javap-flyway.txt` |
| Production migration file | **None** | D-RCV-28; story v7 §13; D-RUN-07 |

The lint is a **build-time** control that runs before merge. It is not a runtime gate: the service
does not lint files at start. The database is the second control (the D-RUN-14 grants and BR8);
neither control alone is claimed to stop every mistake.

## 2. Tokenizer and the three views

**DOC ID:** DOC-RWB-E1-044-007 · **Maps to:** SPEC-RWB-E1-044-007, -016; AC5; D-RUN-13; TASK-01, TASK-02; CODE-E044-001..004

`MigrationLexer.parse(Path)` reads a `.sql` file **once**, left to right, and returns a
`ParsedMigrationFile`: the file name, the raw lines, three views and the list of unterminated
openers. There is no separate "strip comments" pass and no separate "strip strings" regex. That is
deliberate: removing comments and strings in independent passes lets an opener inside the other
token hide real code (the adversarial cases N1–N15 in T-044-22).

### 2.1 Token precedence

At each position outside a token the lexer tries the openers in this order and takes the first that
matches. Inside a token only that token's own end and escapes are recognised.

| Token | Opens with | Ends with | Inside |
|---|---|---|---|
| Line comment | `--` | end of line | nothing |
| Block comment | `/*` | matching `*/`, nesting counted as PostgreSQL counts it | `/*` and `*/` only |
| Escape string | `E'` / `e'`, where `E` does not continue an identifier | `'` | `''` and `\'`; `\\` |
| Standard string | `'`, including `U&'`, `B'`, `X'`, `N'` | `'` not followed by `'` | `''`; backslash is ordinary |
| Quoted identifier | `"` (also `U&"`) | `"` not followed by `"` | `""` |
| Flyway placeholder | `${` | `}` | nothing; `${recoverySchema}` is identifier text, never a dollar quote |
| Dollar-quoted body | `$tag$`, empty or `[A-Za-z_][A-Za-z0-9_]*`, where `$` does not continue an identifier; `$1` is a parameter | next literal `$tag$` | re-tokenized as code with these same rules, bounded by its end |
| Code | anything else | — | — |

Two rules are load-bearing:

- **Dollar-quoted bodies are code.** Every body in Physical Schema v6 is a function body, so a
  `public.` reference inside one is a schema reference, not data. The body is scanned, and its own
  comments and strings are ignored the same way.
- **The body end always wins.** A quote or comment left open inside a body ends at the closing
  `$tag$`, as PostgreSQL ends it, so nothing inside a body can hide text after it.

An opener still open at end of file produces one `LexProblem` (`L-LEX`, `unterminated <kind>`) on
the opener's line; the lexer then treats that one character as code and resumes. PostgreSQL would
reject such a file too, and the rest of the file is still checked by every other rule.

### 2.2 Bounds

| Bound | Value | Effect |
|---|---|---|
| File size | 262,144 characters | Checked against the platform file size **before** the read; a larger file fails with a clear `IllegalArgumentException`, not an OOM or a scan |
| Dollar-body nesting | 32 | Deeper input fails closed rather than overflowing the stack |

The bounds exist because the lint runs on contributor input in shared CI (SEC-044-05, closed for
the reported denial of service).

### 2.3 The three views

Every blanked character becomes a space and every newline is kept, so an offset means the same
position in the raw file and in both text views. Line lookup is a binary search over precomputed
line starts.

| View | Comments | String literals | Quoted identifiers | Dollar delimiters | Dollar bodies | Used by |
|---|---|---|---|---|---|---|
| (a) code text | blanked | **kept** | kept | kept | kept, with their own comments blanked | `L-SEARCH-PATH`, `L-GRANT` line-start |
| (b) identifier text | blanked | blanked, quotes included | kept | blanked | kept as code, with their own comments and strings blanked | `L-LITERAL-SCHEMA`, `L-FK-OUTSIDE` |
| (c) statements | cut from (b), blanked as (b) | as (b) | as (b) | as (b) | kept as code, never split | `L-GRANT` statement-start; `isAllowedQualifier` context |

Statements (c) are offset ranges over view (b). They are cut only at `;` tokens the tokenizer found
at top level — never at a `;` in a comment, string, quoted identifier or body. A statement's start
line, first word and kind (`CREATE TABLE`, `CREATE OR REPLACE VIEW`, `GRANT`, …) are read from (b)
over its range, so a leading comment never supplies or hides the statement kind. A range with no
non-blank character is not a statement. A rule that needs statement **code** (`L-GRANT`) reads the
same offset range in view (a).

The header rules (`L-HEADER`, `L-HEADER-MULTI`, `L-FIX-LINE2`) read the raw lines, because the
header is a comment by design.

## 3. Lint registry and the single extension point

**DOC ID:** DOC-RWB-E1-044-008 · **Maps to:** SPEC-RWB-E1-044-004..-010, -016; AC5, AC6, AC7, BR8; TASK-03, TASK-04; CODE-E044-005..019

### 3.1 Structure

| Type | Role |
|---|---|
| `MigrationRule` | One implementation per rule ID: `ruleId()`, `check(ParsedMigrationFile, FolderContext)`, and a default `checkFolder(FolderContext)` returning no finding. |
| `MigrationRules.all()` | The one ordered registry of the 15 rules. Adding a rule is one class plus one entry; no other rule changes. |
| `FolderContext` | The folder's parsed `.sql` files **and every other entry name**, so `NameRule` can report `notes.txt` (ASM-E044-05). |
| `MigrationLint.lint(Path)` | Lists every entry, parses each `.sql` once, runs each rule's folder hook and then each rule per file, and returns every finding. |
| `MigrationFinding` | Rule, file, 1-based line, key, detail; `format()` renders the `MSG-P3-016` line; equality is `(rule, file, line, key)`, which is the multiplicity rule. |
| `RecoveryMigrationLintTest` | The JUnit entry point: the production folder (README only) plus the 55 fixture folders, each asserting its **complete** finding list. |

`MigrationLint` is fail closed. A missing folder or unreadable entry raises an
`UncheckedIOException` naming it; it never returns an empty list to mean "nothing checked". An empty
folder legitimately gives no finding.

### 3.2 Finding identity

| Rule | Key | Multiplicity |
|---|---|---|
| `L-LITERAL-SCHEMA` | The disallowed schema name as PostgreSQL resolves it (unquoted folded to lower case, quoted as written without quotes) | One finding per (file, line, name), whichever of items 1–4 matched |
| `L-FK-OUTSIDE` | The referenced qualifier | One per (file, line, qualifier) |
| `L-SEARCH-PATH`, `L-GRANT` | none | At most one per line |
| `L-LEX` | The opener offset | One per unterminated opener, on its line |
| File-level rules | version, key or file as stated | Line `0` |

`L-LITERAL-SCHEMA` and `L-FK-OUTSIDE` are separate rules, so one `REFERENCES public.account(id)`
gives two findings on the same line: one under each rule.

### 3.3 The one qualifier decision

`LiteralSchemaRule.isAllowedQualifier(MigrationStatement statement, String qualifier)` is the
single place that decides whether a schema qualifier is allowed. It receives the **whole
enclosing statement**, selected by identifier-view offset range (not by matching start line), so a
later rule can depend on the statement kind even when the qualifier sits on a later line of a
multi-line statement (code-gate CODE-001).

Today it returns true only for `${recoverySchema}`, `information_schema` and `pg_catalog`. There is
no `public` exception. `ForeignKeyOutsideRule` never calls it: the SPEC-016 seam cannot weaken
BR8.

### 3.4 The RWB-E1-069 seam

`CREATE VIEW ${recoverySchema}.v_ace_account AS … FROM public.account a` is exactly the text ADR
v3 ADR-010, D-RCV-35 and Physical Schema v6 Section A need, and the D-RCV-28 lint as written rejects
it. The conflict is recorded as DG-L09, and the resolution is a seam owned by RWB-E1-069:

| Seam | Owner | What the owner adds |
|---|---|---|
| SEAM-E044-01 | RWB-E1-069 | A narrow exception in `isAllowedQualifier`: `public` allowed **only** inside `CREATE [OR REPLACE] VIEW ${recoverySchema}.v_ace_*`, never for `L-FK-OUTSIDE` or any other statement kind; its own pass and fail fixtures |
| SEAM-E044-02 | RWB-E1-069 | Resolution of Section A grants (`GRANT USAGE ON SCHEMA public …`, `GRANT SELECT ON public.account, …`, revoke from PUBLIC) against `L-GRANT` and `L-LITERAL-SCHEMA` items 3 and 4, and of two non-fix files per key against `L-KEY-DUP` (OI-E044-B) |
| SEAM-E044-03 | None named | Job-monitor parts (D-RCV-12; OI-E044-G) |
| SEAM-E044-04 | RWB-TE-001, merged upstream | Nothing more: its combined coverage bundle is inherited, not rebuilt |

This story ships a **seam-marker fixture** (`t02-seam-marker-fail`) that must fail with
`L-LITERAL-SCHEMA`, proving the lint ships D-RCV-28 as written. RWB-E1-069 replaces that fixture
with its own pass and fail fixtures when it adds the exception.

## 4. Schema snapshot and comparator

**DOC ID:** DOC-RWB-E1-044-009 · **Maps to:** SPEC-RWB-E1-044-012; AC2, BR7; TASK-05, TASK-06, TASK-14; CODE-E044-020

```text
recovery database ──► SchemaSnapshotReader.read(Connection, schema, historyTable)
                            │  information_schema + pg_catalog
                            ▼
                      SchemaSnapshot  (tables → columns with type + nullability,
                            │          constraints, indexes; views → column names)
              ┌─────────────┴─────────────┐
              ▼                           ▼
     SchemaSnapshot (result)     SchemaSnapshot (target)
              └────────────► SchemaComparator ◄────────┘
                                   │
                                   ▼
              SchemaDifference.format() = MSG-P3-016 schema=recovery
                                          object=recovery.<table>.<column>
```

- **Reader.** Reads tables, columns, constraints, indexes and views for one schema. The column
  query uses `pg_catalog.format_type(atttypid, atttypmod)` and `attnotnull`, so length,
  precision/scale and enum types are compared, not only `information_schema.data_type`
  (ponytail Should 4). Schema and history-table names are `PreparedStatement` parameters, never
  concatenated. The Flyway history table is excluded: its generated constraint names embed OIDs and
  differ between identical databases (DEV-E044-02). `fromRows` is pure, so T-044-19 needs no
  database.
- **Comparator.** Pure logic. Produces one `SchemaDifference` per added, missing or changed table,
  column, constraint, index or view; formats each as the `MSG-P3-016` line above.
- **Container proof.** T-044-15 builds two databases from the same container template, applies the
  same fixtures, adds `note_x` to `recovery.queue` in one, and expects exactly one difference.
  T-044-16's `driftComparisonSeesAColumnLengthChange` also rejects a width change (`varchar(8)` vs
  `varchar(50)`).

The tooling is test scope only. It is not packaged with the application, has no runtime effect and
reads only catalog metadata. A real-environment run, a read-only account and the
`rwb.p3.migration-drift-gate` flag are out of scope by D-RCV-05.

**Known follow-up.** View columns are stored by name only, so a view **column type** change is not
reported (ponytail Nice 9). It is a follow-up, not a regression and not a spec requirement.

## 5. Flyway configuration and failure reporting

**DOC ID:** DOC-RWB-E1-044-010 · **Maps to:** SPEC-RWB-E1-044-001, -002, -003, -013; AC1, AC3, AC4, AC7, AC8; NFR-027, NFR-052; TASK-08, TASK-10, TASK-14; CODE-E044-021..024

### 5.1 Bean and settings

`RecoveryFlywayConfig` is package-private in `casewf.migration` and is conditional on
`rwb.flyway.enabled` (`matchIfMissing = true`). It builds the `Flyway` bean only; it never calls
`migrate`.

| Setting | Value | Why |
|---|---|---|
| `schemas`, `defaultSchema` | `rwb.schema` (pinned `recovery`) | D-RCV-28 |
| `table` | `flyway_schema_history_recovery` | BR6: the recovery module owns its history |
| `locations` | `classpath:db/modulemigration/recovery` | inherited; overridden only in container tests |
| `placeholders` | `recoverySchema = rwb.schema` | `${recoverySchema}` in every migration |
| `outOfOrder` | `false` | forward only; a lower pending version fails |
| `baselineVersion` | `0` | D-RCV-48: a non-empty schema with no history baselines at 0 |
| `baselineOnMigrate` | `true` | first migrate adopts an existing schema |
| `cleanDisabled` | `true` | NFR-027; no clean in any environment |
| `createSchemas` | `false` | the schema is provisioned, not created by Flyway |
| `validateMigrationNaming` | `true` | a malformed name fails |
| `validateOnMigrate` | `true` (**added by this story**) | AC4; behaviour unchanged, intent explicit |
| `ignoreMigrationPatterns` | Flyway default (`*:future`) | a previous tag starts against a later database |

**Data source selection.** If `rwb.flyway.user` has text, Flyway connects with
`rwb.flyway.url` (or `DataSourceProperties.determineUrl()` when the URL is blank), that user and
password. Otherwise it uses the application `DataSource`. The migrator account is used in
production; the service identity never holds DDL rights (BS-4.5). Credentials come from the
environment or the key store and never appear in the repository or a log line (NFR-052).

### 5.2 Schema pin

The pin is on **binding**, not on the Flyway bean:

```text
application.yaml  rwb.schema: recovery
        │
        ▼
RecoveryMigrationProperties   @ConfigurationProperties(prefix = "rwb")
                              @Validated
                              schema: @NotNull @Pattern("recovery")
        │  registered by
        ▼
MigrationPropertiesConfig     @Configuration, no condition
        │
        ▼
every Spring start (Flyway enabled or not) → BindValidationException → context fails
```

`@EnableConfigurationProperties` was moved off the conditional `RecoveryFlywayConfig` so that
`RWB_FLYWAY_ENABLED=false` cannot bypass the check. The constraint is on `schema` only, so an
unbound nested value is never read, and a compact-constructor check is deliberately not used:
building the record in code (as some tests do) must remain possible. The error names the property
and cites D-RCV-28; Spring's field error adds the rejected value. No message ID applies.

### 5.3 Failure report

```text
container start
   └─ RecoveryMigrationRunner (initMethod = "migrate")
        ├─ flyway.migrate() ─ success → nothing logged
        └─ FlywayException
             ├─ object = versions from validateWithResult()          (validation)
             │           or first pending version from info()        (part-way)
             │           or "recoveryFlyway"                         (no version / lookup failure)
             ├─ log.error("MSG-P3-016 schema={} object={}")
             └─ rethrow → context fails → service does not start
```

- One line per failure; the line holds the message ID, the schema and the object only.
- The detail lookup is wrapped in `try/catch RuntimeException`, so a database that answers neither
  `migrate()` nor `info()` still gets the fallback line and the original exception (SEC-044-04,
  ponytail Must 1).
- Null or blank versions are skipped; `V0002` is displayed as `2` (DEV-E044-03).
- A refused `clean()` is not wrapped: Flyway's own message is shown (DG-L11).
- The rethrown exception is logged by Spring and can contain the failing SQL. That is accepted:
  recovery migrations hold DDL and reference data only, never personal data. Password is a separate
  property, not part of the JDBC URL. Audit A-07 log masking belongs to RWB-TE-011.

## 6. D-RUN-14: the migration account's rights for ACE views

**DOC ID:** DOC-RWB-E1-044-011 · **Maps to:** SPEC-RWB-E1-044-017; BR8; D-RUN-14; TASK-11, TASK-12; CODE-E044-026

### 6.1 What was declined

RWB-E1-069 v7 §3 attributes the **ACE DBA role** to this story, "so it can grant on schema `public`
and set a view owner". The role is declined. Story v7 §3 and §10 name only a migration account from
the key store; ADR v3 ADR-010 gives SELECT on ACE tables to a dedicated view-owner role; D-RCV-35 U3
keeps the Workbench out of ACE DDL and U4 forbids a foreign key into ACE. D-RCV-35 and ADR v3 rank
above story files v7. Also declined: any table privilege in `public` (SELECT, INSERT, UPDATE, DELETE,
TRUNCATE, REFERENCES, TRIGGER), `CREATE` on `public`, `ADMIN` on `ace_view_owner`, and any other role
membership. The SELECT grants to `ace_view_owner` stay with the ACE DBA (RWB-ACE-001 v1; TC-ACE-001-04).

### 6.2 What is granted

Orchestrator decision D-RUN-14 (2026-11-18T00:31) gives `rwb_migrator` exactly two rights and
nothing else in `public`:

| Right | Statement | Why it is needed |
|---|---|---|
| R1 | `GRANT USAGE ON SCHEMA public TO rwb_migrator;` — no table privilege | The RWB-E1-069 view migration must resolve `public.<table>` names in `CREATE VIEW ${recoverySchema}.v_ace_* AS … FROM public.<table>` |
| R2 | `GRANT ace_view_owner TO rwb_migrator WITH INHERIT FALSE, SET TRUE;` — `ADMIN` false | The Section A grant block transfers ownership with `ALTER VIEW … OWNER TO ace_view_owner`; PostgreSQL 16 permits an owner change only to a role the current role can `SET ROLE` to. `INHERIT FALSE` means `rwb_migrator` does **not** get `ace_view_owner`'s SELECT unless it runs `SET ROLE` |

```sql
-- infra/postgres/init/20-grants.sql.inc, after REVOKE ALL ON SCHEMA public FROM PUBLIC
GRANT USAGE ON SCHEMA public TO rwb_migrator;
GRANT ace_view_owner TO rwb_migrator WITH INHERIT FALSE, SET TRUE;
```

The existing `GRANT USAGE, CREATE ON SCHEMA recovery TO ace_view_owner` stays, because a new owner
needs `CREATE` on the view's schema. The role comments in `00-roles-and-databases.sh` and the
`20-grants.sql.inc` header say the same thing. The rights are **not** in a recovery migration:
`GRANT` fails `L-GRANT`, and granting a role membership needs a privilege the migrator must not
hold.

### 6.3 Why BR8 still holds

`rwb_migrator` holds `USAGE` only on `public` and does not inherit `ace_view_owner`'s SELECT, so it
holds no `REFERENCES` on an ACE table. An FK into `public` that names the referenced key is refused
by the database as SQLSTATE `42501`. T-044-17 proves, as the superuser from the catalog:

| Check | Expected |
|---|---|
| (a) schema privilege | `USAGE` true, `CREATE` false on `public` |
| (b) membership | exactly one `pg_auth_members` row: `ace_view_owner`, `inherit_option = false`, `set_option = true`, `admin_option = false` |
| (c) role attributes | `rolsuper`, `rolcreaterole`, `rolcreatedb`, `rolbypassrls` all false |
| (d) table privileges | zero of the 62 ACE `public` relations have any of the seven table privileges for `rwb_migrator` (checks inherited privileges too) |
| (e) direct read | `SELECT count(*) FROM public.account` fails with `42501`, detail `permission denied for table account` |
| (f) FK probe | a fixture creating `REFERENCES public.account(id)` through the recovery Flyway bean fails with `42501` and writes no history row |

The detail assertion matters: a `permission denied for schema public` would mean the schema grant
is wrong, not that the table privilege is absent.

### 6.4 Residual risk and where the rights are applied

- **Residual, OI-E044-J.** With `SET TRUE`, a malicious migration could `SET ROLE ace_view_owner` and
  read ACE tables directly. No lint rule shipped here refuses `SET ROLE`; AGENTS.md §3.12 (read ACE
  data only through `recovery.v_ace_*` views) and code review are the control. A blanket ban would
  break a legitimate later migration that must alter a Section A view after the owner change.
- **In this repository** the rights are applied in `infra/postgres/init/`, the local stand-in for the
  environment owner.
- **In SIT, UAT and PROD** the environment owner applies R1 and R2 (OI-E044-I). This repository
  claims no environment change and no test there.
- **Confirmation** by the recovery tech lead is OI-E044-J; D-RUN-14 is applied as the orchestrator's
  decision, not as a human approval.

## 7. The no-production-migration boundary and coverage wiring

**DOC ID:** DOC-RWB-E1-044-012 · **Maps to:** SPEC-RWB-E1-044-014, -015; D-RUN-07; TASK-13, TASK-16; CODE-E044-025, CODE-E044-030, CODE-E044-031

### 7.1 No production migration

| Fact | Value |
|---|---|
| Production folder | `backend/src/main/resources/db/modulemigration/recovery/` |
| Contents | `README.md` only; zero `.sql` files |
| Migration shipped by this story | **None** (D-RCV-28; story v7 §13) |
| `<seq>` fixed anywhere | No (D-RUN-07) |
| Fixtures | `backend/src/test/resources/migration-lint/` (55 folders) and `.../flyway-fixtures/` (10 folders) |
| Fixture numbering | Concrete (`V0001`..) only because the lint checks contiguity from `V0001`; test data, never merged |
| Merged migration edited | No |

If a later story needs a migration for this story's work, it is a separate file named
`V<seq>__rwb_e1_044_<name>.sql` with line 1 `-- Story: RWB-E1-044`, forward only, one file per
story, numbered at merge. The migration-folder README is the rule reference a developer reads before
writing one; it fixes no number and names the RWB-E1-069 seam.

### 7.2 Coverage wiring

`backend/build.gradle.kts` is the one shared file edited (D-RCV-40), and only in the JaCoCo class
directories:

```text
recoveryClasses        all main classes under th/co/scb/ace/demo/recovery/**
boundaryToolingClasses RWB-TE-001's architecture/boundary/** (inherited)
migrationToolingClasses this story's architecture/migration/**   ← added
                       excludes **/*Test.class, **/*Test$*.class, **/*IT.class, **/*IT$*.class
        │
        ├─ recoveryCoverageReport       (XML + HTML; finalizer of `test`)
        └─ recoveryCoverageVerification (one BUNDLE rule: LINE, INSTRUCTION, BRANCH, METHOD ≥ 0.80)
```

- Execution data is the `test` task only; the container suite does not contribute coverage.
- No main class is excluded, no threshold is lowered, no waiver exists, and neither task joins
  `check` (D-RCV-40; D-RCV-28 (3)).
- The `casewf.migration` main classes are already inside `recoveryClasses`; only the new test-scope
  tooling directory needed adding.
- Integration coverage never substitutes for unit coverage; that is why the comparator is split into
  a pure part reached by T-044-19.
- The pre-flight recorded the merged RWB-TE-001 baseline before any change (LINE 0.9746,
  INSTRUCTION 0.9731, BRANCH 0.9531, METHOD 0.9791), and the final bundle is above the gate on all
  four counters (`COMPLIANCE.md` §4).

---
title: "Test scenarios: RWB-TE-011 PDPA lint for code, tests and logs"
run_id: "INC-006-epic-1-RWB-TE-011"
story: "RWB-TE-011"
revision: "v2 (18 Nov 2026): remediation of plan-gate round 1 findings PLAN-001..PLAN-006. The FIXTURE-ID cases now prove the patterns are configuration, and UT-TE011-42 is assigned to named classes and tasks. No scenario is removed."
---

# Test scenarios: RWB-TE-011

Every acceptance criterion, business rule, exception path, T path, SPEC requirement, story test case and added system scenario maps to a named test below, or to an open human-verification item where only the GitLab/ACE host can show the result. Shorthands: `P` = `tools/pdpa-lint`, `M` = `P/src/main/java/th/co/scb/ace/tools/pdpa`, `U` = `P/src/test/java/th/co/scb/ace/tools/pdpa`, `X` = `P/src/test/resources`. "Fixture" means a file or tree written to a temporary directory; "live" means a repository file.

Conventions that apply to every test:

- JUnit 5 and AssertJ, in the tool's `test` task, working directory = repository root. No test starts a Spring context, opens a database or calls the network.
- Every test that produces output asserts that no fixture value, source line or SQL text appears in it (BR7). The helper is `LintHarness.assertNoValue(output, values)`.
- No test is skipped, disabled or weakened. No `@Disabled`, `@Ignore` or assumption. A missing `git` or a missing real input file fails the test loudly.
- Failing FIXTURE-ID values are built by `TestValues` with a fixed seed at run time and never stored.
- `mT` below means a test method name in the named class.

## 1. Acceptance criteria (story file v1 §7)

| AC | Test ID | Named test or item | Expected | Task |
|---|---|---|---|---|
| AC1 | ST-TE011-01 | `LogAndExceptionSystemTest.javaLogCallWithGetterIsAFinding` | exit 1; one PDPA-LOG-FIELD line naming the file, the line and `first_name`; no value in the output | TASK-15, TASK-29 |
| AC2 | ST-TE011-02 | `LogAndExceptionSystemTest.logCallWithWholeEntityIsAFinding` | PDPA-LOG-ENTITY for `CustomerEntity`; the same for a `CustomerView` variant and for `PartyEntity` with a personal member | TASK-15, TASK-29 |
| AC3 | ST-TE011-03 | `FixtureSystemTest.nationalIdGeneratedAtRunTimeIsAFinding` | PDPA-FIXTURE-ID with field `thai_national_id`; the number is absent from the output; the temporary file is deleted | TASK-21, TASK-29 |
| AC4 | ST-TE011-04 | `FixtureSystemTest.fixtureFieldWithoutSyntheticPrefixIsAFinding` | PDPA-FIXTURE-FIELD for `last_name` with `TESTNAME`; exit 0 with a `SYN-LAST-0001` value | TASK-17, TASK-19, TASK-29 |
| AC5 | ST-TE011-05 | `DictionarySystemTest.markingByMigrationRegeneratesTheRules` | dictionary v1 passes `getContractNo`; a form-R2 migration and a form-R1 multi-row variant each add `contract_no` and produce PDPA-LOG-FIELD | TASK-07, TASK-09, TASK-15 |
| AC6 | ST-TE011-06 | `FixtureSystemTest.expiredAllowEntryFailsTheBuild` | run as of 2026-12-01: exit 1, the finding line and `allow entry expired: PDPA-FIXTURE-FIELD ... since 2026-11-30`; run as of 2026-11-30: exit 0 | TASK-23, TASK-29 |
| AC7 | ST-TE011-07 | `LogAndExceptionSystemTest.typeScriptLogCallIsAFinding` | PDPA-LOG-FIELD naming `lastName` in the parentheses form | TASK-15, TASK-29 |
| AC8 | ST-TE011-08 | `LogAndExceptionSystemTest.maskingHelperExemptsTheUse` | no finding for the line that passes the field through the configured helper | TASK-15 |
| AC9 | ST-TE011-09 | `LogAndExceptionSystemTest.exceptionMessageWithGetterIsAFinding` | PDPA-EXCEPTION for `cif_no` | TASK-15, TASK-29 |
| AC10 | ST-TE011-10 | `LogAndExceptionSystemTest.implicitAndExplicitTextFormsAreFindings` | PDPA-TOSTRING for `contact_value` in the implicit record and the explicit `toString()` | TASK-15, TASK-29 |
| X1–X11 | §5 below | X1..X11 rows | the listed behaviour | TASK-15, TASK-21, TASK-23, TASK-27, TASK-29, TASK-31 |
| BR1–BR7 | §2 below | BR1..BR7 rows | the listed behaviour | TASK-03, TASK-07, TASK-09, TASK-15, TASK-17, TASK-19, TASK-21, TASK-23, TASK-29 |
| TC-TE-011-11 | HV-01 | host item | code-owner approval refused on the real host; `BLOCKED — NOT_TESTED_HERE` | TASK-31 |

## 2. Business rules (story file v1 §8)

| BR | Test ID(s) | Named test | Expected |
|---|---|---|---|
| BR1 | UT-TE011-01, -05..-11; ST-TE011-05, -11 | `PersonalFieldReaderTest`, `RuleGeneratorTest`, `DictionarySystemTest` | the field list comes only from the dictionary and the API marks; no field name in code |
| BR2 | UT-TE011-16..-19; ST-TE011-01, -02, -07, -09 | `LogScannerTest`, `LogAndExceptionSystemTest` | every log, exception and text-form use of a personal field or entity is a finding |
| BR3 | UT-TE011-27..-30; ST-TE011-04, -14, -15 | `SqlFixtureScannerTest`, `FixturePositionScannerTest`, `JsonFixtureScannerTest`, `FixtureSystemTest` | a non-synthetic literal in a personal position is a finding; `NULL`, empty and `DEFAULT` are not |
| BR4 | UT-TE011-31..-34; ST-TE011-03 | `FixtureIdMatcherTest`, `FixtureSystemTest` | a valid national ID, a Thai mobile and an address outside the example domains fail anywhere |
| BR5 | UT-TE011-20; ST-TE011-10 | `LogScannerTest.textFormRules`, `LogAndExceptionSystemTest` | a text form that includes a personal member is a finding |
| BR6 | UT-TE011-35; ST-TE011-06 | `AllowListTest`, `FixtureSystemTest` | only a valid, unexpired entry with owner and reason excuses a finding |
| BR7 | UT-TE011-40; every ST | `ReportTest`, `LintHarness` | no value, source line or SQL text in any output; tested in every case |

## 3. System tests (full lint over a temporary tree)

`ST-TE011-01..10` are story test cases TC-TE-011-01..10. `ST-TE011-11..19` are the added scenarios TS-TE011-01..09. `ST-TE011-20` is the recorded real-repository run (FTS-03), not a unit test.

| ST | Source | Class and method | Expected |
|---|---|---|---|
| ST-TE011-01 | TC-01, AC1 | `U/system/LogAndExceptionSystemTest.javaLogCallWithGetterIsAFinding` | exit 1; one PDPA-LOG-FIELD; file, line and `first_name`; no value |
| ST-TE011-02 | TC-02, AC2 | `U/system/LogAndExceptionSystemTest.logCallWithWholeEntityIsAFinding` | PDPA-LOG-ENTITY for `CustomerEntity`, `CustomerView` and `PartyEntity` with a personal member |
| ST-TE011-03 | TC-03, AC3 | `U/system/FixtureSystemTest.nationalIdGeneratedAtRunTimeIsAFinding` | PDPA-FIXTURE-ID `thai_national_id`; no number in the output; the temp file is gone |
| ST-TE011-04 | TC-04, AC4 | `U/system/FixtureSystemTest.fixtureFieldWithoutSyntheticPrefixIsAFinding` | finding for `TESTNAME`; exit 0 for the `SYN-` value |
| ST-TE011-05 | TC-05, AC5 | `U/system/DictionarySystemTest.markingByMigrationRegeneratesTheRules` | two variants (R2 and R1 multi-row) each add `contract_no` and yield PDPA-LOG-FIELD; dictionary v1 passes |
| ST-TE011-06 | TC-06, AC6 | `U/system/FixtureSystemTest.expiredAllowEntryFailsTheBuild` | exit 1 with the finding and the expired line on 2026-12-01; exit 0 on 2026-11-30 |
| ST-TE011-07 | TC-07, AC7 | `U/system/LogAndExceptionSystemTest.typeScriptLogCallIsAFinding` | PDPA-LOG-FIELD with `lastName` in parentheses |
| ST-TE011-08 | TC-08, AC8 | `U/system/LogAndExceptionSystemTest.maskingHelperExemptsTheUse` | no finding for the helper call; a nested argument is also exempt |
| ST-TE011-09 | TC-09, AC9 | `U/system/LogAndExceptionSystemTest.exceptionMessageWithGetterIsAFinding` | PDPA-EXCEPTION for `cif_no` |
| ST-TE011-10 | TC-10, AC10 | `U/system/LogAndExceptionSystemTest.implicitAndExplicitTextFormsAreFindings` | PDPA-TOSTRING for `contact_value` in the record and in the explicit `toString()` |
| ST-TE011-11 | TS-01 | `U/system/DictionarySystemTest.dictionarySeedTablesRaiseNoFinding` | 0 findings on every `sys_fields`, `sys_objects` and `data_product` row; exactly 1 finding on the business-table row; an allow entry on the file gives exit 2; the negative `reviewer_name` variant gives exactly 1 finding; the dictionary describes every seed column before the run |
| ST-TE011-12 | TS-02 | `U/system/FixtureSystemTest.pointInTimeDictionaryIsUsed` | no finding on A; one notice naming A's file and line; a test SQL fixture outside the folder gives a finding |
| ST-TE011-13 | TS-03 | `U/system/FixtureSystemTest.sourceFieldKeyMatches` | finding for `last_name (surname)` |
| ST-TE011-14 | TS-04 | `U/system/FixtureSystemTest.unresolvedObjectsFollowTheNameRule` | (a) `it_customer.first_name` finding and the `SYN-` value none; (b) `InteractionRequest.summary` finding and the `SYN-` value none; (c) `TimelineItem` finding; (d) `summary` still a finding when made ambiguous; (e) `public.address.address` finding under the union dictionary; no value in the output |
| ST-TE011-15 | TS-05 | `U/system/FixtureSystemTest.sqlWithNoNamedColumnFailsClosed` | (a) `(columns not named)`; (b) `COPY ... FROM stdin` same; (c) `DEFAULT VALUES` none; (d) the same file in the migration folder with an allow entry gives exit 2; no value |
| ST-TE011-16 | TS-06 | `U/system/CorrectiveMigrationSystemTest.correctiveMigrationConditions` | (a) exit 1; (b) exit 0 with one `corrected by` notice; (c) exit 1 for a different story key; (d) exit 1 for no named file; (e) exit 1 for a lower sequence; (f) exit 2 for an unknown file; (g) exit 1 with no write on the table; (h) exit 1 with a finding in C; (i) exit 1 when the changed-file list holds O; (j) exit 2 with an allow entry on O; no value |
| ST-TE011-17 | TS-07 | `U/system/SqlClassSystemTest.statementClasses` | 0 findings for the accepted forms and the guards; exactly one finding per listed violation, with the listed field label; `COPY ... TO` and a `DROP FUNCTION` guard raise nothing; no SQL text |
| ST-TE011-18 | TS-08 | `U/system/LintFixtureSystemTest.lintFixturesGetFixtureIdOnly` | default configuration: exit 0, 0 findings, a `PDPA-SCOPE: lint fixtures` line with the count; a run-time number in a temp copy gives exit 1 with PDPA-FIXTURE-ID and no number; the same tree under `other-sql` gives exit 2; a lint-fixture root over the migration folder gives exit 2; a root over `backend/src/main/java` gives exit 2 |
| ST-TE011-19 | TS-09 | `U/system/ChangedFileSystemTest.changedFileListDecisions` | (a) to (l) exactly as the spec: built, not built, exit 2 for a missing target, no merge base, `branch not determined`, O on the list, no target table, the squashed promotion and the missing target in a clone; one scope line per case |
| ST-TE011-20 | SPEC-016 state (1) | recorded run, TASK-33 (`implement/baseline-run.log`, `implement/baseline-files.md`) | exit 0, 0 findings, the notice and scope lines, every file merged by orders 1–5 listed with its result, the state named (state (1); state (2) is RWB-E1-001's merge condition), and the residual-risk limit beside the result |

## 4. Unit tests

| UT | Area | Cases | Expected | Trace | Task |
|---|---|---|---|---|---|
| UT-TE011-01 | Configuration | production file parses with every section and default; unknown key; missing file; wrong type; root, exclusion, lint-fixture and `except` keys; a pattern with no `forms`, a form that does not compile, a duplicate pattern name and a checksum whose `weights` length is not `digitCount - 1`; `changedFiles` defaults; empty allow list parses | exact `configuration invalid` or `configuration not readable` line; the production values as `data-model.md` §3 | SPEC-015 | TASK-02, TASK-03 |
| UT-TE011-02 | Scan configuration validation | a lint-fixture root outside the test roots; a root over `infra/**`; an accepted root under `backend/src/test/resources/x/**` | exit 2 `lint-fixture root outside the test roots: {key}`; the accepted root passes | SPEC-003 | TASK-02, TASK-03 |
| UT-TE011-03 | Repository layout | `classpath:db/modulemigration/recovery` maps to `backend/src/main/resources/db/modulemigration/recovery`; missing key; `${...}` placeholder; non-classpath value; `dictionary.migrationFolder` equal and different | exact `migration folder does not match rwb.flyway.location` failures; equal path accepted; the live `application.yaml` reads `classpath:db/modulemigration/recovery` | SPEC-003, -015 | TASK-02, TASK-03 |
| UT-TE011-04 | SQL splitter | single and doubled quotes; `E'...'`; `$$` and `$tag$` bodies; nested block comment; line comment; `${recoverySchema}` is not a dollar quote; `sys_fields` in a literal or comment is not a target; psql meta-commands; unterminated literal, quoted identifier, block comment, dollar body; start lines | statements split with 1-based lines; `source not parsable: {file}:{line}` for each unterminated case; no text in the message | SPEC-001, -008 | TASK-04, TASK-05 |
| UT-TE011-05 | Reader R1 | single row; multi-row with mixed true and false; reordered columns; `${recoverySchema}.`, `recovery.` and quoted `"sys_fields"`; omitted `is_personal` defaults false; `source_field` key kept; `is_active = false` still listed | the expected (object, field) and personal flags; exit 0 | SPEC-001 | TASK-06, TASK-07 |
| UT-TE011-06 | Reader R2 | `WHERE field_id = '<id>'`; `WHERE field_id IN (...)`; a `true` to `false` change | the mark set; one `PDPA-NOTICE: {field_id} unmarked at {file}:{line}`; exit unchanged | SPEC-001 | TASK-06, TASK-07 |
| UT-TE011-07 | Reader ignored | `UPDATE ... SET description ...`; `CREATE TABLE sys_fields`; `CREATE INDEX`; `COMMENT ON`; `ALTER TABLE ... ADD CONSTRAINT`; a view that reads it; an FK in another table in `CREATE TABLE` and in `ALTER TABLE`; `GRANT` and `REVOKE` | the field list is unchanged; exit 0 | SPEC-001 | TASK-06, TASK-07 |
| UT-TE011-08 | Reader fail closed | `UPDATE` of `is_personal` by object name; `UPDATE` with a subquery; `UPDATE` of `field_name`; `DELETE`; `TRUNCATE`; `COPY ... FROM` and `\copy`; `INSERT ... SELECT`; `INSERT ... ON CONFLICT DO UPDATE` of `is_personal`; `MERGE`; `ALTER TABLE ... ALTER COLUMN`; `DROP TABLE`; a `DO` block naming it; a function body; a non-literal `is_personal`; an unknown `field_id`; a duplicate across migrations | exit 2 with the exact line for each case; no SQL text | SPEC-001 | TASK-06, TASK-07 |
| UT-TE011-09 | Reader order and snapshots | a migration row replaces a baseline row; an unreplaced baseline row stays; a duplicate in two migrations; a point-in-time snapshot after each file | the expected lists; duplicate exit 2; the snapshot excludes later marks | SPEC-001, -008 | TASK-06, TASK-07 |
| UT-TE011-10 | Dictionary inputs | the real Physical Schema v6 copy yields 18 personal fields and no exit 2; the real API v4 yields the 5 names and pairs; a missing, unparsable and empty dictionary; an empty union; camel to snake | 18 fields; 5 API names; the exact exit-2 lines | SPEC-001, -016 | TASK-06, TASK-07 |
| UT-TE011-11 | Rule generator and rules file | variants for `id_no_last4` and `extracted_fields`; entity names with both suffixes; object and source-field keys; ambiguity over every row; API names; two runs byte-identical; no timestamp; sorted | the shape of `data-model.md` §1; byte-identical files | SPEC-002 | TASK-08, TASK-09 |
| UT-TE011-12 | Scan scope classes | every class; the overlap precedence; per-root `except`; a file directly under each root (top level) and a nested file; an exclusion that matches no migration with its count; Windows separators | each file in exactly the expected classes; counts printed; the top-level and nested files both matched | SPEC-003, -015 | TASK-10, TASK-11 |
| UT-TE011-13 | Scan scope probes | a root list without the migration class and an empty folder; an exclusion `backend/src/main/resources/db/**`; an exclusion matching one migration; a lint-fixture root covering the folder; a probe path uncovered | exit 2 with `scan configuration excludes the migration folder: {key}` for each; the correct key printed | SPEC-003, -018 | TASK-10, TASK-11 |
| UT-TE011-14 | Source lexer | Java strings, char, text blocks, comments, annotations; TypeScript strings, template literal parts and `${...}` expressions, regex literals; a personal name in a string is a literal token; unterminated source | token kinds and offsets; `source not parsable` for the unterminated case | SPEC-004..-007 | TASK-12, TASK-13 |
| UT-TE011-15 | Source index | field, parameter, local, record component, `var`; TypeScript annotation; `@Table(name = ...)`; `components["schemas"]["..."]` from `schema.d.ts`; a member list per type | the declarations and resolved types; a type with a personal member | SPEC-004..-007 | TASK-12, TASK-13 |
| UT-TE011-16 | LOG-FIELD Java | getter; member access; record accessor; concatenation; `String.format`; `StringBuilder`; `MessageFormat`; bare identifier; fluent SLF4J; `System.out` and `System.err`; a personal name inside a string literal; a non-logger method | a finding for each use; none for the literal and the non-logger | SPEC-004 | TASK-14, TASK-15 |
| UT-TE011-17 | LOG-FIELD TypeScript | `console.log`, `info`, `warn`, `error`, `debug`, `trace`; a configured `tsLoggerNames` call; template literal; property access; a literal text | findings for the uses; none for the literal | SPEC-004 | TASK-14, TASK-15 |
| UT-TE011-18 | LOG-ENTITY | `CustomerEntity`, `CustomerView`, `PartyEntity` with a personal member; `this`; `String.valueOf`; concatenation; `.toString()`; a member access after the identifier; a type from `@Table`; a type from `schema.d.ts` | findings for the whole-object uses; none for the member access and the non-personal type | SPEC-005 | TASK-14, TASK-15 |
| UT-TE011-19 | EXCEPTION | `new X(...)` with an `Exception`, `Error`, `Throwable` and a configured suffix; a personal field argument; a whole entity argument; a nested call; a non-exception constructor | findings for each case; none for the non-exception | SPEC-006 | TASK-14, TASK-15 |
| UT-TE011-20 | TOSTRING | a record with no `toString()`; an explicit `toString()` that uses a member; a record with an explicit `toString()` that excludes it; a class with no personal member; a TypeScript class | one finding per personal member in the first two cases; none in the last two | SPEC-007 | TASK-14, TASK-15 |
| UT-TE011-21 | Masking exemption | a configured Java helper; a nested argument; a TypeScript `module#function`; an unconfigured helper; the exemption for LOG, EXCEPTION and TOSTRING only | no finding through the helper; a finding when not configured | SPEC-010 | TASK-14, TASK-15 |
| UT-TE011-22 | SQL class 1 | `ON CONFLICT (k) DO NOTHING`; `ON CONFLICT ON CONSTRAINT`; `DO UPDATE SET c = literal` (a position); `SET c = EXCLUDED.c` (not); `RETURNING`; read-only `WITH`; `INSERT ... SELECT ... WHERE NOT EXISTS`; `UPDATE ... FROM ... WHERE`; `'x'::text` as a literal | 0 findings when no literal is in a personal position; one per personal literal | SPEC-008 | TASK-16, TASK-17 |
| UT-TE011-23 | SQL class 2 and DEFAULT | `CREATE`, `ALTER`, `DROP` of the listed object kinds; `ALTER` and `DROP` function and procedure; `COMMENT ON`; `GRANT`, `REVOKE`; `SET`, `RESET`; transaction control; `SELECT` without `INTO`; `DELETE`, `TRUNCATE`, maintenance; `COPY ... TO`; psql meta; empty; `DEFAULT` on a personal pair, a non-personal pair and `NULL`; `ADD COLUMN ... DEFAULT`; `SET DEFAULT` | no finding except the non-`SYN-` `DEFAULT` on a resolved personal pair; a non-text `DEFAULT` is a finding | SPEC-008 | TASK-16, TASK-17 |
| UT-TE011-24 | SQL class 3 `DO` | `SELECT INTO`, `PERFORM`, assignment, `IF`, `CASE`, loops, `EXIT`, `CONTINUE`, `GET DIAGNOSTICS`, cursors, `RAISE`, `ASSERT`, `RETURN`, `NULL`; a direct class-2 statement; a direct `ALTER TABLE ... ADD CONSTRAINT` guard; `EXECUTE 'literal'` of class 2; `format` with `%I` in positional, width and flag forms; `%s` and `%L` in each form; `%%`; `COMMENT ON ... IS` text; a placeholder `DEFAULT`; a literal `DEFAULT` on a personal pair; `INSERT`, `UPDATE`, `MERGE`, `COPY ... FROM`, `CALL`, a non-literal `EXECUTE`, `ALTER ROLE`, `CREATE TABLE ... AS` | no finding for the accepted forms; the `(DML in procedural body)` finding at the block's first line for each catch-all; the literal `DEFAULT` gives its FIXTURE-FIELD finding at the `EXECUTE` line | SPEC-008 | TASK-16, TASK-17 |
| UT-TE011-25 | SQL class 3 function and procedure | a body `INSERT` with a personal literal; `INSERT ... VALUES (NEW.c)`; a variable value; reads and control flow; a direct class-2 statement; `EXECUTE` of class-2 literal text; `MERGE`, `COPY ... FROM`, a column-less `INSERT` with a literal, `CALL`, any other `EXECUTE`, a class-4 statement | findings only for the literal in a personal position and for the catch-all cases; no finding for `NEW.c` or a variable | SPEC-008 | TASK-16, TASK-17 |
| UT-TE011-26 | SQL class 4 | `MERGE`; `CALL`; top-level `EXECUTE`; `PREPARE`; `SELECT ... INTO <table>`; `CREATE TABLE ... AS`; a data-modifying `WITH`; `IMPORT FOREIGN SCHEMA`; `ALTER ROLE`, `ALTER DATABASE`, `ALTER SYSTEM`; an unknown keyword | one `(statement not recognised)` finding at the statement's first line; no SQL text | SPEC-008 | TASK-16, TASK-17 |
| UT-TE011-27 | SQL columns not named | column-less `INSERT ... VALUES` with a literal; with only `NULL` or `DEFAULT`; column-less `INSERT ... SELECT` with and without a literal; `COPY ... FROM stdin`, `COPY ... FROM '<file>'`, `\copy ... from`; `COPY ... TO`; `INSERT ... DEFAULT VALUES` | `(columns not named)` for the literal cases and the `COPY` forms; none for the others | SPEC-008 | TASK-16, TASK-17 |
| UT-TE011-28 | SQL positions | single and multi-row values; `INSERT ... SELECT` at a personal column; `UPDATE SET`; `ON CONFLICT DO UPDATE`; resolved, described and unresolved pairs; a `source_field` key; the six seed tables; non-text date and numeric values; `NULL`, empty string and `DEFAULT`; `SYN-`; a `sys_fields` statement in a non-reader file; reader precedence in a reader file | findings only on resolved personal pairs with a non-`SYN-` non-null literal; a notice for a described non-personal pair; reader exit 2 in the reader file | SPEC-008, -018 | TASK-16, TASK-17 |
| UT-TE011-29 | Java and TypeScript positions | `setXxx(literal)`, builder `.xxx(literal)`, `receiver.xxx = literal`, object literal `xxx: literal`; resolution by generated entity, `@Table`, `schema.d.ts`; untyped; unambiguous name; ambiguous name; API personal name in an API-typed position; `null`, empty string; non-text literal | a finding for each resolved personal or unambiguous case; a notice for an unresolved ambiguous case; none for `null` and empty; an API name is a finding even when ambiguous | SPEC-008 | TASK-18, TASK-19 |
| UT-TE011-30 | JSON positions | `fixtureObjects` glob for a nested key; no entry (unresolved); an array of objects; unambiguous and ambiguous names; an API-typed JSON file; a missing or malformed JSON | a finding for the resolved or unambiguous case; a notice for the ambiguous case; `source not parsable` for malformed JSON | SPEC-008 | TASK-18, TASK-19 |
| UT-TE011-31 | FIXTURE-ID check digit | valid; invalid; dashed form; 12 and 14 digits; digit adjacency; a 13-digit run with an invalid check digit; the dashed form removed from the `thai_national_id` pattern's `forms` | a match only for a valid, non-adjacent value; no match for the removed dashed form | SPEC-009, -015 | TASK-20, TASK-21 |
| UT-TE011-32 | FIXTURE-ID mobile | national 3-3-4; international 2-3-4; bare country code; `-` and space separators; adjacency; the two bare `66` forms removed from the `thai_mobile` pattern's `forms` | a match for each built value; none for a longer digit run; with the forms removed a bare `66` value no longer matches and `+66` still does | SPEC-009, -015 | TASK-20, TASK-21 |
| UT-TE011-33 | FIXTURE-ID e-mail | `example.com`; `sub.example.org`; `x.test`; another domain built at run time; subdomains of the reserved TLDs; `.test` removed from the email `exemptDomainSuffixes` | no match for the example and reserved domains; one match for the other domain; with the suffix removed an `x.test` address becomes a match | SPEC-009, -015 | TASK-20, TASK-21 |
| UT-TE011-34 | FIXTURE-ID all roots and self-scan | a match in a comment, a string, a SQL value and a tool source; a stored value under `P` fails the self-scan; a lint-fixture file gets FIXTURE-ID only; no value in the message | one finding with the pattern name; the self-scan fails; no value printed | SPEC-009, -003 | TASK-20, TASK-21 |
| UT-TE011-35 | Allow list | valid `line`; valid `pattern`; missing `owner`, `reason` or `expires`; both `line` and `pattern`; an invalid date; an expired entry that matches; an expired entry that matches nothing; an entry matching the migration folder by exact path and by `**/*.sql`; entry index | the entry excuses; `allow entry expired`; unused expired passes; invalid and migration entries exit 2 with `entries[n]` | SPEC-011 | TASK-22, TASK-23 |
| UT-TE011-36 | Changed-file decision | target and branch matrix; `origin/` prefix; protected branches; a branch added to the configuration; no option; missing, empty and `HEAD` branch; a fake runner records every call | built only for the target branch from a non-protected branch; zero calls otherwise; exit 2 `branch not determined` for the three bad branches | SPEC-013 | TASK-24, TASK-25 |
| UT-TE011-37 | Changed-file git | added, modified and renamed files; deleted file excluded; paths relative; target missing; no merge base (unrelated histories and a depth-1 clone); a stale ref with a failed fetch | the exact list; `target branch not found`; `no merge base`; never an empty list | SPEC-013, -018 | TASK-24, TASK-25 |
| UT-TE011-38 | Corrective naming | one and two names; no `-- Fix:`; empty reason; a token that is not a name; an unknown file; a `-- Fix:` line outside the folder | names parsed; unknown file exit 2 at `{file}:2`; a line outside the folder is ignored | SPEC-018 | TASK-26, TASK-27 |
| UT-TE011-39 | Corrective acceptance | each condition (a)–(e) failing in turn; every target-table row of `data-model.md` §5.4; a placeholder column (table write alone); a placeholder table (never accepted); no target table (a)–(c) and (e); a finding in C; a second C | only the full condition set accepts; the accepted finding becomes the `corrected by` notice | SPEC-018 | TASK-26, TASK-27 |
| UT-TE011-40 | Report and exit codes | sort by file, line, rule, field; field and token parentheses; expired line; four notices; four counts; scope lines and class order; exit 0, 1 and 2; two runs identical; no value in any line | the exact order and text; exit codes; byte-identical two runs | SPEC-012 | TASK-28, TASK-29 |
| UT-TE011-41 | Step over a tree | the step with a complete config and tree; a config error before scanning; a dictionary error; a missing scan root; the rules file written before the scan | the expected exit code and lines; the rules file exists after a scan-reaching run and not after a dictionary failure | SPEC-012, -016 | TASK-28, TASK-29 |
| UT-TE011-42 | Self-scan and baseline inputs | reader half (`PersonalFieldReaderTest`): the real Physical Schema v6 copy and API v4 read as inputs, and the dictionary is not read from a database; scope half (`ScanScopeTest`): the tool's own tree is classified `tool` and a lint-fixture file is classified there only and not parsed for FIXTURE-FIELD | 18 fields, 5 API names, no database opened; no FIXTURE-FIELD on the tool tree; no exit 2 from a lint fixture | SPEC-001, -003, -016 | TASK-06, TASK-07, TASK-10, TASK-11 |
| UT-TE011-43 | Repository configuration | `.gitlab-ci.yml` job, stage, three rules, `GIT_DEPTH`, git install, target variable equals `changedFiles.targetBranch`, artifacts, script text; `.gitlab/CODEOWNERS` section and line; `scripts/dev.ps1` command, helper and `test` step | every assertion holds; a missing or drifted item fails with its name | SPEC-013, -014 | TASK-30, TASK-31 |

## 5. Exception paths (spec "Exceptional-case behaviour")

| ID | Test ID(s) | Expected |
|---|---|---|
| X1 | ST-TE011-01, UT-TE011-16 | PDPA-LOG-FIELD; build fails (exit 1) |
| X2 | ST-TE011-02, UT-TE011-18 | PDPA-LOG-ENTITY; exit 1 |
| X3 | ST-TE011-03, UT-TE011-31 | PDPA-FIXTURE-ID `thai_national_id`; exit 1 |
| X4 | ST-TE011-04, UT-TE011-28 | PDPA-FIXTURE-FIELD; exit 1 |
| X5 | ST-TE011-05, UT-TE011-11 | rules regenerated; the new use is a PDPA-LOG-FIELD finding |
| X6 | ST-TE011-06, UT-TE011-35 | finding line plus `allow entry expired: ...`; exit 1 |
| X7 | ST-TE011-07, UT-TE011-17 | PDPA-LOG-FIELD; exit 1 |
| X8 | ST-TE011-08, UT-TE011-21 | no finding; exit 0 |
| X9 | ST-TE011-09, UT-TE011-19 | PDPA-EXCEPTION; exit 1 |
| X10 | ST-TE011-10, UT-TE011-20 | PDPA-TOSTRING; exit 1 |
| X11 | UT-TE011-43, HV-01 | the line is present and valid; the host refuses a non-code-owner approval |
| T1 | UT-TE011-10, UT-TE011-01 | exit 2, file name only; an empty list gives `dictionary is empty` |
| T2 | UT-TE011-35 | exit 2 with the entry index |
| T3 | UT-TE011-14, ST-TE011-18 | exit 2 with file and line, no source text; a lint fixture never gives exit 2 from content |
| T4 | UT-TE011-08 | exit 2 with `dictionary statement not supported` or the duplicate or unknown-ID line; no SQL text |
| T5 | UT-TE011-06, UT-TE011-09 | `PDPA-NOTICE: {field_id} unmarked at {file}:{line}`; exit unchanged |
| T6 | UT-TE011-29, UT-TE011-30, ST-TE011-14 | `PDPA-NOTICE: ... object not resolved for {field} ...`; no finding; exit unchanged |
| T7 | UT-TE011-09, ST-TE011-12 | `PDPA-NOTICE: ... seeds {field}, marked personal by a later migration`; no finding |
| T8 | UT-TE011-10, TASK-34 | no output; the limit statement is in the evidence |
| T9 | UT-TE011-27, ST-TE011-15 | PDPA-FIXTURE-FIELD `(columns not named)`; no value |
| T10 | UT-TE011-24, UT-TE011-25, UT-TE011-26, ST-TE011-17 | `(statement not recognised)` or `(DML in procedural body)`; no SQL text |
| T11 | UT-TE011-38, UT-TE011-39, ST-TE011-16 | `corrected by` notice; unknown file exit 2 |
| T12 | UT-TE011-02, UT-TE011-13, ST-TE011-18 | exit 2 with the named configuration key |
| T13 | ST-TE011-18, UT-TE011-34 | no parse, no class finding, never exit 2; FIXTURE-ID only |
| T14 | UT-TE011-36, UT-TE011-37, ST-TE011-19 | exit 2 with `target branch ... not found`, `no merge base with ...` or `branch not determined` |
| T15 | UT-TE011-36, ST-TE011-19 | `PDPA-SCOPE: changed-file list not built ...`; no git call; condition (e) not evaluated |

## 6. SPEC to test

| SPEC | System tests | Unit tests |
|---|---|---|
| SPEC-TE011-001 | ST-TE011-05, -11, -12, -13 | UT-TE011-04..10, -42 |
| SPEC-TE011-002 | ST-TE011-05 | UT-TE011-11 |
| SPEC-TE011-003 | ST-TE011-18 | UT-TE011-02, -12, -13, -34, -42 |
| SPEC-TE011-004 | ST-TE011-01, -07 | UT-TE011-16, -17 |
| SPEC-TE011-005 | ST-TE011-02 | UT-TE011-18 |
| SPEC-TE011-006 | ST-TE011-09 | UT-TE011-19 |
| SPEC-TE011-007 | ST-TE011-10 | UT-TE011-20 |
| SPEC-TE011-008 | ST-TE011-04, -13, -14, -15, -17 | UT-TE011-22..30 |
| SPEC-TE011-009 | ST-TE011-03 | UT-TE011-31..34 |
| SPEC-TE011-010 | ST-TE011-08 | UT-TE011-21 |
| SPEC-TE011-011 | ST-TE011-06 | UT-TE011-35 |
| SPEC-TE011-012 | all ST; ST-TE011-20 | UT-TE011-40, -41 |
| SPEC-TE011-013 | ST-TE011-19 | UT-TE011-36, -37, -43 |
| SPEC-TE011-014 | HV-01, HV-02 | UT-TE011-43 |
| SPEC-TE011-015 | — | UT-TE011-01, -03, -31..33 |
| SPEC-TE011-016 | ST-TE011-11, ST-TE011-20 | UT-TE011-10, -42 |
| SPEC-TE011-017 | ST-TE011-20 | TASK-00 and TASK-34 checks |
| SPEC-TE011-018 | ST-TE011-16, -19 | UT-TE011-38, -39 |

## 7. Test class map

| Class | Unit tests | System tests |
|---|---|---|
| `U/config/ConfigLoaderTest` | UT-TE011-01, -02 | — |
| `U/config/RepositoryLayoutTest` | UT-TE011-03 | — |
| `U/sql/SqlSplitterTest` | UT-TE011-04 | — |
| `U/dictionary/PersonalFieldReaderTest` | UT-TE011-05..10, -42 | — |
| `U/dictionary/ApiSpecificationReaderTest` | UT-TE011-10 | — |
| `U/dictionary/RuleGeneratorTest` | UT-TE011-11 | — |
| `U/report/RulesFileWriterTest` | UT-TE011-11 | — |
| `U/scan/ScanScopeTest` | UT-TE011-12, -13, -42 | — |
| `U/scan/SourceLexerTest` | UT-TE011-14 | — |
| `U/scan/SourceIndexTest` | UT-TE011-15 | — |
| `U/scan/LogScannerTest` | UT-TE011-16..21 | — |
| `U/scan/SqlFixtureScannerTest` | UT-TE011-22..28 | — |
| `U/scan/FixturePositionScannerTest` | UT-TE011-29 | — |
| `U/scan/JsonFixtureScannerTest` | UT-TE011-30 | — |
| `U/scan/FixtureIdMatcherTest` | UT-TE011-31..34 | — |
| `U/scan/CorrectiveMigrationsTest` | UT-TE011-38, -39 | — |
| `U/allow/AllowListTest` | UT-TE011-35 | — |
| `U/changes/ChangedFileListTest` | UT-TE011-36, -37 | — |
| `U/report/ReportTest` | UT-TE011-40 | — |
| `U/PdpaLintStepTest` | UT-TE011-41 | — |
| `U/system/LogAndExceptionSystemTest` | — | ST-TE011-01, -02, -07, -08, -09, -10 |
| `U/system/FixtureSystemTest` | — | ST-TE011-03, -04, -06, -12..15 |
| `U/system/DictionarySystemTest` | — | ST-TE011-05, -11 |
| `U/system/SqlClassSystemTest` | — | ST-TE011-17 |
| `U/system/LintFixtureSystemTest` | — | ST-TE011-18 |
| `U/system/CorrectiveMigrationSystemTest` | — | ST-TE011-16 |
| `U/system/ChangedFileSystemTest` | — | ST-TE011-19 |
| `U/system/RepositoryConfigTest` | UT-TE011-43 | — |

## 8. Human verification (open; never reported as passed here)

| ID | Item | Owner | Status |
|---|---|---|---|
| HV-01 | On the real repository host, a merge request whose `pdpa-lint` job fails cannot merge, and an approval from a non-code-owner does not satisfy the `[Recovery module]` rule (TC-TE-011-11, X11) | ACE platform with the recovery tech lead (OPEN-038) | `BLOCKED — NOT_TESTED_HERE` |
| HV-02 | A merge request pipeline exists for every merge request and holds `pdpa-lint`; a branch pipeline and a tag pipeline also hold it; the runner's delete-then-fetch and `GIT_DEPTH: 0` behave as SPEC-TE011-013 describes | ACE platform | `OPEN — NOT_TESTED_HERE` |
| HV-03 | The ACE pipeline runs the same check on the `develop-recovery` merge request (D-RCV-50) | ACE platform | `OPEN — NOT_TESTED_HERE` |
| HV-04 | The Artifact keeps `pdpa-rules.yaml` and the console log on a failed run, and the job blocks the merge | ACE platform | `OPEN — NOT_TESTED_HERE` |

## 9. Story test cases (TC-TE-011-01..11)

| TC | Test ID | Status |
|---|---|---|
| TC-TE-011-01 | ST-TE011-01 | automated |
| TC-TE-011-02 | ST-TE011-02 | automated |
| TC-TE-011-03 | ST-TE011-03 | automated |
| TC-TE-011-04 | ST-TE011-04 | automated |
| TC-TE-011-05 | ST-TE011-05 | automated |
| TC-TE-011-06 | ST-TE011-06 | automated |
| TC-TE-011-07 | ST-TE011-07 | automated |
| TC-TE-011-08 | ST-TE011-08 | automated |
| TC-TE-011-09 | ST-TE011-09 | automated |
| TC-TE-011-10 | ST-TE011-10 | automated |
| TC-TE-011-11 | HV-01 | `BLOCKED` until OPEN-038 and RWB-TE-002's host exist; never reported as passed |

## 10. Data and leak rules applied to every test

- Every fixture value is synthetic. No real name, address, account number, identifier, credential or production value appears in any test, fixture or log.
- Any value that would match a FIXTURE-ID pattern is built by `TestValues` at run time with a fixed seed and is never written to a file under version control. The self-scan of `P` (UT-TE011-34) fails the build if one is stored.
- Every test that produces output asserts the absence of every value it supplied, and of any source line or SQL statement text (BR7). The assertion is part of the test, not a manual review.
- A failing test is reported with its command, exit code and first failing assertion; no result is invented.

# Recovery migrations

Flyway location for the recovery module. History table `flyway_schema_history_recovery`.

Rules (D-RCV-28, BS-2.2 to BS-2.6, checked by `RecoveryMigrationLintTest` and the test-scope
tooling in `architecture/migration`):

- File name `V<seq>__<story>_<name>.sql`, a 4-digit contiguous sequence taken at merge.
- Line 1 `-- Story: <story key>`. A corrective file takes the next sequence, keeps the story key and
  adds line 2 `-- Fix: <reason>`; the reason is required.
- Always `${recoverySchema}`, never a literal `recovery.`, `ace.` or `public.`; no `SET search_path`.
- No `R__` files, no `U` files, no `GRANT`/`REVOKE`, never edit a merged file.
- At most one non-fix file per story key.

The lint reports 15 rule IDs, one line per finding:

| Rule ID | Checks |
|---|---|
| `L-NAME` | The file name follows the pattern; every non-`.sql` entry except `README.md` fails |
| `L-UNDO` | No `U*.sql` undo file |
| `L-REPEATABLE` | No `R__*.sql` repeatable file |
| `L-SEQ-GAP` | The sequence starts at the first sequence and is contiguous; the distinct numbers are compared, and a zero-numbered file is refused |
| `L-SEQ-DUP` | Two files with the same sequence; the finding names both |
| `L-HEADER` | Line 1 is `-- Story: <key derived from the file name>` |
| `L-HEADER-MULTI` | A second `-- Story:` line anywhere in the file |
| `L-KEY-DUP` | At most one non-fix file per story key; the finding names both files and the key |
| `L-FIX-LINE2` | A `-- Fix:` line 2 gives a non-empty reason |
| `L-FIX-NO-BASE` | A fix file has exactly one non-fix file of its key below it |
| `L-SEARCH-PATH` | No `search_path`, in any form, including inside `set_config(...)` |
| `L-LITERAL-SCHEMA` | No literal schema qualifier unless `${recoverySchema}`, `information_schema` or `pg_catalog` |
| `L-FK-OUTSIDE` | No `REFERENCES <qualifier>.` outside `${recoverySchema}` (BR8) |
| `L-GRANT` | No `GRANT` or `REVOKE` as the first word of a line or of a statement |
| `L-LEX` | An unterminated string, quoted identifier, block comment or dollar-quoted body |

One finding is one line:

```text
MSG-P3-016 schema=recovery object=<file>:<line> rule=<RULE-ID> <detail>
```

`line` is 1-based, and 0 for the file-level rules. Findings are counted by
(rule, file, line, key): one identity gives exactly one finding, however many clauses or positions
matched. `L-LITERAL-SCHEMA` and `L-FK-OUTSIDE` are keyed by the schema name or qualifier,
`L-LEX` by the opener offset, and `L-SEARCH-PATH` / `L-GRANT` have no key (at most one per line).
A `;` inside a comment, string, quoted identifier or dollar-quoted body never ends a statement, and a
leading comment never supplies a statement's line or kind. A qualifier may be split from its dot by
whitespace or a comment; the reference is still reported, on the qualifier's line.

The tokenizer refuses input above 262144 characters and dollar-quote nesting deeper than 32, with a
clear error instead of scanning it. Both bounds keep a pathological file from stalling the build.

`L-GRANT` is the line-start and statement-start check of SPEC-009. It does not inspect GRANT or
REVOKE inside `EXECUTE`/`DO` dynamic SQL (gap DG-E044-DYN-01): a future rule or a ban on dynamic SQL
in migrations owns that, and until then code review is the control.

`L-LITERAL-SCHEMA` item 1 matches object-name positions lexically. An alias or record qualifier
after `FROM` or `INTO` (for example `EXTRACT(YEAR FROM a.created_at)` or PL/pgSQL
`SELECT ... INTO NEW.id`) is therefore reported. This fails closed; a later rule change may refine
it (ASM-E044-06). `ON` counts only as the first `ON` after `INDEX`, `TRIGGER`, `POLICY`,
`ALTER`/`DROP RULE`, `GRANT` or `REVOKE`, which is the object name, so a join condition such as
`ON a.id = b.id` passes, also inside `CREATE POLICY` or `CREATE RULE`. A quoted identifier before
that `ON` is skipped whole, so `CREATE INDEX "on" ON s.t` is still checked, and a keyword
boundary treats `$` as part of a name, as PostgreSQL does, so in `CREATE INDEX idx$on ON s.t` the
name `idx$on` holds no keyword and `s` is checked. In `CREATE RULE` the
`ON` names an event and is not checked; the table after `TO` is. `COMMENT ON <kind>` is checked
for every kind except `CAST`: in `COMMENT ON CAST (s.t AS u)` the source type `s.t` is not checked
(known limitation; the target type after `AS` is). For `COLUMN` only a three-part name `s.t.c` has
a schema, so `COMMENT ON COLUMN t.c` passes.
A column data type is checked in a `CREATE TABLE` column list and in `ADD [COLUMN]`. It runs on identifiers only: comments and string literals are ignored, and a
dollar-quoted body is scanned as code (D-RUN-13).

`L-LITERAL-SCHEMA` is also the single extension point for the ACE view migration. RWB-E1-069 adds a
narrow exception so `public` is allowed only inside a `CREATE [OR REPLACE] VIEW
${recoverySchema}.v_ace_*` statement (SEAM-E044-01). No exception exists here today, and
`L-FK-OUTSIDE` never consults that method (SEAM-E044-02 covers the Section A grants).

The folder is empty on purpose. Locally the schema comes from Physical Schema v6, loaded by
`infra/postgres/init/10-load-ace-database.sh`. When the baseline and the view migrations ship
together, set `RWB_LOAD_REFERENCE_SCHEMA=false` and Flyway builds the schema from here.

# Implementation assumptions: RWB-E1-044

No question was put to the user (L-RCV-03, RUN-BRIEF rule 4). These are the choices this stage made
where the plan left the detail to the builder.

| ID | Assumption | Basis |
|---|---|---|
| IA-E044-01 | The lint test asserts the complete finding list in **registry order** (the plan's class order: name, undo, repeatable, sequence, header, key, fix, search path, literal schema, foreign key, grant, lex). | `MigrationRules.all()` is one ordered list (SPEC-016); tests describe the list, so the order must be stable. |
| IA-E044-02 | A sequence number is read from any `V<seq>__` prefix, even when the story token is malformed; `L-NAME` and the header/key/fix rules still require the full pattern. | Keeps `t01-name-fail` and `t06-format-fail` at their planned finding lists (the projects' broken name is reported once, not as a gap too). |
| IA-E044-03 | The `previous-tag` case removes the later file from the classpath; the applied higher version is `FUTURE` and Flyway's `*:future` default ignores it. | SPEC-013 / NFR-027; verified green against Flyway 12.4.0 in T-044-13. |
| IA-E044-04 | The drift snapshot excludes Flyway's own history table. | DEV-E044-02: its generated constraint names embed OIDs and differ between identical databases. |
| IA-E044-05 | The `L-LEX` key is the opener offset (SPEC-004); where a fixture has no second finding on that line the test matches the key with a wildcard, so the assertion is about rule, file and line. | SPEC-004 key table; T-044-22. |
| IA-E044-06 | `L-SEQ-DUP` uses the four-digit sequence (`0001`) as its key and names both files in the detail; `L-SEQ-GAP` uses the missing version (`V0002`) as file and key. | `data-model.md` §2 leaves the file-level key to the rule. |
| IA-E044-07 | The container test asserts the history row by `script` (file name) rather than by `version = '1'`, because Flyway stores the raw padded version `0001` for a `V0001` file. | AC1 says "its version, as Flyway records it"; the script column is unambiguous. |

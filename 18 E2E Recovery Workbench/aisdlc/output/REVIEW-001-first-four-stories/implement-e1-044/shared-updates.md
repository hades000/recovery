# Shared updates proposed: RWB-E1-044 confirmation-gate fixes (REVIEW-001)

The orchestrator applies these rows. This stage does not edit `aisdlc/docs/open-items.md`.

## Open item (for `aisdlc/docs/open-items.md`, main table)

The ID is the orchestrator's next free `OPEN-` number.

| ID | Item | Stories affected | Owner | Needed by | Raised in |
|---|---|---|---|---|---|
| OPEN-<next> | The migration lint refuses any file above 262,144 bytes (`MigrationLexer.MAX_CHARACTERS`) and dollar-quote nesting deeper than 32 (`MAX_DOLLAR_DEPTH`). The lint fails closed: an over-cap file fails `RecoveryMigrationLintTest` and the build. Physical Schema v6 is 925,733 bytes, so a single-file baseline migration derived from it would be rejected. RWB-E1-001 must split its baseline into files below the cap (each its own `V<seq>` in merge order; one-script-per-story then needs a recorded exception or a corrective-script approach under D-RCV-28), or raise the cap in its plan with a recorded reason (deviation plus security-review note on SEC-044-05). | RWB-E1-001 (seam); RWB-E1-069 if its view migration is large | RWB-E1-001 planner, with the tech lead | RWB-E1-001 plan gate | RWB-E1-044 code gate confirmation, CONF-E044-06; `INC-001-epic-1-RWB-E1-044/implement/deviations.md` DEV-E044-05 |

## AGENTS.md section 11 entry (the confirmation review's note, for the orchestrator to add)

| Date | Error | Rule added |
|---|---|---|
| 2026-11-19 | RWB-E1-044: every literal-schema position fixture used a known qualifier (`public`, `recovery`), which the broader item-4 check already reported, so removing the position check left every test green. Found by the code gate confirmation review (CONF-E044-01, Medium). | No new rule proposed; section 3 rule 10 applies. The orchestrator decides whether to add one ("a fixture for a narrow check uses input that no broader check reports") |

# Assumptions: INC-001-epic-1-RWB-E1-044 (specify)

No question was put to the user (L-RCV-03; RUN-BRIEF rule 4). Each assumption names its basis. A reviewer can overturn any of them, and the affected SPEC item is listed.

| ID | Assumption | Basis | Affects | Overturn by |
|---|---|---|---|---|
| ASM-E044-01 | `RecoveryFlywayConfig` stays in `platform.internal`; the story §13 package `recovery.casewf.migration` is not created | Audit A-01 gives module mapping to RWB-TE-001; audit A-04 says extend the baseline, do not duplicate | SPEC-001 | RWB-TE-001 module map |
| ASM-E044-02 | On PostgreSQL a failed migration leaves no history row (transactional DDL), so the "failure record" in AC8/X6 is the ERROR log line with MSG-P3-016 and the version. The job-monitor record is deferred | Story v7 AC8, X6; D-RCV-12; Flyway behaviour on PostgreSQL (verified by T-044-14) | SPEC-003, T-044-14 | BA confirmation (open-item candidate in shared-updates) |
| ASM-E044-03 | A wrong `rwb.schema` value is a start-up configuration error with no message ID. Error and Message Standard v4 has no configuration-error message, and MSG-P3-016 describes a schema check during deployment | D-RCV-28; story v7 §13; Error and Message Standard v4 | SPEC-002 | Message owner adds an ID |
| ASM-E044-04 | Lint findings use MSG-P3-016 with `{schema}` = `recovery` and `{object}` = `<file>:<line>`. All findings are listed in one run | Story v7 X3 ("names the file and line"), AC6; Error and Message Standard v4 parameters | SPEC-004 | — |
| ASM-E044-05 | Any non-`.sql` file other than `README.md` in the migration folder is a naming finding | D-RCV-28 (1) naming is fatal; the README exists in the folder today | SPEC-005 | — |
| ASM-E044-06 | The keyword positions in SPEC-007 are the minimum set that implements D-RCV-28 (2) "object-name positions". The plan may extend the set but not narrow it | D-RCV-28 (2) names the categories, not a keyword list | SPEC-007 | Recovery tech lead |
| ASM-E044-07 | INSTRUCTION and METHOD counters are added to `recoveryCoverageVerification`, or per-class evidence for all four counters is attached. Test-scope lint and comparator are covered at rule level | Specification execution gates (80% lines, statements, branches, functions); D-RCV-40; build file today sets LINE and BRANCH only | SPEC-014 | Plan gate |
| ASM-E044-08 | Story and plan convention (audit A-19): `docs/stories/<KEY>/story.md` and `docs/stories/<KEY>/plan.md` in the code repository | AGENTS.md §6 ("held next to the code"), §7; audit A-19 | SPEC-015 | Recovery tech lead |
| ASM-E044-09 | The ACE-only items (D-RCV-45 `db-migrate` guard, H2 skip, Jenkins step) do not apply in this repository and are carried to the ACE port unchanged | `README.md` local-versus-target table; no H2, no `db-migrate` profile, no Jenkins here | §14 | ACE port |
| ASM-E044-10 | Container fixtures use story key `rwb_e1_044` and synthetic table names from the story ACs (`queue`, `timer`, `note_x`, `team_code`) in isolated test databases | Story v7 §7; RUN-BRIEF rule 7 | SPEC-011, SPEC-012 | — |

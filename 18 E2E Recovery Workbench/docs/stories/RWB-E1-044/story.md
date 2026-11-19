# RWB-E1-044 Database migrations versioned with parameterized schema names

| Field | Value |
|---|---|
| Story key | RWB-E1-044 |
| Epic | EPIC-001 |
| Module | P3 Case and workflow |
| Feature | FEAT-CWC-24 Run versioned migrations with parameterized schema names |
| Requirement IDs | REQ-RDF-001, REQ-RDF-014 |
| Story file (v7) | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-044-database-migrations-versioned-with-parameterized-schema-names-v1.md` (document set v14, read only) |
| Specification | `aisdlc/output/INC-001-epic-1-RWB-E1-044/specify/spec.md` (v14-7, spec gate round 7 PASS) |
| Plan | `aisdlc/output/INC-001-epic-1-RWB-E1-044/plan/plan.md` (committed beside this file as `plan.md`) |

As a platform administrator (RW-PLATADM), I want every schema change applied by a versioned Flyway
migration, one migration per story, forward-only in PROD, with the schema name taken from a
parameter, so that the database in every environment is the sum of known migrations and nothing
else.

This story ships **no production migration**: it adds the lint, the schema pin, the failure report,
the local migrator rights and the container proof that the inherited Flyway bean behaves correctly.

## Acceptance criteria (restated in the specification)

| AC | Restatement |
|---|---|
| AC1 | Fixture `V<seq>__rwb_e1_044_add_queue.sql` applies once. Its version, as Flyway records it, and its checksum are in `flyway_schema_history_recovery`. A second migrate applies nothing |
| AC2 | A drift between the migration result and a target fails with `MSG-P3-016` naming `<schema>.<table>.<column>`; here, a container-to-container comparison (`recovery.queue.note_x`) |
| AC3 | The same fixture creates `recovery.timer` in two clean databases; the recorded checksums are equal |
| AC4 | `V<seq>` applied, then the file changed: migrate fails validation, the ERROR `MSG-P3-016` line names that version, and the context does not start |
| AC5 | Fixture line 2 `CREATE INDEX ix_a ON recovery.queue (team_code)` gives `MSG-P3-016 … object=<file>:2 rule=L-LITERAL-SCHEMA` |
| AC6 | Two non-fix files with key `rwb_e1_028` give one `L-KEY-DUP` finding naming both files and `RWB-E1-028` |
| AC7 | `clean()` is refused with Flyway's message; a `U<seq>__…sql` file gives `L-UNDO` |
| AC8 | A fixture whose second statement references a missing table: the first statement's object is absent, there is no history row for that version, the ERROR `MSG-P3-016` line names the version, and the context does not start |
| AC9 | Two contexts migrate concurrently with one pending fixture: one history row for the version, and both start |

## Out of scope

The job-monitor parts (`MigrationRunRecorder`, `GET /api/recovery/v1/admin/jobs?type=MIGRATION`,
SCR-44, `MSG-P4-002`, TC-E1-044-10) are deferred by D-RCV-12 with no named owner. Real-environment
drift, a read-only account and `rwb.p3.migration-drift-gate` are parked by D-RCV-05. The ACE DBA role
for the migration account is declined; the account gets only the two D-RUN-14 rights. The `public`
exception for the RWB-E1-069 view migrations is a named seam, not built here.

# Document gaps: INC-010-epic-1-RWB-E1-069 (Implementation Planner, plan v1, 18 Nov 2026)

This stage adds `DG-P01..DG-P03`. Every spec gap `DG-L01..DG-L30` is carried unchanged and remains Blocker = No; the ones that bear on the plan are listed at the end. Precedence is the RUN-BRIEF order: D-RCV-35/36, then ADR v3, then Decision Log v10, then story files v7, then older maps and drafts.

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why (blocker or not) | How this stage proceeded |
|---|---|---|---|---|---|---|
| DG-P01 | RWB-E1-001 spec Revision 4, SPEC-RWB-E1-001-010 hand-off and ASM-E1001-18: E1-069 "keeps [the version-`0` baseline assertion] in the S2 stage" and "no assertion removed" | E1-069 spec revision 4, DG-L30 and SPEC-017: with S2 `false` the schema is empty at init, no baseline row exists, and E1-069 retires that assertion and replaces it with the per-file history assertion | E1-069 spec SPEC-017 and DG-L30; RWB-E1-001 spec Revision 4 line 367 and its §hand-off; `RecoveryFlywayConfig` (`baselineOnMigrate(true)`, `baselineVersion("0")`) and Flyway's rule that a baseline row is written only to a non-empty schema | No | Both specs passed their gates; the later E1-069 spec settles the consequence of S2 `false` and the replacement is stronger (one success row per applied file, no version-`0` row), so no coverage is lost. The wording difference is carried to the owners in OI-069-L. | SPEC-017 per-file history assertion; TASK-14; DG-L30; OI-069-L |
| DG-P02 | RWB-E1-001 spec Revision 4 line 367 and §hand-off name `RecoverySchemaMigrationIT`; E1-069 spec SPEC-015(c) and ASM-014 require E1-069 to pin it to the RWB-E1-001 version | The E1-001 plan folder `aisdlc/output/INC-009-epic-1-RWB-E1-001/plan/` does not exist at plan time, so the class's merged path and exact Flyway construction are not yet fixed | `aisdlc/docs/increments/INDEX.md` row 009 (specified, not planned); E1-069 spec line 367 naming the same test; `../specify/spec.md` SPEC-015(c) | No | The dependency is build order (E1-001 order 9 before E1-069 order 10, [S14]), not a missing decision; the plan names the class, marks the file `[E1-001]` and states the mechanism (ASM-014). A different mechanism is absorbed by the same assertions. | `tasks.md` TASK-00 records the merged path and stops if the class is absent; TASK-07 edits only the Flyway construction |
| DG-P03 | E1-069 spec SPEC-008: `backend/src/test/java/th/co/scb/ace/demo/recovery/ViewConformanceTest.java` "(package per [T1] module layout if it moves; the plan names it)" | The spec defers the class's package to this stage | RWB-TE-001 v4 SPEC-002: the module map covers main packages only; no test package is mapped. The file path itself fixes `th.co.scb.ace.demo.recovery` | No | No conflict and no decision: the path in the spec names the package, and the same package already holds `RecoveryDatabaseIT` | The plan names `th.co.scb.ace.demo.recovery` and TASK-08 writes the class there |

## Carried spec gaps that bear on this plan (all Blocker = No)

| Gap | Subject | How the plan applies it |
|---|---|---|
| DG-L01 | Which file creates the four extension tables | The RWB-E1-001 migration; E1-069 verifies them (TASK-09 test, TASK-19 check) |
| DG-L02 | Which file creates the three helpers | The Section A file, `CREATE OR REPLACE`; `ace_to_date` to the SPEC-002 behaviour (TASK-09) |
| DG-L03 | Two files, `public.` qualifiers and grants break D-RCV-28 | The two seams of SPEC-014 (TASK-03, TASK-04) |
| DG-L05 | Dictionary totals 122 / 1,366 / 1,062 against 123 / 1,379 / 1,075 against the seed 123 / 1,382 / 1,078 | Assert the seed (TASK-09; PA-E1-069-11) |
| DG-L11 | Commented `GRANT SELECT ON ALL TABLES` in the sources | One grant per view; the only `ON ALL TABLES` is the PUBLIC REVOKE (TASK-09, TASK-15) |
| DG-L12 | BR2 against the PostgreSQL ownership rule | Transient `USAGE, CREATE`, SELECT grant before the owner change, final revoke (TASK-09, TASK-11) |
| DG-L13 | `permission denied for schema public` needs the PUBLIC revoke | ACE DBA precondition P4(d); local via `20-grants.sql.inc` (TASK-15, EX-02) |
| DG-L16 | RWB-ACE-001 is an external dependency | Probe stand-in locally; Section B merge gated (TASK-11, TASK-19, EX-03) |
| DG-L18 | Who delivers the view files | E1-069; README corrected (TASK-17) |
| DG-L20 | Skipping the Section B stage under `outOfOrder(false)` | Section B merges only after RWB-ACE-001; A then B contiguous (TASK-11, PA-E1-069-16) |
| DG-L22 | ACE-side grants are not in a recovery migration | P4(d) precondition; local stand-in (TASK-15, S-06, EX-02) |
| DG-L23 | The `ace_to_date` body raises on impossible dates | SPEC-002 behaviour, not the source body; SPEC-020 tests (TASK-08, TASK-09) |
| DG-L24 | `is_personal` 9 against 250 | Assert what the seed holds: 250 true, 54 false among the 304 (TASK-08); 526 is E1-001's (PA-E1-069-12) |
| DG-L25 | DML for `recovery_svc` on Workbench tables in SIT and above | Out of scope; OI-069-I (TASK-19) |
| DG-L27 | The local switch hand-over is a sibling spec's | S1 and S3 stay E1-001's; E1-069 takes S2 (TASK-15) |
| DG-L29 | The migration account's rights: two specs disagreed | D-RUN-14 applied as recorded; E1-044 v14-7 delivers it; E1-069 asserts and weakens nothing (TASK-04, TASK-08, TASK-19) |
| DG-L30 | The E1-001 hand-over on the baseline row and the seed counts | SPEC-017 per-file history; DG-P01; OI-069-L (TASK-14) |

No Blocker = Yes gap exists in this run. RWB-ACE-001 remains the Tier 2 probe stand-in and the external dependency, Blocker = No (DG-L16). D-RUN-14 remains the orchestrator's decision with OI-069-M / OPEN-051 open and no human approval claimed.

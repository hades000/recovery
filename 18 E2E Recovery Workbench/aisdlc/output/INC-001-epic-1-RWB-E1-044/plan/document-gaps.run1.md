# Document gaps: INC-001-epic-1-RWB-E1-044 (plan)

Paths are under `<docset>/17 AI-First SDLC Repository v2/requirement/legacy/` unless they start with `aisdlc/` or a repository path. Precedence (RUN-BRIEF): D-RCV-35/36 > ADR v3 > Decision Log v10 > story files v7 > older maps and drafts.

**No blockers.** The 13 gaps recorded by the specifier stand unchanged (`../specify/document-gaps.md`, DG-L01 to DG-L13; all Blocker = No) and are carried, not re-litigated. This stage adds three plan-stage gaps (PG-E044-01 to -03), all Blocker = No.

## Carried gaps (from specify, unchanged)

| ID | Subject | Blocker? |
|---|---|---|
| DG-L01 | Story v7 uses `RWB_SCHEMA` `rwb_case`, `${schema}`, `spring.flyway.*`, `V12..V18`; Decision Log v10 D-RCV-28 says `recovery`, `${recoverySchema}`, `V<seq>__<story>_<name>.sql` | No |
| DG-L02 | Story v7 wants a real-environment drift check with a read-only account and `rwb.p3.migration-drift-gate`; D-RCV-05 parks it | No |
| DG-L03 | Story v7 says the history records a failed migration; PostgreSQL transactional DDL leaves no failed row | No |
| DG-L04 | Sources fix conflicting migration numbers; D-RCV-28 and D-RUN-07 settle it for this repository | No |
| DG-L05 | RWB-E1-069's Section A grants and two non-fix files per key conflict with L-GRANT, L-LITERAL-SCHEMA and L-KEY-DUP | No |
| DG-L06 | Story v7 package and migration folder differ from the repository; the package is settled by D-RUN-17, the folder is inherited | No |
| DG-L07 | Root README and migration-folder README say "RWB-E1-001 ships V0001 to V0003" | No |
| DG-L08 | The 10 Nov 2026 spec traced FR-RWB-020; the matrix maps FR-RWB-013 | No |
| DG-L09 | ADR-010, D-RCV-35 and Env v4 need `FROM public.<table>` inside a recovery view; the D-RCV-28 lint rejects it | No |
| DG-L10 | D-RCV-12 defers the job-monitor parts and names no receiving story | No |
| DG-L11 | Refused clean shows Flyway's own message, not MSG-P3-016 | No |
| DG-L12 | Squad register D-RCV-48 names schema `ace`; Decision Log v10 and L-RCV-07 settle `recovery` | No |
| DG-L13 | RWB-E1-069 v7 §3 attributes an ACE DBA role to the E1-044 migration account; declined, D-RUN-14 gives two narrower rights | No |

## New gaps recorded by this stage

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why (blocker or not) | How this stage proceeded |
|---|---|---|---|---|---|---|
| PG-E044-01 | `aisdlc/RUN-BRIEF.md` rule 2 ("Write only to your own stage folder") | The plan cannot be written directly to `docs/stories/RWB-E1-044/plan.md` by this stage, although the location is named as the plan's own | Story spec v14-7 SPEC-015 ("`docs/stories/RWB-E1-044/plan.md` is written by the Implementation Planner"); `AGENTS.md` §6 ("One story file per story, held next to the code it produces") and §7 ("The agent writes `plan.md` for each story before any code") | No | Both are satisfied: the planning artefact is this stage's `plan/plan.md`, and TASK-16 has the builder commit it at the code path with the code. No rule depends on the stage folder being the only copy at merge | TASK-16 copies `plan.md` into `docs/stories/RWB-E1-044/`; PA-E044-05 records the reading. The builder does not rewrite the content |
| PG-E044-02 | `aisdlc/.github/rules/versioning-standards.md`, "Database Changes" ("Use migrations"; "Include rollback guidance when possible") | A rollback script is suggested, while D-RCV-28, BS-2.2 and BS-2.4 allow forward-only migrations only: one file per story, never edited, a corrective file with `-- Fix:`, no undo file | `AGENTS.md` §2 ("versioned migrations, one migration per story, forward-only"), §3.7; `aisdlc/.github/contexts/backend-standards.md` BS-2.2 to BS-2.4; RUN-BRIEF (the toolkit templates are generic; where they conflict with the contexts, the contexts win) | No | The contexts and AGENTS.md are the project standard and outrank the generic template rule; the story adds no migration at all, so the point is not exercised | Rollback is the previous tag (NFR-027, T-044-13), recorded in `plan.md` "Release and rollback". No undo file and no `clean` is planned |
| PG-E044-03 | RWB-TE-001 plan v7, `plan.md` "Coverage tests" row `casewf/migration/RecoveryFlywayConfigTest.java` and `tasks.md` TASK-10 and TASK-12 | The TE-001 plan says the `RecoveryFlywayConfig` binding test reads `application.yaml` through an `ApplicationContextRunner`, but it does not state whether that context supplies a `DataSource` or creates the `Flyway` bean. E1-044 adds a second bean (`recoveryMigrationRunner`) to the same configuration class, so the answer decides whether that merged test needs anything beyond the allowed change (2) | RWB-TE-001 plan v7 line 211 (method list) and line 218 (runner design) name the runner and the environment but not the beans the binding method creates; spec v14-7 SPEC-002 "Existing tests" allows at most two named changes | No | The TE-001 plan is gated and merged before this story; TASK-00 reads the merged test and reports a mismatch instead of rebuilding TE-001 (ASM-E044-19). The spec already bounds the allowed change | TASK-00 records the exact setup and the list of TE-001 tests that bind the record or build the bean; TASK-08 applies only the allowed `MigrationPropertiesConfig` addition and changes no assertion. If anything else is needed, the build stops and reports to the orchestrator |

## Checked and not recorded as gaps

- `aisdlc/.github/rules/architectural-standards.md` (Flutter, `/api/v1`, `AUTH-XXX`) conflicts with the recovery contexts, but RUN-BRIEF already records that the contexts win and says not to report it again. No API is in scope here, so it does not bite.
- `backend/src/main/resources/db/modulemigration/recovery/README.md` is corrected by SPEC-015 and TASK-16 (DG-L07); the root `README.md` is left to the orchestrator (recorded in `shared-updates.md`).
- The story/plan convention files do not exist yet (`docs/` is absent); audit A-19 says the first story sets the convention and this story does. Not a gap.
- No document is silent on the message ID: `MSG-P3-016` exists in Error and Message Standard v4 with the `schema` and `object` parameters this plan uses.

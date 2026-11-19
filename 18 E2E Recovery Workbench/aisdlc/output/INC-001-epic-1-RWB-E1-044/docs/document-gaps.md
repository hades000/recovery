# Document gaps: RWB-E1-044 documentation stage

No **new** document-set gap was found while writing the documentation. The specifier recorded
DG-L01..DG-L13 (all Blocker = No, eight contradictions settled, five gaps); the planner recorded
PG-E044-01..-03 (stage-local, closed by TASK-00 and TASK-16); the implementation recorded one gap,
`DG-E044-DYN-01`, reproduced here because it is the one limitation a reader of the delivered lint
must know.

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why (blocker or not) | How this stage proceeded |
|---|---|---|---|---|---|---|
| DG-E044-DYN-01 | Specification `INC-001-epic-1-RWB-E1-044/specify/spec.md` v14-7, SPEC-RWB-E1-044-009 and T-044-20 | `L-GRANT` refuses GRANT/REVOKE only as the first word of a line or of a statement. It does not inspect inside `EXECUTE`/`DO` dynamic SQL, so `EXECUTE 'GRANT …'`, `EXECUTE $q$GRANT …$q$`, `format('GRANT …')` and a concatenation are not refused by the lint. | `../review/security-review.md` §3 SEC-044-03 (Low), reproduced against the compiled test classes; the gated spec text is the conflicting source | **No** | SPEC-009 defines the rule exactly and the gate passed on that wording. The rule is a build-time, test-scope control; D-RUN-14 leaves the migrator with no table privilege in `public`; code review remains the control. Adding dynamic-SQL analysis to `L-GRANT` exceeded the gated spec and was reverted after four review rounds. | Documented in `COMPLIANCE.md` §5.3 and in the migration-folder README. The rule is restored to SPEC-009 exactly; the gap is recorded, not silently accepted. Suggested owner: recovery tech lead / specification owner. Suggested next step: `L-DYNAMIC-SQL`, or a documented ban on dynamic SQL in migrations, each with its own gated spec change. |

## Post-gate drifts (not document gaps)

| Item | Difference | Disposition |
|---|---|---|
| Lint fixture count | `../implement/code-map.md` CODE-E044-028 records "50 folders"; the delivered tree holds **55** because review rounds added cases, and `RecoveryMigrationLintTest` asserts all 55 | Delivery evidence, not a conflict inside the document set. Recorded in `COMPLIANCE.md` §6; no gated file was edited |
| Unit-test report | `../implement/unit-tests/report.md` was stale in the pre-fix code-gate pass (239 tests); it now records the final 243-test run | Code-gate CODE-002, closed at `89477bc` |
| Ponytail review | The artifact had no closure in the pre-fix pass; it now ends with the closure and **Verdict: Ship** | Code-gate CODE-003, closed at `89477bc` |
| Container count | `../implement/deviations.md` said 17 container tests; the suite is 18 (12 `RecoveryMigrationIT` + 6 `RecoveryDatabaseIT`) | Code-gate CODE-003, closed at `89477bc` |

These are differences between an early evidence artifact and the delivered code, not gaps in the
document set. The documentation follows the delivered code.

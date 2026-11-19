# Assumptions — Technical Documenter, RWB-E1-042

RUN_ID `INC-003-epic-1-RWB-E1-042`. Recorded instead of asking the user (AGENTS.md §10.6). No approval
recorded (D-RUN-09).

| ID | Assumption | Basis | Effect if wrong |
|---|---|---|---|
| A-DOC-E042-01 | The figures of record are those at tip `25c8f94` in `implement/code-gate-fix/test-and-coverage-counts.txt` (388 unit, 59 container, 13 API; LINE 91.0, INSTRUCTION 90.7, BRANCH 80.9, METHOD 95.8). No Gradle task was run by this stage | Brief; round 3 code gate recomputed the same from native XML | Re-quote the figures from the new counts file |
| A-DOC-E042-02 | The docs name the migration `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql`, although the branch file is `V0001__…`; the orchestrator assigns `<seq>` at merge | D-RUN-07, D-RCV-28, SPEC-001; round 3 gate row 7 | Replace `<seq>` with the merged number in a later docs pass |
| A-DOC-E042-03 | OPERATIONS.md is omitted: the story adds no job, schedule, queue, alert or runbook step; its operating notes (flag, readiness indicator, cache TTL, 503 behaviour) fit README §6 | RWB-E1-044 docs shape; brief | Add OPERATIONS.md if the release owner wants a runbook entry for the readiness indicator |
| A-DOC-E042-04 | D-RUN-18..D-RUN-21 are documented as the orchestrator's build decisions in force for this run, marked unratified (OPEN-050), not as approved architecture | Build log; open-items OPEN-050 | ARCHITECTURE §3 and §4 change if a decision is replaced |
| A-DOC-E042-05 | The code gate round 4 PASS (0/0/0/0, CODE3-001 closed by DEV-20) is documented as a review result, not an approval; human sign-off remains unrecorded (OPEN-016) | `review/code-gate-review-4.md`; D-RUN-09 | — |
| A-DOC-E042-06 | Where `implement/traceability.md` (CODE-08 "11 constants") and the generated code (19 `ParameterKeys` constants) differ, the docs follow the code at `25c8f94` | Worktree read; catalog CSV has 19 rows | — |
| A-DOC-E042-07 | Document-gap candidates are listed without DG-nnn numbers; the Traceability Manager or orchestrator numbers them in `aisdlc/DOCUMENT-GAPS.md` | Brief | — |
| A-DOC-E042-08 | Every carried open item and gap is Blocker No; the spec marks none as a blocker | `specify/spec.md`; `implement/document-gaps.md` | Raise to the orchestrator if a source marks one Yes |

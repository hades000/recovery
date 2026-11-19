# Proposed shared-file updates — Technical Documenter, RWB-E1-042

RUN_ID `INC-003-epic-1-RWB-E1-042`. This stage edits no shared file. The rows below are for the
Traceability Manager or the orchestrator to apply. No approval recorded (D-RUN-09).

| ID | Target file | Proposed change |
|---|---|---|
| SU-DOC-E042-01 | `aisdlc/requirement/Traceability_Matrix.md` | Add DOC rows `DOC-RWB-E1-042-001`..`-022` against `FR-RWB-010` / RWB-E1-042, each pointing at `output/INC-003-epic-1-RWB-E1-042/docs/<file>` §n, with the SPEC / TASK / CODE / TC mapping in the README DOC ID index (§9) |
| SU-DOC-E042-02 | `aisdlc/requirement/Traceability_Matrix.md` | Record the TC → test mapping of DEV-20 for TC-04, -10(b), -17, -28, -32 and -44 (planned names in `plan/tests/scenarios.md` do not exist; CODE3-001, closed in code gate round 4) |
| SU-DOC-E042-03 | `aisdlc/requirement/Traceability_Matrix.md` | Keep TC-E1-042-12 as **Blocked** (OI-E1-042-001), not passed |
| SU-DOC-E042-04 | `aisdlc/docs/open-items.md` | No new open item from this stage. Note against OI-E1-042-011 that the identical-repeat response is still absent from API Specification v4, and against OPEN-050 that ARCHITECTURE §3 (D-RUN-19) and §4 (D-RUN-20) document those decisions as unratified |
| SU-DOC-E042-05 | `aisdlc/output/INDEX.md` (or the run index) | Add the six docs files for RWB-E1-042 with status "DOCUMENTED, code gate round 4 PASS 0/0/0/0, no approval; sign-off not recorded (OPEN-016)" |
| SU-DOC-E042-06 | `aisdlc/DOCUMENT-GAPS.md` | Add the candidates in `docs/document-gaps.md` §1 (unnumbered; Blocker No) |
| SU-DOC-E042-07 | `aisdlc/output/INC-003-epic-1-RWB-E1-042/implement/traceability.md` (owner: builder) | Correct CODE-08 "11 constants" to 19 constants (11 is the `casewf.config.api` published-type count) |
| SU-DOC-E042-08 | `aisdlc/output/INC-003-epic-1-RWB-E1-042/api-tests/report.md` header (owner: API Tester / orchestrator) | Header says tip `9056ed2` and cites run4; run table says run5 at `25c8f94` is current. Align the header |
| SU-DOC-E042-09 | `aisdlc/output/INC-003-epic-1-RWB-E1-042/implement/shared-updates.md` §5 (owner: builder) | Replace the garbled advisory-lock text with `pg_advisory_xact_lock(hashtext(validFrom || '|' || contentHash))` as in the code; fix the §2 path `implementation-builder/implement/traceability.md` to `implement/traceability.md` |

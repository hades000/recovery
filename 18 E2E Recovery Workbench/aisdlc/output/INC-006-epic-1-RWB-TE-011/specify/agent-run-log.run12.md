# Technical Specifier run log — INC-006 RWB-TE-011

| Field | Value |
|---|---|
| RUN_ID | `INC-006-epic-1-RWB-TE-011` |
| Story | `RWB-TE-011` PDPA lint for code, tests and logs |
| Agent | `.claude/agents/technical-specifier.md` (Technical Specifier), human-started stage |
| Start / end | First run 2026-11-17; remediation runs 2026-11-18 (after rounds 4 to 10; sections below) |
| Status (current) | Spec remediated after round 11 (run 11, directed by the orchestrator with the churn direction "fix the three findings, simplify"). Spec gate round 11 (`review/spec-gate-review-11.md`): FAIL, 0 Critical, 0 High, 0 Medium, 3 Low (SG11-01..03), now fixed. Round 12 is for the orchestrator to run; this stage did not run it. The first run's `SUCCESS_WITH_WARNING` and `REVIEW_GATE_WARNING` (Low findings only) were not accepted under D-RUN-09; the Lows were fixed and re-reviewed. |
| Interaction policy | No questions (L-RCV-03). Current set: 29 assumptions (ASM-TE011-01..29) and 15 clarification rows (CLAR-001..015), all `RESOLVED` by precedence, orchestrator triage or a labelled assumption. The first run recorded 19 and 8. |
| MCP | None connected (RUN-BRIEF rule 5). The story was read from the document set. |
| Baseline | No `_v2-baseline` exists for this run. |

## Steps

| Step | Result |
|---|---|
| Sequence check | Build order 6. RWB-TE-001 is implemented. RWB-TE-002 (order 4) is specified, not built. |
| Change classification | `NEW_STORY`. UI NO, Logic YES, API NO (`NO_API_CHANGE`). Build tooling only; no application code. |
| Orchestrator notes | The PDPA job of A-09 is in scope (SPEC-TE011-013). A-07 is out of scope (static check, no runtime path), and an owner change is proposed. **Superseded by D-RUN-15 (run 6):** A-07 belongs to RWB-TE-003, `X-Correlation-Id` is not built, and the owner-change proposal is withdrawn. |
| Classification | `sys_fields.is_personal` (Physical Schema v6, 18 fields) plus `x-personal-data` (API Specification v4, 5 properties). Cross-checked against LDM v8, Inventory v4 and PDPA Design v2. The conflict is DGL-01. |
| Requirement coverage | 30 rows, 0 blocked. |
| Document gaps | DGL-01..12, no blocker. |
| Spec gate round 1 | `review/spec-gate-review.md`: FAIL, 2 Medium, 5 Low. All fixed. |
| Spec gate round 2 | `review/spec-gate-review-2.md`: FAIL, 1 Medium, 1 Low. Round-1 findings resolved. Both fixed. |
| Spec gate round 3 | `review/spec-gate-review-3.md`: FAIL, 0 Critical/High/Medium, 2 Low. `REVIEW_GATE_WARNING`. Both Lows were fixed in the text afterwards; the fixes were not re-reviewed. |

## Outputs (`output/INC-006-epic-1-RWB-TE-011/specify/`)

`spec.md`, `compliance-validation.md`, `assumptions.md`, `document-gaps.md`, `shared-updates.md`,
`gate-response.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`,
`figma/figma_report.md`, `agent-run-log.md`. The reviews are in `review/`.

## Evidence commands (read only)

- `cmp` of the Physical Schema v6 copy and `diff` of the API Specification v4 copy: both identical to the document set.
- A count of `sys_fields` INSERTs with `is_personal = true`: 18.
- Greps of `backend/src`, `frontend/src`, `frontend/e2e` and `infra/` for 13-digit numbers, Thai mobile numbers, e-mail domains and personal field names found only `local.test` e-mails.
- Inventory v4: 17 Restricted fields, 9 of them not marked in the seed. 14 of the 18 seed fields are marked "Yes".

First-run note (superseded): `REVIEW_GATE_WARNING` was raised after round 3 for Low-only findings; under D-RUN-09 it was not accepted, and the run continued through rounds 4 and 5.

## Remediation run after spec gate round 4 (2026-11-18)

| Field | Value |
|---|---|
| Trigger | `review/spec-gate-review-4.md`: FAIL, 0 Critical, 0 High, 3 Medium (SG4-01..03), 1 Low (SG4-04); `review/document-gaps-4.md` DG4-01, DG4-02 |
| Direction | Orchestrator triage (Claude Code as orchestrator; `AI-SDLC-BUILD-LOG.md` 2026-11-18T00:04:03; D-RUN-07, -08, -13). No human disposition is claimed. |
| Inputs read | RUN-BRIEF; `.claude/agents/technical-specifier.md`; the spec set; review rounds 1-4; RWB-E1-001 spec under revision and `evidence/is_personal_union_v4.tsv`; RWB-E1-043 spec SPEC-RWB-E1-043-031 and GAP-38; Physical Schema v6 copy; API Specification v4 copy |
| Backups | `spec.run4.md`, `assumptions.run4.md`, `document-gaps.run4.md`, `shared-updates.run4.md`, `compliance-validation.run4.md`, `gate-response.run4.md`, `contracts/backend-apis.run4.json` |
| Evidence | `evidence/te011_round4_check.py` (`python -I`, read only, prints no values) and `-output.txt`. The PS v6 copy holds 2,584 INSERTs. Its pattern scan finds 0/0/0/0. Its `sys_fields` statements are 1,379 INSERTs plus DDL, comments and 1 view. The union has 390 personal names, 71 of them ambiguous; none of the 18 PS v6 names is ambiguous, and none of the 9 Restricted names. The six seed tables hold 1 personal pair, `data_product.owner_user_id`. Today's 4 log calls use no union name. |
| Changes | SPEC-TE011-001 (reader: R1/R2, ignored class, fail closed, order rules, keys, dictionary at a point); -002 (keys, unambiguous names); -003 (INSERT count, scan); -004 (name-based log rules stated); -008 ((object, field) matching, resolution, notices, point-in-time); -011 (no allow entry on a migration); -012 (notices); -015 (configuration); -016 (baseline restated for 3 states); new -017 (RWB-E1-001 obligations, RWB-E1-043 seam). TS-TE011-01..03 and unit scenarios. 31 coverage rows. CLAR-009, CLAR-010. ASM-TE011-20..23. DGL-13, DGL-14. |
| Document gaps | DGL-01..14, Blocker = No for all |
| Spec gate | Round 5 requested from Compliance Reviewer -> `review/spec-gate-review-5.md` |

| Spec gate result (round 5) | `review/spec-gate-review-5.md`: FAIL, 0 Critical, 0 High, 1 Medium (SG5-01), 3 Low (SG5-02..04). SG4-01..04 resolved; DG4-01/02 accepted as DGL-13/14. New gap DG5-01 (Blocker = No) in `review/document-gaps-5.md`. Medium blocks the plan stage. |
| Next step | Technical Specifier round-5 remediation (SG5-01..04, DG5-01), then spec gate round 6. Orchestrator to settle the RWB-E1-043 GAP-38 row that hands the lint load route back to this story (SG5-02). |

## Remediation run after spec gate round 5 (2026-11-18)

| Field | Value |
|---|---|
| Trigger | `review/spec-gate-review-5.md`: FAIL, 0 Critical, 0 High, 1 Medium (SG5-01), 3 Low (SG5-02..04); `review/document-gaps-5.md` DG5-01 |
| Direction | Orchestrator triage (Claude Code as orchestrator; `AI-SDLC-BUILD-LOG.md` 2026-11-18T00:35:10). SG5-02 settled by the orchestrator: the dictionary-load seam belongs to RWB-E1-064, with an open item owned by RW-COMPLY. No human disposition is claimed. |
| Inputs read | Review round 5 and DG5-01; the spec set; RWB-E1-064 story file v1 (Story Files v7); Build Sequence v6 (`aisdlc/docs/increments/build-sequence.md`, order 13); RWB-E1-043 `document-gaps.md` GAP-38; API Specification v4 copy; ACE schema copy; Physical Schema v6 copy |
| Backups | `spec.run5.md`, `assumptions.run5.md`, `document-gaps.run5.md`, `shared-updates.run5.md`, `compliance-validation.run5.md`, `gate-response.run5.md`, `agent-run-log.run5.md`, `contracts/backend-apis.run5.json` |
| Evidence | `evidence/te011_round5_check.py` (`python -I`, read only, prints names and counts only) and `-output.txt`. Every column of the PS v6 seed INSERTs is described on its table. Today, 4 API properties with a PS v6 personal name sit on schemas outside the dictionary (`InteractionRequest.summary`, `TimelineItem.summary`, `AgentOutput.summary`, `FieldCaptureItem.fileName`). Under the union, 20 more API properties lack a dictionary row for their pair, and the ACE copy has 12 pairs outside the dictionary that carry an unambiguous name, plus 5 with an ambiguous name. The scan roots hold no `.sql` file and no `COPY`. The PS v6 copy has 0 column-less INSERTs, 0 `COPY` and 0 foreign keys to `sys_fields`; its INSERTs split as 1,379 / 598 / 421 / 123 / 54 / 8 / 1 by table. |
| Changes | SPEC-TE011-008: described pairs; unresolved positions use the name rule; API personal names in API-typed positions; SQL with no named column is a finding. SPEC-TE011-001: foreign key to `sys_fields` is ignored. SPEC-TE011-002: API personal names. SPEC-TE011-003: full INSERT breakdown. SPEC-TE011-016: state evidence. SPEC-TE011-017: RWB-E1-064 seam row and RWB-E1-043 pipeline row. T6, T8, new T9. TS-TE011-04, -05 and unit scenarios. CLAR-010 updated, CLAR-011 added. ASM-TE011-12, -20, -23 revised; ASM-TE011-24, -25 added. DGL-13 revised; DGL-15 added. Shared updates: OPEN-NEW-TE011-7 (RW-COMPLY, RWB-E1-064 seam), OPEN-NEW-TE011-8 (API marks), notes to RWB-E1-043, RWB-E1-064 and the orchestrator. |
| Document gaps | DGL-01..15, Blocker = No for all |
| Spec gate | Round 6 requested from the Compliance Reviewer → `review/spec-gate-review-6.md` |
| Spec gate result (round 6) | `review/spec-gate-review-6.md`: FAIL, 0 Critical, 0 High, 0 Medium, 4 Low (SG6-01..04). SG5-01..04 resolved; DG5-01 accepted as DGL-15. No new document gap. Low-only failure is not accepted under D-RUN-09. |
| Next step | Orchestrator triage of SG6-01..04, then Technical Specifier run 6 and spec gate round 7. Merge OPEN-NEW-TE011-7 with RWB-E1-043 open item R4 under RW-COMPLY (SG6-04). |

## Remediation run after spec gate round 6 (2026-11-18)

| Field | Value |
|---|---|
| Trigger | `review/spec-gate-review-6.md`: FAIL, 0 Critical, 0 High, 0 Medium, 4 Low (SG6-01..04) |
| Direction | Orchestrator triage (Claude Code as orchestrator; event 2026-11-18T01:02), with D-RUN-09 and D-RUN-15. Corrective migration as the only remedy for a merged migration; unrecognised SQL and DML in `DO` blocks fail closed; the migration folder cannot be excluded; OPEN-NEW-TE011-7 merged into RWB-E1-043 R4. No human disposition is claimed. The run stopped once on a usage limit and resumed on the orchestrator's instruction. |
| Inputs read | Review round 6; the spec set; `AGENTS.md` §3.7, §4.6; decision register D-RCV-28; the specifications of orders 1–5 (RWB-E1-044, RWB-E1-042, RWB-TE-002, RWB-TE-003; RWB-TE-001 per D-RUN-17); RWB-E1-043 revision 3 (GAP-38, R4, §3.2) |
| Backups | `spec.run6.md`, `assumptions.run6.md`, `document-gaps.run6.md`, `shared-updates.run6.md`, `compliance-validation.run6.md`, `gate-response.run6.md`, `agent-run-log.run6.md`, `contracts/backend-apis.run6.json` |
| Changes | SPEC-TE011-003: the migration folder cannot be excluded (exit 2), and the exclusions in force are printed. SPEC-TE011-008: SQL statement classes, with unrecognised forms and DML in `DO` blocks as findings; "Known files" now covers orders 1–5. New SPEC-TE011-018: corrective migration. SPEC-TE011-011, -012, -013, -015, -016 (states (1) and (2)) and -017 (row for orders 1–5; RWB-E1-043 rev 3; RWB-E1-064 per §3.2) are updated. T10–T12. TS-TE011-01 has its dictionary scope and a negative variant. New tests TS-TE011-06 and -07, plus unit rows. The coverage table has 32 rows. CLAR-012 and -013. ASM-TE011-22 and -25 are revised; ASM-TE011-26 and -27 are new. DGL-13 cites R4. Shared updates: OPEN-NEW-TE011-2, -3 and -7 and §3a are withdrawn; §3b is a note for the planners of orders 1–5. |
| Document gaps | DGL-01..15, Blocker = No for all; no new gap |
| Spec gate | Round 7 requested from the Compliance Reviewer → `review/spec-gate-review-7.md` |
| Spec gate result (round 7) | `review/spec-gate-review-7.md`: FAIL, 0 Critical, 0 High, 1 Medium, 3 Low (SG7-01..04). SG6-01..04 resolved; rounds 1–5 still resolved. No new document gap. SG7-01 (Medium): RWB-E1-044's lint fixtures, merged at order 1 under `backend/src/test/resources/`, are designed to be malformed (unterminated files, `ALTER ROLE`/`DATABASE`/`FUNCTION`, `search_path` forms), so this lint would give exit 2 or findings at its own merge; "Known files", state (1) and §3b claim otherwise. SG7-02..04 (Low): RWB-E1-042 step-3 constraint guards are `DO` blocks and DDL in `DO` bodies is ambiguous; four points of SPEC-TE011-018 and -003 undefined; stale or over-claimed text, including the R4 owner wording after RWB-E1-043 revision 4. |
| Next step | Held for the orchestrator's triage of SG7-01..04, as the orchestrator directed; no round-7 remediation started. Then Technical Specifier run 7 and spec gate round 8. |

## Remediation run after spec gate round 7 (2026-11-18)

| Field | Value |
|---|---|
| Trigger | `review/spec-gate-review-7.md`: FAIL, 0 Critical, 0 High, 1 Medium (SG7-01), 3 Low (SG7-02..04) |
| Direction | Orchestrator triage (Claude Code as orchestrator; event 2026-11-18T04:54; D-RUN-09). SG7-01: apply the gate's fixes 1–4 with the lint-fixture option, set its default from the RWB-E1-044 spec as it stands, and ask nothing of RWB-E1-044. SG7-02..04: fix as the gate states; for the local changed-file list, use `git diff --name-only <merge-base>..HEAD` against `develop-recovery`. No human disposition is claimed. |
| Inputs read | Review round 7. RWB-E1-044 spec v14-7: SPEC-007 table, SPEC-010, SPEC-011, T-044-10..22. RWB-E1-042 spec revision 7 §12.3 (steps 1–8). RWB-E1-043 revision 4 `shared-updates.md` R4. `backend/src/main/resources/application.yaml` (`rwb.flyway.location`). `scripts/dev.ps1` (commands). Build log D-RUN-06 (local merge on a green `dev.ps1 test`). |
| Backups | `spec.run7.md`, `assumptions.run7.md`, `document-gaps.run7.md`, `shared-updates.run7.md`, `compliance-validation.run7.md`, `gate-response.run7.md`, `agent-run-log.run7.md`, `contracts/backend-apis.run7.json` |
| Changes | SPEC-TE011-003: new lint-fixture class, default `backend/src/test/resources/migration-lint/**` (`flyway-fixtures/` left out, with reasons); the migration folder is read from `rwb.flyway.location`. SPEC-TE011-008: reader precedence limited to the reader's files; `DO`-body rules made explicit (direct DDL, `DELETE`, `TRUNCATE` and DDL `EXECUTE`/`format` raise nothing); `ALTER`/`DROP FUNCTION|PROCEDURE` in class 2; `CREATE TABLE … AS` in class 4 only; a `DEFAULT` literal on a resolved personal pair is a position; "Known files" corrected for RWB-E1-042 step 3 and RWB-E1-044; non-text personal values in migrations. SPEC-TE011-013: changed-file list built from git in GitLab and in `scripts/dev.ps1 test` (required). SPEC-TE011-018: scope limited to the migration folder; target table per finding kind. SPEC-TE011-012, -015, -016 state (1) and -017 updated. T3, T12–T14; TS-TE011-07 extended; new TS-TE011-08 and -09 and unit rows. CLAR-004, -014, -015. ASM-TE011-05, -25..-27 revised; -28 and -29 new. DGL-08 and DGL-13 revised. R4 owner given as RW-COMPLY (RWB-E1-043 revision 4). Shared updates §3b items 1, 5, 6 and closing lines; "already passed" wording removed. |
| Document gaps | DGL-01..15, Blocker = No for all; no new gap |
| Spec gate | Round 8 requested from the Compliance Reviewer → `review/spec-gate-review-8.md` |
| Spec gate result (round 8) | `review/spec-gate-review-8.md`: FAIL, 0 Critical, 0 High, 0 Medium, 6 Low (SG8-01..06). SG7-01..04 resolved; rounds 1–6 still resolved. No new document gap. Low-only failure is not accepted under D-RUN-09. |
| Next step | The orchestrator's 04:54 triage allows one more specifier round on a Low-only failure: run 8, then round 9. |

## Remediation run after spec gate round 8 (2026-11-18)

| Field | Value |
|---|---|
| Trigger | `review/spec-gate-review-8.md`: FAIL, 0 Critical, 0 High, 0 Medium, 6 Low (SG8-01..06) |
| Direction | Orchestrator triage of round 7 (Claude Code as orchestrator; event 2026-11-18T04:54; D-RUN-09): if round 8 fails on Low findings only, the specifier may do one more round (run 8, then round 9). Each fix follows the gate's "Required fix". No human disposition is claimed. |
| Inputs read | Review round 8; the spec set; the `.gitlab-ci.yml` facts the gate reports (no `workflow:` block, no `rules:`) |
| Backups | `spec.run8.md`, `assumptions.run8.md`, `document-gaps.run8.md`, `shared-updates.run8.md`, `compliance-validation.run8.md`, `gate-response.run8.md`, `agent-run-log.run8.md`, `contracts/backend-apis.run8.json` |
| Changes | SPEC-TE011-018: condition (e) applies to every finding. A FIXTURE-ID in a `DEFAULT` takes that table and needs `ALTER COLUMN … DROP|SET DEFAULT`. A FIXTURE-ID in any other statement takes the table it writes, when that table can be read. SPEC-TE011-008 class 3: a catch-all for `DO`, function and procedure bodies. `EXECUTE` literal text is classed as a top-level statement. `GRANT`, `REVOKE`, `SET`, `RESET` and cursor reads are placed. SPEC-TE011-013: GitLab branch pipelines pass `origin/<targetBranch>` with `GIT_DEPTH: 0`, and no merge base gives exit 2. SPEC-TE011-003: the RWB-E1-044 AC8 form is not fixed, so a route is named for a Flyway-fixture finding; lint-fixture roots must lie under the test roots. Also updated: SPEC-TE011-001 item 2, -011, -012, -015, -016 state (1) and -017; the trigger note; T12 and T14; TS-TE011-06 (i), -07, -08 and -09 (f)(g); the unit rows; CLAR-015. The system-test rows are in order and the duplicate scan-scope scenario is removed. ASM-TE011-26..29 are revised. Contract: trigger, inputs, exit 2, `fixtureMatching`, `correctiveMigration`, and two new lines. `shared-updates.md` §3b: the rules are for orders 2–5, item 5 is information only, and nothing is asked of RWB-E1-044. |
| Document gaps | DGL-01..15, Blocker = No for all; no new gap |
| Spec gate | Round 9 requested from the Compliance Reviewer → `review/spec-gate-review-9.md` |
| Spec gate result (round 9) | `review/spec-gate-review-9.md`: FAIL, 0 Critical, 0 High, 0 Medium, 4 Low (SG9-01..04). SG8-01..06 resolved; rounds 1–7 still resolved. No new document gap. Every finding is in text that run 8 added. SG9-01: a FIXTURE-ID in an `INSERT` or `UPDATE` inside a procedural body matches two target-table rows. SG9-02: `%s` and `%L` placeholders, a literal `DEFAULT` inside `EXECUTE` text, and the class-2 list against the body catch-all (`COPY … TO`, `LOCK`, `COMMIT`). SG9-03: the changed-file list is also built for targets other than `changedFiles.targetBranch`, so a promotion from `develop-recovery` would fail. SG9-04: stale text in the status-transition exit-2 row and T10, and SPEC-RWB-E1-044-010 cited for the Flyway fixtures. A Low-only failure is not accepted under D-RUN-09. |
| Next step | Stopped as the orchestrator directed: the 04:54 triage allowed one further round only (run 8, round 9). The orchestrator triages SG9-01..04, then the Technical Specifier runs run 9 and requests round 10. |

## Remediation run after spec gate round 9 (2026-11-18)

| Field | Value |
|---|---|
| Trigger | `review/spec-gate-review-9.md`: FAIL, 0 Critical, 0 High, 0 Medium, 4 Low (SG9-01..04) |
| Direction | Orchestrator triage (Claude Code as orchestrator; event 2026-11-18T05:13; D-RUN-09). Apply each required fix of review 9 inside the sections it names. For SG9-03: a promotion of `develop-recovery` to `main` must never fail for lack of a changed-file list; the rules that need the list run only where the list is defined; the behaviour on every other target is stated and tested. Re-read the run-9 text for new contradictions before requesting round 10. No human disposition is claimed. |
| Inputs read | Review round 9; the spec set; RWB-E1-044 spec v14-7 SPEC-010 and T-044-18 (citation check) |
| Backups | `spec.run9.md`, `assumptions.run9.md`, `document-gaps.run9.md`, `shared-updates.run9.md`, `compliance-validation.run9.md`, `gate-response.run9.md`, `agent-run-log.run9.md`, `contracts/backend-apis.run9.json` |
| Changes | SG9-01: in SPEC-TE011-018, a FIXTURE-ID in an `INSERT` or `UPDATE` value takes that statement's table wherever the statement is. `(DML in procedural body)` takes each table that the body's `INSERT`, `UPDATE`, `MERGE INTO` or `COPY … FROM` names. SG9-02: in SPEC-TE011-008 class 3, only `%I` is read as a name, `%s` and `%L` give the finding (except as `COMMENT ON` text), a placeholder `DEFAULT` pair gives the finding, a literal `DEFAULT` in `EXECUTE` text is a class-2 position, the full class-2 list is allowed in bodies, and the catch-all names `COPY … FROM`. SG9-03: in SPEC-TE011-013, `ChangedFileList` takes `--branch` and builds the list only for a change into `changedFiles.targetBranch` from a branch that is not protected. Elsewhere no git command runs and (e) is not evaluated. New configuration key `changedFiles.protectedBranches`, new T15, and TS-TE011-09 (e), (h)–(k). SG9-04: the status-transition exit-2 row, T10, the compliance row and the Flyway-fixture citation (RUN-BRIEF rule 7). Aligned: SPEC-TE011-012, -015, -017 row, T11, T14, TS-TE011-06 (i), -07, unit rows, CLAR-015, ASM-TE011-26, -27, -29, the contract, and §3b item 1. Self-check pass: stale "list is empty" and bare `COPY` wording removed, and "the finding" defined for `EXECUTE` text. |
| Document gaps | DGL-01..15, Blocker = No for all; no new gap |
| Spec gate | Round 10 requested from the Compliance Reviewer → `review/spec-gate-review-10.md` |
| Spec gate result (round 10) | FAIL, 0 Critical, 0 High, 0 Medium, 3 Low (SG10-01..03); SG9-01..04 resolved |
| Next step | Low findings only, so run 10 follows under the same triage (section below) |

## Remediation run after spec gate round 10 (2026-11-18)

| Field | Value |
|---|---|
| Trigger | `review/spec-gate-review-10.md`: FAIL, 0 Critical, 0 High, 0 Medium, 3 Low (SG10-01..03) |
| Direction | Orchestrator triage (Claude Code as orchestrator; event 2026-11-18T05:13; D-RUN-09): on a Low-only failure of round 10, one more specifier round (run 10, then round 11). Each required fix of review 10 applied inside the sections it names. No human disposition is claimed. |
| Inputs read | Review round 10; the spec set |
| Backups | `spec.run10.md`, `assumptions.run10.md`, `document-gaps.run10.md`, `shared-updates.run10.md`, `compliance-validation.run10.md`, `gate-response.run10.md`, `agent-run-log.run10.md`, `contracts/backend-apis.run10.json` |
| Changes | SG10-01: `.gitlab-ci.yml` creates branch and tag pipelines (trigger note, SPEC-TE011-013, contract, CLAR-015, ASM-TE011-29). A tag pipeline fetches nothing and passes no changed-file option, so no list is built. A branch pipeline uses a non-fatal fetch and `--branch "$CI_COMMIT_BRANCH"`. A `--branch` that is missing, empty or `HEAD` gives exit 2, `changed-file list: branch not determined` (replaces `--branch not given`; SPEC-TE011-012, status matrix, T14, contract key `changedFileBranchUndeterminedLine`). Also T15 (tag pipeline), TS-TE011-09 (k) and new (l), and the unit row. SG10-02: the SPEC-TE011-018 table applies the readable-table rules at top level, in bodies and in literal `EXECUTE` text. `(DML in procedural body)` also takes `CREATE TABLE <t> AS` and literal-`EXECUTE` writes. "None" applies only where no written table can be read. Contract matches. Unit scenarios added. SG10-03: "only `%I` placeholders" added to the known-files row, the SPEC-TE011-017 row and ASM-TE011-27. Every specifier form other than `%I` follows the `%s`/`%L` rule, and `%%` is literal; unit scenarios use `%1$I … %2$L` and `%%`. Contract phrase "DML in a DO block" replaced. TS-TE011-09 (e) now states exit 1. ASM-TE011-29 risk says "where the list is built" and names the not-built line. Unit Output row now reads "paths, branch names and counts". Self-check: CLAR-015 "the only kind" removed; the sentence that callers "always pass a branch name" was corrected for the local detached case; the line-386 wording was aligned. |
| Document gaps | DGL-01..15, Blocker = No for all; no new gap |
| Spec gate | Round 11 requested from the Compliance Reviewer → `review/spec-gate-review-11.md` |
| Spec gate result (round 11) | FAIL, 0 Critical, 0 High, 0 Medium, 3 Low (SG11-01..03); SG10-01..03 resolved; no earlier finding reopened |
| Next step | Orchestrator triage, recorded in the section below |

## Remediation run after spec gate round 11 (2026-11-18)

| Field | Value |
|---|---|
| Trigger | `review/spec-gate-review-11.md`: FAIL, 0 Critical, 0 High, 0 Medium, 3 Low (SG11-01..03) |
| Direction | Orchestrator (Claude Code) directed remediation run 11 under D-RUN-09, with a churn direction: fix exactly the three findings and simplify rather than add cases, keeping the change inside the existing rule text. The stage was told not to run the gate and not to spawn a reviewer; the orchestrator runs round 12. No human disposition is claimed. |
| Inputs read | Review round 11; the spec set; `.gitlab-ci.yml` re-read (`backend-recovery-it` `rules: changes:` at lines 45–50) |
| Backups | `spec.run11.md`, `assumptions.run11.md`, `document-gaps.run11.md`, `shared-updates.run11.md`, `compliance-validation.run11.md`, `gate-response.run11.md`, `agent-run-log.run11.md`, `contracts/backend-apis.run11.json` |
| Changes | SG11-01: in SPEC-TE011-018, `(d)` requires `DROP DEFAULT`/`SET DEFAULT` only for a literal column, and a `DEFAULT` whose table is a placeholder is a finding no corrective migration accepts; `(DML in procedural body)` takes `ALTER TABLE <t> ADD COLUMN … DEFAULT` and `ALTER COLUMN … SET DEFAULT`, and shares one phrase with the lead sentence and the contract ("literal `EXECUTE` text or a `format` call with a literal format string"); four unit scenarios. SG11-02: the "no merge request pipeline" claim is corrected in the trigger note, SPEC-TE011-013, ASM-TE011-29, CLAR-015 and the contract; `pdpa-lint` carries `rules:` for `merge_request_event`, branch and tag pipelines, so a merge request pipeline exists for every merge request, the job runs in it and wherever `backend-recovery-it` runs, and the duplicate-pipeline case is stated; the merge request bullet is no longer conditional; a configuration check is added. SG11-03: (e) lists the no-option/tag case; the "carries only files that met (e)" claim is limited to commits already merged into the target branch and a no-option run elsewhere is stated not to be a merge gate; the job deletes `refs/remotes/origin/<target>` before the non-fatal fetch, so a failed fetch gives exit 2 instead of reading a stale ref; unit scenario added. |
| Document gaps | DGL-01..15, Blocker = No for all; no new gap |
| Spec gate | Not run in this stage, as directed: the orchestrator runs round 12 |
| Next step | Orchestrator runs spec gate round 12 (`review/spec-gate-review-12.md`) |

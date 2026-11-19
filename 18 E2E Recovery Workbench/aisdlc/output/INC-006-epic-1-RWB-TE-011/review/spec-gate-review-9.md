# Spec gate review, round 9: RWB-TE-011 PDPA lint for code, tests and logs

| Field | Value |
|---|---|
| RUN_ID | `INC-006-epic-1-RWB-TE-011` |
| Gate | Spec gate, re-review round 9 (Compliance Reviewer, independent of the author) |
| Earlier rounds | Round 1 `review/spec-gate-review.md` (FAIL, 2 Medium, 5 Low); round 2 `-2.md` (FAIL, 1 Medium, 1 Low); round 3 `-3.md` (FAIL, 2 Low); round 4 `-4.md` (FAIL, 3 Medium, 1 Low) with `document-gaps-4.md`; round 5 `-5.md` (FAIL, 1 Medium, 3 Low) with `document-gaps-5.md`; round 6 `-6.md` (FAIL, 4 Low); round 7 `-7.md` (FAIL, 1 Medium, 3 Low); round 8 `-8.md` (FAIL, 6 Low: SG8-01..SG8-06) |
| Reviewed | `specify/spec.md` (SPEC-TE011-001..018, revised 18 Nov 2026 after round 8), `assumptions.md` (ASM-TE011-01..29), `document-gaps.md` (DGL-01..15, unchanged since run 7), `shared-updates.md` (§1–§5, including §3b), `gate-response.md` ("Gate response — round 8"), `compliance-validation.md`, `agent-run-log.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `evidence/`; the `*.run8.*` copies, compared with `diff --strip-trailing-cr` |
| Direction checked | The round-7 triage came from the orchestrator (Claude Code), logged at 2026-11-18T04:54. It allowed one further specifier round (run 8) on a Low-only failure. It is an agent's direction, not a human's. D-RUN-06, -07, -08, -09, -15, -17 (`AI-SDLC-BUILD-LOG.md` §1). Under D-RUN-09, Low findings are fixed, not accepted |
| Cross-story input (read only) | RWB-E1-044 spec v14-7 (`INC-001`: SPEC-RWB-E1-044-007, -010, -011; restated AC8; T-044-10..T-044-22); RWB-E1-042 spec revision 9 (`INC-003`, §12.3, identical to revision 8); RWB-TE-001 v4 (`INC-002`); RWB-TE-002 (`INC-004`); RWB-TE-003 (`INC-005`); RWB-E1-043 (`INC-008`, now revision 6: open item R4 and `shared-updates.md` §3.2 unchanged from revision 4); RWB-E1-001 (`INC-009`); RWB-E1-064 story file v1 (Story Files v7 §11: DF-REF-105 `is_personal` Read); `AGENTS.md` §3.7, §4.6; decision register D-RCV-28, D-RCV-50, L-RCV-13 |
| Checked against | `.gitlab-ci.yml` (no `workflow:` block; `backend-unit` and `frontend-check` have no `rules:`; header comment "the ACE pipeline on the develop-recovery MR"); `backend/src/main/resources/application.yaml` (`rwb.flyway.location: classpath:db/modulemigration/recovery`); `scripts/dev.ps1` (`ValidateSet`; `test` runs Gradle `test`, then `npm run check`); today's tree (migration folder holds `README.md` only; `backend/src/test/resources/` holds `architecture/` only) |
| Method | Diff of every changed file against its `run8` copy, then a full read of SPEC-TE011-001, -003, -008, -011..-018, the trigger note, the status-transition and exception tables, the test tables and the coverage table. Each new claim about another story was checked in that story's specification. Greps of `specify/` (backups excluded) for e-mail addresses, runs of 9 or more digits and stale phrases; the scripts printed counts only. Both contracts parsed as JSON |
| Date | 2026-11-18 |
| Reviewer | Compliance Reviewer (agent) |

## 1. Result

**Overall status: FAIL**

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 4 |

**Round 8.** SG8-01 to SG8-06 are resolved. Each was checked against `spec.md` and the other artefacts,
not against `gate-response.md` alone. No finding from rounds 1–7 has reopened.

Four new Low findings remain. All four are in text that run 8 added or changed. Under D-RUN-09 Low findings
are fixed, not accepted, so the gate fails.

- **SG9-01.** In the target-table table, an `INSERT` or `UPDATE` inside a `DO`, function or procedure body
  fits two FIXTURE-ID rows that give different answers.
- **SG9-02.** Several points in the new class-3 text are open:
  - an `EXECUTE` placeholder is read as a name even where it stands for a clause;
  - a literal `DEFAULT` inside `EXECUTE` text is not covered;
  - the list of direct class-2 statements in a `DO` body conflicts with the catch-all for `COPY … TO` and
    other class-2 forms.
- **SG9-03.** The changed-file list is also built on `main`, `develop` and merge requests that target
  them. There, a merged migration that has already been corrected can fail the pipeline, and no remedy
  exists.
- **SG9-04.** Four stale or over-cited text items.

## 2. Disposition of round-8 findings

| Finding | Severity | Disposition | Evidence (checked against the spec, not against `gate-response.md` alone) |
|---|---|---|---|
| SG8-01 Condition (e) dropped for findings with no target table | Low | **Resolved** | SPEC-TE011-018 (d): "A finding with no target table needs no table write: (d) is met, and (a) to (c) and (e) still apply". (e): "(e) applies to every finding, with or without a target table". These agree with T11 ("(a) to (e)"). ASM-TE011-26 ("every other condition still applies, including that the original is not on the changed-file list"); contract `correctiveMigration` ("the changed-file condition applies to every finding"); unit row "Corrective migration" ("accepted on (a) to (c) and (e); the same with O on the changed-file list → still a finding"); TS-TE011-09 (f) (O2 with a `DO`-block `INSERT` plus C2 → exit 1). |
| SG8-02 FIXTURE-ID in a `DEFAULT` had no table; FIXTURE-ID rows not exhaustive | Low | **Resolved.** A residual overlap between two of the new rows is raised as SG9-01. | New rows: "FIXTURE-ID in a `DEFAULT` … That table; C also needs `ALTER COLUMN … DROP|SET DEFAULT`", and "FIXTURE-ID in any other statement → the table the statement writes, when the lint can read it (`COPY <t>` with its data block, `MERGE INTO <t>`, `SELECT … INTO <t>`, `CREATE TABLE <t> AS`); otherwise none". (d) applies the `ALTER COLUMN` need to both rule kinds. Contract aligned. Unit scenarios for `ADD COLUMN … DEFAULT` and a `COPY` data block. |
| SG8-03 No catch-all in procedural bodies; `EXECUTE` leading-keyword test | Low | **Resolved.** Residual gaps in the new text are raised as SG9-02. | Class 3 `DO` list: no-finding reads (cursor `OPEN`/`FETCH`/`MOVE`/`CLOSE` added); direct class-2 statements (`GRANT`, `REVOKE`, `SET`, `RESET` named); `EXECUTE` text "classed as it would class a top-level statement"; "Finding, as a catch-all: every other statement" (`CALL`, class 4, unknown keyword). The function-body paragraph applies the same catch-all. ASM-TE011-27, contract `fixtureMatching` and §3b item 1 match. TS-TE011-07 and the unit row cover `CALL` in a `DO` body, `EXECUTE 'CREATE TABLE t AS VALUES …'` and a direct `ALTER ROLE`. |
| SG8-04 GitLab list never built; merge-base failure undefined | Low | **Resolved.** The new branch-pipeline rule raises SG9-03, and the status matrix was not updated (SG9-04). | SPEC-TE011-013 first bullet: "GitLab creates branch (push) pipelines only … It creates no merge request pipeline … `GIT_DEPTH: 0`". The "GitLab branch pipeline" bullet passes `origin/<targetBranch>` on any other branch. "No merge base" gives exit 2 and "never falls back to an empty list". This is in T14, SPEC-TE011-012, contract `changedFileNoMergeBaseLine`, the unit row (unrelated histories and a depth-1 clone) and TS-TE011-09 (g). The trigger note, CLAR-015, ASM-TE011-29 and "Impacted Existing Nodes" (`GIT_DEPTH: 0`) match. |
| SG8-05 Flyway-fixture over-claim; mixed §3b message; unbounded lint-fixture roots | Low | **Resolved.** One citation in the new rule over-reaches (SG9-04 item 3). | (1) SPEC-TE011-003 says RWB-E1-044 does not fix the AC8 form. The reviewer confirmed that E1-044 v14-7 restated AC8 says "A fixture whose second statement references a missing table", and T-044-14 gives no form. The spec states that a column-less `INSERT` gives `(columns not named)`, and the new rule "If a merged Flyway fixture gives a finding" names the route. "Known files", state (1), the SPEC-TE011-017 row and ASM-TE011-28 match. (2) §3b now addresses rules 1–4 and 6 to orders 2–5 only, says "RWB-E1-044 is not asked anything", and labels item 5 "For information only". (3) "Bound": every lint-fixture root must lie under a test root, otherwise exit 2. This is in T12, SPEC-TE011-012 and -015, the unit row "Scan scope", TS-TE011-08 and the contract. |
| SG8-06 Stale and inconsistent text | Low | **Resolved** | (1) TS-TE011-06 (i) uses `--changed-files-from-git develop-recovery` in a temporary repository. No `--changed-files ` remains. (2) The system-test rows run -01 to -09. (3) The duplicate "`dictionary.migrationFolder` … → exit 2" scenario is gone. (4) SPEC-TE011-001 item 2 and SPEC-TE011-011 read the folder from `rwb.flyway.location`. (5) The ASM-TE011-29 risk now says that a changed location gives exit 2 (T12) until code owners change the root. |

**Regression check, rounds 1–7.** No finding has reopened. The reviewer re-checked:

- SG-01 (9 Restricted fields);
- SG-04 (`infra/postgres/schema/**` is the only `infra` exclusion);
- SG2-01 (14 of 18; 509);
- SG4-01 ((object, field) matching; no allow entry on a migration; point in time);
- SG4-03 (R1/R2 reader; fail closed);
- SG5-01 (per-pair resolution);
- SG5-03 (`(columns not named)`);
- SG6-02 (the migration folder cannot be left out, and neither can lint-fixture roots);
- SG7-01 (lint-fixture class; nothing asked of RWB-E1-044);
- SG7-02 (E1-042 §12.3 steps 1–8; revision 9 §12.3 is identical to revision 8);
- SG7-03 (target-table table, scope, `rwb.flyway.location`).

The counts 18 / 14 / 509 / 526 / 390 / 71 still agree. The coverage table has 32 rows (`TOTAL_RULES: 32`).

## 3. New findings

### REVIEW-TE011-SG9-01: A FIXTURE-ID in an `INSERT` or `UPDATE` inside a procedural body fits two target-table rows (Low)

- **Affects:** SPEC-TE011-018 (d), the target-table table; contract `correctiveMigration`; unit row
  "Corrective migration".
- **Evidence:**
  1. **Row "FIXTURE-ID in a value of an `INSERT` or `UPDATE`".** It gives "That statement's table". It
     does not exclude statements inside a body. Class 3 splits `DO`, function and procedure bodies into
     statements, so the lint can read the table of an `INSERT` or `UPDATE` there.
  2. **Row "FIXTURE-ID in any other statement".** It gives "otherwise none (… a `DO`, function or
     procedure body …)". The contract also says "A finding with no target table (FIXTURE-ID in … a
     procedural body …)".
  3. **The conflict.** Take a 13-digit ID in `DO $$ BEGIN INSERT INTO t (c) VALUES ('<id>'); END $$`.
     - Under the first row, C must hold an `UPDATE`, `DELETE` or `TRUNCATE` on `t`.
     - Under the second row, C needs no table write.

     The same holds for a function-body `INSERT`. Its FIXTURE-FIELD finding takes "the position's table",
     because class 3 checks function-body `INSERT`s as position forms. Its FIXTURE-ID finding may take
     none.
  4. **The harm.** The `DO`-body ID is written to rows of `t`. The SG8-02 principle is that a value which
     reaches rows needs a data change. The weaker reading lets C carry no data change.
  5. **No test.** No unit scenario covers either case.
- **Required fix:**
  1. Say which row wins. Recommended: a FIXTURE-ID in a value of an `INSERT` or `UPDATE` takes that
     statement's table wherever the statement is, including inside a `DO`, function or procedure body.
     The "otherwise none" list then names only body text that is not such a value.
  2. Align the contract.
  3. Add unit scenarios: an ID in a `DO`-body `INSERT` gives `t`, and C without a write on `t` is not
     accepted. Add the function-body equivalent.

### REVIEW-TE011-SG9-02: The new class-3 text leaves three cases open (Low)

- **Affects:** SPEC-TE011-008 class 3 (`DO` bullets and the function-body paragraph); ASM-TE011-27;
  contract `fixtureMatching`; `shared-updates.md` §3b item 1; unit row "SQL statement classes"; TS-TE011-07.
- **Evidence:**
  1. **A placeholder that stands for a clause.** The lint reads "each `%I`, `%s` or `%L` placeholder as a
     name". Only a placeholder "in a `DEFAULT` clause" gives a finding.

     Take `EXECUTE format('ALTER TABLE t %s', v)`, where an earlier assignment (no finding) sets `v` to
     `ADD COLUMN c text DEFAULT '<text>'`. Read with `%s` as a name, the text is `ALTER TABLE …`, which is
     class 2, so it raises nothing. It still writes the value into every existing row of `t`, the harm
     that makes a `DEFAULT` a position in class 2.

     A `DEFAULT` whose table or column is an `%I` placeholder also raises nothing. The pair can never be
     resolved, and class 2 checks a `DEFAULT` only "when … the pair (table, column) is resolved and
     personal". So `format('ALTER TABLE %I ADD COLUMN %I text DEFAULT ''<text>''', …)` passes.
  2. **A literal `DEFAULT` inside `EXECUTE` text.** The direct-DDL bullet says "A `DEFAULT` literal in
     such DDL is checked as in class 2". The `EXECUTE` bullet says "No finding" when the text is class 2.
     It names only a placeholder in a `DEFAULT`, not a literal. So it is open whether
     `EXECUTE 'ALTER TABLE case_note ADD COLUMN description text DEFAULT ''<text>'''`, on a resolved
     personal pair, is a finding.
  3. **The direct class-2 list conflicts with the catch-all.**
     - The `DO` bullet reads "a direct statement of class 2 (DDL as listed there, `COMMENT ON`, `GRANT`,
       `REVOKE`, `SET`, `RESET`, `DELETE` and `TRUNCATE`)".
     - Class 2 also holds `COPY … TO`, `LOCK`, `REFRESH MATERIALIZED VIEW`, `ANALYZE`, transaction control
       and `SELECT` without `INTO`.
     - The catch-all names `COPY` without a direction.

     So `COPY t TO STDOUT`, `LOCK TABLE t` or `COMMIT` in a `DO` body is either no finding (class 2) or a
     finding (catch-all or "keyword not listed here"). PostgreSQL allows `COMMIT` in a `DO` block.
- **Required fix:**
  1. Read only `%I` as a name. A `%s` or `%L` placeholder outside `COMMENT ON` text gives the finding. A
     `DEFAULT` clause in `EXECUTE` text gives the finding when its table or column is a placeholder.
  2. State that a literal `DEFAULT` in `EXECUTE` text is checked as in class 2.
  3. Make the class-2 parenthetical either the whole class-2 list or an explicit subset. Write the
     catch-all as `COPY … FROM`.
  4. Align ASM-TE011-27, the contract and §3b item 1.
  5. Add unit scenarios for `format('ALTER TABLE t %s', v)`, a literal `DEFAULT` in `EXECUTE` text on a
     personal pair, and `COPY t TO STDOUT` in a `DO` body.

### REVIEW-TE011-SG9-03: The changed-file list is built for downstream branches and promotion merge requests, where a corrected migration has no remedy (Low)

- **Affects:** SPEC-TE011-013 ("GitLab branch pipeline", "GitLab merge request pipeline" and the ACE
  bullet); SPEC-TE011-018 (e); ASM-TE011-29; contract `inputs` "Changed-file list"; unit row
  "Changed-file list"; TS-TE011-09.
- **Evidence:**
  1. **Who the list is for.** Condition (e) exists so that "a file added or edited in the same change is
     fixed in the file, not corrected". That makes sense only for a change that merges into
     `changedFiles.targetBranch` (`develop-recovery`), where O can still be edited.
  2. **Downstream branches are included.** SPEC-TE011-013 builds the list "on any branch other than
     `changedFiles.targetBranch`". The same section says branch pipelines run on `main` and `develop`.
     The merge-request rule uses `$CI_MERGE_REQUEST_TARGET_BRANCH_NAME` whatever the target is.
     SPEC-TE011-013 also says "In ACE the same check runs in the ACE pipeline on the `develop-recovery`
     merge request" (D-RCV-50).
  3. **The failure case.** A promotion from `develop-recovery` to `develop` lists every recovery file
     added since the last promotion. This happens in an MR that targets `develop`, or in a `develop` or
     `main` branch pipeline after a squash or cherry-pick promotion. Suppose O was merged into
     `develop-recovery` and later corrected by C, which met (a) to (e) there. In the promotion, O is on
     the list, so (e) fails and O's finding fails the pipeline.
  4. **No remedy.** O is merged and cannot be edited (`AGENTS.md` §4.6). No allow entry or exclusion may
     excuse it (SPEC-TE011-018 "Nothing else excuses O"). The promotion is blocked with no way forward.
  5. **No test.** No scenario covers a target other than `develop-recovery`.
- **Required fix:**
  1. Build the list only for a change whose target is `changedFiles.targetBranch`:
     - a merge request pipeline whose `$CI_MERGE_REQUEST_TARGET_BRANCH_NAME` equals it;
     - a branch pipeline on a branch other than the target and the protected branches `main` and
       `develop` (L-RCV-13).

     Everywhere else, pass no option, so the list is empty, as on the target branch itself.
  2. Align ASM-TE011-29 and the contract.
  3. Add a unit or TS-TE011-09 case: a branch named `develop` holding O and C, built from a squashed
     promotion, gives exit 0 with the `corrected by` notice.

### REVIEW-TE011-SG9-04: Stale and over-cited text (Low)

- **Affects:** Status-transition matrix; T10; `compliance-validation.md` §1 row "Unrecognised SQL fails
  closed"; SPEC-TE011-003 "If a merged Flyway fixture gives a finding".
- **Evidence:**
  1. **Status-transition matrix.** The exit-2 row lists "a changed-file target branch that cannot be
     resolved". It omits two exit-2 cases that run 8 added to SPEC-TE011-012, T12, T14 and the contract:
     a lint-fixture root outside the test roots, and no merge base.
  2. **T10 and the compliance row describe the old rule.** T10 reads "or DML in a `DO` body". The
     `compliance-validation.md` row reads "anything else and DML in a `DO` block is a finding". After
     SG8-03, the finding covers every unlisted statement in a `DO`, function or procedure body, including
     `CALL`, a class-4 statement and an unknown keyword.
  3. **Citation.** The new rule says "RWB-E1-044 SPEC-RWB-E1-044-010 requires its fixtures to be
     synthetic", as a reason to move a Flyway fixture into the lint-fixture class. SPEC-RWB-E1-044-010
     ("Lint testability and fixtures") is about the lint fixtures under `migration-lint/`.
     SPEC-RWB-E1-044-011, which covers the Flyway fixtures, does not state it. The basis for the Flyway
     fixtures is RUN-BRIEF rule 7, with E1-044's "All names are synthetic" and "synthetic table" wording
     in its test rows.
- **Required fix:**
  1. Add both cases to the status-transition exit-2 row.
  2. Restate T10 and the compliance row as "any statement in a `DO`, function or procedure body that the
     class-3 rules do not list".
  3. Cite RUN-BRIEF rule 7 (and E1-044's test-row wording) for the Flyway fixtures, or limit the
     SPEC-RWB-E1-044-010 citation to the lint fixtures.

## 4. Other checks

| Check | Result |
|---|---|
| Personal data in the artefacts | None found. No e-mail address and no run of 9 or more digits in `specify/` outside the `*.run*` backups. Only synthetic values and placeholders are used (`SYN-…`, `<text>`, `<id>`, `V0003__rwb_e1_042_seed.sql`, `V0004__rwb_e1_042_seed2.sql`). The reviewer's scripts printed counts only. |
| Secrets | None. |
| Contracts | Both parse as JSON. The new lines `lintFixtureRootOutsideLine` and `changedFileNoMergeBaseLine` match SPEC-TE011-003 and -013. The exit-2 list matches SPEC-TE011-012. `correctiveMigration` carries the SG9-01 overlap. `inputs` "Changed-file list" carries the SG9-03 scope. `NO_API_CHANGE` is consistent. |
| Authorization and audit | Unchanged and appropriate for a build tool. Change control is through code owners (SPEC-TE011-014). `lintFixtureRoots` and `changedFiles.targetBranch` are configuration under that entry (SPEC-TE011-015), and the new bound stops a lint-fixture root from silencing the log rules on production source. Running `git` reads repository metadata only, with no database and no network (story §13, §17). |
| Unit Test Applicability | Compliant. The front end is `NOT_APPLICABLE` with evidence. The tool back end is `REQUIRED` at 80% on JaCoCo LINE, BRANCH, METHOD and INSTRUCTION. SG9-01..SG9-03 add scenarios. |
| Evidence | No new script. The new claims rest on other stories' specifications and repository files, which the reviewer read directly: E1-044 SPEC-010/-011, restated AC8, T-044-14, -18, -21, -22; E1-042 revision 9 §12.3; `.gitlab-ci.yml`; `application.yaml`; `dev.ps1`. |
| Cross-story versions | RWB-E1-042 moved to revision 9 (05:16) and RWB-E1-043 to revision 6 (05:24), after run 8 had read them. E1-042 §12.3 is identical in revision 9. E1-043 revision 6 keeps open item R4 (owner RW-COMPLY, blocks RWB-E1-064) and its `shared-updates.md` §3.2 forward note (`validate` refuses an `is_personal` change, 422 MSG-P1-002; `apply` and `onRolledBack` never write it). It still asks nothing of RWB-TE-011 (GAP-38). SRC-25 and the E1-044 v14-7 citations remain correct in substance; no finding. E1-044 (01:35), TE-001, TE-002, TE-003 and E1-001 have not changed since round 8. |
| Run decisions | D-RUN-06: the local merge gate on the branch is matched by `dev.ps1 test` with the branch as HEAD. Today the repository has only the local branch `develop-recovery` (read from `.git/HEAD` and `refs/heads`; git was not run). D-RUN-07: no number is fixed. D-RUN-08: no dependency on a later story; nothing is asked of RWB-E1-044 (§3b, SPEC-TE011-003, -017). D-RUN-09 is applied. D-RUN-15 and D-RUN-17 are unchanged. The triage is attributed to the orchestrator (Claude Code), and no human disposition is claimed. The build log has no row for the round-8 gate, for specifier run 8 or for a TE-011 triage after 04:59:09. That is the orchestrator's log to complete, not a defect in this specification. |
| Data classification (pdlc stop condition) | The classification source, the residual risk, both RWB-E1-001 outcomes and the load-route limit are visible. R4 (RW-COMPLY) is consistent with RWB-E1-043 revision 6. The RWB-E1-064 story file lists DF-REF-105 `is_personal` as Read, as DGL-13 says. No open data-classification blocker belongs to this story. |
| Document gaps | No new document gap. The findings concern this specification, not the document set. `review/document-gaps-9.md` is not written. |

## 5. Gate output

```text
REVIEW_STATUS: FAIL
REVIEW_COUNTS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 4]
ROUND_8_DISPOSITION: SG8-01 Resolved ((e) applies to every finding; ASM-26, contract, unit row; TS-09 (f)). SG8-02 Resolved (FIXTURE-ID DEFAULT row and catch-all row; unit scenarios); residual row overlap in SG9-01. SG8-03 Resolved (body catch-all; GRANT/REVOKE/SET/RESET; EXECUTE text classed as top level); residual gaps in SG9-02. SG8-04 Resolved (branch pipelines pass origin/<targetBranch>, GIT_DEPTH 0, no merge base exit 2; T14, TS-09 (g)); downstream scope in SG9-03, status matrix in SG9-04. SG8-05 Resolved (AC8 form not fixed, named route; section 3b asks nothing of E1-044; lint-fixture roots bounded to test roots); citation in SG9-04. SG8-06 Resolved
ROUND_1_7_DISPOSITION: all remain Resolved; no regression
NEW_FINDINGS: SG9-01 Low (FIXTURE-ID in an INSERT/UPDATE inside a DO, function or procedure body fits both "that statement's table" and "none"); SG9-02 Low (%s/%L placeholders read as names even for a clause, and a DEFAULT with %I table or column passes; literal DEFAULT in EXECUTE text unaddressed; DO-body class-2 parenthetical vs catch-all for COPY ... TO, LOCK, COMMIT); SG9-03 Low (changed-file list built on main/develop and for MRs to any target, so a promotion lists a merged and corrected O, which fails with no remedy); SG9-04 Low (status matrix exit-2 row lacks lint-fixture-root and no-merge-base cases; T10 and the compliance row still say DML in a DO body; SPEC-RWB-E1-044-010 cited for Flyway fixtures)
NEW_DOCUMENT_GAPS: none
CROSS_STORY_RWB-E1-044: Consistent with v14-7 (SPEC-010 lint fixtures; SPEC-011 Flyway fixtures; restated AC8 and T-044-14 fix no statement form); nothing asked of it
CROSS_STORY_RWB-E1-042: Revision 9 section 12.3 identical to revision 8; Known-files row correct; guard form requested through the orchestrator
CROSS_STORY_RWB-E1-043: Revision 6 keeps R4 (RW-COMPLY) and the section 3.2 forward note; nothing asked of TE-011
CROSS_STORY_RWB-E1-001: Consistent; unchanged since round 8
CROSS_STORY_RWB-TE-001/-002/-003: Consistent; unchanged since round 8
BLOCKING: YES under D-RUN-09 (Low-only failure is not accepted by the orchestrator; REVIEW_GATE_WARNING would otherwise apply)
NEXT_STEP: The orchestrator triages SG9-01..SG9-04. Under D-RUN-09 the Technical Specifier fixes all four, then requests spec gate round 10 (review/spec-gate-review-10.md). This review does not start the Implementation Planner.
```

# Spec gate review, round 11: RWB-TE-011 PDPA lint for code, tests and logs

| Field | Value |
|---|---|
| RUN_ID | `INC-006-epic-1-RWB-TE-011` |
| Gate | Spec gate, re-review round 11 (Compliance Reviewer, independent of the author) |
| Earlier rounds | Round 1 `review/spec-gate-review.md` (FAIL, 2 Medium, 5 Low); round 2 `-2.md` (FAIL, 1 Medium, 1 Low); round 3 `-3.md` (FAIL, 2 Low); round 4 `-4.md` (FAIL, 3 Medium, 1 Low) with `document-gaps-4.md`; round 5 `-5.md` (FAIL, 1 Medium, 3 Low) with `document-gaps-5.md`; round 6 `-6.md` (FAIL, 4 Low); round 7 `-7.md` (FAIL, 1 Medium, 3 Low); round 8 `-8.md` (FAIL, 6 Low); round 9 `-9.md` (FAIL, 4 Low); round 10 `-10.md` (FAIL, 3 Low: SG10-01..SG10-03) |
| Reviewed | `specify/spec.md` (SPEC-TE011-001..018, revised 18 Nov 2026 after round 10), `assumptions.md` (ASM-TE011-01..29), `document-gaps.md` (DGL-01..15, unchanged since run 7), `shared-updates.md` (§1–§5, including §3b), `gate-response.md` ("Gate response — round 10" and its self-check note), `compliance-validation.md`, `agent-run-log.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `evidence/`; the `*.run10.*` copies, compared with `diff --strip-trailing-cr` |
| Direction checked | Run 10 is the one further Low-only round that the orchestrator (Claude Code) allowed in its round-9 triage (cited in the specification as 2026-11-18T05:13; the build log row carries 2026-11-18T05:31:18 and reads "one further Low-only round allowed (run 10, review-11)"). It is an agent's direction, not a human decision. D-RUN-06, -07, -08, -09 (`AI-SDLC-BUILD-LOG.md` §1). Under D-RUN-09 Low findings are fixed, not accepted, and a Low that is not fixed goes to the engagement lead for a human disposition |
| Cross-story input (read only) | RWB-E1-044 spec v14-7 (`INC-001`, unchanged since 01:35); RWB-E1-042 spec revision 12 (`INC-003`; §12.3 identical to its `spec.run9.md` copy); RWB-TE-001 v4 (`INC-002`); RWB-TE-002 (`INC-004`); RWB-TE-003 (`INC-005`); RWB-E1-043 revision 8 (`INC-008`; open item R4 in its `shared-updates.md`, the RWB-E1-064 forward note and "asked for nothing by this story (GAP-38)" unchanged); RWB-E1-001 (`INC-009`, unchanged); `AGENTS.md` §3.7, §4.6; D-RCV-28, D-RCV-50, L-RCV-13 |
| Checked against | `.gitlab-ci.yml` (no `workflow:` block and no `include:`; `backend-unit` and `frontend-check` have no `rules:` or `only:`; **`backend-recovery-it` has `rules:` whose first entry is a `changes:` list with no `if:`**); `scripts/dev.ps1` (`ValidateSet` has no `pdpa-lint` yet; `test` runs Gradle `test`); today's tree (migration folder holds `README.md` only; `.git/HEAD` is `refs/heads/develop-recovery`; git was not run) |
| Method | Diff of every changed file against its `run10` copy (59 new and 40 removed lines in `spec.md`, all inside the trigger note, SPEC-TE011-008 class 3 and its known-files row, -012, -013, -017, -018, the status and exception tables, TS-TE011-09, the unit rows and CLAR-015). Then a full read of SPEC-TE011-008 class 2 and class 3, -012, -013, -017, -018, the status-transition and exception tables (T10–T15), TS-TE011-07/-09 and the unit rows, cross-read against ASM-TE011-26, -27, -29, CLAR-015, §3b and the contract. Greps of `specify/` (backups excluded) for e-mail addresses and runs of 9 or more digits printed counts only (0 and 0). Both contracts parsed as JSON |
| Date | 2026-11-18 |
| Reviewer | Compliance Reviewer (agent) |

## 1. Result

**Overall status: FAIL**

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 3 |

**Round 10.** SG10-01, SG10-02 and SG10-03 are resolved. Each required fix was applied as written, and
each was checked against `spec.md` and the other artefacts, not against `gate-response.md` alone. No
finding from rounds 7–9 (or earlier) has reopened.

Three new Low findings remain. Under D-RUN-09 Low findings are fixed, not accepted, so the gate fails.

- **SG11-01.** The new SPEC-TE011-018 rule says "None" applies only where no written table can be read.
  The `(DML in procedural body)` row still uses a closed list. That list leaves out a `DEFAULT` written
  through `EXECUTE` text on a literal table, although class 2 says `ADD COLUMN … DEFAULT` writes every
  existing row. The phrase "literal `EXECUTE` text" is also used where the lead sentence says "literal
  `EXECUTE` text or a `format` string".
- **SG11-02.** "It creates no merge request pipeline" is not accurate for this `.gitlab-ci.yml`. The
  `rules: changes:` of `backend-recovery-it` makes GitLab create a merge request pipeline for a merge
  request that touches the migration folder. The `pdpa-lint` job is not in that pipeline.
- **SG11-03.** Some text was not aligned after run 10:
  - SPEC-TE011-018 (e) does not list the no-option (tag pipeline) case.
  - The claim "such a run carries only files that met (e)" is now too broad.
  - The non-fatal fetch claim fails where the runner keeps an old remote-tracking ref.

## 2. Disposition of round-10 findings

| Finding | Severity | Disposition | Evidence (checked against the spec, not against `gate-response.md` alone) |
|---|---|---|---|
| SG10-01 Tag pipelines build the list; fetch before the tool decides; detached `HEAD` | Low | **Resolved.** All six parts of the required fix are applied. New issues in the same bullet are raised as SG11-02 (merge request pipelines) and SG11-03 items 2–3. | (1) SPEC-TE011-013 first bullet: "GitLab creates a pipeline for every branch push and every tag push"; trigger note "branch pipelines and tag pipelines". (2) "**Tag pipeline** (`$CI_COMMIT_TAG` set): the job fetches nothing and passes no changed-file option, so the list is not built"; branch pipeline passes `--branch "$CI_COMMIT_BRANCH"`; T15 "no option (for example a GitLab tag pipeline)". (3) "non-fatal fetch (a failed fetch is ignored) … On `develop-recovery`, `main` and `develop` it builds no list, so a failed fetch there has no effect". (4) "`--branch` missing, empty or `HEAD` (a detached checkout) fails with exit 2, `changed-file list: branch not determined`, before any other check"; the local path: "On a detached checkout `git rev-parse` prints `HEAD`, and the run gives exit 2". (5) ASM-TE011-29 "a tag pipeline passes no option, so no list is built"; contract `inputs` "GitLab tag pipeline: no option, no fetch, list not built", key `changedFileBranchUndeterminedLine`; CLAR-015 "tag pipelines pass no option". The status matrix, SPEC-TE011-012 and the contract exit-2 text all name "missing, empty or `HEAD`". (6) TS-TE011-09 (l): "run with no changed-file option as a GitLab tag pipeline runs it → … exit 0 and one `corrected by` notice"; (k) adds `--branch HEAD`; unit row: "with an empty `--branch` or with `--branch HEAD` → exit 2 `branch not determined`, before any git command". |
| SG10-02 Target tables inside procedural bodies split between rows | Low | **Resolved** as written. A remaining case (a `DEFAULT` written through `EXECUTE` text on a literal table) and a wording mismatch are raised as SG11-01. | (1) New lead sentence: the readable-table rules "apply wherever the statement is: at top level, inside a `DO`, function or procedure body, and inside literal `EXECUTE` text or a `format` string whose table is literal". The `(DML in procedural body)` row now covers "an `INSERT`, `UPDATE`, `MERGE INTO`, `COPY … FROM` or `CREATE TABLE <t> AS` in the body, directly or in literal `EXECUTE` text with a literal table name". (2) "'None' applies only where no written table can be read"; the FIXTURE-ID "any other statement" row's "otherwise none" now reads "only where no written table can be read", and the old "body text that is not a value of an `INSERT` or `UPDATE`" phrase is gone. The SG9-01 overlap is closed. (3) Contract `correctiveMigration` matches. (4) Unit row "Corrective migration", **SG10-02**: a `DO`-body `CREATE TABLE t AS VALUES (…)` → `t`; a FIXTURE-ID in a `DO`-body `MERGE INTO t` → `t`; `EXECUTE 'INSERT INTO t (c) VALUES (…)'` → `t`; "in each case C without a write on `t` is not accepted"; `format('INSERT INTO %I …')` → none. |
| SG10-03 Stale or incomplete text after run 9 | Low | **Resolved.** | (1) Known-files row: "with a literal format string and only `%I` placeholders (SPEC-TE011-008 class 3); a `%L` for a check-constraint value would be a finding". The same limit is in the SPEC-TE011-017 orders 1–5 row and in the ASM-TE011-27 risk column. (2) Contract `fixtureMatching`: "any statement in a DO, function or procedure body that the class-3 rules do not list". (3) Class 3: "A `%I` specifier, in any positional, width or flag form … is read as a name"; "Every other specifier (`%s`, `%L`), in any positional, width or flag form (for example `%1$s`, `%2$L`, `%-10s`), gives the finding"; "`%%` is a literal percent sign". Unit: `%1$I … %2$L` → finding; `''A%%''` → none. ASM-TE011-27, the contract and §3b item 1 match. (4) TS-TE011-09 (e): "exit 1 from the uncorrected O (the absence of a git call is checked in the unit row)". (5) ASM-TE011-29 risk: "where the list is built … Where it is not built, condition (e) is skipped on purpose, and the `PDPA-SCOPE: changed-file list not built` line says so". (6) Unit Output row: "paths, branch names and counts only"; SPEC-TE011-012 notes that the changed-file lines "also carry branch names". |

**Regression check, rounds 7–9.**

| Earlier finding | Still resolved | Check |
|---|---|---|
| SG7-01 | Yes | Lint-fixture class untouched by run 10. SPEC-TE011-018 scope is still limited to the migration folder. |
| SG7-02 | Yes | Class-2 `DEFAULT` position and the `DO`-body rules are intact. |
| SG7-03 | Yes | Target-table table, scope sentence, changed-file list and `rwb.flyway.location` are all present. |
| SG7-04 | Yes | Counts and the R4 owner are unchanged. |
| SG8-01 | Yes | (d) still says "(a) to (c) and (e) still apply", and (e) "applies to every finding, with or without a target table". |
| SG8-02 | Yes | The FIXTURE-ID `DEFAULT` row is kept. The "any other statement" row still names the `COPY` data block, `MERGE INTO`, `SELECT … INTO` and `CREATE TABLE … AS`. `SELECT … INTO <t>` is now qualified "top-level", which is correct: in a body it assigns a variable. |
| SG8-03 | Yes | The body catch-all is intact. |
| SG8-04 | Yes | The list is built in branch pipelines with `GIT_DEPTH: 0`, and no merge base gives exit 2. The premise "no merge request pipeline", which review 8 itself stated, is corrected as new finding SG11-02. The SG8-04 fix itself still holds. |
| SG8-05 | Yes | The E1-044 Flyway-fixture reading, "nothing asked of RWB-E1-044" and the test-root bound on lint-fixture roots are unchanged. |
| SG8-06 | Yes | TS-TE011-06 (i) still passes `--branch <feature branch>`. |
| SG9-01 to SG9-04 | Yes | See the SG10-02 and SG10-03 rows above. The status row and T10 wording are kept. |

Spot checks on earlier rounds: 9 Restricted fields; 18 fields; 14 of 18; `infra/postgres/schema/**`;
(object, field) matching; no allow entry on a migration. The coverage table still reads `TOTAL_RULES: 32`
and `CONTRADICTIONS: 0`.

**The orchestrator's three SG9-03 tests, re-assessed.**

| Test | Met? | Evidence |
|---|---|---|
| (1) A promotion never fails for lack of a changed-file list | **Met.** | Tag pipelines pass no option (T15, TS-TE011-09 (l)). Branch pipelines on `main` and `develop` build no list, and their fetch is non-fatal. A promotion merge request targets another branch (TS-TE011-09 (h), (i), (j)). SG11-02 does not change this. Any merge request pipeline that GitLab creates holds no `pdpa-lint` job. |
| (2) The rules that need the list run only where it is defined | **Met.** | SPEC-TE011-018 (e) is evaluated only where the list is built (T11, contract). |
| (3) The behaviour on every other target is stated and tested | **Met**, with the text gaps of SG11-03 item 1. | A tag pipeline or no option: T15, TS-TE011-09 (l), unit row. A detached `HEAD` or empty branch: T14, TS-TE011-09 (k), unit row. |

## 3. New findings

### REVIEW-TE011-SG11-01: A `DEFAULT` written through `EXECUTE` text on a literal table has no stated target table (Low)

- **Affects:** SPEC-TE011-018 (d), the lead sentence and the `(DML in procedural body)` row of the
  target-table table; the FIXTURE-ID `INSERT`/`UPDATE` row; contract `correctiveMigration`; unit row
  "Corrective migration".
- **Evidence:**
  1. **Run 10 added a general rule.** "'None' applies only where no written table can be read", and the
     readable-table rules apply "inside literal `EXECUTE` text or a `format` string whose table is
     literal".
  2. **Class 2 says a `DEFAULT` writes rows.** `ALTER TABLE … ADD COLUMN … DEFAULT` "writes the value
     into every existing row".
  3. **Class 3 gives such a `DEFAULT` a finding.** A `%s` or `%L` specifier gives the finding. So does
     "A `DEFAULT` clause whose table or column is a placeholder". In both cases the finding is
     `(DML in procedural body)`.
  4. **The table row is still a closed list.** The `(DML in procedural body)` row gives "the table of an
     `INSERT`, `UPDATE`, `MERGE INTO`, `COPY … FROM` or `CREATE TABLE <t> AS`". It does not list
     `ALTER TABLE <t> ADD COLUMN … DEFAULT` or `SET DEFAULT`. The contract has the same list.
  5. **Two cases that fall between the rules.** Take a migration O whose `DO` body runs one of these:
     - `EXECUTE format('ALTER TABLE case_note ADD COLUMN note text DEFAULT %L', v)`
     - `EXECUTE format('ALTER TABLE case_note ADD COLUMN %I text DEFAULT ''<text>''', c)`

     Each is a finding, and the value reaches every row of `case_note`. By the row, the target is
     "None", so a corrective C needs no write on `case_note`. By the lead sentence, `case_note` is a
     written table that can be read, so C needs a write on it.
  6. **The `DEFAULT` clause of (d) is undefined here.** (d) asks for `ALTER COLUMN … DROP|SET DEFAULT`
     "for a finding in a `DEFAULT`". The spec does not say whether that covers a
     `(DML in procedural body)` finding caused by a `DEFAULT`. In the second case the column is a
     placeholder, so there is no `<c>` to match. This is the SG8-02, SG9-01 and SG10-02 principle again:
     a value that reaches rows needs a data change.
  7. **The wording does not match.** The lead sentence says "literal `EXECUTE` text or a `format`
     string whose table is literal". The `(DML in procedural body)` row, the FIXTURE-ID
     `INSERT`/`UPDATE` row and the contract say only "literal `EXECUTE` text". Class 3 treats both as one
     case, but the rows do not say so. The unit row tests `format('INSERT INTO %I …')` → none. It does
     not test `format('INSERT INTO t (c) VALUES (%L)', v)` → `t`.
  8. **No test** covers either `DEFAULT` case or the `format` case with a literal table.
- **Required fix:**
  1. Add to the `(DML in procedural body)` target set the table of an `ALTER TABLE <t> ADD COLUMN …
     DEFAULT` or `ALTER COLUMN … SET DEFAULT` whose table is literal, in `EXECUTE` or `format` text where
     the `DEFAULT` gives the finding.
  2. State what C needs in that case:
     - a write on `t`;
     - where the column is literal, also `ALTER COLUMN <c> DROP|SET DEFAULT`;
     - where the column is a placeholder, the write on `t` only. Code owners check the rest (the
       "Limit" bullet).
  3. Use one phrase in the lead sentence, both rows and the contract, for example "literal `EXECUTE`
     text, including a `format` call with a literal format string".
  4. Add unit scenarios:
     - `format('ALTER TABLE t ADD COLUMN c text DEFAULT %L', v)` → `t`, plus `DROP DEFAULT` on `c`;
     - `format('ALTER TABLE t ADD COLUMN %I text DEFAULT ''<text>''', c)` → `t`;
     - `format('INSERT INTO t (c) VALUES (%L)', v)` → `t`;
     - in each case, C without the required write is not accepted.

### REVIEW-TE011-SG11-02: GitLab does create merge request pipelines for this file, and `pdpa-lint` is not in them (Low)

- **Affects:** trigger note under "Entry trigger and preconditions"; SPEC-TE011-013 (first bullet,
  "GitLab" bullets); ASM-TE011-29; CLAR-015; contract `trigger` and `inputs` "Changed-file list".
- **Evidence:**
  1. **The spec says no merge request pipeline is created.** The trigger note says "GitLab creates
     branch pipelines and tag pipelines, and no merge request pipeline". SPEC-TE011-013 says "It creates
     no merge request pipeline (review SG8-04, SG10-01)" and describes a merge request pipeline only
     "where a later change to `.gitlab-ci.yml` adds one". ASM-TE011-29 says "`.gitlab-ci.yml` creates
     branch and tag pipelines only". The contract `trigger` says the same.
  2. **The file shows otherwise.** `backend-recovery-it` has `rules:` whose first entry is
     `- changes:` (`backend/src/main/resources/db/**/*`, `…/RecoveryFlywayConfig.java`,
     `infra/postgres/**/*`) with no `if:`. A rule with no `if:` is not limited to a pipeline source. For
     a `merge_request_event` it compares the merge request's changes with its target. So when a merge
     request changes the migration folder, GitLab adds this job and creates a merge request pipeline. This
     is the "duplicate pipelines" case in GitLab's documentation.
  3. **`pdpa-lint` is not in that pipeline.** The spec gives `pdpa-lint` "no `rules:` filter", so its
     default is `only: [branches, tags]`, like `backend-unit` and `frontend-check`. The merge request
     pipeline therefore holds `backend-recovery-it` only. Note that the merge requests that touch the
     migration folder are the very ones condition (e) exists for.
  4. **Effect.** In the branch pipeline of the source branch, `pdpa-lint` still runs and builds the list,
     so the lint's own behaviour is right. But when both pipelines exist for one commit, GitLab normally
     shows the later merge request pipeline on the merge request and uses it for the "Pipelines must
     succeed" check. So the `pdpa-lint` result may not be the one that gates the merge.
  5. **Materiality.** No GitLab pipeline runs in this repository (D-RUN-06), and in ACE the check runs in
     the ACE pipeline (D-RCV-50), so the effect here is limited. The finding is about an incorrect
     statement in the spec and a gap in the GitLab path it specifies.
- **Required fix:**
  1. Correct the statement in all five places: GitLab creates branch and tag pipelines. It also creates
     a merge request pipeline when a merge request changes a path in `backend-recovery-it`'s
     `rules: changes:`.
  2. Choose one of these and state it:
     - **(a) Recommended.** Give `pdpa-lint` `rules:` that keep it in branch and tag pipelines and also add
       it to `merge_request_event` pipelines. There it uses the merge request command that SPEC-TE011-013
       already specifies: non-fatal fetch, `origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME`,
       `--branch "$CI_MERGE_REQUEST_SOURCE_BRANCH_NAME"`.
     - **(b)** Keep the job without `rules:`. State that it does not run in such a merge request pipeline.
       Record the merge-check limit as a residual risk in ASM-TE011-29, with the local merge gate
       (D-RUN-06) and the ACE pipeline (D-RCV-50) as the controls.
  3. Under (a), add a unit or configuration check that the job runs for each of the three pipeline
     sources with the right options.

### REVIEW-TE011-SG11-03: Text not aligned after run 10 (Low)

- **Affects:** SPEC-TE011-018 (e); SPEC-TE011-013 "Not built" bullet and "Branch pipeline" bullet.
- **Evidence:**
  1. **SPEC-TE011-018 (e) leaves out the no-option case.** It reads: "Where the list is not built (on the
     target branch itself, on `main` or `develop`, or in a merge request into another target), (e) is not
     evaluated". SPEC-TE011-013, T15, the unit row and the contract also give "a run without
     `--changed-files-from-git`, as in a GitLab tag pipeline". The (e) list reads as complete, and the
     focus of this round is the agreement between SPEC-TE011-013 and -018 (e).
  2. **"Such a run carries only files that met (e)" is now too broad.** SPEC-TE011-013 and -018 (e) both
     make this claim. Run 10 put the no-option run, "as in a GitLab tag pipeline", among the runs it
     covers. A tag can be pushed on any commit, including an unmerged commit on a story branch. A manual
     run without the option can check any tree. For those runs the claim is not true.
     No merge gate depends on it: the story branch's own pipeline and the local merge build the list. The
     text still needs to say where the claim holds.
  3. **A failed fetch does not always leave the target unresolved.** SPEC-TE011-013 says: "Where it builds
     the list and the fetch failed, the target cannot be resolved and the run gives exit 2 (T14)". The job
     sets `GIT_DEPTH: 0` but not `GIT_STRATEGY`. GitLab's default `fetch` strategy can reuse the runner's
     working copy. A `refs/remotes/origin/develop-recovery` ref left there by an earlier job (for example
     this job's own fetch in an earlier pipeline) survives a failed fetch. The ref then resolves to an old
     commit, and the list is built from an older merge base. A migration O that was merged into
     `develop-recovery` after that commit appears as added. A valid corrective C is then refused (a false
     exit 1). The outcome fails closed, but it differs from the stated behaviour, and the false failure is
     the kind that SG9-03 and SG10-01 set out to remove.
- **Required fix:**
  1. Add "a run without the option (for example a GitLab tag pipeline)" to the not-built list in
     SPEC-TE011-018 (e).
  2. Limit the "carries only files that met (e)" sentence in SPEC-TE011-013 and -018 (e) to runs on
     commits already merged into `changedFiles.targetBranch`, such as promotions and release tags. State
     that a no-option run on any other commit is not a merge gate.
  3. Make the claim true. Before the non-fatal fetch, the job deletes `refs/remotes/origin/<targetBranch>`
     (or fetches into a dedicated ref that it passes as `<target>`, or sets `GIT_STRATEGY: clone`). A
     failed fetch then leaves the target unresolved, and the run gives exit 2 where the list is built.
     State the chosen form in SPEC-TE011-013 and ASM-TE011-29.

## 4. Other checks

| Check | Result |
|---|---|
| Personal data in the artefacts | None found. No e-mail address and no run of 9 or more digits in `specify/` outside the `*.run*` backups (counts only printed: 0 and 0). Only synthetic values and placeholders are used (`SYN-…`, `<text>`, `<id>`, `V0003__rwb_e1_042_seed.sql`, `V0004__rwb_e1_042_seed2.sql`, `feature/x`, `case_note`). |
| Secrets | None. |
| Contracts | Both parse as JSON. The renamed key `changedFileBranchUndeterminedLine` matches SPEC-TE011-013 and T14. The exit-2 text matches SPEC-TE011-012 and the status matrix. `fixtureMatching` matches class 3 after run 10. `correctiveMigration` carries the SG11-01 gap. `trigger` carries SG11-02. `NO_API_CHANGE` is consistent. |
| Class 3 and SPEC-TE011-018 (focus 3) | Consistent apart from SG11-01. The `%I` rule ("read as a name") and the -018 phrase "a table given by a placeholder → none" agree. A `%s`/`%L` finding with no readable written table (for example a check-constraint value) has no target table, which is consistent. TS-TE011-07 and the unit rows agree with class 3 (`%1$I … %2$L`, `%%`, `format('ALTER TABLE t %s', v)`). §3b item 1 and ASM-TE011-27 agree. |
| SPEC-TE011-013 and the exception tables (focus 3) | T14 (`branch not determined`), T15 (no option, tag pipeline), the status matrix, SPEC-TE011-012, TS-TE011-09 (e), (k), (l), the unit row, ASM-TE011-29, CLAR-015 and the contract agree on the decision rules. The remaining issues are the pipeline premise (SG11-02) and the text items in SG11-03. "Before any other check" for an undetermined branch is consistent with "decides first, before any git command". |
| Authorization and audit | Unchanged and appropriate for a build tool. `changedFiles.targetBranch` and `changedFiles.protectedBranches` are configuration under the code-owner entry (SPEC-TE011-014, -015). Running `git` reads repository metadata only: no database and no network (story §13, §17). |
| Unit Test Applicability | Compliant. The front end is `NOT_APPLICABLE` with evidence. The tool back end is `REQUIRED` at 80% on JaCoCo LINE, BRANCH, METHOD and INSTRUCTION, with coverage verification in the job. SG11-01 and SG11-02 would add scenarios. |
| Evidence | No new script. The new claims rest on repository files, which the reviewer read directly: `.gitlab-ci.yml` (all four parts), `scripts/dev.ps1`, `.git/HEAD` and the migration folder. |
| Cross-story versions | RWB-E1-042 is now revision 12. Its §12.3 is identical to its `spec.run9.md` copy: step 3 still lists check constraints with value lists, so the "only `%I`" limit and §3b ("a check-constraint value is written literally") matter. RWB-E1-043 is now revision 8. It keeps the RWB-E1-064 forward note and R4 (owner RW-COMPLY, in its `shared-updates.md`), and says RWB-TE-011 "is asked for nothing by this story (GAP-38)". E1-044, TE-001, TE-002, TE-003 and E1-001 are unchanged since round 10. |
| Run decisions | D-RUN-06: the local merge gate runs `dev.ps1 test` on the story branch, where the list is built. A detached checkout now fails closed with exit 2. D-RUN-07: no number is fixed. D-RUN-08: no dependency on a later story, and nothing is asked of RWB-E1-044. D-RUN-09 applied: the triage is attributed to the orchestrator (Claude Code), and no human disposition is claimed. `agent-run-log.md` states "No further specifier round is allowed after round 11". The round-10 observation stands: the build log row carries 2026-11-18T05:31:18, while the specification, `gate-response.md` and `agent-run-log.md` cite 05:13. Reconciling it is for the orchestrator. |
| Data classification (pdlc stop condition) | The classification source, the residual risk, both RWB-E1-001 outcomes and the load-route limit are visible and unchanged. R4 (RW-COMPLY) is consistent with RWB-E1-043 revision 8. No open data-classification blocker belongs to this story. |
| Document gaps | No new document gap. The findings concern this specification and the repository's CI file, not the document set. `review/document-gaps-11.md` is not written. |

## 5. Gate output

```text
REVIEW_STATUS: FAIL
REVIEW_COUNTS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 3]
ROUND_10_DISPOSITION: SG10-01 Resolved (tag pipelines named; tag pipeline passes no option and fetches nothing; branch pipeline non-fatal fetch with $CI_COMMIT_BRANCH; --branch missing/empty/HEAD gives exit 2 "branch not determined"; T14, T15, TS-09 (k), (l), unit row, ASM-29, CLAR-015, contract aligned); pipeline premise in SG11-02, fetch and claim wording in SG11-03. SG10-02 Resolved as written (readable-table rules in bodies and literal EXECUTE text; DML-in-body set takes CREATE TABLE AS and EXECUTE writes; "None" only where no written table can be read; unit scenarios); DEFAULT-through-EXECUTE case and format wording in SG11-01. SG10-03 Resolved (only-%I limit in known-files row, SPEC-017 row, ASM-27; contract phrase; all specifier forms and %%; TS-09 (e) exit 1; ASM-29 risk; Output unit row)
ROUND_7_9_DISPOSITION: all remain Resolved; no regression. SG8-04 fix holds; its premise "no merge request pipeline" is corrected in SG11-02
SG9-03_TRIAGE_TESTS: (1) promotion never fails for lack of a list: met; (2) list-dependent rules only where defined: met; (3) every other target stated and tested: met, with SG11-03 item 1 text gap
NEW_FINDINGS: SG11-01 Low (DML-in-body target list omits ADD COLUMN ... DEFAULT / SET DEFAULT on a literal table in EXECUTE or format text, though class 2 says it writes every row and -018 now says "None" only where no written table can be read; (d) DEFAULT clause undefined for a placeholder column; "literal EXECUTE text" vs "format string" wording; no tests); SG11-02 Low (backend-recovery-it rules: changes with no if makes GitLab create merge request pipelines for MRs touching the migration folder; pdpa-lint with no rules is not in them; "no merge request pipeline" stated in trigger note, SPEC-013, ASM-29, CLAR-015, contract); SG11-03 Low (SPEC-018 (e) not-built list omits no-option/tag case; "carries only files that met (e)" too broad for tag/no-option runs; a failed non-fatal fetch can leave a stale origin/<target> on a reused working copy, so the target resolves and a valid corrective is refused)
NEW_DOCUMENT_GAPS: none
CROSS_STORY_RWB-E1-044: Consistent with v14-7; nothing asked of it
CROSS_STORY_RWB-E1-042: Revision 12; section 12.3 unchanged; step-3 value-list checks keep the only-%I limit material
CROSS_STORY_RWB-E1-043: Revision 8 keeps R4 (RW-COMPLY) and the RWB-E1-064 forward note; nothing asked of TE-011
CROSS_STORY_RWB-E1-001: Consistent; unchanged since round 10
CROSS_STORY_RWB-TE-001/-002/-003: Consistent; unchanged since round 10
BLOCKING: YES under D-RUN-09 (Low-only failure is not accepted by the orchestrator; REVIEW_GATE_WARNING would otherwise apply)
NEXT_STEP: The orchestrator (Claude Code) triages SG11-01..SG11-03. Its round-9 triage allowed no specifier round after this one, so under D-RUN-09 the orchestrator either directs a further remediation run or refers the Low findings to the engagement lead for a human disposition, recorded with name and time. This review records no disposition and does not start the Implementation Planner.
```

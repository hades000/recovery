# Spec gate review, round 10: RWB-TE-011 PDPA lint for code, tests and logs

| Field | Value |
|---|---|
| RUN_ID | `INC-006-epic-1-RWB-TE-011` |
| Gate | Spec gate, re-review round 10 (Compliance Reviewer, independent of the author) |
| Earlier rounds | Round 1 `review/spec-gate-review.md` (FAIL, 2 Medium, 5 Low); round 2 `-2.md` (FAIL, 1 Medium, 1 Low); round 3 `-3.md` (FAIL, 2 Low); round 4 `-4.md` (FAIL, 3 Medium, 1 Low) with `document-gaps-4.md`; round 5 `-5.md` (FAIL, 1 Medium, 3 Low) with `document-gaps-5.md`; round 6 `-6.md` (FAIL, 4 Low); round 7 `-7.md` (FAIL, 1 Medium, 3 Low); round 8 `-8.md` (FAIL, 6 Low); round 9 `-9.md` (FAIL, 4 Low: SG9-01..SG9-04) |
| Reviewed | `specify/spec.md` (SPEC-TE011-001..018, revised 18 Nov 2026 after round 9), `assumptions.md` (ASM-TE011-01..29), `document-gaps.md` (DGL-01..15, unchanged since run 7), `shared-updates.md` (§1–§5, including §3b), `gate-response.md` ("Gate response — round 9" and its self-check note), `compliance-validation.md`, `agent-run-log.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `evidence/`; the `*.run9.*` copies, compared with `diff --strip-trailing-cr` |
| Direction checked | The round-9 triage came from the orchestrator (Claude Code), logged at 2026-11-18T05:13 per the specification and `agent-run-log.md`. It is an agent's direction, not a human decision. For SG9-03 it set three tests: (1) a promotion of `develop-recovery` towards `main` never fails for lack of a changed-file list; (2) the corrective-migration rules that need the list run only where the list is defined; (3) the behaviour on every other target is stated and tested. D-RUN-06, -07, -08, -09 (`AI-SDLC-BUILD-LOG.md` §1). Under D-RUN-09 Low findings are fixed, not accepted |
| Cross-story input (read only) | RWB-E1-044 spec v14-7 (`INC-001`: SPEC-RWB-E1-044-010, -011; T-044-10..22; fixture rule "synthetic table and column names … (RUN-BRIEF rule 7)"); RWB-E1-042 spec revision 10 (`INC-003`, §12.3, identical to revision 9); RWB-TE-001 v4 (`INC-002`); RWB-TE-002 (`INC-004`); RWB-TE-003 (`INC-005`); RWB-E1-043 (`INC-008`, now revision 7; open item R4 and the RWB-E1-064 forward note unchanged); RWB-E1-001 (`INC-009`); RWB-E1-064 story file v1 (DF-REF-105 `is_personal` Read); `AGENTS.md` §3.7, §4.6; decision register D-RCV-28, D-RCV-50 (full text read in `INC-001-decisions.md`), L-RCV-13 |
| Checked against | `.gitlab-ci.yml` (no `workflow:` block; `backend-unit` and `frontend-check` have no `rules:` or `only:`; header comment "the ACE pipeline on the develop-recovery MR"); `backend/src/main/resources/application.yaml` (`rwb.flyway.location`); `scripts/dev.ps1` (`ValidateSet` has no `pdpa-lint` yet; `test` runs Gradle `test`); today's tree (migration folder holds `README.md` only; `.git/HEAD` is `refs/heads/develop-recovery`, the only local branch; git was not run) |
| Method | Diff of every changed file against its `run9` copy (152 changed lines in `spec.md`, all inside SPEC-TE011-003, -008, -012, -013, -015, -017, -018, the status and exception tables, the test tables and CLAR-015), then a full read of SPEC-TE011-008 class 3, -012, -013, -015, -017, -018, the status-transition and exception tables and the test tables. Each new claim was checked against the repository file or the other story's specification it relies on. Greps of `specify/` (backups excluded) for e-mail addresses and runs of 9 or more digits printed counts only. Both contracts parsed as JSON |
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

**Round 9.** SG9-01 to SG9-04 are resolved. Each was checked against `spec.md` and the other artefacts,
not against `gate-response.md` alone. No finding from rounds 1–8 has reopened.

Three new Low findings remain. All three are in text that run 9 added or changed, or in text that run 9's
changes made stale. Under D-RUN-09 Low findings are fixed, not accepted, so the gate fails.

- **SG10-01.** The changed-file decision misses GitLab tag pipelines, and the job's unconditional fetch
  runs before the tool decides. The first of the orchestrator's three SG9-03 tests is not fully met.
- **SG10-02.** Target tables inside procedural bodies are still split between rows for a class-4
  `CREATE TABLE … AS`, a body `MERGE INTO`, and DML inside literal `EXECUTE` text.
- **SG10-03.** Stale or incomplete text after run 9 (the `%s`/`%L` rule not carried into three
  places, the contract wording, positional placeholders, TS-TE011-09 (e), ASM-TE011-29, the `PDPA-SCOPE`
  unit row).

## 2. Disposition of round-9 findings

| Finding | Severity | Disposition | Evidence (checked against the spec, not against `gate-response.md` alone) |
|---|---|---|---|
| SG9-01 FIXTURE-ID in a body `INSERT`/`UPDATE` fits two target-table rows | Low | **Resolved.** Residual overlaps for other body statements are raised as SG10-02. | SPEC-TE011-018 table: "FIXTURE-ID in a value of an `INSERT` or `UPDATE`, wherever the statement is: top level, or in a `DO`, function or procedure body … That statement's table". The "otherwise none" list now names only "body text that is not a value of an `INSERT` or `UPDATE`". The `(DML in procedural body)` row gives "Each table that an `INSERT`, `UPDATE`, `MERGE INTO` or `COPY … FROM` in the body names". Contract `correctiveMigration` and ASM-TE011-26 match. Unit row "Corrective migration": `DO`-body `INSERT INTO t` → `t`, C without a write on `t` not accepted; function-body equivalent; `CALL p()`-only block → none. |
| SG9-02 Class-3 `EXECUTE` placeholders, literal `DEFAULT`, class-2 list vs catch-all | Low | **Resolved.** Residual text items are raised in SG10-03 (items 1 and 3). | Class 3 `EXECUTE` rules: "A `%I` placeholder (also the positional form `%1$I`) is read as a name"; "A `%s` or `%L` placeholder gives the finding, except as the comment text of `COMMENT ON … IS`"; a `DEFAULT` on a placeholder table or column gives the finding; "A literal `DEFAULT` with a literal table and column is checked as a class-2 `DEFAULT` position". The direct-statement bullet now lists the whole class-2 list, including transaction control, `LOCK` and `COPY … TO`. The catch-all and the function-body paragraph name `COPY … FROM`. ASM-TE011-27, contract `fixtureMatching` and §3b item 1 match. Unit and TS-TE011-07 scenarios added (`format('ALTER TABLE t %s', v)`, `%I`-pair `DEFAULT`, literal `DEFAULT` on a personal pair and with `SYN-`, `COMMENT ON … IS %L`, `COPY t TO STDOUT`, `LOCK`, `COMMIT`, `COPY t FROM stdin`). |
| SG9-03 Changed-file list built for downstream branches and promotion MRs | Low | **Resolved** as far as the review-9 fix reached. Tag pipelines and the job's fetch step are raised as SG10-01. | SPEC-TE011-013: `ChangedFileList` takes `--branch` and "decides first, before any git command". "Built" only when the target without `origin/` equals `changedFiles.targetBranch` and the branch is neither that branch nor in `changedFiles.protectedBranches` (default `main`, `develop`; L-RCV-13). "Not built" otherwise: no git command, (e) not evaluated, `PDPA-SCOPE: changed-file list not built …`. `--changed-files-from-git` without `--branch` → exit 2. SPEC-TE011-018 (e), T11, T14, new T15, SPEC-TE011-012, -015, ASM-TE011-26, -29, the contract and CLAR-015 agree. TS-TE011-09 (h) (squashed promotion on `develop` → exit 0 with the `corrected by` notice), (i), (j), (k), and the unit decision row. |
| SG9-04 Stale and over-cited text | Low | **Resolved.** One residual phrase in the contract is raised in SG10-03 item 2. | (1) Status-transition exit-2 row lists "a lint-fixture root that covers it or lies outside the test roots" and "has no merge base with HEAD (where the list is built), or a changed-file option without `--branch`". (2) T10 and the `compliance-validation.md` row read "any statement in a `DO`, function or procedure body that the class-3 rules do not list"; so does the SPEC-TE011-017 orders 1–5 row. (3) SPEC-TE011-003 now cites RUN-BRIEF rule 7 and T-044-18 ("a synthetic table"), and states that SPEC-RWB-E1-044-010 covers the lint fixtures only. The reviewer confirmed E1-044 v14-7: "Fixtures use synthetic table and column names and no personal data (RUN-BRIEF rule 7)". |

**Regression check, rounds 1–8.** The run-9 diff touches only the sections listed in the header; no
earlier finding has reopened. Spot checks: 9 Restricted fields; 18 fields; 14 of 18; 509 / 526 / 390 / 71;
`infra/postgres/schema/**`; (object, field) matching; no allow entry on a migration; the lint-fixture class
and its bound; nothing asked of RWB-E1-044; `rwb.flyway.location`. The coverage table still has
`TOTAL_RULES: 32`.

**The orchestrator's three SG9-03 tests.**

| Test | Met? | Evidence |
|---|---|---|
| (1) A promotion never fails for lack of a changed-file list | **Partly.** Met for `develop` and `main` branch pipelines and for a promotion merge request (T15, TS-TE011-09 (h), (i), (j)). Not met for a tag pipeline on a promoted commit, and the job's unconditional fetch can fail a `main` or `develop` pipeline before the tool decides (SG10-01). | SPEC-TE011-013 "GitLab" bullet; `.gitlab-ci.yml` has no `workflow:` and no job-level `rules:` or `only:` |
| (2) The rules that need the list run only where it is defined | **Met.** Only condition (e) needs the list; SPEC-TE011-018 (e) is "evaluated only where the list is built", and conditions (a) to (d) do not read it. T11 and the contract agree. | SPEC-TE011-018 (e); T11; contract `correctiveMigration` |
| (3) The behaviour on every other target is stated and tested | **Partly.** Stated and tested for a non-target target, the target branch, the protected branches, a missing option and a missing `--branch`. Not stated for a tag pipeline or a detached `HEAD` in the local path (SG10-01). | T14, T15; unit row "Changed-file list"; TS-TE011-09 (e), (h)–(k) |

## 3. New findings

### REVIEW-TE011-SG10-01: Tag pipelines build the changed-file list, and the job's fetch runs before the tool decides (Low)

- **Affects:** SPEC-TE011-013 (first bullet and the "GitLab" and "Local merge" bullets); T15;
  ASM-TE011-29; contract `inputs` "Changed-file list"; CLAR-015; TS-TE011-09; unit row "Changed-file list".
- **Evidence:**
  1. **Tag pipelines exist.** SPEC-TE011-013 says "GitLab creates branch (push) pipelines only". The job
     has "no `rules:` filter", and `.gitlab-ci.yml` has no `workflow:` block. GitLab creates a pipeline
     both when a branch is pushed and when a tag is pushed. A job with no `rules:` or `only:` runs in both.
  2. **A tag pipeline builds the list.** In a tag pipeline `$CI_COMMIT_REF_NAME` is the tag name. A tag
     name is neither `changedFiles.targetBranch` nor in `changedFiles.protectedBranches`. So the job's
     `--changed-files-from-git origin/develop-recovery --branch "$CI_COMMIT_REF_NAME"` builds the list.
  3. **The failure case.** Tag a release on `main` after a squash promotion that carried O and C. The
     squash commit is not in the history of `develop-recovery`, so the merge base is older than O. The
     tree diff from the merge base lists O and C as added. Condition (e) fails, and O's finding fails the
     tag pipeline. O is merged and cannot be edited, and nothing else excuses it (SPEC-TE011-018). This is
     the SG9-03 failure on the release path, and it contradicts "promoting `develop-recovery` never fails
     for lack of a changed-file list".
  4. **The fetch runs before the tool decides.** The job "in every pipeline … fetches
     `changedFiles.targetBranch`" before it runs the tool. On `main` or `develop`, where the tool builds no
     list, a failed fetch (for example a mirror without `develop-recovery`, or a renamed target) fails the
     job. TS-TE011-09 (j) proves only that the tool itself gives no exit 2 in such a clone.
  5. **Detached `HEAD` locally.** `dev.ps1` takes the branch from `git rev-parse --abbrev-ref HEAD`. On a
     detached checkout this prints `HEAD`, which is neither the target nor protected, so the list is
     built. The spec does not say whether that is intended.
  6. **No test** covers a tag pipeline or a detached `HEAD`.
- **Required fix:**
  1. Correct the first bullet of SPEC-TE011-013: GitLab also creates tag pipelines.
  2. In a tag pipeline (`$CI_COMMIT_TAG` set), pass no changed-file option, so the list is not built.
     Pass the option only in a branch pipeline (`$CI_COMMIT_BRANCH`) or a merge request pipeline. Add tag
     pipelines to T15.
  3. Fetch the target branch only when the list will be built. Otherwise make the fetch non-fatal: where
     the list is built, the tool already gives exit 2 if the target is missing.
  4. State the detached-`HEAD` case in the local path. Recommended: `--branch HEAD` gives exit 2,
     `changed-file list: branch not determined`, because the local merge gate always runs on a named
     branch.
  5. Align ASM-TE011-29, the contract and CLAR-015.
  6. Add a TS-TE011-09 case: the squashed-promotion tree of (h), run as a tag pipeline would run it, gives
     exit 0 with the `corrected by` notice and the "not built" line. Add a unit scenario for `--branch HEAD`.

### REVIEW-TE011-SG10-02: Target tables inside procedural bodies are still split between rows (Low)

- **Affects:** SPEC-TE011-018 (d), the target-table table; contract `correctiveMigration`; unit row
  "Corrective migration".
- **Evidence:**
  1. **A class-4 `CREATE TABLE … AS` in a body.**
     - The row "FIXTURE-FIELD `(statement not recognised)`" gives `<t>` for a top-level
       `CREATE TABLE <t> AS`.
     - The row "FIXTURE-FIELD `(DML in procedural body)`" gives "None when the body names no such table
       (for example … a class-4 statement)".
     - So `DO $$ BEGIN CREATE TABLE t AS VALUES ('<text>'); END $$` needs no data change in C, although
       the value reaches rows of `t` exactly as at top level. The same holds for
       `EXECUTE 'CREATE TABLE t AS VALUES (…)'`. The SG8-02 and SG9-01 principle is that a value which
       reaches rows needs a data change.
  2. **FIXTURE-ID in a body `MERGE INTO t` (or `CREATE TABLE t AS`).** The row "FIXTURE-ID in any other
     statement" gives "`MERGE INTO <t>` … `CREATE TABLE <t> AS`" → that table. The same row's "otherwise
     none" list names "body text that is not a value of an `INSERT` or `UPDATE`", which a body `MERGE` or
     `CREATE TABLE … AS` also is. The contract lists "body text that is not an INSERT or UPDATE value"
     plainly among the findings with no target table. This is the same kind of overlap as SG9-01.
  3. **DML inside literal `EXECUTE` text.** Take `EXECUTE 'INSERT INTO t (c) VALUES (''<text>'')'`. The
     spec can read its table, because class 3 classes literal `EXECUTE` text "as it would class a
     top-level statement". The spec does not say whether that `INSERT` is "in the body" for the
     `(DML in procedural body)` row, or "a value of an `INSERT`" for the FIXTURE-ID row. The unit row
     tests the finding for `DO` with `EXECUTE 'INSERT …'`, but not its target table.
  4. **No test** covers any of the three cases.
- **Required fix:**
  1. State that the readable-table rules apply inside bodies and inside literal `EXECUTE` text, as at
     top level. The `(DML in procedural body)` target set also takes the table of a class-4
     `CREATE TABLE <t> AS`, and of an `INSERT`, `UPDATE`, `MERGE INTO`, `COPY … FROM` or
     `CREATE TABLE <t> AS` in literal `EXECUTE` text whose table is literal.
  2. Limit "None" and "body text that is not a value of an `INSERT` or `UPDATE`" to text from which no
     table can be read.
  3. Align the contract.
  4. Add unit scenarios:
     - a `DO`-body `CREATE TABLE t AS VALUES (…)` → `t`;
     - a FIXTURE-ID in a `DO`-body `MERGE INTO t` → `t`;
     - `EXECUTE 'INSERT INTO t (c) VALUES (…)'` → `t`;
     - in each case, C without a write on `t` is not accepted.

### REVIEW-TE011-SG10-03: Stale or incomplete text after run 9 (Low)

- **Affects:** SPEC-TE011-008 "Known files" row for order 3 and the class-3 `EXECUTE` rules;
  SPEC-TE011-017 row for orders 1–5; ASM-TE011-27 (risk column), ASM-TE011-29 (risk column); contract
  `fixtureMatching`; TS-TE011-09 (e); unit row "Output (-012)".
- **Evidence:**
  1. **The `%s`/`%L` rule is missing in three places.** Run 9 made a `%s` or `%L` placeholder a finding
     everywhere except as `COMMENT ON … IS` text, and §3b item 1 now tells the planners "In `format`, use
     only `%I` placeholders". Three places still say that a step-3 guard raises nothing "through `EXECUTE
     format('ALTER TABLE …', …)` with a literal format string", with no placeholder limit:
     - the "Known files" row for RWB-E1-042;
     - the SPEC-TE011-017 obligation row for orders 1–5;
     - the ASM-TE011-27 risk column.

     RWB-E1-042 revision 10 §12.3 step 3 adds check constraints with value lists (for example
     `ck_parameter_catalog_scope (GLOBAL, PRODUCT)`). A guard written as `format('… CHECK (scope IN (%L,
     %L))', …)` is now a `(DML in procedural body)` finding, while those three places say it is not.
  2. **The contract keeps the old phrase.** `fixtureMatching` still says "DML in a DO block is a finding
     with field (DML in procedural body)". SG9-04 removed that phrase from T10 and from the compliance
     row, because the catch-all covers every unlisted statement in a `DO`, function or procedure body.
  3. **Other placeholder forms are not named.** The rules name `%I` and its positional form `%1$I`. They
     do not name the positional or flagged forms of the other specifiers (`%1$s`, `%2$L`, `%-10s`), or
     `%%`. A lint that matches the text `%s` literally would read `%1$s` as neither rule.
  4. **TS-TE011-09 (e) gives no result.** It asserts only the "not built" line and "no git command". The
     base tree holds O with an uncorrected finding, so the run exits 1. A system test cannot observe "no
     git command"; the unit row's mock git runner does that.
  5. **ASM-TE011-29 risk is no longer exact.** It reads "a repository without the target branch fails
     with exit 2, so the condition is never skipped silently". Since run 9 that holds only where the list
     is built. Elsewhere (e) is skipped on purpose, with a `PDPA-SCOPE` line.
  6. **The unit row "Output (-012)" is out of date.** It says `PDPA-SCOPE:` lines "carry paths and counts
     only". The new lines also carry target and branch names.
- **Required fix:**
  1. Add "with only `%I` placeholders (SPEC-TE011-008 class 3)" to the "Known files" row, the
     SPEC-TE011-017 orders 1–5 row and the ASM-TE011-27 risk column.
  2. In the contract, replace "DML in a DO block is a finding" with "any statement in a DO, function or
     procedure body that the class-3 rules do not list".
  3. State that every format specifier other than `%I`, in any positional or flagged form, follows the
     `%s`/`%L` rule, and that `%%` is a literal percent sign. Add one unit scenario with `%1$L`.
  4. In TS-TE011-09 (e), state the exit code (1, from the uncorrected O), or add C so the run exits 0.
     Leave the "no git command" check to the unit row.
  5. Restate the ASM-TE011-29 risk as "where the list is built", and name the `PDPA-SCOPE` line for the
     other case.
  6. Change the unit row to "paths, branch names and counts".

## 4. Other checks

| Check | Result |
|---|---|
| Personal data in the artefacts | None found. No e-mail address and no run of 9 or more digits in `specify/` outside the `*.run*` backups (counts only printed). Only synthetic values and placeholders are used (`SYN-…`, `<text>`, `<id>`, `V0003__rwb_e1_042_seed.sql`, `V0004__rwb_e1_042_seed2.sql`, `feature/x`). |
| Secrets | None. |
| Contracts | Both parse as JSON. The new lines `changedFileBuiltLine`, `changedFileNotBuiltLine` and `changedFileBranchMissingLine` match SPEC-TE011-013 and T14/T15. The exit-2 list matches SPEC-TE011-012 and the status matrix. `correctiveMigration` carries the SG10-02 split. `fixtureMatching` carries SG10-03 item 2. `NO_API_CHANGE` is consistent. |
| Authorization and audit | Unchanged and appropriate for a build tool. `changedFiles.protectedBranches` is configuration under the code-owner entry (SPEC-TE011-014, -015), so shrinking it to re-enable the list on `main` or `develop` needs a tech-lead approval. Running `git` reads repository metadata only, with no database and no network (story §13, §17). |
| Unit Test Applicability | Compliant. The front end is `NOT_APPLICABLE` with evidence. The tool back end is `REQUIRED` at 80% on JaCoCo LINE, BRANCH, METHOD and INSTRUCTION, with coverage verification in the job. SG10-01..03 add scenarios. |
| Evidence | No new script. The new claims rest on repository files and other stories' specifications, which the reviewer read directly: `.gitlab-ci.yml`, `scripts/dev.ps1`, `.git/HEAD`, D-RCV-50 (full text: story MRs target `develop-recovery`; `develop-recovery` is merged into `develop` in batches; `develop-recovery` is brought up to date with `develop` before a story branch is cut), L-RCV-13, E1-044 v14-7 T-044-18 and its fixture rule, E1-042 revision 10 §12.3. A sync from `develop` into `develop-recovery` through a story-like branch builds the list, but a tree diff does not list a file whose content is unchanged, so it does not trip (e); no finding. |
| Cross-story versions | RWB-E1-042 is now revision 10 (05:28); §12.3 is identical to revision 9, so the "Known files" reading stands apart from SG10-03 item 1. RWB-E1-043 is now revision 7 (05:34). It keeps open item R4 (owner RW-COMPLY, blocks RWB-E1-064) and the forward note that `validate` refuses an `is_personal` change (422 MSG-P1-002) and that `apply` and `onRolledBack` never write it. It still asks nothing of RWB-TE-011 (GAP-38). E1-044 (01:35), TE-001, TE-002, TE-003 and E1-001 are unchanged since round 9. |
| Run decisions | D-RUN-06: the local merge gate runs `dev.ps1 test` on the story branch, where the list is built. D-RUN-07: no number is fixed. D-RUN-08: no dependency on a later story; nothing is asked of RWB-E1-044 (§3b, SPEC-TE011-003, -017). D-RUN-09 applied. The triage is attributed to the orchestrator (Claude Code), and no human disposition is claimed. Observation, not a finding against this specification: the build log row for this triage carries the batch time 2026-11-18T05:31:18 and says "one further Low-only round allowed (run 10, review-11)", while the specification and `agent-run-log.md` cite 05:13. The build log row also does not restate the three SG9-03 tests. Reconciling it is for the orchestrator. |
| Data classification (pdlc stop condition) | The classification source, the residual risk, both RWB-E1-001 outcomes and the load-route limit are visible and unchanged. R4 (RW-COMPLY) is consistent with RWB-E1-043 revision 7. The RWB-E1-064 story file lists DF-REF-105 `is_personal` as Read (DGL-13). No open data-classification blocker belongs to this story. |
| Document gaps | No new document gap. The findings concern this specification, not the document set. `review/document-gaps-10.md` is not written. |

## 5. Gate output

```text
REVIEW_STATUS: FAIL
REVIEW_COUNTS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 3]
ROUND_9_DISPOSITION: SG9-01 Resolved (FIXTURE-ID in a body INSERT/UPDATE takes its table; DML-in-body row lists body tables; unit scenarios); residual splits in SG10-02. SG9-02 Resolved (%I only as a name; %s/%L give the finding; placeholder DEFAULT; literal DEFAULT as class 2; whole class-2 list in bodies; COPY ... FROM catch-all); residual text in SG10-03. SG9-03 Resolved as specified (built only into develop-recovery from a non-protected branch; T15; TS-09 (h)-(k)); tag pipelines and fetch order in SG10-01. SG9-04 Resolved; contract phrase in SG10-03
ROUND_1_8_DISPOSITION: all remain Resolved; no regression
SG9-03_TRIAGE_TESTS: (1) promotion never fails for lack of a list: partly (tag pipeline; unconditional fetch); (2) list-dependent rules only where defined: met; (3) every other target stated and tested: partly (tag pipeline; detached HEAD)
NEW_FINDINGS: SG10-01 Low (GitLab tag pipelines are not branch pipelines and build the list, so a release tag after a squash promotion fails on (e); the job fetches the target before the tool decides; detached HEAD gives --branch HEAD, undefined); SG10-02 Low (body CREATE TABLE ... AS gives no target table though top level gives t; FIXTURE-ID in a body MERGE INTO / CREATE TABLE AS fits "that table" and "body text ... none"; DML inside literal EXECUTE text has no stated target table); SG10-03 Low (%I-only limit missing from Known-files row, SPEC-017 orders 1-5 row and ASM-27 risk; contract "DML in a DO block"; %1$s/%2$L/%% not named; TS-09 (e) no exit code; ASM-29 risk; PDPA-SCOPE unit row)
NEW_DOCUMENT_GAPS: none
CROSS_STORY_RWB-E1-044: Consistent with v14-7 (SPEC-010 lint fixtures; SPEC-011 Flyway fixtures; RUN-BRIEF rule 7 cited; T-044-18 synthetic table); nothing asked of it
CROSS_STORY_RWB-E1-042: Revision 10 section 12.3 identical to revision 9; step-3 check lists make SG10-03 item 1 material
CROSS_STORY_RWB-E1-043: Revision 7 keeps R4 (RW-COMPLY) and the RWB-E1-064 forward note; nothing asked of TE-011
CROSS_STORY_RWB-E1-001: Consistent; unchanged since round 9
CROSS_STORY_RWB-TE-001/-002/-003: Consistent; unchanged since round 9
BLOCKING: YES under D-RUN-09 (Low-only failure is not accepted by the orchestrator; REVIEW_GATE_WARNING would otherwise apply)
NEXT_STEP: The orchestrator (Claude Code) triages SG10-01..SG10-03. Under D-RUN-09 the Technical Specifier fixes all three and requests spec gate round 11 (review/spec-gate-review-11.md). This review does not start the Implementation Planner.
```

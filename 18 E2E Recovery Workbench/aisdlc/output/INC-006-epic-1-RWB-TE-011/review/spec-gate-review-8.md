# Spec gate review, round 8: RWB-TE-011 PDPA lint for code, tests and logs

| Field | Value |
|---|---|
| RUN_ID | `INC-006-epic-1-RWB-TE-011` |
| Gate | Spec gate, re-review round 8 (Compliance Reviewer, independent of the author) |
| Earlier rounds | Round 1 `review/spec-gate-review.md` (FAIL, 2 Medium, 5 Low); round 2 `-2.md` (FAIL, 1 Medium, 1 Low); round 3 `-3.md` (FAIL, 2 Low); round 4 `-4.md` (FAIL, 3 Medium, 1 Low) with `document-gaps-4.md`; round 5 `-5.md` (FAIL, 1 Medium, 3 Low) with `document-gaps-5.md`; round 6 `-6.md` (FAIL, 4 Low); round 7 `-7.md` (FAIL, 1 Medium, 3 Low: SG7-01..SG7-04) |
| Reviewed | `specify/spec.md` (SPEC-TE011-001..018, revised 18 Nov 2026 after round 7), `assumptions.md` (ASM-TE011-01..29), `document-gaps.md` (DGL-01..15), `shared-updates.md` (§1–§5, including §3b), `gate-response.md` ("Gate response — round 7"), `compliance-validation.md`, `agent-run-log.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `evidence/`; the `*.run7.*` copies, compared line by line (unified diff in the reviewer scratchpad) |
| Direction checked | The round-7 triage came from the orchestrator (Claude Code), logged at 2026-11-18T04:54, not from a human. The build log has no row for that triage itself; its 04:59:09 row ("Gate triage (note)") refers to "the 04:54 triage". D-RUN-06, -07, -08, -09, -15, -17 (`AI-SDLC-BUILD-LOG.md` §1) |
| Cross-story input (read only) | RWB-E1-044 spec v14-7 (`INC-001`: SPEC-RWB-E1-044-007 search-path table and tokenizer, -010, -011; restated AC1–AC9; T-044-10..T-044-22 and the T-044-22 case tables); RWB-E1-042 spec revision 8 (`INC-003`, §12.3 steps 1–8; identical to revision 7, which the specifier read); RWB-TE-001 v4 (`INC-002`, SPEC-012 (b), T-TE001-13, plan: "merges … only after `./scripts/dev.ps1 test` exits 0 on the branch"); RWB-TE-002 (`INC-004`, UT-15); RWB-TE-003 (`INC-005`); RWB-E1-043 revision 4 (`INC-008`, open item R4 owner RW-COMPLY, §3.2); RWB-E1-001 (`INC-009`, `evidence/is_personal_union_v4.tsv`); RWB-E1-064 story file v1 (Story Files v7 §12: DF-REF-105 `is_personal` Read); `AGENTS.md` §3.7, §4.6; decision register D-RCV-28 |
| Checked against | `backend/src/main/resources/application.yaml` (line 83 `location: classpath:db/modulemigration/recovery` under `rwb.flyway`); `application-local.yaml` (no override of `rwb.flyway.location`); `scripts/dev.ps1` (`ValidateSet` and the `test` command: Gradle `test`, then `npm run check`); `.gitlab-ci.yml` (no `workflow:` block; `backend-unit` and `frontend-check` have no `rules:`); Physical Schema v6 copy (`sys_fields` rows DF-REF-104, -156, -166); today's tree (`*.sql` outside `aisdlc/`: only `infra/postgres/schema/*` and `infra/postgres/init/20-grants.sql.inc`; migration folder holds `README.md` only; `backend/src/test/resources/` holds `architecture/` only) |
| Method | Diff of every changed file against its `run7` copy, then a full read of SPEC-TE011-001, -003, -008, -012, -013, -015..-018, the exception table, the test tables and the coverage table. Each new claim about another story was checked in that story's specification. Greps of `specify/` (backups excluded) for e-mail addresses, runs of 9 or more digits and stale phrases. Both contracts parsed as JSON |
| Date | 2026-11-18 |
| Reviewer | Compliance Reviewer (agent) |

## 1. Result

**Overall status: FAIL**

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 6 |

**Round 7.** SG7-01, SG7-02, SG7-03 and SG7-04 are resolved as the orchestrator's triage directed. Each
was checked against `spec.md` and the other artefacts, not against `gate-response.md` alone. No finding
from rounds 1–6 has reopened. The Medium is closed: RWB-E1-044's malformed and out-of-class lint fixtures
no longer give exit 2 or findings at this story's merge.

Six new Low findings remain. Under D-RUN-09 Low findings are fixed, not accepted, so the gate fails.

- **SG8-01.** For a finding with no target table, the text drops condition (e). That contradicts T11.
- **SG8-02.** The target-table table gives a FIXTURE-ID inside a `DEFAULT` no table, although the value is
  written into rows. Its FIXTURE-ID rows also leave several statement forms unplaced.
- **SG8-03.** The procedural-body rules have no catch-all. The `EXECUTE` leading-keyword test also admits
  class-4 forms that are findings at top level.
- **SG8-04.** In this repository's `.gitlab-ci.yml`, the GitLab branch of the changed-file list is never
  used. A shallow-clone merge-base failure is undefined.
- **SG8-05.** The Flyway-fixture reading over-claims, and §3b both asks RWB-E1-044 and says nothing is
  asked of it. Lint-fixture roots are not bounded to test roots.
- **SG8-06.** Five stale or inconsistent text items.

**The orchestrator's round-7 triage is applied soundly:**

- **SG7-01.** The lint-fixture class is in SPEC-TE011-003:
  - FIXTURE-ID only, on the raw text, never parsed, never exit 2 from content;
  - printed in `PDPA-SCOPE: lint fixtures …` with its file count;
  - forbidden from covering the migration folder (T12).

  Its default, `backend/src/test/resources/migration-lint/**`, is taken from RWB-E1-044 v14-7
  SPEC-RWB-E1-044-010 as it stands, and both folders are cited. `flyway-fixtures/` is left out with
  reasons (but see SG8-05). Reader precedence is limited to the reader's files, and SPEC-TE011-018 to the
  migration folder, with a unit scenario for each. TS-TE011-08 mirrors:
  - N11–N13;
  - the three `ALTER … SET search_path` forms;
  - the T-044-21 INSERT;
  - a `-- Fix:` naming an unknown file.

  It expects exit 0 by default and PDPA-FIXTURE-ID on a run-time-built ID. Nothing is asked of RWB-E1-044
  (SPEC-TE011-003, -017).
- **SG7-02.** The reviewer re-read RWB-E1-042 §12.3 (revision 8, identical to revision 7). The "Known
  files" row now lists steps 1–8 and the 16 step-3 guards. Class 3 now lists:
  - direct DDL, `DELETE` and `TRUNCATE` in a `DO` body;
  - the `EXECUTE` of a literal or of `format(<literal>, …)`.

  `ALTER`/`DROP FUNCTION|PROCEDURE` are in class 2 and `CREATE TABLE … AS` is in class 4 only. A `DEFAULT`
  literal on a resolved personal pair is a position. §3b item 1 asks the RWB-E1-042 planner for the
  direct guard form. TS-TE011-07 and the unit row cover each case.
- **SG7-03.**
  - SPEC-TE011-018 has a target-table table and a scope line.
  - SPEC-TE011-013 makes the changed-file list required, built with `git merge-base` and `git diff
    --name-only --diff-filter=AMR`, in GitLab and in `scripts/dev.ps1 test` against `develop-recovery`.
    T14, TS-TE011-09 and a unit row test it. RWB-TE-001's plan confirms that the orchestrator runs
    `dev.ps1 test` on the story branch before merging, so HEAD there is the story branch, as the design
    needs.
  - The migration folder is read from `rwb.flyway.location`, and a mismatch gives exit 2. The property
    is at line 83 and has no profile override.
  - ASM-TE011-26 and the contract were rewritten (but see SG8-01).
- **SG7-04.**
  - The run-log header now reads 29 assumptions, 15 CLARs and round 8.
  - DGL-08, CLAR-004 and SPEC-TE011-008 state that a non-text personal value in a migration must be
    `NULL`. §3b item 6 tells the owner of such a seed to raise it.
  - Both "already passed" claims are gone.
  - SRC-25 cites RWB-E1-043 revision 4, and R4's owner is "RW-COMPLY" everywhere. The phrase "data
    architect" appears nowhere outside the backups.

## 2. Disposition of round-7 findings

| Finding | Severity | Disposition | Evidence (checked against the spec, not against `gate-response.md` alone) |
|---|---|---|---|
| SG7-01 RWB-E1-044 lint fixtures give exit 2 or findings at this story's merge | Medium | **Resolved** as triaged. A residual over-claim on the Flyway fixtures and a mixed §3b message are raised as SG8-05 (new evidence: E1-044 does not fix the AC8 statement form). | **Fix 1.** SPEC-TE011-008 "Other rules" and the closing paragraph of "SQL statement classes" limit reader precedence to "a file the reader reads (the baseline, the recovery migration folder and configured dictionary files)". SPEC-TE011-018 "Scope" and "Unknown file" are limited to the migration folder. Unit rows "SQL statement classes" (test-SQL `sys_fields` INSERT: no exit 2; the reviewer confirmed DF-REF-104 `sys_fields.source_field` is described with `is_personal` false in PS v6 and is not in the protective union) and "Corrective migration" (scope). **Fix 2.** SPEC-TE011-003 class "Lint fixtures" and the "Lint fixtures" block. The test class excludes the lint-fixture roots, and a file under both is in the lint-fixture class only. ASM-TE011-05 and -28. The default matches E1-044 SPEC-010 ("fixture tests scan folders under `backend/src/test/resources/migration-lint/`"), and T-044-22 says "Each case is its own fixture file in its own folder". **Fix 3.** "Known files" E1-044 row, state (1), SPEC-TE011-017 orders 1–5 row, §3b item 5 and closing lines, ASM-TE011-25 and -27. **Fix 4.** TS-TE011-08, T13. |
| SG7-02 E1-042 step-3 guards omitted; class 3 ambiguous; four class gaps | Low | **Resolved.** Residual gaps in the body rules are raised as SG8-03. | "Known files" E1-042 row matches E1-042 rev 8 §12.3 steps 1–8 (step 2: three columns, no `DEFAULT`; step 3: 16 guarded additions; step 8: self-check). Class 3 `DO`-body list; function-body sentence; class 2 `ALTER`/`DROP FUNCTION|PROCEDURE`; class 4 `CREATE TABLE … AS`, `ALTER ROLE`, `ALTER DATABASE`, `ALTER SYSTEM`; `DEFAULT` position in `CREATE TABLE`, `ADD COLUMN`, `SET DEFAULT`. §3b item 1; ASM-TE011-27; contract `fixtureMatching`; TS-TE011-07; unit row. |
| SG7-03 Four undefined points in SPEC-TE011-018 and -003 | Low | **Resolved** on each of the five fixes. The new text raises SG8-01, SG8-02 and SG8-04. | (1) Target-table table; unit scenarios. (2) Scope. (3) SPEC-TE011-013 "Changed-file list" (required); `scripts/dev.ps1` is named in "Impacted Existing Nodes"; T14; TS-TE011-09 (a)–(e); unit row "Changed-file list". (4) SPEC-TE011-003 "Source of the path"; T12; unit row "Scan scope"; contract. The reviewer confirmed `application.yaml` line 83 and that `application-local.yaml` does not override it. (5) ASM-TE011-26 and contract `correctiveMigration` now carry the no-target-table case. |
| SG7-04 Stale and over-claimed text | Low | **Resolved.** | (1) `agent-run-log.md` header: round 8 requested, ASM-TE011-01..29, CLAR-001..015 (both counts match the files). (2) DGL-08, CLAR-004, SPEC-TE011-008 non-text bullet, §3b item 6. DF-REF-156 and -166 are uuid and in the union (`is_personal_union_v4.tsv`). (3) SPEC-TE011-017 lead-in, "Known files" ending, §3b closing ("records no hand-off"), and the RWB-E1-001 note now reads "first raised in the orchestrator's triage". (4) SRC-25 revision 4; R4 owner "RW-COMPLY" in the spec, DGL-13, OPEN-NEW-TE011-7 and the "Out of scope" list. |

**Regression check, rounds 1–6.** No finding has reopened. The reviewer re-checked:

- SG-01 (9 Restricted fields);
- SG-04 (`infra/postgres/schema/**` the only `infra` exclusion);
- SG2-01 (14 of 18; 509);
- SG4-01 ((object, field) matching; no allow entry on a migration; point in time);
- SG4-03 (R1/R2 reader; fail closed);
- SG5-01 (per-pair resolution);
- SG5-03 (`(columns not named)`);
- SG6-02 (migration folder cannot be left out; it now also covers lint-fixture roots);
- SG6-03 (TS-TE011-01 dictionary scope).

The counts 18 / 14 / 509 / 526 / 390 / 71 still agree. The coverage table has 32 rows (`TOTAL_RULES: 32`).

## 3. New findings

### REVIEW-TE011-SG8-01: Condition (e) is dropped for findings with no target table; T11 says (a) to (e) (Low)

- **Affects:**
  - SPEC-TE011-018 condition (d), "A finding with no target table needs only (a) to (c)";
  - ASM-TE011-26, "needs only the first three conditions";
  - contract `correctiveMigration`, "needs only the first three conditions";
  - unit row "Corrective migration" ("accepted on (a) to (c)", twice);
  - T11;
  - TS-TE011-09.
- **Evidence:**
  1. **Literal reading.** Condition (d) says a finding with no target table "needs only (a) to (c)".
     Condition (e) is the changed-file rule. Read literally, (e) does not apply to these findings.
     ASM-TE011-26 and the contract say the same: (e) is the fourth condition there, so "the first three
     conditions" leave it out.
  2. **The contradiction.** T11 says a finding is accepted with "a corrective migration that meets
     conditions (a) to (e)". The (e) bullet says "A file added or edited in the same change is fixed in
     the file, not corrected".
  3. **Which findings this covers.** Under the target-table table, findings with no target table include
     `(DML in procedural body)`, which is a `DO` block that writes seed rows. They also include FIXTURE-ID
     in a comment, `COMMENT ON` text, DDL or a `DO` body, and `(statement not recognised)` where no table
     is readable.
  4. **The consequence.** An implementer who follows (d), ASM-TE011-26 or the contract would accept a new
     migration O and its "corrective" C added in the same change. The new `DO`-block DML, or a new stored
     ID, would then show only as a notice. Only code-owner review would stand in the way. That is the
     bypass that SG7-03 item 3 and condition (e) exist to stop.
  5. **No test.** TS-TE011-09 tests (e) only with a target-table finding.
- **Required fix:**
  1. State that (e) applies to every finding. For example: "A finding with no target table needs (a) to
     (c) and (e)". Apply the same wording in ASM-TE011-26, the contract and the unit row.
  2. Add a TS-TE011-09 case: a story branch adds O, holding a `DO` block with an `INSERT`, together with
     C naming O. The changed-file list holds O, so the expected result is exit 1.

### REVIEW-TE011-SG8-02: The target-table table gives no table to a FIXTURE-ID in a `DEFAULT`, and its FIXTURE-ID rows are not exhaustive (Low)

- **Affects:** SPEC-TE011-018 condition (d) and its target-table table; unit row "Corrective migration"
  ("in a DDL default → none"); contract `correctiveMigration`.
- **Evidence:**
  1. **`DEFAULT` values reach rows.** SPEC-TE011-008 class 2 makes a `DEFAULT` literal a position because
     `ALTER TABLE … ADD COLUMN … DEFAULT` "writes the value into every existing row". For a FIXTURE-FIELD
     `DEFAULT` finding, (d) therefore requires an `UPDATE`/`DELETE`/`TRUNCATE` and an `ALTER COLUMN …
     DROP|SET DEFAULT`. A FIXTURE-ID in the same `DEFAULT` (for example a stored 13-digit ID) is put in
     the row "in DDL (including a `DEFAULT`) → None". A corrective migration with no data change is then
     accepted, and the ID stays in every existing row and in every later row. That is the same harm, but
     a weaker rule.
  2. **Unplaced FIXTURE-ID forms.** The FIXTURE-ID rows cover only two cases: "a value of an `INSERT` or
     `UPDATE`", and "a comment, `COMMENT ON` text, DDL or a `DO` body". They do not place a FIXTURE-ID
     match in:
     - a `COPY … FROM stdin` data block;
     - `MERGE INTO <t>`;
     - `SELECT … INTO <t>`;
     - `CREATE TABLE <t> AS VALUES …`;
     - a function or procedure body;
     - `CALL p('<value>')`;
     - a `SET` value.

     The first four write data to a readable table. The `(statement not recognised)` row already gives
     their table for FIXTURE-FIELD. For FIXTURE-ID the implementer must guess.
- **Required fix:**
  1. Treat a FIXTURE-ID match in a `DEFAULT` like the FIXTURE-FIELD `DEFAULT` row: the target table is
     the table, and C also needs `ALTER COLUMN … DROP|SET DEFAULT`.
  2. Add a default FIXTURE-ID row: "in any other statement, the table the statement writes when the lint
     can read it (`COPY <t>`, `MERGE INTO <t>`, `SELECT … INTO <t>`, `CREATE TABLE <t> AS`); otherwise
     none".
  3. Align the contract, and add unit scenarios for an ID in an `ADD COLUMN … DEFAULT` and in a `COPY`
     data block.

### REVIEW-TE011-SG8-03: Procedural bodies have no catch-all, and the `EXECUTE` keyword test admits class-4 forms (Low)

- **Affects:** SPEC-TE011-008 class 3 (`DO` blocks; function and procedure bodies); ASM-TE011-27; contract `fixtureMatching`; §3b item 1; unit row "SQL statement classes"; TS-TE011-07.
- **Evidence:**
  1. **No catch-all.** The `DO`-body list names only what raises nothing and what is a finding. It does
     not say what happens to any other statement in a body, for example:
     - `CALL p(…)`;
     - a direct `ALTER ROLE … SET search_path`, `ALTER DATABASE` or `ALTER SYSTEM`;
     - a direct `CREATE TABLE t AS SELECT …` or `IMPORT FOREIGN SCHEMA`;
     - a direct `GRANT`, `REVOKE` or `SET`, unless these count as "direct DDL of the class-2 kinds";
     - cursor statements.

     At top level these are class 2 or class 4. In a body they are unplaced. SG5-03 and the 01:02 triage
     say unrecognised forms fail closed. The body list does not say so.
  2. **`EXECUTE` checks only the first keyword.** An `EXECUTE` of a literal that starts with `CREATE` or
     `ALTER` raises nothing, because "The lint reads only that leading keyword". So the following pass
     with no finding inside a `DO` body or function, although each is a class-4 finding at top level:
     - `EXECUTE 'CREATE TABLE t AS VALUES (''<text>'')'`, which writes a row;
     - `EXECUTE format('CREATE TABLE %I AS SELECT …', …)`;
     - `EXECUTE 'ALTER ROLE … SET search_path …'` and `EXECUTE 'ALTER SYSTEM …'`.

     The `DO` body then writes data or changes roles while raising nothing.
- **Required fix:**
  1. Add a catch-all to class 3. Any statement in a `DO`, function or procedure body that the list does
     not name gives `(DML in procedural body)`, or `(statement not recognised)` if that name is preferred.
     Say whether `GRANT`, `REVOKE` and `SET` count as "direct DDL of the class-2 kinds".
  2. Class a DDL `EXECUTE` literal, or a `format` string, by its leading words as a top-level statement
     would be classed. `CREATE TABLE … AS` and `ALTER ROLE|DATABASE|SYSTEM` are then findings.
  3. Align ASM-TE011-27, the contract and §3b item 1.
  4. Add unit scenarios: `CALL` in a `DO` body; `EXECUTE 'CREATE TABLE t AS …'`; direct `ALTER ROLE` in a
     `DO` body.

### REVIEW-TE011-SG8-04: The GitLab changed-file list is never built in this repository's pipeline, and a merge-base failure is undefined (Low)

- **Affects:** SPEC-TE011-013 ("GitLab merge request pipeline"; first bullet "no `rules:` filter … merge requests and every branch build"); SPEC-TE011-018 condition (e); T14; ASM-TE011-29; unit row "Changed-file list".
- **Evidence:**
  1. **No merge request pipelines.** `.gitlab-ci.yml` has no `workflow:` block. `backend-unit` and
     `frontend-check` have no `rules:`, and the new `pdpa-lint` job is specified the same way. In GitLab,
     jobs with no `rules:` and no `workflow:rules` run in branch (push) pipelines only. No
     `merge_request_event` pipeline is created, so `$CI_MERGE_REQUEST_TARGET_BRANCH_NAME` is never set.
  2. **(e) is not enforced on GitLab.** The spec passes `--changed-files-from-git` only in a merge request
     pipeline: "In a branch pipeline it passes no option". So on a GitLab host the list is always empty
     and condition (e) is never enforced there. The local `dev.ps1 test` path, which is the merge gate in
     this repository, is not affected.
  3. **Shallow clones.** GitLab clones shallowly by default (`GIT_DEPTH`). `git merge-base` can then find
     no common ancestor even though the target resolves. The spec defines exit 2 only for "a target that
     cannot be resolved". It does not say what happens when no merge base is found. An implementation
     that returns an empty list would skip (e) silently.
- **Required fix:**
  1. In a GitLab branch pipeline on any branch other than `changedFiles.targetBranch`, fetch that branch
     and pass `--changed-files-from-git origin/<targetBranch>`, as the local path does. Keep the
     merge-request variable for merge request pipelines where they exist. The list is empty only on the
     target branch itself.
  2. Set `GIT_DEPTH: 0` for the job, or fetch enough history.
  3. Make "no merge base found" exit 2, with a message such as `changed-file list: no merge base with
     {name}`. Add it to T14, the contract and the unit row.
  4. Correct the first SPEC-TE011-013 bullet so that it does not imply merge request pipelines exist.

### REVIEW-TE011-SG8-05: The Flyway-fixture reading over-claims; §3b both asks and does not ask RWB-E1-044; lint-fixture roots are unbounded (Low)

- **Affects:** SPEC-TE011-003 "Not in the default: `flyway-fixtures/`" and "Lint fixtures" rules; SPEC-TE011-008 "Known files" E1-044 row; SPEC-TE011-016 state (1); `shared-updates.md` §3b heading, rules 1–3 and item 5; ASM-TE011-28.
- **Evidence:**
  1. **The AC8 form is not fixed.** The spec says the Flyway fixtures, including "for AC8 a statement
     that references a missing table", "are valid SQL in recognised forms", "class 1 or 2", and that "0
     findings are expected". RWB-E1-044 v14-7 does not fix that statement's form. Its restated AC8 says
     only "A fixture whose second statement references a missing table" (see also T-044-14).
     `INSERT INTO ${recoverySchema}.missing_t VALUES (1);` is a natural way to write it. That is a
     column-less `INSERT` with a literal, a PDPA-FIXTURE-FIELD `(columns not named)` finding in the test
     class (SPEC-TE011-008 "Other rules"; TS-TE011-05 (a)).
  2. **No remedy named.** The spec names no remedy for a finding in another story's merged test fixture
     outside the migration folder. The allow list would need renewing at each expiry (BR6), because the
     fixture is permanent. Moving the folder into the lint-fixture class would drop FIXTURE-FIELD from it.
     Editing another story's fixture is a cross-story change. ASM-TE011-28 gives the configuration route
     only for fixtures "elsewhere".
  3. **Mixed message in §3b.** §3b is addressed to "the planners of build orders 1–5 (RWB-E1-044, …)".
     Its rule 1 ("Every SQL `INSERT` names its columns") therefore reaches RWB-E1-044's Flyway fixtures,
     but item 5 says "**Nothing is asked of RWB-E1-044**". The 04:54 triage says nothing is asked of
     RWB-E1-044.
  4. **Lint-fixture roots are unbounded.** The only bound on `lintFixtureRoots` is that it must not
     cover the migration folder. The spec gives precedence only over the test class ("a file under both a
     lint-fixture root and the test root is in the lint-fixture class only"). For a root over production
     source or `infra/**`, the class is undefined. If the lint-fixture class wins there, the LOG,
     EXCEPTION and TOSTRING rules silently stop for those files. The class is meant for test SQL
     (ASM-TE011-28: "Test SQL that another tool needs malformed").
- **Required fix:**
  1. State that E1-044 does not fix the AC8 statement form. Say what this story's merge does if a merged
     Flyway fixture gives a finding: for example, the implementation run records it and the orchestrator
     decides, or a named reviewed route. Keep the claim at "expected if the fixture names its columns".
  2. Make §3b consistent with the triage. Either exclude RWB-E1-044 from rules 1–3, or label them as
     information for it, not as a request.
  3. Require every lint-fixture root to lie under the test roots (`backend/src/test/**`, the front-end
     test roots), otherwise exit 2. Add the case to T12 and the unit row "Scan scope".

### REVIEW-TE011-SG8-06: Stale and inconsistent text (Low)

- **Affects:** TS-TE011-06 (i); system-test table order; unit row "Scan scope"; SPEC-TE011-001 "Sources and order" item 2; ASM-TE011-29 risk.
- **Evidence:**
  1. **Stale option name.** TS-TE011-06 (i) still reads "with O on the `--changed-files` list". That
     option was replaced by `--changed-files-from-git <target>` (SPEC-TE011-013), and no other text
     defines `--changed-files`.
  2. **Row order.** The system-test table lists TS-TE011-08 and -09 before TS-TE011-07.
  3. **Duplicate scenario.** The unit row "Scan scope" lists "`dictionary.migrationFolder` set to another
     path → exit 2" twice.
  4. **Fixed path in SPEC-TE011-001.** Item 2 still names the fixed folder
     `backend/src/main/resources/db/modulemigration/recovery/`. It does not say the folder comes from
     `rwb.flyway.location`, as SPEC-TE011-003 now requires ("The reader (SPEC-TE011-001) and the scan both
     use that folder").
  5. **ASM-TE011-29 over-claims.** Its risk column says "A change to `rwb.flyway.location` moves the
     scanned folder with Flyway". The default root of the class "Seeds and migrations" is a fixed glob, so
     such a change gives exit 2 (T12) until the root is changed by a reviewed configuration change.
     Failing closed is the right outcome, but the text should say that is what happens.
- **Required fix:**
  1. Write TS-TE011-06 (i) with `--changed-files-from-git` and a temporary repository, or point it to
     TS-TE011-09.
  2. Put the system-test rows in order and remove the duplicate scenario.
  3. Make SPEC-TE011-001 item 2 read "every `*.sql` file in the folder given by `rwb.flyway.location`
     (SPEC-TE011-003)".
  4. Correct the ASM-TE011-29 risk text.

## 4. Other checks

| Check | Result |
|---|---|
| Personal data in the artefacts | None found. No e-mail address and no run of 9 or more digits in `specify/` outside the `*.run*` backups. Only synthetic values and placeholders are used (`SYN-…`, `<text>`, `V0003__rwb_e1_042_seed.sql`, `r`, `d`, `f()`). The reviewer's scripts printed counts only. |
| Secrets | None. |
| Contracts | Both parse as JSON. The new lines `lintFixtureScopeLine`, `migrationFolderMismatchLine` and `changedFileTargetMissingLine` match SPEC-TE011-003 and -013. The exit-2 list matches SPEC-TE011-012. "correctiveMigration" carries the SG8-01 wording defect. `NO_API_CHANGE` is consistent with the status matrix. |
| Authorization and audit | Unchanged and appropriate for a build tool. Change control is through code owners (SPEC-TE011-014), and `lintFixtureRoots` and `changedFiles.targetBranch` are configuration under that entry (SPEC-TE011-015). Running `git` reads repository metadata only, with no database and no network. This is consistent with story §13 "Database. None" and §17 "the lint reads files only" (Story Files v7). |
| Unit Test Applicability | Compliant. The front end is `NOT_APPLICABLE` with evidence. The tool back end is `REQUIRED` at 80% on JaCoCo LINE, BRANCH, METHOD and INSTRUCTION. `ChangedFileList` is listed among the tool components and has a unit row. SG8-01..SG8-05 add scenarios. |
| Evidence | No round-7 script was added. The new claims rest on other stories' specifications and repository files, which the reviewer read directly: E1-044 SPEC-010/-011, T-044-10..22, restated AC8; E1-042 rev 8 §12.3; TE-001 SPEC-012 (b) and plan; `application.yaml`; `dev.ps1`; `.gitlab-ci.yml`. |
| Run decisions | D-RUN-06: the local merge gate on the branch is matched by `dev.ps1 test` with the branch as HEAD. D-RUN-07: no number is fixed. D-RUN-08: no dependency on a later story; nothing is asked of RWB-E1-044, but see the §3b mixed message in SG8-05. D-RUN-09 is applied. D-RUN-15 and D-RUN-17 are unchanged. The triage is attributed to the orchestrator (Claude Code), and no human disposition is claimed. The build log records no row for the TE-011 round-7 triage itself, only the 04:59:09 note that cites it. That is the orchestrator's log to complete; it is not a defect in this specification. |
| Data classification (pdlc stop condition) | The classification source, the residual risk, both RWB-E1-001 outcomes and the load-route limit are visible. R4 (RW-COMPLY) is consistent with RWB-E1-043 revision 4. RWB-E1-064 story file v7 lists DF-REF-105 `is_personal` as Read, as DGL-13 says. No open data-classification blocker belongs to this story. |
| Document gaps | No new document gap. The findings concern this spec, other runs' specifications and this repository's CI file, not the document set. `review/document-gaps-8.md` is not written. |

## 5. Gate output

```text
REVIEW_STATUS: FAIL
REVIEW_COUNTS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 6]
ROUND_7_DISPOSITION: SG7-01 Resolved as triaged by the orchestrator (lint-fixture class, FIXTURE-ID only, never exit 2, PDPA-SCOPE count, cannot cover the migration folder; reader precedence and SPEC-TE011-018 limited; TS-TE011-08; nothing asked of E1-044); residual Flyway-fixture over-claim in SG8-05. SG7-02 Resolved (E1-042 rev 8 steps 1-8; DO-body rules; DEFAULT position; class changes); residual body gaps in SG8-03. SG7-03 Resolved (target-table table, scope, changed-file list in GitLab and dev.ps1, rwb.flyway.location, ASM-26/contract); new defects SG8-01, SG8-02, SG8-04. SG7-04 Resolved
ROUND_1_6_DISPOSITION: all remain Resolved; no regression
NEW_FINDINGS: SG8-01 Low (condition (e) dropped for no-target-table findings in (d), ASM-26, contract, unit row; contradicts T11); SG8-02 Low (FIXTURE-ID in a DEFAULT has no target table though written to rows; FIXTURE-ID rows not exhaustive: COPY data, MERGE, SELECT INTO, CREATE TABLE AS); SG8-03 Low (no catch-all in DO/function bodies; EXECUTE leading-keyword test admits CREATE TABLE AS and ALTER ROLE/SYSTEM); SG8-04 Low (.gitlab-ci.yml has no rules/workflow, so no MR pipelines and the GitLab list is never built; merge-base failure on shallow clone undefined); SG8-05 Low (E1-044 AC8 Flyway fixture form unfixed, could be a column-less INSERT; section 3b asks and does not ask E1-044; lint-fixture roots not bounded to test roots); SG8-06 Low (TS-06 (i) stale --changed-files; row order; duplicate scenario; SPEC-001 item 2 fixed path; ASM-29 risk wording)
NEW_DOCUMENT_GAPS: none
CROSS_STORY_RWB-E1-044: Consistent with v14-7 for the lint fixtures (SPEC-010 migration-lint, T-044-20..22); AC8 Flyway fixture form unfixed (SG8-05)
CROSS_STORY_RWB-E1-042: Rev 8 section 12.3 identical to rev 7; Known-files row correct; guard form requested through the orchestrator
CROSS_STORY_RWB-E1-043: Revision 4 R4 owner RW-COMPLY and section 3.2 consistent
CROSS_STORY_RWB-E1-001: Consistent; DF-REF-156/-166 in the union; DF-REF-104 not
CROSS_STORY_RWB-TE-001/-002/-003: Consistent (local merge gate on the branch; UT-15 synthetic path; ContractFixtures Java)
BLOCKING: YES under D-RUN-09 (Low-only failure is not accepted by the orchestrator; REVIEW_GATE_WARNING would otherwise apply)
NEXT_STEP: The orchestrator triages SG8-01..SG8-06. Under D-RUN-09 the Technical Specifier fixes all six, then requests spec gate round 9 (review/spec-gate-review-9.md). This review does not start the Implementation Planner.
```

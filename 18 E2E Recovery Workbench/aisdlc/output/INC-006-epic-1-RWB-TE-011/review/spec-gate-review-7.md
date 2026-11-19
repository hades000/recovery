# Spec gate review, round 7: RWB-TE-011 PDPA lint for code, tests and logs

| Field | Value |
|---|---|
| RUN_ID | `INC-006-epic-1-RWB-TE-011` |
| Gate | Spec gate, re-review round 7 (Compliance Reviewer, independent of the author) |
| Earlier rounds | Round 1 `review/spec-gate-review.md` (FAIL, 2 Medium, 5 Low); round 2 `-2.md` (FAIL, 1 Medium, 1 Low); round 3 `-3.md` (FAIL, 2 Low); round 4 `-4.md` (FAIL, 3 Medium, 1 Low) with `document-gaps-4.md`; round 5 `-5.md` (FAIL, 1 Medium, 3 Low) with `document-gaps-5.md`; round 6 `-6.md` (FAIL, 0 Medium, 4 Low: SG6-01..SG6-04) |
| Reviewed | `specify/spec.md` (SPEC-TE011-001..018, revised 18 Nov 2026 after round 6), `assumptions.md` (ASM-TE011-01..27), `document-gaps.md` (DGL-01..15), `shared-updates.md` (§1–§5, including §3b), `gate-response.md` ("Gate response — round 6"), `compliance-validation.md`, `agent-run-log.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `evidence/`; the `*.run6.*` copies for comparison |
| Direction checked | The round-6 triage came from the orchestrator (Claude Code), event 2026-11-18T01:02 (`AI-SDLC-BUILD-LOG.md` line 200), not from a human. D-RUN-06, -07, -08, -09, -15, -17 (`AI-SDLC-BUILD-LOG.md` §1) |
| Cross-story input (read only) | RWB-E1-044 spec v14-4 (`output/INC-001-epic-1-RWB-E1-044/specify/spec.md`: rules L-FIX-LINE2, L-FIX-NO-BASE, L-LEX, L-SEARCH-PATH; tests T-044-20, T-044-21, T-044-22 and its case tables); RWB-TE-001 v4 (`INC-002`); RWB-E1-042 spec revision 5 (`INC-003`, §12.3 migration steps 1–8, SPEC-RWB-E1-042-006, -027); RWB-TE-002 (`INC-004`); RWB-TE-003 (`INC-005`, SPEC-RWB-TE-003-011, -020, -021, test resources `contract/`); RWB-E1-043 (`INC-008`, revision 3 backup `shared-updates.run3.md` and the current revision 4 of 01:24: GAP-38, open item R4, §3.2); RWB-E1-001 (`INC-009`, SPEC-RWB-E1-001-001/-002 T1–T11, `evidence/is_personal_union_v4.tsv`); `AGENTS.md` §3.7, §4.6; decision register D-RCV-28 |
| Checked against | Physical Schema v6 copy (`infra/postgres/schema/03-recovery-physical-schema-v6.sql`); `backend/src/main/resources/application.yaml` (`rwb.flyway.location`); today's tree (`find` for `*.sql`; migration folder holds `README.md` only) |
| Method | Independent quote-aware split of the PS v6 copy in the reviewer scratchpad (`python -I`, prints keywords and counts only): 4,070 statements and 4 dollar-quoted bodies, each statement classed against the four classes of SPEC-TE011-008. A parse of the PS v6 `sys_fields` seed for the rows that describe the columns of `sys_fields`, `sys_objects`, `data_product` and `lov_value`, and for `reviewer_name`. A read of every order-1–5 specification for the SQL and fixture files it adds. Greps of `specify/` for e-mail addresses and runs of 9 or more digits. Both contracts parsed as JSON |
| Date | 2026-11-18 |
| Reviewer | Compliance Reviewer (agent) |

## 1. Result

**Overall status: FAIL**

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 1 |
| Low | 3 |

**Round 6.** SG6-01, SG6-02, SG6-03 and SG6-04 are resolved as the orchestrator's triage directed.
Each was checked against `spec.md` and the other artefacts, not against `gate-response.md` alone. No
finding from rounds 1–5 has reopened. The corrected "Known files" reading (SG6-01 fix 4) has two errors
of fact. They are raised as new findings because they rest on content of other stories' specifications
that round 6 did not examine: SG7-01 (RWB-E1-044 test fixtures) and SG7-02 (RWB-E1-042 step 3).

**The orchestrator's round-6 triage is applied soundly:**

- **SG6-01.** The four statement classes are in SPEC-TE011-008. Unrecognised forms and DML in a `DO` body
  fail closed as findings, consistent with SG5-03. The specifier followed the triage rather than the
  reviewer's "skip" suggestion, and it says so. The new SPEC-TE011-018 accepts a finding in a merged
  migration only through a later corrective migration under the same story key that names the original
  on line 2. This is consistent with `AGENTS.md` §3.7 and §4.6, D-RCV-28, and RWB-E1-044 L-FIX-LINE2 and
  L-FIX-NO-BASE. The naming regex matches the lower-case `V<seq>__rwb_e1_0nn_<name>.sql` names that
  RWB-E1-042, -043 and -001 use. TS-TE011-06 (a)–(j) and TS-TE011-07 test it. `shared-updates.md` §3b
  asks the orchestrator to pass the rules to the planners of orders 1–5.
- **SG6-02.** No root or exclusion can leave out the migration folder. Real files and two probe paths are
  tested; T12 gives exit 2; `PDPA-SCOPE:` lines print the exclusions with file counts; the unit row
  "Scan scope" covers each case, including an empty folder.
- **SG6-03.** The dictionary scope of TS-TE011-01 is stated: the PS v6 copy, then the synthetic rows. The
  reviewer confirmed that PS v6 has non-personal `sys_fields` rows for every column of `sys_fields`
  (including `owner_role`, `source_system`, `description`, `field_name`), `sys_objects`, `data_product`
  (including `owner_role` and `owner_user_id`) and `lov_value` that the test uses. `reviewer_name` occurs
  in no PS v6 row, so the negative variant does give an unambiguous name on an undescribed pair.
- **SG6-04.** ASM-TE011-22 is corrected. D-RUN-15 is cited, and OPEN-NEW-TE011-2, -3 and §3a are
  withdrawn. OPEN-NEW-TE011-7 is withdrawn into RWB-E1-043 open item R4, and the orchestrator is asked to
  keep the single item. The RWB-E1-064 note follows §3.2.

**PS v6 against the statement classes.** All 4,070 PS v6 statements fall in class 1 or 2, or are
function definitions whose bodies hold no DML. These are `CREATE EXTENSION`, `CREATE SCHEMA`, `SET`,
`CREATE TABLE`, `CREATE [UNIQUE] INDEX`, `ALTER TABLE`, `CREATE [OR REPLACE] VIEW`,
`CREATE OR REPLACE FUNCTION`, `CREATE TRIGGER`, `COMMENT ON`, named-column `INSERT … VALUES` and
`INSERT … SELECT`. RWB-E1-001's baseline migration, which carries PS v6 lines 16–6130 with T1 removing
`SET search_path`, therefore raises no `(statement not recognised)` and no `(DML in procedural body)`
finding.

The four new findings:

- **SG7-01 (Medium).** RWB-E1-044 (order 1) commits test-fixture SQL that it designs to be malformed or
  unusual. It merges before this lint and is scanned at this story's merge. Under this spec those files
  give exit 2 or findings, with no specified remedy. "Known files", state (1) and §3b say the opposite.
- **SG7-02 (Low).** RWB-E1-042's guarded constraint additions are `DO` blocks. "Known files" and
  ASM-TE011-27 omit them, and the class 3 rule for direct DDL in a `DO` body is ambiguous. The class lists
  also leave four smaller forms unplaced or unchecked.
- **SG7-03 (Low).** SPEC-TE011-018 and SPEC-TE011-003 leave four points undefined: the target table of a
  FIXTURE-ID finding, the scope of the corrective-file rules, the changed-file list in this repository's
  local merge, and the source of the expected migration path.
- **SG7-04 (Low).** Stale or over-claimed text in the run log, DGL-08/CLAR-004, the R4 owner wording and
  two "already passed" claims.

## 2. Disposition of round-6 findings

| Finding | Severity | Disposition | Evidence (checked against the spec, not against `gate-response.md` alone) |
|---|---|---|---|
| SG6-01 Earlier stories merge SQL before this lint; forms unspecified; no remedy in a merged migration | Low | **Resolved** as triaged. The corrected "Known files" reading has two errors of fact, raised as SG7-01 and SG7-02 (new evidence, not a reopen). | **Fix 1, statement classes.** SPEC-TE011-008 "SQL statement classes" 1–4. Class 1 accepts `ON CONFLICT … DO NOTHING`/`DO UPDATE SET`, where a literal is a position and `EXCLUDED.c` is not, plus `RETURNING`, `WHERE NOT EXISTS`, a read-only `WITH` and `UPDATE … FROM … WHERE`. Class 2 is non-position forms, which FIXTURE-ID still scans. Class 4 is `(statement not recognised)`. Unit row "SQL statement classes", one scenario per tail, on a non-`sys_fields` table. The triage overrode the reviewer's "skip, never exit 2" with "fail closed as a finding", and the spec follows the triage. **Fix 2, `DO` DML.** `(DML in procedural body)`; function bodies are checked as position forms (`NEW.c` is not a literal); TS-TE011-07; ASM-TE011-27. **Fix 3, states.** State (2) reads "orders 1–8"; state (1) requires the implementation run to list each order-1–5 file with its result. **Fix 4, remedy.** SPEC-TE011-018 conditions (a)–(e), the `corrected by` notice, exit 2 for an unknown named file, C scanned like any migration, no allow entry or exclusion. It is also in SPEC-TE011-011, -012, -013, T11, the status matrix, the coverage row (32 rows), CLAR-012 and ASM-TE011-26. "Known files" and the ASM-TE011-25 risk are rewritten. **Fix 5, note.** `shared-updates.md` §3b. |
| SG6-02 A scan exclusion can cover the migration folder | Low | **Resolved.** One residual point (the source of the expected path) is in SG7-03 item 4. | SPEC-TE011-003 "The migration folder cannot be left out": `dictionary.migrationFolder` must be the Flyway location. Every real file and the probes `<folder>/probe.sql` and `<folder>/sub/probe.sql` are tested against the roots and exclusions. A root that misses one, or an exclusion that matches one, gives exit 2 with `scan configuration excludes the migration folder: {config key}`. The real-file test catches an exclusion such as `**/V*.sql` that the probes would miss. `PDPA-SCOPE:` lines print paths and counts only. T12, SPEC-TE011-012, -015, the status matrix, the contract ("excludedMigrationFolderLine", "scopeLine") and the unit row "Scan scope" all agree. |
| SG6-03 TS-TE011-01 dictionary set-up unstated | Low | **Resolved.** | TS-TE011-01 "Dictionary scope": PS v6 baseline, then the synthetic rows. The test asserts 0 undescribed seed columns before it runs. The reviewer's parse confirms the PS v6 rows for the columns used (see §1). The negative variant `lov_value (…, reviewer_name)` gives exactly 1 finding. It is valid because no PS v6 row is named `reviewer_name`. |
| SG6-04 Stale text after D-RUN-15 and RWB-E1-043 revision 3 | Low | **Resolved.** A drift caused by RWB-E1-043 revision 4 (published 01:24, after this run) is in SG7-04. | (1) ASM-TE011-22 risk: "RWB-E1-043 does not guard unmarking", and the guard is the RWB-E1-064 seam under §3.2, with R4 deciding. (2) "Scope decisions" rows A-07 (a)/(b) and "Out of scope" cite D-RUN-15. OPEN-NEW-TE011-2, -3 and §3a are withdrawn. `compliance-validation.md` §4 row 1 reads "A-07 assigned to RWB-TE-003". The run-log Steps row is marked superseded. (3) SRC-25, the classification section, SPEC-TE011-017 (RWB-E1-043 row: GAP-38 corrected, §3.2 item 5), DGL-13, T8, CLAR-010, the coverage row and the contract cite R4. OPEN-NEW-TE011-7 is withdrawn into R4, and the orchestrator note keeps a single item and carries this story's question. The RWB-E1-064 note matches §3.2 item 3 (422 MSG-P1-002 "is_personal cannot be changed by a load"; `apply` and `onRolledBack` never write it). |

**Regression check, rounds 1–5.** No finding has reopened. The reviewer re-checked:

- SG-01 (precondition 2 "Partly met"; 9 Restricted fields listed);
- SG-03 (`is_active` fail-safe);
- SG-04 (`infra/postgres/schema/**` the only `infra` exclusion);
- SG2-01 ("add marks only"; 14 of 18; 509);
- SG4-01 ((object, field) matching; no allow entry on a migration; point in time);
- SG4-03 (R1/R2 reader; fail closed);
- SG5-01 (per-pair resolution);
- SG5-03 (`(columns not named)`).

The counts 18 / 14 / 509 / 523 / 1,366 / 17 / 9 / 526 / 390 / 71 still agree across `spec.md`,
DGL-01, OPEN-NEW-TE011-1 and `assumptions.md`. The coverage table has 32 rows (`TOTAL_RULES: 32`).

## 3. New findings

### REVIEW-TE011-SG7-01: RWB-E1-044's lint fixtures, merged at order 1, give exit 2 or findings at this story's merge; "Known files", state (1) and §3b claim they pass (Medium)

- **Affects:**
  - SPEC-TE011-008: "Known files", row 1, "Scanned as test fixtures, against the full dictionary";
  - SPEC-TE011-016 state (1), "0 findings";
  - SPEC-TE011-017 orders 1–5 row;
  - SPEC-TE011-018 "Unknown file";
  - T3;
  - `shared-updates.md` §3b item 5 and its closing line, "By their specifications, the files of orders 1–5 already meet these rules";
  - ASM-TE011-25 and -27, risk columns.
- **Evidence:**
  1. **Scan roots.** SPEC-TE011-003 class "Tests and fixtures" scans `backend/src/test/**/*.{java,sql,json}`
     and `backend/src/test/resources/**`. RWB-E1-044 (Build Sequence v6 order 1, merged before this story
     under D-RUN-06 and D-RUN-17) puts its lint fixtures under `backend/src/test/resources/migration-lint/`
     (E1-044 SPEC-RWB-E1-044-010). It puts its Flyway fixtures under
     `backend/src/test/resources/flyway-fixtures/`.
  2. **Malformed SQL by design.** E1-044 T-044-22 says "Each case is its own fixture file in its own
     folder". Its cases include:
     - N11, an unterminated literal: `INSERT INTO ${recoverySchema}.t (v) VALUES ('abc);`;
     - N12, an unterminated block comment: `/* not closed`;
     - N13, an unterminated dollar body: `DO $q$ BEGIN NULL; END;`.

     E1-044's L-LEX expects these files to be unterminated. This spec's T3 makes a "source file the lint
     cannot parse" exit 2. The quote-aware splitter that SPEC-TE011-008 shares with the reader cannot
     close these tokens. Exit 2 cannot be excused by an allow entry (SPEC-TE011-011 excuses findings only).
  3. **Forms outside the classes.** E1-044 T-044-20 makes L-SEARCH-PATH fail "each form in the SPEC-007
     table". That table includes `ALTER ROLE … SET search_path`, `ALTER DATABASE … SET search_path` and
     `ALTER FUNCTION … SET search_path`. None of `ALTER ROLE`, `ALTER DATABASE` or `ALTER FUNCTION` is in
     class 2, which lists `ALTER` only for TABLE, INDEX, VIEW, MATERIALIZED VIEW, SEQUENCE, SCHEMA, TYPE,
     DOMAIN, EXTENSION and TRIGGER. Fixture files that hold them give `(statement not recognised)`
     findings. The fixtures are permanent, but an allow entry must expire (BR6). Allow-listing them would
     therefore fail the pipeline again at each expiry date.
  4. **Reader precedence on test SQL.** E1-044 T-044-21 holds
     `INSERT INTO ${recoverySchema}.sys_fields (source_field) VALUES ('public.account.account_key');`.
     That is an INSERT on `sys_fields` without `field_id`, `object_name` or `field_name`, which R1
     requires. SPEC-TE011-008 says twice that "When a statement targets `sys_fields`, the reader's exit 2
     (SPEC-TE011-001) takes precedence". It does not limit this to files the reader reads: the baseline,
     the migration folder and the configured dictionary files. Read literally, this test fixture gives
     exit 2. T-044-21 may hold this text in Java source rather than in a `.sql` file. In that case the
     ambiguity remains, but this file does not trigger it.
  5. **The only working escape is unspecified.** An exclusion of `backend/src/test/resources/migration-lint/**`
     is allowed, because only the migration folder is protected. It would also remove those files from
     FIXTURE-ID, and the spec neither names it nor tests it. The implementer would have to invent the
     remedy at this story's merge.
  6. **Why Medium.** This is a predictable failure of this story's own merge condition ("Done when … zero
     findings"; exit 0 in state (1)). It follows from an earlier story's specification as it stands. The
     spec states the opposite in three places. Round 6 rated SG6-01 Low because the problem was "not a
     known failure". This one is.
- **Required fix:**
  1. Limit the reader-precedence rule (exit 2 for a `sys_fields` target) to the files the reader reads.
     In other scanned `.sql` files, a `sys_fields` statement is checked as a position form or classed like
     any other statement. Limit SPEC-TE011-018, including "Unknown file", to files in the recovery
     migration folder. Add a unit scenario for each.
  2. Specify how a scanned test `.sql` file outside the migration folder is handled when it is malformed
     on purpose or uses a form outside classes 1–3. Never let it give exit 2. One option: a configured,
     code-owner-reviewed "lint fixture" root class that gets FIXTURE-ID only, applied to the raw text,
     like the self-scan of `tools/pdpa-lint/**`. It is printed in `PDPA-SCOPE:` with its file count, and
     the SG6-02 check forbids it from covering the migration folder. Put its default
     (`backend/src/test/resources/migration-lint/**`) in SPEC-TE011-003 and ASM-TE011-05.
  3. Correct the RWB-E1-044 row of "Known files", state (1), the orders 1–5 row of SPEC-TE011-017,
     `shared-updates.md` §3b item 5 and its closing claim, and the ASM-TE011-25 and -27 risks.
  4. Add a system test with a fixture tree that mirrors E1-044 T-044-22 N11–N13, an
     `ALTER ROLE … SET search_path` fixture and a test-SQL `sys_fields` INSERT. Assert exit 0 with the
     default configuration, and assert that FIXTURE-ID still fires on a run-time-built ID placed in such
     a file.

### REVIEW-TE011-SG7-02: RWB-E1-042's guarded constraint `DO` blocks are left out of "Known files"; class 3 is ambiguous for direct DDL; four smaller class gaps (Low)

- **Affects:** SPEC-TE011-008 ("SQL statement classes" 2–4; "Known files" RWB-E1-042 row); ASM-TE011-27; `shared-updates.md` §3b item 1; TS-TE011-07; unit row "SQL statement classes".
- **Evidence:**
  1. **Step 3 omitted.** RWB-E1-042 §12.3 step 3 makes its constraint additions as "`DO` blocks testing
     `pg_constraint` by name in `${recoverySchema}`". There are 16 constraints, each added if absent. Step 8
     is a separate self-check `DO` block. "Known files" lists `ALTER TABLE … ADD CONSTRAINT` as a top-level
     form and "a self-check `DO` block that only reads and raises". ASM-TE011-27 says "RWB-E1-042's `DO`
     block only reads". The step-3 blocks run DDL, and neither text mentions them.
  2. **"Such DDL" is ambiguous.** Class 3 says a `DO` body that holds only reads, `RAISE`, `ASSERT "or
     such DDL"` gives no finding. "Such" refers to the literal `EXECUTE 'CREATE …'` of the sentence before.
     A plain `IF NOT EXISTS (…) THEN ALTER TABLE … ADD CONSTRAINT …; END IF;` in a `DO` body is the common
     guard form. It is neither a listed DML statement nor a literal `EXECUTE`. The text does not say it is
     allowed, and no test covers it.
  3. **The note and the spec disagree.** A guard written as `EXECUTE format('ALTER TABLE %I.… ADD
     CONSTRAINT …', …)` is DDL, but its argument is not a string literal, so the spec makes it a finding.
     §3b item 1 forbids only a "non-DDL `EXECUTE`", which a planner would read as allowing it. Once
     merged, such a finding could be cleared only by a corrective migration.
  4. **Smaller class gaps:**
     - (a) `ALTER FUNCTION`/`PROCEDURE` and `DROP FUNCTION`/`PROCEDURE` are in no class, so they are
       `(statement not recognised)`. A forward-only migration that replaces or removes a trigger function,
       such as RWB-E1-043's append-only triggers, needs them.
     - (b) `CREATE TABLE … AS` is a `CREATE TABLE` in class 2 and an example in class 4, but "each
       statement falls in exactly one class".
     - (c) "A `DEFAULT` or `CHECK` literal in DDL is a rule, not a row". Yet
       `ALTER TABLE t ADD COLUMN c … DEFAULT '<literal>'` writes the literal into every existing row, and a
       personal-column default is personal data in code. FIXTURE-ID sees it only if it matches an ID,
       mobile or e-mail pattern.
     - (d) The `DO` body list does not say whether `DELETE` or `TRUNCATE` inside a body is allowed. Both
       are class 2 at top level.
- **Required fix:**
  1. Correct the RWB-E1-042 row of "Known files" and ASM-TE011-27 to list the step-3 guard blocks. Say
     how each guard form is read.
  2. In class 3, state that direct DDL of the class-2 kinds, and `DELETE` or `TRUNCATE`, inside a `DO`
     body raise no finding. State whether a non-literal `EXECUTE` of DDL is a finding. Align §3b item 1
     with the result, and tell the RWB-E1-042 planner which guard form to use.
  3. Place `ALTER`/`DROP FUNCTION|PROCEDURE` (class 2) and `CREATE TABLE … AS` (one class only).
  4. Treat a non-`NULL` `DEFAULT` literal on a resolved personal pair as a FIXTURE-FIELD position.
  5. Add unit scenarios: a `DO` guard with direct `ALTER TABLE … ADD CONSTRAINT` (no finding); a `DO`
     guard with `EXECUTE format(…)` (as decided); `DROP FUNCTION IF EXISTS` (no finding); `ADD COLUMN …
     DEFAULT` on a personal pair (finding). Add the direct-DDL guard to TS-TE011-07.

### REVIEW-TE011-SG7-03: SPEC-TE011-018 and SPEC-TE011-003 leave four points undefined (Low)

- **Affects:** SPEC-TE011-018 condition (d) and "Unknown file"; SPEC-TE011-013; SPEC-TE011-003 ("must resolve to that path"); ASM-TE011-26; `contracts/backend-apis.json` "correctiveMigration"; unit rows "Corrective migration" and "Scan scope".
- **Evidence:**
  1. **Target table of a FIXTURE-ID finding.** Condition (d) applies "for a finding with a target table".
     SPEC-TE011-018 includes FIXTURE-ID among the SQL rules. A FIXTURE-ID match can sit in a `--` comment,
     in `COMMENT ON` text, in a DDL default or in an `INSERT` value. The spec does not say which of these
     has a target table. For `COMMENT ON TABLE t`, reading `t` as the target would demand an `UPDATE`,
     `DELETE` or `TRUNCATE` on `t`, when the real correction is a new `COMMENT ON`.
  2. **Scope of the corrective-file rules.** Condition text says "a file C in the migration folder".
     "Unknown file" ("A `-- Fix:` line that names a file absent from the migration folder gives exit 2")
     has no such limit, so it could apply to test SQL that carries `-- Fix:` lines. RWB-E1-044's
     L-FIX-LINE2 and L-FIX-NO-BASE fixtures are an example. This is covered by SG7-01 fix 1; it is recorded
     here so that the SPEC-TE011-018 text is changed too.
  3. **Condition (e) in this repository.** SPEC-TE011-013 builds `--changed-files` only in a GitLab merge
     request pipeline, and "In a branch pipeline the list is empty". In this repository no GitLab pipeline
     runs. The orchestrator merges locally on a green `./scripts/dev.ps1 test` (D-RUN-06; build-log
     triage 23:57 for RWB-TE-001). The `dev.ps1` entry point is only "Recommended for the plan".
     Locally, condition (e) is therefore never enforced: a story could add O and C in the same merge, and
     O would be "corrected" rather than fixed.
  4. **Expected migration path.** "`dictionary.migrationFolder` must resolve to that path, the recovery
     Flyway location", and the unit row expects exit 2 when it is "set to another path". The spec does not
     say where the expected value comes from. If it comes from `pdpa-lint.yaml`, one configuration change
     moves both. The source of truth in the repository is `rwb.flyway.location:
     classpath:db/modulemigration/recovery` in `backend/src/main/resources/application.yaml` (line 83).
  5. **Contract drift.** ASM-TE011-26 and the contract's "correctiveMigration" text require an `UPDATE`,
     `DELETE` or `TRUNCATE` without the spec's exception: "a finding with no target table … needs only (a)
     to (c)".
- **Required fix:**
  1. Define the target table for each finding kind. For FIXTURE-FIELD it is the position's table. For
     FIXTURE-ID it is the table of the `INSERT`/`UPDATE` holding the token, and none for a comment,
     `COMMENT ON` or DDL. Add unit scenarios.
  2. Limit "Unknown file" and the line-2 parsing to files in the recovery migration folder.
  3. Make the local entry point build the changed-file list from the merge base with the target branch,
     for example the added or modified files of `git diff --name-only develop-recovery...HEAD`. Make it a
     required part of SPEC-TE011-013, not a recommendation, so that the orchestrator's local merge check
     enforces (e). Test it.
  4. Name the source of the expected migration path: read `rwb.flyway.location` from `application.yaml`,
     or state a fixed tool constant and a test that it matches that property. Say what happens when the
     two disagree (exit 2).
  5. Align ASM-TE011-26 and the contract with condition (d) as written.

### REVIEW-TE011-SG7-04: Stale and over-claimed text (Low)

- **Affects:** `agent-run-log.md` header; DGL-08 "How"/"Why"; CLAR-004; SPEC-TE011-017 lead-in and orders 1–5 row; SPEC-TE011-008 "Known files" last paragraph; SRC-25, "Personal data classification used", OPEN-NEW-TE011-7 and DGL-13 (R4 owner); compliance-validation `Independent gate` row (round 6 wording).
- **Evidence:**
  1. **Run log.** The `agent-run-log.md` header still reads "Status (current): Spec remediated after round
     5; spec gate round 6 requested" and "25 assumptions (ASM-TE011-01..25) and 11 clarification rows
     (CLAR-001..011)". The set now has ASM-TE011-01..27 and CLAR-001..013, and round 7 is requested. The
     run-6 section is correct. This is the kind of header staleness that SG5-04 fixed.
  2. **DGL-08 and CLAR-004.** Both still give "an allow-list entry (BR6)" as the exception route for
     non-text personal fields. In the migration folder no allow entry is possible (SPEC-TE011-011), so
     the only compliant value there is `NULL`. SPEC-TE011-008 says this indirectly ("Outside the migration
     folder it can be allow-listed"). The gap row and the CLAR do not. Under the protective union this
     matters:
     - `parameter_value.author_user_id` (DF-REF-156, uuid, NOT NULL per RWB-E1-042 §12) and
       `reference_version.author_user_id` (DF-REF-166) become personal non-text pairs;
     - a later migration that seeds such a row can never pass, except through a column reference;
     - no story is known to need this today: RWB-E1-043 SPEC-029 seeds catalog rows only.
  3. **"Already passed".** SPEC-TE011-017 opens with "The orchestrator has already passed each one to the
     owning remediation run". "Known files" ends with "The planners of orders 1–5 have been asked, through
     the orchestrator". The build log records no such hand-off after the 01:02 triage. §3b is a request,
     not an action taken.
  4. **R4 owner.** This spec calls R4 "owner RW-COMPLY with the data architect", citing RWB-E1-043
     revision 3. That matches E1-043's `shared-updates.run3.md`. E1-043 revision 4 (01:24) now lists R4's
     owner as "RW-COMPLY" alone, and its §3.2 item 2 says no role code exists for a data architect.
     SRC-25 also still cites revision 3.
- **Required fix:**
  1. Update the run-log header: current status, 27 assumptions, 13 CLARs, round 7 requested.
  2. Revise DGL-08 and CLAR-004: in the migration folder a non-text personal value must be `NULL`, and
     the allow list does not apply. Add one sentence in SPEC-TE011-008 that a NOT NULL non-text personal
     column cannot be seeded by a migration. Add a line to `shared-updates.md` §3 or §3b so that the owner
     of such a seed raises it before planning.
  3. Change both "already passed" and "have been asked" sentences to "`shared-updates.md` §3b asks the
     orchestrator to pass …".
  4. Cite RWB-E1-043 revision 4 in SRC-25 and give R4's owner as "RW-COMPLY" wherever this spec names it.

## 4. Other checks

| Check | Result |
|---|---|
| Personal data in the artefacts | None found. No e-mail address and no run of 9 or more digits in `specify/` outside the `*.run*` backups. Only synthetic values are used (`SYN-LAST-0001`, `TESTNAME`, `RW-DATASTEW`, `<text>` placeholders). The reviewer's script printed keywords and counts only. |
| Secrets | None. |
| Contracts | Both parse as JSON. The exit codes, `columnsNotNamedField`, `statementNotRecognisedField`, `dmlInProceduralBodyField`, the four notice lines, `scopeLine`, `excludedMigrationFolderLine` and `unknownCorrectiveLine` match SPEC-TE011-003, -008, -012 and -018. "correctiveMigration" omits the no-target-table case (SG7-03). `NO_API_CHANGE` is consistent with the status matrix. |
| Authorization and audit | Unchanged and appropriate for a build tool: no run-time path; change control through code owners (SPEC-TE011-014). The corrective-migration acceptance relies on code-owner review for correctness, and the spec says so ("Limit"). |
| Unit Test Applicability | Compliant. The front end is `NOT_APPLICABLE` with evidence. The tool back end is `REQUIRED` at 80% on JaCoCo LINE, BRANCH, METHOD and INSTRUCTION. SG7-01..SG7-03 add scenarios. |
| Evidence | No round-6 script was added. The new claims rest on the specifications of orders 1–5 (SRC-30), which the reviewer read directly (§1, SG7-01, SG7-02). The reviewer's PS v6 class check supports the RWB-E1-001 reading. |
| Run decisions | D-RUN-06 (merge in build order) and D-RUN-17 (TE-001 before E1-044) are applied in "Known files". D-RUN-07: no number is fixed, and test fixtures use concrete names only. D-RUN-08: the RWB-E1-064 seam and RWB-E1-001 obligations stand; no dependency on a later story. D-RUN-09 is applied. D-RUN-15 is applied. The triage is attributed to the orchestrator (Claude Code), with no human disposition claimed. |
| Data classification (pdlc stop condition) | The classification source, the residual risk, both RWB-E1-001 outcomes and the load-route limit are visible. No open data-classification blocker belongs to this story. |
| Document gaps | No new document gap. The findings concern this spec and other runs' specifications, not the document set. `review/document-gaps-7.md` is not written. |

## 5. Gate output

```text
REVIEW_STATUS: FAIL
REVIEW_COUNTS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 1] [LOW: 3]
ROUND_6_DISPOSITION: SG6-01 Resolved as triaged by the orchestrator (statement classes, DO-body DML fail closed, states, SPEC-TE011-018 corrective migration, shared-updates 3b); its corrected Known-files reading has errors raised as SG7-01/SG7-02. SG6-02 Resolved (residual path source in SG7-03). SG6-03 Resolved (PS v6 describes the seed columns; reviewer_name absent from PS v6). SG6-04 Resolved (R4 owner drift from E1-043 revision 4 in SG7-04)
ROUND_1_5_DISPOSITION: all remain Resolved; no regression
NEW_FINDINGS: SG7-01 Medium (RWB-E1-044 lint fixtures, merged at order 1, are unterminated or use ALTER ROLE/DATABASE/FUNCTION; this lint gives exit 2 or findings at its own merge; reader precedence and Unknown-file rule not limited to the files they concern); SG7-02 Low (E1-042 step-3 guard DO blocks omitted; direct DDL in DO bodies ambiguous; 3b EXECUTE wording; ALTER/DROP FUNCTION, CREATE TABLE AS, DEFAULT literal, DELETE in DO); SG7-03 Low (FIXTURE-ID target table; corrective-rule scope; changed-file list in the local merge; source of the expected Flyway path; contract and ASM-26 drift); SG7-04 Low (run-log header; DGL-08/CLAR-004 allow-list route in migrations; "already passed" claims; R4 owner per E1-043 revision 4)
NEW_DOCUMENT_GAPS: none
CROSS_STORY_RWB-E1-001: Consistent. All 4,070 PS v6 statements are in classes 1-2 or are DML-free function bodies, so its baseline migration raises no class-3/4 finding; T10 INSERT literals; owner_user_id NULL
CROSS_STORY_RWB-E1-044: Conflict (SG7-01): T-044-22 N11-N13 unterminated fixture files and T-044-20 search_path forms under backend/src/test/resources/
CROSS_STORY_RWB-E1-042: Step-3 constraint guards are DO blocks (SG7-02); seed author_user_id gives a T7 notice at RWB-E1-001's merge, as stated
CROSS_STORY_RWB-E1-043: Revision 4 keeps GAP-38 corrected, R4 (owner RW-COMPLY) and §3.2; owner wording drift (SG7-04)
BLOCKING: YES (Medium finding SG7-01 blocks the Implementation Planner)
NEXT_STEP: The orchestrator triages SG7-01..SG7-04. Under D-RUN-09 the Technical Specifier fixes all four, and the Low ones too, then requests spec gate round 8 (review/spec-gate-review-8.md). This review does not start the Implementation Planner.
```

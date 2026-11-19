# Compliance validation — RWB-TE-011 specification (specifier self-check)

| Field | Value |
|---|---|
| RUN_ID | `INC-006-epic-1-RWB-TE-011` |
| Artifact | `output/INC-006-epic-1-RWB-TE-011/specify/spec.md` (SPEC-TE011-001..018) |
| Prepared by | Technical Specifier, 2026-11-17; revised 2026-11-18 after spec gate round 9 |
| Purpose | Checklist of `.github/rules/specification-execution-gates.md` "Spec Validation Checklist" and the banking controls, before the gate |
| Independent gate | Compliance Reviewer, rounds kept in `output/INC-006-epic-1-RWB-TE-011/review/`: `spec-gate-review.md` (round 1), `spec-gate-review-2.md` (round 2), `spec-gate-review-3.md` (round 3), `spec-gate-review-4.md` (round 4), `spec-gate-review-5.md` (round 5: FAIL, 1 Medium, 3 Low), `spec-gate-review-6.md` (round 6: FAIL, 0 Medium, 4 Low), `spec-gate-review-7.md` (round 7: FAIL, 1 Medium, 3 Low), `spec-gate-review-8.md` (round 8: FAIL, 0 Medium, 6 Low), `spec-gate-review-9.md` (round 9: FAIL, 0 Medium, 4 Low, remediated 18 Nov 2026); round 10 `spec-gate-review-10.md`; responses in `specify/gate-response.md` |

## 1. Banking and domain controls against source requirements

| Control | Source | Where in the spec | Result |
|---|---|---|---|
| No personal data in code, test fixtures or logs | NFR-054 (NFR Specification v3); `AGENTS.md` §4.7; BS-4.6 | SPEC-TE011-004..-009, -013 | Specified as a blocking pipeline job |
| Synthetic data in development | NFR-045; `AGENTS.md` §3.9; testing standards §2 | SPEC-TE011-008 (`SYN-` prefix), -009 (ID/mobile/e-mail) | Specified |
| Masking by role not bypassed through logs | REQ-RDF-010, REQ-ACA-005 (Business Requirements Program v4 §6.7, §6.9); CTL-11 (Controls Catalog v3) | SPEC-TE011-004..-007, -010 | Specified; run-time masking stays in RWB-E1-037 |
| Classification owned by Compliance, not by code | DL26 (Decision Log v10); story BR1 | SPEC-TE011-001, -015 | Specified; classification differences recorded as DGL-01, not resolved by this stage |
| Coverage claim matches the route of later changes | Decision Log v10 D-RCV-29; story §13, §17 | Spec "Personal data classification used", SPEC-TE011-001, -016, -017 | Narrowed: committed SQL, fixtures and logs against the dictionary as seeded and changed by migrations; run-time loads are not policed. Protecting marks on load is a seam owned by RWB-E1-064, with the decision in RWB-E1-043 open item R4, owned by RW-COMPLY (DGL-13) |
| Classification applied per entity and field | Inventory v4 sheet Fields; `sys_fields.object_name` | SPEC-TE011-008 | Fixtures matched by (object, field) where the dictionary describes the pair; an object or field outside the dictionary falls back to the unambiguous-name rule; log rules stay name-based (fail-safe) (DGL-14) |
| No fixture position skipped silently | Story BR3; review SG5-01, SG5-03 | SPEC-TE011-008; T6, T9; TS-TE011-04, -05 | Unresolved positions: finding (unambiguous name or API personal name) or notice (ambiguous). SQL with no named column: finding `(columns not named)` |
| Inconsistent API personal-data marks read protectively | API Specification v4 `Interaction.summary` vs `InteractionRequest`/`TimelineItem.summary`; DF-INT-011 | SPEC-TE011-002, -008; ASM-TE011-24 | Unmarked `summary` properties treated as personal (DGL-15; OPEN-NEW-TE011-8) |
| The lint never discloses the value it finds | Story BR7; §17 | SPEC-TE011-012; every TC asserts it | Specified |
| Exceptions are time-boxed and owned | Story BR6; §17 | SPEC-TE011-011 | Specified; invalid entry fails closed |
| Change control on lint configuration | Story §10; L-RCV-12 | SPEC-TE011-014 | Specified; depends on RWB-TE-002 |
| Fails closed on missing input or on a dictionary statement it cannot read | ASM-TE011-03 | SPEC-TE011-001, status matrix, T4 | Specified; one unit scenario per unsupported form |
| No database read; files only | Story §13, §17 | SPEC-TE011-001, Backend Specification | Specified |
| Merged migrations are never edited; a finding in one is remedied only by a corrective migration | `AGENTS.md` §3.7, §4.6; D-RCV-28; review SG6-01 | SPEC-TE011-018; T11; TS-TE011-06 | Specified: the corrective file names the original on line 2 and keeps its story key; the lint checks order, key, naming, target table and the changed-file list; no allow entry or exclusion |
| The migration folder cannot be left out of the scan | Story §17 (configuration, not code); review SG6-02 | SPEC-TE011-003, -015; T12; unit row "Scan scope" | Specified: an exclusion matching, or roots missing, any file or probe path in the folder gives exit 2; exclusions in force are printed with file counts |
| Test SQL that is malformed on purpose never blocks the merge, and is still scanned for real identifiers | Review SG7-01; RWB-E1-044 T-044-20..22 | SPEC-TE011-003 "Lint fixtures"; T13; TS-TE011-08 | Specified: lint-fixture class (default `backend/src/test/resources/migration-lint/**`), FIXTURE-ID only on the raw text, never exit 2, cannot cover the migration folder; reader precedence and corrective rules limited to their own files |
| Corrective acceptance is enforced where merges happen | Review SG7-03, SG8-01, SG8-04; D-RUN-06 | SPEC-TE011-013, -018; T14; TS-TE011-09 | Specified: changed-file list from `git merge-base` and `git diff` in GitLab branch pipelines (full history) and in `scripts/dev.ps1 test`; a missing target or no merge base gives exit 2; condition (e) applies to every finding where the list is built (a change into `develop-recovery` from a branch that is not protected) and is not evaluated elsewhere, so a promotion never fails for lack of a list; migration folder read from `rwb.flyway.location` |
| Unrecognised SQL fails closed | Story BR3; review SG5-03, SG6-01 | SPEC-TE011-008 "SQL statement classes"; T10; TS-TE011-07 | Specified: four statement classes; anything else, and any statement in a `DO`, function or procedure body that the class-3 rules do not list, is a finding |

## 2. Spec Validation Checklist (specification-execution-gates.md)

| # | Check | Result |
|---|---|---|
| 1 | spec.md and this file re-read | Done |
| 2 | Traceability matrix updated with unique SPEC IDs | Not edited (RUN-BRIEF rule 3); row 006 proposed in `shared-updates.md`. SPEC IDs are unique (`SPEC-TE011-001..018`). |
| 3 | Every SPEC entry linked to requirements | Done: Requirement-to-SPEC Logic Coverage, 32 rows (D-RCV-29 added in round 4; D-RCV-28 / `AGENTS.md` §3.7, §4.6 added in round 6), 0 BLOCKED |
| 4 | Screen table | Not applicable: no screen (story §15) |
| 5 | Design evidence source recorded | `figma/figma_report.md`: NONE, NOT_REQUIRED |
| 6 | Data models and contracts | `contracts/backend-apis.json` (NO_API_CHANGE plus the file/CLI contract) and `contracts/frontend-integrations.json` (NOT_APPLICABLE) parse as JSON; file contracts in spec "Data model" |
| 7 | API impact decision | `NO_API_CHANGE`, with evidence |
| 8 | Banking controls re-validated | Section 1 |
| 9 | Classification against requirement, trace chain, footprint | `NEW_STORY`: no trace chain (matrix row 006), no `tools/` folder, CI has 3 jobs |
| 10 | Zero unmapped business-rule lines | 7 flow steps, BR1–BR7, X1–X11, AC1–AC10, §10, §11, §12, §13, §17 and the upstream IDs all mapped |
| 11 | Intent, triggers, preconditions, constraints, transitions, exceptions preserved | Sections "User story intent", "Entry trigger and preconditions", "Status-transition matrix", "Exceptional-case behavior" |
| 12 | Gaps reported | `document-gaps.md` DGL-01..15, no blocker; `assumptions.md` ASM-TE011-01..29 |

## 3. Data protection scan of the outputs

- No real name, national ID, account, contract or mobile number, address or e-mail of a person appears in
  any file of this stage. The only identifiers are field names, synthetic placeholders (`SYN-LAST-0001`,
  `TESTNAME` from AC4) and the reserved-domain rule. Values that would match a FIXTURE-ID pattern are
  specified as generated at run time (SPEC-TE011-009).
- No secret, token or credential.

## 4. Points the gate should look at

| Point | Spec position |
|---|---|
| A-07 assigned to RWB-TE-003; `X-Correlation-Id` not built (D-RUN-15) | "Scope decisions on the orchestrator notes"; OPEN-NEW-TE011-2 and -3 withdrawn |
| Production classification narrower than the story Background | "Personal data classification used"; DGL-01 |
| TC-TE-011-11 cannot pass locally | SPEC-TE011-014; ASM-TE011-17 |
| Strict rule for DATE/NUMBER personal fields | SPEC-TE011-008; DGL-08 |
| Unresolved fixture positions (no object, or an object or field the dictionary does not describe): unambiguous names and API personal names enforced, ambiguous names reported as notices | SPEC-TE011-008; ASM-TE011-20, -24 |
| SQL with no named column fails closed as a finding | SPEC-TE011-008; ASM-TE011-25 |
| Point-in-time dictionary for migrations; no allow entry on a migration | SPEC-TE011-008, -011; ASM-TE011-21 |
| Cross-story obligations on RWB-E1-001, the RWB-E1-064 seam and RWB-E1-043's pipeline | SPEC-TE011-017; RWB-E1-043 open item R4 |
| SQL merged by orders 1–5 scanned at this story's merge; corrective migration as the only remedy | SPEC-TE011-008 "Known files", -016 state (1), -017, -018; `shared-updates.md` §3b |
| Statement classes; unrecognised forms and DML in `DO` blocks fail closed | SPEC-TE011-008; ASM-TE011-27 |
| Migration folder cannot be excluded | SPEC-TE011-003; T12 |
| TS-TE011-01 dictionary scope and negative variant | Test requirements, TS-TE011-01 |
| RWB-E1-044 lint fixtures in a FIXTURE-ID-only class; reader precedence and SPEC-TE011-018 limited to their files | SPEC-TE011-003, -008, -016, -018; ASM-TE011-28; TS-TE011-08 |
| `DO` guard forms, `DEFAULT` literal as a position, `ALTER`/`DROP FUNCTION`, `CREATE TABLE … AS` | SPEC-TE011-008; TS-TE011-07; ASM-TE011-27 |
| Target table per finding kind; local changed-file list; migration path from `application.yaml` | SPEC-TE011-003, -013, -018; ASM-TE011-26, -29; TS-TE011-09 |
| Condition (e) for every finding; FIXTURE-ID target tables (`DEFAULT`, `COPY`, `MERGE`, `SELECT … INTO`, `CREATE TABLE … AS`) | SPEC-TE011-018; ASM-TE011-26; TS-TE011-09 (f); unit row "Corrective migration" |
| Procedural-body catch-all; `EXECUTE` text classed as a top-level statement | SPEC-TE011-008 class 3; ASM-TE011-27; TS-TE011-07; `shared-updates.md` §3b item 1 |
| GitLab branch pipelines build the changed-file list (`GIT_DEPTH: 0`); no merge base gives exit 2 | SPEC-TE011-013; T14; TS-TE011-09 (g); ASM-TE011-29 |
| RWB-E1-044 Flyway-fixture route; §3b asks nothing of RWB-E1-044; lint-fixture roots bounded to test roots | SPEC-TE011-003; T12; TS-TE011-08; ASM-TE011-28; `shared-updates.md` §3b |
| FIXTURE-ID target table inside procedural bodies; `(DML in procedural body)` target tables | SPEC-TE011-018; unit row "Corrective migration"; contract |
| `EXECUTE format` placeholders (`%I` only as a name), literal `DEFAULT` in `EXECUTE` text, whole class-2 list in bodies, catch-all `COPY … FROM` | SPEC-TE011-008 class 3; ASM-TE011-27; TS-TE011-07; `shared-updates.md` §3b item 1 |
| Changed-file list built only for a change into `develop-recovery` from a non-protected branch; promotions never fail on (e) | SPEC-TE011-013, -018 (e); T11, T14, T15; TS-TE011-09 (e), (h)–(k); ASM-TE011-29 |

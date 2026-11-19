---
run_id: INC-006-epic-1-RWB-TE-011
story: RWB-TE-011
title: PDPA lint for code, tests and logs
stage: specify
spec_ids: SPEC-TE011-001..SPEC-TE011-018
change_type: NEW_STORY
ui_in_scope: NO
api_impact: NO_API_CHANGE
prepared: 2026-11-17
revised: 2026-11-18 (remediation after spec gate round 10)
author: Technical Specifier (agent run)
---

# Technical Specification — RWB-TE-011 PDPA lint for code, tests and logs

| Field | Value |
|---|---|
| Story | RWB-TE-011, E1, module P2 Integration, story type Enabler, priority Must (SRC-01 header) |
| RUN_ID | `INC-006-epic-1-RWB-TE-011` |
| Increment card | `aisdlc/docs/increments/INC-006-epic-1-RWB-TE-011.md` (build order 6 of 72, Build Sequence v6) |
| Upstream IDs | `REQ-RDF-010` (Business Requirements Program v4 §6.7), `REQ-ACA-005` (v4 §6.9), `NFR-054` and `NFR-045` (Non-Functional Specification v3), `CTL-11` (Controls Catalog v3); matrix grouping `BR-RWB-013` / `FR-RWB-013` |
| Depends on | RWB-TE-001 (implemented, Traceability Matrix v2.0 row 002). See SPEC-TE011-014 for the code-owner dependency on RWB-TE-002. Earlier stories whose SQL this lint scans at its merge (orders 1–5), and later stories that must meet this lint (RWB-E1-001) or own a seam next to it (RWB-E1-064, with RWB-E1-043's load pipeline), are in SPEC-TE011-017; this story depends on neither (D-RUN-08). |
| SPEC ID scheme | `SPEC-TE011-nnn`, story-scoped so that IDs do not collide with other runs' `SPEC-nnn` |
| Status | Revised after spec gate round 10 (`review/spec-gate-review-10.md`: FAIL, 0 Critical, 0 High, 0 Medium, 3 Low; SG10-01..SG10-03). The orchestrator's triage of round 9 (Claude Code as orchestrator, 2026-11-18T05:13; D-RUN-09: Lows are fixed, not accepted) allowed one further specifier round on a Low-only failure. Round 9 (FAIL, 4 Low; all found resolved in round 10) was remediated under that triage. Round 8 (FAIL, 6 Low; all found resolved in round 9) was remediated under the orchestrator's triage of 2026-11-18T04:54. Earlier rounds: 1 (FAIL, 2 Medium, 5 Low), 2 (FAIL, 1 Medium, 1 Low), 3 (FAIL, 2 Low), 4 (FAIL, 3 Medium, 1 Low), 5 (FAIL, 1 Medium, 3 Low), 6 (FAIL, 4 Low), 7 (FAIL, 1 Medium, 3 Low; all found resolved in round 8). Every change is mapped in `specify/gate-response.md`. Next: spec gate round 11 (`review/spec-gate-review-11.md`) |

## Sources

Every statement below cites one of these sources or a labelled assumption (`ASM-TE011-nn`, in
`assumptions.md`). `legacy/` means `<docset>/17 AI-First SDLC Repository v2/requirement/legacy/`.

| ID | Document, version, section | Path |
|---|---|---|
| SRC-01 | RWB-TE-011 story file v1, from Epic 1 Story Files v7 (28 Oct 2026) | `legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-011-pdpa-lint-for-code-tests-and-logs-v1.md` |
| SRC-02 | Technical Enabler Stories v7 (16 Nov 2026), section RWB-TE-011 | `legacy/04-user-stories/recovery-workbench-technical-enabler-stories-v7.md` |
| SRC-03 | Build Notes Technical Enablers v2, section RWB-TE-011 | `legacy/04-user-stories/recovery-workbench-build-notes-technical-enablers-v2.md` |
| SRC-04 | Story Defects Epic 1, Epic 2 and Enablers v4, rows RWB-TE-011 step 2 and step 4 | `legacy/04-user-stories/recovery-workbench-story-defects-epic-1-epic-2-and-enablers-v4-xlsx.md` |
| SRC-05 | Test Cases v7, tab Story test cases, TC-TE-011-01..11 | `legacy/09-testing-and-quality/recovery-workbench-test-cases-v7-xlsx.md` |
| SRC-06 | Physical Schema v6: `sys_fields` table and seed (column `is_personal`) | `legacy/06-data/recovery-workbench-physical-schema-v6.sql`; byte-identical repo copy `infra/postgres/schema/03-recovery-physical-schema-v6.sql` (verified with `cmp`, 17 Nov 2026) |
| SRC-07 | API Specification v4, property extension `x-personal-data: true` | `legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml`; identical repo copy `api/recovery-api-v4.yaml` (verified with `diff`) |
| SRC-08 | Personal Data Protection Design v2 (document table reads "Version 1, 28 October 2026"), §1, §4 | `legacy/10-policy-controls-and-compliance/recovery-workbench-personal-data-protection-design-v2-docx.md` |
| SRC-09 | Data Classification and Personal Data Inventory v4, sheet Fields | `legacy/06-data/recovery-workbench-data-classification-and-personal-data-inventory-v4-xlsx.md` |
| SRC-10 | Logical Data Model and Data Dictionary v8, sheet Fields, column "Personal data" | `legacy/06-data/recovery-workbench-logical-data-model-and-data-dictionary-v8-xlsx.md` |
| SRC-11 | Non-Functional Specification v3: NFR-045, NFR-052, NFR-054 | `legacy/03-requirements-and-specifications/recovery-workbench-non-functional-specification-v3-docx.md` |
| SRC-12 | Controls Catalog v3: CTL-11 | `legacy/10-policy-controls-and-compliance/recovery-workbench-controls-catalog-v3-xlsx.md` |
| SRC-13 | Business Requirements Program v4: REQ-RDF-010, REQ-ACA-005 | `legacy/03-requirements-and-specifications/recovery-workbench-business-requirements-program-v4-docx.md` |
| SRC-14 | Audit and Logging Design v2 (document table reads "Version 1"), §3, §6 | `legacy/05-technical-architecture/recovery-workbench-audit-and-logging-design-v2-docx.md` |
| SRC-15 | RWB-E1-065 story file v1 (Story Files v7), §13 ValueFactory, BR7, BR9 | `legacy/04-user-stories/.../rwb-e1-065-sandbox-database-with-synthetic-recovery-data-v1.md` |
| SRC-16 | RWB-TE-002 story file v1 (Story Files v7), §8 BR1–BR7 | `legacy/04-user-stories/.../rwb-te-002-code-owners-for-the-recovery-module-v1.md` |
| SRC-17 | D-RCV-35 ACE DB alignment, §3.3 Personal data | `aisdlc/docs/decisions/d-rcv-35-ace-db-alignment.md` |
| SRC-18 | Decision register: D-RCV-16, D-RCV-28 (migration names; corrective script keeps the story key, line 2 `-- Fix: <reason>`), D-RCV-50, L-RCV-03, L-RCV-12, L-RCV-13 | `aisdlc/docs/decisions/decision-register.md` |
| SRC-19 | Phase 0 standards audit, findings A-07, A-09, A-10 | `aisdlc/evidence/phase0-standards-audit.md` |
| SRC-20 | Backend context v2.0 §6–§7; backend standards v2.0 BS-1.5, BS-4.6, BS-7.2; testing standards v2.0 §1–§6 | `aisdlc/.github/contexts/` |
| SRC-21 | `AGENTS.md` §3.7 (migration naming and corrective script), §3.9, §4.4, §4.6 (a merged migration is never edited), §4.7, §6 (acceptance of a story with no business ACs, generalising D-RCV-16), §9; `README.md` "Decisions taken while setting this up" | repository root |
| SRC-22 | Decision Log v10, DL26 (retention and masking; owner Compliance) and D-RCV-29 (line 78: "Later dictionary changes are reference loads through RWB-E1-043") | `legacy/01-decisions-and-governance/recovery-workbench-decision-log-v10-xlsx.md` |
| SRC-23 | RWB-TE-002 specification (run `INC-004-epic-1-RWB-TE-002`, 17 Nov 2026): SPEC-RWB-TE-002-001 (`.gitlab/CODEOWNERS`, GitLab sections), -009 (owner register), validator rules V4, V7, V9 | `aisdlc/output/INC-004-epic-1-RWB-TE-002/specify/spec.md` |
| SRC-24 | RWB-E1-001 specification under revision (run `INC-009-epic-1-RWB-E1-001`, 18 Nov 2026): SPEC-RWB-E1-001-004, -006 (seeds), `ASM-E1001-14` (protective union, 526 fields; Blocker = Yes gap `GAP-E1001-18` awaiting a human ruling); evidence `is_personal_union_v4.tsv` | `aisdlc/output/INC-009-epic-1-RWB-E1-001/specify/` |
| SRC-25 | RWB-E1-043 specification, revision 4 (run `INC-008-epic-1-RWB-E1-043`, 18 Nov 2026; revision 3 first corrected GAP-38): SPEC-RWB-E1-043-031 (dictionary loads and the `is_personal` mark); `document-gaps.md` GAP-38 (corrected in revision 3: nothing asked of RWB-TE-011); `shared-updates.md` open item R4 (owner RW-COMPLY; revision 4 names no data-architect role) and §3.2 forward note to RWB-E1-064 | `aisdlc/output/INC-008-epic-1-RWB-E1-043/specify/` |
| SRC-26 | Run decisions D-RUN-07 (migration numbers at merge), D-RUN-08 (dependencies and seams), D-RUN-13 (SQL identifiers versus string literals); orchestrator triage of RWB-TE-011, 2026-11-18T00:04 (round 4) and 2026-11-18T00:35 (round 5: the dictionary-load seam belongs to RWB-E1-064) | `AI-SDLC-BUILD-LOG.md` §1 and the event log |
| SRC-27 | Round-4 evidence of this stage: INSERT count and pattern scan of the Physical Schema v6 copy, statements that write `sys_fields`, name ambiguity of the protective union, today's log calls | `specify/evidence/te011_round4_check.py` and `-output.txt` (run 18 Nov 2026, `python -I`) |
| SRC-28 | Round-5 evidence of this stage: described (object, field) pairs, API properties with a personal name and whether their schema is described, ACE schema copy pairs reached only by the name rule, SQL files, column-less INSERTs and `COPY` in the scan roots, INSERTs of the PS v6 copy by table | `specify/evidence/te011_round5_check.py` and `-output.txt` (run 18 Nov 2026, `python -I`) |
| SRC-29 | RWB-E1-064 story file v1 (Story Files v7), Data dictionary for the 14 data products: flow steps 2–3 (`sys_fields` load through POST /admin/reference-loads; `DataDictionaryLoader`), §11 (`is_personal` DF-REF-105 is **Read**), BR8, BR9, §12 (`DataDictionaryLoader` published interface). Build Sequence v6 order 13 | `legacy/04-user-stories/.../rwb-e1-064-data-dictionary-for-the-14-data-products-v1.md`; `aisdlc/docs/increments/build-sequence.md` |
| SRC-30 | Earlier merges, build orders 1–5 (D-RUN-06 merge in build order): RWB-E1-042 spec (run `INC-003-epic-1-RWB-E1-042`), migration steps 1–8 (DDL, `COMMENT ON`, `INSERT … ON CONFLICT (param_key) DO NOTHING`, `INSERT … SELECT … WHERE NOT EXISTS`, a self-check `DO` block) and SPEC-RWB-E1-042-006; RWB-E1-044 spec (run `INC-001`: no production migration, test-fixture migrations under `backend/src/test/resources/`, lint rule L-FIX-LINE2); RWB-TE-001 (no migration, D-RUN-17); RWB-TE-002 (no migration); RWB-TE-003 spec SPEC-RWB-TE-003-011 (`ContractFixtures`). Run decision D-RUN-15 (A-07 to RWB-TE-003; no `X-Correlation-Id`) | `aisdlc/output/INC-00{1..5}-*/specify/spec.md`; `AI-SDLC-BUILD-LOG.md` §1 |
| SRC-31 | RWB-E1-044 specification v14-7 (run `INC-001-epic-1-RWB-E1-044`, 18 Nov 2026): SPEC-RWB-E1-044-007 search-path table (`ALTER ROLE`, `ALTER DATABASE`, `ALTER FUNCTION … SET search_path`, `SET LOCAL`, `RESET`, `set_config`), SPEC-RWB-E1-044-010 (lint fixture tests scan folders under `backend/src/test/resources/migration-lint/`; fixtures synthetic), SPEC-RWB-E1-044-011 and T-044-10..18 (Flyway fixtures under `backend/src/test/resources/flyway-fixtures/`, applied to PostgreSQL), T-044-20, T-044-21 (`sys_fields` INSERT with `source_field` only), T-044-22 N11–N13 (unterminated literal, block comment, dollar body). Repository: `backend/src/main/resources/application.yaml` `rwb.flyway.location: classpath:db/modulemigration/recovery`; `scripts/dev.ps1` command `test`; build log: the orchestrator merges locally on a green `./scripts/dev.ps1 test` (D-RUN-06) | `aisdlc/output/INC-001-epic-1-RWB-E1-044/specify/spec.md`; repository files; `AI-SDLC-BUILD-LOG.md` |

## Change Scope Declaration

| Item | Value | Evidence |
|---|---|---|
| Change Type | `NEW_STORY` | No prior trace chain: Traceability Matrix v2.0 row 006 reads "No current spec/plan"; no `output/INC-006-*` folder existed; no `tools/` folder exists in the repository. The story adds a new build-time flow (SRC-01 §4). |
| UI In Scope | NO | SRC-01 §15: "No screen in this story." |
| Logic In Scope | YES | Six lint rules, allow-list logic and rule generation (SRC-01 §4, §8, §12). |
| API In Scope | NO | No endpoint; SRC-01 §10 "No Workbench capability area applies"; TC-TE-011-11 "This story has no Workbench endpoint". |
| API Impact Type | `NO_API_CHANGE` | As above. API Specification v4 is read as an input file only (SRC-01 §12). |
| Impacted Existing Nodes | `.gitlab-ci.yml` (new job `pdpa-lint` with `GIT_DEPTH: 0`); `.gitlab/CODEOWNERS` delivered by RWB-TE-002 (one new entry in section `[Recovery module]`; RWB-TE-002 spec SPEC-RWB-TE-002-001, L-RCV-12); `scripts/dev.ps1` (required: the `test` command runs the lint with the changed-file list, and a new `pdpa-lint` command runs it alone; SPEC-TE011-013) | SRC-01 §13 build step 6; SRC-19 A-09; SPEC-TE011-013, -014 |
| New Nodes Required | YES: `tools/pdpa-lint/` (tool source, tests, configuration, `pdpa-allow.yaml`) | SRC-01 §13 "Package. Folder `tools/pdpa-lint`" |
| Inherited Existing Behavior | Existing CI jobs `backend-unit`, `frontend-check`, `backend-recovery-it` unchanged; ESLint D-RCV-39 rule unchanged; Physical Schema v6 and API Specification v4 read unchanged | `.gitlab-ci.yml`; `frontend/eslint.config.js` |
| Frontend Changes Required | NO | Front-end source is scan input only. No file under `frontend/` changes (see Frontend Specification). |
| Backend Changes Required | YES — build tooling only | New tool under `tools/pdpa-lint/` and a CI job. No change to `backend/src/main` or to any endpoint, entity, migration or runtime configuration. |

## Preflight evidence

| Input | Finding |
|---|---|
| Requirement text | SRC-01 §1–§19 (10 ACs, 7 BRs, 11 exception paths, 11 test cases). SRC-02 (16 Nov) is the consolidated copy aligned to D-RCV-35; it removes the ACs and test cases and adds the view columns. This spec uses SRC-01 for ACs and test cases (increment card; SRC-05 rows are "Live") and applies the SRC-02 additions. Even without the ACs the story would be accepted on its business rules and test cases (`AGENTS.md` §6, which generalises D-RCV-16). Gap DGL-02. |
| Trace chain | None for RWB-TE-011 (matrix row 006). |
| Implementation footprint | `.gitlab-ci.yml` has three jobs and no PDPA lint (SRC-19 A-09). No `tools/` folder. No code-owner file (SRC-19 A-10); RWB-TE-002 is specified to deliver `.gitlab/CODEOWNERS` (SRC-23) but is not built. No common module and no masking helper in the repository (SRC-19 A-02; OPEN-024). Back-end log calls today: `ApiExceptionHandler` (2), `DroolsRuleEngine` (1), `TemporalConfig` (1); none uses a personal field. Fixture literals today: three e-mail addresses in `frontend/e2e/platform.spec.ts`, all in domain `local.test`; no 13-digit number and no Thai mobile number in `backend/src` or `frontend/src`/`frontend/e2e` (grep, 17 Nov 2026). |

## User story intent

A build check, run on every merge request and every build of the default branch, that fails when code,
test fixtures, log statements or error messages carry personal data, and that takes the list of
personal fields from the data dictionary rather than from the lint's own code (SRC-01 §1, §2, BR1).
The lint reads files only; it never reads data values from a database and never prints the value it
found (SRC-01 §11 note, §17, BR7).

## Scope decisions on the orchestrator notes

| Note | Decision | Reason |
|---|---|---|
| A-09, PDPA part: "CI has no PDPA lint job" (SRC-19) | **In scope** → SPEC-TE011-013 | SRC-01 §4 step 7 and §13 build step 6 ("Add PdpaLintStep to the pull request pipeline"); testing standards §1 row "Security: PDPA lint … Pass on every MR". |
| A-09, other jobs (contract, dependency scan, ZAP, Playwright/axe, coverage verification) | Out of scope | Not in SRC-01. Dependency approval and secret scanning are excluded by SRC-01 §19 (NFR-052, NFR-054: "the ACE pipeline, outside the recovery backlog"). The contract job is assigned to RWB-TE-003 by SRC-19. |
| A-07 (a): `ApiExceptionHandler` logs raw exception text (`log.error("Unhandled recovery API error", ex)`) | Out of scope | SRC-01 specifies a static, file-reading build check: §13 "Database. None", "Feature flag. None. A build check has no runtime path to switch off", §12 Input lists files only. No AC, BR or flow step changes runtime logging. The lint rules key on personal field names and personal entities (BR2); a raw `Throwable` argument carries neither, so the lint cannot flag it without a rule the story does not contain. The concern is real under Audit and Logging Design v2 §6 and BS-4.6. **Owner settled by D-RUN-15 (orchestrator, 2026-11-18T00:39): A-07 belongs to RWB-TE-003**, which stops `ApiExceptionHandler` logging raw exception text and carries the Problem `traceId` (SRC-30). No open item or owner change is proposed here. |
| A-07 (b): no correlation ID in the MDC; `X-Correlation-Id` not read or echoed | Out of scope | Not in SRC-01 or SRC-08. `X-Correlation-Id` occurs 0 times in API Specification v4 and in the converted document set. **Settled by D-RUN-15:** `X-Correlation-Id` is not built, because no source names it; the orchestrator records it as a document gap. The `traceId` part goes with A-07 to RWB-TE-003 (SRC-30). No open item is proposed here. |
| Fixtures and log lines checkable for personal data | **In scope** → SPEC-TE011-001, -004..-009 | Classification used: Physical Schema v6 `sys_fields.is_personal` plus API Specification v4 `x-personal-data`, as SRC-01 §12 names. Cross-checked against Personal Data Protection Design v2 §1, Inventory v4 and LDM v8 (next section). |

## Entry trigger and preconditions

| Precondition (SRC-01 §3) | State on 17 Nov 2026 | Effect |
|---|---|---|
| RWB-TE-001 done; recovery folders and pipeline checks exist | Done (matrix row 002); `.gitlab-ci.yml` has 3 jobs | Met |
| Dictionary marks each personal field (`sys_fields.is_personal`; `x-personal-data: true`) | **Partly met**: the mechanism exists (18 fields `is_personal = true` in the Physical Schema v6 seed; 5 properties with `x-personal-data: true` in API Specification v4), but the marks do not cover fields that Inventory v4 classes as personal, including 9 Restricted fields (DGL-01). Later marks by D-RCV-29 reference load do not reach any file (DGL-13) | The lint can be built and run. Production coverage is the dictionary as seeded and changed by migrations: 18 fields today, the 526-field protective union if RWB-E1-001 seeds it (SPEC-TE011-017) |
| Synthetic values use the prefix "SYN-" (assumed convention of RWB-E1-065) | Evidenced: RWB-E1-065 §13 ValueFactory produces names such as "SYN-FIRST-000123" (SRC-15). RWB-E1-065 is not built (build order 14). | Met as configuration (SPEC-TE011-015) |
| Masking helper of the common module available | **Not met**: no common module in the repository (SRC-19 A-02; OPEN-024) | AC8 is proven with a configured helper name in the lint's test configuration; production list empty until published (ASM-TE011-07, DGL-06) |

Trigger: every merge request pipeline and every pipeline of the default and protected branches
(SRC-01 §12 "Every pull request and every build of main"; D-RCV-50 integration branch
`develop-recovery`; L-RCV-13 protected branches `main`, `develop-recovery`, `develop`). This
repository's `.gitlab-ci.yml` has no `workflow:` block, so GitLab creates branch pipelines and tag
pipelines, and no merge request pipeline; the job runs in each of them (SPEC-TE011-013).

## Personal data classification used

The lint's field list is the union of (SRC-01 §12, BR1):

1. Every `sys_fields` row with `is_personal = true` in the dictionary as seeded and changed by
   migrations (SRC-06; SPEC-TE011-001), each kept as an (object, field) pair, and
2. Every schema property with `x-personal-data: true` in the API specification (SRC-07), mapped to its
   snake-case field name, with the snake case of its schema name as the object.

**What the lint covers, stated narrowly.** The lint covers what is committed: SQL migrations, test
fixtures and log statements, checked against the dictionary as seeded and changed by migrations. That
dictionary is the Physical Schema v6 copy (the stand-in for the RWB-E1-001 seed) and the `sys_fields`
statements in the recovery migration folder. It does not police run-time dictionary loads. Decision Log
v10 D-RCV-29 sends "later dictionary changes" through reference loads (SRC-22). Such a load changes the
database and no repository file, and this lint reads files only (story §13, §17). A mark added or removed
by a load is therefore not visible to the lint.

Who owns that route (orchestrator triage 2026-11-18T00:35, SRC-26; D-RUN-08):

- **RWB-E1-064** (Build Sequence v6 order 13) owns the dictionary load handler. Its `DataDictionaryLoader`
  applies approved `sys_fields` loads, and its contract lists `is_personal` (DF-REF-105) as **Read**
  (SRC-29). Protecting `is_personal` marks against a later dictionary load is an RWB-E1-064 seam.
- **RWB-E1-043** (order 8) provides the load pipeline only: version log, change summary by field ID and
  non-author approval (SRC-25 SPEC-RWB-E1-043-031). It does not build the dictionary handler, does not
  refuse removal of a mark and does not make loads visible to this lint. Its revision 3 corrected
  GAP-38, and revision 4 keeps it: nothing is asked of RWB-TE-011. Its forward note to RWB-E1-064 (§3.2) states the protective
  requirement: the `sys_fields` handler refuses any load that changes `is_personal` and never writes it
  (SRC-25).
- **RW-COMPLY (Compliance)** owns the single open item for the decision: **RWB-E1-043 open item R4**
  ("Decide which governed path may change an `is_personal` mark in `sys_fields`"; owner RW-COMPLY;
  SRC-25). This stage's earlier proposal OPEN-NEW-TE011-7 is withdrawn in its favour
  (orchestrator triage, round 6). `shared-updates.md` asks the orchestrator to carry this story's
  question in R4: how an approved change reaches a committed file the lint reads.

This conflict is recorded as DGL-13.

Resulting list at Physical Schema v6 / API Specification v4 (field names only; no values):

| BR Field ID | Object | Field | Data type | Source |
|---|---|---|---|---|
| DF-ACE-057 | v_ace_customer | first_name | TEXT | seed |
| DF-ACE-058 | v_ace_customer | last_name | TEXT | seed |
| DF-ACE-059 | v_ace_customer | date_of_birth | DATE | seed |
| DF-ACE-066 | v_ace_customer | spouse_name | TEXT | seed |
| DF-ACE-072 | v_ace_customer | vat_number | TEXT | seed |
| DF-ACE-073 | v_ace_customer | id_no_masked | TEXT | seed |
| DF-ACE-074 | v_ace_customer | id_no_last4 | TEXT | seed |
| DF-ACE-078 | v_ace_contact | contact_value | TEXT | seed |
| DF-ACE-079 | v_ace_contact | contact_value_masked | TEXT | seed |
| DF-INT-011 | interaction | summary | TEXT | seed + API (`summary`) |
| DF-DOC-015 | document_field | field_value | TEXT | seed + API (`fieldValue`) |
| DF-DOC-034 | document_field | extracted_value | TEXT | seed + API (`extractedValue`) |
| DF-DOC-028 | document | capture_latitude | NUMBER | seed + API (`captureLatitude`) |
| DF-DOC-029 | document | capture_longitude | NUMBER | seed + API (`captureLongitude`) |
| DF-DOC-049 | document_intake | file_name | TEXT | seed |
| DF-DOC-052 | document_intake | sender_address | TEXT | seed |
| DF-DOC-077 | document_intake | extracted_fields | TEXT (jsonb) | seed |
| DF-DOC-089 | document_text | text_content | TEXT | seed |

Cross-check (recorded as DGL-01, not resolved here because classification is owned by Compliance under
DL26 and is out of scope, SRC-01 §19):

| Source | Count marked personal | Notable differences from the list above |
|---|---|---|
| LDM v8, "Personal data" column (SRC-10) | 9 | None of the `v_ace_customer` / `v_ace_contact` fields is marked, although story BR1 names the LDM as a source |
| Inventory v4, "Personal data" = Yes (SRC-09) | 523 of 1,366; 17 classed Restricted | Marks 14 of the 18 seed fields. It classes DF-DOC-049 `file_name`, DF-DOC-052 `sender_address`, DF-DOC-077 `extracted_fields` and DF-DOC-089 `text_content` as "Not personal" / Internal, which the seed marks personal. It also marks 509 fields that the seed does not, among them `cif_no`, `contract_no`, `case_no` (indirect identifiers) and the 9 Restricted fields listed below |
| Personal Data Protection Design v2 §1 (SRC-08) | Categories | Names the Inventory workbook as "the field-level inventory". Sensitive flags are "Restricted"; account, contract and case numbers are "Confidential" indirect identifiers |
| Backend context v2.0 §6 (SRC-20) | — | "field-level classification in the Personal Data Inventory v4" |
| SRC-01 §7 Background | 8 | Includes `cif_no`, which the seed marks `false` |
| SRC-01 §11 Data | 11 rows | Lists `cif_no` (DF-ACE-055), `vulnerable` (DF-EXT-002), `deceased_flag` (DF-ACE-061) and `bankruptcy` (DF-EXT-004) among the definitions the lint reads; none is marked in the seed |
| SRC-05 Background | 10 | Adds `id_no_last4`, `contact_value_masked` (both in the seed) and `cif_no` |

Precedence used: the story's own contract (SRC-01 §12 and SRC-02 BR1/§12, story files v7) names the
`sys_fields` seed and the API specification as the input. PDPA Design v2 and backend context v2.0
point to Inventory v4 for the classification, but they are not story-level sources, and which fields
are personal is DL26 (Compliance) and out of scope (SRC-01 §19). This stage therefore does not choose
a classification. It records the difference (DGL-01) and proposes an open item (OPEN-NEW-TE011-1).

**Residual risk, stated so that it stays visible.** With the dictionary as it is today (Physical
Schema v6 copy, no migration yet), the production lint does not flag the following Inventory v4
**Restricted** fields, because the seed marks them `is_personal = false`:

| BR Field ID | Object | Field | Inventory v4 category |
|---|---|---|---|
| DF-ACE-003 | v_ace_account | account_name | Direct identifier |
| DF-ACE-041 | v_ace_account | special_memo | Direct identifier (free text) |
| DF-ACE-053 | v_ace_payment | comments | Direct identifier (free text) |
| DF-ACE-116 | v_ace_efs_action | comments | Direct identifier (free text) |
| DF-ACE-060 | v_ace_customer | deceased_date | Sensitive |
| DF-ACE-061 | v_ace_customer | deceased_flag | Sensitive |
| DF-EXT-002 | party_ext | vulnerable | Sensitive |
| DF-EXT-003 | party_ext | deceased_override | Sensitive |
| DF-EXT-004 | party_ext | bankruptcy | Sensitive |

It also does not flag the other Inventory v4 "Yes" fields that the seed does not mark (509 in all,
including the 9 above; for example `cif_no`, `contract_no`, `case_no`). The conflict also runs the other
way: the seed marks 4 document-intake and document-text fields that Inventory v4 classes as not personal.
The lint keeps them, because it follows the seed. The seed's own descriptions support the marks
(Physical Schema v6 `sys_fields`): DF-DOC-049 `file_name` "personal where it names a customer";
DF-DOC-052 `sender_address` and DF-DOC-089 `text_content` "masked by role". For DF-DOC-077
`extracted_fields`, PDPA Design v2 §1 classes extracted document fields as direct identifiers. Any
alignment should add marks, never remove them (OPEN-NEW-TE011-1).

How the residual risk closes depends on RWB-E1-001 (SPEC-TE011-017):

| If | Then |
|---|---|
| RWB-E1-001's baseline migration (`V<seq>__RWB-E1-001_<name>.sql`, number at merge, D-RUN-07) seeds the protective union of `ASM-E1001-14` (526 fields: PS v6 `true` or Inventory v4 "Personal data" = Yes; SRC-24) as `INSERT` rows the reader parses | Items (a) and (b) of OPEN-NEW-TE011-1 close at RWB-E1-001's merge. All 17 Inventory v4 Restricted fields, including the 9 above, are then in the lint's list, and so are 508 of the 509 unmarked "Yes" fields. The one left out has an Inventory v4 row but no `sys_fields` row in PS v6, so no dictionary can mark it (RWB-E1-001 evidence `pdpa_v4_vs_ps_v6-output.txt`, set C). No code change in the lint is needed (BR1, AC5) |
| RWB-E1-001 seeds PS v6 as written (the human ruling on `GAP-E1001-18` goes the other way) | Items (a) and (b) stay open. They close only when committed dictionary rows add the marks in a form the reader recognises (SPEC-TE011-001): a migration, or a committed export decided under RWB-E1-043 open item R4. A mark added only by reference load does not close them (DGL-13) |

A green lint therefore proves that the fields in the dictionary as seeded and changed by migrations
stay out of code, fixtures and logs: today the 18 marked fields. The story's ACs use a test dictionary
that marks the Background fields (SPEC-TE011-016).

## Functional specification

### SPEC-TE011-001 Personal field reader (BR1; flow step 1; AC5)

**Sources and order** (configuration, SPEC-TE011-015; ASM-TE011-02):

1. The baseline: `infra/postgres/schema/03-recovery-physical-schema-v6.sql`. It is the Physical Schema
   v6 copy that stands in for the dictionary seed RWB-E1-001 delivers (`README.md`;
   `infra/postgres/init/10-load-ace-database.sh`).
2. Then every `*.sql` file in the recovery migration folder given by `rwb.flyway.location`
   (SPEC-TE011-003; today `backend/src/main/resources/db/modulemigration/recovery/`), in Flyway version
   order.
3. Then any further dictionary file listed in configuration (none by default). A later story that
   commits a dictionary export can add it under code owners without a code change, provided it uses the
   recognised forms below.

**Statement handling.** Each file is split into statements by one quote-aware pass: single-quoted
strings, dollar-quoted strings, `--` and `/* */` comments. A statement writes `sys_fields` when the
identifier `sys_fields` is its target. The identifier may be bare, qualified (`${recoverySchema}.`,
`recovery.`) or double-quoted. Text in string literals and comments is never an identifier (D-RUN-13).
Every statement that names `sys_fields` falls into exactly one of three classes:

| Class | Statements | Effect |
|---|---|---|
| Read | (R1) `INSERT INTO sys_fields (<columns>) VALUES (<row>)[, (<row>)]…`: single-row and multi-row. Values are matched by column name, not by position. The columns must include `field_id`, `object_name` and `field_name`. Those three and `is_personal` must be literals (string, `true`/`false`, `NULL`). An omitted `is_personal` takes the table default `false`. `source_field` is read when present. | Adds or replaces rows (see "Order rules") |
| Read | (R2) `UPDATE sys_fields SET is_personal = true\|false [, <other columns> = <literal>] WHERE field_id = '<id>'` or `WHERE field_id IN ('<id>', …)`, with literal IDs only. The other columns must not include `field_id`, `object_name`, `field_name` or `source_field`. | Sets the mark of the named fields |
| Ignored (cannot change the field list) | `UPDATE sys_fields SET …` whose SET list names none of `is_personal`, `field_id`, `object_name`, `field_name`, `source_field`. `CREATE TABLE sys_fields`. `CREATE [UNIQUE] INDEX … ON sys_fields`. `COMMENT ON TABLE\|COLUMN sys_fields…`. `ALTER TABLE sys_fields ADD CONSTRAINT …`. `GRANT`/`REVOKE … ON sys_fields`. A foreign key in another table that references `sys_fields` (`CREATE TABLE <other> (… REFERENCES sys_fields …)` or `ALTER TABLE <other> … REFERENCES sys_fields …`): it names the table without writing it. Any statement that only reads `sys_fields` (`SELECT`, a view or an `INSERT INTO <other table> … SELECT … FROM sys_fields`). | None |
| **Fail closed** | Every other statement that writes `sys_fields`. Examples: `DELETE`, `TRUNCATE`, `COPY` (and psql `\copy`), `MERGE`, `INSERT … SELECT`, `INSERT … ON CONFLICT`, a non-literal value in a key column or in `is_personal`, an `UPDATE` of `is_personal` or a key column in any form not listed under R2 (for example `WHERE object_name = …`, a subquery, an expression), any other `ALTER TABLE sys_fields` action, `DROP TABLE sys_fields`, and a `DO` block, function or procedure body that names `sys_fields`. | Exit 2 with `dictionary statement not supported: {file}:{line}`; never the statement text (BR7) |

Physical Schema v6 contains only R1 and ignored statements on `sys_fields`. These are 1,379
single-row INSERTs, 1 `CREATE TABLE`, 1 view that reads it, 1 `ALTER TABLE … ADD CONSTRAINT` and 18
`COMMENT ON`, so the baseline reads without failing (SRC-27). It has no foreign key that references
`sys_fields` (SRC-28).

**Order rules** (fail-safe; ASM-TE011-21, -22):

- An R1 row for a `field_id` already read from the **baseline** replaces the baseline row. The migration
  is the real seed that the baseline stands in for, so once RWB-E1-001's migration is merged its rows
  govern with no configuration change. A baseline row that no migration replaces stays in the list.
- An R1 row for a `field_id` already read from an earlier **migration** fails closed (exit 2), because
  the database rejects it (`uk_sys_fields`).
- An R2 `UPDATE` that names a `field_id` not yet read fails closed (exit 2). It would change no row, so a
  mark that someone meant to add would be lost silently.
- When a replacement or an R2 `UPDATE` turns a mark from `true` to `false`, the change is applied (the
  lint follows the dictionary; classification is Compliance's, DL26). The run then prints
  `PDPA-NOTICE: {field_id} unmarked at {file}:{line}` so that code owners see the unmarking. The notice
  names the field ID only and does not change the exit code.
- A field stays in the list whatever its `is_active` value (fail-safe: a deactivated field can still be
  used in code, fixtures or logs).

**Keys kept for each personal field** (used by SPEC-TE011-008):

- `(object_name, field_name)`.
- When `source_field` has the form `<schema>.<table>.<column>`, the pair `(<table>, <column>)` is also
  kept. Example: DF-ACE-058 `v_ace_customer.last_name` has source field `public.customer.surname`. In
  the protective union, 244 fields carry such a source field (SRC-27). This lets a fixture that writes
  an ACE-shaped source table be matched.
- For an API property, `(snake case of the schema name, snake case of the property)`.

**Dictionary at a point.** For each migration file, the reader also keeps the field list as it stands
after that file has been read: the baseline, every earlier migration and the file itself. SPEC-TE011-008
uses it.

**API and limits.**

- Reads the configured API specification (default `api/recovery-api-v4.yaml`). Each schema property with
  `x-personal-data: true` adds its property name, converted from camel case to snake case.
- Never reads a database and never reads a field value (SRC-01 §11 note, §13 "Database. None"). A mark
  that reaches only the database, such as a D-RCV-29 dictionary load, is outside the lint. The lint covers
  committed SQL, fixtures and log statements only; protecting marks on load is the RWB-E1-064 seam
  (DGL-13; SPEC-TE011-017; RWB-E1-043 open item R4).
- Fails closed: exit code 2 with a message naming the file and line, never the content, in these
  cases: a configured source is missing or unparsable; a statement is in the fail-closed class above;
  the union is empty (ASM-TE011-03).

### SPEC-TE011-002 Rule generator (flow step 2; contract "Rule set"; AC5)

- Writes `pdpa-rules.yaml` on every run, before scanning, from the SPEC-TE011-001 list. It is generated,
  never edited by hand and not committed; it is written to the tool's build output and kept as a CI
  artifact (SRC-03 step 2; ASM-TE011-15).
- Contains the six rules PDPA-LOG-FIELD, PDPA-LOG-ENTITY, PDPA-EXCEPTION, PDPA-TOSTRING,
  PDPA-FIXTURE-FIELD and PDPA-FIXTURE-ID (SRC-01 §12).
- For each personal field it lists the name variants: snake case (`last_name`), camel case property used
  in Java, JSON and TypeScript (`lastName`), Java getter (`getLastName`) (SRC-01 §13 RuleGenerator).
- It lists personal entity type names (flow step 2 "entity class names"; SRC-02 adds "view names"; story
  defect SRC-04 step 2 resolved in favour of the flow and AC2): Pascal case of the object name with a
  leading `v_ace_` removed, with each configured suffix; default suffixes `Entity` and `View`
  (`v_ace_customer` → `CustomerEntity`, `CustomerView`; `v_ace_contact` → `ContactEntity`, `ContactView`)
  (ASM-TE011-04).
- For each personal field it lists the object keys from SPEC-TE011-001. It also lists, for each field
  name, whether the name is **unambiguous**: every dictionary row with that `field_name` is personal.
  Under the protective union, 71 of the 390 personal names are ambiguous, for example `status`,
  `description`, `owner_role`, `source_system` and `field_name`. None of the 18 PS v6 names is ambiguous,
  and neither is any of the 9 Restricted names in the residual-risk table (SRC-27).
- It lists the **API personal names**: the snake case of every property with `x-personal-data: true`
  on any schema. Today these are `summary`, `field_value`, `extracted_value`, `capture_latitude` and
  `capture_longitude` (SRC-28). SPEC-TE011-008 uses them for positions typed by an API schema (DGL-15).
- Output is deterministic: entries sorted by field name and rule; no timestamp in the file body (contract
  "Idempotency").

### SPEC-TE011-003 Scan scope (flow steps 3–4; §13 Package)

Scan roots and exclusions are configuration, not code (SRC-01 §6 "Negotiable"; §17). Defaults
(ASM-TE011-05), all relative to the repository root:

| Class | Default roots | Rules applied |
|---|---|---|
| Production source | `backend/src/main/java/th/co/scb/ace/demo/recovery/**/*.java`; `frontend/src/modules/recovery/**/*.{ts,tsx}` excluding `__tests__/**` and `*.test.*` | LOG-FIELD, LOG-ENTITY, EXCEPTION, TOSTRING, FIXTURE-ID |
| Seeds and migrations | `backend/src/main/resources/db/modulemigration/recovery/**/*.sql` | FIXTURE-FIELD, matched by (object, field) against the dictionary at that migration (SPEC-TE011-008); FIXTURE-ID. Never excused by the allow list (SPEC-TE011-011) |
| Lint fixtures | `backend/src/test/resources/migration-lint/**` (RWB-E1-044's lint fixture folders; SRC-31) | FIXTURE-ID only, on the raw text. No parsing, no statement classes, no reader, no corrective-migration rules, never exit 2 from content |
| Tests and fixtures | `backend/src/test/**/*.{java,sql,json}` and `backend/src/test/resources/**`, except the lint-fixture roots; `frontend/src/modules/recovery/__tests__/**`, `frontend/src/**/*.test.{ts,tsx}`, `frontend/src/test/**`; `frontend/e2e/**/*.{ts,json}` | FIXTURE-FIELD, FIXTURE-ID |
| Local infrastructure | `infra/**` except `infra/postgres/schema/**` (init scripts, mock identity provider, Temporal set-up; repo-authored and a likely place for future SQL seeds, story §4 step 4) | FIXTURE-FIELD, FIXTURE-ID |
| The lint itself | `tools/pdpa-lint/**` | FIXTURE-ID only (self-scan; enforces story §17 "generated at run time and never stored") |

Not scanned: `infra/postgres/schema/**` (three read-only copies: `01-ace-schema-v1.sql`, header "Schema only: no
data rows"; `02-ace-tier2-probe.sql`, DDL only; `03-recovery-physical-schema-v6.sql`, the byte-identical
copy of Physical Schema v6, which holds reference and dictionary seed INSERTs, including the `sys_fields`
seed that is the lint's input. None is a test fixture, and none may be edited in this repository. The
third file holds 2,584 INSERT statements, all with a named column list: 1,379 into `sys_fields`, 598 into
`lov_value`, 421 `INSERT … SELECT` into `permission`, 123 into `sys_objects`, 54 into `role`, 8 into
`rule_package` and 1 multi-row into `data_product` (14 rows). It holds no `COPY` (SRC-27, SRC-28). The pattern scan of 18 Nov 2026 found 0 13-digit runs, 0 dashed
IDs, 0 Thai mobile numbers and 0 e-mail addresses (SRC-27), so the exclusion hides no FIXTURE-ID
match); FIXTURE-FIELD and the log rules on `tools/pdpa-lint/**` (its
fixtures name personal fields by design); `frontend/src/api/schema.d.ts` (generated types; read only to
recognise personal entity types); `node_modules`, `build`, `dist`, `coverage`.

On 17 Nov 2026 the repo-authored `infra/` files hold no personal-field literal, no 13-digit number and
only e-mail addresses in the reserved domain `local.test` (grep), so the added roots keep the zero-finding
baseline (SPEC-TE011-016).

**The migration folder cannot be left out** (review SG6-02). The scan of the recovery migration folder
`backend/src/main/resources/db/modulemigration/recovery/` is not optional:

- **Source of the path** (review SG7-03). The lint reads the folder from `rwb.flyway.location` in
  `backend/src/main/resources/application.yaml` (today `classpath:db/modulemigration/recovery`; SRC-31).
  It maps `classpath:` to `backend/src/main/resources/`. The reader (SPEC-TE011-001) and the scan both use
  that folder. The run fails with exit 2, `migration folder does not match rwb.flyway.location: {config
  key}`, in three cases: the property is missing; it is not a single `classpath:` location (for example
  an environment placeholder); or `pdpa-lint.yaml` sets `dictionary.migrationFolder` to another path. The
  property is the single source; the configuration key may only repeat it.
- Before scanning, the lint tests every file in that folder, and two probe paths (`<folder>/probe.sql` and
  `<folder>/sub/probe.sql`), against the roots and exclusions. If any of them is not covered by a root of
  the class "Seeds and migrations", or is matched by any exclusion or any lint-fixture root, the run
  fails with exit 2:
  `scan configuration excludes the migration folder: {config key}`, where `{config key}` names the root
  or exclusion, for example `exclusions[3]`. The probes make the check hold while the folder has no `.sql`
  file.
- Every run prints the exclusions in force, one line each, after the notices:
  `PDPA-SCOPE: exclusion {config key} {glob} excludes {n} files`, followed by the number of files
  scanned in each class. Each lint-fixture root is printed the same way:
  `PDPA-SCOPE: lint fixtures {config key} {glob} holds {n} files`. These lines carry paths and counts
  only; the changed-file lines of SPEC-TE011-013 also carry branch names.
  Code owners can see what a configuration change leaves out (SPEC-TE011-014).

**Lint fixtures** (review SG7-01; orchestrator triage 2026-11-18T04:54). Another SQL tool's tests need
SQL that is malformed, or outside the statement classes of SPEC-TE011-008, on purpose. RWB-E1-044 (order
1, merged before this story) commits such files, and this story adapts to its specification as it stands
(SRC-31). Nothing is asked of RWB-E1-044.

- **Default root: `backend/src/test/resources/migration-lint/**`.** RWB-E1-044 SPEC-RWB-E1-044-010 puts
  its lint fixture tests in folders there. They include unterminated SQL by design: T-044-22 N11
  (literal), N12 (block comment) and N13 (dollar body). They include every search-path form of its
  SPEC-RWB-E1-044-007 table (T-044-20), among them `ALTER ROLE`, `ALTER DATABASE` and `ALTER FUNCTION …
  SET search_path`, which are class 4 here. They include `INSERT INTO ${recoverySchema}.sys_fields
  (source_field) VALUES (…)` (T-044-21), and `-- Fix:` lines for its L-FIX rules.
- **Not in the default: `backend/src/test/resources/flyway-fixtures/`.** RWB-E1-044 SPEC-RWB-E1-044-011
  and T-044-10..18 describe these as migrations that Flyway applies to PostgreSQL: `CREATE TABLE`,
  `REFERENCES`, and for AC8 a statement that references a missing table. They are meant to be valid
  SQL, so they stay in the class "Tests and fixtures" with every rule. RWB-E1-044 does not fix the form
  of the AC8 statement (its restated AC8 and T-044-14 say only that the second statement references a
  missing table). Written as DDL or as an `INSERT` that names its columns, with synthetic names, it gives
  0 findings. Written as a column-less `INSERT` with a literal, it gives a `(columns not named)` finding
  (review SG8-05).
- **If a merged Flyway fixture gives a finding.** At this story's merge the implementation run records
  the file, line, rule and field (no value) and reports it to the orchestrator (D-RUN-08). The route
  this story offers is a reviewed configuration change that adds that one file, not the folder, to
  `lintFixtureRoots`. The file is under a test root, its names are synthetic (RUN-BRIEF rule 7, which
  binds every run; RWB-E1-044's test rows describe synthetic tables, for example T-044-18), and
  FIXTURE-ID still applies. (SPEC-RWB-E1-044-010 covers the lint fixtures only.) An allow entry (SPEC-TE011-011) is also valid, because
  the file is outside the migration folder, but it must be renewed at each expiry. This story does not
  edit or exclude another story's fixture and asks nothing of RWB-E1-044.
- **Rules.** A file in this class gets FIXTURE-ID only, applied to its raw text, as `tools/pdpa-lint/**`
  does. A match in a comment or inside an unterminated token still counts. The file is never split into
  statements. The statement classes, FIXTURE-FIELD, the dictionary reader and SPEC-TE011-018 do not apply
  to it, and its content never gives exit 2.
- **Limit.** FIXTURE-FIELD does not run on these files, so a personal-field literal there is not found.
  RWB-E1-044 SPEC-RWB-E1-044-010 requires synthetic table and column names and no personal data. Code
  owners review the roots of this class (`lintFixtureRoots`, SPEC-TE011-014, -015). The SG6-02 check
  forbids a lint-fixture root from covering any file or probe path in the recovery migration folder.
- **Bound** (review SG8-05). Every lint-fixture root must lie under a root of the class "Tests and
  fixtures" (`backend/src/test/**`, `frontend/src/modules/recovery/__tests__/**`, `frontend/src/test/**`,
  `frontend/e2e/**`, or a `*.test.*` file). The lint checks the root's fixed prefix (the path before its
  first wildcard). A root outside them, for example over production source or `infra/**`, fails the
  run with exit 2, `lint-fixture root outside the test roots: {config key}`. The log, exception and
  text-form rules therefore never stop for production source.

### SPEC-TE011-004 PDPA-LOG-FIELD (BR2; X1, X5, X7; AC1, AC5, AC7)

A finding is raised when the argument list of a log call uses a personal field.

- **Log call (Java):** a method `trace|debug|info|warn|error` (and SLF4J fluent `atTrace..atError(...).log(...)`)
  on a receiver declared in the file with type `org.slf4j.Logger` or named in `javaLoggerNames` (default
  `log`, `logger`, `LOG`, `LOGGER`); and `System.out`/`System.err` `print|println|printf` (ASM-TE011-06).
- **Log call (TypeScript):** `console.log|info|warn|error|debug|trace` and method calls on identifiers in
  `tsLoggerNames` (default empty) (X7 "a front end console or logger call").
- **Uses a personal field:** anywhere in the argument expressions, including string concatenation,
  `String.format`, `StringBuilder` chains, `MessageFormat` and TypeScript template literals (flow step 3
  "string building in log calls"): a Java getter call `getXxx()`, a member access `.xxx` or `.xxx()` on the
  camel-case name (record accessor, TS property), or a bare identifier equal to a camel-case or snake-case
  variant. Text inside string literals is not a use (it names a field, it does not carry a value).
- Matching here, and in SPEC-TE011-005..-007, stays by name variant. This is a deliberate choice: a log
  line or exception message is run-time output, and a missed field leaks data, while a false positive
  costs a source edit or an allow entry (source files can be edited; BR6). Today's four back-end log
  calls use no name in the 390-name protective union (SRC-27), so this choice keeps the zero-finding
  baseline (SPEC-TE011-016).
- AC1: `customer.getFirstName()` in a log call → PDPA-LOG-FIELD for `first_name`.
- AC7: `console.log(customer.lastName)` → PDPA-LOG-FIELD for `lastName` (output format SPEC-TE011-012).

### SPEC-TE011-005 PDPA-LOG-ENTITY (BR2; X2; AC2)

A finding is raised when a log call argument is a whole object of a personal entity type: an identifier
(or `this`) used as an operand, in concatenation, in `String.valueOf(..)` or with `.toString()`, but not
followed by member access.

- The identifier's type is resolved from its declaration in the same file: field, parameter, local
  variable, record component, or `var x = new T(..)`; TypeScript type annotations.
- A type is a personal entity type when (a) its simple name is in the generated list (SPEC-TE011-002), or
  (b) it is declared in a scanned file or in `frontend/src/api/schema.d.ts` and has a member field, record
  component or property whose name is a personal variant (SRC-01 §4 step 5 "each entity with a personal
  field"; SRC-03 step 2).
- AC2: a log call writing `customer` of type `CustomerEntity` → PDPA-LOG-ENTITY. The same holds for
  `CustomerView` (SRC-05) and `PartyEntity` when it declares a personal field (SRC-01 TC-TE-011-02).

### SPEC-TE011-006 PDPA-EXCEPTION (BR2; X9; AC9)

The same "uses a personal field" and "whole entity" tests as SPEC-TE011-004/-005, applied to the
arguments of an exception construction: `new T(..)` where the simple name of `T` ends in `Exception`,
`Error` or `Throwable`, or is in `exceptionTypes` (Java and TypeScript) (ASM-TE011-06).
AC9: `throw new X("No case for " + customer.getCifNo())` with `cif_no` personal → PDPA-EXCEPTION for
`cif_no`.

### SPEC-TE011-007 PDPA-TOSTRING (BR5; X10; AC10)

For each type in production source that declares a personal member (SPEC-TE011-005 (b)):

- Java `record` with no explicit `toString()`: one finding per personal component, because the implicit
  text form of a record includes every component (Java language rule).
- Explicit `toString()` (Java class or record; TypeScript class) whose body uses a personal member, its
  getter or accessor: one finding per member, unless the use is inside a masking helper call
  (SPEC-TE011-010).
- Lombok is not a dependency of the back end (`backend/build.gradle.kts`), so no Lombok annotation rule is
  specified.
- AC10: `ContactEntity` whose text form includes `contact_value` → PDPA-TOSTRING for `contact_value`.

### SPEC-TE011-008 PDPA-FIXTURE-FIELD (BR3; X4; AC4)

A finding is raised for a non-null, non-empty literal in a personal field position that does not start
with the configured synthetic prefix (default `SYN-`) (flow step 4; BR3; SRC-15 ValueFactory).

Matching is by **(object, field)**, never by field name alone (orchestrator triage 2026-11-18;
DGL-14; ASM-TE011-12, -20). Inventory v4 classifies per entity and field. The same name can be personal
on one object and not on another: `status` is personal on `recovery_case` and not on `listing`.

**Described pairs** (revised after review SG5-01; orchestrator triage 2026-11-18T00:35). The dictionary
*describes* a field on an object when one of these holds:

- a `sys_fields` row has that `object_name` and `field_name`, personal or not;
- a `sys_fields` row has a `source_field` of the form `<schema>.<table>.<column>` with that table and
  column;
- an API schema property carries `x-personal-data: true` (object: snake case of the schema name).

A position is **resolved** when its object is resolved (table below) **and** the dictionary describes
that field on that object. A resolved position is personal exactly when the pair is a key of a personal
field (SPEC-TE011-001). Every other position is **unresolved**, and the name rule below applies. Three
kinds of position are unresolved:

- no object can be found;
- the object is outside the field dictionary: a SQL table with no dictionary row, a JPA
  `@Table(name = …)` on such a table, or an API schema such as `InteractionRequest`;
- the object is in the dictionary but the dictionary does not describe that field on it.

The rule works per pair, which is stricter than per object, as the review proposed. A per-object rule
would still skip a field that a described object lacks. Under the protective union, 20 API properties
with a personal name sit on schemas that map to a dictionary object but have no dictionary row for that
pair (SRC-28). On the six dictionary and reference seed tables, every column of every Physical Schema v6
seed INSERT is described on its own table (0 undescribed; SRC-28). Those seeds therefore stay resolved
and raise nothing (TS-TE011-01).

| File type | Position and object | Object resolution |
|---|---|---|
| SQL (`.sql` files) | `INSERT INTO <t> (<cols>) VALUES (<row>)[, (<row>)]…`: the value in a column `<c>`. `INSERT INTO <t> (<cols>) SELECT <list> …`: a literal in the select list at column `<c>`. `UPDATE <t> SET <c> = <literal>`. The tails these forms accept, and what happens to every other statement, are in "SQL statement classes" below. | `<t>`, with any schema qualifier removed (`${recoverySchema}.`, `recovery.`, `public.`, quoted). The key is (`<t>`, `<c>`). It also matches a source-field key, so `public.customer (surname)` matches DF-ACE-058. |
| Java / TypeScript test source | `setXxx(<literal>)` or builder `.xxx(<literal>)` on a receiver; `<receiver>.xxx = <literal>`; object-literal property `xxx: <literal>`. | The declared type of the receiver, builder or object literal, resolved in the same file: (1) a generated entity type name (SPEC-TE011-002: `CustomerEntity` → `v_ace_customer`); (2) a JPA `@Table(name = "<t>")` on a type declared in a scanned file; (3) an API schema type from `frontend/src/api/schema.d.ts` (`components["schemas"]["DocumentField"]` → `document_field`). |
| JSON | The value of a key at any depth. | A `fixtureObjects` entry in configuration, mapping a path glob to an object (SPEC-TE011-015). |

**When a position is unresolved** (for example a JSON file with no `fixtureObjects` entry, a bare
`xxx = <literal>`, an untyped object literal, `INSERT INTO it_customer (first_name)`, an ACE-shaped
`INSERT INTO public.address (address)`, or a fixture typed as `InteractionRequest`), the lint applies the
(object, field) test across the whole dictionary:

- If the name is **unambiguous** (every dictionary row with that name is personal; SPEC-TE011-002), the
  position is a finding. No non-personal (object, field) pair has that name, so the result cannot be a
  match against the wrong object. This keeps every PS v6 field and every Restricted field checked in
  SQL, JSON and test source, whatever table or type the fixture uses (SRC-27, SRC-28).
- **API personal names in API-typed positions.** When the object comes from an API schema type
  (resolution (3)) and the property's snake-case name is an API personal name (SPEC-TE011-002), the
  position is a finding even if the dictionary name is ambiguous. This is the protective reading of
  DGL-15: API Specification v4 marks `Interaction.summary` but not `InteractionRequest.summary`,
  `TimelineItem.summary` or `AgentOutput.summary`. The lint treats all of them as personal.
- Otherwise, if the name is **ambiguous**, the position is not a finding. The run prints
  `PDPA-NOTICE: {file}:{line} object not resolved for {field}; add a fixtureObjects entry or a typed
  receiver` (field name only, no value). A notice does not change the exit code. This is the remaining
  gap of object scoping, and it is reported on every run, not hidden (ASM-TE011-20).

What this reaches (SRC-28):

- **Today (PS v6, API v4).** Four API properties on undescribed schemas carry an unambiguous personal
  name: `InteractionRequest.summary`, `TimelineItem.summary`, `AgentOutput.summary` and
  `FieldCaptureItem.fileName`. All four are now findings in a typed fixture.
- **Under the protective union, ACE schema copy.** 44 of its 62 tables are outside the dictionary. Their
  12 (table, column) pairs with an unambiguous union name are now findings, for example `address.address`,
  `address.city` and `email.person_key`. The 5 pairs with an ambiguous name are now notices. Columns of
  in-dictionary ACE tables that no dictionary row names are reached in the same way.

**Migrations use the dictionary at that point.** A file in the recovery migration folder is checked
against the dictionary as it stands after that file has been read (SPEC-TE011-001). Two consequences:

- The migration's own `sys_fields` rows count. RWB-E1-001's seed is checked against the classification
  it seeds.
- A mark added by a later migration does not turn a merged migration red. A merged migration is never
  edited (`AGENTS.md` §4.6), and the allow list never excuses a migration (SPEC-TE011-011). Instead the
  run prints `PDPA-NOTICE: {file}:{line} seeds {field}, marked personal by a later migration` (no value),
  so code owners can decide on a corrective migration (ASM-TE011-21; SPEC-TE011-018).

Every other scanned file is checked against the full dictionary (baseline, every migration, API).

**Dictionary and reference seed tables.** These rules alone keep `sys_fields`, `sys_objects`,
`data_product`, `lov_value`, `role` and `permission` seed rows clean. Their columns `field_name`,
`description`, `source_system` and `owner_role` share names with personal fields on other objects, but
the (object, field) pairs differ. Under the protective union, the only personal pair on those six tables
is `data_product.owner_user_id` (SRC-27). RWB-E1-001 seeds it `NULL` (SRC-24 SPEC-RWB-E1-001-006), and
`NULL` is never a finding. No table is exempted by name, so a personal column added to one of these
tables later is still checked. A system test proves this (TS-TE011-01).

**Other rules.**

- **SQL with no named column fails closed as a finding** (review SG5-03). In a scanned `.sql` file
  (migration, test or infrastructure), these statements are PDPA-FIXTURE-FIELD findings, with the field
  shown as `(columns not named)`:
  - an `INSERT INTO <t> VALUES …` with no column list and at least one literal other than `NULL` or
    `DEFAULT`;
  - an `INSERT INTO <t> SELECT …` with no column list and at least one such literal in the select list;
  - any `COPY <t> FROM …` or psql `\copy <t> from …`, with an inline data block, a file or a program.

  The lint cannot name the column of such a value, so it cannot show that the value is synthetic. Values
  are never read into the output. `INSERT … DEFAULT VALUES`, a column-less `INSERT … SELECT` with no
  literal, and `COPY … TO` are not findings. In a file the reader reads (the baseline, the recovery
  migration folder and configured dictionary files; SPEC-TE011-001), the reader already fails these forms
  closed on `sys_fields` (exit 2), and that takes precedence. In any other scanned `.sql` file a
  `sys_fields` statement is checked like any other statement. Outside the migration folder a finding can be
  allow-listed. In the migration folder it is fixed before merge, or after merge by a corrective
  migration (SPEC-TE011-011, -018).
- **SQL statement classes** (review SG6-01; orchestrator triage 2026-11-18T01:02). A scanned `.sql` file is
  split into statements by the quote-aware splitter (comments, string literals and dollar-quoted bodies
  respected). Each statement falls in exactly one class. An unrecognised statement fails closed as a
  finding, in the same way as SQL with no named column (ASM-TE011-27).
  1. **Position forms**, checked by (object, field) as above:
     - `INSERT INTO <t> (<cols>) VALUES …` and `INSERT INTO <t> (<cols>) SELECT …`, the select with any
       `FROM`, join, `WHERE` (for example `WHERE NOT EXISTS (…)`), `GROUP BY` or `ORDER BY`;
     - an optional read-only `WITH` prefix, where every common table expression is a `SELECT`;
     - an optional `ON CONFLICT [(<cols>) | ON CONSTRAINT <name>] DO NOTHING`;
     - an optional `ON CONFLICT … DO UPDATE SET <c> = <value> [, …] [WHERE …]`, where a literal value is
       a position on (`<t>`, `<c>`) and `EXCLUDED.<c>` is not a new value;
     - an optional `RETURNING …`;
     - `UPDATE <t> SET <c> = <value> [, …] [FROM …] [WHERE …] [RETURNING …]`.

     A value made only of literals (a cast such as `'x'::text`, or a concatenation of literals) counts as
     a literal. A column reference, parameter or function of columns is not a literal.
  2. **Non-position forms.** These raise no FIXTURE-FIELD finding. FIXTURE-ID still scans their text.
     - `CREATE`, `ALTER` and `DROP` of a TABLE, INDEX, VIEW, MATERIALIZED VIEW, SEQUENCE, SCHEMA, TYPE,
       DOMAIN, EXTENSION or TRIGGER, with `IF [NOT] EXISTS`, `UNIQUE`, `CONCURRENTLY` or `OR REPLACE`.
       `CREATE TABLE … AS` is not in this class; it is class 4.
     - `ALTER` and `DROP` of a FUNCTION or PROCEDURE, for example `DROP FUNCTION IF EXISTS` when a
       forward-only migration replaces a trigger function. `CREATE [OR REPLACE] FUNCTION | PROCEDURE` is
       class 3.
     - A `CHECK` literal in DDL is a rule, not a row. A **`DEFAULT` literal is a position** (review SG7-02)
       when it is not `NULL` and the pair (table, column) is resolved and personal. This covers `CREATE
       TABLE`, `ALTER TABLE … ADD COLUMN … DEFAULT` (which writes the value into every existing row) and
       `ALTER TABLE … ALTER COLUMN … SET DEFAULT`. It is checked like any value: a finding unless it
       starts with `SYN-`, and for a non-text type any literal. A `DEFAULT` on any other pair, or a
       function such as `now()`, raises nothing.
     - `COMMENT ON`, `GRANT`, `REVOKE`, `SET` and `RESET`.
     - Transaction control: `BEGIN`, `START TRANSACTION`, `COMMIT`, `ROLLBACK`, `SAVEPOINT` and `RELEASE`.
     - `SELECT` without `INTO`.
     - `DELETE`, `TRUNCATE`, `ANALYZE`, `VACUUM`, `REFRESH MATERIALIZED VIEW`, `LOCK` and `COPY … TO`.
     - psql meta-commands other than `\copy` (for example `\set`, `\echo`, `\i`), and an empty
       statement.
  3. **Procedural bodies.** The body of a `DO $$ … $$` block, or of a `CREATE [OR REPLACE] FUNCTION` or
     `PROCEDURE`, is split again into statements.
     - **`DO` blocks** run once, when the migration runs, so they can write seed data. Their statements
       are read as follows (review SG7-02):
       - No finding: reads and control flow (`SELECT … INTO` a variable, `PERFORM`, assignment, `IF`,
         `CASE`, loops, `EXIT`, `CONTINUE`, `GET DIAGNOSTICS`, and `OPEN`, `FETCH`, `MOVE` and `CLOSE`
         of a cursor over a literal query), `RAISE`, `ASSERT`, `RETURN` and `NULL`.
       - No finding: a direct statement of class 2, that is any statement in the class-2 list above (DDL,
         `COMMENT ON`, `GRANT`, `REVOKE`, `SET`, `RESET`, transaction control, `SELECT` without `INTO`,
         `DELETE`, `TRUNCATE`, `ANALYZE`, `VACUUM`, `REFRESH MATERIALIZED VIEW`, `LOCK` and `COPY … TO`;
         review SG9-02). The common guard `IF NOT EXISTS (SELECT 1 FROM pg_constraint …) THEN ALTER TABLE … ADD CONSTRAINT …; END IF;` is this case. A `DEFAULT` literal
         in such DDL is checked as in class 2.
       - No finding: an `EXECUTE` (or `OPEN … FOR EXECUTE`) whose argument is a string literal, or
         `format(<string literal>, …)` with a literal format string, when that text is class 2 (review
         SG8-03, SG9-02). The lint classes the text as it would class a top-level statement, with these
         rules ("the finding" is the body's `(DML in procedural body)` finding):
         - A `%I` specifier, in any positional, width or flag form (for example `%1$I`), is read as a
           name.
         - Every other specifier (`%s`, `%L`), in any positional, width or flag form (for example `%1$s`,
           `%2$L`, `%-10s`), gives the finding, except as the comment text of `COMMENT ON … IS`. Its
           value, which the lint cannot see, could be a clause or a literal (review SG10-03).
         - `%%` is a literal percent sign, not a specifier.
         - A `DEFAULT` clause whose table or column is a placeholder gives the finding, because the pair
           cannot be resolved.
         - A literal `DEFAULT` with a literal table and column is checked as a class-2 `DEFAULT`
           position: on a resolved personal pair, a value that class 2 does not accept gives a
           PDPA-FIXTURE-FIELD finding for that field, at the `EXECUTE` line.

         So `EXECUTE 'CREATE TABLE t AS …'` and `EXECUTE 'ALTER ROLE …'` (class 4) are findings, and so is
         `EXECUTE format('ALTER TABLE t %s', v)`.
       - Finding, as a catch-all: every other statement. This covers `INSERT`, `UPDATE`, `MERGE`,
         `COPY … FROM`, `CALL`, any other `EXECUTE` (a variable, a concatenation, or a literal that is not
         class 2), and a direct statement of class 4 (`CREATE TABLE … AS`, `ALTER ROLE`, `ALTER DATABASE`, `ALTER
         SYSTEM`, `IMPORT FOREIGN SCHEMA`) or any keyword not listed here. The block gives one finding at
         its first line, with field `(DML in procedural body)`.
     - **Function and procedure bodies** run later, on run-time values. Their `INSERT` and `UPDATE`
       statements are checked as position forms, so a literal in a personal position is a finding and
       `NEW.<c>` or a variable is not. Reads, control flow, direct class-2 statements and an `EXECUTE`
       of class-2 literal text raise nothing, as for `DO` blocks, under the same `EXECUTE` rules. Every
       other statement (`MERGE`, `COPY … FROM`,
       a column-less `INSERT` with a literal, `CALL`, any other `EXECUTE`, a class-4 statement or an
       unknown keyword) gives the `(DML in procedural body)` finding, by the same catch-all.
  4. **Anything else** gives one PDPA-FIXTURE-FIELD finding at the statement's first line, with field
     `(statement not recognised)`. Examples are `MERGE`, `CALL`, a top-level `EXECUTE` or `PREPARE`,
     `SELECT … INTO <table>`, `CREATE TABLE … AS`, a `WITH` prefix holding a data-modifying expression,
     `IMPORT FOREIGN SCHEMA`, `ALTER ROLE`, `ALTER DATABASE`, `ALTER SYSTEM` and any leading keyword not
     listed above.

  No class prints a value or SQL text. When a statement in a file the reader reads targets `sys_fields`,
  the reader's exit 2 (SPEC-TE011-001) takes precedence. In any other scanned file the statement is
  classed here like any other (review SG7-01). Lint-fixture files are not classed at all (SPEC-TE011-003). Outside the migration folder a finding can be allow-listed. In the
  migration folder it is fixed before merge, or after merge by a corrective migration (SPEC-TE011-018).

  **Known files** (revised after review SG6-01). On 18 Nov 2026 the scan roots hold no `.sql` file, and
  the migration folder holds only `README.md` (SRC-28). The earlier build orders merge before this story
  (D-RUN-06), and their files are scanned at this story's merge (SPEC-TE011-016, SPEC-TE011-018). Their
  specifications give this reading (SRC-30):

  | Order | Story | SQL it adds | Reading |
  |---|---|---|---|
  | 3 | RWB-E1-042 | The only production migration among orders 1–5 (its §12.3). Step 1 `CREATE TABLE IF NOT EXISTS`. Step 2 `ALTER TABLE … ADD COLUMN IF NOT EXISTS` (three columns, no `DEFAULT`). Step 3: 16 guarded constraint additions, each a `DO` block that tests `pg_constraint` by name and adds the constraint if absent. Step 4 `CREATE [UNIQUE] INDEX IF NOT EXISTS`. Step 5 `COMMENT ON`. Step 6 `INSERT … (<cols>) VALUES … ON CONFLICT (param_key) DO NOTHING`. Step 7 `INSERT … (<cols>) SELECT … WHERE NOT EXISTS (…)`. Step 8 a self-check `DO` block that only reads and raises. | Steps 1, 2 and 4–7 are class 1 or 2. Step 8 is a read-only `DO` body. Step 3 raises nothing if each guard runs its `ALTER TABLE … ADD CONSTRAINT` directly, or through `EXECUTE format('ALTER TABLE …', …)` with a literal format string and only `%I` placeholders (SPEC-TE011-008 class 3); a `%L` for a check-constraint value would be a finding. Its spec does not fix the form; a guard built by string concatenation would be a `(DML in procedural body)` finding, so `shared-updates.md` §3b asks for the direct form. None gives `(statement not recognised)`. Its columns name no PS v6 personal pair, so under PS v6 it gives 0 FIXTURE-FIELD findings. Its seed identity sits in `author_user_id` (DF-REF-156), which is not personal in PS v6 but is personal under the protective union. At RWB-E1-001's merge that is a later mark on a merged migration: one notice, not a finding (T7). |
  | 1 | RWB-E1-044 | No production migration. Lint fixtures under `backend/src/test/resources/migration-lint/`, malformed or out of class by design (T-044-20..22). Flyway fixtures under `backend/src/test/resources/flyway-fixtures/` (T-044-10..18). SRC-31. | The lint fixtures are in the lint-fixture class (SPEC-TE011-003): FIXTURE-ID only, no exit 2. They are synthetic (its SPEC-010), so 0 findings. The Flyway fixtures are test fixtures with every rule. `CREATE TABLE` and `REFERENCES` are class 2. The AC8 statement on a missing table is not fixed in form (T-044-14): as DDL or a named-column `INSERT` with synthetic names it gives 0 findings; as a column-less `INSERT` with a literal it gives a `(columns not named)` finding, handled as SPEC-TE011-003 "If a merged Flyway fixture gives a finding" says. |
  | 2, 4 | RWB-TE-001, RWB-TE-002 | None (D-RUN-17; TE-002's UT-15 uses a synthetic path). | Nothing to scan. |
  | 5 | RWB-TE-003 | None. `ContractFixtures` is Java test source. | Scanned as Java test source. |

  The implementation run of this story re-checks the files as merged and records the result for each
  one (SPEC-TE011-016 state (1)). The Physical Schema v6 copy is not scanned, and it has 0 column-less
  INSERTs and 0 `COPY` statements. RWB-E1-001 uses named columns (its T10). The `infra/postgres/init/`
  scripts are shell scripts and a grants include file (`20-grants.sql.inc`). They load the schema copies
  with `psql -f`, hold no `COPY` and no data `INSERT`, and are not `.sql` positions (SRC-28; grep, 18 Nov
  2026). `shared-updates.md` §3b asks the orchestrator to pass these rules to the planners of orders 1–5.
- `NULL`, an empty string and SQL `DEFAULT` are never a finding.
- Non-text personal fields (`date_of_birth` DATE; `capture_latitude`, `capture_longitude` numeric) cannot
  carry the prefix. Any non-null literal in such a position is a finding. Outside the migration folder
  it can be allow-listed (BR3 read as written; DGL-08). In the migration folder no allow entry applies
  (SPEC-TE011-011), so the value there must be `NULL` or come from a column reference or function, not a
  literal. A migration therefore cannot seed a literal into a NOT NULL non-text column that is personal
  at that point. Under the protective union this covers `parameter_value.author_user_id` (DF-REF-156,
  uuid) and `reference_version.author_user_id` (DF-REF-166). No known story needs such a seed. A story
  that does raises it before planning (`shared-updates.md` §3b).
- SQL inside a Java or TypeScript string literal is not a SQL position. The lint does not parse
  embedded SQL; the literal is still scanned by FIXTURE-ID.
- AC4: `last_name = 'TESTNAME'` → finding; `'SYN-LAST-0001'` → no finding. The TC-TE-011-04 fixture
  writes the object of the test dictionary's `last_name` row.

### SPEC-TE011-009 PDPA-FIXTURE-ID (BR4; X3; AC3)

A finding is raised, in every scanned file (BR4 "anywhere in code or tests"; ASM-TE011-13), for a token
that matches one of three configured patterns. `{field}` in the output is the pattern name.

| Pattern name | Match (ASM-TE011-08..10) |
|---|---|
| `thai_national_id` | 13 digits, contiguous or as `d-dddd-ddddd-dd-d`, not adjacent to another digit, **and** a valid check digit: with digits d1..d13, `d13 = (11 − (Σ_{i=1..12} d_i × (14 − i)) mod 11) mod 10` |
| `thai_mobile` | National form: `0`, then `6`, `8` or `9`, then 8 digits (10 digits), optionally grouped 3-3-4 with `-` or space. International form: `+66` or `66`, optional separator, then `6`, `8` or `9` and 8 digits (9 digits), optionally grouped 2-3-4 with `-` or space. Not adjacent to another digit. The bare `66` prefix widens false positives (ASM-TE011-09) |
| `email` | an e-mail address whose domain is not in `exampleDomains` (default: `example.com`, `example.net`, `example.org` and their subdomains, and any domain under the reserved TLDs `.test`, `.example`, `.invalid`, `.localhost`) |

- A 13-digit number with an invalid check digit is not a finding (BR4 "with a valid check digit").
- AC3: the test writes a JSON fixture whose `idNoMasked` holds a 13-digit number with a valid check
  digit, generated at run time into a temporary directory and deleted afterwards; the lint scans that
  directory and fails with PDPA-FIXTURE-ID. No such number is stored in the repository (SRC-01 §17;
  story defect SRC-04 step 4 resolved this way).
- The same holds for every failing value in the lint's own tests (national ID, mobile number, e-mail
  outside the example domains): each is built at run time. The self-scan of `tools/pdpa-lint/**`
  (SPEC-TE011-003) fails the build if one is stored.

### SPEC-TE011-010 Masking helper exemption (X8; AC8)

A personal field use that is an argument (directly or nested) of a call to a method listed in
`maskingHelpers` (fully qualified `Type.method` for Java, `module#function` for TypeScript) is not a
finding for LOG-FIELD, EXCEPTION or TOSTRING. The production list is empty until the common module
publishes its PII logging interface (SRC-01 §3 "assumed published"; OPEN-024; ASM-TE011-07). AC8 is
proven with a helper name configured in the lint's test configuration.

### SPEC-TE011-011 Allow list (BR6; X6; AC6; contract "Allow list entry")

`tools/pdpa-lint/pdpa-allow.yaml` (ASM-TE011-11): a list of entries.

| Field | Required | Rule |
|---|---|---|
| `rule` | Yes | One of the six rule IDs |
| `path` | Yes | Glob relative to the repository root |
| `line` | One of `line` / `pattern` | Positive integer |
| `pattern` | One of `line` / `pattern` | Regular expression matched against the text of the source line |
| `owner` | Yes | Non-empty |
| `reason` | Yes | Non-empty |
| `expires` | Yes | ISO date `YYYY-MM-DD`; the entry excuses findings up to and including that date, in time zone Asia/Bangkok |

- A finding is excused only by a matching entry that is valid and not expired (BR6).
- An entry with a missing or invalid field makes the run fail with exit code 2, naming the entry index
  (BR6; §17 "always has an owner and an expiry date").
- **The allow list never excuses a migration.** An entry whose `path` glob matches any file in the
  recovery migration folder (from `rwb.flyway.location`, today
  `backend/src/main/resources/db/modulemigration/recovery/`) is invalid: exit
  2, naming the entry index. Every entry must expire, and a merged migration can never be edited
  (`AGENTS.md` §4.6). An entry for a migration would therefore expire and fail every later pipeline
  with no fix available. A finding in an unmerged migration is fixed in the file before merge. A
  finding in a merged migration is handled by a corrective migration (SPEC-TE011-018). A later
  mark that touches a merged migration gives a notice, not a failure (SPEC-TE011-008). The allow list is
  for editable files only (ASM-TE011-12).
- A finding matched only by an expired entry fails the build and prints
  `allow entry expired: {rule} {path} since {date}` (SRC-01 §14), in addition to the finding line.
- An expired entry that matches no finding does not fail the build (ASM-TE011-11).
- AC6: entry for PDPA-FIXTURE-FIELD in `ace-service/src/test/resources/recovery/legacy-seed.sql`
  expiring 2026-11-30; run as of 2026-12-01 → build fails with "allow entry expired". The run date is
  injectable for tests (ASM-TE011-19).

### SPEC-TE011-012 Output, exit and determinism (flow step 7; BR7; contract "Output", "Idempotency", "Restart")

- One line per unexcused finding, in the SRC-01 §14 form:
  `{rule}: {file}:{line} uses personal field {field}. Remove it or use the masking helper.`
  `{file}` is relative to the repository root. `{field}` is the dictionary field name; when the matched
  token differs, the token follows in parentheses, for example `last_name (lastName)` (AC1 names
  `first_name`, AC7 names `lastName`; ASM-TE011-14).
- The lint never prints a value found, a source line, or a fixture value, including in its own error and
  exception messages (BR7). A parse error names the file and line only.
- Lines are sorted by file, line, rule, field. The same commit and dictionary give the same output.
- After the finding lines, the run prints the `PDPA-NOTICE:` lines of SPEC-TE011-001 and -008, sorted
  the same way, then a count of each kind. They are four: an unmarking, an object that could not be
  resolved for an ambiguous name, a merged migration that touches a later mark, and a finding in a merged
  migration accepted by a corrective migration (SPEC-TE011-018). The `PDPA-SCOPE:` lines of SPEC-TE011-003 and -013
  follow the notices. A notice carries a
  field ID or field name, a file and a line, never a value. It does not change the exit code. Notices
  are kept in the CI artifact with the console output.
- Exit code: 0 no unexcused finding; 1 at least one; 2 configuration or input error, including an
  unsupported dictionary statement (SPEC-TE011-001), an allow entry on a migration (SPEC-TE011-011), a
  scan configuration that excludes or omits the migration folder or lets a lint-fixture root cover it,
  a lint-fixture root outside the test roots, a migration folder that does not match
  `rwb.flyway.location` (SPEC-TE011-003), a corrective migration in the migration folder that names an
  unknown file (SPEC-TE011-018), and, where the changed-file list is built, a target branch that cannot
  be resolved or has no merge base with HEAD; also a changed-file option whose `--branch` is
  missing, empty or `HEAD` (SPEC-TE011-013) (ASM-TE011-14). A lint-fixture file never gives exit 2 from
  its content.
- The lint holds no state between runs; a failed run is repeated by rerunning the pipeline.

### SPEC-TE011-013 Pipeline job (flow step 7; §13 build step 6; A-09 PDPA part)

- New job `pdpa-lint` in `.gitlab-ci.yml`, stage `verify`, no `rules:` filter, so it runs in every
  pipeline that file creates, as the existing `backend-unit` and `frontend-check` do. The file has no
  `workflow:` block, so GitLab creates a pipeline for every branch push and every tag push: branch
  pipelines on every branch, which covers `main`, `develop-recovery` and `develop` (D-RCV-50,
  L-RCV-13), and tag pipelines. It creates no merge request pipeline (review SG8-04, SG10-01). The
  job sets `GIT_DEPTH: 0`, so the clone holds the history that `git merge-base` needs.
- The job runs the tool's unit tests with coverage verification, then the lint over the repository; any
  non-zero exit fails the job. `pdpa-rules.yaml` and the console output are kept as artifacts
  (`when: always`).
- **Changed-file list** (required; SPEC-TE011-018 condition (e); review SG7-03, SG9-03). The lint takes
  the files that the change under review adds, modifies or renames, and never accepts a corrective
  migration for a migration on that list. The list exists only for a change into
  `changedFiles.targetBranch` (default `develop-recovery`), the one branch where a story's migration can
  still be fixed in its file. The tool's `ChangedFileList` component takes `--changed-files-from-git
  <target>` and `--branch <name>`, the branch under test. It decides first, before any git command:
  - **Built** when `<target>`, with any `origin/` prefix removed, equals `changedFiles.targetBranch`,
    and `<name>` is neither that branch nor one of `changedFiles.protectedBranches` (default `main`,
    `develop`; L-RCV-13). It runs `git merge-base <target> HEAD`, then `git diff --name-only
    --diff-filter=AMR <merge-base>..HEAD`. This reads repository metadata only: no database and no
    network. If `<target>` cannot be resolved, the run fails with exit 2, `changed-file list: target
    branch {name} not found`. If `git merge-base` finds no common ancestor (for example in a shallow
    clone, or with unrelated histories), the run fails with exit 2, `changed-file list: no merge base
    with {name}`; it never falls back to an empty list. The run prints `PDPA-SCOPE: changed-file list
    against {target}: {n} files`.
  - **Not built** in every other case: a target other than `changedFiles.targetBranch` (for example a
    promotion merge request into `develop` or `main`); a run on `changedFiles.targetBranch` itself; a run
    on a protected branch (for example a `develop` or `main` pipeline after a squash or cherry-pick
    promotion); or a run without `--changed-files-from-git`, as in a GitLab tag pipeline. No git
    command runs, so neither exit 2 above can occur. Condition (e) of SPEC-TE011-018 is not evaluated. The run prints
    `PDPA-SCOPE: changed-file list not built: target {target}, branch {name}` (or `none`). Such a run
    carries only files that met (e) when they merged into `changedFiles.targetBranch`, so promoting
    `develop-recovery` never fails for lack of a changed-file list.
  - `--changed-files-from-git` with `--branch` missing, empty or `HEAD` (a detached checkout) fails with
    exit 2, `changed-file list: branch not determined`, before any other check (review SG10-01).
    GitLab branch and merge request pipelines always pass a branch name; the local caller passes `HEAD`
    only on a detached checkout (below).
  - **GitLab** (branch and tag pipelines; review SG10-01):
    - **Tag pipeline** (`$CI_COMMIT_TAG` set): the job fetches nothing and passes no changed-file option,
      so the list is not built. A release tag on `main` after a squash promotion therefore never fails
      on condition (e).
    - **Branch pipeline** (`$CI_COMMIT_BRANCH` set): the job fetches `changedFiles.targetBranch` with a
      non-fatal fetch (a failed fetch is ignored), then passes `--changed-files-from-git
      origin/<targetBranch> --branch "$CI_COMMIT_BRANCH"`. The tool decides as above. On
      `develop-recovery`, `main` and `develop` it builds no list, so a failed fetch there has no effect.
      Where it builds the list and the fetch failed, the target cannot be resolved and the run gives
      exit 2 (T14).
    - **Merge request pipeline**, where a later change to `.gitlab-ci.yml` adds one: the same non-fatal
      fetch of the merge request's target, then `--changed-files-from-git
      origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME --branch "$CI_MERGE_REQUEST_SOURCE_BRANCH_NAME"`. A
      merge request into any target other than `changedFiles.targetBranch` builds no list.
  - **Local merge in this repository.** No GitLab pipeline runs here. The orchestrator merges a story
    branch into `develop-recovery` only on a green `./scripts/dev.ps1 test` (D-RUN-06; SRC-31). This
    story therefore changes `scripts/dev.ps1`. The `test` command runs the lint after the Gradle tests,
    with `--changed-files-from-git develop-recovery --branch <current branch>` (from `git rev-parse
    --abbrev-ref HEAD`). The target is configuration (`changedFiles.targetBranch`). On
    `develop-recovery`, `main` and `develop` the tool builds no list. On a detached checkout `git
    rev-parse` prints `HEAD`, and the run gives exit 2, `changed-file list: branch not determined`; the
    local merge gate always runs on a named story branch. A new `pdpa-lint` command runs the
    same step alone (SRC-01 §10 "RW-TRIBE … Run the lint"). This is required, not a recommendation,
    because condition (e) is enforced only where the list is built.
- In ACE the same check runs in the ACE pipeline on the `develop-recovery` merge request (D-RCV-50; header
  comment of `.gitlab-ci.yml`). Its target is `develop-recovery`, so the list is built there.

### SPEC-TE011-014 Code owners for lint configuration (§10; X11; TC-TE-011-11)

- Add the line `/tools/pdpa-lint/ @scb-ace/techx-recovery-tech-leads` to section `[Recovery module]` of
  `.gitlab/CODEOWNERS`, the GitLab-format file that RWB-TE-002 delivers (SRC-23 SPEC-RWB-TE-002-001;
  L-RCV-12). This covers `pdpa-allow.yaml`, `pdpa-lint.yaml` and the rule generator, so allow-list and
  rule changes need a tech-lead approval (SRC-01 §10).
- The entry must pass the RWB-TE-002 validator (SRC-23): anchored, with no wildcard (V4); owner listed in
  `.gitlab/codeowners-register.yaml` (V7; the handle is already there for `[Recovery module]`); pattern
  matches a file (V9). It is therefore added in the same merge as `tools/pdpa-lint/`, never before.
- Dependency: RWB-TE-002 (build order 4) must be merged first. SRC-16 BR1/BR2 and the RWB-TE-002 file
  content do not cover `tools/`, so the entry is this story's change. The repository host and team
  handles are open (OPEN-038).
- TC-TE-011-11 is executed on the real repository host only; until OPEN-038 closes and RWB-TE-002 is
  built it is recorded as `BLOCKED`, not passed (ASM-TE011-17).

### SPEC-TE011-015 Configuration, no business values in code (§13 Configuration; §17 guardrail 1)

`tools/pdpa-lint/pdpa-lint.yaml` holds: dictionary sources (baseline file, migration folder, further
dictionary files), API specification path, scan roots and exclusions, synthetic prefix (`SYN-`), example
domains, the three FIXTURE-ID patterns, logger names, exception types, masking helpers, entity suffixes,
and `fixtureObjects` (path glob → object, for JSON fixtures; empty by default). Code holds no field name,
object name, prefix, domain or pattern. The six dictionary and reference seed tables are not listed
anywhere: they need no exemption (SPEC-TE011-008). No root or exclusion can leave out the migration
folder (SPEC-TE011-003). `lintFixtureRoots` (default `backend/src/test/resources/migration-lint/**`;
each root must lie under the test roots) and
`changedFiles.targetBranch` (default `develop-recovery`) and `changedFiles.protectedBranches` (default
`main`, `develop`) are configuration too. The migration folder is
read from `rwb.flyway.location` in `application.yaml`, not set here (SPEC-TE011-003).
Owned by the TechX tech leads through code owners (SPEC-TE011-014); the personal field marks are owned
by Compliance through the dictionary (DL26).

### SPEC-TE011-016 Test dictionary and baseline pass (§13 "Done when"; `AGENTS.md` §6)

- System tests (TC-TE-011-01..10) run the full lint (reader → generator → scan → allow list → output)
  against fixture trees under `tools/pdpa-lint/src/test/resources/`, with a synthetic test dictionary that
  marks the SRC-01 Background fields (`first_name`, `last_name`, `cif_no`, `id_no_masked`, `date_of_birth`,
  `contact_value`, `summary`, `field_value`) plus `id_no_last4` and `contact_value_masked` (SRC-05).
**Zero-finding baseline, restated.** "Done when … the lint runs on main with zero findings" is a
condition at every merge, not only at this story's merge. The `pdpa-lint` job has no `rules:` filter
(SPEC-TE011-013). Exit code 0 is required in three states:

| State | Dictionary | Expected result and evidence |
|---|---|---|
| (1) This story's merge | Baseline: PS v6 copy, 18 fields; the migration folder holds no `sys_fields` statement. API v4: 5 properties | 0 findings. The only e-mail literals are in `local.test`, a reserved `.test` domain (ASM-TE011-08). No 13-digit number, no Thai mobile number, no personal-field literal (grep, 17 Nov 2026). With the round-5 rule (unresolved positions use the name rule), the test roots hold 0 positions with one of the 18 names and a non-`SYN-` literal, and the scan roots hold no `.sql` file, so the column-less SQL rule finds nothing (SRC-28). The run also covers every migration and fixture that orders 1–5 merged before this story (SRC-30, SRC-31; "Known files" in SPEC-TE011-008). RWB-E1-044's lint fixtures under `backend/src/test/resources/migration-lint/` are in the lint-fixture class (SPEC-TE011-003), so their deliberately malformed and out-of-class SQL gives neither exit 2 nor a statement-class finding. FIXTURE-ID still applies to them, and they are synthetic (TS-TE011-08). RWB-E1-044's Flyway fixtures keep every rule; 0 findings are expected if its AC8 statement is DDL or names its columns, and any finding is handled as SPEC-TE011-003 "If a merged Flyway fixture gives a finding" says. The implementation run lists each such file with its result. A finding in a merged migration is handled by a corrective migration (SPEC-TE011-018), never by an allow entry or an exclusion. The implementation stage records the run. |
| (2) RWB-E1-001's merge, if it seeds the protective union | RWB-E1-001's migration replaces the baseline rows: 526 fields | 0 findings is RWB-E1-001's merge condition (SPEC-TE011-017). On the files that exist on 18 Nov 2026, 0 findings are expected; every file merged after the 18 Nov 2026 evidence and before RWB-E1-001 (orders 1–8) was checked by this lint, at this story's merge (orders 1–5) or at its own merge (orders 6–8), but against the smaller baseline dictionary, so RWB-E1-001's merge request is where any new finding on them first shows. In a merged migration such a finding is a T7 notice (point in time), not a failure. The four back-end log calls use no union name. The keys in `infra/mock-oidc/config.json` (`name`, `sub`, `preferred_username`, `roles`, `aud`) are not personal on any object. The SQL in `RecoveryDatabaseIT.java` sits in Java strings, which are not a SQL position (SPEC-TE011-008). An upper-bound scan that treats every test-root position as unresolved finds one candidate under the union, `final_call` at `RecoveryDatabaseIT.java:110`, and it is inside such a Java text block (SRC-28). Every column of the PS v6 seed INSERTs is described on its own table, so the round-5 rule leaves seed rows resolved (SRC-28). On RWB-E1-001's own migration, the six dictionary and reference seed tables raise 0 FIXTURE-FIELD findings under (object, field) matching. The only personal pair among them is `data_product.owner_user_id`, which RWB-E1-001 seeds `NULL` (SRC-24, SRC-27). The 4,274 name-only findings that review SG4-01 counted do not arise. No allow entry may be used for it (SPEC-TE011-011). |
| (3) Every later merge | As changed by migrations | 0 findings, or the merge request fails. Notices do not fail the run; they are read by code owners. |

- The implementation stage records the run for state (1). It also runs the lint on a synthetic,
  E1-001-shaped migration under a test dictionary that marks the protective-union names (TS-TE011-01).
  That is the evidence available before RWB-E1-001 exists.
- "Zero findings" is measured against the dictionary as seeded and changed by migrations. It does not
  show that fields marked only by reference load (DGL-13), or Inventory v4 fields the dictionary leaves
  unmarked, stay out of code, fixtures and logs. In state (1) those are the 9 Restricted fields and the
  other unmarked "Yes" fields ("Personal data classification used"). The implementation report must
  repeat this limit next to the zero-finding result. It must also state which of states (1) and (2) the
  repository is in.
- The fixture trees contain no value that matches a FIXTURE-ID pattern; such values are written at run
  time into temporary directories (SPEC-TE011-009).

### SPEC-TE011-017 Cross-story obligations and seams (D-RUN-08; DGL-13; orchestrator triage 2026-11-18)

This story is build order 6. It depends on no later story. The items below are what later stories must
meet, or the seams they own. `shared-updates.md` asks the orchestrator to pass each one to the owning run (§3, §3b).

| Story (order) | Obligation or seam | Why |
|---|---|---|
| RWB-E1-044, RWB-TE-001, RWB-E1-042, RWB-TE-002, RWB-TE-003 (1–5) | **SQL merged before this story is scanned at this story's merge.** Every `INSERT` names its columns. No `COPY … FROM`, `MERGE`, `CALL`, or any statement in a `DO` block that the class-3 rules do not list. A guard in a `DO` block runs its DDL directly, or through `EXECUTE format(…)` with a literal format string and only `%I` placeholders (SPEC-TE011-008 class 3), never by concatenation. No literal other than `NULL` or a `SYN-` value in a PS v6 personal pair. No FIXTURE-ID match. Fixtures use `SYN-` values in personal positions. Once a migration is merged, a corrective migration under its story key is the only remedy (SPEC-TE011-018). RWB-E1-044's lint fixtures (`migration-lint/`) are in the lint-fixture class and get FIXTURE-ID only. Its Flyway fixtures (`flyway-fixtures/`) are test fixtures with every rule; a finding there is handled by this story (SPEC-TE011-003). This story adapts to RWB-E1-044 as specified; nothing is asked of RWB-E1-044, and the rules in this row are for orders 2–5. | Review SG6-01, SG7-01, SG7-02; orchestrator triage 2026-11-18T01:02 and 04:54; D-RUN-06; SRC-30, SRC-31. Requested through the orchestrator (`shared-updates.md` §3b). |
| RWB-E1-001 (9) | **Seed the protective classification as parseable `INSERT` values.** The `sys_fields` seed in its baseline migration uses form R1 of SPEC-TE011-001: single-row or multi-row `INSERT … VALUES` with literal `field_id`, `object_name`, `field_name` and `is_personal`. It sets `is_personal` in the row itself. It does not use a bulk `UPDATE`, `ON CONFLICT`, `INSERT … SELECT` or `COPY`; any of those fails this lint closed. | Without this, the 526-field union never reaches the lint (review SG4-03). |
| RWB-E1-001 (9) | **Pass this lint with zero findings** on its merge request, with no allow-list entry for its migration (SPEC-TE011-011). Its seed values for personal (object, field) pairs are `NULL` or start with `SYN-`. | The `pdpa-lint` job runs on every pipeline (SPEC-TE011-013). |
| RWB-E1-064 (13) | **Seam: protecting `is_personal` marks against a later dictionary load (D-RCV-29).** RWB-E1-064 owns the dictionary load handler (`DataDictionaryLoader`). Its story file lists `is_personal` (DF-REF-105) as Read (SRC-29). This lint does not see a load: it covers committed SQL migrations, fixtures and log statements only, and story §13 and §17 forbid a database read. The decision on which governed path may change an `is_personal` mark, and on whether an approved change reaches a committed file, is RWB-E1-043 open item R4. R4 is owned by RW-COMPLY, and it blocks RWB-E1-064. RWB-E1-043 §3.2 already tells RWB-E1-064 that `validate` refuses a file whose `is_personal` differs from the value in force (422 MSG-P1-002), and that `apply` and `onRolledBack` never write `is_personal` (SRC-25). If the decision is a committed export in form R1, SPEC-TE011-001 item 3 reads it with no code change. | Orchestrator triage 2026-11-18T00:35 (SRC-26); Decision Log v10 D-RCV-29 (SRC-22); D-RUN-08; DGL-13. |
| RWB-E1-043 (8) | **Load pipeline only.** SPEC-RWB-E1-043-031 builds the version log, the change summary by field ID and non-author approval (SRC-25). It does not build the dictionary handler, does not refuse removal of a mark and does not make loads visible to this lint. Revision 3 of RWB-E1-043 corrected GAP-38: nothing is asked of RWB-TE-011, and its §3.2 item 5 says this lint covers committed SQL, fixtures and logs and is not a run-time check. The open question goes to its open item R4 (owner RW-COMPLY). | SRC-25; SRC-26. |

Until RWB-E1-001 merges, the lint's dictionary is the PS v6 baseline (state 1 of SPEC-TE011-016). The
residual risk and its two outcomes are in "Personal data classification used".

### SPEC-TE011-018 Findings in a merged migration: corrective migration (D-RCV-28; `AGENTS.md` §3.7, §4.6; review SG6-01)

When this story merges (order 6), the lint runs over every migration and fixture already on
`develop-recovery`, including the SQL of orders 1–5 (SRC-30). A merged migration is never edited
(`AGENTS.md` §4.6), and the allow list never excuses a migration (SPEC-TE011-011). The only remedy for a
finding in a merged migration is a corrective migration (D-RCV-28; `AGENTS.md` §3.7). It takes the next
`<seq>` and keeps the original story key on line 1 (`-- Story: <story key>`). Line 2 is
`-- Fix: <reason>`.

The lint recognises a corrective migration as follows (ASM-TE011-26). **Scope:** these rules apply only to
files in the recovery migration folder (SPEC-TE011-003). Line 2 of any other file is not read for
corrective names, so a `-- Fix:` line in a test or lint fixture never gives exit 2 (review SG7-01,
SG7-03).

- **Naming the original.** Line 2 of the corrective file C starts `-- Fix:`. After the reason it names
  each original it corrects, for example `-- Fix: replace non-synthetic seed value; corrects
  V0003__rwb_e1_042_<name>.sql`. Every token on line 2 that matches `V\d{4}__[A-Za-z0-9_]+\.sql`
  counts as a named file. The reason must not be empty (RWB-E1-044 rule L-FIX-LINE2).
- **Accepted findings.** A finding of a SQL rule in an original O is accepted only when a file C in the
  migration folder meets all of these conditions. The SQL rules are FIXTURE-FIELD (including
  `(columns not named)`, `(statement not recognised)` and `(DML in procedural body)`) and FIXTURE-ID.
  - (a) C sorts after O in Flyway version order (`<seq>`).
  - (b) C's line-1 story key equals O's line-1 story key.
  - (c) C's line 2 starts `-- Fix:`, has a non-empty reason and names O.
  - (d) For a finding with a target table, C holds an `UPDATE`, `DELETE` or `TRUNCATE` on that table,
    with the schema qualifier removed. For a finding in a `DEFAULT` (FIXTURE-FIELD or FIXTURE-ID), C
    must also hold `ALTER TABLE <t> ALTER COLUMN <c> DROP DEFAULT` or `SET DEFAULT`. A finding with no
    target table needs no table write: (d) is met, and (a) to (c) and (e) still apply (review SG8-01).
    The target table of each finding kind (review SG7-03, SG8-02). The rules that read a table apply
    wherever the statement is: at top level, inside a `DO`, function or procedure body, and inside
    literal `EXECUTE` text or a `format` string whose table is literal (review SG10-02). "None" applies
    only where no written table can be read.

    | Finding | Target table |
    |---|---|
    | FIXTURE-FIELD on a position (`INSERT`, `UPDATE`, `ON CONFLICT … DO UPDATE`, `DEFAULT`) | The position's table |
    | FIXTURE-FIELD `(columns not named)` | The table of the `INSERT` or `COPY` |
    | FIXTURE-FIELD `(statement not recognised)` | The table the statement writes, when the lint can read it (`MERGE INTO <t>`, `SELECT … INTO <t>`, `CREATE TABLE <t> AS`); otherwise none |
    | FIXTURE-FIELD `(DML in procedural body)` | Each table the body writes that the lint can read: the table of an `INSERT`, `UPDATE`, `MERGE INTO`, `COPY … FROM` or `CREATE TABLE <t> AS` in the body, directly or in literal `EXECUTE` text with a literal table name. C needs an `UPDATE`, `DELETE` or `TRUNCATE` on each. None only when no such table can be read (for example only `CALL`, a non-literal `EXECUTE`, `ALTER ROLE`, or a table given by a placeholder) |
    | FIXTURE-ID in a value of an `INSERT` or `UPDATE`, wherever the statement is: top level, in a `DO`, function or procedure body, or in literal `EXECUTE` text (review SG9-01, SG10-02) | That statement's table |
    | FIXTURE-ID in a `DEFAULT` (`CREATE TABLE`, `ADD COLUMN`, `SET DEFAULT`) | That table; C also needs `ALTER COLUMN … DROP|SET DEFAULT` |
    | FIXTURE-ID in any other statement | The table the statement writes, when the lint can read it (`COPY <t>` with its data block, `MERGE INTO <t>`, top-level `SELECT … INTO <t>`, `CREATE TABLE <t> AS`), wherever the statement is; otherwise none, that is only where no written table can be read (a comment, `COMMENT ON` text, other DDL, `CALL`, `SET`, or other text from which no written table can be read) |
  - (e) O is not on the changed-file list of the change under review (SPEC-TE011-013). (e) is evaluated
    only where the list is built: a change into `changedFiles.targetBranch` from a branch that is not
    protected (the GitLab pipeline of a story branch, or the local merge into `develop-recovery`). There,
    a file added or edited in the same change is fixed in the file, not corrected, and (e) applies to
    every finding, with or without a target table. Where the list is not built (on the target branch
    itself, on `main` or `develop`, or in a merge request into another target), (e) is not evaluated;
    such a run carries only files that met (e) when they merged into the target branch (review SG9-03).
- **Output.** An accepted finding prints
  `PDPA-NOTICE: {file}:{line} {rule} {field} corrected by {corrective file}` (no value) in place of the
  finding line. It does not change the exit code. A finding that fails any condition stays a finding.
- **Unknown file.** A `-- Fix:` line of a file in the migration folder that names a file absent from
  that folder gives exit 2: `corrective migration names unknown file: {file}:2`.
- **C is scanned** like any migration, against the dictionary at its point in Flyway order. A finding in
  C is a finding.
- **Nothing else excuses O.** No allow entry (SPEC-TE011-011) and no exclusion (SPEC-TE011-003) may be
  used. While a finding in a merged migration is not yet corrected, this story's merge request fails. The
  orchestrator assigns the corrective migration to the story that owns O, which merges it under O's story
  key first (D-RUN-06, D-RUN-07).
- **Limit.** The lint checks the naming, the header, the order, the target table and the changed-file
  list. It does not check that C actually removes or replaces the value. Code owners check that in review
  (SPEC-TE011-014). A FIXTURE-ID value stays in O's file and its history, which no migration can change.
  Removing it is a matter for RW-COMPLY, outside the lint.

## Field-level behavior matrix

The story has no screen and no entity it writes. The "fields" are the configuration and file
contracts.

| Field | Source / prefill | Editable by | Constraints |
|---|---|---|---|
| Personal field list | `sys_fields.is_personal` as seeded and changed by migrations, `x-personal-data` (SPEC-TE011-001); keys (object, field) | Compliance, through the dictionary (DL26); a reference-load mark is not visible (DGL-13) | Never in lint code (BR1); unsupported `sys_fields` statement fails closed |
| `fixtureObjects` | `pdpa-lint.yaml` (SPEC-TE011-015) | TechX tech leads (code owners) | Path glob → object name in the dictionary |
| `pdpa-rules.yaml` | Generated each run (SPEC-TE011-002) | Nobody | Deterministic; not committed |
| `pdpa-allow.yaml` entry | Pull request | Proposed by RW-TRIBE; approved by TechX tech leads (code owners) | All of `rule`, `path`, `line`/`pattern`, `owner`, `reason`, `expires` (SPEC-TE011-011) |
| `pdpa-lint.yaml` | Repository file | TechX tech leads (code owners) | SPEC-TE011-015 |
| Synthetic prefix | `pdpa-lint.yaml`, default `SYN-` | TechX tech leads | Case-sensitive prefix match |
| Run date | System clock, Asia/Bangkok; injectable in tests | — | ISO date |

## Status-transition matrix

None (SRC-01 §9). The only state is the build result:

| Source | Condition | Target |
|---|---|---|
| Lint running | No unexcused finding, no input error | Pass (exit 0) |
| Lint running | ≥ 1 unexcused finding (including one matched only by an expired entry) | Fail (exit 1) |
| Lint running | Dictionary or API file missing or unparsable, unsupported statement writing `sys_fields`, duplicate seed row across migrations, `UPDATE` of an unknown `field_id`, empty field list, invalid allow-list entry (including any entry on a migration), configuration (including one that excludes or omits the migration folder, a lint-fixture root that covers it or lies outside the test roots, or a migration folder that does not match `rwb.flyway.location`), a corrective migration in the migration folder naming an unknown file, a changed-file target branch that cannot be resolved or has no merge base with HEAD (where the list is built), or a changed-file option whose `--branch` is missing, empty or `HEAD` | Fail (exit 2) |
| Lint running | Only notices (unmarking, unresolved object for an ambiguous name, later mark on a merged migration, finding in a merged migration accepted by a corrective migration) | Pass (exit 0); notices printed and kept |

## Exceptional-case behavior

| ID | Trigger | Behaviour | Output | SPEC |
|---|---|---|---|---|
| X1 | Log call writes a personal field | Build fails | PDPA-LOG-FIELD line | -004 |
| X2 | Log call writes a whole personal entity | Build fails | PDPA-LOG-ENTITY line | -005 |
| X3 | Fixture holds a valid Thai national identifier | Build fails | PDPA-FIXTURE-ID line, field `thai_national_id` | -009 |
| X4 | Personal field value without `SYN-` | Build fails | PDPA-FIXTURE-FIELD line | -008 |
| X5 | Field newly marked personal | Rules regenerate; existing uses found | PDPA-LOG-FIELD line | -001, -002, -004 |
| X6 | Matching allow entry expired | Finding fails the build | finding line + `allow entry expired: …` | -011 |
| X7 | Front-end console or logger call writes a personal property | Build fails | PDPA-LOG-FIELD line | -004 |
| X8 | Personal field passed through the masking helper | Passes | none | -010 |
| X9 | Exception message carries a personal field | Build fails | PDPA-EXCEPTION line | -006 |
| X10 | Entity text form includes a personal field | Build fails | PDPA-TOSTRING line | -007 |
| X11 | Allow-list change approved only by a non code owner | Merge refused by the repository host | Host: "Review required from code owners" | -014 |
| T1 | Dictionary or API file missing, unparsable or empty list | Fail closed | exit 2, file name only | -001 |
| T2 | Invalid allow-list entry, including any entry whose path matches a migration | Fail | exit 2, entry index | -011 |
| T3 | Source file the lint cannot parse, outside the lint-fixture class | Fail | exit 2, file and line, no source text | -012 |
| T4 | Statement writing `sys_fields` that the reader cannot interpret (for example `DELETE`, `COPY`, `INSERT … SELECT`, `ON CONFLICT`, bulk `UPDATE`), a duplicate seed row across migrations, or an `UPDATE` of an unknown `field_id` | Fail closed | exit 2, `dictionary statement not supported: {file}:{line}` or the duplicate/unknown ID message, no SQL text | -001 |
| T5 | A later source turns a mark from `true` to `false` | Applied; build result unchanged | `PDPA-NOTICE: {field_id} unmarked at {file}:{line}` | -001 |
| T6 | Unresolved fixture position (no object, or an object or field the dictionary does not describe) with an ambiguous personal name that is not an API personal name in an API-typed position | Not a finding | `PDPA-NOTICE: … object not resolved for {field} …` | -008 |
| T7 | Merged migration seeds a field that a later migration marks personal | Not a finding | `PDPA-NOTICE: … marked personal by a later migration` | -008 |
| T8 | Dictionary mark added or removed by a D-RCV-29 dictionary load | Not visible to the lint (committed files only) | none; seam owned by RWB-E1-064, decision in RWB-E1-043 open item R4 (RW-COMPLY) | -001, -017 |
| T9 | Scanned SQL with no named column: a column-less `INSERT` holding a literal, or `COPY … FROM` / `\copy … from` | Build fails | PDPA-FIXTURE-FIELD line, field `(columns not named)`, no value | -008 |
| T10 | Scanned SQL statement outside the recognised classes (for example `MERGE`, `CALL`), or any statement in a `DO`, function or procedure body that the class-3 rules do not list | Build fails | PDPA-FIXTURE-FIELD line, field `(statement not recognised)` or `(DML in procedural body)`, no SQL text | -008 |
| T11 | Finding in a merged migration, with a corrective migration that meets conditions (a) to (e) ((e) only where the changed-file list is built, SPEC-TE011-013) | Accepted; build result unchanged | `PDPA-NOTICE: {file}:{line} {rule} {field} corrected by {corrective file}`; a `-- Fix:` naming an unknown file gives exit 2 | -018 |
| T12 | Scan configuration whose exclusions or lint-fixture roots match, or whose roots miss, a file or probe path in the migration folder; a lint-fixture root outside the test roots; or a migration folder that does not match `rwb.flyway.location` | Fail | exit 2, `scan configuration excludes the migration folder: {config key}`, `lint-fixture root outside the test roots: {config key}` or `migration folder does not match rwb.flyway.location: {config key}` | -003 |
| T13 | Lint-fixture file that is malformed or holds statements outside the classes (RWB-E1-044 T-044-20..22) | No parse, no statement-class finding, never exit 2; FIXTURE-ID on the raw text | none, or a PDPA-FIXTURE-ID line | -003 |
| T14 | Where the changed-file list is built: a target that cannot be resolved, or no merge base between the target and HEAD (shallow clone, unrelated histories). Also `--changed-files-from-git` with `--branch` missing, empty or `HEAD` | Fail | exit 2, `changed-file list: target branch {name} not found`, `changed-file list: no merge base with {name}` or `changed-file list: branch not determined` | -013 |
| T15 | Changed-file list not built: no option (for example a GitLab tag pipeline), a target other than `changedFiles.targetBranch`, or a run on that branch or on a protected branch (`main`, `develop`) | Condition (e) not evaluated; no git command runs; a promotion never fails for lack of a list | `PDPA-SCOPE: changed-file list not built: target {target}, branch {name}` | -013, -018 |

## API change assessment

`NO_API_CHANGE`. No endpoint, schema, status code or message is added or changed. API Specification v4 is
an input file. Backward compatibility: not applicable. Versioning impact: none.

## Frontend Specification

- **Changes required: NO.** No screen, route, state, component, service or test under `frontend/` is
  added or changed. Front-end source and tests are scan input (SPEC-TE011-003).
- `frontend/e2e/platform.spec.ts` holds three `local.test` addresses; they pass under the default example
  domains (ASM-TE011-08). No change.
- Design evidence: `NOT_REQUIRED` (UI In Scope = NO). See `figma/figma_report.md`.
- Unit tests and coverage: `NOT_APPLICABLE` for the front-end surface. The TypeScript rules are unit- and
  system-tested inside the tool's own test suite with `.ts`/`.tsx` fixture files.

## Backend Specification

- **Application code: unchanged.** No change to `backend/src/main`, `backend/build.gradle.kts`, endpoints,
  entities, migrations, security, audit or runtime configuration.
- **Build tooling: new.** `tools/pdpa-lint/` (SRC-01 §13 Package) with components PersonalFieldReader
  (-001, including the quote-aware SQL statement splitter shared with the SQL fixture scanner), RuleGenerator
  (-002), the rule scanners (-004..-009, with object resolution for -008), CheckDigitMatcher (-009),
  allow-list handling (-011), ChangedFileList (-013) and PdpaLintStep (-012, -013). `scripts/dev.ps1` gains the lint step in `test` and a `pdpa-lint` command (SPEC-TE011-013). The splitter is the tool's own code; it does
  not depend on the migration lint of another story.
- Technology (ASM-TE011-01): Java 21 and Gradle, the back end's toolchain, so JaCoCo gives native
  coverage. No new third-party dependency without plan approval (BS-1.5; `AGENTS.md` §4.4); the plan
  names and pins any YAML/JSON parser it needs.
- Persistence boundary: none. Files only (SRC-01 §13 "Database. None"; §17 "the lint reads files only").
- Authorization: none at run time (SRC-01 §10). Change control through code owners (SPEC-TE011-014).
- Audit: none; no case or decision changes (SRC-01 §9).
- Contracts: `contracts/backend-apis.json` records `NO_API_CHANGE` and the file/CLI contract.

## Data model (file contracts)

```yaml
# pdpa-rules.yaml (generated; illustrative shape)
generatedFrom: { dictionary: [<file>...], api: <file> }
fields:
  - name: last_name            # sys_fields.field_name
    fieldId: DF-ACE-058
    object: v_ace_customer
    keys: [[v_ace_customer, last_name], [customer, surname]]   # second key from source_field
    unambiguousName: true      # every dictionary row named last_name is personal; used for unresolved positions
    dataType: TEXT
    variants: [last_name, lastName, getLastName]
apiPersonalNames: [capture_latitude, capture_longitude, extracted_value, field_value, summary]
entityTypes: [ContactEntity, ContactView, CustomerEntity, CustomerView, ...]
rules: [PDPA-LOG-FIELD, PDPA-LOG-ENTITY, PDPA-EXCEPTION, PDPA-TOSTRING, PDPA-FIXTURE-FIELD, PDPA-FIXTURE-ID]

# pdpa-allow.yaml (reviewed by code owners)
- rule: PDPA-FIXTURE-FIELD
  path: ace-service/src/test/resources/recovery/legacy-seed.sql
  pattern: "^INSERT INTO"        # or line: 12
  owner: <team or person handle>
  reason: <why>
  expires: 2026-11-30
```

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | SPEC-TE011-003 (scan input only) | No file under `frontend/` changes (Frontend Specification). | N/A. TS rule behaviour is covered in the backend (tool) row. |
| Backend | YES (build tooling `tools/pdpa-lint/`; application code unchanged) | REQUIRED | ≥ 80% for lines, branches, methods and instructions (JaCoCo LINE, BRANCH, METHOD, INSTRUCTION) on `tools/pdpa-lint` production classes, enforced by a coverage verification task that fails the job below threshold | SPEC-TE011-001..-018; BR1–BR7; AC1–AC10 | New code with logic (SRC-01 §13). BS-7.2 and testing standards §6 set 80%. Results and native reports per `.github/rules/implementation-execution-gates.md` under `output/<RUN_ID>/implement/unit-tests/`. | Per rule: positive (finding), negative (no finding), boundary and error path, listed in "Test requirements". Every test asserts that no fixture value appears in the output (BR7). |

## Test requirements

Story test cases (system level, the full lint against fixture trees; SRC-01 §16; SRC-05):

| TC | AC / BR | SPEC | Fixture and assertion |
|---|---|---|---|
| TC-TE-011-01 | AC1, BR2, BR7 | -004, -012 | Java file `recovery/casewf/internal/SampleService.java` logging `customer.getFirstName()`; exit 1; line names PDPA-LOG-FIELD, file, line, `first_name`; output contains no fixture value |
| TC-TE-011-02 | AC2, BR2 | -005 | Log call writing `customer` of type `CustomerEntity` (and a `CustomerView` variant, SRC-05); PDPA-LOG-ENTITY |
| TC-TE-011-03 | AC3, BR4 | -009 | Valid-check-digit 13-digit number generated at run time into a temp JSON fixture under key `idNoMasked`; PDPA-FIXTURE-ID; number absent from output; temp file deleted |
| TC-TE-011-04 | AC4, BR3 | -008 | SQL seed writing `last_name` on the test dictionary's object, value `TESTNAME` → PDPA-FIXTURE-FIELD; with `SYN-LAST-0001` → exit 0 |
| TC-TE-011-05 | AC5, BR1 | -001, -002, -004 | Dictionary v1 without `contract_no`: `account.getContractNo()` passes. Dictionary v2 adds a migration with `UPDATE sys_fields SET is_personal = true WHERE field_id = '<contract_no id>'` (form R2): rules regenerated with `contract_no`, PDPA-LOG-FIELD for `contract_no`. A second variant marks it through a multi-row `INSERT` (form R1) with the same result. This proves AC5 for the route the lint covers: changes by migration. A reference-load mark is outside the lint (DGL-13) |
| TC-TE-011-06 | AC6, BR6 | -011 | Entry expiring 2026-11-30; run as of 2026-12-01 → exit 1 and `allow entry expired: PDPA-FIXTURE-FIELD … since 2026-11-30`; run as of 2026-11-30 → excused |
| TC-TE-011-07 | AC7, BR2 | -004 | `src/modules/recovery/caserecord/*.tsx` with `console.log(customer.lastName)`; PDPA-LOG-FIELD naming `lastName` |
| TC-TE-011-08 | AC8 | -010 | Log line passing `contact_value` through the configured helper → no finding for that line |
| TC-TE-011-09 | AC9, BR2 | -006 | `throw new …Exception("No case for " + customer.getCifNo())` → PDPA-EXCEPTION for `cif_no` |
| TC-TE-011-10 | AC10, BR5 | -007 | `ContactEntity` whose `toString()` includes `contactValue`, and a `record` with component `contactValue` and no `toString()` → PDPA-TOSTRING for `contact_value` |
| TC-TE-011-11 | Access, X11 | -014 | Allow-list change approved only by a non code owner → merge refused. Real repository host only; `BLOCKED` locally until OPEN-038 and RWB-TE-002 (ASM-TE011-17) |

Additional system tests (the full lint against synthetic fixture trees; TS-TE011-01..03 added after spec gate round 4, -04 and -05 after round 5, -06 and -07 after round 6, -08 and -09 after round 7):

| ID | SPEC | Fixture and assertion |
|---|---|---|
| TS-TE011-01 | -001, -008, -011, -016, -017 | **Dictionary seed tables raise no finding.** It uses a synthetic migration shaped like RWB-E1-001's baseline. It holds a multi-row and a single-row `INSERT INTO ${recoverySchema}.sys_fields (field_id, object_name, field_name, …, source_system, source_field, is_personal, description, owner_role)`. Those rows mark `description`, `owner_role`, `field_name` and `source_system` personal on synthetic business objects (for example `case_note.description`, `team_assignment.owner_role`). It also holds `INSERT INTO ${recoverySchema}.sys_objects (…, description)` and `INSERT INTO ${recoverySchema}.data_product (…, owner_role, owner_user_id)` with `owner_role = 'RW-DATASTEW'` and `owner_user_id` `NULL`. All values are non-`SYN-` text. **Assert:** 0 FIXTURE-FIELD findings on every `sys_fields`, `sys_objects` and `data_product` row. **Assert:** exactly 1 finding on a business-table row in the same file (`INSERT INTO case_note (description) VALUES ('<free text>')`). **Assert:** an allow entry whose path matches the file gives exit 2. **Dictionary scope** (review SG6-03): the test dictionary is the PS v6 copy as baseline, then the synthetic migration's own `sys_fields` rows. The baseline describes every column of the six seed tables that the synthetic INSERTs use, each by a non-personal row on its own table (0 undescribed, SRC-28). The test asserts this before it runs the lint, so a seed column cannot be resolved by accident. **Negative variant:** the same file with `INSERT INTO ${recoverySchema}.lov_value (…, reviewer_name) VALUES (…, '<text>')`, where `reviewer_name` is marked personal only on `case_note` and is not described on `lov_value` (an unambiguous name on an undescribed pair) → exactly 1 PDPA-FIXTURE-FIELD finding for `reviewer_name`. |
| TS-TE011-02 | -001, -008 | **Point in time.** Migration A seeds `x.col` with a literal. Migration B marks (`x`, `col`) personal. **Assert:** no finding on A and one notice naming A's file and line. **Assert:** a test SQL fixture outside the migration folder that writes `x.col` with a literal gives a finding. |
| TS-TE011-03 | -001, -008 | **Source-field key.** A test SQL fixture `INSERT INTO public.customer (surname) VALUES ('<text>')`, with the test dictionary row `v_ace_customer.last_name` and source field `public.customer.surname`, gives PDPA-FIXTURE-FIELD for `last_name (surname)`. |
| TS-TE011-04 | -002, -008 | **Objects outside the dictionary are unresolved** (review SG5-01). Test dictionary: the PS v6 copy. (a) SQL fixture `INSERT INTO it_customer (first_name) VALUES ('<text>')`, where `it_customer` has no dictionary row → PDPA-FIXTURE-FIELD for `first_name`; the same with `'SYN-FIRST-0001'` → none. (b) TypeScript test fixture typed `components["schemas"]["InteractionRequest"]` with `summary: '<text>'` → PDPA-FIXTURE-FIELD for `summary`; with a `SYN-` value → none. (c) The same for `TimelineItem` → finding. (d) A test dictionary that adds a non-personal `summary` row on another object makes `summary` ambiguous; (b) still gives a finding, because `summary` is an API personal name (DGL-15). (e) Under a union-shaped test dictionary, `INSERT INTO public.address (address) VALUES ('<text>')` → PDPA-FIXTURE-FIELD for `address`. In every case the output holds no fixture value. |
| TS-TE011-05 | -008 | **SQL with no named column** (review SG5-03). (a) `INSERT INTO case_note VALUES ('<text>')` → PDPA-FIXTURE-FIELD `(columns not named)`. (b) A `COPY case_note FROM stdin` block with one data row → the same finding. (c) `INSERT INTO case_note DEFAULT VALUES` → none. (d) The same as (a) in the migration folder with an allow entry on it → exit 2 (SPEC-TE011-011). The output holds no data value. |
| TS-TE011-06 | -003, -008, -011, -012, -013, -018 | **Corrective migration** (review SG6-01). Migration folder with O = `V0003__rwb_e1_042_seed.sql` (line 1 `-- Story: RWB-E1-042`) writing a non-`SYN-` literal into a personal pair. (a) O alone → exit 1. (b) Add C = `V0010__rwb_e1_042_fix_seed.sql`, line 1 `-- Story: RWB-E1-042`, line 2 `-- Fix: replace seed value; corrects V0003__rwb_e1_042_seed.sql`, holding an `UPDATE` on O's table → exit 0, one `corrected by` notice naming O's line and C. (c) C with line 1 `-- Story: RWB-E1-043` → exit 1. (d) C whose line 2 names no file → exit 1. (e) C numbered `V0002` → exit 1. (f) C naming `V0099__rwb_e1_042_absent.sql` → exit 2. (g) C with no statement on O's table → exit 1. (h) C that itself writes a non-`SYN-` literal into a personal pair → exit 1, finding on C. (i) As (b), in a temporary git repository where the feature branch also edits O, so that `--changed-files-from-git develop-recovery --branch <feature branch>` lists O → exit 1 (as TS-TE011-09 (c)). (j) As (b), with an allow entry on O → exit 2. No output holds a value. |
| TS-TE011-07 | -008 | **SQL statement classes** (review SG6-01). One migration with: `INSERT … (<cols>) VALUES … ON CONFLICT (k) DO NOTHING`; `INSERT … (<cols>) VALUES … RETURNING id`; `INSERT … (<cols>) SELECT … WHERE NOT EXISTS (…)`; `CREATE TABLE IF NOT EXISTS`, `CREATE UNIQUE INDEX IF NOT EXISTS`, `ALTER TABLE … ADD CONSTRAINT`, `COMMENT ON`; a `DO` block with only `SELECT … INTO` and `RAISE`. **Assert:** 0 findings, and a non-`SYN-` literal placed in a personal column of each INSERT form gives exactly one finding per form. Also in that migration: a `DO` guard `IF NOT EXISTS (SELECT 1 FROM pg_constraint …) THEN ALTER TABLE … ADD CONSTRAINT …; END IF;`, a `DO` guard with `EXECUTE format('ALTER TABLE %I.t ADD CONSTRAINT …', …)`, and `DROP FUNCTION IF EXISTS f()`; still 0 findings. Separate files: `MERGE INTO case_note …` → 1 finding `(statement not recognised)`; a `DO` guard with `EXECUTE 'ALTER TABLE ' || v` → 1 finding `(DML in procedural body)`; `ALTER TABLE case_note ADD COLUMN description text DEFAULT '<text>'` with `case_note.description` personal → 1 PDPA-FIXTURE-FIELD finding; `CALL p()` → the same; a `DO` block holding `INSERT INTO case_note (description) VALUES ('<text>')` → 1 finding `(DML in procedural body)`; a `CREATE FUNCTION` trigger body with `INSERT … VALUES (NEW.c)` → none; a `DO` block with `EXECUTE 'CREATE TABLE t AS VALUES (''<text>'')'` → 1 finding `(DML in procedural body)`; a `DO` block with `CALL p()` → the same; a `DO` block with a direct `ALTER ROLE r SET search_path TO x` → the same; a `DO` block with `EXECUTE format('ALTER TABLE t %s', v)` → the same; a `DO` block with `COPY t TO STDOUT` → none. Output holds no SQL text. |
| TS-TE011-08 | -001, -003, -008, -009, -012, -018 | **Lint fixtures** (review SG7-01). A fixture tree mirrors RWB-E1-044 under `backend/src/test/resources/migration-lint/`, one folder per case, each file with line 1 `-- Story: RWB-E1-044`. The cases: N11 `INSERT INTO ${recoverySchema}.t (v) VALUES ('abc);`; N12 `/* not closed`; N13 `DO $q$ BEGIN NULL; END;`; `ALTER ROLE r SET search_path TO x;`, `ALTER DATABASE d SET search_path TO x;` and `ALTER FUNCTION f() SET search_path TO x;`; `INSERT INTO ${recoverySchema}.sys_fields (source_field) VALUES ('public.account.account_key');`; a file whose line 2 is `-- Fix: reason; corrects V0099__rwb_e1_044_absent.sql`. **Assert:** with the default configuration, exit 0 and 0 findings, plus a `PDPA-SCOPE: lint fixtures …` line with the file count. **Assert:** a valid-check-digit 13-digit number built at run time and written into a temporary copy of the N11 file gives exit 1 with one PDPA-FIXTURE-ID finding, and the number is absent from the output. **Assert:** the same tree under `backend/src/test/resources/other-sql/` (outside the class) gives exit 2 for N11 (T3), which shows the class is what keeps the merge green. **Assert:** a configuration that adds the lint-fixture root `backend/src/main/resources/db/**` gives exit 2 (T12). **Assert:** a lint-fixture root `backend/src/main/java/**` gives exit 2, `lint-fixture root outside the test roots` (T12). |
| TS-TE011-09 | -013, -018 | **Changed-file list** (review SG7-03, SG9-03). Every run passes `--branch` with the name of the branch under test, unless a case says otherwise. A temporary git repository has branch `develop-recovery` holding migration O (`V0003__rwb_e1_042_seed.sql`) with a non-`SYN-` literal in a personal pair. (a) A feature branch adds only the valid corrective C of TS-TE011-06 (b). `--changed-files-from-git develop-recovery` lists C only → exit 0, one `corrected by` notice. (b) A feature branch adds O and C together → O is on the list → exit 1. (c) A feature branch edits O and adds C → exit 1. (d) A configuration with `changedFiles.targetBranch: no-such-branch` and `--changed-files-from-git no-such-branch` → exit 2. (e) `--branch develop-recovery` → the list is not built, one `PDPA-SCOPE: changed-file list not built` line, and exit 1 from the uncorrected O (the absence of a git call is checked in the unit row). (f) A feature branch adds O2 (`V0004__rwb_e1_042_seed2.sql`), holding a `DO` block with `CALL p()`, together with C2 naming O2 (a finding with no target table). O2 is on the list → exit 1 (review SG8-01). (g) A feature branch from an unrelated history (an orphan branch) → `no merge base` → exit 2 (T14). (h) A branch named `develop` holds O and C, built from a squashed promotion of `develop-recovery` (one commit adding both, C meeting (a) to (d)); `--changed-files-from-git origin/develop-recovery --branch develop` → the list is not built, exit 0, one `corrected by` notice (T15). (i) The same tree with `--changed-files-from-git origin/develop --branch develop-recovery`, as in a promotion merge request → not built, exit 0. (j) `--changed-files-from-git origin/develop-recovery --branch main` in a clone that has no `develop-recovery` → not built, no exit 2. (k) `--changed-files-from-git develop-recovery` without `--branch`, and with `--branch HEAD` → exit 2, `branch not determined`. (l) The squashed-promotion tree of (h), run with no changed-file option as a GitLab tag pipeline runs it → the list is not built, one `PDPA-SCOPE: changed-file list not built` line, exit 0 and one `corrected by` notice (T15). |

Additional unit-level scenarios (testing standards §3 "Engineering enabler: one test per business rule
and test case"; positive, negative, boundary, error):

| Area | Scenarios |
|---|---|
| Reader (-001), read forms | **R1** single-row INSERT by column name, with columns reordered. **R1** multi-row INSERT (3 rows, mixed `true`/`false`). Qualifiers `${recoverySchema}.`, `recovery.` and `"sys_fields"`. `is_personal` column omitted → `false`. `source_field` key kept. **R2** `UPDATE … WHERE field_id = '<id>'`. **R2** `UPDATE … WHERE field_id IN (…)`. `is_active = false` row still listed. API `x-personal-data` camel → snake with the schema object. |
| Reader (-001), ignored forms | `UPDATE sys_fields SET description = … WHERE object_name = …` leaves the list unchanged. `CREATE TABLE`, `CREATE INDEX`, `COMMENT ON`, `ALTER TABLE … ADD CONSTRAINT` and a view reading `sys_fields` are ignored. A foreign key in another table that references `sys_fields` (in `CREATE TABLE` and in `ALTER TABLE … ADD CONSTRAINT … REFERENCES sys_fields`) is ignored. `sys_fields` inside a string literal, a `--` comment, a `/* */` comment or a dollar-quoted string is not a statement target. The PS v6 copy reads without exit 2 and yields 18 fields. |
| Reader (-001), fail closed, one scenario each, each exit 2 with file and line and no SQL text in the output | `UPDATE … SET is_personal = true WHERE object_name = '…'`. `UPDATE … SET is_personal = (SELECT …)`. `UPDATE … SET field_name = …`. `DELETE FROM sys_fields …`. `TRUNCATE sys_fields`. `COPY sys_fields FROM …` and `\copy`. `INSERT INTO sys_fields … SELECT …`. `INSERT … ON CONFLICT … DO UPDATE SET is_personal = …`. `MERGE INTO sys_fields`. `ALTER TABLE sys_fields ALTER COLUMN is_personal …`. `DROP TABLE sys_fields`. A `DO $$ … sys_fields … $$` block. An INSERT whose `is_personal` is a function call. An `UPDATE` naming an unknown `field_id`. A duplicate `field_id` INSERT in two migrations. |
| Reader (-001), order and notices | A migration row replaces a baseline row. A baseline row not replaced stays. A `true` → `false` change by replacement or by R2 is applied with one `PDPA-NOTICE` naming the field ID only, and the exit code is unchanged. Missing file → exit 2. Empty union → exit 2. |
| Generator (-002) | Variants for `id_no_last4` (digits), `extracted_fields`; entity names with suffixes; API personal names listed from `x-personal-data` (camel → snake); byte-identical output on two runs |
| Check digit (-009) | Valid and invalid check digit; dashed form; 12 and 14 digits; digit-adjacent match rejected |
| Mobile / e-mail (-009) | Every failing value assembled at run time (never stored): national 3-3-4 form, `+66` 2-3-4 separated form, bare `66` form; `example.com`, `sub.example.org`, `x.test` pass; an address in another domain, built at run time, fails |
| Self-scan (-003, -009) | A stored FIXTURE-ID match under `tools/pdpa-lint/**` fails the build; FIXTURE-FIELD is not applied there |
| Log rules (-004..-006) | Field name inside a string literal → no finding; concatenation, `String.format`, template literal → finding; non-logger method → no finding |
| TOSTRING (-007) | Record with explicit `toString()` excluding the field → no finding; class without personal member → no finding |
| Fixture field (-008) | `NULL`, empty string and `DEFAULT` → no finding. DATE literal → finding. JSON nested key. Builder call. **Object scoping:** `INSERT INTO listing (status)` with only `recovery_case.status` personal → no finding; `INSERT INTO recovery_case (status)` → finding; multi-row VALUES checked row by row; a literal in `INSERT … SELECT` at a personal column → finding. **Resolution:** a `CustomerEntity` setter → `v_ace_customer`; `@Table(name = …)`; a schema.d.ts type; a `fixtureObjects` glob for JSON. **Unresolved:** an unambiguous name (`lastName`) → finding; an ambiguous name (`status`) → notice and no finding. **Described pairs (SG5-01):** an `INSERT` into a table with no dictionary row: an unambiguous name gives a finding, an ambiguous name gives a notice. `@Table(name = "<undescribed>")` with a setter of an unambiguous name → finding. A TS fixture typed as an API schema with no `x-personal-data` (`InteractionRequest.summary`) → finding. A described object with a field the dictionary does not describe on it, carrying an unambiguous name → finding. A described pair that is not personal (`listing.status`) → no finding and no notice. An API personal name made ambiguous in the test dictionary, in an API-typed position → still a finding. **No named column (SG5-03):** column-less `INSERT … VALUES` with a literal → finding `(columns not named)`; with only `NULL`/`DEFAULT` → none; column-less `INSERT … SELECT` with a literal → finding; without a literal → none; `COPY … FROM stdin`, `COPY … FROM '<file>'` and `\copy … from` → finding; `COPY … TO` → none. SQL in a Java string → no FIXTURE-FIELD. |
| Scan scope (-003) | Migration folder from `rwb.flyway.location` in a test `application.yaml`: `classpath:db/modulemigration/recovery` → `backend/src/main/resources/db/modulemigration/recovery`; property missing → exit 2; a `${…}` placeholder → exit 2; `dictionary.migrationFolder` set to a different path → exit 2; set to the same path → accepted. A lint-fixture root that covers a migration file or probe path → exit 2. A lint-fixture file with an unterminated literal → no exit 2; with a run-time-built ID → PDPA-FIXTURE-ID. A file under both a lint-fixture root and the test root is in the lint-fixture class only. An exclusion `backend/src/main/resources/db/**` → exit 2 naming `exclusions[n]`. An exclusion `**/V0003__*.sql` that matches one migration → exit 2. A roots list without the migration class → exit 2 naming the root key, also with an empty migration folder (probe paths). A lint-fixture root `backend/src/main/java/**` or `infra/**` → exit 2, `lint-fixture root outside the test roots`; a root `backend/src/test/resources/x/**` → accepted. An exclusion that matches no migration (`node_modules`) → accepted, and the `PDPA-SCOPE:` line gives its file count. |
| SQL statement classes (-008) | One scenario each, on a non-`sys_fields` table: `ON CONFLICT … DO NOTHING`, `ON CONFLICT … DO UPDATE SET c = 'lit'` (a position) and `SET c = EXCLUDED.c` (not a position), `RETURNING`, `WHERE NOT EXISTS` on `INSERT … SELECT`, a read-only `WITH` prefix, `UPDATE … FROM … WHERE`. A cast literal `'x'::text` counts as a literal. Each class 2 form → no FIXTURE-FIELD. `MERGE`, `CALL`, `EXECUTE`, `SELECT … INTO t`, `CREATE TABLE … AS`, a data-modifying `WITH`, an unknown keyword → `(statement not recognised)`. `DO` with `INSERT`, `UPDATE`, `MERGE`, `COPY … FROM`, or `EXECUTE 'INSERT …'` → `(DML in procedural body)`. `DO` with `EXECUTE 'CREATE INDEX …'` → none. A function body `INSERT` with a personal literal → finding. A `sys_fields` target in any of these in the migration folder → exit 2 (reader precedence). **Reader precedence limited (SG7-01):** `INSERT INTO sys_fields (source_field) VALUES ('<text>')` in a test `.sql` file outside the reader's files → no exit 2, checked as a position (`sys_fields.source_field` is described and not personal → no finding); the same statement in the migration folder → exit 2. **DO bodies (SG7-02):** a direct `ALTER TABLE … ADD CONSTRAINT` guard → none; `EXECUTE format('<DDL literal>', …)` → none; `EXECUTE` of a concatenation → `(DML in procedural body)`; `DELETE` and `TRUNCATE` in a body → none. `DROP FUNCTION IF EXISTS` and `ALTER FUNCTION … OWNER TO` → none. **Body catch-all (SG8-03):** `CALL p()` in a `DO` body → `(DML in procedural body)`; a direct `ALTER ROLE … SET search_path` in a `DO` body → the same; `EXECUTE 'CREATE TABLE t AS …'` and `EXECUTE format('CREATE TABLE %I AS SELECT …', …)` → the same; `EXECUTE 'ALTER SYSTEM …'` → the same; a direct `GRANT` or `SET` in a `DO` body → none; `FETCH` from a cursor → none; `CALL p()` in a function body → `(DML in procedural body)`; `EXECUTE format('ALTER TABLE %I ADD COLUMN c text DEFAULT %L', …)` → the same. **`EXECUTE` text and the class-2 list (SG9-02):** `EXECUTE format('ALTER TABLE t %s', v)` → `(DML in procedural body)`; `EXECUTE format('ALTER TABLE %I ADD COLUMN %I text DEFAULT ''<text>''', …)` → the same (pair not resolvable); `EXECUTE 'ALTER TABLE case_note ADD COLUMN description text DEFAULT ''<text>'''` with `case_note.description` personal → 1 PDPA-FIXTURE-FIELD finding for `description`, and with `''SYN-…''` → none; `EXECUTE format('COMMENT ON TABLE %I IS %L', …)` → none; `EXECUTE format('ALTER TABLE %1$I ADD CONSTRAINT ck CHECK (c IN (%2$L))', …)` → `(DML in procedural body)`; `EXECUTE format('ALTER TABLE %I ADD CONSTRAINT ck CHECK (c LIKE ''A%%'')', …)` → none (`%%` is a literal); `COPY t TO STDOUT`, `LOCK TABLE t` and `COMMIT` in a `DO` body → none; `COPY t FROM stdin` in a `DO` body → `(DML in procedural body)`. `CREATE TABLE t AS SELECT …` → `(statement not recognised)` only. **DEFAULT literal:** `ADD COLUMN c … DEFAULT '<text>'`, `SET DEFAULT '<text>'` and `CREATE TABLE (c … DEFAULT '<text>')` on a resolved personal pair → finding; with `'SYN-…'`, `NULL` or `now()` → none; on a non-personal pair → none; `CHECK (c <> '<text>')` → none. |
| Corrective migration (-018) | **Scope:** a test `.sql` file outside the migration folder whose line 2 names an unknown file → no exit 2 and no corrective parsing. **Target table per finding kind:** FIXTURE-ID in an `INSERT` value → that table (needs an `UPDATE`/`DELETE`/`TRUNCATE` on it); FIXTURE-ID in a `--` comment or in `COMMENT ON TABLE t` text → none (accepted on (a) to (c) and (e)); FIXTURE-ID in an `ADD COLUMN … DEFAULT` → that table, needs an `UPDATE` and `ALTER COLUMN … DROP DEFAULT`; FIXTURE-ID in a `COPY t FROM stdin` data block → `t`; **SG9-01:** FIXTURE-ID in a `DO`-body `INSERT INTO t (c) VALUES (…)` → `t`, and C without an `UPDATE`/`DELETE`/`TRUNCATE` on `t` is not accepted; the same in a function-body `INSERT` → `t`; `(DML in procedural body)` for a `DO` block with `INSERT INTO t …` → `t`, and for a block holding only `CALL p()` → none; **SG10-02:** a `DO`-body `CREATE TABLE t AS VALUES (…)` → `t`; a FIXTURE-ID in a `DO`-body `MERGE INTO t` → `t`; `EXECUTE 'INSERT INTO t (c) VALUES (…)'` in a `DO` body → `t` for both the `(DML in procedural body)` finding and a FIXTURE-ID in its value; in each case C without a write on `t` is not accepted; `EXECUTE format('INSERT INTO %I …', …)` → none (no readable table); `(statement not recognised)` on `MERGE INTO t` → `t`; a `DEFAULT` position → needs an `UPDATE` and `ALTER COLUMN … DROP DEFAULT`. Line-2 token parsing: one name, two names, a name with no `-- Fix:` prefix (not counted), an empty reason (not accepted). Version order by `<seq>`. Story key compared exactly. Target table with and without a schema qualifier. `DELETE` and `TRUNCATE` count as well as `UPDATE`. An unknown named file → exit 2. A finding with no target table (a `DO` body holding only `CALL p()`) accepted on (a) to (c) and (e); the same with O on the changed-file list → still a finding; the same with the list not built (branch `develop`) → accepted on (a) to (c), (e) not evaluated. |
| Changed-file list (-013) | **Decision before any git command (SG9-03):** target `develop-recovery` or `origin/develop-recovery` with branch `feature/x` → built; target `origin/develop` or `main` → not built; branch `develop-recovery`, `main` or `develop` → not built; a branch added to `changedFiles.protectedBranches` → not built; no option (tag pipeline) → not built; `--changed-files-from-git` without `--branch`, with an empty `--branch` or with `--branch HEAD` → exit 2 `branch not determined`, before any git command. Not built → one `PDPA-SCOPE: changed-file list not built` line, no git command (a mock git runner records no call) and condition (e) not evaluated. **When built:** merge base and `--diff-filter=AMR` with a temporary repository: added, modified and renamed files listed; deleted files not listed; paths relative to the repository root; the target branch absent → exit 2; no merge base (unrelated histories, and a depth-1 clone) → exit 2 `no merge base`, never an empty list. |
| Allow list (-011) | Missing `owner`, `reason` or `expires` → exit 2. Both `line` and `pattern` → exit 2. `line` match. `pattern` match. Unused expired entry → exit 0. A `path` glob matching a file in the migration folder (exact path, and a broad `**/*.sql`) → exit 2. |
| Output (-012) | Sort order. Exit codes. A parse error prints no source text. Notices follow the findings, carry no value and leave the exit code unchanged, including the `corrected by` notice. `PDPA-SCOPE:` lines follow the notices and carry paths, branch names and counts only. |

All test data is synthetic. Any value that would match a FIXTURE-ID pattern is built at run time and
never stored (SRC-01 §17).

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| SRC-01 §4.1 | Read personal fields from the sys_fields seed and the API specification | SPEC-TE011-001 | DIRECT | Union; fail closed | COVERED |
| SRC-01 §4.2 | Generate the rule set: getter, entity class, JSON and TS property names | SPEC-TE011-002 | DIRECT | Entity names per SRC-04 step 2 resolution | COVERED |
| SRC-01 §4.3 | Scan main and front-end source for log calls, string building and exception messages | SPEC-TE011-003, -004, -005, -006 | DIRECT | Roots are configuration | COVERED |
| SRC-01 §4.4 | Scan tests, e2e, SQL seeds, JSON fixtures for non-SYN literals and ID/mobile/e-mail patterns | SPEC-TE011-003, -008, -009 | DIRECT | BR4 applied to all roots | COVERED |
| SRC-01 §4.5 | Entities exclude personal fields from their text form | SPEC-TE011-007 | DIRECT | Records and explicit `toString()` | COVERED |
| SRC-01 §4.6 | Compare findings with the allow list; expired entry does not excuse | SPEC-TE011-011 | DIRECT | | COVERED |
| SRC-01 §4.7 | Fail on any finding; print rule, file, line, field; never the value | SPEC-TE011-012, -013 | DIRECT | | COVERED |
| BR1 | Field list from dictionary and API spec, never in the lint | SPEC-TE011-001, -002, -015 | DIRECT | Dictionary as seeded and changed by migrations; (object, field) keys; reader fails closed on unsupported `sys_fields` statements | COVERED |
| BR2 | No log statement, log string or exception message carries a personal field or entity | SPEC-TE011-004, -005, -006 | DIRECT | | COVERED |
| BR3 | Fixtures carry only `SYN-` values in personal fields | SPEC-TE011-008 | DIRECT | Non-text fields strict (DGL-08) | COVERED |
| BR4 | Valid Thai ID, Thai mobile, non-example e-mail fail anywhere | SPEC-TE011-009 | DIRECT | Patterns are labelled assumptions | COVERED |
| BR5 | Entity text form excludes personal fields | SPEC-TE011-007 | DIRECT | | COVERED |
| BR6 | Excused only by an entry with owner, reason, unexpired expiry | SPEC-TE011-011 | DIRECT | | COVERED |
| BR7 | Lint never prints the value | SPEC-TE011-012 | DIRECT | Asserted in every TC | COVERED |
| X1–X11 | Exception paths | SPEC-TE011-004..-014 | DIRECT | See exceptional-case table | COVERED |
| AC1–AC10 | Acceptance criteria | SPEC-TE011-004..-011 | DIRECT | TC-TE-011-01..10 | COVERED |
| SRC-01 §10 | Authority: tech leads approve allow-list and rule changes | SPEC-TE011-014 | DIRECT | Depends on RWB-TE-002 | COVERED |
| SRC-01 §12 Trigger | Every pull request and every build of main | SPEC-TE011-013 | DIRECT | | COVERED |
| SRC-01 §12 Idempotency / Restart | Same commit and dictionary → same findings; no state | SPEC-TE011-002, -012 | DIRECT | | COVERED |
| SRC-01 §13 Configuration | Prefix, example domains, allow list are configuration | SPEC-TE011-015 | DIRECT | | COVERED |
| SRC-01 §13 Done when | Tests pass and lint runs on main with zero findings | SPEC-TE011-016, -017 | DIRECT | Zero findings at this merge and every later merge, including RWB-E1-001's under the protective union; measured against the dictionary as seeded and changed by migrations (residual risk stated) | COVERED |
| SRC-01 §11 Data | The lint reads the definitions of the listed fields (DF-ACE-055/057/058/073/059/061/078, DF-EXT-002/004, DF-INT-011, DF-DOC-015), never their values | SPEC-TE011-001, -016, -017 | DIRECT | Read through the dictionary. `cif_no`, `vulnerable`, `deceased_flag`, `bankruptcy` are `is_personal = false` in the PS v6 seed, so in production they are covered once a migration marks them: at RWB-E1-001's merge if it seeds the protective union, otherwise when a later migration does (DGL-01, OPEN-NEW-TE011-1); the test dictionary marks `cif_no` for AC9 | COVERED |
| SRC-01 §13 Feature flag | None; build check has no runtime path | SPEC-TE011-013 | INHERITED_EXISTING_BEHAVIOR | No flag added | COVERED |
| SRC-01 §17 | Guardrails: no business value in code; no personal data, run-time check-digit fixtures; files only; allow entry has owner and expiry | SPEC-TE011-001, -009, -011, -015 | DIRECT | | COVERED |
| REQ-RDF-010 | Personal data masked by role in line with PDPA | SPEC-TE011-008, -009, -011, -014 | DIRECT | The lint stops personal data bypassing masking via fixtures (SRC-01 §18) | COVERED |
| REQ-ACA-005 | Personal data masked by role on every screen and agent call | SPEC-TE011-004..-007, -010 | DIRECT | Log lines bypass masking (SRC-01 §2) | COVERED |
| NFR-054 (PDPA part) | Pipeline blocks personal data in code, tests or logs | SPEC-TE011-013 | DIRECT | Secret and dependency parts out of scope (§19) | COVERED |
| NFR-045 | No production data in development | SPEC-TE011-008, -009 | DIRECT | Via BR3/BR4 | COVERED |
| CTL-11 | Personal fields masked unless role may see them | SPEC-TE011-004..-007 | DIRECT | Build-time support of the control | COVERED |
| SRC-19 A-09 (PDPA part) | CI has no PDPA lint job | SPEC-TE011-013 | DIRECT | | COVERED |
| D-RCV-28; `AGENTS.md` §3.7, §4.6 | A merged migration is never edited; a corrective script takes the next sequence, keeps the story key and adds line 2 `-- Fix: <reason>` | SPEC-TE011-003, -008, -011, -013, -018 | DIRECT | Findings in SQL merged by orders 1–5 before this story are scanned at its merge; a corrective migration in the migration folder that names the original is the only remedy, with the changed-file list built in GitLab and in the local merge; the migration folder cannot be excluded and is read from `rwb.flyway.location`; unrecognised SQL fails closed; RWB-E1-044's lint fixtures get FIXTURE-ID only (review SG6-01, SG6-02, SG7-01..03) | COVERED |
| DL v10 D-RCV-29 | Later dictionary changes are reference loads through RWB-E1-043 | SPEC-TE011-001, -017 | DIRECT | The lint states the limit: load marks are not visible (committed files only, story §13/§17). Protecting marks on load is a seam owned by RWB-E1-064, the dictionary handler owner (D-RUN-08; orchestrator triage 2026-11-18T00:35), with the decision in RWB-E1-043 open item R4, owned by RW-COMPLY; DGL-13 | COVERED |

## Out of scope

- Secret scanning and dependency approval in the pipeline (NFR-052, NFR-054): ACE pipeline (SRC-01 §19).
- Masking rules by role at run time: RWB-E1-037 (SRC-01 §19).
- Masked data in SIT and UAT: RWB-TE-004 (SRC-01 §19).
- Which fields are personal and how long they are kept: DL26, Compliance (SRC-01 §19; SRC-22).
- A-07: raw exception text in `ApiExceptionHandler` and the Problem `traceId`: RWB-TE-003 (D-RUN-15). `X-Correlation-Id` is not built (D-RUN-15; see "Scope decisions").
- A-09: contract, dependency scan, ZAP, Playwright/axe and coverage-verification jobs (see "Scope decisions").
- Publishing the masking helper: common module (OPEN-024).
- Writing the CODEOWNERS file and branch rule: RWB-TE-002.
- Protecting `is_personal` marks against D-RCV-29 dictionary loads, and the dictionary load handler: RWB-E1-064 (seam, SPEC-TE011-017; DGL-13), with the decision in RWB-E1-043 open item R4 (RW-COMPLY). The load pipeline (version log, change summary, approval): RWB-E1-043.
- Policing run-time loads of any kind: the lint covers committed SQL migrations, fixtures and log statements only.
- Aligning the `x-personal-data` marks of API Specification v4: the API owner with RW-COMPLY (DGL-15, OPEN-NEW-TE011-8). The lint already treats the unmarked `summary` properties as personal.
- Reading a database or loaded dictionary versions: forbidden by story §13 and §17.
- Seeding the protective classification: RWB-E1-001 (`ASM-E1001-14`), which must pass this lint (SPEC-TE011-017).

## Pending Design Evidence

None. `UI In Scope = NO`; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`.

## Clarification Log

No question was asked (L-RCV-03; RUN-BRIEF rule 4). Each item is resolved by a documented default and
listed for confirmation at the plan gate.

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR1, AC9; DGL-01 | Sources disagree on which fields are personal; the seed does not mark `cif_no`, `contract_no` or the sensitive flags | Production coverage of the lint | Story §12 names the seed + API; DL26 owns classification. Proposed open item for Compliance. | RESOLVED (precedence: story §12) | SPEC-TE011-001, -016 |
| CLAR-002 | §3 precondition 4; AC8 | Masking helper not published | AC8 and the production exemption | Configurable list; empty in production; test config proves AC8 (ASM-TE011-07) | RESOLVED (ASM) | SPEC-TE011-010 |
| CLAR-003 | BR4 | Example domains, Thai mobile pattern, check-digit algorithm not defined | Pattern accuracy | Labelled defaults in configuration (ASM-TE011-08..10) | RESOLVED (ASM) | SPEC-TE011-009, -015 |
| CLAR-004 | BR3 | `SYN-` cannot apply to DATE and NUMBER personal fields | Fixtures for `date_of_birth`, GPS fields | Strict: any literal is a finding. Outside the migration folder it can be allow-listed; in the migration folder no allow entry applies, so the value must be `NULL` (DGL-08; SPEC-TE011-008) | RESOLVED (ASM) | SPEC-TE011-008 |
| CLAR-005 | SRC-04 step 2 | Entity class names in flow vs §13 RuleGenerator | AC2 | Generate them; suffixes `Entity`, `View` (ASM-TE011-04) | RESOLVED (story flow + AC2) | SPEC-TE011-002, -005 |
| CLAR-006 | SRC-04 step 4 | AC3 value generated at run time vs literal scan | AC3 | Test writes the generated value to a temp file the lint scans | RESOLVED (story §17) | SPEC-TE011-009 |
| CLAR-007 | §10, X11 | Code owners come from RWB-TE-002, which is not built; host unconfirmed | TC-TE-011-11 | Add entry to section `[Recovery module]` of `.gitlab/CODEOWNERS` (SRC-23); TC-11 `BLOCKED` locally (OPEN-038) | RESOLVED (ASM) | SPEC-TE011-014 |
| CLAR-008 | AC1 vs AC7 | Output names `first_name` (AC1) but `lastName` (AC7) | Output format | Dictionary name plus matched token in parentheses (ASM-TE011-14) | RESOLVED (ASM) | SPEC-TE011-012 |
| CLAR-009 | BR3, §13 RuleGenerator; DGL-14 (review DG4-02) | The same field name is personal on one object and not on another; name-only fixture matching flags dictionary and reference seeds | FIXTURE-FIELD positions; RWB-E1-001 merge | Orchestrator triage 2026-11-18: match SQL and fixtures by (object, field), never by name alone; no allow entry for a migration. Unresolved objects: unambiguous names only, ambiguous names reported as notices (ASM-TE011-20) | RESOLVED (orchestrator triage; `sys_fields.object_name`) | SPEC-TE011-001, -002, -008, -011, -016 |
| CLAR-010 | BR1; DL v10 D-RCV-29; DGL-13 (review DG4-01) | Later dictionary changes are reference loads, which a files-only lint cannot see | Production coverage claim | Precedence: Decision Log v10 over story files v7 for the route. The lint stays files-only (story §13/§17). Claim narrowed to the dictionary as seeded and changed by migrations. Protecting marks on load is a seam owned by RWB-E1-064, the dictionary handler owner (D-RUN-08; orchestrator triage 2026-11-18T00:35), with the decision in RWB-E1-043 open item R4, owned by RW-COMPLY | RESOLVED (precedence + D-RUN-08 + orchestrator triage) | SPEC-TE011-001, -016, -017 |
| CLAR-011 | BR1, BR3; DGL-15 (review DG5-01) | API Specification v4 marks `Interaction.summary` personal but not `InteractionRequest.summary` or `TimelineItem.summary`, although DF-INT-011 is personal | Fixtures typed by those schemas | Protective reading: the schemas are outside the dictionary, so the positions are unresolved and `summary` is checked by name. An API personal name in an API-typed position is a finding even if the dictionary name becomes ambiguous (ASM-TE011-24). Alignment of the marks goes to the API owner with RW-COMPLY (OPEN-NEW-TE011-8) | RESOLVED (protective reading; ASM) | SPEC-TE011-002, -008 |
| CLAR-012 | D-RCV-28; `AGENTS.md` §3.7, §4.6; review SG6-01 | The lint runs over SQL that orders 1–5 merged before it, and a merged migration cannot be edited or allow-listed | This story's merge; findings in earlier migrations | Orchestrator triage 2026-11-18T01:02: a corrective migration under the original story key, named on its line 2, is the only remedy, and the lint recognises it (conditions (a) to (e)). Unrecognised statement forms and DML in `DO` blocks fail closed. The planners of orders 1–5 are told the rules (ASM-TE011-26, -27) | RESOLVED (orchestrator triage) | SPEC-TE011-008, -016, -017, -018 |
| CLAR-013 | BR1, §17; review SG6-02 | Scan roots and exclusions are configuration, so a configuration could leave the migration folder out | Migration coverage | Orchestrator triage 2026-11-18T01:02: no configuration can exclude the folder; such a configuration fails with exit 2, and the exclusions in force are printed with file counts | RESOLVED (orchestrator triage) | SPEC-TE011-003, -012, -015 |
| CLAR-014 | BR3, BR4; RWB-E1-044 T-044-20..22; review SG7-01 | RWB-E1-044 (order 1) commits SQL fixtures that are malformed or outside the statement classes on purpose; they would give exit 2 or findings at this story's merge | This story's merge condition | Orchestrator triage 2026-11-18T04:54: a code-owner-reviewed lint-fixture class, default `backend/src/test/resources/migration-lint/**`, gets FIXTURE-ID only on the raw text and never gives exit 2; it cannot cover the migration folder. Reader precedence and SPEC-TE011-018 apply only to the files they concern. This story adapts to RWB-E1-044 as specified (ASM-TE011-28) | RESOLVED (orchestrator triage) | SPEC-TE011-003, -008, -016, -018 |
| CLAR-015 | D-RUN-06; review SG7-03 | No GitLab pipeline runs in this repository, so a changed-file list built only in a merge request pipeline is never used; the expected migration path has no stated source | SPEC-TE011-018 condition (e); SPEC-TE011-003 | Orchestrator triage 2026-11-18T04:54: build the list from `git diff --name-only <merge-base>..HEAD` against `develop-recovery` in `scripts/dev.ps1 test`, which gates the local merge; read the migration folder from `rwb.flyway.location` (ASM-TE011-29). In GitLab branch pipelines the job passes `origin/<targetBranch>` with full history after a non-fatal fetch; tag pipelines pass no option; where the list is built, no merge base gives exit 2 (review SG8-04, SG10-01). The list is built only for a change into `develop-recovery` from a branch that is not protected; elsewhere, including GitLab tag pipelines, condition (e) is not evaluated (orchestrator triage 2026-11-18T05:13; review SG9-03, SG10-01) | RESOLVED (orchestrator triage) | SPEC-TE011-003, -013, -018 |

`CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]` — every item is settled by story text, precedence or a
labelled assumption; the assumptions and the proposed open items are carried to the plan gate.

## Status reporting

```text
MCP_STATUS_SUMMARY: No Jira, Confluence, GitLab or Figma MCP is connected (RUN-BRIEF rule 5); the story file was read from the document set.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New build-time PDPA lint in tools/pdpa-lint plus a CI job; no UI, no API, no application code change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: build tooling only; no prior trace chain]
REQUIREMENT_COVERAGE_SUMMARY: All 7 flow steps, 7 business rules, 11 exception paths, 10 ACs, §11 data, contract items, guardrails and 5 upstream requirements map to SPEC-TE011-001..018, plus D-RCV-28 (`AGENTS.md` §3.7, §4.6) and Decision Log v10 D-RCV-29.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 32] [COVERED_RULES: 32] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
```

Contradictions between sources are recorded in `document-gaps.md` (DGL-01..DGL-15); each is settled by
precedence or a labelled assumption, so none is left open in the coverage table.
